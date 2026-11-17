#!/usr/bin/env python3
"""
lyrics_creator.py — 填詞創作工具
模式 B：空白模板 + 韻腳提示 + 節奏引導
支援：韻腳生成、押韻表、段落模板、BPM 計算字數
"""

import sys
import json
import re
import argparse
import random
from pathlib import Path
from datetime import datetime

DATA_DIR = Path.home() / ".karaoke-companion" / "songs"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── 韻腳資料庫 ─────────────────────────────────────────────────────────────

# 國語聲韻分類
RHYMES: dict[str, list[str]] = {
    "ang":  ["光", "央", "香", "鄉", "蒼", "涼", "傷", "長", "牆", "湯", "航", "忙", "王", "康", "房"],
    "eng":  ["風", "中", "城", "生", "疼", "恆", "疼", "曾", "增", "燈", "疼", "疼", "疼", "疼", "疼"],
    "ing":  ["星", "情", "聲", "輕", "聽", "明", "平", "清", "名", "晴", "青", "零", "冰", "心", "盈"],
    "ong":  ["空", "中", "同", "紅", "風", "龍", "宮", "重", "工", "東", "終", "蹤", "洪", "叢", "雄"],
    "ai":   ["愛", "在", "來", "海", "彩", "白", "才", "開", "懷", "改", "賽", "外", "台", "待", "待"],
    "ei":   ["美", "水", "累", "誰", "北", "灰", "飛", "隨", "配", "催", "回", "杯", "退", "對", "雷"],
    "ao":   ["好", "到", "找", "草", "跑", "道", "抱", "倒", "高", "笑", "造", "毛", "早", "操", "奧"],
    "ou":   ["口", "走", "候", "收", "秋", "酒", "有", "頭", "手", "柔", "樓", "丘", "投", "遊", "後"],
    "an":   ["安", "山", "天", "藍", "看", "站", "慢", "單", "飯", "難", "眼", "前", "年", "田", "寒"],
    "en":   ["人", "真", "門", "疼", "本", "等", "生", "哼", "根", "疼", "疼", "疼", "疼", "疼", "疼"],
    "iang": ["想", "香", "陽", "鄉", "光", "長", "忙", "牆", "湯", "翔", "涼", "狂", "唱", "上", "芳"],
    "iang2":["量", "江", "僵", "匠", "相", "娘", "將", "羊", "香", "詳", "降", "疆", "詳", "翔", "商"],
    "ong2": ["龍", "中", "重", "風", "工", "蹤", "東", "公", "紅", "洪", "通", "洪", "叢", "空", "筒"],
    "er":   ["兒", "而", "二", "耳", "爾", "爾", "爾", "爾", "爾", "爾", "爾", "爾", "爾", "爾", "爾"],
}

RHYME_NAMES: dict[str, str] = {
    "ang":  "昂聲（-ang/-eng 如：光/風）",
    "eng":  "eng（-eng 如：中/生）",
    "ing":  "ing（-ing 如：星/情）",
    "ong":  "ong（-ong 如：空/中）",
    "ai":   "愛聲（-ai 如：愛/在）",
    "ei":   "ei聲（-ei 如：水/美）",
    "ao":   "奧聲（-ao 如：好/到）",
    "ou":   "歐聲（-ou 如：走/口）",
    "an":   "安聲（-an 如：安/山）",
    "en":   "恩聲（-en 如：人/真）",
    "iang": "央聲（-iang 如：想/光）",
    "iang2": "央2（-iang 如：量/將）",
    "ong2": "ong2（-ong 如：龍/重）",
    "er":   "兒化（-er 如：兒/而）",
}


# ── 段落模板 ───────────────────────────────────────────────────────────────

VERSE_TEMPLATES = {
    "verse_2line": {
        "label": "二句式（主歌）",
        "lines": 2,
        "syllables": [7, 7],
        "rhyme": [True, True],
        "structure": "第一句7字 → 第二句7字押韻",
    },
    "verse_4line": {
        "label": "四句式（主歌）",
        "lines": 4,
        "syllables": [7, 7, 7, 7],
        "rhyme": [False, True, False, True],
        "structure": "七言絕句風：第2、4句押韻",
    },
    "chorus_4line": {
        "label": "四句式（副歌）",
        "lines": 4,
        "syllables": [7, 7, 5, 7],
        "rhyme": [False, True, False, True],
        "structure": "副歌：第2、4句押韻，第3句稍短",
    },
    "rap_4beat": {
        "label": "四拍 Rap",
        "lines": 4,
        "syllables": [10, 10, 10, 10],
        "rhyme": [True, False, True, False],
        "structure": "Rap：1押、2不押、3押、4不押",
    },
    "bridge_2line": {
        "label": "二句橋段",
        "lines": 2,
        "syllables": [9, 9],
        "rhyme": [True, True],
        "structure": "橋段：感嘆句，押韻",
    },
}

# ── 創作主題 ───────────────────────────────────────────────────────────────

THEMES: dict[str, list[str]] = {
    "love":      ["初戀", "暗戀", "失戀", "熱戀", "遠距離", "告別", "重逢", "思念", "錯過", "珍惜"],
    "growth":    ["勇氣", "夢想", "追尋", "失敗", "成長", "抉擇", "突破", "堅持", "初心", "告別過去"],
    "life":      ["時光", "城市", "夜歸", "日常", "孤獨", "陪伴", "離別", "平凡", "選擇", "代價"],
    "nature":    ["雨天", "星空", "海洋", "森林", "秋風", "春雨", "日出", "月夜", "四季", "雨後彩虹"],
    "family":    ["父母", "童年", "故鄉", "老家", "餐桌", "離家", "歸途", "家書", "背影", "愛"],
}


# ── 生成輔助 ───────────────────────────────────────────────────────────────

def suggest_rhymes(exclude: list[str] = None) -> dict[str, list[str]]:
    """建議不重複的韻腳"""
    exclude = set(exclude or [])
    suggestions = {}
    for k, words in RHYMES.items():
        avail = [w for w in words if w not in exclude]
        if avail:
            suggestions[k] = avail[:6]
    return suggestions


def print_rhyme_guide(exclude: list[str] = None):
    """印出韻腳指引"""
    suggestions = suggest_rhymes(exclude)
    print("\n🎵 可用韻腳參考：\n")
    for k, words in suggestions.items():
        label = RHYME_NAMES.get(k, k)
        examples = "、".join(words[:4])
        print(f"  {k:<8} {label}")
        print(f"           示範字：{examples}")
    print()


def generate_verse_template(verse_type: str, theme: str = "life",
                           bpm: float = 0, given_rhymes: list = None) -> str:
    """生成一個空白段落模板"""
    tpl = VERSE_TEMPLATES.get(verse_type, VERSE_TEMPLATES["verse_4line"])
    lines  = tpl["lines"]
    syls   = tpl["syllables"]
    rhymes = tpl["rhyme"]

    # Pick rhymes
    given_rhymes = given_rhymes or []
    selected = []
    for i in range(lines):
        if rhymes[i] and i < len(given_rhymes):
            selected.append(given_rhymes[i])
        elif rhymes[i]:
            avail = list(RHYMES.values())[random.randint(0, len(RHYMES)-1)]
            selected.append(random.choice(avail))
        else:
            selected.append("_")

    theme_words = random.choice(THEMES.get(theme, THEMES["life"]))

    out = []
    out.append(f"╔{'═'*52}╗")
    out.append(f"║ {tpl['label']}（{tpl['structure']}）              ║")
    out.append(f"╠{'═'*52}╣")

    for i in range(lines):
        s = syls[i]
        r = selected[i]
        rhyme_hint = f"【押{r}】" if rhymes[i] else "      "
        placeholder = "_" * (s * 2 - 3) + "…" if s >= 5 else "…"

        if rhymes[i]:
            line = f"║  {i+1}. 【{s}字】{rhyme_hint:<12}{placeholder:<20}║"
        else:
            line = f"║  {i+1}. 【{s}字】              {placeholder:<20}║"
        out.append(line)

    out.append(f"╠{'═'*52}╣")
    out.append(f"║ 主題方向：{theme_words:<40}║")
    out.append(f"╚{'═'*52}╝")
    return "\n".join(out)


def generate_full_template(title: str, genre: str = "pop",
                          bpm: float = 0) -> str:
    """生成完整歌曲模板"""
    lines_out = []
    bpm_note = f"BPM ≈ {bpm:.0f}" if bpm else "BPM 未定"

    lines_out.extend([
        "",
        "╔════════════════════════════════════════════════════════╗",
        "║  🎤 填詞創作模板                                      ║",
        "╠════════════════════════════════════════════════════════╣",
        f"║  歌名：《{title}》                                  ║",
        f"║  風格：{genre:<47}║",
        f"║  {bpm_note:<53}║",
        "╚════════════════════════════════════════════════════════╝",
        "",
        "─" * 56,
        "📝 段落結構建議：",
        "",
        "  【前奏】  4小節 →  intro",
        "  【主歌1】Verse 1 — 說故事（4句 x 2段）",
        "  【預副歌】Pre-chorus — 情緒升溫",
        "  【副 歌】Chorus — 高潮（4句）",
        "  【主歌2】Verse 2 — 深化情感",
        "  【副 歌】Chorus — 再次高潮",
        "  【橋 段】Bridge — 轉折（2句）",
        "  【副 歌】Final Chorus — 最終爆發",
        "  【尾 奏】Outro — 情緒釋放",
        "",
    ])

    # Generate example template for each section
    sections = [
        ("前奏", "intro", "四句式（主歌）", "nature", []),
        ("主歌1 A", "verse_4line", "四句式（主歌）", "life", []),
        ("主歌1 B", "verse_4line", "四句式（主歌）", "life", []),
        ("預副歌", "verse_2line", "二句式（主歌）", "growth", []),
        ("副歌", "chorus_4line", "四句式（副歌）", "love", []),
        ("主歌2 A", "verse_4line", "四句式（主歌）", "life", []),
        ("主歌2 B", "verse_4line", "四句式（主歌）", "life", []),
        ("副歌", "chorus_4line", "四句式（副歌）", "love", []),
        ("橋段", "bridge_2line", "二句橋段", "growth", []),
        ("尾聲", "verse_2line", "二句式（主歌）", "nature", []),
    ]

    for label, key, _, theme_key, rhymes in sections:
        lines_out.append(f"  ── {label} ──")
        lines_out.append(generate_verse_template(key, theme_key, bpm, rhymes))
        lines_out.append("")

    return "\n".join(lines_out)


# ── 字數計算器 ─────────────────────────────────────────────────────────────

def count_chars(text: str) -> dict:
    """計算字數"""
    chars = [c for c in text if c.strip()]
    total = len(chars)
    zh = sum(1 for c in chars if '\u4e00' <= c <= '\u9fff')
    en = sum(1 for c in chars if c.isalpha())
    num = sum(1 for c in chars if c.isdigit())
    return {
        "total":    total,
        "chinese":  zh,
        "english":  en,
        "numbers":  num,
        "chars":    chars,
    }


def check_line_fit(text: str, target: int) -> str:
    """檢查一行是否符合字數要求"""
    counts = count_chars(text)
    diff = counts["total"] - target
    if diff == 0:
        return f"✅ 剛好 {target} 字"
    elif diff > 0:
        return f"⚠️ 超過 {diff} 字（{counts['total']}/{target}）"
    else:
        return f"📝 少 {-diff} 字（{counts['total']}/{target}）"


def bpm_to_bar(bpm: float) -> dict:
    """BPM → 每小節秒數"""
    if bpm <= 0:
        return {"bar_sec": 0, "4bar_sec": 0, "note_4bar": "?"}
    bar = 60.0 / (bpm / 4)  # 4 beats per bar
    return {
        "bar_sec":   round(bar, 2),
        "4bar_sec":  round(bar * 4, 1),
        "8bar_sec":  round(bar * 8, 1),
        "16bar_sec": round(bar * 16, 1),
    }


# ── 歌曲保存 ───────────────────────────────────────────────────────────────

def save_song(title: str, lyrics: str, genre: str = "", bpm: float = 0) -> Path:
    file = DATA_DIR / f"{title}.txt"
    content = f"# {title}\n# 風格：{genre} | BPM：{bpm}\n# 建立：{datetime.now().strftime('%Y-%m-%d')}\n\n{lyrics}"
    file.write_text(content, encoding="utf-8")
    return file


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="🎤 填詞創作工具")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("guide",   help="韻腳指引")

    p = sub.add_parser("verse",   help="生成段落模板")
    p.add_argument("-t", "--type", choices=list(VERSE_TEMPLATES.keys()),
                   default="verse_4line")
    p.add_argument("-m", "--theme", default="life",
                   choices=list(THEMES.keys()))
    p.add_argument("-r", "--rhyme", nargs="+", help="指定韻腳")
    p.add_argument("-b", "--bpm", type=float, default=0)

    p = sub.add_parser("song",    help="生成完整歌曲模板")
    p.add_argument("title", help="歌名")
    p.add_argument("-g", "--genre", default="流行")
    p.add_argument("-b", "--bpm", type=float, default=120)

    p = sub.add_parser("rhyme",   help="查詢韻腳")
    p.add_argument("char", help="韻腳字")

    p = sub.add_parser("count",   help="計算字數")
    p.add_argument("text", help="要計算的文字")

    p = sub.add_parser("bpm",     help="BPM 計算器")
    p.add_argument("bpm", type=float, nargs="?", default=120)

    p = sub.add_parser("save",    help="儲存歌詞")
    p.add_argument("title", help="歌名")
    p.add_argument("-l", "--lyrics", help="歌詞內容")
    p.add_argument("-f", "--file", type=Path)
    p.add_argument("-g", "--genre", default="流行")
    p.add_argument("-b", "--bpm", type=float, default=0)

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["guide"])

    def log(msg=""): print(msg)

    if args.cmd == "guide":
        print_rhyme_guide()

    elif args.cmd == "verse":
        out = generate_verse_template(args.type, args.theme, args.bpm, args.rhyme or [])
        log(out)

    elif args.cmd == "song":
        out = generate_full_template(args.title, args.genre, args.bpm)
        log(out)

    elif args.cmd == "rhyme":
        c = args.char[0] if args.char else ""
        found = None
        for k, words in RHYMES.items():
            if c in words:
                found = k; break
        if found:
            label = RHYME_NAMES.get(found, found)
            same_rhyme = RHYMES[found]
            log(f"\n🎵 「{c}」屬於韻腳：{label}")
            log(f"   同韻字：{'、'.join(same_rhyme)}")
        else:
            log(f"\n❌ 「{c}」不在韻腳庫中")

    elif args.cmd == "count":
        result = count_chars(args.text)
        log(f"\n📊 字數統計：")
        log(f"  總字數：{result['total']}")
        log(f"  中文：{result['chinese']}  英文：{result['english']}  數字：{result['numbers']}")

    elif args.cmd == "bpm":
        info = bpm_to_bar(args.bpm)
        log(f"\n⏱️  BPM {args.bpm} 節奏計算：")
        log(f"  每小節（4拍）：{info['bar_sec']} 秒")
        log(f"  4小節：{info['4bar_sec']} 秒")
        log(f"  8小節：{info['8bar_sec']} 秒")
        log(f"  16小節：{info['16bar_sec']} 秒")

    elif args.cmd == "save":
        lyrics = ""
        if args.file and args.file.exists():
            lyrics = args.file.read_text(encoding="utf-8", errors="replace")
        elif args.lyrics:
            lyrics = args.lyrics
        else:
            log("❌ 請提供 -f 檔案 或 -l 歌詞文字"); return
        path = save_song(args.title, lyrics, args.genre, args.bpm)
        log(f"✅ 已儲存：{path}")


if __name__ == "__main__":
    main()
