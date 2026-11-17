# 批量出金交易查询

官方来源：<https://paas.huifu.com/partners/api/doc/api_plcjjycx.md>。来源快照：2026-11-04；SHA-256：`99f34f8a7787d4a0c5920df14fe35e70fc715a6719f4c0d78b5cee752e85a458`。

接口：`/v2/trade/batchtranslog/query`。方法：POST。

## 查询条件与分页

批量查询已有出金记录，不能发起新的出金。`huifu_id`、`begin_date`、`end_date` 正式Y；`batch_trans_type` 可SURROGATE银行卡代发、ENCHASHMENT取现、TSENCHASHMENT TS结算，不传默认查银行卡代发和取现，保留拼写。

`payment_hf_seq_id` 用于TS结算，正文称非空时商户号、开始和结束日期非必填，与正式Y有条件性冲突。保留Y与此条件，[需要官方确认]后明确场景校验，不能全局改N或虚构省略条件。`page_num`默认1，`page_size`默认10，正式长度和最大页大小未公布，不套用流水查询100或结算查询50。

## 响应编码与状态

`response.data.trans_log_result_list` 正式Array，元素按完整目录解析；示例却使用JSON字符串，不能把示例字符串当成正式类型。分页计数字段正式String、示例数值，类型差异单列适配点。不要与结算记录查询的正式String(JSON Array)合并成一种DTO。

每条trans_status与re_exchange独立核对；退款、退汇、支付成功和出金成功是不同事实。查询响应不定义新的通知协议。

## 完整字段与SDK

单字段类型/必填、完整DTO或同步响应字段均按接口与方向读取 `payment-extension-complete-field-catalog.md` 中的“批量出金交易查询”，覆盖38条正式字段路径。代码任务联读 `payment-extension-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`；专属类 `V2TradeBatchtranslogQueryRequest`，Python模块 `v2_trade_batchtranslog_query`。扩展字段先拒绝覆盖SDK已声明字段，再经官方SDK发送；SDK合并本身不提供此保护。日期、流水、金额、账户和角色ID保持调用方值，来源头按实际参与的Skill确定。
