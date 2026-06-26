# RAG Schema 文档

本文档定义了 MaskClaw 框架中 ChromaDB 向量数据库的存储范式与元数据设计。

## 1. 概述

ChromaDB 作为 MaskClaw 的本地向量数据库，主要用于：

1. **隐私规则向量检索**：存储用户个性化隐私规则，支持语义相似度搜索
2. **行为记忆**：记录用户历史行为模式，用于 SOP 进化
3. **场景匹配**：根据当前 UI 上下文匹配最相关的规则

## 2. Collection 设计

### 2.1 Collection 列表

| Collection | 用户隔离 | 说明 |
|:------------|:---------|:-----|
| `rules_{user_id}` | ✅ | 用户个性化规则 |
| `behaviors_{user_id}` | ✅ | 用户行为记录 |
| `system_rules` | ❌ | 系统内置规则 |

### 2.2 命名规范

```
rules_{user_id}     # 例: rules_user_001
behaviors_{user_id} # 例: behaviors_user_001
system_rules         # 系统级，不带用户后缀
```

## 3. 系统规则 Collection

### 3.1 Document Schema

```json
{
  "content": "在微信发送位置时，应使用模糊位置而非精确坐标",
  "rule_id": "sys_wechat_location_001",
  "app_context": "wechat",
  "sensitive_type": "location",
  "risk_level": "S",
  "strategy": "mask",
  "confidence": 0.95,
  "source": "builtin",
  "created_ts": 1700000000
}
```

### 3.2 元数据字段

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `rule_id` | string | 规则唯一标识 |
| `app_context` | string | 应用上下文 |
| `sensitive_type` | string | 敏感数据类型 |
| `risk_level` | string | 风险等级 (H/S/N) |
| `strategy` | string | 处理策略 |
| `confidence` | float | 置信度 (0-1) |
| `source` | string | 规则来源 |
| `created_ts` | int | 创建时间戳 |

## 4. 用户规则 Collection

### 4.1 Document Schema

```json
{
  "content": "在钉钉发送给同事时，不要发送病历截图",
  "rule_id": "user_001_20260325_001",
  "app_context": "dingtalk",
  "sensitive_type": "medical_record",
  "risk_level": "H",
  "strategy": "block",
  "replacement": null,
  "trigger_count": 3,
  "confidence": 0.82,
  "source": "evolution",
  "created_ts": 1700000000,
  "updated_ts": 1700000100,
  "expires_ts": 1700604800,
  "status": "active"
}
```

### 4.2 元数据字段

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `rule_id` | string | 规则唯一标识 |
| `user_id` | string | 用户 ID |
| `app_context` | string | 应用上下文 |
| `sensitive_type` | string | 敏感数据类型 |
| `risk_level` | string | 风险等级 |
| `strategy` | string | 处理策略 |
| `replacement` | string/null | 替代值 |
| `trigger_count` | int | 触发次数 |
| `confidence` | float | 置信度 |
| `source` | string | 来源 (evolution/rule/user) |
| `created_ts` | int | 创建时间 |
| `updated_ts` | int | 更新时间 |
| `expires_ts` | int | 过期时间 |
| `status` | string | 状态 (active/disabled) |

## 5. 行为记录 Collection

### 5.1 Document Schema

```json
{
  "content": "用户拒绝了'发送给同事'操作，原因：包含病历信息",
  "trace_id": "trace_001",
  "user_id": "user_001",
  "app_context": "dingtalk",
  "action": "share_or_send",
  "scenario_tag": "钉钉发送病历截图给同事",
  "resolution": "correction",
  "correction_type": "user_denied",
  "pii_types": ["MedicalRecord"],
  "relationship_tag": "同事",
  "agent_intent": "发送病历截图",
  "quality_score": 3.6,
  "timestamp": 1700000000
}
```

### 5.2 元数据字段

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `trace_id` | string | 轨迹唯一标识 |
| `user_id` | string | 用户 ID |
| `app_context` | string | 应用上下文 |
| `action` | string | 操作类型 |
| `scenario_tag` | string | 场景标签 |
| `resolution` | string | 决策结果 |
| `correction_type` | string | 纠错类型 |
| `pii_types` | list | 涉及 PII 类型 |
| `relationship_tag` | string | 关系标签 |
| `agent_intent` | string | Agent 意图 |
| `quality_score` | float | 质量评分 |
| `timestamp` | int | 时间戳 |

## 6. 敏感数据类型枚举

| 类型 | 说明 |
|:-----|:-----|
| `name` | 姓名 |
| `phone` | 手机号 |
| `id_card` | 身份证号 |
| `bank_card` | 银行卡号 |
| `address` | 地址 |
| `location` | 地理位置 |
| `email` | 邮箱 |
| `medical_record` | 病历信息 |
| `password` | 密码 |
| `payment` | 支付信息 |

## 7. 风险等级

| 等级 | 说明 | 默认策略 |
|:----:|:-----|:---------|
| `H` | High Risk | block |
| `S` | Standard Risk | mask |
| `N` | Normal Risk | ask |

## 8. 过期时间配置

| 策略 | 默认过期时间 |
|:-----|:------------|
| `allow` | 24 小时 |
| `block` | 24 小时 |
| `mask` | 24 小时 |
| `ask` | 7 天 |
| `defer` | 7 天 |
| `interrupt` | 7 天 |

## 9. 查询示例

### 9.1 语义检索相似规则

```python
from memory.chroma_manager import ChromaManager

chroma = ChromaManager()

# 检索与当前场景相关的规则
results = chroma.query_rules(
    user_id="user_001",
    query="钉钉发送工作文档",
    n_results=5,
    filter_dict={
        "app_context": "dingtalk"
    }
)
```

### 9.2 获取用户所有活跃规则

```python
# 获取用户所有活跃规则
results = chroma.get_rules_by_user(
    user_id="user_001",
    status="active"
)
```

### 9.3 按应用上下文统计

```python
# 统计用户在各应用的规则数量
stats = chroma.get_rule_stats_by_app(
    user_id="user_001"
)
# 返回: {"dingtalk": 5, "wechat": 3, "taobao": 2}
```

## 10. 更新日志

### v1.0.0 (2026-03-25)

- 初始版本
- 支持用户隔离规则存储
- 支持语义向量检索
- 支持规则过期机制
