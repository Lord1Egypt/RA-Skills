"""
背景音乐生成器 - 调用 MiniMax Music API 生成章节背景音乐

功能:
  1. 根据章节情绪（mood），自动生成合适的纯音乐
  2. 保存为 MP3 文件，供 audio_assembler.py 混音使用

用法:
  python scripts/music_generator.py --mood "悬疑" --output "bgm_output.mp3"
  python scripts/music_generator.py --mood "温馨" --duration 60

情绪-音乐 Prompt 映射:
  - 平静/日常 → 轻音乐、钢琴
  - 紧张/悬疑 → 低音、弦乐
  - 悲伤 → 钢琴独奏、缓慢
  - 欢快 → 轻快节奏
  - 热血/战斗 → 管弦乐、激昂
"""

import argparse
import json
import sys
import time
from pathlib import Path

import requests as req

SCRIPT_DIR = Path(__file__).parent.absolute()
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_PATH = SKILL_DIR / "config.json"

MUSIC_URL = "https://api.minimaxi.com/v1/music_generation"

# 情绪 → 音乐 Prompt 映射
MOOD_PROMPT_MAP = {
    "平静": "pure music, calm piano, gentle, background music, no lyrics, soft",
    "日常": "pure music, warm, daily life, acoustic guitar, background music, no lyrics",
    "温馨": "pure music, warm, cozy, piano and strings, no lyrics, heartwarming",
    "悲伤": "pure music, sad, piano solo, slow, melancholic, no lyrics",
    "紧张": "pure music, tense, suspense, dark ambient, thriller background, no lyrics",
    "悬疑": "pure music, suspense, mysterious, dark ambient, no lyrics",
    "悬疑紧张": "pure music, suspense, mysterious, dark ambient, no lyrics",
    "欢快": "pure music, cheerful, happy, upbeat piano, no lyrics",
    "热血": "pure music, epic, orchestral, heroic, powerful, no lyrics",
    "战斗": "pure music, epic, orchestral, intense battle, dramatic, no lyrics",
    "浪漫": "pure music, romantic, love, gentle piano, no lyrics",
    "轻松": "pure music, relaxing, chill, lofi, background, no lyrics",
    "恐怖": "pure music, horror, dark, eerie, creepy ambient, no lyrics",
    "悲伤压抑": "pure music, dark, sad, slow piano, melancholy, no lyrics",
    "愤怒": "pure music, intense, aggressive, dramatic orchestral, no lyrics",
    "希望": "pure music, hopeful, inspiring, uplifting strings and piano, no lyrics",
}

DEFAULT_PROMPT = "pure music, ambient, background music, no lyrics"


def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"配置文件不存在: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_music(prompt, api_key, model="music-2.6-free"):
    """
    调用 MiniMax Music API 生成背景音乐。

    参数:
        prompt: 音乐描述 prompt
        api_key: MiniMax API Key
        model: 音乐模型

    返回:
        音频 URL（临时链接，有效期 24 小时）
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "is_instrumental": True,    # 纯音乐模式
        "audio_setting": {
            "sample_rate": 44100,
            "bitrate": 256000,
            "format": "mp3",
        },
        "output_format": "url",
    }

    resp = req.post(MUSIC_URL, headers=headers, json=payload, timeout=180)
    result = resp.json()

    # 检查返回状态
    base_resp = result.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        raise RuntimeError(
            f"Music API 调用失败: {base_resp.get('status_msg')} "
            f"(code={base_resp.get('status_code')})"
        )

    # 获取音频 URL
    audio_data = result.get("data", {})
    audio_url = audio_data.get("audio", "")

    if not audio_url:
        # 可能包含 song 字段
        songs = audio_data.get("song", [])
        if songs:
            audio_url = songs[0].get("audio", "")
        elif "song" in audio_data:
            audio_url = audio_data["song"].get("audio", "")

    if not audio_url:
        raise RuntimeError(f"未能获取音乐 URL: {json.dumps(result, ensure_ascii=False)}")

    return audio_url


def download_music(url, save_path):
    """下载音乐到本地"""
    resp = req.get(url, timeout=120)
    resp.raise_for_status()
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_bytes(resp.content)
    return save_path


def resolve_prompt(mood, custom_prompt=None):
    """根据情绪获取音乐 prompt"""
    if custom_prompt:
        return custom_prompt
    # 尝试精确匹配和部分匹配
    for key, prompt in MOOD_PROMPT_MAP.items():
        if key in mood:
            return prompt
    return DEFAULT_PROMPT


def main():
    parser = argparse.ArgumentParser(description="背景音乐生成器")
    parser.add_argument("--mood", default="平静", help="章节情绪关键词")
    parser.add_argument("--prompt", help="自定义音乐 prompt（覆盖情绪映射）")
    parser.add_argument("--output", default="background_music.mp3", help="输出文件路径")
    args = parser.parse_args()

    config = load_config()
    api_key = config.get("minimax_api_key", "")
    if not api_key:
        print("错误: config.json 中未配置 minimax_api_key", file=sys.stderr)
        sys.exit(1)

    # 确定 prompt
    prompt = resolve_prompt(args.mood, args.prompt)
    print(f"情绪: {args.mood}")
    print(f"音乐 Prompt: {prompt}")

    # 生成音乐
    model = config.get("music_model", "music-2.6-free")
    print(f"调用 MiniMax Music ({model})...")
    audio_url = generate_music(prompt, api_key, model)
    print(f"音乐 URL 获取成功")

    # 下载
    save_path = download_music(audio_url, args.output)
    print(f"背景音乐已保存: {save_path}")

    # 输出路径供其他脚本使用
    print(json.dumps({"bg_music": str(save_path), "mood": args.mood}, ensure_ascii=False))


if __name__ == "__main__":
    main()
