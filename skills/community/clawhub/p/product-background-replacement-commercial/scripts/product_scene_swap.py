#!/usr/bin/env python3
"""用 Nano Banana Pro 做商品边缘与接触关系受控的商业换背景。"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    raise SystemExit("缺少 requests，请运行 pip3 install requests")


API = "https://ai-hive.iclip.cn/api/openapi/v1"
MODEL = "public_model_nano_banana_pro"
CONFIG_PATH = Path.home() / ".ai-hive" / "config.json"
OUTPUT_PATH = Path.home() / "Downloads" / "AiHive"
SCENE_TYPES = (
    "white-studio",
    "lifestyle",
    "campaign",
    "storefront",
    "social-ad",
    "localized",
)
SURFACES = ("floor", "table", "shelf", "hanging", "handheld", "none")
PEOPLE_MODES = ("none", "authorized-hands", "authorized-model")
IMAGE_MIMES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}


def api_key(explicit=None):
    if explicit:
        return explicit
    value = os.environ.get("AI_HIVE_API_KEY")
    if value:
        return value
    try:
        saved = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        value = saved.get("api_key")
        if value:
            try:
                if CONFIG_PATH.stat().st_mode & 0o077:
                    CONFIG_PATH.chmod(0o600)
            except OSError:
                pass
            return value
    except (OSError, ValueError):
        pass
    raise SystemExit(
        "缺少 AI Hive API Key；使用 --api-key、AI_HIVE_API_KEY，"
        "或运行 product_scene_swap.py auth --api-key sk-api-*"
    )


class SceneAPI:
    def __init__(self, key, verbose=False):
        self.verbose = verbose
        self.headers = {
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        }

    def call(self, method, resource, **kwargs):
        url = API + "/" + resource.lstrip("/")
        if self.verbose:
            print("[api]", method, url, file=sys.stderr)
        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                timeout=30,
                **kwargs,
            )
        except requests.RequestException as exc:
            raise SystemExit("AI Hive 请求失败：" + str(exc))
        if not response.ok:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text
            raise SystemExit(
                "AI Hive 返回错误 {}：{}".format(response.status_code, detail)
            )
        if response.status_code == 204:
            return None
        return response.json()

    def pricing(self, routing):
        models = self.call("GET", "models", params={"modelType": "IMAGE"})
        model = next(
            (item for item in models if item.get("publicModelId") == MODEL),
            None,
        )
        if model is None:
            raise SystemExit("当前模型列表没有固定能力：" + MODEL)
        price = next(
            (
                item
                for item in model.get("pricingSnapshot", [])
                if item.get("routingMode") == routing
            ),
            None,
        )
        if price is None:
            raise SystemExit("Nano Banana Pro 不支持路由：" + routing)
        return price

    def reserve_upload(self, path, content_type):
        return self.call(
            "POST",
            "media/upload-token",
            json={
                "filename": path.name,
                "contentType": content_type,
                "sizeBytes": path.stat().st_size,
            },
        )

    def complete_upload(self, media_id):
        self.call("POST", "media/{}/complete".format(media_id))

    def replace(self, routing, pricing, prompt, media_ids, batch, params):
        return self.call(
            "POST",
            "generation/image",
            json={
                "publicModelId": MODEL,
                "routingMode": routing,
                "prompt": prompt,
                "batchSize": batch,
                "imageMediaIds": media_ids,
                "params": params,
                "pricingSnapshot": pricing,
            },
        )

    def task(self, task_id):
        return self.call("GET", "generation/tasks/" + task_id)


def inspect_image(filename):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("图片不存在：" + str(path))
    content_type = IMAGE_MIMES.get(path.suffix.lower())
    if not content_type:
        raise SystemExit("只允许上传 PNG、JPEG、WebP 或 GIF：" + str(path))
    return path, content_type


def upload_image(api, filename):
    path, content_type = inspect_image(filename)
    ticket = api.reserve_upload(path, content_type)
    media_id = ticket["mediaId"]
    transfer = ticket["upload"]
    url = transfer["url"]
    if urlparse(url).scheme != "https":
        raise SystemExit("图片上传地址必须使用 HTTPS")
    try:
        with path.open("rb") as handle:
            response = requests.request(
                transfer.get("method", "PUT"),
                url,
                headers=transfer.get("headers", {}),
                data=handle,
                timeout=300,
            )
    except requests.RequestException as exc:
        raise SystemExit("图片上传失败：" + str(exc))
    if not response.ok:
        raise SystemExit(
            "图片上传失败 {}：{}".format(response.status_code, response.text)
        )
    api.complete_upload(media_id)
    print("[image]", path.name, "->", media_id)
    return media_id


def parse_params(values):
    result = {}
    for pair in values or []:
        if "=" not in pair:
            raise SystemExit("--param 必须使用 key=value：" + pair)
        key, value = pair.split("=", 1)
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        result[key] = value
    return result


def validate_swap(args):
    if not args.product_reference:
        raise SystemExit("必须提供至少一张 --product-reference")
    if len(args.product_reference) > 4:
        raise SystemExit("商品参考图最多 4 张")
    if len(args.background_reference or []) > 2:
        raise SystemExit("背景参考图最多 2 张")
    required = (args.scene, args.keep, args.remove, args.camera,
                args.lighting, args.grounding)
    if not all(value and value.strip() for value in required):
        raise SystemExit(
            "--scene、--keep、--remove、--camera、--lighting 和 --grounding 均不能为空"
        )
    if args.surface == "handheld" and args.people_mode == "none":
        raise SystemExit("handheld 场景必须选择已授权的手或模特模式")
    if args.people_mode != "none" and not args.people_authorized:
        raise SystemExit("出现手或人物时必须确认 --people-authorized")
    if args.batch < 1 or args.batch > 4:
        raise SystemExit("--batch 必须在 1 到 4 之间")


def swap_prompt(args):
    fields = [
        ("商业用途", args.usage),
        ("场景类型", args.scene_type),
        ("目标场景", args.scene),
        ("承托方式", args.surface),
        ("原背景中只移除", args.remove),
        ("商品必须保持", args.keep),
        ("相机与透视", args.camera),
        ("新场景光线", args.lighting),
        ("接触阴影/反射/遮挡", args.grounding),
        ("景深", args.depth),
        ("裁切与安全区", args.crop),
        ("人物模式", args.people_mode),
        ("禁止添加", args.do_not_add),
    ]
    prompt = "；".join(label + "：" + value for label, value in fields if value)
    return (
        prompt
        + "；商品参考图优先锁定商品身份，背景参考图只提供环境与光线；"
        + "只替换明确指定的原背景，不重绘商品轮廓、结构、材质、接口、文字或Logo；"
        + "商品边缘、透视、色温、接触阴影、反射和遮挡关系必须与新场景一致"
    )


def run_swap(args):
    validate_swap(args)
    api = SceneAPI(api_key(args.api_key), args.verbose)
    pricing = api.pricing(args.routing)
    product_ids = [upload_image(api, item) for item in args.product_reference]
    background_ids = [
        upload_image(api, item) for item in args.background_reference or []
    ]
    response = api.replace(
        args.routing,
        pricing,
        swap_prompt(args),
        product_ids + background_ids,
        args.batch,
        parse_params(args.param),
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[scene-swap]", args.scene_type, "taskId =", task_id)
    if not args.no_download:
        poll(api, task_id, Path(args.output_dir))


def preview(args):
    validate_swap(args)
    print(swap_prompt(args))


def save_result(url, destination):
    if urlparse(url).scheme != "https":
        raise SystemExit("结果下载地址必须使用 HTTPS")
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=300) as response:
            response.raise_for_status()
            with destination.open("wb") as handle:
                for chunk in response.iter_content(8192):
                    if chunk:
                        handle.write(chunk)
    except requests.RequestException as exc:
        raise SystemExit("结果下载失败：" + str(exc))
    print("[saved]", destination)


def poll(api, task_id, output_dir, timeout=1200):
    deadline = time.time() + timeout
    task = None
    while time.time() < deadline:
        task = api.task(task_id)
        items = task.get("items", [])
        states = [item.get("status", "UNKNOWN") for item in items]
        print("[task]", task_id, ",".join(states) or "PENDING")
        if items and all(state in ("COMPLETED", "FAILED") for state in states):
            break
        time.sleep(3)
    else:
        raise SystemExit("任务轮询超时；可使用 status 命令继续查询")
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            save_result(
                item["resultUrl"],
                output_dir / "{}_{}.png".format(task_id, index),
            )


def status(args):
    api = SceneAPI(api_key(args.api_key), args.verbose)
    print(json.dumps(api.task(args.task_id), ensure_ascii=False, indent=2))


def upload_only(args):
    api = SceneAPI(api_key(args.api_key), args.verbose)
    print(upload_image(api, args.file))


def auth(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps({"api_key": args.api_key}, indent=2), encoding="utf-8"
    )
    CONFIG_PATH.chmod(0o600)
    print("已安全写入", CONFIG_PATH)


def api_flags(parser):
    parser.add_argument("--api-key")
    parser.add_argument("--verbose", action="store_true")


def swap_flags(parser):
    parser.add_argument("--usage", required=True)
    parser.add_argument("--scene-type", choices=SCENE_TYPES, required=True)
    parser.add_argument("--scene", required=True)
    parser.add_argument("--surface", choices=SURFACES, required=True)
    parser.add_argument("--remove", required=True)
    parser.add_argument("--keep", required=True)
    parser.add_argument("--camera", required=True)
    parser.add_argument("--lighting", required=True)
    parser.add_argument("--grounding", required=True)
    parser.add_argument("--depth")
    parser.add_argument("--crop")
    parser.add_argument("--people-mode", choices=PEOPLE_MODES, default="none")
    parser.add_argument("--people-authorized", action="store_true")
    parser.add_argument("--do-not-add")
    parser.add_argument("--product-reference", nargs="+", required=True)
    parser.add_argument("--background-reference", nargs="*")
    parser.add_argument("--batch", type=int, default=1)


def cli():
    root = argparse.ArgumentParser(
        description="Nano Banana Pro 商品换背景与商业场景合成工具"
    )
    commands = root.add_subparsers(dest="command", required=True)

    replace = commands.add_parser("replace", help="提交商品换背景任务")
    swap_flags(replace)
    replace.add_argument("--param", nargs="*")
    replace.add_argument(
        "--routing",
        choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
        default="COST_FIRST",
    )
    replace.add_argument("--output-dir", default=str(OUTPUT_PATH))
    replace.add_argument("--no-download", action="store_true")
    api_flags(replace)
    replace.set_defaults(handler=run_swap)

    check = commands.add_parser("preview", help="只检查换背景说明")
    swap_flags(check)
    check.set_defaults(handler=preview)

    query = commands.add_parser("status", help="查询换背景任务")
    query.add_argument("--task-id", required=True)
    api_flags(query)
    query.set_defaults(handler=status)

    media = commands.add_parser("upload", help="单独上传商品或背景图片")
    media.add_argument("--file", required=True)
    api_flags(media)
    media.set_defaults(handler=upload_only)

    save = commands.add_parser("auth", help="保存 AI Hive API Key")
    save.add_argument("--api-key", required=True)
    save.set_defaults(handler=auth)
    return root


def main():
    args = cli().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
