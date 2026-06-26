# openclaw-memory-transfer

> **OpenClaw のためのゼロフリクション記憶移行。** ChatGPT、Claude、Gemini、Copilot などから記憶を移行 — 10分以内で完了。

[![Powered by MyClaw.ai](https://img.shields.io/badge/Powered%20by-MyClaw.ai-blue)](https://myclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[English](README.md) | [中文](README.zh-CN.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [Italiano](README.it.md) | [Español](README.es.md)

---

ChatGPT と何ヶ月も（何年も）過ごしてきました。あなたの文体、プロジェクト、好みを知っています。OpenClaw に乗り換えるとき、それらをゼロからやり直す必要はありません。

**Memory Transfer** は、以前の AI アシスタントがあなたについて知っていることをすべて抽出し、クリーンアップして OpenClaw のメモリシステムにインポートします。

## 使い方

OpenClaw エージェントに話しかけてください：

```
ChatGPT から移行したい
```

## サポート対象

| ソース | 方法 | 操作 |
|--------|------|------|
| **ChatGPT** | ZIPデータエクスポート | 設定でエクスポートをクリック、ZIPをアップロード |
| **Claude.ai** | プロンプトガイド | プロンプトをコピー、結果を貼り付け |
| **Gemini** | プロンプトガイド | プロンプトをコピー、結果を貼り付け |
| **Copilot** | プロンプトガイド | プロンプトをコピー、結果を貼り付け |
| **Claude Code** | 自動スキャン | 不要 — 自動 |
| **Cursor** | 自動スキャン | 不要 — 自動 |
| **Windsurf** | 自動スキャン | 不要 — 自動 |

## 移行内容

| カテゴリ | 出力先 | 例 |
|----------|--------|-----|
| アイデンティティ | `USER.md` | 名前、職業、言語、タイムゾーン |
| コミュニケーションスタイル | `USER.md` | 文体、フォーマット好み |
| 知識と経験 | `MEMORY.md` | プロジェクト、専門知識、洞察 |
| 行動パターン | `MEMORY.md` | ワークフロー、習慣、修正記録 |
| ツール設定 | `TOOLS.md` | 技術スタック、プラットフォーム |

## インストール

```bash
clawhub install openclaw-memory-transfer
```

## ライセンス

MIT

---

**Powered by [MyClaw.ai](https://myclaw.ai)**
