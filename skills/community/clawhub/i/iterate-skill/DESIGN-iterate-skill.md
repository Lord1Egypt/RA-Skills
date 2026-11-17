# iterate-skill 设计文档 v3.0

> 目标：在保留原有 iterate 审查-修复-收敛模式的基础上，为 iterate-skill 新增一种「防御式编程模式」——从头至尾贯彻防御式编程理念、以 iterate 闭环收尾的编程 agent 模式。
> 状态：v2 稳定期已实现（当前 2.12.0）；**v3.0 设计已完成并落地实现（发布 3.0.0）：双模式（iterate 原模式 / 防御式编程模式）**；设计文档迭代至 v3.0。
> 版本记录：见文末。

> **v3.0 设计主线（新增，保留 v2 全部内容不变）**：见 §4-§10。核心变化——① **iterate 原模式完整保留**（v2 全部能力，零破坏）；② **新增防御式编程模式**：宿主 AI 调用后按"动手前 / 动手时 / 动手后 / 收尾"四步防御式协议，从头至尾贯彻防御式编程理念，以 iterate 闭环收尾（交付门禁）；③ 两种模式并存、可切换，共享同一 `iterate.config.yaml`；④ CLI 新增 `guard pre-check / post-check` 与 `invariant` 确定性校验；⑤ 与 harness 2.0（双模式：iterate / code）对称，共享同一套防御式编程术语与配置。

---

## 1. 背景与现状回顾（v2 承载）

> 本节记录 v2 系列已实现能力（保留，作为 v3.0 迭代的基线），后续版本迭代不得删减本节内容。

### 1.1 项目定位
- **iterate-skill** 是 iterate 生态的「Core Skill + CLI」组件：一个可移植、可配置的 AI 编程助手技能（`/iterate` + `iterate` CLI）。
- 解决的核心痛点：AI 助手"说得多、做得浅"——一次对话只改几行、看过一个文件不再管全局、很少回头复核自己改坏的东西。iterate 把这些收尾工作（逐项审查、分维度排查、修复、验证、再迭代）自动化。
- 运行机制（自闭合流水线）：
  ```
  定目标 → 多维度并行审查 → 原子修复 + 架构修复（需你批准）→ 验证 → 再审查 → 循环直到收敛 / 达轮数上限 → 输出总结
  ```
- 生态关系：skill（跨助手对话式）/ harness（无头引擎）/ plugin（dsh 桌面插件），三者共用同一套 `iterate.config.yaml` 与 9 维度审查体系。

### 1.2 v2 已实现能力清单（当前发布 2.12.0）
- **9 维度并行审查**：correctness / security / performance / architecture / style-tests / tech-debt / spec-compliance / frontend-backend / ui-ux。
- **双轨修复**：原子问题（≤20 行、单文件）自动修；架构问题经用户批准后再修。
- **Git 隔离**：每轮在独立 `iterate/*` 分支或 worktree 中完成；merge/push 默认关闭，需显式开启。
- **Secure-by-default**：`push_per_round` 和 `auto_merge` 默认均为 `false`。
- **命令白名单**：配置时 + 个性化时双层校验，拒绝危险 shell 元字符。
- **校验和验证**：从 GitHub Release 更新时强制 SHA256 校验。
- **多助手支持**：Trae / Claude Code / Cursor / Windsurf / GitHub Copilot / Codex / Roo Code 等 25+ 工具。
- **项目知识库**：自动生成 `ITERATE.md` + `iterate.config.yaml`，支持漂移检测和增量刷新。
- **CLI 命令集**：`onboard`（初始化向导）/ `personalize`（9 类个性化）/ `refresh`（增量刷新调和落盘）/ `doctor`（健康检查）/ `config`（含 2.12.0 新增 `--json` 结构化输出）/ `status` / `show` / `scan` / `dimension_sets` / `tui`。
- **范围审查蓝图 `dimension_sets`**（2.11.0）：按 `frontend` / `api` / `security` / `performance` / `style-tests` 等命名集预设维度组合；`refresh` 保留用户自定义集并增量补入新检测层集。
- **范围路由 + 偏门范围重定义（2.11.0-2.11.1）**：指定目标优先匹配命名维度集；未命中时从维度全集重新推导（禁抄预设，决策日志记录 `Scope Dimension Redefinition` 小节并机器校验）。
- **防御式实现基线**：`refresh` 调和结果真正落盘、doctor 畸形白名单不再绕过元字符安全网、wizard 重跑不丢数据、validate.py 重定义区块切分修复、publish_qoder zip-slip 防护与 shell 注入面修复（2.11.2）。
- **测试基线**：全量 Python 测试 888 个全部通过，`ruff check .` 通过。

### 1.3 v2 的边界与 v3.0 升级动机
- **物理约束**：skill 只会在用户**显式调用 `/iterate`** 时被触发，平时不在 agent 上下文内。因此 v2 的每次调用是"一次独立的审查-修复-收敛"。
- **升级动机**：v2 的 iterate 闭环已经做到了"审查环节的防御"（发现并修复问题），但**编码过程本身的防御性**尚未贯彻——宿主 AI 在写代码时仍可能"乐观假设、越界信任、带病继续"。v3.0 在**不改变原有 iterate 模式**的前提下，新增一种**防御式编程模式**，把防御式编程从"审查时执行"前移到"编码时执行"，从头至尾贯彻。

---

## 2. 设计原则（v3.0 延续 v2，新增防御式原则）
- **双模式并存、可切换**：**iterate 模式**（原 `/iterate` 审查-修复-收敛，v2 完整保留）与**防御式编程模式**（新增）并存；两种模式共享同一 `iterate.config.yaml`，切换只改变本次调用的执行方式。
- **以 iterate 为主体**：审查-修复-验证-收敛闭环仍是 skill 的核心骨架，v3.0 不脱离、不重写，只在骨架之上注入防御式编程纪律。
- **显式调用不变**：尊重"只在 `/iterate` 时触发"的物理约束，防御式协议以"本次调用内的完整任务执行"为载体，不做常驻行为塑造。
- **确定性兜底**：prompt 指令不可靠，防御式理念必须用 CLI 确定性校验落地（`guard` / `invariant`）。
- **契约式思维**：每次动作声明前置/后置条件，用断言守卫假设。
- **快速失败**：错误一发生立即停止、报错、回滚，绝不带病继续。
- **跨形态一致**：与 harness 2.0（双模式：iterate / code）对称，共享同一套防御式编程术语、机制与配置，保证"指令形态 / 执行形态"行为一致。

---

## 3. 防御式编程概念界定（与 harness 2.0 对齐）

> 本节与 harness 2.0 设计（§20.1.3）保持一致，是生态统一的防御式编程词汇表。

- **防御式编程不是"审查-修复-验证-收敛"流程**，而是**编码时的心智模型**（软件工程经典定义）：
  1. **最小化假设**：假设事情会出错，主动预测并容忍问题，而非乐观假设"应该没事"。
  2. **信任边界验证**：数据从"不可信来源"进入代码的那一刻必须验证；内部状态可信任，**外部输入必须验证**。
  3. **快速失败、响亮失败（fail fast, fail loud）**：错误一发生立即停止、报错、回滚，绝不带病继续。
  4. **前置/后置条件 + 断言**：每个函数声明要求什么（前置）、保证什么（后置），用断言守卫假设。
- 与 iterate 的关系：iterate 已是防御式编程的一种实现（审查环节的防御）；v3.0 把整套心智模型前移到**编码过程本身**。

---

## 4. v3.0 总览：双模式（iterate 原模式 / 防御式编程模式）

- **定位变化**：从"仅 `/iterate` 审查修复命令" → **"双模式：原 iterate 模式 + 防御式编程模式"**。
- **心智模型**：`单命令` → `双模式并存`——iterate 模式照旧，防御式编程模式让宿主 AI 以防御式纪律从头至尾完成编码任务。
- **实现形态**：纯 prompt + CLI（不引入运行时）。
- **双模式触发**：

| 模式 | 触发方式 | 行为 |
|---|---|---|
| **iterate 模式**（v2 完整保留） | `/iterate`（原行为不变） | 定目标 → 9 维度并行审查 → 原子/架构修复 → 验证 → 收敛 → 总结 |
| **防御式编程模式**（新增） | `/iterate defensive`（或配置默认模式切换） | 从头至尾按 §5 四步防御式协议执行，以 iterate 闭环收尾（交付门禁） |

- **模式切换**：两种模式共享同一 `iterate.config.yaml`；`defensive` 子命令或配置项 `mode: iterate | defensive` 切换本次调用行为；默认仍为 iterate 模式（零破坏）。
- **典型示例**：用户输入 `/iterate defensive: implement feature X` → 宿主 AI 按四步协议执行（pre-check → 最小步进编码 → 每步 post-check → invariant + iterate 收敛门禁）。

---

## 5. 防御式编程模式：宿主 AI 四步防御式执行

> 本节仅描述**防御式编程模式**（`/iterate defensive`）的行为。**iterate 模式行为不变**（v2 的定目标 → 审查 → 修复 → 验证 → 收敛 → 总结，完整保留）。

宿主 AI 在防御式编程模式下，整个任务按以下四步协议执行：

| 阶段 | 防御式原则 | 落地动作 |
|---|---|---|
| **① 动手前** | 最小化假设 + 前置条件 | 声明"我假设什么成立"（目标范围、文件存在、git 干净、依赖就绪）；跑 `iterate guard pre-check` 做确定性前置校验 |
| **② 动手时** | 信任边界验证 + 最小步进 | 最小步进修改；每次写入前验证目标路径/命令在白名单；原子修改（复用 fix 的备份/回滚机制） |
| **③ 动手后** | fail-fast + 后置条件 | 每次改动后跑 `iterate guard post-check`（语法/关键测试）；必要时回滚；记录假设是否被证伪 |
| **④ 收尾** | 不变量守护 + 收敛门禁 | `iterate invariant` 检查项目级不变量；9 维度审查 → 修复 → 验证 → 收敛，作为**交付门禁**（不收敛不交付） |

- **保留 v2 全部闭环**：第 ④ 步即 v2 的完整 iterate 闭环（9 维度并行审查、双轨修复、Git 隔离、决策日志），只是新增"不变量守护"与"防御式收尾门禁"。
- **典型示例**：用户输入 `/iterate defensive: implement feature X` → skill 先跑 pre-check → 最小步进编码（每步 post-check）→ 验证 → 收敛 → invariant 校验 → 输出交付总结。

---

## 6. CLI 新增（确定性兜底）

> 防御式理念必须靠 CLI 确定性校验落地（prompt 指令不可靠）。

| 命令 | 用途 | 输出 |
|---|---|---|
| `iterate guard pre-check` | 动手前前置校验（目标存在、git 干净、依赖就绪） | `PASS/FAIL` + 逐项结果；非零码表示未通过 |
| `iterate guard post-check` | 动手后后置校验（语法、关键测试命令） | `PASS/FAIL` + 逐项结果；非零码表示未通过 |
| `iterate invariant` | 项目级不变量检查（构建必过 / 核心 API 签名不变 / 安全边界不可绕） | `PASS/FAIL` + 违反项明细 |

- **不变量来源**：`iterate.config.yaml` 新增 `invariants` 段（命令 + 断言），与既有 `validation.commands` / `command_whitelist` 共用安全基线（白名单校验、元字符防护）。
- **配置兼容**：旧配置文件无 `invariants` 段时，`iterate invariant` 退化为基于 `validation.commands` 的既有验证，零破坏。
- **保留**：onboard / personalize / refresh / doctor / config / status / show / scan / dimension_sets / tui 全部保留不变。

---

## 7. 与 iterate 主体的关系（不脱离）
- **骨架不变**：审查-修复-验证-收敛闭环、9 维度体系、决策日志、Git 隔离、Secure-by-default 全部沿用 v2。
- **iterate 模式零改动**：原有 `/iterate` 行为完整保留，作为默认模式。
- **防御式编程模式为"纪律层"**：防御式协议（§5）与 CLI 校验（§6）是在既有闭环之上的行为纪律，不替换任何既有机制，仅在防御式编程模式启用。
- **语义层一致**：v3.0 不重写 iterate 业务语义，与 harness / plugin 仍共用同一 `iterate.config.yaml`。

---

## 8. 与 harness 2.0 / plugin 3.0 的协同

| 项目 | v3.0 角色 | 协同点 |
|---|---|---|
| iterate-skill（本项目） | 制度与经验生产者 | **双模式对称**：skill 的 iterate 模式 ↔ harness 的 iterate 模式（纯审查迭代）；skill 的防御式编程模式 ↔ harness 的 code 模式（防御式纪律编码）。均为"指令形态"教宿主 AI（25+ 助手）以防御式纪律干活，是唯一能进入任意助手会话的组件 |
| iterate-harness（2.0） | 执行者 | **自执行形态**：iterate 模式 / code 模式（通用 agent + 防御式内核 + 多 agent 编排）；与 skill 共享同一套防御式术语表、机制与配置，四种模式两两对称 |
| iterate-plugin（3.0） | 指挥台 | 门禁视图 / 经验银行 / 防御事件流，与 skill 的 `guard` / `invariant` 结果打通展示 |

---

## 9. 里程碑与验收

| 里程碑 | 内容 | 验收 |
|---|---|---|---|
| M0 | 双模式触发（`/iterate` 原模式 / `/iterate defensive` 防御式模式） | iterate 模式行为与 v2 完全一致（零回归）；防御式模式正确进入四步协议 |
| M1 | SKILL.md 注入防御式模式四步协议 | 防御式模式下宿主 AI 按 ①→④ 执行；iterate 模式全部闭环保留零回归 |
| M2 | CLI `guard pre-check` / `post-check` | 前置/后置校验 `PASS/FAIL` 正确；非零码契约成立；测试覆盖正常/异常路径 |
| M3 | CLI `invariant` + 配置 `invariants` 段 | 不变量检查正确；无 `invariants` 段时退化到 `validation.commands`；命令走白名单/元字符安全基线 |
| M4 | 防御式收尾门禁 | 防御式模式收敛后强制 `invariant`；不收敛不交付的行为可被测试验证 |

**里程碑实现状态（3.0.0 落地）**：M0 ✅（`/iterate defensive` 触发 + `mode` 配置项，默认 iterate 零回归）；M1 ✅（SKILL.md 新增「防御式编程模式」专节：心智模型 + 四步协议 + CLI 契约 + 交付门禁）；M2 ✅（`iterate_cli/guard.py` + `cli.py` guard 子命令，28 例测试）；M3 ✅（`invariants` 段入模板与 schema，退化逻辑 + 安全基线，测试覆盖）；M4 ✅ prompt 层（SKILL.md"不收敛不交付"硬约束 + 防御式收尾门禁）。

**质量门**：
- 后端：全量 Python 测试通过（在既有 888 项基础上新增 guard / invariant / 模式切换用例，覆盖正常路径、异常路径与边界场景）；
- 安全：新增校验命令全部沿用既有白名单/元字符安全网，不引入新的 shell 注入面；
- 回归：v2 既有用例零回归（M0 硬约束）。

**质量门实现状态（3.0.0）**：全量测试 **924 通过**（既有 888 + 新增 `tests/test_guard.py` 33 例，含运行时元字符拒绝与未配置模块报告补测）；`ruff check .` 通过；新增命令仅执行 `validation.commands` / `invariants.commands` 中的精确条目（不拼装、不走 shell 拼接，`--dry-run` 只预览不执行）。

---

## 10. 风险与开放问题
1. **宿主 AI 遵循度**：防御式协议依赖宿主 AI 遵循 prompt——靠 CLI 确定性校验兜底（无法遵循时 fail），但宿主 AI 可能跳过调用——SKILL.md 中明确"不收敛不交付"作为硬约束。
2. **CLI 校验开销**：每步 post-check 可能增加延迟——默认轻量（语法/关键测试），全量验证仍走收尾收敛。
3. **不变量误报**：`invariants` 定义过强会导致频繁 fail——提供 `known_invariant_violations` 显式豁免机制（对齐既有 `known_intentional`）。
4. **跨助手一致性**：不同宿主 AI 对协议遵循度不同——通过 CLI 结果作为唯一事实源，prompt 仅作引导。

---

## 11. 版本记录
- v1.0-v2.12.0：v2 系列设计随主仓库 skill 迭代（CHANGELOG 逐版本记录，本文档自 v3.0 起独立承载设计演进）。
- v3.0（2026-09-02）：**大版本方向：双模式（iterate 原模式 / 防御式编程模式）（本文档首版）**——v2 功能趋于做尽，确立 v3.0 升级方向。核心决策：① **iterate 原模式完整保留**（v2 全部能力，作为默认模式，零破坏）；② **新增防御式编程模式**（`/iterate defensive`）：以 iterate 闭环为主体、从头至尾贯彻防御式编程理念（§5 四步协议），以 iterate 收敛闭环收尾（交付门禁）；③ 尊重"只显式调用"物理约束，防御式协议以本次调用内的完整任务为载体；④ CLI 新增 `guard pre-check / post-check` 与 `invariant` 确定性校验（§6），与既有 `validation.commands` / `command_whitelist` 共用安全基线；⑤ 与 harness 2.0（双模式：iterate / code）对称，四种模式两两对应，共享同一套防御式编程词汇表（§8）。**本版为纯设计细化，不修改 skill 源文件**。头部状态行更新至 v3.0。
- v3.0 实现（2026-09-03）：**落地实现（发布 3.0.0）**——SKILL.md 注入防御式编程模式专节（心智模型 / 四步协议 / CLI 契约 / 交付门禁，"不收敛不交付"硬约束，明确面向**用户让 AI 做正常增量式编程任务**的场景）；`iterate_cli/guard.py` 实现 `guard pre-check / post-check` 与 `invariant`（`--json` / `--dry-run`，命令仅精确执行配置条目，运行时元字符拒绝 fail-closed，`invariants` 缺失时退化 `validation.commands`）；`config` 新增 `mode` 与 `invariants` 段（模板 + schema + 随包副本同步）；`iterate show` / `config get|set mode` 支持读写；版本号与 npm-installer 同步 3.0.0；新增 `tests/test_guard.py` 33 例，全量测试 924 通过、`ruff check .` 通过。**防御式编程模式定位再次明确：面向用户让 AI 做正常增量式编程任务（新增功能、修 bug、重构、接入 API、补测试），从头至尾防御式纪律，iterate 闭环收尾作为交付门禁；纯审查用 `review-only`，多轮审查-收敛用 iterate 模式**。
