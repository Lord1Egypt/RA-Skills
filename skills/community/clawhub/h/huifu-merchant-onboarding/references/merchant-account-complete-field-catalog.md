# 商户子账户配置完整字段目录

来源日期：2026-11-09。共2个接口、130条完整字段路径。基础目录及其历史锁独立保留。

## 目录

- 使用规则
- 覆盖摘要
- 子账户开通配置
- 修改子账户配置

## 使用规则

字段身份为接口＋方向＋完整路径，不能按叶字段名去重。类型、长度和Y/N/C为空时保留未知；C按条件必填。String(JSON)逐层编码/解码，数组标记不是wire字段名。官网表与示例冲突须联读原子参考；本目录不将示例修成合同。

两接口管理商户子账户及结算配置；开通与修改的必填性分别保留，审核通知与账户可用状态不得混同。未公布的通知协议见对应原子参考。

## 覆盖摘要

| 接口 | 字段路径 | 根表 | 嵌套表 |
| --- | --- | --- | --- |
| 子账户开通配置 | 66 | 4 | 4 |
| 修改子账户配置 | 64 | 4 | 4 |

## 子账户开通配置

- 官方来源：<https://paas.huifu.com/partners/api/doc/zhgl/api_zhgl_zhpz_kyc.md>
- SHA-256：`b496d1493ed0615115e8972272f0a717289a5feab6206080a62c83615ea9eb8b`

### 请求信封

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商或商户的huifu_id；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为总部商户时，此字段填写商户huifu_id |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 数据 | `Json` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `32` | `Y` | 已确认 | 示例值：rQ[官网示例已脱敏] |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20220905 |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户汇付Id | `String` | `18` | `Y` | 已确认 | 商户号；示例值：[官网示例已脱敏] |
| `request.data.upper_huifu_id` | `request.data.upper_huifu_id` | `—（直接 JSON 路径）` | 上级汇付Id | `String` | `18` | `Y` | 已确认 | 上级商户或渠道商；示例值：[官网示例已脱敏] |
| `request.data.acct_type` | `request.data.acct_type` | `—（直接 JSON 路径）` | 子账户类型 | `String` | `2` | `Y` | 已确认 | 02:现金户；示例值：02 |
| `request.data.acct_name` | `request.data.acct_name` | `—（直接 JSON 路径）` | 账户名称 | `String` | `32` | `Y` | 已确认 | 示例值：现金账户 |
| `request.data.card_info` | `request.data.card_info` | `—（String(JSON) 容器）` | 结算卡信息配置 | `String` | `—` | `C` | [需要官方确认]：长度 | 新账户绑定的结算银行账户。jsonObject格式。若结算规则中上送token_no，则card_info不填。 |
| `request.data.card_info.card_type` | `request.data.card_info` | `$.card_type` | 结算账户类型 | `String` | `1` | `Y` | 已确认 | 0：对公账户 1：对私法人账户 2：对私非法人账户；示例值：0；个人商户不支持填写对公账户和对私非法人账户。 |
| `request.data.card_info.card_name` | `request.data.card_info` | `$.card_name` | 结算账户名 | `String` | `128` | `Y` | 已确认 | 结算银行卡对应的户名；示例值：上海汇付支付有限公司；当card_type=0时填写企业名称；当card_type=1时填写法人姓名，对私法人结算银行户名与法人姓名必需一致；当card_type=2时填写非法人姓名 |
| `request.data.card_info.card_no` | `request.data.card_info` | `$.card_no` | 结算账号 | `String` | `32` | `Y` | 已确认 | 结算银行卡号，为避免资金结算失败，请正确填写； 示例值：[官网示例已脱敏]；注意：系统会验证卡号所属银行，请准确填写 |
| `request.data.card_info.prov_id` | `request.data.card_info` | `$.prov_id` | 银行所在省 | `String` | `6` | `Y` | 已确认 | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000；如修改省市要级联修改 |
| `request.data.card_info.area_id` | `request.data.card_info` | `$.area_id` | 银行所在市 | `String` | `6` | `Y` | 已确认 | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310100；如修改省市要级联修改 |
| `request.data.card_info.bank_code` | `request.data.card_info` | `$.bank_code` | 银行编号 | `String` | `8` | `C` | 已确认 | 当card_type=0时必填，参考： [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm) ； 示例值：01020000 |
| `request.data.card_info.branch_code` | `request.data.card_info` | `$.branch_code` | 联行号 | `String` | `12` | `C` | 已确认 | 当card_type=0时必填，参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `request.data.card_info.cert_type` | `request.data.card_info` | `$.cert_type` | 持卡人证件类型 | `String` | `2` | `C` | 已确认 | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》 当card_type=0时为空， 当card_type=1或2时必填；示例值：00 |
| `request.data.card_info.cert_no` | `request.data.card_info` | `$.cert_no` | 持卡人证件号码 | `String` | `32` | `N` | 已确认 | 如持卡人证件类型为00：身份证，则填写身份证号码；示例值：[官网示例已脱敏]。**系统会做格式校验** |
| `request.data.card_info.cert_validity_type` | `request.data.card_info` | `$.cert_validity_type` | 持卡人证件有效期类型 | `String` | `1` | `N` | 已确认 | 1:长期有效，0:非长期有效；示例值：0 |
| `request.data.card_info.cert_begin_date` | `request.data.card_info` | `$.cert_begin_date` | 持卡人证件有效期开始 | `String` | `8` | `N` | 已确认 | 日期格式：yyyyMMdd，以北京时间为准；示例值：20220125 |
| `request.data.card_info.cert_end_date` | `request.data.card_info` | `$.cert_end_date` | 持卡人证件有效期截止日期 | `String` | `8` | `C` | 已确认 | 日期格式：yyyyMMdd，以北京时间为准。示例值：20220125，当cert_validity_type=0时必填；当cert_validity_type=1时为空 |
| `request.data.card_info.mp` | `request.data.card_info` | `$.mp` | 结算人手机号 | `String` | `11` | `N` | 已确认 | 需为11位数字；示例值：[官网示例已脱敏] |
| `request.data.card_info.verify_code` | `request.data.card_info` | `$.verify_code` | *验证码* | `String` | `6` | `N` | 已确认 | 结算卡修改需要短信验证码，请先调用[商户短信发送接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shdxfs)；示例值：851249 |
| `request.data.card_info.acct_ids` | `request.data.card_info` | `$.acct_ids` | *适用子账户* | `String` | `128` | `N` | 已确认 | 结算卡适用子账户，多个用逗号隔开；示例值：D02348323,D01236743 |
| `request.data.settle_config` | `request.data.settle_config` | `—（String(JSON) 容器）` | 结算规则配置 | `String` | `—` | `N` | [需要官方确认]：长度 | 商户结算规则配置，jsonObject格式 |
| `request.data.settle_config.settle_cycle` | `request.data.settle_config` | `$.settle_cycle` | 结算周期 | `String` | `2` | `Y` | 已确认 | D1：下个自然日到账， T1：下个工作日到账； 示例值：T1 |
| `request.data.settle_config.min_amt` | `request.data.settle_config` | `$.min_amt` | 起结金额 | `String` | `14` | `N` | 已确认 | 起结金额，账户余额大于等于起结金额才会发起结算。不传则不设置起结金额；单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。；示例值：1000.00 |
| `request.data.settle_config.remained_amt` | `request.data.settle_config` | `$.remained_amt` | 留存金额 | `String` | `14` | `N` | 已确认 | 留存金额，该部分资金不会结算。不传则不设置留存金额；单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。；示例值：1000.00 |
| `request.data.settle_config.settle_abstract` | `request.data.settle_config` | `$.settle_abstract` | 结算摘要 | `String` | `128` | `N` | 已确认 | 可自定义结算打款备注，支持配置格式化摘要内容，参见[结算配置示例说明](https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm)；不填默认为空；示例值：汇付商城业务 |
| `request.data.settle_config.out_settle_flag` | `request.data.settle_config` | `$.out_settle_flag` | 手续费外扣标记 | `String` | `1` | `N` | 已确认 | 1:外扣，结算时从out_settle_huifuid账户扣手续费 ；2:内扣，从结算金额中扣手续费，默认为内扣；示例值：2 |
| `request.data.settle_config.out_settle_huifuid` | `request.data.settle_config` | `$.out_settle_huifuid` | 结算手续费外扣商户号 | `String` | `18` | `C` | 已确认 | 填写承担手续费的汇付商户号；当out_settle_flag=1时必填，否则非必填；示例值：[官网示例已脱敏] |
| `request.data.settle_config.out_settle_acct_type` | `request.data.settle_config` | `$.out_settle_acct_type` | 结算手续费外扣账户类型 | `String` | `2` | `N` | 已确认 | 01：基本户（不填默认取值）；05：充值户；09：营销户；示例值：01 |
| `request.data.settle_config.settle_pattern` | `request.data.settle_config` | `$.settle_pattern` | 结算方式 | `String` | `2` | `N` | 已确认 | P0：批次结算，指按照指定结算批次号进行资金结算。不填默认P0；~~P1：定时结算，自定义时间结算是指按照商户指定到账时间进行资金结算。~~；P2:批次定时结算；P0/P2两种结算方式需二选一。示例值：P1 |
| `request.data.settle_config.settle_batch_no` | `request.data.settle_config` | `$.settle_batch_no` | 结算批次号 | `String` | `16` | `N` | 已确认 | 结算方式为P0：批次结算时必填，即将按指定结算批次号进行资金结算；示例值：100；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| `request.data.settle_config.is_priority_receipt` | `request.data.settle_config` | `$.is_priority_receipt` | 是否优先到账 | `String` | `1` | `N` | 已确认 | 当settle_pattern=P0时选填，不填默认为N，该值在结算那批次号[0-500]间生效； Y：是，N：否，示例值：Y |
| `request.data.settle_config.settle_time` | `request.data.settle_config` | `$.settle_time` | 自定义结算处理时间 | `String` | `6` | `N` | 已确认 | 当settle_pattern=P1/P2自定义时间结算时必填；注意：00:00到00:30不能指定；到账时间，格式：HHmmss；示例值：103000 |
| `request.data.settle_config.token_no` | `request.data.settle_config` | `$.token_no` | 卡序列号 | `String` | `20` | `N` | 已确认 | 与card_info不可同时传入；示例值：0097387899 |
| `request.data.settle_config.fixed_ratio` | `request.data.settle_config` | `$.fixed_ratio` | 节假日结算手续费率 | `String` | `6` | `C` | 已确认 | settle_cycle为D1时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；示例值：0.05 |
| `request.data.settle_config.constant_amt` | `request.data.settle_config` | `$.constant_amt` | 节假日结算手续费固定金额 | `String` | `15` | `C` | 已确认 | settle_cycle为D1时必填。单位元，需保留小数点后两位。不收费请填写0.00；settle_cycle结算周期为D1时，遇节假日按此费率结算；示例值：1.00 |
| `request.data.settle_config.workday_fixed_ratio` | `request.data.settle_config` | `$.workday_fixed_ratio` | 工作日结算手续费率 | `String` | `6` | `N` | 已确认 | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；示例值：0.05 |
| `request.data.settle_config.workday_constant_amt` | `request.data.settle_config` | `$.workday_constant_amt` | 工作日结算手续费固定金额 | `String` | `15` | `N` | 已确认 | 单位元，需保留小数点后两位。不填默认为0.00；示例值：1.00 |
| `request.data.async_return_url` | `request.data.async_return_url` | `—（直接 JSON 路径）` | 异步请求地址 | `String` | `120` | `N` | 已确认 | 消息接收地址，http或https协议请求，为空时不推送消息 ；示例值：http://service.example.com/to/path |

### 同步响应信封及 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 交易响应内容体 | `Object` | `—` | `N` | N/A：结构字段长度 | 业务返回参数，jsonObject格式 |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务响应码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `256` | `Y` | 已确认 | [业务响应信息](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：处理成功 |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `18` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.apply_no` | `response.data.apply_no` | `—（直接 JSON 路径）` | 申请单号 | `String` | `18` | `N` | 已确认 | 汇付返回商户开户业务申请单号；示例值：[官网示例已脱敏] |
| `response.data.acct_id` | `response.data.acct_id` | `—（直接 JSON 路径）` | 子账户号 | `String` | `16` | `N` | 已确认 | 示例值：F00598600 |
| `response.data.token_no` | `response.data.token_no` | `—（直接 JSON 路径）` | 绑卡序列号 | `String` | `20` | `N` | 已确认 | 示例值：10004053462 账号开通成功，结算卡绑定失败，该字段不返回值。；请根据返回的子账户号，通过修改子账户结算信息接口进行重试绑定。 |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `N` | 已确认 | [接口加签验签说明](https://paas.huifu.com/partners/guide/#/api_v2jqyq) |

### 审核异步信封及 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `async.resp_code` | `async.resp_code` | `—（直接 JSON 路径）` | 网关返回码 | `String` | `5` | `Y` | 已确认 | 网关返回码 |
| `async.resp_desc` | `async.resp_desc` | `—（直接 JSON 路径）` | 网关返回描述 | `String` | `512` | `Y` | 已确认 | 网关返回描述 |
| `async.sign` | `async.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `2048` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `async.data` | `async.data` | `—（String(JSON) 容器）` | 交易响应内容体 | `String` | `—` | `N` | [需要官方确认]：长度 | 业务返回参数，jsonObject格式 |
| `async.data.sub_resp_code` | `async.data` | `$.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务响应码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：00000000 |
| `async.data.sub_resp_desc` | `async.data` | `$.sub_resp_desc` | 业务返回描述 | `String` | `512` | `Y` | 已确认 | [业务响应信息](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：处理成功 |
| `async.data.req_seq_id` | `async.data` | `$.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 已确认 | 原请求流水号；示例值：[官网示例已脱敏] |
| `async.data.req_date` | `async.data` | `$.req_date` | 请求时间 | `String` | `8` | `Y` | 已确认 | 原请求时间yyyyMMdd；示例值：20221122 |
| `async.data.audit_status` | `async.data` | `$.audit_status` | 审核结果 | `String` | `1` | `Y` | 已确认 | Y：审核通过， N：审核拒绝， F：失败；示例值：S |
| `async.data.audit_desc` | `async.data` | `$.audit_desc` | 审核描述 | `String` | `512` | `N` | 已确认 | 审核结果描述；示例值：审核通过 |
| `async.data.product_id` | `async.data` | `$.product_id` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：MCS |
| `async.data.huifu_id` | `async.data` | `$.huifu_id` | 商户号 | `String` | `18` | `N` | 已确认 | 汇付分配的商户号，示例值：[官网示例已脱敏] |
| `async.data.apply_no` | `async.data` | `$.apply_no` | 申请单号 | `String` | `18` | `N` | 已确认 | 汇付返回商户开户业务申请单号；示例值：[官网示例已脱敏] |
| `async.data.token_no` | `async.data` | `$.token_no` | 卡序列号 | `String` | `20` | `N` | 已确认 | 示例值：10004053462账号开通成功，结算卡绑定失败，该字段不返回值。；请根据返回的子账户号，通过修改子账户结算信息接口进行重试绑定。 |


## 修改子账户配置

- 官方来源：<https://paas.huifu.com/partners/api/doc/zhgl/api_zhgl_xgzh_kyc.md>
- SHA-256：`6c041ff7af41573a97463077062725c6a0ca2815b0d64b64fea6c32e21bd3c05`

### 请求信封

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.sys_id` | `request.sys_id` | `—（直接 JSON 路径）` | 系统号 | `String` | `32` | `Y` | 已确认 | 渠道商或商户的huifu_id；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为总部商户时，此字段填写商户huifu_id |
| `request.product_id` | `request.product_id` | `—（直接 JSON 路径）` | 产品号 | `String` | `32` | `Y` | 已确认 | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | `request.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | `request.data` | `—（直接 JSON 路径）` | 数据 | `Json` | `—` | `Y` | N/A：结构字段长度 | 业务请求参数，具体值参考API文档 |

### 请求 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `request.data.req_seq_id` | `request.data.req_seq_id` | `—（直接 JSON 路径）` | 请求流水号 | `String` | `32` | `Y` | 已确认 | 示例值：rQ[官网示例已脱敏] |
| `request.data.req_date` | `request.data.req_date` | `—（直接 JSON 路径）` | 请求日期 | `String` | `8` | `Y` | 已确认 | 格式yyyyMMdd；示例值：20220905 |
| `request.data.huifu_id` | `request.data.huifu_id` | `—（直接 JSON 路径）` | 商户汇付Id | `String` | `18` | `Y` | 已确认 | 商户号；示例值：[官网示例已脱敏] |
| `request.data.upper_huifu_id` | `request.data.upper_huifu_id` | `—（直接 JSON 路径）` | 上级汇付Id | `String` | `18` | `Y` | 已确认 | 上级商户或渠道商；示例值：[官网示例已脱敏] |
| `request.data.acct_id` | `request.data.acct_id` | `—（直接 JSON 路径）` | 子账户号 | `String` | `16` | `Y` | 已确认 | 示例值：F00598600 |
| `request.data.settle_config` | `request.data.settle_config` | `—（String(JSON) 容器）` | 结算规则配置 | `String` | `—` | `Y` | [需要官方确认]：长度 | 商户结算规则配置，jsonObject格式 |
| `request.data.settle_config.settle_status` | `request.data.settle_config` | `$.settle_status` | 状态 | `String` | `2` | `Y` | 已确认 | 1:开通 0:关闭；示例值：1 |
| `request.data.settle_config.settle_cycle` | `request.data.settle_config` | `$.settle_cycle` | 结算周期 | `String` | `2` | `Y` | 已确认 | D1：下个自然日到账， T1：下个工作日到账； 示例值：T1 |
| `request.data.settle_config.min_amt` | `request.data.settle_config` | `$.min_amt` | 起结金额 | `String` | `14` | `N` | 已确认 | 起结金额，账户余额大于等于起结金额才会发起结算。不传则不设置起结金额；单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。；示例值：1000.00 |
| `request.data.settle_config.remained_amt` | `request.data.settle_config` | `$.remained_amt` | 留存金额 | `String` | `14` | `N` | 已确认 | 留存金额，该部分资金不会结算。不传则不设置留存金额；单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。；示例值：1000.00 |
| `request.data.settle_config.settle_abstract` | `request.data.settle_config` | `$.settle_abstract` | 结算摘要 | `String` | `128` | `N` | 已确认 | 可自定义结算打款备注，支持配置格式化摘要内容，参见[结算配置示例说明](https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm)；不填默认为空；示例值：汇付商城业务 |
| `request.data.settle_config.out_settle_flag` | `request.data.settle_config` | `$.out_settle_flag` | 手续费外扣标记 | `String` | `1` | `N` | 已确认 | 1:外扣，结算时从out_settle_huifuid账户扣手续费 ；2:内扣，从结算金额中扣手续费，默认为内扣；示例值：2 |
| `request.data.settle_config.out_settle_huifuid` | `request.data.settle_config` | `$.out_settle_huifuid` | 结算手续费外扣商户号 | `String` | `18` | `C` | 已确认 | 填写承担手续费的汇付商户号；当out_settle_flag=1时必填，否则非必填；示例值：[官网示例已脱敏] |
| `request.data.settle_config.out_settle_acct_type` | `request.data.settle_config` | `$.out_settle_acct_type` | 结算手续费外扣账户类型 | `String` | `2` | `N` | 已确认 | 01：基本户（不填默认取值）；05：充值户；09：营销户；示例值：01 |
| `request.data.settle_config.settle_pattern` | `request.data.settle_config` | `$.settle_pattern` | 结算方式 | `String` | `2` | `N` | 已确认 | P0：批次结算，指按照指定结算批次号进行资金结算。不填默认P0；~~P1：定时结算，自定义时间结算是指按照商户指定到账时间进行资金结算。~~；P2:批次定时结算；两种结算方式需二选一。示例值：P1 |
| `request.data.settle_config.settle_batch_no` | `request.data.settle_config` | `$.settle_batch_no` | 结算批次号 | `String` | `16` | `C` | 已确认 | 结算方式为P0：批次结算时必填，即将按指定结算批次号进行资金结算；示例值：100；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| `request.data.settle_config.is_priority_receipt` | `request.data.settle_config` | `$.is_priority_receipt` | 是否优先到账 | `String` | `1` | `N` | 已确认 | 当settle_pattern=P0时选填，不填默认为N，该值在结算那批次号[0-500]间生效； Y：是，N：否，示例值：Y |
| `request.data.settle_config.settle_time` | `request.data.settle_config` | `$.settle_time` | 自定义结算处理时间 | `String` | `6` | `C` | 已确认 | 当settle_pattern=P1/P2自定义时间结算时必填；注意：00:00到00:30不能指定；到账时间，格式：HHmmss；示例值：103000 |
| `request.data.settle_config.token_no` | `request.data.settle_config` | `$.token_no` | 卡序列号 | `String` | `20` | `N` | 已确认 | 与card_info不可同时传入 |
| `request.data.settle_config.fixed_ratio` | `request.data.settle_config` | `$.fixed_ratio` | 节假日结算手续费率 | `String` | `6` | `C` | 已确认 | settle_cycle为D1时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；示例值：0.05 |
| `request.data.settle_config.constant_amt` | `request.data.settle_config` | `$.constant_amt` | 节假日结算手续费固定金额 | `String` | `15` | `C` | 已确认 | settle_cycle为D1时必填。单位元，需保留小数点后两位。不收费请填写0.00；settle_cycle结算周期为D1时，遇节假日按此费率结算；示例值：1.00 |
| `request.data.settle_config.workday_fixed_ratio` | `request.data.settle_config` | `$.workday_fixed_ratio` | 工作日结算手续费率 | `String` | `6` | `N` | 已确认 | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；示例值：0.05 |
| `request.data.settle_config.workday_constant_amt` | `request.data.settle_config` | `$.workday_constant_amt` | 工作日结算手续费固定金额 | `String` | `15` | `N` | 已确认 | 单位元，需保留小数点后两位。不填默认为0.00；示例值：1.00 |
| `request.data.card_info` | `request.data.card_info` | `—（String(JSON) 容器）` | 结算卡信息配置 | `String` | `—` | `C` | [需要官方确认]：长度 | 新账户绑定的结算银行账户。jsonObject格式。若结算规则中上送token_no，则card_info不填。 |
| `request.data.card_info.card_type` | `request.data.card_info` | `$.card_type` | 结算账户类型 | `String` | `1` | `Y` | 已确认 | 0：对公账户 1：对私法人账户 2：对私非法人账户；示例值：0；个人商户不支持填写对公账户和对私非法人账户。 |
| `request.data.card_info.card_name` | `request.data.card_info` | `$.card_name` | 结算账户名 | `String` | `128` | `Y` | 已确认 | 结算银行卡对应的户名；示例值：上海汇付支付有限公司；当card_type=0时填写企业名称；当card_type=1时填写法人姓名，对私法人结算银行户名与法人姓名必需一致；当card_type=2时填写非法人姓名 |
| `request.data.card_info.card_no` | `request.data.card_info` | `$.card_no` | 结算账号 | `String` | `32` | `Y` | 已确认 | 结算银行卡号，为避免资金结算失败，请正确填写； 示例值：[官网示例已脱敏]；注意：系统会验证卡号所属银行，请准确填写 |
| `request.data.card_info.prov_id` | `request.data.card_info` | `$.prov_id` | 银行所在省 | `String` | `6` | `Y` | 已确认 | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000；如修改省市要级联修改 |
| `request.data.card_info.area_id` | `request.data.card_info` | `$.area_id` | 银行所在市 | `String` | `6` | `Y` | 已确认 | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310100；如修改省市要级联修改 |
| `request.data.card_info.bank_code` | `request.data.card_info` | `$.bank_code` | 银行编号 | `String` | `8` | `C` | 已确认 | 参考： [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm) ； 示例值：01020000 ；当card_type=0时必填 |
| `request.data.card_info.branch_code` | `request.data.card_info` | `$.branch_code` | 联行号 | `String` | `12` | `C` | 已确认 | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm) 当card_type=0时必填。；示例值：102290026507 |
| `request.data.card_info.cert_type` | `request.data.card_info` | `$.cert_type` | 持卡人证件类型 | `String` | `2` | `C` | 已确认 | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》 当card_type=0时为空， 当card_type=1或2时必填；示例值：00 |
| `request.data.card_info.cert_no` | `request.data.card_info` | `$.cert_no` | 持卡人证件号码 | `String` | `32` | `N` | 已确认 | 如持卡人证件类型为00：身份证，则填写身份证号码；示例值：[官网示例已脱敏]。**系统会做格式校验** |
| `request.data.card_info.cert_validity_type` | `request.data.card_info` | `$.cert_validity_type` | 持卡人证件有效期类型 | `String` | `1` | `N` | 已确认 | 1:长期有效，0:非长期有效；示例值：0 |
| `request.data.card_info.cert_begin_date` | `request.data.card_info` | `$.cert_begin_date` | 持卡人证件有效期开始 | `String` | `8` | `N` | 已确认 | 日期格式：yyyyMMdd，以北京时间为准；示例值：20220125 |
| `request.data.card_info.cert_end_date` | `request.data.card_info` | `$.cert_end_date` | 持卡人证件有效期开始 | `String` | `8` | `C` | 已确认 | 日期格式：yyyyMMdd，以北京时间为准；示例值：20220125，当cert_validity_type=0时必填；当cert_validity_type=1时为空 |
| `request.data.card_info.mp` | `request.data.card_info` | `$.mp` | 结算人手机号 | `String` | `11` | `N` | 已确认 | 示例值：[官网示例已脱敏] |
| `request.data.card_info.verify_code` | `request.data.card_info` | `$.verify_code` | *验证码* | `String` | `6` | `N` | 已确认 | 结算卡修改需要短信验证码，请先调用[商户短信发送接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shdxfs)；示例值：851249 |
| `request.data.card_info.acct_ids` | `request.data.card_info` | `$.acct_ids` | *适用子账户* | `String` | `128` | `N` | 已确认 | 结算卡适用子账户，多个用逗号隔开；示例值：D02348323,D01236743 |
| `request.data.async_return_url` | `request.data.async_return_url` | `—（直接 JSON 路径）` | 异步请求地址 | `String` | `120` | `N` | 已确认 | 格式：http或https协议请求，为空不推送审核消息。；示例值：http://service.example.com/to/path |

### 同步响应信封及 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `response.data` | `response.data` | `—（直接 JSON 路径）` | 交易响应内容体 | `Object` | `—` | `N` | N/A：结构字段长度 | 业务返回参数，jsonObject格式 |
| `response.data.resp_code` | `response.data.resp_code` | `—（直接 JSON 路径）` | 业务响应码 | `String` | `8` | `Y` | 已确认 | [业务响应码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：00000000 |
| `response.data.resp_desc` | `response.data.resp_desc` | `—（直接 JSON 路径）` | 业务响应信息 | `String` | `256` | `Y` | 已确认 | [业务响应信息](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：处理成功 |
| `response.data.huifu_id` | `response.data.huifu_id` | `—（直接 JSON 路径）` | 商户号 | `String` | `18` | `Y` | 已确认 | 示例值：[官网示例已脱敏] |
| `response.data.token_no` | `response.data.token_no` | `—（直接 JSON 路径）` | 绑卡序列号 | `String` | `20` | `N` | 已确认 | 可用于结算与取现；账号开通成功，结算卡绑定失败，该字段不返回值；示例值：10004053462 |
| `response.sign` | `response.sign` | `—（直接 JSON 路径）` | 加签结果 | `String` | `512` | `N` | 已确认 | [接口加签验签说明](https://paas.huifu.com/partners/guide/#/api_v2jqyq) |

### 审核异步信封及 data

| 合同定位路径 | wire路径 | String(JSON)解码后路径 | 中文名 | 类型 | 长度 | 必填 | 确认状态 | 官方说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `async.resp_code` | `async.resp_code` | `—（直接 JSON 路径）` | 网关返回码 | `String` | `5` | `Y` | 已确认 | 网关返回码 |
| `async.resp_desc` | `async.resp_desc` | `—（直接 JSON 路径）` | 网关返回描述 | `String` | `512` | `Y` | 已确认 | 网关返回描述 |
| `async.sign` | `async.sign` | `—（直接 JSON 路径）` | 签名 | `String` | `2048` | `Y` | 已确认 | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `async.data` | `async.data` | `—（String(JSON) 容器）` | 交易响应内容体 | `String` | `—` | `N` | [需要官方确认]：长度 | 业务返回参数，jsonObject格式 |
| `async.data.sub_resp_code` | `async.data` | `$.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | 已确认 | [业务响应码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：00000000 |
| `async.data.sub_resp_desc` | `async.data` | `$.sub_resp_desc` | 业务返回描述 | `String` | `512` | `Y` | 已确认 | [业务响应信息](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：处理成功 |
| `async.data.req_seq_id` | `async.data` | `$.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 已确认 | 原请求流水号；示例值：rQ[官网示例已脱敏] |
| `async.data.req_date` | `async.data` | `$.req_date` | 请求时间 | `String` | `8` | `Y` | 已确认 | 原请求时间yyyyMMdd；示例值：20221213 |
| `async.data.audit_status` | `async.data` | `$.audit_status` | 审核结果 | `String` | `1` | `Y` | 已确认 | Y：审核通过 N：审核拒绝 F：失败；示例值：Y |
| `async.data.audit_desc` | `async.data` | `$.audit_desc` | 审核描述 | `String` | `512` | `N` | 已确认 | 审核结果描述；示例值：审核通过 |
| `async.data.product_id` | `async.data` | `$.product_id` | 产品编号 | `String` | `32` | `Y` | 已确认 | 汇付产品编号；示例值：YYZY |
| `async.data.huifu_id` | `async.data` | `$.huifu_id` | 汇付客户号 | `String` | `18` | `N` | 已确认 | 商户号；示例值：[官网示例已脱敏] |
| `async.data.apply_no` | `async.data` | `$.apply_no` | 申请单号 | `String` | `18` | `N` | 已确认 | 汇付返回商户开户业务申请单号；示例值：[官网示例已脱敏] |
| `async.data.token_no` | `async.data` | `$.token_no` | 绑卡id | `String` | `20` | `N` | 已确认 | 账号开通成功，结算卡绑定失败，该字段不返回值；示例值：10000093623 |
