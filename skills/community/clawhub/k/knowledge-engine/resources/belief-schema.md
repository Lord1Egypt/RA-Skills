# Belief Card Schema

每个信念卡片是一个 JSON 文件，存储在 `memory/beliefs/` 下。

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---:|:---|
| `id` | string | ✓ | 唯一标识，格式：`belief-YYYYMMDD-NNN` |
| `belief` | string | ✓ | 信念内容 |
| `reasoning` | string | | 支持推理 |
| `confidence` | enum | ✓ | `high` / `medium` / `low` |
| `status` | enum | ✓ | `active` / `challenged` / `superseded` / `archived` |
| `challenges` | array | ✓ | 挑战记录 `[{note, date}]` |
| `updates` | array | ✓ | 更新记录 `[{note, date}]` |
| `created_at` | ISO string | ✓ | 创建时间 |
| `updated_at` | ISO string | ✓ | 最后更新时间 |

## 状态流转

```
active ← 新信念
  ↓ 被事实挑战
challenged ← 有挑战记录
  ↓ 被新信念替代
superseded ← 被新信念取代
  ↓ 归档
archived ← 不再相关但保留记录
```

## 时间衰减规则

信念的"有效置信度" = 原始置信度 × 时间衰减 × 挑战衰减

| 条件 | 效果 |
|:---|:---|
| 最近 7 天内更新 | 不衰减 |
| 7-14 天未更新 | 降一级 |
| 14-30 天未更新 | 再降一级 |
| 30 天以上 + 零更新 | 强制 low |
| 被挑战过 | 额外降一级 |
| 近期有更新 | 保持或提升 |

## 示例

```json
{
  "id": "belief-20260327-001",
  "belief": "Self-belief是做出来的不是喊出来的",
  "reasoning": "Musk的conviction是十几年失败中锤出来的",
  "confidence": "medium",
  "status": "active",
  "challenges": [],
  "updates": [],
  "created_at": "2026-03-27T22:30:00",
  "updated_at": "2026-03-27T22:30:00"
}
```
