# 支付宝实名申请提交

## 接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/ali/realname/apply`。
- 官方来源：[支付宝实名申请提交](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_zfbsmrz.md)；SHA-256 `37418d1dc993c3cbac002e0b4be2607ae929f85b7609f48141a52ac10cc37c5e`。
- 共69个路径：请求63、同步响应6、无异步。请求核心是 `auth_identity_info` 与 `contact_person_info` 两个 String(JSON Object)，另有条件法人和受益人结构。
- 同步返回 `applyment_id/order_status` 只是支付宝实名申请状态，不等同最终授权或支付可用。

## 官方冲突与 SDK

- 主体枚举已补齐 `6=社会组织`，相应certificate_type/certificate_info条件也包含6，不再因缺编码硬停。`auth_identity_info` 当前N，不能为SDK生成类机械补空值。
- 官网示例在非金融机构标记下发送未声明的金融类型，并混用不一致的地区编码与文本；不得复制示例。
- `support_credentials` 本轮正式修为 String(JSON Object)，小微商户 subject_type=3 时必填。按 `request.data.auth_identity_info.support_credentials` 对象路径编码一次，十二条父子路径去掉旧 []；旧数组/对象示例冲突已关闭。`legal_person_info.card_type`长度2、响应order_status长度32。
- 三语言使用 `V2MerchantBusiAliRealnameApplyRequest`；生成类只覆盖五个字段，其余正式字段走 exact-key 白名单。证件、许可证、联系人、受益人和图片 ID 均不得写日志。
