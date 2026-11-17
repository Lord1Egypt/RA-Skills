# IO 契约 — competitor-selector

## 输入

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| asin | string | 是 | — | 目标ASIN |
| marketplace | string | 否 | US | 站点代码 |
| product_type | string | 否 | auto | auto/standard/non-standard/mixed |
| price_tolerance | float | 否 | 0.2 | 价格浮动比例 ±20% |
| overlap_threshold | float | 否 | 0.8 | 功能/外观重合度阈值 |
| max_competitors | int | 否 | 10 | 最终竞品数量上限 |

## 中间数据落盘

落盘到 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/`：

| 文件前缀 | 步骤 | 内容 |
|----------|------|------|
| linkfox-amazon-product-detail-*.json | S0 | 目标ASIN详情(五点/规格/图片) |
| linkfox-sellersprite-traffic-keyword-*.json | S1 | 流量词反查(含翻页) |
| linkfox-amazon-search-*.json | S2 | 前台搜索结果 |
| linkfox-amazon-search-by-image-*.json | S2 | 以图搜图结果(非标品路径) |
| linkfox-keepa-product-request-*.json | S3 | Keepa历史数据 |
| linkfox-aigc-textgen-*.json | S4 | AIGC功能/外观对比结果 |
| linkfox-aba-intelligent-query-*.json | S4b | ABA TOP3反查 |

## 评分脚本 IO

### competitor_selector.py

**输入** (stdin JSON):
```json
{
  "target": {
    "asin": "B0XX",
    "bsr": 767,
    "reviews": 2813,
    "price": 37.99,
    "conv_rate": 4.09,
    "monthly_sales": 1000,
    "launch_date": "20240827"
  },
  "candidates": [
    {
      "asin": "B0YY",
      "brand": "Aiandcc",
      "price": 35.98,
      "bsr": 1966,
      "reviews": 708,
      "conv_rate": 7.22,
      "monthly_sales": 1000,
      "launch_date": "20250329",
      "sales_history": [500,500,1000,2000,3000,1000],
      "rank_30": 1921,
      "rank_180": 1836,
      "aba_kw_count": 34
    }
  ],
  "overlap_scores": {"B0YY": 0.92},
  "product_type": "standard",
  "options": {"max_competitors": 10}
}
```

**输出** (stdout JSON):
```json
{
  "target_asin": "B0XX",
  "product_type": "standard",
  "search_date": "2026-08-07",
  "direct_competitors": [
    {
      "asin": "B0YY",
      "brand": "Aiandcc",
      "price": 35.98,
      "bsr": 1966,
      "reviews": 708,
      "conv_rate": 7.22,
      "score": 3.85,
      "scores": {
        "bsr": 4,
        "reviews": 1,
        "conv": 5,
        "price": 5,
        "overlap": 4,
        "launch": 4
      },
      "overlap_ratio": 0.92
    }
  ],
  "rising_stars": [],
  "benchmarks": [
    {
      "asin": "B0ZZ",
      "brand": "AGPTEK",
      "price": 37.99,
      "bsr": 767,
      "reviews": 2813,
      "score": 3.50,
      "scores": {
        "bsr": 3,
        "reviews": 4,
        "sales": 1,
        "aba": 5,
        "price": 5
      },
      "leads": ["评论4.0x", "ABA 109词", "BSR领先61%"]
    }
  ],
  "summary": {
    "total": 5,
    "direct": 4,
    "rising": 0,
    "benchmark": 1
  }
}
```

## 最终交付

stdout 输出 JSON 结构（无文件落盘，由调用方处理）。

## 积分消耗预估

| 步骤 | 工具 | 预估积分 |
|------|------|----------|
| S0 商品详情 | amazon-product-detail | 15 |
| S1 流量词反查(含翻页) | sellersprite-traffic-keyword | 45-75 (3-5页) |
| S2 前台搜索 | amazon-search | 160 (8词×20) |
| S2 以图搜图(非标品) | amazon-search-by-image | 20 |
| S3 Keepa | keepa-product-request | 50-100 (2-4批) |
| S4 AIGC对比 | aigc-textgen | 30-90 (FLASH+PRO) |
| S4b ABA反查 | aba-intelligent-query | 6500/ASIN |
| **合计(标品,5候选)** | | **~400-600** |
| **合计(含ABA,5候选)** | | **~800-1200** |
