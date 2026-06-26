# Skill Integration

## 目标

让多个 skill 服从同一套记忆规则，但不强迫它们共享同一种实现。

这份文档解决的问题是：

- 多个 skill 都在“写点什么”
- 它们各自有自己的路径和写法
- 但全局上不能各自发明记忆定义

## 核心原则

### 1. 统一 contract

所有 skill 都应共享这些定义：

- 记忆类型
- target classes
- 默认路由
- 升级规则
- 排除规则

### 2. 不统一 implementation

所有 skill 不必统一这些东西：

- 内部函数命名
- 内部目录布局
- 交互方式
- 下游工具适配方式
- 自己的执行流程

### 3. skill 只声明，不越权

每个 skill 可以声明：

- 自己会产出哪些信息类型
- 默认映射到哪些 target classes
- 当前环境里优先使用哪个 adapter
- 哪些信息只应该提炼后再写
- 哪些纠错默认应先进入候选层

每个 skill 不应自行定义：

- 新的全局记忆层
- 新的长期记忆标准
- 与内核冲突的升级规则

## 推荐接入方式

每个会写记忆的 skill，都应该在自己的 `SKILL.md` 或 reference 里明确：

1. 它会产生哪些 memory types
2. 这些类型默认映射到哪些 target classes
3. 当前环境优先使用哪些 adapter
4. 哪些内容绝不能直接写入长期层
5. stateful target 用 append、replace 还是 merge
6. 哪些纠错或新模式先进入 `learning_candidates`
7. 它依赖 `memory-governor` 的哪些规则

## 建议模板

可以在其他 skill 里用类似这样的声明：

```markdown
## Memory Contract

This skill follows `memory-governor`.

Typical outputs:
- project facts -> `project_facts`
- temporary recovery hints -> `working_buffer`
- explicit corrections -> `learning_candidates`
- reusable workflow lessons -> `reusable_lessons`

This skill does not define its own global memory rules.
```

## Correction Staging Rule

默认规则：

- 单次明确纠错 -> `learning_candidates`
- 已经被证明跨任务可复用的经验 -> `reusable_lessons`
- 会改变全局启动、工具、表达方式的规则 -> 仍然要先经过 promotion，再决定是否升到系统级文件

不要让 skill 自己跳过候选层，除非宿主已经有更强的人工审核或明确的长期规则判定。

## 典型对接关系

### `inbox-processor`

- 可以继续做 inbox 分类
- 但“稳定内容”“项目事实”“临时线索”的定义应服从内核

### `record-router`

- 可以继续做 Notion / OmniFocus 流转
- 但不能自行定义“长期记忆”的标准

### `notion-personal`

- 可以继续定义什么适合进 Notion
- 但它定义的是外脑沉淀规则，不是全局记忆规则

### `second-brain-claw`

- 可以继续做捕获、沉淀、执行分流
- 但上游“什么算记忆、写到哪一层”应由 `memory-governor` 约束

## 适配器思路

后续如果进入 Phase 2，可以为各 skill 增加轻量 adapter，而不是重写它们本身。

adapter 的职责：

- 把 skill 的输出映射到标准 memory types
- 把 memory types 映射到 target classes
- 调用统一路由规则
- 对 correction / emerging lesson 默认先走候选层
- 标记哪些内容需要提炼，哪些内容只能短存
- 对 stateful target 应遵守 canonical write semantics

## Sampling Boundary

自动采样或自动纠错抽取不是当前 phase 的强制能力。

在 `0.2.8-lite` 里：

- skill 可以声明自己会产出 correction candidates
- 宿主可以手动或半自动 review `learning_candidates`
- 但 `memory-governor` 不要求所有宿主立刻接入自动 sampling

先证明候选层有用，再让工具链依赖它。

## Dreaming-Aware Capture Policy

如果宿主启用了 Dreaming，skill 仍然不应把“让 Dreaming 以后自己清洗”当成偷懒理由。

默认分工应是：

- explicit corrections -> `learning_candidates`
- first-sighting emerging lessons -> `learning_candidates`
- same-day events and recurring context -> `daily_memory`
- stable reusable know-how already proven across tasks -> `reusable_lessons`

不要这样做：

- 把明确纠错直接丢进 `daily_memory`，指望 Dreaming 帮你决定它是不是长期规则
- 把 Dreaming 当成 `learning_candidates` 的替代品
- 让 Dreaming 直接生成系统级治理规则

一句话：

- `learning_candidates` handles explicit correction staging
- Dreaming handles background consolidation from short-term signals

两者可以配合，但不应争同一类输入。

## Compiled-Surface-Aware Capture Policy

新版 OpenClaw 增加了 People Wiki、Memory Wiki（Claim/Evidence）、Memory Palace、Imported Insights 等编译 / 运行时表面。

skill 不应把这些表面当成 capture 入口或新的 target class。

默认分工应是：

- 稳定人物事实 -> `long_term_memory`
- 项目内人物关系 -> `project_facts`
- 未验证的人物推断 -> `learning_candidates`
- 外部导入内容（Imported Insights） -> 先当 `learning_candidates`，不直接成长期记忆
- Claim / Provenance 是编译产物，不是 capture 层

不要这样做：

- 让 skill 直接写 `people/` 目录或 Person Card
- 把外部导入内容直接写进 `long_term_memory`
- 因为一条 Claim 出现在 Memory Wiki，就认为它已经被 promote

完整清单见 [compiled-surfaces.md](compiled-surfaces.md)。

## Skill Workshop 版本化

OpenClaw 2026.6.1 的 Skill Workshop 让 skill 走 提案 → 审核 → 发布，并带版本管理和回滚。

对 `Memory Contract` 的影响：

- skill 的 `Memory Contract` 声明应随 skill 版本一起管理
- skill 回滚时，它引入的记忆规则应一起回滚，避免留下孤儿规则
- 新版本 skill 如果改了 target class 映射，应显式说明旧映射如何迁移，而不是让两套映射同时生效

建议：

- 在 `Memory Contract` 里标注依赖的 `memory-governor` 最低版本
- 回滚 skill 时，同时检查它是否写过 `system_rules` / `tool_rules`，避免回滚后规则与代码不一致

## 禁止事项

- 不把 `memory-governor` 变成下游写入总线
- 不要求所有 skill 重构成同一种文件结构
- 不为了一致性而打断已有有效工作流
- 不把 Dreaming 当成跳过候选层或人工升格的理由
- 不把 People Wiki / Memory Wiki / Memory Palace 当成 capture 入口或新 target class
- skill 回滚后留下与代码不一致的孤儿记忆规则
