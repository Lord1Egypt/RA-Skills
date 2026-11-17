# 修改子账户配置

官方来源：<https://paas.huifu.com/partners/api/doc/zhgl/api_zhgl_xgzh_kyc.md>。来源快照：2026-11-09；SHA-256：`6c041ff7af41573a97463077062725c6a0ca2815b0d64b64fea6c32e21bd3c05`。

接口：`/v2/merchant/settle/modify`。方法：POST。

## 使用条件与边界

- 配置修改由商户huifu_id、上级upper_huifu_id和子账户acct_id定位，均Y；与开通接口分开建模，不额外添加开通接口的acct_name/acct_type字段。

- 修改接口的settle_config正式Y，card_info为C，二者均为String(JSON Object)；不能复制开通接口settle_config的N标志。token_no与卡信息的条件、卡类型、证件有效期和省市联动分别按本页完整父路径执行。

- 原请求req_date、req_seq_id保留，银行卡、证件、手机号和token只从安全配置/调用方接收并脱敏。短信验证码衔接商户短信发送，不调用余额支付短信接口代替。

- 异步data为String(JSON Object)，audit_status为Y/N/F；同步受理、账户可用、绑卡审核及结算可用分别判断。通知未声明的ACK、验签原文、重试规则保留[需要官方确认]，不套用支付或用户通知。

## 完整字段与SDK

完整DTO、响应或嵌套字段任务联读 `merchant-account-complete-field-catalog.md` 中的“修改子账户配置”，已覆盖64条正式字段路径；仅请求定义的接口不称为已掌握完整响应。

代码任务联读 `merchant-account-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`，按本项目实际SDK版本核对。只使用官方SDK的专属或通用入口，扩展字段不得覆盖已声明字段。公共请求头使用当前实际参与的Skill来源；调用方的日期、流水、账户与角色ID原样保留。
