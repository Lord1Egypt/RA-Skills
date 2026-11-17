# 余额支付发送短信验证码

官方来源：<https://paas.huifu.com/partners/api/doc/yuer/api_smscode.md>；快照 `2026-11-04`，官网更新时间 `2025-07-18`。

接口：`POST /v2/trade/sms/verifycode/send`。用于已开通余额支付功能、操作前需要短信核验的商户；完整14个字段路径见 `payment-complete-field-catalog.md` 的“余额支付发送短信验证码”。

## 请求与有效期

五个字段均 Y：`req_seq_id:String(128)`、`req_date:String(8)`、`out_huifu_id:String(32)`、`mobile_no:String(11)`、`trans_type:String(256)`。手机号需11位数字；业务类型仅声明 `ACCT_PAYMENT`。

同一个出款方、同一业务类型下验证码五分钟有效。验证码由用户接收，后续支付设置 `verify_type=SMS`、`verify_value`。本接口没有手机号之外的接收号码绑定规则，也没有重发频率、尝试次数、旧码失效、幂等重发语义；不自行编造限制。短信内容、验证码和手机号不进入日志。

## 响应与 SDK

`resp_code/resp_desc/req_seq_id` 为同步业务响应，未声明返回验证码或异步通知；不能从成功响应读取验证码，更不能判支付成功。

`2026-10-08` 核验 Java3.0.41、PHP2.0.31、Python2.0.28，三者均无匹配本路由的专属 Request/常量；使用各 SDK 原生通用调用入口，精确路由及签验路径见 `balancepay-sdk-matrix.md` 和语言 adapter。商户短信发送、快捷支付短信或发票验证码的相似类不能替代。
