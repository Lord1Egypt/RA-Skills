"""
科大讯飞 录音文件转写大模型 API (语音文件 -> 文字)
文档: https://www.xfyun.cn/doc/spark/asr_llm/Ifasr_llm.html

支持格式: mp3/wav/pcm/mp4/m4a/aac/ogg/flac/speex/opus/wma
文件大小: ≤500MB
音频时长: ≤5小时
"""

import os
import sys
import time
import hmac
import hashlib
import base64
import json
import string
import random
import wave
import subprocess
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

# 加载 .env 配置
# 尝试从 skill 根目录加载 .env
skill_root = Path(__file__).parent.parent
if (skill_root / ".env").exists():
    load_dotenv(skill_root / ".env")
else:
    # 兼容旧位置
    load_dotenv(Path(__file__).parent / ".env")

APP_ID = os.getenv("XFYUN_APP_ID")
ACCESS_KEY_ID = os.getenv("XFYUN_ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("XFYUN_ACCESS_KEY_SECRET")

BASE_URL = "https://office-api-ist-dx.iflyaisol.com"
URL_UPLOAD = f"{BASE_URL}/v2/upload"
URL_GET_RESULT = f"{BASE_URL}/v2/getResult"


def generate_random_string(length=16):
    """生成指定长度的随机字符串"""
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def get_datetime():
    """获取格式化的时间字符串 yyyy-MM-dd'T'HH:mm:ss+0800"""
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    return now.strftime("%Y-%m-%dT%H:%M:%S+0800")


def generate_signature(params):
    """
    生成签名:
    1. 排除 signature 字段，按参数名自然排序
    2. URL编码后拼接 key=value&...
    3. HMAC-SHA1 + Base64
    """
    # 过滤掉 signature，按 key 排序
    sorted_params = sorted(
        [(k, v) for k, v in params.items() if k != "signature" and v is not None and v != ""],
        key=lambda x: x[0],
    )

    # URL编码并拼接
    parts = []
    for k, v in sorted_params:
        encoded_key = urllib.parse.quote(str(k), safe="")
        encoded_value = urllib.parse.quote(str(v), safe="")
        parts.append(f"{encoded_key}={encoded_value}")
    base_string = "&".join(parts)

    # HMAC-SHA1 签名
    signature = hmac.new(
        ACCESS_KEY_SECRET.encode("utf-8"),
        base_string.encode("utf-8"),
        hashlib.sha1,
    ).digest()

    return base64.b64encode(signature).decode("utf-8")


def get_audio_duration_ms(file_path):
    """获取音频时长（毫秒）"""
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    # wav 文件直接用 wave 模块读取
    if suffix == ".wav":
        try:
            with wave.open(str(file_path), "rb") as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                duration_ms = int(frames / rate * 1000)
                return duration_ms
        except Exception:
            pass

    # 其他格式用 ffprobe
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)],
            capture_output=True, text=True, timeout=30,
        )
        duration_s = float(result.stdout.strip())
        return int(duration_s * 1000)
    except Exception:
        pass

    # 都失败则根据文件大小粗略估算 (16kHz 16bit mono)
    file_size = file_path.stat().st_size
    return int(file_size / 32000 * 1000)


def upload_file(file_path):
    """上传音频文件，返回 orderId"""
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"[错误] 文件不存在: {file_path}")
        sys.exit(1)

    file_size = file_path.stat().st_size
    duration_ms = get_audio_duration_ms(file_path)
    print(f"[信息] 文件: {file_path.name}, 大小: {file_size / 1024 / 1024:.2f} MB, 时长: {duration_ms / 1000:.1f} 秒")

    date_time = get_datetime()
    sig_random = generate_random_string(16)

    params = {
        "appId": APP_ID,
        "accessKeyId": ACCESS_KEY_ID,
        "dateTime": date_time,
        "signatureRandom": sig_random,
        "fileSize": str(file_size),
        "fileName": file_path.name,
        "duration": str(duration_ms),
        "language": "autodialect",
        "roleType": "0",
        "audioMode": "fileStream",
    }

    signature = generate_signature(params)

    headers = {
        "Content-Type": "application/octet-stream",
        "signature": signature,
    }

    print("[信息] 正在上传文件...")
    with open(file_path, "rb") as f:
        file_data = f.read()

    resp = requests.post(URL_UPLOAD, params=params, headers=headers, data=file_data)
    result = resp.json()
    print(f"[调试] 上传响应: {result}")

    if result.get("code") != "000000":
        print(f"[错误] 上传失败: {result}")
        sys.exit(1)

    order_id = result["content"]["orderId"]
    estimate_time = result["content"].get("taskEstimateTime", 0)
    print(f"[信息] 上传成功, orderId: {order_id}")
    if estimate_time:
        print(f"[信息] 预估处理时间: {estimate_time / 1000:.0f} 秒")

    return order_id, sig_random


def get_result(order_id, sig_random):
    """轮询获取转写结果"""
    print("[信息] 等待转写完成...")
    max_retries = 120
    for i in range(max_retries):
        date_time = get_datetime()

        params = {
            "appId": APP_ID,
            "accessKeyId": ACCESS_KEY_ID,
            "dateTime": date_time,
            "signatureRandom": sig_random,
            "orderId": order_id,
            "resultType": "transfer",
        }

        signature = generate_signature(params)

        headers = {
            "Content-Type": "application/json",
            "signature": signature,
        }

        resp = requests.post(URL_GET_RESULT, params=params, headers=headers)
        result = resp.json()

        if result.get("code") != "000000":
            print(f"[错误] 查询失败: {result}")
            sys.exit(1)

        content = result.get("content", {})
        order_info = content.get("orderInfo", {})
        status = order_info.get("status")

        if status == 4:
            print("[信息] 转写完成!")
            order_result = content.get("orderResult")
            if order_result:
                return order_result
            print("[信息] 转写完成，但结果为空")
            return None
        elif status == -1:
            fail_type = order_info.get("failType", "未知")
            print(f"[错误] 转写失败, failType: {fail_type}")
            return None
        else:
            status_map = {0: "已创建", 3: "处理中"}
            status_text = status_map.get(status, f"处理中({status})")
            estimate = content.get("taskEstimateTime", 0)
            extra = f", 预估剩余 {estimate / 1000:.0f}s" if estimate else ""
            print(f"  [{i + 1}/{max_retries}] 状态: {status_text}{extra}, 等待10秒...")
            time.sleep(10)

    print("[错误] 查询超时")
    return None


def parse_result(result_str):
    """解析转写结果为纯文本"""
    try:
        result_data = json.loads(result_str)
    except json.JSONDecodeError:
        return result_str

    texts = []
    lattice_list = result_data.get("lattice", [])
    for item in lattice_list:
        json_1best = item.get("json_1best", "")
        try:
            best_data = json.loads(json_1best)
            st = best_data.get("st", {})
            rt = st.get("rt", [])
            sentence = ""
            for r in rt:
                ws = r.get("ws", [])
                for w in ws:
                    cw = w.get("cw", [])
                    for c in cw:
                        sentence += c.get("w", "")
            if sentence.strip():
                texts.append(sentence)
        except json.JSONDecodeError:
            continue

    return "\n".join(texts) if texts else result_str


def speech_to_text(audio_file, output_file=None):
    """主函数: 将语音文件转为文字"""
    if not APP_ID or not ACCESS_KEY_ID or not ACCESS_KEY_SECRET:
        print("[错误] 请先在 .env 文件中配置:")
        print("       XFYUN_APP_ID, XFYUN_ACCESS_KEY_ID, XFYUN_ACCESS_KEY_SECRET")
        print("       申请地址: https://www.xfyun.cn")
        sys.exit(1)

    if "your_" in (ACCESS_KEY_ID or "") or "your_" in (ACCESS_KEY_SECRET or ""):
        print("[错误] 请在 .env 中填写真实的 ACCESS_KEY_ID 和 ACCESS_KEY_SECRET")
        sys.exit(1)

    audio_path = Path(audio_file)

    supported = {".mp3", ".wav", ".pcm", ".mp4", ".m4a", ".aac", ".ogg", ".flac", ".speex", ".opus", ".wma"}
    if audio_path.suffix.lower() not in supported:
        print(f"[错误] 不支持的格式: {audio_path.suffix}")
        print(f"       支持的格式: {', '.join(sorted(supported))}")
        sys.exit(1)

    # 1. 上传文件
    order_id, sig_random = upload_file(audio_file)

    # 2. 轮询获取结果
    result = get_result(order_id, sig_random)

    if not result:
        print("[错误] 未获取到转写结果")
        sys.exit(1)

    # 3. 解析结果
    text = parse_result(result)

    # 4. 保存结果
    if output_file is None:
        output_file = audio_path.with_suffix(".txt")

    output_path = Path(output_file)
    output_path.write_text(text, encoding="utf-8")
    print(f"\n[完成] 转写结果已保存到: {output_path}")
    print(f"{'=' * 50}")
    print(text[:500])
    if len(text) > 500:
        print(f"\n... (共 {len(text)} 字符, 完整内容见文件)")
    print(f"{'=' * 50}")

    return text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python speech_to_text.py <音频文件路径> [输出文件路径]")
        print()
        print("示例:")
        print("  python speech_to_text.py recording.mp3")
        print("  python speech_to_text.py meeting.wav output.txt")
        print()
        print("支持格式: mp3, wav, pcm, mp4, m4a, aac, ogg, flac, speex, opus, wma")
        print("文件限制: ≤500MB, ≤5小时")
        sys.exit(0)

    audio = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    speech_to_text(audio, output)
