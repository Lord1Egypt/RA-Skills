# Kline and Intraday

核心接口：
- `/quotes/get_rt_data` → 分时
- `/quotes/get_cur_kline` → K 线

## Intraday

当用户询问：
- 实时分时
- 盘中走势
- 今天走势如何

优先使用 `/quotes/get_rt_data`。

默认摘要：
- 当前价
- 均价
- 昨收
- 成交量 / 成交额
- 当前时间点
- 简短走势观察

## Kline

当用户询问：
- 日K / 周K / 月K
- 最近 N 天走势
- 5 分钟 K / 15 分钟 K / 60 分钟 K

使用 `/quotes/get_cur_kline`。

关键参数：
- `code`：优先传标准代码
- `num`：返回 K 线个数
- `ktype`：K 线周期
- `autype`：复权方式

## KType Mapping

自然语言到 `KLType` 的常见映射：
- 1分钟K → `K_1_M`
- 5分钟K → `K_5_M`
- 15分钟K → `K_15_M`
- 30分钟K → `K_30_M`
- 60分钟K → `K_60_M`
- 日K → `K_DAY`
- 周K → `K_WEEK`
- 月K → `K_MON`

## AuType Guidance

- 不特别说明时，可优先用 `NONE`
- 用户明确要求前复权 → `QFQ`
- 用户明确要求后复权 → `HFQ`

## Output Guidance

默认不要逐根回吐全部 K 线；先做摘要：
- 最近区间涨跌
- 区间高低点
- 最近成交活跃度
- 若用户明确要明细，再展开最近 N 根
