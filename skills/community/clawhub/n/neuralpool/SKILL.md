---
name: neuralpool-node
description: Monetize idle LLM API capacity or access 100+ models through a unified OpenAI-compatible API. No GPU required.
homepage: https://neuralpool.ai
metadata:
  clawdbot:
    emoji: "🌐"
    requires:
      env: ["NEURALPOOL_AUTH_TOKEN"]
    primaryEnv: "NEURALPOOL_AUTH_TOKEN"
    files: ["scripts/install.sh"]
---

# NeuralPool Node

## What is NeuralPool?

NeuralPool is a decentralized LLM API marketplace. Think of it as an "Airbnb for LLM API access" — a peer-to-peer network where API resource owners and AI developers meet.

### Two ways to participate

**1. As a Node Operator (Earn Money)**

If you have cloud compute credits or access to LLM APIs sitting idle, you can monetize them:

- Register at [neuralpool.ai](https://neuralpool.ai)
- Install this Node Agent on your machine
- Configure your upstream providers and set your own prices
- Your idle capacity starts earning immediately — paid per token forwarded
- Earnings settle after a T+1 or T+30 clearing period, then withdraw to your Solana wallet

Your API keys **never leave your machine**. The Node Agent connects to NeuralPool's central server via an encrypted tunnel, receives inference requests, forwards them to your configured upstream provider, and streams the response back. The server handles all billing, user management, and payment settlement.

**2. As an API Consumer (Save Money)**

If you build AI applications and need affordable, reliable access to LLM models:

- Register at [neuralpool.ai](https://neuralpool.ai)
- Deposit USDT (SPL) to your account
- Get a single OpenAI-compatible API key that works across **all models from all providers** on the network
- Pay only for what you use — token-by-token billing with no monthly commitments
- Often significantly cheaper than direct provider pricing due to marketplace competition

### How it works

```
API Consumer                    Central Server                   Node Operator
    │                               │                               │
    │  OpenAI-format request        │                               │
    │──────────────────────────────>│                               │
    │                               │  Encrypted tunnel               │
    │                               │──────────────────────────────>│
    │                               │                               │──> Upstream LLM
    │                               │                               │<── Provider API
    │<──────────────────────────────│                               │
    │  OpenAI-format response       │  Billing: token-by-token      │
    │                               │  Settlement: NC credits        │
```

## Platform Features

- **Unified API**: One endpoint, one API key, all models. Different provider formats are handled automatically.
- **Self-pricing**: Node operators set their own per-model input/output prices. Market competition drives prices down for consumers.
- **Key security**: Upstream API keys never leave the Node operator's machine.
- **Real-time billing**: Accurate token-by-token charging. No over-billing.
- **Solana payments**: Deposit USDT (SPL), withdraw to any Solana wallet after T+1 or T+30 settlement (varies by funding source). NC (NeuralCredit) internal currency: 1 USD = 100 NC.
- **Multi-provider**: Support for major LLM providers with pre-configured endpoints. Just bring your API key.

## Quick Start for Node Operators

### Step 1: Register

Visit [neuralpool.ai](https://neuralpool.ai) and create an account. Navigate to the Nodes section and generate an authentication token.

### Step 2: Install

Run the installer script — it auto-detects your OS and architecture:

```bash
curl -fsSL https://neuralpool.ai/install.sh | bash
```

Or download manually from [GitHub Releases](https://github.com/neuralpool/neuralpool-node/releases):

| Platform | File |
|----------|------|
| Linux x86_64 | `npnode-linux-amd64` |
| Linux ARM64 | `npnode-linux-arm64` |
| macOS x86_64 | `npnode-darwin-amd64` |
| macOS ARM64 | `npnode-darwin-arm64` |
| Windows x86_64 | `npnode-windows-amd64.exe` |
| Windows ARM64 | `npnode-windows-arm64.exe` |

### Step 3: Configure

```bash
npnode setup
```

The interactive wizard will guide you through:
- Setting your NeuralPool auth token
- Adding upstream LLM providers (API key, provider selection)
- Selecting models to serve and setting your prices (per 1M tokens, input/output separately)
- Configuring concurrency and timeout limits

### Step 4: Start

```bash
npnode start
```

Your Node connects to the NeuralPool network and begins receiving requests. You earn NC credits for every token forwarded.

### Step 5: Monitor & Withdraw

- Dashboard at [neuralpool.ai](https://neuralpool.ai) shows real-time earnings, request stats, and node health
- Withdraw earnings to any Solana wallet after T+1 or T+30 settlement (varies by funding source)

## Quick Start for API Consumers

1. Register at [neuralpool.ai](https://neuralpool.ai)
2. Deposit USDT (SPL) to your dedicated deposit address
3. Generate an API key from the dashboard
4. Use it as a drop-in replacement for any OpenAI SDK:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://neuralpool.ai/v1",
    api_key="sk-YOUR_API_KEY_HERE"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Node Agent Commands

| Command | Description |
|---------|-------------|
| `npnode setup` | Interactive configuration wizard |
| `npnode start` | Start the Node and begin forwarding requests |
| `npnode config` | Display current configuration |
| `npnode reset-quota [model]` | Reset token quota counter for a model (or all) |
| `npnode version` | Print version |

## Pricing & Currency

- **NC (NeuralCredit)**: Internal platform currency. 1 USD = 100 NC = 1,000,000 uNC
- Node operators set prices in uNC per 1M tokens (input and output separately)
- Platform commission applies on top of node operator prices
- Consumers see and pay the final price including commission

## Security Model

- Upstream API keys stored locally, never transmitted to the server
- All communication with the server is encrypted
- Server connection is automatic — no manual configuration needed

## Requirements

- Any machine with internet access (no GPU required — you're proxying API calls, not running inference locally)
- Go 1.24+ (only if building from source)
- Network access to NeuralPool Central Server
- Network access to your configured upstream LLM provider APIs

## External Endpoints

| URL | Purpose | Data Sent |
|-----|---------|-----------|
| NeuralPool server | Encrypted tunnel to central server | Auth token, model requests/responses, billing data |
| Upstream LLM providers | Pre-configured provider API endpoints | LLM prompts, receives completions |

## Links

- **Website**: [neuralpool.ai](https://neuralpool.ai)
- **Documentation**: [docs.neuralpool.ai](https://neuralpool.ai/docs)
- **GitHub**: [github.com/neuralpool](https://github.com/neuralpool)
- **Support**: support@neuralpool.ai

## License

MIT

---

# NeuralPool ノード

## NeuralPoolとは？

NeuralPoolは、分散型LLM APIマーケットプレイスです。「LLM APIアクセスのAirbnb」のような存在で、APIリソースの所有者とAI開発者が出会うP2Pネットワークです。

### 参加方法は2つ

**1. ノードオペレーターとして（収益化）**

クラウドコンピューティングクレジットやLLM APIへのアクセスが余っている場合、それを収益化できます：

- [neuralpool.ai](https://neuralpool.ai) でアカウント登録
- このノードエージェントをマシンにインストール
- 上流プロバイダーを設定し、独自の価格を設定
- アイドルキャパシティがすぐに収益を生み始めます — 転送されたトークンごとに課金
- 収益はT+1またはT+30決済期間後にSolanaウォレットに出金可能

APIキーは**マシンから一切送信されません**。ノードエージェントは暗号化トンネルでNeuralPoolの中央サーバーに接続し、推論リクエストを受信、設定された上流プロバイダーに転送し、レスポンスをストリーミングします。サーバーは課金、ユーザー管理、決済をすべて処理します。

**2. API利用者として（コスト削減）**

AIアプリケーションを構築していて、安価で信頼性の高いLLMモデルアクセスが必要な場合：

- [neuralpool.ai](https://neuralpool.ai) でアカウント登録
- USDT（SPL）をアカウントに入金
- ネットワーク上の**すべてのプロバイダーのすべてのモデル**に対応する単一のOpenAI互換APIキーを取得
- 従量課金 — トークンごとの課金、月額コミットメントなし
- マーケットプレイスの競争により、直接プロバイダー料金より大幅に安価

### ノードオペレーターのクイックスタート

**ステップ1**: [neuralpool.ai](https://neuralpool.ai) で登録し、認証トークンを生成

**ステップ2**: インストール
```bash
curl -fsSL https://neuralpool.ai/install.sh | bash
```

**ステップ3**: 設定
```bash
npnode setup
```

**ステップ4**: 起動
```bash
npnode start
```

**ステップ5**: ダッシュボードでリアルタイム収益を確認し、Solanaウォレットに出金

### プラットフォーム機能

- **統合API**: エンドポイント1つ、APIキー1つで全モデル対応。異なるプロバイダー間の形式差異は自動処理
- **自己価格設定**: ノードオペレーターがモデルごとに入力/出力価格を自由設定。市場競争が消費者価格を下げる
- **キーセキュリティ**: 上流APIキーはノードオペレーターのマシンから一切送信されない
- **リアルタイム課金**: 正確なトークンごとの課金
- **Solana決済**: USDT（SPL）入金、T+1またはT+30決済後に任意のSolanaウォレットに出金可能
- **マルチプロバイダー**: 主要なLLMプロバイダーに対応。エンドポイントは事前設定済み、APIキーを追加するだけ

### API利用者のクイックスタート

1. [neuralpool.ai](https://neuralpool.ai) で登録
2. 専用入金アドレスにUSDT（SPL）を入金
3. ダッシュボードでAPIキーを生成
4. 任意のOpenAI SDKのドロップイン置き換えとして使用：

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://neuralpool.ai/v1",
    api_key="sk-YOUR_API_KEY_HERE"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "こんにちは！"}]
)
```

### ノードエージェントコマンド

| コマンド | 説明 |
|---------|------|
| `npnode setup` | 対話型設定ウィザード |
| `npnode start` | ノードを起動しリクエストの転送を開始 |
| `npnode config` | 現在の設定を表示 |
| `npnode reset-quota [model]` | モデルのトークンクォータカウンターをリセット（全モデルも可） |
| `npnode version` | バージョンを表示 |

### 料金と通貨

- **NC（NeuralCredit）**: プラットフォーム内部通貨。1 USD = 100 NC = 1,000,000 uNC
- ノードオペレーターは1MトークンあたりのuNCで価格を設定（入力/出力別）
- プラットフォーム手数料がオペレーター価格に上乗せ
- 利用者は手数料込みの最終価格を確認し支払う

### セキュリティモデル

- 上流APIキーはローカル保存、サーバーに送信されない
- サーバーとの通信はすべて暗号化
- サーバー接続は自動 — 手動設定不要

### 要件

- インターネット接続のあるマシン（GPU不要 — API呼び出しの転送であり、ローカル推論ではない）
- Go 1.24+（ソースからビルドする場合のみ）
- NeuralPoolセントラルサーバーへのネットワークアクセス
- 設定した上流LLMプロバイダーAPIへのネットワークアクセス

### 外部エンドポイント

| URL | 目的 | 送信データ |
|-----|------|-----------|
| NeuralPoolサーバー | 暗号化トンネルでセントラルサーバーに接続 | 認証トークン、モデルリクエスト/レスポンス、課金データ |
| 上流LLMプロバイダー | 事前設定済みのプロバイダーAPIエンドポイント | LLMプロンプト、レスポンス受信 |

### リンク

- **ウェブサイト**: [neuralpool.ai](https://neuralpool.ai)
- **ドキュメント**: [docs.neuralpool.ai](https://neuralpool.ai/docs)
- **GitHub**: [github.com/neuralpool](https://github.com/neuralpool)
- **サポート**: support@neuralpool.ai

### ライセンス

MIT

---

# NeuralPool 节点

## NeuralPool 是什么？

NeuralPool 是一个去中心化的 LLM API 市场。你可以把它想象成"LLM API 访问的 Airbnb"——一个 API 资源拥有者和 AI 开发者直接对接的 P2P 网络。

### 两种参与方式

**1. 作为节点运营者（赚钱）**

如果你有云计算额度或 LLM API 访问权限处于闲置状态，你可以把它们变现：

- 在 [neuralpool.ai](https://neuralpool.ai) 注册账号
- 在你的机器上安装本节点代理
- 配置你的上游 LLM 供应商，自主定价
- 闲置算力立即开始赚钱——按转发的 token 计费
- 收益经 T+1 或 T+30 结算周期后可提现到你的 Solana 钱包

你的 API 密钥**永远不会离开你的机器**。节点代理通过加密隧道连接到 NeuralPool 中央服务器，接收推理请求，转发到配置的上游供应商，并流式返回响应。服务器负责所有计费、用户管理和支付结算。

**2. 作为 API 使用者（省钱）**

如果你在构建 AI 应用，需要经济实惠、稳定可靠的 LLM 模型访问：

- 在 [neuralpool.ai](https://neuralpool.ai) 注册账号
- 向账户充值 USDT（SPL）
- 获取一个 OpenAI 兼容的 API 密钥，即可访问网络上**所有供应商的所有模型**
- 按量付费——逐 token 计费，无需月度承诺
- 由于市场竞争，通常比直接使用供应商便宜得多

### 节点运营者快速开始

**第1步**: 在 [neuralpool.ai](https://neuralpool.ai) 注册并生成认证令牌

**第2步**: 安装
```bash
curl -fsSL https://neuralpool.ai/install.sh | bash
```

**第3步**: 配置
```bash
npnode setup
```

**第4步**: 启动
```bash
npnode start
```

**第5步**: 在仪表盘查看实时收益，T+1 或 T+30 结算后提现到 Solana 钱包

### 平台特性

- **统一 API**: 一个端点、一个密钥、所有模型。不同供应商格式自动处理
- **自主定价**: 节点运营者自行设置每个模型的输入/输出价格。市场竞争为使用者带来更低价格
- **密钥安全**: 上游 API 密钥从不离开节点运营者的机器
- **实时计费**: 精确的逐 token 计费
- **Solana 支付**: 充值 USDT（SPL），T+1 或 T+30 结算后可提现到任意 Solana 钱包
- **多供应商支持**: 支持主流 LLM 供应商，端点已预配置，只需提供 API 密钥

### API 使用者快速开始

1. 在 [neuralpool.ai](https://neuralpool.ai) 注册
2. 向专属充值地址存入 USDT（SPL）
3. 在仪表盘生成 API 密钥
4. 作为任意 OpenAI SDK 的即插即用替代：

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://neuralpool.ai/v1",
    api_key="sk-YOUR_API_KEY_HERE"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "你好！"}]
)
```

### 节点代理命令

| 命令 | 说明 |
|---------|------|
| `npnode setup` | 交互式配置向导 |
| `npnode start` | 启动节点并开始转发请求 |
| `npnode config` | 显示当前配置 |
| `npnode reset-quota [model]` | 重置某模型（或全部）的 token 配额计数 |
| `npnode version` | 打印版本号 |

### 定价与货币

- **NC（NeuralCredit）**：平台内部货币。1 USD = 100 NC = 1,000,000 uNC
- 节点运营者以 uNC/百万 token 为单位自主定价（输入/输出分开）
- 平台在运营者价格之上收取佣金
- 使用者看到并支付含佣金的最终价格

### 安全模型

- 上游 API 密钥存储在本地，绝不发送到服务器
- 与服务器的所有通信均已加密
- 服务器连接自动完成——无需手动配置

### 系统要求

- 任意可联网的机器（无需 GPU——你转发 API 调用，不在本地跑推理）
- Go 1.24+（仅源码编译时需要）
- 可访问 NeuralPool 中央服务器的网络
- 可访问你配置的上游 LLM 供应商 API 的网络

### 外部端点

| URL | 用途 | 发送的数据 |
|-----|------|-----------|
| NeuralPool 服务器 | 加密隧道连接中央服务器 | 认证令牌、模型请求/响应、计费数据 |
| 上游 LLM 供应商 | 预配置的供应商 API 端点 | LLM 提示词，接收回复 |

### 链接

- **网站**: [neuralpool.ai](https://neuralpool.ai)
- **文档**: [docs.neuralpool.ai](https://neuralpool.ai/docs)
- **GitHub**: [github.com/neuralpool](https://github.com/neuralpool)
- **支持**: support@neuralpool.ai

### 许可证

MIT
