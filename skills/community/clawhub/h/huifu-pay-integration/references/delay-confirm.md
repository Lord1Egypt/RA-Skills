# 交易确认

官方来源：<https://paas.huifu.com/partners/api/doc/smzf/api_jyqr.md>。来源快照：2026-11-04；SHA-256：`9fbf6c70cb9be4422fb2b0a724588c7bda363f6a8bb779cba54435a5e86c82fc`。

接口：`/v2/trade/payment/delaytrans/confirm`。方法：POST。

## 使用条件与边界

- 适用于已开通延时交易功能的商户；确认用于分配原交易资金，不能当作普通支付下单。

- 原交易定位三选一：org_hf_seq_id；org_req_date＋org_req_seq_id；org_req_date＋org_mer_ord_id。余额支付仅支持日期＋原请求流水组合。不能把三种定位强制全部填写。

- 原交易为快捷、余额或全域资金时按条件填写pay_type（QUICK_PAY、ACCT_PAYMENT、REMITTANCE_PAY）。SDK声明pay_type并不使该C字段变成所有场景无条件必填。

- acct_split_bunch为空时按交易时分账串分配。请求该容器为String(JSON Object)，acct_infos为Array。percentage_flag=Y时填写total_div_amt，百分比之和必须100.00%；非Y时按条件填写div_amt，单位元、两位小数且最低0.01。

- 请求和同步acct_split_bunch为String；异步正式类型Object但说明称jsonObject字符串，保留[需要官方确认]，不可统一成一种wire。异步外层resp_data为string但未声明JSON编码，不能把内层合同定位路径直接当作wire。同步trans_stat为P/S/F，通知为S/F；返回码00000000不单独替代业务状态判断。

- 通知应先验签并核对原确认记录、金额与商户，再幂等处理；页面未明确的签名原文、ACK和重试留适配点，不套用控台Webhook或用户业务入驻通知。

## 完整字段与SDK

完整DTO、响应或嵌套字段任务联读 `payment-extension-complete-field-catalog.md` 中的“交易确认”，已覆盖72条正式字段路径；仅请求定义的接口不称为已掌握完整响应。

代码任务联读 `payment-extension-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`，按本项目实际SDK版本核对。只使用官方SDK的专属或通用入口，扩展字段不得覆盖已声明字段。公共请求头使用当前实际参与的Skill来源；调用方的日期、流水、账户与角色ID原样保留。
