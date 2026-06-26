---
name: interactive-skills-platform-mvp
description: >
  设计并落地 Skills Web 平台 MVP，让非技术用户无需 CLI 即可使用 SKILL.md 能力。
  用于“skills 平台”“skill 网页化”“interactive skills platform”“上传 SKILL.md 生成 UI”
  “对话式执行 skill”等需求，输出可执行的架构方案、API 设计、分阶段清单、验收与风险计划。
model: opus
---

# Design: Interactive Skills Platform (MVP)

## 何时使用

当用户出现以下诉求时启用本 skill：
- “把 skill 做成网页给非技术用户用”
- “做一个 skills 平台 / interactive skills platform”
- “上传 SKILL.md 并自动生成交互 UI”
- “要对话式引导，而不是表单式参数输入”

## 目标产出

在一次会话内，默认交付以下内容（可按用户要求裁剪）：
1. 明确的 Problem/Goal/Non-Goal 定义
2. MVP 架构方案（前端、后端、存储、执行链路）
3. API 草案（上传、分析、对话、执行、状态查询）
4. 分阶段实施清单（按周）
5. 验证方案（至少用 2 个真实 skills）
6. 风险清单与后续迭代边界

## 执行工作流（必须按顺序）

### Phase 1: 问题对齐（最少提问）

- 先复述用户目标与边界，确认是否只做 MVP。
- 如果信息缺失，只问 1-3 个关键问题（例如部署环境、目标用户、首批 skills）。
- 明确是否已有代码仓库；若无，则按“新项目”输出。

### Phase 2: 方案设计（先给推荐）

- 先给一个推荐方案，再给备选方案，不做“选项轰炸”。
- 推荐方案必须覆盖：
  - Monorepo 结构
  - 前后端技术栈
  - skills 存储与 metadata 结构
  - Claude API 分析链路
  - Agent SDK 执行链路
  - 动态 UI 策略（text/progress/url）

### Phase 3: 交付可执行计划

- 输出分阶段任务，要求每项任务可直接实现和验收。
- 必须包含：
  - 完成定义（Definition of Done）
  - 基本测试用例
  - 错误处理与回退策略

### Phase 4: MVP 现实性审查

- 强制检查是否过度设计（YAGNI）。
- 明确“本期不做什么”，避免范围蔓延。
- 标注 blocker（必须解决）与 nice-to-have（可后移）。

## 输出格式要求

- 默认中文输出，结构尽量固定：背景 -> 问题 -> 方案 -> 清单 -> 风险。
- 对架构和流程，优先给可落地清单而非抽象原则。
- 若用户要“直接开工”，把清单细化成可以逐步实现的工程任务。
- 若用户要“先评审”，给出关键 trade-off 与推荐结论。

## 质量标准

- 方案必须能支撑以下最小闭环：
  1) 上传 SKILL.md
  2) AI 分析出参数和 UI 配置
  3) 对话收集参数
  4) 执行 skill
  5) 渲染结果（文本/进度/链接）
- 至少包含一个短任务样例（如 felo-search）和一个长任务样例（如 felo-slides）。
- 明确列出安全、认证、市场化等延后议题，避免假性完成。

## 参考设计稿（可直接复用）

> Status: Draft
> Created: 2026-03-06
> Repo: skills-ai-page (Monorepo)

## Background

Skills 创作者创作了有用的 skills（Claude Code/OpenClaw），但这些 skills 只能在命令行工具中运行，只有技术用户能用。创作者希望让更多非技术用户也能使用自己的 skills，从而扩大 skills 的影响力和价值。

## Problem Statement

**WHO**: Skills 创作者

**SITUATION**:
- 创作了有用的 skills（可能包含 Python 脚本、CLI 调用等）
- 想让更多人使用自己的 skills
- 但 skills 只能在 Claude Code/OpenClaw 中运行，只有技术用户能用

**PROBLEM**:
Skills 的传播和使用受限于技术门槛 - 潜在用户装不好 Claude Code/OpenClaw，创作者的作品无法触达非技术用户

**IMPACT**:
- 创作者的作品价值无法最大化
- 好的 skills 埋没在技术圈子里
- 无法形成 skills 创作者生态

## Related Features

目前没有 `.features/` 目录，这是新项目。

## Goals

1. **降低 skills 使用门槛** - 非技术用户无需安装 Claude Code，通过 Web 界面即可使用 skills
2. **智能交互体验** - 对话式引导 + 动态 UI，不只是填表单
3. **验证核心价值** - 用真实 skills（felo-skills）验证方案可行性

## Non-Goals

- 不做安全沙箱隔离（MVP 阶段不考虑，后面迭代）
- 不做用户认证和权限管理（MVP 阶段不考虑）
- 不做 skills 市场功能（发布、评分、付费等）
- 不做复杂的数据可视化（图表、地图等，MVP 只支持基础 UI）

## Jobs to be Done

**Functional Job**:
- Skills 创作者：让我的 skills 能被更多人使用
- 普通用户：不需要懂技术就能用 skills 完成任务

**Social Job**:
- 创作者：展示自己的作品，获得认可
- 用户：使用先进的 AI 工具，提升效率

**Emotional Job**:
- 创作者：成就感（作品被使用）
- 用户：轻松感（不需要学习复杂工具）

## Solution

### Overview

创建一个 Web 平台，用户上传 Claude Code 标准的 `SKILL.md` 文件，平台使用 Claude API 分析 skill 并生成交互界面，通过 Claude Agent SDK 执行 skills。

**核心特性：**
1. **对话式交互（A）** - 用户不填表单，而是跟 AI 对话，AI 引导用户提供必要信息
2. **动态 UI（B）** - 根据 skill 特性生成不同的交互界面（进度条、链接、预览等）

### Architecture

**Monorepo 结构：**

```text
skills-ai-page/
├── frontend/          # React + TypeScript
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/           # 对话界面
│   │   │   ├── SkillUpload/    # 上传 skills
│   │   │   ├── DynamicUI/      # 动态 UI 组件
│   │   │   │   ├── ProgressBar.tsx
│   │   │   │   ├── LinkOutput.tsx
│   │   │   │   └── TextOutput.tsx
│   │   │   └── SkillList/      # Skills 列表
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── store/              # Zustand 状态管理
│   └── package.json
├── backend/           # Python + FastAPI
│   ├── app/
│   │   ├── api/
│   │   │   ├── skills.py       # Skills CRUD
│   │   │   ├── chat.py         # 对话接口
│   │   │   └── execute.py      # 执行 skills
│   │   ├── services/
│   │   │   ├── skill_analyzer.py    # Claude 分析 SKILL.md
│   │   │   ├── agent_executor.py    # Claude Agent SDK 执行
│   │   │   └── ui_generator.py      # 生成 UI 配置
│   │   └── storage/
│   │       └── file_storage.py      # 文件系统存储
│   ├── skills/                      # Skills 存储目录
│   │   ├── felo-search/
│   │   │   ├── SKILL.md
│   │   │   └── metadata.json
│   │   └── felo-slides/
│   │       ├── SKILL.md
│   │       └── metadata.json
│   └── requirements.txt
└── README.md
```

### Detailed Design

#### 1. Skills 上传与存储

**用户上传 SKILL.md：**
- 前端：文件上传组件
- 后端：接收文件，保存到 `skills/{skill-name}/SKILL.md`
- 生成 `metadata.json`（创建时间、skill 名称等）

**文件存储结构：**
```text
skills/
├── felo-search/
│   ├── SKILL.md
│   └── metadata.json
└── felo-slides/
    ├── SKILL.md
    └── metadata.json
```

**metadata.json 格式：**
```json
{
  "name": "felo-search",
  "description": "Real-time web search",
  "created_at": "2026-03-06T10:00:00Z",
  "author": "anonymous",
  "ui_config": {
    "type": "chat",
    "supports_progress": false,
    "output_types": ["text", "markdown"]
  }
}
```

#### 2. AI 分析 SKILL.md

**调用 Claude API 分析：**
- 输入：SKILL.md 内容
- 输出：
  - Skill 功能描述
  - 需要的参数（名称、类型、描述）
  - 需要的 UI 类型（chat、progress、link 等）
  - 预期输出类型（text、file、url 等）

**Prompt 示例：**
```text
分析以下 SKILL.md，提取：
1. Skill 的功能描述（一句话）
2. 需要的输入参数（JSON 格式）
3. 需要的 UI 类型（chat/progress/link）
4. 预期输出类型（text/file/url）

SKILL.md:
{skill_content}

返回 JSON 格式。
```

**返回示例：**
```json
{
  "description": "Real-time web search with AI-generated answers",
  "parameters": [
    {
      "name": "query",
      "type": "string",
      "description": "Search query",
      "required": true
    }
  ],
  "ui_type": "chat",
  "supports_progress": false,
  "output_types": ["text", "markdown"]
}
```

#### 3. 对话式交互

**用户点击"使用这个 skill"：**
1. 进入对话界面（类似 ChatGPT）
2. AI 发送欢迎消息：「这个 skill 可以帮你 {description}，你想做什么？」
3. 用户输入需求
4. AI 引导用户提供必要参数（对话式）
5. 参数收集完成后，调用后端执行 skill

**对话流程示例（felo-search）：**
```text
AI: 这个 skill 可以帮你进行实时网络搜索，你想搜索什么？
User: 东京今天天气
AI: 好的，正在搜索"东京今天天气"...
[调用 skill 执行]
AI: [展示搜索结果]
```

**对话流程示例（felo-slides）：**
```text
AI: 这个 skill 可以帮你生成 PPT，你想生成什么主题的 PPT？
User: React 入门教程，5 页
AI: 好的，正在生成"React 入门教程"PPT，大约需要 5-10 分钟...
[显示进度条]
AI: PPT 生成完成！[点击查看](https://...)
```

#### 4. 动态 UI 渲染

**根据 skill 的 ui_config 渲染不同的 UI：**

**A) 基础对话（默认）：**
- 文本输入/输出
- Markdown 渲染

**B) 进度展示：**
- 进度条组件
- 状态文本（进行中/完成/失败）
- 用于长时间运行的 skills（如 felo-slides）

**C) 链接输出：**
- 可点击的链接
- 可选：iframe 预览

**前端组件：**
```tsx
function DynamicUI({ uiConfig, data }) {
  if (uiConfig.supports_progress && data.status === "running") {
    return <ProgressBar progress={data.progress} />;
  }

  if (uiConfig.output_types.includes("url")) {
    return <LinkOutput url={data.url} />;
  }

  return <TextOutput content={data.content} />;
}
```

#### 5. 执行 Skills

**后端使用 Claude Agent SDK 执行：**

```python
from claude_agent_sdk import Agent

async def execute_skill(skill_name: str, parameters: dict):
    # 读取 SKILL.md
    skill_path = f"skills/{skill_name}/SKILL.md"
    with open(skill_path, "r", encoding="utf-8") as f:
        skill_content = f.read()

    # 创建 Agent
    agent = Agent(skill_content=skill_content)

    # 执行
    result = await agent.execute(parameters)

    return result
```

**执行流程：**
1. 前端发送执行请求（skill_name + parameters）
2. 后端创建 Agent，加载 SKILL.md
3. Agent SDK 执行 skill（调用 Bash 工具、Claude API 等）
4. 返回结果给前端
5. 前端根据 ui_config 渲染结果

#### 6. MVP 支持的 UI 类型

| UI 类型 | 用途 | 示例 Skill |
|---------|------|-----------|
| 对话式交互 | 文本输入/输出 | felo-search |
| 进度展示 | 长时间任务状态 | felo-slides |
| 链接输出 | URL 结果 | felo-slides |

**不支持（后面迭代）：**
- 文件上传/下载
- 数据可视化（图表）
- 画布/编辑器
- 地图/视频

### Why This Approach

**为什么选择对话式交互 + 动态 UI？**
- **差异化价值** - 其他平台都是填表单，我们是对话式，更自然
- **降低门槛** - 用户不需要理解参数，AI 引导即可
- **更好的体验** - 动态 UI 让 skills 看起来像真正的产品

**为什么选择 Python + FastAPI？**
- Claude Agent SDK 有 Python 版本，集成方便
- FastAPI 现代、快速，适合 API 开发
- Python 生态丰富，适合 AI 相关开发

**为什么选择文件存储而不是数据库？**
- MVP 阶段快速验证，不需要配置数据库
- 文件存储符合 skills 的文件结构（SKILL.md）
- 版本控制友好（可以用 git）
- 后面可以轻松迁移到数据库

**为什么选择 Monorepo？**
- MVP 阶段代码量不大，放一起方便管理
- 前后端可以共享类型定义
- 部署简单

## Alternatives Considered

### Option A: 只生成表单，不做对话式交互
- **优点**: 实现简单，工作量小
- **缺点**: 用户体验差，没有差异化价值
- **拒绝理由**: 不够 cool，无法吸引用户

### Option B: 支持所有类型的动态 UI（图表、画布、编辑器等）
- **优点**: 功能强大，用户体验好
- **缺点**: 工作量大，MVP 阶段不现实
- **拒绝理由**: 过度设计，先验证核心价值

### Option C: 后端用 Node.js
- **优点**: 前后端语言统一，性能好
- **缺点**: Claude Agent SDK 的 Node.js 支持不如 Python
- **拒绝理由**: Python 更适合 AI 相关开发

### Option D: 使用数据库存储
- **优点**: 查询效率高，扩展性好
- **缺点**: 需要配置数据库，增加复杂度
- **拒绝理由**: MVP 阶段不需要，文件存储足够

## Implementation Checklist

### Phase 1: 基础架构（Week 1）
- [ ] 创建 Monorepo 项目结构
- [ ] 前端：React + TypeScript + Tailwind CSS 脚手架
- [ ] 后端：Python + FastAPI 脚手架
- [ ] 文件存储：实现 skills 的 CRUD 操作
- [ ] API 设计：定义前后端接口

### Phase 2: Skills 上传与分析（Week 1-2）
- [ ] 前端：Skills 上传组件
- [ ] 后端：接收并保存 SKILL.md
- [ ] 集成 Claude API：分析 SKILL.md
- [ ] 生成 ui_config（UI 类型、参数定义）
- [ ] 前端：Skills 列表展示

### Phase 3: 对话式交互（Week 2-3）
- [ ] 前端：对话界面组件（类似 ChatGPT）
- [ ] 后端：对话接口（接收用户消息，返回 AI 回复）
- [ ] 集成 Claude API：引导用户提供参数
- [ ] 参数收集逻辑（对话式）
- [ ] 前端：消息渲染（Markdown 支持）

### Phase 4: 动态 UI（Week 3）
- [ ] 前端：进度条组件
- [ ] 前端：链接输出组件
- [ ] 前端：文本输出组件（Markdown）
- [ ] 前端：根据 ui_config 动态渲染
- [ ] 后端：返回 UI 配置给前端

### Phase 5: Skills 执行（Week 3-4）
- [ ] 集成 Claude Agent SDK（Python）
- [ ] 后端：执行 skills 接口
- [ ] 后端：处理长时间任务（进度更新）
- [ ] 前端：轮询任务状态（felo-slides）
- [ ] 错误处理和重试逻辑

### Phase 6: 验证与测试（Week 4）
- [ ] 导入 felo-skills 仓库的两个 skills
- [ ] 测试 felo-search（对话式搜索）
- [ ] 测试 felo-slides（进度展示 + 链接输出）
- [ ] 修复 bug 和优化体验
- [ ] 部署到测试环境

### Phase 7: 部署（Week 4）
- [ ] 前端部署到 Vercel/Netlify
- [ ] 后端部署到云服务器
- [ ] 配置域名和 HTTPS
- [ ] 监控和日志

## Open Questions

### 1. 安全性问题（后面迭代）
- **问题**: Skills 可以执行任意 CLI 命令，如何防止恶意代码？
- **可能方案**:
  - 容器隔离（Docker/K8s）
  - 沙箱执行（Firecracker、gVisor）
  - 白名单 CLI（只允许安全命令）
  - 人工审核 + 容器隔离
- **决策时机**: V2 迭代时讨论

### 2. 数据库迁移（后面迭代）
- **问题**: 文件存储扩展性差，何时迁移到数据库？
- **可能方案**: PostgreSQL + SQLAlchemy
- **决策时机**: 用户数 > 100 或 skills 数 > 50 时

### 3. 用户认证（后面迭代）
- **问题**: 如何管理用户和权限？
- **可能方案**:
  - OAuth（GitHub、Google）
  - 自建用户系统
- **决策时机**: V2 迭代时讨论

### 4. Skills 市场（后面迭代）
- **问题**: 如何让创作者发布、分享、甚至售卖 skills？
- **可能方案**:
  - 公开/私有 skills
  - 评分和评论
  - 付费 skills（Stripe 集成）
- **决策时机**: V3 迭代时讨论

### 5. 更多 UI 类型（后面迭代）
- **问题**: 何时支持图表、画布、编辑器等复杂 UI？
- **可能方案**:
  - 图表：ECharts/Recharts
  - 画布：Fabric.js/Konva
  - 编辑器：Monaco Editor/CodeMirror
- **决策时机**: 根据用户反馈决定优先级

## References

- [Claude Agent SDK Documentation](https://github.com/anthropics/anthropic-sdk-python)
- [felo-skills Repository](https://github.com/Felo-Inc/felo-skills)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
