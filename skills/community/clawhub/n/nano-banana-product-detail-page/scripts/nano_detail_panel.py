#!/usr/bin/env python3
"""为电商详情页逐张生成事实受控的 Nano Banana 2 面板。"""

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


OPENAPI = "https://ai-hive.iclip.cn/api/openapi/v1"
NANO_MODEL = "public_model_nano_banana_2"
KEY_PATH = Path.home() / ".ai-hive" / "config.json"
DOWNLOADS = Path.home() / "Downloads" / "AiHive"
PANEL_TYPES = (
    "hero",
    "problem",
    "feature",
    "material",
    "how-it-works",
    "scenario",
    "spec",
    "comparison",
    "steps",
    "closing",
)
EVIDENCE_REQUIRED = {"how-it-works", "spec", "comparison", "steps"}
MIME_BY_SUFFIX = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}


def key_from(explicit=None):
    if explicit:
        return explicit
    environment = os.environ.get("AI_HIVE_API_KEY")
    if environment:
        return environment
    try:
        record = json.loads(KEY_PATH.read_text(encoding="utf-8"))
        value = record.get("api_key")
        if value:
            try:
                if KEY_PATH.stat().st_mode & 0o077:
                    KEY_PATH.chmod(0o600)
            except OSError:
                pass
            return value
    except (OSError, ValueError):
        pass
    raise SystemExit(
        "缺少 AI Hive API Key；使用 --api-key、AI_HIVE_API_KEY，"
        "或运行 nano_detail_panel.py auth --api-key sk-api-*"
    )


class DetailAPI:
    def __init__(self, key, trace=False):
        self.trace = trace
        self.headers = {
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        }

    def exchange(self, method, resource, **kwargs):
        url = OPENAPI + "/" + resource.lstrip("/")
        if self.trace:
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

    def snapshot(self, routing):
        models = self.exchange("GET", "models", params={"modelType": "IMAGE"})
        model = next(
            (item for item in models if item.get("publicModelId") == NANO_MODEL),
            None,
        )
        if model is None:
            raise SystemExit("当前模型列表没有固定能力：" + NANO_MODEL)
        price = next(
            (
                item
                for item in model.get("pricingSnapshot", [])
                if item.get("routingMode") == routing
            ),
            None,
        )
        if price is None:
            raise SystemExit("Nano Banana 2 不支持路由：" + routing)
        return price

    def upload_reservation(self, path, content_type):
        return self.exchange(
            "POST",
            "media/upload-token",
            json={
                "filename": path.name,
                "contentType": content_type,
                "sizeBytes": path.stat().st_size,
            },
        )

    def confirm(self, media_id):
        self.exchange("POST", "media/{}/complete".format(media_id))

    def generate_panel(self, routing, price, prompt, media_ids, batch, params):
        return self.exchange(
            "POST",
            "generation/image",
            json={
                "publicModelId": NANO_MODEL,
                "routingMode": routing,
                "prompt": prompt,
                "batchSize": batch,
                "imageMediaIds": media_ids,
                "params": params,
                "pricingSnapshot": price,
            },
        )

    def task(self, task_id):
        return self.exchange("GET", "generation/tasks/" + task_id)


def image_source(filename):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("参考素材不存在：" + str(path))
    content_type = MIME_BY_SUFFIX.get(path.suffix.lower())
    if not content_type:
        raise SystemExit("详情页参考素材必须是常见图片：" + str(path))
    return path, content_type


def upload_evidence(api, filename):
    path, content_type = image_source(filename)
    ticket = api.upload_reservation(path, content_type)
    media_id = ticket["mediaId"]
    transfer = ticket["upload"]
    url = transfer["url"]
    if urlparse(url).scheme != "https":
        raise SystemExit("参考素材上传地址必须使用 HTTPS")
    try:
        with path.open("rb") as stream:
            response = requests.request(
                transfer.get("method", "PUT"),
                url,
                headers=transfer.get("headers", {}),
                data=stream,
                timeout=300,
            )
    except requests.RequestException as exc:
        raise SystemExit("参考素材上传失败：" + str(exc))
    if not response.ok:
        raise SystemExit(
            "参考素材上传失败 {}：{}".format(response.status_code, response.text)
        )
    api.confirm(media_id)
    print("[evidence]", path.name, "->", media_id)
    return media_id


def parameter_map(values):
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


def check_panel(args):
    if args.sequence < 1 or args.sequence > 30:
        raise SystemExit("--sequence 必须在 1 到 30 之间")
    if not args.claim.strip() or not args.visual_proof.strip():
        raise SystemExit("--claim 和 --visual-proof 不能为空")
    if not args.reference:
        raise SystemExit("每张详情页面板至少需要一张 --reference 商品事实图")
    if len(args.reference) > 6:
        raise SystemExit("每张面板最多使用 6 张职责明确的参考图")
    if args.panel_type in EVIDENCE_REQUIRED and not args.evidence:
        raise SystemExit(args.panel_type + " 面板必须提供 --evidence 已核实依据")
    if args.batch < 1 or args.batch > 3:
        raise SystemExit("--batch 必须在 1 到 3 之间")
    if args.required_text and len(args.required_text) > 160:
        raise SystemExit("--required-text 最多 160 个字符，交付前必须人工核对")


def panel_prompt(args):
    text_instruction = (
        "仅尝试呈现以下已核准文字，须逐字人工核对：『{}』".format(
            args.required_text
        )
        if args.required_text
        else "只生成无字底片，不生成标题、参数、价格、折扣、认证或按钮"
    )
    fields = [
        ("页面编号", args.page_id),
        ("顺序", str(args.sequence)),
        ("面板类型", args.panel_type),
        ("商品事实", args.product_facts),
        ("本图唯一主张", args.claim),
        ("主张来源", args.claim_source),
        ("画面如何证明", args.visual_proof),
        ("已核实依据", args.evidence),
        ("必须保持", args.must_keep),
        ("品牌视觉系统", args.style_system),
        ("文案安全区", args.text_zone),
        ("文字规则", text_instruction),
        ("禁止项", args.do_not_show),
    ]
    body = "；".join(label + "：" + value for label, value in fields if value)
    return (
        body
        + "；一张图只表达一个主张；参考图只用于已授权商品事实和已核准证据；"
        + "不得虚构内部结构、对比结果、参数、认证、功效、使用步骤或品牌关系"
    )


def create_panel(args):
    check_panel(args)
    api = DetailAPI(key_from(args.api_key), args.trace)
    price = api.snapshot(args.routing)
    media_ids = [upload_evidence(api, item) for item in args.reference]
    response = api.generate_panel(
        args.routing,
        price,
        panel_prompt(args),
        media_ids,
        args.batch,
        parameter_map(args.param),
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print(
        "[panel]",
        args.page_id,
        "#{}".format(args.sequence),
        args.panel_type,
        "taskId =",
        task_id,
    )
    if args.required_text:
        print("[text-check] 含指定文字，交付前必须逐字人工核对")
    if not args.no_download:
        collect(api, task_id, Path(args.output_dir), args.page_id, args.sequence)


def preview_panel(args):
    check_panel(args)
    print(panel_prompt(args))


def download_image(url, destination):
    if urlparse(url).scheme != "https":
        raise SystemExit("结果下载地址必须使用 HTTPS")
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=300) as response:
            response.raise_for_status()
            with destination.open("wb") as stream:
                for part in response.iter_content(8192):
                    if part:
                        stream.write(part)
    except requests.RequestException as exc:
        raise SystemExit("结果下载失败：" + str(exc))
    print("[saved]", destination)


def collect(api, task_id, output_dir, page_id, sequence, timeout=1200):
    deadline = time.time() + timeout
    task = None
    while time.time() < deadline:
        task = api.task(task_id)
        items = task.get("items", [])
        statuses = [item.get("status", "UNKNOWN") for item in items]
        print("[task]", task_id, ",".join(statuses) or "PENDING")
        if items and all(state in ("COMPLETED", "FAILED") for state in statuses):
            break
        time.sleep(3)
    else:
        raise SystemExit("任务轮询超时；可用 status 命令继续查询")
    safe_page = "".join(c for c in page_id if c.isalnum() or c in "-_") or "page"
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            filename = "{}_{:02d}_{}_{}.png".format(
                safe_page, sequence, task_id, index
            )
            download_image(item["resultUrl"], output_dir / filename)


def status(args):
    api = DetailAPI(key_from(args.api_key), args.trace)
    print(json.dumps(api.task(args.task_id), ensure_ascii=False, indent=2))


def upload_one(args):
    api = DetailAPI(key_from(args.api_key), args.trace)
    print(upload_evidence(api, args.file))


def auth(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    KEY_PATH.write_text(
        json.dumps({"api_key": args.api_key}, indent=2), encoding="utf-8"
    )
    KEY_PATH.chmod(0o600)
    print("已安全写入", KEY_PATH)


def api_flags(parser):
    parser.add_argument("--api-key")
    parser.add_argument("--trace", action="store_true")


def panel_flags(parser):
    parser.add_argument("--page-id", required=True)
    parser.add_argument("--sequence", required=True, type=int)
    parser.add_argument("--panel-type", choices=PANEL_TYPES, required=True)
    parser.add_argument("--product-facts", required=True)
    parser.add_argument("--claim", required=True)
    parser.add_argument("--claim-source", required=True)
    parser.add_argument("--visual-proof", required=True)
    parser.add_argument("--evidence")
    parser.add_argument("--must-keep", required=True)
    parser.add_argument("--style-system")
    parser.add_argument("--text-zone")
    parser.add_argument("--required-text")
    parser.add_argument("--do-not-show")
    parser.add_argument("--reference", nargs="+", required=True)
    parser.add_argument("--batch", type=int, default=1)


def cli():
    root = argparse.ArgumentParser(
        description="Nano Banana 2 商品详情页单图单卖点面板工具"
    )
    commands = root.add_subparsers(dest="command", required=True)

    panel = commands.add_parser("panel", help="提交一张详情页面板")
    panel_flags(panel)
    panel.add_argument("--param", nargs="*")
    panel.add_argument(
        "--routing",
        choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
        default="COST_FIRST",
    )
    panel.add_argument("--output-dir", default=str(DOWNLOADS))
    panel.add_argument("--no-download", action="store_true")
    api_flags(panel)
    panel.set_defaults(handler=create_panel)

    preview = commands.add_parser("preview", help="只检查面板提示词")
    panel_flags(preview)
    preview.set_defaults(handler=preview_panel)

    query = commands.add_parser("status", help="查询面板任务")
    query.add_argument("--task-id", required=True)
    api_flags(query)
    query.set_defaults(handler=status)

    media = commands.add_parser("evidence", help="单独上传商品或证据图片")
    media.add_argument("--file", required=True)
    api_flags(media)
    media.set_defaults(handler=upload_one)

    save = commands.add_parser("auth", help="保存 AI Hive API Key")
    save.add_argument("--api-key", required=True)
    save.set_defaults(handler=auth)
    return root


def main():
    args = cli().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
