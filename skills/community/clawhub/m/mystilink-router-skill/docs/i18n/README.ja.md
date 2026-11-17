# Mystilink Router Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概要

ユーザーが体系を指定していない場合、どの方法が適しているかを尋ねた場合、または複数の伝統を混在させた場合に、Mystilink の命理／占術 skill（八字、紫微、タロット、六爻、西洋占星）のうち 1 つを選ぶ Agent Skill です。盤計算や抽選は行いません。

## 配布形態

本リポジトリは **Agent Skill** パッケージ（`SKILL.md` + references + examples）です。計算機ライブラリで用いる C / C++ / C# / Java / JavaScript / Python の言語マトリクスは **適用しません**。

## 要件

- Agent Skills 互換ホスト（Cursor、Claude Code、OpenClaw、Hermes など）
- ルーティング後に引き継ぐ場合は、対象の理論 skill がインストール済みであること

## インストール

本リポジトリをホストの skills ディレクトリへ `mystilink-router` として複製します（フォルダ名は `SKILL.md` の `name` と一致必須）：

| ホスト | パス |
|------|------|
| Cursor | `.cursor/skills/mystilink-router/` または `~/.cursor/skills/mystilink-router/` |
| Claude Code | `.claude/skills/mystilink-router/` または `~/.claude/skills/mystilink-router/` |

```bash
cp -R mystilink-router-skill /path/to/.cursor/skills/mystilink-router
```

## 使い方

`SKILL.md` に従います。ルーティングの目安：

| 必要 | Skill |
|------|--------|
| 生年月日時 → 長期構造・十神 | `mystilink-bazi` |
| 生 → 十二宮 / 紫微星曜 | `mystilink-ziwei` |
| 出生地 + 時刻 → 惑星／ハウス／アスペクト | `mystilink-horoscope` |
| 具体的な一問・象徴カード | `mystilink-tarot` |
| 具体的な一問・卦／動爻 | `mystilink-liuyao` |

任意の Wiki 補助（ネットワーク）：

```text
GET https://wiki.mystilink.com/api/v1/pages/shared.concept.choosing-a-system?locale=en
```

選択後、その skill の `SKILL.md` を読み込み続行します。1 リクエストにつき主体系は 1 つを優先します。

## 例

サンプル意図と期待ターゲットは `examples/routing-cases.md` を参照。

## 制限

- 本 skill に計算スクリプトはない
- 「念のため複数体系を同時実行」しない
- Wiki 呼び出しは任意；`locale`/`lang` 省略 → `en`；欠訳時は `zh-Hans` にフォールバックする場合あり

## ライセンス

MIT。[LICENSE](../../LICENSE) を参照。

## フィードバック

ユーザー意図文（架空のみ）と、選択または取りこぼした skill 名を添えて報告してください。
