#!/usr/bin/env python3
"""视频管线：下载 → 提音频 → 转录 → 清洗"""
import subprocess, sys, os, json
from pathlib import Path

WORKDIR = Path("/tmp/links-pipeline")
WORKDIR.mkdir(parents=True, exist_ok=True)

def download_video(url: str) -> Path:
    """yt-dlp 下载视频"""
    print(f"[pipeline] 下载视频: {url}")
    result = subprocess.run(
        ["yt-dlp", "--no-check-certificate", "-o", str(WORKDIR / "video.%(ext)s"), url],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        print(f"[pipeline] yt-dlp失败: {result.stderr[:200]}")
        print("[pipeline] 尝试从浏览器提取直链...")
        return None  # 调用方需用其他方式获取视频直链
    # 查找下载的文件
    for f in WORKDIR.glob("video.*"):
        if f.suffix != ".wav":
            return f
    return None

def extract_audio(video_path: Path) -> Path:
    """ffmpeg 提取音频为16kHz wav"""
    audio_path = WORKDIR / "audio.wav"
    print(f"[pipeline] 提取音频: {video_path.name} → audio.wav")
    subprocess.run([
        "ffmpeg", "-i", str(video_path), "-vn",
        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        "-y", str(audio_path)
    ], capture_output=True, check=True, timeout=300)
    return audio_path

def transcribe(audio_path: Path) -> str:
    """whisper base 模型转录"""
    print(f"[pipeline] 转录音频 (base model)...")
    result = subprocess.run(
        ["whisper", str(audio_path), "--model", "base",
         "--language", "zh", "--output_dir", str(WORKDIR),
         "--output_format", "txt"],
        capture_output=True, text=True, timeout=900
    )
    txt_path = WORKDIR / "audio.txt"
    if txt_path.exists():
        return txt_path.read_text(encoding="utf-8")
    return ""

def run(url: str):
    """完整视频管线"""
    print(f"[pipeline] === 视频管线启动 ===")
    video = download_video(url)
    if not video:
        print("[pipeline] 需要手动从浏览器获取视频直链")
        return {"status": "need_browser_url", "url": url}
    audio = extract_audio(video)
    text = transcribe(audio)
    print(f"[pipeline] 转录完成: {len(text)} 字符")
    # 保存原始转录
    (WORKDIR / "transcript.txt").write_text(text, encoding="utf-8")
    return {"status": "ok", "transcript": text, "chars": len(text)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 download.py <视频URL>")
        sys.exit(1)
    result = run(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
