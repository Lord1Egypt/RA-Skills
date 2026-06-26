# 中文回复模板

## 记录成功

已记录{meal_zh}：
{item_lines}

本餐合计：约 {kcal} kcal，蛋白质 {protein_g}g{optional_macros}
数据来源：{source_summary}
置信度：{confidence}
假设：{assumptions}

## 今日汇总

今日汇总：
- 热量：约 {kcal} kcal
- 蛋白质：{protein_g}g
- 碳水/脂肪：{carbs_g}g / {fat_g}g（如可用）
- 数据来源：用户提供 {user_provided_kcal} kcal，标签计算 {label_calculated_kcal} kcal，估算 {estimated_kcal} kcal
- 缺失字段：{missing_values_count} 个

提示：{gentle_advice}

## 本周总结

本周总结：
{daily_lines}

平均每天：约 {average_kcal} kcal，蛋白质 {average_protein_g}g
数据缺失日期：{missing_days}
提示：{gentle_advice}

## 修正完成

已修正：
- {food}：{change_summary}

更新后本餐合计：约 {kcal} kcal，蛋白质 {protein_g}g
说明：已保留原始消息，并在日志中记录修正说明。

## 撤销完成

已撤销上一条记录：
- {meal_zh} {time}：{food_summary}

今日合计已重新计算。

## 修正不明确

我无法唯一确定要修正哪一条。请回复对应序号：
{candidate_lines}

## 低置信度估算

这条记录里有低置信度估算：{reason}
我已记录原始描述；如果你知道重量、包装营养表或份数，可以继续补充，我会修正日志。
