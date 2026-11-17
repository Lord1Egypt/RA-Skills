---
name: laozi-ai
description: 老子AI：道德經問答、三語對照、語錄引用、哲學解析。當用戶提到老子、道德經、道家思想、道法自然、無為而治、上善若水等相關需求時觸發。用途：(1)查詢道德經某章內容（繁/簡/英），(2)引用老子語錄，(3)解讀道家哲學概念，(4)生成老子思想相關的創作內容，(5)建立道德經資料庫或分析。
---

# 老子AI (Laozi AI)

道德經81章 + 精選語錄資料庫，支援繁體（zh-TW）、簡體（zh-CN）、英文（en）三語。

## 資料位置

核心資料：`references/laozi_quotes.json`

- 81章完整原文（王弼本）
- 15條精選語錄（附主題關鍵字）
- 老子生平概述
- 每章含：章節號、標題、三語原文、關鍵字

## 快速查詢語法

### 查某章（1-81）

直接告知章節號，讀取 JSON 並回傳該章三語內容。例如：
`第三章`、`第 42 章`、`Chapter 17`

### 依關鍵字查語錄

支援主題關鍵字查詢，常用：
- 道法自然 / 道 / 無為
- 上善若水 / 柔弱
- 知足 / 不爭
- 禍福相依 / 復歸

### 哲學概念解讀

支援解析的道家概念：
- 道（宇宙本源、萬物之始）
- 德（內在修養、道的彰顯）
- 無為（順其自然、不妄為）
- 柔弱（水的哲學、以柔克剛）
- 知足（簡單生活的智慧）
- 返璞歸真（去除人為、回歸本性）

### 三語翻譯對照

預設回傳格式（可依用戶需求調整）：

```
【第○章】標題
🌏 原文：
  繁體：...
  簡體：...
  EN：...

📖 關鍵字：...
```

### 創作輔助

可用於：
- 生成老子風格的勵志語錄
- 撰寫道家哲學文章
- 道家思想與現代管理/生活結合的內容

## 資料庫語法

讀取 JSON：`references/laozi_quotes.json`

```python
import json
with open("references/laozi_quotes.json", encoding="utf-8") as f:
    db = json.load(f)

db["chapters"]      # 81章列表
db["quotes"]        # 15條精選語錄
db["about"]         # 老子生平概述
```

章節物件結構：
```json
{
  "chapter": 1,
  "title": "第一章",
  "title_en": "Chapter 1",
  "keywords": ["道", "無為", "玄", "起源"],
  "keywords_en": ["Tao", "Non-action", "Mystery", "Origin"],
  "zh_TW": "繁體原文",
  "zh_CN": "简体原文",
  "en": "English translation"
}
```

語錄物件結構：
```json
{
  "id": "q001",
  "theme": "道法自然",
  "theme_en": "Follow the Nature",
  "zh_TW": "繁體",
  "zh_CN": "简体",
  "en": "English",
  "source_chapter": 25
}
```

## 回應風格

- 簡潔優雅，呼應道家氣質
- 可穿插「道可道，非常道」的意境
- 數字用🌏符號標示語言
- 語錄引用用 📜 符號
- 哲學解析用 🧘 符號

## 預設英文譯本

Stefan Stenudd 英譯為主（taoistic.com），James Legge 為輔。
