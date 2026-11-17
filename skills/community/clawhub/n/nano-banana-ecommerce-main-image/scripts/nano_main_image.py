#!/usr/bin/env python3
"""用 Nano Banana 2 制作商品事实受控的电商主图。"""

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


API_ROOT = "https://ai-hive.iclip.cn/api/openapi/v1"
MODEL_ID = "public_model_nano_banana_2"
CONFIG = Path.home() / ".ai-hive" / "config.json"
OUTPUT = Path.home() / "Downloads" / "AiHive"
PLATFORMS = (
    "amazon",
    "taobao",
    "tmall",
    "jd",
    "pinduoduo",
    "douyin",
    "xiaohongshu",
    "tiktok-shop",
    "shopify",
    "other",
)
ASSETS = (
    "white-main",
    "scene-main",
    "feature-main",
    "lifestyle-main",
    "localized-main",
)
IMAGE_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}


def load_key(explicit=None):
    if explicit:
        return explicit
    environment = os.environ.get("AI_HIVE_API_KEY")
    if environment:
        return environment
    try:
        saved = json.loads(CONFIG.read_text(encoding="utf-8"))
        value = saved.get("api_key")
        if value:
            try:
                if CONFIG.stat().st_mode & 0o077:
                    CONFIG.chmod(0o600)
            except OSError:
                pass
            return value
    except (OSError, ValueError):
        pass
    raise SystemExit(
        "缺少 AI Hive API Key。使用 --api-key、AI_HIVE_API_KEY，"
        "或运行 nano_main_image.py auth --api-key sk-api-*"
    )


class MainImageAPI:
    def __init__(self, key, verbose=False):
        self.verbose = verbose
        self.headers = {
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        }

    def request(self, method, path, **kwargs):
        url = API_ROOT + "/" + path.lstrip("/")
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

    def model_price(self, routing):
        models = self.request("GET", "models", params={"modelType": "IMAGE"})
        model = next(
            (row for row in models if row.get("publicModelId") == MODEL_ID),
            None,
        )
        if model is None:
            raise SystemExit("当前模型列表没有固定能力：" + MODEL_ID)
        snapshot = next(
            (
                row
                for row in model.get("pricingSnapshot", [])
                if row.get("routingMode") == routing
            ),
            None,
        )
        if snapshot is None:
            raise SystemExit("Nano Banana 2 不支持所选路由：" + routing)
        return snapshot

    def upload_ticket(self, path, content_type):
        return self.request(
            "POST",
            "media/upload-token",
            json={
                "filename": path.name,
                "contentType": content_type,
                "sizeBytes": path.stat().st_size,
            },
        )

    def complete_upload(self, media_id):
        self.request("POST", "media/{}/complete".format(media_id))

    def create(self, routing, snapshot, prompt, reference_ids, batch, params):
        return self.request(
            "POST",
            "generation/image",
            json={
                "publicModelId": MODEL_ID,
                "routingMode": routing,
                "prompt": prompt,
                "batchSize": batch,
                "imageMediaIds": reference_ids,
                "params": params,
                "pricingSnapshot": snapshot,
            },
        )

    def task(self, task_id):
        return self.request("GET", "generation/tasks/" + task_id)


def source_image(filename):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("参考图不存在：" + str(path))
    content_type = IMAGE_TYPES.get(path.suffix.lower())
    if not content_type:
        raise SystemExit("参考素材必须是 PNG、JPEG、WebP 或 GIF：" + str(path))
    return path, content_type


def upload_reference(api, filename):
    path, content_type = source_image(filename)
    ticket = api.upload_ticket(path, content_type)
    media_id = ticket["mediaId"]
    transfer = ticket["upload"]
    url = transfer["url"]
    if urlparse(url).scheme != "https":
        raise SystemExit("参考图上传地址必须使用 HTTPS")
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
        raise SystemExit("参考图上传失败：" + str(exc))
    if not response.ok:
        raise SystemExit(
            "参考图上传失败 {}：{}".format(response.status_code, response.text)
        )
    api.complete_upload(media_id)
    print("[reference]", path.name, "->", media_id)
    return media_id


def parse_params(values):
    result = {}
    for item in values or []:
        if "=" not in item:
            raise SystemExit("--param 必须使用 key=value：" + item)
        key, value = item.split("=", 1)
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        result[key] = value
    return result


def validate_brief(args):
    if not args.product_facts.strip():
        raise SystemExit("--product-facts 不能为空")
    if not args.must_keep.strip():
        raise SystemExit("--must-keep 不能为空")
    if not args.reference:
        raise SystemExit("商业主图必须提供至少一张 --reference 商品事实图")
    if len(args.reference) > 8:
        raise SystemExit("最多提供 8 张职责明确的参考图")
    if args.batch < 1 or args.batch > 4:
        raise SystemExit("--batch 必须在 1 到 4 之间")
    if args.required_text and len(args.required_text) > 120:
        raise SystemExit("--required-text 最多 120 个字符，并须在交付前人工核对")


def main_image_prompt(args):
    text_rule = (
        "必须逐字尝试呈现以下文字，并在交付前人工核对：『{}』".format(
            args.required_text
        )
        if args.required_text
        else "不生成文字、价格、折扣、认证标识、Logo 或界面按钮"
    )
    fields = [
        ("渠道", args.platform),
        ("素材类型", args.asset),
        ("SKU", args.sku),
        ("商品事实", args.product_facts),
        ("本图唯一目标", args.objective),
        ("必须保持", args.must_keep),
        ("允许改变", args.may_change),
        ("构图", args.composition),
        ("光线与背景", args.lighting),
        ("安全区", args.safe_zone),
        ("文字规则", text_rule),
        ("禁止项", args.negative),
    ]
    prompt = "；".join(label + "：" + value for label, value in fields if value)
    return (
        prompt
        + "；参考图只用于已授权商品事实；不得虚构结构、配件、容量、功能、认证、功效或品牌关系；"
        + "输出前按当前平台规则人工复核尺寸、留白、文字与禁限售要求"
    )


def render(args):
    validate_brief(args)
    api = MainImageAPI(load_key(args.api_key), args.verbose)
    snapshot = api.model_price(args.routing)
    references = [upload_reference(api, item) for item in args.reference]
    response = api.create(
        args.routing,
        snapshot,
        main_image_prompt(args),
        references,
        args.batch,
        parse_params(args.param),
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[main-image]", args.platform, args.asset, "taskId =", task_id)
    if args.required_text:
        print("[text-check] 含指定文字，发布前必须逐字人工核对")
    if not args.no_download:
        wait_and_download(api, task_id, Path(args.output_dir))


def preview_brief(args):
    validate_brief(args)
    print(main_image_prompt(args))


def safe_download(url, destination):
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


def wait_and_download(api, task_id, output_dir, timeout=1200):
    deadline = time.time() + timeout
    task = None
    while time.time() < deadline:
        task = api.task(task_id)
        items = task.get("items", [])
        statuses = [item.get("status", "UNKNOWN") for item in items]
        print("[task]", task_id, ",".join(statuses) or "PENDING")
        if items and all(value in ("COMPLETED", "FAILED") for value in statuses):
            break
        time.sleep(3)
    else:
        raise SystemExit("任务轮询超时；可用 status 命令继续查询")
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            safe_download(
                item["resultUrl"],
                output_dir / "{}_{}.png".format(task_id, index),
            )


def show_status(args):
    api = MainImageAPI(load_key(args.api_key), args.verbose)
    print(json.dumps(api.task(args.task_id), ensure_ascii=False, indent=2))


def upload_only(args):
    api = MainImageAPI(load_key(args.api_key), args.verbose)
    print(upload_reference(api, args.file))


def save_key(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(
        json.dumps({"api_key": args.api_key}, indent=2), encoding="utf-8"
    )
    CONFIG.chmod(0o600)
    print("已安全写入", CONFIG)


def connection_flags(parser):
    parser.add_argument("--api-key")
    parser.add_argument("--verbose", action="store_true")


def brief_flags(parser):
    parser.add_argument("--platform", choices=PLATFORMS, required=True)
    parser.add_argument("--asset", choices=ASSETS, required=True)
    parser.add_argument("--sku", required=True)
    parser.add_argument("--product-facts", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--must-keep", required=True)
    parser.add_argument("--may-change")
    parser.add_argument("--composition")
    parser.add_argument("--lighting")
    parser.add_argument("--safe-zone")
    parser.add_argument("--required-text")
    parser.add_argument("--negative")
    parser.add_argument("--reference", nargs="+", required=True)
    parser.add_argument("--batch", type=int, default=1)


def build_cli():
    root = argparse.ArgumentParser(
        description="Nano Banana 2 商品事实受控电商主图工具"
    )
    commands = root.add_subparsers(dest="command", required=True)

    render_command = commands.add_parser("render", help="提交电商主图任务")
    brief_flags(render_command)
    render_command.add_argument("--param", nargs="*")
    render_command.add_argument(
        "--routing",
        choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
        default="COST_FIRST",
    )
    render_command.add_argument("--output-dir", default=str(OUTPUT))
    render_command.add_argument("--no-download", action="store_true")
    connection_flags(render_command)
    render_command.set_defaults(handler=render)

    brief = commands.add_parser("brief", help="只生成并检查商品主图提示词")
    brief_flags(brief)
    brief.set_defaults(handler=preview_brief)

    status = commands.add_parser("status", help="查询主图任务")
    status.add_argument("--task-id", required=True)
    connection_flags(status)
    status.set_defaults(handler=show_status)

    media = commands.add_parser("upload", help="单独上传商品参考图")
    media.add_argument("--file", required=True)
    connection_flags(media)
    media.set_defaults(handler=upload_only)

    auth = commands.add_parser("auth", help="保存 AI Hive API Key")
    auth.add_argument("--api-key", required=True)
    auth.set_defaults(handler=save_key)
    return root


def main():
    args = build_cli().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
