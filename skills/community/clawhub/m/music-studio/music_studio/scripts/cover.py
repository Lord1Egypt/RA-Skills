"""cover 命令：基于参考音频生成翻唱"""

import urllib.request
import uuid
from music_studio import config, providers, library


def _safe_name(name: str, fallback: str = "cover") -> str:
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
        print("用法: python -m music_studio cover \"<翻唱描述>\" --audio <URL> [选项]")
        print()
        print("参数说明：")
        print("  <翻唱描述>    - 目标翻唱风格描述（必填，10~300字符）")
        print("  --audio <url> - 参考音频URL（必填，6秒~6分钟，≤50MB）")
        print("  --lyrics <歌词> - 可选歌词（不传则自动从参考音频提取）")
        return

    if not args.audio:
        print("❌ 翻唱需要参考音频，请使用 --audio 提供 URL")
        return

    try:
        api_key = config.get_api_key()
    except RuntimeError as e:
        print(f"❌ {e}")
        return
    client = providers.get_api_client(api_key, config.get_provider())
    preprocess_model = config.get_cover_model()
    generate_model = config.get_music_model()

    print("🎙️ 翻唱前处理中...")
    try:
        prep = client.music_cover_preprocess(model=preprocess_model, audio_url=args.audio)
        client.raise_on_error(prep)
    except Exception as e:
        print(f"❌ 翻唱前处理失败: {e}")
        return

    cover_feature_id = prep.get("cover_feature_id", "")
    auto_lyrics = prep.get("formatted_lyrics", "")
    if not cover_feature_id:
        print("❌ 翻唱前处理失败：未返回 cover_feature_id")
        return

    print("🎙️ 翻唱生成中...")
    try:
        resp = client.music_generation(
            model=generate_model,
            prompt=args.prompt,
            lyrics=args.lyrics or auto_lyrics or None,
            cover_feature_id=cover_feature_id,
        )
        client.raise_on_error(resp)
    except Exception as e:
        print(f"❌ 翻唱生成失败: {e}")
        return

    audio_url = resp.get("data", {}).get("audio", "")
    if not audio_url:
        print("❌ 翻唱生成失败：未返回音频链接")
        return

    out_id = str(uuid.uuid4())
    timestamp = library._now()
    library.ensure_output_dir()
    title = args.prompt
    safe = _safe_name(title, "cover")

    url_file = library.OUTPUT_DIR() / f"{safe}.url"
    url_file.write_text(audio_url + "\n")
    meta_file = library.OUTPUT_DIR() / f"{safe}.meta.txt"
    meta_file.write_text(
        f"id: {out_id}\n"
        f"title: {title}\n"
        f"type: cover\n"
        f"provider: {config.get_provider()}\n"
        f"model: {generate_model}\n"
        f"preprocess_model: {preprocess_model}\n"
        f"prompt: {args.prompt}\n"
        f"created: {timestamp}\n"
        f"audio_url: {audio_url}\n"
        f"reference_url: {args.audio}\n"
        f"cover_feature_id: {cover_feature_id}\n"
    )

    lyrics_path = ""
    lyrics_text = args.lyrics or auto_lyrics or ""
    if lyrics_text:
        lyrics_file = library.OUTPUT_DIR() / f"{safe}.lyrics.txt"
        lyrics_file.write_text(lyrics_text)
        lyrics_path = str(lyrics_file)

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
        "type": "cover",
        "provider": config.get_provider(),
        "model": generate_model,
        "preprocess_model": preprocess_model,
        "music_url": audio_url,
        "reference_url": args.audio,
        "cover_feature_id": cover_feature_id,
        "formatted_lyrics": auto_lyrics,
        "lyrics_path": lyrics_path,
        "local_path": local_path,
        "url_path": str(url_file),
        "meta_path": str(meta_file),
        "expires": library._expires(),
    }
    library.add_entry(entry)

    print(f"🎵 翻唱已生成（{config.get_provider()}/{generate_model}）:")
    if local_path:
        print(f"[音频已保存: {local_path}]")
    else:
        print(f"[音频自动下载失败: {download_err}]")
    if lyrics_path:
        print(f"[歌词已保存: {lyrics_path}]")
    print(f"[链接已保存: {url_file}]")
    print(f"[说明已保存: {meta_file}]")
