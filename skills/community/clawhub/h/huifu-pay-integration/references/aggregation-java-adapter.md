# Java 适配层

这份文件只讲 Java 接入。  
协议规则不在这里重复写。

## 适配范围

| 项目 | 内容 |
| --- | --- |
| 当前适配 SDK | `dg-lightning-sdk` `1.0.5` |
| 最低运行时 | JDK 1.8+ |
| 初始化入口 | `MerConfig` + `BasePay.initWithMerConfig()` |
| 主要调用方式 | `Factory.Payment.Common()` |

## 先看哪些文件

- `references/aggregation-java-sdk-quickstart.md`
- `references/aggregation-java-tech-spec.md`
- `references/aggregation-async-webhook.md`

## Java 特有说明

1. Lightning SDK 的产品号方法名是 `setProductId()`，这里拼写正常。
2. Spring Boot 2.x 和 3.x 的 import 不一样。
   2.x 常见是 `javax.annotation.PostConstruct`
   3.x 常见是 `jakarta.annotation.PostConstruct`
3. 当前仓库的异步通知示例使用了 `fastjson`。
   这是 Java 示例选型，不是协议层要求。
4. `method_expand`、`acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info` 这类字段，仍然建议先在业务层建对象，再在 SDK 边界统一序列化。
5. `T_JSAPI`、`T_MINIAPP`、`T_APP`、`T_MICROPAY`、`A_JSAPI`、`A_NATIVE`、`A_MICROPAY`、`U_JSAPI`、`U_NATIVE`、`U_MICROPAY` 这些值不是 `method_expand` 的 key；`method_expand` 的 JSON 内容直接是当前场景对象本身。
6. `tx_metadata` 本身不作为请求字段上送；交易能力扩展按能力名直接传 `acct_split_bunch`、`terminal_device_data`、`combinedpay_data`、`combinedpay_data_fee_info`、`trans_fee_allowance_info`。
7. `MerConfig.setSkillSource(...)` 直接传 `<skill_source>` 即可；聚合支付要求的 `sys_id` 仍通过独立请求头 `sys_id` / `jpt-sys_id` 传递，`jpt-x-skill-source` 只透传来源值。
8. 当前 Java SDK 基线如果请求参数里的 `huifu_id` 存在且非空，还会自动补 `jpt-x-skill-huifu_id`；该值必须与本次请求的 `huifu_id` 一致，不要手工写成固定常量。

## 不属于这里的内容

- 签名规则：看 `references/shared-signing-v2.md`
- 异步通知规则：看 `references/shared-async-notify.md`
- 其他语言入口：看 `references/shared-server-sdk-matrix.md`
