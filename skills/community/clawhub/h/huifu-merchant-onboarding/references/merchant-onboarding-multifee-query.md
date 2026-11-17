# 商户多费率配置查询

## 适用范围

用于商户成功开通多费率配置后，查询支付功能与场景维度的手续费底价配置。官方来源：[商户多费率配置查询](https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflcx.md)，官网更新时间 `2026-09-20`，本地活动快照 `2026-11-09`，原文 SHA-256 为 `e2c0f53e77a1ef00827cc8be28ac688c068e5c8a4dc9f741845b841dcd16881a`。

本接口只读取多费率配置，不创建或修改配置，也不返回支付交易的实际手续费结算结果。调用前必须已有真实 `huifu_id`，且商户已成功开通多费率配置；接口存在不证明调用方拥有查询权限。

## 已确认的接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/multiFee/query`。
- 请求顶层为 `sys_id:String(32) Y`、`product_id:String(32) Y`、`sign:String(512) Y`、`data:Json Y`；响应顶层为 `sign:String(512) Y`、`data:Json N`。
- 完整目录共17个节点：请求8、同步响应9、无异步通知。完整路径、官网类型、长度、Y/N/C 和说明见 `merchant-onboarding-complete-field-catalog.md` 的“商户多费率配置查询”。
- 请求定位字段为 `data.req_seq_id:String(32) Y`、`data.req_date:String(8) Y`、`data.huifu_id:String(18) Y`。`req_seq_id` 在同一商户号当天唯一，`req_date` 使用北京时间 `yyyyMMdd`，`huifu_id` 为渠道或一级代理商的直属商户 ID。
- `data.fee_sign:String(32) N` 是支付功能与场景维度生成的费率唯一标识，必须来自真实配置或查询结果。官网没有说明省略后的精确筛选范围、返回数量和分页语义，不得自行承诺“返回全部配置”。

## 同步响应

- `data.resp_code:String(8) Y`、`data.resp_desc:String(512) Y`。
- `data.conf_list:String N` 仅在有配置结果时返回，说明已明确为 jsonArray格式；解一层 String(JSON Array) 后按存在性读取 `pay_scene:String(2) N`、`fee_rate:String(6) N`、`fee_sign:String(32) N`、`pay_way:String(1) N`。不得沿用旧响应必填标记。
- `data.conf_list[].pay_way:String(1) N` 存在时仅 `A=支付宝`、`W=微信`；缺失时不得猜测渠道。
- `pay_way=W` 时，`pay_scene` 仅 `1=线下反扫`、`2=线下公众号`、`3=线下小程序`、`4=线上公众号`、`5=线上小程序`、`12=线上反扫`；`pay_way=A` 时仅 `1=线下扫码`、`2=线上扫码`。必须先按 `pay_way` 选择枚举空间，不能复用一个无渠道上下文的数字枚举。
- `fee_rate:String(6) N` 存在时表示手续费底价百分比，数值大于等于0并保留2位小数；保持字符串，不自行换算或猜默认费率。`fee_sign:String(32) N` 存在时是后续交易或配置修改可传入的真实标识，不得为缺失值生成占位标识。

查询响应没有 `req_seq_id`、`req_date` 或 `conf_status` 字段。不得从“商户多费率配置”同步响应复制这三个字段；当前配置和查询两页都明确写 `W=微信`，禁止沿用旧版 `T`。

## 三语言 SDK 边界

用户提供且已锁定源码树摘要的 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 均有本接口专属类和精确路由：

| 语言 | Request / 模块 | 路由证据 | 扩展字段方式 |
| --- | --- | --- | --- |
| Java | `V2MerchantBusiMultifeeQueryRequest` | `V2_MERCHANT_BUSI_MULTIFEE_QUERY = v2.merchant.busi.multiFee.query` | `setExtendInfo(Map<String, Object>)`，使用 exact key `fee_sign`。 |
| PHP | `V2MerchantBusiMultifeeQueryRequest` | `V2_MERCHANT_BUSI_MULTIFEE_QUERY = v2/merchant/busi/multiFee/query` | `setExtendInfo(array)`，使用 exact key `fee_sign`。 |
| Python | `V2MerchantBusiMultifeeQueryRequest` / `v2_merchant_busi_multifee_query_request.py` | `V2_MERCHANT_BUSI_MULTIFEE_QUERY = /v2/merchant/busi/multiFee/query` | `post(extend_infos)`，使用 exact key `fee_sign`。 |

三个生成类都只声明 `req_seq_id`、`req_date`、`huifu_id`，可选 `fee_sign` 必须通过 exact-key 扩展字段传入。三种 SDK 的扩展字段最终都能覆盖已声明字段，因此扩展映射必须拒绝 `req_seq_id`、`req_date`、`huifu_id` 三个键，只允许本接口合同内尚未声明的 `fee_sign`；禁止用扩展字段绕过定位字段校验或传入配置接口的 `wx_conf_list/ali_conf_list`。

Java 可运行代码仍须在进程初始化、任何 SDK 请求前全局执行一次 `BasePay.debug = false;`，且不得并发临时切换。PHP 必须在加载 SDK 和 `BsPay::init` 前固定 `DEBUG=false`，不得使用会开启 DEBUG 的 Demo loader。三语言均使用官方 Request/Client 主链路，保留请求签名和同步响应验签，不为本接口改走手写 HTTP。

## 生成前检查

1. 确认目标 `huifu_id`、多费率已开通状态和查询权限。
2. 传 `fee_sign` 时确认它来自真实配置；不传时明确官网未定义精确返回范围和数量，不猜分页或全量语义。
3. 确认扩展映射没有覆盖 `req_seq_id`、`req_date`、`huifu_id`，也没有 `fee_sign` 之外的合同外键。
4. 响应先完成 SDK 验签，再判断 `resp_code`；`conf_list` 按 String(JSON Array) 解码后再按 `pay_way=A/W` 选择 `pay_scene` 枚举。

## 公共请求头

`jpt-x-skill-source: <skill_source>` 必须按 `shared-request-header-policy.md` 生成；仅进件默认 `hfms/1.2.0`，同时使用支付与进件 Skill 时默认 `hfps/1.6.0;hfms/1.2.0`。
