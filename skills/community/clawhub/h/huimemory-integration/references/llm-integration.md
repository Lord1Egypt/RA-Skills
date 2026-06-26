# LLM 集成深度指南

## 核心设计哲学

**检索系统 = 搜索引擎，LLM = 决策者**

HuiMemory 的定位非常明确：它只负责高效地"捞"数据，所有的语义理解、意图推断、答案组织都交给 LLM 完成。

## 集成模式

### 模式 1：工具调用（推荐）

将 HuiMemory 封装为 LLM 的工具（Tool），让 LLM 主动调用。

**优势**：
- LLM 自主决定何时检索
- 支持多轮检索和追问
- 灵活性高

**示例**：

```python
from openai import OpenAI
from huimemory import Retriever
from huimemory.embedding import BGEEmbedding

# 初始化
retriever = Retriever(
    embedding=BGEEmbedding(model_path="models/bge-small-zh-v1.5"),
    config_path="configs/config.yaml"
)

# 工具定义
tools = [
    {
        "type": "function",
        "function": {
            "name": "recall_memory",
            "description": "检索历史对话记忆。支持关键词搜索、时间过滤、分段扫描。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词或问题"
                    },
                    "filter_expr": {
                        "type": "string",
                        "description": "时间过滤表达式，如 \"timestamp >= '2026-04-06'\""
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "返回结果数量，默认 5",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recall_by_id",
            "description": "根据轮次 ID 检索特定对话。用于导航到相邻轮次。",
            "parameters": {
                "type": "object",
                "properties": {
                    "turn_id": {
                        "type": "string",
                        "description": "轮次 ID，如 'a3f2c7'"
                    }
                },
                "required": ["turn_id"]
            }
        }
    }
]

# 工具实现
def recall_memory(query, filter_expr=None, top_k=5):
    results = retriever.search(
        query=query,
        top_k=top_k,
        filter_expr=filter_expr,
        enable_progressive_scan=True
    )
    return retriever.format_search_results(results)

def recall_by_id(turn_id):
    # 根据 turn_id 查询 metadata
    # 实现略
    pass

# LLM 调用
client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "我之前问过什么关于 AI 意识的问题？"}
    ],
    tools=tools,
    tool_choice="auto"
)

# 处理工具调用
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        if tool_call.function.name == "recall_memory":
            args = json.loads(tool_call.function.arguments)
            result = recall_memory(**args)
            # 将结果返回给 LLM
```

### 模式 2：RAG（检索增强生成）

在用户提问前，先检索相关记忆，作为上下文注入。

**优势**：
- 实现简单
- 适合单轮问答

**示例**：

```python
def chat_with_memory(user_input: str) -> str:
    # 1. 检索相关记忆
    results = retriever.search(
        query=user_input,
        top_k=5,
        enable_progressive_scan=True
    )
    
    # 2. 构建上下文
    context = retriever.format_search_results(results)
    
    # 3. 调用 LLM
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": f"你是一个拥有长期记忆的 AI 助手。\n\n历史对话：\n{context}"
            },
            {"role": "user", "content": user_input}
        ]
    )
    
    return response.choices[0].message.content
```

---

## System Prompt 设计

### 核心原则

1. **明确职责边界**：检索系统只负责"捞"，LLM 负责"判断"
2. **提供工具说明**：清晰描述工具的能力和限制
3. **给出示例**：展示典型场景的工具调用方式

### 推荐模板

```markdown
你是一个拥有长期记忆的 AI 助手。你可以通过 `recall_memory` 工具检索历史对话。

## 记忆检索规则

### 1. 关键词检索

当用户提到具体内容时，使用关键词搜索。

**示例**：
- 用户："我之前问过什么关于 AI 意识的问题？"
- 调用：`recall_memory(query="AI 意识", top_k=5)`

### 2. 时间过滤

当用户提到时间范围时，使用时间过滤。

**支持的时间表达式**：
- `timestamp >= '2026-04-06'`：2026-04-06 之后
- `timestamp <= '2026-04-13'`：2026-04-13 之前
- `timestamp >= '2026-04-06' AND timestamp <= '2026-04-13'`：时间范围

**示例**：
- 用户："上周我们讨论了什么？"
- 调用：`recall_memory(query="", filter_expr="timestamp >= '2026-04-06' AND timestamp <= '2026-04-13'")`

### 3. 分段扫描

当时间模糊时，系统会自动分段扫描。

**示例**：
- 用户："前段时间我们聊过什么项目？"
- 调用：`recall_memory(query="项目", top_k=5)`（系统自动启用分段扫描）

### 4. 轮次导航

当需要查看上下文时，使用 `recall_by_id`。

**检索结果格式**：
```
[id:a3f2c7 | prev: k7f2a1 | next: d2n7p3 | 相似度: 0.778]
📁 2026-W15/2026-04-13/chat_xxx.md | 话题: 本地模型部署 | 2026-04-13 Mon 10:00:07

<user timestamp="...">...</user>
<assistant timestamp="...">...</assistant>
```

**导航示例**：
- 检索结果：`[id:a3f2c7 | prev: k7f2a1 | next: d2n7p3]`
- 查看上一轮：`recall_by_id(turn_id="k7f2a1")`
- 查看下一轮：`recall_by_id(turn_id="d2n7p3")`

## 检索策略

### 何时检索？

1. **用户明确提问历史**："我之前问过..."
2. **用户提到具体内容**："那个项目..."
3. **用户提到时间**："上周"、"上个月"

### 何时追问？

1. **检索结果不明确**：多个相似结果，需要用户确认
2. **时间范围模糊**：用户说"前段时间"，但检索结果过多
3. **上下文不足**：需要查看相邻轮次

### 如何组织答案？

1. **基于检索结果**：不要编造，只基于检索到的内容
2. **标注来源**：说明信息来自哪个对话文件
3. **提供导航**：如果用户想看更多，提供 prev/next ID

## 注意事项

1. **不要过度检索**：一次检索 top_k=5 通常足够
2. **不要忽略时间过滤**：时间信息能显著提升检索精度
3. **不要编造记忆**：如果检索不到，直接说"我没有找到相关记忆"
```

---

## 工具 Schema

### recall_memory

```json
{
    "name": "recall_memory",
    "description": "检索历史对话记忆。支持关键词搜索、时间过滤、分段扫描。",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索关键词或问题"
            },
            "filter_expr": {
                "type": "string",
                "description": "时间过滤表达式，如 \"timestamp >= '2026-04-06'\""
            },
            "top_k": {
                "type": "integer",
                "description": "返回结果数量，默认 5",
                "default": 5
            }
        },
        "required": ["query"]
    }
}
```

### recall_by_id

```json
{
    "name": "recall_by_id",
    "description": "根据轮次 ID 检索特定对话。用于导航到相邻轮次。",
    "parameters": {
        "type": "object",
        "properties": {
            "turn_id": {
                "type": "string",
                "description": "轮次 ID，如 'a3f2c7'"
            }
        },
        "required": ["turn_id"]
    }
}
```

---

## 高级场景

### 场景 1：多轮检索

用户提问需要多次检索才能回答。

**示例**：

```
用户：我之前问过关于 AI 意识的问题，后来我们又讨论了什么？

LLM 思考：
1. 先检索 "AI 意识" 相关对话
2. 找到对话文件和轮次 ID
3. 使用 recall_by_id 查看后续轮次
```

### 场景 2：时间范围推断

用户提到模糊时间，LLM 需要推断具体范围。

**示例**：

```
用户：上周我们讨论了什么项目？

LLM 推断：
- 当前时间：2026-04-13
- "上周"：2026-04-06 ~ 2026-04-12
- 调用：recall_memory(query="项目", filter_expr="timestamp >= '2026-04-06' AND timestamp <= '2026-04-12'")
```

### 场景 3：上下文扩展

检索结果不够，需要查看相邻轮次。

**示例**：

```
用户：那个项目后来怎么样了？

LLM 思考：
1. 检索 "项目" 相关对话
2. 找到结果：[id:a3f2c7 | next: d2n7p3]
3. 使用 recall_by_id(turn_id="d2n7p3") 查看下一轮
```

---

## 性能优化

### 1. 减少检索次数

- 一次检索 top_k=5 通常足够
- 避免频繁调用 recall_by_id

### 2. 使用时间过滤

- 时间过滤能显著提升检索精度
- 减少无关结果

### 3. 缓存检索结果

- 对相同 query 缓存结果
- 减少重复计算

---

## 常见问题

### Q1: LLM 如何知道当前时间？

**方案 1**：在 System Prompt 中注入当前时间

```python
from datetime import datetime

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
system_prompt = f"""
当前时间：{current_time}

你是一个拥有长期记忆的 AI 助手...
"""
```

**方案 2**：提供 `get_current_time` 工具

### Q2: 如何处理"我记得..."这类表述？

用户说"我记得..."时，通常是确认记忆是否存在，而不是检索。

**处理方式**：

```
用户：我记得上周我们讨论过 AI 意识，对吗？

LLM 思考：
1. 检索 "AI 意识" + 时间过滤
2. 如果找到：确认用户记忆
3. 如果找不到：说明"我没有找到相关记忆"
```

### Q3: 如何避免编造记忆？

**核心原则**：只基于检索结果回答，不要编造

**System Prompt 提示**：

```markdown
## 注意事项

- 如果检索不到相关记忆，直接说"我没有找到相关记忆"
- 不要编造或推测历史对话内容
- 所有信息必须来自检索结果
```

---

**核心原则**：检索系统只负责"捞"，LLM 负责"判断"。保持简单，避免过度设计。
