# Memory Templates - 记忆写入模板

快速参考模板，用于规范记忆文件格式。

## SESSION-STATE.md 模板

```markdown
# SESSION-STATE.md — 活跃工作记忆

此文件是Agent的"热内存"，在压缩、重启、切换任务后依然存活。

## Current Task
[当前正在进行的任务，一句话描述]

## Key Context
- User preference: [用户明确表达的偏好]
- Decision made: [最近的重要决策]
- Blocker: [当前障碍，如果有]

## Pending Actions
- [ ] [待办事项1]
- [ ] [待办事项2]

## Recent Decisions
- [决策1]: [原因]
- [决策2]: [原因]

---
*Last updated: YYYY-MM-DD HH:MM*
*Rule: Write BEFORE responding (WAL protocol)*
```

---

## MEMORY.md 索引模板

```markdown
# MEMORY.md — 长期记忆索引

此文件是长期记忆的目录，不存储具体内容，只指向分类文件。

## User Memory
用户画像、偏好、角色信息
- [profile](memory/user/profile.md) — [简短描述]
- [preferences](memory/user/preferences.md) — [简短描述]

## Feedback Memory
用户纠正、确认、风格指导
- [item-name](memory/feedback/item-name.md) — [简短描述]

## Project Memory
项目状态、决策、推理过程
- [item-name](memory/project/item-name.md) — [简短描述]

## Reference
外部资源、工具、位置信息
- [item-name](memory/reference/item-name.md) — [简短描述]

---
*Created: YYYY-MM-DD*
*Max size: 5KB (prune when exceeded)*
```

---

## 分类记忆文件模板

### User Memory

```markdown
---
name: [记忆名称]
description: [一行描述，用于判断相关性]
type: user
created: YYYY-MM-DD
---

## 用户画像
- 角色: [职业/身份]
- 技术栈: [技术背景]
- 背景: [经验描述]

## 沟通偏好
- 风格: [简洁/详细]
- 格式: [列表/表格/代码]
- 语言: [中文/英文/混合]

## 工作习惯
- 时区: [时区]
- 工作时间: [时间段]

## 应用方式
当回复时，[具体指导]。
```

### Feedback Memory

```markdown
---
name: [记忆名称]
description: [一行描述]
type: feedback
created: YYYY-MM-DD
---

## 纠正/确认内容
用户[纠正/确认]: [具体内容]

## 原因
[为什么重要]

## 应用方式
当[场景]时，[具体行为]。

## 避免
避免: [不应做的行为]
使用: [应做的行为]
```

### Project Memory

```markdown
---
name: [记忆名称]
description: [一行描述]
type: project
created: YYYY-MM-DD
---

## 决策内容
[具体决策]

## 原因
1. [原因1]
2. [原因2]
3. [原因3]

## 权衡
- [选项A]: [优点和缺点]
- [选项B]: [优点和缺点]

## 应用方式
当[场景]时，[具体行为]。
相关工具: [相关工具列表]
```

### Reference Memory

```markdown
---
name: [记忆名称]
description: [一行描述]
type: reference
created: YYYY-MM-DD
---

## 资源位置
- [资源类型1]: [路径/地址]
- [资源类型2]: [路径/地址]

## 重要文件
- [文件描述]: [路径]

## 应用方式
当用户询问[场景]时，指向以上路径。
```

---

## Daily Log 模板

```markdown
# YYYY-MM-DD Daily Log

## Session Log

### HH:MM - [主题]
**User said**: [用户说的关键内容]
**Action**: [Agent执行的动作]
**Remember**: [需要记住的要点]

### HH:MM - [主题]
**User said**: [用户说的关键内容]
**Decision**: [做出的决策]
**Reason**: [决策原因]

---

## End of Day Summary

### Tasks Completed
- [x] [任务1]
- [x] [任务2]

### In Progress
- [ ] [进行中任务]

### Important to Remember
1. [关键点1]
2. [关键点2]

### Follow Up Needed
- [ ] [后续事项]
```

---

## 写入优先级参考

| 优先级 | 时机 | 写入位置 | 模板 |
|--------|------|----------|------|
| 1 | 需要即时缓存 | Session Buffer | 简短备注 |
| 2 | 会话开始（今天） | 今日Daily Log | Session Start |
| 3 | 会话开始（近期） | 最近7天 | 先搜索 |
| 4 | 用户分享信息 | memory/user/ | User Profile |
| 5 | 承诺事项 | SESSION-STATE.md | Commitment |
| 6 | 用户纠正 | memory/feedback/ | User Correction |
| 7 | 项目决策 | memory/project/ | Project Decision |
| 8 | 外部资源 | memory/reference/ | Reference |
| 9 | 会话结束 | 今日Daily Log | Daily Summary |

---

## 快速格式化规则

### 精简原则

```markdown
<!-- Good: 精简有效 -->
- User preference: 深色模式

<!-- Bad: 冗余无效 -->
用户说他喜欢深色模式，不喜欢浅色模式，之前用过浅色觉得眼睛不舒服，所以偏好深色
```

### 包含上下文

```markdown
<!-- Good: 有上下文 -->
## 原因
用户熟悉React生态，团队有开发经验。

<!-- Bad: 无上下文 -->
## 原因
因为好用。
```

### 使用时间戳

```markdown
<!-- Good: 绝对时间 -->
*Created: 2026-04-06*

<!-- Bad: 相对时间 -->
*Created: 昨天*
```

### 交叉引用

```markdown
<!-- Good: 有关联 -->
## 相关决策
参见 [react-decision](../project/react-decision.md)

<!-- Bad: 孤立无关联 -->
(未提及相关决策)
```

---

## 示例：完整工作流

### 场景：用户表达偏好

```
用户: "我喜欢深色模式，界面用深色主题"

Step 1: 检测到偏好表达 (type=user)
Step 2: 写入SESSION-STATE.md
Step 3: 存储到向量
Step 4: 创建/更新 memory/user/preferences.md
Step 5: 更新 MEMORY.md 索引
Step 6: 返回响应
```

### SESSION-STATE.md 更新

```markdown
## Key Context
- User preference: 深色模式，界面使用深色主题
```

### 向量存储

```json
{
  "content": "用户偏好深色模式，界面使用深色主题",
  "type": "user",
  "importance": 0.9
}
```

### memory/user/preferences.md

```markdown
---
name: preferences
description: 用户界面偏好
type: user
created: 2026-04-06
---

## 界面偏好
- 主题: 深色模式
- 原因: 用户明确表达喜欢深色

## 应用方式
当生成界面设计、代码示例时，使用深色主题配色。
```

### MEMORY.md 更新

```markdown
## User Memory
- [preferences](memory/user/preferences.md) — 用户界面偏好深色模式
```

---

*Templates Version: 1.0*
*Quick reference for memory writing*
