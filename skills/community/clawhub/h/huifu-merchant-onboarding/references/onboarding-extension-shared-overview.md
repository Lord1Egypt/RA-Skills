# 进件扩展能力总览

## 能力与路由

| 能力 | Endpoint | 原子 reference |
| --- | --- | --- |
| 电子合同重发 | `POST /v2/agreement/elect/signurl/resend` | `onboarding-electronic-contract-resend.md` |
| 电子合同列表查询 | `POST /v2/agreement/apply/list` | `onboarding-electronic-contract-list-query.md` |
| 电子合同拒签 | `POST /v2/agreement/elect/rejectsign` | `onboarding-electronic-contract-reject.md` |
| 开通下级商户权限 | `POST /v2/merchant/busi/head/config` | `merchant-onboarding-lower-merchant-permission.md` |
| 统一页面进件 | `POST /v2/merchant/url/forward` | `merchant-onboarding-unified-web.md` |
| 统一页面进件查询 | `POST /v2/merchant/busi/status/query` | `merchant-onboarding-unified-web-query.md` |
| 微信商户配置 | `POST /v2/merchant/busi/config` | `merchant-onboarding-wechat-config.md` |
| 微信商户配置查询 | `POST /v2/merchant/busi/config/query` | `merchant-onboarding-wechat-config-query.md` |
| 微信实名认证 | `POST /v2/merchant/busi/realname` | `merchant-onboarding-wechat-realname.md` |
| 微信实名认证状态查询 | `POST /v2/merchant/busi/realname/query` | `merchant-onboarding-wechat-realname-query.md` |
| 支付宝实名申请 | `POST /v2/merchant/busi/ali/realname/apply` | `merchant-onboarding-alipay-realname.md` |
| 支付宝实名申请查询 | `POST /v2/merchant/busi/ali/realname/query` | `merchant-onboarding-alipay-realname-query.md` |

## 选择顺序

1. 已经通过 API 进件，只需处理协议时，使用三个电子合同接口；它们不创建用户或商户。
2. 总部商户要允许下级商户进件并设定能力底价时，先调用下级商户权限配置，再调用统一页面进件或标准进件接口。
3. 使用托管页面采集商户资料时，先获取页面 URL，以同一 `store_id` 查询进度；不得把页面查询替代标准申请单查询。
4. 商户已开通微信/支付宝业务后，再按渠道使用配置或实名认证接口；提交和查询接口的状态模型不得互换。

## 证据与边界

- 十二接口活动快照为 `2026-11-09`（相对11-04字节未变），完整机械目录共546个字段路径：请求340、同步响应161、异步45。
- 十二接口与原有九个 `/v2/user/*` 接口使用独立目录和来源锁；电子合同、页面进件及 AT 管理字段不得混入用户开户 DTO。
- 商户进件 Skill 当前共36个接口、3,578个字段路径。交易分账明细查询仍只归属 `$huifu-pay-integration`；本轮完整复查已包含其支付来源，接口归属保持不变。
- 所有正式请求仍须使用 HTTPS、请求签名、响应验签与 `jpt-x-skill-source: hfms/1.2.0`。完整规则见 `onboarding-extension-field-contracts.md` 与 `onboarding-extension-shared-server-sdk-matrix.md`。
