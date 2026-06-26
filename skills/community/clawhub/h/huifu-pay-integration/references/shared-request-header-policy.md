# 请求头策略

本文件定义当前 Skill 包在 `1.3.0` 版本下的统一请求头约束。

## 目录

- 核心规则
- Java、PHP 与 Python 的确认结论
- 托管支付请求头
- 聚合支付请求头
- 脚本语言约束
- 常规 HTTP 与报文约束
- 明确禁止

## 核心规则

无论是官方 Java SDK、官方 PHP SDK、官方 Python SDK，还是自行封装 HTTP 请求，都必须补齐与官方 SDK 一致的请求头。

`HUIFU_SKILL_SOURCE` 的最终上送值保持为业务配置传入的 `<skill_source>`，不再自动拼接 `sys_id`：

```text
<skill_source>
```

如果业务方显式配置 `HUIFU_SKILL_SOURCE`、`skill_source` 或 `jpt_x_skill_source`，HTTP 层应原样透传该值。聚合支付里的 `sys_id` 由各官方 SDK 按自己的实现上送：Java Lightning SDK 会放到独立请求头 `sys_id` / `jpt-sys_id`，PHP 官方 SDK 则仍放在签名前请求体顶层字段，Python 官方 SDK 由 `MerConfig` 管理。

`jpt-x-skill-source` 属于 HTTP 请求头，不属于业务报文字段本身，不要把它写进 `data`。

## Java、PHP 与 Python 的确认结论

- 当前 Java SDK 基线会把 `MerConfig.setSkillSource(...)` 的值按 `<skill_source>` 原样透传到 `jpt-x-skill-source`
- 如果当前 Java 请求参数里的 `huifu_id` 存在且非空，SDK 还会自动补 `jpt-x-skill-huifu_id: <data.huifu_id>`
- 当前 Skill 包对齐的官方 PHP SDK 主链路会在 `MerConfig.skill_source` 非空时，于 `BsPay::post()` 主链路自动补 `jpt-x-skill-source`
- 如果当前 PHP 请求参数里的 `huifu_id` 存在且非空，且 `MerConfig.skill_source` 已配置，SDK 还会自动补 `jpt-x-skill-huifu_id: <data.huifu_id>`
- `BsPaySdk\core\Payment` 和 `BsPayClient::postRequest()` 都走这条官方 `BsPay::post()` 主链路，不需要再为来源头打补丁
- PHP 侧只有在绕开官方 SDK 主链路时，才需要手动补 `jpt-x-skill-source` / `jpt-x-skill-huifu_id`
- 当前 Python SDK 基线会把 `MerConfig.jpt_x_skill_source` 的值透传到 `jpt-x-skill-source`
- 当前 Python SDK 基线会从最终请求参数 `data.huifu_id` 自动推导 `jpt-x-skill-huifu_id`
- 当前 Python SDK 的 `MerConfig` 不接收 `jpt_x_skill_huifu_id`；业务侧必须保证每次 request 对象中的 `huifu_id` 是本次真实商户号
- Python SDK 的 `jpt-sdk_version` 请求头为 `python_2.0.22`

源码核对提示：

- 当前本地 PHP SDK 在补 `jpt-x-skill-huifu_id` 前直接读取 `$request_params['huifu_id']`；如果某接口请求参数没有 `huifu_id` 且运行环境把 PHP warning 升级为异常，应按 SDK 源码修正或升级 SDK，不要通过关闭 warning、吞异常或写固定 `huifu_id` 来掩盖问题
- 当前 Python SDK 的 `jpt-x-skill-huifu_id` 来自 `ApiRequest._build_request_info()` 对最终请求参数执行的 `params.get("huifu_id", "")`；多商户或代调用时不要配置固定 huifu 头字段，而要逐次设置 request 的 `huifu_id`

## 托管支付请求头

适用接口：

- `v2/trade/hosting/payment/preorder`
- `v2/trade/hosting/payment/queryorderinfo`
- `v2/trade/hosting/payment/splitpay/query`
- `v2/trade/hosting/payment/close`
- `v2/trade/hosting/payment/htRefund`
- `v2/trade/hosting/payment/queryRefundInfo`
- `v2/trade/check/filequery`

Java 官方 SDK 请求头：

| Header | 值 |
| --- | --- |
| `sdk_version` | `javaSDK_3.0.38` |
| `jpt-x-skill-source` | `<skill_source>` |

条件性 `huifu_id` 约束：

- 当前 Java SDK 基线会在 `params.huifu_id` 存在且非空时自动补 `jpt-x-skill-huifu_id: <data.huifu_id>`

PHP 官方 SDK 请求头：

| Header | 值 |
| --- | --- |
| `sdk_version` | `php#v2.0.27` |
| `charset` | `UTF-8` |
| `jpt-x-skill-source` | `MerConfig.skill_source` 非空时自动带 `<skill_source>` |
| `jpt-x-skill-huifu_id` | `MerConfig.skill_source` 已配置且 `params.huifu_id` 存在且非空时自动带 `<data.huifu_id>` |

Python 官方 SDK 请求头：

| Header | 值 |
| --- | --- |
| `jpt-sdk_version` | `python_2.0.22` |
| `jpt-x-skill-source` | `MerConfig.jpt_x_skill_source` |
| `jpt-x-skill-huifu_id` | SDK 从最终请求参数 `data.huifu_id` 自动取值；没有 `huifu_id` 时为空 |
| `Content-Type` | 非文件请求为 `application/json;charset=utf-8` |

SDK 版本请求头是 SDK 自动生成的 HTTP 请求头，不作为手写值或安装包下载依据；当前 Skill 的 PHP / Python 安装包基线见 `references/shared-server-sdk-matrix.md`。

## 聚合支付请求头

适用接口：

- `v4/trade/payment/create`
- `v4/trade/payment/scanpay/query`
- `v2/trade/payment/scanpay/close`
- `v2/trade/payment/scanpay/closequery`
- `v4/trade/payment/scanpay/refund`
- `v4/trade/payment/scanpay/refundquery`
- `v2/trade/check/filequery`

Java Lightning SDK 请求头：

| Header | 值 |
| --- | --- |
| `sdk_version` | `javaSDK_lightning_1.0.5` |
| `jpt-sdk_version` | `javaSDK_lightning_1.0.5` |
| `sys_id` | 当前调用方 `sys_id` |
| `jpt-sys_id` | 当前调用方 `sys_id` |
| `jpt-x-skill-source` | `<skill_source>` |

条件性 `huifu_id` 约束：

- 当前 Java SDK 基线会在 `params.huifu_id` 存在且非空时自动补 `jpt-x-skill-huifu_id: <data.huifu_id>`

PHP 官方 SDK 请求头：

| Header | 值 |
| --- | --- |
| `sdk_version` | `php#v2.0.27` |
| `charset` | `UTF-8` |
| `jpt-x-skill-source` | `MerConfig.skill_source` 非空时自动带 `<skill_source>` |
| `jpt-x-skill-huifu_id` | `MerConfig.skill_source` 已配置且 `params.huifu_id` 存在且非空时自动带 `<data.huifu_id>` |

Python 官方 SDK 请求头：

| Header | 值 |
| --- | --- |
| `jpt-sdk_version` | `python_2.0.22` |
| `jpt-x-skill-source` | `MerConfig.jpt_x_skill_source` |
| `jpt-x-skill-huifu_id` | SDK 从最终请求参数 `data.huifu_id` 自动取值；没有 `huifu_id` 时为空 |
| `Content-Type` | 非文件请求为 `application/json;charset=utf-8` |

说明：

- PHP 官方 SDK 不会额外生成 `jpt-sdk_version`、`sys_id`、`jpt-sys_id` 请求头
- Python 官方 SDK 会生成 `jpt-sdk_version`，但不会额外生成 `sys_id`、`jpt-sys_id` 请求头
- `sys_id` 仍由 SDK 放入签名前请求体顶层字段，不要误写成 PHP / Python 请求头模板

## 脚本语言约束

先区分三类情况，不要把 PHP / Python 官方 SDK 路径和“没有自动补头能力的脚本语言”混为一谈。

### PHP 官方 SDK 路径

如果当前使用官方 `huifurepo/dg-php-sdk`，默认不需要手动补 `jpt-x-skill-source` / `jpt-x-skill-huifu_id`。当前推荐顺序是：

1. 业务调用仍使用官方 `huifurepo/dg-php-sdk`
2. 聚合支付核心主链路优先 `BsPaySdk\core\Payment`；聚合对账与托管支付优先 `BsPayClient::postRequest()`
3. 在 `MerConfig` 初始化时显式配置 `skill_source`
4. 当前 Skill 包不再内置 PHP 模板资产；只有在绕开官方 SDK 主链路时，才按本文件手动对齐来源头

### Python 官方 SDK 路径

如果当前使用官方 `dg-sdk`，默认不需要绕开 SDK 手写签名和 HTTP client。当前推荐顺序是：

1. 业务调用仍使用官方 `dg_sdk`
2. 聚合支付核心主链路优先 `dg_sdk.Payment`；聚合对账与托管支付优先 request 类 `.post({})`
3. 初始化 `MerConfig` 时显式传入 `jpt_x_skill_source`
4. 每次业务 request 对象必须设置本次真实 `huifu_id`，SDK 会据此生成 `jpt-x-skill-huifu_id`
5. 差异排查时先比对本地请求头、签名串和官方 SDK 实际源码，不引入自维护 client

### 其他脚本语言或非官方调用路径

如果接入方使用 Go、Node.js 等没有官方 SDK 自动补头能力的脚本语言，或者 PHP / Python 虽然有官方 SDK 但当前绕开了官方主链路，就必须在 HTTP 客户端层手动补齐上述来源头。

手动补头时只对齐正在模拟的官方 SDK 请求头口径，不要混用 Java Lightning、PHP 和 Python 的 SDK 版本请求头。聚合支付 PHP 路径不要生成 Java Lightning 专属的 `jpt-sdk_version`、`sys_id`、`jpt-sys_id` 请求头；Python 路径只保留 Python SDK 自己的 `jpt-sdk_version`，不要补 `sys_id`、`jpt-sys_id`。

## 常规 HTTP 与报文约束

下面这些是基础 HTTP / 报文约束，不替代上面的 SDK 对齐头：

- `Content-Type: application/json;charset=UTF-8`
- 请求报文顶层字段位置固定为 `sys_id`、`product_id`、`sign`、`data`
- URL 参数中不要携带 JSON 数据
- 请求体和响应体应尽量避免超过 `10MB`；文件场景优先走文件服务
- 业务接口避免返回空响应体

## 明确禁止

1. 只传请求体，不补来源相关 SDK 请求头
2. 只在部分接口补来源头，其他接口漏掉
3. 聚合支付沿用托管支付头，或托管支付沿用聚合支付头
4. 把 `jpt-x-skill-huifu_id` 写成无条件必带，或让它和当前请求里的 `huifu_id` 脱钩
5. 为了补来源头，绕开官方 PHP SDK 另写一套签名 / HTTP 主链路
6. 缺头后静默忽略，靠默认值兜底
7. Python 使用官方 SDK 时，误把 `jpt-x-skill-huifu_id` 当作业务 `data` 字段或继续按旧版构造 `MerConfig(..., jpt_x_skill_source, jpt_x_skill_huifu_id)`
8. Python 安装或版本核对失败时，静默安装不带版本约束的 `dg-sdk` 或降级
