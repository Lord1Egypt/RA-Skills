#!/usr/bin/env python3
"""用 GPT Image 2 按参考图权责契约合成图片。"""

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
IDENTITY_POLICIES = ("no-people", "single-person", "multiple-people")
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
        "或运行 reference_contract.py auth --api-key sk-api-*"
    )


class ContractAPI:
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
    validate_id(args.project_id, "--project-id")
    validate_id(args.asset_id, "--asset-id")
    count = len(args.reference)
    if count < 2 or count > 8:
        raise SystemExit("多参考合成必须提供 2 到 8 张 --reference")
    for values, flag in (
        (args.reference_role, "--reference-role"),
        (args.reference_allow, "--reference-allow"),
        (args.reference_deny, "--reference-deny"),
    ):
        if len(values) != count:
            raise SystemExit("每张参考图必须对应一条 " + flag)
    if not 1 <= args.primary_subject_source <= count:
        raise SystemExit("--primary-subject-source 超出参考图编号范围")
    if not 1 <= args.layout_anchor <= count:
        raise SystemExit("--layout-anchor 超出参考图编号范围")
    identity_sources = args.identity_source or []
    if len(identity_sources) != len(set(identity_sources)):
        raise SystemExit("--identity-source 不能重复")
    if any(index < 1 or index > count for index in identity_sources):
        raise SystemExit("--identity-source 超出参考图编号范围")
    if args.identity_policy == "no-people" and identity_sources:
        raise SystemExit("no-people 不接受 --identity-source")
    if args.identity_policy == "single-person" and len(identity_sources) != 1:
        raise SystemExit("single-person 必须且只能提供一个 --identity-source")
    if args.identity_policy == "multiple-people" and len(identity_sources) < 2:
        raise SystemExit("multiple-people 至少提供两个 --identity-source")
    if len(args.ownership) < 2:
        raise SystemExit("至少提供 2 条 --ownership")
    if len(args.conflict_rule) < 2:
        raise SystemExit("至少提供 2 条 --conflict-rule")
    if len(args.do_not_blend) < 3:
        raise SystemExit("至少提供 3 条 --do-not-blend")
    if len(args.consistency_lock) < 4:
        raise SystemExit("至少提供 4 条 --consistency-lock")


def contract_prompt(args):
    ledger = []
    for index, (role, allow, deny) in enumerate(zip(
        args.reference_role, args.reference_allow, args.reference_deny
    ), 1):
        ledger.append(
            "参考图{}[职责={}；允许借用={}；禁止借用={}]".format(
                index, role, allow, deny
            )
        )
    identities = "、".join(
        "参考图{}".format(index) for index in (args.identity_source or [])
    ) or "无人物身份来源"
    fields = [
        ("项目", args.project_id), ("资产", args.asset_id),
        ("交付渠道", args.channel), ("输出任务", args.output_job),
        ("目标画面", args.scene), ("参考图权责表", "；".join(ledger)),
        ("主主体来源", "参考图{}".format(args.primary_subject_source)),
        ("版式锚点", "参考图{}".format(args.layout_anchor)),
        ("人物身份策略", args.identity_policy), ("身份来源", identities),
        ("元素所有权", "；".join(args.ownership)),
        ("冲突裁决", "；".join(args.conflict_rule)),
        ("严禁混用", "；".join(args.do_not_blend)),
        ("一致性锁定", "；".join(args.consistency_lock)),
        ("光线统一", args.light_unification), ("尺度关系", args.scale_map),
        ("遮挡与接触", args.contact_map), ("后期文字地图", args.copy_map),
        ("排除项", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；按参考图权责表合成一个新画面，不平均混合全部参考；"
        "每张图只贡献允许借用的属性，禁止属性不得跨图迁移；"
        "发生冲突时严格按冲突裁决和元素所有权处理，不自行折中；"
        "主主体的身份、结构、Logo、包装、数量、颜色与可见文字只能来自其授权事实源；"
        "人物脸、发型、肤色、体型、服装、姿势和配饰不得在不同身份来源间拼接；"
        "背景只提供环境时不得污染主体外观，风格图只提供风格时不得带入人物、商品或文字；"
        "画面内不生成价格、参数、认证、品牌关系或未批准文案；一次只输出一个可审核版本"
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
    print("[reference]", path.name, "->", media_id)
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


def run_compose(args):
    validate(args)
    prompt = contract_prompt(args)
    params = parse_params(args.param)
    if args.preview:
        print(json.dumps({
            "publicModelId": MODEL_ID,
            "batchSize": 1,
            "projectId": args.project_id,
            "assetId": args.asset_id,
            "references": [
                {"path": path, "role": role, "allow": allow, "deny": deny}
                for path, role, allow, deny in zip(
                    args.reference, args.reference_role,
                    args.reference_allow, args.reference_deny
                )
            ],
            "prompt": prompt,
            "params": params,
        }, ensure_ascii=False, indent=2))
        return
    api = ContractAPI(load_key(args.api_key), args.verbose)
    snapshot = api.pricing(args.routing)
    media_ids = [upload(api, item) for item in args.reference]
    response = api.generate(args.routing, snapshot, prompt, media_ids, params)
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[reference-contract]", args.project_id, args.asset_id,
          "taskId =", task_id)
    if not args.no_download:
        wait_and_download(
            api, task_id, Path(args.output_dir), args.project_id, args.asset_id
        )


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


def wait_and_download(api, task_id, output_dir, project_id, asset_id):
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
    stem = "{}-{}".format(safe_name(project_id), safe_name(asset_id))
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            safe_download(
                item["resultUrl"], output_dir / "{}-{}.png".format(stem, index)
            )


def status(args):
    api = ContractAPI(load_key(args.api_key), args.verbose)
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
    root = argparse.ArgumentParser(description="GPT Image 2 多参考图权责契约合成")
    commands = root.add_subparsers(dest="command", required=True)

    compose = commands.add_parser("compose", help="按允许与禁止属性合成参考图")
    compose.add_argument("--project-id", required=True)
    compose.add_argument("--asset-id", required=True)
    compose.add_argument("--channel", required=True)
    compose.add_argument("--output-job", required=True)
    compose.add_argument("--scene", required=True)
    compose.add_argument("--reference", nargs="+", required=True)
    compose.add_argument("--reference-role", nargs="+", required=True)
    compose.add_argument("--reference-allow", action="append", required=True)
    compose.add_argument("--reference-deny", action="append", required=True)
    compose.add_argument("--primary-subject-source", type=int, required=True)
    compose.add_argument("--layout-anchor", type=int, required=True)
    compose.add_argument(
        "--identity-policy", choices=IDENTITY_POLICIES, required=True
    )
    compose.add_argument("--identity-source", type=int, action="append")
    compose.add_argument("--ownership", action="append", required=True)
    compose.add_argument("--conflict-rule", action="append", required=True)
    compose.add_argument("--do-not-blend", action="append", required=True)
    compose.add_argument("--consistency-lock", action="append", required=True)
    compose.add_argument("--light-unification", required=True)
    compose.add_argument("--scale-map", required=True)
    compose.add_argument("--contact-map", required=True)
    compose.add_argument("--copy-map", required=True)
    compose.add_argument("--reject")
    compose.add_argument("--preview", action="store_true")
    compose.add_argument("--param", action="append")
    compose.add_argument(
        "--routing", choices=("COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"),
        default="COST_FIRST",
    )
    compose.add_argument("--output-dir", default=str(OUTPUT))
    compose.add_argument("--no-download", action="store_true")
    compose.add_argument("--api-key")
    compose.add_argument("--verbose", action="store_true")
    compose.set_defaults(handler=run_compose)

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
