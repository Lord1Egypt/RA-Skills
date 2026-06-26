# MT4 智能交易桥 · 量化自动交易系统

MT4 智能交易桥。通过文件 I/O 与 MT4 EA 通信，无需 DLL 或额外依赖。支持 OpenClaw（小龙虾 AI Agent）通过微信 / 飞书 / Telegram 等渠道直接操作 MT4 交易。

> **关键词**：MT4, MetaTrader 4, 外汇交易, Python交易, 算法交易, 自动交易, 网格策略, 支撑压力位, ATR止损, 移动止损, 黄金交易, 原油交易, 比特币交易, OpenClaw, 小龙虾, AI交易助手, 微信操作MT4, 飞书操作MT4




## 🎯 自然语言交互示例

### 📱 微信/飞书/Telegram 口语化命令

| 你说 | MT4 做 |
|-----|--------|
| 黄金多少钱 | 返回 XAUUSD.s 实时报价 |
| 买黄金 0.05 手 | 市价买入 0.05 手 |
| 平仓 95832104 | 平掉指定订单 |
| 全平 | 平掉所有持仓 |
| 查持仓 | 列出当前所有持仓 |
| 设置止损 95832104 4500 | 设置止损位 |
| 启动黄金网格 | 启动黄金网格策略 |
| 获取MT4 黄金的1小时K线数据进行行情分析 | 将会自动帮您分析好黄金后市走向以及给出交易方案 |


---

## 文件结构

```
mt4-trader/
├── SKILL.md                         # 本使用说明
├── mql4/                            # MT4 EA 编译文件（.ex4，由脚本生成）
│   [用户手动下载 .ex4 文件放到此目录]
├── scripts/                         # Python 脚本
│   ├── mt4_client.py                # Python 交易客户端（核心）
│   ├── deploy_ex4.py                # EA 部署指引（显示下载链接和安装步骤）
│   ├── alert_commands.py            # 价格预警命令行工具
│   ├── position_summary.py          # 持仓汇总（命令行输出）
│   ├── position_summary_cron.py     # 持仓汇总（定时推送）
│   ├── sr_strategy.py               # 支撑压力位策略编排
│   └── summary_utils.py             # 持仓汇总工具模块
└── references/
    └── api_docs.md                  # 完整 API 参考文档
```

---

## 安装步骤（详细版）

### 第一步：找到你的 MT4 数据目录

每个 MT4 安装实例都有一个专属的数据目录，格式为：

```
%APPDATA%\MetaQuotes\Terminal\<32位随机ID>
```

例如：`C:\Users\Administrator\AppData\Roaming\MetaQuotes\Terminal\ABC123...`

> 怎么找？在 MT4 中按 `F7` 打开 MetaEditor（代码编辑器），点击菜单 `文件 → 打开数据文件夹`，弹出的路径就是你的 MT4 数据目录。

### 第二步：确认 MT4 安装目录

EA 文件需要部署到两个不同的目录：

| EA 文件 | 目标目录 | 说明 |
|---------|---------|------|
| `mt4_bridge.ex4` | `MT4安装目录\MQL4\Experts\` | 主程序 EA（必须） |
| `芝麻网格V2.ex4` | `MT4安装目录\MQL4\Experts\` | 网格策略 EA（可选） |
| `tools2.3.ex4` | `MT4安装目录\MQL4\Libraries\` | **网格策略依赖库**（网格必须，不是 Experts！） |

> ⚠️ `Libraries` 目录与 `Experts`、`Indicators` 同级，**不是** `Experts` 的子目录。

典型路径结构：
```
C:\Program Files (x86)\EBC Financial Group Cayman MT4 Terminal\MQL4\
├── Experts\           ← mt4_bridge.ex4, 芝麻网格V2.ex4 放这里
│   ├── mt4_bridge.ex4
│   └── 芝麻网格V2.ex4
├── Libraries\         ← tools2.3.ex4 放这里（与 Experts 同级！）
│   └── tools2.3.ex4
├── Indicators\
└── Scripts\
```

### 第三步：下载 .ex4 文件

从 Gitee 仓库下载 3 个 .ex4 文件：

https://gitee.com/3603317/skill-plugin/tree/master/mt4

需要下载的文件：

| 文件 | 说明 |
|------|------|
| `mt4_bridge.ex4` | 主程序 EA（**必选**） |
| `芝麻网格V2.ex4` | 网格策略 EA（可选） |
| `tools2.3.ex4` | 网格策略依赖库（选网格则必选） |

> 点击文件 → 点右上角 **Raw** 按钮即可保存到本地。

下载后放入 skills\mt4-trader\mql4\ 目录，然后运行以下命令一键部署到 MT4：

```bash
cd scripts\
python deploy_ex4.py deploy
```

### 第四步：在 MT4 中挂载 EA

**挂载 mt4_bridge（核心，必须操作）：**
1. 打开 MT4，按 `Ctrl+N` 打开左侧"导航器"面板
2. 展开"EA 交易"列表，找到 `mt4_bridge`
3. 用鼠标左键拖拽到任意品种图表上（推荐 XAUUSD.s 或主流品种）
4. 弹出 EA 属性对话框 → **选项卡"常用"**：
   - **允许实时交易** → ✅ 勾选（必须！）
   - **允许导入 DLL** → ✅ 勾选
   - **确认取消"手动交易禁止"** 等限制
5. 点"确定"关闭对话框
6. 图表右上角显示一个 EA 图标：
   - 😊 **绿色笑脸** → ✅ 正常工作中
   - 😢 哭脸或灰脸 → 检查下面"第五步"的自动交易按钮
7. **右键图表 → 属性 → 常用** 中可修改 EA 输入参数（可选）

**可选：挂载芝麻网格 EA：**
1. 将 `芝麻网格V2` EA 拖到需要跑网格的品种图表上（如 XAUUSD.s、XTIUSD.s）
2. 勾选"允许实时交易"
3. **确认 `tools2.3.ex4` 已放在 `Libraries\` 目录中**，否则网格 EA 无法运行

**多图表挂载（重要）：**
- mt4_bridge EA 可以挂载在**多个品种**的图表上（例如黄金一个图表、原油一个图表）
- 每个 EA 实例自动通过品种专属请求文件区分，不会互相干扰
- Python 客户端传了 `symbol` 参数后，会自动路由到对应的品种请求文件

### 第五步：开启自动交易

这是新手最容易忽略的一步！

1. 在 MT4 工具栏上方找到 **"自动交易"按钮**（一个黄色播放 ▶️ 图标）
2. 如果它是 **灰色** 的 → 点击一下，变成 **绿色** ✅
3. 此时所有已挂载的 EA 图标都应变成 **绿色笑脸** 😊
4. 如果某个 EA 还是哭脸，右键该 EA 图标 → "属性" → 勾选"允许实时交易"

> 💡 每次重启 MT4 后，自动交易按钮默认为关闭状态，需要手动开启。
> 建议在 MT4 设置中勾选"启动时启用自动交易"。

### 第六步：验证部署是否成功

**方法一：脚本检查**
```bash
cd scripts\
python mt4_client.py
```
如果看到类似下面的交互菜单，说明通信正常：
```
=== MT4 交易助手 ===
1. 获取报价  2. 查询持仓  3. 交易  4. 网格策略
请输入指令：
```

**方法二：Python 代码验证**
```python
from mt4_client import MT4Client
client = MT4Client()

# 获取账户信息（确认通信正常）
info = client.get_account_info()
print(info)  # 应该看到余额、净值、可用保证金

# 获取实时报价
price = client.get_price("XAUUSD.s")
print(price) # 应该看到 bid/ask 价格
```

**如果返回 `"MT4 超时未响应"`：**
- MT4 在运行吗？→ 打开 MT4
- EA 挂载了吗？→ 图表上有没有 EA 图标
- 自动交易开了吗？→ 工具栏自动交易按钮是绿色吗
- EA 属性中"允许实时交易"勾了吗？→ 右键 EA 图标检查

---

## 核心 Python 方法

```python
from mt4_client import MT4Client
client = MT4Client()

# === 行情 ===
client.get_price("XAUUSD.s")             # 获取实时报价（bid/ask）
client.get_positions()                    # 查询持仓列表
client.get_account_info()                 # 账户余额/净值/保证金
client.get_history(7)                     # 历史订单（最近 7 天）

# === 交易 ===
client.buy(symbol="XAUUSD.s", lots=0.03)  # 市价买入 0.03 手
client.sell(symbol="XAUUSD.s", lots=0.03) # 市价卖出 0.03 手
client.close(ticket=123456)               # 平指定订单
client.close_all()                        # 一键全平
client.partial_close(ticket=123456, lots=0.02) # 部分平仓

# === 止损止盈 ===
client.set_sl(ticket=123456, sl=75000)          # 设置止损
client.set_tp(ticket=123456, tp=80000)          # 设置止盈
client.modify_order(ticket=123456, sl=75000, tp=80000) # 同时修改
client.auto_sl(ticket=123456, risk_percent=2.0) # 按账户 2% 风险自动止损
client.atr_sl(ticket=123456, period=14, multiplier=2.0) # ATR 止损
client.trailing_stop(ticket=123456, distance=300) # 移动止损（300 点间距）

# === 平所有多单/空单 ===
client.close_all_buy()                     # 平所有多单
client.close_all_sell()                    # 平所有空单
client.close_profit()                      # 平所有盈利单
client.close_loss()                        # 平所有亏损单

# === 挂单 ===
client.buy_limit(symbol="XAUUSD.s", lots=0.03, price=4500.0)  # 限价买入
client.sell_limit(symbol="XAUUSD.s", lots=0.03, price=4600.0) # 限价卖出
client.buy_stop(symbol="XAUUSD.s", lots=0.03, price=4700.0)   # 买入止损（突破追涨）
client.sell_stop(symbol="XAUUSD.s", lots=0.03, price=4500.0)  # 卖出止损（破位追空）
client.get_pending_orders()                # 查询当前挂单
client.cancel_pending(ticket=123456)       # 取消挂单

# === OCO 订单（二选一挂单） ===
client.oco_order(symbol="XAUUSD.s", lots=0.03,
    order1={"type": "buy_stop",  "price": 77000, "sl": 76500},
    order2={"type": "sell_stop", "price": 76000, "sl": 76500}
)

# === 手数计算 ===
client.calc_lots(symbol="XAUUSD.s", risk_percent=1.0, sl_distance=5.0)
# 1% 风险，止损 5 美元 → 返回建议手数

# === K 线数据（量化分析用） ===
client.get_klines(symbol="XAUUSD.s", timeframe="H1", count=20)   # H1 最近 20 根
client.get_klines(symbol="XAUUSD.s", timeframe="M15", count=100) # M15 最近 100 根
client.get_klines(symbol="XAUUSD.s", timeframe="D1", count=30)   # 最近 30 根日线

# === 支撑压力位 ===
client.get_sr_levels(symbol="XAUUSD.s")      # 获取支撑压力位
client.draw_sr_levels(symbol="XAUUSD.s")     # 在图表上画出支撑压力位线
client.clear_chart_objects(symbol="XAUUSD.s")  # 清除图表上所有对象
client.draw_hline(symbol="XAUUSD.s", name="R1", price=4750)  # 画自定义水平线
client.clear_hline(symbol="XAUUSD.s", prefix="HL_")  # 按前缀删除水平线
```

> ⚠️ **重要：使用关键字参数！**
> 所有交易方法（buy/sell/close/set_sl 等）**必须使用关键字参数**传参：
> ```python
> # ✅ 正确
> client.buy(symbol="XAUUSD.s", lots=0.03)
> client.set_sl(ticket=123456, sl=75000)
>
> # ❌ 错误——按位置传参可能会导致 order 4106（交易被禁用）
> client.buy(0.03, "XAUUSD.s")      # 顺序可能不对！
> ```

---

## 网格策略（芝麻网格 EA）

| 命令 | 说明 |
|------|------|
| `client.grid_start(symbol="XAUUSD.s")` | 启动网格 |
| `client.grid_stop(symbol="XAUUSD.s")` | 停止网格（不再开新单） |
| `client.grid_close_all(symbol="XAUUSD.s")` | 平掉所有网格持仓单 |
| `client.grid_status(symbol="XAUUSD.s")` | 查询网格运行状态 |
| `client.grid_set_sl_tp(symbol="XAUUSD.s")` | 批量设置网格单的止损止盈 |

> ⚠️ **平网格仓必须按以下顺序分两步执行：**
> ```python
> client.grid_stop(symbol="XAUUSD.s")        # 第一步：停止网格
> client.grid_close_all(symbol="XAUUSD.s")   # 第二步：平掉所有网格单
> ```
> **不可直接用 `close_all()` 平网格单**。`close_all` 命令会拒绝 magic=777777（网格单）。
> 网格单必须走芝麻网格 EA 自己的关闭通道。

---

## 价格预警（可选）

```bash
cd scripts\

python alert_commands.py profit 20        # 总盈利达到 $20 时提醒
python alert_commands.py above 77000      # BTC 突破 77000 时提醒
python alert_commands.py below 75000      # BTC 跌破 75000 时提醒
python alert_commands.py list             # 查看当前所有预警
python alert_commands.py clear            # 清除所有预警
python alert_commands.py cancel 3        # 取消第 3 号预警
```

---

## 品种代码

| 品种 | 代码 | 说明 |
|------|------|------|
| 黄金 | `XAUUSD.s` | XAUUSD 后缀 .s 是部分经纪商标准 |
| 比特币 | `BTCUSD` | 部分平台为 BTCUSD.pro |
| 原油 | `XTIUSD.s` | 美国原油（WTI） |
| 白银 | `XAGUSD.s` | 现货白银 |

> 品种代码精确格式因经纪商而异。如果 get_price 找不到品种，在 MT4 市场报价中右键 → "全部显示"确认准确的品种名。

---

## 通信原理

```
┌──────────┐    JSON 文件     ┌──────────────┐
│  Python   │ ───request────→ │  MT4 EA      │
│  Client   │ ←──response──── │  (on chart)   │
└──────────┘    JSON 文件     └──────────────┘
```

- **共享目录**：`%APPDATA%\MetaQuotes\Terminal\Common\Files\mt4_bridge\`
  - 示例：`C:\Users\Administrator\AppData\Roaming\MetaQuotes\Terminal\Common\Files\mt4_bridge\`
- **请求文件**：`request_{品种}.json`（如 `request_XAUUSD.s.json`）
- **响应文件**：`response_{品种}.json`
- **协议**：JSON over 文件（零 DLL 依赖）
- **超时**：5 秒（Python 客户端默认配置）
- **多品种支持**：多个 EA 实例通过品种专属文件名自动区分

---

## 常见问题排查

| 现象 | 可能原因 | 解决方法 |
|------|---------|---------|
| MT4 超时未响应 | EA 未挂载或自动交易未启动 | 确认图表右上角为绿色笑脸 😊 |
| error 4106（交易禁用） | EA 属性中"允许实时交易"未勾选 | 右键 EA → 属性 → 勾选"允许实时交易" |
| 找不到价格（空结果） | 品种代码不匹配 | 在 MT4 市场报价中确认精确名称 |
| tools2.3 编译报错 | 文件放错了目录 | 确认 tools2.3.ex4 在 `MQL4\Libraries\`，**不是** Experts\ |
| 重复下单 | 多个 EA 读同一个请求文件 | 使用 v1.84+ 版本，自动使用品种专属文件 |
| BTC 无法市价交易 | 部分经纪商禁用 BTC 市价单 | 改用 `buy_limit()`/`sell_limit()` 限价单 |
| 重启 MT4 后 EA 不跑 | 自动交易默认关闭 | 手动点绿色播放按钮，或在设置中勾选"启动时启用" |
| 芝麻网格周末不运行 | 经纪商周末休市 | 正常现象，周一开市自动恢复 |

---

## 交流与反馈

欢迎加入 **MT4 自动化技术交流群**，一起讨论 MT4 自动交易、Python 量化、EA 开发等话题。


微信搜索：jiaoyibaohe    （老码农）   加我好友，备注 **MT4** 即可拉入群聊。

[或进入gitee项目主页，查看群二维码](https://gitee.com/3603317/skill-plugin/tree/master)

https://gitee.com/3603317/skill-plugin/tree/master

> 📱 扫码添加微信好友，备注 **MT4** 即可拉入技术交流群。
> 群内可交流：安装问题、使用技巧、功能建议、Bug 反馈。

---

## 版本信息

| 文件 | 版本 | 最后更新 |
|------|------|---------|
| mt4_bridge.ex4 | v1.86 | 2026-05 |
| 芝麻网格V2.ex4 | v1.41 | 2026-03 |
| tools2.3.ex4 | v2.3 | 2025-12 |
| mt4_client.py | v1.86 | 2026-05-05 |
| deploy_ex4.py | v1.0.7 | 2026-05-05 |
---

# MT4 Trading Bridge · Automated Trading System

MT4 Trading Bridge communicates with MT4 EA via file I/O — zero DLLs, zero extra dependencies. Supports OpenClaw AI Agent to control MT4 trading through WeChat / Feishu / Telegram and other channels.

> **Keywords**: MT4, MetaTrader 4, Forex Trading, Python Trading, Algorithmic Trading, Automated Trading, Grid Strategy, Support & Resistance, ATR Stop Loss, Trailing Stop, Gold Trading, Crude Oil Trading, Bitcoin Trading, OpenClaw, AI Trading Assistant

---

## File Structure

```
mt4-trader/
├── SKILL.md                         # This documentation
├── mql4/                            # MT4 EA compiled files (.ex4, generated by script)
│   [Manually download .ex4 files here]
├── scripts/                         # Python scripts
│   ├── mt4_client.py                # Python trading client (core)
│   ├── deploy_ex4.py                # EA deployment guide (shows download links & steps)
│   ├── alert_commands.py            # Price alert CLI tool
│   ├── position_summary.py          # Position summary (CLI output)
│   ├── position_summary_cron.py     # Position summary (scheduled push)
│   ├── sr_strategy.py               # Support/Resistance strategy orchestrator
│   └── summary_utils.py             # Position summary utility module
└── references/
    └── api_docs.md                  # Full API reference
```

---

## Installation

### Step 1: Find Your MT4 Data Directory

Each MT4 installation has a unique data directory:

```
%APPDATA%\MetaQuotes\Terminal\<32-char-random-ID>
```

> How to find it? In MT4, press F7 to open MetaEditor, then click File -> Open Data Folder.

### Step 2: Confirm MT4 Directory

EA files go into two directories:

| EA File | Target Directory | Notes |
|---------|-----------------|-------|
| mt4_bridge.ex4 | MT4_Install_Dir\MQL4\Experts\ | Core EA (required) |
| SesameGridV2.ex4 | MT4_Install_Dir\MQL4\Experts\ | Grid strategy EA (optional) |
| tools2.3.ex4 | MT4_Install_Dir\MQL4\Libraries\ | Grid dependency (required if using grid) |

> Libraries is at the same level as Experts — NOT a subdirectory of Experts.

### Step 3: Download .ex4 Files

From Gitee: https://gitee.com/3603317/skill-plugin/tree/master/mt4

Files: mt4_bridge.ex4 (required), SesameGridV2.ex4 (optional), tools2.3.ex4 (grid dependency).

### Step 4: Attach EAs in MT4

Drag mt4_bridge onto any chart. In properties -> Common tab: check "Allow live trading" and "Allow DLL imports". Green smiley means working.

Optional: Attach SesameGridV2 on grid-trading charts.

### Step 5: Enable Auto Trading

Click the yellow play icon (unicode triangle) on MT4 toolbar to turn it green.

### Step 6: Verify

Run: python mt4_client.py

---

## Core Python Methods

```python
from mt4_client import MT4Client
client = MT4Client()

# Market Data
client.get_price("XAUUSD.s")           # Real-time quote
client.get_positions()                 # Open positions
client.get_account_info()              # Account info
client.get_history(7)                  # Order history (7 days)

# Trading
client.buy(symbol="XAUUSD.s", lots=0.03)
client.sell(symbol="XAUUSD.s", lots=0.03)
client.close(ticket=123456)
client.close_all()                     # Close all positions

# SL/TP
client.set_sl(ticket=123456, sl=75000)
client.set_tp(ticket=123456, tp=80000)
client.modify_order(ticket=123456, sl=75000, tp=80000)
client.trailing_stop(ticket=123456, distance=300)

# Pending Orders
client.buy_limit(symbol="XAUUSD.s", lots=0.03, price=4500.0)
client.sell_limit(symbol="XAUUSD.s", lots=0.03, price=4600.0)
client.buy_stop(symbol="XAUUSD.s", lots=0.03, price=4700.0)
client.sell_stop(symbol="XAUUSD.s", lots=0.03, price=4500.0)
client.get_pending_orders()
client.cancel_pending(ticket=123456)

# Kline Data
client.get_klines(symbol="XAUUSD.s", timeframe="H1", count=20)

# Support & Resistance
client.get_sr_levels(symbol="XAUUSD.s")
client.draw_sr_levels(symbol="XAUUSD.s")
client.clear_chart_objects(symbol="XAUUSD.s")  # Clear all chart objects
client.draw_hline(symbol="XAUUSD.s", name="R1", price=4750)  # Draw horizontal line
client.clear_hline(symbol="XAUUSD.s", prefix="HL_")  # Delete lines by prefix
```

> Use keyword arguments for all trading methods!

---

## Grid Strategy

| Command | Description |
|---------|-------------|
| grid_start(symbol) | Start grid |
| grid_stop(symbol) | Stop grid |
| grid_close_all(symbol) | Close grid orders |
| grid_status(symbol) | Check status |

For closing grid: call grid_stop() first, then grid_close_all().

---

## Symbol Codes

| Instrument | Code |
|------------|------|
| Gold | XAUUSD.s |
| Bitcoin | BTCUSD |
| Crude Oil | XTIUSD.s |
| Silver | XAGUSD.s |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MT4 Timeout | EA not attached or auto-trading off |
| error 4106 | "Allow live trading" unchecked |
| Empty price result | Wrong symbol code |
| Duplicate orders | Use v1.84+ for symbol-specific files |
| BTC market order fails | Some brokers disable BTC market orders |
---

## Communication & Feedback
Join the **MT4 Automated Trading Technical Group** to discuss MT4 auto trading, Python quantitative trading, EA development, and more.

Search WeChat: jiaoyibaohe (MT4 Developer) — add me as a friend, note **MT4** to join the group.

[Click to view Gitee project homepage, group QR code](https://gitee.com/3603317/skill-plugin/tree/master)

> Scan the QR code to add WeChat friend, note **MT4** to join the technical group.
> Topics: installation issues, usage tips, feature suggestions, bug reports.

---
