---
name: gmncode-usage
description: 通过 HTTP 接口查询 GMNCODE / gmncode.cn 中转站的大模型用量，包括 dashboard 汇总、每日趋势、按模型拆分的 token 与费用数据。当用户要求查看 GMNCODE token 用量、每日模型消耗、API/中转站花费、dashboard 用量，或希望用脚本/HTTP 接口直接获取 GMNCODE 使用数据而不是手动打开网页时使用。
---

# GMNCODE Usage

使用本技能自带脚本，通过可用的 dashboard HTTP 接口查询 GMNCODE 用量数据。

## 快速开始

1. 先确保凭据已经通过环境变量或 `~/.openclaw/.env` 提供。
2. 优先运行 `scripts/gmncode_usage.py`，不要每次都重新手写登录、token 缓存和重试逻辑。
3. 常用命令：
   - `python3 scripts/gmncode_usage.py brief`  
     查询你最常要的那组指标：**账户每日额度 + 今日模型用量**
   - `python3 scripts/gmncode_usage.py quota`  
     只看账户每日额度
   - `python3 scripts/gmncode_usage.py report --date today`
   - `python3 scripts/gmncode_usage.py report --date 2026-03-25`
   - `python3 scripts/gmncode_usage.py report --start 2026-03-01 --end 2026-03-26`
   - `python3 scripts/gmncode_usage.py models --date 2026-03-25 --json`
   - `python3 scripts/gmncode_usage.py trend --start 2026-03-01 --end 2026-03-26 --json`

## 工作流

### 1. 安全加载凭据

不要把邮箱和密码硬编码进临时脚本、回复内容或日志里。

优先使用：
- `GMNCODE_EMAIL`
- `GMNCODE_PASSWORD`

`GMNCODE_BASE_URL` 已固定写死为 `https://gmncode.cn`，因为这不是敏感信息，不需要放进环境变量。

如果缺少凭据，就停止执行，并提示用户补充到 `~/.openclaw/.env`。

### 2. 复用内置客户端

脚本已经处理好了：
- 通过 `/api/v1/auth/login` 登录
- access token 本地缓存
- 遇到 `401` / `INVALID_TOKEN` 时自动重新登录并重试一次
- dashboard 所需的 referer / headers

除非 HTTP 接口失效，否则不要退回浏览器自动化方案。

### 3. 使用正确接口

使用以下接口：
- `/api/v1/subscriptions?status=active`
- `/api/v1/usage/dashboard/stats`
- `/api/v1/usage/dashboard/trend`
- `/api/v1/usage/dashboard/models`

请求参数统一传：
- `start_date=YYYY-MM-DD`
- `end_date=YYYY-MM-DD`
- `timezone=Asia/Shanghai`

不要用 `/api/v1/admin/dashboard/*`，普通用户 token 会返回 `403 FORBIDDEN`。

### 4. 按指标口径取值

如果用户要的是这组固定指标，按下面口径取：

#### A. 账户每日使用额度

从 `/api/v1/subscriptions?status=active` 读取所有活跃订阅：
- **每日使用额度** = `sum(group.daily_limit_usd)`
- **今日已用** = `sum(daily_usage_usd)`
- **今日剩余** = 每日使用额度 - 今日已用

#### B. 今日模型用量

从 `/api/v1/usage/dashboard/models` 读取指定日期：
- 模型名：`model`
- token 用量：`total_tokens`
- 实际金额：`actual_cost`

默认把 token 格式化成 `x.x M` / `x.xx B` 这种紧凑写法。

## 输出建议

如果用户只想看固定口径，优先给两块：
1. **账户额度**：每日使用额度 / 今日已用 / 今日剩余
2. **今日模型使用**：模型名 / token 用量 / 实际金额

如果用户要更完整的汇报，再补：
- `stats` 的汇总数据
- `trend` 的每日趋势
- 当查询区间为单日时，补 `models` 的按模型拆分

默认使用紧凑表格或短列表，避免冗长描述。

## 资源

### scripts/

- `scripts/gmncode_usage.py`：安全的 HTTP 客户端与 CLI，负责登录、stats、trend、models 查询。

### references/

- `references/api.md`：接口说明、安全约定、凭据存储方式与字段解释。
