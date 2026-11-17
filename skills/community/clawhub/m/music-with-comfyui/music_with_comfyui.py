#!/usr/bin/env python3
"""
music_with_comfyui.py - Call a ComfyUI server to generate music/audio with
the AceStep Audio 1.5 workflow (text/lyrics -> audio).

Mode:
    music   Text-to-Music (AceStep Audio 1.5)

Usage:
    python3 music_with_comfyui.py music --tags "..." [--lyrics "..."]
    python3 music_with_comfyui.py music --tags "..." --lyrics "..." --duration 120
    python3 music_with_comfyui.py music --tags "..." --lyrics "..." --bpm 120
    python3 music_with_comfyui.py music --duration 90 --seed 42
    python3 music_with_comfyui.py music --prompt "..."  (alias of --tags)
    python3 music_with_comfyui.py test

Configuration:
    Reads config from this SKILL's config.json (relative to this script).
    The endpoint is user-defined: COMFYUI_URL env var, or comfyui_url in
    config.json (bundled default http://localhost:8188). If no ComfyUI server
    is reachable, the script exits with configuration instructions.
    Environment overrides:
      COMFYUI_URL              endpoint (non-local hosts print a warning)
      COMFYUI_TIMEOUT          global generation timeout in seconds
      COMFYUI_POLL_INTERVAL    polling interval in seconds
      COMFYUI_OUTPUT_DIR       output directory
      COMFYUI_APIKEY           ComfyUI Bearer API key

Data flow:
    Prompts (tags/lyrics) and the workflow JSON are sent to the configured
    endpoint; generated audio is written to the media output directory
    (config output_dir / COMFYUI_OUTPUT_DIR). After the local save succeeds the
    script posts /purge_after_retrieval to delete the server-side copy
    (disabled by --keep / purge_remote: false / COMFYUI_PURGE=0).
"""

import argparse
import base64
import copy
import io
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

# ---------------------------------------------------------------------------
# Safe redirect: never let the Bearer key follow a cross-origin 3xx
# ---------------------------------------------------------------------------
# The default urllib opener carries the Authorization header across 3xx
# redirects, which would leak the ComfyUI Bearer key to a different origin.
# We install a custom opener that strips the header before following any
# cross-origin redirect; same-origin redirects keep the header exactly as
# before. This is defense-in-depth (there is no exploitable redirect route in
# this workflow) but keeps the API key from ever leaving the configured host.

def _request_origin(url) -> tuple:
    """Return (scheme, host, port) identifying a URL's origin (RFC 6454)."""
    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or "").lower()
    port = parsed.port
    return (parsed.scheme or "", host, port)


class _SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Strip the Authorization header before following any redirect that would
    leave the request's own origin. Same-origin redirects behave as before."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        try:
            if _request_origin(newurl) != _request_origin(
                req.full_url if hasattr(req, "full_url") else req.get_full_url()
            ):
                # Cross-origin: drop the Bearer key before following.
                req.headers.pop("Authorization", None)
        except ValueError:
            # Unparseable URL — fall back to default behaviour (keep header).
            pass
        return super().redirect_request(req, fp, code, msg, headers, newurl)


# Build the custom opener first, then route every request through it so the
# Bearer key is only ever sent to the configured endpoint.
_SAFE_OPEN = urllib.request.build_opener(_SafeRedirectHandler())


def _safe_urlopen(req, *args, **kwargs):
    """urllib.request.urlopen replacement that routes through _SAFE_OPEN so the
    Bearer key is never sent across an origin change. Accepts a Request or URL
    string plus urlopen's usual kwargs (data, timeout, ...)."""
    if isinstance(req, urllib.request.Request):
        wrapped = req
    else:
        wrapped = urllib.request.Request(req, data=kwargs.pop("data", None))
    opener = kwargs.pop("opener", _SAFE_OPEN)
    return opener.open(wrapped, *args, **kwargs)


# Patch once: every call site (submit / history / view / purge / health) now
# uses the safe opener automatically.
urllib.request.urlopen = _safe_urlopen

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = SCRIPT_DIR / "config.json"

# Workspace / config directory detection — mirror image_with_comfyui.
def resolve_config_dir(env=None, homedir=None) -> Path:
    """Replicate OpenClaw's config-dir resolution (resolveConfigDir)."""
    if env is None:
        env = os.environ
    if homedir is None:
        homedir = os.path.expanduser("~")
    override = (env.get("OPENCLAW_STATE_DIR") or "").strip()
    if override:
        return Path(override).expanduser().resolve()
    config_path = (env.get("OPENCLAW_CONFIG_PATH") or "").strip()
    if config_path:
        return Path(config_path).expanduser().resolve().parent
    return Path(homedir).expanduser().resolve() / ".openclaw"

def find_workspace_dir(env=None) -> Path:
    if env is None:
        env = os.environ
    ws = (env.get("OPENCLAW_WORKSPACE_DIR") or "").strip()
    if ws:
        return Path(ws).expanduser().resolve()
    return resolve_config_dir(env)

WORKSPACE_DIR = find_workspace_dir()

def _endpoint_disclosure(cfg: dict) -> None:
    """Disclose data flow when the endpoint is non-local."""
    url = cfg.get("comfyui_url", "")
    try:
        parsed = urllib.parse.urlparse(url)
    except ValueError:
        return
    host = (parsed.hostname or "").lower()
    if host in ("127.0.0.1", "localhost", "local", "0.0.0.0", "::1"):
        return
    scheme = (parsed.scheme or "http").upper()
    print(
        f"⚠️  Non-local ComfyUI endpoint: {url} — prompts, lyrics and "
        f"(when given) a full reference image will be sent to this host via "
        f"{scheme}. Only point COMFYUI_URL at a server you control.",
        file=sys.stderr,
    )

def load_config() -> dict:
    """Load config from config.json, then apply env overrides."""
    config_path = SCRIPT_DIR / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    env_url = os.environ.get("COMFYUI_URL")
    if env_url:
        cfg["comfyui_url"] = env_url
    env_poll = os.environ.get("COMFYUI_POLL_INTERVAL")
    if env_poll:
        cfg["poll_interval_seconds"] = int(env_poll)
    env_timeout = os.environ.get("COMFYUI_TIMEOUT")
    if env_timeout:
        cfg["timeout_seconds"] = int(env_timeout)
    env_out = os.environ.get("COMFYUI_OUTPUT_DIR")
    if env_out:
        cfg["output_dir"] = env_out
    env_keep = os.environ.get("COMFYUI_KEEP_MODELS_RESIDENT")
    if env_keep is not None:
        cfg["keep_models_resident"] = env_keep.strip().lower() in ("1", "true", "yes", "on")
    env_key = os.environ.get("COMFYUI_APIKEY")
    if env_key is not None:
        cfg["comfyui_api_key"] = env_key.strip()
    cfg.setdefault("comfyui_api_key", "")
    # 取回即删：默认开；COMFYUI_PURGE=0 全局关（--keep 是单次关）
    env_purge = os.environ.get("COMFYUI_PURGE")
    if env_purge is not None:
        cfg["purge_remote"] = env_purge.strip().lower() in ("1", "true", "yes", "on")
    cfg.setdefault("purge_fail_hints", 0)  # 取回后删除的失败提示计数（状态存 config；成功删除自动归零）
    _endpoint_disclosure(cfg)
    return cfg

# ── 取回后删除（purge）──────────────────────────────────────────────────────
# 本地音频落盘成功后，调 ComfyUI 服务端的 /purge_after_retrieval 端点删掉服务端
# 生成的那份音频（AceStep 工作流不上传任何输入文件，所以只删产物本身）。
# 删除失败（通常是服务端没装 purge_after_retrieval 插件）时：
# 提示用户安装插件，最多 3 次；3 次之后不再提示，默认按 --keep 处理（保留服务端文件）。
# 状态存 config.json 的 "purge_fail_hints" 项目（0=正常；1-3=已提示删除失败的次数）。
# 重新启用：服务端装好插件后把 config.json 的 purge_fail_hints 置 0（成功删除一次也会自动归零）。
PURGE_MAX_HINTS = 3
PURGE_PLUGIN_REPO = "https://github.com/sunshinejnjn/comfyui-purge-after-retrieval"


def _save_purge_fail_hints(n: int) -> None:
    """把删除失败提示计数写回 config.json 的 purge_fail_hints 项目（只改这一个键，不动其他配置）。"""
    try:
        cfg_path = SCRIPT_DIR / "config.json"
        with open(cfg_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["purge_fail_hints"] = n
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
    except Exception:
        pass


def _print_purge_hint(hints: int) -> None:
    print(f"   💡 提示 {hints}/{PURGE_MAX_HINTS}：删除失败，ComfyUI 服务端可能未安装 purge 插件。"
          f"装上它才能实现「取回后自动删除服务端生成的音频」：")
    print(f"      在服务端执行: git clone {PURGE_PLUGIN_REPO} <ComfyUI目录>/custom_nodes/purge_after_retrieval 然后重启 ComfyUI")
    print(f"      安装/配置文档: {PURGE_PLUGIN_REPO}")
    if hints >= PURGE_MAX_HINTS:
        print("      （这是最后一次提示。之后默认保留服务端文件；服务端装好插件后把 config.json 的 purge_fail_hints 置 0 可恢复自动删除）")


def purge_remote(cfg: dict, items: list) -> None:
    """取回后销毁服务端副本：调 /purge_after_retrieval 删掉本次任务在 ComfyUI 服务器上的音频。

    items: [{filename, subfolder, type}]（与 get_output_audios 同构）。
    只在本地落盘成功后调用；任何失败都是 warning 而非致命（本地文件已到手）。
    config: "purge_remote": true（默认开），CLI --keep 可关。
    提示计数存 config.json 的 purge_fail_hints 项目，成功删除一次即自动归零。
    """
    if not items:
        return
    if not cfg.get("purge_remote", True):
        print("   (purge: 已在 config 关闭，服务端文件保留)")
        return
    try:
        hints = int(cfg.get("purge_fail_hints", 0))
    except (TypeError, ValueError):
        hints = 0
    if hints >= PURGE_MAX_HINTS:
        # 已提示满 3 次：不再提示，默认按 --keep 处理（保留服务端文件，不再尝试删除）
        print("   (purge: 之前删除失败已提示 3 次，现默认保留服务端文件；服务端装好插件后把 config.json 的 purge_fail_hints 置 0 恢复自动删除)")
        return
    files = [
        {"filename": it.get("filename", ""), "subfolder": it.get("subfolder", ""),
         "type": it.get("type", "output")}
        for it in items if it.get("filename")
    ]
    if not files:
        return
    try:
        body = json.dumps({"files": files}).encode("utf-8")
        req = urllib.request.Request(
            api_url(cfg, "/purge_after_retrieval"), data=body, method="POST",
            headers=_merge_headers(auth_headers(cfg), {"Content-Type": "application/json"}),
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            res = json.loads(resp.read().decode())
        purged = res.get("purged", [])
        skipped = res.get("skipped", [])
        print(f"   🧹 服务端已销毁 {len(purged)} 个文件" + (f"（{len(skipped)} 个跳过）" if skipped else ""))
        if res.get("ok"):
            _save_purge_fail_hints(0)  # 恢复正常：计数写回 0
    except Exception as e:
        print(f"   ⚠️ 服务端文件清理失败（不影响本次结果，文件仍留在服务器）: {e}", file=sys.stderr)
        if hints < PURGE_MAX_HINTS:
            hints += 1
            _save_purge_fail_hints(hints)
            _print_purge_hint(hints)


def _endpoint_setup_help(cfg: dict, err: Exception) -> None:
    """Explain how to point this skill at a reachable ComfyUI server."""
    source = "COMFYUI_URL env var" if os.environ.get("COMFYUI_URL") else "comfyui_url in config.json"
    print(f"❌ Cannot reach the ComfyUI server at {cfg['comfyui_url']} (endpoint from {source})",
          file=sys.stderr)
    print(f"   Connection error: {err}", file=sys.stderr)
    print("   To configure this skill:", file=sys.stderr)
    print("     1. Start a ComfyUI server (see README.md → 'Models & Custom Nodes')", file=sys.stderr)
    print("     2. Point the skill at it: export COMFYUI_URL=http://host:port", file=sys.stderr)
    print("        or edit \"comfyui_url\" in the skill's config.json", file=sys.stderr)
    print("     3. Verify: python3 music_with_comfyui.py test", file=sys.stderr)

def ensure_comfyui_reachable(cfg: dict) -> None:
    """Fail fast with setup instructions when no ComfyUI server answers."""
    url = cfg["comfyui_url"].rstrip("/") + "/history"
    try:
        req = urllib.request.Request(url, method="GET", headers=auth_headers(cfg))
        with urllib.request.urlopen(req, timeout=5):
            pass
    except Exception as e:
        _endpoint_setup_help(cfg, e)
        sys.exit(1)

# ---------------------------------------------------------------------------
# Config accessors
# ---------------------------------------------------------------------------

def get_music_cfg(cfg: dict) -> dict:
    """Get the music (AceStep) config section."""
    return cfg["music"]["acestep15"]

def get_output_subdir(cfg: dict, model_id: str = None) -> str:
    if model_id:
        return get_music_cfg(cfg).get("output_subdir", "music")
    return "music"

def ensure_output_dir(cfg: dict, model_id: str = None, cmd_output_dir: str = None) -> Path:
    if cmd_output_dir:
        return Path(resolve_workspace_path(cmd_output_dir))
    base = Path(resolve_workspace_path(cfg.get("output_dir", "media/comfyui")))
    if model_id:
        output_subdir = get_output_subdir(cfg, model_id)
        return base / output_subdir
    return base

# ---------------------------------------------------------------------------
# Node package mapping — mirrors the image skill (used only for error text).
# The AceStep 1.5 audio workflow uses core ComfyUI nodes plus a small set of
# AceStep / audio custom nodes.
# ---------------------------------------------------------------------------

NODE_PACKAGE_MAP = {
    "TextEncodeAceStepAudio1.5": ("AceStep-ComfyUI", "https://github.com/AceStep/AceStep-ComfyUI"),
    "EmptyAceStep1.5LatentAudio": ("AceStep-ComfyUI", "https://github.com/AceStep/AceStep-ComfyUI"),
    "VAEDecodeAudio": ("ComfyUI-Audio", "https://github.com/ligersearch/ComfyUI-Audio"),
    "SaveAudioAdvanced": ("ComfyUI-VideoHelperSuite", "https://github.com/Fannovel16/ComfyUI-VideoHelperSuite"),
    "VAEDecodeAudio": ("ComfyUI-Audio", "https://github.com/ligersearch/ComfyUI-Audio"),
}

# Core ComfyUI nodes used by the AceStep audio graph (e.g. the AuraFlow
# model-sampling node). A missing core node means "update ComfyUI", not
# "clone a custom package".
CORE_AUDIO_NODES = {
    "ModelSamplingAuraFlow",
}

def resolve_workspace_path(p: str) -> str:
    p = str(Path(p).expanduser())
    if not Path(p).is_absolute():
        p = str(WORKSPACE_DIR / p)
    return p

def resolve_skill_path(p: str) -> str:
    p = str(Path(p).expanduser())
    if not Path(p).is_absolute():
        p = str(SCRIPT_DIR / p)
    return p

# ---------------------------------------------------------------------------
# ComfyUI API helpers (same contract as the image skill)
# ---------------------------------------------------------------------------

def api_url(cfg: dict, path: str) -> str:
    base = cfg["comfyui_url"].rstrip("/")
    return f"{base}{path}"

def auth_headers(cfg: dict) -> dict:
    """Return {'Authorization': 'Bearer <key>'} when a key is configured."""
    key = (cfg.get("comfyui_api_key") or "").strip()
    if not key:
        return {}
    return {"Authorization": f"Bearer {key}"}

def _merge_headers(*dicts):
    merged = {}
    for d in dicts:
        merged.update(d)
    return merged

def fetch_object_info(cfg: dict) -> dict:
    req = urllib.request.Request(
        api_url(cfg, "/object_info"),
        method="GET",
        headers=auth_headers(cfg),
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())

def find_nodes_by_class(workflow: dict, class_type: str):
    results = []
    for node_id, node_data in workflow.items():
        if not isinstance(node_data, dict):
            continue
        if node_data.get("class_type") == class_type:
            results.append((node_id, node_data))
    return results

def find_node_package(class_type: str):
    if class_type in NODE_PACKAGE_MAP:
        return NODE_PACKAGE_MAP[class_type]
    ct_lower = class_type.lower().replace(" ", "").replace("_", "")
    for known, info in NODE_PACKAGE_MAP.items():
        known_norm = known.lower().replace(" ", "").replace("_", "")
        if known_norm in ct_lower or ct_lower in known_norm:
            return info
    return None

def bypass_node(workflow: dict, missing_node_id: str) -> dict:
    """Remove a missing sink node and reroute upstream → downstream."""
    modified = copy.deepcopy(workflow)
    missing_id = str(missing_node_id)
    downstream = {}
    for nid, nd in modified.items():
        for k, v in nd.get("inputs", {}).items():
            if isinstance(v, list) and len(v) >= 2 and v[0] == missing_id:
                downstream.setdefault(nid, []).append((k, str(v[1])))
    if not downstream:
        modified.pop(missing_id, None)
        return modified
    upstream_nids = []
    missing_node = modified.get(missing_id, {})
    for k, v in missing_node.get("inputs", {}).items():
        if isinstance(v, list) and len(v) >= 2:
            src_nid = str(v[0])
            if src_nid != missing_id:
                upstream_nids.append(src_nid)
    if not upstream_nids:
        modified.pop(missing_id, None)
        return modified
    up_nid = str(upstream_nids[0])
    updates = []
    for down_nid, connections in downstream.items():
        for param, port in connections:
            if down_nid in modified and param in modified[down_nid].get("inputs", {}):
                updates.append((down_nid, param, [up_nid, 0]))
    for dn, p, val in updates:
        modified[dn]["inputs"][p] = val
    modified.pop(missing_id, None)
    return modified

def submit_workflow_with_errors(cfg: dict, workflow: dict, timeout: int = 30,
                            skip_autosubstitute: bool = False):
    """Send workflow to ComfyUI and report missing-node / model problems."""
    warnings = []
    data = json.dumps({"prompt": workflow}).encode("utf-8")
    req = urllib.request.Request(
        api_url(cfg, "/prompt"),
        data=data,
        headers=_merge_headers(auth_headers(cfg), {"Content-Type": "application/json"}),
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            result = json.loads(e.read().decode())
        except Exception:
            result = {}

    error_type = result.get("error", {}).get("type", "")
    if error_type == "missing_node_type":
        class_type = result.get("error", {}).get("extra_info", {}).get("class_type", "Unknown")
        node_id = result.get("error", {}).get("extra_info", {}).get("node_id", "")
        if class_type == "UnloadAllModels":
            warnings.append(
                f"⚠️ Workflow missing node: `UnloadAllModels` (memory cleanup, non-critical)\n"
                f"🔄 Auto-bypassed — generation continues"
            )
            bypassed = bypass_node(workflow, node_id)
            return submit_workflow_with_errors(cfg, bypassed, timeout, skip_autosubstitute)
        if class_type in CORE_AUDIO_NODES:
            warnings.append(
                f"⚠️ Missing node: `{class_type}`\n"
                f"📦 ComfyUI **core** node — used by the AceStep 1.5 audio workflow\n"
                f"ℹ️ Update the ComfyUI server to a build that ships this core node and restart"
            )
            return None, f"missing_node: {class_type}", warnings
        pkg_info = find_node_package(class_type)
        if pkg_info:
            pkg_name, github_url = pkg_info
            warnings.append(
                f"⚠️ Missing node: `{class_type}`\n"
                f"📦 Package: {pkg_name}\n"
                f"🔗 GitHub: {github_url}\n"
                f"ℹ️ Install manually: cd ComfyUI/custom_nodes && git clone {github_url}"
            )
        else:
            warnings.append(f"⚠️ Missing node: `{class_type}` (unknown package, search GitHub)")
        return None, f"missing_node: {class_type}", warnings

    job_id = result.get("prompt_id")
    error_msg = result.get("error", {}).get("message", "") if "error" in result else ""
    return job_id, error_msg if error_msg else None, warnings

def wait_for_completion(cfg: dict, job_id: str, timeout: int = 120) -> dict:
    start = time.time()
    poll_interval = cfg.get("poll_interval_seconds", 10)
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(
                api_url(cfg, f"/history/{job_id}"),
                method="GET",
                headers=auth_headers(cfg),
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                history = json.loads(resp.read().decode())
        except urllib.error.URLError:
            time.sleep(poll_interval)
            continue
        status = history.get(job_id, {}).get("status", {})
        status_str = status.get("status_str", "")
        if status_str == "error":
            return history
        if status.get("completed"):
            return history
        time.sleep(poll_interval)
    raise TimeoutError(f"Generation timed out after {timeout}s (prompt_id={job_id})")

# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def sanitize_filename(filename, output_dir) -> str:
    if not filename or not isinstance(filename, str):
        print(f"⚠️ sanitize_filename: empty or non-string filename", file=sys.stderr)
        return None
    basename = Path(filename).name
    if not basename or basename in (".", ".."):
        print(f"⚠️ sanitize_filename: rejected suspicious name ({basename!r} from {filename!r})", file=sys.stderr)
        return None
    if "/" in basename or "\\" in basename:
        print(f"⚠️ sanitize_filename: path separator in filename ({filename!r})", file=sys.stderr)
        return None
    candidate = (output_dir / basename).resolve()
    if not str(candidate).startswith(str(output_dir.resolve())):
        print(f"⚠️ sanitize_filename: path traversal detected ({filename!r}) - dropping directory", file=sys.stderr)
        basename = Path(filename).name
        candidate = (output_dir / basename).resolve()
        if not str(candidate).startswith(str(output_dir.resolve())):
            return None
    return basename

def get_output_audios(history: dict, job_id: str, output_dir: Path):
    """Extract output audio entries from a prompt result."""
    audios = []
    for node_id, node_result in history.get(job_id, {}).get("outputs", {}).items():
        for item in node_result.get("audio", []):
            if item.get("type") == "output":
                safe_name = sanitize_filename(item.get("filename", ""), output_dir)
                if safe_name is None:
                    print(f"⚠️ Skipping unsafe audio filename from ComfyUI", file=sys.stderr)
                    continue
                audios.append({
                    "filename": safe_name,
                    "subfolder": item.get("subfolder", ""),
                    "type": item.get("type", "output"),
                })
    return audios

def audio_b64_from_comfyui(cfg: dict, audio: dict) -> str:
    params = urllib.parse.urlencode({
        "filename": audio["filename"],
        "subfolder": audio.get("subfolder", ""),
        "type": audio.get("type", "output"),
    })
    req = urllib.request.Request(
        f"{api_url(cfg, '/view')}?{params}",
        method="GET",
        headers=auth_headers(cfg),
    )
    with urllib.request.urlopen(req, timeout=cfg.get("timeout_seconds", 60)) as resp:
        return base64.b64encode(resp.read()).decode("utf-8")

def save_b64_audio(b64_data: str, filename: str, output_dir: Path) -> Path:
    safe_name = sanitize_filename(filename, output_dir)
    if safe_name is None:
        safe_name = f"music_{int(time.time())}.mp3"
    safe_name = _strip_trailing_underscore(safe_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / safe_name
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(b64_data))
    return out_path

def _strip_trailing_underscore(name: str) -> str:
    stem, _, ext = name.rpartition(".")
    if ext and stem.endswith("_"):
        return stem.rstrip("_") + "." + ext
    return name.rstrip("_")

def _save_prefix(base: str) -> str:
    ts = time.strftime("%Y%m%d_%H%M%S")
    return f"{base}_{ts}"

# ---------------------------------------------------------------------------
# Workflow preparation
# ---------------------------------------------------------------------------

def strip_unload_nodes(workflow: dict) -> dict:
    """When keep_models_resident is enabled, drop VRAM-cleanup nodes so the
    model stays resident between runs."""
    modified = copy.deepcopy(workflow)
    for nid, nd in list(modified.items()):
        if nd.get("class_type") in ("UnloadAllModels", "UnloadModel"):
            modified.pop(nid, None)
    return modified

def apply_keep_resident(cfg: dict, workflow: dict) -> dict:
    if cfg.get("keep_models_resident", False):
        return strip_unload_nodes(workflow)
    return workflow

def prepare_music_workflow(cfg: dict, tags: str, lyrics: str,
                           duration: int = None, seed: int = None,
                           override: dict = None) -> tuple[dict, int]:
    """Prepare the AceStep Audio 1.5 workflow.

    Returns (workflow, seed). The `override` dict may contain any of the
    text-encode params (bpm, keyscale, language, timesignature, cfg_scale,
    temperature, top_p, top_k, min_p, generate_audio_codes, duration).

    Note: AceStep 1.5 takes *only* text (tags + lyrics). There is no image
    input anywhere in this workflow, so no reference image is ever uploaded.
    If a user supplies an image, the agent (not the program) reads it and
    turns it into tags/lyrics before calling this function.
    """
    model_cfg = get_music_cfg(cfg)
    params = dict(model_cfg.get("default_params", {}))
    if override:
        params.update({k: v for k, v in override.items() if v is not None})

    workflow_path = resolve_skill_path(model_cfg["workflow_path"])
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    if duration is not None:
        params["duration"] = int(duration)
    if seed is None:
        seed = int(random.randint(0, 2**63 - 1))
    params["seed"] = seed

    # Set the AceStep text-encode node inputs (tags/lyrics + all params).
    for node_id, node_data in find_nodes_by_class(workflow, "TextEncodeAceStepAudio1.5"):
        node_data["inputs"]["tags"] = tags or ""
        node_data["inputs"]["lyrics"] = lyrics or ""
        for k, v in params.items():
            if k in ("tags", "lyrics"):
                continue
            node_data["inputs"][k] = v

    # Empty audio latent — its `seconds` must match the requested duration.
    for node_id, node_data in find_nodes_by_class(workflow, "EmptyAceStep1.5LatentAudio"):
        node_data["inputs"]["seconds"] = int(params.get("duration", model_cfg.get("default_duration", 120)))

    # Seed primitive (node 109), if present, kept in sync with the request.
    for node_id, node_data in find_nodes_by_class(workflow, "PrimitiveInt"):
        if node_data.get("class_type") == "PrimitiveInt":
            node_data["inputs"]["value"] = seed

    # Output prefix (scheme: amusic_<timestamp>).
    for node_id, node_data in find_nodes_by_class(workflow, "SaveAudioAdvanced"):
        node_data["inputs"]["filename_prefix"] = _save_prefix("amusic")

    workflow = apply_keep_resident(cfg, workflow)
    return workflow, seed

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def cmd_music(cfg: dict, args: argparse.Namespace) -> None:
    seed = args.seed
    override = {}
    for flag_name in ("bpm", "keyscale", "language", "timesignature", "cfg_scale",
                      "temperature", "top_p", "top_k", "min_p", "generate_audio_codes"):
        override[flag_name] = getattr(args, flag_name, None)

    if args.prompt:
        tags = args.prompt
    else:
        tags = args.tags
    if not tags:
        print("❌ A music description is required: pass --tags (or --prompt).", file=sys.stderr)
        sys.exit(1)

    model_cfg = get_music_cfg(cfg)
    output_dir = ensure_output_dir(cfg, "acestep15", args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    timeout = model_cfg.get("timeout_seconds", 600)

    try:
        workflow, seed_used = prepare_music_workflow(
            cfg, tags=tags, lyrics=args.lyrics,
            duration=args.duration, seed=args.seed,
            override=override,
        )
    except Exception as e:
        print(f"❌ Failed to prepare the workflow: {e}", file=sys.stderr)
        sys.exit(1)

    job_id, err_msg, errs = submit_workflow_with_errors(cfg, workflow, timeout, skip_autosubstitute=True)
    for w in errs:
        print(w)
    if job_id is None:
        print(f"❌ Music generation failed to queue: {err_msg}", file=sys.stderr)
        print("   AceStep 1.5 needs `acestep_v1.5_xl_turbo_bf16.safetensors`", file=sys.stderr)
        print("   plus `qwen_*_ace15.safetensors` (CLIP) and `ace_1.5_vae.safetensors`", file=sys.stderr)
        print("   in the server's ComfyUI model folders.", file=sys.stderr)
        sys.exit(1)

    try:
        history = wait_for_completion(cfg, job_id, timeout)
    except TimeoutError:
        print(f"❌ Music generation timed out after {timeout}s (prompt_id={job_id})", file=sys.stderr)
        sys.exit(1)
    status_str = history.get(job_id, {}).get("status", {}).get("status_str", "")
    if status_str == "error":
        node_msgs = history.get(job_id, {}).get("status", {}).get("messages", [])
        print(f"❌ Music generation error: {node_msgs}", file=sys.stderr)
        sys.exit(1)

    audios = get_output_audios(history, job_id, output_dir)
    if not audios:
        print("❌ No audio found in the output! (the SaveAudioAdvanced node may be missing "
              "or the endpoint stores audio under a different output key)", file=sys.stderr)
        sys.exit(1)

    b64s = [audio_b64_from_comfyui(cfg, a) for a in audios]
    local_paths = [save_b64_audio(b, a["filename"], output_dir) for b, a in zip(b64s, audios)]

    purge_remote(cfg, audios)

    print(f"✅ Music: {local_paths[0].name}")
    print(f"   Tags: {tags[:100]}")
    print(f"   File: {local_paths[0]}")
    print(f"   Seed: {seed_used}")
    print("   📤 DELIVER: to send to the user, put the channel's directive line in your reply — "
          f"e.g. `MEDIA: {local_paths[0]}` on its own line, or send it as a media attachment via the "
          "message tool (media=<path>). Never invent directive variants (e.g. /MIL).")

def cmd_test(cfg: dict, args: argparse.Namespace) -> None:
    url = cfg["comfyui_url"].rstrip("/") + "/history"
    try:
        req = urllib.request.Request(url, method="GET", headers=auth_headers(cfg))
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode()
        print(f"✅ ComfyUI is reachable at {cfg['comfyui_url']}")
        print(f"   Response: {data[:100]}")
    except Exception as e:
        _endpoint_setup_help(cfg, e)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="ComfyUI AceStep 1.5 music generation client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_music = subparsers.add_parser("music", help="Text-to-Music generation (AceStep Audio 1.5)")
    p_music.add_argument("--tags", default=None,
                         help='Music description / style tags (the main prompt). E.g. "Lo-fi hip hop, 80 BPM, chill". '
                              "You can also use --prompt as an alias.")
    p_music.add_argument("--prompt", default=None, help="Alias of --tags (the main prompt)")
    p_music.add_argument("--lyrics", default=None,
                         help="Sonic-lyrics (structured text, passed INLINE — this script never reads files; "
                              "a file path here would be sent to the model as the lyric text). "
                              "Omit for instrumental; if omitted, the agent should derive style + lyrics from the request.")
    p_music.add_argument("--duration", type=int, default=None,
                         help="Duration in seconds (default: config default_duration, 120)")
    p_music.add_argument("--seed", type=int, default=None)
    p_music.add_argument("--bpm", type=int, default=None,
                         help="Tempo in BPM (default: config default_params.bpm)")
    p_music.add_argument("--keyscale", default=None,
                         help='Musical key/scale (default: config default_params.keyscale, e.g. "E minor")')
    p_music.add_argument("--language", default=None,
                         help='Song language code (default: config default_params.language, e.g. "en")')
    p_music.add_argument("--timesignature", default=None,
                         help='Time signature (default: config default_params.timesignature, e.g. "4")')
    p_music.add_argument("--cfg-scale", type=float, default=None, dest="cfg_scale",
                         help='CFG scale (default: config default_params.cfg_scale)')
    p_music.add_argument("--temperature", type=float, default=None,
                         help='Sampling temperature (default: config default_params.temperature)')
    p_music.add_argument("--top-p", type=float, default=None, dest="top_p",
                         help="Top-p (default: config default_params.top_p)")
    p_music.add_argument("--top-k", type=int, default=None, dest="top_k",
                         help="Top-k (default: config default_params.top_k)")
    p_music.add_argument("--min-p", type=float, default=None, dest="min_p",
                         help="Min-p (default: config default_params.min_p)")
    p_music.add_argument("--generate-audio-codes", action="store_true",
                         help="Set generate_audio_codes=true on the text-encode node")
    p_music.add_argument("--output-dir", default=None)
    p_music.add_argument("--keep", action="store_true", help="保留服务端文件（默认取回后销毁）")

    subparsers.add_parser("test", help="Health check")

    args = parser.parse_args()

    # These attributes only exist on the `music` subparser — guard them so
    # other subcommands (e.g. `test`) parse and run cleanly.
    if args.command == "music":
        if args.generate_audio_codes:
            args.generate_audio_codes = True
        else:
            args.generate_audio_codes = None
        if getattr(args, "top_k", None) == 0:
            args.top_k = None
        if getattr(args, "min_p", None) == 0:
            args.min_p = None

    cfg = load_config()
    if getattr(args, "keep", False):
        cfg["purge_remote"] = False

    if args.command in ("music",):
        ensure_comfyui_reachable(cfg)

    if args.command == "music":
        cmd_music(cfg, args)
    elif args.command == "test":
        cmd_test(cfg, args)

if __name__ == "__main__":
    main()
