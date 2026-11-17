# 商品接口

用于商品搜索、详情、评价、每日/月度数据、流量词反查。

## 对应脚本

- 商品搜索：`scripts/search_items.py`
- 商品详情/每日/月度/评价/流量词：`scripts/get_item_info.py`（用参数切换，默认 info）
  - `--daily`｜`--monthly`｜`--reviews`｜`--keywords`｜`--all`（5个全查，仅用户明确要"完整拆解"才用）

## 接口选择规则

| 脚本                              | 接口                          | 何时调用                                            | 何时不调          |
| ------------------------------- | --------------------------- | ----------------------------------------------- | ------------- |
| search\_items.py                | `POST /items/search`        | 找商品、竞品列表、按条件筛选商品、某类目/店铺商品                       | 只要单商品详情/评价/趋势 |
| get\_item\_info.py 默认           | `GET /item/info`            | 单商品详情（价格/店铺/类目/物流/佣金/变体/评分）。**用户没指定查哪方面优先只查这个** | 只要评价/价格走势/流量词 |
| get\_item\_info.py `--daily`    | `GET /item/daily`           | 最近 7/14/30 天销量/价格/库存/访问波动                       | 只看静态/月度       |
| get\_item\_info.py `--monthly`  | `GET /item/monthly`         | 长期趋势、月度表现、季节性、月度 GMV                            | 只看最近几天/静态     |
| get\_item\_info.py `--reviews`  | `GET /item/review`          | 差评原因、口碑、产品优缺点、用户反馈                              | 只要销量价格、不要文字评论 |
| get\_item\_info.py `--keywords` | `GET /item/keyword/reverse` | 关键词、流量来源、标题优化、竞品投词                              | 只要基础信息、不要关键词  |

**组合规则**：只有明确要"完整竞品拆解/全量分析"才 `--all`；普通详情优先 info，追问再补。先 search 锁商品池，再对个别商品深挖，不要对每个搜索结果都跑 5 个接口。

***

## POST /items/search 商品搜索

> ⚡ 每次 **5 积分** ｜ 方法：POST

### 请求参数

|   必填   | 参数组    | 说明                                                                                                                        |
| :----: | ------ | ------------------------------------------------------------------------------------------------------------------------- |
|    ✅   | siteId | `MLM`/`MLB`/`MLC`/`MLA`/`MCO`，默认 `MLM`                                                                                    |
| <br /> | 分页     | pageNo（1）/ pageSize（50）                                                                                                   |
| <br /> | 定位条件   | sellerId（店铺ID）、title（标题关键词）、categoryId（类目ID）、skuId                                                                        |
| <br /> | 卖家/仓储  | storageType（`FULL`/`CBT,LOCAL`）、sellerType（`LOCAL`本土/`CBT`跨境）、isUsaFull（美国转运仓，**脚本默认 false**，传 `--is-usa-full true` 才开启）  |
| <br /> | 跟卖/时间  | follow（0=非/1=跟卖）、startTimeAdded（15/30/60/90/180/365 天内上架）、startTimeBegin/End（`YYYY-MM-DD`）、itemStatus（`active`/`paused`）  |
| <br /> | 数值区间   | priceBegin/End、commentBegin/End、soldTotalBegin/End、sale30Start/End、sale30RangeStart/End、weightStart/End（g）、scoreStart/End |
| <br /> | 排序     | sortKey（`sale7`/`sale30`/`saleTotal`/`amount30`）+ sortOrder（`asc`/`desc`）                                                 |

### CLI 映射

`siteId→--site`，`sellerId→--seller-id`，`categoryId→--category-id`，`title→--title`，`sortKey→--sort-key`，`sortOrder→--sort-order`，`pageSize→--page-size`，其他参数驼峰转 `--kebab-case`。Token 二选一：`--token xxx` 或 `LJXP_TOKEN` 环境变量（下同）。

```bash
# 例：墨西哥本土、phone case、30天销量倒序、价格 100~500
python scripts/search_items.py --token <TKN> --site MLM --seller-type LOCAL \
  --title "phone case" --sort-key sale30 --sort-order desc --price-begin 100 --price-end 500
```

### ItemDetail 关键字段

- 基本：`id / title / titleCn / price / priceUsd / basePrice / currencyId / itemStatus / permalink / categoryId / brandId`
- 店铺：`sellerId / sellerName / sellerLevel / sellerType（LOCAL/CBT）/ sellerTotal`
- 时间：`dateCreated / startTime / lastUpdated`
- 库存销量：`availableQuantity / soldQuantity / variationsCount / freeShipping / bsr / health / isUsaFull / catalogListing / productId`
- 销售周期：`sale7 / gmv7 / sale30 / gmv30 / visit30 / sale60 / gmv60 / sale90 / gmv90 / visitTotal`（对应间隔期：`sale714 / sale3060`）
- 物流图片：`picBig / picSmall / logisticType / packetWeight`
- 子对象：`shipping.mode/freeShipping/logisticType/tags`｜`rating.amount/stars`｜`pathFromRoot[].name/id`

***

## GET /item/info 商品详情

> ⚡ 每次 **1 积分** ｜ 必填：`itemId`｜可选：`productId`（目录链接ID）

CLI：`get_item_info.py --item-id <ID> [--product-id <ID>]`

### ItemInfoData 关键字段

- 基本：`id / siteId / title / categoryId / categoryName / categoryNameZn / price / avgPrice / minPrice / maxPrice / currencyId / brandId`
- 销售：`sale7/sale30/sale60/sale90 + 对应 gmv*`、`saleRate7/saleRate30`、`visitTotal`
- 库存状态：`availableQuantity / soldQuantity / itemStatus / variationsCount / startTime / health / packetWeight`
- 其他：`url / picSmall/picBig / catalogListing / cbtItem / isUsaFull / sellerName / logisticType / saleFeeAmount（佣金）`
- 子对象：`rating.amount/stars`｜`pathFromRoot[].name/id`｜`shipping.mode/freeShipping/logisticType/tags`｜`variations[].id/availableQuantity/price/sale30/attrs`｜`sellerInfo.id/name/permalink/sellerType/saleTotal/itemTotal/brands/registrationDate`｜`rateSite / rateRmb（汇率）`｜`weightInfo.finalFreight / weight / additionalCost（运费）`

***

## GET /item/review 商品评价

> ⚡ 每次 **1 积分** ｜ 必填：`itemId`

**后端原生支持**：`pageNo`（默认 1）/ `pageSize`（默认 20）。
**脚本封装现状**：`get_item_info.py` 内部固定 `pageNo=1, pageSize=20`，**未暴露 CLI 参数**；需要翻页或改大小时手动修改脚本中的请求体（或直接调用 utils.py 发请求）。

CLI：`get_item_info.py --item-id <ID> --reviews`（脚本固定取第 1 页 20 条）

字段：`reviewList[].itemId / productId / content / contentZh / rate / createTime`

***

## GET /item/daily 每日数据

> ⚡ 每次 **2 积分** ｜ 必填：`itemId`｜可选：`productId`

CLI：`get_item_info.py --item-id <ID> --daily`

字段：`date / availableQuantity / currencyId / price / soldQuantity / visit`

***

## GET /item/monthly 每月数据

> ⚡ 每次 **2 积分** ｜ 必填：`itemId`｜可选：`productId`

CLI：`get_item_info.py --item-id <ID> --monthly`

字段：`month / amount / currencyId / soldQuantity / visit`

***

## GET /item/keyword/reverse 流量词反查

> ⚡ 每次 **2 积分** ｜ 必填：`itemId`

CLI：`get_item_info.py --item-id <ID> --keywords`（或 `--all` 组合全查）

关键字段：

- `itemInfo`: `id / title / price / sale30 / siteId / rating.stars / visit30 / picSmall / url`
- `keyList[]`: `key / keyCn / totalItem / keyCount / sale30 / bgl / ranking / visit30 / runDate / history`

***

## 本模块积分明细表

| 接口                          | 功能      | 积分 |
| --------------------------- | ------- | -: |
| `POST /items/search`        | 商品分页查询  |  5 |
| `GET /item/daily`           | 商品每日历史  |  2 |
| `GET /item/monthly`         | 商品每月历史  |  2 |
| `GET /item/keyword/reverse` | 商品流量词反查 |  2 |
| `GET /item/info`            | 商品详情概要  |  1 |
| `GET /item/review`          | 商品评价    |  1 |

