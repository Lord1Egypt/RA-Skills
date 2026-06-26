---
name: org-memory-curator
description: curates and archives durable organizational memory from project progress, meeting notes, feishu chat content, user clarifications, and markdown materials. use when any agent needs to decide whether information is worth preserving in long-term memory and where it should be stored in ai-org-memory.
---

# 概述

当任意 Agent 需要将项目进展、会议纪要、飞书聊天内容、用户补充说明或 markdown 材料沉淀到 `ai-org-memory` 时，使用本 skill。

本 skill 是一个**谨慎筛选型记忆归档器**，不是原始材料倾倒器。

它负责判断：

1. 这份内容是否值得进入长期记忆
2. 是否能归属到某个项目
3. 应该写入哪个记忆文件
4. 应该停留在项目层、lesson 层，还是提升到 engineering-standards

## 适用来源

本 skill 适用于以下输入来源：

- 飞书聊天内容
- 飞书会议纪要
- 项目的阶段汇总
- 用户临时补充说明
- 本地文档 / markdown 材料

## 工作模式

本 skill 采用“**谨慎筛选员**”模式。

处理顺序必须如下：

1. 先判断内容是否值得进入长期记忆
2. 若不值得，则不归档
3. 若值得，先判断是否能归属到具体项目
4. 若能归属到项目，优先按项目归档
5. 若不能明确项目，则不归档，并明确返回：
   `信息不足，暂不归档；请补充 project-id 或项目名称。`
6. 再按材料类型决定落到哪个文件
7. 只写入经过提炼的长期有效信息，不直接倾倒原始聊天记录

## 归档优先级

归档判断优先级固定为：

1. **项目优先**
2. 其次按**材料类型**
3. 最后参考**来源**

这意味着：

- 只要可以明确归属于某个项目，就优先写入该项目的 initiative 目录
- 只有在项目范围之外，且内容具有跨项目复用价值时，才考虑 lesson 或 engineering-standards

## 项目优先归档规则

若能识别项目，则优先归档到：

`/root/ai-company/memory/ai-org-memory/teams/team-alpha/initiatives/<project-id>/`

候选文件包括：

- `context.md`
- `roadmap.md`
- `reports.md`
- `decisions.md`
- `risks.md`

具体路由规则见：
[references/routing-matrix.md](references/routing-matrix.md)

## 向上提升规则

只在必要时将记忆向上提升：

- **项目级信息** -> 写入项目文件
- **可复用的团队经验** -> 写入 `lessons/...`
- **跨项目稳定工程规则** -> 写入 `company/engineering-standards.md`

禁止过早提升。

具体规则见：
[references/archive-rules.md](references/archive-rules.md)

## 输出要求

使用本 skill 时，必须输出结构化结果，至少包括：

- `archive_decision`：`archive` / `do_not_archive`
- `reason`
- `project_detected`：`yes` / `no`
- `project_id`：若已识别则给出
- `target_files`：目标文件列表
- `write_mode`：`create` / `append` / `no_write`
- `content_summary`
- `promotion_level`：`project` / `lesson` / `engineering-standard` / `none`

若信息不足，必须明确返回：

`信息不足，暂不归档；请补充 project-id 或项目名称。`

## 写入原则

归档时必须遵守：

- 优先写长期有效事实，不写原始噪音
- 保留范围、决策、风险、里程碑、验收结论、lesson
- 避免重复写入
- 避免写入低价值临时聊天
- 禁止将代码写入记忆库
- 禁止将记忆写入项目代码目录

## 输出对象

本 skill 支持判断并路由到以下目标：

- `context.md`
- `roadmap.md`
- `reports.md`
- `decisions.md`
- `risks.md`
- `lessons/...`
- `company/engineering-standards.md`

## 使用参考文件

- 归档判断规则：  
  [references/archive-rules.md](references/archive-rules.md)

- 文件路由矩阵：  
  [references/routing-matrix.md](references/routing-matrix.md)

- 输出模板：  
  [references/templates.md](references/templates.md)