#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JSON 出片 —— 读 `04-提示词/分镜JSON.json`（或裸请求体），单镜出片。

**只根据 JSON 出片**：不做概念、不做歌词、不回写提示词；脚本只负责把 JSON 变成视频
（该组装就组装、该透传就透传），正文一字不改。

一、分镜 JSON（顶层 `shots[]`）——单镜调 Seedance 2.5，出片后裁到精确秒：
  {
    "project": "MV01-<名字>", "ratio": "9:16", "generate_audio": false,
    "shots": [
      {
        "id": "S01",
        "prompt": "<六段式全文>",              # ★ 原样透传（本 skill 的提示词已是最终正文）
        "refs_urls": ["https://…/04-图片/ref_人物.png"],
        "ref_audio_urls": ["https://…/00-输入/音频/S01.wav"],   # ★ 口型驱动源（每镜恰 1 条）
        "seconds": 16.7,                      # ★ 该镜长度，≤30
        "duration": 17,                       # ★ 整数 = ceil(seconds)
        "seed": 0,
        "mode": "reference",
        "resolution": ""                      # 可选：720p
      }
    ]
  }

二、裸请求体 JSON（顶层 `content[]`、无 `shots`）——直接就是 Seedance 建任务请求体：
  {"model": "…", "ratio": "9:16", "duration": 30, "generate_audio": false,
   "content": [{"type": "text", "text": "…"}, {"type": "image_url", "role": "reference_image",
               "image_url": {"url": "https://…/04-图片/ref_人物.png"}},
               {"type": "audio_url", "role": "reference_audio",
                "audio_url": {"url": "https://…/00-输入/音频/30s.wav"}}]}
  该模式**严格原样透传**：只把 content 里本地素材路径解析为 base64（http(s) 直传），
  其余键一字不改；一条请求出一支视频。

人物说唱口径（本 skill 默认）：
  - **口型由参考音频驱动**：`generate_audio:false`（JSON 未写时也默认 false）；
    声音不生成、片段无声，成片音轨由 `assemble.py` 贴回原声；
  - **必须有参考音频**：`ref_audio_urls` 恰 1 条，否则请求体里不会出现 `audio_url`，口型无驱动源；
  - **提示词原样透传**：六段式（① 一句话摘要 / ② 人物与参考图锁定 / ③ 时间轴说唱 /
    ④ 镜头与表演 / ⑤ 声音设计 / ⑥ 画风与强制约束）已是最终正文；
  - **单镜 ≤30 秒**：`shots` 1–4 条；40s 按信息段拆 3–4 镜，`seconds ≤ 30`、`duration = ceil(seconds)`；
  - **不做帧接续、不做视频延长**；
  - **精确秒**：`--exact-seconds` + `--enforce-seconds` 默认开；出片后长了裁尾、短了冻结末帧补齐；
  - **落点**：`<项目>/成片片段/S01.mp4 …`（逐镜平铺，每轮重出覆盖）；
  - **成本纪律**：先 `--dry-run` 看请求体，再出 1 条；`--workers` 默认 1。

素材解析：
  - `refs_urls` 为 http(s) 直链 → 直接投递（推荐先跑 `upload_project.py --verify --fill-json`）；
  - 本地路径 → 先按 JSON 目录解析，再按**项目根**解析（兼容 `04-图片/ref_人物.png`），
    最后回退 base64（单文件 >8MB 会告警）。

用法：
  # 先上传 + 回填直链（推荐）
  python3 scripts/upload_project.py assets/output/MV01-xxx --verify --fill-json
  # 干跑：只看组装后的请求体
  python3 scripts/generate_video.py assets/output/MV01-xxx/04-提示词/分镜JSON.json --dry-run
  # 正式出片
  python3 scripts/generate_video.py assets/output/MV01-xxx/04-提示词/分镜JSON.json
  # 重出（单镜只有 S01）
  python3 scripts/generate_video.py <分镜JSON.json> --only S01

环境变量：VIDEO_GATEWAY_BASE 覆盖网关（默认读 scripts/config.json 的 gateway_base）。
"""

from __future__ import annotations

import argparse
import base64
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Iterator, Optional

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import CLIPS_ROOT, project_root_for, video_api_config  # noqa: E402

DEFAULT_BASE = "http://127.0.0.1:4000"
DEFAULT_MODEL = "doubao-seedance-2-5-260628"
PASS_THROUGH_PATH = "/v1"  # 可用 --api-prefix / VIDEO_API_PREFIX / config.video_api_prefix 覆盖
CREATE_SUFFIX = "/api/v3/contents/generations/tasks"
TERMINAL_SUCCESS = {"success", "succeeded", "completed", "done"}
TERMINAL_FAILURE = {"failed", "error", "cancelled", "canceled"}
TRANSIENT_STATUS_CODES = {502, 503, 504}
TRANSIENT_DOWNLOAD_STATUS_CODES = {408, 429, 500, 502, 503, 504}

_IMAGE_MIME = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}
_AUDIO_MIME = {
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/mp4",
    ".aac": "audio/aac",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
}
_VIDEO_MIME = {
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
}
_MAX_BASE64_BYTES = 8 * 1024 * 1024

_SESSION = requests.Session()
_SESSION.trust_env = False

_LONG_MODES = {"text2video", "image2video_long", "extend"}
_REF_NAME_RE = re.compile(r"@([^\s@]+)")

_SKILL_ROOT = Path(__file__).resolve().parent.parent

# 相对素材的额外解析根（cli_main 会压入项目根，兼容 `图片/<kind>/图N.png`）
_EXTRA_ROOTS: list[Path] = []

# 延续素材上传：调用**调用方自带**的上传脚本（--uploader-script 显式指定，本 skill 不引用其他 skill）
_UPLOAD_MANIFEST_JSON = "素材外网路径.json"


def run_stamp() -> str:
    """出片时间戳（本地时间 `YYYYMMDD-HHMMSS`）：同一次运行的成片共用。"""
    return time.strftime("%Y%m%d-%H%M%S")


def drop_legacy_records(out_dir: Path, *names: str) -> None:
    """清除旧版本落盘的结果清单（`<name>.json` / `batch_result.json`）。

    新契约不记录清单，旧清单留着会和新成片对不上，所以重出时顺手清掉。
    """
    for name in names:
        stale = out_dir / name
        if stale.is_file():
            try:
                stale.unlink()
                print(f"  🧹 已清除旧结果清单 {stale.name}", flush=True)
            except OSError as exc:
                print(f"  ⚠ 旧结果清单删除失败 {stale}：{exc}", file=sys.stderr)


# ---------------------------------------------------------------- JSON 工具

def _walk_json(value: Any) -> Iterator[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child
            yield from _walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_json(child)


def _find_first(value: Any, keys: set[str]) -> Any:
    for key, child in _walk_json(value):
        if key.lower() in keys and child not in (None, ""):
            return child
    return None


def task_id_from(response: Any) -> Optional[str]:
    candidate = _find_first(response, {"task_id", "taskid", "id"})
    return str(candidate) if candidate is not None else None


def task_state_from(response: Any) -> Optional[str]:
    candidate = _find_first(response, {"status", "state", "task_status", "taskstatus"})
    return str(candidate).lower() if candidate is not None else None


def video_url_from(response: Any) -> Optional[str]:
    candidate = _find_first(response, {"video_url", "videourl", "url"})
    return str(candidate) if candidate is not None else None


# ---------------------------------------------------------------- 素材解析

def to_data_url(path: Path) -> str:
    suffix = path.suffix.lower()
    mime = _IMAGE_MIME.get(suffix) or _AUDIO_MIME.get(suffix) or _VIDEO_MIME.get(suffix)
    if not mime:
        raise ValueError(
            f"不支持的素材格式：{path}（图 JPEG/PNG/WebP；音 mp3/wav/m4a/aac/ogg/flac；视 mp4/mov/webm）")
    raw = path.read_bytes()
    if len(raw) > _MAX_BASE64_BYTES:
        print(
            f"  ⚠ {path.name} 原始 {len(raw) / 1024 / 1024:.1f} MB（>8MB），网关可能拒绝，建议压缩",
            file=sys.stderr,
        )
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def resolve_asset(value: str, base_dir: Path) -> Optional[str]:
    """素材 → url：http(s) 直传；本地路径（先 JSON 目录、再项目根）回退 base64。空值返回 None。"""
    value = (value or "").strip()
    if not value:
        return None
    if value.startswith(("http://", "https://")):
        return value
    path = Path(value)
    candidates: list[Path] = []
    if path.is_absolute():
        candidates.append(path)
    else:
        candidates.append(base_dir / path)
        for root in _EXTRA_ROOTS:
            candidates.append(root / path)
    found = next((p for p in candidates if p.is_file()), None)
    if found is None:
        print(f"  素材不存在：{candidates[0] if candidates else path}", file=sys.stderr)
        return None
    try:
        return to_data_url(found)
    except ValueError as exc:
        print(f"  {exc}", file=sys.stderr)
        return None


def resolve_list(values: Optional[list], base_dir: Path) -> list[str]:
    out: list[str] = []
    for v in values or []:
        url = resolve_asset(str(v), base_dir)
        if url:
            out.append(url)
    return out


def collect_audio_urls(shot: dict, base_dir: Path) -> list[str]:
    """兼容：ref_audio_urls（MV）、voice_urls（list 或 dict）、audio_url（单条）、dialogue[].audio_url。"""
    vals: list[str] = []
    raw = shot.get("ref_audio_urls") or shot.get("voice_urls")
    if isinstance(raw, dict):
        raw = list(raw.values())
    vals += resolve_list(raw, base_dir)
    au = shot.get("audio_url")
    if au:
        u = resolve_asset(str(au), base_dir)
        if u:
            vals.insert(0, u)
    for d in shot.get("dialogue") or []:
        u = d.get("audio_url")
        if u:
            u = resolve_asset(str(u), base_dir)
            if u:
                vals.append(u)
    return list(dict.fromkeys([x for x in vals if x]))


def resolve_video_url(value: str, base_dir: Path) -> str:
    """参考视频（extend 视频延长）：http(s) 直传；本地路径 → base64 data URL；空返回 ''。"""
    value = (value or "").strip()
    if not value:
        return ""
    if value.startswith(("http://", "https://")):
        return value
    path = Path(value)
    if not path.is_absolute():
        path = base_dir / path
    if not path.is_file():
        print(f"  参考视频不存在：{path}", file=sys.stderr)
        return ""
    try:
        return to_data_url(path)
    except ValueError as exc:
        print(f"  {exc}", file=sys.stderr)
        return ""


# ---------------------------------------------------------------- 延续素材上传（调调用方自带的上传脚本）

DEFAULT_UPLOADER = (Path(__file__).resolve().parent
                    / "material-uploader" / "upload_assets.py")


def find_uploader_script(explicit: str = "") -> Optional[Path]:
    """延续素材上传：默认用本 skill 内置 `scripts/material-uploader`；也可显式覆盖。

    `--uploader-script` > 默认 material-uploader > 找不到则回退 base64。
    """
    if explicit:
        path = Path(explicit).expanduser()
        return path if path.is_file() else None
    return DEFAULT_UPLOADER if DEFAULT_UPLOADER.is_file() else None


def upload_material(src_file: Path, prefix: str, uploader: Path,
                    staging_root: Path, timeout: int = 300) -> Optional[str]:
    """把延续素材上传为公网直链（调调用方自带的上传脚本，接口同 upload_assets.py）。

    staging → `--src <staging> --strip-root --prefix <prefix>`，目标 = /var/www/public/mv/<prefix>/<文件名>；
    `--keep-source` 保留源文件（尤其上一镜成片 mp4，后续合并仍需要）；`--overwrite` 重跑刷新。
    成功返回外链 URL；任何异常/非零退出/无成功项 → 返回 None（由调用方回退 base64）。
    """
    try:
        stage = staging_root / src_file.stem
        stage.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, stage / src_file.name)
        cmd = [
            sys.executable, str(uploader),
            "--src", str(stage), "--strip-root",
            "--prefix", prefix,
            "--keep-source", "--overwrite", "--json", "--quiet",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if proc.returncode != 0:
            print(f"  ⚠ 延续素材上传失败（退出码 {proc.returncode}）：{src_file.name}；"
                  f"回退 base64{(chr(10) + proc.stderr[-300:]) if proc.stderr else ''}", file=sys.stderr)
            return None
        manifest = stage / _UPLOAD_MANIFEST_JSON
        if not manifest.is_file():
            print(f"  ⚠ 未找到上传清单 {manifest}，回退 base64", file=sys.stderr)
            return None
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for item in data.get("items", []):
            if item.get("status") in ("ok", "skip") and item.get("url"):
                return str(item["url"])
        print(f"  ⚠ 上传清单无成功项：{src_file.name}，回退 base64", file=sys.stderr)
        return None
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ 延续素材上传异常：{src_file.name}（{exc}）；回退 base64", file=sys.stderr)
        return None


# ---------------------------------------------------------------- 提示词组装

def _strip_mouth(text: str) -> str:
    """剥掉口型/说话类分句（首尾帧干净模式无音频，不写口型）。"""
    return "；".join(p for p in (text or "").split("；") if ("口型" not in p and "开口说话" not in p))


def _append_once(text: str, piece: str, marker: str) -> str:
    """marker 未在 text 中出现时，把 piece 追加到末尾（去掉重复标点；空文本不加前导分隔符）。"""
    if not piece or (marker and marker in text):
        return text
    if not text.strip():
        return piece.lstrip("； \n")
    return text.rstrip("。；; \n") + piece


def apply_audio_control(text: str, generate_audio: bool) -> str:
    """把官方字幕/音频控制句追加到 text 末尾（空文本不加前导分号）。"""
    ctrl = audio_control_line(generate_audio)
    if not text.strip():
        return ctrl
    return text.rstrip("。；; \n") + "；" + ctrl


def _is_final_mv_prompt(body: str) -> bool:
    """判断提示词是否已是最终正文（MV 四段式 / 首帧动画 ① 正向提示词 / 素材清单）。

    命中则**原样透传**，不再拼 refs_line / voice_line / style_tail。
    """
    text = (body or "").strip()
    if not text:
        return False
    if text.startswith("素材：") or text.startswith("① 正向提示词"):
        return True
    return any(marker in text for marker in (
        "① 一句话摘要", "② 时间轴", "[主体与素材绑定]", "[全局约束]",
    ))


def compose_prompt_text(shot: dict, keyframes: bool = False) -> str:
    """text = refs_line + voice_line + prompt + style_tail。

    **不再把 `negative` 写进正文**：官方 Seedance 2.5 的负向只支持字幕/音频控制，
    风格/画质/结构类负向不生效、还会稀释正向描述；`negative` 字段仅作 QA 清单。
    首尾帧干净模式：只留动效正文（剥掉 refs_line/voice_line 与口型话术），仍补 style。
    """
    body = shot.get("prompt") or ""
    # MV 完整四段式：已经是最终正文，原样使用，不再拼 refs/voice/style
    if (not keyframes) and _is_final_mv_prompt(body):
        return body
    if keyframes:
        text = _strip_mouth(body)
    else:
        voice_line = (shot.get("voice_line") or "").strip()
        if not voice_line:
            ds = shot.get("dialogue") or []
            if ds:
                voice_line = "【声音】" + "；".join(
                    f"{d.get('speaker','')}：{d.get('text','')}" for d in ds if d.get("text")
                )
        refs_line = (shot.get("refs_line") or "").strip()
        if (not refs_line and shot.get("refs_urls")
                and "素材：" not in body and "参考图：" not in body):
            n = len(shot.get("refs_urls") or [])
            refs_line = ("参考图：图1 是主体形象参考" if n == 1
                         else f"参考图：图1–图{n} 是主体/场景参考")
        parts = [
            refs_line,
            voice_line,
            body.strip(),
        ]
        text = "\n".join(p for p in parts if p)

    style_tail = (shot.get("style_tail") or "").strip()
    if style_tail:
        text = _append_once(text, "；风格：" + style_tail, "风格：" + style_tail)
    return text


def compose_prompt_text_extend(shot: dict) -> str:
    """视频延长（extend）提示词：官方触发词 + 延续说明 + 本镜新增动作 + 风格尾句。

    官方规则：延长 role 需为 reference_video，ratio=adaptive，提示词含
    「向后延长 / 延续 / 续写」之一；建议用 mov 输出。
    """
    body = _strip_mouth(shot.get("prompt") or "")
    # MV 完整四段式延长：已含触发词/四段式，原样使用
    if "向后延长" in body or _is_final_mv_prompt(body):
        return body
    refs_line = "参考图：图1 是主体形象参考；" if shot.get("refs_urls") else ""
    text = refs_line + "向后延长@视频1，延续前视频的风格、主体、光影与镜头运动；" + body
    style_tail = (shot.get("style_tail") or "").strip()
    if style_tail:
        text = _append_once(text, "；风格：" + style_tail, "风格：" + style_tail)
    return text


def build_content(prompt: str, image_urls: list[str], image_role: str,
                  audio_urls: Optional[list[str]] = None, audio_role: str = "reference_audio",
                  first_frame_url: str = "", last_frame_url: str = "") -> list[dict]:
    content: list[dict] = [{"type": "text", "text": prompt}]
    # 严格首/尾帧用官方 role；其余参考图仍走 reference_image
    if first_frame_url:
        content.append({"type": "image_url", "role": "first_frame",
                        "image_url": {"url": first_frame_url}})
    if last_frame_url:
        content.append({"type": "image_url", "role": "last_frame",
                        "image_url": {"url": last_frame_url}})
    for url in image_urls:
        if url:
            content.append({"type": "image_url", "role": image_role, "image_url": {"url": url}})
    for url in audio_urls or []:
        if url:
            content.append({"type": "audio_url", "role": audio_role, "audio_url": {"url": url}})
    return content


def build_content_keyframes(prompt: str, first_frame_url: str, last_frame_url: str) -> list[dict]:
    content: list[dict] = [{"type": "text", "text": prompt}]
    if first_frame_url:
        content.append({"type": "image_url", "role": "first_frame", "image_url": {"url": first_frame_url}})
    if last_frame_url:
        content.append({"type": "image_url", "role": "last_frame", "image_url": {"url": last_frame_url}})
    return content


def build_content_extend(prompt: str, video_urls: list[str],
                         image_urls: Optional[list[str]] = None,
                         audio_urls: Optional[list[str]] = None) -> list[dict]:
    """视频延长（extend）：content = text + reference_video[] + 可选 reference_image/audio。

    官方 2.5 的延长任务允许 reference_image / reference_video / reference_audio 同时出现；
    ratio 由待延长视频锁定（adaptive），body 另带 `omni_reference_task_type=extend`。
    """
    content: list[dict] = [{"type": "text", "text": prompt}]
    for url in video_urls:
        if url:
            content.append({"type": "video_url", "role": "reference_video", "video_url": {"url": url}})
    for url in image_urls or []:
        if url:
            content.append({"type": "image_url", "role": "reference_image", "image_url": {"url": url}})
    for url in audio_urls or []:
        if url:
            content.append({"type": "audio_url", "role": "reference_audio", "audio_url": {"url": url}})
    return content


def audio_control_line(generate_audio: bool) -> str:
    """官方负向仅支持字幕/音频控制。"""
    if generate_audio:
        return "不额外加入对白字幕；不加入旁白；无 bgm，只生成环境音和动作音"
    return "不额外加入对白字幕；不加入旁白；不要任何声音"


# ---------------------------------------------------------------- API

def create_task(base: str, body: dict, timeout: int) -> dict:
    url = base.rstrip("/") + PASS_THROUGH_PATH + CREATE_SUFFIX
    response = _SESSION.post(
        url,
        headers={"Content-Type": "application/json", "User-Agent": "doubao-storyboard/1.0"},
        json=body,
        timeout=timeout,
    )
    if response.status_code in TRANSIENT_STATUS_CODES:
        raise requests.HTTPError(f"HTTP {response.status_code}", response=response)
    try:
        payload = response.json()
    except ValueError:
        payload = {"non_json_body": response.text[:4096]}
    response.raise_for_status()
    return payload


def get_task(base: str, task_id: str, timeout: int) -> dict:
    url = base.rstrip("/") + PASS_THROUGH_PATH + CREATE_SUFFIX + "/" + task_id
    response = _SESSION.get(url, headers={"User-Agent": "doubao-storyboard/1.0"}, timeout=timeout)
    if response.status_code in TRANSIENT_STATUS_CODES:
        raise requests.HTTPError(f"HTTP {response.status_code}", response=response)
    try:
        payload = response.json()
    except ValueError:
        payload = {"non_json_body": response.text[:4096]}
    response.raise_for_status()
    return payload


def wait_task(base: str, task_id: str, poll_interval: int, max_wait: int, timeout: int) -> tuple[dict, int]:
    deadline = time.monotonic() + max_wait
    latest: dict = {}
    polls = 0
    while True:
        try:
            latest = get_task(base, task_id, timeout=timeout)
            polls += 1
        except requests.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else None
            if status_code not in TRANSIENT_STATUS_CODES:
                raise
            if time.monotonic() >= deadline:
                raise TimeoutError(f"轮询持续 HTTP {status_code}，等待超过 {max_wait}s") from exc
            time.sleep(poll_interval)
            continue
        state = task_state_from(latest)
        if state in TERMINAL_SUCCESS:
            return latest, polls
        if state in TERMINAL_FAILURE:
            raise RuntimeError(f"任务结束但未成功，状态={state}")
        if time.monotonic() >= deadline:
            raise TimeoutError(f"等待任务超过 {max_wait}s，最后状态={state or 'unknown'}")
        time.sleep(poll_interval)


def download_video(url: str, dest: Path, timeout: int = 900, retries: int = 2) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries + 1):
        try:
            with _SESSION.get(url, stream=True, timeout=timeout) as response:
                response.raise_for_status()
                partial = dest.with_name(dest.name + ".part")
                with partial.open("wb") as handle:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            handle.write(chunk)
                partial.replace(dest)
            return attempt
        except requests.RequestException as exc:
            status_code = (
                exc.response.status_code
                if isinstance(exc, requests.HTTPError) and exc.response is not None
                else None
            )
            if attempt >= retries or (status_code is not None and status_code not in TRANSIENT_DOWNLOAD_STATUS_CODES):
                raise
            print(f"  下载失败（{status_code}），重试 {attempt + 1}/{retries}…", file=sys.stderr)
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("下载失败")


# ---------------------------------------------------------------- 抽帧（帧对帧接续）

def extract_last_frame(mp4: Path, out_png: Path, offset: float = 0.15, timeout: int = 120) -> Optional[Path]:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    for off in (offset, 0.15, 0.3, 0.5):
        cmd = ["ffmpeg", "-y", "-sseof", f"-{max(0.0, off):.3f}", "-i", str(mp4),
               "-frames:v", "1", "-update", "1", str(out_png)]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout)
        except Exception:  # noqa: BLE001
            continue
        if out_png.is_file() and out_png.stat().st_size > 0:
            return out_png
    return None


# ---------------------------------------------------------------- 时长裁/补（对轴用）

def probe_video_seconds(mp4: Path, timeout: int = 60) -> Optional[float]:
    """用 ffprobe 探视频真实时长（秒）。探测失败返回 None。"""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(mp4)],
            capture_output=True, text=True, timeout=timeout,
        )
        return float(result.stdout.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        return None


def enforce_exact_duration(video: Path, target: float, tolerance: float = 0.05,
                           timeout: int = 600) -> tuple[Optional[float], Optional[float], str]:
    """把成片严格裁/补到 target 秒（对轴用）。

    - 实际 > 目标：`-t target` 裁掉尾巴；
    - 实际 < 目标：`tpad=stop_mode=clone` 冻结末帧补齐到目标（正好做落幅定格）。
    帧对齐有 ≤1 帧残差，迭代收敛到容差内（最多 3 遍）。返回 (裁补前秒数, 裁补后秒数, 状态)。
    状态：ok（本就吻合）/ fixed（已裁补）/ failed / probe-failed。
    """
    actual = probe_video_seconds(video)
    if actual is None:
        return None, None, "probe-failed"
    if abs(actual - target) <= tolerance:
        return actual, actual, "ok"
    if shutil.which("ffmpeg") is None:
        return actual, None, "failed"

    tmp = video.with_suffix(".exact.mp4")
    enc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"]
    status = "failed"
    for _ in range(3):
        cur = probe_video_seconds(video)
        if cur is None:
            return actual, None, "probe-failed"
        if abs(cur - target) <= tolerance:
            return actual, cur, "fixed"
        base = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video)]
        if cur > target:
            cmd = base + ["-t", f"{target:.3f}"] + enc + [str(tmp)]
        else:
            pad = max(0.0, target - cur)
            cmd = base + ["-vf", f"tpad=stop_mode=clone:stop_duration={pad:.3f}",
                          "-t", f"{target:.3f}"] + enc + [str(tmp)]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except (subprocess.TimeoutExpired, OSError):
            return actual, None, "failed"
        if proc.returncode != 0 or not tmp.is_file():
            print(f"  ⚠ 时长裁补失败：{video.name} → {target:g}s（{proc.stderr.strip()[:200]}）",
                  file=sys.stderr)
            return actual, probe_video_seconds(video), "failed"
        tmp.replace(video)
        status = "fixed"
    return actual, probe_video_seconds(video), status


# ---------------------------------------------------------------- 逐镜执行

def shot_name(shot: dict) -> str:
    sid = str(shot.get("id") or "").strip()
    if sid:
        return sid
    try:
        return f"S{int(shot.get('no')):02d}"
    except (TypeError, ValueError):
        return "shot"


def resolve_frame(shot: dict, key: str, base_dir: Path) -> str:
    """首/尾帧：优先 http(s) 直链，其次 *_local 本地路径，再 shot[key] 本地路径。"""
    direct = str(shot.get(key) or "").strip()
    if direct.startswith(("http://", "https://")):
        return direct
    local = str(shot.get(key + "_local") or "").strip()
    for candidate in (local, direct):
        if not candidate:
            continue
        url = resolve_asset(candidate, base_dir)
        if url:
            return url
    return ""


def run_shot(shot: dict, base: str, model: str, ratio: str, image_role: str, voice_role: str,
             out_dir: Path, base_dir: Path, plan_dir: Path,
             poll_interval: int, max_wait: int, timeout: int,
             generate_audio: bool, send_seed: bool, send_motion: bool,
             no_refs: bool, no_audio: bool, max_refs: int, long_max: float,
             image_max: float = 12.0,
             min_seconds: float = 4.0, exact_seconds: bool = False,
             first_frame_override: str = "", chain_video: str = "",
             extend_format: str = "", audio_control: bool = False) -> dict:
    name = shot["_name"]
    started_at = time.monotonic()

    mode = str(shot.get("mode") or "").strip()
    if mode in ("normal", "hard_cut", "hook", "image2video_long", "reference", "image2video"):
        mode = "image2video"
    if mode == "text":
        mode = "text2video"
    if not mode:
        mode = "keyframes" if str(shot.get("last_frame") or "").strip() else "image2video"

    # 帧对帧接续：接了上一镜 → 本镜首帧用上一镜末帧
    first_frame_url = first_frame_override or resolve_frame(shot, "first_frame", base_dir)
    last_frame = "" if mode == "text2video" else resolve_frame(shot, "last_frame", base_dir)

    audio_urls: list[str] = []
    if (not no_audio) and mode not in ("keyframes", "text2video"):
        audio_urls = collect_audio_urls(shot, base_dir)

    ref_urls: list[str] = []
    if (not no_refs) and mode not in ("keyframes", "text2video"):
        ref_urls = resolve_list(shot.get("refs_urls"), base_dir)
        if max_refs:
            ref_urls = ref_urls[:max_refs]

    body: dict[str, Any] = {"model": model, "watermark": False}

    if mode == "extend":
        if chain_video:
            # 视频延长：content = text + reference_video（上一镜整段成片）；ratio 锁 adaptive
            content = build_content_extend(compose_prompt_text_extend(shot), [chain_video],
                                           ref_urls, audio_urls)
            ratio_use = "adaptive"
            body["omni_reference_task_type"] = "extend"
            if extend_format:
                body["output_format"] = extend_format
        else:
            print(f"  ⚠ {name} 标记为 extend 但取不到上一镜成片 → 退化为普通图生视频", file=sys.stderr)
            content = build_content(compose_prompt_text(shot), ref_urls, image_role, audio_urls, voice_role,
                                    first_frame_url=first_frame_url)
            ratio_use = "adaptive" if first_frame_url else ratio
    elif mode == "keyframes" and (last_frame or first_frame_override):
        content = build_content_keyframes(
            compose_prompt_text(shot, keyframes=True), first_frame_url, last_frame)
        ratio_use = "adaptive"
    else:
        # 严格首帧：first_frame / chain 末帧 → role=first_frame；refs_urls 只作 reference_image
        content = build_content(compose_prompt_text(shot), ref_urls, image_role, audio_urls, voice_role,
                                first_frame_url=first_frame_url)
        ratio_use = "adaptive" if first_frame_url else ratio

    n_ref = sum(1 for c in content if c.get("type") != "text")
    if n_ref > 50:
        print(f"  ⚠ {name} 参考素材 {n_ref} 个（>50），可能超限", file=sys.stderr)

    ga = shot.get("generate_audio") if isinstance(shot.get("generate_audio"), bool) else generate_audio
    if content and content[0].get("type") == "text" and audio_control:
        content[0]["text"] = apply_audio_control(content[0].get("text") or "", ga)

    try:
        seconds = float(shot.get("seconds") or 4)
    except (TypeError, ValueError):
        seconds = 4.0
    cap = long_max if mode in _LONG_MODES else image_max
    if seconds > cap:
        print(f"  ⚠ {name} seconds={seconds:g}s 超过单镜上限 {cap:g}s → 按 {cap:g}s 出片；"
              f"建议回③分镜拆镜（Seedance 2.5 带素材最长 30s）", file=sys.stderr)
    seconds = max(max(0.0, min_seconds), min(cap, seconds))

    body["ratio"] = ratio_use
    dur_override = shot.get("duration")
    body["duration"] = (int(dur_override) if dur_override not in (None, "", 0)
                        else (round(seconds, 2) if exact_seconds else int(round(seconds))))
    body["content"] = content
    body["generate_audio"] = bool(ga)
    if shot.get("resolution"):
        body["resolution"] = str(shot["resolution"])
    if send_seed:
        try:
            seed = int(shot.get("seed"))
        except (TypeError, ValueError):
            seed = -1
        if seed > 0:
            body["seed"] = seed
    if send_motion and shot.get("motion_strength") is not None:
        try:
            body["motion_strength"] = float(shot["motion_strength"])
        except (TypeError, ValueError):
            pass

    print(f"[{name}] 创建任务 · {mode} · {ratio_use} · {body['duration']}s · "
          f"参考图×{len(ref_urls)} + 音频×{len(audio_urls)}"
          f"{' · 首尾帧' if mode == 'keyframes' and last_frame else ''}"
          f"{' · 接续' if first_frame_override else ''}"
          f"{' · 视频延长' if mode == 'extend' and chain_video else ''}", flush=True)
    created = create_task(base, body, timeout)
    task_id = task_id_from(created)
    if not task_id:
        raise RuntimeError(f"创建响应无任务 ID：{json.dumps(created, ensure_ascii=False)[:1000]}")
    print(f"[{name}] 任务 {task_id}", flush=True)

    final, poll_count = wait_task(base, task_id, poll_interval, max_wait, timeout)
    video_url = video_url_from(final)
    if not video_url:
        raise RuntimeError(f"任务成功但无视频 URL：{json.dumps(final, ensure_ascii=False)[:1000]}")

    dest = out_dir / f"{name}.mp4"
    print(f"[{name}] 下载 → {dest}（逐镜固定名，每轮重出覆盖）", flush=True)
    download_retries = download_video(video_url, dest, timeout=timeout)
    file_size = dest.stat().st_size

    # 仅内存汇总（不落盘）：返回给调用方统计成功数 / 打印终端结果
    result = {
        "name": name,
        "id": shot.get("id"),
        "no": shot.get("no"),
        "mode": mode,
        "task_id": task_id,
        "ratio": ratio_use,
        "model": model,
        "duration": body["duration"],
        "reference_images": len(ref_urls) + (1 if first_frame_url else 0),
        "reference_audio": len(audio_urls),
        "reference_video": 1 if (mode == "extend" and chain_video) else 0,
        "status": task_state_from(final),
        "video_url": video_url,
        "video": str(dest),
        "file_size": file_size,
        "elapsed_seconds": round(time.monotonic() - started_at, 2),
        "poll_count": poll_count,
        "download_retries": download_retries,
    }
    drop_legacy_records(out_dir, f"{name}.json")
    print(f"[{name}] ✅ 完成（{file_size / 1024:.0f} KB）", flush=True)
    return result


# ---------------------------------------------------------------- 合并整集

def merge_clips(files: list[Path], output: Path, timeout: int = 1800) -> bool:
    """按顺序合并逐镜 mp4：优先 concat 流拷贝，失败回退 libx264 重编码。返回是否成功。"""
    if not files:
        return False
    if len(files) == 1:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(files[0].read_bytes())
        return True

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as handle:
        list_path = Path(handle.name)
        for f in files:
            handle.write(f"file '{f.resolve()}'\n")
    try:
        result = subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_path),
             "-c", "copy", str(output)],
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode == 0 and output.is_file() and output.stat().st_size > 0:
            return True
        print(f"  流拷贝合并失败，回退重编码：{result.stderr[-400:]}", file=sys.stderr)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        print(f"  流拷贝异常：{exc}", file=sys.stderr)
    finally:
        list_path.unlink(missing_ok=True)

    inputs: list[str] = []
    for f in files:
        inputs += ["-i", str(f)]
    v_parts = "".join(f"[{i}:v:0]" for i in range(len(files)))
    a_present = all(_has_audio(f) for f in files)
    if a_present:
        a_parts = "".join(f"[{i}:a:0]" for i in range(len(files)))
        filter_graph = f"{v_parts}{a_parts}concat=n={len(files)}:v=1:a=1[v][a]"
        map_args = ["-map", "[v]", "-map", "[a]"]
    else:
        filter_graph = f"{v_parts}concat=n={len(files)}:v=1:a=0[v]"
        map_args = ["-map", "[v]"]
    try:
        result = subprocess.run(
            ["ffmpeg", "-y", *inputs, "-filter_complex", filter_graph, *map_args,
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
             "-c:a", "aac", "-b:a", "192k", str(output)],
            capture_output=True, text=True, timeout=timeout,
        )
    except FileNotFoundError:
        print("未找到 ffmpeg：合并依赖系统 ffmpeg（brew install ffmpeg）", file=sys.stderr)
        return False
    except subprocess.TimeoutExpired:
        print("ffmpeg 重编码超时", file=sys.stderr)
        return False
    return result.returncode == 0 and output.is_file() and output.stat().st_size > 0


def _has_audio(mp4: Path) -> bool:
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
             "stream=codec_type", "-of", "csv=p=0", str(mp4)],
            capture_output=True, text=True, timeout=60,
        )
        return "audio" in result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


# ---------------------------------------------------------------- 主流程

def _natural_key(name: str):
    parts = re.split(r"(\d+)", name)
    return [int(p) if p.isdigit() else p for p in parts]


def load_plan(spec: str, source_dir: Path) -> tuple[dict, Path, str]:
    """定位并读入 JSON：先按给定路径（cwd/绝对），再按 source 目录。

    返回 (JSON 数据, JSON 所在目录, 文件名去掉扩展名)。
    """
    candidates: list[Path] = []
    given = Path(spec).expanduser()
    candidates.append(given)
    if not given.is_absolute():
        candidates.append(source_dir / given)
    for candidate in candidates:
        if candidate.is_file():
            path = candidate.resolve()
            return json.loads(path.read_text(encoding="utf-8")), path.parent, path.stem
    tried = " / ".join(str(c) for c in candidates)
    sys.exit(f"[FAIL] 找不到 JSON：{spec}（已试 {tried}）")


# ---------------------------------------------------------------- 裸请求体模式

def is_raw_request_body(plan: Any) -> bool:
    """顶层含 content[]（列表）且无 shots → 裸请求体（Seedance 建任务请求体）模式。"""
    return isinstance(plan, dict) and isinstance(plan.get("content"), list) and not plan.get("shots")


_RAW_URL_KEYS = ("image_url", "audio_url", "video_url")


def resolve_raw_body(body: dict, base_dir: Path) -> dict:
    """裸请求体：仅把 content 块里的本地素材路径解析为 base64，其余键一字不改（严格透传）。"""
    resolved = copy.deepcopy(body)
    content = resolved.get("content")
    if not isinstance(content, list):
        return resolved
    for block in content:
        if not isinstance(block, dict):
            continue
        for key in _RAW_URL_KEYS:
            holder = block.get(key)
            if isinstance(holder, dict):
                url = holder.get("url")
                if isinstance(url, str) and url.strip():
                    new_url = resolve_asset(url, base_dir)
                    if new_url:
                        holder["url"] = new_url
            elif isinstance(holder, str) and holder.strip():
                new_url = resolve_asset(holder, base_dir)
                if new_url:
                    block[key] = new_url
    return resolved


def run_raw(plan: dict, args: argparse.Namespace) -> int:
    """裸请求体 JSON 出片：原样透传 body（仅解析本地素材），一条请求一支视频。"""
    name = (getattr(args, "name", "") or "全片").strip() or "全片"
    out_dir = args.out
    plan_dir = getattr(args, "plan_dir", Path.cwd())
    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    body = resolve_raw_body(plan, plan_dir)
    if getattr(args, "generate_audio", None) is not None:
        body["generate_audio"] = bool(args.generate_audio)
    run_ts = run_stamp()

    print(f"[配置] 裸请求体模式（原样透传）· base={args.base} · model={body.get('model')} · "
          f"ratio={body.get('ratio')} · duration={body.get('duration')} · generate_audio={body.get('generate_audio')}")

    if args.dry_run:
        print(f"\n--- {name}-{run_ts}.mp4 · 裸请求体（原样透传，仅本地素材转 base64） ---")
        print(json.dumps(body, ensure_ascii=False, indent=2))
        return 0

    dest = out_dir / f"{name}-{run_ts}.mp4"   # 成片按时间戳命名，旧版本全部保留

    error: Optional[str] = None
    drop_legacy_records(out_dir, f"{name}.json", "batch_result.json")
    try:
        created = create_task(args.base.rstrip("/"), body, args.timeout)
        task_id = task_id_from(created)
        if not task_id:
            raise RuntimeError(f"创建响应无任务 ID：{json.dumps(created, ensure_ascii=False)[:1000]}")
        print(f"[{name}] 任务 {task_id}", flush=True)

        final, poll_count = wait_task(args.base, task_id, args.poll_interval, args.max_wait, args.timeout)
        video_url = video_url_from(final)
        if not video_url:
            raise RuntimeError(f"任务成功但无视频 URL：{json.dumps(final, ensure_ascii=False)[:1000]}")

        print(f"[{name}] 下载 → {dest}", flush=True)
        download_retries = download_video(video_url, dest, timeout=args.timeout)
        file_size = dest.stat().st_size
        print(f"[{name}] ✅ 完成（{file_size / 1024:.0f} KB · 轮询 {poll_count} 次 · "
              f"下载重试 {download_retries} 次）", flush=True)
        print(f"[成片] {dest}")
    except Exception as exc:  # noqa: BLE001
        error = str(exc)
        print(f"[{name}] ❌ 失败：{exc}", flush=True)

    return 1 if error else 0


def _safe_component(text: str) -> str:
    """把名称压成安全的目录名（去路径分隔符）。"""
    safe = re.sub(r"[\\/\s]+", "_", text or "").strip("_")
    return safe or "video"


def cli_main(argv: Optional[list[str]] = None) -> int:
    _vcfg = video_api_config()
    parser = argparse.ArgumentParser(
        description="JSON 出片（Seedance 2.5）· 只根据 source 目录下的 JSON 出片，不做任何创作")
    parser.add_argument("json", nargs="?", default="",
                        help="JSON 文件名（相对 --source 解析）或路径；每次只出一个")
    parser.add_argument("--plan", "--json", dest="json_alias", default="",
                        help="兼容旧写法：等同位置参数（JSON 路径）")
    parser.add_argument("--source", type=Path, default=_SKILL_ROOT / "assets" / "output",
                        help="JSON 所在目录（默认 <skill>/assets/output，可只给项目名）")
    parser.add_argument("--name", default="", help="成片名前缀（默认取 JSON 文件名）")
    parser.add_argument("--out", type=Path, default=None,
                        help=f"片段输出目录（默认 <项目>/{CLIPS_ROOT}）")
    parser.add_argument("--merge-out", type=Path, default=None,
                        help="合并输出（默认 <项目>/06-MV成片_无音轨.mp4，仅 --merge 时用）")
    parser.add_argument("--only", default="", help="只跑指定镜号，逗号分隔（如 S03,S05）")
    parser.add_argument("--force", action="store_true", help=argparse.SUPPRESS)  # 兼容旧命令，无作用
    parser.add_argument("--workers", type=int, default=1,
                        help="并发数（默认 1＝逐镜顺序；成本纪律，要并发显式给 N）")
    parser.add_argument("--ratio", default="", help="画幅（覆盖 JSON，默认取 JSON 的 ratio 或 9:16）")
    parser.add_argument("--base", default=os.environ.get("VIDEO_GATEWAY_BASE") or _vcfg["base"])
    parser.add_argument("--model", default=os.environ.get("VIDEO_MODEL") or _vcfg["model"])
    parser.add_argument("--api-prefix", default=os.environ.get("VIDEO_API_PREFIX") or _vcfg["prefix"],
                        help="网关路径前缀（默认 /v1；直连 Ark 可设为 /api/v3 或空串）")
    parser.add_argument("--image-role", default="reference_image", help="参考图 role")
    parser.add_argument("--voice-role", default="reference_audio", help="参考音频 role")
    parser.add_argument("--no-refs", action="store_true", help="不传资产参考图（refs_urls）")
    parser.add_argument("--max-refs", type=int, default=0, help="资产参考图上限（0=不限）")
    parser.add_argument("--no-audio", action="store_true", help="不传参考音频（voice_urls）")
    parser.add_argument("--require-audio", action="store_true",
                        help="逐句演唱版硬门：除器乐镜外，每镜必须有 ref_audio_urls/voice_urls/audio_url，否则拒绝出片")
    parser.add_argument("--generate-audio", dest="generate_audio", action="store_true", default=None,
                        help="强制让 Seedance 生成音频（默认不传=按 JSON；本 skill 应为 false）")
    parser.add_argument("--audio-control", action="store_true",
                        help="追加官方字幕/音频控制句（默认不追加，JSON 说什么就是什么）")
    parser.add_argument("--no-generate-audio", dest="generate_audio", action="store_false", default=None,
                        help="强制关闭 Seedance 生成音频")
    parser.add_argument("--no-seed", action="store_true", help="不传 seed")
    parser.add_argument("--motion", action="store_true", help="传 motion_strength（默认关，网关支持时才开）")
    parser.add_argument("--no-keyframes", action="store_true", help="忽略尾帧，全部走普通图生视频")
    parser.add_argument("--no-chain", action="store_true", help="关闭帧对帧接续/视频延长（默认按 chain_from 接续）")
    parser.add_argument("--no-upload-chain", dest="upload_chain", action="store_false", default=True,
                        help="关闭延续素材上传（chain_from / extend 传了 --uploader-script 才上传）")
    parser.add_argument("--uploader-script", default="",
                        help="调用方自带的素材上传脚本路径（upload_assets.py 同接口）；不传则延续素材走 base64")
    parser.add_argument("--upload-prefix", default="",
                        help="公网命名空间目录（默认 <项目>_第<集>集_延续）")
    parser.add_argument("--extend-format", default="mov", help="extend 视频延长的 output_format（默认 mov，官方建议；传空串则不传）")
    parser.add_argument("--merge", action="store_true",
                        help="出片后拼成 <项目>/06-MV成片_无音轨.mp4（默认不合并：音轨交给⑥合成官贴原曲）")
    parser.add_argument("--no-merge", action="store_true", help=argparse.SUPPRESS)  # 兼容旧命令
    parser.add_argument("--flat-clips", action="store_true", help=argparse.SUPPRESS)  # 片段默认已平铺
    parser.add_argument("--long-max-seconds", type=float, default=30.0, help="长模式时长上限（默认 30）")
    parser.add_argument("--image-max-seconds", type=float, default=30.0,
                        help="普通模式（带参考图/首尾帧）时长上限（默认 30＝Seedance 2.5 带素材上限）")
    parser.add_argument("--min-seconds", type=float, default=0.0,
                        help="单镜时长下限（默认 0＝MV 短镜不设下限；漫剧等可传 4）")
    parser.add_argument("--exact-seconds", action=argparse.BooleanOptionalAction, default=True,
                        help="duration 直接取 JSON 的 seconds 原值（含小数），不取整（默认开）")
    parser.add_argument("--enforce-seconds", action=argparse.BooleanOptionalAction, default=True,
                        help="出片后逐镜裁/补到 JSON 的精确 seconds（默认开；长了裁尾、短了冻结末帧补齐）")
    parser.add_argument("--enforce-tolerance", type=float, default=0.05,
                        help="--enforce-seconds 的容差秒数（默认 0.05）")
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--max-wait", type=int, default=1800, help="单镜最长等待秒数")
    parser.add_argument("--timeout", type=int, default=600, help="HTTP 请求超时秒数")
    parser.add_argument("--dry-run", action="store_true", help="只打印请求体，不调 API")
    args = parser.parse_args(argv)

    global PASS_THROUGH_PATH
    PASS_THROUGH_PATH = (args.api_prefix or "").rstrip("/")

    spec = (args.json or args.json_alias).strip()
    if not spec:
        parser.error("请指定要出片的 JSON（例：python3 scripts/generate_video.py assets/output/M01-xxx/05-视频生成提示词/分镜JSON.json）")

    source_dir = args.source.expanduser()
    if not source_dir.is_dir():
        cand = Path(spec).expanduser()
        if cand.is_file():
            source_dir = cand.parent
        else:
            sys.exit(f"[FAIL] source 目录不存在：{source_dir}")

    # 只给项目名/项目目录时，自动找 05-视频生成提示词/分镜JSON.json
    _given = Path(spec).expanduser()
    _proj_cand = _given if _given.is_dir() else (source_dir / spec)
    if _proj_cand.is_dir():
        for _plan in (_proj_cand / "05-视频生成提示词" / "分镜JSON.json",
                      _proj_cand / "05-提示词" / "分镜JSON.json",
                      _proj_cand / "分镜JSON.json"):
            if _plan.is_file():
                spec = str(_plan)
                break

    plan, plan_dir, stem = load_plan(spec, source_dir)
    name = (args.name or stem).strip() or stem
    args.name = name
    args.plan_dir = plan_dir       # 裸请求体模式的本地素材按 JSON 所在目录解析
    project_root = project_root_for(plan_dir / f"{stem}.json")
    _EXTRA_ROOTS.clear()
    _EXTRA_ROOTS.append(project_root)
    out_dir = args.out.expanduser() if args.out else (project_root / CLIPS_ROOT)
    args.out = out_dir
    # 逐镜片段平铺在 成片片段/（S01.mp4 …），固定名每轮覆盖
    clips_dir = out_dir
    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    plan_file = plan_dir / f"{stem}.json"
    print(f"[输入] {spec} → {plan_file}"
          f"（{'裸请求体' if is_raw_request_body(plan) else '分镜 shots[]'} 模式）")
    print(f"[项目] {project_root} · 片段输出 {out_dir}")

    if is_raw_request_body(plan):
        return run_raw(plan, args)
    shots_raw = list(plan.get("shots") or plan.get("slices") or [])
    hook = plan.get("hook")
    if isinstance(hook, dict) and hook.get("id"):
        shots_raw = [hook] + shots_raw
    if not shots_raw:
        sys.exit("[FAIL] JSON 既没有 shots（分镜模式），也没有 content 数组（裸请求体模式）")

    json_ratio = str(plan.get("ratio") or "9:16")
    ratio = args.ratio or json_ratio
    episode = plan.get("episode")
    project = str(plan.get("project") or plan_dir.name)
    # 本 skill：口型由参考音频驱动，默认不出声（JSON 显式 true 才让模型生成声音）
    ga_default = (args.generate_audio if args.generate_audio is not None
                  else (plan.get("generate_audio") if isinstance(plan.get("generate_audio"), bool) else False))

    if not args.dry_run:
        clips_dir.mkdir(parents=True, exist_ok=True)

    only = {s.strip() for s in args.only.split(",") if s.strip()}
    shots: list[dict] = []
    for raw in shots_raw:
        if not isinstance(raw, dict):
            continue
        s = dict(raw)
        s["_name"] = shot_name(s)
        if only and s["_name"] not in only and str(s.get("no")) not in only:
            continue
        if args.no_keyframes:
            s["last_frame"] = ""
            s["last_frame_local"] = ""
            if str(s.get("mode") or "") == "keyframes":
                s["mode"] = "image2video"
        shots.append(s)

    shots.sort(key=lambda s: (_natural_key(str(s.get("no", 0))), _natural_key(s["_name"])))
    if not shots:
        sys.exit("[FAIL] --only 未匹配任何镜")

    # 逐句演唱版硬门：除器乐镜外，每镜必须绑一句音频（否则口型没有驱动源）
    if args.require_audio:
        def _has_audio_ref(shot: dict) -> bool:
            for key in ("ref_audio_urls", "voice_urls", "audio_url", "dialogue"):
                value = shot.get(key)
                if value:
                    return True
            return False

        def _instrumental(shot: dict) -> bool:
            if str(shot.get("type") or "").lower() in ("instrumental", "instrument"):
                return True
            for key in ("line", "lines"):
                if key in shot and shot.get(key) in (None, "", []):
                    return True
            return False

        missing = [s["_name"] for s in shots if not _instrumental(s) and not _has_audio_ref(s)]
        if missing:
            sys.exit(f"[FAIL] --require-audio：{len(missing)} 镜没有逐句音频 → 口型无驱动源：{', '.join(missing)}\n"
                     f"  先跑：python3 scripts/line_audio.py <项目> --bind\n"
                     f"  再跑：python3 scripts/upload_project.py <项目> --with-line-audio --fill-json --verify")
        n_audio_shots = sum(1 for s in shots if _has_audio_ref(s))
        print(f"[口型] 逐句音频 {n_audio_shots}/{len(shots)} 镜（其余为器乐镜）")

    # CLI 显式开关优先于 JSON（实测回退用：--generate-audio）
    if args.generate_audio is not None:
        for s in shots:
            s["generate_audio"] = bool(args.generate_audio)
        if args.generate_audio:
            print("[配置] ⚠ 已用 CLI 强制 generate_audio=true（回退模式）：成片必须丢弃生成音轨、贴回原音",
                  file=sys.stderr)

    # 帧对帧接续 / 视频延长：chain_from → {本镜名: 上一镜名}
    # chain_from 兼容两种写法：镜名（如 1-3）或 S{no:02d}（如 S03，漫剧镜头计划约定）
    alias: dict[str, str] = {}
    for raw in shots_raw:
        if not isinstance(raw, dict):
            continue
        nm = shot_name(raw)
        alias[nm] = nm
        try:
            alias.setdefault(f"S{int(raw.get('no')):02d}", nm)
        except (TypeError, ValueError):
            pass
    chain_src: dict[str, str] = {}
    if not args.no_chain:
        for s in shots:
            cf = str(s.get("chain_from") or "").strip()
            if not cf:
                continue
            prev = alias.get(cf) or alias.get(cf.upper())
            if prev and prev != s["_name"]:
                chain_src[s["_name"]] = prev
    if chain_src and len(shots) > 1 and args.workers > 1:
        print("[接续] 开启帧对帧接续/视频延长 → 逐镜顺序执行（workers 1）", flush=True)
        args.workers = 1

    chain_dir = clips_dir / "_链帧"

    # 延续素材上传：只认显式指定的上传脚本（不引用其他 skill），命名空间 / 暂存目录在此解析
    uploader_script = find_uploader_script(args.uploader_script) if args.upload_chain else None
    if args.upload_chain and uploader_script is None:
        if args.uploader_script:
            print(f"[上传] ⚠ 指定的上传脚本不存在：{args.uploader_script} → 延续素材回退 base64",
                  file=sys.stderr)
        else:
            print("[上传] 未找到 material-uploader → 延续素材回退 base64", file=sys.stderr)
    _proj_safe = re.sub(r"[\\/\s]+", "_", project).strip("_") or "project"
    _ep_safe = str(episode) if episode not in (None, "") else "0"
    # MV 项目：命名空间默认取**项目文件夹名**（与 refs_urls 的 <项目文件夹名>/图片/... 对齐）。
    upload_prefix = (args.upload_prefix.strip("/").strip()
                     or project_root.name
                     or f"{_proj_safe}_第{_ep_safe}集_延续")
    staging_root = clips_dir / "_延续素材"

    def build_chain(s: dict, dry: bool = False) -> Optional[dict]:
        """取 chain_from 指向的上一镜 → {prev, frame(末帧), video(整段), missing}；无接续返回 None。

        默认用 material-uploader 上传换公网直链，失败回退 base64（--no-upload-chain 关闭）。
        extend 模式只需上一镜整段 mp4；其余接续模式只需上一镜末帧 PNG。
        """
        prev = chain_src.get(s["_name"])
        if not prev:
            return None
        mp4 = clips_dir / f"{prev}.mp4"
        exists = mp4.is_file()
        mode = str(s.get("mode") or "").strip() or (
            "keyframes" if str(s.get("last_frame") or "").strip() else "image2video")
        up_hint = "（将上传换公网直链）" if (uploader_script and not dry) else ""
        if dry:
            note = "" if exists else "（缺失）"
            return {"prev": prev, "frame": f"（上镜末帧：{prev}.mp4）{note}{up_hint}",
                    "video": f"（视频延长：{prev}.mp4）{note}{up_hint}", "missing": not exists}
        if not exists:
            print(f"  ⚠ {s['_name']} 需接续 {prev}，但其成片不存在 → 放弃接续/延长", file=sys.stderr)
            return {"prev": prev, "frame": "", "video": "", "missing": True}
        # ★ 二次保险：源片段必须裁到它自己的精确秒（防止上一段未走逐段裁切）
        if args.enforce_seconds:
            prev_shot = next((x for x in shots_raw if shot_name(x) == prev), None)
            if prev_shot:
                try:
                    pt = float(prev_shot.get("seconds"))
                    b, a, st = enforce_exact_duration(mp4, pt, tolerance=args.enforce_tolerance)
                    if st == "fixed":
                        print(f"  [对齐] 源 {prev}: {b:g}s → {a:g}s（目标 {pt:g}s）", flush=True)
                except (TypeError, ValueError):
                    pass

        def upload_or_none(path: Path) -> str:
            if not uploader_script:
                return ""
            url = upload_material(path, upload_prefix, uploader_script, staging_root, timeout=args.timeout)
            if url:
                print(f"  ↗ {s['_name']} 延续素材已上传（material-uploader）→ {url}", flush=True)
                return url
            return ""

        if mode == "extend":
            # 视频延长：只需上一镜整段成片 → 上传换直链，失败回退 base64
            video_url = upload_or_none(mp4)
            if not video_url:
                try:
                    video_url = to_data_url(mp4)
                except ValueError as exc:
                    print(f"  {exc}", file=sys.stderr)
                    video_url = ""
            return {"prev": prev, "frame": "", "video": video_url, "missing": False}

        # 帧对帧接续：抽上一镜末帧 → 上传换直链，失败回退 base64
        frame_url = ""
        frame = extract_last_frame(mp4, chain_dir / f"{prev}_last.png")
        if frame:
            frame_url = upload_or_none(frame)
            if not frame_url:
                try:
                    frame_url = to_data_url(frame)
                except ValueError as exc:
                    print(f"  {exc}", file=sys.stderr)
        else:
            print(f"  ⚠ {s['_name']} 抽取 {prev} 末帧失败 → 走普通模式", file=sys.stderr)
        return {"prev": prev, "frame": frame_url, "video": "", "missing": False}

    print(f"[配置] base={args.base}  model={args.model}  ratio={ratio}  workers={args.workers}")
    print(f"[配置] 时长：下限 {args.min_seconds:g}s · 上限 {args.image_max_seconds:g}s · "
          f"{'精确秒' if args.exact_seconds else '取整秒'} · "
          f"{'出片后裁/补精确秒' if args.enforce_seconds else '不裁补'}")
    print(f"[配置] 生成音频={'开' if ga_default else '关'} · 参考图={'关' if args.no_refs else '全传'} · "
          f"音频={'关' if args.no_audio else '全传'} · seed={'关' if args.no_seed else '按镜'} · "
          f"运动强度={'传' if args.motion else '关'} · 接续={'关' if args.no_chain else '开'} · "
          f"延续上传={'开（' + upload_prefix + '）' if uploader_script else '关'}")
    _ep_part = f" 第{episode}集" if episode not in (None, "") else ""
    print(f"[计划] {project}{_ep_part} · {len(shots)} 镜" + (f" · 接续 {len(chain_src)} 镜" if chain_src else ""), flush=True)

    if args.dry_run:
        for s in shots:
            mode = str(s.get("mode") or "").strip()
            if mode in ("normal", "hard_cut", "hook", "image2video_long", "reference", "image2video"):
                mode = "image2video"
            if mode == "text":
                mode = "text2video"
            if not mode:
                mode = "keyframes" if str(s.get("last_frame") or "").strip() else "image2video"
            ch = build_chain(s, dry=True)
            override = (ch or {}).get("frame", "")
            chain_video = (ch or {}).get("video", "")
            first_frame_url = override or resolve_frame(s, "first_frame", plan_dir)
            last_frame = "" if mode == "text2video" else resolve_frame(s, "last_frame", plan_dir)
            ref_urls = [] if (args.no_refs or mode in ("keyframes", "text2video")) else resolve_list(s.get("refs_urls"), plan_dir)
            if args.max_refs:
                ref_urls = ref_urls[:args.max_refs]
            audio_urls = [] if (args.no_audio or mode in ("keyframes", "text2video")) else collect_audio_urls(s, plan_dir)
            if mode == "extend" and chain_video:
                content = build_content_extend(compose_prompt_text_extend(s), [chain_video],
                                               ref_urls, audio_urls)
                ratio_use = "adaptive"
            elif mode == "keyframes" and last_frame:
                content = build_content_keyframes(compose_prompt_text(s, keyframes=True), first_frame_url, last_frame)
                ratio_use = "adaptive"
            else:
                content = build_content(compose_prompt_text(s), ref_urls,
                                        args.image_role, audio_urls, args.voice_role,
                                        first_frame_url=first_frame_url)
                ratio_use = "adaptive" if first_frame_url else ratio
            try:
                seconds = float(s.get("seconds") or 4)
            except (TypeError, ValueError):
                seconds = 4.0
            cap = args.long_max_seconds if mode in _LONG_MODES else args.image_max_seconds
            seconds = max(max(0.0, args.min_seconds), min(cap, seconds))
            ga = s.get("generate_audio") if isinstance(s.get("generate_audio"), bool) else ga_default
            if args.audio_control:
                content[0]["text"] = apply_audio_control(content[0].get("text") or "", bool(ga))
            dur_override = s.get("duration")
            body = {"model": args.model, "watermark": False, "ratio": ratio_use,
                    "duration": (int(dur_override) if dur_override not in (None, "", 0)
                                 else (round(seconds, 2) if args.exact_seconds else int(round(seconds)))),
                    "content": content,
                    "generate_audio": bool(ga)}
            if s.get("resolution"):
                body["resolution"] = str(s["resolution"])
            if mode == "extend" and chain_video:
                body["omni_reference_task_type"] = "extend"
                if args.extend_format:
                    body["output_format"] = args.extend_format
            if not args.no_seed:
                try:
                    if int(s.get("seed")) > 0:
                        body["seed"] = int(s["seed"])
                except (TypeError, ValueError):
                    pass
            if args.motion and s.get("motion_strength") is not None:
                try:
                    body["motion_strength"] = float(s["motion_strength"])
                except (TypeError, ValueError):
                    pass
            kf_tag = " · 首尾帧" if (mode == "keyframes" and last_frame) else ""
            ext_tag = f" · 视频延长←{(ch or {}).get('prev')}.mp4" if (mode == "extend" and chain_video) else ""
            print(f"\n--- {s['_name']} · {mode} · {ratio_use} · {body['duration']}s · "
                  f"参考图×{len(ref_urls)}（+首帧 {1 if first_frame_url else 0}） · 音频×{len(audio_urls)}{kf_tag}{ext_tag} ---")
            print(content[0]["text"])
        return 0

    # 不记录清单、不做断点跳过：逐镜 <id>.mp4 固定名每轮覆盖
    todo = list(shots)
    drop_legacy_records(clips_dir, "batch_result.json", *(f"{s['_name']}.json" for s in shots))

    results: list[dict] = []   # 仅内存统计（不落盘清单）
    errors: list[dict] = []

    def submit(s: dict, first_frame_override: str, chain_video: str = "") -> dict:
        return run_shot(
            s, args.base.rstrip("/"), args.model, ratio, args.image_role, args.voice_role,
            clips_dir, plan_dir, plan_dir, args.poll_interval, args.max_wait, args.timeout,
            bool(ga_default), not args.no_seed, bool(args.motion),
            args.no_refs, args.no_audio, args.max_refs, args.long_max_seconds,
            args.image_max_seconds,
            min_seconds=args.min_seconds, exact_seconds=args.exact_seconds,
            first_frame_override=first_frame_override, chain_video=chain_video,
            extend_format=args.extend_format, audio_control=args.audio_control,
        )

    t0 = time.monotonic()
    by_name = {s["_name"]: s for s in shots}
    if chain_src and not args.enforce_seconds:
        print("[对齐] 检测到 extend/接续链 → 自动开启逐段精确裁切（--enforce-seconds）", flush=True)
        args.enforce_seconds = True
    if chain_src:
        for s in todo:
            ch = build_chain(s)
            override = (ch or {}).get("frame", "")
            chain_video = (ch or {}).get("video", "")
            try:
                r = submit(s, override, chain_video)
                results.append(r)
                # ★ 关键：本段出完立刻裁到精确秒，下一段才能拿到对齐的源视频
                if args.enforce_seconds:
                    clip = Path(r["video"])
                    try:
                        target = float(s.get("seconds"))
                    except (TypeError, ValueError):
                        target = None
                    if target and clip.is_file():
                        before, after, st = enforce_exact_duration(clip, target, tolerance=args.enforce_tolerance)
                        print(f"  [对齐] {r['name']}: {before:g}s → {after:g}s（目标 {target:g}s，{st}）", flush=True)
            except Exception as exc:  # noqa: BLE001
                errors.append({"name": s["_name"], "error": str(exc)})
                print(f"[{s['_name']}] ❌ 失败：{exc}", flush=True)
    else:
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            futures = {pool.submit(submit, s, ""): s for s in todo}
            for future in as_completed(futures):
                s = futures[future]
                try:
                    results.append(future.result())
                except Exception as exc:  # noqa: BLE001
                    errors.append({"name": s["_name"], "error": str(exc)})
                    print(f"[{s['_name']}] ❌ 失败：{exc}", flush=True)

    # 对轴：逐镜裁/补到 JSON 的精确 seconds（长了裁尾、短了冻结末帧补齐）
    if args.enforce_seconds and results:
        print(f"[对轴] 逐镜复核精确 seconds（容差 {args.enforce_tolerance:g}s）", flush=True)
        for r in results:
            shot = by_name.get(r["name"])
            clip = Path(r["video"])
            if not shot or not clip.is_file():
                continue
            try:
                target = float(shot.get("seconds"))
            except (TypeError, ValueError):
                continue
            before, after, st = enforce_exact_duration(clip, target, tolerance=args.enforce_tolerance)
            if st == "fixed":
                print(f"  {r['name']}: {before:g}s → {after:g}s（目标 {target:g}s）", flush=True)
            elif st == "ok":
                print(f"  {r['name']}: 已吻合 {after:g}s", flush=True)
            else:
                print(f"  ⚠ {r['name']}: 裁补未完成（{st}，实际 {before}s → 目标 {target:g}s）",
                      file=sys.stderr)

    # 片段默认已平铺在 成片片段/；--flat-clips 仅为兼容旧命令保留（同目录不再复制）
    if args.flat_clips:
        print(f"[平铺] 片段已在 {out_dir}（无需复制）")

    # 合并（可选）：<项目>/06-MV成片_无音轨.mp4，音轨由⑥合成官贴回原曲
    merged_path = None
    if args.merge and not args.no_merge:
        ordered = [clips_dir / f"{s['_name']}.mp4" for s in shots if (clips_dir / f"{s['_name']}.mp4").is_file()]
        if len(ordered) == len(shots):
            merge_out = args.merge_out or (project_root / "06-MV成片_无音轨.mp4")
            print(f"[合并] {len(ordered)} 段 → {merge_out}", flush=True)
            if merge_clips(ordered, merge_out):
                merged_path = str(merge_out)
                print(f"[合并] ✅ {merge_out}", flush=True)
            else:
                print(f"[合并] ❌ 失败（逐镜片段仍保留在 {clips_dir}）", file=sys.stderr)
        else:
            print(f"[合并] 跳过：{len(ordered)}/{len(shots)} 镜有片段（有失败或未跑）", file=sys.stderr)
    elif not args.merge:
        print(f"[合并] 未合并（默认）：音轨交给⑥合成官贴原曲；要预览合并加 --merge")

    print(f"\n[完成] 成功 {len(results)} / {len(todo)}，耗时 {(time.monotonic() - t0) / 60:.1f} 分钟")
    print(f"[片段] {clips_dir}")
    if merged_path:
        print(f"[成片] {merged_path}")
    if errors:
        print("[失败清单]")
        for e in errors:
            print(f"  - {e['name']}: {e['error'][:160]}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(cli_main())
