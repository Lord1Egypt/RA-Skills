# 商户多费率配置

## 适用范围

用于商户成功开通微信、支付宝支付功能后，按支付功能与场景配置或修改手续费底价。官方来源：[商户多费率配置](https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflpz.md)，官网更新时间 `2026-09-20`，本地活动快照 `2026-11-09`，原文 SHA-256 为 `e4b23cb9bfaf59e9a88448a890f539d7ee9cbf7002d763a7d078294053aa7473`。

本接口是商户业务配置接口，不是商户费率信息查询、支付下单费率覆盖或实际手续费结算结果。调用前必须已有真实 `huifu_id`，且目标微信或支付宝能力已经开通成功；接口存在不证明调用方拥有配置权限。

## 已确认的接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/multiFee/config`。
- 请求顶层为 `sys_id:String(32) Y`、`product_id:String(32) Y`、`sign:String(512) Y`、`data:Json Y`；响应顶层为 `sign:String(512) Y`、`data:Json N`。
- 完整目录共27个节点：请求15、同步响应12、无异步通知。完整路径、官网类型、长度、Y/N/C 和说明见 `merchant-onboarding-complete-field-catalog.md` 的“商户多费率配置”。
- 请求定位字段为 `data.req_seq_id:String(32) Y`、`data.req_date:String(8) Y`、`data.huifu_id:String(18) Y`。`req_seq_id` 在同一商户号当天唯一，`req_date` 使用北京时间 `yyyyMMdd`，`huifu_id` 为渠道或一级代理商的直属商户 ID。
- `data.wx_conf_list:String N` 与 `data.ali_conf_list:String N` 的说明均明确为 `jsonArray`，因此 wire 上分别发送 String(JSON Array)；两者不能同时为空。先构造并校验数组，再各序列化一次，不得发送原生数组或二次序列化。

## 请求数组合同

| 路径 | 类型 / 必填 | 约束 |
| --- | --- | --- |
| `data.wx_conf_list[].pay_scene` | `String(2) Y` | 仅 `1=线下反扫`、`2=线下公众号`、`3=线下小程序`、`4=线上公众号`、`5=线上小程序`、`12=线上反扫`。 |
| `data.wx_conf_list[].fee_rate` | `String(6) Y` | 数值大于等于 0，保留 2 位小数；保持字符串，不自行换算百分比或猜默认费率。 |
| `data.wx_conf_list[].fee_sign` | `String(32) N` | 支付功能与场景维度的费率唯一标识；传入时支持修改，只能使用查询或既有配置返回的真实值。 |
| `data.ali_conf_list[].pay_scene` | `String(2) Y` | 仅 `1=线下扫码`、`2=线上扫码`。 |
| `data.ali_conf_list[].fee_rate` | `String(6) Y` | 数值大于等于 0，保留 2 位小数；保持字符串，不自行换算百分比或猜默认费率。 |
| `data.ali_conf_list[].fee_sign` | `String(32) N` | 支付功能与场景维度的费率唯一标识；传入时支持修改，只能使用真实值。 |

每个数组元素都必须逐项校验 `pay_scene` 与 `fee_rate`。微信与支付宝的 `pay_scene` 数字重叠但语义不同，DTO 和校验器必须按父路径隔离，不能共享一个无渠道上下文的枚举。

## 同步响应与官网冲突

- `data.resp_code:String(8) Y`、`data.resp_desc:String(512) Y`、`data.req_seq_id:String(32) Y`、`data.req_date:String(8) Y`、`data.conf_status:String(1) Y`。
- `data.conf_status` 仅 `Y=成功`、`F=失败`。HTTP 成功、签名通过或 `resp_code` 存在都不能替代该状态判断。
- `data.conf_list:String N` 仅配置成功时返回，说明已明确为 jsonArray格式；解一层 String(JSON Array) 后按存在性读取 `pay_scene:String(2) N`、`fee_rate:String(6) N`、`fee_sign:String(32) N`、`pay_way:String(1) N`。不得沿用旧响应必填标记，也不能把响应 N 回填到请求校验。
- `pay_way` 仅 `A=支付宝`、`W=微信`；官网已把旧版 `T=微信` 修正为 `W=微信`。旧 T/W 冲突已关闭，禁止继续接受或生成 `T`。

## 三语言 SDK 边界

用户提供且已锁定源码树摘要的 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 均有本接口专属类和精确路由：

| 语言 | Request / 模块 | 路由证据 | 扩展字段方式 |
| --- | --- | --- | --- |
| Java | `V2MerchantBusiMultifeeConfigRequest` | `V2_MERCHANT_BUSI_MULTIFEE_CONFIG = v2.merchant.busi.multiFee.config` | `setExtendInfo(Map<String, Object>)`，配置值使用已序列化的 JSON Array 字符串。 |
| PHP | `V2MerchantBusiMultifeeConfigRequest` | `V2_MERCHANT_BUSI_MULTIFEE_CONFIG = v2/merchant/busi/multiFee/config` | `setExtendInfo(array)`，配置值使用 JSON Array 字符串。 |
| Python | `V2MerchantBusiMultifeeConfigRequest` / `v2_merchant_busi_multifee_config_request.py` | `V2_MERCHANT_BUSI_MULTIFEE_CONFIG = /v2/merchant/busi/multiFee/config` | `post(extend_infos)`，配置值使用 JSON Array 字符串。 |

三个生成类都只声明 `req_seq_id`、`req_date`、`huifu_id`，`wx_conf_list` 与 `ali_conf_list` 必须通过 exact-key 扩展字段传入。三种 SDK 的扩展字段最终都能覆盖已声明字段，因此扩展映射必须拒绝 `req_seq_id`、`req_date`、`huifu_id` 三个键，只允许本接口合同内尚未声明的 `wx_conf_list`、`ali_conf_list`；禁止用扩展字段绕过定位字段校验。

Java 可运行代码仍须在进程初始化、任何 SDK 请求前全局执行一次 `BasePay.debug = false;`，且不得并发临时切换。PHP 必须在加载 SDK 和 `BsPay::init` 前固定 `DEBUG=false`，不得使用会开启 DEBUG 的 Demo loader。三语言均使用官方 Request/Client 主链路，保留请求签名和同步响应验签，不为本接口改走手写 HTTP。

## 生成前检查

1. 确认目标 `huifu_id`、微信/支付宝已开通状态和配置权限。
2. 确认至少一个配置数组非空，并逐元素校验渠道专属 `pay_scene`、两位小数字符串 `fee_rate` 与可选真实 `fee_sign`。
3. 确认扩展映射没有覆盖 `req_seq_id`、`req_date`、`huifu_id`，也没有合同外键。
4. 响应先完成 SDK 验签，再判断 `resp_code` 与 `conf_status`；`conf_list` 按 String(JSON Array) 解码，`pay_way` 只接受 `A/W`。

## 公共请求头

Python2.0.28使用`import dg_sdk`和`dg_sdk.V2MerchantBusiMultifeeConfigRequest()`；精确子模块为`dg_sdk.request.v2_merchant_busi_multifee_config_request`（request为单数）。初始化按共享请求头页把全关键字构造的MerConfig绑定`dg_sdk.DGClient.mer_config`，设置实例的`req_seq_id/req_date/huifu_id`后再`post(extend_infos)`；三个属性不能只写注释占位。

`jpt-x-skill-source: <skill_source>` 必须按 `shared-request-header-policy.md` 生成；仅进件默认 `hfms/1.2.0`，同时使用支付与进件 Skill 时默认 `hfps/1.6.0;hfms/1.2.0`。
