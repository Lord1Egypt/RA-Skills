# 目录链接接口

用于目录链接、官链、跟卖商品、BSR 和每日数据分析。

## 对应脚本

- 目录链接查询：`scripts/catalog_search.py`（3 个模式：默认 search / 默认 --product-id 进 info / --product-id + --daily 进 daily）

## 接口选择规则

| 接口 | 模式参数 | 何时调用 | 何时不调 |
|---|---|---|---|
| `POST /catalogs/search` | 默认（无 --product-id） | 找官链机会、按关键词/类目筛选 | 只要单链接详情/BSR趋势 |
| `GET /catalog/info` | `--product-id <ID>`（不加 --daily） | 看某目录链接的跟卖结构（followItems）、价格/库存/销量对比 | 只看搜索列表、只看BSR日趋势 |
| `GET /catalog/daily` | `--product-id <ID> --daily` | 看某链接BSR是否稳定、销量/价格变动 | 只看静态详情、只看跟卖结构 |

**组合规则**：用户明确要求"完整分析"才同时调 info+daily；普通选品先 search 筛候选，再按需深挖。

---

## POST /catalogs/search 目录搜索

> ⚡ 每次 **4 积分** ｜ 方法：POST

### 后端接口请求参数（全量）

以下参数后端均接受；`catalog_search.py` 只封装了其中一部分为 CLI（见下表脚注和下一节映射）。

| 必填 | 参数 | 说明 | 脚本已封装 CLI |
|:-:|---|---|:-:|
| ✅ | siteId | `MLM`/`MLB`/`MLC`/`MLA`/`MCO` | ✅ `--site` |
| | pageNo/pageSize | 默认 1/50 | ✅ `--page-no` / `--page-size` |
| | searchText / keySearch | 关键词模糊搜 / 精搜 | ✅ searchText（`--search-text`）；**keySearch 未封装** |
| | categoryId / sellerId / skuId / bland | 类目 / 店铺 / SKU / 品牌 | ✅ `--category-id` / `--seller-id` / `--sku-id` / `--bland` |
| | month | 月份 `YYYYMM`（BSR 相关需要） | ✅ `--month` |
| | sortKey + sortOrder | `bsr`/`sale30`/`price`/`score`/`weight` + `asc`/`desc` | ✅ `--sort-key` / `--sort-order` |
| | priceBegin/End ~ saleStart/End | 价格/评论/评分/BSR/重量/30天销量/总销量/跟卖数/SA 区间 | ❌ **脚本未封装，需手动改脚本 body** |
| | startTimeAdded / startTimeBegin/End | 上架 N 天内 / 上架时间段 `YYYY-MM-DD` | ❌ **同上** |
| | follow / storageType | 跟卖(0/1) / 仓储(`FULL`/`CBT,LOCAL`) | ❌ **同上** |

### CLI 映射（catalog_search.py 已封装部分）

`siteId→--site`，`searchText→--search-text`，`categoryId→--category-id`，`sellerId→--seller-id`，`skuId→--sku-id`，`bland→--bland`，`month→--month`，`sortKey→--sort-key`，`sortOrder→--sort-order`，`pageNo→--page-no`，`pageSize→--page-size`。
详情/每日模式无需 `--info`，直接 `--product-id <ID>`（不加 `--daily`=info，加了=daily）。

```bash
# 例：关键词 phone case + BSR 倒序
python scripts/catalog_search.py --token <TKN> --site MLM --search-text "phone case" --sort-key bsr --sort-order desc

# 目录详情（info 模式：--product-id 不带 --daily）
python scripts/catalog_search.py --token <TKN> --product-id MLM123456789

# 目录每日数据（daily 模式：--product-id + --daily）
python scripts/catalog_search.py --token <TKN> --product-id MLM123456789 --daily
```

### ProductItem 关键字段

销量周期：`sale7 / sale30d / sale60 / sale90`、`sale714 / sale3060`、对应 `gmv*`、`sa*`
通用：`id / title / siteId / categoryId / price / currencyId`、`availableQuantity / soldQuantity`、`bsr / health`、`sellerId / sellerName / sellerType`、`permalink / url`、`picSmall / picBig`、`startTime / dateCreated / lastUpdated`、`catalogListing / isUsaFull`、`productId / familyId`、`rating / shipping / pathFromRoot`

---

## GET /catalog/info 目录详情

> ⚡ 每次 **1 积分** ｜ 必填：`productId`（如 `MLM1072916439`）

CLI：`catalog_search.py --product-id <ID>`

### 关键字段

- 顶层：`productId / siteId / dateCreated / name / permalink / pictures / soldQuantity / status / categoryId / followCount`
- `followItems[]`（跟卖列表）：`id / sellerId / sellerName / price / sale7 / sale30d / availableQuantity / brandId / sellerType`

---

## GET /catalog/daily 每日数据

> ⚡ 每次 **2 积分** ｜ 必填：`productId`

CLI：`catalog_search.py --product-id <ID> --daily`

字段：`date / bsr / soldQuantity / price`

---

## 本模块积分明细表

| 接口 | 功能 | 积分 |
|---|---|---:|
| `POST /catalogs/search` | 目录链接分页列表 | 4 |
| `GET /catalog/daily` | 目录每日历史数据 | 2 |
| `GET /catalog/info` | 目录链接详情 | 1 |
