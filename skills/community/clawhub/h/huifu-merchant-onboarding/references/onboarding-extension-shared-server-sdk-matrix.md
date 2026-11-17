# 进件扩展十二接口服务端 SDK 矩阵

## 当前 SDK 版本与源码边界

Python 当前 SDK 为 `2.0.28`，来自官方PyPI 2.0.28制品；本页专属类、新旧路由、字段与通用入口已按实际源码复核，不代表网关权限或业务结果已验证。其他版本差异按 `shared-server-sdk-matrix.md` 留 TODO 并继续明确的官方 SDK 接入，不设整体开发前置核验要求。

本轮依据2026-10-08已核验的官方固定Git提交/PyPI制品：Java `3.0.41`、PHP `2.0.31`、Python `2.0.28`，API来源为2026-11-09（十二页相对11-04字节未变）。九个商户/AT 接口有精确专属 Request；三个电子合同正式 Endpoint 已迁移到 `/v2/agreement/...`，未找到对应专属类，须使用官方 SDK 通用入口。SDK 中的 `V2Invoice*` 类仍指向旧 invoice 路由，不能用于新文档接口。进件 skill 版本为 1.2.0。

| 接口 | 三语言 Request 类 | 生成类直接字段 |
| --- | --- | --- |
| 下级商户权限配置 | `V2MerchantBusiHeadConfigRequest` | `req_seq_id/req_date/huifu_id/product_id/upper_huifu_id` |
| 统一页面进件 | `V2MerchantUrlForwardRequest` | `req_seq_id/req_date/upper_huifu_id/store_id` |
| 统一页面查询 | `V2MerchantBusiStatusQueryRequest` | `req_seq_id/req_date/store_id` |
| 微信商户配置 | `V2MerchantBusiConfigRequest` | `req_seq_id/req_date/huifu_id/fee_type/wx_woa_app_id/wx_woa_path/wx_applet_app_id` |
| 微信商户配置查询 | `V2MerchantBusiConfigQueryRequest` | `req_seq_id/req_date/huifu_id` |
| 微信实名认证 | `V2MerchantBusiRealnameRequest` | `req_seq_id/req_date/huifu_id/name/mobile/id_card_number/contact_type` |
| 微信实名状态查询 | `V2MerchantBusiRealnameQueryRequest` | `req_seq_id/req_date/huifu_id` |
| 支付宝实名申请 | `V2MerchantBusiAliRealnameApplyRequest` | `req_seq_id/req_date/huifu_id/auth_identity_info/contact_person_info` |
| 支付宝实名查询 | `V2MerchantBusiAliRealnameQueryRequest` | `req_seq_id/req_date/huifu_id` |

## 使用规则

- 代码生成必须读取 `shared-server-sdk-matrix.md` 的“同步返回形状”：Java常规调用已经返回业务data，不能再get("data")；PHP先检查SDK响应对象isError再取信封data；Python正常签名响应返回业务data。
- 九个商户/AT 接口必须使用对应官方 Request/Client 主链路；其余正式请求字段通过接口级 exact-key 白名单扩展。三种 SDK 的扩展合并都可能覆盖直接字段，扩展层必须拒绝覆盖生成类字段。
- Java 在任何请求前固定 `BasePay.debug=false`；PHP 在加载 SDK/Demo 与 `BsPay::init` 前固定 `DEBUG=false`；新代码不主动关闭 TLS 校验，本地 PHP 既有风险按下方提醒处理。
- 新版电子合同只用 `/v2/agreement/elect/signurl/resend`、`/v2/agreement/apply/list`、`/v2/agreement/elect/rejectsign`。Java 使用 `BasePayClient.request(params, "v2.agreement.elect.signurl.resend", false)`（其余功能码按精确路径转换）；PHP 使用 `postRequest(['funcCode' => 'v2/agreement/elect/signurl/resend', 'params' => $params])`；Python 使用 `DGTools.request_post('/v2/agreement/elect/signurl/resend', params)`。列表和拒签分别使用自己的精确路由，不复用重发。
- `V2InvoiceContractrepeatRequest`、`V2InvoiceQueryecmsapplylistRequest`、`V2InvoiceRejectsignRequest` 分别指向旧 `/v2/invoice/contractRepeat`、`/v2/invoice/queryEcmsApplyList`、`/v2/invoice/rejectSign`，不得拿来替代新 agreement 接口，也不得沿用旧类字段集合。通用入口字段按本轮完整目录校验，默认保留签验，仍不允许手写 HTTP。
- PHP 本地源码的 TLS 校验关闭风险按 `shared-server-sdk-matrix.md` 作为非阻断提醒，不要求先提交修复证据；Python 2.0.28 构造器仍使用正确关键字。未知 API 字段与通知协议按 `shared-overview.md` 提示核对对应官方文档、咨询汇付官方或汇付开发者交流沟通群，并继续明确的 SDK 流程；类存在不替代签验、真实数据和调用授权。
