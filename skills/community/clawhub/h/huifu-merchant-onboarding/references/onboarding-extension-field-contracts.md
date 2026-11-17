# 进件扩展十二接口字段合同

## 公共规则

- 十二个接口均为 HTTPS POST。以各原子页的正式字段表和 `onboarding-extension-complete-field-catalog.md` 为字段证据；示例不得覆盖字段表。字段说明命中公共规范、编码表或第三方渠道资料时同时读取 `onboarding-extension-external-resources.md`。
- `Y` 为必填、`N` 为可选、`C` 为条件满足时必填。字段标为 `N` 但说明写“必填”时，仍执行说明中的条件并记录官网标记冲突。
- String(JSON Object/Array) 只序列化一层。类型为 `Object` 的字段按原生 JSON 结构处理；类型、说明与示例不一致时标记 `[需要官方确认]`，按 `shared-overview.md` 的“文档疑义与开发提醒”给出对应原子页官方文档，建议核对或咨询汇付官方、汇付开发者交流沟通群。继续明确的 SDK/业务代码，争议 wire 用 TODO/配置隔离，不将官方答复作为开发前提。
- `sys_id` 是调用主体，`data.huifu_id` 是被操作商户，`upper_huifu_id/head_huifu_id` 是层级关系，`store_id` 是接入方门店标识；四者不得互换。
- 请求示例里的商户号、证件号、手机号、APP secret、合同 URL、二维码和签名均不是默认值，不得复制或记录。

## 已确认的结构边界

- 电子合同重发、列表和拒签都没有异步字段表。合同列表的 `result_list` 正式类型为 String 且说明 `jsonArray`，按一层 String(JSON Array) 解码；列表内部仍以正式字段名为准。
- 下级商户权限配置的21组扩展结构均从正式父字段展开；`data.product_id` 与外层 `product_id` 是两个独立字段。配置响应只有9个正式路径，不得套用官网错误的商户详情示例。
- 统一页面进件同时有审核异步与逐业务异步，分别使用 `async.audit.data` 和 `async.business.data`；不能共用一个无通知类型的 DTO。
- 微信配置当前原文仅有 request、request.data、response.data、async.data 四张根表；后两者仅为目录语义分组，不能由此推断线上的外层信封、data 类型或签名。微信配置查询的 `atu_config_bo_list`、`atu_config_bo_fail_list` 及嵌套 `wx_config_list` 都按 String(JSON Array) 解码。
- 微信与支付宝实名认证的结构字段按正式 String(JSON) 定义编码；查询结果只表示渠道申请与授权状态，不代表汇付商户审核或支付交易终态。
- 微信实名查询的 `response.data.applyment_stat` 必须联读字段表外九值状态表，并保留官网原拼写：`APPLYMENT_STATE_EDITTING/WAITTING_FOR_AUDIT/WAITTING_FOR_CONFIRM_CONTACT/WAITTING_FOR_CONFIRM_LEGALPERSON/PASSED/REJECTED/FREEZED/CANCELED/NOAPPLY`。`authorize_stat=1/0` 是独立授权轴，不得由申请状态推导。

## 必须保留的官方冲突

1. 三个电子合同接口的 `resp_code` 已统一为8位；列表现在使用 `page_size/create_time`，响应分页字段也已正式声明，旧拼写与长度冲突关闭。但 `result_list:String/jsonArray` 与原生数组示例仍冲突；无协议时不返回该字段，不能伪造空值。三接口路由已迁移到 `/v2/agreement/elect/signurl/resend`、`/v2/agreement/apply/list`、`/v2/agreement/elect/rejectsign`。本地新增 `V2Invoice*` 专属类仍是旧 invoice 路由，不可用于最新接口；使用已核验的官方 SDK 通用入口。
2. 下级商户权限配置的请求示例漏掉正式必填的 `data.product_id`，响应示例仍复制商户详情。只使用正式表；真实响应联调前保持宽容读取并记录未知键。
3. 统一页面进件 `use_chains_flag` 已明确四值，`head_huifu_id` 为 C，旧冲突关闭；业务 `resp_code`、URL 长度、审核通知日期长度冲突仍保留。页面 URL 按不透明敏感值处理，不截断。
4. 统一页面查询正式拼写已修为 `wx_real_name_list`；五组列表都正式定义为 String(JSON Array)，旧拼写与容器冲突关闭。本轮 `pay_scene` 长度已修为2，旧长度冲突关闭；链接文字写“微信业务开通类型”、目标锚点却是“微信支付场景”，不得静默选择外部枚举。
5. 微信配置异步 `config_type` 已修为 String(2)，同步四字段均 N 且未声明长度；旧长度冲突关闭。微信配置查询的一行仍把必填和长度写成 `32/N`，且新增/查询页对公众号 APPID 长度给出20/512；外层签名/信封、HTTP 状态与重试仍未知。
6. 微信实名状态的 `qrcode_data` 同时被描述为 base64、可直接加载图片和完整 HTML。不得直接插入 DOM，也不得在确认 wire 前做二次解码。
7. 支付宝实名申请已给社会组织主体编码6及对应证件条件，`auth_identity_info` 改为 N；旧主体编码缺口关闭。`support_credentials` 已改 String(JSON Object)，小微商户条件必填，旧数组/对象冲突关闭；`industry_qualification_info` 正文仍与社会组织枚举不一致；金融机构与地区示例冲突仍保留。

## 异步与状态

- 仅统一页面进件与微信商户配置声明异步字段。正式表未完整给出 HTTP 状态、超时、重试和统一 ACK；可继续 webhook 框架、业务状态处理和测试，未声明协议留 TODO/待填配置；提示开发者核对相应官方文档或咨询官方/交流群，不补造统一 ACK、重试或验签规则。
- 处理异步时先验签，再用 `req_date + req_seq_id + notify_type/ord_id` 做状态感知幂等；不得在验签前解析并落库敏感 data。
- 同步受理、审核通过、渠道实名通过、渠道授权成功和支付可用是不同状态层级，输出必须逐层说明。
