# 余额支付 SDK 证据

## 本轮核验

`2026-10-08` 从官方固定提交/制品读取源码：通用Java3.0.41、PHP2.0.31、Python2.0.28；Lightning1.0.6仅服务聚合支付，不用于余额支付。SDK版本、官方提交/归档SHA、所选文件SHA和源码树SHA由维护证据锁定；不代表真实网关联调或资金结果。

| 接口 | 三语言同名专属 Request | 声明的业务字段 |
| --- | --- | --- |
| 支付 | `V2TradeAcctpaymentPayRequest` | `req_seq_id/req_date/out_huifu_id/ord_amt/acct_split_bunch/risk_check_data/fund_type/trans_fee_take_flag/verify_value` |
| 支付查询 | `V2TradeAcctpaymentPayQueryRequest` | `huifu_id/org_req_date` |
| 退款 | `V2TradeAcctpaymentRefundRequest` | `req_seq_id/req_date/huifu_id/org_req_date/org_req_seq_id/org_hf_seq_id/ord_amt` |
| 退款查询 | `V2TradeAcctpaymentRefundQueryRequest` | `org_req_seq_id/org_req_date/huifu_id` |
| 试算 | `V2TradeFeecalcRequest` | `huifu_id/req_date/req_seq_id/trade_type/trans_amt` |
| 付款关系 | `V2TradePayrelationApplyRequest` | `out_huifu_id/req_date/req_seq_id/pay_relations` |
| 短信 | 三语言均无匹配专属 Request/路由常量 | 经官方通用入口发送五个正式字段 |

字段表是 SDK 声明范围，不是官方必填范围。例如支付 `fund_type/trans_fee_take_flag/verify_value` 是条件字段，SDK 类存在不意味着无条件要求。未声明正式参数通过 exact-key 扩展传入，拒绝与声明字段重叠；请求只发正式接口字段。退款查询无额外正式字段，扩展为空。

## 路由与调用

Java 的功能码以点分隔，`BasePayClient` 内部替换为斜杠；PHP 功能码不带前导斜杠；Python 路由带前导斜杠。专属类全部指向各原子 reference 的精确 API 路由。

短信采用下列原生通用入口，仍复用官方签名、验签及请求头，不是手写 HTTP：

- Java：`BasePayClient.request(data, "v2.trade.sms.verifycode.send", false)`。
- PHP：`BsPayClient::postRequest(["funcCode" => "v2/trade/sms/verifycode/send", "params" => data], false)`。
- Python：`dg_sdk.DGTools.request_post("/v2/trade/sms/verifycode/send", data)`。

不能用商户进件短信、快捷支付短信、发票验证码或钱包支付的相似 Request 替代。通用入口的 `data` 为业务映射，不是整个 sys_id/product_id/sign 信封。

## 编码、扩展与安全

Java `params.putAll`、PHP `array_merge`、Python `required_params.update` 都允许扩展覆盖已有字段；业务适配器必须提前拒绝覆盖。String(JSON) 在交给 SDK 前编码一次，Java 风控专用处理不会再次编码已经是 String 的值。

Python2.0.28 `MerConfig` 第五参数是 `sign_type`，第六是 `jpt_x_skill_source`。初始化用 `sign_type="RSA", jpt_x_skill_source=...`；不能复制旧版第五位置的来源参数。

Java请求前全局 `BasePay.debug=false`；PHP加载任何SDK文件前固定 `DEBUG=false`，不能使用Demo loader。PHP2.0.31源码仍关闭 peer TLS校验，按已确认维护规则作为非阻断提醒；生成代码不增加关闭校验、不修改SDK。Python/通用Java公共默认TLS路径按实际源码记录。

来源头仅支付为 `hfps/1.6.0`，两套Skill共同参与为 `hfps/1.6.0;hfms/1.2.0`，显式配置原样透传。只有出款方、没有正式 `huifu_id` 的接口不得为商户头添加虚构业务键；SDK内部头生成保持其原生行为。

## 官方源码来源

- Java：<https://github.com/huifurepo/bspay-java-sdk-parent/tree/3dd088b159ad94ebc5246114c07c97070e0581b2>
- PHP：<https://github.com/huifurepo/bspay-php-sdk/tree/d93cae52dea2033c4a737dc0d6877a2f65a34418>
- Python：<https://pypi.org/project/dg-sdk/2.0.28/>

分别读取对应语言 adapter；不能把一种语言的字段编码和调用方式复制为另一语言手写客户端。
