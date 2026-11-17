# 跨平台电商 skills

**18 个 skill**，覆盖非亚马逊平台：TikTok Shop（FastMoss / EchoTik）/ Shopee（友鹰）/ Walmart（原生 + WallySmarter）/ eBay / Ozon（MPStats）/ 1688（DLD / 以图搜图）/ 独立站 / TSearch 通用搜索。

**归属 agent**：全部挂载在 `default`。`linkfox-market-analysis-agent` / `linkfox-product-selection-agent` 也继承。

**不确定用哪个 agent？** → 用 `default`。default 包含本桶全部 18 个 skill。

## Skills

| skill | 平台 | 用途 | 入参（关键字段） | 返回摘要 |
|---|---|---|---|---|
| `linkfox-1688-search-by-image` | 1688 | 以图搜图找同款货源 | `imageUrl` (图片URL, 与base64/imageId三选一), `page`, `filter`, `sort` | 商品列表JSON（offerId/title/price/salesQuantity/repurchaseRate/sellerIdentities） |
| `linkfox-dld-product-billboard` | 1688 | 1688周/月热销榜单（店雷达）| `keyWord` (中文), `pageType` (2周/3月), `date` (周日或月首日), `sortField` | 榜单商品JSON（title/price/consignPrice/orderCount/saleCount/company） |
| `linkfox-dld-product-search` | 1688 | 1688关键词选品搜索（店雷达）| `keyWord` (中文), `cycle` (7/30天), `companyType` (店铺/工厂), `sortField` | 商品列表JSON（title/price/consignPrice/salesQuantity/company/shopUrl） |
| `linkfox-ebay-search` | eBay | 多站点eBay商品listing搜索 | `keyword`, `ebayDomain` (站点域名), `page`, `orderBy` (排序码) | listing列表JSON（title/price/condition/seller/sold/productUrl） |
| `linkfox-echotik-list-new-product-rank` | TikTok Shop | TikTok Shop新品热销榜（EchoTik，16站）| `date` (YYYY-MM-DD,必填), `region` (默认US), `pageNum`, `pageSize` | 新品榜JSON（title/price/totalSaleCnt/totalSaleGmv30dAmt/totalIflCnt/productRating） |
| `linkfox-echotik-list-product` | TikTok Shop | TikTok Shop商品搜索+筛选（EchoTik）| `keyword`, `region`, `minTotalSale30dCnt`, `productSortField` | 商品列表JSON（title/price/totalSale30dCnt/totalSaleGmv30dAmt/productCommissionRate/totalIflCnt） |
| `linkfox-fastmoss-product-rank-top-selling` | TikTok Shop | TikTok日/周/月热销榜（FastMoss，9站）| `region` (必填), `dateInfo` (必填, type+value), `category`, `orderby` | 热销榜JSON（title/price/totalSaleCnt/totalSaleGmvAmt/growthRate/shopName） |
| `linkfox-fastmoss-product-search` | TikTok Shop | TikTok关键词商品搜索（FastMoss，15站）| `keyword`, `region`, `commissionRateRange`, `orderField` | 商品列表JSON（title/price/totalSale7dCnt/productCommissionRate/totalIflCnt/shopName） |
| `linkfox-mpstats-ozon-brand-products` | Ozon | Ozon品牌下钻SKU销售分析 | `brandName` (必填,俄/拉丁), `filters`, `sortField`, `currency` | SKU列表JSON（productId/title/price/sales/revenue/rating/balance/lostProfit） |
| `linkfox-mpstats-ozon-category-products` | Ozon | Ozon类目下钻爆款/蓝海挖掘 | `categoryPath` (必填,俄语全路径), `filters`, `sortField`, `currency` | SKU列表JSON（productId/title/price/sales/revenue/rating/balance/categoryPosition） |
| `linkfox-mpstats-ozon-product-detail` | Ozon | Ozon商品卡批量详情（≤100个SKU）| `productIds` (必填,≤100), `startDate`, `endDate`, `includeFbs` | SKU详情JSON（title/price/rating/reviews/monthlySalesUnits/revenue/lostProfit/stock） |
| `linkfox-mpstats-ozon-product-search` | Ozon | Ozon关键词/SKU反查基础卡片 | `keyword` (俄语) 或 `productIds` (二选一), `startDate`, `endDate` | 基础商品JSON（productId/title/brand/sellerName/productPageUrl/imageUrl） |
| `linkfox-mpstats-ozon-product-trend` | Ozon | Ozon单SKU分日销量/价格走势 | `productId` (必填), `startDate`, `endDate`, `includeSearchStats` | 分日时间序列JSON（date/sales/price/balance/rating/searchPosition） |
| `linkfox-mpstats-ozon-seller-products` | Ozon | Ozon卖家店铺下钻SKU分析 | `sellerId` (必填,数字), `filters`, `sortField`, `currency` | SKU列表JSON（productId/title/price/sales/revenue/rating/balance/lostProfit） |
| `linkfox-tsearch-search` | 通用 | 网络搜索并抽取网页内容 | `keyword` (必填,≤1000字) | 搜索结果JSON（searchList: title/url/content/score, costToken） |
| `linkfox-wallysmarter-product-detail` | Walmart | Walmart商品详情+价格/销量历史 | `productId` (必填, ItemId), `includeStats` | 商品详情JSON（title/price/rating/reviews/salesEstimate/revenue/stats） |
| `linkfox-walmart-search` | Walmart | Walmart商品listing搜索 | `keyword` 或 `categoryId` (二选一), `sort`, `page`, `minPrice`/`maxPrice` | 商品列表JSON（productId/title/price/rating/reviews/sellerName/productPageUrl） |
| `linkfox-youying-shopee-get-product-infos` | Shopee | Shopee 11站点商品搜索+筛选（友鹰）| `station` (必填,站点), `keyword`, `keywordType`, `page` | 商品列表JSON（pid/title/price/sold/estimateSold/rating/shopName/cbOption） |
