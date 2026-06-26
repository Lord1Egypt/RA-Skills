# Concept Card Schema

每个概念卡片是一个 JSON 文件，存储在 `memory/concepts/` 下。

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---:|:---|
| `id` | string | ✓ | 唯一标识，格式：`slug-hash8` |
| `concept` | string | ✓ | 概念名称 |
| `source` | string | | 来源（文章链接、书名、对话等） |
| `context` | string | | 上下文描述 |
| `tags` | string[] | ✓ | 标签列表（不含 `level:` 前缀的为用户标签） |
| `confidence` | enum | ✓ | `high` / `medium` / `low` |
| `status` | enum | ✓ | `active` / `deprecated` / `superseded` |
| `related` | string[] | | 已废弃，请用 concept_links 表 |
| `created_at` | ISO string | ✓ | 创建时间 |
| `updated_at` | ISO string | ✓ | 最后更新时间 |

## 特殊标签

| 标签 | 含义 |
|:---|:---|
| `level:l2` | L2 洞察（从 L1 蒸馏而来） |
| `level:l3` | L3 元规律（从 L2 蒸馏而来） |
| `洞察` | 自动生成的洞察概念 |

## 示例

```json
{
  "id": "分发能力-制作能力-d2a0e8ed",
  "concept": "分发能力 > 制作能力",
  "source": "HN 2026-03-27",
  "context": "当AI让创作成本趋近于零，稀缺资源转移到分发",
  "tags": ["创业", "洞察", "AI", "分发"],
  "confidence": "high",
  "status": "active",
  "related": [],
  "created_at": "2026-03-27T22:05:43.566376",
  "updated_at": "2026-03-27T22:05:43.566376"
}
```
