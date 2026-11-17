#!/usr/bin/env python3
"""AI Hive 固定模型视频任务工具。

只提供 Seedance 2.5 文生视频、图生视频、参考生视频、视频编辑、视频延长、
允许范围内的媒体上传、任务查询与 API Key 初始化。

依赖：requests（pip3 install requests）
"""

import argparse
import json
import os
import sys
import time
import webbrowser
from pathlib import Path

try:
    import requests
except ImportError:
    print("缺少依赖：requests。请运行 pip3 install requests", file=sys.stderr)
    sys.exit(1)


# === 常量 ===

DEFAULT_BASE_URL = "https://ai-hive.iclip.cn/api"
API_KEY_HELP_URL = "https://ai-hive.iclip.cn/chat"
CONFIG_FILE_PATH = os.path.expanduser("~/.ai-hive/config.json")
DEFAULT_OUTPUT_DIR = os.path.expanduser("~/Downloads/AiHive")
DEFAULT_TIMEOUT = 30  # HTTP 请求超时（秒）
DEFAULT_POLL_INTERVAL = 3  # 轮询间隔（秒）
DEFAULT_POLL_TIMEOUT = 1200  # 轮询总超时（秒），约 20 分钟

# 文件扩展名到 MIME 的映射（仅常见类型，最终以模型 videoConfig/imageConfig 为准）
MIME_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".tiff": "image/tiff",
    ".tif": "image/tiff",
    ".heic": "image/heic",
    ".heif": "image/heif",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mov": "video/quicktime",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
}


# === 配置管理 ===

class Config:
    """读取 API Key；认证请求始终发送到固定 AI Hive 地址。"""

    def __init__(self, api_key=None, verbose=False):
        self.verbose = verbose
        self.api_key = self._resolve_api_key(api_key)

    def _resolve_api_key(self, cli_key):
        if cli_key:
            return cli_key
        env_key = os.environ.get("AI_HIVE_API_KEY")
        if env_key:
            return env_key
        file_config = self._read_config_file()
        if file_config.get("api_key"):
            return file_config["api_key"]
        raise SystemExit(
            "未找到 API Key。\n"
            f"请运行 python3 {sys.argv[0]} init --skill-name <skill-name>，"
            "或通过 --api-key / AI_HIVE_API_KEY / ~/.ai-hive/config.json 配置。"
        )

    @staticmethod
    def _read_config_file():
        try:
            with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            try:
                if os.stat(CONFIG_FILE_PATH).st_mode & 0o077:
                    os.chmod(CONFIG_FILE_PATH, 0o600)
            except OSError:
                pass
            return data
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return {}

    def log(self, msg):
        if self.verbose:
            print(f"[verbose] {msg}", file=sys.stderr)


# === HTTP 客户端 ===

class AiHiveClient:
    """封装 AI Hive OpenAPI HTTP 调用。"""

    def __init__(self, config):
        self.config = config
        self.base = DEFAULT_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        }

    def _url(self, path):
        return f"{self.base}/openapi/v1/{path}"

    def _request(self, method, url, **kwargs):
        self.config.log(f"{method} {url}")
        try:
            resp = requests.request(
                method, url, headers=self.headers, timeout=DEFAULT_TIMEOUT, **kwargs
            )
        except requests.exceptions.ConnectionError as e:
            raise SystemExit(
                f"无法连接到 API 服务器：{url}\n"
                f"原因：{e}\n"
                "请检查：网络是否正常 / Base URL 是否正确 / 是否需要代理"
            )
        except requests.exceptions.Timeout:
            raise SystemExit(
                f"API 请求超时（{DEFAULT_TIMEOUT}s）：{url}\n"
                "可稍后重试，或检查网络稳定性"
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(f"网络请求异常：{e}")
        if not resp.ok:
            try:
                detail = resp.json()
            except ValueError:
                detail = resp.text
            raise SystemExit(f"API 请求失败 ({resp.status_code}): {detail}")
        if resp.status_code == 204:
            return None
        return resp.json()

    # --- 业务端点 ---

    def list_models(self, model_type=None):
        params = {}
        if model_type:
            params["modelType"] = model_type
        return self._request("GET", self._url("models"), params=params)

    def find_model(self, public_model_id, model_type=None):
        """查询模型列表并找到指定 publicModelId 的模型。"""
        models = self.list_models(model_type)
        for m in models:
            if m.get("publicModelId") == public_model_id:
                return m
        raise SystemExit(f"未找到模型：{public_model_id}")

    def get_pricing_snapshot(self, model_entry, routing_mode):
        """从模型条目中提取指定路由模式的 pricingSnapshot。"""
        snapshots = model_entry.get("pricingSnapshot", [])
        for s in snapshots:
            if s.get("routingMode") == routing_mode:
                return s
        raise SystemExit(
            f"模型 {model_entry.get('publicModelId')} 不支持路由模式：{routing_mode}"
        )

    def create_upload_token(self, filename, content_type, size_bytes):
        body = {
            "filename": filename,
            "contentType": content_type,
            "sizeBytes": size_bytes,
        }
        return self._request("POST", self._url("media/upload-token"), json=body)

    def complete_upload(self, media_id):
        return self._request(
            "POST", self._url(f"media/{media_id}/complete")
        )

    def generate_video(self, public_model_id, routing_mode, prompt, pricing_snapshot,
                       image_media_ids=None, video_media_ids=None, audio_media_ids=None,
                       first_frame_media_id=None, last_frame_media_id=None,
                       params=None):
        body = {
            "publicModelId": public_model_id,
            "routingMode": routing_mode,
            "prompt": prompt,
            "imageMediaIds": image_media_ids or [],
            "videoMediaIds": video_media_ids or [],
            "audioMediaIds": audio_media_ids or [],
            "params": params or {},
            "pricingSnapshot": pricing_snapshot,
        }
        if first_frame_media_id:
            body["firstFrameMediaId"] = first_frame_media_id
        if last_frame_media_id:
            body["lastFrameMediaId"] = last_frame_media_id
        return self._request("POST", self._url("generation/video"), json=body)

    def get_task(self, task_id):
        return self._request("GET", self._url(f"generation/tasks/{task_id}"))


# === 媒体上传流程 ===

def guess_mime(file_path):
    """根据扩展名推断 MIME 类型。"""
    ext = Path(file_path).suffix.lower()
    return MIME_MAP.get(ext, "application/octet-stream")


def upload_media(client, file_path, expected=None):
    """三步上传：upload-token → PUT → complete。返回 mediaId。"""
    path = Path(file_path)
    if not path.is_file():
        raise SystemExit(f"文件不存在：{file_path}")

    filename = path.name
    content_type = guess_mime(str(path))
    if not content_type.startswith(("image/", "video/", "audio/")):
        raise SystemExit(f"仅允许上传图片、视频或音频素材：{file_path}")
    if expected and not content_type.startswith(expected + "/"):
        raise SystemExit(f"此参数必须提供{expected}文件：{file_path}")
    size = path.stat().st_size

    print(f"[1/3] 创建上传凭证：{filename} ({content_type}, {size} bytes)")
    token = client.create_upload_token(filename, content_type, size)

    media_id = token["mediaId"]
    upload_url = token["upload"]["url"]
    upload_method = token["upload"].get("method", "PUT")
    upload_headers = token["upload"].get("headers", {})

    # PUT 到 OSS — 不携带 API Key，使用返回的 headers
    print(f"[2/3] 上传文件到对象存储...")
    with open(str(path), "rb") as f:
        try:
            oss_resp = requests.request(
                upload_method, upload_url, headers=upload_headers,
                data=f, timeout=300,
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(
                f"OSS 上传网络异常：{e}\n"
                "请检查网络连接或文件大小是否过大"
            )
    if not oss_resp.ok:
        try:
            detail = oss_resp.text
        except Exception:
            detail = "<无法读取响应>"
        raise SystemExit(f"OSS 上传失败 ({oss_resp.status_code}): {detail}")

    print(f"[3/3] 确认上传完成...")
    result = client.complete_upload(media_id)
    print(f"[ok] mediaId = {media_id}")
    return media_id


# === 文件下载 ===

def download_file(url, out_path, timeout=300):
    """流式下载文件，带进度条显示。"""
    print(f"[download] {out_path.name}")
    try:
        resp = requests.get(url, stream=True, timeout=timeout)
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        downloaded = 0
        with open(str(out_path), "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        pct = int(downloaded * 100 / total)
                        bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
                        print(f"\r  {bar} {pct}% ({downloaded // 1024}KB)", end="", flush=True)
        print()
        size_mb = downloaded / (1024 * 1024)
        print(f"[ok] {out_path} ({size_mb:.1f} MB)")
    except requests.exceptions.RequestException as e:
        print(f"\n[error] 下载失败: {e}", file=sys.stderr)


# === 任务轮询 ===

def poll_task(client, task_id, output_dir=DEFAULT_OUTPUT_DIR, no_download=False,
              timeout=DEFAULT_POLL_TIMEOUT, interval=DEFAULT_POLL_INTERVAL):
    """轮询任务直到全部子任务 COMPLETED 或 FAILED。"""
    deadline = time.time() + timeout
    last_progress = {}
    # 状态中文映射
    STATUS_CN = {
        "PENDING": "排队中",
        "QUEUED": "排队中",
        "RUNNING": "生成中",
        "COMPLETED": "已完成",
        "FAILED": "失败",
        "UNKNOWN": "未知",
    }

    while time.time() < deadline:
        task = client.get_task(task_id)
        items = task.get("items", [])
        all_done = True
        for item in items:
            status = item.get("status", "UNKNOWN")
            progress = item.get("progress")
            item_id = item.get("id", "?")
            key = f"{item_id}"
            if progress != last_progress.get(key):
                status_cn = STATUS_CN.get(status, status)
                print(f"  子任务 {item_id}: {status_cn}" +
                      (f" ({progress}%)" if progress is not None else ""))
                last_progress[key] = progress
            if status not in ("COMPLETED", "FAILED"):
                all_done = False

        if all_done:
            break
        time.sleep(interval)
    else:
        raise SystemExit(f"任务轮询超时（{timeout}s），taskId={task_id}")

    # 结果处理
    task = client.get_task(task_id)
    items = task.get("items", [])
    failed = [i for i in items if i.get("status") == "FAILED"]
    succeeded = [i for i in items if i.get("status") == "COMPLETED"]

    if failed:
        for item in failed:
            print(f"[failed] 子任务 {item.get('id')}: {item.get('errorMessage')}",
                  file=sys.stderr)

    if no_download:
        print(f"\n任务完成：{len(succeeded)} 成功, {len(failed)} 失败")
        print(json.dumps(task, ensure_ascii=False, indent=2))
        return

    if not succeeded:
        print("没有成功的子任务可下载", file=sys.stderr)
        return

    # 下载结果
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    task_type = task.get("taskType", "task")
    for i, item in enumerate(succeeded):
        result_url = item.get("resultUrl")
        if not result_url:
            continue
        ext = ".mp4" if "video" in task_type.lower() else ".png"
        filename = f"{task_type}_{task_id}_{i+1}{ext}"
        out_path = out_dir / filename
        download_file(result_url, out_path)

    # 尾帧
    for item in succeeded:
        last_frame = item.get("lastFrameUrl")
        if last_frame:
            out_path = out_dir / f"{task_type}_{task_id}_lastframe.png"
            download_file(last_frame, out_path)

    print(f"\n任务完成：{len(succeeded)} 成功, {len(failed)} 失败")


# === CLI 子命令处理 ===

def cmd_video(client, args):
    model_entry = client.find_model(args.model, "VIDEO")
    pricing = client.get_pricing_snapshot(model_entry, args.mode)

    # 上传媒体
    image_media_ids = []
    video_media_ids = []
    audio_media_ids = []
    first_frame_id = None
    last_frame_id = None

    if args.image:
        for p in args.image:
            image_media_ids.append(upload_media(client, p, "image"))
    if args.video:
        for p in args.video:
            video_media_ids.append(upload_media(client, p, "video"))
    if args.audio:
        for p in args.audio:
            audio_media_ids.append(upload_media(client, p, "audio"))
    if args.first_frame:
        first_frame_id = upload_media(client, args.first_frame, "image")
    if args.last_frame:
        last_frame_id = upload_media(client, args.last_frame, "image")

    params = parse_params(args.param)

    result = client.generate_video(
        args.model, args.mode, args.prompt, pricing,
        image_media_ids=image_media_ids,
        video_media_ids=video_media_ids,
        audio_media_ids=audio_media_ids,
        first_frame_media_id=first_frame_id,
        last_frame_media_id=last_frame_id,
        params=params,
    )
    task_id = result.get("taskId")
    if not task_id:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"视频生成任务已提交：taskId = {task_id}")
    if args.no_download:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    poll_task(client, task_id, output_dir=args.output_dir,
              no_download=args.no_download)


def cmd_task(client, args):
    task = client.get_task(args.task_id)
    print(json.dumps(task, ensure_ascii=False, indent=2))


def cmd_upload(client, args):
    media_id = upload_media(client, args.file)
    print(f"\nmediaId: {media_id}")
    print("该 mediaId 可用于本 Skill 的视频生成任务")


# === 辅助函数 ===

def parse_params(param_list):
    """将 ['key=value', ...] 解析为 dict。"""
    if not param_list:
        return {}
    result = {}
    for p in param_list:
        if "=" not in p:
            raise SystemExit(f"参数格式错误（应为 key=value）：{p}")
        k, v = p.split("=", 1)
        # 尝试解析为数字
        try:
            v = int(v)
        except ValueError:
            try:
                v = float(v)
            except ValueError:
                pass
        result[k] = v
    return result


def add_common_args(parser):
    parser.add_argument("--api-key", help="AI Hive API Key (sk-api-*)")
    parser.add_argument("--verbose", action="store_true", help="详细日志")


# === CLI 入口 ===

def _try_read_existing_api_key():
    """安全读取已配置的 API Key，失败返回 None。"""
    env_key = os.environ.get("AI_HIVE_API_KEY")
    if env_key:
        return env_key
    try:
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("api_key")
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def cmd_init(args):
    """交互式初始化 API Key 配置。"""
    # 1. 检查是否已配置
    existing = _try_read_existing_api_key()
    if existing:
        print(f"已检测到 API Key（{existing[:12]}...）")
        response = input("是否重新配置？(y/N): ").strip().lower()
        if response != "y":
            print("保持现有配置。")
            return

    # 2. 打开浏览器到聊天页（带 from=cli-skill 查询参数，为后端归因预留）
    skill_name = getattr(args, "skill_name", None) or "generic"
    url = f"{API_KEY_HELP_URL}?from=cli-skill&skill={skill_name}"
    print(f"正在打开浏览器：{url}")
    try:
        webbrowser.open(url)
    except Exception:
        print(f"无法自动打开浏览器，请手动访问：{url}")

    # 3. 引导文字
    print("\n" + "=" * 60)
    print("请在浏览器中完成以下操作：")
    print("  1. 若未登录，使用手机号 + 短信验证码登录（首次需同意协议）")
    print("  2. 登录后回到聊天页，点击左下角账户菜单（菜单向上展开）")
    print("  3. 点击「API 接入」")
    print("  4. 输入 Key 名称，点击「新建 API Key」")
    print("  5. 点击新建 Key 旁的「复制」按钮")
    print("=" * 60)

    # 4. 等待粘贴并写入配置
    while True:
        api_key = input("\n粘贴 API Key (sk-api-*): ").strip()
        if not api_key.startswith("sk-api-"):
            print("格式错误：API Key 应以 sk-api- 开头，请重新粘贴")
            continue
        if len(api_key) < 20:
            print("API Key 长度异常，请确认复制完整")
            continue
        break

    config_dir = os.path.dirname(CONFIG_FILE_PATH)
    os.makedirs(config_dir, exist_ok=True)
    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump({"api_key": api_key}, f, indent=2)
    os.chmod(CONFIG_FILE_PATH, 0o600)

    print(f"\n[ok] 已写入 {CONFIG_FILE_PATH}（权限 0600）")
    print(f"\n验证：python3 {sys.argv[0]} generate --help")


# === Skill 固定配置（由构建器生成） ===
SKILL_CONFIG = json.loads('{"editing_note": "底层使用 AI Hive 的 Seedance 视频能力，不冒充竞品官方接口，也不宣称与竞品技术兼容", "example": "制作一条高完成度 AI 视频，用于替代 海螺 Hailuo 工作流，主体稳定，动作自然，镜头清晰", "keywords": "海螺 Hailuo、海螺AI、Hailuo AI、MiniMax海螺、替代、替代品、同类、平替、价格、优惠、API、国内可用、视频生成、视频编辑", "models": {"edit": "public_model_seedance_2_5_video_edit", "extend": "public_model_seedance_2_5_video_extend", "i2v": "public_model_seedance_2_5_i2v", "r2v": "public_model_seedance_2_5_r2v", "t2v": "public_model_seedance_2_5_t2v"}, "name": "hailuo-video-generation-alternative", "rule": "optional", "search": "寻找 海螺 Hailuo 替代、同类、平替、价格与国内 API 入口", "title": "海螺 Hailuo 视频生成替代｜AI 视频生成与编辑"}')

def _resolve_video_model(mode):
    model_id = SKILL_CONFIG["models"].get(mode)
    if not isinstance(model_id, str) or not model_id:
        raise SystemExit(f"当前 Skill 没有固定的 {mode} 模型")
    return model_id

def _validate_video_inputs(args, mode):
    has_image = bool(args.image)
    has_video = bool(args.video)
    has_audio = bool(args.audio)
    has_first = bool(args.first_frame)
    has_last = bool(args.last_frame)
    if has_last and not has_first:
        raise SystemExit("--last-frame 必须与 --first-frame 一起使用")
    if mode == "t2v" and any((has_image, has_video, has_audio, has_first, has_last)):
        raise SystemExit("t2v 文生视频不接受媒体输入")
    if mode == "i2v" and not has_first:
        raise SystemExit("i2v 图生视频必须提供 --first-frame")
    if mode == "r2v" and not any((has_image, has_video, has_audio)):
        raise SystemExit("r2v 参考生视频至少需要 --image/--video/--audio 中的一种")
    if mode in ("edit", "extend") and not has_video:
        raise SystemExit(f"{mode} 模式必须提供 --video")

def _select_video_mode(args):
    modes = SKILL_CONFIG["models"]
    fixed = SKILL_CONFIG.get("fixed_mode")
    if fixed:
        return fixed
    if args.mode:
        return args.mode
    if args.first_frame:
        return "i2v"
    if args.image or args.video or args.audio:
        return "r2v"
    return "t2v"

def skill_generate(client, args):
    mode = _select_video_mode(args)
    if mode not in SKILL_CONFIG["models"]:
        raise SystemExit(f"当前 Skill 不支持模式：{mode}")
    _validate_video_inputs(args, mode)
    model_id = _resolve_video_model(mode)
    params = list(args.param or [])
    if mode == "extend":
        params.append(f"extendDirection={args.extend_direction}")
    forwarded = argparse.Namespace(
        model=model_id, mode=args.routing,
        prompt=args.prompt, image=args.image, video=args.video,
        audio=args.audio, first_frame=args.first_frame,
        last_frame=args.last_frame, param=params,
        output_dir=args.output_dir, no_download=args.no_download,
        api_key=args.api_key, verbose=args.verbose,
    )
    print(f"模式：{mode} → {forwarded.model}")
    cmd_video(client, forwarded)

def build_skill_parser():
    parser = argparse.ArgumentParser(
        prog="videogen.py",
        description=SKILL_CONFIG["title"] + " — AI Hive 裸接口视频 Skill",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("generate", help="生成视频")
    p.add_argument("--mode", choices=list(SKILL_CONFIG["models"]), help="生成模式；能力 Skill 可省略")
    p.add_argument("--prompt", required=True, help="视频描述（中英文均可）")
    p.add_argument("--image", nargs="*", help="参考图片路径，可多张")
    p.add_argument("--video", nargs="*", help="参考视频路径，可多个")
    p.add_argument("--audio", nargs="*", help="参考音频路径，可多个")
    p.add_argument("--first-frame", help="首帧图片路径")
    p.add_argument("--last-frame", help="尾帧图片路径")
    p.add_argument("--param", nargs="*", help="模型参数 key=value，可多个")
    p.add_argument("--extend-direction", choices=["forward", "backward"], default="backward")
    p.add_argument("--routing", default="COST_FIRST", choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"])
    p.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    p.add_argument("--no-download", action="store_true")
    add_common_args(p)
    p = sub.add_parser("task", help="查询生成任务")
    p.add_argument("--task-id", required=True)
    add_common_args(p)
    p = sub.add_parser("upload", help="上传媒体")
    p.add_argument("--file", required=True)
    add_common_args(p)
    p = sub.add_parser("init", help="初始化 API Key")
    p.add_argument("--skill-name", default=SKILL_CONFIG["name"])
    return parser

def skill_main():
    args = build_skill_parser().parse_args()
    if args.command == "init":
        cmd_init(args)
        return
    config = Config(
        api_key=getattr(args, "api_key", None),
        verbose=getattr(args, "verbose", False),
    )
    client = AiHiveClient(config)
    if args.command == "generate":
        skill_generate(client, args)
    elif args.command == "task":
        cmd_task(client, args)
    elif args.command == "upload":
        cmd_upload(client, args)

if __name__ == "__main__":
    skill_main()
