---
name: multi-agent-project-builder
description: 多 Agent 项目协作工厂 - 一键实现智能分工完成互联网项目
version: 1.0.0
author: 爱马仕
license: MIT
metadata:
  hermes:
    tags:
      - multi-agent
      - project-builder
      - ai-collaboration
      - task-delegation
      - automation
    related_skills:
      - autonomous-ai-agents/multi-agent-coordination
---

# 多 Agent 项目协作工厂

帮助新手在 OpenClaw/Hermes/Claude 上实现真正意义上的多 Agent 协作，完成互联网项目。通过专业分工的 AI 协作自动完成复杂项目，将大任务分解为需求分析、资料调研、架构设计、代码实现、测试验证等环节，由专业 Agent 并行协作完成。

## 功能特性

- 🎯 **智能任务分解** - 自动将复杂项目拆分为多个子任务
- 👥 **专业 Agent 分工** - 5 个专业角色：分析师、研究员、架构师、实现者、测试者
- 🔄 **并行协作** - 支持并行执行独立任务，提高效率
- 📋 **任务追踪** - 实时跟踪每个 Agent 的进度和产出
- 🎨 **可自定义配置** - 支持自定义 Agent 角色、任务流程、输出格式
- 📦 **一键生成** - 提供脚本自动生成完整项目结构
- 🌐 **跨平台支持** - 兼容 OpenClaw、Hermes、Claude 等多个平台

## 核心概念

### Agent 角色

| 角色 | 职责 | 关键产出 |
|------|------|----------|
| **Analyst (分析师)** | 需求分析、用户调研、功能规划 | 需求文档、功能清单、用户故事 |
| **Researcher (研究员)** | 技术调研、竞品分析、方案选型 | 调研报告、技术选型建议、参考资料 |
| **Architect (架构师)** | 系统设计、架构规划、接口定义 | 架构图、技术方案、API 文档 |
| **Implementer (实现者)** | 代码实现、模块开发、集成测试 | 完整代码、构建脚本、部署指南 |
| **Tester (测试者)** | 测试计划、质量验证、问题反馈 | 测试报告、Bug 列表、优化建议 |

### 工作流程

```
项目需求
    ↓
[任务分解] → 创建 Todo 列表
    ↓
┌─────────────────────────────────────┐
│  并行执行阶段                         │
│  ├─ Analyst → 需求分析               │
│  ├─ Researcher → 技术调研            │
│  └─ Architect → 架构设计             │
└─────────────────────────────────────┘
    ↓
[需求整合] → 整合分析/调研/架构结果
    ↓
[代码实现] → Implementer 编写代码
    ↓
[测试验证] → Tester 测试和反馈
    ↓
✅ 项目完成
```

## 快速开始

### 方式一：使用生成脚本（推荐）

```bash
# 生成多 Agent 项目模板
python ~/.hermes/skills/autonomous-ai-agents/multi-agent-project-builder/scripts/generate-project.py my-awesome-project

# 进入项目目录
cd my-awesome-project

# 查看生成的配置
cat PROJECT_CONFIG.yaml

# 开始执行（需要在 Hermes 中运行）
# 参考 EXECUTION_GUIDE.md
```

### 方式二：手动使用 Skill

1. **加载 Skill**
   ```
   /skills autonomous-ai-agents/multi-agent-project-builder
   ```

2. **定义项目目标**
   ```
   我要创建一个 [项目类型]，主要功能包括 [功能列表]
   ```

3. **启动多 Agent 协作**
   Skill 会自动：
   - 创建 Todo 列表
   - 委托任务给各个专业 Agent
   - 整合结果
   - 生成最终产出

## 项目结构

生成的项目包含：

```
my-project/
├── PROJECT_CONFIG.yaml      # 项目配置文件
├── EXECUTION_GUIDE.md       # 执行指南
├── outputs/                  # 输出目录
│   ├── 01-requirements/     # 需求分析结果
│   ├── 02-research/         # 技术调研结果
│   ├── 03-architecture/     # 架构设计结果
│   ├── 04-implementation/   # 代码实现
│   └── 05-testing/          # 测试报告
└── templates/                # 模板文件（可选）
```

## 自定义配置

### PROJECT_CONFIG.yaml 示例

```yaml
project:
  name: "AI 聊天机器人"
  type: "web-app"
  description: "一个基于 LLM 的智能对话机器人"

agents:
  - name: analyst
    enabled: true
    goal: "分析用户需求，制定功能规划"
  - name: researcher
    enabled: true
    goal: "调研 LLM 集成方案，对比不同框架"
  - name: architect
    enabled: true
    goal: "设计系统架构和 API 接口"
  - name: implementer
    enabled: true
    goal: "实现完整的聊天机器人代码"
  - name: tester
    enabled: true
    goal: "测试功能完整性和用户体验"

workflow:
  parallel_phases:
    - ["analyst", "researcher", "architect"]
  sequential_phases:
    - ["implementer"]
    - ["tester"]

outputs:
  format: "markdown"
  directory: "./outputs"
```

## 使用示例

### 示例 1：创建一个 Todo 应用

```
项目目标：创建一个现代化的 Todo 任务管理应用

功能需求：
- 用户可以添加、编辑、删除任务
- 任务可以标记完成/未完成
- 支持任务分类和标签
- 响应式设计，支持移动端

技术偏好：
- 前端：React + TypeScript
- 后端：Node.js + Express
- 数据库：SQLite
```

Skill 会自动：
1. Analyst 输出详细需求文档
2. Researcher 调研最佳实践
3. Architect 设计系统架构
4. Implementer 编写完整代码
5. Tester 提供测试报告

### 示例 2：创建一个数据分析工具

```
项目目标：创建一个 CSV 数据分析和可视化工具

功能需求：
- 上传 CSV 文件
- 自动数据清洗和预处理
- 生成统计摘要
- 可视化图表（折线图、柱状图、饼图）
- 导出报告

技术偏好：
- Python + Streamlit
- Pandas 数据处理
- Matplotlib/Plotly 可视化
```

## 高级用法

### 自定义 Agent 提示词

在 `PROJECT_CONFIG.yaml` 中为每个 Agent 自定义提示词：

```yaml
agents:
  - name: analyst
    custom_prompt: |
      你是一位专业的产品经理，擅长从用户角度思考问题。
      请特别关注：
      1. 用户体验设计
      2. 功能优先级排序
      3. 商业化可能性
```

### 跳过某些阶段

```yaml
agents:
  - name: researcher
    enabled: false  # 跳过技术调研
```

### 添加自定义 Agent

```yaml
agents:
  - name: designer
    enabled: true
    goal: "UI/UX 设计"
    custom_prompt: "你是一位专业的 UI/UX 设计师..."
```

## 技术栈

- **核心框架**：Hermes Agent + delegate_task
- **任务管理**：Todo 工具
- **输出格式**：Markdown / JSON
- **模板引擎**：Jinja2（可选）
- **支持平台**：OpenClaw、Hermes、Claude

## 相关资源

- [multi-agent-coordination](../multi-agent-coordination/) - 多 Agent 协调基础
- [Hermes Agent 文档](https://github.com/your-repo/hermes-agent)

## 许可证

MIT License - 可自由使用和修改。
