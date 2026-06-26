# Adapter Manifest

## Goal

让 custom host 可以显式声明：

- 自己实现了哪些 target classes
- 每个 target class 映射到哪些路径
- 是 single 还是 split adapter
- 哪些 target 需要结构化 schema 校验

这样 host checker 就不必只靠 reference profile 猜目录。

## File Name

默认文件名：

- `memory-governor-host.toml`

推荐放在宿主根目录。

## Minimal Shape

```toml
version = "0.1"
profile = "generic"

[targets.reusable_lessons]
mode = "single"
paths = ["memory/reusable-lessons.md"]
structured = true
```

## Top-Level Keys

- `version`
  当前 manifest 版本。推荐先用 `"0.1"`。
- `profile`
  可选。宿主自我声明的 profile，比如 `"generic"`、`"openclaw"`、`"custom"`。
- `[integration]`
  可选。把宿主入口和 memory-writing skill contract 也声明进去，方便 checker 验证“真的接线了”。
- `[targets.*]`
  每个 target class 一张表。

## Optional Integration Table

如果你想让 checker 不只验证 adapter，还验证宿主接线，可加：

```toml
[integration]
host_entry_paths = ["HOST.md"]
writer_contract_paths = ["skills/example-writer/SKILL.md"]
```

字段含义：

- `host_entry_paths`
  宿主级入口文件，比如 `HOST.md`、`AGENTS.md`
- `writer_contract_paths`
  会写记忆的 skill contract 文件

checker 当前行为：

- host entry 必须存在并明确提到 `memory-governor` -> `OK`
- writer contract 必须存在，并同时包含 `## Memory Contract` 和 `memory-governor` -> `OK`
- 声明了但文件不存在，或只是占位内容 -> `ERROR`
- 不声明 -> 不报错，但验证范围只覆盖 adapter 层

## Supported Target Classes

当前标准 target classes：

- `long_term_memory`
- `daily_memory`
- `learning_candidates`
- `reusable_lessons`
- `proactive_state`
- `working_buffer`
- `project_facts`
- `system_rules`
- `tool_rules`

## Per-Target Fields

### `mode`

支持：

- `single`
- `split`
- `directory`
- `pattern`

含义：

- `single` -> 一个文件实现一个 target
- `split` -> 多个文件联合实现一个 target
- `directory` -> 一个目录承接这个 target
- `pattern` -> 用路径模式描述，例如 daily note

### `paths`

必须是字符串数组。

示例：

```toml
paths = ["memory/proactive-state.md"]
paths = ["~/proactivity/memory.md", "~/proactivity/session-state.md"]
paths = ["memory"]
paths = ["notes/daily/YYYY-MM-DD.md"]
```

规则：

- 相对路径按宿主根目录解析
- `~` 会展开到当前用户 home
- `single` 必须只有一个路径
- `split` 至少两个路径
- `directory` 应声明一个目录根，而不是具体文件
- `pattern` 应声明一个稳定命名模式，而不是临时通配符

### `fallback_paths`

可选字符串数组。

用于声明：

- primary adapter 不可用时
- 当前 target class 可以退回到哪些本地 fallback 路径

示例：

```toml
[targets.reusable_lessons]
mode = "single"
paths = ["~/self-improving/memory.md"]
fallback_paths = ["memory/reusable-lessons.md"]
structured = false
```

解释：

- `paths` 表示宿主当前优先使用的 adapter
- `fallback_paths` 表示 primary 缺失时可接受的本地降级落点

当前 checker 的行为是：

- primary 存在时，按 primary 检查
- primary 缺失但 fallback 完整存在时，给出 fallback `OK`
- primary 和 fallback 都缺时，报错

### `structured`

可选布尔值。

用于声明这个 target 是否应该走 schema 校验。

默认建议：

- `learning_candidates` -> `true`
- `reusable_lessons` -> `true`
- `proactive_state` -> `true`
- `working_buffer` -> `true`

但如果宿主当前接的是 legacy external adapter，而且这些文件还不是 schema-frontmatter 格式，也可以先声明成 `false`。

这表示：

- target class 语义仍然成立
- checker 只做路径和模式检查
- 宿主暂时不承诺 machine-checkable structure

## Example

```toml
version = "0.1"
profile = "generic"

[integration]
host_entry_paths = ["HOST.md"]
writer_contract_paths = ["skills/example-writer/SKILL.md"]

[targets.long_term_memory]
mode = "single"
paths = ["memory/long-term.md"]
structured = false

[targets.daily_memory]
mode = "pattern"
paths = ["notes/daily/YYYY-MM-DD.md"]
structured = false

[targets.learning_candidates]
mode = "single"
paths = ["memory/learning-candidates.md"]
structured = true

[targets.reusable_lessons]
mode = "single"
paths = ["memory/reusable-lessons.md"]
structured = true

[targets.proactive_state]
mode = "single"
paths = ["memory/proactive-state.md"]
structured = true

[targets.working_buffer]
mode = "single"
paths = ["memory/working-buffer.md"]
structured = true
```

## Primary + Fallback Example

```toml
[targets.proactive_state]
mode = "split"
paths = ["~/proactivity/memory.md", "~/proactivity/session-state.md"]
fallback_paths = ["memory/proactive-state.md"]
structured = false

[targets.working_buffer]
mode = "single"
paths = ["~/proactivity/memory/working-buffer.md"]
fallback_paths = ["memory/working-buffer.md"]
structured = false
```

## Reusable Lessons as Directory

如果宿主按 domain 或 project 拆分 `reusable_lessons`，推荐直接声明成 `directory`：

```toml
[targets.reusable_lessons]
mode = "directory"
paths = ["memory/reusable-lessons"]
structured = false
```

常见布局例如：

- `memory/reusable-lessons/general.md`
- `memory/reusable-lessons/product.md`
- `memory/reusable-lessons/project-alpha.md`

这表示：

- `reusable_lessons` 仍然是一个 target class
- 只是 adapter 选择按目录承载，而不是单文件承载

## Reusable Lessons as Pattern

如果宿主想保留显式命名约定，也可以用 `pattern`：

```toml
[targets.reusable_lessons]
mode = "pattern"
paths = ["memory/reusable-lessons/*.md"]
structured = false
```

适合：

- host 已经有稳定文件命名规则
- checker 当前只需要承认这个 target 的存在方式
- 你还不想把它收紧成单目录 contract

对于 `pattern`，当前 checker 会验证声明本身，不会尝试枚举所有匹配文件。

## Split Adapter Example

```toml
version = "0.1"
profile = "openclaw"

[targets.proactive_state]
mode = "split"
paths = ["~/proactivity/memory.md", "~/proactivity/session-state.md"]
structured = true
```

对于 `split` adapter，checker 会把“至少一个 canonical current-state slice 通过 schema 校验”视为通过条件。

## Mode Selection Advice

对 `reusable_lessons` 来说，推荐顺序通常是：

1. `single`
2. `directory`
3. `pattern`

选择原则：

- 想要最简单、最强约束：`single`
- 已经按 domain / project 拆分：`directory`
- 已有成熟命名约定但不想重构：`pattern`

## project_facts 是特殊的

`project_facts` 是 9 个 target class 里唯一**天然多项目**的。其余 8 个都是工作区全局的，但 `project_facts` 离开项目就没意义。

因此：

- **不要**把 `project_facts` 映射成单个全局文件（`mode = "single"` + 一个工作区根文件）
- 多项目宿主应使用 `directory` 或 `pattern`，承认事实分散在多个项目里：

```toml
[targets.project_facts]
mode = "directory"
paths = ["docs/projects"]
```

或：

```toml
[targets.project_facts]
mode = "pattern"
paths = ["docs/projects/*.md"]
```

- 如果项目已经有自己的 `README.md`、`progress.md` 等文档，可以直接写进项目自己的文档，不强制单独建文件
- 如果宿主完全不想在工作区根声明 `project_facts`（每个项目自己管），也可以从 manifest 省略这一条——但要意识到这样 checker 就无法验证它的路由

常见错误：

- 把多个项目的事实挤进一个全局 `docs/project-facts.md`，破坏项目作用域语义
- 用 `mode = "single"` 暗示 project_facts 像其他 target 一样只有一个全局落点

## Checker Behavior

`check-memory-host.py` 的顺序是：

1. 先找 `memory-governor-host.toml`
2. 如果存在，就按 manifest 检查
3. 如果不存在，才回退到 reference profile auto-detect

这意味着 manifest 优先级高于目录猜测。

在 manifest 内部，优先级则是：

1. `paths`
2. `fallback_paths`

## Recommended Practice

- reference profile 宿主也可以写 manifest
- custom host 强烈建议写 manifest
- `adapter-map.md` 可以继续保留给人看
- `memory-governor-host.toml` 负责给工具读
