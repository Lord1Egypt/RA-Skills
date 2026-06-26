---
name: housing-price-data
description: 'Fetch official Chinese 70-city residential property price index data from the National Bureau of Statistics (国家统计局). Use when users ask about 房价指数, housing trends, 环比, 同比, 定基, 新建商品住宅, 二手住宅, or recent housing price movement for any of the 70 major cities such as 北京, 上海, 广州, 深圳, 武汉.'
metadata:
  author: jiangshengcheng
  version: "2.2.3"
---

# 中国70城住宅价格指数数据技能

本技能通过国家统计局 RSS 抓取《70个大中城市商品住宅销售价格变动情况》，返回可直接供 agent 总结的结构化数据。

依赖：Python 3、`requests`、`beautifulsoup4`，以及在需要图表时可用的 `matplotlib`。运行时需要能访问 `stats.gov.cn`。

## 何时使用

- 用户问某个 70 城城市最近房价走势、环比/同比/定基指数
- 用户要看新建商品住宅或二手住宅的价格指数
- 用户要最新一期官方数据，或指定近几期历史数据
- 用户需要图表辅助分析

## 快速流程

1. 先告知用户正在从国家统计局获取官方数据。
2. 判断需求是“最新一期”还是“历史走势”：
   - 最新一期：使用 `--latest`
   - 历史走势：使用 `--limit <N>`
3. 运行脚本：

```bash
python3 scripts/fetch_data.py --city <城市> --metrics <指标> --latest
python3 scripts/fetch_data.py --city <城市> --metrics <指标> --limit 24
python3 scripts/fetch_data.py --city <城市> --chart --limit 24
```

4. 读取 JSON 输出中的顶层字段，再决定如何组织回答。
5. 以表格或简短摘要呈现，不要把原始 JSON 直接贴给用户，除非用户明确要求。

## 常用参数

- `--city`：目标城市，支持常见输入变体，如 `北京市`
- `--metrics`：逗号分隔，支持 `环比`、`同比`、`定基`
- `--latest`：只返回最新一期
- `--limit`：返回最近 N 期历史数据
- `--chart`：生成图表
- `--output`：图表输出路径
- `--no-cache`：禁用缓存

指标别名可直接输入：`mom`、`yoy`、`环比指数`、`同比指数`、`fixed-base`。

## 输出重点

重点看这些字段：

- `requested_city`：用户请求的城市输入
- `matched_city`：脚本最终匹配到的规范城市名
- `latest_period`：本次结果中的最新期次
- `record_count`：返回记录数
- `records`：核心数据

`records` 中每条记录包含：

- `period`
- `city`
- `indicator`
- `metrics`
- `source_url`

## 呈现建议

- 默认优先展示最新一期或最近几期结果
- 指标名可简写为：
  - `新建商品住宅销售价格指数` -> `新建商品住宅`
  - `二手住宅销售价格指数` -> `二手住宅`
- 指数以 `100` 为基准：
  - 高于 `100` 表示上涨
  - 低于 `100` 表示下降

## 示例

```bash
python3 scripts/fetch_data.py --city 武汉 --metrics 环比,同比 --latest
python3 scripts/fetch_data.py --city 上海市 --metrics yoy --limit 12
python3 scripts/fetch_data.py --city 北京 --metrics 环比,同比 --chart --limit 24
```

## 参考资料

- 城市列表和指标说明：`references/REFERENCE.md`
- 数据来源：国家统计局 RSS 与公告正文
- 注意：这里是价格指数，不是绝对房价

## 注意事项

- 国家统计局通常在每月中旬发布上月数据
- 网络受限时可能出现 RSS 或详情页抓取失败
- 图表默认保存到当前 skill 目录，可用 `--output` 覆盖
