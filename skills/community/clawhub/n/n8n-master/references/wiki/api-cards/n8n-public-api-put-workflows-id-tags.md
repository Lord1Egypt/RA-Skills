# Update tags of a workflow

## 何时读取

当用户需要从 n8n workflow 或外部系统调用 n8n Public API 时读取。

## Endpoint

- Method: `PUT`
- Path: `/workflows/{id}/tags`
- Base URL: `https://<your-n8n-host>/api/v1`

## Auth / Headers

- Header: `X-N8N-API-KEY: <api-key>`
- 不要把真实 API key 写入 workflow JSON、示例或日志。

## Params

- No explicit parameters in OpenAPI spec.

## Body

- Request body present in OpenAPI spec.

## Responses

- `200`: List of tags after add the tag
- `400`: response
- `401`: response
- `404`: response

