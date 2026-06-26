# Auth and Preflight

## Config Source

本 skill 的可执行前提是：必须提供 API token。未配置 token 时，查询脚本不可用。

默认从工作区本地 secrets 文件读取：

- `<repo-or-workspace-root>/.secrets/noah-market.env`

期望字段：
- `NOAH_API_BASE_URL`
- `NOAH_MARKET_APIKEY`

不要把 token 写入 `SKILL.md` 或公开文档。

## Request Auth

- 所有业务请求默认使用 Bearer Token：
  - `Authorization: Bearer <NOAH_MARKET_APIKEY>`
- base URL 使用：
  - `NOAH_API_BASE_URL`

## Preflight Checklist

1. 确认 secrets 文件存在。
2. 确认 `NOAH_API_BASE_URL` 非空。
3. 确认 `NOAH_MARKET_APIKEY` 非空。
4. 确认该值是**公司证券行情服务的 API key**，而不是 GitHub token 或其他平台凭证。
5. 若接口报 401/403，提示用户更新本地 API key，而不是把 key 回显到聊天里。
6. 安装后优先执行 `scripts/smoke_test.py` 验证快照、市场状态与 K 线链路是否可用。
7. 单次查询优先走 `scripts/run_query.py`，避免每次重复手写接口调用逻辑。
8. `/security/get_token` 已不再作为当前 market skill 的鉴权流程；统一使用外部配置 Bearer token。

## Error Handling

- `success=false`：优先展示 `msg`。
- 401 / 403：说明 token 无效或权限不足。
- 404：说明标的、数据或市场映射不存在。
- 500：说明服务端异常，建议稍后重试。
- 有订阅限制的接口（如 `/quotes/get_stock_quote`）失败时，优先回退到更通用的快照接口。
