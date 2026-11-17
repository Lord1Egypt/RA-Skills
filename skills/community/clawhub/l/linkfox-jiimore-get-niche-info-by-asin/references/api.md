# 极目-亚马逊-根据 ASIN 查询相关细分市场信息 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/jiimore/getNicheInfoByAsin`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和算力问题** 处理）

## 请求参数

POST Body（JSON）：

### 必填参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| asin | string | 是 | 商品 ASIN（必填）。工具会查找与该 ASIN 共享相同细分市场（Niche）的市场段落 |

### 站点与数量

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| countryCode | string | 否 | US | 国家编码，可选值：`US`（美国）、`JP`（日本）、`DE`（德国） |
| count | integer | 否 | 10 | 返回的细分市场数量 |

### 筛选参数（均为可选）

**商品与价格**：

| 参数 | 类型 | 说明 |
|------|------|------|
| productCountMin | integer | 商品数量（当前）最小值 |
| productCountMax | integer | 商品数量（当前）最大值 |
| avgPriceMin | number | 平均价格（当前）最小值 |
| avgPriceMax | number | 平均价格（当前）最大值 |

**搜索与销售（7天统计）**：

| 参数 | 类型 | 说明 |
|------|------|------|
| searchVolumeT7Min | integer | 搜索量（7天统计）最小值 |
| searchVolumeT7Max | integer | 搜索量（7天统计）最大值 |
| unitsSoldT7Min | integer | 销售量（7天统计）最小值 |
| unitsSoldT7Max | integer | 销售量（7天统计）最大值 |
| clickCountT7Min | integer | 点击量（7天统计）最小值 |
| clickCountT7Max | integer | 点击量（7天统计）最大值 |
| clickConversionRateT7Min | number | 点击转换率（7天统计）最小值，数值范围为0-1，0.1表示10%的转换率 |
| clickConversionRateT7Max | number | 点击转换率（7天统计）最大值，数值范围为0-1，0.1表示10%的转换率 |

**品牌指标**：

| 参数 | 类型 | 说明 |
|------|------|------|
| brandCountMin | integer | 品牌数量最小值 |
| brandCountMax | integer | 品牌数量最大值 |
| top5BrandsClickShareMin | number | 前5个品牌所占细分市场的点击量份额最小值，数值范围为0-1，0.1表示10%的点击份额 |
| top5BrandsClickShareMax | number | 前5个品牌所占细分市场的点击量份额最大值，数值范围为0-1，0.1表示10%的点击份额 |
| avgBrandAgeMin | number | 平均品牌年龄（当前）最小值 |
| avgBrandAgeMax | number | 平均品牌年龄（当前）最大值 |
| avgBrandAgeQoqMin | number | 平均品牌年龄（90天统计）最小值 |
| avgBrandAgeQoqMax | number | 平均品牌年龄（90天统计）最大值 |
| avgBrandAgeYoyMin | number | 平均品牌年龄（360天统计）最小值 |
| avgBrandAgeYoyMax | number | 平均品牌年龄（360天统计）最大值 |

**卖家指标**：

| 参数 | 类型 | 说明 |
|------|------|------|
| avgSellingPartnerAgeMin | number | 平均销售伙伴年龄最小值 |
| avgSellingPartnerAgeMax | number | 平均销售伙伴年龄最大值 |
| avgSellingPartnerAgeQoqMin | number | 平均销售伙伴年龄（90天统计）最小值 |
| avgSellingPartnerAgeQoqMax | number | 平均销售伙伴年龄（90天统计）最大值 |
| avgSellingPartnerAgeYoyMin | number | 平均销售伙伴年龄（360天统计）最小值 |
| avgSellingPartnerAgeYoyMax | number | 平均销售伙伴年龄（360天统计）最大值 |

**竞争与广告**：

| 参数 | 类型 | 说明 |
|------|------|------|
| top5ProductsClickShareMin | number | 排名前5位的商品点击份额（当前）最小值，数值范围为0-1，0.1表示10%的点击份额 |
| top5ProductsClickShareMax | number | 排名前5位的商品点击份额（当前）最大值，数值范围为0-1，0.1表示10%的点击份额 |
| sponsoredProductsPercentageMin | number | SP广告占比最小值，数值范围为0-1，0.1表示10%的占比 |
| sponsoredProductsPercentageMax | number | SP广告占比最大值，数值范围为0-1，0.1表示10%的占比 |
| cpcMediumMin | number | CPC（当前）最小值 |
| cpcMediumMax | number | CPC（当前）最大值 |

**新品与退货**：

| 参数 | 类型 | 说明 |
|------|------|------|
| launchRateT180Min | number | 发布商品的成功率（180天统计）最小值，数值范围为0-1，0.1表示10%的成功率 |
| launchRateT180Max | number | 发布商品的成功率（180天统计）最大值，数值范围为0-1，0.1表示10%的成功率 |
| returnRateT360Min | number | 退货率（360天统计）最小值，数值范围为0-1，0.1表示10%的退货率 |
| returnRateT360Max | number | 退货率（360天统计）最大值，数值范围为0-1，0.1表示10%的退货率 |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码，200 表示成功 |
| costToken | integer | 消耗 token |
| nicheInfoVoList | array | 细分市场信息列表（见下方细分市场对象字段） |

> 说明：业务状态通过响应体中的 `errcode` 字段区分（`errcode = 200` 表示成功）。当结果为空时接口会返回业务错误（无符合要求的细分市场信息）。

### 细分市场对象字段（`nicheInfoVoList` 数组内）

| 字段 | 类型 | 说明 |
|------|------|------|
| nicheId | string | 细分市场ID |
| nicheTitle | string | 细分市场标题 |
| translationZh | string | 细分市场标题(中文) |
| demand | integer | 细分市场得分 |
| productCount | integer | 商品数量 |
| avgPrice | number | 产品均价 |
| minimumPrice | number | 产品最低价 |
| maximumPrice | number | 产品最高价 |
| searchVolumeWeekly | integer | 搜索量（周数据） |
| searchVolumeQuarterly | integer | 搜索量（季度数据） |
| searchVolumeGrowthWeekly | number | 搜索量增长率（周数据） |
| searchVolumeGrowthQuarterly | number | 搜索量增长率（季度数据） |
| unitsSoldWeekly | integer | 销售数量（周数据） |
| unitsSoldQuarterly | integer | 销售数量（季度数据） |
| clickCountWeekly | integer | 点击量（周数据） |
| clickCountQuarterly | integer | 点击量（季度数据） |
| clickToSaleConversionWeekly | number | 点击转换率（周数据） |
| clickConversionRateQuarterly | number | 点击转换率（季度数据） |
| searchConversionRateWeekly | number | 搜索转换率（周数据） |
| searchConversionRateQuarterly | number | 搜索转换率（季度数据） |
| brandCount | integer | 品牌数量 |
| top5BrandsClickShare | number | 前5个品牌所占细分市场的点击量份额 |
| top5ProductsClickShare | number | 排名前5位的商品点击份额 |
| avgBrandAgeNow | number | 平均品牌年龄(当前) |
| avgBrandAgeQuarterly | number | 平均品牌年龄(季度数据) |
| newProductsLaunchedSemiannual | integer | 已发布新产品的数量（半年数据） |
| successfulLaunchedSemiannual | integer | 成功发布商品的数量（半年数据） |
| launchRateSemiannual | number | 发布商品的成功率（半年数据） |
| returnRateAnnual | number | 退货率（全年数据） |
| acos | number | （ACOS）广告销售成本比 |
| profitMarginGt50PctSkuRatio | number | 利润率大于50%的商品比例 |
| breakEvenRatio | number | 盈亏平衡自然占比 |
| cpc | object | CPC数据：`{ high（最高价）, medium（中间价）, low（最低价） }` |
| categorieList | array | 商品品类列表 |
| referenceAsinImageUrl | string | 细分市场参考图片地址 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和算力问题** 处理。|
| 402 | 算力不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和算力问题** 处理。|
| 10000 | 无符合要求的细分市场信息 | 放宽筛选条件或更换 ASIN 后重试 |
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
curl -X POST https://tool-gateway.linkfox.com/jiimore/getNicheInfoByAsin \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "asin": "B0D9NWVC6Z",
    "countryCode": "US",
    "count": 10
  }'
```

### 带筛选条件的查询示例

```bash
curl -X POST https://tool-gateway.linkfox.com/jiimore/getNicheInfoByAsin \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "asin": "B0D9NWVC6Z",
    "countryCode": "US",
    "count": 20,
    "top5BrandsClickShareMax": 0.5,
    "brandCountMin": 20,
    "searchVolumeT7Min": 5000
  }'
```

---

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-jiimore-get-niche-info-by-asin",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter
- `sentiment`: Choose ONE — `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE — `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
