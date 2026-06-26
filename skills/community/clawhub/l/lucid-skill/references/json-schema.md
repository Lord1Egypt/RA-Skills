# update-semantic JSON Format

Schema for `lucid-skill update-semantic`. Defines business semantics, relationships, and metrics for connected tables.

## Full Example

```json
{
  "tables": [
    {
      "table_name": "orders",
      "description": "订单主表，记录所有交易信息",
      "business_domain": "电商/交易",
      "tags": ["核心表", "财务"],
      "columns": [
        {
          "name": "id",
          "semantic": "订单唯一标识",
          "role": "id"
        },
        {
          "name": "customer_id",
          "semantic": "关联客户ID",
          "role": "dimension"
        },
        {
          "name": "amount",
          "semantic": "订单金额",
          "role": "measure",
          "unit": "CNY",
          "aggregation": "sum"
        },
        {
          "name": "status",
          "semantic": "订单状态",
          "role": "dimension"
        },
        {
          "name": "created_at",
          "semantic": "下单时间",
          "role": "timestamp"
        }
      ],
      "relations": [
        {
          "target_table": "customers",
          "join_condition": "orders.customer_id = customers.id",
          "relation_type": "many_to_one"
        }
      ],
      "metrics": [
        {
          "name": "日GMV",
          "expression": "SUM(amount)",
          "group_by": "DATE(created_at)"
        },
        {
          "name": "订单数",
          "expression": "COUNT(*)",
          "group_by": "DATE(created_at)"
        }
      ]
    }
  ]
}
```

## Field Reference

### Table Level

| Field | Required | Description |
|-------|----------|-------------|
| `table_name` | Yes | Exact table name as shown by `lucid-skill tables` |
| `description` | Yes | Human-readable description of the table's purpose |
| `business_domain` | No | Business domain category (e.g., "电商/交易", "用户/增长") |
| `tags` | No | Array of tags for categorization |
| `columns` | Yes | Array of column definitions |
| `relations` | No | Array of foreign key relationships |
| `metrics` | No | Array of common business metrics |

### Column Level

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Exact column name |
| `semantic` | Yes | Human-readable meaning of this column |
| `role` | Yes | One of: `id`, `dimension`, `measure`, `timestamp`, `attribute` |
| `unit` | No | Unit of measure (e.g., "CNY", "USD", "件", "秒") |
| `aggregation` | No | Default aggregation for measures: `sum`, `avg`, `count`, `min`, `max` |

### Column Roles

| Role | When to Use |
|------|-------------|
| `id` | Primary key or unique identifier |
| `dimension` | Categorical grouping column (status, category, region) |
| `measure` | Numeric value for aggregation (amount, count, price) |
| `timestamp` | Date/time column |
| `attribute` | Descriptive field not typically used for grouping (name, address) |

### Relation Level

| Field | Required | Description |
|-------|----------|-------------|
| `target_table` | Yes | The related table name |
| `join_condition` | Yes | SQL JOIN condition (e.g., `orders.customer_id = customers.id`) |
| `relation_type` | Yes | One of: `one_to_one`, `one_to_many`, `many_to_one`, `many_to_many` |

### Metric Level

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Business metric name |
| `expression` | Yes | SQL aggregation expression |
| `group_by` | No | Default GROUP BY expression |
