# 创建广告 — `temu.searchrec.ad.create`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_ads_searchrec_ad_create.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.searchrec.ad.create`，业务载荷放在 Body 的 `params` |

**Description:** Create search recommendation ads.

> **`createAdReqs`** 为必填；子字段在 Partner 表中为折叠行，按 **Request Example** 展开。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=product-inventory`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── createAdReqs[] (OBJECT[], 必填)
        ├── goodsId (LONG, 必填)
        ├── budget (LONG, 必填)
        ├── roas (LONG, 必填)
        └── roasType (INTEGER, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| createAdReqs | OBJECT[] | **是** | CreateAd parameter |

#### `createAdReqs[]`（Request Example 展开）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsId | LONG | 是 | Goods id |
| budget | LONG | 是 | Ad budget（广告预算） |
| roas | LONG/INTEGER | 是 | Target ROAS（目标 ROAS） |
| roasType | INTEGER | 是 | ROAS type（ROAS 类型；具体枚举以 Partner 文档为准） |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "request": {
    "createAdReqs": [
      {
        "goodsId": 100001,
        "budget": 5000,
        "roas": 350,
        "roasType": 1
      }
    ]
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
    ├── alreadyCreatedGoodsNum (INTEGER)
    ├── successCreateProductNum (INTEGER)
    ├── successGoodsIdLists[] (LONG)
    ├── createGoodsFailMap (OBJECT)
    └── createGoodsFailObjList[]
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
| alreadyCreatedGoodsNum | INTEGER | Number of goods that already had ads created |
| successCreateProductNum | INTEGER | Number of successfully created ad products |
| successGoodsIdLists | LONG[] | Successfully created goods id list |
| createGoodsFailMap | OBJECT | Fail map（Example 键为 `$key`/`$value`，表示失败 goodsId → 原因） |
| createGoodsFailObjList | OBJECT[] | Fail list with details |

#### `createGoodsFailObjList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | Goods id |
| reason | STRING | Failure reason |
| success | BOOLEAN | Whether succeeded（Example 中存在，以实际返回为准） |

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
python scripts/eu_ads_searchrec_ad_create.py '{"accessToken": "TOKEN", "tokenPurpose": "product-inventory", "request": {"createAdReqs": [{"goodsId": 100001, "budget": 5000, "roas": 350, "roasType": 1}]}}'
```

**典型流程：** 可先 [goods.create.query](./temu-searchrec-ad-goods-create-query.md) 确认可投 → [roas.pred](./temu-searchrec-ad-roas-pred.md) 预估 → 本接口创建。
