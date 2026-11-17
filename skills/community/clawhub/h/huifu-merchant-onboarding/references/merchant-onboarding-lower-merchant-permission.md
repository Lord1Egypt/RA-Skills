# 开通下级商户权限配置

## 接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/head/config`。
- 官方来源：[开通下级商户权限配置](https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_xjshpz.md)；官网更新 `2026-09-22`；SHA-256 `e213479c4b3bb355dd8bbccefcee1d1980e12f83af2fb14323760c6776d24d8f`。
- 共141个路径：请求132、同步响应9、无异步；包含21个扩展表。完整配置字段只能从机械目录读取。
- 请求 data 必填 `req_seq_id/req_date/huifu_id/product_id`；`upper_huifu_id:C` 在 `sys_id` 为渠道商时填写，总部商户主体时选填。

## 配置与风险

- 支持支付宝、微信、银联二维码、银行卡、分账、直连、线上、余额、补贴、大额、全域资金、结算、取现、外扣、抖音等权限或底价。只发送调用方明确选择且有真实值来源的配置，不得把示例费率当默认值。
- 官网请求示例漏掉正式必填的 `data.product_id`；外层 `product_id:String(32)` 与 data 内 `product_id:String(16)` 是两个字段，不能互相代替。
- 官网成功示例仍是商户详情结构，与正式9字段响应完全不符。严格响应只能信任正式表；未知实际 wire 标记 `[需要官方确认]`。
- 三语言使用 `V2MerchantBusiHeadConfigRequest`；生成类只覆盖五个定位字段，其余配置用 exact-key 白名单扩展，禁止覆盖生成类字段。
