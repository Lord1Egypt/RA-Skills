# Market Status

优先使用以下接口：
- 个股所属市场状态：`/infos/get_market_state`
- 全局市场状态：`/quote/get_global_state`
- 交易日历：`/quote/request_trading_days`

## Human-Friendly Mapping

常见市场状态枚举要翻译成人话：
- `AUCTION` → 盘前竞价
- `WAITING_OPEN` → 等待开盘
- `MORNING` → 早盘交易中
- `REST` → 午间休市
- `AFTERNOON` → 午盘 / 持续交易中
- `CLOSED` → 已收盘
- `PRE_MARKET_BEGIN` → 美股盘前交易中
- `PRE_MARKET_END` → 美股盘前结束
- `AFTER_HOURS_BEGIN` → 美股盘后交易中
- `AFTER_HOURS_END` → 美股盘后结束
- `OVERNIGHT` → 夜盘交易中
- `HK_CAS` → 港股盘后竞价

## Output Pattern

默认输出：
1. 市场或标的
2. 当前状态
3. 是否处于交易时段
4. 如有必要，补充下一关键阶段说明

避免只回原始枚举值。
