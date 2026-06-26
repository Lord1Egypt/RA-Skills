# MIA Planner Skill

## 概述

MIA Planner 是一个智能规划器，负责生成 Search Plan。支持利用历史记忆辅助规划，通过参考历史轨迹生成优化后的新 Plan。

## 核心特性

- **Plan 生成**：将用户问题分解为可执行的中间目标
- **历史参考**：支持参考历史轨迹生成优化 Plan
- **无硬编码**：所有配置通过环境变量传入

## 使用方式

### 命令行调用

```bash
# 本地部署模式（默认）
node mia-planner.mjs "你的问题"

# API调用模式（OpenAI协议兼容）
export MIA_PLANNER_MODE=api
export MIA_PLANNER_API_KEY=sk-xxx
node mia-planner.mjs "你的问题"

# 参考历史轨迹生成 Plan
node mia-planner.mjs "你的问题" --reference "历史Plan文本"
```

### 配置示例

**本地部署（Qwen）：**
```bash
export MIA_PLANNER_MODE=local
export MIA_PLANNER_URL=http://localhost:8000/v1/chat/completions
export MIA_PLANNER_MODEL=Qwen3-8B
```

**OpenAI API：**
```bash
export MIA_PLANNER_MODE=api
export MIA_PLANNER_API_KEY=sk-xxx
export MIA_PLANNER_MODEL=gpt-4
```

**阿里云 DashScope（OpenAI兼容）：**
```bash
export MIA_PLANNER_MODE=api
export MIA_PLANNER_API_KEY=sk-xxx
export MIA_PLANNER_URL=https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
export MIA_PLANNER_MODEL=qwen3-8b
```

### 环境变量

| 变量 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `MIA_PLANNER_MODE` | 否 | `local` | 运行模式：`local`（本地部署）或 `api`（OpenAI协议） |
| `MIA_PLANNER_URL` | 否 | 见下方 | 自定义API端点（完整URL，包含路径） |
| `MIA_PLANNER_MODEL` | 否 | 见下方 | 模型名称 |
| `MIA_PLANNER_API_KEY` | api模式必需 | - | API密钥（Bearer认证） |

**默认配置：**
- local模式：`http://localhost:8000/v1/chat/completions`
- api模式：`https://api.openai.com/v1/chat/completions`

**默认模型：**
- local模式：`Qwen3-8B`
- api模式：`gpt-4`

### 输出格式

```json
{
  "question": "用户问题",
  "plan": "完整的计划文本",
  "steps": ["步骤1", "步骤2", "步骤3"],
  "reference_used": true,
  "model": "使用的模型",
  "timestamp": "2026-03-15T..."
}
```

## 参考历史轨迹的工作流程

当传入历史 Plan 时，Planner 会：
1. 分析历史 Plan 的结构和策略
2. 结合当前问题的特点
3. 生成优化后的新 Plan

## 架构位置

```
用户问题
    ↓
[MIA Memory] 检索相似轨迹（基于通用结构）
    ↓
[MIA Planner] ← 本 Skill
    ├─ 配置读取 (MODE/apiKey/URL/MODEL)
    ├─ 有相似轨迹 → 参考历史生成优化 Plan
    └─ 无相似轨迹 → 全新生成 Plan
    ↓
[OpenClaw 执行者]
    ↓
执行搜索、验证、生成答案
```

## 运行模式

### local 模式（默认）
- 连接到本地部署的大模型服务
- 无需 API Key
- 默认端点：`http://localhost:8000/v1/chat/completions`
- 默认模型：`Qwen3-8B`

### api 模式
- 连接到 OpenAI 协议兼容的 API 服务
- 需要 `MIA_PLANNER_API_KEY`
- 支持：OpenAI、阿里云 DashScope、Azure 等
- 默认端点：`https://api.openai.com/v1/chat/completions`
- 默认模型：`gpt-4`

## Prompt 模板

### 基础 Prompt
```
你是一名规划助手，为OpenClaw提供战略指导。

任务：分析问题，建议清晰的工作计划。

要求：
1. 表述清晰简洁（≤300字）
2. 每步独立可执行
3. 不直接给答案，只给方案
4. 不包含事实性信息

问题：{问题}
```

### 参考历史 Prompt
```
你是一名规划助手。之前解决过类似问题：

[历史方案]
{历史Plan}

请基于参考，为当前问题生成优化后的 Plan：
1. 借鉴历史方案的结构
2. 根据当前问题调整
3. 生成更高效的 Plan

当前问题：{问题}
```

## 注意事项

- 本 Skill **不执行任何搜索**
- 只生成 Plan，由调用者执行
- 所有配置通过环境变量传入，无硬编码
- 支持参考历史轨迹，但不会直接照抄答案
