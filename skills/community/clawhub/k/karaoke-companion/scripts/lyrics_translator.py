#!/usr/bin/env python3
"""
lyrics_translator.py — 翻譯對照模式
模式 C：中/英/日 三語同步歌詞顯示
支援：LRCLIB 取原文、翻譯對照、並排顯示、關鍵字標記
"""

import sys
import json
import re
import argparse
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

CACHE_DIR = Path.home() / ".karaoke-companion" / "trans_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

LRCLIB_BASE = "https://lrclib.net/api"


# ── Translation via LibreTranslate ─────────────────────────────────────────────

def translate_text(text: str, from_lang: str = "auto",
                   to_lang: str = "zh") -> str | None:
    """
    用 LibreTranslate（免費開源）翻譯
    """
    try:
        url = "https://libretranslate.com/translate"
        data = json.dumps({
            "q": text,
            "source": from_lang,
            "target": to_lang,
            "format": "text",
        }).encode("utf-8")
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json",
                     "User-Agent": "KaraokeCompanion/1.0"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("translatedText")
    except Exception:
        pass
    return None


def translate_batch(lines: list[str], from_lang: str = "en",
                    to_lang: str = "zh") -> list[str | None]:
    """批量翻譯"""
    results = []
    for text in lines:
        if not text.strip():
            results.append("")
            continue
        # Batch limit
        translated = translate_text(text, from_lang, to_lang)
        results.append(translated)
        if translated:
            # Small delay to be polite
            import time; time.sleep(0.3)
    return results


# ── Japanese romanization ──────────────────────────────────────────────────────

# Simple hiragana/katakana charts (subset)
KATAKANA_CHARS = {
    "a": "ア", "i": "イ", "u": "ウ", "e": "エ", "o": "オ",
    "ka": "カ", "ki": "キ", "ku": "ク", "ke": "ケ", "ko": "コ",
    "sa": "サ", "si": "シ", "su": "ス", "se": "セ", "so": "ソ",
    "ta": "タ", "chi": "チ", "tsu": "ツ", "te": "テ", "to": "ト",
    "na": "ナ", "ni": "ニ", "nu": "ヌ", "ne": "ネ", "no": "ノ",
    "ha": "ハ", "hi": "ヒ", "fu": "フ", "he": "ヘ", "ho": "ホ",
    "ma": "マ", "mi": "ミ", "mu": "ム", "me": "メ", "mo": "モ",
    "ra": "ラ", "ri": "リ", "ru": "ル", "re": "レ", "ro": "ロ",
    "wa": "ワ", "wo": "ヲ", "n": "ン",
    "ga": "ガ", "gi": "ギ", "gu": "グ", "ge": "ゲ", "go": "ゴ",
    "da": "ダ", "di": "ヂ", "du": "ヅ", "de": "デ", "do": "ド",
    "ba": "バ", "bi": "ビ", "bu": "ブ", "be": "ベ", "bo": "ボ",
}

HIRAGANA_CHARS = {
    "a": "あ", "i": "い", "u": "う", "e": "え", "o": "お",
    "ka": "か", "ki": "き", "ku": "く", "ke": "け", "ko": "こ",
    "sa": "さ", "shi": "し", "su": "す", "se": "せ", "so": "そ",
    "ta": "た", "chi": "ち", "tsu": "つ", "te": "て", "to": "と",
    "na": "な", "ni": "に", "nu": "ぬ", "ne": "ね", "no": "の",
    "ha": "は", "hi": "ひ", "fu": "ふ", "he": "へ", "ho": "ほ",
    "ma": "ま", "mi": "み", "mu": "む", "me": "め", "mo": "も",
    "ra": "ら", "ri": "り", "ru": "る", "re": "れ", "ro": "ろ",
    "wa": "わ", "wo": "を", "n": "ん",
}

# Common romaji→katakana (full words)
ROMAJI_KATAKANA = {
    "love": "ラブ", "kiss": "キス", "baby": "ベビー",
    "heart": "ハート", "song": "ソング", "music": "ミュージック",
    "dream": "ドリーム", "sky": "スカイ", "star": "スター",
    "moon": "ムーン", "sun": "サン", "rain": "レイン",
    "night": "ナイト", "day": "デイ", "you": "ユー",
    "me": "ミー", "i": "アイ", "we": "ウィ",
    "happy": "ハッピー", "sad": "サッド", "crazy": "クレイジー",
    "party": "パーティー", "dance": "ダンス", "run": "リーン",
}


def to_katakana(text: str) -> str:
    """簡單的羅馬字→片假名轉換"""
    result = text
    for romaji, kata in ROMAJI_KATAKANA.items():
        result = re.sub(rf'\b{romaji}\b', kata, result, flags=re.IGNORECASE)
    # Individual chars
    result2 = ""
    i = 0
    while i < len(result):
        # Try 2-char match
        if i + 1 < len(result):
            two = result[i:i+2].lower()
            if two in KATAKANA_CHARS:
                result2 += KATAKANA_CHARS[two]
                i += 2
                continue
        # Try 1-char
        one = result[i].lower()
        if one in KATAKANA_CHARS:
            result2 += KATAKANA_CHARS[one]
        else:
            result2 += result[i]
        i += 1
    return result2


# ── LRC parse ────────────────────────────────────────────────────────────────

def parse_lrc(raw: str) -> list[dict]:
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        matches = re.findall(r'\[(\d{1,2}):(\d{2})[.:](\d{1,3})\]', line)
        text = re.sub(r'\[\d{1,2}:\d{2}[.:]\d{1,3}\]', '', line).strip()
        if not text:
            continue
        for m in matches:
            minutes, seconds, centis = m
            t = int(minutes) * 60 + int(seconds) + int(centis.ljust(3,'0')) / 1000
            lines.append({"time": t, "text": text})
    lines.sort(key=lambda x: x["time"])
    return lines


def parse_plain(plain: str, interval: float = 4.0) -> list[dict]:
    lines = []
    t = 0.0
    for text in plain.splitlines():
        text = text.strip()
        if not text:
            continue
        lines.append({"time": t, "text": text})
        t += interval
    return lines


# ── Compare display ───────────────────────────────────────────────────────────

RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"


def _fmt_time(t: float) -> str:
    return f"{int(t//60):02d}:{int(t%60):02d}"


def render_comparison(lines: list[dict],
                     translations: list[str | None],
                     originals: list[str],
                     lang_labels: tuple[str, str] = ("原文", "中文")) -> str:
    """三欄對照顯示"""
    if not lines:
        return f"{YELLOW}  沒有歌詞{RESET}"

    out = []
    out.append(f"{BOLD}{CYAN}🎤 翻譯對照模式{RESET}")
    out.append("─" * 60)
    out.append(f"  {DIM}左：{lang_labels[0]}  │  右：{lang_labels[1]}{RESET}")
    out.append("─" * 60)

    for i, item in enumerate(lines):
        orig = item.get("text", originals[i] if i < len(originals) else "")
        trans = translations[i] if i < len(translations) else ""
        t_str = _fmt_time(item.get("time", 0))

        # Color code
        orig_display = f"{GREEN}{orig}{RESET}"
        if trans:
            trans_display = f"{YELLOW}{trans}{RESET}"
        else:
            trans_display = f"{DIM}（翻譯中...）{RESET}"

        out.append(f"\n  {BOLD}[{t_str}]{RESET}")
        out.append(f"  {orig_display}")
        out.append(f"  {trans_display}")

    return "\n".join(out)


def render_live_compare(lines: list[dict],
                        translations: list[str | None],
                        originals: list[str],
                        current_idx: int,
                        lang_labels: tuple[str, str]) -> str:
    """Live 卡拉 OK 對照模式"""
    out = []
    out.append("\033[2J\033[H")  # clear
    total = len(lines)
    out.append(f"{BOLD}{CYAN}🎤 KARAOKE 翻譯對照 — [{current_idx+1}/{total}]{RESET}")
    out.append("─" * 60)
    out.append(f"{DIM}左：{lang_labels[0]}  │  右：{lang_labels[1]}{RESET}")
    out.append("─" * 60)

    # Show prev, current, next
    start = max(0, current_idx - 1)
    end   = min(total, current_idx + 3)

    for i in range(start, end):
        item = lines[i]
        orig  = item.get("text", originals[i] if i < len(originals) else "")
        trans = translations[i] if i < len(translations) else ""

        if i == current_idx:
            out.append(f"\n  {BOLD}{GREEN}▶ {orig}{RESET}")
            if trans:
                out.append(f"  {YELLOW}  {trans}{RESET}")
            out.append(f"  {DIM}  [{_fmt_time(item['time'])}]{RESET}")
        else:
            out.append(f"\n  {DIM}  {orig}{RESET}")

    return "\n".join(out)


# ── CJK detection ─────────────────────────────────────────────────────────────

def detect_lang(text: str) -> str:
    """簡單語言偵測"""
    zh = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    ja = sum(1 for c in text if '\u3040' <= c <= '\u30ff')
    en = sum(1 for c in text if c.isalpha() and c.isascii())
    total = max(1, zh + ja + en)
    if ja / total > 0.3:
        return "ja"
    elif zh / total > 0.3:
        return "zh"
    elif en / total > 0.5:
        return "en"
    return "en"


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="🎤 歌詞翻譯對照")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("compare", help="對照顯示")
    p.add_argument("lyrics_file", type=Path, nargs="?", default=None)
    p.add_argument("-t", "--text", help="歌詞文字")
    p.add_argument("-s", "--source-lang", default="en")
    p.add_argument("-d", "--dest-lang", default="zh")
    p.add_argument("-i", "--interval", type=float, default=4.0)
    p.add_argument("-o", "--output", type=Path, help="輸出檔案")
    p.add_argument("--no-translate", action="store_true")

    p = sub.add_parser("live",   help="Live 對照模式")
    p.add_argument("lyrics_file", type=Path, nargs="?", default=None)
    p.add_argument("-t", "--text")
    p.add_argument("-s", "--source-lang", default="en")
    p.add_argument("-d", "--dest-lang", default="zh")
    p.add_argument("-i", "--interval", type=float, default=4.0)

    p = sub.add_parser("katakana", help="轉換為片假名")
    p.add_argument("text", nargs="?", help="要轉換的文字")

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])

    def log(msg=""): print(msg)

    # Load lyrics
    raw_lines = []
    lyrics_file = getattr(args, 'lyrics_file', None)
    if lyrics_file and lyrics_file.exists():
        raw = lyrics_file.read_text(encoding="utf-8", errors="replace")
        if re.search(r'\[\d{2}:\d{2}', raw):
            raw_lines = parse_lrc(raw)
        else:
            raw_lines = parse_plain(raw, getattr(args, 'interval', 4.0))
    elif args.text:
        if re.search(r'\[\d{2}:\d{2}', args.text):
            raw_lines = parse_lrc(args.text)
        else:
            raw_lines = parse_plain(args.text, getattr(args, 'interval', 4.0))
    else:
        # Demo
        raw_lines = parse_plain(
            "I love you more than words can say\n"
            "Every night I dream of you\n"
            "Under the moonlight so bright\n"
            "You are my only star tonight\n"
            "Dancing in the rain together\n"
            "Forever holding hands forever", interval=4.0)

    originals = [item["text"] for item in raw_lines]

    if args.cmd == "katakana":
        text = args.text or "Hello World Love Dream"
        kata = to_katakana(text)
        log(f"\n  原文：{text}\n  片假名：{kata}")
        return

    if args.cmd == "compare":
        if args.no_translate:
            translations = [""] * len(originals)
        else:
            log(f"\n🔄 正在翻譯 {len(originals)} 行（請稍候）...")
            translations = []
            for i, text in enumerate(originals):
                lang = detect_lang(text)
                src = lang if lang != "en" else (args.source_lang or "en")
                dst = args.dest_lang or "zh"
                trans = translate_text(text, src, dst) if src != dst else ""
                translations.append(trans)
                if (i + 1) % 5 == 0:
                    log(f"  已翻譯 {i+1}/{len(originals)} 行...")

        result = render_comparison(raw_lines, translations, originals,
                                 lang_labels=(args.source_lang.upper(), args.dest_lang.upper()))

        if args.output:
            args.output.write_text(result, encoding="utf-8")
            log(f"\n✅ 已儲存至：{args.output}")
        else:
            log(result)

    elif args.cmd == "live":
        log(f"\n🔄 翻譯中...")
        translations = []
        for text in originals:
            lang = detect_lang(text)
            src = lang if lang != "en" else (args.source_lang or "en")
            dst = args.dest_lang or "zh"
            trans = translate_text(text, src, dst) if src != dst else ""
            translations.append(trans)

        log(f"✅ 翻譯完成，開始 Live 對照...")
        log(f"{DIM}按 Ctrl+C 退出{RESET}")
        import time
        try:
            idx = 0
            while idx < len(raw_lines):
                print(render_live_compare(raw_lines, translations, originals,
                                        idx,
                                        (args.source_lang.upper(),
                                         args.dest_lang.upper())))
                time.sleep(max(1.0, raw_lines[idx+1]["time"] - raw_lines[idx]["time"]) if idx+1 < len(raw_lines) else 4.0)
                idx += 1
            print(f"\n{GREEN}✅ 對照結束！{RESET}")
        except KeyboardInterrupt:
            print(f"\n{DIM}已退出{RESET}")


if __name__ == "__main__":
    main()
