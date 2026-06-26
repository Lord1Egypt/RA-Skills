# 广告 ROAS 预测 — `temu.searchrec.ad.roas.pred`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_ads_searchrec_ad_roas_pred.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=dfff26bad8e94ed5abaaf5cdade50c26 |
| **网关** | `POST /temu/proxy`，`type`=`temu.searchrec.ad.roas.pred`，业务载荷放在 Body 的 `params` |

**Description:** Predict ad ROAS for goods.

> **`goodsInfoList`** 为必填。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=product-inventory`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── goodsInfoList (OBJECT[], 必填)
    ├── goodsInfoList[] (OBJECT[], 必填)
    └──     └── goodsId (LONG, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsInfoList | OBJECT[] | **是** | Goods information list |

#### `goodsInfoList[]`（Request Example 展开）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsId | LONG | 是 | Goods id |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "request": {
    "goodsInfoList": [
      {
        "goodsId": 100001
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
    └── queryAdBidResult[]
        ├── goodsId (LONG)
        └── predList[]
            └── roas (STRING)
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
| queryAdBidResult | OBJECT[] | Query ad bid / ROAS prediction results |

#### `queryAdBidResult[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | Goods id |
| predList | OBJECT[] | Prediction list |

#### `predList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| roas | STRING | Predicted ROAS value（Partner Example 为字符串） |

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
python scripts/us_ads_searchrec_ad_roas_pred.py '{"accessToken": "TOKEN", "tokenPurpose": "product-inventory", "request": {"goodsInfoList": [{"goodsId": 100001}]}}'
```

**典型流程：** 创建广告前可用本接口预估 ROAS → [ad.create](./temu-searchrec-ad-create.md)。
