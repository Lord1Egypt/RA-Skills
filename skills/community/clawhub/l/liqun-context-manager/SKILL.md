---
name: context-manager
description: 管理对话上下文和记忆提取。根据关键词高效检索历史记忆。
---

# Context Manager Skill

## 功能
- 搜索记忆文件
- 提取相关上下文
- 管理会话状态

## 使用方法
```python
from context_manager import search_memory, get_recent

# 搜索记忆
results = search_memory('关键词')

# 获取最近记忆
recent = get_recent(5)
```
