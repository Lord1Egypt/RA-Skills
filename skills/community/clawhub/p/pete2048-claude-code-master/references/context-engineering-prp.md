# Context Engineering 和 PRP 工作流详解

## 一、Context Engineering 核心概念

### 1.1 为什么需要上下文工程？

大多数 AI 智能体失败的原因：
- ❌ 不是模型能力不足
- ✅ 缺乏足够的上下文信息

**效果对比：**
- 上下文工程 vs 提示工程：10x 提升
- 上下文工程 vs 靠感觉写代码：100x 提升

### 1.2 核心组件

```
Context Engineering = {
    项目规则 (CLAUDE.md)
  + 代码示例 (examples/)
  + 文档引用 (references/)
  + 验证流程 (tests/)
  + 规范系统 (specs/)
}
```

## 二、项目结构详解

### 2.1 标准目录结构

```
project/
├── .claude/                    # Claude Code 配置
│   ├── commands/              # 自定义斜杠命令
│   │   ├── generate-prp.md   # 生成 PRP
│   │   └── execute-prp.md    # 执行 PRP
│   ├── settings.local.json   # 本地权限
│   ├── agents/               # Sub Agents
│   └── output-styles/        # Output Styles
│
├── .ai-rules/                 # 工具无关的全局上下文
│   ├── product.md            # 产品愿景
│   ├── tech.md               # 技术栈
│   └── structure.md          # 文件结构
│
├── specs/                     # 功能规范
│   └── feature-name/
│       ├── requirements.md    # 需求文档
│       ├── design.md         # 设计文档
│       └── tasks.md          # 任务清单
│
├── PRPs/                      # 产品需求提示
│   ├── templates/
│   │   └── prp_base.md
│   └── feature-prp.md
│
├── examples/                  # 代码示例
│   ├── README.md
│   ├── api-client.ts
│   ├── test-pattern.ts
│   └── component-pattern.tsx
│
├── CLAUDE.md                  # AI 全局规则
└── INITIAL.md                 # 初始需求模板
```

### 2.2 .ai-rules/ 文件详解

#### product.md - 产品愿景

```markdown
---
title: Product Vision
description: "Defines the project's core purpose, target users, and main features."
inclusion: always
---

# Product Vision

## 产品名称
[产品名称]

## 核心价值主张
[一句话描述产品解决的核心问题]

## 目标用户
- 主要用户：[描述]
- 次要用户：[描述]

## 主要功能
1. [功能 1]
2. [功能 2]
3. [功能 3]

## 成功指标
- [指标 1]
- [指标 2]

## 业务约束
- [约束 1]
- [约束 2]
```

#### tech.md - 技术栈

```markdown
---
title: Technology Stack
description: "Technology choices, frameworks, and tools used in the project."
inclusion: always
---

# Technology Stack

## 核心技术
- **语言**: TypeScript/Python/Go
- **框架**: Next.js/FastAPI/Gin
- **数据库**: PostgreSQL/MongoDB
- **缓存**: Redis

## 开发工具
- **包管理器**: pnpm/poetry/go mod
- **测试框架**: Jest/pytest/go test
- **Linter**: ESLint/Ruff/golangci-lint
- **Formatter**: Prettier/Black/gofmt

## 部署
- **容器化**: Docker
- **编排**: Kubernetes
- **CI/CD**: GitHub Actions

## 常用命令
```bash
# 开发
pnpm dev

# 测试
pnpm test

# 构建
pnpm build

# Lint
pnpm lint
```

## 关键依赖版本
- Next.js: 14.x
- React: 18.x
- TypeScript: 5.x
```

#### structure.md - 文件结构

```markdown
---
title: Project Structure
description: "File organization and naming conventions."
inclusion: always
---

# Project Structure & Conventions

## 目录组织

### /src/app - 应用页面
- 页面级组件和路由

### /src/components - 组件库
- 可复用的 UI 组件
- 子目录按功能域组织

### /src/lib - 工具库
- 共享工具函数
- API 客户端
- 类型定义

### /src/hooks - 自定义 Hooks
- 可复用的 React Hooks

### /src/types - 类型定义
- TypeScript 接口和类型

## 命名规范

### 文件命名
- 组件: PascalCase.tsx
- 工具: camelCase.ts
- 类型: types.ts
- 测试: *.test.ts

### 组件结构
```typescript
// 1. Imports
import React from 'react'

// 2. Types
interface Props {
  // ...
}

// 3. Component
export function Component({ prop }: Props) {
  // ...
}

// 4. Styles
const styles = {
  // ...
}
```

## 代码组织原则
- 单一职责原则
- 每个文件 < 300 行
- 相关文件就近放置
- 共享代码提升到 lib/
```

## 三、PRP（产品需求提示）工作流

### 3.1 什么是 PRP？

**PRP = PRD + 精选代码库知识 + 智能体运行手册**

它是 AI 能够一次性生成接近可交付代码的最小可行单元。

### 3.2 PRP 工作流程

```
┌─────────────┐
│  INITIAL.md │  用户的初始需求描述
└──────┬──────┘
       │
       ├─> /generate-prp
       │
       ▼
┌─────────────────┐
│   Analysis      │  分析代码库
│   ┌─────────┐   │
│   │ Patterns│   │  查找相似实现
│   │ Docs    │   │  收集相关文档
│   │ Examples│   │  提取代码示例
│   └─────────┘   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Generate PRP   │  生成详细 PRP
│                 │
│  - 上下文信息    │
│  - 实现步骤      │
│  - 验证检查点    │
│  - 测试要求      │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Human Review   │  人工审核 PRP
│                 │
│  ⚠️ 必须审核!   │
└──────┬──────────┘
       │
       ├─> /execute-prp
       │
       ▼
┌─────────────────┐
│  Implementation │  执行实现
│                 │
│  1. 创建计划     │
│  2. 逐步实现     │
│  3. 运行测试     │
│  4. 修复错误     │
│  5. 验证完成     │
└─────────────────┘
```

### 3.3 INITIAL.md 模板

```markdown
# 功能需求

## 功能：
构建一个基于 BeautifulSoup 的异步爬虫，抓取电商产品信息，支持速率限制，结果存入 PostgreSQL

## 示例：
参考 `examples/crawler/` 中的爬虫模式
- base_crawler.py - 基础爬虫类
- async_client.py - 异步 HTTP 客户端
- rate_limiter.py - 速率限制实现

## 文档链接：
- BeautifulSoup 文档: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- asyncio 文档: https://docs.python.org/3/library/asyncio.html
- PostgreSQL Python: https://www.postgresql.org/docs/current/python.html

## 其他注意事项：
- 必须遵守 robots.txt
- 实现指数退避重试机制
- 支持代理轮换
- 需要处理 JavaScript 渲染的页面
- 常见陷阱：
  - 不要在同一域名上并发过多请求
  - 注意 User-Agent 轮换
  - 处理反爬虫检测
```

### 3.4 PRP 模板结构

```markdown
# PRP: {功能名称}

## 概览
- **功能名称**: {name}
- **优先级**: P0/P1/P2
- **预计时间**: {duration}
- **置信度**: {1-10}

## 上下文信息

### 技术栈
[从 tech.md 提取的相关技术栈]

### 相关代码模式
[从 examples/ 提取的相关代码示例]

### 文档资源
[从 INITIAL.md 提取的文档链接]

## 实现步骤

### Task 1: {task name}
**目标**: {description}
**文件**: {files to create/modify}
**验证**: {how to verify}

**实现细节**:
```python
# 伪代码或关键实现
```

**测试**:
```python
def test_{task_name}():
    # 测试代码
```

### Task 2: {task name}
[同上结构]

## 错误处理
- 预期错误: {error}
- 处理方式: {handling}

## 验收标准
- [ ] 标准 1
- [ ] 标准 2
- [ ] 标准 3

## 风险和注意事项
- 风险 1: {description}
- 缓解措施: {mitigation}
```

## 四、斜杠命令定义

### 4.1 generate-prp.md

**文件位置：** `.claude/commands/generate-prp.md`

```markdown
# Generate PRP Command

When this command is triggered with a file path argument:

1. **Read INITIAL.md**
   - Parse the feature request
   - Extract key requirements
   - Identify referenced examples

2. **Analyze Codebase**
   - Search for similar implementations
   - Identify relevant patterns
   - Find existing utilities

3. **Collect Documentation**
   - Parse provided documentation links
   - Extract relevant sections
   - Note best practices

4. **Generate PRP**
   - Create detailed implementation steps
   - Include code examples
   - Add validation checkpoints
   - Write test requirements

5. **Save Output**
   - Create `PRPs/{feature-name}.md`
   - Present to user for review

## Output Format
[标准 PRP 格式，见 3.4]
```

### 4.2 execute-prp.md

**文件位置：** `.claude/commands/execute-prp.md`

```markdown
# Execute PRP Command

When this command is triggered with a PRP file path:

1. **Load Context**
   - Read entire PRP
   - Load referenced examples
   - Understand project structure

2. **Create Plan**
   - Use TodoWrite to generate task list
   - Order tasks by dependencies
   - Estimate time for each

3. **Execute Tasks**
   - Implement each component
   - Follow PRP specifications exactly
   - Don't skip or combine steps

4. **Validate**
   - Run all tests
   - Fix errors iteratively (max 3 attempts)
   - Ensure all acceptance criteria met

5. **Report**
   - Summarize changes made
   - List files created/modified
   - Note any deviations from PRP

## Rules
- Execute ONE task at a time
- Run tests after each task
- Don't proceed if tests fail
- Ask for clarification if ambiguous
```

## 五、实战案例

### 案例 1：添加用户认证功能

**INITIAL.md:**
```markdown
## 功能：
为现有 API 添加 JWT 用户认证系统

## 示例：
- examples/auth/jwt-handler.ts - JWT 生成和验证
- examples/auth/middleware.ts - 认证中间件
- examples/auth/user-model.ts - 用户模型

## 文档链接：
- JWT.io: https://jwt.io/
- Passport.js: http://www.passportjs.org/

## 其他注意事项：
- 密码使用 bcrypt 加密
- Token 有效期 7 天
- 支持刷新 token
- 需要速率限制防止暴力破解
```

**执行流程:**
```bash
# 1. 生成 PRP
/generate-prp INITIAL.md

# 2. 审核生成的 PRP
# 打开 PRPs/user-authentication.md 检查

# 3. 执行 PRP
/execute-prp PRPs/user-authentication.md
```

### 案例 2：构建数据分析管道

**INITIAL.md:**
```markdown
## 功能：
构建 ETL 数据管道，从多个源提取数据，转换后加载到数据仓库

## 示例：
- examples/etl/extractor.py - 数据提取器基类
- examples/etl/transformer.py - 转换器模式
- examples/etl/loader.py - 数据加载器

## 文档链接：
- Apache Airflow: https://airflow.apache.org/
- Pandas: https://pandas.pydata.org/

## 其他注意事项：
- 支持增量更新
- 错误不中断整个管道
- 记录数据血缘
- 支持回滚
```

## 六、最佳实践

### 6.1 INITIAL.md 编写要点

✅ **好的写法：**
```markdown
## 功能：
构建一个 RESTful API 端点 /api/users/{id}/orders，返回用户的所有订单，支持分页和过滤

## 示例：
- examples/api/user-endpoint.ts - 类似的 API 端点实现
- examples/api/pagination.ts - 分页工具

## 其他注意事项：
- 需要验证用户权限
- 默认按时间倒序排列
- 每页最大 100 条记录
```

❌ **不好的写法：**
```markdown
## 功能：
做个订单 API

## 其他注意事项：
要快
```

### 6.2 PRP 审核检查清单

- [ ] 所有技术决策都有说明
- [ ] 实现步骤清晰且可执行
- [ ] 包含足够的代码示例
- [ ] 测试覆盖所有关键功能
- [ ] 错误处理考虑周全
- [ ] 性能影响已评估
- [ ] 安全问题已考虑

### 6.3 examples/ 最佳实践

**内容建议：**
1. **代码结构模式** - 模块组织、导入规范
2. **测试用例模式** - 测试文件结构、mock 使用
3. **集成模式** - API 客户端、数据库连接
4. **错误处理模式** - 异常捕获、错误传播

**examples/README.md 示例：**
```markdown
# Code Examples

## API Patterns
- `api-client.ts` - REST API 客户端实现
- `api-middleware.ts` - 认证和日志中间件

## Testing Patterns
- `test-helpers.ts` - 测试工具函数
- `mock-factories.ts` - Mock 数据生成器

## Component Patterns
- `component-template.tsx` - React 组件模板
- `hook-pattern.ts` - 自定义 Hook 模板
```

## 七、与 Spec-Driven Development 的结合

PRP 工作流可以与 Kiro 风格的 spec-driven 开发结合：

```
INITIAL.md
    ↓
/generate-prp
    ↓
PRPs/feature.md
    ↓
人工审核 + 提取到 specs/
    ↓
specs/feature/
├── requirements.md
├── design.md
└── tasks.md
    ↓
@task-executor 逐步执行
```

这种结合方式：
1. PRP 提供详细的实现指导
2. specs/ 提供规范化的文档结构
3. Sub Agents 确保执行的精确性

---

**记住：PRP 生成后一定要亲自校对！PRP 框架的设计就是让你参与其中，确保上下文的准确性。执行的质量取决于 PRP 的质量。**
