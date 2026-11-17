# 出金交易查询

官方来源：<https://paas.huifu.com/partners/api/doc/jyjs/qx/api_cjjycx.md>。来源快照：2026-11-04；SHA-256：`af155863727a56fe26d8603c02257c444bc434429368fe3711cd2ed4df1c6d34`。

接口：`/v2/trade/settlement/query`。方法：POST。

## 定位与补偿

这是已有出金记录查询，官方适用对象要求商户已开通取现权限；请求huifu_id字段同时列出渠道商、商户、用户，保持目标角色与原始ID，不将调用主体与被查询主体混同。`org_req_date:String(8) Y` 必传；`org_hf_seq_id` 与 `org_req_seq_id` 为C，原全局流水和原请求流水二选一必填。请求无新的req_date/req_seq_id，不生成新流水，不调用取现或代发实现查询补偿。

响应 `trans_status` 为S/F/P，`re_exchange=Y` 表示已退汇；不能把查询中的S与异步回账状态B混为同一成功。先成功后退汇是需要更新的业务事实，保留既有资金流水及查询证据。查询未公布acct_status/channel_status/msg_type，不从通知表补入本接口响应DTO。

## 传输冲突

请求信封data正式String(JSON)，示例和官方SDK发送对象data，分别保留证据，官方SDK请求不二次序列化整个data。完整合同只按本接口各方向构建；公共外层成功码不代替trans_status与退汇核对。

## 完整字段与SDK

单字段类型/必填、完整DTO或同步响应字段均按接口与方向读取 `payment-extension-complete-field-catalog.md` 中的“出金交易查询”，覆盖20条正式字段路径。代码任务联读 `payment-extension-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`；专属类 `V2TradeSettlementQueryRequest`，Python模块 `v2_trade_settlement_query`。扩展字段先拒绝覆盖SDK已声明字段，再经官方SDK发送；SDK合并本身不提供此保护。日期、流水、金额、账户和角色ID保持调用方值，来源头按实际参与的Skill确定。
