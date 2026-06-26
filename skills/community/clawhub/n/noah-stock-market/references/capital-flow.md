# Capital Flow

核心接口：
- `/infos/get_capital_flow`

## Suitable Questions

- 个股资金流向
- 主力资金净流入 / 净流出
- 大单 / 中单 / 小单流向

## Default Output

默认展示：
- 整体净流入
- 主力大单净流入
- 特大单净流入
- 大单 / 中单 / 小单净流入
- 数据有效时间

## Summary Rule

优先总结资金方向：
- 净流入 → 偏强
- 净流出 → 偏弱
- 主力与小单方向相反时，提示分歧

保持客观，不把资金流向直接解释成交易建议。
