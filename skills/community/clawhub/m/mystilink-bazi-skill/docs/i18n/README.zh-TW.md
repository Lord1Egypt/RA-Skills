# Mystilink 八字 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

八字 Agent Skill：透過內嵌腳本根據出生資料計算四柱、大運、流年，再結合理論詞條（日主、十神等）進行解讀。排盤演算法位於 `scripts/`。

## 交付類型

本倉庫為 **Agent Skill** 包（`SKILL.md` + `scripts/` + `references/` + `examples/`）。**不適用**計算器庫的 C / C++ / C# / Java / JavaScript / Python 語言矩陣。多語言 SDK/CLI 見同系列 `mystilink-bazi-calculator`（可選，執行本 skill 非必需）。

## 環境需求

- Python 3.9+（`zoneinfo`）
- 相容 Agent Skills 的宿主
- 解讀時可選存取 Mystilink Wiki API（需網路）

## 安裝

安裝目錄名須為 `mystilink-bazi`（與 `SKILL.md` 的 `name` 一致）：

| 宿主 | 路徑 |
|------|------|
| Cursor | `.cursor/skills/mystilink-bazi/` |
| Claude Code | `.claude/skills/mystilink-bazi/` |

```bash
cp -R mystilink-bazi-skill /path/to/.cursor/skills/mystilink-bazi
```

## 快速開始（腳本）

在 skill 目錄下：

```bash
python3 scripts/bazi_calculate.py --date 1990-05-15 --hour 12
python3 scripts/bazi_calculate.py --birth-json examples/profile.v0.json
python3 scripts/bazi_calculate.py --profile-json examples/profile.json
python3 scripts/bazi_dayun_calculate.py --date 1990-05-15 --gender female --count 8
python3 scripts/bazi_liunian_calculate.py --year 2026 --day-stem 甲
```

成功：stdout 輸出 JSON。失敗：非零結束代碼，並輸出 `{"error":…}`。

柱物件含 `stem_index`、`branch_index`、`text`，並保留舊欄位 `ganzhi`（與 `text` 相同）。

## 工作流

1. 採集出生資料——任選其一：
   - `examples/profile.v0.json`（`mystilink.birth/0.1` BirthProfile），或
   - `examples/profile.json`（舊版 skill 欄位）
2. 按需執行排盤腳本（`--birth-json` / `--profile-json` 兩種形狀均可）
3. 可選 Wiki 解讀：

```text
GET https://wiki.mystilink.com/api/v1/search?q=day+master&system=bazi&locale=en
GET https://wiki.mystilink.com/api/v1/pages/bazi.concept.ri-zhu?locale=en
```

4. 區分 **盤面事實** 與 **解釋**；使用 Wiki 時註明出處

完整說明見 `SKILL.md`。常用頁面 id 見 `references/wiki-ids.md`。

## 範例

- `examples/profile.v0.json` — BirthProfile（`mystilink.birth/0.1`，虛構）
- `examples/profile.json` — 舊版出生資料（虛構）；腳本仍接受

## 限制

- 腳本為獨立安裝用的內嵌副本，不是多語言 SDK
- 大運節氣日為公曆近似
- 真太陽時需同時提供時區與經度
- Wiki：省略 locale → `en`；缺譯可能回落 `zh-Hans`

## 授權

MIT。見 [LICENSE](../../LICENSE)。

## 問題回饋

請附帶完整腳本命令（僅用虛構日期）及 stdout/stderr JSON。
