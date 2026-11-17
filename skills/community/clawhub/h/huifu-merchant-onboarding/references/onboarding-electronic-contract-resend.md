# 电子合同重发

## 接口合同

- Endpoint：`POST https://api.huifu.com/v2/agreement/elect/signurl/resend`。
- 官方来源：[电子合同重发](https://paas.huifu.com/partners/api/doc/shgl/fp/api_fp_dzhtcf.md)；快照 `2026-11-09`；SHA-256 `169b62c666fbe0345ab4f5b10f7f39116d5fd774f6a04ec6abdb77c3923a156e`。
- 共13个路径：请求9、同步响应4、无异步。完整字段见 `onboarding-extension-complete-field-catalog.md`。
- 请求 data 必须包含 `req_seq_id/req_date/huifu_id/agreement_id/sign_user_email`；长度分别为 `32/8/32/32/64`，均为 String Y。

## 风险与 SDK

- `response.data.resp_code:String(8) Y` 与成功示例一致；旧9位冲突已关闭。
- `sign_user_email` 与重发后得到的签署链接均为敏感信息，不写日志。官网说明链接生成后7天有效，但不授权本地缓存或延长。
- 本地 Java 3.0.41、PHP 2.0.31、Python 2.0.28 中的 `V2InvoiceContractrepeatRequest` 仍指向旧 `/v2/invoice/contractRepeat`，不能用于最新接口。新路径须通过三语言已核验的官方 SDK 通用调用入口传入精确 `/v2/agreement/elect/signurl/resend`，复用官方签名、验签及请求头链路；不得手写生产 HTTP。
