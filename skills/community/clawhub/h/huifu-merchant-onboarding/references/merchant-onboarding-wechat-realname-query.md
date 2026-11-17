# 微信实名认证状态查询

## 接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/realname/query`。
- 官方来源：[微信实名认证状态查询](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxsmrzztcx.md)；SHA-256 `8477b7bada0041c3f7ef6fc33ae2a35d041a3898e6ef2c23f6d1ff2d7be66872`。
- 共22个路径：请求9、同步响应13、无异步。`applyment_stat` 与 `authorize_stat` 是两套状态，必须分别展示。
- 只有指定待确认、通过或冻结状态可能返回 `qrcode_data`；驳回时读取 `reject_param/reject_reason`。

## 申请单状态

官网在字段表之外另列九个精确值，必须按原拼写处理，不能改正其中的 `EDITTING/WAITTING/FREEZED`：

| 值 | 含义 | 处理边界 |
| --- | --- | --- |
| `APPLYMENT_STATE_EDITTING` | 编辑中 | 可使用同一业务申请编号重新提交 |
| `APPLYMENT_STATE_WAITTING_FOR_AUDIT` | 审核中 | 等待微信支付审核 |
| `APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT` | 待确认联系信息 | 扫描小程序码确认联系信息 |
| `APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON` | 待账户验证 | 扫描小程序码完成账户验证 |
| `APPLYMENT_STATE_PASSED` | 审核通过 | 仍需扫描小程序码完成授权流程 |
| `APPLYMENT_STATE_REJECTED` | 审核驳回 | 按驳回原因修改资料并更换业务申请编码重提 |
| `APPLYMENT_STATE_FREEZED` | 已冻结 | 按驳回原因通知指定联系人完成授权 |
| `APPLYMENT_STATE_CANCELED` | 已作废 | 无需继续处理该申请单 |
| `APPLYMENT_STATE_NOAPPLY` | 未申请 | 不得解释为审核失败 |

`authorize_stat` 是另一状态轴：`1=授权成功`、`0=授权失败`。申请审核通过不能替代授权成功。

## 二维码与 SDK

- 官网把 `qrcode_data` 同时描述成 base64、图片和完整 HTML `<img>`。不得直接插 DOM、不得假定需要 base64 解码；实际 wire 未确认前标记 `[需要官方确认]`。
- 三语言使用 `V2MerchantBusiRealnameQueryRequest`；`pay_channel_id/pay_scene` 走 exact-key 白名单，禁止覆盖三个生成字段。
