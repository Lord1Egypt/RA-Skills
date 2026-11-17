# 微信商户配置

## 接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/config`。
- 官方来源：[微信商户配置](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxshpz.md)；SHA-256 `bc0b92c4e46e7a097248cf3e048fcd9f13159b41ccd26194b2825babc132426a`。
- 共31个路径：请求16、同步响应4、异步11。接口只添加配置，官网明确成功后不支持修改或删除，每类参数最多5组。
- `wx_woa_app_id/wx_woa_path/micro_sub_appid/wx_applet_app_id` 四者不能同时为空；APP secret 是高敏凭据，不输出、不落日志。

## 冲突、通知与 SDK

- 异步 `async.data.result_list[].config_type:String(2) N` 现已匹配 `01/02`；`config_stat:String(2) N`。同步 `resp_code/resp_desc/huifu_id/apply_no` 四个业务字段均 N，长度均未给，不得复制旧长度。
- 最新页已删除正式同步/异步信封表，只剩请求信封、请求 data、同步业务 data、异步业务 data 四张根表。目录中的 `response.data.*` / `async.data.*` 是业务路径定位，不证明外层 data 类型或 sign 存在；不得补回旧 `response.sign/data`、`async.resp_code/resp_desc/sign/data` 定义。异步 `result_list` 按正式 String(JSON Array) 保留，`ord_id` 提示 ACK 为 `RECV_ORD_ID_` + ord_id；外层包装、验签原文、HTTP、重试与超时仍未明确，按 `shared-overview.md` 的开发提醒给出本页官方来源与咨询建议。可继续回调框架和已明确的业务字段处理，未知协议用 TODO/配置隔离，不补造外层字段或签验规则。
- 三语言使用 `V2MerchantBusiConfigRequest`；生成类缺少 secret、反扫 APPID、渠道号和回调地址，使用 exact-key 白名单且禁止覆盖生成字段。
