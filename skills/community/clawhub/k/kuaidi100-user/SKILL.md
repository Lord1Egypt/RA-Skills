---
name: kuaidi100-user
description: "快递100用户版智能寄件助手：寄件下单全流程（寄快递需登录）、物流查询、订单管理。寄快递时必须先 SSO 登录并使用服务端地址簿，禁止使用本地缓存；未登录仅可使用地址解析、重量查询、快递比价等辅助功能。Use when: 用户要寄快递、查物流、管理快递订单、比价选快递、查运费，或提到快递100/寄件/查单/运费/快递价格相关服务。"
---

# 快递100用户版

## 前置要求

### CLI 安装检查

调用任何业务命令前，先确认 `kuaidi100-cli` 已安装且可在 PATH 中访问：

```bash
kd100 --version
# 或
kuaidi100-cli --version
```

若命令不存在、报「不是内部或外部命令」或无法执行，**必须先安装 CLI，不得继续寄件/查单流程**。

**安装方式（npm 全局安装）：**

```bash
npm i -g @kuaidi100-user/cli
```

安装完成后再次执行 `kd100 --version` 验证，确认输出版本号后再继续。

> 若 `npm install` 失败，联系管理员获取安装指引。

- **CLI 工具**：`kuaidi100-cli`（别名 `kd100`）已安装并可在 PATH 中访问
- **登录**：执行 `kd100 auth login --open` 完成 SSO 授权（CLI 自动用系统外部浏览器打开授权页，Agent **不得**代为打开链接，见 [SSO 授权登录](#sso-授权登录)）

## 运行模式

### 寄快递（需登录）

用户发起**寄快递 / 下单**意图时，**必须先登录**，禁止使用本地缓存填充寄件人/收件人：

```
kd100 auth status
    ↓ hasKey: false
    → 立即执行 kd100 auth login --open 完成 SSO 授权（见 [SSO 授权登录](#sso-授权登录)）
    → 授权成功前不得进入寄件流程，不得读取 kd100 data sender / data receivers
    ↓ hasKey: true
    → 进入寄件流程，仅使用服务端地址簿（kd100 sender / kd100 receiver）
```

### 辅助功能（无需登录）

未登录时可单独使用以下命令（**不含寄件下单**）：
- ✅ 地址解析（`kd100 address`）
- ✅ 物品重量查询（`kd100 weight`）
- ✅ 快递比价（`kd100 companies`）
- ❌ 寄件下单（`kd100 order create`）
- ❌ 服务端地址簿、物流查询、订单管理

### 登录后全部功能

用户通过 SSO 授权登录后可使用：
- 寄件下单全流程（服务端地址簿，不用本地缓存）
- 物流查询、订单管理

## CLI 命令速查

所有命令输出 JSON，成功写入 stdout，错误写入 stderr。成功格式：`{"status":200,"message":"ok","data":{...}}`

### 认证
```bash
kd100 auth login --open                      # SSO 授权登录（推荐：CLI 自动打开系统外部浏览器并等待授权）
kd100 auth login --no-wait --json            # 降级：仅返回授权链接与 device_code
kd100 auth login --device-code <code> --json # 降级：配合 --no-wait 轮询完成登录
kd100 auth logout                            # 登出清除登录信息
kd100 auth status                            # 查看当前状态和运行模式
```

### SSO 授权登录

需要登录时，**优先执行 `kd100 auth login --open`**。CLI 会调用 SSO 设备授权接口，并用**系统默认外部浏览器**（Chrome / Edge / Safari 等）打开授权页，随后在终端阻塞等待用户完成授权。

> **SSO 登录：由 CLI `--open` 打开外部浏览器，Agent 禁止代为打开**
>
> - **Agent 只执行** `kd100 auth login --open`，等待命令返回登录成功 JSON
> - **禁止** Agent 使用 `start`/`open`/`xdg-open`、Cursor 内置浏览器、MCP 浏览器等**重复打开**授权链接
> - CLI 内部通过 `openBrowser()` 调用系统外部浏览器，与 Agent 手动打开效果相同，无需 Agent 再操作
> - **授权成功前**不得执行寄件、查单等业务命令

#### 授权链接（供理解 / 降级参考）

授权 URL 由 SSO 设备授权接口返回的 `verificationUriComplete` 字段提供；CLI 在 `--open` 模式下自动打开该链接，Agent 无需自行拼接或构造 URL。

**标准流程（推荐）**

```bash
kd100 auth login --open
```

**Agent 只做两件事：**
1. 执行上述命令，**等待终端返回**（命令会阻塞直到用户在外部浏览器完成授权或超时）
2. 告知用户：「CLI 已在系统浏览器中打开授权页面，请在外部浏览器中完成登录」

**Agent 禁止：**
- 再用任何方式打开授权 URL（会导致两个授权页）
- 在 `--open` 等待期间并行执行其他业务 CLI 命令

**降级流程（仅当 `--open` 失败时）**

若 stderr 出现「无法自动打开浏览器」，改用分步登录：

```bash
kd100 auth login --no-wait --json
# → 将 data.verificationUriComplete 文本展示给用户，提示用户自行复制到外部浏览器打开
kd100 auth login --device-code <deviceCode> --json
```

降级时 Agent **仍禁止**代为打开浏览器，仅展示链接文案。

**授权等待规则：**
- `--open` 模式下 CLI 已阻塞等待，Agent 等待命令结束即可
- 登录成功 stdout 含 `hasKey: true` 后，方可继续后续业务流程

### 基础功能（无需登录）
```bash
kd100 address <地址>            # 地址解析 → 省/市/区/subArea
kd100 weight <物品名>           # 查物品参考重量 → spec_weight/category/restriction_level
kd100 companies <寄件城市> <收件城市> [重量]  # 快递比价 → 名称/编码/价格/时效
```

### 寄件下单（需登录）

**未登录时不得执行**，须先完成 SSO 授权。

```bash
kd100 order create \
  --sender-name <name> --sender-phone <phone> \
  --sender-province <prov> --sender-city <city> --sender-district <dist> --sender-address <addr> \
  --receiver-name <name> --receiver-phone <phone> \
  --receiver-province <prov> --receiver-city <city> --receiver-district <dist> --receiver-address <addr> \
  --item-name <name> --weight <kg> \
  --kuaidi-name <name> --kuaidi-com <com> --company-sign <sign> \
  [--service-type <type>] [--estimated-amount <amount>] [--remark <remark>] [--expected-pickup-time-desc <desc>]
```

### 订单管理（需登录）
```bash
kd100 order list [--limit N]              # 查询订单列表
kd100 order track <运单号> [--com <编码>]  # 物流轨迹查询
kd100 order cancel <订单号> --reason <原因> # 取消订单
```

### 地址簿（需登录）
```bash
kd100 sender                     # 查询默认寄件人
kd100 receiver <姓名>            # 按姓名查收件人
```

### 本地数据管理

> **寄快递流程不使用本地缓存**；以下命令仅供数据维护或未登录时查本地订单。

```bash
kd100 data sender                # 查看本地默认寄件人
kd100 data sender --set <JSON>   # 设置本地默认寄件人
kd100 data receivers             # 查看本地收件人历史
kd100 data orders                # 查看本地订单缓存
kd100 data clear [--what sender|receivers|orders|all]  # 清理本地数据
```

## 寄件流程概览

**前置：登录检查** → `kd100 auth status`，未登录则 `kd100 auth login --open`，**禁止使用本地缓存**

```
Step 0: 确认已登录 → 未登录则引导 SSO 授权，授权成功后再继续
Step 1: 获取寄件人 → kd100 sender（服务端）→ 失败则重新登录 → 仍无则手动询问
Step 2: 获取收件人 → kd100 receiver（服务端）→ 失败则重新登录 → 仍无则手动输入
Step 3: 物品信息   → 查重量 → 确认
Step 4: 地址解析   → 结构化自由文本地址
Step 5: 查快递公司 → 比价 → 用户选择
Step 6: 确认下单   → 预下单 → 展示链接
Step 7: 物流查询   → 仅查服务端（不合并本地缓存）
```

每个步骤的决策分支、降级策略详见 **[references/workflow.md](references/workflow.md)**。

## 物流查询

- **未登录模式**：仅查询本地 `kd100 data orders`
- **登录模式**：仅查服务端
  - `kd100 order list` / `kd100 order track`
  - 查不到数据时**不展示本地缓存**，提示用户 `kd100 auth login --open` 重新登录并重试

## 取消订单

- **未登录模式**：不支持（需登录）
- **登录模式**：确认订单号 + 取消原因 → `kd100 order cancel <orderNo> --reason <原因>`

## 关键字段映射

### 地址簿 → 下单参数

地址簿返回的字段名与下单参数不同，编排时必须映射：

| 地址簿字段 | 下单参数 | 说明 |
|-----------|---------|------|
| `mobile` | `--sender-phone` / `--receiver-phone` | 手机号 |
| `addr` | `--sender-address` / `--receiver-address` | 详细地址 |

其余字段（`name`/`province`/`city`/`district`）名称一致，直接对应 `--sender-name`/`--sender-province` 等。

### 快递公司 → 下单参数

| 比价返回字段 | 下单参数 | 说明 |
|------------|---------|------|
| `name` | `--kuaidi-name` | 快递公司名称 |
| `com` | `--kuaidi-com` | 快递公司编码 |
| `sign` | `--company-sign` | 签名标识（下单必传） |
| `totalprice` | `--estimated-amount` | 运费 |

### 重量字段

`kd100 weight` 返回的 `spec_weight` 是**字符串类型**，使用时需 `parseFloat()` 转换。

## 核心原则

- **寄快递必须先登录**：用户要寄快递时，先 `kd100 auth status`；未登录则 `kd100 auth login --open`，**禁止用 `kd100 data sender` / `kd100 data receivers` 本地缓存**
- **SSO 登录用 CLI `--open`**：CLI 自动用系统外部浏览器打开授权页并等待；Agent 只执行命令，**禁止** Agent 代为打开授权链接
- **分步交互**：每步只问一类信息，等用户回答后再进入下一步。禁止一次性列出所有问题。
- **登录模式仅用服务端（地址簿/订单/物流）**：服务端查不到数据时，**禁止展示本地缓存**，提示 `kd100 auth login --open` 重新登录并重试
- **必须询问**：物品类型、最终确认不可跳过
- **绝不自动执行**：不猜测物品、不自动选收件人、不跳过确认直接下单
- **下单后必须展示链接**：获取到下单链接后，**必须以文本形式**展示下单链接和二维码，然后可选地用浏览器工具自动打开。文本展示是必选项，浏览器打开是可选项——无论浏览器是否成功，用户都能看到链接完成下单。
- **适时提示登录**：用户查询物流/订单但未登录时，引导 `kd100 auth login --open`；每次会话最多提示一次

## 分步交互规则

**关键**：寄件流程是多轮对话，不是一次表单。每次只问一件事，拿到答案再往下走。

```
轮次0: [未登录] 引导 SSO 登录，等待授权成功后再继续
轮次1: "请确认寄件人信息" → 展示 kd100 sender 结果让用户确认
轮次2: "请提供收件人信息" → 等用户回答
轮次3: "要寄什么物品？" → 等用户回答
轮次4: "以下是可选快递，请选择" → 等用户回答
轮次5: "确认以下订单信息，是否下单？" → 等用户确认
```

每步之间可以调用 CLI 命令（查地址簿、查重量、查价格），但对用户只呈现一步的问题或选项。

## 错误处理

CLI 错误输出到 stderr，格式为 JSON：

```json
{"status": 401, "message": "未登录，请先执行 kuaidi100-cli auth login", "keyRequired": true}
```

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 参数错误 |

**`keyRequired: true`** 表示该命令需要登录，执行 `kd100 auth login --open`（CLI 打开系统外部浏览器，Agent 禁止重复打开链接），等待登录成功后再继续。

## 参考资料

- **[工作流](references/workflow.md)** — 完整决策逻辑、异常降级矩阵
  - 包含寄快递登录门禁与完整寄件流程
  - 分步交互规则和降级策略
  - 寄件人/收件人获取的三分支处理逻辑
- **[字段说明](references/fields.md)** — 地址簿、快递公司、下单返回等完整字段说明
