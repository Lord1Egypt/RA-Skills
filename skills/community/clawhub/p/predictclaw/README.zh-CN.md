# PredictClaw

[English Version / 英文版](./README.md)

PredictClaw 是一个面向 **OpenClaw** 的 `predict.fun` skill / CLI，用于浏览市场、检查钱包 readiness、查看资金引导、执行买入、查询持仓，以及在需要时分析对冲机会。

这个仓库将 PredictClaw 打包为一个独立的 OpenClaw skill，并包含自己的 CLI、运行时配置和测试体系。

PredictClaw 的版本以仓库根目录的 `pyproject.toml` 为唯一 source of truth。无论你是在 GitHub 上核对版本，还是准备从源码安装，都应该直接看这个仓库根目录。

## PredictClaw 的作用

PredictClaw 为 OpenClaw 提供一套稳定的 predict.fun 工作流接口：

- 浏览市场与查看单市场详情
- 检查钱包 readiness 与入金引导
- 通过 EOA 或 Predict Account 路径交易
- 记录并查询持仓
- 在启用模型能力时执行可选 hedge 分析

对于高级资金路线，PredictClaw 支持在官方 Predict Account 路径上叠加 **Vault funding overlay**。在这条路线中，**Predict Account remains** 交易身份与入金地址，而 Vault 作为资金来源。

## 安装

### 通过 ClawHub 安装

```bash
clawhub install predictclaw
cd ~/.openclaw/skills/predictclaw
uv sync
cp template.env .env
```

安装后的 skill 目录 `~/.openclaw/skills/predictclaw` 是唯一规范的用户配置根目录。在 OpenClaw 的一些清单或示例里，这个已安装路径也可能写成 `{baseDir}`。任何仓库 checkout 或 workspace 副本都只是 development-only artifact，不是用户配置根目录。

### 手动安装

1. 将整个仓库复制或软链接到 `~/.openclaw/skills/predictclaw/`
2. 在安装后的 skill 目录执行：

```bash
cd {baseDir} && uv sync
cd {baseDir} && cp template.env .env
```

### 在仓库内本地开发

在仓库根目录执行：

```bash
uv sync
uv run pytest -q
uv run python scripts/predictclaw.py --help
```

仓库根目录只用于开发和测试，不应被当作日常用户编辑 `.env` 或调用已安装 skill CLI 的规范位置。

## 配置实际上是怎么生效的

PredictClaw 本身只读取标准环境变量。当前已验证、可用的输入方式只有两种：

- 进程环境变量，例如 `export PREDICT_ENV=testnet`
- 本地 `~/.openclaw/skills/predictclaw/.env` 文件；`scripts/predictclaw.py` 启动时会自动加载它，在清单或示例里这个已安装路径也可能写成 `{baseDir}`

如果两者同时存在，显式导出的环境变量优先，`.env` 只会补齐缺失项。

如果你的 OpenClaw 宿主版本会把配置注入成环境变量，PredictClaw 也能工作，因为它最终看到的仍然是普通 env。旧文档里提到过 `skills.entries.predictclaw.env`；现在应把它视为“某些宿主版本可能支持的便利映射”，而不是 PredictClaw 自己保证的标准配置入口。

SKILL frontmatter 的 metadata 现在会把外部 runtime 和条件性使用的 env 面暴露出来，方便 ClawHub 用户在安装前审查。各模式自己的必填项仍然以下面的示例和运行时配置校验为准；列出来的变量并不代表必须一次性全部填写。

## 先选模式，再填字段（推荐）

先确定模式，再只填写该模式的最小字段集。

- `read-only`
  - 只适合浏览。
  - 最小字段：`PREDICT_ENV`、`PREDICT_WALLET_MODE`，以及 mainnet 读取所需的 `PREDICT_API_KEY`。
- `eoa`
  - 适合直接用 signer 做交易，不经过 Predict Account overlay。
  - 最小字段：`PREDICT_ENV`、`PREDICT_WALLET_MODE=eoa`、`PREDICT_API_KEY`、`PREDICT_EOA_PRIVATE_KEY`。
- `predict-account + ERC_MANDATED_*`（推荐的带资金交易路径）
  - 适合 Predict Account 保持交易身份、Vault 负责供资的场景。
  - 先问一句：**你是否已经有 vault？**
  - **已有 vault** -> 最小字段：`PREDICT_ENV`、`PREDICT_WALLET_MODE=predict-account`、`PREDICT_API_KEY`、`PREDICT_ACCOUNT_ADDRESS`、`PREDICT_PRIVY_PRIVATE_KEY`、`ERC_MANDATED_MCP_COMMAND`、`ERC_MANDATED_CHAIN_ID`、`ERC_MANDATED_VAULT_ADDRESS`，以及可选的 `ERC_MANDATED_CONTRACT_VERSION`。
  - **还没有 vault** -> 默认建议先用 pure `mandated-vault` 路线部署或重建 vault，再回到 overlay。
- pure `mandated-vault`（推荐的治理 / control-plane 路径）
  - 适合 bootstrap、治理、vault-only 控制平面工作流。
  - 最小字段：`PREDICT_ENV`、`PREDICT_WALLET_MODE=mandated-vault`、`PREDICT_API_KEY`、`PREDICT_EOA_PRIVATE_KEY`、`ERC_MANDATED_MCP_COMMAND`、`ERC_MANDATED_CHAIN_ID`。

authority / executor / bootstrap 私钥属于按需追加的高级字段。只有当前工作流真的需要 vault 侧执行时，才应该继续展示它们。
对于 overlay onboarding，不要把完整 derivation tuple 当成第一屏默认答案；只有进入高级 / 手动恢复路径时才展示。

## 首次配置（推荐）

1. 安装 skill 并执行 `uv sync`。
2. 先选择一个启动模板：
    - `template.env` -> 无 secret 的本地 fixture 启动
    - `template.readonly.env` -> live 只读市场读取
    - `template.eoa.env` -> 直接私钥交易
    - `template.predict-account.env` -> Predict Account 交易
    - `template.predict-account-vault.env` -> Predict Account + vault
    - `template.mandated-vault.env` -> 内部/兼容 bootstrap 模板
3. 在 `~/.openclaw/skills/predictclaw/` 中把选中的模板复制为 `.env`。
4. 只填写该模式需要的最小变量集。
5. 先用 `uv run python scripts/predictclaw.py --help` 确认安装无误。
6. 再按模式做一次验证：
   - fixture 启动 -> `uv run python scripts/predictclaw.py markets trending`
   - live read-only -> `uv run python scripts/predictclaw.py markets trending`
   - `eoa` / `predict-account` -> `uv run python scripts/predictclaw.py wallet status --json`
   - `predict-account + vault` -> `uv run python scripts/predictclaw.py wallet status --json`

### 先选路线，再填配置

- `read-only` 只用于浏览。
- 当目标是保留 Predict Account 作为交易身份，并让 Vault 仅供资时，立即选择 `predict-account + ERC_MANDATED_*`。
- pure `mandated-vault` 是独立的 control-plane 路径，只适合你要创建新 Vault，或直接操作 Vault control-plane 流程时使用。

如果你想让 Vault 提供资金、但不改变交易身份，请从 `template.predict-account.env` 开始，使用 `PREDICT_WALLET_MODE=predict-account`。这就是“保留官方交易身份、让 Vault 仅供资”这个工作流的默认答案；除非你正在创建新 vault，或明确在处理 control-plane，否则不要先从 pure `wallet bootstrap-vault` 开始。

对于 overlay onboarding，先回答 vault 问题：

- **已有 vault** -> 先提供 `ERC_MANDATED_VAULT_ADDRESS`，再让 PredictClaw 解析或校验剩余 vault metadata。
- **还没有 vault** -> 默认先走 pure `mandated-vault` 的 bootstrap / redeploy。

不要把完整 derivation tuple 当成 overlay 的第一屏默认答案，除非用户明确进入高级 / 手动恢复路径。

## 启动模板

- `template.env` -> 最安全的首装入口；使用 `test-fixture` + `read-only`，不需要 secrets，也不会访问网络
- `template.readonly.env` -> live 市场读取；mainnet 的市场读取需要 PREDICT_API_KEY
- `template.eoa.env` -> EOA signer 路线，固定走主网 `https://api.predict.fun`
- `template.predict-account.env` -> Predict Account signer 路线，固定走主网 `https://api.predict.fun`
- `template.predict-account-vault.env` -> 面向用户的 Predict Account + vault 模板
- `template.mandated-vault.env` -> 仅用于内部/兼容 bootstrap 的模板

### 推荐的运行模型

- 面向用户的带资金交易，主推 `predict-account + vault`。
- 在这个模型里，Predict Account 仍然是交易身份和充值地址，Vault 只承担资金 / control-plane 角色。
- `mandated-vault` 不是独立模式，而是创建或准备 Vault 时使用的内部/bootstrap 兼容路径。

## 真实首装路径

### A. 先确认 CLI 能启动

```bash
uv sync
uv run python scripts/predictclaw.py --help
```

### B. 无 secret 的本地验证

复制 `template.env` 后运行：

```bash
uv run python scripts/predictclaw.py markets trending
```

这条路径使用 `test-fixture`，只证明 skill 能正确启动、加载配置并路由命令，不会访问 live API。
fixture 模式只认识仓库自带的本地 market ID（`123`、`456`、`789`、`101`、`202`）。如果你要查询真实 market ID，请先切到 live read-only 模板。

### C. live read-only 市场读取

复制 `template.readonly.env`，直接在主网上读取生产市场数据。

```bash
uv run python scripts/predictclaw.py markets trending
uv run python scripts/predictclaw.py market <market_id> --json
```

如果 mainnet 读取返回 `401 unauthorized`，通常表示 `PREDICT_API_KEY` 缺失或无效。

### D. signer 路线

wallet status 需要 signer 配置。它适合 `eoa` 和 `predict-account` 的下一步验证，但不是 `read-only` 的第一条命令。

### E. mode-first 最小字段规则

不要一开始就把完整 env 矩阵贴给用户。应该先问用户选择了哪个模式，再只给该模式的最小字段；authority / executor / bootstrap 这些高级密钥，只在所选流程真的需要 vault 执行时再补充。

## 配置示例

下面的片段全部使用 `.env` 写法。你可以直接写进 `~/.openclaw/skills/predictclaw/.env`（同一个已安装路径有时也会写成 `{baseDir}`），也可以在 shell 里 `export` 同名变量。

`OPENROUTER_API_KEY` 只在非 fixture 的 `hedge scan` / `hedge analyze` 中需要；market、wallet、buy 流程都不依赖它。

### bootstrap-safe fixture 模式

```dotenv
PREDICT_ENV=test-fixture
PREDICT_WALLET_MODE=read-only
```

这个模式只适合无 secret 的 CLI 验证与本地市场浏览，不会访问 live API。需要执行 wallet / trade 子命令时，请切换到 `eoa`、`predict-account` 或 `predict-account + vault`。

### live read-only 模式

```dotenv
PREDICT_ENV=mainnet
PREDICT_WALLET_MODE=read-only
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
```

mainnet 的市场读取需要 `PREDICT_API_KEY`。

### eoa 模式

```dotenv
PREDICT_ENV=mainnet
PREDICT_WALLET_MODE=eoa
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_EOA_PRIVATE_KEY=0xYOUR_EOA_PRIVATE_KEY
```

### predict-account 模式

```dotenv
PREDICT_ENV=mainnet
PREDICT_WALLET_MODE=predict-account
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_ACCOUNT_ADDRESS=0xYOUR_PREDICT_ACCOUNT
PREDICT_PRIVY_PRIVATE_KEY=0xYOUR_PRIVY_EXPORTED_KEY
```

### predict-account + vault 路线

用户-facing 的高级模式是 `predict-account + vault`，不是单独的 `mandated-vault` 模式。

先从规范模板开始：

```dotenv
PREDICT_ENV=mainnet
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_WALLET_MODE=predict-account
PREDICT_ACCOUNT_ADDRESS=0xYOUR_PREDICT_ACCOUNT
PREDICT_PRIVY_PRIVATE_KEY=0xYOUR_PRIVY_EXPORTED_KEY
ERC_MANDATED_VAULT_ADDRESS=0xYOUR_DEPLOYED_VAULT
ERC_MANDATED_VAULT_ASSET_ADDRESS=0xYOUR_ASSET
ERC_MANDATED_VAULT_AUTHORITY=0xYOUR_AUTHORITY
ERC_MANDATED_AUTHORITY_PRIVATE_KEY=0xYOUR_VAULT_AUTHORITY_KEY
ERC_MANDATED_MCP_COMMAND=erc-mandated-mcp
ERC_MANDATED_CONTRACT_VERSION=v0.3.0-agent-contract
ERC_MANDATED_CHAIN_ID=56
```

如果你已经有 Vault，就直接用这些变量绑定。

如果你还没有 Vault，就先运行 bootstrap helper。

### 内部 bootstrap 子流程（`mandated-vault`）

较旧的 `mandated-vault` 路径仍然作为内部/兼容 bootstrap 子流程存在，用来在返回 `predict-account + vault` 之前创建或准备 Vault。

```dotenv
PREDICT_ENV=mainnet
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_WALLET_MODE=mandated-vault
PREDICT_EOA_PRIVATE_KEY=0xYOUR_EOA_PRIVATE_KEY
ERC_MANDATED_MCP_COMMAND=erc-mandated-mcp
ERC_MANDATED_CHAIN_ID=56
```

PredictClaw 会使用固定产品 factory `0x6eFC613Ece5D95e4a7b69B4EddD332CeeCbb61c6`，从 `PREDICT_PRIVATE_KEY` 推导 signer 地址，先给出预览，再要求显式确认，最后在成功后把 deployed vault 地址和解析后的值回填到 `.env`。

执行 `--confirm` 时，PredictClaw 会自动为该 MCP 子进程打开 broadcast 开关，并桥接 bootstrap signer key。标准流程下，你不需要再手动设置 `ERC_MANDATED_ENABLE_BROADCAST=1` 或 `ERC_MANDATED_BOOTSTRAP_PRIVATE_KEY`，但它也不会再自动修改 `.env`。

先做预览：

```bash
uv run python scripts/predictclaw.py wallet bootstrap-vault --json
```

确认并广播：

```bash
uv run python scripts/predictclaw.py wallet bootstrap-vault --confirm --json
```

可选的部署 / 资金额度控制：

```dotenv
ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_TX=5000000000000000000
ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_WINDOW=10000000000000000000
ERC_MANDATED_FUNDING_WINDOW_SECONDS=3600
```

### 内部 bootstrap 兼容路径

如果你确实需要直接进入内部 bootstrap 路径，仍然保留以下 legacy/compatibility 变体：

#### 已知 deployed vault

```dotenv
PREDICT_ENV=mainnet
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_WALLET_MODE=mandated-vault
ERC_MANDATED_VAULT_ADDRESS=0xYOUR_DEPLOYED_VAULT
ERC_MANDATED_MCP_COMMAND=erc-mandated-mcp
ERC_MANDATED_CHAIN_ID=56
```

只有在你明确需要内部 bootstrap 路径直接绑定已部署 Vault 时，才使用这条兼容路径。

#### 完整 derivation tuple

```dotenv
PREDICT_ENV=mainnet
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_WALLET_MODE=mandated-vault
ERC_MANDATED_FACTORY_ADDRESS=0xYOUR_FACTORY
ERC_MANDATED_VAULT_ASSET_ADDRESS=0xYOUR_ASSET
ERC_MANDATED_VAULT_NAME=Mandated Vault
ERC_MANDATED_VAULT_SYMBOL=MVLT
ERC_MANDATED_VAULT_AUTHORITY=0xYOUR_AUTHORITY
ERC_MANDATED_VAULT_SALT=0xYOUR_SALT
ERC_MANDATED_MCP_COMMAND=erc-mandated-mcp
ERC_MANDATED_CONTRACT_VERSION=v0.3.0-agent-contract
ERC_MANDATED_CHAIN_ID=56
```

`ERC_MANDATED_EXECUTOR_PRIVATE_KEY` 是可选项。未设置时，PredictClaw 会在当前 Preflight MVP 合约路径中复用 `ERC_MANDATED_AUTHORITY_PRIVATE_KEY` 作为 executor signer。这是高级 / 手动恢复路径；如果预测到的 vault 还未部署，PredictClaw 仍然可以给出 preparation 信息和 `manual-only` 指引，但不会自动广播。

对于高级 override，`ERC_MANDATED_BOOTSTRAP_PRIVATE_KEY` 可以替换默认 bootstrap signer 解析规则，`ERC_MANDATED_ENABLE_BROADCAST` 可以显式强制 execute-mode gate 开或关。但标准 `--confirm` 路径里，PredictClaw 会自动把这两项桥接给 MCP 子进程。

### predict-account + vault overlay（推荐的高级资金路线）

```dotenv
PREDICT_ENV=mainnet
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_WALLET_MODE=predict-account
PREDICT_ACCOUNT_ADDRESS=0xYOUR_PREDICT_ACCOUNT
PREDICT_PRIVY_PRIVATE_KEY=0xYOUR_PRIVY_EXPORTED_KEY
ERC_MANDATED_VAULT_ADDRESS=0xYOUR_DEPLOYED_VAULT
ERC_MANDATED_MCP_COMMAND=erc-mandated-mcp
ERC_MANDATED_CONTRACT_VERSION=v0.3.0-agent-contract
ERC_MANDATED_CHAIN_ID=56
```

在 overlay 路线中，Predict Account remains 入金地址与交易身份，而 Vault 通过 MCP 支持的 session / asset-transfer 规划来为 Predict Account 提供资金。

当 Predict Account 继续作为入金/交易身份，而 Vault 只负责供资时，这就是正确路线。

如果你已经有已部署的 vault，这就是 overlay 的主路径：先提供 `ERC_MANDATED_VAULT_ADDRESS`，再让 PredictClaw 尽量自动解析其余 metadata。

如果你**还没有 vault**，默认建议先用 pure `mandated-vault` 路线部署或重建 vault，再回到 overlay。完整 derivation tuple（`ERC_MANDATED_FACTORY_ADDRESS`、`ERC_MANDATED_VAULT_ASSET_ADDRESS`、`ERC_MANDATED_VAULT_NAME`、`ERC_MANDATED_VAULT_SYMBOL`、`ERC_MANDATED_VAULT_AUTHORITY`、`ERC_MANDATED_VAULT_SALT`）保留为高级 / 手动路径，而不是默认首步。

只有在自动解析失败时，才再手动补充 `ERC_MANDATED_VAULT_ASSET_ADDRESS`、`ERC_MANDATED_VAULT_AUTHORITY`，以及 authority / executor 私钥这类高级字段。

可选的 overlay 限额：

```dotenv
ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_TX=5000000000000000000
ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_WINDOW=10000000000000000000
ERC_MANDATED_FUNDING_WINDOW_SECONDS=3600
```

这些变量会限制 Vault→Predict 的单笔额度、窗口累计额度和窗口时长。以 BSC mainnet USDT 为例：`5U = 5000000000000000000`，`10U = 10000000000000000000`。

## 钱包模式

PredictClaw 只对外暴露四种用户模式：

- `read-only` — 仅浏览市场数据，不允许 signer-backed 钱包动作。
- `eoa` — 直接私钥 signer 路径，用于钱包、交易和资金相关流程。
- `predict-account` — 使用 `PREDICT_ACCOUNT_ADDRESS` 与 `PREDICT_PRIVY_PRIVATE_KEY` 的官方 Predict Account 路径。
- `predict-account + vault` — Predict Account 保持交易身份，Vault 作为高级资金来源。

### 推荐路线

如果目标是保留 Predict Account 作为交易身份，同时让 Vault 仅供资，请使用：

- `PREDICT_WALLET_MODE=predict-account`
- 再叠加所需的 `ERC_MANDATED_*` overlay 输入（`predict-account + ERC_MANDATED_*`）

这是 Predict Account 交易身份工作流的默认路线。这样在 `wallet status --json` 与 `wallet deposit --json` 中会暴露 `vault-to-predict-account` 语义。

### 当用户问“充值地址是什么”时应如何回答

- 在 `predict-account + vault` 中，面向用户的默认回答应是：先走 Vault deposit flow。
- Predict Account 继续保持交易身份，后续再接受由 Vault 驱动的补资。
- 因此 `wallet deposit --json` / `wallet status --json` 需要区分：
  - 默认补资入口（`manualTopUpAddress` / `fundingAddress`）-> Vault
  - 交易身份 / 最终收款目标（`predictAccountAddress`、`tradingIdentityAddress`）-> Predict Account
- 只有在 plain `predict-account`（不带 vault overlay）时，才默认回答 Predict Account deposit 地址。

### 内部 bootstrap 说明

<<<<<<< HEAD
`mandated-vault` 是一个高级显式 opt-in 模式，应把它视为独立的 control-plane 路径，而不是 Predict Account 交易的平级答案。

内置 factory 默认值和成功后返回的手动 env block，只是在 pure bootstrap 场景里提供便利，并不能替代部署时 signer 输入，也不能替代 `predict-account` overlay 所需的专用 env。

对于默认 pure bootstrap 流程，用户只需要提供 EOA signer、部署手续费资金，以及可选的额度控制。PredictClaw 会处理固定 factory、预览、确认，并在成功后返回手动 env block。

pure `mandated-vault` 不提供 predict.fun trading parity。`wallet approve`、`wallet withdraw`、`buy`、`positions`、`position`、`hedge scan`、`hedge analyze` 都会 fail closed，并返回 `unsupported-in-mandated-vault-v1`。
=======
`mandated-vault` 仍然在运行时里存在，但只作为内部/兼容 bootstrap 子流程，**不是独立模式**。它的职责是在回到 `predict-account + vault` 路线前创建或准备 Vault。
>>>>>>> 7e22c30 (docs: reframe vault onboarding as predict-account plus vault)

### 常见配置错误

- `read-only` 只能浏览市场；不要直接跑 signer-backed 的 wallet / trade 命令。
- `wallet status` 需要 signer 配置；在 `read-only` 下请先跑 `markets trending` 或 `market <id> --json`。
- mainnet 的市场读取需要 `PREDICT_API_KEY`；没配会在配置阶段直接失败，配错通常会返回 `401 unauthorized`。
- `eoa` 必须配置 `PREDICT_EOA_PRIVATE_KEY`，并且不能混用 Predict Account 或 mandated-vault 输入。
- `predict-account` 必须同时配置 `PREDICT_ACCOUNT_ADDRESS` 和 `PREDICT_PRIVY_PRIVATE_KEY`。
- `mainnet` 必须配置 `PREDICT_API_KEY`。
- pure `mandated-vault` 需要一个可用的 `ERC_MANDATED_MCP_COMMAND`；overlay 模式的默认路径是先提供显式 `ERC_MANDATED_VAULT_ADDRESS`，再由系统尽量自动解析 asset 与 authority，只有自动解析失败时才升级到手动字段。

## `ERC_MANDATED_MCP_COMMAND` / `@erc-mandated/mcp` 依赖说明

`ERC_MANDATED_MCP_COMMAND` 是 PredictClaw 与 mandated-vault MCP runtime 通信时使用的启动命令，默认值为 `erc-mandated-mcp`。

它在实际工作流中的作用有三层：

1. **Vault 预测与准备** — 当只有 derivation tuple 时，用 MCP 预测 vault 地址并生成准备信息。
2. **Vault bootstrap 执行** — 通过 `vault_bootstrap` 支持 pure mandated-vault 的预览与确认部署。
3. **Vault overlay 编排** — 在 overlay 模式下暴露 `vault-to-predict-account` 路由、funding-policy 上下文与会话规划。
4. **控制面安全边界** — 当 MCP 不存在或不可用时，PredictClaw 会显式 fail closed，而不是静默猜测。

如果你的环境通过类似 `@erc-mandated/mcp` 的包来提供这套 runtime，那么你真正需要给 PredictClaw 配置的是该 runtime 对应的启动命令，也就是 `ERC_MANDATED_MCP_COMMAND`。PredictClaw 对外公开的契约是“命令入口”，而不是某个固定的包管理器依赖。

默认安全路径可以运行：

```bash
uv run python scripts/predictclaw.py setup mandated-mcp
```

PredictClaw 在默认路径里只会检测 `erc-mandated-mcp` launcher 是否可用。它不会全局安装包，也不会自动修改 `.env`。请先自行安装外部 `erc-mandated-mcp` runtime，然后再手动设置 `ERC_MANDATED_MCP_COMMAND`。

MCP orchestrates transport and preparation; the vault contract policy authorizes what the vault can actually execute.

## 命令面

```bash
uv run python scripts/predictclaw.py markets trending
uv run python scripts/predictclaw.py markets search "election"
uv run python scripts/predictclaw.py market 123 --json
uv run python scripts/predictclaw.py wallet status --json
uv run python scripts/predictclaw.py wallet approve --json
uv run python scripts/predictclaw.py wallet deposit --json
uv run python scripts/predictclaw.py wallet bootstrap-vault --json
uv run python scripts/predictclaw.py wallet bootstrap-vault --confirm --json
uv run python scripts/predictclaw.py wallet withdraw usdt 1 0xb30741673D351135Cf96564dfD15f8e135f9C310 --json
uv run python scripts/predictclaw.py wallet withdraw bnb 0.1 0xb30741673D351135Cf96564dfD15f8e135f9C310 --json
uv run python scripts/predictclaw.py buy 123 YES 25 --json
uv run python scripts/predictclaw.py positions --json
uv run python scripts/predictclaw.py position pos-123-yes --json
uv run python scripts/predictclaw.py hedge scan --query election --json
uv run python scripts/predictclaw.py hedge analyze 101 202 --json
```

## 核心工作流说明

- `wallet status` 会报告 signer mode、funding guidance、余额和 approval readiness。
- `wallet deposit` 是一个资金引导命令：在 `predict-account + vault` 中，它会把 Vault deposit flow 作为默认补资入口，同时继续分开展示 Predict Account 收款/交易身份和 orchestration vault 元数据，并给出可接受资产（`BNB`、`USDT`）。
- `wallet bootstrap-vault` 是 pure mandated-vault 的预览 / 确认入口。
- 默认 bootstrap 流程会使用固定 factory `0x6eFC613Ece5D95e4a7b69B4EddD332CeeCbb61c6`，并在确认成功后返回可手动复制的 env block。
- `wallet redeem-vault --preview --json` 会预检 vault share 赎回，并返回 `redeemableNow`、`blockingReason` 以及像 `ERC4626ExceededMaxRedeem` 这样的合约错误。
- `wallet withdraw` 在尝试执行转账逻辑前会先验证目标地址 checksum、金额为正、余额充足以及 BNB gas 余量。
- 在 fixture 模式下，withdraw 会返回确定性的占位 tx hash，而不会触链。
- 在 `predict-account + ERC_MANDATED_*` overlay 中，`wallet status` / `wallet deposit` 会暴露：
  - `manualTopUpAddress`
  - `tradingIdentityAddress`
  - `predictAccountAddress`
  - `tradeSignerAddress`
  - `orchestrationVaultAddress`
  - `vaultAddress`
  - `fundingRoute = vault-to-predict-account`
- 默认补资入口是 Vault deposit flow。
- Predict Account 继续是交易身份 / 下单账户。
- 内部 orchestration 的最终资金目标仍然是 Predict Account，但用户-facing 的补资入口是 Vault。
- 可选的 Vault funding-policy 环境变量允许你限制 Vault→Predict 转账的单笔额度、窗口累计额度和窗口时长。
- 与 vault 相关的 JSON 现在还会提供 `vaultAuthority`、`vaultExecutor`、`bootstrapSigner`、`allowedTokenAddresses`、`allowedRecipients`，方便用户和 OpenClaw 直接理解权限边界。
- 这些 funding-policy 金额使用 raw token units；以 BSC mainnet USDT（18 decimals）为例：`5 U = 5000000000000000000`，`10 U = 10000000000000000000`。
- 如果 Predict Account 已有足够余额，`buy` 会继续走官方 Predict Account 下单路径。
- 如果余额不足，`buy` 会以确定性的 `funding-required` 引导失败，并提示用户查看 `wallet deposit --json`；当前本地 signer 上下文不会自动执行 vault 资金腿。

### 赎回预检

在任何真实赎回动作之前，先使用 preview-only 预检：

```bash
uv run python scripts/predictclaw.py wallet redeem-vault --share-token 0x4a88c1c95d0f59ee87c3286ed23e9dcdf4cf08d7 --holder 0x7df0ba782D85B93266b595d496088ABFAc823950 --all --preview --json
```

这个命令会读取 share token、底层资产、`maxRedeem`、`maxWithdraw` 和一次模拟赎回调用，并输出 `redeemableNow`、`blockingReason`、`contractError`。当前版本故意保持 `preview-only`，不会广播真实赎回交易。

## 运行模式

- `test-fixture` — 使用本地 JSON fixture 和确定性的 wallet / hedge / trade 行为，适合开发、集成测试、CI，以及无 secret 的首装验证。
- `mainnet` — 需要 `PREDICT_API_KEY`，即使只是市场读取也应视为真实交易环境。
- `testnet` — 仍然支持，但只适合你显式选择非主网环境时使用；它不再是打包模板或首装引导里的默认路径。

## 环境变量

| 变量 | 作用 |
| --- | --- |
| `PREDICT_STORAGE_DIR` | 本地 journal 与持仓存储 |
| `PREDICT_ENV` | 代码默认是 `mainnet`；`template.env` 刻意以 `test-fixture` 做 bootstrap；可选 `mainnet`、`testnet`、`test-fixture` |
| `PREDICT_WALLET_MODE` | 显式模式覆盖：`read-only`、`eoa`、`predict-account`、`mandated-vault` |
| `PREDICT_API_BASE_URL` | 可选 REST base override；打包的 live 模板会直接固定成 `https://api.predict.fun`，留空时才按环境自动选择 |
| `PREDICT_API_KEY` | mainnet 认证后的 predict.fun API 访问；mainnet 市场读取与交易都需要它 |
| `PREDICT_EOA_PRIVATE_KEY` | EOA 交易与资金路径 |
| `PREDICT_ACCOUNT_ADDRESS` | Predict Account 智能钱包地址 |
| `PREDICT_PRIVY_PRIVATE_KEY` | Predict Account 模式下的 Privy 导出 signer |
| `ERC_MANDATED_VAULT_ADDRESS` | 已知部署好的 mandated vault 显式地址 |
| `ERC_MANDATED_FACTORY_ADDRESS` | 当未提供显式 vault 地址时，用于预测 vault 的 factory 地址 |
| `ERC_MANDATED_VAULT_ASSET_ADDRESS` | mandated-vault 预测 / create 准备时使用的 ERC-4626 资产 |
| `ERC_MANDATED_VAULT_NAME` | mandated-vault 预测 / create 准备时使用的 Vault 名称 |
| `ERC_MANDATED_VAULT_SYMBOL` | mandated-vault 预测 / create 准备时使用的 Vault 符号 |
| `ERC_MANDATED_VAULT_AUTHORITY` | Authority 地址，以及手动 create-vault 准备中的 `from` 地址 |
| `ERC_MANDATED_VAULT_SALT` | 用于 vault 预测 / create 准备的确定性 salt |
| `ERC_MANDATED_AUTHORITY_PRIVATE_KEY` | 当前单密钥 MVP 合约路径的 Preflight Vault signer key |
| `ERC_MANDATED_EXECUTOR_PRIVATE_KEY` | 可选的 executor signer；未设置时回退到 `ERC_MANDATED_AUTHORITY_PRIVATE_KEY` |
| `ERC_MANDATED_BOOTSTRAP_PRIVATE_KEY` | 可选的 execute-mode bootstrap signer override；未设置时，PredictClaw 会依次回退到 `PREDICT_EOA_PRIVATE_KEY`、`ERC_MANDATED_AUTHORITY_PRIVATE_KEY` |
| `ERC_MANDATED_ENABLE_BROADCAST` | 可选的 execute-mode MCP gate override；`wallet bootstrap-vault --confirm` 默认会自动桥接成 `1`，除非你显式覆盖 |
| `ERC_MANDATED_MCP_COMMAND` | MCP 启动命令（默认 `erc-mandated-mcp`） |
| `ERC_MANDATED_CONTRACT_VERSION` | 透传给 mandated-vault MCP client 的版本号 |
| `ERC_MANDATED_CHAIN_ID` | MCP bridge 的可选显式链选择 |
| `ERC_MANDATED_ALLOWED_ADAPTERS_ROOT` | 可选的 32-byte hex `allowedAdaptersRoot`，用于 Vault 执行 mandate；当前单密钥 MVP / PoC 路径默认 `0x11…11` |
| `ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_TX` | 可选的 Vault→Predict funding-policy `maxAmountPerTx`（raw token units） |
| `ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_WINDOW` | 可选的 Vault→Predict funding-policy `maxAmountPerWindow`（raw token units） |
| `ERC_MANDATED_FUNDING_WINDOW_SECONDS` | 可选的 Vault→Predict funding-policy `windowSeconds` |
| `OPENROUTER_API_KEY` | hedge analysis 模型访问 |
| `PREDICT_MODEL` | OpenRouter 模型覆盖 |
| `PREDICT_SMOKE_ENV` | 启用 smoke suite |
| `PREDICT_SMOKE_API_BASE_URL` | 可选 smoke REST base override |
| `PREDICT_SMOKE_PRIVATE_KEY` | 启用 signer/JWT smoke 检查 |
| `PREDICT_SMOKE_ACCOUNT_ADDRESS` | Predict Account smoke 模式 |
| `PREDICT_SMOKE_PRIVY_PRIVATE_KEY` | Predict Account smoke signer |
| `PREDICT_SMOKE_API_KEY` | smoke REST auth |

## Hedge 说明

- Hedge analysis 通过 OpenRouter 的纯 HTTP JSON 合约实现。
- `OPENROUTER_API_KEY` 只在非 fixture 的 hedge analysis 中需要。
- fixture 模式使用确定性的关键字 / 配对逻辑，因此 CLI 与 integration tests 可以保持 secret-free。
- 当前公开命令面仍是 PolyClaw 对齐加上 `wallet deposit` / `wallet withdraw`；v1 仍没有公开 `sell` 命令。

## 项目结构

- `scripts/predictclaw.py` — 顶层 CLI router
- `scripts/` — 各命令入口脚本
- `lib/` — config、auth、REST、wallet、funding、trade、positions、hedge 与 MCP bridge 逻辑
- `tests/` — Python skill package 的 unit、integration、smoke 覆盖

## 验证层

```bash
# unit + command tests
uv run pytest -q

# fixture-backed end-to-end CLI checks
uv run pytest tests/integration -q

# env-gated smoke (passes or skips)
uv run pytest tests/smoke/test_testnet_smoke.py -q
```

## 安全说明

- 不要把 fixture 模式视作 funded-wallet 行为的证明。
- 不要仅凭 testnet 或 mainnet 文档就假设 live liquidity 一定存在。
- 自动化密钥应只保留有限资金。
- Withdraw 命令是公开能力；虽然转账前会做验证，但实际操作风险仍由用户承担。
- `predict-account + ERC_MANDATED_*` 是推荐的高级交易路线：Vault 给 Predict Account 提供资金，但 Predict Account 保持官方订单模型。
- 显式 vault 与 predicted vault 语义：`ERC_MANDATED_VAULT_ADDRESS` 直接指向已有 vault；否则 PredictClaw 会使用 derivation tuple 通过 MCP 预测 vault 地址。
- 如果 predicted vault 尚未部署，`wallet deposit` 可以返回包含 `predictedVault`、交易摘要和 `manual-only` 的 create-vault preparation 信息，但不会自动广播。
- pure `mandated-vault` 不提供 predict.fun trading parity，并会对不支持的路径以 `unsupported-in-mandated-vault-v1` 明确 fail closed。
