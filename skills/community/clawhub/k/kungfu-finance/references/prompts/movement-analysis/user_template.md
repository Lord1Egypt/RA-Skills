你的任务是分析 <origin_input> 中的股票数据, 并结合提供的两张 K 线图（一张为近1.5年的中长期图表，一张为近半年的短期图表），提取与机会和风险相关的见解, 并提供专业的分析报告(以 JSON 格式输出). "Q&As" 代表"问题和答案". 

<TARGET DATE>
分析目标日期：{TODAY} 
</TARGET DATE>


您应该考虑的更多要求
<extra_requirments>
{EXTRA_REQUIREMENTS}
</extra_requirments>

到今天为止的**交易日** (非自然日)
{TRADING_DAYS}

以下是最近30个交易日的收盘价数据（日期降序），请以此为准进行价格点位分析：
<recent_prices>
{RECENT_PRICES}
</recent_prices>

## 按照前面定义的所有规则和规范, 输出分析结果 JSON 格式:

🚨 输出风格要求（至关重要）：
1. **专家与小白兼顾**：在使用专业术语（如金叉、背离、乖离率等）时，必须在括号内用**大白话解释**其含义和影响。
   - 错误示例：均线金叉，MACD底背离。
   - 正确示例：均线金叉（短期趋势转强，多头力量占优），MACD底背离（股价跌但动能减弱，可能见底）。
2. **结论先行**：每个分析段落的最后一句，必须是对当前局势的**客观总结**。（严禁操作建议）。
   - 示例：“...综上所述，目前处于主升浪，多头趋势稳健。”

🚨 输出前检查清单：
1. ✓ has_5_days_normal_movements 字段存在？
2. ✓ overall_analysis 列表存在且有3个要点？
3. ✓ risks 列表存在且有2-3个？
4. ✓ opportunities 列表存在且有2-3个？
5. ✓ all_unusual_movements 精确3个？
6. ✓ 任意两个异动日期间隔≥5天？
7. ✓ 最近5天内的异动已按重要程度对比处理？（新异动更重要才替换）

输出必须为 JSON，字段要求：
1. has_5_days_normal_movements: bool
2. overall_analysis: 3个对象（短期趋势/中期趋势/长期格局）
3. risks: 2-3个对象
4. opportunities: 2-3个对象
5. all_unusual_movements: 精确3个对象（trading_day/name/analysis/descriptions/value_judgement）

===

以下是用户输入:

<origin_input>
{ORIGIN_INPUT}
</origin_input>

以下是检测到的异常波动, 供您参考:
<detected_unusual_movements>
{UNUSUAL_MOVEMENTS}
</detected_unusual_movements>

请结合 K 线图进行形态识别。

以下是市场技术状态分析 (量能变化、趋势突破与关键筹码位置):
<market_technical_status>
{MARKET_TECHNICAL_STATUS}
</market_technical_status>

历史异动报告参考 (过去5个交易日的异动分析结果，用于智能去重和异动日期一致性管理)
<historical_reports>
{HISTORICAL_REPORTS}
</historical_reports>
