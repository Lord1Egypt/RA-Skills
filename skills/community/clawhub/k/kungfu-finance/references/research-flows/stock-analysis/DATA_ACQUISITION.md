# Stock Research Data Acquisition

当前仓库的 `stock-research` 不复用 source skill 中的东方财富拉数方式。
本仓库的 repo-controlled 数据采集真源如下：

## Structured Inputs

- `/api/visualization/content`
  - 用途：股票名称解析到 `instrument_id.exchange_id`
- `/api/visualization/finance`
  - 用途：主营业务、估值、概念归属、预告摘要
- `/api/visualization/finance/basic`
  - 用途：财务时间序列
- `/api/visualization/price`
  - 用途：最新价、区间涨跌
- `/api/visualization/bar`
  - 用途：主曲线所需的日 K 线

## SVG 输入规则

- 主曲线使用 `/api/visualization/bar` 的真实价格窗口。
- 周线若未接入独立公开路由，可由日线窗口本地聚合。
- 估值区间先使用当前仓库的快照映射，不在本文件承诺 source skill 的全部估值建模细节。
- 副线优先使用当前已验证的财务时间序列；未接入的资金流与行业分位保持为显式降级项。

## Search-Native Evidence

- 宏观、政策、竞争、催化剂仍属于独立 `web_search` 边界。
- 这些证据不得隐式继承 `KUNGFU_OPENKEY`。

## Current Boundary

本文件服务于当前 `kungfu_finance` repo build 的数据获取边界，不等同于 source skill 的原始外部接口说明。
