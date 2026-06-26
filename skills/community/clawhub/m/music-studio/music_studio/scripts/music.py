"""music 命令：文本生成音乐"""

import urllib.request
import uuid
from music_studio import config, providers, library


def _safe_name(name: str, fallback: str = "music") -> str:
    safe = (name or fallback).replace("/", "_").replace("\\", "_").strip()
    return safe or fallback


def _download_audio(url: str, out_file):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    out_file.write_bytes(data)
    return len(data)


def main(args):
    if not args.prompt:
        print("用法: python -m music_studio music \"<描述>\" [歌词] [选项]")
        print()
        print("参数说明：")
        print("  <描述>           - 音乐风格/情绪/场景描述（必填）")
        print("  歌词              - 可选，歌词内容（\\n分隔）")
        print("  --instrumental   - 生成纯音乐（无人声）")
        print("  --optimizer      - 自动根据描述生成歌词")
        print("  --format <fmt>   - 输出格式：url（默认，临时有效）或 hex")
        print("  --sr <rate>      - 采样率：16000/24000/32000/44100（默认44100）")
        print("  --bitrate <rate> - 比特率：32000/64000/128000/256000（默认256000）")
        return

    try:
        api_key = config.get_api_key()
    except RuntimeError as e:
        print(f"❌ {e}")
        return
    client = providers.get_api_client(api_key, config.get_provider())
    model = config.get_music_model()

    print("🎵 音乐生成中...")

    try:
        resp = client.music_generation(
            model=model,
            prompt=args.prompt,
            lyrics=args.lyrics or None,
            is_instrumental=args.instrumental,
            lyrics_optimizer=args.optimizer,
            output_format=args.format,
            sample_rate=args.sr,
            bitrate=args.bitrate,
        )
        client.raise_on_error(resp)
    except Exception as e:
        print(f"❌ 音乐生成失败: {e}")
        return

    out_id = str(uuid.uuid4())
    timestamp = library._now()
    library.ensure_output_dir()
    title = args.prompt
    safe = _safe_name(title, "music")

    if args.format == "hex":
        audio_data = resp.get("data", {}).get("audio", "")
        hex_file = library.OUTPUT_DIR() / f"{safe}.hex"
        hex_file.write_text(audio_data)
        meta_file = library.OUTPUT_DIR() / f"{safe}.meta.txt"
        meta_file.write_text(
            f"id: {out_id}\n"
            f"title: {title}\n"
            f"type: music\n"
            f"provider: {config.get_provider()}\n"
            f"model: {model}\n"
            f"format: hex\n"
            f"created: {timestamp}\n"
        )

        entry = {
            "id": out_id,
            "title": title,
            "created": timestamp,
            "type": "music",
            "provider": config.get_provider(),
            "model": model,
            "format": "hex",
            "hex_path": str(hex_file),
            "meta_path": str(meta_file),
            "expires": library._expires(),
        }
        library.add_entry(entry)

        print(f"🎵 音乐已生成（{config.get_provider()}/{model}）:")
        print(f"[HEX 已保存: {hex_file}]")
        print(f"[说明已保存: {meta_file}]")
        return

    audio_url = resp.get("data", {}).get("audio", "")
    if not audio_url:
        print("❌ 音乐生成失败：未返回音频链接")
        return

    url_file = library.OUTPUT_DIR() / f"{safe}.url"
    url_file.write_text(audio_url + "\n")
    meta_file = library.OUTPUT_DIR() / f"{safe}.meta.txt"
    meta_file.write_text(
        f"id: {out_id}\n"
        f"title: {title}\n"
        f"type: music\n"
        f"provider: {config.get_provider()}\n"
        f"model: {model}\n"
        f"prompt: {args.prompt}\n"
        f"created: {timestamp}\n"
        f"audio_url: {audio_url}\n"
    )

    local_path = ""
    download_err = ""
    try:
        out_mp3 = library.OUTPUT_DIR() / f"{safe}.mp3"
        _download_audio(audio_url, out_mp3)
        local_path = str(out_mp3)
    except Exception as e:
        download_err = str(e)

    entry = {
        "id": out_id,
        "title": title,
        "created": timestamp,
        "type": "music",
        "provider": config.get_provider(),
        "model": model,
        "music_url": audio_url,
        "local_path": local_path,
        "url_path": str(url_file),
        "meta_path": str(meta_file),
        "expires": library._expires(),
    }
    library.add_entry(entry)

    print(f"🎵 音乐已生成（{config.get_provider()}/{model}）:")
    if local_path:
        print(f"[音频已保存: {local_path}]")
    else:
        print(f"[音频自动下载失败: {download_err}]")
    print(f"[链接已保存: {url_file}]")
    print(f"[说明已保存: {meta_file}]")
