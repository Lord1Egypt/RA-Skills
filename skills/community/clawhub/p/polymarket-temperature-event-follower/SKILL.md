---
name: polymarket-temperature-event-follower
description: Automated trader for Polymarket weather highest temperature markets. Scans global weather markets and executes buys during local morning window (9-10 AM) when YES price is favorable. Built for SkillPay billing integration with robust error handling and state persistence.
metadata:
  author: "stefantaylor5"
  version: "1.0.1"
  displayName: "Polymarket Temperature Event Follower"
  difficulty: "intermediate"
  tags: ["polymarket", "weather", "trading", "sniper", "event-driven"]
---

# SkillPay Weather Sniper / 天气狙击机器人

**Polymarket 天气事件市场自动化交易系统**

---

## 📋 目录

1. [项目概述](#1)
2. [快速开始（5分钟）](#2)
3. [准备工作](#3)
4. [API 密钥获取教程](#4)
5. [配置文件详解 (.env)](#5)
6. [代码参数详解](#6)
7. [启动指南](#7)
8. [安全建议](#8)
9. [故障排查](#9)
10. [FAQ 常见问题](#10)

---

<a name="1"></a>
## 1. 项目概述 / Project Overview

### 1.1 这是什么？/ What is this?

这是一个自动化交易机器人，用于在 **Polymarket** 预测市场平台上交易**天气事件**合约。

**核心功能**：
- ✅ 实时扫描全球 33 个城市的天气市场
- ✅ 在气温预测确定窗口期（10:00-14:00）自动买入"今日高温超过阈值"的合约
- ✅ 集成 SkillPay 按次计费（每笔成功下单扣 0.01 USDT）
- ✅ 异常容错：网络重试、余额检查、滑点保护
- ✅ 完整日志和状态持久化

### 1.2 适合谁用？/ Who is this for?

- 对天气预测市场感兴趣的交易者
- 想要自动化策略的开发者
- 学习 Polymarket API 和预测市场的新手

### 1.3 核心策略 / Core Strategy

```
假设：每日最高温通常出现在下午14:00-15:00（气象学原理）
逻辑：
  1. 上午10:00后，官方气温预报已发布，市场不确定性降低
  2. 当 YES token 价格低于 0.35 时，认为市场低估了"高温"概率
  3. 以固定金额（默认 $1.0）买入，等待气温确定后价格上涨
  4. 可在价格上涨后卖出，或持有至结算（自动按 $1.0 或 $0.0 结算）
```

---

<a name="2"></a>
## 2. 快速开始（5分钟）/ Quick Start (5 min)

### 2.1 前置条件 / Prerequisites

- ✅ Python 3.9+（推荐 3.10-3.12）
- ✅ 已注册 [Polymarket](https://polymarket.com) 账户
- ✅ 懂基本命令行操作

### 2.2 一键启动脚本 / One-Command Setup

```bash
# 1. 克隆/进入项目目录（你已经在了）
cd C:\Users\19154\Desktop\skill

# 2. 安装依赖（全程约 2 分钟）
pip install -r requirements.txt

# 3. 复制环境变量模板
copy .env.example .env
# 然后编辑 .env 文件，填入你的密钥（见第4节）

# 4. 测试运行（模拟模式，不花钱）
python sniper.py --dry-run --once

# 5. 看到扫描输出后，说明安装成功！
# 6. 真实交易（谨慎！）
python sniper.py --live --once
```

---

<a name="3"></a>
## 3. 准备工作 / Preparation

### 3.1 环境检查 / Environment Check

```bash
# 检查 Python 版本（需要 3.9+）
python --version
# 预期输出: Python 3.10.x 或 3.11.x 或 3.12.x

# 检查 pip
pip --version
```

### 3.2 创建虚拟环境（可选但推荐）/ Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3.3 依赖列表 / Dependencies

创建 `requirements.txt` 文件（如果不存在）：

```
python-dotenv>=1.0.0
requests>=2.31.0
aiohttp>=3.9.0
pytz>=2024.1
eth-account>=0.11.0
py-clob-client>=0.2.0  # Polymarket 官方客户端（实盘必需）
```

安装：
```bash
pip install -r requirements.txt
```

---

<a name="4"></a>
## 4. API 密钥获取教程 / API Key Tutorial

### 4.1 Polymarket 凭证 / Polymarket Credentials

#### 步骤 1：导出钱包（EOA 和 Proxy）

1. 访问 [Polymarket Settings](https://polymarket.com/settings)
2. 将metamask钱包登录到polymarket主页
3. 你需要以下信息：

| 字段 | 说明 | 从哪里获取 |
|------|------|-----------|
| `PRIVATE_KEY` | 你的 EOA 钱包私钥（**绝密！**） | MetaMask 导出私钥（注意：不是助记词） |
| `PROXY_WALLET` | Polymarket 代理钱包地址 | Settings 页面显示的 "Wallet Address" |
| `POLY_API_KEY` | L2 API Key | 待会儿运行命令获得 |
| `POLY_API_SECRET` | L2 API Secret | 待会儿运行命令获得 |
| `POLY_API_PASSPHRASE` | L2 密码 | 待会儿运行命令获得 |

#### 步骤 2：生成私钥（MetaMask）

1. 打开 MetaMask 扩展
2. 选择账户 → 更多 → "Account details"
3. 点击 "Export Private Key"
4. 输入密码确认
5. 复制以 `0x` 开头的 64 位十六进制字符串

⚠️ **安全警告**：
- 私钥 = 完全控制权！任何人拿到私钥可以转移所有资产
- 不要将私钥上传到 GitHub、云盘
- 建议使用**单独钱包**专门用于交易，不要存放大额资金

#### 步骤 3：确定 `SIGNER_TYPE`

- 如果 `PRIVATE_KEY` 属于普通 EOA 钱包→ `SIGNER_TYPE = "2"`
- 如果使用 Gnosis Safe 多签 → `SIGNER_TYPE = "2"`（推荐）

大多数用户选择 `"1"`。
选择1的时候 可以不用运行命令获取L2凭证，直接用邮箱注册polymarket获得一个私钥钱包 去设置页面获取生成L2凭证并且导出私钥 然后复制代理钱包地址
Polymarket 官网看到的钱包地址（通常以 0x 开头），它持有你的 USDC.e 资金。
PRIVATE_KEY: 你的邮箱钱包私钥。你需要从官方导出页面获取。
---
#### 步骤 4：确定 `L2凭证`
在代码所在目录下运行 python sniper.py --live --once
命令行会返回3个凭证 依次填入.env文件中



### 4.2 SkillPay 

**注意**：
- 这是按次计费服务，每成功下单一次扣除 **0.01 USDT**
- 如果余额不足，下单会失败（系统会提示充值链接）
- 最低充值金额：**8 USDT**（相当于 800 次调用额度）

---

### 4.3 userId / 用户ID

`SKILLPAY_USER_ID`：同PROXY_WALLET的值



<a name="5"></a>
## 5. 配置文件详解 / Configuration

所有配置通过**环境变量**（`.env` 文件）管理。

### 5.1 创建 `.env` 文件

在项目根目录创建文件 `.env`，内容如下：

```ini
# ============================================
# 必填：Polymarket 认证
# ============================================
PRIVATE_KEY=0xsk_your_private_key_here_64_hex_chars
PROXY_WALLET=0x1234567890123456789012345678901234567890
POLY_API_KEY=pk_live_xxxxxxxxxxxxxxxxxxxx
POLY_API_SECRET=sk_live_xxxxxxxxxxxxxxxxxxxx
POLY_API_PASSPHRASE=your_passphrase_here
SIGNER_TYPE=1  # 1=邮箱账户, 2=metamask注册的polymarket账户

# ============================================
# 交易参数（建议保持默认）
# ============================================
TRADE_AMOUNT_USD=1.0          # 每笔下单金额（美元）
MIN_ORDERBOOK_SIZE=1.0        # 最小订单簿深度（流动性过滤）
SLIPPAGE_TOLERANCE=0.15       # 滑点容忍度（15%）
ENTRY_THRESHOLD=0.35          # 入场阈值（YES token 价格 < 0.35 才买入）
MAX_COST_PER_TRADE=1.2        # 单笔最大成本（超出则不买）

# ============================================
# 时间窗口（本地时间，UTC+8）
# ============================================
MONITOR_START_HOUR=9          # 监控开始时间（小时，小数形式）
MONITOR_END_HOUR=9.9167       # 监控结束时间（9:55 = 9 + 55/60 = 9.9167）
FALLBACK_START_HOUR=10        # Fallback 开始时间
FALLBACK_WINDOW_MINUTES=5     # Fallback 窗口长度（分钟）

# ============================================
# 执行频率（秒）
# ============================================
CHECK_INTERVAL=300            # 扫描间隔（300秒 = 5分钟）
REPORT_INTERVAL=240           # 报告间隔（240秒 = 4分钟）

# ============================================
# 缓存与重试
# ============================================
CACHE_TTL=3600                # 通用缓存时间（1小时）
GAMMA_CACHE_TTL=300           # Gamma API 缓存（5分钟）
CLOB_CACHE_TTL=30             # CLOB 订单簿缓存（30秒）
MAX_CONCURRENT_REQUESTS=50    # 最大并发请求数
REQUEST_DELAY=0.05            # 请求间延迟（秒）
MAX_RETRIES=3                 # 最大重试次数（网络失败时）
RETRY_DELAY=1.0               # 重试延迟（秒）

# ============================================
# 文件路径
# ============================================
STATE_FILE=state.json         # 状态文件（持仓、交易历史）
CACHE_DIR=cache               # 缓存目录
```

---

### 5.2 参数详细说明 / Parameter Reference

#### 5.2.1 认证参数 / Authentication

| 参数 | 类型 | 必填 | 说明 | 示例值 | 建议值 |
|------|------|------|------|--------|--------|
| `PRIVATE_KEY` | string | ✅ | EOA 钱包私钥（ hexadecimal，带 `0x` 前缀） | `0xabc123...` | 使用**专用钱包**，不要用主钱包 |
| `PROXY_WALLET` | string | ✅ | Polynomial 代理钱包地址（从网站导出） | `0x1234...` | 与 PRIVATE_KEY 对应的地址 |
| `POLY_API_KEY` | string | ✅ | Polynomial L2 API Key（`pk_` 或 `sk_` 开头） | `pk_live_xxx` | 从 Settings → API Keys 创建 |
| `POLY_API_SECRET` | string | ✅ | L2 API Secret | `sk_live_xxx` | 同上 |
| `POLY_API_PASSPHRASE` | string | ✅ | 创建 API Key 时设置的密码 | `myPass123` | 记住它，不会显示第二次 |
| `SIGNER_TYPE` | int | ✅ | 签名器类型：`1`=邮箱, `2`=Gnosis Safe | `0` | 普通钱包选 `2` |

#### 5.2.2 交易参数 / Trading

| 参数 | 类型 | 默认值 | 说明 | 建议值 | 风险提示 |
|------|------|--------|------|--------|----------|
| `TRADE_AMOUNT_USD` | float | `1.0` | 每笔订单目标金额（美元）。系统会自动计算 shares 数量 | `0.5` - `5.0` | 金额越大，潜在收益/损失都越高 |
| `MIN_ORDERBOOK_SIZE` | float | `1.0` | 订单簿最小深度（需要至少有 $1.0 的流动性） | `1.0` | 太低可能滑点严重 |
| `SLIPPAGE_TOLERANCE` | float | `0.15` (15%) | 滑点容忍度。如果 best_ask > 预期价格 × (1+滑点)，则取消订单 | `0.05` - `0.20` | 保守交易选 5%，激进选 20% |
| `ENTRY_THRESHOLD` | float | `0.35` | 入场阈值。YES token 价格必须低于此值才买入 | `0.30` - `0.50` | 太低可能错过机会，太高可能买贵 |
| `MAX_COST_PER_TRADE` | float | `1.2` | 单笔最大成本（USD）。实际成本 = price × shares，如果超过此值则不买 | `1.5` - `2.0` | 用于控制极端滑点损失 |

**公式示例**：
```
假设 TRADE_AMOUNT_USD = 1.0, best_ask = 0.5
目标 shares = 1.0 / 0.5 = 2.0 shares
实际 cost = 0.5 × 2.0 = $1.0 OK

假设 best_ask = 0.6, 但 max_price = 0.6 × 1.15 = 0.69
如果 0.6 < 0.69 → 仍可买入
如果 0.7 > 0.69 → 跳过（滑点过大）
```

#### 5.2.3 时间窗口 / Time Windows

| 参数 | 类型 | 默认值 | 说明 | 计算方式 |
|------|------|--------|------|----------|
| `MONITOR_START_HOUR` | float | `9` | 监控开始时间（小时） | `9` = 09:00 |
| `MONITOR_END_HOUR` | float | `9.9167` | 监控结束时间 | `9 + 55/60 = 9.9167` = 09:55 |
| `FALLBACK_START_HOUR` | float | `10` | Fallback 开始时间 | `10` = 10:00 |
| `FALLBACK_WINDOW_MINUTES` | int | `5` | Fallback 窗口长度 | 10:00-10:04 |

**时间逻辑**：
- 09:00-09:55：正常扫描窗口（今日市场）
- 10:00-10:04：Fallback 强制买入窗口（为今日未持仓的城市强行下单）
- 09:55-10:00：空档期，不扫描

**为什么这样设置**：
- 气象局通常在早上 08:00-09:00 发布当日天气预报
- 9:00 后市场已消化信息，不确定性降低
- 10:00 是最后买入机会，离 14:00 最高温还有 4 小时
- Fallback 窗口很短，避免重复下单

#### 5.2.4 执行频率 / Execution

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `CHECK_INTERVAL` | int | `300` | 扫描周期（秒），每 5 分钟检查一次市场 |
| `REPORT_INTERVAL` | int | `240` | 状态报告周期（秒），每 4 分钟打印持仓/PnL |

**建议**：
- 测试阶段：`CHECK_INTERVAL=60`（每分钟）以便快速看到效果
- 生产环境：`CHECK_INTERVAL=300`（5分钟）避免 API 限流

#### 5.2.5 缓存与重试 / Caching & Retry

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `CACHE_TTL` | int | `3600` | 通用缓存生存期（秒），1 小时 |
| `GAMMA_CACHE_TTL` | int | `300` | Gamma Events API 缓存（5分钟） |
| `CLOB_CACHE_TTL` | int | `30` | CLOB 订单簿缓存（30秒） |
| `MAX_CONCURRENT_REQUESTS` | int | `50` | 最大并发请求数（异步） |
| `REQUEST_DELAY` | float | `0.05` | 请求间最小延迟（秒），防限流 |
| `MAX_RETRIES` | int | `3` | 网络失败最大重试次数 |
| `RETRY_DELAY` | float | `1.0` | 重试延迟（秒），指数退避 |

#### 5.2.6 文件路径 / Paths

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `STATE_FILE` | string | `state.json` | 状态文件，保存持仓、交易历史、统计 |
| `CACHE_DIR` | string | `cache` | 缓存目录，存储 API 响应（自动创建） |

---

<a name="6"></a>
## 6. 代码参数详解（sniper.py 常量）

除了 `.env` 配置，代码中还有一些**硬编码常量**需要了解：

### 6.1 气象相关常量

```python
# 城市列表（33个）
CITY_SLUGS = [
    "taipei", "seoul", "shanghai", "shenzhen", "wuhan", "beijing", "chongqing",
    "tokyo", "singapore", "hong-kong", "tel-aviv", "lucknow",
    "london", "warsaw", "paris", "milan", "madrid", "munich", "ankara",
    "atlanta", "nyc", "toronto", "miami", "chicago", "dallas", "seattle",
    "wellington", "buenos-aires", "sao-paulo",
    "denver", "houston", "austin", "san-francisco",
]

# 时区映射（自动将本地时间转为 UTC）
TIMEZONES = {
    "nyc": "America/New_York",
    "tokyo": "Asia/Tokyo",
    "london": "Europe/London",
    # ... 共 33 个时区定义
}
```

**修改城市**：如需增减城市，直接修改 `CITY_SLUGS` 列表。

### 6.2 API 端点（通常不需要改）

```python
GAMMA_API_BASE = "https://gamma-api.polymarket.com"
CLOB_API_BASE = "https://clob.polymarket.com"
BILLING_URL = "https://skillpay.me/api/v1/billing"
```


<a name="7"></a>
## 7. 启动指南 / Launch Guide

### 7.1 命令行参数 / CLI Arguments

```bash
python sniper.py [OPTIONS]

选项：
  --dry-run          扫描但不实际下单（默认模式）
  --once             只运行一次扫描后退出（调试用）
  --status           显示当前持仓和统计信息
  --live             启用真实交易（需要已配置所有 API 凭证）
```

### 7.2 启动流程 / Launch Sequence

#### 场景 1：首次测试（强烈建议）

```bash
# 1. 确保 .env 已配置
# 2. 运行模拟模式（不花钱、不下单）
python sniper.py --dry-run --once

# 预期输出：
# [AUTH] Loaded credentials...
# [SCAN] Starting scan...
# [SCAN] Tradeable in monitor window: X
# [BUY] Triggered: ... (如果触发条件满足)
# [DRY] Would buy 1 share @ $0.45 (max: $0.52)
# [OK] State saved, exiting.
```

**验证点**：
- ✅ 无报错
- ✅ 看到 `[SCAN]` 日志
- ✅ 如果市场条件满足，看到 `[BUY] Triggered` 和 `[DRY] Would buy...`
- ✅ 最后 `[OK] State saved, exiting.`

#### 场景 2：查看当前状态

```bash
python sniper.py --status
```

输出示例：
```
Positions:
  - tokyo_2026-03-26: entry_price=0.45, shares=2.22, PnL=$0.12
  - london_2026-03-26: entry_price=0.52, shares=1.92, PnL=-$0.08

Stats:
  Total trades: 5
  Total PnL: $0.45
  Billing cost: 0.05 USDT
```

#### 场景 3：生产环境运行
在此之前不要忘了往polymarket网页端充值 只需点击充值按钮即可。
```bash
# 方式 A：前台运行（用于测试）
python sniper.py --live --once

# 方式 B：后台持续运行（推荐）
# Windows (使用 start)
start /B python sniper.py --live

# macOS/Linux (使用 screen/tmux)
screen -S weather_sniper
python sniper.py --live
# 按 Ctrl+A, D  detached
```

**监控日志**：
```bash
# 实时查看
tail -f sniper.log  # 如果配置了日志文件
# 或在代码中添加 FileHandler
```

---

<a name="8"></a>
## 8. 安全建议 / Security Best Practices

### 8.1 私钥管理 / Private Key Management

| 做法 | 推荐度 | 说明 |
|------|--------|------|
| 使用硬件钱包（Ledger/Trezor）+ 代理 | ⭐⭐⭐⭐⭐ | 最安全，但配置复杂 |
| 使用单独 EOA 钱包，小额（< $100） | ⭐⭐⭐⭐ | 平衡安全与便利 |
| 主钱包直接投入 | ⭐⭐ | 风险高，不推荐 |

### 8.2 环境变量安全

```bash
# ✅ 正确：.env 文件加入 .gitignore
echo ".env" >> .gitignore

# ❌ 错误：不要硬编码在代码里
PRIVATE_KEY="0x..."  # 不要这样！

# ✅ 正确：从环境变量读取
private_key = os.getenv('PRIVATE_KEY')
```

<a name="9"></a>
## 9. 故障排查 / Troubleshooting

### 9.1 常见错误 / Common Errors

#### 错误 1：`py-clob-client not available`

**原因**：未安装依赖

**解决**：
```bash
pip install py-clob-client
```

---

#### 错误 2：`Invalid private key` 或 `Insufficient balance`

**原因**：
- 私钥格式错误（缺 `0x` 前缀）
- 钱包余额不足（Polygnosis 需要支付 Gas）

**解决**：
1. 检查 `PRIVATE_KEY` 是否为 64 位十六进制，带 `0x` 前缀
2. 钱包转入至少 $5-10 等值的 USDC/ETH（Polygon 链）
3. 确认网络为 Polygon Mainnet

---

#### 错误 3：`market not found` (404)

**原因**：
- `token_id` 对应的市场未开市
- 城市/日期组合不存在

**解决**：
```bash
# 手动测试 API
curl "https://gamma-api.polymarket.com/markets?limit=10"
# 确认返回的数据中包含你感兴趣的城市和日期
```

---

#### 错误 4：`Billing failed (balance: 0.0000)`

**原因**：SkillPay 余额耗尽

**解决**：
1. 访问 SkillPay Dashboard 充值（最低 8 USDT）
2. 或等下一轮扫描自动重试（已跳过耗尽余额的情况）

---

#### 错误 5：`rate limit` 或 `429`

**原因**：API 调用过于频繁

**解决**：
- 增大 `CHECK_INTERVAL`（如改为 `600` 秒）
- 减小 `MAX_CONCURRENT_REQUESTS`
- 确保 `REQUEST_DELAY` >= `0.1`

---

### 9.2 日志级别调整

如需更详细日志，在代码中添加：

```python
import logging
logging.basicConfig(level=logging.DEBUG)  # 或 INFO, WARNING
```

---

### 9.3 重置状态

删除 `state.json` 和 `cache/` 目录，重启即可：

```bash
del state.json
rmdir /S /Q cache
python sniper.py --dry-run --once
```

---

<a name="10"></a>
## 10. FAQ 常见问题

### Q1: 实盘和模拟模式有什么区别？

A：`--dry-run` 会调用 `execute_buy_order` 但：
- 不初始化真实 `ClobClient`
- 不发送 HTTP 请求到 Polymarket
- 不调用 `billing_charge`
仅打印"would buy"日志，用于验证逻辑是否正确。

### Q3: 如果计费失败，订单会撤销吗？

A：不会。设计原则是"订单优先"：
- 订单上链成功后，即使计费失败，订单仍然有效
- 计费失败只记录 warning 并显示充值链接
- 这是**正确的行为**，因为链上订单无法撤销

### Q4: 为什么我的 `state.json` 持仓信息不更新？

A：`state.json` 在每次成功下单后立即保存。如果没有更新：
- 检查文件权限（是否可写）
- 检查是否发生崩溃（查看错误日志）
- 手动重启后会自动加载

### Q5: 可以同时运行多个实例吗？

A：**不建议**。多个实例会竞争 `state.json` 文件，导致数据损坏。

### Q6: 如何调整交易的城市或时间？

A：编辑 `CITY_SLUGS` 列表（sniper.py:93-100），或修改 `MONITOR_START_HOUR` 等时间参数。

### Q7: profit 如何计算？

A：系统未实现自动卖出，持仓会一直保留到结算：
- 如果 YES token 结算价为 $1.0 → 收益 = shares × ($1.0 - entry_price)
- 如果 NO token 结算价为 $1.0 → YES token 归零 → 损失 = - shares × entry_price
实际盈亏 = 持仓市值变化 + 已实现盈亏（如果手动平仓）

### Q8: 有退订或取消订阅机制吗？

A：没有自动退订。持仓会保留在 `state.json` 中，直到手动删除或结算完成。

### Q9: 如何设置 Telegram 通知？

A：不在当前功能范围内。建议使用外部脚本监控 `sniper.log`，匹配关键词（如 `Billing failed`、`余额不足`）后发送通知。

### Q10: 代码中的 `MIN_CHARGE_AMOUNT` 有什么作用？

A：这是预检阈值。如果 `billing_get_balance` 返回值 < 0.01，扫描会提前退出，避免浪费 API 调用。这是**保护机制**，不是计费金额。

---

## 📞 支持 / Support

- 纸飞机：@zerofinnley

---

**祝交易顺利！记住：风险管理第一，收益第二。** 🎯
