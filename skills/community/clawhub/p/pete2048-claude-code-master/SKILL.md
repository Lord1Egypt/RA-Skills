---
name: claude-code-master
description: |
  Claude Code 终极使用指南 - 涵盖上下文工程、规范驱动开发、Hooks 回调、Sub Agents、Output Styles、SuperClaude 框架等高级技巧。当用户需要：1) 提升 Claude Code 编程效率，2) 省 Token 技巧，3) Spec-driven 开发，4) 多 Agent 协作，5) 自定义工作流，6) Claude Code 高级配置。MUST BE USED for Claude Code optimization, workflow setup, best practices.
---

# Claude Code Master - 终极使用指南

## 核心理念

**上下文工程 > 提示工程 > 靠感觉写代码**

Claude Code 的成功不在于模型能力，而在于上下文的完整性。本 skill 提供系统化的方法，让 Claude Code 从"能用"变成"高效专业"。

## 一、Context Engineering（上下文工程）

### 1.1 什么是上下文工程？

上下文工程是传统提示工程的范式转变：
- **提示工程**：关注措辞和句式，像给 AI 留便签
- **上下文工程**：提供完整体系化上下文，像为 AI 写完整剧本

### 1.2 核心文件结构

```
project/
├── .claude/
│   ├── commands/           # 自定义斜杠命令
│   ├── settings.local.json # 本地权限设置
│   ├── agents/            # Sub Agents 配置
│   └── output-styles/     # Output Styles 配置
├── CLAUDE.md              # 项目全局规则
├── .ai-rules/             # 工具无关的全局上下文
│   ├── product.md         # 项目愿景（"为什么"）
│   ├── tech.md           # 技术栈（"用什么"）
│   └── structure.md      # 文件结构（"在哪里"）
├── specs/                # 功能规范（Spec-driven）
│   └── feature-name/
│       ├── requirements.md  # 用户故事和验收标准
│       ├── design.md       # 技术架构
│       └── tasks.md        # 实现计划
├── PRPs/                 # 产品需求提示
│   └── templates/
│       └── prp_base.md
└── examples/             # 代码示例
```

### 1.3 CLAUDE.md 模板

```markdown
# 项目 AI 协作规则

## 项目感知
- 能理解规划文档、任务清单
- 自动读取 specs/ 目录下的规范文件

## 代码结构约束
- 文件大小：单文件 < 300 行
- 模块拆分：按功能域组织
- 命名规范：使用一致的命名模式

## 测试要求
- 单元测试：所有新功能必须有测试
- 覆盖率：最低 80%
- 测试框架：使用项目标准测试框架

## 编码风格
- 语言偏好：[指定语言]
- 格式规范：使用 linter 自动格式化
- 注释要求：复杂逻辑必须注释

## 文档规范
- API 文档：所有公开接口必须文档化
- README：保持更新
- 变更日志：记录重要变更
```

## 二、Spec-Driven Development（规范驱动开发）

### 2.1 两阶段工作流

**Phase 1: Planning（规划模式）**
- AI 角色：初级架构师
- 任务：通过交互式问答创建技术规范
- 输出：requirements.md, design.md, tasks.md

**Phase 2: Execution（执行模式）**
- AI 角色：细致的工程师
- 任务：严格按规范逐任务实现
- 特点：一次一个任务，外科手术般精确

### 2.2 PRP（产品需求提示）工作流

PRP = PRD + 精选代码库知识 + 智能体运行手册

**生成 PRP：**
```bash
/generate-prp INITIAL.md
```

**执行 PRP：**
```bash
/execute-prp PRPs/your-feature-name.md
```

### 2.3 INITIAL.md 模板

```markdown
## 功能：
[具体描述你想实现什么功能，清晰明确地写出需求]

## 示例：
[列出 examples/ 文件夹中参考的代码，并说明它们的用途]

## 文档链接：
[加入相关文档、API 说明或 MCP 服务器资源链接]

## 其他注意事项：
[说明任何易错点、特别需求，或 AI 可能忽略的内容]
```

## 三、Hooks 回调机制（省 Token 技巧）

### 3.1 核心思想

**Dispatch 模式：发射后不管，完成自动回报**

传统方式（高 Token 消耗）：
```
OpenClaw → 每隔几秒轮询 → Claude Code 状态
↓
重复轮询 = Token 爆炸
```

Hooks 方式（零轮询）：
```
OpenClaw → 下达任务 → Claude Code 独立运行
                      ↓
                    完成后触发 Hook
                      ↓
              自动通知 OpenClaw
```

### 3.2 配置示例

**latest.json 输出格式：**
```json
{
  "session_id": "abc123",
  "timestamp": "2026-02-09T14:54:27+00:00",
  "cwd": "/home/ubuntu/projects/hn-scraper",
  "event": "SessionEnd",
  "output": "Claude Code 的完整输出内容...",
  "status": "done"
}
```

**Wake Event 调用：**
```bash
curl -X POST "http://127.0.0.1:18789/api/cron/wake" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"text": "Claude Code 任务完成，读取 latest.json", "mode": "now"}'
```

### 3.3 双通道设计

| 通道 | 作用 | 为什么需要 |
|------|------|-----------|
| latest.json | 数据通道（存结果） | 持久化，不依赖服务在线 |
| wake event | 信号通道（通知到达） | 实时响应，秒级通知 |

**容错设计：** 即使 wake event 失败，latest.json 依然存在，AGI 最迟在下次 heartbeat 时也能发现。

## 四、Sub Agents（子智能体）

### 4.1 核心优势

1. **上下文保护**：独立上下文窗口，避免主对话污染
2. **专业化提升**：针对特定领域深度定制
3. **可重用性**：跨项目复用，团队共享
4. **权限管理**：不同 Sub Agent 不同工具访问级别

### 4.2 配置位置

- 项目级别：`.claude/agents/`（高优先级）
- 用户级别：`~/.claude/agents/`

### 4.3 内置 Sub Agents

**代码审查专家：**
```yaml
---
name: code-reviewer
description: 专业代码审查专家。在编写或修改代码后必须立即使用。
tools: file_search, bash, file_edit
---

你是一位资深代码审查专家，致力于确保代码质量和安全性。

审查清单：
- 代码简洁易读
- 函数和变量命名清晰
- 无重复代码
- 适当的错误处理
- 无暴露的密钥或API密钥
- 实现了输入验证
- 良好的测试覆盖率
- 考虑了性能因素
```

**调试专家：**
```yaml
---
name: debugger
description: 错误调试和问题排查专家。当遇到任何技术问题必须主动使用。
tools: file_search, file_edit, bash
---

你是一位专业的调试专家，专精于根因分析和问题解决。

调试流程：
- 分析错误信息和日志
- 检查最近的代码更改
- 形成并测试假设
- 添加策略性调试日志
- 检查变量状态
```

### 4.4 Kiro 工作流 Sub Agents

实现 AWS Kiro 风格的 spec-driven 开发：

1. **steering-architect** - 项目分析师，创建 .ai-rules/
2. **strategic-planner** - 规划师，创建 specs/feature/
3. **task-executor** - 执行器，逐任务实现

**使用方式：**
```bash
# 1. 项目初始化
"@steering-architect 分析现有代码库并创建项目指导文件"

# 2. 功能规划
"@strategic-planner 规划用户认证功能"

# 3. 逐步实现
"@task-executor 执行 specs/user-authentication/tasks.md 中的任务"
```

## 五、Output Styles（输出风格）

### 5.1 内置风格

1. **Default** - 面向高效软件工程协作
2. **Explanatory** - 讲解型，插入 Insights 解释实现选择
3. **Learning** - 学习型，边做边教，插入 TODO(human)

### 5.2 切换方式

```bash
# 交互式切换
/output-style

# 直接切换
/output-style explanatory
/output-style learning
```

### 5.3 自定义风格

**创建新风格：**
```bash
/output-style:new 我想要一个安全审计风格：偏严格、先 threat modeling、产出修复建议
```

**手动创建文件：**
```markdown
---
name: Code Reviewer
description: 自动化代码审查和优化
---

You are a specialized code review assistant...

## Core Workflow Process
...

## Response Structure
...
```

**存储位置：**
- 用户级：`~/.claude/output-styles/`
- 项目级：`.claude/output-styles/`（团队共享）

### 5.4 实用风格示例

**PRD Writer：**
```markdown
---
name: PRD Writer
description: "标准化 PRD 输出：背景、目标、指标、scope、用户故事、验收标准"
---

# Product Requirement Document - {title}
## 1. 概要
## 2. 背景与问题陈述
## 3. 目标（3-5个，可量化）
## 4. 成功衡量（KPI）
## 5. Scope（包含/不包含）
## 6. 用户画像与使用场景
## 7. UX / Flow
## 8. API / 数据需求
## 9. 非功能性需求
## 10. Risks & Mitigations
## 11. Rollout & Rollback Plan
## 12. Open Questions
## 13. Acceptance Criteria
```

## 六、SuperClaude 框架

### 6.1 安装

```bash
# 克隆项目
git clone https://github.com/NomenAK/SuperClaude.git
cd SuperClaude

# 执行安装
./install.sh

# 验证
ls -la ~/.claude/
ls -la ~/.claude/commands/
```

### 6.2 核心命令

**开发构建类：**
- `/build --react --magic --tdd` - React 项目开发
- `/build --api --tdd --coverage` - API 后端开发
- `/build --init --magic --c7 --plan` - 项目初始化

**分析类：**
- `/analyze --architecture --persona-architect` - 架构分析
- `/troubleshoot --investigate --prod` - 问题排查

**设计类：**
- `/design --api --ddd "功能描述"` - 领域驱动设计
- `/design --prd "产品描述"` - 生成 PRD

**运维类：**
- `/deploy --env staging --plan` - 部署规划
- `/scan --security --owasp` - 安全扫描

### 6.3 Persona 角色

```bash
-persona-architect    # 系统架构师
-persona-frontend     # 前端专家
-persona-backend      # 后端专家
-persona-security     # 安全专家
-persona-qa           # 质量保证
-persona-performance  # 性能专家
-persona-analyzer     # 分析专家
-persona-mentor       # 导师
-persona-refactorer   # 重构专家
```

### 6.4 通用标志

**规划与思考：**
- `-plan` - 显示执行计划
- `-think` - 标准分析
- `-think-hard` - 深度分析
- `-ultrathink` - 关键分析

**MCP 服务器：**
- `-c7` - 启用 Context7 文档查找
- `-seq` - 启用 Sequential 深度思维
- `-magic` - 启用 Magic UI 构建器
- `-pup` - 启用 Puppeteer 浏览器测试

**输出控制：**
- `-uc` - UltraCompressed 模式（70% token 减少）
- `-verbose` - 详细输出

### 6.5 必要的 MCP Server

```bash
# Context7 - 文档查找
claude mcp add --transport http context7 https://mcp.context7.com/mcp

# Sequential Thinking - 深度思维
claude mcp add sequential-thinking npx @modelcontextprotocol/server-sequential-thinking

# Puppeteer - 浏览器自动化
npx @modelcontextprotocol/server-puppeteer
claude mcp add puppeteer npx @modelcontextprotocol/server-puppeteer

# Magic - UI 构建
claude mcp add magic npx @21st-dev/magic@latest --env API_KEY=你的api_key
```

## 七、最佳实践

### 7.1 示例越多越好

`examples/` 文件夹对成功至关重要。AI 在有代码模式可参考时表现更出色。

**示例内容建议：**
- 代码结构模式（模块组织、导入规范）
- 测试用例模式（测试文件结构、mock 使用）
- 集成模式（API 客户端、数据库连接）
- 命令行工具模式（参数解析、错误处理）

### 7.2 验证机制

PRP 中自带测试任务，AI 会迭代执行直到全部通过：
1. 加载完整 PRP 与上下文
2. 使用 TodoWrite 创建详细计划
3. 逐步实现每个组件
4. 执行测试并修复错误
5. 确保满足所有功能与质量要求

### 7.3 INITIAL.md 要说清楚

- 不要假设 AI 知道你的意图
- 写明所有约束和需求
- 多引用示例代码
- 包含文档链接
- 说明易错点和注意事项

### 7.4 定制 CLAUDE.md

- 加入你的项目规范
- 写明代码风格要求
- 制定 AI 编码标准
- 定义测试要求
- 说明架构约束

### 7.5 Output Styles 最佳实践

- 团队将常用风格沉淀到 `.claude/output-styles/`
- 形成"标准化智能体角色库"
- 把经验固化为可执行的系统提示
- 支持项目/用户级自定义与复用

## 八、复杂工作流示例

### 8.1 完整开发流程

```bash
# 1. 项目规划
/design --api --ddd --plan --persona-architect

# 2. 前端开发
/build --react --magic --tdd --persona-frontend

# 3. 后端开发
/build --api --tdd --coverage --persona-backend

# 4. 质量检查
/review --quality --evidence --persona-qa

# 5. 安全扫描
/scan --security --owasp --persona-security

# 6. 性能优化
/improve --performance --iterate --persona-performance

# 7. 部署准备
/deploy --env staging --plan --persona-architect
```

### 8.2 问题排查流程

```bash
# 1. 问题分析
/troubleshoot --investigate --prod --persona-analyzer

# 2. 根因分析
/troubleshoot --prod --five-whys --seq --persona-analyzer

# 3. 性能分析
/analyze --profile --perf --seq --persona-performance

# 4. 修复实施
/improve --quality --threshold 95% --persona-refactorer
```

### 8.3 Spec-Driven 工作流

```bash
# 1. 项目初始化
"@steering-architect 分析代码库"

# 2. 创建功能规范
"@strategic-planner 规划用户认证功能"
# 输出: specs/user-auth/requirements.md, design.md, tasks.md

# 3. 逐步实现
"@task-executor 执行 specs/user-auth/tasks.md"
# 重复直到所有任务完成

# 4. 新功能继续
"@strategic-planner 规划支付系统"
"@task-executor 执行 specs/payment/tasks.md"
```

## 九、Token 优化技巧

### 9.1 使用 Hooks 避免轮询

- 传统轮询：每隔几秒查询状态 = Token 爆炸
- Hooks 回调：任务完成后自动通知 = 零轮询

### 9.2 使用 `-uc` 标志

UltraCompressed 模式可减少约 70% token 消耗：
```bash
/build --react --uc "todo应用"
```

### 9.3 善用 references 文件

将详细文档放入 `references/` 目录，只在需要时加载：
- 减少 SKILL.md 大小
- 按需加载详细内容
- 避免一次性消耗大量 token

### 9.4 Sub Agents 隔离上下文

- 每个 Sub Agent 独立上下文窗口
- 避免主对话被任务细节污染
- 专业化配置更高效

## 十、故障排查

### 10.1 Claude Code 常见问题

**问题：任务卡住不动**
- 解决：使用 `Ctrl+C` 中断，重新描述任务
- 预防：任务拆分更细，一次一个明确目标

**问题：生成代码质量差**
- 解决：提供更多 examples/ 示例代码
- 预防：完善 CLAUDE.md 规则，明确编码规范

**问题：偏离项目规范**
- 解决：检查 CLAUDE.md 配置，补充约束
- 预防：使用 Sub Agents 强制遵循特定模式

### 10.2 Hooks 不触发

检查清单：
- Hook 脚本是否有执行权限
- 文件路径是否正确
- API endpoint 是否可访问
- Token 是否有效

### 10.3 Sub Agents 未被调用

- 检查 description 描述是否清晰
- 确保触发关键词匹配
- 验证文件位置正确
- 重启 Claude Code

## 参考资源

- [Context Engineering Intro](https://github.com/coleam00/Context-Engineering-Intro)
- [SuperClaude](https://github.com/NomenAK/SuperClaude)
- [Claude Code Hooks](https://github.com/win4r/claude-code-hooks)
- [Anthropic Official Docs](https://docs.anthropic.com)
- [OpenClaw Documentation](https://docs.openclaw.ai)

---

**记住：上下文工程的效果比提示工程好 10 倍，比"靠感觉写代码"好 100 倍！**
