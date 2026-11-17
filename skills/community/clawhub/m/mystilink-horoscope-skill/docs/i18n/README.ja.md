# Mystilink 西洋占星 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概要

西洋出生図向け Agent Skill：内嵌スクリプトで出生時刻と場所から惑星・ハウス・アスペクトを計算し、理論ページで解釈します。

## 配布形態

**Agent Skill** パッケージ。計算機の言語マトリクスは **適用しません**。任意の同系列：`mystilink-horoscope-calculator`。

## 要件

- Python 3.9+
- `pip install pyswisseph`
- Agent Skills 互換ホスト
- Wiki API は任意（ネットワーク）

## インストール

フォルダ名は `mystilink-horoscope` 必須：

```bash
cp -R mystilink-horoscope-skill /path/to/.cursor/skills/mystilink-horoscope
```

| ホスト | パス |
|------|------|
| Cursor | `.cursor/skills/mystilink-horoscope/` |
| Claude Code | `.claude/skills/mystilink-horoscope/` |

## クイックスタート

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

任意：`--zodiac tropical|sidereal`、`--true-solar-time`。

成功：stdout に JSON。失敗：非ゼロ終了 + JSON error。

## ワークフロー

1. 出生データを収集 — `examples/profile.v0.json`（BirthProfile）または旧 `examples/profile.json`
2. ネイタルスクリプトを実行
3. 任意 Wiki：

```text
GET https://wiki.mystilink.com/api/v1/search?q=ascendant&system=horoscope&locale=en
GET https://wiki.mystilink.com/api/v1/pages/horoscope.concept.natal-chart?locale=en
```

4. 盤データと解釈を分ける

詳細：`SKILL.md`。案内：`references/overview.md`。

## 例

- `examples/profile.v0.json` — BirthProfile（`mystilink.birth/0.1`、架空）
- `examples/profile.json` — 旧架空ネイタル入力

## 制限

- `pyswisseph`（Swiss Ephemeris）が必要
- skill インストール用の内嵌スクリプトであり、多言語 SDK ではない
- Wiki locale 省略 → `en`；欠訳時は `zh-Hans` の場合あり

## ライセンス

MIT。[LICENSE](../../LICENSE) を参照。

## フィードバック

正確なコマンド（架空座標／日時）と JSON 出力／エラーを含めてください。
