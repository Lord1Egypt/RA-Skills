# 用户开户与入驻字段合同

## 目录

- [公共包络](#公共包络)
- [字段审计覆盖索引](#字段审计覆盖索引)
- [Y/N/C 与值来源](#ync-与值来源)
- [官网未定义项](#官网未定义项)
- [开户合同](#开户合同)
- [企业用户基本信息修改合同](#企业用户基本信息修改合同)
- [个人用户基本信息修改合同](#个人用户基本信息修改合同)
- [用户业务入驻合同](#用户业务入驻合同)
- [用户业务入驻修改合同](#用户业务入驻修改合同)
- [业务入驻异步合同](#业务入驻异步合同)
- [查询合同](#查询合同)
- [用户列表查询合同](#用户列表查询合同)

## 字段审计覆盖索引

完整字段任务先在 `user-onboarding-complete-field-catalog.md` 定位目标接口，分页读取所需方向与父容器，再对照本页相关章节；未选择的能力不强制写入请求。输出前检查：

| 目标 | 必须核对的现有资料 |
| --- | --- |
| 开户及基础信息修改 | 本页开户/修改合同；完整目录中的证件条件、地区长度、材料父容器和参数表外注记 |
| 入驻、结算卡和取现 | 本页入驻/修改合同；目标目录的上级ID、卡类型/户名、D1配置、收费条件与冲突 |
| 电子账户及回单 | 目标目录的父容器、卡子项和回单条件；`user-onboarding-platform-contracts.md` 的wire矩阵与接入方裁决 |
| 账户等级及资金配置 | 本页“用户等级与新资金配置”；平台页新增字段章节；完整目录按请求、详情与异步分别核对String(JSON)及原生Object |
| 状态、查询及敏感字段 | 本页查询/异步合同；平台页公共返回与状态边界；`user-onboarding-shared-credential-boundary.md` 的敏感字段 |
| 全量统计及未知项 | 完整目录的生成覆盖摘要、各方向节点和表外注记；父节点计数、完整路径去重，空说明保留 `—` |

列出完整英文父路径及方向，不只写“配置见文档”。局部问题可只展开目标部分，但应说明未覆盖部分；完整性结论不能只依据搜索片段或请求示例。

## 公共包络

九个接口均为 HTTPS POST JSON。请求外层为 `sys_id:String(32) Y`、`product_id:String(32) Y`、`sign:String(512) Y`、`data:Json Y`；同步响应外层包含 `sign:String(512) Y` 和业务 `data`。九页正式公共返回表都把外层 `response.data` 标为 `N`：用户业务入驻修改仍为 `String`，其余为 `Json`。用户列表查询的 `user_list_info_list` 当前为 `String/jsonArray格式`，按 String(JSON Array) 解码；成功示例使用原生数组，保留冲突。成功码下缺少 `data` 按协议异常处理，同时 DTO 允许网关或异常响应整体缺失。这些是 JSON 包络参数，不是 HTTP 请求头。

`sys_id` 表示调用主体：渠道商填写渠道商号，直连/总部商户填写商户号。它不是本次开户生成的用户号。`jpt-x-skill-source` 是本地 Skill/SDK 合同，不是九份官网页面声明的业务字段；其他 SDK 内部请求头不进入本 Skill 的字段合同。

## Y/N/C 与值来源

- `Y` 必填、`N` 非必填；接入方已确认 `C` 统一表示条件必填。保留官网原始标记，按字段说明和主体/卡类型矩阵执行触发条件，不得把全部 `C` 无条件映射成必填。
- 字段为 `N` 但说明给出条件时，按说明触发条件校验并保留官网矛盾。
- 示例值不是默认值；只有说明明确写“默认”才能使用默认口径。
- 未读取外部编码表正文时，只能要求调用方提供经核验编码，不能从示例猜测。
- 不得为满足 SDK 的“required”标记而给官方 `C` 字段填空字符串。

## 官网未定义项

这些缺口按 `shared-overview.md` 的“文档疑义与开发提醒”处理：指出完整路径及原子页的对应官方文档，不清楚时建议咨询汇付官方或汇付开发者交流沟通群。继续已明确部分，争议约束与序列化用 TODO/待填配置隔离，不等待答复才开始整体开发。

完整目录对官网空白单元格统一保留 `—`，不代表值为空字符串，也不授权从同名字段或 SDK 推断。当前充值账户等字段仍有空说明，account_info父对象说明已补齐；仍不得从查询字段、示例或SDK补齐，详见机械目录；当前已没有长度为空的标量叶字段。对象、数组及 String(JSON) 父节点长度为空是结构字段的正常口径，不得把 `—` 改成 `0` 或空字符串。

官网没有写出两个 `C` 字段的触发条件，接入方现已补充裁决：所有通过主体校验的 `request.data.card_info.card_type` 都条件必填 `card_name`；`response.data.elec_acct_config.elec_card_list[].mp` 在 `card_type=1` 对私法人卡时要求存在，在 `card_type=0` 对公卡时不要求。官网空说明仍在机械目录保留为 `—`，语义校验读取接入决策，不从同名字段推断。

## 开户合同

- 企业证照和法人证件：`validity_type=0` 时结束日期必填；法人证件为外国人居留证时国籍必填。官网长期有效示例仍带结束日期，不构成长期时必填。
- 企业页在参数表外明确：系统会对 `request.data.legal_name` 与 `request.data.legal_cert_no` 做法人姓名和身份证号实名认证；完整目录把同一注记绑定到两个字段，不能只保留其中一个。
- 个人证件：`cert_end_date:String(8)` 的必填列为 `N`，说明却要求非长期有效时必填；保留为“官网 N + 条件必填”。外国人居留证触发国籍。
- 企业 `mcc` 以及个人 `mcc/prov_id/area_id/district_id` 的必填列均为 `N`，但说明明确“用户业务入驻修改且电子回单配置开通时需填写”；必须保留该完整触发条件。
- 企业和个人开户的 `file_list:String/jsonArray格式` 均按一层 String(JSON Array) 发送。个人页的表外注意说明仍要求：证件类型为身份证时，汇付会对姓名和身份证号做实名认证。
- 两个开户接口的 `sms_send_flag` 只使用 `Y/N`，默认不发送。企业要发送或升级LV3时 `login_name` 必填；企业ent_type现在Y；当前两个请求示例均已使用 `"Y"`。
- 企业注册省/市/区长度分别为6/8/12；个人电子回单相关省/市/区字段为6位口径。不得统一截断或补齐。
- 两个开户请求都没有 `data.huifu_id` 或 `upper_huifu_id`，也没有异步通知。
- 传 `login_name` 时可能返回 `login_password`；该字段按一次性高敏凭据处理。
- 企业与个人开户的当前成功示例均已包含 `response.sign:String(512) Y`；必须继续验签，且不得复用示例签名值。

## 企业用户基本信息修改合同

- `request.data.huifu_id:String(18) Y` 的中文名和说明现已统一为直属汇付客户 ID，响应同名字段也明确为汇付企业用户 ID；按企业用户号定位，不得传商户号。本接口仍不得与 `/v2/merchant/basicdata/modify` 共用 DTO。
- 页内注意要求修改法人证件时同步填写 `legal_cert_type`、`legal_cert_validity_type`、`legal_cert_begin_date`、`legal_cert_end_date`。完整目录将该注记绑定到四个路径；`legal_cert_no` 虽是可修改字段，但官网注意原文没有把它列入这组“必须同步填写”的字段，不得擅自改写原文。
- `legal_cert_nationality:String(50) C` 仅在法人证件类型为外国人居留证时触发；其余修改字段保持官网 `N`，但不把空字符串解释为删除值。
- `file_list:String(JSON Array)` 在 wire 中仍是一层字符串，子项路径保留 `[]`；不得按原生数组传输。
- 三语言 `V2UserBasicdataEntModifyRequest` 只声明四个字段；其他正式请求字段通过 exact-key 扩展。扩展后合并能覆盖声明字段，因此接入层必须拒绝覆盖 `req_date/req_seq_id/huifu_id/legal_cert_nationality`，并对扩展使用正式请求字段白名单。
- 本接口37个节点为请求32、响应5，无异步方向；响应 `huifu_id` 的官方说明为企业用户ID。

## 个人用户基本信息修改合同

- `request.data.huifu_id:String(18) Y` 的说明现已统一为直属汇付客户 ID；按个人用户号定位，不得传商户号。
- `cert_validity_type:String(1) N` 正式枚举为 `1=长期有效`、`0=非长期有效`，当前请求示例也已修正为 `1`。
- `file_list:String(JSON Array)` 的 `file_id:String(64) Y` 与 `file_name:String(64) N` 均为64位口径，不能复制企业修改接口的128位长度。扩展中仍发送一层 JSON Array 字符串。
- `address:String(256) N` 的说明在开通中信E管家或电子回单时要求填写；`mcc` 与省市区的说明绑定“用户业务入驻修改且电子回单开通”组合场景。保留这些来源条件，不把它们无条件提升为本接口必填。
- `prov_id/area_id/district_id` 均为 `String(6) N`，修改时按官网要求级联修改；不得复制企业修改的6/8/12长度。
- 三语言 `V2UserBasicdataIndvModifyRequest` 只声明 `req_date/req_seq_id/huifu_id`；其他正式请求字段通过 exact-key 扩展。扩展后合并能覆盖声明字段，因此拒绝覆盖这三个键，并对扩展使用正式请求字段白名单。
- 本接口26个节点为请求21、响应5，无异步方向；当前成功示例包含 `response.sign:String(512) Y`，仍须验签。

## 用户业务入驻合同

`POST /v2/user/busi/open` 的新增合同见本节；修改接口的差异边界见下一节。两者字段相近也不得共享未经接口限定的 DTO 或 wire 假设。

- `data.huifu_id:String(18) Y` 必须是开户返回的 `userHuifuId`；`data.upper_huifu_id:String(18) Y` 必须是真实渠道商/商户号。
- `settle_config_list:String(JSON Array)` 不支持同时开通 T1 与 D1；`settle_cycle` 为 `T1/D1/TS`。
- `card_info:String(JSON Object)` 的 `card_type` 为 `0` 对公、`1` 对私法人、`2` 对私非法人、`4` 对公非同名。接入方确认：个人用户只允许 `1`，禁止 `0/2/4`；企业用户按业务条件使用 `0/1/2/4`。所有接受的类型都要求 `card_name`，并按企业/个人及账户关系填写对应账户名。
- `card_type=4` 需要文件 `F07`、`F08`、`F516`，并按法人证件类型补相应材料。示例多出的 `bank_code`、`branch_name` 不属于该正式子表。
- `settle_cycle=D1` 时正式说明要求 `fixed_ratio`、`constant_amt` 必填且费率/金额保留两位小数；当前请求示例已包含 `constant_amt:"1.00"`，并使用 `fixed_ratio:"2.00"`、`cash_config.fee_rate:"2.00"`。仍只执行正式字段规则，不把示例值当默认值。
- `elec_acct_config.elec_card_list[].card_type` 正式枚举为 `0/1`，当前示例已修正为 `0`。
- `cash_config:String(JSON Array)` 中 `fix_amt` 与 `fee_rate` 至少一项；`out_fee_flag=1/2`，默认2；账户类型只按正式枚举处理。
- `delay_flag` 仅 `Y/N`。电子回单开通时 `sign_user_info` 条件必填；当前正式类型为 String，wire 按 String(JSON Object) 发送。
- 同步成功 `response.data:Json` 是原生对象，`resp_business:String(JSON Array)` 解一层后读取 `type=1/2/3/5`、`code=S/F`；接入方确认成功响应返回 `apply_no`，但这不等同审核最终通过。

## 用户业务入驻修改合同

- 使用 `POST /v2/user/busi/modify`；完整目录精确151个节点：请求104、同步响应11、异步36，包含6个根表、18个扩展表。`request.data.huifu_id:String(18) Y` 明确填写开户返回的用户ID，不得替换为商户号。
- `settle_config_list`、`cash_config`、`file_list` 按 String(JSON Array) 发送；`card_info`、`elec_acct_config`、`elec_receipt_config`、`sign_user_info` 按 String(JSON Object) 发送。
- `request.data.elec_acct_config.elec_card_list` 当前正式类型为 String 且说明为 jsonArray字符串；先序列化子数组，再放入父对象并对父对象序列化一次。
- `request.data.settle_config_list[].is_priority_receipt` 的必填列为 `C`，说明明确 `settle_pattern=P0` 时必填，但又描述空值默认；按 P0 条件执行必填，默认描述作为官方矛盾保留。当前 `delay_flag` 示例已修正为 `N`，`async_return_url` 示例也已修正为合法 HTTP URL。
- 官网请求示例是合法 JSON，且只声明一次 `file_list`；示例仍不构成默认值或正式字段合同，不得用示例覆盖参数表。
- 三语言 `V2UserBusiModifyRequest` 都只声明 `req_seq_id/req_date/huifu_id/sign_user_info`，路由精确为 `/v2/user/busi/modify`。当前官网与 Java 的 String setter 对 `sign_user_info` 已一致，三语言均传一层 JSON Object 字符串。生成类的扩展后合并都能覆盖已声明键，因此扩展必须拒绝 `req_seq_id/req_date/huifu_id/sign_user_info`，并对白名单内其余正式字段逐项放行。
- 同步公共表把 `response.data` 写成 `String N`，成功示例却返回原生 JSON Object；本接口没有独立 wire 裁决，DTO 需隔离两种形态并容忍异常响应缺失，解析形态通过明确的 TODO/可配置策略隔离，不静默认定任一示例为官方结论；这不阻断其余 SDK/业务实现。异步现在使用36节点配置类通知合同，不能因修改接口而省略验签、回包、重试或状态感知幂等。

## 用户等级与新资金配置（2026-09-22）

业务入驻与修改的 `request.data.account_level:String(6) N` 为LV1/LV2/LV3，不填默认LV1。余额支付、账户充值、延迟支付配置只在LV3开通；个人用户不支持LV3。不要把这些开户配置路由到实际支付交易。

| 完整路径 | 方向与wire | 关键条件 |
| --- | --- | --- |
| `request.data.balance_pay_config` | 入驻/修改 String(JSON Object) | fee_rate/fee_fix_amt均String(9) Y，但说明要求至少一项；存在必填列冲突，严格校验策略留 TODO/待填配置，同时继续其余 DTO 与 SDK 开发。两者都有时费用相加。 |
| `request.data.account_recharge_config` | 入驻/修改 String(JSON Object) | fee_rate/fee_fix_amt保留既有冲突；本轮新增out_fee_flag=1外扣/2内扣，开通外扣时out_fee_huifu_id与out_fee_acct_id为C必填。不能复制查询独有switch_state等字段。 |
| `request.data.delay_pay_config` | 入驻/修改 String(JSON Object) | switch_state:String(1) Y，1开通/0关闭。不同于delay_flag Y/N。 |
| `async.data.account_info` | 入驻/修改 String(JSON Object) N | notify_type=A/U时返回；account_level/face_url/trans_status/verify_ord_id/fail_msg逐层读取。不能沿用旧Object wire。 |
| `response.data.account_info/balance_pay_config/account_recharge_config/delay_pay_config` | 用户详情原生Object N | 只解析状态，不能按请求String(JSON)重复解码，或把查询独有字段回填请求。 |

- 余额扣费charge_mode：内扣01/02/03，默认01；外扣10/11/12，默认10。out_fee_acct_type为01/02/05/09，默认01。余额支付配置的请求out_fee_flag说明未给枚举，不能把查询的1外扣/2内扣反向提升为请求合同；外扣时out_fee_huifuid条件必填。
- LV2企业需营业执照F07，对公结算F08及相应法人证件；LV2个人需对应身份证明。LV3仅企业，另按对公/对私法人提供F08/F13，并提供F22门头、F105收银台、F371办公环境；法定证件材料按完整目录，不能只保留card_type=4规则。
- 升级LV3并开通取现、余额、充值、延迟支付任一功能时sign_user_info必填，电子回单开通条件继续有效。
- 对公打款验证trans_status=1打款中/2打款成功验证中/3打款失败/4通过/5失败；法人活体验证只有1/4/5。与审核Y/P/N、配置S/F及支付终态分开。
- face_url为敏感不透明活体链接，不能回显或写日志。verify_ord_id用于另一个打款验证接口；本次文档未覆盖该接口，不虚构端点、金额或调用实现。
- 当前用户路径644=请求345+响应227+通知72；来源冻结于2026-11-09，本轮相对11-04字节未变；10-25已新增协议配置、协议结果、外扣账户及升级失败原因；两条开户sys_id关系注记绑定在公共请求信封，非data新增字段。

## 业务入驻异步合同

异步外层已声明 `resp_code:String(6) Y`、`resp_desc:String(512) Y`、`sign:String(512) Y`。业务入驻新增的 `data:String(JSON) N`、业务入驻修改的 `data:Json N` 都包含原请求流水、日期、`huifu_id` 和 `notify_type`；当前两页均已把 `async.data.huifu_id:String(18) Y` 的说明统一为汇付客户号，应映射为 `userHuifuId`，不得映射为商户号：

| 通知 | 条件与状态 |
| --- | --- |
| `notify_type=E` | 审核消息；audit_info为String(JSON Object)，audit_status=Y/P/N |
| `notify_type=A` | 业务消息；来源说明audit_info在A/E时返回，配置列表code=S/F；account_info在A/U时返回 |
| `notify_type=U` | 用户升级通知；account_info先解码String(JSON Object)，独立判断升级/验证状态 |
| `notify_type=Z` | `elec_acct_result:String(JSON Object)`；`bank_status=S/F` |

协议结果新增`agreement_info_list:String(JSON Array) N`，其中con_stat为协议状态；协议链接按敏感不透明字符串处理。业务入驻请求的父字段为`agreement_info:String(JSON Object)`，修改请求父字段却正式命名`agreement_type:String(JSON Object)`，其中子字段亦叫agreement_type；完整父路径分别保留，不能自行统一命名。协议类型0电子协议，message_send_type=0发送（默认）/1不发送，触发条件为协议类型电子且业务开通审核通过。

公共异步规范已补齐：汇付以 POST/UTF-8 推送配置类 `data`，默认超时5秒；超时及500-599默认重试3次，不支持重定向，URL 不带查询参数。接收端对原始 `data` 免排序执行 SHA256WithRSA 验签，成功处理后返回 HTTP 200 和 `RECV_ORD_ID_` + `req_seq_id`，并对重复通知做状态感知幂等。完整协议和 Webhook 隔离读取 `user-onboarding-platform-contracts.md`。

## 查询合同

- 申请状态查询必须带真实用户号、当日唯一流水、日期和 `apply_no`；仅用于非同名对公结算卡审核。官网必填列把 `apply_reason/apply_status/huifu_id` 标为 `N`；接入方确认成功查询在 `apply_status=Y/P/N/F` 四种状态都会返回这三个字段。该裁决不能泛化为其他用户申请状态接口。
- 用户信息查询请求只有用户号、流水和日期；官网同样明确 `req_seq_id` 在同一商户号当天唯一。响应大部分字段可选，不能把缺失父对象解释为未开户或失败。
- 用户信息查询的 `ent_base_info`、`indv_base_info`、`card_info`、`settle_config_list`、`qry_cash_config_list`、`qry_cash_card_info_list` 是 String(JSON)；先解一层字符串，再在各自父路径内解析。
- `elec_acct_config`、`elec_receipt_config` 和 `sign_user_info` 均按 String(JSON Object) 解码。
- `response.data.ent_base_info.file_list[]` 与 `response.data.indv_base_info.file_list[]` 当前为 String/jsonArray格式，是解码各自 String(JSON Object) 父字段后仍需再解一层的 String(JSON Array)；完整目录分别保留两组 `file_list[]` 子路径，不得合并。
- `elec_acct_config.elec_card_list` 是解码 `elec_acct_config` 父字符串后的 String(JSON Array)，需要再解一层；保留 `elec_card_list[]` 及子路径，不得按普通对象或直接数组解析。
- `sign_user_info` 的必填列为 `C`，说明为“开通电子回单必填”；按条件和字段存在性解析，不得把响应中缺少该父对象直接判为失败。
- 个人基础信息的省/区示例分别为 `310101/310000`，取现卡的市/省示例分别为 `310000/310100`，与同页其他省市区样例顺序相反。示例不能作为默认编码，必须用外部地区编码表校验。
- `response.data.qry_cash_card_info_list[].branch_code` 原接口行没有链接目标；接入方提供的官方“基础参数汇总”明确给出银行支行编码 XLSX/JSON/CSV 下载入口，现按完整路径绑定该公共编码来源。
- `settle_config_list[].out_settle_acct_type` 正式枚举为 `01/02/05`，当前示例已修正为 `01`。
- `qry_cash_config_list[].weekday_fix_amt` 与 `weekday_fee_rate` 的说明现已统一为 `cash_type=D1` 时生效，并用于 D1 工作日结算。
- `resp_code` 已修正为 `String(8)`，与8位成功码示例一致。

## 用户列表查询合同

- `POST /v2/user/list/query` 精确17个节点：请求8、同步响应9、无异步；请求必填 `legal_cert_no/req_date/req_seq_id`，`upper_huifu_id:String(18) N` 仅用于限定上级范围。
- `response.data.user_list_info_list:String N` 注明 `jsonArray格式`，按一层 String(JSON Array) 解码并保留 `response.data.user_list_info_list[]` 子路径；成功示例使用原生数组，与正式类型冲突。
- 列表项 `huifu_id/upper_huifu_id` 当前正式长度均为18；16位成功示例在上限内，不得沿用旧版长度2。
- 当前请求与成功响应示例均包含正式 `sign:String(512) Y`；生产仍必须加签并验签。`cust_type` 只解析 `1=企业用户` 和 `2=个人用户`。
- 三语言 `V2UserListQueryRequest` 只声明 `legal_cert_no/req_date/req_seq_id`；`upper_huifu_id` 走白名单 exact-key 扩展，且扩展拒绝覆盖三个已声明键。
