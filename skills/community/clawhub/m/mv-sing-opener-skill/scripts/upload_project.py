#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""上传 30 秒说唱项目的公开素材（人物参考图 + 30s 音频 → public 命名空间）。

为什么需要它：
  - `04-提示词/分镜JSON.json` 里 `refs_urls` 必须是**公网直链**（HEAD 200），
    但 `04-图片/ref_人物.png` 只在本地；
  - 用户素材先在 ② 上传成功，才允许进入方案/歌词/出片；
  - material-uploader 用 `--src` 指项目文件夹时会**整目录覆盖**目标，
    所以这里先把「04-图片」镜像到暂存目录，再交给它上传；
  - 上传成功后按**文件名**把公网直链回填进分镜 JSON / 裸请求体（`--fill-json`）。

用法：
  python3 scripts/upload_project.py <项目目录> --verify --fill-json
  python3 scripts/upload_project.py <项目目录> --dry-run
  python3 scripts/upload_project.py <项目目录> --verify-json      # 不重传，只核验已有直链

示例：
  python3 scripts/upload_project.py assets/output/MV01-xxx --verify --fill-json
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    CLIPS_ROOT, IMAGE_ROOT, PLAN_DIRS, PLAN_NAME, resolve_uploader,
)

SKILL_ROOT = Path(__file__).resolve().parent.parent
UPLOADER = resolve_uploader()
UPLOAD_CONFIG = SKILL_ROOT / "scripts" / "material-uploader" / "config.json"
UPLOAD_CONFIG_EXAMPLE = SKILL_ROOT / "scripts" / "material-uploader" / "config.example.json"
MANIFEST = "素材外网路径.json"
PERSIST_DIR = Path("03-上传")
PERSIST_MANIFEST = "素材外网路径.json"

# --fill-json 的默认回填目标（相对项目目录）
FILL_TARGETS = (
    [f"{d}/{PLAN_NAME}" for d in PLAN_DIRS]
    + [f"{d}/裸请求体/*.json" for d in PLAN_DIRS]
    + [PLAN_NAME]
)

# 参考音频目录（--with-line-audio 只传被 JSON ref_audio_urls 引用的那些）
LINE_AUDIO_ROOT = Path("00-输入") / "音频"

# 值可能是「单个 URL/路径」或「URL/路径列表」的键
MEDIA_KEYS = {
    "refs_urls", "ref_audio_urls", "ref_video_urls", "voice_urls",
    "first_frame", "last_frame", "first_frame_local", "last_frame_local",
}
# 值可能是 {"url": "..."} 的键（Seedance content[] 口径）
URL_OBJECT_KEYS = {"image_url", "audio_url", "video_url"}


def link_or_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def mirror_dir(src: Path, dst: Path, exts: tuple[str, ...] | None = None) -> int:
    n = 0
    if not src.is_dir():
        return 0
    for p in sorted(src.rglob("*")):
        if not p.is_file() or p.name.startswith("."):
            continue
        if exts and p.suffix.lower() not in exts:
            continue
        rel = p.relative_to(src)
        link_or_copy(p, dst / rel)
        n += 1
    return n


def mirror_clips(src: Path, dst: Path) -> int:
    """成片片段：顶层 mp4/mov（平铺）；兼容 `_片段/<name>/*.mp4`。"""
    n = 0
    if not src.is_dir():
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    for p in sorted(src.glob("*")):
        if p.is_file() and p.suffix.lower() in (".mp4", ".mov") and not p.name.startswith("."):
            link_or_copy(p, dst / p.name)
            n += 1
    for p in sorted(src.glob("_片段/*/*.mp4")):
        target = dst / p.name
        if target.exists():
            continue
        link_or_copy(p, target)
        n += 1
    return n


def collect_ref_audio(project: Path, patterns: list[str]) -> tuple[list[Path], list[str]]:
    """收集分镜 JSON 里 `ref_audio_urls` 的本地路径（逐句演唱版）。

    只上传**被引用**的那几行，不把 `01-对轴/片段/` 全量（31 行）都推上去；
    返回 (存在的文件, 缺失的路径说明)。
    """
    seen: list[Path] = []
    missing: list[str] = []
    for pat in patterns:
        targets = sorted(project.glob(pat)) if any(ch in pat for ch in "*?[") else [project / pat]
        for path in targets:
            if not path.is_file() or path.name != PLAN_NAME:
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            for shot in data.get("shots", []) if isinstance(data, dict) else []:
                if not isinstance(shot, dict):
                    continue
                values = shot.get("ref_audio_urls")
                if isinstance(values, str):
                    values = [values]
                for value in values or []:
                    text = str(value or "").strip()
                    if not text or text.startswith("data:"):
                        continue
                    if text.startswith(("http://", "https://")):
                        # JSON 已补成绝对直链（link_assets.py）时，按 URL 路径还原本地文件
                        p = unquote(urlparse(text).path)
                        idx = p.find(LINE_AUDIO_ROOT.as_posix())
                        if idx < 0:
                            continue
                        local = project / p[idx:]
                    else:
                        local = Path(text)
                        if not local.is_absolute():
                            local = project / local
                    if not local.is_file():
                        missing.append(f"{shot.get('id', '?')} → {text}")
                        continue
                    if local not in seen:
                        seen.append(local)
    return seen, missing


def collect_ref_images(project: Path, patterns: list[str]) -> list[str]:
    """收集分镜 JSON 里 `refs_urls` 引用的图片（相对项目目录）。

    只上传**被引用**的图，不再整目录镜像（避免把 `图片/_风格基准/`、早期废弃图一起推上去）。
    """
    rels: list[str] = []
    for pat in patterns:
        targets = sorted(project.glob(pat)) if any(ch in pat for ch in "*?[") else [project / pat]
        for path in targets:
            if not path.is_file() or path.name != PLAN_NAME:
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            for shot in data.get("shots", []) if isinstance(data, dict) else []:
                if not isinstance(shot, dict):
                    continue
                values = shot.get("refs_urls")
                if isinstance(values, str):
                    values = [values]
                for value in values or []:
                    text = str(value or "").strip()
                    if not text or text.startswith("data:"):
                        continue
                    path_part = unquote(urlparse(text).path) if "://" in text else text
                    idx = path_part.find(IMAGE_ROOT)
                    if idx < 0:
                        continue
                    rel = path_part[idx:]
                    if rel not in rels:
                        rels.append(rel)
    return rels


# ---------------------------------------------------------------- --fill-json


def _basename(value: str) -> str:
    """取 URL / 路径里的文件名（解码百分号）。"""
    text = str(value or "").strip()
    if not text:
        return ""
    path = urlparse(text).path if "://" in text else text
    return Path(unquote(path)).name


def load_manifest(staging: Path) -> tuple[dict[str, str], list[str]]:
    """读 material-uploader 的清单 → {文件名: 公网直链}，并返回重名告警。"""
    path = staging if staging.is_file() else staging / MANIFEST
    if not path.is_file():
        return {}, [f"未找到上传清单：{path}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {}, [f"上传清单解析失败：{exc}"]

    lookup: dict[str, str] = {}
    dup: list[str] = []
    for item in data.get("items", []):
        if item.get("status") not in ("ok", "skip") or not item.get("url"):
            continue
        http = str(item.get("http") or "")
        if http and not http.startswith("2"):
            dup.append(f"{_basename(item.get('rel') or '')}（HEAD {http}，未回填）")
            continue
        name = _basename(item.get("rel") or item.get("name") or "")
        if not name:
            continue
        if name in lookup and lookup[name] != item["url"]:
            dup.append(name)  # 同名不同图：保留先出现的，只告警
            continue
        lookup[name] = str(item["url"])
        rel = str(item.get("rel") or "")
        if rel:
            lookup.setdefault(rel, str(item["url"]))
    return lookup, dup


def _fill_one(value, lookup: dict[str, str], stats: dict) -> str:
    if not isinstance(value, str):
        return value
    name = _basename(value)
    if not name or name not in lookup:
        return value
    new = lookup[name]
    if new != value:
        stats["changed"] += 1
    return new


def _fill_node(node, lookup: dict[str, str], stats: dict) -> None:
    if isinstance(node, dict):
        for key, value in list(node.items()):
            if key in MEDIA_KEYS:
                if isinstance(value, list):
                    node[key] = [_fill_one(v, lookup, stats) for v in value]
                else:
                    node[key] = _fill_one(value, lookup, stats)
            elif key in URL_OBJECT_KEYS:
                if isinstance(value, dict) and "url" in value:
                    value["url"] = _fill_one(value["url"], lookup, stats)
                elif isinstance(value, str):
                    node[key] = _fill_one(value, lookup, stats)
            elif isinstance(value, (dict, list)):
                _fill_node(value, lookup, stats)
            elif key == "url":
                node[key] = _fill_one(value, lookup, stats)
    elif isinstance(node, list):
        for item in node:
            _fill_node(item, lookup, stats)


def fill_json(project: Path, lookup: dict[str, str], patterns: list[str],
              dry_run: bool = False) -> list[str]:
    """把公网直链按文件名回填进分镜 JSON / 裸请求体；返回日志行。"""
    logs: list[str] = []
    if not lookup:
        return ["[回填] 跳过：没有可用的外链清单"]

    targets: list[Path] = []
    for pat in patterns:
        if any(ch in pat for ch in "*?["):
            targets.extend(sorted(project.glob(pat)))
        else:
            cand = project / pat
            if cand.is_file():
                targets.append(cand)

    for path in dict.fromkeys(targets):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            logs.append(f"[回填] 跳过 {path.name}：{exc}")
            continue
        stats = {"changed": 0}
        _fill_node(data, lookup, stats)
        rel = path.relative_to(project)
        if not stats["changed"]:
            logs.append(f"[回填] {rel}：无需改动")
            continue
        if dry_run:
            logs.append(f"[回填] {rel}：将改 {stats['changed']} 处（dry-run 未写）")
            continue
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        logs.append(f"[回填] {rel}：已改 {stats['changed']} 处")
    if not targets:
        logs.append("[回填] 没有找到分镜 JSON / 裸请求体（跳过）")
    return logs


# ---------------------------------------------------------------- --verify-json

def _head(url: str, timeout: int = 10) -> str:
    """HEAD 核验：返回 HTTP 状态码或 `ERR:xxx`（中文/空格自动转义）。"""
    parts = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(unquote(parts.path), safe="/:@!$&'()*+,;=~-._")
    req_url = urllib.parse.urlunsplit((parts.scheme, parts.netloc, safe_path,
                                       parts.query, parts.fragment))
    try:
        req = urllib.request.Request(req_url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return str(resp.status)
    except Exception as exc:  # noqa: BLE001
        return f"ERR:{exc}"


def iter_media_urls(node, path: str = "") -> list[tuple[str, str]]:
    """收集 JSON 里所有媒体直链 → [(JSON 路径, url)]。"""
    out: list[tuple[str, str]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}.{key}" if path else key
            if key in ("refs_urls", "ref_audio_urls", "ref_video_urls", "voice_urls") \
                    and isinstance(value, list):
                out += [(here, str(v)) for v in value if isinstance(v, str) and v.strip()]
            elif key in URL_OBJECT_KEYS and isinstance(value, dict):
                url = str(value.get("url") or "").strip()
                if url:
                    out.append((here, url))
            elif isinstance(value, (dict, list)):
                out += iter_media_urls(value, here)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            out += iter_media_urls(item, f"{path}[{i}]")
    return out


def verify_json(project: Path, patterns: list[str]) -> list[str]:
    """对 JSON 里已有直链做 HEAD 核验；返回日志行（含 ❌ 汇总）。"""
    logs: list[str] = []
    targets: list[Path] = []
    for pat in patterns:
        if any(ch in pat for ch in "*?["):
            targets.extend(sorted(project.glob(pat)))
        else:
            cand = project / pat
            if cand.is_file():
                targets.append(cand)
    if not targets:
        return ["[核验] 没有找到分镜 JSON（跳过）"]

    bad = 0
    checked = 0
    for path in dict.fromkeys(targets):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            logs.append(f"[核验] 跳过 {path.name}：{exc}")
            continue
        rel = path.relative_to(project)
        for where, url in iter_media_urls(data):
            if not url.startswith(("http://", "https://")):
                logs.append(f"[核验] {rel} · {where} 非绝对直链：{url}")
                bad += 1
                continue
            code = _head(url)
            checked += 1
            if not code.startswith("2"):
                logs.append(f"[核验] ❌ {rel} · {where} [{code}] {url}")
                bad += 1
    logs.append(f"[核验] HEAD {checked} 条 · ❌ {bad} 条")
    return logs


def main() -> None:
    ap = argparse.ArgumentParser(
        description="上传 MV 项目素材（图片 / 可选成片片段）到 public 命名空间，并回填/核验直链")
    ap.add_argument("project", help="项目目录，如 assets/output/M01-lanlantian")
    ap.add_argument("--prefix", default="", help="public 命名空间，默认取项目文件夹名")
    ap.add_argument("--verify", action="store_true", help="上传后 HEAD 核验外链")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不上传")
    ap.add_argument("--with-clips", action="store_true",
                    help="连 成片片段/ 一起上传（帧接续/视频延长要用）")
    ap.add_argument("--with-line-audio", action="store_true",
                    help="连 00-输入/音频/ 里被 ref_audio_urls 引用的参考音频一起上传（30s 说唱对口型用）")
    ap.add_argument("--no-images", action="store_true", help="不上传 图片/")
    ap.add_argument("--keep-staging", action="store_true",
                    help="保留 00-输入/上传暂存/（默认上传+回填成功后删除）")
    ap.add_argument("--force", action="store_true", help="跳过 /var/www/public/mv 预检查（仍可能失败）")
    ap.add_argument("--dest", default=os.environ.get("ASSET_DEST_DIR", ""), help="覆盖上传器目标根目录（默认读 ASSET_DEST_DIR / material-uploader config）")
    ap.add_argument("--url-base", default=os.environ.get("ASSET_URL_BASE", ""), help="覆盖外链根（默认读 ASSET_URL_BASE / config 的 url_base）")
    ap.add_argument("--no-url-encode", action="store_true",
                    help="关闭外链百分号编码（默认开；中文路径必须编码，否则服务端大概率 404）")
    ap.add_argument("--probe", action="store_true",
                    help="只做落点探测：往命名空间写 1KB 文件并 HEAD 外链，打印磁盘/URL 对照，通过再传全量")
    ap.add_argument("--all-images", action="store_true",
                    help=f"上传 {IMAGE_ROOT}/ 下全部文件（默认只传分镜JSON 里 refs_urls 引用到的那些；"
                         f"JSON 还没写时自动改为全部）")
    ap.add_argument("--fill-json", action="store_true",
                    help="上传后按文件名把公网直链回填进 分镜JSON.json / 裸请求体")
    ap.add_argument("--fill-only", action="store_true",
                    help="不重传：只用 03-上传/素材外网路径.json 里已保存的直链回填 JSON")
    ap.add_argument("--fill-target", action="append", default=[],
                    help=f"自定义回填目标（相对项目目录，可多次；默认 {FILL_TARGETS}）")
    ap.add_argument("--verify-json", action="store_true",
                    help="不重传：只对 JSON 里已有直链做 HEAD 核验（可单独使用）")
    args = ap.parse_args()

    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        sys.exit(f"[FAIL] 项目目录不存在：{project}")
    name = args.prefix.strip() or project.name
    patterns = args.fill_target or FILL_TARGETS

    # 只核验：不碰上传器
    if args.verify_json:
        for line in verify_json(project, patterns):
            print(line)
        return

    # 只回填：读已保存的 03-上传/素材外网路径.json，不重传
    if args.fill_only:
        manifest = project / PERSIST_DIR / PERSIST_MANIFEST
        if not manifest.is_file():
            sys.exit(f"[FAIL] 找不到已保存的上传清单：{manifest}\n"
                     f"  先跑：python3 scripts/upload_project.py {args.project} --verify --fill-json")
        lookup, dup = load_manifest(manifest)
        for warn in dup:
            print(f"[回填][warn] 同名文件多个外链，已保留先出现的：{warn}", file=sys.stderr)
        for line in fill_json(project, lookup, patterns):
            print(line)
        return

    if UPLOADER is None:
        sys.exit("[FAIL] 找不到上传脚本：scripts/material-uploader/upload_assets.py")

    # 0) 落点探测：只写 1KB 探测文件 + HEAD，验「磁盘落点 ↔ URL」是否一致
    if args.probe:
        cmd = [sys.executable, str(UPLOADER), "--src", str(project), "--name", name, "--probe"]
        if args.dest:
            cmd += ["--dest", args.dest]
        if args.url_base:
            cmd += ["--url-base", args.url_base]
        if args.no_url_encode:
            cmd.append("--no-url-encode")
        print("[probe] " + " ".join(cmd))
        sys.exit(subprocess.run(cmd).returncode)

    # /var/www/public/mv 预检查（material-uploader 的目标根）
    dest_root = args.dest or os.environ.get("ASSET_DEST_DIR") or "/var/www/public/mv"
    try:
        cfg_path = UPLOAD_CONFIG if UPLOAD_CONFIG.is_file() else UPLOAD_CONFIG_EXAMPLE
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        dest_root = args.dest or os.environ.get("ASSET_DEST_DIR") or str(cfg.get("dest_dir") or dest_root)
    except Exception:  # noqa: BLE001
        pass
    if not Path(dest_root).is_dir() and not args.force and not args.dry_run:
        sys.exit(
            f"[FAIL] 目标根不存在：{dest_root}\n"
            f"  本机没有 {dest_root}；请到服务器/容器里跑，或挂载站点目录。\n"
            f"  预览可加 --dry-run；跳过检查加 --force（仍可能因目录不可写失败）；\n"
            f"  换环境用 --dest / --url-base 覆盖，别改配置文件。"
        )

    # 1) 建暂存镜像（先清空，避免上次遗留）
    staging = project / "00-输入" / "上传暂存" / name
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True, exist_ok=True)

    if args.all_images:
        n_img = 0 if args.no_images else mirror_dir(
            project / IMAGE_ROOT, staging / IMAGE_ROOT, (".png", ".jpg", ".jpeg", ".webp"))
    else:
        # 默认只传被 refs_urls 引用的图；JSON 还没写（③ 之前的上传门）时自动改为全部
        n_img = 0
        if not args.no_images:
            refs = collect_ref_images(project, patterns)
            if not refs:
                print(f"[素材] 未找到 refs_urls 引用（JSON 可能还没写）→ 改为上传 {IMAGE_ROOT}/ 全部图片")
                n_img = mirror_dir(project / IMAGE_ROOT, staging / IMAGE_ROOT,
                                   (".png", ".jpg", ".jpeg", ".webp"))
            for rel in refs:
                src_file = project / rel
                if not src_file.is_file():
                    print(f"[素材][warn] JSON 引用的图片不存在，跳过：{rel}", file=sys.stderr)
                    continue
                link_or_copy(src_file, staging / rel)
                n_img += 1
    n_clip = mirror_clips(project / CLIPS_ROOT, staging / CLIPS_ROOT) if args.with_clips else 0

    n_line = 0
    if args.with_line_audio:
        line_files, line_missing = collect_ref_audio(project, patterns)
        if line_missing:
            sys.exit("[FAIL] 分镜 JSON 引用的逐句音频不存在：\n  - " + "\n  - ".join(line_missing)
                     + "\n  先跑：python3 scripts/line_audio.py <项目> --bind")
        if not line_files:
            print("[素材] ⚠ 分镜 JSON 里没有 ref_audio_urls：本片不是逐句演唱版，跳过逐句音频")
        for src_file in line_files:
            link_or_copy(src_file, staging / LINE_AUDIO_ROOT / src_file.name)
            n_line += 1

    if n_img + n_clip + n_line == 0:
        sys.exit(f"[FAIL] 没有可上传的素材（{IMAGE_ROOT}/ 为空"
                 f"{'，且未加 --with-clips' if not args.with_clips else ''}"
                 f"{'，且未加 --with-line-audio' if not args.with_line_audio else ''}）")

    print(f"[暂存] {staging}")
    print(f"[素材] 图片 {n_img}"
          + (f" · 成片片段 {n_clip}" if args.with_clips else "")
          + (f" · 逐句音频 {n_line}" if args.with_line_audio else ""))

    # 2) 调 material-uploader；目标目录已存在时默认整目录覆盖
    cmd = [
        sys.executable, str(UPLOADER),
        "--src", str(staging),
        "--keep-source", "--no-purge-project",
        "--json",
    ]
    if args.dest:
        cmd += ["--dest", args.dest]
    if args.url_base:
        cmd += ["--url-base", args.url_base]
    cmd.append("--no-url-encode" if args.no_url_encode else "--url-encode")
    if args.verify:
        cmd.append("--verify")
    if args.dry_run:
        cmd.append("--dry-run")

    print("[执行] " + " ".join(cmd))
    proc = subprocess.run(cmd)

    # 3) 保存上传清单到 03-上传/（供 JSON 写好后 --fill-only 回填）
    bad_http: list[str] = []
    if proc.returncode == 0 and not args.dry_run:
        src_manifest = staging / MANIFEST
        if src_manifest.is_file():
            dst_manifest = project / PERSIST_DIR / PERSIST_MANIFEST
            dst_manifest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_manifest, dst_manifest)
            print(f"[清单] {dst_manifest}")
            if args.verify:
                try:
                    data = json.loads(src_manifest.read_text(encoding="utf-8"))
                    for item in data.get("items", []):
                        http = str(item.get("http") or "")
                        if item.get("status") == "ok" and not http.startswith("2"):
                            bad_http.append(f"{item.get('rel') or item.get('name')} [{http}]")
                except (OSError, ValueError):
                    pass

    # 4) 回填公网直链（上传成功才做；dry-run 只报告将改几处）
    if args.fill_json and proc.returncode == 0:
        lookup, dup = load_manifest(staging)
        for warn in dup:
            print(f"[回填][warn] 同名文件多个外链，已保留先出现的：{warn}", file=sys.stderr)
        for line in fill_json(project, lookup, patterns, dry_run=args.dry_run):
            print(line)

    # 5) 清暂存（上传成功或 dry-run 预览完，未 --keep-staging）
    if proc.returncode == 0 and not args.keep_staging:
        shutil.rmtree(staging, ignore_errors=True)
        try:
            staging.parent.rmdir()      # 上传暂存/ 空了就一起删
        except OSError:
            pass
        tag = "dry-run 预览完" if args.dry_run else "上传完成"
        print(f"[清暂存] {tag}，已删除 {staging}（--keep-staging 可保留）")

    if bad_http:
        print("[FAIL] 外链核验未通过（上传门不放行）：", file=sys.stderr)
        for line in bad_http:
            print(f"  ❌ {line}", file=sys.stderr)
        print("  检查命名空间/路径/站点目录；修好后重跑本命令。", file=sys.stderr)
        sys.exit(2)

    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
