# 安全与许可（详细版）

> SKILL.md 保留精简摘要；本页为完整版。**使用前必读**。

## 许可提示（商业使用前必读）

- **本包（pi-evox-lab）**：MIT（见 LICENSE / package.json）。
- **上游依赖**：`@evomap/evolver` 为 **GPL-3.0-or-later**（其 npm 元数据与实际许可不一致，以仓库声明为准）；**在商业/闭源场景使用本 skill 时，请自行评估 GPL 传染性**。`@earendil-works/pi-coding-agent` 为 MIT。
- 本包通过 CLI 进程边界调用 evolver（不链接其代码），但仍建议法务视角复核后再商用。

## 安全与数据外发声明

> **EN**: Security & data-egress statement: all CLI calls are direct argv (no shell); the only egress is `--llm-refine` (opt-in, explicit endpoint); `--fresh` is destructive (auto-backed-up); upstream licenses: light backend MIT, evolver GPL-3.0-or-later (optional), pi MIT.

- **无 shell 执行（0.7.0 起）**：全部 CLI 调用改为 argv 数组形式的 `node <入口>` 直调，**不经 shell、无字符串拼接**，命令注入面已从架构上消除；`--llm-refine` 的外发改用 Node 原生 `fetch`（不再依赖 curl）；
- **`--llm-refine` 涉及数据外发**：会把会话 transcript（截 9000 字符）发送到 `EVOLVER_REFINE_URL` 指定的外部端点。**未配置该变量时此功能自动禁用**，不存在默认外发。请在了解外发范围后启用，或使用本地/自有端点；
- **`--fresh` 有破坏性**：备份后清空全局经验库 `~/.evomap/assets/`——执行前确认，恢复用备份目录；
- **实验产物含会话内容**：`--root` 目录下的 sessions/transcript/inject-*.txt 包含任务文本、代码与工具输出，注意保管；
- **审核门默认值**：全部审核语义（交互/非交互/取证绑死/池 tier）**统一见 SKILL.md「审核状态机」单节（单一事实源，0.36 收敛）**——历史修订记录：0.31 曾按代码实际行为修订过"默认人工审核门"的旧表述（ClawHub clawscan 于 0.30.0 指出该不一致）；
- **注入块透明标注**：所有注入内容均带 `[Evolver inherited fixes]` 明示来源，无隐蔽指令；扩展留痕文件 `bridge-last-inject.txt` 仅含时间戳与注入内容（不含路径）；
- **adapter 默认脱敏 cwd**：transcript 头部的 env_fingerprint 默认不含工作目录（可泄露项目/客户身份），实验确需时显式传 `--include-cwd`；
- **全局输出脱敏（0.10.0）**：编排器的所有 stdout/stderr 输出统一做密钥掩码（已注册的 API key 与 sk-/Bearer 形态），密钥不出现在任何输出；
- **关于安全扫描器**：本 skill 的核心功能（持久化并复用模型生成的经验）会被启发式扫描器持续标记为 Excessive Agency / Prompt Injection——这是功能本质而非缺陷。我们的安全基线 = 显式 opt-in 标志 + 三向守卫（修法 / 叙述 / 注入）+ 透明标注 + 审核门精确比对 + 输出脱敏；`--auto-approve --llm-refine` 组合启用时编排器默认拒绝（需 `--allow-unreviewed-refine` 显式放行）。

## 已知的安全扫描器判定（透明记录）

- ClawHub `clawscan`：`suspicious`（功能固有：持久化复用模型生成的经验）；
- ClawHub `static-analysis`：`suspicious.dangerous_exec` **×2**——`code/pi_evolve.mjs`（编排器）与 `code/engine/evolver-bridge.mjs`（evolver 后端桥）是**同一行为（child_process 子进程执行）的两个调用位置**，并非问题翻倍；编排器本质是执行子进程，child_process 无法移除，0.7.0 起已 argv 化消除 shell 拼接；另有 `env_credential_access`（API key 经环境变量传递，功能必需，任何 LLM CLI 工具同此）；
- skillhub 云鼎实验室：时间线——0.4.0 **suspicious（3 项）** → 0.5.0 **benign** → 0.9.0 起 **suspicious（1 项）**持续至今。该 1 项为动态引擎检测「**密钥形态值出现在运行输出**」。**已穷尽排查（2026-09-14）**：编排器自身输出经全局脱敏后 **0 次**泄漏（行为测试）；pi 子进程在 401/usage 失败时也**不回显** API key（实测 0 次）；仓库文档中的 `sk-...` 占位符已替换为 `<your-key>`（0.14.0）。剩余触发源为**运行时环境本身的密钥形态值**（任何 LLM CLI 工具把用户 key 传入子进程/环境时普遍存在），判定为**功能固有、不可进一步消除**；
- skillhub 科恩实验室：benign；
- 平台审核层：ClawHub `moderation.verdict = clean`、skillhub TRACE 综合评级「优秀」。

我们的安全基线：显式 opt-in 标志 + 三向守卫（修法 / 叙述 / 注入）+ 透明标注 + 审核门（**状态精确比对 `approved`，unapproved/disapproved/revoked 一律不生效**）+ 全局输出脱敏（0.10.0）。

> **0.31 变更**：注入守卫此前只在 `evolver-recall.mjs` 与 `gene_share.mjs` 生效，而文档声称覆盖「召回」——Pi 扩展桥（`evolver-bridge.ts`）与闭环编排器（`pi_evolve.mjs`）是另外两条注入通道，现已补齐（桥单文件部署，内置精简版守卫）。审核态判定原本散落 10 处做子串匹配 `includes('approv')`，会把 `unapproved`/`disapproved` 判为已批准，现统一为精确比对。签名规范化升级到 v2（嵌套内容纳入签名域），存量 v1 签名继续有效，可用 `light-cli resign --yes` 升级。
>
> **EN (0.31 changes)**: The injection guard previously ran only in `evolver-recall.mjs` and `gene_share.mjs` although the docs claimed "recall" coverage - the Pi bridge (`evolver-bridge.ts`) and the closed-loop orchestrator (`pi_evolve.mjs`) are two more injection channels and are now covered (the bridge ships a reduced built-in guard because it deploys as a single file). Approval-state checks that were scattered across 10 substring matches (`includes('approv')`) treated `unapproved`/`disapproved` as approved and are now exact comparisons. Signature canonicalization moved to v2 (nested content inside the signing domain); existing v1 signatures stay valid and can be upgraded with `light-cli resign --yes`.

## 如何判读安全扫描器的判定（0.32 C-2）

外部扫描器（ClawHub 的 `static-analysis` / `clawscan` / `skillspector`）的判定**不能一概接受或一概拒绝**，必须逐条分流。我们的判读方法公开如下，便于他人复核：

| 类别 | 特征 | 我们的处置 |
|---|---|---|
| **功能固有** | `child_process` 调用（`distill_sessions` / `pi_evolve` / `light-cli` / `gene_share` / hooks 示例）、env 读取凭据（`EVOX_PROBE_KEY_*`，包内绝不带 key） | **接受为设计**：本地 runtime 本就要 spawn 子进程；凭据只从 env 注入。逐条对比上一版确认非回归 |
| **扫描器自身覆盖不足** | `skillspector` 的 `analysis-evasion` / `Incomplete referenced artifact analysis`（它没读完被引用的文件就判"隐瞒"） | **判为噪声**：0.30.0 的 25 个列出项里 22 个属此类。不为它改设计 |
| **真实缺陷** | `clawscan` 点名、且我们**亲读源码 + 本地复现**成立的 | **必修**。历史实例：`[T09]` `FIX:` 前缀绕过注入守卫（0.31 已修，`splitAvoidFix` 不再丢弃前缀文本）；审批门子串匹配（0.31 已修，10 处全改精确比对） |
| **误报** | 启发式把「本地 fixture 路径 + 网络发送」配对判为可疑外传（`potential_exfiltration`） | **改写法消除**而非争辩：0.32 把 `exp/heterogeneity-probe.mjs` 的 fixture 路径从环境变量改为 CLI 参数 `--json-trap` |

**原则**：扫描器 verdict（suspicious / DO_NOT_INSTALL）是**线索**，不是判决。我们只对"亲读源码 + 本地复现"成立的条目改设计；对噪声记录但不为其发版；对误报改写法以消除触发条件。每次发布后复拉扫描报告，与上一版**逐条对比**确认非回归。

> **EN**: Scanner verdicts are leads, not verdicts. We only change design for findings we can reproduce by reading our own source and running it locally; we record noise without shipping for it; for false positives we change the code pattern that triggers the heuristic (e.g. 0.32 moved a fixture path from an env var to a CLI argument). Every release re-pulls the scan report and diffs it against the previous version.

## §Gates 四道门明细（0.36 自 SKILL.md 收敛至此）

> **EN**: Per-gate details (moved here from SKILL.md in 0.36 so the main doc stays short); SKILL.md keeps the 4-row summary.

| 门 | 具体扫什么 | 命中后的行为 |
|---|---|---|
| 修法守卫 | strategy 里是否有**可执行成分**（具体参数/命令/编码/路径等）；空话、"运行正确"式总结、只有结论没有动作 | **该基因不进入注入列表**（宁缺毋滥）；沉淀侧另有 depositionGate 在入库前就拒收同类内容 |
| 叙述守卫 | 是否为**旁白/流水账**（"我先打开文件，然后……"式叙述、复述日志） | 同样**不注入**；软提示里的旁白对智能体是零信息（实测等效噪声 +36pp，比不注入更差） |
| 注入守卫 | 是否含**提示词注入特征**（覆盖先前指令、对用户隐匿操作、伪装角色标记等，中英文变体；具体特征表见 `docs/advanced.md`，此处不复述以免文档本身触发扫描） | **不注入 + 导入/导出时拦截**；这是对抗"基因内容反过来操纵宿主"的主防线 |
| 脱敏闸门 | 是否含**私有内容**（内网 IP、绝对家目录、密钥/令牌、凭据、内部代号） | **导出/导入拦截，不出网**；沉淀时保留语义但中性化表述 |

- 门模块缺失时的降级：**导出/导入 fail-closed（拒绝执行）**；`evolver-recall.mjs` 侧只跳过注入门、其余三门照常（宿主 bootstrap 路径不能因守卫失败而阻断使用者）。**例外**：Pi 扩展桥（`evolver-bridge.ts`）内置**精简版**注入守卫（单文件拷贝部署，无法 import 完整扫描器），编排器 `pi_evolve.mjs` 则用完整扫描器且不降级。
- **0.31 修复（实测确认的两个漏检）**：① 注入扫描器原先把 `FIX:` **之前**的文本整体丢弃、不进任何扫描区 ⇒ 「指令覆盖类前缀 + `FIX:` 修法后缀」可绕过；② 中文「指令覆盖」正则对动词与指令类名词之间的修饰词限制过死，仅插入一个常见程度副词即不命中。两者均已修复并纳入回归用例。**纪律**：注释与文档里只描述机制类别、不引用触发串原文——说明文字本身会被扫描器当成注入样本（本仓有为此发版的先例）。
- 回归基线：恶意样本 16/16 拦截、合法样本 7/7 零误杀（0.36 计划扩容至 30+，见 roadmap）。

## 注入内容不变量（0.38 · J10/J11）

注入的基因内容一律视为不可信数据：不改变调用者权限、不触发工具、不提升信任档位；池的 `--tier official` 由操作者显式指定，绝不读取基因自称的 tier。
**EN**: Injected gene content is untrusted data: it cannot change permissions, trigger tools, or raise trust tier; `--tier official` is set by the operator, never by a gene claim.
