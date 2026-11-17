# 支付宝实名申请单查询

## 接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/ali/realname/query`。
- 官方来源：[支付宝实名申请单查询](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_zfbsmcx.md)；SHA-256 `cf2e66377106963060ac93656e20bfbc13e0dc4f1a1eaba0b935e9e7f2a8bed6`。
- 共25个路径：请求9、同步响应16、无异步。申请状态、经办人授权状态及子商户授权结果分别建模。
- `reject_reason` 与 `check_result_list` 都按一层 String(JSON Array) 解码；二维码 URL 为敏感短期结果，不写日志。

## 示例与 SDK

- 成功示例省略正式响应信封的 `sign`，真实响应仍必须验签。
- 三语言使用 `V2MerchantBusiAliRealnameQueryRequest`；可选 `pay_channel_id/pay_scene` 用 exact-key 白名单，禁止覆盖三个生成字段。
