# Plates and Basic Info

核心接口：
- `/quote/get_plate_list`
- `/quote/get_plate_stock`
- `/quote/get_stock_basicinfo`

## Plate List

用于：
- 查询某市场下的子板块
- 查询行业 / 概念 / 地域板块

## Plate Stocks

用于：
- 查询某板块的成分股
- 获取板块内股票列表

默认返回：
- 板块名称
- 成分股数量或分页结果
- 可选：挑出前几只代表股票

## Basic Info

用于：
- 查询股票基础信息
- 上市日期
- 每手股数
- 是否退市

默认摘要：
- 股票名称 / 代码
- 市场
- 每手股数
- 上市日期
- 是否退市

## Notes

`get_plate_stock` 文档当前疑似存在参数引用问题：
- `plate_code` 不应引用 `PlateStockSortField`
后续实现时建议按真实服务行为校正。
