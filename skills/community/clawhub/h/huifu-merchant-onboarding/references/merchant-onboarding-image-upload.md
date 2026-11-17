# 商户进件图片上传

## 目录

- 适用范围
- 已确认的请求合同
- SDK 源码核验结论
- Java 官方 SDK 调用
- PHP / Python 受控降级
- 公共请求头与安全边界
- 仍需要官方确认

## 适用范围

本文件处理商户进件材料的文件标识获取。官方来源：[图片上传](https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json)；本地活动快照 `2026-11-09`，原文 SHA-256 为 `2fcb84dd1cfe0260cfa3d49b79174d2e7b8a287cdf860faa62011bfc1e8472dd`。当前锁定 SDK 中，只有 Java `dg-java-sdk 3.0.41` 具有与该接口匹配的完整专用实现；PHP `2.0.31` 与 Python `2.0.28` 的专用生成实现不可直接使用，但本接口允许按已核验 Java wire 生成受控通用 POST 或自写 HTTPS multipart 适配器。

Python 当前 SDK 为 `2.0.28`，本页缺陷已按该版实际 Request 和底层调用入口重新复核，不是由旧版外推。其他安装版本差异按 `shared-server-sdk-matrix.md` 核对；可继续已明确的 multipart 合同、适配接口和测试，未明确部分留 TODO，不阻断整体开发。

## 已确认的请求合同

- 官方 JSON 只给 URI `v2/supplementary/picture` 和元数据 `sign=true`，未给 HTTP method、host、Content-Type 或响应字段；Java SDK 源码使用 POST，但不得把 POST 说成该 JSON 明示的合同。
- 官方 `requestDemo` 含 `sys_id`、`product_id`、`data`，但没有顶层 `sign`；这与元数据 `sign=true` 并列保留。实际调用不手写包络，以锁定 Java SDK 的加签实现为准。
- 官方 JSON 的八个可见请求路径（三个仅见于 `requestDemo` 的顶层路径和五个正式 `data` 参数）及其证据边界见 `merchant-onboarding-complete-field-catalog.md` 的“图片上传”；本轮 `requestDemo` 已删除顶层 `file`，不再将它列为正式目录路径；文件流仍见于互斥说明及 Java SDK，需单列 SDK 传输证据，不能将其类型、长度和必填性补为正式字段。
- 图片示例顶层 `sys_id/product_id/data` 的正式类型、长度及必填列未声明，目录保留 `—`；不得用常规JSON接口的String(32)或必填规则填补为本接口正式元数据。
- `data` 必填 `req_seq_id:String(32)`、`req_date:String(8)`（`yyyyMMdd`）、`file_type:String(32)`；`huifu_id:String(18)` 可选；`file_url:String(512)` 标为 C，选择 URL 模式时提供，与文件流模式互斥。
- `data.file_url` 与顶层 `file` 文件流互斥；官网未说明二者都空是否合法。生成实际调用时必须选择一个真实文件来源。
- 未开户或未确认目标商户号时 `huifu_id` 可为空。官网明确不支持填写企业/个人用户开户返回的用户号；只能在已确认是渠道或一级代理商直属商户 ID 时传入。
- 图片支持 JPG、BMP、PNG，单张最大 2MB；其他文件最大 10MB。`file_type` 必须按官方文件类型表和目标进件字段选择。
- 容量上限不是格式准入合同。生成校验器时先核对目标材料的已确认格式白名单及实际文件内容，再选择容量上限；不得将所有未知后缀自动作为“非图片、10MB”接受。官网仅明确 JPG/BMP/PNG，JPEG 扩展名及其他格式的接受条件未确认，不能自行扩充已确认列表；未知格式只暂停该文件上传，继续已明确的适配骨架。
- 校验必须同时覆盖真实文件名后缀和内容：仅magic/MIME识别成JPG不能放行 `.jpeg` 或未知后缀，也不能通过改名绕过准入；后缀或内容未确认、二者不一致时暂停该文件。URL模式同样需要受控来源提供已核实的文件名与内容证据，不能只从URL末尾或Content-Type推断。
- 可调用代码必须在网络请求前真正执行上述格式、容量和来源校验；写注释或把普通Path/string命名为 `validated` 不构成验证。校验器未接通时必须抛错，不能留TODO后继续上传。若由上游验证，上传层必须检查不可任意构造的验证证明及文件一致性；只接收普通路径/URL的框架应拒绝未验证输入，明确部分的开发仍可继续。
- 回答 `file_type`、目标材料类型或图片上传前置关系时必须同时读取 `merchant-onboarding-external-resources.md`，单列“外部资料提示”并给出未经改写的官方文件类型表地址。

## SDK 源码核验结论

核验来源：官方固定提交和 PyPI 2.0.28 制品，见 `shared-server-sdk-matrix.md`。`2026-10-08` 复核下表及后续 Python 源码结论；该分发目录不含 Demo，不以旧 Demo 缺陷作为本版证据。

| 语言 / 版本 | 源码事实 | Skill 结论 |
| --- | --- | --- |
| Java `dg-java-sdk 3.0.41` | 有 `V2SupplementaryPictureRequest`、`V2_SUPPLEMENTARY_PICTURE`、`BasePayClient.upload(...)`；无文件时对该 URI 特判为 multipart 文本字段，有文件时以 `file` 为 multipart 文件字段；两条路径都先对 `data` 加签 | 支持。`file_url` 走 `BasePayClient.request(request, true)`；本地文件走 `BasePayClient.upload(request, file)`；二者不得同时使用 |
| PHP `php_v2.0.31` | 有 Request 类和路由常量；`BsPayClient` 的 `CURLFile` 包装分支把 `needSign`、`needVerfySign` 都设为 `false`；官方 Demo 又同时设置 `file_url` 和 `CURLFile`；无文件分支只是通用 JSON POST | 不直接使用该专用包装；允许保持请求加签的通用 POST 或自写 HTTPS multipart 适配器 |
| Python `dg_sdk 2.0.28` | 有 Request 类和路由常量，但专用 `post(extend_infos)` 忽略参数、读取未定义的 `self.picture`、遗漏 `req_seq_id/req_date`、使用 `picture` 而非官网 `file`，并关闭签名和验签 | 不直接使用专用类；允许显式开启加签的底层通用 POST 或自写 HTTPS multipart 适配器 |

“官方 SDK 专用实现可用”与“可通过受控降级接入”必须分开表达。不得把 PHP/Python 生成类或 Demo 宣称为已修复；但可为本接口生成 Guzzle、`curl_*`、requests/httpx 或等价通用 POST，实现下述专用 wire 与签名合同。本例外不得用于其他进件接口或商户费率查询。

## Java 官方 SDK 调用

所有值由服务端安全配置和调用方提供。`BasePay.debug` 默认为 `true`，会输出私钥、签名和请求数据；必须在进程初始化阶段、任何 SDK 请求之前全局关闭，不能在并发请求中临时切换。

### 受控 `file_url`

```java
import com.huifu.bspay.sdk.opps.client.BasePayClient;
import com.huifu.bspay.sdk.opps.core.BasePay;
import com.huifu.bspay.sdk.opps.core.request.V2SupplementaryPictureRequest;
import java.util.HashMap;
import java.util.Map;

// 进程初始化阶段执行一次，必须早于任何 SDK 请求。
BasePay.debug = false;

V2SupplementaryPictureRequest request = new V2SupplementaryPictureRequest();
request.setReqSeqId(input.reqSeqId());
request.setReqDate(input.reqDate());
request.setFileType(input.fileType());
Map<String, Object> extendInfo = new HashMap<>();
if (input.huifuId() != null && !input.huifuId().isBlank()) {
    extendInfo.put("huifu_id", input.huifuId());
}
extendInfo.put("file_url", input.controlledHttpsUrl());
request.setExtendInfo(extendInfo);

Map<String, Object> rawResult = BasePayClient.request(request, true);
```

### 本地文件

```java
import com.huifu.bspay.sdk.opps.client.BasePayClient;
import com.huifu.bspay.sdk.opps.core.BasePay;
import com.huifu.bspay.sdk.opps.core.request.V2SupplementaryPictureRequest;
import java.io.File;
import java.util.HashMap;
import java.util.Map;

// 进程初始化阶段执行一次，必须早于任何 SDK 请求。
BasePay.debug = false;

V2SupplementaryPictureRequest request = new V2SupplementaryPictureRequest();
request.setReqSeqId(input.reqSeqId());
request.setReqDate(input.reqDate());
request.setFileType(input.fileType());
Map<String, Object> extendInfo = new HashMap<>();
if (input.huifuId() != null && !input.huifuId().isBlank()) {
    extendInfo.put("huifu_id", input.huifuId());
}
if (!extendInfo.isEmpty()) {
    request.setExtendInfo(extendInfo);
}
// 本地文件模式不得设置 file_url。
Map<String, Object> rawResult = BasePayClient.upload(request, new File(input.localPath()));
```

Java 两条图片路径都在 SDK 内完成请求 `data` 加签。SDK 对图片调用使用 `isPage=true`：在响应验签前把原始响应包装进返回 Map 的 `data`，因此这里的 `rawResult` 不是已验签的业务 DTO。不得直接假定 `rawResult.data.file_id` 或任何其他文件标识字段；保留原始响应边界，自动续提不得使用未经验证或猜测的标识。可继续上传适配器、响应映射接口和后续业务骨架，把未明确的映射留 TODO/配置；不将取得官方样本作为整体开发的前提。

官方 Java Demo 同时设置 `file_url` 并传入本地 `File`，与官网互斥合同冲突，属于不可复制的反例。实际代码必须只选上面一种模式。

## PHP / Python 受控降级

只对 `/v2/supplementary/picture` 放开通用 POST/自写 HTTP。实现必须同时满足：

- 使用 HTTPS POST；生产 host 来自服务端环境配置，不从用户输入拼接。客户端必须校验证书链和主机名，设置连接/读取超时，不启用自动业务重试。
- 请求使用 `multipart/form-data`，让 HTTP 库生成 boundary，不手写固定 boundary。文本部分固定为 `sys_id`、`product_id`、`data`、`sign`；`data` 是包含 `req_seq_id/req_date/file_type` 及可选 `huifu_id/file_url` 的紧凑 JSON 字符串。
- 按 `shared-signing-v2.md` 对排序后的 `data` JSON 做 V2 RSA 加签。不得把文件字节、multipart boundary 或整个外层信封加入签名原文，也不得关闭请求签名。
- 本地文件模式增加且仅增加顶层文件 part `file`；不得使用 `picture`。`file_url` 模式不带文件 part；两种来源不得同时发送。
- 发送 `jpt-x-skill-source`；其他 SDK 内部请求头不由 Skill 生成。自写适配器不得伪造 `jpt-sdk_version`。
- 响应存在 `sign` 时按 V2 规则验签；响应无签名时保留原始响应并标为未验签，不自动读取猜测的文件标识继续进件。

语言边界：

- PHP：不得使用会把 `needSign/needVerfySign` 改为 `false` 的 `BsPayClient::postRequest($request, new CURLFile(...))`。可以使用保留加签的通用调用层或 Guzzle/cURL multipart 适配器；若自写 cURL，必须启用 peer 与 hostname 校验。
- Python（已核验源码基线 `2.0.28`）：不得直接调用该基线的 `V2SupplementaryPictureRequest.post(...)`。本地文件可使用底层 `dg_sdk.core.request_tools.request_post`，但必须补齐全部字段、文件键固定为 `file`，并显式 `need_sign=True`；`DGTools.request_post` 不暴露 `need_sign/need_verfy_sign` 开关，不得向其传这些关键字。也可使用仅限图片接口的 requests/httpx multipart 适配器。`file_url` 不得走通用 JSON body，必须按上述 multipart 文本字段发送。
- 依据已核验源码选择降级时，明确标注“已核验 PHP 2.0.31 / Python 2.0.28 的官方 SDK 专用实现不可用，当前采用图片接口受控降级”（按实际语言保留对应版本），避免把降级实现误称为官方 SDK 支持；其他版本按其实际源码判断，不自动套用本版缺陷或修复结论。

## 公共请求头与安全边界

- Java 使用 Skill 调用时要求 `jpt-x-skill-source: <skill_source>`；未显式配置时，仅进件实际参与当前请求使用 `hfms/1.2.0`，支付与进件都实际参与时使用 `hfps/1.6.0;hfms/1.2.0`，仅安装未参与的不计入。
- 其他 SDK 内部请求头由 SDK 自行获取和发送，Skill 不配置、不校验，也不以其生成方式决定图片能力。
- `file_url` 必须来自受控 HTTPS 对象存储并使用短时授权；业务层校验 scheme、允许 host、有效期和可访问性。URL、材料内容、请求流水、商户号和密钥不得写入代码、日志或测试样例。
- Python SDK 的连接重试和任一 SDK 的网络行为都不等于图片接口已确认的业务重试语义；调用方不得自行重放上传。

## 仍需要官方确认

以下内容标记 `[需要官方确认]`，按 `shared-overview.md` 的开发提醒给出本页官方来源；建议开发者核对，不清楚时咨询汇付官方或汇付开发者交流沟通群。继续已核验传输、请求签名和业务框架，未知映射/策略留 TODO，不等待回复才开发：

- PHP/Python 何时提供满足字段、传输、签名和响应处理合同的正式专用 SDK 实现；在此之前使用上述受控降级。
- 图片上传成功响应的完整 envelope、文件标识字段名、响应验签方式、失败码、幂等和业务重试语义。
- Java 图片 SDK 为何固定跳过响应验签，以及官方推荐的响应可信性校验方式。
- 各材料类型支持的非图片格式、JPEG 扩展名的接受条件以及对应内容检查规则；10MB 上限不代表任意格式均可上传。

真实提交时，图片类进件字段只填写调用方已通过受信流程取得并核验的文件标识；不得从字段名猜测、从未验签原始响应自动提取或在上传失败后继续提交进件。
