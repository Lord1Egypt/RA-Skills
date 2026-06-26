#!/usr/bin/env python3
"""
MiniMax TTS streaming player (WebSocket + ffplay).

Usage:
  python3 stream_play.py --text "要播放的文本" [--voice male-qn-jingying] \
      [--speed 1.0] [--vol 1.0] [--pitch 0]

功能：
  - 通过 WebSocket 连接 MiniMax TTS API，实现真正的流式音频生成
  - 音频 chunk 实时通过管道喂给 ffplay，实现边生成边播放
  - 无需等待完整音频生成完毕，首个音频包到达即开始播放
  - 适合 channel=webchat 场景：直接播放，不生成文件

输出：
  - stdout: "STREAM_PLAY_DONE" (播放完成) 或 "STREAM_PLAY_ERROR: <msg>" (失败)
  - stderr: 日志信息
"""

import argparse
import asyncio
import json
import os
import shutil
import signal
import ssl
import subprocess
import sys
from datetime import date

try:
    import websockets
except ImportError:
    print("[ERROR] 缺少 websockets 库，请运行: pip3 install websockets", file=sys.stderr)
    sys.exit(1)

# ------------------ 配置区（可被命令行参数覆盖）------------------
# TODO: 初始化时填入实际值（与 generate.py 保持一致）
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.minimaxi.com"  # CN: api.minimaxi.com
# ----------------------------------------------------------------

DEFAULT_VOICE = "male-qn-jingying"
DEFAULT_SPEED = 1.0
DEFAULT_VOL = 1.0
DEFAULT_PITCH = 0
DEFAULT_MODEL = "speech-2.8-hd"

# 常用声优（与 generate.py 保持一致）
COMMON_VOICES = {
    "male-qn-jingying": "精英青年音色（推荐）",
    "female-tianmei": "甜美女性音色",
    "male-qn-badao": "霸道青年音色",
    "female-yujie": "御姐音色",
    "male-qn-daxuesheng": "青年大学生音色",
    "female-shaonv": "少女音色",
}


def check_ffplay():
    """检查 ffplay 是否可用"""
    if shutil.which("ffplay") is None:
        print("[ERROR] ffplay 未安装。请安装 ffmpeg：", file=sys.stderr)
        print("  macOS:   brew install ffmpeg", file=sys.stderr)
        print("  Ubuntu:  sudo apt install ffmpeg", file=sys.stderr)
        print("  Windows: https://ffmpeg.org/download.html", file=sys.stderr)
        sys.exit(1)


def start_ffplay():
    """启动 ffplay 子进程，从 stdin 读取音频数据播放"""
    try:
        process = subprocess.Popen(
            [
                "ffplay",
                "-nodisp",       # 不显示窗口
                "-autoexit",     # 数据播完自动退出
                "-loglevel", "error",  # 只输出错误
                "-f", "mp3",     # 输入格式为 mp3
                "-",             # 从 stdin 读取
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        print("[INFO] ffplay 播放器已启动", file=sys.stderr)
        return process
    except FileNotFoundError:
        print("[ERROR] ffplay 未找到", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 启动 ffplay 失败: {e}", file=sys.stderr)
        sys.exit(1)


def stop_ffplay(process):
    """安全关闭 ffplay"""
    if process is None:
        return
    try:
        if process.stdin and not process.stdin.closed:
            process.stdin.close()
        process.wait(timeout=30)
    except subprocess.TimeoutExpired:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
    except Exception:
        pass


async def stream_and_play(
    text: str,
    voice: str = DEFAULT_VOICE,
    speed: float = DEFAULT_SPEED,
    vol: float = DEFAULT_VOL,
    pitch: float = DEFAULT_PITCH,
    model: str = DEFAULT_MODEL,
    api_key: str = API_KEY,
    base_url: str = BASE_URL,
    save_path: str = None,
):
    """
    通过 WebSocket 流式获取音频并实时播放。

    流程:
        1. 建立 WebSocket 连接
        2. 发送 task_start（配置音色、音频参数）
        3. 发送 task_continue（传入文本）
        4. 接收音频 chunks，实时喂给 ffplay
        5. 收到 is_final=true 后发送 task_finish
    """

    # 检查 API Key
    if api_key == "YOUR_API_KEY_HERE" or not api_key:
        print("[ERROR] API Key 未配置，请先运行 init 流程", file=sys.stderr)
        return False

    # 参数校验
    if not text or len(text.strip()) == 0:
        print("[ERROR] 文本不能为空", file=sys.stderr)
        return False

    if len(text) > 10000:
        print(f"[ERROR] 文本长度 {len(text)} 超过 10000 字符限制", file=sys.stderr)
        return False

    # 构建 WebSocket URL
    ws_host = base_url.replace("https://", "").replace("http://", "")
    ws_url = f"wss://{ws_host}/ws/v1/t2a_v2"

    voice_name = COMMON_VOICES.get(voice, voice)
    print(f"[INFO] 流式播放模式", file=sys.stderr)
    print(f"[INFO] 使用声优: {voice} ({voice_name})", file=sys.stderr)
    print(f"[INFO] 语速: {speed}, 音量: {vol}, 音调: {pitch}", file=sys.stderr)
    print(f"[INFO] 文本长度: {len(text)} 字符", file=sys.stderr)

    # SSL 配置
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # 启动 ffplay
    player = start_ffplay()

    # 可选：同时保存到文件
    audio_buffer = bytearray() if save_path else None

    chunk_count = 0
    total_bytes = 0

    try:
        # 1. 建立 WebSocket 连接
        headers = {"Authorization": f"Bearer {api_key}"}
        async with websockets.connect(
            ws_url,
            additional_headers=headers,
            ssl=ssl_context,
        ) as ws:
            # 等待 connected_success
            resp = json.loads(await ws.recv())
            if resp.get("event") != "connected_success":
                print(f"[ERROR] 连接失败: {resp}", file=sys.stderr)
                stop_ffplay(player)
                return False
            print("[INFO] WebSocket 连接成功", file=sys.stderr)

            # 2. 发送 task_start
            task_start_msg = {
                "event": "task_start",
                "model": model,
                "voice_setting": {
                    "voice_id": voice,
                    "speed": speed,
                    "vol": vol,
                    "pitch": pitch,
                },
                "audio_setting": {
                    "sample_rate": 32000,
                    "bitrate": 128000,
                    "format": "mp3",  # WebSocket 流式仅支持 mp3
                    "channel": 1,
                },
            }
            await ws.send(json.dumps(task_start_msg))

            resp = json.loads(await ws.recv())
            if resp.get("event") != "task_started":
                err_msg = resp.get("base_resp", {}).get("status_msg", str(resp))
                print(f"[ERROR] 任务启动失败: {err_msg}", file=sys.stderr)
                stop_ffplay(player)
                return False
            print("[INFO] 任务已启动", file=sys.stderr)

            # 3. 发送 task_continue（传入文本）
            await ws.send(json.dumps({
                "event": "task_continue",
                "text": text,
            }))
            print("[INFO] 文本已发送，等待音频流...", file=sys.stderr)

            # 4. 接收音频 chunks 并实时播放
            while True:
                try:
                    resp = json.loads(await asyncio.wait_for(ws.recv(), timeout=60))
                except asyncio.TimeoutError:
                    print("[ERROR] 接收超时", file=sys.stderr)
                    break

                # 检查错误
                if resp.get("event") == "task_failed":
                    err_msg = resp.get("base_resp", {}).get("status_msg", "未知错误")
                    err_code = resp.get("base_resp", {}).get("status_code", -1)
                    print(f"[ERROR] 任务失败: code={err_code}, msg={err_msg}", file=sys.stderr)
                    break

                # 提取音频数据
                audio_hex = resp.get("data", {}).get("audio")
                if audio_hex:
                    audio_bytes = bytes.fromhex(audio_hex)
                    chunk_count += 1
                    total_bytes += len(audio_bytes)

                    # 喂给 ffplay
                    try:
                        if player.stdin and not player.stdin.closed:
                            player.stdin.write(audio_bytes)
                            player.stdin.flush()
                    except BrokenPipeError:
                        print("[WARN] ffplay 管道已关闭", file=sys.stderr)
                        break

                    # 可选保存
                    if audio_buffer is not None:
                        audio_buffer.extend(audio_bytes)

                    if chunk_count % 5 == 0:
                        print(f"[INFO] 已接收 {chunk_count} chunks ({total_bytes} bytes)", file=sys.stderr)

                # 检查是否完成
                if resp.get("is_final"):
                    print(f"[INFO] 音频流完成: 共 {chunk_count} chunks, {total_bytes} bytes", file=sys.stderr)
                    break

            # 5. 发送 task_finish
            try:
                await ws.send(json.dumps({"event": "task_finish"}))
            except Exception:
                pass

    except Exception as e:
        print(f"[ERROR] 流式播放失败: {e}", file=sys.stderr)
        stop_ffplay(player)
        return False

    # 关闭 ffplay（等待播放完成）
    print("[INFO] 等待播放完成...", file=sys.stderr)
    stop_ffplay(player)

    # 可选：保存到文件
    if save_path and audio_buffer:
        try:
            save_dir = os.path.dirname(save_path)
            if save_dir:
                os.makedirs(save_dir, exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(audio_buffer)
            print(f"[INFO] 音频同时保存到: {save_path}", file=sys.stderr)
        except Exception as e:
            print(f"[WARN] 保存文件失败: {e}", file=sys.stderr)

    print(f"[SUCCESS] 流式播放完成", file=sys.stderr)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="MiniMax TTS - 流式播放（WebSocket + ffplay）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--text", "-t",
        required=True,
        help="要播放的文本（最长 10000 字符）"
    )
    parser.add_argument(
        "--voice", "-v",
        default=DEFAULT_VOICE,
        help=f"声优 ID（默认: {DEFAULT_VOICE}）"
    )
    parser.add_argument(
        "--speed", "-s",
        type=float,
        default=DEFAULT_SPEED,
        help=f"语速 0.5-2.0（默认: {DEFAULT_SPEED}）"
    )
    parser.add_argument(
        "--vol",
        type=float,
        default=DEFAULT_VOL,
        help=f"音量 0-10（默认: {DEFAULT_VOL}）"
    )
    parser.add_argument(
        "--pitch",
        type=float,
        default=DEFAULT_PITCH,
        help=f"音调 -12 到 12（默认: {DEFAULT_PITCH}）"
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"模型（默认: {DEFAULT_MODEL}）"
    )
    parser.add_argument(
        "--save", "-o",
        default=None,
        help="同时保存到文件（可选，MP3 格式）"
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="API Key（默认使用文件顶部配置）"
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="API Base URL（默认使用文件顶部配置）"
    )

    args = parser.parse_args()

    # 检查 ffplay
    check_ffplay()

    # 覆盖全局配置
    final_api_key = args.api_key if args.api_key else API_KEY
    final_base_url = args.base_url if args.base_url else BASE_URL

    # 验证参数范围
    if not 0.5 <= args.speed <= 2.0:
        print("[ERROR] 语速必须在 0.5-2.0 之间", file=sys.stderr)
        sys.exit(1)
    if not 0 < args.vol <= 10:
        print("[ERROR] 音量必须在 0-10 之间（0不含）", file=sys.stderr)
        sys.exit(1)
    if not -12 <= args.pitch <= 12:
        print("[ERROR] 音调必须在 -12 到 12 之间", file=sys.stderr)
        sys.exit(1)

    # 运行流式播放
    success = asyncio.run(stream_and_play(
        text=args.text,
        voice=args.voice,
        speed=args.speed,
        vol=args.vol,
        pitch=args.pitch,
        model=args.model,
        api_key=final_api_key,
        base_url=final_base_url,
        save_path=args.save,
    ))

    if success:
        print("STREAM_PLAY_DONE")
    else:
        print("STREAM_PLAY_ERROR: 流式播放失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
