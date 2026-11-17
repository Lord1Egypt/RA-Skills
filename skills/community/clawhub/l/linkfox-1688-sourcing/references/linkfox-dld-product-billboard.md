---
name: linkfox-dld-product-billboard
description: 1688 商品热销榜单查询。用于发现国内货源批发爆款、一件代发选品及趋势商品调研。

# 1688 商品热销榜单（DLD Product Billboard）

本技能用于查询 1688 平台商品热销榜单数据，帮助卖家在国内最大的 B2B 批发市场发现热销批发商品与货源机会。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询 1688 平台商品排名数据，覆盖**周榜**与**月榜**两种榜单。
- 发现热销批发商品、对比供应商、识别国内批发市场的货源与趋势机会。
- 支持按关键词、价格区间、销量区间、公司类型（店铺/工厂）、卖家会员类型、发货时间、代发权益、面单支持等多维筛选与排序。

### ❌ 边界与限制

- **关键词语言**：`keyWord` 参数必须为中文，非中文关键词需先翻译再查询。
- **日期格式**：周榜日期须为该周周日；月榜日期须为该月第一天。
- **数据时效**：周榜仅近 90 天，月榜仅近 12 个月。
- **分页上限**：单次请求最多 100 条；按商品 ID 查询时最多 20 个。
- **不在范围内**：Amazon 选品与关键词分析（用 ABA 工具）；1688 店铺级分析（店铺排名、店铺评分）；Alibaba.com 国际站数据；价格议价与下单；商品质量评价与认证；物流成本计算与货代。

## 核心概念

1688 商品热销榜单提供 1688 平台商品排名数据，覆盖**周榜**与**月榜**，帮助发现趋势批发商品、对比供应商、识别货源机会。

**榜单类型**：
- **周榜**（`pageType=2`）：日期传该周周日，如 `2025-06-15`；数据为近 90 天。
- **月榜**（`pageType=3`）：日期传该月第一天，如 `2025-06-01`；数据为近 12 个月。

**默认行为**：月榜，按销售笔数降序，每页 20 条。

## 使用示例

**1. 某关键词的月度热销榜**
> "查一下 1688 本月手机壳的热销榜"
```json
{"keyWord": "手机壳", "pageType": 3, "date": "2026-03-01", "sortField": "orderCount", "sortType": "desc"}
```

**2. 周榜按销售额排序**
> "上周瑜伽垫品类里销售额最高的是哪些？"
```json
{"keyWord": "瑜伽垫", "pageType": 2, "date": "2026-03-22", "sortField": "saleVolume", "sortType": "desc"}
```

**3. 工厂直供并限价**
> "在 1688 找 5-30 元的耳机工厂直供商品"
```json
{"keyWord": "耳机", "companyType": 2, "beginPrice": 5, "endPrice": 30, "sortField": "saleCount", "sortType": "desc"}
```

**4. 跨境标签且 24 小时发货**
> "看下 24 小时内发货的跨境标签 LED 灯商品"
```json
{"keyWord": "LED灯", "offerType": 4, "sendTime": "24", "sortField": "orderCount", "sortType": "desc"}
```

**5. 超级工厂新品**
> "找宠物用品类目下超级工厂的新上架商品"
```json
{"keyWord": "宠物用品", "offerType": 2, "shiLiType": "superFactory", "sortField": "offerCreateTime", "sortType": "desc"}
```

**6. 支持代发且有买家保障的商品**
> "看下支持一件代发、包邮且支持 7 天退货的包包商品"
```json
{"keyWord": "包包", "proxyRights": "4360897", "buyerProtections": "商品包邮,7天包退货", "sortField": "orderCount", "sortType": "desc"}
```

**7. 价格区间内的高销量商品**
> "找玩具类目下批发价 50 元以内、销售笔数超 1000 的商品"
```json
{"keyWord": "玩具", "beginOrderCount": 1000, "endPrice": 50, "sortField": "orderCount", "sortType": "desc"}
```

**8. 按商品 ID 查询**
> "查这几个 1688 商品 ID：123456、789012"
```json
{"productIds": "123456、789012"}
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示商品标题、批发价、代发价、销售笔数、销售件数、预估销售额、供应商名称、上架时间等。
2. **图片展示**：返回 `imageUrl` 时展示商品图片，便于直观识别。
3. **提供链接**：附商品链接（`asinUrl`）与店铺链接（`shopUrl`），方便直达 1688 商品页。
4. **价格格式**：价格须带币种（CNY/RMB），并注明是批发价还是代发价。
5. **销量口径**：展示销量数据时，按 `dataType` 字段标明是周数据还是月数据。
6. **分页提示**：总条数超出当前页时，告知总数并询问是否继续翻页。
7. **关键词翻译**：用户提供非中文关键词时，先翻译为中文再查询，并告知译文。
8. **错误处理**：查询失败时说明原因，并建议调整参数（如放宽筛选、检查日期格式）。

## 用户表达与场景速查

**适用** —— 1688 批发商品发现与货源调研：

| 用户说 | 场景 |
|--------|------|
| "1688 上什么火"、"1688 趋势商品" | 热销商品发现 |
| "给 XX 找便宜货源"、"XX 批发货源" | 按关键词找货源 |
| "工厂直供商品"、"OEM 供应商" | 工厂筛选 |
| "跨境货源"、"出口商品" | 跨境标签筛选 |
| "1688 一件代发商品" | 支持代发的商品搜索 |
| "1688 新品"、"最近上架的" | 新品发现 |
| "对比 XX 的供应商" | 多结果对比 |
| "1688 商品排行"、"热销榜" | 榜单浏览 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用 skill 内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个 skill 并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个 skill。

---

# 店雷达-1688商品榜单 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/dld/productBillboard`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyWord | string | 否 | 商品搜索关键字（搜索关键词必须是中文，如果不是请先翻译），最大长度50 |
| date | string | 否 | 查询时间。周榜：传入该周的周天日期，如 `2025-06-15`（最长近90天）；月榜：传入该月第一天，如 `2025-06-01`（最长近一年） |
| pageType | integer | 否 | 榜单类型：`2` = 周榜，`3` = 月榜。默认 `3` |
| pageIndex | integer | 否 | 页码（从1开始），默认 `1` |
| pageSize | integer | 否 | 每页返回数量（10-100），默认 `20` |
| sortField | string | 否 | 排序字段，默认 `orderCount`。可选值：`orderCount`（销售笔数）、`saleCount`（销售件数）、`saleVolume`（预估销售额）、`offerCreateTime`（上架时间）、`price`（批发价）、`consignPrice`（代发价） |
| sortType | string | 否 | 排序类型：`desc`（降序）、`asc`（升序），默认 `desc` |
| searchType | integer | 否 | 商品关键词搜索类型：`1` = 模糊匹配，`3` = 精准匹配。默认 `1` |
| offerType | integer | 否 | 商品标识：`0` = 不限制，`2` = 新品，`3` = 1688严选，`4` = 跨境，`5` = 支持定制，`6` = 镇店之宝。默认 `0` |
| companyType | integer | 否 | 公司类型：`0` = 不限，`1` = 店铺，`2` = 工厂 |
| shiLiType | string | 否 | 卖家会员类型（多选），多个使用","号隔开。可选值：`superFactory`（超级工厂）、`Power`（实力商家）、`TrustPass`（仅诚信通会员） |
| beginTpYear | integer | 否 | 开始诚信通年限 |
| endTpYear | integer | 否 | 结束诚信通年限 |
| beginPrice | number | 否 | 批发价（起始） |
| endPrice | number | 否 | 批发价（结束） |
| beginConsignPrice | number | 否 | 代发价（起始） |
| endConsignPrice | number | 否 | 代发价（结束） |
| beginOrderCount | integer | 否 | 销售笔数（起始） |
| endOrderCount | integer | 否 | 销售笔数（结束） |
| beginSaleCount | integer | 否 | 销售件数（起始） |
| endSaleCount | integer | 否 | 销售件数（结束） |
| beginSaleVolume | number | 否 | 销售额（起始） |
| endSaleVolume | number | 否 | 销售额（结束） |
| beginStartQuantity | integer | 否 | 起始起批量 |
| endStartQuantity | integer | 否 | 结束起批量 |
| beginOfferCreateTime | string | 否 | 上架时间（起始），格式：`YYYY-MM-DD` |
| endOfferCreateTime | string | 否 | 上架时间（结束），格式：`YYYY-MM-DD` |
| sendTime | string | 否 | 发货时间（多选），多个使用","号隔开。可选值：`24`（24小时）、`48`（48小时）、`72`（72小时） |
| proxyRights | string | 否 | 代发权益（多选），多个使用","号隔开。可选值：`4360897`（一件代发包邮）、`449154`（先采后付） |
| shopService | string | 否 | 卖家服务（多选），多个使用","号隔开。可选值：`4057409`（安心购）、`888777`（深度认证报告） |
| buyerProtections | string | 否 | 权益保障（多选），多个用","隔开。可选值：`商品包邮`、`7天包退货`、`支持运费险` |
| faceToFaceSupport | string | 否 | 面单支持（多选），多个使用","号隔开。可选值：`441218`（淘宝）、`386434`（抖音）、`422914`（拼多多）、`422978`（小红书）、`386370`（快手） |
| productIds | string | 否 | 商品ID，顿号隔开搜索多个，最多20个 |
| goodsUrl | string | 否 | 商品链接地址 |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| type | string | 渲染的样式 |
| columns | array | 渲染的列 |
| products | array | 商品列表（见下方商品对象） |

### 商品对象

| 字段 | 类型 | 说明 |
|------|------|------|
| offerId | string | 商品id |
| asin | string | 商品编号 |
| title | string | 商品标题 |
| price | number | 批发价 |
| consignPrice | number | 代发价 |
| currency | string | 币种 |
| unit | string | 单位 |
| quantityBegin | integer | 起批量 |
| quantityPrices | string | 价格区间 |
| salesOrderCount | integer | 销售笔数（按统计周期返回对应的值） |
| salesQuantity | integer | 销售件数（按统计周期返回对应的值） |
| estimatedSalesAmount | integer | 预估销售额（按统计周期返回对应的值） |
| dataType | string | 数据类型：`weeklyData` = 周数据，`monthlyData` = 月数据 |
| availableDate | string | 商品上架时间，格式为 `yyyy-MM-dd HH:mm:ss` |
| deliveryTime | string | 发货时间 |
| levelName | string | 类目层级名称 |
| company | string | 店铺名称 |
| shopId | string | 店铺id |
| shopUrl | string | 店铺链接地址 |
| asinUrl | string | 商品链接地址 |
| imageUrl | string | 图片地址 |
| sourceType | string | 来源平台（1688） |
| sourceTool | string | 来源工具 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/dld/productBillboard \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "keyWord": "手机壳",
    "pageType": 3,
    "date": "2026-03-01",
    "sortField": "orderCount",
    "sortType": "desc",
    "pageSize": 20,
    "pageIndex": 1
  }'
```
