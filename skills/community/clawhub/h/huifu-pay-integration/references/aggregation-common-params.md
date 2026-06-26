# 公共参数说明


## 目录

- 公共请求参数
- 公共返回参数
- 业务数据通用字段
- 交易状态枚举（trans_stat）
- 金额格式
- 日期时间格式
- 流水号规则
- 支付类型详解
- 标准字段与格式约束
- 结算术语
- 手续费术语

## 公共请求参数

所有聚合支付 API 请求的外层参数：

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|-------|------|------|------|------|
| sys_id | 系统号 | String | 32 | Y | 渠道商/代理商/商户的 huifu_id |
| product_id | 产品号 | String | 32 | Y | 汇付分配的产品号，如 `MYPAY`、`YYZY` |
| sign | 加签结果 | String | 512 | Y | SDK 自动生成，无需手动处理 |
| data | 请求数据 | JSON | - | Y | 业务请求参数 |

> 强制请求头约束：
> - 必须带 `jpt-x-skill-source: <skill_source>`
> - 如果当前按 PHP 接入，且接口业务报文里存在 `huifu_id`，还必须带 `jpt-x-skill-huifu_id: <data.huifu_id>`
> - 当前 Skill 包对齐的官方 PHP SDK 主链路在 `MerConfig.skill_source` 已配置时，会自动带 `jpt-x-skill-source`，并在当前请求 `huifu_id` 存在且非空时自动带 `jpt-x-skill-huifu_id`
> - 当前 Java SDK 基线也会在接口业务报文里 `huifu_id` 存在且非空时自动带 `jpt-x-skill-huifu_id: <data.huifu_id>`
> - 这两项属于 HTTP 请求头，不属于 `data` 字段本身；完整口径见 `references/shared-request-header-policy.md`

### sys_id 说明

| 主体类型 | sys_id 填写 |
|---------|-----------|
| 渠道商/代理商 | 渠道商/代理商的 huifu_id |
| 直连商户 | 商户自身的 huifu_id |

> **sys_id vs huifu_id**：`sys_id` 是外层公共参数，标识调用方身份；`huifu_id` 是 `data` 内业务参数，标识交易商户。渠道商模式下两者不同，直连商户模式下两者相同。

## 公共返回参数

| 参数 | 中文名 | 类型 | 长度 | 说明 |
|------|-------|------|------|------|
| sign | 签名 | String | 512 | SDK 自动验证 |
| data | 响应内容体 | JSON | - | 业务返回参数 |

## 业务数据通用字段

以下字段在多数业务接口的 `data` 中出现：

| 参数 | 中文名 | 类型 | 说明 |
|------|-------|------|------|
| resp_code | 业务响应码 | String(8) | 接口受理返回码，用于排查；订单终态仍看 `trans_stat` 和查单结果 |
| resp_desc | 业务响应信息 | String(512) | 响应描述 |
| huifu_id | 商户号 | String(32) | 商户 huifu_id |
| req_date | 请求日期 | String(8) | 格式 yyyyMMdd |
| req_seq_id | 请求流水号 | String(128) | 同一 huifu_id 下当天唯一 |
| hf_seq_id | 汇付全局流水号 | String(128) | 汇付生成的全局唯一标识 |

## 交易状态枚举（trans_stat）

| 值 | 含义 | 处理方式 |
|---|------|---------|
| I | 初始 | 罕见状态，联系汇付技术人员 |
| P | 处理中 | 等待异步通知或轮询查询接口 |
| S | 成功 | 交易完成 |
| F | 失败 | 交易失败，可重新发起 |

## 金额格式

- **单位**：元（CNY）
- **精度**：保留两位小数
- **最小值**：0.01
- **示例**：`"1.00"`、`"100.50"`、`"0.01"`

## 日期时间格式

| 格式 | 说明 | 示例 |
|------|------|------|
| yyyyMMdd | 日期 | `20250320` |
| yyyyMMddHHmmss | 日期时间（14位） | `20250320143000` |
| HHmmss | 时间（6位） | `143000` |

## 流水号规则

| 字段 | 规则 | 说明 |
|------|------|------|
| req_seq_id | 同一 huifu_id 下当天唯一 | 商户自行生成 |
| hf_seq_id | 全局唯一 | 汇付返回，用于查询/退款 |
| org_req_seq_id | 原交易的 req_seq_id | 用于关联原交易 |
| org_hf_seq_id | 原交易的 hf_seq_id | 可替代 org_req_seq_id |

## 支付类型详解

### 正扫 vs 反扫

| 类型 | 说明 | 适用 trade_type |
|------|------|----------------|
| 正扫 (NATIVE) | 商户生成二维码，用户扫码支付 | A_NATIVE、U_NATIVE |
| 反扫 (MICROPAY) | 用户出示付款码，商户扫码收款 | T_MICROPAY、A_MICROPAY、U_MICROPAY |
| JS 支付 (JSAPI) | 在对应 APP 内通过 JS 调起支付 | T_JSAPI、A_JSAPI、U_JSAPI |
| 小程序 (MINIAPP) | 微信小程序内支付 | T_MINIAPP |
| APP 支付 | 原生 APP 内支付 | T_APP |

### method_expand 参数

不同 trade_type 需要传入不同的 `method_expand` 扩展参数。注意，`trade_type` 是场景选择器，这 10 个枚举值本身不是 `method_expand` 的 key。`method_expand` 的 JSON 内容直接是当前场景对象本身。

| trade_type | method_expand 必填字段 | 说明 |
|-----------|----------------------|------|
| T_JSAPI | sub_appid, sub_openid | 微信公众号 AppID 和用户 OpenID |
| T_MINIAPP | sub_appid, sub_openid | 微信小程序 AppID 和用户 OpenID |
| T_APP | sub_appid | 微信开放平台 AppID |
| T_MICROPAY | auth_code | 用户付款码 |
| A_JSAPI | buyer_id 或 buyer_logon_id | 支付宝买家 ID / 账号，二选一 |
| A_NATIVE | - | 无需额外参数 |
| A_MICROPAY | auth_code | 用户付款码 |
| U_JSAPI | user_id, qr_code, customer_ip | 银联 JS 常见关键字段 |
| U_NATIVE | - | 无需额外参数 |
| U_MICROPAY | auth_code | 用户付款码 |

## 标准字段与格式约束

- 请求和返回统一使用 JSON，字符编码统一为 `UTF-8`。
- 参数命名统一采用下划线命名法，如 `req_seq_id`、`trade_type`。
- 金额单位统一为元，保留两位小数。
- 时间统一按北京时间（东八区）处理。
- 数值字段在 API 层尽量使用字符串承载，避免精度损失。

## 结算术语

| 术语 | 说明 |
|------|------|
| T1 自动结算 | 前一工作日周期内余额结算到银行卡 |
| D1 自动结算 | 前一自然日周期内余额结算到银行卡 |
| D0 取现 | 发起后通常 2 小时内到账 |
| DM 取现 | 不包含在途资金的快速取现方式 |

## 手续费术语

| 术语 | 说明 |
|------|------|
| 实时收取 | 默认模式，按交易费率实时计算并收取 |
| 手续费内扣 | 从交易金额中扣收手续费 |
| 手续费外扣 | 从指定主体或账户额外扣收手续费 |
