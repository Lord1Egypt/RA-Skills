#!/usr/bin/env python3
"""
lyrics_searcher.py — 歌詞搜尋引擎
LRCLIB API 即時查詢 + 本地快取 + 手動歌詞建立
"""

import sys
import json
import re
import argparse
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

CACHE_DIR = Path.home() / ".karaoke-companion" / "lyrics_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ── LRCLIB API ───────────────────────────────────────────────────────────────

LRCLIB_BASE = "https://lrclib.net/api"

def search_lrclib(artist: str = "", title: str = "",
                  duration: int = 0) -> list[dict]:
    """搜尋 LRCLIB 歌詞庫"""
    params = {}
    if artist: params["artist"] = artist
    if title:  params["q"] = title
    if duration: params["duration"] = str(duration)

    url = f"{LRCLIB_BASE}/search"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "KaraokeCompanion/1.0"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
            if isinstance(data, list):
                return data
            return [data] if data else []
    except Exception as e:
        return []


def get_lrclib_track(id_or_url: str) -> dict | None:
    """取得特定歌詞（含完整 LRC），只接受 LRCLIB 數字 ID 或純數字字串"""
    # 安全：僅接受 LRCLIB API ID，杜絕任意 URL 請求
    if id_or_url.startswith("http"):
        print("⚠  請使用 LRCLIB 歌曲 ID，而非 URL。可用 `search` 查詢後取 ID。", file=sys.stderr)
        return None
    url = f"{LRCLIB_BASE}/{id_or_url}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "KaraokeCompanion/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:
        return None


def parse_lrc(raw_lrc: str, fallback_plain: str = "") -> list[dict]:
    """
    解析 LRC 為 [{time: float, text: str}] 列表
    time 為秒數，text 為該行的歌詞文字（去掉時間標記）
    """
    lines_out = []
    for line in raw_lrc.splitlines():
        line = line.strip()
        if not line:
            continue
        # 匹配 [mm:ss.xx] 或 [mm:ss:xx] 格式
        matches = re.findall(r'\[(\d{1,2}):(\d{2})[.:](\d{1,3})\]', line)
        text = re.sub(r'\[\d{1,2}:\d{2}[.:]\d{1,3}\]', '', line).strip()
        if text.startswith("作词") or text.startswith("作曲") or text.startswith("编曲"):
            continue
        for m in matches:
            minutes, seconds, centis = m
            t = int(minutes) * 60 + int(seconds) + int(centis.ljust(3, '0')) / 1000
            lines_out.append({"time": t, "text": text})
    return lines_out


def lrc_to_html(lrc_lines: list[dict]) -> list[dict]:
    """轉為 HTML karaoke 格式（現在唱的 + 下一句 + 緩衝）"""
    karaoke = []
    for i, line in enumerate(lrc_lines):
        prev = lrc_lines[i-1]["text"] if i > 0 else ""
        curr = line["text"]
        next1 = lrc_lines[i+1]["text"] if i+1 < len(lrc_lines) else ""
        next2 = lrc_lines[i+2]["text"] if i+2 < len(lrc_lines) else ""
        karaoke.append({
            "time": line["time"],
            "current": curr,
            "prev": prev,
            "next1": next1,
            "next2": next2,
        })
    return karaoke


# ── Cache ────────────────────────────────────────────────────────────────────

def cache_key(artist: str, title: str) -> str:
    import hashlib
    key = f"{artist}|{title}".lower()
    return hashlib.md5(key.encode()).hexdigest()


def cache_save(artist: str, title: str, data: dict):
    key = cache_key(artist, title)
    file = CACHE_DIR / f"{key}.json"
    out = dict(data)
    out["_cached_at"] = datetime.now().isoformat()
    file.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")


def cache_load(artist: str, title: str) -> dict | None:
    key = cache_key(artist, title)
    file = CACHE_DIR / f"{key}.json"
    if file.exists():
        age = datetime.now() - datetime.fromtimestamp(file.stat().st_mtime)
        if age.days < 7:  # 7天快取
            return json.loads(file.read_text(encoding="utf-8"))
    return None


# ── Plain text lyrics search (fallback) ──────────────────────────────────────

def search_plain_lyrics(query: str) -> list[dict]:
    """用 DuckDuckGo HTML 搜尋歌詞（非同步）"""
    url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query + ' 歌詞')}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        results = []
        for m in re.finditer(
            r'<a class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL
        ):
            snippet = re.sub(r"<[^>]+>", "", m.group(1)).strip()[:200]
            if snippet and any(c >= '\u4e00' for c in snippet):
                results.append({"type": "text", "snippet": snippet})
                if len(results) >= 3:
                    break
        return results
    except Exception:
        return []


# ── Manual lyrics builder ──────────────────────────────────────────────────────

def build_from_text(plain_text: str, bpm: float = 0,
                    line_interval: float = 3.0) -> dict:
    """
    將純文字歌詞自動對時（每行 3 秒，可調整）
    bpm 不為 0 時，按 BPM 計算（4/4 拍每行 4 小節 ≈ 4*60/BPM 秒）
    """
    lines = [l.strip() for l in plain_text.splitlines() if l.strip()]
    lrc_lines = []
    t = 0.0
    if bpm > 0:
        line_interval = 240.0 / bpm  # 4 bars
    for line in lines:
        lrc_lines.append({"time": round(t, 2), "text": line})
        t += line_interval

    lrc_parts = []
    for item in lrc_lines:
        s = item["time"]
        text = item["text"]
        part = f"[{int(s//60):02d}:{int(s%60):02d}.00]{text}"
        lrc_parts.append(part)
    lrc_text = "\n".join(lrc_parts)
    return {
        "plain_text": plain_text,
        "lines": lrc_lines,
        "lrc": lrc_text,
        "source": "manual",
        "duration": lrc_lines[-1]["time"] if lrc_lines else 0,
    }


# ── Lyrics display helpers ────────────────────────────────────────────────────

def _fmt_time(t: float) -> str:
    m = int(t // 60)
    s = int(t % 60)
    cs = int((t % 1) * 100)
    return f"{m:02d}:{s:02d}.{cs:02d}"


def render_search_results(results: list[dict], query: str) -> str:
    lines = [f"\n🎤 搜尋「{query}」，共 {len(results)} 筆：\n"]
    for i, r in enumerate(results[:8], 1):
        name  = r.get("trackName", r.get("name", "?"))
        artist = r.get("artistName", r.get("artist", "?"))
        album = r.get("albumName", r.get("album", ""))
        dur   = r.get("duration", 0)
        has_lrc = bool(r.get("syncedLyrics") or r.get("plainLyrics"))

        dur_str = f"⏱️ {int(dur//60)}:{int(dur%60):02d}" if dur else ""
        lrc_icon = "📝 有同步歌詞" if has_lrc else "📄 僅文字歌詞"
        lines.append(
            f"  {i}. 🎵 {name}\n"
            f"     👤 {artist}" + (f"  💿 {album}" if album else "") + "\n"
            f"     {lrc_icon} {dur_str}"
        )
        if r.get("syncedLyrics"):
            preview = r["syncedLyrics"].splitlines()[1][:60] if "\n" in r["syncedLyrics"] else ""
            lines.append(f"     → {preview}")
        lines.append("")
    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="🎤 歌詞搜尋引擎")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("search", help="搜尋歌詞")
    p.add_argument("query", help="歌名或歌手")
    p.add_argument("-a", "--artist", default="")
    p.add_argument("-d", "--duration", type=int, default=0)

    p = sub.add_parser("get", help="用 LRCLIB 歌曲 ID 取得歌詞")
    p.add_argument("id", help="LRCLIB 歌曲 ID（整數）")

    p = sub.add_parser("parse", help="解析 LRC 文字")
    p.add_argument("lrc_file", type=Path, nargs="?")
    p.add_argument("-t", "--text", help="直接輸入 LRC 文字")
    p.add_argument("-s", "--speed", type=float, default=3.0,
                   help="每行秒數（純文字模式）")
    p.add_argument("-b", "--bpm", type=float, default=0,
                   help="BPM（純文字模式，按 BPM 自動計算）")

    p = sub.add_parser("build", help="從純文字建立歌詞（自動對時）")
    p.add_argument("-f", "--file", type=Path)
    p.add_argument("-t", "--text", help="歌詞文字（多行）")
    p.add_argument("-s", "--speed", type=float, default=3.0)
    p.add_argument("-b", "--bpm", type=float, default=0)

    p = sub.add_parser("cache-list", help="列出快取歌詞")

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])

    def log(msg=""): print(msg)

    if args.cmd == "search":
        q = args.query
        results = search_lrclib(artist=args.artist, title=q,
                                 duration=args.duration)
        if not results:
            log(f"\n❌ 找不到「{q}」的歌詞，嘗試純文字搜尋...")
            plain = search_plain_lyrics(q)
            for r in plain:
                log(f"  📄 {r['snippet']}")
            return
        log(render_search_results(results, q))
        log("  使用 `get` + ID 或 URL 取得完整歌詞")

    elif args.cmd == "get":
        track = get_lrclib_track(args.id)
        if not track:
            log("❌ 找不到或請求失敗"); return

        log(f"\n🎤 {track.get('trackName','?')} — {track.get('artistName','?')}")
        if track.get("albumName"):
            log(f"  💿 {track['albumName']}")

        if track.get("syncedLyrics"):
            log("\n📝 同步歌詞（LRC）：")
            log(track["syncedLyrics"][:800] + ("..." if len(track.get("syncedLyrics","")) > 800 else ""))
        elif track.get("plainLyrics"):
            log("\n📄 純文字歌詞：")
            log(track["plainLyrics"][:800] + ("..." if len(track.get("plainLyrics","")) > 800 else ""))
        else:
            log("\n⚠️  此曲目沒有歌詞")

    elif args.cmd == "parse":
        lrc_text = ""
        if args.lrc_file and args.lrc_file.exists():
            lrc_text = args.lrc_file.read_text(encoding="utf-8", errors="replace")
        elif args.text:
            lrc_text = args.text
        else:
            log("❌ 請提供 -t 文字 或 LRC 檔案"); return

        if args.bpm > 0:
            args.speed = 240.0 / args.bpm

        # If it's not in LRC format, build from plain text
        if not re.search(r'\[\d{2}:\d{2}', lrc_text):
            built = build_from_text(lrc_text, bpm=args.bpm, line_interval=args.speed)
            lrc_lines = built["lines"]
            log(f"\n📝 已自動對時（每行 {args.speed:.1f} 秒），共 {len(lrc_lines)} 行：")
            for item in lrc_lines[:10]:
                log(f"  [{_fmt_time(item['time'])}] {item['text']}")
            if len(lrc_lines) > 10:
                log(f"  ...（共 {len(lrc_lines)} 行）")
        else:
            lrc_lines = parse_lrc(lrc_text)
            log(f"\n📝 LRC 解析完成，共 {len(lrc_lines)} 行：")
            for item in lrc_lines[:10]:
                log(f"  [{_fmt_time(item['time'])}] {item['text']}")
            if len(lrc_lines) > 10:
                log(f"  ...（共 {len(lrc_lines)} 行）")

    elif args.cmd == "build":
        text = ""
        if args.file and args.file.exists():
            text = args.file.read_text(encoding="utf-8", errors="replace")
        elif args.text:
            text = args.text
        else:
            log("❌ 請提供 -f 檔案 或 -t 文字"); return

        built = build_from_text(text, bpm=args.bpm, line_interval=args.speed)
        log(f"\n✅ 歌詞已建立，共 {len(built['lines'])} 行，時長 {built['duration']:.0f} 秒")
        log("\n📝 LRC 格式：")
        log(built["lrc"])

    elif args.cmd == "cache-list":
        files = list(CACHE_DIR.glob("*.json"))
        if not files:
            log("📭 快取為空"); return
        log(f"\n💾 快取歌詞（共 {len(files)} 筆）：\n")
        for f in sorted(files, key=lambda x: -x.stat().st_mtime)[:20]:
            d = json.loads(f.read_text(encoding="utf-8"))
            name = d.get("trackName", d.get("plain_text", "?"))[:40]
            log(f"  {f.stem[:12]}... | {name}")


if __name__ == "__main__":
    main()
