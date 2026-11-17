# 进件扩展十二接口完整字段目录

本文件由仓库维护脚本从锁定的十二份官方原文机械生成，覆盖电子合同、下级商户权限、统一页面进件及微信/支付宝 AT 管理。条件必填、官方冲突、路由和 SDK 边界仍须同时读取对应原子接口 reference 与 `onboarding-extension-field-contracts.md`。

安全说明：官网说明中的证件号、手机号、邮箱、密钥、二维码、合同链接和长流水已机械脱敏；字段名、枚举、条件、材料编号和资料链接保持原文。

## 目录

- [使用规则](#使用规则)
- [生成覆盖摘要](#生成覆盖摘要)
- [电子合同接口](#电子合同重发)
- [页面进件与下级权限](#开通下级商户权限配置)
- [微信与支付宝 AT 管理](#微信商户配置)

## 使用规则

1. 十二个接口都保留独立 DTO；不得因同属进件流程而复用商户详情、用户开户或支付交易模型。
2. 按完整路径区分同名字段；String(JSON) 仅按接口级合同编码，不能由 `*_list` 名称猜测。
3. 官网类型、长度、必填、字段名与示例冲突时，目录保留正式参数表原值并标记官方证据，不以示例覆盖。
4. 微信/支付宝实名、页面进件和配置异步通知分别建模；未声明的 ACK、重试、超时和验签原文保持 `[需要官方确认]`。

## 生成覆盖摘要

| 接口 | 字段路径总数 | 扩展表数量 | 最大路径深度 |
| --- | ---: | ---: | ---: |
| 电子合同重发 | 13 | 0 | 3 |
| 电子合同列表查询 | 40 | 1 | 4 |
| 电子合同拒签 | 12 | 0 | 3 |
| 开通下级商户权限配置 | 141 | 21 | 4 |
| 商户统一进件（页面版） | 59 | 1 | 5 |
| 统一进件页面版查询 | 51 | 5 | 4 |
| 微信商户配置 | 31 | 1 | 4 |
| 微信商户配置查询 | 32 | 3 | 5 |
| 微信实名认证 | 51 | 2 | 4 |
| 微信实名认证状态查询 | 22 | 0 | 3 |
| 支付宝实名申请提交 | 69 | 7 | 5 |
| 支付宝实名申请单查询 | 25 | 2 | 4 |

## 电子合同重发

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/fp/api_fp_dzhtcf.md>
- SHA-256：`169b62c666fbe0345ab4f5b10f7f39116d5fd774f6a04ec6abdb77c3923a156e`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号，同一商户号当天唯一 |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd，以北京时间为准 |
| `request.data.huifu_id` | 汇付商户号 | `String` | `32` | `Y` | 渠道与一级代理商的直属商户ID |
| `request.data.agreement_id` | 协议编号 | `String` | `32` | `Y` | — |
| `request.data.sign_user_email` | 个人邮箱 | `String` | `64` | `Y` | — |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：00000000 |
| `response.data.resp_desc` | 业务返回描述 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：成功；签约链接从生成起7天有效，如果超过七天请重新发起电子合同重发 |

## 电子合同列表查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/fp/api_fp_dzhtsqlbcx.md>
- SHA-256：`2a774b8820cdb4e5e4dc1364f1be9bcdcfc273b7b86e064aa3c631c97e8d397b`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd，以北京时间为准 |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号，同一商户号当天唯一 |
| `request.data.huifu_id` | 汇付商户号 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.agreement_id` | 协议编号 | `String` | `32` | `N` | 示例值：[官网示例已脱敏] |
| `request.data.scene_code` | 场景类型 | `String` | `32` | `N` | MER_REGIST-商户入驻，MER_MODIFY-商户变更，MER_KYC-商户聚合示例值：MER_REGIST |
| `request.data.sign_status` | 协议状态 | `String` | `32` | `N` | WAIT_SIGN-待签约SIGNING-签约中SIGN_SUCCESS-签约完成EXPIRE_SIGN-失效SIGN_REJECT-已拒签SIGN_FAIL-签约失败示例值：SIGN_FAIL |
| `request.data.order_id` | 申请单号 | `String` | `32` | `N` | 示例值：[官网示例已脱敏] |
| `request.data.mer_name` | 商户名称 | `String` | `128` | `N` | 示例值：中国建筑工程总公司 |
| `request.data.agreement_type` | 协议类型 | `String` | `18` | `Y` | ELECT-电子 |
| `request.data.page_num` | 当前页 | `String` | `10` | `Y` | 示例值：1 |
| `request.data.page_size` | 分页大小 | `String` | `10` | `Y` | 示例值：10 |
| `request.data.product_id` | 产品号 | `String` | `32` | `N` | 示例值：CYL |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：00000000 |
| `response.data.resp_desc` | 业务返回描述 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：处理成功 |
| `response.data.total_size` | 总条数 | `String` | `10` | `N` | — |
| `response.data.page_num` | 当前页 | `String` | `10` | `N` | — |
| `response.data.page_size` | 分页大小 | `String` | `10` | `N` | — |
| `response.data.result_list[]` | 结果列表 | `String` | `—` | `N` | jsonArray格式,若无协议，该字段不返回 |
| `response.data.result_list[].agreement_id` | 协议编号 | `String` | `32` | `N` | 协议编号 |
| `response.data.result_list[].mer_name` | 商户名称 | `String` | `128` | `N` | 示例值：中国建筑工程总公司 |
| `response.data.result_list[].huifu_id` | 商户号 | `String` | `32` | `N` | 商户号 |
| `response.data.result_list[].agreement_name` | 协议名称 | `String` | `64` | `N` | 协议名称 |
| `response.data.result_list[].sign_status` | 协议状态 | `String` | `32` | `N` | WAIT_SIGN-待签约,SIGNING-签约中,SIGN_SUCCESS-签约完成,EXPIRE_SIGN-失效,SIGN_REJECT-已拒签,SIGN_FAIL-签约失败 |
| `response.data.result_list[].sign_status_desc` | 协议状态描述 | `String` | `32` | `N` | 示例值：待签约 |
| `response.data.result_list[].create_time` | 创建时间 | `String` | `16` | `N` | 示例值：20260508184332 |
| `response.data.result_list[].start_date` | 合同有效期起始日 | `String` | `8` | `N` | 示例值：20260508 |
| `response.data.result_list[].expiration_date` | 合同失效日 | `String` | `8` | `N` | 示例值：20270508 |
| `response.data.result_list[].sign_url` | 合同签署链接 | `String` | `128` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.result_list[].agreement_type` | 协议类型 | `String` | `32` | `N` | ELECT-电子；示例值：ELECT |
| `response.data.result_list[].agreement_type_name` | 协议类型名称 | `String` | `500` | `N` | 电子；示例值：电子 |
| `response.data.result_list[].download_url` | 下载地址 | `String` | `256` | `N` | — |
| `response.data.result_list[].scene_code` | 场景类型 | `String` | `32` | `N` | MER_REGIST-商户入驻、MER_MODIFY-商户变更、MER_KYC-商户聚合 |
| `response.data.result_list[].scene_code_desc` | 场景类型描述 | `String` | `64` | `N` | — |
| `response.data.result_list[].order_id` | 申请单号 | `String` | `64` | `N` | 申请单号 |

## 电子合同拒签

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/fp/api_fp_dzhtjq.md>
- SHA-256：`ec6aea1f10e1ab3113993d16422214e9a3aaa586e71bcd646841f45ad60c1f9e`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd，以北京时间为准 |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号，同一商户号当天唯一 |
| `request.data.huifu_id` | 汇付商户号 | `String` | `18` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.agreement_id` | 协议编号 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：00000000 |
| `response.data.resp_desc` | 业务返回描述 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm)；示例值：成功 |

## 开通下级商户权限配置

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_xjshpz.md>
- SHA-256：`e213479c4b3bb355dd8bbccefcee1d1980e12f83af2fb14323760c6776d24d8f`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `16` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，例MCS |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号；示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求时间 | `String` | `8` | `Y` | 请求时间 yyyyMMdd；示例值：20220125 |
| `request.data.huifu_id` | 汇付客户Id | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID；示例值：666600010885495 |
| `request.data.product_id` | 产品编号 | `String` | `16` | `Y` | 汇付分配的产品号，示例值:MCS |
| `request.data.upper_huifu_id` | 直属渠道号 | `String` | `18` | `C` | 该商户进件完成后归属的渠道商huifu_id；sys_id主体为渠道商时填写；sys_id主体为总部商户时选填；示例值：[官网示例已脱敏] |
| `request.data.ali_conf_list[]` | 支付宝配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.ali_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 1、线下扫码（正扫&反扫&台牌），2、线上扫码，示例值：1 |
| `request.data.ali_conf_list[].fee_rate` | 手续费 | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.ali_conf_list[].open_flag` | 允许开通该业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.ali_conf_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `6` | `N` | 固定金额保留2位小数；大于0。示例值：0.38 |
| `request.data.wx_conf_list[]` | 微信配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.wx_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 1：线下反扫；2：线下公众号；3：线下小程序；4：线上公众号；5：线上小程序；12：线上反扫；13：APP支付；示例值：1 |
| `request.data.wx_conf_list[].fee_rate` | 手续费 | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.wx_conf_list[].open_flag` | 允许开通该场景业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.wx_conf_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `6` | `N` | 固定金额保留2位小数；大于0。示例值：0.38 |
| `request.data.union_conf_list[]` | 银联二维码配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.union_conf_list[].charge_cate_code` | 银联业务手续费类型 | `String` | `2` | `N` | 03-标准类 小微商户仅有03 标准类 ；04-线上费率（银联二维码线上）；默认03标志类 |
| `request.data.union_conf_list[].debit_fee_rate_up` | 借记卡手续费1000以上(%) | `String` | `9` | `Y` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.union_conf_list[].debit_fee_limit_up` | 借记卡封顶1000以上（元） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；示例值：20.00 |
| `request.data.union_conf_list[].credit_fee_rate_up` | 银联二维码业务贷记卡手续费1000以上(%) | `String` | `9` | `Y` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.union_conf_list[].debit_fee_rate_down` | 借记卡手续费1000以下(%) | `String` | `9` | `Y` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.union_conf_list[].debit_fee_limit_down` | 借记卡封顶1000以下（元） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；示例值：20.00 |
| `request.data.union_conf_list[].credit_fee_rate_down` | 银联二维码业务贷记卡手续费1000以下(%) | `String` | `9` | `Y` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.union_conf_list[].open_flag` | 允许开通银联二维码业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.bank_card_config` | 银联卡配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `request.data.bank_card_config.debit_fee_rate` | 借记卡手续费（%） | `String` | `9` | `Y` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]； 示例值：0.60 |
| `request.data.bank_card_config.debit_fee_limit` | 借记卡封顶值 | `String` | `9` | `N` | 数字类型，大于0保留2位小数； 示例值：20.00 |
| `request.data.bank_card_config.credit_fee_rate` | 贷记卡手续费（%） | `String` | `9` | `Y` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.90 |
| `request.data.bank_card_config.cloud_debit_fee_rate_up` | 银联手机闪付借记卡手续费1000以上（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.bank_card_config.cloud_debit_fee_limit_up` | 银联手机闪付借记卡封顶1000以上（元） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；示例值：20.00 |
| `request.data.bank_card_config.cloud_credit_fee_rate_up` | 银联手机闪付贷记卡手续费1000以上（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.bank_card_config.cloud_debit_fee_rate_down` | 银联手机闪付借记卡手续费1000以下（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.bank_card_config.cloud_debit_fee_limit_down` | 银联手机闪付借记卡封顶1000以下（元） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；示例值：20.00 |
| `request.data.bank_card_config.cloud_credit_fee_rate_down` | 银联手机闪付贷记卡手续费1000以下（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.bank_card_config.open_flag` | 允许开通银行卡业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.split_config` | 分账配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `request.data.split_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.split_config.fee_fix_amt` | 固定手续费(元) | `String` | `9` | `N` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.split_config.open_flag` | 允许开通分账业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.wx_zl_conf_list[]` | 微信直连配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.wx_zl_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 1、微信直连小程序；2、微信直连公众号；3、微信直连H5；示例值：1 |
| `request.data.wx_zl_conf_list[].fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.wx_zl_conf_list[].open_flag` | 允许开通微信直连业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.ali_zl_conf` | 支付宝直连配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `request.data.ali_zl_conf.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.ali_zl_conf.open_flag` | 允许开通支付宝直连业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.online_fee_conf_list[]` | 线上配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.online_fee_conf_list[].bus_type` | 业务类型 | `String` | `2` | `Y` | 1.网银支付，；2.快捷支付，；3.手机WAP支付,；4：B2B网银充值，；5：B2C网银充值；6：代扣支付;；示例值：1 |
| `request.data.online_fee_conf_list[].dc_flag` | 借贷记标识 | `String` | `2` | `Y` | D:借记,C:贷记；B2B网银填写D；示例值：D |
| `request.data.online_fee_conf_list[].fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，最低传入0.00,示例值：1.00 |
| `request.data.online_fee_conf_list[].bank_code` | 银行号 | `String` | `8` | `Y` | 8位银行号 |
| `request.data.online_fee_conf_list[].fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.online_fee_conf_list[].open_flag` | 允许开通线上支付业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.online_fee_conf_list[].fee_min_amt` | 手续费最小值（元） | `String` | `6` | `N` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.online_fee_conf_list[].fee_formula_type` | 代扣手续费计费模式 | `String` | `2` | `N` | bus_type为6：代扣支付时，才可传入；01: 百分比手续费，无封顶值或保底值；02: 百分比手续费，有保底值；03: 固定手续费；04: 固定手续费+百分比手续费；为空默认04 示例值：04 |
| `request.data.balance_pay_config` | 余额支付配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `request.data.balance_pay_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.balance_pay_config.fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.balance_pay_config.open_flag` | 允许开通余额支付业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.combine_pay_config` | 补贴支付配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `request.data.combine_pay_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.combine_pay_config.fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.combine_pay_config.open_flag` | 允许开通补贴支付业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.bank_big_amt_pay_config` | 银行大额转账配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `request.data.bank_big_amt_pay_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.bank_big_amt_pay_config.fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.bank_big_amt_pay_config.open_flag` | 允许开通大额转账业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.out_order_funds_config` | 全域资金管理配置对象（华通银行） | `String` | `—` | `N` | jsonObject格式 |
| `request.data.out_order_funds_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.out_order_funds_config.open_fee_fix_amt` | 开户手续费（元） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.out_order_funds_config.fee_fix_amt` | 保底手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.out_order_funds_config.open_flag` | 允许开通全域资金业务（华通） | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.out_order_funds_new_net_config` | 全域资金管理配置(新网银行) | `String` | `—` | `N` | jsonObject格式 |
| `request.data.out_order_funds_new_net_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.out_order_funds_new_net_config.fee_min_amt` | 保底手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.out_order_funds_new_net_config.public_fee_fix_amt` | 对公固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.out_order_funds_new_net_config.private_fee_fix_amt` | 对私固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.out_order_funds_new_net_config.open_flag` | 允许开通全域资金业务(新网) | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.settle_config_list[]` | 结算配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.settle_config_list[].bus_type` | 业务类型 | `String` | `2` | `Y` | D1：下个自然日到账，；T1：下个工作日到账；TS：笔笔到账；示例值：T1 |
| `request.data.settle_config_list[].fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.settle_config_list[].fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.settle_config_list[].open_flag` | 允许开通结算配置 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.cash_config_list[]` | 取现配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.cash_config_list[].bus_type` | 业务类型 | `String` | `2` | `Y` | D0：当日到账；当日交易资金当天可取现到账；T1：下个工作日到账;；D1：下个自然日到账;；DM：当日到账；到账资金不包括当天的交易资金；示例值：T1 |
| `request.data.cash_config_list[].fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.cash_config_list[].fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.cash_config_list[].open_flag` | 允许开通取现配置 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.out_fee_config` | 外扣配置对象 | `String` | `—` | `N` | jsonObject格式 内容参考：out_fee_config |
| `request.data.out_fee_config.settle_out_fee_flag` | 支持结算手续费外扣 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.out_fee_config.trans_fee_out_flag` | 支持交易手续费外扣 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.out_fee_config.cash_out_fee_flag` | 支持取现手续费外扣 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.alipay_pre_auth_flag` | 允许开通支付宝预授权 | `String` | `1` | `N` | 支付宝预授权开通；Y：是，N：否 |
| `request.data.wechatpay_pre_auth_flag` | 允许开通微信预授权 | `String` | `1` | `N` | 微信预授权开通；Y：是，N：否 |
| `request.data.mer_timing_settle_flag` | 允许开通商户定时结算 | `String` | `1` | `N` | 定时结算开通；Y：是，N：否 |
| `request.data.mer_prior_settle_flag` | 允许开通商户优先结算 | `String` | `1` | `N` | 优先结算开通；Y：是，N：否 |
| `request.data.use_upper_mer_auth_flag` | 允许使用上级商户经营信息 | `String` | `1` | `N` | 开通下级商户时支持复用上级的经营信息；Y：是，N：否 |
| `request.data.use_upper_mer_at_trans_flag` | 允许使用上级商户号发起AT交易 | `String` | `1` | `N` | 开通下级商户时支持复用上级的微信、支付宝商户号信息；Y：是，N：否 |
| `request.data.large_amt_pay_config_list` | 大额支付配置 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.large_amt_pay_config_list.fee_rate` | 手续费（%） | `String` | `6` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.large_amt_pay_config_list.fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00 ，最低传入0.00 |
| `request.data.large_amt_pay_config_list.open_flag` | 允许开通大额转账业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.large_amt_pay_config_list.allow_user_deposit_flag` | 允许用户入账 | `String` | `1` | `N` | Y：是，N：否，示例值：Y ，默认为N |
| `request.data.large_amt_pay_config_list.mer_same_card_recharge_flag` | 银行卡绑定支付权限 | `String` | `1` | `N` | Y：是，N：否，示例值：Y ，默认为N |
| `request.data.large_amt_pay_config_list.business_model` | 大额支付业务模式 | `String` | `15` | `Y` | 大额支付业务模式 bank：银行模式 provisions：备付金模式，示例值：provisions |
| `request.data.large_amt_pay_config_list.provisions_auto_refund_flag` | 备付金固定账号模式自动退款 | `String` | `1` | `N` | Y-开通/N-关闭，默认为N ；示例值：Y；该配置仅在开通大额支付备付金绑卡模式时生效 |
| `request.data.out_order_funds_su_shang_config` | 全域资金管理配置(苏商) | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.out_order_funds_su_shang_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.out_order_funds_su_shang_config.fee_min_amt` | 保底手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.out_order_funds_su_shang_config.public_fee_fix_amt` | 对公固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.out_order_funds_su_shang_config.private_fee_fix_amt` | 对私固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `request.data.out_order_funds_su_shang_config.open_flag` | 允许开通全域资金业务(苏商) | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `request.data.half_pay_host_flag` | 统一收银台开关 | `String` | `1` | `N` | Y:是 N:否（为空默认未开通） ；示例值：Y |
| `request.data.out_order_funds_fee_list[]` | 全域资金费用配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.out_order_funds_fee_list[].bus_type` | 业务类型 | `String` | `2` | `Y` | 01：付款手续费，；02：取现手续费；示例值：01 |
| `request.data.out_order_funds_fee_list[].fee_rate` | 手续费（百分比/%） | `String` | `6` | `Y` | 手续费（百分比/%），保留小数点后两位；取值范围[0.00,100.00] ；示例值：0.05 |
| `request.data.out_order_funds_fee_list[].fee_fix_amt` | 手续费（固定/元） | `String` | `9` | `Y` | 手续费（固定/元），保留小数点后两位；示例值：1.00 |
| `request.data.out_order_funds_fee_list[].open_flag` | 是否允许开通 | `String` | `1` | `Y` | Y：是，N：否；示例值：Y |
| `request.data.lla_withhold_config[]` | 本地生活生活配置对象 | `Object` | `—` | `N` | jsonArray格式 |
| `request.data.lla_withhold_config[].llaWithholdFlag` | 本地生活开关 | `String` | `1` | `Y` | Y:是 N:否（为空默认未开通） ；示例值：Y |
| `request.data.lla_withhold_config[].fee_rate` | 佣金收取手续费率 | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.bill_payment_flag` | 是否开通账单支付 | `String` | `1` | `N` | Y:是 N:否 ；示例值：Y |
| `request.data.dy_conf_list[]` | 抖音配置对象 | `String` | `—` | `N` | jsonArray字符串 |
| `request.data.dy_conf_list[].mer_industry_category` | 抖音商户行业分类 | `String` | `1` | `Y` | 目前仅支持C，适用于7999-其他娱乐服务、5541-加油加气充电站、5811-包办伙食，宴会承包商、 5812-就餐场所和餐馆、 5813-休闲饮品场所、酒吧、咖啡厅、茶馆 |
| `request.data.dy_conf_list[].fee_model` | 手续费模式 | `String` | `2` | `Y` | 01-百分比 02-百分比+最低手续费 |
| `request.data.dy_conf_list[].fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `request.data.dy_conf_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `9` | `N` | 固定金额保留2位小数；大于0。需要渠道商开通此功能。示例值：0.38 |
| `request.data.dy_conf_list[].open_flag` | 是否允许开通 | `String` | `1` | `N` | Y：是，N：否；示例值：Y |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务返回码 | `String` | `8` | `N` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务返回描述 | `String` | `512` | `N` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.product_id` | 产品号 | `String` | `32` | `N` | 汇付分配的产品号，示例值：MCS |
| `response.data.req_date` | 请求时间 | `String` | `32` | `Y` | 请求时间 |
| `response.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号 |
| `response.data.huifu_id` | 商户汇付Id | `String` | `18` | `Y` | 商户汇付Id；示例值：[官网示例已脱敏] |
| `response.data.apply_no` | 申请单 | `String` | `128` | `Y` | 申请单 |

## 商户统一进件（页面版）

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shtyjjweb.md>
- SHA-256：`d3ce5d64bf4c9783b40e0700a93476016b469478ba9b3d2c9adf82f55d1e5888`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 异步通知信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.resp_code` | 网关返回码 | `String` | `6` | `Y` | [网关返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#%E7%BD%91%E5%85%B3%E8%BF%94%E5%9B%9E%E7%A0%81) |
| `async.resp_desc` | 网关返回描述 | `String` | `512` | `Y` | 网关返回描述 |
| `async.sign` | 签名 | `String` | `512` | `Y` | 签名，对报文整体签名 |
| `async.data` | 业务返回参数 | `String` | `—` | `N` | JSON |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号；示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 请求时间 yyyyMMdd；示例值：20220915 |
| `request.data.upper_huifu_id` | 渠道商号 | `String` | `18` | `C` | 汇付分配的渠道商号，该商户进件完成后将隶属该渠道商/代理商；sys_id主体为渠道商时填写；sys_id主体为总部商户时选填；示例值：[官网示例已脱敏] |
| `request.data.phone` | 手机号 | `String` | `11` | `N` | 手机号；示例值：[官网示例已脱敏] |
| `request.data.store_id` | 门店号 | `String` | `64` | `Y` | 门店号，示例值：SH001 |
| `request.data.expires` | 跳转地址失效时间 | `String` | `5` | `N` | 单位秒；示例值：50000 |
| `request.data.back_page_url` | 返回页面URL | `String` | `256` | `N` | 进件完成后回跳指定页面。http或https开头；示例值：http://service.huifu.com/xxx?grantsId=xx&encryptMsg=xxxx |
| `request.data.async_receive_url` | 异步接收URL | `String` | `256` | `N` | 消息接收地址，示例值：http://service.example.com/to/path |
| `request.data.template_id` | 模版编号 | `String` | `20` | `N` | 服务商控制台，商户入驻费率模版列表中模版编号；示例值：155677 |
| `request.data.head_office_flag` | 商户身份 | `String` | `1` | `N` | 1：总部商户， 0：下级商户； 不传默认普通商户。示例值：0 开通下级商户时，所选的上级商户需要有开通商户权限，需先调用[“开通下级商户权限配置接口”](https://paas.huifu.com/open/doc/api/#/shgl/shywkt/api_shjj_shywkt_xjshpz) |
| `request.data.head_huifu_id` | 上级汇付Id | `String` | `18` | `C` | 如果head_office_flag=0，则字段必填，如果head_office_flag=1，上级汇付Id不可传 |
| `request.data.use_chains_flag` | 使用上级微信、支付宝商户号发起交易 | `String` | `8` | `N` | 1 微信+支付宝 2 不使用 3 微信 4 支付宝； 使用上级微信、支付宝商户号需对应开通微信、支付宝功能；示例值：2 |
| `request.data.micro_biz_type` | 小微经营类型 | `String` | `32` | `N` | MICRO_TYPE_STORE-门店场所,MICRO_TYPE_MOBILE-流动经营/便民服务,MICRO_TYPE_ONLINE-线上商品/服务交易;不传默认为MICRO_TYPE_MOBILE示例值：MICRO_TYPE_STORE |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务响应码 | `String` | `8` | `Y` | 业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务响应信息 | `String` | `512` | `Y` | 业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.req_seq_id` | 请求流水号 | `String` | `32` | `N` | 原请求流水号；示例值：[官网示例已脱敏] |
| `response.data.req_date` | 请求时间 | `String` | `8` | `N` | 原请求时间yyyyMMdd；示例值：20220912 |
| `response.data.product_id` | 产品号 | `String` | `32` | `N` | 汇付分配的产品号，示例值：MCS |
| `response.data.url` | 跳转地址 | `String` | `32` | `Y` | 商户进件页面跳转地址；http或https开头； 示例值：http://service.huifu.com/xxx?grantsId=xx&encryptMsg=xxxx |

### 审核异步 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.audit.data.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#%E5%95%86%E6%88%B7%E8%BF%9B%E4%BB%B6%E8%BF%94%E5%9B%9E%E7%A0%81) |
| `async.audit.data.sub_resp_desc` | 业务返回描述 | `String` | `512` | `Y` | 业务返回描述 |
| `async.audit.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `async.audit.data.req_date` | 请求日期 | `String` | `32` | `Y` | 请求时间yyyyMMdd；示例值：20220912 |
| `async.audit.data.product_id` | 产品编号 | `String` | `32` | `Y` | 示例值：YYZY |
| `async.audit.data.huifu_id` | 商户汇付Id | `String` | `18` | `Y` | 参见同步返回的huifu_id；示例值：[官网示例已脱敏] |
| `async.audit.data.apply_no` | 申请单 | `String` | `18` | `Y` | 与同步返回的申请单号相同；示例值：202209120038432 |
| `async.audit.data.audit_status` | 审核状态 | `String` | `1` | `Y` | Y：审核通过 N：审核拒绝；示例值：Y |
| `async.audit.data.audit_desc` | 审核状态描述 | `String` | `256` | `N` | 示例值： |
| `async.audit.data.token_no` | 取现卡序列号 | `String` | `20` | `N` | 填写了卡配置信息，审核通过后有值，交易时用到；示例值：[官网敏感示例已脱敏] |
| `async.audit.data.store_id` | 门店号 | `String` | `64` | `Y` | 商户门店号；示例值：SH001 |

### 业务异步 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.business.data.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#%E5%95%86%E6%88%B7%E8%BF%9B%E4%BB%B6%E8%BF%94%E5%9B%9E%E7%A0%81) |
| `async.business.data.sub_resp_desc` | 业务返回描述 | `String` | `512` | `Y` | 业务返回描述 |
| `async.business.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原请求流水号；示例值：[官网示例已脱敏] |
| `async.business.data.req_date` | 请求日期 | `String` | `8` | `Y` | 原请求时间yyyyMMdd；示例值：20220912 |
| `async.business.data.product_id` | 产品编号 | `String` | `32` | `Y` | 固定值产品编号；示例值：YYZY |
| `async.business.data.huifu_id` | 汇付客户号 | `String` | `18` | `Y` | 参见同步返回的huifu_id；示例值：[官网示例已脱敏] |
| `async.business.data.apply_no` | 申请单号 | `String` | `18` | `N` | 汇付返回商户开户业务申请单号；示例值：202209120038432 |
| `async.business.data.store_id` | 门店号 | `String` | `64` | `Y` | 商户门店号；示例值：SH001 |
| `async.business.data.notify_type` | 通知类型 | `String` | `1` | `Y` | W:微信 A：支付宝 U:银联二维码 B:刷卡；示例值：W |
| `async.business.data.ord_id` | 通知流水号 | `String` | `44` | `N` | 回调方返回应答，应答内容为：”RECV_ORD_ID_”+该ordId |
| `async.business.data.reg_result_list[]` | 入驻结果集合 | `Object` | `—` | `N` | jsonArray格式；notify_type等于U或者B时，此集合最多只有一条数据; notify_type等于A或者W时，此集合可能有多条数据 |
| `async.business.data.reg_result_list[].pay_scene` | 费率类型 | `String` | `2` | `N` | 请求参数pay_scene；参见《[微信支付场景](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e6%94%af%e4%bb%98%e5%9c%ba%e6%99%af)》说明；示例值：1 |
| `async.business.data.reg_result_list[].business_stat` | 业务开通状态 | `String` | `1` | `Y` | S-成功，F-失败；示例值：S |
| `async.business.data.reg_result_list[].business_desc` | 业务开通描述 | `String` | `200` | `N` | 业务开通描述 |
| `async.business.data.reg_result_list[].sub_mer_id` | 二级商户号 | `String` | `32` | `N` | 银联商户号或者微信/支付宝二级商户号；示例值：A[官网示例已脱敏] |
| `async.business.data.reg_result_list[].sub_mer_name` | 二级商户名称 | `String` | `50` | `N` | 示例值：上海汇付支付有限公司 |
| `async.business.data.reg_result_list[].pay_channel_id` | 渠道号 | `String` | `50` | `N` | 示例值：JP00001 |
| `async.business.data.reg_result_list[].bank_mer_code` | 真实商户号 | `String` | `20` | `N` | 示例值：[官网示例已脱敏] |
| `async.business.data.reg_result_list[].wx_real_name_flag` | 实名入驻标识 | `String` | `1` | `N` | Y-微信/支付宝实名认证，N-非微信/支付宝 实名认证；用于区分微信/支付宝配置和微信/支付宝实名；当notify_type是W/A时返回；示例值：Y |

## 统一进件页面版查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shtyjjwebcx.md>
- SHA-256：`252db113d3eab2a6de3b1fb27291bc7346f9c2c3a53bcc54657c44cc875357c8`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号；示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 请求时间 yyyyMMdd；示例值：20220915 |
| `request.data.store_id` | 门店号 | `String` | `64` | `Y` | 门店号，示例值：SH001 |
| `request.data.upper_huifu_id` | 渠道商号 | `String` | `18` | `N` | sys_id为商户时，需传入，传入的值为商户统一进件时传入的upper_huifu_id 示例值：[官网示例已脱敏] |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务响应码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务响应信息 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.channel_huifu_id` | 渠道商汇付id | `String` | `18` | `Y` | 示例值：[官网示例已脱敏] |
| `response.data.store_id` | 门店号 | `String` | `64` | `Y` | 示例值：SH001 |
| `response.data.huifu_id` | 汇付号 | `String` | `18` | `Y` | 示例值：[官网示例已脱敏] |
| `response.data.check_status` | 审核状态 | `String` | `1` | `N` | Y：审核成功，N:审核拒绝，P:审核中示例值：Y |
| `response.data.head_office_flag` | 商户身份 | `String` | `1` | `N` | 1：总部商户， 0：下级商户； 为空则为普通商户 示例值：1 |
| `response.data.head_huifu_id` | 上级汇付Id | `String` | `18` | `N` | head_office_flag为0时返回； 示例值：[官网示例已脱敏] |
| `response.data.use_chains_flag` | 使用上级微信、支付宝商户号发起交易 | `String` | `8` | `N` | 1 微信+支付宝 2 不使用 3 微信 4 支付宝； 示例值：1 |
| `response.data.wx_pay_config_info[]` | 微信支付实体 | `String` | `—` | `N` | jsonArray格式字符串 |
| `response.data.wx_pay_config_info[].wx_pay_be_swept_down` | 微信被扫支付线下 | `String` | `1` | `Y` | Y：已开通，N:未开通；示例值：Y |
| `response.data.wx_pay_config_info[].wx_pay_be_swept_down_rate` | 微信被扫支付线下费率(%) | `String` | `8` | `N` | 示例值：0.6 |
| `response.data.wx_pay_config_info[].wx_public_account_down` | 微信公众号支付线下 | `String` | `1` | `Y` | Y：已开通，N:未开通；示例值：Y |
| `response.data.wx_pay_config_info[].wx_public_account_down_rate` | 微信公众号支付线下费率(%) | `String` | `8` | `N` | 示例值：0.6 |
| `response.data.wx_pay_config_info[].wx_public_account_up` | 微信公众号支付线上 | `String` | `1` | `Y` | Y：已开通，N:未开通；示例值：Y |
| `response.data.wx_pay_config_info[].wx_public_account_up_rate` | 微信公众号支付线上费率(%) | `String` | `8` | `N` | 示例值：0.6 |
| `response.data.wx_pay_config_info[].wx_small_program_down` | 微信小程序线下 | `String` | `1` | `Y` | Y：已开通，N:未开通；示例值：Y |
| `response.data.wx_pay_config_info[].wx_small_program_down_rate` | 微信小程序线下费率(%) | `String` | `8` | `N` | 示例值：0.6 |
| `response.data.wx_pay_config_info[].wx_small_program_up` | 微信小程序线上 | `String` | `1` | `Y` | Y：已开通，N:未开通；示例值：Y |
| `response.data.wx_pay_config_info[].wx_small_program_up_rate` | 微信小程序线上费率(%) | `String` | `8` | `N` | 示例值：0.6 |
| `response.data.wx_real_name_list[]` | 微信实名实体 | `String` | `—` | `N` | jsonArray格式字符串 |
| `response.data.wx_real_name_list[].pay_scene` | 场景 | `String` | `2` | `Y` | 参见《[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e6%94%af%e4%bb%98%e5%9c%ba%e6%99%af)》 |
| `response.data.wx_real_name_list[].authorize_stat` | 授权状态 | `String` | `8` | `Y` | 1：授权成功；0：授权失败；示例值：1 |
| `response.data.ali_pay_config_info[]` | 支付宝支付实体 | `String` | `—` | `N` | jsonArray格式字符串 |
| `response.data.ali_pay_config_info[].ali_pay_be_swept_down` | 支付宝被扫支付线下 | `String` | `1` | `Y` | Y：已开通，N:未开通；示例值：Y |
| `response.data.ali_pay_config_info[].ali_pay_be_swept_down_rate` | 支付宝被扫支付线下费率(%) | `String` | `8` | `N` | 示例值：0.6 |
| `response.data.ali_pay_config_info[].ali_master_sweep_down` | 支付宝主扫支付线下 | `String` | `1` | `Y` | Y：已开通，N:未开通；示例值：Y |
| `response.data.ali_pay_config_info[].ali_master_sweep_down_rate` | 支付宝主扫支付线下费率(%) | `String` | `8` | `N` | 示例值：0.6 |
| `response.data.ali_pay_config_info[].ali_small_program_down` | 支付宝小程序支付线下 | `String` | `1` | `Y` | Y：已开通，N:未开通；示例值：Y |
| `response.data.ali_pay_config_info[].ali_small_program_down_rate` | 支付宝小程序支付线下费率(%) | `String` | `8` | `N` | 示例值：0.6 |
| `response.data.ali_pay_config_info[].ali_small_program_up` | 支付宝小程序线上 | `String` | `1` | `Y` | Y：已开通，N:未开通；示例值：Y |
| `response.data.ali_pay_config_info[].ali_small_program_up_rate` | 支付宝小程序线上费率(%) | `String` | `8` | `N` | 示例值：0.6 |
| `response.data.ali_real_name_list[]` | 支付宝实名实体 | `String` | `—` | `N` | jsonArray格式字符串 |
| `response.data.ali_real_name_list[].pay_scene` | 场景 | `String` | `1` | `Y` | 1-线下扫码；示例值：1 |
| `response.data.ali_real_name_list[].authorize_stat` | 授权状态 | `String` | `8` | `Y` | 1：授权成功；0：授权失败；示例值：1 |
| `response.data.agreement_info_list[]` | 协议信息 | `String` | `—` | `N` | jsonArray格式字符串 |
| `response.data.agreement_info_list[].agreement_type` | 协议类型 | `String` | `1` | `N` | 0-电子协议 |
| `response.data.agreement_info_list[].agreement_link` | 协议签署链接 | `String` | `512` | `N` | — |
| `response.data.agreement_info_list[].agreement_no` | 协议号 | `String` | `32` | `N` | 示例值：3245234 |
| `response.data.agreement_info_list[].agreement_name` | 协议名称 | `String` | `128` | `N` | — |
| `response.data.agreement_info_list[].con_stat` | 合同状态 | `String` | `2` | `N` | 电子协议类型会返回以下值： 2：创建合同异常 3：待签约 4：签约中 5：签约完成(电子协议只有签约完成才能做交易) 6：已失效 7：已拒签 8：签约失败 示例值：5 |

## 微信商户配置

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxshpz.md>
- SHA-256：`bc0b92c4e46e7a097248cf3e048fcd9f13159b41ccd26194b2825babc132426a`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | 签名，对报文整体签名；[接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `String` | `—` | `Y` | JSON格式 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 格式yyyyMMdd，示例值：20210228 |
| `request.data.huifu_id` | 汇付商户号 | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID |
| `request.data.fee_type` | 业务开通类型 | `String` | `2` | `Y` | 示例值：01；枚举值参见《[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e4%b8%9a%e5%8a%a1%e5%bc%80%e9%80%9a%e7%b1%bb%e5%9e%8b)》说明 |
| `request.data.wx_woa_app_id` | 公众号支付Appid | `String` | `20` | `C` | 条件必填，示例值：wx3767c5bd01df5061 ；wx_woa_app_id 、wx_woa_path、micro_sub_appid和 wx_applet_app_id四者不能同时为空 |
| `request.data.wx_woa_path` | 微信公众号授权目录 | `String` | `512` | `C` | 条件必填，示例值：https://paas.huifu.com/shouyintai/demo/h5/；wx_woa_app_id 、wx_woa_path、micro_sub_appid和 wx_applet_app_id四者不能同时为空 |
| `request.data.wx_woa_secret` | 微信公众号APPID对应的秘钥 | `String` | `64` | `N` | 示例值：[官网敏感示例已脱敏] |
| `request.data.wx_applet_app_id` | 微信小程序APPID | `String` | `20` | `C` | 条件必填，示例值：wx8523175fea790f10 ；wx_woa_app_id 、wx_woa_path、micro_sub_appid和 wx_applet_app_id四者不能同时为空 |
| `request.data.micro_sub_appid` | 微信反扫类交易APPID | `String` | `32` | `N` | 如需在汇付反扫交易支付完成后获取sub_openid则此参数必传，示例值：wx23175fea790f10 ；wx_woa_app_id 、wx_woa_path、micro_sub_appid和 wx_applet_app_id四者不能同时为空 |
| `request.data.wx_applet_secret` | 微信小程序APPID对应的秘钥 | `String` | `64` | `N` | 示例值：[官网敏感示例已脱敏] |
| `request.data.bank_channel_no` | 渠道号 | `String` | `32` | `N` | 示例值：JQF00001；有值时设置指定值，为空时使用的微信入驻记录；参见[支付渠道号说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo) |
| `request.data.async_return_url` | 异步消息接收地址 | `String` | `120` | `N` | 为空不推送审核消息。示例值：http://service.example.com/to/path |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务返回码 | `String` | `—` | `N` | 参考[业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码)；示例值：00000000 |
| `response.data.resp_desc` | 业务返回描述 | `String` | `—` | `N` | 示例值：处理成功 |
| `response.data.huifu_id` | 汇付商户号 | `String` | `—` | `N` | 汇付商户号，状态为审核中时返回；示例值：[官网示例已脱敏] |
| `response.data.apply_no` | 申请单号 | `String` | `—` | `N` | 商户开户业务申请单号，状态为审核中时返回；示例值：[官网示例已脱敏] |

### 异步通知 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.data.sub_resp_code` | 业务返回码 | `String` | `8` | `N` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `async.data.sub_resp_desc` | 业务返回描述 | `String` | `512` | `N` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `async.data.req_seq_id` | 请求流水号 | `String` | `32` | `N` | 原请求流水号；示例值：rQ2021121311651 |
| `async.data.req_date` | 请求日期 | `String` | `8` | `N` | 原请求时间yyyyMMdd；示例值：20221121 |
| `async.data.product_id` | 产品编号 | `String` | `32` | `N` | 汇付产品编号；示例值：YYZY |
| `async.data.huifu_id` | 汇付商户号 | `String` | `18` | `N` | 示例值：[官网示例已脱敏] |
| `async.data.apply_no` | 申请单号 | `String` | `18` | `N` | 汇付返回商户开户业务申请单号；示例值：[官网示例已脱敏] |
| `async.data.ord_id` | 通知流水号 | `String` | `44` | `N` | 回调方返回应答，应答内容为：”RECV_ORD_ID_”+该ordId；示例值：RECV_ORD_ID_[官网示例已脱敏] |
| `async.data.result_list[]` | 微信配置结果集合 | `String` | `—` | `N` | jsonArray格式 参考：result_list; |
| `async.data.result_list[].config_type` | 配置类型 | `String` | `2` | `N` | 01 -公众号配置 02-小程序配置；示例值：01 |
| `async.data.result_list[].config_stat` | 配置值 | `String` | `2` | `N` | S-成功,F-失败，B-部分成功；示例值：S |

## 微信商户配置查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxshpzcx.md>
- SHA-256：`99937c6b7807a691d017830e8553521b1e13691f66a02473dcf6ce3e6bc0924e`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商或商户的huifu_id；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为总部商户时，此字段填写商户huifu_id |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | 签名，对报文整体签名 |
| `response.data` | 交易响应内容体 | `String` | `—` | `N` | 返回参数 json格式 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 示例值：rQ[官网示例已脱敏] |
| `request.data.req_date` | 请求时间 | `String` | `8` | `Y` | 格式yyyyMMdd，示例值：20210228 |
| `request.data.huifu_id` | 汇付客户Id | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] |
| `request.data.bank_channel_no` | 渠道号 | `String` | `32` | `N` | 示例值：JQF00001；参见[支付渠道号说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo) |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 返回描述 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.atu_config_bo_list[]` | 配置信息 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.atu_config_bo_list[].fee_type` | 业务开通类型 | `String` | `2` | `N` | 示例值：01；参见《[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e4%b8%9a%e5%8a%a1%e5%bc%80%e9%80%9a%e7%b1%bb%e5%9e%8b)》说明 |
| `response.data.atu_config_bo_list[].wx_applet_app_id` | 微信小程序APPID | `String` | `20` | `N` | 示例值：wx8523175fea790f10 |
| `response.data.atu_config_bo_list[].wx_woa_app_id` | 公众号支付APPID | `String` | `512` | `N` | 示例值：wx3767c5bd01df5061 |
| `response.data.atu_config_bo_list[].wx_woa_path` | 微信公众号授权目录 | `String` | `512` | `N` | 示例值：https://paas.huifu.com/shouyintai/demo/h5/ |
| `response.data.atu_config_bo_list[].micro_sub_appid` | 微信反扫类交易APPID | `String` | `N` | `32` | 示例值：wx23175fea790f10 |
| `response.data.atu_config_bo_list[].bank_channel_no` | 渠道号 | `String` | `32` | `N` | 示例值：JQF00001 |
| `response.data.atu_config_bo_list[].wx_config_list[]` | 微信配置结果集 | `String` | `—` | `N` | jsonArray格式 参考：wx_config_list 微信配置结果集 |
| `response.data.atu_config_bo_list[].wx_config_list[].config_type` | 配置类型 | `String` | `1` | `Y` | 1-小程序appId， 2-公众号appId， 3-授权目录， 4-关注的公众号，5-微信反扫类交易appId；示例值：1 |
| `response.data.atu_config_bo_list[].wx_config_list[].config_value` | 配置值 | `String` | `256` | `Y` | 对应配置类型参数值 |
| `response.data.atu_config_bo_list[].wx_config_list[].control_flag` | 管控标识 | `String` | `1` | `N` | Y-管控中,N-已解控，为空时无管控 |
| `response.data.atu_config_bo_list[].wx_config_list[].control_time` | 管控/解控时间 | `String` | `20` | `N` | 管控/解控时间：yyyy-MM-dd HH:mm:ss格式，当controlFlag为Y时为管控时间，当controlFlag为N时为解控时间 |
| `response.data.atu_config_bo_fail_list[]` | 配置失败信息 | `String` | `—` | `N` | jsonArray格式；配置失败信息仅返回最新一条 |
| `response.data.atu_config_bo_fail_list[].fee_type` | 业务开通类型 | `String` | `2` | `N` | 参见《[微信业务开通类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e4%b8%9a%e5%8a%a1%e5%bc%80%e9%80%9a%e7%b1%bb%e5%9e%8b)》说明 |
| `response.data.atu_config_bo_fail_list[].wx_applet_app_id` | 微信小程序APPID | `String` | `20` | `N` | 示例值：wx8523175fea790f10 |
| `response.data.atu_config_bo_fail_list[].wx_woa_app_id` | 公众号支付APPID | `String` | `512` | `N` | 示例值：wx3767c5bd01df5061 |
| `response.data.atu_config_bo_fail_list[].wx_woa_path` | 微信公众号授权目录 | `String` | `512` | `N` | 示例值：https://paas.huifu.com/shouyintai/demo/h5/ |
| `response.data.atu_config_bo_fail_list[].bank_channel_no` | 渠道号 | `String` | `32` | `N` | 示例值：JQF00001 |
| `response.data.atu_config_bo_fail_list[].business_desc` | 业务失败描述信息 | `String` | `512` | `N` | 业务失败描述信息 |
| `response.data.atu_config_bo_fail_list[].bank_message` | 微信/支付宝侧失败描述信息 | `String` | `512` | `N` | 微信/支付宝侧失败描述信息 |

## 微信实名认证

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxsmrz.md>
- SHA-256：`41d4520a560c4cafb61cf8b87f7d15bf316c949e2b126a131833e343c8fa3197`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | 签名，对报文整体签名 |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `request.data` | 数据 | `String` | `—` | `Y` | jsonObject格式 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 示例值：rQ[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 必填，请求日期yyyyMMdd，示例值：20220809 |
| `request.data.huifu_id` | 汇付ID | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏]；**请确认该商户已成功入驻微信** |
| `request.data.pay_channel_id` | 子渠道号 | `String` | `32` | `N` | 如需要填写汇付和渠道商约定的值，参见[支付渠道号说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo)；示例值：JQF00001 |
| `request.data.pay_scene` | 支付场景 | `String` | `2` | `N` | 示例值：01；参见《[微信业务开通类型](http://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e4%b8%9a%e5%8a%a1%e5%bc%80%e9%80%9a%e7%b1%bb%e5%9e%8b)》说明 |
| `request.data.owner` | 经营者/法人是否为受益人 | `String` | `1` | `N` | 企业开通微信支付时需要填写；Y：是最终受益人；N：非最终受益人(默认)；示例值：Y |
| `request.data.identification_address` | 法人证件居住地址 | `String` | `256` | `N` | 1、主体类型为企业时，需要填写。其他主体类型，无需上传。；2、请按照证件上住址填写，若证件上无住址则按照实际住址填写，示例值：广东省深圳市南山区xx路xx号xx室。 |
| `request.data.ubo_info_list[]` | 受益人信息 | `String` | `—` | `N` | jsonArray格式；受益人仅企业需要填写。；若经营者/法人不是最终受益所有人，则需提填写受益所有人信息，最多上传4个。 若经营者/法人是最终受益所有人之一，可在此填写其他受益所有人信息，最多上传3个。 |
| `request.data.ubo_info_list[].ubo_id_doc_type` | 受益人证件类型 | `String` | `10` | `Y` | 企业开通微信业务必填；枚举值00：身份证， 01：护照，11：港澳同胞回乡证，12：外国人居留证，13：港澳居民证，14：台湾居民证；个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关仅支持身份证类型。；示例值：00 |
| `request.data.ubo_info_list[].ubo_id_doc_copy` | 证件正面照片 | `String` | `64` | `Y` | 1、请上传受益人证件的正面照片；企业开通微信业务必填；2、若证件类型为身份证，请上传人像面照片;；3、请上传彩色照片or彩色扫描件or复印件;；4、开通微信业务时需加盖公章鲜章，可添加“微信支付”相关水印（如微信支付认证）；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.ubo_info_list[].ubo_id_doc_copy_back` | 证件反面照片 | `String` | `64` | `N` | 1、请上传受益人证件的反面照片；企业开通微信业务必填；2、若证件类型为护照，无需上传反面照片;；3、请上传彩色照片or彩色扫描件or复印件;；4、开通微信业务时需加盖公章鲜章，可添加“微信支付”相关水印（如微信支付认证）；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.ubo_info_list[].ubo_id_doc_name` | 受益人证件姓名 | `String` | `128` | `Y` | 示例值：张三 |
| `request.data.ubo_info_list[].ubo_id_doc_number` | 受益人证件号码 | `String` | `128` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.ubo_info_list[].ubo_id_doc_address` | 证件居住地址 | `String` | `256` | `Y` | 请按照证件上住址填写，若证件上无住址则按照实际住址填写；示例值：广东省深圳市南山区xx路xx号xx室 。 |
| `request.data.ubo_info_list[].ubo_period_begin` | 证件有效期开始时间 | `String` | `20` | `Y` | 格式：yyyyMMdd； 示例值：20190606 |
| `request.data.ubo_info_list[].ubo_period_end` | 证件有效期结束时间 | `String` | `20` | `Y` | 1、格式：yyyyMMdd； 示例值：20290606；若证件有效期为长期，请填写：长期；2、结束时间大于开始时间 |
| `request.data.name` | 联系人姓名 | `String` | `64` | `Y` | 示例值：[官网敏感示例已脱敏] |
| `request.data.mobile` | 联系人手机号 | `String` | `11` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.id_card_number` | 联系人身份证号码 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.contact_type` | 联系人类型 | `String` | `10` | `Y` | LEGAL：经营者/法人；SUPER：经办人（经商户授权办理微信支付业务的人员）； 1、主体为“小微/个人卖家”，可选择：LEGAL：；2、主体为“个体工商户/企业/政府机关/事业单位/社会组织”，可选择：LEGAL、SUPER；示例值：LEGAL |
| `request.data.contact_id_doc_type` | 联系人证件类型 | `String` | `10` | `N` | 当联系人类型是经办人时，请上传联系人证件类型；枚举值参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明，示例值：00；个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关仅支持身份证类型。；另外还需上传证件件，见【special_file_info_list】字段说明 |
| `request.data.contact_period_begin` | 联系人证件有效期开始时间 | `String` | `20` | `N` | 1、当联系人类型是经办人时，请填写证件有效期开始时间;；2、格式：yyyy-MM-dd； 示例值：2019-06-06 |
| `request.data.contact_period_end` | 联系人证件有效期结束时间 | `String` | `20` | `N` | 1、当联系人类型是经办人时，请填写证件有效期结束时间;；2、格式：yyyy-MM-dd； 示例值：2029-06-06 ；3、结束时间大于开始时间;若证件有效期为长期，请填写：长期 |
| `request.data.cert_type` | 证书类型 | `String` | `64` | `N` | CERTIFICATE_TYPE_2388：事业单位法人证书 ；仅支持事业单位；CERTIFICATE_TYPE_2389：统一社会信用代码证书 ；政府机关使用此类型；社会组织使用以下类型：；CERTIFICATE_TYPE_2389：统一社会信用代码证书；CERTIFICATE_TYPE_2394：社会团体法人登记证书 ；CERTIFICATE_TYPE_2395：民办非企业单位登记证书 ；CERTIFICATE_TYPE_2396：基金会法人登记证书 ；CERTIFICATE_TYPE_2399：宗教活动场所登记证 ；CERTIFICATE_TYPE_2400：其他证书/批文/证明 ；CERTIFICATE_TYPE_2520：执业许可证/执业证；CERTIFICATE_TYPE_2521：基层群众性自治组织特别法人统一社会信用代码证 ；CERTIFICATE_TYPE_2522：农村集体经济组织登记证；示例值：CERTIFICATE_TYPE_2389 |
| `request.data.cert_number` | 证书编号 | `String` | `32` | `N` | 各类证书编号，如营业执照编号、事业部单位法人证书等；示例值：[官网敏感示例已脱敏] |
| `request.data.cert_copy` | 证书照片 | `String` | `64` | `N` | **事业单位**填写，图片上传接口生成的file_id；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.micro_biz_type` | 小微经营类型 | `String` | `32` | `N` | 门店场所：MICRO_TYPE_STORE ；流动经营/便民服务：MICRO_TYPE_MOBILE ；线上商品/服务交易：MICRO_TYPE_ONLINE；示例值：MICRO_TYPE_STORE |
| `request.data.store_name` | 门店名称 | `String` | `32` | `N` | 32个字符，16个汉字；示例值：肯德基共富新村店 |
| `request.data.store_header_copy` | 门店门头照片 | `String` | `64` | `N` | 小微商户填写，图片上传接口生成的fileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.store_indoor_copy` | 店内环境照片 | `String` | `64` | `N` | 小微商户填写，图片上传接口生成的fileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.store_address_code` | 门店省市编码 | `String` | `16` | `N` | 小微商户填写，请参考[省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：360400 |
| `request.data.store_address` | 门店地址 | `String` | `128` | `N` | 小微商户填写；示例值：上海宝山区共富路512号 |
| `request.data.identification_front_copy` | 身份证件人像面 | `String` | `64` | `N` | 小微商户填写，图片上传接口生成的fileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.identification_back_copy` | 身份证件国徽面 | `String` | `64` | `N` | 小微商户填写，图片上传接口生成的fileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.company_prove_copy` | 单位证明函照片 | `String` | `64` | `N` | 事业单位填写，图片上传接口生成的fileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.finance_institution_flag` | 是否金融机构 | `String` | `1` | `N` | 选填，Y/N；默认N；示例值：N ；请根据申请主体的实际情况填写，可参见[微信金融机构接入指引](https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html) |
| `request.data.finance_type` | 金融机构类型 | `String` | `128` | `N` | 当主体是金融机构时，必填；金融机构类型需与营业执照/登记证书上一致，可参见[微信金融机构接入指引](https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html)。；BANK_AGENT：银行业, 适用于商业银行、政策性银行、农村合作银行、村镇银行、开发性金融机构等；PAYMENT_AGENT：支付机构, 适用于非银行类支付机构；INSURANCE：保险业, 适用于保险、保险中介、保险代理、保险经纪等保险类业务；TRADE_AND_SETTLE：交易及结算类金融机构, 适用于交易所、登记结算类机构、银行卡清算机构、资金清算中心等；OTHER：其他金融机构, 适用于财务公司、信托公司、金融资产管理公司、金融租赁公司、汽车金融公司、贷款公司、货币经纪公司、消费金融公司、证券业、金融控股公司、股票、期货、货币兑换、小额贷款公司、金融资产管理、担保公司、商业保理公司、典当行、融资租赁公司、财经咨询等其他金融业务；示例值：INSURANCE；金融机构需上传许可证图片，见【special_file_info_list】字段说明 |
| `request.data.category_id` | 特殊行业Id | `String` | `3` | `N` | 特殊行业填写，参看微信支付提供的[特殊行业id对照表](https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/applysubject_new/chapter6_1.shtml)；示例值：100 |
| `request.data.special_file_info_list[]` | 文件列表 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.special_file_info_list[].file_type` | 文件类型 | `String` | `8` | `Y` | F28：联系人身份证人像面；（联系人是经办人时需要提供，参见下文说明）；F29：联系人身份证国徽面；（联系人是经办人时需要提供，参见下文说明）；F33：联系人护照人像面；（联系人是经办人时需要提供，参见下文说明）；F241：联系人证件照正面，非身份证与护照类型；（联系人是经办人时需要提供，参见下文说明）；F242：联系人证件照反面，非身份证类型；（联系人是经办人时需要提供，参见下文说明）；F227：微信业务办理授权函；（联系人是经办人时必需提供，参见下文说明）；F236：金融机构许可证图片一；（金融机构需提供）；F237：金融机构许可证图片二；F238：金融机构许可证图片三；F239：金融机构许可证图片四；F240：金融机构许可证图片五；F150:行业经营许可证资质照片一（特殊行业选填） ；F151:行业经营许可证资质照片二 ；F152:行业经营许可证资质照片三 ；F153:行业经营许可证资质照片四 ；F154:行业经营许可证资质照片五 ；F155:行业经营许可证资质照片六；示例值：F28 |
| `request.data.special_file_info_list[].file_id` | 文件jfileID | `String` | `64` | `Y` | 图片上传接口生成的fileId；示例值：[官网敏感示例已脱敏] |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 返回码 | `String` | `8` | `Y` | [交易返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 返回描述 | `String` | `512` | `Y` | [交易返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.huifu_id` | 汇付ID | `String` | `18` | `Y` | 示例值：[官网示例已脱敏] |
| `response.data.applyment_id` | 申请单编号 | `String` | `256` | `N` | 微信支付分配的申请单号，申请成功时返回；示例值：[官网示例已脱敏] |

## 微信实名认证状态查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxsmrzztcx.md>
- SHA-256：`8477b7bada0041c3f7ef6fc33ae2a35d041a3898e6ef2c23f6d1ff2d7be66872`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 示例值：rQ[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 必填，请求日期yyyyMMdd，示例值：20220809 |
| `request.data.huifu_id` | 汇付Id | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏]；**请确认该商户已成功入驻微信** |
| `request.data.pay_channel_id` | 子渠道号 | `String` | `32` | `N` | 如需要填写汇付和渠道商约定的值，参见[支付渠道号说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo)；示例值：JQF00001 |
| `request.data.pay_scene` | 支付场景 | `String` | `2` | `N` | 示例值：01；参见《[微信业务开通类型](http://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e4%b8%9a%e5%8a%a1%e5%bc%80%e9%80%9a%e7%b1%bb%e5%9e%8b)》说明 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务响应码 | `String` | `8` | `Y` | 示例值：00000000；参见[交易返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务响应信息 | `String` | `512` | `Y` | 示例值：成功；参见[交易返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.huifu_id` | 汇付ID | `String` | `18` | `Y` | 示例值：[官网示例已脱敏] |
| `response.data.applyment_stat` | 微信实名认证申请单状态 | `String` | `32` | `N` | [参见下文说明](https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxsmrzztcx.md#微信实名认证申请单状态)（官网相对地址原文：`#微信实名认证申请单状态`）；示例值：APPLYMENT_STATE_PASSED |
| `response.data.authorize_stat` | 实名授权状态 | `String` | `16` | `N` | 授权状态 1：授权成功；0：授权失败；示例值：1 |
| `response.data.pay_channel_id` | 子渠道号 | `String` | `32` | `N` | 示例值：JQF00001 |
| `response.data.pay_scene` | 支付场景 | `String` | `2` | `N` | 示例值：01 |
| `response.data.qrcode_data` | 授权二维码 | `String` | `1000` | `N` | 1、当申请单状态为APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT、；APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON、；APPLYMENT_STATE_PASSED、；APPLYMENT_STATE_FREEZED时，会返回二维码图片。；2、使用base64解码该字段，可得到图片二进制数据。； 3、可用img标签直接加载该图片。； 示例值：[官网敏感示例已脱敏] |
| `response.data.reject_param` | 驳回参数 | `String` | `1000` | `N` | 当申请单状态为“审核驳回”时，会返回该字段，标识被驳回的字段名。；多个参数名以“\|”分割；示例值：licence_number\|cert_number |
| `response.data.reject_reason` | 驳回原因 | `String` | `1000` | `N` | 当申请单状态为“审核驳回”时，会返回该字段，表示驳回原因。 |
| `response.data.smid` | 微信真实商户号 | `String` | `32` | `N` | 示例值：[官网敏感示例已脱敏] |

## 支付宝实名申请提交

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_zfbsmrz.md>
- SHA-256：`37418d1dc993c3cbac002e0b4be2607ae929f85b7609f48141a52ac10cc37c5e`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | 签名，对报文整体签名 |
| `response.data` | 交易响应内容体 | `String` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 示例值：rQ[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 请求日期格式yyyyMMdd；示例值：20220809 |
| `request.data.huifu_id` | 汇付ID | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] |
| `request.data.pay_channel_id` | 子渠道号 | `String` | `32` | `N` | 如需要填写汇付和渠道商约定的值，参见[支付渠道号说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo)；示例值：JQF00001 |
| `request.data.pay_scene` | 业务开通类型 | `String` | `2` | `N` | 1-线下扫码；示例值：1 |
| `request.data.auth_identity_info` | 主体信息 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.auth_identity_info.business_type` | 主体类型 | `String` | `32` | `Y` | 枚举定义：；0 - 个人/小微；1 - 政府机构；2 - 国营企业；3 - 私营企业；4 - 外资企业；5 - 个体工商户；6 - 社会组织 ；7 - 事业单位 ；示例值：3 |
| `request.data.auth_identity_info.finance_institution_flag` | 是否金融机构 | `String` | `1` | `N` | Y-金融机构，N-非金融机构；默认值：N；示例值：N |
| `request.data.auth_identity_info.financial_type` | 金融机构类型 | `String` | `32` | `N` | 当主体是金融机构时，必填；金融机构类型需与营业执照/登记证书上一致。；BANK_AGENT：银行业, 适用于商业银行、政策性银行、农村合作银行、村镇银行、开发性金融机构等；PAYMENT_AGENT：支付机构, 适用于非银行类支付机构；INSURANCE：保险业, 适用于保险、保险中介、保险代理、保险经纪等保险类业务；TRADE_AND_SETTLE：交易及结算类金融机构, 适用于交易所、登记结算类机构、银行卡清算机构、资金清算中心等；OTHER：其他金融机构, 适用于财务公司、信托公司、金融资产管理公司、金融租赁公司、汽车金融公司、贷款公司、货币经纪公司、消费金融公司、证券业、金融控股公司、股票、期货、货币兑换、小额贷款公司、金融资产管理、担保公司、商业保理公司、典当行、融资租赁公司、财经咨询等其他金融业务；示例值：BANK_AGENT |
| `request.data.auth_identity_info.finance_license_pics` | 金融机构许可证图片 | `String` | `350` | `N` | 当主体是金融机构时，必填；上送图片上传返回的jfileId，文件类型F236~F240。最多五张图片使用“,”分隔；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529,57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.auth_identity_info.certificate_type` | 证照类型 | `String` | `32` | `N` | 营业执照(BUSINESS_CERT)；登记证书(REGISTER_CERT)；示例值：BUSINESS_CERT；主体类型为企业/个体户/政府机关/事业单位/社会组织时（1/2/3/4/5/6/7），必填；主体为政府机关/事业单位/社会组织时（1/6/7），填登记证书；主体类型为企业/个体户时（2/3/4/5），填营业执照 |
| `request.data.auth_identity_info.certificate_info` | 登记证书信息 | `String` | `—` | `N` | jsonObject字符串；主体类型为企业/个体户/政府机关/事业单位/社会组织（1/2/3/4/5/6/7）时必填，**小微商户切勿填写** |
| `request.data.auth_identity_info.certificate_info.cert_type` | 登记证书类型 | `String` | `32` | `C` | **证照类型为登记证书时(certificate_type=REGISTER_CERT)必填**。枚举：；统一社会信用代码证书(CERTIFICATE_TYPE_2389)；慈善组织公开募捐资格证书(CERTIFICATE_TYPE_2397)；社会团体法人登记证书(CERTIFICATE_TYPE_2394)；民办非企业单位登记证书(CERTIFICATE_TYPE_2395)；基金会法人登记证书(CERTIFICATE_TYPE_2396)；农民专业合作社法人营业执照(CERTIFICATE_TYPE_2398)；宗教活动场所登记证(CERTIFICATE_TYPE_2399)；其他证书/批文/证明(CERTIFICATE_TYPE_2400)；示例值：CERTIFICATE_TYPE_2389 |
| `request.data.auth_identity_info.certificate_info.cert_number` | 证照编号 | `String` | `64` | `N` | 示例值：[官网敏感示例已脱敏] |
| `request.data.auth_identity_info.certificate_info.cert_copy` | 证照图片 | `String` | `128` | `N` | 上送图片上传返回的jfileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.auth_identity_info.certificate_info.cert_merchant_name` | 证照商户名称 | `String` | `64` | `N` | 示例值：新新饭店 |
| `request.data.auth_identity_info.certificate_info.cert_legal_person` | 证照法人姓名 | `String` | `64` | `N` | 示例值：李四 |
| `request.data.auth_identity_info.certificate_info.cert_company_address` | 证照注册地址 | `String` | `128` | `N` | 示例值：浙江省杭州市西湖区xxx街道xxx门牌号 |
| `request.data.auth_identity_info.certificate_info.effect_time` | 证照生效时间 | `String` | `32` | `N` | 示例值：19990101 |
| `request.data.auth_identity_info.certificate_info.expire_time` | 证照过期时间 | `String` | `32` | `N` | 示例值：20201101，若证件有效期为长期，请填写：长期 |
| `request.data.auth_identity_info.company_prove_copy` | 单位证明函照片 | `String` | `128` | `N` | 上送图片上传返回的jfileId，文件类型F46。主体类型为政府机关/事业单位时必填；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.auth_identity_info.support_credentials` | 辅助证明材料信息 | `String` | `—` | `N` | jsonObject字符串 ； 主体类型为小微商户时，辅助证明材料信息必填 |
| `request.data.auth_identity_info.support_credentials.micro_biz_type` | 小微经营类型 | `String` | `32` | `Y` | 门店场所：MICRO_TYPE_STORE；流动经营/便民服务：MICRO_TYPE_MOBILE；示例值：MICRO_TYPE_STORE |
| `request.data.auth_identity_info.support_credentials.store_name` | 门店名称 | `String` | `64` | `Y` | 示例值：肯德基共富新村店 |
| `request.data.auth_identity_info.support_credentials.province_code` | 门店省市编码 | `String` | `32` | `Y` | [参考地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310000 |
| `request.data.auth_identity_info.support_credentials.province` | 门店省份 | `String` | `32` | `Y` | 示例值：浙江省 |
| `request.data.auth_identity_info.support_credentials.city_code` | 门店市行政区号 | `String` | `32` | `Y` | [参考地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310100 |
| `request.data.auth_identity_info.support_credentials.city` | 门店城市 | `String` | `32` | `Y` | 示例值：杭州市 |
| `request.data.auth_identity_info.support_credentials.district_code` | 门店街道区号 | `String` | `32` | `Y` | [参考地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310101 |
| `request.data.auth_identity_info.support_credentials.district` | 门店街道 | `String` | `32` | `Y` | 最长16个汉字；示例值：西湖区留下街道 |
| `request.data.auth_identity_info.support_credentials.store_address` | 门店场所填写门店详细地址 | `String` | `128` | `Y` | 门店场所填写门店详细地址，流动经营类型填“无”；示例值：上海宝山区共富路512号 |
| `request.data.auth_identity_info.support_credentials.store_door_img` | 门店门头照信息或摊位照 | `String` | `128` | `N` | 为空时取开户或开业务时上送的门头照片，文件类型F22；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.auth_identity_info.support_credentials.store_inner_img` | 门店店内照片或者摊位照侧面 | `String` | `128` | `N` | 为空时取开户或开业务时上送的店铺内景图片，文件类型F24；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.auth_identity_info.qualification_info_list[]` | 经营许可证 | `String` | `—` | `N` | jsonArray字符串 1、填写特殊行业的经营许可证信息 2、最多填写支持5个行业 |
| `request.data.auth_identity_info.qualification_info_list[].mcc_code` | 行业类目id | `String` | `20` | `Y` | 参见[支付宝商家行业二级类目code](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_zfbmcc)；示例值：5411 |
| `request.data.auth_identity_info.qualification_info_list[].image_list` | 行业经营许可证资质照片 | `String` | `400` | `Y` | 上送图片上传返回的jfileId，一个行业类目下最多上传6张资质照片，文件类型F150~F155。使用“,”分隔；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529,57cc7f00-600a-33ab-b614-6221bbf2e534 |
| `request.data.legal_person_info` | 法人身份信息 | `String` | `—` | `N` | jsonObject字符串；为空时取开户时法人信息 |
| `request.data.legal_person_info.legal_type` | 证件持有人类型 | `String` | `32` | `N` | 法人：LEGAL，为空时默认选项； 主体类型为企业、个体户、社会组织、小微商户时，必须为经营者/法人。；经办人：SUPER；主体类型为政府机关、事业单位时默认是法人。若因特殊情况，无法提供法人证件时可填经办人类型。；示例值：LEGAL |
| `request.data.legal_person_info.card_type` | 证件类型 | `String` | `2` | `N` | 枚举值：；00:身份证 01:护照 13：港澳居民证 14:台湾居民证；为空时取开户时法人信息 ；个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关、小微商户仅支持身份证类型。；示例值：00 |
| `request.data.legal_person_info.person_name` | 法人姓名 | `String` | `64` | `N` | 为空时取开户时法人信息；示例值：李四 |
| `request.data.legal_person_info.card_no` | 证件号码 | `String` | `64` | `N` | 为空时取开户时法人信息；示例值：[官网敏感示例已脱敏] |
| `request.data.legal_person_info.effect_time` | 证件生效时间 | `String` | `32` | `N` | 为空时取开户时法人信息；示例值：19990101 |
| `request.data.legal_person_info.expire_time` | 证件过期时间 | `String` | `32` | `N` | 为空时取开户时法人信息；示例值：20001101，长期有效时传“长期” |
| `request.data.legal_person_info.card_front_img` | 证件人像面 | `String` | `128` | `N` | 为空时取开户时法人信息，如果开户时未传该字段必填；上送[图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)返回的jfileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.legal_person_info.card_back_img` | 证件国徽面 | `String` | `128` | `N` | 为空时取开户时法人信息，如果开户时未传该字段必填；只有身份证类型需要上传反面；上送[图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)返回的jfileId，示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.legal_person_info.auth_letter_img` | 授权函照片 | `String` | `128` | `N` | 上送图片上传返回的jfileId；文件类型F224业务办理授权函；当证件持有人类型为经办人时必须上传。其他情况，无需上传。；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.legal_person_info.is_benefit_person` | 是否为受益人 | `String` | `1` | `N` | Y-受益人;N-非受益人 默认值：Y；示例值：Y |
| `request.data.contact_person_info` | 联系人信息 | `String` | `—` | `Y` | jsonObject字符串 |
| `request.data.contact_person_info.name` | 联系人姓名 | `String` | `64` | `N` | 为空时取企业商户取联系人姓名，个人商户取入驻时填写的名称；示例值：[官网敏感示例已脱敏] |
| `request.data.contact_person_info.mobile` | 联系人手机号 | `String` | `11` | `N` | 为空时取企业商户取联系人手机号；示例值：[官网示例已脱敏] |
| `request.data.contact_person_info.id_card_number` | 联系人身份证号码 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.ubo_info` | 受益人信息 | `String` | `—` | `N` | jsonObject字符串；主体为企业，且经营者/法人不是最终受益人，因为受益人是第三方所以必需填写 |
| `request.data.ubo_info.ubo_id_doc_name` | 证件姓名 | `String` | `128` | `Y` | 示例值：李四 |
| `request.data.ubo_info.ubo_id_doc_type` | 证件类型 | `String` | `10` | `Y` | 枚举值：；00:身份证； 01:护照； 13：港澳居民证； 14:台湾居民证；示例值：00；个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关、小微商户仅支持身份证类型。 |
| `request.data.ubo_info.ubo_id_doc_number` | 证件号码 | `String` | `128` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.ubo_info.ubo_period_begin` | 证件有效期开始时间 | `String` | `20` | `Y` | 格式：yyyyMMdd； 示例值：20190606 |
| `request.data.ubo_info.ubo_period_end` | 证件有效期结束时间 | `String` | `20` | `Y` | 1、格式：yyyyMMdd； 示例值：20290606；若证件有效期为长期，请填写：长期；2、结束时间大于开始时间 |
| `request.data.ubo_info.ubo_id_doc_copy` | 证件人像面 | `String` | `64` | `Y` | 上送图片上传返回的jfileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.ubo_info.ubo_id_doc_copy_back` | 证件国徽面 | `String` | `64` | `N` | 上送图片上传返回的jfileId，只有身份证类型需要上传反面；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 返回码 | `String` | `8` | `Y` | [交易返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 返回描述 | `String` | `512` | `Y` | [交易返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.applyment_id` | 申请单编号 | `String` | `256` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.order_status` | 意愿申请单状态 | `String` | `32` | `N` | 枚举值：；审核中(AUDITING)；待联系人确认(CONTACT_CONFIRM)；待法人确认(LEGAL_CONFIRM)；审核通过(AUDIT_PASS)；审核失败(AUDIT_REJECT)；已冻结(AUDIT_FREEZE)；本次申请冻结但仍会返回上次的授权码，可以扫码授权。；已撤回(CANCELED)示例值：AUDIT_PASS |

## 支付宝实名申请单查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_zfbsmcx.md>
- SHA-256：`cf2e66377106963060ac93656e20bfbc13e0dc4f1a1eaba0b935e9e7f2a8bed6`
- 说明：完整保留官方类型、长度、必填标记和说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 示例值：rQ[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 必填，请求日期yyyyMMdd，示例值：20220809 |
| `request.data.huifu_id` | 汇付ID | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] |
| `request.data.pay_channel_id` | 子渠道号 | `String` | `32` | `N` | 如需要填写汇付和渠道商约定的值，参见[支付渠道号说明](https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo)；示例值：JQF00001 |
| `request.data.pay_scene` | 支付场景 | `String` | `2` | `N` | 支付宝只支持1-线下扫码；示例值：1 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 返回码 | `String` | `8` | `Y` | 示例值：00000000；参见[交易返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 返回描述 | `String` | `512` | `Y` | 示例值：成功；参见[交易返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.order_no` | 意愿申请单号 | `String` | `64` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.order_status` | 申请单状态 | `String` | `64` | `N` | 枚举值：；审核中(AUDITING)；待联系人确认(CONTACT_CONFIRM)；待法人确认(LEGAL_CONFIRM)；审核通过(AUDIT_PASS)；审核失败(AUDIT_REJECT)；已冻结(AUDIT_FREEZE)本次申请冻结但仍会返回上次的授权码，可以扫码授权。；已撤回(CANCELED)；未申请(NOT_APPLY)；示例值：AUDITING |
| `response.data.qrcode` | 二维码图片地址 | `String` | `128` | `N` | 申请单状态处于CONTACT_CONFIRM、LEGAL_CONFIRM返回，商户使用支付宝APP扫码后完成后续确认动作；示例值：[官网敏感示例已脱敏] |
| `response.data.reject_reason[]` | 审核失败原因 | `String` | `—` | `N` | jsonArray字符串 |
| `response.data.reject_reason[].fail_param` | 审核失败字段 | `String` | `64` | `N` | 示例值：cert_number |
| `response.data.reject_reason[].fail_reason` | 描述申请单审核失败原因 | `String` | `128` | `N` | 示例值：证照编号对应的企业名称、法人名称与录入信息不一致 |
| `response.data.smid` | 支付宝真实商户号 | `String` | `32` | `N` | 示例值：[官网敏感示例已脱敏] |
| `response.data.authorize_stat` | 经办人授权状态 | `String` | `20` | `N` | 已确认（AUTHORIZED）；未确认（UNAUTHORIZED）；已销户（CLOSED）；“已销户”指该商户已销户；smid不存在(SMID_NOT_EXIST)；示例值：AUTHORIZED |
| `response.data.check_result_list[]` | 子商户号授权状态集合 | `String` | `—` | `N` | jsonArray字符串 |
| `response.data.check_result_list[].bank_mer_code` | 支付宝子商户号 | `String` | `32` | `Y` | 示例值:[官网示例已脱敏] |
| `response.data.check_result_list[].channel_type` | 通道类型 | `String` | `1` | `Y` | U-银联，N-网联；示例值:N |
| `response.data.check_result_list[].check_result` | 确认状态 | `String` | `64` | `Y` | 已确认(AUTHORIZED)；未确认(UNAUTHORIZED)；已销户(CLOSED)；smid不存在(SMID_NOT_EXIST)；示例值:AUTHORIZED |
