# Search（直接搜索）接口整理

接口文档：<https://www.volcengine.com/docs/85296/1544974?lang=zh>

## Endpoint

- Method：POST
- Path（默认策略）：`/api/v1/application/{application_id}/search`
- Path（指定策略）：`/api/v1/application/{application_id}/search/{scene_id}`
- 华北：`https://aisearch.cn-beijing.volces.com`
- 柔佛：`https://aisearch.ap-southeast-1.volces.com`

## Auth

- Header：`Authorization: Bearer <API Key>`
- Header：`Content-Type: application/json`

## 核心请求体

- `dataset_id`（必需）：物品数据集 ID
- `query`（必需）：至少包含 `text` 或 `image_url`
- `page_number`（默认 1）
- `page_size`（建议不超过 100）
- `user`（可选）：`{"_user_id":"..."}`
- `filter`（可选）：must/must_not/range/and/or
- `sort_by`（可选）：排序字段名（需在应用中配置可用于过滤/排序的字段）
- `sort_order`（可选）：`desc`/`asc`（默认 desc）
- `output_fields`（可选）：控制 display_fields 返回字段
- `context`（可选）：location 等
- `conditional_boost`（可选）
- `disable_personalize`（可选）

## 注意事项

- 使用范围：仅支持【物品数据集】类型的数据集
- 单次请求 HTTP Body 最大不超过 10MB
- 每租户调用可能存在 QPS 限流（文档示例为 20QPS），超限通常返回 429
