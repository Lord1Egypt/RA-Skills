# 手续费试算

官方来源：<https://paas.huifu.com/partners/api/doc/sxf/api_sxf_sxfss.md>；快照 `2026-11-04`，官网更新时间 `2024-09-01`。

接口：`POST /v2/trade/feecalc`；完整27个字段路径见 `payment-complete-field-catalog.md` 的“手续费试算”。本接口是通用支付辅助能力，不只服务余额支付，也不授权调用本 Skill 未覆盖的实际资金接口。

## 请求

必填 `huifu_id:String(32)`、`req_date:String(8)`、`req_seq_id:String(128)`、`trade_type:String(32)`、`trans_amt:String(14)`。同一商户当天流水唯一，金额为元、两位小数、最低0.01。余额支付使用 `trade_type=ACCT_PAYMENT`，金额字段是 `trans_amt`，不能复制支付的 `ord_amt`。

正式类型还声明 `T_JSAPI/T_MINIAPP/A_JSAPI/A_NATIVE/U_NATIVE/U_JSAPI/ENCASHMENT/ONLINE_PAY/QUICK_PAY/WAP_PAY/UNION_PAY`，不从聚合下单扩充 APP、反扫等未声明枚举。

表格 N 但正文要求的条件字段：网银必传 `online_trans_type`（3000/3001/3002/3003）；网银、快捷、WAP 必传 `bank_id`；扫码必传 `channel_no`；取现必传 `encash_type`（T0/T1/D1）。余额支付不无条件填写这些渠道字段。`card_type=D/C`，默认 D；`pay_scene` 按本页九种场景01至09。

## 响应与冲突

返回借记手续费 `debit_fee_amt`、贷记手续费 `credit_fee_amt`、通用手续费 `fee_amt`，按实际交易类型使用，不能承诺三者全部返回或试算等于实际扣费。本页未声明异步通知。

请求业务表头将“必填/长度”列反置，但行值是 `String | 32 | Y` 等长度后必填形式；完整目录保留行值并记录表头冲突，不把32解释成必填标记。

正式外层响应是 `sign + data`；示例却是无信封的业务对象，且写 `hfSeqId` 而正式字段为 `hf_seq_id`。SDK仍正常验签；不把示例提升为无签名协议或依赖驼峰兼容键。余额支付费率实际采用哪个返回金额未明确的部分留映射配置，不按扫码说明自行推定。

银行编码触发 <https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm>；未读取外部资料时提示人工核验。
