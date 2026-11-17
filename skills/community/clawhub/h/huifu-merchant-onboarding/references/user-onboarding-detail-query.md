# 用户信息查询

## 适用范围

查询用户基本信息、结算卡、结算/取现配置、斗拱e账户和电子回单。官方来源：[用户信息查询](https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhywcx.md)。它不是商户详情查询，尽管请求业务字段同样只有 `huifu_id/req_seq_id/req_date`。

## 接口与字段面

- Endpoint：`POST https://api.huifu.com/v2/user/basicdata/query`。
- 快照更新时间：官网 `2026-10-20`，本地冻结 `2026-11-09`；原文 SHA-256：`3347a35c7706eca63557a8e2c24b7048defd5095540ca5ed32832705c89391ca`。
- 共166个字段路径：请求7、同步响应159、异步0；4个根表、16个扩展表，最大深度5。
- 全部请求、响应父子路径、数组层级、类型、长度、Y/N/C 与官方说明读取 `user-onboarding-complete-field-catalog.md`；wire 裁决和官网冲突同时读取 `user-onboarding-field-contracts.md`。
- 请求 `data.huifu_id` 必须是直属用户 ID，不是商户 ID。
- 请求 `data.req_seq_id` 必须保持调用方真实值；官网明确要求同一商户号当天唯一，不得自动换流水或把该规则外推到开户、业务入驻接口。

## 响应解析顺序

外层 `response.data:Json` 的官网必填列为 `N`，接入方确认成功响应一定包含该对象；成功缺失按协议异常，异常响应 DTO 仍允许缺失。以下嵌套组只在父节点存在时解析。

先验外层签名，再读取业务 `data`。以下父字段按 String(JSON) 解一层后，才解析内部字段：

- `ent_base_info`、`indv_base_info`、`card_info`
- `settle_config_list`
- `qry_cash_config_list`、`qry_cash_card_info_list`

`elec_acct_config`、`elec_receipt_config` 和 `sign_user_info` 当前都按 String(JSON Object) 解码。不得把这些父字段当成原生对象，也不得把同名省市、证件、卡字段跨父路径合并。

`response.data.ent_base_info.file_list[]` 与 `response.data.indv_base_info.file_list[]` 当前是解码各自父 String(JSON Object) 后仍需再解一层的 String(JSON Array)。完整目录分别保留两组 `file_list[]` 及子路径，不得合并附件或删除数组层级。

`elec_acct_config.elec_card_list` 按说明和接入方确认，是解码 `elec_acct_config` 后仍需再解一层的 String(JSON Array)。完整目录保留 `elec_card_list[]` 及其14个子路径，不得按普通数组直接解析。

官网把 `elec_card_list[].mp:String(11)` 标为 `C`，现已补充 11 位数字说明；接入方确认 `card_type=1` 对私法人卡要求存在有效手机号，`card_type=0` 对公卡不要求。历史查询响应仍按存在性容错。`sign_user_info` 的必填列现已为 `C`，按开通电子回单条件解析。

本轮新增account_info及充值账户字段仍有空说明，当前详情页已补齐原有标量长度；结构父节点的空长度仍以 `—` 原样保留，不能从同名请求字段补写。

不同响应组均为可选。缺少 `ent_base_info` 或 `indv_base_info` 不能单独推断用户类型、失败或未开户；先检查 `resp_code`，再按存在性解析。

## 新账户等级与配置

response.data.account_info、balance_pay_config、account_recharge_config、delay_pay_config均为原生Object N，共新增21条路径；不要套用请求String(JSON)编码。account_info含account_level/face_url/trans_status/verify_ord_id；活体链接按敏感不透明值处理，验证状态与审核/支付状态隔离。充值响应独有switch_state/transfer_flag_name/transfer_flag_no，不得复制为入驻请求。材料与费用语义见 `user-onboarding-field-contracts.md` 的“用户等级与新资金配置”。

## 官方冲突与安全边界

- 正式表已将 `resp_code` 修正为 `String(8) Y`，与成功示例 `"00000000"` 一致。
- 企业与个人基础信息下两条 `file_list` 当前正式类型均为 String/jsonArray格式；在各自父字符串解码后再解码一层数组字符串。
- `elec_card_list` 当前正式类型为 String/jsonArray字符串；在 `elec_acct_config` 父字符串解码后再解一层。
- `response.data.settle_config_list[].out_settle_acct_type` 正式枚举为 `01/02/05`，当前示例已修正为 `01`。
- `response.data.qry_cash_config_list[].weekday_fix_amt` 与 `weekday_fee_rate` 的说明现已统一为 `cash_type=D1` 时生效，并用于 D1 工作日结算；旧冲突已关闭。
- `indv_base_info.prov_id/district_id` 的示例为 `310101/310000`，`qry_cash_card_info_list[].area_id/prov_id` 的示例为 `310000/310100`，与同页其他省市区示例顺序相反；必须查外部地区编码，不能照抄样例。`qry_cash_card_info_list[].branch_code` 原行缺链接，现使用接入方提供的官方基础参数汇总中的银行支行编码下载入口。
- 示例证明多组 String(JSON) 会以转义字符串返回；每组只解一次，再按自身父路径校验。
- 响应可能含证件、卡号、手机号、邮箱、地址、文件 ID、`token_no` 等高敏信息。使用白名单提取，只输出业务确需的脱敏字段；禁止完整响应日志。
- 查询响应中的配置状态用于展示现状，不能直接复制成业务入驻请求。

官网未声明异步通知。三语言专属类为 `V2UserBasicdataQueryRequest`；不得与 `V2MerchantBasicdataQueryRequest` 混用。

## 2026-10-25 官网更新同步

本地当前来源SHA-256：`3347a35c7706eca63557a8e2c24b7048defd5095540ca5ed32832705c89391ca`。

本轮在response.data.account_info中新增fail_msg:String(256) N；详情account_info仍为原生Object，不沿用业务通知改为String(JSON Object)的编码。该失败原因与审核、绑卡、升级和支付终态分别判断。

| 新增完整合同路径 | 中文名 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `response.data.account_info.fail_msg` | 验证失败原因 | `String` | `256` | `N` | 条件与完整原文见对应完整目录 |
