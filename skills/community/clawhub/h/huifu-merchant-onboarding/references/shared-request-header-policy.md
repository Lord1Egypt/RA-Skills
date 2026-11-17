# 商户进件请求头策略

## 核心规则

| 请求头 | 来源 |
| --- | --- |
| `jpt-x-skill-source` | 显式合同值；未配置时按当前请求实际加载并参与生成的 Skill 组合生成确定性默认值 |
| SDK 版本头 | 由对应官方 SDK 生成 |

商户十一个与用户九个已有专属 Request 类的 JSON 接口，以及九个商户/AT 扩展接口优先使用对应官方 SDK 主链路，不自行维护签名/HTTP client。商户费率信息查询和新版三个 `/v2/agreement/...` 电子合同接口没有专属类，但可经已核验的官方 SDK 通用入口调用，不能用旧 `V2Invoice*` 类替代。

默认 `skill_source`：

| 当前请求实际参与的 Skill | 默认值 |
| --- | --- |
| 仅 `huifu-merchant-onboarding 1.2.0`，无论使用商户、用户还是扩展接口 | `hfms/1.2.0` |
| `huifu-pay-integration` 与 `huifu-merchant-onboarding` 都参与当前请求 | `hfps/1.6.0;hfms/1.2.0` |

组合顺序固定为支付、进件，中间只使用一个英文分号且不加空格。不得因为两个来源都通过同一个 SDK 配置项传入而丢掉其中一个。调用方显式提供经确认的合同值时原样透传，不再追加默认值或 `sys_id`。

## Java

- 商户十一个与用户九个已有专属 Request 类的 JSON 接口使用公共请求链路，并按 `/v2/merchant/*`、`/v2/user/*` 精确隔离。
- 在任何请求前全局设置 `BasePay.debug = false`。
- Java3.0.41准确包名为`com.huifu.bspay.sdk.opps.core.BasePay`、`com.huifu.bspay.sdk.opps.core.config.MerConfig`和`com.huifu.bspay.sdk.opps.client.BasePayClient`；Request位于`com.huifu.bspay.sdk.opps.core.request`，不得猜用`com.huifu.bspay.sdk.BasePay`。
- 初始化先关闭调试，再构造MerConfig并调用`setSysId(sysId)`、`setProductId(productId)`、`setRsaPrivateKey(privateKey)`、`setRsaPublicKey(publicKey)`、`setSkillSource(skillSource)`，最后`BasePay.initWithMerConfig(config)`（声明throws Exception）。上述方法均已由锁定源码确认，不留不存在的setter疑问或手写HTTP头TODO。配置值取服务端安全配置；skillSource按上表取值。
- 图片 `file_url` 使用 `BasePayClient.request(request, true)` 和 URI 特判的 multipart 文本字段；本地文件使用 `BasePayClient.upload(request, file)`。两种来源互斥，均保留请求签名、跳过响应验签。

## PHP

- 商户十一个与用户九个已有专属 Request 类的 JSON 接口走官方无文件 JSON 路径；本地 PHP 2.0.31 的既有 TLS 校验风险见 `shared-server-sdk-matrix.md`，按本轮要求仅作非阻断提醒，不设修复证明前置条件；继续官方调用链，签验与来源头合同不变。
- 不直接使用 `BsPayClient::postRequest($request, new CURLFile(...))`：该包装层关闭请求签名和响应验签。
- 图片接口允许使用保持 `data` 加签的通用 POST 或自写 HTTPS multipart 适配器；`file_url` 模式也必须发 multipart 文本字段，不能照搬无文件 JSON 分支。

## Python

- 当前 SDK 为 `2.0.28`，以下构造器和图片结论已按本地源码复核。`jpt-sdk_version: python_2.0.28` 由实际 SDK 生成，不为了匹配文档版本手写或覆盖它；其他版本差异按 `shared-server-sdk-matrix.md` 提醒核对，不阻断明确部分。
- 已核验 Python 2.0.28 的 `MerConfig` 第五参数是 `sign_type`，第六参数才是来源。使用 `MerConfig(private_key=private_key, public_key=public_key, sys_id=sys_id, product_id=product_id, sign_type="RSA", jpt_x_skill_source=skill_source)`，生成代码六参全部使用关键字；前四参源码顺序为private_key/public_key/sys_id/product_id，不得猜成sys_id/product_id/private_key/public_key，避免密钥进入外层系统号字段。
- 图片专用 Request 仍存在字段、扩展参数、文件键和签验缺陷，不能直接调用。底层 `dg_sdk.core.request_tools.request_post` 可显式设置 `need_sign=True`；`DGTools.request_post` 没有此关键字形参。补齐官网字段并使用顶层 `file` multipart 键后才可用于本地文件模式；`file_url` 模式使用符合相同 multipart 合同的通用 POST/自写 HTTPS 适配器。

## 明确禁止

1. 除 `/v2/supplementary/picture` 的 PHP/Python 受控降级外，绕开 SDK 另写签名或 HTTP 主链路。
2. 在两个 Skill 都参与当前请求时只保留一个来源值，或把组合顺序、分号格式交给模型自由发挥。
3. 把图片 JSON、multipart 和通知协议当成同一报文规则。
