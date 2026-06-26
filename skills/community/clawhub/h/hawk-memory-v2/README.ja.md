# 🦅 Context-Hawk

> **AI コンテキスト記憶ガーディアン** — 追跡を失うことをやめ、重要ことを記憶し始める。

*どの AI agent にも、session をまたぎ、トピックをまたぎ、時間を超えて実際に機能する記憶を。*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## 何をするのか？

ほとんどの AI agent は**健忘症**に苦しんでいます — 新しい session が開始されるたびにゼロから始まります。Context-Hawk は、本番対応の記憶管理システムでこれ問題を解決します。重要なことを自動的に捕捉し、ノイズを忘れさせ、正しい時間に正しい記憶を思い出させます。

**Context-Hawk なし：**
> "もう言いましたよね — 簡潔な返信が好きだって！"
>（次の session、agent はまた忘れる）

**Context-Hawk あり：**
>（session 1 から静かにコミュニケーションの好みを適用）
> ✅ 毎回簡潔で直接的な回答を配信

---

## ✨ 10 のコア機能

| # | 機能 | 説明 |
|---|---------|-------|
| 1 | **タスク状態持続性** | `hawk resume` — タスク状態を保持、再起動後も再開可能 |
| 2 | **4層記憶** | Working → Short → Long → Archive（Weibull 崩壊付） |
| 3 | **構造化 JSON** | 重要度スコア（0-10）、カテゴリ、ティア、L0/L1/L2 レイヤー |
| 4 | **AI 重要度スコアリング** | 記憶に自動スコア、低価値コンテンツは破棄 |
| 5 | **5つの注入戦略** | A(高重要度) / B(タスク関連) / C(最近) / D(Top5) / E(フル) |
| 6 | **5つの圧縮戦略** | summarize / extract / delete / promote / archive |
| 7 | **自己内省** | タスクの明確さ、欠落情報、ループ検出をチェック |
| 8 | **LanceDB ベクトル検索** | オプション — ハイブリッド vector + BM25 検索 |
| 9 | **Pure-Memory フォールバック** | LanceDB なしでも動作、JSONL ファイル永続化 |
| 10 | **自動重複排除** | 重複記憶を自動的にマージ |

---

## 🏗️ アーキテクチャ

```
┌──────────────────────────────────────────────────────────────┐
│                      Context-Hawk                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Working Memory  ←── 現在の session（最近 5-10 ターン）    │
│       ↓ Weibull 崩壊                                        │
│  Short-term      ←── 24時間コンテンツ、要約済み             │
│       ↓ access_count ≥ 10 + 重要度 ≥ 0.7                │
│  Long-term       ←── 永続的知識、ベクトルインデックス        │
│       ↓ >90 日または decay_score < 0.15                      │
│  Archive          ←── 履歴、オンデマンドでロード           │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Task State Memory  ←── 再起動間を永続化（重要！）          │
│  - 現在のタスク / 次のステップ / 進捗 / 出力             │
├──────────────────────────────────────────────────────────────┤
│  注入エンジン       ←── 戦略 A/B/C/D/E が検索を決定       │
│  自己内省            ←── 毎回答がコンテキストをチェック     │
│  自動トリガー        ←── 毎 10 ターン（設定可能）        │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 タスク状態記憶（最も価値のある機能）

再起動、電源障害、session 切替後も、Context-Hawk は中断した正確な位置から再開します。

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "API 文書を完成させる",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["アーキテクチャテンプレートをレビュー", "ユーザーに報告"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["カバー率は98%必須", "APIはバージョン化管理"],
  "resumed_count": 3
}
```

```bash
hawk task "文書を完成させる"  # タスク作成
hawk task --step 1 done     # ステップ完了をマーク
hawk resume                   # 再起動後に再開 ← コア機能！
```

---

## 🧠 構造化記憶

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "完全な元のコンテンツ",
  "summary": "1行サマリー",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### 重要度スコアリング

| スコア | タイプ | アクション |
|-------|------|--------|
| 0.9-1.0 | 決定/規則/エラー | 永久、最も遅い崩壊 |
| 0.7-0.9 | タスク/好み/知識 | 長期記憶 |
| 0.4-0.7 | 対話/議論 | 短期、アーカイブへ崩壊 |
| 0.0-0.4 | チャット/挨拶 | **破棄、決して格納しない** |

---

## 🎯 5 つのコンテキスト注入戦略

| 戦略 | トリガー | 節約量 |
|------|---------|--------|
| **A: 高重要性** | `重要度 ≥ 0.7` | 60-70% |
| **B: タスク関連** | スコープ一致 | 30-40% ← デフォルト |
| **C: 最近** | 最後 10 ターン | 50% |
| **D: Top5 リコール** | `access_count` Top 5 | 70% |
| **E: フル** | フィルターなし | 100% |

---

## 🗜️ 5 つの圧縮戦略

`summarize` · `extract` · `delete` · `promote` · `archive`

---

## 🔔 4段階アラートシステム

| レベル | 閾値 | アクション |
|-------|---------|------|
| ✅ Normal | < 60% | サイレント |
| 🟡 Watch | 60-79% | 圧縮を提案 |
| 🔴 Critical | 80-94% | 自動書き込みを一時停止、強制提案 |
| 🚨 Danger | ≥ 95% | 書き込みをブロック、圧縮必須 |

---

## 🚀 クイックスタート

```bash
# LanceDB プラグインをインストール（推奨）
openclaw plugins install memory-lancedb-pro@beta

# スキルを有効化
openclaw skills install ./context-hawk.skill

# 初期化
hawk init

# コアコマンド
hawk task "私のタスク"    # タスク作成
hawk resume             # 最後のタスクを再開 ← 最も重要
hawk status            # コンテキスト使用状況を查看
hawk compress          # 記憶を圧縮
hawk strategy B        # タスク関連モードに切替
hawk introspect         # 自己内省レポート
```

---

## 自動トリガー：毎 N ターン

毎 **10 ターン**（デフォルト、設定可能）、Context-Hawk は自動的に：

1. コンテキスト水位を確認
2. 記憶の重要度を評価
3. ユーザーに状況を報告
4. 必要に応じて圧縮を提案

```bash
# 設定（memory/.hawk/config.json）
{
  "auto_check_rounds": 10,          # 毎 N ターン確認
  "keep_recent": 5,                 # 最後の N ターンを保持
  "auto_compress_threshold": 70      # 70% を超えたら圧縮
}
```

---

## ファイル構造

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Python CLI ツール
└── references/
    ├── memory-system.md           # 4層アーキテクチャ
    ├── structured-memory.md      # 記憶フォーマットと重要度
    ├── task-state.md           # タスク状態持続性
    ├── injection-strategies.md  # 5つの注入戦略
    ├── compression-strategies.md # 5つの圧縮戦略
    ├── alerting.md             # アラートシステム
    ├── self-introspection.md   # 自己内省
    ├── lancedb-integration.md  # LanceDB 統合
    └── cli.md                  # CLI リファレンス
```

---

## 🔌 技術仕様

- **永続化**: JSONL ローカルファイル、データベース不要
- **ベクトル検索**: LanceDB（オプション）、ファイルへの自動フォールバック
- **Cross-Agent**:  универсальный, без бизнес-логики, работает с любым AI-агентом
- **ゼロ設定**: 優れたデフォルトで箱から出してすぐ動作
- **拡張可能**: カスタム注入戦略、圧縮ポリシー、スコアリングルール

---

## ライセンス

MIT — 無償で可以使用、修正、配布できます。
