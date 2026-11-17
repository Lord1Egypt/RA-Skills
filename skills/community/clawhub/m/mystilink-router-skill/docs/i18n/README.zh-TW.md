# Mystilink 路由 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

Agent Skill：在使用者未指定體系、詢問該用哪種方法、或一次請求混用多種傳統時，選擇一個 Mystilink 命理/占卜 skill（八字、紫微、塔羅、六爻或西洋占星）。本 skill 不負責排盤或抽牌計算。

## 交付類型

本倉庫為 **Agent Skill** 包（`SKILL.md` + references + examples）。**不適用**計算器庫所要求的 C / C++ / C# / Java / JavaScript / Python 語言矩陣。

## 環境需求

- 相容 Agent Skills 規範的宿主（Cursor、Claude Code、OpenClaw、Hermes 等）
- 路由完成後若要繼續執行，需已安裝對應體系的 skill

## 安裝

將本倉庫複製到宿主 skills 目錄，目錄名使用 `mystilink-router`（須與 `SKILL.md` 中的 `name` 一致）：

| 宿主 | 路徑 |
|------|------|
| Cursor | `.cursor/skills/mystilink-router/` 或 `~/.cursor/skills/mystilink-router/` |
| Claude Code | `.claude/skills/mystilink-router/` 或 `~/.claude/skills/mystilink-router/` |

```bash
cp -R mystilink-router-skill /path/to/.cursor/skills/mystilink-router
```

## 用法

按 `SKILL.md` 執行。路由啟發式：

| 需求 | Skill |
|------|--------|
| 生辰 → 長期結構、十神 | `mystilink-bazi` |
| 生辰 → 十二宮 / 紫微星曜 | `mystilink-ziwei` |
| 生辰地點 + 時間 → 行星/宮位/相位 | `mystilink-horoscope` |
| 一事一問、牌象 | `mystilink-tarot` |
| 一事一問、卦爻 | `mystilink-liuyao` |

可選 Wiki（需網路）：

```text
GET https://wiki.mystilink.com/api/v1/pages/shared.concept.choosing-a-system?locale=en
```

選定後載入目標 skill 的 `SKILL.md` 並繼續。優先每次請求只選一個主體系。

## 範例

見 `examples/routing-cases.md`（示例意圖與期望目標）。

## 限制

- 本 skill 不含計算腳本
- 不「五個體系一起跑」
- Wiki 呼叫可選；省略 `locale`/`lang` → `en`；缺譯可能回落 `zh-Hans`

## 授權

MIT。見 [LICENSE](../../LICENSE)。

## 問題回饋

回饋時請附帶使用者意圖原文（僅用虛構內容）以及選中或漏選的 skill 名稱。
