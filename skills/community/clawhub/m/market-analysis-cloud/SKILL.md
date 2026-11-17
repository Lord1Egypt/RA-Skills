---
name: 行情研判（云端版）
description: 每日A股行情研判编排器（纯云端版，无需MCP连接器，无需电脑开机）。分步执行：日历检查→行情数据→新闻简报→持股诊断→自选股分析→ERP计算→组装报告→上传IMA知识库。运行前请确保已安装依赖技能：stock-price-query-mx、tecent-finance、eastmoney-mx-skills-suite、china-stock-data。
agent_created: true
triggers:
  - "行情研判"
  - "市场分析"
  - "今晚研判"
  - "每日研判"
  - "cloud market analysis"
  - "云端研判"
---

# 行情研判（云端版 v1.0）

> 纯云端运行，不依赖桌面端 MCP（模型上下文协议）连接器。电脑关机也能通过 WorkBuddy App 云端模式定时执行。

---

## 🛠 首次使用：环境安装（必须执行）

本技能依赖以下 4 个市场技能。首次运行时，**先检查是否已安装**，未安装则逐条安装。

### 依赖技能清单

| # | 技能名 | 用途 | 安装链接 |
|---|---|---|---|
| 1 | **stock-price-query-mx** | A股/美股实时报价 | https://clawhub.ai/skills/stock-price-query-mx |
| 2 | **tecent-finance** | 腾讯财经 K 线/估值 | https://clawhub.ai/skills/tecent-finance |
| 3 | **eastmoney-mx-skills-suite** | 东方财富妙想（诊股/PE/国债/新闻） | https://clawhub.ai/kooui/skills/eastmoney-mx-skills-suite |
| 4 | **china-stock-data** | 通达信 K 线/ATR/技术指标 | https://longxiaskill.com/skill/china-stock-data |

安装方式：对 AI 说「请帮我安装 [技能名]，链接是 [链接]」即可。

### 环境变量

| 变量名 | 值 | 说明 |
|---|---|---|
| `MX_APIKEY` | `em_6gQd9wRX98tbIpu7Z6SPWICSKlHinpuk` | 东方财富妙想 API Key（诊股/PE/国债数据源） |

> 如 eastmoney-mx-skills-suite 提示 API Key 无效，请到 https://ai.eastmoney.com/mxClaw 重新领取。

### 安装验证

4 个技能全部安装 + MX_APIKEY 已配置后，回复「环境就绪」继续执行研判。

---

## 🏗 架构

```
编排器（本 Skill）
├── Step 0: 日历检查 → 交易日判断、时间窗口、日历因子
├── Step 1: 行情数据 → 8大指数 + 行业板块 + 涨跌家数
├── Step 2: 新闻简报 → 5类关键词搜索 + 结构化输出
├── Step 3: 持股诊断 → 读持仓 → 逐只诊股 → 四层过滤
├── Step 4: 自选股分析 → 读自选股 → 逐只诊股 → 四层过滤 → 风险评级
├── Step 5: ERP 计算 → 沪深300 PE + 国债收益率
├── Step 6: 组装 → 防呆验证 → 上传 IMA 知识库 → 确认摘要
```

## 🔌 数据源映射（云端版）

| 数据类型 | 桌面版 MCP | 【云端版】技能市场 |
|---|---|---|
| A股实时行情 | `data_quote` MCP（westock） | **stock-price-query-mx**（腾讯财经 qt.gtimg.cn） |
| A股K线/量价 | `data_kline` MCP（westock） | **tecent-finance**（腾讯财经 API） |
| 技术指标（MACD） | `data_technical` MCP（westock） | **china-stock-data**（含通达信 TDX） |
| 主力资金流向 | `data_fund_flow` MCP（westock） | **WebSearch** + 智能提取 |
| 行业板块 | `data_sector` MCP（westock） | **WebSearch** + 智能提取 |
| 美股指数 | `tdx_kline` MCP（通达信） | **stock-price-query-mx**（支持美股） |
| ATR（平均真实波幅） | `tdx_kline` MCP（通达信） | **china-stock-data**（含通达信 K 线） |
| 诊股（基本面/消息） | `mx_ashare_finance_data` MCP | **eastmoney-mx-skills-suite**（需 MX_APIKEY） |
| 新闻搜索 | `WebSearch` + `mx` MCP | **WebSearch**（智能提取日期+来源） |
| PE（市盈率）/国债 | `mx_macro_data` / `data_profile` MCP | **eastmoney-mx-skills-suite**（宏观模块） |
| 交易日历 | `data_trade_calendar` MCP（westock） | **WebSearch**「A股交易日历 YYYY-MM-DD」 |
| IMA 知识库 | `ima` MCP | **IMA 知识库**（云端可直接访问） |

## ⚠️ 核心规则（不可违反）

1. **静默执行**：各 Step 执行期间只输出进度提示，不输出冗余内容
2. **不跳过**：所有 Step 必须依次执行，不得省略任何一步
3. **不简化**：每个 Step 的输出必须包含所有规定字段，不得省略
4. **先验证再上传**：Step 6 防呆验证通过（exit 0）后才可上传 IMA
5. **最终只输出摘要**：上传成功后只输出确认摘要，不在对话中输出报告全文
6. **技能调用说明**：本 Skill 依赖的前置技能均已安装，直接使用即可

---

## Step 0: 日历检查（必须首先执行）

### 0.1 判断交易日

使用 WebSearch 搜索「A股交易日历 YYYY-MM-DD」，判断今日是否为交易日。

非交易日 → 输出「📅 今日休市，研判跳过」→ **结束，不上传**。

### 0.2 判断时间窗口

按当前北京时间（UTC+8）判定：

| 时间 | 窗口 |
|---|---|
| 00:00–09:00 | ① 盘前 |
| 09:00–11:30 | ② 早盘 |
| 11:30–13:00 | ③ 午休 |
| 13:00–15:00 | ④ 下午 |
| 15:00–24:00 | ⑤ 收盘后 |
| 周末/假日 | ⑥ 休市 |

### 0.3 日历因子输出

```markdown
## 日历检查
| 项目 | 状态 |
|:---|:---|
| 交易日 | ✅ / ❌ |
| 窗口 | ①~⑥ |
| 星期效应 | 星期一偏强 / 星期二偏强 / 星期三🔴偏弱 / 星期四偏弱 / 星期五震荡偏弱 |
| 季末 | 是🔴 / 否 |
| 财报季 | 是 / 否 |
```

2026 年节假日（硬编码）：元旦 01-01~02 / 春节 02-16~22 / 清明 04-04~06 / 劳动节 05-01~05 / 端午 06-19~21 / 中秋 09-24~26 / 国庆 10-01~08

---

## Step 1: 行情数据

### 1.1 8 大指数报价

**A股（6个）** — 使用 **stock-price-query-mx**：

查询上证指数(000001)、沪深300(000300)、中证500(000905)、中证2000(932000)、创业板指(399006)、科创50(000688)。从返回结果提取现价、涨跌幅。

**美股（2个）** — 使用 **stock-price-query-mx**：

查询纳斯达克(.IXIC)和标普500(.INX)最新收盘价和涨跌幅。

### 1.2 MACD 技术指标

使用 **china-stock-data** 查询 6 大 A 股指数的 MACD 金叉/死叉状态。

无此技能时，从 `tecent-finance` 获取近 20 日 K 线手动计算 MACD。

### 1.3 主力资金

使用 WebSearch 搜索「沪深300 主力资金 净流入 YYYY-MM-DD」，从搜索结果中提取资金流向数据。

### 1.4 行业板块排行

使用 WebSearch 搜索「A股板块涨幅排行 YYYY-MM-DD」，提取前 10 板块名称和涨跌幅。

### 1.5 涨跌家数

使用 WebSearch 搜索「A股涨跌家数 YYYY-MM-DD」，提取涨跌数量。

### 1.6 输出格式（固定，不可改）

```markdown
# 行情数据 YYYY-MM-DD HH:MM

## 8大指数
| 指数 | 现价 | 涨跌幅 | MACD | 主力资金 |
|:---|:---|:---|:---|:---|
| 上证指数 | XXXX | +X.XX% | 金叉/死叉 | 净流入/出 XX亿 |
| 沪深300 | XXXX | +X.XX% | 金叉/死叉 | 净流入/出 XX亿 |
| 中证500 | XXXX | +X.XX% | 金叉/死叉 | 净流入/出 XX亿 |
| 中证2000 | XXXX | +X.XX% | 金叉/死叉 | 净流入/出 XX亿 |
| 创业板指 | XXXX | +X.XX% | 金叉/死叉 | 净流入/出 XX亿 |
| 科创50 | XXXX | +X.XX% | 金叉/死叉 | 净流入/出 XX亿 |
| 纳指 | XXXX | +X.XX% | — | — |
| 标普500 | XXXX | +X.XX% | — | — |
（8行全填，不可省略）

## 行业板块前10
| 板块 | 涨跌幅 |
|:---|:---|
| ... | +X.XX% |

## 涨跌家数比
XX涨 / XX跌  (X:X)
```

### 1.7 保存

写入 `/tmp/market_data.md`。

---

## Step 2: 新闻简报

### 2.1 搜索当日新闻

**必须逐一执行以下 5 组 WebSearch**，每组搜索词包含当天完整日期（YYYY-MM-DD）：

1. `"A股 市场热点 板块 涨幅 YYYY-MM-DD"`
2. `"涨跌家数 上涨家数 下跌家数 A股 YYYY-MM-DD"`
3. `"主力资金 净流入 大盘 YYYY-MM-DD"`
4. `"财联社 早间新闻 YYYY-MM-DD"`
5. `"美股收盘 纳指 标普 道指 YYYY-MM-DD"`

如有 **eastmoney-mx-skills-suite**，优先使用其新闻搜索模块辅助。

### 2.2 输出格式（固定，不可改）

```markdown
# 新闻简报 YYYY-MM-DD HH:MM

## 政策
[事件1] [来源]
[事件2] [来源]
（≥1条，无则写「当日无重大政策新闻」）

## 海外
[事件1] [来源]
[事件2] [来源]
（≥1条）

## 行业
[事件1] [来源]
[事件2] [来源]
（≥1条）

## 盘面
涨跌家数: XX涨/XX跌 | 成交额: XXXX亿 | 主力资金: 净流入/出 XX亿

## 情绪
[2-3个关键词描述当日市场情绪]
```

### 2.3 保存

写入 `/tmp/market_news.md`。

---

## Step 3: 持股诊断

### 3.1 读取最新持仓文件

从 IMA 知识库「持仓和选股列表更新」文件夹（folder_id: `folder_7474447934047481`）读取最新持仓：

云端模式使用 IMA 知识库 API 浏览和读取持仓文件。

### 3.2 逐只诊股

对每只持仓：

1. **基本面诊断** — 使用 **eastmoney-mx-skills-suite** 的金融数据查询模块：
   查询 PE、PB、ROE、市值等。需配置 MX_APIKEY 环境变量。

2. **K线 + 量价** — 使用 **tecent-finance**：
   获取近 5 日 K 线，提取量比、是否突破 5 日高。

3. **ATR(14)**（平均真实波幅） — 使用 **china-stock-data**：
   拉 20 天日 K 线数据，计算 TR = max(H-L, |H-前收|, |L-前收|)，ATR(14) = SMA(TR, 14)。
   无此技能时，从 tecent-finance 获取 K 线手动计算。

4. **资金流向** — 使用 WebSearch「{股票名} 主力资金 净流入 YYYY-MM-DD」：
   从搜索结果提取主力资金数据。

### 3.3 四层串行过滤

```
① 基本面滤网 → PE为负 或 控股东减持超5亿 → 🔴 淘汰
② 消息面催化 → 有减持/异常波动/立案 → 🔴 淘汰
③ 技术面择时 → MACD金叉 + 不超买 + 放量 → ✅
④ 资金面验证 → 主力流入 → ✅
```

### 3.4 输出格式（固定）

```markdown
# 持股诊断 YYYY-MM-DD
| 标的 | 行业 | ATR | ①基本面 | ②消息 | ③技术 | ④资金 | 结论 |
|:---|:---|:---|:---|:---|:---|:---|:---|
| XX | XX | X.XX | ✅/🔴 | ✅/🔴 | ✅/🔴 | ✅/🔴 | 持有/减仓/加仓 |
> 共 XX 只持仓（全部列出，不可遗漏）

## 逐只详情
#### 标的名 代码 — 🟢🟡🔴 评级
- 基本面：PE=XX, 分位=XX%
- 消息：[利好/利空信息]
- 技术：MACD 金叉/死叉 | RSI=XX | 量比=X.X | ATR=X.XX
- 资金：主力净流入/流出 XX亿
- 建议：[具体操作建议]
```

### 3.5 保存

写入 `/tmp/market_portfolio.md`。

---

## Step 4: 自选股分析

### 4.1 读取自选股列表

从 IMA 知识库同一文件夹取最新自选股文件。

### 4.2 逐只诊股（流程同 Step 3.2）

⚠️ **每次只诊一只，不可并行。**

### 4.3 四层过滤（同 Step 3.3）

### 4.4 输出格式（固定）

```markdown
# 自选股分析 — YYYY-MM-DD HH:MM

## 过滤结果
| 标的 | 行业 | ATR | ①基本面 | ②消息 | ③技术 | ④资金 | 结论 |
|:---|:---|:---|:---|:---|:---|:---|:---|
| XX | XX | X.XX | ✅ | ✅ | ✅ | ✅ | 🟢 关注 |

## 逐只详情
#### 标的名 代码 — 🟢🟡🔴 评级
- 基本面：PE=XX, 分位=XX%
- 消息：[利好/利空信息]
- 技术：MACD 金叉/死叉 | RSI=XX | 量比=X.X | 突破5日高 是/否
- 资金：主力净流入/流出 XX亿
- 结论：[一句话结论]

## 综合评级汇总
| 评级 | 数量 | 标的 |
|:---|:---|:---|
| 🟢 重点关注 | X | ... |
| 🟡 观察 | X | ... |
| 🔴 淘汰 | X | ...（含淘汰原因） |
```

### 4.5 保存

写入 `/tmp/market_selfpick.md`。

---

## Step 5: ERP（股权风险溢价）计算

### 5.1 公式

```
ERP = (100 / 沪深300 PE(TTM)) — 10年期国债收益率
结果单位为百分比（%）。
```

### 5.2 获取 PE 和收盘价

使用 **eastmoney-mx-skills-suite** 的金融数据查询模块：

查询沪深300(000300.SH)的 PE(TTM)（市盈率滚动值）和收盘价。

### 5.3 获取国债收益率

使用 **eastmoney-mx-skills-suite** 的宏观数据模块：

查询中国 10 年期国债收益率。如当日数据未入库，回退至最近可用日期。

### 5.4 估值分段标准

| ERP 范围 | 估值水平 |
|---|---|
| ≥ 6.5% | 🔵 极度低估 |
| 5.5% ~ 6.5% | 🟢 低估 |
| 4.5% ~ 5.5% | 🟡 中等偏低 |
| 3.5% ~ 4.5% | 🟠 中等偏高 |
| 2.5% ~ 3.5% | 🔴 高估 |
| < 2.5% | ⭕ 极度高估 |

### 5.5 输出格式（固定）

```markdown
# 沪深300 ERP 日报 — YYYY-MM-DD HH:MM

| 指标 | 数值 |
|:---|:---|
| 沪深300 收盘价 | XXXX.XX |
| PE(TTM) | XX.XX |
| 10年国债收益率 | X.XX%（取值日期: YYYY-MM-DD） |
| **ERP（股权风险溢价）** | **X.XX%** |
| **估值水平** | **🟡 中等偏低** |

## 估值参考
| ERP | 估值 |
|:---|:---|
| ≥ 6.5% | 🔵 极度低估 |
| 5.5~6.5% | 🟢 低估 |
| 4.5~5.5% | 🟡 中等偏低 |
| 3.5~4.5% | 🟠 中等偏高 |
| 2.5~3.5% | 🔴 高估 |
| < 2.5% | ⭕ 极度高估 |
```

### 5.6 保存

写入 `/tmp/market_erp.md`。

---

## Step 6: 组装最终报告

### 6.1 读取中间结果

依次读取：`/tmp/market_data.md` → `/tmp/market_news.md` → `/tmp/market_portfolio.md` → `/tmp/market_selfpick.md` → `/tmp/market_erp.md`

### 6.2 固定模板（9 个章节，缺一不可）

```markdown
# 每日行情研判报告
> YYYY年MM月DD日 HH:MM | 窗口⑤ 收盘后

---

## 一、昨日/今日行情回顾
（整合 Step 1：8大指数 + 板块前10 + 涨跌比 + 美股三指数收盘）

## 二、📰 新闻简报
（原样使用 Step 2 输出）

## 三、📊 行情数据
（原样使用 Step 1：8行固定表格，MACD + 主力资金）

## 四、股债性价比（ERP）
（原样使用 Step 5 输出：PE/收盘/国债/ERP/估值水平/估值参考表）

## 五、触发因子总表
| 因子 | 状态 | 强度 | 方向 |
|:---|:---|:---|:---|
| 星期效应 | ... | 🟢🟡🔴 | ↕/↑/↓ |
| 季末 | ... | ... | ... |
| 财报季 | ... | ... | ... |

## 六、方向研判
**短期（1-3天）**：[看多/震荡/看空] — [理由，≤100字]
**中期（1-4周）**：[看多/震荡/看空] — [理由，≤100字]

## 七、操作建议
| 时段 | 策略 | 仓位建议 |
|:---|:---|:---|
| 明日早盘 | [建议] | [仓位%] |
| 明日午盘 | [建议] | [仓位%] |
| 本周剩余 | [建议] | [仓位%] |

## 八、💼 持仓诊断
（原样使用 Step 3 输出）

## 九、📋 日历检查
（原样使用 Step 0 输出）

---

## 📋 数据源确认
| 数据 | 来源（云端版） |
|:---|:---|
| A股指数行情 | stock-price-query-mx（腾讯财经） |
| 美股指数 | stock-price-query-mx |
| 技术指标 | china-stock-data（通达信 TDX） |
| 资金/板块 | WebSearch 智能提取 |
| 新闻 | WebSearch + eastmoney-mx |
| 诊股 | eastmoney-mx-skills-suite |
| K线/ATR | china-stock-data + tecent-finance |
| PE/国债/ERP | eastmoney-mx-skills-suite（6段估值） |
| 持仓/自选股 | IMA 知识库（云端直连） |
```

### 6.3 保存

写入 `/tmp/market_final.md`。

---

## Step 7: 上传 IMA 知识库

使用 IMA 知识库 API 将 `/tmp/market_final.md` 上传到「行情研判/研判报告/」文件夹。

### 回复确认（仅输出摘要）

```markdown
✅ 云端研判已生成 → 知识库「行情研判/研判报告/YYYY-MM-DD HHMM」
📊 上证 XXXX (+X.XX%) | 科创 XXXX (+X.XX%) | 涨跌比 X:X
💰 ERP X.XX%（🟡 中等偏低）| 沪深300 PE XX.XX | 国债 X.XX%
💼 持仓: X只诊断 | 🔍 自选: X只分析
☁️ 云端版 | 数据源: stock-price-query-mx + china-stock-data + eastmoney-mx
```

---

## 📝 与桌面版的主要差异

| 方面 | 桌面版 | 云端版 |
|---|---|---|
| 数据源 | MCP 连接器（westock/tdx/mx） | 技能市场技能（stock-price-query-mx 等） |
| 运行环境 | 需电脑开机 + WB 运行 | 手机 App 云端模式即可 |
| IMA 访问 | 通过 MCP | 云端直连 |
| 防呆验证 | Python 脚本（本地） | 内联逻辑（不依赖本地文件） |
| 发布方式 | 本地 ~/.workbuddy/skills/ | 上传 SkillHub + 云端安装 |
