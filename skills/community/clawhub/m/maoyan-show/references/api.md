# 猫眼演出 H5 API 使用规范

目标站点：`https://show.maoyan.com/qqw#/`

更新时间：2026-05-28

## 基础约定

### API 分组

猫眼演出 H5 当前有两组公开展示接口，公共参数放置方式不同，不能混用。

| 分组 | 基址 | 公共参数位置 | 适用接口 |
|---|---|---|---|
| 普通 ajax | `https://show.maoyan.com/maoyansh/myshow/ajax` | URL query | 详情、场次、城市、场馆、推荐、榜单、日历 |
| 频道 ianvs | `https://show.maoyan.com/my/ianvs` | headers，少量业务参数在 query/body | 品类频道模块、`wonderfulPerformances`、筛选项 |

默认值：

| 参数 | 默认策略 |
|---|---|
| `sellChannel` | 除非用户指定渠道，否则使用 `13`，与入口 `/qqw` 保持一致 |
| `clientPlatform` | 除非用户指定平台，否则普通 ajax query 使用 `3`；ianvs query 使用 `3`，header 使用 `pc` |
| `cityId` | 除非用户指定，否则首次需要城市时询问用户，并在后续请求中复用 |
| `lat`, `lng` | 仅在用户提供或场景需要距离/定位时传 |
| `uuid` | 可不传；如实现需要，可生成 UUID v4 并在一次任务内复用 |
| `token` | 公开数据抓取不使用登录 token，ianvs header 可传空字符串 |
| `optimus_risk_level`, `optimus_code` | 默认不主动传；如运行时观察到前端补全，则记录并在后续请求复用 |

渠道入口：

- `https://show.maoyan.com/qqw#/` 中的 `qqw` 对应 QQ 钱包渠道，渠道配置为 `appName=qqwallet`、`sellChannel=13`、`hostPrefix=//show.maoyan.com/qqw`。
- 美团渠道配置为 `appName=meituan`，默认 `sellChannel=2`；当 URL query/hash 中 `sourceType=1` 时为 `sellChannel=34`。
- 当前前端配置中没有发现类似 `qqw` 的美团专用 path 标识。为避免入口 path 和渠道参数不一致，skill 默认使用 QQ 钱包入口对应的 `sellChannel=13`。只有用户明确指定美团渠道时，才使用 `sellChannel=2` 或 `34`。

普通 ajax 默认 headers：

```http
Referer: https://show.maoyan.com/qqw#/
User-Agent: Mozilla/5.0
Accept: application/json,text/plain,*/*
```

ianvs 默认 headers：

```http
Referer: https://show.maoyan.com/qqw#/
Origin: https://show.maoyan.com
User-Agent: Mozilla/5.0
Accept: application/json,text/plain,*/*
sellChannel: 13
cityId: {cityId}
token:
uuid: {uuid}
clientPlatform: pc
Content-Type: application/json
```

## 城市处理

当用户请求搜索、推荐、日历、场馆附近、榜单或其他城市相关能力时：

1. 如果用户已经提供 `cityId`，直接使用。
2. 如果用户提供城市名称，优先使用已知城市映射；没有映射时询问用户确认城市或提供经纬度。
3. 如果用户提供经纬度，调用城市反查接口获取 `cityId`。
4. 如果用户没有提供城市信息，首次需要城市时必须询问用户；得到后在本次任务中复用。

城市反查接口：

```http
GET /city/queryMTCity?lat={lat}&lng={lng}&sellchannel={sellChannel}&t={timestamp}
```

示例：

```bash
curl 'https://show.maoyan.com/maoyansh/myshow/ajax/city/queryMTCity?lat=22.5431&lng=114.0579&sellchannel=13&t=1779958000000'
```

返回字段：

| 字段 | 说明 |
|---|---|
| `data.id` | 城市 ID |
| `data.nm` | 城市名 |
| `data.py` | 拼音 |

深圳示例：`data.id=30`、`data.nm=深圳`、`data.py=shenzhen`。

重要限制：`/my/ianvs/categoryChannel/wonderfulPerformances` 直连时即使 header 中切换 `cityId`，也可能继续返回默认城市/当前上下文城市数据。skill 不能把该接口当成可靠的跨城市列表源；使用时必须检查返回项的 `cityName`，不匹配目标城市则丢弃或改用其他可验证数据源。

## 分类处理

入口路由：

```text
https://show.maoyan.com/qqw#/list/{categoryId}?labelId={labelId}
```

含义：

- `{categoryId}` 是演出一级分类 ID。
- `labelId` 是频道标签/子入口，默认 `0` 表示不额外筛选具体标签。
- 亲子演出入口为 `https://show.maoyan.com/qqw#/list/7?labelId=0`，即 `categoryId=7`、`labelId=0`。

分类导航接口：

```http
GET /performance/navigation?cityId={cityId}&sellChannel={sellChannel}&clientPlatform={clientPlatform}
```

用途：获取完整一级分类 ID 和名称映射。

当前一级分类映射：

| `categoryId` | 分类名 |
|---:|---|
| `0` | 全部 |
| `1` | 演唱会 |
| `2` | 体育赛事 |
| `3` | 戏曲艺术 |
| `4` | 话剧音乐剧 |
| `5` | 舞蹈芭蕾 |
| `6` | 音乐会 |
| `7` | 亲子演出 |
| `8` | 其他 |
| `9` | 休闲展览 |
| `10` | 音乐节 |
| `12` | 电竞赛事 |
| `13` | 剧本杀 |
| `14` | 沉浸剧场 |
| `15` | 脱口秀 |
| `16` | 相声 |
| `17` | Livehouse |

## 已验证可用接口

### 城市反查

```http
GET /city/queryMTCity
```

参数：

| 参数 | 必填 | 说明 |
|---|---|---|
| `lat` | 是 | 纬度 |
| `lng` | 是 | 经度 |
| `sellchannel` | 否 | 默认 `13`，注意字段名为小写 `sellchannel` |
| `t` | 否 | 毫秒时间戳 |

用途：根据经纬度获取城市 ID。深圳经纬度示例返回 `id=30`。

### 演出详情

```http
GET /v2/performance/{performanceId};supportNewPromotion=false
```

必要前置：`performanceId`。

用途：获取演出主数据、价格摘要、场馆、购票规则。

普通 ajax 公共参数放在 query 中：

```bash
curl 'https://show.maoyan.com/maoyansh/myshow/ajax/v2/performance/371188;supportNewPromotion=false?sellChannel=13&clientPlatform=3' \
  -H 'Referer: https://show.maoyan.com/qqw#/' \
  -H 'User-Agent: Mozilla/5.0'
```

关键字段：

| 字段 | 说明 |
|---|---|
| `performanceId` | 演出 ID |
| `name`, `shortName` | 演出名称 |
| `categoryId` | 分类 ID |
| `cityId`, `cityName` | 城市 |
| `shopId`, `shopName` | 场馆 |
| `address`, `lat`, `lng` | 场馆地址和坐标 |
| `posterUrl` | 海报 |
| `showTimeRange` | 演出时间文本 |
| `lowestPrice` | 最低价 |
| `priceList`, `sellPriceList` | 价格列表 |
| `ticketPriceList` | 票价明细，可能为空 |
| `saleStatus`, `ticketStatus`, `stockOut` | 售卖状态 |
| `seatType`, `seatUrl` | 座位相关信息 |
| `detail` | 详情 HTML |
| `ticketNotes` | 购票须知 HTML |
| `serviceTitleList` | 官方票、电子票、退票政策等说明 |
| `needRealName`, `needFaceCheck` | 实名和人脸校验要求，仅作展示，不进入实名接口 |
| `shareLink`, `shareTitle` | 分享信息 |

### 演出场次和票档

```http
GET /v2/performance/{performanceId}/shows/1;supportNewPromotion=false
```

必要前置：`performanceId`。最佳实践是先调用演出详情接口，读取 `saleStatus`、`ticketStatus`、`stockOut`，再决定是否查询票档。

返回为空数组时，表示当前渠道下无可展示票档，常见原因是已结束、售罄、未开票或不可售。

### 搜索/普通列表

```http
GET /performances/search
GET /performances/list
```

必要前置：`cityId`。

用途：返回城市下公开演出列表，可用于补充候选池。当前验证中 `keyword`、`categoryId` 等过滤参数不稳定，不应作为精确搜索或精确分类列表的唯一依据。

参数：

| 参数 | 说明 |
|---|---|
| `cityId` | 城市 ID |
| `keyword` | 搜索词，可能不生效，调用方必须对返回标题二次过滤 |
| `categoryId` | 分类 ID，可能不生效，调用方必须对返回 `categoryId` 二次过滤 |
| `pageNo` | 页码 |
| `pageSize` | 每页数量，接口可能按服务端默认返回 |
| `sellChannel` | 渠道 |
| `clientPlatform` | 平台 |
| `uuid` | 可选 |

处理要求：

- 只保留 `cityName` 或 `cityId` 匹配目标城市的结果。
- 如果用户指定关键词，必须对 `name` / `shortName` 做本地匹配。
- 如果用户指定分类，必须对返回 `categoryId` 做本地过滤。
- 需要完整价格、场馆或购票规则时，继续调用详情接口。

### 分类频道列表

```http
POST https://show.maoyan.com/my/ianvs/categoryChannel/wonderfulPerformances
```

用途：对应 `#/list/{categoryId}` 分类频道页，返回频道模块中的演出项目、榜单/推荐卡片。

必要前置：`categoryId`。如果用户指定城市，也需要先确定 `cityId`，但直连接口不保证按 header `cityId` 切换城市，必须检查返回项城市。

请求约定：

- 不要把 `cityId`、`sellChannel`、`uuid`、`optimus_risk_level`、`optimus_code` 作为 URL query 公共参数传给该接口；这样会触发 OpenResty `403 Forbidden`。
- 公共值放在 headers：`sellChannel`、`cityId`、`token`、`uuid`、`clientPlatform: pc`。
- query 最多保留 `clientPlatform=3`；`optimus_risk_level=71&optimus_code=10` 可在前端运行时自动补全后复用，但默认不传。
- body 使用 JSON。

请求体：

```json
{
  "pageNo": 1,
  "pageSize": 20,
  "categoryId": 7,
  "sortType": 2,
  "startTime": null,
  "endTime": null,
  "currentCity": true,
  "celebrityFilterIdList": null,
  "quickFilterIdList": []
}
```

参数：

| 参数 | 说明 |
|---|---|
| `pageNo` | 页码 |
| `pageSize` | 每页数量，前端默认 `20` |
| `categoryId` | 分类 ID；亲子演出为 `7` |
| `sortType` | 排序；前端分类页常用 `2` |
| `startTime`, `endTime` | 毫秒时间戳，按演出开始时间筛选；不筛选时为 `null` |
| `currentCity` | `true` 表示当前城市语义，直连时仍需校验返回城市 |
| `celebrityFilterIdList` | 艺人筛选；无筛选传 `null` |
| `quickFilterIdList` | 快筛标签 ID 数组 |
| `qft` | 快筛类型组合；有 1 个快筛类型时传该类型，2 个快筛类型时前端传 `3` |

返回结构：

```json
{
  "success": true,
  "data": [
    {
      "itemType": 1,
      "itemInfo": {
        "projectInfo": {}
      }
    },
    {
      "itemType": 2,
      "itemInfo": {
        "rankInfo": {}
      }
    }
  ],
  "paging": {
    "pageNo": 1,
    "pageSize": 20,
    "hasMore": true
  }
}
```

字段说明：

| 字段 | 说明 |
|---|---|
| `itemType=1` | 演出项目项，读取 `itemInfo.projectInfo` |
| `itemType=2` | 榜单/推荐卡片，通常不作为演出去重结果 |
| `projectInfo.projectId` | 演出 ID，对应详情接口的 `performanceId` |
| `projectInfo.name` | 演出名称 |
| `projectInfo.categoryId` | 分类 ID |
| `projectInfo.showTimeRange` | 演出时间文本 |
| `projectInfo.cityName` | 城市名 |
| `projectInfo.shopName` | 场馆名 |
| `projectInfo.priceInfo` | 价格展示对象 |
| `projectInfo.billBoard` | 榜单信息，如 `亲子演出热销榜No.1` |
| `projectInfo.jumpDetailUrl` | 跳转详情 URL |

分类快筛选项接口：

```http
GET https://show.maoyan.com/my/ianvs/categoryChannel/wonderfulPerformancesOptions?categoryId={categoryId}
```

用途：获取该分类下的快筛标签和艺人筛选项。亲子演出当前返回 `quickFilters`，如限时优惠、早鸟票。

### 场馆详情

```http
GET /shop/detail?shopId={shopId}
```

必要前置：`shopId`。

用途：查询场馆基础信息。

字段：

- `shopName`, `shopBranchName`
- `address`
- `lat`, `lng`
- `phones`
- `shopRegion`, `shopCategory`
- `postUrl`
- `roadInfo`
- `mallName`, `mallShopId`, `mallShopUuid`

### 场馆演出列表

```http
GET /shop/performances?shopId={shopId}&pageNo={pageNo}&pageSize={pageSize}
```

必要前置：`shopId`。

用途：查询某场馆下的演出。需要完整详情时继续调用演出详情接口。

### 推荐、日历、榜单

这些接口用于公开展示模块，使用前先确保已有 `cityId`。返回结果仍需要按城市、分类、日期做本地校验。

| 接口 | 方法 | 状态 | 说明 |
|---|---|---|---|
| `/recommend/performances` | GET | 可用 | 城市推荐演出列表 |
| `/performances/calendar` | GET | 可用 | 日历入口演出列表 |
| `/calendarFloor/quickSelectTypeList` | GET | 可用 | 日历快筛类型 |
| `/ranks` | GET | 可用 | 榜单入口列表 |
| `/ranks/{rankType}` | GET | 可用 | 榜单详情；不同 `rankType` 可能为空 |
| `/algoBillBoard/category/list` | GET | 可用 | 算法榜单分类 |
| `/algoBillBoard/performance/list?billBoardAttrType={type}` | GET | 可用 | 榜单项目列表；缺少 `billBoardAttrType` 会返回 400 |
| `/recommend/algoBillBoard/list` | GET | 可用 | 首页推荐榜单 |
| `/recommend/groupPurchase/list` | GET | 可用 | 团购推荐 |

## 不作为 skill 数据源的接口

这些接口本轮验证中不可用、参数不稳定，或不能满足 skill 的公开数据抓取要求，不应作为 skill 的主流程数据源。

| 接口 | 原因 |
|---|---|
| `/search` | 当前返回 404 |
| `/performances` | 当前返回 404 |
| `/calendarFloor/performanceList` | GET 返回 405；POST JSON 返回 400；未确认稳定调用方式 |
| `/algoBillBoard/performance/list` 不带 `billBoardAttrType` | 返回 400 |
| `/v2/performance/getWrapList` | 当前返回 500 |
| `/my/ianvs/category/channel/mustSeeShows` | 当前返回 `success=false` 或空数据，不作为主数据源 |
| `/my/ianvs/categoryChannel/giantFloor` | 当前数据为空，不作为主数据源 |

可作为频道辅助信息、但不作为精确演出列表主源：

```http
GET https://show.maoyan.com/my/ianvs/categoryChannel/modules
GET https://show.maoyan.com/my/ianvs/categoryChannel/projectFloor
GET https://show.maoyan.com/my/ianvs/categoryChannel/brandPavilion
```

## 场景流程

### 已知演出 ID，查详情

1. 调用：

```http
GET /v2/performance/{performanceId};supportNewPromotion=false
```

2. 返回基础信息、场馆、时间、价格摘要、购票规则。
3. 如果用户还要场次、票档或库存，再调用：

```http
GET /v2/performance/{performanceId}/shows/1;supportNewPromotion=false
```

### 已知演出名称，查详情

1. 如本次任务还没有城市上下文，先询问用户城市并保存 `cityId`。
2. 调用：

```http
GET /performances/search
```

3. 对返回结果做本地关键词匹配和城市校验。
4. 从候选结果中选择最匹配的 `performanceId`。
5. 调用演出详情接口。
6. 需要票档时调用场次和票档接口。

### 查询某城市演出列表

1. 如本次任务还没有城市上下文，先询问用户城市并保存 `cityId`。
2. 调用：

```http
GET /recommend/performances
```

3. 如需扩大候选池，可补充调用：

```http
GET /performances/calendar
GET /performances/list
```

4. 对返回项按城市、分类、关键词、日期本地过滤并按 `performanceId` 去重。
5. 列表项需要完整详情时，调用详情接口。

### 查询分类频道页

1. 根据页面路由得到 `categoryId` 和 `labelId`，例如亲子演出为 `categoryId=7`、`labelId=0`。
2. 调用筛选项接口：

```http
GET https://show.maoyan.com/my/ianvs/categoryChannel/wonderfulPerformancesOptions?categoryId=7
```

3. 调用频道列表接口：

```http
POST https://show.maoyan.com/my/ianvs/categoryChannel/wonderfulPerformances?clientPlatform=3
```

4. 只读取 `itemType=1` 的 `itemInfo.projectInfo`。
5. 按 `projectId` 去重，并校验 `categoryId`、`cityName`、日期。城市不匹配时不能使用该结果。
6. 需要完整信息时，用 `projectId` 调用详情接口。

### 查询完整购票信息

1. 调用演出详情接口。
2. 读取 `saleStatus`、`ticketStatus`、`stockOut`、`needRealName`、`ticketNotes`、`serviceTitleList`。
3. 调用场次和票档接口。
4. 只返回公开展示的票档和规则，不调用下单、预支付、实名、地址等接口。

### 查询场馆信息

1. 如果用户给 `performanceId`，先调演出详情接口读取 `shopId`。
2. 调用场馆详情接口：

```http
GET /shop/detail?shopId={shopId}
```

3. 如需该场馆下演出，调用：

```http
GET /shop/performances?shopId={shopId}&pageNo={pageNo}&pageSize={pageSize}
```

## 调用依赖速查

| 目标 | 必要前置 | 首选接口 | 后续接口 |
|---|---|---|---|
| 已知 ID 查详情 | `performanceId` | `/v2/performance/{id}` | `/v2/performance/{id}/shows/1` |
| 关键词查详情 | `cityId`, `keyword` | `/performances/search` | `/v2/performance/{id}` |
| 城市演出列表 | `cityId` | `/recommend/performances` | `/performances/calendar`, `/performances/list`, `/v2/performance/{id}` |
| 分类频道页 | `categoryId`；如指定城市则还需 `cityId` | `/my/ianvs/categoryChannel/wonderfulPerformances` | `/v2/performance/{id}` |
| 票档库存 | `performanceId` | `/v2/performance/{id}` | `/v2/performance/{id}/shows/1` |
| 场馆详情 | `shopId` | `/shop/detail` | `/shop/performances` |
| 榜单 | `cityId`, `billBoardAttrType` | `/algoBillBoard/performance/list` | `/v2/performance/{id}` |

## 标准字段映射

| 标准字段 | 普通列表/详情字段 | 分类频道字段 |
|---|---|---|
| `id` | `performanceId` | `projectInfo.projectId` |
| `title` | `name` / `shortName` | `projectInfo.name` |
| `category_id` | `categoryId` | `projectInfo.categoryId` |
| `city_id` | `cityId` | 无，需从详情补全 |
| `city_name` | `cityName` | `projectInfo.cityName` |
| `venue_id` | `shopId` | 无，需从详情补全 |
| `venue_name` | `shopName` | `projectInfo.shopName` |
| `address` | `address` | 无，需从详情补全 |
| `lat` | `lat` | 无，需从详情补全 |
| `lng` | `lng` | 无，需从详情补全 |
| `time_text` | `showTimeRange` | `projectInfo.showTimeRange` |
| `lowest_price` | `lowestPrice` | `projectInfo.priceInfo` |
| `price_list` | `priceList` / `sellPriceList` | 无，需从详情/场次补全 |
| `poster_url` | `posterUrl` | `projectInfo.posterUrl` |
| `detail_html` | `detail` | 无，需从详情补全 |
| `ticket_notes_html` | `ticketNotes` | 无，需从详情补全 |
| `sale_status` | `saleStatus` | 无，需从详情补全 |
| `ticket_status` | `ticketStatus` | 无，需从详情补全 |
| `need_real_name` | `needRealName` | 无，需从详情补全 |
| `stock_out` | `stockOut` | 无，需从详情补全 |
| `share_url` | `shareLink` | `projectInfo.jumpDetailUrl` |

## SKILL 禁止使用的接口

以下接口需要登录态、涉及用户个人数据，或属于评论/收藏/订单/实名/验票/交易流程。公开演出数据 skill 不应调用这些接口，即使用户要求查询公开演出详情或价格，也不应使用它们作为数据源。

### 用户互动、收藏、评论

```http
GET/POST https://yanchu.maoyan.com/api/mobile/project/popup
GET/POST https://yanchu.maoyan.com/api/mobile/comment/project/pageQuery
GET/POST https://yanchu.maoyan.com/api/mobile/comment/project/myComments
GET/POST https://yanchu.maoyan.com/api/mobile/commentV2/project/hotComment
POST https://yanchu.maoyan.com/api/mobile/comment/submit
POST https://yanchu.maoyan.com/api/mobile/favor/addFavor
POST https://yanchu.maoyan.com/api/mobile/favor/cancelFavor
GET/POST https://yanchu.maoyan.com/my/interact/project/addFavor
GET/POST https://yanchu.maoyan.com/my/interact/project/cancelFavor
```

### 订单、支付、实名、地址、验票

```http
GET/POST /tx/order/detail/v2/{orderId}
GET/POST /tx/smsOrder/detailV2
GET/POST /tx/order/wish
GET/POST /tx/order/conditionRefundDetail/{orderId}
POST /tx/order/refundApply
POST /tx/order/exchange/confirm
GET/POST /tx/prepay/getQueueInfo
GET/POST /tx/V2/address/allAddressList
GET/POST /tx/V2/address/getAddressById
GET/POST /tx/V2/address/queryAddress
POST /tx/V2/address/saveAddress
POST /tx/address/deleteAddress
GET/POST /tx/realName/allRealNameUserList
GET/POST /tx/realName/getRealNameLimit
GET/POST /tx/realName/queryIdType
GET/POST /tx/realName/queryCertLocation
POST /tx/realName/saveRealNameUser
POST /tx/realName/deleteRealNameUser
GET/POST /tx/ticketCheck?orderTicketId={id}
GET/POST /tx/ticketClipCheck?ticketClipId={id}
```

### 发票和用户资产

```http
GET/POST /tx/invoice/{id}
POST /tx/invoice/apply
GET/POST /tx/invoice/getBusinessInfoByName
GET/POST /newFavor/loadFavor
POST /newFavor/addFavor
POST /newFavor/cancelFavor
GET/POST /newFavor/favors
```

## 数据处理要求

- 只抓取公开展示数据。
- 控制请求频率和并发。
- 不绕过登录、验证码、风控、下单、库存锁定或支付流程。
- `detail` 和 `ticketNotes` 是 HTML，展示或入库前应清洗。
- 如果接口返回空数组，按“当前无公开展示数据”处理，不用交易接口补数据。
- 对任何列表型接口，都要本地校验城市、分类、日期、关键词，并按 `performanceId` / `projectId` 去重。
