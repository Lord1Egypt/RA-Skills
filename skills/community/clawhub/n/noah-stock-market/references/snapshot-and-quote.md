# Snapshot and Quote

核心接口：
- `/quotes/get_market_snapshot`
- `/quotes/get_stock_quote`（订阅受限）

## Default Strategy

默认优先使用 `/quotes/get_market_snapshot` 作为快照主接口。
只有在用户明确需要订阅级实时数据，且接口权限可用时，才尝试 `/quotes/get_stock_quote`。

## Default Output Fields

默认摘要优先展示：
- 名称 / 代码
- 最新价
- 涨跌额 / 涨跌幅（由 `last_price` 与 `prev_close_price` 推导）
- 今开 / 最高 / 最低
- 成交量 / 成交额
- 振幅
- 状态（停牌/正常/盘前/盘后等）
- 更新时间

## Optional Fields

用户明确要求时再补充：
- 换手率
- 市盈率 / 市净率 / TTM
- 52 周高低
- 股息率
- 盘前 / 盘后 / 夜盘详细字段
- 买一卖一价量

## Summary Style

默认先输出一句总结，再列关键数字：
- 例如："腾讯控股当前震荡偏强，最新价高于今开，日内振幅中等。"

禁止把所有原始字段无差别倾倒给用户。
