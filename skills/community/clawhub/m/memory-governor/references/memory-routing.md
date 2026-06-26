# Memory Routing

## 原则

路由优先于存储。

先判断这条信息属于什么，再决定写到哪。  
不要因为“某个 skill 手上正好有一个文件可写”就顺手写进去。

更准确地说：

1. 先路由到 target class
2. 再由 adapter 映射到具体路径

## 路由表

| 信息类型 | 判断标准 | Target Class | 默认 adapter 示例 |
|---|---|---|---|
| 长期稳定偏好 | 跨任务稳定、两周后仍有效 | `long_term_memory` | `MEMORY.md` |
| 长期稳定事实 | 长期身份、环境、架构事实 | `long_term_memory` | `MEMORY.md` |
| 当天关键事件 | 与当天决策或后续恢复相关 | `daily_memory` | `memory/YYYY-MM-DD.md` |
| 阶段性进展 | 本周内还会回看 | `daily_memory` | `memory/YYYY-MM-DD.md` |
| 明确纠错 | 用户明确纠正、明确否定，但还未证明跨任务复用 | `learning_candidates` | `~/self-improving/candidates.md` 或 fallback |
| 新出现的可疑模式 | 像经验，但证据只有一次 | `learning_candidates` | `~/self-improving/candidates.md` 或 fallback |
| 可复用执行经验 | 可跨任务复用 | `reusable_lessons` | `~/self-improving/memory.md` 或 fallback |
| 领域专项经验 | 只在某领域复用 | `reusable_lessons` | `~/self-improving/domains/<domain>.md` 或 fallback |
| 项目级例外规则 | 只对当前项目有效 | `project_facts` | project docs / project adapter |
| 主动性边界 | 用户对提醒 / 推进方式的长期偏好 | `proactive_state` | `~/proactivity/memory.md` 或 combined fallback |
| 当前目标 / 阻塞 / 下一步 | 需要跨中断恢复 | `proactive_state` | `~/proactivity/session-state.md` 或 combined fallback |
| 临时恢复线索 | 容易丢、很快过期 | `working_buffer` | `~/proactivity/memory/working-buffer.md` 或 fallback |
| 工具 gotcha | 对未来工具使用有稳定价值 | `tool_rules` | `TOOLS.md` |
| 工作流规则 | 会改变未来启动、路由、协作方式 | `system_rules` | `AGENTS.md` |
| 行为 / 语气准则 | 会改变 agent 长期风格 | `system_rules` | `SOUL.md` |
| 项目事实 | 只对项目本身有意义 | `project_facts` | project docs |

## 特别说明

`AGENTS.md`、`TOOLS.md`、`SOUL.md` 是提炼后的治理目标，不是原始捕获入口。

`learning_candidates` 也是 capture 层，不是默认读取层。
它的职责是先容纳纠错和新出现的模式，再决定是否值得升到 `reusable_lessons` 或系统级规则。

默认顺序是：

- 先写 target class
- 再由 adapter 落到具体路径
- 候选内容先进入 `learning_candidates`
- 再提炼
- 最后才升格到系统级文件

具体 adapter 见 [adapters.md](adapters.md)。

边界项优先级见 [routing-precedence.md](routing-precedence.md)。
