# API 使用注意事项

本文档记录在测试中发现的API接口问题和正确用法，防止再次出错。

## 目录

1. [感知记忆模块](#一感知记忆模块)
2. [短期记忆模块](#二短期记忆模块)
3. [长期记忆模块](#三长期记忆模块)
4. [加密模块](#四加密模块)
5. [记忆索引模块](#五记忆索引模块)
6. [冷热度管理模块](#六冷热度管理模块)
7. [状态捕捉模块](#七状态捕捉模块)
8. [链模块](#八链模块)

---

## 一、感知记忆模块

### PerceptionMemoryStore

#### store_conversation()

**错误用法**：
```python
store.store_conversation(
    session_id=session_id,
    role="user",  # ❌ 错误：没有 role 参数
    content="对话内容"  # ❌ 错误：没有 content 参数
)
```

**正确用法**：
```python
store.store_conversation(
    session_id=session_id,
    user_message="用户消息",  # ✅ 正确参数名
    system_response="系统回复",  # ✅ 正确参数名
    metadata={"topic": "数据分析"}  # 可选
)
```

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| session_id | str | 是 | 会话ID |
| user_message | str | 是 | 用户消息内容 |
| system_response | str | 是 | 系统回复内容 |
| metadata | dict | 否 | 元数据 |

---

## 二、短期记忆模块

### ShortTermMemoryManager

#### get_bucket() vs get_all_buckets()

**注意**：`ShortTermMemoryManager` 没有 `get_all_buckets()` 方法。

**正确用法**：
```python
from scripts.type_defs import SemanticBucketType

manager = ShortTermMemoryManager()

# 获取单个语义桶
bucket = manager.get_bucket(SemanticBucketType.TASK_CONTEXT)

# 添加记忆项到桶
bucket.add_item(
    content="记忆内容",
    metadata={"topic": "主题"}
)

# 获取桶中的项
items = bucket.get_items()

# 获取桶的填充率
fill_ratio = bucket.get_fill_ratio()
```

---

## 三、长期记忆模块

### LongTermMemoryManager

#### update_user_profile()

**错误用法**：
```python
manager.update_user_profile(
    user_id="test_user",  # ❌ 错误：没有 user_id 参数
    identity_tags=["数据分析师"],
    technical_fields=["数据分析"]
)
```

**正确用法**：
```python
# 传入字典参数
profile_data = {
    "identity_tags": ["数据分析师"],
    "technical_fields": ["数据分析"],
    "proficiency_level": "intermediate"
}
profile_id = manager.update_user_profile(profile_data)
```

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| profile_data | dict | 是 | 用户画像数据字典 |

---

## 四、加密模块

### KeyManager

#### set_key()

**错误用法**：
```python
key_manager.set_key(key)  # ❌ 错误：缺少 key_id 参数
```

**正确用法**：
```python
key_manager.set_key(
    key_id="my_key",  # ✅ 密钥ID
    key=key_bytes  # ✅ 密钥字节
)
```

### generate_encryption_key()

**注意**：返回的是 base64 编码的字符串，不是 bytes。

**正确用法**：
```python
import base64
from scripts.encryption import generate_encryption_key, KeyManager, DataEncryptor

# 生成密钥（返回 base64 字符串）
key_str = generate_encryption_key()

# 转换为 bytes
key_bytes = base64.b64decode(key_str)

# 设置密钥
key_manager = KeyManager()
key_manager.set_key(key_id="test_key", key=key_bytes)

# 加密
encryptor = DataEncryptor(key_manager)
encrypted = encryptor.encrypt("敏感数据")

# 解密（返回 bytes，需要转换）
decrypted = encryptor.decrypt(encrypted)
if isinstance(decrypted, bytes):
    decrypted = decrypted.decode('utf-8')
```

---

## 五、记忆索引模块

### MemoryIndexer

#### index() vs add_document()

**错误用法**：
```python
indexer.add_document(doc)  # ❌ 错误：没有 add_document 方法
```

**正确用法**：
```python
indexer.index(
    memory_id="doc_1",  # ✅ 记忆ID
    content="记忆内容",
    metadata={"type": "task_context"}
)
```

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| memory_id | str | 是 | 记忆唯一标识 |
| content | str | 是 | 记忆内容 |
| metadata | dict | 否 | 元数据 |

---

## 六、冷热度管理模块

### HeatManager

#### calculate_heat_score()

**错误用法**：
```python
score = manager.calculate_heat_score(
    access_count=10,
    last_access_hours=1  # ❌ 错误：参数名不正确
)
```

**正确用法**：
```python
score = manager.calculate_heat_score(
    days_since_access=1.0,  # ✅ 正确参数名
    access_count=10,
    importance=0.8,
    user_interaction=0.5
)
```

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| days_since_access | float | 是 | 距上次访问的天数 |
| access_count | int | 是 | 访问次数 |
| importance | float | 是 | 重要性（0-1） |
| user_interaction | float | 是 | 用户交互程度（0-1） |

---

## 七、状态捕捉模块

### GlobalStateCapture

#### capture_snapshot()

**错误用法**：
```python
snapshot = capture.capture_snapshot()  # ❌ 错误：缺少 state 参数
```

**正确用法**：
```python
state = {
    "current_task": "数据分析",
    "user_context": {"role": "analyst"}
}
snapshot = capture.capture_snapshot(state=state)
```

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| state | dict | 是 | 状态字典 |

---

## 八、链模块

### ExtractedCausalChain

**注意**：需要使用特定的节点对象类型，不能直接使用字符串。

**错误用法**：
```python
chain = ExtractedCausalChain(
    chain_id="c1",
    problem="学习Python",  # ❌ 错误：应该是 ProblemNode 对象
    causes=["完成项目"],  # ❌ 错误：应该是 CauseNode 对象列表
    causal_relations=[("学习", "完成")],  # ❌ 错误：应该是 CausalRelation 对象列表
    solutions=["继续学习"]  # ❌ 错误：应该是 SolutionNode 对象列表
)
```

**正确用法**：
```python
from scripts.chains.causal_chain import (
    ProblemNode, CauseNode, CausalRelation, SolutionNode
)

# 创建节点对象
problem = ProblemNode(content="学习Python")
cause = CauseNode(content="完成数据分析项目")
relation = CausalRelation(
    from_cause="cause_1",  # ✅ 正确参数名
    to_effect="effect_1",  # ✅ 正确参数名
    relation_type="leads_to"
)
solution = SolutionNode(content="继续学习")

# 创建链
chain = ExtractedCausalChain(
    chain_id="c1",
    content="用户学习Python导致完成数据分析项目",
    problem=problem,
    causes=[cause],
    causal_relations=[relation],
    solutions=[solution],
    extraction_confidence=0.9
)
```

### CausalRelation

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| from_cause | str | 是 | 原因节点ID |
| to_effect | str | 是 | 结果节点ID |
| relation_type | str | 否 | 关系类型，默认 "causes" |
| strength | float | 否 | 关系强度（0-1），默认 0.5 |

---

## 常见错误汇总

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `store_conversation() got an unexpected keyword argument 'role'` | 参数名错误 | 使用 `user_message` 和 `system_response` |
| `update_user_profile() got an unexpected keyword argument 'user_id'` | 参数格式错误 | 传入字典参数 |
| `KeyManager.set_key() missing 1 required positional argument` | 缺少参数 | 提供 `key_id` 和 `key` |
| `'MemoryIndexer' object has no attribute 'add_document'` | 方法名错误 | 使用 `index()` 方法 |
| `calculate_heat_score() got an unexpected keyword argument 'last_access_hours'` | 参数名错误 | 使用 `days_since_access` |
| `Cannot convert "<class 'str'>" instance to a buffer` | 密钥类型错误 | 将 base64 字符串转换为 bytes |
| `Input should be a valid dictionary or instance of ProblemNode` | 对象类型错误 | 使用正确的节点对象类型 |

---

## 测试验证

使用以下代码验证API是否正确调用：

```python
import sys
sys.path.insert(0, '/workspace/projects/agent-memory')

# 1. 感知记忆
from scripts.perception import PerceptionMemoryStore
store = PerceptionMemoryStore(user_id="test")
session_id = store.create_session()
store.store_conversation(
    session_id=session_id,
    user_message="测试消息",
    system_response="测试回复"
)

# 2. 短期记忆
from scripts.short_term import ShortTermMemoryManager
from scripts.type_defs import SemanticBucketType
manager = ShortTermMemoryManager()
bucket = manager.get_bucket(SemanticBucketType.TASK_CONTEXT)
bucket.add_item(content="测试内容")  # size 是属性，不是方法

# 3. 长期记忆
from scripts.long_term import LongTermMemoryManager
ltm = LongTermMemoryManager()
ltm.update_user_profile({"identity_tags": ["测试"]})

# 4. 加密
import base64
from scripts.encryption import generate_encryption_key, KeyManager, DataEncryptor
key_bytes = base64.b64decode(generate_encryption_key())
km = KeyManager()
km.set_key(key_id="test", key=key_bytes)
enc = DataEncryptor(km)
encrypted = enc.encrypt("测试")
decrypted = enc.decrypt(encrypted)
if isinstance(decrypted, bytes):
    decrypted = decrypted.decode('utf-8')

print("所有API验证通过！")
```

---

## 九、上下文编排模块

### ContextOrchestrator

**重要**：ContextOrchestrator 的初始化需要多个必需参数，方法名也与文档描述不同。

#### 初始化

**错误用法**：
```python
orchestrator = ContextOrchestrator()  # ❌ 错误：缺少必需参数
```

**正确用法**：
```python
from scripts.context_orchestrator import ContextOrchestrator, ContextConfig
from scripts.redis_adapter import RedisAdapter, RedisConfig

# 创建 Redis 适配器
redis_config = RedisConfig(host="localhost", port=6379)
redis_adapter = RedisAdapter(config=redis_config)

# 创建编排器
orchestrator = ContextOrchestrator(
    redis_adapter=redis_adapter,  # ✅ 必需：Redis适配器
    user_id="test_user",           # ✅ 必需：用户ID
    session_id="session_1",        # ✅ 必需：会话ID
    config=None,                   # 可选：ContextConfig
    token_budget_config=None       # 可选：TokenBudgetConfig
)
```

**参数说明**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| redis_adapter | RedisAdapter | 是 | Redis适配器实例 |
| user_id | str | 是 | 用户ID |
| session_id | str | 是 | 会话ID |
| config | ContextConfig | 否 | 上下文配置 |
| token_budget_config | TokenBudgetConfig | 否 | Token预算配置 |

#### prepare_context() vs prepare()

**错误用法**：
```python
context = orchestrator.prepare(user_input="测试")  # ❌ 错误：没有 prepare 方法
```

**正确用法**：
```python
context = orchestrator.prepare_context(
    user_input="用户输入",           # ✅ 正确方法名
    system_instruction="系统指令",   # 可选
    retrieval_results=["检索结果"],  # 可选
    tool_results=["工具结果"],       # 可选
    additional_blocks=[]             # 可选
)
```

#### 其他常用方法

| 方法 | 说明 |
|------|------|
| `prepare_context()` | 准备上下文 |
| `compress_context()` | 压缩上下文 |
| `store_memory()` | 存储记忆 |
| `select_relevant_memories()` | 选择相关记忆 |
| `get_hot_memories()` | 获取热门记忆 |
| `get_cold_memories()` | 获取冷门记忆 |
| `end_session()` | 结束会话 |

---

## 常见错误汇总（更新）

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `ContextOrchestrator.__init__() missing 3 required positional arguments` | 缺少必需参数 | 提供 `redis_adapter`, `user_id`, `session_id` |
| `'ContextOrchestrator' object has no attribute 'prepare'` | 方法名错误 | 使用 `prepare_context()` |
| `'ContextOrchestrator' object has no attribute 'get_context'` | 方法不存在 | 使用 `prepare_context()` 返回上下文 |
