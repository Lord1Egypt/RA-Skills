# set_shop_holiday_mode

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/set_shop_holiday_mode.py` |
| Method / path | POST `api/v2/shop/set_shop_holiday_mode` |
| 官方文档 | [set_shop_holiday_mode](https://open.shopee.com/documents/v2/v2.shop.set_shop_holiday_mode?module=92&type=1) |
| 用途 | true=enable holiday mode (blocks new orders) |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `holiday_mode_on` | — | 是 | 见 notes / 官方文档 |

- Method：**POST**
- POST：传 `body` / `requestBody`，或把 `body_fields` 列在 JSON 顶层
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：true=enable holiday mode (blocks new orders)

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/set_shop_holiday_mode.py '{"shopId": "67890", "holiday_mode_on": true}'

# 通用入口
python scripts/shop_api.py '{"api": "set_shop_holiday_mode", "shopId": "67890", "holiday_mode_on": true}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`setShopHolidayMode`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.shop.set_shop_holiday_mode?module=92&type=1)

**Body（必填）**：`holiday_mode_on`（boolean）— `true` 开启假期模式（买家无法下单）

---

## 网关错误码

| errcode | 含义 | 建议 |
|---------|------|------|
| 1002 | 参数/未登录 | 检查 shopId 与 API Key |
| 1003 | 代理/网络异常 | 重试 |
| 1004 | 无授权记录 | auth skill |
| 1005 | path 未白名单 | 确认 `api/v2/shop/...` |

---
