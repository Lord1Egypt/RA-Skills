# Mystilink タロット Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概要

タロット向け Agent Skill：内嵌 Node スクリプトでスプレッドに正位置／逆位置のカードを引き、牌意ページで解釈します。実抽選（スクリプトまたはユーザー提供）を優先し、黙って抽選結果を捏造しないでください。

## 配布形態

**Agent Skill** パッケージ。計算機の言語マトリクスは **適用しません**。抽選／検証ロジックは `scripts/` のみに内嵌（独立したタロット計算機リポジトリなし）。

## 要件

- Node.js 18+
- Agent Skills 互換ホスト
- Wiki API は任意（ネットワーク）

## インストール

フォルダ名は `mystilink-tarot` 必須：

```bash
cp -R mystilink-tarot-skill /path/to/.cursor/skills/mystilink-tarot
```

| ホスト | パス |
|------|------|
| Cursor | `.cursor/skills/mystilink-tarot/` |
| Claude Code | `.claude/skills/mystilink-tarot/` |

## クイックスタート

```bash
node scripts/draw.mjs --spread three-card --seed 42
# or: echo '{"spread":"three-card","seed":42}' | node scripts/draw.mjs
```

stdout JSON：`id`、`name`、`orientation`（`upright`|`reversed`）、位置を含むカード。カード `id` は Wiki `tarot.card.*` と整合。

## ワークフロー

1. 質問とスプレッドを明確化（既定：three-card）；`examples/draw-request.json` を参照
2. スクリプトで抽選するか、ユーザー提供カードを受理
3. 各カードで任意 Wiki：

```text
GET https://wiki.mystilink.com/api/v1/search?q=The+Fool&system=tarot&locale=en
GET https://wiki.mystilink.com/api/v1/pages/<card.id>?locale=en
```

4. 各位置を質問に結び、Wiki 使用時は出典を明示

詳細：`SKILL.md`。抽選方法：`references/method-draw.md`。

## 例

- `examples/draw-request.json` — 抽選リクエスト例

## 制限

- 医療・法的確定性を主張しない
- 1 抽選につき明確な質問を 1 つ優先
- Wiki locale 省略 → `en`

## ライセンス

MIT。[LICENSE](../../LICENSE) を参照。

## フィードバック

スプレッド flags/seed（または stdin JSON）と stdout JSON（架空の質問のみ）を含めてください。
