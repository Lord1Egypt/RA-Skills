# Mystilink 塔羅 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

塔羅 Agent Skill：用內嵌 Node 腳本按牌陣抽取正/逆位牌，再結合牌意詞條解讀。優先真實抽牌（腳本或使用者已抽結果），禁止靜默編造抽牌結果。

## 交付類型

**Agent Skill** 包。**不適用**計算器語言矩陣。抽牌邏輯僅內嵌於 `scripts/`（無獨立塔羅計算器倉庫）。

## 環境需求

- Node.js 18+
- 相容 Agent Skills 的宿主
- Wiki API 可選（需網路）

## 安裝

目錄名須為 `mystilink-tarot`：

```bash
cp -R mystilink-tarot-skill /path/to/.cursor/skills/mystilink-tarot
```

| 宿主 | 路徑 |
|------|------|
| Cursor | `.cursor/skills/mystilink-tarot/` |
| Claude Code | `.claude/skills/mystilink-tarot/` |

## 快速開始

```bash
node scripts/draw.mjs --spread three-card --seed 42
# or: echo '{"spread":"three-card","seed":42}' | node scripts/draw.mjs
```

stdout JSON：含 `id`、`name`、`orientation`（`upright`|`reversed`）、位置。牌 `id` 對應 Wiki `tarot.card.*`。

## 工作流

1. 明確問題與牌陣（預設三牌）；見 `examples/draw-request.json`
2. 用腳本抽牌或接受使用者已抽結果
3. 對每張牌可選 Wiki：

```text
GET https://wiki.mystilink.com/api/v1/search?q=The+Fool&system=tarot&locale=en
GET https://wiki.mystilink.com/api/v1/pages/<card.id>?locale=en
```

4. 將各位置與問題對應；使用 Wiki 時註明出處

詳見 `SKILL.md`。抽牌說明見 `references/method-draw.md`。

## 範例

- `examples/draw-request.json` — 抽牌請求樣例

## 限制

- 不宣稱醫療或法律確定性
- 盡量一事一抽
- Wiki 省略 locale → `en`

## 授權

MIT。見 [LICENSE](../../LICENSE)。

## 問題回饋

請附帶牌陣參數/seed（或 stdin JSON）與 stdout JSON（僅用虛構問題）。
