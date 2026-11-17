#!/usr/bin/env python3
"""生成 HeyGen 类讲解项目所需的无对白视觉素材。"""

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
AUTH_FILE = Path.home() / ".ai-hive" / "config.json"
RESULT_DIR = Path.home() / "Downloads" / "AiHive"
VISUAL_MODELS = {
    "broll": "public_model_seedance_2_5_t2v",
    "presenter": "public_model_seedance_2_5_i2v",
    "demo": "public_model_seedance_2_5_r2v",
    "background": "public_model_seedance_2_5_video_edit",
    "hold": "public_model_seedance_2_5_video_extend",
}
SAFE_MEDIA = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
}


def secret_key(command_value=None):
    if command_value:
        return command_value
    environment = os.environ.get("AI_HIVE_API_KEY")
    if environment:
        return environment
    try:
        stored = json.loads(AUTH_FILE.read_text(encoding="utf-8"))
        value = stored.get("api_key")
        if value:
            try:
                if AUTH_FILE.stat().st_mode & 0o077:
                    AUTH_FILE.chmod(0o600)
            except OSError:
                pass
            return value
    except (OSError, ValueError):
        pass
    raise SystemExit(
        "缺少 AI Hive API Key；使用 --api-key、AI_HIVE_API_KEY，"
        "或运行 heygen_visual.py auth --api-key sk-api-*"
    )


class VisualAPI:
    def __init__(self, key, log=False):
        self.log = log
        self.headers = {
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        }

    def send(self, method, path, **kwargs):
        url = API + "/" + path.lstrip("/")
        if self.log:
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

    def capability(self, asset, routing):
        fixed_id = VISUAL_MODELS[asset]
        catalog = self.send("GET", "models", params={"modelType": "VIDEO"})
        model = next(
            (row for row in catalog if row.get("publicModelId") == fixed_id),
            None,
        )
        if model is None:
            raise SystemExit("当前模型列表缺少固定能力：" + fixed_id)
        snapshot = next(
            (
                row
                for row in model.get("pricingSnapshot", [])
                if row.get("routingMode") == routing
            ),
            None,
        )
        if snapshot is None:
            raise SystemExit("固定能力不支持路由：" + routing)
        return fixed_id, snapshot

    def reserve_media(self, path, content_type):
        return self.send(
            "POST",
            "media/upload-token",
            json={
                "filename": path.name,
                "contentType": content_type,
                "sizeBytes": path.stat().st_size,
            },
        )

    def accept_media(self, media_id):
        self.send("POST", "media/{}/complete".format(media_id))

    def submit_visual(self, model_id, routing, snapshot, prompt, params,
                      image_ids, video_ids, first_frame=None):
        body = {
            "publicModelId": model_id,
            "routingMode": routing,
            "prompt": prompt,
            "imageMediaIds": image_ids,
            "videoMediaIds": video_ids,
            "audioMediaIds": [],
            "params": params,
            "pricingSnapshot": snapshot,
        }
        if first_frame:
            body["firstFrameMediaId"] = first_frame
        return self.send("POST", "generation/video", json=body)

    def status(self, task_id):
        return self.send("GET", "generation/tasks/" + task_id)


def media_file(filename, expected=None):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("素材不存在：" + str(path))
    content_type = SAFE_MEDIA.get(path.suffix.lower())
    if not content_type:
        raise SystemExit("只允许常见图片和视频素材：" + str(path))
    if expected and not content_type.startswith(expected + "/"):
        raise SystemExit("该位置需要{}文件：{}".format(expected, path))
    return path, content_type


def upload_visual(api, filename, expected=None):
    path, content_type = media_file(filename, expected)
    ticket = api.reserve_media(path, content_type)
    media_id = ticket["mediaId"]
    transfer = ticket["upload"]
    url = transfer["url"]
    if urlparse(url).scheme != "https":
        raise SystemExit("素材上传地址必须使用 HTTPS")
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
        raise SystemExit("素材上传失败：" + str(exc))
    if not response.ok:
        raise SystemExit(
            "素材上传失败 {}：{}".format(response.status_code, response.text)
        )
    api.accept_media(media_id)
    print("[visual-media]", path.name, "->", media_id)
    return media_id


def parse_options(values):
    result = {}
    for value in values or []:
        if "=" not in value:
            raise SystemExit("--param 必须使用 key=value：" + value)
        key, raw = value.split("=", 1)
        try:
            raw = int(raw)
        except ValueError:
            try:
                raw = float(raw)
            except ValueError:
                pass
        result[key] = raw
    return result


def visual_brief(args):
    fields = [
        ("旁白时间段", args.narration_slot),
        ("需要的视觉证据", args.proof),
        ("主持人模式", args.presenter_mode),
        ("人物动作", args.action),
        ("字幕安全区", args.caption_zone),
        ("后期音频来源", args.post_audio),
        ("保护项", args.protect),
        ("补充说明", args.prompt),
    ]
    text = "；".join(label + "：" + value for label, value in fields if value)
    return text + "；输出要求：无对白、无声音；出现主持人时嘴唇保持闭合"


def authorize_and_validate(args):
    if not args.narration_slot or not args.proof:
        raise SystemExit("必须填写 --narration-slot 和 --proof")
    presenter_assets = {"presenter", "demo", "background", "hold"}
    if args.asset in presenter_assets:
        if args.presenter_mode != "authorized-closed-mouth":
            raise SystemExit(
                args.asset + " 必须使用 --presenter-mode authorized-closed-mouth"
            )
        if not args.presenter_authorized:
            raise SystemExit("出现主持人时必须确认 --presenter-authorized")
    elif args.presenter_mode != "absent":
        raise SystemExit("broll 必须使用 --presenter-mode absent")

    if args.asset == "broll":
        if any((args.presenter_still, args.reference_image,
                args.blocking_video, args.source_video)):
            raise SystemExit("broll 无人物镜头不接受媒体输入")
    elif args.asset == "presenter":
        if not args.presenter_still:
            raise SystemExit("presenter 必须提供授权的 --presenter-still")
        if any((args.reference_image, args.blocking_video, args.source_video)):
            raise SystemExit("presenter 只接受一张授权主持人静帧")
    elif args.asset == "demo":
        if not args.reference_image:
            raise SystemExit("demo 至少需要一张 --reference-image")
        if args.presenter_still or args.source_video:
            raise SystemExit("demo 不接受首帧或编辑源视频")
    else:
        if not args.source_video:
            raise SystemExit(args.asset + " 必须提供一个 --source-video")
        if any((args.presenter_still, args.reference_image, args.blocking_video)):
            raise SystemExit(args.asset + " 只接受一个已授权源视频")


def make_visual(args):
    authorize_and_validate(args)
    api = VisualAPI(secret_key(args.api_key), args.log)
    model_id, snapshot = api.capability(args.asset, args.routing)
    first_frame = None
    image_ids = []
    video_ids = []
    if args.presenter_still:
        first_frame = upload_visual(api, args.presenter_still, "image")
    for filename in args.reference_image or []:
        image_ids.append(upload_visual(api, filename, "image"))
    for filename in args.blocking_video or []:
        video_ids.append(upload_visual(api, filename, "video"))
    if args.source_video:
        video_ids.append(upload_visual(api, args.source_video, "video"))
    params = parse_options(args.param)
    if args.asset == "hold":
        params["extendDirection"] = "forward"
    response = api.submit_visual(
        model_id,
        args.routing,
        snapshot,
        visual_brief(args),
        params,
        image_ids,
        video_ids,
        first_frame,
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[visual]", args.asset, "taskId =", task_id)
    print(
        "[boundary] 不含声音克隆、数字人绑定、准确口型同步、TTS 或字幕合成"
    )
    if not args.no_download:
        wait_for_visual(api, task_id, Path(args.output_dir))


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


def wait_for_visual(api, task_id, output_dir, timeout=1200):
    deadline = time.time() + timeout
    task = None
    while time.time() < deadline:
        task = api.status(task_id)
        items = task.get("items", [])
        states = [item.get("status", "UNKNOWN") for item in items]
        print("[status]", task_id, ",".join(states) or "PENDING")
        if items and all(state in ("COMPLETED", "FAILED") for state in states):
            break
        time.sleep(3)
    else:
        raise SystemExit("任务轮询超时；可使用 status 命令继续查询")
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            download(
                item["resultUrl"],
                output_dir / "{}_{}.mp4".format(task_id, index),
            )


def show_status(args):
    api = VisualAPI(secret_key(args.api_key), args.log)
    print(json.dumps(api.status(args.task_id), ensure_ascii=False, indent=2))


def upload_one(args):
    api = VisualAPI(secret_key(args.api_key), args.log)
    print(upload_visual(api, args.file))


def save_auth(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
    AUTH_FILE.write_text(
        json.dumps({"api_key": args.api_key}, indent=2), encoding="utf-8"
    )
    AUTH_FILE.chmod(0o600)
    print("已安全写入", AUTH_FILE)


def api_flags(parser):
    parser.add_argument("--api-key")
    parser.add_argument("--log", action="store_true")


def cli():
    root = argparse.ArgumentParser(
        description="HeyGen 类讲解项目的无对白视觉素材工具"
    )
    commands = root.add_subparsers(dest="command", required=True)

    visual = commands.add_parser("visual", help="生成一项讲解视频视觉资产")
    visual.add_argument("--asset", choices=VISUAL_MODELS, required=True)
    visual.add_argument("--narration-slot", required=True)
    visual.add_argument("--proof", required=True, help="该段需要画面证明的事实")
    visual.add_argument(
        "--presenter-mode",
        choices=["absent", "authorized-closed-mouth"],
        required=True,
    )
    visual.add_argument("--presenter-authorized", action="store_true")
    visual.add_argument("--action", help="无对白人物或物体动作")
    visual.add_argument("--caption-zone")
    visual.add_argument("--post-audio", help="后期旁白或音频的授权来源备注")
    visual.add_argument("--protect")
    visual.add_argument("--prompt")
    visual.add_argument("--presenter-still")
    visual.add_argument("--reference-image", nargs="*")
    visual.add_argument("--blocking-video", nargs="*")
    visual.add_argument("--source-video")
    visual.add_argument("--param", nargs="*")
    visual.add_argument(
        "--routing",
        choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
        default="COST_FIRST",
    )
    visual.add_argument("--output-dir", default=str(RESULT_DIR))
    visual.add_argument("--no-download", action="store_true")
    api_flags(visual)
    visual.set_defaults(handler=make_visual)

    status = commands.add_parser("status", help="查询视觉任务")
    status.add_argument("--task-id", required=True)
    api_flags(status)
    status.set_defaults(handler=show_status)

    media = commands.add_parser("upload", help="单独上传图片或视频")
    media.add_argument("--file", required=True)
    api_flags(media)
    media.set_defaults(handler=upload_one)

    auth = commands.add_parser("auth", help="保存 AI Hive API Key")
    auth.add_argument("--api-key", required=True)
    auth.set_defaults(handler=save_auth)
    return root


def main():
    args = cli().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
