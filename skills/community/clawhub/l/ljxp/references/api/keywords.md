# 关键词接口

用于热搜词查询、关键词趋势、蓝海词筛选和 Listing SEO 研究。

## 对应脚本

- 热搜词查询：`scripts/search_keywords.py`（`--search-type day` 或 `month`）

## 接口选择规则

`/keywords/search` 支持 2 种粒度（**二选一，不要都查**）：

| searchType | 何时调用 | 何时不调 |
|---|---|---|
| `day` | 最近热搜词、短期流量词、今日/本周热门 | 要长期趋势、月度对比、季节性 |
| `month` | 本月热搜、月度关键词、长期热门、季节性判断 | 只看短期波动、某日热度 |

**调用边界**：不要默认超大 pageSize，先拿 50 个。用户未指定类目可不筛 `categoryId`。拿到关键词后按需用 `/items/search` 按 title 验证供给，**不要每个关键词都跑商品搜索**。

---

## POST /keywords/search 热搜词查询

> ⚡ 每次 **3 积分** ｜ 方法：POST

### 请求参数

| 必填 | 参数 | 说明 |
|:-:|---|---|
| ✅ | siteId | `MLM`/`MLB`/`MLC`/`MLA`/`MCO` |
| ✅ | searchType | `day`（日度，默认）/ `month`（月度） |
| ✅(day) | runDate | 日期 `YYYY-MM-DD`（=今天可省略） |
| ✅(month) | runMonth | 月份 `YYYYMM` |
| | runWeek | 周度 1~53 |
| | searchText / keySearch | 模糊/精搜关键词 |
| | categoryId | 类目 ID（可选=全类目） |
| | sort.key + sort.order | `sale30`/`visit30`/`viewCount`/`itemCount` + `asc`/`desc` |
| | pageNo/pageSize | 默认 1/50 |

### CLI 映射

`siteId→--site`，`searchType→--search-type`，`runDate→--run-date`，`runMonth→--run-month`，`runWeek→--run-week`，`searchText→--search-text`，`keySearch→--key-search`，`categoryId→--category-id`，`sort.key→--sort-key`，`sort.order→--sort-order`。**day/month 二选一，不同时传**。

```bash
# 日度 + 精搜 phone（keySearch 精搜）
python scripts/search_keywords.py --token <TKN> --site MLM --search-type day --run-date 2026-03-17 --key-search phone

# 月度 + 类目 + 30天销量倒序
python scripts/search_keywords.py --token <TKN> --site MLB --search-type month --run-month 202603 \
  --category-id MLB1051 --sort-key sale30 --sort-order desc
```

### 关键字段

- `ResultItem`: `dataType（day/month）` / `key / keyCn` / `visit30` / `itemCount / itemTotalCount` / `viewCount` / `sale30` / `categoryIds[]` / `history[]`
- `HistoryItem`: `date` / `sale30` / `totalItem` / `visit30`

**蓝海词判断**：搜索/访问高、30天销量好、商品数相对低。

---

## 本模块积分明细表

| 接口 | 功能 | 积分 |
|---|---|---:|
| `POST /keywords/search` | 热搜词查询（日度/月度） | 3 |
