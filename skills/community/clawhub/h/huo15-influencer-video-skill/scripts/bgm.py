"""背景音乐 + 混音

约定：用户把 BGM 文件放到 ~/Music/huo15-bgm/，文件名作为 key。
推荐准备这 5 个 key（缺哪个就降级到无 BGM）：
  warm.mp3       温暖治愈钢琴
  energetic.mp3  活力电子节拍
  asian.mp3      中国风古筝竹笛
  soft.mp3       柔和氛围
  cinematic.mp3  电影感弦乐

下载渠道（CC0 / 免版税）：
  https://pixabay.com/music/
  https://freesound.org/
  https://incompetech.com/music/royalty-free/

mix_audio() 把人声和 BGM 混到一起，BGM 自动循环到与人声等长，
然后整体淡出 0.5 秒。
"""

import os
import subprocess
from pathlib import Path
from typing import Optional


BGM_DIR = Path(os.environ.get("HUO15_BGM_DIR", str(Path.home() / "Music" / "huo15-bgm")))
SUPPORTED_EXT = (".mp3", ".m4a", ".wav", ".ogg", ".flac")


def find_bgm(key: Optional[str]) -> Optional[str]:
    """按 key 找 BGM 文件。找不到返回 None（无 BGM 模式）"""
    if not key:
        return None
    if os.path.isabs(key) and os.path.exists(key):
        return key
    if not BGM_DIR.exists():
        return None
    for ext in SUPPORTED_EXT:
        p = BGM_DIR / f"{key}{ext}"
        if p.exists():
            return str(p)
    # 模糊匹配第一个含关键字的文件
    for f in BGM_DIR.iterdir():
        if key in f.name and f.suffix.lower() in SUPPORTED_EXT:
            return str(f)
    return None


def list_available_bgm() -> list:
    """列出 BGM 目录下已就位的文件"""
    if not BGM_DIR.exists():
        return []
    return sorted(
        f.stem for f in BGM_DIR.iterdir()
        if f.suffix.lower() in SUPPORTED_EXT
    )


def mix_audio(voice_path: str,
              bgm_key: Optional[str] = None,
              bgm_volume: float = 0.20,
              voice_volume: float = 1.0,
              fade_out: float = 0.5,
              output: Optional[str] = None) -> str:
    """把人声 + BGM 混成一个 mp3。

    - BGM 自动 loop 到人声时长
    - 人声始终保持原音量
    - BGM 默认压到 20% 音量
    - 末尾 fade_out 秒淡出
    """
    output = output or voice_path.replace(".mp3", "_mixed.mp3")
    bgm_path = find_bgm(bgm_key)

    # 取人声时长
    dur = float(subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        voice_path,
    ], text=True).strip())

    if not bgm_path:
        # 没有 BGM，只对人声做淡出
        cmd = [
            "ffmpeg", "-y", "-i", voice_path,
            "-af", f"volume={voice_volume},afade=t=out:st={max(0, dur-fade_out):.2f}:d={fade_out}",
            "-c:a", "libmp3lame", "-b:a", "192k",
            output,
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-i", voice_path,
            "-stream_loop", "-1", "-i", bgm_path,
            "-filter_complex",
            (
                f"[0:a]volume={voice_volume}[v];"
                f"[1:a]volume={bgm_volume},aloop=loop=-1:size=2e9[b];"
                f"[v][b]amix=inputs=2:duration=first:dropout_transition=0,"
                f"afade=t=out:st={max(0, dur-fade_out):.2f}:d={fade_out}"
            ),
            "-t", f"{dur:.2f}",
            "-c:a", "libmp3lame", "-b:a", "192k",
            output,
        ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output


def mux_video_audio(video_path: str, audio_path: str, output: str) -> str:
    """把音频盖到视频上（替换原音轨）。视频时长以视频为准，音频被截断或填静音"""
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-map", "0:v:0", "-map", "1:a:0",
        "-shortest",
        output,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output


if __name__ == "__main__":
    import json
    print(json.dumps({
        "bgm_dir": str(BGM_DIR),
        "available": list_available_bgm(),
    }, ensure_ascii=False, indent=2))
