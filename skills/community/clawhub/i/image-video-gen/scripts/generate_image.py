#!/usr/bin/env python3
"""
AI Image Generator - Async Image Generation Script

Calls the AI Artist API to generate images from text prompts.
Handles async task polling until completion.

Supports Feishu webhook callback for result notification.
Set FEISHU_WEBHOOK_URL environment variable to enable.

Supports local file upload for reference images/videos.
Local files are automatically uploaded to get public URLs before calling generation APIs.
"""

import requests
import json
import time
import sys
import argparse
import os
import base64
from pathlib import Path

# Configuration
API_PREFIX = "https://ai.deepsop.com/prod-api/"
BASE_URL = f"{API_PREFIX.rstrip('/')}/ai"
FILE_UPLOAD_URL = f"{API_PREFIX.rstrip('/')}/system/fileUpload/upload"
ESTIMATE_COST_URL = f"{BASE_URL}/estimate/cost"
MODEL_LIST_URL = f"{BASE_URL}/consumeSource/list?pageNum=1&pageSize=999"
RECHARGE_URL = "https://ai.deepsop.com/"

# In-process cache for the model list (TTL seconds). Models can be toggled
# on/off server-side at any time, so we re-fetch periodically instead of
# hard-coding hiddenState values. A disk-backed fallback avoids hammering the
# API across short-lived CLI invocations on the same machine.
_MODEL_LIST_CACHE = {"rows": None, "expires_at": 0.0}
_MODEL_LIST_TTL = 300  # 5 minutes
import tempfile as _tempfile
_MODEL_LIST_DISK_CACHE = os.path.join(_tempfile.gettempdir(), "deepsop_model_list.json")

# Optionally load a .env file from the project root (best-effort; no hard dep)
try:
    from dotenv import load_dotenv as _load_dotenv  # type: ignore
    _load_dotenv()
except Exception:
    pass

# Get API key from environment variable (required)
API_KEY = os.environ.get("AI_ARTIST_TOKEN")

# Feishu webhook configuration (optional)
FEISHU_WEBHOOK_URL = os.environ.get("FEISHU_WEBHOOK_URL")

# Dry-run toggle: when True, task creators print the payload and skip network
# submission. Set via the CLI `--dry-run` flag or programmatically.
DRY_RUN = False


# Keep stdout reserved for machine-readable final output (URL / JSON) so
# orchestrators like openclaw can parse it reliably. Human progress logs go
# to stderr via _progress().
try:
    sys.stdout.reconfigure(line_buffering=True)  # Python 3.7+
except Exception:
    pass


def _progress(msg):
    """Write a human-facing progress line to stderr (flushed immediately)."""
    print(msg, file=sys.stderr, flush=True)


def _emit_cli_result(result, args, markdown_label=""):
    """Always emit a single terminal line on stdout for orchestrators.

    Behavior:
      - `--json-output` → one-line JSON `{"status","url","message","local_path"?}`
      - `--markdown-output` → `![label](url)` when SUCCESS
      - default → raw URL when SUCCESS, nothing on stdout when failed (errors on stderr)

    Failures always emit a clear stderr message so humans still see them.
    """
    status = (result or {}).get("status") or "FAILED"
    url = (result or {}).get("url")
    message = (result or {}).get("message") or "未知错误"

    if getattr(args, "json_output", False):
        payload = {
            "status": status,
            "url": url,
            "message": message,
        }
        if isinstance(result, dict) and result.get("local_path"):
            payload["local_path"] = result["local_path"]
        print(json.dumps(payload, ensure_ascii=False), flush=True)
        return

    if status == "SUCCESS" and url:
        if getattr(args, "markdown_output", False):
            print(f"![{markdown_label}]({url})", flush=True)
        else:
            print(url, flush=True)
    else:
        # Failure: keep stdout empty, surface a clear human message on stderr
        print(f"任务未成功：status={status}，message={message}", file=sys.stderr, flush=True)


def check_api_key():
    """Check if user has set their API key."""
    if not API_KEY:
        print("错误：未配置 AI_ARTIST_TOKEN 环境变量", file=sys.stderr)
        print("", file=sys.stderr)
        print("请先设置你的 API Key:", file=sys.stderr)
        print("  export AI_ARTIST_TOKEN=\"sk-your_api_key_here\"", file=sys.stderr)
        print("", file=sys.stderr)
        print("验证配置:", file=sys.stderr)
        print("  python3 scripts/test_config.py", file=sys.stderr)
        print("", file=sys.stderr)
        sys.exit(1)
    return True


def get_headers():
    """Build request headers with API key."""
    return {
        "Content-Type": "application/json",
        "X-Api-Key": API_KEY
    }


def estimate_generation_cost(payload):
    try:
        response = requests.post(ESTIMATE_COST_URL, json=payload, headers=get_headers(), timeout=30)
        response.raise_for_status()
        result = response.json()

        if result.get("code") != 200:
            print(f"费用预估失败：{result.get('msg', '未知错误')}", file=sys.stderr)
            return False

        data = result.get("data") or {}
        estimated_cost = data.get("estimatedCost")
        sufficient_balance = data.get("sufficientBalance")

        if estimated_cost is not None:
            _progress(f"预估费用：{estimated_cost} K币")

        if sufficient_balance is True:
            _progress("余额充足，正在创建任务")
            return True

        if sufficient_balance is False:
            print(f"余额不足，无法提交创建任务。请前往 {RECHARGE_URL} 充值 K 币后重试。", file=sys.stderr)
            return False

        print("费用预估返回结果不完整", file=sys.stderr)
        return False

    except requests.exceptions.HTTPError as e:
        print(_explain_http_error(e, context="费用预估"), file=sys.stderr)
        return False
    except requests.exceptions.RequestException as e:
        print(f"费用预估网络错误：{e}", file=sys.stderr)
        return False
    except ValueError as e:
        print(f"费用预估响应解析失败：{e}", file=sys.stderr)
        return False


def _load_disk_cache():
    """Load the disk cache file if present and still fresh; return rows or None."""
    import time
    try:
        if not os.path.exists(_MODEL_LIST_DISK_CACHE):
            return None
        with open(_MODEL_LIST_DISK_CACHE, "r", encoding="utf-8") as f:
            blob = json.load(f)
        if not isinstance(blob, dict) or "rows" not in blob:
            return None
        if blob.get("expires_at", 0) < time.time():
            return None
        return blob["rows"]
    except Exception:
        return None


def _save_disk_cache(rows, expires_at):
    try:
        with open(_MODEL_LIST_DISK_CACHE, "w", encoding="utf-8") as f:
            json.dump({"rows": rows, "expires_at": expires_at}, f, ensure_ascii=False)
    except Exception:
        pass  # best-effort


def fetch_model_list(force_refresh=False):
    """Fetch the full model list from consumeSource/list with TTL caching.

    Caching layers (fastest first):
      1. process-local `_MODEL_LIST_CACHE`
      2. disk cache at `_MODEL_LIST_DISK_CACHE` (survives across CLI runs)
      3. network call to `consumeSource/list`

    Returns a list of dicts (possibly empty on total failure).
    """
    import time
    now = time.time()

    # (1) in-process cache
    if (not force_refresh
            and _MODEL_LIST_CACHE["rows"] is not None
            and _MODEL_LIST_CACHE["expires_at"] > now):
        return _MODEL_LIST_CACHE["rows"]

    # (2) disk cache seed
    if not force_refresh and _MODEL_LIST_CACHE["rows"] is None:
        disk_rows = _load_disk_cache()
        if disk_rows is not None:
            _MODEL_LIST_CACHE["rows"] = disk_rows
            _MODEL_LIST_CACHE["expires_at"] = now + _MODEL_LIST_TTL
            return disk_rows

    # (3) network
    try:
        response = requests.post(
            MODEL_LIST_URL,
            json={"sourceTypeList": ["IMAGE_MODEL", "VIDEO_MODEL"]},
            headers=get_headers(),
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") != 200:
            print(f"模型列表查询失败：{payload.get('msg', '未知错误')}", file=sys.stderr)
            return _MODEL_LIST_CACHE["rows"] or []
        rows = payload.get("rows") or []
        expires_at = now + _MODEL_LIST_TTL
        _MODEL_LIST_CACHE["rows"] = rows
        _MODEL_LIST_CACHE["expires_at"] = expires_at
        _save_disk_cache(rows, expires_at)
        return rows
    except requests.exceptions.HTTPError as e:
        print(_explain_http_error(e, context="模型列表查询"), file=sys.stderr)
        return _MODEL_LIST_CACHE["rows"] or []
    except Exception as e:
        print(f"[warn] 模型列表查询异常，使用上次缓存：{e}", file=sys.stderr)
        return _MODEL_LIST_CACHE["rows"] or []


def check_model_available(model_key):
    """Verify the given model is currently active (hiddenState == '0').

    Returns True if usable, False if disabled or not found. On total network
    failure (no cache + request error) we return True so the user isn't blocked.
    """
    if model_key not in MODEL_CONFIGS:
        print(f"未知模型：{model_key}", file=sys.stderr)
        return False
    config = MODEL_CONFIGS[model_key]
    want_type = "IMAGE_MODEL" if config["media_type"] == "image" else "VIDEO_MODEL"
    want_value = str(config["methodType"])

    rows = fetch_model_list()
    if not rows:
        print(f"[warn] 无法确认 {model_key} 启用状态（模型列表为空），跳过校验", file=sys.stderr)
        return True

    for row in rows:
        if row.get("sourceType") == want_type and str(row.get("sourceValue")) == want_value:
            hidden = str(row.get("hiddenState"))
            if hidden == "1":
                print(
                    f"模型 {model_key} ({row.get('sourceName')}) 当前已停用 "
                    f"(hiddenState=1)，拒绝提交任务。可访问 {RECHARGE_URL} 查看最新可用模型。",
                    file=sys.stderr,
                )
                return False
            return True

    print(
        f"模型 {model_key} (sourceType={want_type}, sourceValue={want_value}) "
        f"不在服务端模型列表中，可能已下线，拒绝提交任务。",
        file=sys.stderr,
    )
    return False


_VIDEO_KEYWORDS = (
    "视频", "动画", "短片", "片段", "动起来", "动图",
    "镜头", "运镜", "画面动", "跳动", "挥手", "旋转", "奔跑",
    "video", "clip", "motion", "animation", "animate", "mp4",
)
_IMAGE_KEYWORDS = (
    "图片", "图像", "画一", "插画", "海报", "壁纸", "封面",
    "肖像", "写真", "头像", "logo",
    "image", "picture", "poster", "wallpaper", "illustration",
)


def _infer_media_type(prompt):
    """Infer 'video' or 'image' from prompt text. Defaults to 'image' when ambiguous."""
    if not prompt:
        return "image"
    p = str(prompt).lower()
    has_video = any(k.lower() in p for k in _VIDEO_KEYWORDS)
    has_image = any(k.lower() in p for k in _IMAGE_KEYWORDS)
    # Prefer video only if it's the dominant cue: a "video" keyword is present
    # AND no image-specific keyword is competing with it.
    if has_video and not has_image:
        return "video"
    return "image"


def list_active_models():
    """Return active (hiddenState == '0') models grouped by image/video.

    Cross-references the server's consumeSource/list with local MODEL_CONFIGS
    so only models the script actually knows how to dispatch are listed.
    """
    rows = fetch_model_list()
    active_by_type = {"IMAGE_MODEL": [], "VIDEO_MODEL": []}
    for row in rows:
        if str(row.get("hiddenState")) != "0":
            continue
        stype = row.get("sourceType")
        if stype not in active_by_type:
            continue
        value = str(row.get("sourceValue"))
        # match back to a MODEL_CONFIGS key
        local_key = next(
            (k for k, cfg in MODEL_CONFIGS.items()
             if str(cfg["methodType"]) == value
             and ((cfg["media_type"] == "image" and stype == "IMAGE_MODEL")
                  or (cfg["media_type"] == "video" and stype == "VIDEO_MODEL"))),
            None,
        )
        active_by_type[stype].append({
            "key": local_key,
            "sourceName": row.get("sourceName"),
            "sourceValue": value,
            "description": row.get("sourceDescription") or "",
        })
    return {
        "image": active_by_type["IMAGE_MODEL"],
        "video": active_by_type["VIDEO_MODEL"],
    }


def print_active_models():
    """Human-readable dump of currently active models."""
    data = list_active_models()
    print("=== 当前可用的图片模型 (hiddenState=0) ===")
    for m in data["image"]:
        key_hint = f"  key={m['key']}" if m["key"] else "  (脚本未注册)"
        print(f"- {m['sourceName']} [sourceValue={m['sourceValue']}]{key_hint}")
        if m["description"]:
            print(f"    {m['description']}")
    print("\n=== 当前可用的视频模型 (hiddenState=0) ===")
    for m in data["video"]:
        key_hint = f"  key={m['key']}" if m["key"] else "  (脚本未注册)"
        print(f"- {m['sourceName']} [sourceValue={m['sourceValue']}]{key_hint}")
        if m["description"]:
            print(f"    {m['description']}")
    print("\n默认模型：图片 → 3.1Nano2-Evo；视频 → V3.1FB")


_UPLOAD_SOFT_LIMIT_MB = 100  # generous cap; specific per-model caps are checked separately


def _explain_http_error(exc, context=""):
    """Produce a user-friendly message for common HTTP failure modes."""
    status = getattr(getattr(exc, "response", None), "status_code", None)
    prefix = f"{context} " if context else ""
    if status == 401:
        return (f"{prefix}认证失败 (401)。请确认环境变量 AI_ARTIST_TOKEN 已设置且未过期，"
                f"并在 {RECHARGE_URL} 重新生成 API Key。")
    if status == 403:
        return f"{prefix}权限不足 (403)。当前 API Key 可能未授权该模型或功能。"
    if status == 429:
        return f"{prefix}请求过于频繁 (429)。请稍候 10-30 秒再重试，或降低并发。"
    if status and 500 <= status < 600:
        return f"{prefix}服务端错误 ({status})。请稍后重试；若持续发生请联系管理员。"
    return f"{prefix}网络/请求错误：{exc}"


def upload_file(file_path):
    """Upload a local file to the file server and get a public URL.

    Pre-checks file existence and size (soft cap 100MB) before uploading to
    avoid wasting bandwidth. Returns the public URL or None on failure.
    """
    if not os.path.exists(file_path):
        print(f"文件不存在：{file_path}", file=sys.stderr)
        return None

    try:
        file_size = os.path.getsize(file_path)
    except OSError as e:
        print(f"无法读取文件大小：{e}", file=sys.stderr)
        return None

    size_mb = file_size / (1024 * 1024)
    if size_mb > _UPLOAD_SOFT_LIMIT_MB:
        print(
            f"文件过大 ({size_mb:.1f} MB > {_UPLOAD_SOFT_LIMIT_MB} MB)，拒绝上传。"
            f"请压缩或分段后重试。",
            file=sys.stderr,
        )
        return None

    _progress(f"[upload] 开始上传 {os.path.basename(file_path)} ({size_mb:.2f} MB)…")
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            headers = {'X-Api-Key': API_KEY}
            response = requests.post(FILE_UPLOAD_URL, headers=headers, files=files, timeout=120)
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 200:
                url = result.get("url")
                _progress(f"[upload] ✓ 上传完成：{url}")
                return url
            print(f"文件上传失败：{result.get('msg', '未知错误')}", file=sys.stderr)
            return None
    except requests.exceptions.HTTPError as e:
        print(_explain_http_error(e, context="文件上传"), file=sys.stderr)
        return None
    except Exception as e:
        print(f"文件上传错误：{e}", file=sys.stderr)
        return None


def download_image(url, output_path=None):
    """
    Download image from URL.
    
    Args:
        url: Image URL
        output_path: Optional path to save the image
    
    Returns:
        bytes: Image data, or None if failed
    """
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        image_data = response.content
        
        # Save to file if path provided
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(image_data)
            _progress(f"图片已保存：{output_path}")
        
        return image_data
        
    except Exception as e:
        print(f"下载图片失败：{e}", file=sys.stderr)
        return None


def image_to_data_uri(image_data, mime_type="image/png"):
    """
    Convert image bytes to data URI.
    
    Args:
        image_data: Raw image bytes
        mime_type: MIME type of the image
    
    Returns:
        str: Data URI string
    """
    base64_data = base64.b64encode(image_data).decode('utf-8')
    return f"data:{mime_type};base64,{base64_data}"


def send_feishu_message(prompt, result, media_type="image"):
    """Send generation result to Feishu chat (supports image or video)."""
    if not FEISHU_WEBHOOK_URL:
        return False

    label = "图片" if media_type == "image" else "视频"
    open_btn = "打开" + label
    try:
        if result and result["status"] == "SUCCESS":
            content = {
                "msg_type": "interactive",
                "card": {
                    "header": {
                        "title": {"tag": "plain_text", "content": f"{label}生成成功"},
                        "template": "green"
                    },
                    "elements": [
                        {
                            "tag": "div",
                            "text": {
                                "tag": "lark_md",
                                "content": f"**提示词**: {prompt}\n\n**{label}链接**: [点击查看]({result['url']})"
                            }
                        },
                        {
                            "tag": "action",
                            "actions": [{
                                "tag": "button",
                                "text": {"tag": "plain_text", "content": open_btn},
                                "url": result["url"],
                                "type": "default"
                            }]
                        }
                    ]
                }
            }
        else:
            error_msg = result.get("message", "未知错误") if result else "未知错误"
            content = {
                "msg_type": "interactive",
                "card": {
                    "header": {
                        "title": {"tag": "plain_text", "content": f"{label}生成失败"},
                        "template": "red"
                    },
                    "elements": [{
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**提示词**: {prompt}\n\n**错误**: {error_msg}"
                        }
                    }]
                }
            }
        
        response = requests.post(
            FEISHU_WEBHOOK_URL,
            json=content,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        return True
        
    except Exception as e:
        print(f"[Feishu] 发送通知失败：{e}", file=sys.stderr)
        return False


# Model configurations
# media_type: "image" or "video" — determines task creation and output handling
# Keys follow API sourceName (DeepSop·X). Only hiddenState=0 (active) models are included.
# source_name / description mirror the API metadata for traceability.

# Note: per-model extra_params intentionally carry ONLY the fields each model
# actually accepts (cross-referenced with VIDEO_FIELD_SUPPORT / IMAGE_FIELD_SUPPORT).
# Target constraints (targetMaxSize / targetMinLength / targetMaxLength) are
# populated by `_apply_restriction()` at runtime and should NOT be duplicated here.

# ---------------------------------------------------------------------------
# Field → supported-models whitelist (mirrors frontend `handleParameterVisibility`).
# After the payload is built, fields not in the active model's whitelist are
# stripped so we don't send parameters the model does not understand.
# ---------------------------------------------------------------------------
# Image-side parameter whitelist (mirrors frontend `handleImgParameterVisibility`).
#   webSearch       → S5.0L (mt=4) + 3.1Nano2-Evo (mt=8)
#   imageSearch     → 3.1Nano2-Evo (mt=8)
#   ratiocination   → Image2 (mt=10)
#   n               → Image2 (mt=10)  [图片生成数量 1-10]
IMAGE_FIELD_SUPPORT = {
    "webSearch":     {"S5.0L", "3.1Nano2-Evo"},
    "imageSearch":   {"3.1Nano2-Evo"},
    "ratiocination": {"Image2"},
    "n":             {"Image2"},
    # Image2 Beta-Evo (mt=11) does NOT submit `quality` (frontend noField.quality=['11']).
    # Models listed here may submit `quality`; others are stripped before POST.
    "quality": {"N2", "S5.0L", "W2.7", "W2.7Pro", "3.1Nano2-Evo", "Nano2-Beta-Evo",
                "Image2", "S4.5", "N1", "N2-147", "N2Pro-147"},
}

# Video-side: each key = optional field; value = set of model keys that accept it.
# Fields NOT listed here (methodType, text, size, duration, generationType,
# imageUrlList, firstImageUrl, targetMax*) are considered universal/contextual
# and pass through unfiltered.
VIDEO_FIELD_SUPPORT = {
    # Negative prompt: V3.1Fast + Wan series (mt 5,6,7,8,9,14,15,16)
    "negativePrompt": {"V3.1Fast", "W2.6t", "W2.6i", "W2.6r",
                       "W2.7t", "W2.7i", "W2.7r"},
    # Audio toggle: S1.5Pro, V3.1Fast, klingV3Omni  (mt 2,5,10)
    "generateAudio": {"S1.5Pro", "V3.1Fast", "klingV3Omni"},
    # English enhancement: V3.1 series (mt 3,4,5)
    "enhancePrompt": {"V3.1FB", "V3.1PB", "V3.1Fast"},
    # Smart rewrite: Wan series (mt 7,8,9,14,15,16)
    "promptExtend": {"W2.6t", "W2.6i", "W2.6r", "W2.7t", "W2.7i", "W2.7r"},
    # Generation count / people / resize: V3.1Fast  (mt 5)
    "n": {"V3.1Fast"},
    "personGeneration": {"V3.1Fast"},
    "resizeMode": {"V3.1Fast"},
    # Shot mode: Wan2.6 + klingV3Omni  (mt 7,8,9,10)
    "shotType": {"W2.6t", "W2.6i", "W2.6r", "klingV3Omni"},
    # Duration switch (manual/intelligent): only S1.5Pro  (mt 2)
    "durationSwitch": {"S1.5Pro"},
    # klingV3Omni exclusives (mt 10)
    "mode": {"klingV3Omni"},
    "multiShot": {"klingV3Omni"},
    "multiPrompt": {"klingV3Omni"},
    "keepOriginalSound": {"klingV3Omni"},
    "elementList": {"klingV3Omni"},
    "videoList": {"klingV3Omni"},
    # Continuation / reference clip: klingV3Omni + W2.7i  (mt 10,14)
    "firstClipUrl": {"klingV3Omni", "W2.7i"},
    # Reference-video list: W2.6r / W2.7r  (mt 9,16)
    "videoUrlList": {"W2.6r", "W2.7r"},
    # Audio URL: Wan text/image/W2.7 series  (mt 7,8,14,15,16)
    "audioUrl": {"W2.6t", "W2.6i", "W2.7t", "W2.7i", "W2.7r"},
    # lastImageUrl: NOT supported by W2.6i (mt=8) or Sora2 variants. All other
    # active video models support it.
    "lastImageUrl": {"S1.5Pro", "V3.1FB", "V3.1PB", "V3.1Fast",
                     "W2.6t", "W2.6r", "klingV3Omni",
                     "W2.7t", "W2.7i", "W2.7r"},
    # ratio: W2.6i (mt=8) and W2.7i (mt=14) derive ratio from the first frame.
    "ratio": {"S1.5Pro", "V3.1FB", "V3.1PB", "V3.1Fast",
              "W2.6t", "W2.6r", "klingV3Omni",
              "W2.7t", "W2.7r"},
    # resolution: klingV3Omni (mt=10) does not expose a resolution selector.
    "resolution": {"S1.5Pro", "V3.1FB", "V3.1PB", "V3.1Fast",
                   "W2.6t", "W2.6i", "W2.6r",
                   "W2.7t", "W2.7i", "W2.7r"},
}


def _filter_by_whitelist(parameter, model, support_matrix):
    """Drop keys from `parameter` that the whitelist says this model doesn't accept."""
    for field, allowed_models in support_matrix.items():
        if field in parameter and model not in allowed_models:
            parameter.pop(field, None)
    return parameter


# ---------------------------------------------------------------------------
# Allowed-value tables per model (mirrors frontend match* option builders).
# Values not listed will be auto-replaced with a safe fallback + warning.
# ---------------------------------------------------------------------------

# generationType whitelist per model (matchGenerationTypeOptions)
VIDEO_GENERATION_TYPES = {
    "S1.5Pro":     ["TEXT", "FIRST&LAST"],
    "V3.1FB":      ["TEXT", "FIRST&LAST", "REFERENCE"],
    "V3.1PB":      ["TEXT", "FIRST&LAST"],
    "V3.1Fast":    ["TEXT", "FIRST&LAST"],
    "W2.6t":       ["TEXT"],
    "W2.6i":       ["FIRST&LAST"],
    "W2.6r":       ["REFERENCE"],
    "klingV3Omni": ["TEXT", "FIRST&LAST", "REFERENCE", "EDIT", "FEATURE"],
    "W2.7i":       ["FIRST&LAST", "CONTINUATION"],
    "W2.7t":       ["TEXT"],
    "W2.7r":       ["REFERENCE"],
}

# ratio whitelist per model (matchVideoRatioOptions). W2.6i / W2.7i derive from
# the first frame so ratio is not submitted at all (handled by VIDEO_FIELD_SUPPORT).
VIDEO_RATIOS = {
    "S1.5Pro":     ["1:1", "3:4", "4:3", "16:9", "9:16", "21:9", "adaptive"],
    "V3.1FB":      ["16:9", "9:16", "adaptive"],
    "V3.1PB":      ["16:9", "9:16", "adaptive"],
    "V3.1Fast":    ["16:9", "9:16", "adaptive"],
    "W2.6t":       ["1:1", "3:4", "4:3", "16:9", "9:16"],
    "W2.6r":       ["1:1", "3:4", "4:3", "16:9", "9:16"],
    "klingV3Omni": ["1:1", "16:9", "9:16"],
    "W2.7t":       ["1:1", "3:4", "4:3", "16:9", "9:16"],
    "W2.7r":       ["1:1", "3:4", "4:3", "16:9", "9:16"],
}

# resolution whitelist per model (matchVideoQualityOptions). klingV3Omni does
# not submit a resolution at all (handled by VIDEO_FIELD_SUPPORT).
VIDEO_RESOLUTIONS = {
    "S1.5Pro":     ["480p", "720p", "1080p"],
    "V3.1FB":      ["720p", "1080p", "4K"],
    "V3.1PB":      ["720p", "1080p", "4K"],
    "V3.1Fast":    ["720p", "1080p", "4K"],
    "W2.6t":       ["720p", "1080p"],
    "W2.6i":       ["720p", "1080p"],
    "W2.6r":       ["720p", "1080p"],
    "W2.7i":       ["720p", "1080p"],
    "W2.7t":       ["720p", "1080p"],
    "W2.7r":       ["720p", "1080p"],
}

# Image quality whitelist (matchImageQualityOptions, active models only).
# `Image2-Beta-Evo` (mt=11) intentionally absent: the frontend hides quality for it
# and the field is stripped via IMAGE_FIELD_SUPPORT["quality"] before POST.
IMAGE_QUALITIES = {
    "N2":             ["1K", "2K", "4K"],
    "S5.0L":          ["2K", "3K"],
    "W2.7":           ["1K", "2K"],
    "W2.7Pro":        ["1K", "2K"],
    "3.1Nano2-Evo":   ["1K", "2K", "4K"],
    "Nano2-Beta-Evo": ["1K", "2K", "4K"],
    "Image2":         ["1K", "2K", "4K"],
}

# Image ratio/size exclusions (matchImageRatioOptions excludedRatios).
# Values listed are NOT allowed; empty set means any ratio allowed.
# Note: only relevant when the user passes a ratio-style size (e.g. "16:9");
# pixel-size strings like "2048x2048" / "2048*2048" pass through unchecked.
IMAGE_SIZE_EXCLUDED = {
    "N2":              ["1:2", "2:1", "1:3", "3:1", "1:4", "4:1", "1:8", "8:1", "9:21"],
    "S5.0L":           ["auto"],
    "W2.7":            ["auto", "9:21", "21:9"],
    "W2.7Pro":         ["auto", "9:21", "21:9"],
    "3.1Nano2-Evo":    ["1:2", "2:1", "1:3", "3:1", "9:21"],
    "Nano2-Beta-Evo":  ["1:2", "2:1", "1:3", "3:1", "9:21"],
    "Image2":          ["1:4", "4:1", "1:8", "8:1"],
    "Image2-Beta-Evo": ["1:4", "4:1", "1:8", "8:1", "4:5", "5:4"],
}


def _coerce_value(current, allowed, fallback, label, model):
    """If current not in allowed, warn and return fallback; else return current."""
    if current is None:
        return current
    if current in allowed:
        return current
    print(
        f"{model} 不支持 {label}={current!r}（可选：{allowed}），自动调整为 {fallback!r}",
        file=sys.stderr,
    )
    return fallback


# ---------------------------------------------------------------------------
# Per-model restrictions (sourced from frontend `Restrictions` mixin).
# - textLength / negativeTextLength → prompt length caps (chars)
# - targetMaxSize / targetMinLength / targetMaxLength → reference-image
#   constraints that MUST be forwarded to the API via the `targetMax*` fields.
# ---------------------------------------------------------------------------
VIDEO_RESTRICTIONS = {
    "S1.5Pro":     {"textLength": 500,  "targetMaxSize": 30, "targetMinLength": 300, "targetMaxLength": 6000},
    "V3.1FB":      {"textLength": 1000, "negativeTextLength": 250, "targetMaxSize": 10, "targetMinLength": 300, "targetMaxLength": 6000},
    "V3.1PB":      {"textLength": 1000, "negativeTextLength": 250, "targetMaxSize": 10, "targetMinLength": 300, "targetMaxLength": 6000},
    "V3.1Fast":    {"textLength": 1000, "negativeTextLength": 250, "targetMaxSize": 10, "targetMinLength": 300, "targetMaxLength": 6000},
    "W2.6t":       {"textLength": 750,  "negativeTextLength": 250, "targetMaxSize": 10, "targetMinLength": 360, "targetMaxLength": 2000},
    "W2.6i":       {"textLength": 750,  "negativeTextLength": 250, "targetMaxSize": 10, "targetMinLength": 360, "targetMaxLength": 2000},
    "W2.6r":       {"textLength": 750,  "negativeTextLength": 250, "targetMaxSize": 10, "targetMinLength": 240, "targetMaxLength": 5000},
    "klingV3Omni": {"textLength": 1250, "targetMaxSize": 10, "targetMinLength": 300},
    "W2.7i":       {"textLength": 2500, "negativeTextLength": 250, "targetMaxSize": 20, "targetMinLength": 240, "targetMaxLength": 8000},
    "W2.7t":       {"textLength": 2500, "negativeTextLength": 250, "targetMaxSize": 20, "targetMinLength": 240, "targetMaxLength": 8000},
    "W2.7r":       {"textLength": 2500, "negativeTextLength": 250, "targetMaxSize": 10, "targetMinLength": 240, "targetMaxLength": 5000},
}

IMAGE_RESTRICTIONS = {
    "N2":              {"textLength": 1000, "targetMaxSize": 10, "targetMaxLength": 6000},
    "S5.0L":           {"textLength": 300,  "targetMaxSize": 10, "targetMaxLength": 6000},
    "W2.7":            {"textLength": 2500, "targetMaxSize": 20, "targetMaxLength": 8000, "targetMinLength": 240},
    "W2.7Pro":         {"textLength": 2500, "targetMaxSize": 20, "targetMaxLength": 8000, "targetMinLength": 240},
    "3.1Nano2-Evo":    {"textLength": 1000, "targetMaxSize": 20, "targetMaxLength": 6000},
    "Nano2-Beta-Evo":  {"textLength": 1000, "targetMaxSize": 10, "targetMaxLength": 6000},
    # GPT Image2 series: large prompt window, no max/min length constraint on refs.
    "Image2":          {"textLength": 16000, "targetMaxSize": 50},
    "Image2-Beta-Evo": {"textLength": 16000, "targetMaxSize": 50},
}

# Render-quality (ratiocination) whitelist for Image2 (imageRenderQualityList).
IMAGE_RATIOCINATION_OPTIONS = ["low", "medium", "high"]


def _apply_restriction(parameter, restriction):
    """Overwrite targetMaxSize / targetMinLength / targetMaxLength per restriction."""
    for key in ("targetMaxSize", "targetMinLength", "targetMaxLength"):
        if key in restriction:
            parameter[key] = restriction[key]
        else:
            parameter.pop(key, None)


def _check_text_length(text, limit, label, model):
    """Warn (but don't block) when text exceeds the model's limit."""
    if text and limit and len(str(text)) > limit:
        print(
            f"⚠️  {model} {label} 长度 {len(text)} 超过限制 {limit}，已截断末尾 {len(text) - limit} 字符后提交",
            file=sys.stderr,
        )
        return str(text)[:limit]
    return text


MODEL_CONFIGS = {
    # ===== Image models (type=10) =====
    "N2": {
        "media_type": "image",
        "type": "10",
        "methodType": "2",
        "source_name": "DeepSop·N2",
        "description": "N2 支持多模态输入 精细参数调节 卓越的文字渲染和角色一致性",
        "default_size": "1:1",
        "default_quality": "2K",
        "extra_params": {}
    },
    "S5.0L": {
        "media_type": "image",
        "type": "10",
        "methodType": "4",
        "source_name": "DeepSop·S5.0L",
        "description": "生成快、风格全、易用，支持联网，适合快速出图",
        "default_size": "2048x2048",
        "default_quality": "2K",
        "extra_params": {"duration": 10}
    },
    "W2.7": {
        "media_type": "image",
        "type": "10",
        "methodType": "6",
        "source_name": "DeepSop.W2.7",
        "description": "W2.7 支持文生图、图生图多模态输入，画质清晰，细节丰富",
        "default_size": "2048*2048",
        "default_quality": "2K",
        "extra_params": {}
    },
    "W2.7Pro": {
        "media_type": "image",
        "type": "10",
        "methodType": "7",
        "source_name": "DeepSop.W2.7Pro",
        "description": "W2.7Pro 精准控图与风格迁移，角色一致性更优，画质细节更优",
        "default_size": "2048*2048",
        "default_quality": "2K",
        "extra_params": {}
    },
    "3.1Nano2-Evo": {
        "media_type": "image",
        "type": "10",
        "methodType": "8",
        "source_name": "DeepSop·3.1Nano2-Evo",
        "description": "N2 支持多模态输入 精细参数调节 卓越的文字渲染和角色一致性",
        "default_size": "1:1",
        "default_quality": "2K",
        "extra_params": {}
    },
    "Nano2-Beta-Evo": {
        "media_type": "image",
        "type": "10",
        "methodType": "9",
        "source_name": "DeepSop·Nano2 Beta-Evo",
        "description": "N2 支持多模态输入 精细参数调节 卓越的文字渲染和角色一致性",
        "default_size": "1:1",
        "default_quality": "2K",
        "extra_params": {}
    },
    "Image2": {
        "media_type": "image",
        "type": "10",
        "methodType": "10",
        "source_name": "DeepSop·Image2",
        "description": "Image2 支持多模态图像生成 精准控图 细节丰富 角色一致性更优（GPTimage-2）",
        "default_size": "auto",
        "default_quality": "2K",
        # ratiocination/imageSearch/n 均为 Image2 专属；默认不开启 imageSearch
        "extra_params": {"ratiocination": "medium", "imageSearch": True, "n": 1},
    },
    "Image2-Beta-Evo": {
        "media_type": "image",
        "type": "10",
        "methodType": "11",
        "source_name": "DeepSop·Image2 Beta-Evo",
        "description": "Image2 Beta（服务端当前 hiddenState=1，待启用）",
        "default_size": "auto",
        # mt=11 不提交 quality 字段，但保留 default 以防调用者误传
        "default_quality": "2K",
        "extra_params": {},
    },
    # ----- Image models currently hiddenState=1 (kept for future reactivation) -----
    "S4.5": {
        "media_type": "image",
        "type": "10",
        "methodType": "0",
        "source_name": "DeepSop·S4.5",
        "description": "S4.5 支持电影级画质4K 角色一致性",
        "default_size": "2048x2048",
        "default_quality": "2K",
        "extra_params": {}
    },
    "N1": {
        "media_type": "image",
        "type": "10",
        "methodType": "1",
        "source_name": "DeepSop·N1",
        "description": "N1 支持多模态输入 精细参数调节 卓越的文字渲染和角色一致性",
        "default_size": "1:1",
        "default_quality": "1K",
        "extra_params": {}
    },
    "N2-147": {
        "media_type": "image",
        "type": "10",
        "methodType": "3",
        "source_name": "DeepSop·3-Nano2-147",
        "description": "N2 支持多模态输入 精细参数调节 卓越的文字渲染和角色一致性",
        "default_size": "1:1",
        "default_quality": "2K",
        "extra_params": {}
    },
    "N2Pro-147": {
        "media_type": "image",
        "type": "10",
        "methodType": "5",
        "source_name": "DeepSop·3.1Nano2-147",
        "description": "N2 支持多模态输入 精细参数调节 卓越的文字渲染和角色一致性",
        "default_size": "1:1",
        "default_quality": "2K",
        "extra_params": {}
    },

    # ===== Video models (type=9) =====
    "S1.5Pro": {
        "media_type": "video",
        "type": "9",
        "methodType": "2",
        "source_name": "DeepSop·S1.5Pro",
        "description": "S1.5Pro 影视级连贯叙事视频 音画同步与精准口型对齐",
        "default_ratio": "16:9",
        "default_resolution": "720p",
        "default_duration": 10,
        "extra_params": {
            "generationType": "FIRST&LAST",
            "negativePrompt": "",
            "firstImageUrl": None,
            "lastImageUrl": None,
            "durationList": [],
            "enhancePrompt": False,
            "generateAudio": True,
            "n": 1,
            "personGeneration": "allow_adult",
            "resizeMode": "pad",
            "promptExtend": False,
            "shotType": "single",
            "durationSwitch": "1",
            "targetMaxSize": 30,
            "targetMinLength": 300,
            "targetMaxLength": 6000
        }
    },
    "V3.1FB": {
        "media_type": "video",
        "type": "9",
        "methodType": "3",
        "source_name": "DeepSop·V3.1FB",
        "description": "V3.1FB 快速生成 基础流畅",
        "default_ratio": "16:9",
        "default_resolution": "1080p",
        "default_duration": 8,
        "extra_params": {
            "generationType": "FIRST&LAST",
            "enhancePrompt": False,
            "durationList": [],
        }
    },
    "V3.1PB": {
        "media_type": "video",
        "type": "9",
        "methodType": "4",
        "source_name": "DeepSop·V3.1PB",
        "description": "V3.1Pro 多图参考 角色一致性",
        "default_ratio": "adaptive",
        "default_resolution": "720p",
        "default_duration": 8,
        "extra_params": {
            "generationType": "FIRST&LAST",
            "enhancePrompt": False,
            "durationList": [],
        }
    },
    "V3.1Fast": {
        "media_type": "video",
        "type": "9",
        "methodType": "5",
        "source_name": "DeepSop·V3.1Fast",
        "description": "V3.1Fast 快速生成 音画同步 竖屏适配",
        "default_ratio": "16:9",
        "default_resolution": "720p",
        "default_duration": 8,
        "extra_params": {
            "generationType": "FIRST&LAST",
            "negativePrompt": "",
            "enhancePrompt": False,
            "generateAudio": True,
            "n": 1,
            "personGeneration": "allow_adult",
            "resizeMode": "pad",
            "durationList": [],
        }
    },
    "W2.6t": {
        "media_type": "video",
        "type": "9",
        "methodType": "7",
        "source_name": "DeepSop·W2.6t",
        "description": "W2.6t 文生视频 智能多镜头叙事 15秒 1080P高清",
        "default_ratio": "16:9",
        "default_resolution": "720p",
        "default_duration": 10,
        "extra_params": {
            "generationType": "TEXT",
            "negativePrompt": "",
            "promptExtend": False,
            "shotType": "single",
            "durationList": [],
        }
    },
    "W2.6i": {
        "media_type": "video",
        "type": "9",
        "methodType": "8",
        "source_name": "DeepSop·W2.6i",
        "description": "W2.6i 适合让插画或照片\"活起来\" 动作延展与场景叙事",
        "default_ratio": "16:9",
        "default_resolution": "720p",
        "default_duration": 10,
        "extra_params": {
            "generationType": "FIRST&LAST",
            "negativePrompt": "",
            "promptExtend": False,
            "shotType": "single",
            "durationList": [],
        }
    },
    "W2.6r": {
        "media_type": "video",
        "type": "9",
        "methodType": "9",
        "source_name": "DeepSop·W2.6r",
        "description": "W2.6r 参考视频生成视频 保留角色和音色 可跨场景迁移与互动",
        "default_ratio": "16:9",
        "default_resolution": "720p",
        "default_duration": 10,
        "extra_params": {
            "generationType": "REFERENCE",
            "negativePrompt": "",
            "promptExtend": False,
            "shotType": "single",
            "durationList": [],
        }
    },
    "klingV3Omni": {
        "media_type": "video",
        "type": "9",
        "methodType": "10",
        "source_name": "DeepSop.klingV3Omni",
        "description": "支持多模态融合输入，画面细节丰富，角色与场景一致性更优（按张计费）",
        "default_ratio": "16:9",
        "default_resolution": "720p",
        "default_duration": 10,
        "extra_params": {
            "generationType": "FIRST&LAST",
            "negativePrompt": "",
            "imageUrlList": None,
            "firstImageUrl": None,
            "lastImageUrl": None,
            "firstClipUrl": None,
            "elementList": [],
            "durationList": [],
            "mode": "pro",
            "multiShot": False,
            "keepOriginalSound": "yes",
            "generateAudio": True,
            "shotType": "single",
            "targetMaxSize": 10,
            "targetMinLength": 300,
            "targetMaxLength": 6000,
        }
    },
    "W2.7i": {
        "media_type": "video",
        "type": "9",
        "methodType": "14",
        "source_name": "DeepSop·W2.7i",
        "description": "W2.7i 图生视频 首尾帧平滑过渡 动作延展与视频续写 更流畅自然",
        "default_ratio": "16:9",
        "default_resolution": "720p",
        "default_duration": 10,
        "extra_params": {
            "generationType": "FIRST&LAST",
            "negativePrompt": "",
            "promptExtend": False,
            "durationList": [],
        }
    },
    "W2.7t": {
        "media_type": "video",
        "type": "9",
        "methodType": "15",
        "source_name": "DeepSop.W2.7t",
        "description": "W2.7t 文生视频 智能多镜头剪辑 自动配音 2K高清 成片更高效",
        "default_ratio": "16:9",
        "default_resolution": "720p",
        "default_duration": 10,
        "extra_params": {
            "generationType": "TEXT",
            "negativePrompt": "",
            "promptExtend": False,
            "durationList": [],
        }
    },
    "W2.7r": {
        "media_type": "video",
        "type": "9",
        "methodType": "16",
        "source_name": "DeepSop.W2.7r",
        "description": "W2.7r 参考视频生成 保留角色音色 多模态融合编辑 跨场景迁移",
        "default_ratio": "16:9",
        "default_resolution": "720p",
        "default_duration": 10,
        "extra_params": {
            "generationType": "REFERENCE",
            "negativePrompt": "",
            "promptExtend": False,
            "durationList": [],
        }
    },
    # ----- Video models currently hiddenState=1 (kept for future reactivation) -----
    "Sora2-BetaMax": {
        "media_type": "video",
        "type": "9",
        "methodType": "1",
        "source_name": "DeepSop·Sora2 Beta Max Evolink",
        "description": "Sora 2 Beta Max Evolink",
        "default_ratio": "16:9",
        "default_resolution": "720p",
        "default_duration": 10,
        "extra_params": {}
    },
    "V3.1Pro": {
        "media_type": "video",
        "type": "9",
        "methodType": "6",
        "source_name": "DeepSop·V3.1Pro",
        "description": "专业版模型 4K超清 多图参考角色跨场景一致性 商业级",
        "default_ratio": "16:9",
        "default_resolution": "1080p",
        "default_duration": 8,
        "extra_params": {
            "generationType": "FIRST&LAST",
            "negativePrompt": "",
            "enhancePrompt": False,
            "generateAudio": True,
            "n": 1,
            "personGeneration": "allow_adult",
            "resizeMode": "pad",
            "durationList": [],
        }
    },
    "Sora2-147": {
        "media_type": "video",
        "type": "9",
        "methodType": "11",
        "source_name": "DeepSop·Sora2.147",
        "description": "物理真实、叙事连贯、音画同步，电影级质感",
        "default_ratio": "16:9",
        "default_resolution": "720p",
        "default_duration": 10,
        "extra_params": {}
    },
    "Sora2Pro-147": {
        "media_type": "video",
        "type": "9",
        "methodType": "12",
        "source_name": "DeepSop·Sora2 Pro.147",
        "description": "物理真实、时长更长、音画同步、画质专业、影视级可控性强",
        "default_ratio": "16:9",
        "default_resolution": "720p",
        "default_duration": 10,
        "extra_params": {}
    },
    "Sora2Pro-Evolink": {
        "media_type": "video",
        "type": "9",
        "methodType": "13",
        "source_name": "DeepSop·Sora2 Pro Evolink",
        "description": "原生视频生成，具备帧级动态控制、音画同步等视频专属能力",
        "default_ratio": "16:9",
        "default_resolution": "720p",
        "default_duration": 10,
        "extra_params": {}
    }
}


def create_video_task(prompt, model="V3.1FB", ratio=None, resolution=None,
                      duration=None, first_image_url=None, last_image_url=None,
                      generate_audio=None, scale_factor=None, generation_type=None,
                      enhance_prompt=None, prompt_extend=None, audio_url=None,
                      image_url_list=None, video_url_list=None,
                      mode=None, keep_original_sound=None, shot_type=None,
                      element_list=None, first_clip_url=None, multi_shot=None,
                      n=None, person_generation=None, resize_mode=None,
                      negative_prompt=None, duration_switch=None,
                      multi_prompt=None):
    """Create a video generation task.

    Args:
        prompt: Text description of the video
        model: Video model key (e.g. S1.5Pro, V3.1FB, V3.1PB, V3.1Fast,
               W2.6t, W2.6i, W2.6r, klingV3Omni, W2.7i, W2.7t, W2.7r)
        ratio: Aspect ratio, e.g. '16:9', '9:16', '1:1'
        resolution: Video resolution, e.g. '720p', '1080p'
        duration: Video duration in seconds
        first_image_url: URL of the first frame image (FIRST&LAST mode)
        last_image_url: URL of the last frame image (FIRST&LAST mode)
        generate_audio: Whether to generate audio (True/False)
        scale_factor: Optional scaleFactor override
        generation_type: Generation type override, e.g. 'FIRST&LAST', 'TEXT', 'REFERENCE'
        enhance_prompt: Whether to enhance the prompt
        prompt_extend: Whether to extend the prompt
        audio_url: URL of audio file (WAN series)
        image_url_list: List of image URLs for reference (WAN *r / multimodal)
        video_url_list: List of video URLs for reference (WAN *r)
    """
    url = f"{BASE_URL}/AiArtistRecord"

    if model not in MODEL_CONFIGS or MODEL_CONFIGS[model]["media_type"] != "video":
        print(f"不支持的视频模型：{model}", file=sys.stderr)
        return None

    # Prompt requirement (mirrors frontend handleVerifyParams):
    # - W2.6i / W2.7i (image-to-video) can omit prompt
    # - klingV3Omni with shotType='customize' uses per-shot prompts, not top-level
    # - all other video models require a non-empty prompt
    _image_to_video = model in {"W2.6i", "W2.7i"}
    _kling_customize = (model == "klingV3Omni" and shot_type == "customize")
    if not _image_to_video and not _kling_customize:
        if not prompt or not str(prompt).strip():
            print(f"模型 {model} 必须提供非空的生成提示词 (prompt)", file=sys.stderr)
            return None

    # Runtime availability check: consumeSource/list 可能随时将模型切成 hiddenState=1
    if not check_model_available(model):
        return None

    # Apply per-model length caps (truncate with warning, match frontend maxlength)
    restriction = VIDEO_RESTRICTIONS.get(model, {})
    prompt = _check_text_length(prompt, restriction.get("textLength"), "prompt", model)
    if negative_prompt is not None:
        negative_prompt = _check_text_length(
            negative_prompt, restriction.get("negativeTextLength"),
            "negativePrompt", model,
        )

    config = MODEL_CONFIGS[model]
    effective_ratio = ratio or config.get("default_ratio", "16:9")
    effective_resolution = resolution or config.get("default_resolution", "720p")
    effective_duration = duration or config.get("default_duration", 10)

    # Validate ratio / resolution / generationType against per-model whitelists.
    if model in VIDEO_RATIOS:
        effective_ratio = _coerce_value(
            effective_ratio, VIDEO_RATIOS[model],
            config.get("default_ratio", "16:9"), "ratio", model,
        )
    if model in VIDEO_RESOLUTIONS:
        effective_resolution = _coerce_value(
            effective_resolution, VIDEO_RESOLUTIONS[model],
            config.get("default_resolution", "720p"), "resolution", model,
        )
    if generation_type is not None and model in VIDEO_GENERATION_TYPES:
        generation_type = _coerce_value(
            generation_type, VIDEO_GENERATION_TYPES[model],
            VIDEO_GENERATION_TYPES[model][0], "generationType", model,
        )

    parameter = dict(config["extra_params"])  # copy defaults

    # Resolve pixel size from ratio + resolution
    resolution_size_map = {
        ("16:9", "720p"): "1280x720",
        ("16:9", "1080p"): "1920x1080",
        ("9:16", "720p"): "720x1280",
        ("9:16", "1080p"): "1080x1920",
        ("1:1", "720p"): "720x720",
        ("1:1", "1080p"): "1080x1080",
        ("3:4", "720p"): "720x960",
        ("3:4", "1080p"): "1080x1440",
        ("4:3", "720p"): "960x720",
        ("4:3", "1080p"): "1440x1080",
    }
    pixel_size = resolution_size_map.get((effective_ratio, effective_resolution), effective_ratio)

    parameter.update({
        "methodType": config["methodType"],
        "text": prompt,
        "resolution": effective_resolution,
        "ratio": effective_ratio,
        "size": pixel_size,
        "duration": effective_duration,
    })

    # --- Duration rules (aligned with frontend `matchVideoDurationInfo`) ---
    # V3.1FB (mt=3), V3.1PB (mt=4): fixed 8 seconds
    if model in ["V3.1FB", "V3.1PB"]:
        if effective_duration != 8:
            print(f"{model} 时长固定为 8 秒，当前 {effective_duration} 秒，自动调整为 8 秒")
            effective_duration = 8
            parameter["duration"] = effective_duration
        parameter["size"] = effective_ratio

    # V3.1Fast (mt=5): 4 or 8 seconds
    if model == "V3.1Fast":
        if effective_duration not in [4, 8]:
            print(f"{model} 时长必须是 4 或 8 秒，当前 {effective_duration} 秒，自动调整为 8 秒")
            effective_duration = 8
            parameter["duration"] = effective_duration
        parameter["size"] = effective_ratio

    # WAN2.6 / WAN2.7 series & klingV3Omni: size + duration rules
    # Size format (per frontend): only W2.6t (mt=7) and W2.6r (mt=9) use '*'-separated pixels;
    # W2.6i, W2.7*, klingV3Omni all submit size = ratio string.
    wan_text_models = {"W2.6t", "W2.7t"}
    wan_image_models = {"W2.6i", "W2.7i"}
    wan_ref_models = {"W2.6r", "W2.7r"}
    wan_models = wan_text_models | wan_image_models | wan_ref_models
    pixel_size_models = {"W2.6t", "W2.6r"}  # only these use '1280*720' form

    if model in wan_models or model == "klingV3Omni":
        # Duration range
        if model == "W2.6r":
            min_d, max_d, default_d = 3, 10, 10
        elif model == "W2.7r" and video_url_list:
            # W2.7r with reference video(s): 3-10s (frontend videoUrlList?.length)
            min_d, max_d, default_d = 3, 10, 10
        else:
            # W2.6t/W2.6i, W2.7t/W2.7i, klingV3Omni, W2.7r (no ref video) → 3-15s
            min_d, max_d, default_d = 3, 15, 10
        if effective_duration < min_d or effective_duration > max_d:
            print(f"{model} 时长必须是 {min_d}-{max_d} 秒，当前 {effective_duration} 秒，自动调整为 {default_d} 秒")
            effective_duration = default_d
            parameter["duration"] = effective_duration

        # Size serialization
        if model in pixel_size_models:
            parameter["size"] = pixel_size.replace("x", "*")  # e.g., "1280*720"
        else:
            parameter["size"] = effective_ratio  # e.g., "16:9"

    # Image-to-video: auto-switch generationType based on first_image_url
    if model in wan_image_models and generation_type is None:
        parameter["generationType"] = "FIRST&LAST"

    # Reference-to-video: force REFERENCE generationType (W2.6r / W2.7r)
    if model in wan_ref_models:
        parameter["generationType"] = "REFERENCE"

    # Apply optional overrides
    if first_image_url is not None:
        parameter["firstImageUrl"] = first_image_url
    if last_image_url is not None:
        parameter["lastImageUrl"] = last_image_url
    if generate_audio is not None:
        parameter["generateAudio"] = generate_audio
    if scale_factor is not None:
        parameter["scaleFactor"] = scale_factor
    if generation_type is not None:
        parameter["generationType"] = generation_type
    if enhance_prompt is not None:
        parameter["enhancePrompt"] = enhance_prompt
    if prompt_extend is not None:
        parameter["promptExtend"] = prompt_extend
    # WAN series: audio_url, image_url_list, video_url_list
    if audio_url is not None:
        parameter["audioUrl"] = audio_url
    if image_url_list is not None:
        parameter["imageUrlList"] = image_url_list
    if video_url_list is not None:
        parameter["videoUrlList"] = video_url_list

    # Model-specific exclusives
    if mode is not None:
        parameter["mode"] = mode
    if keep_original_sound is not None:
        parameter["keepOriginalSound"] = keep_original_sound
    if shot_type is not None:
        parameter["shotType"] = shot_type
    if element_list is not None:
        parameter["elementList"] = element_list
    if first_clip_url is not None:
        parameter["firstClipUrl"] = first_clip_url
    if multi_shot is not None:
        parameter["multiShot"] = multi_shot
    if n is not None:
        parameter["n"] = n
    if person_generation is not None:
        parameter["personGeneration"] = person_generation
    if resize_mode is not None:
        parameter["resizeMode"] = resize_mode
    if negative_prompt is not None:
        parameter["negativePrompt"] = negative_prompt
    if duration_switch is not None:
        parameter["durationSwitch"] = duration_switch
    if multi_prompt is not None:
        parameter["multiPrompt"] = multi_prompt

    # klingV3Omni customize shotType requires multiPrompt
    if model == "klingV3Omni" and parameter.get("shotType") == "customize" \
            and not parameter.get("multiPrompt"):
        print(
            "klingV3Omni shotType='customize' 需要传入 multi_prompt（分镜列表），"
            "当前为空，可能会被 API 拒绝",
            file=sys.stderr,
        )

    # klingV3Omni-specific serialization (mirrors frontend `buildNewParams`):
    #   - shotType 'multi' must be emitted as 'intelligence'
    #   - firstClipUrl + keep_original_sound are packed into a `videoList` array
    #     whose `refer_type` depends on generationType (base for EDIT, feature
    #     for FEATURE). generateAudio is disabled when a reference clip is given.
    if model == "klingV3Omni":
        if parameter.get("shotType") == "multi":
            parameter["shotType"] = "intelligence"

        clip_url = parameter.pop("firstClipUrl", None)
        if clip_url:
            gen_type = parameter.get("generationType")
            refer_type = "base" if gen_type == "EDIT" else "feature"
            parameter["videoList"] = [{
                "video_url": clip_url,
                "refer_type": refer_type,
                "keep_original_sound": parameter.get("keepOriginalSound", "yes"),
            }]
            # When a reference clip is supplied, mute generated audio (frontend rule)
            parameter["generateAudio"] = False

    # Reapply the text length-capped prompt / negativePrompt
    parameter["text"] = prompt
    if negative_prompt is not None:
        parameter["negativePrompt"] = negative_prompt

    # Overwrite targetMaxSize / targetMinLength / targetMaxLength per model
    _apply_restriction(parameter, restriction)

    # Strip fields this model does not accept (mirrors frontend visibility rules)
    _filter_by_whitelist(parameter, model, VIDEO_FIELD_SUPPORT)

    payload = {
        "type": config["type"],
        "methodType": config["methodType"],
        "parameter": json.dumps(parameter)
    }

    if DRY_RUN:
        _progress("[dry-run] 视频任务 payload（未提交）:")
        _progress(json.dumps(payload, ensure_ascii=False, indent=2))
        return "DRY_RUN_TASK_ID"

    if not estimate_generation_cost(payload):
        return None

    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=30)
        response.raise_for_status()
        result = response.json()

        if result.get("code") == 200 and result.get("data"):
            return result["data"][0]
        else:
            print(f"创建视频任务失败：{result.get('msg', '未知错误')}", file=sys.stderr)
            return None

    except requests.exceptions.HTTPError as e:
        print(_explain_http_error(e, context="创建视频任务"), file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"网络错误：{e}", file=sys.stderr)
        return None


def generate_video(prompt, model="V3.1FB", ratio=None, resolution=None,
                   duration=None, poll_interval=5, first_image_url=None,
                   last_image_url=None, generate_audio=None, scale_factor=None,
                   generation_type=None, enhance_prompt=None, prompt_extend=None,
                   first_image_path=None, last_image_path=None, audio_url=None,
                   image_url_list=None, video_url_list=None, audio_path=None,
                   mode=None, keep_original_sound=None, shot_type=None,
                   element_list=None, first_clip_url=None, multi_shot=None,
                   n=None, person_generation=None, resize_mode=None,
                   negative_prompt=None, duration_switch=None,
                   multi_prompt=None, max_wait=1200):
    """Generate a video from a text prompt.

    Args:
        prompt: Text description of the video
        model: Video model key (e.g. S1.5Pro, V3.1FB, V3.1PB, V3.1Fast,
               W2.6t, W2.6i, W2.6r, klingV3Omni, W2.7i, W2.7t, W2.7r)
        ratio: Aspect ratio (e.g. '16:9')
        resolution: Video resolution (e.g. '720p')
        duration: Video duration in seconds
        poll_interval: Polling interval in seconds
        first_image_url: URL of the first frame image (FIRST&LAST mode)
        last_image_url: URL of the last frame image (FIRST&LAST mode)
        generate_audio: Whether to generate audio
        scale_factor: Optional scaleFactor override
        generation_type: Generation type override
        enhance_prompt: Whether to enhance the prompt
        prompt_extend: Whether to extend the prompt
        first_image_path: Local path to first frame image (auto-uploaded)
        last_image_path: Local path to last frame image (auto-uploaded)
        audio_url: URL of audio file (WAN series)
        audio_path: Local path to audio file (auto-uploaded, WAN series)
        image_url_list: List of image URLs for reference (WAN *r / multimodal)
        video_url_list: List of video URLs for reference (WAN *r)

    Returns:
        dict with 'status', 'url', 'message'
    """
    # Upload local files to get URLs if provided
    if first_image_path and not first_image_url:
        first_image_url = upload_file(first_image_path)
    if last_image_path and not last_image_url:
        last_image_url = upload_file(last_image_path)
    if audio_path and not audio_url:
        audio_url = upload_file(audio_path)
    
    config = MODEL_CONFIGS.get(model, {})
    effective_ratio = ratio or config.get("default_ratio", "16:9")
    effective_resolution = resolution or config.get("default_resolution", "720p")
    effective_duration = duration or config.get("default_duration", 10)

    _progress(f"正在生成视频：{prompt}")
    _progress(f"   模型：{model} | 分辨率：{effective_resolution} | 比例：{effective_ratio} | 时长：{effective_duration}s")
    if first_image_url:
        _progress(f"   首帧图片：{first_image_url}")
    if last_image_url:
        _progress(f"   尾帧图片：{last_image_url}")
    if audio_url:
        _progress(f"   音频：{audio_url}")
    if image_url_list:
        _progress(f"   参考图片：{image_url_list}")
    if video_url_list:
        _progress(f"   参考视频：{video_url_list}")

    task_id = create_video_task(
        prompt, model, ratio, resolution, duration,
        first_image_url=first_image_url,
        last_image_url=last_image_url,
        generate_audio=generate_audio,
        scale_factor=scale_factor,
        generation_type=generation_type,
        enhance_prompt=enhance_prompt,
        prompt_extend=prompt_extend,
        audio_url=audio_url,
        image_url_list=image_url_list,
        video_url_list=video_url_list,
        mode=mode,
        keep_original_sound=keep_original_sound,
        shot_type=shot_type,
        element_list=element_list,
        first_clip_url=first_clip_url,
        multi_shot=multi_shot,
        n=n,
        person_generation=person_generation,
        resize_mode=resize_mode,
        negative_prompt=negative_prompt,
        duration_switch=duration_switch,
        multi_prompt=multi_prompt,
    )
    if not task_id:
        return None

    _progress(f"   任务 ID: {task_id}")
    _progress(f"   开始轮询任务结果（间隔 {poll_interval}s，最长等待 {max_wait}s）…")

    result = poll_task_status(task_id, interval=poll_interval, max_wait=max_wait)

    if result and result["status"] == "SUCCESS":
        _progress(f"视频生成成功！链接：{result['url']}")
    else:
        print(f"视频生成失败：{result.get('message', '未知错误')}", file=sys.stderr)

    return result


def create_generation_task(prompt, quality="2K", size=None, model="3.1Nano2-Evo",
                           reference_image_url=None, web_search=None,
                           image_search=None, ratiocination=None, n=None):
    """Create an image generation task.

    Args:
        prompt: Text description of the image
        quality: Image quality (2K/4K)
        size: Image dimensions. S5.0L / W2.7 / W2.7Pro use e.g. '2048x2048';
              N2 / 3.1Nano2-Evo / Nano2-Beta-Evo use e.g. '1:1';
              Image2 / Image2-Beta-Evo use 'auto' or a ratio string (e.g. '1:1').
        model: Image model key (N2, S5.0L, W2.7, W2.7Pro, 3.1Nano2-Evo,
               Nano2-Beta-Evo, Image2, Image2-Beta-Evo)
        reference_image_url: Optional reference image URL for image-to-image generation
        web_search: Toggle webSearch (S5.0L / 3.1Nano2-Evo)
        image_search: Toggle imageSearch (3.1Nano2-Evo only)
        ratiocination: Render-quality preset for Image2 (low/medium/high)
        n: Image count for Image2 (1-10)
    """
    url = f"{BASE_URL}/AiArtistRecord"
    
    if model not in MODEL_CONFIGS:
        print(f"不支持的模型：{model}，可用模型：{list(MODEL_CONFIGS.keys())}", file=sys.stderr)
        return None

    # Image generation always requires a non-empty prompt (frontend: required rule)
    if not prompt or not str(prompt).strip():
        print(f"模型 {model} 必须提供非空的生成提示词 (prompt)", file=sys.stderr)
        return None

    # Runtime availability check: consumeSource/list 可能随时将模型切成 hiddenState=1
    if not check_model_available(model):
        return None

    # Apply per-model prompt length cap
    image_restriction = IMAGE_RESTRICTIONS.get(model, {})
    prompt = _check_text_length(prompt, image_restriction.get("textLength"), "prompt", model)

    config = MODEL_CONFIGS[model]

    # Validate quality against per-model whitelist (matchImageQualityOptions)
    if model in IMAGE_QUALITIES:
        quality = _coerce_value(
            quality, IMAGE_QUALITIES[model],
            config.get("default_quality", "2K"), "quality", model,
        )

    # Use model's default size if not specified
    if size is None:
        size = config["default_size"]
    else:
        # Validate ratio-style size (e.g. "16:9"); pixel sizes contain 'x' or '*'.
        is_pixel_size = ("x" in size and any(c.isdigit() for c in size.split("x")[0])) \
                        or ("*" in size and any(c.isdigit() for c in size.split("*")[0]))
        if not is_pixel_size and model in IMAGE_SIZE_EXCLUDED:
            excluded = IMAGE_SIZE_EXCLUDED[model]
            if size in excluded:
                print(
                    f"{model} 不支持 size={size!r}（被排除：{excluded}），"
                    f"自动调整为默认值 {config['default_size']!r}",
                    file=sys.stderr,
                )
                size = config["default_size"]
    
    # Build image array - support reference image for image-to-image
    image_array = []
    if reference_image_url:
        image_array = [reference_image_url]
    
    parameter = {
        "methodType": config["methodType"],
        "prompt": prompt,
        "image": image_array,
        "quality": quality,
        "size": size,
        "webSearch": bool(web_search) if web_search is not None else False,
        "targetMaxSize": 10,
        "targetMaxLength": 6000,
    }
    # Merge model-specific extra params (defaults for ratiocination / imageSearch / n etc.)
    parameter.update(config["extra_params"])

    # ----- Image2 / Nano2 explicit overrides from caller -----
    if image_search is not None:
        parameter["imageSearch"] = bool(image_search)
    if ratiocination is not None:
        ratiocination = _coerce_value(
            ratiocination, IMAGE_RATIOCINATION_OPTIONS,
            "medium", "ratiocination", model,
        )
        parameter["ratiocination"] = ratiocination
    if n is not None:
        try:
            n_int = int(n)
        except (TypeError, ValueError):
            print(f"{model} 参数 n={n!r} 非法，已忽略", file=sys.stderr)
            n_int = None
        if n_int is not None:
            if n_int < 1 or n_int > 10:
                print(
                    f"{model} n={n_int} 超出范围 [1,10]，已截断到合法区间",
                    file=sys.stderr,
                )
                n_int = max(1, min(10, n_int))
            parameter["n"] = n_int

    # Overwrite targetMaxSize / targetMinLength / targetMaxLength per model
    _apply_restriction(parameter, image_restriction)

    # Strip image fields this model does not accept (mirrors frontend rules)
    _filter_by_whitelist(parameter, model, IMAGE_FIELD_SUPPORT)

    payload = {
        "type": config["type"],
        "methodType": config["methodType"],
        "parameter": json.dumps(parameter)
    }

    if DRY_RUN:
        _progress("[dry-run] 图片任务 payload（未提交）:")
        _progress(json.dumps(payload, ensure_ascii=False, indent=2))
        return "DRY_RUN_TASK_ID"

    if not estimate_generation_cost(payload):
        return None

    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 200 and result.get("data"):
            return result["data"][0]
        else:
            print(f"创建任务失败：{result.get('msg', '未知错误')}", file=sys.stderr)
            return None

    except requests.exceptions.HTTPError as e:
        print(_explain_http_error(e, context="创建图片任务"), file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"网络错误：{e}", file=sys.stderr)
        return None


def poll_task_status(task_id, interval=5, max_wait=1200):
    """Poll the task status until completion or failure."""
    if task_id == "DRY_RUN_TASK_ID":
        return {"status": "SUCCESS", "url": None,
                "message": "dry-run 模式，未提交真实任务"}
    url = f"{BASE_URL}/AiArtistImage/getInfoByArtistId/{task_id}"
    
    elapsed = 0
    last_status = None
    
    while elapsed < max_wait:
        try:
            response = requests.get(url, headers=get_headers(), timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") != 200:
                time.sleep(interval)
                elapsed += interval
                continue
            
            data = result.get("data", {})
            status = data.get("status", "")
            
            # Only print status when it changes
            if status != last_status:
                _progress(f"{status} - {data.get('message', '')}")
                last_status = status
            
            if status == "SUCCESS":
                return {
                    "status": "SUCCESS",
                    "url": data.get("url"),
                    "message": data.get("message", "生成成功")
                }
            elif status == "FAILED":
                return {
                    "status": "FAILED",
                    "url": None,
                    "message": data.get("message", "生成失败")
                }
            else:
                time.sleep(interval)
                elapsed += interval
                
        except requests.exceptions.RequestException as e:
            print(f"查询状态出错：{e}", file=sys.stderr)
            time.sleep(interval)
            elapsed += interval
    
    return {
        "status": "TIMEOUT",
        "url": None,
        "message": f"超时（{max_wait}秒）"
    }


def generate_image(prompt, quality="2K", size=None, poll_interval=5,
                   download=False, output_dir=None, model="3.1Nano2-Evo",
                   reference_image_path=None, reference_image_url=None,
                   web_search=None, image_search=None, ratiocination=None,
                   n=None, max_wait=1200):
    """
    Main function to generate an image from a prompt.
    
    Args:
        prompt: Text description of the image
        quality: Image quality (2K/4K)
        size: Image dimensions. Defaults to model's default size if not specified.
              S5.0L / W2.7 / W2.7Pro: e.g. '2048x2048'
              N2 / 3.1Nano2-Evo / Nano2-Beta-Evo: e.g. '1:1'
        poll_interval: Polling interval in seconds
        download: Whether to download the image
        output_dir: Directory to save the image (default: workspace/images)
        model: Image model key (N2, S5.0L, W2.7, W2.7Pro, 3.1Nano2-Evo, Nano2-Beta-Evo)
        reference_image_path: Local path to reference image (auto-uploaded)
        reference_image_url: URL of reference image (if already uploaded)
    
    Returns:
        dict with generation result including 'url', 'local_path', 'data_uri' if successful
    """
    config = MODEL_CONFIGS.get(model, {})
    effective_size = size or config.get("default_size", "2048x2048")

    # Upload reference image if local path provided
    if reference_image_path and not reference_image_url:
        reference_image_url = upload_file(reference_image_path)

    _progress(f"正在生成：{prompt}")
    _progress(f"   模型：{model} | 质量：{quality} | 尺寸：{effective_size}")
    if reference_image_url:
        _progress(f"   参考图：{reference_image_url}")

    # Step 1: Create task
    task_id = create_generation_task(
        prompt, quality, size, model, reference_image_url,
        web_search=web_search,
        image_search=image_search,
        ratiocination=ratiocination,
        n=n,
    )
    if not task_id:
        return None

    _progress(f"   任务 ID: {task_id}")
    _progress(f"   开始轮询任务结果（间隔 {poll_interval}s，最长等待 {max_wait}s）…")

    # Step 2: Poll until complete
    result = poll_task_status(task_id, interval=poll_interval, max_wait=max_wait)

    if result and result["status"] == "SUCCESS":
        _progress(f"生成成功！链接：{result['url']}")
        
        # Download image if requested
        if download and result.get("url"):
            if not output_dir:
                output_dir = os.path.join(os.path.expanduser("~"), ".openclaw", "workspace", "images")
            
            # Generate filename from prompt
            safe_prompt = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in prompt)
            safe_prompt = safe_prompt[:50].strip().replace(' ', '_')
            filename = f"{safe_prompt}_{int(time.time())}.png"
            output_path = os.path.join(output_dir, filename)
            
            image_data = download_image(result["url"], output_path)
            if image_data:
                result["local_path"] = output_path
                result["data_uri"] = image_to_data_uri(image_data)
                result["image_data"] = image_data  # Raw bytes for programmatic use
        
        return result
    else:
        print(f"生成失败：{result.get('message', '未知错误')}", file=sys.stderr)
        return result


if __name__ == "__main__":
    # Check API key before proceeding
    check_api_key()

    image_models = [k for k, v in MODEL_CONFIGS.items() if v["media_type"] == "image"]
    video_models = [k for k, v in MODEL_CONFIGS.items() if v["media_type"] == "video"]
    all_models = list(MODEL_CONFIGS.keys())

    parser = argparse.ArgumentParser(
        description="AI 图片/视频生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"图片模型：{', '.join(image_models)}\n视频模型：{', '.join(video_models)}"
    )
    parser.add_argument("prompt", nargs="?", default=None,
                        help="生成提示词（使用 --list-models 时可省略）")
    parser.add_argument("--list-models", action="store_true",
                        help="列出当前服务端激活的可用模型 (hiddenState=0) 后退出")
    parser.add_argument("--model", default=None,
                        choices=all_models,
                        help="生成模型。未指定时根据 prompt 自动推断：视频关键词 → V3.1FB，其余 → 3.1Nano2-Evo")
    # 图片专属参数
    parser.add_argument("--quality", default="2K", help="[图片] 图片质量 (默认：2K)")
    parser.add_argument("--size", default=None, help="[图片] 图片尺寸，不传则使用模型默认值")
    parser.add_argument("--download", action="store_true", help="[图片] 下载图片到本地")
    parser.add_argument("--output-dir", help="[图片] 图片保存目录")
    parser.add_argument("--markdown-output", action="store_true", help="以 Markdown 格式输出图片链接")
    parser.add_argument("--reference-image", default=None, help="[图片] 参考图本地路径，自动上传后作为 image-to-image 参考")
    parser.add_argument("--reference-image-url", default=None, help="[图片] 已上传的参考图 URL")
    parser.add_argument("--web-search", dest="web_search", action="store_true", default=None,
                        help="[图片] 启用联网搜索 (仅 S5.0L / 3.1Nano2-Evo)")
    parser.add_argument("--no-web-search", dest="web_search", action="store_false",
                        help="[图片] 关闭联网搜索")
    parser.add_argument("--image-search", dest="image_search", action="store_true", default=None,
                        help="[图片] 启用图像搜索 (仅 3.1Nano2-Evo)")
    parser.add_argument("--no-image-search", dest="image_search", action="store_false",
                        help="[图片] 关闭图像搜索")
    parser.add_argument("--ratiocination", default=None,
                        choices=["low", "medium", "high"],
                        help="[图片] 渲染质量预设 (仅 Image2)：low=最快 / medium=平衡 / high=质量")
    # 视频专属参数
    parser.add_argument("--ratio", default=None, help="[视频] 画面比例，如 16:9、9:16、1:1 (默认：16:9)")
    parser.add_argument("--resolution", default=None, help="[视频] 分辨率，如 720p、1080p (默认：720p)")
    parser.add_argument("--duration", type=int, default=None, help="[视频] 视频时长 (秒) (默认：10)")
    # 视频通用参数（首尾帧 / 音频 / 生成模式）
    parser.add_argument("--first-image-url", default=None, help="[视频] 首帧图片 URL（FIRST&LAST 模式）")
    parser.add_argument("--last-image-url", default=None, help="[视频] 尾帧图片 URL（FIRST&LAST 模式）")
    parser.add_argument("--first-image", default=None, help="[视频] 首帧图片本地路径，自动上传")
    parser.add_argument("--last-image", default=None, help="[视频] 尾帧图片本地路径，自动上传")
    parser.add_argument("--generate-audio", action="store_true", default=None, help="[视频] 生成音频")
    parser.add_argument("--no-audio", action="store_true", help="[视频] 不生成音频")
    parser.add_argument("--scale-factor", type=float, default=None, help="[视频] 可选 scaleFactor 覆盖值")
    parser.add_argument("--generation-type", default=None, help="[视频] 生成类型，如 FIRST&LAST、TEXT、REFERENCE、CONTINUATION、EDIT、FEATURE")
    parser.add_argument("--negative-prompt", default=None, help="[视频] 反向提示词 (V3.1Fast/Wan系列)")
    parser.add_argument("--enhance-prompt", action="store_true", default=None, help="[视频] 翻译成英文 (V3.1 系列)")
    parser.add_argument("--prompt-extend", action="store_true", default=None, help="[视频] 智能改写 (Wan 系列)")
    parser.add_argument("--shot-type", default=None, help="[视频] 镜头模式：single/multi/customize (Wan2.6/klingV3Omni)")
    parser.add_argument("--mode", default=None, help="[视频] 生成模式：std/pro (仅 klingV3Omni)")
    parser.add_argument("--keep-original-sound", default=None, help="[视频] yes/no (仅 klingV3Omni)")
    parser.add_argument("--multi-shot", action="store_true", default=None, help="[视频] 多镜头模式 (仅 klingV3Omni)")
    parser.add_argument("--n", type=int, default=None,
                        help="[视频] 生成数量 1-4 (仅 V3.1Fast) | [图片] 生成数量 1-10 (仅 Image2)")
    parser.add_argument("--person-generation", default=None, help="[视频] allow_adult/dont_allow (仅 V3.1Fast)")
    parser.add_argument("--resize-mode", default=None, help="[视频] pad/crop (仅 V3.1Fast)")
    parser.add_argument("--duration-switch", default=None, help="[视频] 1=手选秒数, 2=智能时长 (仅 S1.5Pro)")
    # 通用参数
    parser.add_argument("--interval", type=int, default=5, help="轮询间隔秒数")
    parser.add_argument("--max-wait", type=int, default=1200, help="任务轮询最长等待秒数 (默认 1200)")
    parser.add_argument("--dry-run", action="store_true",
                        help="仅构建并打印最终 payload，不实际调用 API（用于调试）")
    parser.add_argument("--json-output", action="store_true",
                        help="以单行 JSON 向 stdout 输出最终结果 {status,url,message}，便于外部编排解析")

    args = parser.parse_args()

    # --list-models short-circuit
    if args.list_models:
        print_active_models()
        sys.exit(0)

    if not args.prompt:
        parser.error("prompt 为必填参数（查看可用模型请加 --list-models）")

    # Toggle dry-run globally so all downstream task creators honor it
    if args.dry_run:
        DRY_RUN = True

    # Auto-select default model when the user did NOT pass --model explicitly
    if args.model is None:
        inferred = _infer_media_type(args.prompt)
        args.model = "V3.1FB" if inferred == "video" else "3.1Nano2-Evo"
        print(f"[auto] 根据提示词推断媒介 → {inferred}，使用默认模型 {args.model}",
              file=sys.stderr)

    media_type = MODEL_CONFIGS[args.model]["media_type"]

    if media_type == "video":
        # Resolve audio flag
        gen_audio = None
        if args.no_audio:
            gen_audio = False
        elif args.generate_audio:
            gen_audio = True

        result = generate_video(
            prompt=args.prompt,
            model=args.model,
            ratio=args.ratio,
            resolution=args.resolution,
            duration=args.duration,
            poll_interval=args.interval,
            first_image_url=args.first_image_url,
            last_image_url=args.last_image_url,
            first_image_path=args.first_image,
            last_image_path=args.last_image,
            generate_audio=gen_audio,
            scale_factor=args.scale_factor,
            generation_type=args.generation_type,
            negative_prompt=args.negative_prompt,
            enhance_prompt=args.enhance_prompt,
            prompt_extend=args.prompt_extend,
            shot_type=args.shot_type,
            mode=args.mode,
            keep_original_sound=args.keep_original_sound,
            multi_shot=args.multi_shot,
            n=args.n,
            person_generation=args.person_generation,
            resize_mode=args.resize_mode,
            duration_switch=args.duration_switch,
            max_wait=args.max_wait,
        )
        # Send result to Feishu if webhook is configured
        if FEISHU_WEBHOOK_URL:
            send_feishu_message(args.prompt, result, media_type="video")
        _emit_cli_result(result, args, markdown_label=args.prompt)
        sys.exit(0 if (result and result.get("status") == "SUCCESS") else 1)
    else:
        result = generate_image(
            prompt=args.prompt,
            quality=args.quality,
            size=args.size,
            poll_interval=args.interval,
            download=args.download,
            output_dir=args.output_dir,
            model=args.model,
            reference_image_path=args.reference_image,
            reference_image_url=args.reference_image_url,
            web_search=args.web_search,
            image_search=args.image_search,
            ratiocination=args.ratiocination,
            n=args.n,
            max_wait=args.max_wait
        )

        # Send result to Feishu if webhook is configured
        if FEISHU_WEBHOOK_URL:
            send_feishu_message(args.prompt, result, media_type="image")
        _emit_cli_result(result, args, markdown_label=args.prompt)
        sys.exit(0 if (result and result.get("status") == "SUCCESS") else 1)
