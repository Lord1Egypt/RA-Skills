# Adapters

## 目标

把抽象的 memory target classes 映射到当前环境里的具体落地点。

这意味着：

- 内核定义“去哪里”
- adapter 决定“在这个环境里具体写到哪个文件”

## 默认 target classes

| Target Class | 含义 |
|---|---|
| `long_term_memory` | 长期稳定记忆 |
| `daily_memory` | 每日事件与阶段记录 |
| `learning_candidates` | 低承诺纠错与新模式候选层 |
| `reusable_lessons` | 可复用经验、纠错、长期执行教训 |
| `proactive_state` | 主动性边界族和当前推进态 |
| `working_buffer` | 极短期恢复线索 |
| `project_facts` | 项目内事实 |
| `system_rules` | 系统级工作流和行为规则 |
| `tool_rules` | 工具、命令、平台约束 |

## 默认 adapter 映射

这些是默认值，不是强制值：

| Target Class | Preferred Adapter | Default Path |
|---|---|---|
| `long_term_memory` | built-in | `MEMORY.md` |
| `daily_memory` | built-in | `memory/YYYY-MM-DD.md` |
| `learning_candidates` | `self-improving` if resolved | `~/self-improving/candidates.md` |
| `learning_candidates` | packaged fallback template | `assets/fallbacks/learning-candidates.md` |
| `reusable_lessons` | `self-improving` if resolved | `~/self-improving/...` |
| `reusable_lessons` | packaged fallback template | `assets/fallbacks/reusable-lessons.md` |
| `proactive_state` | `proactivity` if resolved | `~/proactivity/memory.md` + `~/proactivity/session-state.md` |
| `proactive_state` | packaged fallback template | `assets/fallbacks/proactive-state.md` |
| `working_buffer` | `proactivity` if resolved | `~/proactivity/memory/working-buffer.md` |
| `working_buffer` | packaged fallback template | `assets/fallbacks/working-buffer.md` |
| `project_facts` | built-in | project docs |
| `system_rules` | built-in | `AGENTS.md` / `SOUL.md` |
| `tool_rules` | built-in | `TOOLS.md` |

## Dreaming Boundary

如果宿主启用了 OpenClaw Dreaming，需要把它当成 **consolidation engine**，不是新的 target class。

固定边界：

- `DREAMS.md` is a dreaming artifact, not a target class
- `memory/.dreams/` is engine state, not host memory contract
- skills should not write directly into either of them
- adapter tables should not model `dream_diary` or `dream_state` as standard memory targets

Dreaming 的默认职责应限定在：

- reading short-term memory signals
- consolidating daily memory
- promoting durable output into `MEMORY.md`

它不应替代：

- `learning_candidates`
- `reusable_lessons`
- `system_rules`
- `tool_rules`

## Optional Skill Policy

可选 skill 不应成为内核前提。

因此：

- `learning_candidates` 是低承诺 capture layer，不是 `reusable_lessons` 的别名
- `self-improving` 是 `reusable_lessons` 的一个 adapter，不是内核本身
- `self-improving` 也可以承接 `learning_candidates`
- `proactivity` 是 `proactive_state` / `working_buffer` 的一个 adapter，不是全局记忆的唯一来源

如果某个 optional skill 没安装：

- target class 依然存在
- 只是换用 fallback adapter

## Proactive State Contract

`proactive_state` 默认应理解为一个抽象 state family。

它至少包含：

- current task truth

它还可以包含：

- durable proactive boundaries

允许两种实现：

1. one combined file, such as `proactive-state.md`
2. one split adapter, such as `memory.md` + `session-state.md`

如果是 split implementation：

- `session-state.md` is the canonical slice for current objective / blocker / next move
- the durable boundary slice complements it, but does not replace current task truth

## Adapter Resolution Order

“resolved” 的推荐判定顺序应明确固定：

1. host config explicitly maps the target class
2. the host explicitly declares an installed adapter skill
3. the expected adapter-owned path exists and is recognized by the host
4. otherwise use the packaged fallback template

不要只写 “if available” 而不定义顺序。

## Fallback Principle

fallback 的目标不是完美，而是不让内核失效。

一个好的 fallback 应该：

- 本地可写
- 含义明确
- 容易后续迁移
- 不伪装成正式插件能力

当前默认 packaged fallback 模板：

- `assets/fallbacks/learning-candidates.md`
- `assets/fallbacks/proactive-state.md`
- `assets/fallbacks/reusable-lessons.md`
- `assets/fallbacks/working-buffer.md`

某些宿主可以把这些模板复制到自己的本地路径中。  
例如 OpenClaw reference profile 当前常见落点是：

- `workspace/memory/reusable-lessons.md`
- `workspace/memory/proactive-state.md`
- `workspace/memory/working-buffer.md`

## 禁止事项

- 不把 optional skill 写成 mandatory dependency
- 不把某个 adapter 的路径当成 target class 本身
- 不因为缺少某个 skill 就重写内核定义
- 不把 `DREAMS.md` 或 `memory/.dreams/` 伪装成普通 target class adapter
