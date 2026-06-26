# OpenClaw Agent 与 Workflow 编排指南

## 目录
- [核心概念](#核心概念)
- [节点类型详解](#节点类型详解)
- [Workflow 设计模式](#workflow-设计模式)
- [编排最佳实践](#编排最佳实践)
- [模板库](#模板库)

---

## 核心概念

### Agent vs Workflow

| 概念 | 说明 | 适用场景 |
|------|------|---------|
| **Agent** | 具有自主决策能力的智能体 | 开放式任务、复杂推理 |
| **Workflow** | 预定义流程的编排 | 固定流程、重复任务 |

### 节点 (Node)

节点是 Workflow 的基本单元，每个节点执行特定功能。

### 边 (Edge)

边连接节点，定义数据流向和执行顺序。

---

## 节点类型详解

### 1. LLM 节点

```json
{
  "id": "llm_node",
  "type": "llm",
  "config": {
    "model": "gpt-4o",
    "prompt": "{{input.message}}",
    "system_prompt": "你是一个专业助手",
    "parameters": {
      "temperature": 0.7,
      "max_tokens": 4096
    }
  }
}
```

**适用场景：**
- 文本生成
- 对话交互
- 内容分析
- 翻译总结

### 2. Tool 节点

```json
{
  "id": "tool_node",
  "type": "tool",
  "config": {
    "tool": "web_search",
    "input": {"query": "{{input.query}}"},
    "timeout": 30
  }
}
```

**适用场景：**
- 外部 API 调用
- 数据查询
- 文件操作

### 3. Condition 节点

```json
{
  "id": "condition_node",
  "type": "condition",
  "config": {
    "conditions": [
      {
        "expression": "{{score}} >= 80",
        "branch": "pass"
      },
      {
        "expression": "{{score}} >= 60",
        "branch": "retry"
      }
    ],
    "default_branch": "fail"
  }
}
```

**适用场景：**
- 路由分发
- 质量检查
- 异常处理

### 4. Loop 节点

```json
{
  "id": "loop_node",
  "type": "loop",
  "config": {
    "loop_type": "for",
    "items": "{{items}}",
    "max_iterations": 100,
    "body": {"nodes": [], "edges": []}
  }
}
```

**适用场景：**
- 批量处理
- 重试机制
- 递归操作

### 5. Memory 节点

```json
{
  "id": "memory_node",
  "type": "memory",
  "config": {
    "operation": "store",
    "content": "{{output}}",
    "metadata": {"source": "user_input"}
  }
}
```

**适用场景：**
- 记忆存储
- 上下文管理
- 知识积累

### 6. Retrieval 节点

```json
{
  "id": "retrieval_node",
  "type": "retrieval",
  "config": {
    "query": "{{question}}",
    "top_k": 5,
    "score_threshold": 0.7
  }
}
```

**适用场景：**
- RAG 检索
- 知识库问答
- 相似度搜索

---

## Workflow 设计模式

### 1. 顺序执行 (Sequential)

```
[Input] → [Step 1] → [Step 2] → [Step 3] → [Output]
```

**适用：** 简单的多步骤流程

```json
{
  "name": "sequential_workflow",
  "workflow_type": "sequential",
  "nodes": [
    {"id": "input", "type": "input"},
    {"id": "process", "type": "action"},
    {"id": "output", "type": "output"}
  ]
}
```

### 2. 条件分支 (Conditional)

```
        ┌─[Pass]─→ [处理A]
[Input]─┼─[Retry]─→ [处理B]
        └─[Fail]─→ [处理C]
```

**适用：** 决策树、状态机

### 3. 并行执行 (Parallel)

```
           ┌─[Task 1]─┐
[Input]───→┤─[Task 2]─┼──→[Output]
           └─[Task 3]─┘
```

**适用：** 无依赖的任务并行

### 4. 扇出扇入 (Fan-Out Fan-In)

```
[Input] → [分发] → [并行执行] → [聚合] → [Output]
```

**适用：** MapReduce 模式

### 5. 流水线 (Pipeline)

```
[Input] → [Stage 1] → [Stage 2] → [Stage 3] → [Output]
```

**适用：** ETL、数据处理

---

## 编排最佳实践

### 最佳实践 1: 清晰的节点命名

```json
{
  "nodes": [
    {"id": "validate_input", "type": "action"},
    {"id": "query_database", "type": "tool"},
    {"id": "format_response", "type": "action"}
  ]
}
```

### 最佳实践 2: 错误处理

```json
{
  "nodes": [
    {"id": "main_process", "type": "llm"},
    {
      "id": "error_handler",
      "type": "condition",
      "config": {"condition": "{{error}}"}
    }
  ]
}
```

### 最佳实践 3: 超时控制

```json
{
  "config": {
    "timeout": 30,
    "retry": {
      "enabled": true,
      "max_attempts": 3,
      "backoff": "exponential"
    }
  }
}
```

### 最佳实践 4: 记忆管理

```json
{
  "nodes": [
    {"id": "retrieve_memory", "type": "retrieval"},
    {"id": "process", "type": "llm"},
    {"id": "store_memory", "type": "memory"}
  ]
}
```

---

## 模板库

### RAG 模板

```json
{
  "name": "rag_workflow",
  "type": "workflow",
  "nodes": [
    {"id": "input", "type": "input"},
    {"id": "retrieve", "type": "retrieval"},
    {"id": "augment", "type": "action"},
    {"id": "generate", "type": "llm"},
    {"id": "output", "type": "output"}
  ]
}
```

### 客服机器人模板

```json
{
  "name": "customer_service_bot",
  "type": "agent",
  "config": {
    "intents": ["order_query", "refund", "complaint"],
    "tools": ["db_query", "refund_api"],
    "fallback": "transfer_human"
  }
}
```

### 数据处理模板

```json
{
  "name": "data_processing_pipeline",
  "type": "workflow",
  "workflow_type": "pipeline",
  "stages": [
    "extract",
    "transform",
    "validate",
    "load",
    "report"
  ]
}
```

---

## 变量引用

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{input.*}}` | 输入变量 | `{{input.message}}` |
| `{{output.*}}` | 输出变量 | `{{output.result}}` |
| `{{env.*}}` | 环境变量 | `{{env.API_KEY}}` |
| `{{context.*}}` | 上下文变量 | `{{context.user_id}}` |
