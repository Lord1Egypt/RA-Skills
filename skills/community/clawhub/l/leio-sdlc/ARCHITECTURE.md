# 🦞 leio-sdlc v0.2 架构白皮书 (Architecture Blueprint)

## 1. 核心设计哲学 (Core Philosophy)
v0.2 版本标志着 `leio-sdlc` 从“单步手动触发脚本”正式跃升为**“全自动、状态机驱动、具备自愈能力的智能体流水线 (Agentic Microservice Engine)”**。
- **解耦 (Decoupling)**：剥离 PM 职责（冷热分离、防上下文污染）。引擎的唯一合法输入是硬盘上已存在的 `PRD.md`，不再处理模糊的聊天上下文。将 PM 的需求梳理过程（热对话）与 SDLC 的严格执行过程（冷指令）物理隔离，防止前端闲聊污染开发链路的上下文。
- **目录即沙盘、文件即队列 (Workspace-as-a-Job-Queue)**：不使用内存或数据库保存状态。每个 PRD 拥有专属的执行沙盘（如 `.sdlc/jobs/Feature_X/`）。该沙盘内各 Markdown PR 合约文件的状态 (`status: open | blocked | closed`) 构成了当前需求的局部消息队列。这天然隔离了不同业务模块的并发冲突。
- **物理熔断与降维打击 (Circuit Breaker & Adaptive Re-slicing)**：当大模型智商触顶陷入死循环时，系统绝不无限重试，而是物理销毁现场，并要求上游重新“切碎”任务。

---

## 2. 全生命周期状态机 (The Lifecycle State Machine)

### 2.0 任务初始化与防并发污染 (Job Isolation)
为了支持多需求并行开发，禁止将 PR 散落在全局的 `docs/PRs/` 目录。
- **触发**：执行 `./run.sh --prd docs/PRDs/Feature_X.md`。
- **Job 隔离**：引擎在项目根目录自动创建该 PRD 的专属队列空间 `.sdlc/jobs/Feature_X/`。
- **拆分下发**：Planner 将生成的 PR 合约按顺序放入该专属目录，如 `.sdlc/jobs/Feature_X/01_DB.md`。

### 🟢 Green Path (顺风局 / 理想流)
1. **Queue Polling**: 引擎仅扫描当前专属目录 `.sdlc/jobs/Feature_X/` 下处于 `status: open` 的工单。
2. **Branching**: 引擎签出新分支 `git checkout -b feature/PR_001_DB`。
3. **Coding**: 引擎拉起 Coder，Coder 读取 PR 合约并修改代码，提交 Commit。
4. **Reviewing**: 引擎生成 Diff，拉起 Reviewer。Reviewer 痛快地输出 `[LGTM]`。
5. **Merging**: 引擎将代码 Merge 进 master，删除 feature 分支。
6. **Closing**: 引擎将 `PR_001_DB.md` 的状态修改为 `status: closed`。引擎轮询下一个 open 的 PR。

### 🟨 Yellow Path (纠错流 / 局部自愈)
*触发条件：Coder 写出了 Bug 或未满足验收标准。*
1. **Review Rejection**: Reviewer 审查 Diff 后，输出 `[ACTION_REQUIRED]` 并附带修改意见。
2. **Correction Loop**: 引擎**不合并代码**，而是将修改意见追加到上下文，**第二次拉起 Coder** 继续在当前 feature 分支上修改。
3. **Threshold**: 这个循环最多允许发生 **MAX_REVISIONS (默认 5 次)**。如果在 MAX_REVISIONS (默认 5 次)内 Reviewer 给出了 `[LGTM]`，则回归 Green Path。

### 🟥 Red Path (死亡循环 / 熔断与降维重构)
*触发条件：Yellow Path 连续失败 MAX_REVISIONS (默认 5 次)，或者 Coder 执行超时 (Timeout/Token Cap 触顶)。*
1. **Hard Abort (物理斩首)**: 引擎判定当前分支已被“剧毒污染 (Toxic Branch)”。立刻执行强杀。
2. **Tabula Rasa (恢复出厂设置)**: 执行 `git reset --hard` 和 `git clean -fd`，强制切换回 master，并**彻底删除**那个被污染的 feature 分支 (`git branch -D`)。
3. **Status Update**: 将该 PR 的状态改为 `status: blocked`。
4. **Adaptive Re-slicing (动态切片)**: 
   - 引擎拿着失败日志，**定向拉起 Planner**。
   - 下达指令：“`PR_001_DB.md` 任务过于复杂导致 Coder 崩溃。请将该任务拆解为 2-3 个更小的、职责更单一的 Micro-PRs。”
   - Planner 生成 `PR_001a.md` 和 `PR_001b.md` (`status: open`)。
5. **Queue Resumes**: 引擎重新扫描队列，发现新的、更简单的 open PR，流水线继续运转。

---

## 3. 测试覆盖矩阵 (Testing Matrix for v0.2)
为了保证这套精密仪器的绝对可靠，v0.2 将构建以下 3 层沙盒测试：

1. **`test_e2e_green_path.sh` (已完成雏形 ISSUE-024)**
   - **目的**: 测试无障碍连播能力。
   - **验证**: 提供包含 2 个简单 PR 的环境，验证引擎能否自动轮询，依次拉起 Coder 和 Reviewer，最终完成 2 次 Merge。

2. **`test_e2e_yellow_path.sh` (即将开展 ISSUE-025)**
   - **目的**: 测试打回重做机制 (Review-Correction Loop)。
   - **验证**: 故意在沙盒注入一个挑剔的“假 Reviewer (Mock)”，强制前两次输出 `[ACTION_REQUIRED]`，第三次才输出 `[LGTM]`。断言引擎是否成功发起了 MAX_REVISIONS (默认 5 次)循环而不崩溃。

3. **`test_e2e_red_path.sh` (终极抗压测试)**
   - **目的**: 测试熔断与动态切片能力。
   - **验证**: 注入“死锁 Coder”或“永远拒绝的 Reviewer”，强制触发 MAX_REVISIONS (默认 5 次)阈值。断言引擎是否执行了 `git branch -D` 清理现场，并成功拉起 Planner 生成了新的分裂 PR。