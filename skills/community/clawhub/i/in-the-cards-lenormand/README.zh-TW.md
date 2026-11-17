# 牌間 · In the Cards

**Lenormand Interpreter · 雷諾曼解牌**

> [English](README.md) · [简体中文](README.zh-CN.md)

遵循 [Agent Skills](https://agentskills.io) 開放標準的 Lenormand 雷諾曼解讀 skill。它讀出牌與牌之間的意義，將每次解讀儲存為結構化資料，並生成 A4 PDF、獨立網頁、社群卡片或長圖。既支援自由輸入牌陣，也相容 [Stargazer’s Oracle（觀星者神諭）](https://lenor.star-oracle.app/) 提示詞，不綁定單一平台。

```
請幫我安裝這個 skill：https://github.com/locoda/in-the-cards-lenormand-skill
```

## 設計

所有產品共享統一視覺語言，靈感來自兩個源頭：

- **[Kami](https://github.com/tw93/Kami)** — 暖羊皮紙底色 (#f5f4ed)、墨藍強調色 (#1B365D)、昭源宋體排版。乾淨、文雅、留白從容。
- **幾何沉默 (Geometric Silence)** — 一套 36 張原創 Lenormand 牌組，建築藍圖風格。灰鼠尾草綠 (#7A8B7A) 線條繪製於米白底色 (#F5F0E8) 之上，塵玫瑰色 (#C4A0A0) 點綴。瑞士國際主義風格遇上了科研標本圖版。無任何神祕紋飾——純粹幾何抽象。

二者共同營造出學術、溫暖、安靜優雅的閱讀體驗。

## 功能特色

- **6 種牌陣**：1 張是非題 · 2 張對牌 · 3 張線性 · 5 張線性 · 9 張九宮格（3×3）· 二選一
- **雙語自動辨識**：中英文提示詞自動偵測，輸出語言與輸入一致
- **組合優先解讀**：系統性組合方法論——相鄰牌對鏈式解讀，修飾詞類型系統（名詞+修飾詞模型）。每張牌按修飾類型影響相鄰牌；8 張負面修飾牌自動壓低 tone。中立誠實，不做空洞安慰
- **一次解讀，四種產出**：A4 PDF（預設）· 獨立網頁 · 1080×1440 社群卡輪播 · 全頁 PNG 長圖
- **解讀持久化**：結構化 JSON + 人類可讀 Markdown 雙存，隨時再生為任意產品型態
- **種子 HTML**：複製即用，不再從零建構 HTML
- **幾何沉默牌組 (Geometric Silence)**：36 張原創 SVG 牌面，建築藍圖風格
- **昭源字體系列**：Chiron Sung HK（昭源宋體）正文 + Chiron Hei HK（昭源黑體）標籤，透過 Google Fonts CDN 載入，國內自動切換鏡像

## 預覽

產品展示：[牌間 / In the Cards](https://skills.1mether.me/in-the-cards/)

## 安裝

對你的 AI 助理說：

> 幫我從 GitHub 安裝「牌間」Lenormand skill：https://github.com/locoda/in-the-cards-lenormand-skill

或手動複製到你的 agent 技能目錄：

```bash
git clone https://github.com/locoda/in-the-cards-lenormand-skill.git ~/your-agent/skills/in-the-cards-lenormand/
```

需要 Node.js + Puppeteer（首次生成 PDF 或社群卡片時自動安裝 Chromium）。

已有安裝可繼續保留舊目錄名 `stargazer-interpreter`；新安裝使用 `in-the-cards-lenormand`。

## 使用方式

### 首次解讀

貼上 Lenormand 牌陣或相容的 Stargazer 提示詞 — agent 自動執行 Phase 1（解析）+ Phase 2（解讀+儲存），預設生成 A4 PDF。

```
使用者: 幫我解讀這個牌陣

你是一位傳統 Lenormand 占卜師。請為我解讀今天的每日運勢。
【日期】2026/06/20
【牌陣】每日運勢 3 張（由左至右連讀）
1. 幸運草 (Clover)
2. 小孩 (Child)
3. 蛇 (Snake)
```

### 從已儲存的解讀生成不同產品

```
使用者: 把上次的解讀生成社群卡片
使用者: 用 #2 解讀生成網頁版
```

### 一次生成多個產品

```
使用者: 幫我解讀這個牌陣，生成 PDF 和社群卡片
[Lenormand 牌陣或 Stargazer 提示詞...]
```

### 三階段架構

```
Lenormand 提示詞
（相容 Stargazer 格式）
    │
    ▼
[Phase 1] 解析 → 結構化牌面資料
    │
    ▼
[Phase 2] 解讀 → 儲存 (JSON + MD)
    │
    ▼
[Phase 3] 從儲存的解讀生成產品
           ├── A4 PDF（預設）
           ├── 獨立網頁
           ├── 社群卡片（1080×1440 輪播）
           └── 全頁 PNG 長圖
```

## 目錄結構

```
├── SKILL.md                         # 主技能指令
├── README.md                        # 英文文檔
├── README.zh-CN.md                  # 簡體中文文檔
├── README.zh-TW.md                  # 繁體中文文檔
├── assets/
│   ├── seed-a4-pdf.html             # A4 PDF HTML 骨架
│   ├── seed-social-card.html        # 1080×1440 社群卡片骨架
│   └── seed-web-page.html           # 網頁版骨架
├── cards/
│   └── card-01-rider.svg ...        # 36 張 Geometric Silence SVG
├── references/
│   ├── lenormand-cards.md           # 36 張牌資料庫 (MIT)、修飾類型、組合方法論
│   ├── spread-parsing.md            # 提示詞解析規則
│   ├── design-system.md             # 共享字體／顏色／牌名表
│   ├── reading-schema.md            # 解讀 JSON 結構
│   └── template-a4-pdf.md           # A4 PDF 章節與分頁平衡規則
└── scripts/
    ├── generate-pdf.js              # HTML → A4 PDF (Puppeteer)
    ├── render-social-cards.js       # HTML → 1080×1440 PNG (Puppeteer)
    ├── render-long-image.js         # HTML → 全頁 PNG 長圖 (Puppeteer)
    ├── validate.js                  # 產物驗證（靜態 + Puppeteer）
    └── manage-readings.js           # 解讀索引 CLI
```

> **網站與預覽** 維護在獨立的 [`locoda/skill-showcase`](https://github.com/locoda/skill-showcase) 倉庫：[牌間 / In the Cards](https://skills.1mether.me/in-the-cards/)。

## 授權條款

MIT

## 致謝與參考

**字體**
- [昭源宋體 (Chiron Sung HK)](https://github.com/chiron-fonts/chiron-sung-hk) — 可變宋體，SIL OFL 1.1
- [昭源黑體 (Chiron Hei HK)](https://github.com/chiron-fonts/chiron-hei-hk) — 可變黑體，SIL OFL 1.1

**設計**
- [Kami](https://github.com/tw93/Kami) — 視覺風格啟發，MIT
- 幾何沉默 (Geometric Silence) — 原創牌組設計

**資料**
- [Stargazer’s Oracle（觀星者神諭）](https://lenor.star-oracle.app/)
- [lenormand-oracle](https://github.com/jintianbaihe/lenormand-oracle) — 36 張牌雙語資料集，MIT
- 組合修飾系統 — 基於公有領域雷諾曼傳統的原創 synthesis