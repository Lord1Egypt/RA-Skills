# Retrieve rows from a data table

## 何时读取

当用户需要从 n8n workflow 或外部系统调用 n8n Public API 时读取。

## Endpoint

- Method: `GET`
- Path: `/data-tables/{dataTableId}/rows`
- Base URL: `https://<your-n8n-host>/api/v1`

## Auth / Headers

- Header: `X-N8N-API-KEY: <api-key>`
- 不要把真实 API key 写入 workflow JSON、示例或日志。

## Params

- `filter` in `query`; required: `False`
- `sortBy` in `query`; required: `False`
- `search` in `query`; required: `False`

## Body

- No request body in OpenAPI spec.

## Responses

- `200`: Successfully retrieved rows
- `400`: response
- `401`: response
- `404`: response

