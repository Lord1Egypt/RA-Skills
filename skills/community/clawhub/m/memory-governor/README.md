# Memory Governor

**Memory governance for AI agents. Aligned with the OpenClaw 2026.6.x memory stack: Dreaming, Active Memory, Memory Wiki, People Wiki, and the Skill Workshop / Workboard era.**

Languages: **English** | [中文](#中文)

`memory-governor` is a governance kernel for hosts that already have multiple memory layers, memory-writing skills, or optional adapters. It was built to give those systems one shared contract for deciding what should be remembered, where it should go, when it should stay temporary, and when it is safe to harden into durable guidance.

OpenClaw kept expanding its runtime memory stack across the 2026.4 and 2026.6 lines: Dreaming for background consolidation, Active Memory for pre-reply recall, Memory Wiki for compiled knowledge views, People Wiki (2026.4.29) for entity-compiled profiles and provenance, plus Skill Workshop and Workboard (2026.6.1) for governed skill lifecycle and multi-agent coordination. This release keeps `memory-governor` focused on the governance layer it was always designed for, while aligning its boundaries with all of those runtime systems so they do not compete.

In short:

- Dreaming handles background consolidation.
- Active Memory handles runtime recall before replies.
- Memory Wiki handles compiled wiki-style views, claims/provenance, and shared search surfaces.
- People Wiki handles entity-compiled profiles and relationship graphs.
- Skill Workshop / Workboard handle skill lifecycle and multi-agent coordination.
- `memory-governor` handles capture rules, target classes, correction staging, scope/privacy boundaries, and hardening boundaries.

## Why Install It

Install `memory-governor` when your agent memory is starting to drift:

- multiple skills write memory-like state
- explicit corrections are getting mixed into daily notes
- single observations harden into long-term rules too quickly
- optional adapters such as `self-improving` or `proactivity` create routing ambiguity
- you want one contract before the system becomes path-based chaos

This is not an execution-first productivity skill. It is infrastructure for memory-heavy agent systems.

## What It Adds

- Standard memory target classes:
  `long_term_memory`, `daily_memory`, `learning_candidates`, `reusable_lessons`, `proactive_state`, `working_buffer`, `project_facts`, `system_rules`, and `tool_rules`
- A routing model:
  `memory type -> target class -> adapter / fallback`
- A low-commitment `learning_candidates` layer for explicit corrections and first-sighting lessons
- Candidate review guidance for `keep / promote / discard`
- Clear promotion authority:
  Dreaming-preferred for `daily_memory -> long_term_memory`, manual review for correction hardening and system-rule promotion
- Boundaries for Dreaming artifacts:
  `DREAMS.md` and `memory/.dreams/` are engine-owned artifacts, not standard memory target classes
- A consolidated compiled-surfaces boundary:
  People Wiki, Memory Wiki claims, Memory Palace, Imported Insights, and Provenance Views are all downstream compiled / runtime surfaces, not target classes
- A scope / privacy boundary:
  scoped memories (project, chat, agent) should record scope at capture time so compiled surfaces do not widen them, complementing Active Memory Filters such as `allowedChatIds` / `deniedChatIds`
- A multi-agent writer rule:
  coordinated agents on Workboard should not each harden unconfirmed intermediate state
- Host manifest support through `memory-governor-host.toml`
- Host checker, frontmatter validator, candidate reviewer, and generic-host bootstrap scripts
- A generic host example that does not require OpenClaw-specific directories

## Core Model

`memory-governor` separates memory decisions into three layers:

1. **Memory type**
   What kind of information is this?
2. **Target class**
   Which abstract memory layer should own it?
3. **Adapter / fallback**
   Where does this host store that target class?

That keeps the core contract independent from any one plugin, folder layout, or host implementation.

## Alignment with Dreaming

`memory-governor` was not created because Dreaming exists. It was created to govern memory capture, routing, staging, and hardening in hosts that were already becoming complex.

Dreaming changes the integration boundary:

- it should be preferred for `daily_memory -> long_term_memory`
- it should not replace explicit correction staging
- it should not turn `DREAMS.md` or `memory/.dreams/` into normal memory target classes

Recommended split:

- Dreaming:
  `daily_memory -> long_term_memory`
- `memory-governor`:
  capture rules, correction staging, adapter boundaries, and manual hardening
- Human / explicit review:
  `learning_candidates -> reusable_lessons -> system_rules / tool_rules`

Do not model `DREAMS.md` or `memory/.dreams/` as normal memory target classes. Treat them as Dreaming-owned artifacts.

See [dreaming-integration.md](references/dreaming-integration.md).

## Alignment with Active Memory and Memory Wiki

Recent OpenClaw updates make the runtime boundary clearer:

- Active Memory is the runtime recall layer.
- Memory Wiki is a compiled knowledge layer built from memory artifacts.
- `memory-governor` should stay upstream of both.

Recommended interpretation:

- `memory-governor` decides what kind of memory something is and whether it should harden at all
- OpenClaw memory plugins decide runtime recall and promotion behavior
- Memory Wiki compiles durable knowledge views from existing memory, claims, and provenance trails

Do **not** treat wiki page types or vault folders as new target classes.

Examples of things that should remain adapter details, not governance primitives:

- `WIKI.md`
- `entities/`
- `concepts/`
- `syntheses/`
- wiki-native digests or claim indexes

Those are useful compiled outputs, but they are not replacements for:

- `long_term_memory`
- `learning_candidates`
- `reusable_lessons`
- `system_rules`
- `tool_rules`

Practical rule:

- canonical durable truth still lives in the host's memory contract
- wiki outputs should be treated as downstream compiled views, recall aids, and provenance-friendly summaries

## Alignment with People Wiki and Imported Insights

OpenClaw 2026.4.29 added People Wiki (entity-compiled profiles, relationship graphs, canonical aliases) and provenance views, plus Active Memory Filters for recall-time access control. Later builds added Imported Insights and Memory Palace.

The boundary is the same as for Memory Wiki:

- People Wiki, Person Cards, Relationship Graphs, Memory Palace, and Provenance Views are compiled / UI surfaces, not target classes
- entity facts are captured upstream into `long_term_memory` / `project_facts` / `learning_candidates`, then compiled
- Imported Insights are unverified by this host and should stage through `learning_candidates`, not jump to canonical truth
- Active Memory Filters (`allowedChatIds` / `deniedChatIds`) are a recall-time control; capture-time governance still records scope on the target class entry so a compiled surface cannot widen it

The full surface inventory and the capture-vs-compile rule live in [compiled-surfaces.md](references/compiled-surfaces.md).

## Implications for OpenClaw Hosts

If your host enables newer OpenClaw memory features:

- keep startup reads minimal and let Active Memory do the heavy recall work
- keep `working_buffer` and current-task `proactive_state` compact, because session pruning and automatic memory flush increase the value of short, high-signal recovery state
- keep explicit corrections out of wiki compilation inputs until they have cleared candidate review
- keep `learning_candidates -> reusable_lessons -> system_rules / tool_rules` as a manual hardening path even if the runtime stack becomes more capable

This prevents three common mistakes:

- reading too many layers manually even though Active Memory already performs recall
- treating compiled wiki pages as if they were canonical governance sources
- allowing one-off corrections to surface everywhere before they are proven durable

## Readiness Model

`memory-governor` uses three readiness states:

- `Installed`
  The skill is available and the rules can be read.
- `Integrated`
  The host has wired itself to the memory contract.
- `Validated`
  The host checker has confirmed the wiring.

Installation does **not** silently rewrite `AGENTS.md`, other skills, or existing memory files. Host integration should be explicit.

## Quick Start

Recommended first reading path:

1. [SKILL.md](SKILL.md)
2. [memory-routing.md](references/memory-routing.md)
3. [promotion-rules.md](references/promotion-rules.md)
4. [dreaming-integration.md](references/dreaming-integration.md)
5. [compiled-surfaces.md](references/compiled-surfaces.md)
6. [adapters.md](references/adapters.md)
7. [installation-integration.md](references/installation-integration.md)

For a generic host example:

- [examples/generic-host/README.md](examples/generic-host/README.md)

For package maintenance:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## Scripts

- [check-memory-host.py](scripts/check-memory-host.py)
  checks host manifest wiring, fallback paths, and integration declarations
- [validate-memory-frontmatter.py](scripts/validate-memory-frontmatter.py)
  validates structured memory files
- [review-learning-candidates.py](scripts/review-learning-candidates.py)
  reviews candidate freshness and structure without auto-promoting
- [bootstrap-generic-host.sh](scripts/bootstrap-generic-host.sh)
  creates a minimal generic host skeleton
- [refresh-clawhub-package.sh](scripts/refresh-clawhub-package.sh)
  refreshes the publish-only ClawHub package

Python compatibility:

- Python 3.11+ uses standard-library `tomllib`
- Python 3.9 / 3.10 should install `tomli`

## Package Layout

Runtime package:

- `SKILL.md`
- `README.md`
- `VERSION`
- `references/`
- `assets/`
- `scripts/`
- `examples/generic-host/`

Maintainer-only material:

- `tests/`
- `dev/`
- `releases/`

ClawHub should be published from:

- `publish/clawhub/`

not from the repository root.

## What It Is Not

`memory-governor` is not:

- a second-brain platform
- a Notion / Obsidian sync engine
- a universal sync bus
- an auto-archiving system
- a replacement for Dreaming
- a runtime hook system that forces memory routing automatically

It gives the host a contract. The host still decides how to integrate it.

## Current Version

`0.3.0`

## 中文

**面向 AI agent 的记忆治理内核。已和 OpenClaw 2026.6.x 记忆栈重新对齐边界：Dreaming、Active Memory、Memory Wiki、People Wiki，以及 Skill Workshop / Workboard 时代。**

`memory-governor` 适合已经出现多层记忆、多种写记忆 skill、或者可选 adapter 越来越多的宿主系统。它本来就在解决记忆治理问题：什么值得记、应该进入哪一层、什么时候保持短期、什么时候可以被硬化成长期规则。

OpenClaw 在 2026.4 和 2026.6 两条线上持续补齐 runtime memory stack：Dreaming 负责后台巩固，Active Memory 负责回复前 recall，Memory Wiki 负责把已有记忆编译成 wiki 视图和 provenance 友好的知识层，People Wiki（2026.4.29）负责实体画像和关系图谱，Skill Workshop / Workboard（2026.6.1）负责 skill 生命周期治理和多 agent 协作。所以这次更新不是因为这些能力才开始做 `memory-governor`，而是把已有的治理内核和它们重新对齐边界，避免重复或冲突。

一句话：

- Dreaming 负责后台巩固。
- Active Memory 负责运行时 recall。
- Memory Wiki 负责编译后的 wiki 视图、claims/provenance 和共享搜索面。
- People Wiki 负责实体画像和关系图谱。
- Skill Workshop / Workboard 负责 skill 生命周期和多 agent 协作。
- `memory-governor` 负责捕获规则、target classes、纠错候选层、scope/隐私边界和 hardening 边界。

## 为什么安装

当你的 agent 记忆开始变复杂时，`memory-governor` 会更有价值：

- 多个 skill 都在写 memory-like state
- 明确纠错混进了 daily notes
- 单次观察太快硬化成长期规则
- `self-improving`、`proactivity` 这类可选 adapter 开始带来路由歧义
- 你想在系统变乱之前先建立一套共享 contract

它不是一个“装上立刻替你干活”的生产力 skill。它更像复杂记忆系统的基础设施。

## 它提供什么

- 标准 memory target classes：
  `long_term_memory`、`daily_memory`、`learning_candidates`、`reusable_lessons`、`proactive_state`、`working_buffer`、`project_facts`、`system_rules`、`tool_rules`
- 路由模型：
  `memory type -> target class -> adapter / fallback`
- 低承诺候选层 `learning_candidates`，用于明确纠错和首次出现但尚未证明可复用的经验
- `keep / promote / discard` 的 candidate review 规则
- 清晰的 promotion authority：
  Dreaming 优先处理 `daily_memory -> long_term_memory`，人工 review 处理纠错 hardening 和系统规则升格
- Dreaming 产物边界：
  `DREAMS.md` 和 `memory/.dreams/` 是 engine-owned artifacts，不是标准 target classes
- `memory-governor-host.toml` 宿主 manifest
- host checker、frontmatter validator、candidate reviewer、generic-host bootstrap 等轻量工具
- 不依赖 OpenClaw 固定目录结构的 generic host 示例

## 核心模型

`memory-governor` 把记忆决策拆成三层：

1. **Memory type**
   这条信息是什么？
2. **Target class**
   它应该进入哪个抽象记忆层？
3. **Adapter / fallback**
   当前宿主把这个 target class 落到哪里？

这样治理内核就不会被某个插件、目录结构或宿主实现绑死。

## 和 Dreaming 的边界对齐

`memory-governor` 不是因为 Dreaming 才出现的。它原本就是为复杂宿主做记忆捕获、路由、候选层和 hardening 治理。

Dreaming 出现后，需要重新明确边界：

- `daily_memory -> long_term_memory` 优先交给 Dreaming
- 显式纠错候选层仍由 `learning_candidates` 承接
- `DREAMS.md` 和 `memory/.dreams/` 不应被建模成普通 memory target class

推荐分工：

- Dreaming：
  `daily_memory -> long_term_memory`
- `memory-governor`：
  捕获规则、纠错候选层、adapter 边界、人工 hardening
- 人工 / 显式 review：
  `learning_candidates -> reusable_lessons -> system_rules / tool_rules`

不要把 `DREAMS.md` 或 `memory/.dreams/` 当成普通 memory target class。它们应被视为 Dreaming 的 engine-owned artifacts。

详见 [dreaming-integration.md](references/dreaming-integration.md)。

## 接入状态

`memory-governor` 推荐用三种状态理解：

- `Installed`
  skill 已安装，规则可读
- `Integrated`
  宿主已经显式接入这套 contract
- `Validated`
  host checker 已确认接线状态

安装不会静默修改 `AGENTS.md`、其他 skill 或已有记忆文件。宿主集成应该显式执行。

## 快速开始

推荐阅读顺序：

1. [SKILL.md](SKILL.md)
2. [memory-routing.md](references/memory-routing.md)
3. [promotion-rules.md](references/promotion-rules.md)
4. [dreaming-integration.md](references/dreaming-integration.md)
5. [adapters.md](references/adapters.md)
6. [installation-integration.md](references/installation-integration.md)

Generic host 示例：

- [examples/generic-host/README.md](examples/generic-host/README.md)

维护者测试入口：

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## 它不是什么

`memory-governor` 不是：

- second-brain 平台
- Notion / Obsidian 同步器
- 通用同步总线
- 自动归档系统
- Dreaming 替代品
- 强制执行记忆路由的 runtime hook 系统

它提供的是 contract。宿主仍然需要决定如何接入。
