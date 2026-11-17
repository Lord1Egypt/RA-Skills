# Goal Loop 执行监督

对复杂任务施加目标导向的执行监督，解决 AI 常见失效模式：忘记原始要求、漏项、只做容易部分、
失败即停、七八成就宣布完成、用解释或建议替代实施、长任务后丢失目标、恢复时从零重来。

## 包含的技能

- `goal-loop`（可由 `/goal-loop` 手动强制调用，也按任务复杂度自动触发）
  - Goal Capture：目标、完成定义、约束、交付物、验证方式
  - Goal Ledger：`TODO / IN_PROGRESS / DONE / BLOCKED / NOT_APPLICABLE / SUPERSEDED`，DONE 必须带证据
  - Engineering Loop：Inspect → Select → Execute → Validate → Repair → Revalidate
  - Anti-Laziness Gate：九类偷懒失效模式的强制自查
  - Truthful Verification：`VERIFIED / OBSERVED / INFERRED / UNVERIFIED` 四态证据标注
  - Exit Gate：16 项交付门禁；终态仅 `COMPLETE / PARTIAL / BLOCKED / REWORK`
  - Checkpoint：`PROJECT-CHECKPOINT.md` 自动创建、维护与恢复（模板在 `templates/`）

## 适用场景

软件开发与缺陷修复、网站建设、文档（Word/Excel/PPT/PDF）、数据分析、深度研究、文件批处理、
多 Agent 协同、跨会话长期项目。简单问答与微小修改不会启动任何流程。

## 与其它规则的关系

优先级：用户当前明确要求 → 项目自身规则（AGENTS.md / SPEC / README）→ 本套通用监督规则。
本套件只负责执行纪律，不改变项目的技术栈、目录边界与验收标准。

## 无连接器依赖

全部能力在本地文件与对话内即可完成，不依赖任何外部工具或连接器。
