# Options and Derivatives

核心接口：
- `/derivatives/get_option_expiration_date`
- `/derivatives/get_option_chain`
- `/derivatives/get_warrant`

## Option Expiration Dates

适用问法：
- 期权到期日有哪些
- 某标的有哪些到期月份

默认输出：
- 到期日列表
- 若有必要，按时间顺序排序

## Option Chain

适用问法：
- 查期权链
- 查 call / put
- 查某个到期日的期权

可使用筛选参数：
- `start`
- `end`
- `option_type`
- `option_cond_type`
- `index_option_type`

默认摘要：
- 标的
- 到期日范围
- 看涨 / 看跌分布
- 关键行权价区间

## Warrants

适用问法：
- 港股窝轮
- 牛熊证
- 界内证

这属于更专业的数据，默认只在用户明确提到时启用。
