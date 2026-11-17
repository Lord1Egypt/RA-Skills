#!/usr/bin/env python3
"""用 GPT Image 2 建立营销图片母版、派生与本地化血缘。"""

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
STAGES = ("awareness", "consideration", "conversion", "retention", "loyalty")
CHANNELS = (
    "brand-kv", "landing-page", "email", "wechat", "xiaohongshu", "douyin",
    "instagram", "tiktok", "amazon-storefront", "retail-screen",
    "event-screen", "print", "other",
)
ASSET_TYPES = (
    "master-kv", "hero", "email-header", "social-card", "carousel-cover",
    "retail-banner", "event-backdrop", "crm-card", "storefront-module",
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
        "或运行 campaign_lineage.py auth --api-key sk-api-*"
    )


class LineageAPI:
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


def validate_id(value, flag):
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", value):
        raise SystemExit(flag + " 只能包含字母、数字、点、下划线和连字符")


def validate_sources(images, roles):
    if not images or len(images) > 8:
        raise SystemExit("必须提供 1 到 8 张商品或事实素材")
    if len(images) != len(roles):
        raise SystemExit("每张素材必须对应一条职责说明")


def validate_master(args):
    validate_id(args.campaign_id, "--campaign-id")
    validate_id(args.asset_id, "--asset-id")
    validate_sources(args.product_source, args.product_role)


def master_prompt(args):
    roles = "；".join(
        "事实素材{}={}".format(i, role)
        for i, role in enumerate(args.product_role, 1)
    )
    fields = [
        ("Campaign", args.campaign_id), ("母版资产", args.asset_id),
        ("事实素材职责", roles), ("SKU记录", args.sku_record),
        ("受众", args.audience), ("Campaign任务", args.campaign_job),
        ("核心主张", args.core_promise), ("主张来源", args.promise_source),
        ("视觉母题", args.motif), ("色板", args.palette),
        ("镜头语言", args.camera_language), ("主体锁定", args.subject_lock),
        ("文案地图", args.copy_map), ("排除项", args.forbid),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；这是可供后代资产继承的批准母版候选；"
        "商品、人物、Logo、主张和活动事实只能来自指定批准源；"
        "不得虚构参数、结果、价格、权益、日期、认证、合作或品牌关系；"
        "所有实际文字留给批准文案和可编辑排版"
    )


def validate_derive(args):
    validate_id(args.campaign_id, "--campaign-id")
    validate_id(args.asset_id, "--asset-id")
    validate_id(args.parent_asset_id, "--parent-asset-id")
    validate_sources(args.product_source, args.product_role)
    if args.asset_id == args.parent_asset_id:
        raise SystemExit("子资产不能与父资产使用同一 asset-id")
    if len(args.carry_over) < 4:
        raise SystemExit("derive 至少提供 4 条 --carry-over")


def derive_prompt(args):
    roles = "；".join(
        "商品事实{}={}".format(i, role)
        for i, role in enumerate(args.product_role, 2)
    )
    fields = [
        ("Campaign", args.campaign_id), ("子资产", args.asset_id),
        ("父资产", args.parent_asset_id),
        ("父图", "参考图1是已批准父资产"), ("商品事实职责", roles),
        ("漏斗阶段", args.stage), ("渠道", args.channel),
        ("资产类型", args.asset_type), ("本资产任务", args.asset_job),
        ("必须继承", "；".join(args.carry_over)),
        ("重排规则", args.recompose), ("文案地图", args.copy_map),
        ("渠道安全", args.channel_safe), ("成功信号", args.success_signal),
        ("排除项", args.forbid),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；这是父资产的可追溯派生，不是简单拉伸、复制裁切或重新发明Campaign；"
        "保持事实、品牌母题和核心主张，同时让本渠道完成单一任务；"
        "商品与人物身份只能来自事实素材，文字与政策由人工复核"
    )


def validate_localize(args):
    validate_id(args.campaign_id, "--campaign-id")
    validate_id(args.asset_id, "--asset-id")
    validate_id(args.parent_asset_id, "--parent-asset-id")
    validate_sources(args.product_source, args.product_role)
    if args.asset_id == args.parent_asset_id:
        raise SystemExit("本地化资产不能覆盖父资产")
    if len(args.never_localize) < 3:
        raise SystemExit("localize 至少提供 3 条 --never-localize")


def localize_prompt(args):
    roles = "；".join(
        "商品事实{}={}".format(i, role)
        for i, role in enumerate(args.product_role, 2)
    )
    fields = [
        ("Campaign", args.campaign_id), ("本地化资产", args.asset_id),
        ("父资产", args.parent_asset_id),
        ("父图", "参考图1是已批准父资产"), ("商品事实职责", roles),
        ("市场", args.market), ("语言", args.language), ("渠道", args.channel),
        ("本地任务", args.local_job), ("当地语境", args.local_context),
        ("禁止本地化", "；".join(args.never_localize)),
        ("文案地图", args.copy_map), ("市场批准源", args.market_source),
        ("排除项", args.forbid),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；只改变批准的环境、道具密度和版式语境；"
        "不得把国旗、地标或文化刻板符号当作本地化捷径；"
        "商品、人物、Logo、核心主张和批准事实保持不变；"
        "不自动翻译，语言、单位、价格、法律与渠道信息由当地批准稿后期排版"
    )


def source_file(filename):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("图片不存在：" + str(path))
    content_type = IMAGE_TYPES.get(path.suffix.lower())
    if not content_type:
        raise SystemExit("素材必须是 PNG、JPEG、WebP 或 GIF：" + str(path))
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
    print("[source]", path.name, "->", media_id)
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


def submit(args, prompt, files):
    if args.preview:
        print(prompt)
        return
    api = LineageAPI(load_key(args.api_key), args.verbose)
    snapshot = api.pricing(args.routing)
    media_ids = [upload(api, item) for item in files]
    response = api.generate(
        args.routing, snapshot, prompt, media_ids, parse_params(args.param)
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[lineage]", args.campaign_id, args.asset_id, args.command, "taskId =", task_id)
    if not args.no_download:
        wait_and_download(api, task_id, Path(args.output_dir), args.asset_id)


def master(args):
    validate_master(args)
    submit(args, master_prompt(args), args.product_source)


def derive(args):
    validate_derive(args)
    submit(args, derive_prompt(args), [args.parent] + args.product_source)


def localize(args):
    validate_localize(args)
    submit(args, localize_prompt(args), [args.parent] + args.product_source)


def safe_name(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "asset"


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


def wait_and_download(api, task_id, output_dir, asset_id):
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
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            safe_download(
                item["resultUrl"],
                output_dir / "{}_{}.png".format(safe_name(asset_id), index),
            )


def status(args):
    api = LineageAPI(load_key(args.api_key), args.verbose)
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


def generation_flags(parser):
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--param", nargs="*")
    parser.add_argument(
        "--routing", choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
        default="COST_FIRST",
    )
    parser.add_argument("--output-dir", default=str(OUTPUT))
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--api-key")
    parser.add_argument("--verbose", action="store_true")


def product_flags(parser):
    parser.add_argument("--product-source", nargs="+", required=True)
    parser.add_argument("--product-role", nargs="+", required=True)


def build_cli():
    root = argparse.ArgumentParser(
        description="GPT Image 2 Campaign 图片资产血缘工具"
    )
    commands = root.add_subparsers(dest="command", required=True)

    base = commands.add_parser("master", help="创建Campaign母版")
    base.add_argument("--campaign-id", required=True)
    base.add_argument("--asset-id", required=True)
    product_flags(base)
    base.add_argument("--sku-record", required=True)
    base.add_argument("--audience", required=True)
    base.add_argument("--campaign-job", required=True)
    base.add_argument("--core-promise", required=True)
    base.add_argument("--promise-source", required=True)
    base.add_argument("--motif", required=True)
    base.add_argument("--palette", required=True)
    base.add_argument("--camera-language", required=True)
    base.add_argument("--subject-lock", required=True)
    base.add_argument("--copy-map", required=True)
    base.add_argument("--forbid")
    generation_flags(base)
    base.set_defaults(handler=master)

    child = commands.add_parser("derive", help="从批准父资产派生渠道图片")
    child.add_argument("--campaign-id", required=True)
    child.add_argument("--asset-id", required=True)
    child.add_argument("--parent-asset-id", required=True)
    child.add_argument("--parent", required=True)
    product_flags(child)
    child.add_argument("--stage", choices=STAGES, required=True)
    child.add_argument("--channel", choices=CHANNELS, required=True)
    child.add_argument("--asset-type", choices=ASSET_TYPES, required=True)
    child.add_argument("--asset-job", required=True)
    child.add_argument("--carry-over", action="append", required=True)
    child.add_argument("--recompose", required=True)
    child.add_argument("--copy-map", required=True)
    child.add_argument("--channel-safe", required=True)
    child.add_argument("--success-signal", required=True)
    child.add_argument("--forbid")
    generation_flags(child)
    child.set_defaults(handler=derive)

    local = commands.add_parser("localize", help="从批准父资产派生市场本地化图片")
    local.add_argument("--campaign-id", required=True)
    local.add_argument("--asset-id", required=True)
    local.add_argument("--parent-asset-id", required=True)
    local.add_argument("--parent", required=True)
    product_flags(local)
    local.add_argument("--market", required=True)
    local.add_argument("--language", required=True)
    local.add_argument("--channel", choices=CHANNELS, required=True)
    local.add_argument("--local-job", required=True)
    local.add_argument("--local-context", required=True)
    local.add_argument("--never-localize", action="append", required=True)
    local.add_argument("--copy-map", required=True)
    local.add_argument("--market-source", required=True)
    local.add_argument("--forbid")
    generation_flags(local)
    local.set_defaults(handler=localize)

    task = commands.add_parser("status", help="查询生成任务")
    task.add_argument("--task-id", required=True)
    task.add_argument("--api-key")
    task.add_argument("--verbose", action="store_true")
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
