# AGENTS.md 注册配置

将以下内容添加到 AGENTS.md:

---

## long_task_manager

| 属性 | 值 |
|------|-----|
| **名称** | 长时间任务管理器 |
| **ID** | `long_task_manager` |
| **运行时** | `subagent` |
| **模式** | `run` / `session` |
| **超时** | 无限制 (session模式) |
| **版本** | v1.0 |
| **位置** | `skills/long-task-manager/` |

**能力列表**:
- 长时间任务提交与调度
- 实时进度追踪与查询
- 任务取消与恢复
- 批量任务管理
- 断点续传支持

**任务类型**:
- 代码生成 (大量API/文件)
- 数据处理 (大数据集)
- 批量文档生成
- 长时间计算任务

**使用场景**:
- Agent执行超时问题
- 需要实时进度显示的任务
- 可取消的长时间任务
- 异步非阻塞执行

**最佳实践**:
```python
# 1. 提交任务
manager = LongTaskManager()
task_id = manager.submit(agent_id, task_config)

# 2. 轮询查询
while True:
    status = manager.get_status(task_id)
    if status['status'] == 'completed':
        break
    time.sleep(5)

# 3. 获取结果
result = manager.get_result(task_id)
```

**记忆文件**: `memory/agents/long_task_manager.md`

---
