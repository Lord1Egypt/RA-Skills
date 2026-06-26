# 批量查发布状态 — `bg.local.goods.publish.status.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_manage_publish_status_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=1d70452c1eba40a2b2382fb08833ae4e |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.publish.status.get`，业务载荷放在 Body 的 `params` |

**Description:** Batch Query Product Publication Status.

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── goodsIdList[]    ← 必填
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsIdList | LONG[] | **是** | Goods Id List |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "goodsIdList": [123456, 123457]
  }
}
```

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result
    └── goodsPublishStatusList[]
        ├── goodsId
        ├── status
        └── subStatus
```

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | Current request success status |
| errorCode | INTEGER | Error code |
| errorMsg | STRING | Error message |
| result | OBJECT | result |
| result.goodsPublishStatusList | OBJECT[] | List of product publish status data |

### `result.goodsPublishStatusList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | Goods ID |
| status | INTEGER | Status |
| subStatus | INTEGER | Sub-status |

> **勿**使用旧字段名 `publishStatusList`、`publishStatus`、`rejectReason`、`siteStatusList`（官方为 `goodsPublishStatusList` + `status` / `subStatus`）。

---

## 示例

```bash
python scripts/global_manage_publish_status_get.py '{
  "accessToken": "TOKEN",
  "request": {
    "goodsIdList": [123456, 789012]
  }
}'
```
