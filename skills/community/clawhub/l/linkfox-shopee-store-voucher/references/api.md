# linkfox-shopee-store-voucher — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **Voucher 模块**全部 6 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.voucher.add_voucher](https://open.shopee.com/documents/v2/v2.voucher.add_voucher?module=112&type=1)

## 通用约定

- **path**：须 `api/v2/voucher/...`
- **标识**：通常传 **`shopId`**
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.voucher.{api}?module=112&type=1`

---

## Voucher 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | add_voucher | POST | `api/v2/voucher/add_voucher` | `add_voucher.py` | [apis/add-voucher.md](./apis/add-voucher.md) |
| 2 | delete_voucher | POST | `api/v2/voucher/delete_voucher` | `delete_voucher.py` | [apis/delete-voucher.md](./apis/delete-voucher.md) |
| 3 | end_voucher | POST | `api/v2/voucher/end_voucher` | `end_voucher.py` | [apis/end-voucher.md](./apis/end-voucher.md) |
| 4 | get_voucher | GET | `api/v2/voucher/get_voucher` | `get_voucher.py` | [apis/get-voucher.md](./apis/get-voucher.md) |
| 5 | get_voucher_list | GET | `api/v2/voucher/get_voucher_list` | `get_voucher_list.py` | [apis/get-voucher-list.md](./apis/get-voucher-list.md) |
| 6 | update_voucher | POST | `api/v2/voucher/update_voucher` | `update_voucher.py` | [apis/update-voucher.md](./apis/update-voucher.md) |
通用入口：`voucher_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## 常用接口说明

| API | 要点 |
|-----|------|
| `add_voucher` | 创建店铺优惠券；POST `body` — [apis/add-voucher.md](./apis/add-voucher.md) |
| `get_voucher_list` | 优惠券列表 — [apis/get-voucher-list.md](./apis/get-voucher-list.md) |
| `get_voucher` | 优惠券详情 — [apis/get-voucher.md](./apis/get-voucher.md) |
| `update_voucher` | 更新优惠券 — [apis/update-voucher.md](./apis/update-voucher.md) |
| `end_voucher` | 提前结束 — [apis/end-voucher.md](./apis/end-voucher.md) |
| `delete_voucher` | 删除优惠券 — [apis/delete-voucher.md](./apis/delete-voucher.md) |

---

## curl 示例

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/shopee/developerProxy \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/voucher/get_voucher_list",
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
  -d '{"skillName":"linkfox-shopee-store-voucher","sentiment":"POSITIVE",
       "category":"OTHER","content":"优惠券查询正常"}'
```
