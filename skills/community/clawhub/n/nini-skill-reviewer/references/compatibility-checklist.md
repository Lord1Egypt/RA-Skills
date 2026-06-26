# Compatibility Checklist

审计 skill 的跨平台、跨 Agent、npx skills 生态兼容性。逐项扫描目标 skill 的所有文件。

## Platform — 跨平台兼容性

### Critical

**macOS-only 命令**

扫描以下命令。若出现且无跨平台替代，标记 Critical：

- `osascript` — AppleScript 自动化
- `defaults` — macOS 偏好设置
- `launchctl` — macOS 服务管理
- `say` — macOS 语音合成
- `pbcopy` / `pbpaste` — macOS 剪贴板

**macOS-only 工具**

- `reminders-cli` / `reminders` — Apple Reminders CLI（EventKit）
- `icalBuddy` — Apple Calendar CLI
- `brew install` — Homebrew（macOS/Linux，非 Windows）

> 若 skill 本质上是 macOS 专属（如管理 Apple Calendar），应在 description 中明确标注 "macOS only"。

### High

**Windows 不兼容**

- `.sh` 脚本是否有 PowerShell 替代或 Windows 说明
- 安装说明是否覆盖多平台（brew / apt / winget / choco / scoop）

**平台标注缺失**

- 含 macOS-only 功能的 skill 是否在 SKILL.md 开头或 description 中声明平台限制

### Medium

**hardcoded Unix 路径**

- `/tmp`、`~/`、`/usr/local/` 等 Unix 专属路径
- 建议使用环境变量或相对路径替代

### Low

**Python 可移植性**

- 优先使用 `pathlib.Path` 而非 `os.path.join` 手动拼接
- 避免 hardcoded 路径分隔符 `/`

## Agent — 跨 Agent 兼容性

### Critical

**MCP 工具引用**

扫描 `mcp__` 前缀。MCP 协议是 Claude Code 特性，Codex CLI 不支持。

若 skill 依赖 MCP 工具（如 `mcp__yunxiao__*`），标记 Critical 并建议：

- 提供 CLI fallback 方案（如 `aliyun` CLI 替代 MCP 工具）
- 或在文档中声明 "Requires Claude Code with MCP"

### High

**Claude Code 专属工具**

以下工具在 Codex CLI 中不可用：

- `WebFetch` — 网页内容获取
- `Task` — 子 agent 调度
- `Skill` — skill 调用
- `TodoWrite` — 任务列表管理
- `NotebookEdit` — Jupyter notebook 编辑
- `AskUserQuestion` — 交互式问答

若 skill 指令中要求使用这些工具，标记 High。

**并行 Agent 模式**

- `subagent_type=` — 子 agent 类型指定
- 多 agent 并行编排

这些是 Claude Code 专属能力。

### Medium

**降级路径缺失**

skill 使用了 Claude Code 专属功能但未提供替代方案：

- 无 MCP 时的 CLI fallback
- 无 WebFetch 时的 bash curl 替代
- 无 Task 并行时的顺序执行方案

### Tool Reference Best Practices

skill 指令优先使用 Claude Code 工具术语（便于 Claude Code 直接理解），同时用 `>` blockquote 提供其他环境的 fallback。

**原则：Claude Code-first，fallback 补充**

| Claude Code 术语 | fallback 备注 |
|------------------|--------------|
| `WebFetch: <URL>` | `> 其他环境：curl -sL <URL>` |
| `使用 Task 工具并行启动` | `> 其他 Agent 环境：以下检查相互独立，可按顺序执行` |
| `使用 Context7 获取文档` | `> 若未安装 Context7 MCP，从 GitHub 仓库直接获取` |
| `subagent: 云效数据` | `> 其他环境：直接调用 yunxiao skill 或 aliyun CLI` |

**模板：**

```text
使用 Task 工具并行启动多个检查 Agent。

> 其他 Agent 环境：以下检查相互独立，可按顺序依次执行。
```

### 通用工具（无需 fallback）

以下工具在主流 Agent 中通用：

- `Bash` — 命令执行
- `Read` / `Write` / `Edit` — 文件操作
- `Grep` / `Glob` — 搜索

## Distribution — npx skills 生态兼容性

### Critical

**marketplace.json 注册**

检查 `.claude-plugin/marketplace.json`：

- skill 目录路径（如 `./skills/skill-name`）是否在某个 plugin group 的 `skills` 数组中
- 未注册 = 无法通过 `npx skills add` 安装

**路径安全**

扫描所有文件，不得包含：

- 绝对路径（如 `/Users/xxx/`、`C:\Users\xxx\`）
- 仓库根路径引用（如 `../../scripts/`）

所有 references/ 和 scripts/ 引用必须是相对于 skill 目录的相对路径。

### High

**自包含性**

skill 通过 `npx skills add` 安装后以 symlink 形式存在。以下情况导致安装后不可用：

- 引用仓库级脚本（如 `./scripts/validate.sh`）
- 依赖仓库级配置文件（如根目录的 `.markdownlint.json`）

**跨 skill 依赖**

若 skill A 功能依赖 skill B（如 diary-assistant → schedule-manager）：

- 是否在文档中明确声明依赖关系
- 两者是否在同一 plugin group（确保一起安装）
- 若不在同 group，是否说明缺失时的降级行为

### Medium

**plugin group 归属**

skill 是否放在语义正确的 group：

- workflow-skills — 工作流自动化
- writing-skills — 写作相关
- learning-skills — 学习工具
- fun-skills — 趣味/创意

**description 可搜索性**

description 是否包含足够关键词让 `npx skills find <keyword>` 能发现：

- 英文关键词（供国际用户搜索）
- 中文触发词（供中文用户搜索）
- 功能领域关键词
