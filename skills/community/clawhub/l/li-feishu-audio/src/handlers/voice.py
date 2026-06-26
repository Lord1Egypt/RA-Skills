#!/usr/bin/env python3
"""
Li Feishu Audio - Voice Handler
处理飞书语音消息的接收和回复
"""

import os
import sys
import json
import subprocess
import tempfile
import asyncio
from pathlib import Path

# 获取技能目录
SKILL_DIR = Path(__file__).parent.parent.parent
VENV_DIR = SKILL_DIR / ".venv"
PYTHON_BIN = VENV_DIR / "bin" / "python"

def log(msg: str):
    """打印日志到 stderr"""
    print(f"[LiFeishuAudio] {msg}", file=sys.stderr, flush=True)

def transcribe_audio(audio_path: str) -> str:
    """使用 fast-whisper 将语音转文字"""
    log(f"开始语音转文字: {audio_path}")

    model_dir = os.path.expanduser("~/.fast-whisper-models")

    cmd = [
        str(PYTHON_BIN), "-m", "faster_whisper",
        audio_path,
        "--model", "tiny",
        "--model_dir", model_dir,
        "--language", "zh",
        "--output_format", "txt"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            log(f"语音识别失败: {result.stderr}")
            return ""

        # 解析输出
        text = result.stdout.strip()
        log(f"识别结果: {text}")
        return text
    except Exception as e:
        log(f"语音识别异常: {e}")
        return ""

def text_to_speech(text: str, output_path: str) -> bool:
    """使用 edge-tts 将文字转为语音"""
    log(f"开始文字转语音: {text[:50]}...")

    # 创建临时 mp3 文件
    temp_mp3 = tempfile.mktemp(suffix=".mp3")

    # 生成 TTS
    tts_script = f"""
import asyncio
import edge_tts

async def main():
    communicate = edge_tts.Communicate({repr(text)}, "zh-CN-XiaoxiaoNeural")
    await communicate.save({repr(temp_mp3)})

asyncio.run(main())
"""

    try:
        result = subprocess.run(
            [str(PYTHON_BIN), "-c", tts_script],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            log(f"TTS 生成失败: {result.stderr}")
            return False

        # 转换为 opus 格式 (飞书需要 48kHz opus)
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", temp_mp3,
            "-ar", "48000", "-ac", "1",
            "-c:a", "libopus", "-b:a", "24k",
            output_path
        ]

        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=30)

        # 清理临时文件
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)

        if result.returncode != 0:
            log(f"FFmpeg 转换失败: {result.stderr}")
            return False

        log(f"语音生成成功: {output_path}")
        return True

    except Exception as e:
        log(f"TTS 异常: {e}")
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)
        return False

def get_audio_duration(file_path: str) -> int:
    """获取音频时长（毫秒）"""
    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            duration_sec = float(result.stdout.strip())
            return int(duration_sec * 1000)  # 转换为毫秒
    except Exception as e:
        log(f"获取音频时长失败: {e}")
    return 0

def send_voice_reply(reply_text: str, user_id: str = None) -> tuple[bool, int]:
    """发送语音回复到飞书，返回 (是否成功, 时长毫秒)"""
    output_opus = "/tmp/reply.opus"

    # 生成语音文件
    if not text_to_speech(reply_text, output_opus):
        log("生成语音文件失败")
        return False, 0

    if not os.path.exists(output_opus):
        log(f"语音文件不存在: {output_opus}")
        return False, 0

    # 检查文件大小
    file_size = os.path.getsize(output_opus)
    log(f"语音文件大小: {file_size} bytes")

    if file_size == 0:
        log("语音文件为空")
        return False, 0

    # 获取音频时长
    duration = get_audio_duration(output_opus)
    log(f"音频时长: {duration}ms")

    # 飞书语音发送由 OpenClaw extension 处理
    # 这里只需要确保文件生成成功
    log(f"语音回复已生成: {output_opus}")
    return True, duration

def main():
    """主处理函数"""
    log("=== Li Feishu Audio Handler 启动 ===")

    # 读取输入
    input_data = sys.stdin.read()
    log(f"收到输入: {input_data[:200]}...")

    try:
        data = json.loads(input_data)
    except json.JSONDecodeError as e:
        log(f"JSON 解析失败: {e}")
        print(json.dumps({"error": "Invalid JSON input"}))
        return 1

    # 获取消息内容
    message = data.get("message", "")
    attachments = data.get("attachments", [])

    log(f"消息内容: {message}")
    log(f"附件数量: {len(attachments)}")

    # 如果有语音附件，先进行语音识别
    transcribed_text = ""
    if attachments:
        for attachment in attachments:
            if attachment.get("type") == "audio" or attachment.get("name", "").endswith((".opus", ".mp3", ".wav", ".m4a")):
                audio_path = attachment.get("path") or attachment.get("localPath")
                if audio_path and os.path.exists(audio_path):
                    log(f"处理语音附件: {audio_path}")
                    transcribed_text = transcribe_audio(audio_path)
                    if transcribed_text:
                        message = transcribed_text
                        break

    # 构建回复
    if message:
        reply_text = f"收到你的消息: {message}"
    else:
        reply_text = "你好！我收到了你的语音消息，但未能识别内容。"

    log(f"准备回复: {reply_text}")

    # 生成语音回复
    voice_ok, duration = send_voice_reply(reply_text)
    if voice_ok:
        # 输出结果，包含语音文件路径和时长
        result = {
            "text": reply_text,
            "voice_path": "/tmp/reply.opus",
            "voice_duration": duration,
            "transcribed": transcribed_text if attachments else ""
        }
    else:
        # 仅文字回复
        result = {
            "text": reply_text + "\n\n(语音生成失败，仅发送文字)",
            "error": "Voice generation failed"
        }

    print(json.dumps(result, ensure_ascii=False))
    log("=== 处理完成 ===")
    return 0

if __name__ == "__main__":
    sys.exit(main())
