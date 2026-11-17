# PaperTrade + ONDO Perps 中性对冲机器人教程

## 相关平台

### 对冲交易平台

[PaperTrade](https://papertrade.xyz/) &nbsp;|&nbsp; [ONDO](https://app.ondoperps.xyz/?ref=8RU3VB)

### 新手推荐

**加密货币获取：** [OKX](https://www.mitxcqvwnhj.com/join/9122359) &nbsp;|&nbsp; [币安](https://www.bsmkweb.cc/register?ref=35266688)

**自动化平台：** [Minara](https://minara.ai/r/23EUC6)

**AI 本地使用：** [购买 GPT](https://www.gamsgo.com/partner/JwUY7)

---

## 策略原理

利用 PaperTrade 的独特经济模型进行"亏损即挖矿"：

1. 在 **PaperTrade** 和 **ONDO** 同时开方向相反的仓位（完美对冲）
2. 无论价格涨跌，PaperTrade 一侧必然亏损 → **mint PAPER 代币**（约 95 PAPER/$1 亏损）
3. ONDO 一侧必然盈利 → 获得 **交易积分 + USDC**
4. 净 PnL ≈ 0（仅扣除 ONDO 手续费约 0.05% 往返）
5. **收益 = PAPER 代币 + ONDO 积分**

### 为什么 PaperTrade 亏损是"划算"的？

- PaperTrade 亏损不额外收费，反而 mint PAPER
- 盈利有 asymmetric haircut（小盈利几乎被吃光）
- 因此亏损侧放在 PaperTrade 是最优选择

---

## 快速开始

### 方式一：Web 控制面板（推荐）

提供可视化界面，支持配置填写、模式切换、一键启动、实时日志。

```bash
cd paper中性脚本
python web_server.py
```

然后在浏览器打开 **http://localhost:8765/**

面板功能：
- 🧪 **模拟模式**：无需任何凭证，直接演示完整流程（默认）
- 💰 **真实模式**：配置私钥和 API 后进行真实交易
- 🌐 **中英文切换**
- 🌐 **访问官网**：PaperTrade / ONDO 配置卡片右上角直达官网
- 🔑 **获取 ONDO API Key**：ONDO 配置区一键跳转
- 📊 **实时日志**：每 3 秒自动刷新

### 方式二：命令行

#### 1. 安装依赖

```bash
cd paper中性脚本
pip install -r requirements.txt
```

依赖：`eth-account`, `requests`, `python-dotenv`

#### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，填入以下内容：

```ini
# ── 运行模式 ──
# mock = 模拟模式（不进行真实交易，用于演示）
# real = 真实模式（进行真实交易，需要配置凭证）
HEDGE_MODE=mock

# PaperTrade 钱包私钥（0x 开头的 64 位 hex）
PAPER_WALLET_PRIVATE_KEY=0x你的私钥

# PaperTrade Session Key（可选，运行 register 后填入可避免重复注册）
PAPER_SESSION_KEY=

# ONDO Perps API 凭证（从 ONDO 后台创建 API Key）
ONDO_KEY_ID=ondoKeyId_你的key_id
ONDO_API_SECRET=ondoApiSecret_你的secret

# ── 对冲策略参数 ──
HEDGE_SYMBOL=BTC                  # 交易对：BTC 或 ETH
HEDGE_POSITION_SIZE=50            # 每侧名义仓位价值 (USD)
HEDGE_PAPER_LEVERAGE=10           # PaperTrade 杠杆 (1-1000)
HEDGE_ONDO_LEVERAGE=10            # ONDO 杠杆 (BTC/ETH 最大 25)
HEDGE_TARGET_MOVE_PCT=1.0         # 触发平仓的价格变动百分比
HEDGE_MAX_HOLD_SECONDS=3600       # 最长持仓时间（秒）
HEDGE_POLL_INTERVAL=10            # 价格轮询间隔（秒）
HEDGE_MAX_CYCLES=200              # 最大循环轮次
HEDGE_DIRECTION=random            # random | paper_long | paper_short
```

#### 3. 注册 Session Key（真实模式）

PaperTrade 使用 Session Key 机制：钱包签名注册一个只能交易、不能提现的会话密钥。

```bash
python main.py register
```

将输出的 `PAPER_SESSION_KEY` 填入 `.env`，后续运行就不会重复注册。

#### 4. 查看账户状态

```bash
python main.py status
```

#### 5. 运行对冲机器人

```bash
python main.py
```

#### 6. 紧急平仓

```bash
python main.py close-all
```

---

## 命令一览

| 命令 | 说明 |
|------|------|
| `python web_server.py` | 启动 Web 控制面板 |
| `python main.py` | 运行对冲机器人 |
| `python main.py status` | 查看两平台账户状态 |
| `python main.py close-all` | 平掉所有持仓 |
| `python main.py register` | 注册 PaperTrade Session Key |

---

## 核心参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `HEDGE_POSITION_SIZE` | 50 | 每侧名义仓位（USD），实际保证金 = size / leverage |
| `HEDGE_TARGET_MOVE_PCT` | 1.0 | 价格波动达到此百分比时平仓（如 1.0 = 1%） |
| `HEDGE_MAX_HOLD_SECONDS` | 3600 | 最长持仓时间，超时强制平仓 |
| `HEDGE_POLL_INTERVAL` | 10 | 价格轮询间隔（秒） |
| `HEDGE_MAX_CYCLES` | 200 | 最大循环轮次 |
| `HEDGE_DIRECTION` | random | 开仓方向策略 |
| `HEDGE_MODE` | mock | 运行模式（mock 模拟 / real 真实） |

### 方向策略

- `random`：随机选择 PaperTrade 做多或做空（推荐，平衡 PAPER mint）
- `paper_long`：PaperTrade 做多，ONDO 做空
- `paper_short`：PaperTrade 做空，ONDO 做多

---

## 模拟模式说明

设置 `HEDGE_MODE=mock` 后，机器人使用内置的模拟客户端，**不会进行任何真实交易**：

- 无需配置私钥和 ONDO API 凭证
- 使用固定测试钱包自动运行
- 输出与真实模式完全一致的日志格式
- 适合演示流程和学习使用

切换为真实模式：将 `HEDGE_MODE` 改为 `real`，并填入真实的私钥和 API 凭证。

---

## 项目结构

```
paper中性脚本/
├── paper_client.py     # PaperTrade 客户端（EIP-712 签名、Session Key、开平仓）
├── ondo_client.py      # ONDO Perps 客户端（HMAC 签名、市价单、查询）
├── mock_clients.py     # 模拟客户端（模拟模式使用，不进行真实交易）
├── hedge_bot.py        # 对冲核心逻辑（双向开仓、监控、平仓、统计）
├── main.py             # CLI 入口
├── web_server.py       # Web 控制面板后端
├── index.html          # Web 控制面板前端
├── .env.example        # 配置模板
├── requirements.txt    # 依赖
├── paper-ondo-hedge.md # Skill 技能文件
└── README.md           # 本教程
```

---

## 安全机制

### 开仓失败回滚
如果 PaperTrade 开仓成功但 ONDO 开仓失败，机器人会自动平掉 PaperTrade 仓位，避免单边暴露。

### Session Key 权限限制
- Session Key 只能提交交易意图，**不能提现**
- 即使 Session Key 泄露，攻击者也无法转走资金
- 过期后自动重新注册

### 浮点数精度保护
使用 `Decimal` 精确转换 USD → wad（18 位精度），避免浮点误差导致开仓金额错误。

### 持仓确认等待
开仓后等待 PaperTrade 意图在链上确认，再开始价格监控，避免平仓时找不到仓位。

### Web 服务安全
- Web 服务仅监听 `127.0.0.1`，不对外暴露
- 私钥输入框使用 `type="password"` 隐藏
- 模拟模式为默认模式，避免误触发真实交易

---

## 常见问题

### Q: PaperTrade 平仓时报错找不到仓位？
A: 开仓意图有几秒到几十秒的确认延迟。机器人已内置等待逻辑（最多 60 秒）。如果超时仍未确认，平仓可能失败，可用 `python main.py close-all` 手动重试。

### Q: ONDO 签名错误？
A: ONDO 的签名格式可能随版本变化。如遇签名错误，请修改 `ondo_client.py` 中 `_sign` 方法的签名串格式。标准模式为 `HMAC-SHA256(secret, timestamp + method + path + body)`。

### Q: PAPER mint 数量统计为 0？
A: PAPER mint 有链上结算延迟。平仓后等待 5 秒再统计。如果仍为 0，可能本轮 PaperTrade 侧盈利（盈利不 mint PAPER），可设置 `HEDGE_DIRECTION` 或等待波动更大的行情。

### Q: 净 PnL 是正还是负？
A: 理想情况下净 PnL 略为负（约 -0.05% ONDO 手续费）。实际可能因开仓时间差和滑点有偏差。收益主要来自 PAPER 代币。

### Q: Web 面板日志没有数据？
A: 确保使用 `python web_server.py` 启动，服务会自动处理输出缓冲。如果仍无数据，检查 `bot.log` 文件是否生成。

---

## 风险提示

1. **开仓时间差**：两平台开仓有时间差，期间价格波动可能导致对冲不完全
2. **强平风险**：高杠杆时需注意两平台的维持保证金
3. **PAPER 价格波动**：PAPER 代币本身价格波动大，及时卖出锁定收益
4. **API 限额**：避免轮询过于频繁触发 API 限流
5. **ONDO 手续费**：每次开平仓都有手续费，仓位过小可能不划算
6. **模拟模式不产生收益**：模拟模式仅用于流程演示，不会 mint PAPER 或获得 ONDO 积分

---

## 验证测试

运行以下命令验证安装：

```bash
# 模块导入测试
python -c "import paper_client, ondo_client, hedge_bot, mock_clients, main; print('OK')"

# 模拟模式完整流程测试
HEDGE_MODE=mock HEDGE_MAX_CYCLES=1 HEDGE_MAX_HOLD_SECONDS=10 python main.py

# 公开 API 连通测试
python -c "
from ondo_client import OndoClient, OndoConfig
c = OndoClient(OndoConfig(key_id='t', api_secret='t'))
print('BTC:', c.get_mark_price('BTC-USD.P'))
print('ETH:', c.get_mark_price('ETH-USD.P'))
"
```
