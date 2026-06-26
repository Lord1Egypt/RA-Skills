# Known Limitations

基于当前真实 smoke test，以下情况已确认：

## 已验证可用
- `/quotes/get_market_snapshot`
- `/infos/get_market_state`
- `/quote/get_global_state`
- `/quotes/get_rt_data`
- `/quotes/get_rt_ticker`
- `/quotes/get_broker_queue`
- `/quotes/get_cur_kline`
- `/quotes/get_cur_kline_date`
- `/infos/get_capital_flow`
- `/quote/get_stock_basicinfo`
- `/quote/request_trading_days`
- `/infos/get_us_analysis`
- `/quote/get_ipo_list`
- `/rank/get_stock_rank`

## 当前环境暂不支持或未验证通过
- `/infos/shareholder_inc_red_hold_by_date`
  - 当前主脚本尚未接入按时间范围查询入口；按市场与按股票两条主路径已验证可用

- 美股 K 线（如 `US-AAPL`, `US-NVDA`）
  - 自然语言路由已能正确识别为 `kline`
  - 但当前接口调用返回 HTTP 404
  - 初步判断：问题更可能在后端环境、代码格式或市场支持范围，而不是前端路由逻辑

## Implementation Guidance

- 对未验证通过的能力，不要在主路径里强承诺。
- 如果用户问到这些能力，可以尝试调用；若失败，直接说明当前环境暂不支持，而不是误导成“没有数据”。
- 对 404 场景，优先解释为“当前环境下该标的或该参数暂不可用”，不要直接把原始 message 当成用户提示。
- 后续如环境开放或拿到正确入参规范，再升级这些能力为正式支持。
