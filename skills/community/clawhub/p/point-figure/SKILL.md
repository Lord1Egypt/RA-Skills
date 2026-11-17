---
name: point-figure
description: |
  当用户要用点数图（P&F，X/O 列图）识别支撑阻挡、用"三点转向"生成简洁买卖信号，或用"横向数列法"
  测算价格目标，并需要理解"点数图无时间轴、按反转幅度记录"的制图逻辑时激活。
  不适用于：蜡烛/线图形态（转 ta-chart-basics）、画趋势线（转 trend-tools）。
  关键 trigger 词：点数图、P&F、X/O 列、三点转向、横向数列法、转行参数、整数格。

  Activate when the user wants to use point-and-figure charts (P&F, X/O columns) to identify support/resistance, generate clean buy/sell signals with "three-point reversal", or measure price targets via the "horizontal count method", and needs to understand that "P&F has no time axis and records by reversal magnitude".
  Not applicable: candle/line chart patterns (-> ta-chart-basics), drawing trendlines (-> trend-tools).
  Key trigger words: point-and-figure, P&F, X/O column, three-point reversal, horizontal count, reversal amount, box size.

source_book: 《期货市场技术分析》 约翰·墨菲
source_chapter: 第十一/十二章 日内点数图 / 三点转向和优化点数图
tags: [point-and-figure, pnf, three-point-reversal, column, count-method]
related_skills:
  - slug: ta-chart-basics
    relation: contrasts-with
  - slug: trend-tools
    relation: composes-with
---

# 点数图：无时间轴的支撑阻挡地图

## R — 原文 (Reading)

> "点数图只考虑价格变化，完全忽略时间因素；只有当价格反向变动达到规定幅度（如'三点转向'）才在图上添一格。"
> "只要发生任何简单的卖出信号，就必须平掉所有的多头头寸。"（三点转向纪律）
> "稳妥地设置止损指令，是成功交易最关键的要素之一。"
>
> — 约翰·墨菲，第十一/十二章 点数图

---

## I — 方法论骨架 (Interpretation)

点数图（P&F）是与线图/K 线逻辑不同的制图法，核心特征是**无时间轴**：

1. **只记价格、不记时间**：每一列 X（涨）或 O（跌）只记录价格变动，时间流逝不占空间，天然过滤小幅噪音。
2. **三点转向（3-box reversal）**：价格反向变动达到规定格数（如 3 格）才另起一列，否则在原列延续。转向格数即"反转幅度阈值"，是信号的灵敏度旋钮。
3. **转行参数因市场而异**（c15）：瑞士法郎可用 9 天为转行、棉花用 1 天，须依市场特性选择，才能清晰揭示支撑阻挡。
4. **横向数列法测目标**：数密集区横向 X/O 列数，乘以格值投影出涨跌目标——这是点数图独有的目标测算工具。
5. **信号简洁、纪律至上**（p43）：三点转向系统中任何简单卖出信号即平多，不犹豫、不摊平。
6. **止损第一**（p42）：无论何种图，稳妥设止损是生存第一道防线。

---

## A1 — 书中的应用 (Past Application)

### 案例 1：瑞士法郎 9 天 vs 棉花 1 天转行
- **问题**：不同市场如何用点数图？
- **方法论的使用**：瑞郎采用 9 天为转行的日内点数图，棉花采用 1 天转行，均清晰揭示潜在支撑与阻挡。
- **结论**：转行参数须匹配市场波动节律。
- **结果**：实例说明参数选择的实务考量（c15）。

---

## A2 — 触发场景 (Future Trigger) ★

### 用户会在什么情境下需要这个 skill?
1. 问"点数图怎么画、三点转向是什么意思"。
2. 问"用点数图怎么测算上涨/下跌目标"。
3. 问"该用几格转向、转行参数怎么选"。
4. 困惑"点数图出了卖出信号但我觉得只是调整，要不要平"。

### 语言信号
- "点数图、P&F、X/O 列、三点转向、横向数列法、转行参数、整数格"

### 与相邻 skill 的区分
- 与 `ta-chart-basics` 的区别：线图含时间轴、记录每根 K；点数图无时间轴、只按反转幅度记录。
- 与 `trend-tools` 的区别：点数图自成一格制图法，但揭示的支撑阻挡与趋势工具有互补关系。

---

## E — 可执行步骤 (Execution)

1. **选格值与转行参数**：依市场波动定每格代表的价格与转向格数（如 3 格），必要时按市场选转行周期。
   - 完成标准：确定格值、转向格数、转行参数。
2. **绘制 X/O 列**：只记价格反向达阈值才换列，构建无时间轴图。
   - 完成标准：图能显示关键支撑阻挡密集区。
3. **识别支撑阻挡**：从密集列区读出水平支撑/阻挡，比线图更纯净。
   - 完成标准：标出 2–3 个关键水平区。
4. **横向数列法测目标**：数密集区列数 × 格值，投影目标位。
   - 完成标准：给出测算目标价格。
5. **按信号纪律执行**：三点转向出简单卖出/买入信号即动作，并设止损。
   - 完成标准：信号出现即执行，不犹豫不摊平。

---

## B — 边界 (Boundary) ★

### 不要在以下情况使用此 skill
- 用户问 K 线/蜡烛图形态、OHLC 线图 → 转 ta-chart-basics。
- 用户问画趋势线、管道线 → 转 trend-tools。

### 作者在书中警告的失败模式
- **点数图是辅助制图法**：它揭示支撑阻挡与目标，但不替代趋势方向与时机判断，须与传统工具协同。
- **纪律违背**：出了简单信号却因"觉得只是调整"不平仓，破坏三点转向系统的简洁性（p43）。

### 作者的盲点 / 时代局限
- 1986 年靠手工绘点；现代软件可自动生成，但"无时间轴过滤噪音、横向数列测目标"的逻辑不变。

### 容易混淆的邻近方法论
- 点数图（无时间轴制图）vs 线图（含时间轴）：制图逻辑根本不同，勿把点数图信号当 K 线形态解读（见 ta-chart-basics B）。

---

## 相关 skills
- contrasts-with: ta-chart-basics
- composes-with: trend-tools

---

## 审计信息
- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 100% (6/6, Stage4 盲测)
- **蒸馏时间**: 2026-08-03
