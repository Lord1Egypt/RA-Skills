"""
音频合成器 - 拼接各段语音 + 混入背景音乐 → 最终 MP3

功能:
  1. 读取 tts_generator.py 输出的各段音频
  2. 读取背景音乐（如有）
  3. 拼接所有语音段（含章节标题播报）
  4. 混入背景音乐（音量可调）
  5. 导出完整 MP3

用法:
  python scripts/audio_assembler.py --segments "tts_result.json" --output "有声书_第一章.mp3"
  python scripts/audio_assembler.py --segments "tts_result.json" --bg-music "bgm.mp3" --output "output.mp3"

依赖:
  pip install pydub imageio-ffmpeg
"""

import argparse
import json
import sys
from pathlib import Path

from pydub import AudioSegment

SCRIPT_DIR = Path(__file__).parent.absolute()
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_PATH = SKILL_DIR / "config.json"

# 通过 imageio-ffmpeg 获取 ffmpeg 路径
try:
    import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
    AudioSegment.ffmpeg = FFMPEG_PATH
    AudioSegment.converter = FFMPEG_PATH
except ImportError:
    FFMPEG_PATH = "ffmpeg"  # 尝试系统 PATH


def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"配置文件不存在: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_audio(file_path):
    """加载音频文件，失败时返回 None"""
    path = Path(file_path)
    if not path.exists():
        print(f"  警告: 音频文件不存在: {file_path}")
        return None
    try:
        return AudioSegment.from_mp3(str(path))
    except Exception as e:
        print(f"  警告: 无法加载音频 {file_path}: {e}")
        return None


def concatenate_segments(segments_info):
    """
    拼接所有语音段。

    参数:
        segments_info: tts_generator.py 输出的分段信息（含 audio_file 路径）

    返回:
        拼接后的 AudioSegment
    """
    combined = AudioSegment.empty()
    segment_details = []

    for seg in segments_info:
        audio = load_audio(seg.get("audio_file", ""))
        if audio is None:
            continue

        seg_type = seg.get("type", "unknown")
        character = seg.get("character", "")

        # 旁白段之间加 0.3 秒静音间隔
        # 对话段之间加 0.1 秒间隔
        silence_ms = 300 if seg_type == "narration" else 100

        if len(combined) > 0:
            combined += AudioSegment.silent(duration=silence_ms)

        combined += audio

        segment_details.append({
            "index": seg.get("index"),
            "type": seg_type,
            "character": character,
            "duration_ms": len(audio),
            "silence_before_ms": silence_ms if len(combined) > len(audio) + silence_ms else 0,
        })

    return combined, segment_details


def mix_background_music(voice_audio, bg_music_path, bg_volume=0.15):
    """
    将背景音乐混入语音。

    参数:
        voice_audio: 拼接后的语音 AudioSegment
        bg_music_path: 背景音乐文件路径
        bg_volume: 背景音乐音量比例 (0.0~1.0)

    返回:
        混音后的 AudioSegment
    """
    if not bg_music_path:
        return voice_audio

    bg = load_audio(bg_music_path)
    if bg is None:
        return voice_audio

    # 背景音乐降音量
    bg = bg - (20 * (1 - bg_volume))

    # 如果背景音乐比语音短，循环播放
    if len(bg) < len(voice_audio):
        repeats = (len(voice_audio) // len(bg)) + 1
        bg = bg * repeats

    # 裁剪到和语音一样长
    bg = bg[:len(voice_audio)]

    # 淡入淡出（避免突兀开始/结束）
    fade_duration = 3000  # 3 秒
    if len(bg) > fade_duration * 2:
        bg = bg.fade_in(fade_duration).fade_out(fade_duration)

    # 混音
    mixed = voice_audio.overlay(bg)
    return mixed


def assemble(
    segments_info,
    output_path,
    bg_music_path=None,
    bg_volume=0.15,
):
    """
    完整音频合成流程。

    参数:
        segments_info: tts_generator.py 输出的分段列表
        output_path: 输出 MP3 文件路径
        bg_music_path: 背景音乐路径（可选）
        bg_volume: 背景音乐音量

    返回:
        最终音频信息
    """
    # 1. 拼接语音
    print("[1/3] 拼接语音段...")
    voice_audio, details = concatenate_segments(segments_info)
    print(f"      语音总时长: {len(voice_audio) / 1000:.1f} 秒")

    if len(voice_audio) == 0:
        raise ValueError("没有有效的音频段可拼接")

    # 2. 混入背景音乐
    if bg_music_path:
        print(f"[2/3] 混入背景音乐: {bg_music_path}")
        print(f"      背景音量: {int(bg_volume * 100)}%")
        final_audio = mix_background_music(voice_audio, bg_music_path, bg_volume)
    else:
        print("[2/3] 未使用背景音乐")
        final_audio = voice_audio

    # 3. 导出
    print(f"[3/3] 导出 MP3: {output_path}")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_audio.export(str(output_path), format="mp3", bitrate="256k")

    total_duration = len(final_audio)
    print(f"\n完成! 有声书已保存: {output_path}")
    print(f"总时长: {total_duration / 1000:.1f} 秒 ({total_duration / 60000:.1f} 分钟)")

    return {
        "output_file": str(output_path),
        "duration_seconds": round(total_duration / 1000, 1),
        "segment_count": len(segments_info),
        "segments": details,
    }


def main():
    parser = argparse.ArgumentParser(description="有声书音频合成器")
    parser.add_argument("--segments", required=True, help="tts_generator.py 输出的 JSON 文件")
    parser.add_argument("--bg-music", help="背景音乐 MP3 文件路径")
    parser.add_argument("--output", required=True, help="输出 MP3 文件路径")
    args = parser.parse_args()

    config = load_config()

    # 读取分段音频信息
    with open(args.segments, "r", encoding="utf-8") as f:
        tts_result = json.load(f)

    segments_info = tts_result.get("segments", [])
    if not segments_info:
        print("错误: 没有音频分段数据", file=sys.stderr)
        sys.exit(1)

    bg_volume = config.get("bg_music_volume", 0.15)

    result = assemble(
        segments_info=segments_info,
        output_path=args.output,
        bg_music_path=args.bg_music,
        bg_volume=bg_volume,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
