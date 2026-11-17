# 商户短信发送

## 适用范围

用于结算卡变更或中信 E 管家签约等场景发送、核验短信验证码。官方来源：[商户短信发送](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shdxfs.md)，锁定来源 SHA-256 为 `6982fe07d276cbb0739c9c205afbc5b238dd6d72422154efd6248932aa459b54`。

验证码、手机号和签约流水均为敏感数据；不得记录到日志、仓库、示例或前端持久化。

## 已确认的接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/basicdata/sms/send`。
- 请求顶层为 `sys_id:String(32) Y`、`product_id:String(32) Y`、`sign:String(512) Y`、`data:Json Y`；响应顶层为 `sign:String(512) Y`、`data:Json N`。
- 完整目录共20个节点：请求12、同步响应8、无异步通知。完整路径、类型、长度、Y/N/C 和官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“商户短信发送”。
- 请求必填 `data.req_seq_id:String(32) Y`、`data.req_date:String(8) Y`、`data.huifu_id:String(18) Y`、`data.verify_type:String Y`。

## 条件字段

| 路径 | 官方条件 |
| --- | --- |
| `data.phone:String(11) C` | `verify_type='elecAcctSign'` 时可为空，由系统取联系人手机号；其他场景按业务要求提供真实号码。 |
| `data.operation_type:String C` | `verify_type='elecAcctSign'` 时必填；`sendSmsCode` 发送验证码，`identitySmsCode` 核实验证码。 |
| `data.verify_code:String(6) C` | `verify_type='elecAcctSign'` 且 `operation_type='identitySmsCode'` 时必填。 |
| `data.elec_acct_sign_seq_id:String(64) C` | 同上，使用发送短信响应得到的真实签约流水。 |

`verify_type` 允许 `settleBankChange` 或 `elecAcctSign`。不得生成固定验证码，不得把短信发送成功解释为资料修改、签约或支付能力已经完成。

## 公共请求头

- `jpt-x-skill-source: <skill_source>` 必须按 `shared-request-header-policy.md` 生成；仅进件默认 `hfms/1.2.0`，双 Skill 默认 `hfps/1.6.0;hfms/1.2.0`。

## SDK 证据

用户提供且已锁定源码树摘要的 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 均存在对应封装：

- Java / PHP：`V2MerchantBasicdataSmsSendRequest`
- Python：`V2MerchantBasicdataSmsSendRequest`，模块 `v2_merchant_basicdata_sms_send_request.py`

SDK 类存在不证明短信送达、本人同意或签约成功。Java 代码仍必须在任何 SDK 请求前全局设置 `BasePay.debug = false;`。
