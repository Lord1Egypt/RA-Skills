# Create multiple users

## 何时读取

当用户需要从 n8n workflow 或外部系统调用 n8n Public API 时读取。

## Endpoint

- Method: `POST`
- Path: `/users`
- Base URL: `https://<your-n8n-host>/api/v1`

## Auth / Headers

- Header: `X-N8N-API-KEY: <api-key>`
- 不要把真实 API key 写入 workflow JSON、示例或日志。

## Params

- No explicit parameters in OpenAPI spec.

## Body

- Request body present in OpenAPI spec.

## Responses

- `200`: Operation successful.
- `401`: response
- `403`: response

