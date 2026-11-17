# 商户业务开通修改

## 适用范围

用于企业或小微商户进行微信/支付宝/抖音补开、部分线上业务开通，或修改已开通支付能力的参数和费率。官方来源：[商户业务开通修改](https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md)，官网更新时间 `2026-11-09`，本地活动快照 `2026-11-09`，原文 SHA-256 为 `3f9e0e6b302807646b4a7a02830ef50ae4c6b90f5fab1ddea9eaeb72d12c5cf4`。银联、银行卡业务开通仍使用 `merchant-onboarding-business-open.md`；不能把所有“已开通后的补开”统一路由到本接口。

本接口不是首次基础进件，也不是支付下单接口。首次业务开通以及银联、银行卡业务开通使用 `merchant-onboarding-business-open.md`；支付交易交给 `$huifu-pay-integration`。

## 已确认的接口合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/busi/modify`。
- 请求顶层为 `sys_id:String(32) Y`、`product_id:String(32) Y`、`sign:String(512) Y`、`data:Json Y`。
- 同步响应顶层为 `sign:String(512) Y`、`data:Json N`。
- 完整目录共465个节点：请求 403、同步响应 6、异步通知 56。56 组嵌套表、完整路径、类型、长度、Y/N/C 和经过固定规范化、敏感示例脱敏的官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“商户业务开通修改”；下载原始字节保存在仓库维护来源锁中，不进入发布包。
- 请求 `data.req_seq_id:String(32) Y`、`data.req_date:String(8) Y`、`data.huifu_id:String(18) Y`。其余能力、费率、协议、材料和渠道配置必须按调用方实际修改目标取值，不得从首次开通请求或详情响应整包复制。

## 修改语义与方向隔离

- 本接口用于“修改已开通能力”；同步 `resp_code` 成功只表示本次请求受理或处理结果，不能直接解释为全部能力已可交易。
- `data.async_return_url:String(128) N` 接收申请审核结果；`data.busi_async_return_url:String(128) N` 接收逐业务开通结果；电子协议通知地址位于 `data.agreement_info.agreement_async_return_url`。
- `data.recon_resp_addr:String(256) N` 是交易异步应答地址，不是本接口审核回调，也不能套用支付通知终态逻辑。
- 审核通知、逐业务通知和电子协议通知是三个方向。字段必须分别使用 `async.audit.*`、`async.business.*` 和 `async.agreement.*` 路径。
- 逐业务通知存在 `async.business.ord_id:String(44) N` 时，官方说明的应答是 `RECV_ORD_ID_` + `ord_id`；不得外推到审核或电子协议通知。
- 逐业务通知的 `async.business.reg_result_list[]` 是数组；最新正式类型为Array（说明仍误拼 `josnArray`），目录按正式数组类型保留 `[]`，不得扁平化其 14 个子字段。
- `async.business.huifu_id:String(18) Y` 按字段名和中文名是商户号，但官网说明与示例误写为产品号 `YYZY`；标记 `[官方文档口径冲突]`，禁止采用该示例生成或覆盖商户号。
- 电子协议通知的父字段现定义为 `Object`，完整路径为 `async.agreement.agreement_info_list.con_stat`；不得因 `_list` 名称或申请状态查询中的同名数组而添加 `[]`。

## 字段生成规则

1. 先在完整字段目录定位本次要修改的能力父对象，再读取该对象全部叶子。
2. 保留官方 `String(JSON Object/Array)` 形态；路径仅在官方类型或说明为 `Array/jsonArray` 时带 `[]`。`async.business.reg_result_list[]` 当前已正式声明Array，不再依赖旧版拼写例外。
3. `online_flag/quick_flag/withhold_flag` 仍使用字符串 `Y/N`；不得复制详情查询响应中的 `1/0/空`。
4. 费率、MCC、商户简称、外扣承担方、渠道配置和材料均由调用方或运营提供；官网示例不是默认值。
5. 字段说明命中编码表、XLSX、协议或其他页面时，同时读取 `merchant-onboarding-external-resources.md` 并输出未经改写的原始地址。
6. `wx_zl_conf.wx_zl_pay_conf_list` 当前是String(512) Y且没有JSON格式说明；不得继续沿用旧数组wire，目录不加[]。其新增sales_info.fee_rate_file_list.file_id/file_type必须保留。`jxf_conf_info.jxf_bank_pay_info.jxf_fee_info/split_ext_info/acct_split_bunch_list` 正式类型改为Object但说明仍有JSON字符串/数组描述，逐路径标记冲突。`agreement_info` 为C；多处子字段由Y改N，仍联读条件说明。
7. 捷行付改为 `request.data.jxf_conf_info.default_channel/jxf_bank_pay_info/wx_ent_pay_info`；银行手续费位于 `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info`，微信企业码手续费位于 `request.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info`，各自按所属模式构造，不能把所有费率都放入银行层。修改的 `bank_pay_open_flag`、`wx_ent_pay_open_flag` 及其条件不复制给首次开通。开通/修改/查询的条件、长度和Y/N/C分别使用，不套同一DTO。`request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.sign_start_date` 正式String(8) C，示例为8位YYYYMMDD。官网2026-11-09已将长度从7修正为8，原长度冲突已解决；按8位日期校验，不截断为7位，必填条件仍为银行名称非平安时填写。fee_charge_type不进入正式DTO。
8. `online_fee_conf_list[].fee_formula_type:String N` 只在代扣开通时传入，枚举限 `01/02/03/04`，不得从其他费率对象复制同名字段。

## 公共请求头

- `jpt-x-skill-source: <skill_source>` 必须按 `shared-request-header-policy.md` 生成；仅进件默认 `hfms/1.2.0`，双 Skill 默认 `hfps/1.6.0;hfms/1.2.0`。

## SDK 证据

用户提供且已锁定源码树摘要的 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 均存在对应封装：

- Java / PHP：`V2MerchantBusiModifyRequest`
- Python：`V2MerchantBusiModifyRequest`，模块 `v2_merchant_busi_modify_request.py`

SDK 类存在只证明路由和请求封装可用，不证明商户权限、费率、材料或审核结果。Java 代码仍必须在任何 SDK 请求前全局设置 `BasePay.debug = false;`。

三个生成类均未声明 `jxf_conf_info`、`online_fee_conf_list` 和新增 `dy_conf_list`，通过请求字段白名单的 exact-key 扩展传入；`dy_conf_list` 按当前正式 String/jsonArray 合同整体序列化一层，不能沿用旧版原生数组形态。扩展后合并会覆盖已声明定位字段，必须先拒绝覆盖再发送。

## 通知边界

除上述 `ord_id` 应答规则外，通知验签原文、HTTP 编码、超时、重试及审核/电子协议 ACK 均为 `[需要官方确认]`。按 `shared-overview.md` 的开发提醒引用本页官方来源，建议核对或咨询汇付官方/交流群；继续 Controller 与业务处理框架，未知协议用 TODO/配置隔离，不编造或等待答复才继续整体开发。

## 2026-10-08 字段复核

`request.data.ali_conf_list[].switch_state` 与 `request.data.wx_conf_list[].switch_state` 均由 N 修为 Y；传入对应配置项时必须提供。支付宝项的“默认1”说明已移除，不能再省略后假定开通。该变更只适用于本接口的这两个完整路径，其他配置组以各自正式表为准。

本轮来源复核：2026-11-09；官方最近更新2026-11-09；SHA-256：`3f9e0e6b302807646b4a7a02830ef50ae4c6b90f5fab1ddea9eaeb72d12c5cf4`；<https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md>。
