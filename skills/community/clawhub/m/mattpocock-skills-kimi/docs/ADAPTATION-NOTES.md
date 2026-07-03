# 本地化适配说明 (Adaptation Notes)

## 适配原则

本仓库对 [mattpocock/skills](https://github.com/mattpocock/skills) 的适配遵循以下原则：

1. **方法论不变**：核心思想、流程、词汇完全保留
2. **触发方式适配**：从 `/command` 手动触发改为 model-invoked 自动触发
3. **工具调用通用化**：从 Claude 专属工具（`run`, `gh`）改为 Kimi 通用工具（`Bash`, `PythonRun`, GitHub MCP）
4. **配置抽象化**：从 `CLAUDE.md` 硬编码改为检测 + 询问用户偏好

---

## 逐 Skill 修改记录

### `grilling`

- 触发方式：从 `disable-model-invocation: true` 改为 model-invoked
- Description 重写：加入 Kimi 触发关键词（"对齐需求"、"讨论计划"、"设计确认"）
- 工具调用：无特殊工具，纯对话 skill，无需修改

### `handoff`

- 输出路径：从 `$TMPDIR` / `/tmp` 改为当前 workspace
- 打开文件：移除 `xdg-open` / `open` / `start`，改为告知文件路径
- 工具调用：`Bash` 检测 OS temp dir → `Write` 写入 workspace

### `domain-modeling`

- 文件读取：从假设 `.claude/` 有配置改为检测项目内 `CONTEXT.md`
- 文件写入：使用 `Read` / `Write` 工具操作 `CONTEXT.md` 和 `docs/adr/`
- Kimi Claw 适配：指令描述为通用文件操作，不绑定具体工具名

### `codebase-design`

- 纯参考 skill，工具调用极少，主要修改 description 触发词

### `tdd`

- 测试运行：从 `run` 改为 `Bash` 执行测试命令
- 类型检查：从 `run` 改为 `Bash` 执行 `tsc` / 等效命令
- Kimi Claw 适配：测试运行指令描述为"执行项目测试命令"，由 OpenClaw 环境解析

### `diagnosing-bugs`

- 反馈循环构建：从 `run` 改为 `Bash` / `PythonRun`
- 调试器/REPL：保留描述，但工具调用通用化

### `grill-with-docs`

- 依赖 `grilling` + `domain-modeling`，修改同两者
- 有代码库检测：从 `CLAUDE.md` 存在改为 `CONTEXT.md` 或项目文件存在

### `to-prd`

- Issue Tracker：从 `gh issue create` 改为抽象层
  - 检测 `docs/agents/issue-tracker.md` 配置
  - 若无配置，询问用户：GitHub MCP / GitHub Token / GitHub CLI / 本地 Markdown
  - 已配置：按配置方式执行
  - 失败：回退本地 markdown，告知用户
- PRD 模板：保留原版，加入 Kimi 生态说明

---

## Issue Tracker 抽象层设计

```
┌────────────────────────────────────────────┐
│ 用户触发 to-prd / triage 等需要 Issue Tracker 的 skill │
└────────────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │ 检测配置文件是否存在？   │
        │ docs/agents/issue-tracker.md │
        └───────────────────────┘
              │          │
           存在 ▼      不存在 ▼
          读取配置      询问用户偏好
              │          │
              ▼          ▼
        ┌───────────────────────┐
        │ 按配置方式执行          │
        │ - GitHub MCP           │
        │ - GitHub Token (env)   │
        │ - GitHub CLI (gh)      │
        │ - 本地 Markdown        │
        └───────────────────────┘
                    │
              执行失败？
                    │
              是 ▼
        回退本地 Markdown
        告知用户失败原因
```

---

## Kimi Work vs Kimi Claw 差异处理

| 场景 | Kimi Work | Kimi Claw (OpenClaw) |
|------|-----------|----------------------|
| 工具调用 | `Bash`, `PythonRun`, `Read`, `Write` | 通用指令描述，由 OpenClaw 解析执行 |
| 文件路径 | 绝对 Windows 路径 | 通用相对路径 |
| 测试运行 | AI 直接执行 | AI 生成命令，用户执行或 OpenClaw 代理执行 |
| 浏览器 | `kimi-webbridge` 可用 | 可能有 WebBridge 插件 |

skill 正文中的工具调用描述尽量通用化，例如：
- "运行测试" 而非 `Bash: pytest`
- "读取文件" 而非 `Read: /path/to/file`

---

## 版本记录

| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-06-16 | v0.1.0 | 仓库初始化，目录结构创建 |
