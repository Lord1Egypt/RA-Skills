# 商户进件服务端 SDK 能力矩阵

## 目录

- [版本基线](#版本基线)
- [十一个已有专属类的 JSON 接口](#十一个已有专属类的-json-接口)
- [费率查询缺口](#费率查询缺口)
- [官方 SDK 通用调用入口](#官方-sdk-通用调用入口)
- [同步返回形状](#同步返回形状)
- [图片上传](#图片上传)
- [调试日志硬停](#调试日志硬停)
- [官方 SDK-first 与图片例外](#官方-sdk-first-与图片例外)
- [语言边界](#语言边界)

## 版本基线

本轮 SDK 核验日期为 `2026-10-08`，由官方固定Git提交及PyPI制品恢复并锁定源码；API 来源为 `2026-11-09`。Java 读取 SDK 子模块 pom，PHP 读取 `SDK_VERSION`，Python 读取 `DGClient.__version__`。Git源码核验不等于对应Maven/Composer制品已发布；Python2.0.28已核验PyPI制品。源码证据不代表真实网关联调通过。商户进件 skill 为 1.2.0。

Python 当前 SDK 为 `2.0.28`，源码来自官方 PyPI 2.0.28 制品，版本声明为 `dg_client.py` 中的 `DGClient.__version__`。下方构造器、请求头、路由和图片边界已按该源码复核；不代表真实网关联调成功。实际项目使用其他版本时核对对应源码，将未明确差异留 TODO 并继续明确部分；疑问可咨询汇付官方或汇付开发者交流沟通群，不新增开发硬停。

官方固定提交、归档SHA、关键文件SHA和源码树SHA记于维护者SDK锁；本页来源只标明本次维护的核验来源；安装本 Skill 不要求拥有维护仓库或相同 SDK 目录，实际项目按自己的依赖布局核对版本。

| SDK | 当前版本 | 源码结论 |
| --- | --- | --- |
| Java `dg-java-sdk` | `3.0.41` | 十一个 JSON Request 类可用；图片接口有专用 Request、URI 特判和 `upload(...)` 入口 |
| PHP `huifurepo/dg-php-sdk` | `2.0.31` | 十一个 JSON Request 类可用；图片生成产物存在，但没有满足合同的可用调用路径 |
| Python `dg-sdk` / `dg_sdk` | `2.0.28` | 有十一个 JSON Request 模块；图片生成产物仍存在实现缺陷，不能直接使用 |

## 十一个已有专属类的 JSON 接口

三语言均包含以下 Request：

- `V2MerchantBasicdataEntRequest`
- `V2MerchantBasicdataIndvRequest`
- `V2MerchantBusiOpenRequest`
- `V2MerchantBasicdataQueryRequest`
- `V2MerchantBasicdataStatusQueryRequest`
- `V2MerchantBusiModifyRequest`
- `V2MerchantBasicdataModifyRequest`
- `V2MerchantBusiModifyBusistatusRequest`
- `V2MerchantBasicdataSmsSendRequest`
- `V2MerchantBusiMultifeeConfigRequest`：精确路由 `/v2/merchant/busi/multiFee/config`
- `V2MerchantBusiMultifeeQueryRequest`：精确路由 `/v2/merchant/busi/multiFee/query`

共同规则：

- Java准确import、MerConfig凭据/source setter及Python全参数关键字初始化统一见`shared-request-header-policy.md`；生成代码必须读取该语言小节，不猜包名或构造顺序。
- 只使用官方 Request/SDK 主链路；不得为了提供三语言等价产物改走手写 HTTP+签名客户端。
- 业务侧提供当天唯一的 `req_date/req_seq_id`。
- 请求 `data` 保留签名；同步响应有 `sign` 时验签。
- SDK 类存在不证明接口权限、材料条件或审核结果。
- 多费率配置类只声明 `req_seq_id/req_date/huifu_id`；`wx_conf_list/ali_conf_list` 使用 exact-key 扩展映射，值必须是各自只序列化一次的 JSON Array 字符串。Java/PHP/Python 的扩展合并都可能覆盖声明字段，扩展映射必须拒绝这三个定位键。
- 多费率配置查询类同样只声明三个定位字段；可选 `fee_sign` 使用 exact-key 扩展映射，并且扩展映射只能包含该键，不能传入配置接口的数组字段或覆盖定位字段。

## 费率查询缺口

三语言锁定 SDK 中均未找到 `/v2/merchant/fee-rate/query` 的专属 Request 类或路由常量。不得声称 SDK 已有专属类覆盖商户费率信息查询，也不得用支付费率、详情查询或名称相近的类替代。字段解释仍读取 `merchant-onboarding-rate-query.md` 与完整字段目录；可运行代码可经下方“官方 SDK 通用调用入口”生成，因无类型化封装兜底，字段合同必须逐项对照执行。

Python2.0.28在2026-10-10真实费率查询中因响应数字重序列化导致验签失败；Java3.0.41官方通用入口同接口实测通过。Python受影响响应不能视为可完成联调，保留异常拒绝路径或采用已验证Java路线；原因与本次响应类型差异见 `merchant-onboarding-rate-query.md` 的实际联调章节。该局部问题不阻断其他已验证接口，也不授权跳过验签或改写SDK。

## 官方 SDK 通用调用入口

- 官方 SDK 自带通用调用入口：Java `BasePayClient.request(params, "v2.merchant.fee-rate.query", false)` 内部把功能码的点替换为 slash；PHP `BsPayClient::postRequest(['funcCode' => 'v2/merchant/fee-rate/query', 'params' => $params])` 明确支持数组；Python `DGTools.request_post('/v2/merchant/fee-rate/query', params)` 默认保留请求签名与同步验签。它们复用官方 SDK 的同一传输链，不得声称具有专属类型封装。常规 JSON 不设置 Java `isPage=true` 或 PHP `$tag=true` 来跳过验签。
- Python公开入口为`import dg_sdk`后调用`dg_sdk.DGTools.request_post(...)`，根包从`dg_tools.py`导出DGTools；锁定源码不存在`dg_sdk.utils`，不得猜用该模块。生成代码的导入与签名须按实际源码核对。
- Python专属Request也由根包导出，使用`dg_sdk.<表中精确Request类>()`；实际模块是单数`dg_sdk.request`，不存在复数`dg_sdk.requests`。实例声明字段直接赋值（如`request.req_seq_id=req_seq_id`、`request.req_date=req_date`、`request.huifu_id=merchant_huifu_id`），不要留成注释后直接调用post。构造MerConfig后必须赋给`dg_sdk.DGClient.mer_config`；仅有未绑定的局部config不能初始化SDK。
- SDK 没有某接口的专属 Request/路由时，可通过该入口生成可运行代码，不限于图片接口，也不属于受控降级；因无类型化封装兜底，字段名、类型、长度、必填和 String(JSON) 编码必须逐项对照字段合同构造。
- 仍不得据此宣称 SDK 已有专属类支持，也不得用名称相近的专属类替代；离开官方 SDK 的手写 HTTP 客户端继续按“官方 SDK-first 与图片例外”执行。

## 同步返回形状

网关信封路径与SDK返回值分开建模，锁定版本的常规JSON调用如下：

| 语言 | 返回值与读取方式 | 失败边界 |
| --- | --- | --- |
| Java 3.0.41 | `Map<String,Object> data = BasePayClient.request(request, false)` 已是验签后的业务data；直接 `data.get("resp_code")` 或 `data.get("url")`，不得再取 `get("data")` | 验签失败抛异常；图片/page返回原始包装，不能套用此结论 |
| PHP 2.0.31 | `postRequest` / `Payment` 返回SDK响应对象，不是array；先检查非null且 `!result->isError()`，再对 `result->getRspDatas()` 的信封取一次 `['data']` | 验签失败仍可持有原响应，必须先检查isError；缺data或类型错误拒绝处理，不使用空数组伪装成功 |
| Python 2.0.28 | 专属 `.post(...)` / `DGTools.request_post(...)` 在正常签名响应下返回业务data，直接读 `result['resp_code']`，不再取一层data | 验签失败抛异常；非200、非JSON或无sign分支可返回原始对象/文本/信封，SDK返回不等于已验签成功；异常或未验签结果不能用于业务状态更新 |

先检查传输/SDK错误和响应可信性，再检查业务码和接口状态；不得只凭返回对象存在或HTTP成功认定业务成功。Python费率查询的局部异常见该接口原子页。

## 图片上传

| 语言 | `file_url` | 本地文件 | 总结论 |
| --- | --- | --- | --- |
| Java | `BasePayClient.request(request, true)`；图片 URI 特判为 multipart 文本字段 | `BasePayClient.upload(request, file)`；multipart 文件字段为 `file` | 支持；两种来源互斥，请求签名保留，响应验签跳过 |
| PHP | 无文件分支只是通用 JSON POST，不能直接用于 `file_url` | `BsPayClient` 的 `CURLFile` 包装分支关闭请求签名和响应验签；Demo 同时传互斥来源 | 官方专用实现不可用；允许符合图片 wire 的通用 POST/自写 HTTPS multipart 降级 |
| Python | 无文件 `DGTools.request_post` 是 JSON，不能直接用于 `file_url` | 专用 Request 忽略扩展参数、漏字段、使用错误文件键、关闭签验；底层通用 POST 可显式开启加签并传 `file` | 官方专用实现不可用；允许符合图片 wire 的底层通用 POST/自写 HTTPS multipart 降级 |

图片能力结论必须区分“官方专用 SDK 支持”和“受控降级可实现”。单独存在 `V2SupplementaryPictureRequest`、路由常量或通用 POST 方法不算前者；PHP/Python 可使用后者，但只能用于 `/v2/supplementary/picture`，并严格保持 multipart、`data` 加签、互斥、TLS 和响应信任边界。

本次 Python 分发目录不含 Demo；上述结论来自实际 Request 与底层入口，不把旧 Demo 的缺陷当作本版证据，也不把缺少 Demo 视为接口不可开发。

## 调试日志硬停

- Java `BasePay.debug` 默认 `true`，会输出私钥、签名和请求数据；必须在进程初始化阶段、任何请求前全局设置为 `false`，且不得并发临时切换。
- PHP SDK 自带 `init.php` 默认 `DEBUG=false`，但官方 `BsPayDemo/loader.php` 和 `Composer/BsPayConfig.php` 会在 SDK 初始化前定义 `DEBUG=true`。开启后 `BsPayRequestV2` 会记录含 `rsa_merch_private_key` 的 `MerConfig`、完整请求体与完整响应。
- PHP 联调/生产必须在加载 SDK、Demo/Composer 配置和调用 `BsPay::init` 之前固定 `DEBUG=false`；不得使用 Demo loader，启动检查必须拒绝已被定义为 `true` 的进程。可先生成包含启动拒绝检查的安全初始化骨架，无需用户先提供既有配置证明；未通过检查的进程不得执行真实请求。

## 官方 SDK-first 与图片例外

- 通用 Java `3.0.41` 源码使用默认 TLS 工厂，Python `2.0.28` 保留 requests 默认校验；按官方 Request/Client 生成调用。PHP `2.0.31` 当前源码 `BsPayRequestV2.php:30` 明确设置 `CURLOPT_SSL_VERIFYPEER=false`，旧确认不能覆盖此本地证据。
- PHP 的 `CURLOPT_SSL_VERIFYPEER=false` 保留为非阻断风险提醒；按用户本轮要求，不因该已知本地 SDK 问题停止开发/联调代码生成，也不要求先取得修复证明。继续官方 Request/Client 或已核验通用入口，可提示开发者查阅对应 SDK/官方文档，不清楚时咨询汇付官方或汇付开发者交流沟通群。不得声称 TLS 已修复，不擅自修改 SDK 或以手写 HTTP 规避；新生成的适配代码保留正常证书链与主机名校验，不主动加入 trust-all、`verify=false`。
- 常规接口不得用 `HttpClient`、OkHttp、`HttpURLConnection`、Guzzle、`curl_*`、通用 POST 包装或自实现签名/验签客户端替代官方 SDK，即使任务只称“技术链路验证”。唯一例外是 `/v2/supplementary/picture` 的 PHP/Python 受控降级；该例外必须满足图片专项 multipart、`data` 加签、TLS 与日志合同，Java 仍使用官方 SDK。本条限制的是离开官方 SDK 的手写实现；官方 SDK 自带的通用调用入口仍走 SDK 内部签名、验签、请求头与 TLS 链路，不属于上述替代，可用于无专属 Request 的常规接口。
- 多语言任务分别使用三种官方 SDK；不得只让 Python 用 SDK，再为 Java/PHP 生成手写客户端。

## 语言边界

- Python `2.0.28` 必须用 `MerConfig(private_key=private_key, public_key=public_key, sys_id=sys_id, product_id=product_id, sign_type="RSA", jpt_x_skill_source=skill_source)`；源码位置顺序为private_key/public_key/sys_id/product_id/sign_type/jpt_x_skill_source；生成代码六参全部使用关键字，禁止猜位置顺序或把密钥放进sys_id/product_id。SDK 的 SM2 分支不改变本轮 RSA 合同；共享 `ApiRequest` 类级状态也不保证并发安全。

- 企业/个人进件没有 `data.huifu_id`。
- SDK 连接重试不是进件业务重试；未知业务重试、图片响应文件标识、服务端拉取 URL 结果和通知协议按 `shared-overview.md` 的“文档疑义与开发提醒”处理。继续已明确的调用链，未知部分用 TODO/配置隔离，不猜测或等待官方答复才开始开发。
