# Visual / comic summary prompt

Use when the user asks for 漫画总结, 图片总结, visual summary, or a prompt for a text-to-image model.

## Two-stage process

1. First extract meeting content faithfully:
   - real speakers with substantive speech only
   - speaker identities/roles only if present
   - core issues, facts, data, decisions, and interactions
   - meeting type and suitable layout
2. Then write the image-generation prompt. Do not call an image-generation service unless separately asked.

## Strict fidelity rules

- All speaker names/ids must exist in the transcript.
- Keep only speakers with substantive speech; ignore people merely mentioned by others, no-speech participants, pure acknowledgements, or pure self-introductions.
- All speaker content must be traceable to the transcript.
- Do not invent identities, roles, statements, relationships, numbers, or conclusions.
- If content is unclear or missing, state that it is unclear instead of guessing.

## Meeting type to layout mapping

| Meeting type | Recommended layout | Visual logic |
|-|-|-|
| 日常站会/进度同步会 | vertical timeline or cards | completed / next / blockers |
| 项目启动/规划会 | mind-map or goal pyramid | goal, scope, milestones, owners |
| 头脑风暴/创意讨论会 | clustered sticky notes or bubbles | idea grouping |
| 问题分析与解决会 | left-to-right flow or 5WHY tree | problem → root cause → solution → action |
| 季度/年度复盘会 | two-column review/outlook or SWOT | wins, gaps, next plan |
| 培训/知识分享会 | numbered steps or layered info | concept → method → procedure |
| 评审/决策会 | balance/comparison/dashboard | options, pros/cons, decision |
| 发布/里程碑会 | stage/achievement layout | result, impact, celebration |
| 圆桌会议 | circular equal layout | central topic with speakers around it |
| 领导致辞 | vision ladder/top-center radial | current state → vision/goal |

## Prompt output format

```markdown
请根据以下会议总结内容，生成一张图片总结。

**【会议内容总结】**
1. **会议主题**：...
2. **会议内容**：{发言人1: {角色/身份, 核心发言关键词}, 发言人2: {...}}
3. **关键结论/行动项**：...

**【视觉风格与规范】**
1. **整体风格**：纯白背景；手绘简笔画线条 + 扁平化卡通图标 + 商务PPT版面逻辑 + 手账/板报装饰；色彩统一和谐。
2. **图标使用**：人物头像图标对应核心发言人；对话泡承载发言内容；连接线/箭头表示人物与发言关联；根据会议类型添加主题图标。
3. **版面要求**：采用{根据会议类型选择的布局}，视觉动线清晰，重点突出。
4. **细节要求**：避免写实和复杂渲染；线条简洁轻盈，色块明快平整；可使用虚线、星点、轻微阴影或高光。
5. **语言要求**：中文为主；除原文专有英文外，禁止英文标注。
6. **额外要求**：列出核心发言人的姓名/身份、发言内容关联方式、内容组织方式；如果原文残缺，明确说明。
```

## Self-check before output

- Every included speaker has substantive source speech.
- Every claim and relation is source-grounded.
- The chosen layout matches the meeting type.
- The prompt clearly tells the image model how to associate people and speech.
