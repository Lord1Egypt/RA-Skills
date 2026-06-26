---
name: kiro
description: Kiro agentic IDE 开发工作流指南。使用 spec 驱动开发、hooks 自动化、steering 规则、MCP 集成和 powers 扩展。当用户需要：(1) 用 Kiro 创建/管理 specs，(2) 配置 hooks 自动化工作流，(3) 设置 steering 规则，(4) 连接 MCP 服务器，(5) 使用 powers 扩展 agent 能力，(6) 从原型到生产的完整开发流程。
---

# Kiro 开发工作流

## 概述

Kiro 是 Amazon 开发的 agentic IDE 和 CLI 工具，支持规格驱动开发（Spec-Driven Development）。本技能指导你使用 Kiro 的核心功能从原型快速迭代到生产。

**核心能力**：
- **Specs** - 结构化规格文档，将需求拆解为详细实现计划
- **Hooks** - 基于文件变化和开发事件的自动化触发器
- **Steering** - 通过 markdown 文件定义自定义规则和项目上下文
- **MCP Servers** - 通过 Model Context Protocol 连接外部工具和数据源
- **Powers** - 按需扩展 agent 能力的领域特定知识和集成

## 快速开始

### 1. 安装 Kiro

**IDE（桌面应用）**：
- 访问 [kiro.dev](https://kiro.dev) 下载
- 支持 macOS、Windows、Linux

**CLI（命令行）**：
```bash
# 安装 CLI（参考官方文档）
npm install -g @kiro/cli
```

### 2. 创建第一个 Spec

Spec 是 Kiro 的核心，用于结构化规划功能开发：

```bash
# 在项目根目录创建 spec
kiro spec create "用户认证系统"
```

Spec 标准结构（位于 `.kiro/specs/`）：
- `requirements.md` - 需求定义和用户故事
- `design.md` - 技术设计和架构
- `tasks.md` - 实现任务清单

### 3. 配置 Steering

在项目根目录创建 `.kiro/steering/` 目录，添加规则文件：

```markdown
# .kiro/steering/project-rules.md
## 代码风格
- 使用 TypeScript 严格模式
- 函数不超过 50 行
- 所有公共 API 必须有 JSDoc

## 项目上下文
- 技术栈：Next.js 15 + TypeScript + Tailwind
- 部署目标：Vercel
- 数据库：Supabase
```

### 4. 设置 Hooks

Hooks 自动化重复任务，配置文件变化触发：

```yaml
# .kiro/hooks.yaml
hooks:
  - name: auto-format
    trigger: file.save
    pattern: "*.ts"
    action: run "prettier --write {{file}}"
    
  - name: run-tests
    trigger: file.save
    pattern: "src/**/*.test.ts"
    action: run "npm test"
```

## 核心工作流

### Spec 驱动开发流程

1. **创建 Spec** → 定义需求和验收标准
2. **Review Spec** → 与 Kiro agent 讨论完善
3. **生成 Tasks** → 自动拆解为实现任务
4. **执行 Tasks** → Agent 按任务逐步实现
5. **验证验收** → 对照验收标准测试

### 使用 Agentic Chat

Kiro 的聊天功能理解整个项目上下文：

```
用户：帮我实现用户登录功能
Kiro：我看到你在 .kiro/specs/auth/requirements.md 中定义了登录需求。
     我将按照 spec 中的验收标准逐步实现：
     1. 创建登录表单组件
     2. 实现 Supabase 认证
     3. 添加错误处理
     4. 编写单元测试
     
     开始吗？
```

### 连接 MCP 服务器

MCP 允许 Kiro 访问外部工具和数据：

```json
// .kiro/mcp.json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "options": {
        "allowedPaths": ["/Users/mac/.openclaw/workspace"]
      }
    }
  }
}
```

## 最佳实践

### Spec 编写规范

**好的 Spec 特征**：
- ✅ 清晰的用户故事和验收标准
- ✅ 可测试的需求描述
- ✅ 技术实现细节分离到 design.md
- ✅ 任务拆解到可独立完成的粒度

**避免**：
- ❌ 模糊的需求描述（"提升性能"）
- ❌ 混合需求和实现细节
- ❌ 缺少验收标准

### Steering 规则设计

**有效规则**：
```markdown
## 错误处理
- 所有 async 函数必须用 try-catch 包裹
- API 错误必须返回标准格式：{ error: { code, message } }
- 禁止吞掉错误而不记录日志
```

**无效规则**：
```markdown
## 代码质量
- 写好代码（过于模糊）
- 保持简洁（没有可操作标准）
```

### Hooks 自动化策略

**推荐 Hooks**：
- 保存时自动格式化
- 提交前运行 lint
- 测试文件保存时运行测试
- Spec 更新时同步任务状态

**避免**：
- 耗时操作（>5 秒）阻塞保存
- 依赖外部网络服务的同步操作

## 常见问题

### Q: Spec 应该多详细？
A: 足够让另一个开发者理解需求并实现，但不包含具体代码实现。通常 2-5 页 markdown。

### Q: 如何迁移现有 VS Code 项目？
A: Kiro 支持一键导入 VS Code 设置和扩展。首次启动时会提示迁移。

### Q: MCP 服务器安全吗？
A: MCP 服务器在沙箱中运行，通过明确配置的允许路径访问资源。建议最小权限原则。

## 资源导航

### 官方文档
- [Kiro 文档](https://kiro.dev/docs/)
- [CLI 指南](https://kiro.dev/docs/cli)
- [首个项目教程](https://kiro.dev/docs/getting-started/first-project/)

### 社区
- [Discord](https://discord.gg/kirodotdev)
- [GitHub 仓库](https://github.com/kirodotdev/kiro)

---

**参考文件**：
- `references/spec-template.md` - Spec 模板和示例
- `references/hooks-reference.md` - Hooks 配置完整参考
- `references/mcp-servers.md` - 可用 MCP 服务器列表

**脚本工具**：
- `scripts/create-spec.py` - 快速创建标准结构 Spec
- `scripts/validate-hooks.py` - 验证 hooks 配置语法

**资产模板**：
- `assets/steering-templates/` - 常用 steering 规则模板
