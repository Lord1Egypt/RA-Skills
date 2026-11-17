# H5、PC 预下单

> 依据用户提供的汇付官方文档整理，接口更新时间为 `2026.10.13`。当前文档只保留总览、导航和顶层摘要，详细字段已拆到子文档中，避免单文件超过 500 行。


## 目录

- 接口概览
- 应用场景
- 官方业务开通及配置要点
- 文档拆分导航
- 接入要点
- SDK 映射
- 顶层请求参数速览
- 返回参数速览
- 请求示例
- 同步成功示例
- 文档勘误与实现备注

## 接口概览

| 属性 | 值 |
|------|-----|
| 请求方式 | `POST` |
| 接口地址 | `https://api.huifu.com/v2/trade/hosting/payment/preorder` |
| 场景类型 | H5、PC、动态二维码 |
| `pre_order_type` | `1` |
| SDK Request 类 | `V2TradeHostingPaymentPreorderH5Request` |
| 报文格式 | `application/json` |

## 应用场景

- H5：后端预下单拿到 `jump_url`，前端主动跳转完成支付。
- PC：后端预下单拿到 `jump_url`，前端在新窗口或当前页跳转完成支付。
- 动态二维码：把 `jump_url` 转为二维码，支持微信、支付宝、云闪付、浏览器扫码支付。
- 官方 PC 体验页：<https://paas.huifu.com/checkout/demo/pc/goodsDetail.html?type=2>
- 自有渠道对接：<https://paas.huifu.com/open/doc/api/#/cpjs/api_cpjs_hostingdoc>

## 官方业务开通及配置要点

- 先在合作伙伴控台创建 H5 / PC 托管项目，并记录留存真实 `project_id`。
- 托管项目里勾选的支付方式，前提是商户已经开通对应支付方式；未开通时无法选中。
- 使用微信支付时，官方产品文档要求先配置微信授权域名 `api.huifu.com/hostingH5/`。
- `notify_url` 必须满足官方回调地址约束：`http/https`、不支持重定向、URL 不带参数、自定义端口在 `8000-9005`、成功处理后返回 `200`。
- `callback_url` 只是支付完成后的页面回跳地址，最终结果仍要依赖异步通知或主动查询。

## 文档拆分导航

| 文档 | 内容 |
|------|------|
| `references/hostingpay-preorder-h5-pc.md` | 总览、场景说明、SDK 映射、示例、勘误 |
| `references/hostingpay-preorder-h5-pc-request.md` | 公共请求参数、`data` 顶层字段、`acct_split_bunch`、`hosting_data`、`biz_info` |
| `references/hostingpay-preorder-h5-pc-channel.md` | `wx_data`、`alipay_data`、`dy_data`、`unionpay_data`、`terminal_device_data`、`largeamt_data` |
| `references/hostingpay-preorder-h5-pc-response.md` | 同步返回公共参数、同步 `data`、异步 `resp_data` 顶层字段 |
| `references/hostingpay-preorder-h5-pc-response-channel.md` | `wx_response`、`alipay_response`、`unionpay_response`、`dy_response`、分账与手续费补贴对象 |
| `references/hostingpay-preorder-h5-pc-errors.md` | 常见错误码与排查要点 |

## 接入要点

- `req_seq_id` 在同一 `huifu_id` 下当天必须唯一。
- 预下单成功后，务必保存 `req_date` 和 `req_seq_id`，后续查询、关单、退款都会用到。
- `trans_type` 传单个值时会直达指定支付页；传多个值或不传时进入汇付收银台。
- `notify_url` 才是交易结果回调入口；`callback_url` 只是支付完成后的前端跳转地址。
- `time_expire` 不传时默认 10 分钟。营销高峰或高并发场景建议显式缩短，减少超时订单堆积。
- 指定网银交易类型时，部分浏览器首次跳转银行页需要允许弹窗。

## SDK 映射

`V2TradeHostingPaymentPreorderH5Request` 可直接设置的核心字段如下：

| 字段 | setter | 必填 | 说明 |
|------|--------|------|------|
| `req_date` | `setReqDate()` | Y | 请求日期，格式 `yyyyMMdd` |
| `req_seq_id` | `setReqSeqId()` | Y | 请求流水号 |
| `huifu_id` | `setHuifuId()` | Y | 商户号 |
| `acct_id` | `setAcctId()` | N | 收款汇付账户号 |
| `trans_amt` | `setTransAmt()` | Y | 交易金额 |
| `goods_desc` | `setGoodsDesc()` | Y | 商品描述 |
| `pre_order_type` | `setPreOrderType()` | Y | H5/PC 固定传 `1` |
| `hosting_data` | `setHostingData()` | Y | 统一收银台扩展参数集合，JSON 字符串 |
| `fee_sign` | `setFeeSign()` | N | 手续费场景标识 |

其他扩展字段统一通过 `setExtendInfo(Map<String, Object>)` 传入。

## 顶层请求参数速览

完整字段见 `references/hostingpay-preorder-h5-pc-request.md` 和 `references/hostingpay-preorder-h5-pc-channel.md`。

| 参数 | 必填 | 说明 |
|------|------|------|
| `req_date` | Y | 请求日期，`yyyyMMdd` |
| `req_seq_id` | Y | 请求流水号 |
| `huifu_id` | Y | 商户号 |
| `trans_amt` | Y | 交易金额，单位元 |
| `goods_desc` | Y | 商品描述 |
| `pre_order_type` | Y | 固定为 `1` |
| `hosting_data` | Y | 托管项目标题、项目号、回调地址等 |
| `notify_url` | N | 交易异步通知地址 |
| `trans_type` | N | 指定支付方式；多值进入收银台 |
| `acct_split_bunch` | N | 分账对象 |
| `biz_info` | N | 买家实名/年龄等校验信息 |
| `wx_data` | N | 微信场景扩展 |
| `alipay_data` | N | 支付宝场景扩展 |
| `dy_data` | N | 抖音场景扩展 |
| `unionpay_data` | N | 银联场景扩展 |
| `terminal_device_data` | N | 报备机具号 |
| `largeamt_data` | N | 大额支付校验要素 |

## 返回参数速览

### 同步返回 `data`

完整字段见 `references/hostingpay-preorder-h5-pc-response.md`。

| 参数 | 必填 | 说明 |
|------|------|------|
| `resp_code` | Y | 业务响应码 |
| `resp_desc` | Y | 业务响应信息 |
| `req_date` | Y | 原样返回 |
| `req_seq_id` | Y | 原样返回 |
| `huifu_id` | Y | 原样返回 |
| `pre_order_type` | Y | 原样返回 |
| `pre_order_id` | Y | 预下单 ID |
| `goods_desc` | Y | 商品描述 |
| `jump_url` | Y | 支付跳转链接 |
| `usage_type` | N | 订单类型 |
| `trans_type` | N | 实际预下单交易类型 |
| `hosting_data` | Y | 托管扩展参数 |
| `current_time` | Y | 系统响应时间 |
| `time_expire` | Y | 失效时间 |

### 异步返回 `resp_data`

完整字段见 `references/hostingpay-preorder-h5-pc-response.md` 和 `references/hostingpay-preorder-h5-pc-response-channel.md`。

| 参数 | 必填 | 说明 |
|------|------|------|
| `resp_code` | Y | 业务返回码 |
| `resp_desc` | Y | 业务返回信息 |
| `req_seq_id` | Y | 原样返回 |
| `req_date` | Y | 原样返回 |
| `hf_seq_id` | N | 汇付全局流水号 |
| `huifu_id` | Y | 商户号 |
| `trans_type` | N | 实际支付渠道类型 |
| `trans_amt` | N | 交易金额 |
| `settlement_amt` | N | 结算金额 |
| `trans_stat` | N | `S` 成功，`F` 失败 |
| `end_time` | N | 支付完成时间 |
| `acct_date` | N | 入账时间 |
| `is_div` | Y | 是否分账交易 |
| `acct_split_bunch` | N | 分账结果 |
| `is_delay_acct` | Y | 是否延时交易 |
| `fee_amount` | N | 手续费金额 |
| `wx_response` | N | 微信通道扩展响应 |
| `alipay_response` | N | 支付宝通道扩展响应 |
| `unionpay_response` | N | 银联通道扩展响应 |
| `dy_response` | N | 抖音通道扩展响应 |

## 请求示例

```json
{
  "sys_id": "6666000108840829",
  "data": {
    "checkout_id": "",
    "delay_acct_flag": "N",
    "hosting_data": "{\"callback_url\":\"https://paas.huifu.com\",\"project_id\":\"PROJECTID2023101225142567\",\"project_title\":\"收银台标题\",\"private_info\":\"商户私有信息test\"}",
    "req_seq_id": "20240514163256046l9da4ecgqugo7h",
    "biz_info": "{\"payer_check_wx\":{\"limit_payer\":\"ADULT\",\"real_name_flag\":\"Y\"},\"person_payer\":{\"cert_type\":\"IDENTITY_CARD\",\"cert_no\":\"<ENCRYPTED_CERT_NO_FROM_CLIENT>\",\"name\":\"张三\",\"mobile\":\"<ENCRYPTED_MOBILE_FROM_CLIENT>\"},\"payer_check_ali\":{\"fix_buyer\":\"F\",\"need_check_info\":\"T\",\"min_age\":\"12\"}}",
    "req_date": "20240514",
    "trans_amt": "0.10",
    "huifu_id": "6666000109133323",
    "goods_desc": "支付托管消费",
    "pre_order_type": "1",
    "notify_url": "https://callback.service.com/xx",
    "acct_split_bunch": "{\"acct_infos\":[{\"huifu_id\":\"6666000111546360\",\"div_amt\":\"0.08\"}]}"
  },
  "product_id": "YYZY",
  "sign": "<SDK_AUTOGENERATED_SIGNATURE>"
}
```

## 同步成功示例

```json
{
  "data": {
    "resp_code": "00000000",
    "resp_desc": "交易成功",
    "req_date": "20220424",
    "req_seq_id": "20220424561166000",
    "huifu_id": "6666000111546360",
    "jump_url": "https://api.huifu.com/hostingh5/?jump_id=H20220424140825009124199014&huifu_id=6666000111546360"
  }
}
```

## 文档勘误与实现备注

- 官方请求示例中带有 `checkout_id`，但参数表没有定义该字段；当前 skill 不将其视为正式接入参数。
- 2026-10-10官网已明确通知 `trans_finish_time:String(13)` 为毫秒时间戳；`end_time:String(14)` 仍为 `yyyyMMddHHmmss`，分别解析。
- 2026-10-10官网 `wx_response.cash_fee/coupon_fee` 明确为 String(12)，保留金额字符串并按十进制处理；旧Int/示例冲突已关闭。
- `unionpay_data.pid_info` 正式为 String，说明仅“服务商信息”，没有声明JSON编码；其子表只作合同定位路径，编码留 `[需要官方确认]`。
- `callback_url` 只能控制支付后的页面跳转，不能作为支付成功判定依据；最终结果仍以异步通知或主动查询为准。

## 2026-10-25 官网更新同步

本地当前来源SHA-256：`60381ee32ab1529d05b881b2c944f8c3f130de17a7ad35a44977b166a7986eec`。

本轮新增合单/子单请求、查询或通知字段；同名父容器按本接口和方向建模。官网通知中的`sub_trams_amt`拼写原样保留，不更改为其他字段名；split_fee_details的Object/String/数组语义也不得跨接口外推。完整嵌套类型、长度、条件和解码路径见 `payment-complete-field-catalog.md` 对应接口。

| 新增完整合同路径 | 中文名 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `async.resp_data.sub_orders_response[]` | 子单信息 | `String` | `—` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].acct_date` | 子单入账日期 | `String` | `8` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].acct_split_bunch` | 分账对象 | `String` | `—` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].acct_split_bunch.acct_infos[]` | 分账明细 | `String` | `—` | `Y` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].acct_split_bunch.acct_infos[].acct_id` | 分账接收方账户号 | `String` | `9` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].acct_split_bunch.acct_infos[].div_amt` | 分账金额 | `String` | `14` | `Y` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].acct_split_bunch.acct_infos[].huifu_id` | 分账接收方ID | `String` | `32` | `Y` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].acct_stat` | 子单账务状态 | `String` | `1` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].fee_infos` | 交易手续费信息 | `String` | `—` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_acct_id` | 手续费扣款账户号 | `String` | `9` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_amount` | 手续费金额 | `String` | `16` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_flag` | 手续费扣款标志 | `Integer` | `1` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_formula` | 手续费计算公式 | `String` | `512` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_huifu_id` | 手续费扣款商户号 | `String` | `32` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].fee_infos.fee_rec_type` | 手续费扣取方式 | `Integer` | `1` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].fund_freeze_stat` | 资金冻结状态 | `String` | `16` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].is_div` | 是否分账交易 | `String` | `1` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].split_fee_info` | 分账手续费信息 | `String` | `—` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_details` | 分账手续费信息 | `String` | `—` | `Y` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_details.split_fee_acct_id` | 分账手续费承担方账号 | `String` | `9` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_details.split_fee_amt` | 分账手续费金额(元) | `String` | `16` | `Y` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_details.split_fee_huifu_id` | 分账手续费承担方商户号 | `String` | `32` | `Y` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].split_fee_info.split_fee_flag` | 分账手续费扣款标志 | `Integer` | `1` | `Y` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].split_fee_info.total_split_fee_amt` | 分账手续费总金额(元) | `String` | `14` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].sub_acct_id` | 子单账户号 | `String` | `9` | `Y` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].sub_hf_seq_id` | 子单全局流水号 | `String` | `128` | `Y` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].sub_huifu_id` | 子单商户号 | `String` | `32` | `Y` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].sub_remark` | 子单备注信息 | `String` | `255` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].sub_req_seq_id` | 子单请求流水号 | `String` | `128` | `Y` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].sub_settlement_amt` | 子单结算金额 | `String` | `14` | `N` | 条件与完整原文见对应完整目录 |
| `async.resp_data.sub_orders_response[].sub_trams_amt` | 子单交易金额 | `String` | `14` | `Y` | 条件与完整原文见对应完整目录 |
| `request.data.merge_pay_flag` | 是否合单支付 | `String` | `1` | `N` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[]` | 子单信息列表 | `String` | `—` | `N` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].delay_acct_flag` | 是否延迟交易 | `String` | `1` | `N` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].sub_acct_id` | 子单账户号 | `String` | `9` | `N` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].sub_huifu_id` | 子单商户号 | `String` | `32` | `Y` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].sub_remark` | 子单备注 | `String` | `255` | `N` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].sub_req_seq_id` | 子单请求流水号 | `String` | `128` | `Y` | 条件与完整原文见对应完整目录 |
| `request.data.sub_orders_request[].sub_trans_amt` | 子单交易金额 | `String` | `18` | `Y` | 条件与完整原文见对应完整目录 |
