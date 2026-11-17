# Mystilink 紫微 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概要

紫微斗数向け Agent Skill：内嵌 Python スクリプトで十二宮盤（任意で四化）を作成し、理論ページで解釈します。盤計算は `scripts/` にあります。

## 配布形態

**Agent Skill** パッケージ。計算機の言語マトリクス（C / C++ / C# / Java / JS / Python SDK）は **適用しません**。任意の同系列：`mystilink-ziwei-calculator`。

## 要件

- Python 3.9+
- `pip install zhdate`
- Agent Skills 互換ホスト
- Wiki API は任意（ネットワーク）

## インストール

フォルダ名は `mystilink-ziwei` 必須：

```bash
cp -R mystilink-ziwei-skill /path/to/.cursor/skills/mystilink-ziwei
```

| ホスト | パス |
|------|------|
| Cursor | `.cursor/skills/mystilink-ziwei/` |
| Claude Code | `.claude/skills/mystilink-ziwei/` |

## クイックスタート

```bash
python3 scripts/ziwei_chart_calculate.py \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --gender female \
  --output json

python3 scripts/ziwei_chart_calculate.py \
  --birth-json examples/profile.v0.json \
  --output json
```

任意フラグ：`--si-hua`、`--year YYYY`、`--longitude E`、`--midnight-zi`。

成功：stdout に JSON。失敗：非ゼロ終了 + JSON error。

## ワークフロー

1. 出生データを収集 — `examples/profile.v0.json`（BirthProfile）または旧 `examples/profile.json`
2. 盤スクリプトを実行
3. 任意 Wiki：

```text
GET https://wiki.mystilink.com/api/v1/search?q=life+palace&system=ziwei&locale=en
GET https://wiki.mystilink.com/api/v1/pages/ziwei.concept.ming-gong?locale=en
```

4. 盤の事実と解釈を分ける

詳細：`SKILL.md`。案内：`references/overview.md`。

## 例

- `examples/profile.v0.json` — BirthProfile（`mystilink.birth/0.1`、架空）
- `examples/profile.json` — 旧架空出生入力

## 制限

- 太陰暦変換は `zhdate` に依存
- スタンドアロン skill 用の内嵌スクリプトであり、多言語 SDK ではない
- Wiki locale 省略 → `en`；欠訳時は `zh-Hans` の場合あり

## ライセンス

MIT。[LICENSE](../../LICENSE) を参照。

## フィードバック

正確なコマンド（架空日時）と JSON 出力／エラーを含めてください。
