# SKILL.md - Context Optimizer

> OpenClaw运行时优化系统 — 系级级安装，所有Agent统一受益

## 类型

**Runtime Optimizer（运行时优化）**

- 🎯 受众：OpenClaw系统管理员
- 📦 安装方式：系统级安装（不是Agent级）
- 🔄 生效方式：OpenClaw运行时自动调用，Agent无需感知

## 工作原理

```
Agent A ←┐
Agent B ←┼── OpenClaw运行时（统一优化） ← context-optimizer
Agent C ←┘
```

所有Agent间接受益，但不需要单独配置。

## 功能

### 1. 微压缩 (microcompact)
- 检测重复消息（相似度>85%）
- 合并连续的工具调用结果
- 压缩长文本（保留首尾关键信息）
- **效果**：节省60%+重复token
- **谁在用**：运行时自动
- **Agent感知**：❌ 不感知

### 2. 自动压缩 (autocompact)
- 监控token使用量
- 超过阈值时自动触发压缩
- 生成对话摘要+保留关键文件
- **效果**：长对话节省50%+token
- **谁在用**：运行时自动
- **Agent感知**：❌ 不感知

### 3. 流式并行执行 (streaming_executor)
- 流式检测工具调用
- 并行执行多个工具
- 错误隔离+自动重试
- **效果**：工具执行加速3x
- **谁在用**：运行时自动
- **Agent感知**：❌ 不感知

### 4. Token预算管理 (token_budget)
- Token使用追踪（累计/本次/剩余）
- 三级阈值预警（75%警告/85%压缩/90%危险）
- 预算耗尽自动续期（最多5次）
- **效果**：防止上下文溢出，智能预算管理
- **谁在用**：心跳监控
- **Agent感知**：🟡 告警时感知

### 5. 工具延迟加载 (tool_defer)
- 初始prompt仅加载~10个核心工具
- 40+工具按需搜索加载
- 多维度搜索评分
- **效果**：节省75%+工具描述token
- **谁在用**：运行时自动
- **Agent感知**：❌ 不感知

## 用法

### 直接调用（Python）

```bash
# 微压缩测试
python3 scripts/microcompact.py --test

# 自动压缩测试
python3 scripts/auto_compactor.py --test

# 流式执行器测试
python3 scripts/streaming_executor.py --test

# Token预算测试
python3 scripts/token_budget.py --test

# 工具延迟加载测试
python3 scripts/tool_defer.py --test

# 处理消息文件
python3 scripts/microcompact.py messages.json
python3 scripts/auto_compactor.py messages.json
python3 scripts/streaming_executor.py tools.json
python3 scripts/token_budget.py status
python3 scripts/tool_defer.py --search "飞书"
```

### 集成到Agent工作流

```python
from scripts.microcompact import MicroCompactor
from scripts.auto_compactor import AutoCompactor
from scripts.streaming_executor import StreamingToolExecutor

# 微压缩
compactor = MicroCompactor()
result = compactor.compact(messages)
print(f"节省 {result.savings_percent:.1f}% token")

# 自动压缩
auto = AutoCompactor(context_window=200_000)
if auto.should_compact(current_tokens):
    result = auto.compact(messages)
    messages = result.messages

# 流式执行
executor = StreamingToolExecutor(max_concurrent=5)
for tool in tool_calls:
    await executor.add_tool(tool)
results = await executor.wait_all()
```

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| similarity_threshold | 0.85 | 消息相似度阈值 |
| min_message_length | 100 | 最小合并长度 |
| context_window | 200_000 | 上下文窗口大小 |
| safety_margin | 0.8 | 压缩触发比例 |
| max_concurrent | 5 | 最大并行工具数 |
| timeout_seconds | 30.0 | 工具执行超时 |

## 依赖

- Python 3.8+
- 标准库（json, asyncio, difflib）
- 无外部依赖

## 许可

MIT License
