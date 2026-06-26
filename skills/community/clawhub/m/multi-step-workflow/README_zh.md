# 多步骤工作流 (高信任版 SOP)

轻量级任务追踪，具备 **“机器门控规划” (Machine-Gated Planning)**、**“自主执行” (Autonomous Execution)** 和 **“用户授权式复盘” (User-Opt-In Review)**。

## 开发与合规声明 (ClawHub Audit v4.4.0)

> [!IMPORTANT]
> **审计加固级私有存储 (Owner-Only Access)**
> 为了彻底消除在多用户系统共享 `/tmp` 时可能存在的隐私风险，本版本实现了 **严格的 POSIX 权限锁死**：
> - **私有目录 (0700)**：系统临时目录下的项目专用子文件夹 (`/tmp/openclaw-workflow-*`) 仅限当前用户读写执行。其他用户由于无权 cd 进该目录，无法窥视您的任务状态。
> - **私有文件 (0600)**：所有 JSON 状态文件在生成的同时被锁定为 `0600` 权限（仅 Owner 读写）。
>
> **快照功能可选化 (Default: OFF)**
> 为满足高等级的隐私合规要求，**上下文快照 (Context Snapshot)** 功能现已变为可选。
> - **默认 useSnapshots**: `false`
> - **高忠实度快照**：开启后，快照将原汁原味地记录中间态发现。请仅在您信任本地存储环境时通过配置启用。

### 💾 私有临时存储 (沙箱隔离)
- `approvals.json` (0600)：记录您的审批标记。
- `context-snapshot.json` (0600)：原生忠实度提取物。
- `tasks/*.json` (0600)：任务细化步骤。

## 自适应工作流逻辑

1. **快速路径 (< 3 步)**：针对简单的单项任务。直接执行。
2. **标准路径 (>= 3 步)**：
   - **第一步：规划模式**：Agent 拟定计划。**必须停止以等待您的批准**。
   - **第二步：门控跳转**：一旦您说“OK”，Agent 运行 `node scripts/approve.js`。
   - **第三步：自主执行**：基于全局配置，Agent 自动完成任务。
   - **第四步：持久化**：如果 `useSnapshots` 为 `true`，Agent 会将关键状态存入私有临时沙箱。

## 配置管理

本技能完全通过 OpenClaw 官方 CLI 进行管理。

**初始化配置（首次使用必选）**:
`openclaw config set skills.entries.multi-step-workflow.config '{"useSubAgents": false, "maxSubAgents": 3, "useSnapshots": false}' --strict-json`

**启用子代理（并行处理）**:
`openclaw config set skills.entries.multi-step-workflow.config.useSubAgents true --strict-json`

**启用任务快照（持久化记忆）**:
`openclaw config set skills.entries.multi-step-workflow.config.useSnapshots true --strict-json`

**查看当前配置**:
`openclaw config get skills.entries.multi-step-workflow.config`

## 核心脚本 (可审计)

- `path-resolver.js`：权限锁死存储映射器。
- `task-tracker.js`：进度追踪（0600 权限）。
- `approve.js`：审批标记（0600 权限）。
- `context-snapshot.js`：高忠实度状态快照。

## 仓库与反馈

该 Skill 是 [Agent-Skills](https://github.com/chyern/Agent-Skills) 系列的一部分。
欢迎下载、Star 或通过 Issue 提交反馈！

## 许可证

MIT
