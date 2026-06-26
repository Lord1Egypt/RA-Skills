---
name: claude-code
description: 调用 Claude Code CLI 进行代码开发、代码审查、bug 修复和自动化任务。当用户需要：(1) 代码审查和审查 PR，(2) 重构和性能优化，(3) 编写测试，(4) 自动修复 lint 错误，(5) 创建 commit 和 PR，(6) 复杂的多文件代码修改，(7) 使用自然语言描述编程任务时使用此技能。此 skill 适用于 OpenClaw 通过 PTY 调用 Claude Code 的场景。
---

# Claude Code Skill

此技能允许 OpenClaw 通过 PTY 调用 Claude Code CLI 来执行各种编码任务。

## 安装和认证

### 检查安装状态

```powershell
claude auth status
```

### 安装 Claude Code (Windows PowerShell)

```powershell
irm https://claude.ai/install.ps1 | iex
```

或使用 WinGet:

```powershell
winget install Anthropic.ClaudeCode
```

### 登录

```powershell
claude auth login --email user@example.com
# 支持 SSO
claude auth login --sso
```

---

## 在 OpenClaw 中调用 Claude Code

由于 Claude Code 需要交互式 TTY，OpenClaw 必须使用 **PTY 模式**调用：

### 方式一：Print 模式 (非交互式，单次任务)

```powershell
# 执行单次查询，结果直接输出后退出
claude -p "解释 main.py 中的 auth 函数"

# 指定模型 (sonnet/haiku/opus)
claude -p --model sonnet "审查这个代码"

# 限制执行轮次
claude -p --max-turns 5 "修复这个 bug"

# JSON 输出
claude -p --output-format json "分析代码结构"
```

### 方式二：交互式模式 (复杂任务，需要 PTY)

```powershell
# 启动交互式会话，任务完成后退出
claude

# 带初始提示
claude "解释这个项目的结构"

# 继续最近的会话
claude -c
```

### 方式三：管道模式

```powershell
# 处理日志内容
Get-Content app.log | claude -p "找出异常"

# 审查 git 改动的文件
git diff main --name-only | claude -p "审查这些改动的文件"
```

---

## 完整 CLI 参数参考

| 参数 | 说明 | 示例 |
|------|------|------|
| `-p, --print` | 非交互式，打印结果后退出 | `claude -p "task"` |
| `-c, --continue` | 继续最近会话 | `claude -c` |
| `-r, --resume` | 恢复指定会话 | `claude -r session-name` |
| `--model` | 指定模型 (sonnet/haiku/opus) | `--model sonnet` |
| `--max-turns` | 限制执行轮次 | `--max-turns 3` |
| `--max-budget-usd` | 最大 API 花费 (print 模式) | `--max-budget-usd 5.00` |
| `--dangerously-skip-permissions` | 跳过权限确认 (慎用) | |
| `--output-format` | 输出格式 (text/json/stream-json) | `--output-format json` |
| `--input-format` | 输入格式 | `--input-format stream-json` |
| `--permission-mode` | 权限模式 (plan/auto/medium) | `--permission-mode plan` |
| `--allowedTools` | 允许的工具 (逗号分隔) | `--allowedTools Read,Bash` |
| `--disallowedTools` | 禁止的工具 | `--disallowedTools Edit` |
| `--add-dir` | 添加额外工作目录 | `--add-dir ../lib` |
| `--agent` | 指定子代理 | `--agent my-agent` |
| `--agents` | 动态定义子代理 (JSON) | |
| `--chrome` | 启用 Chrome 集成 | `--chrome` |
| `--from-pr` | 从 GitHub PR 恢复会话 | `--from-pr 123` |
| `--betas` | 启用 Beta 功能 | `--betas interleaved-thinking` |
| `--debug` | 调试模式 | `--debug "api,mcp"` |
| `--fallback-model` | 备用模型 | `--fallback-model haiku` |

---

## 权限模式

Claude Code 有三种权限模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `plan` | 只读分析，不修改文件 | 代码审查、安全检查 |
| `auto` | 自动执行，无需确认 | 快速开发 (谨慎使用) |
| `medium` | 执行前确认 | 日常开发 (默认) |

### 使用方式

```powershell
# Plan 模式 - 安全分析
claude --permission-mode plan -p "分析认证系统的安全问题"

# 交互式切换：Shift+Tab 循环切换模式
```

---

## 常用工作流

### 1. 代码审查

```powershell
# 审查改动的文件
git diff | claude -p "审查这些改动"

# 审查 PR
claude --from-pr 123 "审查这个 PR"

# 审查特定文件
claude -p "审查 auth.js 的安全性"
```

### 2. Bug 修复

```powershell
# 描述 bug 症状
claude -p "修复登录页面的 401 错误"

# 交互式修复
claude "用户报告支付失败，错误码 E001"
```

### 3. 编写测试

```powershell
claude -p "为 auth 模块编写单元测试"

# 完整流程：写测试 + 运行 + 修复
claude -p "为 auth 模块编写测试，运行并修复失败"
```

### 4. 代码重构

```powershell
claude -p "重构 utils.js 使用现代 JS 特性"
claude -p "优化这个函数的性能"
```

### 5. 理解新代码库

```powershell
claude "给我这个代码库的整体概览"
claude "查找处理用户认证的相关文件"
claude "追踪从登录到数据库的整个流程"
```

### 6. 创建 Commit 和 PR

```powershell
# 创建 commit
claude -p "用描述性消息提交我的改动"

# 创建分支并提交
claude -p "创建 feature/auth 分支并提交改动"

# 创建 PR
claude "创建 PR 并描述这次改动"
```

### 7. 处理文档

```powershell
claude -p "为 auth.js 添加 JSDoc 注释"
claude -p "查找项目中没有文档的函数"
```

---

## MCP 集成 (Model Context Protocol)

MCP 让 Claude Code 连接外部工具和服务。

### 添加 MCP Server

```powershell
# stdio 模式
claude mcp add server-name --transport stdio -- env VAR=value -- npx -y mcp-server

# HTTP 模式
claude mcp add server-name --transport http https://mcp-server.example.com

# SSE 模式
claude mcp add server-name --transport sse https://mcp-server.example.com
```

### 列出 MCP Servers

```powershell
claude mcp list
```

### 常用 MCP Servers

- **GitHub**: 代码库管理、PR、Issue
- **Filesystem**: 文件系统操作
- **Database**: 数据库查询
- **Slack/Discord**: 消息通知
- **Jira**: 任务管理

---

## 子代理 (Sub-agents)

Claude Code 可以调用专门的子代理处理特定任务。

### 使用子代理

```powershell
# 自动委托
claude -p "审查我的代码改动中的安全问题"

# 明确指定子代理
claude -p "使用 code-reviewer 子代理审查 auth 模块"
```

### 查看可用子代理

```powershell
claude agents
```

### 创建自定义子代理

在项目 `.claude/agents/` 目录创建 JSON 配置文件，或在项目根目录使用 `/agents` 命令。

---

## 在 OpenClaw 中的最佳实践

### 1. 简单任务用 Print 模式

```powershell
# OpenClaw 调用示例 (使用 exec + pty)
claude -p "审查 src/auth.js 的安全性" --permission-mode plan
```

### 2. 复杂任务用交互模式

```powershell
# 需要多轮交互时
claude "重构整个认证模块，使用 OAuth2"
```

### 3. 敏感操作用 Plan 模式

```powershell
# 代码审查、安全分析
claude --permission-mode plan -p "分析这个 PR 的安全风险"
```

### 4. 限制资源使用

```powershell
# 限制花费
claude -p --max-budget-usd 2.00 "修复这个 bug"

# 限制轮次
claude -p --max-turns 10 "重构这个函数"
```

### 5. 继续之前的工作

```powershell
# 继续最近会话
claude -c

# 继续指定会话
claude -r session-name "继续完成这个任务"
```

---

## 工具调用流程 (OpenClaw)

1. **检查 Claude Code 是否可用**
   ```powershell
   claude auth status
   ```

2. **选择调用模式**
   - 简单任务 → `--print` 模式
   - 复杂任务 → 交互式模式 (需要 PTY)
   - 继续工作 → `--continue` / `--resume`

3. **选择权限模式**
   - 只读分析 → `--permission-mode plan`
   - 日常开发 → `--permission-mode medium` (默认)
   - 自动化脚本 → `--permission-mode auto` (谨慎)

4. **执行并获取结果**

---

## 注意事项

- **PTY 必需**: Claude Code 交互式模式需要 TTY，OpenClaw 必须使用 `pty: true`
- **需要登录**: Claude Code 需要 Anthropic 账户
- **Print 模式限制**: 能力有限，复杂任务用交互式模式
- **权限安全**: 谨慎使用 `--dangerously-skip-permissions`
- **资源限制**: 生产环境建议设置 `--max-budget-usd`
- **会话管理**: 使用 `-c` / `-r` 继续之前的工作

---

## 第三方模型提供商配置

Claude Code 支持配置第三方兼容的模型 API 服务商，如阿里云百炼。

### 配置文件位置

```
%USERPROFILE%\.claude\settings.json
```

### 阿里云百炼配置示例

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-api-key-here",
    "ANTHROPIC_BASE_URL": "https://coding.dashscope.aliyuncs.com/apps/anthropic",
    "API_TIMEOUT_MS": "3000000"
  }
}
```

### 配置说明

| 环境变量 | 说明 | 示例值 |
|----------|------|--------|
| `ANTHROPIC_AUTH_TOKEN` | API Key (百炼控制台获取) | `sk-sp-xxxxxx` |
| `ANTHROPIC_BASE_URL` | API 端点地址 | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| `API_TIMEOUT_MS` | 请求超时时间 (毫秒) | `3000000` |

### 注意事项

1. **Base URL 格式**: 结尾**不要**包含 `/v1`，Claude Code 会自动添加
   - ❌ 错误: `https://xxx.com/apps/anthropic/v1`
   - ✅ 正确: `https://xxx.com/apps/anthropic`

2. **API Key 获取**: 登录阿里云百炼控制台 → 模型服务 → API-KEY

3. **可用模型**: 通过 `--model` 参数指定，如 `MiniMax-M2.5`

### 测试配置

```powershell
# 使用 curl 测试 API
$body = @{
    model = "MiniMax-M2.5"
    max_tokens = 20
    messages = @(
        @{role = "user"; content = "hi"}
    )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "https://coding.dashscope.aliyuncs.com/apps/anthropic/v1/messages" `
    -Method Post `
    -Headers @{
        "Authorization" = "Bearer YOUR_API_KEY"
        "Content-Type" = "application/json"
    } `
    -Body $body
```

---

## 快速命令参考

```powershell
# 认证
claude auth status          # 检查状态
claude auth login           # 登录
claude auth logout          # 登出

# 会话
claude                      # 新会话
claude "task"               # 带提示的新会话
claude -c                   # 继续最近会话
claude -r "name" "task"     # 恢复指定会话

# Print 模式
claude -p "task"            # 单次任务
claude -p --model sonnet    # 指定模型
claude -p --max-turns 5     # 限制轮次

# 工具
claude agents               # 列出子代理
claude mcp                  # MCP 管理
claude update               # 更新版本
```