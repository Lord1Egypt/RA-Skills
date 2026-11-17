#!/usr/bin/env python3
"""AI Hive 单机关视频效果工具。

针对 Pika 替代搜索场景，将一次效果拆成正常、触发、变化、完成和停留，
并固定映射到 Seedance 2.5 的五种视频能力。
"""

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

BASE_URL = "https://ai-hive.iclip.cn/api"
CONFIG_PATH = Path.home() / ".ai-hive" / "config.json"
OUTPUT_DIR = Path.home() / "Downloads" / "AiHive"
MODELS = {
    "create": "public_model_seedance_2_5_t2v",
    "animate": "public_model_seedance_2_5_i2v",
    "borrow": "public_model_seedance_2_5_r2v",
    "isolate": "public_model_seedance_2_5_video_edit",
    "hold": "public_model_seedance_2_5_video_extend",
}
MIME_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
}


def read_key(cli_key=None):
    if cli_key:
        return cli_key
    if os.environ.get("AI_HIVE_API_KEY"):
        return os.environ["AI_HIVE_API_KEY"]
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        if data.get("api_key"):
            try:
                if CONFIG_PATH.stat().st_mode & 0o077:
                    CONFIG_PATH.chmod(0o600)
            except OSError:
                pass
            return data["api_key"]
    except (OSError, ValueError):
        pass
    raise SystemExit(
        "缺少 AI Hive API Key。使用 --api-key、AI_HIVE_API_KEY，"
        "或运行 pika_effect.py init --api-key sk-api-*"
    )


class Hive:
    def __init__(self, key, verbose=False):
        self.verbose = verbose
        self.headers = {
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        }

    def url(self, suffix):
        return BASE_URL + "/openapi/v1/" + suffix

    def call(self, method, url, **kwargs):
        if self.verbose:
            print("[http]", method, url, file=sys.stderr)
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

    def model(self, public_id):
        rows = self.call(
            "GET",
            self.url("models"),
            params={"modelType": "VIDEO"},
        )
        for row in rows:
            if row.get("publicModelId") == public_id:
                return row
        raise SystemExit("AI Hive 当前未找到固定模型：" + public_id)

    @staticmethod
    def price(model, route):
        for snapshot in model.get("pricingSnapshot", []):
            if snapshot.get("routingMode") == route:
                return snapshot
        raise SystemExit("固定模型不支持路由：" + route)

    def upload_token(self, name, content_type, size):
        return self.call(
            "POST",
            self.url("media/upload-token"),
            json={
                "filename": name,
                "contentType": content_type,
                "sizeBytes": size,
            },
        )

    def complete_upload(self, media_id):
        return self.call(
            "POST",
            self.url("media/{}/complete".format(media_id)),
        )

    def submit(self, model_id, route, prompt, pricing, images, videos, params,
               first_frame=None):
        body = {
            "publicModelId": model_id,
            "routingMode": route,
            "prompt": prompt,
            "imageMediaIds": images,
            "videoMediaIds": videos,
            "audioMediaIds": [],
            "params": params,
            "pricingSnapshot": pricing,
        }
        if first_frame:
            body["firstFrameMediaId"] = first_frame
        return self.call(
            "POST",
            self.url("generation/video"),
            json=body,
        )

    def task(self, task_id):
        return self.call(
            "GET",
            self.url("generation/tasks/" + task_id),
        )


def media_type(path, expected=None):
    mime = MIME_TYPES.get(path.suffix.lower())
    if not mime:
        raise SystemExit("仅允许上传常见图片或视频：" + str(path))
    if expected and not mime.startswith(expected + "/"):
        raise SystemExit("该参数必须提供{}文件：{}".format(expected, path))
    return mime


def upload(hive, filename, expected=None):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("素材不存在：" + str(path))
    content_type = media_type(path, expected)
    token = hive.upload_token(path.name, content_type, path.stat().st_size)
    media_id = token["mediaId"]
    upload = token["upload"]
    upload_url = upload["url"]
    scheme = urlparse(upload_url).scheme
    if scheme != "https":
        raise SystemExit("对象存储上传地址必须使用 HTTPS")
    try:
        with path.open("rb") as handle:
            response = requests.request(
                upload.get("method", "PUT"),
                upload_url,
                headers=upload.get("headers", {}),
                data=handle,
                timeout=300,
            )
    except requests.RequestException as exc:
        raise SystemExit("素材上传失败：" + str(exc))
    if not response.ok:
        raise SystemExit(
            "素材上传失败 {}：{}".format(response.status_code, response.text)
        )
    hive.complete_upload(media_id)
    print("[upload]", path.name, "->", media_id)
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


def effect_prompt(args):
    fields = [
        ("正常状态", args.normal),
        ("触发", args.trigger),
        ("变化路径", args.change),
        ("完成状态", args.result),
        ("保护项", args.protect),
        ("补充说明", args.prompt),
    ]
    return "；".join(label + "：" + value for label, value in fields if value)


def validate_effect(args):
    if not any((args.normal, args.trigger, args.change, args.result, args.prompt)):
        raise SystemExit("至少填写 --normal/--trigger/--change/--result/--prompt 之一")
    if args.operation == "create" and any((args.image, args.video)):
        raise SystemExit("create 文生机关不接受媒体输入")
    if args.operation == "animate" and (
        len(args.image or []) != 1 or args.video
    ):
        raise SystemExit("animate 只接受一张 --image 首帧，不接受视频")
    if args.operation == "borrow" and not any((args.image, args.video)):
        raise SystemExit("borrow 至少需要一项 --image 或 --video 参考")
    if args.operation in ("isolate", "hold") and (
        len(args.video or []) != 1 or args.image
    ):
        raise SystemExit(
            args.operation + " 只接受一个 --video 源视频，不接受图片"
        )


def submit_effect(args):
    validate_effect(args)
    hive = Hive(read_key(args.api_key), args.verbose)
    model_id = MODELS[args.operation]
    model = hive.model(model_id)
    pricing = hive.price(model, args.routing)
    images = [upload(hive, item, "image") for item in args.image or []]
    videos = [upload(hive, item, "video") for item in args.video or []]
    params = parse_params(args.param)
    if args.operation == "hold":
        params["extendDirection"] = "forward"
    prompt = effect_prompt(args)
    print("[effect]", args.operation, "->", model_id)
    response = hive.submit(
        model_id,
        args.routing,
        prompt,
        pricing,
        [] if args.operation == "animate" else images,
        videos,
        params,
        first_frame=images[0] if args.operation == "animate" else None,
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("taskId =", task_id)
    if not args.no_download:
        wait_for_task(hive, task_id, Path(args.output_dir))


def download(url, destination):
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


def wait_for_task(hive, task_id, output_dir, timeout=1200):
    deadline = time.time() + timeout
    while time.time() < deadline:
        task = hive.task(task_id)
        items = task.get("items", [])
        states = [item.get("status", "UNKNOWN") for item in items]
        print("[task]", task_id, ",".join(states) or "PENDING")
        if items and all(state in ("COMPLETED", "FAILED") for state in states):
            break
        time.sleep(3)
    else:
        raise SystemExit("任务轮询超时，保留 taskId 后可继续查询")
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        result_url = item.get("resultUrl")
        if item.get("status") == "COMPLETED" and result_url:
            download(result_url, output_dir / "{}_{}.mp4".format(task_id, index))


def show_task(args):
    hive = Hive(read_key(args.api_key), args.verbose)
    print(json.dumps(hive.task(args.task_id), ensure_ascii=False, indent=2))


def upload_only(args):
    hive = Hive(read_key(args.api_key), args.verbose)
    print(upload(hive, args.file))


def initialize(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps({"api_key": args.api_key}, indent=2),
        encoding="utf-8",
    )
    CONFIG_PATH.chmod(0o600)
    print("已安全写入", CONFIG_PATH)


def common(parser):
    parser.add_argument("--api-key")
    parser.add_argument("--verbose", action="store_true")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Pika 替代场景的单机关视频效果工具"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    effect = commands.add_parser("effect", help="生成或调整一次单机关效果")
    effect.add_argument("--operation", choices=MODELS, required=True)
    effect.add_argument("--normal", help="变化前的正常状态")
    effect.add_argument("--trigger", help="唯一触发动作")
    effect.add_argument("--change", help="变化传播路径")
    effect.add_argument("--result", help="完成后的稳定状态")
    effect.add_argument("--protect", help="全程不得改变的主体事实")
    effect.add_argument("--prompt", help="其他镜头说明")
    effect.add_argument("--image", nargs="*")
    effect.add_argument("--video", nargs="*")
    effect.add_argument("--param", nargs="*")
    effect.add_argument(
        "--routing",
        default="COST_FIRST",
        choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
    )
    effect.add_argument("--output-dir", default=str(OUTPUT_DIR))
    effect.add_argument("--no-download", action="store_true")
    common(effect)
    effect.set_defaults(handler=submit_effect)

    task = commands.add_parser("task", help="查询任务")
    task.add_argument("--task-id", required=True)
    common(task)
    task.set_defaults(handler=show_task)

    media = commands.add_parser("upload", help="上传图片或视频素材")
    media.add_argument("--file", required=True)
    common(media)
    media.set_defaults(handler=upload_only)

    init = commands.add_parser("init", help="保存 AI Hive API Key")
    init.add_argument("--api-key", required=True)
    init.set_defaults(handler=initialize)
    return parser


def main():
    args = build_parser().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
