# API 参考文档

## 通用请求参数

所有接口均为 **POST** 请求，参数以 JSON body 传递（`Content-Type: application/json`）。

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| api_key | string | 是 | 认证令牌 |
| start_month | string | 视接口 | 起始月份，yyyy-MM。前置接口不需要，数据查询接口必选 |
| end_month | string | 视接口 | 结束月份，yyyy-MM。前置接口不需要，数据查询接口必选 |
| platform_ids | int[] | 视接口 | 平台ID数组，如 `[47, 38]` |
| brand_ids | int[] | 视接口 | 品牌ID数组 |
| cid_ids | string[] | 视接口 | 品类ID数组 |

## 响应格式

### 成功响应
```json
{
  "code": 0,
  "data": { ... },
  "msg": "操作成功"
}
```

### 失败响应
```json
{
  "code": 1,
  "data": null,
  "msg": "错误信息"
}
```

### 错误类型速查

| 错误场景 | code | msg 示例 | 处理方式 |
|---------|------|---------|---------|
| api_key 无效 | 1 | "Invalid api_key" | 重新获取 key |
| 时间超限 | 1 | "Query date out of range" | 查询可查时间范围，并提示用户访问链接（https://nexus.nint.hk/register?origin_id=22）申请试用获取高级权限 |
| 必选参数缺失 | 1 | "Missing required parameter: brand_ids" | 补充必选参数 |
| 权限不足 | 1 | "No permission for this platform" | 提示用户访问链接（https://nexus.nint.hk/register?origin_id=22）申请试用 |
| 品牌未找到 | 1 | "Brand not found" | 换关键词搜索 |

## 响应包裹层级（重要）

不同接口的 `data` 结构不一致，解析前必须确认：

| 接口组 | data 结构 | 解析路径 | 说明 |
|--------|----------|---------|------|
| 前置接口 | `list` | `d["data"]` | 直接返回列表（get-all-category-list-by-name 同） |
| A1 类目分布 | `{global_category_lv1_list: [], total: "...", "currency_unit": "..."}` | `d["data"]["global_category_lv1_list"]` | total 为字符串 |
| A2 Top品牌 | `{topBrandSalesList: {平台名: [品牌...]}}` | `d["data"]["topBrandSalesList"]` | 按平台名分组的 dict |
| A3 Top店铺 | `{topShopList: {平台名: [店铺...]}}` | `d["data"]["topShopList"]` | 按平台名分组的 dict |
| A4 Top商品 | `{topItemList: {平台名: [商品...]}}` | `d["data"]["topItemList"]` | 按平台名分组的 dict |
| B5 品牌总览 | `{marketOverviewData: [{...}]}` | `d["data"]["marketOverviewData"]` | 单条汇总数据 |
| B6/C7/C8/C9 | `{MarketOverview: [{...}], "currency_unit": "..."}` | `d["data"]["MarketOverview"]` | 按市场分组的列表 |

## 字段类型说明

| 字段 | 类型 | 说明 |
|-----|------|-----|
| sales_total | string | 销售额，需 `float()` 转换 |
| percentage | string | 百分比，如 "15.26" |
| num_total | int | 销量整数 |
| avg_price | float | 均价，可直接计算 |
| item_num | int | 商品数 |
| shop_num | int | 店铺数 |

---

## 前置接口（不需要 start_month / end_month）

### 1. 获取平台列表
```
POST /api/skill/get-platform-list
```

**参数**: `api_key`（必选）

**返回示例**:
```json
{
  "code": 0,
  "data": [
    {"id": "47", "name": "Amazon@United States", "name_cn": "亚马逊@美国"},
    {"id": "51", "name": "Amazon@United Kingdom", "name_cn": "亚马逊@英国"},
    {"id": "3", "name": "Shopee@Malaysia", "name_cn": "虾皮@马来西亚"}
  ],
  "msg": "获取平台列表成功"
}
```

### 2. 获取一级品类列表
```
POST /api/skill/get-top-category-list
```

**参数**: `api_key`（必选）

**返回示例**:
```json
{
  "code": 0,
  "data": {
    "category_list": [
      {"id": "2011010112", "name": "3C Electronics", "name_cn": "3C数码"},
      {"id": "2011010113", "name": "Beauty & Personal Care", "name_cn": "美容护理"},
      {"id": "2011010115", "name": "Household Supplies", "name_cn": "家居用品"}
    ]
  },
  "msg": "获取品类列表成功"
}
```

### 3. 按关键词搜索品类
```
POST /api/skill/get-all-category-list-by-name
```

**参数**: 
- `api_key`（必选）
- `category_like`（必选）- 品类名模糊匹配关键词（中文/英文均可）

**功能**: 根据关键词搜索品类，返回匹配的各级品类（含一级、二级等），用于精确查找品类ID

**返回字段**:
| 字段 | 类型 | 说明 |
|-----|------|------|
| id | string | 品类ID |
| level | string | 品类层级（"0"=一级, "1"=二级, "2"=三级） |
| name | string | 品类完整英文名（含层级路径，用 >> 分隔） |
| name_cn | string | 品类完整中文名（含层级路径，用 >> 分隔） |

**返回示例**:
```json
{
  "code": 0,
  "data": [
    {"id": "2011010113", "level": "0", "name": "Beauty & Personal Care", "name_cn": "美容护理"},
    {"id": "126762001", "level": "1", "name": "Beauty & Personal Care >> Beauty Instrument", "name_cn": "美容护理 >> 美容美体仪器"},
    {"id": "1801", "level": "1", "name": "Beauty & Personal Care >> Beauty & Skin Care/Body Care/Essential Oil", "name_cn": "美容护理 >> 美容护肤/美体/精油"}
  ],
  "msg": "获取品类列表成功"
}
```

**说明**: 
- 支持中英文关键词搜索
- `level: "0"` 为一级类目，`level: "1"` 为二级，以此类推
- `name`/`name_cn` 包含完整层级路径，便于确认品类归属
- 可用于查找 `cid_ids` 参数所需的品类ID

### 4. 获取品牌列表
```
POST /api/skill/get-brand-list
```

**参数**: 
- `api_key`（必选）
- `brand_like`（必选）- 品牌名模糊匹配关键词

**返回示例**:
```json
{
  "code": 0,
  "data": [
    {"id": "63114", "name": "统一/uni-president", "sales": "338789"},
    {"id": "102099", "name": "康师傅/Master Kong", "sales": "972439"}
  ],
  "msg": "获取品牌列表成功"
}
```

**说明**: `sales` 字段为品牌参考销额（CNY，近60天全平台总和），可用于判断品牌规模。

---

## 数据查询接口

### A组：全球排行（brand_ids / cid_ids 均为可选筛选条件）

#### A1. 类目分布
```
POST /api/skill/get-global-primary-categories
```

**必选参数**: `api_key`, `start_month`, `end_month`

**可选参数**: `platform_ids`, `brand_ids`

**功能**: 各平台一级类目销量、销额分布

**返回字段**: 
| 字段 | 类型 | 说明 |
|-----|------|-----|
| global_cid | string | 品类ID |
| global_cate_name | string | 品类英文名 |
| global_cate_name_cn | string | 品类中文名 |
| sales_total | string | 销售额 |
| num_total| bigint| 销量 |

**返回示例**:
```json
{
  "code": 0,
  "data": {
    "currency_unit": "CNY",
    "global_category_lv1_list": [
      {
        "global_cid": "2011010112",
        "global_cate_name": "3C Electronics",
        "global_cate_name_cn": "3C数码",
        "sales_total": "41108867869.92",
        "percentage": "15.26"
      },
      {
        "global_cid": "2011010116",
        "global_cate_name": "Household Decorations",
        "global_cate_name_cn": "家装家饰",
        "sales_total": "35212105501.35",
        "percentage": "13.07"
      }
    ],
    "total": "269382366750.38"
  },
  "msg": "获取一级类目占比成功"
}
```

**注意事项**:
- 不传 `platform_ids` 返回所有有权限市场的汇总数据
- `sales_total` 和 `percentage` 均为字符串类型

---

#### A2. Top品牌排行
```
POST /api/skill/get-global-top-brands-list
```

**必选参数**: `api_key`, `start_month`, `end_month`

**可选参数**: `platform_ids`, `cid_ids`

**功能**: 各平台 Top 品牌（按平台分组）

**返回字段**: 
| 字段 | 类型 | 说明 |
|-----|------|-----|
| brand_id | int | 品牌ID |
| brand_name | string | 品牌名 |
| item_num | int | 商品数 |
| num_total | int | 销量 |
| sales_total | string | 销售额 |
| shop_num | int | 店铺数 |
| avg_price | float | 均价 |
| platform_id/name/name_cn | - | 平台信息 |

**返回示例**:
```json
{
  "code": 0,
  "data": {
    "topBrandSalesList": {
      "Amazon@United States": [
        {
          "brand_id": 123,
          "brand_name": "Apple",
          "item_num": 150,
          "num_total": 50000,
          "sales_total": "25000000",
          "shop_num": 10,
          "avg_price": 500.0,
          "platform_id": 47,
          "platform_name": "Amazon@United States",
          "platform_name_cn": "亚马逊@美国"
        }
      ]
    }
  },
  "msg": "获取Top品牌列表成功"
}
```

---

#### A3. Top店铺排行
```
POST /api/skill/get-global-top-shop-list
```

**必选参数**: `api_key`, `start_month`, `end_month`

**可选参数**: `platform_ids`, `cid_ids`

**功能**: 各平台 Top 店铺（按平台分组）

**返回字段**: 
| 字段 | 类型 | 说明 |
|-----|------|-----|
| shop_id | int | 店铺ID |
| shop_name | string | 店铺名 |
| brand_num | int | 品牌数 |
| item_num | int | 商品数 |
| num_total | int | 销量 |
| sales_total | string | 销售额 |
| avg_price | float | 均价 |
| platform_id/name/name_cn | - | 平台信息 |

---

#### A4. Top商品排行
```
POST /api/skill/get-global-top-items-list
```

**必选参数**: `api_key`, `start_month`, `end_month`, `platform_ids`

**可选参数**: `cid_ids`

**功能**: 各平台 Top 商品（按平台分组）

**返回字段**: 
| 字段 | 类型 | 说明 |
|-----|------|-----|
| item_id | string | 商品ID |
| item_name | string | 商品名 |
| item_name_cn | string | 商品中文名 |
| sku_id | string | SKU ID |
| img | string | 商品图片URL |
| _cid | string | 细分类目ID |
| cate_name | string | 类目名 |
| full_cate_name | string | 完整类目路径 |
| num_total | int | 销量 |
| sales_total | string | 销售额 |
| avg_price | float | 均价 |

**注意事项**:
- ⚠️ `platform_ids` 为必选，不传返回空
- ⚠️ 建议一次最多查 3 个平台（超出可能影响性能）
- ⚠️ 不支持 `brand_ids` 筛选，品牌筛选请使用 B6 接口

---

### B组：品牌概览（brand_ids 和 cid_ids 均为必选）

#### B5. 品牌总览
```
POST /api/skill/get-global-overview
```

**必选参数**: `api_key`, `start_month`, `end_month`, `brand_ids`, `cid_ids`

**功能**: 品牌汇总数据（不分市场）

**返回字段**: 
| 字段 | 类型 | 说明 |
|-----|------|-----|
| item_num | int | 商品数 |
| num_total | int | 总销量 |
| sales_total | string | 总销售额 |
| shop_num | int | 店铺数 |

**返回示例**:
```json
{
  "code": 0,
  "data": {
    "marketOverviewData": [
      {
        "item_num": 100,
        "num_total": 5000,
        "sales_total": "250000",
        "shop_num": 20
      }
    ]
  },
  "msg": "获取品牌总览成功"
}
```

---

#### B6. 品牌各站点详情 + Top商品
```
POST /api/skill/get-global-overview-group-by-market-id-with-top-items
```

**必选参数**: `api_key`, `start_month`, `end_month`, `brand_ids`, `cid_ids`

**可选参数**: `platform_ids`

**功能**: 品牌各站点详情 + Top3 商品

**返回字段**: 
| 字段 | 类型 | 说明 |
|-----|------|-----|
| market_id | string | 市场ID |
| market_name | string | 市场英文名 |
| market_name_cn | string | 市场中文名 |
| num_total | int | 销量 |
| sales_total | string | 销售额 |
| item_num | int | 商品数 |
| shop_num | int | 店铺数 |
| top_items | array | Top商品列表 |

**top_items 字段**:
| 字段 | 类型 | 说明 |
|-----|------|-----|
| item_id | string | 商品ID |
| item_name | string | 商品名 |
| img | string | 商品图片 |
| num_total | int | 销量 |
| sales_total | string | 销售额 |
| avg_price | float | 均价 |
| cate_name | string | 类目名 |

**返回示例**:
```json
{
  "code": 0,
  "data": {
    "MarketOverview": [
      {
        "market_id": "3",
        "market_name": "Shopee@Malaysia",
        "market_name_cn": "虾皮@马来西亚",
        "num_total": 697,
        "sales_total": "18092.23",
        "item_num": 85,
        "shop_num": 24,
        "top_items": [
          {
            "item_id": "9610276580",
            "item_name": "TAIWAN UNI-PRESIDENT 麦香红茶",
            "img": "xxx",
            "num_total": 28,
            "sales_total": "5039.08",
            "avg_price": 144.25,
            "cate_name": "Tea & Tea Bags"
          }
        ]
      }
    ],
    "currency_unit": "CNY"
  },
  "msg": "获取各站点详情成功"
}
```

**注意事项**:
- ⚠️ `brand_ids` 和 `cid_ids` 均不可省略
- ⚠️ 传多个 `brand_ids` 时返回合并数据（不区分品牌）
- ⚠️ `top_items` 可能返回超过 3 条（同商品不同 SKU），需按商品名去重

---

### C组：品类概览（cid_ids 为必选）

#### C7. 品类各站点销售分布
```
POST /api/skill/get-global-overview-group-by-market-id
```

**必选参数**: `api_key`, `start_month`, `end_month`, `cid_ids`

**可选参数**: `platform_ids`

**功能**: 品类各站点销量、销额

**返回字段**: 
| 字段 | 类型 | 说明 |
|-----|------|-----|
| market_id | string | 市场ID |
| market_name | string | 市场英文名 |
| market_name_cn | string | 市场中文名 |
| num_total | int | 销量 |
| sales_total | string | 销售额 |

**注意事项**:
- 不传 `platform_ids` 返回所有有权限的市场

---

#### C8. 品类各站点 Top 品牌
```
POST /api/skill/get-global-overview-group-by-market-id-with-top-brand
```

**必选参数**: `api_key`, `start_month`, `end_month`, `cid_ids`

**可选参数**: `platform_ids`

**功能**: 品类各站点 Top 品牌

**返回字段**: C7 字段 + `top_brand` 列表

**top_brand 字段**:
| 字段 | 类型 | 说明 |
|-----|------|-----|
| brand_id | int | 品牌ID |
| brand_name | string | 品牌名 |
| item_num | int | 商品数 |
| num_total | int | 销量 |
| sales_total | string | 销售额 |
| shop_num | int | 店铺数 |
| avg_price | float | 均价 |

---

#### C9. 品类各站点 Top 店铺
```
POST /api/skill/get-global-overview-group-by-market-id-with-top-shop
```

**必选参数**: `api_key`, `start_month`, `end_month`, `cid_ids`

**可选参数**: `platform_ids`

**功能**: 品类各站点 Top 店铺

**返回字段**: C7 字段 + `top_shops` 列表

**top_shops 字段**:
| 字段 | 类型 | 说明 |
|-----|------|-----|
| shop_id | int | 店铺ID |
| shop_name | string | 店铺名 |
| item_num | int | 商品数 |
| brand_num | int | 品牌数 |
| num_total | int | 销量 |
| sales_total | string | 销售额 |
| avg_price | float | 均价 |

---

## 辅助接口

### 申请临时 api_key
```
POST /api/skill/generate-normal-api-key
```

**参数**: 无

**返回示例**:
```json
{
  "code": 0,
  "data": {
    "api_key": "e795672d29f5fc35...",
    "ip": "8.218.55.169"
  },
  "msg": "生成api_key成功"
}
```

### 查询账号权限范围（数据权限范围，账号过期时间，剩余额度等）
```
POST /api/skill/get-current-api-key-allow-range
```

**参数**: `api_key`（必选）

**返回示例**:
```json
{
  "code": 0,
  "data": {
	"expire_at": "2026-05-31T23:56:45Z",
	"level_text": "高级",
	"query_from": "2023-01-01",
	"query_to": "2026-06-30",
	"remaining_quota": "141",
	"status_text": "正常"
  },
  "msg": "查询成功"
}
```

### 异常记录
```
POST /api/skill/record-openclawd-anomaly
```

**参数**: 
| 参数 | 类型 | 必选 | 说明 |
|-----|------|------|-----|
| api_key | string | 是 | 认证令牌 |
| title | string | 否 | 异常标题 |
| description | string | 否 | 描述 |
| details | string | 否 | 详情 JSON |

**返回示例**:
```json
{
  "code": 0,
  "msg": "记录成功"
}
```

---

## 请求示例

### 查询亚马逊美国站一级类目分布
```bash
curl -s -X POST "https://asia-test-private.nint.hk/api/skill/get-global-primary-categories" -H "Content-Type: application/json" -d '{"api_key":"xxx","start_month":"2026-01","end_month":"2026-01","platform_ids":[47]}'
```

### 查询美容护理品类在东南亚的 Top 品牌（C8）
```bash
curl -s -X POST "https://asia-test-private.nint.hk/api/skill/get-global-overview-group-by-market-id-with-top-brand" -H "Content-Type: application/json" -d '{"api_key":"xxx","start_month":"2026-01","end_month":"2026-01","cid_ids":["2011010113"],"platform_ids":[1,2,3]}'
```

### 查询统一品牌在食品保健品类下的各站点表现（B6）
```bash
curl -s -X POST "https://asia-test-private.nint.hk/api/skill/get-global-overview-group-by-market-id-with-top-items" -H "Content-Type: application/json" -d '{"api_key":"xxx","start_month":"2026-01","end_month":"2026-01","brand_ids":[63114],"cid_ids":["2011010118"]}'
```

### 查询品牌列表（模糊匹配）
```bash
curl -s -X POST "https://asia-test-private.nint.hk/api/skill/get-brand-list" -H "Content-Type: application/json" -d '{"api_key":"xxx","brand_like":"统一"}'
```
