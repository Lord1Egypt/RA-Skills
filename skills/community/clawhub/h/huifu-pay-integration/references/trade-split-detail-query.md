# 交易分账明细查询

## 适用范围

用于已开通分账能力的商户，按分账交易汇付全局流水号查询实时或延时分账明细。官方来源：[交易分账明细查询](https://paas.huifu.com/partners/api/doc/smzf/api_fzmxcx.md)，页面更新时间 `2024.12.20`，锁定来源 SHA-256 为 `dcab5eb128a7987742ea339631add74ad771227d3ce557c1154d6d6a27266270`。

本接口只支持查询 180 天内的分账记录。它不是拆单支付订单查询，也不能创建分账、退款或改变账务状态；没有真实分账流水、商户分账能力或查询权限时必须停止。

## 已确认的接口合同

- Endpoint：`POST https://api.huifu.com/v2/trade/trans/split/query`，报文格式 JSON。
- 请求顶层为 `sys_id:String(32) Y`、`product_id:String(32) Y`、`sign:String(512) Y`、`data:Json Y`；响应顶层为 `sign:String(512) Y`、`data:Json N`。
- 完整目录共 29 个节点：请求 7、同步响应 22、无异步通知；其中结构父节点 3、叶节点 26。完整类型、长度、Y/N 和说明见 `payment-complete-field-catalog.md` 的“交易分账明细查询”。
- `request.data.hf_seq_id:String(128) Y` 是分账交易汇付全局流水号；`request.data.huifu_id:String(32) Y` 是商户号；`request.data.ord_type:String(20) Y` 只能是 `consume`（正向交易）或 `refund`（反向交易）。三个字段缺一不可。
- 官网没有分页请求字段；`response.data.total_size:String(32) Y` 是总记录数，但不得据此发明 page/page_size 或承诺分页行为。

## 同步响应

- `response.data.resp_code:String(8) Y`、`resp_desc:String(256) Y`、`total_size:String(32) Y`。
- 参数表声明 `response.data.split_trans_responses:String N`，并展开 16 个全部为 N 的子字段：`req_seq_id`、`req_date`、`huifu_id`、`in_huifu_id`、`product_id`、`org_ord_id`、`trans_ord_id`、`hf_seq_id`、`ord_type`、`split_amt`、`split_fee_amt`、`split_fee_huifu_id`、`split_seq_id`、`split_type`、`trans_finish_time`、`acct_stat`。
- `split_type` 为 `realTime`（实时）或 `delay`（延时）；`acct_stat` 为 `P`（处理中）、`S`（成功）或 `F`（失败）。金额字段保持 String，单位元并保留两位小数；不得先转浮点数再参与账务判断。
- 官网参数表与成功示例现已统一为 String(JSON Array)：wire 字段保持 `response.data.split_trans_responses`，只反序列化一次后得到数组；解码路径必须保留 `response.data.split_trans_responses[]` 及全部 16 个子字段。不得直接按原生数组读取，也不得二次反序列化。
- 成功示例额外出现 `response.data.huifu_id`，响应参数表没有声明该字段。它不进入完整字段目录、响应 DTO 或必填校验；收到时只能按未知附加字段处理。

## 三语言 SDK 边界

用户提供且已核对的 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 源码均有本接口专属类和精确路由：

| 语言 | Request / 模块 | 路由证据 | 请求字段边界 |
| --- | --- | --- | --- |
| Java | `V2TradeTransSplitQueryRequest` | `V2_TRADE_TRANS_SPLIT_QUERY = v2.trade.trans.split.query` | 类只声明 `hfSeqId`、`huifuId`、`ordType` |
| PHP | `V2TradeTransSplitQueryRequest` | `V2_TRADE_TRANS_SPLIT_QUERY = v2/trade/trans/split/query` | 类只声明 `hf_seq_id`、`huifu_id`、`ord_type` |
| Python | `V2TradeTransSplitQueryRequest` / `v2_trade_trans_split_query_request.py` | `V2_TRADE_TRANS_SPLIT_QUERY = /v2/trade/trans/split/query` | 类只声明 `hf_seq_id`、`huifu_id`、`ord_type` |

官网请求表没有可选业务字段，因此本接口扩展映射必须为空。Java `putAll`、PHP `array_merge`、Python `dict.update` 都可能让扩展值覆盖已声明字段，必须拒绝扩展映射中的 `hf_seq_id`、`huifu_id`、`ord_type` 以及任何其他合同外键。三语言均使用官方 Request/Client 主链路并保留签名和响应验签，不手写 HTTP。

Java 可运行代码仍须在进程初始化、任何 SDK 请求前全局执行一次 `BasePay.debug = false;`，且不得并发切换。PHP 必须在加载 SDK 和 `BsPay::init` 前固定 `DEBUG=false`，不得使用会开启 DEBUG 的 Demo loader。

## 生成前检查

1. 确认商户已开通分账能力、目标记录不超过 180 天，并取得真实 `hf_seq_id` 与匹配的 `huifu_id`、`ord_type`。
2. 确认请求只包含官网三个业务字段，扩展映射为空，未把拆单支付订单号或普通交易流水替代分账全局流水。
3. SDK 验签后再判断 `resp_code`；`acct_stat=P` 不是成功终态。
4. `split_trans_responses` 只按 String(JSON Array) 解码一次；不要把成功示例中的顶层 `huifu_id` 提升为正式字段。

## 公共请求头

`jpt-x-skill-source: <skill_source>` 必须按 `shared-request-header-policy.md` 生成；仅支付默认 `hfps/1.6.0`，同时使用支付与进件 Skill 时默认 `hfps/1.6.0;hfms/1.2.0`。
