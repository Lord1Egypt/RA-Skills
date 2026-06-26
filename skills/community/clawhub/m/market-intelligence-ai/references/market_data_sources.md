---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_4dd4a72f5cc411f1abc85254006c9bbf
    ReservedCode1: 28uGLmQsMw3+4tSoQ4HTCQVMi3t+208rKrP4gVjOYZM/JsC64m/xMF2CHjSHRT8YmrkrTFnGEVswtXJ6mjqtz4I94Eq77Dr/CMCAjUrj5lnmJIUkfBZ6NLXNeIF+zBpJnnTjSjABgwc69cv0WXo1UTELMDUReHlYfQnsr7OlCpU9RntxLX7Lv4SpF/s=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_4dd4a72f5cc411f1abc85254006c9bbf
    ReservedCode2: 28uGLmQsMw3+4tSoQ4HTCQVMi3t+208rKrP4gVjOYZM/JsC64m/xMF2CHjSHRT8YmrkrTFnGEVswtXJ6mjqtz4I94Eq77Dr/CMCAjUrj5lnmJIUkfBZ6NLXNeIF+zBpJnnTjSjABgwc69cv0WXo1UTELMDUReHlYfQnsr7OlCpU9RntxLX7Lv4SpF/s=
---

# 市场数据源参考手册

本文件列出可用的稳定、合规电商公开数据源，按可靠性排序。

---

## 一、主数据源（已验证稳定）

### 1. Keepa — Amazon 价格与销量追踪 API

| 属性 | 值 |
|------|-----|
| 端点 | `https://api.keepa.com/product` |
| 协议 | HTTPS GET，返回 JSON |
| 认证 | API Key 参数 `key={YOUR_KEY}` |
| 覆盖 | Amazon 全站点（US/UK/DE/JP 等） |
| 数据字段 | 价格历史、BSR 排名曲线、库存状态、Buy Box 价格 |
| 免费额度 | 每月 300 tokens（约 30-50 次查询） |
| 可靠度 | ⭐⭐⭐⭐⭐（自 2013 年运营） |

请求示例：
```
GET https://api.keepa.com/product?key={API_KEY}&asin=B0A1B2C3D4&domain=1
```

响应字段：
- `products[].csv` — CSV 格式的时间序列数据（价格 / BSR / 评分 / 评论数）
- `products[].stats` — 统计摘要：均价、最低价、BSR 均值

---

### 2. Amazon Product Advertising API 5.0（PAAPI）

| 属性 | 值 |
|------|-----|
| 端点 | `https://webservices.amazon.com/paapi5/` |
| 协议 | HTTPS POST，JSON 体 |
| 认证 | AWS Signature V4（Access Key + Secret Key） |
| 覆盖 | Amazon 全站点，官方 API 最合规 |
| 数据字段 | 标题、价格、评分、评论数、BSR、图片、ASIN、变体 |
| 免费额度 | 注册 Amazon Associates 后，每月 8640 次免费调用 |
| 可靠度 | ⭐⭐⭐⭐⭐（Amazon 官方） |

请求示例：
```json
POST /paapi5/searchitems
{
    "Keywords": "air fryer",
    "ItemCount": 5,
    "Resources": [
        "ItemInfo.Title",
        "Offers.Listings.Price",
        "CustomerReviews.Count",
        "CustomerReviews.StarRating",
        "SalesRank"
    ]
}
```

---

### 3. Rainforest API（Amazon 非官方爬虫 API）

| 属性 | 值 |
|------|-----|
| 端点 | `https://api.rainforestapi.com/request` |
| 协议 | HTTPS POST，JSON 体 |
| 认证 | API Key 参数 |
| 覆盖 | Amazon 全站点，支持搜索、详情页、评论、Best Sellers |
| 免费额度 | 每月 100 次 |
| 可靠度 | ⭐⭐⭐⭐ |

---


### 4. SerpAPI — Google Shopping 搜索结果

| 属性 | 值 |
|------|-----|
| 端点 | `https://serpapi.com/search` |
| 协议 | HTTPS GET |
| 认证 | API Key 参数 `api_key={YOUR_KEY}` |
| 覆盖 | Google Shopping（多电商平台商品聚合） |
| 数据字段 | 标题、价格、商店名、评分、链接 |
| 免费额度 | 每月 100 次 |
| 可靠度 | ⭐⭐⭐⭐ |

请求示例：
```
GET https://serpapi.com/search?engine=google_shopping&q=air+fryer&api_key={YOUR_KEY}
```

---

### 5. Open Food Facts（公开数据集，免费无限制）

| 属性 | 值 |
|------|-----|
| 端点 | `https://world.openfoodfacts.org/api/v2/search` |
| 协议 | HTTPS GET，JSON |
| 认证 | 无需（完全开放） |
| 覆盖 | 全球食品/消费品条码数据，含价格趋势 |
| 免费额度 | 无限制 |

> 用于食品和消费品类目的辅助校验，数据权威但品类有限。

---

## 二、备用数据源

| 数据源 | 覆盖 | 限制 | 适用场景 |
|--------|------|------|----------|
| Google Trends RSS | 搜索热度趋势 | 无具体商品数据 | 行业趋势判断 |
| Census.gov API | 美国宏观消费数据 | 粒度粗 | 行业大背景分析 |
| Kaggle Amazon Dataset | 历史静态数据集 | 非实时 | 离线训练/校准 |
| AliExpress Dropshipping API | AliExpress 商品 | 需注册卖家 | 跨境电商选品 |

---

## 三、数据采集优先级

```
官方 API（PAAPI）> Keepa > Rainforest > SerpAPI > 公开数据集
```

原则：
1. 优先使用官方 API — 合规性最高，无法律风险
2. 付费 API 优先于爬虫 — 稳定性好，反爬风险低
3. 查询频率限制在每源 1次/秒 — 避免触发限流
4. 所有数据标注来源和获取时间，确保可追溯

---

## 四、API Key 环境变量映射

| 变量名 | 对应数据源 |
|--------|-----------|
| `KEEPA_API_KEY` | Keepa |
| `AMAZON_ACCESS_KEY` + `AMAZON_SECRET_KEY` | PAAPI 5.0 |
| `RAINFOREST_API_KEY` | Rainforest API |
| `SERPAPI_KEY` | SerpAPI / Google Shopping |
| `STOCK_API_KEY` | 金融市场数据（如需商品期货价格） |
| `ALIPAY_APP_ID` | 支付宝 AI 收（收费验证） |

---

## 五、降级策略

当所有实时 API 不可用时（如 API Key 过期、网络故障）：

1. 回退到 **静态公开数据集**（Kaggle Amazon Reviews 2023）
2. 输出报告中明确标注 「数据源：历史公开数据集（非实时）」
3. 不收取进阶版/专业版费用，自动降为基础版（免费）

---

## 六、法律合规声明

- PAAPI 5.0 需遵守 [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/agreement)
- Keepa 数据仅用于分析，不得转售
- 爬虫类 API 需遵守目标网站的 robots.txt
- 报告中不展示用户个人身份信息（PII）
*（内容由AI生成，仅供参考）*
