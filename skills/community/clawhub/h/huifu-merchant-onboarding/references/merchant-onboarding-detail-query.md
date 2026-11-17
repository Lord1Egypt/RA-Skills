# 商户详细信息查询

## 适用范围

用于已获得目标 `huifu_id` 后的服务端最小化资料核对。官方来源：[商户详细信息查询](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md)。它不是申请单状态查询，也不能用于前端轮询或回调重放。

## 已确认的请求合同

- Endpoint：`POST https://api.huifu.com/v2/merchant/basicdata/query`；顶层使用 `sys_id`、`product_id`、`sign`、`data`。
- 官网更新时间 `2026-11-03`；本地活动快照 `2026-11-09`；原文 SHA-256：`3fb7115e030937181c3040f8d57c16ce8b44aa75fb78849d950af8816fc0a918`。
- 请求与响应 602 个具名路径（含父容器；请求7、响应595）的类型、长度、Y/N/C 和官方说明见 `merchant-onboarding-complete-field-catalog.md` 的“商户详细信息查询”；本页的字段白名单策略不能替代完整目录。
- `data` 必填新的 `req_seq_id:String(32)`（当天同商户唯一）、`req_date:String(8)`（`yyyyMMdd`、北京时间）、目标 `huifu_id:String(18)`；高风险约束见 `merchant-onboarding-field-contracts.md`。
- 响应可能覆盖主体、证照、图片、结算卡、结算/取现、协议、渠道配置和账户资料；按查询目的字段白名单读取，禁止沉淀完整响应表或完整原文。
- 若白名单字段说明带 MCC/地区/证件/银行编码表、图片上传文档、签约规则或线上材料 XLSX，必须同时读取 `merchant-onboarding-external-resources.md`，并按响应完整路径单列 `外部资料提示`、给出未经改写的原始地址；不得把响应中的示例/运行时 URL 当资料或请求默认值。

## 请求与响应值域隔离

本接口请求只有 `req_seq_id:String(32) Y`、`req_date:String(8) Y`、`huifu_id:String(18) Y`。其余字段均为响应字段，不得放入请求。

- 响应 `data.quick_flag/online_flag/withhold_flag/pre_authorization_flag/web_flag/balance_pay_flag` 是 `String(1) N`，值域为 `1=开通`、`0=未开通`、空=未配置。
- 上述 `1/0/空` 只用于解析当前状态。业务开通请求 `data.online_flag/quick_flag/withhold_flag` 使用 `Y/N`，预授权请求使用 `data.alipay_pre_auth_flag` / `data.wechatpay_pre_auth_flag=Y/N`；禁止把查询响应直接复制为开通请求。
- 响应 `data.sms_send_flag=Y/N` 表示注册短信是否发送；企业/个人进件请求的同名字段使用 `M/E/A/空`。禁止跨方向复用。
- 响应 `data.cust_type=1/2` 表示企业/个人；`data.ent_type=1/2/3/4/5/6/7/9` 表示企业种类；它们不是可由调用方猜填的请求参数。
- 请求与响应 DTO 分开建模。企业请求 `reg_name:String(64)`、个人请求 `reg_name:String(32)`，本接口响应 `reg_name:String(128)`，不得共享同一长度校验。
- `response.data.material_card_info:String(JSON Object) N` 是独立的对公卡信息；先严格反序列化，再读取 `card_type/card_name/card_no/prov_id/area_id/branch_code` 六个子字段，其中省市不得与响应顶层或其他卡对象的同名字段合并。
- 当前 `response.data.service_phone:String(32)` 已修正旧11位冲突。正式表已删除 `response.data.share_holder_info_list[].cert_no`，不得从请求股东DTO补回。material_card_info.branch_code响应长度12，不得套用企业请求的8位。
- 捷行付响应保留 `response.data.jxf_conf_info.jxf_bank_pay_info.bank_name`，以及独立的default_channel与wx_ent_pay_info，按响应方向类型和N/C保留；线上费率保留 `response.data.online_fee_conf_list[].fee_formula_type:String N`。支付宝、微信配置各自的外扣字段必须按父数组隔离，不能与顶层公共外扣字段合并；抖音 `response.data.qry_dy_conf_list[]` 当前为原生Array，其dy_mer_infos为String(JSON)；`split_bill_result[].acct_split_bunch_list[]` 当前为String(JSON Array)。`merge_pay_config_info.merge_pay_config`正式Object与字符串说明冲突须确认。
- `response.data.qry_cash_config_list[].weekday_fix_amt` 与 `weekday_fee_rate` 的官网说明已统一为 `cash_type=D1` 时生效，并用于 D1 工作日结算；旧版“不生效/生效”冲突已关闭，不再触发硬停。

## 公共请求头

- 在已核验源码基线中，Java 与 PHP 使用 Skill 调用时都要求 `jpt-x-skill-source: <skill_source>`；Java `3.0.41` 与 PHP `2.0.31` 的官方 SDK 主链路会在配置来源值后自动补该头。Python `2.0.28` 同样从 `MerConfig.jpt_x_skill_source` 自动补头。

## 数据边界

- 响应中的证件号、银行卡号、地址、联系人、图片资料和 `token_no` 默认不记录原文、不下发前端、不写日志。
- 必须持久化时采用字段级加密、最小权限、访问审计和保留期；日志只保留掩码或不可逆摘要。
- 审核或渠道状态不明时改用申请单状态查询，不凭详情字段推断审核成功。

## SDK 证据边界

已核验源码基线 Java `3.0.41`、PHP `2.0.31`、Python `2.0.28` 都有 `V2MerchantBasicdataQueryRequest` 作为可选封装，字段仅定位到 `req_seq_id`、`req_date`、`huifu_id`。调用方必须为本次查询生成新的当天唯一流水；SDK 默认响应验签路径不等于允许保存完整响应。

## 2026-10-25 官网更新同步

2026-10-25历史来源SHA-256：`f8fb851eddda3219a5e4feb037b81cc5eed4697903644489e7cccde4fa72bdde`。

新增五项switch_state：支付宝、微信、银行卡、银联和合单业务各自的配置状态。它们只用于详情响应的实际状态判断，不可直接复制为业务开通请求。

| 新增完整合同路径 | 中文名 | 类型 | 长度 | 必填 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `response.data.combine_pay_config.switch_state` | 功能开关 | `String` | `1` | `Y` | 条件与完整原文见对应完整目录 |
| `response.data.qry_ali_conf_list[].switch_state` | 功能开关 | `String` | `1` | `Y` | 条件与完整原文见对应完整目录 |
| `response.data.qry_bank_card_conf.switch_state` | 功能开关 | `String` | `1` | `Y` | 条件与完整原文见对应完整目录 |
| `response.data.qry_union_conf.switch_state` | 功能开关 | `String` | `1` | `Y` | 条件与完整原文见对应完整目录 |
| `response.data.qry_wx_conf_list[].switch_state` | 功能开关 | `String` | `1` | `Y` | 条件与完整原文见对应完整目录 |

本轮来源复核：2026-11-09；官方最近更新2026-11-03；SHA-256：`3fb7115e030937181c3040f8d57c16ce8b44aa75fb78849d950af8816fc0a918`；<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md>。
