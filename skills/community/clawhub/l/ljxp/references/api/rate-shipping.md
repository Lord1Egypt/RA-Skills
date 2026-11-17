# 汇率与运费接口

用于汇率换算、运费查询和利润测算。

## 对应脚本

- **优先**：通过 `scripts/get_item_info.py`（`/item/info`）返回的 `rateSite` / `rateRmb` / `weightInfo` 子对象直接读取（90% 场景够用，无需额外请求）
- **单独调用**：用 `scripts/utils.py` 组装请求（无独立封装脚本）
- **利润测算**：先用 `get_item_info.py` 内置字段，自定义重量/售价时再用 `utils.py` 补查

## 接口选择规则

| 接口 | 何时单独调用 | 何时**不**单独调用（直接复用） |
|---|---|---|
| `GET /rate/{siteId}` | 用户只问汇率、无商品上下文 | 已查过 `/item/info` 且有 `rateSite/rateRmb`，直接复用 |
| `GET /cost/weight/list/cbt` | 需自发货运费重量列表 | `/item/info.weightInfo.finalFreight` 够用 |
| `GET /cost/weight/filter` | 自定义重量/价格/卖家等级精算运费 | `/item/info.weightInfo.finalFreight` 够用且无自定义参数 |

**组合调用**：利润测算先用 `/item/info` 拿 价格+重量+币种+店铺类型+佣金+`rateSite/rateRmb`+`weightInfo.finalFreight`；**只有**用户自定义采购成本/重量/售价/卖家等级，或 info 无 `weightInfo` 时，才补调汇率和运费。**不要默认全查**。

---

## GET /rate/{siteId} 汇率

> ⚡ 每次 **1 积分** ｜ 必填：`siteId`（路径参数）｜ 方法：GET

字段：`usdRate`（美金汇率）/ `cnyRate`（人民币汇率）/ `updateDate`

---

## GET /cost/weight/list/cbt 自发货运费列表

> ⚡ 每次 **8 积分** ｜ 方法：GET

---

## GET /cost/weight/filter 运费查询

> ⚡ 每次 **1 积分** ｜ 方法：GET

### 请求参数（list/cbt 不需要 weight；filter 必填 weight）

| 必填 | 参数 | 说明 |
|:-:|---|---|
| ✅ | siteId | `MLM`/`MLB`/`MLC`/`MLA`/`MCO` |
| ✅ | sellerLevel | `platinum` / `gold` / `silver` |
| ✅(filter) | weight | 商品重量 kg |
| ✅ | price | 商品售价，匹配价格区间 |
| | country | 国家（一般省略，siteId 自带） |

### WeightData 关键字段

`id / siteId / fromWeight~toWeight（kg）/ fromPrice~toPrice / sellerLevel / value（运费）`

---

## 本模块积分明细表

| 接口 | 功能 | 积分 |
|---|---|---:|
| `GET /cost/weight/list/cbt` | 自发货运费重量列表 | 8 |
| `GET /cost/weight/filter` | 运费查询 | 1 |
| `GET /rate/{siteId}` | 站点汇率查询 | 1 |
