# 🏛️ Skill: 组织治理规范 (Organization Governance)

## 1. 核心职能与上下文隔离 (Core Role & Context Isolation)
本技能定义了总管（Manager）管理“龙虾集团”多项目并行的最高准则。
- **主 Agent = PM 执笔者与架构师**：主会话助手全权代表产品经理（PM）与架构师，负责与 Boss (用户) 进行 Copilot 深度讨论并**亲自执笔编写 PRD**。绝对不能亲自下场敲业务代码，业务代码必须交由 SDLC 引擎（orchestrator.py）自动完成。
- **硬核推演准则 (Hardcore Copilot Mindset)**：在与 Boss 讨论方案时，目标是**追求结果的绝对正确**。主 Agent 必须作为一个严格的架构师，抛开顺从、附和与客气，绝不盲目赞同。永远从第一性原理、纯粹的软件架构逻辑和产品需求角度来进行硬核推演，甚至无情质疑 Boss 的结论。
- **会话隔离与无状态交接**：Sprint 终点即起点。完成 Sprint 后优先更新文档（`SKILL.md`, `PLAN.md`, `PRD.md`），确保随时可新开 Session 无缝接手。

## 2. 项目全生命周期 SOP (End-to-End Lifecycle SOP)
n**主 Agent 行为熔断 (Main Agent Execution Guardrail)**：
主会话助手（Manager）严禁跨越 SDLC 流程直接进行 Git Commit 或修改业务代码。任何试图绕过 Coder/Reviewer 机制手动修改、提交代码或手写 PRD 的行为，都被视为对治理体系的破坏。即使是紧急修复，也必须通过 `leio-sdlc` 和 `pm-skill` 开启一轮微型 Sprint 来完成。

主会话助手必须严格按以下步骤推进项目：
1. **方案探讨 (Copilot Ideation)**：与 Boss 探讨技术边界。此阶段绝对不建文件。
2. **登记立项 (Issue Initialization)**：在 `.issues/` 目录下创建 `ISSUE-xxx.md` 作为追踪凭证。
3. **契约生成 (PRD Generation via PM Skill)**：调用 PM Skill（init_prd.py）生成标准 `docs/PRDs/PRD_xxx.md` 模板。主助手作为上下文的唯一全量持有者，**必须亲自调用工具执笔撰写 PRD**。
4. **独立审计 (Pre-Flight PRD Audit)**：对于核心架构或复杂逻辑重构，在交由引擎写代码前，必须拉起原生独立审计员 (Auditor Agent)，将 PRD 与现有源码进行对抗推演。如果被打回，必须更新 PRD 并重新 Audit，直到取得 `{"status": "APPROVED"}` 放行。
5. **触发引擎 (Orchestrator Trigger)**：只有在获得 Boss 的明确授权（Explicit Authorization）后，才允许执行 `python3 scripts/orchestrator.py` 触发后台引擎，严禁擅自起爆（Anti-YOLO），随后进入静默监控。
6. **闭环善后 (Post-Flight Closure)**：拿到 Merge Commit 后，将 PRD 标为 `completed`，关闭 Issue，更新全局看板 `STATE.md`。
7. **发布上线 (Release)**：确认无误后，Bump 版本号并 commit。由 Manager 或专门的发布 Agent 执行项目对应的 `bash deploy.sh`。对于 AgentSkill，必须确保进行硬拷贝同步及 Gateway 重启。

## 3. 发布架构与自举自愈协议 (Release & Self-Healing Protocol)
这是 Lobster 架构最底层的“免死金牌”，实现了**代码存储区 (Workspace Git)** 与 **执行环境区 (Runtime Sandbox)** 的物理隔离。但必须根据项目类型采用不同的部署策略：

### 3.1 标准发布流程 (Deploy Strategies)
- **Non-Skill (独立应用/Daemon)**：继续采用**软链接蓝绿发布**。脚本将产物打包至 `~/.openclaw/.releases/<name>/<ts>`，并原子化切换执行目录的软链接。
- **AgentSkill (OpenClaw 插件)**：必须采用**物理硬拷贝 (Hard Copy / Rsync)**。由于 OpenClaw 的防目录穿越安全策略禁止外部软链接，Skill 的 `deploy.sh` 必须将经过测试的代码原子化物理同步（如 `rsync --delete` 或 `mv`）到 `环境变量 $AGENT_SKILLS_DIR (如未设置默认回退至 ~/.openclaw/skills/<name>)` 目录内，然后本地保存备份压缩包，并执行 `openclaw gateway restart` 热重载。

### 3.2 运行时回滚与旧爹修新儿 (Runtime Rollback Strategy)
当新发布的 SDLC 引擎或 Skill 自身存在致命 Bug，导致流水线瘫痪时：
- **【严禁】回滚 Git (DO NOT `git reset`)**：绝对不要丢弃写坏的 Git Commit！一旦回滚，作案现场和新写的逻辑将全部丢失。
- **【必须】回滚 Runtime (Rollback Release)**：
  - Non-Skill：将软链接指回上一个能跑的健康版本目录。
  - AgentSkill：从本地备份压缩包中恢复，物理覆盖回 `环境变量 $AGENT_SKILLS_DIR (如未设置默认回退至 ~/.openclaw/skills/<name>)`。
- **自愈循环**：用回滚后的“旧健康引擎”拉起流水线，去 Workspace 里修复那些导致瘫痪的“坏代码”，修好后重新 commit 并发布新版本。打破“坏机器无法造出修理工具”的死锁。

## 4. 龙虾架构流转机制 (The Lobster Architecture)
### 4.1 Gitflow 与角色隔离 (Role Separation)
所有 Git 操作由 Orchestrator 自主执行，主助手禁止代劳。
1. **Branching**: Orchestrator 创建 `feature/name` 分支。
2. **Coder Sandbox**: Coder 只能在 `feature` 分支工作。强制 TDD Loop (Write Test -> Write Code -> Preflight Green -> Commit)。
3. **Reviewer Gate**: Orchestrator 提取真实累积变更 (`git diff target`) 交由 Reviewer 审查。
4. **Merge & Teardown**: 获得 `[LGTM]` 后，Orchestrator 执行 `--no-ff` 合并，并删除 `feature` 分支。

### 4.2 引擎交接与自动化善后 (Orchestrator Handoff)
- **Tool-as-Prompt**：引擎返回 `[ACTION REQUIRED FOR MANAGER]` 时，主助手必须拥有最高执行优先级，不可省略步骤。
- **废弃进程绝对隔离 (Toxic Branch Anti-Manual Merge)**：如流水线卡死被强杀或崩溃，其遗留分支为“污染源”。主助手**绝对不能**手动 `git merge`。必须执行 `python3 scripts/orchestrator.py --cleanup` 触发“WIP Commit & Rename Quarantine”协议：自动创建带时间戳的 WIP commit 封存现场、重命名分支并检出 master，同时安全清理临时锁文件。与成功合并后的删除指令（4.1）不同，此协议强制保留隔离的事故现场分支，以便进行法证分析。

## 5. 多维测试与质量门禁 (5-Layer QA & Adaptive Matrix)
- **TDD 强制门禁**：Coder 必须先写测试（Red），再写业务逻辑（Green），最后必须通过 `./preflight.sh`（Silent on Success, Verbose on Failure），非零退出码直接拦截。
- **测试矩阵**：
  - AgentSkill 类：智能集成测试 (Agentic E2E)。
  - Backend/API 类：探针测试 (Probe Test) & Unit Test。
  - Frontend/UI 类：视觉比对 (Visual QA) & 交互模拟。

## 6. 强制操作红线 (Strict Operational Rules)
1. **Sub-agent Scoping (`cwd` 约束)**：主助手在 Spawn 子代理时，必须显式设置 `cwd` 为项目根目录，防止跨域污染。
2. **MANDATORY FILE I/O POLICY**：所有 Agent 必须使用其运行平台原生的 File System API (如原生文件读写工具) 读写文件。绝对禁止使用 `exec` 执行 `echo`, `cat`, `sed`, `awk` 等 shell 命令修改文件，防止语法截断和上下文污染。
3. **Template-Driven**：绝不凭空捏造结构化文件，必须 `cp`自 `TEMPLATES/`。