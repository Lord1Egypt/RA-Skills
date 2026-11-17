# 主动取现

官方来源：<https://paas.huifu.com/partners/api/doc/jyjs/qx/api_qx.md>。来源快照：2026-11-04；SHA-256：`6f64a96c90c0ece5dce058ad7ffb5248a27fb1a6f81b7222d6344a936e2da06b`。

接口：`/v2/trade/settlement/encashment`。方法：POST。

## 使用条件与请求

这是向已绑定取现卡发起的主动取现。官方应用场景列商户、用户和渠道商，但请求 `huifu_id` 字段说明只列已配置取现规则的商户、用户；保留两处口径，渠道商的目标ID与规则适用性需确认，不能把用户或渠道号改写成商户号。官方适用对象要求商户已开通取现权限。绑定卡取得的 `token_no:String(20) Y` 是取现卡序列号，不能替换成银行卡号。`acct_id` 仅基本户、现金户，未填默认基本户；权限或绑卡配置缺失交接进件 Skill，实际取现和查单仍由支付 Skill 处理。

`req_date`、`req_seq_id`、`cash_amt`、`huifu_id`、`into_acct_date_type`、`token_no` 均正式Y；金额为元，两位小数。保留调用方日期、流水及字符串ID，不自动生成或补零。`into_acct_date_type` 为 D0/T1/D1/DM；D0包括当日交易资金，DM不包括当天交易资金，不能按代发的T0枚举替代。`enchashment_channel` 默认00汇付，可10中信e账通，保留官网拼写；`fee_type` 默认2自身承担，可1总部承担。

## 状态与通知

同步 `response.data.trans_stat` 为S/F/P。异步字段名是 `async.resp_data.trans_status`，并独立保留 `acct_status`（S/F/P/B，B为回账成功）、`channel_status`（S/F/P）、`msg_type`（01通道、02账务）及 `re_exchange`（Y已退汇）。外层成功码、同步P、单个状态S都不能推导整体完成；不要把B记为收款方到账成功。

先收到01再收到02时分别更新通道和账务；成功后又收到退汇Y或回账B仍要处理。通知先验签、校验归属/金额/定位，再按事件维度与状态幂等，不能仅按req_seq_id永久丢弃后续事件。正式异步表已公布外层 `sign:String(255) Y`，说明为“对报文整体签名”；`resp_data:String N` 说明为json格式，长度未公布。保留原始报文，验签后再解码 `resp_data`。未明确的是待验签字符串的构造、HTTP承载方式、ACK、重试和跨状态优先级：[需要官方确认]，留TODO；不能借用支付Webhook协议，也不能把已知的sign字段位置说成未知。不确定结果用出金交易查询按原单补偿，不换流水再次取现。

## 传输差异

公共请求 `request.data` 在正式信封表中是String(JSON)，示例及官方SDK实际构造对象。目录保留正式String事实，SDK请求保持对象data，不对整个data二次JSON编码。已明确业务字段继续实现，冲突与通知缺口分别留适配点。

## 完整字段与SDK

单字段类型/必填、完整DTO、响应或通知字段均按接口与方向读取 `payment-extension-complete-field-catalog.md` 中的“主动取现”，覆盖45条正式字段路径。代码任务联读 `payment-extension-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`；专属类 `V2TradeSettlementEncashmentRequest`，Python模块 `v2_trade_settlement_encashment`。扩展字段先拒绝覆盖SDK已声明字段，再经官方SDK发送；SDK合并本身不提供此保护。日期、流水、金额、账户和角色ID保持调用方值，来源头按实际参与的Skill确定。
