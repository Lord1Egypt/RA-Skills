# 支付接口完整字段路径目录

> 生成来源：`payment-source-lock-2026-11-04.json` 锁定的 `2026-11-04` 官方快照；共 24 个 API、3,096 个接口内完整路径。

## 目录

- 使用规则
- 生成覆盖摘要
- 聚合支付下单
- 聚合交易查询
- 聚合交易关单
- 聚合交易关单查询
- 聚合交易退款
- 聚合交易退款查询
- 对账单-v2详细API
- H5/PC预下单
- 支付宝小程序预下单
- 微信小程序预下单
- 抖音直连下单
- 托管交易查询
- 托管交易退款
- 托管交易退款查询
- 托管交易关单
- 拆单支付订单查询
- 交易分账明细查询
- 余额支付查询
- 余额支付退款
- 余额支付退款查询
- 手续费试算
- 付款关系提交
- 余额支付发送短信验证码
- 余额支付

## 使用规则

1. 字段身份必须使用“接口 + 数据面 + 合同定位路径”，禁止按叶字段名或实际 JSON 路径去重；同一 wire 字段可因交易分支不同而拥有不同合同。
2. 数组仅按官方 `Array/jsonArray` 语义添加 `[]`；Object、String(JSON) 不因名称含 `_list` 自动改成数组。
3. “合同定位路径”忠实保留官网展示树；只有官方说明明确写出“只为方便文档展示”或本地已记录接口所有者确认的节点才从 wire/解码路径移除。聚合交易查询 `response.data.method_expand` 下的 `T_*` / `A_*` / `U_*` 行是场景分组，不是 wire key；`method_expand` 只解码一次，场景字段在解码后的对象根层平铺。聚合查询及退款查询响应中的 `tx_metadata` 没有该说明，必须保留为真实 String(JSON) 容器。
4. “wire 字段路径”只标线上报文中的字段；String(JSON) 子字段必须先从该容器反序列化，再使用“解码后路径”。Object/Array 的真实嵌套路径直接出现在 wire JSON 中。
5. 官网把父字段定义为 String 且展开子表时，子字段绝不直接扩展成 wire 路径：有 JSON 线索时按 String(JSON) 建模；无线索时把子表编码标为 `[需要官方确认]`。String(JSON Array) 的 `[]` 只属于解码路径，不属于 wire key。
6. 官网未标异步外层字段名时，合同定位路径使用 `unconfirmed_payload` 作为目录数据面标签，但 wire 列必须明确为未知，禁止把该标签发明成真实字段；只标出 `data`、未说明编码时也不得猜 JSON 与 String(JSON)。
7. 类型、长度或必填为空时原样保留 `—`；“确认状态”逐行区分结构字段的 `N/A` 和必须标记的 `[需要官方确认]`，不得把未知长度解释为无限制。
8. 本目录提供字段合同；场景条件、SDK、安全硬停、通知终态和勘误仍需联读对应原子 reference。
9. 官方字段说明中的绝对链接保持原值；`#锚点` 或相对链接会按该接口的“原始地址”解析成可点击绝对地址，并同时保留官网相对地址原文。已确认的坏锚点会追加规范目标：`#业务返回码` 补公共返回码全集，聚合下单 `notify_url` 的 `#异步返回参数` 同时补正扫、反扫通知参数及异步消息简介。它们只是规范资料指针，不是字段默认值。`notify_url`、`jump_url`、下载地址、二维码等说明里的裸 URL 示例属于运行时值或格式示例，不得当作外部资料或建议值。

## 生成覆盖摘要

| API | 字段路径数 | 扩展表数 | 最大路径深度 |
| --- | ---: | ---: | ---: |
| 聚合支付下单 | 860 | 113 | 7 |
| 聚合交易查询 | 273 | 38 | 7 |
| 聚合交易关单 | 23 | 0 | 3 |
| 聚合交易关单查询 | 23 | 0 | 3 |
| 聚合交易退款 | 173 | 25 | 6 |
| 聚合交易退款查询 | 42 | 5 | 6 |
| 对账单-v2详细API | 31 | 2 | 4 |
| H5/PC预下单 | 333 | 48 | 6 |
| 支付宝小程序预下单 | 169 | 20 | 5 |
| 微信小程序预下单 | 222 | 30 | 6 |
| 抖音直连下单 | 126 | 12 | 6 |
| 托管交易查询 | 197 | 24 | 6 |
| 托管交易退款 | 146 | 21 | 6 |
| 托管交易退款查询 | 87 | 12 | 6 |
| 托管交易关单 | 27 | 0 | 3 |
| 拆单支付订单查询 | 69 | 7 | 7 |
| 交易分账明细查询 | 29 | 1 | 4 |
| 余额支付查询 | 36 | 2 | 5 |
| 余额支付退款 | 44 | 5 | 5 |
| 余额支付退款查询 | 31 | 2 | 5 |
| 手续费试算 | 27 | 0 | 3 |
| 付款关系提交 | 24 | 2 | 4 |
| 余额支付发送短信验证码 | 14 | 0 | 3 |
| 余额支付 | 90 | 7 | 5 |

合计：`3,096` 个接口内完整字段路径。

## 聚合支付下单

- 原始地址：<https://paas.huifu.com/partners/lightning/api/jhzfxd.md>
- SHA-256：`8412cf1c21eaba1164e281fbf4b881e98c7bd9524a1d5def920ff00d4247d8a5`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：MCS |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 数据 | `Json` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `N` | 已确认 | 格式yyyyMMdd；示例值：20220905 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：rQ[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.trade_type` | `request.data.trade_type` | `—（直接 JSON 路径）` | 交易类型 | `String` | `16` | `Y` | 已确认 | T_JSAPI：微信公众号支付；T_MINIAPP：微信小程序支付；T_APP：微信APP支付；T_MICROPAY：微信反扫支付；A_JSAPI：支付宝JS支付；A_NATIVE：支付宝正扫支付；A_MICROPAY：支付宝反扫支付；U_JSAPI：银联JS支付；U_NATIVE：银联正扫支付；U_MICROPAY：银联反扫支付；示例值：A_NATIVE |
| `request.data.trans_amt` | `request.data.trans_amt` | `—（直接 JSON 路径）` | 交易金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1000.00，最低传入0.01 |
| `request.data.goods_desc` | `request.data.goods_desc` | `—（直接 JSON 路径）` | 商品描述 | `String` | `128` | `Y` | 已确认 | 示例值：XX商品 |
| `request.data.remark` | `request.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `255` | `N` | 已确认 | 交易后原样返回；示例值：备注 |
| `request.data.acct_id` | `request.data.acct_id` | `—（直接 JSON 路径）` | 账户号 | `String` | `9` | `N` | 已确认 | 可指定收款账户号，仅支持基本户、现金户，不填默认为基本户；示例值：F00598600 |
| `request.data.time_expire` | `request.data.time_expire` | `—（直接 JSON 路径）` | 交易有效期 | `String` | `14` | `N` | 已确认 | 该笔订单允许付款最晚时间，建议大于1分钟；注意：微信、支付宝交易有订单超时时间，默认两小时关单；请求格式：yyyyMMddHHmmss；示例值：20220912111230 |
| `request.data.delay_acct_flag` | `request.data.delay_acct_flag` | `—（直接 JSON 路径）` | 延迟标识 | `String` | `1` | `N` | 已确认 | Y 为延迟 N为不延迟，不传默认N；示例值：Y |
| `request.data.fee_flag` | `request.data.fee_flag` | `—（直接 JSON 路径）` | 手续费扣款标识 | `Integer` | `1` | `N` | 已确认 | 1: 外扣 2: 内扣 (默认取控台配置值)；示例值：1 |
| `request.data.limit_pay_type` | `request.data.limit_pay_type` | `—（直接 JSON 路径）` | 禁用支付方式 | `String` | `128` | `N` | 已确认 | 本次交易禁止使用的支付方式，默认不禁用；[取值参见说明](https://paas.huifu.com/partners/lightning/api/jhzfxd.md#参数说明)（官网相对地址原文：`#参数说明`）；示例值：NO_CREDIT |
| `request.data.channel_no` | `request.data.channel_no` | `—（直接 JSON 路径）` | 渠道号 | `String` | `32` | `N` | 已确认 | 如果交易走自有渠道请联系运维人员获取；示例值:10000001 |
| `request.data.pay_scene` | `request.data.pay_scene` | `—（直接 JSON 路径）` | 场景类型 | `String` | `2` | `N` | 已确认 | 参见[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E5%BE%AE%E4%BF%A1%E4%B8%9A%E5%8A%A1%E5%BC%80%E9%80%9A%E7%B1%BB%E5%9E%8B)说明；示例值:02 |
| `request.data.term_div_coupon_type` | `request.data.term_div_coupon_type` | `—（直接 JSON 路径）` | 传入分帐遇到优惠的处理规则 | `String` | `2` | `N` | 已确认 | 1:按比例分,2:按分账明细顺序保障,3:只给交易商户（默认)；示例值:1 |
| `request.data.fq_mer_discount_flag` | `request.data.fq_mer_discount_flag` | `—（直接 JSON 路径）` | 商户贴息标记 | `String` | `1` | `N` | 已确认 | 商户补贴活动，Y: 商户全额贴息，P：商户部分贴息，不传为非商户贴息（默认）；示例值：Y；选择P：商户部分贴息活动，需同时在【ali_business_params：商户业务信息】中传入支付宝约定的活动参数，参数说明详见分期支付指引文档。 |
| `request.data.notify_url` | `request.data.notify_url` | `—（直接 JSON 路径）` | 异步通知地址 | `String` | `504` | `N` | 已确认 | 交易异步通知地址，http或https开头，异步回调报文格式见[异步返回参数](https://paas.huifu.com/partners/lightning/api/jhzfxd.md#异步返回参数)（官网相对地址原文：`#异步返回参数`）（已确认同时指向[聚合正扫异步返回参数](https://paas.huifu.com/partners/lightning/api/jhzfxd.md#聚合正扫异步返回参数)和[聚合反扫异步返回参数](https://paas.huifu.com/partners/lightning/api/jhzfxd.md#聚合反扫异步返回参数)两套通知参数；通用传输、验签、ACK、重试与幂等规则见[异步消息简介](https://paas.huifu.com/partners/start/ybxx/jiekouguifan_ybxx.md)）；示例值：https://callback.service.com/xx |
| `request.data.method_expand` | `request.data.method_expand` | `—（String(JSON) 容器）` | 交易类型扩展参数 | `String` | `—` | `Y` | [需要官方确认]：长度 | jsonObject字符串 |
| `request.data.method_expand.T_JSAPI` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 微信公众号支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `request.data.method_expand.T_JSAPI.sub_appid` | `request.data.method_expand` | `$.sub_appid` | 子商户应用ID | `String` | `32` | `N` | 已确认 | 子商户在微信申请的应用ID，全局唯一。**走聚合正扫发货管理的商户，使用的微信公众号/小程序支付 需要填写sub_appid+sub_openid**；示例值：wxd678efh567hg6999 |
| `request.data.method_expand.T_JSAPI.sub_openid` | `request.data.method_expand` | `$.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 公众号和小程序场景必填。用户在子商户sub_appid下的唯一标识。下单前需获取到用户的sub_openid，sub_openid获取详见微信文档[openid获取](https://pay.weixin.qq.com/docs/partner/development/glossary/parameter.html)。；示例值：oUpF8uMuAJO_M2pxb1Q9zNjWeS6o |
| `request.data.method_expand.T_JSAPI.attach` | `request.data.method_expand` | `$.attach` | 附加数据 | `String` | `127` | `N` | 已确认 | 在查询api和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据；示例值：附加数据 |
| `request.data.method_expand.T_JSAPI.body` | `request.data.method_expand` | `$.body` | 商品描述 | `String` | `128` | `N` | 已确认 | 商品或支付单简要描述，格式要求：门店品牌名-城市分店名-实际商品名称；示例值：image形象店-深圳腾大- QQ 公仔 |
| `request.data.method_expand.T_JSAPI.detail` | `request.data.method_expand` | `$.detail` | 商品详情 | `Object` | `—` | `N` | N/A：结构字段长度 | 单品优惠功能字段 |
| `request.data.method_expand.T_JSAPI.detail.cost_price` | `request.data.method_expand` | `$.detail.cost_price` | 订单原价(元) | `String` | `12` | `N` | 已确认 | 1.商户侧一张小票订单可能被分多次支付，订单原价用于记录整张小票的交易金额。 ；2.当订单原价与支付金额不相等，则不享受优惠。；3.该字段主要用于防止同一张小票分多次支付，以享受多次优惠的情况，正常支付订单不必上传此参数。；示例值：999.00 |
| `request.data.method_expand.T_JSAPI.detail.receipt_id` | `request.data.method_expand` | `$.detail.receipt_id` | 商品小票ID | `String` | `32` | `N` | 已确认 | 商家小票 ID；示例值：[官网示例已脱敏] |
| `request.data.method_expand.T_JSAPI.detail.goods_detail[]` | `request.data.method_expand` | `$.detail.goods_detail[]` | 单品列表 | `Array` | `—` | `Y` | N/A：结构字段长度 | 单品信息，使用Json数组格式提交 |
| `request.data.method_expand.T_JSAPI.detail.goods_detail[].goods_id` | `request.data.method_expand` | `$.detail.goods_detail[].goods_id` | 商品编码 | `String` | `32` | `N` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `request.data.method_expand.T_JSAPI.detail.goods_detail[].goods_name` | `request.data.method_expand` | `$.detail.goods_detail[].goods_name` | 商品名称 | `String` | `256` | `N` | 已确认 | 商品的实际名称；示例值：太龙双黄连口服液 |
| `request.data.method_expand.T_JSAPI.detail.goods_detail[].price` | `request.data.method_expand` | `$.detail.goods_detail[].price` | 商品单价(元) | `String` | `12` | `N` | 已确认 | 如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔 100 元的订单使用了商场发的优惠券 100-50，则活动商品的单价应为原单价-50；示例值：43.00 |
| `request.data.method_expand.T_JSAPI.detail.goods_detail[].quantity` | `request.data.method_expand` | `$.detail.goods_detail[].quantity` | 商品数量 | `Integer` | `11` | `N` | 已确认 | 用户购买的数量；示例值：1 |
| `request.data.method_expand.T_JSAPI.detail.goods_detail[].wxpay_goods_id` | `request.data.method_expand` | `$.detail.goods_detail[].wxpay_goods_id` | 微信侧商品编码 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.method_expand.T_JSAPI.goods_tag` | `request.data.method_expand` | `$.goods_tag` | 订单优惠标记 | `String` | `32` | `N` | 已确认 | 代金券或立减优惠功能的参数；示例值：WXG |
| `request.data.method_expand.T_MINIAPP` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 微信小程序支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `request.data.method_expand.T_MINIAPP.sub_appid` | `request.data.method_expand` | `$.sub_appid` | 子商户应用ID | `String` | `32` | `N` | 已确认 | 子商户在微信申请的应用ID，全局唯一。**走聚合正扫发货管理的商户，使用的微信公众号/小程序支付 需要填写sub_appid+sub_openid**；示例值：wxd678efh567hg6999 |
| `request.data.method_expand.T_MINIAPP.sub_openid` | `request.data.method_expand` | `$.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 公众号和小程序场景必填。用户在子商户sub_appid下的唯一标识。下单前需获取到用户的sub_openid，sub_openid获取详见微信文档[openid获取](https://pay.weixin.qq.com/docs/partner/development/glossary/parameter.html)。；示例值：oUpF8uMuAJO_M2pxb1Q9zNjWeS6o |
| `request.data.method_expand.T_MINIAPP.attach` | `request.data.method_expand` | `$.attach` | 附加数据 | `String` | `127` | `N` | 已确认 | 在查询api和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据；示例值：附加数据 |
| `request.data.method_expand.T_MINIAPP.body` | `request.data.method_expand` | `$.body` | 商品描述 | `String` | `128` | `N` | 已确认 | 商品或支付单简要描述，格式要求：门店品牌名-城市分店名-实际商品名称；示例值：image形象店-深圳腾大- QQ 公仔 |
| `request.data.method_expand.T_MINIAPP.detail` | `request.data.method_expand` | `$.detail` | 商品详情 | `Object` | `—` | `N` | N/A：结构字段长度 | 单品优惠功能字段 |
| `request.data.method_expand.T_MINIAPP.detail.cost_price` | `request.data.method_expand` | `$.detail.cost_price` | 订单原价(元) | `String` | `12` | `N` | 已确认 | 1.商户侧一张小票订单可能被分多次支付，订单原价用于记录整张小票的交易金额。 ；2.当订单原价与支付金额不相等，则不享受优惠。；3.该字段主要用于防止同一张小票分多次支付，以享受多次优惠的情况，正常支付订单不必上传此参数。；示例值：999.00 |
| `request.data.method_expand.T_MINIAPP.detail.receipt_id` | `request.data.method_expand` | `$.detail.receipt_id` | 商品小票ID | `String` | `32` | `N` | 已确认 | 商家小票 ID；示例值：[官网示例已脱敏] |
| `request.data.method_expand.T_MINIAPP.detail.goods_detail[]` | `request.data.method_expand` | `$.detail.goods_detail[]` | 单品列表 | `Array` | `—` | `Y` | N/A：结构字段长度 | 单品信息，使用Json数组格式提交 |
| `request.data.method_expand.T_MINIAPP.detail.goods_detail[].goods_id` | `request.data.method_expand` | `$.detail.goods_detail[].goods_id` | 商品编码 | `String` | `32` | `N` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `request.data.method_expand.T_MINIAPP.detail.goods_detail[].goods_name` | `request.data.method_expand` | `$.detail.goods_detail[].goods_name` | 商品名称 | `String` | `256` | `N` | 已确认 | 商品的实际名称；示例值：太龙双黄连口服液 |
| `request.data.method_expand.T_MINIAPP.detail.goods_detail[].price` | `request.data.method_expand` | `$.detail.goods_detail[].price` | 商品单价(元) | `String` | `12` | `N` | 已确认 | 如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔 100 元的订单使用了商场发的优惠券 100-50，则活动商品的单价应为原单价-50；示例值：43.00 |
| `request.data.method_expand.T_MINIAPP.detail.goods_detail[].quantity` | `request.data.method_expand` | `$.detail.goods_detail[].quantity` | 商品数量 | `Integer` | `11` | `N` | 已确认 | 用户购买的数量；示例值：1 |
| `request.data.method_expand.T_MINIAPP.detail.goods_detail[].wxpay_goods_id` | `request.data.method_expand` | `$.detail.goods_detail[].wxpay_goods_id` | 微信侧商品编码 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.method_expand.T_MINIAPP.goods_tag` | `request.data.method_expand` | `$.goods_tag` | 订单优惠标记 | `String` | `32` | `N` | 已确认 | 代金券或立减优惠功能的参数；示例值：WXG |
| `request.data.method_expand.T_APP` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 微信APP支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `request.data.method_expand.T_APP.sub_appid` | `request.data.method_expand` | `$.sub_appid` | 子商户应用ID | `String` | `32` | `N` | 已确认 | 子商户在微信申请的应用ID，全局唯一。**走聚合正扫发货管理的商户，使用的微信公众号/小程序支付 需要填写sub_appid+sub_openid**；示例值：wxd678efh567hg6999 |
| `request.data.method_expand.T_APP.sub_openid` | `request.data.method_expand` | `$.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 公众号和小程序场景必填。用户在子商户sub_appid下的唯一标识。下单前需获取到用户的sub_openid，sub_openid获取详见微信文档[openid获取](https://pay.weixin.qq.com/docs/partner/development/glossary/parameter.html)。；示例值：oUpF8uMuAJO_M2pxb1Q9zNjWeS6o |
| `request.data.method_expand.T_APP.attach` | `request.data.method_expand` | `$.attach` | 附加数据 | `String` | `127` | `N` | 已确认 | 在查询api和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据；示例值：附加数据 |
| `request.data.method_expand.T_APP.body` | `request.data.method_expand` | `$.body` | 商品描述 | `String` | `128` | `N` | 已确认 | 商品或支付单简要描述，格式要求：门店品牌名-城市分店名-实际商品名称；示例值：image形象店-深圳腾大- QQ 公仔 |
| `request.data.method_expand.T_APP.detail` | `request.data.method_expand` | `$.detail` | 商品详情 | `Object` | `—` | `N` | N/A：结构字段长度 | 单品优惠功能字段 |
| `request.data.method_expand.T_APP.detail.cost_price` | `request.data.method_expand` | `$.detail.cost_price` | 订单原价(元) | `String` | `12` | `N` | 已确认 | 1.商户侧一张小票订单可能被分多次支付，订单原价用于记录整张小票的交易金额。 ；2.当订单原价与支付金额不相等，则不享受优惠。；3.该字段主要用于防止同一张小票分多次支付，以享受多次优惠的情况，正常支付订单不必上传此参数。；示例值：999.00 |
| `request.data.method_expand.T_APP.detail.receipt_id` | `request.data.method_expand` | `$.detail.receipt_id` | 商品小票ID | `String` | `32` | `N` | 已确认 | 商家小票 ID；示例值：[官网示例已脱敏] |
| `request.data.method_expand.T_APP.detail.goods_detail[]` | `request.data.method_expand` | `$.detail.goods_detail[]` | 单品列表 | `Array` | `—` | `Y` | N/A：结构字段长度 | 单品信息，使用Json数组格式提交 |
| `request.data.method_expand.T_APP.detail.goods_detail[].goods_id` | `request.data.method_expand` | `$.detail.goods_detail[].goods_id` | 商品编码 | `String` | `32` | `N` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `request.data.method_expand.T_APP.detail.goods_detail[].goods_name` | `request.data.method_expand` | `$.detail.goods_detail[].goods_name` | 商品名称 | `String` | `256` | `N` | 已确认 | 商品的实际名称；示例值：太龙双黄连口服液 |
| `request.data.method_expand.T_APP.detail.goods_detail[].price` | `request.data.method_expand` | `$.detail.goods_detail[].price` | 商品单价(元) | `String` | `12` | `N` | 已确认 | 如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔 100 元的订单使用了商场发的优惠券 100-50，则活动商品的单价应为原单价-50；示例值：43.00 |
| `request.data.method_expand.T_APP.detail.goods_detail[].quantity` | `request.data.method_expand` | `$.detail.goods_detail[].quantity` | 商品数量 | `Integer` | `11` | `N` | 已确认 | 用户购买的数量；示例值：1 |
| `request.data.method_expand.T_APP.detail.goods_detail[].wxpay_goods_id` | `request.data.method_expand` | `$.detail.goods_detail[].wxpay_goods_id` | 微信侧商品编码 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.method_expand.T_APP.goods_tag` | `request.data.method_expand` | `$.goods_tag` | 订单优惠标记 | `String` | `32` | `N` | 已确认 | 代金券或立减优惠功能的参数；示例值：WXG |
| `request.data.method_expand.T_MICROPAY` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 微信反扫支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `request.data.method_expand.T_MICROPAY.auth_code` | `request.data.method_expand` | `$.auth_code` | 支付授权码 | `String` | `128` | `Y` | 已确认 | 扫码设备读出的条形码或者二维码信息；示例值：[官网示例已脱敏] |
| `request.data.method_expand.T_MICROPAY.sub_appid` | `request.data.method_expand` | `$.sub_appid` | 子商户公众账号id | `String` | `32` | `N` | 已确认 | 微信分配的子商户公众账号id，微信js/小程序支付必传。；如需在支付完成后获取sub_openid则此参数必传。示例值：wxec280d4c8a1cc2ca |
| `request.data.method_expand.T_MICROPAY.device_info` | `request.data.method_expand` | `$.device_info` | 设备号 | `String` | `32` | `N` | 已确认 | 终端设备号(门店号或收银设备id)，示例值：[官网示例已脱敏] |
| `request.data.method_expand.T_MICROPAY.goods_tag` | `request.data.method_expand` | `$.goods_tag` | 订单优惠标记 | `String` | `32` | `N` | 已确认 | 代金券或立减优惠功能的参数；示例值：WXG |
| `request.data.method_expand.T_MICROPAY.attach` | `request.data.method_expand` | `$.attach` | 附加数据 | `String` | `127` | `N` | 已确认 | 在查询api和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据；示例值：附加数据 |
| `request.data.method_expand.T_MICROPAY.detail` | `request.data.method_expand` | `$.detail` | 商品详情 | `Object` | `6000` | `N` | 已确认 | 商品详情 |
| `request.data.method_expand.T_MICROPAY.detail.cost_price` | `request.data.method_expand` | `$.detail.cost_price` | 订单原价(元) | `String` | `12` | `N` | 已确认 | 1.商户侧一张小票订单可能被分多次支付，订单原价用于记录整张小票的交易金额。 ；2.当订单原价与支付金额不相等，则不享受优惠。；3.该字段主要用于防止同一张小票分多次支付，以享受多次优惠的情况，正常支付订单不必上传此参数。；示例值：999.00 |
| `request.data.method_expand.T_MICROPAY.detail.receipt_id` | `request.data.method_expand` | `$.detail.receipt_id` | 商品小票ID | `String` | `32` | `N` | 已确认 | 商家小票 ID；示例值：[官网示例已脱敏] |
| `request.data.method_expand.T_MICROPAY.detail.goods_detail[]` | `request.data.method_expand` | `$.detail.goods_detail[]` | 单品列表 | `Array` | `—` | `Y` | N/A：结构字段长度 | 单品信息，使用Json数组格式提交 |
| `request.data.method_expand.T_MICROPAY.detail.goods_detail[].goods_id` | `request.data.method_expand` | `$.detail.goods_detail[].goods_id` | 商品编码 | `String` | `32` | `N` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `request.data.method_expand.T_MICROPAY.detail.goods_detail[].goods_name` | `request.data.method_expand` | `$.detail.goods_detail[].goods_name` | 商品名称 | `String` | `256` | `N` | 已确认 | 商品的实际名称；示例值：太龙双黄连口服液 |
| `request.data.method_expand.T_MICROPAY.detail.goods_detail[].price` | `request.data.method_expand` | `$.detail.goods_detail[].price` | 商品单价(元) | `String` | `12` | `N` | 已确认 | 如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔 100 元的订单使用了商场发的优惠券 100-50，则活动商品的单价应为原单价-50；示例值：43.00 |
| `request.data.method_expand.T_MICROPAY.detail.goods_detail[].quantity` | `request.data.method_expand` | `$.detail.goods_detail[].quantity` | 商品数量 | `Integer` | `11` | `N` | 已确认 | 用户购买的数量；示例值：1 |
| `request.data.method_expand.T_MICROPAY.detail.goods_detail[].wxpay_goods_id` | `request.data.method_expand` | `$.detail.goods_detail[].wxpay_goods_id` | 微信侧商品编码 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.method_expand.T_MICROPAY.scene_info` | `request.data.method_expand` | `$.scene_info` | 场景信息 | `Object` | `2048` | `N` | 已确认 | 该字段用于上报场景信息，目前支持上报实际门店信息 |
| `request.data.method_expand.T_MICROPAY.scene_info.store_info` | `request.data.method_expand` | `$.scene_info.store_info` | 门店信息 | `Object` | `—` | `Y` | N/A：结构字段长度 | 门店信息 |
| `request.data.method_expand.T_MICROPAY.scene_info.store_info.id` | `request.data.method_expand` | `$.scene_info.store_info.id` | 门店id | `String` | `32` | `N` | 已确认 | 门店编号，由商户自定义；示例值：sh001 |
| `request.data.method_expand.T_MICROPAY.scene_info.store_info.name` | `request.data.method_expand` | `$.scene_info.store_info.name` | 门店名称 | `String` | `64` | `N` | 已确认 | 门店名称，由商户自定义；示例值：上海宝山分店 |
| `request.data.method_expand.T_MICROPAY.scene_info.store_info.area_code` | `request.data.method_expand` | `$.scene_info.store_info.area_code` | 门店行政区划码 | `String` | `6` | `N` | 已确认 | 门店所在地行政区划码，详见[行政区划代码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)，示例值：310101 |
| `request.data.method_expand.T_MICROPAY.scene_info.store_info.address` | `request.data.method_expand` | `$.scene_info.store_info.address` | 门店详细地址 | `String` | `128` | `N` | 已确认 | 门店详细地址，由商户自定义；示例值：上海宝山区共富路100号 |
| `request.data.method_expand.T_MICROPAY.promotion_flag` | `request.data.method_expand` | `$.promotion_flag` | 单品优惠标识 | `String` | `1` | `N` | 已确认 | 直联模式使用字段；Y-是，N-否，默认否；示例值：Y；若使用单品优惠，该字段必填，若该字段为Y，则商品详情【detail】必填 |
| `request.data.method_expand.T_MICROPAY.spbill_create_ip` | `request.data.method_expand` | `$.spbill_create_ip` | 收款设备IP | `String` | `16` | `C` | 已确认 | 直联模式必填字段；示例值：192.168.2.2 |
| `request.data.method_expand.T_MICROPAY.receipt` | `request.data.method_expand` | `$.receipt` | 电子发票入口开放标识 | `String` | `8` | `N` | 已确认 | 直联模式使用字段；Y-是；示例值：Y；传入Y时，支付成功消息和支付详情页将出现开票入口。；需要在微信支付商户平台或微信公众平台开通电子发票功能，传此字段才可生效 |
| `request.data.method_expand.A_JSAPI` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 支付宝JS支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `request.data.method_expand.A_JSAPI.alipay_store_id` | `request.data.method_expand` | `$.alipay_store_id` | 支付宝的店铺编号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_JSAPI.buyer_id` | `request.data.method_expand` | `$.buyer_id` | 买家的支付宝唯一用户号 | `String` | `28` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_JSAPI.buyer_logon_id` | `request.data.method_expand` | `$.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com；交易类型为A_JSAPI时【买家支付宝账号】与【买家支付宝用户号】二选一必填 |
| `request.data.method_expand.A_JSAPI.goods_detail[]` | `request.data.method_expand` | `$.goods_detail[]` | 订单包含的商品列表信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 订单包含的商品列表信息 |
| `request.data.method_expand.A_JSAPI.goods_detail[].goods_id` | `request.data.method_expand` | `$.goods_detail[].goods_id` | 商品的编号 | `String` | `32` | `Y` | 已确认 | 示例值：apple-01 |
| `request.data.method_expand.A_JSAPI.goods_detail[].goods_name` | `request.data.method_expand` | `$.goods_detail[].goods_name` | 商品名称 | `String` | `256` | `Y` | 已确认 | 示例值：ipad |
| `request.data.method_expand.A_JSAPI.goods_detail[].price` | `request.data.method_expand` | `$.goods_detail[].price` | 商品单价(元) | `String` | `16` | `Y` | 已确认 | 单位：元；示例值：43.40 |
| `request.data.method_expand.A_JSAPI.goods_detail[].quantity` | `request.data.method_expand` | `$.goods_detail[].quantity` | 商品数量 | `String` | `10` | `Y` | 已确认 | 示例值：40 |
| `request.data.method_expand.A_JSAPI.goods_detail[].body` | `request.data.method_expand` | `$.goods_detail[].body` | 商品描述信息 | `String` | `1000` | `N` | 已确认 | 示例值：个人电脑 |
| `request.data.method_expand.A_JSAPI.goods_detail[].categories_tree` | `request.data.method_expand` | `$.goods_detail[].categories_tree` | 商品类目树 | `String` | `128` | `N` | 已确认 | 商品类目树，从商品类目根节点到叶子节点的类目 id 组成，类目 id 值使用\|分割；示例值：124868003\|126232002\|126252004 |
| `request.data.method_expand.A_JSAPI.goods_detail[].show_url` | `request.data.method_expand` | `$.goods_detail[].show_url` | 商品的展示地址 | `String` | `400` | `N` | 已确认 | 示例值：https://paas.huifu.com/checkout/demo/pc/goodsDetail.html |
| `request.data.method_expand.A_JSAPI.goods_detail[].goods_category` | `request.data.method_expand` | `$.goods_detail[].goods_category` | 商品类目 | `String` | `24` | `N` | 已确认 | 示例值：34543238 |
| `request.data.method_expand.A_JSAPI.extend_params` | `request.data.method_expand` | `$.extend_params` | 业务扩展参数 | `Object` | `—` | `N` | N/A：结构字段长度 | 业务扩展参数 |
| `request.data.method_expand.A_JSAPI.extend_params.card_type` | `request.data.method_expand` | `$.extend_params.card_type` | 卡类型 | `String` | `32` | `N` | 已确认 | 示例值：S0JP0000 |
| `request.data.method_expand.A_JSAPI.extend_params.food_order_type` | `request.data.method_expand` | `$.extend_params.food_order_type` | 支付宝点餐场景类型 | `String` | `20` | `N` | 已确认 | QR_ORDER（店内扫码点餐）；PRE_ORDER（预点到店自提）；HOME_DELIVERY（外送到家）；DIRECT_PAYMENT（直接付款）；QR_FOOD_ORDER（点餐先付）；P_QR_FOOD_ORDER（点餐后付）；SELF_PICK（门店自提）；TAKE_OUT （餐饮外卖）；OTHER（其他）；该参数只适用于支付宝支付窗交易接口；示例值：TAKE_OUT |
| `request.data.method_expand.A_JSAPI.extend_params.hb_fq_num` | `request.data.method_expand` | `$.extend_params.hb_fq_num` | 花呗分期数 | `String` | `5` | `N` | 已确认 | 使用花呗分期要进行的分期数；示例值：3 |
| `request.data.method_expand.A_JSAPI.extend_params.hb_fq_seller_percent` | `request.data.method_expand` | `$.extend_params.hb_fq_seller_percent` | 花呗卖家手续费百分比 | `String` | `3` | `N` | 已确认 | 使用花呗分期需要卖家承担的手续费比，单位比例的百分值。； 花呗商贴支付默认传0，示例值：0 |
| `request.data.method_expand.A_JSAPI.extend_params.fq_channels` | `request.data.method_expand` | `$.extend_params.fq_channels` | 信用卡分期资产方式 | `String` | `20` | `N` | 已确认 | 代表优先使用资产类型；alipayfq_cc：表示信⽤卡分期，为空时默认花呗。示例值：alipayfq_cc |
| `request.data.method_expand.A_JSAPI.extend_params.parking_id` | `request.data.method_expand` | `$.extend_params.parking_id` | 停车场id | `String` | `28` | `N` | 已确认 | isv停车场id、向支付宝停车平台申请获得的支付宝停车场的唯一标识；示例值：PI[官网示例已脱敏] |
| `request.data.method_expand.A_JSAPI.extend_params.sys_service_provider_id` | `request.data.method_expand` | `$.extend_params.sys_service_provider_id` | 系统商编号 | `String` | `64` | `N` | 已确认 | 该参数作为系统商返佣数据提取的依据，请填写系统商签约协议的pid；示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_JSAPI.ali_promo_params` | `request.data.method_expand` | `$.ali_promo_params` | 优惠明细参数 | `String` | `—` | `N` | [需要官方确认]：长度 | 优惠明细参数，通过此属性补充营销参数。注：仅与支付宝协商后可用。；示例: "ali_promo_params": {"consumption_voucher":"shanghai_sanfang","uscc":"11111111"} |
| `request.data.method_expand.A_JSAPI.seller_id` | `request.data.method_expand` | `$.seller_id` | 卖家支付宝用户号 | `String` | `28` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_JSAPI.merchant_order_no` | `request.data.method_expand` | `$.merchant_order_no` | 商户原始订单号 | `String` | `32` | `N` | 已确认 | 示例值：39045032345 |
| `request.data.method_expand.A_JSAPI.operator_id` | `request.data.method_expand` | `$.operator_id` | 商户操作员编号 | `String` | `28` | `N` | 已确认 | 示例值：carl.li@huifu.com |
| `request.data.method_expand.A_JSAPI.product_code` | `request.data.method_expand` | `$.product_code` | 销售产品码 | `String` | `32` | `N` | 已确认 | 示例值：YYZY |
| `request.data.method_expand.A_JSAPI.ext_user_info` | `request.data.method_expand` | `$.ext_user_info` | 外部指定买家 | `Object` | `—` | `N` | N/A：结构字段长度 | 外部指定买家 |
| `request.data.method_expand.A_JSAPI.ext_user_info.name` | `request.data.method_expand` | `$.ext_user_info.name` | 姓名 | `String` | `16` | `N` | 已确认 | 注：need_check_info=T时，该参数才有效；示例值：张三 |
| `request.data.method_expand.A_JSAPI.ext_user_info.mobile` | `request.data.method_expand` | `$.ext_user_info.mobile` | 手机号 | `String` | `20` | `N` | 已确认 | 注：该参数暂不校验；示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_JSAPI.ext_user_info.cert_type` | `request.data.method_expand` | `$.ext_user_info.cert_type` | 证件类型 | `String` | `32` | `N` | 已确认 | 身份证：IDENTITY_CARD，；护照：PASSPORT；军官证：OFFICER_CARD，；士兵证：SOLDIER_CARD；户口本：HOKOU；示例值：IDENTITY_CARD；注：need_check_info=T时，该参数才有效 |
| `request.data.method_expand.A_JSAPI.ext_user_info.cert_no` | `request.data.method_expand` | `$.ext_user_info.cert_no` | 证件号 | `String` | `64` | `N` | 已确认 | 示例值：Ly+fnExeyPOTzfOtgRRur77nJB9TAe4PGgK9M ，；需要密文传输，请参考[加密解密说明](https://paas.huifu.com/open/doc/guide/#/api_jiami_jiemi)使用汇付RSA公钥加密。 ；注：need_check_info=T时，该参数才有效 |
| `request.data.method_expand.A_JSAPI.ext_user_info.min_age` | `request.data.method_expand` | `$.ext_user_info.min_age` | 允许的最小买家年龄 | `String` | `3` | `N` | 已确认 | 买家年龄必须大于等于所传数值。示例值：18 ；注：1\. need_check_info=T 时该参数才有效，2\. min_age 为整数，必须大于等于 0 |
| `request.data.method_expand.A_JSAPI.ext_user_info.fix_buyer` | `request.data.method_expand` | `$.ext_user_info.fix_buyer` | 是否强制校验付款人身份信息 | `String` | `8` | `N` | 已确认 | T：强制校验，F：不强制；示例值：T |
| `request.data.method_expand.A_JSAPI.ext_user_info.need_check_info` | `request.data.method_expand` | `$.ext_user_info.need_check_info` | 是否强制校验身份信息 | `String` | `1` | `N` | 已确认 | T：强制校验，F：不强制；示例值：F |
| `request.data.method_expand.A_JSAPI.subject` | `request.data.method_expand` | `$.subject` | 订单标题 | `String` | `256` | `N` | 已确认 | 直连模式必填；商品的标题/交易标题/订单标题/订单关键字等，是请求时对应的参数，原样通知回来；示例值：红果奶茶 |
| `request.data.method_expand.A_JSAPI.store_name` | `request.data.method_expand` | `$.store_name` | 商家门店名称 | `String` | `512` | `N` | 已确认 | 直连模式字段；示例值：红果奶茶上海宝山店 |
| `request.data.method_expand.A_JSAPI.op_app_id` | `request.data.method_expand` | `$.op_app_id` | 小程序应用的appid | `String` | `32` | `N` | 已确认 | 小程序支付中，商户实际经营主体的小程序应用的appid，也即最终唤起收银台支付所在的小程序的应用id；示例值：wxec280d4c8a1cc2ca |
| `request.data.method_expand.A_JSAPI.ali_business_params` | `request.data.method_expand` | `$.ali_business_params（String(JSON) 容器）` | 商户业务信息 | `String` | `512` | `N` | 已确认 | 商户传入业务信息，具体值要和支付宝约定将商户传入信息分发给相应系统，应用于安全，营销等参数直传场景，格式为JSONObject |
| `request.data.method_expand.A_JSAPI.body` | `request.data.method_expand` | `$.body` | 订单描述 | `String` | `128` | `N` | 已确认 | 示例值：IPhone \| \| ali_promo_params \| 优惠明细参数 \| String \| N \| 否 \| 优惠明细参数，通过此属性补充营销参数。注：仅与支付宝协商后可用。；示例: "ali_promo_params": {"consumption_voucher":"shanghai_sanfang","uscc":"11111111"} |
| `request.data.method_expand.A_NATIVE` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 支付宝正扫支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `request.data.method_expand.A_NATIVE.alipay_store_id` | `request.data.method_expand` | `$.alipay_store_id` | 支付宝的店铺编号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_NATIVE.buyer_id` | `request.data.method_expand` | `$.buyer_id` | 买家的支付宝唯一用户号 | `String` | `28` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_NATIVE.buyer_logon_id` | `request.data.method_expand` | `$.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com；交易类型为A_JSAPI时【买家支付宝账号】与【买家支付宝用户号】二选一必填 |
| `request.data.method_expand.A_NATIVE.goods_detail[]` | `request.data.method_expand` | `$.goods_detail[]` | 订单包含的商品列表信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 订单包含的商品列表信息 |
| `request.data.method_expand.A_NATIVE.goods_detail[].goods_id` | `request.data.method_expand` | `$.goods_detail[].goods_id` | 商品的编号 | `String` | `32` | `Y` | 已确认 | 示例值：apple-01 |
| `request.data.method_expand.A_NATIVE.goods_detail[].goods_name` | `request.data.method_expand` | `$.goods_detail[].goods_name` | 商品名称 | `String` | `256` | `Y` | 已确认 | 示例值：ipad |
| `request.data.method_expand.A_NATIVE.goods_detail[].price` | `request.data.method_expand` | `$.goods_detail[].price` | 商品单价(元) | `String` | `16` | `Y` | 已确认 | 单位：元；示例值：43.40 |
| `request.data.method_expand.A_NATIVE.goods_detail[].quantity` | `request.data.method_expand` | `$.goods_detail[].quantity` | 商品数量 | `String` | `10` | `Y` | 已确认 | 示例值：40 |
| `request.data.method_expand.A_NATIVE.goods_detail[].body` | `request.data.method_expand` | `$.goods_detail[].body` | 商品描述信息 | `String` | `1000` | `N` | 已确认 | 示例值：个人电脑 |
| `request.data.method_expand.A_NATIVE.goods_detail[].categories_tree` | `request.data.method_expand` | `$.goods_detail[].categories_tree` | 商品类目树 | `String` | `128` | `N` | 已确认 | 商品类目树，从商品类目根节点到叶子节点的类目 id 组成，类目 id 值使用\|分割；示例值：124868003\|126232002\|126252004 |
| `request.data.method_expand.A_NATIVE.goods_detail[].show_url` | `request.data.method_expand` | `$.goods_detail[].show_url` | 商品的展示地址 | `String` | `400` | `N` | 已确认 | 示例值：https://paas.huifu.com/checkout/demo/pc/goodsDetail.html |
| `request.data.method_expand.A_NATIVE.goods_detail[].goods_category` | `request.data.method_expand` | `$.goods_detail[].goods_category` | 商品类目 | `String` | `24` | `N` | 已确认 | 示例值：34543238 |
| `request.data.method_expand.A_NATIVE.extend_params` | `request.data.method_expand` | `$.extend_params` | 业务扩展参数 | `Object` | `—` | `N` | N/A：结构字段长度 | 业务扩展参数 |
| `request.data.method_expand.A_NATIVE.extend_params.card_type` | `request.data.method_expand` | `$.extend_params.card_type` | 卡类型 | `String` | `32` | `N` | 已确认 | 示例值：S0JP0000 |
| `request.data.method_expand.A_NATIVE.extend_params.food_order_type` | `request.data.method_expand` | `$.extend_params.food_order_type` | 支付宝点餐场景类型 | `String` | `20` | `N` | 已确认 | QR_ORDER（店内扫码点餐）；PRE_ORDER（预点到店自提）；HOME_DELIVERY（外送到家）；DIRECT_PAYMENT（直接付款）；QR_FOOD_ORDER（点餐先付）；P_QR_FOOD_ORDER（点餐后付）；SELF_PICK（门店自提）；TAKE_OUT （餐饮外卖）；OTHER（其他）；该参数只适用于支付宝支付窗交易接口；示例值：TAKE_OUT |
| `request.data.method_expand.A_NATIVE.extend_params.hb_fq_num` | `request.data.method_expand` | `$.extend_params.hb_fq_num` | 花呗分期数 | `String` | `5` | `N` | 已确认 | 使用花呗分期要进行的分期数；示例值：3 |
| `request.data.method_expand.A_NATIVE.extend_params.hb_fq_seller_percent` | `request.data.method_expand` | `$.extend_params.hb_fq_seller_percent` | 花呗卖家手续费百分比 | `String` | `3` | `N` | 已确认 | 使用花呗分期需要卖家承担的手续费比，单位比例的百分值。； 花呗商贴支付默认传0，示例值：0 |
| `request.data.method_expand.A_NATIVE.extend_params.fq_channels` | `request.data.method_expand` | `$.extend_params.fq_channels` | 信用卡分期资产方式 | `String` | `20` | `N` | 已确认 | 代表优先使用资产类型；alipayfq_cc：表示信⽤卡分期，为空时默认花呗。示例值：alipayfq_cc |
| `request.data.method_expand.A_NATIVE.extend_params.parking_id` | `request.data.method_expand` | `$.extend_params.parking_id` | 停车场id | `String` | `28` | `N` | 已确认 | isv停车场id、向支付宝停车平台申请获得的支付宝停车场的唯一标识；示例值：PI[官网示例已脱敏] |
| `request.data.method_expand.A_NATIVE.extend_params.sys_service_provider_id` | `request.data.method_expand` | `$.extend_params.sys_service_provider_id` | 系统商编号 | `String` | `64` | `N` | 已确认 | 该参数作为系统商返佣数据提取的依据，请填写系统商签约协议的pid；示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_NATIVE.ali_promo_params` | `request.data.method_expand` | `$.ali_promo_params` | 优惠明细参数 | `String` | `—` | `N` | [需要官方确认]：长度 | 优惠明细参数，通过此属性补充营销参数。注：仅与支付宝协商后可用。；示例: "ali_promo_params": {"consumption_voucher":"shanghai_sanfang","uscc":"11111111"} |
| `request.data.method_expand.A_NATIVE.seller_id` | `request.data.method_expand` | `$.seller_id` | 卖家支付宝用户号 | `String` | `28` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_NATIVE.merchant_order_no` | `request.data.method_expand` | `$.merchant_order_no` | 商户原始订单号 | `String` | `32` | `N` | 已确认 | 示例值：39045032345 |
| `request.data.method_expand.A_NATIVE.operator_id` | `request.data.method_expand` | `$.operator_id` | 商户操作员编号 | `String` | `28` | `N` | 已确认 | 示例值：carl.li@huifu.com |
| `request.data.method_expand.A_NATIVE.product_code` | `request.data.method_expand` | `$.product_code` | 销售产品码 | `String` | `32` | `N` | 已确认 | 示例值：YYZY |
| `request.data.method_expand.A_NATIVE.ext_user_info` | `request.data.method_expand` | `$.ext_user_info` | 外部指定买家 | `Object` | `—` | `N` | N/A：结构字段长度 | 外部指定买家 |
| `request.data.method_expand.A_NATIVE.ext_user_info.name` | `request.data.method_expand` | `$.ext_user_info.name` | 姓名 | `String` | `16` | `N` | 已确认 | 注：need_check_info=T时，该参数才有效；示例值：张三 |
| `request.data.method_expand.A_NATIVE.ext_user_info.mobile` | `request.data.method_expand` | `$.ext_user_info.mobile` | 手机号 | `String` | `20` | `N` | 已确认 | 注：该参数暂不校验；示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_NATIVE.ext_user_info.cert_type` | `request.data.method_expand` | `$.ext_user_info.cert_type` | 证件类型 | `String` | `32` | `N` | 已确认 | 身份证：IDENTITY_CARD，；护照：PASSPORT；军官证：OFFICER_CARD，；士兵证：SOLDIER_CARD；户口本：HOKOU；示例值：IDENTITY_CARD；注：need_check_info=T时，该参数才有效 |
| `request.data.method_expand.A_NATIVE.ext_user_info.cert_no` | `request.data.method_expand` | `$.ext_user_info.cert_no` | 证件号 | `String` | `64` | `N` | 已确认 | 示例值：Ly+fnExeyPOTzfOtgRRur77nJB9TAe4PGgK9M ，；需要密文传输，请参考[加密解密说明](https://paas.huifu.com/open/doc/guide/#/api_jiami_jiemi)使用汇付RSA公钥加密。 ；注：need_check_info=T时，该参数才有效 |
| `request.data.method_expand.A_NATIVE.ext_user_info.min_age` | `request.data.method_expand` | `$.ext_user_info.min_age` | 允许的最小买家年龄 | `String` | `3` | `N` | 已确认 | 买家年龄必须大于等于所传数值。示例值：18 ；注：1\. need_check_info=T 时该参数才有效，2\. min_age 为整数，必须大于等于 0 |
| `request.data.method_expand.A_NATIVE.ext_user_info.fix_buyer` | `request.data.method_expand` | `$.ext_user_info.fix_buyer` | 是否强制校验付款人身份信息 | `String` | `8` | `N` | 已确认 | T：强制校验，F：不强制；示例值：T |
| `request.data.method_expand.A_NATIVE.ext_user_info.need_check_info` | `request.data.method_expand` | `$.ext_user_info.need_check_info` | 是否强制校验身份信息 | `String` | `1` | `N` | 已确认 | T：强制校验，F：不强制；示例值：F |
| `request.data.method_expand.A_NATIVE.subject` | `request.data.method_expand` | `$.subject` | 订单标题 | `String` | `256` | `N` | 已确认 | 直连模式必填；商品的标题/交易标题/订单标题/订单关键字等，是请求时对应的参数，原样通知回来；示例值：红果奶茶 |
| `request.data.method_expand.A_NATIVE.store_name` | `request.data.method_expand` | `$.store_name` | 商家门店名称 | `String` | `512` | `N` | 已确认 | 直连模式字段；示例值：红果奶茶上海宝山店 |
| `request.data.method_expand.A_NATIVE.op_app_id` | `request.data.method_expand` | `$.op_app_id` | 小程序应用的appid | `String` | `32` | `N` | 已确认 | 小程序支付中，商户实际经营主体的小程序应用的appid，也即最终唤起收银台支付所在的小程序的应用id；示例值：wxec280d4c8a1cc2ca |
| `request.data.method_expand.A_NATIVE.ali_business_params` | `request.data.method_expand` | `$.ali_business_params（String(JSON) 容器）` | 商户业务信息 | `String` | `512` | `N` | 已确认 | 商户传入业务信息，具体值要和支付宝约定将商户传入信息分发给相应系统，应用于安全，营销等参数直传场景，格式为JSONObject |
| `request.data.method_expand.A_NATIVE.body` | `request.data.method_expand` | `$.body` | 订单描述 | `String` | `128` | `N` | 已确认 | 示例值：IPhone \| \| ali_promo_params \| 优惠明细参数 \| String \| N \| 否 \| 优惠明细参数，通过此属性补充营销参数。注：仅与支付宝协商后可用。；示例: "ali_promo_params": {"consumption_voucher":"shanghai_sanfang","uscc":"11111111"} |
| `request.data.method_expand.A_MICROPAY` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 支付宝反扫参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `request.data.method_expand.A_MICROPAY.auth_code` | `request.data.method_expand` | `$.auth_code` | 支付授权码 | `String` | `128` | `Y` | 已确认 | 扫码设备读出的条形码或者二维码信息；示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_MICROPAY.alipay_store_id` | `request.data.method_expand` | `$.alipay_store_id` | 支付宝的店铺编号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_MICROPAY.goods_detail[]` | `request.data.method_expand` | `$.goods_detail[]` | 订单包含的商品列表信息 | `Array` | `2048` | `N` | 已确认 | 订单包含的商品列表信息 |
| `request.data.method_expand.A_MICROPAY.goods_detail[].goods_id` | `request.data.method_expand` | `$.goods_detail[].goods_id` | 商品的编号 | `String` | `32` | `Y` | 已确认 | 示例值：apple-01 |
| `request.data.method_expand.A_MICROPAY.goods_detail[].goods_name` | `request.data.method_expand` | `$.goods_detail[].goods_name` | 商品名称 | `String` | `256` | `Y` | 已确认 | 示例值：ipad |
| `request.data.method_expand.A_MICROPAY.goods_detail[].price` | `request.data.method_expand` | `$.goods_detail[].price` | 商品单价(元) | `String` | `16` | `Y` | 已确认 | 单位：元；示例值：43.40 |
| `request.data.method_expand.A_MICROPAY.goods_detail[].quantity` | `request.data.method_expand` | `$.goods_detail[].quantity` | 商品数量 | `String` | `10` | `Y` | 已确认 | 示例值：40 |
| `request.data.method_expand.A_MICROPAY.goods_detail[].body` | `request.data.method_expand` | `$.goods_detail[].body` | 商品描述信息 | `String` | `1000` | `N` | 已确认 | 示例值：个人电脑 |
| `request.data.method_expand.A_MICROPAY.goods_detail[].categories_tree` | `request.data.method_expand` | `$.goods_detail[].categories_tree` | 商品类目树 | `String` | `128` | `N` | 已确认 | 商品类目树，从商品类目根节点到叶子节点的类目 id 组成，类目 id 值使用\|分割；示例值：124868003\|126232002\|126252004 |
| `request.data.method_expand.A_MICROPAY.goods_detail[].goods_category` | `request.data.method_expand` | `$.goods_detail[].goods_category` | 商品类目 | `String` | `24` | `N` | 已确认 | 示例值：34543238 |
| `request.data.method_expand.A_MICROPAY.goods_detail[].show_url` | `request.data.method_expand` | `$.goods_detail[].show_url` | 商品的展示地址 | `String` | `400` | `N` | 已确认 | 示例值：https://paas.huifu.com/checkout/demo/pc/goodsDetail.html |
| `request.data.method_expand.A_MICROPAY.extend_params` | `request.data.method_expand` | `$.extend_params` | 业务扩展参数 | `Object` | `2048` | `N` | 已确认 | 业务扩展参数 |
| `request.data.method_expand.A_MICROPAY.extend_params.card_type` | `request.data.method_expand` | `$.extend_params.card_type` | 卡类型 | `String` | `32` | `N` | 已确认 | 示例值：S0JP0000 |
| `request.data.method_expand.A_MICROPAY.extend_params.food_order_type` | `request.data.method_expand` | `$.extend_params.food_order_type` | 支付宝点餐场景类型 | `String` | `20` | `N` | 已确认 | QR_ORDER（店内扫码点餐）；PRE_ORDER（预点到店自提）；HOME_DELIVERY（外送到家）；DIRECT_PAYMENT（直接付款）；QR_FOOD_ORDER（点餐先付）；P_QR_FOOD_ORDER（点餐后付）；SELF_PICK（门店自提）；TAKE_OUT （餐饮外卖）；OTHER（其他）；该参数只适用于支付宝支付窗交易接口；示例值：QR_ORDER |
| `request.data.method_expand.A_MICROPAY.extend_params.hb_fq_num` | `request.data.method_expand` | `$.extend_params.hb_fq_num` | 花呗分期数 | `String` | `5` | `N` | 已确认 | 使用花呗分期要进行的分期数；示例值：3 |
| `request.data.method_expand.A_MICROPAY.extend_params.hb_fq_seller_percent` | `request.data.method_expand` | `$.extend_params.hb_fq_seller_percent` | 花呗卖家承担的手续费百分比 | `String` | `3` | `N` | 已确认 | 使用花呗分期需要卖家承担的手续费比，默认0；数据格式:比例的百分值，示例值：9，传入100代表100% |
| `request.data.method_expand.A_MICROPAY.extend_params.industry_reflux_info` | `request.data.method_expand` | `$.extend_params.industry_reflux_info` | 行业数据回流信息 | `String` | `512` | `N` | 已确认 | 示例值：{\"scene_code\":\"metro_tradeorder\",\"channel\":\"xxxx\",\"scene_data\":{\"asset_name\":\"ALIPAY\"}} |
| `request.data.method_expand.A_MICROPAY.extend_params.parking_id` | `request.data.method_expand` | `$.extend_params.parking_id` | 停车场id | `String` | `28` | `N` | 已确认 | isv停车场id、向支付宝停车平台申请获得的支付宝停车场的唯一标识；示例值：PI[官网示例已脱敏] |
| `request.data.method_expand.A_MICROPAY.extend_params.sys_service_provider_id` | `request.data.method_expand` | `$.extend_params.sys_service_provider_id` | 系统商编号 | `String` | `64` | `N` | 已确认 | 该参数作为系统商返佣数据提取的依据，请填写系统商签约协议的pid；示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_MICROPAY.ali_business_params` | `request.data.method_expand` | `$.ali_business_params（String(JSON) 容器）` | 商户业务信息 | `String` | `512` | `N` | 已确认 | 商户传入业务信息，具体值要和支付宝约定将商户传入信息分发给相应系统，应用于安全，营销等参数直传场景，格式为JSONObject |
| `request.data.method_expand.A_MICROPAY.operator_id` | `request.data.method_expand` | `$.operator_id` | 商户操作员编号 | `String` | `28` | `N` | 已确认 | 示例值：carl.li@huifu.com |
| `request.data.method_expand.A_MICROPAY.store_id` | `request.data.method_expand` | `$.store_id` | 商户门店编号 | `String` | `32` | `N` | 已确认 | 示例值：sh1001 |
| `request.data.method_expand.A_MICROPAY.ext_user_info` | `request.data.method_expand` | `$.ext_user_info` | 外部指定买家 | `Object` | `—` | `N` | N/A：结构字段长度 | — |
| `request.data.method_expand.A_MICROPAY.ext_user_info.name` | `request.data.method_expand` | `$.ext_user_info.name` | 姓名 | `String` | `16` | `N` | 已确认 | 注：need_check_info=T时，该参数才有效；示例值：张三 |
| `request.data.method_expand.A_MICROPAY.ext_user_info.mobile` | `request.data.method_expand` | `$.ext_user_info.mobile` | 手机号 | `String` | `20` | `N` | 已确认 | 注：该参数暂不校验；示例值：[官网示例已脱敏] |
| `request.data.method_expand.A_MICROPAY.ext_user_info.cert_type` | `request.data.method_expand` | `$.ext_user_info.cert_type` | 证件类型 | `String` | `32` | `N` | 已确认 | 身份证：IDENTITY_CARD，；护照：PASSPORT；军官证：OFFICER_CARD，；士兵证：SOLDIER_CARD；户口本：HOKOU；示例值：IDENTITY_CARD；注：need_check_info=T时，该参数才有效 |
| `request.data.method_expand.A_MICROPAY.ext_user_info.cert_no` | `request.data.method_expand` | `$.ext_user_info.cert_no` | 证件号 | `String` | `64` | `N` | 已确认 | 示例值：Ly+fnExeyPOTzfOtgRRur77nJB9TAe4PGgK9M；需要密文传输，请参考[加密解密说明](https://paas.huifu.com/open/doc/guide/#/api_jiami_jiemi)使用汇付RSA公钥加密。 ；注：need_check_info=T时，该参数才有效 |
| `request.data.method_expand.A_MICROPAY.ext_user_info.min_age` | `request.data.method_expand` | `$.ext_user_info.min_age` | 允许的最小买家年龄 | `String` | `3` | `N` | 已确认 | 买家年龄必须大于等于所传数值。示例值：18 ；注：1\. need_check_info=T 时该参数才有效;；2\. min_age 为整数，必须大于等于 0 |
| `request.data.method_expand.A_MICROPAY.ext_user_info.fix_buyer` | `request.data.method_expand` | `$.ext_user_info.fix_buyer` | 是否强制校验付款人身份信息 | `String` | `8` | `N` | 已确认 | T：强制校验，F：不强制；示例值：T |
| `request.data.method_expand.A_MICROPAY.ext_user_info.need_check_info` | `request.data.method_expand` | `$.ext_user_info.need_check_info` | 是否强制校验身份信息 | `String` | `1` | `N` | 已确认 | T：强制校验，F：不强制；示例值：F |
| `request.data.method_expand.A_MICROPAY.body` | `request.data.method_expand` | `$.body` | 订单描述 | `String` | `128` | `N` | 已确认 | 示例值：IPhone |
| `request.data.method_expand.A_MICROPAY.ali_promo_params` | `request.data.method_expand` | `$.ali_promo_params` | 优惠明细参数 | `String` | `—` | `N` | [需要官方确认]：长度 | 优惠明细参数，通过此属性补充营销参数。注：仅与支付宝协商后可用。；示例: "ali_promo_params": {"consumption_voucher":"shanghai_sanfang","uscc":"11111111"} |
| `request.data.method_expand.U_JSAPI` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 银联JS支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `request.data.method_expand.U_JSAPI.qr_code` | `request.data.method_expand` | `$.qr_code` | 二维码 | `String` | `256` | `N` | 已确认 | 台牌码的url，交易类型为U_JSAPI:银联JS时必填 |
| `request.data.method_expand.U_JSAPI.addn_data` | `request.data.method_expand` | `$.addn_data` | 收款方附加数据 | `String` | `3000` | `N` | 已确认 | 请参考[银联收款方附加数据(addn_data)说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylcsjh#银联收款方附加数据(addn_data)) |
| `request.data.method_expand.U_JSAPI.customer_ip` | `request.data.method_expand` | `$.customer_ip` | 持卡人ip | `String` | `40` | `N` | 已确认 | 持卡人确认付款时的ip地址，用于防钓鱼。（js支付必填）示例值：127.1.1.1 |
| `request.data.method_expand.U_JSAPI.front_url` | `request.data.method_expand` | `$.front_url` | 前台通知地址 | `String` | `200` | `N` | 已确认 | 收款方向银联推送订单时上送的前台通知地址（仅允许为外网地址）；用户完成支付点击“返回”后，银联通过浏览器post请求到该地址。；示例值：http://www.huifu.com |
| `request.data.method_expand.U_JSAPI.order_desc` | `request.data.method_expand` | `$.order_desc` | 订单描述 | `String` | `200` | `N` | 已确认 | 示例值：订单描述 |
| `request.data.method_expand.U_JSAPI.payee_comments` | `request.data.method_expand` | `$.payee_comments` | 收款方附言 | `String` | `100` | `N` | 已确认 | 示例值：业务收款 |
| `request.data.method_expand.U_JSAPI.payee_info` | `request.data.method_expand` | `$.payee_info` | 收款方信息 | `Object` | `—` | `N` | N/A：结构字段长度 | — |
| `request.data.method_expand.U_JSAPI.payee_info.mer_cat_code` | `request.data.method_expand` | `$.payee_info.mer_cat_code` | 商户类别 | `String` | `4` | `N` | 已确认 | [参考银联商户类别](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylshlb)；示例值：0101 |
| `request.data.method_expand.U_JSAPI.payee_info.sub_id` | `request.data.method_expand` | `$.payee_info.sub_id` | 二级商户代码 | `String` | `20` | `N` | 已确认 | 示例值：823586070110039 |
| `request.data.method_expand.U_JSAPI.payee_info.sub_name` | `request.data.method_expand` | `$.payee_info.sub_name` | 二级商户名称 | `String` | `100` | `N` | 已确认 | 示例值：上海白乐门酒店 |
| `request.data.method_expand.U_JSAPI.payee_info.term_id` | `request.data.method_expand` | `$.payee_info.term_id` | 终端号 | `String` | `8` | `N` | 已确认 | 示例值：58000001 |
| `request.data.method_expand.U_JSAPI.req_reserved` | `request.data.method_expand` | `$.req_reserved` | 请求方自定义域 | `String` | `500` | `N` | 已确认 | 示例值： |
| `request.data.method_expand.U_JSAPI.user_id` | `request.data.method_expand` | `$.user_id` | 银联用户标识 | `String` | `128` | `N` | 已确认 | 调用[获取银联用户标识接口](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_unionauth)会返回【user_id】；示例值：gaqiMrRnKwwOZO7dNtUc349YTMaa3HkRZg+OMU+46ysDzn6flfomHP88qOvH+6yG |
| `request.data.method_expand.U_NATIVE` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 银联正扫支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `request.data.method_expand.U_NATIVE.qr_code` | `request.data.method_expand` | `$.qr_code` | 二维码 | `String` | `256` | `N` | 已确认 | 台牌码的url，交易类型为U_JSAPI:银联JS时必填 |
| `request.data.method_expand.U_NATIVE.addn_data` | `request.data.method_expand` | `$.addn_data` | 收款方附加数据 | `String` | `3000` | `N` | 已确认 | 请参考[银联收款方附加数据(addn_data)说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylcsjh#银联收款方附加数据(addn_data)) |
| `request.data.method_expand.U_NATIVE.customer_ip` | `request.data.method_expand` | `$.customer_ip` | 持卡人ip | `String` | `40` | `N` | 已确认 | 持卡人确认付款时的ip地址，用于防钓鱼。（js支付必填）示例值：127.1.1.1 |
| `request.data.method_expand.U_NATIVE.front_url` | `request.data.method_expand` | `$.front_url` | 前台通知地址 | `String` | `200` | `N` | 已确认 | 收款方向银联推送订单时上送的前台通知地址（仅允许为外网地址）；用户完成支付点击“返回”后，银联通过浏览器post请求到该地址。；示例值：http://www.huifu.com |
| `request.data.method_expand.U_NATIVE.order_desc` | `request.data.method_expand` | `$.order_desc` | 订单描述 | `String` | `200` | `N` | 已确认 | 示例值：订单描述 |
| `request.data.method_expand.U_NATIVE.payee_comments` | `request.data.method_expand` | `$.payee_comments` | 收款方附言 | `String` | `100` | `N` | 已确认 | 示例值：业务收款 |
| `request.data.method_expand.U_NATIVE.payee_info` | `request.data.method_expand` | `$.payee_info` | 收款方信息 | `Object` | `—` | `N` | N/A：结构字段长度 | — |
| `request.data.method_expand.U_NATIVE.payee_info.mer_cat_code` | `request.data.method_expand` | `$.payee_info.mer_cat_code` | 商户类别 | `String` | `4` | `N` | 已确认 | [参考银联商户类别](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylshlb)；示例值：0101 |
| `request.data.method_expand.U_NATIVE.payee_info.sub_id` | `request.data.method_expand` | `$.payee_info.sub_id` | 二级商户代码 | `String` | `20` | `N` | 已确认 | 示例值：823586070110039 |
| `request.data.method_expand.U_NATIVE.payee_info.sub_name` | `request.data.method_expand` | `$.payee_info.sub_name` | 二级商户名称 | `String` | `100` | `N` | 已确认 | 示例值：上海白乐门酒店 |
| `request.data.method_expand.U_NATIVE.payee_info.term_id` | `request.data.method_expand` | `$.payee_info.term_id` | 终端号 | `String` | `8` | `N` | 已确认 | 示例值：58000001 |
| `request.data.method_expand.U_NATIVE.req_reserved` | `request.data.method_expand` | `$.req_reserved` | 请求方自定义域 | `String` | `500` | `N` | 已确认 | 示例值： |
| `request.data.method_expand.U_NATIVE.user_id` | `request.data.method_expand` | `$.user_id` | 银联用户标识 | `String` | `128` | `N` | 已确认 | 调用[获取银联用户标识接口](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_unionauth)会返回【user_id】；示例值：gaqiMrRnKwwOZO7dNtUc349YTMaa3HkRZg+OMU+46ysDzn6flfomHP88qOvH+6yG |
| `request.data.method_expand.U_MICROPAY` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 银联反扫支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `request.data.method_expand.U_MICROPAY.auth_code` | `request.data.method_expand` | `$.auth_code` | 支付授权码 | `String` | `128` | `N` | 已确认 | 扫码设备读出的条形码或者二维码信息；示例值：[官网示例已脱敏] |
| `request.data.method_expand.U_MICROPAY.currency_code` | `request.data.method_expand` | `$.currency_code` | 币种 | `String` | `3` | `N` | 已确认 | 156代表人民币；示例值：156 |
| `request.data.method_expand.U_MICROPAY.invoice_st` | `request.data.method_expand` | `$.invoice_st` | 支持发票 | `String` | `1` | `N` | 已确认 | 0：表示不支持根据银行返回信息打印发票；此为缺省状态。；1：表示可以根据银行返回信息打印发票；示例值：1 |
| `request.data.method_expand.U_MICROPAY.mer_cat_code` | `request.data.method_expand` | `$.mer_cat_code` | 商户类别 | `String` | `4` | `N` | 已确认 | 商户类别；示例值： |
| `request.data.method_expand.U_MICROPAY.pnr_ins_id_cd` | `request.data.method_expand` | `$.pnr_ins_id_cd` | 服务商机构标识码 | `String` | `11` | `N` | 已确认 | 银联分配的服务商机构标识码；示例值：01008330 |
| `request.data.method_expand.U_MICROPAY.specfeeinfo` | `request.data.method_expand` | `$.specfeeinfo` | 特殊计费信息 | `String` | `3` | `N` | 已确认 | 特殊计费信息；示例值： |
| `request.data.method_expand.U_MICROPAY.term_id` | `request.data.method_expand` | `$.term_id` | 终端号 | `String` | `8` | `N` | 已确认 | 终端号；示例值：58000001 |
| `request.data.method_expand.U_MICROPAY.addn_data` | `request.data.method_expand` | `$.addn_data` | 收款方附加数据 | `String` | `3000` | `N` | 已确认 | 请参考[银联收款方附加数据(addn_data)说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylcsjh#银联收款方附加数据(addn_data)) |
| `request.data.method_expand.U_MICROPAY.pid_info` | `request.data.method_expand` | `$.pid_info` | 服务商信息 | `Object` | `—` | `N` | N/A：结构字段长度 | — |
| `request.data.method_expand.U_MICROPAY.pid_info.pnr_order_id` | `request.data.method_expand` | `$.pid_info.pnr_order_id` | 服务商订单编号 | `String` | `40` | `N` | 已确认 | 服务商自定义并发送，同一交易日期内不可重复，订单编号将作为服务商和银联对账的唯一索引，不超过40字节的变长字母和/或数字字符，不能含“-”或“_” |
| `request.data.method_expand.U_MICROPAY.pid_info.pid_sct` | `request.data.method_expand` | `$.pid_info.pid_sct` | 服务商密文 | `String` | `8` | `N` | 已确认 | 由服务商根据服务商代码标识加密算法生成 |
| `request.data.method_expand.U_MICROPAY.pid_info.trade_scene` | `request.data.method_expand` | `$.pid_info.trade_scene` | 场景标识 | `String` | `8` | `N` | 已确认 | 取值如下:1-扫码点餐示例值：1 |
| `request.data.tx_metadata` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 扩展参数集合 | `String` | `—` | `C` | [需要官方确认]：长度 | jsonObject字符串，交易能力扩展，tx_metadata只是方便文档展示，实际请求时不需要传入，传入下面的子项即可 |
| `request.data.tx_metadata.acct_split_bunch` | `request.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `request.data.tx_metadata.acct_split_bunch.acct_infos[]` | `request.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `—` | `N` | N/A：结构字段长度 | jsonArray分账明细 |
| `request.data.tx_metadata.acct_split_bunch.acct_infos[].div_amt` | `request.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 ，最低传入0.01 |
| `request.data.tx_metadata.acct_split_bunch.acct_infos[].huifu_id` | `request.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `request.data.tx_metadata.acct_split_bunch.acct_infos[].acct_id` | `request.data.acct_split_bunch` | `$.acct_infos[].acct_id` | 账户号 | `String` | `9` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户；示例值：F00598600 |
| `request.data.tx_metadata.acct_split_bunch.acct_infos[].percentage_div` | `request.data.acct_split_bunch` | `$.acct_infos[].percentage_div` | 分账百分比% | `String` | `6` | `N` | 已确认 | 示例值：23.50，表示23.50%。仅在percentage_flag=Y时起作用； acct_infos中全部分账百分比之和必须为100.00%。 |
| `request.data.tx_metadata.acct_split_bunch.percentage_flag` | `request.data.acct_split_bunch` | `$.percentage_flag` | 百分比分账标志 | `String` | `1` | `N` | 已确认 | Y:使用百分比分账；示例值：Y |
| `request.data.tx_metadata.acct_split_bunch.is_clean_split` | `request.data.acct_split_bunch` | `$.is_clean_split` | 是否净值分账 | `String` | `1` | `N` | 已确认 | Y:使用净值分账，仅在交易手续费内扣且使用百分比分账时起作用；示例值：Y |
| `request.data.tx_metadata.terminal_device_data` | `request.data.terminal_device_data` | `—（String(JSON) 容器）` | 设备信息 | `String` | `—` | `C` | [需要官方确认]：长度 | 设备信息；反扫支付时必填 |
| `request.data.tx_metadata.terminal_device_data.device_ip` | `request.data.terminal_device_data` | `$.device_ip` | 交易设备IP | `String` | `16` | `N` | 已确认 | 绑卡设备所在的公网IP，可用于定位所属地区，不是wifi连接时的局域网IP。；示例值：10.10.0.1（IPv4）；ABCD:EF01:2345:6789:ABCD:EF01:2345:6789（IPv6）； 目前暂传IPv4格式。（反扫交易必填） |
| `request.data.tx_metadata.terminal_device_data.device_mac` | `request.data.terminal_device_data` | `$.device_mac` | 交易设备MAC | `String` | `64` | `N` | 已确认 | 示例值：F0E1D2C3B4A5 |
| `request.data.tx_metadata.terminal_device_data.device_imei` | `request.data.terminal_device_data` | `$.device_imei` | 交易设备IMEI | `String` | `64` | `N` | 已确认 | 移动终端设备的唯一标识；示例值：460030912121001 |
| `request.data.tx_metadata.terminal_device_data.device_imsi` | `request.data.terminal_device_data` | `$.device_imsi` | 交易设备IMSI | `String` | `64` | `N` | 已确认 | 示例值：460030912121001 |
| `request.data.tx_metadata.terminal_device_data.device_icc_id` | `request.data.terminal_device_data` | `$.device_icc_id` | 交易设备ICCID | `String` | `64` | `N` | 已确认 | 示例值：898600680113F0123014 |
| `request.data.tx_metadata.terminal_device_data.device_wifi_mac` | `request.data.terminal_device_data` | `$.device_wifi_mac` | 交易设备WIFIMAC | `String` | `64` | `N` | 已确认 | 示例值：968778695A4B |
| `request.data.tx_metadata.terminal_device_data.device_gps` | `request.data.terminal_device_data` | `$.device_gps` | 交易设备GPS | `String` | `64` | `N` | 已确认 | 示例值：20.346790,-4.654321 |
| `request.data.tx_metadata.terminal_device_data.app_version` | `request.data.terminal_device_data` | `$.app_version` | 商户终端应用程序版 | `String` | `8` | `N` | 已确认 | 终端应用程序的版本号。应用程序变更应保证版本号不重复；示例值：3.2.5 |
| `request.data.tx_metadata.terminal_device_data.encrypt_rand_num` | `request.data.terminal_device_data` | `$.encrypt_rand_num` | 加密随机因子 | `String` | `10` | `N` | 已确认 | 参见[《加密随机因子说明》](https://paas.huifu.com/open/doc/api/#/smzf/api_jmsjyzsm)；仅在被扫支付类交易报文中出现：；若付款码为19位数字，则取后6位；若付款码为EMV二维码，则取其tag57的卡号/token号的后6位；示例值：127026 |
| `request.data.tx_metadata.terminal_device_data.icc_id` | `request.data.terminal_device_data` | `$.icc_id` | SIM 卡卡号 | `String` | `20` | `N` | 已确认 | ICCID，SIM 卡卡号；示例值：898600680113F0123014 |
| `request.data.tx_metadata.terminal_device_data.location` | `request.data.terminal_device_data` | `$.location` | 商户终端实时经纬度信息 | `String` | `32` | `N` | 已确认 | 受理终端设备实时经纬度信息，银联云闪付交易必填；格式为纬度/经度，+表示北纬、东经，-表示南纬、西经。示例值：+37.12/-121.213；经度整数位不超过3位，小数位不超过5位；纬度整数位不超过2位，小数位不超过6位。；注：银联AT交易时，location和mer_device_IP二选一必填其一 |
| `request.data.tx_metadata.terminal_device_data.mer_device_ip` | `request.data.terminal_device_data` | `$.mer_device_ip` | 商户交易设备IP | `String` | `64` | `N` | 已确认 | 示例值：10.10.0.1；注：银联AT交易时，location和mer_device_IP二选一必填其一 |
| `request.data.tx_metadata.terminal_device_data.mer_device_type` | `request.data.terminal_device_data` | `$.mer_device_type` | 商户设备类型 | `String` | `2` | `N` | 已确认 | 01：自动柜员机（含ATM和CDM）和多媒体自助终端，02：传统POS，03：mPOS，；04：智能 POS，05：II 型固定电话，06：云闪付终端，；08：手机POS，09：刷脸付终端，10：条码支付受理终端，；11：条码支付辅助受理终端（如：台牌码），；12：行业终端（公交、地铁用于指 定行业的终端），13：MIS 终端；示例值：11 |
| `request.data.tx_metadata.terminal_device_data.mobile_country_cd` | `request.data.terminal_device_data` | `$.mobile_country_cd` | 移动国家代码 | `String` | `3` | `N` | 已确认 | 基站信息，由国际电联(ITU)统一分配的移动国家代码（MCC），中国为 460（默认）；示例值：460 |
| `request.data.tx_metadata.terminal_device_data.mobile_net_num` | `request.data.terminal_device_data` | `$.mobile_net_num` | 移动网络号码 | `String` | `2` | `N` | 已确认 | 由国际电联(ITU)统一分配的移动网络号码（MNC）。；移动：00、02、04、07； 联通：01、06、09； 电信：03、05、11；示例值：00 |
| `request.data.tx_metadata.terminal_device_data.network_license` | `request.data.terminal_device_data` | `$.network_license` | 商户终端入网认证编号 | `String` | `5` | `N` | 已确认 | 银行卡受理终端产品入网认证编号。格式：5 位字符，示例值：P3100；该编号由“中国银联标识产品企业资质认证办公室”为通过入网认证的终端进行分配 |
| `request.data.tx_metadata.terminal_device_data.secret_text` | `request.data.terminal_device_data` | `$.secret_text` | 密文数据 | `String` | `16` | `N` | 已确认 | 仅在被扫支付类交易报文中出现：64bit的密文数据，对终端硬件序列号和加密随机因子加密后的结果。；本子域取值为：64bit密文数据进行base64编码后的结果。反扫辅助类设备可以为空；示例值：MkQ2MTVEQkY=\n |
| `request.data.tx_metadata.terminal_device_data.serial_num` | `request.data.terminal_device_data` | `$.serial_num` | 商户终端序列号 | `String` | `50` | `N` | 已确认 | 终端设备的硬件序列号；示例值：00000304N7NL01933217 |
| `request.data.tx_metadata.terminal_device_data.devs_id` | `request.data.terminal_device_data` | `$.devs_id` | 汇付机具号 | `String` | `32` | `N` | 已确认 | 通过汇付报备的机具必传；示例值：SP003pcf；参见[新增终端报备](https://paas.huifu.com/open/doc/api/#/zdgl/api_zdbb_xzzd)或[商户终端信息查询](https://paas.huifu.com/open/doc/api/#/zdgl/api_zdbb_bdzdxxcx)接口的返参device_id |
| `request.data.tx_metadata.combinedpay_data[]` | `request.data.combinedpay_data` | `—（String(JSON Array) 容器）` | 补贴支付信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray字符串，参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| `request.data.tx_metadata.combinedpay_data[].huifu_id` | `request.data.combinedpay_data` | `$[].huifu_id` | 补贴方汇付商户号 | `String` | `32` | `N` | 已确认 | 补贴方汇付ID；示例值：[官网示例已脱敏] |
| `request.data.tx_metadata.combinedpay_data[].user_type` | `request.data.combinedpay_data` | `$[].user_type` | 补贴方类型 | `String` | `32` | `N` | 已确认 | channel-渠道，merchant-总部商户，agent-代理，mertomer-商户；示例值：channel |
| `request.data.tx_metadata.combinedpay_data[].acct_id` | `request.data.combinedpay_data` | `$[].acct_id` | 补贴方账户号 | `String` | `32` | `N` | 已确认 | 营销补贴方账户号；示例值：F00900982 |
| `request.data.tx_metadata.combinedpay_data[].amount` | `request.data.combinedpay_data` | `$[].amount` | 补贴金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； 示例值：1.01 |
| `request.data.tx_metadata.combinedpay_data_fee_info` | `request.data.combinedpay_data_fee_info` | `—（String(JSON) 容器）` | 补贴支付手续费承担方信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `request.data.tx_metadata.combinedpay_data_fee_info.huifu_id` | `request.data.combinedpay_data_fee_info` | `$.huifu_id` | 补贴支付手续费承担方汇付编号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.tx_metadata.combinedpay_data_fee_info.acct_id` | `request.data.combinedpay_data_fee_info` | `$.acct_id` | 补贴支付手续费承担方账户号 | `String` | `32` | `N` | 已确认 | 补贴支付手续费承担方账户号；示例值：F00598610 |
| `request.data.tx_metadata.trans_fee_allowance_info` | `request.data.trans_fee_allowance_info` | `—（String(JSON) 容器）` | 手续费补贴信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 手续费补贴信息对象，jsonObject字符串 |
| `request.data.tx_metadata.trans_fee_allowance_info.allowance_fee_amt` | `request.data.trans_fee_allowance_info` | `$.allowance_fee_amt` | 补贴手续费金额 | `String` | `16` | `N` | 已确认 | 金额以元为单位，最少1分，示例值：0.01；1.补贴手续费金额小于或等于该笔手续费金额时，按照补贴手续费金额补贴；2.补贴手续费金额大于该笔手续费金额时，按照该笔交易实际手续费金额补贴 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/docs/start/#/kfjr/jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `Json` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/lightning/api/jhzfxd.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `256` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/lightning/api/jhzfxd.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回；示例值：20220905 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 交易时传入，原样返回；示例值：rQ[官网示例已脱敏] |
| `response.data.hf_seq_id` | `response.data.hf_seq_id` | `—（直接 JSON 路径）` | 全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00470topo1A221019132207P068ac1362af00000 |
| `response.data.trade_type` | `response.data.trade_type` | `—（直接 JSON 路径）` | 交易类型 | `String` | `16` | `N` | 已确认 | T_JSAPI: 微信公众号支付；T_MINIAPP: 微信小程序支付 ；A_JSAPI: 支付宝JS ；A_NATIVE: 支付宝正扫 ；U_NATIVE: 银联正扫 ；U_JSAPI: 银联 JS ；D_NATIVE: 数字人民币正扫 ；T_H5：微信直连H5支付；T_APP：微信APP支付；示例值：T_JSAPI |
| `response.data.trans_amt` | `response.data.trans_amt` | `—（直接 JSON 路径）` | 交易金额 | `String` | `14` | `N` | 已确认 | 单位元， 示例值：1.00单位元， 示例值：1.00 |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `1` | `N` | 已确认 | P:处理中、S:成功、F:失败；交易状态以此字段为准。示例值：S |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.delay_acct_flag` | `response.data.delay_acct_flag` | `—（直接 JSON 路径）` | 延时标记 | `String` | `1` | `N` | 已确认 | Y: 延迟 N: 实时（默认）；示例值：Y注意延时交易要调【交易确认】接口资金才能进入收款方账户，否则会停留在延时账户中。 |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `255` | `N` | 已确认 | 原样返回；示例值：备注 |
| `response.data.device_type` | `response.data.device_type` | `—（直接 JSON 路径）` | 终端类型 | `String` | `2` | `N` | 已确认 | 01-智能POS；02-扫码POS；03-云音箱；04-台牌；05-云打印；06-扫脸设备；07-收银机；08-收银助手；09-传统POS；10-一体音箱；11-虚拟终端；示例值：01 |
| `response.data.out_trans_id` | `response.data.out_trans_id` | `—（直接 JSON 路径）` | 用户账单上的交易订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `response.data.party_order_id` | `response.data.party_order_id` | `—（直接 JSON 路径）` | 用户账单上的商户订单号 | `String` | `64` | `N` | 已确认 | 参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd)；示例值：[官网示例已脱敏] |
| `response.data.pay_info` | `response.data.pay_info` | `—（直接 JSON 路径）` | js支付信息 | `String` | `1024` | `N` | 已确认 | JSAPI支付返回信息 |
| `response.data.qr_code` | `response.data.qr_code` | `—（直接 JSON 路径）` | 二维码链接 | `String` | `1024` | `N` | 已确认 | NATIVE支付返回二维码链接；示例值：https://qr.alipay.com/bax03232ftw69valbwmg000d |
| `response.data.atu_sub_mer_id` | `response.data.atu_sub_mer_id` | `—（直接 JSON 路径）` | ATU真实商户号 | `String` | `32` | `N` | 已确认 | 微信、支付宝、银联真实商户号；示例值：411111141 |
| `response.data.unconfirm_amt` | `response.data.unconfirm_amt` | `—（直接 JSON 路径）` | 待确认金额 | `String` | `14` | `N` | 已确认 | 待确认金额；单位元。示例值：1.00 |
| `response.data.settlement_amt` | `response.data.settlement_amt` | `—（直接 JSON 路径）` | 结算金额 | `String` | `16` | `N` | 已确认 | 单位元；示例值：1.00 |
| `response.data.debit_type` | `response.data.debit_type` | `—（直接 JSON 路径）` | 借贷记标识 | `String` | `1` | `N` | 已确认 | 1-借记卡，2-贷记卡，3-其他；示例值：1 |
| `response.data.wx_user_id` | `response.data.wx_user_id` | `—（直接 JSON 路径）` | 微信用户唯一标识码 | `String` | `128` | `N` | 已确认 | 示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk= |
| `response.data.end_time` | `response.data.end_time` | `—（直接 JSON 路径）` | 支付完成时间 | `String` | `14` | `N` | 已确认 | 格式yyyyMMddHHMMSS，示例值：20091225091010 |
| `response.data.acct_id` | `response.data.acct_id` | `—（直接 JSON 路径）` | 账户号 | `String` | `9` | `N` | 已确认 | 商户账户号；示例值：F00598600 |
| `response.data.acct_stat` | `response.data.acct_stat` | `—（直接 JSON 路径）` | 账务状态 | `String` | `1` | `N` | 已确认 | P：处理中，S：成功，F：失败；示例值：S |
| `response.data.bank_message` | `response.data.bank_message` | `—（直接 JSON 路径）` | 通道返回描述 | `String` | `200` | `N` | 已确认 | 示例值：成功[0000000] |
| `response.data.method_expand` | `response.data.method_expand` | `—（String(JSON) 容器）` | 交易扩展参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.method_expand.T_JSAPI` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 微信公众号支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `response.data.method_expand.T_JSAPI.sub_appid` | `response.data.method_expand` | `$.sub_appid` | 子商户公众账号ID | `String` | `32` | `N` | 已确认 | 微信分配的子商户公众账号ID；示例值：wxec280d4c8a1cc2ca |
| `response.data.method_expand.T_JSAPI.openid` | `response.data.method_expand` | `$.openid` | 用户标识 | `String` | `128` | `N` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `response.data.method_expand.T_JSAPI.sub_openid` | `response.data.method_expand` | `$.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `response.data.method_expand.T_JSAPI.bank_type` | `response.data.method_expand` | `$.bank_type` | 付款银行 | `String` | `16` | `N` | 已确认 | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/doc/v3/merchant/4012076355)；示例值：OTHERS |
| `response.data.method_expand.T_JSAPI.coupon_fee` | `response.data.method_expand` | `$.coupon_fee` | 代金券金额 | `String` | `100` | `N` | 已确认 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：0.10 |
| `response.data.method_expand.T_JSAPI.attach` | `response.data.method_expand` | `$.attach` | 商家数据包 | `String` | `127` | `N` | 已确认 | 商家数据包，原样返回；示例值：附加数据 |
| `response.data.method_expand.T_JSAPI.promotion_detail[]` | `response.data.method_expand` | `$.promotion_detail[]` | 营销详情列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 营销详情列表，使返回值为Json格式 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].promotion_id` | `response.data.method_expand` | `$.promotion_detail[].promotion_id` | 券id | `String` | `32` | `Y` | 已确认 | 券或者立减优惠id；示例值：2345234235 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].name` | `response.data.method_expand` | `$.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].scope` | `response.data.method_expand` | `$.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL: 全场代金券，SINGLE: 单品优惠；示例值：GLOBAL |
| `response.data.method_expand.T_JSAPI.promotion_detail[].type` | `response.data.method_expand` | `$.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON: 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致） ；DISCOUNT: 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `response.data.method_expand.T_JSAPI.promotion_detail[].amount` | `response.data.method_expand` | `$.promotion_detail[].amount` | 优惠券面额 | `String` | `12` | `Y` | 已确认 | 用户享受优惠的金额；（优惠券面额=微信出资金额+商家出资金额+其他出资方金额 ）示例值：5.00 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].activity_id` | `response.data.method_expand` | `$.promotion_detail[].activity_id` | 活动ID | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `response.data.method_expand.T_JSAPI.promotion_detail[].merchant_contribute` | `response.data.method_expand` | `$.promotion_detail[].merchant_contribute` | 商户出资 | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；示例值：10.00 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].other_contribute` | `response.data.method_expand` | `$.promotion_detail[].other_contribute` | 其他出资 | `String` | `32` | `N` | 已确认 | 其他出资方出资金额=商家出资+微信出资，单位为元；示例值：20.00 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].goods_detail[]` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[]` | 单品列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 单品信息，使用Json格式，是promotion_detail的元素 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].goods_detail[].goods_id` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].goods_detail[].goods_remark` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。；示例值：商品备注 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].goods_detail[].discount_amount` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，单位为：元；示例值：20.00 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].goods_detail[].quantity` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].goods_detail[].price` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].price` | 商品价格 | `String` | `32` | `Y` | 已确认 | 单位为:元。示例值：99.00；如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，；则活动商品的单价应为原单价-50元 |
| `response.data.method_expand.T_MINIAPP` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 微信小程序支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `response.data.method_expand.T_MINIAPP.sub_appid` | `response.data.method_expand` | `$.sub_appid` | 子商户公众账号ID | `String` | `32` | `N` | 已确认 | 微信分配的子商户公众账号ID；示例值：wxec280d4c8a1cc2ca |
| `response.data.method_expand.T_MINIAPP.openid` | `response.data.method_expand` | `$.openid` | 用户标识 | `String` | `128` | `N` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `response.data.method_expand.T_MINIAPP.sub_openid` | `response.data.method_expand` | `$.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `response.data.method_expand.T_MINIAPP.bank_type` | `response.data.method_expand` | `$.bank_type` | 付款银行 | `String` | `16` | `N` | 已确认 | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/doc/v3/merchant/4012076355)；示例值：OTHERS |
| `response.data.method_expand.T_MINIAPP.coupon_fee` | `response.data.method_expand` | `$.coupon_fee` | 代金券金额 | `String` | `100` | `N` | 已确认 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：0.10 |
| `response.data.method_expand.T_MINIAPP.attach` | `response.data.method_expand` | `$.attach` | 商家数据包 | `String` | `127` | `N` | 已确认 | 商家数据包，原样返回；示例值：附加数据 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[]` | `response.data.method_expand` | `$.promotion_detail[]` | 营销详情列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 营销详情列表，使返回值为Json格式 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].promotion_id` | `response.data.method_expand` | `$.promotion_detail[].promotion_id` | 券id | `String` | `32` | `Y` | 已确认 | 券或者立减优惠id；示例值：2345234235 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].name` | `response.data.method_expand` | `$.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].scope` | `response.data.method_expand` | `$.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL: 全场代金券，SINGLE: 单品优惠；示例值：GLOBAL |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].type` | `response.data.method_expand` | `$.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON: 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致） ；DISCOUNT: 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].amount` | `response.data.method_expand` | `$.promotion_detail[].amount` | 优惠券面额 | `String` | `12` | `Y` | 已确认 | 用户享受优惠的金额；（优惠券面额=微信出资金额+商家出资金额+其他出资方金额 ）示例值：5.00 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].activity_id` | `response.data.method_expand` | `$.promotion_detail[].activity_id` | 活动ID | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].merchant_contribute` | `response.data.method_expand` | `$.promotion_detail[].merchant_contribute` | 商户出资 | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；示例值：10.00 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].other_contribute` | `response.data.method_expand` | `$.promotion_detail[].other_contribute` | 其他出资 | `String` | `32` | `N` | 已确认 | 其他出资方出资金额=商家出资+微信出资，单位为元；示例值：20.00 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].goods_detail[]` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[]` | 单品列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 单品信息，使用Json格式，是promotion_detail的元素 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].goods_detail[].goods_id` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].goods_detail[].goods_remark` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。；示例值：商品备注 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].goods_detail[].discount_amount` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，单位为：元；示例值：20.00 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].goods_detail[].quantity` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].goods_detail[].price` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].price` | 商品价格 | `String` | `32` | `Y` | 已确认 | 单位为:元。示例值：99.00；如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，；则活动商品的单价应为原单价-50元 |
| `response.data.method_expand.T_APP` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 微信APP支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `response.data.method_expand.T_APP.sub_appid` | `response.data.method_expand` | `$.sub_appid` | 子商户公众账号ID | `String` | `32` | `N` | 已确认 | 微信分配的子商户公众账号ID；示例值：wxec280d4c8a1cc2ca |
| `response.data.method_expand.T_APP.openid` | `response.data.method_expand` | `$.openid` | 用户标识 | `String` | `128` | `N` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `response.data.method_expand.T_APP.sub_openid` | `response.data.method_expand` | `$.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `response.data.method_expand.T_APP.bank_type` | `response.data.method_expand` | `$.bank_type` | 付款银行 | `String` | `16` | `N` | 已确认 | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/doc/v3/merchant/4012076355)；示例值：OTHERS |
| `response.data.method_expand.T_APP.coupon_fee` | `response.data.method_expand` | `$.coupon_fee` | 代金券金额 | `String` | `100` | `N` | 已确认 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：0.10 |
| `response.data.method_expand.T_APP.attach` | `response.data.method_expand` | `$.attach` | 商家数据包 | `String` | `127` | `N` | 已确认 | 商家数据包，原样返回；示例值：附加数据 |
| `response.data.method_expand.T_APP.promotion_detail[]` | `response.data.method_expand` | `$.promotion_detail[]` | 营销详情列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 营销详情列表，使返回值为Json格式 |
| `response.data.method_expand.T_APP.promotion_detail[].promotion_id` | `response.data.method_expand` | `$.promotion_detail[].promotion_id` | 券id | `String` | `32` | `Y` | 已确认 | 券或者立减优惠id；示例值：2345234235 |
| `response.data.method_expand.T_APP.promotion_detail[].name` | `response.data.method_expand` | `$.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `response.data.method_expand.T_APP.promotion_detail[].scope` | `response.data.method_expand` | `$.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL: 全场代金券，SINGLE: 单品优惠；示例值：GLOBAL |
| `response.data.method_expand.T_APP.promotion_detail[].type` | `response.data.method_expand` | `$.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON: 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致） ；DISCOUNT: 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `response.data.method_expand.T_APP.promotion_detail[].amount` | `response.data.method_expand` | `$.promotion_detail[].amount` | 优惠券面额 | `String` | `12` | `Y` | 已确认 | 用户享受优惠的金额；（优惠券面额=微信出资金额+商家出资金额+其他出资方金额 ）示例值：5.00 |
| `response.data.method_expand.T_APP.promotion_detail[].activity_id` | `response.data.method_expand` | `$.promotion_detail[].activity_id` | 活动ID | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `response.data.method_expand.T_APP.promotion_detail[].merchant_contribute` | `response.data.method_expand` | `$.promotion_detail[].merchant_contribute` | 商户出资 | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；示例值：10.00 |
| `response.data.method_expand.T_APP.promotion_detail[].other_contribute` | `response.data.method_expand` | `$.promotion_detail[].other_contribute` | 其他出资 | `String` | `32` | `N` | 已确认 | 其他出资方出资金额=商家出资+微信出资，单位为元；示例值：20.00 |
| `response.data.method_expand.T_APP.promotion_detail[].goods_detail[]` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[]` | 单品列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 单品信息，使用Json格式，是promotion_detail的元素 |
| `response.data.method_expand.T_APP.promotion_detail[].goods_detail[].goods_id` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `response.data.method_expand.T_APP.promotion_detail[].goods_detail[].goods_remark` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。；示例值：商品备注 |
| `response.data.method_expand.T_APP.promotion_detail[].goods_detail[].discount_amount` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，单位为：元；示例值：20.00 |
| `response.data.method_expand.T_APP.promotion_detail[].goods_detail[].quantity` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `response.data.method_expand.T_APP.promotion_detail[].goods_detail[].price` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].price` | 商品价格 | `String` | `32` | `Y` | 已确认 | 单位为:元。示例值：99.00；如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，；则活动商品的单价应为原单价-50元 |
| `response.data.method_expand.T_MICROPAY` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 微信反扫支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `response.data.method_expand.T_MICROPAY.openid` | `response.data.method_expand` | `$.openid` | 用户标识 | `String` | `128` | `N` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `response.data.method_expand.T_MICROPAY.sub_openid` | `response.data.method_expand` | `$.sub_openid` | 子商户用户标识 | `String` | `32` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `response.data.method_expand.T_MICROPAY.cash_fee` | `response.data.method_expand` | `$.cash_fee` | 现金支付金额 | `String` | `12` | `N` | 已确认 | 现金支付金额订单现金支付金额；示例值：1.00 |
| `response.data.method_expand.T_MICROPAY.attach` | `response.data.method_expand` | `$.attach` | 商家数据包 | `String` | `128` | `N` | 已确认 | 原样返回；示例值：附加数据 |
| `response.data.method_expand.T_MICROPAY.coupon_fee` | `response.data.method_expand` | `$.coupon_fee` | 代金券金额 | `String` | `—` | `N` | [需要官方确认]：长度 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：1.00 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[]` | `response.data.method_expand` | `$.promotion_detail[]` | 营销详情列表 | `Array` | `6000` | `N` | 已确认 | 使返回值为Json格式， |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].activity_id` | `response.data.method_expand` | `$.promotion_detail[].activity_id` | 活动id | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].amount` | `response.data.method_expand` | `$.promotion_detail[].amount` | 优惠券面额 | `String` | `5` | `Y` | 已确认 | 用户享受优惠的金额；示例值：10.00 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].promotion_id` | `response.data.method_expand` | `$.promotion_detail[].promotion_id` | 券或者立减优惠id | `String` | `32` | `Y` | 已确认 | 示例值：2345234235 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].goods_detail[]` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[]` | 单品列表 | `Array` | `3000` | `N` | 已确认 | 单品信息，使用Json格式，是promotion_detail的元素 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].goods_detail[].discount_amount` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，单位为：元；示例值：20.00 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].goods_detail[].goods_id` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].goods_detail[].price` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].price` | 商品价格 | `String` | `32` | `Y` | 已确认 | 单位为：元。示例值：50.00。；如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，；则活动商品的单价应为原单价-50元 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].goods_detail[].quantity` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].goods_detail[].goods_remark` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | 按照配置原样返回，字段内容在微信后台配置券时进行设置。示例值：商品备注 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].merchant_contribute` | `response.data.method_expand` | `$.promotion_detail[].merchant_contribute` | 商户出资 | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；示例值：10.00 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].name` | `response.data.method_expand` | `$.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].other_contribute` | `response.data.method_expand` | `$.promotion_detail[].other_contribute` | 其他出资 | `String` | `32` | `N` | 已确认 | 其他出资方出资金额=商家出资+微信出资，单位为元；示例值：20.00 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].scope` | `response.data.method_expand` | `$.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL:全场代金券，SINGLE:单品优惠；示例值：GLOBAL |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].type` | `response.data.method_expand` | `$.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON:代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）；DISCOUNT:优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].wxpay_contribute` | `response.data.method_expand` | `$.promotion_detail[].wxpay_contribute` | 微信出资 | `String` | `32` | `N` | 已确认 | 特指由微信支付商户平台创建的优惠，单位：元；示例值：20.00 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].original_other_contribute` | `response.data.method_expand` | `$.promotion_detail[].original_other_contribute` | 微信交易其他出资方出资金额 | `String` | `32` | `N` | 已确认 | 微信的其他出资方出资金额，单位：元；示例值：20.00 |
| `response.data.method_expand.T_MICROPAY.bank_type` | `response.data.method_expand` | `$.bank_type` | 付款银行 | `String` | `16` | `N` | 已确认 | 银行类型，采用字符串类型的银行标识，银行类型见[微信银行类型说明](https://pay.weixin.qq.com/doc/v3/merchant/4012076355)；示例值：ICBC_DEBIT |
| `response.data.method_expand.A_JSAPI` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 支付宝JS支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[]` | `response.data.method_expand` | `$.voucher_detail_list[]` | 优惠券信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 本交易支付时使用的所有优惠券信息；示例值："[{\"id\":\"[官网示例已脱敏]X1M6V\",\"name\":\"全仓 5折优惠券\"}]" |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[].id` | `response.data.method_expand` | `$.voucher_detail_list[].id` | 券id | `String` | `32` | `Y` | 已确认 | 示例值：6934572310301 |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[].name` | `response.data.method_expand` | `$.voucher_detail_list[].name` | 券名称 | `String` | `32` | `Y` | 已确认 | 示例值：实体店付款通用立减券 |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[].type` | `response.data.method_expand` | `$.voucher_detail_list[].type` | 券类型 | `String` | `32` | `Y` | 已确认 | 当前有三种类型：；ALIPAY_FIX_VOUCHER: 全场代金券；ALIPAY_DISCOUNT_VOUCHER: 折扣券；ALIPAY_ITEM_VOUCHER: 单品优惠 ；示例值：ALIPAY_ITEM_VOUCHER注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码 |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[].amount` | `response.data.method_expand` | `$.voucher_detail_list[].amount` | 优惠券面额 | `String` | `12` | `Y` | 已确认 | 优惠券面额，它应该会等于商家出资加上其他出资方出资；示例值：10.00 |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[].merchant_contribute` | `response.data.method_expand` | `$.voucher_detail_list[].merchant_contribute` | 商家出资 | `String` | `12` | `N` | 已确认 | 特指发起交易的商家出资金额；示例值：10.00 |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[].other_contribute` | `response.data.method_expand` | `$.voucher_detail_list[].other_contribute` | 其他出资方出资金额 | `String` | `11` | `N` | 已确认 | 可能是支付宝，可能是品牌商，或者其他方，也可能是他们的一起出资；示例值：0.00 |
| `response.data.method_expand.A_JSAPI.fund_bill_list[]` | `response.data.method_expand` | `$.fund_bill_list[]` | 资金渠道 | `Array` | `—` | `N` | N/A：结构字段长度 | 支付成功的各个渠道金额信息。交易支付使用的资金渠道。只有在签约中指定需要返回资金明细，或者入参的query_options 中指定时才返回该字段信息。 |
| `response.data.method_expand.A_JSAPI.fund_bill_list[].bank_code` | `response.data.method_expand` | `$.fund_bill_list[].bank_code` | 银行卡支付时的银行代码 | `String` | `10` | `N` | 已确认 | 示例值：CEB |
| `response.data.method_expand.A_JSAPI.fund_bill_list[].amount` | `response.data.method_expand` | `$.fund_bill_list[].amount` | 该支付工具类型所使用的金额 | `String` | `32` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `response.data.method_expand.A_JSAPI.fund_bill_list[].fund_channel` | `response.data.method_expand` | `$.fund_bill_list[].fund_channel` | 交易使用的资金渠道 | `String` | `32` | `N` | 已确认 | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；示例值：ALIPAYACCOUNT |
| `response.data.method_expand.A_JSAPI.fund_bill_list[].fund_type` | `response.data.method_expand` | `$.fund_bill_list[].fund_type` | 渠道所使用的资金类型 | `String` | `32` | `N` | 已确认 | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。；DEBIT_CARD:借记卡，；CREDIT_CARD:信用卡，；MIXED_CARD:借贷合一卡；示例值：DEBIT_CARD |
| `response.data.method_expand.A_JSAPI.fund_bill_list[].real_amount` | `response.data.method_expand` | `$.fund_bill_list[].real_amount` | 渠道实际付款金额 | `String` | `11` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `response.data.method_expand.A_JSAPI.buyer_id` | `response.data.method_expand` | `$.buyer_id` | 买家的支付宝唯一用户号 | `String` | `28` | `N` | 已确认 | 买家的支付宝唯一用户号（2088开头的16位纯数字）；示例值：[官网示例已脱敏] |
| `response.data.method_expand.A_JSAPI.buyer_logon_id` | `response.data.method_expand` | `$.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com |
| `response.data.method_expand.A_JSAPI.hb_fq_num` | `response.data.method_expand` | `$.hb_fq_num` | 花呗分期数 | `String` | `10` | `N` | 已确认 | 示例值：3 |
| `response.data.method_expand.A_JSAPI.hb_fq_seller_percent` | `response.data.method_expand` | `$.hb_fq_seller_percent` | 卖家承担的手续费百分比 | `String` | `3` | `N` | 已确认 | 比例的百分值，示例值：0.9，100代表100% |
| `response.data.method_expand.A_NATIVE` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 支付宝正扫支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[]` | `response.data.method_expand` | `$.voucher_detail_list[]` | 优惠券信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 本交易支付时使用的所有优惠券信息；示例值："[{\"id\":\"[官网示例已脱敏]X1M6V\",\"name\":\"全仓 5折优惠券\"}]" |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[].id` | `response.data.method_expand` | `$.voucher_detail_list[].id` | 券id | `String` | `32` | `Y` | 已确认 | 示例值：6934572310301 |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[].name` | `response.data.method_expand` | `$.voucher_detail_list[].name` | 券名称 | `String` | `32` | `Y` | 已确认 | 示例值：实体店付款通用立减券 |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[].type` | `response.data.method_expand` | `$.voucher_detail_list[].type` | 券类型 | `String` | `32` | `Y` | 已确认 | 当前有三种类型：；ALIPAY_FIX_VOUCHER: 全场代金券；ALIPAY_DISCOUNT_VOUCHER: 折扣券；ALIPAY_ITEM_VOUCHER: 单品优惠 ；示例值：ALIPAY_ITEM_VOUCHER注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码 |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[].amount` | `response.data.method_expand` | `$.voucher_detail_list[].amount` | 优惠券面额 | `String` | `12` | `Y` | 已确认 | 优惠券面额，它应该会等于商家出资加上其他出资方出资；示例值：10.00 |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[].merchant_contribute` | `response.data.method_expand` | `$.voucher_detail_list[].merchant_contribute` | 商家出资 | `String` | `12` | `N` | 已确认 | 特指发起交易的商家出资金额；示例值：10.00 |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[].other_contribute` | `response.data.method_expand` | `$.voucher_detail_list[].other_contribute` | 其他出资方出资金额 | `String` | `11` | `N` | 已确认 | 可能是支付宝，可能是品牌商，或者其他方，也可能是他们的一起出资；示例值：0.00 |
| `response.data.method_expand.A_NATIVE.fund_bill_list[]` | `response.data.method_expand` | `$.fund_bill_list[]` | 资金渠道 | `Array` | `—` | `N` | N/A：结构字段长度 | 支付成功的各个渠道金额信息。交易支付使用的资金渠道。只有在签约中指定需要返回资金明细，或者入参的query_options 中指定时才返回该字段信息。 |
| `response.data.method_expand.A_NATIVE.fund_bill_list[].bank_code` | `response.data.method_expand` | `$.fund_bill_list[].bank_code` | 银行卡支付时的银行代码 | `String` | `10` | `N` | 已确认 | 示例值：CEB |
| `response.data.method_expand.A_NATIVE.fund_bill_list[].amount` | `response.data.method_expand` | `$.fund_bill_list[].amount` | 该支付工具类型所使用的金额 | `String` | `32` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `response.data.method_expand.A_NATIVE.fund_bill_list[].fund_channel` | `response.data.method_expand` | `$.fund_bill_list[].fund_channel` | 交易使用的资金渠道 | `String` | `32` | `N` | 已确认 | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；示例值：ALIPAYACCOUNT |
| `response.data.method_expand.A_NATIVE.fund_bill_list[].fund_type` | `response.data.method_expand` | `$.fund_bill_list[].fund_type` | 渠道所使用的资金类型 | `String` | `32` | `N` | 已确认 | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。；DEBIT_CARD:借记卡，；CREDIT_CARD:信用卡，；MIXED_CARD:借贷合一卡；示例值：DEBIT_CARD |
| `response.data.method_expand.A_NATIVE.fund_bill_list[].real_amount` | `response.data.method_expand` | `$.fund_bill_list[].real_amount` | 渠道实际付款金额 | `String` | `11` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `response.data.method_expand.A_NATIVE.buyer_id` | `response.data.method_expand` | `$.buyer_id` | 买家的支付宝唯一用户号 | `String` | `28` | `N` | 已确认 | 买家的支付宝唯一用户号（2088开头的16位纯数字）；示例值：[官网示例已脱敏] |
| `response.data.method_expand.A_NATIVE.buyer_logon_id` | `response.data.method_expand` | `$.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com |
| `response.data.method_expand.A_NATIVE.hb_fq_num` | `response.data.method_expand` | `$.hb_fq_num` | 花呗分期数 | `String` | `10` | `N` | 已确认 | 示例值：3 |
| `response.data.method_expand.A_NATIVE.hb_fq_seller_percent` | `response.data.method_expand` | `$.hb_fq_seller_percent` | 卖家承担的手续费百分比 | `String` | `3` | `N` | 已确认 | 比例的百分值，示例值：0.9，100代表100% |
| `response.data.method_expand.A_MICROPAY` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 支付宝反扫参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `response.data.method_expand.A_MICROPAY.buyer_id` | `response.data.method_expand` | `$.buyer_id` | 买家支付宝用户号 | `String` | `28` | `N` | 已确认 | 买家的支付宝唯一用户号（2088开头的16位纯数字）；示例值：[官网示例已脱敏] |
| `response.data.method_expand.A_MICROPAY.buyer_logon_id` | `response.data.method_expand` | `$.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com |
| `response.data.method_expand.A_MICROPAY.fund_bill_list[]` | `response.data.method_expand` | `$.fund_bill_list[]` | 交易支付使用的资金渠道 | `Array` | `2048` | `N` | 已确认 | — |
| `response.data.method_expand.A_MICROPAY.fund_bill_list[].bank_code` | `response.data.method_expand` | `$.fund_bill_list[].bank_code` | 银行卡支付时的银行代码 | `String` | `10` | `N` | 已确认 | 示例值：CEB，请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
| `response.data.method_expand.A_MICROPAY.fund_bill_list[].amount` | `response.data.method_expand` | `$.fund_bill_list[].amount` | 该支付工具类型所使用的金额 | `String` | `32` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `response.data.method_expand.A_MICROPAY.fund_bill_list[].fund_channel` | `response.data.method_expand` | `$.fund_bill_list[].fund_channel` | 交易使用的资金渠道 | `String` | `32` | `N` | 已确认 | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；示例值：ALIPAYACCOUNT |
| `response.data.method_expand.A_MICROPAY.fund_bill_list[].fund_type` | `response.data.method_expand` | `$.fund_bill_list[].fund_type` | 渠道所使用的资金类型 | `String` | `32` | `N` | 已确认 | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。；DEBIT_CARD:借记卡，CREDIT_CARD:信用卡，MIXED_CARD:借贷合一卡；示例值：DEBIT_CARD |
| `response.data.method_expand.A_MICROPAY.fund_bill_list[].real_amount` | `response.data.method_expand` | `$.fund_bill_list[].real_amount` | 渠道实际付款金额 | `String` | `11` | `N` | 已确认 | 单位：元，两位小数；示例值：2.00 |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[]` | `response.data.method_expand` | `$.voucher_detail_list[]` | 本交易支付时使用的所有优惠券信息 | `Array` | `2048` | `N` | 已确认 | — |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[].amount` | `response.data.method_expand` | `$.voucher_detail_list[].amount` | 优惠券面额（元） | `String` | `8` | `Y` | 已确认 | 用户享受优惠的金额；示例值：10.00 |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[].id` | `response.data.method_expand` | `$.voucher_detail_list[].id` | 券id | `String` | `32` | `Y` | 已确认 | 优惠券号；示例值：6934572310301 |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[].name` | `response.data.method_expand` | `$.voucher_detail_list[].name` | 券名称 | `String` | `32` | `Y` | 已确认 | 优惠名称；示例值：实体店付款通用立减券 |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[].type` | `response.data.method_expand` | `$.voucher_detail_list[].type` | 券类型 | `String` | `32` | `Y` | 已确认 | 当前有三种类型：；ALIPAY_FIX_VOUCHER - 全场代金券,；ALIPAY_DISCOUNT_VOUCHER - 折扣券,；ALIPAY_ITEM_VOUCHER - 单品优惠。；示例值：ALIPAY_DISCOUNT_VOUCHER；注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码 |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[].merchant_contribute` | `response.data.method_expand` | `$.voucher_detail_list[].merchant_contribute` | 商家出资 | `String` | `12` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；示例值：10.00 |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[].other_contribute` | `response.data.method_expand` | `$.voucher_detail_list[].other_contribute` | 其他出资方出资金额 | `String` | `11` | `N` | 已确认 | 单位为元；示例值：0.00 |
| `response.data.method_expand.U_JSAPI` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 银联JS支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `response.data.method_expand.U_JSAPI.qr_valid_time` | `response.data.method_expand` | `$.qr_valid_time` | 二维码有效时间 | `String` | `10` | `N` | 已确认 | 允许对一个订单进行支付的最长相对时间，单位为秒；示例值：120 |
| `response.data.method_expand.U_NATIVE` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 银联正扫支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `response.data.method_expand.U_NATIVE.qr_valid_time` | `response.data.method_expand` | `$.qr_valid_time` | 二维码有效时间 | `String` | `10` | `N` | 已确认 | 允许对一个订单进行支付的最长相对时间，单位为秒；示例值：120 |
| `response.data.method_expand.U_MICROPAY` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 银联反扫支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `response.data.method_expand.U_MICROPAY.coupon_info[]` | `response.data.method_expand` | `$.coupon_info[]` | 银联优惠信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 银联使用优惠活动时出现，jsonArray格式 |
| `response.data.method_expand.U_MICROPAY.coupon_info[].addnInfo` | `response.data.method_expand` | `$.coupon_info[].addnInfo` | 附加信息 | `String` | `100` | `N` | 已确认 | 内容自定义；示例值：附加信息 |
| `response.data.method_expand.U_MICROPAY.coupon_info[].spnsrId` | `response.data.method_expand` | `$.coupon_info[].spnsrId` | 出资方 | `String` | `20` | `Y` | 已确认 | 00010000：银联出资；付款方作为出资方：填写8位付款方机构代码；商户作为出资方：填写15位商户代码；示例值：00010000 |
| `response.data.method_expand.U_MICROPAY.coupon_info[].type` | `response.data.method_expand` | `$.coupon_info[].type` | 项目类型 | `String` | `4` | `Y` | 已确认 | DD01：随机立减；CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券；CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券；示例值：DD01 |
| `response.data.method_expand.U_MICROPAY.coupon_info[].offstAmt` | `response.data.method_expand` | `$.coupon_info[].offstAmt` | 抵消交易金额 | `String` | `14` | `Y` | 已确认 | 不能为全0；示例值：1.00 |
| `response.data.method_expand.U_MICROPAY.coupon_info[].id` | `response.data.method_expand` | `$.coupon_info[].id` | 项目编号 | `String` | `40` | `N` | 已确认 | 用于票券编号等，格式自定义；示例值：938434221 |
| `response.data.method_expand.U_MICROPAY.coupon_info[].desc` | `response.data.method_expand` | `$.coupon_info[].desc` | 项目简称 | `String` | `40` | `N` | 已确认 | 优惠活动简称，可用于展示、打单等；示例值：中秋优惠促销 |
| `response.data.method_expand.U_MICROPAY.acc_no` | `response.data.method_expand` | `$.acc_no` | 付款账号 | `String` | `40` | `N` | 已确认 | 付款方的卡号/账号/Token |
| `response.data.tx_metadata` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 扩展参数集合 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，tx_metadata只是方便文档展示，实际请求时不需要传入，传入下面的子项即可 |
| `response.data.tx_metadata.combinedpay_data[]` | `response.data.combinedpay_data` | `—（String(JSON Array) 容器）` | 补贴支付信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray字符串，参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| `response.data.tx_metadata.combinedpay_data[].huifu_id` | `response.data.combinedpay_data` | `$[].huifu_id` | 补贴方汇付商户号 | `String` | `32` | `N` | 已确认 | 补贴方汇付ID；示例值：[官网示例已脱敏] |
| `response.data.tx_metadata.combinedpay_data[].user_type` | `response.data.combinedpay_data` | `$[].user_type` | 补贴方类型 | `String` | `32` | `N` | 已确认 | channel-渠道，merchant-总部商户，agent-代理，mertomer-商户；示例值：channel |
| `response.data.tx_metadata.combinedpay_data[].acct_id` | `response.data.combinedpay_data` | `$[].acct_id` | 补贴方账户号 | `String` | `32` | `N` | 已确认 | 营销补贴方账户号；示例值：F00900982 |
| `response.data.tx_metadata.combinedpay_data[].amount` | `response.data.combinedpay_data` | `$[].amount` | 补贴金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； 示例值：1.01 |
| `response.data.tx_metadata.combinedpay_data_fee_info` | `response.data.combinedpay_data_fee_info` | `—（String(JSON) 容器）` | 补贴支付手续费承担方信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.tx_metadata.combinedpay_data_fee_info.huifu_id` | `response.data.combinedpay_data_fee_info` | `$.huifu_id` | 补贴支付手续费承担方汇付编号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.tx_metadata.combinedpay_data_fee_info.acct_id` | `response.data.combinedpay_data_fee_info` | `$.acct_id` | 补贴支付手续费承担方账户号 | `String` | `32` | `N` | 已确认 | 补贴支付手续费承担方账户号；示例值：F00598610 |
| `response.data.tx_metadata.combinedpay_data_fee_info.combinedpay_fee_amt` | `response.data.combinedpay_data_fee_info` | `$.combinedpay_fee_amt` | 补贴支付手续费金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； 示例值：1.01 |
| `response.data.tx_metadata.trans_fee_allowance_info` | `response.data.trans_fee_allowance_info` | `—（String(JSON) 容器）` | 手续费补贴信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 手续费补贴信息对象，jsonObject字符串 |
| `response.data.tx_metadata.trans_fee_allowance_info.receivable_fee_amt` | `response.data.trans_fee_allowance_info` | `$.receivable_fee_amt` | 商户应收手续费 | `String` | `16` | `N` | 已确认 | 示例值：5.00 |
| `response.data.tx_metadata.trans_fee_allowance_info.actual_fee_amt` | `response.data.trans_fee_allowance_info` | `$.actual_fee_amt` | 商户实收手续费 | `String` | `16` | `N` | 已确认 | 示例值：4.00 |
| `response.data.tx_metadata.trans_fee_allowance_info.allowance_fee_amt` | `response.data.trans_fee_allowance_info` | `$.allowance_fee_amt` | 补贴手续费 | `String` | `16` | `N` | 已确认 | 示例值：1.00 |
| `response.data.tx_metadata.terminal_device_data` | `response.data.terminal_device_data` | `—（String(JSON) 容器）` | 设备信息 | `String` | `128` | `N` | 已确认 | 设备信息，jsonObject字符串 |
| `response.data.tx_metadata.terminal_device_data.terminal_ip` | `response.data.terminal_device_data` | `$.terminal_ip` | 交易设备IP | `String` | `64` | `N` | 已确认 | 绑卡设备（付款 APP） 所在的公网IP，可用于定位所属地区，不是 wifi 连接时的局域网 IP。；局域网 IP 包括：；A 类： 10.0.0.0-10.255.255.255；B 类： 172.16.0.0-172.31.255.255；C 类： 192.168.0.0-192.168.255.255；示例值：192.168.0.0 |
| `response.data.tx_metadata.terminal_device_data.terminal_location` | `response.data.terminal_device_data` | `$.terminal_location` | 终端实时经纬度信息 | `String` | `32` | `N` | 已确认 | 设备（付款APP）GPS位置,格式为纬度/经度，+表示北纬、东经，-表示南纬、西经。；经度整数位不超过3位，小数位不超过5位；纬度整数位不超过2位，小数位不超过6位。；示例值：+37.12/-121.213 |
| `response.data.payment_fee` | `response.data.payment_fee` | `—（String(JSON) 容器）` | 手续费对象 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.payment_fee.fee_huifu_id` | `response.data.payment_fee` | `$.fee_huifu_id` | 手续费商户号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.payment_fee.fee_flag` | `response.data.payment_fee` | `$.fee_flag` | 手续费扣款标志 | `String` | `1` | `N` | 已确认 | 1: 外扣，2: 内扣；示例值：1 |
| `response.data.payment_fee.fee_formula_infos[]` | `response.data.payment_fee` | `$.fee_formula_infos[]` | 手续费费率信息 | `Array` | `—` | `N` | N/A：结构字段长度 | jsonArray格式；交易成功时返回手续费费率信息 |
| `response.data.payment_fee.fee_formula_infos[].fee_formula` | `response.data.payment_fee` | `$.fee_formula_infos[].fee_formula` | 手续费计算公式 | `String` | `512` | `N` | 已确认 | 示例值：AMT\*0.003 |
| `response.data.payment_fee.fee_formula_infos[].fee_type` | `response.data.payment_fee` | `$.fee_formula_infos[].fee_type` | 手续费类型 | `String` | `32` | `N` | 已确认 | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；示例值：ACCT_FEE |
| `response.data.payment_fee.fee_formula_infos[].huifu_id` | `response.data.payment_fee` | `$.fee_formula_infos[].huifu_id` | 商户号 | `String` | `32` | `N` | 已确认 | 组合支付账户补贴时，补贴账户的huifuId；示例值：[官网示例已脱敏] |
| `response.data.payment_fee.fee_amount` | `response.data.payment_fee` | `$.fee_amount` | 手续费金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，同步成功时返回；示例值：1.00 |

### 正扫异步信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.forward.resp_code` | `async.forward.resp_code` | `—（直接 JSON 路径）` | 网关返回码 | `String` | `8` | `Y` | 已确认 | 示例值：00000000 |
| `async.forward.resp_desc` | `async.forward.resp_desc` | `—（直接 JSON 路径）` | 网关返回信息 | `String` | `512` | `Y` | 已确认 | 示例值：交易成功[000] |
| `async.forward.sign` | `async.forward.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `async.forward.resp_data` | `async.forward.resp_data` | `—（String(JSON) 容器）` | 返回业务数据 | `String` | `—` | `Y` | [需要官方确认]：长度 | jsonObject |

### 正扫异步 resp_data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.forward.resp_data.resp_code` | `async.forward.resp_data` | `$.resp_code` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/lightning/api/jhzfxd.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `async.forward.resp_data.resp_desc` | `async.forward.resp_data` | `$.resp_desc` | 业务响应信息 | `String` | `256` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/lightning/api/jhzfxd.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `async.forward.resp_data.huifu_id` | `async.forward.resp_data` | `$.huifu_id` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.forward.resp_data.req_seq_id` | `async.forward.resp_data` | `$.req_seq_id` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 交易时传入，原样返回；示例值：rQ[官网示例已脱敏] |
| `async.forward.resp_data.req_date` | `async.forward.resp_data` | `$.req_date` | 请求日期 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回；示例值：20220905 |
| `async.forward.resp_data.trans_type` | `async.forward.resp_data` | `$.trans_type` | 交易类型 | `String` | `16` | `N` | 已确认 | T_JSAPI: 微信公众号支付；T_MINIAPP: 微信小程序支付 ；A_JSAPI: 支付宝JS ；A_NATIVE: 支付宝正扫 ；U_NATIVE: 银联正扫 ；U_JSAPI: 银联 JS ；D_NATIVE: 数字人民币正扫 ；T_H5：微信直连H5支付；T_APP：微信APP支付；示例值：T_JSAPI |
| `async.forward.resp_data.hf_seq_id` | `async.forward.resp_data` | `$.hf_seq_id` | 全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00470topo1A221019132207P068ac1362af00000 |
| `async.forward.resp_data.out_trans_id` | `async.forward.resp_data` | `$.out_trans_id` | 用户账单上的交易订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.forward.resp_data.party_order_id` | `async.forward.resp_data` | `$.party_order_id` | 用户账单上的商户订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.forward.resp_data.trans_amt` | `async.forward.resp_data` | `$.trans_amt` | 交易金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `async.forward.resp_data.pay_amt` | `async.forward.resp_data` | `$.pay_amt` | 消费者实付金额 | `String` | `14` | `N` | 已确认 | 单位元， 示例值：1.00 |
| `async.forward.resp_data.settlement_amt` | `async.forward.resp_data` | `$.settlement_amt` | 结算金额(元) | `String` | `16` | `N` | 已确认 | 实际应结金额(订单金额扣除优惠金额后的值)，保留小数点后两位，示例值：1000.00 |
| `async.forward.resp_data.end_time` | `async.forward.resp_data` | `$.end_time` | 支付完成时间 | `String` | `14` | `N` | 已确认 | 格式yyyyMMddHHmmss，示例值：20091225091010 |
| `async.forward.resp_data.acct_date` | `async.forward.resp_data` | `$.acct_date` | 入账时间 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20091225 |
| `async.forward.resp_data.trans_stat` | `async.forward.resp_data` | `$.trans_stat` | 交易状态 | `String` | `1` | `N` | 已确认 | S：成功、F：失败，交易状态以此字段为准。示例值：S |
| `async.forward.resp_data.fee_flag` | `async.forward.resp_data` | `$.fee_flag` | 手续费扣款标志 | `Integer` | `1` | `N` | 已确认 | 1: 外扣，2: 内扣；示例值：2 |
| `async.forward.resp_data.fee_formula_infos[]` | `async.forward.resp_data` | `$.fee_formula_infos[]` | 手续费费率信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 交易成功时返回手续费费率信息 |
| `async.forward.resp_data.fee_formula_infos[].fee_formula` | `async.forward.resp_data` | `$.fee_formula_infos[].fee_formula` | 手续费计算公式 | `String` | `512` | `Y` | 已确认 | 示例值：AMT\*0.003 |
| `async.forward.resp_data.fee_formula_infos[].fee_type` | `async.forward.resp_data` | `$.fee_formula_infos[].fee_type` | 手续费类型 | `String` | `32` | `Y` | 已确认 | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；示例值：ACCT_FEE |
| `async.forward.resp_data.fee_formula_infos[].huifu_id` | `async.forward.resp_data` | `$.fee_formula_infos[].huifu_id` | 商户号 | `String` | `32` | `N` | 已确认 | 补贴支付账户补贴时，补贴账户的huifuId；示例值：[官网示例已脱敏] |
| `async.forward.resp_data.fee_amount` | `async.forward.resp_data` | `$.fee_amount` | 手续费金额 | `String` | `16` | `N` | 已确认 | 单位元，保留小数点后两位，示例值：1.00 |
| `async.forward.resp_data.trans_fee_allowance_info` | `async.forward.resp_data` | `$.trans_fee_allowance_info` | 手续费补贴信息 | `Object` | `—` | `N` | N/A：结构字段长度 | Json格式；参加银行补贴手续费 |
| `async.forward.resp_data.trans_fee_allowance_info.receivable_fee_amt` | `async.forward.resp_data` | `$.trans_fee_allowance_info.receivable_fee_amt` | 商户应收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `async.forward.resp_data.trans_fee_allowance_info.actual_fee_amt` | `async.forward.resp_data` | `$.trans_fee_allowance_info.actual_fee_amt` | 商户实收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `async.forward.resp_data.trans_fee_allowance_info.allowance_fee_amt` | `async.forward.resp_data` | `$.trans_fee_allowance_info.allowance_fee_amt` | 补贴手续费 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `async.forward.resp_data.trans_fee_allowance_info.allowance_type` | `async.forward.resp_data` | `$.trans_fee_allowance_info.allowance_type` | 补贴类型 | `String` | `10` | `N` | 已确认 | 0：不补贴，为空默认；1：补贴；2：部分补贴；3：全额补贴(优惠后)；4：部分补贴(优惠后)；示例值：2 |
| `async.forward.resp_data.trans_fee_allowance_info.no_allowance_desc` | `async.forward.resp_data` | `$.trans_fee_allowance_info.no_allowance_desc` | 不补贴原因 | `String` | `128` | `N` | 已确认 | 1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴；2:额度用完；3:不在有效期；4:活动不存在；5:手续费金额为0不补贴；6:顶格优惠；7:额度不足；8:手续费后补；9:未达到起始补贴金额；示例值：2 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos` | 手续费补贴活动详情 | `Object` | `—` | `N` | N/A：结构字段长度 | 补贴系统返回，斗拱原样返回 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.acct_id` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.acct_id` | 门店 | `String` | `64` | `N` | 已确认 | 示例值：sh002 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.merchant_group` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.merchant_group` | 商户号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys` | 补贴方 | `String` | `64` | `Y` | 已确认 | 1:银行 2:服务商 3:汇来米；示例值：1 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys_id` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys_id` | 补贴方ID | `String` | `64` | `Y` | 已确认 | 对应补贴方的id；示例值：[官网示例已脱敏] |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.is_delay_allowance` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.is_delay_allowance` | 补贴类型 | `String` | `2` | `Y` | 已确认 | 1:实补,2:后补,默认实补；示例值：1 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_id` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.market_id` | 自定义活动编号 | `String` | `64` | `Y` | 已确认 | 示例值：ISFE00232 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_name` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.market_name` | 自定义活动名称 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_desc` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.market_desc` | 自定义活动描述 | `String` | `64` | `N` | 已确认 | 示例值：新店开业大促 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.start_time` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.start_time` | 活动开始时间 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20220909 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.end_time` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.end_time` | 活动结束时间 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20220911 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_debit_limit_amt` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.pos_debit_limit_amt` | pos借记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：2.00 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_credit_limit_amt` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.pos_credit_limit_amt` | pos贷记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_limit_amt` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.pos_limit_amt` | pos补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.qr_limit_amt` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.qr_limit_amt` | 扫码补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.total_limit_amt` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.total_limit_amt` | 活动总补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：10.00 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.status` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.status` | 活动是否有效 | `String` | `4` | `Y` | 已确认 | 1:生效 0：失效；示例值：1 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.human_flag` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.human_flag` | 是否人工操作 | `String` | `4` | `Y` | 已确认 | N：自动 Y：人工；示例值：Y |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.activity_id` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.activity_id` | 活动号 | `String` | `64` | `Y` | 已确认 | 示例值：223402342 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.activity_name` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.activity_name` | 活动描述 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.create_by` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.create_by` | 创建人 | `String` | `32` | `Y` | 已确认 | 示例值：Lg[官网示例已脱敏] |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.create_time` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.create_time` | 创建时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 22:00:30 |
| `async.forward.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.update_time` | `async.forward.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.update_time` | 更新时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 23:00:30 |
| `async.forward.resp_data.combinedpay_data[]` | `async.forward.resp_data` | `$.combinedpay_data（String(JSON Array) 容器）` | 补贴支付信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray字符串，参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| `async.forward.resp_data.combinedpay_data[].huifu_id` | `async.forward.resp_data` | `$.combinedpay_data => JSON decode => $[].huifu_id` | 补贴方汇付商户号 | `String` | `32` | `Y` | 已确认 | 补贴方汇付ID；示例值：[官网示例已脱敏] |
| `async.forward.resp_data.combinedpay_data[].user_type` | `async.forward.resp_data` | `$.combinedpay_data => JSON decode => $[].user_type` | 补贴方类型 | `String` | `32` | `Y` | 已确认 | 补贴方类型：channel-渠道，agent-代理；示例值：agent |
| `async.forward.resp_data.combinedpay_data[].acct_id` | `async.forward.resp_data` | `$.combinedpay_data => JSON decode => $[].acct_id` | 补贴方账户号 | `String` | `32` | `Y` | 已确认 | 营销补贴方账户号；示例值：F00900982 |
| `async.forward.resp_data.combinedpay_data[].amount` | `async.forward.resp_data` | `$.combinedpay_data => JSON decode => $[].amount` | 补贴金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； 示例值：1.01 |
| `async.forward.resp_data.combinedpay_data_fee_info` | `async.forward.resp_data` | `$.combinedpay_data_fee_info（String(JSON) 容器）` | 补贴支付手续费信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `async.forward.resp_data.combinedpay_data_fee_info.huifu_id` | `async.forward.resp_data` | `$.combinedpay_data_fee_info => JSON decode => $.huifu_id` | 补贴支付手续费承担方汇付编号 | `String` | `32` | `Y` | 已确认 | 补贴支付手续费承担方汇付编号；示例值：[官网示例已脱敏] |
| `async.forward.resp_data.combinedpay_data_fee_info.acct_id` | `async.forward.resp_data` | `$.combinedpay_data_fee_info => JSON decode => $.acct_id` | 补贴支付手续费承担方账户号 | `String` | `32` | `Y` | 已确认 | 补贴支付手续费承担方账户号；示例值：F00900982 |
| `async.forward.resp_data.combinedpay_data_fee_info.combinedpay_fee_amt` | `async.forward.resp_data` | `$.combinedpay_data_fee_info => JSON decode => $.combinedpay_fee_amt` | 补贴支付手续费金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； 示例值：1.01 |
| `async.forward.resp_data.debit_type` | `async.forward.resp_data` | `$.debit_type` | 借贷记标识 | `String` | `1` | `N` | 已确认 | D-借记卡，C-贷记卡，0-其他；示例值：D |
| `async.forward.resp_data.is_div` | `async.forward.resp_data` | `$.is_div` | 是否分账交易 | `String` | `1` | `Y` | 已确认 | 1:分账交易， 0:非分账交易；示例值：1 |
| `async.forward.resp_data.acct_split_bunch` | `async.forward.resp_data` | `$.acct_split_bunch` | 分账对象 | `Object` | `—` | `N` | N/A：结构字段长度 | jsonObject字符串 |
| `async.forward.resp_data.acct_split_bunch.acct_infos[]` | `async.forward.resp_data` | `$.acct_split_bunch.acct_infos[]` | 分账明细 | `Array` | `—` | `Y` | N/A：结构字段长度 | jsonArray分账明细 |
| `async.forward.resp_data.acct_split_bunch.acct_infos[].div_amt` | `async.forward.resp_data` | `$.acct_split_bunch.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 ，最低传入0.01 |
| `async.forward.resp_data.acct_split_bunch.acct_infos[].huifu_id` | `async.forward.resp_data` | `$.acct_split_bunch.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `async.forward.resp_data.acct_split_bunch.acct_infos[].acct_date` | `async.forward.resp_data` | `$.acct_split_bunch.acct_infos[].acct_date` | 账务日期 | `String` | `8` | `N` | 已确认 | 示例值：20220909 |
| `async.forward.resp_data.is_delay_acct` | `async.forward.resp_data` | `$.is_delay_acct` | 是否延时交易 | `String` | `1` | `Y` | 已确认 | 1:延迟， 0:非延迟；示例值：1 |
| `async.forward.resp_data.wx_user_id` | `async.forward.resp_data` | `$.wx_user_id` | 微信用户唯一标识码 | `String` | `128` | `N` | 已确认 | 示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk= |
| `async.forward.resp_data.wx_response` | `async.forward.resp_data` | `$.wx_response` | 微信返回的响应报文 | `Object` | `—` | `N` | N/A：结构字段长度 | jsonObject字符串 |
| `async.forward.resp_data.wx_response.sub_appid` | `async.forward.resp_data` | `$.wx_response.sub_appid` | 子商户公众账号ID | `String` | `32` | `N` | 已确认 | 微信分配的子商户公众账号ID；示例值：wxec280d4c8a1cc2ca |
| `async.forward.resp_data.wx_response.openid` | `async.forward.resp_data` | `$.wx_response.openid` | 用户标识 | `String` | `128` | `Y` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `async.forward.resp_data.wx_response.sub_openid` | `async.forward.resp_data` | `$.wx_response.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `async.forward.resp_data.wx_response.bank_type` | `async.forward.resp_data` | `$.wx_response.bank_type` | 付款银行 | `String` | `16` | `Y` | 已确认 | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/doc/v3/merchant/4012076355)；示例值：OTHERS |
| `async.forward.resp_data.wx_response.cash_fee` | `async.forward.resp_data` | `$.wx_response.cash_fee` | 现金支付金额 | `String` | `100` | `N` | 已确认 | 现金支付金额订单现金支付金额；示例值：10.00 |
| `async.forward.resp_data.wx_response.coupon_fee` | `async.forward.resp_data` | `$.wx_response.coupon_fee` | 代金券金额 | `String` | `100` | `N` | 已确认 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：0.10 |
| `async.forward.resp_data.wx_response.attach` | `async.forward.resp_data` | `$.wx_response.attach` | 商家数据包 | `String` | `128` | `N` | 已确认 | 商家数据包，原样返回；示例值：附加数据 |
| `async.forward.resp_data.wx_response.promotion_detail[]` | `async.forward.resp_data` | `$.wx_response.promotion_detail[]` | 营销详情列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 营销详情列表，使返回值为Json格式 |
| `async.forward.resp_data.wx_response.promotion_detail[].promotion_id` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].promotion_id` | 券id | `String` | `32` | `Y` | 已确认 | 券或者立减优惠id；示例值：2345234235 |
| `async.forward.resp_data.wx_response.promotion_detail[].name` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `async.forward.resp_data.wx_response.promotion_detail[].scope` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL: 全场代金券，SINGLE: 单品优惠；示例值：GLOBAL |
| `async.forward.resp_data.wx_response.promotion_detail[].type` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON: 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致） ；DISCOUNT: 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `async.forward.resp_data.wx_response.promotion_detail[].amount` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].amount` | 优惠券面额 | `String` | `12` | `Y` | 已确认 | 用户享受优惠的金额；（优惠券面额=微信出资金额+商家出资金额+其他出资方金额 ）示例值：5.00 |
| `async.forward.resp_data.wx_response.promotion_detail[].activity_id` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].activity_id` | 活动ID | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `async.forward.resp_data.wx_response.promotion_detail[].merchant_contribute` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].merchant_contribute` | 商户出资 | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；示例值：10.00 |
| `async.forward.resp_data.wx_response.promotion_detail[].other_contribute` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].other_contribute` | 其他出资 | `String` | `32` | `N` | 已确认 | 其他出资方出资金额=商家出资+微信出资，单位为元；示例值：20.00 |
| `async.forward.resp_data.wx_response.promotion_detail[].goods_detail[]` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].goods_detail[]` | 单品列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 单品信息，使用Json格式，是promotion_detail的元素 |
| `async.forward.resp_data.wx_response.promotion_detail[].goods_detail[].goods_id` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].goods_detail[].goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `async.forward.resp_data.wx_response.promotion_detail[].goods_detail[].goods_remark` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].goods_detail[].goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。；示例值：商品备注 |
| `async.forward.resp_data.wx_response.promotion_detail[].goods_detail[].discount_amount` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].goods_detail[].discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，单位为：元；示例值：20.00 |
| `async.forward.resp_data.wx_response.promotion_detail[].goods_detail[].quantity` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].goods_detail[].quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `async.forward.resp_data.wx_response.promotion_detail[].goods_detail[].price` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].goods_detail[].price` | 商品价格 | `String` | `32` | `Y` | 已确认 | 单位为:元。示例值：99.00；如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，；则活动商品的单价应为原单价-50元 |
| `async.forward.resp_data.wx_response.promotion_detail[].wxpay_contribute` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].wxpay_contribute` | 微信出资 | `String` | `32` | `N` | 已确认 | 特指由微信支付商户平台创建的优惠，单位：元；示例值：20.00 |
| `async.forward.resp_data.wx_response.promotion_detail[].original_other_contribute` | `async.forward.resp_data` | `$.wx_response.promotion_detail[].original_other_contribute` | 微信交易其他出资方出资金额 | `String` | `32` | `N` | 已确认 | 微信的其他出资方出资金额，单位：元；示例值：20.00 |
| `async.forward.resp_data.wx_response.sub_mch_id` | `async.forward.resp_data` | `$.wx_response.sub_mch_id` | 子商户号 | `String` | `—` | `N` | [需要官方确认]：长度 | 微信支付分配的子商户号；直联模式返回字段；示例值：1632157057 |
| `async.forward.resp_data.wx_response.device_info` | `async.forward.resp_data` | `$.wx_response.device_info` | 设备号 | `String` | `—` | `N` | [需要官方确认]：长度 | 调用接口提交的终端设备号；直联模式返回字段；示例值：SP003pcf |
| `async.forward.resp_data.wx_response.is_subscribe` | `async.forward.resp_data` | `$.wx_response.is_subscribe` | 是否关注公众账号 | `String` | `—` | `N` | [需要官方确认]：长度 | 用户是否关注公众账号，直联模式返回字段；Y-关注，N-未关注（机构商户不返回）；示例值：Y |
| `async.forward.resp_data.wx_response.sub_is_subscribe` | `async.forward.resp_data` | `$.wx_response.sub_is_subscribe` | 是否关注子公众账号 | `String` | `—` | `N` | [需要官方确认]：长度 | 用户是否关注子公众账号，直联模式返回字段；Y-关注，N-未关注（机构商户不返回）；示例值：Y |
| `async.forward.resp_data.wx_response.fee_type` | `async.forward.resp_data` | `$.wx_response.fee_type` | 现金支付货币类型 | `String` | `—` | `N` | [需要官方确认]：长度 | 符合ISO 4217标准的三位字母代码，默认人民币：CNY；直联模式返回字段；示例值：CNY |
| `async.forward.resp_data.wx_response.coupon_count` | `async.forward.resp_data` | `$.wx_response.coupon_count` | 代金券使用数量 | `String` | `—` | `N` | [需要官方确认]：长度 | 直联模式返回字段；示例值：1 ；使用单品优惠时不再返回coupon_count，参数promotion_detail会返回每张券的具体信息，；商户可以通过解析promotion_detail参数来确认使用了几张代金券。 |
| `async.forward.resp_data.alipay_response` | `async.forward.resp_data` | `$.alipay_response` | 支付宝返回的响应报文 | `Object` | `—` | `N` | N/A：结构字段长度 | jsonObject字符串 |
| `async.forward.resp_data.alipay_response.voucher_detail_list[]` | `async.forward.resp_data` | `$.alipay_response.voucher_detail_list[]` | 优惠券信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 本交易支付时使用的所有优惠券信息；示例值："[{\"id\":\"[官网示例已脱敏]X1M6V\",\"name\":\"全仓 5折优惠券\"}]" |
| `async.forward.resp_data.alipay_response.voucher_detail_list[].id` | `async.forward.resp_data` | `$.alipay_response.voucher_detail_list[].id` | 券id | `String` | `32` | `Y` | 已确认 | 示例值：6934572310301 |
| `async.forward.resp_data.alipay_response.voucher_detail_list[].name` | `async.forward.resp_data` | `$.alipay_response.voucher_detail_list[].name` | 券名称 | `String` | `32` | `Y` | 已确认 | 示例值：实体店付款通用立减券 |
| `async.forward.resp_data.alipay_response.voucher_detail_list[].type` | `async.forward.resp_data` | `$.alipay_response.voucher_detail_list[].type` | 券类型 | `String` | `32` | `Y` | 已确认 | 当前有三种类型：；ALIPAY_FIX_VOUCHER: 全场代金券；ALIPAY_DISCOUNT_VOUCHER: 折扣券；ALIPAY_ITEM_VOUCHER: 单品优惠 ；示例值：ALIPAY_ITEM_VOUCHER注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码 |
| `async.forward.resp_data.alipay_response.voucher_detail_list[].amount` | `async.forward.resp_data` | `$.alipay_response.voucher_detail_list[].amount` | 优惠券面额 | `String` | `12` | `Y` | 已确认 | 优惠券面额，它应该会等于商家出资加上其他出资方出资；示例值：10.00 |
| `async.forward.resp_data.alipay_response.voucher_detail_list[].merchant_contribute` | `async.forward.resp_data` | `$.alipay_response.voucher_detail_list[].merchant_contribute` | 商家出资 | `String` | `12` | `N` | 已确认 | 特指发起交易的商家出资金额；示例值：10.00 |
| `async.forward.resp_data.alipay_response.voucher_detail_list[].other_contribute` | `async.forward.resp_data` | `$.alipay_response.voucher_detail_list[].other_contribute` | 其他出资方出资金额 | `String` | `11` | `N` | 已确认 | 可能是支付宝，可能是品牌商，或者其他方，也可能是他们的一起出资；示例值：0.00 |
| `async.forward.resp_data.alipay_response.fund_bill_list[]` | `async.forward.resp_data` | `$.alipay_response.fund_bill_list[]` | 资金渠道 | `Array` | `—` | `N` | N/A：结构字段长度 | 支付成功的各个渠道金额信息。交易支付使用的资金渠道。只有在签约中指定需要返回资金明细，或者入参的query_options 中指定时才返回该字段信息。 |
| `async.forward.resp_data.alipay_response.fund_bill_list[].bank_code` | `async.forward.resp_data` | `$.alipay_response.fund_bill_list[].bank_code` | 银行卡支付时的银行代码 | `String` | `10` | `N` | 已确认 | 示例值：CEB |
| `async.forward.resp_data.alipay_response.fund_bill_list[].amount` | `async.forward.resp_data` | `$.alipay_response.fund_bill_list[].amount` | 该支付工具类型所使用的金额 | `String` | `32` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `async.forward.resp_data.alipay_response.fund_bill_list[].fund_channel` | `async.forward.resp_data` | `$.alipay_response.fund_bill_list[].fund_channel` | 交易使用的资金渠道 | `String` | `32` | `N` | 已确认 | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；示例值：ALIPAYACCOUNT |
| `async.forward.resp_data.alipay_response.fund_bill_list[].fund_type` | `async.forward.resp_data` | `$.alipay_response.fund_bill_list[].fund_type` | 渠道所使用的资金类型 | `String` | `32` | `N` | 已确认 | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。；DEBIT_CARD:借记卡，；CREDIT_CARD:信用卡，；MIXED_CARD:借贷合一卡；示例值：DEBIT_CARD |
| `async.forward.resp_data.alipay_response.fund_bill_list[].real_amount` | `async.forward.resp_data` | `$.alipay_response.fund_bill_list[].real_amount` | 渠道实际付款金额 | `String` | `11` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `async.forward.resp_data.alipay_response.buyer_id` | `async.forward.resp_data` | `$.alipay_response.buyer_id` | 买家的支付宝唯一用户号 | `String` | `28` | `N` | 已确认 | 买家的支付宝唯一用户号（2088开头的16位纯数字）；示例值：[官网示例已脱敏] |
| `async.forward.resp_data.alipay_response.buyer_logon_id` | `async.forward.resp_data` | `$.alipay_response.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com |
| `async.forward.resp_data.alipay_response.hb_fq_num` | `async.forward.resp_data` | `$.alipay_response.hb_fq_num` | 花呗分期数 | `String` | `10` | `N` | 已确认 | 示例值：3 |
| `async.forward.resp_data.alipay_response.hb_fq_seller_percent` | `async.forward.resp_data` | `$.alipay_response.hb_fq_seller_percent` | 卖家承担的手续费百分比 | `String` | `3` | `N` | 已确认 | 比例的百分值，示例值：0.9，传入100代表100% |
| `async.forward.resp_data.alipay_response.notify_time` | `async.forward.resp_data` | `$.alipay_response.notify_time` | 通知时间 | `String` | `—` | `N` | [需要官方确认]：长度 | 直连模式字段；通知的发送时间。格式为Date格式，yyyy-MM-dd HH:mm:ss；示例值2022-10-11 10:12:24 |
| `async.forward.resp_data.alipay_response.app_id` | `async.forward.resp_data` | `$.alipay_response.app_id` | 支付宝应用app_id | `String` | `32` | `N` | 已确认 | 直连模式字段；支付宝分配给开发者的应用Id；示例值：[官网示例已脱敏] |
| `async.forward.resp_data.alipay_response.out_biz_no` | `async.forward.resp_data` | `$.alipay_response.out_biz_no` | 商户业务号 | `String` | `64` | `N` | 已确认 | 直连模式字段；商户业务ID，主要是退款通知中返回退款申请的流水号；示例值： |
| `async.forward.resp_data.alipay_response.invoice_amount` | `async.forward.resp_data` | `$.alipay_response.invoice_amount` | 开票金额 | `String` | `11` | `N` | 已确认 | 直连模式字段；用户在交易中支付的可开发票的金额；示例值：100.00 |
| `async.forward.resp_data.alipay_response.buyer_pay_amount` | `async.forward.resp_data` | `$.alipay_response.buyer_pay_amount` | 付款金额 | `String` | `13` | `N` | 已确认 | 直连模式字段；用户在交易中支付的金额；示例值：100.00 |
| `async.forward.resp_data.alipay_response.subject` | `async.forward.resp_data` | `$.alipay_response.subject` | 订单标题 | `String` | `256` | `N` | 已确认 | 直连模式字段；商品的标题/交易标题/订单标题/订单关键字等，是请求时对应的参数，原样通知回来；示例值：红果奶茶 |
| `async.forward.resp_data.alipay_response.body` | `async.forward.resp_data` | `$.alipay_response.body` | 商品描述 | `String` | `128` | `N` | 已确认 | 直连模式字段；该订单的备注、描述、明细等。对应请求时的body参数，；原样通知回来；示例值：中杯 |
| `async.forward.resp_data.alipay_response.gmt_create` | `async.forward.resp_data` | `$.alipay_response.gmt_create` | 交易创建时间 | `String` | `64` | `N` | 已确认 | 直连模式字段；该笔交易创建的时间。格式为yyyy-MM-dd HH:mm:ss；示例值2022-10-11 10:12:24 |
| `async.forward.resp_data.dc_response` | `async.forward.resp_data` | `$.dc_response` | 数字货币返回的响应报文 | `Object` | `—` | `N` | N/A：结构字段长度 | jsonObject字符串 |
| `async.forward.resp_data.dc_response.merchant_id` | `async.forward.resp_data` | `$.dc_response.merchant_id` | 商户号 | `String` | `35` | `N` | 已确认 | 数字货币: 工行；示例值：S5088295305 |
| `async.forward.resp_data.dc_response.term_id` | `async.forward.resp_data` | `$.dc_response.term_id` | 终端号 | `String` | `32` | `N` | 已确认 | 数字货币: 工行；示例值：58000001 |
| `async.forward.resp_data.dc_response.trade_type` | `async.forward.resp_data` | `$.dc_response.trade_type` | 交易类型 | `String` | `16` | `N` | 已确认 | 数字货币: 工行；示例值：SCANPAY |
| `async.forward.resp_data.dc_response.custom_bank_code` | `async.forward.resp_data` | `$.dc_response.custom_bank_code` | 客户所属运营机构代码 | `String` | `14` | `N` | 已确认 | 数字货币: 工行；示例值： |
| `async.forward.resp_data.dc_response.custom_bank_name` | `async.forward.resp_data` | `$.dc_response.custom_bank_name` | 客户所属运营机构名称 | `String` | `70` | `N` | 已确认 | 数字货币: 工行；示例值： |
| `async.forward.resp_data.dc_response.openid` | `async.forward.resp_data` | `$.dc_response.openid` | 用户标识 | `String` | `64` | `N` | 已确认 | 数字货币: 工行；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `async.forward.resp_data.dc_response.sub_openid` | `async.forward.resp_data` | `$.dc_response.sub_openid` | 用户子标识 | `String` | `64` | `N` | 已确认 | 数字货币: 工行；示例值：oWNHX5RNaCUmZR |
| `async.forward.resp_data.dc_response.coupon_amount` | `async.forward.resp_data` | `$.dc_response.coupon_amount` | 代金券金额 | `String` | `14` | `N` | 已确认 | 数字货币: 工行;单位：元；示例值：0.01 |
| `async.forward.resp_data.dc_response.coupon_count` | `async.forward.resp_data` | `$.dc_response.coupon_count` | 代金券数量 | `String` | `3` | `N` | 已确认 | 数字货币: 工行；示例值：1 |
| `async.forward.resp_data.dc_response.coupon_list[]` | `async.forward.resp_data` | `$.dc_response.coupon_list[]` | 代金券集合 | `Array` | `—` | `N` | N/A：结构字段长度 | 数字货币: 工行；示例值：[{"coupon_type":"5","coupon_id":"2020060702001","coupon_amount":"50.00"}] |
| `async.forward.resp_data.dc_response.coupon_list[].coupon_id` | `async.forward.resp_data` | `$.dc_response.coupon_list[].coupon_id` | 代金券ID | `String` | `40` | `N` | 已确认 | 示例值：2020060702001 |
| `async.forward.resp_data.dc_response.coupon_list[].coupon_type` | `async.forward.resp_data` | `$.dc_response.coupon_list[].coupon_type` | 代金券类型 | `String` | `8` | `N` | 已确认 | 示例值：5 |
| `async.forward.resp_data.dc_response.coupon_list[].coupon_amount` | `async.forward.resp_data` | `$.dc_response.coupon_list[].coupon_amount` | 单个代金券支付金额 | `String` | `14` | `N` | 已确认 | 单个代金券支付金额，单位：元；示例值：50.00 |
| `async.forward.resp_data.dc_response.creditorWalletName` | `async.forward.resp_data` | `$.dc_response.creditorWalletName` | 收款钱包名称 | `String` | `60` | `N` | 已确认 | 数字货币: 邮储；示例值：上海汇涵信息科技服务有限公司 |
| `async.forward.resp_data.dc_response.creditorWalletId` | `async.forward.resp_data` | `$.dc_response.creditorWalletId` | 收款钱包ID | `String` | `68` | `N` | 已确认 | 数字货币: 邮储；示例值：002250******5081 |
| `async.forward.resp_data.dc_response.creditorWalletType` | `async.forward.resp_data` | `$.dc_response.creditorWalletType` | 收款钱包类型 | `String` | `4` | `N` | 已确认 | 数字货币: 邮储 ；收款钱包类型 ；WT01: 个人钱包 ；WT02: 子个人钱包 ；WT09: 对公钱包 ；WT10: 子对公钱包；示例值：WT09 |
| `async.forward.resp_data.dc_response.creditorWalletLevel` | `async.forward.resp_data` | `$.dc_response.creditorWalletLevel` | 收款钱包等级 | `String` | `4` | `N` | 已确认 | 数字货币: 邮储 ；收款钱包等级 ；WL01: 一类钱包 ；WL02: 二类钱包 ；WL03: 三类钱包 ；WL04: 四类钱包；示例值：WL01 |
| `async.forward.resp_data.dc_response.debtorWalletName` | `async.forward.resp_data` | `$.dc_response.debtorWalletName` | 付款钱包名称 | `String` | `60` | `N` | 已确认 | 数字货币: 邮储；示例值：我的钱包 |
| `async.forward.resp_data.dc_response.debtorWalletId` | `async.forward.resp_data` | `$.dc_response.debtorWalletId` | 付款钱包ID | `String` | `68` | `N` | 已确认 | 数字货币: 邮储；示例值：004100******0032 |
| `async.forward.resp_data.dc_response.debtorWalletType` | `async.forward.resp_data` | `$.dc_response.debtorWalletType` | 付款钱包类型 | `String` | `4` | `N` | 已确认 | 数字货币: 邮储 ；付款钱包类型 ；WT01: 个人钱包 ；WT02: 子个人钱包 ；WT09: 对公钱包 ；WT10: 子对公钱包；示例值：WT01 |
| `async.forward.resp_data.dc_response.debtorWalletLevel` | `async.forward.resp_data` | `$.dc_response.debtorWalletLevel` | 付款钱包等级 | `String` | `4` | `N` | 已确认 | 数字货币: 邮储 ；付款钱包等级 ；WL01: 一类钱包 ；WL02: 二类钱包 ；WL03: 三类钱包 ；WL04: 四类钱包；示例值：WL02 |
| `async.forward.resp_data.dc_response.debtorPartyIdentification` | `async.forward.resp_data` | `$.dc_response.debtorPartyIdentification` | 付款运营机构 | `String` | `14` | `N` | 已确认 | 数字货币: 邮储；示例值： |
| `async.forward.resp_data.dc_response.businessType` | `async.forward.resp_data` | `$.dc_response.businessType` | 支付类型 | `String` | `1` | `N` | 已确认 | 数字货币: 邮储；支付类型：O-本贷他，I-本贷本；示例值：O |
| `async.forward.resp_data.unionpay_response` | `async.forward.resp_data` | `$.unionpay_response` | 银联返回的响应报文 | `Object` | `—` | `N` | N/A：结构字段长度 | jsonObject字符串 |
| `async.forward.resp_data.unionpay_response.coupon_info[]` | `async.forward.resp_data` | `$.unionpay_response.coupon_info[]` | 银联优惠信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 银联使用优惠活动时出现，jsonArray格式 |
| `async.forward.resp_data.unionpay_response.coupon_info[].addnInfo` | `async.forward.resp_data` | `$.unionpay_response.coupon_info[].addnInfo` | 附加信息 | `String` | `100` | `N` | 已确认 | 内容自定义；示例值：附加信息 |
| `async.forward.resp_data.unionpay_response.coupon_info[].spnsrId` | `async.forward.resp_data` | `$.unionpay_response.coupon_info[].spnsrId` | 出资方 | `String` | `20` | `Y` | 已确认 | 00010000：银联出资；付款方作为出资方：填写8位付款方机构代码；商户作为出资方：填写15位商户代码；示例值：00010000 |
| `async.forward.resp_data.unionpay_response.coupon_info[].type` | `async.forward.resp_data` | `$.unionpay_response.coupon_info[].type` | 项目类型 | `String` | `4` | `Y` | 已确认 | DD01：随机立减；CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券；CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券；示例值：DD01 |
| `async.forward.resp_data.unionpay_response.coupon_info[].offstAmt` | `async.forward.resp_data` | `$.unionpay_response.coupon_info[].offstAmt` | 抵消交易金额 | `String` | `14` | `Y` | 已确认 | 不能为全0；示例值：1.00 |
| `async.forward.resp_data.unionpay_response.coupon_info[].id` | `async.forward.resp_data` | `$.unionpay_response.coupon_info[].id` | 项目编号 | `String` | `40` | `N` | 已确认 | 用于票券编号等，格式自定义；示例值：938434221 |
| `async.forward.resp_data.unionpay_response.coupon_info[].desc` | `async.forward.resp_data` | `$.unionpay_response.coupon_info[].desc` | 项目简称 | `String` | `40` | `N` | 已确认 | 优惠活动简称，可用于展示、打单等；示例值：中秋优惠促销 |
| `async.forward.resp_data.unionpay_response.acc_no` | `async.forward.resp_data` | `$.unionpay_response.acc_no` | 付款账号 | `String` | `40` | `N` | 已确认 | 付款方的卡号/账号/Token |
| `async.forward.resp_data.device_type` | `async.forward.resp_data` | `$.device_type` | 终端类型 | `String` | `2` | `N` | 已确认 | 01-智能POS；02-扫码POS；03-云音箱；04-台牌；05-云打印；06-扫脸设备；07-收银机；08-收银助手；09-传统POS；10-一体音箱；11-虚拟终端；示例值：01 |
| `async.forward.resp_data.mer_dev_location` | `async.forward.resp_data` | `$.mer_dev_location` | 商户终端定位 | `Object` | `—` | `N` | N/A：结构字段长度 | 商户终端定位信息，jsonObject字符串 |
| `async.forward.resp_data.mer_dev_location.terminal_ip` | `async.forward.resp_data` | `$.mer_dev_location.terminal_ip` | 交易设备IP | `String` | `64` | `N` | 已确认 | 绑卡设备（付款 APP） 所在的公网IP，可用于定位所属地区，不是 wifi 连接时的局域网 IP。；局域网 IP 包括：；A 类： 10.0.0.0-10.255.255.255；B 类： 172.16.0.0-172.31.255.255；C 类： 192.168.0.0-192.168.255.255；示例值：172.3.46.44 |
| `async.forward.resp_data.mer_dev_location.terminal_location` | `async.forward.resp_data` | `$.mer_dev_location.terminal_location` | 终端实时经纬度信息 | `String` | `32` | `N` | 已确认 | 设备（付款APP）GPS位置,格式为纬度/经度，+表示北纬、东经，-表示南纬、西经。；示例值：+37.12/-121.213 |
| `async.forward.resp_data.bank_message` | `async.forward.resp_data` | `$.bank_message` | 通道返回描述 | `String` | `200` | `N` | 已确认 | 示例值：成功[0000000] |
| `async.forward.resp_data.remark` | `async.forward.resp_data` | `$.remark` | 备注 | `String` | `255` | `N` | 已确认 | 原样返回；示例值：备注 |
| `async.forward.resp_data.fq_channels` | `async.forward.resp_data` | `$.fq_channels` | 分期资产方式 | `String` | `20` | `N` | 已确认 | 花呗分期功能，代表优先使用的资产类型；alipayfq_cc：表示信⽤卡分期。；示例值：alipayfq_cc |
| `async.forward.resp_data.notify_type` | `async.forward.resp_data` | `$.notify_type` | 通知类型 | `Integer` | `1` | `N` | 已确认 | 1：通道通知，2：账务通知；示例值：1 |
| `async.forward.resp_data.split_fee_info` | `async.forward.resp_data` | `$.split_fee_info` | 分账手续费信息 | `Object` | `—` | `N` | N/A：结构字段长度 | 分账手续费信息 |
| `async.forward.resp_data.split_fee_info.total_split_fee_amt` | `async.forward.resp_data` | `$.split_fee_info.total_split_fee_amt` | 分账手续费总金额(元) | `String` | `14` | `N` | 已确认 | 示例值：0.10 |
| `async.forward.resp_data.split_fee_info.split_fee_flag` | `async.forward.resp_data` | `$.split_fee_info.split_fee_flag` | 分账手续费扣款标志 | `Integer` | `1` | `Y` | 已确认 | 1: 外扣 2: 内扣；示例值：2 |
| `async.forward.resp_data.split_fee_info.split_fee_details[]` | `async.forward.resp_data` | `$.split_fee_info.split_fee_details[]` | 分账手续费信息 | `Array` | `—` | `Y` | N/A：结构字段长度 | 分账手续费信息 |
| `async.forward.resp_data.split_fee_info.split_fee_details[].split_fee_amt` | `async.forward.resp_data` | `$.split_fee_info.split_fee_details[].split_fee_amt` | 分账手续费金额(元) | `String` | `14` | `Y` | 已确认 | 示例值：0.10 |
| `async.forward.resp_data.split_fee_info.split_fee_details[].split_fee_huifu_id` | `async.forward.resp_data` | `$.split_fee_info.split_fee_details[].split_fee_huifu_id` | 分账手续费承担方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.forward.resp_data.split_fee_info.split_fee_details[].split_fee_acct_id` | `async.forward.resp_data` | `$.split_fee_info.split_fee_details[].split_fee_acct_id` | 分账手续费承担方账号 | `String` | `32` | `N` | 已确认 | 示例值：F00598600 |
| `async.forward.resp_data.atu_sub_mer_id` | `async.forward.resp_data` | `$.atu_sub_mer_id` | ATU真实商户号 | `String` | `32` | `N` | 已确认 | 示例值：411111141 |
| `async.forward.resp_data.devs_id` | `async.forward.resp_data` | `$.devs_id` | 汇付终端号 | `String` | `32` | `N` | 已确认 | 使用汇付机具交易时返回；示例值：[官网示例已脱敏] |
| `async.forward.resp_data.fund_freeze_stat` | `async.forward.resp_data` | `$.fund_freeze_stat` | 资金冻结状态 | `String` | `16` | `N` | 已确认 | FREEZE：冻结；UNFREEZE：解冻；示例值：UNFREEZE |

### 正扫解冻异步 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.forward.unfreeze.resp_code` | `async.forward.unfreeze.resp_code` | `—（直接 JSON 路径）` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/open/doc/api/#/smzf/api_jhfs?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81) |
| `async.forward.unfreeze.resp_desc` | `async.forward.unfreeze.resp_desc` | `—（直接 JSON 路径）` | 业务返回描述 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/open/doc/api/#/smzf/api_jhfs?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81) |
| `async.forward.unfreeze.hf_seq_id` | `async.forward.unfreeze.hf_seq_id` | `—（直接 JSON 路径）` | 交易的汇付全局流水号 | `String` | `40` | `Y` | 已确认 | 示例值：00470topo1A221019132207P068ac1362af00000 |
| `async.forward.unfreeze.req_seq_id` | `async.forward.unfreeze.req_seq_id` | `—（直接 JSON 路径）` | 交易请求流水号 | `String` | `128` | `Y` | 已确认 | 交易时传入，原样返回；示例值：rQ[官网示例已脱敏] |
| `async.forward.unfreeze.req_date` | `async.forward.unfreeze.req_date` | `—（直接 JSON 路径）` | 交易请求日期 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回,格式为yyyyMMdd，示例值：20091225 |
| `async.forward.unfreeze.huifu_id` | `async.forward.unfreeze.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.forward.unfreeze.notify_type` | `async.forward.unfreeze.notify_type` | `—（直接 JSON 路径）` | 通知类型 | `Integer` | `1` | `Y` | 已确认 | 3：资金解冻通知；示例值：3 |
| `async.forward.unfreeze.fund_freeze_stat` | `async.forward.unfreeze.fund_freeze_stat` | `—（直接 JSON 路径）` | 资金冻结状态 | `String` | `16` | `Y` | 已确认 | UNFREEZE：解冻；示例值：UNFREEZE |
| `async.forward.unfreeze.unfreeze_amt` | `async.forward.unfreeze.unfreeze_amt` | `—（直接 JSON 路径）` | 解冻金额 | `String` | `14` | `Y` | 已确认 | 单元：元。示例值：1.23 |
| `async.forward.unfreeze.freeze_time` | `async.forward.unfreeze.freeze_time` | `—（直接 JSON 路径）` | 冻结时间 | `String` | `14` | `Y` | 已确认 | 格式为yyyyMMddHHMMSS，示例值：20091225091010 |
| `async.forward.unfreeze.unfreeze_time` | `async.forward.unfreeze.unfreeze_time` | `—（直接 JSON 路径）` | 解冻时间 | `String` | `14` | `Y` | 已确认 | 格式为yyyyMMddHHMMSS，示例值：20091225091010 |

### 反扫异步信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.reverse.resp_code` | `async.reverse.resp_code` | `—（直接 JSON 路径）` | 网关返回码 | `String` | `8` | `Y` | 已确认 | 示例值：00000000 |
| `async.reverse.resp_desc` | `async.reverse.resp_desc` | `—（直接 JSON 路径）` | 网关返回信息 | `String` | `512` | `Y` | 已确认 | 示例值：交易成功[000] |
| `async.reverse.sign` | `async.reverse.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `async.reverse.resp_data` | `async.reverse.resp_data` | `—（String(JSON) 容器）` | 返回业务数据 | `String` | `—` | `Y` | [需要官方确认]：长度 | jsonObject |

### 反扫异步 resp_data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.reverse.resp_data.resp_code` | `async.reverse.resp_data` | `$.resp_code` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/lightning/api/jhzfxd.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `async.reverse.resp_data.resp_desc` | `async.reverse.resp_data` | `$.resp_desc` | 业务响应信息 | `String` | `256` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/lightning/api/jhzfxd.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `async.reverse.resp_data.huifu_id` | `async.reverse.resp_data` | `$.huifu_id` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.reverse.resp_data.req_seq_id` | `async.reverse.resp_data` | `$.req_seq_id` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 交易时传入，原样返回；示例值：rQ[官网示例已脱敏] |
| `async.reverse.resp_data.req_date` | `async.reverse.resp_data` | `$.req_date` | 请求日期 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回；示例值：20220905 |
| `async.reverse.resp_data.trans_type` | `async.reverse.resp_data` | `$.trans_type` | 交易类型 | `String` | `16` | `N` | 已确认 | T_MICROPAY: 微信反扫；A_MICROPAY: 支付宝反扫 ；U_MICROPAY: 银联二维码反扫 ；D_MICROPAY: 数字人民币反扫 ；示例值：T_MICROPAY |
| `async.reverse.resp_data.hf_seq_id` | `async.reverse.resp_data` | `$.hf_seq_id` | 全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00470topo1A221019132207P068ac1362af00000 |
| `async.reverse.resp_data.out_trans_id` | `async.reverse.resp_data` | `$.out_trans_id` | 用户账单上的交易订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.reverse.resp_data.party_order_id` | `async.reverse.resp_data` | `$.party_order_id` | 用户账单上的商户订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.reverse.resp_data.trans_amt` | `async.reverse.resp_data` | `$.trans_amt` | 交易金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `async.reverse.resp_data.pay_amt` | `async.reverse.resp_data` | `$.pay_amt` | 消费者实付金额 | `String` | `14` | `N` | 已确认 | 单位元， 示例值：1.00 |
| `async.reverse.resp_data.settlement_amt` | `async.reverse.resp_data` | `$.settlement_amt` | 结算金额(元) | `String` | `16` | `N` | 已确认 | 实际应结金额(订单金额扣除优惠金额后的值)，保留小数点后两位，示例值：1000.00 |
| `async.reverse.resp_data.end_time` | `async.reverse.resp_data` | `$.end_time` | 支付完成时间 | `String` | `14` | `N` | 已确认 | 格式yyyyMMddHHmmss，示例值：20091225091010 |
| `async.reverse.resp_data.acct_date` | `async.reverse.resp_data` | `$.acct_date` | 入账时间 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20091225 |
| `async.reverse.resp_data.trans_stat` | `async.reverse.resp_data` | `$.trans_stat` | 交易状态 | `String` | `1` | `N` | 已确认 | S：成功、F：失败，交易状态以此字段为准。示例值：S |
| `async.reverse.resp_data.fee_flag` | `async.reverse.resp_data` | `$.fee_flag` | 手续费扣款标志 | `Integer` | `1` | `N` | 已确认 | 1: 外扣，2: 内扣；示例值：2 |
| `async.reverse.resp_data.fee_formula_infos[]` | `async.reverse.resp_data` | `$.fee_formula_infos[]` | 手续费费率信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 交易成功时返回手续费费率信息 |
| `async.reverse.resp_data.fee_formula_infos[].fee_formula` | `async.reverse.resp_data` | `$.fee_formula_infos[].fee_formula` | 手续费计算公式 | `String` | `512` | `Y` | 已确认 | 示例值：AMT\*0.003 |
| `async.reverse.resp_data.fee_formula_infos[].fee_type` | `async.reverse.resp_data` | `$.fee_formula_infos[].fee_type` | 手续费类型 | `String` | `32` | `Y` | 已确认 | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；示例值：ACCT_FEE |
| `async.reverse.resp_data.fee_formula_infos[].huifu_id` | `async.reverse.resp_data` | `$.fee_formula_infos[].huifu_id` | 商户号 | `String` | `32` | `N` | 已确认 | 补贴支付账户补贴时，补贴账户的huifuId；示例值：[官网示例已脱敏] |
| `async.reverse.resp_data.fee_amount` | `async.reverse.resp_data` | `$.fee_amount` | 手续费金额 | `String` | `16` | `N` | 已确认 | 单位元，保留小数点后两位，示例值：1.00 |
| `async.reverse.resp_data.trans_fee_allowance_info` | `async.reverse.resp_data` | `$.trans_fee_allowance_info` | 手续费补贴信息 | `Object` | `—` | `N` | N/A：结构字段长度 | Json格式；参加银行补贴手续费 |
| `async.reverse.resp_data.trans_fee_allowance_info.receivable_fee_amt` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.receivable_fee_amt` | 商户应收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `async.reverse.resp_data.trans_fee_allowance_info.actual_fee_amt` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.actual_fee_amt` | 商户实收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `async.reverse.resp_data.trans_fee_allowance_info.allowance_fee_amt` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.allowance_fee_amt` | 补贴手续费 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `async.reverse.resp_data.trans_fee_allowance_info.allowance_type` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.allowance_type` | 补贴类型 | `String` | `10` | `N` | 已确认 | 0：不补贴，为空默认；1：补贴；2：部分补贴；3：全额补贴(优惠后)；4：部分补贴(优惠后)；示例值：2 |
| `async.reverse.resp_data.trans_fee_allowance_info.no_allowance_desc` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.no_allowance_desc` | 不补贴原因 | `String` | `128` | `N` | 已确认 | 1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴；2:额度用完；3:不在有效期；4:活动不存在；5:手续费金额为0不补贴；6:顶格优惠；7:额度不足；8:手续费后补；9:未达到起始补贴金额；示例值：2 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos` | 手续费补贴活动详情 | `Object` | `—` | `N` | N/A：结构字段长度 | 补贴系统返回，斗拱原样返回 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.acct_id` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.acct_id` | 门店 | `String` | `64` | `N` | 已确认 | 示例值：sh002 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.merchant_group` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.merchant_group` | 商户号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys` | 补贴方 | `String` | `64` | `Y` | 已确认 | 1:银行 2:服务商 3:汇来米；示例值：1 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys_id` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys_id` | 补贴方ID | `String` | `64` | `Y` | 已确认 | 对应补贴方的id；示例值：[官网示例已脱敏] |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.is_delay_allowance` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.is_delay_allowance` | 补贴类型 | `String` | `2` | `Y` | 已确认 | 1:实补,2:后补,默认实补；示例值：1 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_id` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.market_id` | 自定义活动编号 | `String` | `64` | `Y` | 已确认 | 示例值：ISFE00232 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_name` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.market_name` | 自定义活动名称 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_desc` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.market_desc` | 自定义活动描述 | `String` | `64` | `N` | 已确认 | 示例值：新店开业大促 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.start_time` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.start_time` | 活动开始时间 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20220909 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.end_time` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.end_time` | 活动结束时间 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20220911 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_debit_limit_amt` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.pos_debit_limit_amt` | pos借记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：2.00 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_credit_limit_amt` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.pos_credit_limit_amt` | pos贷记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_limit_amt` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.pos_limit_amt` | pos补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.qr_limit_amt` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.qr_limit_amt` | 扫码补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.total_limit_amt` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.total_limit_amt` | 活动总补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：10.00 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.status` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.status` | 活动是否有效 | `String` | `4` | `Y` | 已确认 | 1:生效 0：失效；示例值：1 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.human_flag` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.human_flag` | 是否人工操作 | `String` | `4` | `Y` | 已确认 | N：自动 Y：人工；示例值：Y |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.activity_id` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.activity_id` | 活动号 | `String` | `64` | `Y` | 已确认 | 示例值：223402342 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.activity_name` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.activity_name` | 活动描述 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.create_by` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.create_by` | 创建人 | `String` | `32` | `Y` | 已确认 | 示例值：Lg[官网示例已脱敏] |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.create_time` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.create_time` | 创建时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 22:00:30 |
| `async.reverse.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.update_time` | `async.reverse.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.update_time` | 更新时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 23:00:30 |
| `async.reverse.resp_data.combinedpay_data[]` | `async.reverse.resp_data` | `$.combinedpay_data（String(JSON Array) 容器）` | 补贴支付信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray字符串，参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| `async.reverse.resp_data.combinedpay_data[].huifu_id` | `async.reverse.resp_data` | `$.combinedpay_data => JSON decode => $[].huifu_id` | 补贴方汇付商户号 | `String` | `32` | `Y` | 已确认 | 补贴方汇付ID；示例值：[官网示例已脱敏] |
| `async.reverse.resp_data.combinedpay_data[].user_type` | `async.reverse.resp_data` | `$.combinedpay_data => JSON decode => $[].user_type` | 补贴方类型 | `String` | `32` | `Y` | 已确认 | 补贴方类型：channel-渠道，agent-代理；示例值：agent |
| `async.reverse.resp_data.combinedpay_data[].acct_id` | `async.reverse.resp_data` | `$.combinedpay_data => JSON decode => $[].acct_id` | 补贴方账户号 | `String` | `32` | `Y` | 已确认 | 营销补贴方账户号；示例值：F00900982 |
| `async.reverse.resp_data.combinedpay_data[].amount` | `async.reverse.resp_data` | `$.combinedpay_data => JSON decode => $[].amount` | 补贴金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； 示例值：1.01 |
| `async.reverse.resp_data.combinedpay_data_fee_info` | `async.reverse.resp_data` | `$.combinedpay_data_fee_info（String(JSON) 容器）` | 补贴支付手续费信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `async.reverse.resp_data.combinedpay_data_fee_info.huifu_id` | `async.reverse.resp_data` | `$.combinedpay_data_fee_info => JSON decode => $.huifu_id` | 补贴支付手续费承担方汇付编号 | `String` | `32` | `Y` | 已确认 | 补贴支付手续费承担方汇付编号；示例值：[官网示例已脱敏] |
| `async.reverse.resp_data.combinedpay_data_fee_info.acct_id` | `async.reverse.resp_data` | `$.combinedpay_data_fee_info => JSON decode => $.acct_id` | 补贴支付手续费承担方账户号 | `String` | `32` | `Y` | 已确认 | 补贴支付手续费承担方账户号；示例值：F00900982 |
| `async.reverse.resp_data.combinedpay_data_fee_info.combinedpay_fee_amt` | `async.reverse.resp_data` | `$.combinedpay_data_fee_info => JSON decode => $.combinedpay_fee_amt` | 补贴支付手续费金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； 示例值：1.01 |
| `async.reverse.resp_data.debit_type` | `async.reverse.resp_data` | `$.debit_type` | 借贷记标识 | `String` | `1` | `N` | 已确认 | D-借记卡，C-贷记卡，0-其他；示例值：D |
| `async.reverse.resp_data.is_div` | `async.reverse.resp_data` | `$.is_div` | 是否分账交易 | `String` | `1` | `Y` | 已确认 | 1:分账交易， 0:非分账交易；示例值：1 |
| `async.reverse.resp_data.acct_split_bunch` | `async.reverse.resp_data` | `$.acct_split_bunch` | 分账对象 | `Object` | `—` | `N` | N/A：结构字段长度 | jsonObject字符串 |
| `async.reverse.resp_data.acct_split_bunch.acct_infos[]` | `async.reverse.resp_data` | `$.acct_split_bunch.acct_infos[]` | 分账明细 | `Array` | `—` | `Y` | N/A：结构字段长度 | jsonArray分账明细 |
| `async.reverse.resp_data.acct_split_bunch.acct_infos[].div_amt` | `async.reverse.resp_data` | `$.acct_split_bunch.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 ，最低传入0.01 |
| `async.reverse.resp_data.acct_split_bunch.acct_infos[].huifu_id` | `async.reverse.resp_data` | `$.acct_split_bunch.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `async.reverse.resp_data.acct_split_bunch.acct_infos[].acct_date` | `async.reverse.resp_data` | `$.acct_split_bunch.acct_infos[].acct_date` | 账务日期 | `String` | `8` | `N` | 已确认 | 示例值：20220909 |
| `async.reverse.resp_data.is_delay_acct` | `async.reverse.resp_data` | `$.is_delay_acct` | 是否延时交易 | `String` | `1` | `Y` | 已确认 | 1:延迟， 0:非延迟；示例值：1 |
| `async.reverse.resp_data.wx_user_id` | `async.reverse.resp_data` | `$.wx_user_id` | 微信用户唯一标识码 | `String` | `128` | `N` | 已确认 | 示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk= |
| `async.reverse.resp_data.wx_response` | `async.reverse.resp_data` | `$.wx_response` | 微信返回的响应报文 | `Object` | `—` | `N` | N/A：结构字段长度 | jsonObject字符串 |
| `async.reverse.resp_data.wx_response.sub_appid` | `async.reverse.resp_data` | `$.wx_response.sub_appid` | 子商户公众账号ID | `String` | `32` | `N` | 已确认 | 微信分配的子商户公众账号ID；示例值：wxec280d4c8a1cc2ca |
| `async.reverse.resp_data.wx_response.openid` | `async.reverse.resp_data` | `$.wx_response.openid` | 用户标识 | `String` | `128` | `Y` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `async.reverse.resp_data.wx_response.sub_openid` | `async.reverse.resp_data` | `$.wx_response.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `async.reverse.resp_data.wx_response.bank_type` | `async.reverse.resp_data` | `$.wx_response.bank_type` | 付款银行 | `String` | `16` | `Y` | 已确认 | 银行类型，采用字符串类型的银行标识，银行类型见[微信银行类型说明](https://pay.weixin.qq.com/doc/v3/merchant/4012076355)；示例值：ICBC_DEBIT |
| `async.reverse.resp_data.wx_response.cash_fee` | `async.reverse.resp_data` | `$.wx_response.cash_fee` | 现金支付金额 | `String` | `100` | `N` | 已确认 | 现金支付金额订单现金支付金额；示例值：10.00 |
| `async.reverse.resp_data.wx_response.coupon_fee` | `async.reverse.resp_data` | `$.wx_response.coupon_fee` | 代金券金额 | `String` | `100` | `N` | 已确认 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：0.10 |
| `async.reverse.resp_data.wx_response.attach` | `async.reverse.resp_data` | `$.wx_response.attach` | 商家数据包 | `String` | `128` | `N` | 已确认 | 商家数据包，原样返回；示例值：附加数据 |
| `async.reverse.resp_data.wx_response.promotion_detail[]` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[]` | 营销详情列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 营销详情列表，使返回值为Json格式 |
| `async.reverse.resp_data.wx_response.promotion_detail[].promotion_id` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].promotion_id` | 券id | `String` | `32` | `Y` | 已确认 | 券或者立减优惠id；示例值：2345234235 |
| `async.reverse.resp_data.wx_response.promotion_detail[].name` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `async.reverse.resp_data.wx_response.promotion_detail[].scope` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL: 全场代金券，SINGLE: 单品优惠；示例值：GLOBAL |
| `async.reverse.resp_data.wx_response.promotion_detail[].type` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON: 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致） ；DISCOUNT: 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `async.reverse.resp_data.wx_response.promotion_detail[].amount` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].amount` | 优惠券面额 | `String` | `12` | `Y` | 已确认 | 用户享受优惠的金额；（优惠券面额=微信出资金额+商家出资金额+其他出资方金额 ）示例值：5.00 |
| `async.reverse.resp_data.wx_response.promotion_detail[].activity_id` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].activity_id` | 活动ID | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `async.reverse.resp_data.wx_response.promotion_detail[].merchant_contribute` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].merchant_contribute` | 商户出资 | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；示例值：10.00 |
| `async.reverse.resp_data.wx_response.promotion_detail[].other_contribute` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].other_contribute` | 其他出资 | `String` | `32` | `N` | 已确认 | 其他出资方出资金额=商家出资+微信出资，单位为元；示例值：20.00 |
| `async.reverse.resp_data.wx_response.promotion_detail[].goods_detail[]` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].goods_detail[]` | 单品列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 单品信息，使用Json格式，是promotion_detail的元素 |
| `async.reverse.resp_data.wx_response.promotion_detail[].goods_detail[].goods_id` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].goods_detail[].goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `async.reverse.resp_data.wx_response.promotion_detail[].goods_detail[].goods_remark` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].goods_detail[].goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。；示例值：商品备注 |
| `async.reverse.resp_data.wx_response.promotion_detail[].goods_detail[].discount_amount` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].goods_detail[].discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，单位为：元；示例值：20.00 |
| `async.reverse.resp_data.wx_response.promotion_detail[].goods_detail[].quantity` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].goods_detail[].quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `async.reverse.resp_data.wx_response.promotion_detail[].goods_detail[].price` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].goods_detail[].price` | 商品价格 | `String` | `32` | `Y` | 已确认 | 单位为:元。示例值：99.00；如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，；则活动商品的单价应为原单价-50元 |
| `async.reverse.resp_data.wx_response.promotion_detail[].wxpay_contribute` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].wxpay_contribute` | 微信出资 | `String` | `32` | `N` | 已确认 | 特指由微信支付商户平台创建的优惠，单位：元；示例值：20.00 |
| `async.reverse.resp_data.wx_response.promotion_detail[].original_other_contribute` | `async.reverse.resp_data` | `$.wx_response.promotion_detail[].original_other_contribute` | 微信交易其他出资方出资金额 | `String` | `32` | `N` | 已确认 | 微信的其他出资方出资金额，单位：元；示例值：20.00 |
| `async.reverse.resp_data.wx_response.sub_mch_id` | `async.reverse.resp_data` | `$.wx_response.sub_mch_id` | 子商户号 | `String` | `—` | `N` | [需要官方确认]：长度 | 微信支付分配的子商户号；直联模式返回字段；示例值：1632157057 |
| `async.reverse.resp_data.wx_response.device_info` | `async.reverse.resp_data` | `$.wx_response.device_info` | 设备号 | `String` | `—` | `N` | [需要官方确认]：长度 | 调用接口提交的终端设备号；直联模式返回字段；示例值：SP003pcf |
| `async.reverse.resp_data.wx_response.is_subscribe` | `async.reverse.resp_data` | `$.wx_response.is_subscribe` | 是否关注公众账号 | `String` | `—` | `N` | [需要官方确认]：长度 | 用户是否关注公众账号，直联模式返回字段；Y-关注，N-未关注（机构商户不返回）；示例值：Y |
| `async.reverse.resp_data.wx_response.sub_is_subscribe` | `async.reverse.resp_data` | `$.wx_response.sub_is_subscribe` | 是否关注子公众账号 | `String` | `—` | `N` | [需要官方确认]：长度 | 用户是否关注子公众账号，直联模式返回字段；Y-关注，N-未关注（机构商户不返回）；示例值：Y |
| `async.reverse.resp_data.wx_response.fee_type` | `async.reverse.resp_data` | `$.wx_response.fee_type` | 现金支付货币类型 | `String` | `—` | `N` | [需要官方确认]：长度 | 符合ISO 4217标准的三位字母代码，默认人民币：CNY；直联模式返回字段；示例值：CNY |
| `async.reverse.resp_data.wx_response.coupon_count` | `async.reverse.resp_data` | `$.wx_response.coupon_count` | 代金券使用数量 | `String` | `—` | `N` | [需要官方确认]：长度 | 直联模式返回字段；示例值：1 ；使用单品优惠时不再返回coupon_count，参数promotion_detail会返回每张券的具体信息，；商户可以通过解析promotion_detail参数来确认使用了几张代金券。 |
| `async.reverse.resp_data.alipay_response` | `async.reverse.resp_data` | `$.alipay_response` | 支付宝返回的响应报文 | `Object` | `—` | `N` | N/A：结构字段长度 | jsonObject字符串 |
| `async.reverse.resp_data.alipay_response.voucher_detail_list[]` | `async.reverse.resp_data` | `$.alipay_response.voucher_detail_list[]` | 优惠券信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 本交易支付时使用的所有优惠券信息；示例值："[{\"id\":\"[官网示例已脱敏]X1M6V\",\"name\":\"全仓 5折优惠券\"}]" |
| `async.reverse.resp_data.alipay_response.voucher_detail_list[].id` | `async.reverse.resp_data` | `$.alipay_response.voucher_detail_list[].id` | 券id | `String` | `32` | `Y` | 已确认 | 示例值：6934572310301 |
| `async.reverse.resp_data.alipay_response.voucher_detail_list[].name` | `async.reverse.resp_data` | `$.alipay_response.voucher_detail_list[].name` | 券名称 | `String` | `32` | `Y` | 已确认 | 示例值：实体店付款通用立减券 |
| `async.reverse.resp_data.alipay_response.voucher_detail_list[].type` | `async.reverse.resp_data` | `$.alipay_response.voucher_detail_list[].type` | 券类型 | `String` | `32` | `Y` | 已确认 | 当前有三种类型：；ALIPAY_FIX_VOUCHER: 全场代金券；ALIPAY_DISCOUNT_VOUCHER: 折扣券；ALIPAY_ITEM_VOUCHER: 单品优惠 ；示例值：ALIPAY_ITEM_VOUCHER注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码 |
| `async.reverse.resp_data.alipay_response.voucher_detail_list[].amount` | `async.reverse.resp_data` | `$.alipay_response.voucher_detail_list[].amount` | 优惠券面额 | `String` | `12` | `Y` | 已确认 | 优惠券面额，它应该会等于商家出资加上其他出资方出资；示例值：10.00 |
| `async.reverse.resp_data.alipay_response.voucher_detail_list[].merchant_contribute` | `async.reverse.resp_data` | `$.alipay_response.voucher_detail_list[].merchant_contribute` | 商家出资 | `String` | `12` | `N` | 已确认 | 特指发起交易的商家出资金额；示例值：10.00 |
| `async.reverse.resp_data.alipay_response.voucher_detail_list[].other_contribute` | `async.reverse.resp_data` | `$.alipay_response.voucher_detail_list[].other_contribute` | 其他出资方出资金额 | `String` | `11` | `N` | 已确认 | 可能是支付宝，可能是品牌商，或者其他方，也可能是他们的一起出资；示例值：0.00 |
| `async.reverse.resp_data.alipay_response.fund_bill_list[]` | `async.reverse.resp_data` | `$.alipay_response.fund_bill_list[]` | 资金渠道 | `Array` | `—` | `N` | N/A：结构字段长度 | 支付成功的各个渠道金额信息。交易支付使用的资金渠道。只有在签约中指定需要返回资金明细，或者入参的query_options 中指定时才返回该字段信息。 |
| `async.reverse.resp_data.alipay_response.fund_bill_list[].bank_code` | `async.reverse.resp_data` | `$.alipay_response.fund_bill_list[].bank_code` | 银行卡支付时的银行代码 | `String` | `10` | `N` | 已确认 | 示例值：CEB |
| `async.reverse.resp_data.alipay_response.fund_bill_list[].amount` | `async.reverse.resp_data` | `$.alipay_response.fund_bill_list[].amount` | 该支付工具类型所使用的金额 | `String` | `32` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `async.reverse.resp_data.alipay_response.fund_bill_list[].fund_channel` | `async.reverse.resp_data` | `$.alipay_response.fund_bill_list[].fund_channel` | 交易使用的资金渠道 | `String` | `32` | `N` | 已确认 | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；示例值：ALIPAYACCOUNT |
| `async.reverse.resp_data.alipay_response.fund_bill_list[].fund_type` | `async.reverse.resp_data` | `$.alipay_response.fund_bill_list[].fund_type` | 渠道所使用的资金类型 | `String` | `32` | `N` | 已确认 | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。；DEBIT_CARD:借记卡，；CREDIT_CARD:信用卡，；MIXED_CARD:借贷合一卡；示例值：DEBIT_CARD |
| `async.reverse.resp_data.alipay_response.fund_bill_list[].real_amount` | `async.reverse.resp_data` | `$.alipay_response.fund_bill_list[].real_amount` | 渠道实际付款金额 | `String` | `11` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `async.reverse.resp_data.alipay_response.buyer_id` | `async.reverse.resp_data` | `$.alipay_response.buyer_id` | 买家的支付宝唯一用户号 | `String` | `28` | `N` | 已确认 | 买家的支付宝唯一用户号（2088开头的16位纯数字）；示例值：[官网示例已脱敏] |
| `async.reverse.resp_data.alipay_response.buyer_logon_id` | `async.reverse.resp_data` | `$.alipay_response.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com |
| `async.reverse.resp_data.alipay_response.hb_fq_num` | `async.reverse.resp_data` | `$.alipay_response.hb_fq_num` | 花呗分期数 | `String` | `10` | `N` | 已确认 | 示例值：3 |
| `async.reverse.resp_data.alipay_response.hb_fq_seller_percent` | `async.reverse.resp_data` | `$.alipay_response.hb_fq_seller_percent` | 卖家承担的手续费百分比 | `String` | `3` | `N` | 已确认 | 比例的百分值，示例值：0.9，传入100代表100% |
| `async.reverse.resp_data.alipay_response.notify_time` | `async.reverse.resp_data` | `$.alipay_response.notify_time` | 通知时间 | `String` | `—` | `N` | [需要官方确认]：长度 | 直连模式字段；通知的发送时间。格式为Date格式，yyyy-MM-dd HH:mm:ss；示例值2022-10-11 10:12:24 |
| `async.reverse.resp_data.alipay_response.app_id` | `async.reverse.resp_data` | `$.alipay_response.app_id` | 支付宝应用app_id | `String` | `32` | `N` | 已确认 | 直连模式字段；支付宝分配给开发者的应用Id；示例值：[官网示例已脱敏] |
| `async.reverse.resp_data.alipay_response.out_biz_no` | `async.reverse.resp_data` | `$.alipay_response.out_biz_no` | 商户业务号 | `String` | `64` | `N` | 已确认 | 直连模式字段；商户业务ID，主要是退款通知中返回退款申请的流水号；示例值： |
| `async.reverse.resp_data.alipay_response.invoice_amount` | `async.reverse.resp_data` | `$.alipay_response.invoice_amount` | 开票金额 | `String` | `11` | `N` | 已确认 | 直连模式字段；用户在交易中支付的可开发票的金额；示例值：100.00 |
| `async.reverse.resp_data.alipay_response.buyer_pay_amount` | `async.reverse.resp_data` | `$.alipay_response.buyer_pay_amount` | 付款金额 | `String` | `13` | `N` | 已确认 | 直连模式字段；用户在交易中支付的金额；示例值：100.00 |
| `async.reverse.resp_data.alipay_response.subject` | `async.reverse.resp_data` | `$.alipay_response.subject` | 订单标题 | `String` | `256` | `N` | 已确认 | 直连模式字段；商品的标题/交易标题/订单标题/订单关键字等，是请求时对应的参数，原样通知回来；示例值：红果奶茶 |
| `async.reverse.resp_data.alipay_response.body` | `async.reverse.resp_data` | `$.alipay_response.body` | 商品描述 | `String` | `128` | `N` | 已确认 | 直连模式字段；该订单的备注、描述、明细等。对应请求时的body参数，；原样通知回来；示例值：中杯 |
| `async.reverse.resp_data.alipay_response.gmt_create` | `async.reverse.resp_data` | `$.alipay_response.gmt_create` | 交易创建时间 | `String` | `64` | `N` | 已确认 | 直连模式字段；该笔交易创建的时间。格式为yyyy-MM-dd HH:mm:ss；示例值2022-10-11 10:12:24 |
| `async.reverse.resp_data.dc_response` | `async.reverse.resp_data` | `$.dc_response` | 数字货币返回的响应报文 | `Object` | `—` | `N` | N/A：结构字段长度 | jsonObject字符串 |
| `async.reverse.resp_data.dc_response.merchant_id` | `async.reverse.resp_data` | `$.dc_response.merchant_id` | 商户号 | `String` | `35` | `N` | 已确认 | 数字货币: 工行；示例值：S5088295305 |
| `async.reverse.resp_data.dc_response.term_id` | `async.reverse.resp_data` | `$.dc_response.term_id` | 终端号 | `String` | `32` | `N` | 已确认 | 数字货币: 工行；示例值：58000001 |
| `async.reverse.resp_data.dc_response.trade_type` | `async.reverse.resp_data` | `$.dc_response.trade_type` | 交易类型 | `String` | `16` | `N` | 已确认 | 数字货币: 工行；示例值：SCANPAY |
| `async.reverse.resp_data.dc_response.custom_bank_code` | `async.reverse.resp_data` | `$.dc_response.custom_bank_code` | 客户所属运营机构代码 | `String` | `14` | `N` | 已确认 | 数字货币: 工行；示例值： |
| `async.reverse.resp_data.dc_response.custom_bank_name` | `async.reverse.resp_data` | `$.dc_response.custom_bank_name` | 客户所属运营机构名称 | `String` | `70` | `N` | 已确认 | 数字货币: 工行；示例值： |
| `async.reverse.resp_data.dc_response.openid` | `async.reverse.resp_data` | `$.dc_response.openid` | 用户标识 | `String` | `64` | `N` | 已确认 | 数字货币: 工行；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `async.reverse.resp_data.dc_response.sub_openid` | `async.reverse.resp_data` | `$.dc_response.sub_openid` | 用户子标识 | `String` | `64` | `N` | 已确认 | 数字货币: 工行；示例值：oWNHX5RNaCUmZR |
| `async.reverse.resp_data.dc_response.coupon_amount` | `async.reverse.resp_data` | `$.dc_response.coupon_amount` | 代金券金额 | `String` | `14` | `N` | 已确认 | 数字货币: 工行;单位：元；示例值：0.01 |
| `async.reverse.resp_data.dc_response.coupon_count` | `async.reverse.resp_data` | `$.dc_response.coupon_count` | 代金券数量 | `String` | `3` | `N` | 已确认 | 数字货币: 工行；示例值：1 |
| `async.reverse.resp_data.dc_response.coupon_list[]` | `async.reverse.resp_data` | `$.dc_response.coupon_list[]` | 代金券集合 | `Array` | `—` | `N` | N/A：结构字段长度 | 数字货币: 工行；示例值：[{"coupon_type":"5","coupon_id":"2020060702001","coupon_amount":"50.00"}] |
| `async.reverse.resp_data.dc_response.coupon_list[].coupon_id` | `async.reverse.resp_data` | `$.dc_response.coupon_list[].coupon_id` | 代金券ID | `String` | `40` | `N` | 已确认 | 示例值：2020060702001 |
| `async.reverse.resp_data.dc_response.coupon_list[].coupon_type` | `async.reverse.resp_data` | `$.dc_response.coupon_list[].coupon_type` | 代金券类型 | `String` | `8` | `N` | 已确认 | 示例值：5 |
| `async.reverse.resp_data.dc_response.coupon_list[].coupon_amount` | `async.reverse.resp_data` | `$.dc_response.coupon_list[].coupon_amount` | 单个代金券支付金额 | `String` | `14` | `N` | 已确认 | 单个代金券支付金额，单位：元；示例值：50.00 |
| `async.reverse.resp_data.dc_response.creditorWalletName` | `async.reverse.resp_data` | `$.dc_response.creditorWalletName` | 收款钱包名称 | `String` | `60` | `N` | 已确认 | 数字货币: 邮储；示例值：上海汇涵信息科技服务有限公司 |
| `async.reverse.resp_data.dc_response.creditorWalletId` | `async.reverse.resp_data` | `$.dc_response.creditorWalletId` | 收款钱包ID | `String` | `68` | `N` | 已确认 | 数字货币: 邮储；示例值：002250******5081 |
| `async.reverse.resp_data.dc_response.creditorWalletType` | `async.reverse.resp_data` | `$.dc_response.creditorWalletType` | 收款钱包类型 | `String` | `4` | `N` | 已确认 | 数字货币: 邮储 ；收款钱包类型 ；WT01: 个人钱包 ；WT02: 子个人钱包 ；WT09: 对公钱包 ；WT10: 子对公钱包；示例值：WT09 |
| `async.reverse.resp_data.dc_response.creditorWalletLevel` | `async.reverse.resp_data` | `$.dc_response.creditorWalletLevel` | 收款钱包等级 | `String` | `4` | `N` | 已确认 | 数字货币: 邮储 ；收款钱包等级 ；WL01: 一类钱包 ；WL02: 二类钱包 ；WL03: 三类钱包 ；WL04: 四类钱包；示例值：WL01 |
| `async.reverse.resp_data.dc_response.debtorWalletName` | `async.reverse.resp_data` | `$.dc_response.debtorWalletName` | 付款钱包名称 | `String` | `60` | `N` | 已确认 | 数字货币: 邮储；示例值：我的钱包 |
| `async.reverse.resp_data.dc_response.debtorWalletId` | `async.reverse.resp_data` | `$.dc_response.debtorWalletId` | 付款钱包ID | `String` | `68` | `N` | 已确认 | 数字货币: 邮储；示例值：004100******0032 |
| `async.reverse.resp_data.dc_response.debtorWalletType` | `async.reverse.resp_data` | `$.dc_response.debtorWalletType` | 付款钱包类型 | `String` | `4` | `N` | 已确认 | 数字货币: 邮储 ；付款钱包类型 ；WT01: 个人钱包 ；WT02: 子个人钱包 ；WT09: 对公钱包 ；WT10: 子对公钱包；示例值：WT01 |
| `async.reverse.resp_data.dc_response.debtorWalletLevel` | `async.reverse.resp_data` | `$.dc_response.debtorWalletLevel` | 付款钱包等级 | `String` | `4` | `N` | 已确认 | 数字货币: 邮储 ；付款钱包等级 ；WL01: 一类钱包 ；WL02: 二类钱包 ；WL03: 三类钱包 ；WL04: 四类钱包；示例值：WL02 |
| `async.reverse.resp_data.dc_response.debtorPartyIdentification` | `async.reverse.resp_data` | `$.dc_response.debtorPartyIdentification` | 付款运营机构 | `String` | `14` | `N` | 已确认 | 数字货币: 邮储；示例值： |
| `async.reverse.resp_data.dc_response.businessType` | `async.reverse.resp_data` | `$.dc_response.businessType` | 支付类型 | `String` | `1` | `N` | 已确认 | 数字货币: 邮储；支付类型：O-本贷他，I-本贷本；示例值：O |
| `async.reverse.resp_data.unionpay_response` | `async.reverse.resp_data` | `$.unionpay_response` | 银联返回的响应报文 | `Object` | `—` | `N` | N/A：结构字段长度 | jsonObject字符串 |
| `async.reverse.resp_data.unionpay_response.coupon_info[]` | `async.reverse.resp_data` | `$.unionpay_response.coupon_info[]` | 银联优惠信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 银联使用优惠活动时出现，jsonArray格式 |
| `async.reverse.resp_data.unionpay_response.coupon_info[].addnInfo` | `async.reverse.resp_data` | `$.unionpay_response.coupon_info[].addnInfo` | 附加信息 | `String` | `100` | `N` | 已确认 | 内容自定义；示例值：附加信息 |
| `async.reverse.resp_data.unionpay_response.coupon_info[].spnsrId` | `async.reverse.resp_data` | `$.unionpay_response.coupon_info[].spnsrId` | 出资方 | `String` | `20` | `Y` | 已确认 | 00010000：银联出资；付款方作为出资方：填写8位付款方机构代码；商户作为出资方：填写15位商户代码；示例值：00010000 |
| `async.reverse.resp_data.unionpay_response.coupon_info[].type` | `async.reverse.resp_data` | `$.unionpay_response.coupon_info[].type` | 项目类型 | `String` | `4` | `Y` | 已确认 | DD01：随机立减；CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券；CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券；示例值：DD01 |
| `async.reverse.resp_data.unionpay_response.coupon_info[].offstAmt` | `async.reverse.resp_data` | `$.unionpay_response.coupon_info[].offstAmt` | 抵消交易金额 | `String` | `14` | `Y` | 已确认 | 不能为全0；示例值：1.00 |
| `async.reverse.resp_data.unionpay_response.coupon_info[].id` | `async.reverse.resp_data` | `$.unionpay_response.coupon_info[].id` | 项目编号 | `String` | `40` | `N` | 已确认 | 用于票券编号等，格式自定义；示例值：938434221 |
| `async.reverse.resp_data.unionpay_response.coupon_info[].desc` | `async.reverse.resp_data` | `$.unionpay_response.coupon_info[].desc` | 项目简称 | `String` | `40` | `N` | 已确认 | 优惠活动简称，可用于展示、打单等；示例值：中秋优惠促销 |
| `async.reverse.resp_data.unionpay_response.acc_no` | `async.reverse.resp_data` | `$.unionpay_response.acc_no` | 付款账号 | `String` | `40` | `N` | 已确认 | 付款方的卡号/账号/Token |
| `async.reverse.resp_data.device_type` | `async.reverse.resp_data` | `$.device_type` | 终端类型 | `String` | `2` | `N` | 已确认 | 01-智能POS；02-扫码POS；03-云音箱；04-台牌；05-云打印；06-扫脸设备；07-收银机；08-收银助手；09-传统POS；10-一体音箱；11-虚拟终端；示例值：01 |
| `async.reverse.resp_data.mer_dev_location` | `async.reverse.resp_data` | `$.mer_dev_location` | 商户终端定位 | `Object` | `—` | `N` | N/A：结构字段长度 | 商户终端定位信息，jsonObject字符串 |
| `async.reverse.resp_data.mer_dev_location.terminal_ip` | `async.reverse.resp_data` | `$.mer_dev_location.terminal_ip` | 交易设备IP | `String` | `64` | `N` | 已确认 | 绑卡设备（付款 APP） 所在的公网IP，可用于定位所属地区，不是 wifi 连接时的局域网 IP。；局域网 IP 包括：；A 类： 10.0.0.0-10.255.255.255；B 类： 172.16.0.0-172.31.255.255；C 类： 192.168.0.0-192.168.255.255；示例值：172.3.46.44 |
| `async.reverse.resp_data.mer_dev_location.terminal_location` | `async.reverse.resp_data` | `$.mer_dev_location.terminal_location` | 终端实时经纬度信息 | `String` | `32` | `N` | 已确认 | 设备（付款APP）GPS位置,格式为纬度/经度，+表示北纬、东经，-表示南纬、西经。；示例值：+37.12/-121.213 |
| `async.reverse.resp_data.bank_message` | `async.reverse.resp_data` | `$.bank_message` | 通道返回描述 | `String` | `200` | `N` | 已确认 | 示例值：成功[0000000] |
| `async.reverse.resp_data.remark` | `async.reverse.resp_data` | `$.remark` | 备注 | `String` | `255` | `N` | 已确认 | 原样返回；示例值：备注 |
| `async.reverse.resp_data.fq_channels` | `async.reverse.resp_data` | `$.fq_channels` | 分期资产方式 | `String` | `20` | `N` | 已确认 | 花呗分期功能，代表优先使用的资产类型；alipayfq_cc：表示信⽤卡分期。；示例值：alipayfq_cc |
| `async.reverse.resp_data.notify_type` | `async.reverse.resp_data` | `$.notify_type` | 通知类型 | `Integer` | `1` | `N` | 已确认 | 1：通道通知，2：账务通知；示例值：1 |
| `async.reverse.resp_data.split_fee_info` | `async.reverse.resp_data` | `$.split_fee_info` | 分账手续费信息 | `Object` | `—` | `N` | N/A：结构字段长度 | 分账手续费信息 |
| `async.reverse.resp_data.split_fee_info.total_split_fee_amt` | `async.reverse.resp_data` | `$.split_fee_info.total_split_fee_amt` | 分账手续费总金额(元) | `String` | `14` | `N` | 已确认 | 示例值：0.10 |
| `async.reverse.resp_data.split_fee_info.split_fee_flag` | `async.reverse.resp_data` | `$.split_fee_info.split_fee_flag` | 分账手续费扣款标志 | `Integer` | `1` | `Y` | 已确认 | 1: 外扣 2: 内扣；示例值：2 |
| `async.reverse.resp_data.split_fee_info.split_fee_details[]` | `async.reverse.resp_data` | `$.split_fee_info.split_fee_details[]` | 分账手续费信息 | `Array` | `—` | `Y` | N/A：结构字段长度 | 分账手续费信息 |
| `async.reverse.resp_data.split_fee_info.split_fee_details[].split_fee_amt` | `async.reverse.resp_data` | `$.split_fee_info.split_fee_details[].split_fee_amt` | 分账手续费金额(元) | `String` | `14` | `Y` | 已确认 | 示例值：0.10 |
| `async.reverse.resp_data.split_fee_info.split_fee_details[].split_fee_huifu_id` | `async.reverse.resp_data` | `$.split_fee_info.split_fee_details[].split_fee_huifu_id` | 分账手续费承担方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.reverse.resp_data.split_fee_info.split_fee_details[].split_fee_acct_id` | `async.reverse.resp_data` | `$.split_fee_info.split_fee_details[].split_fee_acct_id` | 分账手续费承担方账号 | `String` | `32` | `N` | 已确认 | 示例值：F00598600 |
| `async.reverse.resp_data.atu_sub_mer_id` | `async.reverse.resp_data` | `$.atu_sub_mer_id` | ATU真实商户号 | `String` | `32` | `N` | 已确认 | 示例值：411111141 |
| `async.reverse.resp_data.devs_id` | `async.reverse.resp_data` | `$.devs_id` | 汇付终端号 | `String` | `32` | `N` | 已确认 | 使用汇付机具交易时返回；示例值：[官网示例已脱敏] |

## 聚合交易查询

- 原始地址：<https://paas.huifu.com/partners/lightning/api/jyddcx.md>
- SHA-256：`9e714b3db5c041bbc4732dec8db3b084f0d1f0464b67f759986cf40276747b92`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/代理商/商户的huifu_id ；（1）当主体为渠道商/代理商时，此字段填写渠道商/代理商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：MCS |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 汇付商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `C` | 已确认 | 日期格式：yyyyMMdd，以北京时间为准 |
| `request.data.out_ord_id` | `request.data.out_ord_id` | `—（直接 JSON 路径）` | 汇付服务订单号 | `String` | `32` | `C` | 已确认 | out_ord_id,hf_seq_id,req_seq_id 必填其一；汇付生成的服务订单号；示例值：1234323JKHDFE1243252 |
| `request.data.hf_seq_id` | `request.data.hf_seq_id` | `—（直接 JSON 路径）` | 创建服务订单返回的汇付全局流水号 | `String` | `128` | `C` | 已确认 | out_ord_id,hf_seq_id,req_seq_id 必填其一；示例值：00290TOP1GR210919004230P853ac[官网示例已脱敏] |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 服务订单创建请求流水号 | `String` | `128` | `C` | 已确认 | out_ord_id,hf_seq_id,req_seq_id 必填其一；示例值：[官网示例已脱敏] |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | 参见[业务返回码](https://paas.huifu.com/partners/lightning/api/jyddcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | 参见[业务返回码](https://paas.huifu.com/partners/lightning/api/jyddcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 日期格式：yyyyMMdd，以北京时间为准 |
| `response.data.hf_seq_id` | `response.data.hf_seq_id` | `—（直接 JSON 路径）` | 交易返回的全局流水号 | `String` | `128` | `N` | 已确认 | 斗拱返回的全局流水号；示例值：00290TOP1GR210919004230P853ac[官网示例已脱敏] |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `N` | 已确认 | 请求流水号，同一商户号当天唯一 |
| `response.data.out_trans_id` | `response.data.out_trans_id` | `—（直接 JSON 路径）` | 用户账单上的交易订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `response.data.party_order_id` | `response.data.party_order_id` | `—（直接 JSON 路径）` | 用户账单上的商户订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `response.data.trans_amt` | `response.data.trans_amt` | `—（直接 JSON 路径）` | 交易金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.settlement_amt` | `response.data.settlement_amt` | `—（直接 JSON 路径）` | 结算金额 | `String` | `14` | `N` | 已确认 | 单位元；示例值：1000.00 |
| `response.data.unconfirm_amt` | `response.data.unconfirm_amt` | `—（直接 JSON 路径）` | 待确认总金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.trade_type` | `response.data.trade_type` | `—（直接 JSON 路径）` | 交易类型 | `String` | `16` | `N` | 已确认 | T_JSAPI: 微信JS支付； T_MINIAPP: 微信小程序支付； T_MICROPAY：微信付款码支付； A_JSAPI: 支付宝JS支付 ； A_NATIVE: 支付宝正扫 ； A_NATIVE: 支付宝付款码 ； U_JSAPI: 银联JS支付 ； U_NATIVE: 银联正扫支付 ； U_MICROPAY: 银联付款码 ； 示例值：T_JSAPI；[接入方确认勘误] 官网说明中第二个 `A_NATIVE: 支付宝付款码` 应为 `A_MICROPAY: 支付宝付款码`；当前成功示例已使用正确值 `A_MICROPAY` |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `1` | `N` | 已确认 | P：处理中；S：成功；F：失败；I: 初始（初始状态很罕见，请联系汇付技术人员处理）；交易状态以此字段为准。；示例值：S |
| `response.data.end_time` | `response.data.end_time` | `—（直接 JSON 路径）` | 支付完成时间 | `String` | `14` | `N` | 已确认 | 格式yyyyMMddHHMMSS，如2009年12月25日9点10分10秒，示例值：20091225091010 |
| `response.data.delay_acct_flag` | `response.data.delay_acct_flag` | `—（直接 JSON 路径）` | 是否延时交易 | `String` | `1` | `Y` | 已确认 | Y：延迟， N：不延迟；示例值：Y |
| `response.data.acct_id` | `response.data.acct_id` | `—（直接 JSON 路径）` | 账户号 | `String` | `9` | `N` | 已确认 | 商户账户号；示例值：F00598600 |
| `response.data.acct_date` | `response.data.acct_date` | `—（直接 JSON 路径）` | 账务日期 | `String` | `8` | `N` | 已确认 | 格式：yyyyMMdd；示例值：20221010 |
| `response.data.acct_stat` | `response.data.acct_stat` | `—（直接 JSON 路径）` | 账务状态 | `String` | `1` | `N` | 已确认 | "I：初始"; "P:处理中"; "S:成功"; "F:失败。示例值：S； 返回“I：初始”状态时，请联系客服确认订单问题 |
| `response.data.debit_type` | `response.data.debit_type` | `—（直接 JSON 路径）` | 借贷记标识 | `String` | `1` | `N` | 已确认 | D：借记卡，C：信用卡，Z：借贷合一卡，O：其他；示例值：D |
| `response.data.wx_user_id` | `response.data.wx_user_id` | `—（直接 JSON 路径）` | 微信用户唯一标识码 | `String` | `128` | `N` | 已确认 | 示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk= |
| `response.data.div_flag` | `response.data.div_flag` | `—（直接 JSON 路径）` | 是否分账交易 | `String` | `1` | `Y` | 已确认 | Y：分账交易，N：非分账交易；示例值：Y |
| `response.data.combinedpay_fee_amt` | `response.data.combinedpay_fee_amt` | `—（直接 JSON 路径）` | 补贴部分的手续费 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `255` | `N` | 已确认 | 原样返回；示例值：备注 |
| `response.data.device_type` | `response.data.device_type` | `—（直接 JSON 路径）` | 终端类型 | `String` | `2` | `N` | 已确认 | 01-智能POS；02-扫码POS；03-云音箱；04-台牌；05-云打印；06-扫脸设备；07-收银机；08-收银助手；09-传统POS；10-一体音箱；11-虚拟终端；示例值：01 |
| `response.data.bank_message` | `response.data.bank_message` | `—（直接 JSON 路径）` | 外部通道返回描述 | `String` | `200` | `N` | 已确认 | 示例值：TRADE_SUCCESS |
| `response.data.atu_sub_mer_id` | `response.data.atu_sub_mer_id` | `—（直接 JSON 路径）` | ATU真实商户号 | `String` | `32` | `N` | 已确认 | 示例值：411111141 |
| `response.data.freeze_time` | `response.data.freeze_time` | `—（直接 JSON 路径）` | 冻结时间 | `String` | `14` | `Y` | 已确认 | 格式为yyyyMMddHHMMSS，示例值：20091225091010 |
| `response.data.unfreeze_amt` | `response.data.unfreeze_amt` | `—（直接 JSON 路径）` | 解冻金额 | `String` | `14` | `Y` | 已确认 | 单元：元。示例值：1.23 |
| `response.data.unfreeze_time` | `response.data.unfreeze_time` | `—（直接 JSON 路径）` | 解冻时间 | `String` | `14` | `Y` | 已确认 | 格式为yyyyMMddHHMMSS，示例值：20091225091010 |
| `response.data.fund_freeze_stat` | `response.data.fund_freeze_stat` | `—（直接 JSON 路径）` | 资金冻结状态 | `String` | `16` | `N` | 已确认 | FREEZE：冻结；UNFREEZE：解冻；示例值：UNFREEZE |
| `response.data.method_expand` | `response.data.method_expand` | `—（String(JSON) 容器）` | 交易类型扩展参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.method_expand.T_JSAPI` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 微信公众号支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.method_expand.T_JSAPI.sub_openid` | `response.data.method_expand` | `$.sub_openid` | 子商户公众账号ID | `String` | `16` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `response.data.method_expand.T_JSAPI.openid` | `response.data.method_expand` | `$.openid` | 用户标识 | `String` | `128` | `N` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `response.data.method_expand.T_JSAPI.cash_fee` | `response.data.method_expand` | `$.cash_fee` | 现金支付金额 | `String` | `14` | `N` | 已确认 | 现金支付金额订单现金支付金额；单位格式为0.00；示例值：1.00 |
| `response.data.method_expand.T_JSAPI.attach` | `response.data.method_expand` | `$.attach` | 商家数据包 | `String` | `128` | `N` | 已确认 | 原样返回；示例值：附加数据 |
| `response.data.method_expand.T_JSAPI.coupon_fee` | `response.data.method_expand` | `$.coupon_fee` | 代金券金额 | `String` | `14` | `N` | 已确认 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：1.00 |
| `response.data.method_expand.T_JSAPI.promotion_detail[]` | `response.data.method_expand` | `$.promotion_detail[]` | 营销详情列表 | `Array` | `6000` | `N` | 已确认 | 营销详情列表，使返回值为Json格式 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].activity_id` | `response.data.method_expand` | `$.promotion_detail[].activity_id` | 活动id | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `response.data.method_expand.T_JSAPI.promotion_detail[].amount` | `response.data.method_expand` | `$.promotion_detail[].amount` | 优惠券面额 | `String` | `5` | `Y` | 已确认 | 用户享受优惠的金额；示例值：10.00 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].promotion_id` | `response.data.method_expand` | `$.promotion_detail[].promotion_id` | 券或者立减优惠id | `String` | `32` | `Y` | 已确认 | 示例值：2345234235 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].goods_detail[]` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[]` | 单品列表 | `Array` | `3000` | `N` | 已确认 | 单品信息，Json格式 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].goods_detail[].discount_amount` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，**单位为：元**；示例值：20.00 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].goods_detail[].goods_id` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].goods_detail[].price` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].price` | 商品价格 | `String` | `32` | `Y` | 已确认 | **单位为：元**。示例值：50.00；如果商户有优惠，需传输商户优惠后的单价。；例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].goods_detail[].quantity` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].goods_detail[].goods_remark` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | 按照配置原样返回，字段内容在微信后台配置券时进行设置。示例值：商品备注 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].merchant_contribute` | `response.data.method_expand` | `$.promotion_detail[].merchant_contribute` | 商户出资(元) | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额；示例值：1000 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].name` | `response.data.method_expand` | `$.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].other_contribute` | `response.data.method_expand` | `$.promotion_detail[].other_contribute` | 其他出资(元) | `String` | `32` | `N` | 已确认 | 其他出资方出资金额；示例值：2000 |
| `response.data.method_expand.T_JSAPI.promotion_detail[].scope` | `response.data.method_expand` | `$.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL- 全场代金券，SINGLE- 单品优惠；示例值：GLOBAL |
| `response.data.method_expand.T_JSAPI.promotion_detail[].type` | `response.data.method_expand` | `$.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致） ；DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `response.data.method_expand.T_JSAPI.bank_type` | `response.data.method_expand` | `$.bank_type` | 付款银行 | `String` | `16` | `N` | 已确认 | 银行类型，采用字符串类型的银行标识；参见[微信银行类型说明](https://pay.weixin.qq.com/wiki/doc/api/micropay_sl.php?chapter=4_2)；示例值：CMB |
| `response.data.method_expand.T_JSAPI.sub_appid` | `response.data.method_expand` | `$.sub_appid` | 商户公众号APPID | `String` | `32` | `N` | 已确认 | 直连交易字段；示例值：wx5934540532 |
| `response.data.method_expand.T_JSAPI.device_info` | `response.data.method_expand` | `$.device_info` | 交易终端设备信息 | `String` | `32` | `N` | 已确认 | 直连交易字段；示例值： |
| `response.data.method_expand.T_MINIAPP` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 微信小程序支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.method_expand.T_MINIAPP.sub_openid` | `response.data.method_expand` | `$.sub_openid` | 子商户公众账号ID | `String` | `16` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `response.data.method_expand.T_MINIAPP.openid` | `response.data.method_expand` | `$.openid` | 用户标识 | `String` | `128` | `N` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `response.data.method_expand.T_MINIAPP.cash_fee` | `response.data.method_expand` | `$.cash_fee` | 现金支付金额 | `String` | `14` | `N` | 已确认 | 现金支付金额订单现金支付金额；单位格式为0.00；示例值：1.00 |
| `response.data.method_expand.T_MINIAPP.attach` | `response.data.method_expand` | `$.attach` | 商家数据包 | `String` | `128` | `N` | 已确认 | 原样返回；示例值：附加数据 |
| `response.data.method_expand.T_MINIAPP.coupon_fee` | `response.data.method_expand` | `$.coupon_fee` | 代金券金额 | `String` | `14` | `N` | 已确认 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：1.00 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[]` | `response.data.method_expand` | `$.promotion_detail[]` | 营销详情列表 | `Array` | `6000` | `N` | 已确认 | 营销详情列表，使返回值为Json格式 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].activity_id` | `response.data.method_expand` | `$.promotion_detail[].activity_id` | 活动id | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].amount` | `response.data.method_expand` | `$.promotion_detail[].amount` | 优惠券面额 | `String` | `5` | `Y` | 已确认 | 用户享受优惠的金额；示例值：10.00 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].promotion_id` | `response.data.method_expand` | `$.promotion_detail[].promotion_id` | 券或者立减优惠id | `String` | `32` | `Y` | 已确认 | 示例值：2345234235 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].goods_detail[]` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[]` | 单品列表 | `Array` | `3000` | `N` | 已确认 | 单品信息，Json格式 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].goods_detail[].discount_amount` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，**单位为：元**；示例值：20.00 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].goods_detail[].goods_id` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].goods_detail[].price` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].price` | 商品价格 | `String` | `32` | `Y` | 已确认 | **单位为：元**。示例值：50.00；如果商户有优惠，需传输商户优惠后的单价。；例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].goods_detail[].quantity` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].goods_detail[].goods_remark` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | 按照配置原样返回，字段内容在微信后台配置券时进行设置。示例值：商品备注 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].merchant_contribute` | `response.data.method_expand` | `$.promotion_detail[].merchant_contribute` | 商户出资(元) | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额；示例值：1000 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].name` | `response.data.method_expand` | `$.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].other_contribute` | `response.data.method_expand` | `$.promotion_detail[].other_contribute` | 其他出资(元) | `String` | `32` | `N` | 已确认 | 其他出资方出资金额；示例值：2000 |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].scope` | `response.data.method_expand` | `$.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL- 全场代金券，SINGLE- 单品优惠；示例值：GLOBAL |
| `response.data.method_expand.T_MINIAPP.promotion_detail[].type` | `response.data.method_expand` | `$.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致） ；DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `response.data.method_expand.T_MINIAPP.bank_type` | `response.data.method_expand` | `$.bank_type` | 付款银行 | `String` | `16` | `N` | 已确认 | 银行类型，采用字符串类型的银行标识；参见[微信银行类型说明](https://pay.weixin.qq.com/wiki/doc/api/micropay_sl.php?chapter=4_2)；示例值：CMB |
| `response.data.method_expand.T_MINIAPP.sub_appid` | `response.data.method_expand` | `$.sub_appid` | 商户公众号APPID | `String` | `32` | `N` | 已确认 | 直连交易字段；示例值：wx5934540532 |
| `response.data.method_expand.T_MINIAPP.device_info` | `response.data.method_expand` | `$.device_info` | 交易终端设备信息 | `String` | `32` | `N` | 已确认 | 直连交易字段；示例值： |
| `response.data.method_expand.T_APP` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 微信APP支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.method_expand.T_APP.sub_openid` | `response.data.method_expand` | `$.sub_openid` | 子商户公众账号ID | `String` | `16` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `response.data.method_expand.T_APP.openid` | `response.data.method_expand` | `$.openid` | 用户标识 | `String` | `128` | `N` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `response.data.method_expand.T_APP.cash_fee` | `response.data.method_expand` | `$.cash_fee` | 现金支付金额 | `String` | `14` | `N` | 已确认 | 现金支付金额订单现金支付金额；单位格式为0.00；示例值：1.00 |
| `response.data.method_expand.T_APP.attach` | `response.data.method_expand` | `$.attach` | 商家数据包 | `String` | `128` | `N` | 已确认 | 原样返回；示例值：附加数据 |
| `response.data.method_expand.T_APP.coupon_fee` | `response.data.method_expand` | `$.coupon_fee` | 代金券金额 | `String` | `14` | `N` | 已确认 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：1.00 |
| `response.data.method_expand.T_APP.promotion_detail[]` | `response.data.method_expand` | `$.promotion_detail[]` | 营销详情列表 | `Array` | `6000` | `N` | 已确认 | 营销详情列表，使返回值为Json格式 |
| `response.data.method_expand.T_APP.promotion_detail[].activity_id` | `response.data.method_expand` | `$.promotion_detail[].activity_id` | 活动id | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `response.data.method_expand.T_APP.promotion_detail[].amount` | `response.data.method_expand` | `$.promotion_detail[].amount` | 优惠券面额 | `String` | `5` | `Y` | 已确认 | 用户享受优惠的金额；示例值：10.00 |
| `response.data.method_expand.T_APP.promotion_detail[].promotion_id` | `response.data.method_expand` | `$.promotion_detail[].promotion_id` | 券或者立减优惠id | `String` | `32` | `Y` | 已确认 | 示例值：2345234235 |
| `response.data.method_expand.T_APP.promotion_detail[].goods_detail[]` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[]` | 单品列表 | `Array` | `3000` | `N` | 已确认 | 单品信息，Json格式 |
| `response.data.method_expand.T_APP.promotion_detail[].goods_detail[].discount_amount` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，**单位为：元**；示例值：20.00 |
| `response.data.method_expand.T_APP.promotion_detail[].goods_detail[].goods_id` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `response.data.method_expand.T_APP.promotion_detail[].goods_detail[].price` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].price` | 商品价格 | `String` | `32` | `Y` | 已确认 | **单位为：元**。示例值：50.00；如果商户有优惠，需传输商户优惠后的单价。；例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50 |
| `response.data.method_expand.T_APP.promotion_detail[].goods_detail[].quantity` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `response.data.method_expand.T_APP.promotion_detail[].goods_detail[].goods_remark` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | 按照配置原样返回，字段内容在微信后台配置券时进行设置。示例值：商品备注 |
| `response.data.method_expand.T_APP.promotion_detail[].merchant_contribute` | `response.data.method_expand` | `$.promotion_detail[].merchant_contribute` | 商户出资(元) | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额；示例值：1000 |
| `response.data.method_expand.T_APP.promotion_detail[].name` | `response.data.method_expand` | `$.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `response.data.method_expand.T_APP.promotion_detail[].other_contribute` | `response.data.method_expand` | `$.promotion_detail[].other_contribute` | 其他出资(元) | `String` | `32` | `N` | 已确认 | 其他出资方出资金额；示例值：2000 |
| `response.data.method_expand.T_APP.promotion_detail[].scope` | `response.data.method_expand` | `$.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL- 全场代金券，SINGLE- 单品优惠；示例值：GLOBAL |
| `response.data.method_expand.T_APP.promotion_detail[].type` | `response.data.method_expand` | `$.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致） ；DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `response.data.method_expand.T_APP.bank_type` | `response.data.method_expand` | `$.bank_type` | 付款银行 | `String` | `16` | `N` | 已确认 | 银行类型，采用字符串类型的银行标识；参见[微信银行类型说明](https://pay.weixin.qq.com/wiki/doc/api/micropay_sl.php?chapter=4_2)；示例值：CMB |
| `response.data.method_expand.T_APP.sub_appid` | `response.data.method_expand` | `$.sub_appid` | 商户公众号APPID | `String` | `32` | `N` | 已确认 | 直连交易字段；示例值：wx5934540532 |
| `response.data.method_expand.T_APP.device_info` | `response.data.method_expand` | `$.device_info` | 交易终端设备信息 | `String` | `32` | `N` | 已确认 | 直连交易字段；示例值： |
| `response.data.method_expand.T_MICROPAY` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 微信反扫支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.method_expand.T_MICROPAY.sub_openid` | `response.data.method_expand` | `$.sub_openid` | 子商户公众账号ID | `String` | `16` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `response.data.method_expand.T_MICROPAY.openid` | `response.data.method_expand` | `$.openid` | 用户标识 | `String` | `128` | `N` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `response.data.method_expand.T_MICROPAY.cash_fee` | `response.data.method_expand` | `$.cash_fee` | 现金支付金额 | `String` | `14` | `N` | 已确认 | 现金支付金额订单现金支付金额；单位格式为0.00；示例值：1.00 |
| `response.data.method_expand.T_MICROPAY.attach` | `response.data.method_expand` | `$.attach` | 商家数据包 | `String` | `128` | `N` | 已确认 | 原样返回；示例值：附加数据 |
| `response.data.method_expand.T_MICROPAY.coupon_fee` | `response.data.method_expand` | `$.coupon_fee` | 代金券金额 | `String` | `14` | `N` | 已确认 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：1.00 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[]` | `response.data.method_expand` | `$.promotion_detail[]` | 营销详情列表 | `Array` | `6000` | `N` | 已确认 | 营销详情列表，使返回值为Json格式 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].activity_id` | `response.data.method_expand` | `$.promotion_detail[].activity_id` | 活动id | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].amount` | `response.data.method_expand` | `$.promotion_detail[].amount` | 优惠券面额 | `String` | `5` | `Y` | 已确认 | 用户享受优惠的金额；示例值：10.00 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].promotion_id` | `response.data.method_expand` | `$.promotion_detail[].promotion_id` | 券或者立减优惠id | `String` | `32` | `Y` | 已确认 | 示例值：2345234235 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].goods_detail[]` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[]` | 单品列表 | `Array` | `3000` | `N` | 已确认 | 单品信息，Json格式 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].goods_detail[].discount_amount` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，**单位为：元**；示例值：20.00 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].goods_detail[].goods_id` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].goods_detail[].price` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].price` | 商品价格 | `String` | `32` | `Y` | 已确认 | **单位为：元**。示例值：50.00；如果商户有优惠，需传输商户优惠后的单价。；例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].goods_detail[].quantity` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].goods_detail[].goods_remark` | `response.data.method_expand` | `$.promotion_detail[].goods_detail[].goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | 按照配置原样返回，字段内容在微信后台配置券时进行设置。示例值：商品备注 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].merchant_contribute` | `response.data.method_expand` | `$.promotion_detail[].merchant_contribute` | 商户出资(元) | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额；示例值：1000 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].name` | `response.data.method_expand` | `$.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].other_contribute` | `response.data.method_expand` | `$.promotion_detail[].other_contribute` | 其他出资(元) | `String` | `32` | `N` | 已确认 | 其他出资方出资金额；示例值：2000 |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].scope` | `response.data.method_expand` | `$.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL- 全场代金券，SINGLE- 单品优惠；示例值：GLOBAL |
| `response.data.method_expand.T_MICROPAY.promotion_detail[].type` | `response.data.method_expand` | `$.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致） ；DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `response.data.method_expand.T_MICROPAY.bank_type` | `response.data.method_expand` | `$.bank_type` | 付款银行 | `String` | `16` | `N` | 已确认 | 银行类型，采用字符串类型的银行标识；参见[微信银行类型说明](https://pay.weixin.qq.com/wiki/doc/api/micropay_sl.php?chapter=4_2)；示例值：CMB |
| `response.data.method_expand.T_MICROPAY.sub_appid` | `response.data.method_expand` | `$.sub_appid` | 商户公众号APPID | `String` | `32` | `N` | 已确认 | 直连交易字段；示例值：wx5934540532 |
| `response.data.method_expand.T_MICROPAY.device_info` | `response.data.method_expand` | `$.device_info` | 交易终端设备信息 | `String` | `32` | `N` | 已确认 | 直连交易字段；示例值： |
| `response.data.method_expand.A_JSAPI` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 支付宝JS支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.method_expand.A_JSAPI.buyer_id` | `response.data.method_expand` | `$.buyer_id` | 买家支付宝用户号 | `String` | `28` | `N` | 已确认 | 买家的支付宝唯一用户号（2088开头的16位纯数字）；示例值：[官网示例已脱敏] |
| `response.data.method_expand.A_JSAPI.buyer_logon_id` | `response.data.method_expand` | `$.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com |
| `response.data.method_expand.A_JSAPI.fund_bill_list[]` | `response.data.method_expand` | `$.fund_bill_list[]` | 交易支付使用的资金渠道 | `Array` | `2048` | `N` | 已确认 | 支付成功的各个渠道金额信息，详见资金明细信息说明 |
| `response.data.method_expand.A_JSAPI.fund_bill_list[].bank_code` | `response.data.method_expand` | `$.fund_bill_list[].bank_code` | 银行卡支付时的银行代码 | `String` | `10` | `N` | 已确认 | 示例值：CEB，请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
| `response.data.method_expand.A_JSAPI.fund_bill_list[].amount` | `response.data.method_expand` | `$.fund_bill_list[].amount` | 该支付工具类型所使用的金额 | `String` | `32` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `response.data.method_expand.A_JSAPI.fund_bill_list[].fund_channel` | `response.data.method_expand` | `$.fund_bill_list[].fund_channel` | 交易使用的资金渠道 | `String` | `32` | `N` | 已确认 | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；示例值：ALIPAYACCOUNT |
| `response.data.method_expand.A_JSAPI.fund_bill_list[].fund_type` | `response.data.method_expand` | `$.fund_bill_list[].fund_type` | 渠道所使用的资金类型 | `String` | `32` | `N` | 已确认 | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。；DEBIT_CARD:借记卡，CREDIT_CARD:信用卡，MIXED_CARD:借贷合一卡；示例值：DEBIT_CARD |
| `response.data.method_expand.A_JSAPI.fund_bill_list[].real_amount` | `response.data.method_expand` | `$.fund_bill_list[].real_amount` | 渠道实际付款金额 | `String` | `11` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `response.data.method_expand.A_JSAPI.hb_fq_num` | `response.data.method_expand` | `$.hb_fq_num` | 花呗分期数 | `String` | `10` | `N` | 已确认 | 示例值：3 |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[]` | `response.data.method_expand` | `$.voucher_detail_list[]` | 本交易支付时使用的所有优惠券信息 | `Array` | `2048` | `N` | 已确认 | 本交易支付时使用的所有优惠券信息 |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[].amount` | `response.data.method_expand` | `$.voucher_detail_list[].amount` | 优惠券面额（元） | `String` | `32` | `Y` | 已确认 | 用户享受优惠的金额；示例值：10.00 |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[].id` | `response.data.method_expand` | `$.voucher_detail_list[].id` | 券id | `String` | `32` | `Y` | 已确认 | 优惠券号；示例值：6934572310301 |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[].name` | `response.data.method_expand` | `$.voucher_detail_list[].name` | 券名称 | `String` | `32` | `Y` | 已确认 | 优惠名称；示例值：实体店付款通用立减券 |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[].type` | `response.data.method_expand` | `$.voucher_detail_list[].type` | 券类型 | `String` | `32` | `Y` | 已确认 | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）；DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[].merchant_contribute` | `response.data.method_expand` | `$.voucher_detail_list[].merchant_contribute` | 商家出资 | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元。示例值：0.10 |
| `response.data.method_expand.A_JSAPI.voucher_detail_list[].other_contribute` | `response.data.method_expand` | `$.voucher_detail_list[].other_contribute` | 其他出资方出资金额 | `String` | `14` | `N` | 已确认 | 其他出资方出资金额，单位为元。示例值：0.20 |
| `response.data.method_expand.A_NATIVE` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 支付宝正扫支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.method_expand.A_NATIVE.buyer_id` | `response.data.method_expand` | `$.buyer_id` | 买家支付宝用户号 | `String` | `28` | `N` | 已确认 | 买家的支付宝唯一用户号（2088开头的16位纯数字）；示例值：[官网示例已脱敏] |
| `response.data.method_expand.A_NATIVE.buyer_logon_id` | `response.data.method_expand` | `$.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com |
| `response.data.method_expand.A_NATIVE.fund_bill_list[]` | `response.data.method_expand` | `$.fund_bill_list[]` | 交易支付使用的资金渠道 | `Array` | `2048` | `N` | 已确认 | 支付成功的各个渠道金额信息，详见资金明细信息说明 |
| `response.data.method_expand.A_NATIVE.fund_bill_list[].bank_code` | `response.data.method_expand` | `$.fund_bill_list[].bank_code` | 银行卡支付时的银行代码 | `String` | `10` | `N` | 已确认 | 示例值：CEB，请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
| `response.data.method_expand.A_NATIVE.fund_bill_list[].amount` | `response.data.method_expand` | `$.fund_bill_list[].amount` | 该支付工具类型所使用的金额 | `String` | `32` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `response.data.method_expand.A_NATIVE.fund_bill_list[].fund_channel` | `response.data.method_expand` | `$.fund_bill_list[].fund_channel` | 交易使用的资金渠道 | `String` | `32` | `N` | 已确认 | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；示例值：ALIPAYACCOUNT |
| `response.data.method_expand.A_NATIVE.fund_bill_list[].fund_type` | `response.data.method_expand` | `$.fund_bill_list[].fund_type` | 渠道所使用的资金类型 | `String` | `32` | `N` | 已确认 | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。；DEBIT_CARD:借记卡，CREDIT_CARD:信用卡，MIXED_CARD:借贷合一卡；示例值：DEBIT_CARD |
| `response.data.method_expand.A_NATIVE.fund_bill_list[].real_amount` | `response.data.method_expand` | `$.fund_bill_list[].real_amount` | 渠道实际付款金额 | `String` | `11` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `response.data.method_expand.A_NATIVE.hb_fq_num` | `response.data.method_expand` | `$.hb_fq_num` | 花呗分期数 | `String` | `10` | `N` | 已确认 | 示例值：3 |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[]` | `response.data.method_expand` | `$.voucher_detail_list[]` | 本交易支付时使用的所有优惠券信息 | `Array` | `2048` | `N` | 已确认 | 本交易支付时使用的所有优惠券信息 |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[].amount` | `response.data.method_expand` | `$.voucher_detail_list[].amount` | 优惠券面额（元） | `String` | `32` | `Y` | 已确认 | 用户享受优惠的金额；示例值：10.00 |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[].id` | `response.data.method_expand` | `$.voucher_detail_list[].id` | 券id | `String` | `32` | `Y` | 已确认 | 优惠券号；示例值：6934572310301 |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[].name` | `response.data.method_expand` | `$.voucher_detail_list[].name` | 券名称 | `String` | `32` | `Y` | 已确认 | 优惠名称；示例值：实体店付款通用立减券 |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[].type` | `response.data.method_expand` | `$.voucher_detail_list[].type` | 券类型 | `String` | `32` | `Y` | 已确认 | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）；DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[].merchant_contribute` | `response.data.method_expand` | `$.voucher_detail_list[].merchant_contribute` | 商家出资 | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元。示例值：0.10 |
| `response.data.method_expand.A_NATIVE.voucher_detail_list[].other_contribute` | `response.data.method_expand` | `$.voucher_detail_list[].other_contribute` | 其他出资方出资金额 | `String` | `14` | `N` | 已确认 | 其他出资方出资金额，单位为元。示例值：0.20 |
| `response.data.method_expand.A_MICROPAY` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 支付宝反扫支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.method_expand.A_MICROPAY.buyer_id` | `response.data.method_expand` | `$.buyer_id` | 买家支付宝用户号 | `String` | `28` | `N` | 已确认 | 买家的支付宝唯一用户号（2088开头的16位纯数字）；示例值：[官网示例已脱敏] |
| `response.data.method_expand.A_MICROPAY.buyer_logon_id` | `response.data.method_expand` | `$.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com |
| `response.data.method_expand.A_MICROPAY.fund_bill_list[]` | `response.data.method_expand` | `$.fund_bill_list[]` | 交易支付使用的资金渠道 | `Array` | `2048` | `N` | 已确认 | 支付成功的各个渠道金额信息，详见资金明细信息说明 |
| `response.data.method_expand.A_MICROPAY.fund_bill_list[].bank_code` | `response.data.method_expand` | `$.fund_bill_list[].bank_code` | 银行卡支付时的银行代码 | `String` | `10` | `N` | 已确认 | 示例值：CEB，请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
| `response.data.method_expand.A_MICROPAY.fund_bill_list[].amount` | `response.data.method_expand` | `$.fund_bill_list[].amount` | 该支付工具类型所使用的金额 | `String` | `32` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `response.data.method_expand.A_MICROPAY.fund_bill_list[].fund_channel` | `response.data.method_expand` | `$.fund_bill_list[].fund_channel` | 交易使用的资金渠道 | `String` | `32` | `N` | 已确认 | [详见支付宝官方说明](https://doc.open.alipay.com/doc2/detail?treeId=26&articleId=103259&docType=1) ；示例值：ALIPAYACCOUNT |
| `response.data.method_expand.A_MICROPAY.fund_bill_list[].fund_type` | `response.data.method_expand` | `$.fund_bill_list[].fund_type` | 渠道所使用的资金类型 | `String` | `32` | `N` | 已确认 | 目前只在资金渠道(fund_channel)是银行卡渠道(BANKCARD)的情况下才返回该信息。；DEBIT_CARD:借记卡，CREDIT_CARD:信用卡，MIXED_CARD:借贷合一卡；示例值：DEBIT_CARD |
| `response.data.method_expand.A_MICROPAY.fund_bill_list[].real_amount` | `response.data.method_expand` | `$.fund_bill_list[].real_amount` | 渠道实际付款金额 | `String` | `11` | `N` | 已确认 | 单位：元，两位小数；示例值：0.01 |
| `response.data.method_expand.A_MICROPAY.hb_fq_num` | `response.data.method_expand` | `$.hb_fq_num` | 花呗分期数 | `String` | `10` | `N` | 已确认 | 示例值：3 |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[]` | `response.data.method_expand` | `$.voucher_detail_list[]` | 本交易支付时使用的所有优惠券信息 | `Array` | `2048` | `N` | 已确认 | 本交易支付时使用的所有优惠券信息 |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[].amount` | `response.data.method_expand` | `$.voucher_detail_list[].amount` | 优惠券面额（元） | `String` | `32` | `Y` | 已确认 | 用户享受优惠的金额；示例值：10.00 |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[].id` | `response.data.method_expand` | `$.voucher_detail_list[].id` | 券id | `String` | `32` | `Y` | 已确认 | 优惠券号；示例值：6934572310301 |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[].name` | `response.data.method_expand` | `$.voucher_detail_list[].name` | 券名称 | `String` | `32` | `Y` | 已确认 | 优惠名称；示例值：实体店付款通用立减券 |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[].type` | `response.data.method_expand` | `$.voucher_detail_list[].type` | 券类型 | `String` | `32` | `Y` | 已确认 | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）；DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[].merchant_contribute` | `response.data.method_expand` | `$.voucher_detail_list[].merchant_contribute` | 商家出资 | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元。示例值：0.10 |
| `response.data.method_expand.A_MICROPAY.voucher_detail_list[].other_contribute` | `response.data.method_expand` | `$.voucher_detail_list[].other_contribute` | 其他出资方出资金额 | `String` | `14` | `N` | 已确认 | 其他出资方出资金额，单位为元。示例值：0.20 |
| `response.data.method_expand.U_JSAPI` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 银联JS支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.method_expand.U_JSAPI.coupon_info[]` | `response.data.method_expand` | `$.coupon_info[]` | 银联优惠信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 银联使用优惠活动时出现，jsonArray格式 |
| `response.data.method_expand.U_JSAPI.coupon_info[].type` | `response.data.method_expand` | `$.coupon_info[].type` | 项目类型 | `String` | `4` | `Y` | 已确认 | DD01：随机立减；CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券；CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券；示例值：DD01 |
| `response.data.method_expand.U_JSAPI.coupon_info[].spnsrId` | `response.data.method_expand` | `$.coupon_info[].spnsrId` | 出资方 | `String` | `20` | `Y` | 已确认 | 00010000：银联出资；付款方作为出资方：填写8位付款方机构代码；商户作为出资方：填写15位商户代码；示例值：00010000 |
| `response.data.method_expand.U_JSAPI.coupon_info[].offstAmt` | `response.data.method_expand` | `$.coupon_info[].offstAmt` | 抵消交易金额 | `String` | `14` | `Y` | 已确认 | 不能为全0；示例值：1.00 |
| `response.data.method_expand.U_JSAPI.coupon_info[].id` | `response.data.method_expand` | `$.coupon_info[].id` | 项目编号 | `String` | `40` | `N` | 已确认 | 用于票券编号等，格式自定义；示例值：938434221 |
| `response.data.method_expand.U_JSAPI.coupon_info[].desc` | `response.data.method_expand` | `$.coupon_info[].desc` | 项目简称 | `String` | `40` | `N` | 已确认 | 优惠活动简称，可用于展示、打单等；示例值：中秋优惠促销 |
| `response.data.method_expand.U_JSAPI.coupon_info[].addnInfo` | `response.data.method_expand` | `$.coupon_info[].addnInfo` | 附加信息 | `String` | `100` | `N` | 已确认 | 内容自定义；示例值：附加信息 |
| `response.data.method_expand.U_JSAPI.acc_no` | `response.data.method_expand` | `$.acc_no` | 付款账号 | `String` | `40` | `N` | 已确认 | 付款方的卡号/账号/Token |
| `response.data.method_expand.U_NATIVE` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 银联正扫支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.method_expand.U_NATIVE.coupon_info[]` | `response.data.method_expand` | `$.coupon_info[]` | 银联优惠信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 银联使用优惠活动时出现，jsonArray格式 |
| `response.data.method_expand.U_NATIVE.coupon_info[].type` | `response.data.method_expand` | `$.coupon_info[].type` | 项目类型 | `String` | `4` | `Y` | 已确认 | DD01：随机立减；CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券；CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券；示例值：DD01 |
| `response.data.method_expand.U_NATIVE.coupon_info[].spnsrId` | `response.data.method_expand` | `$.coupon_info[].spnsrId` | 出资方 | `String` | `20` | `Y` | 已确认 | 00010000：银联出资；付款方作为出资方：填写8位付款方机构代码；商户作为出资方：填写15位商户代码；示例值：00010000 |
| `response.data.method_expand.U_NATIVE.coupon_info[].offstAmt` | `response.data.method_expand` | `$.coupon_info[].offstAmt` | 抵消交易金额 | `String` | `14` | `Y` | 已确认 | 不能为全0；示例值：1.00 |
| `response.data.method_expand.U_NATIVE.coupon_info[].id` | `response.data.method_expand` | `$.coupon_info[].id` | 项目编号 | `String` | `40` | `N` | 已确认 | 用于票券编号等，格式自定义；示例值：938434221 |
| `response.data.method_expand.U_NATIVE.coupon_info[].desc` | `response.data.method_expand` | `$.coupon_info[].desc` | 项目简称 | `String` | `40` | `N` | 已确认 | 优惠活动简称，可用于展示、打单等；示例值：中秋优惠促销 |
| `response.data.method_expand.U_NATIVE.coupon_info[].addnInfo` | `response.data.method_expand` | `$.coupon_info[].addnInfo` | 附加信息 | `String` | `100` | `N` | 已确认 | 内容自定义；示例值：附加信息 |
| `response.data.method_expand.U_NATIVE.acc_no` | `response.data.method_expand` | `$.acc_no` | 付款账号 | `String` | `40` | `N` | 已确认 | 付款方的卡号/账号/Token |
| `response.data.method_expand.U_MICROPAY` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 银联反扫支付参数 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.method_expand.U_MICROPAY.coupon_info[]` | `response.data.method_expand` | `$.coupon_info[]` | 银联优惠信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 银联使用优惠活动时出现，jsonArray格式 |
| `response.data.method_expand.U_MICROPAY.coupon_info[].type` | `response.data.method_expand` | `$.coupon_info[].type` | 项目类型 | `String` | `4` | `Y` | 已确认 | DD01：随机立减；CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券；CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券；示例值：DD01 |
| `response.data.method_expand.U_MICROPAY.coupon_info[].spnsrId` | `response.data.method_expand` | `$.coupon_info[].spnsrId` | 出资方 | `String` | `20` | `Y` | 已确认 | 00010000：银联出资；付款方作为出资方：填写8位付款方机构代码；商户作为出资方：填写15位商户代码；示例值：00010000 |
| `response.data.method_expand.U_MICROPAY.coupon_info[].offstAmt` | `response.data.method_expand` | `$.coupon_info[].offstAmt` | 抵消交易金额 | `String` | `14` | `Y` | 已确认 | 不能为全0；示例值：1.00 |
| `response.data.method_expand.U_MICROPAY.coupon_info[].id` | `response.data.method_expand` | `$.coupon_info[].id` | 项目编号 | `String` | `40` | `N` | 已确认 | 用于票券编号等，格式自定义；示例值：938434221 |
| `response.data.method_expand.U_MICROPAY.coupon_info[].desc` | `response.data.method_expand` | `$.coupon_info[].desc` | 项目简称 | `String` | `40` | `N` | 已确认 | 优惠活动简称，可用于展示、打单等；示例值：中秋优惠促销 |
| `response.data.method_expand.U_MICROPAY.coupon_info[].addnInfo` | `response.data.method_expand` | `$.coupon_info[].addnInfo` | 附加信息 | `String` | `100` | `N` | 已确认 | 内容自定义；示例值：附加信息 |
| `response.data.method_expand.U_MICROPAY.acc_no` | `response.data.method_expand` | `$.acc_no` | 付款账号 | `String` | `40` | `N` | 已确认 | 付款方的卡号/账号/Token |
| `response.data.tx_metadata` | `response.data.tx_metadata` | `—（String(JSON) 容器）` | 扩展参数集合 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.tx_metadata.acct_split_bunch` | `response.data.tx_metadata` | `$.acct_split_bunch（String(JSON) 容器）` | 分账对象 | `String` | `4000` | `N` | 已确认 | 分账对象，jsonObject字符串 |
| `response.data.tx_metadata.acct_split_bunch.acct_infos[]` | `response.data.tx_metadata` | `$.acct_split_bunch => JSON decode => $.acct_infos[]` | 分账明细 | `Array` | `4000` | `Y` | 已确认 | 分账明细 |
| `response.data.tx_metadata.acct_split_bunch.acct_infos[].div_amt` | `response.data.tx_metadata` | `$.acct_split_bunch => JSON decode => $.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 描述:单位元；示例值：0.20 |
| `response.data.tx_metadata.acct_split_bunch.acct_infos[].huifu_id` | `response.data.tx_metadata` | `$.acct_split_bunch => JSON decode => $.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.tx_metadata.acct_split_bunch.acct_infos[].acct_id` | `response.data.tx_metadata` | `$.acct_split_bunch => JSON decode => $.acct_infos[].acct_id` | 分账接收方子账户 | `String` | `9` | `N` | 已确认 | 示例值：F00598600 |
| `response.data.tx_metadata.acct_split_bunch.is_clean_split` | `response.data.tx_metadata` | `$.acct_split_bunch => JSON decode => $.is_clean_split` | 是否净值分账 | `String` | `1` | `N` | 已确认 | Y:使用净值分账，仅在percentage_flag=Y时起作用；示例值：Y |
| `response.data.tx_metadata.combinedpay_data[]` | `response.data.tx_metadata` | `$.combinedpay_data（String(JSON Array) 容器）` | 补贴支付信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray字符串，参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| `response.data.tx_metadata.combinedpay_data[].huifu_id` | `response.data.tx_metadata` | `$.combinedpay_data => JSON decode => $[].huifu_id` | 补贴方汇付商户号 | `String` | `32` | `Y` | 已确认 | 补贴方汇付ID；示例值：[官网示例已脱敏] |
| `response.data.tx_metadata.combinedpay_data[].user_type` | `response.data.tx_metadata` | `$.combinedpay_data => JSON decode => $[].user_type` | 补贴方类型 | `String` | `32` | `Y` | 已确认 | 补贴方类型：channel-渠道，agent-代理；示例值：agent |
| `response.data.tx_metadata.combinedpay_data[].acct_id` | `response.data.tx_metadata` | `$.combinedpay_data => JSON decode => $[].acct_id` | 补贴方账户号 | `String` | `32` | `Y` | 已确认 | 营销补贴方账户号；示例值：F00900982 |
| `response.data.tx_metadata.combinedpay_data[].amount` | `response.data.tx_metadata` | `$.combinedpay_data => JSON decode => $[].amount` | 补贴金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； 示例值：1.01 |
| `response.data.tx_metadata.combinedpay_data_fee_info` | `response.data.tx_metadata` | `$.combinedpay_data_fee_info（String(JSON) 容器）` | 补贴支付手续费信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.tx_metadata.combinedpay_data_fee_info.huifu_id` | `response.data.tx_metadata` | `$.combinedpay_data_fee_info => JSON decode => $.huifu_id` | 补贴支付手续费承担方汇付编号 | `String` | `32` | `Y` | 已确认 | 补贴支付手续费承担方汇付编号；示例值：[官网示例已脱敏] |
| `response.data.tx_metadata.combinedpay_data_fee_info.acct_id` | `response.data.tx_metadata` | `$.combinedpay_data_fee_info => JSON decode => $.acct_id` | 补贴支付手续费承担方账户号 | `String` | `32` | `Y` | 已确认 | 补贴支付手续费承担方账户号；示例值：F00900982 |
| `response.data.tx_metadata.combinedpay_data_fee_info.combinedpay_fee_amt` | `response.data.tx_metadata` | `$.combinedpay_data_fee_info => JSON decode => $.combinedpay_fee_amt` | 补贴支付手续费金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； 示例值：1.01 |
| `response.data.tx_metadata.trans_fee_allowance_info` | `response.data.tx_metadata` | `$.trans_fee_allowance_info（String(JSON) 容器）` | 手续费补贴信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 返回值为Json格式 |
| `response.data.tx_metadata.trans_fee_allowance_info.actual_fee_amt` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.actual_fee_amt` | 商户实收手续费 | `String` | `14` | `Y` | 已确认 | 示例值：0.10 |
| `response.data.tx_metadata.trans_fee_allowance_info.allowance_fee_amt` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.allowance_fee_amt` | 补贴手续费 | `String` | `14` | `Y` | 已确认 | 示例值：0.20 |
| `response.data.tx_metadata.trans_fee_allowance_info.allowance_type` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.allowance_type` | 补贴类型 | `String` | `1` | `Y` | 已确认 | 0：不补贴，为空默认；1：补贴；2：部分补贴；3：全额补贴(优惠后)；4：部分补贴(优惠后)；示例值：2 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos` | 手续费补贴活动详情 | `Object` | `—` | `N` | N/A：结构字段长度 | Json格式，见下文描述 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.merchant_group` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.merchant_group` | 商户号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.acct_id` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.acct_id` | 门店 | `String` | `64` | `N` | 已确认 | 示例值：sh002 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.activity_id` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.activity_id` | 活动号 | `String` | `64` | `Y` | 已确认 | 示例值：223402342 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.activity_name` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.activity_name` | 活动描述 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.status` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.status` | 活动是否有效 | `String` | `4` | `Y` | 已确认 | 1:生效 0：失效；示例值：1 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.total_limit_amt` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.total_limit_amt` | 活动总补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：10.00 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.start_time` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.start_time` | 活动开始时间 | `String` | `8` | `Y` | 已确认 | yyyyMMdd；示例值：20220909 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.end_time` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.end_time` | 活动结束时间 | `String` | `8` | `Y` | 已确认 | yyyyMMdd；示例值：202209011 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.human_flag` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.human_flag` | 是否人工操作 | `String` | `4` | `Y` | 已确认 | N：自动 Y：人工；示例值：N |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.allowance_sys` | 补贴方 | `String` | `64` | `Y` | 已确认 | 1:银行 2:服务商 3:汇来米；示例值：1 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys_id` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.allowance_sys_id` | 补贴方ID | `String` | `64` | `Y` | 已确认 | 对应补贴方的id；示例值：[官网示例已脱敏] |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.is_delay_allowance` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.is_delay_allowance` | 补贴类型 | `String` | `2` | `Y` | 已确认 | 1:实补,2:后补,默认实补；示例值：1 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.is_share` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.is_share` | 是不是共享额度 | `String` | `4` | `N` | 已确认 | 示例值： |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.market_id` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.market_id` | 自定义活动编号 | `String` | `64` | `Y` | 已确认 | 示例值：ISFE00232 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.market_name` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.market_name` | 自定义活动名称 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.market_desc` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.market_desc` | 自定义活动描述 | `String` | `64` | `N` | 已确认 | 示例值：新店开业大促 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.pos_credit_limit_amt` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.pos_credit_limit_amt` | pos贷记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.pos_debit_limit_amt` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.pos_debit_limit_amt` | pos借记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：2.00 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.pos_limit_amt` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.pos_limit_amt` | pos补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.qr_limit_amt` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.qr_limit_amt` | 扫码补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.create_by` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.create_by` | 创建人 | `String` | `32` | `Y` | 已确认 | 示例值：Lg[官网示例已脱敏] |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.create_time` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.create_time` | 创建时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 22:00:30 |
| `response.data.tx_metadata.trans_fee_allowance_info.cur_allowance_config_infos.update_time` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.update_time` | 更新时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 23:00:30 |
| `response.data.tx_metadata.trans_fee_allowance_info.no_allowance_desc` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.no_allowance_desc` | 不补贴原因 | `String` | `128` | `Y` | 已确认 | 1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴；2:额度用完；3:不在有效期；4:活动不存在；5:手续费金额为0不补贴；6:顶格优惠；7:额度不足；8:手续费后补；9:未达到起始补贴金额；示例值：2 |
| `response.data.tx_metadata.trans_fee_allowance_info.receivable_fee_amt` | `response.data.tx_metadata` | `$.trans_fee_allowance_info => JSON decode => $.receivable_fee_amt` | 商户应收手续费 | `String` | `14` | `Y` | 已确认 | 示例值：4.00 |
| `response.data.tx_metadata.terminal_device_data` | `response.data.tx_metadata` | `$.terminal_device_data（String(JSON) 容器）` | 设备信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 设备信息，jsonObject字符串 |
| `response.data.tx_metadata.terminal_device_data.terminal_ip` | `response.data.tx_metadata` | `$.terminal_device_data => JSON decode => $.terminal_ip` | 交易设备IP | `String` | `64` | `N` | 已确认 | 绑卡设备（付款 APP） 所在的公网IP，可用于定位所属地区，不是 wifi 连接时的局域网 IP。局域网 IP 包括：；A 类： 10.0.0.0-10.255.255.255；B 类： 172.16.0.0-172.31.255.255；C 类： 192.168.0.0-192.168.255.255；示例值：192.168.0.200 |
| `response.data.tx_metadata.terminal_device_data.terminal_location` | `response.data.tx_metadata` | `$.terminal_device_data => JSON decode => $.terminal_location` | 终端实时经纬度信息 | `String` | `32` | `N` | 已确认 | 设备（付款APP）GPS位置,格式为纬度/经度。；+表示北纬、东经，-表示南纬、西经。示例值：+37.12/-121.213；经度整数位不超过3位，小数位不超过5位；纬度整数位不超过2位，小数位不超过6位 |
| `response.data.payment_fee` | `response.data.payment_fee` | `—（String(JSON) 容器）` | 手续费对象 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.payment_fee.fee_huifu_id` | `response.data.payment_fee` | `$.fee_huifu_id` | 手续费商户号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.payment_fee.fee_formula_infos[]` | `response.data.payment_fee` | `$.fee_formula_infos[]` | 手续费费率信息 | `Array` | `—` | `N` | N/A：结构字段长度 | jsonArray格式；交易成功时返回手续费费率信息 |
| `response.data.payment_fee.fee_formula_infos[].fee_formula` | `response.data.payment_fee` | `$.fee_formula_infos[].fee_formula` | 手续费计算公式 | `String` | `512` | `N` | 已确认 | 示例值：AMT\*0.003 |
| `response.data.payment_fee.fee_formula_infos[].fee_type` | `response.data.payment_fee` | `$.fee_formula_infos[].fee_type` | 手续费类型 | `String` | `32` | `N` | 已确认 | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；示例值：ACCT_FEE |
| `response.data.payment_fee.fee_formula_infos[].huifu_id` | `response.data.payment_fee` | `$.fee_formula_infos[].huifu_id` | 商户号 | `String` | `32` | `N` | 已确认 | 组合支付账户补贴时，补贴账户的huifuId；示例值：[官网示例已脱敏] |
| `response.data.payment_fee.fee_flag` | `response.data.payment_fee` | `$.fee_flag` | 手续费扣款标志 | `String` | `1` | `N` | 已确认 | 1: 外扣，2: 内扣；示例值：1 |
| `response.data.payment_fee.fee_amount` | `response.data.payment_fee` | `$.fee_amount` | 手续费金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00,最低传入0.01 |

## 聚合交易关单

- 原始地址：<https://paas.huifu.com/partners/lightning/api/jygd.md>
- SHA-256：`acb6416d691ad8e3692fd823210be97f9c1addd9c9e53a41053ae901188edc7c`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：MCS |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 数据 | `Json` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `Json` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20220905 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 开户后自动生成；示例值：[官网示例已脱敏] |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20220905 |
| `request.data.org_hf_seq_id` | `request.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原交易返回的全局流水号 | `String` | `128` | `N` | 已确认 | org_hf_seq_id，org_req_seq_id二选一；示例值：0030default220825182711P099ac1f343f00000 |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `N` | 已确认 | org_hf_seq_id，org_req_seq_id二选一；示例值：[官网示例已脱敏] |
| `request.data.merge_flag` | `request.data.merge_flag` | `—（直接 JSON 路径）` | 是否合单交易关单 | `String` | `2` | `N` | 已确认 | Y-合单交易关单，N或空-非合单交易关单。；为Y时，上送的交易信息需要是主单信息，其他情况上送子单信息 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/lightning/api/jygd.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/lightning/api/jygd.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回，示例值：20220905 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 交易时传入原样返回，示例值：rQ[官网示例已脱敏] |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20220905 |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `N` | 已确认 | 示例值：rQ[官网示例已脱敏] |
| `response.data.org_hf_seq_id` | `response.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原交易的全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：0030default220825182711P099ac1f343f00000 |
| `response.data.org_trans_stat` | `response.data.org_trans_stat` | `—（直接 JSON 路径）` | 原交易状态 | `String` | `1` | `N` | 已确认 | P：处理中、S：成功、F：失败；示例值：S |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 关单状态 | `String` | `1` | `Y` | 已确认 | P：处理中、S：成功、F：失败；示例值：S |

## 聚合交易关单查询

- 原始地址：<https://paas.huifu.com/partners/lightning/api/jygdcx.md>
- SHA-256：`57fa894392eab458c7031020c47232269c08f62aed272ee4834c7629e302184c`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：MCS |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 数据 | `Json` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `Json` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20220905 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 开户后自动生成；示例值：[官网示例已脱敏] |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20220905 |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `N` | 已确认 | org_hf_seq_id，org_req_seq_id二选一；示例值：[官网示例已脱敏] |
| `request.data.org_hf_seq_id` | `request.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原交易返回的全局流水号 | `String` | `128` | `N` | 已确认 | org_hf_seq_id，org_req_seq_id二选一；示例值：0030default220825182711P099ac1f343f00000 |
| `request.data.merge_flag` | `request.data.merge_flag` | `—（直接 JSON 路径）` | 是否合单交易关单查询 | `String` | `2` | `N` | 已确认 | Y-合单交易关单查询，N或空-非合单交易退款查询。；为Y时，上送的交易信息需要是主单信息，其他情况上送子单信息 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/lightning/api/jygdcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/lightning/api/jygdcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回，格式为yyyyMMdd，示例值：20220905 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 交易时传入，原样返回；示例值：[官网示例已脱敏] |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20220905 |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `N` | 已确认 | 示例值：rQ[官网示例已脱敏] |
| `response.data.org_hf_seq_id` | `response.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原交易的全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：0030default220825182711P099ac1f343f00000 |
| `response.data.org_trans_stat` | `response.data.org_trans_stat` | `—（直接 JSON 路径）` | 原交易状态 | `String` | `1` | `N` | 已确认 | P：处理中、S：成功、F：失败；示例值：S |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 关单状态 | `String` | `1` | `Y` | 已确认 | P：处理中、S：成功、F：失败；示例值：S |

## 聚合交易退款

- 原始地址：<https://paas.huifu.com/partners/lightning/api/jytk.md>
- SHA-256：`ed632a82bcc7d5c706c51f651fdede9e63ef7e359d2f6e2d1195c1185f55225e`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 数据 | `Json` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `Json` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20220925 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.ord_amt` | `request.data.ord_amt` | `—（直接 JSON 路径）` | 申请退款金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位；示例值：1.00，最低传入0.01；**注意：如果是原交易是延时交易，退款金额必须小于等于待确认金额** |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `Y` | 已确认 | 格式：yyyyMMdd；示例值：20220925 |
| `request.data.org_hf_seq_id` | `request.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原交易全局流水号 | `String` | `128` | `N` | 已确认 | org_hf_seq_id，org_party_order_id，org_req_seq_id三选一；示例值：0030default220825182711P099ac1f343f00000 |
| `request.data.org_party_order_id` | `request.data.org_party_order_id` | `—（直接 JSON 路径）` | 原交易微信支付宝的商户单号 | `String` | `64` | `N` | 已确认 | org_hf_seq_id，org_party_order_id，org_req_seq_id三选一；示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `N` | 已确认 | org_hf_seq_id，org_party_order_id，org_req_seq_id三选一；示例值：[官网示例已脱敏] |
| `request.data.remark` | `request.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `84` | `N` | 已确认 | 原样返回；示例值：备注 |
| `request.data.notify_url` | `request.data.notify_url` | `—（直接 JSON 路径）` | 异步通知地址 | `String` | `512` | `N` | 已确认 | 示例值： http://service.example.com/to/path |
| `request.data.tx_metadata` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 扩展参数集合 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `request.data.tx_metadata.acct_split_bunch` | `request.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `2048` | `N` | 已确认 | 分账信息，jsonObject字符串 |
| `request.data.tx_metadata.acct_split_bunch.acct_infos[]` | `request.data.acct_split_bunch` | `$.acct_infos[]` | 分账信息列表 | `Array` | `2048` | `N` | 已确认 | 分账明细 |
| `request.data.tx_metadata.acct_split_bunch.acct_infos[].div_amt` | `request.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `request.data.tx_metadata.acct_split_bunch.acct_infos[].huifu_id` | `request.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `request.data.tx_metadata.acct_split_bunch.confirm_acct_infos[]` | `request.data.acct_split_bunch` | `$.confirm_acct_infos[]` | 交易确认分账信息列表 | `Array` | `2048` | `N` | 已确认 | 交易确认分账明细 |
| `request.data.tx_metadata.acct_split_bunch.confirm_acct_infos[].confirm_hf_seq_id` | `request.data.acct_split_bunch` | `$.confirm_acct_infos[].confirm_hf_seq_id` | 交易确认单号 | `String` | `128` | `Y` | 已确认 | — |
| `request.data.tx_metadata.acct_split_bunch.confirm_acct_infos[].div_amt` | `request.data.acct_split_bunch` | `$.confirm_acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `request.data.tx_metadata.acct_split_bunch.confirm_acct_infos[].huifu_id` | `request.data.acct_split_bunch` | `$.confirm_acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `request.data.tx_metadata.combinedpay_data[]` | `request.data.combinedpay_data` | `—（String(JSON Array) 容器）` | 补贴支付信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray字符串；参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| `request.data.tx_metadata.combinedpay_data[].huifu_id` | `request.data.combinedpay_data` | `$[].huifu_id` | 汇付商户号 | `String` | `32` | `Y` | 已确认 | 渠道与一级代理商的直属商户ID |
| `request.data.tx_metadata.combinedpay_data[].user_type` | `request.data.combinedpay_data` | `$[].user_type` | 补贴方类型 | `String` | `32` | `Y` | 已确认 | channel-渠道，merchant-总部商户，agent-代理，mertomer-商户；示例值：channel |
| `request.data.tx_metadata.combinedpay_data[].acct_id` | `request.data.combinedpay_data` | `$[].acct_id` | 补贴方账户号 | `String` | `32` | `Y` | 已确认 | 营销补贴方账户号；示例值：F00598600 |
| `request.data.tx_metadata.combinedpay_data[].amount` | `request.data.combinedpay_data` | `$[].amount` | 补贴金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `request.data.tx_metadata.terminal_device_data` | `request.data.terminal_device_data` | `—（String(JSON) 容器）` | 设备信息 | `String` | `2048` | `N` | 已确认 | 设备信息，jsonObject字符串 |
| `request.data.tx_metadata.terminal_device_data.device_type` | `request.data.terminal_device_data` | `$.device_type` | 设备类型 | `String` | `2` | `N` | 已确认 | 1:手机，2:平板，3:手表，4:PC；示例值：1 |
| `request.data.tx_metadata.terminal_device_data.device_ip` | `request.data.terminal_device_data` | `$.device_ip` | 交易设备IP | `String` | `64` | `N` | 已确认 | 用于标识交易设备IP地址，绑卡设备所在的公网IP，可用于定位所属地区，；不是wifi连接时的局域网IP。；示例值：10.10.0.1（IPv4）；目前暂传IPv4格式。；ABCD:EF01:2345:6789:ABCD:EF01:2345:6789（IPv6） |
| `request.data.tx_metadata.terminal_device_data.device_mac` | `request.data.terminal_device_data` | `$.device_mac` | 交易设备MAC | `String` | `64` | `N` | 已确认 | 示例值：F0E1D2C3B4A5 |
| `request.data.tx_metadata.terminal_device_data.device_imei` | `request.data.terminal_device_data` | `$.device_imei` | 交易设备IMEI | `String` | `64` | `N` | 已确认 | 移动终端设备的唯一标识；示例值：460030912121001 |
| `request.data.tx_metadata.terminal_device_data.device_imsi` | `request.data.terminal_device_data` | `$.device_imsi` | 交易设备IMSI | `String` | `64` | `N` | 已确认 | 示例值：460030912121001 |
| `request.data.tx_metadata.terminal_device_data.device_icc_id` | `request.data.terminal_device_data` | `$.device_icc_id` | 交易设备ICCID | `String` | `64` | `N` | 已确认 | 示例值：898600680113F0123014 |
| `request.data.tx_metadata.terminal_device_data.device_wifi_mac` | `request.data.terminal_device_data` | `$.device_wifi_mac` | 交易设备WIFIMAC | `String` | `64` | `N` | 已确认 | 示例值：968778695A4B |
| `request.data.tx_metadata.terminal_device_data.device_gps` | `request.data.terminal_device_data` | `$.device_gps` | 交易设备GPS | `String` | `64` | `N` | 已确认 | 示例值：20.346790,-4.654321 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/lightning/api/jytk.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/lightning/api/jytk.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `response.data.product_id` | `response.data.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 交易时传入，原样返回；示例值：YYZY |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.org_hf_seq_id` | `response.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原交易全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00470topo1A221019132207P068ac1362af00000 |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `N` | 已确认 | 示例值：rQ[官网示例已脱敏] |
| `response.data.trans_date` | `response.data.trans_date` | `—（直接 JSON 路径）` | 退款交易发生日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `response.data.trans_time` | `response.data.trans_time` | `—（直接 JSON 路径）` | 退款交易发生时间 | `String` | `6` | `N` | 已确认 | 格式：HHMMSS，示例值：091010 代表9点10分10秒 |
| `response.data.trans_finish_time` | `response.data.trans_finish_time` | `—（直接 JSON 路径）` | 退款完成时间 | `String` | `14` | `N` | 已确认 | 格式yyyyMMddHHmmss；示例值：20091225091010 |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `1` | `N` | 已确认 | P：处理中、S：成功、F：失败；示例值：S |
| `response.data.ord_amt` | `response.data.ord_amt` | `—（直接 JSON 路径）` | 退款金额（元） | `String` | `14` | `Y` | 已确认 | 需保留小数点后两位；示例值：1.00，最低传入0.01 |
| `response.data.actual_ref_amt` | `response.data.actual_ref_amt` | `—（直接 JSON 路径）` | 实际退款金额（元） | `String` | `14` | `N` | 已确认 | 需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `84` | `N` | 已确认 | 原样返回；示例值：备注 |
| `response.data.bank_message` | `response.data.bank_message` | `—（直接 JSON 路径）` | 通道返回描述 | `String` | `256` | `N` | 已确认 | 示例值：SUCCESS |
| `response.data.fund_freeze_stat` | `response.data.fund_freeze_stat` | `—（直接 JSON 路径）` | 资金冻结状态 | `String` | `16` | `N` | 已确认 | FREEZE：冻结；UNFREEZE：解冻；示例值：UNFREEZE；退款发生时，对应原交易的资金冻结状态。 |
| `response.data.pay_channel` | `response.data.pay_channel` | `—（直接 JSON 路径）` | 交易通道 | `String` | `1` | `N` | 已确认 | 枚举值：A-支付宝、T-微信、U-银联二维码、D-数字货币 |
| `response.data.fee_amount` | `response.data.fee_amount` | `—（直接 JSON 路径）` | 退款返还手续费 | `String` | `14` | `N` | 已确认 | 单位元，保留小数点后两位，示例值：1.00 |
| `response.data.trade_type` | `response.data.trade_type` | `—（直接 JSON 路径）` | 交易类型 | `String` | `—` | `N` | [需要官方确认]：长度 | TRANS_REFUND：交易退款；目前仅该一个枚举值；示例值：TRANS_REFUND |
| `response.data.tx_metadata` | `—（官网展示分组，不存在该 wire key）` | `—（官网展示分组，不参与解码）` | 扩展参数集合 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串，此字段只为方便文档展示，实际请求时不需要传入，直接传入下层子字段 |
| `response.data.tx_metadata.acct_split_bunch` | `response.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账信息 | `String` | `2048` | `N` | 已确认 | jsonObject字符串 |
| `response.data.tx_metadata.acct_split_bunch.acct_infos[]` | `response.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `2048` | `N` | 已确认 | 分账明细 |
| `response.data.tx_metadata.acct_split_bunch.acct_infos[].div_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.tx_metadata.acct_split_bunch.acct_infos[].huifu_id` | `response.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `response.data.tx_metadata.acct_split_bunch.confirm_acct_infos[]` | `response.data.acct_split_bunch` | `$.confirm_acct_infos[]` | 交易确认分账信息列表 | `Array` | `2048` | `N` | 已确认 | 交易确认分账明细 |
| `response.data.tx_metadata.acct_split_bunch.confirm_acct_infos[].confirm_hf_seq_id` | `response.data.acct_split_bunch` | `$.confirm_acct_infos[].confirm_hf_seq_id` | 交易确认单号 | `String` | `128` | `Y` | 已确认 | — |
| `response.data.tx_metadata.acct_split_bunch.confirm_acct_infos[].div_amt` | `response.data.acct_split_bunch` | `$.confirm_acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.tx_metadata.acct_split_bunch.confirm_acct_infos[].huifu_id` | `response.data.acct_split_bunch` | `$.confirm_acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `response.data.tx_metadata.acct_split_bunch.confirm_acct_infos[].confirm_refund_status` | `response.data.acct_split_bunch` | `$.confirm_acct_infos[].confirm_refund_status` | 交易确认退款状态 | `String` | `1` | `N` | 已确认 | 交易确认退款状态P/S /F ,P:说明该笔交易确认退款为处理中，返回为空代表不走交易确认退款 |
| `response.data.tx_metadata.acct_split_bunch.fee_amount` | `response.data.acct_split_bunch` | `$.fee_amount` | 退款返还手续费 | `String` | `14` | `N` | 已确认 | 单位元，保留小数点后两位，示例值：1.00 |
| `response.data.tx_metadata.combinedpay_data[]` | `response.data.combinedpay_data` | `—（String(JSON Array) 容器）` | 补贴支付信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray字符串；参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| `response.data.tx_metadata.combinedpay_data[].huifu_id` | `response.data.combinedpay_data` | `$[].huifu_id` | 补贴方汇付编号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.tx_metadata.combinedpay_data[].user_type` | `response.data.combinedpay_data` | `$[].user_type` | 补贴方类型 | `String` | `32` | `Y` | 已确认 | 补贴方类型：channel-渠道，branch-总部/分支机构，agent-代理；示例值：channel |
| `response.data.tx_metadata.combinedpay_data[].acct_id` | `response.data.combinedpay_data` | `$[].acct_id` | 补贴方账户号 | `String` | `32` | `Y` | 已确认 | 营销补贴方账户号；示例值：F00598600 |
| `response.data.tx_metadata.combinedpay_data[].amount` | `response.data.combinedpay_data` | `$[].amount` | 补贴金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |

### 退款异步载荷（官网未标外层字段名）

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.unconfirmed_payload.resp_code` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/lightning/api/jytk.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `async.unconfirmed_payload.resp_desc` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/lightning/api/jytk.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `async.unconfirmed_payload.huifu_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.unconfirmed_payload.req_date` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `async.unconfirmed_payload.req_seq_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：rQ[官网示例已脱敏] |
| `async.unconfirmed_payload.hf_seq_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：0030default220825182711P099ac1f343f00000 |
| `async.unconfirmed_payload.org_req_date` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 原交易请求日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `async.unconfirmed_payload.org_req_seq_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 原交易请求流水号 | `String` | `128` | `N` | 已确认 | 示例值： |
| `async.unconfirmed_payload.org_ord_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 原交易订单金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.unconfirmed_payload.org_fee_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 原交易手续费 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.unconfirmed_payload.trans_date` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款交易发生日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `async.unconfirmed_payload.trans_time` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款交易发生时间 | `String` | `6` | `N` | 已确认 | 格式：HHMMSS，示例值：0910109点10分10秒 |
| `async.unconfirmed_payload.trans_finish_time` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款完成时间 | `String` | `14` | `N` | 已确认 | 格式yyyyMMddHHmmss；示例值：20091225091010 |
| `async.unconfirmed_payload.trans_type` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 交易类型 | `String` | `40` | `Y` | 已确认 | TRANS_REFUND：交易退款；目前仅该一个枚举值；示例值：TRANS_REFUND |
| `async.unconfirmed_payload.trans_stat` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 交易状态 | `String` | `1` | `N` | 已确认 | P：处理中、S：成功、F：失败；示例值： |
| `async.unconfirmed_payload.ord_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.unconfirmed_payload.actual_ref_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 实际退款金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.unconfirmed_payload.total_ref_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 原交易累计退款金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.unconfirmed_payload.total_ref_fee_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 原交易累计退款手续费金额 | `String` | `14` | `Y` | 已确认 | 单位元，示例值：1.00；注意：退还手续费规则参见[说明文档](https://paas.huifu.com/open/doc/api/#/api_tksxfsm) |
| `async.unconfirmed_payload.ref_cut` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 累计退款次数 | `String` | `14` | `Y` | 已确认 | 示例值：1 |
| `async.unconfirmed_payload.acct_split_bunch` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 分账信息 | `Object` | `4000` | `Y` | 已确认 | 分账信息 |
| `async.unconfirmed_payload.acct_split_bunch.acct_infos[]` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 分账明细 | `Array` | `2048` | `N` | 已确认 | 分账明细 |
| `async.unconfirmed_payload.acct_split_bunch.acct_infos[].div_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.unconfirmed_payload.acct_split_bunch.acct_infos[].huifu_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `async.unconfirmed_payload.acct_split_bunch.confirm_acct_infos[]` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 交易确认分账信息列表 | `Array` | `2048` | `N` | 已确认 | 交易确认分账明细 |
| `async.unconfirmed_payload.acct_split_bunch.confirm_acct_infos[].confirm_hf_seq_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 交易确认单号 | `String` | `128` | `Y` | 已确认 | — |
| `async.unconfirmed_payload.acct_split_bunch.confirm_acct_infos[].div_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.unconfirmed_payload.acct_split_bunch.confirm_acct_infos[].huifu_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `async.unconfirmed_payload.acct_split_bunch.confirm_acct_infos[].confirm_refund_status` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 交易确认退款状态 | `String` | `1` | `N` | 已确认 | 交易确认退款状态P/S /F ,P:说明该笔交易确认退款为处理中，返回为空代表不走交易确认退款 |
| `async.unconfirmed_payload.acct_split_bunch.fee_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款返还手续费 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.unconfirmed_payload.party_order_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 微信支付宝的商户单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.unconfirmed_payload.wx_response` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 微信返回的响应报文 | `Object` | `6000` | `N` | 已确认 | — |
| `async.unconfirmed_payload.wx_response.sub_appid` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 子商户公众账号ID | `String` | `32` | `N` | 已确认 | 示例值：wx[官网示例已脱敏] |
| `async.unconfirmed_payload.wx_response.sub_mch_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 子商户号 | `String` | `32` | `N` | 已确认 | 示例值：1800008315 |
| `async.unconfirmed_payload.wx_response.org_out_trans_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 微信订单号 | `String` | `32` | `N` | 已确认 | 示例值：20201030189770 |
| `async.unconfirmed_payload.wx_response.out_trans_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 微信退款单号 | `String` | `32` | `N` | 已确认 | 示例值：6545342375 |
| `async.unconfirmed_payload.wx_response.cash_fee` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 现金支付金额 | `String` | `12` | `N` | 已确认 | 现金支付金额订单现金支付金额，单位:元；示例值：1.00 |
| `async.unconfirmed_payload.wx_response.cash_refund_fee` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 现金退款金额 | `String` | `12` | `N` | 已确认 | 单位:元；示例值：1.00 |
| `async.unconfirmed_payload.wx_response.coupon_refund_fee` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 代金券退款总金额 | `String` | `12` | `N` | 已确认 | 单位:元；示例值：1.00 |
| `async.unconfirmed_payload.wx_response.coupon_refund_count` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款代金券使用数量 | `Integer` | `12` | `N` | 已确认 | 示例值：1 |
| `async.unconfirmed_payload.wx_response.refund_coupon_info[]` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款代金券信息 | `Array` | `1024` | `N` | 已确认 | 退款代金券信息 |
| `async.unconfirmed_payload.wx_response.refund_coupon_info[].coupon_type` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 代金券类型 | `String` | `8` | `N` | 已确认 | CASH--充值代金券；NO_CASH---非充值代金券；订单使用代金券时有返回，示例值：NO_CASH |
| `async.unconfirmed_payload.wx_response.refund_coupon_info[].coupon_refund_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款代金券ID | `String` | `20` | `N` | 已确认 | 示例值：4058934532 |
| `async.unconfirmed_payload.wx_response.refund_coupon_info[].coupon_refund_fee` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 单个退款代金券支付金额 | `String` | `11` | `N` | 已确认 | 单位:元，示例值：1.00 |
| `async.unconfirmed_payload.wx_response.promotion_detail[]` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 优惠详情 | `Array` | `—` | `N` | N/A：结构字段长度 | 优惠详情 |
| `async.unconfirmed_payload.wx_response.promotion_detail[].promotion_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 券ID | `String` | `32` | `Y` | 已确认 | 券或者立减优惠id；示例值：4058934532 |
| `async.unconfirmed_payload.wx_response.promotion_detail[].scope` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL- 全场代金券；SINGLE- 单品优惠；示例值：SINGLE |
| `async.unconfirmed_payload.wx_response.promotion_detail[].type` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON- 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致）；DISCOUNT- 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `async.unconfirmed_payload.wx_response.promotion_detail[].refund_amount` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 代金券退款金额 | `String` | `32` | `N` | 已确认 | 单位:元，示例值：1.00 |
| `async.unconfirmed_payload.wx_response.promotion_detail[].amount` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 代金券面额 | `String` | `32` | `N` | 已确认 | 用户享受优惠的金额，单位:元，示例值：1.00 |
| `async.unconfirmed_payload.wx_response.promotion_detail[].goods_detail[]` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 商品列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 仅使用单品优惠退款时返回，商品列表 |
| `async.unconfirmed_payload.wx_response.promotion_detail[].goods_detail[].goods_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 商品编码 | `String` | `32` | `Y` | 已确认 | 商户系统的商品编码。由半角的大小写字母、数字、中划线、下划线中的一种或几种组成，示例值：6934572310301 |
| `async.unconfirmed_payload.wx_response.promotion_detail[].goods_detail[].wxpay_goods_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 微信支付商品编码 | `String` | `32` | `N` | 已确认 | 微信支付定义的统一商品编号（没有可不传）；示例值： |
| `async.unconfirmed_payload.wx_response.promotion_detail[].goods_detail[].goods_name` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 商品名称 | `String` | `14` | `N` | 已确认 | 示例值：华为手机 |
| `async.unconfirmed_payload.wx_response.promotion_detail[].goods_detail[].refund_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 商品退款金额 | `String` | `11` | `Y` | 已确认 | 示例值：1.00 |
| `async.unconfirmed_payload.wx_response.promotion_detail[].goods_detail[].refund_quantity` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 商品退款数量 | `Integer` | `11` | `Y` | 已确认 | 示例值：1。 |
| `async.unconfirmed_payload.wx_response.promotion_detail[].goods_detail[].price` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 商品单价 | `String` | `11` | `Y` | 已确认 | 单位为：元。示例值：50.00。如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50元，则活动商品的单价应为原单价-50元 |
| `async.unconfirmed_payload.wx_response.user_received_account` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款入账账户 | `String` | `64` | `N` | 已确认 | 取当前退款单的退款入账方1）退回银行卡：{银行名称}{卡类型}{卡尾号} (示例：招商银行信用卡0403）2）退回支付用户零钱：支付用户零钱3）退还商户：商户基本账户商户结算银行账户4）退回支付用户零钱通：支付用户零钱通 |
| `async.unconfirmed_payload.dc_response` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 数字人民币响应报文 | `Object` | `2048` | `N` | 已确认 | jsonObject格式 |
| `async.unconfirmed_payload.dc_response.merchant_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 商户号 | `String` | `35` | `N` | 已确认 | 示例值：S5088295305 |
| `async.unconfirmed_payload.dc_response.sub_merchant_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 子商户号 | `String` | `35` | `N` | 已确认 | 示例值：58000001 |
| `async.unconfirmed_payload.dc_response.openid` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 用户标识 | `String` | `64` | `N` | 已确认 | 示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `async.unconfirmed_payload.dc_response.sub_openid` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 用户子标识 | `String` | `64` | `N` | 已确认 | 示例值：oWNHX5RNaCUmZR |
| `async.unconfirmed_payload.dc_response.custom_bank_code` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 客户所属运营机构代码 | `String` | `14` | `N` | 已确认 | 示例值： |
| `async.unconfirmed_payload.dc_response.custom_bank_name` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 客户所属运营机构名称 | `String` | `70` | `N` | 已确认 | 示例值： |
| `async.unconfirmed_payload.dc_response.coupon_refund_count` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款代金券使用数量 | `String` | `3` | `N` | 已确认 | 示例值：2 |
| `async.unconfirmed_payload.dc_response.coupon_refund_list[]` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款代金券集合 | `Array` | `2048` | `N` | 已确认 | — |
| `async.unconfirmed_payload.dc_response.coupon_refund_list[].id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款代金券ID | `String` | `40` | `N` | 已确认 | 示例值： |
| `async.unconfirmed_payload.dc_response.coupon_refund_list[].type` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款代金券类型 | `String` | `8` | `N` | 已确认 | 示例值： |
| `async.unconfirmed_payload.dc_response.coupon_refund_list[].amount` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 单个退款代金券支付金额 | `String` | `14` | `N` | 已确认 | 单位：元；示例值： |
| `async.unconfirmed_payload.dc_response.refund_recv_wallet_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款入账钱包ID | `String` | `22` | `N` | 已确认 | 示例值： |
| `async.unconfirmed_payload.combinedpay_data[]` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 补贴支付信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 参见《[补贴支付信息](https://paas.huifu.com/open/doc/api/#/api_zfbtxx)》 |
| `async.unconfirmed_payload.combinedpay_data[].huifu_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 补贴方汇付编号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.unconfirmed_payload.combinedpay_data[].user_type` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 补贴方类型 | `String` | `32` | `Y` | 已确认 | 补贴方类型：channel-渠道，branch-总部/分支机构，agent-代理；示例值：channel |
| `async.unconfirmed_payload.combinedpay_data[].acct_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 补贴方账户号 | `String` | `32` | `Y` | 已确认 | 营销补贴方账户号；示例值：F00598600 |
| `async.unconfirmed_payload.combinedpay_data[].amount` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 补贴金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.unconfirmed_payload.combinedpay_data_fee_info` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 补贴支付手续费承担方信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `async.unconfirmed_payload.combinedpay_data_fee_info.huifu_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 补贴支付手续费承担方汇付编号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.unconfirmed_payload.combinedpay_data_fee_info.acct_id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 补贴支付手续费承担方账户号 | `String` | `32` | `N` | 已确认 | 补贴支付手续费承担方账户号；示例值：F00598610 |
| `async.unconfirmed_payload.combinedpay_data_fee_info.combinedpay_fee_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 补贴支付手续费金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，例如：1.00,最低传入0.01； 示例值：1.01 |
| `async.unconfirmed_payload.remark` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 备注 | `String` | `1500` | `N` | 已确认 | 原样返回；示例值：备注 |
| `async.unconfirmed_payload.bank_code` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 通道返回码 | `String` | `64` | `N` | 已确认 | 示例值：01020000 |
| `async.unconfirmed_payload.bank_message` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 通道返回描述 | `String` | `256` | `N` | 已确认 | 示例值：SUCCESS |
| `async.unconfirmed_payload.unionpay_response` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 银联返回的响应报文 | `Object` | `6000` | `N` | 已确认 | Json格式 |
| `async.unconfirmed_payload.unionpay_response.coupon_info[]` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 银联优惠信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 银联使用优惠活动时出现，jsonArray格式 |
| `async.unconfirmed_payload.unionpay_response.coupon_info[].addnInfo` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 附加信息 | `String` | `100` | `N` | 已确认 | 内容自定义；示例值：附加信息 |
| `async.unconfirmed_payload.unionpay_response.coupon_info[].spnsrId` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 出资方 | `String` | `20` | `Y` | 已确认 | 00010000：银联出资；付款方作为出资方：填写8位付款方机构代码；商户作为出资方：填写15位商户代码；示例值：00010000 |
| `async.unconfirmed_payload.unionpay_response.coupon_info[].type` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 项目类型 | `String` | `4` | `Y` | 已确认 | DD01：随机立减；CP01：抵金券1：无需领取，交易时直接适配并承兑的优惠券；CP02：抵金券2：事前领取，交易时上送银联并承兑的优惠券；示例值：DD01 |
| `async.unconfirmed_payload.unionpay_response.coupon_info[].offstAmt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 抵消交易金额 | `String` | `14` | `Y` | 已确认 | 不能为全0；单位元；示例值：1.00 |
| `async.unconfirmed_payload.unionpay_response.coupon_info[].id` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 项目编号 | `String` | `40` | `N` | 已确认 | 用于票券编号等，格式自定义；示例值：938434221 |
| `async.unconfirmed_payload.unionpay_response.coupon_info[].desc` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 项目简称 | `String` | `40` | `N` | 已确认 | 优惠活动简称，可用于展示、打单等；示例值：中秋优惠促销 |
| `async.unconfirmed_payload.fund_freeze_stat` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 资金冻结状态 | `String` | `16` | `N` | 已确认 | FREEZE：冻结；UNFREEZE：解冻；示例值：UNFREEZE；退款发生时，对应原交易的资金冻结状态。 |
| `async.unconfirmed_payload.trans_fee_ref_allowance_info` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 手续费补贴返还信息 | `Object` | `—` | `N` | N/A：结构字段长度 | 手续费补贴返还信息对象，jsonObject字符串 |
| `async.unconfirmed_payload.trans_fee_ref_allowance_info.receivable_ref_fee_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款返还总手续费 | `String` | `16` | `Y` | 已确认 | 退款返还总手续费， 示例值：5.00 |
| `async.unconfirmed_payload.trans_fee_ref_allowance_info.actual_ref_fee_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款返还商户手续费 | `String` | `16` | `Y` | 已确认 | 退款返还商户手续费金额，示例值：1.00 |
| `async.unconfirmed_payload.trans_fee_ref_allowance_info.allowance_ref_fee_amt` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 退款返还补贴手续费 | `String` | `16` | `Y` | 已确认 | 退款返还补贴手续费金额，示例值：4.00 |
| `async.unconfirmed_payload.pay_channel` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 交易通道 | `String` | `1` | `N` | 已确认 | 枚举值：A-支付宝、T-微信、U-银联二维码、D-数字货币 |
| `async.unconfirmed_payload.is_confirm_refund_flag` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 是否已延迟分账 | `String` | `—` | `N` | [需要官方确认]：长度 | 是否已延迟分账 Y: 是， N-否 默认N |
| `async.unconfirmed_payload.is_refund_fee_flag` | `—（官网未标异步外层字段名）` | `—（[需要官方确认]：异步外层字段名和编码）` | 是否退还手续费 | `String` | `1` | `N` | 已确认 | 是否退还手续费，支付宝直连场景下返回,Y或者空: 退费，N-不退费 |

## 聚合交易退款查询

- 原始地址：<https://paas.huifu.com/partners/lightning/api/jytkcx.md>
- SHA-256：`9775730d9b922e856e36dd5dc3cdbc0cb37d3c29fe11049339bb8cfa3bcd7ee1`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/代理商/商户的huifu_id ；（1）当主体为渠道商/代理商时，此字段填写渠道商/代理商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `Json` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 开户自动生成；示例值：[官网示例已脱敏] |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 退款请求日期 | `String` | `8` | `C` | 已确认 | 退款发生的日期，格式为yyyyMMdd，示例值：20220925；传入退款全局流水号时，非必填，其他场景必填 |
| `request.data.org_hf_seq_id` | `request.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 退款全局流水号 | `String` | `128` | `C` | 已确认 | 退款请求流水号,退款全局流水号,终端订单号三选一不能都为空；示例值：0030default220825182711P099ac1f343f00000 |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 退款请求流水号 | `String` | `128` | `C` | 已确认 | 退款请求流水号,退款全局流水号,终端订单号三选一不能都为空；示例值：[官网示例已脱敏] |
| `request.data.mer_ord_id` | `request.data.mer_ord_id` | `—（直接 JSON 路径）` | 终端订单号 | `String` | `50` | `C` | 已确认 | 退款请求流水号,退款全局流水号,终端订单号三选一不能都为空；示例值：[官网示例已脱敏] |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/lightning/api/jytkcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/lightning/api/jytkcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.org_hf_seq_id` | `response.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 退款全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：0030default220825182711P099ac1f343f00000 |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 退款请求日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 退款请求流水号 | `String` | `128` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.ord_amt` | `response.data.ord_amt` | `—（直接 JSON 路径）` | 退款金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.actual_ref_amt` | `response.data.actual_ref_amt` | `—（直接 JSON 路径）` | 实际退款金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.trans_date` | `response.data.trans_date` | `—（直接 JSON 路径）` | 交易发生日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `response.data.trans_time` | `response.data.trans_time` | `—（直接 JSON 路径）` | 交易发生时间 | `String` | `6` | `N` | 已确认 | 格式：HHMMSS；示例值：091010 表示9点10分10秒 |
| `response.data.trade_type` | `response.data.trade_type` | `—（直接 JSON 路径）` | 交易类型 | `String` | `20` | `N` | 已确认 | 示例值：TRANS_REFUND |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `1` | `N` | 已确认 | P：处理中；S：成功；F：失败；I: 初始；初始状态很罕见，请联系汇付技术人员处理；示例值：S |
| `response.data.bank_code` | `response.data.bank_code` | `—（直接 JSON 路径）` | 通道返回码 | `String` | `64` | `N` | 已确认 | 示例值：01020000 |
| `response.data.bank_message` | `response.data.bank_message` | `—（直接 JSON 路径）` | 通道返回描述 | `String` | `256` | `N` | 已确认 | 示例值：SUCCESS |
| `response.data.fee_amount` | `response.data.fee_amount` | `—（直接 JSON 路径）` | 手续费金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.trans_finish_time` | `response.data.trans_finish_time` | `—（直接 JSON 路径）` | 退款完成时间 | `String` | `14` | `N` | 已确认 | 格式yyyyMMddHHmmss；示例值：20091225091010 |
| `response.data.pay_channel` | `response.data.pay_channel` | `—（直接 JSON 路径）` | 交易通道 | `String` | `1` | `N` | 已确认 | 枚举值：A-支付宝、T-微信、U-银联二维码、D-数字货币 |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `84` | `N` | 已确认 | 退款时上送的备注，原样返回；示例值：备注 |
| `response.data.tx_metadata` | `response.data.tx_metadata` | `—（String(JSON) 容器）` | 扩展参数集合 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.tx_metadata.acct_split_bunch` | `response.data.tx_metadata` | `$.acct_split_bunch（String(JSON) 容器）` | 分账对象 | `String` | `—` | `N` | [需要官方确认]：长度 | 分账对象，jsonObject字符串 |
| `response.data.tx_metadata.acct_split_bunch.acct_infos[]` | `response.data.tx_metadata` | `$.acct_split_bunch => JSON decode => $.acct_infos[]` | 分账信息列表 | `Array` | `2048` | `N` | 已确认 | 分账信息列表 |
| `response.data.tx_metadata.acct_split_bunch.acct_infos[].div_amt` | `response.data.tx_metadata` | `$.acct_split_bunch => JSON decode => $.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.tx_metadata.acct_split_bunch.acct_infos[].huifu_id` | `response.data.tx_metadata` | `$.acct_split_bunch => JSON decode => $.acct_infos[].huifu_id` | 商户号 | `String` | `16` | `Y` | 已确认 | 分账商户号；示例值：[官网示例已脱敏] |
| `response.data.tx_metadata.acct_split_bunch.is_clean_split` | `response.data.tx_metadata` | `$.acct_split_bunch => JSON decode => $.is_clean_split` | 是否净值分账 | `String` | `1` | `N` | 已确认 | Y:使用净值分账，仅在percentage_flag=Y时起作用；示例值：Y |
| `response.data.tx_metadata.split_fee_info` | `response.data.tx_metadata` | `$.split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 分账手续费信息 |
| `response.data.tx_metadata.split_fee_info.total_split_fee_amt` | `response.data.tx_metadata` | `$.split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费总金额(元) | `String` | `14` | `N` | 已确认 | 示例值：0.10 |
| `response.data.tx_metadata.split_fee_info.split_fee_flag` | `response.data.tx_metadata` | `$.split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费扣款标志 | `Integer` | `1` | `Y` | 已确认 | 1: 外扣 2: 内扣；示例值：1 |
| `response.data.tx_metadata.split_fee_info.split_fee_details[]` | `response.data.tx_metadata` | `$.split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费明细 | `Array` | `—` | `Y` | N/A：结构字段长度 | jsonArray格式 |
| `response.data.tx_metadata.split_fee_info.split_fee_details[].split_fee_amt` | `response.data.tx_metadata` | `$.split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费金额 | `String` | `14` | `Y` | 已确认 | 示例值：1.00 |
| `response.data.tx_metadata.split_fee_info.split_fee_details[].split_fee_huifu_id` | `response.data.tx_metadata` | `$.split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费承担方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.tx_metadata.split_fee_info.split_fee_details[].split_fee_acct_id` | `response.data.tx_metadata` | `$.split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费承担方账号 | `String` | `32` | `N` | 已确认 | 示例值：F00598600 |

## 对账单-v2详细API

- 原始地址：<https://paas.huifu.com/partners/api/doc/jyjs/api_jyjs_wjcx.md>
- SHA-256：`4ca6260c74f5f74820b645dd58935c777bea007795599bf41e974195dc2fc55f`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名 |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：MCS |
| `request.data` | `request.data` | `—（String(JSON) 容器）` | 数据 | `String` | `—` | `Y` | [需要官方确认]：长度 | JSON格式 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式:yyyyMMdd，示例值：20210811 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 请求流水号，示例值：[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 汇付客户Id | `String` | `18` | `Y` | 已确认 | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] |
| `request.data.file_date` | `request.data.file_date` | `—（直接 JSON 路径）` | 文件生成日期 | `String` | `8` | `Y` | 已确认 | 格式:yyyyMMdd，示例值：20210811；如果是调接口补生成要填写交易日期+1天（即原对账单生成日期） |
| `request.data.bill_type` | `request.data.bill_type` | `—（直接 JSON 路径）` | 文件类型 | `String` | `128` | `N` | 已确认 | TRADE_BILL-交易对账单；SPLIT_BILL-分账对账单；WITHDRAWAL_BILL-出金对账单；SETTLE_BILL-结算对账单；TRADE_BILL_MONTH-月交易对账单；SETTLE_BILL_MONTH-月结算对账单；SETTLE_USER_BILL-用户结算对账单；SETTLE_BILL_USER_MONTH-用户月结算对账单SETTLE_FUND_BILL-结算资金对账单；MERGE_BILL-合单支付对账单；示例值：TRADE_BILL |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务返回描述 | `String` | `512` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：成功 |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 原请求信息返回；示例值：20221025 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 原请求信息返回；示例值：[官网示例已脱敏]m1lqvgmjmxw8fm |
| `response.data.file_details[]` | `response.data.file_details[]` | `—（直接 JSON 路径）` | 文件信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 文件生成才会有值 |
| `response.data.file_details[].huifu_id` | `response.data.file_details[].huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 汇付商户号；示例值：[官网示例已脱敏] |
| `response.data.file_details[].file_date` | `response.data.file_details[].file_date` | `—（直接 JSON 路径）` | 文件日期 | `String` | `8` | `Y` | 已确认 | 格式:yyyyMMdd；示例值：20221025 |
| `response.data.file_details[].file_name` | `response.data.file_details[].file_name` | `—（直接 JSON 路径）` | 文件名 | `String` | `64` | `Y` | 已确认 | 文件名称；示例值：20221025_[官网示例已脱敏]_order.zip |
| `response.data.file_details[].bill_type` | `response.data.file_details[].bill_type` | `—（直接 JSON 路径）` | 文件类型 | `String` | `128` | `Y` | 已确认 | TRADE_BILL-交易对账单；SPLIT_BILL-分账对账单；WITHDRAWAL_BILL-出金对账单；SETTLE_BILL-结算对账单；TRADE_BILL_MONTH-月交易对账单；SETTLE_BILL_MONTH-月结算对账单；SETTLE_USER_BILL-用户结算对账单；SETTLE_BILL_USER_MONTH-用户月结算对账单；SETTLE_FUND_BILL-结算资金对账单；示例值：TRADE_BILL |
| `response.data.file_details[].download_url` | `response.data.file_details[].download_url` | `—（直接 JSON 路径）` | 文件http下载地址 | `String` | `2048` | `Y` | 已确认 | 示例值：[官网临时签名 URL 示例已省略] |
| `response.data.task_details[]` | `response.data.task_details[]` | `—（直接 JSON 路径）` | 文件生成任务信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 可以查看还未生成的文件，包含生成文件跑批任务的状态信息 |
| `response.data.task_details[].huifu_id` | `response.data.task_details[].huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `16` | `Y` | 已确认 | 汇付商户号；示例值：[官网示例已脱敏] |
| `response.data.task_details[].bill_type` | `response.data.task_details[].bill_type` | `—（直接 JSON 路径）` | 文件类型 | `String` | `128` | `Y` | 已确认 | TRADE_BILL-交易对账单；SPLIT_BILL-分账对账单；WITHDRAWAL_BILL-出金对账单；SETTLE_BILL-结算对账单；TRADE_BILL_MONTH-月交易对账单；SETTLE_BILL_MONTH-月结算对账单；SETTLE_USER_BILL-用户结算对账单；SETTLE_BILL_USER_MONTH-用户月结算对账单；示例值：TRADE_BILL |
| `response.data.task_details[].file_id` | `response.data.task_details[].file_id` | `—（直接 JSON 路径）` | 文件id | `String` | `128` | `N` | 已确认 | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `response.data.task_details[].file_name` | `response.data.task_details[].file_name` | `—（直接 JSON 路径）` | 文件名 | `String` | `64` | `N` | 已确认 | zip原始文件名，http下载后会有临时文件名；示例值：20221025_[官网示例已脱敏]_order.zip |
| `response.data.task_details[].download_url` | `response.data.task_details[].download_url` | `—（直接 JSON 路径）` | 文件http下载地址 | `String` | `256` | `N` | 已确认 | 示例值：[官网临时签名 URL 示例已省略] |
| `response.data.task_details[].data_date` | `response.data.task_details[].data_date` | `—（直接 JSON 路径）` | 数据日期 | `String` | `8` | `N` | 已确认 | 对账文件里的交易发生日期；示例值：20221025 |
| `response.data.task_details[].task_stat` | `response.data.task_details[].task_stat` | `—（直接 JSON 路径）` | 跑批任务状态 | `String` | `2` | `N` | 已确认 | I:初始化；P:任务处理中；DP:数据处理中；FP:文件处理中；F:失败；S:成功；示例值：S |
| `response.data.task_details[].task_start_time` | `response.data.task_details[].task_start_time` | `—（直接 JSON 路径）` | 任务开始时间 | `String` | `14` | `N` | 已确认 | 示例值：20230701145959 |
| `response.data.task_details[].task_end_time` | `response.data.task_details[].task_end_time` | `—（直接 JSON 路径）` | 任务结束时间 | `String` | `14` | `N` | 已确认 | 示例值：20230701145959 |

## H5/PC预下单

- 原始地址：<https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hosting.md>
- SHA-256：`60381ee32ab1529d05b881b2c944f8c3f130de17a7ad35a44977b166a7986eec`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 请求格式：yyyyMMdd；示例值：20221023 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 开户自动生成；示例值：[官网示例已脱敏] |
| `request.data.acct_id` | `request.data.acct_id` | `—（直接 JSON 路径）` | 收款汇付账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，示例值：A14186488；仅支持微信、支付宝、网银交易指定收款账户 |
| `request.data.trans_amt` | `request.data.trans_amt` | `—（直接 JSON 路径）` | 交易金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `request.data.goods_desc` | `request.data.goods_desc` | `—（直接 JSON 路径）` | 商品描述 | `String` | `40` | `Y` | 已确认 | 示例值：个人电脑 |
| `request.data.pre_order_type` | `request.data.pre_order_type` | `—（直接 JSON 路径）` | 预下单类型 | `String` | `1` | `Y` | 已确认 | H5/PC预先下单：1；示例值：1 |
| `request.data.delay_acct_flag` | `request.data.delay_acct_flag` | `—（直接 JSON 路径）` | 是否延迟交易 | `String` | `1` | `N` | 已确认 | Y 为延迟，N为不延迟，不传默认N；示例值：N |
| `request.data.multi_pay_way_flag` | `request.data.multi_pay_way_flag` | `—（直接 JSON 路径）` | 是否支持切换支付方式 | `String` | `1` | `N` | 已确认 | N：不支持，不允许选择支付方式后切换另一种支付方式；Y：支持，允许选择支付方式后切换另一种支付方式；注：不传时默认N，若需要对接未完成时支持切换支付方式，对账环节需选择如下方式对账；方式1：以支付成功返回的全局流水号作为对账的唯一标记；方式2：以请求流水号作为对账的唯一标记时，解析斗拱的交易账单时，应忽略请求流水号字段中“-”及“-”后的数字信息；示例值：N |
| `request.data.merge_pay_flag` | `request.data.merge_pay_flag` | `—（直接 JSON 路径）` | 是否合单支付 | `String` | `1` | `N` | 已确认 | Y-合单支付，N-非合单支付，默认N，示例值：N；合单支付，不支持切换支付方式（即multi_pay_way_flag不能为Y） |
| `request.data.sub_orders_request[]` | `request.data.sub_orders_request` | `—（String(JSON Array) 容器）` | 子单信息列表 | `String` | `—` | `N` | [需要官方确认]：长度 | 合单支付时，该字段必填；jsonArray字符串，最多支持20条，最少2条 |
| `request.data.sub_orders_request[].sub_req_seq_id` | `request.data.sub_orders_request` | `$[].sub_req_seq_id` | 子单请求流水号 | `String` | `128` | `Y` | 已确认 | 同一合单huifu_id下，当天唯一 |
| `request.data.sub_orders_request[].sub_huifu_id` | `request.data.sub_orders_request` | `$[].sub_huifu_id` | 子单商户号 | `String` | `32` | `Y` | 已确认 | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] |
| `request.data.sub_orders_request[].sub_acct_id` | `request.data.sub_orders_request` | `$[].sub_acct_id` | 子单账户号 | `String` | `9` | `N` | 已确认 | 可指定收款账户号， 仅支持基本户、现金户，不填默认为基本户 |
| `request.data.sub_orders_request[].sub_trans_amt` | `request.data.sub_orders_request` | `$[].sub_trans_amt` | 子单交易金额 | `String` | `18` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1000.00，最低传入0.01；全部子单交易金额之和等于合单交易金额。 |
| `request.data.sub_orders_request[].delay_acct_flag` | `request.data.sub_orders_request` | `$[].delay_acct_flag` | 是否延迟交易 | `String` | `1` | `N` | 已确认 | Y 为延迟 N为不延迟，不传默认N；示例值：Y |
| `request.data.sub_orders_request[].sub_remark` | `request.data.sub_orders_request` | `$[].sub_remark` | 子单备注 | `String` | `255` | `N` | 已确认 | 交易后原样返回；示例值：子单备注 |
| `request.data.acct_split_bunch` | `request.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `2000` | `N` | 已确认 | 分账对象，jsonObject字符串 |
| `request.data.acct_split_bunch.acct_infos[]` | `request.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `—` | `N` | N/A：结构字段长度 | 分账明细 |
| `request.data.acct_split_bunch.acct_infos[].div_amt` | `request.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00。；支持传入0.00，如果是全额分账，可以分给商户自身0.00元 |
| `request.data.acct_split_bunch.acct_infos[].huifu_id` | `request.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `N` | 已确认 | 斗拱开户时生成返回；示例值：[官网示例已脱敏] |
| `request.data.acct_split_bunch.acct_infos[].acct_id` | `request.data.acct_split_bunch` | `$.acct_infos[].acct_id` | 收款汇付账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，示例值：A14186488；仅支持微信、支付宝、网银交易指定收款账户 |
| `request.data.acct_split_bunch.acct_infos[].percentage_div` | `request.data.acct_split_bunch` | `$.acct_infos[].percentage_div` | 分账百分比% | `String` | `6` | `N` | 已确认 | 示例值：23.50，表示23.50%。仅在percentage_flag=Y时起作用；acct_infos中全部分账百分比只和必须为100.00%。 |
| `request.data.acct_split_bunch.percentage_flag` | `request.data.acct_split_bunch` | `$.percentage_flag` | 百分比分账标志 | `String` | `1` | `N` | 已确认 | Y:使用百分比分账；示例值：Y |
| `request.data.acct_split_bunch.is_clean_split` | `request.data.acct_split_bunch` | `$.is_clean_split` | 是否净值分账 | `String` | `1` | `N` | 已确认 | Y:使用净值分账，仅在交易手续费内扣且使用百分比分账时起作用；示例值：Y |
| `request.data.hosting_data` | `request.data.hosting_data` | `—（String(JSON) 容器）` | 统一收银台扩展参数集合 | `String` | `2000` | `Y` | 已确认 | jsonObject统一收银台扩展参数集合 |
| `request.data.hosting_data.project_title` | `request.data.hosting_data` | `$.project_title` | 项目标题 | `String` | `64` | `Y` | 已确认 | 用于账单页面显示；示例值：汇付收银台 |
| `request.data.hosting_data.project_id` | `request.data.hosting_data` | `$.project_id` | 项目号 | `String` | `32` | `Y` | 已确认 | 商户创建的项目号；示例值：PROJECTID[官网示例已脱敏] |
| `request.data.hosting_data.private_info` | `request.data.hosting_data` | `$.private_info` | 商户私有信息 | `String` | `255` | `N` | 已确认 | 对应异步通知和主动查询接口中的remark字段；示例值：收取服务费 |
| `request.data.hosting_data.callback_url` | `request.data.hosting_data` | `$.callback_url` | 回调地址 | `String` | `512` | `N` | 已确认 | 若不填，支付成功后停留在当前页面，填写后跳转回指定地址；示例值：https://paas.huifu.com |
| `request.data.hosting_data.request_type` | `request.data.hosting_data` | `$.request_type` | 请求类型 | `String` | `1` | `C` | 已确认 | P:PC页面版，默认：P；M:H5页面版；指定交易类型时必填；示例值：M |
| `request.data.time_expire` | `request.data.time_expire` | `—（直接 JSON 路径）` | 交易失效时间 | `String` | `14` | `N` | 已确认 | 请求格式：yyyyMMddHHmmss；示例值：20220912111230；注意:为空默认失效时间为10分钟；用户在交易失效时间后完成交易有可能被关单。最终结果以异步为准；建议商户在交易量大时，或在搞营销活动时将失效时间设置短一些。 |
| `request.data.biz_info` | `request.data.biz_info` | `—（String(JSON) 容器）` | 业务信息 | `String` | `2000` | `N` | 已确认 | jsonObject格式；交易相关的信息 |
| `request.data.biz_info.payer_check_ali` | `request.data.biz_info` | `$.payer_check_ali` | 付款人验证（支付宝） | `Object` | `—` | `N` | N/A：结构字段长度 | 支付宝特殊交易需验证买家信息；如彩票行业等；当前只支持AT类交易有验证功能 |
| `request.data.biz_info.payer_check_ali.need_check_info` | `request.data.biz_info` | `$.payer_check_ali.need_check_info` | 是否提供校验身份信息 | `String` | `1` | `N` | 已确认 | T：强制校验，需要填写person_payer字段；F：不强制；示例值：T |
| `request.data.biz_info.payer_check_ali.min_age` | `request.data.biz_info` | `$.payer_check_ali.min_age` | 允许的最小买家年龄 | `String` | `3` | `N` | 已确认 | 买家年龄必须大于等于所传数值。示例值：18；注：1. need_check_info=T 时该参数才有效，；2. min_age 为整数，必须大于等于 0 |
| `request.data.biz_info.payer_check_ali.fix_buyer` | `request.data.biz_info` | `$.payer_check_ali.fix_buyer` | 是否强制校验付款人身份信息 | `String` | `8` | `N` | 已确认 | 用户进行实名认证校验；T：强制校验，F：不强制；示例值：T |
| `request.data.biz_info.payer_check_wx` | `request.data.biz_info` | `$.payer_check_wx` | 付款人验证（微信） | `Object` | `—` | `N` | N/A：结构字段长度 | 微信实名支付需验证买家信息；如彩票行业等；当前只支持AT类交易有验证功能 |
| `request.data.biz_info.payer_check_wx.limit_payer` | `request.data.biz_info` | `$.payer_check_wx.limit_payer` | 指定支付者 | `String` | `5` | `N` | 已确认 | 上传此参数，可限制用户只有是成年人才能支付，；值：ADULT；示例值：ADULT |
| `request.data.biz_info.payer_check_wx.real_name_flag` | `request.data.biz_info` | `$.payer_check_wx.real_name_flag` | 微信实名验证 | `String` | `1` | `N` | 已确认 | Y/N；默认N；示例值：Y |
| `request.data.biz_info.person_payer` | `request.data.biz_info` | `$.person_payer` | 个人付款人信息 | `Object` | `—` | `N` | N/A：结构字段长度 | 付款人验证打开后需要填写付款人信息，但非必填；微信/支付宝共用字段 |
| `request.data.biz_info.person_payer.name` | `request.data.biz_info` | `$.person_payer.name` | 姓名 | `String` | `16` | `N` | 已确认 | 注：支付宝交易need_check_info=T时，该参数才有效；示例值：张三 |
| `request.data.biz_info.person_payer.cert_type` | `request.data.biz_info` | `$.person_payer.cert_type` | 证件类型 | `String` | `32` | `N` | 已确认 | 身份证：IDENTITY_CARD，（微信只支持身份证）；护照：PASSPORT；军官证：OFFICER_CARD，；士兵证：SOLDIER_CARD；户口本：HOKOU；微信/支付宝共用字段；示例值：IDENTITY_CARD ；注：支付宝交易need_check_info=T时，该参数才有效 |
| `request.data.biz_info.person_payer.cert_no` | `request.data.biz_info` | `$.person_payer.cert_no` | 证件号 | `String` | `64` | `N` | 已确认 | 注：支付宝交易need_check_info=T时，该参数才有效；需要密文传输，请参考[加密解密说明](https://paas.huifu.com/open/doc/guide/#/api_jiami_jiemi)使用汇付RSA公钥加密。；示例值：Mc5pjf+b/Keyi/t/wnH……MfYQnK7Lzw== |
| `request.data.biz_info.person_payer.mobile` | `request.data.biz_info` | `$.person_payer.mobile` | 手机号 | `String` | `20` | `N` | 已确认 | 支付宝字段；注：该参数暂不校验；示例值：[官网示例已脱敏] |
| `request.data.notify_url` | `request.data.notify_url` | `—（直接 JSON 路径）` | 交易异步通知地址 | `String` | `512` | `N` | 已确认 | http或https开头，示例值：https://callback.service.com/xx；在交易成功/失败时触发回调，正常情况下只会触发一次，具体回调策略参见[链接](https://paas.huifu.com/open/doc/api_standard/#/ybxx/jiekouguifan_ybxx) |
| `request.data.usage_type` | `request.data.usage_type` | `—（直接 JSON 路径）` | 使用类型 | `String` | `1` | `N` | 已确认 | P-支付（默认）； R-充值；示例值：P |
| `request.data.trans_type` | `request.data.trans_type` | `—（直接 JSON 路径）` | 交易类型 | `String` | `256` | `N` | 已确认 | 支持同时上送多个支付类型（多个时，使用英文逗号分割），上送多个或未传值时进入收银台，上送单个时直接到支付页；T_JSAPI: 微信公众号支付；支付PC、H5场景；A_JSAPI: 支付宝JS；支付PC、H5场景；A_NATIVE: 支付宝正扫；支付PC、H5场景；U_NATIVE: 银联正扫；支付PC、H5场景；U_JSAPI: 银联 JS；支付PC、H5场景；ONLINE_PAY_B2B：B2B网银支付；支付PC场景；ONLINE_PAY_B2C：B2C网银支付；支付PC场景；QUICK_PAY：快捷支付；支付PC、H5场景；LARGE_PAY：备付金下单模式；支付PC、H5场景；Y_H5：抖音H5支付；支付H5场景；示例值：A_JSAPI；**注意：[指定网银支付首次跳转银行页面需要打开浏览器弹窗限制](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/imgs/hosting/%E6%B5%8F%E8%A7%88%E5%99%A8%E5%85%81%E8%AE%B8%E5%BC%B9%E7%AA%97%E9%85%8D%E7%BD%AE.png)** |
| `request.data.wx_data` | `request.data.wx_data` | `—（String(JSON) 容器）` | 微信参数集合 | `String` | `2048` | `N` | 已确认 | jsonObject字符串 |
| `request.data.wx_data.attach` | `request.data.wx_data` | `$.attach` | 附加数据 | `String` | `127` | `N` | 已确认 | 在查询api和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据；示例值：附加数据 |
| `request.data.wx_data.detail` | `request.data.wx_data` | `$.detail` | 商品详情 | `Object` | `6000` | `N` | 已确认 | 单品优惠功能字段 |
| `request.data.wx_data.detail.cost_price` | `request.data.wx_data` | `$.detail.cost_price` | 订单原价(元) | `String` | `12` | `N` | 已确认 | 1.商户侧一张小票订单可能被分多次支付，订单原价用于记录整张小票的交易金额。 ；2.当订单原价与支付金额不相等，则不享受优惠。；3.该字段主要用于防止同一张小票分多次支付，以享受多次优惠的情况，正常支付订单不必上传此参数。；示例值：999.00 |
| `request.data.wx_data.detail.receipt_id` | `request.data.wx_data` | `$.detail.receipt_id` | 商品小票ID | `String` | `32` | `N` | 已确认 | 商家小票 ID；示例值：[官网示例已脱敏] |
| `request.data.wx_data.detail.goods_detail[]` | `request.data.wx_data` | `$.detail.goods_detail[]` | 单品列表 | `Array` | `2048` | `Y` | 已确认 | 单品信息，使用Json数组格式提交 |
| `request.data.wx_data.detail.goods_detail[].goods_id` | `request.data.wx_data` | `$.detail.goods_detail[].goods_id` | 商品编码 | `String` | `32` | `N` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `request.data.wx_data.detail.goods_detail[].goods_name` | `request.data.wx_data` | `$.detail.goods_detail[].goods_name` | 商品名称 | `String` | `256` | `N` | 已确认 | 商品的实际名称；示例值：太龙双黄连口服液 |
| `request.data.wx_data.detail.goods_detail[].price` | `request.data.wx_data` | `$.detail.goods_detail[].price` | 商品单价(元) | `String` | `12` | `N` | 已确认 | 如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔 100 元的订单使用了商场发的优惠券 100-50，则活动商品的单价应为原单价-50；示例值：43.00 |
| `request.data.wx_data.detail.goods_detail[].quantity` | `request.data.wx_data` | `$.detail.goods_detail[].quantity` | 商品数量 | `Int` | `11` | `N` | 已确认 | 用户购买的数量；示例值：1 |
| `request.data.wx_data.detail.goods_detail[].wxpay_goods_id` | `request.data.wx_data` | `$.detail.goods_detail[].wxpay_goods_id` | 微信侧商品编码 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.wx_data.goods_tag` | `request.data.wx_data` | `$.goods_tag` | 订单优惠标记 | `String` | `32` | `N` | 已确认 | 代金券或立减优惠功能的参数；示例值：WXG |
| `request.data.wx_data.receipt` | `request.data.wx_data` | `$.receipt` | 开发票入口开放标识 | `String` | `8` | `N` | 已确认 | 示例值：Y |
| `request.data.wx_data.scene_info` | `request.data.wx_data` | `$.scene_info` | 场景信息 | `Object` | `2048` | `N` | 已确认 | 该字段用于上报场景信息，目前支持上报实际门店信息。 |
| `request.data.wx_data.scene_info.store_info` | `request.data.wx_data` | `$.scene_info.store_info` | 门店信息 | `Object` | `2048` | `N` | 已确认 | 门店信息 |
| `request.data.wx_data.scene_info.store_info.id` | `request.data.wx_data` | `$.scene_info.store_info.id` | 门店id | `String` | `32` | `N` | 已确认 | 门店编号，由商户自定义；示例值：sh001 |
| `request.data.wx_data.scene_info.store_info.name` | `request.data.wx_data` | `$.scene_info.store_info.name` | 门店名称 | `String` | `64` | `N` | 已确认 | 门店名称，由商户自定义；示例值：上海宝山分店 |
| `request.data.wx_data.scene_info.store_info.area_code` | `request.data.wx_data` | `$.scene_info.store_info.area_code` | 门店行政区划码 | `String` | `6` | `N` | 已确认 | 门店所在地行政区划码，详见[行政区划代码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)，示例值：310101 |
| `request.data.wx_data.scene_info.store_info.address` | `request.data.wx_data` | `$.scene_info.store_info.address` | 门店详细地址 | `String` | `128` | `N` | 已确认 | 门店详细地址，由商户自定义；示例值：上海宝山区共富路100号 |
| `request.data.wx_data.promotion_flag` | `request.data.wx_data` | `$.promotion_flag` | 单品优惠标识 | `String` | `1` | `N` | 已确认 | Y-是，N-否，默认否；直连模式需要填写；示例值：Y；若使用单品优惠，该字段必填，若该字段为Y，则商品详情【detail】必填 |
| `request.data.wx_data.product_id` | `request.data.wx_data` | `$.product_id` | 新增商品ID | `String` | `32` | `N` | 已确认 | 直连模式【trade_type】=T_NATIVE支付的时候必填；示例值： |
| `request.data.alipay_data` | `request.data.alipay_data` | `—（String(JSON) 容器）` | 支付宝参数集合 | `String` | `2048` | `N` | 已确认 | jsonObject字符串 |
| `request.data.alipay_data.alipay_store_id` | `request.data.alipay_data` | `$.alipay_store_id` | 支付宝的店铺编号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.alipay_data.extend_params` | `request.data.alipay_data` | `$.extend_params` | 业务扩展参数 | `Object` | `2048` | `N` | 已确认 | 业务扩展参数 |
| `request.data.alipay_data.extend_params.card_type` | `request.data.alipay_data` | `$.extend_params.card_type` | 卡类型 | `String` | `32` | `N` | 已确认 | 示例值：S0JP0000 |
| `request.data.alipay_data.extend_params.food_order_type` | `request.data.alipay_data` | `$.extend_params.food_order_type` | 支付宝点餐场景类型 | `String` | `20` | `N` | 已确认 | QR_ORDER（店内扫码点餐）；PRE_ORDER（预点到店自提）；HOME_DELIVERY（外送到家）；DIRECT_PAYMENT（直接付款）；QR_FOOD_ORDER（点餐先付）；P_QR_FOOD_ORDER（点餐后付）；SELF_PICK（门店自提）；TAKE_OUT （餐饮外卖）；OTHER（其他）；该参数只适用于支付宝支付窗交易接口；示例值：TAKE_OUT |
| `request.data.alipay_data.extend_params.hb_fq_num` | `request.data.alipay_data` | `$.extend_params.hb_fq_num` | 花呗分期数 | `String` | `5` | `N` | 已确认 | 使用花呗分期要进行的分期数；示例值：3 |
| `request.data.alipay_data.extend_params.hb_fq_seller_percent` | `request.data.alipay_data` | `$.extend_params.hb_fq_seller_percent` | 花呗卖家手续费百分比 | `String` | `3` | `N` | 已确认 | 使用花呗分期需要卖家承担的手续费比，单位比例的百分值。； 花呗商贴支付默认传0，示例值：0 |
| `request.data.alipay_data.extend_params.industry_reflux_info` | `request.data.alipay_data` | `$.extend_params.industry_reflux_info` | 行业数据回流信息 | `String` | `64` | `N` | 已确认 | 示例值：{\"scene_code\":\"metro_tradeorder\",\"channel\":\"xxxx\",\"scene_data\":{\"asset_name\":\"ALIPAY\"}} |
| `request.data.alipay_data.extend_params.fq_channels` | `request.data.alipay_data` | `$.extend_params.fq_channels` | 信用卡分期资产方式 | `String` | `20` | `N` | 已确认 | 代表优先使用资产类型；alipayfq_cc：表示信⽤卡分期，为空时默认花呗。示例值：alipayfq_cc |
| `request.data.alipay_data.extend_params.parking_id` | `request.data.alipay_data` | `$.extend_params.parking_id` | 停车场id | `String` | `28` | `N` | 已确认 | isv停车场id、向支付宝停车平台申请获得的支付宝停车场的唯一标识；示例值：PI[官网示例已脱敏] |
| `request.data.alipay_data.extend_params.sys_service_provider_id` | `request.data.alipay_data` | `$.extend_params.sys_service_provider_id` | 系统商编号 | `String` | `64` | `N` | 已确认 | 该参数作为系统商返佣数据提取的依据，请填写系统商签约协议的pid；示例值：[官网示例已脱敏] |
| `request.data.alipay_data.goods_detail[]` | `request.data.alipay_data` | `$.goods_detail[]` | 订单包含的商品列表信息 | `Array` | `2048` | `N` | 已确认 | 订单包含的商品列表信息 |
| `request.data.alipay_data.goods_detail[].goods_id` | `request.data.alipay_data` | `$.goods_detail[].goods_id` | 商品的编号 | `String` | `32` | `Y` | 已确认 | 示例值：apple-01 |
| `request.data.alipay_data.goods_detail[].goods_name` | `request.data.alipay_data` | `$.goods_detail[].goods_name` | 商品名称 | `String` | `256` | `Y` | 已确认 | 示例值：ipad |
| `request.data.alipay_data.goods_detail[].price` | `request.data.alipay_data` | `$.goods_detail[].price` | 商品单价(元) | `String` | `16` | `Y` | 已确认 | 单位：元；示例值：43.40 |
| `request.data.alipay_data.goods_detail[].quantity` | `request.data.alipay_data` | `$.goods_detail[].quantity` | 商品数量 | `String` | `10` | `Y` | 已确认 | 示例值：40 |
| `request.data.alipay_data.goods_detail[].body` | `request.data.alipay_data` | `$.goods_detail[].body` | 商品描述信息 | `String` | `1000` | `N` | 已确认 | 示例值：个人电脑 |
| `request.data.alipay_data.goods_detail[].categories_tree` | `request.data.alipay_data` | `$.goods_detail[].categories_tree` | 商品类目树 | `String` | `128` | `N` | 已确认 | 商品类目树，从商品类目根节点到叶子节点的类目 id 组成，类目 id 值使用\ |
| `request.data.alipay_data.goods_detail[].goods_category` | `request.data.alipay_data` | `$.goods_detail[].goods_category` | 商品类目 | `String` | `24` | `N` | 已确认 | 示例值：34543238 |
| `request.data.alipay_data.goods_detail[].show_url` | `request.data.alipay_data` | `$.goods_detail[].show_url` | 商品的展示地址 | `String` | `400` | `N` | 已确认 | 示例值：https://paas.huifu.com/checkout/demo/pc/goodsDetail.html |
| `request.data.alipay_data.merchant_order_no` | `request.data.alipay_data` | `$.merchant_order_no` | 商户原始订单号 | `String` | `32` | `N` | 已确认 | 示例值：39045032345 |
| `request.data.alipay_data.operator_id` | `request.data.alipay_data` | `$.operator_id` | 商户操作员编号 | `String` | `28` | `N` | 已确认 | 示例值：carl.li@huifu.com |
| `request.data.alipay_data.product_code` | `request.data.alipay_data` | `$.product_code` | 销售产品码 | `String` | `32` | `N` | 已确认 | 示例值：YYZY |
| `request.data.alipay_data.seller_id` | `request.data.alipay_data` | `$.seller_id` | 卖家支付宝用户号 | `String` | `28` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.alipay_data.store_id` | `request.data.alipay_data` | `$.store_id` | 商户门店编号 | `String` | `32` | `N` | 已确认 | 示例值：sh1001 |
| `request.data.alipay_data.subject` | `request.data.alipay_data` | `$.subject` | 订单标题 | `String` | `256` | `N` | 已确认 | 直连模式必填；商品的标题/交易标题/订单标题/订单关键字等，是请求时对应的参数，原样通知回来；示例值：红果奶茶 |
| `request.data.alipay_data.store_name` | `request.data.alipay_data` | `$.store_name` | 商家门店名称 | `String` | `512` | `N` | 已确认 | 直连模式字段；示例值：红果奶茶上海宝山店 |
| `request.data.alipay_data.ali_business_params` | `request.data.alipay_data` | `$.ali_business_params（String(JSON) 容器）` | 商户业务信息 | `String` | `512` | `N` | 已确认 | 商户传入业务信息，具体值要和支付宝约定将商户传入信息分发给相应系统，应用于安全，营销等参数直传场景，格式为JSONObject |
| `request.data.alipay_data.fq_mer_discount_flag` | `request.data.alipay_data` | `$.fq_mer_discount_flag` | 商户贴息标记 | `String` | `1` | `N` | 已确认 | 花呗分期商户补贴活动，Y：商户全额贴息，P：商户部分贴息，不传为非商户贴息（默认）；示例值：P；选择P：商户部分贴息活动，需同时在【ali_business_params：商户业务信息】中传入支付宝约定的活动参数，参数说明详见分期支付指引文档。 |
| `request.data.dy_data` | `request.data.dy_data` | `—（String(JSON) 容器）` | 抖音参数集合 | `String` | `2048` | `N` | 已确认 | jsonObject字符串 |
| `request.data.dy_data.sub_appid` | `request.data.dy_data` | `$.sub_appid` | 子商户应用ID | `String` | `32` | `Y` | 已确认 | 子商户/二级商户在抖音开放平台申请的应用ID，全局唯一。；此处请填写移动应用类型的AppID，并确保该sub_appid与sub_mchid有绑定关系。；示例值：awofz9bncda6x7w8 |
| `request.data.dy_data.coupon_info` | `request.data.dy_data` | `$.coupon_info（String(JSON) 容器）` | 优惠标记 | `String` | `1024` | `N` | 已确认 | 1、json格式。和抖音支付协商后可用。；2、传参说明：；（1）业务场景区分，可通过传入key值=biz_scene，value值为约定场景值。；（2）个性化策略区分，可通过传入key值=product_tag，value值为约定参数值。；（3）指定优惠信息区分，可通过传入key值=assign_discounts，value值为“抖音支付优惠查询接口”返回的“指定优惠信息”字段值。；示例值：{"biz_scene":"xxx","product_tag":"xxx","assign_discounts":"xxx"} |
| `request.data.dy_data.h5_info` | `request.data.dy_data` | `$.h5_info` | H5场景信息 | `Object` | `2048` | `Y` | 已确认 | H5场景信息 |
| `request.data.dy_data.h5_info.type` | `request.data.dy_data` | `$.h5_info.type` | 场景类型 | `String` | `32` | `Y` | 已确认 | Ios, Android, Wap示例值：Ios |
| `request.data.dy_data.h5_info.app_name` | `request.data.dy_data` | `$.h5_info.app_name` | 应用名称 | `String` | `64` | `N` | 已确认 | 示例值：抖音 |
| `request.data.dy_data.h5_info.app_url` | `request.data.dy_data` | `$.h5_info.app_url` | 网站URL | `String` | `128` | `N` | 已确认 | 示例值：示例值：https://douyinpay.com/ |
| `request.data.dy_data.h5_info.bundle_id` | `request.data.dy_data` | `$.h5_info.bundle_id` | iOS平台BundleID | `String` | `128` | `N` | 已确认 | iOS平台BundleID |
| `request.data.dy_data.h5_info.package_name` | `request.data.dy_data` | `$.h5_info.package_name` | Android平台PackageName | `String` | `128` | `N` | 已确认 | Android平台PackageName |
| `request.data.dy_data.scene_info` | `request.data.dy_data` | `$.scene_info` | 场景信息 | `Object` | `2048` | `Y` | 已确认 | 支付场景描述 |
| `request.data.dy_data.scene_info.payer_client_ip` | `request.data.dy_data` | `$.scene_info.payer_client_ip` | 用户终端IP | `String` | `45` | `Y` | 已确认 | 用户的客户端IP，支持IPv4和IPv6两种格式的IP地址；示例值：14.23.150.211 |
| `request.data.unionpay_data` | `request.data.unionpay_data` | `—（String(JSON) 容器）` | 银联参数集合 | `String` | `2048` | `N` | 已确认 | jsonObject字符串 |
| `request.data.unionpay_data.addn_data` | `request.data.unionpay_data` | `$.addn_data` | 收款方附加数据 | `String` | `3000` | `N` | 已确认 | 请参考[银联收款方附加数据(addn_data)说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylcsjh#银联收款方附加数据(addn_data)) |
| `request.data.unionpay_data.area_info` | `request.data.unionpay_data` | `$.area_info` | 地区信息 | `String` | `32` | `N` | 已确认 | 示例值：310000 |
| `request.data.unionpay_data.front_url` | `request.data.unionpay_data` | `$.front_url` | 前台通知地址 | `String` | `200` | `N` | 已确认 | 收款方向银联推送订单时上送的前台通知地址（仅允许为外网地址）；用户完成支付点击“返回”后，银联通过浏览器post请求到该地址。；示例值：http://www.huifu.com |
| `request.data.unionpay_data.payee_comments` | `request.data.unionpay_data` | `$.payee_comments` | 收款方附言 | `String` | `100` | `N` | 已确认 | 示例值：业务收款 |
| `request.data.unionpay_data.payee_info` | `request.data.unionpay_data` | `$.payee_info` | 收款方信息 | `Object` | `2048` | `N` | 已确认 | 收款方信息 |
| `request.data.unionpay_data.payee_info.mer_cat_code` | `request.data.unionpay_data` | `$.payee_info.mer_cat_code` | 商户类别 | `String` | `4` | `N` | 已确认 | [参考银联商户类别](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylshlb)；示例值：0101 |
| `request.data.unionpay_data.payee_info.sub_id` | `request.data.unionpay_data` | `$.payee_info.sub_id` | 二级商户代码 | `String` | `20` | `N` | 已确认 | 示例值：823586070110039 |
| `request.data.unionpay_data.payee_info.sub_name` | `request.data.unionpay_data` | `$.payee_info.sub_name` | 二级商户名称 | `String` | `100` | `N` | 已确认 | 示例值：上海白乐门酒店 |
| `request.data.unionpay_data.payee_info.term_id` | `request.data.unionpay_data` | `$.payee_info.term_id` | 终端号 | `String` | `8` | `N` | 已确认 | 示例值：58000001 |
| `request.data.unionpay_data.pnr_ins_id_cd` | `request.data.unionpay_data` | `$.pnr_ins_id_cd` | 银联分配的服务商机构标识码 | `String` | `11` | `N` | 已确认 | 示例值：01008330 |
| `request.data.unionpay_data.req_reserved` | `request.data.unionpay_data` | `$.req_reserved` | 请求方自定义域 | `String` | `500` | `N` | 已确认 | 示例值： |
| `request.data.unionpay_data.term_info` | `request.data.unionpay_data` | `$.term_info` | 终端信息 | `String` | `32` | `N` | 已确认 | 示例值： |
| `request.data.unionpay_data.pid_info` | `request.data.unionpay_data` | `$.pid_info => [需要官方确认]：String 子表编码` | 服务商信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 服务商信息 |
| `request.data.unionpay_data.pid_info.pnr_order_id` | `request.data.unionpay_data` | `$.pid_info => [需要官方确认]：String 子表编码` | 服务商订单编号 | `String` | `40` | `N` | 已确认 | 服务商自定义并发送，同一交易日期内不可重复，订单编号将作为服务商和银联对账的唯一索引，不超过40字节的变长字母和/或数字字符，不能含“-”或“_” |
| `request.data.unionpay_data.pid_info.pid_sct` | `request.data.unionpay_data` | `$.pid_info => [需要官方确认]：String 子表编码` | 服务商密文 | `String` | `8` | `N` | 已确认 | 由服务商根据服务商代码标识加密算法生成 |
| `request.data.unionpay_data.pid_info.trade_scene` | `request.data.unionpay_data` | `$.pid_info => [需要官方确认]：String 子表编码` | 场景标识 | `String` | `8` | `N` | 已确认 | 取值如下:1-扫码点餐示例值：1 |
| `request.data.terminal_device_data` | `request.data.terminal_device_data` | `—（String(JSON) 容器）` | 设备信息 | `String` | `2048` | `N` | 已确认 | jsonObject字符串 |
| `request.data.terminal_device_data.devs_id` | `request.data.terminal_device_data` | `$.devs_id` | 汇付机具号 | `String` | `32` | `Y` | 已确认 | 通过汇付报备的机具必传；示例值：[官网示例已脱敏] |
| `request.data.largeamt_data` | `request.data.largeamt_data` | `—（String(JSON) 容器）` | 大额支付参数集合 | `String` | `2500` | `N` | 已确认 | jsonObject字符串 |
| `request.data.largeamt_data.certificate_name` | `request.data.largeamt_data` | `$.certificate_name` | 付款方名称 | `String` | `64` | `N` | 已确认 | 要素校验时使用；使用大额支付三要素校验时必填；示例值：上海汇付支付有限公司 |
| `request.data.largeamt_data.bank_card_no` | `request.data.largeamt_data` | `$.bank_card_no` | 付款方银行卡号 | `String` | `2048` | `N` | 已确认 | 要素校验时使用，使用大额支付四要素校验时必填；原文最大为19位，密文最大长度为2048；使用斗拱公钥做RSA加密；示例值：b9LE5RccVVLChrHgo9lvp……PhWhjKrWg2NPfbe0mkQ== |
| `request.data.fee_sign` | `request.data.fee_sign` | `—（直接 JSON 路径）` | 手续费场景标识 | `String` | `32` | `N` | 已确认 | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。；示例值：6850aad1e92f4244a74a42fcc1ad6360 |
| `request.data.fee_split_flag` | `request.data.fee_split_flag` | `—（直接 JSON 路径）` | 是否交易手续费分摊 | `String` | `1` | `N` | 已确认 | Y-分摊，N-不分摊，不传默认为N。示例值：N |
| `request.data.fee_flag` | `request.data.fee_flag` | `—（直接 JSON 路径）` | 手续费扣款标志 | `String` | `1` | `N` | 已确认 | 1: 外扣 2: 内扣 (默认取控台配置值)；示例值：1 |
| `request.data.channel_no` | `request.data.channel_no` | `—（直接 JSON 路径）` | 渠道号 | `String` | `32` | `N` | 已确认 | 如果交易走自有渠道请联系联调群运维人员获取；示例值:10000001 |
| `request.data.pay_scene` | `request.data.pay_scene` | `—（直接 JSON 路径）` | 场景类型 | `String` | `2` | `N` | 已确认 | 取值参见[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E5%BE%AE%E4%BF%A1%E4%B8%9A%E5%8A%A1%E5%BC%80%E9%80%9A%E7%B1%BB%E5%9E%8B)说明；示例值:02；pay_scene需和channel_no配合使用。在指定channel_no的情况下需要传入pay_scene取值；为空取默认配置 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hosting.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `128` | `Y` | 已确认 | 业务返回描述；示例值：处理成功 |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：20221023 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：[官网示例已脱敏] |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：[官网示例已脱敏] |
| `response.data.pre_order_type` | `response.data.pre_order_type` | `—（直接 JSON 路径）` | 预下单类型 | `String` | `1` | `Y` | 已确认 | H5/PC预先下单：1；示例值：1 |
| `response.data.pre_order_id` | `response.data.pre_order_id` | `—（直接 JSON 路径）` | 预下单ID | `String` | `64` | `Y` | 已确认 | 示例值：H[官网示例已脱敏] |
| `response.data.goods_desc` | `response.data.goods_desc` | `—（直接 JSON 路径）` | 商品描述 | `String` | `40` | `Y` | 已确认 | 示例值：个人电脑 |
| `response.data.jump_url` | `response.data.jump_url` | `—（直接 JSON 路径）` | 支付跳转链接 | `String` | `256` | `Y` | 已确认 | 直接跳转当前链接唤起支付；示例值：https://callback.service.com/xx |
| `response.data.usage_type` | `response.data.usage_type` | `—（直接 JSON 路径）` | 订单类型 | `String` | `1` | `N` | 已确认 | P-支付 R-充值 默认：P-支付；示例值：P |
| `response.data.trans_type` | `response.data.trans_type` | `—（直接 JSON 路径）` | 交易类型 | `String` | `256` | `N` | 已确认 | 支持同时上送多个支付类型，上送多个或未传值时进入收银台，上送单个时直接到支付页；T_JSAPI: 微信公众号支付；支付PC、H5场景；A_JSAPI: 支付宝JS；支付PC、H5场景；A_NATIVE: 支付宝正扫；支付PC、H5场景；U_NATIVE: 银联正扫；支付PC、H5场景；U_JSAPI: 银联 JS；支付PC、H5场景；ONLINE_PAY_B2B：B2B网银支付；支付PC场景；ONLINE_PAY_B2C：B2C网银支付；支付PC场景；QUICK_PAY：快捷支付；支付PC、H5场景；LARGE_PAY：备付金下单模式；支付PC、H5场景；Y_H5：抖音H5支付；支付H5场景；示例值：A_JSAPI；**注意：[指定网银支付首次跳转银行页面需要打开浏览器弹窗限制](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/imgs/hosting/%E6%B5%8F%E8%A7%88%E5%99%A8%E5%85%81%E8%AE%B8%E5%BC%B9%E7%AA%97%E9%85%8D%E7%BD%AE.png)** |
| `response.data.hosting_data` | `response.data.hosting_data` | `—（String(JSON) 容器）` | 统一收银台扩展参数集合 | `String` | `2000` | `Y` | 已确认 | jsonObject统一收银台扩展参数集合 |
| `response.data.hosting_data.project_title` | `response.data.hosting_data` | `$.project_title` | 项目标题 | `String` | `64` | `Y` | 已确认 | 用于账单页面显示；示例值：汇付收银台 |
| `response.data.hosting_data.project_id` | `response.data.hosting_data` | `$.project_id` | 项目号 | `String` | `32` | `Y` | 已确认 | 商户创建的项目号；示例值：PROJECTID[官网示例已脱敏] |
| `response.data.hosting_data.private_info` | `response.data.hosting_data` | `$.private_info` | 商户私有信息 | `String` | `255` | `N` | 已确认 | 对应异步通知和主动查询接口中的remark字段；示例值：收取服务费 |
| `response.data.hosting_data.callback_url` | `response.data.hosting_data` | `$.callback_url` | 回调地址 | `String` | `512` | `N` | 已确认 | 若不填，支付成功后停留在当前页面，填写后跳转回指定地址；示例值：https://paas.huifu.com |
| `response.data.hosting_data.request_type` | `response.data.hosting_data` | `$.request_type` | 请求类型 | `String` | `1` | `C` | 已确认 | P:PC页面版，默认：P；M:H5页面版；指定交易类型时必填；示例值：M |
| `response.data.current_time` | `response.data.current_time` | `—（直接 JSON 路径）` | 系统响应时间 | `String` | `14` | `Y` | 已确认 | 格式：yyyyMMddHHmmss示例值：20231215090052 |
| `response.data.time_expire` | `response.data.time_expire` | `—（直接 JSON 路径）` | 交易失效时间 | `String` | `14` | `Y` | 已确认 | 格式：yyyyMMddHHmmss；示例值：20231215090052 |

### 支付异步 resp_data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.resp_data.resp_code` | `async.resp_data` | `$.resp_code` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hosting.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：00000000 |
| `async.resp_data.resp_desc` | `async.resp_data` | `$.resp_desc` | 业务返回信息 | `String` | `512` | `Y` | 已确认 | 业务返回描述；示例值：处理成功 |
| `async.resp_data.req_seq_id` | `async.resp_data` | `$.req_seq_id` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 交易时传入，原样返回；示例值：[官网示例已脱敏] |
| `async.resp_data.req_date` | `async.resp_data` | `$.req_date` | 请求时间 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回，格式为yyyyMMdd，示例值：20091225 |
| `async.resp_data.hf_seq_id` | `async.resp_data` | `$.hf_seq_id` | 汇付全局流水号 | `String` | `40` | `N` | 已确认 | 示例值：00470topo1A211015160805P090ac132fef00000 |
| `async.resp_data.out_trans_id` | `async.resp_data` | `$.out_trans_id` | 用户账单上的交易订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.resp_data.party_order_id` | `async.resp_data` | `$.party_order_id` | 用户账单上的商户订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.resp_data.huifu_id` | `async.resp_data` | `$.huifu_id` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.trans_type` | `async.resp_data` | `$.trans_type` | 交易类型 | `String` | `20` | `N` | 已确认 | T_JSAPI: 微信公众号支付；支付PC、H5场景；A_JSAPI: 支付宝JS；支付H5场景；A_NATIVE: 支付宝正扫；支付PC场景；U_NATIVE: 银联正扫；支付PC场景；U_JSAPI: 银联 JS；支付H5场景；ONLINE_PAY_B2B：B2B网银支付；支付PC场景；ONLINE_PAY_B2C：B2C网银支付；支付PC场景；QUICK_PAY：快捷支付；支付PC、H5场景；Y_H5：抖音H5支付；支付H5场景；示例值：A_JSAPI |
| `async.resp_data.trans_amt` | `async.resp_data` | `$.trans_amt` | 交易金额 | `String` | `12` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.resp_data.settlement_amt` | `async.resp_data` | `$.settlement_amt` | 结算金额 | `String` | `16` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.resp_data.trans_stat` | `async.resp_data` | `$.trans_stat` | 交易状态 | `String` | `1` | `N` | 已确认 | S：成功、F：失败；示例值：S |
| `async.resp_data.trans_finish_time` | `async.resp_data` | `$.trans_finish_time` | 汇付侧交易完成时间 | `String` | `13` | `N` | 已确认 | 毫秒时间戳，示例值：1791598928000 |
| `async.resp_data.end_time` | `async.resp_data` | `$.end_time` | 支付完成时间 | `String` | `14` | `N` | 已确认 | 格式yyyyMMddHHmmss，示例值：20091225091010 |
| `async.resp_data.acct_date` | `async.resp_data` | `$.acct_date` | 入账时间 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20091225 |
| `async.resp_data.debit_flag` | `async.resp_data` | `$.debit_flag` | 借贷记标识 | `String` | `1` | `N` | 已确认 | D-借记卡 C-信用卡 Z-借贷合一卡；示例值：C |
| `async.resp_data.user_huifu_id` | `async.resp_data` | `$.user_huifu_id` | 用户号 | `String` | `32` | `N` | 已确认 | 汇付分配的用户号快捷支付时才有值；示例值：[官网示例已脱敏] |
| `async.resp_data.wx_user_id` | `async.resp_data` | `$.wx_user_id` | 微信用户唯一标识码 | `String` | `128` | `N` | 已确认 | 示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk= |
| `async.resp_data.wx_response` | `async.resp_data` | `$.wx_response` | 微信返回的响应报文 | `Object` | `6000` | `N` | 已确认 | jsonObject格式 |
| `async.resp_data.wx_response.sub_appid` | `async.resp_data` | `$.wx_response.sub_appid` | 子商户公众账号ID | `String` | `32` | `N` | 已确认 | 微信分配的子商户公众账号ID；示例值：wxec280d4c8a1cc2ca |
| `async.resp_data.wx_response.openid` | `async.resp_data` | `$.wx_response.openid` | 用户标识 | `String` | `128` | `Y` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `async.resp_data.wx_response.sub_openid` | `async.resp_data` | `$.wx_response.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `async.resp_data.wx_response.bank_type` | `async.resp_data` | `$.wx_response.bank_type` | 付款银行 | `String` | `16` | `Y` | 已确认 | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/wiki/doc/apiv3/terms_definition/chapter1_1_3.shtml#part-7)；示例值：OTHERS |
| `async.resp_data.wx_response.cash_fee` | `async.resp_data` | `$.wx_response.cash_fee` | 现金支付金额 | `String` | `12` | `N` | 已确认 | 订单现金支付金额；示例值：10.00 |
| `async.resp_data.wx_response.coupon_fee` | `async.resp_data` | `$.wx_response.coupon_fee` | 代金券金额 | `String` | `12` | `N` | 已确认 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：1.00 |
| `async.resp_data.wx_response.attach` | `async.resp_data` | `$.wx_response.attach` | 商家数据包 | `String` | `128` | `N` | 已确认 | 原样返回；示例值：附加数据 |
| `async.resp_data.wx_response.promotion_detail[]` | `async.resp_data` | `$.wx_response.promotion_detail[]` | 营销详情列表 | `Array` | `6000` | `N` | 已确认 | 营销详情列表，使返回值为Json格式 |
| `async.resp_data.wx_response.promotion_detail[].promotion_id` | `async.resp_data` | `$.wx_response.promotion_detail[].promotion_id` | 券或者立减优惠id | `String` | `32` | `Y` | 已确认 | 示例值：2345234235 |
| `async.resp_data.wx_response.promotion_detail[].name` | `async.resp_data` | `$.wx_response.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `async.resp_data.wx_response.promotion_detail[].scope` | `async.resp_data` | `$.wx_response.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL: 全场代金券，SINGLE: 单品优惠；示例值：SINGLE |
| `async.resp_data.wx_response.promotion_detail[].type` | `async.resp_data` | `$.wx_response.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON: 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致） ；DISCOUNT: 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `async.resp_data.wx_response.promotion_detail[].amount` | `async.resp_data` | `$.wx_response.promotion_detail[].amount` | 优惠券面额 | `String` | `5` | `Y` | 已确认 | 用户享受优惠的金额；示例值：10.00 |
| `async.resp_data.wx_response.promotion_detail[].activity_id` | `async.resp_data` | `$.wx_response.promotion_detail[].activity_id` | 活动ID | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `async.resp_data.wx_response.promotion_detail[].merchant_contribute` | `async.resp_data` | `$.wx_response.promotion_detail[].merchant_contribute` | 商户出资 | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；示例值：10.00 |
| `async.resp_data.wx_response.promotion_detail[].other_contribute` | `async.resp_data` | `$.wx_response.promotion_detail[].other_contribute` | 其他出资 | `String` | `32` | `N` | 已确认 | 其他出资方出资金额，单位为元；示例值：5.00 |
| `async.resp_data.wx_response.promotion_detail[].goods_detail` | `async.resp_data` | `$.wx_response.promotion_detail[].goods_detail` | 单品列表 | `Object` | `3000` | `N` | 已确认 | 使用Json格式 |
| `async.resp_data.wx_response.promotion_detail[].goods_detail.goods_id` | `async.resp_data` | `$.wx_response.promotion_detail[].goods_detail.goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `async.resp_data.wx_response.promotion_detail[].goods_detail.goods_remark` | `async.resp_data` | `$.wx_response.promotion_detail[].goods_detail.goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。示例值：商品备注 |
| `async.resp_data.wx_response.promotion_detail[].goods_detail.discount_amount` | `async.resp_data` | `$.wx_response.promotion_detail[].goods_detail.discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，单位为：元；示例值：20.00 |
| `async.resp_data.wx_response.promotion_detail[].goods_detail.quantity` | `async.resp_data` | `$.wx_response.promotion_detail[].goods_detail.quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `async.resp_data.wx_response.promotion_detail[].goods_detail.price` | `async.resp_data` | `$.wx_response.promotion_detail[].goods_detail.price` | 商品价格 | `String` | `32` | `Y` | 已确认 | 单位为: 元。示例值：50.00；如果商户有优惠，需传输商户优惠后的单价(例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50) |
| `async.resp_data.alipay_response` | `async.resp_data` | `$.alipay_response` | 支付宝返回的响应报文 | `Object` | `6000` | `N` | 已确认 | jsonObject格式 |
| `async.resp_data.alipay_response.voucher_detail_list[]` | `async.resp_data` | `$.alipay_response.voucher_detail_list[]` | 优惠券信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 本交易支付时使用的所有优惠券信息 |
| `async.resp_data.alipay_response.voucher_detail_list[].id` | `async.resp_data` | `$.alipay_response.voucher_detail_list[].id` | 券id | `String` | `32` | `Y` | 已确认 | 示例值：6934572310301 |
| `async.resp_data.alipay_response.voucher_detail_list[].name` | `async.resp_data` | `$.alipay_response.voucher_detail_list[].name` | 券名称 | `String` | `32` | `Y` | 已确认 | 示例值：实体店付款通用立减券 |
| `async.resp_data.alipay_response.voucher_detail_list[].type` | `async.resp_data` | `$.alipay_response.voucher_detail_list[].type` | 券类型 | `String` | `32` | `Y` | 已确认 | 当前有三种类型： ；ALIPAY_FIX_VOUCHER: 全场代金券；ALIPAY_DISCOUNT_VOUCHER: 折扣券；ALIPAY_ITEM_VOUCHER: 单品优惠 ；示例值：ALIPAY_ITEM_VOUCHER；注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码 |
| `async.resp_data.alipay_response.voucher_detail_list[].amount` | `async.resp_data` | `$.alipay_response.voucher_detail_list[].amount` | 优惠券面额（元） | `String` | `8` | `Y` | 已确认 | 它应该会等于商家出资加上其他出资方出资；示例值：10.00 |
| `async.resp_data.alipay_response.voucher_detail_list[].merchant_contribute` | `async.resp_data` | `$.alipay_response.voucher_detail_list[].merchant_contribute` | 商家出资 | `String` | `8` | `N` | 已确认 | 特指发起交易的商家出资金额；示例值：10.00 |
| `async.resp_data.alipay_response.voucher_detail_list[].other_contribute` | `async.resp_data` | `$.alipay_response.voucher_detail_list[].other_contribute` | 其他出资方出资金额 | `String` | `11` | `N` | 已确认 | 可能是支付宝、品牌商、第三方，也可能是他们的一起出资；示例值：0.00 |
| `async.resp_data.alipay_response.fund_bill_list` | `async.resp_data` | `$.alipay_response.fund_bill_list（String(JSON) 容器）` | 支付金额信息 | `String` | `512` | `N` | 已确认 | 支付成功的各个渠道金额信息，详见资金明细信息说明；json格式 |
| `async.resp_data.alipay_response.fund_bill_list.bank_code` | `async.resp_data` | `$.alipay_response.fund_bill_list => JSON decode => $.bank_code` | 银行代码 | `String` | `10` | `N` | 已确认 | 银行卡支付时的银行代码；示例值：CEB；请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
| `async.resp_data.alipay_response.buyer_id` | `async.resp_data` | `$.alipay_response.buyer_id` | 买家的支付宝唯一用户号 | `String` | `28` | `N` | 已确认 | 2088开头的16位纯数字；示例值：[官网示例已脱敏] |
| `async.resp_data.alipay_response.buyer_logon_id` | `async.resp_data` | `$.alipay_response.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com |
| `async.resp_data.alipay_response.hb_fq_num` | `async.resp_data` | `$.alipay_response.hb_fq_num` | 花呗分期数 | `String` | `10` | `N` | 已确认 | 示例值：3 |
| `async.resp_data.alipay_response.hb_fq_seller_percent` | `async.resp_data` | `$.alipay_response.hb_fq_seller_percent` | 卖家承担的手续费 | `String` | `3` | `N` | 已确认 | 示例值：1.00 |
| `async.resp_data.unionpay_response` | `async.resp_data` | `$.unionpay_response` | 银联返回的响应报文 | `Object` | `6000` | `N` | 已确认 | jsonObject格式 |
| `async.resp_data.unionpay_response.coupon_info` | `async.resp_data` | `$.unionpay_response.coupon_info` | 银联优惠信息 | `Object` | `—` | `N` | N/A：结构字段长度 | 优惠信息，银联使用优惠活动时出现，json格式 |
| `async.resp_data.unionpay_response.coupon_info.addnInfo` | `async.resp_data` | `$.unionpay_response.coupon_info.addnInfo` | 附加信息 | `String` | `100` | `N` | 已确认 | 内容自定义；示例值：附加信息 |
| `async.resp_data.unionpay_response.coupon_info.spnsr_id` | `async.resp_data` | `$.unionpay_response.coupon_info.spnsr_id` | 出资方 | `String` | `20` | `Y` | 已确认 | 00010000：银联出资，示例值：00010000；未来将增加付款方等出资方 |
| `async.resp_data.unionpay_response.coupon_info.type` | `async.resp_data` | `$.unionpay_response.coupon_info.type` | 项目类型 | `String` | `4` | `Y` | 已确认 | DD01：随机立减， CP01：抵金券；示例值：CP01 |
| `async.resp_data.unionpay_response.coupon_info.offst_amt` | `async.resp_data` | `$.unionpay_response.coupon_info.offst_amt` | 抵消交易金额 | `String` | `12` | `Y` | 已确认 | 不能为全0；示例值：1.00 |
| `async.resp_data.unionpay_response.coupon_info.id` | `async.resp_data` | `$.unionpay_response.coupon_info.id` | 项目编号 | `String` | `40` | `N` | 已确认 | 用于票券编号等，格式自定义；示例值：938434221 |
| `async.resp_data.unionpay_response.coupon_info.desc` | `async.resp_data` | `$.unionpay_response.coupon_info.desc` | 项目简称 | `String` | `40` | `N` | 已确认 | 优惠活动简称，可用于展示、打单等；示例值：中秋优惠促销 |
| `async.resp_data.dy_response` | `async.resp_data` | `$.dy_response（String(JSON) 容器）` | 抖音返回的响应报文 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `async.resp_data.dy_response.sub_appid` | `async.resp_data` | `$.dy_response => JSON decode => $.sub_appid` | 子商户应用ID | `String` | `32` | `N` | 已确认 | 在抖音开放平台申请的应用ID，全局唯一。此处请填写移动应用（APP）/网站应用（H5）类型的AppID |
| `async.resp_data.dy_response.openid` | `async.resp_data` | `$.dy_response => JSON decode => $.openid` | 用户标识 | `String` | `128` | `Y` | 已确认 | 用户在商户appid下的唯一标识；示例值：897ae8bd9f194107-9cb3-85f5672037de |
| `async.resp_data.dy_response.sub_openid` | `async.resp_data` | `$.dy_response => JSON decode => $.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：823ae8bd9f893402-9cb3-85f8794657ea |
| `async.resp_data.dy_response.bank_type` | `async.resp_data` | `$.dy_response => JSON decode => $.bank_type` | 付款银行 | `String` | `16` | `Y` | 已确认 | 银行类型，采用字符串类型的银行标识示例值：OTHERS |
| `async.resp_data.dy_response.promotion_detail` | `async.resp_data` | `$.dy_response.promotion_detail（String(JSON) 容器）` | 营销详情列表 | `String` | `—` | `N` | [需要官方确认]：长度 | 营销详情列表，使返回值为Json格式 |
| `async.resp_data.dy_response.promotion_detail.coupon_id` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.coupon_id` | 券id | `String` | `32` | `N` | 已确认 | 券或者立减优惠id；示例值：2345234235 |
| `async.resp_data.dy_response.promotion_detail.name` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `async.resp_data.dy_response.promotion_detail.scope` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL: 全场代金券，SINGLE: 单品优惠；示例值：GLOBAL |
| `async.resp_data.dy_response.promotion_detail.type` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.type` | 优惠类型 | `String` | `32` | `N` | 已确认 | CASH: 充值型代金券；NOCASH：免充值型代金券；示例值：CASH |
| `async.resp_data.dy_response.promotion_detail.amount` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.amount` | 优惠券面额 | `String` | `12` | `Y` | 已确认 | 示例值：5.00 |
| `async.resp_data.dy_response.promotion_detail.stock_id` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.stock_id` | 活动ID | `String` | `32` | `N` | 已确认 | 活动ID |
| `async.resp_data.dy_response.promotion_detail.douyinpay_contribute` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.douyinpay_contribute` | 抖音出资 | `String` | `32` | `N` | 已确认 | 抖音出资，单位为元；示例值：10.00 |
| `async.resp_data.dy_response.promotion_detail.merchant_contribute` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.merchant_contribute` | 商户出资 | `String` | `32` | `N` | 已确认 | 商户出资，单位为元；示例值：10.00 |
| `async.resp_data.dy_response.promotion_detail.other_contribute` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.other_contribute` | 其他出资 | `String` | `32` | `N` | 已确认 | 其他出资，单位为元；示例值：20.00 |
| `async.resp_data.dy_response.promotion_detail.currency` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.currency` | 优惠币种 | `String` | `32` | `N` | 已确认 | CNY：人民币，境内商户号仅支持人民币 |
| `async.resp_data.dy_response.promotion_detail.goods_detail[]` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.goods_detail[]` | 单品列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 单品信息，使用Json格式，是promotion_detail的元素 |
| `async.resp_data.dy_response.promotion_detail.goods_detail[].goods_id` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.goods_detail[].goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `async.resp_data.dy_response.promotion_detail.goods_detail[].quantity` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.goods_detail[].quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `async.resp_data.dy_response.promotion_detail.goods_detail[].unit_price` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.goods_detail[].unit_price` | 商品单价 | `String` | `32` | `N` | 已确认 | 单位为:元。示例值：99.00 |
| `async.resp_data.dy_response.promotion_detail.goods_detail[].discount_amount` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.goods_detail[].discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，单位为：元；示例值：20.00 |
| `async.resp_data.dy_response.promotion_detail.goods_detail[].goods_remark` | `async.resp_data` | `$.dy_response.promotion_detail => JSON decode => $.goods_detail[].goods_remark` | 商品备注 | `String` | `128` | `N` | 已确认 | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。；示例值：商品备注 |
| `async.resp_data.is_div` | `async.resp_data` | `$.is_div` | 是否分账交易 | `String` | `1` | `Y` | 已确认 | 1: 分账交易, 0: 非分账交易；示例值：1 |
| `async.resp_data.acct_split_bunch` | `async.resp_data` | `$.acct_split_bunch（String(JSON) 容器）` | 分账对象 | `String` | `2048` | `N` | 已确认 | 分账对象，jsonObject字符串 |
| `async.resp_data.acct_split_bunch.acct_infos[]` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[]` | 分账明细 | `Array` | `2048` | `Y` | 已确认 | 分账明细 |
| `async.resp_data.acct_split_bunch.acct_infos[].div_amt` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.resp_data.acct_split_bunch.acct_infos[].huifu_id` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `async.resp_data.acct_split_bunch.acct_infos[].acct_id` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[].acct_id` | 收款汇付账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，示例值：A14186488；仅支持微信、支付宝、网银交易指定收款账户 |
| `async.resp_data.acct_split_bunch.acct_infos[].acct_date` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[].acct_date` | 账务日期 | `String` | `8` | `N` | 已确认 | 示例值：20221023 |
| `async.resp_data.is_delay_acct` | `async.resp_data` | `$.is_delay_acct` | 是否延时交易 | `String` | `1` | `Y` | 已确认 | 1: 延迟 0: 不延迟；示例值：1 |
| `async.resp_data.fee_flag` | `async.resp_data` | `$.fee_flag` | 手续费扣款标志 | `Int` | `1` | `N` | 已确认 | 1: 外扣，2: 内扣；默认返回控台配置方式；示例值：2 |
| `async.resp_data.fee_amount` | `async.resp_data` | `$.fee_amount` | 手续费金额 | `String` | `16` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.resp_data.trans_fee_allowance_info` | `async.resp_data` | `$.trans_fee_allowance_info` | 手续费补贴信息 | `Object` | `6000` | `N` | 已确认 | jsonObject格式 |
| `async.resp_data.trans_fee_allowance_info.receivable_fee_amt` | `async.resp_data` | `$.trans_fee_allowance_info.receivable_fee_amt` | 商户应收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `async.resp_data.trans_fee_allowance_info.actual_fee_amt` | `async.resp_data` | `$.trans_fee_allowance_info.actual_fee_amt` | 商户实收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `async.resp_data.trans_fee_allowance_info.allowance_fee_amt` | `async.resp_data` | `$.trans_fee_allowance_info.allowance_fee_amt` | 补贴手续费 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `async.resp_data.trans_fee_allowance_info.allowance_type` | `async.resp_data` | `$.trans_fee_allowance_info.allowance_type` | 补贴类型 | `String` | `10` | `N` | 已确认 | 0：不补贴，为空默认；1：补贴；2：部分补贴；3：全额补贴(优惠后)；4：部分补贴(优惠后)；示例值：2 |
| `async.resp_data.trans_fee_allowance_info.no_allowance_desc` | `async.resp_data` | `$.trans_fee_allowance_info.no_allowance_desc` | 不补贴原因 | `String` | `128` | `N` | 已确认 | 补贴系统返回的不补贴原因；1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴；2:额度用完；3:不在有效期；4:活动不存在；5:手续费金额为0不补贴；6:顶格优惠；7:额度不足；8:手续费后补；9:未达到起始补贴金额；示例值：2 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos` | 手续费补贴活动详情 | `Object` | `—` | `N` | N/A：结构字段长度 | 补贴系统返回，斗拱原样返回 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.acct_id` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.acct_id` | 门店 | `String` | `64` | `N` | 已确认 | 示例值：sh002 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.merchant_group` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.merchant_group` | 商户号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys` | 补贴方 | `String` | `64` | `Y` | 已确认 | 1:银行 2:服务商 3:汇来米；示例值：1 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys_id` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys_id` | 补贴方ID | `String` | `64` | `Y` | 已确认 | 对应补贴方的id；示例值：[官网示例已脱敏] |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.is_delay_allowance` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.is_delay_allowance` | 补贴类型 | `String` | `2` | `Y` | 已确认 | 1:实补 2:后补,默认实补；示例值：1 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_id` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.market_id` | 自定义活动编号 | `String` | `64` | `Y` | 已确认 | 示例值：ISFE00232 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_name` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.market_name` | 自定义活动名称 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_desc` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.market_desc` | 自定义活动描述 | `String` | `64` | `N` | 已确认 | 示例值：新店开业大促 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.start_time` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.start_time` | 活动开始时间 | `String` | `8` | `Y` | 已确认 | yyyyMMdd；示例值：20220909 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.end_time` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.end_time` | 活动结束时间 | `String` | `8` | `Y` | 已确认 | yyyyMMdd；示例值：20220913 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_debit_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.pos_debit_limit_amt` | pos借记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：2.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_credit_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.pos_credit_limit_amt` | pos贷记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.pos_limit_amt` | pos补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.qr_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.qr_limit_amt` | 扫码补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.total_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.total_limit_amt` | 活动总补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：10.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.status` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.status` | 活动是否有效 | `String` | `4` | `Y` | 已确认 | 1:生效 0：失效；示例值：1 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.human_flag` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.human_flag` | 是否人工操作 | `String` | `4` | `Y` | 已确认 | N：自动 Y：人工；示例值：N |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.activity_id` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.activity_id` | 活动号 | `String` | `64` | `Y` | 已确认 | 示例值：223402342 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.activity_name` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.activity_name` | 活动描述 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.create_by` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.create_by` | 创建人 | `String` | `32` | `Y` | 已确认 | 示例值：Lg[官网示例已脱敏] |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.create_time` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.create_time` | 创建时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 22:00:30 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.update_time` | `async.resp_data` | `$.trans_fee_allowance_info.cur_allowance_config_infos.update_time` | 更新时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 23:00:30 |
| `async.resp_data.remark` | `async.resp_data` | `$.remark` | 备注 | `String` | `45` | `N` | 已确认 | 原样返回；示例值：备注 |
| `async.resp_data.bank_code` | `async.resp_data` | `$.bank_code` | 通道返回码 | `String` | `32` | `N` | 已确认 | 示例值：00 |
| `async.resp_data.bank_message` | `async.resp_data` | `$.bank_message` | 通道返回描述 | `String` | `200` | `N` | 已确认 | 示例值：成功[0000000] |
| `async.resp_data.bank_id` | `async.resp_data` | `$.bank_id` | 收款方银行代号 | `String` | `8` | `N` | 已确认 | 快捷、网银返回；示例值：01040000 |
| `async.resp_data.bank_extend_param` | `async.resp_data` | `$.bank_extend_param（String(JSON) 容器）` | 银行扩展信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject格式；网银返回 |
| `async.resp_data.bank_extend_param.gate_type` | `async.resp_data` | `$.bank_extend_param => JSON decode => $.gate_type` | 网关支付类型 | `String` | `2` | `N` | 已确认 | 01: 个人网关02:企业网关；示例值：02 |
| `async.resp_data.bank_extend_param.bank_id` | `async.resp_data` | `$.bank_extend_param => JSON decode => $.bank_id` | 付款方银行号 | `String` | `32` | `N` | 已确认 | 示例值：01040000 |
| `async.resp_data.bank_extend_param.pyer_acct_id` | `async.resp_data` | `$.bank_extend_param => JSON decode => $.pyer_acct_id` | 付款方银行账户 | `String` | `1024` | `N` | 已确认 | B2B支付成功后可能返回密文；示例值：[官网示例已脱敏] |
| `async.resp_data.bank_extend_param.pyer_acct_nm` | `async.resp_data` | `$.bank_extend_param => JSON decode => $.pyer_acct_nm` | 付款方银行账户名 | `String` | `128` | `N` | 已确认 | 示例值：上海汇付支付有限公司 |
| `async.resp_data.fee_formula_infos[]` | `async.resp_data` | `$.fee_formula_infos（String(JSON Array) 容器）` | 手续费费率信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray格式；微信、支付宝、云闪付交易成功时返回手续费费率信息 |
| `async.resp_data.fee_formula_infos[].fee_formula` | `async.resp_data` | `$.fee_formula_infos => JSON decode => $[].fee_formula` | 手续费计算公式 | `String` | `512` | `Y` | 已确认 | 示例值：AMT*0.003 |
| `async.resp_data.fee_formula_infos[].fee_type` | `async.resp_data` | `$.fee_formula_infos => JSON decode => $[].fee_type` | 手续费类型 | `String` | `32` | `Y` | 已确认 | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；示例值：ACCT_FEE |
| `async.resp_data.fee_formula_infos[].huifu_id` | `async.resp_data` | `$.fee_formula_infos => JSON decode => $[].huifu_id` | 商户号 | `String` | `32` | `N` | 已确认 | 补贴支付账户补贴时，补贴账户的huifuId；示例值：[官网示例已脱敏] |
| `async.resp_data.fee_formula_infos[].fee_sign` | `async.resp_data` | `$.fee_formula_infos => JSON decode => $[].fee_sign` | 手续费场景标识 | `String` | `32` | `N` | 已确认 | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。；示例值：6850aad1e92f4244a74a42fcc1ad6360 |
| `async.resp_data.order_type` | `async.resp_data` | `$.order_type` | 订单类型 | `String` | `1` | `N` | 已确认 | P-支付 R-充值 默认：P-支付；示例值：P |
| `async.resp_data.devs_id` | `async.resp_data` | `$.devs_id` | 汇付机具号 | `String` | `32` | `Y` | 已确认 | 通过汇付报备的机具必传；示例值：[官网示例已脱敏] |
| `async.resp_data.request_ip` | `async.resp_data` | `$.request_ip` | 请求IP | `String` | `15` | `N` | 已确认 | 付款方IP,仅在支付成功后返回;示例：192.168.1.1 |
| `async.resp_data.sub_orders_response[]` | `async.resp_data` | `$.sub_orders_response（String(JSON Array) 容器）` | 子单信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray格式；子单信息，合单支付的订单返回该字段 |
| `async.resp_data.sub_orders_response[].sub_req_seq_id` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_req_seq_id` | 子单请求流水号 | `String` | `128` | `Y` | 已确认 | 交易时传入，原样返回；示例值：SUB[官网示例已脱敏] |
| `async.resp_data.sub_orders_response[].sub_hf_seq_id` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_hf_seq_id` | 子单全局流水号 | `String` | `128` | `Y` | 已确认 | 示例值：00470topo1A221019132207P068ac1362af00001 |
| `async.resp_data.sub_orders_response[].sub_huifu_id` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_huifu_id` | 子单商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.sub_orders_response[].sub_acct_id` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_acct_id` | 子单账户号 | `String` | `9` | `Y` | 已确认 | 示例值：A123456 |
| `async.resp_data.sub_orders_response[].sub_trams_amt` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_trams_amt` | 子单交易金额 | `String` | `14` | `Y` | 已确认 | 位元；示例值：1.00 |
| `async.resp_data.sub_orders_response[].sub_settlement_amt` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_settlement_amt` | 子单结算金额 | `String` | `14` | `N` | 已确认 | 位元；示例值：1.00 |
| `async.resp_data.sub_orders_response[].sub_remark` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_remark` | 子单备注信息 | `String` | `255` | `N` | 已确认 | 原样返回；示例值：子单备注 |
| `async.resp_data.sub_orders_response[].acct_date` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].acct_date` | 子单入账日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20091225 |
| `async.resp_data.sub_orders_response[].acct_stat` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].acct_stat` | 子单账务状态 | `String` | `1` | `N` | 已确认 | "I：初始"; "P:处理中"; "S:成功"; "F:失败。示例值：S； 返回“I：初始”状态时，请联系客服确认订单问题 |
| `async.resp_data.sub_orders_response[].is_div` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].is_div` | 是否分账交易 | `String` | `1` | `N` | 已确认 | 1:分账交易， 0:非分账交易；示例值：1 |
| `async.resp_data.sub_orders_response[].acct_split_bunch` | `async.resp_data` | `$.sub_orders_response[].acct_split_bunch（String(JSON) 容器）` | 分账对象 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `async.resp_data.sub_orders_response[].acct_split_bunch.acct_infos[]` | `async.resp_data` | `$.sub_orders_response[].acct_split_bunch.acct_infos（String(JSON Array) 容器）` | 分账明细 | `String` | `—` | `Y` | [需要官方确认]：长度 | jsonArray分账明细 |
| `async.resp_data.sub_orders_response[].acct_split_bunch.acct_infos[].div_amt` | `async.resp_data` | `$.sub_orders_response[].acct_split_bunch.acct_infos => JSON decode => $[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 ，最低传入0.01 |
| `async.resp_data.sub_orders_response[].acct_split_bunch.acct_infos[].huifu_id` | `async.resp_data` | `$.sub_orders_response[].acct_split_bunch.acct_infos => JSON decode => $[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `async.resp_data.sub_orders_response[].acct_split_bunch.acct_infos[].acct_id` | `async.resp_data` | `$.sub_orders_response[].acct_split_bunch.acct_infos => JSON decode => $[].acct_id` | 分账接收方账户号 | `String` | `9` | `N` | 已确认 | 示例值：A123456 |
| `async.resp_data.sub_orders_response[].fee_infos` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 交易手续费信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 交易手续费信息 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_formula` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 手续费计算公式 | `String` | `512` | `N` | 已确认 | 示例值：AMT\*0.003 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_huifu_id` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 手续费扣款商户号 | `String` | `32` | `N` | 已确认 | — |
| `async.resp_data.sub_orders_response[].fee_infos.fee_acct_id` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 手续费扣款账户号 | `String` | `9` | `N` | 已确认 | — |
| `async.resp_data.sub_orders_response[].fee_infos.fee_flag` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 手续费扣款标志 | `Integer` | `1` | `N` | 已确认 | 1: 外扣，2: 内扣；示例值：2 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_rec_type` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 手续费扣取方式 | `Integer` | `1` | `N` | 已确认 | 1: 实收，2: 后收；示例值：1 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_amount` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 手续费金额 | `String` | `16` | `N` | 已确认 | 单位元，保留小数点后两位。根据手续费公式计算的手续费小于0.01时，至少收取0.01元。示例值：1.00 |
| `async.resp_data.sub_orders_response[].split_fee_info` | `async.resp_data` | `$.sub_orders_response[].split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 分账手续费信息 |
| `async.resp_data.sub_orders_response[].split_fee_info.total_split_fee_amt` | `async.resp_data` | `$.sub_orders_response[].split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费总金额(元) | `String` | `14` | `N` | 已确认 | 示例值：0.10 |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_flag` | `async.resp_data` | `$.sub_orders_response[].split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费扣款标志 | `Integer` | `1` | `Y` | 已确认 | 1: 外扣 2: 内扣；示例值：2 |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_details` | `async.resp_data` | `$.sub_orders_response[].split_fee_info.split_fee_details => [需要官方确认]：String 子表编码` | 分账手续费信息 | `String` | `—` | `Y` | [需要官方确认]：长度 | 分账手续费信息 |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_details.split_fee_amt` | `async.resp_data` | `$.sub_orders_response[].split_fee_info.split_fee_details => [需要官方确认]：String 子表编码` | 分账手续费金额(元) | `String` | `16` | `Y` | 已确认 | 示例值：0.10 |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_details.split_fee_huifu_id` | `async.resp_data` | `$.sub_orders_response[].split_fee_info.split_fee_details => [需要官方确认]：String 子表编码` | 分账手续费承担方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_details.split_fee_acct_id` | `async.resp_data` | `$.sub_orders_response[].split_fee_info.split_fee_details => [需要官方确认]：String 子表编码` | 分账手续费承担方账号 | `String` | `9` | `N` | 已确认 | 示例值：F00598600 |
| `async.resp_data.sub_orders_response[].fund_freeze_stat` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].fund_freeze_stat` | 资金冻结状态 | `String` | `16` | `N` | 已确认 | FREEZE：冻结；UNFREEZE：解冻；示例值：UNFREEZE |

## 支付宝小程序预下单

- 原始地址：<https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_zfbpreorder.md>
- SHA-256：`3082194cef49961ec70fde375efd96f8a36f9427d64f9a8cfef325c48a429ef5`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 开户自动生成；示例值：[官网示例已脱敏] |
| `request.data.acct_id` | `request.data.acct_id` | `—（直接 JSON 路径）` | 收款汇付账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，示例值：A14186488；仅支持微信、支付宝、网银交易指定收款账户 |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 请求格式：yyyyMMdd；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `request.data.pre_order_type` | `request.data.pre_order_type` | `—（直接 JSON 路径）` | 预下单类型 | `String` | `1` | `Y` | 已确认 | 支付宝预下单：2；示例值：2 |
| `request.data.trans_amt` | `request.data.trans_amt` | `—（直接 JSON 路径）` | 交易金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `request.data.goods_desc` | `request.data.goods_desc` | `—（直接 JSON 路径）` | 商品描述 | `String` | `40` | `Y` | 已确认 | 示例值：个人电脑 |
| `request.data.delay_acct_flag` | `request.data.delay_acct_flag` | `—（直接 JSON 路径）` | 是否延迟交易 | `String` | `1` | `N` | 已确认 | Y 为延迟 N为不延迟，不传默认N；示例值：N |
| `request.data.merge_pay_flag` | `request.data.merge_pay_flag` | `—（直接 JSON 路径）` | 是否合单支付 | `String` | `1` | `N` | 已确认 | Y-合单支付，N-非合单支付，默认N，示例值：N；合单支付，不支持切换支付方式（即multi_pay_way_flag不能为Y） |
| `request.data.sub_orders_request[]` | `request.data.sub_orders_request` | `—（String(JSON Array) 容器）` | 子单信息列表 | `String` | `—` | `N` | [需要官方确认]：长度 | 合单支付时，该字段必填；jsonArray字符串，最多支持20条，最少2条 |
| `request.data.sub_orders_request[].sub_req_seq_id` | `request.data.sub_orders_request` | `$[].sub_req_seq_id` | 子单请求流水号 | `String` | `128` | `Y` | 已确认 | 同一合单huifu_id下，当天唯一 |
| `request.data.sub_orders_request[].sub_huifu_id` | `request.data.sub_orders_request` | `$[].sub_huifu_id` | 子单商户号 | `String` | `32` | `Y` | 已确认 | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] |
| `request.data.sub_orders_request[].sub_acct_id` | `request.data.sub_orders_request` | `$[].sub_acct_id` | 子单账户号 | `String` | `9` | `N` | 已确认 | 可指定收款账户号， 仅支持基本户、现金户，不填默认为基本户 |
| `request.data.sub_orders_request[].sub_trans_amt` | `request.data.sub_orders_request` | `$[].sub_trans_amt` | 子单交易金额 | `String` | `18` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1000.00，最低传入0.01；全部子单交易金额之和等于合单交易金额。 |
| `request.data.sub_orders_request[].delay_acct_flag` | `request.data.sub_orders_request` | `$[].delay_acct_flag` | 是否延迟交易 | `String` | `1` | `N` | 已确认 | Y 为延迟 N为不延迟，不传默认N；示例值：Y |
| `request.data.sub_orders_request[].sub_remark` | `request.data.sub_orders_request` | `$[].sub_remark` | 子单备注 | `String` | `255` | `N` | 已确认 | 交易后原样返回；示例值：子单备注 |
| `request.data.acct_split_bunch` | `request.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `2000` | `N` | 已确认 | 分账对象，jsonObject字符串 |
| `request.data.acct_split_bunch.acct_infos[]` | `request.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `—` | `N` | N/A：结构字段长度 | 分账明细 |
| `request.data.acct_split_bunch.acct_infos[].div_amt` | `request.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `request.data.acct_split_bunch.acct_infos[].huifu_id` | `request.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `N` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `request.data.acct_split_bunch.acct_infos[].acct_id` | `request.data.acct_split_bunch` | `$.acct_infos[].acct_id` | 收款汇付账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，示例值：A14186488；仅支持微信、支付宝、网银交易指定收款账户 |
| `request.data.acct_split_bunch.acct_infos[].percentage_div` | `request.data.acct_split_bunch` | `$.acct_infos[].percentage_div` | 分账百分比% | `String` | `6` | `N` | 已确认 | 示例值：23.50，表示23.50%。仅在percentage_flag=Y时起作用；acct_infos中全部分账百分比只和必须为100.00%。 |
| `request.data.acct_split_bunch.percentage_flag` | `request.data.acct_split_bunch` | `$.percentage_flag` | 百分比分账标志 | `String` | `1` | `N` | 已确认 | Y:使用百分比分账；示例值：Y |
| `request.data.acct_split_bunch.is_clean_split` | `request.data.acct_split_bunch` | `$.is_clean_split` | 是否净值分账 | `String` | `1` | `N` | 已确认 | Y:使用净值分账，仅在交易手续费内扣且使用百分比分账时起作用；示例值：Y |
| `request.data.hosting_data` | `request.data.hosting_data` | `—（String(JSON) 容器）` | 统一收银台扩展参数集合 | `String` | `2000` | `N` | 已确认 | jsonObject统一收银台扩展参数集合 |
| `request.data.hosting_data.project_id` | `request.data.hosting_data` | `$.project_id` | 项目号 | `String` | `32` | `N` | 已确认 | 商户创建的项目号；示例值：PROJECTID[官网示例已脱敏] |
| `request.data.app_data` | `request.data.app_data` | `—（[需要官方确认]：String 子表编码）` | app扩展参数集合 | `String` | `2000` | `Y` | 已确认 | app扩展参数 |
| `request.data.app_data.appid` | `request.data.app_data` | `—（[需要官方确认]：String 子表编码）` | 支付宝小程序ID | `String` | `32` | `N` | 已确认 | 支付宝小程序appid，托管支付宝小程序时上送；示例值：2088xxxxxxxx |
| `request.data.app_data.app_schema` | `request.data.app_data` | `—（[需要官方确认]：String 子表编码）` | 小程序返回码 | `String` | `100` | `Y` | 已确认 | 小程序完成支付后需要返回所填写的AppScheme，返回App必填信息。；示例值：https://callback.service.com/xx注：参数过长容易导致浏览器截取跳转地址，无法唤起收银台，限100字符。 ；**如果地址中有“+/?%#&=”字符需要进行编码操作** |
| `request.data.app_data.private_info` | `request.data.app_data` | `—（[需要官方确认]：String 子表编码）` | 私有信息 | `String` | `255` | `N` | 已确认 | 对应异步通知和主动查询接口中的remark字段；示例值：收取服务费 |
| `request.data.time_expire` | `request.data.time_expire` | `—（直接 JSON 路径）` | 交易失效时间 | `String` | `14` | `N` | 已确认 | 请求格式：yyyyMMddHHmmss；示例值：20220912111230；注意:为空默认失效时间为10分钟；用户在交易失效时间后完成交易有可能被关单。最终结果以异步为准；建议商户在交易量大时，或在搞营销活动时将失效时间设置短一些。 |
| `request.data.biz_info` | `request.data.biz_info` | `—（String(JSON) 容器）` | 业务信息 | `String` | `2000` | `N` | 已确认 | jsonObject格式；交易相关的信息 |
| `request.data.biz_info.payer_check_ali` | `request.data.biz_info` | `$.payer_check_ali` | 付款人验证（支付宝） | `Object` | `—` | `N` | N/A：结构字段长度 | 支付宝特殊交易需验证买家信息；如彩票行业等；当前只支持AT类交易有验证功能 |
| `request.data.biz_info.payer_check_ali.need_check_info` | `request.data.biz_info` | `$.payer_check_ali.need_check_info` | 是否提供校验身份信息 | `String` | `1` | `N` | 已确认 | T：强制校验，需要填写person_payer字段；F：不强制；示例值：T |
| `request.data.biz_info.payer_check_ali.min_age` | `request.data.biz_info` | `$.payer_check_ali.min_age` | 允许的最小买家年龄 | `String` | `3` | `N` | 已确认 | 买家年龄必须大于等于所传数值。示例值：18；注：1. need_check_info=T 时该参数才有效，；2. min_age 为整数，必须大于等于 0 |
| `request.data.biz_info.payer_check_ali.fix_buyer` | `request.data.biz_info` | `$.payer_check_ali.fix_buyer` | 是否强制校验付款人身份信息 | `String` | `8` | `N` | 已确认 | 用户进行实名认证校验；T：强制校验，F：不强制；示例值：T |
| `request.data.biz_info.person_payer` | `request.data.biz_info` | `$.person_payer` | 个人付款人信息 | `Object` | `—` | `N` | N/A：结构字段长度 | 付款人验证打开后需要填写付款人信息，但非必填；微信/支付宝共用字段 |
| `request.data.biz_info.person_payer.name` | `request.data.biz_info` | `$.person_payer.name` | 姓名 | `String` | `16` | `N` | 已确认 | 注：支付宝交易need_check_info=T时，该参数才有效；示例值：张三 |
| `request.data.biz_info.person_payer.cert_type` | `request.data.biz_info` | `$.person_payer.cert_type` | 证件类型 | `String` | `32` | `N` | 已确认 | 身份证：IDENTITY_CARD，；护照：PASSPORT；军官证：OFFICER_CARD，；士兵证：SOLDIER_CARD；户口本：HOKOU；示例值：IDENTITY_CARD ；注：支付宝交易need_check_info=T时，该参数才有效 |
| `request.data.biz_info.person_payer.cert_no` | `request.data.biz_info` | `$.person_payer.cert_no` | 证件号 | `String` | `64` | `N` | 已确认 | 注：支付宝交易need_check_info=T时，该参数才有效；需要密文传输，请参考[加密解密说明](https://paas.huifu.com/open/doc/guide/#/api_jiami_jiemi)使用汇付RSA公钥加密。；示例值：Mc5pjf+b/Keyi/t/wnH……MfYQnK7Lzw== |
| `request.data.biz_info.person_payer.mobile` | `request.data.biz_info` | `$.person_payer.mobile` | 手机号 | `String` | `20` | `N` | 已确认 | 注：该参数暂不校验；示例值：[官网示例已脱敏] |
| `request.data.notify_url` | `request.data.notify_url` | `—（直接 JSON 路径）` | 异步通知地址 | `String` | `512` | `N` | 已确认 | 交易异步通知地址，http或https开头，示例值：https://callback.service.com/xx；在交易成功/失败时触发回调，正常情况下只会触发一次，具体回调策略参见[链接](https://paas.huifu.com/open/doc/api_standard/#/ybxx/jiekouguifan_ybxx) |
| `request.data.alipay_data` | `request.data.alipay_data` | `—（String(JSON) 容器）` | 支付宝参数集合 | `String` | `2048` | `N` | 已确认 | jsonObject字符串 |
| `request.data.alipay_data.alipay_store_id` | `request.data.alipay_data` | `$.alipay_store_id` | 支付宝的店铺编号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.alipay_data.extend_params` | `request.data.alipay_data` | `$.extend_params` | 业务扩展参数 | `Object` | `2048` | `N` | 已确认 | 业务扩展参数 |
| `request.data.alipay_data.extend_params.card_type` | `request.data.alipay_data` | `$.extend_params.card_type` | 卡类型 | `String` | `32` | `N` | 已确认 | 示例值：S0JP0000 |
| `request.data.alipay_data.extend_params.food_order_type` | `request.data.alipay_data` | `$.extend_params.food_order_type` | 支付宝点餐场景类型 | `String` | `20` | `N` | 已确认 | QR_ORDER（店内扫码点餐）；PRE_ORDER（预点到店自提）；HOME_DELIVERY（外送到家）；DIRECT_PAYMENT（直接付款）；QR_FOOD_ORDER（点餐先付）；P_QR_FOOD_ORDER（点餐后付）；SELF_PICK（门店自提）；TAKE_OUT （餐饮外卖）；OTHER（其他）；该参数只适用于支付宝支付窗交易接口；示例值：TAKE_OUT |
| `request.data.alipay_data.extend_params.hb_fq_num` | `request.data.alipay_data` | `$.extend_params.hb_fq_num` | 花呗分期数 | `String` | `5` | `N` | 已确认 | 使用花呗分期要进行的分期数；示例值：3 |
| `request.data.alipay_data.extend_params.hb_fq_seller_percent` | `request.data.alipay_data` | `$.extend_params.hb_fq_seller_percent` | 花呗卖家手续费百分比 | `String` | `3` | `N` | 已确认 | 使用花呗分期需要卖家承担的手续费比，单位比例的百分值。； 花呗商贴支付默认传0，示例值：0 |
| `request.data.alipay_data.extend_params.industry_reflux_info` | `request.data.alipay_data` | `$.extend_params.industry_reflux_info` | 行业数据回流信息 | `String` | `64` | `N` | 已确认 | 示例值：{\"scene_code\":\"metro_tradeorder\",\"channel\":\"xxxx\",\"scene_data\":{\"asset_name\":\"ALIPAY\"}} |
| `request.data.alipay_data.extend_params.fq_channels` | `request.data.alipay_data` | `$.extend_params.fq_channels` | 信用卡分期资产方式 | `String` | `20` | `N` | 已确认 | 代表优先使用资产类型；alipayfq_cc：表示信⽤卡分期，为空时默认花呗。示例值：alipayfq_cc |
| `request.data.alipay_data.extend_params.parking_id` | `request.data.alipay_data` | `$.extend_params.parking_id` | 停车场id | `String` | `28` | `N` | 已确认 | isv停车场id、向支付宝停车平台申请获得的支付宝停车场的唯一标识；示例值：PI[官网示例已脱敏] |
| `request.data.alipay_data.extend_params.sys_service_provider_id` | `request.data.alipay_data` | `$.extend_params.sys_service_provider_id` | 系统商编号 | `String` | `64` | `N` | 已确认 | 该参数作为系统商返佣数据提取的依据，请填写系统商签约协议的pid；示例值：[官网示例已脱敏] |
| `request.data.alipay_data.goods_detail[]` | `request.data.alipay_data` | `$.goods_detail[]` | 订单包含的商品列表信息 | `Array` | `2048` | `N` | 已确认 | 订单包含的商品列表信息 |
| `request.data.alipay_data.goods_detail[].goods_id` | `request.data.alipay_data` | `$.goods_detail[].goods_id` | 商品的编号 | `String` | `32` | `Y` | 已确认 | 示例值：apple-01 |
| `request.data.alipay_data.goods_detail[].goods_name` | `request.data.alipay_data` | `$.goods_detail[].goods_name` | 商品名称 | `String` | `256` | `Y` | 已确认 | 示例值：ipad |
| `request.data.alipay_data.goods_detail[].price` | `request.data.alipay_data` | `$.goods_detail[].price` | 商品单价(元) | `String` | `16` | `Y` | 已确认 | 单位：元；示例值：43.40 |
| `request.data.alipay_data.goods_detail[].quantity` | `request.data.alipay_data` | `$.goods_detail[].quantity` | 商品数量 | `String` | `10` | `Y` | 已确认 | 示例值：40 |
| `request.data.alipay_data.goods_detail[].body` | `request.data.alipay_data` | `$.goods_detail[].body` | 商品描述信息 | `String` | `1000` | `N` | 已确认 | 示例值：个人电脑 |
| `request.data.alipay_data.goods_detail[].categories_tree` | `request.data.alipay_data` | `$.goods_detail[].categories_tree` | 商品类目树 | `String` | `128` | `N` | 已确认 | 商品类目树，从商品类目根节点到叶子节点的类目 id 组成，类目 id 值使用\ |
| `request.data.alipay_data.goods_detail[].goods_category` | `request.data.alipay_data` | `$.goods_detail[].goods_category` | 商品类目 | `String` | `24` | `N` | 已确认 | 示例值：34543238 |
| `request.data.alipay_data.goods_detail[].show_url` | `request.data.alipay_data` | `$.goods_detail[].show_url` | 商品的展示地址 | `String` | `400` | `N` | 已确认 | 示例值：https://paas.huifu.com/checkout/demo/pc/goodsDetail.html |
| `request.data.alipay_data.merchant_order_no` | `request.data.alipay_data` | `$.merchant_order_no` | 商户原始订单号 | `String` | `32` | `N` | 已确认 | 示例值：39045032345 |
| `request.data.alipay_data.operator_id` | `request.data.alipay_data` | `$.operator_id` | 商户操作员编号 | `String` | `28` | `N` | 已确认 | 示例值：carl.li@huifu.com |
| `request.data.alipay_data.product_code` | `request.data.alipay_data` | `$.product_code` | 产品码 | `String` | `32` | `N` | 已确认 | 商家和支付宝签约的产品码。小程序场景支付：JSAPI_PAY；当面付场景：FACE_TO_FACE_PAYMENT；示例值：JSAPI_PAY |
| `request.data.alipay_data.seller_id` | `request.data.alipay_data` | `$.seller_id` | 卖家支付宝用户号 | `String` | `28` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.alipay_data.store_id` | `request.data.alipay_data` | `$.store_id` | 商户门店编号 | `String` | `32` | `N` | 已确认 | 示例值：sh1001 |
| `request.data.alipay_data.subject` | `request.data.alipay_data` | `$.subject` | 订单标题 | `String` | `256` | `N` | 已确认 | 直连模式必填；商品的标题/交易标题/订单标题/订单关键字等，是请求时对应的参数，原样通知回来；示例值：红果奶茶 |
| `request.data.alipay_data.store_name` | `request.data.alipay_data` | `$.store_name` | 商家门店名称 | `String` | `512` | `N` | 已确认 | 直连模式字段；示例值：红果奶茶上海宝山店 |
| `request.data.alipay_data.ali_business_params` | `request.data.alipay_data` | `$.ali_business_params（String(JSON) 容器）` | 商户业务信息 | `String` | `512` | `N` | 已确认 | 商户传入业务信息，具体值要和支付宝约定将商户传入信息分发给相应系统，应用于安全，营销等参数直传场景，格式为JSONObject |
| `request.data.alipay_data.fq_mer_discount_flag` | `request.data.alipay_data` | `$.fq_mer_discount_flag` | 商户贴息标记 | `String` | `1` | `N` | 已确认 | 花呗分期商户补贴活动，Y：商户全额贴息，P：商户部分贴息，不传为非商户贴息（默认）；示例值：P；选择P：商户部分贴息活动，需同时在【ali_business_params：商户业务信息】中传入支付宝约定的活动参数，参数说明详见分期支付指引文档。 |
| `request.data.terminal_device_data` | `request.data.terminal_device_data` | `—（String(JSON) 容器）` | 设备信息 | `String` | `2048` | `N` | 已确认 | jsonObject字符串 |
| `request.data.terminal_device_data.devs_id` | `request.data.terminal_device_data` | `$.devs_id` | 汇付机具号 | `String` | `32` | `Y` | 已确认 | 通过汇付报备的机具必传；示例值：[官网示例已脱敏] |
| `request.data.fee_sign` | `request.data.fee_sign` | `—（直接 JSON 路径）` | 手续费场景标识 | `String` | `32` | `N` | 已确认 | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。；示例值：6850aad1e92f4244a74a42fcc1ad6360 |
| `request.data.fee_split_flag` | `request.data.fee_split_flag` | `—（直接 JSON 路径）` | 是否交易手续费分摊 | `String` | `1` | `N` | 已确认 | Y-分摊，N-不分摊，不传默认为N。示例值：N |
| `request.data.fee_flag` | `request.data.fee_flag` | `—（直接 JSON 路径）` | 手续费扣款标志 | `String` | `1` | `N` | 已确认 | 1: 外扣 2: 内扣 (默认取控台配置值)；示例值：1 |
| `request.data.channel_no` | `request.data.channel_no` | `—（直接 JSON 路径）` | 渠道号 | `String` | `32` | `N` | 已确认 | 如果交易走自有渠道请联系联调群运维人员获取；示例值:10000001 |
| `request.data.pay_scene` | `request.data.pay_scene` | `—（直接 JSON 路径）` | 场景类型 | `String` | `2` | `N` | 已确认 | 取值参见[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E5%BE%AE%E4%BF%A1%E4%B8%9A%E5%8A%A1%E5%BC%80%E9%80%9A%E7%B1%BB%E5%9E%8B)说明；示例值:02；pay_scene需和channel_no配合使用。在指定channel_no的情况下需要传入pay_scene取值；为空取默认配置 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `128` | `Y` | 已确认 | 业务返回描述；示例值：处理成功 |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：20221023 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：[官网示例已脱敏] |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：[官网示例已脱敏] |
| `response.data.trans_amt` | `response.data.trans_amt` | `—（直接 JSON 路径）` | 交易金额 | `String` | `12` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：100.00 |
| `response.data.jump_url` | `response.data.jump_url` | `—（直接 JSON 路径）` | 支付跳转链接 | `String` | `256` | `Y` | 已确认 | 用于app跳转支付宝时使用；示例值：https://callback.service.com/xx |

### 支付异步 resp_data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.resp_data.resp_code` | `async.resp_data` | `$.resp_code` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：00000000 |
| `async.resp_data.resp_desc` | `async.resp_data` | `$.resp_desc` | 业务返回信息 | `String` | `512` | `Y` | 已确认 | 业务返回描述；示例值：处理成功 |
| `async.resp_data.huifu_id` | `async.resp_data` | `$.huifu_id` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.req_date` | `async.resp_data` | `$.req_date` | 请求时间 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回，格式为yyyyMMdd，示例值：20091225 |
| `async.resp_data.req_seq_id` | `async.resp_data` | `$.req_seq_id` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 交易时传入，原样返回；示例值：[官网示例已脱敏] |
| `async.resp_data.hf_seq_id` | `async.resp_data` | `$.hf_seq_id` | 全局流水号 | `String` | `40` | `N` | 已确认 | 示例值：00470topo1A211015160805P090ac132fef00000 |
| `async.resp_data.out_trans_id` | `async.resp_data` | `$.out_trans_id` | 用户账单上的交易订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.resp_data.party_order_id` | `async.resp_data` | `$.party_order_id` | 用户账单上的商户订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.resp_data.trans_type` | `async.resp_data` | `$.trans_type` | 交易类型 | `String` | `20` | `N` | 已确认 | T_JSAPI: 微信公众号支付；T_MINIAPP: 微信小程序支付 ；A_JSAPI: 支付宝JS ；A_NATIVE: 支付宝正扫 ；U_NATIVE: 银联正扫 ；U_JSAPI: 银联 JS ；T_MICROPAY: 微信反扫 ；A_MICROPAY: 支付宝反扫 ；U_MICROPAY: 银联反扫 ；D_NATIVE: 数字人民币正扫 ；D_MICROPAY: 数字人民币反扫；示例值：D_NATIVE |
| `async.resp_data.trans_amt` | `async.resp_data` | `$.trans_amt` | 交易金额 | `String` | `12` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.resp_data.settlement_amt` | `async.resp_data` | `$.settlement_amt` | 结算金额 | `String` | `16` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.resp_data.fee_amount` | `async.resp_data` | `$.fee_amount` | 手续费金额 | `String` | `16` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.resp_data.trans_stat` | `async.resp_data` | `$.trans_stat` | 交易状态 | `String` | `1` | `N` | 已确认 | S：成功、F：失败，示例值：S |
| `async.resp_data.trans_finish_time` | `async.resp_data` | `$.trans_finish_time` | 汇付侧交易完成时间 | `String` | `13` | `N` | 已确认 | 毫秒时间戳，示例值：1791598928000 |
| `async.resp_data.end_time` | `async.resp_data` | `$.end_time` | 支付完成时间 | `String` | `14` | `N` | 已确认 | 格式yyyyMMddHHmmss，示例值：20091225091010 |
| `async.resp_data.acct_date` | `async.resp_data` | `$.acct_date` | 入账时间 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20091225 |
| `async.resp_data.debit_flag` | `async.resp_data` | `$.debit_flag` | 借贷记标识 | `String` | `1` | `N` | 已确认 | D-借记卡 C-信用卡 Z-借贷合一卡，示例值：D |
| `async.resp_data.alipay_response` | `async.resp_data` | `$.alipay_response（String(JSON) 容器）` | 支付宝返回的响应报文 | `String` | `6000` | `N` | 已确认 | Json格式 |
| `async.resp_data.alipay_response.voucher_detail_list[]` | `async.resp_data` | `$.alipay_response => JSON decode => $.voucher_detail_list[]` | 本交易支付时使用的所有优惠券信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 本交易支付时使用的所有优惠券信息 |
| `async.resp_data.alipay_response.voucher_detail_list[].id` | `async.resp_data` | `$.alipay_response => JSON decode => $.voucher_detail_list[].id` | 券id | `String` | `32` | `Y` | 已确认 | 示例值：6934572310301 |
| `async.resp_data.alipay_response.voucher_detail_list[].name` | `async.resp_data` | `$.alipay_response => JSON decode => $.voucher_detail_list[].name` | 券名称 | `String` | `32` | `Y` | 已确认 | 示例值：实体店付款通用立减券 |
| `async.resp_data.alipay_response.voucher_detail_list[].type` | `async.resp_data` | `$.alipay_response => JSON decode => $.voucher_detail_list[].type` | 券类型 | `String` | `32` | `Y` | 已确认 | 当前有三种类型： ；ALIPAY_FIX_VOUCHER: 全场代金券；ALIPAY_DISCOUNT_VOUCHER: 折扣券；ALIPAY_ITEM_VOUCHER: 单品优惠；示例值：ALIPAY_ITEM_VOUCHER ；注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码 |
| `async.resp_data.alipay_response.voucher_detail_list[].amount` | `async.resp_data` | `$.alipay_response => JSON decode => $.voucher_detail_list[].amount` | 优惠券面额 | `String` | `8` | `Y` | 已确认 | 优惠券面额，它应该会等于商家出资加上其他出资方出资；示例值：10.00 |
| `async.resp_data.alipay_response.voucher_detail_list[].merchant_contribute` | `async.resp_data` | `$.alipay_response => JSON decode => $.voucher_detail_list[].merchant_contribute` | 商家出资（特指发起交易的商家出资金额） | `String` | `8` | `N` | 已确认 | 商家出资（特指发起交易的商家出资金额）；示例值：10.00 |
| `async.resp_data.alipay_response.voucher_detail_list[].other_contribute` | `async.resp_data` | `$.alipay_response => JSON decode => $.voucher_detail_list[].other_contribute` | 其他出资方出资金额 | `String` | `11` | `N` | 已确认 | 可能是支付宝、品牌商、第三方，也可能是他们的一起出资；示例值：0.00 |
| `async.resp_data.alipay_response.fund_bill_list` | `async.resp_data` | `$.alipay_response.fund_bill_list => [需要官方确认]：String 子表编码` | 支付金额信息 | `String` | `512` | `N` | 已确认 | 支付成功的各个渠道金额信息，详见资金明细信息说明 |
| `async.resp_data.alipay_response.fund_bill_list.bank_code` | `async.resp_data` | `$.alipay_response.fund_bill_list => [需要官方确认]：String 子表编码` | 银行卡支付时的银行代码 | `String` | `10` | `N` | 已确认 | 银行卡支付时的银行代码；示例值：CEB；请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
| `async.resp_data.alipay_response.buyer_id` | `async.resp_data` | `$.alipay_response => JSON decode => $.buyer_id` | 买家的支付宝唯一用户号 | `String` | `28` | `N` | 已确认 | 2088开头的16位纯数字；示例值：[官网示例已脱敏] |
| `async.resp_data.alipay_response.buyer_logon_id` | `async.resp_data` | `$.alipay_response => JSON decode => $.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com |
| `async.resp_data.alipay_response.hb_fq_num` | `async.resp_data` | `$.alipay_response => JSON decode => $.hb_fq_num` | 花呗分期数 | `String` | `10` | `N` | 已确认 | 示例值：3 |
| `async.resp_data.alipay_response.hb_fq_seller_percent` | `async.resp_data` | `$.alipay_response => JSON decode => $.hb_fq_seller_percent` | 卖家承担的手续费 | `String` | `3` | `N` | 已确认 | 示例值：1.00 |
| `async.resp_data.is_div` | `async.resp_data` | `$.is_div` | 是否分账交易 | `String` | `1` | `Y` | 已确认 | 1: 分账交易, 0: 非分账交易；示例值：1 |
| `async.resp_data.acct_split_bunch` | `async.resp_data` | `$.acct_split_bunch（String(JSON) 容器）` | 分账对象 | `String` | `2048` | `N` | 已确认 | 分账对象，jsonObject字符串 |
| `async.resp_data.acct_split_bunch.acct_infos[]` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[]` | 分账明细 | `Array` | `2048` | `Y` | 已确认 | 分账明细 |
| `async.resp_data.acct_split_bunch.acct_infos[].div_amt` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.resp_data.acct_split_bunch.acct_infos[].huifu_id` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `async.resp_data.acct_split_bunch.acct_infos[].acct_id` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[].acct_id` | 收款汇付账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，示例值：A14186488；仅支持微信、支付宝、网银交易指定收款账户 |
| `async.resp_data.acct_split_bunch.acct_infos[].acct_date` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[].acct_date` | 账务日期 | `String` | `8` | `N` | 已确认 | 示例值：20221023 |
| `async.resp_data.is_delay_acct` | `async.resp_data` | `$.is_delay_acct` | 是否延时交易 | `String` | `1` | `Y` | 已确认 | 1: 延迟 0: 不延迟，示例值：1 |
| `async.resp_data.fee_flag` | `async.resp_data` | `$.fee_flag` | 手续费扣款标志 | `Int` | `1` | `N` | 已确认 | 1: 外扣 2: 内扣；默认返回控台配置方式 ，示例值：2 |
| `async.resp_data.trans_fee_allowance_info` | `async.resp_data` | `$.trans_fee_allowance_info（String(JSON) 容器）` | 手续费补贴信息 | `String` | `6000` | `N` | 已确认 | Json格式 |
| `async.resp_data.trans_fee_allowance_info.receivable_fee_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.receivable_fee_amt` | 商户应收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `async.resp_data.trans_fee_allowance_info.actual_fee_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.actual_fee_amt` | 商户实收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `async.resp_data.trans_fee_allowance_info.allowance_fee_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.allowance_fee_amt` | 补贴手续费 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `async.resp_data.trans_fee_allowance_info.allowance_type` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.allowance_type` | 补贴类型 | `String` | `10` | `N` | 已确认 | 0：不补贴，为空默认；1：补贴；2：部分补贴；3：全额补贴(优惠后)；4：部分补贴(优惠后)；示例值：2 |
| `async.resp_data.trans_fee_allowance_info.no_allowance_desc` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.no_allowance_desc` | 不补贴原因 | `String` | `128` | `N` | 已确认 | 补贴系统返回的不补贴原因；1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴；2:额度用完；3:不在有效期；4:活动不存在；5:手续费金额为0不补贴；6:顶格优惠；7:额度不足；8:手续费后补；9:未达到起始补贴金额；示例值：2 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos` | 手续费补贴活动详情 | `Object` | `—` | `N` | N/A：结构字段长度 | 补贴系统返回，斗拱原样返回 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.acct_id` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.acct_id` | 门店 | `String` | `64` | `N` | 已确认 | 示例值：sh002 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.merchant_group` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.merchant_group` | 商户号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.allowance_sys` | 补贴方 | `String` | `64` | `Y` | 已确认 | 1:银行 2:服务商 3:汇来米；示例值：1 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys_id` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.allowance_sys_id` | 补贴方ID | `String` | `64` | `Y` | 已确认 | 对应补贴方的id；示例值：[官网示例已脱敏] |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.is_delay_allowance` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.is_delay_allowance` | 补贴类型 | `String` | `2` | `Y` | 已确认 | 1:实补 2:后补,默认实补；示例值：1 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_id` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.market_id` | 自定义活动编号 | `String` | `64` | `Y` | 已确认 | 示例值：ISFE00232 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_name` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.market_name` | 自定义活动名称 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_desc` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.market_desc` | 自定义活动描述 | `String` | `64` | `N` | 已确认 | 示例值：新店开业大促 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.start_time` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.start_time` | 活动开始时间 | `String` | `8` | `Y` | 已确认 | yyyyMMdd；示例值：20220909 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.end_time` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.end_time` | 活动结束时间 | `String` | `8` | `Y` | 已确认 | yyyyMMdd；示例值：20220911 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_debit_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.pos_debit_limit_amt` | pos借记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：2.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_credit_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.pos_credit_limit_amt` | pos贷记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.pos_limit_amt` | pos补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.qr_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.qr_limit_amt` | 扫码补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.total_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.total_limit_amt` | 活动总补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.status` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.status` | 活动是否有效 | `String` | `4` | `Y` | 已确认 | 1:生效 0：失效；示例值：1 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.human_flag` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.human_flag` | 是否人工操作 | `String` | `4` | `Y` | 已确认 | N：自动 Y：人工 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.activity_id` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.activity_id` | 活动号 | `String` | `64` | `Y` | 已确认 | 示例值：223402342 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.activity_name` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.activity_name` | 活动描述 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.create_by` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.create_by` | 创建人 | `String` | `32` | `Y` | 已确认 | 示例值：Lg[官网示例已脱敏] |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.create_time` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.create_time` | 创建时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 22:00:30 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.update_time` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos.update_time` | 更新时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 23:00:30 |
| `async.resp_data.fee_formula_infos[]` | `async.resp_data` | `$.fee_formula_infos（String(JSON Array) 容器）` | 手续费费率信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray格式；微信、支付宝、云闪付交易成功时返回手续费费率信息 |
| `async.resp_data.fee_formula_infos[].fee_formula` | `async.resp_data` | `$.fee_formula_infos => JSON decode => $[].fee_formula` | 手续费计算公式 | `String` | `512` | `Y` | 已确认 | 示例值：AMT*0.003 |
| `async.resp_data.fee_formula_infos[].fee_type` | `async.resp_data` | `$.fee_formula_infos => JSON decode => $[].fee_type` | 手续费类型 | `String` | `32` | `Y` | 已确认 | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；示例值：ACCT_FEE |
| `async.resp_data.fee_formula_infos[].huifu_id` | `async.resp_data` | `$.fee_formula_infos => JSON decode => $[].huifu_id` | 商户号 | `String` | `32` | `N` | 已确认 | 补贴支付账户补贴时，补贴账户的huifuId；示例值：[官网示例已脱敏] |
| `async.resp_data.fee_formula_infos[].fee_sign` | `async.resp_data` | `$.fee_formula_infos => JSON decode => $[].fee_sign` | 手续费场景标识 | `String` | `32` | `N` | 已确认 | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。；示例值：6850aad1e92f4244a74a42fcc1ad6360 |
| `async.resp_data.remark` | `async.resp_data` | `$.remark` | 备注 | `String` | `45` | `N` | 已确认 | 原样返回，示例值：备注 |
| `async.resp_data.bank_code` | `async.resp_data` | `$.bank_code` | 通道返回码 | `String` | `32` | `N` | 已确认 | 示例值：00 |
| `async.resp_data.bank_message` | `async.resp_data` | `$.bank_message` | 通道返回描述 | `String` | `200` | `N` | 已确认 | 示例值：成功[0000000] |
| `async.resp_data.devs_id` | `async.resp_data` | `$.devs_id` | 汇付机具号 | `String` | `32` | `Y` | 已确认 | 通过汇付报备的机具必传；示例值：[官网示例已脱敏] |

## 微信小程序预下单

- 原始地址：<https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_wxpreorder.md>
- SHA-256：`d2d91fb6b25a2f6477b5ca1531d7bc4349b4760f63c4033d6e1b307c31ba48f6`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.pre_order_type` | `request.data.pre_order_type` | `—（直接 JSON 路径）` | 预下单类型 | `String` | `1` | `Y` | 已确认 | 微信预下单：3；示例值：3 |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 请求格式：yyyyMMdd；示例值：20221023 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 开户自动生成；示例值：[官网示例已脱敏] |
| `request.data.acct_id` | `request.data.acct_id` | `—（直接 JSON 路径）` | 收款汇付账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，示例值：A14186488；仅支持微信、支付宝、网银交易指定收款账户 |
| `request.data.trans_amt` | `request.data.trans_amt` | `—（直接 JSON 路径）` | 交易金额 | `String` | `14` | `Y` | 已确认 | 单位元，保留两位小数，示例值：1.00，最低传入0.01 |
| `request.data.goods_desc` | `request.data.goods_desc` | `—（直接 JSON 路径）` | 商品描述 | `String` | `40` | `Y` | 已确认 | 示例值：个人电脑 |
| `request.data.delay_acct_flag` | `request.data.delay_acct_flag` | `—（直接 JSON 路径）` | 是否延迟交易 | `String` | `1` | `N` | 已确认 | Y 为延迟 N为不延迟，不传默认N；示例值：N |
| `request.data.merge_pay_flag` | `request.data.merge_pay_flag` | `—（直接 JSON 路径）` | 是否合单支付 | `String` | `1` | `N` | 已确认 | Y-合单支付，N-非合单支付，默认N，示例值：N；合单支付，不支持切换支付方式（即multi_pay_way_flag不能为Y） |
| `request.data.sub_orders_request[]` | `request.data.sub_orders_request` | `—（String(JSON Array) 容器）` | 子单信息列表 | `String` | `—` | `N` | [需要官方确认]：长度 | 合单支付时，该字段必填；jsonArray字符串，最多支持20条，最少2条 |
| `request.data.sub_orders_request[].sub_req_seq_id` | `request.data.sub_orders_request` | `$[].sub_req_seq_id` | 子单请求流水号 | `String` | `128` | `Y` | 已确认 | 同一合单huifu_id下，当天唯一 |
| `request.data.sub_orders_request[].sub_huifu_id` | `request.data.sub_orders_request` | `$[].sub_huifu_id` | 子单商户号 | `String` | `32` | `Y` | 已确认 | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] |
| `request.data.sub_orders_request[].sub_acct_id` | `request.data.sub_orders_request` | `$[].sub_acct_id` | 子单账户号 | `String` | `9` | `N` | 已确认 | 可指定收款账户号， 仅支持基本户、现金户，不填默认为基本户 |
| `request.data.sub_orders_request[].sub_trans_amt` | `request.data.sub_orders_request` | `$[].sub_trans_amt` | 子单交易金额 | `String` | `18` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1000.00，最低传入0.01；全部子单交易金额之和等于合单交易金额。 |
| `request.data.sub_orders_request[].delay_acct_flag` | `request.data.sub_orders_request` | `$[].delay_acct_flag` | 是否延迟交易 | `String` | `1` | `N` | 已确认 | Y 为延迟 N为不延迟，不传默认N；示例值：Y |
| `request.data.sub_orders_request[].sub_remark` | `request.data.sub_orders_request` | `$[].sub_remark` | 子单备注 | `String` | `255` | `N` | 已确认 | 交易后原样返回；示例值：子单备注 |
| `request.data.split_pay_flag` | `request.data.split_pay_flag` | `—（直接 JSON 路径）` | 是否拆单支付 | `String` | `1` | `N` | 已确认 | 拆单支付标识，Y：拆单支付，N：非拆单支付，不填默认为N。商户需预开通拆单支付权限后方可使用；示例值：N |
| `request.data.split_pay_data` | `request.data.split_pay_data` | `—（[需要官方确认]：String 子表编码）` | 拆单支付参数集合 | `String` | `2000` | `N` | 已确认 | 拆单支付参数集合 |
| `request.data.split_pay_data.fq_mer_discount_flag` | `request.data.split_pay_data` | `—（[需要官方确认]：String 子表编码）` | 商户贴息标记 | `String` | `1` | `N` | 已确认 | 花呗分期商户补贴活动，拆单支付时生效，Y：商户全额贴息，P：商户部分贴息，不传为非商户贴息（默认）；示例值：P；选择P：商户部分贴息活动，需同时在【ali_business_params：商户业务信息】中传入支付宝约定的活动参数，参数说明详见分期支付指引文档。 |
| `request.data.split_pay_data.ali_business_params` | `request.data.split_pay_data` | `—（[需要官方确认]：String 子表编码）` | 商户业务信息 | `String` | `1` | `N` | 已确认 | 拆单支付时生效，商户传入业务信息，具体值要和支付宝约定将商户传入信息分发给相应系统，应用于安全，营销等参数直传场景，格式为JSONObject |
| `request.data.acct_split_bunch` | `request.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `2000` | `N` | 已确认 | 分账对象，jsonObject字符串，拆单支付时该字段不生效 |
| `request.data.acct_split_bunch.acct_infos[]` | `request.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `—` | `N` | N/A：结构字段长度 | 分账明细 |
| `request.data.acct_split_bunch.acct_infos[].div_amt` | `request.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `request.data.acct_split_bunch.acct_infos[].huifu_id` | `request.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `N` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `request.data.acct_split_bunch.acct_infos[].acct_id` | `request.data.acct_split_bunch` | `$.acct_infos[].acct_id` | 收款汇付账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，示例值：A14186488；仅支持微信、支付宝、网银交易指定收款账户 |
| `request.data.acct_split_bunch.acct_infos[].percentage_div` | `request.data.acct_split_bunch` | `$.acct_infos[].percentage_div` | 分账百分比% | `String` | `6` | `N` | 已确认 | 示例值：23.50，表示23.50%。仅在percentage_flag=Y时起作用；acct_infos中全部分账百分比只和必须为100.00%。 |
| `request.data.acct_split_bunch.percentage_flag` | `request.data.acct_split_bunch` | `$.percentage_flag` | 百分比分账标志 | `String` | `1` | `N` | 已确认 | Y:使用百分比分账；示例值：Y |
| `request.data.acct_split_bunch.is_clean_split` | `request.data.acct_split_bunch` | `$.is_clean_split` | 是否净值分账 | `String` | `1` | `N` | 已确认 | Y:使用净值分账，仅在交易手续费内扣且使用百分比分账时起作用；示例值：Y |
| `request.data.hosting_data` | `request.data.hosting_data` | `—（String(JSON) 容器）` | 统一收银台扩展参数集合 | `String` | `2000` | `N` | 已确认 | jsonObject统一收银台扩展参数集合 |
| `request.data.hosting_data.project_id` | `request.data.hosting_data` | `$.project_id` | 项目号 | `String` | `32` | `N` | 已确认 | 商户创建的项目号；示例值：PROJECTID[官网示例已脱敏] |
| `request.data.miniapp_data` | `request.data.miniapp_data` | `—（[需要官方确认]：String 子表编码）` | 微信小程序扩展参数集合 | `String` | `2000` | `Y` | 已确认 | 微信小程序扩展参数集合 |
| `request.data.miniapp_data.seq_id` | `request.data.miniapp_data` | `—（[需要官方确认]：String 子表编码）` | 应用ID | `String` | `64` | `N` | 已确认 | 示例值：APP_[官网示例已脱敏]；不传默认使用斗拱收银台唤起支付。；如使用自有渠道时通过控台小程序托管功能上传同主体小程序并发布代码获取应用ID填写此处。[参见图片说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/imgs/hosting/%E6%94%AF%E4%BB%98%E6%89%98%E7%AE%A1%E5%BA%94%E7%94%A8ID.png) ；如使用微信插件该参数不传值。 |
| `request.data.miniapp_data.private_info` | `request.data.miniapp_data` | `—（[需要官方确认]：String 子表编码）` | 私有信息 | `String` | `255` | `N` | 已确认 | 对应异步通知和主动查询接口中的remark字段；示例值：备注 |
| `request.data.miniapp_data.need_scheme` | `request.data.miniapp_data` | `—（[需要官方确认]：String 子表编码）` | 是否生成scheme_code | `String` | `1` | `Y` | 已确认 | Y；适用于APP、短信链接、邮件、外部网页、微信内等拉起汇付小程序的业务场景时需填Y；N；通过汇付微信插件支付填N |
| `request.data.time_expire` | `request.data.time_expire` | `—（直接 JSON 路径）` | 交易失效时间 | `String` | `14` | `N` | 已确认 | 请求格式：yyyyMMddHHmmss；示例值：20220912111230；注意:为空默认失效时间为10分钟；用户在交易失效时间后完成交易有可能被关单。最终结果以异步为准；建议商户在交易量大时，或在搞营销活动时将失效时间设置短一些。 |
| `request.data.biz_info` | `request.data.biz_info` | `—（String(JSON) 容器）` | 业务信息 | `String` | `2000` | `N` | 已确认 | jsonObject格式；交易相关的信息 |
| `request.data.biz_info.payer_check_wx` | `request.data.biz_info` | `$.payer_check_wx` | 付款人验证（微信） | `Object` | `—` | `N` | N/A：结构字段长度 | 微信实名支付需验证买家信息；如彩票行业等；当前只支持AT类交易有验证功能 |
| `request.data.biz_info.payer_check_wx.limit_payer` | `request.data.biz_info` | `$.payer_check_wx.limit_payer` | 指定支付者 | `String` | `5` | `N` | 已确认 | 上传此参数，可限制用户只有是成年人才能支付，；值：ADULT；示例值：ADULT |
| `request.data.biz_info.payer_check_wx.real_name_flag` | `request.data.biz_info` | `$.payer_check_wx.real_name_flag` | 微信实名验证 | `String` | `1` | `N` | 已确认 | Y/N；默认N；示例值：Y |
| `request.data.biz_info.person_payer` | `request.data.biz_info` | `$.person_payer` | 个人付款人信息 | `Object` | `—` | `N` | N/A：结构字段长度 | 付款人验证打开后需要填写付款人信息，但非必填 |
| `request.data.biz_info.person_payer.name` | `request.data.biz_info` | `$.person_payer.name` | 姓名 | `String` | `16` | `N` | 已确认 | 示例值：张三 |
| `request.data.biz_info.person_payer.cert_type` | `request.data.biz_info` | `$.person_payer.cert_type` | 证件类型 | `String` | `32` | `N` | 已确认 | 身份证：IDENTITY_CARD，（微信只支持身份证）；示例值：IDENTITY_CARD |
| `request.data.biz_info.person_payer.cert_no` | `request.data.biz_info` | `$.person_payer.cert_no` | 证件号 | `String` | `64` | `N` | 已确认 | 需要密文传输，请参考[加密解密说明](https://paas.huifu.com/open/doc/guide/#/api_jiami_jiemi)使用汇付RSA公钥加密。；示例值：Mc5pjf+b/Keyi/t/wnH……MfYQnK7Lzw== |
| `request.data.notify_url` | `request.data.notify_url` | `—（直接 JSON 路径）` | 交易异步通知地址 | `String` | `512` | `N` | 已确认 | http或https开头，示例值：https://callback.service.com/xx；在交易成功/失败时触发回调，正常情况下只会触发一次，具体回调策略参见[链接](https://paas.huifu.com/open/doc/api_standard/#/ybxx/jiekouguifan_ybxx) |
| `request.data.wx_data` | `request.data.wx_data` | `—（String(JSON) 容器）` | 微信参数集合 | `String` | `2048` | `N` | 已确认 | jsonObject字符串 |
| `request.data.wx_data.sub_appid` | `request.data.wx_data` | `$.sub_appid` | 子商户应用ID | `String` | `32` | `N` | 已确认 | 子商户在微信申请的应用ID，全局唯一。**走聚合正扫发货管理的商户，使用的微信公众号/小程序支付 需要填写sub_appid+sub_openid**；示例值：wxd678efh567hg6999 |
| `request.data.wx_data.sub_openid` | `request.data.wx_data` | `$.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 公众号和小程序场景必填。用户在子商户sub_appid下的唯一标识。下单前需获取到用户的sub_openid，sub_openid获取详见微信文档[openid获取](https://pay.weixin.qq.com/docs/partner/development/glossary/parameter.html)。；示例值：oUpF8uMuAJO_M2pxb1Q9zNjWeS6o |
| `request.data.wx_data.attach` | `request.data.wx_data` | `$.attach` | 附加数据 | `String` | `127` | `N` | 已确认 | 在查询api和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据；示例值：附加数据 |
| `request.data.wx_data.body` | `request.data.wx_data` | `$.body` | 商品描述 | `String` | `128` | `N` | 已确认 | 商品或支付单简要描述，格式要求：门店品牌名-城市分店名-实际商品名称；示例值：image形象店-深圳腾大- QQ 公仔 |
| `request.data.wx_data.detail` | `request.data.wx_data` | `$.detail` | 商品详情 | `Object` | `6000` | `N` | 已确认 | 单品优惠功能字段 |
| `request.data.wx_data.detail.cost_price` | `request.data.wx_data` | `$.detail.cost_price` | 订单原价(元) | `String` | `12` | `N` | 已确认 | 1.商户侧一张小票订单可能被分多次支付，订单原价用于记录整张小票的交易金额。 ；2.当订单原价与支付金额不相等，则不享受优惠。；3.该字段主要用于防止同一张小票分多次支付，以享受多次优惠的情况，正常支付订单不必上传此参数。；示例值：999.00 |
| `request.data.wx_data.detail.receipt_id` | `request.data.wx_data` | `$.detail.receipt_id` | 商品小票ID | `String` | `32` | `N` | 已确认 | 商家小票 ID；示例值：[官网示例已脱敏] |
| `request.data.wx_data.detail.goods_detail[]` | `request.data.wx_data` | `$.detail.goods_detail[]` | 单品列表 | `Array` | `2048` | `Y` | 已确认 | 单品信息，使用Json数组格式提交 |
| `request.data.wx_data.detail.goods_detail[].goods_id` | `request.data.wx_data` | `$.detail.goods_detail[].goods_id` | 商品编码 | `String` | `32` | `N` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `request.data.wx_data.detail.goods_detail[].goods_name` | `request.data.wx_data` | `$.detail.goods_detail[].goods_name` | 商品名称 | `String` | `256` | `N` | 已确认 | 商品的实际名称；示例值：太龙双黄连口服液 |
| `request.data.wx_data.detail.goods_detail[].price` | `request.data.wx_data` | `$.detail.goods_detail[].price` | 商品单价(元) | `String` | `12` | `N` | 已确认 | 如果商户有优惠，需传输商户优惠后的单价；例如：用户对一笔 100 元的订单使用了商场发的优惠券 100-50，则活动商品的单价应为原单价-50；示例值：43.00 |
| `request.data.wx_data.detail.goods_detail[].quantity` | `request.data.wx_data` | `$.detail.goods_detail[].quantity` | 商品数量 | `Int` | `11` | `N` | 已确认 | 用户购买的数量；示例值：1 |
| `request.data.wx_data.detail.goods_detail[].wxpay_goods_id` | `request.data.wx_data` | `$.detail.goods_detail[].wxpay_goods_id` | 微信侧商品编码 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.wx_data.device_info` | `request.data.wx_data` | `$.device_info` | 设备号 | `String` | `32` | `N` | 已确认 | 终端设备号(商户自定义，如门店编号)，示例值：[官网示例已脱敏]；注意：H5与小程序支付填以下值：；苹果APP：1；安卓APP：2；IOS手机网站：3；ANDROID手机网站：4 |
| `request.data.wx_data.goods_tag` | `request.data.wx_data` | `$.goods_tag` | 订单优惠标记 | `String` | `32` | `N` | 已确认 | 代金券或立减优惠功能的参数；示例值：WXG |
| `request.data.wx_data.identity` | `request.data.wx_data` | `$.identity` | 实名支付 | `String` | `128` | `N` | 已确认 | 实名支付功能，用于公安和保险类商户使用, 包含类型、证件号、姓名三个子域。；示例值："{\\"type\":\\"IDCARD\\",\\"number\\":\\"111111111111\\",\\"name\\":\\"张三\\"}" |
| `request.data.wx_data.receipt` | `request.data.wx_data` | `$.receipt` | 开发票入口开放标识 | `String` | `8` | `N` | 已确认 | 示例值：Y |
| `request.data.wx_data.scene_info` | `request.data.wx_data` | `$.scene_info` | 场景信息 | `Object` | `2048` | `N` | 已确认 | 该字段用于上报场景信息，目前支持上报实际门店信息。 |
| `request.data.wx_data.scene_info.store_info` | `request.data.wx_data` | `$.scene_info.store_info` | 门店信息 | `Object` | `2048` | `N` | 已确认 | 门店信息 |
| `request.data.wx_data.scene_info.store_info.id` | `request.data.wx_data` | `$.scene_info.store_info.id` | 门店id | `String` | `32` | `N` | 已确认 | 门店编号，由商户自定义；示例值：sh001 |
| `request.data.wx_data.scene_info.store_info.name` | `request.data.wx_data` | `$.scene_info.store_info.name` | 门店名称 | `String` | `64` | `N` | 已确认 | 门店名称，由商户自定义；示例值：上海宝山分店 |
| `request.data.wx_data.scene_info.store_info.area_code` | `request.data.wx_data` | `$.scene_info.store_info.area_code` | 门店行政区划码 | `String` | `6` | `N` | 已确认 | 门店所在地行政区划码，详见[行政区划代码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)，示例值：310101 |
| `request.data.wx_data.scene_info.store_info.address` | `request.data.wx_data` | `$.scene_info.store_info.address` | 门店详细地址 | `String` | `128` | `N` | 已确认 | 门店详细地址，由商户自定义；示例值：上海宝山区共富路100号 |
| `request.data.wx_data.spbill_create_ip` | `request.data.wx_data` | `$.spbill_create_ip` | 终端ip | `String` | `64` | `N` | 已确认 | 调用微信支付API的机器IP；示例值：172.28.52.52 |
| `request.data.wx_data.promotion_flag` | `request.data.wx_data` | `$.promotion_flag` | 单品优惠标识 | `String` | `1` | `N` | 已确认 | Y-是，N-否，默认否；直连模式需要填写；示例值：Y；若使用单品优惠，该字段必填，若该字段为Y，则商品详情【detail】必填 |
| `request.data.wx_data.product_id` | `request.data.wx_data` | `$.product_id` | 新增商品ID | `String` | `32` | `N` | 已确认 | 直连模式【trade_type】=T_NATIVE支付的时候必填；示例值： |
| `request.data.wx_data.limit_payer` | `request.data.wx_data` | `$.limit_payer` | 指定支付者 | `String` | `5` | `N` | 已确认 | 上传此参数，可限制用户只有是成年人才能支付，示例值：ADULT |
| `request.data.terminal_device_data` | `request.data.terminal_device_data` | `—（String(JSON) 容器）` | 设备信息 | `String` | `2048` | `N` | 已确认 | jsonObject字符串 |
| `request.data.terminal_device_data.devs_id` | `request.data.terminal_device_data` | `$.devs_id` | 汇付机具号 | `String` | `32` | `Y` | 已确认 | 通过汇付报备的机具必传；示例值：[官网示例已脱敏] |
| `request.data.fee_sign` | `request.data.fee_sign` | `—（直接 JSON 路径）` | 手续费场景标识 | `String` | `32` | `N` | 已确认 | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。；示例值：6850aad1e92f4244a74a42fcc1ad6360 |
| `request.data.fee_split_flag` | `request.data.fee_split_flag` | `—（直接 JSON 路径）` | 是否交易手续费分摊 | `String` | `1` | `N` | 已确认 | Y-分摊，N-不分摊，不传默认为N。示例值：N |
| `request.data.fee_flag` | `request.data.fee_flag` | `—（直接 JSON 路径）` | 手续费扣款标志 | `String` | `1` | `N` | 已确认 | 1: 外扣 2: 内扣 (默认取控台配置值)；示例值：1 |
| `request.data.channel_no` | `request.data.channel_no` | `—（直接 JSON 路径）` | 渠道号 | `String` | `32` | `N` | 已确认 | 如果交易走自有渠道请联系联调群运维人员获取；示例值:10000001 |
| `request.data.pay_scene` | `request.data.pay_scene` | `—（直接 JSON 路径）` | 场景类型 | `String` | `2` | `N` | 已确认 | 取值参见[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E5%BE%AE%E4%BF%A1%E4%B8%9A%E5%8A%A1%E5%BC%80%E9%80%9A%E7%B1%BB%E5%9E%8B)说明；示例值:02；pay_scene需和channel_no配合使用。在指定channel_no的情况下需要传入pay_scene取值；为空取默认配置 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_wxpreorder.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `128` | `Y` | 已确认 | 业务返回描述；示例值：处理成功 |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：20221023 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：[官网示例已脱敏] |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：[官网示例已脱敏] |
| `response.data.trans_amt` | `response.data.trans_amt` | `—（直接 JSON 路径）` | 交易金额 | `String` | `12` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：300.00 |
| `response.data.pre_order_id` | `response.data.pre_order_id` | `—（直接 JSON 路径）` | 预下单订单号 | `String` | `64` | `Y` | 已确认 | 示例值：H[官网示例已脱敏] |
| `response.data.miniapp_data` | `response.data.miniapp_data` | `—（String(JSON) 容器）` | 微信小程序返回集合 | `String` | `2000` | `Y` | 已确认 | json格式，用于app跳转微信支付 |
| `response.data.miniapp_data.gh_id` | `response.data.miniapp_data` | `$.gh_id` | 小程序原始ID | `String` | `64` | `N` | 已确认 | 示例值：gh_1ad0a7231d39 |
| `response.data.miniapp_data.path` | `response.data.miniapp_data` | `$.path` | 小程序页面支付路径 | `String` | `64` | `N` | 已确认 | 示例值：pages/cashier/cashier |
| `response.data.miniapp_data.scheme_code` | `response.data.miniapp_data` | `$.scheme_code` | 小程序跳转码 | `String` | `64` | `N` | 已确认 | 示例值：weixin://dl/business/?t=c1HAi9XnUnt；need_scheme=N时返回空 |

### 支付异步 resp_data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.resp_data.resp_code` | `async.resp_data` | `$.resp_code` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_wxpreorder.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：00000000 |
| `async.resp_data.resp_desc` | `async.resp_data` | `$.resp_desc` | 业务返回信息 | `String` | `512` | `Y` | 已确认 | 业务返回描述；示例值：处理成功 |
| `async.resp_data.req_date` | `async.resp_data` | `$.req_date` | 请求时间 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回，格式为yyyyMMdd，示例值：20091225 |
| `async.resp_data.req_seq_id` | `async.resp_data` | `$.req_seq_id` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 交易时传入，原样返回；示例值：[官网示例已脱敏] |
| `async.resp_data.hf_seq_id` | `async.resp_data` | `$.hf_seq_id` | 全局流水号 | `String` | `40` | `N` | 已确认 | 示例值：00470topo1A211015160805P090ac132fef00000 |
| `async.resp_data.out_trans_id` | `async.resp_data` | `$.out_trans_id` | 用户账单上的交易订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.resp_data.party_order_id` | `async.resp_data` | `$.party_order_id` | 用户账单上的商户订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.resp_data.huifu_id` | `async.resp_data` | `$.huifu_id` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.trans_type` | `async.resp_data` | `$.trans_type` | 交易类型 | `String` | `20` | `N` | 已确认 | T_JSAPI: 微信公众号支付；T_MINIAPP: 微信小程序支付 ；A_JSAPI: 支付宝JS ；A_NATIVE: 支付宝正扫 ；U_NATIVE: 银联正扫 ；U_JSAPI: 银联 JS ；T_MICROPAY: 微信反扫 ；A_MICROPAY: 支付宝反扫 ；U_MICROPAY: 银联反扫 ；D_NATIVE: 数字人民币正扫 ；D_MICROPAY: 数字人民币反扫；示例值：U_MICROPAY |
| `async.resp_data.trans_amt` | `async.resp_data` | `$.trans_amt` | 交易金额 | `String` | `12` | `N` | 已确认 | 单位元，保留两位小数，示例值：1.00，最低0.01 |
| `async.resp_data.settlement_amt` | `async.resp_data` | `$.settlement_amt` | 结算金额 | `String` | `16` | `N` | 已确认 | 单位元，保留两位小数，示例值：1.00，最低0.01 |
| `async.resp_data.fee_amount` | `async.resp_data` | `$.fee_amount` | 手续费金额 | `String` | `16` | `N` | 已确认 | 单位元，保留两位小数，示例值：1.00，最低0.01 |
| `async.resp_data.acct_date` | `async.resp_data` | `$.acct_date` | 入账时间 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20091225 |
| `async.resp_data.trans_stat` | `async.resp_data` | `$.trans_stat` | 交易状态 | `String` | `1` | `N` | 已确认 | S：成功、F：失败；示例值：S |
| `async.resp_data.end_time` | `async.resp_data` | `$.end_time` | 支付完成时间 | `String` | `14` | `N` | 已确认 | 格式yyyyMMddHHmmss，示例值：20091225091010 |
| `async.resp_data.trans_finish_time` | `async.resp_data` | `$.trans_finish_time` | 汇付侧交易完成时间 | `String` | `13` | `N` | 已确认 | 毫秒时间戳，示例值：1791598928000 |
| `async.resp_data.debit_flag` | `async.resp_data` | `$.debit_flag` | 借贷记标识 | `String` | `1` | `N` | 已确认 | D-借记卡 C-信用卡 Z-借贷合一卡示例值：C |
| `async.resp_data.wx_user_id` | `async.resp_data` | `$.wx_user_id` | 微信用户唯一标识码 | `String` | `128` | `N` | 已确认 | 示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk= |
| `async.resp_data.wx_response` | `async.resp_data` | `$.wx_response（String(JSON) 容器）` | 微信返回的响应报文 | `String` | `6000` | `N` | 已确认 | JsonObject格式 |
| `async.resp_data.wx_response.sub_appid` | `async.resp_data` | `$.wx_response => JSON decode => $.sub_appid` | 子商户公众账号ID | `String` | `32` | `N` | 已确认 | 微信分配的子商户公众账号ID；示例值：wxec280d4c8a1cc2ca |
| `async.resp_data.wx_response.openid` | `async.resp_data` | `$.wx_response => JSON decode => $.openid` | 用户标识 | `String` | `128` | `Y` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `async.resp_data.wx_response.sub_openid` | `async.resp_data` | `$.wx_response => JSON decode => $.sub_openid` | 用户子标识 | `String` | `128` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `async.resp_data.wx_response.bank_type` | `async.resp_data` | `$.wx_response => JSON decode => $.bank_type` | 付款银行 | `String` | `16` | `Y` | 已确认 | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/wiki/doc/apiv3/terms_definition/chapter1_1_3.shtml#part-7)；示例值：OTHERS |
| `async.resp_data.wx_response.cash_fee` | `async.resp_data` | `$.wx_response => JSON decode => $.cash_fee` | 现金支付金额 | `String` | `12` | `N` | 已确认 | 订单现金支付金额；示例值：10.00 |
| `async.resp_data.wx_response.coupon_fee` | `async.resp_data` | `$.wx_response => JSON decode => $.coupon_fee` | 代金券金额 | `String` | `12` | `N` | 已确认 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：1.00 |
| `async.resp_data.wx_response.attach` | `async.resp_data` | `$.wx_response => JSON decode => $.attach` | 商家数据包 | `String` | `128` | `N` | 已确认 | 原样返回；示例值：附加数据 |
| `async.resp_data.wx_response.promotion_detail[]` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[]` | 营销详情列表 | `Array` | `6000` | `N` | 已确认 | 营销详情列表，使返回值为Json格式 |
| `async.resp_data.wx_response.promotion_detail[].promotion_id` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].promotion_id` | 券或者立减优惠id | `String` | `32` | `Y` | 已确认 | 示例值：2345234235 |
| `async.resp_data.wx_response.promotion_detail[].name` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `async.resp_data.wx_response.promotion_detail[].scope` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL: 全场代金券，SINGLE: 单品优惠；示例值：SINGLE |
| `async.resp_data.wx_response.promotion_detail[].type` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON: 代金券，需要走结算资金的充值型代金券,境外商户券币种与支付币种一致；DISCOUNT: 优惠券，不走结算资金的免充值型优惠券，境外商户券币种与标价币种一致；示例值：DISCOUNT |
| `async.resp_data.wx_response.promotion_detail[].amount` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].amount` | 优惠券面额 | `String` | `5` | `Y` | 已确认 | 用户享受优惠的金额；示例值：10.00 |
| `async.resp_data.wx_response.promotion_detail[].activity_id` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].activity_id` | 活动ID | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `async.resp_data.wx_response.promotion_detail[].merchant_contribute` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].merchant_contribute` | 商户出资(元) | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额；示例值：10.00 |
| `async.resp_data.wx_response.promotion_detail[].other_contribute` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].other_contribute` | 其他出资(元) | `String` | `32` | `N` | 已确认 | 其他出资方出资金额；示例值：5.00 |
| `async.resp_data.wx_response.promotion_detail[].goods_detail` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].goods_detail` | 单品列表 | `Object` | `3000` | `N` | 已确认 | 使用Json格式 |
| `async.resp_data.wx_response.promotion_detail[].goods_detail.goods_id` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].goods_detail.goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `async.resp_data.wx_response.promotion_detail[].goods_detail.goods_remark` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].goods_detail.goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。；示例值：商品备注 |
| `async.resp_data.wx_response.promotion_detail[].goods_detail.discount_amount` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].goods_detail.discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，单位为：元；示例值：20.00 |
| `async.resp_data.wx_response.promotion_detail[].goods_detail.quantity` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].goods_detail.quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `async.resp_data.wx_response.promotion_detail[].goods_detail.price` | `async.resp_data` | `$.wx_response => JSON decode => $.promotion_detail[].goods_detail.price` | 商品价格(元) | `String` | `32` | `Y` | 已确认 | 示例值：50.00。如果商户有优惠，需传输商户优惠后的单价。；例如：100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50 |
| `async.resp_data.is_div` | `async.resp_data` | `$.is_div` | 是否分账交易 | `String` | `1` | `Y` | 已确认 | 1: 分账交易, 0: 非分账交易；示例值：1 |
| `async.resp_data.acct_split_bunch` | `async.resp_data` | `$.acct_split_bunch（String(JSON) 容器）` | 分账对象 | `String` | `2048` | `N` | 已确认 | 分账对象，jsonObject字符串 |
| `async.resp_data.acct_split_bunch.acct_infos[]` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[]` | 分账明细 | `Array` | `2048` | `Y` | 已确认 | 分账明细 |
| `async.resp_data.acct_split_bunch.acct_infos[].div_amt` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.resp_data.acct_split_bunch.acct_infos[].huifu_id` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `async.resp_data.acct_split_bunch.acct_infos[].acct_id` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[].acct_id` | 收款汇付账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，示例值：A14186488；仅支持微信、支付宝、网银交易指定收款账户 |
| `async.resp_data.acct_split_bunch.acct_infos[].acct_date` | `async.resp_data` | `$.acct_split_bunch => JSON decode => $.acct_infos[].acct_date` | 账务日期 | `String` | `8` | `N` | 已确认 | 示例值：20221023 |
| `async.resp_data.is_delay_acct` | `async.resp_data` | `$.is_delay_acct` | 是否延时交易 | `String` | `1` | `Y` | 已确认 | 1: 延迟 0: 不延迟；示例值：1 |
| `async.resp_data.fee_flag` | `async.resp_data` | `$.fee_flag` | 手续费扣款标志 | `Int` | `1` | `N` | 已确认 | 1: 外扣，2: 内扣；默认返回控台配置方式；示例值：1 |
| `async.resp_data.trans_fee_allowance_info` | `async.resp_data` | `$.trans_fee_allowance_info（String(JSON) 容器）` | 手续费补贴信息 | `String` | `6000` | `N` | 已确认 | JsonObject格式 |
| `async.resp_data.trans_fee_allowance_info.receivable_fee_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.receivable_fee_amt` | 商户应收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `async.resp_data.trans_fee_allowance_info.actual_fee_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.actual_fee_amt` | 商户实收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `async.resp_data.trans_fee_allowance_info.allowance_fee_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.allowance_fee_amt` | 补贴手续费 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `async.resp_data.trans_fee_allowance_info.allowance_type` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.allowance_type` | 补贴类型 | `String` | `10` | `N` | 已确认 | 0：不补贴，为空默认；1：补贴；2：部分补贴；3：全额补贴(优惠后)；4：部分补贴(优惠后)；示例值：2 |
| `async.resp_data.trans_fee_allowance_info.no_allowance_desc` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.no_allowance_desc` | 不补贴原因 | `String` | `128` | `N` | 已确认 | 补贴系统返回的不补贴原因；1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴；2:额度用完；3:不在有效期；4:活动不存在；5:手续费金额为0不补贴；6:顶格优惠；7:额度不足；8:手续费后补；9:未达到起始补贴金额；示例值：2 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[]` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[]` | 手续费补贴活动详情 | `Array` | `—` | `N` | N/A：结构字段长度 | 补贴系统返回，斗拱原样返回 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].acct_id` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].acct_id` | 门店 | `String` | `64` | `N` | 已确认 | 示例值：sh002 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].merchant_group` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].merchant_group` | 商户号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].allowance_sys` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].allowance_sys` | 补贴方 | `String` | `64` | `N` | 已确认 | 1:银行 2:服务商 3:汇来米；示例值：1 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].allowance_sys_id` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].allowance_sys_id` | 补贴方ID | `String` | `64` | `N` | 已确认 | 对应补贴方的id；示例值：[官网示例已脱敏] |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].is_delay_allowance` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].is_delay_allowance` | 补贴类型 | `String` | `2` | `N` | 已确认 | 1:实补 2:后补,默认实补；示例值：1 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].market_id` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].market_id` | 自定义活动编号 | `String` | `64` | `N` | 已确认 | 示例值：ISFE00232 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].market_name` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].market_name` | 自定义活动名称 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].market_desc` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].market_desc` | 自定义活动描述 | `String` | `64` | `N` | 已确认 | 示例值：新店开业大促 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].start_time` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].start_time` | 活动开始时间 | `String` | `8` | `N` | 已确认 | yyyyMMdd；示例值：20220909 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].end_time` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].end_time` | 活动结束时间 | `String` | `8` | `N` | 已确认 | yyyyMMdd；示例值：20220919 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].pos_debit_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].pos_debit_limit_amt` | pos借记卡补贴额度 | `String` | `16` | `N` | 已确认 | 示例值：2.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].pos_credit_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].pos_credit_limit_amt` | pos贷记卡补贴额度 | `String` | `16` | `N` | 已确认 | 示例值：5.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].pos_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].pos_limit_amt` | pos补贴额度 | `String` | `16` | `N` | 已确认 | 示例值：4.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].qr_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].qr_limit_amt` | 扫码补贴额度 | `String` | `16` | `N` | 已确认 | 示例值：1.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].total_limit_amt` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].total_limit_amt` | 活动总补贴额度 | `String` | `16` | `N` | 已确认 | 示例值：10.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].status` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].status` | 活动是否有效 | `String` | `4` | `N` | 已确认 | 1:生效 0：失效；示例值：1 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].human_flag` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].human_flag` | 是否人工操作 | `String` | `4` | `N` | 已确认 | N：自动 Y：人工；示例值：N |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].activity_id` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].activity_id` | 活动号 | `String` | `64` | `N` | 已确认 | 示例值：223402342 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].activity_name` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].activity_name` | 活动描述 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].create_by` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].create_by` | 创建人 | `String` | `32` | `N` | 已确认 | 示例值：Lg[官网示例已脱敏] |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].create_time` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].create_time` | 创建时间 | `String` | `32` | `N` | 已确认 | 示例值：2022-04-14 22:00:30 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos[].update_time` | `async.resp_data` | `$.trans_fee_allowance_info => JSON decode => $.cur_allowance_config_infos[].update_time` | 更新时间 | `String` | `32` | `N` | 已确认 | 示例值：2022-04-14 23:00:30 |
| `async.resp_data.fee_formula_infos[]` | `async.resp_data` | `$.fee_formula_infos（String(JSON Array) 容器）` | 手续费费率信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray格式；微信、支付宝、云闪付交易成功时返回手续费费率信息 |
| `async.resp_data.fee_formula_infos[].fee_formula` | `async.resp_data` | `$.fee_formula_infos => JSON decode => $[].fee_formula` | 手续费计算公式 | `String` | `512` | `Y` | 已确认 | 示例值：AMT*0.003 |
| `async.resp_data.fee_formula_infos[].fee_type` | `async.resp_data` | `$.fee_formula_infos => JSON decode => $[].fee_type` | 手续费类型 | `String` | `32` | `Y` | 已确认 | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；示例值：ACCT_FEE |
| `async.resp_data.fee_formula_infos[].huifu_id` | `async.resp_data` | `$.fee_formula_infos => JSON decode => $[].huifu_id` | 商户号 | `String` | `32` | `N` | 已确认 | 补贴支付账户补贴时，补贴账户的huifuId；示例值：[官网示例已脱敏] |
| `async.resp_data.fee_formula_infos[].fee_sign` | `async.resp_data` | `$.fee_formula_infos => JSON decode => $[].fee_sign` | 手续费场景标识 | `String` | `32` | `N` | 已确认 | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。；示例值：6850aad1e92f4244a74a42fcc1ad6360 |
| `async.resp_data.remark` | `async.resp_data` | `$.remark` | 备注 | `String` | `45` | `N` | 已确认 | 原样返回；示例值：备注 |
| `async.resp_data.bank_code` | `async.resp_data` | `$.bank_code` | 通道返回码 | `String` | `32` | `N` | 已确认 | 示例值：00 |
| `async.resp_data.bank_message` | `async.resp_data` | `$.bank_message` | 通道返回描述 | `String` | `200` | `N` | 已确认 | 示例值：成功[0000000] |
| `async.resp_data.devs_id` | `async.resp_data` | `$.devs_id` | 汇付机具号 | `String` | `32` | `Y` | 已确认 | 通过汇付报备的机具必传；示例值：[官网示例已脱敏] |
| `async.resp_data.sub_orders_response[]` | `async.resp_data` | `$.sub_orders_response（String(JSON Array) 容器）` | 子单信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray格式；子单信息，合单支付的订单返回该字段 |
| `async.resp_data.sub_orders_response[].sub_req_seq_id` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_req_seq_id` | 子单请求流水号 | `String` | `128` | `Y` | 已确认 | 交易时传入，原样返回；示例值：SUB[官网示例已脱敏] |
| `async.resp_data.sub_orders_response[].sub_hf_seq_id` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_hf_seq_id` | 子单全局流水号 | `String` | `128` | `Y` | 已确认 | 示例值：00470topo1A221019132207P068ac1362af00001 |
| `async.resp_data.sub_orders_response[].sub_huifu_id` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_huifu_id` | 子单商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.sub_orders_response[].sub_acct_id` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_acct_id` | 子单账户号 | `String` | `9` | `Y` | 已确认 | 示例值：A123456 |
| `async.resp_data.sub_orders_response[].sub_trams_amt` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_trams_amt` | 子单交易金额 | `String` | `14` | `Y` | 已确认 | 位元；示例值：1.00 |
| `async.resp_data.sub_orders_response[].sub_settlement_amt` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_settlement_amt` | 子单结算金额 | `String` | `14` | `N` | 已确认 | 位元；示例值：1.00 |
| `async.resp_data.sub_orders_response[].sub_remark` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].sub_remark` | 子单备注信息 | `String` | `255` | `N` | 已确认 | 原样返回；示例值：子单备注 |
| `async.resp_data.sub_orders_response[].acct_date` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].acct_date` | 子单入账日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20091225 |
| `async.resp_data.sub_orders_response[].acct_stat` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].acct_stat` | 子单账务状态 | `String` | `1` | `N` | 已确认 | "I：初始"; "P:处理中"; "S:成功"; "F:失败。示例值：S； 返回“I：初始”状态时，请联系客服确认订单问题 |
| `async.resp_data.sub_orders_response[].is_div` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].is_div` | 是否分账交易 | `String` | `1` | `N` | 已确认 | 1:分账交易， 0:非分账交易；示例值：1 |
| `async.resp_data.sub_orders_response[].acct_split_bunch` | `async.resp_data` | `$.sub_orders_response[].acct_split_bunch（String(JSON) 容器）` | 分账对象 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `async.resp_data.sub_orders_response[].acct_split_bunch.acct_infos[]` | `async.resp_data` | `$.sub_orders_response[].acct_split_bunch.acct_infos（String(JSON Array) 容器）` | 分账明细 | `String` | `—` | `Y` | [需要官方确认]：长度 | jsonArray分账明细 |
| `async.resp_data.sub_orders_response[].acct_split_bunch.acct_infos[].div_amt` | `async.resp_data` | `$.sub_orders_response[].acct_split_bunch.acct_infos => JSON decode => $[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 ，最低传入0.01 |
| `async.resp_data.sub_orders_response[].acct_split_bunch.acct_infos[].huifu_id` | `async.resp_data` | `$.sub_orders_response[].acct_split_bunch.acct_infos => JSON decode => $[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `async.resp_data.sub_orders_response[].acct_split_bunch.acct_infos[].acct_id` | `async.resp_data` | `$.sub_orders_response[].acct_split_bunch.acct_infos => JSON decode => $[].acct_id` | 分账接收方账户号 | `String` | `9` | `N` | 已确认 | 示例值：A123456 |
| `async.resp_data.sub_orders_response[].fee_infos` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 交易手续费信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 交易手续费信息 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_formula` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 手续费计算公式 | `String` | `512` | `N` | 已确认 | 示例值：AMT\*0.003 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_huifu_id` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 手续费扣款商户号 | `String` | `32` | `N` | 已确认 | — |
| `async.resp_data.sub_orders_response[].fee_infos.fee_acct_id` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 手续费扣款账户号 | `String` | `9` | `N` | 已确认 | — |
| `async.resp_data.sub_orders_response[].fee_infos.fee_flag` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 手续费扣款标志 | `Integer` | `1` | `N` | 已确认 | 1: 外扣，2: 内扣；示例值：2 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_rec_type` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 手续费扣取方式 | `Integer` | `1` | `N` | 已确认 | 1: 实收，2: 后收；示例值：1 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_amount` | `async.resp_data` | `$.sub_orders_response[].fee_infos => [需要官方确认]：String 子表编码` | 手续费金额 | `String` | `16` | `N` | 已确认 | 单位元，保留小数点后两位。根据手续费公式计算的手续费小于0.01时，至少收取0.01元。示例值：1.00 |
| `async.resp_data.sub_orders_response[].split_fee_info` | `async.resp_data` | `$.sub_orders_response[].split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 分账手续费信息 |
| `async.resp_data.sub_orders_response[].split_fee_info.total_split_fee_amt` | `async.resp_data` | `$.sub_orders_response[].split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费总金额(元) | `String` | `14` | `N` | 已确认 | 示例值：0.10 |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_flag` | `async.resp_data` | `$.sub_orders_response[].split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费扣款标志 | `Integer` | `1` | `Y` | 已确认 | 1: 外扣 2: 内扣；示例值：2 |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_details` | `async.resp_data` | `$.sub_orders_response[].split_fee_info.split_fee_details => [需要官方确认]：String 子表编码` | 分账手续费信息 | `String` | `—` | `Y` | [需要官方确认]：长度 | 分账手续费信息 |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_details.split_fee_amt` | `async.resp_data` | `$.sub_orders_response[].split_fee_info.split_fee_details => [需要官方确认]：String 子表编码` | 分账手续费金额(元) | `String` | `16` | `Y` | 已确认 | 示例值：0.10 |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_details.split_fee_huifu_id` | `async.resp_data` | `$.sub_orders_response[].split_fee_info.split_fee_details => [需要官方确认]：String 子表编码` | 分账手续费承担方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_details.split_fee_acct_id` | `async.resp_data` | `$.sub_orders_response[].split_fee_info.split_fee_details => [需要官方确认]：String 子表编码` | 分账手续费承担方账号 | `String` | `9` | `N` | 已确认 | 示例值：F00598600 |
| `async.resp_data.sub_orders_response[].fund_freeze_stat` | `async.resp_data` | `$.sub_orders_response => JSON decode => $[].fund_freeze_stat` | 资金冻结状态 | `String` | `16` | `N` | 已确认 | FREEZE：冻结；UNFREEZE：解冻；示例值：UNFREEZE |

### 拆单支付异步 resp_data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.split.resp_data.resp_code` | `async.split.resp_data` | `$.resp_code` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_wxpreorder.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：00000000 |
| `async.split.resp_data.resp_desc` | `async.split.resp_data` | `$.resp_desc` | 业务返回信息 | `String` | `512` | `Y` | 已确认 | 业务返回描述；示例值：处理成功 |
| `async.split.resp_data.huifu_id` | `async.split.resp_data` | `$.huifu_id` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.split.resp_data.req_date` | `async.split.resp_data` | `$.req_date` | 请求时间 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回，格式为yyyyMMdd，示例值：20091225 |
| `async.split.resp_data.req_seq_id` | `async.split.resp_data` | `$.req_seq_id` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 交易时传入，原样返回；示例值：[官网示例已脱敏] |
| `async.split.resp_data.trans_stat` | `async.split.resp_data` | `$.trans_stat` | 交易状态 | `String` | `1` | `Y` | 已确认 | S：成功、F：失败；示例值：S |
| `async.split.resp_data.sys_id` | `async.split.resp_data` | `$.sys_id` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |

## 抖音直连下单

- 原始地址：<https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_dypreorder.md>
- SHA-256：`2aae00b6db20e91f71720a3e3bbb2c8c424ee1959b3dea4feeac502a9fc5478d`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.pre_order_type` | `request.data.pre_order_type` | `—（直接 JSON 路径）` | 预下单类型 | `String` | `1` | `Y` | 已确认 | 抖音直连下单：4；示例值：4 |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 请求格式：yyyyMMdd；示例值：20221023 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 开户自动生成；示例值：[官网示例已脱敏] |
| `request.data.trans_amt` | `request.data.trans_amt` | `—（直接 JSON 路径）` | 交易金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `request.data.goods_desc` | `request.data.goods_desc` | `—（直接 JSON 路径）` | 商品描述 | `String` | `40` | `Y` | 已确认 | 示例值：个人电脑 |
| `request.data.time_expire` | `request.data.time_expire` | `—（直接 JSON 路径）` | 交易失效时间 | `String` | `14` | `N` | 已确认 | 请求格式：yyyyMMddHHmmss；示例值：20220912111230；注意:为空默认失效时间为10分钟；用户在交易失效时间后完成交易有可能被关单。最终结果以异步为准；建议商户在交易量大时，或在搞营销活动时将失效时间设置短一些。 |
| `request.data.notify_url` | `request.data.notify_url` | `—（直接 JSON 路径）` | 交易异步通知地址 | `String` | `512` | `N` | 已确认 | http或https开头，示例值：https://callback.service.com/xx；在交易成功/失败时触发回调，正常情况下只会触发一次，具体回调策略参见[链接](https://paas.huifu.com/open/doc/api_standard/#/ybxx/jiekouguifan_ybxx) |
| `request.data.dy_data` | `request.data.dy_data` | `—（String(JSON) 容器）` | 抖音参数集合 | `String` | `2048` | `Y` | 已确认 | jsonObject字符串 |
| `request.data.dy_data.sub_appid` | `request.data.dy_data` | `$.sub_appid` | 子商户应用ID | `String` | `32` | `Y` | 已确认 | 子商户/二级商户在抖音开放平台申请的应用ID，全局唯一。；此处请填写移动应用类型的AppID，并确保该sub_appid与sub_mchid有绑定关系。；示例值：awofz9bncda6x7w8 |
| `request.data.dy_data.busi_scene` | `request.data.dy_data` | `$.busi_scene` | 业务场景 | `String` | `3` | `Y` | 已确认 | APP、H5；示例值：H5 |
| `request.data.dy_data.coupon_info` | `request.data.dy_data` | `$.coupon_info（String(JSON) 容器）` | 优惠标记 | `String` | `1024` | `N` | 已确认 | 1、json格式。和抖音支付协商后可用。；2、传参说明：；（1）业务场景区分，可通过传入key值=biz_scene，value值为约定场景值。；（2）个性化策略区分，可通过传入key值=product_tag，value值为约定参数值。；（3）指定优惠信息区分，可通过传入key值=assign_discounts，value值为“抖音支付优惠查询接口”返回的“指定优惠信息”字段值。；示例值：{"biz_scene":"xxx","product_tag":"xxx","assign_discounts":"xxx"} |
| `request.data.dy_data.h5_info` | `request.data.dy_data` | `$.h5_info` | H5场景信息 | `Object` | `2048` | `C` | 已确认 | 业务场景为H5时必填 |
| `request.data.dy_data.h5_info.type` | `request.data.dy_data` | `$.h5_info.type` | 场景类型 | `String` | `32` | `Y` | 已确认 | Ios, Android, Wap示例值：Ios |
| `request.data.dy_data.h5_info.app_name` | `request.data.dy_data` | `$.h5_info.app_name` | 应用名称 | `String` | `64` | `N` | 已确认 | 示例值：抖音 |
| `request.data.dy_data.h5_info.app_url` | `request.data.dy_data` | `$.h5_info.app_url` | 网站URL | `String` | `128` | `N` | 已确认 | 示例值：示例值：https://douyinpay.com/ |
| `request.data.dy_data.h5_info.bundle_id` | `request.data.dy_data` | `$.h5_info.bundle_id` | iOS平台BundleID | `String` | `128` | `N` | 已确认 | iOS平台BundleID |
| `request.data.dy_data.h5_info.package_name` | `request.data.dy_data` | `$.h5_info.package_name` | Android平台PackageName | `String` | `128` | `N` | 已确认 | Android平台PackageName |
| `request.data.dy_data.scene_info` | `request.data.dy_data` | `$.scene_info` | 场景信息 | `Object` | `2048` | `Y` | 已确认 | 支付场景描述 |
| `request.data.dy_data.scene_info.payer_client_ip` | `request.data.dy_data` | `$.scene_info.payer_client_ip` | 用户终端IP | `String` | `45` | `Y` | 已确认 | 用户的客户端IP，支持IPv4和IPv6两种格式的IP地址；示例值：14.23.150.211 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_dypreorder.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `128` | `Y` | 已确认 | 业务返回描述；示例值：处理成功 |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：20221023 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：[官网示例已脱敏] |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：[官网示例已脱敏] |
| `response.data.trans_amt` | `response.data.trans_amt` | `—（直接 JSON 路径）` | 交易金额 | `String` | `12` | `Y` | 已确认 | 预下单时传入，原样返回；示例值：100.00 |
| `response.data.jump_url` | `response.data.jump_url` | `—（直接 JSON 路径）` | 预支付会话标识 | `String` | `256` | `Y` | 已确认 | app场景：预支付交易会话标识。用于后续接口调用中使用，该值有效期为2小时；示例值：{\\"package\\":\\"Sign=DYPay\\",\\"appid\\":\\"aaaa\\",\\"sign\\":\\"aa4Wec0=\\",\\"partnerid\\":\\"6660001\\",\\"prepayid\\":\\"dy12346\\",\\"noncestr\\":\\"628easdfadsf\\",\\"timestamp\\":\\"1770277075\\"}；H5场景：拉起抖音支付收银台的中间页面，可通过访问该url来拉起抖音客户端，完成支付，h5_url的有效期为5分钟。；示例值：https://cashier.ulpay.com/bytepay-cashdesk/bytepay-invoke?prepay_id=dy96y894ox66yv43x10uquv34s5s7sx3oso28squqsx |

### 支付异步 resp_data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.resp_data.resp_code` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_dypreorder.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：00000000 |
| `async.resp_data.resp_desc` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 业务返回信息 | `String` | `512` | `Y` | 已确认 | 业务返回描述；示例值：处理成功 |
| `async.resp_data.req_seq_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 交易时传入，原样返回；示例值：[官网示例已脱敏] |
| `async.resp_data.req_date` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 请求时间 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回，格式为yyyyMMdd，示例值：20091225 |
| `async.resp_data.hf_seq_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 汇付全局流水号 | `String` | `40` | `N` | 已确认 | 示例值：00470topo1A211015160805P090ac132fef00000 |
| `async.resp_data.out_trans_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 用户账单上的交易订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.resp_data.party_order_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 用户账单上的商户订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.resp_data.huifu_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.trans_type` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 交易类型 | `String` | `20` | `N` | 已确认 | Y_APP：抖音APP支付；Y_H5：抖音H5支付；示例值：Y_H5 |
| `async.resp_data.trans_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 交易金额 | `String` | `12` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.resp_data.settlement_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 结算金额 | `String` | `16` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.resp_data.trans_stat` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 交易状态 | `String` | `1` | `N` | 已确认 | S：成功、F：失败；示例值：S |
| `async.resp_data.trans_finish_time` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 汇付侧交易完成时间 | `String` | `13` | `N` | 已确认 | 毫秒时间戳，示例值：1791598928000 |
| `async.resp_data.end_time` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 支付完成时间 | `String` | `14` | `N` | 已确认 | 格式yyyyMMddHHmmss，示例值：20091225091010 |
| `async.resp_data.acct_date` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 入账时间 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20091225 |
| `async.resp_data.dy_response` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 抖音返回的响应报文 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `async.resp_data.dy_response.sub_appid` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 子商户应用ID | `String` | `32` | `N` | 已确认 | 在抖音开放平台申请的应用ID，全局唯一。此处请填写移动应用（APP）/网站应用（H5）类型的AppID |
| `async.resp_data.dy_response.openid` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 用户标识 | `String` | `128` | `Y` | 已确认 | 用户在商户appid下的唯一标识；示例值：897ae8bd9f194107-9cb3-85f5672037de |
| `async.resp_data.dy_response.sub_openid` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：823ae8bd9f893402-9cb3-85f8794657ea |
| `async.resp_data.dy_response.bank_type` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 付款银行 | `String` | `16` | `Y` | 已确认 | 银行类型，采用字符串类型的银行标识示例值：OTHERS |
| `async.resp_data.dy_response.promotion_detail` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 营销详情列表 | `String` | `—` | `N` | [需要官方确认]：长度 | 营销详情列表，使返回值为Json格式 |
| `async.resp_data.dy_response.promotion_detail.coupon_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 券id | `String` | `32` | `N` | 已确认 | 券或者立减优惠id；示例值：2345234235 |
| `async.resp_data.dy_response.promotion_detail.name` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `async.resp_data.dy_response.promotion_detail.scope` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL: 全场代金券，SINGLE: 单品优惠；示例值：GLOBAL |
| `async.resp_data.dy_response.promotion_detail.type` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 优惠类型 | `String` | `32` | `N` | 已确认 | CASH: 充值型代金券；NOCASH：免充值型代金券；示例值：CASH |
| `async.resp_data.dy_response.promotion_detail.amount` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 优惠券面额 | `String` | `12` | `Y` | 已确认 | 示例值：5.00 |
| `async.resp_data.dy_response.promotion_detail.stock_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 活动ID | `String` | `32` | `N` | 已确认 | 活动ID |
| `async.resp_data.dy_response.promotion_detail.douyinpay_contribute` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 抖音出资 | `String` | `32` | `N` | 已确认 | 抖音出资，单位为元；示例值：10.00 |
| `async.resp_data.dy_response.promotion_detail.merchant_contribute` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 商户出资 | `String` | `32` | `N` | 已确认 | 商户出资，单位为元；示例值：10.00 |
| `async.resp_data.dy_response.promotion_detail.other_contribute` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 其他出资 | `String` | `32` | `N` | 已确认 | 其他出资，单位为元；示例值：20.00 |
| `async.resp_data.dy_response.promotion_detail.currency` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 优惠币种 | `String` | `32` | `N` | 已确认 | CNY：人民币，境内商户号仅支持人民币 |
| `async.resp_data.dy_response.promotion_detail.goods_detail[]` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 单品列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 单品信息，使用Json格式，是promotion_detail的元素 |
| `async.resp_data.dy_response.promotion_detail.goods_detail[].goods_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `async.resp_data.dy_response.promotion_detail.goods_detail[].quantity` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `async.resp_data.dy_response.promotion_detail.goods_detail[].unit_price` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 商品单价 | `String` | `32` | `N` | 已确认 | 单位为:元。示例值：99.00 |
| `async.resp_data.dy_response.promotion_detail.goods_detail[].discount_amount` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，单位为：元；示例值：20.00 |
| `async.resp_data.dy_response.promotion_detail.goods_detail[].goods_remark` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 商品备注 | `String` | `128` | `N` | 已确认 | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。；示例值：商品备注 |
| `async.resp_data.is_div` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 是否分账交易 | `String` | `1` | `Y` | 已确认 | 1: 分账交易, 0: 非分账交易；示例值：1 |
| `async.resp_data.acct_split_bunch` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账对象 | `String` | `2048` | `N` | 已确认 | 分账对象，jsonObject字符串 |
| `async.resp_data.acct_split_bunch.acct_infos[]` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账明细 | `Array` | `2048` | `Y` | 已确认 | 分账明细 |
| `async.resp_data.acct_split_bunch.acct_infos[].div_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.resp_data.acct_split_bunch.acct_infos[].huifu_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `async.resp_data.acct_split_bunch.acct_infos[].acct_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 收款汇付账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，示例值：A14186488；仅支持微信、支付宝、网银交易指定收款账户 |
| `async.resp_data.acct_split_bunch.acct_infos[].acct_date` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 账务日期 | `String` | `8` | `N` | 已确认 | 示例值：20221023 |
| `async.resp_data.is_delay_acct` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 是否延时交易 | `String` | `1` | `Y` | 已确认 | 1: 延迟 0: 不延迟；示例值：1 |
| `async.resp_data.fee_flag` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 手续费扣款标志 | `Int` | `1` | `N` | 已确认 | 1: 外扣，2: 内扣；默认返回控台配置方式；示例值：2 |
| `async.resp_data.fee_amount` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 手续费金额 | `String` | `16` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.resp_data.trans_fee_allowance_info` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 手续费补贴信息 | `Object` | `6000` | `N` | 已确认 | jsonObject格式 |
| `async.resp_data.trans_fee_allowance_info.receivable_fee_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 商户应收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `async.resp_data.trans_fee_allowance_info.actual_fee_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 商户实收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `async.resp_data.trans_fee_allowance_info.allowance_fee_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 补贴手续费 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `async.resp_data.trans_fee_allowance_info.allowance_type` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 补贴类型 | `String` | `10` | `N` | 已确认 | 0：不补贴，为空默认；1：补贴；2：部分补贴；3：全额补贴(优惠后)；4：部分补贴(优惠后)；示例值：2 |
| `async.resp_data.trans_fee_allowance_info.no_allowance_desc` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 不补贴原因 | `String` | `128` | `N` | 已确认 | 补贴系统返回的不补贴原因；1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴；2:额度用完；3:不在有效期；4:活动不存在；5:手续费金额为0不补贴；6:顶格优惠；7:额度不足；8:手续费后补；9:未达到起始补贴金额；示例值：2 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 手续费补贴活动详情 | `Object` | `—` | `N` | N/A：结构字段长度 | 补贴系统返回，斗拱原样返回 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.acct_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 门店 | `String` | `64` | `N` | 已确认 | 示例值：sh002 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.merchant_group` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 商户号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 补贴方 | `String` | `64` | `Y` | 已确认 | 1:银行 2:服务商 3:汇来米；示例值：1 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 补贴方ID | `String` | `64` | `Y` | 已确认 | 对应补贴方的id；示例值：[官网示例已脱敏] |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.is_delay_allowance` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 补贴类型 | `String` | `2` | `Y` | 已确认 | 1:实补 2:后补,默认实补；示例值：1 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 自定义活动编号 | `String` | `64` | `Y` | 已确认 | 示例值：ISFE00232 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_name` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 自定义活动名称 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.market_desc` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 自定义活动描述 | `String` | `64` | `N` | 已确认 | 示例值：新店开业大促 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.start_time` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 活动开始时间 | `String` | `8` | `Y` | 已确认 | yyyyMMdd；示例值：20220909 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.end_time` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 活动结束时间 | `String` | `8` | `Y` | 已确认 | yyyyMMdd；示例值：20220913 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_debit_limit_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | pos借记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：2.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_credit_limit_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | pos贷记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.pos_limit_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | pos补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.qr_limit_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 扫码补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.total_limit_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 活动总补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：10.00 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.status` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 活动是否有效 | `String` | `4` | `Y` | 已确认 | 1:生效 0：失效；示例值：1 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.human_flag` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 是否人工操作 | `String` | `4` | `Y` | 已确认 | N：自动 Y：人工；示例值：N |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.activity_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 活动号 | `String` | `64` | `Y` | 已确认 | 示例值：223402342 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.activity_name` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 活动描述 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.create_by` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 创建人 | `String` | `32` | `Y` | 已确认 | 示例值：Lg[官网示例已脱敏] |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.create_time` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 创建时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 22:00:30 |
| `async.resp_data.trans_fee_allowance_info.cur_allowance_config_infos.update_time` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 更新时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 23:00:30 |
| `async.resp_data.remark` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 备注 | `String` | `45` | `N` | 已确认 | 原样返回；示例值：备注 |
| `async.resp_data.bank_code` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 通道返回码 | `String` | `32` | `N` | 已确认 | 示例值：00 |
| `async.resp_data.bank_message` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 通道返回描述 | `String` | `200` | `N` | 已确认 | 示例值：成功[0000000] |
| `async.resp_data.bank_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 收款方银行代号 | `String` | `8` | `N` | 已确认 | 快捷、网银返回；示例值：01040000 |
| `async.resp_data.bank_extend_param` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 银行扩展信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject格式；网银返回 |
| `async.resp_data.bank_extend_param.gate_type` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 网关支付类型 | `String` | `2` | `N` | 已确认 | 01: 个人网关02:企业网关；示例值：02 |
| `async.resp_data.bank_extend_param.bank_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 付款方银行号 | `String` | `32` | `N` | 已确认 | 示例值：01040000 |
| `async.resp_data.bank_extend_param.pyer_acct_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 付款方银行账户 | `String` | `1024` | `N` | 已确认 | B2B支付成功后可能返回密文；示例值：[官网示例已脱敏] |
| `async.resp_data.bank_extend_param.pyer_acct_nm` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 付款方银行账户名 | `String` | `128` | `N` | 已确认 | 示例值：上海汇付支付有限公司 |
| `async.resp_data.fee_formula_infos[]` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 手续费费率信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray格式；微信、支付宝、云闪付交易成功时返回手续费费率信息 |
| `async.resp_data.fee_formula_infos[].fee_formula` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 手续费计算公式 | `String` | `512` | `Y` | 已确认 | 示例值：AMT*0.003 |
| `async.resp_data.fee_formula_infos[].fee_type` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 手续费类型 | `String` | `32` | `Y` | 已确认 | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；示例值：ACCT_FEE |
| `async.resp_data.fee_formula_infos[].huifu_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 商户号 | `String` | `32` | `N` | 已确认 | 补贴支付账户补贴时，补贴账户的huifuId；示例值：[官网示例已脱敏] |
| `async.resp_data.fee_formula_infos[].fee_sign` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 手续费场景标识 | `String` | `32` | `N` | 已确认 | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。；示例值：6850aad1e92f4244a74a42fcc1ad6360 |
| `async.resp_data.order_type` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 订单类型 | `String` | `1` | `N` | 已确认 | P-支付 R-充值 默认：P-支付；示例值：P |
| `async.resp_data.devs_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 汇付机具号 | `String` | `32` | `Y` | 已确认 | 通过汇付报备的机具必传；示例值：[官网示例已脱敏] |
| `async.resp_data.request_ip` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 请求IP | `String` | `15` | `N` | 已确认 | 付款方IP,仅在支付成功后返回;示例：192.168.1.1 |

## 托管交易查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hostingcx.md>
- SHA-256：`43a8d643d66e7657ad0de01544a48a2fd6cecc651960f22235ef886c6ca6bc86`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 请求格式：yyyyMMdd；示例值：20221023 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `C` | 已确认 | 开户自动生成；商户号不填时必填party_order_id；示例值：[官网示例已脱敏] |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `C` | 已确认 | 请求格式：yyyyMMdd；该字段不填时必填party_order_id；示例值：20221023 |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `64` | `C` | 已确认 | 该字段不填时必填party_order_id；示例值：rQ[官网示例已脱敏] |
| `request.data.party_order_id` | `request.data.party_order_id` | `—（直接 JSON 路径）` | 用户账单上的商户订单号 | `String` | `64` | `C` | 已确认 | 该字段不填时，商户号、原交易请求日期、原交易请求流水号必填；示例值：[官网示例已脱敏] |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [参见业务返回码](http://paas.huifutest.com/partners/api/#/smzf/api_qrpay_cx?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)（官网原始地址为非 HTTPS，不得静默改写）（官网原文测试域，不作为生产地址）；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [参见业务返回码](http://paas.huifutest.com/partners/api/#/smzf/api_qrpay_cx?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)（官网原始地址为非 HTTPS，不得静默改写）（官网原文测试域，不作为生产地址）；示例值：操作成功 |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 请求格式：yyyyMMdd；示例值：20221023 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 原机构请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20220125 |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原机构请求流水号 | `String` | `128` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.org_hf_seq_id` | `response.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 斗拱返回的全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00290TOP1GR210919004230P853ac[官网示例已脱敏] |
| `response.data.pre_order_id` | `response.data.pre_order_id` | `—（直接 JSON 路径）` | 预下单订单号 | `String` | `64` | `Y` | 已确认 | 示例值：H[官网示例已脱敏] |
| `response.data.order_stat` | `response.data.order_stat` | `—（直接 JSON 路径）` | 预下单状态 | `String` | `1` | `N` | 已确认 | 1:支付成功,2:支付中,3:已退款,4:处理中,5:支付失败,6-部分退款；[参见状态说明文档](http://paas.huifu.com/open/doc/api/#/cpjs/api_cpjs_statsm)（官网原始地址为非 HTTPS，不得静默改写）；示例值：1 |
| `response.data.party_order_id` | `response.data.party_order_id` | `—（直接 JSON 路径）` | 用户账单上的商户订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；[参见用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `response.data.trans_date` | `response.data.trans_date` | `—（直接 JSON 路径）` | 订单日期 | `String` | `8` | `Y` | 已确认 | 格式：yyyymmdd；示例值：20221023 |
| `response.data.trans_amt` | `response.data.trans_amt` | `—（直接 JSON 路径）` | 交易金额(元) | `String` | `14` | `Y` | 已确认 | 保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.pay_type` | `response.data.pay_type` | `—（直接 JSON 路径）` | 交易类型 | `String` | `16` | `N` | 已确认 | T_JSAPI：微信公众号支付；T_MINIAPP：微信小程序支付；A_JSAPI：支付宝JS；A_NATIVE ：支付宝正扫；U_NATIVE：银联正扫；U_JSAPI：银联 JS；QUICK_PAY：快捷支付、快捷充值(查询快捷交易必填)；ONLINE_PAY_B2B：B2B网银支付；ONLINE_PAY_B2C：B2C网银支付；UNION_PAY：银联APP统一支付；Y_H5：抖音H5支付；示例值：ONLINE_PAY_B2C |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `1` | `N` | 已确认 | P：处理中；S：成功；F：失败；I: 初始；示例值：S；初始状态很罕见，请联系汇付技术人员处理 |
| `response.data.trans_time` | `response.data.trans_time` | `—（直接 JSON 路径）` | 交易时间 | `String` | `14` | `N` | 已确认 | 格式：yyyymmddHHMMSS；示例值：20231112200913 |
| `response.data.close_stat` | `response.data.close_stat` | `—（直接 JSON 路径）` | 关单状态 | `String` | `1` | `N` | 已确认 | P：处理中、S：成功、F：失败；示例值：S |
| `response.data.fee_flag` | `response.data.fee_flag` | `—（直接 JSON 路径）` | 手续费扣款标志 | `Int` | `1` | `N` | 已确认 | 1: 外扣，2: 内扣；默认返回控台配置方式；示例值：2 |
| `response.data.fee_amt` | `response.data.fee_amt` | `—（直接 JSON 路径）` | 手续费金额(元) | `String` | `14` | `N` | 已确认 | 保留小数点后两位，最低传入0.01。示例值：1.00 |
| `response.data.ref_amt` | `response.data.ref_amt` | `—（直接 JSON 路径）` | 可退金额(元) | `String` | `14` | `N` | 已确认 | 示例值：1.00 |
| `response.data.goods_desc` | `response.data.goods_desc` | `—（直接 JSON 路径）` | 商品描述 | `String` | `40` | `N` | 已确认 | 示例值：电脑PC |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `255` | `N` | 已确认 | 原样返回；示例值：备注 |
| `response.data.mer_priv` | `response.data.mer_priv` | `—（直接 JSON 路径）` | 商户私有域 | `String` | `1500` | `N` | 已确认 | 示例值：商户私有域 |
| `response.data.bank_code` | `response.data.bank_code` | `—（直接 JSON 路径）` | 外部通道返回码 | `String` | `32` | `N` | 已确认 | 示例值：TRADE_SUCCESS |
| `response.data.bank_desc` | `response.data.bank_desc` | `—（直接 JSON 路径）` | 外部通道返回描述 | `String` | `200` | `N` | 已确认 | 示例值：TRADE_SUCCESS |
| `response.data.wx_response` | `response.data.wx_response` | `—（String(JSON) 容器）` | 微信返回的响应报文 | `String` | `6000` | `N` | 已确认 | jsonObject格式 |
| `response.data.wx_response.sub_appid` | `response.data.wx_response` | `$.sub_appid` | 子商户公众账号ID | `String` | `32` | `N` | 已确认 | 微信分配的子商户公众账号ID；示例值：wxec280d4c8a1cc2ca |
| `response.data.wx_response.openid` | `response.data.wx_response` | `$.openid` | 用户标识 | `String` | `128` | `Y` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `response.data.wx_response.sub_openid` | `response.data.wx_response` | `$.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `response.data.wx_response.bank_type` | `response.data.wx_response` | `$.bank_type` | 付款银行 | `String` | `16` | `Y` | 已确认 | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/wiki/doc/apiv3/terms_definition/chapter1_1_3.shtml#part-7)；示例值：OTHERS |
| `response.data.wx_response.cash_fee` | `response.data.wx_response` | `$.cash_fee` | 现金支付金额 | `String` | `12` | `N` | 已确认 | 订单现金支付金额；示例值：10.00 |
| `response.data.wx_response.coupon_fee` | `response.data.wx_response` | `$.coupon_fee` | 代金券金额 | `String` | `12` | `N` | 已确认 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：1.00 |
| `response.data.wx_response.attach` | `response.data.wx_response` | `$.attach` | 商家数据包 | `String` | `128` | `N` | 已确认 | 原样返回；示例值：附加数据 |
| `response.data.wx_response.promotion_detail[]` | `response.data.wx_response` | `$.promotion_detail[]` | 营销详情列表 | `Array` | `6000` | `N` | 已确认 | 营销详情列表，使返回值为Json格式 |
| `response.data.wx_response.promotion_detail[].promotion_id` | `response.data.wx_response` | `$.promotion_detail[].promotion_id` | 券或者立减优惠id | `String` | `32` | `Y` | 已确认 | 示例值：2345234235 |
| `response.data.wx_response.promotion_detail[].name` | `response.data.wx_response` | `$.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `response.data.wx_response.promotion_detail[].scope` | `response.data.wx_response` | `$.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL: 全场代金券，SINGLE: 单品优惠；示例值：SINGLE |
| `response.data.wx_response.promotion_detail[].type` | `response.data.wx_response` | `$.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON: 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致） ；DISCOUNT: 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `response.data.wx_response.promotion_detail[].amount` | `response.data.wx_response` | `$.promotion_detail[].amount` | 优惠券面额 | `String` | `5` | `Y` | 已确认 | 用户享受优惠的金额；示例值：10.00 |
| `response.data.wx_response.promotion_detail[].activity_id` | `response.data.wx_response` | `$.promotion_detail[].activity_id` | 活动ID | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `response.data.wx_response.promotion_detail[].merchant_contribute` | `response.data.wx_response` | `$.promotion_detail[].merchant_contribute` | 商户出资 | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；示例值：10.00 |
| `response.data.wx_response.promotion_detail[].other_contribute` | `response.data.wx_response` | `$.promotion_detail[].other_contribute` | 其他出资 | `String` | `32` | `N` | 已确认 | 其他出资方出资金额，单位为元；示例值：5.00 |
| `response.data.wx_response.promotion_detail[].goods_detail` | `response.data.wx_response` | `$.promotion_detail[].goods_detail` | 单品列表 | `Object` | `3000` | `N` | 已确认 | 使用Json格式 |
| `response.data.wx_response.promotion_detail[].goods_detail.goods_id` | `response.data.wx_response` | `$.promotion_detail[].goods_detail.goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `response.data.wx_response.promotion_detail[].goods_detail.goods_remark` | `response.data.wx_response` | `$.promotion_detail[].goods_detail.goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。示例值：商品备注 |
| `response.data.wx_response.promotion_detail[].goods_detail.discount_amount` | `response.data.wx_response` | `$.promotion_detail[].goods_detail.discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，单位为：元；示例值：20.00 |
| `response.data.wx_response.promotion_detail[].goods_detail.quantity` | `response.data.wx_response` | `$.promotion_detail[].goods_detail.quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `response.data.wx_response.promotion_detail[].goods_detail.price` | `response.data.wx_response` | `$.promotion_detail[].goods_detail.price` | 商品价格 | `String` | `32` | `Y` | 已确认 | 单位为: 元。示例值：50.00；如果商户有优惠，需传输商户优惠后的单价(例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50) |
| `response.data.alipay_response` | `response.data.alipay_response` | `—（String(JSON) 容器）` | 支付宝返回的响应报文 | `String` | `6000` | `N` | 已确认 | jsonObject格式 |
| `response.data.alipay_response.voucher_detail_list[]` | `response.data.alipay_response` | `$.voucher_detail_list[]` | 优惠券信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 本交易支付时使用的所有优惠券信息 |
| `response.data.alipay_response.voucher_detail_list[].id` | `response.data.alipay_response` | `$.voucher_detail_list[].id` | 券id | `String` | `32` | `Y` | 已确认 | 示例值：6934572310301 |
| `response.data.alipay_response.voucher_detail_list[].name` | `response.data.alipay_response` | `$.voucher_detail_list[].name` | 券名称 | `String` | `32` | `Y` | 已确认 | 示例值：实体店付款通用立减券 |
| `response.data.alipay_response.voucher_detail_list[].type` | `response.data.alipay_response` | `$.voucher_detail_list[].type` | 券类型 | `String` | `32` | `Y` | 已确认 | 当前有三种类型： ；ALIPAY_FIX_VOUCHER: 全场代金券；ALIPAY_DISCOUNT_VOUCHER: 折扣券；ALIPAY_ITEM_VOUCHER: 单品优惠 ；示例值：ALIPAY_ITEM_VOUCHER；注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码 |
| `response.data.alipay_response.voucher_detail_list[].amount` | `response.data.alipay_response` | `$.voucher_detail_list[].amount` | 优惠券面额（元） | `String` | `8` | `Y` | 已确认 | 它应该会等于商家出资加上其他出资方出资；示例值：10.00 |
| `response.data.alipay_response.voucher_detail_list[].merchant_contribute` | `response.data.alipay_response` | `$.voucher_detail_list[].merchant_contribute` | 商家出资 | `String` | `8` | `N` | 已确认 | 特指发起交易的商家出资金额；示例值：10.00 |
| `response.data.alipay_response.voucher_detail_list[].other_contribute` | `response.data.alipay_response` | `$.voucher_detail_list[].other_contribute` | 其他出资方出资金额 | `String` | `11` | `N` | 已确认 | 可能是支付宝、品牌商、第三方，也可能是他们的一起出资；示例值：0.00 |
| `response.data.alipay_response.fund_bill_list` | `response.data.alipay_response` | `$.fund_bill_list` | 支付金额信息 | `Object` | `512` | `N` | 已确认 | 支付成功的各个渠道金额信息，详见资金明细信息说明；json格式 |
| `response.data.alipay_response.fund_bill_list.bank_code` | `response.data.alipay_response` | `$.fund_bill_list.bank_code` | 银行代码 | `String` | `10` | `N` | 已确认 | 银行卡支付时的银行代码；示例值：CEB；请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
| `response.data.alipay_response.buyer_id` | `response.data.alipay_response` | `$.buyer_id` | 买家的支付宝唯一用户号 | `String` | `28` | `N` | 已确认 | 2088开头的16位纯数字；示例值：[官网示例已脱敏] |
| `response.data.alipay_response.buyer_logon_id` | `response.data.alipay_response` | `$.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com |
| `response.data.alipay_response.hb_fq_num` | `response.data.alipay_response` | `$.hb_fq_num` | 花呗分期数 | `String` | `10` | `N` | 已确认 | 示例值：3 |
| `response.data.alipay_response.hb_fq_seller_percent` | `response.data.alipay_response` | `$.hb_fq_seller_percent` | 卖家承担的手续费 | `String` | `3` | `N` | 已确认 | 示例值：1.00 |
| `response.data.unionpay_response` | `response.data.unionpay_response` | `—（String(JSON) 容器）` | 银联返回的响应报文 | `String` | `6000` | `N` | 已确认 | jsonObject格式 |
| `response.data.unionpay_response.coupon_info[]` | `response.data.unionpay_response` | `$.coupon_info（String(JSON Array) 容器）` | 银联优惠信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 优惠信息，银联使用优惠活动时出现，jsonArray字符串格式 |
| `response.data.unionpay_response.coupon_info[].addnInfo` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].addnInfo` | 附加信息 | `String` | `100` | `N` | 已确认 | 内容自定义；示例值：附加信息 |
| `response.data.unionpay_response.coupon_info[].spnsr_id` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].spnsr_id` | 出资方 | `String` | `20` | `Y` | 已确认 | 00010000：银联出资，示例值：00010000；未来将增加付款方等出资方 |
| `response.data.unionpay_response.coupon_info[].type` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].type` | 项目类型 | `String` | `4` | `Y` | 已确认 | DD01：随机立减， CP01：抵金券；示例值：CP01 |
| `response.data.unionpay_response.coupon_info[].offst_amt` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].offst_amt` | 抵消交易金额 | `String` | `12` | `Y` | 已确认 | 不能为全0；示例值：1.00 |
| `response.data.unionpay_response.coupon_info[].id` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].id` | 项目编号 | `String` | `40` | `N` | 已确认 | 用于票券编号等，格式自定义；示例值：938434221 |
| `response.data.unionpay_response.coupon_info[].desc` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].desc` | 项目简称 | `String` | `40` | `N` | 已确认 | 优惠活动简称，可用于展示、打单等；示例值：中秋优惠促销 |
| `response.data.wx_user_id` | `response.data.wx_user_id` | `—（直接 JSON 路径）` | 微信用户唯一标识码 | `String` | `128` | `N` | 已确认 | 示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk= |
| `response.data.dy_response` | `response.data.dy_response` | `—（String(JSON) 容器）` | 抖音返回的响应报文 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.dy_response.sub_appid` | `response.data.dy_response` | `$.sub_appid` | 子商户应用ID | `String` | `32` | `N` | 已确认 | 在抖音开放平台申请的应用ID，全局唯一。此处请填写移动应用（APP）/网站应用（H5）类型的AppID |
| `response.data.dy_response.openid` | `response.data.dy_response` | `$.openid` | 用户标识 | `String` | `128` | `Y` | 已确认 | 用户在商户appid下的唯一标识；示例值：897ae8bd9f194107-9cb3-85f5672037de |
| `response.data.dy_response.sub_openid` | `response.data.dy_response` | `$.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：823ae8bd9f893402-9cb3-85f8794657ea |
| `response.data.dy_response.bank_type` | `response.data.dy_response` | `$.bank_type` | 付款银行 | `String` | `16` | `Y` | 已确认 | 银行类型，采用字符串类型的银行标识示例值：OTHERS |
| `response.data.dy_response.promotion_detail` | `response.data.dy_response` | `$.promotion_detail（String(JSON) 容器）` | 营销详情列表 | `String` | `—` | `N` | [需要官方确认]：长度 | 营销详情列表，使返回值为Json格式 |
| `response.data.dy_response.promotion_detail.coupon_id` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.coupon_id` | 券id | `String` | `32` | `N` | 已确认 | 券或者立减优惠id；示例值：2345234235 |
| `response.data.dy_response.promotion_detail.name` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `response.data.dy_response.promotion_detail.scope` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL: 全场代金券，SINGLE: 单品优惠；示例值：GLOBAL |
| `response.data.dy_response.promotion_detail.type` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.type` | 优惠类型 | `String` | `32` | `N` | 已确认 | CASH: 充值型代金券；NOCASH：免充值型代金券；示例值：CASH |
| `response.data.dy_response.promotion_detail.amount` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.amount` | 优惠券面额 | `String` | `12` | `Y` | 已确认 | 示例值：5.00 |
| `response.data.dy_response.promotion_detail.stock_id` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.stock_id` | 活动ID | `String` | `32` | `N` | 已确认 | 活动ID |
| `response.data.dy_response.promotion_detail.douyinpay_contribute` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.douyinpay_contribute` | 抖音出资 | `String` | `32` | `N` | 已确认 | 抖音出资，单位为元；示例值：10.00 |
| `response.data.dy_response.promotion_detail.merchant_contribute` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.merchant_contribute` | 商户出资 | `String` | `32` | `N` | 已确认 | 商户出资，单位为元；示例值：10.00 |
| `response.data.dy_response.promotion_detail.other_contribute` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.other_contribute` | 其他出资 | `String` | `32` | `N` | 已确认 | 其他出资，单位为元；示例值：20.00 |
| `response.data.dy_response.promotion_detail.currency` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.currency` | 优惠币种 | `String` | `32` | `N` | 已确认 | CNY：人民币，境内商户号仅支持人民币 |
| `response.data.dy_response.promotion_detail.goods_detail[]` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.goods_detail[]` | 单品列表 | `Array` | `—` | `N` | N/A：结构字段长度 | 单品信息，使用Json格式，是promotion_detail的元素 |
| `response.data.dy_response.promotion_detail.goods_detail[].goods_id` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.goods_detail[].goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `response.data.dy_response.promotion_detail.goods_detail[].quantity` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.goods_detail[].quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `response.data.dy_response.promotion_detail.goods_detail[].unit_price` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.goods_detail[].unit_price` | 商品单价 | `String` | `32` | `N` | 已确认 | 单位为:元。示例值：99.00 |
| `response.data.dy_response.promotion_detail.goods_detail[].discount_amount` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.goods_detail[].discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，单位为：元；示例值：20.00 |
| `response.data.dy_response.promotion_detail.goods_detail[].goods_remark` | `response.data.dy_response` | `$.promotion_detail => JSON decode => $.goods_detail[].goods_remark` | 商品备注 | `String` | `128` | `N` | 已确认 | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。；示例值：商品备注 |
| `response.data.is_div` | `response.data.is_div` | `—（直接 JSON 路径）` | 是否分账交易 | `String` | `1` | `Y` | 已确认 | Y: 分账交易, N: 非分账交易；示例值：N |
| `response.data.acct_split_bunch` | `response.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `2048` | `N` | 已确认 | 分账信息，jsonObject字符串 |
| `response.data.acct_split_bunch.acct_infos[]` | `response.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `2048` | `Y` | 已确认 | 分账明细 |
| `response.data.acct_split_bunch.acct_infos[].div_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.acct_split_bunch.acct_infos[].huifu_id` | `response.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `response.data.acct_split_bunch.acct_infos[].acct_date` | `response.data.acct_split_bunch` | `$.acct_infos[].acct_date` | 账务日期 | `String` | `8` | `N` | 已确认 | 示例值：20221023 |
| `response.data.is_delay_acct` | `response.data.is_delay_acct` | `—（直接 JSON 路径）` | 是否延时交易 | `String` | `1` | `Y` | 已确认 | Y: 延迟 N: 不延迟；示例值：N |
| `response.data.trans_fee_allowance_info` | `response.data.trans_fee_allowance_info` | `—（String(JSON) 容器）` | 手续费补贴信息 | `String` | `6000` | `N` | 已确认 | 手续费补贴信息，jsonObject字符串 |
| `response.data.trans_fee_allowance_info.receivable_fee_amt` | `response.data.trans_fee_allowance_info` | `$.receivable_fee_amt` | 商户应收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `response.data.trans_fee_allowance_info.actual_fee_amt` | `response.data.trans_fee_allowance_info` | `$.actual_fee_amt` | 商户实收手续费 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `response.data.trans_fee_allowance_info.allowance_fee_amt` | `response.data.trans_fee_allowance_info` | `$.allowance_fee_amt` | 补贴手续费 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `response.data.trans_fee_allowance_info.allowance_type` | `response.data.trans_fee_allowance_info` | `$.allowance_type` | 补贴类型 | `String` | `10` | `N` | 已确认 | 0：不补贴，为空默认；1：补贴；2：部分补贴；3：全额补贴(优惠后)；4：部分补贴(优惠后)；示例值：2 |
| `response.data.trans_fee_allowance_info.no_allowance_desc` | `response.data.trans_fee_allowance_info` | `$.no_allowance_desc` | 不补贴原因 | `String` | `128` | `N` | 已确认 | 补贴系统返回的不补贴原因；1:汇收款产品(HSK)银联二维码交易金额大于1000元不补贴；2:额度用完；3:不在有效期；4:活动不存在；5:手续费金额为0不补贴；6:顶格优惠；7:额度不足；8:手续费后补；9:未达到起始补贴金额；示例值：2 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos` | 手续费补贴活动详情 | `Object` | `—` | `N` | N/A：结构字段长度 | 补贴系统返回，斗拱原样返回 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.acct_id` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.acct_id` | 门店 | `String` | `64` | `N` | 已确认 | 示例值：sh002 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.merchant_group` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.merchant_group` | 商户号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.allowance_sys` | 补贴方 | `String` | `64` | `Y` | 已确认 | 1:银行 2:服务商 3:汇来米；示例值：1 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.allowance_sys_id` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.allowance_sys_id` | 补贴方ID | `String` | `64` | `Y` | 已确认 | 对应补贴方的id；示例值：[官网示例已脱敏] |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.is_delay_allowance` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.is_delay_allowance` | 补贴类型 | `String` | `2` | `Y` | 已确认 | 1:实补 2:后补,默认实补；示例值：1 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.market_id` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.market_id` | 自定义活动编号 | `String` | `64` | `Y` | 已确认 | 示例值：ISFE00232 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.market_name` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.market_name` | 自定义活动名称 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.market_desc` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.market_desc` | 自定义活动描述 | `String` | `64` | `N` | 已确认 | 示例值：新店开业大促 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.start_time` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.start_time` | 活动开始时间 | `String` | `8` | `Y` | 已确认 | yyyyMMdd；示例值：20220909 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.end_time` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.end_time` | 活动结束时间 | `String` | `8` | `Y` | 已确认 | yyyyMMdd；示例值：20220913 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.pos_debit_limit_amt` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.pos_debit_limit_amt` | pos借记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：2.00 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.pos_credit_limit_amt` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.pos_credit_limit_amt` | pos贷记卡补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：5.00 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.pos_limit_amt` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.pos_limit_amt` | pos补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：4.00 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.qr_limit_amt` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.qr_limit_amt` | 扫码补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：1.00 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.total_limit_amt` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.total_limit_amt` | 活动总补贴额度 | `String` | `16` | `Y` | 已确认 | 示例值：10.00 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.status` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.status` | 活动是否有效 | `String` | `4` | `Y` | 已确认 | 1:生效 0：失效；示例值：1 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.human_flag` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.human_flag` | 是否人工操作 | `String` | `4` | `Y` | 已确认 | N：自动 Y：人工；示例值：N |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.activity_id` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.activity_id` | 活动号 | `String` | `64` | `Y` | 已确认 | 示例值：223402342 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.activity_name` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.activity_name` | 活动描述 | `String` | `128` | `N` | 已确认 | 示例值：开业大促 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.create_by` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.create_by` | 创建人 | `String` | `32` | `Y` | 已确认 | 示例值：Lg[官网示例已脱敏] |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.create_time` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.create_time` | 创建时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 22:00:30 |
| `response.data.trans_fee_allowance_info.cur_allowance_config_infos.update_time` | `response.data.trans_fee_allowance_info` | `$.cur_allowance_config_infos.update_time` | 更新时间 | `String` | `32` | `Y` | 已确认 | 示例值：2022-04-14 23:00:30 |
| `response.data.quick_online_response` | `response.data.quick_online_response` | `—（[需要官方确认]：String 子表编码）` | 快捷网银响应 | `String` | `6000` | `N` | 已确认 | 新设计的域字段 |
| `response.data.quick_online_response.debit_flag` | `response.data.quick_online_response` | `—（[需要官方确认]：String 子表编码）` | 借贷记标识 | `String` | `1` | `N` | 已确认 | D-借记卡 C-信用卡 Z-借贷合一卡；示例值：C |
| `response.data.quick_online_response.user_huifu_id` | `response.data.quick_online_response` | `—（[需要官方确认]：String 子表编码）` | 用户号 | `String` | `32` | `N` | 已确认 | 汇付分配的用户号快捷支付时才有值；示例值：[官网示例已脱敏] |
| `response.data.quick_online_response.order_type` | `response.data.quick_online_response` | `—（[需要官方确认]：String 子表编码）` | 订单类型 | `String` | `1` | `N` | 已确认 | P-支付 R-充值 默认：P-支付；示例值：P |
| `response.data.quick_online_response.bank_id` | `response.data.quick_online_response` | `—（[需要官方确认]：String 子表编码）` | 银行代号 | `String` | `8` | `N` | 已确认 | 示例值：30200000 |
| `response.data.bank_extend_param` | `response.data.bank_extend_param` | `—（String(JSON) 容器）` | 银行扩展信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject格式；网银返回 |
| `response.data.bank_extend_param.gate_type` | `response.data.bank_extend_param` | `$.gate_type` | 网关支付类型 | `String` | `2` | `N` | 已确认 | 01: 个人网关02:企业网关；示例值：02 |
| `response.data.bank_extend_param.bank_id` | `response.data.bank_extend_param` | `$.bank_id` | 付款方银行号 | `String` | `32` | `N` | 已确认 | 示例值：01040000 |
| `response.data.bank_extend_param.pyer_acct_id` | `response.data.bank_extend_param` | `$.pyer_acct_id` | 付款方银行账户 | `String` | `1024` | `N` | 已确认 | B2B支付成功后可能返回密文；示例值：[官网示例已脱敏] |
| `response.data.bank_extend_param.pyer_acct_nm` | `response.data.bank_extend_param` | `$.pyer_acct_nm` | 付款方银行账户名 | `String` | `128` | `N` | 已确认 | 示例值：上海汇付支付有限公司 |
| `response.data.fee_formula_infos[]` | `response.data.fee_formula_infos` | `—（String(JSON Array) 容器）` | 手续费费率信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray格式；微信、支付宝、云闪付交易成功时返回手续费费率信息 |
| `response.data.fee_formula_infos[].fee_formula` | `response.data.fee_formula_infos` | `$[].fee_formula` | 手续费计算公式 | `String` | `512` | `Y` | 已确认 | 示例值：AMT*0.003 |
| `response.data.fee_formula_infos[].fee_type` | `response.data.fee_formula_infos` | `$[].fee_type` | 手续费类型 | `String` | `32` | `Y` | 已确认 | TRANS_FEE：交易手续费；ACCT_FEE：组合支付账户补贴手续费；示例值：ACCT_FEE |
| `response.data.fee_formula_infos[].huifu_id` | `response.data.fee_formula_infos` | `$[].huifu_id` | 商户号 | `String` | `32` | `N` | 已确认 | 补贴支付账户补贴时，补贴账户的huifuId；示例值：[官网示例已脱敏] |
| `response.data.fee_formula_infos[].fee_sign` | `response.data.fee_formula_infos` | `$[].fee_sign` | 手续费场景标识 | `String` | `32` | `N` | 已确认 | 商户业务开通配置时获取的手续费场景标识码，仅微信、支付宝交易时生效，不传时使用商户微信支付宝默认交易费率。；示例值：6850aad1e92f4244a74a42fcc1ad6360 |
| `response.data.devs_id` | `response.data.devs_id` | `—（直接 JSON 路径）` | 汇付机具号 | `String` | `32` | `Y` | 已确认 | 通过汇付报备的机具必传；示例值：[官网示例已脱敏] |
| `response.data.out_trans_id` | `response.data.out_trans_id` | `—（直接 JSON 路径）` | 交易单号 | `String` | `64` | `N` | 已确认 | 用户账单上的交易订单号，示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/partners/api/#/czsm/api_czsm_yhzd) |
| `response.data.request_ip` | `response.data.request_ip` | `—（直接 JSON 路径）` | 请求IP | `String` | `15` | `N` | 已确认 | 付款方IP,仅在支付成功后返回;示例：192.168.1.1 |
| `response.data.sub_orders_response[]` | `response.data.sub_orders_response` | `—（String(JSON Array) 容器）` | 子单信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray格式；子单信息，合单支付的订单返回该字段 |
| `response.data.sub_orders_response[].sub_req_seq_id` | `response.data.sub_orders_response` | `$[].sub_req_seq_id` | 子单请求流水号 | `String` | `128` | `N` | 已确认 | 交易时传入，原样返回；示例值：SUB[官网示例已脱敏] |
| `response.data.sub_orders_response[].sub_hf_seq_id` | `response.data.sub_orders_response` | `$[].sub_hf_seq_id` | 子单全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00470topo1A221019132207P068ac1362af00001 |
| `response.data.sub_orders_response[].sub_huifu_id` | `response.data.sub_orders_response` | `$[].sub_huifu_id` | 子单商户号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.sub_orders_response[].sub_acct_id` | `response.data.sub_orders_response` | `$[].sub_acct_id` | 子单账户号 | `String` | `9` | `N` | 已确认 | 示例值：A123456 |
| `response.data.sub_orders_response[].sub_trans_amt` | `response.data.sub_orders_response` | `$[].sub_trans_amt` | 子单交易金额 | `String` | `14` | `N` | 已确认 | 位元；示例值：1.00 |
| `response.data.sub_orders_response[].sub_settlement_amt` | `response.data.sub_orders_response` | `$[].sub_settlement_amt` | 子单结算金额 | `String` | `14` | `N` | 已确认 | 位元；示例值：1.00 |
| `response.data.sub_orders_response[].sub_remark` | `response.data.sub_orders_response` | `$[].sub_remark` | 子单备注信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 原样返回；示例值：子单备注 |
| `response.data.sub_orders_response[].acct_date` | `response.data.sub_orders_response` | `$[].acct_date` | 入账时间 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20091225 |
| `response.data.sub_orders_response[].unconfirm_amt` | `response.data.sub_orders_response` | `$[].unconfirm_amt` | 待确认总金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.sub_orders_response[].confirmed_amt` | `response.data.sub_orders_response` | `$[].confirmed_amt` | 已确认总金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.sub_orders_response[].delay_acct_flag` | `response.data.sub_orders_response` | `$[].delay_acct_flag` | 是否延时交易 | `String` | `1` | `N` | 已确认 | Y：延迟， N：不延迟；示例值：Y |
| `response.data.sub_orders_response[].acct_stat` | `response.data.sub_orders_response` | `$[].acct_stat` | 账务状态 | `String` | `1` | `N` | 已确认 | "I：初始"; "P:处理中"; "S:成功"; "F:失败。示例值：S； 返回“I：初始”状态时，请联系客服确认订单问题 |
| `response.data.sub_orders_response[].div_flag` | `response.data.sub_orders_response` | `$[].div_flag` | 是否分账交易 | `String` | `1` | `N` | 已确认 | Y：分账交易，N：非分账交易；示例值：Y |
| `response.data.sub_orders_response[].acct_split_bunch` | `response.data.sub_orders_response` | `$[].acct_split_bunch（String(JSON) 容器）` | 分账对象 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串 |
| `response.data.sub_orders_response[].acct_split_bunch.acct_infos[]` | `response.data.sub_orders_response` | `$[].acct_split_bunch.acct_infos（String(JSON Array) 容器）` | 分账明细 | `String` | `—` | `Y` | [需要官方确认]：长度 | jsonArray分账明细 |
| `response.data.sub_orders_response[].acct_split_bunch.acct_infos[].huifu_id` | `response.data.sub_orders_response` | `$[].acct_split_bunch.acct_infos => JSON decode => $[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `response.data.sub_orders_response[].acct_split_bunch.acct_infos[].acct_id` | `response.data.sub_orders_response` | `$[].acct_split_bunch.acct_infos => JSON decode => $[].acct_id` | 分账接收方子账户 | `String` | `9` | `N` | 已确认 | 示例值：F00598600/font> |
| `response.data.sub_orders_response[].acct_split_bunch.acct_infos[].div_amt` | `response.data.sub_orders_response` | `$[].acct_split_bunch.acct_infos => JSON decode => $[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 ，最低传入0.01 |
| `response.data.sub_orders_response[].acct_split_bunch.is_clean_split` | `response.data.sub_orders_response` | `$[].acct_split_bunch => JSON decode => $.is_clean_split` | 是否净值分账 | `String` | `1` | `N` | 已确认 | Y:使用净值分账，仅在percentage_flag=Y时起作用；示例值：Y |
| `response.data.sub_orders_response[].fee_info` | `response.data.sub_orders_response` | `$[].fee_info => [需要官方确认]：String 子表编码` | 交易手续费信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 交易手续费信息 |
| `response.data.sub_orders_response[].fee_info.fee_formula` | `response.data.sub_orders_response` | `$[].fee_info => [需要官方确认]：String 子表编码` | 手续费计算公式 | `String` | `512` | `N` | 已确认 | 示例值：AMT\*0.003 |
| `response.data.sub_orders_response[].fee_info.fee_huifu_id` | `response.data.sub_orders_response` | `$[].fee_info => [需要官方确认]：String 子表编码` | 手续费扣款商户号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.sub_orders_response[].fee_info.fee_acct_id` | `response.data.sub_orders_response` | `$[].fee_info => [需要官方确认]：String 子表编码` | 手续费扣款账户号 | `String` | `9` | `N` | 已确认 | 示例值：F00598600 |
| `response.data.sub_orders_response[].fee_info.fee_flag` | `response.data.sub_orders_response` | `$[].fee_info => [需要官方确认]：String 子表编码` | 手续费扣款标志 | `Integer` | `1` | `N` | 已确认 | 1: 外扣，2: 内扣；示例值：2 |
| `response.data.sub_orders_response[].fee_info.fee_rec_type` | `response.data.sub_orders_response` | `$[].fee_info => [需要官方确认]：String 子表编码` | 手续费扣取方式 | `Integer` | `1` | `N` | 已确认 | 1: 实收，2: 后收；示例值：1 |
| `response.data.sub_orders_response[].fee_info.fee_amount` | `response.data.sub_orders_response` | `$[].fee_info => [需要官方确认]：String 子表编码` | 手续费金额 | `String` | `16` | `N` | 已确认 | 单位元，保留小数点后两位。根据手续费公式计算的手续费小于0.01时，取0.01。示例值：1.00 |
| `response.data.sub_orders_response[].split_fee_info` | `response.data.sub_orders_response` | `$[].split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 分账手续费信息 |
| `response.data.sub_orders_response[].split_fee_info.total_split_fee_amt` | `response.data.sub_orders_response` | `$[].split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费总金额(元) | `String` | `14` | `N` | 已确认 | 示例值：0.10 |
| `response.data.sub_orders_response[].split_fee_info.split_fee_flag` | `response.data.sub_orders_response` | `$[].split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费扣款标志 | `Integer` | `1` | `Y` | 已确认 | 1: 外扣 2: 内扣；示例值：2 |
| `response.data.sub_orders_response[].split_fee_info.split_fee_details` | `response.data.sub_orders_response` | `$[].split_fee_info.split_fee_details => [需要官方确认]：String 子表编码` | 分账手续费信息 | `String` | `—` | `Y` | [需要官方确认]：长度 | 分账手续费信息 |
| `response.data.sub_orders_response[].split_fee_info.split_fee_details.split_fee_amt` | `response.data.sub_orders_response` | `$[].split_fee_info.split_fee_details => [需要官方确认]：String 子表编码` | 分账手续费金额(元) | `String` | `14` | `Y` | 已确认 | 示例值：0.10 |
| `response.data.sub_orders_response[].split_fee_info.split_fee_details.split_fee_huifu_id` | `response.data.sub_orders_response` | `$[].split_fee_info.split_fee_details => [需要官方确认]：String 子表编码` | 分账手续费承担方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.sub_orders_response[].split_fee_info.split_fee_details.split_fee_acct_id` | `response.data.sub_orders_response` | `$[].split_fee_info.split_fee_details => [需要官方确认]：String 子表编码` | 分账手续费承担方账号 | `String` | `9` | `N` | 已确认 | 示例值：F00598600 |
| `response.data.sub_orders_response[].fund_freeze_stat` | `response.data.sub_orders_response` | `$[].fund_freeze_stat` | 资金冻结状态 | `String` | `16` | `N` | 已确认 | FREEZE：冻结；UNFREEZE：解冻；示例值：UNFREEZE |
| `response.data.sub_orders_response[].freeze_time` | `response.data.sub_orders_response` | `$[].freeze_time` | 冻结时间 | `String` | `14` | `N` | 已确认 | 格式为yyyyMMddHHMMSS，示例值：20091225091010 |
| `response.data.sub_orders_response[].unfreeze_amt` | `response.data.sub_orders_response` | `$[].unfreeze_amt` | 解冻金额 | `String` | `14` | `N` | 已确认 | 单元：元。示例值：1.23 |
| `response.data.sub_orders_response[].unfreeze_time` | `response.data.sub_orders_response` | `$[].unfreeze_time` | 解冻时间 | `String` | `14` | `N` | 已确认 | 格式为yyyyMMddHHMMSS，示例值：20091225091010 |

## 托管交易退款

- 原始地址：<https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hostingtk.md>
- SHA-256：`fe45dca45e8fce7a5caa19eb54196c51715546675abbaa1081984eb768e332cb`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20220925 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 开户后自动生成；示例值：[官网示例已脱敏] |
| `request.data.ord_amt` | `request.data.ord_amt` | `—（直接 JSON 路径）` | 申请退款金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位；示例值：1.00，最低传入0.01；注意：如果是原交易是延时交易，退款金额必须小于等于待确认金额 |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `Y` | 已确认 | 格式：yyyyMMdd；示例值：20220925 |
| `request.data.org_hf_seq_id` | `request.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原交易全局流水号 | `String` | `128` | `N` | 已确认 | org_hf_seq_id，org_party_order_id，org_req_seq_id三选一；拆单支付场景下，org_hf_seq_id，org_party_order_id二选一；示例值：0030default220825182711P099ac1f343f00000 |
| `request.data.org_party_order_id` | `request.data.org_party_order_id` | `—（直接 JSON 路径）` | 原交易微信支付宝的商户单号 | `String` | `64` | `N` | 已确认 | 扫码交易退款字段；org_hf_seq_id，org_party_order_id，org_req_seq_id三选一；拆单支付场景下，org_hf_seq_id，org_party_order_id二选一；示例值：[官网示例已脱敏] |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `N` | 已确认 | org_hf_seq_id，org_party_order_id，org_req_seq_id三选一；示例值：[官网示例已脱敏] |
| `request.data.acct_split_bunch` | `request.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `2048` | `N` | 已确认 | 分账信息，jsonObject字符串 |
| `request.data.acct_split_bunch.acct_infos[]` | `request.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `2048` | `N` | 已确认 | 分账明细 |
| `request.data.acct_split_bunch.acct_infos[].div_amt` | `request.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 ，最低传入0.01 |
| `request.data.acct_split_bunch.acct_infos[].huifu_id` | `request.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `request.data.acct_split_bunch.acct_infos[].part_loan_amt` | `request.data.acct_split_bunch` | `$.acct_infos[].part_loan_amt` | 垫资金额 | `String` | `12` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01；注：若由第三方全额垫资，则不传该字段 |
| `request.data.remark` | `request.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `84` | `N` | 已确认 | 原样返回；示例值：备注 |
| `request.data.loan_flag` | `request.data.loan_flag` | `—（直接 JSON 路径）` | 是否垫资退款 | `String` | `2` | `N` | 已确认 | Y 是垫资出款， N 是普通出款，为空默认N；示例值： N；注意：延时交易退款在【交易确认退款】接口中设置loan_flag为垫资，；本接口不可再次设置垫资。 |
| `request.data.loan_undertaker` | `request.data.loan_undertaker` | `—（直接 JSON 路径）` | 垫资承担者 | `String` | `32` | `N` | 已确认 | 垫资方的huifu_id；示例值：[官网示例已脱敏]；为空则各自承担。不为空走第三方垫资，目前支持商户垫资 |
| `request.data.loan_acct_type` | `request.data.loan_acct_type` | `—（直接 JSON 路径）` | 垫资账户类型 | `String` | `2` | `N` | 已确认 | 01:基本户, 05: 充值户, 默认充值户；示例值：01 |
| `request.data.risk_check_data` | `request.data.risk_check_data` | `—（String(JSON) 容器）` | 安全信息 | `String` | `2048` | `C` | 已确认 | 线上交易退款必填，参见线上退款接口；jsonObject字符串 |
| `request.data.risk_check_data.ip_addr` | `request.data.risk_check_data` | `$.ip_addr` | ip地址 | `String` | `32` | `N` | 已确认 | IP地址、经纬度、基站地址最少要送其中一项；示例值：172.28.52.52 |
| `request.data.risk_check_data.base_station` | `request.data.risk_check_data` | `$.base_station` | 基站地址 | `String` | `64` | `N` | 已确认 | 【mcc】+【mnc】+【location_cd】+【lbs_num】；- mcc:移动国家代码，460代表中国；3位长；- mnc：移动网络号码；2位长；- location_cd：位置区域码，16进制，5位长；- lbs_num：基站编号，16进制，5位长；- 注意若位数不足用空格补足；示例值：460001039217563，其中460（mcc)， 00(mnc)，10392(location_cd)， 17563(lbs_num) |
| `request.data.risk_check_data.latitude` | `request.data.risk_check_data` | `$.latitude` | 纬度 | `String` | `20` | `N` | 已确认 | 格式：+表示北纬，-表示南纬。纬度整数位不超过2位，小数位不超过6位。示例值：+37.12；IP地址、经纬度、基站地址最少要送其中一项 |
| `request.data.risk_check_data.longitude` | `request.data.risk_check_data` | `$.longitude` | 经度 | `String` | `20` | `N` | 已确认 | 格式：+表示东经，-表示西经；经度整数位不超过3位，小数位不超过5位；示例值：-121.213；IP地址、经纬度、基站地址最少要送其中一项 |
| `request.data.terminal_device_data` | `request.data.terminal_device_data` | `—（String(JSON) 容器）` | 设备信息 | `String` | `2048` | `C` | 已确认 | 线上交易退款必填，参见线上退款接口；jsonObject字符串 |
| `request.data.terminal_device_data.device_type` | `request.data.terminal_device_data` | `$.device_type` | 设备类型 | `String` | `2` | `N` | 已确认 | 1: 手机，2: 平板，3: 手表，4: PC；示例值：1 |
| `request.data.terminal_device_data.device_ip` | `request.data.terminal_device_data` | `$.device_ip` | 交易设备IP | `String` | `64` | `N` | 已确认 | 绑卡设备所在的公网IP，可用于定位所属地区，不是wifi连接时的局域网IP。；ABCD:EF01:2345:6789:ABCD:EF01:2345:6789（IPv6）；目前暂传IPv4格式。示例值：10.10.0.1（IPv4） |
| `request.data.terminal_device_data.device_mac` | `request.data.terminal_device_data` | `$.device_mac` | 交易设备MAC | `String` | `64` | `N` | 已确认 | 示例值：F0E1D2C3B4A5 |
| `request.data.terminal_device_data.device_gps` | `request.data.terminal_device_data` | `$.device_gps` | 交易设备GPS | `String` | `64` | `N` | 已确认 | 示例值：20.346790,-4.654321 |
| `request.data.terminal_device_data.device_imei` | `request.data.terminal_device_data` | `$.device_imei` | 交易设备IMEI | `String` | `64` | `N` | 已确认 | 移动终端设备的唯一标识；示例值：460030912121001 |
| `request.data.terminal_device_data.device_imsi` | `request.data.terminal_device_data` | `$.device_imsi` | 交易设备IMSI | `String` | `64` | `N` | 已确认 | 示例值：460030912121001 |
| `request.data.terminal_device_data.device_icc_id` | `request.data.terminal_device_data` | `$.device_icc_id` | 交易设备ICCID | `String` | `64` | `N` | 已确认 | 示例值：898600680113F0123014 |
| `request.data.terminal_device_data.device_wifi_mac` | `request.data.terminal_device_data` | `$.device_wifi_mac` | 交易设备WIFIMAC | `String` | `64` | `N` | 已确认 | 示例值：968778695A4B |
| `request.data.notify_url` | `request.data.notify_url` | `—（直接 JSON 路径）` | 异步通知地址 | `String` | `512` | `N` | 已确认 | 示例值： http://service.example.com/to/path |
| `request.data.bank_info_data` | `request.data.bank_info_data` | `—（String(JSON) 容器）` | 大额转账支付账户信息数据 | `String` | `1024` | `C` | 已确认 | jsonObject格式；银行大额转账支付交易退款申请时必填 |
| `request.data.bank_info_data.province` | `request.data.bank_info_data` | `$.province` | 省份 | `String` | `4` | `C` | 已确认 | 付款方为对公账户时必填，参见省市地区码；示例值：0013 |
| `request.data.bank_info_data.area` | `request.data.bank_info_data` | `$.area` | 地区 | `String` | `4` | `C` | 已确认 | 付款方为对公账户时必填，参见省市地区码；示例值：1301 |
| `request.data.bank_info_data.bank_code` | `request.data.bank_info_data` | `$.bank_code` | 银行编号 | `String` | `8` | `C` | 已确认 | 付款方为对公账户时必填，参考：银行编码； 示例值：01040000 |
| `request.data.bank_info_data.correspondent_code` | `request.data.bank_info_data` | `$.correspondent_code` | 联行号 | `String` | `30` | `C` | 已确认 | 付款方为对公账户时必填，参见：银行支行编码； 示例值：102290026507 |
| `request.data.bank_info_data.card_acct_type` | `request.data.bank_info_data` | `$.card_acct_type` | 付款方账户类型 | `String` | `1` | `N` | 已确认 | 对公:E，对私:P；默认：P，示例值：P |
| `request.data.dy_data` | `request.data.dy_data` | `—（String(JSON) 容器）` | 抖音拓展参数集合 | `String` | `2048` | `N` | 已确认 | jsonObject字符串 |
| `request.data.dy_data.refund_desc` | `request.data.dy_data` | `$.refund_desc` | 退款原因 | `String` | `200` | `N` | 已确认 | 会在下发给用户的退款消息中体现退款原因 |
| `request.data.sub_orders_request[]` | `request.data.sub_orders_request` | `—（String(JSON Array) 容器）` | 子单退款信息列表 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray字符串，合单支付的订单该字段必填 |
| `request.data.sub_orders_request[].sub_req_date` | `request.data.sub_orders_request` | `$[].sub_req_date` | 子单请求日期 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20220925 |
| `request.data.sub_orders_request[].sub_req_seq_id` | `request.data.sub_orders_request` | `$[].sub_req_seq_id` | 子单请求流水号 | `String` | `128` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `request.data.sub_orders_request[].sub_huifu_id` | `request.data.sub_orders_request` | `$[].sub_huifu_id` | 子单商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.sub_orders_request[].sub_ord_amt` | `request.data.sub_orders_request` | `$[].sub_ord_amt` | 子单申请退款金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位；示例值：1.00，最低传入0.01；**注意：如果原交易是延时交易，退款金额必须小于等于待确认金额** |
| `request.data.sub_orders_request[].org_sub_req_date` | `request.data.sub_orders_request` | `$[].org_sub_req_date` | 原子单交易请求日期 | `String` | `8` | `Y` | 已确认 | 格式：yyyyMMdd；示例值：20220925 |
| `request.data.sub_orders_request[].org_sub_hf_seq_id` | `request.data.sub_orders_request` | `$[].org_sub_hf_seq_id` | 原子单交易全局流水号 | `String` | `128` | `N` | 已确认 | org_sub_hf_seq_id，org_sub_req_seq_id二选一；示例值：0030default220825182711P099ac1f343f00000 |
| `request.data.sub_orders_request[].org_sub_req_seq_id` | `request.data.sub_orders_request` | `$[].org_sub_req_seq_id` | 原子单交易请求流水号 | `String` | `128` | `N` | 已确认 | org_sub_hf_seq_id，org_sub_req_seq_id二选一；示例值：[官网示例已脱敏] |
| `request.data.sub_orders_request[].acct_split_bunch` | `request.data.sub_orders_request` | `$[].acct_split_bunch（String(JSON) 容器）` | 分账对象 | `String` | `2048` | `N` | 已确认 | 分账信息，jsonObject字符串 |
| `request.data.sub_orders_request[].acct_split_bunch.acct_infos` | `request.data.sub_orders_request` | `$[].acct_split_bunch.acct_infos => [需要官方确认]：String 子表编码` | 分账信息列表 | `String` | `2048` | `N` | 已确认 | 分账明细 |
| `request.data.sub_orders_request[].acct_split_bunch.acct_infos.div_amt` | `request.data.sub_orders_request` | `$[].acct_split_bunch.acct_infos => [需要官方确认]：String 子表编码` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `request.data.sub_orders_request[].acct_split_bunch.acct_infos.huifu_id` | `request.data.sub_orders_request` | `$[].acct_split_bunch.acct_infos => [需要官方确认]：String 子表编码` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `request.data.sub_orders_request[].sub_remark` | `request.data.sub_orders_request` | `$[].sub_remark` | 子单备注 | `String` | `84` | `N` | 已确认 | 原样返回；示例值：子单备注 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tk?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81) ；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tk?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)；示例值：交易成功 |
| `response.data.product_id` | `response.data.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 交易时传入，原样返回；示例值：YYZY |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 交易时传入，原样返回；示例值：rQ[官网示例已脱敏] |
| `response.data.hf_seq_id` | `response.data.hf_seq_id` | `—（直接 JSON 路径）` | 全局流水号 | `String` | `128` | `N` | 已确认 | 扫码交易返回；示例值：0030default220825182711P099ac1f343f00000 |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `N` | 已确认 | 示例值：rQ[官网示例已脱敏] |
| `response.data.org_hf_seq_id` | `response.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原交易全局流水号 | `String` | `128` | `N` | 已确认 | 线上交易返回；示例值：0030default220825182711P099ac1f343f00000 |
| `response.data.trans_time` | `response.data.trans_time` | `—（直接 JSON 路径）` | 退款交易发生时间 | `String` | `14` | `N` | 已确认 | 扫码交易返回；示例值：20091225091010 |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `1` | `N` | 已确认 | P：处理中、S：成功、F：失败；示例值：S；示例值：S |
| `response.data.ord_amt` | `response.data.ord_amt` | `—（直接 JSON 路径）` | 退款金额（元） | `String` | `14` | `Y` | 已确认 | 需保留小数点后两位；示例值：1.00，最低传入0.01 |
| `response.data.actual_ref_amt` | `response.data.actual_ref_amt` | `—（直接 JSON 路径）` | 实际退款金额（元） | `String` | `14` | `N` | 已确认 | 扫码交易返回；示例值：100.00 |
| `response.data.acct_split_bunch` | `response.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账信息 | `String` | `2048` | `N` | 已确认 | 分账信息，jsonObject字符串 |
| `response.data.acct_split_bunch.acct_infos[]` | `response.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `2048` | `N` | 已确认 | 分账明细 |
| `response.data.acct_split_bunch.acct_infos[].div_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 ，最低传入0.01 |
| `response.data.acct_split_bunch.acct_infos[].huifu_id` | `response.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `response.data.acct_split_bunch.fee_amt` | `response.data.acct_split_bunch` | `$.fee_amt` | 退款返还手续费 | `String` | `14` | `N` | 已确认 | 单位元，保留小数点后两位，示例值：1.00 |
| `response.data.unionpay_response` | `response.data.unionpay_response` | `—（String(JSON) 容器）` | 银联返回的响应报文 | `String` | `6000` | `N` | 已确认 | JsonObject字符串格式；扫码交易返回，参见扫码交易退款接口 |
| `response.data.unionpay_response.coupon_info[]` | `response.data.unionpay_response` | `$.coupon_info（String(JSON Array) 容器）` | 银联优惠信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 银联使用优惠活动时出现，jsonArray格式 |
| `response.data.unionpay_response.coupon_info[].addnInfo` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].addnInfo` | 附加信息 | `String` | `100` | `N` | 已确认 | 内容自定义；示例值：附加信息 |
| `response.data.unionpay_response.coupon_info[].spnsrId` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].spnsrId` | 出资方 | `String` | `20` | `Y` | 已确认 | 00010000：银联出资；付款方作为出资方：填写8位付款方机构代码；商户作为出资方：填写15位商户代码；示例值：00010000 |
| `response.data.unionpay_response.coupon_info[].type` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].type` | 项目类型 | `String` | `4` | `Y` | 已确认 | DD01：随机立减， CP01：抵金券；示例值：DD01 |
| `response.data.unionpay_response.coupon_info[].offstAmt` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].offstAmt` | 抵消交易金额 | `String` | `14` | `Y` | 已确认 | 不能为全0；单位元；示例值：1.00 |
| `response.data.unionpay_response.coupon_info[].id` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].id` | 项目编号 | `String` | `40` | `N` | 已确认 | 用于票券编号等，格式自定义；示例值：938434221 |
| `response.data.unionpay_response.coupon_info[].desc` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].desc` | 项目简称 | `String` | `40` | `N` | 已确认 | 优惠活动简称，可用于展示、打单等；示例值：中秋优惠促销 |
| `response.data.dy_response` | `response.data.dy_response` | `—（String(JSON) 容器）` | 抖音返回的响应报文 | `String` | `6000` | `N` | 已确认 | jsonObject字符串 |
| `response.data.dy_response.org_out_trans_id` | `response.data.dy_response` | `$.org_out_trans_id` | 抖音原交易订单号 | `String` | `32` | `N` | 已确认 | 示例值：20201030189770 |
| `response.data.dy_response.out_trans_id` | `response.data.dy_response` | `$.out_trans_id` | 抖音退款单号 | `String` | `32` | `N` | 已确认 | 示例值：6545342375 |
| `response.data.dy_response.payer_refund` | `response.data.dy_response` | `$.payer_refund` | 用户退款金额 | `String` | `12` | `N` | 已确认 | 退款给用户的金额，不包含所有优惠券金额 ，单位:元；示例值：1.00 |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `84` | `N` | 已确认 | 原样返回；示例值：备注 |
| `response.data.bank_code` | `response.data.bank_code` | `—（直接 JSON 路径）` | 通道返回码 | `String` | `64` | `N` | 已确认 | 示例值：01020000 |
| `response.data.bank_message` | `response.data.bank_message` | `—（直接 JSON 路径）` | 通道返回描述 | `String` | `256` | `N` | 已确认 | 示例值：SUCCESS |
| `response.data.fee_amt` | `response.data.fee_amt` | `—（直接 JSON 路径）` | 退款返还手续费 | `String` | `14` | `N` | 已确认 | 线上交易返回；示例值：1.00 |

### 退款异步 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.data.resp_code` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tk?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81) ；示例值：00000000 |
| `async.data.resp_desc` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tk?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)；示例值：交易成功 |
| `async.data.huifu_id` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.data.mer_name` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 商户名称 | `String` | `128` | `Y` | 已确认 | 线上交易返回；示例值：上海汇付支付服务公司 |
| `async.data.req_date` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `async.data.req_seq_id` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：rQ[官网示例已脱敏] |
| `async.data.hf_seq_id` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：0030default220825182711P099ac1f343f00000 |
| `async.data.org_req_date` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 原交易请求日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `async.data.org_req_seq_id` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 原交易请求流水号 | `String` | `128` | `N` | 已确认 | 示例值：rQ[官网示例已脱敏] |
| `async.data.org_ord_amt` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 原交易订单金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.data.org_fee_amt` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 原交易手续费 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.data.trans_date` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 退款交易发生日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `async.data.trans_time` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 退款交易发生时间 | `String` | `6` | `N` | 已确认 | 格式：HHMMSS，示例值：091010；9点10分10秒 |
| `async.data.trans_finish_time` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 退款完成时间 | `String` | `14` | `N` | 已确认 | 格式yyyyMMddHHmmss；示例值：20091225091010 |
| `async.data.trans_type` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 交易类型 | `String` | `40` | `Y` | 已确认 | TRANS_REFUND：交易退款；目前仅该一个枚举值；示例值：TRANS_REFUND |
| `async.data.trans_stat` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 交易状态 | `String` | `1` | `N` | 已确认 | P：处理中、S：成功、F：失败；示例值：S |
| `async.data.ord_amt` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 退款金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.data.actual_ref_amt` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 实际退款金额 | `String` | `14` | `N` | 已确认 | 扫码交易返回；示例值：111.00 |
| `async.data.total_ref_amt` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 原交易累计退款金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `async.data.total_ref_fee_amt` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 原交易累计退款手续费金额 | `String` | `14` | `Y` | 已确认 | 单位元，示例值：1.00；注意：退还手续费规则参见[说明文档](https://paas.huifu.com/open/doc/api/#/api_tksxfsm) |
| `async.data.ref_cut` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 累计退款次数 | `String` | `14` | `Y` | 已确认 | 示例值：1 |
| `async.data.acct_split_bunch` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 分账信息 | `String` | `4000` | `Y` | 已确认 | 与同步返参的相同 |
| `async.data.acct_split_bunch.acct_infos[]` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 分账明细 | `Array` | `2048` | `N` | 已确认 | 分账明细 |
| `async.data.acct_split_bunch.acct_infos[].div_amt` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 ，最低传入0.01 |
| `async.data.acct_split_bunch.acct_infos[].huifu_id` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `async.data.acct_split_bunch.fee_amt` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 退款返还手续费 | `String` | `14` | `N` | 已确认 | 单位元，保留小数点后两位，示例值：1.00 |
| `async.data.split_fee_info` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 分账手续费信息 | `String` | `2048` | `N` | 已确认 | 线上交易返回 |
| `async.data.split_fee_info.split_fee_flag` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 分账手续费扣款标志 | `String` | `1` | `Y` | 已确认 | 1:外扣 2:内扣；示例值：1 |
| `async.data.split_fee_info.total_split_fee_amt` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 总分账手续费金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `async.data.split_fee_info.split_fee_details[]` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 分账手续费明细 | `Array` | `2048` | `Y` | 已确认 | 分账手续费明细 |
| `async.data.split_fee_info.split_fee_details[].split_fee_amt` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 分账手续费金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `async.data.split_fee_info.split_fee_details[].split_fee_huifu_id` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 分账手续费承担方商户号 | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `async.data.split_fee_info.split_fee_details[].split_fee_acct_id` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 分账手续费承担方账号 | `String` | `16` | `N` | 已确认 | 示例值：F00598600 |
| `async.data.party_order_id` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 微信支付宝的商户单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；参见[用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `async.data.fee_amt` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 退款返还手续费 | `String` | `14` | `N` | 已确认 | 线上交易返回 |
| `async.data.remark` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 备注 | `String` | `84` | `N` | 已确认 | 原样返回；示例值：备注 |
| `async.data.bank_code` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 通道返回码 | `String` | `64` | `N` | 已确认 | 示例值：01020000 |
| `async.data.bank_message` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 通道返回描述 | `String` | `256` | `N` | 已确认 | 示例值：SUCCESS |
| `async.data.unionpay_response` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 银联返回的响应报文 | `String` | `6000` | `N` | 已确认 | JsonObject格式 |
| `async.data.unionpay_response.coupon_info[]` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 银联优惠信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 银联使用优惠活动时出现，jsonArray格式 |
| `async.data.unionpay_response.coupon_info[].addnInfo` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 附加信息 | `String` | `100` | `N` | 已确认 | 内容自定义；示例值：附加信息 |
| `async.data.unionpay_response.coupon_info[].spnsrId` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 出资方 | `String` | `20` | `Y` | 已确认 | 00010000：银联出资；付款方作为出资方：填写8位付款方机构代码；商户作为出资方：填写15位商户代码；示例值：00010000 |
| `async.data.unionpay_response.coupon_info[].type` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 项目类型 | `String` | `4` | `Y` | 已确认 | DD01：随机立减， CP01：抵金券；示例值：DD01 |
| `async.data.unionpay_response.coupon_info[].offstAmt` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 抵消交易金额 | `String` | `14` | `Y` | 已确认 | 不能为全0；单位元；示例值：1.00 |
| `async.data.unionpay_response.coupon_info[].id` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 项目编号 | `String` | `40` | `N` | 已确认 | 用于票券编号等，格式自定义；示例值：938434221 |
| `async.data.unionpay_response.coupon_info[].desc` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 项目简称 | `String` | `40` | `N` | 已确认 | 优惠活动简称，可用于展示、打单等；示例值：中秋优惠促销 |
| `async.data.dy_response` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 抖音返回的响应报文 | `String` | `6000` | `N` | 已确认 | jsonObject字符串 |
| `async.data.dy_response.org_out_trans_id` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 抖音原交易订单号 | `String` | `32` | `N` | 已确认 | 示例值：20201030189770 |
| `async.data.dy_response.out_trans_id` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 抖音退款单号 | `String` | `32` | `N` | 已确认 | 示例值：6545342375 |
| `async.data.dy_response.payer_refund` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 用户退款金额 | `String` | `12` | `N` | 已确认 | 退款给用户的金额，不包含所有优惠券金额 ，单位:元；示例值：1.00 |
| `async.data.bank_id` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 银行编号 | `String` | `32` | `N` | 已确认 | 线上交易返回；示例值： |
| `async.data.bank_name` | `async.data` | `—（[需要官方确认]：外层 data 的 JSON/String(JSON) 编码）` | 银行名称 | `String` | `128` | `N` | 已确认 | 线上交易返回；示例值： |

## 托管交易退款查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hostingtkcx.md>
- SHA-256：`4b78ba8567f606a870076d9f637fe064b21743f8139382c7a06e9016e5449f0c`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20221023 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 开户自动生成；示例值：[官网示例已脱敏] |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 退款请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20221023 |
| `request.data.org_hf_seq_id` | `request.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 退款全局流水号 | `String` | `128` | `C` | 已确认 | 退款请求流水号/退款全局流水号二选一不能都为空；示例值：0030default220825182711P099ac1f343f00000 |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 退款请求流水号 | `String` | `128` | `C` | 已确认 | 退款请求流水号/退款全局流水号二选一不能都为空；示例值：[官网示例已脱敏] |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tkcx?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/open/doc/api/#/smzf/api_qrpay_tkcx?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)；示例值：操作成功 |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20220925 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.org_hf_seq_id` | `response.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 退款全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：0030default220825182711P099ac1f343f00000 |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 退款请求日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 退款请求流水号 | `String` | `128` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.ord_amt` | `response.data.ord_amt` | `—（直接 JSON 路径）` | 退款金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.actual_ref_amt` | `response.data.actual_ref_amt` | `—（直接 JSON 路径）` | 实际退款金额 | `String` | `14` | `N` | 已确认 | 扫码退款返回，示例值：1.00 |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `1` | `N` | 已确认 | P：处理中；S：成功；F：失败；I: 初始；初始状态很罕见，请联系汇付技术人员处理；示例值：S |
| `response.data.bank_code` | `response.data.bank_code` | `—（直接 JSON 路径）` | 通道返回码 | `String` | `64` | `N` | 已确认 | 示例值：01020000 |
| `response.data.bank_message` | `response.data.bank_message` | `—（直接 JSON 路径）` | 通道返回描述 | `String` | `256` | `N` | 已确认 | 示例值：SUCCESS |
| `response.data.fee_amt` | `response.data.fee_amt` | `—（直接 JSON 路径）` | 退款返还手续费 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.acct_split_bunch` | `response.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `—` | `N` | [需要官方确认]：长度 | 分账对象，jsonObject字符串 |
| `response.data.acct_split_bunch.acct_infos[]` | `response.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `2048` | `Y` | 已确认 | 分账明细 |
| `response.data.acct_split_bunch.acct_infos[].div_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00；最低传入0.01 |
| `response.data.acct_split_bunch.acct_infos[].huifu_id` | `response.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.acct_split_bunch.acct_infos[].acct_id` | `response.data.acct_split_bunch` | `$.acct_infos[].acct_id` | 账户号 | `String` | `16` | `N` | 已确认 | 示例值：F00598600 |
| `response.data.acct_split_bunch.acct_infos[].part_loan_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].part_loan_amt` | 垫资金额 | `String` | `12` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01；注：若由第三方全额垫资，则不传该字段 |
| `response.data.split_fee_info` | `response.data.split_fee_info` | `—（String(JSON) 容器）` | 分账手续费信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 分账手续费信息，jsonObject字符串 |
| `response.data.split_fee_info.total_split_fee_amt` | `response.data.split_fee_info` | `$.total_split_fee_amt` | 分账手续费总金额(元) | `String` | `14` | `N` | 已确认 | 单位元 |
| `response.data.split_fee_info.split_fee_flag` | `response.data.split_fee_info` | `$.split_fee_flag` | 分账手续费扣款标志 | `String` | `1` | `N` | 已确认 | 1: 外扣 2: 内扣 |
| `response.data.split_fee_info.split_fee_details[]` | `response.data.split_fee_info` | `$.split_fee_details[]` | 分账手续费明细 | `Array` | `—` | `N` | N/A：结构字段长度 | 分账手续费明细 |
| `response.data.split_fee_info.split_fee_details[].split_fee_amt` | `response.data.split_fee_info` | `$.split_fee_details[].split_fee_amt` | 分账手续费金额(元) | `String` | `14` | `Y` | 已确认 | 单位元 |
| `response.data.split_fee_info.split_fee_details[].split_fee_huifu_id` | `response.data.split_fee_info` | `$.split_fee_details[].split_fee_huifu_id` | 分账手续费承担方商户号 | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `response.data.split_fee_info.split_fee_details[].split_fee_acct_id` | `response.data.split_fee_info` | `$.split_fee_details[].split_fee_acct_id` | 分账手续费承担方账号 | `String` | `16` | `Y` | 已确认 | 分账手续费承担方账号；示例值：F00598600 |
| `response.data.org_party_order_id` | `response.data.org_party_order_id` | `—（直接 JSON 路径）` | 原交易用户账单上的商户订单号 | `String` | `64` | `N` | 已确认 | 扫码退款返回；示例值：H[官网示例已脱敏] |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `84` | `N` | 已确认 | 扫码退款返回；示例值：备注 |
| `response.data.loan_flag` | `response.data.loan_flag` | `—（直接 JSON 路径）` | 是否垫资退款 | `String` | `2` | `N` | 已确认 | Y 是垫资出款， N 是普通出款，为空默认N；示例值： N；注意：延时交易退款在【交易确认退款】接口中设置loan_flag为垫资，；本接口不可再次设置垫资。 |
| `response.data.loan_undertaker` | `response.data.loan_undertaker` | `—（直接 JSON 路径）` | 垫资承担者 | `String` | `32` | `N` | 已确认 | 垫资方的huifu_id；示例值：[官网示例已脱敏]；为空则各自承担。不为空走第三方垫资，目前支持商户垫资 |
| `response.data.loan_acct_type` | `response.data.loan_acct_type` | `—（直接 JSON 路径）` | 垫资账户类型 | `String` | `2` | `N` | 已确认 | 01:基本户, 05: 充值户, 默认充值户；示例值：01 |
| `response.data.org_out_order_id` | `response.data.org_out_order_id` | `—（直接 JSON 路径）` | 原外部订单号 | `String` | `128` | `N` | 已确认 | 扫码退款返回；示例值：H[官网示例已脱敏] |
| `response.data.unionpay_response` | `response.data.unionpay_response` | `—（String(JSON) 容器）` | 银联返回的响应报文 | `String` | `6000` | `N` | 已确认 | 扫码退款返回，同扫码退款查询接口，jsonObject字符串 |
| `response.data.unionpay_response.coupon_info[]` | `response.data.unionpay_response` | `$.coupon_info（String(JSON Array) 容器）` | 银联优惠信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 银联使用优惠活动时出现，jsonArray字符串格式 |
| `response.data.unionpay_response.coupon_info[].addnInfo` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].addnInfo` | 附加信息 | `String` | `100` | `N` | 已确认 | 内容自定义；示例值：附加信息 |
| `response.data.unionpay_response.coupon_info[].spnsrId` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].spnsrId` | 出资方 | `String` | `20` | `N` | 已确认 | 00010000：银联出资；付款方作为出资方：填写8位付款方机构代码；商户作为出资方：填写15位商户代码；示例值：00010000 |
| `response.data.unionpay_response.coupon_info[].type` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].type` | 项目类型 | `String` | `4` | `N` | 已确认 | DD01：随机立减， CP01：抵金券；示例值：DD01 |
| `response.data.unionpay_response.coupon_info[].offstAmt` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].offstAmt` | 抵消交易金额 | `String` | `14` | `N` | 已确认 | 不能为全0；单位元；示例值：1.00 |
| `response.data.unionpay_response.coupon_info[].id` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].id` | 项目编号 | `String` | `40` | `N` | 已确认 | 用于票券编号等，格式自定义；示例值：938434221 |
| `response.data.unionpay_response.coupon_info[].desc` | `response.data.unionpay_response` | `$.coupon_info => JSON decode => $[].desc` | 项目简称 | `String` | `40` | `N` | 已确认 | 优惠活动简称，可用于展示、打单等；示例值：中秋优惠促销 |
| `response.data.dy_response` | `response.data.dy_response` | `—（String(JSON) 容器）` | 抖音返回的响应报文 | `String` | `6000` | `N` | 已确认 | 抖音返回的响应报文，jsonObject字符串 |
| `response.data.dy_response.org_out_trans_id` | `response.data.dy_response` | `$.org_out_trans_id` | 抖音原交易订单号 | `String` | `32` | `N` | 已确认 | 示例值：20201030189770 |
| `response.data.dy_response.out_trans_id` | `response.data.dy_response` | `$.out_trans_id` | 抖音退款单号 | `String` | `32` | `N` | 已确认 | 示例值：6545342375 |
| `response.data.dy_response.payer_refund` | `response.data.dy_response` | `$.payer_refund` | 用户退款金额 | `String` | `12` | `N` | 已确认 | 退款给用户的金额，不包含所有优惠券金额 ，单位:元；示例值：1.00 |
| `response.data.trans_finish_time` | `response.data.trans_finish_time` | `—（直接 JSON 路径）` | 退款完成时间 | `String` | `14` | `N` | 已确认 | 格式yyyyMMddHHmmss；示例值：20091225091010 |
| `response.data.sub_orders_response[]` | `response.data.sub_orders_response` | `—（String(JSON Array) 容器）` | 退款子单返回信息列表 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray格式字符串；合单支付的订单返回该字段 |
| `response.data.sub_orders_response[].sub_huifu_id` | `response.data.sub_orders_response` | `$[].sub_huifu_id` | 退款子单商户号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.sub_orders_response[].sub_req_date` | `response.data.sub_orders_response` | `$[].sub_req_date` | 退款子单请求日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `response.data.sub_orders_response[].sub_req_seq_id` | `response.data.sub_orders_response` | `$[].sub_req_seq_id` | 退款子单请求流水号 | `String` | `128` | `N` | 已确认 | 示例值：rQ[官网示例已脱敏] |
| `response.data.sub_orders_response[].sub_hf_seq_id` | `response.data.sub_orders_response` | `$[].sub_hf_seq_id` | 退款子单全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：0030default220825182711P099ac1f343f00000 |
| `response.data.sub_orders_response[].sub_org_req_date` | `response.data.sub_orders_response` | `$[].sub_org_req_date` | 原子单交易请求日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `response.data.sub_orders_response[].sub_org_req_seq_id` | `response.data.sub_orders_response` | `$[].sub_org_req_seq_id` | 原子单交易请求流水号 | `String` | `128` | `N` | 已确认 | 示例值： |
| `response.data.sub_orders_response[].sub_org_ord_amt` | `response.data.sub_orders_response` | `$[].sub_org_ord_amt` | 原子单交易订单金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.sub_orders_response[].sub_org_fee_amt` | `response.data.sub_orders_response` | `$[].sub_org_fee_amt` | 原子单交易手续费 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.sub_orders_response[].sub_trans_date` | `response.data.sub_orders_response` | `$[].sub_trans_date` | 子单退款交易发生日期 | `String` | `8` | `N` | 已确认 | 格式为yyyyMMdd，示例值：20220925 |
| `response.data.sub_orders_response[].sub_ord_amt` | `response.data.sub_orders_response` | `$[].sub_ord_amt` | 子单退款金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.sub_orders_response[].sub_actual_ref_amt` | `response.data.sub_orders_response` | `$[].sub_actual_ref_amt` | 子单实际退款金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.sub_orders_response[].sub_total_ref_amt` | `response.data.sub_orders_response` | `$[].sub_total_ref_amt` | 原子单交易累计退款金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.sub_orders_response[].sub_total_ref_fee_amt` | `response.data.sub_orders_response` | `$[].sub_total_ref_fee_amt` | 原子单交易累计退款手续费金额 | `String` | `14` | `N` | 已确认 | 单位元，示例值：1.00；注意：退还手续费规则参见[说明文档](https://paas.huifu.com/open/doc/api/#/api_tksxfsm) |
| `response.data.sub_orders_response[].sub_ref_cut` | `response.data.sub_orders_response` | `$[].sub_ref_cut` | 子单累计退款次数 | `String` | `14` | `N` | 已确认 | 示例值：1 |
| `response.data.sub_orders_response[].acct_split_bunch` | `response.data.sub_orders_response` | `$[].acct_split_bunch => [需要官方确认]：String 子表编码` | 分账信息 | `String` | `4000` | `N` | 已确认 | 分账信息 |
| `response.data.sub_orders_response[].acct_split_bunch.acct_infos` | `response.data.sub_orders_response` | `$[].acct_split_bunch.acct_infos => [需要官方确认]：String 子表编码` | 分账明细 | `String` | `2048` | `N` | 已确认 | 分账明细 |
| `response.data.sub_orders_response[].acct_split_bunch.acct_infos.div_amt` | `response.data.sub_orders_response` | `$[].acct_split_bunch.acct_infos => [需要官方确认]：String 子表编码` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.sub_orders_response[].acct_split_bunch.acct_infos.huifu_id` | `response.data.sub_orders_response` | `$[].acct_split_bunch.acct_infos => [需要官方确认]：String 子表编码` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户时生成；示例值：[官网示例已脱敏] |
| `response.data.sub_orders_response[].acct_split_bunch.fee_amt` | `response.data.sub_orders_response` | `$[].acct_split_bunch => [需要官方确认]：String 子表编码` | 退款返还手续费 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.sub_orders_response[].split_fee_info` | `response.data.sub_orders_response` | `$[].split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费信息 | `String` | `—` | `N` | [需要官方确认]：长度 | 分账手续费信息 |
| `response.data.sub_orders_response[].split_fee_info.total_split_fee_amt` | `response.data.sub_orders_response` | `$[].split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费总金额(元) | `String` | `14` | `N` | 已确认 | 示例值：0.10 |
| `response.data.sub_orders_response[].split_fee_info.split_fee_flag` | `response.data.sub_orders_response` | `$[].split_fee_info => [需要官方确认]：String 子表编码` | 分账手续费扣款标志 | `Integer` | `1` | `Y` | 已确认 | 1: 外扣 2: 内扣；示例值：1 |
| `response.data.sub_orders_response[].split_fee_info.split_fee_details[]` | `response.data.sub_orders_response` | `$[].split_fee_info.split_fee_details（String(JSON Array) 容器）` | 分账手续费明细 | `String` | `—` | `Y` | [需要官方确认]：长度 | jsonArray格式 |
| `response.data.sub_orders_response[].split_fee_info.split_fee_details[].split_fee_amt` | `response.data.sub_orders_response` | `$[].split_fee_info.split_fee_details => JSON decode => $[].split_fee_amt` | 分账手续费金额 | `String` | `14` | `Y` | 已确认 | 示例值：1.00 |
| `response.data.sub_orders_response[].split_fee_info.split_fee_details[].split_fee_huifu_id` | `response.data.sub_orders_response` | `$[].split_fee_info.split_fee_details => JSON decode => $[].split_fee_huifu_id` | 分账手续费承担方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.sub_orders_response[].split_fee_info.split_fee_details[].split_fee_acct_id` | `response.data.sub_orders_response` | `$[].split_fee_info.split_fee_details => JSON decode => $[].split_fee_acct_id` | 分账手续费承担方账号 | `String` | `9` | `N` | 已确认 | 示例值：F00598600 |
| `response.data.sub_orders_response[].sub_remark` | `response.data.sub_orders_response` | `$[].sub_remark` | 子单备注 | `String` | `1500` | `N` | 已确认 | 原样返回；示例值：子单备注 |
| `response.data.sub_orders_response[].fund_freeze_stat` | `response.data.sub_orders_response` | `$[].fund_freeze_stat` | 资金冻结状态 | `String` | `16` | `N` | 已确认 | FREEZE：冻结；UNFREEZE：解冻；示例值：UNFREEZE；退款发生时，对应原交易的资金冻结状态。 |

## 托管交易关单

- 原始地址：<https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hostinggd.md>
- SHA-256：`97b61f7e7725b4cf999a8a05ad3eb332a2183cc56100d558c2499ebe57574f51`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 请求格式：yyyyMMdd；示例值：20221023 |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 开户自动生成示例值：[官网示例已脱敏] |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 原请求日期 | `String` | `8` | `Y` | 已确认 | 请求格式：yyyyMMdd；示例值：20221023 |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原请求流水号 | `String` | `64` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | 参见业务返回码；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | 参见业务返回码；示例值：交易成功 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 交易时传入原样返回，示例值：rQ[官网示例已脱敏] |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 交易时传入，原样返回，示例值：20220905 |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 原请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20221023 |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原请求流水号 | `String` | `64` | `Y` | 已确认 | 示例值：rQ[官网示例已脱敏] |
| `response.data.org_trans_stat` | `response.data.org_trans_stat` | `—（直接 JSON 路径）` | 原交易状态 | `String` | `1` | `N` | 已确认 | P：处理中、S：成功、F：失败；示例值：S |
| `response.data.close_stat` | `response.data.close_stat` | `—（直接 JSON 路径）` | 关单状态 | `String` | `1` | `Y` | 已确认 | P：处理中、S：成功、F：失败；示例值：S |

### 关单异步 resp_data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.resp_data.resp_code` | `async.resp_data` | `$.resp_code` | 业务响应码 | `String` | `8` | `Y` | 已确认 | 参见业务返回码；示例值：00000000 |
| `async.resp_data.resp_desc` | `async.resp_data` | `$.resp_desc` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | 参见业务返回码；示例值：交易成功 |
| `async.resp_data.huifu_id` | `async.resp_data` | `$.huifu_id` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.org_req_date` | `async.resp_data` | `$.org_req_date` | 原请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20221023 |
| `async.resp_data.org_req_seq_id` | `async.resp_data` | `$.org_req_seq_id` | 原请求流水号 | `String` | `64` | `Y` | 已确认 | 示例值：rQ[官网示例已脱敏] |
| `async.resp_data.org_trans_stat` | `async.resp_data` | `$.org_trans_stat` | 原交易状态 | `String` | `1` | `N` | 已确认 | P：处理中、S：成功、F：失败；示例值：S |
| `async.resp_data.close_stat` | `async.resp_data` | `$.close_stat` | 关单状态 | `String` | `1` | `Y` | 已确认 | S：成功、F：失败；示例值：S |

## 拆单支付订单查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/cpjs/api_cpjs_hostingcdzf.md>
- SHA-256：`96e61c672ce32f16f4f8f7068d26063b3c8302be7bca5e2b17dce4d309282938`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 请求格式：yyyyMMdd；示例值：20221023 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 开户自动生成；示例值：[官网示例已脱敏] |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `Y` | 已确认 | 请求格式：yyyyMMdd；示例值：20221023 |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `64` | `Y` | 已确认 | 示例值：rQ[官网示例已脱敏] |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [参见业务返回码](http://paas.huifutest.com/partners/api/#/smzf/api_qrpay_cx?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)（官网原始地址为非 HTTPS，不得静默改写）（官网原文测试域，不作为生产地址）；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `512` | `Y` | 已确认 | [参见业务返回码](http://paas.huifutest.com/partners/api/#/smzf/api_qrpay_cx?id=%e4%b8%9a%e5%8a%a1%e8%bf%94%e5%9b%9e%e7%a0%81)（官网原始地址为非 HTTPS，不得静默改写）（官网原文测试域，不作为生产地址）；示例值：操作成功 |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 请求格式：yyyyMMdd；示例值：20221023 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `64` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：rQ[官网示例已脱敏] |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20220125 |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.pre_order_id` | `response.data.pre_order_id` | `—（直接 JSON 路径）` | 预下单订单号 | `String` | `64` | `Y` | 已确认 | 示例值：H[官网示例已脱敏] |
| `response.data.order_stat` | `response.data.order_stat` | `—（直接 JSON 路径）` | 预下单状态 | `String` | `1` | `N` | 已确认 | 1:支付成功,2:支付中,3:已退款,4:处理中,5:支付失败,6-部分退款；[参见状态说明文档](http://paas.huifu.com/open/doc/api/#/cpjs/api_cpjs_statsm)（官网原始地址为非 HTTPS，不得静默改写）；示例值：1 |
| `response.data.trans_list[]` | `response.data.trans_list` | `—（String(JSON Array) 容器）` | 拆单支付列表 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonArray格式 |
| `response.data.trans_list[].pay_type` | `response.data.trans_list` | `$[].pay_type` | 交易类型 | `String` | `16` | `N` | 已确认 | T_MINIAPP：微信小程序支付；A_NATIVE ：支付宝正扫；示例值：T_JSAPI |
| `response.data.trans_list[].org_hf_seq_id` | `response.data.trans_list` | `$[].org_hf_seq_id` | 原机构请求流水号 | `String` | `128` | `N` | 已确认 | 示例值：00290TOP1GR210919004230P853ac[官网示例已脱敏] |
| `response.data.trans_list[].trans_amt` | `response.data.trans_list` | `$[].trans_amt` | 交易金额(元) | `String` | `14` | `N` | 已确认 | 保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.trans_list[].party_order_id` | `response.data.trans_list` | `$[].party_order_id` | 用户账单上的商户订单号 | `String` | `64` | `N` | 已确认 | 示例值：[官网示例已脱敏]；[参见用户账单说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_yhzd) |
| `response.data.trans_list[].fee_amt` | `response.data.trans_list` | `$[].fee_amt` | 手续费金额(元) | `String` | `14` | `N` | 已确认 | 保留小数点后两位，最低传入0.01。示例值：1.00 |
| `response.data.trans_list[].ref_amt` | `response.data.trans_list` | `$[].ref_amt` | 可退金额(元) | `String` | `14` | `N` | 已确认 | 示例值：1.00 |
| `response.data.trans_list[].trans_stat` | `response.data.trans_list` | `$[].trans_stat` | 交易状态 | `String` | `1` | `N` | 已确认 | P：处理中；S：成功；F：失败；I: 初始；示例值：S；初始状态很罕见，请联系汇付技术人员处理 |
| `response.data.trans_list[].trans_time` | `response.data.trans_list` | `$[].trans_time` | 交易时间 | `String` | `14` | `N` | 已确认 | 格式：yyyymmddHHMMSS；示例值：20231112200913 |
| `response.data.trans_list[].bank_code` | `response.data.trans_list` | `$[].bank_code` | 外部通道返回码 | `String` | `32` | `N` | 已确认 | 示例值：TRADE_SUCCESS |
| `response.data.trans_list[].bank_desc` | `response.data.trans_list` | `$[].bank_desc` | 外部通道返回描述 | `String` | `200` | `N` | 已确认 | 示例值：TRADE_SUCCESS |
| `response.data.trans_list[].wx_response` | `response.data.trans_list` | `$[].wx_response（String(JSON) 容器）` | 微信返回的响应报文 | `String` | `6000` | `N` | 已确认 | jsonObject格式 |
| `response.data.trans_list[].wx_response.wx_user_id` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.wx_user_id` | 微信用户唯一标识码 | `String` | `128` | `N` | 已确认 | 示例值：W6NYVcMwXDfAT+3LXuLSMx+UH5AXx1kG7JzTiTEomdk= |
| `response.data.trans_list[].wx_response.sub_appid` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.sub_appid` | 子商户公众账号ID | `String` | `32` | `N` | 已确认 | 微信分配的子商户公众账号ID；示例值：wxec280d4c8a1cc2ca |
| `response.data.trans_list[].wx_response.openid` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.openid` | 用户标识 | `String` | `128` | `Y` | 已确认 | 用户在商户appid下的唯一标识；示例值：oGhiSxIAPtEnPfe9Xo000000B |
| `response.data.trans_list[].wx_response.sub_openid` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.sub_openid` | 子商户用户标识 | `String` | `128` | `N` | 已确认 | 用户在子商户appid下的唯一标识；示例值：oWNHX5RNaCUmZR |
| `response.data.trans_list[].wx_response.bank_type` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.bank_type` | 付款银行 | `String` | `16` | `Y` | 已确认 | 银行类型，采用字符串类型的银行标识，[银行类型见附表](https://pay.weixin.qq.com/wiki/doc/apiv3/terms_definition/chapter1_1_3.shtml#part-7)；示例值：OTHERS |
| `response.data.trans_list[].wx_response.cash_fee` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.cash_fee` | 现金支付金额 | `String` | `12` | `N` | 已确认 | 订单现金支付金额；示例值：10.00 |
| `response.data.trans_list[].wx_response.coupon_fee` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.coupon_fee` | 代金券金额 | `String` | `12` | `N` | 已确认 | 代金券或立减优惠金额<=订单总金额，；订单总金额-代金券或立减优惠金额=现金支付金额；示例值：1.00 |
| `response.data.trans_list[].wx_response.attach` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.attach` | 商家数据包 | `String` | `128` | `N` | 已确认 | 原样返回；示例值：附加数据 |
| `response.data.trans_list[].wx_response.promotion_detail[]` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[]` | 营销详情列表 | `Array` | `6000` | `N` | 已确认 | 营销详情列表，使返回值为Json格式 |
| `response.data.trans_list[].wx_response.promotion_detail[].promotion_id` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].promotion_id` | 券或者立减优惠id | `String` | `32` | `Y` | 已确认 | 示例值：2345234235 |
| `response.data.trans_list[].wx_response.promotion_detail[].name` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].name` | 优惠名称 | `String` | `64` | `N` | 已确认 | 示例值：八折券 |
| `response.data.trans_list[].wx_response.promotion_detail[].scope` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].scope` | 优惠范围 | `String` | `32` | `N` | 已确认 | GLOBAL: 全场代金券，SINGLE: 单品优惠；示例值：SINGLE |
| `response.data.trans_list[].wx_response.promotion_detail[].type` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].type` | 优惠类型 | `String` | `32` | `N` | 已确认 | COUPON: 代金券，需要走结算资金的充值型代金券,（境外商户券币种与支付币种一致） ；DISCOUNT: 优惠券，不走结算资金的免充值型优惠券，（境外商户券币种与标价币种一致）；示例值：DISCOUNT |
| `response.data.trans_list[].wx_response.promotion_detail[].amount` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].amount` | 优惠券面额 | `String` | `5` | `Y` | 已确认 | 用户享受优惠的金额；示例值：10.00 |
| `response.data.trans_list[].wx_response.promotion_detail[].activity_id` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].activity_id` | 活动ID | `String` | `32` | `Y` | 已确认 | 在微信商户后台配置的批次ID；示例值：[官网示例已脱敏] |
| `response.data.trans_list[].wx_response.promotion_detail[].merchant_contribute` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].merchant_contribute` | 商户出资 | `String` | `32` | `N` | 已确认 | 特指商户自己创建的优惠，出资金额等于本项优惠总金额，单位为元；示例值：10.00 |
| `response.data.trans_list[].wx_response.promotion_detail[].other_contribute` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].other_contribute` | 其他出资 | `String` | `32` | `N` | 已确认 | 其他出资方出资金额，单位为元；示例值：5.00 |
| `response.data.trans_list[].wx_response.promotion_detail[].goods_detail` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].goods_detail` | 单品列表 | `Object` | `3000` | `N` | 已确认 | 使用Json格式 |
| `response.data.trans_list[].wx_response.promotion_detail[].goods_detail.goods_id` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].goods_detail.goods_id` | 商品编码 | `String` | `32` | `Y` | 已确认 | 由半角的大小写字母、数字、中划线、下划线中的一种或几种组成；示例值：6934572310301 |
| `response.data.trans_list[].wx_response.promotion_detail[].goods_detail.goods_remark` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].goods_detail.goods_remark` | 商品备注 | `String` | `32` | `N` | 已确认 | goods_remark为备注字段，按照配置原样返回，字段内容在微信后台配置券时进行设置。示例值：商品备注 |
| `response.data.trans_list[].wx_response.promotion_detail[].goods_detail.discount_amount` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].goods_detail.discount_amount` | 商品优惠金额 | `String` | `32` | `Y` | 已确认 | 单品的总优惠金额，单位为：元；示例值：20.00 |
| `response.data.trans_list[].wx_response.promotion_detail[].goods_detail.quantity` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].goods_detail.quantity` | 商品数量 | `String` | `32` | `Y` | 已确认 | 用户购买的数量；示例值：10 |
| `response.data.trans_list[].wx_response.promotion_detail[].goods_detail.price` | `response.data.trans_list` | `$[].wx_response => JSON decode => $.promotion_detail[].goods_detail.price` | 商品价格 | `String` | `32` | `Y` | 已确认 | 单位为: 元。示例值：50.00；如果商户有优惠，需传输商户优惠后的单价(例如：用户对一笔100元的订单使用了商场发的纸质优惠券100-50，则活动商品的单价应为原单价-50) |
| `response.data.trans_list[].alipay_response` | `response.data.trans_list` | `$[].alipay_response（String(JSON) 容器）` | 支付宝返回的响应报文 | `String` | `6000` | `N` | 已确认 | jsonObject格式 |
| `response.data.trans_list[].alipay_response.voucher_detail_list[]` | `response.data.trans_list` | `$[].alipay_response => JSON decode => $.voucher_detail_list[]` | 优惠券信息 | `Array` | `—` | `N` | N/A：结构字段长度 | 本交易支付时使用的所有优惠券信息 |
| `response.data.trans_list[].alipay_response.voucher_detail_list[].id` | `response.data.trans_list` | `$[].alipay_response => JSON decode => $.voucher_detail_list[].id` | 券id | `String` | `32` | `Y` | 已确认 | 示例值：6934572310301 |
| `response.data.trans_list[].alipay_response.voucher_detail_list[].name` | `response.data.trans_list` | `$[].alipay_response => JSON decode => $.voucher_detail_list[].name` | 券名称 | `String` | `32` | `Y` | 已确认 | 示例值：实体店付款通用立减券 |
| `response.data.trans_list[].alipay_response.voucher_detail_list[].type` | `response.data.trans_list` | `$[].alipay_response => JSON decode => $.voucher_detail_list[].type` | 券类型 | `String` | `32` | `Y` | 已确认 | 当前有三种类型： ；ALIPAY_FIX_VOUCHER: 全场代金券；ALIPAY_DISCOUNT_VOUCHER: 折扣券；ALIPAY_ITEM_VOUCHER: 单品优惠 ；示例值：ALIPAY_ITEM_VOUCHER；注：不排除将来新增其他类型的可能，商家接入时注意兼容性避免硬编码 |
| `response.data.trans_list[].alipay_response.voucher_detail_list[].amount` | `response.data.trans_list` | `$[].alipay_response => JSON decode => $.voucher_detail_list[].amount` | 优惠券面额（元） | `String` | `8` | `Y` | 已确认 | 它应该会等于商家出资加上其他出资方出资；示例值：10.00 |
| `response.data.trans_list[].alipay_response.voucher_detail_list[].merchant_contribute` | `response.data.trans_list` | `$[].alipay_response => JSON decode => $.voucher_detail_list[].merchant_contribute` | 商家出资 | `String` | `8` | `N` | 已确认 | 特指发起交易的商家出资金额；示例值：10.00 |
| `response.data.trans_list[].alipay_response.voucher_detail_list[].other_contribute` | `response.data.trans_list` | `$[].alipay_response => JSON decode => $.voucher_detail_list[].other_contribute` | 其他出资方出资金额 | `String` | `11` | `N` | 已确认 | 可能是支付宝、品牌商、第三方，也可能是他们的一起出资；示例值：0.00 |
| `response.data.trans_list[].alipay_response.fund_bill_list` | `response.data.trans_list` | `$[].alipay_response => JSON decode => $.fund_bill_list` | 支付金额信息 | `Object` | `512` | `N` | 已确认 | 支付成功的各个渠道金额信息，详见资金明细信息说明；json格式 |
| `response.data.trans_list[].alipay_response.fund_bill_list.bank_code` | `response.data.trans_list` | `$[].alipay_response => JSON decode => $.fund_bill_list.bank_code` | 银行代码 | `String` | `10` | `N` | 已确认 | 银行卡支付时的银行代码；示例值：CEB；请参考[支付宝直付通结算账户填写标准表](https://opendocs.alipay.com/open/direct-payment/cg5mkp#%E7%9B%B8%E5%85%B3%E8%B5%84%E6%96%99) |
| `response.data.trans_list[].alipay_response.buyer_id` | `response.data.trans_list` | `$[].alipay_response => JSON decode => $.buyer_id` | 买家的支付宝唯一用户号 | `String` | `28` | `N` | 已确认 | 2088开头的16位纯数字；示例值：[官网示例已脱敏] |
| `response.data.trans_list[].alipay_response.buyer_logon_id` | `response.data.trans_list` | `$[].alipay_response => JSON decode => $.buyer_logon_id` | 买家支付宝账号 | `String` | `100` | `N` | 已确认 | 示例值：carl.chen@huifu.com |
| `response.data.trans_list[].alipay_response.hb_fq_num` | `response.data.trans_list` | `$[].alipay_response => JSON decode => $.hb_fq_num` | 花呗分期数 | `String` | `10` | `N` | 已确认 | 示例值：3 |
| `response.data.trans_list[].alipay_response.hb_fq_seller_percent` | `response.data.trans_list` | `$[].alipay_response => JSON decode => $.hb_fq_seller_percent` | 卖家承担的手续费 | `String` | `3` | `N` | 已确认 | 示例值：1.00 |

## 交易分账明细查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/smzf/api_fzmxcx.md>
- SHA-256：`dcab5eb128a7987742ea339631add74ad771227d3ce557c1154d6d6a27266270`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：MCS |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 数据 | `Json` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `Json` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.hf_seq_id` | `request.data.hf_seq_id` | `—（直接 JSON 路径）` | 分账交易汇付全局流水号 | `String` | `128` | `Y` | 已确认 | 示例值：00470topo1A211015160805P090ac132fef00000 |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 汇付分配的商户号，示例值：[官网示例已脱敏] |
| `request.data.ord_type` | `request.data.ord_type` | `—（直接 JSON 路径）` | 交易类型 | `String` | `20` | `Y` | 已确认 | consume：正向交易，refund：反向交易；示例值：consume |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/smzf/api_fzmxcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `256` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/api/doc/smzf/api_fzmxcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：成功 |
| `response.data.total_size` | `response.data.total_size` | `—（直接 JSON 路径）` | 总记录数 | `String` | `32` | `Y` | 已确认 | 总计返回条数，示例值：100 |
| `response.data.split_trans_responses[]` | `response.data.split_trans_responses` | `$[]（String(JSON Array) 解码结果）` | 分账交易列表 | `String` | `—` | `N` | [需要官方确认]：长度 | — |
| `response.data.split_trans_responses[].req_seq_id` | `response.data.split_trans_responses` | `$[].req_seq_id（String(JSON Array) 解码结果）` | 请求流水号 | `String` | `128` | `N` | 已确认 | 示例值：202101171122111 |
| `response.data.split_trans_responses[].req_date` | `response.data.split_trans_responses` | `$[].req_date（String(JSON Array) 解码结果）` | 请求日期 | `String` | `8` | `N` | 已确认 | yyyyMMdd；示例值：20221023 |
| `response.data.split_trans_responses[].huifu_id` | `response.data.split_trans_responses` | `$[].huifu_id（String(JSON Array) 解码结果）` | 出账方商户号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.split_trans_responses[].in_huifu_id` | `response.data.split_trans_responses` | `$[].in_huifu_id（String(JSON Array) 解码结果）` | 入账方商户号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.split_trans_responses[].product_id` | `response.data.split_trans_responses` | `$[].product_id（String(JSON Array) 解码结果）` | 产品号 | `String` | `32` | `N` | 已确认 | 示例值：YYZY |
| `response.data.split_trans_responses[].org_ord_id` | `response.data.split_trans_responses` | `$[].org_ord_id（String(JSON Array) 解码结果）` | 订单流水号 | `String` | `128` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.split_trans_responses[].trans_ord_id` | `response.data.split_trans_responses` | `$[].trans_ord_id（String(JSON Array) 解码结果）` | 汇付交易订单号 | `String` | `128` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.split_trans_responses[].hf_seq_id` | `response.data.split_trans_responses` | `$[].hf_seq_id（String(JSON Array) 解码结果）` | 分账交易汇付全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00470topo1A211015160805P090ac132fef00000 |
| `response.data.split_trans_responses[].ord_type` | `response.data.split_trans_responses` | `$[].ord_type（String(JSON Array) 解码结果）` | 交易类型 | `String` | `20` | `N` | 已确认 | consume：正向交易、refund：反向交易；示例值：refund |
| `response.data.split_trans_responses[].split_amt` | `response.data.split_trans_responses` | `$[].split_amt（String(JSON Array) 解码结果）` | 分账金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：25.00 |
| `response.data.split_trans_responses[].split_fee_amt` | `response.data.split_trans_responses` | `$[].split_fee_amt（String(JSON Array) 解码结果）` | 分账手续费 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.split_trans_responses[].split_fee_huifu_id` | `response.data.split_trans_responses` | `$[].split_fee_huifu_id（String(JSON Array) 解码结果）` | 分账手续费承担方商户号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.split_trans_responses[].split_seq_id` | `response.data.split_trans_responses` | `$[].split_seq_id（String(JSON Array) 解码结果）` | 分账流水号 | `String` | `128` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.split_trans_responses[].split_type` | `response.data.split_trans_responses` | `$[].split_type（String(JSON Array) 解码结果）` | 分账类型 | `String` | `20` | `N` | 已确认 | realTime：实时、delay：延时；示例值：delay |
| `response.data.split_trans_responses[].trans_finish_time` | `response.data.split_trans_responses` | `$[].trans_finish_time（String(JSON Array) 解码结果）` | 分账完成时间 | `String` | `14` | `N` | 已确认 | yyyyMMddHHmmss；示例值：20221023112345 |
| `response.data.split_trans_responses[].acct_stat` | `response.data.split_trans_responses` | `$[].acct_stat（String(JSON Array) 解码结果）` | 账务状态 | `String` | `1` | `N` | 已确认 | P：处理中、S：成功、F：失败；示例值：S |

## 余额支付查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/yuer/api_acctpaycx.md>
- SHA-256：`79815b5911c183d16107976c94495a26e786157e511040013a4f7f90e45d6da7`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 发起方商户号；示例值：[官网示例已脱敏] |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `Y` | 已确认 | 原交易请求日期，格式：yyyyMMdd；示例值：20221023 |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `N` | 已确认 | 与org_hf_seq_id二选一；示例值：[官网示例已脱敏] |
| `request.data.org_hf_seq_id` | `request.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原交易全局流水号 | `String` | `128` | `N` | 已确认 | 与org_req_seq_id二选一；示例值：003500TOP2B211021163242P447ac132fd200000 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/yuer/api_acctpaycx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） ；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务返回描述 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/api/doc/yuer/api_acctpaycx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：交易成功 |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原交易请求流水号 | `String` | `128` | `Y` | 已确认 | 业务请求流水号(发起余额支付请求流水号)；示例值：[官网示例已脱敏] |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 原交易请求日期 | `String` | `8` | `Y` | 已确认 | 原交易请求日期，格式：yyyyMMdd，示例值：20221013 |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 发起方商户号；示例值：[官网示例已脱敏] |
| `response.data.ord_amt` | `response.data.ord_amt` | `—（直接 JSON 路径）` | 支付金额 | `String` | `14` | `Y` | 已确认 | 示例值：23.00 |
| `response.data.acct_split_bunch` | `response.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `—` | `N` | [需要官方确认]：长度 | 分账信息，jsonObject字符串。余额支付支持付款给多账户。；如余额支付100元，支付给A账户60元，支付给B账户40元。 |
| `response.data.acct_split_bunch.acct_infos[]` | `response.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `—` | `N` | N/A：结构字段长度 | acct_infos |
| `response.data.acct_split_bunch.acct_infos[].div_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `response.data.acct_split_bunch.acct_infos[].huifu_id` | `response.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 斗拱开户自动生成编号；示例值：[官网示例已脱敏] |
| `response.data.acct_split_bunch.acct_infos[].trans_stat` | `response.data.acct_split_bunch` | `$.acct_infos[].trans_stat` | 分账交易状态 | `String` | `1` | `N` | 已确认 | 分账交易状态。灵活用工余额支付交易状态为C时，需查看分账交易状态 |
| `response.data.acct_split_bunch.acct_infos[].fee_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].fee_amt` | 手续费金额 | `String` | `14` | `N` | 已确认 | 手续费金额，单位:元。仅在分账接受方承担手续费时返回。 示例值：0.02 |
| `response.data.acct_split_bunch.acct_infos[].unconfirm_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].unconfirm_amt` | 未确认金额 | `String` | `14` | `N` | 已确认 | 未确认金额:元。 示例值：0.02 |
| `response.data.acct_split_bunch.fee_huifu_id` | `response.data.acct_split_bunch` | `$.fee_huifu_id` | 手续费承担方商户号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.acct_split_bunch.fee_acct_id` | `response.data.acct_split_bunch` | `$.fee_acct_id` | 手续费承担方账户号 | `String` | `32` | `N` | 已确认 | 示例值：F00598600 |
| `response.data.acct_split_bunch.fee_amt` | `response.data.acct_split_bunch` | `$.fee_amt` | 手续费金额 | `String` | `14` | `Y` | 已确认 | 单位:元，保留两位小数。示例值：1.23 |
| `response.data.out_huifu_id` | `response.data.out_huifu_id` | `—（直接 JSON 路径）` | 出款商户号 | `String` | `32` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.org_hf_seq_id` | `response.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原交易全局流水号 | `String` | `128` | `N` | 已确认 | 汇付返回的流水号；示例值：00470topo1A211015160805P090ac132fef00000 |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `1` | `Y` | 已确认 | P:处理中；S：成功；F：失败；C：完成（灵活用工余额支付特有，需查看分账交易状态）；示例值：S |
| `response.data.trans_finish_time` | `response.data.trans_finish_time` | `—（直接 JSON 路径）` | 交易完成时间 | `String` | `14` | `Y` | 已确认 | 格式：yyyyMMddHHmmss；示例值：20211021163242 |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `256` | `N` | 已确认 | 示例值：备注 |
| `response.data.good_desc` | `response.data.good_desc` | `—（直接 JSON 路径）` | 商品描述 | `String` | `256` | `N` | 已确认 | 示例值：商品描述 |
| `response.data.delay_acct_flag` | `response.data.delay_acct_flag` | `—（直接 JSON 路径）` | 延时标记 | `String` | `1` | `N` | 已确认 | 是否延时交易，Y为延迟，N为不延迟，不传默认N；示例值：N |
| `response.data.trans_fee_take_flag` | `response.data.trans_fee_take_flag` | `—（直接 JSON 路径）` | 手续费承担方标识 | `String` | `4` | `C` | 已确认 | 余额支付手续费承担方标识；商户余额支付扣收规则为接口指定承担方时必填！枚举值：；OUT：出款方；IN：分账接受方。；示例值：IN |
| `response.data.unconfirm_amt` | `response.data.unconfirm_amt` | `—（直接 JSON 路径）` | 待确认总金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.confirmed_amt` | `response.data.confirmed_amt` | `—（直接 JSON 路径）` | 已确认总金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |

## 余额支付退款

- 原始地址：<https://paas.huifu.com/partners/api/doc/yuer/api_acctpaytk.md>
- SHA-256：`b95fbc14df93458a916fb59a5158f563af8f76a9e68bc4dc984ae4ac81168f1f`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20221023 |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 发起方商户号，示例值：[官网示例已脱敏] |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 原余额支付请求日期 | `String` | `8` | `Y` | 已确认 | 格式：yyyyMMdd；示例值：20221023 |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原余额支付请求流水号 | `String` | `128` | `C` | 已确认 | org_hf_seq_id和orgReqSeqId二选一；示例值：[官网示例已脱敏] |
| `request.data.org_hf_seq_id` | `request.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原余额支付支付全局流水号 | `String` | `128` | `C` | 已确认 | org_hf_seq_id和orgReqSeqId二选一；示例值：00470topo1A211015160805P090ac132fef00000 |
| `request.data.ord_amt` | `request.data.ord_amt` | `—（直接 JSON 路径）` | 退款金额 | `String` | `14` | `Y` | 已确认 | 示例值：10.00 |
| `request.data.acct_split_bunch` | `request.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `—` | `N` | [需要官方确认]：长度 | 分账信息，jsonObject字符串。余额支付分账给一个商户或多个商户，退款时也支持从多个商户分账退款。；每个商户退款金额不能超过原入账金额。 |
| `request.data.acct_split_bunch.acct_infos[]` | `request.data.acct_split_bunch` | `$.acct_infos[]` | 退账明细 | `Array` | `—` | `Y` | N/A：结构字段长度 | 退款明细 |
| `request.data.acct_split_bunch.acct_infos[].div_amt` | `request.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 退款金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 ,最低传入0.01 |
| `request.data.acct_split_bunch.acct_infos[].huifu_id` | `request.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 退款方ID | `String` | `32` | `Y` | 已确认 | 开户自动生成编号；示例值：[官网示例已脱敏] |
| `request.data.risk_check_data` | `request.data.risk_check_data` | `—（String(JSON) 容器）` | 安全信息 | `String` | `—` | `N` | [需要官方确认]：长度 | jsonObject字符串。例如:"{"subProduct":"","transferType":""}" |
| `request.data.risk_check_data.sub_product` | `request.data.risk_check_data` | `$.sub_product` | 产品子类 | `String` | `20` | `N` | 已确认 | 示例值：1 |
| `request.data.risk_check_data.transfer_type` | `request.data.risk_check_data` | `$.transfer_type` | 转账原因 | `String` | `2` | `Y` | 已确认 | 01：卡券推广类；02：卡券核销类；03：消费；04：工资代发；05：分润；示例值：01 |
| `request.data.remark` | `request.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `256` | `N` | 已确认 | 示例值：备注 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/yuer/api_acctpaytk.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） ；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务返回描述 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/api/doc/yuer/api_acctpaytk.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：交易成功 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 业务请求流水号；示例值：[官网示例已脱敏] |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 请求日期。格式：yyyyMMdd，示例值：20221013 |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 发起方商户号；示例值：[官网示例已脱敏] |
| `response.data.product_id` | `response.data.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 接入时提供；示例值：YYZY |
| `response.data.hf_seq_id` | `response.data.hf_seq_id` | `—（直接 JSON 路径）` | 全局流水号 | `String` | `40` | `N` | 已确认 | 汇付返回流水号；示例值：00470topo1A211015160805P090ac132fef00000 |
| `response.data.ord_amt` | `response.data.ord_amt` | `—（直接 JSON 路径）` | 退款金额 | `String` | `14` | `Y` | 已确认 | 示例值：20.00 |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 原余额支付请求日期 | `String` | `8` | `Y` | 已确认 | 格式：yyyyMMdd；示例值：20221103 |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 原余额支付请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.org_hf_seq_id` | `response.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原余额支付支付全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00470topo1A211015160805P090ac132fef00001 |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `1` | `N` | 已确认 | P:处理中；S：成功；F：失败；示例值：S |
| `response.data.trans_finish_time` | `response.data.trans_finish_time` | `—（直接 JSON 路径）` | 退款完成时间 | `String` | `14` | `Y` | 已确认 | 格式yyyyMMddHHmmss；示例值：20221104132334 |
| `response.data.acct_split_bunch` | `response.data.acct_split_bunch` | `—（String(JSON) 容器）` | 退款分账串 | `String` | `—` | `N` | [需要官方确认]：长度 | 分账信息，jsonObject字符串。；余额支付分账给一个商户或多个商户，退款时也支持从多个商户分账退款。；每个商户退款金额不能超过原入账金额。 |
| `response.data.acct_split_bunch.acct_infos[]` | `response.data.acct_split_bunch` | `$.acct_infos[]` | 退账明细 | `Array` | `—` | `Y` | N/A：结构字段长度 | 退款明细 |
| `response.data.acct_split_bunch.acct_infos[].div_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 退款金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 ,最低传入0.01 |
| `response.data.acct_split_bunch.acct_infos[].huifu_id` | `response.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 退款方ID | `String` | `32` | `Y` | 已确认 | 开户自动生成编号；示例值：[官网示例已脱敏] |
| `response.data.acct_split_bunch.acct_infos[].acct_id` | `response.data.acct_split_bunch` | `$.acct_infos[].acct_id` | 账户号 | `String` | `32` | `N` | 已确认 | 分账账户号；示例值：F00598600 |
| `response.data.acct_split_bunch.acct_infos[].fee_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].fee_amt` | 手续费金额 | `String` | `14` | `N` | 已确认 | 单位:元。仅在分账接受方承担手续费时返回。 示例值：0.02 |
| `response.data.acct_split_bunch.fee_huifu_id` | `response.data.acct_split_bunch` | `$.fee_huifu_id` | 手续费承担方商户号 | `String` | `16` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.acct_split_bunch.fee_acct_id` | `response.data.acct_split_bunch` | `$.fee_acct_id` | 手续费承担方账户号 | `String` | `32` | `N` | 已确认 | 示例值：A28356961 |
| `response.data.acct_split_bunch.fee_amt` | `response.data.acct_split_bunch` | `$.fee_amt` | 手续费 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `256` | `N` | 已确认 | 示例值：备注 |

## 余额支付退款查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/yuer/api_acctpaytkcx.md>
- SHA-256：`e31b15b8f72aa21458b054b33f6ddaa32d1f1a927edb48a56ce93d7c64685ce0`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.org_req_seq_id` | `request.data.org_req_seq_id` | `—（直接 JSON 路径）` | 退款请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.org_req_date` | `request.data.org_req_date` | `—（直接 JSON 路径）` | 余额支付退款请求日期 | `String` | `8` | `Y` | 已确认 | 格式：yyyyMMdd；示例值：20210917 |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 发起方商户号；示例值：[官网示例已脱敏] |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/yuer/api_acctpaytkcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） ；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务返回描述 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/api/doc/yuer/api_acctpaytkcx.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：交易成功 |
| `response.data.org_req_seq_id` | `response.data.org_req_seq_id` | `—（直接 JSON 路径）` | 退款请求流水号 | `String` | `128` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.org_req_date` | `response.data.org_req_date` | `—（直接 JSON 路径）` | 余额支付退款请求日期 | `String` | `8` | `Y` | 已确认 | 格式：yyyyMMdd；示例值：20210917 |
| `response.data.org_hf_seq_id` | `response.data.org_hf_seq_id` | `—（直接 JSON 路径）` | 原余额支付退款全局流水号 | `String` | `40` | `N` | 已确认 | 原余额支付退款全局流水号 |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 退款请求发起方商户号；示例值：[官网示例已脱敏] |
| `response.data.product_id` | `response.data.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 产品号，接入时提供；示例值：YYZY |
| `response.data.ord_amt` | `response.data.ord_amt` | `—（直接 JSON 路径）` | 退款金额 | `String` | `14` | `Y` | 已确认 | 需保留小数点后两位，示例值：10.00最低传入0.01 |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `1` | `Y` | 已确认 | P:处理中；S：成功；F：失败；示例值：S |
| `response.data.trans_finish_time` | `response.data.trans_finish_time` | `—（直接 JSON 路径）` | 退款完成时间 | `String` | `14` | `Y` | 已确认 | 格式yyyyMMddHHmmss；示例值：20221023112343 |
| `response.data.acct_split_bunch` | `response.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `—` | `N` | [需要官方确认]：长度 | 分账信息，jsonObject字符串。 |
| `response.data.acct_split_bunch.acct_infos[]` | `response.data.acct_split_bunch` | `$.acct_infos[]` | 退账明细 | `Array` | `—` | `Y` | N/A：结构字段长度 | 退款信息 |
| `response.data.acct_split_bunch.acct_infos[].div_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 退款金额 | `String` | `14` | `Y` | 已确认 | 示例值：9.00 |
| `response.data.acct_split_bunch.acct_infos[].huifu_id` | `response.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 退账方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.acct_split_bunch.acct_infos[].acct_id` | `response.data.acct_split_bunch` | `$.acct_infos[].acct_id` | 账户号 | `String` | `32` | `N` | 已确认 | 分账账户号；示例值：F00598600 |
| `response.data.acct_split_bunch.acct_infos[].fee_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].fee_amt` | 手续费金额 | `String` | `14` | `N` | 已确认 | 手续费金额，单位:元。仅在分账接受方承担手续费时返回。 示例值：0.02 |
| `response.data.acct_split_bunch.fee_huifu_id` | `response.data.acct_split_bunch` | `$.fee_huifu_id` | 手续费承担方商户号 | `String` | `16` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.acct_split_bunch.fee_acct_id` | `response.data.acct_split_bunch` | `$.fee_acct_id` | 手续费承担方账户号 | `String` | `32` | `N` | 已确认 | 示例值：A28356961 |
| `response.data.acct_split_bunch.fee_amt` | `response.data.acct_split_bunch` | `$.fee_amt` | 手续费 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `45` | `N` | 已确认 | 示例值：备注 |
| `response.data.unconfirm_amt` | `response.data.unconfirm_amt` | `—（直接 JSON 路径）` | 待确认总金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.confirmed_amt` | `response.data.confirmed_amt` | `—（直接 JSON 路径）` | 已确认总金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |

## 手续费试算

- 原始地址：<https://paas.huifu.com/partners/api/doc/sxf/api_sxf_sxfss.md>
- SHA-256：`e5a3270bbb76fa2a4948b129414568e3b57d41fae1ff080749e1c2b171a9f862`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：MCS |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 数据 | `Json` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `Json` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式为yyyyMMdd，示例值：20091225 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 同一huifu_id下当天唯一；示例值：[官网示例已脱敏] |
| `request.data.trade_type` | `request.data.trade_type` | `—（直接 JSON 路径）` | 交易类型 | `String` | `32` | `Y` | 已确认 | T_JSAPI: 微信公众号,； T_MINIAPP: 微信小程序, ；A_JSAPI: 支付宝JS,； A_NATIVE: 支付宝正扫,； U_NATIVE: 银联正扫,； U_JSAPI: 银联JS,； ENCASHMENT：取现，；ACCT_PAYMENT:余额支付，； ONLINE_PAY:网银，；QUICK_PAY:快捷，；WAP_PAY:手机WAP，；UNION_PAY：银联统一支付；示例值：UNION_PAY |
| `request.data.online_trans_type` | `request.data.online_trans_type` | `—（直接 JSON 路径）` | 网银交易类型 | `String` | `3` | `N` | 已确认 | 网银交易必传；3000:B2B网银支付，3001:B2C网银支付，3002:B2B网银充值，3003:B2C网银充值；示例值：3001 |
| `request.data.trans_amt` | `request.data.trans_amt` | `—（直接 JSON 路径）` | 交易金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.01 |
| `request.data.bank_id` | `request.data.bank_id` | `—（直接 JSON 路径）` | 付款方银行编号 | `String` | `8` | `N` | 已确认 | 网银、快捷和wap手机支付类交易需传入；参考： [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；示例值：01020000 |
| `request.data.card_type` | `request.data.card_type` | `—（直接 JSON 路径）` | 卡类型 | `String` | `8` | `N` | 已确认 | D：借记卡，C：信用卡，默认：D（借记卡）；示例值：C |
| `request.data.channel_no` | `request.data.channel_no` | `—（直接 JSON 路径）` | 渠道号 | `String` | `32` | `N` | 已确认 | 扫码交易必传；如果交易走自有渠道请联系运维人员获取；示例值:10000001 |
| `request.data.digital_bank_no` | `request.data.digital_bank_no` | `—（直接 JSON 路径）` | 数字货币银行编号 | `String` | `5` | `N` | 已确认 | 01002: 工行，01004: 中行， 01005: 建行，01008：邮储 ；示例值：01002 |
| `request.data.encash_type` | `request.data.encash_type` | `—（直接 JSON 路径）` | 取现到账类型 | `String` | `3` | `N` | 已确认 | 取现交易必传；T0：当日到账，T1：次工作日到账，D1：次自然日到账；示例值:T0 |
| `request.data.pay_scene` | `request.data.pay_scene` | `—（直接 JSON 路径）` | 场景类型 | `String` | `2` | `N` | 已确认 | 01:标准线上场景； 02:标准线下场景；03:非盈利商户场景；04:缴费行业场景；05:保险行业场景；06:蓝海绿洲活动场景；07:校园餐饮场景；08:k12中小幼行业场景；09:非在线教培行业场景；示例值:01 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | 示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应描述 | `String` | `256` | `Y` | 已确认 | 示例值：成功 |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 原样返回；示例值：[官网示例已脱敏] |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 原样返回,格式为yyyyMMdd；示例值：20091225 |
| `response.data.credit_fee_amt` | `response.data.credit_fee_amt` | `—（直接 JSON 路径）` | 贷记手续费 | `String` | `14` | `N` | 已确认 | 快捷、网银、代扣交易根据实际银行、借贷记取对应借贷记手续费；示例值：1.00 |
| `response.data.debit_fee_amt` | `response.data.debit_fee_amt` | `—（直接 JSON 路径）` | 借记手续费 | `String` | `14` | `N` | 已确认 | 快捷、网银、代扣交易根据实际银行、借贷记取对应借贷记手续费；示例值：1.00 |
| `response.data.fee_amt` | `response.data.fee_amt` | `—（直接 JSON 路径）` | 通用手续费 | `String` | `14` | `N` | 已确认 | 扫码类、刷卡类交易取通用手续费；示例值：1.00 |
| `response.data.hf_seq_id` | `response.data.hf_seq_id` | `—（直接 JSON 路径）` | 全局流水号 | `String` | `128` | `N` | 已确认 | 示例值：00470topo1A221019132207P068ac1362af00000 \| |

## 付款关系提交

- 原始地址：<https://paas.huifu.com/partners/api/doc/yuer/api_acct_fkgxtj.md>
- SHA-256：`884ca71510e55b1d0bc63fbd01dec4770b667901a324dd743c5af4278a5e7c05`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.out_huifu_id` | `request.data.out_huifu_id` | `—（直接 JSON 路径）` | 出款方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式为YYYYMMDD，示例值：20221023 |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.pay_relations[]` | `request.data.pay_relations` | `—（String(JSON Array) 容器）` | 付款关系明细 | `String` | `—` | `Y` | [需要官方确认]：长度 | 付款关系，jsonArray |
| `request.data.pay_relations[].in_huifu_id` | `request.data.pay_relations` | `$[].in_huifu_id` | 入账方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.pay_relations[].apply_type` | `request.data.pay_relations` | `$[].apply_type` | 操作类型 | `String` | `3` | `Y` | 已确认 | ADD:新增；DEL:删除；示例值：ADD |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/yuer/api_acct_fkgxtj.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） ；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务返回描述 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/api/doc/yuer/api_acct_fkgxtj.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：交易成功 |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式为YYYYMMDD，示例值：20221013 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 业务请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.out_huifu_id` | `response.data.out_huifu_id` | `—（直接 JSON 路径）` | 出款方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.pay_relations` | `response.data.pay_relations` | `—（[需要官方确认]：正式说明 jsonArry 的数组编码）` | 付款关系明细 | `String` | `—` | `Y` | [需要官方确认]：长度 | 付款关系，jsonArry |
| `response.data.pay_relations.in_huifu_id` | `response.data.pay_relations` | `—（[需要官方确认]：正式说明 jsonArry 的数组编码）` | 入账方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.pay_relations.apply_type` | `response.data.pay_relations` | `—（[需要官方确认]：正式说明 jsonArry 的数组编码）` | 操作类型 | `String` | `3` | `Y` | 已确认 | ADD:新增；DEL:删除；示例值：ADD |
| `response.data.pay_relations.in_mer_name` | `response.data.pay_relations` | `—（[需要官方确认]：正式说明 jsonArry 的数组编码）` | 入账方商户名称 | `String` | `128` | `N` | 已确认 | 示例值：上海汇付支付服务公司 |
| `response.data.pay_relations.apply_stat` | `response.data.pay_relations` | `—（[需要官方确认]：正式说明 jsonArry 的数组编码）` | 提交状态 | `String` | `1` | `Y` | 已确认 | S=成功；F=失败；示例值：S |
| `response.data.pay_relations.apply_desc` | `response.data.pay_relations` | `—（[需要官方确认]：正式说明 jsonArry 的数组编码）` | 提交状态描述 | `String` | `32` | `N` | 已确认 | 示例值：待删除入账方不在付款关系中 |
| `response.data.confirm_url` | `response.data.confirm_url` | `—（直接 JSON 路径）` | 付款关系确认页面URL | `String` | `128` | `N` | 已确认 | 示例值：https://spin-test.cloudpnr.com/balance/?hfSeqId=0035000topB240314153727P590c0a8309800000 |

## 余额支付发送短信验证码

- 原始地址：<https://paas.huifu.com/partners/api/doc/yuer/api_smscode.md>
- SHA-256：`2e13d8bbb9c8c4f0f9cf0054388e8d4ae8e85309ab0710192fae87fd28bcf87e`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20221023 |
| `request.data.out_huifu_id` | `request.data.out_huifu_id` | `—（直接 JSON 路径）` | 出款方商户号 | `String` | `32` | `Y` | 已确认 | 出款方商户号，示例值：[官网示例已脱敏] |
| `request.data.mobile_no` | `request.data.mobile_no` | `—（直接 JSON 路径）` | 接收验证码的手机号 | `String` | `11` | `Y` | 已确认 | 需为11位数字；示例值：[官网示例已脱敏] |
| `request.data.trans_type` | `request.data.trans_type` | `—（直接 JSON 路径）` | 业务类型 | `String` | `256` | `Y` | 已确认 | 业务类型，ACCT_PAYMENT-余额支付 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/yuer/api_smscode.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） ；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务返回描述 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/api/doc/yuer/api_smscode.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：交易成功 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 业务请求流水号；示例值：[官网示例已脱敏] |

## 余额支付

- 原始地址：<https://paas.huifu.com/partners/api/doc/yuer/api_acctpayzf.md>
- SHA-256：`f0d354f91b4b554caa970a9b67f2f94db9cfeedea77531b112f46c23c7deb943`

### 请求信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 请求数据 | `JSON` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 同步响应信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `512` | `Y` | 已确认 | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 响应内容体 | `JSON` | `—` | `N` | N/A：结构字段长度 | 业务返回参数 |

### 请求 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20221023 |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 发起方商户号 | `String` | `32` | `N` | 已确认 | 该字段已废弃，新接入商户不建议使用；历史商户已用此参数，后续余额支付、查询、退款、交易确认接口仍以参数值为准 |
| `request.data.out_huifu_id` | `request.data.out_huifu_id` | `—（直接 JSON 路径）` | 出款方商户号 | `String` | `32` | `Y` | 已确认 | 出款方商户号，示例值：[官网示例已脱敏] |
| `request.data.ord_amt` | `request.data.ord_amt` | `—（直接 JSON 路径）` | 支付金额 | `String` | `14` | `Y` | 已确认 | 单元：元。保留两位小数。示例值：1.23 |
| `request.data.good_desc` | `request.data.good_desc` | `—（直接 JSON 路径）` | 商品描述 | `String` | `256` | `N` | 已确认 | 示例值：商品描述 |
| `request.data.remark` | `request.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `256` | `N` | 已确认 | 示例值：备注 |
| `request.data.delay_acct_flag` | `request.data.delay_acct_flag` | `—（直接 JSON 路径）` | 是否延迟分账 | `String` | `1` | `N` | 已确认 | Y 为延迟，N为不延迟，不传默认N；示例值：Y |
| `request.data.acct_split_bunch` | `request.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `—` | `Y` | [需要官方确认]：长度 | json格式；余额支付支持付款给多账户。；如余额支付100元，支付给A账户60元，支付给B账户40元。 |
| `request.data.acct_split_bunch.acct_infos[]` | `request.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `—` | `N` | N/A：结构字段长度 | — |
| `request.data.acct_split_bunch.acct_infos[].div_amt` | `request.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 ,最低传入0.01 |
| `request.data.acct_split_bunch.acct_infos[].huifu_id` | `request.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 开户自动生成编号；示例值：[官网示例已脱敏] |
| `request.data.acct_split_bunch.acct_infos[].acct_id` | `request.data.acct_split_bunch` | `$.acct_infos[].acct_id` | 账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，示例值：F00598600 |
| `request.data.acct_split_bunch.acct_infos[].percentage_div` | `request.data.acct_split_bunch` | `$.acct_infos[].percentage_div` | 分账百分比% | `String` | `6` | `N` | 已确认 | 示例值：23.50，表示23.50%。仅在percentage_flag=Y时起作用； acct_infos中全部分账百分比之和必须为100.00%。 |
| `request.data.acct_split_bunch.percentage_flag` | `request.data.acct_split_bunch` | `$.percentage_flag` | 百分比分账标志 | `String` | `1` | `N` | 已确认 | Y:使用百分比分账；示例值：Y |
| `request.data.acct_split_bunch.is_clean_split` | `request.data.acct_split_bunch` | `$.is_clean_split` | 是否净值分账 | `String` | `1` | `N` | 已确认 | Y:使用净值分账，仅在交易手续费由出款方承担且使用百分比分账时起作用；示例值：Y |
| `request.data.risk_check_data` | `request.data.risk_check_data` | `—（String(JSON) 容器）` | 安全信息 | `String` | `—` | `Y` | [需要官方确认]：长度 | json格式；示例: {"subProduct":"","transferType":""} |
| `request.data.risk_check_data.sub_product` | `request.data.risk_check_data` | `$.sub_product` | 产品子类 | `String` | `20` | `N` | 已确认 | 示例值：1 |
| `request.data.risk_check_data.transfer_type` | `request.data.risk_check_data` | `$.transfer_type` | 转账原因 | `String` | `2` | `Y` | 已确认 | 01：卡券推广类；02：卡券核销类；03：消费；04：工资代发；05：分润；06：灵活用工；示例值：01 |
| `request.data.risk_check_data.latitude` | `request.data.risk_check_data` | `$.latitude` | 纬度 | `String` | `32` | `N` | 已确认 | 格式：+表示北纬，-表示南纬。纬度整数位不超过2位，小数位不超过6位。示例值：+37.12；IP地址、经纬度、基站地址最少要送其中一项 |
| `request.data.risk_check_data.longitude` | `request.data.risk_check_data` | `$.longitude` | 经度 | `String` | `32` | `N` | 已确认 | 格式：+表示东经，-表示西经；经度整数位不超过3位，小数位不超过5位；示例值：-121.213；IP地址、经纬度、基站地址最少要送其中一项 |
| `request.data.risk_check_data.base_station` | `request.data.risk_check_data` | `$.base_station` | 基站地址 | `String` | `32` | `N` | 已确认 | 【mcc】+【mnc】+【location_cd】+【lbs_num】；- mcc:移动国家代码，460代表中国；3位长；- mnc：移动网络号码；2位长；- location_cd：位置区域码，16进制，5位长；- lbs_num：基站编号，16进制，5位长；- 注意若位数不足用空格补足；示例值：460001039217563，460（mcc)， 00(mnc)，10392(location_cd)， 17563(lbs_num) ；经纬度、基站地址、IP地址三组信息至少填写一组 |
| `request.data.risk_check_data.ip_addr` | `request.data.risk_check_data` | `$.ip_addr` | IP地址 | `String` | `32` | `N` | 已确认 | 示例值：172.28.52.52；经纬度、基站地址、IP地址三组信息至少填写一组 |
| `request.data.out_acct_id` | `request.data.out_acct_id` | `—（直接 JSON 路径）` | 出款方账户号 | `String` | `32` | `N` | 已确认 | 只支持基本户和现金户；示例值：F00598600 |
| `request.data.fund_type` | `request.data.fund_type` | `—（直接 JSON 路径）` | 资金类型 | `String` | `16` | `C` | 已确认 | 资金类型。支付渠道为中信E管家时，资金类型必填（[详见说明](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)） |
| `request.data.acct_channel` | `request.data.acct_channel` | `—（直接 JSON 路径）` | 支付渠道 | `String` | `8` | `N` | 已确认 | 支付渠道。HUIFU=汇付账务(默认)；ZXE=中信E管家 |
| `request.data.trans_fee_take_flag` | `request.data.trans_fee_take_flag` | `—（直接 JSON 路径）` | 手续费承担方标识 | `String` | `4` | `C` | 已确认 | 余额支付手续费承担方标识；商户余额支付扣收规则为接口指定承担方时必填！枚举值：；OUT：出款方；IN：分账接受方。；示例值：IN |
| `request.data.verify_type` | `request.data.verify_type` | `—（直接 JSON 路径）` | 余额支付安全核验方式 | `String` | `16` | `N` | 已确认 | SMS-短信验证 |
| `request.data.verify_value` | `request.data.verify_value` | `—（直接 JSON 路径）` | 核验值 | `String` | `64` | `C` | 已确认 | verify_type不为空时必填。当verify_type=SMS时，填写用户收到的短信验证码 |
| `request.data.imaxn_pay` | `request.data.imaxn_pay` | `—（直接 JSON 路径）` | 支付类型 | `String` | `10` | `N` | 已确认 | SURETY_PAY:延迟交易 |
| `request.data.imax_pay_callback_url` | `request.data.imax_pay_callback_url` | `—（直接 JSON 路径）` | 验证成功后跳转地址 | `String` | `512` | `N` | 已确认 | 验证成功后跳转地址，无时不显示返回按钮。在交易参与方有用户，且用户是LV3时生效。 |
| `request.data.notify_url` | `request.data.notify_url` | `—（直接 JSON 路径）` | 异步通知地址 | `String` | `256` | `N` | 已确认 | 异步通知地址，在交易参与方有用户，且用户是LV3时生效。 |

### 同步响应 data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/partners/api/doc/yuer/api_acctpayzf.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查） ；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务返回描述 | `String` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/partners/api/doc/yuer/api_acctpayzf.md#业务返回码)（官网相对地址原文：`#业务返回码`）（公共返回码全集：[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)；接口页专属码与公共码需合并排查）；示例值：交易成功 |
| `response.data.req_seq_id` | `response.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `128` | `Y` | 已确认 | 业务请求流水号；示例值：[官网示例已脱敏] |
| `response.data.req_date` | `response.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 请求日期。格式：yyyyMMdd，示例值：20221013 |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `32` | `Y` | 已确认 | 发起方商户号；示例值：[官网示例已脱敏] |
| `response.data.out_huifu_id` | `response.data.out_huifu_id` | `—（直接 JSON 路径）` | 出款商户号 | `String` | `32` | `N` | 已确认 | 出款方商户号；示例值：[官网示例已脱敏] |
| `response.data.ord_amt` | `response.data.ord_amt` | `—（直接 JSON 路径）` | 支付金额 | `String` | `14` | `Y` | 已确认 | 示例值：200.00 |
| `response.data.acct_split_bunch` | `response.data.acct_split_bunch` | `—（String(JSON) 容器）` | 分账对象 | `String` | `—` | `Y` | [需要官方确认]：长度 | json格式。余额支付支持付款给多账户。；如余额支付100元，支付给A账户60元，支付给B账户40元。 |
| `response.data.acct_split_bunch.acct_infos[]` | `response.data.acct_split_bunch` | `$.acct_infos[]` | 分账明细 | `Array` | `—` | `N` | N/A：结构字段长度 | — |
| `response.data.acct_split_bunch.acct_infos[].div_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，灵活用工以异步返回的金额为准示例值：1.00 ,最低传入0.01 |
| `response.data.acct_split_bunch.acct_infos[].huifu_id` | `response.data.acct_split_bunch` | `$.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 开户自动生成编号；示例值：[官网示例已脱敏] |
| `response.data.acct_split_bunch.acct_infos[].acct_id` | `response.data.acct_split_bunch` | `$.acct_infos[].acct_id` | 账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，示例值：F00598600 |
| `response.data.acct_split_bunch.acct_infos[].trans_stat` | `response.data.acct_split_bunch` | `$.acct_infos[].trans_stat` | 交易状态 | `String` | `1` | `N` | 已确认 | P：处理中、S：成功、F：失败；灵工用工场景，以异步返回的交易状态为准示例值：P |
| `response.data.acct_split_bunch.acct_infos[].fee_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].fee_amt` | 手续费金额 | `String` | `14` | `N` | 已确认 | 手续费金额，单位:元。仅在分账接受方承担手续费时返回。 示例值：0.02 |
| `response.data.acct_split_bunch.acct_infos[].unconfirm_amt` | `response.data.acct_split_bunch` | `$.acct_infos[].unconfirm_amt` | 待确认总金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.acct_split_bunch.fee_huifu_id` | `response.data.acct_split_bunch` | `$.fee_huifu_id` | 手续费承担方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.acct_split_bunch.fee_acct_id` | `response.data.acct_split_bunch` | `$.fee_acct_id` | 手续费承担方账户号 | `String` | `32` | `N` | 已确认 | 示例值：F00598600 |
| `response.data.acct_split_bunch.fee_amt` | `response.data.acct_split_bunch` | `$.fee_amt` | 手续费金额 | `String` | `14` | `N` | 已确认 | 单位:元，保留两位小数。示例值：1.23 |
| `response.data.acct_split_bunch.is_clean_split` | `response.data.acct_split_bunch` | `$.is_clean_split` | 是否净值分账 | `String` | `1` | `N` | 已确认 | Y:使用净值分账，仅在交易手续费由出款方承担且使用百分比分账时起作用；示例值：Y |
| `response.data.hf_seq_id` | `response.data.hf_seq_id` | `—（直接 JSON 路径）` | 全局流水号 | `String` | `128` | `N` | 已确认 | 汇付返回流水号；示例值：00470topo1A211015160805P090ac132fef00000 |
| `response.data.good_desc` | `response.data.good_desc` | `—（直接 JSON 路径）` | 商品描述 | `String` | `256` | `N` | 已确认 | 示例值：商品描述 |
| `response.data.trans_stat` | `response.data.trans_stat` | `—（直接 JSON 路径）` | 交易状态 | `String` | `1` | `N` | 已确认 | P:处理中；S：成功；F：失败；示例值：S |
| `response.data.trans_finish_time` | `response.data.trans_finish_time` | `—（直接 JSON 路径）` | 交易完成时间 | `String` | `14` | `N` | 已确认 | 余额支付完成时间，格式：yyyyMMddHHmmss；示例值：20211021163242 |
| `response.data.remark` | `response.data.remark` | `—（直接 JSON 路径）` | 备注 | `String` | `256` | `N` | 已确认 | 示例值：备注 |
| `response.data.out_acct_id` | `response.data.out_acct_id` | `—（直接 JSON 路径）` | 出款方账户号 | `String` | `32` | `N` | 已确认 | 示例值：F00598600 |
| `response.data.fund_type` | `response.data.fund_type` | `—（直接 JSON 路径）` | 资金类型 | `String` | `16` | `C` | 已确认 | 资金类型。支付渠道为中信E管家时，资金类型必填（[详见说明](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)） |
| `response.data.acct_channel` | `response.data.acct_channel` | `—（直接 JSON 路径）` | 支付渠道 | `String` | `8` | `N` | 已确认 | 支付渠道。HUIFU=汇付账务(默认)；ZXE=中信E管家 |
| `response.data.trans_fee_take_flag` | `response.data.trans_fee_take_flag` | `—（直接 JSON 路径）` | 手续费承担方标识 | `String` | `4` | `C` | 已确认 | 余额支付手续费承担方标识；商户余额支付扣收规则为接口指定承担方时必填！枚举值：；OUT：出款方；IN：分账接受方。；示例值：IN |
| `response.data.unconfirm_amt` | `response.data.unconfirm_amt` | `—（直接 JSON 路径）` | 待确认总金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.confirmed_amt` | `response.data.confirmed_amt` | `—（直接 JSON 路径）` | 已确认总金额 | `String` | `14` | `N` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 |
| `response.data.jump_url` | `response.data.jump_url` | `—（直接 JSON 路径）` | 支付密码验证跳转地址 | `String` | `512` | `N` | 已确认 | 交易参与方有用户，且用户是LV3时返回。商户引导用户跳转该地址完成验证。链接有效期5分钟。 |

### 支付异步信封

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.resp_code` | `async.resp_code` | `—（直接 JSON 路径）` | 业务返回码 | `string` | `8` | `Y` | 已确认 | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%e7%ba%bf%e4%b8%8a%e4%ba%a4%e6%98%93%e8%bf%94%e5%9b%9e%e7%a0%81), 示例值：00000000 |
| `async.resp_desc` | `async.resp_desc` | `—（直接 JSON 路径）` | 业务返回描述 | `string` | `512` | `Y` | 已确认 | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%e7%ba%bf%e4%b8%8a%e4%ba%a4%e6%98%93%e8%bf%94%e5%9b%9e%e7%a0%81)；示例值：交易成功 |
| `async.resp_data` | `async.resp_data` | `—（直接 JSON 路径）` | 业务数据 | `string` | `—` | `Y` | [需要官方确认]：长度 | 业务数据，见resp_data |

### 支付异步 resp_data

| 合同定位路径（仅定位，禁止作为 wire/DTO 层级） | wire 字段路径 | String(JSON) 解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | ---: | :---: | --- | --- |
| `async.resp_data.req_date` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 业务请求时间YYYYMMDD（发起余额支付请求时间）YYYYMMDD |
| `async.resp_data.req_seq_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 交易请求流水号 | `String` | `128` | `Y` | 已确认 | 业务请求流水号(发起余额支付请求流水号) |
| `async.resp_data.hf_seq_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 全局流水号 | `String` | `128` | `N` | 已确认 | 汇付返回流水号 |
| `async.resp_data.product_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 产品号 | `String` | `64` | `Y` | 已确认 | 产品号 |
| `async.resp_data.huifu_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 商户号 | `String` | `32` | `Y` | 已确认 | 发起方商户号 |
| `async.resp_data.ord_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 订单金额 | `String` | `14` | `Y` | 已确认 | 订单金额 |
| `async.resp_data.trans_type` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 交易类型 | `String` | `32` | `Y` | 已确认 | 余额支付：ACCT_PAYMENT |
| `async.resp_data.trans_stat` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 交易状态 | `String` | `1` | `Y` | 已确认 | PSF P:处理中；S：成功；F：失败；C：完成。 状态为完成时，需查看分账对象中每个分账的具体状态 |
| `async.resp_data.acct_split_bunch` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账对象 | `Object` | `—` | `Y` | N/A：结构字段长度 | 分账对象，jsonObject字符串 |
| `async.resp_data.acct_split_bunch.acct_infos[]` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账明细 | `Array` | `—` | `N` | N/A：结构字段长度 | — |
| `async.resp_data.acct_split_bunch.acct_infos[].div_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账金额 | `String` | `14` | `Y` | 已确认 | 单位元，需保留小数点后两位，示例值：1.00 ,最低传入0.01 |
| `async.resp_data.acct_split_bunch.acct_infos[].huifu_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账接收方ID | `String` | `32` | `Y` | 已确认 | 开户自动生成编号；示例值：[官网示例已脱敏] |
| `async.resp_data.acct_split_bunch.acct_infos[].acct_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 账户号 | `String` | `32` | `N` | 已确认 | 可指定账户号，仅支持基本户、现金户，不填默认为基本户，示例值：F00598600 |
| `async.resp_data.acct_split_bunch.acct_infos[].trans_stat` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 分账交易状态 | `String` | `1` | `N` | 已确认 | P：处理中、S：成功、F：失败；灵活用工余额支付交易状态为C时，需查看分账交易状态；示例值：P |
| `async.resp_data.acct_split_bunch.acct_infos[].fee_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 手续费金额 | `String` | `14` | `N` | 已确认 | 手续费金额，单位:元。仅在分账接受方承担手续费时返回。 示例值：0.02 |
| `async.resp_data.acct_split_bunch.fee_huifu_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 手续费承担方商户号 | `String` | `32` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `async.resp_data.acct_split_bunch.fee_acct_id` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 手续费承担方账户号 | `String` | `32` | `N` | 已确认 | 示例值：F00598600 |
| `async.resp_data.acct_split_bunch.fee_amt` | `async.resp_data` | `—（[需要官方确认]：外层 resp_data 的 JSON/String(JSON) 编码）` | 手续费金额 | `String` | `14` | `N` | 已确认 | 单位:元，保留两位小数。示例值：1.23 |
