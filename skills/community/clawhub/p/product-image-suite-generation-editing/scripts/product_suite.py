#!/usr/bin/env python3
"""生成商品事实受控、职责明确的 Nano Banana Pro 电商套图。"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    raise SystemExit("缺少 requests，请运行 pip3 install requests")


API_ROOT = "https://ai-hive.iclip.cn/api/openapi/v1"
MODEL_ID = "public_model_nano_banana_pro"
CONFIG = Path.home() / ".ai-hive" / "config.json"
OUTPUT = Path.home() / "Downloads" / "AiHive"
PLATFORMS = (
    "amazon", "taobao", "tmall", "jd", "pinduoduo", "douyin",
    "xiaohongshu", "tiktok-shop", "shopify", "shopee", "lazada",
    "temu", "aliexpress", "etsy", "walmart", "ebay", "other",
)
SLOTS = (
    "hero-white", "hero-scene", "feature", "detail", "material",
    "size-scale", "lifestyle", "comparison", "packaging", "localized",
)
CLAIM_SLOTS = {"feature", "detail", "comparison"}
IMAGE_TYPES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif",
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
        "或运行 product_suite.py auth --api-key sk-api-*"
    )


class ProductSuiteAPI:
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
                method, url, headers=self.headers, timeout=30, **kwargs
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
            (row for row in models if row.get("publicModelId") == MODEL_ID), None
        )
        if model is None:
            raise SystemExit("当前模型列表没有固定能力：" + MODEL_ID)
        snapshot = next(
            (row for row in model.get("pricingSnapshot", [])
             if row.get("routingMode") == routing),
            None,
        )
        if snapshot is None:
            raise SystemExit("Nano Banana Pro 不支持所选路由：" + routing)
        return snapshot

    def upload_ticket(self, path, content_type):
        return self.request(
            "POST", "media/upload-token",
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
            "POST", "generation/image",
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
        raise SystemExit("参考图必须是 PNG、JPEG、WebP 或 GIF：" + str(path))
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
                transfer.get("method", "PUT"), url,
                headers=transfer.get("headers", {}), data=handle, timeout=300,
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
        if not key:
            raise SystemExit("--param 的 key 不能为空")
        lowered = value.lower()
        if lowered in ("true", "false"):
            value = lowered == "true"
        else:
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
    if not args.sku_record.strip():
        raise SystemExit("--sku-record 不能为空")
    if not args.identity_lock.strip():
        raise SystemExit("--identity-lock 不能为空")
    if not args.source_image or len(args.source_image) > 8:
        raise SystemExit("必须提供 1 到 8 张 --source-image 已授权参考图")
    if len(args.source_role) != len(args.source_image):
        raise SystemExit("每张 --source-image 都必须有一个对应的 --source-role")
    if args.sequence < 1 or args.sequence > 30:
        raise SystemExit("--sequence 必须在 1 到 30 之间")
    if args.batch < 1 or args.batch > 3:
        raise SystemExit("--batch 必须在 1 到 3 之间")
    if args.slot in CLAIM_SLOTS and (
        not args.approved_claim or not args.claim_record
    ):
        raise SystemExit(
            "feature、detail、comparison 必须同时提供 --approved-claim 和 --claim-record"
        )
    if args.approved_claim and not args.claim_record:
        raise SystemExit("使用 --approved-claim 时必须提供 --claim-record")
    if args.slot == "size-scale" and not args.measurement_record:
        raise SystemExit("size-scale 必须提供 --measurement-record")
    if args.slot == "comparison" and not args.comparison_rule:
        raise SystemExit("comparison 必须提供 --comparison-rule")
    if args.exact_copy and len(args.exact_copy) > 180:
        raise SystemExit("--exact-copy 最多 180 个字符，并须逐字人工核对")


def suite_prompt(args):
    roles = "；".join(
        "参考图{}={}".format(index, role)
        for index, role in enumerate(args.source_role, 1)
    )
    text_rule = (
        "尝试逐字呈现『{}』，但交付前必须由人工逐字核对".format(
            args.exact_copy
        )
        if args.exact_copy
        else "不生成实际文字、价格、折扣、认证徽章、参数标签或界面按钮"
    )
    fields = [
        ("套图编号", args.suite_id), ("套图序号", str(args.sequence)),
        ("渠道", args.platform), ("图片职责", args.slot), ("SKU", args.sku),
        ("参考图职责", roles), ("SKU事实台账", args.sku_record),
        ("本帧职责", args.frame_job), ("身份锁定", args.identity_lock),
        ("可编辑元素", args.editable_elements),
        ("已批准宣称", args.approved_claim), ("宣称记录", args.claim_record),
        ("测量记录", args.measurement_record), ("对比规则", args.comparison_rule),
        ("版式", args.layout), ("置景", args.set_design),
        ("照明", args.illumination), ("叠加层预留", args.overlay_reserve),
        ("文字规则", text_rule), ("排除项", args.exclusions),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；这是同一套商品资产中的单张图片，只承担本图唯一目标；"
        "所有商品结构、数量、配件、材质、颜色、标签、Logo、包装和宣称必须来自指定事实与参考图；"
        "不得把风格参考当作商品事实，不得虚构功能、参数、认证、排名、价格或品牌关系；"
        "平台尺寸、文字和广告政策须按发布时的当前规则人工复核"
    )


def render(args):
    validate_brief(args)
    api = ProductSuiteAPI(load_key(args.api_key), args.verbose)
    snapshot = api.model_price(args.routing)
    references = [upload_reference(api, item) for item in args.source_image]
    response = api.create(
        args.routing, snapshot, suite_prompt(args), references,
        args.batch, parse_params(args.param),
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print(
        "[suite]", args.suite_id, "sequence", args.sequence,
        "slot", args.slot, "taskId =", task_id,
    )
    if args.exact_copy:
        print("[text-check] 含指定文字，发布前必须逐字人工核对")
    if not args.no_download:
        wait_and_download(
            api, task_id, Path(args.output_dir),
            args.suite_id, args.sequence, args.slot,
        )


def preview_brief(args):
    validate_brief(args)
    print(suite_prompt(args))


def safe_name(value):
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return cleaned or "suite"


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


def wait_and_download(api, task_id, output_dir, suite_id, sequence, slot):
    deadline = time.time() + 1200
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
    stem = "{}_{:02d}_{}".format(safe_name(suite_id), sequence, safe_name(slot))
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            safe_download(
                item["resultUrl"], output_dir / "{}_{}.png".format(stem, index)
            )


def show_status(args):
    api = ProductSuiteAPI(load_key(args.api_key), args.verbose)
    print(json.dumps(api.task(args.task_id), ensure_ascii=False, indent=2))


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
    parser.add_argument("--suite-id", required=True)
    parser.add_argument("--sku", required=True)
    parser.add_argument("--slot", choices=SLOTS, required=True)
    parser.add_argument("--sequence", type=int, required=True)
    parser.add_argument("--source-image", nargs="+", required=True)
    parser.add_argument("--source-role", nargs="+", required=True)
    parser.add_argument("--sku-record", required=True)
    parser.add_argument("--frame-job", required=True)
    parser.add_argument("--identity-lock", required=True)
    parser.add_argument("--editable-elements")
    parser.add_argument("--approved-claim")
    parser.add_argument("--claim-record")
    parser.add_argument("--measurement-record")
    parser.add_argument("--comparison-rule")
    parser.add_argument("--layout")
    parser.add_argument("--set-design")
    parser.add_argument("--illumination")
    parser.add_argument("--overlay-reserve")
    parser.add_argument("--exact-copy")
    parser.add_argument("--exclusions")
    parser.add_argument("--batch", type=int, default=1)


def build_cli():
    root = argparse.ArgumentParser(
        description="Nano Banana Pro 商品套图生成与编辑工具"
    )
    commands = root.add_subparsers(dest="command", required=True)

    render_command = commands.add_parser("render", help="提交套图中的单张图片")
    brief_flags(render_command)
    render_command.add_argument("--param", nargs="*")
    render_command.add_argument(
        "--routing", choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
        default="COST_FIRST",
    )
    render_command.add_argument("--output-dir", default=str(OUTPUT))
    render_command.add_argument("--no-download", action="store_true")
    connection_flags(render_command)
    render_command.set_defaults(handler=render)

    brief = commands.add_parser("brief", help="只验证并输出套图提示词")
    brief_flags(brief)
    brief.set_defaults(handler=preview_brief)

    status = commands.add_parser("status", help="查询图片任务")
    status.add_argument("--task-id", required=True)
    connection_flags(status)
    status.set_defaults(handler=show_status)

    auth = commands.add_parser("auth", help="保存 AI Hive API Key")
    auth.add_argument("--api-key", required=True)
    auth.set_defaults(handler=save_key)
    return root


def main():
    args = build_cli().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
