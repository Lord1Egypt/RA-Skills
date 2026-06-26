---
name: memos-recall
description: Recall memories from MemOS Cloud before responding. Use this skill when you need context about user's previous conversations, preferences, or decisions.
triggers:
  - user asks about previous conversations
  - user mentions "before", "last time", "previously"
  - need user preferences or context
  - user asks "what did I say"
version: 1.0.0
---

# MemOS 记忆召回

在回答前从 MemOS Cloud 召回相关记忆。

## 使用方式

当需要上下文时，执行以下命令：

```bash
node ~/.claude/plugins/memos-cloud/memos-api.js search "{user_query}"
```

## 参数
- `user_query` - 用户的输入或提炼的搜索关键词

## 处理结果

### 成功返回记忆
将记忆整合到回复中：
```
根据之前的记录，{memory_content}
```

### 无相关记忆
正常回复，不提及记忆功能。

### API 错误
静默失败，正常回复。

## 示例场景

**用户**: "我之前说的那个项目怎么样了？"
**动作**:
```bash
node ~/.claude/plugins/memos-cloud/memos-api.js search "之前说的那个项目"
```
**回复**: "根据之前的记录，你提到的项目是 X，当时..."

---

**用户**: "我还是喜欢之前那个方案"
**动作**:
```bash
node ~/.claude/plugins/memos-cloud/memos-api.js search "方案偏好"
```
**回复**: "根据记录，你之前倾向于..."
