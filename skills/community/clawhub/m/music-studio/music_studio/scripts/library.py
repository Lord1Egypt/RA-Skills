"""library 命令：音乐库管理"""

import urllib.request

from music_studio import library as lib_mod


def _out():
    return lib_mod.OUTPUT_DIR()


def _safe_name(name: str, fallback: str = "output") -> str:
    safe = (name or fallback).replace("/", "_").replace("\\", "_").strip()
    return safe or fallback


def _read_text_if_exists(*paths) -> str:
    for p in paths:
        if not p:
            continue
        p = _out() / p if isinstance(p, str) and not str(p).startswith("/") else p
        try:
            if p.exists():
                return p.read_text().strip()
        except Exception:
            pass
    return ""


def _download_to_path(url: str, out_file):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    out_file.write_bytes(data)
    return len(data)


def main(args):
    action = args.action
    arg = args.arg

    if action == "list":
        _list(arg)
    elif action == "get":
        _get(arg)
    elif action == "lyrics":
        _lyrics(arg)
    elif action == "url":
        _url(arg)
    elif action == "tags":
        _tags(arg)
    elif action == "download":
        _download(arg)
    elif action == "export":
        _export(arg, args.sub)
    elif action == "clean":
        _clean()
    elif action == "purge":
        _purge()
    else:
        _list(None)


def _list(filter_type=None):
    lib_mod.remove_expired()
    try:
        entries = list(lib_mod.list_entries(filter_type))
    except Exception:
        print("📭 暂无任何记录")
        return

    count = len(entries)
    print(f"=== 音乐库记录（共 {count} 条）===\n")
    for idx, song in entries:
        print(f"[{idx}] {song.get('title', '未知')}")
        t = song.get("type", "-")
        m = song.get("model", "-") or "-"
        has_local = " 📥" if song.get("local_path") else ""
        print(f"    类型: {t} | 模型: {m} | 创建: {song.get('created', '-')}{has_local}")
        print()


def _resolve(selector):
    if not selector:
        return None, None
    resolved = lib_mod.resolve_selector(selector)
    if not resolved:
        lib = lib_mod.read_library()
        songs = list(reversed(lib["songs"]))
        if selector.isdigit():
            print(f"❌ 没有第 {selector} 条记录（共 {len(songs)} 条）")
        else:
            print(f"❌ 未找到: {selector}")
        return None, None
    entry = lib_mod.get_entry(resolved)
    if not entry:
        print(f"❌ 未找到: {selector}")
        return None, None
    return resolved, entry


def _get(selector):
    if not selector:
        print("用法: python -m music_studio library get <编号或UUID前缀>")
        return
    _, entry = _resolve(selector)
    if not entry:
        return

    print("=== 记录详情 ===")
    import json
    print(json.dumps(entry, indent=2, ensure_ascii=False))


def _lyrics(selector):
    if not selector:
        print("用法: python -m music_studio library lyrics <编号或UUID前缀>")
        return
    resolved, entry = _resolve(selector)
    if not entry:
        return

    lyrics = _read_text_if_exists(
        entry.get("lyrics_path", ""),
        f"{resolved}.lyrics.txt",
        f"{_safe_name(entry.get('title', 'lyrics'), 'lyrics')}.lyrics.txt",
    )

    title = entry.get("title", "未知")
    print(f"=== {title} ===\n")
    print(lyrics or "无歌词内容")


def _url(selector):
    if not selector:
        print("用法: python -m music_studio library url <编号或UUID前缀>")
        return
    resolved, entry = _resolve(selector)
    if not entry:
        return

    url = entry.get("music_url", "") or _read_text_if_exists(
        entry.get("url_path", ""),
        f"{resolved}.url",
        f"{_safe_name(entry.get('title', 'music'), 'music')}.url",
    )
    print(url or "无链接")


def _tags(selector):
    if not selector:
        print("用法: python -m music_studio library tags <编号或UUID前缀>")
        return
    resolved, entry = _resolve(selector)
    if not entry:
        return

    tags = entry.get("style_tags", "") or _read_text_if_exists(
        entry.get("tags_path", ""),
        f"{resolved}.tags.txt",
        f"{_safe_name(entry.get('title', 'lyrics'), 'lyrics')}.tags.txt",
    )
    print(tags or "无标签")


def _download(selector):
    if not selector:
        print("用法: python -m music_studio library download <编号或UUID前缀>")
        return
    resolved, entry = _resolve(selector)
    if not entry:
        return

    song_type = entry.get("type", "")
    if song_type not in ("music", "cover"):
        print("⚠️  只有 music/cover 类型才有音频可下载")
        return

    existing = entry.get("local_path", "")
    if existing:
        print(f"✅ 本地音频已存在: {existing}")
        return

    audio_url = entry.get("music_url", "") or _read_text_if_exists(
        entry.get("url_path", ""),
        f"{resolved}.url",
        f"{_safe_name(entry.get('title', resolved), resolved)}.url",
    )
    if not audio_url:
        print("❌ 该记录没有音频链接，可能已过期")
        return

    print("📥 正在下载音频...")
    title = _safe_name(entry.get("title", resolved), resolved)
    out_file = _out() / f"{title}.mp3"
    try:
        size = _download_to_path(audio_url, out_file)
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return

    entry["local_path"] = str(out_file)
    lib = lib_mod.read_library()
    lib["songs"] = [s if s["id"] != resolved else entry for s in lib["songs"]]
    lib_mod.write_library(lib)

    print(f"✅ 已下载: {out_file} ({size / 1024:.1f} KB)")


def _export(subcmd=None, subarg=None):
    if subcmd == "all":
        _export_all()
    elif subcmd == "lyrics":
        _export_lyrics(subarg)
    else:
        print("用法: python -m music_studio library export lyrics <编号或UUID前缀>")
        print("       python -m music_studio library export all")


def _export_lyrics(selector):
    resolved, entry = _resolve(selector)
    if not entry:
        return

    lyrics = _read_text_if_exists(
        entry.get("lyrics_path", ""),
        f"{resolved}.lyrics.txt",
        f"{_safe_name(entry.get('title', 'lyrics'), 'lyrics')}.lyrics.txt",
    )
    if not lyrics:
        print("无歌词内容")
        return

    title = _safe_name(entry.get("title", "未知"), "未知")
    export_file = _out() / f"{title}.lyrics.txt"
    export_file.write_text(lyrics)
    print(f"✅ 歌词已导出: {export_file}")


def _export_all():
    lib_mod.remove_expired()
    lib = lib_mod.read_library()
    count = len(lib["songs"])
    print(f"📦 开始导出所有记录（{count} 条）...\n")

    for song in lib["songs"]:
        title = _safe_name(song.get("title", "未知"), "未知")
        song_type = song.get("type", "")

        if song.get("meta_path"):
            print(f"📝 说明文件: {song.get('meta_path')}")

        if song_type == "lyrics":
            lyrics = _read_text_if_exists(
                song.get("lyrics_path", ""),
                f"{song['id']}.lyrics.txt",
                f"{title}.lyrics.txt",
            )
            if lyrics:
                (_out() / f"{title}.lyrics.txt").write_text(lyrics)
                print(f"✅ 歌词: {title}.lyrics.txt")
            tags = _read_text_if_exists(
                song.get("tags_path", ""),
                f"{song['id']}.tags.txt",
                f"{title}.tags.txt",
            )
            if tags:
                (_out() / f"{title}.tags.txt").write_text(tags + ("\n" if not tags.endswith("\n") else ""))
                print(f"✅ 标签: {title}.tags.txt")
        elif song_type in ("music", "cover"):
            url = song.get("music_url", "") or _read_text_if_exists(
                song.get("url_path", ""),
                f"{song['id']}.url",
                f"{title}.url",
            )
            if url:
                (_out() / f"{title}.url").write_text(url + ("\n" if not url.endswith("\n") else ""))
                print(f"✅ 链接: {title}.url")
            if song.get("local_path"):
                print(f"✅ 音频: {song.get('local_path')}")

    print("\n导出完成")


def _clean():
    print("=== 清理过期记录 ===")
    removed = lib_mod.remove_expired()
    lib = lib_mod.read_library()
    remaining = len(lib["songs"])
    print(f"✅ 已移除 {removed} 条过期记录，剩余 {remaining} 条")


def _purge():
    print("⚠️  将删除所有输出文件和 library.json，操作不可恢复")
    confirm = input("确认执行 [y/N]: ").strip().lower()
    if confirm not in ("y",):
        print("已取消")
        return
    lib_mod.purge_all()
    print("✅ 已删除所有输出文件")
