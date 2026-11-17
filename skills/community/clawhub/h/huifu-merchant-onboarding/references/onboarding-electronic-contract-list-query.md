# 电子合同列表查询

## 接口合同

- Endpoint：`POST https://api.huifu.com/v2/agreement/apply/list`。
- 官方来源：[电子合同列表查询](https://paas.huifu.com/partners/api/doc/shgl/fp/api_fp_dzhtsqlbcx.md)；快照 `2026-11-09`；SHA-256 `2a774b8820cdb4e5e4dc1364f1be9bcdcfc273b7b86e064aa3c631c97e8d397b`。
- 共40个路径：请求16、同步响应24、无异步。请求必填 `req_date/req_seq_id/huifu_id/agreement_type/page_num/page_size`。
- `result_list:String/jsonArray` 按一层 String(JSON Array) 解码；列表项完整字段见机械目录。

## 官方冲突

- 正式请求与示例现在都使用 `page_size:String(10) Y`，禁止继续生成旧 `pageSize`。
- `response.data.total_size/page_num/page_size:String(10) N` 已进入正式表；列表项正式字段现在为 `create_time:String(16) N`，不再使用 `createTime`。
- 正式长度已修正：`sign_status/agreement_type/scene_code=32`，`start_date/expiration_date=8`，`sign_url=128`，业务返回码为8位。无协议时 `result_list` 不返回；不得伪造 `0`、`"0"` 或空数组。正式 `result_list` 仍是 String/jsonArray，但成功示例为原生数组，wire 冲突仍须 `[需要官方确认]`。
- 示例包含合同下载/签署链接形态；不得复制、展示或记录。三语言本地 SDK 的 `V2InvoiceQueryecmsapplylistRequest` 仍指向旧 `/v2/invoice/queryEcmsApplyList`，不支持本页最新路径。使用已核验的官方 SDK 通用入口调用精确 `/v2/agreement/apply/list`，不得手写生产 HTTP。
