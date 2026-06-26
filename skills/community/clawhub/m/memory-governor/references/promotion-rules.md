# Promotion Rules

## 总原则

升级不是复制粘贴，而是提炼。

只有当一条信息已经从“发生过什么”变成“以后怎么判断 / 怎么做”时，才值得升格。

## 规则

### daily → MEMORY

这是最容易和 Dreaming 重叠的路径，所以先分两种宿主：

- **Dreaming-enabled host**：优先由 Dreaming 负责 `daily_memory -> long_term_memory`
- **Dreaming-disabled host**：才由人工 promotion 作为 fallback

如果宿主 **没有启用 Dreaming**，满足任意两个条件时，才考虑从 `memory/YYYY-MM-DD.md` 升到 `MEMORY.md`：

- 两周后大概率仍然有效
- 在多个任务里重复出现
- 会影响未来判断或协作方式
- 已经从事件变成稳定模式

如果宿主 **启用了 Dreaming**：

- `daily_memory` 默认继续写入 daily layer
- Dreaming 负责后台整理、主题提炼和长期记忆 promote
- 人工只在 Dreaming disabled、Dreaming unavailable、或显式 override 时直接做 `daily -> MEMORY`

不要让人工 promotion 和 Dreaming 同时对同一批 daily notes 做默认长期化。

### correction → learning_candidates

默认先把明确纠错写进 `learning_candidates`。

原因：

- 用户纠正的是这一次的错，不一定已经证明是长期规则
- 单次纠错太容易过拟合到当前任务
- 候选层让宿主先收集证据，再决定是否值得硬化

### learning_candidates → reusable_lessons

满足任意两个条件时，才考虑升到 `reusable_lessons`：

- 同类问题在多个任务、日期或上下文中重复出现
- 已经能被改写成脱离当前案例的通用原则
- 用户明确把它表述为以后都应遵守的规则
- 它会稳定影响未来判断、执行或协作质量

例子：

- 纠错：别写客服腔
- 候选：这次输出太像客服模板，需要更直接
- 规则：默认直接、简洁、有判断

### self-improving/* → AGENTS

当经验会改变启动流程、协作边界、默认路由时，升级到 `AGENTS.md`。

### self-improving/* → TOOLS

当经验主要约束工具、命令、平台格式、配置时，升级到 `TOOLS.md`。

### self-improving/* → SOUL

当经验改变长期表达风格、判断方式、人格边界时，升级到 `SOUL.md`。

### session-state / working-buffer → 其他层

这两层默认不能直接升格。  
必须先提炼成稳定事实或复用规则，再进入长期层。

### learning_candidates → system_rules / tool_rules / AGENTS / TOOLS / SOUL

候选层默认不能直接升到系统级文件。

正确顺序是：

1. 先升到 `reusable_lessons`
2. 再判断它是否已经改变全局启动、工具、表达或协作规则

capture 阶段遇到歧义时，先看 [routing-precedence.md](routing-precedence.md)。

## Promotion Authority

为了避免功能冗余，默认 authority 应固定：

### Dreaming-preferred

- `daily_memory -> long_term_memory`

前提：

- 宿主已经启用 Dreaming
- 宿主接受 Dreaming 作为 daily consolidation engine

### Manual-only

- `learning_candidates -> reusable_lessons`
- `reusable_lessons -> system_rules`
- `reusable_lessons -> tool_rules`
- `reusable_lessons -> AGENTS / TOOLS / SOUL`
- `project_facts -> project docs`

原因：

- `learning_candidates` 承载的是显式纠错和待验证经验
- 系统级规则仍应保持人工审核和明确 hardening

Dreaming 不应直接决定 `AGENTS.md`、`TOOLS.md`、`SOUL.md` 这类治理文件。

## 两段式 Manual Path（不可跳级）

从候选层到系统级规则是**两段式 manual-only**，不允许一步跳：

1. `learning_candidates -> reusable_lessons`（manual-only）
2. `reusable_lessons -> system_rules / tool_rules / AGENTS / TOOLS / SOUL`（再一步 manual-only）

候选层**不能直接升到** `AGENTS` / `TOOLS` / `SOUL`，必须先过 `reusable_lessons`。跳级会把未验证的纠错直接固化成全局规则。

## Dreaming 不是无条件默认

`daily_memory -> long_term_memory` 交给 Dreaming 只在** Dreaming-enabled host** 下成立。

- Dreaming 启用且可用：Dreaming 负责 daily 巩固，人工不重复长期化同一批 daily notes
- Dreaming 未启用 / 不可用：才走人工 promotion 作为 fallback
- 人工 promotion 和 Dreaming 不应同时对同一批 daily notes 做默认长期化

## 禁止升级的情况

- 原始长日志直接升到长期层
- 未验证的猜测升到长期层
- 单次纠错直接升到 `reusable_lessons`
- 候选内容直接升到 `AGENTS.md` / `TOOLS.md` / `SOUL.md`
- 临时恢复线索直接升到 `MEMORY.md`
- 项目局部事实直接升到全局规则
- 在 Dreaming-enabled host 中，让人工 promotion 和 Dreaming 同时默认长期化同一批 daily 内容
