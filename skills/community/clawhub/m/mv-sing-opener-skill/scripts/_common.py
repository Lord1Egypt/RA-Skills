#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mv-sing-opener-skill 脚本公共层。

只做四件事，全部零依赖（标准库）：

1. **路径解析**：项目目录（绝对/相对/`assets/output/<名字>`）、参考图、分镜 JSON；
2. **配置读取**：`scripts/config.json`（外链根 / 出图接口 / 出片网关）；
3. **外链工具**：外链根、文件名归一、公网直链拼接（与 material-uploader 口径一致）；
4. **素材定位**：按名字递归扫 `04-图片/**`（`图N_名称.png` 可带可不带扩展名）。

被 `upload_project.py` / `generate_images.py` / `generate_video.py` / `test_image_api.py` 共用。
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
OUTPUT_ROOT = SKILL_ROOT / "assets" / "output"
CONFIG_PATH = SCRIPT_DIR / "config.json"
EXAMPLE_CONFIG_PATH = SCRIPT_DIR / "config.example.json"

DEFAULT_URL_BASE = "https://your-static-host.example.com/public/mv"
DEFAULT_DEST_DIR = "/var/www/public/mv"
DEFAULT_MODEL = "doubao-seedance-2-5-260628"
DEFAULT_GATEWAY = "http://127.0.0.1:4000"

IMAGE_ROOT = "04-图片"          # 人物参考图落点：<项目>/04-图片/ref_人物.png
CLIPS_ROOT = "成片片段"          # 出片落点：<项目>/成片片段/S01.mp4（与多镜 MV 流程保持一致）
PLAN_DIRS = ("04-提示词",)
PLAN_NAME = "分镜JSON.json"
PROMPTS_NAME = "文生图提示词.json"

# 本地环境变量：.env 不进 Git，密钥/本地地址都放这里
ENV_PATH = SKILL_ROOT / ".env"


def _load_env_file() -> None:
    """把 `.env` 里的 KEY=VALUE 读进 os.environ；已有的环境变量优先，不覆盖。"""
    if not ENV_PATH.is_file():
        return
    for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


_load_env_file()

# 兄弟目录 fallback（同级 skill 目录树；整包拷走后不存在也不影响）
_SIBLING_ROOT = SKILL_ROOT.parents[1] if len(SKILL_ROOT.parents) > 1 else SKILL_ROOT.parent
# 出图接口/出片网关只读本 skill scripts/config.json（不引用同级 skill）
# 上传器只用本 skill 内置副本（scripts/material-uploader），不引用同级 skill


# ---------------------------------------------------------------- 配置
def load_config() -> dict:
    """读本 skill 的 `scripts/config.json`；没有就回退到 `config.example.json`。"""
    cfg: dict = {}
    for path in (CONFIG_PATH, EXAMPLE_CONFIG_PATH):
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(data, dict):
            cfg.update({k: v for k, v in data.items() if not k.startswith("_")})
        break
    return cfg


def url_base() -> str:
    return str(os.environ.get("ASSET_URL_BASE") or load_config().get("asset_url_base") or DEFAULT_URL_BASE).rstrip("/") + "/"


def image_api_config() -> dict:
    """出图接口配置：`--base-url/--key/--model` > 环境变量 > config.json > 内置默认。"""
    cfg = load_config()
    return {
        "base_url": (os.environ.get("NEWAPI_IMAGE_BASE_URL")
                     or cfg.get("newapi_image_base_url") or "https://your-image-api.example.com"),
        "key": os.environ.get("NEWAPI_IMAGE_KEY") or cfg.get("newapi_image_key") or "",
        "model": (os.environ.get("NEWAPI_IMAGE_MODEL")
                  or cfg.get("newapi_image_model") or "gpt-image-2-c"),
        "quality": (os.environ.get("NEWAPI_IMAGE_QUALITY")
                    or cfg.get("newapi_image_quality") or "high"),
    }


def video_api_config() -> dict:
    """出片网关/模型：环境变量 > config.json > 内置默认。"""
    cfg = load_config()
    return {
        "base": (os.environ.get("VIDEO_GATEWAY_BASE")
                 or cfg.get("gateway_base") or DEFAULT_GATEWAY),
        "model": os.environ.get("VIDEO_MODEL") or cfg.get("model") or DEFAULT_MODEL,
        "prefix": (os.environ.get("VIDEO_API_PREFIX")
                   or cfg.get("video_api_prefix") or "/v1"),
    }


# ---------------------------------------------------------------- 路径
def resolve_uploader(explicit: str = "") -> Path | None:
    """上传器解析顺序：显式 > 本 skill 自带（`scripts/material-uploader`）> None。"""
    cands: list[Path] = []
    if explicit:
        cands.append(Path(explicit).expanduser())
    cands.append(SCRIPT_DIR / "material-uploader" / "upload_assets.py")
    for path in cands:
        if path.is_file():
            return path
    return None


def resolve_project(arg: str) -> Path:
    """项目目录：绝对/相对路径优先，其次 `assets/output/<名字>`。"""
    p = Path(arg).expanduser()
    if p.is_dir():
        return p.resolve()
    for cand in (OUTPUT_ROOT / arg, OUTPUT_ROOT / arg.strip("/")):
        if cand.is_dir():
            return cand.resolve()
    raise SystemExit(f"[FAIL] 找不到项目目录：{arg}\n"
                     f"       已尝试：{p}、{OUTPUT_ROOT / arg}")


def project_root_for(plan_path: Path) -> Path:
    """分镜 JSON 所在路径 → 项目根。

    `05-视频生成提示词/分镜JSON.json` → 项目根；
    `05-视频生成提示词/裸请求体/S01.json` → 项目根；
    裸 JSON 直接放项目根 → 项目根本身。
    """
    parent = plan_path.parent
    for _ in range(3):
        if parent.name in PLAN_DIRS:
            return parent.parent
        if parent.parent == parent:
            break
        parent = parent.parent
    return plan_path.parent


def project_prompts(project: Path) -> Path:
    return project / PROMPTS_NAME


def project_plan(project: Path, name: str = PLAN_NAME) -> Path:
    """分镜 JSON：优先 `05-视频生成提示词/`，其次 `05-提示词/`，最后项目根。"""
    for cand in [project / d / name for d in PLAN_DIRS] + [project / name]:
        if cand.is_file():
            return cand
    return project / PLAN_DIRS[0] / name


def find_ref_image(project: Path, name: str) -> Path | None:
    """按名字找参考图：递归扫 `图片/**`。

    `name` 可带或不带扩展名、可带子目录；多个同名时取路径最短的那个。
    """
    img_root = project / IMAGE_ROOT
    if not img_root.is_dir():
        return None
    stem = Path(name).stem or Path(name).name
    hits = [p for p in img_root.rglob("*")
            if p.is_file() and (p.stem == stem or p.name == name)]
    if not hits:
        return None
    return sorted(hits, key=lambda p: (len(p.parts), str(p)))[0]


# ---------------------------------------------------------------- URL
def url_filename(url: str) -> str:
    """取 URL 里的文件名（解码百分号）；带查询串也能取对。"""
    try:
        path = urlparse(str(url)).path
    except ValueError:
        path = str(url)
    return Path(unquote(path)).name


def public_url(prefix: str, *parts: str, encode: bool = False) -> str:
    """拼公网直链：外链根 + prefix + 各段（与 material-uploader 的 build_url 口径一致）。"""
    segs = [str(prefix).strip("/")] if str(prefix).strip("/") else []
    segs += [str(p).strip("/") for p in parts if str(p).strip("/")]
    tail = "/".join(segs)
    if encode:
        tail = quote(tail, safe="/")
    return url_base() + tail
