---
name: mia
description: MIA (Memory-Intelligent Assistant) - 智能记忆助手系统，通过记忆、规划、反馈三模块让OpenClaw具备经验学习能力
homepage: https://github.com/yourname/mia
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["node"],"env":["MIA_PLANNER_MODE","MIA_PLANNER_API_KEY","MIA_PLANNER_URL","MIA_PLANNER_MODEL","MIA_MEMORY_FILE","MIA_SIMILARITY_THRESHOLD","MIA_FEEDBACK_FILE"]},"primaryEnv":"MIA_PLANNER_API_KEY"}}
---

# MIA - Memory-Intelligent Assistant

MIA 是一个智能记忆助手系统，让 OpenClaw 具备"经验学习"能力 —— 不是每次遇到问题都从零开始，而是能记住过去如何解决类似问题，并在未来复用这些经验。

## 🎯 核心特性

- **通用结构匹配** —— 不依赖具体实体，识别问题的抽象模式
- **优胜劣汰** —— 只保留最高效的解决轨迹
- **无硬编码** —— 所有配置通过环境变量传入

## 🏗️ 架构组成

MIA 由三个核心模块组成：

| 模块 | 功能 | 路径 |
|-----|------|------|
| **Memory** | 智能记忆存储与检索，支持优胜劣汰 | `memory/` |
| **Planner** | 任务规划与分解，支持参考历史优化 | `planner/` |
| **Feedback** | 执行反馈收集（仅针对全新问题） | `feedback/` |

## 📋 工作流程

```
用户问题
    ↓
[MIA Memory] 检索相似轨迹（基于通用结构）
    ↓
[MIA Planner] 生成执行计划（参考历史或全新生成）
    ↓
[OpenClaw 执行者] 执行搜索、验证、生成答案
    ↓
[MIA Memory] 存储新轨迹（自动优胜劣汰）
    ↓
[MIA Feedback] 收集反馈（仅针对全新问题）
```

## 🚀 安装

```bash
cd /path/to/mia
npm install
```

## ⚙️ 配置

### Planner 配置

| 环境变量 | 必需 | 默认值 | 说明 |
|---------|------|--------|------|
| `MIA_PLANNER_MODE` | 否 | `local` | 运行模式：`local` 或 `api` |
| `MIA_PLANNER_URL` | 否 | - | 自定义API端点 |
| `MIA_PLANNER_MODEL` | 否 | `Qwen3-8B`/`gpt-4` | 模型名称 |
| `MIA_PLANNER_API_KEY` | api模式必需 | - | API密钥 |

**本地部署示例：**
```bash
export MIA_PLANNER_MODE=local
export MIA_PLANNER_URL=http://localhost:8000/v1/chat/completions
export MIA_PLANNER_MODEL=Qwen3-8B
```

**OpenAI API 示例：**
```bash
export MIA_PLANNER_MODE=api
export MIA_PLANNER_API_KEY=sk-xxx
export MIA_PLANNER_MODEL=gpt-4
```

**阿里云 DashScope 示例：**
```bash
export MIA_PLANNER_MODE=api
export MIA_PLANNER_API_KEY=sk-xxx
export MIA_PLANNER_URL=https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
export MIA_PLANNER_MODEL=qwen3-8b
```

### Memory 配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `MIA_MEMORY_FILE` | `./memory/memory.jsonl` | 记忆文件路径 |
| `MIA_SIMILARITY_THRESHOLD` | `0.90` | 相似度阈值 |

### Feedback 配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `MIA_FEEDBACK_FILE` | `./feedback/feedback.jsonl` | 反馈文件路径 |

## 📖 使用方式

### Memory 模块

```bash
# 查找最相似的记忆
node memory/mia-memory.mjs search "你的问题"

# 存储新轨迹（自动优胜劣汰）
node memory/mia-memory.mjs store '{"question": "...", "plan": "...", "execution": [...]}'

# 列出记忆
node memory/mia-memory.mjs list [数量]
```

**输出示例：**
```json
{
  "found": true,
  "similarity": 0.93,
  "record": { ... }
}
```

### Planner 模块

```bash
# 生成 Plan（本地模式）
node planner/mia-planner.mjs "你的问题"

# 参考历史轨迹生成优化 Plan
node planner/mia-planner.mjs "你的问题" --reference "历史Plan文本"
```

**输出示例：**
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

### Feedback 模块

```bash
# 存储反馈
node feedback/mia-feedback.mjs store "问题" "答案" "good"

# 列出反馈
node feedback/mia-feedback.mjs list [数量]
```

## 🔍 相似度计算原理

MIA Memory 提取以下通用结构特征（不依赖具体实体）：

| 特征 | 识别模式 | 说明 |
|------|---------|------|
| TIME_REF | 那年、当年、时候、举办 | 时间参照 |
| DUAL_ENTITY_COMPARE | A和B、A比B、谁更 | 双实体比较 |
| ATTRIBUTE_CONFIRM | 是不是、是否、都是 | 属性确认 |
| NUMERIC_QUERY | 多少、几、多大 | 数值查询 |
| RELATIONSHIP_QUERY | 关系、关联、联系 | 关系查询 |
| RANKING_QUERY | 第一、第二、冠军 | 排名查询 |

**相似度权重：**
- 结构特征相似度：50%
- 模板相似度：30%
- 语义相似度：20%

## 📊 效率评估

MIA Memory 的优胜劣汰机制基于以下指标：

| 指标 | 权重 | 说明 |
|------|------|------|
| search_count | 40% | 搜索次数 |
| step_count | 30% | 执行步骤数 |
| success | 30% | 是否成功 |

新轨迹效率分数 > 旧轨迹 → 替换  
新轨迹效率分数 ≤ 旧轨迹 → 丢弃

## 📝 注意事项

- **Planner 不执行搜索** —— 只生成 Plan，由调用者执行
- **Memory 严格优胜劣汰** —— 只保留最高效轨迹
- **Feedback 智能判断** —— 仅对全新问题收集反馈，避免打扰用户
- **所有配置通过环境变量** —— 无硬编码，灵活部署

## 📄 许可证

ISC
