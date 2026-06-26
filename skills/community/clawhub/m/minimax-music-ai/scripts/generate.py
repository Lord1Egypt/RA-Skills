"""
MiniMax 音乐生成脚本
用法:
    python generate.py --help
    python generate.py --prompt "描述" --name "文件名" --save "D:\\path"
    python generate.py --lyrics-prompt "歌词主题" --song-title "歌名" --prompt "风格" --name "文件名" --save "D:\\path"
    python generate.py --merge "f1.mp3" "f2.mp3" --output "merged.mp3"
"""

import argparse
import os
import sys
import json
import time
import requests

# ============ 配置 ============
API_KEY = "sk-cp-F-oQWZsbhwv06vJlTx0ZdpsYS4lj6_SexMokhjTvL5I08cwoPHb22r49qvecJjxt8Qn1LHsIRlVJn12WLJjF9GIdjOcqJqyf8jSd33YhcYb3E9XciwvlrXM"
API_BASE = "https://api.minimaxi.com/v1"
DEFAULT_TIMEOUT = 600  # 600秒，等待音乐生成


def generate_lyrics(prompt, title=None, timeout=60):
    """生成歌词"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {"mode": "write_full_song", "prompt": prompt}
    if title:
        payload["title"] = title

    print(f"  [歌词] 生成中: {prompt[:30]}...")
    r = requests.post(f"{API_BASE}/lyrics_generation",
                     headers=headers, json=payload, timeout=timeout)
    data = r.json()
    if data.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"歌词生成失败: {data.get('base_resp')}")
    print(f"  [歌词] 完成: {data.get('song_title')} | 风格: {data.get('style_tags')}")
    return data


def generate_music(prompt, lyrics=None, instrumental=True, timeout=DEFAULT_TIMEOUT):
    """生成歌曲"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": "music-2.6",
        "prompt": prompt,
        "is_instrumental": instrumental,
        "output_format": "url"
    }
    if lyrics:
        payload["lyrics"] = lyrics
        payload["is_instrumental"] = False

    print(f"  [歌曲] 生成中（约2-5分钟）...")
    r = requests.post(f"{API_BASE}/music_generation",
                     headers=headers, json=payload, timeout=timeout)
    data = r.json()
    if data.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"歌曲生成失败: {data.get('base_resp')}")
    audio_url = data["data"]["audio"]
    duration = data.get("extra_info", {}).get("music_duration", 0)
    print(f"  [歌曲] 完成! 时长: {duration//1000}秒")
    return audio_url


def download_audio(url, filepath, timeout=60):
    """下载音频文件"""
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(r.content)
    size = os.path.getsize(filepath)
    print(f"  [下载] 保存: {filepath} ({size//1024}KB)")


def merge_audio(files, output_path):
    """用ffmpeg合并多个音频文件"""
    list_file = output_path + ".concat_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for fp in files:
            # 绝对路径
            abs_path = os.path.abspath(fp)
            f.write(f"file '{abs_path}'\n")

    import subprocess
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        output_path
    ]
    print(f"  [合并] 执行 ffmpeg 合并 {len(files)} 个文件...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(list_file)
    if result.returncode != 0:
        raise Exception(f"ffmpeg 合并失败: {result.stderr}")
    size = os.path.getsize(output_path)
    print(f"  [合并] 完成: {output_path} ({size//1024}KB)")


def main():
    parser = argparse.ArgumentParser(description="MiniMax AI 音乐生成工具")
    parser.add_argument("--prompt", type=str, help="歌曲风格描述（纯音乐用）")
    parser.add_argument("--lyrics-prompt", type=str, help="歌词主题描述")
    parser.add_argument("--song-title", type=str, help="歌曲标题")
    parser.add_argument("--name", type=str, default="output", help="输出文件名（不含扩展名）")
    parser.add_argument("--save", type=str, default=".", help="保存目录")
    parser.add_argument("--merge", nargs="+", help="合并多个mp3文件")
    parser.add_argument("--output", type=str, help="合并后的输出文件路径")

    args = parser.parse_args()

    # 合并模式
    if args.merge:
        if not args.output:
            print("错误: --merge 需要配合 --output 指定输出文件")
            sys.exit(1)
        merge_audio(args.merge, args.output)
        return

    if not args.prompt and not args.lyrics_prompt:
        print("错误: 请指定 --prompt 或 --lyrics-prompt")
        sys.exit(1)

    os.makedirs(args.save, exist_ok=True)

    # Step 1: 歌词（如需要）
    lyrics_text = None
    if args.lyrics_prompt:
        lyrics_data = generate_lyrics(args.lyrics_prompt, args.song_title)
        lyrics_text = lyrics_data.get("lyrics", "")
        # 保存歌词到文件
        lyrics_file = os.path.join(args.save, f"{args.name}_歌词.txt")
        with open(lyrics_file, "w", encoding="utf-8") as f:
            f.write(f"歌名: {lyrics_data.get('song_title', '')}\n")
            f.write(f"风格: {lyrics_data.get('style_tags', '')}\n\n")
            f.write(lyrics_text)
        print(f"  [歌词] 已保存: {lyrics_file}")

    # Step 2: 生成歌曲
    prompt = args.prompt or (
        "古风音乐" if "古" in args.lyrics_prompt else
        "摇滚音乐" if "摇滚" in args.lyrics_prompt else
        "流行音乐"
    )
    audio_url = generate_music(prompt, lyrics_text)

    # Step 3: 下载
    ext = "mp3"
    filepath = os.path.join(args.save, f"{args.name}.{ext}")
    download_audio(audio_url, filepath)

    print(f"\n完成! 文件: {filepath}")


if __name__ == "__main__":
    main()
