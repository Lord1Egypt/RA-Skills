# get_shopee_ip_ranges

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_shopee_ip_ranges.py` |
| Method / path | GET `api/v2/public/get_shopee_ip_ranges` |
| 官方文档 | [get_shopee_ip_ranges](https://open.shopee.com/documents/v2/v2.public.get_shopee_ip_ranges?module=104&type=1) |
| 用途 | Shopee Open Platform IP ranges for allowlisting |

经 **`POST /shopee/developerProxy`** 转发。Public 多为 Partner / OAuth 级接口，**通常无需** `shopId`/`merchantId`；日常授权优先走 `linkfox-shopee-store-auth`。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 否 | Public 接口通常可省略 |
| `merchantId` | string | 否 | Public 接口通常可省略 |

- Method：**GET**
- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：Shopee Open Platform IP ranges for allowlisting

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_shopee_ip_ranges.py '{}'

# 通用入口
python scripts/public_api.py '{"api": "get_shopee_ip_ranges"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getShopeeIpRanges`**（Shopee `response` 解析结果）
3. 字段以官方文档为准
