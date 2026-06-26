# 删除商品 — `temu.local.goods.delete`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_manage_goods_delete.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=d651ab650f3546fea22874a9d758ffe4 |
| **网关** | `POST /temu/proxy`，`type`=`temu.local.goods.delete`，业务载荷放在 Body 的 `params` |

**Description:** Product deletion.

---

## Request（`params`）

与同族接口一致，业务字段建议放在 **`request`** 下（`goodsId` 为必填，以 Partner 入参页为准）：

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456
  }
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| request | OBJECT | 否 | 请求体 |
| request.goodsId | LONG | **是** | 待删除商品 ID |

---

## Response（Temu `body` 解析后）

```text
response
├── success              ← 整单请求是否成功
├── errorCode
├── errorMsg
└── result               ← Specific information
    ├── success          ← delete result（删除操作结果）
    └── errorMsg         ← error message（删除失败时的说明）
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | Whether it was successful or not（**顶层**，整单请求） |
| errorCode | INTEGER | Error code |
| errorMsg | STRING | Error message（**顶层**） |
| result | OBJECT | Specific information |
| result.success | BOOLEAN | delete result（**业务层**删除是否成功） |
| result.errorMsg | STRING | error message（**业务层**删除相关说明） |

> 注意区分两层 `success`：**顶层**表示 API 调用是否成功；**`result.success`** 表示商品删除操作本身是否成功。`result` 下**无** `errorCode` 字段（以官方文档为准）。

---

## 示例

```bash
python scripts/eu_manage_goods_delete.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsId": 123456
  }
}'
```
