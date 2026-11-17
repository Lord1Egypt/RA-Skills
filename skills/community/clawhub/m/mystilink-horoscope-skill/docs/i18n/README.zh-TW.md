# Mystilink 占星 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

西洋本命盤 Agent Skill：用內嵌腳本根據出生時間與地點計算行星、宮位與相位，再結合理論詞條解讀。

## 交付類型

**Agent Skill** 包。**不適用**計算器語言矩陣。可選同系列：`mystilink-horoscope-calculator`。

## 環境需求

- Python 3.9+
- `pip install pyswisseph`
- 相容 Agent Skills 的宿主
- Wiki API 可選（需網路）

## 安裝

目錄名須為 `mystilink-horoscope`：

```bash
cp -R mystilink-horoscope-skill /path/to/.cursor/skills/mystilink-horoscope
```

| 宿主 | 路徑 |
|------|------|
| Cursor | `.cursor/skills/mystilink-horoscope/` |
| Claude Code | `.claude/skills/mystilink-horoscope/` |

## 快速開始

```bash
python3 scripts/astro_chart_calculate.py \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --lat 31.23 --lon 121.47 \
  --output json

python3 scripts/astro_chart_calculate.py \
  --birth-json examples/profile.v0.json \
  --output json
```

可選：`--zodiac tropical|sidereal`、`--true-solar-time`。

成功：stdout JSON。失敗：非零結束 + JSON error。

## 工作流

1. 採集出生資料——`examples/profile.v0.json`（BirthProfile）或舊版 `examples/profile.json`
2. 執行本命盤腳本
3. 可選 Wiki：

```text
GET https://wiki.mystilink.com/api/v1/search?q=ascendant&system=horoscope&locale=en
GET https://wiki.mystilink.com/api/v1/pages/horoscope.concept.natal-chart?locale=en
```

4. 區分盤面資料與解釋

詳見 `SKILL.md`。短指引見 `references/overview.md`。

## 範例

- `examples/profile.v0.json` — BirthProfile（`mystilink.birth/0.1`，虛構）
- `examples/profile.json` — 舊版虛構本命輸入

## 限制

- 依賴 `pyswisseph`（Swiss Ephemeris）
- 內嵌腳本供 skill 獨立使用，非多語言 SDK
- Wiki 省略 locale → `en`；缺譯可能回落 `zh-Hans`

## 授權

MIT。見 [LICENSE](../../LICENSE)。

## 問題回饋

請附帶完整命令（虛構座標/時間）與 JSON 輸出或錯誤。
