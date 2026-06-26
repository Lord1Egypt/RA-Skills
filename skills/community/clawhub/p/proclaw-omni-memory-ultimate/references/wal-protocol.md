# WAL Protocol - 写前日志协议规范

## 概述

WAL (Write-Ahead Log) 协议是Omni-Memory系统的核心保护机制，确保关键信息在压缩、崩溃、重启后依然存活。

## 核心原则

**先写后响应 (Write BEFORE Responding)**

```
用户输入 → 写入SESSION-STATE.md → 存储向量 → 返回响应
         ↑ 关键步骤，不可跳过
```

## 为何需要WAL

### 问题场景

1. **上下文压缩 (Compaction)**
   - 当上下文超过阈值时，系统会压缩历史对话
   - 未持久化的重要信息可能被清除

2. **系统崩溃**
   - 模型推理过程中断
   - 内存中的上下文丢失

3. **会话切换**
   - 用户切换到其他任务
   - 当前上下文被新话题覆盖

### WAL解决方案

通过在响应前先写入持久化存储，确保：
- 重要信息永久保存
- 压缩后可从SESSION-STATE.md恢复
- 崩溃后可从向量库召回

## 触发条件

| 触发条件 | 必需动作 | 存储位置 |
|----------|----------|----------|
| 用户表达偏好 | 先写 → 再回复 | SESSION-STATE.md + 向量(user类型) |
| 用户做决策 | 先写 → 再回复 | SESSION-STATE.md + 向量(project类型) |
| 用户纠正 | 先写 → 再回复 | SESSION-STATE.md + 向量(feedback类型) |
| 用户给期限 | 先写 → 再回复 | SESSION-STATE.md |
| 用户给具体细节 | 先写 → 再回复 | SESSION-STATE.md |

## 执行流程

### 标准流程

```python
def handle_user_input(user_input):
    # Step 1: 分析输入是否包含关键信息
    if contains_critical_info(user_input):
        # Step 2: 写入SESSION-STATE.md（WAL核心）
        write_to_session_state(user_input)
        
        # Step 3: 分类并存储到向量
        memory_type = classify_memory(user_input)
        store_to_vector(user_input, memory_type)
        
    # Step 4: 生成并返回响应
    return generate_response(user_input)
```

### 具体示例

```
用户: "我喜欢深色模式，不要用浅色"

Agent内部流程:
1. [WAL] 检测到偏好表达
2. [WAL] 写入SESSION-STATE.md:
   - Key Context > User preference: 深色模式
3. [WAL] 存储到向量:
   - type: user
   - content: "用户偏好深色模式，不喜欢浅色"
   - importance: 0.9
4. [响应] "好的，我会使用深色主题..."
```

## SESSION-STATE.md 写入模板

```markdown
# SESSION-STATE.md — 活跃工作记忆

## Current Task
[当前任务描述，如果用户指定]

## Key Context
- User preference: [用户明确表达的偏好]
- Decision made: [最近的重要决策]
- Blocker: [当前障碍，如果有]

## Pending Actions
- [ ] [待办事项]

## Recent Decisions
- [决策]: [原因]

---
*Last updated: YYYY-MM-DD HH:MM*
```

## 写入时机判断

### 必须写入

- 用户说"我喜欢/不喜欢..."
- 用户说"我们用...吧"
- 用户说"不对，应该是..."
- 用户说"记住..."
- 用户纠正Agent的回答
- 用户确认某个方案
- 用户给出具体参数/配置

### 可以跳过

- 简单的问答（如"今天天气"）
- 闲聊内容
- 明确的临时性请求
- 信息查询类请求

## 错误处理

### 写入失败

```python
def handle_write_failure():
    # 1. 记录错误日志
    log_error("WAL write failed")
    
    # 2. 尝试备用存储
    try_backup_storage()
    
    # 3. 仍要响应用户，但提醒风险
    return "好的，但可能需要您再确认一次..."
```

### 恢复流程

```python
def recover_from_session_state():
    # 1. 会话开始时读取SESSION-STATE.md
    context = read_session_state()
    
    # 2. 加载到当前上下文
    load_context(context)
    
    # 3. 向量召回相关记忆
    relevant_memories = vector_recall(context.keywords)
    
    # 4. 合并上下文
    full_context = merge(context, relevant_memories)
```

## 最佳实践

### 1. 及时更新

```markdown
<!-- 每次关键交互后更新时间戳 -->
---
*Last updated: 2026-04-06 14:35*
```

### 2. 精简记录

```markdown
<!-- Good: 精简有效 -->
- User preference: 深色模式

<!-- Bad: 冗余无效 -->
- User preference: 用户说他喜欢深色模式，不喜欢浅色模式，之前用过浅色觉得眼睛不舒服
```

### 3. 结构化存储

```markdown
<!-- Good: 结构化 -->
## Recent Decisions
- 采用React: 用户熟悉React生态

<!-- Bad: 非结构化 -->
## Recent Decisions
用户说用React，因为之前用过Vue觉得不好，所以决定用React了
```

## 性能考量

### 写入开销

| 操作 | 耗时 | 影响 |
|------|------|------|
| 写入SESSION-STATE.md | ~10ms | 可忽略 |
| 向量存储 | ~50-100ms | 轻微延迟 |
| 总体开销 | <150ms | 用户无感知 |

### 优化策略

1. **异步存储**: 向量存储可异步执行
2. **批量写入**: 多条信息合并写入
3. **缓存机制**: 频繁读取的SESSION-STATE.md缓存

## 与其他机制配合

### 与向量检索配合

```
WAL写入 → 向量存储 → 后续检索时召回
```

### 与Dream整合配合

```
SESSION-STATE.md → Daily Log → Dream整合 → Long-term Memory
```

### 与流体衰减配合

```
向量存储 → 流体衰减 → 低分遗忘 → 高分保留
```

---

*WAL Protocol Version: 1.0*
*Essential for: Context persistence, Crash recovery, Cross-session memory*
