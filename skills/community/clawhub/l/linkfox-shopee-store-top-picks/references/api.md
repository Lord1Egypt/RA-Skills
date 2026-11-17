# linkfox-shopee-store-top-picks — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **Top Picks 模块**全部 4 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.top_picks.get_top_picks_list](https://open.shopee.com/documents/v2/v2.top_picks.get_top_picks_list?module=100&type=1)

## 通用约定

- **path**：须 `api/v2/top_picks/...`
- **标识**：通常传 **`shopId`**
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.top_picks.{api}?module=100&type=1`

---

## Top Picks 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | add_top_picks | POST | `api/v2/top_picks/add_top_picks` | `add_top_picks.py` | [apis/add-top-picks.md](./apis/add-top-picks.md) |
| 2 | delete_top_picks | POST | `api/v2/top_picks/delete_top_picks` | `delete_top_picks.py` | [apis/delete-top-picks.md](./apis/delete-top-picks.md) |
| 3 | get_top_picks_list | GET | `api/v2/top_picks/get_top_picks_list` | `get_top_picks_list.py` | [apis/get-top-picks-list.md](./apis/get-top-picks-list.md) |
| 4 | update_top_picks | POST | `api/v2/top_picks/update_top_picks` | `update_top_picks.py` | [apis/update-top-picks.md](./apis/update-top-picks.md) |
通用入口：`top_picks_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## 常用接口说明

| API | 要点 |
|-----|------|
| `get_top_picks_list` | 精选商品集合列表 — [apis/get-top-picks-list.md](./apis/get-top-picks-list.md) |
| `add_top_picks` | 创建精选集合；POST `body` — [apis/add-top-picks.md](./apis/add-top-picks.md) |
| `update_top_picks` | 更新精选集合 — [apis/update-top-picks.md](./apis/update-top-picks.md) |
| `delete_top_picks` | 删除精选集合 — [apis/delete-top-picks.md](./apis/delete-top-picks.md) |

---

## curl 示例

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/shopee/developerProxy \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/top_picks/get_top_picks_list",
    "method": "GET",
    "accessToken": "xxx",
    "shopId": "67890"
  }'
```

---

## Feedback API

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-top-picks","sentiment":"POSITIVE",
       "category":"OTHER","content":"Top Picks查询正常"}'
```
