#!/usr/bin/env python3
"""
image_with_comfyui.py - Call local ComfyUI for T2I / I2I image generation.

Usage:
    python3 image_with_comfyui.py t2i --prompt "..." [--aspect 16:9] [--model z-image]
    python3 image_with_comfyui.py t2i --prompt "..." --model sd35
    python3 image_with_comfyui.py i2i --prompt "..." --image image.jpg
    python3 image_with_comfyui.py test                       # Quick health check

Configuration:
    Reads config from this SKILL's config.json (relative to this script).
    Environment variable COMFYUI_URL overrides comfyui_url in config.
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
import http.client
import mimetypes
from email.encoders import encode_base64
from io import BytesIO
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = SCRIPT_DIR / "config.json"

# Workspace directory detection
import os

def _find_workspace_dir() -> Path:
    """Find the OpenClaw workspace directory."""
    if ws := os.environ.get("OPENCLAW_WORKSPACE"):
        return Path(ws).resolve()
    p = SCRIPT_DIR
    for _ in range(10):
        p = p.parent
        candidate = p / ".openclaw" / "workspace"
        if candidate.is_dir():
            return candidate.resolve()
    return Path(os.getcwd()).resolve()

WORKSPACE_DIR = _find_workspace_dir()

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
    return cfg

# ---------------------------------------------------------------------------
# Helper: get model config from nested structure
# ---------------------------------------------------------------------------

def get_model_cfg(cfg: dict, model_id: str) -> dict:
    """Get config for a specific model by ID.
    
    model_id examples: 'z-image', 'sd35', 'qwen_imageedit', 'wan2.2_i2v'
    """
    # Search in image/t2i
    if "image" in cfg and "t2i" in cfg["image"]:
        if model_id in cfg["image"]["t2i"]:
            return cfg["image"]["t2i"][model_id]
    # Search in image/i2i
    if "image" in cfg and "i2i" in cfg["image"]:
        if model_id in cfg["image"]["i2i"]:
            return cfg["image"]["i2i"][model_id]
    # Search in video
    if "video" in cfg and model_id in cfg["video"]:
        return cfg["video"][model_id]
    raise KeyError(f"Model '{model_id}' not found in config")

def get_workflow_path(cfg: dict, model_id: str) -> str:
    return get_model_cfg(cfg, model_id)["workflow_path"]

def get_output_subdir(cfg: dict, model_id: str, default: str = "images") -> str:
    return get_model_cfg(cfg, model_id).get("output_subdir", default)

# ---------------------------------------------------------------------------
# Node package mapping — maps class_type → (package_name, github_url)
# Note: install_command is NOT executed by this script.
# Users must manually run git clone in their ComfyUI/custom_nodes directory.
# ComfyUI may be on a remote server not reachable from this agent.
# ---------------------------------------------------------------------------

NODE_PACKAGE_MAP: dict[str, tuple[str, str]] = {
    # Impact Pack (most common)
    "ImpactPack.IA2PlusPatch": ("ComfyUI-Impact-Pack", "https://github.com/ltdrdata/ComfyUI-Impact-Pack"),
    "ImpactKSamplerBasicPipe": ("ComfyUI-Impact-Pack", "https://github.com/ltdrdata/ComfyUI-Impact-Pack"),
    "ImpactKSamplerAdvancedBasicPipe": ("ComfyUI-Impact-Pack", "https://github.com/ltdrdata/ComfyUI-Impact-Pack"),
    "ImpactSimpleDetectorSEGS": ("ComfyUI-Impact-Pack", "https://github.com/ltdrdata/ComfyUI-Impact-Pack"),
    "ImpactSegsAndMask": ("ComfyUI-Impact-Pack", "https://github.com/ltdrdata/ComfyUI-Impact-Pack"),
    "ImpactSAM2VideoDetectorSEGS": ("ComfyUI-Impact-Pack", "https://github.com/ltdrdata/ComfyUI-Impact-Pack"),
    "BasicPipeToDetailerPipe": ("ComfyUI-Impact-Pack", "https://github.com/ltdrdata/ComfyUI-Impact-Pack"),
    "SAMLoader": ("ComfyUI-Impact-Pack", "https://github.com/ltdrdata/ComfyUI-Impact-Pack"),
    "ImpactIPAdapterApplySEGS": ("ComfyUI-Impact-Pack", "https://github.com/ltdrdata/ComfyUI-Impact-Pack"),
    "ImpactControlNetApplySEGS": ("ComfyUI-Impact-Pack", "https://github.com/ltdrdata/ComfyUI-Impact-Pack"),
    "UltralyticsDetectorProvider": ("ComfyUI-Impact-Subpack", "https://github.com/ltdrdata/ComfyUI-Impact-Pack"),
    "ImpactWildcardEncode": ("ComfyUI-Impact-Pack", "https://github.com/ltdrdata/ComfyUI-Impact-Pack"),
    "ImpactWildcardProcessor": ("ComfyUI-Impact-Pack", "https://github.com/ltdrdata/ComfyUI-Impact-Pack"),

    # Video Helper Suite
    "VHS_VideoCombine": ("ComfyUI-VideoHelperSuite", "https://github.com/Fannovel16/ComfyUI-VideoHelperSuite"),
    "VHS_LoadVideo": ("ComfyUI-VideoHelperSuite", "https://github.com/Fannovel16/ComfyUI-VideoHelperSuite"),
    "VHS_LoadVideoPath": ("ComfyUI-VideoHelperSuite", "https://github.com/Fannovel16/ComfyUI-VideoHelperSuite"),
    "VHS_LoadVideoFFmpeg": ("ComfyUI-VideoHelperSuite", "https://github.com/Fannovel16/ComfyUI-VideoHelperSuite"),

    # Frame Interpolation (RIFE)
    "RIFE VFI": ("ComfyUI-Frame-Interpolation", "https://github.com/Fannovel16/ComfyUI-Frame-Interpolation"),
    "RIFE_VFI_Opt": ("ComfyUI-Frame-Interpolation", "https://github.com/Fannovel16/ComfyUI-Frame-Interpolation"),
    "RIFE_VFI_Advanced": ("ComfyUI-Frame-Interpolation", "https://github.com/Fannovel16/ComfyUI-Frame-Interpolation"),
    "AMT VFI": ("ComfyUI-Frame-Interpolation", "https://github.com/Fannovel16/ComfyUI-Frame-Interpolation"),
    "IFRNet VFI": ("ComfyUI-Frame-Interpolation", "https://github.com/Fannovel16/ComfyUI-Frame-Interpolation"),
    "FILM VFI": ("ComfyUI-Frame-Interpolation", "https://github.com/Fannovel16/ComfyUI-Frame-Interpolation"),
    "GMFSS Fortuna VFI": ("ComfyUI-Frame-Interpolation", "https://github.com/Fannovel16/ComfyUI-Frame-Interpolation"),

    # WAS Node Suite
    "BLIP Analyze Image": ("WASms_Node_Suite_For_ComfyUI", "https://github.com/WASasquatch/was-node-suite-comfyui"),
    "BLIP Model Loader": ("WASms_Node_Suite_For_ComfyUI", "https://github.com/WASasquatch/was-node-suite-comfyui"),
    "Blend Latents": ("WASms_Node_Suite_For_ComfyUI", "https://github.com/WASasquatch/was-node-suite-comfyui"),

    # rgthree
    "Any Switch (rgthree)": ("rgthree-comfy", "https://github.com/rgthree/rgthree-comfy"),
    "Context (rgthree)": ("rgthree-comfy", "https://github.com/rgthree/rgthree-comfy"),
    "Image Comparer (rgthree)": ("rgthree-comfy", "https://github.com/rgthree/rgthree-comfy"),

    # mtb
    "Add To Playlist (mtb)": ("comfy-mtb", "https://github.com/melMass/comfy_mtb"),

    # easy-use
    "dynamicThresholdingFull": ("ComfyUI-easy-use", "https://github.com/easymatic/ComfyUI-easy-use"),

    # kjnodes
    "AppendInstanceDiffusionTracking": ("comfyui-kjnodes", "https://github.com/kijai/ComfyUI-KJNodes"),
    "ImageResizeKJ": ("comfyui-kjnodes", "https://github.com/kijai/ComfyUI-KJNodes"),
    "ApplyRifleXRoPE_WanVideo": ("comfyui-kjnodes", "https://github.com/kijai/ComfyUI-KJNodes"),

    # Crystools
    "Get resolution [Crystools]": ("ComfyUI-Crystools", "https://github.com/crystian/ComfyUI-Crystools"),

    # GGUF
    "CLIPLoaderGGUF": ("ComfyUI-GGUF", "https://github.com/city96/ComfyUI-GGUF"),
    "UnetLoaderGGUF": ("ComfyUI-GGUF", "https://github.com/city96/ComfyUI-GGUF"),

    # wanvideo custom nodes
    "WanImageToVideo": ("wanvideo-comfyui", "https://github.com/kijai/ComfyUI-WanVideoWrapper"),
    "WanMoeKamplerAdvanced": ("wanvideo-comfyui", "https://github.com/kijai/ComfyUI-WanVideoWrapper"),

    # ControlNet
    "ControlNetLoader": ("ComfyUI-ControlNet-Live2D", "https://github.com/coqui-ai/ComfyUI-ControlNet-Live2D"),
    "ControlNetApply": ("ComfyUI-ControlNet", "https://github.com/comfyanonymous/ComfyUI_controlnet_aux"),
    "ControlNetApplyAdvanced": ("ComfyUI-ControlNet", "https://github.com/comfyanonymous/ComfyUI_controlnet_aux"),
}

# ---------------------------------------------------------------------------
# ComfyUI API helpers
# ---------------------------------------------------------------------------

def api_url(cfg: dict, path: str) -> str:
    base = cfg["comfyui_url"].rstrip("/")
    return f"{base}{path}"

def fetch_object_info(cfg: dict) -> dict:
    """Fetch ComfyUI /object_info to get available node types and models."""
    req = urllib.request.Request(api_url(cfg, "/object_info"), method="GET")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())

def find_node_package(class_type: str) -> tuple[str, str, str] | None:
    """Look up a node class in the package map. Supports partial matching."""
    if class_type in NODE_PACKAGE_MAP:
        return NODE_PACKAGE_MAP[class_type]
    # Try partial match: normalize and search
    ct_lower = class_type.lower().replace(" ", "").replace("_", "")
    for known, info in NODE_PACKAGE_MAP.items():
        known_norm = known.lower().replace(" ", "").replace("_", "")
        if known_norm in ct_lower or ct_lower in known_norm:
            return info
    return None

def get_available_models(obj_info: dict) -> dict:
    """Extract model file lists from object_info.
    
    Returns dict: {loader_type: {param_name: [model_names]}}
    """
    models = {}
    for node_name, node_info in obj_info.items():
        inp = node_info.get("input", {})
        for param, spec in {**inp.get("required", {}), **inp.get("optional", {})}.items():
            if isinstance(spec, list) and len(spec) > 0 and isinstance(spec[0], list):
                if node_name not in models:
                    models[node_name] = {}
                models[node_name][param] = spec[0]
    return models

def find_model_substitute(requested_model: str, available_models: dict) -> tuple[str, str, str] | None:
    """Find a substitute model for a missing model.
    
    Returns (loader_node, param, substitute_model) or None.
    
    Substitution rules:
    - sd3.5_medium → sd3.5_large
    - WAN2.2 High → WAN2.2 Low (or vice versa)
    - Any exact match in available models
    """
    base_name = requested_model.replace(".safetensors", "")
    
    # Filter: only keep string values (ComfyUI API includes non-string validation values)
    str_lists = {}
    for loader, params in available_models.items():
        str_lists[loader] = {
            k: [v for v in vs if isinstance(v, str)]
            for k, vs in params.items()
            if any(isinstance(x, str) for x in vs)
        }
    
    # Rule 1: sd3.5_medium → sd3.5_large
    if "sd3.5_medium" in base_name or "sd3_medium" in base_name:
        for loader, params in str_lists.items():
            for param, model_list in params.items():
                for m in model_list:
                    if "sd3.5_large" in m or "sd3_large" in m:
                        return (loader, param, m)
                    if "sd3_medium" in m and requested_model != m:
                        return (loader, param, m)
    
    # Rule 2: WAN2.2 High/Low substitution
    if "wan" in base_name.lower() or "WAN" in base_name:
        for loader, params in str_lists.items():
            for param, model_list in params.items():
                has_high = any("High" in m or "high" in m for m in model_list)
                has_low = any("Low" in m or "low" in m for m in model_list)
                if has_high and has_low:
                    if "High" in base_name or "high" in base_name:
                        for m in model_list:
                            if "Low" in m or "low" in m:
                                return (loader, param, m)
                    elif "Low" in base_name or "low" in base_name:
                        for m in model_list:
                            if "High" in m or "high" in m:
                                return (loader, param, m)
                    else:
                        for m in model_list:
                            if "High" in m or "high" in m:
                                return (loader, param, m)
    
    # Rule 3: Any exact match
    for loader, params in str_lists.items():
        for param, model_list in params.items():
            if requested_model in model_list:
                return (loader, param, requested_model)
    
    # Rule 4: Fuzzy match - find any model with similar base name
    for loader, params in str_lists.items():
        for param, model_list in params.items():
            for m in model_list:
                m_base = m.replace(".safetensors", "")
                shared_parts = set(base_name.split("_")) & set(m_base.split("_"))
                if len(shared_parts) >= 2 and m != requested_model:
                    return (loader, param, m)
    
    return None

def update_workflow_model(workflow: dict, loader_node: str, param: str, substitute_model: str) -> dict:
    """Create a modified workflow copy with the substitute model."""
    import copy
    modified = copy.deepcopy(workflow)
    for node_id, node_data in modified.items():
        ct = node_data.get("class_type", "")
        # Find the loader node by class_type
        if ct == loader_node:
            if param in node_data.get("inputs", {}):
                modified[node_id]["inputs"][param] = substitute_model
    return modified


def bypass_node(workflow: dict, missing_node_id: str) -> dict:
    """Create a bypass workflow: remove missing_node_id and redirect upstream → downstream.

    Usage: when ComfyUI reports a missing node but it's a utility/bridging node
    like UnloadAllModels, we can safely skip it by rerouting the signal path.
    """
    import copy
    modified = copy.deepcopy(workflow)
    missing_id = str(missing_node_id)

    # 1. Collect downstream connections — who receives FROM this node
    downstream: dict[str, list[tuple[str, str]]] = {}  # {downstream_node_id: [(upstream_param, port)]}
    for nid, nd in modified.items():
        for k, v in nd.get("inputs", {}).items():
            if isinstance(v, list) and len(v) >= 2 and v[0] == missing_id:
                downstream.setdefault(nid, []).append((k, str(v[1])))

    if not downstream:
        # No downstream — just remove the node, nothing to redirect to
        modified.pop(missing_id, None)
        return modified

    # 2. Find the upstream source — what feeds INTO this node
    # The missing node's own inputs reference its upstream, e.g. {'value': ['43', 0]}
    # means node 43 is the upstream source.
    upstream_nids: list[str] = []
    missing_node = modified.get(missing_id, {})
    for k, v in missing_node.get("inputs", {}).items():
        if isinstance(v, list) and len(v) >= 2:
            src_nid = str(v[0])
            if src_nid != missing_id:  # avoid self-reference
                upstream_nids.append(src_nid)

    if not upstream_nids:
        # No upstream — orphan node, just remove it
        modified.pop(missing_id, None)
        return modified

    up_nid = str(upstream_nids[0])
    up_port = 0

    # 3. Collect connections to update, then apply (avoid mutation during iteration)
    updates: list[tuple[str, str, list]] = []
    for down_nid, connections in downstream.items():
        for param, port in connections:
            if down_nid in modified and param in modified[down_nid].get("inputs", {}):
                updates.append((down_nid, param, [up_nid, up_port]))

    for dn, p, val in updates:
        modified[dn]["inputs"][p] = val

    # 5. Remove the missing node
    modified.pop(missing_id, None)
    return modified

def send_prompt(cfg: dict, workflow: dict, timeout: int = 30) -> str:
    """Send workflow to ComfyUI with error handling for missing nodes and models."""
    data = json.dumps({"prompt": workflow}).encode("utf-8")
    req = urllib.request.Request(
        api_url(cfg, "/prompt"),
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        result = json.loads(resp.read().decode())
    return result.get("prompt_id", result.get("error", "unknown"))

def send_prompt_with_errors(cfg: dict, workflow: dict, timeout: int = 30, retry_count: int = 0, max_retries: int = 1) -> tuple[str | None, str | None, list[str]]:
    """Send workflow to ComfyUI with automatic error handling.
    
    Returns: (prompt_id_or_None, error_message_or_None, warning_messages)
    """
    warnings = []
    
    # Send prompt and capture raw result
    data = json.dumps({"prompt": workflow}).encode("utf-8")
    req = urllib.request.Request(
        api_url(cfg, "/prompt"),
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        result = json.loads(e.read().decode())
    
    # Check for missing node type error
    error_type = result.get("error", {}).get("type", "")
    if error_type == "missing_node_type":
        class_type = result.get("error", {}).get("extra_info", {}).get("class_type", "Unknown")
        node_id = result.get("error", {}).get("extra_info", {}).get("node_id", "")

        # UnloadAllModels: bypass it (utility node, not needed for generation)
        if class_type == "UnloadAllModels":
            warnings.append(
                f"⚠️ Workflow missing node: `UnloadAllModels` (memory cleanup, non-critical)\n"
                f"🔄 Auto-bypassed — generation continues"
            )
            bypassed = bypass_node(workflow, node_id)
            b_pid, b_err, b_warns = send_prompt_with_errors(cfg, bypassed, timeout, retry_count + 1, max_retries)
            return b_pid, b_err, warnings + b_warns

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
    
    # Check for model validation errors
    node_errors = result.get("node_errors", {})
    for node_id, node_err in node_errors.items():
        err_details = node_err.get("errors", [{}])[0] if node_err.get("errors") else {}
        err_type = err_details.get("type", "")
        if err_type == "value_not_in_list":
            # Find the requested model from the node's current inputs
            requested = None
            loader_node = None
            param_name = None
            for nid, nd in workflow.items():
                if str(nid) == str(node_id) and nd.get("class_type", "") in ["CheckpointLoaderSimple", "UNETLoader", "CLIPLoader"]:
                    for param, val in nd.get("inputs", {}).items():
                        if isinstance(val, str) and val.endswith(".safetensors"):
                            requested = val
                            param_name = param
                            loader_node = nd.get("class_type", "")
            
            if requested and loader_node:
                obj_info = fetch_object_info(cfg)
                available = get_available_models(obj_info)
                sub = find_model_substitute(requested, available)
                if sub:
                    sub_loader, sub_param, substitute_model = sub
                    warnings.append(
                        f"⚠️ Model missing: `{requested}`\n"
                        f"🔄 Substituted: `{substitute_model}`\n"
                        f"📦 Loader: {sub_loader}.{sub_param}"
                    )
                    new_workflow = update_workflow_model(workflow, loader_node, param_name, substitute_model)
                    sub_pid, sub_err, sub_warns = send_prompt_with_errors(cfg, new_workflow, timeout, retry_count + 1, max_retries)
                    return sub_pid, sub_err, warnings + sub_warns
    
    prompt_id = result.get("prompt_id")
    error_msg = result.get("error", {}).get("message", "") if "error" in result else ""
    return prompt_id, error_msg if error_msg else None, warnings

def wait_for_completion(cfg: dict, prompt_id: str, timeout: int = 120) -> dict:
    start = time.time()
    poll_interval = cfg.get("poll_interval_seconds", 3)
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(
                api_url(cfg, f"/history/{prompt_id}"),
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                history = json.loads(resp.read().decode())
        except urllib.error.URLError:
            time.sleep(poll_interval)
            continue
        status = history.get(prompt_id, {}).get("status", {})
        status_str = status.get("status_str", "")
        if status_str == "error":
            # ComfyUI reported an error — return immediately so caller
            # can inspect the error messages instead of waiting for timeout.
            return history
        if status.get("completed"):
            return history
        time.sleep(poll_interval)
    raise TimeoutError(f"Generation timed out after {timeout}s (prompt_id={prompt_id})")

def sanitize_filename(filename: str, output_dir: Path) -> str | None:
    """Sanitize a filename from a remote ComfyUI server.

    Prevents path traversal attacks (e.g. `../../../etc/passwd`) by:
    1. Stripping all directory components — only the bare basename is kept
    2. Rejecting empty names, `..`, `.`, or names containing path separators
    3. Verifying the final resolved path stays within output_dir

    Returns the sanitized filename, or None if the filename is unsafe.
    """
    if not filename or not isinstance(filename, str):
        print(f"⚠️ sanitize_filename: empty or non-string filename", file=sys.stderr)
        return None

    # Strip all directory components — only keep the bare filename
    basename = Path(filename).name

    # Reject empty, dot, or dot-dot
    if not basename or basename in (".", ".."):
        print(f"⚠️ sanitize_filename: rejected suspicious name ({basename!r} from {filename!r})", file=sys.stderr)
        return None

    # Reject names with embedded path separators (cross-platform)
    if "/" in basename or "\\" in basename:
        print(f"⚠️ sanitize_filename: path separator in filename ({filename!r})", file=sys.stderr)
        return None

    # Reconstruct candidate path and verify it stays within output_dir
    candidate = (output_dir / basename).resolve()
    if not str(candidate).startswith(str(output_dir.resolve())):
        print(f"⚠️ sanitize_filename: path traversal detected ({filename!r} resolves outside output_dir)", file=sys.stderr)
        return None

    return basename


def get_output_images(history: dict, prompt_id: str, output_dir: Path = None) -> list[dict]:
    """Extract only the final output images from a single prompt_id result.
    Filters out type='temp' intermediate images and sanitizes filenames
    to prevent path traversal from a potentially compromised ComfyUI server.
    """
    images = []
    for node_id, node_result in history.get(prompt_id, {}).get("outputs", {}).items():
        for img in node_result.get("images", []):
            # Only include final output images, skip temp/intermediate
            if img.get("type") == "output":
                safe_name = sanitize_filename(img.get("filename", ""), output_dir)
                if safe_name is None:
                    print(f"⚠️ Skipping unsafe image filename from ComfyUI", file=sys.stderr)
                    continue
                images.append({
                    "filename": safe_name,
                    "subfolder": img.get("subfolder", ""),
                    "type": img.get("type", "output"),
                })
    return images

def image_b64_from_comfyui(cfg: dict, img: dict) -> str:
    params = urllib.parse.urlencode({
        "filename": img["filename"],
        "subfolder": img.get("subfolder", ""),
        "type": img.get("type", "output"),
    })
    req = urllib.request.Request(
        f"{api_url(cfg, '/view')}?{params}",
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=cfg.get("timeout_seconds", 30)) as resp:
        return base64.b64encode(resp.read()).decode("utf-8")

# ---------------------------------------------------------------------------
# Workflow manipulation
# ---------------------------------------------------------------------------

ASPECT_RATIOS = {
    "1:1": (1024, 1024),
    "4:3": (1280, 960),
    "3:4": (960, 1280),
    "16:9": (1280, 720),
    "9:16": (720, 1280),
    "3:2": (1536, 1024),
    "2:3": (1024, 1536),
}

# WAN2.2 I2V resolution reference (fast_ok, user_fav, native)
WAN2_2_RES = {
    "3:4": [(560, 720), (720, 912), (848, 1088)],
    "2:3": [(528, 768), (656, 960), (784, 1136)],
    "9:16": [(480, 848), (608, 1072), (720, 1264)],
    "16:9": [(896, 512), (1264, 720), (1072, 608)],
    "1:1": [(560, 560), (704, 704), (832, 832)],
    "4:3": [(720, 560), (864, 672), (1024, 768)],
    "3:2": [(768, 528), (960, 656), (1136, 784)],
}

WAN2_2_ADDITIONAL = {
    "3:4": [(416, 544), (672, 864), (784, 1008)],
    "2:3": [(384, 576), (624, 912), (736, 1072)],
    "9:16": [(368, 624), (576, 1008), (672, 1184)],
    "16:9": [(416, 240), (640, 368), (1008, 576)],
    "1:1": [(480, 480), (624, 624), (736, 736)],
    "4:3": [(576, 416), (848, 608), (1008, 736)],
    "3:2": [(512, 352), (768, 512), (1184, 768)],
}

def find_closest_wan2_2_resolution(iw: int, ih: int) -> tuple[int, int]:
    """Given input image dimensions, find the closest matching Wan2.2 resolution.
    
    Collects all resolutions from WAN2_2_RES and WAN2_2_ADDITIONAL,
    computes aspect ratio, and picks the one with smallest difference.
    """
    target_ar = iw / ih
    best_diff = float("inf")
    best_resolution = None
    
    all_resolutions = []
    for category, res_list in WAN2_2_RES.items():
        for w, h in res_list:
            all_resolutions.append((w, h))
    for category, res_list in WAN2_2_ADDITIONAL.items():
        for w, h in res_list:
            all_resolutions.append((w, h))
    
    for w, h in all_resolutions:
        ar = w / h
        diff = abs(ar - target_ar)
        if diff < best_diff:
            best_diff = diff
            best_resolution = (w, h)
    
    return best_resolution

def find_nodes_by_class(workflow: dict, class_type: str) -> list[dict]:
    results = []
    for node_id, node_data in workflow.items():
        if node_data.get("class_type") == class_type:
            results.append((node_id, node_data))
    return results

def resolve_skill_path(p: str) -> str:
    p = str(Path(p).expanduser())
    if not Path(p).is_absolute():
        p = str(SCRIPT_DIR / p)
    return p

def resolve_workspace_path(p: str) -> str:
    p = str(Path(p).expanduser())
    if not Path(p).is_absolute():
        p = str(WORKSPACE_DIR / p)
    return p

def prepare_t2i_workflow(cfg: dict, prompt: str, aspect: str = "16:9",
                         seed: int = None, steps: int = None,
                         model_type: str = "z-image") -> tuple[dict, str, int]:
    """Prepare T2I workflow from config, return (workflow, prompt_type, seed)."""
    if model_type == "sd35":
        return prepare_sd35_workflow(cfg, prompt, aspect, seed, steps)
    
    model_cfg = get_model_cfg(cfg, "z-image")
    workflow_path = resolve_skill_path(model_cfg["workflow_path"])
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)
    
    # Fill prompt node
    found = False
    for node_id, node_data in workflow.items():
        ct = node_data.get("class_type", "")
        if ct in ("CLIPTextEncode", "TextMultiline") and "text" in node_data.get("inputs", {}):
            workflow[node_id]["inputs"]["text"] = prompt
            found = True
            break
    if not found:
        raise ValueError("T2I: Could not find a prompt node with 'text' input")
    
    # Set dimensions
    if aspect in ASPECT_RATIOS:
        w, h = ASPECT_RATIOS[aspect]
        for node_id, node_data in find_nodes_by_class(workflow, "EmptySD3LatentImage"):
            workflow[node_id]["inputs"]["width"] = w
            workflow[node_id]["inputs"]["height"] = h
    
    if seed is None:
        import random
        seed = random.randint(0, 2**63 - 1)
    
    # Override KSampler
    ks_nodes = find_nodes_by_class(workflow, "KSampler")
    if ks_nodes:
        node_id, _ = ks_nodes[0]
        workflow[node_id]["inputs"]["seed"] = seed
        if steps is not None:
            workflow[node_id]["inputs"]["steps"] = steps
    
    return workflow, "Z-Image T2I", seed

def prepare_sd35_workflow(cfg: dict, prompt: str, aspect: str = "1:1",
                          seed: int = None, steps: int = None,
                          cfg_cfg: float = None, negative: str = "") -> tuple[dict, str, int]:
    model_cfg = get_model_cfg(cfg, "sd35")
    workflow_path = resolve_skill_path(model_cfg["workflow_path"])
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)
    
    default_w = model_cfg.get("default_width", 1024)
    default_h = model_cfg.get("default_height", 1024)
    default_steps = model_cfg.get("default_steps", 20)
    default_cfg = model_cfg.get("default_cfg", 4.01)
    
    if seed is None:
        import random
        seed = random.randint(0, 2**63 - 1)
    
    if aspect in ASPECT_RATIOS:
        w, h = ASPECT_RATIOS[aspect]
    else:
        w, h = default_w, default_h
    
    for node_id, _ in find_nodes_by_class(workflow, "EmptySD3LatentImage"):
        workflow[node_id]["inputs"]["width"] = w
        workflow[node_id]["inputs"]["height"] = h
    
    # Fill prompts
    pos_found = False
    for node_id, node_data in workflow.items():
        ct = node_data.get("class_type", "")
        if ct == "CLIPTextEncode" and "text" in node_data.get("inputs", {}):
            if not pos_found:
                workflow[node_id]["inputs"]["text"] = prompt
                pos_found = True
            else:
                workflow[node_id]["inputs"]["text"] = negative if negative else ""
    
    ks_nodes = find_nodes_by_class(workflow, "KSampler")
    if ks_nodes:
        node_id, _ = ks_nodes[0]
        workflow[node_id]["inputs"]["seed"] = seed
        if steps is not None:
            workflow[node_id]["inputs"]["steps"] = steps
        if cfg_cfg is not None:
            workflow[node_id]["inputs"]["cfg"] = cfg_cfg
    
    return workflow, "SD3.5 Medium T2I", seed

def _build_multipart_body(parts: list[tuple[str, str]], files: list[tuple[str, str, str]]) -> tuple[bytes, str]:
    import uuid
    boundary = str(uuid.uuid4())
    body = BytesIO()
    for name, value in parts:
        body.write(f"--{boundary}\r\n".encode())
        body.write(f"Content-Disposition: form-data; name=\"{name}\"\r\n\r\n".encode())
        body.write(f"{value}\r\n".encode())
    for file_name, filepath, content_type in files:
        body.write(f"--{boundary}\r\n".encode())
        body.write(f"Content-Disposition: form-data; name=\"image\"; filename=\"{file_name}\"\r\n".encode())
        body.write(f"Content-Type: {content_type}\r\n\r\n".encode())
        with open(filepath, "rb") as f:
            body.write(f.read())
        body.write(b"\r\n")
    body.write(f"--{boundary}--\r\n".encode())
    return body.getvalue(), boundary

def upload_image_to_comfyui(cfg: dict, local_path: str, filename: str = None) -> str:
    if filename is None:
        filename = Path(local_path).name
    body, boundary = _build_multipart_body(
        [("subfolder", ""), ("type", "input")],
        [(filename, local_path, "image/jpeg")]
    )
    req = urllib.request.Request(
        api_url(cfg, "/upload/image"),
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=cfg.get("timeout_seconds", 30)) as resp:
        result = json.loads(resp.read().decode())
    return result.get("name", filename)

def prepare_i2i_workflow(cfg: dict, prompt: str, image_path: str,
                         seed: int = None, steps: int = None) -> tuple[dict, str, str, int]:
    model_cfg = get_model_cfg(cfg, "qwen_imageedit")
    workflow_path = resolve_skill_path(model_cfg["workflow_path"])
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)
    
    uploaded_filename = upload_image_to_comfyui(cfg, image_path)
    
    for node_id, node_data in find_nodes_by_class(workflow, "LoadImage"):
        workflow[node_id]["inputs"]["image"] = uploaded_filename
    
    prompt_nodes = find_nodes_by_class(workflow, "TextEncodeQwenImageEditPlus")
    if prompt_nodes:
        # Find positive prompt node (has a non-empty default prompt)
        positive_node = None
        for node_id, node_data in prompt_nodes:
            default_prompt = node_data.get("inputs", {}).get("prompt", "")
            if default_prompt and default_prompt != "":
                positive_node = (node_id, node_data)
                break
        # Fallback to first node if no positive node found
        if positive_node is None:
            positive_node = prompt_nodes[0]
        node_id, _ = positive_node
        workflow[node_id]["inputs"]["prompt"] = prompt
    
    ks_nodes = find_nodes_by_class(workflow, "KSampler")
    if ks_nodes:
        node_id, _ = ks_nodes[0]
        if seed is None:
            import random
            seed = random.randint(0, 2**63 - 1)
        workflow[node_id]["inputs"]["seed"] = seed
        if steps is not None:
            workflow[node_id]["inputs"]["steps"] = steps
    
    return workflow, "Qwen Image Edit", uploaded_filename, seed

# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def ensure_output_dir(cfg: dict, model_id: str = None, cmd_output_dir: str = None) -> Path:
    """Get output directory: output_dir + output_subdir.
    
    Output path = resolve_workspace(output_dir) / output_subdir
    
    Args:
        cfg: config dict
        model_id: model identifier (e.g. 'z-image', 'sd35', 'qwen_imageedit', 'wan2.2_i2v')
        cmd_output_dir: override from --output-dir CLI arg (absolute path)
    """
    # CLI override takes highest priority
    if cmd_output_dir:
        return Path(resolve_workspace_path(cmd_output_dir))
    
    # Base output_dir from config
    base = Path(resolve_workspace_path(cfg.get("output_dir", "media/comfyui")))
    
    # Append model-specific output_subdir
    if model_id:
        output_subdir = get_output_subdir(cfg, model_id)
        return base / output_subdir
    
    return base

def save_b64_image(b64_data: str, filename: str, output_dir: Path) -> Path:
    safe_name = sanitize_filename(filename, output_dir)
    if safe_name is None:
        safe_name = f"image_{int(time.time())}.png"  # fallback name
    output_path = output_dir / safe_name
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(b64_data))
    return output_path

def print_result(prompt_type: str, prompt: str, images: list[dict],
                 local_paths: list[Path], output_dir: Path, cfg: dict = None):
    for i, img, path in zip(range(1, len(local_paths)+1), images, local_paths):
        sz = path.stat().st_size / 1024
        print(f"✅ Image {i}: {path.name} ({sz:.0f} KB)")
        print(f"   Prompt: {prompt[:80]}")
        print(f"   File: {path}")

# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def get_output_videos(history: dict, prompt_id: str, wan_cfg: dict = None, output_dir: Path = None) -> list:
    result = history.get(prompt_id, {}).get("outputs", {})
    videos = []
    for node_id, node_output in result.items():
        for key, value in node_output.items():
            if isinstance(value, list):
                for item in value:
                    if key in ("gifs", "video") or (isinstance(item, dict) and item.get("type") == "video"):
                        if wan_cfg and wan_cfg.get("keep_interpolated_only"):
                            frame_rate = item.get("frame_rate", 0)
                            filename = item.get("filename", "")
                            safe_name = sanitize_filename(filename, output_dir)
                            if frame_rate == 32 or (safe_name and "_00002_" in safe_name):
                                videos.append(item)
                        else:
                            safe_name = sanitize_filename(item.get("filename", ""), output_dir)
                            if safe_name is None:
                                print(f"⚠️ Skipping unsafe video filename from ComfyUI", file=sys.stderr)
                                continue
                            videos.append(item)
    return videos

def video_b64_from_comfyui(cfg: dict, video_item: dict) -> str:
    filename = video_item.get("filename", "")
    subfolder = video_item.get("subfolder", "")
    v_type = video_item.get("type", "output")
    url = f'{cfg["comfyui_url"].rstrip("/")}/view?filename={urllib.parse.quote(filename)}&subfolder={urllib.parse.quote(subfolder)}&type={urllib.parse.quote(v_type)}'
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
        return base64.b64encode(data).decode("utf-8")
    except urllib.error.URLError as e:
        print(f"   ❌ Failed to download video: {e}", file=sys.stderr)
        return ""

def save_b64_video(b64_data: str, filename: str, output_dir: Path) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_name = sanitize_filename(filename, output_dir)
    if safe_name is None:
        safe_name = f"video_{int(time.time())}.mp4"  # fallback name
    output_path = output_dir / safe_name
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(b64_data))
    return str(output_path)

def print_result_video(prompt_type: str, prompt: str, video_items: list,
                       local_paths: list, output_dir: Path, cfg: dict) -> None:
    for i, v, p in zip(range(1, len(local_paths)+1), video_items, local_paths):
        p = Path(p) if isinstance(p, str) else p
        sz = p.stat().st_size / 1024
        print(f"✅ Video {i}: {p.name} ({sz:.0f} KB)")
        print(f"   Prompt: {prompt[:80]}")
        print(f"   File: {p}")

def cmd_t2i(cfg: dict, args: argparse.Namespace) -> None:
    prompt = args.prompt
    aspect = args.aspect
    seed = args.seed
    steps = args.steps
    model_type = args.model or "z-image"
    
    # Determine model config and defaults
    if model_type == "sd35":
        model_cfg = get_model_cfg(cfg, "sd35")
        default_steps = model_cfg.get("default_steps", 20)
        default_cfg = model_cfg.get("default_cfg", 4.01)
        cfg_val = args.cfg if args.cfg is not None else default_cfg
        negative = getattr(args, 'negative', '') or ''
        print_type = "SD3.5"
    else:
        model_cfg = get_model_cfg(cfg, "z-image")
        default_steps = model_cfg.get("default_steps", 9)
        cfg_val = None
        negative = ""
        print_type = "T2I"
    
    if steps is None:
        steps = default_steps
    if seed is None:
        import random
        seed = random.randint(0, 2**63 - 1)
    
    output_dir = ensure_output_dir(cfg, model_type, args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    timeout = model_cfg.get("timeout_seconds", 100)
    
    if model_type == "sd35":
        workflow, prompt_type_str, seed_used = prepare_sd35_workflow(cfg, prompt, aspect, seed, steps, cfg_val, negative)
    else:
        workflow, prompt_type_str, seed_used = prepare_t2i_workflow(cfg, prompt, aspect, seed, steps, model_type)
    
    prompt_id, err_msg, errs = send_prompt_with_errors(cfg, workflow, timeout)
    if prompt_id is None:
        for w in errs:
            print(w)
        sys.exit(1)
    
    history = wait_for_completion(cfg, prompt_id, timeout)
    images = get_output_images(history, prompt_id, output_dir)
    if not images:
        print("❌ No images found in output!")
        sys.exit(1)
    
    b64_images = [image_b64_from_comfyui(cfg, img) for img in images]
    local_paths = [save_b64_image(b64, img["filename"], output_dir)
                   for b64, img in zip(b64_images, images)]
    print_result(prompt_type_str, prompt, images, local_paths, output_dir, cfg)

def cmd_i2i(cfg: dict, args: argparse.Namespace) -> None:
    prompt = args.prompt
    image_path = Path(args.image).expanduser()
    if not image_path.exists():
        print(f"❌ Image not found: {image_path}", file=sys.stderr)
        sys.exit(1)
    
    model_cfg = get_model_cfg(cfg, "qwen_imageedit")
    seed = args.seed
    steps = args.steps
    output_dir = ensure_output_dir(cfg, "qwen_imageedit", args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    workflow, prompt_type_str, uploaded_fn, seed_used = prepare_i2i_workflow(cfg, prompt, str(image_path), seed, steps)
    timeout = model_cfg.get("timeout_seconds", 600)
    prompt_id, err_msg, errs = send_prompt_with_errors(cfg, workflow, timeout)
    if prompt_id is None:
        for w in errs:
            print(w)
        sys.exit(1)
    
    history = wait_for_completion(cfg, prompt_id, timeout)
    images = get_output_images(history, prompt_id, output_dir)
    if not images:
        print("❌ No images found in output!", file=sys.stderr)
        sys.exit(1)
    
    b64_images = [image_b64_from_comfyui(cfg, img) for img in images]
    local_paths = [save_b64_image(b64, img["filename"], output_dir)
                   for b64, img in zip(b64_images, images)]
    print_result(prompt_type_str, prompt, images, local_paths, output_dir)

def cmd_test(cfg: dict, args: argparse.Namespace) -> None:
    url = cfg["comfyui_url"].rstrip("/") + "/history"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode()
        print(f"✅ ComfyUI is reachable at {cfg['comfyui_url']}")
        print(f"   Response: {data[:100]}")
    except urllib.error.URLError as e:
        print(f"❌ ComfyUI unreachable at {cfg['comfyui_url']}: {e}")
        sys.exit(1)

def prepare_wan2_2_i2v_workflow(cfg: dict, prompt: str, image_path: str,
                                 width: int = None, height: int = None,
                                 length: int = None, steps: int = None,
                                 seed: int = None, negative: str = "") -> tuple[dict, str, str, int]:
    import random, time
    model_cfg = get_model_cfg(cfg, "wan2.2_i2v")
    default_w = model_cfg.get("default_width", 528)
    default_h = model_cfg.get("default_height", 768)
    default_len = model_cfg.get("default_length", 81)
    default_steps = model_cfg.get("default_steps", 4)
    
    if seed is None:
        seed = random.randint(0, 2**63 - 1)
    w = width if width is not None else default_w
    h = height if height is not None else default_h
    l = length if length is not None else default_len
    s = steps if steps is not None else default_steps
    
    workflow_path = resolve_skill_path(model_cfg["workflow_path"])
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)
    
    uploaded_filename = upload_image_to_comfyui(cfg, image_path)
    for node_id, node_data in find_nodes_by_class(workflow, "LoadImage"):
        workflow[node_id]["inputs"]["image"] = uploaded_filename
    
    clip_nodes = find_nodes_by_class(workflow, "CLIPTextEncode")
    for node_id, node_data in clip_nodes:
        if "clip" in node_data.get("inputs", {}):
            if "the girl" in str(node_data.get("inputs", {}).get("text", "")):
                workflow[node_id]["inputs"]["text"] = prompt
            else:
                workflow[node_id]["inputs"]["text"] = negative if negative else ""
    
    for node_id, node_data in find_nodes_by_class(workflow, "WanImageToVideo"):
        workflow[node_id]["inputs"]["width"] = w
        workflow[node_id]["inputs"]["height"] = h
        workflow[node_id]["inputs"]["length"] = l
    
    for node_id, node_data in find_nodes_by_class(workflow, "WanMoeKSamplerAdvanced"):
        workflow[node_id]["inputs"]["steps"] = s
    for node_id, node_data in find_nodes_by_class(workflow, "Seed (rgthree)"):
        safe_seed = abs(seed) % (1125899906842624 + 1)
        workflow[node_id]["inputs"]["seed"] = safe_seed
    
    timestamp = time.strftime("%Y-%m-%d/%H%M%S")
    for node_id, node_data in find_nodes_by_class(workflow, "VHS_VideoCombine"):
        workflow[node_id]["inputs"]["filename_prefix"] = f"ComfyUI_{timestamp}"
    
    return workflow, "Wan2.2 I2V", uploaded_filename, seed

def cmd_wan2_2_i2v(cfg: dict, args: argparse.Namespace) -> None:
    prompt = args.prompt
    image_path = Path(args.image).expanduser()
    if not image_path.exists():
        print(f"❌ Image not found: {image_path}", file=sys.stderr)
        sys.exit(1)
    
    model_cfg = get_model_cfg(cfg, "wan2.2_i2v")
    length = args.length if args.length is not None else model_cfg.get("default_length", 81)
    steps = args.steps if args.steps is not None else model_cfg.get("default_steps", 4)
    seed = args.seed
    negative = args.negative or ""
    output_dir = ensure_output_dir(cfg, "wan2.2_i2v", args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Auto-detect resolution from image aspect ratio
    if args.width is not None and args.height is not None:
        width, height = args.width, args.height
    else:
        from PIL import Image
        try:
            with Image.open(str(image_path)) as img:
                iw, ih = img.size
                # Find closest matching Wan2.2 resolution from ALL available options
                width, height = find_closest_wan2_2_resolution(iw, ih)
                print(f"   Detected image size {iw}x{ih}, using {width}x{height}")
        except Exception as e:
            width = model_cfg.get("default_width", 560)
            height = model_cfg.get("default_height", 720)
    
    workflow, prompt_type_str, uploaded_fn, seed_used = prepare_wan2_2_i2v_workflow(
        cfg, prompt, str(image_path), width, height, length, steps, seed, negative
    )
    timeout = model_cfg.get("timeout_seconds", 1000)
    prompt_id, err_msg, errs = send_prompt_with_errors(cfg, workflow, timeout)
    if prompt_id is None:
        for w in errs:
            print(w)
        sys.exit(1)
    
    history = wait_for_completion(cfg, prompt_id, timeout)
    videos = get_output_videos(history, prompt_id, model_cfg, output_dir)
    if not videos:
        print("❌ No videos found in output!", file=sys.stderr)
        sys.exit(1)
    
    b64_videos = [video_b64_from_comfyui(cfg, v) for v in videos]
    local_paths = [save_b64_video(b64, v["filename"], output_dir)
                   for b64, v in zip(b64_videos, videos)]
    print_result_video(prompt_type_str, prompt, videos, local_paths, output_dir, cfg)

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="ComfyUI image generation client (T2I / I2I)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # t2i
    p_t2i = subparsers.add_parser("t2i", help="Text-to-Image generation")
    p_t2i.add_argument("--prompt", required=True, help="Text prompt")
    p_t2i.add_argument("--aspect", default="16:9", choices=list(ASPECT_RATIOS.keys()),
                         help="Aspect ratio")
    p_t2i.add_argument("--model", default="z-image", choices=["z-image", "sd35"],
                         help="Model: z-image (Z-Image, default) or sd35 (SD3.5)")
    p_t2i.add_argument("--seed", type=int, default=None)
    p_t2i.add_argument("--steps", type=int, default=None)
    p_t2i.add_argument("--cfg", type=float, default=None, help="CFG scale (SD3.5 only)")
    p_t2i.add_argument("--negative", default="", help="Negative prompt (SD3.5 only)")
    p_t2i.add_argument("--output-dir", default=None)

    # i2i
    p_i2i = subparsers.add_parser("i2i", help="Image-to-Image / Edit generation")
    p_i2i.add_argument("--prompt", required=True, help="Edit instructions")
    p_i2i.add_argument("--image", required=True, help="Source image file path")
    p_i2i.add_argument("--seed", type=int, default=None)
    p_i2i.add_argument("--steps", type=int, default=None)
    p_i2i.add_argument("--output-dir", default=None)

    # wan2.2
    p_wan22 = subparsers.add_parser("wan2.2", help="Wan2.2 Image-to-Video generation")
    p_wan22.add_argument("--prompt", required=True, help="Motion description")
    p_wan22.add_argument("--image", required=True, help="Input image file path")
    p_wan22.add_argument("--width", type=int, default=None)
    p_wan22.add_argument("--height", type=int, default=None)
    p_wan22.add_argument("--length", type=int, default=None)
    p_wan22.add_argument("--steps", type=int, default=None)
    p_wan22.add_argument("--seed", type=int, default=None)
    p_wan22.add_argument("--negative", default="")
    p_wan22.add_argument("--output-dir", default=None)

    # test
    subparsers.add_parser("test", help="Health check")

    args = parser.parse_args()
    cfg = load_config()

    if args.command == "t2i":
        cmd_t2i(cfg, args)
    elif args.command == "i2i":
        cmd_i2i(cfg, args)
    elif args.command == "wan2.2":
        cmd_wan2_2_i2v(cfg, args)
    elif args.command == "test":
        cmd_test(cfg, args)

if __name__ == "__main__":
    main()
