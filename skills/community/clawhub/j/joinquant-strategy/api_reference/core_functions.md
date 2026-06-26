# 聚宽核心API参考

## 初始化函数
- `initialize(context)` - 策略初始化，只执行一次
- `process_initialize(context)` - 进程重启时执行
- `after_code_changed(context)` - 代码修改后执行

## 定时运行函数
- `run_daily(func, time, reference_security)` - 每天运行
- `run_weekly(func, weekday, time, reference_security, force)` - 每周运行
- `run_monthly(func, monthday, time, reference_security, force)` - 每月运行

## 数据获取函数
- `attribute_history(security, count, unit, fields, skip_paused, fq)` - 单只股票历史数据
- `history(count, unit, field, security_list, skip_paused, fq)` - 多只股票历史数据
- `get_current_data()` - 获取当前数据
- `get_fundamentals(query_object, date, statDate)` - 获取财务数据

## 下单函数
- `order(security, amount)` - 按股数下单
- `order_value(security, value)` - 按金额下单
- `order_target(security, amount)` - 调整至目标股数
- `order_target_value(security, value)` - 调整至目标金额

## 其他常用函数
- `set_benchmark(security)` - 设置基准
- `set_option(name, value)` - 设置选项
- `set_order_cost(cost, type)` - 设置手续费
- `set_slippage(slippage)` - 设置滑点
- `get_all_securities(types, date)` - 获取所有证券
- `get_index_stocks(index_symbol, date)` - 获取指数成分股
- `get_industry_stocks(industry_code, date)` - 获取行业成分股
- `get_concept_stocks(concept_code, date)` - 获取概念成分股
- `log.info(msg)` - 输出信息日志
- `log.warning(msg)` - 输出警告日志
- `log.error(msg)` - 输出错误日志
- `record(**kwargs)` - 记录变量用于图表显示
