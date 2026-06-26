"""
MeetingOS - 转录模块
功能：把音频/视频文件转换成文字
支持：本地 Whisper（隐私模式）或 OpenAI 云端转录
"""

import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

# 从环境变量读取配置（只读取，不联网）
PRIVACY_MODE        = os.getenv("MEETINGOS_PRIVACY_MODE", "local")
WHISPER_LOCAL_MODEL = os.getenv("WHISPER_LOCAL_MODEL", "base")
OPENAI_API_KEY      = os.getenv("OPENAI_API_KEY", "")
DOWNLOAD_DIR        = os.getenv("MEETINGOS_DOWNLOAD_DIR", "/tmp/meetingos_recordings")


def extract_audio(video_path: str) -> str:
    """
    从视频文件里提取音频

    参数：
        video_path - 视频文件的本地路径，如 /tmp/meeting.mp4

    返回：
        提取出来的音频文件路径，如 /tmp/meeting_audio.wav

    说明：
        需要电脑上安装了 ffmpeg 才能使用
        安装方法：https://ffmpeg.org/download.html
    """
    # 把视频路径的后缀换成 .wav
    audio_path = video_path.rsplit(".", 1)[0] + "_audio.wav"

    # 调用 ffmpeg 提取音频
    command = [
        "ffmpeg",
        "-i", video_path,        # 输入文件
        "-ar", "16000",          # 采样率 16kHz（Whisper 要求）
        "-ac", "1",              # 单声道
        "-c:a", "pcm_s16le",    # 音频格式
        audio_path,              # 输出文件
        "-y",                    # 自动覆盖已有文件
        "-loglevel", "error"     # 只显示错误信息
    ]

    try:
        subprocess.run(command, check=True)
        print(f"✅ 音频提取成功：{audio_path}")
        return audio_path
    except FileNotFoundError:
        raise RuntimeError(
            "❌ 找不到 ffmpeg，请先安装：\n"
            "   Windows 下载：https://ffmpeg.org/download.html\n"
            "   安装后重启电脑"
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError(f"❌ 音频提取失败：{error}")


def transcribe_local(audio_path: str) -> str:
    """
    使用本地 Whisper 模型转录音频（隐私模式，不联网）

    参数：
        audio_path - 音频文件路径

    返回：
        转录出来的文字内容（字符串）

    说明：
        需要先安装 Whisper：pip install openai-whisper
        模型大小由环境变量 WHISPER_LOCAL_MODEL 控制
        推荐中文会议使用 large-v3 模型（准确率最高）
        base 模型速度快但准确率低
    """
    try:
        import whisper
    except ImportError:
        raise RuntimeError(
            "❌ 未安装 Whisper，请运行：\n"
            "   pip install openai-whisper"
        )

    print(f"🎵 正在用本地 Whisper ({WHISPER_LOCAL_MODEL}) 转录，请稍候...")
    print("   （第一次运行需要下载模型文件，请耐心等待）")

    # 加载模型
    model = whisper.load_model(WHISPER_LOCAL_MODEL)

    # 开始转录
    result = model.transcribe(
        audio_path,
        language=None,          # 自动检测语言（中文/英文/混杂都支持）
        verbose=False
    )

    text = result.get("text", "")
    print(f"✅ 转录完成，共 {len(text)} 个字符")
    return text


def transcribe_cloud(audio_path: str) -> str:
    """
    使用 OpenAI Whisper API 云端转录（需要联网和 API Key）

    参数：
        audio_path - 音频文件路径

    返回：
        转录出来的文字内容（字符串）

    说明：
        需要设置环境变量 OPENAI_API_KEY
        会产生 OpenAI 费用（约 $0.006/分钟）
        数据会发送到 OpenAI 服务器
    """
    if not OPENAI_API_KEY:
        raise ValueError(
            "❌ 未设置 OPENAI_API_KEY\n"
            "   请在 .env 文件里添加：OPENAI_API_KEY=sk-..."
        )

    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError(
            "❌ 未安装 openai 包，请运行：\n"
            "   pip install openai"
        )

    print("☁️  正在使用 OpenAI 云端转录...")

    client = OpenAI(api_key=OPENAI_API_KEY)

    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    text = result.text
    print(f"✅ 云端转录完成，共 {len(text)} 个字符")
    return text


def transcribe(input_path: str) -> str:
    """
    主转录入口：自动判断是视频还是音频，选择本地或云端转录

    参数：
        input_path - 文件路径（支持 .mp4 .mov .avi .mp3 .wav .m4a）

    返回：
        转录出来的完整文字内容

    使用示例：
        text = transcribe("/tmp/meeting.mp4")
        print(text)
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"❌ 文件不存在：{input_path}")

    # 判断文件类型
    extension = input_path.lower().rsplit(".", 1)[-1]
    video_formats = ["mp4", "mov", "avi", "mkv", "webm", "flv"]
    audio_formats = ["mp3", "wav", "m4a", "aac", "ogg", "flac"]

    # 如果是视频，先提取音频
    if extension in video_formats:
        print(f"🎬 检测到视频文件，正在提取音频...")
        audio_path   = extract_audio(input_path)
        need_cleanup = True
    elif extension in audio_formats:
        audio_path   = input_path
        need_cleanup = False
    else:
        raise ValueError(
            f"❌ 不支持的文件格式：.{extension}\n"
            f"   支持的视频格式：{video_formats}\n"
            f"   支持的音频格式：{audio_formats}"
        )

    # 根据隐私模式选择转录方式
    try:
        if PRIVACY_MODE == "local":
            text = transcribe_local(audio_path)
        else:
            text = transcribe_cloud(audio_path)
    finally:
        # 如果是从视频提取的临时音频，处理完后删除
        if need_cleanup and os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"🗑️  已删除临时音频文件")

    return text


# ══════════════════════════════════════════════
# 测试代码
# 只有直接运行这个文件才会执行
# 其他文件导入时不会自动执行（修复安全扫描问题）
# ══════════════════════════════════════════════
if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "test" and len(sys.argv) > 2:
        # 测试转录指定文件
        file_path = sys.argv[2]
        result    = transcribe(file_path)
        print("\n转录结果：")
        print(result[:500])  # 只显示前500字