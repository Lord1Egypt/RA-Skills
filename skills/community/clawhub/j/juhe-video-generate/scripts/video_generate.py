#!/usr/bin/env python3
"""
AI视频创作脚本 — 由聚合数据 (juhe.cn) 提供数据支持
支持文生视频（文字描述生成视频）和图生视频（图片动态化生成视频）
生成完成后自动下载视频到本地

用法（文生视频）:
    python video_generate.py "夕阳下的海边，海浪轻柔拍打礁石，写实风格"
    python video_generate.py "城市夜景" --resolution 1080P --duration 10 --proportion 16:9
    python video_generate.py "唯美樱花" --negative "落叶、枯枝" --no-extend

用法（图生视频）:
    python video_generate.py --image https://example.com/photo.jpg --prompt "让花朵慢慢开放"
    python video_generate.py --image https://example.com/photo.jpg --prompt "手舞足蹈" --resolution 720P

用法（查询已有订单）:
    python video_generate.py --query JH819251208164211x1hC5

API Key 配置（任选其一，优先级从高到低）:
    1. 环境变量: export JUHE_VIDEO_KEY=your_api_key
    2. 脚本同目录的 .env 文件: JUHE_VIDEO_KEY=your_api_key
    3. 直接传参: python video_generate.py --key your_api_key "提示词"

免费申请 API Key: https://www.juhe.cn/docs/api/id/827
"""

import sys
import os
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

TEXT2VIDEO_URL = "https://gpt.juhe.cn/text2video/generate"
IMAGE2VIDEO_URL = "https://gpt.juhe.cn/text2video/baseimg"
QUERY_URL = "https://gpt.juhe.cn/text2video/query"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/827"

MAX_PROMPT_LEN = 500
MAX_NEGATIVE_LEN = 300
POLL_INTERVAL = 15
MAX_WAIT_SECONDS = 600

VALID_RESOLUTIONS = {"480P", "720P", "1080P"}
VALID_PROPORTIONS = {"16:9", "9:16", "1:1", "4:3", "3:4"}
VALID_DURATIONS = {"5", "10", "15"}

RESOLUTION_COST = {"480P": 1, "720P": 2, "1080P": 3}


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_VIDEO_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_VIDEO_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def _post_json(url: str, params: dict, timeout: int = 30) -> dict:
    """发送 POST 请求并返回 JSON"""
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"网络请求失败: {e}") from e


def create_text2video(
    prompt: str,
    api_key: str,
    resolution: str = "480P",
    proportion: str = "16:9",
    duration: str = "5",
    negative_prompt: str = "",
    prompt_extend: int = 1,
    notify_url: str = "",
) -> dict:
    """调用文生视频接口，提交生成任务"""
    if len(prompt) > MAX_PROMPT_LEN:
        prompt = prompt[:MAX_PROMPT_LEN]
        print(f"⚠️  提示词超过 {MAX_PROMPT_LEN} 字符，已自动截断")

    params = {
        "key": api_key,
        "prompt": prompt,
        "resolution": resolution,
        "proportion": proportion,
        "duration": duration,
        "promptExtend": prompt_extend,
    }
    if negative_prompt:
        params["negativePrompt"] = negative_prompt[:MAX_NEGATIVE_LEN]
    if notify_url:
        params["notifyUrl"] = notify_url

    try:
        result = _post_json(TEXT2VIDEO_URL, params)
    except RuntimeError as e:
        return {"success": False, "error": str(e)}

    return _parse_create_response(result)


def create_image2video(
    image: str,
    prompt: str,
    api_key: str,
    resolution: str = "480P",
    duration: str = "5",
    negative_prompt: str = "",
    audio_url: str = "",
    prompt_extend: int = 1,
    notify_url: str = "",
) -> dict:
    """调用图生视频接口，提交生成任务"""
    if len(prompt) > MAX_PROMPT_LEN:
        prompt = prompt[:MAX_PROMPT_LEN]
        print(f"⚠️  提示词超过 {MAX_PROMPT_LEN} 字符，已自动截断")

    params = {
        "key": api_key,
        "prompt": prompt,
        "image": image,
        "resolution": resolution,
        "duration": duration,
        "promptExtend": prompt_extend,
    }
    if negative_prompt:
        params["negativePrompt"] = negative_prompt[:MAX_NEGATIVE_LEN]
    if audio_url:
        params["audioUrl"] = audio_url
    if notify_url:
        params["notifyUrl"] = notify_url

    try:
        result = _post_json(IMAGE2VIDEO_URL, params)
    except RuntimeError as e:
        return {"success": False, "error": str(e)}

    return _parse_create_response(result)


def _parse_create_response(result: dict) -> dict:
    """解析创建任务的响应"""
    error_code = result.get("error_code", -1)
    if error_code == 0:
        res = result.get("result", {})
        return {
            "success": True,
            "orderid": res.get("orderid", ""),
            "orderstatus": res.get("orderstatus", "PENDING"),
        }

    reason = result.get("reason", "提交失败")
    hint = _error_hint(error_code)
    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def query_result(orderid: str, api_key: str) -> dict:
    """查询视频生成结果（POST 方式）"""
    params = {
        "key": api_key,
        "orderId": orderid,
    }

    try:
        result = _post_json(QUERY_URL, params)
    except RuntimeError as e:
        return {"success": False, "error": str(e)}

    error_code = result.get("error_code", -1)
    if error_code == 0:
        res = result.get("result", {})
        return {
            "success": True,
            "orderid": res.get("orderid", orderid),
            "orderstatus": res.get("orderstatus", ""),
            "videourl": res.get("videourl", ""),
            "code": res.get("code", 0),
            "message": res.get("message", ""),
        }

    reason = result.get("reason", "查询失败")
    hint = _error_hint(error_code)
    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def _error_hint(error_code: int) -> str:
    """根据错误码返回提示信息"""
    hints = {
        10001: f"\n   请检查 API Key 是否正确，免费申请：{REGISTER_URL}",
        10002: f"\n   该 Key 无请求权限，请前往 {REGISTER_URL} 申请接口",
        10012: "\n   今日调用次数已用尽，请升级套餐",
        282701: "\n   参数错误，请检查提示词、分辨率、时长或图片链接是否符合要求",
        282702: "\n   订单不存在，请确认 orderid 是否正确",
        282703: "\n   网络错误，请稍后重试",
        282704: "\n   查询失败，请稍后重试",
        282705: "\n   数据源异常，请稍后重试",
    }
    return hints.get(error_code, "")


def poll_until_done(orderid: str, api_key: str) -> dict:
    """轮询查询结果，直到生成完成或超时"""
    elapsed = 0
    attempt = 0

    while elapsed < MAX_WAIT_SECONDS:
        attempt += 1
        result = query_result(orderid, api_key)

        if not result["success"]:
            return result

        code = result.get("code", 0)
        status = result["orderstatus"]

        if status == "SUCCEEDED" or code == 1:
            return result
        elif status == "FAILED" or code == 2:
            msg = result.get("message", "视频生成失败")
            return {"success": False, "error": f"生成失败: {msg}"}
        else:
            dots = "." * ((attempt % 3) + 1)
            print(f"\r   状态: {status}{dots:<4} 已等待 {elapsed}s", end="", flush=True)
            time.sleep(POLL_INTERVAL)
            elapsed += POLL_INTERVAL

    return {
        "success": False,
        "error": (
            f"等待超时（>{MAX_WAIT_SECONDS}s），视频仍在生成中\n"
            f"   请稍后使用以下命令查询：\n"
            f"   python video_generate.py --query {orderid}"
        ),
    }


def download_video(url: str, output_dir: Path) -> str | None:
    """下载视频到本地，返回保存路径或 None"""
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"video_{timestamp}.mp4"
    save_path = output_dir / filename

    try:
        print(f"\n📥 正在下载视频...")
        urllib.request.urlretrieve(url, save_path)
        return str(save_path)
    except Exception as e:
        print(f"⚠️  视频下载失败: {e}")
        return None


def calc_cost(resolution: str, duration: str) -> int:
    """计算本次生成消耗的次数"""
    return RESOLUTION_COST.get(resolution, 1) * int(duration)


def parse_args(args: list) -> dict:
    """解析命令行参数"""
    result = {
        "cli_key": None,
        "prompt": None,
        "image": None,
        "resolution": "480P",
        "proportion": "16:9",
        "duration": "5",
        "negative": "",
        "audio": "",
        "no_extend": False,
        "notify_url": "",
        "output": None,
        "no_download": False,
        "query": None,
        "error": None,
    }

    i = 0
    positional = []

    while i < len(args):
        arg = args[i]

        def next_val(flag):
            nonlocal i
            if i + 1 < len(args):
                val = args[i + 1]
                i += 2
                return val
            result["error"] = f"错误: {flag} 后需要提供值"
            return None

        if arg == "--key":
            v = next_val("--key"); result["cli_key"] = v if v else result["cli_key"]
        elif arg == "--image":
            v = next_val("--image"); result["image"] = v
        elif arg == "--prompt":
            v = next_val("--prompt"); result["prompt"] = v
        elif arg == "--resolution":
            v = next_val("--resolution")
            if v:
                if v.upper() not in VALID_RESOLUTIONS:
                    result["error"] = f"错误: 无效的分辨率 '{v}'，可选: 480P、720P、1080P"
                    return result
                result["resolution"] = v.upper()
        elif arg == "--proportion":
            v = next_val("--proportion")
            if v:
                if v not in VALID_PROPORTIONS:
                    result["error"] = f"错误: 无效的宽高比 '{v}'，可选: 16:9、9:16、1:1、4:3、3:4"
                    return result
                result["proportion"] = v
        elif arg == "--duration":
            v = next_val("--duration")
            if v:
                if v not in VALID_DURATIONS:
                    result["error"] = f"错误: 无效的时长 '{v}'，可选: 5、10、15（秒）"
                    return result
                result["duration"] = v
        elif arg == "--negative":
            v = next_val("--negative"); result["negative"] = v or ""
        elif arg == "--audio":
            v = next_val("--audio"); result["audio"] = v or ""
        elif arg == "--notify-url":
            v = next_val("--notify-url"); result["notify_url"] = v or ""
        elif arg == "--no-extend":
            result["no_extend"] = True
            i += 1
        elif arg == "--output":
            v = next_val("--output"); result["output"] = v
        elif arg == "--no-download":
            result["no_download"] = True
            i += 1
        elif arg == "--query":
            v = next_val("--query"); result["query"] = v
        else:
            positional.append(arg)
            i += 1

        if result["error"]:
            return result

    if positional and result["prompt"] is None:
        result["prompt"] = " ".join(positional)

    # 参数组合校验
    if result["query"] is None:
        if result["image"] is None and result["prompt"] is None:
            result["error"] = (
                "错误: 请提供提示词（文生视频）或 --image 参数（图生视频）\n"
                "用法: python video_generate.py [选项] <提示词>\n"
                '示例: python video_generate.py "夕阳下的海边，写实风格"\n'
                '      python video_generate.py --image https://example.com/img.jpg --prompt "手舞足蹈"\n'
                f"\n免费申请 API Key: {REGISTER_URL}"
            )
            return result

        if result["image"] is not None and result["prompt"] is None:
            result["error"] = "错误: 图生视频模式下 --prompt 为必填参数，请描述期望的动态效果"
            return result

        res = result["resolution"]
        dur = result["duration"]
        prop = result["proportion"]

        if dur == "15" and res == "480P":
            result["error"] = "错误: 480P 分辨率不支持 15 秒时长，请选择 5 或 10 秒，或将分辨率升级为 720P/1080P"
            return result

        if result["image"] is None and prop in ("4:3", "3:4") and res == "480P":
            result["error"] = f"错误: 480P 分辨率不支持 {prop} 宽高比，请选择其他宽高比或升级分辨率"
            return result

    return result


def print_usage():
    print("用法: python video_generate.py [选项] <提示词>")
    print()
    print("文生视频示例:")
    print('  python video_generate.py "夕阳下的海边，海浪轻柔拍打礁石"')
    print('  python video_generate.py "城市夜景，霓虹灯闪烁" --resolution 1080P --duration 10')
    print('  python video_generate.py "唯美樱花" --proportion 9:16 --negative "落叶、枯枝"')
    print()
    print("图生视频示例:")
    print('  python video_generate.py --image https://example.com/photo.jpg --prompt "手舞足蹈"')
    print('  python video_generate.py --image https://example.com/photo.jpg --prompt "花朵开放" --resolution 720P')
    print()
    print("查询已有订单:")
    print("  python video_generate.py --query JH819251208164211x1hC5")
    print()
    print("通用选项:")
    print("  --resolution <档位>  分辨率: 480P(默认,1次/秒)、720P(2次/秒)、1080P(3次/秒)")
    print("  --duration <秒>      时长: 5(默认)、10、15（480P不支持15秒）")
    print("  --negative <文字>    反向提示词，描述不希望出现的内容（最多300字）")
    print("  --no-extend          关闭提示词智能改写（默认开启）")
    print("  --output <目录>      视频保存目录（默认：output/）")
    print("  --no-download        仅返回链接，不下载视频")
    print("  --key <KEY>          临时传入 API Key")
    print()
    print("文生视频专属选项:")
    print("  --proportion <比例>  宽高比: 16:9(默认)、9:16、1:1、4:3、3:4（480P不支持4:3/3:4）")
    print()
    print("图生视频专属选项:")
    print("  --audio <URL>        配音文件链接（wav/mp3，3-30秒，不超过10MB）")
    print()
    print("计费说明: 次数消耗 = 分辨率系数 × 时长（秒）")
    print("  示例: 720P × 10秒 = 2 × 10 = 20次")
    print(f"\n免费申请 API Key: {REGISTER_URL}")


def main():
    args = sys.argv[1:]

    if not args:
        print_usage()
        sys.exit(1)

    parsed = parse_args(args)
    if parsed["error"]:
        print(parsed["error"])
        sys.exit(1)

    api_key = load_api_key(parsed["cli_key"])
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量: export JUHE_VIDEO_KEY=your_api_key")
        print("   2. .env 文件: 在脚本目录创建 .env，写入 JUHE_VIDEO_KEY=your_api_key")
        print("   3. 命令行参数: python video_generate.py --key your_api_key <提示词>")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    output_dir = (
        Path(parsed["output"]).expanduser().resolve()
        if parsed["output"]
        else Path(__file__).parent / "output"
    )

    # 仅查询已有订单
    if parsed["query"]:
        orderid = parsed["query"]
        print(f"\n🔍 查询订单 {orderid} 的生成结果...\n")
        result = query_result(orderid, api_key)
        if not result["success"]:
            print(f"❌ 查询失败: {result['error']}")
            sys.exit(1)
        _handle_result(result, output_dir, parsed["no_download"])
        return

    resolution = parsed["resolution"]
    duration = parsed["duration"]
    prompt_extend = 0 if parsed["no_extend"] else 1
    cost = calc_cost(resolution, duration)

    # 提交生成任务
    if parsed["image"]:
        imgurl = parsed["image"]
        prompt = parsed["prompt"]
        print(f"\n🎬 提交图生视频任务...")
        print(f"   图片链接: {imgurl}")
        print(f"   运动描述: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
        print(f"   分辨率: {resolution}  时长: {duration}秒  预计消耗: {cost}次")
        print()
        submit_result = create_image2video(
            image=imgurl,
            prompt=prompt,
            api_key=api_key,
            resolution=resolution,
            duration=duration,
            negative_prompt=parsed["negative"],
            audio_url=parsed["audio"],
            prompt_extend=prompt_extend,
            notify_url=parsed["notify_url"],
        )
    else:
        prompt = parsed["prompt"]
        proportion = parsed["proportion"]
        print(f"\n🎬 提交文生视频任务...")
        print(f"   提示词: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
        print(f"   分辨率: {resolution}  宽高比: {proportion}  时长: {duration}秒  预计消耗: {cost}次")
        print()
        submit_result = create_text2video(
            prompt=prompt,
            api_key=api_key,
            resolution=resolution,
            proportion=proportion,
            duration=duration,
            negative_prompt=parsed["negative"],
            prompt_extend=prompt_extend,
            notify_url=parsed["notify_url"],
        )

    if not submit_result["success"]:
        print(f"❌ 任务提交失败: {submit_result['error']}")
        sys.exit(1)

    orderid = submit_result["orderid"]
    print(f"✅ 任务已提交，订单号: {orderid}")
    print(f"   （如需中断，可稍后用 --query {orderid} 重新查询）\n")

    # 轮询等待生成完成
    print(f"⏳ 等待视频生成（视频通常需 1-5 分钟，最长等待 {MAX_WAIT_SECONDS}s）...")
    poll_result = poll_until_done(orderid, api_key)
    print()

    if not poll_result["success"]:
        print(f"❌ {poll_result['error']}")
        sys.exit(1)

    _handle_result(poll_result, output_dir, parsed["no_download"])


def _handle_result(result: dict, output_dir: Path, no_download: bool) -> None:
    """处理生成成功的结果：展示链接并可选下载"""
    video_url = result.get("videourl", "")
    orderid = result.get("orderid", "")
    status = result.get("orderstatus", "")

    if not video_url:
        if status in ("PENDING", "RUNNING"):
            print(f"⏳ 视频仍在生成中（状态: {status}），请稍后查询：")
            if orderid:
                print(f"   python video_generate.py --query {orderid}")
        else:
            print(f"⚠️  未获取到视频链接（状态: {status}）")
        return

    print("✅ 视频生成成功！")
    if orderid:
        print(f"   订单号: {orderid}")
    print(f"   在线链接: {video_url}")
    print(f"   ⚠️  链接有效期为 24 小时，请及时下载保存")

    if not no_download:
        save_path = download_video(video_url, output_dir)
        if save_path:
            print(f"   本地文件: {save_path}")
        else:
            print("   请手动访问上方链接保存视频")
    else:
        print("\n（已跳过下载，请手动访问链接保存视频）")

    print()


if __name__ == "__main__":
    main()
