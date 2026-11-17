# 🔒 Vibe Codebase Audit - 日本語使用ガイド

## 📋 概要

**Vibe Codebase Audit**は、AI生成コードベース向けの包括的セキュリティ監査ツールです。エージェントネイティブ統合、マルチプロバイダー対応、依存関係セキュリティスキャンを提供します。

> 🎉 **v2.0の新機能**: エージェントネイティブ監査（APIキー不要）、マルチプロバイダー対応、依存関係スキャン、設定監査

---

## ⚡ クイックスタート

### 方法1：エージェントネイティブ監査（推奨、セットアップ不要！）

```python
# APIキー不要！現在のエージェントのLLMを直接使用
from vibe_audit_enhanced import vibe_audit_enhanced

result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="agent_llm"  # 現在のエージェントのLLMを使用
)
```

### 方法2：APIキーを使用

```python
# 独自のOpenAI/Claude/その他のAPIを使用
result = await vibe_audit_enhanced(
    project_path=".",
    primary_provider="openai",  # または "claude", "ollama", "deepseek"
    fallback_provider="claude"
)
```

### 方法3：CLI使用

```bash
# エージェントのLLMを使用（APIキー不要）
python vibe_audit_enhanced.py /path/to/project --provider agent_llm

# OpenAIを使用
python vibe_audit_enhanced.py /path/to/project --provider openai

# ローカルOllamaモデルを使用
python vibe_audit_enhanced.py /path/to/project --provider ollama

# 増分監査（変更されたファイルのみ）
python vibe_audit_enhanced.py /path/to/project --incremental --base-branch main
```

---

## 🆕 v2.0の新機能

### 1. 🤖 エージェントネイティブ統合
- **セットアップ不要** - APIキー不要
- 現在のエージェントのLLM接続を使用
- OpenCode、Hermes、OpenClawとシームレスに統合
- コスト削減 - 既存のエージェントサブスクリプションを活用

### 2. 🔌 マルチプロバイダー対応
- **Agent LLM** - 現在のエージェントを使用（推奨）
- **OpenAI** - GPT-4, GPT-4-turbo
- **Claude** - Claude-3 Sonnet/Opus
- **DeepSeek** - コスパ重視の選択肢
- **Qwen/通義千問** - アリババのモデル
- **Ollama** - ローカルモデルを実行（無料！）

### 3. 📦 依存関係セキュリティスキャン
- 既知の脆弱性（CVE）をチェック
- 古い依存関係を検出
- ライセンスコンプライアンスチェック
- 対応：npm, pip, maven, cargo, go mod

### 4. ⚙️ 設定セキュリティチェック
- 露出した.envファイル検出
- CORS設定ミス検出
- デバッグモード検出
- SSL検証チェック

---

## 📊 ツール比較

| ツール | 速度 | 精度 | 機能 | APIキー | 最適な用途 |
|--------|------|------|------|---------|----------|
| `vibe_audit_enhanced` | 中速 | 高 | 全機能 | オプション | **本番環境** |
| `vibe_audit_scan` | 高速 | 中 | 基本 | 不要 | クイックチェック |
| `vibe_audit_multi_model` | 低速 | 最高 | AIコンセンサス | 必要 | 重要プロジェクト |
| `vibe_audit_incremental` | 超高速 | 中 | Git対応 | オプション | CI/CD |

**推奨**：`vibe_audit_enhanced`を`primary_provider="agent_llm"`で使用

---

## 🌐 プロバイダー設定

### エージェントLLM（推奨）
```python
# 設定不要！そのまま使用：
primary_provider="agent_llm"
```

### OpenAI
```bash
export OPENAI_API_KEY="sk-..."
```

### Claude
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Ollama（ローカル、無料）
```bash
# Ollamaをインストール
curl -fsSL https://ollama.com/install.sh | sh

# モデルをプル
ollama pull llama2

# 監査で使用
primary_provider="ollama"
```

---

## 🚨 リスクレベル

| レベル | スコア | アクション |
|--------|--------|------------|
| ✅ 安全 | 0 | 公開可能 |
| 🟢 低 | 1-19 | 軽微な問題、レビュー推奨 |
| 🟡 中 | 20-49 | 公開前にレビューと修正 |
| 🟠 高 | 50-79 | 重要な問題、修正必須 |
| 🔴 重大 | 80-100 | **公開禁止** |

---

## 🤝 サポート対象エージェント

- **OpenCode** - ネイティブスキル
- **Hermes** - プラグイン
- **OpenClaw** - モジュールインポート
- **MCP Clients** - プロトコル対応

---

## 📞 サポート

- **Issues**: [GitHub Issues](https://github.com/csmoove530/vibe-codebase-audit/issues)
- **ドキュメント**: SKILL.mdを参照
- **例**: examples/ディレクトリを参照

---

**自信を持ってデプロイ。厳格に監査。安心してコーディング。** 🚀
