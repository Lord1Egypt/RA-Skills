# IO 契约 — competitor-research-pipeline

## 输入

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| asin | string | 是 | — | 目标ASIN |
| marketplace | string | 否 | US | 站点代码 |
| product_type | string | 否 | auto | auto/standard/non-standard/mixed |
| max_competitors | int | 否 | 10 | 竞品数量上限 |
| enable_voc | bool | 否 | true | 是否采集VOC评论 |

## 中间数据落盘

所有中间数据落盘到 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/` 目录：

| 文件前缀 | 来源步骤 | 内容 |
|----------|----------|------|
| linkfox-amazon-product-detail-*.json | S0/S1 | 商品详情(五点/规格/变体/图片) |
| linkfox-sellersprite-traffic-keyword-*.json | S1/S3 | 流量词反查(含翻页) |
| linkfox-amazon-search-*.json | S1/S2 | 前台搜索结果 |
| linkfox-keepa-product-request-*.json | S1/S2/S3 | Keepa历史数据(BSR/月销/评论) |
| linkfox-aigc-textgen-*.json | S1/S4/S6c | AIGC对比结果(功能/外观/A+) |
| linkfox-aba-intelligent-query-*.json | S1/S4b/S4 | ABA TOP3反查 |
| competitor-selector-output.json | S1/S5 | 三模型评分结果 |
| keyword-overlap-analysis.json | S6 | 首页词归因分析 |
| competitor-comparison-analysis.json | S6b | 8维度横向对比 |
| aba-overlap-analysis.json | S7 | ABA交叉对比 |

## 最终交付

HTML报告落盘到 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/reports/` 目录。

脚本 stdout 输出：
```
Saved full response: /absolute/path/to/reports/competitor-research-<timestamp>.html (<bytes> bytes)
```

## 评分脚本 IO

### competitor_selector.py

**输入** (stdin JSON):
```json
{
  "target": {"asin":"B0XX","bsr":767,"reviews":2813,"price":37.99,"conv_rate":4.09,"monthly_sales":1000,"launch_date":"20240827"},
  "candidates": [{"asin":"B0YY","brand":"...","price":35.98,"bsr":1966,"reviews":708,"conv_rate":7.22,"sales_history":[...],"rank_30":1921,"rank_180":1836,"aba_kw_count":34}],
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
  "direct_competitors": [{"asin":"...","score":3.85,"scores":{...},"overlap_ratio":0.92}],
  "rising_stars": [{"asin":"...","score":4.1,"scores":{...},"sales_data":{...}}],
  "benchmarks": [{"asin":"...","score":3.5,"scores":{...},"leads":[...]}],
  "summary": {"total":5,"direct":4,"rising":0,"benchmark":1}
}
```

### competitor_comparison_analyzer.py

**输入** (stdin JSON):
```json
{
  "asins": ["B0XX","B0YY",...],
  "labels": {"B0XX":"目标","B0YY":"直接竞品",...},
  "target_asin": "B0XX",
  "keepa_data": {"B0XX":{...}},
  "product_details": {"B0XX":{...}}
}
```

**输出** (stdout JSON): 8维度对比结果（sales_trend/market_share/deal_impact/volatility/seasonality/bsr_momentum/price_elasticity/spec_comparison）

## 积分消耗预估

| 步骤 | 工具 | 预估积分 |
|------|------|----------|
| S0 商品详情 | amazon-product-detail | 15/ASIN |
| S1 流量词反查 | sellersprite-traffic-keyword | 15/ASIN/页 |
| S1 前台搜索 | amazon-search | 20/词 |
| S1 Keepa | keepa-product-request | 240/批(5ASIN) |
| S1 AIGC对比 | aigc-textgen | 10-30/次 |
| S2 Keepa批量 | keepa-product-request | 240/批 |
| S3 卖家精灵翻页 | sellersprite-traffic-keyword | 15/页 |
| S4 ABA反查 | aba-intelligent-query | 6500/ASIN |
| S5 VOC | voc-review-analysis | ~50/ASIN |
| S6c A+分析 | aigc-textgen | 10-30/ASIN |
| **全流程合计(6ASIN)** | | **~800-1200** |
