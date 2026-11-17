---
name: jdjr-gold-search
description: 查询黄金、白银、铂金等贵金属的实时行情与历史走势/K线（京东金融数据源，免 OAuth 登录）。适用于"黄金现在多少钱"、"白银多少钱"、"黄金近一个月走势"、"黄金K线"等请求。
---

# 黄金/贵金属行情与历史走势查询（京东金融）

查询黄金、白银、铂金等贵金属的**实时行情**（现价、涨跌、今开、昨收、最高、最低、成交量）与**历史走势 / K线**（近 N 天走势、日/周/月 K线）。

> 数据源为京东金融公开行情接口，免登录（无需 OAuth）。

## 什么时候用

用户想查询以下内容时：
- 黄金、白银、铂金实时行情、价格、涨跌 → 走 `jdjr_query_gold.py`
- 黄金、白银、铂金历史走势、近 N 天/月走势、K线、走势图 → 走 `jdjr_query_stock.py`

支持品种：
- 黄金：`Au99.99`、`Au99.95`、`Au100g`、`Au(T+D)`、`mAu(T+D)`、`iAu99.99`
- 白银：`Ag99.99`、`Ag(T+D)`
- 铂金：`Pt99.95`
- 期货黄金：`au2602`（沪金）

> 历史走势 / K线的品种代码需带 `SGE-` 前缀（上海黄金交易所），如 `SGE-Au99.99`、`SGE-Ag99.99`、`SGE-Pt99.95`。

## 怎么用

### 实时行情（jdjr_query_gold.py）

```bash
# 黄金实时行情
python3 scripts/jdjr_query_gold.py Au99.99

# 白银实时行情
python3 scripts/jdjr_query_gold.py Ag99.99

# 列出所有支持的品种
python3 scripts/jdjr_query_gold.py --list
```

### 历史走势 / K线（jdjr_query_stock.py）

品种代码需带 `SGE-` 前缀。

```bash
# 黄金近 15 天走势（纯文字走势描述，对客首选）
python3 scripts/jdjr_query_stock.py chart SGE-Au99.99 --days 15

# 白银近一个月走势
python3 scripts/jdjr_query_stock.py chart SGE-Ag99.99 --days 30

# 黄金日/周/月 K线原始数据（JSON，需二次格式化）
python3 scripts/jdjr_query_stock.py kline SGE-Au99.99 --k-type day
python3 scripts/jdjr_query_stock.py kline SGE-Au99.99 --k-type week
python3 scripts/jdjr_query_stock.py kline SGE-Au99.99 --k-type month
```

> `--days` 建议不超过 30 天。`chart` 直接产出可读文字走势，`kline` 输出原始 JSON 需按 [references/jdjr-output-format.md](references/jdjr-output-format.md) 走势格式转述。

### 意图识别

| 用户说 | 使用脚本 |
|--------|----------|
| 黄金/白银/铂金现在多少钱、实时行情 | `jdjr_query_gold.py {品种代码}` |
| 列出所有黄金品种 | `jdjr_query_gold.py --list` |
| 黄金/白银近 N 天/一个月走势、走势图 | `jdjr_query_stock.py chart SGE-{品种} --days N` |
| 黄金/白银 K线、日K/周K/月K | `jdjr_query_stock.py kline SGE-{品种} --k-type day/week/month` |

> 说明：本 Skill 主 SKILL.md 的「金价走势分析」（`query_price_jhub.py --analyze`）解读的是京东 24h 金价的**当日**走势；此处 `jdjr_query_stock.py` 提供的是贵金属**近 N 天/多日历史**走势与 K线，二者互补。

## 怎么对用户输出（严格按照以下格式输出）

详细格式规范见 [references/jdjr-output-format.md](references/jdjr-output-format.md)。

- 实时行情：`jdjr_query_gold.py` 已产出 Markdown 表格并附来源标注，直接转述。
- 历史走势：`jdjr_query_stock.py chart` 已产出文字走势描述并附来源标注，直接转述。
- K线原始 JSON：按 jdjr-output-format.md「历史走势」格式整理后输出，结尾附「💡 本信息由 [京东金融](链接) 提供」。

## 失败处理

- 品种代码错误 → "请使用正确的品种代码，如 Au99.99、Ag99.99，或让我列出所有支持的品种"
- 历史走势代码缺 `SGE-` 前缀 → 自动补全为 `SGE-{品种}` 后重试
- 接口失败 → 先按全局规则重试；多次失败再提示"查询暂时失败，请稍后重试"
- 查不到数据 → "未找到相关数据"