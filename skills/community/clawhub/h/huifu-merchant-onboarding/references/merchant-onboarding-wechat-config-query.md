# 微信商户配置查询

## 接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/config/query`。
- 官方来源：[微信商户配置查询](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxshpzcx.md)；SHA-256 `99937c6b7807a691d017830e8553521b1e13691f66a02473dcf6ce3e6bc0924e`。
- 共32个路径：请求8、同步响应24、无异步。请求必填 `req_seq_id/req_date/huifu_id`，渠道号可选。
- `atu_config_bo_list`、嵌套 `wx_config_list` 与 `atu_config_bo_fail_list` 均为一层 String(JSON Array)。

## 官方冲突与 SDK

- `atu_config_bo_list[].micro_sub_appid` 所在行把“必填/长度”单元格写成 `32/N`，机械目录按表头原样保留为 `required=32,length=N`；真实约束必须确认。
- 新增页公众号 APPID 长度20，查询页为512；成功示例只有 data 内层且省略信封。响应必须按正式 `sign + data` 处理并验签。
- 三语言使用 `V2MerchantBusiConfigQueryRequest`；可选渠道号用 exact-key 白名单，禁止覆盖三个生成字段。
