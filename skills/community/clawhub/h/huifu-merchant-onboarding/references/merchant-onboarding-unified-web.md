# 商户统一进件（页面版）

## 接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/url/forward`。
- 官方来源：[商户统一进件（页面版）](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shtyjjweb.md)；快照 `2026-11-09`；SHA-256 `d3ce5d64bf4c9783b40e0700a93476016b469478ba9b3d2c9adf82f55d1e5888`。
- 共59个路径：请求17、同步响应8、异步34；审核通知和逐业务通知必须分开建模。
- `store_id:String(64) Y` 是本地关联键；`upper_huifu_id:C` 按调用主体填写。`head_office_flag=0` 时文案要求 `head_huifu_id` 必填，`head_office_flag=1` 时禁止传。

## 页面与通知风险

- `use_chains_flag` 现明确为1微信+支付宝、2不使用、3微信、4支付宝；`head_huifu_id`正式C与条件一致。旧两处冲突已关闭。
- 正式 `resp_code:String(8)` 的成功示例为6位；`url:String(32)` 小于示例；审核异步 `req_date:String(32)` 却说明 `yyyyMMdd`。返回 URL 必须当不透明敏感值保存，不截断、不拼接、不写日志。
- 官网没有完整说明两个通知的 HTTP/重试/统一 ACK。按 `shared-overview.md` 的开发提醒引用本页官方文档并建议咨询官方/交流群；继续 webhook 框架，未知协议留 TODO/配置，不能只因存在 `ord_id` 就外推全套协议。
- 三语言使用 `V2MerchantUrlForwardRequest`；生成类四字段之外的正式字段走 exact-key 白名单，拒绝覆盖。
