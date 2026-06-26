#!/usr/bin/env python3
"""
LinkFoxAI CLI - Call LinkFox AI Open Platform APIs.

Auth: LINKFOXAI_APP_ID + LINKFOXAI_APP_SECRET (sign) or LINKFOXAI_API_KEY (Bearer).
Base URL: https://sbappstoreapi.ziniao.com/openapi-router (or set LINKFOXAI_BASE_URL).

Commands:
    material-list   --type 1                                     # 作图素材（连通性测试）
    upload-base64   --file image.png                             # base64 上传
    change-model    --image-url <url> --head-url <url> ...       # AI 换模特
    make-info       --id <task_id>                               # 查询作图结果（单次）
    poll            --id <task_id> [--interval 3] [--timeout 300]# 轮询作图结果直到完成
    cutout          --image-url <url> --sub-type 1               # 自动抠图
    scene-fission   --image-url <url> ...                        # 场景裂变
    expand-image    --image-url <url> --width 1024 --height 1024 # 智能扩图
    super-resolution --image-url <url> --magnification 2         # 高清放大
    image-edit      --image-url <url> --prompt "描述"             # 智能修图
    erase           --image-url <url> --mask-url <url>           # 消除笔
    sales-video     --prompt "文案" --video-type WAN|SEED         # 带货口播
    image-to-video  --image-url <url> --video-type SEED          # 图转视频
    product-material --image-list <url> ... --seller-point "卖点" # 商品套图V3
    wear-collection  --image-list <url> ... --seller-point "卖点" # 服装套图V2
    refresh         --id <image_id> [--format jpg]               # 刷新结果图片地址
    api-call        --path /linkfox-ai/... --body '{...}'        # 通用 API 调用
"""

import argparse
import base64
import hashlib
import json
import os
import sys
import time
import uuid
from datetime import date
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

DEFAULT_BASE_URL = "https://sbappstoreapi.ziniao.com/openapi-router"
PATH_PREFIX = "/linkfox-ai"
IMAGE_EDIT_V2_EFFECTIVE_DATE = date(2026, 3, 13)


def get_base_url() -> str:
    return os.environ.get("LINKFOXAI_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def get_credentials():
    app_id = os.environ.get("LINKFOXAI_APP_ID")
    app_secret = os.environ.get("LINKFOXAI_APP_SECRET")
    api_key = os.environ.get("LINKFOXAI_API_KEY")
    if app_id and app_secret:
        return app_id, app_secret, None
    if api_key:
        return None, None, api_key
    return None, None, None


def build_sign_headers(app_id: str, app_secret: str) -> dict:
    ts = str(int(time.time() * 1000))
    trace_id = uuid.uuid4().hex.upper()
    noce = uuid.uuid4().hex[:6].upper()
    raw = app_id + trace_id + ts + noce + app_secret
    sign = hashlib.sha256(raw.encode()).hexdigest().upper()
    return {
        "Content-Type": "application/json",
        "appId": app_id,
        "ts": ts,
        "traceId": trace_id,
        "noce": noce,
        "sign": sign,
        "User-Agent": "LinkFoxAI-Skill/1.0",
    }


def build_auth_headers() -> dict:
    app_id, app_secret, api_key = get_credentials()
    if app_id and app_secret:
        return build_sign_headers(app_id, app_secret)
    if api_key:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "LinkFoxAI-Skill/1.0",
        }
    print(
        "Error: Set LINKFOXAI_APP_ID + LINKFOXAI_APP_SECRET, or LINKFOXAI_API_KEY.\n"
        "See: https://open.ziniao.com",
        file=sys.stderr,
    )
    sys.exit(1)


def api_post(path: str, body: dict, timeout: int = 60) -> dict:
    base = get_base_url()
    url = base + path
    data = json.dumps(body).encode("utf-8")
    headers = build_auth_headers()
    req = Request(url, data=data, headers=headers, method="POST")
    try:
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        raw = e.read().decode("utf-8") if e.fp else ""
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"code": str(e.code), "msg": e.reason, "details": raw}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def extract_code(resp: dict):
    """Extract status code from nested open-platform response."""
    if "data" in resp and isinstance(resp["data"], dict):
        inner = resp["data"]
        if "code" in inner:
            return str(inner.get("code", ""))
    return str(resp.get("code", ""))


def is_success(resp: dict) -> bool:
    code = extract_code(resp)
    return code in ("200", "0")


def get_image_edit_path() -> str:
    """
    Resolve image-edit endpoint path.
    Priority:
    1) LINKFOXAI_IMAGE_EDIT_PATH override
       - full path: /linkfox-ai/image/v2/make/imageEdit
       - endpoint suffix: imageEdit / imageEditV2
    2) Date switch:
       - before 2026-03-13 -> imageEdit
       - on/after 2026-03-13 -> imageEditV2
    """
    override = os.environ.get("LINKFOXAI_IMAGE_EDIT_PATH", "").strip()
    if override:
        if override.startswith("/"):
            return override
        return f"{PATH_PREFIX}/image/v2/make/{override}"

    endpoint = "imageEditV2" if date.today() >= IMAGE_EDIT_V2_EFFECTIVE_DATE else "imageEdit"
    return f"{PATH_PREFIX}/image/v2/make/{endpoint}"


# ─── Polling ────────────────────────────────────────────────────────────

def poll_make_info(task_id, interval: int = 3, timeout: int = 300) -> dict:
    """Poll make-info until status is 3 (success) or 4 (fail), or timeout."""
    start = time.time()
    last_status = None
    while True:
        elapsed = time.time() - start
        if elapsed > timeout:
            return {"error": f"Polling timeout after {timeout}s", "last_status": last_status}
        resp = api_post(f"{PATH_PREFIX}/image/v2/make/info", {"id": int(task_id)})
        data = resp.get("data", resp)
        if isinstance(data, dict) and "data" in data:
            data = data["data"]
        status = data.get("status") if isinstance(data, dict) else None
        last_status = status
        if status == 3:
            return resp
        if status == 4:
            return resp
        remaining = timeout - (time.time() - start)
        if remaining <= 0:
            return {"error": f"Polling timeout after {timeout}s", "last_status": last_status}
        print(f"[poll] status={status}, elapsed={int(elapsed)}s, next check in {interval}s...", file=sys.stderr)
        time.sleep(min(interval, remaining))


# ─── Command implementations ───────────────────────────────────────────

def cmd_material_list(typ: str, page_num: int = 1, page_size: int = 10) -> dict:
    return api_post(f"{PATH_PREFIX}/image/v2/material/list",
                    {"type": typ, "pageNum": page_num, "pageSize": page_size})


def cmd_upload_base64(file_path: str) -> dict:
    with open(file_path, "rb") as f:
        raw = f.read()
    b64 = base64.b64encode(raw).decode("ascii")
    name = os.path.basename(file_path)
    return api_post(f"{PATH_PREFIX}/image/v2/uploadByBase64", {"fileName": name, "base64": b64})


def cmd_change_model(image_url, head_url, scene_url=None, output_num=1) -> dict:
    body = {"imageUrl": image_url, "modelHeadImageUrl": head_url, "outputNum": output_num}
    if scene_url:
        body["sceneImgUrl"] = scene_url
    return api_post(f"{PATH_PREFIX}/image/v2/make/changeModel", body)


def cmd_make_info(task_id) -> dict:
    tid = int(task_id) if isinstance(task_id, str) and task_id.isdigit() else task_id
    return api_post(f"{PATH_PREFIX}/image/v2/make/info", {"id": tid})


def cmd_cutout(image_url: str, sub_type: int, cloth_class: str = None) -> dict:
    body = {"imageUrl": image_url, "subType": sub_type}
    if cloth_class:
        body["clothClass"] = cloth_class
    return api_post(f"{PATH_PREFIX}/image/v2/make/cutout", body)


def cmd_scene_fission(image_url: str, strength: str = None, prompt: str = None,
                      provider: str = None, output_num: int = 1) -> dict:
    body = {"imageUrl": image_url, "outputNum": output_num}
    if strength:
        body["strength"] = strength
    if prompt:
        body["prompt"] = prompt
    if provider:
        body["provider"] = provider
    return api_post(f"{PATH_PREFIX}/image/v2/make/sceneFission", body)


def cmd_expand_image(image_url: str, width: int, height: int,
                     prompt: str = None, output_num: int = 1) -> dict:
    body = {"imageUrl": image_url, "width": width, "height": height, "outputNum": output_num}
    if prompt:
        body["prompt"] = prompt
    return api_post(f"{PATH_PREFIX}/image/v2/make/expandImage", body)


def cmd_super_resolution(image_url: str, magnification: float, enhance: bool = False) -> dict:
    body = {"imageUrl": image_url, "magnification": str(magnification), "enhanceQuality": enhance}
    return api_post(f"{PATH_PREFIX}/image/v2/make/superResolution", body)


def cmd_image_edit(
    image_url: str,
    prompt: str,
    provider: str = "BANANA_2",
    output_num: int = 1,
    template: str = None,
    resolution: str = None,
    aspect_ratio: str = None,
    supply_type: str = None,
    need_optimize: bool = False,
) -> dict:
    body = {
        "imageUrl": image_url,
        "prompt": prompt,
        "provider": provider,
        "outputNum": output_num,
    }
    if template:
        body["template"] = template
    if resolution:
        body["resolution"] = resolution
    if aspect_ratio:
        body["aspectRatio"] = aspect_ratio
    if supply_type:
        body["supplyType"] = supply_type
    if need_optimize:
        body["needOptimize"] = True
    return api_post(get_image_edit_path(), body)


def cmd_erase(image_url: str, mask_url: str) -> dict:
    return api_post(f"{PATH_PREFIX}/image/v2/make/interactErase",
                    {"imageUrl": image_url, "maskImageUrl": mask_url})


def cmd_refresh(image_id, fmt: str = None) -> dict:
    body = {"id": int(image_id)}
    if fmt:
        body["downloadFormat"] = fmt
    return api_post(f"{PATH_PREFIX}/image/v2/info", body)


def cmd_sales_video(
    prompt: str,
    video_type: str,
    image_list=None,
    video_time: int = None,
    is_pro: bool = False,
    aspect_ratio: str = None,
    resolution: str = None,
) -> dict:
    body = {"prompt": prompt, "videoType": video_type}
    if image_list:
        body["imageList"] = image_list
    if video_time is not None:
        body["videoTime"] = video_time
    if is_pro:
        body["isPro"] = True
    if aspect_ratio:
        body["aspectRatio"] = aspect_ratio
    if resolution:
        body["resolution"] = resolution
    return api_post(f"{PATH_PREFIX}/image/v2/make/salesVideo", body)


def cmd_image_to_video(
    image_url: str = None,
    video_type: str = None,
    prompt: str = None,
    video_time: int = None,
    is_pro: bool = False,
    resolution: str = None,
    aspect_ratio: str = None,
    last_frame_image_url: str = None,
    prompt_optimizer: bool = False,
    voice: bool = False,
    camera: str = None,
    image_list=None,
) -> dict:
    body = {"videoType": video_type}
    if image_url:
        body["imageUrl"] = image_url
    if image_list:
        body["imageList"] = image_list
    if prompt:
        body["prompt"] = prompt
    if video_time is not None:
        body["videoTime"] = video_time
    if is_pro:
        body["isPro"] = True
    if resolution:
        body["resolution"] = resolution
    if aspect_ratio:
        body["aspectRatio"] = aspect_ratio
    if last_frame_image_url:
        body["lastFrameImageUrl"] = last_frame_image_url
    if prompt_optimizer:
        body["promptOptimizer"] = True
    if voice:
        body["voice"] = True
    if camera:
        body["camera"] = camera
    return api_post("/linkfox-ai/image/v2/make/imageToVideo", body)


def cmd_video_reclone(
    ref_video_url: str,
    ref_image_list: list,
    video_type: str,
    duration: int,
    resolution: str = None,
    ratio: str = None,
    product_info: str = None,
    sale_country: str = None,
    target_language: str = None,
) -> dict:
    body = {
        "refVideoUrl": ref_video_url,
        "refImageList": ref_image_list,
        "videoType": video_type,
        "duration": duration,
    }
    if resolution:
        body["resolution"] = resolution
    if ratio:
        body["ratio"] = ratio
    if product_info:
        body["productInfo"] = product_info
    if sale_country:
        body["saleCountry"] = sale_country
    if target_language:
        body["targetLanguage"] = target_language
    return api_post(f"{PATH_PREFIX}/image/v2/make/videoReclone", body)


def cmd_product_material(
    image_list: list,
    seller_point: str,
    provider: str = "BANANA_PRO",
    a_plus_num: int = 0,
    a_plus_pro_num: int = 0,
    a_plus_has_phone: bool = False,
    a_plus_aspect_ratio: str = None,
    seller_type_num: int = 0,
    is_extract_pre_point: bool = False,
    scene_type_num: int = 0,
    close_up_type_num: int = 0,
    close_up_white_type_num: int = 0,
    white_bg_type_num: int = 0,
    aspect_ratio: str = None,
    brand_key: str = None,
    resolution: str = None,
    quality: str = None,
    no_text: bool = False,
) -> dict:
    body = {
        "imageList": image_list,
        "sellerPoint": seller_point,
        "provider": provider,
    }
    if a_plus_num > 0:
        body["aPlusNum"] = a_plus_num
    if a_plus_pro_num > 0:
        body["aPlusProNum"] = a_plus_pro_num
    if a_plus_has_phone:
        body["aPlusHasPhone"] = True
    if a_plus_aspect_ratio:
        body["aPlusAspectRatio"] = a_plus_aspect_ratio
    if seller_type_num > 0:
        body["sellerTypeNum"] = seller_type_num
    if is_extract_pre_point:
        body["isExtractPrePoint"] = True
    if scene_type_num > 0:
        body["sceneTypeNum"] = scene_type_num
    if close_up_type_num > 0:
        body["closeUpTypeNum"] = close_up_type_num
    if close_up_white_type_num > 0:
        body["closeUpWhiteTypeNum"] = close_up_white_type_num
    if white_bg_type_num > 0:
        body["whiteBgTypeNum"] = white_bg_type_num
    if aspect_ratio:
        body["aspectRatio"] = aspect_ratio
    if brand_key:
        try:
            body["brandKey"] = json.loads(brand_key)
        except json.JSONDecodeError:
            body["brandKey"] = brand_key
    if resolution:
        body["resolution"] = resolution
    if quality:
        body["quality"] = quality
    if no_text:
        body["noText"] = True
    return api_post(f"{PATH_PREFIX}/image/v2/make/productMarketMaterialV3", body)


def cmd_wear_collection(
    image_list: list,
    seller_point: str,
    provider: str = "BANANA_PRO",
    a_plus_num: int = 0,
    a_plus_pro_num: int = 0,
    a_plus_has_phone: bool = False,
    a_plus_aspect_ratio: str = None,
    model_type_num: int = 0,
    model_image_url: str = None,
    scene_image_url: str = None,
    is_exact_scene: bool = True,
    model_and_scene_info: str = None,
    ins_type_num: int = 0,
    seller_type_num: int = 0,
    is_extract_pre_point: bool = False,
    size_type_num: int = 0,
    white_type_num: int = 0,
    aspect_ratio: str = None,
    brand_key: str = None,
    resolution: str = None,
    quality: str = None,
    no_text: bool = False,
) -> dict:
    body = {
        "imageList": image_list,
        "sellerPoint": seller_point,
        "provider": provider,
    }
    if a_plus_num > 0:
        body["aPlusNum"] = a_plus_num
    if a_plus_pro_num > 0:
        body["aPlusProNum"] = a_plus_pro_num
    if a_plus_has_phone:
        body["aPlusHasPhone"] = True
    if a_plus_aspect_ratio:
        body["aPlusAspectRatio"] = a_plus_aspect_ratio
    if model_type_num > 0:
        body["modelTypeNum"] = model_type_num
        if model_image_url:
            body["modelImageUrl"] = model_image_url
        if scene_image_url:
            body["sceneImageUrl"] = scene_image_url
        if not is_exact_scene:
            body["isExactScene"] = False
        if model_and_scene_info:
            body["modelAndSceneInfo"] = model_and_scene_info
    if ins_type_num > 0:
        body["insTypeNum"] = ins_type_num
    if seller_type_num > 0:
        body["sellerTypeNum"] = seller_type_num
    if is_extract_pre_point:
        body["isExtractPrePoint"] = True
    if size_type_num > 0:
        body["sizeTypeNum"] = size_type_num
    if white_type_num > 0:
        body["whiteTypeNum"] = white_type_num
    if aspect_ratio:
        body["aspectRatio"] = aspect_ratio
    if brand_key:
        try:
            body["brandKey"] = json.loads(brand_key)
        except json.JSONDecodeError:
            body["brandKey"] = brand_key
    if resolution:
        body["resolution"] = resolution
    if quality:
        body["quality"] = quality
    if no_text:
        body["noText"] = True
    return api_post(f"{PATH_PREFIX}/image/v2/make/wearCollectionV2", body)


def cmd_api_call(path: str, body_str: str) -> dict:
    try:
        body = json.loads(body_str)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON body: {e}"}
    return api_post(path, body)


# ─── CLI ────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        description="LinkFoxAI Open Platform CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # material-list
    p = sub.add_parser("material-list", help="作图素材列表（连通性测试）")
    p.add_argument("--type", required=True, help="素材类型 1-10")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--size", type=int, default=10)

    # upload-base64
    p = sub.add_parser("upload-base64", help="base64 上传图片")
    p.add_argument("--file", required=True, help="图片文件路径")

    # change-model
    p = sub.add_parser("change-model", help="AI 换模特")
    p.add_argument("--image-url", required=True)
    p.add_argument("--head-url", required=True)
    p.add_argument("--scene-url", default=None)
    p.add_argument("--output-num", type=int, default=1, choices=[1, 2, 3, 4])
    p.add_argument("--wait", action="store_true", help="提交后自动轮询结果")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)

    # make-info
    p = sub.add_parser("make-info", help="查询作图结果（单次）")
    p.add_argument("--id", required=True)

    # poll
    p = sub.add_parser("poll", help="轮询作图结果直到完成")
    p.add_argument("--id", required=True)
    p.add_argument("--interval", type=int, default=3)
    p.add_argument("--timeout", type=int, default=300)

    # cutout
    p = sub.add_parser("cutout", help="自动抠图")
    p.add_argument("--image-url", required=True)
    p.add_argument("--sub-type", type=int, required=True, help="1=通用 2=人像 3=商品 9=服饰 12=头发 13=人脸")
    p.add_argument("--cloth-class", default=None, help="服饰分类(subType=9): tops,coat,skirt,pants,bag,shoes,hat")
    p.add_argument("--wait", action="store_true")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)

    # scene-fission
    p = sub.add_parser("scene-fission", help="场景裂变")
    p.add_argument("--image-url", required=True)
    p.add_argument("--strength", default=None)
    p.add_argument("--prompt", default=None)
    p.add_argument("--provider", default=None, help="SCENE_FISSION_REALISTIC/SIMPLE/INTELLIGENT")
    p.add_argument("--output-num", type=int, default=1)
    p.add_argument("--wait", action="store_true")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)

    # expand-image
    p = sub.add_parser("expand-image", help="智能扩图")
    p.add_argument("--image-url", required=True)
    p.add_argument("--width", type=int, required=True)
    p.add_argument("--height", type=int, required=True)
    p.add_argument("--prompt", default=None)
    p.add_argument("--output-num", type=int, default=1)
    p.add_argument("--wait", action="store_true")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)

    # super-resolution
    p = sub.add_parser("super-resolution", help="图片高清放大")
    p.add_argument("--image-url", required=True)
    p.add_argument("--magnification", type=float, required=True, help="放大倍数 [1,4]")
    p.add_argument("--enhance", action="store_true", help="是否高清化")
    p.add_argument("--wait", action="store_true")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)

    # image-edit
    p = sub.add_parser("image-edit", help="智能修图")
    p.add_argument("--image-url", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--provider", default="BANANA_2", help="BANANA/BANANA_2/BANANA_PRO/WAN2_7/SEEDREAM5")
    p.add_argument("--output-num", type=int, default=1)
    p.add_argument("--template", default=None)
    p.add_argument("--resolution", default=None, help="1K/2K/4K")
    p.add_argument("--aspect-ratio", default=None, help="如 1:1、16:9")
    p.add_argument("--supply-type", default=None, help="eco/stable")
    p.add_argument("--need-optimize", action="store_true", help="启用提示词优化")
    p.add_argument("--wait", action="store_true")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)

    # erase
    p = sub.add_parser("erase", help="消除笔")
    p.add_argument("--image-url", required=True)
    p.add_argument("--mask-url", required=True, help="消除区域（黑白图，白色为消除区域）")
    p.add_argument("--wait", action="store_true")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)

    # refresh
    p = sub.add_parser("refresh", help="刷新结果图片地址")
    p.add_argument("--id", required=True, help="图片 ID（非任务 ID）")
    p.add_argument("--format", default=None, help="下载格式：jpg/png")

    # sales-video
    p = sub.add_parser("sales-video", help="带货口播")
    p.add_argument("--prompt", required=True, help="口播脚本/提示词")
    p.add_argument("--video-type", required=True, choices=["SORA", "WAN", "SEED", "SEED_FAST", "HAPPY_HORSE"], help="模型类型：SORA/WAN/SEED/SEED_FAST/HAPPY_HORSE")
    p.add_argument("--image-list", nargs="+", default=None, help="参考图 URL 列表，空格分隔")
    p.add_argument("--video-time", type=int, default=None, help="视频时长（秒）：WAN 10/15, SEED 5/10/15")
    p.add_argument("--is-pro", action="store_true", help="开启高质量模式（SEED等同720p）")
    p.add_argument("--aspect-ratio", default=None, help="16:9/9:16/1:1")
    p.add_argument("--resolution", default=None, help="视频分辨率：仅SEED支持 480p/720p/1080p")
    p.add_argument("--wait", action="store_true", help="提交后自动轮询结果")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)

    # image-to-video
    p = sub.add_parser("image-to-video", help="图转视频")
    p.add_argument("--image-url", default=None, help="原图地址（单图/首帧模式）")
    p.add_argument("--image-list", nargs="+", default=None, help="多图参考图列表（SEED/SEED_FAST/KLING/HAPPY_HORSE支持）")
    p.add_argument("--video-type", required=True, choices=["KLING", "V", "WAN", "SEED", "SEED_FAST", "HAILUO", "HAPPY_HORSE"], help="模型类型")
    p.add_argument("--prompt", default=None, help="视频提示词（2000字以内）")
    p.add_argument("--video-time", type=int, default=None, help="视频时长（秒）")
    p.add_argument("--is-pro", action="store_true", help="开启Pro模式（已废弃，建议用--resolution）")
    p.add_argument("--resolution", default=None, help="视频分辨率：KLING 720p/1080p, V 720p/1080p, SEED 480p/720p/1080p, SEED_FAST 480p/720p, HAILUO 768p/1080p, HAPPY_HORSE 720p/1080p")
    p.add_argument("--aspect-ratio", default=None, help="视频比例：KLING多图必传1:1/16:9/9:16, SEED/HAPPY_HORSE支持16:9/9:16")
    p.add_argument("--camera", default=None, help="运镜参数：仅WAN支持 single/multi")
    p.add_argument("--last-frame-image-url", default=None, help="尾帧图地址（KLING仅1080p支持）")
    p.add_argument("--prompt-optimizer", action="store_true", help="开启提示词优化")
    p.add_argument("--voice", action="store_true", help="生成声音（WAN/SEED/KLING仅首尾帧1080p支持）")
    p.add_argument("--wait", action="store_true", help="提交后自动轮询结果")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)

    # product-material (商品套图V3)
    p = sub.add_parser("product-material", help="商品套图V3")
    p.add_argument("--image-list", nargs="+", required=True, help="商品图片URL列表（最多5张）")
    p.add_argument("--seller-point", required=True, help="商品卖点描述（最多2500字符）")
    p.add_argument("--provider", default="BANANA_PRO", help="模型：BANANA_PRO/BANANA_2/WAN2_7/GPT_2_IMAGE")
    p.add_argument("--a-plus-num", type=int, default=0, help="普通A+数量，最大12")
    p.add_argument("--a-plus-pro-num", type=int, default=0, help="高级A+数量，最大12")
    p.add_argument("--a-plus-has-phone", action="store_true", help="生成手机版A+")
    p.add_argument("--a-plus-aspect-ratio", default=None, help="A+宽高比：16:9/9:16/1:1")
    p.add_argument("--seller-type-num", type=int, default=0, help="卖点图数量，最大12")
    p.add_argument("--is-extract-pre-point", action="store_true", help="自动提取卖点")
    p.add_argument("--scene-type-num", type=int, default=0, help="场景图数量，最大12")
    p.add_argument("--close-up-type-num", type=int, default=0, help="特写图数量，最大12")
    p.add_argument("--close-up-white-type-num", type=int, default=0, help="白底特写图数量，最大12")
    p.add_argument("--white-bg-type-num", type=int, default=0, help="白底图数量，最大12")
    p.add_argument("--aspect-ratio", default=None, help="素材宽高比：1:1/3:2/2:3/4:3/3:4/4:5/5:4/16:9/9:16/21:9")
    p.add_argument("--brand-key", default=None, help="品牌基因JSON字符串")
    p.add_argument("--resolution", default=None, help="输出分辨率：2K/4K")
    p.add_argument("--quality", default=None, help="输出品质：low/medium/high（仅GPT_2_IMAGE）")
    p.add_argument("--no-text", action="store_true", help="无字模式，排版不含文字")
    p.add_argument("--wait", action="store_true", help="提交后自动轮询结果")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)

    # wear-collection (服装套图V2)
    p = sub.add_parser("wear-collection", help="服装套图V2")
    p.add_argument("--image-list", nargs="+", required=True, help="商品图片URL列表（最多5张）")
    p.add_argument("--seller-point", required=True, help="商品卖点描述（最多2500字符）")
    p.add_argument("--provider", default="BANANA_PRO", help="模型：BANANA_PRO/BANANA_2/WAN2_7/GPT_2_IMAGE")
    p.add_argument("--a-plus-num", type=int, default=0, help="普通A+数量，最大12")
    p.add_argument("--a-plus-pro-num", type=int, default=0, help="高级A+数量，最大12")
    p.add_argument("--a-plus-has-phone", action="store_true", help="生成手机版A+")
    p.add_argument("--a-plus-aspect-ratio", default=None, help="A+宽高比：16:9/9:16/1:1")
    p.add_argument("--model-type-num", type=int, default=0, help="模特图数量，最大12")
    p.add_argument("--model-image-url", default=None, help="模特参考图（未设置启用智能模式）")
    p.add_argument("--scene-image-url", default=None, help="场景参考图（未设置启用智能模式）")
    p.add_argument("--no-exact-scene", action="store_true", help="相似裂变模式（默认遵循背景）")
    p.add_argument("--model-and-scene-info", default=None, help="场景/模特描述")
    p.add_argument("--ins-type-num", type=int, default=0, help="种草图数量，最大12")
    p.add_argument("--seller-type-num", type=int, default=0, help="卖点图数量，最大12")
    p.add_argument("--is-extract-pre-point", action="store_true", help="自动提取卖点")
    p.add_argument("--size-type-num", type=int, default=0, help="尺码图数量，最大12")
    p.add_argument("--white-type-num", type=int, default=0, help="白底图数量，最大12")
    p.add_argument("--aspect-ratio", default=None, help="素材宽高比：1:1/3:2/2:3/4:3/3:4/4:5/5:4/16:9/9:16/21:9")
    p.add_argument("--brand-key", default=None, help="品牌基因JSON字符串")
    p.add_argument("--resolution", default=None, help="输出分辨率：2K/4K")
    p.add_argument("--quality", default=None, help="输出品质：low/medium/high（仅GPT_2_IMAGE）")
    p.add_argument("--no-text", action="store_true", help="无字模式，排版不含文字")
    p.add_argument("--wait", action="store_true", help="提交后自动轮询结果")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)

    # video-reclone (视频复刻)
    p = sub.add_parser("video-reclone", help="视频复刻")
    p.add_argument("--ref-video-url", required=True, help="参考视频URL（需长期有效）")
    p.add_argument("--ref-image-list", nargs="+", required=True, help="参考商品图URL列表（1~6张）")
    p.add_argument("--video-type", required=True, choices=["SEED", "SEED_FAST"], help="模型类型：SEED/SEED_FAST")
    p.add_argument("--duration", type=int, required=True, help="视频时长（秒），5~15整数")
    p.add_argument("--resolution", required=True, help="分辨率：SEED 480P/720P/1080P, SEED_FAST 480P/720P（不支持1080P）")
    p.add_argument("--sale-country", required=True, help="销售国家（如CN、US）")
    p.add_argument("--target-language", required=True, help="目标语言（如zh、en）")
    p.add_argument("--ratio", default=None, help="视频比例：16:9/9:16/1:1/3:4/4:3/21:9")
    p.add_argument("--product-info", default=None, help="商品信息（最多2500字符）")
    p.add_argument("--wait", action="store_true", help="提交后自动轮询结果")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--interval", type=int, default=3)

    # api-call
    p = sub.add_parser("api-call", help="通用 API 调用（任意路径）")
    p.add_argument("--path", required=True, help="接口路径，如 /linkfox-ai/image/v2/make/aiDraw")
    p.add_argument("--body", required=True, help="请求体 JSON 字符串")

    return parser


def maybe_poll(resp: dict, args) -> dict:
    """If --wait is set and resp contains a task id, auto-poll."""
    if not getattr(args, "wait", False):
        return resp
    if not is_success(resp):
        return resp
    data = resp.get("data", resp)
    if isinstance(data, dict) and "data" in data:
        data = data["data"]
    if isinstance(data, dict):
        task_id = data.get("id")
    elif isinstance(data, (str, int)):
        task_id = data
    else:
        task_id = None
    if not task_id:
        return resp
    print(f"[wait] Task created: {task_id}, polling...", file=sys.stderr)
    return poll_make_info(task_id, args.interval, args.timeout)


def main():
    parser = build_parser()
    args = parser.parse_args()
    out = None

    if args.command == "material-list":
        out = cmd_material_list(args.type, args.page, args.size)
    elif args.command == "upload-base64":
        out = cmd_upload_base64(args.file)
    elif args.command == "change-model":
        out = maybe_poll(cmd_change_model(args.image_url, args.head_url, args.scene_url, args.output_num), args)
    elif args.command == "make-info":
        out = cmd_make_info(args.id)
    elif args.command == "poll":
        out = poll_make_info(args.id, args.interval, args.timeout)
    elif args.command == "cutout":
        out = maybe_poll(cmd_cutout(args.image_url, args.sub_type, args.cloth_class), args)
    elif args.command == "scene-fission":
        out = maybe_poll(cmd_scene_fission(args.image_url, args.strength, args.prompt, args.provider, args.output_num), args)
    elif args.command == "expand-image":
        out = maybe_poll(cmd_expand_image(args.image_url, args.width, args.height, args.prompt, args.output_num), args)
    elif args.command == "super-resolution":
        out = maybe_poll(cmd_super_resolution(args.image_url, args.magnification, args.enhance), args)
    elif args.command == "image-edit":
        out = maybe_poll(
            cmd_image_edit(
                args.image_url,
                args.prompt,
                args.provider,
                args.output_num,
                args.template,
                args.resolution,
                args.aspect_ratio,
                args.supply_type,
                args.need_optimize,
            ),
            args,
        )
    elif args.command == "erase":
        out = maybe_poll(cmd_erase(args.image_url, args.mask_url), args)
    elif args.command == "refresh":
        out = cmd_refresh(args.id, getattr(args, "format", None))
    elif args.command == "sales-video":
        out = maybe_poll(
            cmd_sales_video(
                args.prompt,
                args.video_type,
                args.image_list,
                args.video_time,
                args.is_pro,
                args.aspect_ratio,
                args.resolution,
            ),
            args,
        )
    elif args.command == "image-to-video":
        out = maybe_poll(
            cmd_image_to_video(
                args.image_url,
                args.video_type,
                args.prompt,
                args.video_time,
                args.is_pro,
                args.resolution,
                args.aspect_ratio,
                args.last_frame_image_url,
                args.prompt_optimizer,
                args.voice,
                args.camera,
                args.image_list,
            ),
            args,
        )
    elif args.command == "product-material":
        out = maybe_poll(
            cmd_product_material(
                args.image_list,
                args.seller_point,
                args.provider,
                args.a_plus_num,
                args.a_plus_pro_num,
                args.a_plus_has_phone,
                args.a_plus_aspect_ratio,
                args.seller_type_num,
                args.is_extract_pre_point,
                args.scene_type_num,
                args.close_up_type_num,
                args.close_up_white_type_num,
                args.white_bg_type_num,
                args.aspect_ratio,
                args.brand_key,
                args.resolution,
                args.quality,
                args.no_text,
            ),
            args,
        )
    elif args.command == "wear-collection":
        out = maybe_poll(
            cmd_wear_collection(
                args.image_list,
                args.seller_point,
                args.provider,
                args.a_plus_num,
                args.a_plus_pro_num,
                args.a_plus_has_phone,
                args.a_plus_aspect_ratio,
                args.model_type_num,
                args.model_image_url,
                args.scene_image_url,
                not args.no_exact_scene,
                args.model_and_scene_info,
                args.ins_type_num,
                args.seller_type_num,
                args.is_extract_pre_point,
                args.size_type_num,
                args.white_type_num,
                args.aspect_ratio,
                args.brand_key,
                args.resolution,
                args.quality,
                args.no_text,
            ),
            args,
        )
    elif args.command == "video-reclone":
        out = maybe_poll(
            cmd_video_reclone(
                args.ref_video_url,
                args.ref_image_list,
                args.video_type,
                args.duration,
                args.resolution,
                args.ratio,
                args.product_info,
                args.sale_country,
                args.target_language,
            ),
            args,
        )
    elif args.command == "api-call":
        out = cmd_api_call(args.path, args.body)

    if out is None:
        sys.exit(1)

    print(json.dumps(out, indent=2, ensure_ascii=False))
    if not is_success(out) and "error" not in out:
        sys.exit(1)


if __name__ == "__main__":
    main()
