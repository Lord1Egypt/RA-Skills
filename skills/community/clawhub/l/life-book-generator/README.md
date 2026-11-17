# Life Book Generator Skill

这是一个可独立分发的 Agent Skill，用来通过官方 Agent API 创建 Life Book 付费完整报告任务、查询异步状态，并在任务完成后取回最终 18 章报告。

当前这套目录结构已经适合用于：

- GitHub 独立仓库发布
- 私有 Skill 打包
- ClawHub / Hermes 风格 Agent 运行时接入
- 为未来 OKX.AI ASP / A2MCP / x402 做前置准备

## Life Book 是什么

Life Book 不是一个普通问答工具，而是一套围绕个人出生信息、关键经历、现实权衡与核心问题展开的结构化人生说明书生成服务。

它的核心交付物不是一句回答，而是一份完整的长篇报告，包含：

- 个体底层结构判断
- 人生主题与关键矛盾
- 关系、事业、金钱、迁移、家庭等章节分析
- 面向现实选择的解释与建议

这个 Skill 的意义，不是单独暴露几个 API 命令，而是把这套“完整报告交付服务”包装成 Agent 可执行的标准流程。

## 这个 Skill 能做什么

- 创建 `标准版`（`lite`）或 `典藏版`（`pro`）完整报告任务
- 在任务待支付时返回支付状态与支付信息
- 支持手动支付渠道的“已付款”确认提交
- 不依赖网站 cookie，直接轮询 Agent 任务状态
- 使用任务 token 拉取最终完整报告结果

## 这个 Skill 在整个服务里扮演什么角色

如果没有 Skill，Life Book 更像一个网站产品，用户需要自己打开网页、填写资料、支付、等待生成，再回到页面看结果。

有了这个 Skill 之后，Agent 可以直接承接完整流程：

1. 引导用户补齐资料
2. 调用 Agent API 创建完整报告任务
3. 在待支付时返回支付信息
4. 在支付后继续追踪任务状态
5. 在结果 ready 后直接拉回完整报告

也就是说，这个 Skill 的真正意义是：

- 把官网的完整交付能力，包装成 Agent 可调用的服务层
- 让 GitHub / ClawHub / Agent 平台具备一个明确的接入入口
- 为未来 A2MCP / x402 做标准化准备

## 产品边界

当前真正收费的商品只有完整 Life Book 报告：

- `lite`：标准版，约 3 万字，69.9 元
- `pro`：典藏版，约 10 万字，699 元

这个 Skill 不会伪造以下状态：

- 支付成功
- 人工确认到账
- x402 校验完成
- 报告已生成完成

一切以官方 API 的真实返回为准。

## 完整服务流程

从产品视角看，这个 Skill 封装的是一条完整的交付链路，而不是几个零散命令。

### 阶段 1：资料收集

Agent 先收集完整 `intake@1` 数据，包括：

- 出生日期、出生时间、时区、经纬度
- 性别与时间精度
- 当前最核心的人生问题
- 可选补充问题
- 现实中的权衡取舍
- 两条关键人生证据
- 若干人生里程碑
- 同意生成授权

### 阶段 2：创建任务

当资料齐备后，Skill 通过 `/api/agent/report-tasks` 创建一条完整说明书任务，并明确版本：

- `lite`：标准版
- `pro`：典藏版

这一步的输出不只是任务 ID，还包括当前任务状态、后续状态查询地址、结果地址，以及必要时的支付信息。

### 阶段 3：支付与确认

如果任务返回 `awaiting_payment`，说明当前还不能开始正式生成。

此时 Skill 的职责是：

- 返回可用支付渠道
- 告诉用户任务尚未进入生成队列
- 在用户付款后提交“已付款确认”

此时 Skill **不能**做的事情是：

- 假装已到账
- 假装 x402 已完成
- 假装已经开始生成

### 阶段 4：排队与生成

当官方 API 将任务推进到 `queued` 或 `processing` 后，说明任务已经进入正式生成阶段。

此时 Skill 会继续承担：

- 轮询任务状态
- 告诉 Agent 当前处于等待、处理中还是失败
- 在合适的时候切换到结果读取

### 阶段 5：结果交付

当任务进入 `ready`，Skill 可以通过任务 token 拉回最终结果，并把完整报告交付给 Agent。

这里的核心不是跳转网页，而是：

- Agent 内可查询
- Agent 内可确认状态
- Agent 内可获取最终交付内容

这正是这个 Skill 与传统网站结账流程最大的区别。

## 角色分工

为了避免边界混乱，可以把整个服务分成 4 个角色：

### 用户

- 提供人生资料
- 选择标准版或典藏版
- 完成支付
- 等待报告结果

### Agent

- 和用户对话
- 帮用户补齐资料
- 调用 Skill 脚本
- 反馈任务状态与结果

### Skill

- 承接完整报告服务的调用流程
- 负责把用户需求转换为 Agent API 调用
- 负责状态轮询与结果读取
- 不伪造支付、不伪造成功、不伪造结果

### 官方 Life Book API

- 验证资料与任务请求
- 决定支付状态
- 决定任务是否进入队列
- 决定最终结果是否 ready

## 适合哪些平台

这份 Skill 目前最适合的使用场景是：

- GitHub 上作为独立 Skill 仓库分发
- ClawHub 或类似 Agent 市场做早期接入
- Hermes 风格内部 Agent 运行时
- 私有运营平台做受控集成

它当前还不是“任意平台拿去即插即用”的最终公开商品，因为：

- 真实 x402 支付闭环还没完全打通
- OKX.AI ASP 上架所需的最后材料与验证还没全部完成
- 生产级公有发布文档还可以继续补强

## 目录结构

```text
.
├── agents/
│   └── openai.yaml
├── examples/
│   └── intake.example.json
├── scripts/
│   ├── _shared.mjs
│   ├── check-health.mjs
│   ├── confirm-manual-payment.mjs
│   ├── create-intake.mjs
│   ├── create-order.mjs
│   ├── create-report-task.mjs
│   ├── get-order.mjs
│   ├── get-report-result.mjs
│   ├── get-report-task.mjs
│   └── wait-report-result.mjs
├── README.md
├── SKILL.md
└── package.json
```

## 运行要求

- Node.js `>=20`
- 一个可访问的已部署 Life Book 服务

## 环境变量说明

| 变量名 | 是否必需 | 谁来提供 | 作用 |
| --- | --- | --- | --- |
| `LIFE_BOOK_BASE_URL` | 是 | Skill 运营方 / 部署方 / 平台接入方 | Life Book 正式服务地址，例如 `https://app.elife369.site` |
| `LIFE_BOOK_AGENT_API_KEY` | 否 | 平台方或私有集成方 | 用于受控创建 Agent 任务的私有 key，不能暴露给终端用户 |
| `LIFE_BOOK_TASK_TOKEN` | 否 | 通常由 API 在运行时返回 | 后续查询任务状态、获取结果时使用的 bearer token，通常不是用户手动填写 |
| `LIFE_BOOK_TIMEOUT_MS` | 否 | 可选，由运行方决定 | HTTP 超时毫秒数，默认 `15000` |

### 普通用户通常需要提供什么

大多数真实使用场景下，终端用户**不需要自己手动配置全部 4 个变量**。

- `LIFE_BOOK_BASE_URL`：必须由 Skill 运行环境提供
- `LIFE_BOOK_AGENT_API_KEY`：仅平台方或你自己的私有集成需要配置
- `LIFE_BOOK_TASK_TOKEN`：通常由 `create-report-task` 返回，之后再用于后续命令
- `LIFE_BOOK_TIMEOUT_MS`：一般不用管，默认值足够

最小本地配置：

```bash
export LIFE_BOOK_BASE_URL="https://app.elife369.site"
```

私有平台接入示例：

```bash
export LIFE_BOOK_BASE_URL="https://app.elife369.site"
export LIFE_BOOK_AGENT_API_KEY="your_private_agent_key"
```

## 快速开始

### 1. 健康检查

```bash
node scripts/check-health.mjs
```

### 2. 准备 intake 数据

可以先参考示例结构：

```bash
cat examples/intake.example.json
```

提交数据必须符合 `intake@1` 结构。

### 3. 创建完整报告任务

标准版：

```bash
node scripts/create-report-task.mjs \
  --input-file /absolute/path/to/intake.json \
  --edition lite \
  --idempotency-key user-unique-report-key
```

典藏版：

```bash
node scripts/create-report-task.mjs \
  --input-file /absolute/path/to/intake.json \
  --edition pro \
  --idempotency-key user-unique-report-key
```

正常返回会包含：

- `task.id`
- `task.status`
- `access.token`（仅新任务创建时返回一次）
- `payment`（如果当前仍待支付）
- `taskStatusUrl`
- `taskResultUrl`
- `taskStreamUrl`

### 4. 提交手动支付确认

如果任务状态为 `awaiting_payment`，且用户已经通过支持的手动渠道付款：

```bash
node scripts/confirm-manual-payment.mjs \
  --task-id <taskId> \
  --task-token <taskToken> \
  --channel alipay
```

支持渠道：

- `alipay`
- `wechat`
- `evm`

注意：这一步只是提交“我已付款”的确认，**不会自动把订单标记为到账成功**。

### 5. 查询任务状态

```bash
node scripts/get-report-task.mjs \
  --task-id <taskId> \
  --task-token <taskToken>
```

### 6. 获取最终结果

```bash
node scripts/get-report-result.mjs \
  --task-id <taskId> \
  --task-token <taskToken>
```

如果报告还没准备好，API 可能返回 `202`，并带 `result: null`。

### 7. 等待到终态

```bash
node scripts/wait-report-result.mjs \
  --task-id <taskId> \
  --task-token <taskToken> \
  --poll-ms 5000 \
  --max-wait-ms 3600000
```

## 任务状态说明

请始终以官方 Agent API 为准：

- `awaiting_payment`：还未完成支付确认
- `queued`：任务已受理，等待生成
- `processing`：正在生成报告
- `ready`：最终报告已可获取
- `failed`：生成失败
- `canceled`：任务已取消或关闭

## 支付规则

- 只有 API 明确确认，才能说“支付成功”
- 没有真实发生，就不能声称 x402 / OKX.AI 支付校验已完成
- 手动支付确认只是进入运营确认流程，不代表自动到账

## 网站流回退脚本

下面这些脚本依然保留，用于旧版网站结账流程回退：

- `scripts/create-intake.mjs`
- `scripts/create-order.mjs`
- `scripts/get-order.mjs`

只有当 Agent API 路线不可用时才建议使用。它们会把用户带回官网交付流程，**不会直接在聊天里返回完整报告**。

## 当前发布状态

当前这份 Skill 更适合定义为：

- 可发布到 GitHub 的 beta Skill 仓库
- 可用于私有 Agent 集成和早期分发
- 还不是完整的 OKX.AI ASP 上架包
- 还不是完全验证过的 x402 生产支付集成版本

## 相关文件

- 面向 Skill 平台运行时的说明：`SKILL.md`
- OpenAI / Hermes 风格 Agent 配置：`agents/openai.yaml`
