# 电子合同拒签

## 接口合同

- Endpoint：`POST https://api.huifu.com/v2/agreement/elect/rejectsign`。
- 官方来源：[电子合同拒签](https://paas.huifu.com/partners/api/doc/shgl/fp/api_fp_dzhtjq.md)；快照 `2026-11-09`；SHA-256 `ec6aea1f10e1ab3113993d16422214e9a3aaa586e71bcd646841f45ad60c1f9e`。
- 共12个路径：请求8、同步响应4、无异步。请求 data 为 `req_date:String(8) Y`、`req_seq_id:String(32) Y`、`huifu_id:String(18) Y`、`agreement_id:String(32) Y`。

## 风险与 SDK

- 这是有业务副作用的拒签动作，不等同查询或撤销；调用前必须确认真实协议号、商户号与操作者授权。
- `response.data.resp_code:String(8) Y` 与成功示例已一致，旧9位冲突不再触发硬停。
- 三语言本地 SDK 的 `V2InvoiceRejectsignRequest` 仍指向旧 `/v2/invoice/rejectSign`；最新路径须使用已核验的官方 SDK 通用入口，精确传入 `/v2/agreement/elect/rejectsign`，不得误用旧专属类、电子合同列表或手写 HTTP。
