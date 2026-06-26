#!/usr/bin/env python3
"""Sora/Veo/Grok/豆包/Vidu 视频生成兼容入口。"""

import argparse
import json
import os
import socket
import sys
import urllib.error
import urllib.request
import uuid

from _config import first_env, load_env_file, resolve_env_file_from_argv
from _logger import error_exit, print_json, warn
from _validators import check_reference_image, parse_json_array, parse_optional_bool, parse_positive_int

DEFAULT_MODEL = "sora-2"
DEFAULT_SIZE = "720x1280"
DEFAULT_TIMEOUT = 180
DEFAULT_ENV_FILE = ".env"
KNOWN_SIZES = {
    "720x1280",
    "1280x720",
    "720P",
    "1080P",
    "16:9",
    "4:3",
    "1:1",
    "3:4",
    "9:16",
    "21:9",
    "keep_ratio",
    "adaptive",
    "720p",
    "1080p",
}


def resolve_provider_from_model(model: str) -> str:
    text = (model or "").strip().lower()
    if text.startswith("doubao") or text.startswith("seedance"):
        return "doubao"
    if text.startswith("veo"):
        return "veo"
    if text.startswith("sora"):
        return "sora"
    if text.startswith("grok") or text.startswith("viduq"):
        return "grok"
    if "vidu" in text:
        return "vidu"
    return ""


def provider_priority(provider: str):
    provider = (provider or "").strip().lower()
    if provider == "vidu":
        return ["VIDU", "SORA", "DOUBAO", "VEO", "GROK"]
    if provider == "doubao":
        return ["DOUBAO", "SORA", "VIDU", "VEO", "GROK"]
    if provider == "veo":
        return ["VEO", "SORA", "VIDU", "DOUBAO", "GROK"]
    if provider == "grok":
        return ["GROK", "SORA", "VIDU", "DOUBAO", "VEO"]
    return ["SORA", "VEO", "VIDU", "DOUBAO", "GROK"]


def env_by_provider(provider: str, suffix: str, default: str = "", include_video: bool = False) -> str:
    names = [f"{prefix}_{suffix}" for prefix in provider_priority(provider)]
    if include_video:
        names.append(f"VIDEO_{suffix}")
    return first_env(*names, default=default)


def build_multipart_body(fields: dict, files: list):
    boundary = f"----SoraVideoBoundary{uuid.uuid4().hex}"
    parts = []

    for key, value in fields.items():
        if value in (None, ""):
            continue
        if isinstance(value, bool):
            value = "true" if value else "false"
        parts.append(f"--{boundary}\r\n".encode("utf-8"))
        parts.append(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"))
        parts.append(str(value).encode("utf-8"))
        parts.append(b"\r\n")

    for field_name, file_path, mime_type in files:
        filename = os.path.basename(file_path)
        parts.append(f"--{boundary}\r\n".encode("utf-8"))
        parts.append(
            (
                f'Content-Disposition: form-data; name="{field_name}"; '
                f'filename="{filename}"\r\n'
            ).encode("utf-8")
        )
        parts.append(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
        with open(file_path, "rb") as f:
            parts.append(f.read())
        parts.append(b"\r\n")

    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(parts), boundary


def extract_video_url(payload: dict) -> str:
    """提取视频地址，兼容 Sora/Veo/Grok/豆包/Vidu 常见返回字段。"""

    preferred_keys = {"video_url", "videoUrl", "url", "output"}

    def walk(obj):
        if isinstance(obj, dict):
            for key in preferred_keys:
                value = obj.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()
            for value in obj.values():
                nested = walk(value)
                if nested:
                    return nested
        elif isinstance(obj, list):
            for item in obj:
                nested = walk(item)
                if nested:
                    return nested
        return ""

    return walk(payload)


def pick_task_payload(payload: dict) -> dict:
    """提取任务主体，兼容 data 包裹和顶层直出两种结构。"""

    if not isinstance(payload, dict):
        return {}

    data = payload.get("data")
    if isinstance(data, dict) and ("id" in data or "task_id" in data or "status" in data):
        return data
    return payload


def post_generate_multipart(base_url: str, api_key: str, body: bytes, boundary: str, timeout: int) -> dict:
    url = f"{base_url.rstrip('/')}/v1/videos"
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            if not raw.strip():
                error_exit("视频 API 返回空响应")
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                error_exit(f"视频 API 返回非 JSON：{raw[:500]}")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else ""
        error_exit(f"API 错误 {e.code}: {err_body}")
    except (TimeoutError, socket.timeout) as e:
        error_exit(f"请求超时（{timeout}s）：{e}")
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            error_exit(f"请求超时（{timeout}s）：{e.reason}")
        error_exit(f"网络错误: {e.reason}")


def post_generate_vidu(base_url: str, api_key: str, payload: dict, timeout: int) -> dict:
    url = f"{base_url.rstrip('/')}/v1/video/generations"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            if not raw.strip():
                error_exit("Vidu API 返回空响应")
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                error_exit(f"Vidu API 返回非 JSON：{raw[:500]}")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else ""
        error_exit(f"API 错误 {e.code}: {err_body}")
    except (TimeoutError, socket.timeout) as e:
        error_exit(f"请求超时（{timeout}s）：{e}")
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            error_exit(f"请求超时（{timeout}s）：{e.reason}")
        error_exit(f"网络错误: {e.reason}")


def main():
    cli_argv = sys.argv[1:]
    env_file = resolve_env_file_from_argv(cli_argv)
    load_env_file(env_file)

    provider_hint = (os.environ.get("VIDEO_PROVIDER_HINT") or "").strip().lower()

    parser = argparse.ArgumentParser(
        description="调用 Sora/Veo/Grok/豆包/Vidu 视频生成接口",
        epilog="""
环境变量:
    API_KEY       必填，Bearer 鉴权
    API_BASE_URL  必填，接口域名，如 https://xxxxx

示例:
  # 文生视频
  python3 sora_generate_video.py "猫咪听歌摇头晃脑，下大雨" --model sora-2 --seconds 10

    # Grok 视频
    python3 sora_generate_video.py "猫咪听歌摇头晃脑，下大雨" --model grok-video --size 720P --aspect-ratio 2:3 --seconds 10

    # 豆包视频
    python3 sora_generate_video.py "猫咪听歌摇头晃脑，下大雨" --model doubao-seedance-1-5-pro_720p --size 16:9 --seconds 4

    # Vidu 视频（JSON 接口）
    python3 sora_generate_video.py "一个美女在雨中跳舞" --model TC-vidu-q3-turbo --size 720p --seconds 5 --aspect-ratio 16:9

  # 图生视频（支持多张参考图）
  python3 sora_generate_video.py "猫咪带耳机走路" --input-reference ./cat1.jpg ./cat2.png --seconds 10
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--env-file",
        default=env_file,
        help="环境变量文件路径（默认 .env）",
    )
    parser.add_argument("prompt", help="视频提示词")
    parser.add_argument(
        "--model",
        default=env_by_provider(provider_hint, "MODEL", default=DEFAULT_MODEL),
        help="模型名称（如 sora-2、veo_3_1-fast）",
    )
    parser.add_argument(
        "--size",
        default="",
        help="视频尺寸，常用 720x1280 或 1280x720",
    )
    parser.add_argument(
        "--seconds",
        default="",
        help="视频秒数（Veo 建议 8，Sora 常见 10 或 15）",
    )
    parser.add_argument(
        "--enable-upsample",
        default="",
        help="是否开启高清增强（Veo 文档字段，true/false）",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="",
        help="视频比例（Grok 常见 2:3、3:2、1:1）",
    )
    parser.add_argument(
        "--first-frame-image",
        default="",
        help="首帧图片（豆包字段，通常传 URL）",
    )
    parser.add_argument(
        "--last-frame-image",
        default="",
        help="尾帧图片（豆包字段，通常传 URL）",
    )
    parser.add_argument(
        "--input-reference",
        nargs="+",
        default=[],
        help="参考图片路径（传入后即图生视频，可多张）",
    )
    parser.add_argument(
        "--image-urls",
        nargs="+",
        default=[],
        help="图片 URL 列表（Vidu 用于图生/首尾帧生视频）",
    )
    parser.add_argument(
        "--character-url",
        default=os.environ.get("SORA_CHARACTER_URL", ""),
        help="角色视频 URL（可选）",
    )
    parser.add_argument(
        "--character-timestamps",
        default=os.environ.get("SORA_CHARACTER_TIMESTAMPS", ""),
        help="角色出现秒数范围，格式 start,end（可选）",
    )
    parser.add_argument("--vidu-action", default="", help="Vidu metadata.action，可选 textGenerate/generate/firstTailGenerate/referenceGenerate")
    parser.add_argument("--off-peak", default="", help="Vidu metadata.off_peak，true/false")
    parser.add_argument("--callback-url", default="", help="Vidu metadata.callback_url")
    parser.add_argument("--subjects-json", default="", help="Vidu metadata.subjects JSON 数组字符串")
    parser.add_argument(
        "--base-url",
        default="",
        help="接口域名，不带 /v1/videos，例如 https://xxxxx",
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="Bearer Token（不需要填写 Bearer 前缀）",
    )
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="请求超时秒数（默认 180）")
    parser.add_argument("--raw", action="store_true", help="输出原始响应")
    args = parser.parse_args()

    provider = resolve_provider_from_model(args.model) or provider_hint
    size_default = "720p" if provider == "vidu" else DEFAULT_SIZE
    args.size = args.size or env_by_provider(provider, "SIZE", default=size_default)
    args.seconds = args.seconds or env_by_provider(provider, "SECONDS", default="")
    if provider == "vidu" and not args.seconds:
        args.seconds = env_by_provider(provider, "DURATION", default="")
    args.enable_upsample = args.enable_upsample or env_by_provider(provider, "ENABLE_UPSAMPLE", default="")
    args.aspect_ratio = args.aspect_ratio or env_by_provider(provider, "ASPECT_RATIO", default="")
    args.first_frame_image = args.first_frame_image or env_by_provider(provider, "FIRST_FRAME_IMAGE", default="")
    args.last_frame_image = args.last_frame_image or env_by_provider(provider, "LAST_FRAME_IMAGE", default="")
    args.vidu_action = args.vidu_action or env_by_provider(provider, "ACTION", default="")
    args.off_peak = args.off_peak or env_by_provider(provider, "OFF_PEAK", default="")
    args.callback_url = args.callback_url or env_by_provider(provider, "CALLBACK_URL", default="")
    args.subjects_json = args.subjects_json or env_by_provider(provider, "SUBJECTS_JSON", default="")
    args.base_url = args.base_url or os.environ.get("API_BASE_URL", "")
    args.api_key = args.api_key or os.environ.get("API_KEY", "")

    if not args.base_url:
        error_exit("请通过 --base-url 或 API_BASE_URL 提供接口域名")
    if not args.api_key:
        error_exit("请通过 --api-key 或 API_KEY 提供 API Key")

    seconds = parse_positive_int(args.seconds, "seconds")
    enable_upsample = parse_optional_bool(args.enable_upsample, "enable-upsample")
    off_peak = parse_optional_bool(args.off_peak, "off-peak")
    subjects = parse_json_array(args.subjects_json, "subjects-json")
    model_name = (args.model or "").strip().lower()

    if model_name.startswith("veo") and seconds is None:
        seconds = 8
    if model_name.startswith("veo") and seconds != 8:
        warn("Veo 文档说明 seconds 建议使用 8，当前将按你的传参继续请求")

    if provider == "grok" and seconds is None:
        seconds = 10

    if provider == "doubao" and seconds is None:
        seconds = 4

    if provider == "vidu":
        if seconds is None:
            seconds = 5
        if not 1 <= seconds <= 10:
            warn("Vidu 文档建议 duration 在 1-10 秒，当前将按你的传参继续请求")
        if args.input_reference:
            error_exit("Vidu 接口请使用 --image-urls 传图片 URL；--input-reference 本地文件仅适用于 multipart 接口")

    if enable_upsample is True and args.size != "1280x720":
        print(
            "警告：Veo 的 enable_upsample 通常仅适用于横屏 1280x720，当前将按你的传参继续请求",
            file=sys.stderr,
        )

    if args.size and args.size not in KNOWN_SIZES:
        print(
            f"警告：size={args.size} 不在文档常见值 {sorted(KNOWN_SIZES)} 中，仍将继续请求",
            file=sys.stderr,
        )

    if provider == "vidu":
        vidu_payload = {
            "model": args.model,
            "prompt": args.prompt,
            "duration": seconds,
            "size": args.size,
        }
        if args.image_urls:
            vidu_payload["images"] = args.image_urls

        metadata = {}
        if args.vidu_action:
            metadata["action"] = args.vidu_action
        if args.aspect_ratio:
            metadata["aspect_ratio"] = args.aspect_ratio
        if off_peak is not None:
            metadata["off_peak"] = off_peak
        if args.callback_url:
            metadata["callback_url"] = args.callback_url
        if subjects:
            metadata["subjects"] = subjects
        if metadata:
            vidu_payload["metadata"] = metadata

        payload = post_generate_vidu(args.base_url, args.api_key, vidu_payload, args.timeout)
    else:
        files = []
        for image_path in args.input_reference:
            mime_type = check_reference_image(image_path)
            files.append(("input_reference", image_path, mime_type))

        fields = {
            "model": args.model,
            "prompt": args.prompt,
            "size": args.size,
            "aspect_ratio": args.aspect_ratio,
            "seconds": seconds,
            "enable_upsample": enable_upsample,
            "first_frame_image": args.first_frame_image,
            "last_frame_image": args.last_frame_image,
            "character_url": args.character_url,
        }

        body, boundary = build_multipart_body(fields, files)
        payload = post_generate_multipart(args.base_url, args.api_key, body, boundary, args.timeout)

    task = pick_task_payload(payload)
    task_id = (
        task.get("id")
        or task.get("task_id")
        or payload.get("id")
        or payload.get("task_id")
        or ""
    )
    status = task.get("status") or payload.get("status") or ""
    progress = task.get("progress", payload.get("progress", 0))
    video_url = extract_video_url(payload)

    out = {
        "id": task_id,
        "object": task.get("object", payload.get("object", "")),
        "model": task.get("model", payload.get("model", args.model)),
        "status": status,
        "progress": progress,
        "created_at": task.get("created_at", payload.get("created_at", None)),
        "size": task.get("size", payload.get("size", args.size)),
    }
    seconds_out = task.get("seconds", payload.get("seconds", seconds))
    if seconds_out not in (None, ""):
        out["seconds"] = seconds_out
    if video_url:
        out["video_url"] = video_url
    if args.raw:
        out["raw"] = payload

    if not out["id"] and "videoUrl" not in out:
        out["hint"] = "未解析到任务 id，请开启 --raw 检查返回结构"
        print_json(out)
        sys.exit(1)

    print_json(out)


if __name__ == "__main__":
    main()
