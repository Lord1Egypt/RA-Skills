# 📰 Odaily星球日报 · 加密市场智能助手

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


**专为加密市场从业者打造的实时情报引擎——整合 Odaily 星球日报资讯、Polymarket 预测市场信号、CoinGecko 链上行情，在 OpenClaw Agent 中一键获取多维度加密市场快照。**

---

## ✨ 核心特性

- **📌 AI 提炼今日必关注**：从 Odaily Web API 实时拉取文章 + 快讯，AI 自动筛选最具影响力的事件，生成分析性标题（非照抄原文），附真实 Odaily 原文链接
- **📊 主流币实时行情**：BTC/ETH/SOL/BNB/XRP 价格、24h 涨跌、全市场总市值、合约指标、涨跌榜，基于 CoinGecko API 实时拉取
- **📅 明日关注日历**：宏观经济预告 + 链上事件提示，提前布局风险与机会
- **🐳 Polymarket 巨鲸尾盘扫描**：实时监控先知频道最新异动快讯 + 扫描 $10,000+ 大额高胜率押注（price ≥ 0.95），Top 10 表格展示并自动翻译中文
- **🔌 API 模块化原始数据**：完整返回最新 5 篇文章 + 5 条快讯全文，适合二次开发和数据集成
- **🆓 零配置开箱即用**：核心功能无需任何 API Key，Supabase 持久化为可选项

> 💡 **注意**：使用本 Skill 会消耗您 OpenClaw Agent 绑定的 AI 模型 Token，请按需调用。

---

## 📥 安装指南

### 方法 A：使用 Openskills CLI（推荐）

```bash
openskills install git@github.com:odaily/odaily_plugin-.git
openskills sync
```

### 方法 B：使用 NPX

```bash
npx skills add https://github.com/odaily/odaily_plugin-
```

### 方法 C：手动集成

```bash
git clone https://github.com/odaily/odaily_plugin-.git \
  ~/.claude/skills/odaily

cd ~/.claude/skills/odaily
pip install -r requirements.txt
```

---

## 🚀 使用示例（5大板块真实场景）

### M1 · 今日必关注 — 开盘前的市场情报筛选

> **"帮我看看今天有哪些值得关注的加密新闻"**

Agent 从 Odaily Web API 实时获取最新文章和快讯，**不直接罗列原文**，而是 AI 主动筛选、提炼分析性标题，按影响权重排序，每条附真实 Odaily 原文链接。优先呈现：监管政策、机构动向、主流币重大事件、宏观数据发布。

```bash
python3 run.py get_today_watch '{"limit": 10}'
```

**触发关键词**：今日 / 必关注 / 头条 / 快讯 / 新闻

**输出示例（AI提炼，非原文标题）：**
```
🔴 SEC 对 Coinbase 的诉讼迎来关键庭审，判决或重塑交易所合规边界
   → 本周庭审将决定 Coinbase 是否需要注册为证券交易所...
   🔗 https://www.odaily.news/post/5193xxx

🟡 贝莱德比特币 ETF 单日净流入创两周新高，机构买盘重返市场
   → 昨日净流入 $4.2亿，为近14日峰值，与BTC价格反弹吻合...
   🔗 https://www.odaily.news/post/5193xxx
```

---

### M2 · 加密市场分析 — 实时行情 + 宏观联动判断

> **"现在 BTC 行情怎么样？宏观面有什么影响？"**

Agent 拉取全局市场数据（总市值、BTC 主导率）+ 主流币价格 + 合约指标（资金费率、多空比）+ 涨跌榜，结合 Odaily 宏观快讯 + 最新行情播报，AI 给出多空方向判断和近期风险提示。

```bash
python3 run.py get_crypto_market_analysis '{"focus": "overview"}'
```

**触发关键词**：行情 / 市场 / 走势 / 宏观 / 美联储 / fed / BTC / ETH / 比特币 / 以太坊 / 价格 / 涨跌 / 币价

**输出示例：**
```
📊 加密市场分析
════════════════════════
🌍 全局市场
  总市值: $2.48T (▲ +1.64%)
  BTC市占率: 56.57%  恐惧贪婪: 11 😱 极度恐惧

💰 主流币行情
  BTC   $70,203   ▲ +2.31% | 市值$1.4T
  ETH   $2,130    ▲ +3.27% | 市值$257.0B
  SOL   $90.10    ▲ +3.51% | 市值$51.5B

🏆 24H涨幅TOP5 / 💀 24H跌幅TOP5

🏦 宏观事件影响分析
  • 比特币现货ETF昨日总净流入1.67亿美元，过去3日净流出后首次净流入
  • 美国特拉华州提出稳定币监管法案...

📡 Odaily 行情播报
  1. 加密市场普遍反弹，BTC突破7万美元...
     ⏱ 03-24 10:25  🔗 https://www.odaily.news/zh-CN/newsflash/xxx

🤖 AI 分析：BTC 强势突破关键位，ETH 同步跟涨，山寨轮动信号初现...
```

---

### M3 · 明日关注 — 提前布局宏观风险日历

> **"明天有什么需要提前注意的事件？"**

Agent 整合 Odaily 快讯预告，结合宏观经济日历，输出明日高影响事件列表，每项附影响方向预判，最后给出综合建议。

```bash
python3 run.py get_tomorrow_watch '{}'
```

**触发关键词**：明日 / 明天 / 关注

**输出示例：**
```
📅 明日关注 | 03-24 (周二)

• 20:30  美国 2 月核心 PCE 数据发布
  → 若高于预期，或触发加密市场短期回调

• 22:00  以太坊 Pectra 升级最终测试网上线
  → 关注链上活跃度和 ETH 质押量变化

• 全天    Backpack Token 上线窗口（Polymarket 概率 99.9%）
  → 关注 SOL 生态联动效应

💡 综合建议：PCE 数据前控制杠杆，关注 ETH 升级催化。
```

---

### M4 · 预测市场异动 + 巨鲸尾盘跟单 — 读懂聪明钱信号

> **"Polymarket 上现在有什么大动作？巨鲸在押注什么？"**

Agent 先展示 Odaily Seer **先知频道**最新 5 条含实时概率变动的快讯（附 Odaily 原文链接），再扫描 Polymarket 上 $10,000+ 大额交易，筛选 price ≥ 0.95 的高确定性押注，Top 10 表格展示（事件自动翻译为中文）。

```bash
python3 run.py scan_whale_tail_trades '{"min_size": 10000, "min_price": 0.95}'
```

**触发关键词**：巨鲸 / 预测 / 尾盘 / polymarket

**输出示例：**
```
📡 Polymarket预测市场（先知频道最新）

1. "美伊停火"概率短时从10%飙升至54%，后回落至16%
   ⏱ 03-23 20:12  🔗 https://www.odaily.news/zh-CN/newsflash/473498

2. "美军3月底前进入伊朗"概率从24%迅速跌至11%
   ⏱ 03-23 19:23  🔗 https://www.odaily.news/zh-CN/newsflash/473483

🎯 Top 10 高确定性尾盘交易

  #   事件                    方向       金额      胜率   巨鲸
  1   伊朗政权3月底倒台        🔴 NO    $50,000  98.3%  hild
  2   原油3月底触及$140        🟢 YES   $47,226  98.0%  Istaroth
  3   特朗普3月31日前卸任      🟢 YES   $42,667  99.7%  Team-TNT
```

---

### M5 · API 模块化调用 — 获取完整原始数据

> **"给我 Odaily 最新的 5 篇文章和 5 条快讯的完整内容"**

Agent 直接返回 Odaily 最新文章（含完整摘要）+ 最新快讯（含完整正文），所有内容原样输出不截断，适合用作下游数据源或二次分析。最后附 AI 基于全部内容的市场影响提炼。

```bash
python3 run.py get_api_module '{}'
```

**触发关键词**：API / 接口 / 模块

**输出格式：**
```
📰 最新文章（Top 5）

  1. [完整标题]
     [完整摘要，不截断]
     ✍️ 作者  ⏱ 时间
     🔗 https://www.odaily.news/post/xxx

⚡ 最新快讯（Top 5）

  1. [完整标题]
     [完整快讯正文，不截断]
     ⏱ 时间
     🔗 https://www.odaily.news/zh-CN/newsflash/xxx

💡 AI分析：基于以上内容提炼关键信息和市场影响
```

---

### 全板块日报

> **"给我今天的加密日报"** 或直接输入 **"日报"**

触发全部 5 个板块，按 M1→M2→M3→M4→M5 顺序完整输出：

```bash
# 第一批（并行执行）
python3 run.py get_today_watch '{"limit": 10}'
python3 run.py get_tomorrow_watch '{}'
python3 run.py scan_whale_tail_trades '{"min_size": 10000, "min_price": 0.95}'
python3 run.py get_api_module '{}'

# 第二批（CoinGecko 限速，间隔 ≥5s 后执行）
python3 run.py get_crypto_market_analysis '{"focus": "overview"}'
```

---

## 🛠️ 工具清单

| 板块 | 工具名 | 触发关键词 | 说明 |
|------|--------|-----------|------|
| M1 | `get_today_watch` | 今日 / 必关注 / 头条 / 快讯 / 资讯 / 热点 / 最新 / 要闻 / 动态 | Odaily Web API 文章+快讯，AI 提炼分析性标题 |
| M2 | `get_crypto_market_analysis` | 行情 / 市场 / 走势 / 宏观 / 美联储 / BTC / ETH / 比特币 / 以太坊 / 价格 / 涨跌 / 币价 | 主流币实时行情 + 宏观快讯 + Odaily行情播报 AI 综合分析 |
| M3 | `get_tomorrow_watch` | 明日 / 明天 / 关注 / 预告 / 日历 / 事件 / 下周 / 本周 | 宏观日历 + 链上事件预告 + 综合建议 |
| M4 | `scan_whale_tail_trades` | 巨鲸 / 预测 / 尾盘 / polymarket / 跟单 / 押注 / 先知 / 大户 / 聪明钱 / 胜率 | 先知频道快讯 + Polymarket 大额高胜率交易扫描 |
| M5 | `get_api_module` | API / 接口 / 模块 / 原始数据 / 抓取 / 数据源 | 完整返回 5 篇文章 + 5 条快讯原始数据 |

---

## ⚙️ 可选配置

核心功能**无需任何配置**即可使用。如需开启巨鲸交易数据持久化（历史去重查询），可在 `config/settings.py` 中配置 Supabase：

```python
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
```

---

## 📡 数据来源

- 加密新闻 / 快讯：[Odaily 星球日报](https://www.odaily.news)
- 预测市场异动：[Odaily Seer 先知频道](https://t.me/Odaily_Seer)
- 巨鲸交易 / 预测事件：[Polymarket](https://polymarket.com)
- 实时行情：[CoinGecko](https://www.coingecko.com)

---

## ⚠️ 免责声明

本 Skill 输出内容仅供信息参考，不构成任何投资建议。加密市场风险极高，请独立判断，谨慎决策。

---

📝 **License**: MIT License
