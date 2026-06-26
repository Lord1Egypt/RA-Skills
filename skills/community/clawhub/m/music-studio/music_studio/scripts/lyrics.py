"""lyrics 命令：作词"""

import uuid
from music_studio import config, providers, library


def _safe_name(name: str, fallback: str = "lyrics") -> str:
    safe = (name or fallback).replace("/", "_").replace("\\", "_").strip()
    return safe or fallback


def main(args):
    try:
        api_key = config.get_api_key()
    except RuntimeError as e:
        print(f"❌ {e}")
        return
    client = providers.get_api_client(api_key, config.get_provider())

    mode = "edit" if args.edit else "write_full_song"
    prompt = args.prompt or ""
    title = args.title
    lyrics_edit = args.edit

    if mode == "write_full_song" and not prompt:
        print("用法: python -m music_studio lyrics \"<主题>\" [--title \"标题\"] [--edit \"歌词\"]")
        print("运行 python -m music_studio help 查看完整帮助")
        return

    print("🎤 作词中...")

    try:
        resp = client.lyrics_generation(
            prompt=prompt,
            mode=mode,
            lyrics=lyrics_edit,
            title=title,
        )
        client.raise_on_error(resp)
    except Exception as e:
        print(f"❌ 作词失败: {e}")
        return

    song_title = resp.get("song_title", "未命名")
    style_tags = resp.get("style_tags", "")
    lyrics_text = resp.get("lyrics", "")

    if not lyrics_text:
        print("❌ 作词失败：未返回歌词")
        return

    out_id = str(uuid.uuid4())
    timestamp = library._now()
    library.ensure_output_dir()
    safe = _safe_name(song_title, "lyrics")

    lyrics_file = library.OUTPUT_DIR() / f"{safe}.lyrics.txt"
    lyrics_file.write_text(lyrics_text)

    tags_path = ""
    if style_tags:
        tags_file = library.OUTPUT_DIR() / f"{safe}.tags.txt"
        tags_file.write_text(style_tags + "\n")
        tags_path = str(tags_file)

    meta_file = library.OUTPUT_DIR() / f"{safe}.meta.txt"
    meta_file.write_text(
        f"id: {out_id}\n"
        f"title: {song_title}\n"
        f"type: lyrics\n"
        f"provider: {config.get_provider()}\n"
        f"prompt: {prompt}\n"
        f"created: {timestamp}\n"
        f"style_tags: {style_tags}\n"
    )

    entry = {
        "id": out_id,
        "title": song_title,
        "created": timestamp,
        "type": "lyrics",
        "provider": config.get_provider(),
        "style_tags": style_tags,
        "lyrics_path": str(lyrics_file),
        "tags_path": tags_path,
        "meta_path": str(meta_file),
        "expires": library._expires(),
    }
    library.add_entry(entry)

    print(f"=== {song_title} ===")
    if style_tags:
        print(f"风格: {style_tags}")
    print()
    print(lyrics_text)
    print()
    print(f"[歌词已保存: {lyrics_file}]")
    if tags_path:
        print(f"[标签已保存: {tags_path}]")
    print(f"[说明已保存: {meta_file}]")
