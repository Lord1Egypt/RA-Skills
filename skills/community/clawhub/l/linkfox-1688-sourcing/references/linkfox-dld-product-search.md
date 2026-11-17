---
name: linkfox-dld-product-search
description: 1688 批发平台商品搜索。用于寻找国内工厂货源、供应商发现、批发价格对比及选品调研。

# 1688 商品搜索（DLD Product Search）

本技能用于在 1688 批发平台（阿里巴巴国内 B2B 市场）上搜索和分析商品，帮助电商卖家与采购人员寻找优质供应商与有利润空间的商品。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 基于 1688 平台进行关键词商品搜索，聚合商品列表及其销量、价格分层、供应商资质与履约信息。
- 数据来源于店雷达（store radar）分析，覆盖实时商品列表与近 7 天 / 30 天销量指标。
- 支持按关键词、商品链接、商品 ID 检索，并按价格、销量、销售额、上架时间等多维排序。
- 支持按公司类型（店铺/工厂）、卖家会员类型、发货时间、代发权益、面单支持等筛选。

### ❌ 边界与限制

- **关键词语言**：`keyWord` 必须为中文，非中文关键词需先翻译再查询。
- **搜索方式互斥**：`keyWord`、`goodsUrl`、`productIds` 三者择一使用。
- **统计周期**：仅支持近 7 天（`cycle="7"`）或近 30 天（`cycle="30"`）。
- **分页上限**：单次最多 100 条；按商品 ID 查询最多 20 个。
- **不在范围内**：Amazon 等非 1688 平台的商品研究；1688 店铺级分析（店铺流量、店铺排名）；1688 广告与推广策略；商品评论或评分分析；物流成本计算与运费估算；下单与交易处理；用户已有本地商品数据文件需分析。

**边界判断**：当用户说"找货源""找供应商""批发商品"时，若涉及在 1688 平台按价格、销量、供应商类型等条件搜索具体商品，适用本技能；若需要店铺级分析、广告优化或超出商品搜索范围的运营操作，则不适用。

## 核心概念

本工具提供 1688（中国最大的 B2B 批发市场）的关键词商品搜索，聚合商品列表及其销量数据、价格分层、供应商资质与履约选项。数据来源于店雷达分析，覆盖实时商品列表与 7 天、30 天销量指标。

**关键术语**：
- **批发价**（`price`）：按起批量下单时的单件价格。
- **代发价**（`consignPrice`）：单件一件代发的单件价格（通常高于批发价）。
- **诚信通年限**（`tpYear`）：供应商持有阿里巴巴诚信通会员的年数，反映经营年限。
- **销售件数**（`salesQuantity`）：所选统计周期内的总销售件数。
- **销售笔数**（`salesOrderCount`）：所选统计周期内的总订单笔数。
- **预估销售额**（`estimatedSalesAmount`）：所选统计周期内的预估销售额。

## 使用示例

**1. 基础关键词搜索——"瑜伽垫"热销品**
```json
{"keyWord": "瑜伽垫", "cycle": "30", "sortField": "saleCount30d", "sortType": "desc", "pageSize": 20}
```

**2. 仅工厂且有价格区间**
```json
{"keyWord": "蓝牙耳机", "companyType": 2, "beginPrice": 10, "endPrice": 50, "cycle": "30", "sortField": "orderCount30d"}
```

**3. 跨境商品并支持代发**
```json
{"keyWord": "手机壳", "offerType": 4, "proxyRights": "4360897", "cycle": "7", "sortField": "saleVolume7d"}
```

**4. 最近上架的新品，按上架时间排序**
```json
{"keyWord": "夏季连衣裙", "offerType": 2, "sortField": "offerCreateTime", "sortType": "desc", "pageSize": 50}
```

**5. 超级工厂的高销量商品**
```json
{"keyWord": "数据线", "shiLiType": "superFactory", "beginSaleCount": 1000, "cycle": "30", "sortField": "saleCount30d"}
```

**6. 按商品链接搜索**
```json
{"goodsUrl": "https://detail.1688.com/offer/805578065498.html", "cycle": "30"}
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示商品标题、价格、销量指标与供应商信息，并附商品链接方便直达。
2. **价格口径**：有批发价与代发价时同时展示，便于用户对比利润空间。
3. **销量口径**：根据所用的 `cycle` 参数，明确标注是 7 天还是 30 天数据。
4. **图片展示**：返回 `imageUrl` 时展示商品图片，便于直观识别。
5. **分页提示**：总条数超出当前页时，告知总数并询问是否继续翻页。
6. **错误处理**：查询失败时说明原因，并建议调整参数（如放宽筛选、检查关键词拼写）。
7. **关键词翻译**：用户提供英文商品词时，先翻译为中文再调用，并在回复中注明译文。

## 用户表达与场景速查

**适用** —— 1688 批发商品搜索与货源调研：

| 用户说 | 场景 |
|--------|------|
| "在 1688 上找 XX 的供应商" | 关键词商品搜索 |
| "1688 上什么好卖" | 热销商品发现 |
| "找工厂的便宜 XX" | 工厂货源 + 价格筛选 |
| "1688 一件代发 XX 的供应商" | 支持代发的商品搜索 |
| "对比 XX 在 1688 上的价格" | 跨供应商比价 |
| "1688 上 XX 的新品" | 新品发现 |
| "找 1688 跨境商品" | 跨境商品采购 |
| "哪些 1688 供应商 24 小时发货" | 履约速度筛选 |
| "XX 的顶级工厂" | 超级工厂 / 实力商家搜索 |
| "查这个 1688 商品"（带链接或 ID） | 直接查询指定商品 |

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

# 店雷达 1688 选品库 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/dld/productSearch`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| keyWord | string | 否 | - | 搜索关键词（必须为中文，最多50字符） |
| goodsUrl | string | 否 | - | 商品链接地址（与keyWord二选一） |
| productIds | string | 否 | - | 商品ID，多个逗号隔开，最多20个 |
| cycle | string | 否 | - | 统计周期：`7`（近7天）或 `30`（近30天） |
| searchType | integer | 否 | 1 | 搜索类型：1-模糊匹配，3-精准匹配 |
| sortField | string | 否 | orderCount30d | 排序字段：orderCount7d, saleCount7d, saleVolume7d, orderCount30d, saleCount30d, saleVolume30d, offerCreateTime, price, consignPrice |
| sortType | string | 否 | desc | 排序类型：desc（降序）、asc（升序） |
| pageIndex | integer | 否 | 1 | 页码（从1开始） |
| pageSize | integer | 否 | 20 | 每页数量（10-100） |
| beginPrice | number | 否 | - | 批发价（起始） |
| endPrice | number | 否 | - | 批发价（结束） |
| beginConsignPrice | number | 否 | - | 代发价（起始） |
| endConsignPrice | number | 否 | - | 代发价（结束） |
| beginOrderCount | integer | 否 | - | 销售笔数（起始） |
| endOrderCount | integer | 否 | - | 销售笔数（结束） |
| beginSaleCount | integer | 否 | - | 销售件数（起始） |
| endSaleCount | integer | 否 | - | 销售件数（结束） |
| beginSaleVolume | number | 否 | - | 销售额（起始） |
| endSaleVolume | number | 否 | - | 销售额（结束） |
| beginStartQuantity | integer | 否 | - | 起购数量（起始） |
| endStartQuantity | integer | 否 | - | 起购数量（结束） |
| beginTpYear | integer | 否 | - | 诚信通年限（起始） |
| endTpYear | integer | 否 | - | 诚信通年限（结束） |
| beginOfferCreateTime | string | 否 | - | 上架时间起始（格式：YYYY-MM-DD） |
| endOfferCreateTime | string | 否 | - | 上架时间结束（格式：YYYY-MM-DD） |
| companyType | integer | 否 | 0 | 公司类型：0-不限，1-店铺，2-工厂 |
| offerType | integer | 否 | 0 | 商品标识：0-不限，2-新品，3-1688严选，4-跨境，5-支持定制，6-镇店之宝 |
| shiLiType | string | 否 | - | 卖家类型（多选逗号隔开）：superFactory（超级工厂）、Power（实力商家）、TrustPass（诚信通） |
| sendTime | string | 否 | - | 发货时间（多选逗号隔开）：24、48、72 |
| faceToFaceSupport | string | 否 | - | 面单支持（多选逗号隔开）：441218（淘宝）、386434（抖音）、422914（拼多多）、422978（小红书）、386370（快手） |
| proxyRights | string | 否 | - | 代发权益（多选逗号隔开）：4360897（一件代发包邮）、449154（先采后付） |
| shopService | string | 否 | - | 卖家服务（多选逗号隔开）：4057409（安心购）、888777（深度认证报告） |
| buyerProtections | string | 否 | - | 权益保障（多选逗号隔开）：商品包邮、7天包退货、支持运费险 |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总记录数 |
| type | string | 渲染样式 |
| columns | array | 渲染列定义 |
| products | array | 商品列表（详见下方字段） |

### products 数组元素字段

| 字段 | 类型 | 说明 |
|------|------|------|
| offerId | string | 商品ID |
| asin | string | 商品编号 |
| title | string | 商品标题 |
| asinUrl | string | 商品链接地址 |
| imageUrl | string | 商品图片地址 |
| price | number | 批发价 |
| consignPrice | number | 代发价 |
| quantityPrices | string | 价格区间 |
| quantityBegin | integer | 起批量 |
| unit | string | 单位 |
| currency | string | 币种 |
| salesOrderCount | integer | 销售笔数（按统计周期） |
| salesQuantity | integer | 销售件数（按统计周期） |
| estimatedSalesAmount | integer | 预估销售额（按统计周期） |
| deliveryTime | string | 发货时间 |
| availableDate | string | 商品上架时间 |
| levelName | string | 类目层级名称 |
| company | string | 店铺名称 |
| shopId | string | 店铺ID |
| shopUrl | string | 店铺链接地址 |
| dataType | string | 数据类型：weeklyData（周数据）、monthlyData（月数据） |
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
curl -X POST https://tool-gateway.linkfox.com/dld/productSearch \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyWord": "瑜伽垫", "cycle": "30", "sortField": "saleCount30d", "sortType": "desc", "pageSize": 20}'
```
