#!/usr/bin/env python3
"""用 GPT Image 2 生成单变量、可归因的广告测图 Cell。"""

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
MODEL_ID = "public_model_gpt_image_2"
CONFIG = Path.home() / ".ai-hive" / "config.json"
OUTPUT = Path.home() / "Downloads" / "AiHive"
PLATFORMS = (
    "meta-feed", "meta-story", "google-display", "douyin-ads", "qianchuan",
    "xiaohongshu-ads", "amazon-display", "tiktok-ads", "pinterest-ads",
    "linkedin-ads", "other",
)
EVENTS = ("click", "add-to-cart", "lead", "purchase", "product-view")
VARIABLES = (
    "control", "hook", "evidence", "setting", "composition", "color",
    "product-angle", "offer-frame",
)
IMAGE_TYPES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif",
}


def load_key(explicit=None):
    if explicit:
        return explicit
    if os.environ.get("AI_HIVE_API_KEY"):
        return os.environ["AI_HIVE_API_KEY"]
    try:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
        value = data.get("api_key")
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
        "或运行 ad_test_cell.py auth --api-key sk-api-*"
    )


class AdCellAPI:
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

    def pricing(self, routing):
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
            raise SystemExit("GPT Image 2 不支持所选路由：" + routing)
        return snapshot

    def upload_ticket(self, path, content_type):
        return self.request(
            "POST", "media/upload-token",
            json={
                "filename": path.name, "contentType": content_type,
                "sizeBytes": path.stat().st_size,
            },
        )

    def complete_upload(self, media_id):
        self.request("POST", "media/{}/complete".format(media_id))

    def generate(self, routing, snapshot, prompt, media_ids, params):
        return self.request(
            "POST", "generation/image",
            json={
                "publicModelId": MODEL_ID, "routingMode": routing,
                "prompt": prompt, "batchSize": 1,
                "imageMediaIds": media_ids, "params": params,
                "pricingSnapshot": snapshot,
            },
        )

    def task(self, task_id):
        return self.request("GET", "generation/tasks/" + task_id)


def validate_cell(args):
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,64}", args.cell_id):
        raise SystemExit("--cell-id 只能包含字母、数字、点、下划线和连字符")
    if args.cell_role == "control":
        if args.variable != "control" or args.test_change.strip().lower() != "none":
            raise SystemExit("control 必须使用 --variable control 和 --test-change none")
    else:
        if args.variable == "control" or args.test_change.strip().lower() == "none":
            raise SystemExit("variant 必须选择非 control 变量并写明唯一变化")
    if len(args.invariant) < 5:
        raise SystemExit("每个 Cell 至少提供 5 条 --invariant")
    if not args.product_source or len(args.product_source) > 6:
        raise SystemExit("必须提供 1 到 6 张 --product-source")
    if len(args.product_source) != len(args.product_role):
        raise SystemExit("每张 --product-source 必须对应一条 --product-role")
    if args.variable == "evidence" and (not args.claim or not args.claim_source):
        raise SystemExit("evidence 变量必须提供 --claim 和 --claim-source")
    if args.claim and not args.claim_source:
        raise SystemExit("使用 --claim 时必须提供 --claim-source")
    if args.variable == "offer-frame" and (not args.offer or not args.offer_source):
        raise SystemExit("offer-frame 变量必须提供 --offer 和 --offer-source")
    if args.offer and not args.offer_source:
        raise SystemExit("使用 --offer 时必须提供 --offer-source")


def cell_prompt(args):
    roles = "；".join(
        "商品参考{}={}".format(i, role)
        for i, role in enumerate(args.product_role, 1)
    )
    fields = [
        ("实验", args.experiment_id), ("Cell", args.cell_id),
        ("Cell角色", args.cell_role), ("投放平台", args.platform),
        ("优化事件", args.event), ("测试变量", args.variable),
        ("商品参考职责", roles), ("SKU事实", args.sku_truth),
        ("受众", args.audience), ("假设", args.hypothesis),
        ("控制组视觉", args.control_visual), ("唯一变化", args.test_change),
        ("必须不变", "；".join(args.invariant)),
        ("批准宣称", args.claim), ("宣称来源", args.claim_source),
        ("批准优惠", args.offer), ("优惠来源", args.offer_source),
        ("视觉执行", args.visual_execution), ("文案留白", args.copy_reserve),
        ("落地页信息", args.destination_message),
        ("平台安全区", args.ui_safe_zone), ("披露", args.disclosure),
        ("拒绝项", args.rejection),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；只改变本Cell声明的唯一变量，其他不变量必须与控制组一致；"
        "商品结构、接口、数量、颜色、材质、标签、Logo和包装只能来自商品事实图；"
        "广告视觉与落地页必须表达同一商品和同一批准承诺；"
        "不得虚构效果、评价、销量、价格、优惠、倒计时、认证、测试或比较；"
        "文字与政策合规由人工按投放时的当前平台规则复核"
    )


def source_file(filename):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("商品图片不存在：" + str(path))
    content_type = IMAGE_TYPES.get(path.suffix.lower())
    if not content_type:
        raise SystemExit("商品素材必须是 PNG、JPEG、WebP 或 GIF：" + str(path))
    return path, content_type


def upload(api, filename):
    path, content_type = source_file(filename)
    ticket = api.upload_ticket(path, content_type)
    media_id = ticket["mediaId"]
    transfer = ticket["upload"]
    url = transfer["url"]
    if urlparse(url).scheme != "https":
        raise SystemExit("素材上传地址必须使用 HTTPS")
    try:
        with path.open("rb") as handle:
            response = requests.request(
                transfer.get("method", "PUT"), url,
                headers=transfer.get("headers", {}), data=handle, timeout=300,
            )
    except requests.RequestException as exc:
        raise SystemExit("素材上传失败：" + str(exc))
    if not response.ok:
        raise SystemExit(
            "素材上传失败 {}：{}".format(response.status_code, response.text)
        )
    api.complete_upload(media_id)
    print("[product-source]", path.name, "->", media_id)
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


def cell(args):
    validate_cell(args)
    api = AdCellAPI(load_key(args.api_key), args.verbose)
    snapshot = api.pricing(args.routing)
    media_ids = [upload(api, item) for item in args.product_source]
    response = api.generate(
        args.routing, snapshot, cell_prompt(args), media_ids,
        parse_params(args.param),
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print(
        "[ad-cell]", args.experiment_id, args.cell_id,
        args.variable, "taskId =", task_id,
    )
    if not args.no_download:
        wait_and_download(
            api, task_id, Path(args.output_dir),
            args.experiment_id, args.cell_id,
        )


def brief(args):
    validate_cell(args)
    print(cell_prompt(args))


def safe_name(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "ad-cell"


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


def wait_and_download(api, task_id, output_dir, experiment_id, cell_id):
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
    stem = "{}_{}".format(safe_name(experiment_id), safe_name(cell_id))
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            safe_download(
                item["resultUrl"], output_dir / "{}_{}.png".format(stem, index)
            )


def status(args):
    api = AdCellAPI(load_key(args.api_key), args.verbose)
    print(json.dumps(api.task(args.task_id), ensure_ascii=False, indent=2))


def auth(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(
        json.dumps({"api_key": args.api_key}, indent=2), encoding="utf-8"
    )
    CONFIG.chmod(0o600)
    print("已安全写入", CONFIG)


def cell_flags(parser):
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--cell-id", required=True)
    parser.add_argument("--platform", choices=PLATFORMS, required=True)
    parser.add_argument("--event", choices=EVENTS, required=True)
    parser.add_argument("--cell-role", choices=["control", "variant"], required=True)
    parser.add_argument("--variable", choices=VARIABLES, required=True)
    parser.add_argument("--product-source", nargs="+", required=True)
    parser.add_argument("--product-role", nargs="+", required=True)
    parser.add_argument("--sku-truth", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--hypothesis", required=True)
    parser.add_argument("--control-visual", required=True)
    parser.add_argument("--test-change", required=True)
    parser.add_argument("--invariant", action="append", required=True)
    parser.add_argument("--claim")
    parser.add_argument("--claim-source")
    parser.add_argument("--offer")
    parser.add_argument("--offer-source")
    parser.add_argument("--visual-execution", required=True)
    parser.add_argument("--copy-reserve", required=True)
    parser.add_argument("--destination-message", required=True)
    parser.add_argument("--ui-safe-zone", required=True)
    parser.add_argument("--disclosure")
    parser.add_argument("--rejection")


def connection_flags(parser):
    parser.add_argument("--api-key")
    parser.add_argument("--verbose", action="store_true")


def build_cli():
    root = argparse.ArgumentParser(
        description="GPT Image 2 单变量广告测图 Cell 工具"
    )
    commands = root.add_subparsers(dest="command", required=True)

    make = commands.add_parser("cell", help="生成一个可归因广告Cell")
    cell_flags(make)
    make.add_argument("--param", nargs="*")
    make.add_argument(
        "--routing", choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
        default="COST_FIRST",
    )
    make.add_argument("--output-dir", default=str(OUTPUT))
    make.add_argument("--no-download", action="store_true")
    connection_flags(make)
    make.set_defaults(handler=cell)

    preview = commands.add_parser("brief", help="只验证并输出Cell提示词")
    cell_flags(preview)
    preview.set_defaults(handler=brief)

    task = commands.add_parser("status", help="查询生成任务")
    task.add_argument("--task-id", required=True)
    connection_flags(task)
    task.set_defaults(handler=status)

    save = commands.add_parser("auth", help="保存 AI Hive API Key")
    save.add_argument("--api-key", required=True)
    save.set_defaults(handler=auth)
    return root


def main():
    args = build_cli().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
