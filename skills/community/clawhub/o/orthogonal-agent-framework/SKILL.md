---
name: orthogonal-agent-framework
description: 正交性Agent框架 - 模块化AI Agent设计系统。将Agent能力拆分为规划、执行、记忆、评估四个正交维度，实现可组合、可替换、可测试、可扩展的Agent架构。
metadata:
  openclaw:
    emoji: "🧩"
    requires:
      env: []
      bins: ["bash"]
user-invocable: true
---

# 🧩 Orthogonal Agent Framework

> 正交性Agent框架 - 模块化AI Agent设计系统

基于Manus核心设计理念，将AI Agent拆分为四个正交维度：
- **规划（Planning）** - 任务拆解、目标设定
- **执行（Execution）** - 工具调用、操作执行
- **记忆（Memory）** - 上下文保持、长期存储
- **评估（Evaluation）** - 结果检验、反馈改进

## 核心理念

### 什么是正交性？

正交性（Orthogonality）指各模块**相互独立**，改变一个不影响另一个。

```
┌─────────────────────────────────────────────────┐
│                  Agent System                     │
├─────────────┬─────────────┬─────────────┬────────┤
│  Planning   │ Execution   │   Memory    │   Eval │
│    模块      │    模块      │    模块      │   模块  │
└─────────────┴─────────────┴─────────────┴────────┘
       ↕            ↕            ↕            ↕
   可独立       可独立       可独立       可独立
   升级/       替换/       替换/       替换/
   测试        测试        测试        测试
```

### 优势

| 优势 | 说明 |
|------|------|
| 🔧 可组合 | 每个维度可独立升级 |
| 🔄 可替换 | 随时换掉某个模块 |
| 🧪 可测试 | 单独测试每个维度 |
| 📈 可扩展 | 新能力只需加新模块 |

## 使用方法

### 快速开始

```
使用正交性框架帮我规划一个复杂任务
```

### 框架文件

框架会自动创建以下文件管理任务：

| 文件 | 作用 |
|------|------|
| `plan.md` | 任务规划和拆解 |
| `execution.md` | 执行记录和步骤 |
| `memory.md` | 上下文和记忆 |
| `evaluation.md` | 结果评估和反馈 |

### 命令示例

| 命令 | 作用 |
|------|------|
| `正交性框架：规划 [任务]` | 拆解任务为步骤 |
| `正交性框架：执行 [步骤]` | 执行具体操作 |
| `正交性框架：记忆 [内容]` | 存储重要信息 |
| `正交性框架：评估 [结果]` | 检验并反馈 |
| `正交性框架：状态` | 查看当前各模块状态 |

## 适用场景

### ✅ 适合

- 复杂多步骤任务
- 需要长期记忆的任务
- 需要评估/反思的任务
- 构建自定义Agent系统

### ❌ 不适合

- 简单对话任务
- 一次性任务
- 固定流程

## 技术实现

### 模块接口

每个正交模块遵循统一接口：

```yaml
Planning:
  - plan(task) → steps[]
  - update_plan(progress)
  - replan(feedback)

Execution:
  - execute(step) → result
  - tool_call(tool, args)
  - rollback(step)

Memory:
  - store(key, value)
  - retrieve(key)
  - forget(key)
  - summarize()

Evaluation:
  - evaluate(result) → score
  - feedback(issues) → improvements
  - validate(criteria)
```

### 状态管理

```yaml
# agent-state.yaml
planning:
  current_task: "..."
  steps: [...]
  completed: [...]

execution:
  active_step: 1
  results: {...}

memory:
  short_term: [...]
  long_term: {...}

evaluation:
  scores: {...}
  feedback: [...]
```

## 扩展性

### 添加新模块

在框架中集成新能力：

```yaml
modules:
  - planning     # 已有
  - execution    # 已有
  - memory       # 已有
  - evaluation   # 已有
  - creativity   # 新增 - 创意生成
  - research     # 新增 - 信息收集
```

### 替换模块

替换现有模块不影响其他：

```yaml
# 替换记忆模块
memory:
  type: "vector_store"  # 从文件切换到向量数据库
  config: {...}
```

## 示例

### 完整任务流程

```
用户: 帮我研究AI Agent的发展趋势

正交性框架:
1. Planning → 拆解为5个子任务
2. Execution → 搜索信息
3. Memory → 存储重要发现
4. Evaluation → 评估信息质量
5. 循环2-4直到完成
6. 输出最终报告
```

## 文件结构

```
orthogonal-agent-framework/
├── SKILL.md
├── _meta.json
├── references/
│   ├── design-principles.md
│   └── module-interfaces.md
└── templates/
    ├── plan.md
    ├── execution.md
    ├── memory.md
    └── evaluation.md
```

---

*基于Manus正交性设计理念构建*
