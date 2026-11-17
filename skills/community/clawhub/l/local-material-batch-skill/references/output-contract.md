# 输出约定

## 单条输出

每个处理后的条目会写到：

```text
outputs/items/<item_id>/text.md
outputs/items/<item_id>/text.json
```

`text.json` 字段：

- `item_id`
- `source_path`
- `source_type`
- `status`
- `backend`
- `text`
- `error`

## 批量输出

整批处理会写到：

```text
outputs/manifest.json
outputs/summary.csv
```

`manifest.json` 字段：

- `generated_at`
- `root`
- `items`

## 状态值

- `ok`
- `pending-backend`
- `failed`
- `skipped-existing`
