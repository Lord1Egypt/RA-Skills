# Mystilink 六爻 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概要

六爻向け Agent Skill：内嵌 Node スクリプトで六回の起卦から卦象を形成し、方法ページと Wiki の周易章で解釈します。一事一卦。経文を捏造しないでください。

## 配布形態

**Agent Skill** パッケージ。計算機の言語マトリクスは **適用しません**。起卦ロジックは `scripts/` のみに内嵌（独立した六爻計算機リポジトリなし）。

## 要件

- Node.js 18+
- Agent Skills 互換ホスト
- 方法ページと古典のため Wiki へのアクセスを推奨

## インストール

フォルダ名は `mystilink-liuyao` 必須：

```bash
cp -R mystilink-liuyao-skill /path/to/.cursor/skills/mystilink-liuyao
```

| ホスト | パス |
|------|------|
| Cursor | `.cursor/skills/mystilink-liuyao/` |
| Claude Code | `.claude/skills/mystilink-liuyao/` |

## クイックスタート

```bash
node scripts/cast.mjs --seed 42
# or fixed throws: node scripts/cast.mjs --throws "3,2,3,3,2,3"
```

stdout JSON：六爻（下→上）、動爻フラグ、利用可能な卦キー。銭貨モデルはスクリプトヘルプに従う（表=3、裏=2 の合計）。

## ワークフロー

1. 一事を明確化（`examples/cast-request.json`）；多テーマ乱卦は拒否
2. スクリプトで起卦するか、ユーザーの投擲を受理
3. Wiki で読む、例：

```text
GET https://wiki.mystilink.com/api/v1/pages/liuyao.method.six-casts?locale=en
GET https://wiki.mystilink.com/api/v1/pages/liuyao.rule.ben-zhi-bian?locale=en
GET https://wiki.mystilink.com/api/v1/pages/shared.work.yijing.gua.01-qian?locale=zh-Hans
```

4. 周易文は Wiki の references / cites を優先

詳細：`SKILL.md`。案内：`references/overview.md`。

## 例

- `examples/cast-request.json` — 起卦リクエスト例

## 制限

- 古典は他ロケールに本文がない場合、しばしば `zh-Hans` にフォールバック
- 内嵌起卦ヘルパーは製品の銭貨→爻意味の簡略実装
- Wiki locale 省略 → `en`

## ライセンス

MIT。[LICENSE](../../LICENSE) を参照。

## フィードバック

seed/throws と stdout JSON（架空の事案のみ）を含めてください。
