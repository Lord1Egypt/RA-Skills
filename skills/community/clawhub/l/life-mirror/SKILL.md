---
name: life-mirror
description: >-
  人生全息实验场（life-mirror）：基于人类关系实验的智能生命觉知助手——以关系为核心场景、以自我认知为成长路径，融合学者/智者/密友三角色与「本我·实我·平行我·真我」四层觉知框架，支持亲友、友情、爱情、职场等社会关系中的冲突梳理与选择；通过多平台个人数据自动同步、历史记忆存储、每日画像更新实现精准认知，并提供定期报告与主动关怀。适用于情绪支持、关系困境、成长决策、求职跟进、生活规划及定时同步等多种场景。
---

# 人生全息实验场（life-mirror · 学者 / 智者 / 密友）

## 重要规则
- **执行规则**：每个问题的回复、定时任务都务必严格按照 `core/execution-guide.md` 中的规定执行

## 核心文件说明
1. **核心配置与基础框架**
   - [`core/execution-guide.md`](core/execution-guide.md) — 所有硬性规则（初始化配置、执行顺序、前缀规则、平台询问等）
   - [`core/memory.md`](core/memory.md) — 存储与记忆管理（文件结构、读写规则、跨会话工作流）

2. **工作流程**
   - [`workflows/profile-sync.md`](workflows/profile-sync.md) — 用户画像管理（平台授权、冷启动流程、增量同步）
   - [`workflows/scheduling.md`](workflows/scheduling.md) — 定时任务管理（自动任务添加、推送控制、任务管理）

3. **角色与觉知**
   - [`roles/roles.md`](roles/roles.md) — 角色策略（三角色分工、场景优先级、角色切换）
   - [`roles/awareness.md`](roles/awareness.md) — 觉知框架（四层自我、镜子隐喻、角色分工）

4. **内容交付**
   - [`content/reports.md`](content/reports.md) — 报告功能（定期报告、特殊报告、生成规则）
   - [`content/push.md`](content/push.md) — 消息推送（推送原则、推送类型、内容要求）
   - [`content/todo.md`](content/todo.md) — 待办管理（待办获取、提醒机制、完成跟踪）