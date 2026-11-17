# 统一进件页面版查询

## 接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/status/query`。
- 官方来源：[统一进件页面版查询](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shtyjjwebcx.md)；活动 SHA-256 `252db113d3eab2a6de3b1fb27291bc7346f9c2c3a53bcc54657c44cc875357c8`。
- 共51个路径：请求8、同步响应43、无异步。以 `store_id` 查询；`upper_huifu_id:N` 在 `sys_id` 为商户时按原页面请求值传入。
- 返回区分 `check_status`、微信/支付宝支付配置、实名授权和协议信息；任一子状态都不能单独推导“可交易”。

## 官方冲突与 SDK

- 最新正式字段已经修正为 `wx_real_name_list`；停止生成旧 `wx_neal_name_list`。`wx_real_name_list/ali_real_name_list/wx_pay_config_info/ali_pay_config_info/agreement_info_list` 均按 String(JSON Array) 解码，目录保留 `[]`。
- 旧父字段 Object 与 String(JSON) 的冲突已关闭，`wx_real_name_list[].pay_scene` 正式长度已为2，与示例01一致。该字段链接文字仍写“微信业务开通类型”、目标却是“微信支付场景”；剩余枚举疑义标记 `[需要官方确认]`，不得从链接标题或示例猜值。
- 三语言使用 `V2MerchantBusiStatusQueryRequest`；生成类仅有 `req_seq_id/req_date/store_id`，可选 `upper_huifu_id` 走 exact-key 白名单。
