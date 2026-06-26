# 聚合下单请求参数

> 本文只覆盖请求侧参数；渠道扩展参数请继续阅读各渠道分册。
> 
> Java SDK 复核基线：`TradePaymentCreateRequest` 独立字段包含 `trade_type`、`method_expand`、`acct_split_bunch`、`terminal_device_data`；`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info` 作为请求顶层扩展字段通过 `addExtendInfo(...)` / `optional(...)` 注入。`tx_metadata` 本身不作为请求字段上送，文档中的交易能力扩展按能力名直接传对应字段。


## 目录

- 公共请求参数
- `data` 顶层字段
- `trade_type` 枚举
- 官方开发指引确认的关键字段来源
- `limit_pay_type` 枚举
- 请求示例
- 请求侧实现备注
- 参数校验与构造约束

## 公共请求参数

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `sys_id` | 系统号 | String | 32 | Y | 渠道商 / 商户的 `huifu_id` |
| `product_id` | 产品号 | String | 32 | Y | 汇付分配的产品号 |
| `sign` | 加签结果 | String | 512 | Y | 对整个请求报文签名 |
| `data` | 数据 | Json | - | Y | 业务请求参数 |

> 强制请求头约束：
> - 必须带 `jpt-x-skill-source: <skill_source>`
> - 如果当前按 PHP 接入，由于本页请求 `data` 明确包含 `huifu_id`，还必须带 `jpt-x-skill-huifu_id: <data.huifu_id>`
> - 当前 Skill 包对齐的官方 PHP SDK 主链路在 `MerConfig.skill_source` 已配置时，会自动带 `jpt-x-skill-source`，并在当前请求 `huifu_id` 存在且非空时自动带 `jpt-x-skill-huifu_id`
> - 当前 Java SDK 基线也会在请求 `data` 明确包含 `huifu_id` 时自动带 `jpt-x-skill-huifu_id: <data.huifu_id>`
> - 这两项属于 HTTP 请求头，不要误写进 `data`；完整口径见 `references/shared-request-header-policy.md`

## `data` 顶层字段

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `req_date` | 请求日期 | String | 8 | N | `yyyyMMdd` |
| `req_seq_id` | 请求流水号 | String | 128 | Y | 请求流水号 |
| `huifu_id` | 商户号 | String | 32 | Y | 商户号 |
| `trade_type` | 交易类型 | String | 16 | Y | 见下方枚举 |
| `trans_amt` | 交易金额 | String | 14 | Y | 单位元，保留两位小数，最低 `0.01` |
| `goods_desc` | 商品描述 | String | 128 | Y | 商品描述 |
| `remark` | 备注 | String | 255 | N | 原样返回 |
| `acct_id` | 账户号 | String | 9 | N | 指定收款账户号，仅支持基本户、现金户 |
| `time_expire` | 交易有效期 | String | 14 | N | `yyyyMMddHHmmss`；建议大于 1 分钟；不传时微信/支付宝通常按约 2 小时后关单处理 |
| `delay_acct_flag` | 延迟标识 | String | 1 | N | `Y`=延迟，`N`=不延迟，默认 `N` |
| `fee_flag` | 手续费扣款标识 | Integer | 1 | N | `1`=外扣，`2`=内扣 |
| `acct_split_bunch` | 分账对象 | String(JSON Object) | - | C | 顶层请求字段；有分账权限时传 |
| `terminal_device_data` | 设备信息 | String(JSON Object) | - | C | 顶层请求字段；反扫支付时必填，终端报备场景也常用 |
| `limit_pay_type` | 禁用支付方式 | String | 128 | N | 见下方枚举 |
| `channel_no` | 渠道号 | String | 32 | N | 自有渠道号 |
| `pay_scene` | 场景类型 | String | 2 | N | 微信业务开通类型 |
| `term_div_coupon_type` | 分账遇到优惠的处理规则 | String | 2 | N | `1`=按比例分，`2`=按顺序保障，`3`=只给交易商户 |
| `fq_mer_discount_flag` | 商户贴息标记 | String | 1 | N | `Y`=商户全额贴息，`P`=商户部分贴息；`P` 需配合支付宝侧 `ali_business_params` 传贴息明细 |
| `notify_url` | 异步通知地址 | String | 504 | N | HTTP 或 HTTPS 地址 |
| `method_expand` | 交易类型扩展参数 | String(JSON Object) | - | C | 按 `trade_type` 选择当前渠道对象；JSON 内容直接是当前场景参数本身，不再额外包一层 `T_JSAPI` / `A_JSAPI` / `U_MICROPAY` 这类 key |
| `combinedpay_data` | 补贴支付信息 | String(JSON Array) | - | C | 顶层扩展字段；有补贴支付场景时传，Java SDK 通过 `addExtendInfo(...)` / `optional(...)` 注入 |
| `combinedpay_data_fee_info` | 补贴支付手续费承担方信息 | String(JSON Object) | - | C | 顶层扩展字段；有明确承担方时传，Java SDK 通过 `addExtendInfo(...)` / `optional(...)` 注入 |
| `trans_fee_allowance_info` | 手续费补贴信息 | String(JSON Object) | - | C | 顶层扩展字段；有手续费补贴场景时传，Java SDK 通过 `addExtendInfo(...)` / `optional(...)` 注入 |

## `trade_type` 枚举

| 枚举值 | 场景 | 详细文档 |
|--------|------|----------|
| `T_JSAPI` | 微信公众号支付 | `references/aggregation-order-method-wechat.md` |
| `T_MINIAPP` | 微信小程序支付 | `references/aggregation-order-method-wechat.md` |
| `T_APP` | 微信 APP 支付 | `references/aggregation-order-method-wechat.md` |
| `T_MICROPAY` | 微信付款码反扫 | `references/aggregation-order-method-wechat.md` |
| `A_JSAPI` | 支付宝 JS 支付 | `references/aggregation-order-method-alipay.md` |
| `A_NATIVE` | 支付宝正扫 | `references/aggregation-order-method-alipay.md` |
| `A_MICROPAY` | 支付宝付款码反扫 | `references/aggregation-order-method-alipay.md` |
| `U_JSAPI` | 银联 JS 支付 | `references/aggregation-order-method-unionpay.md` |
| `U_NATIVE` | 银联正扫 | `references/aggregation-order-method-unionpay.md` |
| `U_MICROPAY` | 银联付款码反扫 | `references/aggregation-order-method-unionpay.md` |

## 官方开发指引确认的关键字段来源

| 场景 | 关键字段 | 来源要求 |
|------|---------|---------|
| `T_JSAPI` | `sub_openid` | 必须通过当前公众号 `appid` 的网页授权流程获取 |
| `T_MINIAPP` | `sub_openid` | 必须通过当前小程序 `sub_appid` 获取，不能与其他小程序混用 |
| `A_JSAPI` | `buyer_id` | 必须通过支付宝 `user_id` 获取流程拿到 |
| `U_JSAPI` | `user_id` | 必须先走银联网页授权拿 `auth_code`，再换取 `user_id` |
| `T_MICROPAY` / `A_MICROPAY` / `U_MICROPAY` | `auth_code` | 必须来自扫码设备实时采集，不得写死在配置里 |
| `U_JSAPI` | `customer_ip` | 必须来自真实客户端 IP，不能用示例值或固定内网地址代替 |

## `limit_pay_type` 枚举

| 取值 | 说明 |
|------|------|
| `NO_CREDIT` | 禁用信用卡；使用花呗支付时不能禁用信用卡 |
| `BALANCE` | 禁用支付宝余额 |
| `MONEY_FUND` | 禁用支付宝余额宝 |
| `BANK_PAY` | 禁用网银，仅支持支付宝 |
| `DEBIT_CARD_EXPRESS` | 禁用借记卡快捷，仅支持支付宝 |
| `CREDIT_CARD_EXPRESS` | 禁用信用卡快捷，仅支持支付宝 |
| `CREDIT_CARD_CARTOON` | 禁用信用卡卡通，仅支持支付宝 |
| `CARTOON` | 禁用卡通，仅支持支付宝 |
| `PCREDIT` | 禁用支付宝花呗 |
| `PCREDIT_PAY_INSTALLMENT` | 禁用支付宝花呗分期 |
| `CREDIT_GROUP` | 禁用支付宝信用支付类型组合 |
| `COUPON` | 禁用支付宝红包 |
| `POINT` | 禁用支付宝积分 |
| `PROMOTION` | 禁用支付宝优惠 |
| `VOUCHER` | 禁用支付宝营销券 |
| `MDISCOUNT` | 禁用支付宝商户优惠 |
| `HONEY_PAY` | 禁用支付宝亲密付 |
| `MCARD` | 禁用支付宝商户预存卡 |
| `PCARD` | 禁用支付宝个人预存卡 |

## 请求示例

```json
{
  "sys_id": "6666000103334211",
  "product_id": "MCS",
  "data": {
    "req_date": "20250828",
    "req_seq_id": "202508281506304989897129zz",
    "huifu_id": "6666000108604566",
    "trade_type": "U_MICROPAY",
    "trans_amt": "0.01",
    "goods_desc": "银联反扫测试",
    "delay_acct_flag": "N",
    "method_expand": "{\"qr_code\":\"union-542323asdas12351111\",\"user_id\":\"union4f4f5a5f5a5f5111\",\"auth_code\":\"6236171220051893816\"}",
    "terminal_device_data": "{\"device_ip\":\"221.11.52.52\",\"mer_device_type\":\"11\",\"devs_id\":\"SPINTP35142090061111\"}",
    "combinedpay_data": "[{\"huifu_id\":\"6666000108609999\",\"user_type\":\"merchant\",\"acct_id\":\"F00598652\",\"amount\":\"0.02\"}]",
    "combinedpay_data_fee_info": "{\"huifu_id\":\"6666000108609999\",\"acct_id\":\"F00598652\"}",
    "trans_fee_allowance_info": "{\"allowance_fee_amt\":\"0.01\"}"
  },
  "sign": "RSA签名"
}
```

## 请求侧实现备注

- 官方把 `req_date` 标成 N，但 SDK 示例和后续查询 / 回调都依赖它，实务上建议始终传。
- 官方把 `method_expand` 标成 Y，但真实是否有强制子字段取决于 `trade_type`。
- `acct_split_bunch`、`terminal_device_data` 是请求顶层字段，不要再包进 `tx_metadata`。
- 开发确认后，`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info` 也按请求顶层扩展字段处理，不要再包进 `tx_metadata`。
- `tx_metadata` 本身不作为请求字段上送；完整边界见 `references/aggregation-order-tx-metadata.md`。

## 参数校验与构造约束

- `trade_type` 先决定场景，再构造该场景自己的 `method_expand` 对象。
- `method_expand` 的 JSON 内容就是当前渠道对象本身，不要再写成带 `T_MINIAPP`、`A_JSAPI` 等支付类型包装 key 的结构。
- `method_expand`、`acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info` 在业务层不要设计成裸字符串；优先用 DTO / `Map` / `List` / `ObjectNode` 建模。
- 只在调用 SDK 前做一次 JSON 序列化，不要在代码里手写长字符串常量。
- 对象一旦出现，就要保证子结构完整；不要只传一个空壳对象或半截 JSON。
- `sub_openid`、`buyer_id`、`user_id`、`auth_code`、`customer_ip`、`devs_id` 这类值若无明确来源，应先暴露缺口，不要让模型补示例值。

推荐写法：

```java
request.setTradeType(cmd.getTradeType());
request.setMethodExpand(objectMapper.writeValueAsString(buildMethodExpand(cmd)));

if (cmd.getAcctSplitBunch() != null) {
    request.setAcctSplitBunch(objectMapper.writeValueAsString(cmd.getAcctSplitBunch()));
}
if (cmd.getTerminalDeviceData() != null) {
    request.setTerminalDeviceData(objectMapper.writeValueAsString(cmd.getTerminalDeviceData()));
}
if (cmd.getCombinedpayData() != null) {
    request.addExtendInfo("combinedpay_data", objectMapper.writeValueAsString(cmd.getCombinedpayData()));
}
if (cmd.getCombinedpayDataFeeInfo() != null) {
    request.addExtendInfo("combinedpay_data_fee_info", objectMapper.writeValueAsString(cmd.getCombinedpayDataFeeInfo()));
}
if (cmd.getTransFeeAllowanceInfo() != null) {
    request.addExtendInfo("trans_fee_allowance_info", objectMapper.writeValueAsString(cmd.getTransFeeAllowanceInfo()));
}
```
