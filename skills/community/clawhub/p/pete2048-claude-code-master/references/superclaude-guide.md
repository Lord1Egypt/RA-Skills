# SuperClaude 完整指南

## 一、什么是 SuperClaude？

SuperClaude 是一个专门为 Claude Code 设计的综合配置框架，通过结构化的配置文件和专业化的工作流程，极大地增强 Claude Code 的开发能力。

### 核心价值

- **认知专业化**：9 种专业思维模式
- **工作流程标准化**：19 个专业斜杠命令
- **智能文档查找**：通过 Context7 自动引用官方文档
- **Token 优化**：UltraCompressed 模式节省 70% token

## 二、安装配置

### 2.1 安装步骤

```bash
# 克隆项目
git clone https://github.com/NomenAK/SuperClaude.git
cd SuperClaude

# 执行安装脚本
./install.sh

# 验证安装
ls -la ~/.claude/
ls -la ~/.claude/commands/
```

### 2.2 安装后的目录结构

```
~/.claude/
├── commands/              # 19 个斜杠命令
│   ├── build.md          # 构建命令
│   ├── analyze.md        # 分析命令
│   ├── design.md         # 设计命令
│   ├── improve.md        # 改进命令
│   ├── troubleshoot.md   # 排查命令
│   ├── deploy.md         # 部署命令
│   ├── scan.md           # 扫描命令
│   ├── review.md         # 审查命令
│   └── migrate.md        # 迁移命令
├── personas/             # 9 个专业角色
├── settings.json         # 配置
└── mcp.json             # MCP 配置
```

### 2.3 必要的 MCP Server

```bash
# Context7 - 文档查找（重要！）
claude mcp add --transport http context7 https://mcp.context7.com/mcp

# Sequential Thinking - 深度思维
claude mcp add sequential-thinking npx @modelcontextprotocol/server-sequential-thinking

# Puppeteer - 浏览器测试
claude mcp add puppeteer npx @modelcontextprotocol/server-puppeteer

# Magic - UI 构建（需要 API key）
claude mcp add magic npx @21st-dev/magic@latest --env API_KEY=your_api_key
```

## 三、核心命令详解

### 3.1 `/build` - 构建开发

**用途**：创建新项目、开发功能

**常用组合**：

```bash
# React 项目开发
/build --react --magic --tdd --persona-frontend

# API 后端开发
/build --api --tdd --coverage --persona-backend

# 项目初始化
/build --init --magic --c7 --plan --persona-frontend

# 功能开发
/build --feature --tdd --persona-frontend

# 全栈应用
/build --fullstack --magic --tdd
```

**标志说明**：
- `--react` - React 框架
- `--api` - REST API
- `--magic` - 启用 Magic UI 构建器
- `--tdd` - 测试驱动开发
- `--coverage` - 代码覆盖率检查
- `--c7` - 启用 Context7 文档查找
- `--plan` - 显示执行计划

### 3.2 `/analyze` - 分析审查

**用途**：分析代码库、架构、性能

**常用组合**：

```bash
# 架构分析
/analyze --architecture --persona-architect

# 代码分析
/analyze --code --persona-analyzer

# 性能分析
/analyze --profile --perf --seq --persona-performance

# 安全分析
/analyze --security --persona-security

# 完整分析
/analyze --architecture --code --perf --seq
```

### 3.3 `/design` - 设计规划

**用途**：生成 PRD、API 规范、架构设计

**常用组合**：

```bash
# 领域驱动设计
/design --api --ddd "功能描述" --persona-architect

# 生成 PRD
/design --prd "产品描述" --persona-frontend

# API 规范（OpenAPI）
/design --api --openapi "API 描述" --persona-backend

# 系统设计
/design --system --ddd --plan --persona-architect
```

### 3.4 `/troubleshoot` - 问题排查

**用途**：调试错误、性能问题、生产问题

**常用组合**：

```bash
# 问题调查
/troubleshoot --investigate --prod --persona-analyzer

# 根因分析（5 Whys 方法）
/troubleshoot --prod --five-whys --seq --persona-analyzer

# 性能问题
/troubleshoot --perf --persona-performance

# 复杂问题（深度分析）
/troubleshoot --investigate --prod --five-whys --seq --ultrathink
```

### 3.5 `/improve` - 优化改进

**用途**：代码优化、重构、性能提升

**常用组合**：

```bash
# 代码质量改进
/improve --quality --threshold 95% --persona-refactorer

# 性能优化
/improve --performance --iterate --persona-performance

# 重构
/improve --refactor --persona-refactorer

# 迭代改进
/improve --quality --iterate --threshold 90%
```

### 3.6 `/scan` - 扫描检查

**用途**：安全扫描、依赖检查

**常用组合**：

```bash
# 安全扫描（OWASP Top 10）
/scan --security --owasp --persona-security

# 依赖扫描
/scan --dependencies --persona-security

# 完整安全检查
/scan --security --owasp --dependencies --persona-security
```

### 3.7 `/review` - 代码审查

**用途**：PR 审查、代码质量检查

**常用组合**：

```bash
# 代码审查
/review --quality --evidence --persona-qa

# PR 审查
/review --pr --quality --persona-qa

# 安全审查
/review --security --persona-security
```

### 3.8 `/deploy` - 部署发布

**用途**：部署规划、环境配置

**常用组合**：

```bash
# 部署规划
/deploy --env staging --plan --persona-architect

# 生产部署
/deploy --env production --plan --persona-architect

# 回滚准备
/deploy --env production --rollback
```

### 3.9 `/migrate` - 迁移升级

**用途**：数据库迁移、框架升级

**常用组合**：

```bash
# 数据库迁移
/migrate --database --plan --persona-backend

# 框架升级
/migrate --framework --plan --persona-architect
```

## 四、Persona 角色系统

### 4.1 可用角色

| 角色 | 专注领域 | 使用场景 |
|------|---------|---------|
| `architect` | 系统设计和可扩展性 | 架构设计、技术选型 |
| `frontend` | UX 和 React 开发 | 前端开发、UI 组件 |
| `backend` | API 和性能优化 | 后端开发、数据库设计 |
| `security` | 威胁建模和安全代码 | 安全审计、漏洞修复 |
| `qa` | 质量保证和测试 | 测试计划、代码审查 |
| `performance` | 性能优化和瓶颈分析 | 性能调优、优化策略 |
| `analyzer` | 根因分析和调试 | 问题排查、错误调试 |
| `mentor` | 教学和指导 | 学习新技术、知识传递 |
| `refactorer` | 代码质量和简化 | 代码重构、清理技术债 |

### 4.2 使用方式

```bash
# 方式 1：作为标志使用
/build --react --persona-frontend

# 方式 2：独立调用
/persona-architect "设计微服务架构"

# 方式 3：组合使用
/analyze --architecture --code --persona-architect --persona-security
```

## 五、通用标志详解

### 5.1 规划与思考

```bash
-plan          # 显示执行计划（执行前预览）
-think         # 标准分析模式
-think-hard    # 深度分析模式
-ultrathink    # 关键分析模式（最强）
```

**使用建议**：
- 简单任务：不需要思考标志
- 中等复杂：使用 `-think`
- 高复杂度：使用 `-think-hard`
- 关键决策：使用 `-ultrathink`

### 5.2 MCP 服务器控制

```bash
-c7            # 启用 Context7 文档查找
-seq           # 启用 Sequential 深度思维
-magic         # 启用 Magic UI 构建器
-pup           # 启用 Puppeteer 浏览器测试
```

**MCP Server 作用**：
- **Context7**：自动查找官方文档，确保代码基于最新最佳实践
- **Sequential**：提供更深入的思考和分析能力
- **Magic**：自动生成 UI 组件，加速前端开发
- **Puppeteer**：浏览器自动化测试和验证

### 5.3 输出控制

```bash
-uc            # UltraCompressed 模式（约70% token 减少）
-verbose       # 详细输出模式
```

**使用建议**：
- Token 紧张：使用 `-uc`
- 学习场景：使用 `-verbose`
- 正常开发：默认即可

### 5.4 特定功能标志

```bash
-init          # 项目初始化
-feature       # 功能开发
-tdd           # 测试驱动开发
-coverage      # 代码覆盖率
-e2e           # 端到端测试
-dry-run       # 预演模式（不实际执行）
-rollback      # 回滚准备
```

## 六、复杂工作流示例

### 6.1 完整产品开发流程

```bash
# 1. 项目规划阶段
/design --prd "社交应用" --plan --persona-architect
/design --api --ddd "社交应用" --persona-architect

# 2. 前端开发阶段
/build --init --magic --c7 --plan --persona-frontend
/build --react --magic --tdd --persona-frontend

# 3. 后端开发阶段
/build --api --tdd --coverage --persona-backend

# 4. 质量检查阶段
/review --quality --evidence --persona-qa
/scan --security --owasp --persona-security

# 5. 性能优化阶段
/improve --performance --iterate --persona-performance

# 6. 部署准备阶段
/deploy --env staging --plan --persona-architect
```

### 6.2 问题排查完整流程

```bash
# 1. 问题发现
/troubleshoot --investigate --prod --persona-analyzer

# 2. 根因分析
/troubleshoot --prod --five-whys --seq --persona-analyzer

# 3. 性能分析（如果是性能问题）
/analyze --profile --perf --seq --persona-performance

# 4. 修复实施
/improve --quality --threshold 95% --persona-refactorer

# 5. 验证修复
/review --quality --evidence --persona-qa
```

### 6.3 代码重构流程

```bash
# 1. 代码质量分析
/analyze --code --persona-analyzer

# 2. 识别重构点
/analyze --architecture --persona-architect --seq

# 3. 制定重构计划
/design --refactor --plan --persona-refactorer

# 4. 执行重构
/improve --refactor --persona-refactorer

# 5. 测试验证
/build --tdd --coverage --persona-qa
```

## 七、高级技巧

### 7.1 组合多个 MCP Server

```bash
# 结合 Context7 + Sequential Thinking
/build --react --magic --c7 --seq --think-hard

# 全栈开发：前端 + 后端 + 测试
/build --fullstack --magic --tdd --c7 --seq
```

### 7.2 Token 优化策略

```bash
# 使用 UltraCompressed 模式
/build --react --uc "todo list 应用"

# 结合 -plan 预览，避免重复
/build --react --plan --uc "todo list 应用"

# 使用 Context7 避免提供大量文档
/build --react --c7 "使用最新的 Next.js 14"
```

### 7.3 学习新技术栈

```bash
# 切换到讲解模式
/output-style explanatory

# 使用 mentor persona
/persona-mentor "教我如何实现 GraphQL API"

# 结合文档查找
/build --api --c7 --persona-mentor "GraphQL API 教程"
```

## 八、与 Context Engineering 的结合

SuperClaude 可以与 Context Engineering 完美结合：

```bash
# 1. 使用 SuperClaude 生成 PRD
/design --prd "功能描述" --persona-architect

# 2. 将 PRD 转换为 PRP
/generate-prp INITIAL.md

# 3. 执行 PRP
/execute-prp PRPs/feature.md

# 4. 使用 SuperClaude 进行质量检查
/review --quality --evidence --persona-qa
```

## 九、常见问题

### 9.1 命令不生效

**问题**：输入 `/build` 没有反应

**解决**：
1. 检查是否正确安装：`ls -la ~/.claude/commands/`
2. 重启 Claude Code
3. 检查命令格式：使用 `/build` 而非 `build`

### 9.2 MCP Server 不工作

**问题**：`-c7` 标志无效

**解决**：
1. 检查 MCP 配置：`/mcp`
2. 测试 MCP 连接：`/mcp test context7`
3. 重新安装 MCP：`claude mcp add ...`

### 9.3 Persona 不生效

**问题**：`--persona-architect` 没有改变行为

**解决**：
1. 确保使用双破折号：`--persona-architect`
2. 检查安装：`ls -la ~/.claude/personas/`
3. 尝试独立调用：`/persona-architect "任务"`

## 十、最佳实践

### 10.1 项目初始化

```bash
# 一次性设置完整环境
/build --init --magic --c7 --plan --persona-architect
```

### 10.2 日常开发

```bash
# 功能开发
/build --feature --tdd --c7

# 快速原型
/build --react --magic --uc "功能描述"
```

### 10.3 代码审查

```bash
# 定期审查
/review --quality --evidence --persona-qa --seq
```

### 10.4 性能优化

```bash
# 定期优化
/improve --performance --iterate --persona-performance
```

---

**SuperClaude 官方仓库**：https://github.com/NomenAK/SuperClaude
