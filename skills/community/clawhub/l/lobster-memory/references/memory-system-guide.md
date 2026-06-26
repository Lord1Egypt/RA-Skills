# 龙虾记忆系统指南

## 核心概念

### 1. 记忆层级

```
MEMORY.md          ← 长期记忆（人工维护）
  ↓
memory/*.md        ← 每日归档（自动）
  ↓
working-buffer.md  ← 工作缓冲区（自动清理）
```

### 2. 触发条件

| 条件 | 动作 |
|------|------|
| Context > 60% | 进入 Working Buffer 协议 |
| Context > 90% | 强制归档 |
| 用户问及往事 | memory_search → memory_get |
| 每日定时 | 自动归档 + 学习日志 |

### 3. 文件作用

**MEMORY.md**
- 人工维护的核心记忆
- 用户关键信息、决策、偏好
- 项目状态、技术栈

**memory/YYYY-MM-DD.md**
- 每日自动归档
- 对话摘要、关键进展
- 便于追溯历史

**working-buffer.md**
- 危险区记录
- Context 超限时的临时存储
- 定期清理

**SESSION-STATE.md**
- 当前会话状态
- 活跃项目、待办事项
- 快速恢复上下文

**HEARTBEAT.md**
- 自检清单
- 定期执行的记忆维护
- 主动行为建议

## 工作流程

### 日常流程

```
1. 对话开始 → 加载 MEMORY.md + SESSION-STATE.md
2. 对话中 → 如有重要信息，记入 working-buffer
3. Context > 60% → 归档到 memory/YYYY-MM-DD.md
4. 每日 2:00 AM → 自动归档清理
5. 每日 10:00 AM → 自主学习 + 汇报
```

### 查询流程

```
1. memory_search(query) → 找相关文件
2. memory_get(path, from, lines) → 拉取内容
3. 回答 + Source: path#line
```

## 最佳实践

1. **定期归档**：不要让 working-buffer 堆积
2. **精简 MEMORY.md**：只保留核心信息
3. **引用来源**：回答时注明记忆来源
4. **主动清理**：Heartbeat 时检查并清理
5. **区分主次**：核心放 MEMORY.md，细节放 memory/

## 故障排除

### Context 100% 怎么办？

1. 立即停止加载新记忆
2. 进入 Working Buffer 协议
3. 归档到 memory/YYYY-MM-DD.md
4. 清空 working-buffer.md
5. 更新 SESSION-STATE.md

### 找不到记忆？

1. 检查 memory_search 关键词
2. 尝试不同的搜索词
3. 手动检查 memory/ 目录
4. 如果是重要信息，补充到 MEMORY.md
