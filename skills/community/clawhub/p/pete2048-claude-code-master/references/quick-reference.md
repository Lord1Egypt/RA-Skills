# Claude Code 快速参考指南

## 一、常用命令速查

### 1.1 基本操作

```bash
# 启动 Claude Code
claude

# 指定工作目录
claude --cwd /path/to/project

# 使用特定模型
claude --model claude-3-opus-20240229

# 非交互模式
claude -p "task description" --output-format json
```

### 1.2 Output Styles

```bash
# 查看所有风格
/output-style

# 切换到讲解模式
/output-style explanatory

# 切换到学习模式
/output-style learning

# 创建自定义风格
/output-style:new 我想要一个[描述]风格
```

### 1.3 Sub Agents

```bash
# 调用特定 sub agent
"@code-reviewer 审查这个 PR"
"@debugger 分析这个错误"
"@data-scientist 查询用户行为数据"
```

### 1.4 配置管理

```bash
# 打开配置
/config

# 查看当前设置
/settings

# MCP 服务器管理
/mcp
```

## 二、SuperClaude 命令速查

### 2.1 开发构建

```bash
# React 项目
/build --react --magic --tdd --persona-frontend

# API 后端
/build --api --tdd --coverage --persona-backend

# 项目初始化
/build --init --magic --c7 --plan

# 功能开发
/build --feature --tdd
```

### 2.2 分析审查

```bash
# 架构分析
/analyze --architecture --persona-architect

# 代码分析
/analyze --code --persona-analyzer

# 性能分析
/analyze --profile --perf --seq

# 安全扫描
/scan --security --owasp --persona-security
```

### 2.3 设计规划

```bash
# 领域驱动设计
/design --api --ddd "功能描述"

# 生成 PRD
/design --prd "产品描述"

# API 规范
/design --api --openapi "API 描述"
```

### 2.4 问题排查

```bash
# 问题调查
/troubleshoot --investigate --prod

# 根因分析
/troubleshoot --prod --five-whys --seq

# 性能问题
/troubleshoot --perf --persona-performance
```

### 2.5 优化改进

```bash
# 代码质量
/improve --quality --threshold 95%

# 性能优化
/improve --performance --iterate

# 重构
/improve --refactor --persona-refactorer
```

### 2.6 通用标志

```bash
# 规划与思考
-plan              # 显示执行计划
-think             # 标准分析
-think-hard        # 深度分析
-ultrathink        # 关键分析

# MCP 服务器
-c7                # Context7 文档查找
-seq               # Sequential 深度思维
-magic             # Magic UI 构建器
-pup               # Puppeteer 浏览器测试

# 输出控制
-uc                # UltraCompressed (70% token 减少)
-verbose           # 详细输出
```

## 三、Spec-Driven 工作流

### 3.1 Kiro 风格流程

```bash
# 1. 项目初始化
"@steering-architect 分析代码库"

# 2. 功能规划
"@strategic-planner 规划[功能名称]"

# 3. 逐步实现
"@task-executor 执行 specs/[feature]/tasks.md"
```

### 3.2 PRP 工作流

```bash
# 1. 编辑 INITIAL.md
vim INITIAL.md

# 2. 生成 PRP
/generate-prp INITIAL.md

# 3. 审核 PRP
vim PRPs/feature-prp.md

# 4. 执行 PRP
/execute-prp PRPs/feature-prp.md
```

## 四、文件路径速查

### 4.1 Claude Code 配置

```
~/.claude/
├── config.json              # 全局配置
├── settings.json            # 设置
├── commands/                # 自定义命令
├── agents/                  # Sub Agents
└── output-styles/           # Output Styles
```

### 4.2 项目配置

```
project/
├── .claude/
│   ├── settings.local.json  # 本地设置
│   ├── commands/            # 项目命令
│   ├── agents/              # 项目 Agents
│   └── output-styles/       # 项目 Styles
├── CLAUDE.md                # AI 规则
├── .ai-rules/               # 全局上下文
├── specs/                   # 功能规范
├── PRPs/                    # 产品需求提示
└── examples/                # 代码示例
```

### 4.3 Hooks

```
~/.claude/hooks/
├── stop-hook.sh             # 停止时触发
└── session-end-hook.sh      # 会话结束时触发

/tmp/claude-code-hooks/
└── latest.json              # 最新结果
```

## 五、MCP Server 配置

### 5.1 常用 MCP Server

```bash
# Context7 - 文档查找
claude mcp add --transport http context7 https://mcp.context7.com/mcp

# Sequential Thinking - 深度思维
claude mcp add sequential-thinking npx @modelcontextprotocol/server-sequential-thinking

# Puppeteer - 浏览器自动化
claude mcp add puppeteer npx @modelcontextprotocol/server-puppeteer

# Magic - UI 构建
claude mcp add magic npx @21st-dev/magic@latest --env API_KEY=your_key

# Filesystem - 文件系统
claude mcp add filesystem npx @anthropic-ai/mcp-server-filesystem /path/to/dir

# GitHub - GitHub 集成
claude mcp add github npx @anthropic-ai/mcp-server-github --env GITHUB_TOKEN=your_token
```

### 5.2 管理 MCP

```bash
# 列出所有 MCP
/mcp

# 添加新 MCP
/mcp add

# 删除 MCP
/mcp remove <name>

# 测试 MCP
/mcp test <name>
```

## 六、Persona 角色

```bash
-persona-architect      # 系统架构师
-persona-frontend       # 前端专家
-persona-backend        # 后端专家
-persona-security       # 安全专家
-persona-qa             # 质量保证
-persona-performance    # 性能专家
-persona-analyzer       # 分析专家
-persona-mentor         # 导师
-persona-refactorer     # 重构专家
```

## 七、环境变量

```bash
# OpenClaw Token（用于 Hooks）
export OPENCLAW_TOKEN="your-token"

# Claude API Key
export ANTHROPIC_API_KEY="your-api-key"

# 默认模型
export CLAUDE_MODEL="claude-3-opus-20240229"

# Hooks 开关
export CLAUDE_HOOKS_ENABLED="true"
```

## 八、常见场景

### 8.1 快速原型

```bash
# 一句话生成应用
/build --react --magic "todo list 应用"

# 快速 API
/build --api --tdd "用户管理 REST API"
```

### 8.2 代码审查

```bash
# 快速审查
"@code-reviewer 审查最近的代码变更"

# 深度审查
/analyze --code --persona-analyzer --seq
```

### 8.3 问题调试

```bash
# 调试错误
"@debugger 分析这个错误: [错误信息]"

# 根因分析
/troubleshoot --prod --five-whys
```

### 8.4 学习新代码库

```bash
# 切换到讲解模式
/output-style explanatory

# 分析架构
/analyze --architecture --persona-architect

# 走查代码
"为 services/ 目录做系统性走查"
```

### 8.5 生成文档

```bash
# API 文档
/analyze --code --doc --persona-backend

# PRD 文档
/design --prd "功能描述"

# 架构文档
/analyze --architecture --doc
```

## 九、最佳实践速记

### 9.1 Token 优化

✅ **使用 `-uc` 标志** - 减少 70% token
✅ **使用 Hooks** - 避免轮询消耗
✅ **善用 references/** - 按需加载
✅ **Sub Agents** - 隔离上下文

### 9.2 代码质量

✅ **提供 examples/** - 示例越多越好
✅ **完善 CLAUDE.md** - 明确项目规范
✅ **使用 Persona** - 专业化角色
✅ **测试驱动** - 总是使用 `-tdd`

### 9.3 工作流优化

✅ **Spec-Driven** - 先规划后执行
✅ **逐步验证** - 每步都测试
✅ **版本控制** - 所有配置纳入 Git
✅ **团队共享** - 项目级配置

## 十、故障排查速查

| 问题 | 解决方案 |
|------|---------|
| 任务卡住 | Ctrl+C 中断，重新描述 |
| 代码质量差 | 增加 examples/，完善 CLAUDE.md |
| 偏离规范 | 检查 CLAUDE.md，使用 Sub Agents |
| Hook 不触发 | 检查权限、路径、配置 |
| MCP 不工作 | 检查安装、API key、网络 |
| Token 超限 | 使用 `-uc`，优化上下文 |

---

**记住：上下文工程 > 提示工程 > 靠感觉写代码！**
