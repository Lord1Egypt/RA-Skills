# 商户进件 V2 签名与验签

## JSON 接口

- 请求顶层为 `sys_id`、`product_id`、`sign`、`data`。
- 业务字段位于 `data`；使用官方 SDK 生成签名，不自行排序或拼接。
- 仅字段合同明确为 `String(JSON Object)` / `String(JSON Array)` 时序列化为字符串；原生 `Object` / `Array` 保持原生类型交给官方 SDK，不能因嵌套或旧版类型而统一字符串化。
- 同步响应包含 `sign` 时使用 SDK 验签，再解析业务状态。
- 关闭 Java 调试日志不影响签名或验签。
- 已核验 Python `2.0.28` 源码提供 RSA/SM2 分支，仍明确 `sign_type="RSA"`；没有官方接口及账户依据不自动切换算法。Python 初始化的来源使用 `jpt_x_skill_source` 关键字，不能占用第五位置的算法参数；实际项目版本差异按 `shared-server-sdk-matrix.md` 提醒核对。

## 图片例外

- Java `file_url` 模式通过图片 URI 特判发送 multipart 文本字段。
- 末参必须使用 `isPage=true`：请求签名保留，响应验签跳过。
- 已核验 PHP `2.0.31` / Python `2.0.28` 专用生成实现不可直接使用，但允许为 `/v2/supplementary/picture` 生成受控通用 POST 或自写 HTTPS 适配器：对排序后的 `data` JSON 使用 V2 RSA 规则加签，multipart 文本字段固定为 `sys_id`、`product_id`、`data`、`sign`，本地文件额外使用顶层 `file`。Python 图片缺陷已按本版源码复核，不是仅依据旧版推断。
- 该例外只放开传输实现，不放开免签、关闭 TLS、猜测响应字段或自动重试；响应含 `sign` 时按 V2 规则验签，不含时只保留原始响应边界。

## 通知例外

审核、逐业务和电子协议通知不能套用支付 `notify_url` 或控台 Webhook 规则。ACK、验签原文、HTTP、超时和重试未明确时，按 `shared-overview.md` 的开发提醒给出对应官方文档，建议核对或咨询汇付官方、汇付开发者交流沟通群；继续 Controller、协议适配接口和测试骨架，将未知部分留为 TODO/待填策略。不得伪造验签成功、ACK 或重试规则，也不因这些待确认项停止其余开发。

## 禁止

- 不把官网示例签名、密钥或请求数据复制进代码。
- 不因同步 `resp_code` 成功推断审核或逐业务终态。
- 不在没有官方通知样本时猜测签名字段和 ACK。
