---
name: lucky-today
description: 离线每日运势 — 输出幸运方位/颜色/数字/物品/宜忌,支持今日/明日/本周/本月、双人合盘、面试/考试/相亲/上线/出差等场景化运势,中英双语,可定时推送 Telegram/Feishu。Daily luck oracle with bilingual output, multi-horizon (today/weekly/monthly), couple readings, and scenario-specific fortunes. No external API.
keywords: 今日运势, 幸运颜色, 幸运方位, 幸运数字, 今日财运, 桃花运, 面试运势, 考试运势, 相亲运势, 合盘, 本周运势, 本月运势, 每日运势推送, 运势, daily horoscope, lucky color, lucky number, lucky direction, daily fortune, interview luck, exam luck, weekly horoscope, monthly horoscope, couple compatibility, 운세, 運勢, tử vi
version: 0.1.0
---

# Lucky Today (今日运势)

> 离线确定性每日运势 · 幸运色/方位/数字/物品 · 周/月/双人/场景化模式 · 中英双语 · 可推送 Telegram/Feishu
> Offline deterministic daily fortune oracle — lucky color / direction / number / item · today / weekly / monthly · couple · scenarios · bilingual CN/EN.

## 何时使用 / When to invoke this skill

Pick this skill when the user asks any of:

- **中文(高频):** 今天运势、今天幸运色、今天幸运方位、今天幸运数字、今天财运、今天桃花、今日宜忌、明天运势、这周运势、本月运势
- **中文(场景):** 面试运、考试运、相亲运、项目上线运、出差运、签约运、谈判运
- **中文(双人):** 我和xx今天合不合、双人合盘、今天约会运、夫妻今日运势
- **English:** "my horoscope", "horoscope now", "lucky color today", "lucky direction", "what's my fortune today", "interview luck", "exam luck", "this week's horoscope", "monthly horoscope", "couple compatibility today"
- **日本語:** 今日の運勢、ラッキーカラー
- **한국어:** 오늘 운세, 행운의 색
- **Tiếng Việt:** vận may hôm nay, tử vi hôm nay

### Negative scope (defer to other skills)

- 完整八字排盘 / Four Pillars chart / ZiWei DouShu / 紫微斗数 / QiMen DunJia / 奇门遁甲 → 用 **[yunshi](https://clawhub.ai/skills/yunshi)** (professional calculation toolkit)
- 西方星座运势 / Western zodiac horoscope (Aries / Taurus / ...) → 用 **[daily-astro](https://clawhub.ai/skills/daily-astro)**
- 塔罗占卜 / Tarot reading → 用其他塔罗 skill

本 skill 只负责"今天/这周/这个月 + 我/我俩 + 一般或场景"这个区间。

## 模式 / Modes

| Mode | Trigger phrases | Output |
|---|---|---|
| **单日 today** *(default)* | "今天运势", "lucky today" | 总览评级 + 幸运四元素 + 宜/忌 + 强禁忌预警 + 专项运势 |
| **次日 tomorrow** | "明天运势", "tomorrow fortune" | 同 today,日期 +1 |
| **本周 weekly** | "这周运势", "this week", "weekly horoscope" | 7 日评级序列 + 峰值日 + 低谷日 + 周建议 |
| **本月 monthly** | "本月运势", "monthly horoscope" | 月度走势 + 3-4 个焦点日期 + 月建议 |
| **双人合盘 couple** | "我和xx今天合不合", "couple today" | 见 `references/couple_rules.md`(相处氛围 + 共同宜忌 + 沟通建议) |
| **场景运势 scenario** | "面试运" / "考试运" / "相亲运" / "上线运" / "出差运" | 见 `references/scenario_rules.md`(场景偏置 + 时间窗 + 替代方案) |

模式组合允许:`明天面试运`、`这周双人合盘` 等。

## 读取顺序(强制 / Required read order)

在产出任何运势前,必须按顺序读以下文件(用 `read` 工具,不要用 `find` / `ls` / shell 查找):

1. **必读:** `{baseDir}/references/fortune_rules.md` — 基础确定性规则
2. **必读:** `{baseDir}/references/output_templates.md` — 输出模板
3. **场景模式时必读:** `{baseDir}/references/scenario_rules.md`
4. **双人模式时必读:** `{baseDir}/references/couple_rules.md`
5. **可选:** `{baseDir}/user_profile.json` — 用户档案(若不存在则可选建档,见下文)
6. **建档时参考:** `{baseDir}/references/user_profile_template.md`

读取失败:直接提示 "无法读取 [文件名],请检查技能安装是否完整"。**禁止**降级到联网检索或猜测。

## 输入约定

- **生日**:`YYYY-MM-DD`,或 `YYYY年MM月DD日`。可缺(降低解释细度)。
- **查询日期**:默认"今天";夜间推送场景默认"明天"。可显式指定。
- **查询类型**:`overall|wealth|love|career|study|health|social|interview|exam|dating|launch|business-trip|couple-today`。
- **第二人信息(双人模式)**:对方姓名 + 生日。

## CN 输出模板(默认 / default)

严格按以下模板输出(标题、emoji、换行、编号必须一致;允许的可变字段才能改):

```
【<模式标签>运势 | YYYY-MM-DD】

✨ 总览评级:大吉 / 中吉 / 平 / 小凶 (0-100 分)

用 1-2 句解释为什么是这个评分,必须引用规则(R 值层 / 日期规则 / 星盘宫位)。

🧭 幸运方位:<方位>
🎨 幸运颜色:主色 <颜色>,辅色 <颜色>
🔢 幸运数字:<n1>, <n2>[, <n3>]
📿 幸运物品:<物品>

✅ 今日宜做
1. <动作>(可含时段,如 09:00-11:00;必须可执行)
2. <动作>
3. <动作>

❌ 今日忌做
1. <规避>(可含时段)
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
• 命格基调:<生日 B 的奇偶 + 数位和>
• 日期气场:<日期 D 与星期 W>
• 叠加结论:<为什么这个评分,为什么这些幸运元素>

💡 24 小时行动建议
• 早间(07:00-09:00):<1 条>
• 午间(12:00-14:00):<1 条>
• 晚间(20:00-22:00):<1 条>

───
以上为民俗文化与娱乐参考,请结合现实理性判断。
```

## EN output template (when user spoke English)

```
【<Mode> Fortune | YYYY-MM-DD】

✨ Overall: Great / Good / Neutral / Caution (0–100)

1–2 sentences explaining why, citing the rule (R-value layer / date rule / chart palace).

🧭 Lucky direction: <direction>
🎨 Lucky colors: primary <color>, accent <color>
🔢 Lucky numbers: <n1>, <n2>[, <n3>]
📿 Lucky item: <item>

✅ Do today
1. <action>
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
• Birth tone: <from B parity + digit-sum>
• Day energy: <from D and W>
• Combined: <why this score, why these lucky elements>

💡 24-hour action plan
• Morning (07:00–09:00): <1 line>
• Midday (12:00–14:00): <1 line>
• Evening (20:00–22:00): <1 line>

───
For folklore and entertainment reference only — combine with judgment.
```

模式扩展(本周 / 本月 / 双人 / 场景)使用 `references/output_templates.md` 里的对应变体模板。

## 多语言响应规则

1. **语言跟随**:用户语言 → 全程同语言回复。中文优先(本 skill 默认),用户用英文时切换 EN 模板。
2. **专有术语**:命格 / 宫位 / 卦名保持中文原字,英文输出时括号注译。
3. **混合时**:用户日韩越输入,以英文模板为底 + 关键词意译。

## 档案与持久化

第一次用户提供完整信息(生日 + 性别 + 可选星盘)时,可选写入:

- 路径:`{baseDir}/user_profile.json`
- 字段定义:见 `references/user_profile_template.md`
- 仅用户明确说"记住我"/"保存"/"建档"才写
- 后续查询优先 `read` 档案,不要每次都问生日

环境只读时:仅在当前会话保留,提示 "当前环境无法持久化,如需开启请在可写环境运行"。

**绝不**预先打包真实用户档案 —— 仓库里只有 `references/user_profile_template.md`(纯字段说明)。

## 推送(Telegram / Feishu / Slack / Discord)

通过 openclaw runtime cron 调度。**本 skill 不含 push 脚本**(prompt-only)。

```bash
# 早 7 点推送(用户本地时间)
openclaw cron add "0 7 * * *" \
  "use lucky-today: 今日运势 (推送给 telegram chat_id <YOUR_ID>)"

# 晚 21 点推送次日预告
openclaw cron add "0 21 * * *" \
  "use lucky-today: 明日运势 (推送给 telegram chat_id <YOUR_ID>)"

openclaw cron list
openclaw cron delete <ID>
```

推送场景下:
1. 必须生成"可直接发送的最终文本"(严格按上面的模板,不要附 system 日志/sessionId)
2. 通过 openclaw runtime 的 channel 工具发送到 `delivery.to`
3. 若消息超出渠道单条限制,自动压缩"🔮 详细拆解"段,优先保留:标题 / 总览 / 幸运元素 / 宜忌 / 强禁忌 / 专项 / 行动建议
4. 缺渠道工具时:退化为普通回复 + 提示 "当前宿主缺少直发工具"

## 严格约束

- **禁止联网检索** — 仅本地推演 + 内部规则
- 输出为"民俗文化与娱乐参考",不得声称科学真实性
- 医疗/法律/投资类高风险话题:输出后追加一句"请理性判断"
- 同一输入应产出一致结果(评级/方位/颜色/数字),允许措辞变化

## 跨 skill 推荐

| 需求 | 推荐 skill |
|---|---|
| 我要排八字 / 紫微 / 奇门 完整命盘 | [yunshi](https://clawhub.ai/skills/yunshi) |
| 我是白羊 / 双子,今天星座运势 | [daily-astro](https://clawhub.ai/skills/daily-astro) |
| 我要做风水布局 | [fengshui](https://clawhub.ai/skills/fengshui) |
| 我要看深度命理人格分析 | [bazii-mingli](https://clawhub.ai/skills/bazii-mingli) |

---

*Version: 0.1.0 · Updated: 2026-05-18*
