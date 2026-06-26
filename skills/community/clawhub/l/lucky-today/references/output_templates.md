# Output Templates — 输出模板集合

按模式选择对应模板。所有模板都"逐字严格输出"(emoji / 标题 / 分隔线必须一致),只有 `<>` 包裹的内容才能替换。

模板顺序:

1. 单日 today / 次日 tomorrow(CN + EN)
2. 本周 weekly(CN + EN)
3. 本月 monthly(CN + EN)
4. 双人合盘 couple(CN + EN)
5. 场景运势 scenario(CN + EN)
6. 推送精简版(CN + EN)

---

## 1) 单日 / 次日 模板

### CN(默认)

```
【今日运势 | YYYY-MM-DD】

✨ 总览评级:<大吉 / 中吉 / 平 / 小凶> (<0-100>/100)

<1-2 句解释,必须引用 R 值层或日期规则。例如:"R=587,午时阳气足,叠加周三沟通日,整体偏顺。">

🧭 幸运方位:<方位>
🎨 幸运颜色:主色 <颜色>,辅色 <颜色>
🔢 幸运数字:<n1>, <n2>[, <n3>]
📿 幸运物品:<物品>

✅ 今日宜做
1. <动作>(可含时段)
2. <动作>
3. <动作>

❌ 今日忌做
1. <规避>
2. <规避>
3. <规避>

⚠️ 强禁忌预警
- 禁忌事项:<事项>
- 禁忌时间:即刻起至 YYYY-MM-DD HH:mm
- 原因:<规则推导>
- 替代方案:<可执行替代>

🌟 专项运势
• 财运:<结论>。<进财时段>。<风险点>
• 桃花:<结论>。<利好时段>。<避雷>
• 事业/学业:<结论>。<建议>
• 人际:<结论>。<沟通要点>

🔮 详细拆解
• 命格基调:<偏稳 / 偏动 + 原因>
• 日期气场:<偏沟通 / 偏执行 / 偏收敛 + W 值>
• 叠加结论:<为什么这个评分,为什么这些元素>

💡 24 小时行动建议
• 早间(07:00-09:00):<1 条>
• 午间(12:00-14:00):<1 条>
• 晚间(20:00-22:00):<1 条>

───
以上为民俗文化与娱乐参考,请结合现实理性判断。
```

### EN

```
【Daily Fortune | YYYY-MM-DD】

✨ Overall: <Great / Good / Neutral / Caution> (<0-100>/100)

<1-2 sentence explanation citing R value or date rule.>

🧭 Lucky direction: <direction>
🎨 Lucky colors: primary <color>, accent <color>
🔢 Lucky numbers: <n1>, <n2>[, <n3>]
📿 Lucky item: <item>

✅ Do today
1. <action> (optional time slot)
2. <action>
3. <action>

❌ Avoid today
1. <avoid>
2. <avoid>
3. <avoid>

⚠️ Strong warning
- Avoid: <thing>
- Window: from now until YYYY-MM-DD HH:mm
- Reason: <rule derivation>
- Alternative: <executable alternative>

🌟 By topic
• Wealth: <conclusion>. <best window>. <risk>
• Love: <conclusion>. <best social window>. <avoid>
• Career / Study: <conclusion>. <suggestion>
• Social: <conclusion>. <communication tip>

🔮 Breakdown
• Birth tone: <stable / mobile + reason>
• Day energy: <communicative / executive / inward + W>
• Combined: <why this score, why these elements>

💡 24-hour plan
• Morning (07:00-09:00): <1 line>
• Midday (12:00-14:00): <1 line>
• Evening (20:00-22:00): <1 line>

───
For folklore and entertainment reference only — combine with judgment.
```

次日模板与单日完全相同,只把标题改成 `【明日运势 | YYYY-MM-DD】` / `【Tomorrow's Fortune | YYYY-MM-DD】`,内容使用次日的 D 计算。

---

## 2) 本周 weekly 模板

### CN

```
【本周运势 | YYYY-MM-DD ~ YYYY-MM-DD】

✨ 整周评级:<等级> (avg <平均分>)

<1-2 句概述本周整体气场>

📈 峰值日:YYYY-MM-DD <星期> · <大吉/中吉> <分数>
   建议:<一句话用途建议,如"重要会议 / 表白 / 投递简历">

📉 低谷日:YYYY-MM-DD <星期> · <平/小凶> <分数>
   建议:<一句话避雷建议,如"避免重大决策,以休整为主">

🗓️ 每日速览
• 周一 YYYY-MM-DD:<等级> <分数> · 方位<…> · 主色<…>
• 周二 YYYY-MM-DD:<等级> <分数> · 方位<…> · 主色<…>
• 周三 YYYY-MM-DD:<等级> <分数> · 方位<…> · 主色<…>
• 周四 YYYY-MM-DD:<等级> <分数> · 方位<…> · 主色<…>
• 周五 YYYY-MM-DD:<等级> <分数> · 方位<…> · 主色<…>
• 周六 YYYY-MM-DD:<等级> <分数> · 方位<…> · 主色<…>
• 周日 YYYY-MM-DD:<等级> <分数> · 方位<…> · 主色<…>

✅ 本周宜做
1. <周级动作>(关联峰值日)
2. <周级动作>
3. <周级动作>

❌ 本周忌做
1. <周级规避>(关联低谷日)
2. <周级规避>
3. <周级规避>

⚠️ 本周强禁忌(若整周累计 risk ≥ 80 触发)
- 禁忌事项 / 时间窗 / 原因 / 替代方案

💡 本周策略
• 把重要的事尽量安排在<峰值日>之前推进
• 低谷日给自己留一个"什么都不决定"的窗口
• 一条最关键的执行建议

───
以上为民俗文化与娱乐参考。
```

### EN

```
【Weekly Fortune | YYYY-MM-DD ~ YYYY-MM-DD】

✨ Week rating: <Great / Good / Neutral / Caution> (avg <score>)

<1-2 sentence overview of the week's overall energy.>

📈 Peak day: YYYY-MM-DD <weekday> · <rating> <score>
   Use it for: <suggestion>

📉 Trough day: YYYY-MM-DD <weekday> · <rating> <score>
   Caution: <avoid suggestion>

🗓️ Daily snapshot
• Mon YYYY-MM-DD: <rating> <score> · dir <…> · color <…>
• Tue YYYY-MM-DD: <rating> <score> · dir <…> · color <…>
• Wed YYYY-MM-DD: ...
• Thu YYYY-MM-DD: ...
• Fri YYYY-MM-DD: ...
• Sat YYYY-MM-DD: ...
• Sun YYYY-MM-DD: ...

✅ Do this week
1. <week-level action>
2. <week-level action>
3. <week-level action>

❌ Avoid this week
1. <week-level avoid>
2. <week-level avoid>
3. <week-level avoid>

⚠️ Strong warning (if cumulative risk ≥ 80)
- Avoid / Window / Reason / Alternative

💡 Weekly strategy
• Schedule the important things before <peak day>.
• Reserve a "no decisions" window on the trough day.
• One key executable suggestion.

───
For folklore reference only.
```

---

## 3) 本月 monthly 模板

### CN

```
【本月运势 | YYYY 年 MM 月】

✨ 月度主题:<6 个主题之一>

<2-3 句概述本月气场基调>

📈 焦点日(优先安排重要事):
• YYYY-MM-DD · <大吉> <分数> · 适合<事项类型>
• YYYY-MM-DD · <大吉/中吉> <分数> · 适合<…>
• YYYY-MM-DD · <中吉> <分数> · 适合<…>
[7-8 个]

📉 避坑日(避免重大决定):
• YYYY-MM-DD · <小凶/平> <分数>
• YYYY-MM-DD · <小凶/平> <分数>
• YYYY-MM-DD · <小凶/平> <分数>
[3 个]

🌟 月度专项运势
• 财运:<月度结论 + 1 个推进建议 + 1 个守住建议>
• 桃花:<月度结论 + 1 个开放建议 + 1 个避坑>
• 事业 / 学业:<月度结论 + 关键节点建议>
• 人际:<月度结论 + 沟通主题>

⚠️ 月度强禁忌(若月内有 ≥3 天 risk ≥ 70)
- 禁忌事项 / 集中时间窗 / 原因 / 替代方案

💡 月度建议
1. <策略 1 — 长程动作>
2. <策略 2 — 关系或健康节奏>
3. <策略 3 — 财务或职业方向>

───
以上为民俗文化与娱乐参考。
```

### EN

```
【Monthly Fortune | YYYY-MM】

✨ Monthly theme: <one of 6 themes>

<2-3 sentence overview.>

📈 Focus days (prioritize important things):
• YYYY-MM-DD · <Great> <score> · best for <activity type>
• YYYY-MM-DD · <Great/Good> <score> · best for <…>
[7-8 entries]

📉 Caution days (avoid big decisions):
• YYYY-MM-DD · <Caution/Neutral> <score>
[3 entries]

🌟 Monthly by topic
• Wealth: <conclusion + push tip + hold tip>
• Love: <conclusion + open tip + caution>
• Career / Study: <conclusion + key node tip>
• Social: <conclusion + communication theme>

⚠️ Monthly warning (if ≥3 days with risk ≥ 70)
- Avoid / Concentrated window / Reason / Alternative

💡 Monthly strategy
1. <long-horizon action>
2. <relationship or health rhythm>
3. <financial or career direction>

───
For folklore reference only.
```

---

## 4) 双人合盘 couple 模板

见 `couple_rules.md` §3,这里不重复。

---

## 5) 场景运势 scenario 模板

见 `scenario_rules.md` §6,这里不重复。

---

## 6) 推送精简版(单条消息渠道限制)

### CN

```
【明日运势 | YYYY-MM-DD】

✨ <评级> · 方位 <…> · 主色 <…> · 数字 <n1, n2>

✅ 宜:<3 条紧凑列表,用「、」分隔>
❌ 忌:<3 条紧凑列表>

⚠️ 关键提醒:<1 条强禁忌简版,包含时间窗截止>
```

### EN

```
【Tomorrow | YYYY-MM-DD】

✨ <Rating> · dir <…> · color <…> · nums <n1, n2>

✅ Do: <3 items, comma-separated>
❌ Avoid: <3 items, comma-separated>

⚠️ Key warning: <1-line strong warning with window end>
```

推送时若仍超字数:再压缩"宜"和"忌"到 2 条;若仍超,拆为 2-3 条消息按顺序发。

---

## 输出规则总结

1. **不附加** sessionId / system 日志 / 模型名 / 内部 R 值数字(除非"详细拆解"段引用)
2. **永远** 输出末尾的免责声明分隔线
3. **永远** 用统一 emoji 集合(`✨🧭🎨🔢📿✅❌⚠️🌟🔮💡📈📉🗓️💞🌬️💬`),不要替换为其他 emoji
4. **同一模式同一输入下** 评级和四元素必须稳定
5. **跨模式组合**(如"明日面试运")时:用次日 D + 场景偏置 + 场景模板
