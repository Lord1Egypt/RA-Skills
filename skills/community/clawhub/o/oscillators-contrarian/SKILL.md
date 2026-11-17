---
name: oscillators-contrarian
description: |
  当用户问摆动指数（RSI/KD/%R/MACD/ROC/动力指数）的超买超卖、背离，或相反意见理论（看涨一致数字、
  COT 持仓报告、看跌/看涨期权比）的情绪极端信号，并需要理解"趋势市 vs 横盘市用法相反"时激活。
  不适用于：趋势方向/均线交叉（转 moving-averages）、画趋势线（转 trend-tools）。
  关键 trigger 词：RSI 超买超卖、KD 金叉死叉、MACD 背离、%R、相反意见、看涨一致数字、市场情绪、COT。

  Activate when the user asks about oscillator (RSI/KD/%R/MACD/ROC/momentum) overbought/oversold and divergences, or contrary-opinion theory (bullish consensus, COT report, put/call ratio) sentiment extremes, and needs to understand that "usage in trending vs range-bound markets is opposite".
  Not applicable: trend direction / MA cross (-> moving-averages), drawing trendlines (-> trend-tools).
  Key trigger words: RSI overbought/oversold, KD cross, MACD divergence, %R, contrary opinion, bullish consensus, market sentiment, COT.

source_book: 《期货市场技术分析》 约翰·墨菲
source_chapter: 第十章 摆动指数和相反意见理论
tags: [oscillator, rsi, macd, stochastic, contrary-opinion, sentiment, divergence]
related_skills:
  - slug: dow-theory-framework
    relation: composes-with
  - slug: moving-averages
    relation: contrasts-with
---

# 摆动指数与相反意见：附属于趋势的辅助工具

## R — 原文 (Reading)

> "摆动指数分析附属于价格变化分析，绝不可僭越趋势的方向。"
> "RSI 超过 70 为超买状态，低于 30 为超卖状态。"
> "当绝大多数人看法一致时，他们一般是错误的一方。"（相反意见理论）
> "看涨意见一致数字超过 80% 为超买（顶），低于 30% 为超卖（底）。"
>
> — 约翰·墨菲，第十章 摆动指数和相反意见理论

---

## I — 方法论骨架 (Interpretation)

摆动指数（振荡量）是一类**有固定中间线、有超买/超卖阈值**的指标统称：动力指数、ROC、RSI、随机指数（%K、%D）、威廉斯 %R、MACD。相反意见理论则把"大众情绪极端"当作反向信号。核心要点：

1. **必须附属于趋势**（p36 / ce23）：摆动指数告诉你"超买超卖"，但方向由价格趋势决定。逆主趋势抄底摸顶是最大误用陷阱。
2. **趋势市与横盘市用法相反**（核心反直觉）：横盘市中"超卖买、超买卖"有效；趋势市中超买可更强、超卖可更深，**背离才有意义**。
3. **RSI 70/30 阈值**（p38）：进入极端区仅是警告，非动作指令。
4. **不因接近极限放弃有利头寸**（p39 / ce25）：强势趋势中指标可长期钝化在极端区，仅因 RSI 超买就平仓会过早丢掉主升浪。
5. **背离不可奉若神灵**（ce24）：背离是警示而非确证，强趋势中可多次失效，绝不可抛弃趋势分析。
6. **相反意见：极端一致才有效**（p40/p41/ce26）：80% 以上看涨=潜在顶部（无人剩余推升），30% 以下看跌=潜在底部；仅在极端下反向，是确认工具非独立信号。
7. **应用相反意见须兼顾持仓结构**（ce27）：须看 COT 持仓报告，不可与商业保值大户立场冲突（散户悲观但商业大量做多时，反向做空必败）。

---

## A1 — 书中的应用 (Past Application)

### 案例 1：看涨意见一致数字 80%/30% 极端阈值
- **问题**：如何把"大众情绪"量化成可操作的反向信号？
- **方法论的使用**：作者给出看涨一致数字的阈值——>80% 看顶、<30% 看底，作为相反意见理论的落地指标。
- **结论**：情绪极端是反转的预警工具。
- **结果**：成为情绪类相反指标的经典操作阈值（c14）。

### 案例 2：豆粕 COT 报告顶部预警（1985）
- **问题**：如何用持仓结构判顶？
- **方法论的使用**：1985-01-18 豆粕 COT 显示商业套保者庞大净空、投机大众庞大净多——相反意见式的顶部先兆。
- **结论**：商业 vs 投机的持仓错位是顶部信号，事后豆粕下跌验证。
- **结果**：印证"兼顾持仓兴趣"的相反意见用法（c05）。

---

## A2 — 触发场景 (Future Trigger) ★

### 用户会在什么情境下需要这个 skill?
1. 问"RSI/KD 到多少算超买超卖、背离怎么看"。
2. 问"MACD 顶背离是不是要反转了"。
3. 问"市场情绪是不是太一致了、是不是要见顶/见底"。
4. 困惑"为什么趋势很强但 RSI 一直超买、不敢持有"。

### 语言信号
- "RSI 超买超卖、KD 金叉死叉、MACD 背离、%R"
- "相反意见、看涨一致数字、市场情绪、COT、看跌看涨比"

### 与相邻 skill 的区分
- 与 `moving-averages` 的区别：均线是趋势跟踪（顺大势），摆动指数是动量/超买超卖（附属于趋势）。
- 与 `dow-theory-framework` 的区别：dow 定趋势方向，本 skill 在其框架下做次级确认与极值提示。

---

## E — 可执行步骤 (Execution)

1. **先定趋势方向**：用趋势线/均线/道氏判当前主趋势；摆动的用法取决于此。
   - 完成标准：明确趋势市还是横盘市。
2. **读摆动极值**：趋势市看背离、横盘市看超买卖；用 RSI 70/30 等作参考。
   - 完成标准：定位是否极端、有无背离。
3. **用背离做反转预警**（仅趋势末端）：价格创新高而指标未创新高，配合其它信号。
   - 完成标准：背离出现 + 至少一项传统反转信号确认，才动作。
4. **查情绪极端（相反意见）**：看涨一致数字 >80% / <30%，或 COT 持仓极端错位。
   - 完成标准：仅极端区反向；同时核对商业持仓方向，不与大户冲突。
5. **不逆主趋势**：趋势初期忽略超买，强趋势中钝化可接受，保护有利头寸。
   - 完成标准：动作方向与主趋势不冲突，或仅在确凿反转信号下反向。

---

## B — 边界 (Boundary) ★

### 不要在以下情况使用此 skill
- 用户问均线金叉死叉、移动平均线 → 转 moving-averages。
- 用户问画趋势线、管道线 → 转 trend-tools。

### 作者在书中警告的失败模式
- **必须附属趋势**（ce23）：仅凭超买超卖逆势操作，强趋势中会被碾。
- **背离不可奉若神灵**（ce24）：背离常出现但不总预示反转，不能扔掉趋势分析。
- **趋势初期别太介意摆动**（ce25）：新趋势刚启动 RSI 速超买并维持，过早离场踏空主升段。
- **极端一致才反向**（ce26）：非极端时随大流无碍，只有 80/90% 极端才反向。
- **须兼顾持仓结构**（ce27）：机械反向散户情绪却与商业保值大户对赌，必败。

### 作者的盲点 / 时代局限
- 1986 年无现代情绪数据（如散户持仓、搜索引擎情绪）；但"极端拥挤=拐点"原则仍核心。

### 容易混淆的邻近方法论
- 摆动指数（动量/极值）vs 均线（趋势）：强趋势中摆动指数可长期超买，勿用摆动逆均线（见 moving-averages B）。

---

## 相关 skills
- composes-with: dow-theory-framework
- contrasts-with: moving-averages

---

## 审计信息
- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 100% (6/6, Stage4 盲测)
- **蒸馏时间**: 2026-08-03
