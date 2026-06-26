"""
TTS 生成器 - 调用 MiniMax TTS API 逐段生成语音

功能:
  1. 接收分段数据（从 chapter_analyzer.py 输出）
  2. 按角色分配音色，逐段调用 MiniMax TTS
  3. 下载每段音频 MP3

用法:
  python scripts/tts_generator.py --segments-file "analysis.json" --output-dir "temp_audio/"

语音映射规则:
  - title / narration → narration_voice（旁白音色）
  - 男性角色 → male_voice
  - 女性角色 → female_voice
  - 可在 config.json 中自定义角色-音色映射
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests as req

SCRIPT_DIR = Path(__file__).parent.absolute()
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_PATH = SKILL_DIR / "config.json"

# MiniMax TTS API
TTS_URL = "https://api.minimaxi.com/v1/t2a_v2"


def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"配置文件不存在: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def tts_segment(text, voice_id, api_key, model="speech-2.8-hd", speed=1.0):
    """
    调用 MiniMax TTS 生成单段语音。

    参数:
        text: 要朗读的文本
        voice_id: 音色 ID
        api_key: MiniMax API Key
        model: TTS 模型版本
        speed: 语速 (0.5~2.0)

    返回:
        MP3 音频二进制内容
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": model,
        "text": text,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": 1.0,
        },
        "audio_setting": {
            "sample_rate": 44100,
            "bitrate": 256000,
            "format": "mp3",
        },
    }

    resp = req.post(TTS_URL, headers=headers, json=payload, timeout=120)

    # MiniMax TTS 成功时返回音频二进制，失败时返回 JSON
    content_type = resp.headers.get("Content-Type", "")
    if "audio" in content_type or "octet-stream" in content_type:
        return resp.content
    else:
        # 可能是 JSON 错误响应
        err = resp.json()
        raise RuntimeError(
            f"TTS 调用失败: {err.get('base_resp', {}).get('status_msg', str(err))}"
        )


def guess_voice(character, config):
    """
    根据角色名猜测合适的音色。
    规则: 如果角色名包含常见女性称谓，用女声；否则默认男声。
    用户可在 config.json 的 character_voices 中自定义。
    """
    # 检查是否有自定义映射
    custom_voices = config.get("character_voices", {})
    if character in custom_voices:
        return custom_voices[character]

    # 根据名字推测性别
    female_indicators = ["妹", "姐", "女", "娘", "姑", "婆", "妈", "婶", "嫂", "娜", "丽", "小", "阿"]
    male_indicators = ["哥", "爷", "叔", "伯", "爹", "爸", "兄", "弟"]

    for ind in female_indicators:
        if ind in character:
            return config.get("default_female_voice", "female-shaonv")
    for ind in male_indicators:
        if ind in character:
            return config.get("default_male_voice", "male-qingnian")

    # 默认男声
    return config.get("default_male_voice", "male-qingnian")


def generate_all_segments(segments_data, api_key, config, output_dir):
    """
    为所有分段生成语音。

    参数:
        segments_data: chapter_analyzer.py 输出的数据（含 segments 列表）
        api_key: MiniMax API Key
        config: 完整配置
        output_dir: 临时音频输出目录

    返回:
        带有音频文件路径的分段信息列表
    """
    segments = segments_data.get("segments", [])
    if not segments:
        raise ValueError("没有分段数据")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    tts_model = config.get("tts_model", "speech-2.8-hd")
    narration_voice = config.get("narration_voice", "female-shaonv")
    chapter_intro_voice = config.get("chapter_intro_voice", narration_voice)

    result_segments = []

    for i, seg in enumerate(segments):
        seg_type = seg.get("type", "narration")
        text = seg.get("text", "")
        character = seg.get("character")

        if not text.strip():
            continue

        # 确定音色
        if seg_type == "title":
            voice_id = chapter_intro_voice
        elif seg_type == "narration":
            voice_id = narration_voice
        elif seg_type == "dialogue" and character:
            voice_id = guess_voice(character, config)
        else:
            voice_id = narration_voice

        # 文件名
        filename = f"seg_{i:04d}_{seg_type}_{character or 'narration'}.mp3"
        # 清理文件名中的非法字符
        filename = "".join(c for c in filename if c.isalnum() or c in "._- ")
        filepath = output_dir / filename

        print(f"  生成第 {i + 1}/{len(segments)} 段: [{seg_type}]"
              f"{'(' + character + ')' if character else ''} "
              f"音色={voice_id} 长度={len(text)}字")

        # 调用 TTS
        audio_data = tts_segment(text, voice_id, api_key, tts_model)

        # 保存
        filepath.write_bytes(audio_data)

        result_segments.append({
            "index": i,
            "type": seg_type,
            "character": character,
            "text_preview": text[:50],
            "audio_file": str(filepath),
            "voice_id": voice_id,
        })

        # MiniMax API 有速率限制，稍微延迟
        time.sleep(0.3)

    return result_segments


def main():
    parser = argparse.ArgumentParser(description="TTS 语音生成器")
    parser.add_argument("--segments-file", required=True, help="chapter_analyzer.py 输出的 JSON 文件")
    parser.add_argument("--output-dir", default="temp_audio", help="音频输出目录")
    args = parser.parse_args()

    config = load_config()
    api_key = config.get("minimax_api_key", "")
    if not api_key:
        print("错误: config.json 中未配置 minimax_api_key", file=sys.stderr)
        sys.exit(1)

    # 读取分段数据
    with open(args.segments_file, "r", encoding="utf-8") as f:
        segments_data = json.load(f)

    # 生成语音
    result = generate_all_segments(segments_data, api_key, config, args.output_dir)

    # 输出结果
    output = {
        "segments": result,
        "stats": segments_data.get("stats", {}),
    }
    print(f"\n所有语音生成完成! 共 {len(result)} 段")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
