# Lesson Template

每次任务遇到非预见问题时，复制此模板创建新文件：
文件名格式：docs/lessons/YYYY-MM-DD-TASK-ID.md

---

## Lesson: [简短标题，描述问题]
- trigger: [什么情况下触发了这个问题，要够具体]
- wrong: [错误的做法或假设]
- right: [正确的做法]
- affected: [具体文件路径/函数名/API]   ← 有此字段 = 技术层 lesson，会进入 AGENTS.md
- agent_note: [orchestrator 下次注意]   ← 有此字段 = 流程层 lesson，会进入 skill
- tags: [相关标签，如 typescript, pg, auth, nextjs, ...]

注意：affected 和 agent_note 互斥，只填其中一个。
