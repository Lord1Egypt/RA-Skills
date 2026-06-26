# Java 适配层

这份文件只讲 Java 接入。
协议规则不在这里重复写。

## 适配范围

| 项目 | 内容 |
| --- | --- |
| 当前适配 SDK | `dg-java-sdk` `3.0.38`（当前仓库示例基线） |
| 当前文档口径 | 当前仓库与 Skill 常量统一为 `3.0.38` |
| 最低运行时 | JDK 1.8+ |
| 初始化入口 | `MerConfig` + `BasePay.initWithMerConfig()` |
| 主要调用方式 | `BasePayClient.request()` |

## 先看哪些文件

- `references/hostingpay-java-sdk-quickstart.md`
- `references/hostingpay-java-tech-spec.md`
- `references/hostingpay-async-webhook.md`
- `references/hostingpay-refund.md`

## Java 特有说明

1. 设置产品号的方法名是 `setProductId()`。
   `dg-java-sdk 3.0.38` 源码已使用正常拼写，不要再生成旧文档中的 `setProcutId()`。
2. Spring Boot 2.x 和 3.x 的 import 不一样。
   2.x 常见是 `javax.*`
   3.x 常见是 `jakarta.*`
3. 当前仓库的异步通知示例使用了 `fastjson`。
   这是 Java 示例选型，不是协议层要求。
4. 有些字段没有独立 setter，要通过 `extendInfoMap` 传入。
5. 退款场景的 `org_req_seq_id` 就属于这一类。
   这个坑已经在退款 skill 里单独标出。
6. `MerConfig.setSkillSource(...)` 直接传 `<skill_source>` 即可；如果项目侧配置 `HUIFU_SKILL_SOURCE`，按原值透传到 `jpt-x-skill-source`，不要再在该字段内补 `sys_id`。
7. 当前 Java SDK 基线如果请求参数里的 `huifu_id` 存在且非空，还会自动补 `jpt-x-skill-huifu_id`；该值必须与本次请求的 `huifu_id` 一致，不要手工写成固定常量。

## 不属于这里的内容

- 签名规则：看 `references/shared-signing-v2.md`
- 异步通知规则：看 `references/shared-async-notify.md`
- 其他语言入口：看 `references/shared-server-sdk-matrix.md`
