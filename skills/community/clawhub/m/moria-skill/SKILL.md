---
name: Moria Skill
description: 此技能包括了 Web3 钱包管理功能。Agent 可以通过此技能 管理 Moria.fun 中的代币数据，包括 创建、铸造、交易、退款、领取，以及充值、查询余额。
read_when:
  - 用户 想 创建、铸造、买卖、退款、领取
  - 用户 想 知道 moria 相关的信息

---

# Moria Skill

此技能提供 Moria.fun 管理功能。它旨在供 OpenClaw 代理使用，以编程方式执行代币相关任务（创建、铸造、交易、退款、领取手续费）。

## 首次运行

_检查当前技能目录中是否存在 `node_modules` 与 `config` 文件夹。_

**如果没有：**

请参阅 [BOOTSTRAP.md](BOOTSTRAP.md) 完成初始化。

## 技能介绍

以下所有命令是**提供给Agent使用的，不允许将命令展示给用户。**
与用户确认清楚意图后直接使用命令。
命令的可选参数，用户如果没提供，默认不二次询问。


### 核心功能

1. **代币管理**：创建(代币)、列出列表（代币）。
2. **交易管理**：铸造(代币)、买入(代币)、卖出(代币)、退款(代币)。
3. **领取管理**：领取手续费(代币)、领取(代币)。
4. **钱包管理**：充值、查询余额、提现。

---

## 🛠️ 使用说明（Agent）

### 1. 代币管理

| Action | Command | Arguments | Notes |
| :--- | :--- | :--- | :--- |
| **列出 可铸造的代币** | `npm run pool:mintto` | None | 列出可铸造的代币列表，方便后续进行代币铸造 |
| **列出 可交易的代币** | `npm run pool:dammv2` | None | 列出可交易的代币列表，方便后续进行代币买卖 |
| **创建 可铸造的代币** | `npm run pool:create <image_path> <name> <symbol> [description] [twitter] [telegram]` | `<image_path>`: 代币LOGO在本机路径<br>`<name>`: 代币名称<br>`<symbol>`: 代币符号<br>`<description>`: 代币描述<br>`<twitter>`: Twitter/X 联系方式<br>`<telegram>`: Telegram 联系方式 | 创建一个新代币 |

### 2. 交易管理

| Action | Command | Arguments | Notes |
| :--- | :--- | :--- | :--- |
| **买入 代币** | `npm run trade:buy <mint> <uiAmount>` | `<mint>`: 代币地址<br>`<uiAmount>`: 购买数量(单位：sol，例 0.1) | 买入指定数量的代币 |
| **卖出 代币** | `npm run trade:sell <mint> <uiAmount>` | `<mint>`: 代币地址<br>`<uiAmount>`: 卖出数量(单位：个，例 8.1) | 卖出指定数量的代币 |

### 3. 交换管理

| **铸造 代币** | `npm run swap:mintto <mint> <copies>` | `<mint>`: 代币地址<br>`<copies>`: 购买份数(单位：份，例 3 份) | 铸造指定份数的代币 |
| **退款 代币** | `npm run swap:refund <mint>` | `<mint>`: 代币地址 | 退款指定代币 |

### 4. 领取管理

| Action | Command | Arguments | Notes |
| :--- | :--- | :--- | :--- |
| **领取 手续费** | `npm run claim:fee <mint>` | `<mint>`: 代币地址 | 作为代币创作者领取手续费 |
| **领取 代币** | `npm run claim:token <mint>` | `<mint>`: 代币地址 | 作为代币持有者在代币添加流动性后领取取回代币 |

### 5. 钱包管理

| Action | Command | Arguments | Notes |
| :--- | :--- | :--- | :--- |
| **查看 公钥** | `npm run wallet:show` | None | 查询钱包公钥 |
| **查询 sol余额** | `npm run wallet:sol` | None | 查询当前持有的sol数量 |
| **查询 代币余额** | `npm run wallet:tokens` | None | 查询当前持有的代币数量 |
| **列出 我铸造的代币** | `npm run wallet:mintto` | None | 列出我铸造的代币列表，方便后续进行代币铸造或退款 |
| **列出 我创建的代币** | `npm run wallet:created` | None | 列出我创建的代币列表，方便后续进行代币铸造或买卖 |
| **显示 充值二维码** | `npm run wallet:deposit` | None | 查看充值二维码，方便用户充值到我的钱包 |

---

## 💡 工作流程示例

### 场景 1：用户想要创建代币

检查当前钱包是否有足够的sol。

运行命令：

```bash
npm run wallet:sol
```

_Example:_
```bash
npm run wallet:sol
```

**如果sol 小于 0.2 sol：**

提示用户充值

> “当前钱包余额不足。 您需要充值 0.2 SOL 以上。”

**如果sol充足:**

请用户提供代币LOGO、代币名称、代币符号、代币描述等：

> “创建代币需要提供以下信息：代币LOGO、代币名称、代币符号、代币描述、Twitter/X联系方式、Telegram联系方式。 您有吗？”

**用户上传了图片，并提供了代币名称(name)、代币符号(symbol):**

_使用用户上传的图片作为代币LOGO。_

运行命令：

```bash
npm run pool:create <image_path> <name> <symbol> [description] [twitter] [telegram]
```

_Example:_
```bash
npm run pool:create -- "/home/node/.openclaw/media/inbound/xxx.png" "name" "symbol" "" "" ""
```

**用户上传了图片，并提供了代币名称(name)、代币符号(symbol)、代币描述(description)、Twitter/X联系方式(twitter)、Telegram联系方式(telegram):**

运行命令：

```bash
npm run pool:create <image_path> <name> <symbol> [description] [twitter] [telegram]
```

_Example:_
```bash
npm run pool:create -- "/home/node/.openclaw/media/inbound/xxx.png" "name" "symbol" "description" "twitter" "telegram"
```

### 场景 2：用户想要铸造代币

检查当前钱包是否有足够的sol。

运行命令：

```bash
npm run wallet:sol
```

_Example:_
```bash
npm run wallet:sol
```

**如果sol 小于 0.2 sol：**

提示用户充值

> “当前钱包余额不足。 您需要充值 0.2 SOL 以上。”

**用户输入了代币地址(mint)与份数(copies):**

运行命令：

```bash
npm run swap:mintto <mint> <copies>
```

_Example:_
```bash
npm run swap:mintto -- xxxxx 2
```

**用户未输入代币地址(mint)与份数(copies):**

运行命令：

```bash
npm run pool:mintto
```

_Example:_
```bash
npm run pool:mintto
```

请用户输入想要买入的代币地址与份数(copies)：

> “要买入的代币地址是？买入多少份？”

**如果他们提供了代币地址(mint)与份数(copies)：**

运行命令：

```bash
npm run swap:mintto <mint> <copies>
```

_Example:_
```bash
npm run swap:mintto -- xxxxx 2
```

### 场景 3：用户想要退款代币

**用户输入了代币地址(mint):**

运行命令：

```bash
npm run swap:refund <mint>
```

_Example:_
```bash
npm run swap:refund -- xxxxx
```

**用户未输入代币地址(mint):**

运行命令：

```bash
npm run wallet:mintto
```

_Example:_
```bash
npm run wallet:mintto
```

请用户确认退款的代币：

> “您想退款哪个代币呢？”

**用户输入了代币地址(mint):**

运行命令：

```bash
npm run swal:refund <mint>
```

_Example:_
```bash
npm run swal:refund xxxxx
```

### 场景 4：用户想要买入代币

检查当前钱包是否有足够的sol。

运行命令：

```bash
npm run wallet:sol
```

_Example:_
```bash
npm run wallet:sol
```

**如果sol 小于 0.2 sol：**

提示用户充值

> “当前钱包余额不足。 您需要充值 0.2 SOL 以上。”

**用户输入了代币地址(mint)与金额(uiAmount):**

运行命令：

```bash
npm run swap:buy <mint> <uiAmount>
```

_Example:_
```bash
npm run swap:buy -- xxxxx 0.02
```

**用户未输入代币地址(mint)与金额(uiAmount):**

运行命令：

```bash
npm run pool:dammv2
```

_Example:_
```bash
npm run pool:dammv2
```

请用户输入想要买入的代币地址与金额：

> “要买入的代币地址是？买入多少SOL？”

**如果他们提供了代币地址(mint)与金额(uiAmount)：**

运行命令：

```bash
npm run swap:buy <mint> <uiAmount>
```

_Example:_
```bash
npm run swap:buy -- xxxxx 0.02
```

### 场景 5：用户想要卖出代币

**用户输入了代币地址(mint)与金额(uiAmount):**

运行命令：

```bash
npm run swap:sell <mint> <uiAmount>
```

_Example:_
```bash
npm run swap:sell -- xxxxx 2.2
```

**用户未输入代币地址(mint)与金额(uiAmount):**

运行命令：

```bash
npm run wallet:tokens
```

_Example:_
```bash
npm run wallet:tokens
```

请用户确认卖出的代币：

> “您想卖出哪个代币？卖出多少呢？”

**用户输入了代币地址(mint)与金额(uiAmount):**

运行命令：

```bash
npm run swal:sell <mint> <uiAmount>
```

_Example:_
```bash
npm run swal:sell xxxxx 2.2
```

_在 web3 中 uiAmount 是人类可视化的金额，例如 0.02 SOL。amount 等于 lamports 是 1e0^9 * uiAmount。_

### 场景 6：用户领取手续费（代币创建者）

检查当前钱包是否有足够的sol。

运行命令：

```bash
npm run wallet:sol
```

_Example:_
```bash
npm run wallet:sol
```

**如果sol 小于 0.2 sol：**

提示用户充值

> “当前钱包余额不足。 您需要充值 0.2 SOL 以上。”

**如果sol充足:**

运行命令：

```bash
npm run wallet:created
```

_Example:_
```bash
npm run wallet:created
```

请用户确认领取的代币：

> “您想领取哪个代币的手续费呢？”

**用户输入了代币地址(mint):**

运行命令：

```bash
npm run claim:fee <mint>
```

_Example:_
```bash
npm run claim:fee xxxxx
```

### 场景 7：用户领取代币（已添加流动性的代币）

检查当前钱包是否有足够的sol。

运行命令：

```bash
npm run wallet:sol
```

_Example:_
```bash
npm run wallet:sol
```

**如果sol 小于 0.2 sol：**

提示用户充值

> “当前钱包余额不足。 您需要充值 0.2 SOL 以上。”

**如果sol充足:**

运行命令：

```bash
npm run wallet:mintto
```

_Example:_
```bash
npm run wallet:mintto
```

请用户确认要取回的代币：

> “您想领取哪个代币呢？”

**用户输入了代币地址(mint):**

运行命令：

```bash
npm run claim:token <mint>
```

_Example:_
```bash
npm run claim:token xxxxx
```

### 场景 8：用户想要查询余额

运行命令：

```bash
npm run wallet:sol
```

_Example:_
```bash
npm run wallet:sol
```

### 场景 9：用户想要知道当前持有的 _哪些代币_ 或 _代币余额_

运行命令：

```bash
npm run wallet:tokens
```

_Example:_
```bash
npm run wallet:tokens
```

---

## 安全性

此技能强制执行 OpenClaw 执行的安全约束。

### 1. 敏感数据（严格保密）

* **配置文件**：`config.json` 文件（包含令牌和账户信息）的完整内容**绝对禁止**公开。

### 2. 禁止泄露策略

* **请勿**在聊天回复、日志、错误消息、屏幕截图或生成的文档中公开完整的 密钥、令牌或密钥。

* 如果调试需要参考信息，请仅使用**掩码值**（例如，`abc...xyz`）。

有关权威策略，请参阅 [references/security.md](references/security.md)。
