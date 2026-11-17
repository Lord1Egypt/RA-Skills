# get_stock_aging

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_stock_aging.py` |
| Method / path | GET `api/v2/sbs/get_stock_aging` |
| 官方文档 | [get_stock_aging](https://open.shopee.com/documents/v2/v2.sbs.get_stock_aging?module=124&type=1) |
| 用途 | Stock aging report |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |

- Method：**GET**
- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：Stock aging report

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_stock_aging.py '{"shopId": "67890"}'

# 通用入口
python scripts/sbs_api.py '{"api": "get_stock_aging", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getStockAging`**（Shopee `response` 解析结果）
3. 字段以官方文档为准
