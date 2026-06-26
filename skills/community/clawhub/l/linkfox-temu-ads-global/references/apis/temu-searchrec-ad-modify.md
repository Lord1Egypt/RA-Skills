# 修改广告 — `temu.searchrec.ad.modify`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_ads_searchrec_ad_modify.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.searchrec.ad.modify`，业务载荷放在 Body 的 `params` |

**Description:** Modify ads (delete, pause, budget, ROAS, etc.).

> **`status`**、**`modifyAdDTO`** 均为必填；**`status`** 决定 **`modifyAdDTO`** 中哪些字段生效。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=product-inventory`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── modifyAdDTO (OBJECT, 必填)
    │   ├── goodsId (LONG, 必填)
    │   ├── budget (LONG, 否)
    │   └── roas (LONG, 否)
    └── status (INTEGER, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| modifyAdDTO | OBJECT | **是** | ModifyAdDTO request body |
| status | INTEGER | **是** | Modification type: 1:delete, 2:pause, 3:open, 4:modify budget, 5:modify roas |

#### `status`（必填）

| 值 | 说明 |
|----|------|
| `1` | delete |
| `2` | pause |
| `3` | open |
| `4` | modify budget |
| `5` | modify roas |

#### `modifyAdDTO`（OBJECT，必填）

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | Goods id（必填） |
| budget | LONG | New budget（`status=4` 时使用） |
| roas | LONG/NUMBER | New ROAS（`status=5` 时使用） |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "request": {
    "status": 4,
    "modifyAdDTO": {
      "goodsId": 100001,
      "budget": 8000,
      "roas": 400
    }
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 嵌套子行在导出 HTML 中多为折叠状态，下列层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success / errorCode / errorMsg
└── result
    ├── successModifyProductNum (INTEGER)
    └── modifyGoodsRespList[]
        ├── goodsId, reason, success
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT 或 OBJECT[] | 业务结果（见下表） |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| successModifyProductNum | INTEGER | Number of successfully modified products |
| modifyGoodsRespList | OBJECT[] | Per-goods modify result |

#### `modifyGoodsRespList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | Goods id |
| reason | STRING | Failure reason（失败时） |
| success | BOOLEAN | Whether modify succeeded |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 230012000 | bad query params | 见 Partner 文档；修正入参或权限后重试 |
| 230012003 | unmatch mall and goods | 见 Partner 文档；修正入参或权限后重试 |
| 230013000 | business exception | 见 Partner 文档；修正入参或权限后重试 |
| 230014000 | system exception | 见 Partner 文档；修正入参或权限后重试 |
| 230016701 | has no permission | 见 Partner 文档；修正入参或权限后重试 |
| 230016103 | not signed because of not main account | 见 Partner 文档；修正入参或权限后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_ads_searchrec_ad_modify.py '{"accessToken": "TOKEN", "tokenPurpose": "product-inventory", "request": {"status": 4, "modifyAdDTO": {"goodsId": 100001, "budget": 8000, "roas": 400}}}'
```

**典型流程：** 按 **`status`** 删除/暂停/开启/改预算/改 ROAS。
