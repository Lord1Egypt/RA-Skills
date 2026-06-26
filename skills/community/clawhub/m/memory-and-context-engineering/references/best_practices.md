# 最佳实践

本文档提供 Agent Memory System 的最佳实践指南。

## 目录

1. [架构设计](#架构设计)
2. [性能优化](#性能优化)
3. [安全性](#安全性)
4. [调试与监控](#调试与监控)
5. [部署与运维](#部署与运维)

---

## 架构设计

### 1. 模块化设计

将上下文管理拆分为独立的模块，每个模块负责单一职责。

**推荐做法**：
```python
# 使用 ContextOrchestrator 作为总控层
orchestrator = ContextOrchestrator(
    redis_adapter=redis_adapter,
    user_id=user_id,
    session_id=session_id,
)

# 按需启用功能
orchestrator.enable_quality_assessment()
orchestrator.enable_performance_monitoring()
```

**不推荐做法**：
```python
# 直接使用内部实现模块
from scripts.context_orchestrator import PriorityResolver

resolver = PriorityResolver()
# 应该通过 ContextOrchestrator 使用
```

### 2. 上下文来源分类

合理使用 9 种上下文来源（8 种标准 + 1 种自定义）。

**推荐做法**：
```python
# 使用标准来源
ContextBlock(
    source=ContextSource.SYSTEM,
    priority=ContextPriority.CRITICAL,
    content="系统指令",
    metadata={"subtype": "system_prompt"},
)

# 使用自定义来源处理未知类型
orchestrator.register_custom_type(
    custom_type="workflow_step",
    priority=ContextPriority.HIGH,
)

ContextBlock(
    source=ContextSource.CUSTOM,
    priority=ContextPriority.HIGH,
    content="工作流步骤",
    metadata={
        "custom_type": "workflow_step",
        "step_id": "001",
    },
)
```

### 3. Metadata 规范化

为所有上下文块提供规范的 metadata。

**推荐做法**：
```python
metadata = {
    # 细粒度类型（可选）
    "subtype": "system_prompt",

    # 自定义类型（仅 CUSTOM 来源必需）
    "custom_type": "workflow_step",

    # 推荐字段
    "version": "1.0",
    "timestamp": "2024-01-01T00:00:00Z",
    "source_id": "source_123",

    # 可选字段
    "weight": 0.8,

    # 扩展字段
    "extra": {"custom_field": "value"},
}
```

---

## 性能优化

### 1. 启用 LRU 缓存

对于高并发场景，启用 LRU 缓存可以显著提升性能。

**推荐做法**：
```python
# 启用 LRU 缓存
orchestrator.enable_lru_cache(cache_size=1000)

# 监控缓存命中率
cache_stats = orchestrator.get_cache_stats()
print(f"缓存命中率: {cache_stats['hit_rate']}")
```

**性能提升**：
- 首次解析：~4ms
- 缓存命中：~0.1ms
- 加速比：~40x

### 2. 批量处理

对于大量上下文块，使用批量处理方法。

**推荐做法**：
```python
# 批量验证 metadata
results = orchestrator.validate_metadata_batch(
    metadata_list=metadata_list,
    source_list=source_list,
)

# 批量解析优先级
priorities = orchestrator._priority_resolver.resolve_priorities_batch(blocks)
```

### 3. 按需启用功能

根据实际需求启用功能，避免不必要的性能开销。

**推荐做法**：
```python
# 生产环境：启用性能监控
orchestrator.enable_performance_monitoring()

# 开发环境：启用质量评估
orchestrator.enable_quality_assessment(
    storage_path="usage_stats.json",
    enable_monitoring=True,
)

# 测试环境：禁用所有监控
orchestrator.disable_performance_monitoring()
orchestrator.disable_quality_assessment()
```

### 4. 缓存大小配置

根据实际数据量和内存限制配置缓存大小。

**推荐做法**：
```python
# 小型应用（< 1000 上下文块）
orchestrator.enable_lru_cache(cache_size=500)

# 中型应用（1000 - 10000 上下文块）
orchestrator.enable_lru_cache(cache_size=2000)

# 大型应用（> 10000 上下文块）
orchestrator.enable_lru_cache(cache_size=5000)
```

---

## 安全性

### 1. 隐私保护

始终在使用记忆功能前获取用户同意。

**推荐做法**：
```python
from scripts import PrivacyManager, ConsentStatus

privacy_manager = PrivacyManager(user_id="user_123")
if privacy_manager.get_consent_status("memory_storage") != ConsentStatus.GRANTED:
    privacy_manager.request_consent(
        consent_type="memory_storage",
        description="是否允许存储交互记忆以提供个性化服务？"
    )
```

### 2. 数据加密

对于敏感数据，使用加密存储。

**推荐做法**：
```python
from scripts import encrypt_data, decrypt_data

# 加密敏感数据
encrypted = encrypt_data(
    data="用户密码",
    password="encryption_key",
)

# 解密数据
decrypted = decrypt_data(
    encrypted_data=encrypted,
    password="encryption_key",
)
```

### 3. 访问控制

确保用户只能访问自己的数据。

**推荐做法**：
```python
# 使用 user_id 隔离数据
orchestrator = ContextOrchestrator(
    redis_adapter=redis_adapter,
    user_id=current_user_id,  # 当前用户 ID
    session_id=session_id,
)

# 不要共享 user_id
```

### 4. 输入验证

始终验证用户输入。

**推荐做法**：
```python
from scripts import MetadataValidator

# 验证 metadata
result = MetadataValidator.validate(metadata, source)
if not result.valid:
    raise ValueError(f"Invalid metadata: {result.message}")
```

---

## 调试与监控

### 1. 启用性能监控

在生产环境中启用性能监控，及时发现性能问题。

**推荐做法**：
```python
orchestrator.enable_performance_monitoring()

# 定期生成性能报告
report = orchestrator.generate_performance_report()
print(report)
```

### 2. 启用质量评估

在开发环境中启用质量评估，确保 metadata 质量。

**推荐做法**：
```python
orchestrator.enable_quality_assessment(
    storage_path="usage_stats.json",
    enable_monitoring=True,
)

# 生成质量报告
quality_report = orchestrator.generate_quality_report(blocks)
print(quality_report)

# 生成改进建议
recommendations = orchestrator.generate_improvement_recommendations()
print(recommendations)
```

### 3. 定期清理

定期清理未使用的自定义类型和过期数据。

**推荐做法**：
```python
# 清理 90 天未使用的自定义类型
cleaned = orchestrator.cleanup_unused_custom_types(threshold_days=90)
print(f"清理的类型: {cleaned}")

# 清空缓存
orchestrator._priority_resolver.clear_cache()
```

### 4. 日志记录

记录关键操作和错误信息。

**推荐做法**：
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    context = orchestrator.prepare_context(
        user_input=user_input,
        system_instruction=system_instruction,
    )
    logger.info(f"上下文准备成功，Token 数: {context.token_count}")
except Exception as e:
    logger.error(f"上下文准备失败: {e}")
    raise
```

---

## 部署与运维

### 1. Redis 配置

合理配置 Redis 连接池和超时参数。

**推荐做法**：
```python
from scripts import create_redis_adapter

redis_adapter = create_redis_adapter(
    host="localhost",
    port=6379,
    db=0,
    password="your_password",
    max_connections=100,
    socket_timeout=5,
)
```

### 2. 存储路径管理

统一管理所有存储路径，便于维护。

**推荐做法**：
```python
import os

base_path = "./memory_data"
os.makedirs(base_path, exist_ok=True)

key_storage_path = f"{base_path}/keys"
sync_state_path = f"{base_path}/sync_state"
usage_stats_path = f"{base_path}/usage_stats.json"
```

### 3. 错误处理

实现完善的错误处理和重试机制。

**推荐做法**：
```python
import time
from typing import Callable

def retry_on_failure(
    func: Callable,
    max_retries: int = 3,
    delay: float = 1.0,
):
    """重试失败的函数"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
    return None

# 使用重试
context = retry_on_failure(
    lambda: orchestrator.prepare_context(
        user_input=user_input,
        system_instruction=system_instruction,
    ),
    max_retries=3,
    delay=1.0,
)
```

### 4. 监控告警

设置监控告警，及时发现和解决问题。

**推荐做法**：
```python
# 检查性能指标
stats = orchestrator.get_performance_stats()
for op_name, op_stats in stats["operations"].items():
    avg_time = op_stats["avg_time"]
    if avg_time > 0.1:  # 平均耗时超过 100ms
        # 发送告警
        send_alert(f"操作 {op_name} 耗时过长: {avg_time} 秒")

# 检查缓存命中率
cache_stats = orchestrator.get_cache_stats()
if cache_stats["hit_rate"] < 0.8:  # 命中率低于 80%
    # 发送告警
    send_alert(f"缓存命中率过低: {cache_stats['hit_rate']}")
```

### 5. 定期备份

定期备份重要数据。

**推荐做法**：
```python
import shutil
from datetime import datetime

# 备份统计数据
backup_path = f"./backups/usage_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
shutil.copy("usage_stats.json", backup_path)

# 备份 Redis 数据
# 使用 redis-cli --rdb 命令
```

---

## 常见问题

### Q1: 如何选择合适的缓存大小？

**A**: 根据实际数据量和内存限制选择：
- 小型应用：500-1000
- 中型应用：1000-2000
- 大型应用：2000-5000

### Q2: 什么时候应该启用质量评估？

**A**: 
- 开发环境：始终启用，确保 metadata 质量
- 生产环境：按需启用，避免性能开销

### Q3: 如何处理并发访问？

**A**:
- 使用线程锁保护共享数据
- 使用原子操作更新计数
- 最小化锁的持有时间

### Q4: 如何优化内存使用？

**A**:
- 使用 LRU 缓存限制内存占用
- 定期清理未使用的数据
- 避免存储过大的 metadata

---

## 总结

遵循这些最佳实践可以：
- 提升系统性能
- 保证数据安全
- 简化调试过程
- 便于部署运维
