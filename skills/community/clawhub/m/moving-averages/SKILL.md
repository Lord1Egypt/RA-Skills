---
name: moving-averages
description: |
  当用户要用移动平均线（MA）判断趋势、选择均线类型/周期/组合，或理解四周规则（唐奇安突破）、
  4-9-18 天组合，并清楚其"滞后性"与"横盘失效"局限时激活。
  不适用于：超买超卖摆动指数（转 oscillators-contrarian）、画趋势线（转 trend-tools）。
  关键 trigger 词：均线金叉死叉、移动平均线、四周规则、双均线、EMA、均线滞后、4-9-18。

  Activate when the user wants to use moving averages (MA) to judge trend, choose MA type/period/combination, or understand the four-week rule (Donchian breakout), the 4-9-18 day combo, and its limitations of "lag" and "failure in range-bound markets".
  Not applicable: overbought/oversold oscillators (-> oscillators-contrarian), drawing trendlines (-> trend-tools).
  Key trigger words: MA golden/death cross, moving average, four-week rule, dual MA, EMA, MA lag, 4-9-18.

source_book: 《期货市场技术分析》 约翰·墨菲
source_chapter: 第九章 移动平均线
tags: [moving-average, crossover, four-week-rule, trend-following, lag]
related_skills:
  - slug: dow-theory-framework
    relation: composes-with
  - slug: oscillators-contrarian
    relation: contrasts-with
---

# 移动平均线：趋势跟踪工具

## R — 原文 (Reading)

> "移动平均线是一种追踪趋势的滞后指标，它天生具有平滑作用和滞后特性。"
> "双移动平均线组合（一快一慢）在各类系统中表现最佳。"
> "当价格涨出前 4 周的新高位时买入，跌出前 4 周的新低位时卖出。"（四周规则）
>
> — 约翰·墨菲，第九章 移动平均线

---

## I — 方法论骨架 (Interpretation)

均线是"顺应趋势"的量化版，但有其固有特性：

1. **滞后性不可消除**（ce19）：均值是过去价格的平均，天生慢半拍；别把它当领先信号。
2. **简单均线常更可靠**（美林研究）：对多数市场，朴素简单均线胜过加权/EMA；不要过度追逐复杂变体。
3. **双均线组合最优**：快+慢交叉平衡灵敏与可靠；单均线噪音多，三均线太滞后。
4. **周期选择**：较长期胜较短（分水岭约 40 天）；期货常用短组合（4/9/18 天分别看短/中/长趋势）。
5. **四周规则（唐奇安）**：突破前 4 周高低点做方向，是最成功的趋势跟踪系统之一，但**连续在市**在横盘会拉锯（ce22）。
6. **场景局限**：均线法在横向市占 1/3~1/2 时间表现糟（ce21），短期均线更易出伪信号（ce20）。

**用法**：金叉/死叉、价格穿均线、均线多排/空排判断趋势；用 ADXR 等过滤器先判有无趋势再上均线系统。

---

## A1 — 书中的应用 (Past Application)

### 案例 1：美林 1978–1982 均线研究
- **问题**：均线系统是否真能跑赢买入持有？
- **方法论的使用**：美林实证显示优化参数组合持续跑赢买入持有。
- **结论**：均线作为趋势跟踪工具有机构级证据。
- **结果**：验证均线系统有效性。

### 案例 2：4-9-18 天组合（艾伦 1972）
- **问题**：怎么同时看短/中/长趋势？
- **方法论的使用**：4/9/18 天三条均线分别刻画短/中/长期，依相对位置与交叉判时机。
- **结论**：多周期均线组合是经典实务方案。
- **结果**：成为书中推荐组合。

### 案例 3：四周规则 1970 测试最成功
- **问题**：最简单的趋势系统哪种好？
- **方法论的使用**：邓恩和哈吉特 1970 测试，四周规则表现最佳。
- **结论**：简单通道突破在趋势市极有效。
- **结果**：经典趋势跟踪系统。

---

## A2 — 触发场景 (Future Trigger) ★

### 用户会在什么情境下需要这个 skill?
1. 问"均线金叉/死叉怎么看、该用什么周期"。
2. 问"EMA 和简单均线哪个好"。
3. 问"四周规则/唐奇安突破怎么用"。
4. 困惑"为什么均线信号总是慢、横盘总亏"。

### 语言信号
- "均线金叉死叉、移动平均线"
- "EMA、简单均线、双均线"
- "四周规则、唐奇安"
- "均线滞后、横盘亏钱"

### 与相邻 skill 的区分
- 与 `oscillators-contrarian` 的区别：均线是趋势跟踪（顺大势），摆动指数是动量/超买超卖（附属于趋势）。
- 与 `dow-theory-framework` 的区别：dow 是框架，均线是量化落地工具。

---

## E — 可执行步骤 (Execution)

1. **选类型与周期**：默认简单均线；期货用短组合（如 4/9/18），长线偏长（>40 天）。
   - 完成标准：确定均线类型与 1–2 条周期。
2. **判趋势**：用双均线交叉/价格穿线/均线排列定方向。
   - 完成标准：明确多空。判停：若 ADXR 低（<20）无趋势，降级或不用。
3. **用四周规则等突破**：趋势市用通道突破（前 N 周期高低）触发。
   - 完成标准：定义突破阈值。
4. **接受滞后与横盘磨损**：不期待均线"预测"，横盘期控制暴露。
   - 完成标准：认知滞后代价，配过滤器/退出机制。

---

## B — 边界 (Boundary) ★

### 不要在以下情况使用此 skill
- 用户问 RSI/K%/背离超买超卖 → 转 oscillators-contrarian。
- 用户问画趋势线 → 转 trend-tools。

### 作者在书中警告的失败模式
- **本质滞后**（ce19）：别用均线拐点当领先信号。
- **横盘表现糟**（ce21）：1/3~1/2 时间无效，须先判有无趋势。
- **短期均线伪信号**（ce20）：震荡市频繁交叉，反复止损。
- **四周规则连续在市拉锯**（ce22）：无趋势期须有横向退出机制。

### 作者的盲点 / 时代局限
- 1986 年无现代机器学习择时；但"先判趋势状态再选系统"的原则仍核心。

### 容易混淆的邻近方法论
- 均线（趋势）vs 摆动指数（动量）：强趋势中摆动指数可长期超买，勿用摆动逆均线（见 oscillators-contrarian B）。

---

## 相关 skills
- composes-with: dow-theory-framework
- contrasts-with: oscillators-contrarian

---

## 审计信息
- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 100% (6/6, Stage4 盲测)
- **蒸馏时间**: 2026-08-03
