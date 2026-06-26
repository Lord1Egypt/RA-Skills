# API Issues / Follow-ups

本文档记录当前 `noah-stock-trade` 在测试环境联调中发现的接口异常、文档不一致点和待确认问题，方便后续继续推进或反馈给后端。

## 1. `/trade/get_order_list`
### OpenAPI 文档预期
- `GET /trade/get_order_list`
- 支持空参查询当日订单列表
- 可选参数：`code`、`page`、`page_size`

### 当前测试环境实际返回
空参或常规列表参数下，返回：
- `请求参数错误,不传订单场景场景则查询订单详情，此时订单号必传`

### 当前判断
- 服务端实现与 OpenAPI 文档不一致
- 或当前测试环境挂载的是不同版本实现

## 2. `/trade/get_finished_order_list`
### OpenAPI 文档预期
- `GET /trade/get_finished_order_list`
- 支持日期范围、分页、订单过滤等参数

### 当前测试环境实际返回
即使补入：
- `start_date`
- `end_date`
- `code`
- `order_status`
- `order_id`

仍返回：
- `请求参数错误,不传订单场景场景则查询订单详情，此时订单号必传`

### 当前判断
- 与 `get_order_list` 类似，疑似服务实现或路由逻辑异常

## 3. `/trade/get_order_detail`
### 测试参数
- `order_id=1`
- `is_history=true`

### 当前测试环境实际返回
- HTTP 500
- `Cannot invoke "String.toUpperCase(java.util.Locale)" because the return value of "...firstNonBlank(String[])" is null`

### 当前判断
- 当前测试环境对无效参数或缺失字段的空值处理不稳
- 更像服务端空指针类问题，而不是单纯前端脚本错误

## 4. `/trade/get_order_fee_detail`
### 测试参数
- `order_id=1`
- `is_history=true`

### 当前测试环境实际返回
- HTTP 500
- 与 `get_order_detail` 类似的空指针类错误

### 当前判断
- 服务端空值处理或内部参数依赖存在问题

## 5. `/trade/max_enable_buy_amt`
### 初始认知
原先以为只需：
- `code`
- `order_type`

### 当前测试环境实际要求
至少还需要：
- `entrust_price`

### 已验证可成功参数示例
- `code=HK.00700`
- `order_type=LO`
- `entrust_price=320`

### 返回示例
- 普通可买：`33900`
- 融资最大可买：`84100`

## 6. 当前已验证成功的接口
### 账户 / 持仓 / 资产
- `/trade/get_account_info`
- `/trade/get_positions`
- `/trade/get_sec_asset`
- `/trade/get_sec_capital_flow`

### 交易 / 评估
- `/trade/order_fee_query`
- `/trade/get_stock_amount`
- `/trade/max_enable_buy_amt`（需 `entrust_price`）
- `/trade/get_today_deal_list`
- `/trade/get_history_deal_list`（需日期）
- `/trade/get_today_order_list`

## 7. 建议后续动作
1. 与后端确认 `get_order_list` / `get_finished_order_list` 的真实参数与路由逻辑
2. 与后端确认 `get_order_detail` / `get_order_fee_detail` 的空值处理和必要参数约束
3. 更新 OpenAPI 文档，确保与当前测试环境保持一致
4. 在 skill references 中继续沉淀“已成功能力”和“已知异常”清单，避免上下文丢失
