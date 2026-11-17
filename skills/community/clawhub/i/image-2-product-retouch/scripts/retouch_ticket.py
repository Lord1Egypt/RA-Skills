#!/usr/bin/env python3
"""用 GPT Image 2 按缺陷工单执行受控商品精修。"""

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
ASSET_TYPES = (
    "packshot", "packaging", "macro", "flat-lay", "on-model", "lifestyle",
    "white-background", "other",
)
TEXT_POLICIES = ("preserve-approved", "repair-from-qc", "remove-unapproved")
BACKGROUND_POLICIES = ("preserve", "cleanup-only")
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
        "或运行 retouch_ticket.py auth --api-key sk-api-*"
    )


class RetouchAPI:
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
                "filename": path.name,
                "contentType": content_type,
                "sizeBytes": path.stat().st_size,
            },
        )

    def complete_upload(self, media_id):
        self.request("POST", "media/{}/complete".format(media_id))

    def generate(self, routing, snapshot, prompt, media_ids, params):
        return self.request(
            "POST", "generation/image",
            json={
                "publicModelId": MODEL_ID,
                "routingMode": routing,
                "prompt": prompt,
                "batchSize": 1,
                "imageMediaIds": media_ids,
                "params": params,
                "pricingSnapshot": snapshot,
            },
        )

    def task(self, task_id):
        return self.request("GET", "generation/tasks/" + task_id)


def validate_id(value, flag):
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", value):
        raise SystemExit(flag + " 只能包含字母、数字、点、下划线和连字符")


def validate(args):
    validate_id(args.job_id, "--job-id")
    validate_id(args.asset_id, "--asset-id")
    if not args.truth_source or len(args.truth_source) > 8:
        raise SystemExit("必须提供 1 到 8 张商品或包装QC事实图")
    if len(args.truth_source) != len(args.truth_role):
        raise SystemExit("每张 --truth-source 必须对应一条 --truth-role")
    count = len(args.defect)
    if count < 1 or count > 8:
        raise SystemExit("每次工单必须包含 1 到 8 个 --defect")
    if len(args.edit_zone) != count or len(args.acceptance) != count:
        raise SystemExit("每个 --defect 必须对应一个 --edit-zone 和 --acceptance")
    if len(args.preserve) < 5:
        raise SystemExit("商品精修至少提供 5 条 --preserve")
    if args.text_policy == "repair-from-qc" and not args.approved_text:
        raise SystemExit("repair-from-qc 必须提供 --approved-text")


def retouch_prompt(args):
    truth = "；".join(
        "QC事实图{}={}".format(index, role)
        for index, role in enumerate(args.truth_role, 2)
    )
    tickets = []
    for index, (defect, zone, acceptance) in enumerate(
        zip(args.defect, args.edit_zone, args.acceptance), 1
    ):
        tickets.append(
            "缺陷{}[区域={}；问题={}；验收={}]".format(
                index, zone, defect, acceptance
            )
        )
    fields = [
        ("精修工单", args.job_id), ("资产", args.asset_id),
        ("资产类型", args.asset_type), ("交付渠道", args.channel),
        ("原始图", "参考图1是待精修原图，也是构图和像素关系的第一依据"),
        ("SKU主档", args.sku_record), ("QC事实素材", truth),
        ("缺陷票据", "；".join(tickets)),
        ("修改预算", args.change_budget),
        ("必须保持", "；".join(args.preserve)),
        ("背景策略", args.background_policy),
        ("裁切策略", args.crop_policy), ("文字策略", args.text_policy),
        ("批准文字", args.approved_text), ("目标质感", args.finish),
        ("排除项", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；这是局部商品精修，不是重新设计、换背景、换SKU或生成广告创意；"
        "只修改列出的缺陷区域，每项修改达到对应验收标准后停止；"
        "原图中未列为缺陷的区域保持像素关系、构图、透视、阴影和反射；"
        "商品结构、材质、颜色、Logo、包装、配件、数量和批准文字以QC事实源为准；"
        "保留真实表面纹理与制造特征，不把材质磨成塑料，不创造不存在的完美；"
        "涉及人物时不得改变身份、肤色、体型、五官、年龄、姿态或身体比例；"
        "不得生成价格、功效、参数、认证、标签、赠品或额外文字"
    )


def image_file(filename):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("图片不存在：" + str(path))
    content_type = IMAGE_TYPES.get(path.suffix.lower())
    if content_type is None:
        raise SystemExit("素材必须是 PNG、JPEG、WebP 或 GIF：" + str(path))
    return path, content_type


def upload(api, filename):
    path, content_type = image_file(filename)
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
            value = json.loads(value)
        except json.JSONDecodeError:
            pass
        result[key] = value
    return result


def run_retouch(args):
    validate(args)
    prompt = retouch_prompt(args)
    params = parse_params(args.param)
    sources = [args.source] + args.truth_source
    if args.preview:
        print(json.dumps({
            "publicModelId": MODEL_ID,
            "batchSize": 1,
            "prompt": prompt,
            "sourceImage": args.source,
            "truthSources": args.truth_source,
            "params": params,
        }, ensure_ascii=False, indent=2))
        return
    api = RetouchAPI(load_key(args.api_key), args.verbose)
    snapshot = api.pricing(args.routing)
    media_ids = [upload(api, item) for item in sources]
    response = api.generate(args.routing, snapshot, prompt, media_ids, params)
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[retouch]", args.job_id, args.asset_id, "taskId =", task_id)
    if not args.no_download:
        wait_and_download(
            api, task_id, Path(args.output_dir), args.job_id, args.asset_id
        )


def safe_name(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "retouch"


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


def wait_and_download(api, task_id, output_dir, job_id, asset_id):
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
        raise SystemExit("任务轮询超时；请用 status 查询原 taskId")
    stem = "{}-{}".format(safe_name(job_id), safe_name(asset_id))
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            safe_download(
                item["resultUrl"], output_dir / "{}-{}.png".format(stem, index)
            )


def status(args):
    api = RetouchAPI(load_key(args.api_key), args.verbose)
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


def build_cli():
    root = argparse.ArgumentParser(description="GPT Image 2 商品精修缺陷工单")
    commands = root.add_subparsers(dest="command", required=True)

    retouch = commands.add_parser("retouch", help="按缺陷、区域与验收标准局部精修")
    retouch.add_argument("--job-id", required=True)
    retouch.add_argument("--asset-id", required=True)
    retouch.add_argument("--source", required=True)
    retouch.add_argument("--asset-type", choices=ASSET_TYPES, required=True)
    retouch.add_argument("--channel", required=True)
    retouch.add_argument("--sku-record", required=True)
    retouch.add_argument("--truth-source", nargs="+", required=True)
    retouch.add_argument("--truth-role", nargs="+", required=True)
    retouch.add_argument("--defect", action="append", required=True)
    retouch.add_argument("--edit-zone", action="append", required=True)
    retouch.add_argument("--acceptance", action="append", required=True)
    retouch.add_argument("--change-budget", required=True)
    retouch.add_argument("--preserve", action="append", required=True)
    retouch.add_argument(
        "--background-policy", choices=BACKGROUND_POLICIES, default="preserve"
    )
    retouch.add_argument("--crop-policy", default="preserve original crop")
    retouch.add_argument(
        "--text-policy", choices=TEXT_POLICIES, default="preserve-approved"
    )
    retouch.add_argument("--approved-text")
    retouch.add_argument("--finish", required=True)
    retouch.add_argument("--reject")
    retouch.add_argument("--preview", action="store_true")
    retouch.add_argument("--param", action="append")
    retouch.add_argument(
        "--routing", choices=("COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"),
        default="COST_FIRST",
    )
    retouch.add_argument("--output-dir", default=str(OUTPUT))
    retouch.add_argument("--no-download", action="store_true")
    retouch.add_argument("--api-key")
    retouch.add_argument("--verbose", action="store_true")
    retouch.set_defaults(handler=run_retouch)

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
