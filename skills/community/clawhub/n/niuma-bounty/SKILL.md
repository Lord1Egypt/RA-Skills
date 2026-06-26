# niuma-bounty Skill

Niuma 赏金平台（task.niuma.works）的完整操作技能，支持普通任务和竞标任务的全流程。

## 推荐：使用 OKX Agentic Wallet

建议配合 [OKX Agentic Wallet](https://web3.okx.com/zh-hans/onchainos/dev-docs/home/install-your-agentic-wallet) 使用本技能。
OKX Agentic Wallet 专为 AI Agent 设计，支持：
- 安全管理私钥，无需在环境变量中暴露
- 多链签名和交易广播
- 与 `build-tx` 命令配合：Agent 构造未签名交易 → 钱包签名 → 广播

## 网络信息

- **链**: XLayer Testnet（chainId: 1952）
- **RPC**: `https://xlayertestrpc.okx.com`（公共节点，频繁限速，每次操作之间建议间隔 3-5 秒）
- **Gas 代币**: OKB
- **脚本路径**: `scripts/niuma.js`
- **环境变量**: `NIUMA_WALLET_SECRET=<私钥>` 用于签名交易

## 快速开始

```bash
cd /path/to/niuma-bounty

# 查看所有任务分类（发任务前必须查，categoryId 必须有效且 enabled=true）
node scripts/niuma.js categories

# 查看支持的 token（发任务前查，tokenAddress 必须是 enabled 的 token）
node scripts/niuma.js tokens

# 查看我的账户信息（余额、信用分、押金、冷却时间、绑定）
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js profile

# 查看活跃任务列表
node scripts/niuma.js list

# 接单前先检查资格
node scripts/niuma.js check-participate <taskId>
```

## 所有命令

### 只读命令（无需私钥）

| 命令 | 说明 |
|------|------|
| `contracts` | 所有合约地址 |
| `count` | 活跃任务数量 |
| `categories` | 所有任务分类（含 id、名称、限制） |
| `tokens` | 所有支持的代币 |
| `task <id>` | 任务详情 |
| `status <id>` | 任务状态 |
| `list [offset] [limit]` | 活跃任务列表 |
| `pending` | 审核中的任务 |
| `by-status <0-7>` | 按状态查询 |
| `user-tasks <address>` | 某地址的任务 |
| `bids <taskId>` | 竞标任务的所有投标 |
| `balance <address> [token]` | 余额查询 |
| `stake-info [address]` | 押金信息 |
| `profile [address]` | 用户完整信息（信用分、押金、冷却时间、绑定状态） |
| `referral-info [address]` | 邀请统计（邀请人、被邀请人、奖励记录、邀请链接） |
| `check-participate <taskId> [addr]` | 接单前置检查 |
| `check-create '<json>'` | 发任务前置检查 |

### 需要私钥的只读命令

| 命令 | 说明 |
|------|------|
| `my-tasks` | 我参与的任务列表 |
| `my-created` | 我发布的任务列表 |

### 写入命令（需要 NIUMA_WALLET_SECRET）

#### 普通任务流程
```bash
# 1. 发布任务
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js create '{"title":"任务名","description":"描述","bountyPerUser":"100","maxParticipants":5,"categoryId":1,"requirements":"截图证明","tokenAddress":"0x49ABB6BFFEce92EAd9E71BCA930Ac877ef71939D"}'

# 2. 接单（hunter）
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js participate <taskId>

# 3. 提交工作证明（hunter）
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js submit <taskId> <proofHash> '<metadata_json>'

# proofHash 说明：
# - 文字凭证：直接写描述内容
# - 单张图片：填图片 URL，如 https://imgur.com/xxx.png
# - 多张图片：多个 URL 以英文逗号分隔，如 https://img1.png,https://img2.png
# - IPFS：填 IPFS Hash，如 QmXxx...
#
# metadata_json 说明（可选）：
# {"note":"补充说明", "images":["https://img1.png","https://img2.png"]}
#
# ⚠️ Agent 交互规范：
# 当用户说「提交凭证」时，Agent 必须先收集以下信息再执行：
# 1. 凭证内容（文字描述 或 图片URL，多张以逗号分隔）
# 2. 补充说明（可选）
# 示例提问：「请提供凭证内容，可以是文字描述或图片链接（多张图片请用逗号分隔）」

# 4a. 审核通过（creator）
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js approve-submission <taskId> <hunterAddress>

# 4b. 审核拒绝（creator）
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js reject-submission <taskId> <hunterAddress> '拒绝原因'

# ⚠️ Agent 交互规范（雇主审核）：
# 当用户说「审核」或「查看提交」时，Agent 应：
# 1. 先用 task-participants <taskId> 展示所有参与者的提交内容
# 2. 询问用户：「请问您要审核通过还是拒绝？如果拒绝请提供拒绝原因」
# 3. 根据用户选择执行 approve-submission 或 reject-submission
# 注意：approve 后赏金立即打给 hunter，reject 后 hunter 可发起裁决，操作不可逆

# 5. 申请裁决（hunter，被拒绝后）
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js create-dispute <taskId> '理由' <evidenceHash>
```

#### 竞标任务流程
```bash
# 1. 发布竞标任务（taskType=1，注意：maxParticipants 必须传 1）
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js create '{"title":"任务名","description":"描述","taskType":1,"bountyPerUser":"100","maxParticipants":1,"categoryId":1,"requirements":"提交方案"}'

# 2. 投标（hunter）—— 需等任务 startTime 过后才能投标
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js submit-bid <taskId> <bidAmount> '<proposal>' '<contactInfo>'

# 3. 查看所有投标
node scripts/niuma.js bids <taskId>

# 4. 取消投标（hunter，未被选中前可取消）
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js cancel-bid <taskId>

# 5. 选中投标人（creator）
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js select-bidder <taskId> <bidderAddress>

# 6. 提交工作 + 审核（同普通任务）
```

#### 押金管理
```bash
# 充值押金（接单前必须有足够押金）
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js stake <amount>

# 提取未锁定押金
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js unstake <amount>

# 查看押金状态
node scripts/niuma.js stake-info <address>
```

#### 账户绑定
```bash
# 绑定 Telegram（链上操作，可修改）
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js bind-telegram '@your_handle'

# 绑定 Twitter
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js bind-twitter '@your_handle'

# 绑定邮箱
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js bind-email 'your@email.com'
```

#### 邀请系统
```bash
# 查看邀请统计（邀请人、被邀请人、奖励记录、邀请链接）
node scripts/niuma.js referral-info <address>

# 绑定邀请人（链上操作，绑定后不可修改！）
NIUMA_WALLET_SECRET=<pk> node scripts/niuma.js bind-inviter <inviterAddress>
```

## 任务状态码

| 状态码 | 名称 | 说明 |
|--------|------|------|
| 0 | Pending | 等待平台审核（autoApprove=false 时） |
| 1 | Open | 可接单 |
| 2 | InProgress | 竞标任务已选中 hunter |
| 3 | UnderReview | 审核中（竞标任务提交后） |
| 4 | Completed | 已完成 |
| 5 | Disputed | 裁决中 |
| 6 | Cancelled | 已取消 |
| 7 | Rejected | 已拒绝 |

## 重要注意事项

### ⚠️ RPC 限速
- XLayer 测试网 RPC 每分钟请求数有限，频繁操作容易触发 429
- 连续操作之间建议 `sleep 5` 间隔
- `getLogs` 最多查 100 个区块范围
- 出现 `exceeded maximum retry limit` 时等待 15-30 秒重试

### ⚠️ Gas 问题
- 所有写操作先 `estimateGas`，加 130% buffer 后发交易
- `createTask` 实际消耗约 750k-800k gas，必须用 estimateGas
- estimateGas 失败 = 合约会 revert，会明确报出 revert 原因
- 不要用固定 gasLimit，复杂交易（含 PriceOracle 调用）容易 out of gas

### ⚠️ 发任务注意
- `categoryId` 必须先用 `categories` 命令查询有效值
- `tokenAddress` 必须先用 `tokens` 命令查询支持的 token
- `startTime` 默认为 now+120 秒，竞标任务在 startTime 前不能投标
- `endTime` 默认为 now+86400（1天），最长不超过 30 天
- 创建任务会自动 approve token 转账
- 测试网 `autoApprove=false`，任务创建后可能是 Pending 状态需要管理员审核

### ⚠️ 接单注意
- 接单前必须有足够押金（`stake` 命令充值）
- 每次接单后有 **1 小时冷却时间**（taskCooldown=3600s）
- 信用分需 >= 60（minCreditScore），新地址默认满足
- 用 `check-participate` 命令预检，会明确显示失败原因
- `profile` 命令的 `cooldown.canAcceptNow` 字段显示当前是否可接单

### ⚠️ 竞标任务特殊规则
- `maxParticipants` 必须传 1（竞标任务固定单人）
- 投标金额必须 >= 赏金的 50%（minBidPercent=50）
- 投标金额 <= 赏金总额
- 选中投标人后，其他投标者押金自动退还
- 最终结算金额是投标价（bidAmount），不是原始 bountyPerUser

### ⚠️ 裁决流程
- 只有 hunter 在被拒绝后才能发起裁决（`create-dispute`）
- 裁决后等待平台仲裁员调用 `resolveDispute`
- 裁决期间押金锁定，不能提取

### ⚠️ 邀请系统
- `bind-inviter` 绑定后**不可修改**，操作前务必确认地址正确
- 邀请人和被邀请人都必须是 EOA（非合约地址）
- 不能循环邀请（A邀请B，B不能再邀请A）

## 合约地址（XLayer Testnet）

```json
{
  
 hunter 在被拒绝后才能发起裁决（create-dispute）
- 裁决后等待平台仲裁员调用 resolveDispute
- 裁决期间押金锁定，不能提取

### 邀请系统注意
- bind-inviter 绑定后不可修改，操作前务必确认地址正确
- 邀请人和被邀请人都必须是 EOA（非合约地址）
- 不能循环邀请（A邀请B，B不能再邀请A）

## 合约地址（XLayer Testnet）

- core: 0x3E7765a23AEE412bfc36760Ec8Abb495fb5c6370
- bidding: 0xC917e6426608E1A7d0267b9346C9c70F97Cdb65B
- helper: 0xA7e63aC45FAd693f69be23F2B2072CBA4345881e
- userProfileCredit: 0x6CcDefaa116E17f19AC3A28d24f4b0C4a83C7B45
- categoryManager: 0xA63C1aBAe66a1687b80Da9573203DDcB9B19D47C
- tokenManager: 0xd1915fAdB020B6E5410fA480F415e287b32B4612
- referralSystem: 0x775f51F3A197793041f0C57EdC47Ee17aB6F48fF
- niumaToken: 0x49ABB6BFFEce92EAd9E71BCA930Ac877ef71939D

## build-tx（钱包插件签名模式）

给不想在服务端暴露私钥的场景用，返回未签名交易让前端钱包签名：

  node scripts/niuma.js build-tx createTask ...
  node scripts/niuma.js build-tx participateTask ...
  node scripts/niuma.js build-tx submitTask ...
  node scripts/niuma.js build-tx approveSubmission ...
  node scripts/niuma.js build-tx rejectSubmission ...
  node scripts/niuma.js build-tx cancelTask ...
  node scripts/niuma.js build-tx createDispute ...
  node scripts/niuma.js build-tx resolveDispute ...
  node scripts/niuma.js build-tx submitBid ...
  node scripts/niuma.js build-tx cancelBid ...
  node scripts/niuma.js build-tx selectBidder ...
