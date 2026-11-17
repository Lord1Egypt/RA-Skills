# 子账户开通配置

官方来源：<https://paas.huifu.com/partners/api/doc/zhgl/api_zhgl_zhpz_kyc.md>。来源快照：2026-11-09；SHA-256：`b496d1493ed0615115e8972272f0a717289a5feab6206080a62c83615ea9eb8b`。

接口：`/v2/merchant/settle/config`。方法：POST。

## 使用条件与边界

- 用于为商户创建现金子账户及配置结算、绑结算卡；不是企业/个人用户开户。huifu_id为商户号，upper_huifu_id为上级商户或渠道，不能用userHuifuId替代。

- acct_type正式只列02现金户；acct_name、商户与上级ID均Y。card_info为C、String(JSON Object)；settle_config为N、String(JSON Object)。结算规则提供token_no时不填card_info。

- 卡类型0对公、1法人对私、2非法人对私；个人商户只支持1。银行所在省市使用card_info.prov_id/area_id，均String(6)，不能与商户经营地区混合；对公卡bank_code和branch_code按条件必填。

- 子账户创建与结算卡审核分开：绑卡失败不代表子账户不可用，但会影响提现、结算；未返回token_no不能伪造。审核通知data为String(JSON Object)，审核结果audit_status为Y/N/F。

- 同步字段表与成功示例的apply_no/resp_code覆盖不完全一致，完整方向以目录与[需要官方确认]说明为准。请求使用async_return_url，不能改成支付notify_url；通知ACK、签名原文和重试未知部分留适配点。

## 完整字段与SDK

完整DTO、响应或嵌套字段任务联读 `merchant-account-complete-field-catalog.md` 中的“子账户开通配置”，已覆盖66条正式字段路径；仅请求定义的接口不称为已掌握完整响应。

代码任务联读 `merchant-account-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`，按本项目实际SDK版本核对。只使用官方SDK的专属或通用入口，扩展字段不得覆盖已声明字段。公共请求头使用当前实际参与的Skill来源；调用方的日期、流水、账户与角色ID原样保留。
