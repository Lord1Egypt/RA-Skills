# 微信实名认证

## 接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/realname`。
- 官方来源：[微信实名认证](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxsmrz.md)；SHA-256 `41d4520a560c4cafb61cf8b87f7d15bf316c949e2b126a131833e343c8fa3197`。
- 共51个路径：请求45、同步响应6、无异步。商户必须已经成功入驻微信；同步成功只返回申请单，不代表实名与授权完成。
- 联系人、受益人、金融机构、特殊主体和材料字段按主体条件执行；标为 N 但说明“企业/经办人/金融机构时必填”的字段仍条件必填。

## SDK 与安全

- `ubo_info_list`、`special_file_info_list` 按 String(JSON Array) 发送；证件、手机号、地址和图片 ID 全部属于敏感数据。
- 三语言使用 `V2MerchantBusiRealnameRequest`；生成类只包含7个基础字段，其他正式字段通过 exact-key 白名单扩展，禁止覆盖。
- 后续必须调用微信实名认证状态查询分别检查申请状态与授权状态。
