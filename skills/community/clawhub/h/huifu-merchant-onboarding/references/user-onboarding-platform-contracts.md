# 用户开户公共平台合同

## 目录

- [官方公共来源](#官方公共来源)
- [API 请求与同步响应](#api-请求与同步响应)
- [用户业务入驻类接口异步通知](#用户业务入驻类接口异步通知)
- [控台 Webhook 边界](#控台-webhook-边界)
- [接入方确认的字段裁决](#接入方确认的字段裁决2026-08-10)
- [接入方确认的 wire 矩阵](#接入方确认的-wire-矩阵2026-08-10)
- [本轮新增字段的官方 wire 定义](#2026-09-22-新增字段的官方-wire-定义)

本页补充当前九个接口页共同引用的开发、签名、加密、密钥、异步通知、公共参数和 Webhook 规范。具体业务字段仍以接口页和完整字段目录为准；接入方明确确认的冲突裁决标记为“接入方确认”，不改写官网原始字段目录。`2026-09-15` 快照已将多处 JSON 容器的类型列修正为 String；用户业务入驻修改的同步 `response.data` 与示例仍冲突，用户列表的正式 String(JSON Array) 与原生数组示例也仍冲突。

## 官方公共来源

| 资料 | 官方地址 | 本次读取 SHA-256 |
| --- | --- | --- |
| 异步消息简介 | https://paas.huifu.com/partners/start/ybxx/jiekouguifan_ybxx.md | `e5f1ad5d92511c343d6bbf7d5f09ef0eee4a252bdac3b4d53934c177f6805364` |
| 开发规范 | https://paas.huifu.com/partners/start/kfgf.md | `340ba948aae4cb1fc6b12503b58e24d11c538b5ba70d0728ef374b0d1a4137a5` |
| 加签验签 | https://paas.huifu.com/partners/start/api_v2jqyq.md | `f3ddf23effad316d247033eb5d2f781e57a8d3d23260387b42470de8e1fd76c5` |
| 加密解密 | https://paas.huifu.com/partners/start/api_jiami_jiemi.md | `de9c44b0dc59d34a609ea6fde5437cc7d633722cd770ecadf37a13b347f4bb82` |
| 获取密钥 | https://paas.huifu.com/partners/start/guide_gsycshq.md | `8f79c590233daba14ba2c958ba89d4f6326f624a20bff053d5c5159ec03afab0` |
| 开发接入说明 | https://paas.huifu.com/partners/start/api_kfzn.md | `a50c162dcbafd71044c1c6687b6b908e050a5e5aa54267336ef75661b1f5410d` |
| 基础参数汇总 | https://paas.huifu.com/partners/api/doc/csfl/api_csfl.md | `2d8b73e1009da4b2fccfae75b0bc2546acfc105b2219ada12a2af41f2b6da191` |
| Webhook介绍 | https://paas.huifu.com/partners/devtools/doc/webhook/webhook_jieshao.md | `8a14a938445d9b7e15f2bce5af27b0a38708a601fbbfd88c3004a045cb333089` |

## API 请求与同步响应

- 主动调用采用 HTTPS、POST、JSON、UTF-8，`Content-Type` 为 `application/json;charset=UTF-8`；HTTP 状态只表示接口层通信结果，业务状态读取 `response.data.resp_code`。
- 请求 `body.data` 是 JSON Object。只对 `data` 第一层实际传递的参数按字段名 ASCII 升序排序；字段名区分大小写，空值不得为了 SDK required 标记自动补齐。
- 第一层的复杂业务对象按接口说明处理。说明或接入方确认要求 String(JSON) 时，先把完整对象或数组序列化成一个 JSON 字符串；该字符串内部不再为签名排序。
- 使用 `SHA256WithRSA`：商户私钥为请求加签，汇付公钥为同步响应和异步通知验签。同步响应 `data` 第一层排序后验签；异步通知对收到的原始 `data` 字符串验签，不排序、不得先反序列化再序列化。
- 汇付公钥还用于指定敏感请求字段加密，商户私钥用于指定敏感响应字段解密。仅对具体接口说明要求加密的字段执行 RSA 加密，不得把所有证件、卡号和手机号盲目加密。
- 私钥只能从服务端密钥管理或受控挂载读取；不得进入源码、日志、前端、异常文本、回答示例或工单。公共参数 `sys_id/product_id` 从开放平台开发者工作台取得，不从示例或用户号推导。
- 官方“基础参数汇总”是地区、银行、银行支行、MCC 和文件类型的公共入口。`response.data.qry_cash_card_info_list[].branch_code` 的接口行虽缺链接，现按接入方提供的该公共来源读取银行支行编码 XLSX/JSON/CSV；这不改变字段本身的 String(12) N 合同。

## 用户业务入驻类接口异步通知

`request.data.async_return_url` 触发的是接口异步通知，不是控台 Webhook。用户业务入驻及其修改属于配置类接口，业务体参数名使用 `data`，不能使用支付交易通知的 `resp_data`。

- 汇付以 HTTP(S) POST 推送，编码 UTF-8，默认超时5秒；URL 不带查询参数、不支持重定向，自定义端口使用8000-9005。
- 超时默认重试3次；HTTP 500-599 默认重试3次。其他非成功状态会被视为错误，但公共页没有承诺统一重试次数。
- 接收端必须先保存原始 `data` 字符串，用汇付公钥和 `sign` 执行 SHA256WithRSA 验签；异步 `data` 不排序。验签成功后才解一层 String(JSON) 并处理字段。
- 成功处理后返回 HTTP 200，响应体为 `RECV_ORD_ID_` 加指定业务字段。结合公共页示例与本接口异步体中的原请求流水，本接口使用 `RECV_ORD_ID_` + `async.data.req_seq_id`。
- 同一消息可能重复推送，处理必须幂等。官方没有定义全局事件 ID；持久化原始报文摘要、`req_date/req_seq_id/notify_type`、状态和处理结果，允许同一请求后续状态更新，不能只用 `req_seq_id` 粗暴丢弃。
- 通知发送侧对 HTTPS 证书校验的历史描述不授权接收端或主动请求客户端关闭 TLS 校验；接收端仍必须使用有效证书并执行正常 TLS 校验。

## 控台 Webhook 边界

控台注册的 Webhook 是另一套事件订阅机制，不是 `async_return_url`：

| 项目 | 接口异步通知 | 控台 Webhook |
| --- | --- | --- |
| 配置入口 | 接口字段 `async_return_url` | 汇付控台端点订阅 |
| 传输体 | 表单参数中的 `data` String(JSON) | HTTPS 原始 JSON 事件体 |
| 验签 | 汇付 RSA 公钥 + SHA256WithRSA | 端点32位终端密钥；按 Webhook Demo 校验原始体签文 |
| 成功响应 | HTTP 200 + `RECV_ORD_ID_` + 请求流水 | 任意2xx |
| 重推 | 超时和部分5xx默认3次 | 失败后1秒一次共3次，之后每小时一次直至成功，也可控台手工重推 |

禁止把 Webhook 的终端密钥、2xx应答或重推规则套到用户业务入驻及其修改接口通知，也禁止把接口通知的 RSA、`RECV_ORD_ID_` 套到 Webhook。

## 接入方确认的字段裁决（2026-08-10）

- `C` 统一解释为“条件必填”，不再解释为条件选填；仍必须按字段说明或本页主体/卡类型矩阵确定触发条件。
- 个人用户只允许对私法人卡：`card_type=1`。`0=对公`、`2=对私非法人`、`4=对公非同名` 均不得用于个人用户。企业用户可按业务条件使用 `0/1/2/4`。
- 所有已接受的 `card_type` 都要求提交 `card_name`：企业用户按0/1/2/4分别填写对应账户名，个人用户按1填写本人对私账户名。不得用主体姓名静默覆盖传入卡户名。
- e账户卡 `elec_card_list[].mp` 按卡类型区分：`card_type=1` 对私法人卡要求存在有效手机号；`card_type=0` 对公卡不要求该手机号。查询响应仍按字段存在性解析，不能因历史数据缺失判整单失败。
- 申请状态查询成功返回 `data` 时，`apply_reason/apply_status/huifu_id` 在 `Y/P/N/F` 四种状态均返回；`apply_status` 值域为 `Y/P/N/F`。
- 用户业务入驻成功响应返回 `apply_no`。该结论不表示审核已通过；仍按同步配置结果和异步审核状态分别持久化。
- 当时五个接口成功响应都包含外层 `response.data`。官网的 `N` 继续保留为原始字段事实，用于兼容网关或异常响应缺少 `data`；成功响应缺少 `data` 按协议异常处理。企业修改成功示例同样包含原生对象，但不把示例提升为接入方确认事实。

## 接入方确认的 wire 矩阵（2026-08-10）

| 完整路径 | wire 形态 |
| --- | --- |
| `request.data`、`2026-08-10` 已裁决五接口的成功 `response.data` | 原生 JSON Object |
| 企业/个人开户 `request.data.file_list` | String(JSON Array) |
| 业务入驻 `request.data.settle_config_list/cash_config/file_list` | String(JSON Array) |
| 业务入驻 `request.data.card_info/elec_acct_config` | String(JSON Object) |
| 业务入驻 `request.data.elec_acct_config.elec_card_list` | 父 String(JSON Object) 内的 String(JSON Array) |
| 业务入驻 `request.data.elec_receipt_config/sign_user_info` | String(JSON Object) |
| 业务入驻 `response.data.resp_business` | 外层对象中的 String(JSON Array) |
| 业务入驻 `async.data` | 原始 String(JSON Object)，先验签再解码 |
| 业务入驻 `async.data.audit_info/elec_acct_result` | 解码异步 data 后的 String(JSON Object) |
| 业务入驻 `async.data.audit_info.resp_business` | 解码 audit_info 后的 String(JSON Array) |
| 业务入驻修改 `request.data.settle_config_list/cash_config/file_list` | String(JSON Array) |
| 业务入驻修改 `request.data.card_info/elec_acct_config` | String(JSON Object) |
| 业务入驻修改 `request.data.sign_user_info/elec_receipt_config` | String(JSON Object) |
| 业务入驻修改 `request.data.elec_acct_config.elec_card_list` | 父 String(JSON Object) 内的 String(JSON Array) |
| 业务入驻修改 `response.data` | 正式表 String N，成功示例原生 JSON Object；保留冲突 |
| 业务入驻修改 `async.data.audit_info.resp_business` | 解码 audit_info 后的 String(JSON Array) |
| 用户列表查询 `response.data.user_list_info_list` | 正式表为 String(JSON Array)，成功示例为原生数组；保留冲突 |
| 详情 `response.data.ent_base_info/indv_base_info/card_info/elec_acct_config` | String(JSON Object) |
| 详情 `response.data.settle_config_list/qry_cash_config_list/qry_cash_card_info_list` | String(JSON Array) |
| 详情 `ent_base_info.file_list/indv_base_info.file_list` | 解码各自父对象后的 String(JSON Array) |
| 详情 `elec_acct_config.elec_card_list` | 解码父对象后的 String(JSON Array) |
| 详情 `response.data.elec_receipt_config/sign_user_info` | String(JSON Object) |

序列化和解码必须逐层按表执行，不能把所有 `String` 都当普通文本，也不能把所有带子表的字段都改成原生对象。

## 用户等级与资金配置的当前 wire 定义（10-25复核）

以下是本轮正式字段表新增合同，不追溯冒充 `2026-08-10` 接入方确认。

| 完整路径 | wire 形态 |
| --- | --- |
| 业务入驻及修改 `request.data.balance_pay_config` | String(JSON Object) |
| 业务入驻及修改 `request.data.account_recharge_config` | String(JSON Object) |
| 业务入驻及修改 `request.data.delay_pay_config` | String(JSON Object) |
| 业务入驻及修改 `async.data.account_info` | 当前String(JSON Object)，解码异步data后再解码该字段；A/U时返回 |
| 详情 `response.data.balance_pay_config` | 原生 Object |
| 详情 `response.data.account_recharge_config` | 原生 Object |
| 详情 `response.data.delay_pay_config` | 原生 Object |
| 详情 `response.data.account_info` | 原生 Object |

四组查询对象不得套用请求 String(JSON) 编码。余额/充值收费两字段 `Y` 与“至少填写一个”的说明仍冲突；按 `shared-overview.md` 的开发提醒列出对应业务入驻/修改官方文档，建议核对或咨询汇付官方、汇付开发者交流沟通群。继续 DTO/SDK 开发，争议必填策略用 TODO/配置隔离，不猜互斥或同时必填，也不把取得答复作为开发前提。当前请求account_recharge_config除两项费率外新增out_fee_flag、out_fee_huifu_id、out_fee_acct_id，必须按本接口条件填写；仍不能倒灌查询响应的switch_state/transfer_flag_no/transfer_flag_name。

10-25通知分派使用E审核、A业务、U升级、Z电子账户。audit_info在A/E时返回；account_info在A/U时返回并使用String(JSON Object)。新增协议列表为String(JSON Array)。消息业务类型变化不改变已有公共原文验签、HTTP200与RECV_ORD_ID_应答合同。
