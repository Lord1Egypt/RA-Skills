#!/usr/bin/env python3
"""用 Nano Banana 2 统一同一 SKU 多角度商品图的批次视觉标准。"""

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
MODEL_ID = "public_model_nano_banana_2"
CONFIG = Path.home() / ".ai-hive" / "config.json"
OUTPUT = Path.home() / "Downloads" / "AiHive"
ASSET_TYPES = (
    "electronics", "footwear", "jewelry", "apparel", "transparent-product",
    "packaging", "cosmetics", "home-goods", "other",
)
MODES = ("background", "color", "scale", "shadow", "full-batch")
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
        key = data.get("api_key")
        if key:
            try:
                if CONFIG.stat().st_mode & 0o077:
                    CONFIG.chmod(0o600)
            except OSError:
                pass
            return key
    except (OSError, ValueError):
        pass
    raise SystemExit(
        "缺少 AI Hive API Key。使用 --api-key、AI_HIVE_API_KEY，"
        "或运行 batch_calibrate.py auth --api-key sk-api-*"
    )


class ImageAPI:
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
            raise SystemExit("Nano Banana 2 不支持所选路由：" + routing)
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
    validate_id(args.batch_id, "--batch-id")
    validate_id(args.frame_id, "--frame-id")
    if Path(args.target).expanduser().resolve() == Path(args.master).expanduser().resolve():
        raise SystemExit("--target 和 --master 必须是两张不同图片")
    if not args.truth_source or len(args.truth_source) > 6:
        raise SystemExit("必须提供 1 到 6 张 SKU 或包装真值图")
    if len(args.truth_source) != len(args.truth_role):
        raise SystemExit("每张 --truth-source 必须对应一条 --truth-role")
    count = len(args.deviation)
    if count < 1 or count > 8:
        raise SystemExit("每帧必须声明 1 到 8 项 --deviation")
    if len(args.correction) != count or len(args.acceptance) != count:
        raise SystemExit("每项 --deviation 必须对应 --correction 和 --acceptance")
    if len(args.batch_lock) < 5:
        raise SystemExit("至少提供 5 条 --batch-lock")
    if len(args.view_lock) < 3:
        raise SystemExit("至少提供 3 条 --view-lock")


def build_prompt(args):
    truth = "；".join(
        "真值图{}={}".format(index, role)
        for index, role in enumerate(args.truth_role, 3)
    )
    tickets = []
    for index, (deviation, correction, acceptance) in enumerate(
        zip(args.deviation, args.correction, args.acceptance), 1
    ):
        tickets.append(
            "校准项{}[偏差={}；修正={}；验收={}]".format(
                index, deviation, correction, acceptance
            )
        )
    fields = [
        ("批次", args.batch_id), ("帧", args.frame_id),
        ("资产类型", args.asset_type), ("交付渠道", args.channel),
        ("SKU主档", args.sku_record), ("目标视角", args.target_view),
        ("目标图", "参考图1，拥有构图、视角和所有视角专属事实"),
        ("批次母版", "参考图2，仅提供获准的全局视觉标准"),
        ("母版允许传递", args.master_allow),
        ("母版禁止传递", args.master_deny), ("SKU事实源", truth),
        ("归一化模式", args.normalization_mode),
        ("校准票据", "；".join(tickets)),
        ("批次锁", "；".join(args.batch_lock)),
        ("视角锁", "；".join(args.view_lock)),
        ("背景目标", args.background_target),
        ("白平衡目标", args.white_balance_target),
        ("主体比例目标", args.subject_scale_target),
        ("阴影目标", args.shadow_target),
        ("裁切策略", args.crop_policy), ("目标质感", args.finish),
        ("排除项", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；这是同一SKU多角度影像的批次归一化，不是重新设计或自由修图；"
        "不得把母版的拍摄角度、可见结构、文字位置、配件或局部细节复制到目标图；"
        "只传递母版允许的背景、白平衡、主体比例、阴影或整体光感；"
        "目标图拥有视角、透视、遮挡和视角专属细节，SKU事实以真值图为准；"
        "仅修正声明的批次偏差，未声明的局部瑕疵、褶皱、纹理和制造特征保持不变；"
        "不得改变颜色、材质、Logo、包装文字、端口、鞋底、缝线、配件或数量；"
        "不得新增文字、背景道具、卖点、价格、认证、功效、赠品或不存在的商品特征"
    )


def image_file(filename):
    path = Path(filename).expanduser()
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


def run_normalize(args):
    validate(args)
    prompt = build_prompt(args)
    params = parse_params(args.param)
    sources = [args.target, args.master] + args.truth_source
    if args.preview:
        print(json.dumps({
            "publicModelId": MODEL_ID,
            "batchSize": 1,
            "sourceOrder": {
                "reference1Target": args.target,
                "reference2Master": args.master,
                "reference3PlusTruth": args.truth_source,
            },
            "prompt": prompt,
            "params": params,
        }, ensure_ascii=False, indent=2))
        return
    api = ImageAPI(load_key(args.api_key), args.verbose)
    snapshot = api.pricing(args.routing)
    media_ids = [upload(api, item) for item in sources]
    response = api.generate(args.routing, snapshot, prompt, media_ids, params)
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[normalize]", args.batch_id, args.frame_id, "taskId =", task_id)
    if not args.no_download:
        wait_and_download(
            api, task_id, Path(args.output_dir), args.batch_id, args.frame_id
        )


def safe_name(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "batch"


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


def wait_and_download(api, task_id, output_dir, batch_id, frame_id):
    deadline = time.time() + 1200
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
    stem = "{}-{}".format(safe_name(batch_id), safe_name(frame_id))
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            safe_download(
                item["resultUrl"], output_dir / "{}-{}.png".format(stem, index)
            )


def status(args):
    api = ImageAPI(load_key(args.api_key), args.verbose)
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
    root = argparse.ArgumentParser(description="Nano Banana 2 商品批次精修")
    commands = root.add_subparsers(dest="command", required=True)

    norm = commands.add_parser("normalize", help="把单帧校准到同一SKU批次标准")
    norm.add_argument("--batch-id", required=True)
    norm.add_argument("--frame-id", required=True)
    norm.add_argument("--target", required=True)
    norm.add_argument("--master", required=True)
    norm.add_argument("--truth-source", nargs="+", required=True)
    norm.add_argument("--truth-role", nargs="+", required=True)
    norm.add_argument("--asset-type", choices=ASSET_TYPES, required=True)
    norm.add_argument("--channel", required=True)
    norm.add_argument("--sku-record", required=True)
    norm.add_argument("--target-view", required=True)
    norm.add_argument("--master-allow", required=True)
    norm.add_argument("--master-deny", required=True)
    norm.add_argument("--deviation", action="append", required=True)
    norm.add_argument("--correction", action="append", required=True)
    norm.add_argument("--acceptance", action="append", required=True)
    norm.add_argument("--batch-lock", action="append", required=True)
    norm.add_argument("--view-lock", action="append", required=True)
    norm.add_argument("--normalization-mode", choices=MODES, required=True)
    norm.add_argument("--background-target")
    norm.add_argument("--white-balance-target")
    norm.add_argument("--subject-scale-target")
    norm.add_argument("--shadow-target")
    norm.add_argument("--crop-policy", default="preserve target crop")
    norm.add_argument("--finish", required=True)
    norm.add_argument("--reject")
    norm.add_argument("--preview", action="store_true")
    norm.add_argument("--param", action="append")
    norm.add_argument(
        "--routing", choices=("COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"),
        default="COST_FIRST",
    )
    norm.add_argument("--output-dir", default=str(OUTPUT))
    norm.add_argument("--no-download", action="store_true")
    norm.add_argument("--api-key")
    norm.add_argument("--verbose", action="store_true")
    norm.set_defaults(handler=run_normalize)

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
