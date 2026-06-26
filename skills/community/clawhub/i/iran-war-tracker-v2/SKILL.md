---
name: iran-war-tracker
description: |-
  为2026年3月爆发的伊朗战争提供每日结构化局势日报与实时风险监测。整合金十数据MCP（实时快讯+行情）、WebSearch/Jina网页抓取、Tavily深度搜索等多源数据，生成面向地缘可信度分级报告。

  **核心能力：**
  - **多源数据采集**：金十MCP实时快讯（关键词搜索，默认当天全量）、金十MCP行情（布伦特原油/黄金/天然气/USD-CNH，BTC/纳指/美债由AlphaVantage/Stooq补充）、WebSearch新闻检索、Jina网页预处理
  - **时效性控制**：快讯默认过滤当天当前小时数（如9点执行则覆盖0-9时），新闻默认过去18小时

  English: Structured daily Iran war situation briefs integrating Jin10 MCP real-time flashes & quotes, WebSearch, and Tavily deep search. Applies a rigorous ceasefire-period analytical framework with credibility-graded output (multi-source confirmed / single-source / unverified / denied), covering Hormuz Strait transit, actor pressure variables, scenario probability forecasts (A/B/C), and risk asset implications for geopolitical trading decisions.
version: 1.2.0
clawhub: https://clawhub.ai/chinfi-codex/iran-war-tracker
triggers: /irantracker 伊朗动态
---

## 行动基准哲学
* 分析框架是展开一切行动的基准：必须先加载本地文件 `【FRAME】停火期.md`。
* 基于分析框架，要做到绝对的冷静、客观，不会做任何主观预设，绝对不将自己置于信息茧房的可能性中。
* 将世界事件的走向认为是在多重变量变化叠加下所产生的概率论分支。所以要识别当前事件的核心变量，思考其对应权重。然后和高可信度信源信息叠加分析，推演事件的走向，和其对现实世界施加的影响性。

---

## 信息数据收集
确保完成以下所有信息收集工作

### 搜索新闻
##### 第一步，构建搜索词
根据加载的分析框架，分析变量和权重，推导出最重要的3-5个研究方向，每个方向构建搜索关键词组。举例如下：
 * 战争局势更新 / war situation updates
 * 霍尔木兹海峡关闭、通航、油轮及袭船事件 / Hormuz Strait closure, transit, tanker, ship attacks
 * 石油供应、出口、制裁及产量变化 / oil supply, exports, sanctions, production
 * 天然气供应、LNG、基础设施及出口变化 / natural gas supply, LNG, infrastructure, exports
 * 领导人、外交官及军方表态 / leader, diplomat, military statements

##### 第二步，使用搜索工具搜索全部关键词组
* 优先使用当前环境下可用的 Tool：WebSearch/Kimi_search，**WebFetch**
  * **Jina**（可选预处理层，可与 WebFetch/curl 组合使用，由于其特性可节省 tokens 消耗，请积极在任务合适时组合使用）：第三方网络服务，可将网页转为 Markdown，大幅节省 token 但可能有信息损耗。调用方式为 `r.jina.ai/example.com`（URL 前加前缀，不保留原网址 http 前缀），限 20 RPM。
* 可选使用 Tavily 搜索，需要配置 API KEY

### 快讯（金十数据 MCP）
使用脚本 `scripts/jin10_flash.py` 通过金十 MCP 协议获取实时快讯：

```bash
python scripts/jin10_flash.py --keyword 伊朗
```

参数说明：
* `--keyword`：搜索关键词，默认 `伊朗`
* `--hours`：时效过滤，默认取**当天当前小时数**（如 9 点执行则默认 9 小时，覆盖当天全部快讯），传入 `0` 表示不限
* `--limit`：最大返回条数，默认**不限制**
* `--format`：输出格式，可选 `raw` / `normalized` / `markdown`

此脚本已替代原有的 `telegraph.py`（财联社+金十混合抓取方案），数据源更稳定、标准化程度更高。

### 风险资产数据
使用脚本 `scripts/macro_monitor.py` 获取以下资产数据：

**金十 MCP 核心品种（优先来源）：**
- 布伦特原油（UKOIL）
- 现货黄金（XAUUSD）
- 天然气（NGAS）
- 美元/离岸人民币（USDCNH）

**补充来源（AlphaVantage / Stooq）：**
- BTC
- 纳指期货
- 美国 10 年期国债

```bash
python scripts/macro_monitor.py
```

`macro_monitor.py` 的数据获取策略：
1. **优先使用金十 MCP** 获取 Brent / Gold / Natural Gas / USD-CNH
2. 金十失败时回退到 AlphaVantage
3. AlphaVantage 限流或缺失时回退到 Stooq
4. BTC、美债、纳指期货由 AlphaVantage / Stooq 覆盖

---

## 分析输出

### 分析要求
遵守以下规则（非风格建议，而是硬性要求）：
* 根据信源等级确定可信度
  * 最高：官网、国家级官媒，官方平台，官方领导人社交平台发言
  * 次要：社交大V，传言的重要人物讲话
* 【重要】对新闻、电报数据，筛选时效性，默认为过去 18 小时
* 报告默认必须使用中文产出。每个部分都应内容充实，而非一句话总结。
* 不能仅停留在事件总结。每个部分都需要证据加解读。
* 必须区分：
  * 确认的事实
  * 市场定价信号
  * 推断或情景判断
* 能源与经济影响的传导路径：
  * 必须分开分析石油和天然气，不能合并成笼统的"能源"段落。
  * 必须严格按照加载的分析框架 `【FRAME】停火期.md` 所指引的传导路径对要素进行分析
* 补充其他从分析框架中得出的重要路径和变量信号

### 输出报告
* 【重要】在报告中输出新闻内容，以 `时间-新闻[来源]` 的格式呈现
* 报告中不同的模块内容，使用适当的分割线，恰当不要喧宾夺主，同时要考虑手机屏幕宽度
* 报告总字数控制在 3000 字以内。

### 报告模板
加载本地文件 `【TEMPLATE】.md` 作为输出格式基准，严格按照模板结构填充内容。

模板核心结构：
```
# 🔥 美以伊动态播报 | YYYY-MM-DD
更新时间：XX:XX
**停火第N天 / 剩余X天 / 当前阶段：XX**

## 📈 形势速览
### **一句话判断：**[...]
##### 战争烈度级别：X级（🔺/🔻/➡️）
**核心事实变化**
🔴 违约/升级信号
🟢 合规/缓和信号
⚪ 谈判动态
##### 未来24-48小时关键观察节点

## ⚔️ 各方行动
### 调解进展
### 🇺🇸 美国
### 🇮🇱 以色列
##### 以色列独立意志监测 🔑
### 🇮🇷 伊朗
### 🔴 代理人网络
### 世界行动

## 🛢 航运

## 🔮 到期推演
- 情景A：...（XX%）
- 情景B：...（XX%）
- 情景C：...（XX%）

**今日结论：** [...]
```

日报必须包含的字段（来自 `【FRAME】停火期.md`）：
1. **停火倒计时**：停火第 N 天 / 剩余 X 天 / 当前阶段
2. **战争烈度级别**：1-10 级，含趋势箭头
3. **核心事实变化**：分 🔴 违约/升级、🟢 合规/缓和、⚪ 谈判动态 三类
4. **以色列独立意志监测**：必含模块
5. **到期推演**：情景 A/B/C 概率（每日滚动更新）
6. **今日结论**：一句话总结
