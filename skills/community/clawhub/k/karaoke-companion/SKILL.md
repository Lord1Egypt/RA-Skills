---
name: karaoke-companion
description: 歌詞隨唱伴侶 — 跟著歌詞學唱歌、卡拉 OK 模式練歌、填詞創作（含韻腳表）、中英日翻譯對照。LRCLIB 即時歌詞，支援減速、段落反覆。
---

# 🎤 歌詞隨唱伴侶（Karaoke Companion）

## 概述

專為「想學唱歌但不知道從哪裡開始」的人設計。跟著同步歌詞學唱、卡拉 OK 練習、填詞創作、翻譯對照，全部一站式完成。

**觸發關鍵字：** 練歌、學唱歌、卡拉 OK、跟著唱、歌詞、填詞、韻腳、這首歌在唱什麼、中文翻譯、英文翻譯、日文翻譯

---

## 三種模式

| 模式 | 腳本 | 說明 |
|------|------|------|
| 🎤 練歌模式 | `karaoke_player.py` | 減速 0.75x、逐句對唱、段落反覆 |
| ✍️ 填詞創作 | `lyrics_creator.py` | 空白模板、韻腳表、BPM 計算 |
| 🌏 翻譯對照 | `lyrics_translator.py` | 中/英/日同步顯示、即時翻譯 |

---

## 腳本清單

| 腳本 | 用途 |
|------|------|
| `scripts/lyrics_searcher.py` | LRCLIB 即時歌詞搜尋、本地快取、手動對時 |
| `scripts/karaoke_player.py` | 卡拉 OK 播放器（逐字高亮/速度控制/段落反覆）|
| `scripts/lyrics_creator.py` | 填詞創作（韻腳表/段落模板/BPM計算）|
| `scripts/lyrics_translator.py` | 翻譯對照（中/英/日/片假名）|

---

## 環境要求

- 標準 Python 3，無需額外依賴
- macOS Music.app（Lyrics 同步用）
- 網路（歌詞搜尋 / 翻譯）

---

## 網路與第三方服務說明

| 服務 | 用途 | 資料傳輸 |
|------|------|----------|
| [LRCLIB](https://lrclib.net) | 歌詞搜尋與取得 | 歌名/歌手/時長 → 回傳歌詞 |
| [LibreTranslate](https://libretranslate.com) | 歌詞中英日翻譯 | 歌詞文字 → 回譯譯文（不上傳使用者個資）|
| DuckDuckGo HTML | 歌詞找不到時備援搜尋 | 搜尋關鍵字 → 回傳標題摘要 |

**安全限制：** `get` 命令僅接受 LRCLIB 數字 ID，不支援任意 URL。
本地快取存放於 `~/.karaoke-companion/cache/`。

---

## 使用方式

```bash
# ── 搜歌 + 練唱 ───────────────────────────────────────
# 搜尋歌詞
python3 scripts/lyrics_searcher.py search "光年之外"

# 取得歌詞（用 LRCLIB 歌曲 ID）
python3 scripts/lyrics_searcher.py get 123456

# 卡拉 OK 播放（需先播放音樂或指定歌詞）
python3 scripts/karaoke_player.py play -t "你就是我的星光..." --speed 0.75

# 練歌模式：逐句跟唱
python3 scripts/karaoke_player.py practice -t "你就是我的星光..." --speed 0.5

# ── 填詞創作 ──────────────────────────────────────────
# 韻腳總表
python3 scripts/lyrics_creator.py guide

# 生成完整歌曲模板
python3 scripts/lyrics_creator.py song "我的天空" --genre 流行 --bpm 120

# 生成副歌段落
python3 scripts/lyrics_creator.py verse -t chorus_4line -m love

# 查某字押韻
python3 scripts/lyrics_creator.py rhyme "光"

# 字數計算
python3 scripts/lyrics_creator.py count "你就是我的星光"

# ── 翻譯對照 ─────────────────────────────────────────
# 對照顯示（自動翻譯）
python3 scripts/lyrics_translator.py compare -t "I love you more than words can say"

# Live 對照模式
python3 scripts/lyrics_translator.py live -t "Dreaming under the moonlight"
```
