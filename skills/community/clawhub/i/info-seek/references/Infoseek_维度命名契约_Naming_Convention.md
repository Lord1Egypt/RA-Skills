# Infoseek 维度命名契约（人物 6 维分桶）

> 版本：v1.0.1 ｜ 状态：✅ 已提供 ｜ 对齐目标：`core/entity_profile.py` / `core/entity_trajectory.py`

## 1. 目的

为「人物类」实体调研提供统一的 6 维分桶约定，其他人物类工具（实体画像 / 轨迹追踪 / 热度预测）对齐此命名，保证跨工具字段一致。

## 2. 人物 6 维分桶

| 维度 | 字段名 | 说明 | 示例值 |
|------|--------|------|--------|
| ① 身份 | `role` | 职级/角色 | `founder` / `CEO` / `researcher` |
| ② 组织 | `org` | 所属机构/公司 | `DeepSeek` / `OpenAI` |
| ③ 领域 | `domain` | 专业方向 | `AI` / `finance` |
| ④ 活跃度 | `activity` | 近期活跃（0-100） | `76` |
| ⑤ 影响力 | `influence` | 声量/热度（0-100） | `88` |
| ⑥ 关联 | `affiliations` | 关键关联实体列表 | `["DeepSeek", "清华"]` |

## 3. 数据结构约定

实体画像（`EntityProfile`）核心字段：

```json
{
  "entity_name": "string",
  "entity_type": "PERSON|ORG|TECH|...",
  "topics": ["string"],
  "source_domains": ["string"],
  "first_seen": "ISO8601",
  "last_seen": "ISO8601",
  "hit_total": 0,
  "conflict_refs": []
}
```

轨迹（`entity_trajectory.py`）输出字段：

```json
{
  "entity": "string",
  "timeline": [{"date": "ISO8601", "subject": "string"}],
  "subjects_seen": [],
  "total_occurrences": 0,
  "active_days": 0,
  "avg_claims_per_day": 0.0,
  "is_rising": true,
  "first_seen": "ISO8601"
}
```

## 4. 热度分级

| 等级 | 热度值 | 含义 |
|------|--------|------|
| hot | ≥60 | 高热度（近期高频） |
| warm | 30-59 | 中等 |
| cold | <30 | 低/冷却 |

热度预测（`entity_heat.py`）：基于 90 天半衰期衰减外推，`trend ∈ {stable, rising, falling}`。

## 5. 兼容性

- 命名均小写下划线 snake_case，与 `core/` 全库一致
- 新工具若需扩展维度，须在现有 6 维基础上追加，不得重命名既有字段
