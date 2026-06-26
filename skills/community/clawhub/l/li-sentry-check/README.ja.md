# 🔍 li_sentry_check - サーバーインスペクションスキル

> マルチプラットフォームサーバーインスペクション＆ヘルスチェックスキル。SSHキー認証でリモートLinuxサーバーにログインし、読み取り専用インスペクションコマンドを実行して、構造化されたMarkdownレポートを生成します。

[![バージョン](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://clawhub.ai/skills/li_sentry_check)
[![プラットフォーム](https://img.shields.io/badge/プラットフォーム-nanobot%20%7C%20OpenClaw%20%7C%20Hermes-green.svg)]()
[![ライセンス](https://img.shields.io/badge/ライセンス-MIT-green.svg)](LICENSE)

## 📋 概要

`li_sentry_check`は**nanobot**、**OpenClaw**、**Hermes agent**をサポートするクロスプラットフォームサーバーインスペクションスキルです。SSHキー認証でリモートLinuxサーバーにログインし、読み取り専用インスペクションコマンド（CPU、メモリ、ディスク、ネットワーク、サービス、セキュリティ）を実行して、異常情報を自動的にハイライトする構造化されたMarkdownレポートを生成します。

## ✨ コア機能

| 機能 | 説明 |
|------|------|
| 🔐 SSHキー認証 | キー認証のみ、パスワードログイン無効化、セキュリティ強化 |
| 📊 ハードウェアインスペクション | CPU、メモリ、ディスク、ネットワーク使用量 |
| 🖥️ サービスインスペクション | 重要サービス状態、エラーログ |
| 🛡️ セキュリティインスペクション | SSH異常ログイン、ファイアウォールアラート、カーネルエラー |
| 📝 構造化レポート | Markdown/JSON形式、異常優先表示 |
| 🌐 クロスプラットフォーム | nanobot、OpenClaw、Hermesをサポート |

## 🚀 クイックスタート

### 1. スキルインストール

```bash
# nanobot
./manage.sh skill install li_sentry_check

# OpenClaw
npx clawhub@latest install li_sentry_check

# Hermes
hermes skill install li_sentry_check
```

### 2. SSHキー設定

```bash
# キーペア生成
ssh-keygen -t rsa -b 4096 -f ~/.ssh/li_sentry_check -N ""

# 公開キーをリモートサーバーにコピー
ssh-copy-id -i ~/.ssh/li_sentry_check.pub inspector@<サーバーIP>

# 接続テスト
ssh -i ~/.ssh/li_sentry_check inspector@<サーバーIP>
```

### 3. ターゲットサーバー設定

`references/targets.yaml`を編集：

```yaml
targets:
  プロダクション-web:
    host: YOUR_SERVER_IP
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - nginx
      - docker
      - sshd
```

### 4. インスペクション実行

```bash
# ベーシックインスペクション（ハードウェアリソース）
python3 scripts/inspect.py --target プロダクション-web --checks basic

# サービスインスペクション
python3 scripts/inspect.py --target プロダクション-web --checks services

# 完全インスペクション（ベーシック + サービス + セキュリティ + ログ）
python3 scripts/inspect.py --target プロダクション-web --checks daily

# JSON形式出力
python3 scripts/inspect.py --target プロダクション-web --checks daily --format json

# ファイルに出力
python3 scripts/inspect.py --target プロダクション-web --checks daily --output report.md
```

## 📖 インスペクションチェックグループ

| グループ | 内容 | コマンド数 |
|----------|------|------------|
| `basic` | CPU、メモリ、ディスク、ネットワーク | 8 |
| `services` | サービス状態 + エラーログ（動的） | 3×N |
| `daily` | 完全インスペクション（ベーシック + サービス + セキュリティ + ログ） | 26 |

## 📊 レポート例

```markdown
# 🔍 サーバーインスペクションレポート

- ターゲット: プロダクション-web
- ホスト: YOUR_SERVER_IP
- ユーザー: inspector
- チェック: daily
- 開始: 2026-04-26T09:00:00+00:00
- 総チェック: 26
- ⚠️ 異常: 3

## 全体ステータス: ⚠️ 警告

## ⚠️ 異常（優先）

### ⚠️ systemd_failed_units
コマンド: `systemctl --failed --no-pager`
ステータス: OK（異常を含む）

出力:
```
UNIT          LOAD   ACTIVE SUB    DESCRIPTION
mcelog.service loaded failed failed Machine Check Exception Logging Daemon
```
```

## 🔧 コマンドラインオプション

| オプション | 説明 | デフォルト |
|------------|------|------------|
| `--target` | ターゲットサーバー名（targets.yamlで定義） | （必須） |
| `--checks` | チェックグループ: `basic`、`services`、`daily` | `basic` |
| `--format` | 出力形式: `markdown`、`json` | `markdown` |
| `--output` | ファイルに出力（デフォルト: stdout） | stdout |

## 🌐 クロスプラットフォームサポート

| プラットフォーム | ランタイム | スクリプト | コマンド |
|------------------|------------|------------|----------|
| **OpenClaw** | Node.js 24+ | `scripts/inspect.mjs` | `node scripts/inspect.mjs --target bogon --checks daily` |
| **NanoBot** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |
| **Hermes** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |

## 📁 ファイル構造

```
li_sentry_check/
├── SKILL.md                  # スキルドキュメント
├── _meta.json                # スキルメタデータ
├── design.md                 # デザインドキュメント
├── references/
│   ├── targets.yaml          # ターゲットサーバー設定
│   └── checks.yaml           # インスペクションコマンドホワイトリスト
└── scripts/
    ├── inspect.mjs           # Node.js実装（OpenClaw）
    └── inspect.py            # Python実装（NanoBot/Hermes）
```

## 🔒 セキュリティベストプラクティス

- **キー権限**: `chmod 600 ~/.ssh/li_sentry_check`
- **ホスト検証**: プロダクションでは`accept-new`の代わりに`known_hosts`を事前に設定
- **サービス名**: 英数字、ハイフン、アンダースコアのみ許可（使用前に検証）
- **コマンドホワイトリスト**: `checks.yaml`を状態変更コマンドで決して修正しない
- **レポート処理**: レポートにシステムデータが含まれる可能性があります — 公開で共有しないでください

## 🔧 拡張ガイド

### 新しいターゲットサーバー追加

`references/targets.yaml`を編集：

```yaml
targets:
  データベース-サーバー:
    host: YOUR_SERVER_IP
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - mysql
      - redis
```

### 新しいチェックグループ追加

`references/checks.yaml`を編集：

```yaml
checks:
  データベース:
    description: データベースインスペクション
    commands:
      - id: mysql_status
        cmd: "systemctl status mysql --no-pager | sed -n '1,20p'"
        timeoutSec: 10
      - id: mysql_connections
        cmd: "mysql -e 'SHOW STATUS LIKE \"Threads_connected\"' || true"
        timeoutSec: 15
```

## 📝 バージョン履歴

| バージョン | 日付 | 変更 |
|------------|------|------|
| 0.1.0 | 2026-04-26 | 初期リリース: ベーシック、サービス、完全インスペクション |

## 📄 ライセンス

MITライセンス
