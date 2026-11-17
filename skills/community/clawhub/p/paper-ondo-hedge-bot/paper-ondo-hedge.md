---
name: paper-ondo-hedge
description: 操作 PaperTrade + ONDO Perps 中性对冲机器人。支持 Web 控制面板和命令行两种方式，包含模拟模式和真实模式。用于配置、运行、监控、紧急平仓这个亏损挖矿策略机器人。当用户需要运行对冲机器人、查看状态、平仓、注册 Session Key、调整参数时使用。
---

# PaperTrade + ONDO 中性对冲机器人操作指南

## 相关平台

### 对冲交易平台

[PaperTrade](https://papertrade.xyz/) &nbsp;|&nbsp; [ONDO](https://app.ondoperps.xyz/?ref=8RU3VB)

### 新手推荐

**加密货币获取：** [OKX](https://www.mitxcqvwnhj.com/join/9122359) &nbsp;|&nbsp; [币安](https://www.bsmkweb.cc/register?ref=35266688)

**自动化平台：** [Minara](https://minara.ai/r/23EUC6)

**AI 本地使用：** [购买 GPT](https://www.gamsgo.com/partner/JwUY7)

---

## 技能适用场景

当用户提到以下需求时使用本技能：
- 运行/启动对冲机器人
- 查看 PaperTrade 或 ONDO 账户状态
- 平掉所有持仓
- 注册 PaperTrade Session Key
- 调整对冲参数（仓位大小、杠杆、目标波动等）
- 启动 Web 控制面板
- 切换模拟/真实模式
- 排查运行错误

## 项目路径

`/Users/caroline/Desktop/源代码/demo/paper中性脚本/`

## 核心文件

| 文件 | 作用 |
|------|------|
| `paper_client.py` | PaperTrade 客户端（EIP-712 签名、Session Key、开平仓） |
| `ondo_client.py` | ONDO Perps 客户端（HMAC 签名、市价单、查询） |
| `mock_clients.py` | 模拟客户端（模拟模式使用，不进行真实交易） |
| `hedge_bot.py` | 对冲核心逻辑（双向开仓、监控、平仓、统计） |
| `main.py` | CLI 入口 |
| `web_server.py` | Web 控制面板后端（端口 8765） |
| `index.html` | Web 控制面板前端 |
| `.env` | 配置文件（私钥、API 凭证、策略参数） |

---

## 操作步骤

### 方式一：Web 控制面板（推荐）

```bash
cd /Users/caroline/Desktop/源代码/demo/paper中性脚本
python web_server.py
```

打开浏览器访问 **http://localhost:8765/**

面板功能：
- 🧪 模拟 / 💰 真实 模式切换（默认模拟）
- 🌐 中英文语言切换
- 🌐 访问官网：PaperTrade / ONDO 配置卡片右上角直达官网
- 🔗 获取 ONDO API Key
- ▶ 启动 / ■ 停止机器人
- 📊 实时运行日志（每 3 秒刷新）

### 方式二：命令行

#### 1. 检查依赖和配置

```bash
cd /Users/caroline/Desktop/源代码/demo/paper中性脚本
cat .env
```

**模拟模式**（默认 `HEDGE_MODE=mock`）：无需配置凭证，直接运行。

**真实模式**（`HEDGE_MODE=real`）必须配置：
- `PAPER_WALLET_PRIVATE_KEY`：PaperTrade 钱包私钥（0x 开头 64 位 hex）
- `ONDO_KEY_ID` 和 `ONDO_API_SECRET`：ONDO API 凭证

可选配置：
- `PAPER_SESSION_KEY`：已注册的 Session Key，避免重复注册

#### 2. 安装依赖

```bash
cd /Users/caroline/Desktop/源代码/demo/paper中性脚本
pip install -r requirements.txt
```

#### 3. 注册 Session Key（真实模式，首次运行或 Key 过期时）

```bash
cd /Users/caroline/Desktop/源代码/demo/paper中性脚本
python main.py register
```

将输出的 `PAPER_SESSION_KEY` 写入 `.env`。

#### 4. 查看账户状态

```bash
cd /Users/caroline/Desktop/源代码/demo/paper中性脚本
python main.py status
```

确认两个平台都有足够余额。

#### 5. 运行对冲机器人

```bash
cd /Users/caroline/Desktop/源代码/demo/paper中性脚本
python main.py
```

机器人会自动循环开仓-监控-平仓。

#### 6. 紧急平仓

如果需要立即停止并平掉所有持仓：

```bash
cd /Users/caroline/Desktop/源代码/demo/paper中性脚本
python main.py close-all
```

---

## 模式说明

| 模式 | `HEDGE_MODE` 值 | 行为 |
|------|-----------------|------|
| 模拟模式 | `mock` | 使用内置模拟客户端，不进行真实交易，无需凭证 |
| 真实模式 | `real` | 进行真实交易，需要配置私钥和 API 凭证 |

模拟模式使用固定测试钱包，输出与真实模式完全一致的日志格式，适合演示和学习。

---

## 策略参数调整

编辑 `.env` 文件中的以下参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `HEDGE_SYMBOL` | BTC | 交易对（BTC/ETH） |
| `HEDGE_POSITION_SIZE` | 50 | 每侧名义仓位 USD |
| `HEDGE_PAPER_LEVERAGE` | 10 | PaperTrade 杠杆 |
| `HEDGE_ONDO_LEVERAGE` | 10 | ONDO 杠杆（BTC/ETH 最大 25） |
| `HEDGE_TARGET_MOVE_PCT` | 1.0 | 触发平仓的价格变动百分比 |
| `HEDGE_MAX_HOLD_SECONDS` | 3600 | 最长持仓秒数 |
| `HEDGE_DIRECTION` | random | 开仓方向（random/paper_long/paper_short） |

---

## 常见错误处理

### Session Key 过期
```
RuntimeError: Session Key 已过期，请重新注册
```
解决：运行 `python main.py register` 重新注册。

### ONDO 签名错误
```
ONDO API 错误: signature invalid
```
解决：检查 `ONDO_KEY_ID` 和 `ONDO_API_SECRET` 是否正确。如仍错误，可能 ONDO API 签名格式已更新，需修改 `ondo_client.py` 的 `_sign` 方法。

### PaperTrade 平仓找不到仓位
开仓意图有链上确认延迟。机器人已内置 60 秒等待。如果超时，手动重试 `python main.py close-all`。

### 余额不足
确认 PaperTrade 钱包和 ONDO 账户都有足够的 USDC。PaperTrade 至少需要 `HEDGE_POSITION_SIZE / HEDGE_PAPER_LEVERAGE * 1.5` USDC。

### Web 面板日志没有数据
确保使用 `python web_server.py` 启动服务。服务已内置 `-u` 无缓冲输出，日志会实时写入 `bot.log`。

---

## 验证测试

快速验证系统是否正常：

```bash
cd /Users/caroline/Desktop/源代码/demo/paper中性脚本

# 模块导入
python -c "import paper_client, ondo_client, hedge_bot, mock_clients, main; print('模块导入 OK')"

# 模拟模式完整流程
HEDGE_MODE=mock HEDGE_MAX_CYCLES=1 HEDGE_MAX_HOLD_SECONDS=10 python main.py

# ONDO 行情 API
python -c "
from ondo_client import OndoClient, OndoConfig
c = OndoClient(OndoConfig(key_id='t', api_secret='t'))
print('BTC:', c.get_mark_price('BTC-USD.P'))
"
```

## 安全提示

1. Session Key 只能交易不能提现，泄露不会丢失资金
2. 高杠杆注意强平风险，建议 PaperTrade 和 ONDO 使用相同杠杆
3. 开仓时间差可能导致对冲不完全，建议仓位不要太大
4. PAPER 代币及时卖出锁定收益
5. Web 服务仅监听 `127.0.0.1`，不对外暴露
6. 默认模拟模式，避免误触发真实交易
