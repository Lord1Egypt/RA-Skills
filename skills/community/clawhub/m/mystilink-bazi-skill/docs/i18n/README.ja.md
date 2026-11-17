# Mystilink 八字 Skill

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

## 概要

八字（四柱）向け Agent Skill：内嵌スクリプトで出生データから柱・大運・流年を計算し、理論ページ（日主・十神など）で解釈します。盤の計算は `scripts/` にあります。

## 配布形態

本リポジトリは **Agent Skill** パッケージ（`SKILL.md` + `scripts/` + `references/` + `examples/`）です。計算機ライブラリの C / C++ / C# / Java / JavaScript / Python 言語マトリクスは **適用しません**。多言語 SDK/CLI は同系列の `mystilink-bazi-calculator`（任意；本 skill の実行に必須ではありません）。

## 要件

- Python 3.9+（`zoneinfo`）
- Agent Skills 互換ホスト
- 解釈時の Mystilink Wiki API は任意（ネットワーク）

## インストール

フォルダ名は `mystilink-bazi`（`SKILL.md` の `name` と一致）：

| ホスト | パス |
|------|------|
| Cursor | `.cursor/skills/mystilink-bazi/` |
| Claude Code | `.claude/skills/mystilink-bazi/` |

```bash
cp -R mystilink-bazi-skill /path/to/.cursor/skills/mystilink-bazi
```

## クイックスタート（スクリプト）

skill ディレクトリで：

```bash
python3 scripts/bazi_calculate.py --date 1990-05-15 --hour 12
python3 scripts/bazi_calculate.py --birth-json examples/profile.v0.json
python3 scripts/bazi_calculate.py --profile-json examples/profile.json
python3 scripts/bazi_dayun_calculate.py --date 1990-05-15 --gender female --count 8
python3 scripts/bazi_liunian_calculate.py --year 2026 --day-stem 甲
```

成功：stdout に JSON。失敗：非ゼロ終了と JSON `{"error":…}`。

柱オブジェクトは `stem_index`、`branch_index`、`text`、および旧フィールド `ganzhi`（`=` `text`）を含みます。

## ワークフロー

1. 出生プロフィールを収集——いずれか：
   - `examples/profile.v0.json`（`mystilink.birth/0.1` BirthProfile）、または
   - `examples/profile.json`（旧 skill フィールド）
2. 必要に応じて盤スクリプトを実行（`--birth-json` / `--profile-json` は両形状を受理）
3. 任意で Wiki 解釈：

```text
GET https://wiki.mystilink.com/api/v1/search?q=day+master&system=bazi&locale=en
GET https://wiki.mystilink.com/api/v1/pages/bazi.concept.ri-zhu?locale=en
```

4. **盤の事実** と **解釈** を分け、Wiki 使用時は出典を明示

詳細：`SKILL.md`。短い id：`references/wiki-ids.md`。

## 例

- `examples/profile.v0.json` — BirthProfile（`mystilink.birth/0.1`、架空）
- `examples/profile.json` — 旧出生プロフィール（架空）；スクリプトは引き続き受理

## 制限

- スクリプトはスタンドアロン skill 用の内嵌コピーであり、多言語 SDK ではない
- 大運の節気日は公暦の近似
- 真太陽時にはタイムゾーンと経度の両方が必要
- Wiki locale：省略 → `en`；欠訳時は `zh-Hans` にフォールバックする場合あり

## ライセンス

MIT。[LICENSE](../../LICENSE) を参照。

## フィードバック

正確なスクリプトコマンド（架空日付のみ）と stdout/stderr JSON を添えて報告してください。
