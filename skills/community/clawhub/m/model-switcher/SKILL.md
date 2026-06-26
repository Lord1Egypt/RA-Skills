---
name: model-switcher
description: Automatically switch between fast (haiku) and powerful (sonnet) models based on task complexity. Triggers when detecting complex tasks like analysis, refactoring, architecture design, optimization, or when user explicitly mentions model switching needs.
---

# Model Switcher

Automatically detect task complexity and switch to the appropriate model.

## Model Configuration

Based on your setup:
- **Fast model (haiku):** `custom-kiro-cli-vipdump-eu-org/claude-haiku-4-5` - For simple, quick tasks
- **Powerful model (sonnet):** `custom-kiro-cli-vipdump-eu-org/claude-sonnet-4-5` - For complex analysis

## Trigger Keywords (Chinese)

Switch to **sonnet** when message contains:
- 分析、深入分析、详细分析
- 重构、代码重构
- 架构、系统架构、设计架构
- 设计、系统设计
- 优化、性能优化
- 复杂、复杂问题
- 调试、深度调试
- 评估、技术评估

## Workflow

1. **Check current model** using `session_status`
2. **Detect keywords** in user message
3. **Switch if needed:**
   - Complex task detected + currently on haiku → switch to sonnet
   - Simple task + currently on sonnet → optionally switch back to haiku
4. **Inform user** briefly about the switch

## Implementation

Use `session_status` tool with `model` parameter:

```javascript
// Switch to sonnet for complex tasks
session_status({ model: "kiro-cli" })

// Switch back to haiku for simple tasks
session_status({ model: "haiku" })

// Reset to default
session_status({ model: "default" })
```

## Example Detection Logic

```
User message: "帮我分析一下这个系统的架构"
→ Contains: "分析", "架构"
→ Action: Switch to sonnet if not already on it
→ Response: "🔄 切换到 sonnet 模型来处理这个复杂任务..."
```

## Notes

- Be smart about switching - don't switch for every message
- Batch related complex tasks on sonnet before switching back
- Inform user only on actual switches, not when already on correct model
- Consider context: if already discussing complex topic, stay on sonnet
