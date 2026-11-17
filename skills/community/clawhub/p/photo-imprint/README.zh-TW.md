# Photo Imprint (印痕)

> 留住那張照片，只換一種筆觸去記。

[English](README.md) | [简体中文](README.zh-CN.md)

你從日本回來，手機裡一堆杯子、機艙、六本木街頭的照片，想整理成一套手帳輪播發小紅書或 IG。直接丟給模型，漂亮但小杯變大杯，還幫你加個東京鐵塔，你的那張不見了。

`locoda/photo-imprint-skill` · 英文 skill，中文名印痕

```
請幫我安裝這個 skill：https://github.com/locoda/photo-imprint-skill
```

![license MIT](https://img.shields.io/badge/license-MIT-green) ![version 1.6.0](https://img.shields.io/badge/version-1.6.0-blue) ![tests 34 gates](https://img.shields.io/badge/tests-34%20gates-lightgrey)

| 印痕（下方置中，上方 caption 範例） | 原片已模糊，保護隱私 |
|---|---|
| ![印痕01](assets/samples/01-sjc-small-cup-paper-locked-v11.webp) | ![原片01](assets/samples/source-01.webp) |
| 小杯保持小，蓋子鎖死，50%紙白，下方置中 | SJC 小杯（12px模糊） |
| ![印痕02](assets/samples/02-in-flight-paper-locked-v11.webp) | ![原片02](assets/samples/source-02.webp) |
| 機艙簡化成冷色塊，不編天空 | 飛機上（已模糊） |
| ![印痕03](assets/samples/03-roppongi-paper-locked-v11.webp) | ![原片03](assets/samples/source-03.webp) |
| 背景強簡化，不編東京鐵塔 | 六本木街頭（已模糊） |

範例 webp <100KB 在 `assets/samples/`，終版 1152×2048 jpg ~400KB，無 EXIF。

## 一堆旅行照終於像一本手帳的時候

**你：** 有10張日本的照片，想做成一套水彩手帳輪播，但原片太雜，不想露臉，也不想讓模型亂加地標。試過一個 prompt 套全部，第2張小杯就變大杯。

**印痕：** 把輪廓、比例、蓋子、logo 位置全部鎖住。丟8張真實風格縮圖給你選，選一種後只算第1頁，把 `production-plan.md` + 6欄位 style contract + 範例一起給你看，等你原話批准才批次 2..N。

**現在你可以：** 用第1張判斷整套，小杯保持小，4張全是暖紙 #F1EBDD、55%頂部留白、下方置中，沒有編造的地點/日期，拿到的 ZIP 已雙維 QA。

## 怎麼跟 AI 說

你不用跑腳本，AI 跑。

**裝一次：**
```
請幫我安裝這個 skill：https://github.com/locoda/photo-imprint-skill
```

**開一套：**
> 我有10張日本照片在 /path/to/photos，幫我做成水彩手帳，小杯保持小，下方置中，上面55%留白，不要字。

**選風格：**
> 用 sumi-e-ink / 你定 / 用預設水彩

**批准：**
> 批准第1張，繼續

**改一頁：**
> 第2張背景太滿，簡化一下

**換風格（會退回風格門，符合預期）：**
> 換成廣重去雨版

小技巧：小杯保持小是預設鎖死的。caption 只認 EXIF，不想要就說「不要字」。私人參考圖只存本地，除非你說「可以上傳到 X」。

## 怎麼做到的

### 鎖住該留的，只在筆觸上抽象

原片是權威。Template A/B 現在都走下方置中：主體 y=0.72 置中，1152×2048，暖紙，50%空白保底。shape-lock 鎖杯/瓶輪廓、高度、蓋子、logo，抽象只在筆觸和貼邊2-3處 ≤10%寬度溶色，顏色從主圖取。不帶手/布/相框。

### 單選風格，凍住合約，不混搭

已打包8個：`watercolor-journal`（預設，下方置中）、`blue-lavender-watercolor`、`highway-485-lithograph`、`sumi-e-ink`（芝田浙信1847 疏朗墨線）、`hiroshige-bokashi`（廣重1833去雨 平塗+bokashi）、`seurat-conte`（秀拉1882 無硬輪廓 Conté排線）。選一種寫進 `work/style_choice.json`，凍進 `work/sample_style_contract.json`，批次時 hash-lock。要求混搭會拒絕。

### 先 plan+範例，再批次，你說了算

不是 prompt 合集，是帶門禁的生產流：EXIF 排序 → 每頁 `production_brief` → `production-plan.md` → 只算第1頁 → 討論 → 明確批准 → 批次 2..N 用凍結合約 → 洗版 → 確定性合成 → 雙維 QA → 已驗證 ZIP。你跟 AI 說人話就行：

> 我有10張日本照片在 /path/to/photos，幫我做成水彩手帳，小杯保持小，下方置中，上面55%留白，不要字。

AI 按 EXIF 排序，缺 EXIF 會問是否授權 draft，丟8張風格，你說「你定」就用預設，算範例，等你說「批准第1張，繼續」。改圖說「第2張背景太滿」只重算第2張。私人參考圖只存本地，除非你說「可以上傳到 X」。

<details>
<summary>給 AI 的實作（人不用看）</summary>

6層：Config → Plan → Gate → Render → QA → Package。Invariants：EXIF不可變、範例僅第1張、範例不作參考、每張 plate 有 receipt、無 EXIF/GPS/XMP、不編造。

預設 9:16 1152×2048、紙 #F1EBDD 50%留白、預設 watercolor-journal、EXIF升冪、QA 全尺寸+360×640。

工作流：`check_environment.py` → `resolve_config.py` + `preprocess.py` → `build_render_plan.py` + `build_production_plan.py` + `build_render_plan.py + build_production_plan.py (sample scope)` → 風格門 → 範例 → `review_gate.py approve` + `compose.py batch` → 批次合成 → QA → revision → `package_verified.py`

驗證：`python3 bin/validate_skill.py --json`

</details>

## 參考

- 行為和邊界：`SKILL.md`、`references/configuration.md`、`references/review-gate.md`、`references/quality-checks.md`
- 回歸和邊界用例：`tests/`（34個門禁/回歸）、`references/test-cases.md`、`bin/validate_skill.py`
- 儲存和封存：`work/resolved-config.json`（SHA256）、`work/manifest.json`（EXIF排序）、`work/style_choice.json`、`work/composition-manifest.json`、`work/verify-report.json`
- 未使用需額外授權的字型或圖片，風格包為 Smithsonian 公開域 `assets/style-packs/`，範例 webp <100KB，原片 12px 模糊保護隱私，終版無 EXIF/GPS/XMP，不含受版權保護原文

## License

MIT License — Copyright (c) 2026 locoda。程式碼與文件 MIT，風格包遵循各自 Smithsonian 公開域條款，範例同倉庫授權，原片已模糊處理。

---
Made by [1mether](https://1mether.me).

*留住那張照片，只換一種筆觸去記。*
