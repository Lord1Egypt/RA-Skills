# 活动商品操作结果查询 — `bg.promotion.activity.goods.operation.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_promotion_activity_goods_operation_query.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.promotion.activity.goods.operation.query`，业务载荷放在 Body 的 `params` |

**Description:** Query promotion goods operation result by draft ID.

> **`draftIdList`** 为必填（来自 enroll/update 返回的 **`draftId`**）。
> Partner **Response Example** 中 **`result`** 为 **OBJECT[]**（非带 `total` 的对象包装）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=product-inventory`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── draftIdList (LONG[], 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| draftIdList | LONG[] | **是** | goods registration activity draft id, which will be generated when the pre-procedure is successfully completed. |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "request": {
    "draftIdList": [
      10001,
      10002
    ]
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表嵌套子行在导出 HTML 中多为折叠状态，下列层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success / errorCode / errorMsg
└── result[]
    ├── draftId (LONG)
    ├── operationStatus (INTEGER)
    ├── failReason (STRING)
    └── goodsId (LONG)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功） |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT 或 OBJECT[] | 业务结果（见下表；**goods.operation.query** 的 `result` 为数组） |

### `result`（OBJECT[]）

Partner Response Example 中 **`result`** 直接为数组。每个元素：

| 参数 | 类型 | 说明 |
|------|------|------|
| draftId | LONG | Draft id |
| operationStatus | INTEGER | Operation status（操作状态码） |
| failReason | STRING | Failure reason |
| goodsId | LONG | goods id |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 220010001 | parameter is illegal | 见 Partner 文档；修正入参或活动状态后重试 |
| 220010002 | system error, please try again later | 见 Partner 文档；修正入参或活动状态后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_promotion_activity_goods_operation_query.py '{"accessToken": "TOKEN", "tokenPurpose": "product-inventory", "request": {"draftIdList": [10001, 10002]}}'
```

**典型流程：** 轮询 [goods.enroll](./bg-promotion-activity-goods-enroll.md) / [goods.update](./bg-promotion-activity-goods-update.md) 提交的 **`draftId`**。
