# 故障排查指南

本文档提供 Agent Memory System 的常见问题及解决方案。

## 目录

1. [安装与配置问题](#安装与配置问题)
2. [运行时错误](#运行时错误)
3. [性能问题](#性能问题)
4. [数据一致性问题](#数据一致性问题)
5. [内存问题](#内存问题)

---

## 安装与配置问题

### 问题 1：导入错误

**症状**：
```
ModuleNotFoundError: No module named 'scripts'
```

**解决方案**：
```python
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts.context_orchestrator import ContextOrchestrator
```

### 问题 2：Redis 连接失败

**症状**：
```
ConnectionError: Error 111 connecting to localhost:6379. Connection refused.
```

**解决方案**：
1. 检查 Redis 是否启动
```bash
redis-cli ping
# 应返回 PONG
```

2. 检查 Redis 配置
```python
from scripts import create_redis_adapter

redis_adapter = create_redis_adapter(
    host="localhost",
    port=6379,
    password="your_password",  # 如果设置了密码
)

if not redis_adapter.is_available():
    print("Redis 连接失败")
```

3. 使用环境变量配置
```bash
export REDIS_HOST=localhost
export REDIS_PORT=6379
```

### 问题 3：依赖缺失

**症状**：
```
ImportError: cannot import name 'pydantic' from '...'
```

**解决方案**：
```bash
pip install pydantic>=2.0.0 typing-extensions>=4.0.0 cryptography>=41.0.0 redis>=4.5.0 tiktoken>=0.5.0 mmh3>=3.0.0
```

---

## 运行时错误

### 问题 1：验证错误

**症状**：
```
ValueError: Invalid metadata: CUSTOM 来源缺少必需字段: custom_type
```

**解决方案**：
```python
# 为 CUSTOM 来源提供 custom_type
metadata = {
    "custom_type": "system_prompt",  # 必需
    "timestamp": "2024-01-01T00:00:00Z",
}

# 验证 metadata
from scripts import MetadataValidator
result = MetadataValidator.validate(metadata, ContextSource.CUSTOM)
if not result.valid:
    print(f"验证失败: {result.message}")
```

### 问题 2：优先级解析失败

**症状**：
```
KeyError: 'priority'
```

**解决方案**：
```python
# 注册自定义类型
orchestrator.register_custom_type(
    custom_type="workflow_step",
    priority=ContextPriority.HIGH,
    required_fields=["step_id", "status"],
)

# 使用已注册的类型
metadata = {
    "custom_type": "workflow_step",
    "step_id": "001",
    "status": "in_progress",
}
```

### 问题 3：质量评估失败

**症状**：
```
AttributeError: 'NoneType' object has no attribute 'assess_quality'
```

**解决方案**：
```python
# 启用质量评估
orchestrator.enable_quality_assessment(
    storage_path="usage_stats.json",
)

# 检查是否启用
if not orchestrator._enable_quality_assessment:
    print("质量评估未启用")
```

---

## 性能问题

### 问题 1：优先级解析慢

**症状**：
优先级解析耗时过长（> 10ms）

**解决方案**：
```python
# 启用 LRU 缓存
orchestrator.enable_lru_cache(cache_size=1000)

# 监控缓存命中率
cache_stats = orchestrator.get_cache_stats()
print(f"缓存命中率: {cache_stats['hit_rate']}")

# 如果命中率低，增加缓存大小
if cache_stats['hit_rate'] < 0.8:
    orchestrator.enable_lru_cache(cache_size=2000)
```

### 问题 2：内存占用高

**症状**：
进程内存占用持续增长

**解决方案**：
```python
# 定期清理缓存
orchestrator._priority_resolver.clear_cache()

# 清理未使用的自定义类型
cleaned = orchestrator.cleanup_unused_custom_types(threshold_days=90)
print(f"清理的类型: {cleaned}")

# 使用 LRU 缓存限制内存
orchestrator.enable_lru_cache(cache_size=1000)
```

### 问题 3：批量处理慢

**症状**：
批量处理大量上下文块时性能下降

**解决方案**：
```python
# 使用批量处理方法
from scripts import BatchProcessor

# 批量验证
results = BatchProcessor.validate_metadata_batch(
    metadata_list=metadata_list,
    source_list=source_list,
)

# 批量解析优先级
priorities = BatchProcessor.resolve_priorities_batch_optimized(
    resolver=orchestrator._priority_resolver,
    blocks=blocks,
)
```

---

## 数据一致性问题

### 问题 1：统计数据不一致

**症状**：
使用统计数据与实际使用情况不符

**解决方案**：
```python
# 重新加载统计数据
lifecycle_manager = CustomTypeLifecycleManager(storage_path="usage_stats.json")

# 检查统计数据
stats = lifecycle_manager.get_type_stats("custom_type_name")
print(f"使用次数: {stats['count'] if stats else 0}")

# 手动记录使用
lifecycle_manager.track_usage("custom_type_name")
```

### 问题 2：缓存不一致

**症状**：
修改规则后缓存未更新

**解决方案**：
```python
# 修改规则后清空缓存
orchestrator.register_custom_type(
    custom_type="new_type",
    priority=ContextPriority.HIGH,
)

# 清空缓存
orchestrator._priority_resolver.clear_cache()
```

### 问题 3：数据丢失

**症状**：
重启后统计数据丢失

**解决方案**：
```python
# 确保使用持久化存储
orchestrator.enable_quality_assessment(
    storage_path="./memory_data/usage_stats.json",  # 使用绝对路径
)

# 定期备份数据
import shutil
from datetime import datetime

backup_path = f"./backups/usage_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
shutil.copy("./memory_data/usage_stats.json", backup_path)
```

---

## 内存问题

### 问题 1：内存泄漏

**症状**：
长时间运行后内存占用持续增长

**解决方案**：
```python
# 定期清理缓存
import time

def cleanup_task():
    while True:
        time.sleep(3600)  # 每小时清理一次
        orchestrator._priority_resolver.clear_cache()
        orchestrator.cleanup_unused_custom_types(threshold_days=90)

# 启动清理任务
import threading
cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
cleanup_thread.start()
```

### 问题 2：大数据量内存不足

**症状**：
处理大量数据时出现 `MemoryError`

**解决方案**：
```python
# 使用分批处理
def process_in_batches(items, batch_size=100):
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        # 处理批次
        results = BatchProcessor.validate_metadata_batch(
            metadata_list=[item["metadata"] for item in batch],
            source_list=[item["source"] for item in batch],
        )
        yield results

# 使用分批处理
for batch_results in process_in_batches(large_dataset, batch_size=100):
    # 处理每个批次
    pass
```

---

## 调试技巧

### 1. 启用详细日志

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### 2. 使用性能监控

```python
orchestrator.enable_performance_monitoring()

# 执行操作
context = orchestrator.prepare_context(...)

# 查看性能报告
report = orchestrator.generate_performance_report()
print(report)
```

### 3. 检查缓存统计

```python
cache_stats = orchestrator.get_cache_stats()
print(f"缓存大小: {cache_stats['size']}")
print(f"命中率: {cache_stats['hit_rate']}")
print(f"访问次数: {cache_stats['access_count']}")
```

### 4. 检查质量评估

```python
quality_report = orchestrator.generate_quality_report(blocks)
print(quality_report)

recommendations = orchestrator.generate_improvement_recommendations()
print(recommendations)
```

---

## 获取帮助

如果问题仍未解决：

1. 查看日志文件
2. 检查 API 文档
3. 查看最佳实践文档
4. 提交 Issue 并附上：
   - 错误信息
   - 代码片段
   - 环境信息（Python 版本、依赖版本）
   - 复现步骤
