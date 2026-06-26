# {{meeting_title}}

**日期**：{{date}} | **时长**：{{duration}} | **参会人**：{{participants}}

---

## 📌 关键讨论点
{{#each key_discussions}}
- **{{topic}}**：{{summary}}
{{/each}}

## ✅ 决策事项
{{#each decisions}}
- [决策] {{decision}}（{{made_by}}）
{{/each}}

## 🎯 行动项

| # | 责任人 | 任务 | 截止 | 优先级 |
|---|-------|------|------|--------|
{{#each action_items}}
| {{id}} | {{who}} | {{what}} | {{when}} | {{priority_emoji}} {{priority}} |
{{/each}}

## 💡 会议洞察
- **情绪氛围**：{{sentiment}}
- **潜在风险**：{{risks}}
- **会议效率评分**：{{effectiveness_score}}/10

---
*由 MeetingOS 🧠 自动生成 · [ClawHub](https://clawhub.io/skills/meetingos)*
