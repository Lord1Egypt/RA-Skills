# 用户开户服务端 SDK 能力矩阵

## 版本基线

结论来自2026-10-08核验的官方固定Git提交/PyPI制品，源码和SHA由维护仓库锁定。类和URI存在不证明接口权限、材料条件、审核结果或通知协议。

Python 当前 SDK 为 `2.0.28`，来自官方PyPI 2.0.28制品；本页九接口类、字段、构造器与传输边界已按该源码复核，API 来源为 `2026-11-09`。源码和离线探针不代替真实网关联调；其他版本差异按 `shared-server-sdk-matrix.md` 核对，继续已明确部分，不新增硬检查点。

| SDK | 当前版本 | 九接口专属类 | 使用规则 |
| --- | --- | --- | --- |
| Java `dg-java-sdk` | `3.0.41` | 已找到 | 使用官方 Request/Client；先关闭敏感调试 |
| PHP `huifurepo/dg-php-sdk` | `2.0.31` | 已找到 | 使用官方 Request/Client；DEBUG/Demo 入口仍需独立检查 |
| Python `dg-sdk` / `dg_sdk` | `2.0.28` | 已找到 | 使用官方 Request；仍需按业务授权完成字段与网关联调 |

## 九个精确类与 URI

三语言均应只使用对应专属 Request，不得按后缀复用 merchant 类：

| Request 类 | URI |
| --- | --- |
| `V2UserBasicdataEntRequest` | `/v2/user/basicdata/ent` |
| `V2UserBasicdataIndvRequest` | `/v2/user/basicdata/indv` |
| `V2UserBusiOpenRequest` | `/v2/user/busi/open` |
| `V2UserApplyQueryRequest` | `/v2/user/apply/query` |
| `V2UserBasicdataQueryRequest` | `/v2/user/basicdata/query` |
| `V2UserBasicdataEntModifyRequest` | `/v2/user/basicdata/ent/modify` |
| `V2UserBasicdataIndvModifyRequest` | `/v2/user/basicdata/indv/modify` |
| `V2UserBusiModifyRequest` | `/v2/user/busi/modify` |
| `V2UserListQueryRequest` | `/v2/user/list/query` |

共同要求：保留 SDK 请求签名和同步响应验签；显式传入业务流水和日期。SDK 连接重试不能解释成开户或入驻业务重试。

## 官方合同优先与运行探针

- 生成类可能把官方 `C` 字段建模成 required 或发送空字符串，例如开户有效期/国籍/地址、企业登录名以及业务入驻 `sign_user_info`。以官方 Y/N/C 和条件说明为准。
- `file_list`、`elec_card_list`、`sign_user_info` 和 `elec_receipt_config` 当前正式类型均已改为 String；按 `user-onboarding-platform-contracts.md` 的逐层 String(JSON) 矩阵处理。公共返回 `data` 与用户列表成功示例冲突仍须保留，不得仅靠类属性名决定。
- `sign_user_info` 当前官网类型为 String，与生成类 String setter 一致；传一层合法 JSON Object 字符串，并在脱敏运行探针中记录最终 JSON 类型、签名输入和网关结果。
- 企业用户基本信息修改类只声明 `req_date/req_seq_id/huifu_id/legal_cert_nationality`。其余正式可选字段通过 exact-key 扩展传入；Java `putAll`、PHP `array_merge`、Python `dict.update` 都会后写覆盖同名显式字段，因此必须拒绝扩展覆盖这四个键，并拒绝所有合同外键。
- 个人用户基本信息修改类只声明 `req_date/req_seq_id/huifu_id`。其余正式可选字段通过 exact-key 扩展传入；三语言的后写合并同样会覆盖显式字段，因此必须拒绝扩展覆盖这三个键，并拒绝所有合同外键。
- 用户业务入驻修改类只声明 `req_date/req_seq_id/huifu_id/sign_user_info`。`sign_user_info` 当前按官网 String(JSON Object) 传输；三语言均以运行探针锁定只序列化一次，四个直接字段禁止被扩展覆盖。
- 用户列表查询类只声明 `legal_cert_no/req_date/req_seq_id`。官网可选 `upper_huifu_id` 使用白名单 exact-key 扩展；三语言后写合并会覆盖显式字段，因此必须拒绝扩展中的 `legal_cert_no/req_date/req_seq_id`。
- 探针不能绕过签名、验签或敏感日志安全要求；本地 SDK 的既有 TLS 风险按下方非阻断提醒处理，新代码不主动关闭正常校验。

## 调试日志硬停

- Java `BasePay.debug` 默认 `true`，可能记录私钥、签名和请求数据。进程初始化、任何请求之前全局固定为 `false`，不得并发临时切换。
- PHP SDK 主配置默认可为 `DEBUG=false`，但官方 Demo/Composer 入口可能在 `BsPay::init` 前定义 `DEBUG=true`，进而记录含 RSA 私钥的配置、完整请求和响应。
- PHP 联调/生产不得加载启用 DEBUG 的 Demo loader；启动检查必须在加载 SDK 和初始化前拒绝 `DEBUG=true`，且不能被后续配置改回。

## 官方 SDK-only 传输规则

- 九接口均使用各自官方 Request/Client。通用 Java `3.0.41` 使用默认 TLS 工厂，Python `2.0.28` 保留 requests 默认校验；PHP `2.0.31` 本地源码仍设置 `CURLOPT_SSL_VERIFYPEER=false`。按本轮要求仅作非阻断提醒，继续已明确的 SDK 接入，不要求先提供修复证明或官方答复。
- 建议开发者核对对应 SDK/官方文档，疑问可咨询汇付官方或汇付开发者交流沟通群；详见 `shared-server-sdk-matrix.md`。新代码不主动加入 trust-all、`verify=false`，不擅自修改 SDK，不把离线验证或本轮策略说成风险已修复。字段疑义按 `shared-overview.md` 继续明确部分并用 TODO/配置隔离。
- 禁止用 `HttpClient`、OkHttp、`HttpURLConnection`、Guzzle、`curl_*`、通用 POST 或自实现签名/验签客户端替代官方 SDK。三语言交付分别使用官方 SDK，不允许只让 Python 使用 SDK。

企业/个人开户的业务合同没有 `data.huifu_id`，请求 DTO 按官网字段生成，不增加合同外业务字段。

Python 2.0.28 初始化必须显式使用 `sign_type="RSA", jpt_x_skill_source=skill_source`；第五位置参数已是算法，不再是来源。SDK 的共享类级请求状态需串行或进程隔离，不承诺多用户并发线程安全。
