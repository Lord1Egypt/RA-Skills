# Mystilink 六爻 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概述

六爻 Agent Skill：用內嵌 Node 腳本完成六次起卦並形成卦象，再結合方法頁與 Wiki 中的周易篇章解讀。一事一卦。禁止編造經文。

## 交付類型

**Agent Skill** 包。**不適用**計算器語言矩陣。起卦邏輯僅內嵌於 `scripts/`（無獨立六爻計算器倉庫）。

## 環境需求

- Node.js 18+
- 相容 Agent Skills 的宿主
- 建議可存取 Wiki（方法頁與經典）

## 安裝

目錄名須為 `mystilink-liuyao`：

```bash
cp -R mystilink-liuyao-skill /path/to/.cursor/skills/mystilink-liuyao
```

| 宿主 | 路徑 |
|------|------|
| Cursor | `.cursor/skills/mystilink-liuyao/` |
| Claude Code | `.claude/skills/mystilink-liuyao/` |

## 快速開始

```bash
node scripts/cast.mjs --seed 42
# or fixed throws: node scripts/cast.mjs --throws "3,2,3,3,2,3"
```

stdout JSON：六爻（自下而上）、動爻標記、可用時的卦鍵。錢幣模型見腳本說明（字=3、背=2 求和）。

## 工作流

1. 明確一事（`examples/cast-request.json`）；拒絕多主題濫卦
2. 用腳本起卦或接受使用者投擲結果
3. 透過 Wiki 解讀，例如：

```text
GET https://wiki.mystilink.com/api/v1/pages/liuyao.method.six-casts?locale=en
GET https://wiki.mystilink.com/api/v1/pages/liuyao.rule.ben-zhi-bian?locale=en
GET https://wiki.mystilink.com/api/v1/pages/shared.work.yijing.gua.01-qian?locale=zh-Hans
```

4. 周易原文優先走 Wiki 引用 / cites

詳見 `SKILL.md`。短指引見 `references/overview.md`。

## 範例

- `examples/cast-request.json` — 起卦請求樣例

## 限制

- 經典文本在其它語言缺譯時常見回落 `zh-Hans`
- 內嵌起卦助手為產品錢幣→爻語義的簡化實作
- Wiki 省略 locale → `en`

## 授權

MIT。見 [LICENSE](../../LICENSE)。

## 問題回饋

請附帶 seed/throws 與 stdout JSON（僅用虛構事項）。
