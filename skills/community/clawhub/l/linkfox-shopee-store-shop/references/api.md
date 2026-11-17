# linkfox-shopee-store-shop — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **Shop 模块**全部 9 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.shop.get_shop_info](https://open.shopee.com/documents/v2/v2.shop.get_shop_info?module=92&type=1)

## 通用约定

- **Base URL**：`https://tool-gateway.linkfox.com`
- **Method**：POST（网关），上游 Method 见各接口
- **Auth**：Header `Authorization: <api_key>`（`LINKFOXAGENT_API_KEY`）
- **流程**：`POST /shopee/storeTokens` → `POST /shopee/developerProxy`
- **path**：须 `api/v2/shop/...`
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.shop.{api}?module=92&type=1`

---

## Shop 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | get_shop_info | GET | `api/v2/shop/get_shop_info` | `get_shop_info.py` | [apis/get-shop-info.md](./apis/get-shop-info.md) |
| 2 | get_profile | GET | `api/v2/shop/get_profile` | `get_profile.py` | [apis/get-profile.md](./apis/get-profile.md) |
| 3 | update_profile | POST | `api/v2/shop/update_profile` | `update_profile.py` | [apis/update-profile.md](./apis/update-profile.md) |
| 4 | get_warehouse_detail | GET | `api/v2/shop/get_warehouse_detail` | `get_warehouse_detail.py` | [apis/get-warehouse-detail.md](./apis/get-warehouse-detail.md) |
| 5 | get_shop_notification | GET | `api/v2/shop/get_shop_notification` | `get_shop_notification.py` | [apis/get-shop-notification.md](./apis/get-shop-notification.md) |
| 6 | get_authorised_reseller_brand | GET | `api/v2/shop/get_authorised_reseller_brand` | `get_authorised_reseller_brand.py` | [apis/get-authorised-reseller-brand.md](./apis/get-authorised-reseller-brand.md) |
| 7 | get_br_shop_onboarding_info | GET | `api/v2/shop/get_br_shop_onboarding_info` | `get_br_shop_onboarding_info.py` | [apis/get-br-shop-onboarding-info.md](./apis/get-br-shop-onboarding-info.md) |
| 8 | get_shop_holiday_mode | GET | `api/v2/shop/get_shop_holiday_mode` | `get_shop_holiday_mode.py` | [apis/get-shop-holiday-mode.md](./apis/get-shop-holiday-mode.md) |
| 9 | set_shop_holiday_mode | POST | `api/v2/shop/set_shop_holiday_mode` | `set_shop_holiday_mode.py` | [apis/set-shop-holiday-mode.md](./apis/set-shop-holiday-mode.md) |

通用入口：`shop_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## Feedback API

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-shop","sentiment":"POSITIVE",
       "category":"OTHER","content":"店铺信息查询正常"}'
```
