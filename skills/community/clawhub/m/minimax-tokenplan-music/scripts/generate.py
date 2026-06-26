#!/usr/bin/env python3
"""
MiniMax Music Generation (music-2.6 / music-cover) wrapper.

Usage:
  python3 generate.py --prompt "风格描述" [--lyrics "歌词"] [--instrumental] \
      [--cover] [--audio /path/to/ref.mp3] \
      [--sample-rate 44100] [--bitrate 256000] [--format wav] \
      [--output /path/to/output.wav]

Rules:
  - model: 默认 music-2.6（文生音乐），翻唱模式用 music-cover
  - USE_FREE_MODEL=True 时自动使用 *-free 免费模型
  - 非纯音乐 + 无歌词 → 自动调用 lyrics_generation 生成歌词
  - 参考音频支持 URL 和本地文件（本地文件自动 base64 编码）
  - API 返回 audio 字段是 HEX 编码（不是 base64），脚本自动解码
  - 默认输出: WAV 格式, 44100Hz, 256kbps, HEX, 非流式
  - 输出目录: ~/.openclaw/media/minimax/music/
"""

import argparse
import base64
import json
import os
import re
import sys
import wave
from datetime import date

try:
    import requests
except ImportError:
    print("[ERROR] 缺少 requests 库，请运行: pip3 install requests", file=sys.stderr)
    sys.exit(1)

# ------------------ 配置区（可被命令行参数覆盖）------------------
# TODO: 初始化时填入实际值
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.minimaxi.com"  # CN: api.minimaxi.com, Global: api.minimaxi.io
USE_FREE_MODEL = True  # init 时：用户提供 API Key → False，未提供 → True
# ----------------------------------------------------------------

OUTPUT_DIR = os.path.expanduser("~/.openclaw/media/minimax/music/")

VALID_SAMPLE_RATES = [16000, 24000, 32000, 44100]
VALID_BITRATES = [32000, 64000, 128000, 256000]
VALID_FORMATS = ["mp3", "wav", "pcm"]

# 歌词结构标签（供参考）
LYRICS_TAGS = [
    "[Intro]", "[Verse]", "[Pre Chorus]", "[Chorus]", "[Interlude]",
    "[Bridge]", "[Outro]", "[Post Chorus]", "[Transition]", "[Break]",
    "[Hook]", "[Build Up]", "[Inst]", "[Solo]",
]

# 错误码映射
ERROR_MESSAGES = {
    1002: "限流中，请稍后重试",
    1004: "鉴权失败，请检查 API Key",
    1008: "余额不足，请充值",
    1026: "内容涉及敏感词，请修改描述后重试",
    2013: "参数异常，请检查入参",
    2049: "无效的 API Key，请检查 Key 是否正确",
}


def make_slug(text: str) -> str:
    """将 text 转换为 safe 文件名：取前20字符，保留中文、英文、数字。"""
    slug = text[:20]
    slug = slug.replace(" ", "-")
    slug = ''.join(c for c in slug if c.isalnum() or c in '-_')
    slug = slug[:40] or "music"
    return slug


def handle_api_error(data, resp_status_code=200):
    """统一处理 API 错误响应。"""
    base_resp = data.get("base_resp", {})
    code = base_resp.get("status_code", 0)
    if code != 0:
        msg = base_resp.get("status_msg", "未知错误")
        hint = ERROR_MESSAGES.get(code, "")
        print(f"[ERROR] API 返回: code={code}, msg={msg}", file=sys.stderr)
        if hint:
            print(f"[HINT] {hint}", file=sys.stderr)
        sys.exit(1)


def generate_lyrics(prompt, api_key, base_url, timeout=60):
    """调用 /v1/lyrics_generation 生成歌词。

    返回 (song_title, style_tags, lyrics) 三元组。
    """
    print(f"[INFO] 未提供歌词，自动调用歌词生成 API ...", file=sys.stderr)

    payload = {
        "mode": "write_full_song",
        "prompt": prompt,
    }

    try:
        resp = requests.post(
            f"{base_url}/v1/lyrics_generation",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=timeout,
        )
    except Exception as e:
        print(f"[ERROR] 歌词生成请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        data = resp.json()
    except Exception as e:
        print(f"[ERROR] 歌词生成响应解析失败: {e}", file=sys.stderr)
        sys.exit(1)

    handle_api_error(data, resp.status_code)

    song_title = data.get("song_title", "")
    style_tags = data.get("style_tags", "")
    lyrics = data.get("lyrics", "")

    if not lyrics:
        print("[ERROR] 歌词生成返回为空", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] 歌词生成完成: 标题={song_title}", file=sys.stderr)
    print(f"[INFO] 风格标签: {style_tags}", file=sys.stderr)
    print(f"[INFO] 歌词长度: {len(lyrics)} 字符", file=sys.stderr)

    return song_title, style_tags, lyrics


def generate(
    prompt,
    lyrics=None,
    is_instrumental=False,
    is_cover=False,
    audio=None,
    stream=False,
    output_format="hex",
    sample_rate=44100,
    bitrate=256000,
    audio_format="wav",
    aigc_watermark=False,
    lyrics_optimizer=False,
    output=None,
    api_key=API_KEY,
    base_url=BASE_URL,
    timeout=240,
):
    """调用 MiniMax Music Generation API，生成音乐文件。"""

    # 检查 API Key 是否已配置
    if api_key == "YOUR_API_KEY_HERE" or not api_key:
        print("[ERROR] API Key 未配置，请先运行 init 流程", file=sys.stderr)
        sys.exit(1)

    # ---------- 确定模型 ----------
    if is_cover:
        model = "music-cover-free" if USE_FREE_MODEL else "music-cover"
    else:
        model = "music-2.6-free" if USE_FREE_MODEL else "music-2.6"
    print(f"[INFO] 使用模型: {model}", file=sys.stderr)

    # ---------- 自动歌词生成 ----------
    # 非纯音乐 + 无歌词 + 未开启 lyrics_optimizer → 调用歌词生成 API
    if not is_instrumental and not lyrics and not lyrics_optimizer:
        if not prompt:
            print("[ERROR] 非纯音乐模式下必须提供 --prompt 或 --lyrics", file=sys.stderr)
            sys.exit(1)
        song_title, style_tags, lyrics = generate_lyrics(
            prompt, api_key, base_url, timeout=timeout,
        )
        print(f"[INFO] 自动生成的歌词将用于音乐生成", file=sys.stderr)

    # ---------- 参数校验 ----------
    if sample_rate not in VALID_SAMPLE_RATES:
        closest = min(VALID_SAMPLE_RATES, key=lambda x: abs(x - sample_rate))
        print(f"[WARN] 采样率 {sample_rate} 不在有效值中，自动调整为 {closest}", file=sys.stderr)
        sample_rate = closest

    if bitrate not in VALID_BITRATES:
        closest = min(VALID_BITRATES, key=lambda x: abs(x - bitrate))
        print(f"[WARN] 比特率 {bitrate} 不在有效值中，自动调整为 {closest}", file=sys.stderr)
        bitrate = closest

    if audio_format not in VALID_FORMATS:
        print(f"[WARN] 格式 {audio_format} 无效，自动使用 wav", file=sys.stderr)
        audio_format = "wav"

    # 流式模式下 output_format 必须是 hex
    if stream and output_format != "hex":
        print(f"[WARN] 流式模式下 output_format 必须为 hex，已自动调整", file=sys.stderr)
        output_format = "hex"

    # AIGC 水印仅在非流式模式下生效
    if aigc_watermark and stream:
        print(f"[WARN] AIGC 水印仅在非流式模式下生效，已忽略", file=sys.stderr)
        aigc_watermark = False

    # ---------- 构建 payload ----------
    payload = {
        "model": model,
        "stream": stream,
        "output_format": output_format,
        "audio_setting": {
            "sample_rate": sample_rate,
            "bitrate": bitrate,
            "format": audio_format,
        },
        "aigc_watermark": aigc_watermark,
    }

    if prompt:
        payload["prompt"] = prompt

    if lyrics:
        payload["lyrics"] = lyrics

    if lyrics_optimizer:
        payload["lyrics_optimizer"] = True

    # is_instrumental 和 lyrics_optimizer 仅对 music-2.6 系列有效
    if not is_cover:
        payload["is_instrumental"] = is_instrumental

    # ---------- 翻唱模式：参考音频处理 ----------
    if is_cover:
        if not audio:
            print("[ERROR] 翻唱模式必须提供 --audio 参考音频", file=sys.stderr)
            sys.exit(1)

        if audio.startswith("http://") or audio.startswith("https://"):
            # 公网 URL
            payload["audio_url"] = audio
            print(f"[INFO] 使用 URL 参考音频: {audio[:80]}...", file=sys.stderr)
        elif os.path.isfile(audio):
            # 本地文件 → base64
            file_size = os.path.getsize(audio)
            if file_size > 50 * 1024 * 1024:
                print(f"[ERROR] 参考音频文件过大 ({file_size / 1024 / 1024:.1f}MB)，最大 50MB", file=sys.stderr)
                sys.exit(1)
            with open(audio, "rb") as f:
                audio_data = f.read()
            audio_b64 = base64.b64encode(audio_data).decode("utf-8")
            payload["audio_base64"] = audio_b64
            print(f"[INFO] 已将本地音频转为 base64 ({file_size / 1024:.1f}KB)", file=sys.stderr)
        else:
            print(f"[ERROR] 参考音频路径不存在: {audio}", file=sys.stderr)
            sys.exit(1)

    # ---------- 打印请求信息 ----------
    mode_str = "翻唱" if is_cover else ("纯音乐" if is_instrumental else "文生音乐")
    print(f"[INFO] 模式: {mode_str}", file=sys.stderr)
    print(f"[INFO] 采样率: {sample_rate}Hz, 比特率: {bitrate}, 格式: {audio_format}", file=sys.stderr)
    print(f"[INFO] 流式: {stream}, 输出格式: {output_format}", file=sys.stderr)
    if lyrics:
        print(f"[INFO] 歌词长度: {len(lyrics)} 字符", file=sys.stderr)

    # ---------- 发送请求 ----------
    try:
        resp = requests.post(
            f"{base_url}/v1/music_generation",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=timeout,
        )
    except Exception as e:
        print(f"[ERROR] 请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    # ---------- 解析响应 ----------
    try:
        data = resp.json()
    except Exception as e:
        print(f"[ERROR] 响应解析失败: {e}", file=sys.stderr)
        print(f"[ERROR] 响应内容: {resp.text[:500]}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        handle_api_error(data, resp.status_code)
        # 如果 handle_api_error 没有退出（status_code=0 但 HTTP 非 200）
        print(f"[ERROR] HTTP {resp.status_code}: {resp.text[:500]}", file=sys.stderr)
        sys.exit(1)

    handle_api_error(data, resp.status_code)

    # 检查合成状态
    status = data.get("data", {}).get("status")
    if status == 1:
        print("[WARN] 音乐合成仍在进行中（status=1），响应可能不完整", file=sys.stderr)

    # 提取 extra_info
    extra_info = data.get("extra_info", {})
    if extra_info:
        duration = extra_info.get("music_duration", 0)
        print(f"[INFO] 音乐时长: {duration}ms ({duration / 1000:.1f}s)", file=sys.stderr)
        print(f"[INFO] 采样率: {extra_info.get('music_sample_rate', 'N/A')}Hz, "
              f"声道: {extra_info.get('music_channel', 'N/A')}, "
              f"比特率: {extra_info.get('bitrate', 'N/A')}, "
              f"大小: {extra_info.get('music_size', 'N/A')} bytes", file=sys.stderr)

    # ---------- 处理输出 ----------
    audio_data_raw = data.get("data", {}).get("audio")
    if not audio_data_raw:
        print("[ERROR] 响应中缺少 audio 字段", file=sys.stderr)
        sys.exit(1)

    # URL 模式：直接返回 URL
    if output_format == "url":
        print(audio_data_raw)
        return audio_data_raw

    # HEX 模式：解码为 bytes
    try:
        audio_bytes = bytes.fromhex(audio_data_raw)
    except Exception as e:
        print(f"[ERROR] HEX 解码失败: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] 音频大小: {len(audio_bytes)} bytes ({len(audio_data_raw)} hex chars)", file=sys.stderr)

    # 生成输出路径
    if output is None:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        slug = make_slug(prompt or "music")
        today = date.today().isoformat()
        output = os.path.join(OUTPUT_DIR, f"music-{today}-{slug}.{audio_format}")

    # 确保输出目录存在
    output_dir = os.path.dirname(output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # 写入文件
    try:
        if audio_format == "wav" and audio_bytes[:4] != b'RIFF':
            # Raw PCM 数据，包装成 WAV
            channels = extra_info.get("music_channel", 2)
            with wave.open(output, 'wb') as wav_file:
                wav_file.setnchannels(channels)
                wav_file.setsampwidth(2)  # 16-bit = 2 bytes
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_bytes)
        else:
            # 已是完整文件（WAV 有 RIFF 头，或 mp3/pcm），直接写入
            with open(output, 'wb') as f:
                f.write(audio_bytes)
        print(f"[SUCCESS] 音频已保存: {output}", file=sys.stderr)
    except Exception as e:
        print(f"[ERROR] 保存文件失败: {e}", file=sys.stderr)
        sys.exit(1)

    # stdout 只输出路径
    print(output)
    return output


def main():
    parser = argparse.ArgumentParser(
        description="MiniMax Music Generation - 文生音乐 / 纯音乐 / 翻唱",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  # 文生音乐（自动生成歌词）
  python3 generate.py --prompt "一首关于夏天的民谣"

  # 带歌词的音乐
  python3 generate.py --prompt "流行,欢快" --lyrics "[verse]\\n阳光洒在脸上\\n微风轻轻吹"

  # 纯音乐
  python3 generate.py --prompt "轻快的钢琴曲,治愈" --instrumental

  # 翻唱（URL 参考音频）
  python3 generate.py --prompt "翻唱风格" --cover --audio "https://example.com/song.mp3"

  # 翻唱（本地参考音频）
  python3 generate.py --prompt "翻唱风格" --cover --audio "/path/to/ref.mp3"

歌词结构标签:
  [Intro] [Verse] [Pre Chorus] [Chorus] [Interlude] [Bridge]
  [Outro] [Post Chorus] [Transition] [Break] [Hook] [Build Up]
  [Inst] [Solo]
""",
    )
    parser.add_argument(
        "--prompt", "-p",
        default=None,
        help="音乐风格描述（文生音乐: 1-2000字符；翻唱: 10-300字符）"
    )
    parser.add_argument(
        "--lyrics", "-l",
        default=None,
        help="歌词内容，用 \\n 分隔行，支持结构标签如 [Verse] [Chorus]"
    )
    parser.add_argument(
        "--lyrics-file",
        default=None,
        help="从文件读取歌词（与 --lyrics 互斥）"
    )
    parser.add_argument(
        "--instrumental",
        action="store_true",
        default=False,
        help="生成纯音乐（无人声），仅 music-2.6 系列支持"
    )
    parser.add_argument(
        "--cover",
        action="store_true",
        default=False,
        help="翻唱模式（需提供 --audio 参考音频），模型自动切换为 music-cover"
    )
    parser.add_argument(
        "--audio", "-a",
        default=None,
        help="参考音频: 公网 URL 或本地文件路径（翻唱模式必填，6秒-6分钟，最大50MB）"
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        default=False,
        help="流式输出（启用后 output_format 强制为 hex）"
    )
    parser.add_argument(
        "--output-format",
        default="hex",
        choices=["hex", "url"],
        help="输出格式: hex（默认，HEX 编码音频数据）或 url（返回下载链接，24小时有效）"
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=44100,
        help="采样率（默认: 44100），可选: 16000/24000/32000/44100"
    )
    parser.add_argument(
        "--bitrate",
        type=int,
        default=256000,
        help="比特率（默认: 256000），可选: 32000/64000/128000/256000"
    )
    parser.add_argument(
        "--format", "-f",
        dest="audio_format",
        default="wav",
        choices=VALID_FORMATS,
        help="音频格式（默认: wav），可选: mp3/wav/pcm"
    )
    parser.add_argument(
        "--aigc-watermark",
        action="store_true",
        default=False,
        help="添加 AIGC 水印（仅非流式模式生效）"
    )
    parser.add_argument(
        "--lyrics-optimizer",
        action="store_true",
        default=False,
        help="根据 prompt 自动生成歌词（仅 music-2.6 系列支持）"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help=f"输出路径（默认自动生成到 {OUTPUT_DIR}）"
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
    parser.add_argument(
        "--timeout",
        type=int,
        default=240,
        help="API 请求超时时间（秒，默认: 240）"
    )

    args = parser.parse_args()

    # 覆盖全局配置
    final_api_key = args.api_key if args.api_key else API_KEY
    final_base_url = args.base_url if args.base_url else BASE_URL

    # --lyrics 和 --lyrics-file 互斥
    lyrics = args.lyrics
    if args.lyrics_file:
        if lyrics:
            print("[ERROR] --lyrics 和 --lyrics-file 不能同时使用", file=sys.stderr)
            sys.exit(1)
        if not os.path.isfile(args.lyrics_file):
            print(f"[ERROR] 歌词文件不存在: {args.lyrics_file}", file=sys.stderr)
            sys.exit(1)
        with open(args.lyrics_file, "r", encoding="utf-8") as f:
            lyrics = f.read()
        print(f"[INFO] 从文件读取歌词: {args.lyrics_file} ({len(lyrics)} 字符)", file=sys.stderr)

    # 基本校验
    if not args.prompt and not lyrics and not args.lyrics_optimizer:
        print("[ERROR] 至少提供 --prompt、--lyrics 或 --lyrics-optimizer 之一", file=sys.stderr)
        sys.exit(1)

    if args.cover and args.instrumental:
        print("[ERROR] --cover 和 --instrumental 不能同时使用", file=sys.stderr)
        sys.exit(1)

    generate(
        prompt=args.prompt,
        lyrics=lyrics,
        is_instrumental=args.instrumental,
        is_cover=args.cover,
        audio=args.audio,
        stream=args.stream,
        output_format=args.output_format,
        sample_rate=args.sample_rate,
        bitrate=args.bitrate,
        audio_format=args.audio_format,
        aigc_watermark=args.aigc_watermark,
        lyrics_optimizer=args.lyrics_optimizer,
        output=args.output,
        api_key=final_api_key,
        base_url=final_base_url,
        timeout=args.timeout,
    )


if __name__ == "__main__":
    main()
