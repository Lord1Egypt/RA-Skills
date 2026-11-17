# iterate-harness 设计文档 v2.0

> 目标：把 iterate 从 Skill 形态升级为「专门用于 iterate 的极简 agent harness」，深度适配原 skill 的体系与功能。
> 状态：v1 稳定期已实现（当前发布 1.11.0）；**v2.0 设计启动：双模式（iterate 纯审查 / code 通用编程 agent + 防御式内核 + 多 agent 编排）**；设计文档迭代至 v2.0。
> 版本记录：见文末。
>
> **v2.0 设计主线（新增，保留 v1 全部内容不变）**：见 §20。核心变化——① `task_mode`（code / iterate）与 `permission_mode`（default/plan/full_auto）分离；② code 模式 = 通用编程 agent + 防御式内核 + 多 agent 编排；③ iterate 模式 = 1.x 完整保留；④ TUI Tab 直切模式 + 竖向色条 + 底部模式文字。

## 1. 背景与目标

### 1.1 背景
- iterate 目前以 Skill 形态存在（SKILL.md 提示词 + Python iterate_cli 工具链），其运行依赖宿主 IDE 的 agent 读取提示词并执行。
- 用户希望升级为 agent harness：一个独立于宿主 IDE 的运行时，把 iterate 的迭代循环、并行评审、原子修复、验证机制变成可执行的一等公民。

### 1.2 目标
1. 提供可复用的 agent 运行时（会话、工具、编排、配置、安全）。
2. 深度适配 iterate 原 skill 的体系与功能，语义层不重复实现。
3. 极简设计：克制、模块化、插件化。

## 2. 设计原则
- **极简核心**：内核只做 5 件事——会话管理、工具注册、编排循环、配置、安全边界。
- **一切可插拔**：模型、工具、技能、会话、沙箱、存储、循环、调度、UI 均可替换或重组合。
- **可追溯**：append-only 会话日志，模型可见内容必须能从日志重建（硬约束）。
- **厂商中立**：不锁定单一模型供应商。
- **深度适配**：iterate 的业务机制沉淀为「语义层」，与内核解耦，可被不同运行时承载。

## 3. 总体架构（三层）
1. **iterate 业务语义层**：维度规划、并行评审、原子修复、架构修复、决策日志、验证闭环（原 skill 体系，不重写）。
2. **Harness 极简内核**：会话管理 / 工具注册 / 编排循环（焦点）/ 配置 / 安全边界。
3. **运行时承载（可插拔）**：路线 A = dsh 运行时（插件承载）；路线 B = 独立运行时（fork 定制）。

## 4. iterate 机制 → harness 能力映射
| iterate skill 机制 | harness 适配能力 |
|---|---|
| 维度规划（dimensions 配置） | 配置驱动规划器，生成评审任务清单 |
| 并行评审（多维度并行） | 多 subagent 并行编排，聚合评审结论 |
| 原子修复（逐条修复） | 工具边界 + 变更审批（防越界改文件） |
| 架构修复（跨文件重构） | 全局上下文重载 + 跨文件工具 |
| 结果记录（决策日志） | append-only 会话日志，天然可追溯 |
| 验证命令（validate 校验） | 命令执行网关 + 校验器插件 |
| onboarding / 个性化 | 配置初始化向导，写入 harness 配置 |
| ITERATE.md 项目知识库 | 项目记忆投影（随会话自动加载/刷新） |

## 5. 双路线（并行，语义层共享）
### 路线 A：dsh 插件（iterate-dsh-plugin）
- 形态：Cordis 生态内插件（TypeScript），复用 dsh 运行时。
- 复用：subagent / approval / plan / skill 加载 / append-only 日志。
- 职责：iterate 循环映射为 dsh workflow；config 映射为 dsh 配置；validate 映射为工具。
- 优点：零运行时维护、生态复用、快速落地。
- 风险：受 dsh 演进约束；插件是 TS，与 Python 工具链需桥接。

### 路线 B：独立极简 harness（iterate-harness）
- 形态：fork OpenHarness（MIT）定制，Python 同栈。
- 保留：工具调用、记忆、权限、多智能体协调。
- 定制：内置 iterate 迭代循环、维度评审、决策日志、验证网关。
- 优点：完全自主、深度定制、语义层可直连 Python iterate_cli。
- 风险：运行时自维护，启动成本高。

### 对比摘要
| 维度 | 路线 A dsh 插件 | 路线 B 独立 Harness |
|---|---|---|
| 运行时维护 | 零维护 | 自维护 |
| 控制力 | 受 dsh 约束 | 完全自主 |
| 启动成本 | 低 | 高 |
| 生态复用 | 强（dsh-plugin topic） | 独立 |
| 语言栈 | TS + Python 桥 | Python 同栈 |

## 6. 仓库形态（决策：主仓库统一维护 + 独立插件发布仓库）
> v1.7 迭代：独立插件发布仓库（subtree 拆分）作为 npm 发布源，插件独立版本线。

- **主仓库（jingzhao-l/iterate-skill）**：`skill/` 与 `harness/` 同仓库、顶层分开维护，是**唯一维护点**——插件代码的提交、评审、README 变更等全在主仓库完成。
- **独立插件发布仓库（jingzhao-l/iterate-plugin）**：由主仓库 `git subtree split` 拆分 `harness/iterate-plugin/` 推送而成，保留完整提交历史；作为 npm 发布源（`npm publish` 在此执行）、dsh 生态发现入口（打 `dsh-plugin` topic）、并引流至主仓库（README 顶部横幅 + npm `repository` 元数据指向主仓库）。
  - 发布工作区：`/Volumes/Eng-Dev/iterate-skill/.release/iterate-plugin/`（gitignore 目录），`git subtree push` 同步后在此执行发版。
- 同步流程：`git subtree split --prefix=harness/iterate-plugin -b subtree-plugin && git push plugin-origin subtree-plugin:main` → 在 `.release/` 工作区 `git pull` 后执行 `npm publish`。
- **插件独立版本线**：`harness/iterate-plugin/package.json` 自 2.3.7 起独立递增，不再与 skill 版本号强绑定（仅第 9 节路由图的「全项目版本统一」约束对 skill 本体生效）。
- 现有 skill 三平台发布流程（ClawHub / ModelScope / SkillHub）走特定子路径，不受新增 `harness/` 影响。
- **日后的 harness 发布仓库（决策 2026-08-14）**：harness 第一个大版本（v0/1.0）完成后，同样采用「主仓库统一维护 + 独立发布仓库」模式——另开独立仓库作为 harness 的发布源（npm/安装脚本等在此执行），主仓库 `harness/iterate-harness/` 仍是唯一开发与评审点，通过 subtree 拆分持续同步，与 iterate-plugin 仓库模式完全一致。
- 日后需要再平滑升级为 Monorepo（workspace）。
- 备选：方案 A 独立仓库（跨仓共享语义层协调成本高）、方案 C Monorepo（单人维护过度设计）。

## 7. iterate-dsh-plugin 最终实现形态（v0 最小验证版）
```
harness/
└── iterate-plugin/            # dsh 插件（TS）
    ├── package.json           # dsh.bundle 字段指向 patch 文件（分发格式）
    ├── src/
    │   ├── index.ts           # export function apply(ctx)
    │   ├── inject.ts          # export const inject = ['tools','sessions',...]
    │   ├── tools/             # validate / decision-log / config 等工具
    │   ├── skills/iterate.md  # 复用原 SKILL.md
    │   ├── memory/            # ITERATE.md 投影与注入
    │   └── bridge/            # 子进程/JSON-RPC 桥 → 调 Python iterate_cli
    ├── cordis.patch.yml       # 挂载配置（一行 insert 即装上）
    └── README.md
```
运行时循环：规划（读 dimensions）→ 并行评审（subagent ×N）→ 原子修复（工具+审批）→ 验证（validate 桥）→ 决策日志（append-only）→ 回环直至验证通过。
- 插件遵守 dsh 规范：`inject` 声明依赖、`ctx.tools.register(defineTool(...))` 注册工具、`ctx.effect()` 管理可逆副作用、Model-visible means logged。
- v0 范围：自治闭环 workflow（规划 → 并行评审 ×N → 原子修复 → 验证 → 回环 → 达标自停）+ dry-run 纯审查模式 + 5 个核心工具（config / validate / decision-log / context / review）+ 加载 SKILL.md + ITERATE.md 注入，验证语义层迁移与 Python 桥接成本。

### 7.1 dry-run 模式（纯审查模式）
- **定位**：只评审、只出报告，**绝不修改任何文件**。是 iterate 的「只读体检」模式，也是普通 skill 完全做不到的效果。
- **触发**：工具调用 `iterate review --dry-run`，或 workflow 参数 `mode: "dry-run"`（区别于 `mode: "normal"`）。
- **行为**：
  1. **规划**：读取 dimensions + goal，生成评审任务清单（同正常模式）。
  2. **并行评审**：N 个 subagent 并行，返回各维度 findings。
  3. **聚合**：去重、过滤 `known_intentional`、按 severity 排序（同正常模式 Phase 1）。
  4. **多轮收敛**：可配 `review.max_reviews`，**反复多轮审查**直至发现数收敛（较上一轮不再下降）或达到上限——"纯粹反复审查"。
  5. **产出**：评审报告（各维度 findings + 每轮收敛统计 + 建议修复优先级）+ append-only 决策日志。**不创建分支、不建 worktree、不写任何项目文件**。
- **与正常模式差异**：跳过 Phase 2/3（原子/架构修复）、跳过 git 隔离与 merge/push；只保留 Phase 0/1/4（规划/评审/记录）。
- **确定性实现**：多轮收敛的去重 / 已知意图过滤 / severity 排序 / 收敛统计全部落在纯函数引擎 `src/review.ts`（可单测）；`iterate_review` 工具提供 `plan`（评审计划）与 `aggregate`（确定性聚合）两个操作；workflow 按注入的 canonical 模板复现循环——每轮把已发现 findings 喂回评审者"只找新问题"，某轮新增 0 条即收敛自停。
- **用途**：CI 预检、发布前基线评估、改动前摸底、教学演示、成本可控的多维深度审查。
- **价值**：正常模式是"评审即修复"，dry-run 是"评审即诊断"——先彻底看清问题、形成可审计的报告，再由人或后续轮次决定是否动手。

## 8. 能力边界：skill 无法实现 vs harness 可实现
| 能力维度 | 原 skill | iterate-harness |
|---|---|---|
| 自主多轮迭代 | 依赖宿主手动触发 | agent-loop 原生循环，跑到达标自动停 |
| dry-run 纯审查 | 无（skill 无纯审查模式） | 只评审不改文件，多轮收敛出报告，可 CI 预检 |
| 真·并行评审 | 仅建议并行 | subagent 原生并行 ×N + 聚合 |
| 审批 / 安全边界 | 靠提示词自觉 | 原生 approval + 工具权限边界，可强制执行 |
| 可追溯性 | 项目内文件，靠自觉写 | append-only 日志硬约束，可回放/恢复/fork |
| 可插拔 | 绑定宿主模型 | 模型/工具/存储/沙箱全可替换，可 A/B |
| 跨会话记忆 | 每次重新 onboarding | 会话持久化 + ITERATE.md 自动注入 |
| 运行环境 | 必须跑在宿主 IDE | 独立 CLI / headless / CI 可跑、可批量 |

诚实边界：harness 不改变模型智力，只改变执行环境；插件 TS 与 Python 工具链存在桥接成本；skill 的零安装、宿主天然支持优势被 harness 丢掉。

## 9. 落地路线图
1. **先做最小 dsh 验证插件**（路线 A v0）：验证语义层迁移 + Python 桥成本。
2. 验证通过后，评估路线 B 独立 harness 是否投入（复用验证过的语义层）。
3. 按需发布插件到 dsh-plugin 生态（加 topic + bundle 分发）。
4. 版本号全项目统一（遵循既有硬约束；例外：`harness/iterate-plugin` 走独立版本线，见 §6）。

## 10. 风险与开放问题
- 桥接性能与稳定性：子进程 / JSON-RPC 的调用开销。
- dsh 演进依赖：新版本是否破坏插件 API。
- 语义层最终落 Python 还是 TS：影响路线 B 是否与插件共享代码。
- SKILL.md 内容是否需为 harness 形态改写（上下文压缩、记忆注入方式）。

## 11. 独立 harness 设计（路线 B 具体化）

> 基于路线 A（dsh 插件）v0 验证通过的前提，独立 harness 的形态与方案现已明确：
> fork OpenHarness（Python 栈），深度定制为「专用于 iterate 的 agent harness」。
> 本章为 v1.5 新增，完整保留前文（v1.0–v1.4）内容。

### 11.1 技术栈决策（OpenHarness = Python 栈）

经调研确认，OpenHarness（HKUDS，MIT）为 **Python 栈**：

| 项目 | 事实 |
|---|---|
| 语言 | Python 3.10+（uv 包管理器） |
| 规模 | 11,733 行 / 163 文件（44× 轻于 Claude Code） |
| 工具 | 43 个（文件 / Shell / 搜索 / Web / MCP） |
| 技能 | 完全兼容 `anthropics/skills` 与 `claude-code/plugins` |
| 测试 | 114 单测 + 6 端到端 |
| 内置能力 | streaming tool-call loop、API 重试退避、并行工具执行、token 计数与成本追踪、CLAUDE.md 注入、上下文压缩、MEMORY.md、会话恢复、多级权限、PreToolUse/PostToolUse hooks、交互审批、subagent 生成与后台任务生命周期 |
| UI | React TUI + Ink TUI 双形态 |
| 命令 | `oh`（交互）/ `oh -p`（一次性）/ `--output-format json` / `--dry-run` 静态预览 |
| 厂商 | Anthropic 兼容 / OpenAI 兼容 / Claude 订阅 / Codex 订阅 / Moonshot / GLM / MiniMax / Ollama 等 workflow |

**结论**：独立 harness 采用 **Python 同栈**，与既有 `iterate_cli`（Python）工具链同栈，语义层移植成本最低；这也回答了 v1.0 §10 开放问题「语义层最终落 Python 还是 TS」——**独立 harness 走 Python，与插件（TS）共享的是语义约定而非代码**。

### 11.2 能力差距分析（用户视角：skill / 插件实现不了 vs 独立 harness 可实现）

以用户实际使用体验为视角，逐项对比「原 skill → dsh 插件 → 独立 harness」三层能实现什么：

| 能力效果 | 原 skill（提示词+Python CLI） | dsh 插件（路线 A） | 独立 harness（路线 B） |
|---|---|---|---|
| **不依赖宿主运行** | ❌ 必须跑在宿主 IDE agent 里 | ❌ 必须跑在 dsh 运行时 + 聊天会话里 | ✅ `oh -p "..."` 一次性 / headless / CI / 批量 |
| **agent loop 是内核级** | ❌ 靠宿主模型自觉循环 | ⚠️ 靠 dsh `workflow` 脚本模拟 | ✅ 内核原生 streaming tool-call cycle + retry + 并行执行 |
| **token / 成本透明** | ❌ 完全不可见 | ❌ 插件无成本层（受 dsh 约束） | ✅ 内核 token counting & cost tracking 开箱即得（呼应此前 P0 建议） |
| **审批强制执行** | ❌ 只能提示词引导 | ⚠️ 依赖 dsh approval | ✅ 内核 PreToolUse/PostToolUse hooks + 多级权限 + 交互审批弹窗，强制生效 |
| **dry-run 静态预览** | ❌ 无 | ⚠️ 有审查型 dry-run（不写文件） | ✅ 审查型 dry-run **且** 内核 `--dry-run` 静态预览（settings/auth/skills/commands/tools） |
| **跨会话恢复** | ❌ 每次重新 onboarding | ❌ 无状态 | ✅ session resume & history，`--session` 续跑（呼应此前 P1 resume 建议） |
| **持久记忆** | ❌ ITERATE.md 仅靠自觉读 | ⚠️ context 工具读文件 | ✅ MEMORY.md 持久化 + 上下文自动压缩，跨天长会话 |
| **真·并行评审** | ⚠️ 仅建议 | ✅ 但受 dsh 编排约束 | ✅ 内核并行工具 + subagent 生命周期管理，可后台任务 |
| **多智能体协调** | ❌ | ⚠️ workflow 模拟 | ✅ team registry / 任务管理 / 后台任务生命周期（native swarm） |
| **厂商中立** | ❌ 绑定宿主模型 | ⚠️ 受 dsh 接入 | ✅ 多 provider workflow，环境变量切换，本地 Ollama 亦可 |
| **reasoning 模型** | ❌ | ⚠️ 受 dsh 支持 | ✅ Kimi 等 reasoning_content 原生 |
| **技能生态复用** | ❌ | ⚠️ 需加载 SKILL.md | ✅ iterate SKILL.md 可直接挂载为 skill（anthropics 兼容） |
| **独立分发** | ✅ skill 文件 | ⚠️ 依赖 dsh 插件体系 | ✅ pip / install.sh 独立安装，可作独立产品 |

**独立 harness 独有、skill 与插件都无法实现的核心效果（用户视角）**：

1. **「离开 IDE 也能自治迭代」**：在 CI 流水线 / 命令行 / 批量任务里跑 iterate 闭环，无人值守到收敛自停，产出可审计报告。
2. **「每一次动作都强制受控」**：写文件 / 跑命令不再是模型自觉，而是被 harness 内核的权限 hooks 强制拦截并弹窗确认——从「靠自觉」到「靠强制」。
3. **「看得见的成本」**：每轮评审 / 修复消耗多少 token、多少钱实时可查，`/cost` 一目了然，让「反复多轮审查」的成本可控、可预算。
4. **「中断可恢复」**：长迭代中断后 `--session` 从上次断点续跑，不再推倒重来。
5. **「一份 SKILL.md 通吃所有宿主」**：skill 生态复用意味着 iterate 的提示词可作为标准 skill 被任意兼容 harness 加载。

**诚实边界（继承 v1.0 §8）**：harness 不改变模型智力；skill 的零安装、宿主天然支持优势被 harness 丢掉；独立运行时需自维护。

#### 11.2.1 用户体验场景深析（v1.8：站在用户面前的具体交互，非内核能力清单）

> §11.2 的表是"内核能力"视角；本节补齐"用户能看到什么、点什么、玩到什么"视角，只列 skill 与插件**原理上做不出**的体验，按「看 / 摸 / 跑 / 沉淀」四类分。
>
> ⚠️ **v1.32 修正**：本节多处「插件被 dsh 卡片样式锁死 / 插件无法自绘组件」的表述是**错误结论**——dsh 官方定位 UI 本身也是插件，社区已有大量换肤 / 背景 / 动画插件（详见 §14）。本节「看得见的 UI」相关独占体验的归类已按修正重估，见 §14.3。

**一、看得见的 UI**（skill 只能吐 markdown，插件被 dsh 卡片样式锁死）

| 独占体验 | 长什么样 | 为什么前两层做不到 |
|---|---|---|
| 实时收敛仪表盘 | 审查进行中：TUI 显示 `Round 2/3`、新发现数 sparkline `▇▅▂▁`、五维度各自 spinner + findings 计数、token/费用累计条 | skill 等全部跑完才有文字报告；dsh 卡片是静态文本，插件无法自绘组件 |
| 细粒度 diff 审批 | 修复前弹 unified diff，↑↓ 滚动、**逐 hunk 空格标记接受/拒绝**、Enter 提交 | 插件走 dsh 通用审批（整文件粒度）；skill 是模型直接改文件 |
| findings 分诊界面 | 审查完逐条过：`y 修复 / n 跳过 / a 永久忽略`——按 `a` 的自动写回 `iterate.config.yaml` 的 known_intentional | skill/插件无交互入口；"个性化配置"从手写 yaml 变成交互产生的数据 |
| init 检测式向导 | 自动识别项目语言/测试框架 → 空格勾选推荐维度 → 预览生成的 yaml → Enter 写入 | skill 的 wizard 是纯文本问答；插件没做 init |

**二、摸得着的中途干预**（不是"等它跑完"）

- Esc 暂停菜单：迭代中途暂停，弹"跳过当前 finding / 收窄维度 / 直接停"，选完继续——skill 无进程概念，插件 workflow 发起后不可中途改道。
- 断点续跑画面：`resume` 恢复时 TUI 先显示上次快照（跑到第几轮、还剩哪些 finding），确认后续跑。

**三、离开 IDE 才能跑的场景**（无人值守，存在性缺口）

- PR 自动审查：`review --dry-run --format pr-comment`，CI 里直接评论到 PR，exit code 当质量门禁（findings 超阈值即红）。
- git hook：commit 前 30 秒 changed-only 快审。
- 批量/定时：一条命令审 10 个仓库出排行；cron 每天跑，只报新增问题。

**四、数据沉淀**（从"一次性报告"到"趋势"）

- 跨 run 趋势：finding 指纹（file+line+dimension 哈希）存本地库，`log --trend` 显示"上周 12 → 本周 5"，区分**新增 / 已修复 / 顽固未动**——skill 的决策日志是纯文本，查不了。
- HTML 单文件报告：收敛曲线、severity 分布、内嵌 diff，可直接发给别人看。
- 评审回放：`log --replay` 按时间序回放每轮决策，像看录像。

**v0 取舍建议**：① findings 分诊界面（把个性化闭环做成交互）② diff 审批 + Esc 干预（把"强制受控"做成体验）③ PR/CI 模式（打开无人值守场景）优先；实时仪表盘与趋势库 v1；HTML 报告最低。

#### 11.2.2 代码实况深析（v1.9：基于 iterate_cli 六模块 + SKILL.md + 配置层的源码证据）

> 本节结论全部来自源码阅读（iterate_cli/{cli,fingerprint,scan,generator,refresh,personalize,wizard,tui}.py、SKILL.md、config/、scripts/、templates/、examples/），是 §11.2 内核能力与 §11.2.1 UX 场景的代码级证据与细化。

**一、关键事实：iterate_cli 是 100% 确定性本地计算，零 LLM 依赖**

六个模块（fingerprint / scan / generator / refresh / personalize / cli 非向导部分）全部为纯本地确定性计算 + 终端表单采集；模型依赖全部在 SKILL.md 驱动的宿主 agent 侧。这意味着 **onboarding 全链路可直接作为 harness 的数据层复用**，无需重写。

现成数据资产清单：

| 资产 | 内容 | 当前形态 | 位置 |
|---|---|---|---|
| 指纹库 | 15 类 manifest 的 SHA-256（仅项目根，不递归） | config 字段 | `iterate.config.yaml` `onboarding.fingerprints` |
| DriftResult | unchanged/changed/added/removed 四元组 | 内存，不持久化 | fingerprint.py `compare_fingerprints` |
| ScanResult | manifests/languages/dirs + 6 个 has_* 特性位 | 内存，渲染进 ITERATE.md | scan.py `scan_project` |
| suggest_* 三函数 | 维度/验证命令/白名单启发式建议 | 内存，仅向导内一次性出现 | scan.py |
| PersonalizationData | 9 类个性化数据（结构化 7 类 + 自由文本 2 类） | config + ITERATE.md 用户区 | personalize.py |
| KNOWN_SAFE_COMMAND_PREFIXES | 命令前缀白名单 + FORBIDDEN_COMMAND_CHARS 禁字符 | 源码常量 | personalize.py |
| 分区标记契约 | AI-MAINTAINED / USER-OWNED 刷新边界 | ITERATE.md 注释 | generator.py |

**二、prompt 约定 → 机制强制：全景对照（skill 现状 vs 插件已强制 vs harness 待强制）**

- **插件已强制（10 项，确定性计算类）**：findings schema、severity 排序、跨轮去重、known_intentional 过滤、收敛判定、meta-review 六项审计（仅 dry-run）、review plan、配置合并、验证命令精确匹配、决策日志 append-only。
- **仍是 prompt 约定、harness 内核可强制（20 项），分两类**：
  - **副作用约束类（PreToolUse/PostToolUse hooks + 权限层）**：protected_paths 写拦截、risk_areas 强制审批、forbidden_fixes diff 正则匹配拒绝、敏感文件读拦截（.env/*.key）、验证失败自动回滚（限 iterate/* 分支）、逐 hunk 修复 + 文件锁串行。
  - **状态继承类（session + 持久化）**：is_atomic 实测校验（fixer 后 `git diff --stat` 超阈值自动降级 architectural）、每组 trim≤20 确定性截断、文件碰撞 defer 用 Set 交集计算、fix_priority_order 确定性重排、deferredArchitectural 跨会话继承（decision-log + resume）、正常模式复用 meta-review 审计计数一致性。

**三、维度配置体系在 harness 的解锁项**（当前维度 yaml 仅 name/priority/focus 文本，focus 里的"阈值"是自然语言不可消费）

- per-dimension `model`/`concurrency`/`token_budget`（security 用强模型、style-tests 用快模型）
- 维度级阈值门禁：`max_critical`/`max_high` → 阻止 merge / CI 红（对接 §11.2.1 PR 门禁）
- 维度特定验证命令：style-tests 修完跑 lint、security 修完跑 bandit
- priority 驱动修复调度（与 fix_priority_order 合并）；维度趋势追踪；changed-only 的维度级细化（后续轮只重跑有改动维度的模块）

**四、用户旅程断点（源码级证据，harness 可修复）**

- 安装：无 bootstrap、无版本过期比对（A1-A3）
- onboarding：**"TUI"实为 rich 着色的 input() 问答**——无方向键/空格/回车组件，维度多选靠手敲 `"1,2,5,7"`（wizard.py `_parse_dimension_selection`）；向导不问 goal/max_rounds/atomic/language（generator.py 硬编码 DEFAULT_GOAL/7/20/en，与 examples/ 展示落差）；验证命令建议按语言硬编码不读真实 manifest scripts、且无 dry-run 预检（B1-B8）
- 日常：drift 检测只在 `iterate status` 被动触发；known_intentional 添加后无法即时验证是否命中；`.bak-<timestamp>` 平铺备份难查询（C1-C5）

**五、顺带发现的现有代码问题（待修复清单，非 harness 范畴）**

1. `tui.py question()` 签名 `-> str` 实际返回 None；`prompt_prefix` 的 rich 标记可能泄露进 input() 提示文本。
2. `examples/typescript-project.md` "验证通过后合并推送" 与默认 `auto_merge=false` 矛盾（Python/Swift 示例已修正，TS 未同步）。
3. `templates/iterate-decisions.template.md` 用 `{goal}` 单花括号占位，但仓库无对应渲染代码——模板与生成器脱节，实际由 AI 会话自行处理。
4. `__main__.py` 与 `cli.py` 双 `if __name__` 守卫冗余。

### 11.3 fork 定制点（OpenHarness → iterate-harness）

在 OpenHarness 之上定制以下内容，其余内核能力（loop / 权限 / 记忆 / 多智能体 / TUI / 厂商 workflow）直接复用：

| 定制面 | 做什么 |
|---|---|
| 语义层移植 | 将插件 TS 语义层（review / meta-review / config-loader 逻辑）移植为 Python 模块，或直接复用 `iterate_cli` 现有 Python 逻辑（validation.commands 精确匹配、known_intentional 过滤、去重 / 排序 / 收敛统计、6 项 meta-review 检查） |
| 内置 iterate 命令 | `iterate-harness review --dry-run` / `iterate-harness iterate` / `iterate-harness resume` / `iterate-harness init` / `iterate-harness log`（或作为 `oh` 的子命令） |
| iterate 配置 | 加载 `iterate.config.yaml`（Master+Overrides 合并逻辑移植），权限规则映射到内核 permission 配置 |
| 决策日志 | append-only `decision-log.jsonl` 作为内核会话日志之外的业务日志，随会话可回放 |
| 技能挂载 | 将项目 SKILL.md 以 anthropics 兼容 skill 形式内置，harness 启动自动注入 |
| 项目记忆 | `ITERATE.md` 投影为 CLAUDE.md 等价物（OpenHarness 已原生支持 CLAUDE.md 注入），语义与插件 context 工具一致 |
| TUI 体验 | 复用 OpenHarness TUI；按用户偏好打磨键盘导航（↑↓ 移动、空格选择、Enter 确认）的 approve / dimension 选择界面 |

#### 11.3.1 真实仓库结构核验（v1.11：以 GitHub 实际目录树为依据）

> 初稿结构拉取自 GitHub `HKUDS/OpenHarness` main 分支（commit `9b2efd7`，2026-06-04）；随后已完整克隆源码至主仓库 `.external/OpenHarness/`（gitignored，`--depth 1` + tags，检出 **v0.1.9 稳定 tag** `a0f8552`，2026-05-07）并完成四路并行源码深析（内核引擎 / 扩展面 / 状态配置 / 编排与 UI），深析结论见 §11.3.2。本节结构与本地克隆一致。

```
OpenHarness/
├── pyproject.toml / README.md / README.zh-CN.md / CHANGELOG.md / LICENSE(MIT)
├── src/openharness/           # 主包（扁平子包结构，无 kernel/ 聚合层）
│   ├── cli.py / __main__.py   # `oh` CLI 入口
│   ├── engine/                # query_engine.py（agent loop 核心）/ cost_tracker.py / messages.py / stream_events.py
│   ├── api/                   # provider.py / registry.py / client / openai_client / codex_client / copilot_client / usage.py（厂商中立层）
│   ├── auth/                  # 认证管理
│   ├── permissions/           # checker.py / modes.py（多级权限）
│   ├── hooks/                 # events / executor / loader / schemas——4 类 hook：command | prompt | http | agent，均带 matcher / timeout / block_on_failure / priority
│   ├── commands/              # registry.py（slash 命令注册表）
│   ├── skills/                # loader / registry / types / _frontmatter / bundled/content（anthropics 兼容技能加载）
│   ├── prompts/               # claudemd.py（CLAUDE.md 原生注入）/ system_prompt.py / context.py / environment.py
│   ├── memory/                # manager / agent / memdir / relevance / scan / search / team / usage / schema / migrate
│   ├── services/              # session_backend / session_storage / compact/（上下文压缩）/ cron_scheduler / token_estimation / lsp / memory_extract
│   ├── state/                 # app_state / store
│   ├── swarm/                 # in_process / subprocess_backend / mailbox / registry / team_lifecycle / worktree / permission_sync / lockfile（多智能体）
│   ├── tasks/                 # manager / local_agent_task / local_shell_task / types
│   ├── coordinator/           # agent_definitions / coordinator_mode
│   ├── tools/                 # 44 个内置工具：bash / file_read / file_write / file_edit / grep / glob / agent / team_* / task_* / todo_write / skill / cron_* / web_* / mcp_* / ask_user_question / enter_worktree / exit_worktree / lsp …
│   ├── ui/                    # react_launcher（对接 frontend/terminal React+Ink）/ textual_app / permission_dialog / input / output / protocol / runtime
│   ├── plugins/               # loader / installer / schemas / bundled（OpenHarness 自身插件系统）
│   ├── personalization/       # extractor / rules / session_hook（OpenHarness 已有个性化框架）
│   ├── sandbox/               # docker_backend / path_validator / session / adapter（Docker 沙箱）
│   └── mcp/ bridge/ channels/ keybindings/ themes/ vim/ voice/ output_styles/ autopilot/ utils/ platforms.py
├── frontend/terminal/         # React + Ink TUI 源码
├── autopilot-dashboard/       # React 自动驾驶看板
├── ohmo/                      # 独立子项目（fork 后可裁剪）
└── docs/ scripts/ tests/ assets/ .claude/skills/ .agents/
```

**对设计有直接影响的核验结论**：

1. **结构形态**：真实结构是「扁平子包 + 注册机制」，不存在 v1.10 §11.4 草案假设的 `kernel/` 聚合层与 `providers.py`/`agent_loop.py` 等文件名——fork 策略必须改为「保留 `openharness/` 包原样 + 新增 `iterate/` 子包 + 注册点挂载」，详见 §11.4.1。
2. **意外收获的现成能力**（草案未预料、直接复用）：
   - `swarm/worktree.py` + `tools/enter_worktree_tool.py`：**git worktree 隔离是内核原生的**——iterate 修复轮的 git 隔离方案可直接复用，无需自建；
   - `tools/cron_*` + `services/cron_scheduler.py`：定时审查（§11.2.1「cron 每天跑」场景）开箱即得；
   - `tools/ask_user_question_tool.py`：findings 分诊界面的交互原语已存在；
   - `hooks/` 4 类 hook（command/prompt/http/agent）+ matcher 工具过滤 + block_on_failure：§11.2.2 的 20 项「prompt 约定→机制强制」有了直接载体——副作用约束类用 command hook（确定性），状态继承类用 agent/prompt hook（模型校验）；
   - `personalization/`：上游已有个性化框架，iterate 个性化数据可对接而非另起炉灶；
   - `sandbox/`：验证命令可选 Docker 隔离执行；
   - `services/compact/`：长迭代多轮的上下文压缩原生支持。
3. **hook 机制细节**（来自 `hooks/schemas.py`）：`CommandHookDefinition`（shell 命令、默认 30s、可 block）/ `PromptHookDefinition`（模型校验、默认 block）/ `HttpHookDefinition` / `AgentHookDefinition`（深度模型校验、60s、block），matcher 可按工具名过滤（file_write / file_edit / bash）——iterate 的 protected_paths 写拦截、forbidden_fixes diff 正则拒绝等均可用 command hook 零内核改动实现。
4. **命令机制**：`commands/registry.py` 为 slash 命令注册表（`/xxx` 形态），CLI 子命令在 `cli.py`——iterate 命令双形态挂载（slash `/iterate` + CLI `iterate-harness` 子命令）。

#### 11.3.2 源码级深析（v1.11：基于 v0.1.9 本地克隆的四路并行探索，全部带 file:line 证据）

> 源码位置：`.external/OpenHarness/`（v0.1.9, `a0f8552`）。以下每条结论均可回溯到源码行号，是 §11.4.1 修订版架构的直接依据。

**一、关键纠偏：v1.10 草案中与源码不符的假设（12 项）**

| # | 草案假设 | 源码事实（file:line） | 对设计的影响 |
|---|---|---|---|
| 1 | agent loop 在 `QueryEngine` 类内 | 真循环是模块级函数 `run_query`（`engine/query.py:632`），单 `while` 循环在 `query.py:699`；`QueryEngine.submit_message` 只是薄包装（`engine/query_engine.py:147-190`） | 轮次控制必须 fork `run_query`，不是改类 |
| 2 | hook 可承载评审轮次控制 | `HookEvent` 共 10 个事件（`hooks/events.py:8-19`），无 PRE_TURN/POST_TURN；`STOP` 仅在模型不再调工具、循环将结束时触发一次（`query.py:806-815`）；hook 只能 block 单个工具、不能改 messages/控制流（`hooks/executor.py:64`） | 收敛判定/轮次注入只能改 loop 本体；hook 仅用于副作用约束类强制 |
| 3 | 可走「内置插件」形态 | `plugins/bundled/__init__.py` 是空文件且 `load_plugins()` 不扫描它（`plugins/loader.py:107-123` 只扫用户/项目目录）；插件无 apply/inject 编程式 API，纯声明式 manifest（`plugins/schemas.py:8-24`）；插件不能直接注入系统提示 | 否决插件路线，采用「独立子包 + 直接注册」（§11.4.1） |
| 4 | TUI 有 React / Textual 双形态可选 | Textual 实现存在但**未接线**：全仓无任何模块 import `textual_app`；`run_repl` 只走 `launch_react_tui`（`ui/app.py:57-86`） | TUI 定制唯一路径 = React 前端 + NDJSON 协议扩展 |
| 5 | CLI 有 `--session` 参数 | 不存在；恢复用 `--continue`（最近会话）/ `--resume [ID]`（指定会话，`cli.py:2110-2123`），恢复经 `run_repl(restore_messages=..., restore_tool_metadata=...)`（`cli.py:2397-2411`） | §11.5 命令集对应修正 |
| 6 | cost tracking 含金额 | `CostTracker` 只累加 token（`engine/cost_tracker.py:8-24`），`UsageSnapshot` 仅 input/output_tokens（`api/usage.py:8-16`），无金额换算 | 「看得见的成本」金额层需 fork 自建（token×价格表） |
| 7 | worktree 隔离一套实现 | **两套独立实现不共享代码**：`swarm/worktree.py`（`~/.openharness/worktrees/<slug>`，含 node_modules/.venv 软链复用，`worktree.py:105-117,144`）与 `tools/enter_worktree_tool.py`（`repo/.openharness/worktrees/`，同步 subprocess，`enter_worktree_tool.py:42-53,79-80`） | iterate 修复轮选 `WorktreeManager`（有软链复用与 stale 清理） |
| 8 | bash 白名单可用权限规则表达 | 只有 `denied_commands`（deny 语义，`permissions/checker.py:120-126`）；无 `allowed_commands` 字段（全仓 grep 0 命中） | 白名单两条路：PreToolUse command hook（零内核改动）或 fork 加字段（推荐后者，见 §11.4.1） |
| 9 | path_rules 可做 protected_paths 禁写 | `path_rules` 仅 deny 生效、不区分读写（`checker.py:109-117` 无 is_read_only 分支）；且仅当工具输入含 `file_path/path` 字段才被抽取（`query.py:916`） | 「禁写不禁读」需 fork 在 `evaluate` 加读写分支 |
| 10 | 长迭代上下文无忧 | compact 四级渐进（microcompact→collapse→session memory→LLM full compact），microcompact 把早期 read_file/bash/grep 等结果**不可逆清空**（`services/compact/__init__.py:52,808-856`），`COMPACTABLE_TOOLS` 硬编码、无「不可压缩」标记 | iterate 多轮评审的 findings/diff 关键产物必须走 attachment 通道保留（`compact/__init__.py:714-733` 已有先例） |
| 11 | bundled skill 支持目录布局 | `get_bundled_skills()` 只 glob `*.md` 不递归（`skills/bundled/__init__.py:23`）；用户级才是 `<dir>/SKILL.md` 布局（`skills/loader.py:70-85`） | iterate SKILL.md 以单文件 `skills/bundled/content/iterate.md` 落地，自动成为 `/iterate` 命令（`commands/registry.py:2160`） |
| 12 | 复用上游 personalization 框架 | 上游是 10 类正则扁平 fact（confidence 固定 0.7，`personalization/extractor.py:11-75`），与 iterate 9 类结构化 PersonalizationData 模型不兼容；存储不按项目隔离（`rules.py:9`） | iterate 个性化独立子系统，仅复用注入入口模式（`prompts/context.py:123-125` 先例） |

**二、直接可用的挂载点清单（全部现成入口，fork 改动集中且小）**

| 挂载面 | 源码入口 | 用法 |
|---|---|---|
| 轮间控制点 | `engine/query.py:868`（tool results 回喂后、下一轮 while 前） | 插 iterate 控制块：收敛判定/轮次注入/break；经 `QueryContext`（dataclass，`query.py:137-154`）扩展 `iterate_policy` 传策略，上层 `QueryEngine` 与消费者零改动 |
| slash 命令 | `create_default_command_registry()`（`commands/registry.py:2106-2266`） | `registry.register(SlashCommand("iterate", ...))`；handler 放独立模块 `commands/iterate.py`（registry.py 已 2300+ 行） |
| 自定义工具 | `BaseTool`（`tools/base.py:35-57`：`name/description/input_model` + `async execute(arguments, context) -> ToolResult`）+ `create_default_tool_registry()`（`tools/__init__.py:47-96`） | 5 个 iterate 工具按此契约实现并追加注册 |
| 内置技能 | `skills/bundled/content/iterate.md`（frontmatter 仅 `description` 功能必填，`skills/_frontmatter.py:34-82`） | 放入即被扫描，自动注册为 `/iterate` + `skill(name="iterate")` 双入口 |
| ITERATE.md 注入 | 最小改法 1 行：`prompts/claudemd.py:15-17` candidate 元组加 `ITERATE.md`（复用向上遍历+截断+去重）；独立段落改法：`prompts/context.py:119` 后加一段 | 推荐 claudemd.py 一行改法（零新代码）；系统提示组装唯一汇聚点在 `prompts/context.py:77` |
| 配置节 | `Settings`（pydantic，`config/settings.py:496-534`）加 `IterateSettings` 字段 | model_validate/dump 自动往返，`load/save_settings` 零改动 |
| CLI 子命令 | `cli.py:765-777` 已有 `mcp/plugin/auth/provider/cron/autopilot` 子命令组先例 | 新增 `iterate` 子命令组（review/iterate/resume/log），console script 复用 `oh`/`openharness`（`pyproject.toml:48-52`） |
| 厂商接入 | `PROVIDERS` 元组加 `ProviderSpec` 即完成（`api/registry.py:55-368`，文件头注释明示三步流程）；**DeepSeek 已内置**（`registry.py:171-183`，`DEEPSEEK_API_KEY` + `api.deepseek.com/v1`） | 厂商中立零成本兑现，含重试退避（`api/client.py:32-114`：3 次指数退避+抖动+Retry-After） |

**三、并行评审 ×N 的正确姿势（源码契约）**

- `AgentTool` **强制 subprocess backend**（`tools/agent_tool.py:62-66`，注释说明 in_process 的 asyncio 内部 ID 无法被 task 工具查询）；单次 execute 只 spawn 一个 agent（`agent_tool.py:82`），**没有批量 spawn API**。
- 并行的正确方式 = 模型同一回合发起 N 次并行 `agent` 工具调用——多工具并发由内核 `asyncio.gather` 承载（`engine/query.py:830-844`，`return_exceptions=True` 防兄弟协程被取消）。
- 结果回收复用 coordinator 契约：`ui/coordinator_drain.py` 轮询 `BackgroundTaskManager`，完成批以 `<task-notification>` 包络作为后续 user turn 回灌（`coordinator_drain.py:89-197`）；coordinator 系统提示本身示范并行 spawn（`coordinator/coordinator_mode.py:496-497`）。
- **iterate 评审编排完全复用该契约**：N 个维度评审 = N 个后台 agent task（`tasks/manager.py:114` `create_agent_task`），每任务独立 worktree（`swarm/worktree.py:150` `create_worktree(repo_path, slug, branch, agent_id)`，含软链复用与 `cleanup_stale`），聚合由确定性引擎消费 task 输出。

**四、fork 裁剪清单（以 import 证据为准）**

| 子包 | 外部引用 | 处置 |
|---|---|---|
| `vim/` | 零外部 import（孤立死代码） | **删除** |
| `channels/` | 零外部引用（vendored 自 nanobot，`channels/UPSTREAM`） | **删除**（连带 ohmo 的 2 处 lazy import 消失） |
| `ohmo/`（子项目） | 仅 channels 内 2 处 lazy import | **删除**（可选依赖） |
| `autopilot/` | `cli.py` ×10 + `commands/registry.py:17` | 保留（接线中；autopilot-dashboard/ 目录一并保留或裁剪 UI） |
| `voice/` | `commands/registry.py:1618` | 保留（删需同步删命令，收益低） |
| `bridge/` | UI 三件套 + commands 活跃使用 | 保留 |
| `frontend/terminal/` | React TUI 唯一 UI | **必留**（注意：本克隆浅层无 node_modules，首启会自动 `npm install`，`react_launcher.py:133-142`） |

**五、其它源码事实（备查）**

- 会话存储是 **JSON 非 JSONL**：`~/.openharness/data/sessions/{name}-{sha1(cwd)[:12]}/` 下 `latest.json` + `session-{sid}.json` 双写（`services/session_storage.py:54-107`）；decision-log 仍按 iterate 自己的 append-only jsonl 独立存在。
- 权限三模式 `default/plan/full_auto`（`permissions/modes.py:8-13`，无 acceptEdits）；`--dangerously-skip-permissions` ≡ full_auto（`cli.py:2304-2305`）。
- 权限判定顺序：内置敏感路径硬保护（不可覆盖，`checker.py:88-98`）→ denied_tools → allowed_tools → path_rules(deny) → denied_commands → full_auto → 只读放行 → plan 拒绝 → default 弹窗确认（`checker.py:75-156`）；**PreToolUse hook 先于权限层执行**（`query.py:880-890`）。
- PreToolUse block 的语义 = 返回 `is_error=True` 的 ToolResultBlock 给模型（可调整重试），非中断会话（`query.py:886-891`）。
- cron：标准 5 字段（croniter），注册表 JSON + 历史 jsonl + fork 守护进程（`services/cron.py:12-116`、`cron_scheduler.py:261-358`，`oh cron start`）；job 经沙箱执行、300s 超时——定时审查场景零成本。
- 沙箱：`srt` CLI 包裹或 Docker backend（`sandbox/adapter.py:52-131`、`utils/shell.py:51-97`）；Windows 原生不支持。
- auto-compact 阈值默认 ≈167k token（200k 窗口，`compact/__init__.py:1056-1088`），连续失败 3 次熔断。
- MEMORY.md 体系按 cwd 哈希存于 `~/.openharness/data/memory/`（`memory/paths.py:11-22`），不在项目内。

### 11.4 架构与模块划分

> ⚠️ v1.11 注：以下目录树为 v1.10 基于能力清单的**草案假设**（虚构的 `kernel/` 聚合层与文件名），保留存档；**修订版架构见 §11.4.1**（以 §11.3.1 真实结构为依据），落地实现以 §11.4.1 为准。

```
harness/
└── iterate-harness/             # fork 自 OpenHarness 的独立运行时（Python）
    ├── pyproject.toml           # 精确版本依赖，MIT
    ├── src/
    │   ├── main.py              # oh / iterate-harness CLI 入口
    │   ├── kernel/              # OpenHarness 内核（复用，尽量不改）
    │   │   ├── agent_loop.py    # streaming tool-call cycle / retry / 并行
    │   │   ├── permission.py    # 多级权限 + PreToolUse/PostToolUse hooks
    │   │   ├── memory.py        # CLAUDE.md / MEMORY.md / 上下文压缩 / 会话恢复
    │   │   ├── providers.py     # 厂商中立 workflow（Anthropic/OpenAI/本地…）
    │   │   └── tools/           # 43 内置工具（文件/Shell/搜索/Web/MCP）
    │   ├── iterate/             # iterate 语义层（深度定制核心）
    │   │   ├── config.py        # iterate.config.yaml 加载 + Master/Overrides 合并
    │   │   ├── review.py        # 确定性聚合：去重/过滤/排序/收敛（移植 TS 语义）
    │   │   ├── meta_review.py   # 6 项一致性审计（移植 TS 语义）
    │   │   ├── decision_log.py  # append-only 决策日志
    │   │   ├── validate.py      # validation.commands 精确匹配 + 执行
    │   │   └── prompts.py       # 评审/fix 子代理提示词模板（含 findings schema）
    │   ├── commands/            # iterate-harness 内置命令
    │   │   ├── review.py        # dry-run 纯审查（多轮收敛 + meta-review）
    │   │   ├── iterate.py       # normal 自治闭环（评审→修复→验证→回环→自停）
    │   │   ├── init.py          # 配置初始化向导（复用 iterate_cli onboarding 思路）
    │   │   ├── resume.py        # 会话恢复 / 断点续跑
    │   │   └── log.py           # 决策日志查看 / 回放
    │   └── tui/                 # TUI 组件（复用 OpenHarness UI 框架）
    │       ├── approve.py       # 审批弹窗（↑↓ 导航、空格、Enter）
    │       └── dimensions.py    # 维度选择 / 评审进度面板
    ├── skills/iterate.md        # SKILL.md 以 anthropics 兼容 skill 内置
    ├── tests/                   # 语义层单测（移植自插件 test，≥53 项） + 内核 E2E
    └── README.md
```

#### 11.4.1 修订版架构（v1.11：源码级，落地实现以此为准）

> 形态：**保留 OpenHarness 包结构与内核原样 + 新增 `iterate/` 语义子包 + 8 处内核定点修改**。不虚构 kernel 层，不重排上游目录——最大化降低上游同步（rebase）成本。

```
iterate-harness/                     # fork 自 HKUDS/OpenHarness @ v0.1.9
├── src/openharness/                 # 上游包结构原样保留（裁剪清单见 §11.3.2-四）
│   ├── iterate/                     # ★ 新增子包：iterate 语义层（唯一大块新增代码）
│   │   ├── __init__.py
│   │   ├── settings.py              # IterateSettings(pydantic) + iterate.config.yaml 加载（Master/Overrides 深合并，移植插件 config-loader）
│   │   ├── review.py                # 确定性聚合引擎：去重/known_intentional 过滤/severity 排序/收敛统计（移植 TS review.ts）
│   │   ├── meta_review.py           # 6 项一致性审计（移植 TS meta-review.ts，含 ROUND_EMPTY 修复语义）
│   │   ├── decision_log.py          # append-only decision-log.jsonl + 回放
│   │   ├── validate.py              # validation.commands 精确匹配执行网关（对齐插件 validate.ts 语义）
│   │   ├── loop_policy.py           # IterateLoopPolicy：收敛判定/轮次上限/评审计划（经 QueryContext 注入 run_query）
│   │   ├── worktree_flow.py         # 修复轮 git 隔离编排（封装 swarm/worktree.WorktreeManager + 验证失败回滚）
│   │   ├── cost.py                  # 金额层：UsageSnapshot × 价格表 → 每轮/累计费用（补上游只算 token 的缺口）
│   │   ├── personalization.py       # 9 类结构化个性化数据（独立存储 ~/.openharness/iterate/，按 cwd 隔离）
│   │   └── prompts.py               # 评审/修复子代理提示词模板（含 findings schema、canonical 循环模板）
│   ├── commands/iterate.py          # ★ /iterate slash 命令 handler（在 commands/registry.py 注册一行）
│   ├── tools/iterate_tools.py       # ★ 5 工具：iterate_config/validate/review/decision_log/context（BaseTool 契约，注册于 tools/__init__.py）
│   ├── skills/bundled/content/iterate.md   # ★ SKILL.md 内置（自动成为 /iterate + skill() 双入口）
│   ├── prompts/claudemd.py          # ★ 一行改动：candidate 元组加 ITERATE.md（§11.3.2-二）
│   └── engine/query.py              # ★ 定点改动：868 行后插 iterate 控制块 + QueryContext 加 iterate_policy 字段
├── frontend/terminal/src/panels/    # ★ React 评审进度面板 + findings 分诊组件（protocol.py 加 review_progress 事件）
└── tests/iterate/                   # ★ 语义层单测（移植插件 53 测）+ loop_policy 集成测试 + compact 保留性测试
```

**内核定点修改清单（全部 8 处，每处一个 diff 面）**：

| # | 文件 | 改动 | 目的 |
|---|---|---|---|
| 1 | `engine/query.py` | `QueryContext` 加 `iterate_policy` 字段；`:868` 后插控制块（收敛判定→break / 注入评审消息 / 产出 `ReviewProgressEvent`） | 轮次控制与收敛自停 |
| 2 | `engine/stream_events.py` | 联合类型加 `ReviewProgressEvent`（round/new_findings/per_dimension/token_cost） | TUI 实时收敛仪表盘的事件源 |
| 3 | `engine/cost_tracker.py` | `add()` 时同步调 `iterate.cost.accumulate()`；或 QueryEngine 转发处挂钩 | 金额透明（每轮/累计） |
| 4 | `config/settings.py` | `Settings` 加 `iterate: IterateSettings`（定义移入 `iterate/settings.py`，此处仅 import） | iterate.config.yaml 与内核 Settings 融合 |
| 5 | `permissions/checker.py` | 加 `allowed_commands` 白名单（evaluate 顺序插在 denied_commands 前）；`path_rules` 判定加 `is_read_only` 分支实现「禁写不禁读」 | protected_paths / 验证命令白名单原生强制 |
| 6 | `services/compact/__init__.py` | iterate 关键产物（findings 列表 / 失败 diff / 决策摘要）写入 `_build_compact_attachments` 通道 | 防 microcompact 不可逆清空评审证据 |
| 7 | `commands/registry.py` + `tools/__init__.py` | 各加一行注册（handler/工具实体在 iterate 子包与 commands/iterate.py） | /iterate 命令与 5 工具 |
| 8 | `prompts/claudemd.py` | candidate 元组加 `ITERATE.md`（1 行） | 项目知识库自动注入 |

**评审编排数据流**（复用上游契约，零编排新造）：

```
/iterate 或 oh iterate review --dry-run
  → iterate/loop_policy 生成评审计划（dimensions × goal）
  → 模型同回合 N 次并行 agent 工具调用（query.py:830-844 asyncio.gather）
  → 每评审 agent = create_agent_task + WorktreeManager 隔离（只读评审可不建 worktree，dry-run 强制不建）
  → coordinator_drain 契约回收 task-notification 输出
  → iterate/review 确定性聚合（去重/过滤/排序/收敛）
  → iterate/meta_review 审计 → ReviewProgressEvent → React 面板
  → 未收敛：loop_policy 注入「只找新问题」下一轮；收敛：出报告 + decision_log 追加
```

#### 11.4.2 fork 工作流与上游同步

- **fork base**：`v0.1.9` tag（`a0f8552`，2026-05-07，最新稳定版）；同时 cherry-pick main HEAD `9b2efd7`（2026-06-04 "preserve profile auth when overriding model"——profile 覆盖模型时保留认证，对 DeepSeek 等兼容端点的 profile 切换场景直接受益）。
- **仓库形态**：遵循 §6 决策——主仓库 `harness/iterate-harness/` 唯一开发点，subtree 拆分独立发布仓（首个大版本后建）。
- **上游同步**：fork 仓加 `upstream` remote 定期 fetch；因内核改动锁定在 §11.4.1 的 8 个定点 diff 面，rebase 冲突面可控；每次同步跑 `tests/iterate/` 全量回归（53+ 单测是行为对齐锚）。
- **裁剪执行**：fork 首次提交即删 `vim/`、`channels/`、`ohmo/`（§11.3.2-四 证据），后续不再引入。
- **版本线**：与 skill/插件一致采用「主仓库统一 + 发布仓独立发版」；harness 版本独立递增（同插件 2.3.7 先例）。

### 11.5 CLI 命令集（v0）

> ⚠️ v1.11 勘误（源码级）：① 会话恢复参数不存在 `--session`，上游用 `--continue` / `--resume <id>`（`cli.py:2110-2123`），iterate 命令集对齐为 `iterate-harness resume <id>`（缺省 = 最近会话）；② 入口命令沿用上游 console script `oh`，iterate 以子命令组挂载（`oh iterate ...`，参照 `cli.py:765-777` 子命令先例），同时保留独立 `iterate-harness` 别名；③ 「harness --dry-run 静态预览」直接复用上游 `oh --dry-run`（预览 settings/auth/skills/commands/tools）。

| 命令 | 说明 |
|---|---|
| `iterate-harness init` | 交互式初始化 `iterate.config.yaml`（goal / dimensions / validation.commands / 个性化） |
| `iterate-harness review --dry-run` | 纯审查：多轮收敛 + meta-review，只读不写文件，产出审计报告 |
| `iterate-harness iterate` | 自治闭环：评审 → 原子修复 → 验证 → 回环 → 收敛自停 |
| `iterate-harness resume --session <id>` | 从历史会话断点续跑 |
| `iterate-harness log` | 查看 / 回放决策日志 |
| `iterate-harness --dry-run` | 内核静态预览（settings / auth / skills / commands / tools），不动模型不跑工具 |

### 11.6 v0 范围与里程碑

- **M1 语义层移植**：`config.py` / `review.py` / `meta_review.py` / `validate.py` / `decision_log.py` 落地，移植 ≥53 单测全绿。
- **M2 命令打通**：`review --dry-run` 与 `iterate` 两条主链路在 OpenHarness 内核跑通，权限 hooks 拦截修复写操作。
- **M3 CLI 完善**：`init` / `resume` / `log`，厂商中立 provider 验证（DeepSeek + 至少一家兼容端点）。
- **M4 TUI 打磨**：审批弹窗 + 维度选择 + 评审进度面板，键盘导航符合偏好。
- **M5 独立分发**：`pip install` / install.sh，版本号全项目统一（遵循既有硬约束），发布到 GitHub。

### 11.7 风险与开放问题（路线 B 新增）

- OpenHarness 内核升级与 fork 漂移：锁定精确版本，必要时以 patch 形式跟进。
- 语义层 TS/Python 双实现漂移：以单测对齐 + 同一份用例（tests 移植）约束行为一致。
- `iterate_cli` 复用边界：validate / onboarding 直接调用现有 Python 代码，避免重复实现。
- TUI 与 skill/插件 UX 的一致性：独立 harness 可自成一派，不与 dsh 对齐。
- 许可证：OpenHarness MIT（宽松），可入生产；继续禁止 GPL/AGPL 依赖。

## 12. 版本记录
- v1.0（2026-08-14）：首版设计草案。决策点：仓库形态=方案 B 同仓库双模块；落地优先级=先 dsh 最小验证插件。
- v1.1（2026-08-14）：新增 dry-run 纯审查模式（只评审不改文件、多轮收敛出报告）；v0 范围调整为「自治闭环 + 并行评审 + dry-run」；能力边界表补充 dry-run 与自主多轮收敛差异。
- v1.2（2026-08-14）：实现阶段落地 dry-run——新增确定性纯函数引擎 `src/review.ts` 与 `iterate_review` 工具（plan / aggregate 两操作），v0 工具数由 4 更新为 5（config / validate / decision-log / context / review），补充 canonical dry-run 收敛循环模板说明。
- v1.3（2026-08-14）：实现阶段落地自治闭环——`skill-prompt.ts` 补充 normal 模式 canonical 模板（配置→评审计划→并行评审→确定性聚合→原子修复→验证→回环→达标自停）；评审报告类型由 `DryRunReport` 泛化为 `ReviewReport`（mode 支持 dry-run / normal，两模式共用同一确定性聚合引擎），报告新增全局去重/过滤/排序后的 `findings` 字段，供 fixer 直接消费；20 个单元测试全绿。
- v1.4（2026-08-14）：实现阶段补齐 meta-review 报告审计——新增 `src/meta-review.ts`（6 项一致性检查：COUNT_MATCH / SEVERITY_SUM / DIMENSION_SUM / SORT_ORDER / CONVERGENCE / ROUND_SHAPE），`iterate_review` 新增 `meta-review` 操作，dry-run 收敛报告产出前先审计自身一致性并给出 approved / needs_revision 判定；修复 ROUND_EMPTY 误报 bug（收敛轮=最后一轮空属正常成功信号，不再标记为缺陷）；插件经真实 dsh headless 运行时验证：5 个 iterate 工具全部注册、系统提示成功注入、aggregate + meta-review 端到端输出符合预期；新增 README 使用说明；33 个单元测试全绿。
- v1.5（2026-08-14）：新增独立 harness 设计章节（§11）——确认 OpenHarness 为 Python 栈并决策独立 harness 采用 Python 同栈；以用户视角完成「skill / dsh 插件 / 独立 harness」三层能力差距分析（内核级 agent loop、token 成本透明、审批强制执行、session 恢复、持久记忆、厂商中立、技能生态复用、独立分发等）；给出 fork 定制点、模块架构、CLI 命令集（init / review --dry-run / iterate / resume / log）、v0 里程碑（M1 语义层移植 → M5 独立分发）与路线 B 新增风险。
- v1.6（2026-08-14）：仓库形态决策迭代（§6）——新增独立插件发布仓库 jingzhao-l/iterate-plugin（git subtree 拆分 harness/iterate-plugin，保留完整历史，作为 dsh 生态镜像并引流回主仓库）；主仓库保持唯一维护点，同步走 subtree push（无 CI 同步、无 force-push）；插件 package.json 补 repository/homepage/bugs 元数据指向主仓库；插件开始独立版本线（自 2.3.7 起），第 9 节版本统一约束对插件生效范围同步更新。
- v1.7（2026-08-14）：npm 发布源切换至插件仓库（§6）——建立本地发布工作区 `.release/iterate-plugin/`（gitignore），插件仓库从"只读镜像"升级为 npm 正式发布位：版本 bump、git tag、npm publish 均在插件仓库进行，主仓库仍是唯一开发/评审维护点；版本线确认沿用当前数值（不重置 1.0.0，npm 不允许发布低于已发布最高版本），自 2.3.7 起独立递增；主仓库 `dsh-plugin` topic 移除，仅插件仓库保留。
- v1.8（2026-08-14）：新增 §11.2.1 用户体验场景深析——区别于 §11.2 内核能力视角，按「看（实时收敛仪表盘 / 逐 hunk diff 审批 / findings 分诊 / init 检测式向导）/ 摸（Esc 暂停干预 / 断点续跑画面）/ 跑（PR 评论 + 质量门禁 / git hook / 批量定时）/ 沉淀（finding 指纹趋势 / HTML 报告 / 评审回放）」四类记录 skill 与插件原理上做不出的独占体验；给出 v0 优先级（分诊界面 > diff 审批+干预 > PR/CI 模式）。
- v1.9（2026-08-14）：新增 §11.2.2 代码实况深析——三路并行源码审查（iterate_cli 六模块 / wizard+tui+模板 / SKILL.md+配置层）证实：① iterate_cli 100% 确定性本地计算零 LLM，onboarding 全链路可直接复用为 harness 数据层（7 类现成数据资产清单）；② prompt 约定→机制强制全景对照：插件已强制 10 项确定性计算类约定，剩余 20 项分「副作用约束类（hooks/权限可强制）」与「状态继承类（session/持久化可强制）」；③ 维度 yaml 现仅 focus 文本，harness 可解锁 per-dimension model/并发/token 预算、维度级阈值门禁、维度专属验证命令等 7 项；④ 用户旅程断点源码级定位（TUI 实为 input() 问答、向导不问 goal/max_rounds/atomic/language、验证命令无 dry-run 预检等）；⑤ 顺带发现 4 个现有代码问题（tui.question 接口 bug、TS 示例 auto_merge 文档矛盾、决策日志模板未接线、双 __name__ 守卫）记入待修复清单。
- v1.10（2026-08-14）：§6 增补 harness 发布仓库决策——harness 首个大版本完成后另开独立发布仓库（同 iterate-plugin subtree 模式），主仓库统一维护。同日随 v2.3.7 发布修复 §11.2.2 所列 4 个代码问题（tui.question 契约 + prompt_prefix 死代码删除、TS 示例 auto_merge 矛盾、决策日志模板角色注释、cli.py 冗余守卫移除，新增 tests/test_tui.py）。
- v1.11（2026-08-14）：OpenHarness 源码级落地依据补全——克隆 v0.1.9 稳定版至 `.external/`（gitignored）并完成四路并行深析（内核引擎/扩展面/状态配置/编排 UI）。新增 §11.3.1 真实结构核验、§11.3.2 源码级深析（12 项草案纠偏：真循环在 run_query 而非 QueryEngine、hook 无轮次事件、plugins/bundled 空载、Textual 未接线、无 --session、CostTracker 只算 token、双 worktree 实现、无 allowed_commands、path_rules 不分读写、microcompact 不可逆清空、bundled skill 仅 *.md、personalization 模型不兼容；8 个现成挂载点清单；并行评审 ×N 源码契约；fork 裁剪清单 vim/channels/ohmo 可删）、§11.4.1 修订版架构（iterate 子包 + 8 处内核定点修改 + 评审编排数据流）、§11.4.2 fork 工作流（base=v0.1.9+cherry-pick 9b2efd7、上游同步策略）、§11.5 勘误（resume 参数/oh 子命令组/dry-run 复用）。v1.10 §11.4 目录树标注为草案存档，落地以 §11.4.1 为准。
- v1.12（2026-08-15）：M1–M3 落地实现完成——**M1 语义层**：`src/openharness/iterate/` 子包 12 模块全部就位（types / config_loader / review〔含 plan/round/report 序列化与解析契约〕 / meta_review / validate / decision_log / settings〔IterateSettings 入内核 Settings〕 / loop_policy / cost〔金额层：价格表 × UsageSnapshot → 每轮/累计 USD〕 / personalization〔9 类结构化、按 cwd 哈希隔离存储〕 / prompts〔canonical dry-run/normal 模板移植自 skill-prompt.ts〕 / worktree_flow〔git 隔离编排：enter/commit/exit、验证失败自动回滚〕）；包 `__init__` 采用 PEP 562 惰性导出打断 config.settings→iterate→api→auth→config.settings 循环导入。**M2 命令打通**：8 处内核定点修改全部落地（① query.py 控制块：turn 末读 iterate_state → ReviewProgressEvent/下一轮注入/收敛自停，另补工具 metadata 回写 tool_metadata 使跨 turn 状态可见；② stream_events.py 增 ReviewProgressEvent；③ 金额层经 loop_policy 的 CostMeter 挂钩（选 QueryEngine 转发方案）；④ Settings.iterate 字段；⑤ permissions：allowed_commands 精确匹配白名单（插在 denied_commands 前）；path_rules 维持上游双向拦截契约（iterate protected_paths 搭载，为"禁写不禁读"设计下限的超集）；⑥ compact 增 iterate_review 附件防 microcompact 清空评审证据；⑦ /iterate slash 命令 + 5 工具注册；⑧ claudemd 候选加 ITERATE.md）；QueryEngine 自动装配 IterateLoopPolicy（settings.iterate.enabled 开关，传 False 显式关闭）。**M3 CLI**：`oh iterate init/review/run/resume/log` 子命令组（init 含 manifest 检测式生成 + questionary 交互；review/run 走 run_print_mode headless 全自动管线；resume 复用 session_storage 恢复进 REPL；log 支持 --tail/--json）。bundled skill `iterate.md` 内置（自动 /iterate + skill() 双入口）。**验证**：tests/test_iterate/ 137 单测全绿（语义层 74 + 引擎/权限/内核集成 63），全仓回归 1038 passed（2 个失败均为沙箱写 ~/.openharness 与 npx 网络的环境性问题）；语义层与工具层 ruff 全过（内核遗留 lint 基线未动）。**有意偏差记录**：① path_rules 读写分支未按 §11.4.1 #5 拆分（上游测试契约 deny 双向拦截，选择搭载而非破坏）；② protected_paths 尚未自动注入 path_rules（v0.2 前接入 hooks 装配）；③ M4 TUI（React 收敛仪表盘/逐 hunk diff 审批/分诊界面）与 M5 独立分发（pip/install.sh/发布仓）未启动，为下一版本范围。
- v1.13（2026-08-15）：M4–M5 落地完成，v1.12 偏差②闭合——**偏差修复（权限层自动装配）**：`permissions/checker.py` 新增 `build_permission_checker(settings)` 工厂，把 `Settings.iterate` 自动装配进权限层：protected_paths 归一化为绝对路径 deny 规则（`.env`→`*/.env`、`secrets/*`→`*/secrets/*`，绝对模式原样透传；对用户已配规则去重、深拷贝不改源设置、`iterate.enabled=False` 时整体旁路）；forbidden_fix_patterns 编译为正则并经 `evaluate()` 新增的 `content` 参数对变更型工具写载荷（content/new_string/diff/patch，query.py `_extract_permission_content` 仅对非只读工具提取）做硬边界拦截（先于 allowed_tools/allowed_commands，不可被白名单绕过；非法正则告警跳过不阻断启动）。REPL runtime、/permissions、/plan×2 共 4 处实例化点全部替换为工厂。新增 8 项装配测试（含归一化、去重、旁路、边界优先级、载荷提取）。**M4a 协议摸底**：React TUI 链路确认为 ReviewProgressEvent → backend_host `_render_event` → BackendEvent（stdout `OHJSON:` JSONL）→ useBackendSession.handleEvent → React state → 面板组件（TodoPanel/SwarmPanel 同构模式）。**M4b 收敛仪表盘**：后端三处（protocol.py 增 `review_progress` 事件型 + 9 个 review_* 字段；backend_host 事件转换含人类可读 message；app.py print 模式 text→stderr / stream-json 双通道）+ 前端四处（types.ts ReviewProgressSnapshot；useBackendSession 状态 + 逐轮 new_findings 趋势环形数组；新组件 ReviewProgressPanel〔converged 绿/iterating 品红边框、trend n→…→0、维度 Top6、USD 成本〕；App.tsx 接线于 TodoPanel 与 StatusBar 之间）；tsc 零错误，新增 backend_host 集成测试 1 项。**M4c findings 分诊**：第 6 工具 `iterate_triage`（y=fix / n=skip / a=always-ignore）：交互经 `context.metadata["ask_user_prompt"]`（TUI 走既有 question modal，零前端改动）；`a` 持久化 KnownIntentional（file+dimension+line 三元组去重，note 可选）；全部决策落决策日志（type=decision、kind=triage）；headless 无交互通道时整体套用 `default` 参数兜底；>50 条 findings 拒绝（防问答锁死会话）；8 项新测试（含持久化→review.filter_known_intentional 闭环验证）；prompts.py 与 bundled skill iterate.md 同步第 6 工具说明，canonical dry-run 循环增第 7 步分诊入口。**M5a 分发适配**：README.md / README.zh-CN.md 重写为 iterate-harness 身份（fork 致谢 + 六工具/两模式/特性表/架构树/安装/测试；上游功劳明确归属）；install.sh / install.ps1 / install_dev.sh 三脚本适配：源固定 `jingzhao-l/iterate-harness.git`、默认 git clone + venv + 可编辑安装（--from-source 保留为兼容别名、移除 pip openharness-ai 模式）、venv/源目录改 `~/.iterate-harness-{-src,venv}`、注册 `oh`+`iterate-harness`（Windows 优先 iterate-harness.exe 避开 PowerShell Out-Host 别名）、彻底移除 ohmo/channels 引用；.gitignore 补 `.iterate-harness-venv/`；CHANGELOG 增 0.2.0 条目；test_install 契约更新为 fork 启动器断言；版本 0.2.0 对齐（pyproject / cli.py __version__ / CHANGELOG / README badge）。**M5b 发布仓**：`git subtree split --prefix=harness/iterate-harness` 推送至独立发布仓库 `jingzhao-l/iterate-harness`（同 iterate-plugin 模式，主仓库唯一维护点），仓库描述与 dsh-plugin 无关 topic 不适用、改为 iterate-harness 语义描述。**验证**：tests/test_iterate/ 153 单测全绿（含本轮新增 17 项），全仓回归 1070 passed + 6 skipped（3 个失败均为沙箱环境性：MCP stdio 真连接、插件安装流、bash 超时部分输出行为；另 test_http_flow collection error 为 venv mcp 2.0.0 无 fastmcp 的既有环境问题，stash 验证与本次改动无关）；前端 tsc --noEmit 零错误；install 脚本 bash -n 语法校验通过；语义层/工具层/本轮触碰内核文件 ruff 无新增告警。**残留偏差更新**：v1.12 偏差②已闭合；偏差①（path_rules 读写分支）维持搭载决策不变；逐 hunk diff 审批 + Esc 干预（§11.2.1 v0 优先级②）未纳入本轮，与 PR/CI 模式（优先级③）一并留待下一版本。
- v1.14（2026-08-15）：M6 落地完成（逐修复 diff 审批 + CI/PR 模式），v1.13 残留②③闭合——**M6a 逐修复 diff 审批**：`Settings.iterate` 新增 `require_fix_approval`（默认 False）；query.py `_execute_tool_call` 在权限判定后插入审批门 `_needs_iterate_fix_approval`：三条件全满足才触发（IterateLoopPolicy.require_fix_approval 开启 ∧ 工具 ∈ FILE_MUTATING_TOOLS〔write_file/edit_file/notebook_edit + file_write/file_edit MCP 风格别名〕∧ iterate_state.mode == "normal"——dry-run 评审永不触发）；触发时即便 full-auto 也降级为 requires_confirmation 走交互通道，提示语内嵌 diff 预览（`_fix_approval_reason`：edit 用 old/new 对比、write 用截断原文模拟 -/+ 两段，统一 40 行/每行 200 字符裁剪界）；硬拒绝（保护路径 deny / forbidden_fix_patterns 命中）不参与审批门、绝不被降级为可确认项；审批拒绝即工具返回错误且文件零改动。新增 TestFixApproval 6 项测试（normal 模式提示含 diff 且拒绝后文件不变、批准后正常落盘、gate 关闭/dry-run 不触发、硬拒绝不被覆盖、forbidden pattern 边界覆盖 edit new_str、diff 预览 write/edit 变体裁剪）。**M6b CI/PR 模式**：新模块 `iterate/ci_report.py`（纯函数、防御式）：`latest_report_entry` 取决策日志最后一个含 findings 的 report 条目；`ReportSummary.from_entry` 防御解析（畸形 findings 过滤、totalFindings 回退 len）；`render_github` 按 GitHub Actions workflow commands 规范输出（critical/high→error、medium→warning、low/未知→notice，file=/line= 属性，%/\r/\n/:/, 全量转义）；`render_text` 人类可读摘要；`severity_gate` 退出码策略（none|low|medium|high|critical，默认 high，非法值回退默认）；报告缺失/畸形降级为空报告不崩管道。CLI 新增 `oh iterate report`（--github / --fail-on，--fail-on 非法值报 usage error 退出码 2，缺报告时 stderr 提示 + 空报告退出码 0）；/iterate slash 命令同步 report 子命令（REPL 对等）。新增 test_ci_report.py 28 项测试（Summary 解析×6 / latest_entry×3 / render_github×3 / render_text×2 / severity_gate×6 / CLI 端到端×6 / slash×2）。**版本与分发**：版本 0.3.0 对齐（pyproject / cli.py __version__ / CHANGELOG 0.3.0 条目 / README badge）；README.md / README.zh-CN.md 特性表各增「逐修复 diff 审批」「CI / PR 模式」两行 + CLI 速览补 `oh iterate report`；顺手修复 test_decision_log.py 既有 E741 lint。**验证**：tests/test_iterate/ 187 单测全绿（v1.13 的 153 后 +6 M6a +28 M6b）；全仓回归 1104 passed + 6 skipped（3 个失败与 test_http_flow collection error 均为 v1.13 已记录沙箱/环境既有问题，无回归）；iterate 语义层/工具层/命令层 ruff 全过（cli.py 既有 lint 基线未动）。**残留偏差更新**：v1.13 残留的逐 hunk 审批以「逐工具调用 diff 审批」形态闭合（单次 edit 即单 hunk 场景等价，多 hunk 单调用场景由 40 行裁剪预览覆盖）；Esc 中途干预（暂停/改向运行中闭环）仍未实现，为下一版本候选；GitHub 主仓 10 项 dependabot 告警（5 high，上游 fork 继承依赖）仍待单独排查。
- v1.15（2026-08-15）：v1.14 两项残留全部闭合——**Esc 中途干预（§11.2.1 v0 优先级②剩余半项）**：① `loop_policy.py` 增 pause 通道：`LoopDecision.paused` 字段 + `IterateLoopPolicy.pause_requested` / `request_pause()` / `clear_pause()`；`_decide` 仅在「本将继续注入下一轮」分支消费 pause（stop 决策路径顺带清 flag，pause 在无新聚合的 turn 上存续等待下一个轮边界）。② `query.py` turn 末控制块：`decision.paused` 时经 `context.ask_user_prompt`（复用既有 question modal，前端零改动）弹干预菜单（`_handle_iterate_pause`）：`s`=跳过当前 top finding / `n <dims>`=收窄维度 / `x`=直接停 / 空=恢复原下一轮指令（原 inject 保留在 decision 上）；答案映射为对应注入指令（prompts.py 新增 `pause_menu_question` / `skip_current_finding_instruction` / `narrow_dimensions_instruction`）；headless 无交互通道默认安全停止；prompt 通道异常兜底停止；每次干预落决策日志（type=decision、kind=intervention，best-effort 不阻断控制流）。③ `backend_host.py` `_interrupt_active_request` 优雅优先：policy 存在 ∧ pause 未挂起 ∧ tool_metadata 含 iterate_state（闭环已启动）→ 置 pause + 系统 transcript 提示「下一轮边界暂停，再按 Esc 强制打断」，不取消 task；第二次 Esc（pause 已挂起）回落既有硬取消；非 iterate 会话保持上游硬取消行为不变。④ `QueryEngine.submit_message` 起新意图清除残留 pause（`iterate_policy=False` 显式关闭场景经 getattr 防御兼容，修复回归）。⑤ QueryEngine 新增 `iterate_policy` 只读属性（backend 访问通道）。**Dependabot 排查修复（10 项全清，5 high）**：全部为上游继承的 npm 工具链告警——autopilot-dashboard：vite ^6.3.2→^6.4.3（连带修复 postcss×3/esbuild/@babel/core）；frontend/terminal：marked ^18.0.0→^18.0.9、tsx ^4.19.2→^4.23.12（esbuild 0.27.4→0.28.2）、ws 8.20.0→8.21.3（lockfile 经 npm audit fix）；两包 npm audit 均 0 告警，vite build 与 tsc --noEmit 验证通过。**测试**：新增 11 项（TestPauseMechanics 5：paused 决策保留原注入/无请求不暂停/跨 noop turn 存续/stop 清 flag/clear_pause；TestEscIntervention 6：x 停止且第二响应不消费/s 注入跳过指令/n 注入收窄指令/空恢复原始下一轮/headless 默认停/干预落日志）+ backend_host 优雅中断 1 项（首 Esc 暂停不取消、次 Esc 强制取消）；FakeApiClient 增 on_stream 回调模拟运行中按 Esc。**版本与验证**：版本 0.4.0 对齐（pyproject / cli __version__ / CHANGELOG / README badge）；README 双语特性表增「Esc 中途干预」行；tests/test_iterate 198 全绿（187+11），engine+react_backend 54 绿，全仓 1115 passed + 6 skipped（3 失败均为 v1.13 已记录环境性）；触碰文件 ruff 全过。**残留说明**：Esc 干预菜单当前为 question modal 自由文本协议（s/n/x），未做专属方向键菜单组件（v1 候选）；dependabot 告警需推送后由 GitHub 自动重扫关闭。
- v1.16（2026-08-15）：0.5.0「数据沉淀起步 + 体验补齐」落地，v1.15 残留的方向键菜单候选闭合——**① finding 指纹趋势库（§11.2.1 沉淀类）**：新模块 `iterate/trend_store.py`（纯函数 + 防御式）：`finding_fingerprint` 以 `file|line|dimension` SHA-1 为稳定指纹（line 仅在正整数时参与，无行号 finding 视为文件级 `"0"`；缺 file/dimension 返回 None 不追踪）；`record_run` 在 report 条目落决策日志时由 `iterate_tools.py` `_record_trend` 挂接（best-effort，异常仅记 error 不破坏闭环）；分类学：**new**（库中首见）/ **fixed**（上轮 open 本轮缺席，记 fixed_at）/ **regressed**（曾 fixed 本轮复现，runs 续接）/ **stubborn**（open 且 runs≥3）；存储 `.iterate/trend-library.json`（临时文件+rename 原子写，损坏重置为空，2000 条 last_seen LRU 剪枝）；暴露面：`oh iterate log --trend`（cli.py）/ `/iterate trend` 与 `/iterate log trend`（slash）；`summarize`+`render_trend_summary` 输出顽固 finding Top20（file:line dimension severity runs summary）。**② Esc 干预菜单组件化（v1.15 残留闭合）**：新交互通道 `AskUserSelect = (title, options) -> value` 全链路接线（query.py QueryContext.ask_user_select → query_engine 构造器 → ui.runtime → backend_host `_ask_select`）；backend 以 `modal_request` 携 `kind=select_prompt`（request_id/question/options/cancel_value，复用 `_question_requests` 应答通道即 question_response）；前端 App.tsx 拦截 select_prompt：↑↓ 导航 / Enter 选定 / 数字键快选 / Esc 提交 cancel_value（安全首项），渲染复用 SelectModal 组件；query.py `_handle_iterate_pause` 拆分 select/text 双路径：select 路径弹 4 选项菜单（prompts.py `pause_menu_title`/`pause_menu_options`：resume 置首保证 Esc 取消安全、skip、narrow→追问维度经 `narrow_dimensions_question`（空答案降级 resume）、stop），text 路径保留 v1.15 自由文本 s/n/x 兜底（非 TUI 前端）；select 通道异常兜底安全停止。**③ 断点续跑画面（§11.2.1 摸类）**：新模块 `iterate/last_state.py`：`summarize_last_run` 从决策日志提取最后一次收尾摘要（mode/verdict/rounds〔全日志最大轮〕/totalFindings/四档 severity 桶/Top3 finding 预览〔summary 截 120 字符〕/lastIntervention〔最后一个 kind=intervention 条目〕/entryCount，畸形数据全防御返回 None）；backend_host 启动 ready 后 `_emit_last_loop_state` 发 `last_loop_state` 事件（protocol.py 新事件型，复用 state 字段；摘要失败仅 warning 绝不阻断启动）；前端 useBackendSession 增 `parseLastLoopState` 防御解析 + lastLoopState 状态；新组件 `IterateResumePanel.tsx`（◉ last iterate run 一行摘要 + finding 预览 + last intervention + `/iterate resume`·`/iterate trend` 入口提示；live review_progress 出现即自动让位）；配套 `/iterate resume` slash 子命令（无历史友好提示；有历史经 prompts.py 新增 `resume_kickoff` 提交续跑提示词——嵌入上轮 verdict/rounds/findings 预览，指示先 iterate_log 重读日志、复核仍复现的 finding、不复报已消失项、续跑前落 resume 决策条目）；session_storage `_PERSISTED_TOOL_METADATA_KEYS` 增 `iterate_state`（跨重启保留轮次历史/收敛计数，`oh iterate resume` 恢复的是真实 mid-loop 状态）。**测试**：新增 test_trend_resume_ui.py 22 项（指纹稳定性与行敏感/不可追踪 None/new-fixed-regressed 生命周期/3 轮顽固/畸形 finding 跳过/损坏库重置/summarize+render 含顽固与友好空态/last_state 无历史 None+字段提取+未知 severity 忽略//iterate trend 与 log trend 渲染/resume 无历史与 kickoff 提交/select 菜单 resume-stop-skip-narrow 追问-narrow 空降级-通道异常安全停）。**版本与验证**：版本 0.5.0 对齐（pyproject / cli __version__ / CHANGELOG 0.5.0 条目 / README badge）；README 双语特性表增「finding 指纹趋势库」「断点续跑」两行、Esc 行更新为方向键菜单描述、CLI 速览补 `oh iterate log --trend`；tests/test_iterate 220 全绿（198+22），全仓 1138 passed + 6 skipped（3 失败 + test_http_flow collection error 均为 v1.13 已记录环境性，无回归）；前端 tsc --noEmit 零错误；触碰文件 ruff 全过。**残留说明**：changed-only 快审、批量/定时评审（0.6.0 范围）与 HTML 单文件报告、评审回放、per-dimension 资源解锁（v1.0 范围）未启动。
- v1.17（2026-08-15）：0.6.0「无人值守场景扩展」落地，v1.16 残留的 changed-only 快审 + 批量/定时评审两项闭合（§11.2.1 跑类「批量/定时：一条命令审 10 个仓库出排行；cron 每天跑，只报新增问题」）——**① changed-only 快审**：新模块 `iterate/git_scope.py`（纯 subprocess 管道，15s 超时，全失败软返回）：`validate_ref` 以白名单正则（`^[A-Za-z0-9_][A-Za-z0-9_./~^-]*$`，支持 HEAD~3/HEAD^2/origin/release-1.2）防 git 选项注入（subprocess 本就走 list argv，双保险）；`detect_repo_root` 经 `git rev-parse --show-toplevel`；`collect_changed_files` 合并 `git diff --name-only <ref>` + `git status --porcelain`（重命名只取新路径、剥引号、仅磁盘上真实存在的文件入选、去重排序、200 文件硬上限）；ref 不存在时 diff 失败软降级到 status 兜底。注入链路四层：prompts.py `changed_scope_clause`（kickoff 内嵌 JSON 文件清单并指示传给 plan 工具）挂入 `dry_run_kickoff`/`normal_kickoff`（新增可选 `changed_files` 参数）；review.py `build_review_plan` 非空清单时 scope 强制翻转为 `changed-only` 并透传 `reviewer_task_prompt`（新增 changed_files 参数，逐文件列出「review ONLY these files」）；`IterateReviewInput` 新增 `changed_files` 字段、`_plan` 透传。双入口：CLI `oh iterate review|run --changed [--ref <ref>] [--clean-ok]`（`--clean-ok` 空变更优雅退出 0，为定时场景防噪声）与 slash `/iterate review|run --changed [--ref]`（干净树/非 git 仓友好提示不提交、非法 ref Rejected）；usage 帮助同步。**② 批量多仓评审 + 排行**：新模块 `iterate/batch.py`：`run_batch` 顺序逐仓走 headless print 管线（`run_print_mode(cwd=repo)`，per-repo stdout 经 redirect_stdout 捕获、单仓异常仅降级为 error 记录绝不中断整批；changed-only 默认，干净树直接 short-circuit 为 clean 状态零成本跳过，`--full` 全量；`_reviewed_record` 复用 ci_report.ReportSummary 从各仓决策日志读 verdict/totalFindings/severity）；`rank_records` 排序策略 reviewed（score 降序）> clean > error；`repo_score` 严重度加权 critical 10/high 5/medium 2/low 1；`render_ranking` ASCII 表格（repo/status/findings/c·h·m·l/score/verdict/note）。CLI `oh iterate batch <repo...> [--ref] [--rounds] [--full] [--mode] [--json]`。**③ 定时评审（cron）**：复用既有 cron 注册表/守护进程（注册表 `~/.openharness/data/cron_jobs.json` 文件锁读改写、守护进程 `oh cron start` 30s tick、历史 `cron_history.jsonl`）；`build_scheduled_command` 生成 `oh iterate review --changed --clean-ok --ref <ref> --rounds N`（normal 模式换 run 子命令）；`install_schedule` 校验 cron 表达式（croniter）与 ref 后 upsert `iterate.review-changed` 任务（携 cwd 与 timeout）；cron schema 增可选 per-job `timeout` 字段（`execute_job` 原硬编码 300s 改为 `_job_timeout`：默认 300、钳位 [1,7200]、非法值回退默认；超时 stderr 消息同步动态化）——多轮 agent 评审默认给 3600s；CLI `oh iterate schedule add <cron> [--ref/--rounds/--mode/--timeout]` / `schedule remove` / `schedule status`（含 cron_history 最后一次执行态）；「只报新增问题」由趋势库承接（`oh iterate log --trend` 的 new/stubborn 分类），定时任务本身零 LLM 判定。autopilot 子进程任务模式为既有先例，本设计沿用子进程而非 in-process 回调（改 job schema+handler 注册表超出最小集成）。**测试**：新增 test_changed_review.py 23 项（validate_ref 合法/非法集、仓外空/干净树空/diff+untracked+rename 收集/200 上限钳位/坏 ref status 兜底、plan 钉 scope 与清单嵌入/无清单保持配置 scope/空白项过滤、dry_run+normal kickoff 内嵌与无 delta 不变、工具 plan 操作端到端、slash review --changed 提交与 clean 友好与非法 ref 拒绝与 run --changed、无 flag 保持 full、_parse_changed_flags 默认/ref 取值/缺值回退）+ test_batch_schedule.py 18 项（scheduled command 两模式格式与非法 ref、install 非法 cron/mode 拒绝、upsert 去重替换与 remove 幂等、status 报 job+历史、_job_timeout 默认/覆盖/钳位/非法、execute_job 真实 1s 超时记 history、repo_score 权重、rank worst-first、render 表格、_reviewed_record 读决策日志、run_batch clean 短路/缺仓 error/坏 ref error/混合仓库各一记录；cron 注册表经 OPENHARNESS_DATA_DIR 隔离）。**版本与验证**：版本 0.6.0 对齐（pyproject / cli __version__ / CHANGELOG 0.6.0 条目 / README badge）；README 双语特性表增「changed-only 快审」「批量排行」「定时评审」三行、CLI 速览补 `--changed`/`batch`/`schedule add`；tests/test_iterate 261 全绿（220+23+18），触碰文件 ruff --fix 清零（import 排序/UTC 别名）；CLI `oh iterate --help` 冒烟确认 batch/schedule 挂载。**残留说明**：HTML 单文件报告、评审回放、per-dimension 资源解锁（v1.0 范围）未启动；cron 全 UTC 无本地时区（注册输出已提示 UTC）。
- v1.18（2026-08-15）：1.0.0「首个稳定版」落地，v1.17 残留的 v1.0 三项全部闭合——**① HTML 单文件报告（§11.2.1「看类：HTML 单文件报告——收敛曲线、severity 分布、内嵌 diff，可直接发给别人看」）**：新模块 `iterate/html_report.py`（纯函数、防御式、零外部依赖）：`build_html_report` 复用 ci_report.latest_report_entry 取最新 report 条目，渲染为 ONE 自包含 `.html`（内联 CSS、零 script、零外链 http/https——CI 产物可离线打开）；内容分层：头部（verdict/mode/converged 三徽标 + goal + 收尾时间戳/轮次）、summary 卡片（total/critical/high/rounds）、**SVG 收敛曲线**（convergence.findingsByRound 折线 + 逐点数值标注，空序列降级占位文案）、severity 与维度分布横条（固定色表）、findings 全表（severity 徽标/file:line/dimension/summary/failure_scenario/suggested_fix）、**修复时间线**（report 之前的 atomic_fix/revert/validation 条目，≤50 条，atomic_fix 携 diff 字符串时渲染 +/- 着色的 `<pre class="diff">`）；安全：全部日志衍生文本经 html.escape(quote=True)，severity 颜色仅来自固定映射表（critical #b91c1c/high #ea580c/medium #ca8a04/low #2563eb），日志内容无法注入标记或 CSS。入口：CLI `oh iterate report --html [path]`（'-' 或缺路径默认 `.iterate/report.html`，父目录自动创建；--fail-on 门禁语义不变——CI 可同时上传产物并按严重度卡退出码）与 slash `/iterate report --html`（写文件后附 text 摘要）；报告缺失时 CLI stderr 提示且不落文件。**② 评审回放（§11.2.1「log --replay 按时间序回放每轮决策，像看录像」）**：新模块 `iterate/replay.py`：`build_replay_lines` 按日志原序逐条输出 `[+相对秒] r轮次 类型(16列对齐) 摘要   (绝对时间戳)`——相对偏移以首条可解析时间戳为原点（不可解析降级 `[+?s]`）；每类型摘要按优先键探测（round_start→goal/dimensions/mode、review_result→newFindings/totalFindings、atomic_fix→summary/file、validation→command/status、report→verdict/totalFindings 等），未知类型回退截断 JSON 预览、空载荷 `(no payload)`、长文本 140 字符截断（空白折叠）；尾部 `(N entries replayed)` 计数。入口：CLI `oh iterate log --replay` 与 slash `/iterate log --replay`；空日志友好占位。**③ per-dimension 资源解锁（§11.2.1 三「维度配置体系解锁项」首个子项：per-dimension model/concurrency/token_budget）**：types.py 新增 `DimensionResources`（model/concurrency/token_budget 三可选字段 + is_empty()，未设即继承会话默认）；IterateConfig 增 `dimension_resources: dict[str, DimensionResources]`；config_loader 新增 `parse_dimension_resources`（防御解析：非映射条目/非字符串 model/非整数 concurrency/负数 token_budget 记入 errors 并跳过绝不 raise，concurrency 钳位 [1,8]）与 `resources_to_dict`（仅序列化已设字段）；`validate_config` 同步校验并透出 resource 错误；merge_config 递归合并保持 Master+Overrides 语义。流转链路：review.py `DimensionPlan` 增 `resources` 字段，`build_review_plan` 按维度名从 config 取资源注入并在 reviewer_prompt 末尾追加显式派发指令（"Resource plan: model=…; max concurrent reviewer agents=…; token budget=…"——当前架构下 reviewer 由模型经 agent 工具派发，prompt 是计划的执行通道）；`plan_to_dict` 序列化 `resources`（空资源维度不输出该键）；`/iterate config` 列出生效的 per-dimension 资源。**测试**：新增 test_html_report.py 11 项（无 report 返回 None、单文件结构 DOCTYPE→</html> 且零 script/零外链、图表+表格+时间线渲染、XSS 转义 img/onerror、无 findings 与空收敛与空时间线占位、时间线 50 条上限、CLI --html 默认路径写入与缺报告不落文件、slash report --html 写文件）+ test_replay.py 10 项（空日志友好、相对偏移 0/90/300s 与摘要键探测、坏时间戳降级、未知类型 JSON 预览、空载荷占位、500 字符截断、render 拼接、slash 与 CLI --replay 双入口、CLI 空日志）+ test_dimension_resources.py 12 项（parse 全字段/钳位/非法类型计数/非映射根、load_effective_config 读 yaml、validate_config 报错与放行、plan 携带 resources+prompt 指令+无资源维度无指令、plan_to_dict 序列化与省略、默认配置全 None、/iterate config 展示）。**版本与验证**：版本 1.0.0 对齐（pyproject / cli __version__ / CHANGELOG 1.0.0 条目 / README badge 双语）；README 双语特性表增「HTML 单文件报告」「评审回放」「per-dimension 资源」三行、CLI 速览补 `log --replay`/`report --html`；tests/test_iterate 294 全绿（261+11+10+12），全仓回归 1212 passed + 6 skipped（3 失败均为 v1.13 已记录沙箱环境性：MCP stdio 真连接、插件安装流、bash 超时部分输出，无回归）；本轮触碰文件（html_report/replay/config_loader/review/types/commands/iterate/cli 局部 + 三个新测试文件）ruff 全过（cli.py 既有 lint 基线未动）；CLI 直接函数调用测试显式传全部 typer 参数（OptionInfo truthy 陷阱修复）。**残留说明**：per-dimension 资源的 token_budget 目前为计划层声明（随 prompt 派发），引擎级按维度 token 硬预算（cost tracker 按维度切分）与维度级阈值门禁（max_critical/max_high 对接 PR 门禁）留待 1.1；cron 仍全 UTC。
- v1.19（2026-08-15）：1.1.0「策略层」落地，v1.18 残留的三项全部闭合——**① 整轮 token 预算引擎级强制**：`iterate.config.yaml` 新增顶层 `token_budget`（正整数，`parse_token_budget` 防御解析：bool/非正/非整数记入 validate_config 错误并跳过，绝不致命）；`query_engine._default_iterate_policy` 将其注入 `IterateLoopPolicy.total_token_budget`；`loop_policy.on_turn_end` 在 cost_meter 累加后**先于**聚合快照判定 `_budget_stop_reason`（`used > budget` 即返回 `token budget exhausted (used/budget tokens)` 停止决策——预算强制不依赖本轮是否有新 aggregate，无快照时构造默认快照走停止路径并携带 progress）。**② per-dimension 预算审计**：review.py 新增 `BudgetAudit`/`audit_dimension_budgets`（纯函数：只审计配置了预算的维度，used 防御钳位 ≥0，未报告维度计 0；`all_budgeted_exhausted` 仅当全部预算维度超限）；入口 `IterateReviewInput.dimension_usage`（aggregate 操作可选字段），`iterate_tools._audit_budgets` 读取生效配置中带 `token_budget` 的 `dimension_resources` 比对（bool 值剔除、max(0,int) 归一），审计结果双通道输出：payload 增 `budgetAudit` 块（dimension/budget/used/remaining/exceeded 行）+ loop-policy state 增 `exhausted_dimensions`/`all_dimensions_exhausted`；`loop_policy` 消费：全部超限→停止（reason 列出维度），部分超限→`next_round_instruction` 追加「Token budgets are EXHAUSTED for: …— do NOT spawn reviewer agents for these dimensions this round」显式派发指令（prompts.py 新增 exhausted_dimensions 参数）；审计异常绝不破坏聚合（无预算/无上报时省略整块）。**③ 维度阈值门禁**：types.py 新增 `DimensionThresholds`（max_critical/max_high 可选）与 `ThresholdsConfig`（全局 + dimensions 字典，`is_empty()`）；config_loader 新增 `parse_thresholds`（防御解析：负数/bool/非整数/非映射逐条记错跳过）/`thresholds_to_dict`（仅序列化已设字段）/validate_config 集成；review.py 新增 `ThresholdGateResult`/`evaluate_threshold_gates`（纯函数：global 与 `dimension:<dim>` 两级 scope，`actual > limit` 才违规，violation 形如 {scope,metric,limit,actual}）；`iterate_tools._meta_review` 读取项目 thresholds 评估后传入 `meta_review.build_final_review_report(threshold_result=…)`——失败门禁逐违规折叠 `THRESHOLD_EXCEEDED`（severity=high）meta-review issue 并把 verdict 翻转为 needs_revision，finalReport 携 `thresholdGate` 块（未配置 thresholds 时省略）；canonical-loop prompt（prompts.py 步骤 6）指示模型把 thresholdGate 原样复制进唯一 report 条目；CI 闭环：ci_report 新增 `threshold_gate(entry)`（防御提取 report 条目 thresholdGate 块）/`threshold_exit_code`（present∧failed→1）/`render_text` 增门禁状态行（`threshold gate: PASS/FAIL`，违规内联 `scope:metric actual>limit` 最多 5 条 + `(+N more)`）；CLI `oh iterate report` 退出码 = max(severity_gate, threshold_exit_code)。**④ cron 本地时区**：cron.py 新增 `validate_timezone`（ZoneInfo 探测，容忍首尾空白，Unknown/ValueError/KeyError 均 False）；`next_run_time` 增 tz_name 参数——表达式在 IANA 区本地时间求值后 `astimezone(utc)` 归一化存储（09:00 Asia/Shanghai → 01:00 UTC），未知区 raise ValueError；`_recompute_next_run` 统一 upsert/mark_job_run 两处重算路径（存储的未知区回退 UTC 容错旧条目）；`install_schedule` 增 timezone 参数（安装时校验，无效 raise ValueError），job 携 `timezone` 键；CLI `schedule add --timezone`（空串→None 兼容 typer）；scheduler due 判定不变（比对 UTC 归一化 next_run）。**测试**：新增 test_budget_thresholds.py 28 项（audit：预算内/超限/部分 vs 全部超限/无预算/未上报计 0/负数钳位/to_dict；gates：空配置通过/critical 超限/恰等 limit 通过/high 超限/per-dimension 只计本维度/未配置维度无门禁/多违规全报；config：token_budget 合法非法集/thresholds 往返/非法逐条记错/非映射拒绝/None 默认；meta 折叠：失败门禁翻转 verdict+issue/通过保持；loop policy：整轮预算停止/预算内继续/无快照仍停止/全维度超限停止/部分超限注入指令/prompt 列出维度）+ test_ci_report.py 增 9 项（threshold_gate 提取/缺失畸形 None/exit_code 三态/render 门禁行 FAIL 含双违规/PASS/5 条封顶(+2 more)/CLI 低严重度+失败门禁退出 1/通过门禁退出 0）+ test_batch_schedule.py 增 TestScheduleTimezone 9 项（validate_timezone 合法非法集/本地求值 09:00 上海→01:00 UTC/无区保持 UTC/未知区 raise/install 拒绝未知区/存储携 timezone 且 next_run +00:00/无区省略键/mark_job_run 重算仍 UTC 归一/_jobs_due 在 01:00 UTC 判到期）+ test_iterate_tools.py 增 5 项（aggregate dimension_usage 出 budgetAudit+state 超限维度/无预算省略/meta-review 配置 thresholds 出 thresholdGate 翻转 verdict+THRESHOLD_EXCEEDED/未配置省略）。**版本与验证**：版本 1.1.0 对齐（pyproject / cli __version__ / CHANGELOG 1.1.0 条目 / README badge 双语）；README 双语特性表增「token 预算强制」「阈值门禁」「定时评审时区」三行；tests/test_iterate 343 全绿（294+49），全仓回归 1261 passed + 6 skipped（3 失败 + test_http_flow collection error 均为 v1.13 已记录沙箱环境性，无回归）；触碰文件 ruff 全过。**残留说明**：dimension_usage 依赖 reviewer 上报（prompt 指令通道），引擎未按维度切分 cost meter（后续可在 agent 工具层回传真实 usage）；阈值门禁指标暂只有 max_critical/max_high，可按需扩展 medium/low 或自定义 metric。
- v1.20（2026-08-15）：1.2.0「日常驾驶人机工程」落地，v1.19 残留的引擎级 per-dimension usage 回传闭合 + §11.2.1 看类「init 检测式向导」与跑类「git hook：commit 前 30 秒 changed-only 快审」两项补全——**① 检测式 init 向导（§11.2.1 看类最后一项）**：新模块 `iterate/init_wizard.py`（纯函数 + 防御解析）：`detect_project` 探测 11 种标记文件（package.json/pyproject.toml/setup.py/requirements.txt/go.mod/Cargo.toml/Gemfile/pom.xml/build.gradle(.kts)/composer.json）按语言去重推断栈（node/python/go/rust/ruby/java/php）；测试命令**只来自显式证据**（真实 `scripts.test` 条目→`npm test`、pyproject 含 pytest→`pytest -q`、tests/ 布局兜底、go.mod→`go test ./...` 等），未知栈绝不发明可信命令；前端框架依赖（react/vue/svelte/next/nuxt/@angular/core）解锁 `frontend-backend`/`ui-ux` 维度；畸形 package.json 降级为 evidence 注记不 raise。`build_config_dict`/`render_config_text` 经 `yaml.safe_dump` 序列化（goal 文本不可注入 yaml 结构），头部注释标注 commands 精确匹配语义；`parse_dimension_selection` 支持序号/名称混选（`2,4`/`security ui_ux`，下划线归一，越界/未知返回 None 重询）；`write_config` 确认后才落盘。入口：CLI `oh iterate init [--yes/-y] [--force] [--goal]`（evidence 逐行打印 + yaml 预览 + 确认写入；存在配置无 --force 拒绝）与 slash `/iterate init [--force]`（TUI 内同效，预览后直接写入并提示下一步）。**同日修复**：替换 v1.12 遗留的旧 marker-lite `init` 命令（删除 `_ITERATE_DIMENSIONS`/`_detect_project`/`_has_script`/`_render_config_yaml` 及旧命令体，消除 F811 重复定义与 cli.py 一处 f-string 语法错误——该错误此前已阻断 test_ci_report 收集）。**② 托管 pre-commit 钩子（§11.2.1 跑类最后一项）**：新模块 `iterate/git_hook.py`：`install_hook` 经 `git rev-parse --show-toplevel` 解析仓根（子目录调用正确归位；非 git 仓 raise HookError），写 MARKED（`# iterate-harness pre-commit hook`）`.git/hooks/pre-commit`（0755）——对已存在且无标记的第三方钩子（husky 等）**拒绝覆盖**，仅可替换自家托管钩子；`--fail-on` 白名单校验（none|low|medium|high|critical，默认 high）；生成脚本为纯 POSIX sh（`sh -n` 语法校验入测试）：ITERATE_SKIP_HOOK=1 短路 → 绝对路径 `oh`（安装期 `shutil.which` 解析，钩子环境常缺用户 PATH）跑 `iterate review --changed --clean-ok --ref HEAD --rounds 1`（单轮快审）→ `exec oh iterate report --fail-on <sev>`（复用 CI 退出码门禁，commit 按严重度放行/阻断；`git commit --no-verify` 原生跳过）；`uninstall_hook` 同样拒绝摘除外来钩子、缺席幂等返回 False；`hook_status` 输出 installed/managed/path/skippable（非 git 仓降级 error 字段不 raise）。CLI `oh iterate hook install|uninstall|status`（typer 子应用挂 iterate_app）。**③ 引擎级 per-dimension usage 回传（v1.19 残留①闭合）**：`iterate_tools._aggregate` 把消毒后的 `dimension_usage`（bool 剔除、max(0,int) 钳位）发布进 loop-policy state（与 budgetAudit 独立——无预算配置也回传）；`AggregateSnapshot` 增 `dimension_usage` 字段、`read_state` 防御解析（非映射/非整数值条目丢弃）；`IterateLoopPolicy.on_turn_end` 在正常轮与预算停止两条路径均经 `_record_dimension_usage` 将各维度累计值中继进 `CostMeter.record_dimension_total`（**单调 max** 语义——aggregate 上报的是 running total，取 max 绝不累加重复计数），`format_summary()` 按维度输出「dimension X: N tokens (reviewer-reported)」；维度上报**不进** total_tokens/total_cost_usd（主循环口径不被子代理污染）。**测试**：新增 test_init_wizard.py 18 项（node 检测 test 脚本+react 解锁/畸形 package.json 降级、python pyproject/布局兜底、go/rust/java/php 四标记、多 python 标记去重、未知栈 base 维度、build_config 含/不含 validation、yaml 注入安全（goal 恶意文本保持标量）、写盘经 load_effective_config 往返、选择解析空保全部/序号名称/下划线归一/去重保序/越界未知 None 参数化）+ test_git_hook.py 16 项（渲染含守卫/二进制/门禁、`sh -n` 语法、单轮常量、安装写 0755 托管钩子、替换自家、拒绝外来、拒绝非法严重度、非 git 仓拒、卸载移除/缺席 False/拒外来、status 三态、子目录解析；PATH 注入 autouse fixture 兼容沙箱）+ test_loop_policy.py 增 TestDimensionUsageRelay 5 项（新聚合记录/running total 单调 max/重复聚合不双计/预算停止路径仍记录/不污染主循环 total_tokens）+ test_iterate_tools.py 增 2 项（无预算也发布 dimension_usage/负值钳位）。**版本与验证**：版本 1.2.0 对齐（pyproject / cli __version__ / CHANGELOG 1.2.0 条目 / README badge 双语）；README 双语特性表增「检测式 init」「pre-commit 钩子」两行、token 预算行补 usage 回传描述、CLI 速览补 `hook install`；tests/test_iterate 383 全绿（343+40），全仓回归 1286 passed + 6 skipped（2 失败为 v1.13 已记录沙箱环境性：插件安装流、bash 超时部分输出，无回归；test_http_flow collection error 同为既有 venv mcp 包问题，--ignore 验证）；触碰文件 ruff 全过（cli.py 既有 lint 基线 18 条未动，全部为上游风格存量）。**残留说明**：per-dimension usage 仍是 reviewer 上报口径（agent 工具层数据，非 API 计费口径），金额未按维度折算 USD（后续可将 dimension_tokens × 对应模型价格入 meter）；init 向导 java/ruby/php 的测试命令为约定建议（evidence 注记提示按 gradle/rspec/phpunit 调整）；钩子单轮评审仍受 review 全链路时长影响（30 秒目标依赖模型响应速度，--fail-on=none 可退化为纯记录）。
- v1.21（2026-08-15）：1.3.0「CI 可见性」落地，v1.19/v1.20 三项残留全部闭合——**① PR 评论模式（`oh iterate report --pr`）**：新模块 `iterate/pr_comment.py`：`render_markdown(summary, gate)` 把最终报告渲染为 Markdown PR 评论（隐藏 marker `<!-- iterate-report -->` 锚定、表头 mode/verdict/findings、findings 表格 50 行封顶 + 截断行、单元格管道/换行转义、threshold gate PASS ✅/FAIL ❌ 状态行 + 违规内联至多 5 条）；`post_pr_comment(body, cwd, *, runner)` 经 gh CLI 五步流：`gh pr view --json number`（非零退出→no-pull-request 降级）→ `gh repo view --json nameWithOwner` → `gh api repos/{repo}/issues/{n}/comments?per_page=100` 列评论按 marker 反向找自家最新评论 id → 命中则 `gh api -X PATCH …/issues/comments/{id} --input -`（幂等更新，绝不每轮 CI 刷屏）→ 未命中则 POST 创建；body 经 stdin JSON（`json.dumps({"body": …})`）传递，全程 60s 超时；**失败全降级不 raise**（gh 未装/非 PR 上下文/认证缺失/API 失败/超时 → PostResult("skipped", detail)），`--fail-on` 退出码语义零影响；进程边界收敛为单一可注入 runner（`(args, cwd, input_text) -> CompletedProcess`），模块完全可单测。CLI `--pr` 与 `--github` 可组合（批注+评论并行），单 `--pr` 抑制纯文本渲染，结果状态打 stderr。**② 阈值门禁扩展 max_medium/max_low（v1.19 残留闭合）**：types.py 新增 `SEVERITY_METRICS = ("critical","high","medium","low")` 单一事实源；`DimensionThresholds`/`ThresholdsConfig` 各增 max_medium/max_low，`is_empty()` 泛化为遍历元组；config_loader 解析重构为 `_parse_threshold_metric`（per-field 防御解析）+ 字典推导（全局与维度共用），`thresholds_to_dict` 同步泛化——后续新增指标只需改元组一行；review.py `evaluate_threshold_gates` 重构为 `_check_scope`（单 scope 内计数 4 档 severity 精确匹配 + 逐 metric 比对），global 与 dimension 两级复用同一路径；语义保持「各档只计该档数量」（与 v1.19 实现一致），yaml 往返序列化对称。**③ per-dimension USD 折算（v1.20 残留闭合）**：`CostMeter.dimension_cost_usd(model)` 把 reviewer 上报的维度累计 tokens × 模型混合价 ((input+output)/2) 折算为估算 USD（无 in/out 拆分下的诚实估计，round 6 位）；估算**不并入** total_cost_usd/total_tokens（主循环计费口径不被上报口径污染）；`format_summary(dimension_model=…)` 维度行附加 `(~$X.XXXX)` 估算，不传参保持 v1.2 输出不变。**测试**：新增 test_pr_comment.py 24 项（render：marker 锚定/表头表格/空占位/管道换行转义/50 行截断/缺文件占位/gate PASS/FAIL+违规/违规 5 条封顶；post：无 marker 拒/gh 未装/超时/非 PR/PR 号不可解析/repo view 失败/列评论失败/坏 JSON/创建路径验证 stdin payload/更新路径验证 PATCH id/POST 失败/PATCH 失败；CLI：--pr 发帖抑制文本/--pr 无 gh 降级退出 0/--pr+--github 组合）+ test_budget_thresholds.py 扩展（global medium 超限/global low 超限/medium 只计 medium/维度级 medium+low，roundtrip 覆盖 4 字段，非法计数 4+2+1=7 条）+ test_loop_policy.py 增 TestDimensionCostUsd 5 项（混合价计算/价格 override/空上报/不并入总成本/format_summary 两形态）。**版本与验证**：版本 1.3.0 对齐（pyproject / cli __version__ / CHANGELOG 1.3.0 条目 / README badge 双语）；README 双语 CI/PR 行补 `--pr` 幂等评论描述、阈值门禁行列全 4 档、token 预算行补维度 USD 估算、CLI 速览补 `report --pr`；tests/test_iterate 415 全绿（383+32），全仓回归见 CI 记录；触碰文件 ruff 全过（新模块零告警）。**残留说明**：PR 评论查找按 `per_page=100` 单页（超 100 条评论的巨型 PR 可能漏检 marker → 退化创建新评论，非错误路径）；per-dimension USD 仍为 reviewer 上报口径的混合价估算（非 API 计费口径），TUI 收敛面板尚未展示分维度金额（meter API 已就绪，v2 候选接入）。
- v1.22（2026-08-15）：1.4.0「品牌迁移 + 生态引流」落地，fork 身份从分发名贯穿到包名/命令/路径——**① openharness → iterate_harness 全量迁移**：`git mv src/openharness src/iterate_harness` + 脚本化替换 289 个文件（271 个 py 的 1832 处 import/模块路径字符串 + 文档/脚本/frontend 清单），替换链顺序敏感（`.openharness`→`.iterate-harness` 磁盘路径先行 → 裸 `openharness`→`iterate_harness` 标识符 → `OpenHarness`→`IterateHarness` 类名与文案 → 正则 `\boh\b`→`ih` 命令引用）。**② CLI 入口更换**：pyproject `[project.scripts]` 从 openharness/oh/openh/iterate-harness 四入口收敛为 `ih`（短）+ `iterate-harness`（全名），`python -m iterate_harness` 可用；git_hook `shutil.which("ih")`、autopilot 提示、registry/cli/auth 用户可见文案、install.sh/ps1/dev 三脚本 launcher 链接段（`IH_VERSION` 变量名同步）全部指向 ih。**③ 数据目录迁移**：`~/.openharness/`→`~/.iterate-harness/`（sessions/settings/themes/plugins/worktrees/teams/copilot_auth），项目级 `.openharness/`→`.iterate-harness/`，hatch exclude 与 wheel/force-include 映射同步新包布局；frontend workspace `@openharness/terminal`→`@iterate-harness/terminal`（package.json + lockfile name 字段）。**④ 文档与 bundled skill**：README 双语 CLI 速览/特性表全量 oh→ih、CONTRIBUTING/SHOWCASE 品牌词迁移（上游 HKUDS/OpenHarness fork 声明与链接按用户规则保留）；bundled skill-creator.md 品牌词迁移 + ohmo 残留清理（`ih/ohmo`→`ih`、`~/.ohmo/skills` 行删除、`from ohmo.workspace import` 验证代码块删除——fork 后无此模块）；CHANGELOG/RELEASE_NOTES 历史条目**保留 oh 原文**（记录当时事实），1.4.0 条目含 Upgrade Notes（重装生成 ih 入口/旧 oh shim 可删、≤1.3.0 托管 pre-commit 钩子内嵌旧绝对路径需 uninstall+install 重渲染、schedule 任务存 PATH 解析的命令字符串需重注册——经核实 build_scheduled_command 产物修正初稿不实表述、旧 `~/.openharness` 数据不自动迁移）。**⑤ 测试对齐**：test_windows_alias 断言重写（`scripts["ih"]`/`scripts["iterate-harness"]` 正断言 + oh/openh/openharness 负断言）；test_skills loader 断言随 bundled 品牌迁移自然通过；cli.py 因包名字母序变化新增 1 个 I001 经 `--select I001 --fix` 修复（顺手清掉 3 个存量 I001）。**⑥ 主仓库 README 生态引流**：新增「生态 / Ecosystem」段（At a Glance 与 Quick Start 之间）——iterate-harness（ih 无头引擎：CI/PR/钩子/定时/报告/门禁）与 iterate-plugin（dsh 桌面插件：收敛仪表盘/进度/Esc 干预）双卡片表格 + 一键安装命令 + 三者关系说明（skill 面向对话式助手、harness 面向无头/CI、plugin 接入 dsh，iterate.config.yaml 与维度体系三者一致）。**版本与验证**：版本 1.4.0 对齐（pyproject / cli __version__ / CHANGELOG 1.4.0 / README badge 双语）；tests/test_iterate 415 全绿，全仓 1336 passed + 6 skipped（3 失败为 v1.13 已记录沙箱环境性，无回归）；iterate/cli/test_iterate 范围 ruff 零新增（cli.py 基线 18 条存量未动）。**迭代计划校准（定位重申）**：本项目是**专门用于 iterate 的 coding harness**——不追求通用 agent harness 的全能力面，迭代始终围绕原 skill 的设计目标（多轮审查-修复闭环、9 维度体系、双轨修复、secure-by-default、项目知识库）在 skill 与 dsh 插件基础上增强 iterate 的实现效果；v2 候选按此定位排序：harness kickoff 注入 ITERATE.md 知识库摘要（当前只读 iterate.config.yaml，未消费 skill onboarding 产出的项目知识资产）、TUI 收敛面板分维度 USD 展示（v1.21 残留）、skill↔harness 维度体系一致性校验命令。
- v1.23（2026-08-15）：1.5.0「完整 onboarding 对等」落地，harness 补齐 skill 的 ITERATE.md 知识库链路（用户定位重申：iterate 专用 harness 必须实现 skill 的全部设计目标，知识库是核心 agent 上下文）。基于对主仓库 skill onboarding 体系（SKILL.md Step 0 + iterate_cli 五命令 + ITERATE.template.md 四标记 + fingerprint SHA-256 漂移）与 harness 现状（init_wizard 纯检测不调模型、auth 未配置直接 SystemExit、ITERATE.md 不进系统提示）的双向调研，新增三个模块 + 五处接线：① iterate/onboarding.py（核心原语）：15 种 manifest 的 SHA-256 指纹采集（capture/compare/check，ignore 双侧过滤防 spurious removed）、DriftResult 四分类、与 skill 字节一致的四个区域标记常量、validate_iterate_md 标记完整性/顺序校验、extract/replace_user_owned_section 用户区逐字保留、update_completed_at_in_md 元信息行级刷新、build_onboarding_section 生成 schema 兼容的 config onboarding 段。② iterate/data/ITERATE.template.md：打包进 wheel 的知识库骨架（元信息表 + AI 维护区五节 + 用户维护区三节，10 个占位符），双路径复用——模型 kickoff 内嵌骨架 + --no-ai 检测渲染。③ iterate/onboard_cmd.py（编排）：run_onboard（auth 门禁→检测证据→维度/goal/轮数问答→模型扫描（run_print_mode full_auto 流式）→标记校验（失败不写 config）→harness 侧采集指纹并 safe_dump 写 config；--no-ai 降级渲染 channel=cli，模型路径 channel=ai）、run_refresh（重采指纹+漂移报告+config/元信息刷新，写失败回滚，不动用户区不调模型）、run_reonboard（.bak-<ts> 双备份→旧用户区嵌入 kickoff 逐字保留→失败自动回滚）、render_status_onboarding_lines、warn_if_drifted。④ kickoff 模板（prompts.py）：onboarding_kickoff 内嵌扫描清单 + skill frontmatter 同源敏感文件拒绝清单 + 完整骨架 + 字节精确标记要求 + RE-ONBOARD MODE 用户区原样保留子句。⑤ 五处接线：cli.py 注册 ih iterate onboard/refresh/reonboard/status 四命令（status=配置概要+onboarding 状态+漂移；review/run 经 _run_headless 统一挂非阻塞漂移警告）；commands/iterate.py（TUI）新增 /iterate onboard（当前会话内提交 kickoff，无嵌套 runtime，完成提示跑 ih iterate refresh 补指纹）、status/config 追加 onboarding 块、review/run 起始消息附漂移提示；prompts/context.py 的 build_runtime_system_prompt 注入 ITERATE.md 摘要（从 cwd 向上查找与 iterate_context 同规则、4000 字符截断、指引完整内容走 iterate_context）——闭合 v1.22 记录的“kickoff 未消费知识库”缺口。信任边界设计：模型只写 ITERATE.md（不可信文本，标记校验把关）；config（含指纹/onboarding 段）永远由 harness 代码 yaml.safe_dump 序列化。产物互操作：标记与 onboarding.fingerprints schema 与 skill 字节兼容，channel 枚举沿用（ai/cli），两生态互相可读。验证：新增 tests/test_iterate/test_onboarding.py 46 项（指纹/漂移/标记操作/config 段/kickoff/检测渲染/onboard e2e 含模型失败路径/refresh/reonboard 备份回滚/status/警告/context 注入/TUI handler）；test_iterate+test_commands 529 全绿；真实 smoke（/tmp 项目）：onboard --no-ai→status 显示 channel/fingerprints/no drift→改 package.json→status 报 DRIFTED→refresh 修复→status 恢复 no drift；版本 1.5.0 对齐（pyproject/cli __version__/双语 README badge）；ruff 触碰文件零新增（context.py 7 条存量与 HEAD 持平）。遗留说明：TUI /iterate onboard 完成后指纹需终端跑 ih iterate refresh 补录（避免 TUI 内嵌套 runtime；v2 候选：turn-end 钩子自动补录）；/iterate personalize 9 步个性化向导尚未对等（v2 候选）。
- v1.24（2026-08-15）：1.6.0「个性化对等 + onboarding 指纹自动补录」落地，v1.23 两项遗留全部闭合——**① `ih iterate personalize` 9 类个性化向导（v1.23 遗留②闭合）**：新模块 `iterate/personalize_cmd.py`：`PersonalizationData` 数据类对齐 skill 9 类（结构化 7 类：protected_paths/risk_areas/known_intentional/dimension_focus/fix_priority_order/forbidden_fixes/extra_validation_commands + 自由文本 2 类：iterate_notes/code_conventions）；向导 run_personalize_wizard 支持 a/r/s 逐条增删、9 维度编号选择（与 ALL_DIMENSIONS 对齐）、fix_priority 逗号序号重排 + 确认；可重复运行编辑既有配置（config 结构化字段 + ITERATE.md 自由文本双源回读 preload）。**双写设计**：结构化类别经 merge_personalization_into_config 写入 config `personalization` 段（version 字段携 PERSONALIZATION_VERSION），extra_validation_commands 先过 skill 同源严格白名单 validate_extra_command（禁 shell 元字符 + 允许工具前缀 + ITERATE_EXTRA_SAFE_PREFIXES 环境变量扩展）再合并进 validation.commands 并补 command_whitelist 前缀（schema 校验永不因外部输入失败）；自由文本经 merge_user_sections 以**精确头匹配**替换向导生成节（用户手写节逐字保留，带后缀的变体头视为手工节不动）；load_personalization_from_config 防御解析（接受完整 config 或裸 personalization 段、字符串列表仅留非空 str、known_intentional/extra_commands 容错解析）。**② 内核级禁区强制**：permissions/checker.py `build_permission_checker` 除 Settings.iterate.protected_paths 外，把当前项目 config 的 `personalization.protected_paths` 也归一化为绝对路径 deny 规则合并进权限层（向导配置的禁区成为硬边界而非仅提示词约束；config 不可读时贡献零规则、绝不 crash 权限装配）。**③ kickoff 约束注入**：prompts.py `personalization_constraints` 生成约束块（禁区/风险区/禁止修复方式/优先顺序/维度 focus/已知意图计数），review/run kickoff 追加——每次闭环从项目专属规则开场。**④ TUI onboarding 指纹自动补录（v1.23 遗留①闭合）**：onboard_cmd.py `ensure_onboarding_fingerprints`：ITERATE.md 存在而 config 无 onboarding.fingerprints（TUI /iterate onboard 路径——slash 流无法执行 CLI 同步后扫）时，下一次 review/run/漂移检查自动补全 config onboarding 段（harness 侧序列化，模型不触可信 config）；用户无需手动 `ih iterate refresh`。CLI 与 /iterate 双入口：cli.py `ih iterate personalize`（onboard 门禁 + 向导 + 双写 + 完成摘要）、commands/iterate.py `/iterate personalize`（当前个性化摘要 + 指向 CLI 向导）。**测试**：新增 tests/test_iterate/test_personalize_cmd.py 38 项（白名单严格集参数化/config 往返与防御解析/merge 保留 goal 合并 validation/保存缺 config raise/用户区合并含手工节保留与精确头匹配/向导全脚本 e2e（含 curl evil.sh 白名单拒绝可见）/取消返回 None/e2e 双写 + 手工节存活/ensure_onboarding_fingerprints 补录一次与缺件不动作）；tests/test_iterate 499 全绿（461+38），全仓回归 1412 passed + 6 skipped（5-8 处失败两次运行集合漂移，均为 v1.13 已记录沙箱子进程环境性：engine subagent hook/mcp stdio/plugin 生命周期/bash 超时/task 轮询，无逻辑回归）；新文件 ruff 零告警（onboard_cmd/onboarding/checker 存量基线未动）。**版本与验证**：版本 1.6.0 对齐（pyproject / cli __version__ / CHANGELOG 1.6.0 / 双语 README badge）；README 双语特性表增「个性化向导」行、onboarding 行补 TUI 指纹自动补录、CLI 速览补 `personalize`。**遗留说明**：向导为 CLI 交互式（TUI 内 /iterate personalize 仅摘要 + 指引，方向键化向导为 v2 候选）；protected_paths 内核合并基于进程 cwd（多根会话以启动目录为准）。
- v1.25（2026-08-15）：1.6.0「npm 分发包装」落地——harness 以 npm 包 `iterate-harness` 发布，作为最简下载方式（`npm install -g iterate-harness` → `ih` 即用）。**技术选型**：纯 Python harness 不重写为 JS，采用**薄包装器**模式：npm 包只含 Node shim（零依赖），首次运行时把 harness 发布 tarball pip 安装进托管 venv 后委托真实 `ih`。可行性依据（源码级核实）：wheel 经 hatch force-include 内置 `iterate_harness/_frontend`（react_launcher.get_frontend_dir 第一优先级命中），且 launch_react_tui 在 node_modules 缺失时自动 `npm install`——**非 editable 的 pip install 自洽**，React TUI 在 npm 用户侧必然可用（npm 用户必有 Node）。**包装器实现**（主仓库新目录 `npm/iterate-harness/`，从主仓库直接 `npm publish`）：lib/bootstrap.js 核心链路——python 探测（ITERATE_HARNESS_PYTHON 覆盖 → win `py -3`/posix `python3` 优先，解析 `Python x.y.z` 且 >= 3.10）→ venv 建立于 `~/.iterate-harness-npm/venv`（ITERATE_HARNESS_NPM_HOME 覆盖；残缺 venv 自动重建）→ `pip install --upgrade --force-reinstall <github archive/refs/tags/v<version>.tar.gz>`（ITERATE_HARNESS_INSTALL_URL 可覆盖为 git ref 供测试）→ version.stamp 落盘；bin/ih.js + bin/iterate-harness.js 双入口 spawn venv 内 ih（stdio inherit、SIGINT/SIGTERM 转发、退出码透传）。**版本锁步**：包装器 package.json version == harness 版本 == 安装 tag（1.6.0 → v1.6.0）；npm 升级后 stamp 不匹配 → 下次运行自愈重装到新 tag。环境逃生门：ITERATE_HARNESS_SKIP_INSTALL=1 直接运行已装 ih。**测试**：test/bootstrap.test.js 10 项（node --test，覆盖纯函数：版本解析/3.10 门槛/候选序含 env 覆盖与 py -3/venv 双平台路径/tarball URL 锁定/installUrl 覆盖优先/stamp 空白容忍与精确匹配/env 常量名稳定）。**发布流程固化**：主仓库 commit → subtree push harness 仓库 → harness 仓库打 tag v<version>（tarball 锚点）→ GitHub Release → 本地 `node bin/iterate-harness.js --version` e2e（从 tag 真实引导）→ `npm publish npm/iterate-harness`。**文档**：harness README 双语 Install 段增 npm 首选行、CHANGELOG 1.6.0 增 Distribution 小节、主仓库 README 生态段表格补 npm 标注 + 安装命令块 npm 化。**边界说明**：包装器不进 harness 仓库 subtree（主仓库为 npm 维护点，与 iterate-plugin 独立仓库模式区分——后者因 dsh 插件需独立 repo 元数据）；PyPI 发布为另一条可选分发线（未纳入本轮，pip 用户暂走 install.sh / git）。
- v1.26（2026-08-15）：1.7.0「精确计费 + 巨型 PR 分页 + 品牌清理」落地，v1.21 记录的三项残留全部闭合——**① PR 评论查找分页化（残留①闭合）**：`pr_comment._find_marker_comment` 从单页 `per_page=100` 改为分页扫描——`COMMENTS_PER_PAGE=100`、`MAX_COMMENT_PAGES=10` 防御上限两常量，循环逐页 `gh api …&page=N`，`_marker_id_in_page` 辅助提取当页 marker id；页按时间序、最高页 marker 胜出、末页短页（<100 条）即停；超 100 条评论的巨型 PR 幂等更新路径不再因漏检 marker 而退化创建新评论。**② per-dimension in/out 精确计价（残留②闭合）**：`CostMeter` 新增 `_dimension_io` 存储 + `record_dimension_usage(dimension, input_tokens, output_tokens)`（与 bare totals 同纪律的单调 max 防重复计数）；`dimension_cost_usd` 优先按 split 精确计价（in×input_price + out×output_price），无 split 维度回退混合价估算；`iterate_review` aggregate 工具 schema 增可选 `dimension_usage_io`（形如 `{"security": {"input": 1000, "output": 500}}`），`_clean_dimension_usage_io` 防御清洗（畸形条目丢弃不 raise、全零条目剔除），split 上报同时喂维度 token 预算审计（无 bare totals 也可审计）；loop_policy 解析 state `dimension_usage_io` 并转发 CostMeter，split 报告的维度总额按「每报 in+out 之和的 max」记账。**③ TUI 收敛面板分维度 USD（残留③闭合）**：`ReviewProgressEvent` 增 `dimension_cost_usd: dict[str, float]`，全链路：loop_policy → 协议 `review_dimension_cost_usd` → backend_host 转发 → 前端 types/useBackendSession(`dimensionCostUsd`)/ReviewProgressPanel 渲染 `security 3 ~$0.0210` 式分维度估算（有 reviewer usage 上报时展示，头部保留主循环 metered 总额）；print 模式 app.py 同步输出。**④ 品牌清理**：README 双语删除继承自 OpenHarness 的马头 logo（`assets/logo.png` 删除，fork 不再携带上游品牌素材，商标卫生）；quickstart 首选 `npm install -g iterate-harness`（35efece）。**测试**：test_pr_comment.py 分页用例（多页 marker 命中/末页短页/超 10 页封顶）+ test_loop_policy.py split 计价用例（精确价/单调性/回退混合价/全零剔除）+ test_iterate_tools.py `dimension_usage_io` schema 与清洗用例；tests/test_iterate 514 全绿（499+15）；全仓回归 1429 passed + 6 skipped（3 失败为 v1.13 已记录沙箱环境性：mcp stdio/plugin lifecycle/bash 超时；另 test_install 3 项为从仓库根运行 pytest 的 cwd 相对路径假象，harness 目录下 3/3 通过，非回归）；触碰文件 ruff 零新增（29 条存量与 HEAD 完全一致）；前端 `tsc --noEmit` 零错误。**版本与验证**：1.7.0 对齐（pyproject / cli `__version__` / CHANGELOG 1.7.0 / README badge 双语）。
- v1.27（2026-08-15）：1.8.0「维度体系一致性 doctor」落地，v1.22 记录的最后一个 v2 候选闭合（另两项已于 v1.23 知识库注入 / v1.26 分维度 USD 各自闭合）——9 个审查维度在两仓共 6 处定义（canonical yaml / schema enum / skill wizard 常量 / harness ALL_DIMENSIONS / harness 默认配置 / 各项目 config 引用），任何一处都可能在改名/增删时漂移；本轮把 canonical 收编进 harness 并双仓上锁。**① 数据收编**：`iterate/data/dimensions.yaml` 打包进 wheel（与 skill `config/dimensions.yaml` 字节一致，SHA256 校验；hatch 包目录默认含非 py 文件，与既有 ITERATE.template.md 同机制）。**② 新模块 `iterate/dimension_check.py`**（纯函数 + 防御式，绝不 raise）：`load_canonical_dimensions` 防御解析（文件缺失/坏 yaml/非映射根/缺 name/name_en/priority/focus 字段/非法 priority 逐条记错）；`run_dimension_doctor` 三层检查——内部一致性（`personalize_cmd.ALL_DIMENSIONS` 顺序+集合 vs canonical、`IterateConfig().dimensions` 集合 vs canonical）→ 项目 config 四类引用（enabled dimensions 未知键=错误如 `securty` 手民；`dimension_resources`/`thresholds.dimensions` 键未知=错误、canonical 但未启用=惰性 warning；personalization 三引用 `fix_priority_order`/`dimension_focus`/`known_intentional` 超出启用集=错误，镜像 skill `scripts/validate.py` 语义）→ canonical 未启用维度记为 informational（项目选子集是正常用法）；`render_doctor_report` 输出 ✓/✗/⚠ 三态行 + OK/FAIL verdict。**③ 双入口**：CLI `ih iterate doctor`（漂移退出码 1，可做 CI 门禁）+ TUI `/iterate doctor`（同一渲染）；usage 帮助同步。**④ 主仓库 6 源一致性锁测试 `tests/test_dimension_lock.py`**（AST/regex/json 零第三方依赖；同时处理 Assign/AnnAssign、List/Tuple、dataclass field default_factory lambda）：canonical yaml 顶层键序 ↔ schema `$defs.dimension.enum` ↔ skill wizard `ALL_DIMENSIONS`（序）+`DIMENSION_LABELS`（集）↔ harness `personalize_cmd` 两常量 ↔ harness `IterateConfig` 默认维度（集）+ `init_wizard.BASE_DIMENSIONS`（子集）↔ 内置副本字节等价（9 项测试；找不到源时 AssertionError 而非静默通过）。**测试**：harness 新增 tests/test_iterate/test_dimension_check.py 20 项（canonical 加载顺序与字段/干净项目 OK/完整 config 项目 OK/未启用 informational/未知 enabled 键/未知 resources 键/未知 thresholds 键/惰性 warning/FAIL 渲染/personalization 三类悬挂各一+全部通过路径/slash OK 与 FAIL/CLI 退出码 0 与 1）；tests/test_iterate 534 全绿（514+20），全仓回归 1452 passed + 6 skipped（3 失败 + test_http_flow collection error 均为 v1.13 已记录沙箱环境性，无回归）；主仓库 404 全绿（395+9）；npm 包装器 bootstrap 10/10。触碰文件 ruff 零新增（cli.py 15 条存量基线未动）；`__init__.py` 惰性导出补 dimension_check 四符号。**版本与验证**：1.8.0 对齐（pyproject / cli `__version__` / CHANGELOG 1.8.0 / README badge 双语 + 特性表「Dimension doctor/维度 doctor」行 + CLI 速览 `doctor` / npm 包装器 package.json）。
- v1.28（2026-08-16）：1.9.0「TUI 方向键化 personalize 向导」落地，闭合 v1.24 遗留（向导为 CLI 交互式、TUI 内 `/iterate personalize` 仅摘要 + 指引、方向键化为 v2 候选）——9 类个性化向导在 TUI 内完整可用，无需切终端。**① 新模块 `iterate/personalize_tui.py`**：`run_tui_personalize` 复用 CLI 向导的数据模型与保存链（`PersonalizationData` 深拷贝上做全部变更，取消即干净丢弃），但每一步经 TUI 交互通道驱动——`ask_select(title, options)`（方向键选择弹窗，options 为 `{value,label,description?}`）+ `ask_prompt(question)`（自由文本弹窗）；两通道运行时可选，任一缺失 slash 命令回退摘要 + CLI 指引；所有 handler 防御式——弹窗取消（空/未知应答）中止当前步骤而非整个向导。菜单哨兵值（`__add__`/`__back__`/`__save__`/`__cancel__`/`__reset__`/`__rm__` 前缀/`__dim__` 前缀）永不与用户文本或维度键冲突。主菜单列出 9 分类（带实时条目数预览，LABEL_PREVIEW_LIMIT=60 截断）+ Save&finish / Cancel；各分类编辑器支持添加（文本经问题弹窗）与逐条删除；`known_intentional` 结构化采集 file → dimension（canonical 9 选一）→ line（非法输入回退 0）→ reason；`dimension_focus` 维度选择配 focus 追问；`fix_priority_order` 经 move-to-front 重排（任意排列可达）+ reset-to-default；`extra_validation_commands` 保持严格白名单校验（`validate_extra_command`），拒绝原因直接回显在重提示里；末尾确认门 save / keep-editing / discard。保存链与 CLI 向导字节一致（`save_personalization_to_config` + `update_iterate_md_user_section`）。**② 通道暴露**：`QueryEngine.ask_user_select_channel` / `ask_user_prompt_channel` 只读属性把交互通道暴露给 slash 命令（无头运行均为 None）。**③ 接线**：`commands/iterate.py` `/iterate personalize` 检测交互通道——有则进向导（保存失败返回错误消息、取消返回提示），无通道（无头）保持摘要 + `ih iterate personalize` 指引；engine 为 None 时 `getattr` 防御。**测试**：新增 tests/test_iterate/test_personalize_tui.py 25 项（主菜单取消保留原值/字符串类增删存盘/known_intentional 结构化采集含非法行号回退/dimension_focus 配对/fix_priority move-to-front 与 reset/白名单拒绝原因回显重试/确认门三分支/保存失败错误消息/无通道回退摘要/slash 集成 e2e 写盘验证 config 与 ITERATE.md 双产物）；tests/test_iterate 559 全绿（534+25）。**版本与验证**：1.9.0 对齐（pyproject / cli `__version__` / CHANGELOG 1.9.0 / README badge 双语 + 特性表「Personalization wizard/个性化向导」行补 TUI 向导描述 + REPL 速览 `/iterate personalize` / npm 包装器 package.json）。
- v1.29（2026-08-16）：1.9.1「npm 包装器 tarball 下载降级链」落地，修复 1.9.0 发布 e2e 暴露的真实缺陷——本机（python.org Python、信任链损坏）`pip install <github tarball>` 因 `CERTIFICATE_VERIFY_FAILED` 死失败，而同机 curl/Node 下载同一 URL 正常；包装器此前只打印修复指引直接退出，用户无法自愈。**① 两级安装链 `installHarness`**（可注入 runStepFn/downloader 供测试）：第一级维持原状（pip 直接装 tag URL）；失败且目标为 http(s) URL 时进第二级——Node 自有 https 栈下载 tarball 至 `<npm-home>/cache/iterate-harness-<version>.tar.gz` 后 pip 安装本地文件；非 http 目标（本地路径 / ITERATE_HARNESS_INSTALL_URL 指向 git+ 等）保持单次尝试原语义；双失败时抛出的 BootstrapError 携带原始 pip 诊断 + 降级失败原因（cert 指引文案保留）。**② `downloadFile`**：重定向跟随（GitHub archive→codeload 恰需 1 跳，MAX_DOWNLOAD_REDIRECTS=5 防环）、DOWNLOAD_TIMEOUT_MS=120s 超时销毁、2xx/3xx/其它状态码三分支、URL 解析失败即拒；`downloadTarballTo` 包装 mkdir 缓存目录 + 失败清理半写文件。**③ 异步化 ripple**：bootstrap/ensureRuntime/runHarness 转 async（runStep 仍 spawnSync），runHarness 内部 catch 统一 `reportBootstrapFailure`（BootstrapError 打 message、其它打 stack）+ exit 1；bin/ih.js 与 bin/iterate-harness.js 改为 promise `.catch` + 同步 catch 双保险，杜绝 unhandled rejection。**测试**：bootstrap.test.js 新增 10 项（isRemoteHttpUrl 真值表含 git+/本地路径/空值/downloadCachePath 路径形状/pipInstallArgs 参数序/MAX_DOWNLOAD_REDIRECTS=5 稳定性/installHarness 首次成功不下载/TLS 失败→下载→本地装全链断言/双失败包装消息断言/非 http 直抛原错/二次 pip 失败透传/downloadFile 重定向预算耗尽即拒），20/20 全绿；node --check 三文件语法通过。**版本与验证**：1.9.1 对齐（pyproject / cli `__version__` / CHANGELOG 1.9.1 Fixed 小节 / README badge 双语 / npm 包装器 package.json）；发布 e2e 在暴露缺陷的同一台机器上不走 INSTALL_URL 旁路、以真实降级链完成引导（pip TLS 失败→Node 下载→本地安装→`iterate_harness 1.9.1`），缺陷修复即被原始环境验证。**补充（同轮迭代内）**：首轮 e2e 显示降级链触发了 Node 层、但本机 Node 26 同样验签失败（`unable to verify the first certificate`——Node 自带 CA 不读系统钥匙串，本机疑似存在 TLS 拦截代理，而 curl 走系统信任链可用），遂把下载降级扩为两级：`downloadTarballTo` 先 Node https、失败后 `curlDownload`（`curl -fsSL --max-time 240 -o <dest> <url>`，spawnSync、参数与双失败路径可注入测试；macOS 必有 curl、Win10 1803+ 自带、Linux 常见；两级 TLS 验证全程开启，仅换验证者不降安全，层级间清理半写文件，双失败抛聚合错误）；测试增至 25 项（curlDownload 参数序与非零退出/ENOENT、downloadTarballTo node 成功跳过 curl/node 失败落 curl/双失败聚合消息），25/25 全绿；重打 tag 重发 Release 后 e2e 全链成功（pip TLS 失败→Node 失败→curl 成功→本地安装→`iterate_harness 1.9.1`）。
- v1.30（2026-08-16）：发布架构调整「npm 包装器并入 harness subtree，与 iterate-plugin 对称」。v1.25 的「包装器不进 subtree、主仓库为 npm 维护点」决策被本条目修订——npm 包装器从主仓库顶层 `npm/iterate-harness/` 迁移至 `harness/iterate-harness/npm/`，随 Python 源一起经 `git subtree split --prefix=harness/iterate-harness` 发布到独立仓库 `jingzhao-l/iterate-harness`；并建立 `.release/iterate-harness/` 发布工作区（克隆独立仓库），`npm publish` 在 `npm/` 子目录执行，与 plugin 的 `.release/iterate-plugin/` 模式完全对称。**动机**：用户要求保持两项目发布架构对称（plugin 的 npm 包即住在 subtree 仓库）；代价是独立仓库同时承载 Python 源 + npm 包装器两条分发内容（v1.25 曾为避免此而刻意区分，现接受以换取统一心智模型与发布工作区）。**落地**：`git mv npm/iterate-harness harness/iterate-harness/npm`；harness README 与 CHANGELOG 中 npm 路径引用更新为 `harness/iterate-harness/npm`；npm 发布流程 = subtree push（含 npm/）→ `.release/iterate-harness` 克隆/git pull → `npm publish`（在 npm/ 子目录）。**验证**：npm 包装器 25/25 单元测试在迁移后位置通过，`node --check` 语法通过。**残留说明**：独立仓库 `jingzhao-l/iterate-harness` 因同时含 Python 源与 npm 子目录，tag 仍按 harness 版本锁步（vX.Y.Z 同时作 Python tarball 锚点与 npm 包装器版本依据）。
- v1.31（2026-08-16）：收尾与发布流程固化——将 `RELEASE.md` 发布手册并入本文档为 §13（独立 `RELEASE.md` 保留为发布时直接勾选的 checklist，两者内容互为镜像、以 §13 为准）；同步更新文档头部状态行（当前发布 1.9.1，设计文档迭代至 v1.31）。
- v1.32（2026-08-16）：**修正「插件无法改 dsh UI」的错误结论**（新增 §14）——§11.2.1（v1.8）曾断言「插件被 dsh 卡片样式锁死 / 插件无法自绘组件」并把实时仪表盘、分诊界面等归入插件原理上做不出的独占体验，该断言错误。证据：dsh 官方「Everything is a plugin」将 UI 本身列为可插拔能力，前端为插件提供 Client UI 槽位 / 主题令牌 / Cordis 事件 / `dsh.client` 声明（`clientModules` 扫描）；社区实证（2026-08）`dsh-gui-customization`（主题/氛围光/背景）、`dsh-skin-picker`、`dsh-dream-skin`、`Nagi-ovo/dsh-ads`（CSS 动画）均为正规插件而非 hack。修正后：换肤/自绘组件/仪表盘/分诊界面插件侧可实现；独立 harness 真正独占的是**内核级**能力（Esc 中途干预、循环/收敛控制、无人值守、独立存储），原因不是样式被锁死而是编排层不在插件 UI 权限面内。§11.2.1 原文保留存档，以 §14 重估为准。同步在 §11.2.1 引言追加修正指引注记，头部状态行更新至 v1.32。
- v1.33（2026-08-16）：**发布后全面自审（代码 + UX + 功能需求）**，新增 §15。① 代码审查（忽略插件与 skill，仅 harness）：31 项问题定级，确认并修复 4 项真实缺陷——decision_log 解析崩溃 / trend_store 键名不一致 / onboard 配置覆盖 / cron 守护进程 Windows 不兼容，每项带回归测试；git_hook 的 `|| exit 1` 经语义分析判定为 fail-closed 正确行为（非缺陷，不改动）。② 用户体验审查：CLI/TUI 双入口状态、Esc 干预、收敛可视化、onboarding 心智、错误可恢复性 6 维评估，14 项发现（8 好 / 3 可改 / 3 缺口）。③ 功能需求分析：28 项候选排定 6 项高价值——a) 自定义模型提供方 & API 地址（BYOK）；b) 收敛仪表盘进 TUI 面板；c) 失败自愈（重复轮次回退至上一轮失败点）；d) session 工作区隔离（sandboxed worktree）；e) 速率限制/预算熔断；f) HTML 报告服务化。详见 §15。CHANGELOG 补 [Unreleased]（1.9.2 候选）。
- v1.34（2026-08-16）：**插件 UI 层落地细化**——基于 §14.4 决策的完整实现方案（§16）。技术底座对齐 dsh-gui-customization 0.6.2 实证格式（`clientModules` 扫描 + `theme.overrideTokens` + `slots/changed` 事件驱动）；数据流转发器机制（会话快照轮询 `useSession` + `convergence.totalRounds` 变化触发视觉脉冲，否决后端事件桥接方案——dsh 只转发 4 类自有事件）。六项实现逐一细化：收敛仪表盘、进度条、分诊界面、Esc 暂停、diff 审批、配置面板。后端闭环新增 `iterate_triage` 工具（分诊写回的真正后端）。验收清单 16 项。**本版为纯设计细化，不修改 harness 源文件**。
- v1.35（2026-08-16）：**6 项高价值功能完整实现**——本轮迭代将 §15.3 识别的 6 项能力缺口全部落地为可运行代码，覆盖 BYOK / 收敛仪表盘 / 断点续跑 / 工作区隔离 / 预算熔断 / HTML 报告服务。**① 自定义模型提供方（BYOK）**：`config/settings.py` 扩展 `ProviderProfile`（BaseModel，支持自定义 API 格式/Auth 来源/base_url/默认模型），内置 10 档默认 profile（claude-api/claude-subscription/openai-compatible/codex/copilot/moonshot/gemini/minimax/nvidia/qwen/modelscope）+ `default_provider_profiles()`/`merged_profiles()`/`resolve_profile()`；CLI `provider add` 注册自定义端点，`auth/manager.py` 按 profile 装载凭据，`commands/registry.py` `/model` 选择与 profile 状态展示。**② 收敛仪表盘进 TUI**：`ReviewProgressEvent`（round/new_findings/per_dimension/token_cost）经 `ui/app.py` 事件分发渲染——findings 递减 sparkline + 分维度计数 + 累计费用，React 前端 `ReviewProgressPanel.tsx` 实时面板。**③ 失败自愈/断点续跑**：`checkpoint.py` 原子检查点（`save_checkpoint`/`load_checkpoint`/`clear_checkpoint`，保存/加载最后一轮成功 states）；`last_state.py` 持久化上次运行快照供续跑恢复；`loop_policy.py` `on_turn_end` 经 `read_state` 评估进度，引擎在每次成功收敛点落盘 checkpoint。**④ 会话工作区隔离**：`worktree_flow.py` 封装 worktree 创建/合并/回滚（`WorktreeSession` 序列化 + git 命令封装）；`worktree_runtime.py` 管理运行时生命周期（`enter_for_round`/`finalize`/`resume_if_needed`）；`engine/query.py` 集成隔离逻辑（`worktree_isolation` 开启时修复轮在专用 git worktree 内执行，成功合并/异常丢弃）；`swarm/worktree.py` 复用软链复用与 stale 清理。**⑤ 预算熔断/限流**：`loop_policy.py` 扩展 `IterateLoopPolicy`——`total_token_budget`（token 硬上限，超出即 STOP 并引导收尾报告）与 `budget_usd`（美元预算，CostMeter 累计超限即 STOP）经 `_budget_stop_reason()` 熔断；`max_turns_per_minute` 速率限制（`RATE_LIMIT_WINDOW_SECONDS=60` 滚动窗口 + `_throttle_delay` 回退），`before_request` 被引擎每请求前调用返回需休眠秒数。**⑥ HTML 报告服务**：`report_server.py` 新增静态 HTTP 服务器（`serve_report`，oneshot/persist 双模式 + 自动开浏览器 + 扩展 MIME）；`html_report.py` 新增 `build_replay_page` 交互式轮次回放页（按轮分组 panel + prev/next 导航 + jump 圆点 + 键盘 ←/→ + 类型化 entry 卡片 + HTML 转义防 XSS）；CLI `iterate report --serve/--serve-port/--serve-persist` 与 TUI `/iterate report --serve` 双入口。**测试与质量**：新增测试 `test_checkpoint.py`/`test_report_server.py` 及 `test_html_report.py`/`test_loop_policy.py`/`test_last_state.py` 扩展，本轮新增 74 项全绿；新增模块 ruff 零告警、mypy 零错误；本轮同步清理 2 处存量 mypy（worktree_flow 元组收窄、loop_policy 变量遮蔽）。**版本与验证**：1.9.2 对齐（pyproject / cli `__version__` / CHANGELOG 1.9.2 / README badge 双语）。
- v1.36（2026-08-16）：**1.9.3 发布收口 + 版本修正**——v1.35 所述「1.9.2 对齐」因 1.9.2（4 缺陷版，commit `9ff88df`）已先期发布并同步至独立仓库 `jingzhao-l/iterate-harness`，6 项高价值功能实际以 **1.9.3** 发布：pyproject / cli `__version__` / CHANGELOG 新增 [1.9.3] / README badge 双语全部对齐 1.9.3。**质量收口**：全量测试 1526 通过 / 6 跳过（1 项 `test_bash_tool` 沙箱无 Node.js 环境失败为既有环境限制）；新增 6 模块 104 项全绿；ruff 零告警；修复 2 项工具链问题——`mcp` 依赖收窄 `>=1.0.0,<2.0.0`（2.0 移除 `mcp.server.fastmcp` 破坏 MCP HTTP 测试）与补充 `py.typed` 标记（此前缺失导致 mypy 把包当第三方跳过分析，暴露 477 项存量类型债，均为既存代码、非本轮引入，不在本次范围）。头部状态行更新至 1.9.3 / v1.36。
- v1.37（2026-08-17）：**28 项完整清单固化 + 剩余 22 项补齐实现（1.9.4）**——§15.3 的「28 项候选」在 §15.4 完整列出并逐项标注来源/价值/成本/实现状态（不再只记录 6 项高价值子集）。其中 1.9.3 已实现 #1-#6 + 历史版本已实现 #7/#13/#14/#16/#17/#20/#23-#27 后，本次把剩余待实现/部分覆盖项全部落地：**#8** 分诊结果本轮即应用（`personalization.sync_known_intentional_to_config` 配置桥，把 `known_intentional` 合并写入 `iterate.config.yaml`，去重/原子写/保留手写项）；**#9** 常见失败自愈指南章节（README Troubleshooting，TLS/认证/配额/断点/模型未找到五类）；**#10** prompt 模板预设（`prompts.py` TEMPLATE_PRESETS standard/strict/quick + CLI `--template`，`template_suffix` 模式归一化 `dry-run`→`dry_run`）；**#11** 多语言报告（`ci_report.py` L10N_TEXTS en/zh + CLI `--lang`）；**#15** CSV 导出（`render_csv` UTF-8 BOM 供 Excel 直接打开 + CLI `--csv`）；**#21** webhook 推送（新模块 `webhook.py`，自动识别 Slack/飞书/generic，富 Blocks/卡片 + CLI `--webhook`）；**#18** 两次运行 diff（`trend_store.diff_runs`/`RunDiff` new/fixed/regressed/unchanged + `render_diff`，回归经 `previously_fixed_findings` 识别）；**#19** 多分支审查入口（CLI `review|run --branch` + worktree 隔离）；**#22** 维度查看（TUI `/iterate dimensions` 展示维度及资源配置）；**#12** 离线模型（`settings.py` 新增 `local`/`ollama` profile，`auth_source: local`）。**质量与验证**：harness 全量 1602 通过 / 1 失败（`test_bash_tool` 部分输出断言为既有环境限制：macOS 无 `script` 包装时 PTY 无法流式回读，与本次无关，留待跨平台跟进）；npm wrapper 25/25；新增测试 `test_prompts.py`/`test_webhook.py`/`test_branch_review.py` 及 trend diff/ci_report l10n 扩展。**版本**：1.9.3 已发布（npm 不可重发），本次版本推进至 **1.9.4**——pyproject / cli `__version__` / npm / README badge 对齐 1.9.4，CHANGELOG 新增 [1.9.4]。头部状态行更新至 1.9.4 / v1.37。
- v1.38（2026-08-17）：**独立 WebUI 管理台设计（新增 §17）**——路线 B 的「活管理后端」。决策（用户）：完整管理台；技术栈 FastAPI + React；落地形态先独立 Web、后 Electron 壳；**自建、不拉取 DSH WebUI 代码**。论证：DSH WebUI 是 Cordis/Node 主进程的前端壳（WebSocket/RPC 通信），数据模型（会话 + trajectory 事件流）与 harness（decision log + 收敛 + checkpoint + 预算）不对应，桥接层仍需全量重写，且 DSH 处于 developer preview（v0.1.0-rc.5）有破坏性变更，fork 双重维护——故仅借鉴其 UX 设计语言（trajectory 时间线 / 可回溯复盘 / 审批确认流），不拷贝代码（§17.2）。范围：7 页面（Dashboard / Runs / Checkpoints / Workspaces / Budget & Rate / Config / Reports），写操作「只读默认 + 显式确认 + 写入前备份 + 失败回滚」（§17.3）。后端：新模块 `iterate_harness/web/`（api / routes / events SSE / security），默认绑定 127.0.0.1、CORS 仅本机回环、路径白名单、API key 脱敏、写操作审计（§17.4）。前端：Vite + React 18 + TS + react-router + zustand，视觉对齐既有 HTML 报告（severity 固定色表、蓝灰基调），借鉴 DSH trajectory 信息密度（§17.5）。依赖全部宽松许可（fastapi MIT / uvicorn BSD-3 / react MIT / vite MIT 等）并精确锁版（§17.6）。目录镜像既有 `frontend/terminal` force-include 打包模式，`ih web` 一键拉起（§17.7）。Electron 壳锁定为第二阶段、本版不实现（§17.8）。里程碑 M1-M4 与质量门（§17.9）、风险（§17.10）。**本版为纯设计细化，不修改 harness 源文件**。头部状态行更新至 v1.38（当前发布 1.9.4）。

- v1.39（2026-08-17）：**WebUI 迭代：对话界面人类-in-the-loop 控制（新增 §18）**——在 WebUI 管理台中嵌入可折叠侧边对话面板，支持启动/暂停/用户输入/停滞检测/督促注入，匹配 iterate 垂直领域定位（主体是管理台，对话是辅助干预）。
- v1.40（2026-08-17）：**WebUI 迭代：工作区 / Findings 分诊 / 健壮性（新增 §19）**——落地 §17.3 P2 的 Findings 分诊（持久化 approve/reject 审批日志）与 P4 的工作区管理（主工作区 + 隔离 worktree 列表/删除）；对话面板新增工具调用可视化卡片；管理台新增 ErrorBoundary / Skeleton / 键盘快捷键 / SSE 断线轮询兜底 / 连接状态 toast / 浏览器通知等健壮性增强。
- v2.0（2026-09-02）：**大版本方向：双模式（iterate 纯审查 / code 通用编程 agent + 防御式内核 + 多 agent 编排）（新增 §20）**——v1 系列已至 1.11.0 稳定期，功能趋于做尽；本条目确立 harness 2.0 升级方向。核心决策：① `task_mode`（code / iterate）与 `permission_mode`（default/plan/full_auto）**分离**——`task_mode` 决定 agent 干什么（通用编程 vs iterate 审查迭代闭环），`permission_mode` 决定权限多宽松；② **iterate 模式 = 1.x 完整保留**（9 维度审查→分诊→原子/架构修复→验证→收敛，零破坏）；③ **code 模式 = 通用编程 agent + 防御式内核**——深度融入 iterate 理念但**不脱离 iterate 基础**，防御式编程（最小化假设 / 信任边界验证 / fail-fast+原子事务 / 前置后置条件 / 不变量守护 / 假设声明与校验）成为 agent **每个动作的默认行为**而非事后审查，多 agent 编排（agent / send_message / task_stop + coordinator + swarm 全套）直接启用；④ **TUI 模式切换对齐 opencode**——空输入框 Tab 直切 code ↔ iterate，输入框左侧竖向色条随模式变色（code=primary / iterate=amber），输入框底部模式文字随切随色；⑤ 完整能力审计（§20.4）：对比 `.external/OpenHarness` 原始代码，通用编程 + 多 agent 能力 **100% 完整保留**，仅缺 4 个外围扩展（image_generation / autopilot / channels / vim），不影响 code 模式编程核心。**本版为纯设计细化，不修改 harness 源文件**。头部状态行更新至 v2.0。
## 13. 发布手册（Release Manual）

> 本节为 `RELEASE.md` 的镜像章节（v1.31 并入），是 iterate 生态三个对外发布项目的统一发布 checklist。发布操作以本节为准，独立 `RELEASE.md` 保留便于快速勾选。

iterate 生态目前有 **三个** 会独立对外发布的项目：iterate-skill（skill 本体 + CLI + 安装器）、iterate-harness（Python 引擎 + npm 包装器）、iterate-plugin（dsh 插件）。三个项目共用同一主仓库 `jingzhao-l/iterate-skill` 作为唯一开发/评审点，`harness/` 下的两个子项目通过 `git subtree` 拆分到各自的独立发布仓库，再在 `.release/` 发布工作区执行 npm 发布。

### 13.1 生态项目一览

| 项目 | 仓库 | 分发渠道 | 版本线 |
|---|---|---|---|
| **iterate-skill**（skill 本体 + CLI + 安装器） | `jingzhao-l/iterate-skill`（主仓库，唯一维护点） | GitHub Release / npm / ClawHub / ModelScope / Tencent SkillHub | 2.3.x（与 skill 同步） |
| **iterate-harness**（Python 引擎 + npm 包装器） | `jingzhao-l/iterate-harness`（subtree 独立发布仓） | GitHub tag / npm 包装器 | 1.9.x（独立） |
| **iterate-plugin**（dsh 插件） | `jingzhao-l/iterate-plugin`（subtree 独立发布仓） | npm | 2.3.x（独立，自 2.3.7 起） |

### 13.2 项目 1：iterate-skill（skill 本体）

**需要同步的版本号文件**（step 1 一次性完成）：

| 文件 | 字段 |
|---|---|
| `pyproject.toml` | `[project].version` |
| `iterate_cli/__init__.py` | `__version__` |
| `SKILL.md` | frontmatter `version` |
| `npm-installer/package.json` | `version` |
| `CHANGELOG.md` | 新增版本条目 |

**发布清单**：

- [ ] **1. 同步版本号**：人工编辑上述 5 个文件 + 更新 `CHANGELOG.md`（保留旧版本条目，只新增）。
- [ ] **2. 本地验证**：跑通全部测试（`pytest tests/ -q`、`ruff check`），确认 `iterate --version` 输出新版本。
- [ ] **3. 提交并推送主仓库**：`git add -A && git commit && git push origin main`。
- [ ] **4. 打 GitHub Release tag**：`git tag v<X.Y.Z> && git push origin v<X.Y.Z>`，在 GitHub 创建 Release。
      > `.github/workflows/release.yml` 会在 Release published 时自动生成并上传 `iterate-skill.tar.gz` + `SHA256SUMS.txt`（从 tag 树确定性构建）。
- [ ] **5. 发布 npm 安装器**（安装器从 GitHub Release 下载 tarball，务必先于/同步于 npm 发布）：
      ```bash
      cd npm-installer
      npm publish
      ```
      验证：`npx iterate-skill-installer --version` 能拉到新版本。
- [ ] **6. 发布 ClawHub**：
      ```bash
      clawhub publish <stage 目录> --slug iterate-skill --name Iterate --version <X.Y.Z> --no-input
      ```
      > **坑**：必须显式传 `--name Iterate`，否则显示名会被默认取为发布目录 basename（历史上出现过 `Clawhub Stage 2.3.12`）。ClawHub 有已知 bug（issue #2983），偶发 `skillId/versionId invalid value`，发布前需清理残留的 suspended 进程。
- [ ] **7. 发布 ModelScope**：
      - 用 **精简包**（zip 需 < 5MiB，只含核心文件，不含前端/文档等）。
      - 通过 OpenAPI 更新：`openapi.update_skill_settings(owner, name, {'skill_file': file_id})`。
      > **坑**：完整包常超 5MiB 上限，必须用精简包。
- [ ] **8. 发布 Tencent SkillHub**：
      - 用 **SkillHub 专用包 `iterate-skill-skillhub.zip`**（**排除 LICENSE**），skillId `104490`。
      > **坑**：必须用去掉 LICENSE 的精简专用包（约 288KB）防止上传 `Broken pipe`；完整包（含 LICENSE）会因过大上传失败。
- [ ] **9. 三平台版本一致性确认**：ClawHub / ModelScope / SkillHub 均指向 `<X.Y.Z>`。

### 13.3 项目 2：iterate-harness（Python 引擎 + npm 包装器）

**版本锁步规则**：`npm 包装器 version == harness 版本 == GitHub tag`（npm `1.9.1` → tag `v1.9.1`）。包装器首次运行会把匹配版本的 release tarball pip 安装进托管 venv，npm 升级后 stamp 不匹配会自动重装到新 tag。

**需要同步的版本号文件**：

| 文件 | 字段 |
|---|---|
| `harness/iterate-harness/pyproject.toml` | `[project].version` |
| `harness/iterate-harness/src/iterate_harness/__init__.py` | `__version__`（若存在） |
| `harness/iterate-harness/npm/package.json` | `version` |
| `harness/iterate-harness/CHANGELOG.md` | 新增版本条目 |

**发布清单**：

- [ ] **1. 同步版本号**：编辑上述文件 + 更新 `CHANGELOG.md`（保留旧条目）。
- [ ] **2. 本地验证**：跑通 harness 测试（`cd harness/iterate-harness && pytest tests/ -q`）与 npm 包装器测试（`cd harness/iterate-harness/npm && node --test test/bootstrap.test.js`）。
- [ ] **3. 提交并推送主仓库**：`git commit && git push origin main`。
- [ ] **4. subtree 拆分到独立发布仓**：
      ```bash
      git subtree split --prefix=harness/iterate-harness -b subtree-harness
      git push harness-origin subtree-harness:main
      git branch -D subtree-harness
      ```
      > 独立仓 `jingzhao-l/iterate-harness` 同时承载 Python 源码 + `npm/` 包装器。
- [ ] **5. 独立仓打 tag + Release**：在独立仓打 `v<X.Y.Z>` tag 并创建 GitHub Release（作为 npm 包装器 pip-install 的 tarball 锚点）。
- [ ] **6. 同步发布工作区 + npm publish**：
      ```bash
      # 进入发布工作区（克隆的独立仓，gitignore）
      cd .release/iterate-harness
      git pull origin main
      cd npm
      npm publish
      ```
      验证：`npm install -g iterate-harness && ih --version` 输出新版本。
      > npm `repository` 元数据指向独立仓 `jingzhao-l/iterate-harness`。

### 13.4 项目 3：iterate-plugin（dsh 插件）

**版本规则**：独立版本线（自 2.3.7 起），不再与 skill 本体版本号强绑定。仅改 `harness/iterate-plugin/package.json` 的 `version`。

**需要同步的版本号文件**：

| 文件 | 字段 |
|---|---|
| `harness/iterate-plugin/package.json` | `version` |
| `harness/iterate-plugin/package-lock.json` | `version` |
| `harness/iterate-plugin/CHANGELOG.md`（若存在） | 新增版本条目 |

**发布清单**：

- [ ] **1. 同步版本号**：编辑 `package.json`（含 `package-lock.json` 若已提交）。
- [ ] **2. 本地验证**：`cd harness/iterate-plugin && npm install && npm run typecheck && npm test`。
- [ ] **3. 提交并推送主仓库**：`git commit && git push origin main`。
- [ ] **4. subtree 拆分到独立发布仓**：
      ```bash
      # 若尚未配置 plugin 独立仓 remote（主仓库默认只有 origin / harness-origin）：
      git remote add plugin-origin https://github.com/jingzhao-l/iterate-plugin.git

      git subtree split --prefix=harness/iterate-plugin -b subtree-plugin
      git push plugin-origin subtree-plugin:main
      git branch -D subtree-plugin
      ```
      > 独立仓 `jingzhao-l/iterate-plugin` 带 `dsh-plugin` topic，作为 dsh 生态发现入口。
- [ ] **5. 同步发布工作区 + npm publish**：
      ```bash
      cd .release/iterate-plugin
      git pull origin main
      npm publish
      ```
      验证：npm 上 `iterate-plugin` 版本为 `<X.Y.Z>`。
      > npm `repository` 元数据指向主仓库 `jingzhao-l/iterate-skill`（目录 `harness/iterate-plugin`）。

### 13.5 常见遗漏点（Checklist 之外）

- **skill 侧**：改了代码但忘记同步 `npm-installer/package.json` 版本 → npx 拉到旧版安装器。
- **skill 侧**：ClawHub 发布未传 `--name Iterate` → 显示名变成目录名。
- **skill 侧**：ModelScope 用完整 zip → 超 5MiB 失败；SkillHub 忘了去掉 LICENSE → `Broken pipe`。
- **harness 侧**：npm 包装器版本与 harness/tag 不同步 → 用户升级后装错版本。
- **harness 侧**：subtree 拆分后忘记在独立仓打 tag → npm 包装器 pip-install 找不到 tarball。
- **plugin / harness 侧**：subtree push 后忘记同步 `.release/` 工作区就直接 `npm publish` → 发布会发布旧版本。

### 13.6 快速对照（命令速查）

| 动作 | 命令 |
|---|---|
| skill 打 tag | `git tag v<X.Y.Z> && git push origin v<X.Y.Z>` |
| skill npm 安装器 | `cd npm-installer && npm publish` |
| skill ClawHub | `clawhub publish <stage> --slug iterate-skill --name Iterate --version <X.Y.Z> --no-input` |
| skill ModelScope | `openapi.update_skill_settings(owner, name, {'skill_file': file_id})`（精简 zip <5MiB） |
| skill SkillHub | 上传 `iterate-skill-skillhub.zip`（去 LICENSE），skillId `104490` |
| harness subtree | `git subtree split --prefix=harness/iterate-harness -b subtree-harness && git push harness-origin subtree-harness:main` |
| harness npm | `cd .release/iterate-harness/npm && npm publish`（先 `git pull`） |
| plugin subtree | `git subtree split --prefix=harness/iterate-plugin -b subtree-plugin && git push plugin-origin subtree-plugin:main`（先 `git remote add plugin-origin https://github.com/jingzhao-l/iterate-plugin.git` 若未配置） |
| plugin npm | `cd .release/iterate-plugin && npm publish`（先 `git pull`） |

## 14. UI 能力修正（v1.32：推翻「插件无法改 dsh UI」的错误结论）

> **背景**：§11.2.1（v1.8）曾断言「插件被 dsh 卡片样式锁死」「dsh 卡片是静态文本，插件无法自绘组件」，并把「实时收敛仪表盘 / diff 审批 / 分诊界面」全部归入 skill 与插件**原理上做不出**的独占体验。该断言**错误**，本节予以修正；§11.2.1 原文保留存档，以本节重估为准。
>
> **证据链**：dsh 官方架构「Everything is a plugin」，明确将 **UI 本身列为可插拔能力**（官方文档原话：Plugins provide every agent capability, including … the UI）。dsh Web 前端是独立的 Cordis 应用插件（`@deepseek-ai/dsh-web-app`），前端运行时为插件提供：**Client UI 槽位（slot）**、**主题令牌（theme token）**、**Cordis 事件 / 服务**，且 `package.json` 通过 `dsh.client` 声明被 `clientModules` 服务扫描进 Web 启动图。
>
> **社区实证**（2026-08 上线的真实插件）：
>
> | 插件 | 改了什么 | 用的扩展点 |
> |---|---|---|
> | `dsh-gui-customization` | 主题配色 / 氛围光 / 背景图，设置页持久化 | Client UI 槽位 + 主题令牌 + `dsh.client` 声明 |
> | `dsh-skin-picker` / `dsh-skins` | 多套皮肤、自然语言换肤、自定义背景 | 主题令牌 + CSS 注入 |
> | `dsh-dream-skin` | 壁纸 / 主题包导入导出 | 主题令牌 |
> | `Nagi-ovo/dsh-ads` | 界面加动态鲸鱼动画 | Cordis 插件监听事件 + CSS 动画 |
>
> 结论：**皮肤 / 主题 / 背景 / 动画 / 自绘 UI 组件，插件侧都是正经支持的能力**，不是 hack。

### 14.1 修正后的能力边界

| 能力 | skill | dsh 插件（路线 A） | 独立 harness（路线 B） |
|---|---|---|---|
| 换肤 / 主题令牌 / 背景 / 氛围光 | ❌ 无法 | ✅ 原生槽位 + token 系统 | ✅ 自研 |
| 往界面加自绘组件 / 动态动画 | ❌ 无法 | ✅ Client slot + CSS/事件 | ✅ 自研 |
| 自定义审批交互（逐 hunk diff、Esc 暂停干预） | ❌ 无法 | ⚠️ 依赖 dsh 审批框架是否暴露对应 slot / 事件 | ✅ 内核自定 |
| 会话 / 循环 / 编排层深度改造 | ❌ 无法 | ⚠️ 只能走 dsh workflow / 事件，受框架约束 | ✅ 内核原样可控 |
| 无人值守（离开 dsh 会话自治跑） | ❌ | ❌ 仍需 dsh 会话 | ✅ headless / CI |
| 数据沉淀 / 趋势库 / 回放 | ❌ 纯文本 | ⚠️ 可注册工具+持久化，但受 dsh 存储约束 | ✅ 自建本地库 |

### 14.2 对「§11.2.1 独占体验」的重估

| §11.2.1 条目 | 原结论 | v1.32 重估 |
|---|---|---|
| 实时收敛仪表盘（Round/N/维度 spinner/token 累计） | 插件无法自绘 | **插件可实现**：自绘组件进 Client slot，消费 `iterate_review` 事件流 |
| findings 分诊界面（y/修复 n/跳过 a/忽略） | 插件无交互入口 | **插件可实现**：自绘交互组件 + 写回 `iterate.config.yaml` 工具 |
| 细粒度逐 hunk diff 审批 | 插件只能整文件审批 | **视 dsh 审批框架而定**：若暴露 diff 粒度 slot 则可行，否则保持整文件级 |
| init 检测式向导 | 插件没做 init | 插件可实现（自绘 + 复用 `iterate_config` 探测） |
| Esc 暂停 / 中途改道 | 插件 workflow 不可中途改道 | **仍为路线 B 独占**（循环控制需内核级） |
| 无人值守场景（PR 评论 / git hook / 批量定时） | 插件依赖 dsh 会话 | **仍为路线 B 独占**（存在性缺口，与 UI 无关） |
| 数据沉淀趋势 / HTML 报告 / 回放 | 插件做不了 | ⚠️ 插件可部分（工具+持久化），完整趋势库仍需独立存储 |

### 14.3 修正后的设计含义

1. **「看得见的 UI」不再是独立 harness 的独占卖点**：实时仪表盘、分诊界面这类 iterate 专属 UI，走 dsh 插件（路线 A）也可实现，成本是熟悉 dsh 前端 slot / token / `dsh.client` 机制。
2. **路线 B（独立 harness）真正独占的仍是「内核级」能力**：Esc 中途干预、循环/收敛控制、无人值守、独立存储——这些靠 UI 插件做不到，理由不是"样式被锁死"，而是**循环与会话的编排层不在插件 UI 的权限面内**。
3. **插件（路线 A）的 UI 定位建议**：优先做「iterate 专属可视化」——收敛仪表盘、分诊面板、迭代统计，走 Client slot + 事件；不做皮肤 / 主题类（与社区已有插件同质化，且非 iterate 价值点）。
4. **本节不影响已发布的 iterate-plugin 形态**：插件保持瘦实现（prompt 注入 + 5 工具）仍成立，UI 层按需增量演进；是否投入 UI 层由用户决策（见 §14.4 候选清单）。

### 14.4 UI 层候选实现清单（供决策）

> 均以「客户端（web 前端）slot + 主题令牌 + `dsh.client` 声明 + 事件」为技术底座；按 iterate 价值、实现成本、与社区差异化三维评估。

| # | 候选 UI 层实现 | 做什么 | 技术路径 | 价值 | 成本 | 差异化 |
|---|---|---|---|---|---|---|
| 1 | **迭代收敛仪表盘** | 会话侧边/消息内显示 `Round N/M`、五维度 spinner + findings 计数、token/费用累计条、收敛 sparkline | 自绘组件注册 Client slot，消费 `iterate_review` 运行事件流 | 高（iterate 最核心的"看得见收敛"体验） | 中 | 高（生态暂无 iterate 专属可视化） |
| 2 | **findings 分诊面板** | 审查完逐条过 `y/n/a`，`a` 自动写回 `known_intentional` | 自绘交互组件 + 复用 `iterate_config` 读写 | 高（个性化闭环做成交互） | 中 | 高 |
| 3 | **迭代统计卡片** | 每次 iterate 结束生成统计卡：修复数 / 剩余数 / 各维度分布 / 耗时 | 消息卡片（现有卡片机制即可） | 中 | 低 | 中 |
| 4 | **iterate 主题 / 皮肤** | 给 dsh 出一套 iterate 专属配色皮肤 | 主题令牌 + CSS 注入 | 低-中 | 低 | 低（与社区皮肤插件同质化） |
| 5 | **进度通知 / 事件联动** | 迭代轮次变更时做视觉/角标联动（如子代理派发时动画） | Cordis 事件 + CSS 动画 | 中 | 低 | 中 |
| 6 | **设置页扩展** | 在 dsh「设置」里加 iterate 配置管理入口（读取/修改 `iterate.config.yaml`） | 设置页 slot + `iterate_config` 工具 | 中 | 中 | 中 |

**决策建议**：优先 #1 收敛仪表盘 + #2 分诊面板（价值与差异化双高、直接兑现"看得见收敛"）；#3/#5 低成本可作为第一批落地；#4 皮肤与社区同质化不建议投入；#6 视迭代节奏定。

## 15. 发布后全面自审（v1.33：代码审查 + 用户体验审查 + 功能需求分析）

> 本节基于 1.9.1 发布后的全面自审（2026-08-16），**忽略插件（iterate-plugin）与 skill 本体**，仅针对独立 harness。结论已同步至 CHANGELOG [Unreleased]（1.9.2 候选）。本节内容为本次收尾的权威记录，后续迭代以其为输入。

### 15.1 代码审查（31 项问题定级）

对 harness 核心（loop 簿记 / review / cron / personalize / onboarding / trend / decision-log / git 集成 / 分发层）做了全量代码审查，共定位 **31 项问题**，按严重度归类：

| 严重度 | 数量 | 处理 |
|---|---|---|
| **Critical（数据完整性 / 崩溃）** | 4 | ✅ 全部修复 + 回归测试 |
| Major（健壮性 / 边界） | 7 | 已复核为防御式处理或符合预期，无需改动 |
| Minor（风格 / 可读性） | 13 | 记录待后续清理 |
| 误报（审查后判定非缺陷） | 7 | 记录结论，不改代码 |

**已修复的 4 项 Critical 缺陷：**

1. **decision_log 解析崩溃**（[decision_log.py](file:///Volumes/Eng-Dev/iterate-skill/harness/iterate-harness/src/iterate_harness/iterate/decision_log.py)）：`read_entries` 对畸形条目（`round` 非数字、`data` 非映射）抛 `ValueError`/`TypeError`，单行坏数据会连带 `report --fail-on`、趋势分析整体崩溃。修复：字段解析包 try-except，畸形行跳过并告警，绝不中断整次读取（append-only 契约下部分日志优于硬失败）。
2. **trend_store 键名不一致**（[trend_store.py](file:///Volumes/Eng-Dev/iterate-skill/harness/iterate-harness/src/iterate_harness/iterate/trend_store.py)）：`TrendRecord.to_dict()` 写 camelCase（`firstSeen`/`lastSeen`/`fixedAt`）而读取用 snake_case，跨进程重启后趋势分类（new/fixed/regressed/stubborn）静默误读持久化数据。修复：序列化统一 snake_case 与反序列化对齐。
3. **onboarding 配置覆盖**（[onboard_cmd.py](file:///Volumes/Eng-Dev/iterate-skill/harness/iterate-harness/src/iterate_harness/iterate/onboard_cmd.py)）：`run_onboard`/`reonboard` 重建 `iterate.config.yaml` 时丢弃用户自有区块（personalization / review / budget / cron 等）。修复：新增 `_merge_into_existing`，新字段合并到既有配置上而非整体替换。
4. **cron 守护进程 Windows 不兼容**（[cron_scheduler.py](file:///Volumes/Eng-Dev/iterate-skill/harness/iterate-harness/src/iterate_harness/services/cron_scheduler.py)）：`start_daemon` 用 Unix 专属 `os.fork()`+`os.setsid()`，Windows 直接崩溃。修复：改用 `subprocess.Popen` 派生完全分离的子进程，跨平台可用。

**误报澄清（1 项，重点记录）：**

- **git_hook `|| exit 1` 非缺陷**（[git_hook.py](file:///Volumes/Eng-Dev/iterate-skill/harness/iterate-harness/src/iterate_harness/iterate/git_hook.py)）：审查时一度认为它会「绕过 report 门禁」。语义分析确认：`iterate review --changed --clean-ok --ref HEAD` 仅在三类情况非零退出——ref 非法（hook 内恒为 `HEAD`，不会触发）、无变更（`--clean-ok` 下退出 0）、review 真实失败（模型/认证崩溃）。最后一种触发 `|| exit 1` 阻断提交是**fail-closed 正确行为**，且并未绕过 `report --fail-on` 门禁（review 成功即退出 0，门禁照常执行）。若移除该守卫，review 崩溃时 hook 会 fail-open 放行提交——**维持现状**。

### 15.2 用户体验审查（6 维 14 项发现）

以「用户在真实项目中完成一次 iterate 循环」为主线，评估 CLI 与 TUI 双入口：

| 维度 | 发现 | 判定 |
|---|---|---|
| **入口可达性** | CLI 子命令层级清晰（`ih iterate <onboard|review|run|report|personalize|doctor|hook|schedule>`），帮助文本双语 | ✅ 好 |
| **入口可达性** | TUI `/iterate` 斜杠命令与 CLI 行为一致，无头会话优雅降级为摘要+指引 | ✅ 好 |
| **引导与 onboarding** | onboard 检测-问答-模型扫描三步心智一致；`--no-ai` 检测版可离线完成 | ✅ 好 |
| **引导与 onboarding** | reonboard 自动备份 + 失败回滚，用户自有区块保留（v1.33 修复配置覆盖后闭环） | ✅ 好 |
| **反馈与可视化** | dry-run/normal 多轮收敛有逐轮 spinner、token/费用累计、收敛 panel | ✅ 好 |
| **反馈与可视化** | 收敛数据只在 TUI 面板可见，**纯 CLI 会话无实时可视化**（文本阶段性摘要） | ⚠️ 可改 |
| **错误可恢复性** | Esc 中途干预、暂停后可继续/放弃，决策日志可回放 | ✅ 好 |
| **错误可恢复性** | 无头运行中模型失败：错误信息可读，但**无「从失败点重试」路径**（只能整轮重跑） | ⚠️ 可改 |
| **个性化闭环** | TUI 内方向键 9 类向导与 CLI 字节一致，取消干净 | ✅ 好 |
| **个性化闭环** | `known_intentional` 采集后需手动重新审查才生效，缺「本轮结束即应用」联动 | ⚠️ 可改 |
| **无人值守** | cron 调度 + git hook + PR 评论 + HTML 报告四件套齐全，`--clean-ok` 优雅处理无变更 | ✅ 好 |
| **无人值守** | 趋势库（stubborn 3+ 轮）**仅 CLI `log --trend` 可见**，TUI 无入口 | 🔻 缺口 |
| **安全心智** | 模型只写 ITERATE.md（不可信散文），config 始终 harness 序列化；路径白名单、权限最小化已固化 | ✅ 好 |
| **文档/上手** | README 双语 + 快速上手 + `doctor` 一致性自检 | 🔻 缺口：缺「常见失败场景自愈指南」章节（TLS、认证、配额） |

**结论**：整体 UX 成熟度高（8 好 / 3 可改 / 3 缺口），无阻塞性体验缺陷；最值得投入的改进是「失败点重试」与「TUI 收敛可视化」。

### 15.3 功能需求分析（28 项候选 → 6 项高价值）

从代码审查缺口、UX 缺口、真实使用场景三个来源汇总 **28 项候选功能**，按「价值 × 成本 × 差异化」排定 6 项高价值：

| # | 功能 | 动机 / 解决什么 | 价值 | 成本 |
|---|---|---|---|---|
| 1 | **自定义模型提供方（BYOK）** | 当前只支持内置提供方（anthropic/openai），无法接本地/私有端点、无法自定义 base_url 与模型名——这是独立运行时最刚性的能力缺口 | 高 | 低 |
| 2 | **收敛仪表盘进 TUI** | 纯 CLI / 无头会话看不到实时收敛，把 panel 数据落到终端文本/进度条（非全 TUI 亦可用） | 高 | 中 |
| 3 | **失败自愈 / 断点续跑** | 模型中途失败时从「上一轮已收敛结果」续跑而非整轮重跑；决策日志已具备回放基础（本轮缺陷 #1 修复后更稳） | 高 | 中 |
| 4 | **session 工作区隔离（sandboxed worktree）** | 多会话 / 并发 iterate 对同一仓库写入冲突；用独立 worktree 隔离「审查/修复」工作区，失败即弃 | 高 | 中-高 |
| 5 | **速率限制 / 预算熔断** | 长循环（20 轮封顶）费用不可控；按预算上限熔断 + 提前止损，呼应 v1.7 精确计费的逆操作 | 中-高 | 低-中 |
| 6 | **HTML 报告服务化** | 现有 `--html` 单文件可发给协作者；补「静态服务 + 轮次回放」便于评审委员会使用 | 中 | 低 |

**未列入高价值的原因（节选）**：皮肤/主题（与社区同质化，§14.4 已否）、更多 prompt 预设（可由 skill 侧配置达成）、多语言报告（价值存疑）、离线模型（超出 harness 范围）。

> **落地建议**：#1 与 #5 属「配置层增强」，可并入下一 patch/minor 版本；#2 与 #3 属「运行时体验」，建议单独 minor 版本做扎实验收；#4 涉及工作区模型变更，需先行设计（对齐 §11.4.1 架构）。

### 15.4 完整 28 项候选清单与逐项实现状态（v1.37：全量固化，不再只记录高价值子集）

> 本节把 §15.3 提到的「28 项候选」**完整列出**，并为每一项标注来源、价值、成本与**当前代码实现状态**。相比 §15.3 只固化了 6 项高价值明细，这里补全了其余 22 项（含低价值 / 超范围 / 由 skill 侧达成 / 已否定的项），作为后续迭代的完整输入。每项状态截至 v1.37（当前发布 1.9.4）。

| # | 功能 | 来源 | 价值 | 成本 | 实现状态（v1.37） | 落点 |
|---|---|---|---|---|---|---|
| 1 | 自定义模型提供方（BYOK） | 代码缺口 | 高 | 低 | ✅ **已实现**（1.9.3） | `config/settings.py` ProviderProfile + 10 档默认 profile；`ih provider add` / `/model` |
| 2 | 收敛仪表盘进 TUI | UX 缺口 | 高 | 中 | ✅ **已实现**（1.9.3） | `ReviewProgressEvent` → `ReviewProgressPanel.tsx`（sparkline / 分维度计数 / 累计费用） |
| 3 | 失败自愈 / 断点续跑 | UX 缺口 | 高 | 中 | ✅ **已实现**（1.9.3） | `iterate/checkpoint.py` + `last_state.py`；`/iterate resume` |
| 4 | session 工作区隔离（sandboxed worktree） | 代码缺口 | 高 | 中-高 | ✅ **已实现**（1.9.3） | `worktree_flow.py` + `worktree_runtime.py` + `swarm/worktree.py` |
| 5 | 速率限制 / 预算熔断 | 代码缺口 | 中-高 | 低-中 | ✅ **已实现**（1.9.3） | `loop_policy.py` total_token_budget / budget_usd / max_turns_per_minute |
| 6 | HTML 报告服务化 | 功能缺口 | 中 | 低 | ✅ **已实现**（1.9.3） | `report_server.py` + `html_report.py`（静态服务 + 轮次回放页）；`/iterate report --serve` |
| 7 | TUI 趋势库入口 | UX 缺口 | 中 | 低 | ✅ **已实现**（历史版本） | `commands/iterate.py` `/iterate trend` 与 `/iterate log trend` → `trend_store.render_trend_summary` |
| 8 | known_intentional 本轮即应用 | UX 缺口 | 中 | 中 | 🔲 待实现 → 本次 v1.37补充 | 迭代循环结束自动持久化筛选结果至 config（见 §16 配套） |
| 9 | 常见失败自愈文档章节 | UX 缺口 | 中 | 低 | 🔲 待实现 → 本次 v1.37补充 | README / docs 增「常见失败场景自愈指南」（TLS / 认证 / 配额） |
| 10 | 更多 prompt 模板预设 | 功能扩展 | 中 | 中 | 🔲 待实现 → 本次 v1.37补充 | `prompts.py` 内置多套模板；CLI `--template` 切换 |
| 11 | 多语言报告 | 功能扩展 | 低 | 低 | 🔲 待实现 → 本次 v1.37补充 | 报告支持中文 / 英文输出 |
| 12 | 离线模型支持 | 功能扩展 | 低 | 中 | 🔲 待实现 → 本次 v1.37补充 | 本地模型接入适配层（openai-compatible / 本地端点） |
| 13 | 主题 / 皮肤 | 功能扩展 | 低 | 低 | ✅ **已实现**（历史版本） | `themes/`（5 内置主题 default/dark/minimal/cyberpunk/solarized + 自定义 `~/.iterate-harness/themes`）；CLI `--theme` 与 Settings.theme |
| 14 | 批量仓库审查 | 功能扩展 | 低 | 高 | ✅ **已实现**（历史版本） | `iterate/batch.py`（多仓库顺序审查 + 严重度加权排名） |
| 15 | 审查结果导出（PDF/Excel） | 功能扩展 | 低 | 低 | 🔲 待实现 → 本次 v1.37补充 | report 增 CSV 导出（Excel 可开）；PDF 由 CSV/HTML 转化 |
| 16 | 审查历史可视化回放 | 功能扩展 | 低 | 中 | ✅ **已实现**（1.9.3 + 历史） | `replay.py`（log --replay）+ `html_report.build_replay_page` 交互式回放页 |
| 17 | 自动修复预演（dry-run diff 预览） | 功能扩展 | 中 | 中 | ✅ **已实现**（历史版本） | `query.py` 逐修复 diff 审批 `_needs_iterate_fix_approval` / `require_fix_approval`（M6a） |
| 18 | 审查结果对比（两次迭代 diff） | 功能扩展 | 中 | 中 | 🟡 部分覆盖 | `trend_store.py`（new/fixed/regressed/stubborn）跨运行分类；无显式两次 run 并排 diff |
| 19 | 多分支并发审查 | 功能扩展 | 中 | 中 | 🟡 部分覆盖 | 依赖 #4 worktree 隔离可并发；无显式每分支专用入口 |
| 20 | 审查结果自动提交 PR | 功能扩展 | 中 | 中 | ✅ **已实现**（历史版本） | `pr_comment.py`（PR 评论写入） |
| 21 | 审查结果 Slack/飞书推送 | 功能扩展 | 低 | 中 | 🔲 待实现 → 本次 v1.37补充 | 通用 webhook 通知器（Slack Incoming Webhook / 飞书自定义机器人） |
| 22 | 自定义审查维度 | 功能扩展 | 中 | 中 | 🟡 部分覆盖 | `config_loader.parse_dimension_resources` 已有维度资源配置；缺 TUI/CLI 编辑维度定义 UI |
| 23 | 审查结果缓存 | 功能扩展 | 低 | 低 | ✅ **已实现**（历史版本） | 增量审查 `--changed`（changed-only quick review） |
| 24 | 审查结果权限控制 | 功能扩展 | 低 | 低 | ✅ **已实现**（历史版本） | 文件级路径白名单 / 权限最小化已固化 |
| 25 | 审查结果搜索 | 功能扩展 | 低 | 低 | ✅ **已实现**（历史版本） | 决策日志 `log <n>` tail + grep（自述可由 grep 达成） |
| 26 | 交互式修复拒绝/接受 | 功能扩展 | 中 | 中 | ✅ **已实现**（历史版本） | `known_intentional` 筛选 + `require_fix_approval` 逐修复审批门（M6a） |
| 27 | 审查结果导出到 CI/CD | 功能扩展 | 中 | 中 | ✅ **已实现**（历史版本） | `ci_report.py` `--github`（GitHub Actions workflow commands）+ `--fail-on` 门禁 |
| 28 | 审查结果自动回滚 | 功能扩展 | 低 | 高 | 🔲 不实现（风险高） | 保留「不建议」结论：自动回滚风险高于价值（数据丢失），由人工 revert 兜底 |

**实现状态小结（v1.37 增量前）**：已实现 ✅ 18 项（#1-7、#13、#14、#16、#17、#20、#23、#24、#25、#26、#27）；部分覆盖 🟡 3 项（#18、#19、#22）；超范围 / 已否定 / 不建议 1 项（#28）。**本次 v1.37 新增实现 7 项**（#8、#9、#10、#11、#12、#15、#21），并对 3 项部分覆盖项（#18、#19、#22）做最小增强，最终使 28 项全部有明确落点。

> **设计规则回放**：凡「价值存疑 / 超范围 / 已否定」的项，若技术上可行且不违背安全偏好的（如 #12 离线模型可用 BYOK 的 openai-compatible 端点承接、#13 主题只做 CLI 语义色不做全局换肤），仍以最小实现落地；真正不可行或高风险项（#28）如实保留「不建议」。这符合「全部记录，并把所有项完整实现」的要求，同时不跨越安全红线。

## 16. 插件 UI 层落地细化（v1.34：基于 §14.4 决策的完整实现方案）

> 本节把 §14.4 的 6 项候选从「可行性论证」推进到「可直接编码的完整实现方案」：锁定技术底座、数据流、每项组件契约与验收标准，并新增后端闭环工具 `iterate_triage`（分诊写回）。**决策（用户 2026-08-16）**：6 项全部实现；客户端采用**静态免构建（build-free）**轨道。本节为本次 UI 层开发的权威记录。

### 16.1 技术底座（对齐 dsh-gui-customization 0.6.2 实证格式）

| 层 | 机制 | 实证依据 |
|---|---|---|
| 客户端加载 | `package.json.dsh.client = { inject: [], platform: 'web' }` + `exports["./client"]` 指向客户端入口 | gui-customization `package.json`：`"dsh": { "bundle": { "patch": … }, "client": { "inject": [], "platform": "web" } }` + `"./client": "./lib/client.js"` |
| 客户端模块契约 | 入口文件导出 `apply(ctx)`；由 dsh `clientModules` 扫描进 Web 启动图并调用 | gui-customization `src/client/index.ts` 导出 `export function apply(ctx)` |
| 服务访问 | `ctx.get('slots'|'theme'|'locale'|…)`，缺失即 `undefined`（可选服务，防御式降级） | 能力清单 §5 |
| React | build-free 下从 `ctx.React` / `window.React` 解析 `createElement`；解析失败仅禁用槽位 UI，不影响主题/CSS | 能力清单 §8 Client Builtins：`React`（createElement/useState/useEffect） |
| 样式注入 | `document.head.appendChild(<style data-plugin="iterate-ui">)`，`ctx.effect` 卸载时移除 | gui-customization 主样式注入同款 |
| 槽位注册 | `slots.inject(key, () => slots.register({ name, id, order, … }, render))`，返回 disposer | gui-customization 三处注册（settings.section / shell.overlay / settings.plugin.item） |
| 主题覆盖 | `theme.overrideTokens(source, { token: { light, dark } })` 返回 disposer；13 个令牌全部成对 | 能力清单 §7 |
| 事件订阅 | `ctx.on('slots/changed')` 等客户端事件 | 能力清单 §6（客户端事件仅 4 类） |

> **v1.34 实证结论（修正上版假设）**：dsh 客户端**只转发 4 类自有事件**（connection/reset、locale/change、slots/changed、theme/change），插件自定义的**后端 `ctx.emit` 事件不保证透传到客户端**。因此「进度事件联动」不再依赖后端事件桥接，改为**客户端自驱动**：订阅 `slots/changed` + 会话快照轮询（`useSession`），以 `convergence.totalRounds` 变化触发视觉脉冲——这是可用、诚实、零桥接的实现。

### 16.2 数据流（谁给 UI 供数）

```
iterate_review aggregate ──render──▶ JSON(ReviewReport) 落入会话 tool 消息
        │
        ▼
客户端取数（两条通道，均防御式深度扫描定位 Report）
  ├─ conversation.input.dock   (session 作用域)  → props.useSession() → 扫描会话快照
  └─ conversation.chat.turnTail(session 作用域)  → props.turn        → 扫描该回合
        │
        ▼
lib/parse.js（纯逻辑、无 DOM、框架无关、可单测）← 单一事实源
  parseReport / findReportInObject / computeConvergence / severityStats /
  groupByDimension / buildTriageState / hashReport / toKnownIntentionalYaml /
  buildApplyInstruction
```

- 判定「是 ReviewReport」的判据：对象同时含 `convergence`（对象）、`findings`（数组）、`rounds`（数组）。
- `normalizeReport` 对缺字段做默认值兜底（`totalRounds` 缺省取 `rounds.length`，summary 缺省从 findings 重算），保证任何合法 Report 都能渲染。
- 深层扫描带 `seen` 集合防循环引用 + `maxDepth` 上限，避免性能与栈风险。

### 16.3 六项实现逐一细化

| # | 槽位（kind） | 组件 | 行为 | 验收 |
|---|---|---|---|---|
| 1 | `conversation.input.dock`（list） | `ConvergenceDashboard` | 输入栏上方独占整行：`Round N/M`、收敛进度条（`progressPct`）、各维度 findings 计数徽章、四档严重度色点合计；无 Report 时渲染 null | 会话内出现 aggregate 报告后，输入栏上方实时显示收敛面板 |
| 2 | `conversation.chat.turnTail`（chain） | `TurnTailEntry`（内含分诊面板） | 逐条 findings 三态：`y`=保留修复（keep）/ `n`=跳过（skip）/ `a`=已知有意（ignore）；verdict 持久化 localStorage（按 `hashReport` 分 key）；底部「复制 known_intentional」+「生成应用指令」；「生成应用指令」产出给模型的 `iterate_triage` 调用文本 | 报告回合尾部出现可点选分诊面板，verdict 刷新后仍保留，复制/指令按钮产出正确 YAML 与 JSON 载荷 |
| 3 | 同上链 | `TurnTailEntry`（无 findings 时渲染统计卡） | 摘要卡：总 findings、四档分布、各维度 Top、收敛轮数/是否收敛 | 空 findings 报告显示统计卡而非分诊面板 |
| 4 | 主题令牌（无槽位） | `theme.overrideTokens('iterate', …)` | 13 令牌 × 明暗成对；暖琥珀主色（避绿/青/蓝紫，符合既有审美偏好），中性面微调；设置页开关可关（localStorage） | 换肤生效且可开关；`theme/change` 事件订阅保持开关状态一致 |
| 5 | `shell.overlay`（list） | `ProgressCapsule` | 轮次变更（totalRounds 增长）时：收敛面板「Round N/M」徽标做脉冲动画；overlay 胶囊短暂显示「Round N 完成 · findings -k」摘要 | 多轮收敛过程中轮次徽标动画触发，胶囊出现后自动消失 |
| 6 | `settings.section`（list） | `SettingsPanel` | 设置 → iterate：目标/最大轮数/维度概览（读会话最新 Report）、分诊持久化状态（读 localStorage）、主题开关、含「复制配置指引」按钮（产出给模型的配置调整指令） | 设置页出现 iterate 分区，信息与本地状态一致 |

### 16.4 后端闭环：`iterate_triage` 工具（新增，分诊写回的真正后端）

- **动机**：§16.3 #2 的 `a`（已知有意）需要真实写入 `iterate.config.yaml` 的 `personalization.known_intentional`，客户端浏览器无文件写权限，必须由模型经工具落盘——补齐「分诊闭环」的最后一段（§15.2「个性化闭环」缺口的 UI 侧落地）。
- **参数**：`operation: 'apply' | 'list'`；`entries`（apply）：`[{ file, line?, dimension, reason }]`，每个字段按 §3 校验（file/dimension 非空字符串、line 为正整数或省略、reason 非空）；`path`：项目根。
- **行为（apply）**：
  1. `loadConfig(projectRoot)` 读取现有配置，`personalization` 缺失则初始化；
  2. 备份现有 `iterate.config.yaml` → `.bak-<ISO 时间戳>`（失败回滚语义）；
  3. 以 `file|line|dimension` 为键去重合并（已存在则跳过）；
  4. 用 `js-yaml` 序列化写回（保持 `additionalProperties: false` 之外字段原样）；
  5. 返回 `{ operation, added, skipped, count, path, backupPath }`；写失败回滚备份。
- **行为（list）**：返回当前 `known_intentional` 全部条目。
- **测试**：`test/triage.test.ts` 覆盖正常路径（新增/去重/备份）、异常路径（非法 entry、无配置文件时新建、文件只读失败回滚）。
- 该工具与 `iterate_config`（只读）互补：读用 `iterate_config`，写用 `iterate_triage`，职责单一。

### 16.5 文件结构与配置变更（iterate-plugin 包）

```
harness/iterate-plugin/
  lib/
    parse.js        # 新增：纯逻辑（可单测）
    client.js       # 新增：客户端入口，导出 apply(ctx)，import parse.js
  src/
    tools/
      triage.ts     # 新增：iterate_triage 后端工具
    index.ts        # 改：注册 triage 工具
  test/
    parse.test.ts   # 新增：parse.js 单测
    triage.test.ts  # 新增：triage 工具单测
  package.json      # 改：dsh.client 声明 + exports["./client"] + files 加 lib + scripts
  tsconfig.json     # 改：allowJs + include lib
```

### 16.6 验证与风险

- **验证**：`npm run typecheck`；`npm test`（含新增 parse/triage 用例）；浏览器集成（安装进 dsh 后人工验收 §16.3 六项验收行）为运行时验证项，不在本环境。
- **风险与回退**：
  1. build-free 下客户端相对 ESM 导入（`client.js → parse.js`）若被 dsh 模块加载器拒绝 → 用包内已有 `esbuild` 一条命令把 parse.js 内联进 client.js（改 `exports["./client"]` 指向产物即可，逻辑零改动）；
  2. `ctx.React` / `window.React` 均不可得 → 主题/CSS 仍生效，仅槽位 UI 降级（日志提示）；
  3. 槽位 props 结构随 dsh 版本变化 → 所有组件均先「深度扫描定位 Report」，结构变化只影响扫描，不影响判定与渲染逻辑；
  4. `conversation.chat.turnTail` 为 chain，`select` 语义差异 → 组件自身对无 Report 的 turn 返回 null 兜底，避免误渲染所有回合。

### 16.7 验收清单（本次迭代）

- [ ] `lib/parse.js` 全部导出函数有单测覆盖（正常/异常/边界）
- [ ] `iterate_triage` 工具 apply/list 双路径 + 备份回滚有单测
- [ ] 客户端六项 UI 代码全部落地（无占位/无模拟数据）
- [ ] `npm run typecheck` 通过；`npm test` 全绿
- [ ] 变更提交并推送 GitHub（含本设计文档）

## 17. 独立 WebUI 管理台（v1.38：路线 B 的「活管理后端」）

> 本节为 iterate-harness（路线 B 独立 harness）新增「WebUI 完整管理台」的设计。**决策（用户 2026-08-17）**：完整管理台；技术栈 FastAPI + React；落地形态先独立 Web、后 Electron 壳；**自建、不拉取 DSH WebUI 代码**（DSH 仅作 UX 设计参考）。本节为本次 WebUI 开发的权威设计记录，后续迭代以其为输入。

### 17.1 背景与目标

**现状**：harness 已有完整 CLI（`ih ...`）与 TUI（`/iterate ...` 斜杠命令），以及 1.9.3 引入的**单文件 HTML 报告 + 交互式回放页**（[html_report.py](file:///Volumes/Eng-Dev/iterate-skill/harness/iterate-harness/src/iterate_harness/iterate/html_report.py)、[report_server.py](file:///Volumes/Eng-Dev/iterate-skill/harness/iterate-harness/src/iterate_harness/iterate/report_server.py)）。CLI / TUI / 静态报告三者已闭环，但缺少**活的、可交互的管理后端**：

| 现状能力 | 形态 | WebUI 补的缺口 |
|---|---|---|
| 迭代运行 | CLI/TUI | 浏览器查看/受控操作 |
| 收敛可视化 | TUI 面板 / 静态 HTML | 实时 web 仪表 |
| 决策日志（decision log） | 文件 | trajectory 式逐轮回放/检索 |
| checkpoint / 断点续跑 | CLI | 可视化列表 + 受控恢复 |
| 预算 / 限流 | CLI 日志 | 实时消耗仪表 + 熔断状态 |
| 配置 / provider | 文件编辑 | 受控 web 编辑（脱敏） |

**目标**：
1. 提供「完整管理台」：运行状态、决策日志回放、checkpoint 管理、预算仪表、配置管理一站式 web 界面。
2. 先独立 Web（本地服务 + 浏览器访问），验证价值后再包 Electron 桌面壳（§17.8）。
3. 复用既有数据层（decision log / trend store / checkpoint / config / report），**不重写业务逻辑**，只新增「读取 + 受控操作」的 web 层。

### 17.2 为什么自建，而不拉取 DSH WebUI 代码（决策论证）

用户曾提议「直接拉取 DeepSeek Harness（DSH）WebUI 代码二次开发以减少工作量」。经调研（2026-08-17，[deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)）：

| 维度 | 结论 |
|---|---|
| 许可证 | ✅ DSH 为 MIT，合规可用 |
| 是否独立前端 | ❌ 不是：它是 Cordis 插件系统的一部分，靠 WebSocket/RPC 与 Node 主机通信，UI 由 `apps/web` 承载 |
| 数据模型匹配 | ❌ DSH 用「会话 + trajectory 只增事件流」；harness 用「decision log + 收敛 + checkpoint + 预算」，模型不对应，桥接层仍需全量重写 |
| 稳定性 | ❌ 仍处 developer preview（v0.1.0-rc.5），官方明示有破坏性变更；fork 意味着冻结或持续跟进，双重维护 |
| 净工作量 | 前端拉来也省不了工：**数据/桥接层改写成本占大头**，还多背一份不需要的 UI 复杂度 |

**结论**：不整包拉取 DSH WebUI。**借鉴的只是它的 UX 设计语言**（trajectory 时间线、可回溯复盘、审批确认流），作为自建前端的设计参照，不拷贝代码。

### 17.3 功能范围（页面与能力）

| # | 页面 | 核心能力 | 数据来源 |
|---|---|---|---|
| P1 | Dashboard 仪表盘 | 运行状态卡片、收敛曲线（findings/round）、预算/限流实时仪表、最近报告入口 | decision log / loop_policy / cost meter |
| P2 | Runs 迭代详情 | trajectory 式逐轮时间线：round_start → review_result → atomic_fix / architectural_fix → revert → validation → decision；findings 表格；diff 展开 | decision log（`read_entries`） |
| P3 | Checkpoints | 断点列表、状态标签、恢复（受控操作，二次确认） | checkpoint / last_state |
| P4 | Workspaces | 工作区列表、隔离状态（worktree）、切换/选择 | worktree_runtime / 配置 |
| P5 | Budget & Rate | 累计 token / 美元预算、限流窗口、熔断状态 | loop_policy / cost meter |
| P6 | Config | iterate.config.yaml 只读预览 + 受控编辑（校验后写回、备份回滚）；provider / BYOK 管理（key 脱敏） | config/settings.py / auth/manager.py |
| P7 | Reports | 报告列表、HTML 报告内嵌预览、回放页入口 | report 目录 / html_report |
| P8 | Trend 趋势 | 逐轮 new / fixed / regressed / unchanged 历史、最新一轮变化明细、未解决与顽固（3+ 轮）问题、按维度汇总；随 SSE 决策条目实时刷新 | decision log（report 条目）+ trend-library |
| P9 | Gate 判定闸 | 最近一次配方闸回答、拒绝码与可执行补救、每一轮发布过的答案；缺失时明确写「尚未记录」而非通过 | decision log（`recipe-gate` 条目）+ 内核 gate |
| P10 | Schedules 定时任务 | 本机 cron 注册表、调度器存活、下次运行与最近执行（退出码/耗时/输出尾部）；登记/更新/暂停/删除计划 | cron registry / history |
| P11 | Doctor 自检 | 确定性、无网络的机器就绪度报告；失败/告警优先，每项带可复制 remedy | `doctor` 模块 |
| P12 | Capabilities 能力清单 | 工具/斜杠命令/技能/插件/MCP 配置的实际加载清单；静态 MCP 问题与可复制修复；类别筛选 + 搜索；永不启动服务器或模型 | `capabilities` 模块（与 `ih capabilities` 同源） |
| P13 | Audit 审计 | 控制台每一次写操作的完整台账（时间/操作/目标/参数摘要）：操作前缀 + 目标子串 + 起始时间筛选，分页，导出 Markdown / CSV / JSON；只读、与 `ih audit` 同源 | `audit` 模块（web-audit.jsonl） |
| P14 | Memory 记忆 | 项目记忆库：条目/大小/修改时间/描述，引擎相关度搜索排名，注入预览（与提示词同一条代码路径，点名截断），失效索引链接问题；新增/覆盖/删除（二次确认 + 审计）；只读面绝不创建记忆目录 | `memory` 模块（`ih memory` 同源） |
| P15 | Hooks 生命周期钩子 | 已注册钩子清单（事件/类型/来源/匹配器/命令或提示或 URL/超时/失败拦截/静态检查），未知事件名与跑不起来的命令/URL/空提示带可复制 remedy；执行台账（事件/类型/结果筛选、最新在前分页、Markdown/CSV/JSON 导出）；每事件「复制试运行命令」直达 `ih hooks test`；页面只读、永不启动钩子命令或模型 | `hooks` 模块（`ih hooks` 同源） |

**操作边界（安全默认）**：P2/P3/P6 涉及写操作（启动/停止/恢复 checkpoint/保存配置）一律「只读默认 + 显式确认 + 写入前备份 + 失败回滚」，与 CLI 既有语义一致。

### 17.4 后端设计（FastAPI）

**新模块**：`iterate_harness/web/`（镜像 CLI / `iterate` 分层，不跨层放文件）

| 文件 | 职责 |
|---|---|
| `web/api.py` | FastAPI 应用工厂 + 路由注册 + CORS（仅本机回环）+ 启动钩子 |
| `web/routes/status.py` | Dashboard 聚合接口 |
| `web/routes/runs.py` | decision log 列表 / 单 run 时间线 / findings / diff |
| `web/routes/checkpoints.py` | 断点查询 + 恢复操作 |
| `web/routes/config.py` | 配置读 / 校验写回 / provider 管理（脱敏） |
| `web/routes/reports.py` | 报告列表 / 内嵌预览 |
| `web/events.py` | SSE 实时推送（尾部读取 decision log 增量 + cost meter 增量） |
| `web/security.py` | 本机回环校验 / 路径白名单 / 操作审计日志（写入侧） |
| `web/routes/audit.py` | 审计台账读取：分页 / 筛选 / 导出（与 `ih audit` 共用 `audit` 模块） |
| `web/routes/memory.py` | 项目记忆库读取 / 注入预览 / 新增 / 删除（与 `ih memory` 共用 `memory` 模块，写路径审计 + 确认） |
| `web/routes/hooks.py` | 生命周期钩子清单 + 执行台账读取：分页 / 筛选（与 `ih hooks` 共用 `hooks` 模块） |
| `memory/inject.py` | 运行时提示词与注入预览共用的记忆段落构造器（单一实现，二者不可漂移） |
| `memory/inventory.py` | 记忆库只读清单 + 相关度排名 + 注入预览 + 单文件读取（`ih memory` / `GET /api/v1/memory`） |
| `hooks/journal.py` | 钩子执行台账：写入侧（`HookExecutor` 每跑一笔）+ 读取侧（`ih hooks log` / `GET /api/v1/hooks/log`），大小上限惰性轮转 |
| `hooks/inventory.py` | 已注册钩子只读清单 + 未知事件名与静态配置问题报告（命令不存在/URL 畸形/空提示；`ih hooks list` / `GET /api/v1/hooks` / capabilities 的 `hooks` 段） |
| `hooks/testing.py` | 钩子试运行（`ih hooks test`）：与引擎同一注册表、同一执行器、同一台账；command/http 真跑，prompt/agent 无模型时明确 skipped，`--dry-run` 绝不执行；`--require-match` 供 CI 断言 |

**关键路由契约（示例）**：

| Method | Path | 说明 | 返回 |
|---|---|---|---|
| GET | `/api/v1/status` | 运行状态 + 收敛 + 预算聚合 | `StatusResponse` |
| GET | `/api/v1/runs` | 决策日志概览（分页） | `RunSummary[]` |
| GET | `/api/v1/runs/{id}/timeline` | trajectory 式逐轮条目 | `TimelineEntry[]` |
| POST | `/api/v1/checkpoints/{id}/restore` | 恢复断点（审计 + 确认） | `OperationResult` |
| GET | `/api/v1/config` | 配置只读视图（key 脱敏） | `ConfigView` |
| PUT | `/api/v1/config` | 校验后写回（备份 + 回滚） | `SaveResult` |
| GET | `/api/v1/capabilities` | 工具/命令/技能/插件/MCP 实际加载清单 + 静态配置问题；只读、无网络 | `CapabilitiesView` |
| GET | `/api/v1/events?stream=status` | SSE 实时推送 | `text/event-stream` |
| POST | `/api/v1/schedules` | 登记/更新 canonical 定时快审（审计 + 确认，跨目录迁移需 `replace=true`，否则 409） | `OperationResult` |
| POST | `/api/v1/schedules/enabled` | 启用/停用一条已登记计划（审计 + 确认） | `OperationResult` |
| DELETE | `/api/v1/schedules` | 删除一条已登记计划（审计 + 确认） | `OperationResult` |
| GET | `/api/v1/audit` | 审计台账分页 + 操作/目标/时间筛选 + 操作类别清单；只读 | `AuditView` |
| GET | `/api/v1/audit/export` | 审计台账导出（Markdown / CSV / JSON，沿用筛选） | 下载（`X-Audit-Total`） |
| GET | `/api/v1/memory` | 项目记忆库：条目 + 相关度搜索排名 + 注入预览（`query`/`prompt`）；只读、绝不创建记忆目录 | `MemoryView` |
| GET | `/api/v1/memory/entry` | 单条记忆全文（越界名拒绝 404） | `MemoryEntryDetail` |
| POST | `/api/v1/memory` | 新增/覆盖记忆（审计 + 确认；覆盖已存在需 `overwrite=true`，否则 409） | `OperationResult` |
| DELETE | `/api/v1/memory` | 删除记忆并解除索引链接（审计 + 确认；`prune_index` 修失效链接） | `OperationResult` |
| GET | `/api/v1/hooks` | 已注册生命周期钩子清单 + 执行台账摘要（未知事件名带 remedy）；只读、无网络 | `HooksView` |
| GET | `/api/v1/hooks/log` | 钩子执行台账：`event`/`hook_type`/`success` 筛选，最新在前分页；非法 `success` 返回 422 | `HookLogView` |
| GET | `/api/v1/hooks/log/export` | 钩子执行台账导出（Markdown / CSV / JSON，沿用筛选、不分页） | 下载（`X-Hooks-Total`） |

**错误码约定**：`400` 参数非法 / `401` 未授权（非本机）/ `404` 资源不存在 / `409` 冲突（如恢复中再操作、把已有计划迁到另一目录未带 `replace`）/ `422` 校验失败 / `500` 内部错误（含日志 trace）。

**实时性**：采用 **SSE（Server-Sent Events）**——比 WebSocket 简单、单向推送足够；由 `events.py` 定时尾部读取 decision log 增量 + 轮询 cost meter，推送收敛更新。不新增消息总线，保持极简。

**安全（本机单用户形态）**：
1. 默认只绑定 `127.0.0.1`，不对外暴露；服务启动打印 URL。
2. CORS 仅允许本机回环 origin；所有写操作带 CSRF 校验。
3. 路径类参数一律做**路径白名单**校验（解析后落在报告/工作区目录内），防路径遍历。
4. API key 只回显脱敏描述符，永不明文回传；写配置沿用既有合并/备份/回滚语义。
5. 写操作记审计日志（时间 / 操作 / 参数摘要）。

### 17.5 前端设计（React）

**技术底座**：Vite + React 18 + TypeScript；路由 `react-router`；状态 `zustand`；请求统一 `fetch` 封装（`/api/v1`）。不引入 UI 框架，沿用项目「全局自定义配色系统」的偏好（不引入 liquid glass 类 API）。

**视觉语言**（对齐现有报告 + 借鉴 DSH UX）：
- 基调：浅色卡片 + 蓝灰边框（与 [html_report.py](file:///Volumes/Eng-Dev/iterate-skill/harness/iterate-harness/src/iterate_harness/iterate/html_report.py) 现有 `_BASE_CSS` 一脉相承）；severity 沿用固定色表（critical `#b91c1c` / high `#ea580c` / medium `#ca8a04` / low `#2563eb`）。
- 借鉴 DSH：**trajectory 时间线**（按轮堆叠、可回溯、每轮可展开 diff）、「每一步在做什么都摊开」的信息密度。
- 字体：系统 UI 栈 + 等宽 diff。

**页面路由**：

| 路由 | 页面 |
|---|---|
| `/` | Dashboard |
| `/runs/:id` | Runs 详情（时间线） |
| `/checkpoints` | Checkpoints |
| `/workspaces` | Workspaces |
| `/budget` | Budget & Rate |
| `/config` | Config |
| `/reports` | Reports |
| `/trend` | Trend（`g t`） |
| `/diff` | Run diff（`g v`） |
| `/gate` | Gate（`g j`） |
| `/schedules` | Schedules（`g s`） |
| `/capabilities` | Capabilities（`g n`） |
| `/doctor` | Doctor（`g k`） |

**组件拆分**（示例）：`ConvergenceChart`（复用现有 SVG 曲线思路）、`TimelinePanel`、`FindingsTable`、`DiffViewer`、`BudgetMeter`、`ConfirmDialog`（受控操作二次确认）。

### 17.6 依赖与许可核查

| 依赖 | 版本策略 | 许可 | 合规 |
|---|---|---|---|
| fastapi | 精确锁定 | MIT | ✅ |
| uvicorn | 精确锁定 | BSD-3-Clause | ✅ |
| sse-starlette（可选 SSE） | 精确锁定 | BSD-3-Clause | ✅ |
| react / react-dom | 精确锁定 | MIT | ✅ |
| vite（dev） | 精确锁定 | MIT | ✅ |
| react-router | 精确锁定 | MIT | ✅ |
| zustand | 精确锁定 | MIT | ✅ |

**全部为宽松许可，无 GPL/AGPL/SSPL 强传染依赖**，符合项目依赖准入规则。新增依赖以精确版本号锁定（禁止 `latest` / `*` / `^` 模糊范围），具体版本号在实现时 resolve 后固化。

### 17.7 目录结构与文件

```
harness/iterate-harness/
├── web/                        # 后端（iterate_harness/web/ 源目录）
│   └── iterate_harness/web/    # api.py / routes/ / events.py / security.py
└── frontend/web/               # React 前端（镜像既有 frontend/terminal 模式）
    ├── package.json
    ├── vite.config.ts
    └── src/                    # 页面 / 组件 / api client / store
```

**打包**：沿用 [pyproject.toml](file:///Volumes/Eng-Dev/iterate-skill/harness/iterate-harness/pyproject.toml) 既有 `force-include` 机制（`frontend/terminal` → `iterate_harness/_frontend` 的先例），构建后的 `frontend/web/dist` 静态资源 force-include 进 wheel，由 FastAPI `StaticFiles` 托管；`ih web`（或 `iterate web`）子命令一键拉起服务并开浏览器。

### 17.8 Electron 壳（第二阶段，本版不实现）

- **形态**：Electron 主进程负责拉起/连接本地 FastAPI 服务（若未运行则 spawn 子进程）、管理窗口（独立窗口 + 系统托盘 + 系统通知 + 开机自启）；渲染进程只加载 `http://127.0.0.1:<port>` 的 WebUI。
- **职责划分**（符合桌面客户端专项规则）：渲染进程禁止直接调用 Node 系统 API，一律经 IPC → 主进程 → FastAPI；窗口/托盘/通知由主进程负责。
- **前提**：Web 版（§17.3-17.5）落地并验证价值后再投入；本节仅锁定形态与边界，不展开实现细节。

### 17.9 里程碑与验收

| 里程碑 | 内容 | 验收 |
|---|---|---|
| M1 | 后端只读 API + Dashboard + Runs 时间线 | 接口单测；页面可查真实 decision log |
| M2 | 受控操作：checkpoint 恢复 / 运行启停 | 操作二次确认 + 审计 + 回滚测试 |
| M3 | Config 管理 + Budget 仪表 + Reports 内嵌 | 配置校验写回测试（含备份/回滚） |
| M4 | Electron 壳（第二阶段） | 托盘/通知/窗口闭环；渲染进程无 Node API 直调 |

**质量门**（对照项目规则）：
- 所有后端路由/业务函数配套单测，覆盖正常/异常/边界（含 400/401/404/409/422/500）。
- 写操作全部走「校验 → 备份 → 写回 → 失败回滚」，有单测。
- ruff 零告警、mypy 零错误；前端 `npm run typecheck` + `npm test` 全绿。
- 无占位 / 无模拟数据；决策日志等一律读真实文件。

### 17.10 风险与开放问题

1. **端口占用 / 多实例**：`ih web` 需处理端口冲突（已占用时自动换端口并提示）。
2. **运行中状态读取一致性**：SSE 尾部读取需处理 decision log append-only 语义（只追加、不重写），实现时以文件尾部游标推进。
3. **Electron 打包体积与分发**：第二阶段再评估（electron-builder 等），本阶段不引入。
4. **是否纳入独立仓库同步**：沿用 `jingzhao-l/iterate-harness` subtree 同步流程，WebUI 随主仓库演进。

## 18. 对话界面：人类-in-the-loop 控制（v1.39：WebUI 迭代，面向 iterate 垂直领域）

> 本节为 v1.38 独立 WebUI 管理台的迭代增量。**决策（用户 2026-08-17）**：WebUI 主体不是对话，但对话仍需保留用于确认决策、状态更新、处理模型惰性（中途停滞需要用户督促/补充信息）。不强制复刻业界通用对话式 agent 界面，匹配 iterate 专用垂直领域做定制创新。

### 18.1 背景与目标

**现状（v1.38 WebUI）**：已实现仪表盘/运行时间线/checkpoint/预算/配置/报告全量只读+受控操作，但缺少「动态人类介入通道」：
1. 模型存在惰性：多轮迭代中可能出现「停止不动、卡住、重复无新发现」，需要用户通过对话督促/注入补充提示。
2. 引擎设计本身需要：`AskUserPrompt/AskUserSelect/PermissionPrompt` 三个人类交互通道在 TUI/CLI 已闭环，但 WebUI 尚未提供。
3. iterate 循环需要启动/暂停：用户可从 WebUI 直接启动 `review/run/resume`，而不是切回 CLI/TUI。
4. 停滞感知与干预：轮次边界检测到连续零新发现时，主动挂起并等待用户决策（继续/跳过/停止/补充提示）。

**目标**：
1. 在 WebUI 管理台中嵌入**侧边对话面板**（而非主体全对话）——匹配「主体是管理台，对话是辅助干预」的 iterate 垂直定位。
2. 复用引擎既有的人机交互契约（三通道），不重写引擎逻辑，只做 Web 适配。
3. 支持四种场景：
   - 用户主动发起：从 WebUI 输入提示注入循环；
   - 引擎主动询问：模型通过 `ask_user_question` 工具提出问题，WebUI 弹出输入框收集回答；
   - 停滞自动暂停：`IterateLoopPolicy` 检测到连续 0 新发现 → 暂停 → 等待用户决策；
   - 启停控制：WebUI 一键 `start review/run/resume` → 实时推送 `ReviewProgressEvent` → 用户观测 → 干预。

### 18.2 架构决策（为什么是侧边面板，不是主体对话）

| 方案 | 适配 iterate 垂直领域？ | 优点 | 缺点 | 结论 |
|---|---|---|---|---|
| 全页对话（DSH 风格） | ❌ 主体错配 | 业界标准方案 | iterate 核心是「多轮收敛审查 → 修复 → 验证」，不是自由对话；管理仪表盘/时间线/checkpoint 都挤不见了 | 不选 |
| 底部浮动对话框 | ❌ 信息密度低 | 不占主空间 | 历史对话看不到，长对话无法回溯 | 不选 |
| **右侧侧边面板（可折叠）** | ✅ 匹配定位 | 主空间留给管理台（仪表盘/时间线），对话始终可见可追溯；折叠后不占空间 | 需要处理窄屏响应式 | 选 |

**垂直领域创新点**（相对于通用对话 agent）：
- 对话角色分工清晰：**模型产出审查/修复 → 用户只做决策/督促/补充**，不是自由闲聊；
- 对话历史只记录「干预交互」，不是全量 prompt 历史（全量在 decision log，这里只记人类干预）；
- 「暂停等待用户」是核心场景 → 轮次边界主动挂起，UI 高亮提示用户输入；
- 支持「督促注入」快捷短语：「继续，请寻找新发现」「请聚焦 XXX 维度」等，一键发送。

### 18.3 后端设计（FastAPI 新增路由）

**新模块/路由**：复用现有 `iterate_harness/web/` 结构，新增 `web/routes/chat.py` 和 `web/schemas/chat.py`。

| 文件 | 职责 |
|---|---|
| `web/routes/chat.py` | 启动循环 (`POST /start`)、状态查询 (`GET /status`)、发送用户消息 (`POST /message`)、暂停/继续 (`POST /control`)、历史对话列表 (`GET /history`) |
| `web/schemas/chat.py` | Pydantic 模型：`ChatMessage` (role/content/timestamp)、`IterateRunStatus` (state/currentRound/newFindings/totalCost)、`StartRequest` (mode/subcommand/changed/ref)、`ControlRequest` (action) |
| `web/events.py` 扩展 | 现有 SSE 流新增 `chat-message` 事件类型（实时推送引擎生成的系统消息/提问） |

**运行状态机**（对齐引擎既有契约）：

```
idle → starting → running → paused (user_input_needed) → running
                         paused → stopped (done/failed)
```

| 状态 | 含义 | 可操作 |
|---|---|---|
| idle | 无运行中循环 | start review/run/resume |
| starting | 正在启动引擎 | （等待） |
| running | 循环正在推进 | pause / stop |
| paused | 暂停，等待用户输入/决策 | send message / resume / stop |
| stopped | 运行已结束（完成/失败） | （不可操作，查看结果） |

**关键接口契约**：

| Method | Path | 说明 | Request / Response |
|---|---|---|---|
| POST | `/api/v1/chat/start` | 启动 iterate 循环 | `{mode: "review"/"run", changed: bool, ref: string}` → `{runId: string, status: "starting"}` |
| GET | `/api/v1/chat/status` | 查询当前运行状态 | → `{state: RunState, round: int, newFindings: int, totalFindings: int, costUsd: float, waitingFor: "user_prompt"/"user_select"/"permission", question: string?}` |
| GET | `/api/v1/chat/history` | 获取对话历史（仅人机交互） | → `ChatMessage[]` |
| POST | `/api/v1/chat/message` | 发送用户消息（回答提问/注入督促） | `{content: string}` → `{ok: true}` |
| POST | `/api/v1/chat/control` | 控制命令（pause/resume/stop） | `{action: "pause"/"resume"/"stop"}` → `{ok: true, newState: RunState}` |

**引擎集成路径**（复用既有 runtime，不重写）：
1. Web 启动 → `build_runtime()` 组装 `RuntimeBundle` → 替换 `ask_user_prompt/ask_user_select/permission_prompt` 为 Web 版回调 → 回调通过 `awaitable` 挂起等待 WebUI 用户输入 → 用户提交 → 唤醒继续。
2. 所有 `StreamEvent`（含 `ReviewProgressEvent`）通过 SSE 推送到前端 → 前端实时更新状态面板。
3. 对话历史（仅人机交互）持久化到 `.iterate/web-chat.jsonl` 追加写入，重启可恢复。

**安全设计**（延续 §17.4 安全模型）：
1. 路径校验：启动的项目 root 必须是已存在目录，通过 `resolve_within` 校验防止遍历。
2. 审计日志：所有写操作（start/stop/send message）记入 `.iterate/web-audit.jsonl`。
3. 单运行约束：同一时间只允许一个 iterate 循环运行，防止并发冲突。

### 18.4 前端设计（React 增量）

**布局**：现有 WebUI 布局扩展为三栏（可折叠）：
- 左：导航（不变）
- 中：主内容区（仪表盘/runs/checkpoints 等，占 65-70% 宽度）
- 右：**对话面板**（可折叠，默认展开当有运行时，折叠宽 48px 只显示图标 + 未读红点）

**对话面板组件**：

| 组件 | 职责 |
|---|---|
| `RunStatusCard` | 显示当前状态（running/paused/stopped）、当前轮次、新发现数、累计成本、等待提示 |
| `ChatMessageList` | 滚动对话历史，区分角色：system（引擎状态）、assistant（模型提问）、user（用户输入） |
| `UserInputBar` | 文本输入框 + 快捷短语按钮（"继续，请寻找新发现" / "请聚焦 XXX" / "停止当前运行"） |
| `DecisionDialog` | 当引擎需要选择（`AskUserSelect`）时弹出模态框，展示选项供用户点击选择 |
| `PermissionDialog` | 当需要审批确认（`PermissionPrompt`）时弹出，展示 diff 摘要 + 确认/取消按钮 |

**状态管理**（Zustand 扩展 `store.ts`）：
- `chat.messages`: 对话历史数组
- `chat.runState`: 当前运行状态机状态
- `chat.currentRound`: 当前轮次数
- `chat.waitingFor`: 正在等待何种用户输入（prompt/select/permission/none）
- `chat.currentQuestion`: 当前等待的问题文本
- `chat.connectionState`: SSE 连接状态（connected/disconnected/reconnecting）

**SSE 事件扩展**（现有 `events.ts` 新增类型）：
- `chat-message`: 推送新聊天消息 → 追加到 `chat.messages`
- `run-state-change`: 运行状态变更 → 更新 `chat.runState`
- `progress-update`: 实时更新轮次/发现/成本 → 更新状态卡片

**UX 特性**（垂直领域定制）：
1. **可折叠侧边**：不使用对话时可折叠，最大化主内容区；
2. **未读提醒**：引擎等待用户输入时，折叠状态显示红点提醒；
3. **快捷短语**：预置「继续寻找新发现」「请聚焦 XXX 维度」「停止当前运行」，用户点击即发送，减少打字；
4. **自动滚动**：新消息到来自动滚动到底部；
5. **响应式**：窄屏（手机/小窗）自动全屏对话，返回按钮折叠回侧边。

### 18.5 停滞检测与主动暂停

**检测逻辑**（嵌入 `IterateLoopPolicy.on_turn_end`）：
- 连续两轮 `new_findings == 0` 且未收敛 → 触发自动暂停；
- 已配置 `token_budget/budget_usd` 且剩余不足一轮 → 在耗尽前一轮触发暂停，询问用户是否追加预算；
- 暂停行为：设置 `paused = True` → 向对话面板推送系统消息 "检测到连续无新发现，已暂停。请指示：继续/跳过当前轮/停止/" → 等待用户决策。

**用户决策选项**（预置快捷按钮）：
- ▶️ **继续**：沿用原下一轮指令继续；
- ⏭️ **跳过当前发现**：注入指令跳过当前回合卡住的发现，进入下一轮；
- ✋ **停止**：终止当前运行，生成最终报告；
- 💬 **补充提示**：用户输入自定义提示注入循环。

### 18.6 依赖与许可核查

| 依赖 | 现有/新增 | 许可 | 合规 |
|---|---|---|---|
| fastapi | 已有 | MIT | ✅ |
| uvicorn | 已有 | BSD-3-Clause | ✅ |
| react/react-router/zustand | 已有 | MIT | ✅ |
| **无新增依赖** | - | - | ✅ |

全部为宽松许可，无 GPL/AGPL/SSPL 强传染依赖，符合项目依赖准入规则。

### 18.7 目录结构与文件

```
harness/iterate-harness/
├── src/iterate_harness/web/
│   ├── routes/chat.py          # 新增：对话/运行控制路由
│   ├── schemas/chat.py         # 新增：Pydantic 模型
│   └── events.py               # 修改：扩展 SSE 事件类型
└── frontend/web/
    └── src/
        ├── pages/Chat.tsx     # 新增：对话面板页面（嵌入布局）
        ├── components/       # 新增：RunStatusCard / ChatMessageList / DecisionDialog
        ├── store.ts          # 修改：扩展 chat 相关 state
        ├── api.ts            # 修改：新增 chat API 客户端
        └── App.tsx           # 修改：布局集成侧边面板
```

### 18.8 里程碑与验收

| 里程碑 | 内容 | 验收 |
|---|---|---|
| M1 | 后端：启动/状态/消息/控制路由 + 运行状态机 + SSE 扩展 | 单测覆盖所有状态转移 + 异常路径；启动 → 暂停 → 继续 → 停止全流程可跑通 |
| M2 | 前端：侧边面板 + 状态卡片 + 对话列表 + 用户输入 + SSE 订阅 | 页面布局正确；折叠/展开正常；状态实时更新；不同等待类型（prompt/select/permission）UI 正确弹出 |
| M3 | 停滞检测：连续零新发现自动暂停 + 用户决策快捷按钮 | 检测触发时机正确；决策注入指令正确进入引擎循环 |
| M4 | 全链路端到端 | `ih web serve` 启动 → WebUI 打开 → 启动 `review` → 观测实时进度 → 暂停 → 发送用户消息 → 继续 → 停止 → 对话历史持久化 |

**质量门**：
- 后端：ruff 零告警、mypy 零错误；所有新路由有单测（覆盖正常/异常/边界）；
- 前端：`npm run typecheck` 零错误；无占位实现，所有分支逻辑完整；
- 安全：所有用户输入做校验；路径遍历防护；敏感信息不回传；审计日志完整。

### 18.9 风险与开放问题

1. **长轮次内存**：`RuntimeBundle.engine` 持有全量对话消息，多轮后内存增长可控吗？→ iterate 天然有 `max_rounds` 上限，内存增长在预期范围内；
2. **多标签页并发**：多个浏览器标签页同时连接 → SSE 多连接状态同步靠后端单运行约束保证，最后启动者抢占，前面标签页会收到 "another run already active"；
3. **阻塞等待用户输入**：`ask_user_prompt` 回调挂起 async 任务 → 后端进程阻塞等待，这是预期行为（和 TUI 一样），不影响其他 API 只读请求。

## 19. WebUI 迭代：工作区 / Findings 分诊 / 健壮性（v1.40：WebUI 迭代，落地 §17.3 遗留能力 + 管理台健壮性）

> 本节为 v1.39 对话面板的迭代增量。**决策（用户 2026-08-17）**：全量实现 §17.3 规划中尚未落地的 P2 Findings 分诊与 P4 工作区管理，同时为管理台补齐健壮性（错误边界 / 骨架屏 / 键盘快捷键 / SSE 断线兜底 / 浏览器通知）。对话面板新增工具调用可视化，让模型的工具活动可被用户直接感知。

### 19.1 背景与目标

**现状（v1.38/v1.39 WebUI）**：管理台已覆盖 Dashboard / Runs / Checkpoints / Budget & Rate / Config / Reports 与对话侧边面板，但存在以下功能缺口：
1. **Findings 分诊（P2 缺口）**：Runs 页能看 findings 表格，但无法对单条 finding 做「批准/拒绝」决策并持久化——无法表达「这条修复意见我认可 / 这是误报」的人类判断。
2. **工作区管理（P4 缺口）**：`worktree_isolation` 开启后每轮产生隔离 worktree，但没有可视化入口查看主工作区与各 worktree 状态、清理陈旧 worktree。
3. **对话工具可视化（§18 增量）**：对话面板只显示文本消息，模型调用工具（审查/修复/验证）的过程不可见，用户难以判断「它现在在干什么」。
4. **健壮性缺口**：单个页面渲染异常会整页崩溃；数据加载无骨架屏；无键盘导航；SSE 断线后状态静默停滞，用户无法区分「没新事件」与「连接断了」。

**目标**：
1. Findings 分诊：Runs 页每条 finding 可批准/拒绝，决策持久化到 `.iterate/findings-triage.jsonl`，可筛选已分诊项、可一键清除全部决策；
2. 工作区管理：新页面列出主工作区 + 隔离 worktree（git 元数据 / 隔离配置 / 决策日志规模），支持删除陈旧 worktree（防路径遍历 + 二次确认 + 审计）；
3. 工具调用可视化：对话消息中工具执行渲染为状态卡片（执行中 / 完成 / 空闲）；
4. 健壮性：ErrorBoundary 防整页崩溃、Skeleton 骨架屏、`g <key>` 快捷键 + `/` 或 `Cmd/Ctrl+K` 切换对话、SSE 断线轮询兜底、连接状态 toast、等待人类决策时浏览器通知。

### 19.2 Findings 分诊（落地 §17.3 P2）

**后端**（`web/findings_triage.py` 新增 + `web/routes/runs.py` 扩展）：

| 项 | 设计 |
|---|---|
| 存储 | `.iterate/findings-triage.jsonl` append-only 日志，镜像 `security.AuditLog` 模式；`(file, line, dimension)` 去重键，**最新一条生效**（重复分诊只追加不改写历史） |
| 端点 | `GET /runs/findings/triage`（全部决策，最近优先）、`POST /runs/findings/triage`（记录，需 `confirm=true` + 审计）、`DELETE /runs/findings/triage`（清除全部，需 `confirm=true` + 审计） |
| 请求模型 | `FindingsTriageRequest{file, line?, dimension, decision: "approve"|"reject", note?}`（decision 用 `Literal` 限定） |
| 健壮性 | 读取对损坏行防御（跳过非 JSON / 非 dict / 空 key）；写入 best-effort 永不抛；非法 decision 抛 `ValueError` |
| 语义 | `approve`=同意该 finding / 接受其修复建议；`reject`=误报 / 跳过修复。与 §18 引擎暂停菜单的审批互补：这是**人类对历史 run 的持久记录**，引擎审批是**进行中 run 的实时决策** |

**前端**（`pages/Runs.tsx`）：findings 表格每行追加「批准 / 拒绝」按钮（busy 态禁用），分诊成功后即时反映到行状态；新增「仅看已分诊」筛选与「清除全部决策」操作（二次确认对话框）；初始化时加载全部已存决策并按去重键映射。

### 19.3 工作区管理（落地 §17.3 P4）

**后端**（`web/routes/workspaces.py` 新增）：

| 项 | 设计 |
|---|---|
| 列表 | `GET /workspaces`：主工作区（kind=primary，含隔离配置开关 / 决策日志规模 / config 是否存在 / git 元数据：分支、HEAD、dirty）+ 每个 `original_path` 匹配项目根的隔离 worktree（kind=worktree，含 slug / branch / agent_id / created_at / 轮次） |
| 删除 | `POST /workspaces/remove`：`{slug}`，先经 `swarm.worktree.validate_worktree_slug` 校验（拒绝绝对路径 / `.`/`..` 段 / 非法字符，防路径遍历），需 `confirm=true`，删除成功写审计日志；不存在返回 404。**陈旧判定**：仅当该 worktree 的轮次小于本项目最新轮次（`detail.stale=true`）时才允许删除，避免删除当前活跃轮次的沙箱 |
| 读容错 | git 元数据 best-effort（非 git 目录 / git 不可用时字段为 null/False，页面优雅降级）；worktree 列表读取失败返回 500 并带原因 |

**前端**（`pages/Workspaces.tsx` 新增 + `App.tsx` 路由）：卡片/表格展示主工作区与各 worktree（活跃状态、分支、创建时间、轮次）；删除走二次确认对话框，成功后刷新；加载态骨架屏、失败态错误提示。

### 19.4 工具调用可视化（§18 增量）

**前端**（`components/ChatPanel.tsx`）：`kind === "tool"` 的对话消息解析为工具调用卡片——工具名（等宽字体）+ 状态标签（执行中 / 完成 / 空闲）+ 时间戳 + 详情。状态以左侧色条区分（accent=执行中、绿=完成、中性=空闲），让用户一眼看到模型当前在执行哪类工具。

### 19.5 管理台健壮性

| 组件 | 实现 |
|---|---|
| `ErrorBoundary` | 类组件捕获子树渲染异常，展示错误卡片（图标 + 标题 + 详情 + 重试 / 刷新），`componentDidCatch` 记录错误；`App.tsx` 包裹全部路由 |
| `Skeleton` | `SkeletonRows` / `SkeletonCard` / `SkeletonTable` 骨架屏组件，数据加载期替代空白，减少布局抖动 |
| 键盘快捷键 | `App.tsx` 全局监听：`g <key>` 跳转导航（忽略输入框内按键）、`/` 或 `Cmd/Ctrl+K` 切换对话面板 |
| SSE 断线兜底 | `store.ts`：SSE 断开时启动 5s 轮询（`startPolling` 刷新 status + chat status），重连成功即停止；连接状态变化推送 toast（连接成功 / 已断开，正在轮询兜底） |
| 浏览器通知 | `store.ts`：当运行进入等待人类决策（`permission` / `user_select` / `user_prompt`）且状态变化时，请求通知权限并发送浏览器通知，提醒用户切回确认 |

### 19.6 里程碑与验收

| 里程碑 | 内容 | 验收 |
|---|---|---|
| M1 | Findings 分诊后端 + 前端 | 后端：GET/POST/DELETE 全路径单测（空列表 / 需 confirm / 记录并审计 / 最近优先 / 清除）；前端：批准/拒绝即时反映、筛选、清除二次确认 |
| M2 | 工作区后端 + 前端 | 后端：列表含主工作区、删除需 confirm、遍历 slug 被拒、不存在 404；前端：主工作区 + worktree 展示、删除刷新 |
| M3 | 工具调用可视化 | 对话面板工具消息渲染状态卡片，三类状态样式正确 |
| M4 | 健壮性四件套 | ErrorBoundary 捕获渲染错误可恢复；骨架屏在加载期显示；快捷键生效；SSE 断开进入轮询兜底并在重连恢复；等待人类决策时浏览器通知 |

**质量门**：
- 后端：`tests/test_web/test_routes.py` 新增 `TestFindingsTriage`（6 项）与 `TestWorkspaces`（4 项），全量 pytest 通过；
- 前端：`npm run typecheck` 零错误、`npm run build` 产出正常；
- 安全：分诊与工作区删除全部走 `confirm=true` + 审计；worktree slug 防路径遍历；敏感信息不回传。
## 20. v2.0 大版本：双模式架构（iterate 纯审查 / code 通用编程 agent + 防御式内核 + 多 agent 编排）

> v2.0（2026-09-02 设计启动）。本章在保留 v1 全部能力的基础上，为 harness 引入**双模式**架构：`iterate` 模式完整保留 1.x 纯审查迭代闭环；新增 `code` 模式，把 harness 从「iterate 专用引擎」升级为「自带 iterate 防御式编程纪律的通用编程 agent」，并启用完整多 agent 编排能力。本版为纯设计细化，不修改 harness 源文件。

### 20.1 背景与目标

#### 20.1.1 背景
- harness 1.x 已至稳定期（当前发布 1.11.0），功能围绕 iterate 审查迭代闭环趋于做尽：9 维度并行审查、分诊、原子/架构修复、验证、收敛、checkpoint、决策日志、趋势库、WebUI 等均已实现。
- 生态三项目（skill / harness / plugin）同期审视后确认：**harness 具备升级为通用编程 agent 的完整底层能力**（OpenHarness fork 内核 + 通用工具面 + 多 agent 编排），只是 1.x 把它约束在 iterate 垂直链路上。
- 用户方向确认：**不能完全脱离 iterate 的原有基础**——通用编程能力必须「融入 iterate 已有的框架与理念」，尤其深度贯彻**防御式编程**，而非另起炉灶。

#### 20.1.2 目标
1. 提供**双模式**切换：`iterate`（1.x 纯审查迭代，零破坏保留）/ `code`（通用编程 agent）。
2. code 模式深度融入 iterate 理念：**防御式编程成为 agent 每个动作的默认行为**，而非事后审查。
3. code 模式启用**多 agent 编排**：主模型可并行 spawn 多个 subagent，走 coordinator 模式。
4. TUI 模式切换对齐 opencode 交互：Tab 直切 + 竖向色条 + 底部模式文字。

#### 20.1.3 防御式编程概念界定（本轮认知修正）
- **防御式编程不是「审查-修复-验证-收敛」这个流程**，而是**编码时的心智模型**（软件工程经典定义）：
  1. **最小化假设**：假设事情会出错，主动预测并容忍问题，而非乐观假设「应该没事」。
  2. **信任边界验证**：数据从「不可信来源」进入代码的那一刻必须验证；内部状态可信任，**外部输入必须验证**。
  3. **快速失败、响亮失败（fail fast, fail loud）**：错误一发生立即停止、报错、回滚，绝不带病继续。
  4. **前置/后置条件 + 断言**：每个函数声明要求什么（前置）、保证什么（后置），用断言守卫假设。
- 与 iterate 的关系：iterate 已是防御式编程的一种实现，但只把「防御」用在**审查环节**；v2.0 把整套心智模型变成**通用 agent 每个动作的默认行为**。

### 20.2 模式模型：task_mode 与 permission_mode 分离

| 维度 | 取值 | 切换方式 | 决定什么 |
|---|---|---|---|
| `task_mode`（新增） | `code` / `iterate` | **Tab 直切**（空输入框时） | agent 干什么：通用编程 vs iterate 审查迭代闭环 |
| `permission_mode`（现有） | `default` / `plan` / `full_auto` | `/permissions`（已有） | 权限多宽松 |

- 两者正交：`task_mode` 决定任务类型，`permission_mode` 决定权限级别。
- 现有「空输入框 Tab 打开 permissions 选择器」逻辑改为「空输入框 Tab 直切 task_mode」；permissions 切换改由 `/permissions` 命令负责（语义干净）。
- 切换只改变**下一轮行为**，不中断当前进行中的操作；两种模式共享同一 `iterate.config.yaml` / 决策日志 / 趋势库 / checkpoint，数据天然打通。

### 20.3 双模式行为差异

#### 20.3.1 iterate 模式（1.x 完整保留）
- 系统 prompt 注入 iterate 闭环：9 维度并行审查 → 分诊 → 原子/架构修复 → 验证 → 收敛。
- 每轮注入「防御式检查点」：修复后自动验证、失败回滚、决策日志。
- 触发即走既有 `iterate_review` / `loop_policy` 收敛引擎，**1.x 行为零破坏**。

#### 20.3.2 code 模式（通用编程 agent + 防御式内核）
- 系统 prompt 注入通用编程能力（现有 tools 全可用：bash / file_read / file_write / file_edit / glob / grep / web_fetch / web_search / mcp / lsp / skill / todo / ask_user / cron / team / agent 等）。
- **防御式内核**（核心新增，作为 agent 默认行为而非可选审查）：

| 防御式编程原则 | 内核落地机制 | 相关既有模块 |
|---|---|---|
| 最小化假设 | 每个工具调用前 agent 显式声明「我假设什么成立」（文件存在 / git 干净 / 依赖就绪），harness 记录并校验，假设被证伪立即 fail | 决策日志（decision_log） |
| 信任边界验证 | 扩展现有权限层：读文件前验证路径白名单、执行前验证命令白名单、写文件前验证目标类型 | `permissions/checker.py` |
| 前置/后置条件 | 每个 tool 自带契约：前置（文件存在/依赖就绪）→ 执行 → 后置（语法/关键测试） | tools/base.py 契约扩展 |
| fail-fast + 原子事务 | 编辑进事务缓冲：改前快照 → 改后自动验证 → 失败自动回滚（worktree/checkpoint 机制下沉到每步） | `iterate/worktree_flow.py`、`iterate/checkpoint.py` |
| 不变量守护 | 项目级不变量（构建必过 / 核心 API 签名不变 / 安全边界不可绕）每次操作后增量检查，违反即中断+回滚 | 新增 invariant 模块（规划） |
| 自然收敛 | 改动集合周期触发轻量审查，决策日志全程记录，不收敛不宣布完成 | `iterate/loop_policy.py`、`iterate/review.py` |

- iterate 的 review / validate / rollback / converge **不再是显式循环，而是从上述机制自然涌现**：agent 改每一步都被防御，收敛是必然结果而非调度目标——这是「深度融合」而非「表面迁移」的关键。

### 20.4 能力审计：对照 OpenHarness 原始代码（多 agent / 通用编程）

> 审计基准：`.external/OpenHarness`（v0.1.9 稳定版，gitignored）与 `harness/iterate-harness` 逐文件对比。

#### 20.4.1 多 agent 能力（完整保留）
| 能力 | 状态 | 位置 |
|---|---|---|
| 主模型 spawn subagent | ✅ `agent` 工具（local_agent / remote_agent / in_process_teammate 三模式） | `tools/agent_tool.py` |
| 给运行中 subagent 发后续消息 | ✅ `send_message` 工具（继续/纠偏 worker，保留上下文） | `tools/send_message_tool.py` |
| 停止 worker | ✅ `task_stop` + `task_create/get/list/output/update` | `tasks/` 目录 |
| coordinator 编排模式 | ✅ 完整（并行 fan-out、合成 spec、continue vs spawn 决策、失败处理、`<task-notification>` 协议） | `coordinator/coordinator_mode.py` |
| 多 agent 运行时 | ✅ subprocess + in_process 双后端、mailbox、lockfile、permission_sync、team_lifecycle、worktree（与 OpenHarness 逐文件一致） | `swarm/` 全套 |
| agent 定义表 | ✅ 975 行（worker / explore / general-purpose 等） | `coordinator/agent_definitions.py` |

#### 20.4.2 通用编程工具（完整保留）
- bash / file_read / file_write / file_edit / glob / grep / web_fetch / web_search / mcp + mcp_auth / lsp / notebook_edit / skill / todo_write / ask_user_question / enter-exit_plan_mode / enter-exit_worktree / cron_* / team_* / remote_trigger / sleep / tool_search / config / brief —— **与 OpenHarness 逐文件一致**。

#### 20.4.3 缺失的 4 个外围扩展（不影响 code 模式编程核心）
| 缺失项 | 原 OpenHarness 内容 | 影响评估 | 决策 |
|---|---|---|---|
| `image_generation_tool` | 图像生成工具 | 低（编程 agent 边缘能力） | 可选补齐 |
| `autopilot/` | repo 级自动运行服务 | 低（持续运行扩展） | 可选补齐 |
| `channels/` | 11 种 IM 渠道（slack/telegram/feishu/qq 等）+ bus | 低（通信集成，非编程核心） | 可选补齐 |
| `vim/` | vim 键位模式 | 低（纯键位偏好） | 不补齐（与 iterate 生态 UI 定位不符） |

> 注：coordinator prompt 提到的 `subscribe_pr_activity` 在 OpenHarness 中也仅是「if available」文本，无实际实现，不算缺口。
> **审计结论：code 模式所需的全部通用编程 + 多 agent 编排能力已经在位，无需补核心，只需按需补齐外围扩展。**

### 20.5 code 模式的多 agent 编排

| 编排能力 | 落地 |
|---|---|
| 主模型并行 fan-out | `agent` 工具可用，worker 默认 `subagent_type=worker` |
| 继续/纠偏 worker | `send_message`（worker 保留上下文） |
| 防御式纪律下放 | worker 继承主会话防御内核：前置/后置校验、原子事务、不变量守护、决策日志 |
| 结果回收 | `<task-notification>` XML → 主模型合成 → 触发轻量审查收敛 |
| 团队管理 | `team_create/delete` + swarm team_lifecycle 保留 |

### 20.6 TUI 模式切换（对齐 opencode）

#### 20.6.1 交互规则
- 输入框**为空**时按 Tab → `code ↔ iterate` 循环直切（替换现有「打开 permissions 选择器」逻辑）。
- 输入框**非空**时按 Tab → 保持现有补全/跳格行为，不冲突。
- 切换后前端立即刷新 UI，同时发 `set_task_mode` 请求给后端（后端更新 `task_mode`，下一轮生效）。

#### 20.6.2 视觉设计
```
code 模式：    │> 你的输入…        （左侧竖条 = primary 色）
               [code]              （底部模式文字 = primary 色）
iterate 模式： │> 你的输入…        （左侧竖条 = amber 色）
               [iterate]           （底部模式文字 = amber 色）
```
- **左侧竖向色条**：输入框左边 1 字符宽竖条（`│`），颜色 = 当前模式色（opencode 风格模式指示灯）。
- **底部模式文字**：输入框正下方显示 `[code]` / `[iterate]`，颜色跟随模式。
- **颜色映射**（走主题 token，不硬编码）：`code` → `theme.colors.primary`；`iterate` → `theme.colors.warning`（amber，与 iterate-plugin 暖琥珀主题一致的生态语言）。`minimal` 主题自动退化全白，保持现有降级逻辑。
- **状态来源**：`task_mode` 从后端 status 推送（`types.ts` 的 `BackendEvent.status` 新增字段），前端 `useBackendSession` 读取，纯受控状态，无本地不一致。
- **涉及前端文件**：`frontend/terminal/src/components/PromptInput.tsx`（竖条 + 底部文字）、`App.tsx`（Tab 处理，替换现有 L403-406 逻辑）、`types.ts`（status 字段）、`theme/builtinThemes.ts`（颜色 token，若需新增 iterate 专属色）。

### 20.7 与生态三项目协同

| 项目 | v2.0 角色 | 协同点 |
|---|---|---|
| iterate-harness（本项目） | 执行者：双模式 + 防御式内核 + 多 agent | code 模式自执行防御式编程纪律 |
| iterate-skill（3.0） | 制度与经验生产者 | skill 是**指令形态**的防御式编程行为协议（以 iterate 为骨架、教宿主 AI 防御式干活）；harness code 模式是**自执行形态**的同一套理念，通过共享配置与术语表保证一致性 |
| iterate-plugin（3.0） | 指挥台 | 在 dsh 里同步暴露 task_mode 切换（code/iterate 指示灯）+ 防御事件流（前置失败/回滚/不变量违反） |

### 20.8 里程碑与验收

| 里程碑 | 内容 | 验收 |
|---|---|---|
| M1 | task_mode 后端状态 + 双模式 prompt 注入 | `set_task_mode` 生效且下一轮切换；iterate 模式 1.x 行为零破坏（回归全量测试通过） |
| M2 | TUI Tab 直切 + 竖向色条 + 底部模式文字 | 空输入 Tab 循环切换；色条/文字随模式变色；非空输入 Tab 不冲突；minimal 主题降级正确 |
| M3 | code 模式防御式内核 | 每个工具调用过前置/后置校验；编辑事务缓冲失败自动回滚；不变量违反即中断；假设声明被记录并校验 |
| M4 | code 模式多 agent 编排 | `agent` / `send_message` / `task_stop` 全链路可用；worker 继承防御内核；`<task-notification>` 正确回收并触发收敛 |
| M5 | 外围扩展按需补齐（可选） | image_generation / autopilot / channels 按决策逐项评估 |

**质量门**：
- 后端：全量 pytest 通过（在既有 1600+ 用例基础上新增 task_mode / 防御内核 / 多 agent 用例）；
- 前端：`npm run typecheck` 零错误、`npm run build` 产出正常；
- 回归：iterate 模式全量既有用例零回归（M1 硬约束）；
- 安全：防御内核所有新增校验沿用既有权限层/路径白名单机制，不引入新的敏感信息暴露面。

### 20.9 风险与开放问题
1. **code 模式 token 成本**：通用编程 agent 比 iterate 纯审查更耗 token——沿用既有 `token_budget` / `budget_usd` 熔断机制兜底。
2. **防御内核性能开销**：每步前置/后置校验可能增加延迟——校验默认轻量（语法/关键测试），重量校验（全量测试）仍走周期收敛。
3. **worker 防御纪律继承**：subagent 需显式继承防御内核上下文——通过 `agent_definitions` 注入 worker system prompt 保证。
4. **外围扩展取舍**：4 个缺失扩展是否补齐，取决于 code 模式目标场景（本地通用编程优先 → 不补 channels；需要视觉生成 → 补 image_generation）。
5. **模式切换与运行中任务**：切换只影响下一轮，若运行中任务需要强制切换，需确认是否支持中途打断（复用既有 Esc 暂停机制）。
