# 商户进件十三接口完整字段目录

本文件由仓库维护脚本从十三份官方原文机械生成。它负责“字段不遗漏”；高风险枚举、默认值、条件冲突和输出边界仍同时读取 `merchant-onboarding-field-contracts.md` 及对应接口 reference。

安全说明：官方说明中的商户号、证件号、手机号、长流水和示例图片 URL 已机械脱敏；这些示例本来就不是默认值。字段规则、枚举、条件、材料编号和外部资料地址不做脱敏。

## 目录

- [生成覆盖摘要](#生成覆盖摘要)
- [企业商户进件](#企业商户进件)
- [个人商户进件](#个人商户进件)
- [商户业务开通](#商户业务开通)
- [图片上传](#图片上传)
- [商户详细信息查询](#商户详细信息查询)
- [申请单状态查询](#申请单状态查询)
- [商户业务开通修改](#商户业务开通修改)
- [商户基本信息修改](#商户基本信息修改)
- [商户费率信息查询](#商户费率信息查询)
- [商户状态变更](#商户状态变更)
- [商户短信发送](#商户短信发送)
- [商户多费率配置](#商户多费率配置)
- [商户多费率配置查询](#商户多费率配置查询)

使用规则：

1. 回答任一接口字段问题时，先在本文件定位完整路径，再读取对应接口 reference 的约束说明。
2. 不得只读取顶层字段后推断嵌套对象；必须沿 `[]` / 对象路径读到叶子层。
3. 不得按叶字段名去重：`request.data.prov_id/area_id` 是经营省市，`request.data.card_info.prov_id/area_id` 是结算卡省市；适用时两组都保留，后者只能位于 String(JSON) `card_info` 内。企业进件 `request.data.material_card_info.prov_id/area_id` 属于补充对公同名账户，当前 request/response 的 `material_card_info` 均正式定义为 String(JSON Object)，整体序列化或反序列化。详情响应的 `response.data.material_card_info.prov_id/area_id` 是独立响应路径。四组字段均不得合并。基本信息修改的 `card_info.area_id` 长度为 `8`，企业/个人进件对应路径长度为 `6`；当前材料账户请求支行长度8、详情响应12，各自保留，不得静默统一。
4. 官方表格自身冲突时保留原始类型、长度、必填和说明，不自行“修正”；在答案中明确标记 `[官方文档口径冲突]`。
5. 字段说明引用外部网页或文件时，再读取 `merchant-onboarding-external-resources.md` 并给出原始地址。绝对链接保持官网值；相对链接按已登记的官方文档命名空间（无例外时按来源页）解析成可点击地址，同时保留官网相对地址原文。回调、跳转、下载、二维码或图片裸 URL 示例不是资料或默认值。

## 生成覆盖摘要

| 接口 | 字段路径总数 | 扩展表数量 | 最大路径深度 |
| --- | ---: | ---: | ---: |
| 企业商户进件 | 177 | 10 | 5 |
| 个人商户进件 | 129 | 7 | 5 |
| 商户业务开通 | 472 | 57 | 7 |
| 图片上传 | 8 | 0 | 3 |
| 商户详细信息查询 | 602 | 69 | 6 |
| 申请单状态查询 | 93 | 8 | 4 |
| 商户业务开通修改 | 465 | 56 | 8 |
| 商户基本信息修改 | 199 | 12 | 5 |
| 商户费率信息查询 | 35 | 4 | 4 |
| 商户状态变更 | 14 | 0 | 3 |
| 商户短信发送 | 20 | 0 | 3 |
| 商户多费率配置 | 27 | 3 | 4 |
| 商户多费率配置查询 | 17 | 1 | 4 |

## 企业商户进件

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md>
- SHA-256：`6606629100f94813a7a4238c8f1ffc970ec3b905d1af9487bb92baee6138822e`
- 说明：下表保留官方字段类型、长度、必填标记和字段说明；数组父路径以 `[]` 标记。

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
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号，当日唯一；示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd，示例值：20220125 |
| `request.data.upper_huifu_id` | 渠道商号 | `String` | `18` | `C` | 该商户进件完成后归属的渠道商huifu_id；sys_id主体为渠道商时填写；sys_id主体为总部商户时选填；示例值：[官网示例已脱敏] |
| `request.data.reg_name` | 商户名称 | `String` | `64` | `Y` | 必须与企业证照上的名称一致；个体工商户的营业执照如没有名称，名称为“\*”或空，则商户名称应填 “个体户XXX”（XXX为营业执照上经营者姓名），如“个体户张三”，汉字以2个字符计算；示例值：上海汇付支付有限公司 |
| `request.data.short_name` | 商户简称 | `String` | `64` | `Y` | 最少4个字符；会展示在消费账单上；示例值：汇付商城 |
| `request.data.receipt_name` | 小票名称 | `String` | `50` | `Y` | 小票名称展示在POS小票上；示例值：汇付商城 |
| `request.data.mer_en_name` | 商户英文名称 | `String` | `256` | `N` | 示例值：huifupay |
| `request.data.ent_type` | 公司类型 | `String` | `1` | `Y` | 当use_head_info_flag=Y时不填；1：政府机构；2：国营企业；3：私营企业；4：外资企业；5：个体工商户；6：其它组织；7：事业单位；9：业主委员会；示例值：1 |
| `request.data.mcc` | 所属行业 | `String` | `7` | `C` | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；当use_head_info_flag=Y时不填；示例值：5311 |
| `request.data.busi_type` | 经营类型 | `String` | `1` | `C` | 1：实体，2：虚拟 ；示例值：1 ；当use_head_info_flag=Y时不填 |
| `request.data.scene_type` | 场景类型 | `String` | `8` | `Y` | ONLINE：线上场景；OFFLINE：线下场景；ALL：线上线下；示例值：ALL |
| `request.data.license_pic` | 证照图片 | `String` | `64` | `Y` | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F07；**注意执照不能是过期的**；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.license_code` | 证照编号 | `String` | `18` | `Y` | 工商营业执照编号；当use_head_info_flag=Y时不填；公司类型为业主委员会，输入业主委员会备案证明上负责人的身份证号码；示例值：92650109MA79R8E308 |
| `request.data.license_type` | 证照类型 | `String` | `32` | `N` | 参见[机构证照类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E6%9C%BA%E6%9E%84%E8%AF%81%E7%85%A7%E7%B1%BB%E5%9E%8B)说明；默认NATIONAL_LEGAL_MERGE；示例值：NATIONAL_LEGAL |
| `request.data.license_validity_type` | 证照有效期类型 | `String` | `1` | `Y` | 0：非长期有效,1：长期有效；当use_head_info_flag=Y时不填；示例值：0 |
| `request.data.license_begin_date` | 证照有效期开始日期 | `String` | `8` | `Y` | 格式：yyyyMMdd；示例值：20220125；当use_head_info_flag=Y时不填 |
| `request.data.license_end_date` | 证照有效期截止日期 | `String` | `8` | `C` | 格式：yyyyMMdd。示例值：20220125； 当license_validity_type=0时必填；当license_validity_type=1时为空；当use_head_info_flag=Y时不填 |
| `request.data.found_date` | 成立时间 | `String` | `8` | `Y` | 示例值：20091212 |
| `request.data.reg_capital` | 注册资本 | `String` | `16` | `C` | 保留两位小数；条件必填，国营企业、私营企业、外资企业、事业单位、其他、集体经济必填，政府机构、个体工商户可为空；示例值：100.00 |
| `request.data.business_scope` | 经营范围 | `String` | `1000` | `N` | 示例值：日用百货、化妆品、珠宝、化工原料及产品(除危险品)、化学品、纺织原料 |
| `request.data.reg_prov_id` | 注册省 | `String` | `6` | `N` | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310000；当use_head_info_flag=Y时不填 |
| `request.data.reg_area_id` | 注册市 | `String` | `6` | `N` | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310100；当use_head_info_flag=Y时不填 |
| `request.data.reg_district_id` | 注册区 | `String` | `6` | `Y` | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310101；当use_head_info_flag=Y时不填 |
| `request.data.reg_detail` | 注册详细地址 | `String` | `255` | `Y` | 商户注册地址或营业执照住所，汉字以2个字符计算；示例值：上海市徐汇区XX路XX号；当use_head_info_flag=Y时不填 |
| `request.data.prov_id` | 经营省 | `String` | `6` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310000 |
| `request.data.area_id` | 经营市 | `String` | `6` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310100 |
| `request.data.district_id` | 经营区 | `String` | `6` | `Y` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310101 |
| `request.data.detail_addr` | 经营详细地址 | `String` | `256` | `C` | scene_type=OFFLINE/ALL时必填；示例值：上海市徐汇区XX路XX号 |
| `request.data.legal_name` | 法人姓名 | `String` | `32` | `Y` | 法人或负责人姓名，最大支持16个汉字；注意有名字中有“·”时要与银行账号名一致；示例值：张三；当use_head_info_flag=Y时不填 |
| `request.data.legal_cert_type` | 法人证件类型 | `String` | `2` | `Y` | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》；示例值：00；当use_head_info_flag=Y时不填；开通全域资金管理功能只支持法人证件类型是身份证；法人证件类型04、11、14需要补充 F31【法人】港澳台居民来往内地通行证；法人证件类型13需要补充F511【法人】外国人居留证；法人证件类型15需要补充F512【法人】港澳台居住证；其它法人证件类型补充F32【法人】其它证件材料；补充材料填写在extended_material_list 扩展资料包中 |
| `request.data.legal_cert_no` | 法人证件号码 | `String` | `32` | `Y` | 如法人证件类型为00：身份证，则填写身份证号码；当use_head_info_flag=Y时不填；年龄不能小于18岁且不能大于80岁；示例值：[官网示例已脱敏] |
| `request.data.legal_cert_validity_type` | 法人证件有效期类型 | `String` | `1` | `Y` | 1：长期有效；0：非长期有效 ；示例值 ：0 |
| `request.data.legal_cert_begin_date` | 法人证件有效期开始日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd，示例值：20220125；当use_head_info_flag=Y时不填 |
| `request.data.legal_cert_end_date` | 法人证件有效期截止日期 | `String` | `8` | `C` | 日期格式：yyyyMMdd， 示例值：20220125；当legal_cert_validity_type=0时必填；当legal_cert_validity_type=1时为空；当use_head_info_flag=Y时不填 |
| `request.data.legal_mobile_no` | 法人手机号 | `String` | `11` | `N` | 示例值：[官网示例已脱敏]；全域资金业务必填 |
| `request.data.legal_addr` | 法人证件地址 | `String` | `256` | `Y` | 示例值：上海市徐汇区宜山路700号普天信息产业园2期C5栋 |
| `request.data.legal_cert_back_pic` | 法人身份证国徽面 | `String` | `64` | `Y` | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F03；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.legal_cert_front_pic` | 法人身份证人像面 | `String` | `64` | `Y` | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F02；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.beneficiary_info[]` | 受益人列表 | `String` | `—` | `N` | jsonArray字符串 |
| `request.data.beneficiary_info[].bo_name` | 受益人名称 | `String` | `40` | `Y` | 示例值：张三 |
| `request.data.beneficiary_info[].bo_type` | 受益人证件类型 | `String` | `2` | `Y` | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》以及12:营业执照；示例值：12 |
| `request.data.beneficiary_info[].bo_no` | 受益人证件号 | `String` | `50` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.beneficiary_info[].bo_date_start` | 受益人证件有效期开始时间 | `String` | `8` | `Y` | 示例值：20210606 |
| `request.data.beneficiary_info[].bo_dead_line` | 受益人证件有效期结束时间 | `String` | `8` | `Y` | 示例值：20290606；若证件有效期为长期，请填写：29991231；要求结束时间大于开始时间 |
| `request.data.beneficiary_info[].bo_address` | 受益人证件地址 | `String` | `500` | `Y` | 示例值：上海徐汇区共富一路55号401室 |
| `request.data.beneficiary_info[].bo_mobile_no` | 受益人手机号 | `String` | `11` | `C` | 开通全域资金管理业务时必填；示例值：[官网示例已脱敏] |
| `request.data.beneficiary_info[].final_beneficiary_mode` | 最终受益人受益方式 | `String` | `3` | `C` | A01：直接或间接控股25%（含）以上 ；A02：通过人事、财务等其他方式对公司进行控制 ；A03：高级管理人员 ；A04：法人或公司负责人 ；A05：其他；示例值：A01；开通全域资金管理业务时必填 |
| `request.data.contact_name` | 管理员姓名 | `String` | `128` | `N` | 默认法人姓名；示例值：张三 |
| `request.data.contact_mobile_no` | 管理员手机号 | `String` | `11` | `Y` | 需为11位数字 ；示例值：[官网示例已脱敏] |
| `request.data.contact_email` | 管理员电子邮箱 | `String` | `32` | `Y` | 需要带@，遵循邮箱格式；示例值：huifu@xxx.com |
| `request.data.sms_send_flag` | 商户通知标识 | `String` | `1` | `N` | 进件成功后通知商户联系人，；M：发送短信通知；E：发送邮件通知；A：短信、邮件都通知；为空：不作通知。 ；示例值：M |
| `request.data.login_name` | 管理员账号 | `String` | `32` | `Y` | 用于商户平台登录。全局唯一。支持英文、数字、下划线，区分大小写 ；示例值：huifu001 |
| `request.data.service_phone` | 客服电话 | `String` | `32` | `N` | 默认联系人手机号；示例值：021XXXXXXXX |
| `request.data.reg_acct_pic` | 开户许可证 | `String` | `64` | `C` | 企业商户需要，结算账号为对公账户必填；通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F08；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.card_info` | 银行卡信息配置 | `String` | `—` | `Y` | 商户银行账户信息配置，jsonObject字符串 ；开通中信E管家结算的银行卡配置在【elec_acct_config】中 |
| `request.data.card_info.card_type` | 银行账户类型 | `String` | `1` | `Y` | 0：对公账户 1：对私法人账户 2：对私非法人账户 示例值：0 |
| `request.data.card_info.card_name` | 银行账户名 | `String` | `128` | `Y` | 示例值：上海汇付支付有限公司； 当card_type=0时填写企业名称，**企业非同名时，需要在extended_material_list中额外上传非同名结算证明材料，文件枚举：F516**； 当card_type=1时填写法人姓名，**对私法人银行账户名与法人姓名必需一致**；当card_type=2时填写非法人姓名 |
| `request.data.card_info.card_no` | 银行账号 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏]；注意：**系统会验证卡号所属银行**，请准确填写 |
| `request.data.card_info.prov_id` | 银行所在省 | `String` | `6` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000；如修改省市要级联修改 |
| `request.data.card_info.area_id` | 银行所在市 | `String` | `6` | `Y` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310100；如修改省市要级联修改 |
| `request.data.card_info.branch_code` | 联行号 | `String` | `12` | `C` | 当card_type=0时必填，参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm) 当card_type=0时必填， 当card_type=1或2时非必填 ；示例值：102290026507 |
| `request.data.card_info.cert_type` | 持卡人证件类型 | `String` | `2` | `C` | 持卡人证件类型，参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》。； 当card_type=0时为空， 当card_type=1或2时必填； 示例值：00；持卡人证件类型04、11需要补充 F101【结算人】港澳台居民来往内地通行证；持卡人证件类型13需要补充 F513【结算人】外国人居留证；持卡人证件类型14、15需要补充 F514【结算人】港澳台居住证；其它持卡人证件类型补充F102【结算人】其它证件材料；补充材料填写在extended_material_list 扩展资料包中 |
| `request.data.card_info.cert_no` | 持卡人证件号码 | `String` | `32` | `C` | 对私必填；年龄不小于18岁且不能大于80岁；如持卡人证件类型为00：身份证，则填写身份证号码；示例值：[官网示例已脱敏] |
| `request.data.card_info.cert_validity_type` | 持卡人证件有效期类型 | `String` | `1` | `N` | 1:长期有效 0:非长期有效；示例值：0 |
| `request.data.card_info.cert_begin_date` | 持卡人证件有效期开始日期 | `String` | `8` | `N` | 日期格式：yyyyMMdd，示例值：20220125 |
| `request.data.card_info.cert_end_date` | 持卡人证件有效期截止日期 | `String` | `8` | `C` | 日期格式：yyyyMMdd，示例值：20220125； 当cert_validity_type=0时必填；当cert_validity_type=1时为空 |
| `request.data.card_info.mp` | 银行卡绑定手机号 | `String` | `11` | `C` | 11位数字，开通全域资金管理功能必填； 示例值：[官网示例已脱敏] |
| `request.data.card_info.is_settle_default` | 默认结算卡标志 | `String` | `1` | `N` | 是否为默认结算卡标志；Y:是 N:否(为空默认)；示例值：Y |
| `request.data.settle_config` | 结算业务配置 | `String` | `—` | `N` | 商户结算规则配置，jsonObject字符串 |
| `request.data.settle_config.settle_cycle` | 结算周期 | `String` | `2` | `Y` | D1：下个自然日结算， T1：下个工作日结算；TS:笔笔结算； 示例值：T1 |
| `request.data.settle_config.min_amt` | 起结金额 | `String` | `14` | `N` | settle_cycle为TS时不填。账户余额大于等于起结金额才会发起结算；单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。；示例值：1000.00 |
| `request.data.settle_config.remained_amt` | 留存金额 | `String` | `14` | `N` | settle_cycle为TS时不填。该部分资金不会结算。；单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。；示例值：1000.00 |
| `request.data.settle_config.settle_abstract` | 结算摘要 | `String` | `128` | `N` | 可自定义结算打款备注，不填默认为空；支持配置格式化摘要内容，参见[结算配置示例说明](https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm)；示例值：汇付商城业务 |
| `request.data.settle_config.out_settle_flag` | 手续费外扣标记 | `String` | `1` | `N` | 1:外扣，结算时从out_settle_huifuid账户扣手续费 ；2:内扣，从结算金额中扣手续费，默认为内扣；示例值：2 |
| `request.data.settle_config.out_settle_huifuid` | 结算手续费外扣商户号 | `String` | `18` | `C` | 填写承担手续费的汇付商户号；当out_settle_flag=1时必填，否则非必填；示例值：[官网示例已脱敏] |
| `request.data.settle_config.out_settle_acct_type` | 结算手续费外扣账户类型 | `String` | `2` | `N` | 01：基本户（不填默认取值）；02：现金户；05：充值户；09：营销户；示例值：01 |
| `request.data.settle_config.settle_pattern` | 结算方式 | `String` | `2` | `N` | settle_cycle为TS时不填。 P0：批次结算 ，~~P1：定时结算~~(建议选P0和P2)，P2:批次定时结算，E1:中信E管家 ，示例值：P1批次结算指按照指定结算批次号进行资金结算，自定义时间结算是指按照商户指定到账时间进行资金结算。两种结算方式需二选一，不填默认P0：批次结算 |
| `request.data.settle_config.settle_batch_no` | 结算批次号 | `String` | `16` | `C` | settle_cycle为TS时不填。当settle_pattern=P0批次结算时必填，即将按指定结算批次号进行资金结算；示例值：100；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| `request.data.settle_config.is_priority_receipt` | 是否优先到账 | `String` | `1` | `N` | settle_cycle为TS时不填。当settle_pattern=P0时选填，不填默认为N，该值在结算那批次号[0-500]间生效； Y：是，N：否，示例值：Y |
| `request.data.settle_config.settle_time` | 自定义结算处理时间 | `String` | `6` | `C` | settle_cycle为TS时不填。当settle_pattern=P1/P2自定义时间结算时必填；注意：00:00到00:30不能指定；到账时间，格式：HHmmss；示例值：103000 |
| `request.data.settle_config.fixed_ratio` | 节假日结算手续费率 | `String` | `6` | `C` | settle_cycle为D1、TS时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；示例值：0.05 |
| `request.data.settle_config.constant_amt` | 节假日结算手续费固定金额 | `String` | `15` | `C` | settle_cycle为D1、TS时必填。单位元，需保留小数点后两位。不收费请填写0.00；settle_cycle结算周期为D1时，遇节假日按此费率结算；示例值：1.00 |
| `request.data.settle_config.workday_fixed_ratio` | 工作日结算手续费率 | `String` | `6` | `N` | settle_cycle为TS时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；示例值：0.05 |
| `request.data.settle_config.workday_constant_amt` | 工作日结算手续费固定金额 | `String` | `15` | `N` | settle_cycle为TS时必填。单位元，需保留小数点后两位。不填默认为0.00；示例值：1.00 |
| `request.data.settle_card_front_pic` | 银行卡卡号面 | `String` | `64` | `C` | **对私必填**。通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F13；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.settle_cert_back_pic` | 持卡人身份证国徽面 | `String` | `64` | `C` | **对私必填**。通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F56；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.settle_cert_front_pic` | 持卡人身份证人像面 | `String` | `64` | `C` | **对私必填**。通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F55；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.auth_entrust_pic` | 授权委托书 | `String` | `64` | `C` | **对私非法人、对公非同名结算必填**；通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F15；开通银行电子账户（中信E管家）需提供F520；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.cash_config[]` | 取现业务配置 | `String` | `—` | `N` | 商户取现信息配置，jsonArray字符串 |
| `request.data.cash_config[].cash_type` | 取现类型 | `String` | `2` | `N` | D0：当日到账；可取现资金包括当天的交易资金；T1：下个工作日到账；默认值；D1：下个自然日到账;；DM：当日到账；可取现资金不包括当天的交易资金；示例值：T1 |
| `request.data.cash_config[].fix_amt` | 取现手续费（固定/元） | `String` | `6` | `C` | fix_amt与fee_rate至少填写一项， 需保留小数点后两位，不收费请填写0.00；示例值：1.00；注：当cash_type=D1时为节假日取现手续费；当cash_type=T1时为工作日取现手续费 |
| `request.data.cash_config[].fee_rate` | 取现手续费率（%） | `String` | `6` | `C` | fix_amt与fee_rate至少填写一项，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；示例值：0.05；注：1、如果fix_amt与fee_rate都填写了则手续费=fix_amt+支付金额\*fee_rate；2、当cash_type=D1时为节假日取现手续费；当cash_type=T1时为工作日取现手续费 |
| `request.data.cash_config[].weekday_fix_amt` | D1工作日取现手续费固定金额 | `String` | `6` | `C` | 单位元，需保留小数点后两位。不收费请填写0.00；示例值：1.00；cash_type=T1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算，若未配置则默认按照节假日手续费计算 |
| `request.data.cash_config[].weekday_fee_rate` | D1工作日取现手续费率 | `String` | `6` | `C` | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；示例值：0.05；cash_type=T1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算 ，若未配置则默认按照节假日手续费计算 |
| `request.data.cash_config[].out_fee_flag` | 是否取现手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认）；示例值：2 |
| `request.data.cash_config[].out_fee_huifu_id` | 手续费承担方 | `String` | `18` | `C` | 手续费外扣时必需指定手续费承担方ID ；示例值：[官网示例已脱敏] |
| `request.data.cash_config[].out_fee_acct_type` | 手续费外扣的账户类型 | `String` | `2` | `N` | 01-基本户，02-现金户，05-充值户，09-营销户；示例值：01不填默认01 |
| `request.data.cash_config[].is_priority_receipt` | 是否优先到账 | `String` | `1` | `N` | Y：是 ，N：否。不填，默认值为否。仅在cash_type为D1 和 T1 时生效。示例值：Y |
| `request.data.head_office_flag` | 商户身份 | `String` | `1` | `N` | 1：总部商户， 0：下级商户；不传默认普通商户。示例值：0；开通下级商户时，所选的上级商户需要有开通商户权限，需先调用“[开通下级商户权限配置接口](https://paas.huifu.com/open/doc/api/#/shgl/shywkt/api_shjj_shywkt_xjshpz)”； 当head_office_flag为1时，head_type必填，且需通过图片上传接口上传材料；（1）若head_type为0时，需要补充F718,F719,F720（工商截图、至少两个分公司或分支机构的办公地门头照）；（2）若head_type为1时，需要补充F721（行业综合许可证）；（3）若head_type为2时，加盟性质需要补充F722,F723,F724（至少两家门店的门头照、加盟协议），直营性质需要补充F722,F723,F724（提供至少两家门店的门头照、总部盖章说明函）；当head_office_flag为0时，需通过图片上传接口上传材料 ；（1）若对应总部的客群类型为0集团客户，需要补充F725 （集团盖章说明函）；（2）若对应总部的客群类型为1，需要补充F726 （下级商户入驻大型商业综合体的合作协议）；（3）若对应总部的客群类型为2，加盟性质需要补充F727（加盟协议），直营性质需要补充F727（总部盖章说明函） |
| `request.data.use_head_info_flag` | 使用上级资料信息 | `String` | `1` | `N` | Y:是 N：否；示例值：Y；选Y则部分信息复用上级，复用字段：；license_code-营业执照编号,；license_validity_type-营业执照有效期类型,；license_begin_date-营业执照有效期开始日期,；license_end_date-营业执照有效期截止日期,；reg_prov_id-注册省,；reg_area_id-注册市,；reg_district_id-注册区,；reg_detail- 注册详细地址,；legal_name- 法人姓名,；legal_cert_type-法人证件类型,；legal_cert_no-法人证件号码,；legal_cert_validity_type-法人证件有效期类型,；legal_cert_begin_date-法人证件有效期开始日期,；legal_cert_end_date-法人证件有效期截止日期,；busi_type-经营类型,；ent_type-公司类型,；mcc-所属行业 |
| `request.data.head_huifu_id` | 上级汇付Id | `String` | `18` | `C` | 如果head_office_flag=0，则字段必填，如果head_office_flag=1，上级汇付Id不可传；如果headOfficeFlag=0，useHeadInfoFlag=Y,且head_huifu_id不为空则基本信息部分复用上级的基本信息。；示例值：[官网示例已脱敏] |
| `request.data.mer_url` | 商户主页URL | `String` | `256` | `N` | 商户主页URL ；示例值：https://paas.huifu.com/ |
| `request.data.mer_icp` | 商户ICP备案编号 | `String` | `50` | `C` | 商户ICP备案编号或网站许可证号；示例值：沪ICP备06046402号-28 ；类型为PC网站时，且为企业商户，且开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），必填 |
| `request.data.store_header_pic` | 店铺门头照 | `String` | `64` | `C` | scene_type字段含有线下场景时必填；通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F22；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530；微信/支付宝实名认证个人商户，门头照也使用此字段；门店场所：提交门店门口照片，要求招牌清晰可见; ；小微商户流动经营/便民服务：提交经营/服务现场照片 |
| `request.data.store_indoor_pic` | 店铺内景/工作区域照 | `String` | `64` | `C` | scene_type字段含有线下场景时必填；通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F24；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530；微信/支付宝实名认证个人商户，内景照也使用此字段；门店场所：提交店内环境照片 ；小微商户流动经营/便民服务：可提交另一张经营/服务现场照片 |
| `request.data.store_cashier_desk_pic` | 店铺收银台/公司前台照 | `String` | `64` | `C` | scene_type字段含有线下场景时必填；通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；文件类型：F105；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530；微信/支付宝实名认证个人商户，内景照也使用此字段 |
| `request.data.ext_mer_id` | 外部商户号 | `String` | `64` | `N` | 支持关联外部商户系统中的商户号；示例值：HF100001 |
| `request.data.remarks` | 备注 | `String` | `300` | `N` | 备注内容；示例值：华东分公司 |
| `request.data.async_return_url` | 异步请求地址 | `String` | `120` | `N` | 审核结果消息接收地址，为空时不推送消息；示例值：http://service.example.com/to/path |
| `request.data.elec_acct_config` | 斗拱e账户功能配置 | `String` | `—` | `N` | jsonObject字符串；用于下级商户配置银行电子账户功能 |
| `request.data.elec_acct_config.switch_state` | 电子账户开关 | `String` | `1` | `Y` | 电子账户开通总开关；0:关闭 1:开通；示例值：1 |
| `request.data.elec_acct_config.acct_type` | 账户类型 | `String` | `2` | `Y` | 01：中信e管家；示例值：01 |
| `request.data.elec_acct_config.cash_fee_party` | 电子账户取现手续费承担方 | `String` | `1` | `Y` | 1:总部 2:其他；示例值：1 |
| `request.data.elec_acct_config.scene` | 场景类型 | `String` | `3` | `Y` | 必填；与角色类型关联，[中信定义的资金类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；示例值：001 |
| `request.data.elec_acct_config.role_type` | 角色类型 | `String` | `6` | `Y` | 必填；与场景关联，[中信定义的角色类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；示例值：001001 |
| `request.data.elec_acct_config.elec_acct_sign_seq_id` | 中信签约短信流水号 | `String` | `64` | `N` | 示例值：EMSSBPG[官网示例已脱敏] |
| `request.data.elec_acct_config.sign_success_flag` | 签约成功标志 | `String` | `1` | `Y` | Y：成功 |
| `request.data.elec_acct_config.elec_card_list[]` | 银行卡信息 | `String` | `—` | `N` | jsonArray字符串，如果开通斗拱E账户但不提供绑卡信息将无法取现，后续绑卡请调用[电子账户绑卡接口](https://paas.huifu.com/open/doc/api/#/yuer/api_acct_dzzhbk) |
| `request.data.elec_acct_config.elec_card_list[].prov_id` | 银行所在省 | `String` | `6` | `N` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310000 |
| `request.data.elec_acct_config.elec_card_list[].area_id` | 银行所在市 | `String` | `6` | `N` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310100 |
| `request.data.elec_acct_config.elec_card_list[].bank_code` | 银行编码 | `String` | `8` | `Y` | [参考银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；示例值：01020000 |
| `request.data.elec_acct_config.elec_card_list[].branch_code` | 支行联行号 | `String` | `12` | `Y` | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `request.data.elec_acct_config.elec_card_list[].branch_name` | 支行名称 | `String` | `64` | `Y` | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `request.data.elec_acct_config.elec_card_list[].card_name` | 银行账户名 | `String` | `128` | `Y` | 银行卡对应的户名；示例值：上海汇付支付有限公司 |
| `request.data.elec_acct_config.elec_card_list[].card_no` | 银行卡号 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.elec_acct_config.elec_card_list[].card_type` | 银行账户类型 | `String` | `1` | `Y` | 0:对公， 1:对私法人，仅限个体工商户；示例值：0 |
| `request.data.elec_acct_config.elec_card_list[].default_cash_flag` | 默认卡标识 | `String` | `1` | `N` | 0：非默认卡 1：默认卡(不填，默认为0)；示例值：0 |
| `request.data.share_holder_info_list[]` | 股东信息 | `String` | `—` | `N` | jsonArray字符串；全域资金业务新网银行必填 |
| `request.data.share_holder_info_list[].name` | 股东姓名 | `String` | `32` | `Y` | 示例值：张三 |
| `request.data.share_holder_info_list[].cert_type` | 股东证件类型 | `String` | `2` | `Y` | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》；支持00~11，以及12:营业执照；示例值：12 |
| `request.data.share_holder_info_list[].cert_no` | 股东证件号码 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.share_holder_info_list[].cert_validity_type` | 股东证件有效期类型 | `String` | `1` | `Y` | 1:长期有效 0:非长期有效；示例值：1 |
| `request.data.share_holder_info_list[].cert_begin_date` | 股东证件有效期起始日 | `String` | `8` | `Y` | 格式yyyyMMdd；示例值：20201223 |
| `request.data.share_holder_info_list[].cert_end_date` | 股东证件有效期到期日 | `String` | `8` | `N` | 格式yyyyMMdd; 非长期有效时必填；示例值：20301223 |
| `request.data.share_holder_info_list[].mobile_no` | 股东手机号 | `String` | `11` | `N` | 需为11位数字 ；示例值：[官网示例已脱敏] |
| `request.data.extended_material_list[]` | 扩展资料包 | `String` | `—` | `N` | jsonArray字符串；根据要求上传补充相关材料 |
| `request.data.extended_material_list[].file_id` | 文件id | `String` | `64` | `Y` | 请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.extended_material_list[].file_type` | 文件类型 | `String` | `64` | `Y` | [参见文件类型说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；示例值：F01 |
| `request.data.activated_products` | 产品大类 | `String` | `32` | `N` | 01：一体化收款产品，02：账户与资金产品，03：业财数通产品；不传为空 示例值：01,02,03 |
| `request.data.material_card_info` | 对公卡信息 | `String` | `—` | `Y` | jsonObject字符串；商户对公账户信息配置，当非个体工商户的企业商户，card_info选择对私结算（含法人、非法人）时，需补充对公同名账户信息，包括对公账户证明图片信息，通过图片上传接口上传材料；文件类型：F08 |
| `request.data.material_card_info.card_name` | 银行账户名称 | `String` | `128` | `N` | 账户名必须与营业执照名称一致 |
| `request.data.material_card_info.card_no` | 对公银行账号 | `String` | `32` | `Y` | 对公银行账号 |
| `request.data.material_card_info.prov_id` | 银行所在省 | `String` | `6` | `N` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310000 |
| `request.data.material_card_info.area_id` | 银行所在市 | `String` | `6` | `Y` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310100 |
| `request.data.material_card_info.branch_code` | 支行联行号 | `String` | `8` | `Y` | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `request.data.head_type` | 总部客群 | `String` | `1` | `C` | 当head_office_flag为1时，必填；枚举值包含，0 集团客户，1大型商业综合体，2品牌连锁客户 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务返回码 | `String` | `8` | `Y` | 参考[业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码)；示例值：00000000 |
| `response.data.resp_desc` | 业务返回描述 | `String` | `512` | `Y` | 业务返回描述；示例值：处理成功 |
| `response.data.huifu_id` | 商户号 | `String` | `18` | `N` | 汇付商户号，示例值：[官网示例已脱敏] |
| `response.data.apply_no` | 申请单号 | `String` | `18` | `N` | 商户开户业务申请单号，示例值：[官网示例已脱敏] |
| `response.data.token_no` | 银行卡序列号 | `String` | `20` | `N` | 取现时使用 ；示例值：10004053462 |

### 审核异步信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.audit.resp_code` | 网关返回码 | `String` | `5` | `Y` | [网关返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%e7%bd%91%e5%85%b3%e8%bf%94%e5%9b%9e%e7%a0%81)；示例值：10000 |
| `async.audit.resp_desc` | 网关返回描述 | `String` | `512` | `Y` | 网关返回描述；示例值：成功调用 |
| `async.audit.sign` | 签名 | `String` | `512` | `Y` | 签名，对报文整体签名；示例值：o8bYN+DO5AaYl41idy04tZknaRnNORy8TgIztI6d8e3EtrSU9DbSjlN99DAgopNex6pEFFbQimxGxN8n9rADO4Xe7IZ9McPy2I9zJ0hccGpK9YBa2cqSMMzLCmxFiVqlz04RxrduBOHrfIsr4HM9Z3g6r8yOAL/FS1LqH7M3bCo= |
| `async.audit.data` | 业务返回参数 | `String` | `—` | `N` | 业务返回参数 jsonObject格式 |

### 审核异步 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.audit.data.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | 参考[业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) ；示例值：00000000 |
| `async.audit.data.sub_resp_desc` | 业务返回描述 | `String` | `512` | `Y` | 示例值：处理成功 |
| `async.audit.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原请求流水号；示例值：[官网示例已脱敏] |
| `async.audit.data.req_date` | 请求日期 | `String` | `8` | `Y` | 原请求日期；示例值：20220125 |
| `async.audit.data.audit_status` | 审核结果 | `String` | `1` | `Y` | Y：审核通过，N：审核拒绝，F：失败，示例值：Y |
| `async.audit.data.audit_desc` | 审核描述 | `String` | `512` | `N` | 示例值：审核通过 |
| `async.audit.data.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `async.audit.data.huifu_id` | 商户号 | `String` | `18` | `N` | 汇付商户号，状态为审核中时返回；示例值：[官网示例已脱敏] |
| `async.audit.data.apply_no` | 申请单号 | `String` | `18` | `N` | 商户开户业务申请单号，状态为审核中时返回；示例值：[官网示例已脱敏] |
| `async.audit.data.token_no` | 银行卡序列号 | `String` | `20` | `N` | 取现时使用；示例值：10004053462 |
| `async.audit.data.notify_type` | 通知类型 | `String` | `1` | `N` | Z：电子账户；示例值：Z |
| `async.audit.data.elec_acct_result` | 斗拱e账户开通结果 | `String` | `—` | `N` | jsonObject格式；notify_type=Z时返回 |
| `async.audit.data.elec_acct_result.acct_type` | 账户类型 | `String` | `2` | `Y` | 01：中信e管家；示例值：01 |
| `async.audit.data.elec_acct_result.bank_status` | 电子账户开通状态 | `String` | `1` | `Y` | S：成功 F：失败；示例值：S |
| `async.audit.data.elec_acct_result.bank_message` | 银行信息 | `String` | `512` | `N` | 银行信息 |
| `async.audit.data.elec_acct_result.sign_agreement_id` | 签约协议号 | `String` | `32` | `N` | 商户签约中信E管家协议编号； 签约成功才返回示例值：[官网示例已脱敏] |

## 个人商户进件

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_grshjbxxrz_kyc.md>
- SHA-256：`09862a3923b114abcf7dbc9e7545798481abc37f88b6eb64911ce7d53f9f5437`
- 说明：下表保留官方字段类型、长度、必填标记和字段说明；数组父路径以 `[]` 标记。

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
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号，同一商户号当天唯一；示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd，以北京时间为准；示例值：20220125 |
| `request.data.upper_huifu_id` | 直属渠道号 | `String` | `18` | `C` | 该商户进件完成后归属的渠道商huifu_id；sys_id主体为渠道商时填写；sys_id主体为总部商户时选填；示例值：[官网示例已脱敏] |
| `request.data.reg_name` | 商户名 | `String` | `32` | `Y` | 商户名称，个人类商户为负责人姓名；示例值：张三 |
| `request.data.short_name` | 商户简称 | `String` | `32` | `N` | 最少4个字符；会展示在消费账单上；示例值：张三 |
| `request.data.mcc` | 所属行业 | `String` | `7` | `Y` | 参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；示例值：5311 |
| `request.data.scene_type` | 场景类型 | `String` | `8` | `Y` | ONLINE：线上场景，OFFLINE：线下场景，ALL：线上线下；示例值：ALL |
| `request.data.prov_id` | 经营省 | `String` | `6` | `N` | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)，示例值：310000 |
| `request.data.area_id` | 经营市 | `String` | `6` | `N` | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)，示例值：310100 |
| `request.data.district_id` | 经营区 | `String` | `6` | `Y` | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)，示例值：310101 |
| `request.data.detail_addr` | 经营详细地址 | `String` | `256` | `C` | scene_type字段含有线下场景时必填；示例值：上海市徐汇区XX路XX号 |
| `request.data.legal_cert_no` | 负责人证件号码 | `String` | `32` | `Y` | 只支持身份证号；示例值：[官网示例已脱敏]；年龄不允许小于18岁且不能大于80岁 |
| `request.data.legal_cert_begin_date` | 负责人证件有效期开始日期 | `String` | `8` | `Y` | 日期格式yyyyMMdd，示例值：20110112。开始日期需小于当前日期 |
| `request.data.legal_cert_validity_type` | 负责人证件有效期类型 | `String` | `1` | `N` | 1：长期有效；0：非长期有效；示例值：1 |
| `request.data.legal_cert_end_date` | 负责人证件有效期截止日期 | `String` | `8` | `Y` | 日期格式yyyyMMdd；示例值：20410112。结束日期大于当前日期 |
| `request.data.legal_addr` | 负责人身份证地址 | `String` | `256` | `Y` | 示例值：上海市徐汇区XX路XX号 |
| `request.data.legal_cert_back_pic` | 负责人身份证国徽面 | `String` | `64` | `Y` | 涉及文件类型：F41；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.legal_cert_front_pic` | 负责人身份证人像面 | `String` | `64` | `Y` | 涉及文件类型：F40；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.occupation` | 负责人职业 | `String` | `2` | `N` | 1A：各类专业,技术人员；1B：国家机关,党群组织,企事业单位的负责人；1C：办事人员和有关人员；1D：商业工作人员，默认；1E：服务性工作人员；1F：农林牧渔劳动者；1G：生产工作,运输工作和部分体力劳动者；1H：不便分类的其他劳动者；示例值：1G |
| `request.data.contact_mobile_no` | 负责人手机号 | `String` | `11` | `Y` | 负责人手机号，需为11位数字；示例值：[官网示例已脱敏] |
| `request.data.contact_email` | 负责人电子邮箱 | `String` | `32` | `Y` | 负责人电子邮箱，需要带@，遵循邮箱格式；示例值：huifu@xxx.com |
| `request.data.card_info` | 结算卡信息配置 | `String` | `—` | `Y` | 商户结算账户信息配置，jsonObject字符串；开通中信E管家结算的银行卡配置在【elec_acct_config】中 |
| `request.data.card_info.card_name` | 卡户名 | `String` | `128` | `Y` | 结算账户名，结算银行卡对应的户名；示例值：张三 |
| `request.data.card_info.card_no` | 结算账号 | `String` | `32` | `Y` | 结算银行卡号，不支持贷记卡。为避免资金结算失败，请正确填写； 示例值：[官网示例已脱敏] |
| `request.data.card_info.prov_id` | 银行所在省 | `String` | `6` | `N` | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000 |
| `request.data.card_info.area_id` | 银行所在市 | `String` | `6` | `Y` | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310100 |
| `request.data.card_info.bank_code` | 银行编号 | `String` | `8` | `N` | 参考： [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm) ；示例值：01020000 |
| `request.data.card_info.cert_type` | 持卡人证件类型 | `String` | `2` | `Y` | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》 示例值：00 |
| `request.data.card_info.cert_no` | 持卡人证件号码 | `String` | `32` | `Y` | 如持卡人证件类型为00：身份证，则填写身份证号码；示例值：[官网示例已脱敏]。**系统会做格式校验**；年龄不允许小于18岁且不能大于80岁 |
| `request.data.card_info.cert_validity_type` | 持卡人证件有效期类型 | `String` | `1` | `Y` | 1:长期有效，0:非长期有效；示例值：0 |
| `request.data.card_info.cert_begin_date` | 持卡人证件有效期开始 | `String` | `8` | `Y` | 日期格式：yyyyMMdd，以北京时间为准；示例值：20220125 |
| `request.data.card_info.cert_end_date` | 持卡人证件有效期截止日期 | `String` | `8` | `C` | 格式yyyyMMdd，以北京时间为准。示例值：20220125；当cert_validity_type=0时必填 ；当cert_validity_type=1时为空 |
| `request.data.card_info.mp` | 结算人手机号 | `String` | `11` | `N` | 11位数字；示例值：[官网示例已脱敏] |
| `request.data.card_info.is_settle_default` | 默认结算卡标志 | `String` | `1` | `N` | 是否为默认结算卡标志；Y:是 N:否(为空默认)；示例值：Y |
| `request.data.settle_card_front_pic` | 银行卡卡号面 | `String` | `64` | `Y` | 涉及文件类型：F13；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.settle_config` | 结算规则配置 | `String` | `—` | `N` | 商户结算规则配置，jsonObject格式 |
| `request.data.settle_config.settle_cycle` | 结算周期 | `String` | `2` | `Y` | 结算周期；示例值：T1； D1：下个自然日到账 ； T1：下个工作日到账； TS:笔笔结算 |
| `request.data.settle_config.min_amt` | 起结金额 | `String` | `14` | `N` | settle_cycle为TS时不填。账户余额大于等于起结金额才会发起结算。单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。不设置起结金额请填写0.00；示例值：1000.00 |
| `request.data.settle_config.remained_amt` | 留存金额 | `String` | `14` | `N` | settle_cycle为TS时不填。该部分资金不会结算。单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。不设置留存金额请填写0.00；示例值：1000.00 |
| `request.data.settle_config.settle_abstract` | 结算摘要 | `String` | `128` | `N` | 可自定义结算打款备注，不填默认为空；支持配置格式化摘要内容，参见[结算配置示例说明](https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm)；示例值：汇付商城业务 |
| `request.data.settle_config.out_settle_flag` | 手续费外扣标记 | `String` | `1` | `N` | 手续费外扣标记，外扣时从out_settle_huifuid账户扣手续费，内扣时从结算金额中扣手续费；1：外扣；2：内扣；不填默认内扣；示例值：2 |
| `request.data.settle_config.out_settle_huifuid` | 结算手续费外扣商户号 | `String` | `18` | `C` | 结算手续费外扣商户号，填写承担手续费的汇付商户号；当out_settle_flag=1时必填，否则非必填；示例值：[官网示例已脱敏] |
| `request.data.settle_config.out_settle_acct_type` | 结算手续费外扣账户类型 | `String` | `2` | `N` | 结算手续费外扣账户类型，不填默认01：基本户；01：基本户，02：现金户，05：充值户 ，09：营销户；示例值：01 |
| `request.data.settle_config.settle_pattern` | 结算方式 | `String` | `—` | `N` | settle_cycle为TS时不填。P0：批次结算 ，P1：定时结算(建议选P0和P2)，P2:批次定时结算，E1:中信E管家 示例值：P1 批次结算指按照指定结算批次号进行资金结算，自定义时间结算是指按照商户指定到账时间进行资金结算。两种结算方式需二选一，不填默认P0：批次结算 |
| `request.data.settle_config.settle_batch_no` | 结算批次号 | `String` | `16` | `C` | settle_cycle为TS时不填。结算方式为P0：批次结算时必填，即将按指定结算批次号进行资金结算；示例值：100；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| `request.data.settle_config.is_priority_receipt` | 是否优先到账 | `String` | `1` | `N` | 当settle_pattern=P0时选填，不填默认为N，该值在结算那批次号[0-500]间生效； Y：是，N：否，示例值：Y |
| `request.data.settle_config.settle_time` | 自定义结算处理时间 | `String` | `6` | `C` | settle_cycle为TS时不填。当settle_pattern=P1/P2自定义时间结算时必填；注意：00:00到00:30不能指定；到账时间，格式：HHmmss；示例值：103000 |
| `request.data.settle_config.fixed_ratio` | 节假日结算手续费率 | `String` | `6` | `C` | settle_cycle为D1、TS时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；示例值：0.05 |
| `request.data.settle_config.constant_amt` | 节假日结算手续费固定金额 | `String` | `15` | `C` | settle_cycle为D1、TS时必填。单位元，需保留小数点后两位。不收费请填写0.00；settle_cycle结算周期为D1时，遇节假日按此费率结算；示例值：1.00 |
| `request.data.settle_config.workday_fixed_ratio` | 工作日结算手续费率 | `String` | `6` | `N` | settle_cycle为TS时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；示例值：0.05 |
| `request.data.settle_config.workday_constant_amt` | 工作日结算手续费固定金额 | `String` | `15` | `N` | settle_cycle为TS时必填。单位元，需保留小数点后两位。不填默认为0.00；示例值：1.00 |
| `request.data.cash_config[]` | 取现信息配置 | `String` | `—` | `N` | 商户取现信息配置，jsonArray字符串 |
| `request.data.cash_config[].cash_type` | 取现类型 | `String` | `2` | `Y` | T1：下个工作日到账；D1：下个自然日到账 ；D0：当日到账，当日交易资金当天可取现到账；DM：当日到账，到账资金不包括当天的交易资金；示例值：T1 |
| `request.data.cash_config[].fix_amt` | 提现手续费（固定/元） | `String` | `6` | `C` | fix_amt与fee_rate至少填写一项， 需保留小数点后两位，不收费请填写0.00；示例值：1.00；注：当cash_type=D1时为节假日取现手续费 |
| `request.data.cash_config[].fee_rate` | 提现手续费率（%） | `String` | `6` | `C` | fix_amt与fee_rate至少填写一项，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；示例值：0.05；注：1、如果fix_amt与fee_rate都填写了则手续费=fix_amt+支付金额\*fee_rate；2、当cash_type=D1时为节假日取现手续费 |
| `request.data.cash_config[].weekday_fix_amt` | D1工作日取现手续费固定金额 | `String` | `6` | `C` | 单位元，需保留小数点后两位。不收费请填写0.00；示例值：1.00；cash_type=T1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算，若未配置则默认按照节假日手续费计算 |
| `request.data.cash_config[].weekday_fee_rate` | D1工作日取现手续费率 | `String` | `6` | `C` | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；示例值：0.05；cash_type=T1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算 ，若未配置则默认按照节假日手续费计算 |
| `request.data.cash_config[].out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）； 示例值：2 |
| `request.data.cash_config[].out_fee_huifu_id` | 手续费承担方 | `String` | `18` | `C` | 手续费外扣时必需指定手续费承担方ID； 示例值：[官网示例已脱敏] |
| `request.data.cash_config[].out_fee_acct_type` | 交易手续费外扣的账户类型 | `String` | `2` | `N` | 01-基本户，02-现金户，05-充值户；不填默认01； 示例值：01 |
| `request.data.cash_config[].is_priority_receipt` | 是否优先到账 | `String` | `1` | `N` | Y：是 ，N：否。不填，默认值为否。仅在取现类型配置为D1 和 T1 时生效。示例值：Y |
| `request.data.sms_send_flag` | 商户通知标识 | `String` | `1` | `N` | 入驻成功后通知商户联系人，M：发送短信通知；E：发送邮件通知；A：短信、邮件都通知；为空：不作通知。 示例值：M |
| `request.data.login_name` | 管理员账号 | `String` | `32` | `N` | 管理员账号，用于商户平台登录。全局唯一，支持英文、数字、下划线，区分大小写；示例值：huifu001 |
| `request.data.mer_url` | 商户主页URL | `String` | `256` | `N` | 示例值：https://paas.huifu.com/ |
| `request.data.mer_icp` | 商户ICP备案编号 | `String` | `50` | `C` | 商户ICP备案编号或网站许可证号；示例值：沪ICP备06046402号-28 ；类型为PC网站时，且为企业商户，且开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），必填 |
| `request.data.store_header_pic` | 店铺门头照 | `String` | `64` | `C` | scene_type字段含有线下场景时必填；文件类型：F22；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530；微信/支付宝实名认证个人商户，门头照也使用此字段；门店场所：提交门店门口照片，要求招牌清晰可见; ；小微商户流动经营/便民服务：提交经营/服务现场照片 |
| `request.data.store_indoor_pic` | 店铺内景/工作区域照 | `String` | `64` | `C` | scene_type字段含有线下场景时必填；文件类型：F24；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530；微信/支付宝实名认证个人商户，内景照也使用此字段；门店场所：提交店内环境照片 ；小微商户流动经营/便民服务：可提交另一张经营/服务现场照片 |
| `request.data.store_cashier_desk_pic` | 店铺收银台/公司前台照 | `String` | `64` | `C` | scene_type字段含有线下场景时必填；文件类型：F105；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.ext_mer_id` | 外部商户号 | `String` | `64` | `N` | 支持关联外部商户系统中的商户号；示例值：HF100001 |
| `request.data.remarks` | 备注 | `String` | `300` | `N` | 备注内容；示例值：华东分公司 |
| `request.data.async_return_url` | 异步通知地址 | `String` | `120` | `N` | 审核结果消息接收地址，为空时不推送消息 ；示例值：http://service.example.com/to/path |
| `request.data.head_office_flag` | 商户身份 | `String` | `1` | `N` | 0：下级商户，不传默认普通商户。示例值：0；开通下级商户时，所选的上级商户需要有开通商户权限，需先调用“[开通下级商户权限配置接口](https://paas.huifu.com/open/doc/api/#/shgl/shywkt/api_shjj_shywkt_xjshpz)”；（1）若对应总部的客群类型为0，需要补充F725 （集团盖章说明函）；（2）若对应总部的客群类型为1，需要补充F726 （下级商户入驻大型商业综合体的合作协议）；（3）若对应总部的客群类型为2，加盟性质需要补充F727（加盟协议），直营性质需要补充F727（总部盖章说明函） |
| `request.data.head_huifu_id` | 上级商户汇付ID | `String` | `18` | `C` | 如果head_office_flag=0，则字段必填；示例值：[官网示例已脱敏] |
| `request.data.elec_acct_config` | 斗拱e账户功能配置 | `String` | `—` | `N` | 用于下级商户开通斗拱E账户功能 |
| `request.data.elec_acct_config.switch_state` | 电子账户开关 | `String` | `1` | `Y` | 电子账户开通总开关；0:关闭 1:开通；示例值：1 |
| `request.data.elec_acct_config.acct_type` | 账户类型 | `String` | `2` | `Y` | 01：中信e管家；示例值：01 |
| `request.data.elec_acct_config.cash_fee_party` | 电子账户提现手续费承担方 | `String` | `1` | `Y` | 1:总部 2:其他；示例值：1 |
| `request.data.elec_acct_config.scene` | 场景类型 | `String` | `3` | `Y` | 必填，与角色类型关联，[中信定义的资金类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；示例值：001 |
| `request.data.elec_acct_config.role_type` | 角色类型 | `String` | `6` | `Y` | 角色编号必填；与场景关联，[中信定义的角色类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；示例值：001001 |
| `request.data.elec_acct_config.elec_card_list[]` | 银行卡信息 | `Object` | `—` | `N` | jsonArray字符串；如果开通斗拱E账户但不提供绑卡信息将无法取现，后续绑卡请调用[电子账户绑卡接口](https://paas.huifu.com/open/doc/api/#/yuer/api_acct_dzzhbk) |
| `request.data.elec_acct_config.elec_card_list[].prov_id` | 银行所在省 | `String` | `6` | `N` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310000 |
| `request.data.elec_acct_config.elec_card_list[].area_id` | 银行所在市 | `String` | `6` | `N` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310100 |
| `request.data.elec_acct_config.elec_card_list[].bank_code` | 银行编码 | `String` | `8` | `Y` | [参考银行编码；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)示例值：01020000 |
| `request.data.elec_acct_config.elec_card_list[].branch_code` | 支行联行号 | `String` | `12` | `Y` | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `request.data.elec_acct_config.elec_card_list[].branch_name` | 支行名称 | `String` | `64` | `Y` | 示例值：中国工商银行上海市中山北路支行 |
| `request.data.elec_acct_config.elec_card_list[].card_name` | 结算账户名 | `String` | `128` | `Y` | 银行卡对应的户名；示例值：上海汇付支付有限公司 |
| `request.data.elec_acct_config.elec_card_list[].card_no` | 银行卡号 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.elec_acct_config.elec_card_list[].card_type` | 卡类型 | `String` | `1` | `Y` | 0:对公 1:对私法人；示例值：1 |
| `request.data.elec_acct_config.elec_card_list[].default_cash_flag` | 默认卡标识 | `String` | `1` | `N` | 0：非默认卡 1：默认卡(不填，默认为0)；示例值：1 |
| `request.data.elec_acct_config.elec_card_list[].mp` | 银行绑定手机号 | `String` | `11` | `C` | 为空取联系人手机号，注意如果联系人非持卡人银行会报错；示例值:[官网示例已脱敏] |
| `request.data.elec_acct_config.elec_card_list[].auth_version` | 用户授权协议版本号 | `String` | `64` | `C` | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的电子协议版本号，通过该版本号能够确定协议的具体内容 |
| `request.data.elec_acct_config.elec_card_list[].auth_no` | 用户授权协议号 | `String` | `64` | `C` | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的授权交易流水号，通过该流水号应能确定电子协议版本号、签约人、签约时间 |
| `request.data.elec_acct_config.elec_acct_sign_seq_id` | 中信签约短信流水号 | `String` | `64` | `N` | 示例值：EMSSBPG[官网示例已脱敏] |
| `request.data.elec_acct_config.sign_success_flag` | 签约成功标志 | `String` | `1` | `Y` | Y：成功 |
| `request.data.extended_material_list[]` | 扩展资料包 | `String` | `—` | `N` | jsonArray字符串；根据要求上传补充相关材料 |
| `request.data.extended_material_list[].file_id` | 文件id | `String` | `64` | `Y` | 请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.extended_material_list[].file_type` | 文件类型 | `String` | `64` | `Y` | [参见文件类型说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；示例值：F01 |
| `request.data.activated_products` | 产品大类 | `String` | `—` | `N` | 01：一体化收款产品，02：账户与资金产品，03：业财数通产品；不传为空 示例值：01,02,03 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务返回码 | `String` | `8` | `Y` | 参考[业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) ；示例值：00000000 |
| `response.data.resp_desc` | 业务返回描述 | `String` | `512` | `Y` | 业务返回描述 ；示例值：处理成功 |
| `response.data.huifu_id` | 商户号 | `String` | `18` | `N` | 汇付商户号，状态为审核中时返回；示例值：[官网示例已脱敏] |
| `response.data.apply_no` | 申请单号 | `String` | `18` | `N` | 商户开户业务申请单号，状态为审核中时返回；示例值：[官网示例已脱敏] |
| `response.data.token_no` | 取现卡序列号 | `String` | `20` | `N` | 取现时使用 ；示例值：10004053462 |

### 审核异步信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.audit.resp_code` | 网关返回码 | `String` | `5` | `Y` | [网关返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#网关返回码) ；示例值：10000 |
| `async.audit.resp_desc` | 网关返回描述 | `String` | `512` | `Y` | 网关返回描述 ；示例值：成功调用 |
| `async.audit.sign` | 签名 | `String` | `512` | `Y` | 签名，对报文整体签名； 示例值：o8bYN+……/FS1LqH7M3bCo= |
| `async.audit.data` | 交易响应内容体 | `String` | `—` | `N` | 业务返回参数， jsonObject格式 |

### 审核异步 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.audit.data.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | 参考[业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码)；示例值：00000000 |
| `async.audit.data.sub_resp_desc` | 业务返回描述 | `String` | `512` | `Y` | 业务返回描述；示例值：处理成功 |
| `async.audit.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原请求流水号；示例值：[官网示例已脱敏] |
| `async.audit.data.req_date` | 请求日期 | `String` | `8` | `Y` | 原请求日期；格式：yyyyMMdd 示例值：20220125 |
| `async.audit.data.audit_status` | 审核结果 | `String` | `1` | `Y` | 审核结果；Y：审核通过；N：审核拒绝；F：失败；示例值：Y |
| `async.audit.data.audit_desc` | 审核描述 | `String` | `512` | `N` | 审核描述，审核人员编辑的审核描述；示例值：审核通过 |
| `async.audit.data.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：MCS |
| `async.audit.data.huifu_id` | 商户号 | `String` | `18` | `N` | 汇付商户号，状态为审核中时返回 ；示例值：[官网示例已脱敏] |
| `async.audit.data.apply_no` | 申请单号 | `String` | `18` | `N` | 商户开户业务申请单号，状态为审核中时返回；示例值：[官网示例已脱敏] |
| `async.audit.data.token_no` | 取现卡序列号 | `String` | `20` | `N` | 取现时使用；示例值：10004053462 |
| `async.audit.data.notify_type` | 通知类型 | `String` | `1` | `N` | Z：电子账户；示例值：Z |
| `async.audit.data.elec_acct_result` | 斗拱e账户开通结果 | `String` | `—` | `N` | jsonObject格式；notify_type=Z时返回 |
| `async.audit.data.elec_acct_result.acct_type` | 账户类型 | `String` | `2` | `Y` | 01：中信e管家；示例值：01 |
| `async.audit.data.elec_acct_result.bank_status` | 电子账户开通状态 | `String` | `1` | `Y` | S：成功 F：失败；示例值：S |
| `async.audit.data.elec_acct_result.bank_message` | 银行信息 | `String` | `512` | `N` | 银行信息 |
| `async.audit.data.elec_acct_result.sign_agreement_id` | 签约协议号 | `String` | `32` | `N` | 商户签约中信E管家协议编号； 签约成功才返回示例值：[官网示例已脱敏] |

## 商户业务开通

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_kyc.md>
- SHA-256：`42d692619bd409ae11b95b43a0badec25794316e8fa0fc6de3c02c5fa2ae4ddd`
- 说明：下表保留官方字段类型、长度、必填标记和字段说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商或商户的huifu_id；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为总部商户时，此字段填写商户huifu_id |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/docs/start/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/docs/start/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号（业务申请编号），同一商户号当天唯一，示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 请求日期：yyyyMMdd，以北京时间为准；示例值：20220904 |
| `request.data.huifu_id` | 汇付客户Id | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] |
| `request.data.upper_huifu_id` | 直属渠道号 | `String` | `18` | `C` | 该商户进件完成后归属的渠道商huifu_id；sys_id主体为渠道商时填写；sys_id主体为总部商户时选填；示例值：[官网示例已脱敏] |
| `request.data.short_name` | 微信支付宝商户简称 | `String` | `64` | `N` | 企业商户必填，需与商户注册名称全称相关；用于微信、支付宝入驻时上传；注意：微信只支持20个字节，10个汉字；示例值：上海汇付 |
| `request.data.sign_user_info` | 签约人 | `String` | `—` | `C` | jsonObject字符串；agreement_info中选择电子签约时必填；个人商户填本人信息。 |
| `request.data.sign_user_info.type` | 签约人类型 | `String` | `7` | `Y` | LEGAL-法人，对公结算或对私法人结算时可选法人签约；CONTACT-联系人，对公结算可选联系人（经办人）签约；OTHER-其他，对私非法人结算选“其他”，必须是结算人；示例值：LEGAL |
| `request.data.sign_user_info.name` | 姓名 | `String` | `32` | `C` | 签约人类型=其他，必填；示例值：张三 |
| `request.data.sign_user_info.cert_no` | 身份证 | `String` | `32` | `C` | 签约人类型=联系人/其他，必填 ；注意：**签约人会做姓名+身份证+手机号验证，请正确填写**；示例值：[官网示例已脱敏] |
| `request.data.sign_user_info.mobile_no` | 手机号 | `String` | `11` | `C` | 签约人类型=法人/其他 ，必填；注意：**签约人会做姓名+身份证+手机号验证，请正确填写**；示例值：[官网示例已脱敏] |
| `request.data.sign_user_info.email` | 邮箱 | `String` | `32` | `N` | 示例值：example@email.com |
| `request.data.online_flag` | 是否开通网银 | `String` | `1` | `N` | Y:是 N:否 ；示例值：Y |
| `request.data.quick_flag` | 是否开通快捷 | `String` | `1` | `N` | Y:是 N:否 ；示例值：Y |
| `request.data.withhold_flag` | 是否开通代扣 | `String` | `1` | `N` | Y:是 N:否 ；示例值：Y |
| `request.data.mer_bus_type` | 商户业务类型 | `String` | `2` | `N` | 快捷，网银，手机WAP，银联统一在线收银台开通时（线上费率配置对象不为空）必填；取值参见[商户业务类型](http://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E5%95%86%E6%88%B7%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B)（官网原始地址为非 HTTPS，不得静默改写）；示例值：01 |
| `request.data.out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）,示例值：1；该公共参数会影响余额支付配置，补贴支付配置，线上手续费承担方配置，支付宝配置，微信配置信息，抖音配置信息，银行卡业务配置，银联二维码配置，花呗分期配置，全域资金管理 |
| `request.data.out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填，示例值：[官网示例已脱敏]；该公共参数会影响余额支付配置，补贴支付配置，线上手续费承担方配置，支付宝配置，微信配置信息，抖音配置信息，银行卡业务配置，银联二维码配置，花呗分期配置，全域资金管理 |
| `request.data.out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01；该公共参数会影响余额支付配置，补贴支付配置，线上手续费承担方配置，支付宝信息配置，微信渠道配置信息，抖音配置信息，银行卡业务配置，银联二维码配置，花呗分期配置，全域资金管理 |
| `request.data.ali_conf_list[]` | 支付宝配置对象 | `String` | `—` | `N` | jsonArray字符串 |
| `request.data.ali_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 1.线下扫码，2.线上扫码，3.非盈利费率（需活动报名）；示例值：1；如果一次请求配置了多个场景，以第一个类型为默认场景 |
| `request.data.ali_conf_list[].pay_channel_id` | 子渠道号 | `String` | `32` | `N` | 为空入驻到渠道商默认配置的支付宝渠道号下；示例值：JP00001 |
| `request.data.ali_conf_list[].fee_rate` | 手续费（%） | `String` | `6` | `Y` | 数字格式，大于等于0，保留2位小数；示例值：0.38 |
| `request.data.ali_conf_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `6` | `N` | 金额保留2位小数；大于0。需要渠道商开通此功能。示例值：0.38 |
| `request.data.ali_conf_list[].is_check_real_name` | 是否需要实名认证 | `String` | `1` | `N` | Y-是，业务功能开通成功后使用法人信息发起实名认证申请；N-否；默认为N；示例值：Y |
| `request.data.ali_conf_list[].al_real_name_info` | 实名认证信息 | `String` | `—` | `C` | is_check_real_name=Y时需要填写；jsonObject字符串 ；若请求支付宝入驻成功，但实名申请失败需要调用单独的实名接口重新发起实名。 |
| `request.data.ali_conf_list[].al_real_name_info.finance_institution_flag` | 是否金融机构 | `String` | `5` | `N` | 选填，请根据申请主体的实际情况填写；1、若商户主体是金融机构，则填写：true。；2、若商户主体不是金融机构，则填写：false。；若未传入将默认填写：false；3，支付宝实名金融机构需要提供 F236：金融机构许可证图片一 ；F237：金融机构许可证图片二；F238：金融机构许可证图片三；F239：金融机构许可证图片四；F240：金融机构许可证图片五；补充资料填写在extended_material_list对象中；示例值：true |
| `request.data.ali_conf_list[].al_real_name_info.finance_type` | 金融机构类型 | `String` | `128` | `N` | 当主体是金融机构时，必填；金融机构类型需与营业执照/登记证书上一致；BANK_AGENT：银行业, 适用于商业银行、政策性银行、农村合作银行、村镇银行、开发性金融机构等；PAYMENT_AGENT：支付机构, 适用于非银行类支付机构；INSURANCE：保险业, 适用于保险、保险中介、保险代理、保险经纪等保险类业务；TRADE_AND_SETTLE：交易及结算类金融机构, 适用于交易所、登记结算类机构、银行卡清算机构、资金清算中心等；OTHER：其他金融机构, 适用于财务公司、信托公司、金融资产管理公司、金融租赁公司、汽车金融公司、贷款公司、货币经纪公司、消费金融公司、证券业、金融控股公司、股票、期货、货币兑换、小额贷款公司、金融资产管理、担保公司、商业保理公司、典当行、融资租赁公司、财经咨询等其他金融业务；示例值：BANK_AGENT |
| `request.data.ali_conf_list[].al_real_name_info.cert_type` | 证书类型 | `String` | `64` | `N` | 企业商户必填；枚举：；统一社会信用代码证书(CERTIFICATE_TYPE_2389)；慈善组织公开募捐资格证书(CERTIFICATE_TYPE_2397)；社会团体法人登记证书(CERTIFICATE_TYPE_2394)；民办非企业单位登记证书(CERTIFICATE_TYPE_2395)；基金会法人登记证书(CERTIFICATE_TYPE_2396)；农民专业合作社法人营业执照(CERTIFICATE_TYPE_2398)；宗教活动场所登记证(CERTIFICATE_TYPE_2399)；其他证书/批文/证明(CERTIFICATE_TYPE_2400)；示例值：CERTIFICATE_TYPE_2389；政府机关/事业单位/其他组织 对应需要补充单位证明函照片 文件类型F46；补充资料填写在extended_material_list对象中；示例值：CERTIFICATE_TYPE_2395 |
| `request.data.ali_conf_list[].al_real_name_info.micro_biz_type` | 小微经营类型 | `String` | `32` | `N` | 小微经营类型 必填字段；门店场所：MICRO_TYPE_STORE；流动经营/便民服务：MICRO_TYPE_MOBILE；线上商品/服务交易：MICRO_TYPE_ONLINE；个人商户需要填写；示例值：MICRO_TYPE_STORE；需要提供 F22：店铺门头照图片；F24：店铺内景图片； 补充资料填写在extended_material_list对象中 |
| `request.data.ali_conf_list[].al_real_name_info.special_category_id` | 特殊行业id | `String` | `20` | `N` | 特殊行业必填，参见支付宝商家行业二级类目code；1，支付宝实名特殊行业提供 F150:行业经营许可证资质照片一；F151:行业经营许可证资质照片二；F152:行业经营许可证资质照片三；F153:行业经营许可证资质照片四；F154:行业经营许可证资质照片五；F155:行业经营许可证资质照片六；补充资料填写在extended_material_list对象中；示例值：100 |
| `request.data.ali_conf_list[].al_real_name_info.contact_person_info` | 联系人信息对象 | `String` | `—` | `N` | — |
| `request.data.ali_conf_list[].al_real_name_info.contact_person_info.name` | 联系人姓名 | `String` | `64` | `N` | 为空时取企业商户取联系人姓名，个人商户取入驻时填写的名称；示例值：张三 |
| `request.data.ali_conf_list[].al_real_name_info.contact_person_info.mobile` | 联系人手机号 | `String` | `64` | `N` | 为空时取企业商户取联系人手机号；示例值：[官网示例已脱敏] |
| `request.data.ali_conf_list[].al_real_name_info.contact_person_info.id_card_number` | 联系人身份证号码 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info` | 法人身份信息 | `String` | `—` | `N` | — |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.legal_type` | 证件持有人类型 | `String` | `32` | `N` | 法人：LEGAL，为空时默认选项； 主体类型为企业、个体户、社会组织、小微商户时，必须为经营者/法人。；经办人：SUPER；主体类型为政府机关、事业单位时默认是法人。若因特殊情况，无法提供法人证件时可填经办人类型。；示例值：LEGAL |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.card_type` | 证件类型 | `String` | `32` | `N` | 枚举值：00:身份证 01:护照 13：港澳居民证 14:台湾居民证；为空时取开户时法人信息；个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关、小微商户仅支持身份证类型。；示例值：00 |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.person_name` | 姓名 | `String` | `64` | `N` | 为空时取开户时法人信息；示例值：李四 |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.card_no` | 证件号码 | `String` | `64` | `N` | 为空时取开户时法人信息；示例值：[官网示例已脱敏] |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.effect_time` | 证件生效时间 | `String` | `32` | `N` | 为空时取开户时法人信息；示例值：19990101 |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.expire_time` | 证件过期时间 | `String` | `32` | `N` | 为空时取开户时法人信息；示例值：20001101，长期有效时传“长期” |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.card_front_img` | 证件正面照 | `String` | `128` | `N` | 为空时取开户时法人信息，如果开户时未传该字段必填；上送图片上传返回的jfileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.card_back_img` | 证件反面照 | `String` | `128` | `N` | 为空时取开户时法人信息，如果开户时未传该字段必填；只有身份证类型需要上传反面；上送图片上传返回的jfileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.auth_letter_img` | 授权函照片 | `String` | `128` | `N` | 上送图片上传返回的jfileId；文件类型F224业务办理授权函；当证件持有人类型为经办人时必须上传。其他情况，无需上传。示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.is_benefit_person` | 是否为受益人 | `String` | `1` | `N` | Y-受益人;N-非受益人 默认值：Y；示例值：Y |
| `request.data.ali_conf_list[].mcc` | *商户经营类目* | `String` | `32` | `N` | [支付宝MCC](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_zfbmcc)；示例值：5411 |
| `request.data.ali_zl_conf` | 支付宝直连配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `request.data.ali_zl_conf.apply_type` | 申请类型 | `String` | `32` | `Y` | FACE_TO_FACE：当面付；示例值：FACE_TO_FACE |
| `request.data.ali_zl_conf.contact_name` | 联系人姓名 | `String` | `64` | `N` | 支付宝联系人信息，不传取商户的联系人信息；示例值：张三 |
| `request.data.ali_zl_conf.contact_mobile_no` | 联系人手机号 | `String` | `11` | `N` | 支付宝联系人信息，不传取商户的联系人信息；示例值：[官网示例已脱敏] |
| `request.data.ali_zl_conf.contact_email` | 联系人电子邮箱 | `String` | `40` | `N` | 支付宝联系人信息，不传取商户的联系人信息；示例值：carl.chen@huifu.com |
| `request.data.ali_zl_conf.order_ticket` | 订单授权凭证 | `String` | `40` | `N` | 示例值： |
| `request.data.ali_zl_conf.account` | 商户支付宝账号 | `String` | `128` | `Y` | 商户登录支付宝控台的账号；示例值：zhangsan |
| `request.data.ali_zl_conf.fee_rate` | 服务费率 | `String` | `6` | `C` | 仅支持渠道商。平台商户调用不支持该字段；服务费率（%），0.38~3之间，精确到0.01。示例值：0.06 |
| `request.data.ali_zl_conf.license_code` | 营业执照编号 | `String` | `20` | `N` | 工商营业执照编号，示例值：92650109MA79R8E308 |
| `request.data.ali_zl_conf.license_validity_type` | 营业执照有效期类型 | `String` | `1` | `N` | 1:长期有效 0:非长期有效示例值： |
| `request.data.ali_zl_conf.license_begin_date` | 营业执照有效期开始日期 | `String` | `8` | `N` | 日期格式yyyyMMdd，示例值：20110112 |
| `request.data.ali_zl_conf.license_end_date` | 营业执照有效期截止日期 | `String` | `8` | `N` | 日期格式yyyyMMdd，示例值：20110112 |
| `request.data.ali_zl_conf.file_list[]` | 文件列表 | `String` | `—` | `Y` | jsonArray格式，F47-企业特殊资质图片(可选，企业特殊资质图片，可参考商家经营类目中的“需要的特殊资质证书”)；F48-营业执照授权函图片（可选，个体工商户如果使用总公司或其他公司的营业执照认证需上传该授权函图片）；F49-店铺内景图片(可选)；F50-店铺门头照图片(必填)；示例值：F50 |
| `request.data.ali_zl_conf.file_list[].file_type` | 文件类型 | `String` | `6` | `Y` | 示例值：F50 |
| `request.data.ali_zl_conf.file_list[].file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.alipay_pre_auth_flag` | 开通支付宝预授权 | `String` | `1` | `N` | 支付宝预授权开通；Y：是，N：否；示例值：Y；目前仅支持企业商户，汇付MCC为7011住宿服务、7296服装出租、7512汽车出租三个行业开通预授权 |
| `request.data.wx_conf_list[]` | 微信配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.wx_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 参见《[微信支付场景](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e6%94%af%e4%bb%98%e5%9c%ba%e6%99%af)》说明；示例值：1 |
| `request.data.wx_conf_list[].mcc` | *商户经营类目* | `String` | `7` | `N` | [参见微信支付宝MCC](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_zfbmcc)；个体工商户、小微商户必填；微信暂不支持修改；示例值：5411；**企业使用fee_rule_id代替原有mcc，mcc可不填** |
| `request.data.wx_conf_list[].fee_rule_id` | 费率规则号 | `String` | `3` | `N` | [微信费率规则](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wxflgz)，简称cid。示例值：758 |
| `request.data.wx_conf_list[].pay_channel_id` | 子渠道号 | `String` | `32` | `N` | 不填入驻到渠道默认配置的微信渠道号下；示例值：JP00001 |
| `request.data.wx_conf_list[].fee_rate` | 手续费（%） | `String` | `6` | `Y` | 数字格式，大于等于0,保留2位小数；示例值：0.38，代表0.38% |
| `request.data.wx_conf_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `6` | `N` | 固定金额保留2位小数；大于0。需要渠道商开通此功能。示例值：0.38 |
| `request.data.wx_conf_list[].is_check_real_name` | 是否需要实名认证 | `String` | `1` | `N` | Y-是，业务功能开通成功后使用法人信息发起实名认证申请 ； N-否；默认为N ;示例值：Y |
| `request.data.wx_conf_list[].wx_real_name_info` | 实名认证信息 | `String` | `—` | `C` | 实名时需要填写 jsonObject字符串 ；若请求微信入驻成功，但实名申请失败需要调用单独的实名接口重新发起实名。 |
| `request.data.wx_conf_list[].wx_real_name_info.finance_institution_flag` | 是否金融机构 | `String` | `5` | `N` | 选填，请根据申请主体的实际情况填写，可参考选择：https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html；1、若商户主体是金融机构，则填写：true。；2、若商户主体不是金融机构，则填写：false。；若未传入将默认填写：false；3，微信实名金融机构需要提供 F236：金融机构许可证图片一 ；F237：金融机构许可证图片二；F238：金融机构许可证图片三；F239：金融机构许可证图片四；F240：金融机构许可证图片五；补充资料填写在extended_material_list对象中；示例值：false |
| `request.data.wx_conf_list[].wx_real_name_info.finance_type` | 金融机构类型 | `String` | `128` | `N` | 当主体是金融机构时，必填；金融机构类型需与营业执照/登记证书上一致，可参考选择金融机构指引：；https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html；BANK_AGENT：银行业, 适用于商业银行、政策性银行、农村合作银行、村镇银行、开发性金融机构等；PAYMENT_AGENT：支付机构, 适用于非银行类支付机构；INSURANCE：保险业, 适用于保险、保险中介、保险代理、保险经纪等保险类业务；TRADE_AND_SETTLE：交易及结算类金融机构, 适用于交易所、登记结算类机构、银行卡清算机构、资金清算中心等；OTHER：其他金融机构, 适用于财务公司、信托公司、金融资产管理公司、金融租赁公司、汽车金融公司、贷款公司、货币经纪公司、消费金融公司、证券业、金融控股公司、股票、期货、货币兑换、小额贷款公司、金融资产管理、担保公司、商业保理公司、典当行、融资租赁公司、财经咨询等其他金融业务；示例值：INSURANCE |
| `request.data.wx_conf_list[].wx_real_name_info.cert_type` | 证书类型 | `String` | `64` | `N` | 企业商户必填；CERTIFICATE_TYPE_2388：事业单位法人证书；CERTIFICATE_TYPE_2389：统一社会信用代码证书；CERTIFICATE_TYPE_2394：社会团体法人登记证书；CERTIFICATE_TYPE_2395：民办非企业单位登记证书；CERTIFICATE_TYPE_2396：基金会法人登记证书；CERTIFICATE_TYPE_2399：宗教活动场所登记证；CERTIFICATE_TYPE_2400：其他证书/批文/证明；CERTIFICATE_TYPE_2520：执业许可证/执业证；CERTIFICATE_TYPE_2521：基层群众性自治组织特别法人统一社会信用代码证；CERTIFICATE_TYPE_2522：农村集体经济组织登记证；主体为政府机关/其他组织/事业单位时,F46：单位证明函照片必填；主体为政府机关/其他组织/事业单位时,F45：登记证书必填；补充资料填写在extended_material_list对象中；示例值：CERTIFICATE_TYPE_2389 |
| `request.data.wx_conf_list[].wx_real_name_info.micro_biz_type` | 小微经营类型 | `String` | `32` | `N` | 小微经营类型 必填字段；门店场所：MICRO_TYPE_STORE；流动经营/便民服务：MICRO_TYPE_MOBILE；线上商品/服务交易：MICRO_TYPE_ONLINE；个人商户需要填写；示例值：MICRO_TYPE_STORE ；需要提供 F22：店铺门头照图片；F24：店铺内景图片； 补充资料填写在extended_material_list对象中 |
| `request.data.wx_conf_list[].wx_real_name_info.special_category_id` | 特殊行业id | `String` | `3` | `N` | 特殊行业必填，参看微信支付提供的特殊行业id对照表：；https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/applysubject_new/chapter6_1.shtml；1，微信实名特殊行业提供 F150:行业经营许可证资质照片一；F151:行业经营许可证资质照片二；F152:行业经营许可证资质照片三；F153:行业经营许可证资质照片四；F154:行业经营许可证资质照片五；F155:行业经营许可证资质照片六；补充资料填写在extended_material_list对象中；示例值：100 |
| `request.data.wx_conf_list[].wx_real_name_info.contact_type` | 联系人类型 | `String` | `10` | `N` | LEGAL：经营者/法人；SUPER：经办人（经商户授权办理微信支付业务的人员），默认：LEGAL；1、主体为“小微/个人卖家”，可选择：LEGAL；2、主体为“个体工商户/企业/政府机关/事业单位/社会组织”，可选择：LEGAL、SUPER 示例值：LEGAL；联系人类型为SUPER时需在extended_material_list文件列表中上传联系人证件正反面照片；F28：联系人身份证正面照；F29：联系人身份证反面照；F33：联系人**护照**人像面；F241：联系人证件照正面，非身份证与护照类型；F242：联系人证件照反面，非身份证类型 |
| `request.data.wx_conf_list[].wx_real_name_info.name` | 联系人姓名 | `String` | `64` | `C` | 联系人类型contact_type=SUPER时必填。示例值：张三 |
| `request.data.wx_conf_list[].wx_real_name_info.mobile` | 联系人手机号 | `String` | `11` | `C` | 联系人类型contact_type=SUPER时必填。示例值：[官网示例已脱敏] |
| `request.data.wx_conf_list[].wx_real_name_info.contact_id_doc_type` | 联系人证件类型 | `String` | `10` | `C` | 联系人类型contact_type=SUPER时必填。；枚举值参见《自然人证件类型》说明，示例值：00；个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关仅支持身份证类型。 |
| `request.data.wx_conf_list[].wx_real_name_info.id_card_number` | 联系人证件号码 | `String` | `32` | `C` | 联系人类型contact_type=SUPER时必填。示例值：[官网示例已脱敏] |
| `request.data.wx_conf_list[].wx_real_name_info.contact_period_begin` | 联系人证件有效期开始时间 | `String` | `20` | `C` | 联系人类型contact_type=SUPER时必填；格式：yyyy-MM-dd；示例值：2019-06-06 |
| `request.data.wx_conf_list[].wx_real_name_info.contact_period_end` | 联系人证件有效期结束时间 | `String` | `20` | `C` | 联系人类型contact_type=SUPER时必填；格式：yyyy-MM-dd；示例值：2029-06-06；结束时间大于开始时间;若证件有效期为长期，请填写：长期 |
| `request.data.wx_zl_conf` | 微信直连配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `request.data.wx_zl_conf.sub_mch_id` | 微信子商户号 | `String` | `32` | `C` | 微信支付分配的子商户号；示例值：1632157057 |
| `request.data.wx_zl_conf.contact_info` | 联系人信息 | `String` | `—` | `C` | jsonObject字符串,新增时必填 |
| `request.data.wx_zl_conf.contact_info.contact_type` | 联系人类型 | `String` | `1` | `Y` | 1： 法人；2：经办人；示例值：1 |
| `request.data.wx_zl_conf.contact_info.contact_name` | 联系人姓名 | `String` | `128` | `C` | 联系人类型为经办人时必填；示例值：张三 |
| `request.data.wx_zl_conf.contact_info.cert_type` | 联系人证件类型 | `String` | `2` | `C` | 联系人类型为经办人时必填；00：身份证；01:护照；11：港澳台同胞通行证；12：外国人居留证；13：港澳居民证；14：台湾居民证；示例值：00 |
| `request.data.wx_zl_conf.contact_info.contact_cert_no` | 联系人证件号码 | `String` | `18` | `C` | 联系人类型为经办人时必填；示例值：[官网示例已脱敏] |
| `request.data.wx_zl_conf.contact_info.contact_mobile_no` | 联系人手机号 | `String` | `11` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.wx_zl_conf.contact_info.contact_email` | 联系人电子邮箱 | `String` | `40` | `Y` | 示例值：carl.chen@huifu.com |
| `request.data.wx_zl_conf.contact_info.contact_file_list` | 联系人资料 | `String` | `—` | `C` | 联系人类型为经办人时必填；F28-联系人身份证国徽面 ；F29-联系人身份证人像面；F227-微信业务办理授权函；示例值： |
| `request.data.wx_zl_conf.contact_info.contact_file_list.file_type` | 文件类型 | `String` | `6` | `Y` | 示例值：F50 |
| `request.data.wx_zl_conf.contact_info.contact_file_list.file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.wx_zl_conf.contact_info.contact_cert_validity_type` | 证件有效期类型 | `String` | `1` | `Y` | 有效期类型 1:长期有效 0:非长期有效；示例值：1；若长期有效，则无需填写证书有效期截止日期 |
| `request.data.wx_zl_conf.contact_info.contact_cert_begin_date` | 证件有效期开始日期 | `String` | `8` | `Y` | 格式：YYYYMMDD；示例值：20100908 |
| `request.data.wx_zl_conf.contact_info.contact_cert_end_date` | 证件有效期截止日期 | `String` | `8` | `N` | 格式：YYYYMMDD；示例值：20300908 |
| `request.data.wx_zl_conf.ubo_info` | 最终受益人信息 | `String` | `—` | `C` | jsonObject字符串，商户类型为企业时，微信侧必填。（如果基本信息里有的话，可以不传取 huifu_id 对应的信息）。新增时填入 |
| `request.data.wx_zl_conf.ubo_info.ubo_type` | 经营者/法人是否为受益人 | `String` | `1` | `Y` | Y-是，N-否；示例值：Y |
| `request.data.wx_zl_conf.ubo_info.ubo_info_list[]` | 受益人信息列表 | `String` | `—` | `C` | jsonArray格式,当ubo_type为Y时可不填 |
| `request.data.wx_zl_conf.ubo_info.ubo_info_list[].ubo_cert_type` | 证件类型 | `String` | `2` | `Y` | 00:身份证 01:护照；示例值：00 |
| `request.data.wx_zl_conf.ubo_info.ubo_info_list[].ubo_cert_no` | 证件号码 | `String` | `18` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.wx_zl_conf.ubo_info.ubo_info_list[].ubo_name` | 姓名 | `String` | `32` | `Y` | 示例值：张三 |
| `request.data.wx_zl_conf.ubo_info.ubo_info_list[].ubo_cert_doc_address` | 受益人证件居住地址 | `String` | `128` | `Y` | 示例值：上海宝山区共富路11号 |
| `request.data.wx_zl_conf.ubo_info.ubo_info_list[].ubo_cert_validity_type` | 证件有效类型 | `String` | `1` | `Y` | 1:长期有效 0:非长期有效；示例值：0 |
| `request.data.wx_zl_conf.ubo_info.ubo_info_list[].ubo_cert_begin_date` | 证件有效期开始日期 | `String` | `8` | `Y` | 示例值：20200908 |
| `request.data.wx_zl_conf.ubo_info.ubo_info_list[].ubo_cert_end_date` | 证件有效期截止日期 | `String` | `8` | `N` | 示例值：20330908 |
| `request.data.wx_zl_conf.ubo_info.ubo_info_list[].ubo_file_list[]` | 文件列表 | `String` | `—` | `Y` | jsonArray，F228-受益人身份证正面（国徽面），F229-联系人身份证反面（人像面）；示例值：F229 |
| `request.data.wx_zl_conf.ubo_info.ubo_info_list[].ubo_file_list[].file_type` | 文件类型 | `String` | `6` | `Y` | 示例值：F50 |
| `request.data.wx_zl_conf.ubo_info.ubo_info_list[].ubo_file_list[].file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.wx_zl_conf.sales_info` | 经营场景 | `Object` | `—` | `C` | jsonObject字符串，新增时填入 |
| `request.data.wx_zl_conf.sales_info.sales_scenes_type` | 经营场景类型 | `String` | `256` | `Y` | 多个以英文逗号分割，至少要有一个；线下门店：SALES_SCENES_STORE；公众号：SALES_SCENES_MP；小程序：SALES_SCENES_MINI_PROGRAM；互联网：SALES_SCENES_WEB；APP：SALES_SCENES_APP；企业微信：SALES_SCENES_WEWORK；示例值：SALES_SCENES_WEWORK |
| `request.data.wx_zl_conf.sales_info.fee_rate` | 功能费率 | `String` | `6` | `C` | 仅支持渠道商传入该字段。示例值：0.06；平台商户为子商户开通微信直连支付时，不支持该字段，取平台商户费率上送微信。 |
| `request.data.wx_zl_conf.sales_info.fee_rate_file_list` | 文件列表 | `String` | `—` | `N` | 微信直连商户费率材料，根据微信要求上送。示例值：d1451277-85c6-3177-ac3d-a8be47b9ae9d |
| `request.data.wx_zl_conf.sales_info.fee_rate_file_list.file_type` | 文件类型 | `String` | `6` | `Y` | 微信直连商户费率材料，根据微信要求上送。示例值：F75 |
| `request.data.wx_zl_conf.sales_info.fee_rate_file_list.file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：d1451277-85c6-3177-ac3d-a8be47b9ae9d |
| `request.data.wx_zl_conf.sales_info.biz_store_name` | 门店名称 | `String` | `128` | `N` | 不传，取 huifu_id 关联信息,微信侧条件必填；示例值：卡卡奶茶共富店 |
| `request.data.wx_zl_conf.sales_info.biz_address_code` | 门店省市编码 | `String` | `128` | `N` | 不传，取 huifu_id 关联信息,微信侧条件必填；示例值：310100 |
| `request.data.wx_zl_conf.sales_info.biz_store_address` | 门店地址 | `String` | `128` | `N` | 不传，取 huifu_id 关联信息,微信侧条件必填；示例值：上海宝山共富路1号 |
| `request.data.wx_zl_conf.sales_info.biz_sub_jsapi_app_id` | 线下场所对应的商家公众号APPID | `String` | `256` | `C` | 开通线下门店场景时，填入。都填入时，取公众号的上送微信。示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.sales_info.biz_sub_mini_app_id` | 线下场所对应的商家小程序APPID | `String` | `256` | `C` | 开通线下门店场景时，填入。都填入时，取公众号的上送微信。示例值：wxea9c30a90fs8d3fe |
| `request.data.wx_zl_conf.sales_info.jsapi_app_id` | 服务商公众号 ID | `String` | `256` | `C` | 开通公众号场景时，直连服务商和商户的公众号 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.sales_info.jsapi_sub_app_id` | 商家公众号APPID | `String` | `256` | `C` | 开通公众号场景时，直连服务商和商户的公众号 APP ID，二选一填入。示例值：wxea9c30a90fs8d3fe |
| `request.data.wx_zl_conf.sales_info.mini_app_id` | 服务商小程序APPID | `String` | `256` | `C` | 开通小程序场景时，直连服务商和商户的小程序 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.sales_info.mini_sub_app_id` | 商家小程序APPID | `String` | `256` | `C` | 开通小程序场景时，直连服务商和商户的小程序 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.sales_info.app_app_id` | 服务商应用APPID | `String` | `256` | `C` | 开通 APP 场景时，直连服务商和商户的 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.sales_info.app_sub_app_id` | 商家应用APPID | `String` | `256` | `C` | 开通 APP 场景时，直连服务商和商户的 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.sales_info.web_domain` | 互联网网站域名 | `String` | `256` | `C` | 开通互联网场景时填入；示例值：huifu.com |
| `request.data.wx_zl_conf.sales_info.web_app_id` | 互联网网站对应的商家APPID | `String` | `256` | `C` | 开通互联网场景时填入；示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.sales_info.sub_corp_id` | 商家企业微信CorpID | `String` | `256` | `C` | 开通企业微信场景时填入；示例值：xxxxx |
| `request.data.wx_zl_conf.sales_info.sales_scenes_file_list` | 文件列表 | `String` | `6` | `Y` | 场景资料文件；附件资料列表fileList；线下门店场景，F49与F50必传；公众号场景，F95，F96，F97，F98，F99，总共至少传1张，最多传5张；小程序场景，F60，F61，F62，F63，F64，总共至少传1张，最多传5张；APP场景，F65，F66，F67，F68，各传1张；互联网网站场景，若备案主体与申请主体不同，请务必上传加盖公章的网站授权函(F69)。；企业微信场景，F70，F71，F72，F73，F74，总共至少传1张，最多传5张；F49-店铺内景图片；F50-店铺门头照图片；F95-公众号页面截图一；F96-公众号页面截图二；F97-公众号页面截图三；F98-公众号页面截图四；F99-公众号页面截图五；F60-小程序截图截图一；F61-小程序截图截图二；F62-小程序截图截图三；F63-小程序截图截图四；F64-小程序截图截图五；F65-APP首页截图；F66-APP尾页截图；F67-APP应用内截图；F68-APP支付页截图；F69-网站授权函；F70-企业微信页面截图一；F71-企业微信页面截图二；F72-企业微信页面截图三；F73-企业微信页面截图四；F74-企业微信页面截图五；示例值：F74 |
| `request.data.wx_zl_conf.sales_info.sales_scenes_file_list.file_type` | 文件类型 | `String` | `6` | `Y` | 示例值：F50 |
| `request.data.wx_zl_conf.sales_info.sales_scenes_file_list.file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.wx_zl_conf.certificate_info` | 特殊主体登记证书 | `Object` | `—` | `C` | jsonObject字符串，商户营业执照类型为政府机关/事业单位/其他组织时，传入相应信息。新增时需填入 |
| `request.data.wx_zl_conf.certificate_info.cert_type` | 登记证书类型 | `String` | `32` | `Y` | CERTIFICATE_TYPE_2388：事业单位法人证书；CERTIFICATE_TYPE_2389：统一社会信用代码证书；CERTIFICATE_TYPE_2390：有偿服务许可证（军队医院适用）；CERTIFICATE_TYPE_2391：医疗机构执业许可证（军队医院适用）；CERTIFICATE_TYPE_2392：企业营业执照（挂靠企业的党组织适用）；CERTIFICATE_TYPE_2393：组织机构代码证（政府机关适用）；CERTIFICATE_TYPE_2394：社会团体法人登记证书；CERTIFICATE_TYPE_2395：民办非企业单位登记证书；CERTIFICATE_TYPE_2396：基金会法人登记证书；CERTIFICATE_TYPE_2397：慈善组织公开募捐资格证书；CERTIFICATE_TYPE_2398：农民专业合作社法人营业执照；CERTIFICATE_TYPE_2399：宗教活动场所登记证；CERTIFICATE_TYPE_2400：其他证书/批文/证明；示例值：CERTIFICATE_TYPE_2400 |
| `request.data.wx_zl_conf.certificate_info.cert_no` | 证书号 | `String` | `32` | `Y` | 请填写登记证书上的证书编号。示例值：92650109MA79R8E308 |
| `request.data.wx_zl_conf.certificate_info.cert_mer_name` | 证书商户名称 | `String` | `128` | `Y` | 请填写登记证书上的商户名称。示例值：上海汇付支付服务公司 |
| `request.data.wx_zl_conf.certificate_info.reg_detail` | 注册地址 | `String` | `128` | `Y` | 请填写登记证书的注册地址。示例值：上海徐汇宜山路601号C5栋 |
| `request.data.wx_zl_conf.certificate_info.legal_name` | 法人姓名 | `String` | `32` | `Y` | 1、只能由中文字符、英文字符、可见符号组成。；2、请填写登记证书上的法定代表人姓名。示例值：张三 |
| `request.data.wx_zl_conf.certificate_info.cert_validity_type` | 证书有效期类型 | `String` | `1` | `Y` | 有效期类型 1:长期有效 0:非长期有效；示例值：0；若长期有效，则无需填写证书有效期截止日期 |
| `request.data.wx_zl_conf.certificate_info.cert_begin_date` | 证书有效期开始日期 | `String` | `8` | `Y` | 格式：YYYYMMDD；示例值：20100908 |
| `request.data.wx_zl_conf.certificate_info.cert_end_date` | 证书有效期截止日期 | `String` | `8` | `N` | 格式：YYYYMMDD；示例值：20300908 |
| `request.data.wx_zl_conf.certificate_info.cert_file_list[]` | 文件列表 | `String` | `—` | `Y` | jsonArray，F46-单位证明函，F45-登记证书 |
| `request.data.wx_zl_conf.certificate_info.cert_file_list[].file_type` | 文件类型 | `String` | `6` | `Y` | 示例值：F50 |
| `request.data.wx_zl_conf.certificate_info.cert_file_list[].file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.wx_zl_conf.wx_card_info` | 银行账户信息 | `String` | `—` | `C` | jsonObject字符串，该字段不填时，取商户在汇付系统录入的结算账号信息。新增或修改时填入，修改时必填 |
| `request.data.wx_zl_conf.wx_card_info.card_type` | 账户类型 | `String` | `1` | `Y` | 0：对公银行账户；1：经营者个人银行卡；示例值：0 |
| `request.data.wx_zl_conf.wx_card_info.card_name` | 开户名称 | `String` | `128` | `Y` | 选择“经营者个人银行卡”时，开户名称必须与“经营者证件姓名”一致。选择“对公银行账户”时，开户名称必须与营业执照上的“商户名称”一致。；示例值：张三 |
| `request.data.wx_zl_conf.wx_card_info.bank_code` | 开户银行 | `String` | `8` | `Y` | 客户按汇付银行编码上送；示例值：01020000 |
| `request.data.wx_zl_conf.wx_card_info.prov_id` | 开户银行省编码 | `String` | `6` | `Y` | 按汇付的省市编码；示例值：310000 |
| `request.data.wx_zl_conf.wx_card_info.area_id` | 开户银行市编码 | `String` | `6` | `Y` | 示例值：310100 |
| `request.data.wx_zl_conf.wx_card_info.branch_code` | 开户银行联行号 | `String` | `20` | `C` | 开户银行联行号与开户银行全称（含支行)二选一；示例值：102290026507 |
| `request.data.wx_zl_conf.wx_card_info.branch_name` | 开户银行全称（含支行) | `String` | `128` | `C` | 开户银行联行号与开户银行全称（含支行)二选一；示例值：中国工商银行股份有限公司上海市中山北路支行 |
| `request.data.wx_zl_conf.wx_card_info.card_no` | 银行账号 | `String` | `30` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list[]` | 配置集合 | `Array` | `512` | `C` | 对指定的sub_mch_id做配置 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list[].service_code` | 申请服务 | `String` | `16` | `Y` | JSAPI-公众号，APPLET-小程序；示例值：JSAPI |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list[].sub_app_id` | 功能服务appid | `String` | `32` | `Y` | 子商户的公众号、小程序ID；示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list[].switch_state` | 功能开关 | `String` | `1` | `Y` | 0-关闭，1-打开；示例值：1 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list[].fee_rate` | 功能费率(%) | `String` | `6` | `Y` | 保留两位小数。示例值：0.60 |
| `request.data.wx_zl_conf.business_addition_msg` | 补充说明信息 | `String` | `512` | `N` | 示例值：补充说明 |
| `request.data.wx_zl_conf.addition_file_list[]` | 补充说明文件列表 | `String` | `—` | `N` | jsonArray格式，根据实际审核情况，额外要求商家提供指定的补充资料；F85-微信直连额外补充材料一；F86-微信直连额外补充材料二；F87-微信直连额外补充材料三；F88-微信直连额外补充材料四；F89-微信直连额外补充材料五；F90-法人开户承诺函；F91-法人开户意愿视频 |
| `request.data.wx_zl_conf.addition_file_list[].file_type` | 文件类型 | `String` | `6` | `Y` | 示例值：F50 |
| `request.data.wx_zl_conf.addition_file_list[].file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.wx_zl_conf.operate_type` | 操作类型 | `String` | `10` | `C` | ADD-新增， UPDATE-修改， 默认新增；示例值：ADD |
| `request.data.wechatpay_pre_auth_flag` | 开通微信预授权 | `String` | `1` | `N` | 微信预授权开通；Y：是，N：否；示例值：Y；目前仅支持企业商户，MCC为7011住宿服务、7296服装出租、7512汽车出租三个行业开通预授权 |
| `request.data.union_conf_list[]` | 银联二维码配置 | `String` | `—` | `N` | jsonArray字符串 |
| `request.data.union_conf_list[].charge_cate_code` | 银联业务手续费类型 | `String` | `2` | `N` | 01：减免类；02：优惠类；03：标准类，小微商户仅支持03；04：线上类；默认03标准类；示例值：03 |
| `request.data.union_conf_list[].debit_fee_rate` | 借记卡手续费（%） | `String` | `9` | `Y` | 数字格式，大于等于0，保留2位小数；示例值：0.38 |
| `request.data.union_conf_list[].credit_fee_rate_up` | 贷记卡手续费1000以上（%） | `String` | `9` | `Y` | 数字格式，大于等于0，保留2位小数；示例值：0.60 |
| `request.data.union_conf_list[].credit_fee_rate_down` | 贷记卡手续费1000及以下（%） | `String` | `9` | `Y` | 数字格式，大于等于0，保留2位小数；示例值：0.60 |
| `request.data.union_conf_list[].mcc` | 商户经营类目 | `String` | `7` | `N` | [银联MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylmccbm) ；示例值：5311 |
| `request.data.bank_card_conf` | 银行卡业务配置 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.bank_card_conf.charge_cate_code` | 银行业务手续费类型 | `String` | `2` | `N` | 01-减免类 02-优惠类 03-标准类 ；默认03标准类；示例值：03 |
| `request.data.bank_card_conf.debit_fee_rate` | 借记卡手续费（%） | `String` | `9` | `Y` | 数字格式，大于等于0,保留2位小数；示例值：0.50代表费率为0.5% |
| `request.data.bank_card_conf.debit_fee_limit` | 借记卡封顶值 | `String` | `4` | `N` | 数字格式，大于等于0,保留2位小数；示例值：5.00 |
| `request.data.bank_card_conf.credit_fee_rate` | 贷记卡手续费（%） | `String` | `9` | `Y` | 数字格式，大于等于0,保留2位小数；示例值：0.60代表费率为0.6% |
| `request.data.bank_card_conf.is_open_small_flag` | 是否开通小额双免 | `String` | `1` | `N` | 开关状态 0:不开通双免 1:开通双免 2:仅免签，默认0不开通；示例值：1 |
| `request.data.bank_card_conf.small_free_amt` | 小额双免单笔限额(元) | `String` | `9` | `N` | 限额需小于等于1000，不传默认0（不开通小额双免）， 开通小额双免必须填值；示例值：1000.00 |
| `request.data.bank_card_conf.small_fee_amt` | 小额双免手续费（%） | `String` | `9` | `N` | 数字格式，大于等于0,保留2位小数，开通小额双免填必须填制；示例值：0.38代表费率为0.38% |
| `request.data.bank_card_conf.mcc` | *商户经营类目* | `String` | `7` | `Y` | [银联MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylmccbm)；示例值：5311 |
| `request.data.bank_card_conf.is_open_cloud_flag` | 云闪付开通状态 | `String` | `1` | `N` | 0-关闭 1-开通 |
| `request.data.online_fee_conf_list[]` | 线上费率配置 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.online_fee_conf_list[].fee_type` | 业务类型 | `String` | `25` | `Y` | ONLINE_PERSON:个人网银支付，online_flag开通了才需要填；ONLINE_ENT:企业网银支付，online_flag开通了才需要填；QUICK_DEBIT:快捷借记卡支付，quick_flag开通了才需要填；QUICK_CREDIT:快捷贷记卡支付，quick_flag开通了才需要填；WAP:手机WAP支付，online_flag开通了才需要填；ONLINE_ENT_TOP_UP:B2B网银充值，online_recharge_flag开通了才需要填；ONLINE_PERSON_TOP_UP:B2C网银充值，online_recharge_flag开通了才需要填；WITHHOLD_DEBIT:代扣借记卡支付；WITHHOLD_CREDIT:代扣贷记卡支付，withhold_flag开通了才需要填；示例值：ONLINE_PERSON |
| `request.data.online_fee_conf_list[].bank_id` | 银行编码 | `String` | `8` | `Y` | 参考： [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；示例值：01020000 |
| `request.data.online_fee_conf_list[].bank_name` | 银行名称 | `String` | `50` | `N` | 示例值：中国工商银行上海市中山北路支行 |
| `request.data.online_fee_conf_list[].bank_short_chn` | 银行中文简称 | `String` | `50` | `N` | 示例值：工行上海市中北支行 |
| `request.data.online_fee_conf_list[].stat_flag` | 功能开关状态 | `String` | `1` | `Y` | 各银行不同支付方式的开关状态；1开，0关；示例值：1 |
| `request.data.online_fee_conf_list[].dc_flag` | 借贷标志 | `String` | `1` | `Y` | D:借记,C:贷记；B2B网银填写D；示例值：D |
| `request.data.online_fee_conf_list[].fix_amt` | 手续费（固定/元） | `String` | `16` | `N` | 必须填写一种收费方式；保留两位小数；示例值：1.00 |
| `request.data.online_fee_conf_list[].fee_rate` | 费率（%） | `String` | `6` | `N` | 必须填写一种收费方式；保留两位小数；示例值：0.38 |
| `request.data.online_fee_conf_list[].fee_min_amt` | 手续费最小值（元） | `String` | `6` | `N` | 必须填写一种收费方式；保留两位小数；示例值：1.00 |
| `request.data.online_fee_conf_list[].fee_formula_type` | 代扣手续费计费模式 | `String` | `2` | `N` | withhold_flag为Y时，才可传入；01: 百分比手续费，无封顶值或保底值；02: 百分比手续费，有保底值；03: 固定手续费；04: 固定手续费+百分比手续费；为空默认04 示例值：04 |
| `request.data.online_pay_fee_conf_list[]` | 线上手续费承担方配置 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.online_pay_fee_conf_list[].pay_type` | 业务类型 | `String` | `25` | `N` | ONLINE_PERSON:个人网银；ONLINE_ENT:企业网银；QUICK:快捷；WAP:手机WAP支付；ONLINE_ENT_TOP_UP:B2B网银充值；ONLINE_PERSON_TOP_UP:B2C网银充值；WITHHOLD:代扣支付；示例值：WAP |
| `request.data.online_pay_fee_conf_list[].out_fee_acct_type` | 手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户；示例值：01 |
| `request.data.online_pay_fee_conf_list[].out_fee_huifuid` | 手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填；示例值：[官网示例已脱敏] |
| `request.data.online_pay_fee_conf_list[].out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；示例值：2 |
| `request.data.online_busi_type` | 线上业务类型编码 | `String` | `8` | `C` | 基本信息入驻接口中scene_type=ONLINE/ALL时必填；开通以下业务快捷、网银、余额支付Pro版、银行大额转账、分账比例>30%、代扣需要提供补充材料，参见[线上业务类型编码及补充材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E7%BA%BF%E4%B8%8A%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B%E7%BC%96%E7%A0%81%E5%8F%8A%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E.xlsx)；材料通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传示例值：H7999AL |
| `request.data.online_media_info_list[]` | 运营媒介 | `String` | `—` | `N` | jsonArray字符串；基本信息入驻接口中scene_type=ONLINE/ALL时必填；如果开通快捷、网银、余额支付Pro版、分账、银行大额转账、代扣需提供运营媒介材料 |
| `request.data.online_media_info_list[].media_type` | *运营媒介类型* | `String` | `2` | `Y` | S1-PC网站；若媒介项为PC网站：必填字段（PC网站域名、ICP备案/许可证号）；S2-APP场景；若媒介项为APP场景：必填字段（APP名称、APP下载地址），若开通微信App支付，则新增app_id、app_name必填；S3-小程序场景；若媒介项为小程序：必填字段（小程序名称）；S4-公众号场景；若媒介项为公众号：必填字段（公众号名称）；S5-其他；媒介项为其他：其他有效信息或链接地址必填；线上场景时必填一项；示例值：S1 |
| `request.data.online_media_info_list[].media_name` | *媒介名称* | `String` | `200` | `C` | PC网站域名／APP名称／小程序名称／公众号名称；示例值：汇付服务；运营媒介类型为 ：S1/S2/S3/S4时，必填 |
| `request.data.online_media_info_list[].test_account` | *测试账号* | `String` | `64` | `N` | 示例值：test |
| `request.data.online_media_info_list[].test_secret` | *测试密码* | `String` | `64` | `N` | 示例值：test |
| `request.data.online_media_info_list[].mer_icp` | ICP备案/许可证号 | `String` | `200` | `C` | 运营媒介类型为 ：S1时必填；示例值：沪ICP备06046402号-28 |
| `request.data.online_media_info_list[].other_info` | *其他有效信息* | `String` | `200` | `C` | 其他有效信息或链接地址/APP下载地址；类型为S5或S2必填；示例值：http://download.huifu.com |
| `request.data.online_media_info_list[].media_front_page` | *运营媒介-首页* | `String` | `128` | `N` | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.online_media_info_list[].media_service_page` | *运营媒介-服务/商品明细页面* | `String` | `128` | `N` | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.online_media_info_list[].media_order_page` | *运营媒介-下单场景页面* | `String` | `128` | `N` | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.online_media_info_list[].media_pay_page` | *运营媒介-支付页面* | `String` | `128` | `N` | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.online_media_info_list[].media_mer_common_flag` | *媒介主体与商户主体是否一致* | `String` | `1` | `C` | Y/N；示例值：Y；运营媒介为S1、S2、S3、S4且企业商户开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），必填；若不一致，则需提供ICP备案/APP/微信公众号/小程序主体与商户的使用授权或开发证明材料 |
| `request.data.online_media_info_list[].authorize_materials` | *授权或开发证明材料* | `String` | `128` | `C` | 运营媒介为S1、S2、S3、S4且媒介主体与商户主体不一致时，且企业商户开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），必填；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.online_media_info_list[].other_material` | 微信APP补充材料 | `String` | `128` | `C` | 运营媒介为S2且开通微信下app支付时选填，具体见[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) |
| `request.data.online_media_info_list[].app_id` | appId | `String` | `128` | `C` | 运营媒介为S2且开通微信下app支付时必填 |
| `request.data.online_media_info_list[].app_name` | appId认证主体名称 | `String` | `128` | `C` | 运营媒介为S2且开通微信下app支付时必填 |
| `request.data.online_media_info_list[].supplement` | 补充说明 | `String` | `512` | `C` | 运营媒介为S2且开通微信下app支付时选填 |
| `request.data.balance_pay_config` | *余额支付配置* | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.balance_pay_config.fee_rate` | 手续费(%) | `String` | `9` | `N` | 支持两位小数 fee_rate与fee_fix_amt不能同时为空；示例值：0.50代表费率为0.5% |
| `request.data.balance_pay_config.fee_fix_amt` | 手续费（固定/元） | `String` | `9` | `N` | 支持两位小数 fee_rate与fee_fix_amt不能同时为空；示例值：1.50；注：如果fee_fix_amt与fee_rate都填写了则手续费=fee_fix_amt+支付金额\*fee_rate |
| `request.data.balance_pay_config.out_fee_acct_type` | 手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01 |
| `request.data.balance_pay_config.out_fee_huifuid` | 手续费外扣汇付ID | `String` | `18` | `N` | 开通余额支付手续费外扣业务时必填，示例值：[官网示例已脱敏] |
| `request.data.balance_pay_config.out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣），示例值：1 |
| `request.data.balance_pay_config.balance_model` | *业务模式* | `String` | `1` | `Y` | 2-入驻商户货款（周期性结算）；3-营销补贴（周期性结算）；4-推广方（渠道/代理/个人）的服务佣金/抽成；5-红包发放；6-钱包功能；7-其他模式；8-线上入驻商户货款（周期性结算）；9-线上营销补贴（周期性结算）；10-线上推广方（渠道/代理/个人）的服务佣金/抽成；11-线上其他模式；单选；示例值：6 |
| `request.data.balance_pay_config.description_info` | 业务情况说明 | `String` | `—` | `Y` | jsonObject字符串 |
| `request.data.balance_pay_config.description_info.busi_instruction` | *业务模式说明* | `String` | `500` | `C` | 请详细说明商户的业务模式，包括不限于（业务参与方、各方的权利及义务关系等）。最大500个汉字，仅Pro版时必填；示例值：商户向企业采购产品，并将其展示在其电商平台上，用户注册后购买其产品，产品主要有家电、服饰、鞋帽等，用户购买产品的资金作为商户所得，商户根据订单情况进行物流配送。 |
| `request.data.balance_pay_config.description_info.capital_instruction` | *资金流向说明* | `String` | `500` | `C` | 请详细说明商户的资金流向，包括但不限于（交易所涉及的各方账户、资金流入流出过程等）。最大500个汉字，仅Pro版时必填；示例值：用户选购产品后根据订单支付给商户，商户根据结算周期，结算到对公账户。 |
| `request.data.balance_pay_config.description_info.function_instruction` | *功能开通用途说明* | `String` | `500` | `C` | 请详述所申请功能的原因、场景、涉及对象类型。最大500个汉字，仅Pro版时必填；示例值：企业工资代发 |
| `request.data.balance_pay_config.charge_mode` | 扣费模式 | `String` | `2` | `N` | 内扣时枚举值: 01: 默认规则, 02: 收款方分摊, 03: 交易时指定承担方；外扣时枚举值: 10: 指定承担方, 11: 出款方承担, 12: 交易时指定承担方；示例值：11；内扣时默认为01，外扣时默认为10 |
| `request.data.balance_pay_config.pay_mode` | 余额支付模式 | `String` | `4` | `N` | pro，lite；示例值：pro；为空时默认为pro；lite版不支持当日收款资金余额支付 |
| `request.data.out_order_funds_config` | 全域资金管理配置(华通银行) | `String` | `—` | `N` | jsonObject字符串；**即将废弃**，请对接[全渠道资金管理配置接口](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_qypz) |
| `request.data.out_order_funds_config.out_order_auto_acct_flag` | 自动入账开关 | `String` | `1` | `Y` | 开通、关闭自动入账功能；0:关闭 1:开通；示例值：1；关闭自动入账需要[处理银行来账通知](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_lztz)，并调用[汇付入账确认接口](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_yhskfk)来确认入账。 |
| `request.data.out_order_funds_config.fee_rate` | 支付手续费(%) | `String` | `6` | `N` | 支持两位小数；示例值：0.45；fee_rate与fee_fix_amt与fee_min_amt不能同时为空 |
| `request.data.out_order_funds_config.fee_min_amt` | 手续费最小值(元) | `String` | `6` | `N` | 支付手续费最小值，支持两位小数；示例值：1.00fee_rate与fee_fix_amt与fee_min_amt不能同时为空 |
| `request.data.out_order_funds_config.out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户；示例值：01 |
| `request.data.out_order_funds_config.out_fee_flag` | 交易手续费外扣标记 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；示例值：1 |
| `request.data.out_order_funds_config.out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 示例值：[官网示例已脱敏] |
| `request.data.out_order_funds_config.out_order_acct_card` | 全域资金开户银行卡信息 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.out_order_funds_config.out_order_acct_card.prov_id` | 银行所在省 | `String` | `6` | `N` | [参考省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000 |
| `request.data.out_order_funds_config.out_order_acct_card.area_id` | 银行所在市 | `String` | `6` | `N` | [参考省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310100 |
| `request.data.out_order_funds_config.out_order_acct_card.bank_code` | 银行编码 | `String` | `8` | `N` | 参考[银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；示例值：01020000 |
| `request.data.out_order_funds_config.out_order_acct_card.branch_code` | 支行联行号 | `String` | `12` | `C` | card_type为0时必填，参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `request.data.out_order_funds_config.out_order_acct_card.branch_name` | 支行名称 | `String` | `64` | `C` | card_type为0时必填 ,参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：中国工商银行上海市中山北路支行 |
| `request.data.out_order_funds_config.out_order_acct_card.card_name` | 结算账户名 | `String` | `128` | `Y` | 银行卡对应的户名；示例值：上海汇付支付有限公司 |
| `request.data.out_order_funds_config.out_order_acct_card.card_no` | 银行卡号 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.out_order_funds_config.out_order_acct_card.card_type` | 卡类型 | `String` | `1` | `Y` | 0:对公 1:对私；示例值：0 |
| `request.data.out_order_funds_config.out_order_acct_card.cert_type` | 持卡人证件类型 | `String` | `2` | `C` | 00:身份证；示例值：00；card_type为1时选填。 |
| `request.data.out_order_funds_config.out_order_acct_card.cert_validity_type` | 持卡人证件有效期类型 | `String` | `1` | `N` | card_type为1时选填；1:长期有效 0:非长期有效；示例值：0；若填写cert_begin_date，cert_no，cert_type需同时填写。 |
| `request.data.out_order_funds_config.out_order_acct_card.cert_begin_date` | 持卡人证件有效期（起始） | `String` | `8` | `C` | card_type为1时选填；格式：yyyyMMdd，示例值：20210830；若填写cert_no，cert_validity_type，cert_type需同时填写。 |
| `request.data.out_order_funds_config.out_order_acct_card.cert_end_date` | 持卡人证件有效期（截止） | `String` | `8` | `C` | cert_validity_type变更为0时必填，格式：yyyyMMdd；示例值：20210830 |
| `request.data.out_order_funds_config.out_order_acct_card.cert_no` | 持卡人证件号码 | `String` | `32` | `C` | card_type为1时选填；示例值：[官网示例已脱敏] |
| `request.data.out_order_funds_config.out_order_acct_card.mp` | 银行卡绑定手机号 | `String` | `11` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.out_order_funds_config.out_order_acct_card.open_licence_no` | 开户许可证核准号 | `String` | `32` | `Y` | 示例值：J2900123456789 |
| `request.data.out_order_funds_config.out_order_acct_open_fees` | 全域资金开户手续费 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.out_order_funds_config.out_order_acct_open_fees.fee_fix_amt` | 开户手续费(元) | `String` | `9` | `Y` | 支持两位小数；示例值：1.00 |
| `request.data.out_order_funds_config.out_order_acct_open_fees.out_fee_acct_type` | 开户手续费外扣时的账户类型 | `String` | `2` | `C` | 01-基本户，02-现金户，05-充值户，09-营销户，不填默认01；示例值：01；注：fee_fix_amt：开户手续费大于0时必填 |
| `request.data.out_order_funds_config.out_order_acct_open_fees.out_fee_huifuid` | 开户手续费外扣汇付ID | `String` | `18` | `C` | 开通手续费外扣业务时必填；示例值：[官网示例已脱敏]；注：fee_fix_amt：开户手续费大于0时必填 |
| `request.data.out_order_funds_config.business_model` | 全域支付业务模式 | `String` | `20` | `N` | acquiringMode：收单模式，；示例值：acquiringMode |
| `request.data.out_order_funds_config.other_payment_institutions_pic` | 全渠道资金管理补充材料 | `String` | `64` | `C` | 涉及文件类型：F504-全渠道资金管理补充材料；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.combine_pay_config` | 补贴支付 | `String` | `—` | `N` | jsonObject格式 |
| `request.data.combine_pay_config.fee_rate` | 手续费(%) | `String` | `9` | `N` | 支付手续费(%) 支持两位小数 fee_rate与fee_fix_amt 不能同时为空；示例值：0.50代表费率为0.5% |
| `request.data.combine_pay_config.fee_fix_amt` | 手续费（固定/元） | `String` | `9` | `N` | 支付固定手续费(元)支持两位小数 fee_rate与fee_fix_amt 不能同时为空；示例值：1.50；注：如果fee_fix_amt与fee_rate都填写了则手续费=fee_fix_amt+支付金额\*fee_rate |
| `request.data.combine_pay_config.out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `Y` | 1:外扣，仅支持外扣 ，示例值：1；优先级高于相同名称的公共参数 |
| `request.data.combine_pay_config.out_fee_huifuid` | 手续费外扣汇付ID | `String` | `18` | `Y` | 开通交易手续费外扣时必填，示例值：[官网示例已脱敏]；优先级高于相同名称的公共参数 |
| `request.data.combine_pay_config.out_fee_acct_type` | 手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01；优先级高于相同名称的公共参数 |
| `request.data.hb_fq_fee_config` | 花呗分期费率配置 | `String` | `—` | `N` | jsonObject字符串；分期业务必填写 |
| `request.data.hb_fq_fee_config.three_period` | 花呗分期3期（%） | `String` | `4` | `N` | 不为空时，只接受费率:1.80；示例值：1.80代表费率为1.80% |
| `request.data.hb_fq_fee_config.six_period` | 花呗分期6期（%） | `String` | `4` | `N` | 不为空时，只接受费率:4.50；示例值：4.50代表费率为4.50% |
| `request.data.hb_fq_fee_config.twelve_period` | 花呗分期12期（%） | `String` | `4` | `N` | 不为空时，只接受费率:7.50；示例值：7.50代表费率为7.50% |
| `request.data.hb_fq_fee_config.ali_mcc` | 商户经营类目 | `String` | `32` | `N` | [支付宝MCC](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_zfbmcc)；示例值：5411 |
| `request.data.hb_fq_fee_config.pay_scene` | 支付场景 | `String` | `2` | `N` | 分期业务必填：1：线下扫码；示例值：1 |
| `request.data.hb_fq_fee_config.acq_three_period` | 花呗收单分期3期（%） | `String` | `4` | `C` | 分期费率不为空时，收单费率必填，大于0，保留2位小数，不小于渠道商成本；示例值：1.0代表费率为1.00% |
| `request.data.hb_fq_fee_config.acq_six_period` | 花呗收单分期6期（%） | `String` | `4` | `C` | 分期费率不为空时，收单费率必填，大于0，保留2位小数，不小于渠道商成本；示例值：1.0代表费率为1.00% |
| `request.data.hb_fq_fee_config.acq_twelve_period` | 花呗收单分期12期（%） | `String` | `4` | `C` | 分期费率不为空时，收单费率必填，大于0，保留2位小数，不小于渠道商成本；示例值：1.0代表费率为1.00% |
| `request.data.hb_fq_fee_config.twentyfour_period` | 花呗分期24期（%） | `String` | `4` | `N` | 不为空时，只接受费率:15；示例值：15代表费率为15% |
| `request.data.hb_fq_fee_config.acq_twentyfour_period` | 花呗收单分期24期（%） | `String` | `4` | `C` | 分期费率不为空时，收单费率必填，大于0，保留2位小数，不小于渠道商成本；示例值：1.0代表费率为1.00% |
| `request.data.split_conf_info` | 分账配置信息 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.split_conf_info.div_flag` | 分账开关 | `String` | `1` | `Y` | Y：开，N：关；示例值：Y |
| `request.data.split_conf_info.rule_origin` | 分账规则来源 | `String` | `2` | `Y` | 01：接口动态规则，02：控台固定配置；示例值：01 |
| `request.data.split_conf_info.apply_ratio` | 最大分账比例% | `String` | `9` | `Y` | 0-100 的数值，支持两位小数; 示例值：20.00 |
| `request.data.split_conf_info.acct_split_bunch_list[]` | 分账明细 | `String` | `—` | `N` | 分账规则来源选择平台配置时必填,jsonArray格式 |
| `request.data.split_conf_info.acct_split_bunch_list[].fee_rate` | 分账比例 | `String` | `9` | `Y` | 百分比支持两位小数；所有分账方比例汇总需100%示例值：0.20 |
| `request.data.split_conf_info.acct_split_bunch_list[].huifu_id` | 汇付Id | `String` | `18` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.split_conf_info.start_type` | 生效类型 | `String` | `1` | `N` | 0：审核通过即时生效；1：审核通过次日生效；示例值：1 |
| `request.data.split_conf_info.out_fee_flag` | 手续费外扣开关 | `String` | `1` | `N` | 1:外扣 2:内扣（默认）；示例值：1 |
| `request.data.split_conf_info.out_fee_acct_type` | 手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户(默认)，02-现金户，05-充值户；示例值：01 |
| `request.data.split_conf_info.out_fee_huifuid` | 手续费外扣汇付ID | `String` | `18` | `N` | 选择手续费外扣时必填；示例值： |
| `request.data.split_conf_info.split_fee_rate` | 手续费% | `String` | `9` | `N` | 开通分账业务时必须填写一种收费方式；百分比，支持两位小数；示例值：1.00 ；分账手续费收取方式为费率手续费与固定手续费之和 |
| `request.data.split_conf_info.per_amt` | 固定手续费 | `String` | `9` | `N` | 开通分账业务时必须填写一种收费方式；单位元，支持小数点后两位；示例值：1.00 ；分账手续费收取方式为费率手续费与固定手续费之和 |
| `request.data.split_conf_info.scene` | 分账模式 | `String` | `2` | `Y` | 00-其他；01-医美医院分账；02-线上其他；A1- 教培机构分账；A2-公办/民办学校分账；A3-医美渠道独立收款分账；A4-线上供应商货款；A5-线上推广方（渠道/代理/个人）的服务佣金/抽成；A7-入驻商户货款；A8-线下供应商货款；A9-线下推广方；A10-个人与合作方分账；单选；示例值：A9 |
| `request.data.split_conf_info.split_ext_info` | 业务情况说明 | `String` | `128` | `N` | jsonObject；分账模式选择则其它，分账比例30%以上必填 |
| `request.data.split_conf_info.split_ext_info.busi_instruction` | *业务模式说明* | `String` | `500` | `Y` | 请详细说明商户的业务模式，包括不限于（业务参与方、各方的权利及义务关系等）。最大500个汉字，必填；示例值：商户向企业采购产品，并将其展示在其电商平台上，用户注册后购买其产品，产品主要有家电、服饰、鞋帽等，用户购买产品的资金作为商户所得，商户根据订单情况进行物流配送。 |
| `request.data.split_conf_info.split_ext_info.capital_instruction` | *资金流向说明* | `String` | `500` | `Y` | 请详细说明商户的资金流向，包括但不限于（交易所涉及的各方账户、资金流入流出过程等）。最大500个汉字，必填；示例值：用户选购产品后根据订单支付给商户，商户根据结算周期，结算到对公账户。 |
| `request.data.split_conf_info.split_ext_info.function_instruction` | *功能开通用途说明* | `String` | `500` | `Y` | 请详述所申请功能的原因、场景、涉及对象类型。最大500个汉字，必填；示例值：企业工资代发 |
| `request.data.delay_flag` | 延迟入账开关 | `String` | `1` | `N` | 选项：N：否 Y：是，默认否；示例值：Y |
| `request.data.forced_delay_flag` | 商户开通强制延迟标记 | `String` | `1` | `N` | 选项：N：否 Y：是，默认否；开关打开后商户所有交易都是延迟交易，需要调用[交易确认接口](http://paas.huifu.com/open/doc/api/#/smzf/api_jyqr)（官网原始地址为非 HTTPS，不得静默改写）完成交易；示例值：Y |
| `request.data.use_chains_flag` | 使用上级微信、支付宝商户号发起交易 | `String` | `8` | `N` | 1是 2 否；示例值：2。；1 微信+支付宝 ；2 不使用 ；3 微信；4 支付宝；使用上级微信、支付宝商户号需对应开通微信、支付宝功能 |
| `request.data.extended_material_list[]` | *补充文件信息* | `String` | `—` | `N` | jsonArray字符串；根据开通的功能补充相关材料，包括[商户纸质协议说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%95%86%E6%88%B7%E5%90%88%E5%90%8C%E7%AD%BE%E7%BA%A6%E8%A7%84%E5%88%99.xlsx)、[线上行业补充材料](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E7%BA%BF%E4%B8%8A%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B%E7%BC%96%E7%A0%81%E5%8F%8A%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E.xlsx)、[开通余额支付补充材料](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E4%BD%99%E9%A2%9D%E6%94%AF%E4%BB%98%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99.xlsx) 、[分账功能提供材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/spin/files/20260611/KYC-%E5%88%86%E8%B4%A6%E5%8A%9F%E8%83%BD%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E%281%29.xlsx) 、[代扣支付补充材料](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/%E4%BB%A3%E6%89%A3%E6%94%AF%E4%BB%98%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99.xlsx) |
| `request.data.extended_material_list[].file_id` | *文件id* | `String` | `64` | `Y` | 请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.extended_material_list[].file_type` | *文件类型* | `String` | `64` | `N` | [参见文件类型说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；示例值：F01 |
| `request.data.agreement_info` | *协议信息实体* | `String` | `—` | `C` | jsonObject字符串；[签约协议材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%95%86%E6%88%B7%E5%90%88%E5%90%8C%E7%AD%BE%E7%BA%A6%E8%A7%84%E5%88%99.xlsx) ；若未签署过协议的情况下，调用该接口时必填；若已签署过纸质或电子协议下，调用该接口时必填，且只可以选择纸质或电子协议；若已签署过挂网协议下，调用该接口时，选填。 |
| `request.data.agreement_info.agreement_type` | *协议类型* | `String` | `1` | `Y` | 0-电子协议 1-纸质协议 3-挂网协议；示例值：3 |
| `request.data.agreement_info.agreement_url` | *挂网协议地址* | `String` | `256` | `C` | 挂网协议必填；**必须按示例值填写**，示例值：https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/PaymentServiceAgreement.htm |
| `request.data.agreement_info.agree_begin_date` | 纸质协议开始日期 | `String` | `8` | `N` | 示例值：20220606 |
| `request.data.agreement_info.agree_end_date` | 纸质协议结束日期 | `String` | `8` | `N` | 示例值：20230606；要求结束时间大于开始时间 |
| `request.data.agreement_info.message_send_type` | 电子协议签约短信发送标识 | `String` | `1` | `N` | 协议类型为电子，业务开通审核通过后发送协议签约短信；0：发送，默认；1：不发送；示例值：1 |
| `request.data.agreement_info.agreement_async_return_url` | 电子协议异步通知地址 | `String` | `128` | `N` | 示例值：http://service.example.com/to/path |
| `request.data.enter_fee` | 开户费用值(元) | `String` | `14` | `N` | 示例值：5.00 |
| `request.data.enter_fee_flag` | 开户费用类型 | `String` | `1` | `N` | 1-一次性开户费，2-平台套餐费（元/年）；示例值：2 |
| `request.data.online_refund` | 是否开通在线退款 | `String` | `1` | `N` | N：否 Y：是；示例值：Y |
| `request.data.platform_refund` | 是否支持平台退款 | `String` | `1` | `N` | N：否 Y：是；示例值：Y |
| `request.data.support_revoke` | 是否支持撤销 | `String` | `1` | `N` | N：否 Y：是；示例值：Y |
| `request.data.async_return_url` | 异步消息接收地址 | `String` | `128` | `N` | 审核消息接收地址，示例值：http://service.example.com/to/path。为空不推送审核消息。 |
| `request.data.busi_async_return_url` | 业务开通结果异步消息接收地址 | `String` | `128` | `N` | 当前申请同步成功或者审核通过之后，格式：消息接收地址，示例值：http://service.example.com/to/path。为空不推送审核消息。 |
| `request.data.recon_resp_addr` | 交易异步应答地址 | `String` | `256` | `N` | 交易异步应答地址；格式：消息接收地址，示例值：http://service.example.com/to/path。为空不推送交易异步消息。 |
| `request.data.uni_app_payment_config` | 银联线上收银台 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.uni_app_payment_config.switch_state` | 状态开关 | `String` | `1` | `N` | 0-关闭; 1-开通, 为空默认开通；示例值：1 |
| `request.data.uni_app_payment_config.debit_fee_rate` | 借记手续费（%） | `String` | `6` | `C` | 借记卡费率与贷记卡费率不能同时为空;；保留2位小数，最大值100.00，最小值0.00；示例值：0.02 |
| `request.data.uni_app_payment_config.credit_fee_rate` | 贷记手续费（%） | `String` | `6` | `C` | 借记卡费率与贷记卡费率不能同时为空;；保留2位小数，最大值100.00，最小值0.00；示例值：0.06 |
| `request.data.uni_app_payment_config.out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；示例值：1 ；如果不为空，则out_fee_acct_type，out_fee_huifuid，out_fee_flag取单独配置，否则取公共配置 |
| `request.data.uni_app_payment_config.out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填；示例值：[官网示例已脱敏] |
| `request.data.uni_app_payment_config.out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户，02-现金户，05-充值户，09-营销户；不填默认01；示例值：01 |
| `request.data.uni_app_payment_config.cloud_quick_pass_secret_free_flag` | 云闪付免密支付开通标识 | `String` | `1` | `N` | Y：是，N：否；示例值：Y |
| `request.data.fund_collection_flag` | 资金归集开通标记 | `String` | `1` | `N` | Y：是，N：否；示例值：Y |
| `request.data.surrogate_config_list[]` | 代发配置 | `String` | `—` | `N` | jsonArray格式字符串 |
| `request.data.surrogate_config_list[].surrogate_type` | 代发业务类型 | `String` | `2` | `Y` | D0:当日到账；T1:下个工作日到账;；D1:下个自然日到账;；示例值：T1 |
| `request.data.surrogate_config_list[].fix_amt` | 手续费（固定/元） | `String` | `17` | `C` | 手续费（固定/元），保留小数点后两位；fee_formula_type为05，06时必填 示例值：1.00 |
| `request.data.surrogate_config_list[].fee_rate` | 手续费（百分比/%） | `String` | `6` | `C` | 手续费（百分比/%），保留小数点后两位；取值范围[0.00,100.00]；fee_formula_type为01，02，03，06时必填 示例值：0.05 |
| `request.data.surrogate_config_list[].out_fee_flag` | 是否交手续费外扣标记 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；优先级高于相同名称的公共参数；示例值：1 |
| `request.data.surrogate_config_list[].out_fee_acct_type` | 交易手续费外扣时账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01；优先级高于相同名称的公共参数 |
| `request.data.surrogate_config_list[].out_fee_huifu_id` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填，示例值：[官网示例已脱敏]；优先级高于相同名称的公共参数 |
| `request.data.surrogate_config_list[].surrogate_private_flag` | 是否允许对私代发 | `String` | `1` | `N` | 是否允许代发卡为对私类型；Y:允许 N:不允许；示例值：Y |
| `request.data.surrogate_config_list[].fee_formula_type` | 代发手续费计费模式 | `String` | `8` | `N` | 01: 百分比手续费，无封顶值或保底值；02: 百分比手续费，有保底值；03: 百分比手续费，有封顶值；05: 固定手续费 ；06: 固定手续费+百分比手续费；为空默认06 示例值：06 |
| `request.data.surrogate_config_list[].fee_max_amt` | 手续费封顶值（固定/元） | `String` | `17` | `C` | 手续费封顶值（固定/元），保留小数点后两位；fee_formula_type为03时必填 示例值：100.00 |
| `request.data.surrogate_config_list[].fee_min_amt` | 手续费保底值（固定/元） | `String` | `17` | `C` | 手续费保底值（固定/元），保留小数点后两位；fee_formula_type为02时必填 示例值：1.00 |
| `request.data.large_amt_pay_config` | 大额支付配置 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[]` | 大额支付配置列表 | `String` | `—` | `Y` | 大额支付配置列表，jsonArray格式 |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].switch_state` | 功能开关 | `String` | `1` | `N` | 1:开通 0:关闭 默认：1；示例值：1 |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].business_model` | 大额支付业务模式 | `String` | `15` | `Y` | 大额支付业务模式 bank：银行模式 provisions：备付金模式；示例值：bank |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].fee_rate` | 费率（%） | `String` | `6` | `C` | 开通大额业务时必须填写一种收费方式；大于0,保留2位小数；示例值：1.00 |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].fee_fix_amt` | 交易手续费（固定/元） | `String` | `9` | `C` | 开通大额业务时必须填写一种收费方式；大于0,保留2位小数；示例值：10.00 |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].biz_type` | 大额调账标识申请类型 | `String` | `2` | `N` | 01-四要素，05-三要素；[订单匹配的要素信息](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_ddppys)；示例值：05 |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].mer_same_card_recharge_flag` | 是否允许绑卡支付 | `String` | `1` | `N` | Y-开通/N-关闭，备付金模式时，支持传入；备付金模式银行卡绑定支付权限；示例值：Y |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].allow_user_deposit_flag` | 是否允许用户入账 | `String` | `1` | `N` | Y-开通/N-关闭 ；默认为N；示例值：Y |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].provisions_auto_refund_flag` | 备付金固定账号模式自动退款 | `String` | `1` | `N` | Y-开通/N-关闭 ；示例值：Y；该配置仅在开通大额支付备付金绑卡模式时生效 |
| `request.data.large_amt_pay_config.out_fee_flag` | 交易手续费外扣标记 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；示例值：1 |
| `request.data.large_amt_pay_config.out_fee_huifu_id` | 交易手续费外扣huifuId | `String` | `18` | `C` | 交易手续费外扣时必填；示例值：[官网示例已脱敏] |
| `request.data.large_amt_pay_config.out_fee_acct_id` | 交易手续费外扣账户号 | `String` | `16` | `C` | 交易手续费外扣时必填；示例值：F00598602 |
| `request.data.large_amt_pay_config.mer_payer_card_type` | 商户付款方卡类型 | `String` | `10` | `N` | CORPORATE-对公,PRIVATE-对私,ALL-全部，默认全部；示例值：ALL |
| `request.data.half_pay_host_flag` | 统一收银台开关 | `String` | `1` | `N` | Y:是 N:否（为空默认未开通） ；示例值：Y |
| `request.data.agent_recheck_config` | 代发复核配置 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.agent_recheck_config.agent_recheck_flag` | 代发复核开关 | `String` | `1` | `N` | Y:是 N:否（为空默认未开通） ；示例值：Y |
| `request.data.agent_recheck_config.agent_recheck_huifu_id` | 复核授权商户号 | `String` | `18` | `N` | 复核授权商户号只能填当前商户主体或总部商户号 |
| `request.data.agent_recheck_config.agent_recheck_type` | 复核类型 | `String` | `1` | `N` | A:复核 B:短信验证 |
| `request.data.online_recharge_flag` | 商户开通网银充值开关 | `String` | `1` | `N` | Y:是 N:否 ；示例值：Y |
| `request.data.refund_mend_open_flag` | 是否开通垫资退款 | `String` | `1` | `N` | Y:是 N:否 ；示例值：Y |
| `request.data.jxf_conf_info` | 捷行付配置 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.jxf_conf_info.default_channel` | 默认通道 | `String` | `—` | `C` | 1-银行通道 2-微信企业码 |
| `request.data.jxf_conf_info.jxf_bank_pay_info` | 银行模式配置 | `Object` | `—` | `C` | 银行模式专属配置 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.acct_type` | 账户类型 | `String` | `1` | `Y` | 2:银行账户 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.bank_name` | 银行名称 | `String` | `8` | `Y` | PINGAN-平安银行；示例值：PINGAN |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info` | 银行账户信息 | `Object` | `—` | `C` | 当账户类型为银行账户时必填 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.user_name` | 操作人姓名 | `String` | `16` | `C` | 银行名称非平安银行时，需填写；示例：张三 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.operator_phone` | 操作人手机号 | `String` | `11` | `C` | 银行名称非平安银行时，需填写；示例：[官网示例已脱敏] |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.acct_type` | 付款方账户类型 | `String` | `2` | `N` | 00：单位结算卡，不填默认单位结算卡 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.acct_no` | 付款方账号 | `String` | `50` | `Y` | 示例：[官网示例已脱敏] |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.acct_name` | 付款方账户名称 | `String` | `25` | `Y` | 示例：上海汇付支付有限公司 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.bank_branch_code` | 开户行联行号 | `String` | `50` | `Y` | 示例：991290000099 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.bank_branch_name` | 开户行行名 | `String` | `25` | `Y` | 示例：中国银行 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.sign_start_date` | 签约申请生效日期 | `String` | `8` | `C` | 银行名称非平安银行时，需填写；示例：20251219 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.sign_end_date` | 签约申请失效日期 | `String` | `8` | `C` | 银行名称非平安银行时，需填写；示例：20261219 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.remark` | 附言 | `String` | `128` | `N` | 示例：附言 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.org_code` | 机构编码 | `String` | `64` | `Y` | 示例：12133 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info` | 手续费信息 | `Object` | `—` | `N` | jsonObject字符串 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.open_card_fix_fee` | 虚拟卡开卡手续费（元） | `String` | `11` | `N` | 单位元，支持小数点后两位；示例值：1.00 虚拟卡开卡手续费收取方式为发放数量*固定手续费 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.quota_issue_fee_rate` | 虚拟卡额度发放手续费（%） | `String` | `6` | `N` | 百分比，支持两位小数；示例值：1.00 虚拟卡发放额度手续费收取方式为交易金额*费率手续费 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.out_fee_flag` | 捷行付手续费内外扣标记 | `String` | `1` | `N` | 捷行付手续费只支持外扣；1:外扣；示例值：1 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.out_fee_huifuid` | 捷行付手续费外扣汇付ID | `String` | `18` | `C` | 捷行付设置手续费时必填；示例值：[官网示例已脱敏] |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.out_fee_acct_type` | 捷行付手续费扣款账户类型 | `String` | `2` | `C` | 捷行付手续费外扣时必填；01-基本户(默认)，05-充值户；示例值：01 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.pay_confirm_flag` | 付款确认标识 | `String` | `1` | `N` | Y:是 N:否 ；示例值：Y |
| `request.data.jxf_conf_info.jxf_bank_pay_info.pay_confirm_req_url` | 付款确认请求URL | `String` | `256` | `C` | 付款确认标识为Y时，该字段必填 |
| `request.data.jxf_conf_info.wx_ent_pay_info` | 微信企业码模式配置 | `Object` | `—` | `C` | 微信企业码模式配置 |
| `request.data.jxf_conf_info.wx_ent_pay_info.payment_background` | 付款背景介绍 | `String` | `512` | `Y` | 付款背景介绍 |
| `request.data.jxf_conf_info.wx_ent_pay_info.apply_scenes` | 适用场景 | `String` | `25` | `Y` | 适用场景，多选逗号分隔 1-企业差旅 2-因公宴请 3-会员积分 4-小额采购 5-商报直付 |
| `request.data.jxf_conf_info.wx_ent_pay_info.sub_mch_id` | 微信商户号 | `String` | `32` | `N` | 微信商户号（出资子商户号） |
| `request.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info` | 微信企业码手续费信息 | `Object` | `—` | `Y` | 微信企业码手续费信息 |
| `request.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.open_card_fix_fee` | 虚拟卡开卡手续费（元） | `String` | `11` | `N` | 单位元，支持小数点后两位；示例值：1.00 虚拟卡开卡手续费收取方式为发放数量*固定手续费 |
| `request.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.quota_issue_fee_rate` | 虚拟卡额度发放手续费（%） | `String` | `6` | `N` | 百分比，支持两位小数；示例值：1.00 虚拟卡发放额度手续费收取方式为交易金额*费率手续费 |
| `request.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.out_fee_flag` | 捷行付手续费内外扣标记 | `String` | `1` | `N` | 捷行付手续费只支持外扣；1:外扣；示例值：1 |
| `request.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.out_fee_huifuid` | 捷行付手续费外扣汇付ID | `String` | `18` | `C` | 捷行付设置手续费时必填；示例值：[官网示例已脱敏] |
| `request.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.out_fee_acct_type` | 捷行付手续费扣款账户类型 | `String` | `2` | `C` | 捷行付手续费外扣时必填；01-基本户(默认)，05-充值户；示例值：01 |
| `request.data.merge_pay_config_info` | 合单支付配置信息 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.merge_pay_config_info.merge_pay_flag` | 合单支付开关 | `String` | `1` | `Y` | 合单支付开关 Y：开通 N：关闭 |
| `request.data.merge_pay_config_info.merge_pay_config` | 请求流水号 | `Object` | `—` | `C` | 合单支付配置 （当合单支付开关为开时必填） |
| `request.data.merge_pay_config_info.merge_pay_config.merge_pay_mode` | 合单支付模式 | `String` | `1` | `Y` | 1:电商 2:加油站 3:停车场 4:物业 5:休闲娱乐（不同模式需上传不同材料信息，调用图片上传接口；若选择电商，需上传文件F673《电商平台商家入驻协议》、F674《商家入驻截图》，以及填写线上业务类型编码及运营媒介字段信息；若选择加油站，需上传文件F676《加油站与任一合单参与方合作协议》、F675《任一合单参与方经营照片》；若选择停车场，需上传文件F677《停车场与任一合单参与方合作协议》、F675《任一合单参与方经营照片》；若选择物业需上传文件F678《物业与任一合单参与方合作协议》、F675《任一合单参与方经营照片》；若选择休闲娱乐需上传文件F679《休娱与任一合单参与方合作协议》、F675《任一合单参与方经营照片》） |
| `request.data.bill_payment_flag` | 是否开通账单支付 | `String` | `1` | `N` | Y:是 N:否 ；示例值：Y |
| `request.data.withhold_pay_scene` | 代扣场景 | `String` | `1` | `C` | withhold_flag开通需填写 1:权益投流(订阅),2:非权益投流(订阅),3:保险缴纳,4:道路通行费(ETC),5:公共事业(水电煤)缴费,6:物业缴费 |
| `request.data.recon_resp_sys_id` | 交易应答返回推送系统号 | `String` | `32` | `N` | 交易应答返回推送系统号；示例值：[官网示例已脱敏] |
| `request.data.dy_conf_list[]` | 抖音配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.dy_conf_list[].fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字格式，大于等于0，保留2位小数；示例值：0.38 |
| `request.data.dy_conf_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `9` | `N` | 金额保留2位小数；大于0。需要渠道商开通此功能。示例值：0.38 |
| `request.data.dy_conf_list[].out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣），示例值：1 |
| `request.data.dy_conf_list[].out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通抖音支付手续费外扣业务时必填，示例值：[官网示例已脱敏] |
| `request.data.dy_conf_list[].out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| `response.data.resp_desc` | 业务返回描述 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| `response.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原样返回请求参数的请求流水号；示例值：[官网示例已脱敏] |
| `response.data.req_date` | 请求时间 | `String` | `8` | `Y` | 原请求时间yyyyMMdd；示例值：20220912 |
| `response.data.product_id` | 产品号 | `String` | `32` | `Y` | 返回审核中时有值，汇付分配的产品号，示例值：YYZY |
| `response.data.huifu_id` | 商户号 | `String` | `18` | `Y` | 返回审核中时有值，汇付分配的商户号，示例值：[官网示例已脱敏] |
| `response.data.apply_no` | 申请单号 | `String` | `18` | `Y` | 返回审核中时有值，汇付返回商户的业务申请单号；示例值：202209120038432 |

### 申请审核异步信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.audit.resp_code` | 网关返回码 | `String` | `6` | `Y` | [网关返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%e7%bd%91%e5%85%b3%e8%bf%94%e5%9b%9e%e7%a0%81) |
| `async.audit.resp_desc` | 网关返回描述 | `String` | `512` | `Y` | 网关返回描述 |
| `async.audit.sign` | 签名 | `String` | `512` | `Y` | 签名，对报文整体签名 |
| `async.audit.data` | 业务返回参数 | `String` | `—` | `N` | JSON |

### 申请审核异步 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.audit.data.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| `async.audit.data.sub_resp_desc` | 业务返回描述 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| `async.audit.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原请求流水号；示例值：[官网示例已脱敏] |
| `async.audit.data.req_date` | 请求日期 | `String` | `8` | `Y` | 原请求日期；示例值：20220912 |
| `async.audit.data.audit_status` | 审核结果 | `String` | `1` | `Y` | P:审核中 Y：审核通过 N：审核拒绝 F：失败 C：拒签；示例值：Y |
| `async.audit.data.audit_desc` | 审核描述 | `String` | `256` | `N` | 审核结果描述 |
| `async.audit.data.product_id` | 产品号 | `String` | `32` | `Y` | 返回：处理成功时有值，汇付分配的产品号，示例值：YYZY |
| `async.audit.data.huifu_id` | 商户号 | `String` | `18` | `Y` | 返回：处理成功时有值，汇付分配的商户号，示例值：[官网示例已脱敏] |
| `async.audit.data.apply_no` | 申请单号 | `String` | `18` | `Y` | 返回：处理成功时有值，汇付返回商户的业务申请单号；示例值：202209120038432 |

### 逐业务结果异步

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.business.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | 业务返回码 |
| `async.business.sub_resp_desc` | 业务返回描述 | `String` | `512` | `Y` | 业务返回描述 |
| `async.business.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原请求流水号；示例值：[官网示例已脱敏] |
| `async.business.req_date` | 请求日期 | `String` | `8` | `Y` | 原请求日期yyyyMMdd；示例值：20220912 |
| `async.business.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：YYZY |
| `async.business.huifu_id` | 商户号 | `String` | `18` | `Y` | 汇付分配的商户号，示例值：[官网示例已脱敏] |
| `async.business.apply_no` | 申请单号 | `String` | `18` | `N` | 汇付返回商户的业务申请单号；示例值：202209120038432 |
| `async.business.notify_type` | 通知类型 | `String` | `1` | `Y` | W:微信，A：支付宝，Y:抖音，U:银联二维码，B:刷卡，E:全域资金管理，J:大额转账备付金模式，I:大额转账银行模式；示例值：W |
| `async.business.reg_result_list[]` | 入驻结果集合 | `String` | `—` | `N` | jsonArray格式；notify_type一种类型返回一条异步消息 |
| `async.business.reg_result_list[].sub_mer_id` | 二级商户号 | `String` | `32` | `N` | 银联商户号或者微信/支付宝二级商户号；当notify_type是W/A时返回示例值：A[官网示例已脱敏] |
| `async.business.reg_result_list[].bank_channel_no` | 渠道号 | `String` | `50` | `N` | 示例值：JP00001；当notify_type是W/A时返回 |
| `async.business.reg_result_list[].bank_mer_code` | 真实商户号 | `String` | `20` | `N` | 示例值：[官网示例已脱敏]；当notify_type是W/A时返回 |
| `async.business.reg_result_list[].electron_bank_name` | 电子账户开户行 | `String` | `32` | `N` | 全域资金管理电子账户开户行, 当notify_type是E时返回；示例值：武汉众邦银行股份有限公司 |
| `async.business.reg_result_list[].electron_account` | 电子账号 | `String` | `32` | `N` | 全域资金管理电子账号, 当notify_type是E时返回；示例值：[官网示例已脱敏] |
| `async.business.reg_result_list[].pay_scene` | 费率类型 | `String` | `2` | `N` | 请求参数pay_scene；当notify_type是W/A时返回；参见《[微信支付场景](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e6%94%af%e4%bb%98%e5%9c%ba%e6%99%af)》说明；示例值：1 |
| `async.business.reg_result_list[].business_stat` | 业务开通状态 | `String` | `1` | `Y` | S-成功，F-失败；当notify_type是W/A/E时返回；示例值：S |
| `async.business.reg_result_list[].business_desc` | 业务开通描述 | `String` | `200` | `N` | 业务开通描述；当notify_type是W/A/E时返回 |
| `async.business.reg_result_list[].real_name_applyment_stat` | 实名认证状态 | `String` | `64` | `N` | W:微信 A：支付宝 申请实名时返回；A：支付宝对应值；审核中(AUDITING)；待联系人确认(CONTACT_CONFIRM)；待法人确认(LEGAL_CONFIRM)；审核通过(AUDIT_PASS)；审核失败(AUDIT_REJECT)；已冻结(AUDIT_FREEZE)；已撤回(CANCELED)；未申请(NOT_APPLY)；W:微信对应值；APPLYMENT_STATE_EDITTING--【编辑中】--可能在提交申请时发生错误导致，可用同一个业务申请编号重新提交；APPLYMENT_STATE_WAITTING_FOR_AUDIT--【审核中】--请耐心等待1~2个工作日，微信支付将会完成审核；APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT--【待确认联系信息】--请扫描微信支付返回的小程序码确认联系信息(此过程可修改超级管理员手机号)；APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON--【待账户验证】--请扫描微信支付返回的小程序码在小程序端完成账户验证；APPLYMENT_STATE_PASSED--【审核通过】--请扫描微信支付返回的小程序码在小程序端完成授权流程；APPLYMENT_STATE_REJECTED--【审核驳回】--请按照驳回原因修改申请资料，并更换业务申请编码，重新提交申请；APPLYMENT_STATE_FREEZED--【已冻结】--可能是该主体已完成过入驻，请查看驳回原因，并通知驳回原因中指定的联系人扫描微信支付返回的小程序码在小程序端完成授权流程；APPLYMENT_STATE_CANCELED--【已作废】--表示申请单已被撤销，无需再对其进行操作；APPLYMENT_STATE_NOAPPLY--未申请；示例值：AUDITING |
| `async.business.reg_result_list[].real_name_applyment_desc` | 实名认证描述 | `String` | `128` | `N` | W:微信 A：支付宝 申请实名时返回；示例值：W |
| `async.business.reg_result_list[].qrcode_data` | 授权二维码 | `String` | `512` | `N` | W:微信 A：支付宝 申请实名时返回；若notify_type=W时 且 实名认证状态 real_name_applyment_stat=；APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT、；APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON、；APPLYMENT_STATE_PASSED、；APPLYMENT_STATE_FREEZED时返回；若notify_type=A时 且 实名认证状态 real_name_applyment_stat=；CONTACT_CONFIRM、LEGAL_CONFIRM时返回；示例值：https://qr.alipay.com/bax02911brluc2xieoph6001 |
| `async.business.reg_result_list[].agreement_link` | 协议签署连接 | `String` | `1024` | `N` | 申请实名且签署电子协议时返回；示例值： |
| `async.business.reg_result_list[].agreement_id` | 协议编号 | `String` | `64` | `N` | 申请实名且签署电子协议时返回；示例值： |
| `async.business.reg_result_list[].agreement_name` | 协议名称 | `String` | `256` | `N` | 申请实名且签署电子协议时返回；示例值： |
| `async.business.zl_async_info` | 直连结果合集 | `String` | `512` | `N` | 直连微信/支付宝结果合集 |
| `async.business.zl_async_info.sub_mch_id` | 支付宝/微信商户号 | `String` | `32` | `N` | 示例值：1632157057 |
| `async.business.zl_async_info.apply_type` | 申请类型 | `String` | `32` | `N` | 示例值：FACE_TO_FACE |
| `async.business.zl_async_info.apply_state` | 申请单状态 | `String` | `1` | `N` | S：审核通过，P：审核中，N：审核拒绝，F：系统处理失败；新增状态枚举：C：待签约 |
| `async.business.zl_async_info.mer_app_id` | 应用ID | `String` | `32` | `N` | 示例值：wx51aa91a575359ff5 |
| `async.business.zl_async_info.confirm_url` | 签约链接 | `String` | `256` | `N` | 示例值：https://www.huifu.com |
| `async.business.zl_async_info.reject_reason` | 拒绝原因 | `String` | `128` | `N` | 示例值：支付功能未开通 |
| `async.business.ord_id` | 通知流水号 | `String` | `44` | `N` | 回调方返回应答，应答内容为：”[RECV_ORD_ID_](https://spin.cloudpnr.com/topds/regMerBusiInfo.html#id19)”+该ordId |

### 电子协议异步

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.agreement.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | 业务返回码 |
| `async.agreement.sub_resp_desc` | 业务返回描述 | `String` | `512` | `N` | 业务返回描述 |
| `async.agreement.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原请求流水号；示例值：[官网示例已脱敏] |
| `async.agreement.req_date` | 请求日期 | `String` | `8` | `Y` | 请求日志 |
| `async.agreement.huifu_id` | 商户号 | `String` | `18` | `Y` | 商户号 |
| `async.agreement.apply_no` | 申请单号 | `String` | `18` | `Y` | 业务申请单号 |
| `async.agreement.agreement_info_list` | 协议信息 | `String` | `—` | `N` | 签署电子协议时返回 |
| `async.agreement.agreement_info_list.agreement_type` | 协议类型 | `String` | `1` | `N` | 0-电子协议 |
| `async.agreement.agreement_info_list.agreement_link` | 协议签署链接 | `String` | `512` | `N` | 协议签署链接 |
| `async.agreement.agreement_info_list.agreement_no` | 协议号 | `String` | `32` | `N` | 示例值：3245234 |
| `async.agreement.agreement_info_list.agreement_name` | 协议名称 | `String` | `128` | `N` | 协议名称 |
| `async.agreement.agreement_info_list.con_stat` | 合同状态 | `String` | `2` | `N` | 电子协议类型会返回以下值： 2：创建合同异常 3：待签约 4：签约中 5：签约完成(电子协议只有签约完成才能做交易) 6：已失效 7：已拒签 8：签约失败 示例值：5 |

## 图片上传

- 原始地址：<https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json>
- SHA-256：`2fcb84dd1cfe0260cfa3d49b79174d2e7b8a287cdf860faa62011bfc1e8472dd`
- URI：`v2/supplementary/picture`；接口元数据 `sign=true`。官方 JSON 未给 HTTP method、host 或 Content-Type。
- 官方 JSON 未定义响应字段；不得猜测 `file_id`、其他响应路径或重试语义。

### 请求信封与 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | — | `—` | `—` | `—` | 仅见于 `requestDemo`；官方 JSON 未给正式顶层 schema。 |
| `request.product_id` | — | `—` | `—` | `—` | 仅见于 `requestDemo`；官方 JSON 未给正式顶层 schema。 |
| `request.data` | — | `—` | `—` | `—` | 仅见于 `requestDemo`；`requestBody.params` 定义下列五个 data 字段。 |
| `request.data.req_seq_id` | 业务请求流水号 | `String` | `32` | `Y` | 业务请求流水号；示例值：[官网示例已脱敏] |
| `request.data.req_date` | 业务请求日期 | `String` | `8` | `Y` | 日期格式:yyyyMMdd;示例值：20220915 |
| `request.data.file_type` | 图片类型 | `String` | `32` | `Y` | 具体取值请参考各接口文档中的字段说明。；[枚举取值表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；示例值：F01 |
| `request.data.huifu_id` | 商户号 | `String` | `18` | `N` | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] ；如果商户未开户没有商户号，可以为空。；不支持"企业用户基本信息开户"和"个人用户基本信息开户"接口所返回的用户号 |
| `request.data.file_url` | 文件url链接文件url链接与file文件流不能同时上传；文件支持类型：JPG,BMP,PNG；单个图片最大支持2M；除去图片外其他类型文件支持10M；示例值：[官网示例图片已省略] | `String` | `512` | `C` | 文件url链接与file文件流不能同时上传；文件支持类型：JPG,BMP,PNG；单个图片最大支持2M；除去图片外其他类型文件支持10M；示例值：[官网示例图片已省略] |

## 商户详细信息查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md>
- SHA-256：`3fb7115e030937181c3040f8d57c16ce8b44aa75fb78849d950af8816fc0a918`
- 说明：下表保留官方字段类型、长度、必填标记和字段说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商或商户的huifu_id；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为总部商户时，此字段填写商户huifu_id |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/docs/start/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/docs/start/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号，同一商户号当天唯一；示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd，以北京时间为准；示例值：20220125 |
| `request.data.huifu_id` | 汇付客户Id | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] |

### 响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务返回描述 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.product_id` | 产品号 | `String` | `32` | `N` | 汇付分配的产品号，示例值：MCS |
| `response.data.upper_huifu_id` | 直属渠道号 | `String` | `18` | `N` | 该商户进件完成后隶属的渠道商号； 非直营商户时有值。示例值：[官网示例已脱敏] |
| `response.data.ext_mer_id` | 外部商户号 | `String` | `64` | `N` | 支持关联外部商户系统中的商户号；示例值：HF100001 |
| `response.data.reg_name` | 商户注册名称 | `String` | `128` | `Y` | 1.商户名称必须与商家证照上的名称一致；2. 若个体工商户证照没有商家名称或者名称为“\*”或者“” 则商户名称应填 “个体户XXX”（XXX为营业执照上经营者姓名）当为汉字时，以2个字符计算；示例值：上海汇付支付服务有限公司 |
| `response.data.short_name` | 商户简称 | `String` | `32` | `Y` | 商户经营简称；示例值：汇付支付 |
| `response.data.receipt_name` | 小票名称 | `String` | `50` | `N` | 可以作为POS小票的名称，企业商户有值；示例值：汇付支付 |
| `response.data.mer_en_name` | 商户英文名称 | `String` | `256` | `N` | 商户英文名称；示例值：Shanghai Huifu Payment Co. Ltd. |
| `response.data.remarks` | 备注 | `String` | `300` | `N` | 备注内容；示例值：华东分公司 |
| `response.data.cust_type` | 商户类型 | `String` | `1` | `Y` | 1：企业 2：个人 ；示例值：1 |
| `response.data.ent_type` | 商户种类 | `String` | `1` | `Y` | 1：政府机构、2：国营企业、3：私营企业、4：外资企业、5：个体工商户、6：其他组织、7：事业单位、9：业主委员会；示例值：3 |
| `response.data.busi_type` | 经营类型 | `String` | `1` | `N` | 1:实体 2:虚拟，企业商户有值；示例值：1 |
| `response.data.mcc` | 所属行业（MCC） | `String` | `7` | `N` | [银联MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylmccbm)，企业商户有值；示例值：5411 |
| `response.data.license_type` | 证照类型 | `String` | `32` | `N` | 参见[机构证照类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E6%9C%BA%E6%9E%84%E8%AF%81%E7%85%A7%E7%B1%BB%E5%9E%8B)说明； 示例值：NATIONAL_LEGAL |
| `response.data.license_code` | 营业执照编号 | `String` | `18` | `N` | 工商营业执照编号，示例值：92650109MA79R8E308 |
| `response.data.license_validity_type` | 证照有效期类型 | `String` | `1` | `N` | 企业类商户有值，1:长期有效 0:非长期有效；示例值：0 |
| `response.data.license_begin_date` | 证照开始日期 | `String` | `8` | `N` | 企业类商户有值，格式yyyyMMdd，示例值:20220125，以北京时间为准; |
| `response.data.license_end_date` | 证照结束日期 | `String` | `8` | `N` | 企业类商户有值，格式yyyyMMdd，示例值:20250125，以北京时间为准；“29991231“或”99991231”代表长期 |
| `response.data.reg_prov_id` | 注册省 | `String` | `6` | `N` | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000；与证照保持一致 |
| `response.data.reg_area_id` | 注册市 | `String` | `6` | `N` | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310100；与证照保持一致 |
| `response.data.reg_district_id` | 注册区 | `String` | `6` | `N` | 参考[地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) ；示例值：310101；与证照保持一致 |
| `response.data.reg_detail` | 注册详细地址 | `String` | `256` | `N` | 与证照保持一致；示例值：上海市徐汇区XX路XX号 |
| `response.data.prov_id` | 银行所在省 | `String` | `6` | `N` | [地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310000 |
| `response.data.area_id` | 银行所在市 | `String` | `6` | `N` | [地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310100 |
| `response.data.district_id` | 经营地址所在区县 | `String` | `6` | `N` | [地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)示例值：310101 |
| `response.data.detail_addr` | 商户经营详细地址 | `String` | `256` | `N` | 企业商户有值；示例值：上海市徐汇区XX路XX号 |
| `response.data.legal_name` | 法人姓名 | `String` | `32` | `N` | 支持少数名族,最大支持10个汉字；示例值：张三 |
| `response.data.legal_cert_type` | 法人证件类型 | `String` | `2` | `N` | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》 说明；示例值：00 |
| `response.data.legal_cert_no` | 法人证件号码 | `String` | `40` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.legal_cert_validity_type` | 法人证件有效期类型 | `String` | `1` | `N` | 1:长期有效 0:非长期有效，示例值：0 |
| `response.data.legal_cert_begin_date` | 法人证件有效期开始日期 | `String` | `8` | `N` | yyyyMMdd，示例值:20220125，以北京时间为准 |
| `response.data.legal_cert_end_date` | 法人证件有效期结束日期 | `String` | `8` | `N` | yyyyMMdd，示例值:20220125，以北京时间为准。当法人证件有效期类型为0 |
| `response.data.legal_mobile_no` | 法人手机号 | `String` | `11` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.legal_addr` | 法人身份证地址 | `String` | `256` | `N` | 示例值：上海市徐汇区宜山路700号普天信息产业园2期C5栋 |
| `response.data.occupation` | 负责人职业 | `String` | `2` | `N` | 1A：各类专业,技术人员；1B：国家机关,党群组织,企事业单位的负责人；1C：办事人员和有关人员；1D：商业工作人员；1E：服务性工作人员；1F：农林牧渔劳动者；1G：生产工作,运输工作和部分体力劳动者；1H：不便分类的其他劳动者；示例值：1G |
| `response.data.beneficiary_info_list[]` | 受益人信息实体 | `String` | `—` | `N` | jsonArray字符串 |
| `response.data.beneficiary_info_list[].bo_id` | 受益人唯一ID | `String` | `32` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.beneficiary_info_list[].bo_name` | 受益人名称 | `String` | `40` | `N` | 示例值：张三 |
| `response.data.beneficiary_info_list[].bo_type` | 受益人证件类型 | `String` | `2` | `N` | 00:身份证； 01:护照； 02:军官证； 03:士兵证； 04:回乡证； 05:户口本； 06:外国护照； 07:其他； 08:暂住证； 09:警官证； 10:文职干部证； 11:港澳同胞回乡证； 12:营业执照；示例值：00 |
| `response.data.beneficiary_info_list[].bo_no` | 受益人证件号 | `String` | `50` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.beneficiary_info_list[].bo_date_start` | 受益人证件有效期开始时间 | `String` | `8` | `N` | 示例值：20210606 |
| `response.data.beneficiary_info_list[].bo_dead_line` | 受益人证件有效期结束时间 | `String` | `8` | `N` | 示例值：20290606；若证件有效期为长期，请填写：29991231；要求结束时间大于开始时间 |
| `response.data.beneficiary_info_list[].bo_address` | 受益人地址 | `String` | `500` | `N` | 示例值：上海徐汇区共富一路55号401室 |
| `response.data.beneficiary_info_list[].bo_mobile_no` | 受益人手机号 | `String` | `11` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.beneficiary_info_list[].final_beneficiary_mode` | 最终受益人受益方式 | `String` | `3` | `N` | A01：直接或间接控股25%（含）以上 ；A02：通过人事、财务等其他方式对公司进行控制 ；A03：高级管理人员 ；A04：法人或公司负责人 ；A05：其他；示例值：A01 |
| `response.data.beneficiary_info_list[].bo_stat` | 受益人有效标识 | `String` | `10` | `N` | active：有效，inactive：无效 示例值：active |
| `response.data.contact_name` | 管理员姓名 | `String` | `30` | `N` | 商户联系人姓名。支持少数名族,最大支持15个汉字；示例值：张三 |
| `response.data.contact_mobile_no` | 管理员手机号 | `String` | `11` | `N` | 手机号格式；示例值：[官网示例已脱敏] |
| `response.data.contact_email` | 管理员邮箱 | `String` | `40` | `N` | 邮箱格式；示例值：carl.chen@huifu.com |
| `response.data.service_phone` | 客服电话 | `String` | `32` | `N` | 支持固话格式，手机格式；示例值：021-8888888 |
| `response.data.login_name` | 管理员账号 | `String` | `32` | `N` | 自定义值，必须全系统唯一；作为控台的登陆用户名或POS机的登陆用户名；示例值：cwdsd1001 |
| `response.data.sms_send_flag` | 注册短信发送标记 | `String` | `1` | `N` | Y:已发送,N:未发送；示例值：Y |
| `response.data.mer_url` | 商户主页URL | `String` | `256` | `N` | 商户主页URL； 示例值：https://www.huifu.com/home/ |
| `response.data.mer_icp` | 商户ICP备案编号 | `String` | `50` | `N` | 商户ICP备案编号；示例值：沪ICP备06046402号-28 |
| `response.data.open_licence_no` | 开户许可证核准号 | `String` | `32` | `N` | 示例值：J2900123456789 |
| `response.data.qry_cash_card_info_list[]` | 卡信息 | `String` | `—` | `N` | jsonArray格式字符串 |
| `response.data.qry_cash_card_info_list[].card_type` | 卡类型 | `String` | `1` | `N` | 0:对公 1:对私；示例值：0 |
| `response.data.qry_cash_card_info_list[].card_name` | 卡户名 | `String` | `256` | `N` | 银行账户准确名称；示例值：上海汇付支付服务有限公司 |
| `response.data.qry_cash_card_info_list[].card_no` | 卡号 | `String` | `32` | `N` | 示例值：32453653455 |
| `response.data.qry_cash_card_info_list[].prov_id` | 银行所在省 | `String` | `6` | `N` | [地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310000 |
| `response.data.qry_cash_card_info_list[].area_id` | 银行所在市 | `String` | `6` | `N` | [地区码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310100 |
| `response.data.qry_cash_card_info_list[].bank_code` | 银行号 | `String` | `8` | `N` | 参考： [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm) 示例值：01020000 |
| `response.data.qry_cash_card_info_list[].bank_name` | 银行名称 | `String` | `32` | `N` | 示例值：中国工商银行 |
| `response.data.qry_cash_card_info_list[].branch_code` | 支行联行号 | `String` | `12` | `N` | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm) 对公结算有值，对私结算不一定有值；示例值：102290026507 |
| `response.data.qry_cash_card_info_list[].branch_name` | 支行名称 | `String` | `64` | `N` | 对公结算有值；示例值：中国工商银行上海市中山北路支行 |
| `response.data.qry_cash_card_info_list[].cert_type` | 持卡人证件类型 | `String` | `2` | `N` | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》说明；示例值：00 |
| `response.data.qry_cash_card_info_list[].cert_no` | 持卡人证件号码 | `String` | `32` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.qry_cash_card_info_list[].cert_validity_type` | 持卡人证件有效期类型 | `String` | `1` | `N` | 1:长期有效 0:非长期有效；示例值：0 |
| `response.data.qry_cash_card_info_list[].cert_begin_date` | 持卡人证件有效期开始日期 | `String` | `8` | `N` | 对私结算有值，持卡人证件有效期开始日期yyyyMMdd， 示例值：20220125 ，以北京时间为准 |
| `response.data.qry_cash_card_info_list[].cert_end_date` | 持卡人证件有效期截止日期 | `String` | `8` | `N` | 对私结算有值，持卡人证件有效期开始日期yyyyMMdd， 示例值：20220125 ，以北京时间为准。证件类型长期有效时为空 |
| `response.data.qry_cash_card_info_list[].mp` | 结算人手机号 | `String` | `11` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.qry_cash_card_info_list[].status` | 银行卡绑定状态 | `String` | `1` | `N` | N:正常 C:关闭；示例值：N |
| `response.data.qry_cash_card_info_list[].token_no` | 绑卡序列号 | `String` | `20` | `N` | 示例值：0097387899 |
| `response.data.qry_cash_card_info_list[].is_settle_default` | 默认结算卡标志 | `String` | `1` | `N` | 是否为默认结算卡标志；Y:是 N:否；示例值：Y |
| `response.data.qry_cash_config_list[]` | 取现配置列表 | `String` | `—` | `N` | jsonArray格式字符串 |
| `response.data.qry_cash_config_list[].cash_type` | 业务类型 | `String` | `2` | `N` | D0:当日到账；当日交易资金当天可取现到账；T1:下个工作日到账;；D1:下个自然日到账;；DM：当日到账；到账资金不包括当天的交易资金；示例值：T1 |
| `response.data.qry_cash_config_list[].switch_state` | 开关状态 | `String` | `1` | `N` | 0:关闭 1:开通；示例值：1 |
| `response.data.qry_cash_config_list[].fix_amt` | 提现手续费（固定/元） | `String` | `6` | `C` | fix_amt与fee_rate至少填写一项， 需保留小数点后两位，不收费请填写0.00；示例值：1.00；注：当cash_type=D1时为节假日取现手续费 |
| `response.data.qry_cash_config_list[].fee_rate` | 提现手续费率（%） | `String` | `6` | `C` | fix_amt与fee_rate至少填写一项，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；示例值：0.05；注：1、如果fix_amt与fee_rate都填写了则手续费=fix_amt+支付金额\*fee_rate；2、当cash_type=D1时为节假日取现手续费 |
| `response.data.qry_cash_config_list[].weekday_fix_amt` | D1工作日取现手续费固定金额 | `String` | `6` | `C` | 单位元，需保留小数点后两位。不收费请填写0.00；示例值：1.00；cash_type=D1时，生效 ；cash_type取现类型为D1时，遇工作日按此费率结算，若未配置则默认按照节假日手续费计算 |
| `response.data.qry_cash_config_list[].weekday_fee_rate` | D1工作日取现手续费率 | `String` | `6` | `C` | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；示例值：0.05；cash_type=D1时，生效 ；cash_type取现类型为D1时，遇工作日按此费率结算 ，若未配置则默认按照节假日手续费计算 |
| `response.data.qry_cash_config_list[].out_cash_flag` | 手续费外扣标记 | `String` | `1` | `N` | 1:外扣：取现时，从out_cash_huifuid账户扣手续费，2:内扣：从取现金额中扣手续费；示例值：1 |
| `response.data.qry_cash_config_list[].out_fee_huifuid` | 手续费承担方 | `String` | `18` | `N` | 手续费外扣时必需指定手续费承担方ID；示例值：[官网示例已脱敏] |
| `response.data.qry_cash_config_list[].out_cash_acct_type` | 取现手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户，02-现金户， 05-充值户，out_cash_flag=1时有值；示例值：01 |
| `response.data.qry_settle_config_list[]` | 结算配置 | `String` | `—` | `N` | jsonArray格式字符串 |
| `response.data.qry_settle_config_list[].settle_type` | 结算类型 | `String` | `1` | `N` | 0:对公 1:对私；示例值：0 |
| `response.data.qry_settle_config_list[].settle_cycle` | 结算周期 | `String` | `2` | `N` | T1:下个工作日到账;D1:下个自然日到账；示例值：T1 |
| `response.data.qry_settle_config_list[].min_amt` | 起结金额 | `String` | `18` | `N` | 账户余额大于等于起结金额才会发起结算。无值则不设置起结金额；示例值：1000.00 |
| `response.data.qry_settle_config_list[].remained_amt` | 留存金额 | `String` | `18` | `N` | 结算之后，账户剩余金额。无值则不设置留存金额；示例值：600.00 |
| `response.data.qry_settle_config_list[].fee_rate` | 结算手续费率(%) | `String` | `17` | `N` | 保留两位小数，示例值：0.60 |
| `response.data.qry_settle_config_list[].settle_abstract` | 结算摘要 | `String` | `128` | `N` | 商户在基本信息入驻时编辑的结算摘要；示例值：商品收款 |
| `response.data.qry_settle_config_list[].out_settle_flag` | 手续费外扣标记 | `String` | `1` | `N` | 1:外扣：结算时，从out_settle_huifuid账户扣手续费；2:内扣：从结算金额中扣手续费；示例值：1 |
| `response.data.qry_settle_config_list[].out_settle_huifuid` | 结算手续费外扣商户号 | `String` | `18` | `N` | 手续费外扣时必需指定手续费承担方ID；out_settle_flag=1时有值；示例值：[官网示例已脱敏] |
| `response.data.qry_settle_config_list[].out_settle_acct_type` | 结算手续费外扣账户类型 | `String` | `2` | `N` | 01-基本户，02-现金户， 05-充值户，out_settle_flag=1时有值；示例值：01 |
| `response.data.qry_settle_config_list[].settle_status` | 结算开关 | `String` | `1` | `N` | 0:关闭 1:打开；示例值：1 |
| `response.data.qry_settle_config_list[].settle_pattern` | 结算方式 | `String` | `2` | `N` | P0：批次结算 P1：定时结算 E1:中信E管家；示例值：P1 |
| `response.data.qry_settle_config_list[].is_priority_receipt` | 是否优先到账 | `String` | `1` | `N` | settle_cycle为TS时不填。settle_pattern为P0时，有值 Y：是 N：否；示例值：Y |
| `response.data.qry_settle_config_list[].settle_time` | 自定义结算处理时间 | `String` | `6` | `N` | settle_pattern为P1时有值；格式：HHmmss；示例值：113000 |
| `response.data.qry_settle_config_list[].token_no` | 绑卡序列号 | `String` | `20` | `N` | 结算卡对应的绑卡序列号。示例值：10000093623 |
| `response.data.qry_settle_config_list[].settle_batch_no` | 结算批次号 | `String` | `16` | `N` | 结算方式为P0：批次结算时有值，即将按指定结算批次号进行资金结算；示例值：100;[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| `response.data.qry_settle_config_list[].constant_amt` | 节假日结算手续费固定金额 | `String` | `15` | `C` | settle_cycle为D1时有值。单位元，需保留小数点后两位。不收费请填写0.00；settle_cycle结算周期为D1时，遇节假日按此费率结算；示例值：1.00 |
| `response.data.qry_settle_config_list[].workday_fixed_ratio` | 工作日结算手续费率 | `String` | `6` | `N` | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；示例值：0.05 |
| `response.data.qry_settle_config_list[].workday_constant_amt` | 工作日结算手续费固定金额 | `String` | `15` | `N` | 单位元，需保留小数点后两位。不填默认为0.00；示例值：1.00 |
| `response.data.agreement_info_list[]` | 协议信息 | `String` | `—` | `N` | jsonArray格式；[签约协议说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%95%86%E6%88%B7%E5%90%88%E5%90%8C%E7%AD%BE%E7%BA%A6%E8%A7%84%E5%88%99.xlsx) |
| `response.data.agreement_info_list[].agreement_type` | 协议类型 | `String` | `1` | `N` | 0-电子协议 1-纸质协议 3-挂网协议；示例值：3 |
| `response.data.agreement_info_list[].agreement_query_url` | 挂网协议查看地址 | `String` | `512` | `N` | 示例值：示例值：https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/PaymentServiceAgreement.htm |
| `response.data.agreement_info_list[].agreement_no` | 协议号 | `String` | `64` | `N` | 示例值：3245234 |
| `response.data.agreement_info_list[].agreement_model` | 协议模板号 | `String` | `64` | `C` | 示例值：[官网示例已脱敏] |
| `response.data.agreement_info_list[].agreement_name` | 协议模板名称 | `String` | `256` | `C` | 示例值：支付服务协议 |
| `response.data.agreement_info_list[].sign_date` | 签约日期 | `String` | `8` | `N` | 格式：yyyyMMdd；示例值：20221202 |
| `response.data.agreement_info_list[].agree_begin_date` | 协议开始日期 | `String` | `8` | `N` | 格式：yyyyMMdd；示例值：20221202 |
| `response.data.agreement_info_list[].agree_end_date` | 协议结束日期 | `String` | `8` | `N` | 格式：yyyyMMdd；示例值：20221202 |
| `response.data.agreement_info_list[].agreement_id` | 协议id | `String` | `32` | `N` | 示例值：495603459634 |
| `response.data.agreement_info_list[].agreement_item` | 协议分类 | `String` | `5` | `N` | 业务修改触发的业务分类类型；示例值：M0109 |
| `response.data.agreement_info_list[].con_stat` | 合同状态 | `String` | `2` | `N` | 电子协议类型会返回以下值：；2：创建合同异常；3：待签约 ；4：签约中；5：签约完成(电子协议只有签约完成才能做交易) ；6：已失效 ； 7：已拒签； 8：签约失败；示例值：5 |
| `response.data.agreement_info_list[].sms_send_list[]` | 协议发送集合 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.agreement_info_list[].sms_send_list[].sms_send_time` | 协议短信发送时间 | `String` | `20` | `N` | 格式yyyy-MM-dd HH:mm:ss；示例值：2023-04-13 10:11:12 |
| `response.data.agreement_info_list[].sms_send_list[].sms_send_result` | 协议短信发送结果 | `String` | `1` | `N` | S-成功 F-失败；示例值：S |
| `response.data.agreement_info_list[].sms_send_list[].sms_receiver_owner` | 协议短信接收人所属主体的名称 | `String` | `128` | `N` | 示例值：上海汇付支付服务公司 |
| `response.data.agreement_info_list[].sms_send_list[].sms_receiver_name` | 协议短信接收人姓名 | `String` | `64` | `N` | 示例值：张三 |
| `response.data.agreement_info_list[].sms_send_list[].sms_receiver_phone` | 协议短信接收人手机号码 | `String` | `11` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.agreement_info_list[].message_send_type` | 电子协议签约短信发送标识 | `String` | `1` | `N` | 协议类型为电子，业务开通审核通过后发送协议签约短信；0：发送，默认；1：不发送；示例值：1 |
| `response.data.agreement_info_list[].agreement_link` | 协议签署链 | `String` | `512` | `N` | 电子协议时有值 |
| `response.data.sign_user_info_list[]` | 签约人列表 | `String` | `—` | `N` | jsonArray格式字符串 |
| `response.data.sign_user_info_list[].type` | 签约人类型 | `String` | `7` | `N` | LEGAL-法人，对公结算或对私法人结算时可选法人签约；CONTACT-联系人，对公结算可选联系人（经办人）签约；OTHER-其他，对私非法人结算选“其他”，必须是结算人；示例值：LEGAL |
| `response.data.sign_user_info_list[].name` | 姓名 | `String` | `32` | `N` | 签约人类型=其他，有值；示例值：张三 |
| `response.data.sign_user_info_list[].mobile_no` | 手机号 | `String` | `11` | `N` | 签约人类型=法人/其他 ，有值；示例值：[官网示例已脱敏] |
| `response.data.sign_user_info_list[].cert_no` | 身份证 | `String` | `32` | `N` | 签约人类型=联系人/其他，有值；示例值：[官网示例已脱敏] |
| `response.data.sign_user_info_list[].identity_front_file_id` | 身份证照片-人像面 | `String` | `128` | `N` | 签约人类型=法人，法人身份证照片；签约人类型=联系人，联系人身份证照片；签约人类型=其他，签约人身份证照片；示例值：de2f6e1d-d9e9-3898-9b66-af2a96054193 |
| `response.data.sign_user_info_list[].identity_back_file_id` | 身份证照片-国徽面 | `String` | `128` | `N` | 签约人类型=法人，法人身份证照片；签约人类型=联系人，联系人身份证照片；签约人类型=其他，签约人身份证照片；示例值：de2f6e1d-d9e9-3898-9b66-af2a96054193 |
| `response.data.sign_user_info_list[].auth_file_id` | 法人授权书 | `String` | `128` | `N` | 签约人类型=联系人/其他，有值；示例值：de2f6e1d-d9e9-3898-9b66-af2a96054193 |
| `response.data.sign_user_info_list[].email` | 邮箱 | `String` | `32` | `N` | 示例值：example@email.com |
| `response.data.online_busi_type` | 线上业务类型 | `String` | `64` | `C` | 开通快捷、网银、余额支付Pro版、分账、代扣；参见[线上业务类型编码及补充材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E7%BA%BF%E4%B8%8A%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B%E7%BC%96%E7%A0%81%E5%8F%8A%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E.xlsx)；示例值：H7999AL |
| `response.data.online_media_info_list` | 运营媒介 | `String` | `—` | `N` | jsonObject字符串 |
| `response.data.online_media_info_list.media_type` | 运营媒介类型 | `String` | `2` | `Y` | S1-PC网站；若媒介项为PC网站：（PC网站域名、ICP备案号、ICP许可证号，测试账号、密码 ）；S2-APP场景；若媒介项为APP场景：（APP名称、APP下载地址、测试账号、密码 ），若开通微信App支付，则新增app_id、app_name必填；S3-小程序场景；若媒介项为小程序：（小程序名称、测试账号、密码）；S4-公众号场景；若媒介项为公众号：（公众号名称、测试账号、密码）；S5-其他；媒介项为其他：其他有效信息或链接地址必填；线上场景时必填一项；示例值：S1 |
| `response.data.online_media_info_list.media_name` | 媒介名称 | `String` | `200` | `C` | PC网站域名／APP名称／小程序名称／公众号名称；示例值：汇付服务；运营媒介类型为 ：S1/S2/S3/S4时，必填 |
| `response.data.online_media_info_list.test_account` | 测试账号 | `String` | `64` | `Y` | 示例值：test |
| `response.data.online_media_info_list.test_secret` | 测试密码 | `String` | `64` | `Y` | 示例值：test |
| `response.data.online_media_info_list.other_info` | 其他有效信息 | `String` | `200` | `C` | 其他有效信息或链接地址/APP下载地址；示例值：http://download.huifu.com |
| `response.data.online_media_info_list.media_front_page` | 运营媒介-首页 | `String` | `64` | `C` | 若为企业商户，且开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%）；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `response.data.online_media_info_list.media_service_page` | 运营媒介-服务/商品明细页面 | `String` | `64` | `C` | 若为企业商户，且开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%）；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `response.data.online_media_info_list.media_order_page` | 运营媒介-下单场景页面 | `String` | `64` | `C` | 若为企业商户，且开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%）；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `response.data.online_media_info_list.media_pay_page` | 运营媒介-支付页面 | `String` | `64` | `C` | 若为企业商户，且开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%）；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `response.data.online_media_info_list.media_mer_common_flag` | 媒介主体与商户主体是否一致 | `String` | `1` | `C` | Y/N；示例值：Y；运营媒介为S1、S2、S3、S4且企业商户开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），；若不一致，则需提供ICP备案/APP/微信公众号/小程序主体与商户的使用授权或开发证明材料 |
| `response.data.online_media_info_list.authorize_materials` | 授权或开发证明材料 | `String` | `64` | `C` | 运营媒介为S1、S2、S3、S4且媒介主体与商户主体不一致时，且企业商户开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `response.data.online_media_info_list.other_material` | 微信APP补充材料 | `String` | `128` | `C` | 运营媒介为S2且开通微信下app支付时选填，具体见[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) |
| `response.data.online_media_info_list.app_id` | appId | `String` | `128` | `C` | 运营媒介为S2且开通微信下app支付时有 |
| `response.data.online_media_info_list.app_name` | appId认证主体名称 | `String` | `128` | `C` | 运营媒介为S2且开通微信下app支付时有 |
| `response.data.online_media_info_list.supplement` | 补充说明 | `String` | `512` | `C` | 运营媒介为S2且开通微信下app支付时有 |
| `response.data.quick_flag` | 是否开通快捷 | `String` | `1` | `N` | 1:开通 0:未开通，为空未配置(未开通);示例值：1 |
| `response.data.online_flag` | 是否开通网银 | `String` | `1` | `N` | 1:开通 0:未开通，为空未配置(未开通);示例值：1 |
| `response.data.withhold_flag` | 是否开通代扣 | `String` | `1` | `N` | 1:开通 0:未开通，为空未配置(未开通);示例值：1 |
| `response.data.pre_authorization_flag` | 是否开通支付宝预授权 | `String` | `1` | `N` | 1:开通 0:未开通，为空未配置(未开通);示例值：1 |
| `response.data.web_flag` | 是否开通手机WAP支付 | `String` | `1` | `N` | 1:开通 0:未开通，为空未配置(未开通)；示例值：1 |
| `response.data.balance_pay_flag` | 是否开通余额支付 | `String` | `1` | `N` | 1:开通 0:未开通，为空未配置(未开通)；示例值：1 |
| `response.data.qry_balance_pay_config` | 余额支付配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.qry_balance_pay_config.fee_rate` | 支付手续费(%) | `String` | `17` | `N` | 开通余额支付时fee_amt与fee_rate必须填写一种收费方式。单位%，需保留小数点后两位，示例值：0.50代表费率为0.5%，最低传入0.00 |
| `response.data.qry_balance_pay_config.fee_amt` | 固定手续费(元) | `String` | `17` | `N` | 开通余额支付时fee_amt与fee_rate必须填写一种收费方式。单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.qry_balance_pay_config.balance_model` | 余额支付业务模式 | `String` | `2` | `N` | 2-线上（包括线上+线下）入驻商户货款（周期性结算）；3-线上（包括线上+线下）营销补贴（周期性结算）；4-线上（包括线上+线下）推广方（渠道/代理/个人）的服务佣金/抽成；5-线上（包括线上+线下）红包发放；6-线上（包括线上+线下）钱包功能；7-线上（包括线上+线下）其他模式；单选；示例值：6 |
| `response.data.qry_balance_pay_config.balance_pay_ext_info` | 余额支付情况说明 | `String` | `—` | `N` | jsonObject |
| `response.data.qry_balance_pay_config.balance_pay_ext_info.busi_instruction` | 余额支付业务模式说明 | `String` | `500` | `N` | 请详细说明商户的业务模式，包括不限于（业务参与方、各方的权利及义务关系等）；示例值：商户向企业采购产品，并将其展示在其电商平台上，用户注册后购买其产品，产品主要有家电、服饰、鞋帽等，用户购买产品的资金作为商户所得，商户根据订单情况进行物流配送。 |
| `response.data.qry_balance_pay_config.balance_pay_ext_info.capital_instruction` | 余额支付资金流向说明 | `String` | `500` | `N` | 请详细说明商户的资金流向，包括但不限于（交易所涉及的各方账户、资金流入流出过程等），；示例值：用户选购产品后根据订单支付给商户，商户根据结算周期，结算到对公账户。 |
| `response.data.qry_balance_pay_config.balance_pay_ext_info.function_instruction` | 余额支付功能开通用途说明 | `String` | `500` | `N` | 请详述所申请功能的原因、场景、涉及对象类型；示例值：商户给消费者发放补贴到钱包账户，用于奖励消费行为 |
| `response.data.qry_balance_pay_config.pay_mode` | 余额支付模式 | `String` | `4` | `Y` | pro，lite；示例值：pro；lite版不支持当日收款资金余额支付；示例值：pro |
| `response.data.online_fee_conf_list[]` | 线上费率配置 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.online_fee_conf_list[].fee_type` | 业务类型 | `String` | `25` | `N` | ONLINE_PERSON:个人网银支付，【biz_conf】中online_flag开通了才需要填； ONLINE_ENT:企业网银支付，【biz_conf】中online_flag开通了才需要填； QUICK_DEBIT:快捷借记卡支付，【biz_conf】中quick_flag开通了才需要填； QUICK_CREDIT:快捷贷记卡支付，【biz_conf】中quick_flag开通了才需要填； WAP:手机WAP支付，【biz_conf】中online_flag开通了才需要填；ONLINE_ENT_TOP_UP:B2B网银充值，【biz_conf】中online_recharge_flag开通了才需要填；ONLINE_PERSON_TOP_UP:B2C网银充值，【biz_conf】中online_recharge_flag开通了才需要填；WITHHOLD:代扣，【biz_conf】中withhold_flag开通了才需要填，示例值：ONLINE_PERSON |
| `response.data.online_fee_conf_list[].bank_id` | 银行编码 | `String` | `8` | `N` | 参考： 银行编码；示例值：01020000 |
| `response.data.online_fee_conf_list[].dc_flag` | 借贷标志 | `String` | `1` | `N` | D:借记,C:贷记 ；示例值：D |
| `response.data.online_fee_conf_list[].fix_amt` | 手续费（固定/元） | `String` | `16` | `N` | 必须填写一种收费方式；保留两位小数；示例值：1.00 |
| `response.data.online_fee_conf_list[].fee_rate` | 费率（%） | `String` | `6` | `N` | 必须填写一种收费方式；保留两位小数；示例值：0.38 |
| `response.data.online_fee_conf_list[].bank_name` | 银行名称 | `String` | `50` | `N` | 示例值：中国工商银行上海市中山北路支行 |
| `response.data.online_fee_conf_list[].bank_short_chn` | 银行中文简称 | `String` | `50` | `N` | 示例值：工行上海市中北支行 |
| `response.data.online_fee_conf_list[].stat_flag` | 费率状态 | `String` | `1` | `N` | 1开，0关；示例值：1 |
| `response.data.online_fee_conf_list[].fee_min_amt` | 手续费最小值（元） | `String` | `9` | `N` | 必须填写一种收费方式；保留两位小数；示例值：1.00 |
| `response.data.online_fee_conf_list[].fee_formula_type` | 代扣手续费计费模式 | `String` | `2` | `N` | withhold_flag为Y时；01: 百分比手续费，无封顶值或保底值； 02: 百分比手续费，有保底值； 03: 固定手续费； 04: 固定手续费+百分比手续费； 为空默认04 示例值：04 |
| `response.data.delay_flag` | 是否开通延迟入账 | `String` | `1` | `N` | N：否 Y：是，为空则为否；示例值：Y |
| `response.data.forced_delay_flag` | 商户开通强制延迟标记 | `String` | `—` | `N` | Y:开通,N:关闭；示例值：N |
| `response.data.out_fee_flag` | 交易手续费外扣标记 | `String` | `1` | `N` | 1：外扣，2：内扣；（默认2内扣）；示例值：2 |
| `response.data.out_fee_huifu_id` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填，示例值：[官网示例已脱敏]；优先级高于相同名称的公共参数 |
| `response.data.out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01；优先级高于相同名称的公共参数 |
| `response.data.qry_wx_conf_list[]` | 微信支付配置信息 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.qry_wx_conf_list[].wx_mer_infos` | 微信商户号信息 | `Object` | `—` | `N` | 参见下文描述 |
| `response.data.qry_wx_conf_list[].wx_mer_infos.bank_mer_code` | 银联商户号 | `String` | `32` | `N` | 商户在银联开通的支付宝(或微信)商户号；示例值：2234544 |
| `response.data.qry_wx_conf_list[].wx_mer_infos.nucc_bank_mer_code` | 网联商户号 | `String` | `32` | `N` | 商户在网联开通的支付宝(或微信)商户号 |
| `response.data.qry_wx_conf_list[].wx_mer_infos.pay_channel_id` | 子渠道号 | `String` | `50` | `N` | 示例值：JP00001 |
| `response.data.qry_wx_conf_list[].wx_mer_infos.is_default` | 默认渠道标记 | `String` | `1` | `N` | 1：默认渠道；示例值：1 |
| `response.data.qry_wx_conf_list[].wx_mer_infos.sub_mer_id` | 二级商户号 | `String` | `1` | `N` | 示例值：6634423544 |
| `response.data.qry_wx_conf_list[].fee_rate` | 手续费（%） | `String` | `9` | `N` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.qry_wx_conf_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `6` | `N` | 固定金额保留2位小数；大于0。需要渠道商开通此功能。示例值：0.38 |
| `response.data.qry_wx_conf_list[].pay_channel_id_list[]` | 子渠道号 | `String` | `128` | `N` | String集合，jsonArray格式；示例值：["JQF00001","JQF00002"] |
| `response.data.qry_wx_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `N` | 参见《[微信支付场景](https://paas.huifu.com/partners/api/doc/api_ggcsbm.md#微信支付场景)（官网相对地址原文：`api_ggcsbm.md#微信支付场景`）》说明；示例值：1 |
| `response.data.qry_wx_conf_list[].fee_charge_type` | 交易手续费收取类型 | `String` | `1` | `N` | 1:实收,2:后收；示例值：1 |
| `response.data.qry_wx_conf_list[].out_fee_flag` | 交易手续费外扣标记 | `String` | `1` | `N` | 1：外扣，2：内扣；（默认2内扣）；示例值：2 |
| `response.data.qry_wx_conf_list[].out_fee_huifu_id` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填，示例值：[官网示例已脱敏]；优先级高于相同名称的公共参数 |
| `response.data.qry_wx_conf_list[].out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01；优先级高于相同名称的公共参数 |
| `response.data.qry_wx_conf_list[].switch_state` | 功能开关 | `String` | `1` | `Y` | 0:关闭 1:开通；示例值：1 |
| `response.data.qry_ali_conf_list[]` | 支付宝支付配置信息 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.qry_ali_conf_list[].ali_mer_infos` | 支付宝商户信息 | `Object` | `—` | `N` | — |
| `response.data.qry_ali_conf_list[].ali_mer_infos.bank_mer_code` | 银联商户号 | `String` | `32` | `N` | 商户在银联开通的支付宝(或微信)商户号；示例值：2234544 |
| `response.data.qry_ali_conf_list[].ali_mer_infos.nucc_bank_mer_code` | 网联商户号 | `String` | `32` | `N` | 商户在网联开通的支付宝(或微信)商户号 |
| `response.data.qry_ali_conf_list[].ali_mer_infos.pay_channel_id` | 子渠道号 | `String` | `50` | `N` | 示例值：JP00001 |
| `response.data.qry_ali_conf_list[].ali_mer_infos.is_default` | 默认渠道标记 | `String` | `1` | `N` | 1：默认渠道；示例值：1 |
| `response.data.qry_ali_conf_list[].ali_mer_infos.sub_mer_id` | 二级商户号 | `String` | `10` | `N` | 示例值：6634423544 |
| `response.data.qry_ali_conf_list[].fee_rate` | 手续费（%） | `String` | `9` | `N` | 示例值：0.60 |
| `response.data.qry_ali_conf_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `6` | `N` | 固定金额保留2位小数；大于0。需要渠道商开通此功能。示例值：0.38 |
| `response.data.qry_ali_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `N` | 1、线下扫码（正扫&反扫&台牌），2、线上扫码，3、非盈利费率；示例值：1 |
| `response.data.qry_ali_conf_list[].fee_charge_type` | 交易手续费收取类型 | `String` | `1` | `N` | 1：实收,2：后收；示例值：1 |
| `response.data.qry_ali_conf_list[].pay_channel_id_list` | 子渠道号 | `String` | `128` | `N` | String集合；示例值：["JQF00001","JQF00002"] |
| `response.data.qry_ali_conf_list[].out_fee_flag` | 交易手续费外扣标记 | `String` | `1` | `N` | 1：外扣，2：内扣；（默认2内扣）；示例值：2 |
| `response.data.qry_ali_conf_list[].out_fee_huifu_id` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填，示例值：[官网示例已脱敏]；优先级高于相同名称的公共参数 |
| `response.data.qry_ali_conf_list[].out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01；优先级高于相同名称的公共参数 |
| `response.data.qry_ali_conf_list[].switch_state` | 功能开关 | `String` | `1` | `Y` | 0:关闭 1:开通；示例值：1 |
| `response.data.qry_bank_card_conf` | 银行卡支付配置信息 | `String` | `—` | `N` | jsonObject格式；只有企业商户有值 |
| `response.data.qry_bank_card_conf.bank_mer_code` | 银联商户号 | `String` | `18` | `N` | 银联报备生成的银行商户号；示例值：66345234544 |
| `response.data.qry_bank_card_conf.charge_cate_code` | 银行业务手续费类型 | `String` | `2` | `N` | 01-减免类 02-优惠类 03-标准类（默认）；示例值：03 |
| `response.data.qry_bank_card_conf.debit_fee_rate` | 借记卡手续费（%） | `String` | `9` | `Y` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]； 示例值：0.60 |
| `response.data.qry_bank_card_conf.debit_fee_limit` | 借记卡封顶值 | `String` | `4` | `N` | 数字类型，大于0保留2位小数； 示例值：2.00 |
| `response.data.qry_bank_card_conf.credit_fee_rate` | 贷记卡手续费（%） | `String` | `9` | `Y` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.90 |
| `response.data.qry_bank_card_conf.is_open_cloud_flag` | 是否开通银联手机闪付 | `String` | `1` | `Y` | 选项：0：否 1：是。目前默认开通；示例值：0 |
| `response.data.qry_bank_card_conf.switch_state` | 功能开关 | `String` | `1` | `Y` | 0:关闭 1:开通；示例值：1 |
| `response.data.qry_union_conf` | 银联二维码支付配置信息 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.qry_union_conf.bank_mer_code` | 银联商户号 | `String` | `18` | `N` | 银联报备生成的银行商户号；示例值：66345234544 |
| `response.data.qry_union_conf.qr_code_info` | 银联小微二维码 | `String` | `64` | `N` | — |
| `response.data.qry_union_conf.fee_charge_type` | 交易手续费收取类型 | `String` | `1` | `N` | 1:实收,2:后收；示例值：1 |
| `response.data.qry_union_conf.credit_fee_rate_up` | 贷记卡手续费1000以上（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00];示例值：0.60 |
| `response.data.qry_union_conf.debit_fee_rate` | 借记卡手续费（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00];示例值：0.60 |
| `response.data.qry_union_conf.credit_fee_rate_down` | 贷记卡手续费1000及以下（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.qry_union_conf.debit_fee_rate_up` | 借记卡手续费1000以上（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.qry_union_conf.debit_fee_rate_down` | 借记卡手续费1000及以下（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.qry_union_conf.switch_state` | 功能开关 | `String` | `1` | `Y` | 0:关闭 1:开通；示例值：1 |
| `response.data.out_order_funds_merge` | 全域资金管理配置 | `String` | `—` | `N` | jsonObject字符串 |
| `response.data.out_order_funds_merge.switch_state` | 开通状态 | `String` | `1` | `Y` | 0:关闭 1:开通；示例值：1 |
| `response.data.out_order_funds_merge.out_order_auto_acct_flag` | 全域资金自动入账开关 | `String` | `1` | `Y` | 开通、关闭自动入账功能；0:关闭 1:开通；示例值：1；关闭自动入账需要[处理银行来账通知](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_lztz)，并调用[汇付入账确认接口](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_yhskfk)来确认入账。 |
| `response.data.out_order_funds_merge.batch_auto_acct_flag` | 批量入账开关 | `String` | `1` | `N` | 0:关闭（默认）；单笔入账模式；1:开通；开通批量入账；仅支持自动入账模式；示例值：0 |
| `response.data.out_order_funds_merge.batch_no` | 批次入账时间 | `String` | `20` | `C` | 10:00-10点批次入账；16:00-16点批次入账开通批次入账时必填 ，多个批次使用逗号分隔；示例值：10:00,16:00 |
| `response.data.out_order_funds_merge.fee_rate` | 支付手续费(%) | `String` | `6` | `N` | 支持两位小数；示例值：0.45；fee_rate与fee_fix_amt与fee_min_amt不能同时为空 |
| `response.data.out_order_funds_merge.fee_min_amt` | 手续费最小值(元) | `String` | `6` | `N` | 支付手续费最小值，支持两位小数；示例值：1.00fee_rate与fee_fix_amt与fee_min_amt不能同时为空 |
| `response.data.out_order_funds_merge.out_fee_flag` | 交易手续费外扣标记 | `String` | `1` | `N` | 1：外扣，2：内扣；（默认2内扣）；示例值：2 |
| `response.data.out_order_funds_merge.out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.out_order_funds_merge.out_fee_acctid` | 交易手续费外扣子账户号 | `String` | `16` | `N` | 示例值：F00598600 |
| `response.data.out_order_funds_merge.account_name` | 账户名 | `String` | `128` | `N` | 全域资金管理配置功能涉及字段；示例值：张三收款户 |
| `response.data.out_order_funds_merge.electron_account` | 电子账号 | `String` | `32` | `N` | 全域资金管理配置功能开通的电子账号；示例值： |
| `response.data.out_order_funds_merge.out_order_acct_card` | 全域资金开户使用的银行卡信息 | `String` | `—` | `N` | jsonObject字符串 |
| `response.data.out_order_funds_merge.out_order_acct_card.prov_id` | 银行所在省 | `String` | `6` | `N` | [参考省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000 |
| `response.data.out_order_funds_merge.out_order_acct_card.area_id` | 银行所在市 | `String` | `6` | `N` | [参考省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310100 |
| `response.data.out_order_funds_merge.out_order_acct_card.bank_code` | 银行编码 | `String` | `8` | `N` | 对公时根据支行编码获取总行编码；参考[银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；示例值：01020000 |
| `response.data.out_order_funds_merge.out_order_acct_card.branch_code` | 支行联行号 | `String` | `12` | `N` | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `response.data.out_order_funds_merge.out_order_acct_card.branch_name` | 支行名称 | `String` | `64` | `N` | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：中国工商银行上海市中山北路支行 |
| `response.data.out_order_funds_merge.out_order_acct_card.card_name` | 结算账户名 | `String` | `128` | `Y` | 银行卡对应的户名；示例值：上海汇付支付有限公司 |
| `response.data.out_order_funds_merge.out_order_acct_card.card_no` | 银行卡号 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `response.data.out_order_funds_merge.out_order_acct_card.card_type` | 卡类型 | `String` | `1` | `Y` | 0:对公 1:对私示例值：0 |
| `response.data.out_order_funds_merge.out_order_acct_card.cert_type` | 持卡人证件类型 | `String` | `2` | `N` | 00:身份证示例值：00 |
| `response.data.out_order_funds_merge.out_order_acct_card.cert_begin_date` | 持卡人证件有效期（起始） | `String` | `8` | `N` | 格式：yyyyMMdd，示例值：20210830 |
| `response.data.out_order_funds_merge.out_order_acct_card.cert_end_date` | 持卡人证件有效期（截止） | `String` | `8` | `N` | 格式：yyyyMMdd；示例值：20210830 |
| `response.data.out_order_funds_merge.out_order_acct_card.cert_no` | 持卡人证件号码 | `String` | `32` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.out_order_funds_merge.out_order_acct_card.cert_validity_type` | 持卡人证件有效期类型 | `String` | `1` | `N` | 1:长期有效 0:非长期有效；示例值：0 |
| `response.data.out_order_funds_merge.out_order_acct_card.mp` | 银行卡绑定手机号 | `String` | `11` | `Y` | 示例值：[官网示例已脱敏] |
| `response.data.out_order_funds_merge.out_order_acct_card.open_licence_no` | 开户许可证核准号 | `String` | `32` | `N` | 示例值：J2900123456789 |
| `response.data.out_order_funds_merge.platform_mer_id` | 全域资金平台商户ID | `String` | `32` | `Y` | 全域资金平台商户ID；示例值：XXXXXXXXX |
| `response.data.out_order_funds_merge.business_model` | 全域支付业务模式 | `String` | `20` | `N` | acquiringMode：收单模式，默认；rechargeMode：充值模式，；示例值：acquiringMode |
| `response.data.out_order_funds_merge.other_payment_institutions_pic` | 商户与其他支付机构签署的收单协议或证明材料 | `String` | `64` | `N` | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `response.data.combine_pay_config` | 补贴支付配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.combine_pay_config.fee_rate` | 支付手续费(%) | `String` | `9` | `N` | 支付手续费(%) 支持两位小数 fee_rate与fee_fix_amt 不能同时为空；示例值：0.50代表费率为0.5% |
| `response.data.combine_pay_config.fee_fix_amt` | 支付固定手续费(元) | `String` | `9` | `N` | 支付固定手续费(元)支持两位小数 fee_rate与fee_fix_amt 不能同时为空；示例值：1.50 注：如果fee_fix_amt与fee_rate都填写了则手续费=fee_fix_amt+支付金额\fee_rate |
| `response.data.combine_pay_config.out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 ，示例值：1 优先级高于相同名称的公共参数 |
| `response.data.combine_pay_config.out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时有，示例值：[官网示例已脱敏] 优先级高于相同名称的公共参数 |
| `response.data.combine_pay_config.out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01 优先级高于相同名称的公共参数 |
| `response.data.combine_pay_config.switch_state` | 功能开关 | `String` | `1` | `Y` | 0:关闭 1:开通；示例值：1 |
| `response.data.wx_zl_conf` | 微信直连配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.wx_zl_conf.sub_mch_id` | 微信子商户号 | `String` | `32` | `Y` | 微信支付分配的子商户号；示例值：1632157057 |
| `response.data.wx_zl_conf.wx_zl_pay_conf_list[]` | 配置集合 | `String` | `512` | `Y` | jsonArray |
| `response.data.wx_zl_conf.wx_zl_pay_conf_list[].service_code` | 申请服务 | `String` | `16` | `Y` | JSAPI-公众号，APPLET-小程序；示例值：JSAPI |
| `response.data.wx_zl_conf.wx_zl_pay_conf_list[].sub_app_id` | 功能服务appid | `String` | `32` | `Y` | 子商户的公众号、小程序ID；示例值：wx51aa91a575359ff5 |
| `response.data.wx_zl_conf.wx_zl_pay_conf_list[].switch_state` | 功能开关 | `String` | `1` | `Y` | 0-关闭，1-打开；示例值：1 |
| `response.data.wx_zl_conf.wx_zl_pay_conf_list[].fee_rate` | 功能费率(%) | `String` | `6` | `Y` | 保留两位小数。示例值：0.60 |
| `response.data.wx_zl_conf.contact_info` | 联系人信息 | `String` | `—` | `Y` | jsonObject 对象。按提交时的信息进行返回。 |
| `response.data.wx_zl_conf.contact_info.contact_type` | 联系人类型 | `String` | `1` | `Y` | 1： 法人；2：经办人；示例值：1 |
| `response.data.wx_zl_conf.contact_info.contact_name` | 联系人姓名 | `String` | `128` | `C` | 联系人类型为经办人时有值；示例值：张三 |
| `response.data.wx_zl_conf.contact_info.cert_type` | 联系人证件类型 | `String` | `2` | `C` | 联系人类型为经办人时有值；00：身份证；01:护照；11：港澳台同胞通行证；12：外国人居留证；13：港澳居民证；14：台湾居民证；示例值：00 |
| `response.data.wx_zl_conf.contact_info.contact_cert_no` | 联系人证件号码 | `String` | `18` | `C` | 联系人类型为经办人时有值；示例值：[官网示例已脱敏] |
| `response.data.wx_zl_conf.contact_info.contact_mobile_no` | 联系人手机号 | `String` | `11` | `Y` | 示例值：[官网示例已脱敏] |
| `response.data.wx_zl_conf.contact_info.contact_email` | 联系人电子邮箱 | `String` | `40` | `Y` | 示例值：carl.chen@huifu.com |
| `response.data.wx_zl_conf.sales_info` | 经营场景信息 | `String` | `—` | `Y` | json 对象 |
| `response.data.wx_zl_conf.sales_info.sales_scenes_type` | 经营场景类型 | `String` | `256` | `Y` | 多个以英文逗号分割，至少要有一个；线下门店：SALES_SCENES_STORE；公众号：SALES_SCENES_MP；小程序：SALES_SCENES_MINI_PROGRAM；互联网：SALES_SCENES_WEB；APP：SALES_SCENES_APP；企业微信：SALES_SCENES_WEWORK；示例值：SALES_SCENES_WEWORK |
| `response.data.wx_zl_conf.sales_info.fee_rate` | 功能费率 | `String` | `6` | `C` | 仅支持渠道商传入该字段。示例值：0.06；平台商户为子商户开通微信直连支付时，不支持该字段，取平台商户费率上送微信。 |
| `response.data.wx_zl_conf.sales_info.biz_sub_jsapi_app_id` | 线下场所对应的商家公众号APPID | `String` | `256` | `C` | 开通线下门店场景时，填入。都填入时，取公众号的上送微信。示例值：wx51aa91a575359ff5 |
| `response.data.wx_zl_conf.sales_info.biz_sub_mini_app_id` | 线下场所对应的商家小程序APPID | `String` | `256` | `C` | 开通线下门店场景时，填入。都填入时，取公众号的上送微信。示例值：wxea9c30a90fs8d3fe |
| `response.data.wx_zl_conf.sales_info.jsapi_app_id` | 服务商公众号 ID | `String` | `256` | `C` | 开通公众号场景时，直连服务商和商户的公众号 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `response.data.wx_zl_conf.sales_info.jsapi_sub_app_id` | 商家公众号APPID | `String` | `256` | `C` | 开通公众号场景时，直连服务商和商户的公众号 APP ID，二选一填入。示例值：wxea9c30a90fs8d3fe |
| `response.data.wx_zl_conf.sales_info.mini_app_id` | 服务商小程序APPID | `String` | `256` | `C` | 开通小程序场景时，直连服务商和商户的小程序 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `response.data.wx_zl_conf.sales_info.mini_sub_app_id` | 商家小程序APPID | `String` | `256` | `C` | 开通小程序场景时，直连服务商和商户的小程序 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `response.data.wx_zl_conf.sales_info.app_app_id` | 服务商应用APPID | `String` | `256` | `C` | 开通 APP 场景时，直连服务商和商户的 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `response.data.wx_zl_conf.sales_info.app_sub_app_id` | 商家应用APPID | `String` | `256` | `C` | 开通 APP 场景时，直连服务商和商户的 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `response.data.wx_zl_conf.sales_info.web_app_id` | 互联网网站对应的商家APPID | `String` | `256` | `C` | 开通互联网场景时填入；示例值：wx51aa91a575359ff5 |
| `response.data.wx_zl_conf.sales_info.sub_corp_id` | 商家企业微信CorpID | `String` | `256` | `C` | 开通企业微信场景时填入；示例值：xxxxx |
| `response.data.wx_zl_conf.wx_card_info` | 银行账户信息 | `String` | `—` | `N` | json 对象， |
| `response.data.wx_zl_conf.wx_card_info.card_type` | 账户类型 | `String` | `1` | `Y` | 0：对公银行账户；1：经营者个人银行卡；示例值：0 |
| `response.data.wx_zl_conf.wx_card_info.card_name` | 开户名称 | `String` | `128` | `Y` | 选择“经营者个人银行卡”时，开户名称必须与“经营者证件姓名”一致。选择“对公银行账户”时，开户名称必须与营业执照上的“商户名称”一致。；示例值：张三 |
| `response.data.wx_zl_conf.wx_card_info.bank_code` | 开户银行 | `String` | `8` | `Y` | 客户按汇付银行编码上送；示例值：01020000 |
| `response.data.wx_zl_conf.wx_card_info.prov_id` | 开户银行省编码 | `String` | `6` | `Y` | 按汇付的省市编码；示例值：310000 |
| `response.data.wx_zl_conf.wx_card_info.area_id` | 开户银行市编码 | `String` | `6` | `Y` | 示例值：310100 |
| `response.data.wx_zl_conf.wx_card_info.branch_code` | 开户银行联行号 | `String` | `20` | `C` | 开户银行联行号与开户银行全称（含支行)二选一；示例值：102290026507 |
| `response.data.wx_zl_conf.wx_card_info.branch_name` | 开户银行全称（含支行) | `String` | `128` | `C` | 开户银行联行号与开户银行全称（含支行)二选一；示例值：中国工商银行股份有限公司上海市中山北路支行 |
| `response.data.wx_zl_conf.wx_card_info.card_no` | 银行账号 | `String` | `30` | `Y` | 示例值：[官网示例已脱敏] |
| `response.data.ali_zl_conf_list[]` | 支付宝直连配置列表 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.ali_zl_conf_list[].mer_code` | 支付宝商户号 | `String` | `32` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.ali_zl_conf_list[].mer_app_id` | 应用ID | `String` | `32` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.ali_zl_conf_list[].apply_type` | 申请类型 | `String` | `32` | `N` | FACE_TO_FACE：当面付；示例值：FACE_TO_FACE |
| `response.data.ali_zl_conf_list[].contact_name` | 联系人姓名 | `String` | `64` | `N` | 支付宝联系人信息，不传取商户的联系人信息；示例值：张三 |
| `response.data.ali_zl_conf_list[].contact_mobile_no` | 联系人手机号 | `String` | `11` | `N` | 支付宝联系人信息，不传取商户的联系人信息；示例值：[官网示例已脱敏] |
| `response.data.ali_zl_conf_list[].contact_email` | 联系人电子邮箱 | `String` | `40` | `N` | 支付宝联系人信息，不传取商户的联系人信息；示例值：carl.chen@huifu.com |
| `response.data.ali_zl_conf_list[].account` | 商户支付宝账号 | `String` | `128` | `N` | 商户登录支付宝控台的账号；示例值：zhangsan |
| `response.data.ali_zl_conf_list[].fee_rate` | 服务费率 | `String` | `6` | `C` | 仅支持渠道商。平台商户调用不支持该字段；服务费率（%），0.38~3之间，精确到0.01。示例值：0.06 |
| `response.data.ali_zl_conf_list[].license_code` | 营业执照编号 | `String` | `20` | `N` | 工商营业执照编号，示例值：92650109MA79R8E308 |
| `response.data.file_info_list[]` | 商户材料列表 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.file_info_list[].file_id` | 文件ID | `String` | `64` | `N` | 示例值：e91a6ed5-d258-3ed9-bf52-64ff2b0f2bae |
| `response.data.file_info_list[].file_name` | 文件名称 | `String` | `32` | `N` | 示例值：00.jpg |
| `response.data.file_info_list[].file_type` | 文件类型 | `String` | `32` | `N` | 示例值：F24 |
| `response.data.file_info_list[].file_url` | 文件地址 | `String` | `128` | `N` | 示例值：[官网示例图片已省略] |
| `response.data.file_info_list[].update_time` | 更新时间 | `String` | `14` | `N` | 格式：YYYYMMDDhhmmss示例值：20230512132234 |
| `response.data.recon_resp_addr` | 交易应答异步通知地址 | `String` | `128` | `N` | 消息接收地址，为空不推送消息。 示例值：http://service.example.com/to/path。 |
| `response.data.enter_fee` | 开户费用值(元) | `String` | `14` | `N` | 示例值：5.00 |
| `response.data.enter_fee_flag` | 开户费用类型 | `String` | `1` | `N` | 1-一次性开户费，2-平台套餐费（元/年）；示例值：2 |
| `response.data.mer_Identity` | 商户身份 | `String` | `1` | `N` | 1：总部商户，0：下级商户；示例值：1 |
| `response.data.mer_level` | 商户层级 | `String` | `1` | `N` | 1：总部，2：一级，3：二级，4：三级，5：四级；示例值：1 |
| `response.data.mer_config_info` | 开通下级商户权限配置对象 | `String` | `—` | `N` | 权限配置，价格配置 |
| `response.data.mer_config_info.ali_conf_list[]` | 支付宝配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.mer_config_info.ali_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 1、线下扫码（正扫&反扫&台牌），2、线上扫码，示例值：1 |
| `response.data.mer_config_info.ali_conf_list[].fee_rate` | 手续费 | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.ali_conf_list[].open_flag` | 允许开通该业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.wx_conf_list[]` | 微信配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.mer_config_info.wx_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 1：线下反扫；2：线下公众号；3：线下小程序；4：线上公众号；5：线上小程序；12：线上反扫；示例值：1 |
| `response.data.mer_config_info.wx_conf_list[].fee_rate` | 手续费 | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.wx_conf_list[].open_flag` | 允许开通该场景业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.union_conf_list[]` | 银联二维码配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.mer_config_info.union_conf_list[].charge_cate_code` | 银联业务手续费类型 | `String` | `2` | `N` | 03-标准类 小微商户仅有03 标准类 ；04-线上费率（银联二维码线上）；默认03标志类 |
| `response.data.mer_config_info.union_conf_list[].open_flag` | 允许开通银联二维码业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.union_conf_list[].debit_fee_rate_up` | 借记卡手续费1000以上（%） | `String` | `9` | `Y` | 数字格式，大于等于0，保留2位小数；示例值：0.60 |
| `response.data.mer_config_info.union_conf_list[].debit_fee_limit_up` | 借记卡封顶1000以上 | `String` | `9` | `N` | 数字格式，大于等于0，保留2位小数；示例值：0.60 |
| `response.data.mer_config_info.union_conf_list[].debit_fee_rate_down` | 借记卡手续费1000以下（%） | `String` | `9` | `Y` | 数字格式，大于等于0，保留2位小数；示例值：0.38 |
| `response.data.mer_config_info.union_conf_list[].debit_fee_limit_down` | 借记卡封顶1000以下 | `String` | `9` | `N` | 数字格式，大于等于0，保留2位小数；示例值：18.00 |
| `response.data.mer_config_info.union_conf_list[].credit_fee_rate_up` | 贷记卡手续费1000以上（%） | `String` | `9` | `Y` | 数字格式，大于等于0，保留2位小数；示例值：0.60 |
| `response.data.mer_config_info.union_conf_list[].credit_fee_rate_down` | 银联二维码业务贷记卡手续费1000以下（%） | `String` | `9` | `Y` | 数字格式，大于等于0，保留2位小数；示例值：0.60 |
| `response.data.mer_config_info.bank_card_config` | 银联卡配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.mer_config_info.bank_card_config.debit_fee_rate` | 借记卡手续费（%） | `String` | `9` | `Y` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]； 示例值：0.60 |
| `response.data.mer_config_info.bank_card_config.debit_fee_limit` | 借记卡封顶值 | `String` | `9` | `N` | 数字类型，大于0保留2位小数； 示例值：20.00 |
| `response.data.mer_config_info.bank_card_config.credit_fee_rate` | 贷记卡手续费（%） | `String` | `9` | `Y` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.90 |
| `response.data.mer_config_info.bank_card_config.open_flag` | 允许开通银行卡业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.bank_card_config.cloud_debit_fee_rate_up` | 银联手机闪付借记卡手续费1000以上（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.bank_card_config.cloud_debit_fee_limit_up` | 银联手机闪付借记卡封顶1000以上（元） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；示例值：20.00 |
| `response.data.mer_config_info.bank_card_config.cloud_credit_fee_rate_up` | 银联手机闪付贷记卡手续费1000以上（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.bank_card_config.cloud_debit_fee_rate_down` | 银联手机闪付借记卡手续费1000以下（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.bank_card_config.cloud_debit_fee_limit_down` | 银联手机闪付借记卡封顶1000以下（元） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；示例值：20.00 |
| `response.data.mer_config_info.bank_card_config.cloud_credit_fee_rate_down` | 银联手机闪付贷记卡手续费1000以下（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.split_config` | 分账配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.mer_config_info.split_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.split_config.fee_fix_amt` | 固定手续费(元) | `String` | `9` | `N` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.split_config.open_flag` | 允许开通分账业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.wx_zl_conf_list[]` | 微信直连配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.mer_config_info.wx_zl_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 1、微信直连小程序；2、微信直连公众号；3、微信直连H5；示例值：1 |
| `response.data.mer_config_info.wx_zl_conf_list[].fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.wx_zl_conf_list[].open_flag` | 允许开通微信直连业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.ali_zl_conf` | 支付宝直连配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.mer_config_info.ali_zl_conf.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.ali_zl_conf.open_flag` | 允许开通支付宝直连业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.online_fee_conf_list[]` | 线上配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.mer_config_info.online_fee_conf_list[].bus_type` | 业务类型 | `String` | `2` | `Y` | 1.网银支付，； 2.快捷支付，； 3.手机WAP支付；4：B2B网银充值 ；5：B2C网银充值，；6：代扣支付； 示例值：1 |
| `response.data.mer_config_info.online_fee_conf_list[].dc_flag` | 借贷记标识 | `String` | `2` | `Y` | D:借记,C:贷记；B2B网银填写D；示例值：D |
| `response.data.mer_config_info.online_fee_conf_list[].fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.online_fee_conf_list[].bank_code` | 银行号 | `String` | `8` | `Y` | 8位银行号 |
| `response.data.mer_config_info.online_fee_conf_list[].fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.online_fee_conf_list[].open_flag` | 允许开通线上支付业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.balance_pay_config` | 余额支付配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.mer_config_info.balance_pay_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.balance_pay_config.fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.balance_pay_config.open_flag` | 允许开通余额支付业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.combine_pay_config` | 补贴支付配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.mer_config_info.combine_pay_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.combine_pay_config.fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.combine_pay_config.open_flag` | 允许开通补贴支付业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.bank_big_amt_pay_config` | 银行大额转账配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.mer_config_info.bank_big_amt_pay_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.bank_big_amt_pay_config.fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.bank_big_amt_pay_config.open_flag` | 允许开通大额转账业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.out_order_funds_config` | 全域资金管理配置（华通）对象 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.mer_config_info.out_order_funds_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.out_order_funds_config.open_fee_fix_amt` | 开户手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.out_order_funds_config.fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.out_order_funds_config.open_flag` | 允许开通全域资金（华通）业务 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.out_order_funds_su_shang_config` | 全域资金管理配置(苏商)对象 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.mer_config_info.out_order_funds_su_shang_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.out_order_funds_su_shang_config.fee_min_amt` | 保底手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.out_order_funds_su_shang_config.public_fee_fix_amt` | 对公固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.out_order_funds_su_shang_config.private_fee_fix_amt` | 对私固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.out_order_funds_su_shang_config.open_flag` | 允许开通全域资金业务(苏商) | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.out_order_funds_new_net_config` | 全域资金管理配置(新网)对象 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.mer_config_info.out_order_funds_new_net_config.fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.out_order_funds_new_net_config.fee_min_amt` | 保底手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.out_order_funds_new_net_config.public_fee_fix_amt` | 对公固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.out_order_funds_new_net_config.private_fee_fix_amt` | 对私固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.out_order_funds_new_net_config.open_flag` | 允许开通全域资金业务(新网) | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.settle_config_list[]` | 结算配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.mer_config_info.settle_config_list[].bus_type` | 业务类型 | `String` | `2` | `Y` | D1：下个自然日到账，；T1：下个工作日到账；TS：笔笔到账；示例值：T1 |
| `response.data.mer_config_info.settle_config_list[].fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.settle_config_list[].fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.settle_config_list[].open_flag` | 允许开通结算配置 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.cash_config_list[]` | 取现配置对象 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.mer_config_info.cash_config_list[].bus_type` | 业务类型 | `String` | `2` | `Y` | D0：当日到账；当日交易资金当天可取现到账；T1：下个工作日到账;；D1：下个自然日到账;；DM：当日到账；到账资金不包括当天的交易资金；示例值：T1 |
| `response.data.mer_config_info.cash_config_list[].fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.mer_config_info.cash_config_list[].fee_fix_amt` | 固定手续费(元) | `String` | `9` | `Y` | 单位元，需保留小数点后两位，示例值：1.00，最低传入0.00 |
| `response.data.mer_config_info.cash_config_list[].open_flag` | 允许开通取现配置 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.out_fee_config[]` | 外扣配置对象 | `String` | `—` | `N` | jsonArray字符串 |
| `response.data.mer_config_info.out_fee_config[].settle_out_fee_flag` | 支持结算手续费外扣 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.out_fee_config[].trans_fee_out_flag` | 支持交易手续费外扣 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.out_fee_config[].cash_out_fee_flag` | 支持取现手续费外扣 | `String` | `1` | `Y` | Y：是，N：否，示例值：Y |
| `response.data.mer_config_info.alipay_pre_auth_flag` | 是否开通支付宝预授权 | `String` | `1` | `N` | 支付宝预授权开通；Y：是，N：否 |
| `response.data.mer_config_info.wechatpay_pre_auth_flag` | 开通微信预授权 | `String` | `1` | `N` | 微信预授权开通；Y：是，N：否 |
| `response.data.mer_config_info.mer_timing_settle_flag` | 是否开通商户定时结算 | `String` | `1` | `N` | 定时结算开通；Y：是，N：否 |
| `response.data.mer_config_info.mer_prior_settle_flag` | 是否开通商户优先结算 | `String` | `1` | `N` | 优先结算开通；Y：是，N：否 |
| `response.data.mer_config_info.use_upper_mer_auth_flag` | 是否使用上级商户经营信息 | `String` | `1` | `N` | 开通下级商户时支持复用上级的经营信息；Y：是，N：否 |
| `response.data.mer_config_info.use_upper_mer_at_trans_flag` | 是否使用上级商户号发起AT交易 | `String` | `1` | `N` | 开通下级商户时支持复用上级的微信、支付宝商户号信息；Y：是，N：否 |
| `response.data.elec_acct_config` | 斗拱e账户功能配置 | `String` | `—` | `N` | 用于总部商户、商户配置斗拱E账户功能 |
| `response.data.elec_acct_config.switch_state` | 电子账户开关 | `String` | `1` | `Y` | 电子账户开通总开关；0:关闭 1:开通；示例值：1 |
| `response.data.elec_acct_config.acct_type` | 账户类型 | `String` | `2` | `Y` | 01：中信e管家；示例值：01 |
| `response.data.elec_acct_config.cash_fee_party` | 电子账户提现手续费承担方 | `String` | `1` | `Y` | 1:总部 2:其他；示例值：1 |
| `response.data.elec_acct_config.scene` | 场景类型 | `String` | `3` | `Y` | 必填，与角色类型关联，[中信定义的资金类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；示例值：001 |
| `response.data.elec_acct_config.role_type` | 角色类型 | `String` | `6` | `Y` | 角色编号必填；与场景关联，[中信定义的角色类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；示例值：001001 |
| `response.data.elec_acct_config.elec_card_list[]` | 银行卡信息 | `String` | `—` | `N` | jsonArray字符串 |
| `response.data.elec_acct_config.elec_card_list[].prov_id` | 银行所在省 | `String` | `6` | `N` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310000 |
| `response.data.elec_acct_config.elec_card_list[].area_id` | 银行所在市 | `String` | `6` | `N` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)示例值：310100 |
| `response.data.elec_acct_config.elec_card_list[].bank_code` | 银行编码 | `String` | `8` | `Y` | [参考银行编码；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)示例值：01020000 |
| `response.data.elec_acct_config.elec_card_list[].bank_name` | 银行名称 | `String` | `64` | `Y` | 示例值：中国工商银行 |
| `response.data.elec_acct_config.elec_card_list[].branch_code` | 支行联行号 | `String` | `12` | `Y` | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `response.data.elec_acct_config.elec_card_list[].branch_name` | 支行名称 | `String` | `64` | `Y` | 示例值：中国工商银行上海市中山北路支行 |
| `response.data.elec_acct_config.elec_card_list[].card_name` | 结算账户名 | `String` | `128` | `Y` | 银行卡对应的户名；示例值：上海汇付支付有限公司 |
| `response.data.elec_acct_config.elec_card_list[].card_no` | 银行卡号 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `response.data.elec_acct_config.elec_card_list[].card_type` | 卡类型 | `String` | `1` | `Y` | 0:对公 1:对私法人 |
| `response.data.elec_acct_config.elec_card_list[].default_cash_flag` | 默认卡标识 | `String` | `1` | `N` | 0：非默认卡 1：默认卡 |
| `response.data.elec_acct_config.elec_card_list[].token_no` | 卡序列号 | `String` | `20` | `N` | — |
| `response.data.elec_acct_config.elec_card_list[].mp` | 银行绑定手机号 | `String` | `11` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.elec_acct_config.elec_card_list[].auth_version` | 用户授权协议版本号 | `String` | `64` | `N` | 示例值：43563223 |
| `response.data.elec_acct_config.elec_card_list[].auth_no` | 用户授权协议号 | `String` | `64` | `N` | 示例值：654745222213 |
| `response.data.elec_acct_config.elec_card_list[].status` | 卡状态 | `String` | `1` | `Y` | 绑卡状态，:N-正常，C-关闭，D-注销；示例值：N |
| `response.data.elec_acct_config.elec_card_list[].bind_card_msg` | 绑卡返回描述 | `String` | `256` | `Y` | 示例值：成功 |
| `response.data.elec_acct_config.bank_status` | 电子账户开通状态 | `String` | `1` | `Y` | S：成功 F：失败；示例值：S |
| `response.data.elec_acct_config.bank_message` | 银行信息 | `String` | `512` | `Y` | 示例值：成功 |
| `response.data.elec_acct_config.merchant_id` | 银行会员编号 | `String` | `15` | `N` | 示例值：J00000000000001 |
| `response.data.tax_config` | 灵活用工配置 | `String` | `—` | `N` | jsonObject字符串 |
| `response.data.tax_config.open_tax_flag` | 是否开通灵活用工 | `String` | `1` | `N` | Y:开通, N或空:不开通；示例值：Y |
| `response.data.tax_config.open_tax_state` | 灵活用工开户状态 | `String` | `1` | `N` | 1-待开户，2 开户成功待签约，3-开户失败， 4-签约成功， 5-签约失败；示例值：2 |
| `response.data.tax_config.open_tax_state_desc` | 灵活用工开户状态描述 | `String` | `256` | `N` | 示例值：签约成功 |
| `response.data.online_refund` | 是否开通在线退款 | `String` | `1` | `N` | N：否 Y：是；示例值：Y |
| `response.data.platform_refund` | 是否支持平台退款 | `String` | `1` | `N` | N：否 Y：是；示例值：Y |
| `response.data.support_revoke` | 是否支持撤销 | `String` | `1` | `N` | N：否 Y：是；示例值：Y |
| `response.data.split_bill_result[]` | 分账配置信息 | `String` | `—` | `N` | jsonArray字符串 |
| `response.data.split_bill_result[].rule_origin` | 分账规则来源 | `String` | `2` | `N` | 01 接口发起 02页面配置；示例值：01 |
| `response.data.split_bill_result[].repeal_flag` | 分账是否支持撤销交易 | `String` | `1` | `N` | Y：支持，N：不支持；示例值：Y |
| `response.data.split_bill_result[].refund_flag` | 分账是否支持退货交易 | `String` | `1` | `N` | Y：支持，N：不支持；示例值：Y |
| `response.data.split_bill_result[].div_flag` | 分账开关 | `String` | `1` | `N` | Y：开，N：关；示例值：Y |
| `response.data.split_bill_result[].apply_ratio` | 最大分账比例% | `Number` | `9` | `N` | 0-100 的数值，支持两位小数; 示例值：20.00 |
| `response.data.split_bill_result[].acct_split_bunch_list[]` | 分账明细 | `String` | `—` | `N` | jsonArray格式；分账规则来源选择平台配置时必填,jsonObject字符串 |
| `response.data.split_bill_result[].acct_split_bunch_list[].fee_rate` | 分账比例 | `String` | `9` | `N` | 百分比支持两位小数，示例值：0.20 |
| `response.data.split_bill_result[].acct_split_bunch_list[].huifu_id` | 汇付Id | `String` | `18` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.split_bill_result[].out_fee_flag` | 交易手续费外扣开关 | `String` | `1` | `N` | 1:外扣 2:内扣（默认）；示例值：1 |
| `response.data.split_bill_result[].out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户(默认)，02-现金户，05-充值户；示例值：01 |
| `response.data.split_bill_result[].out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 选择手续费外扣时必填；示例值： |
| `response.data.split_bill_result[].split_fee_rate` | 手续费% | `String` | `9` | `N` | 百分比，支持两位小数；示例值：1.00 |
| `response.data.split_bill_result[].per_amt` | 固定手续费 | `String` | `9` | `N` | 单位元，支持小数点后两位；示例值：1.00 |
| `response.data.split_bill_result[].scene` | 分账模式 | `String` | `2` | `N` | 00-其他；01-医美医院分账；A1- 教培机构分账；A2-公办/民办学校分账；A3-医美渠道独立收款分账；A4-线上供应商货款；A5-线上推广方（渠道/代理/个人）的服务佣金/抽成；A7-入驻商户货款；A8-线下供应商货款；A9-线下推广方；A10-个人与合作方分账；单选；示例值：A9 |
| `response.data.split_bill_result[].split_ext_info` | 业务情况说明 | `String` | `128` | `N` | jsonObject；分账模式选择则其它，分账比例20%以上必填 |
| `response.data.split_bill_result[].split_ext_info.busi_instruction` | 业务模式说明 | `String` | `500` | `Y` | 请详细说明商户的业务模式，包括不限于（业务参与方、各方的权利及义务关系等）。最大500个汉字，必填；示例值：商户向企业采购产品，并将其展示在其电商平台上，用户注册后购买其产品，产品主要有家电、服饰、鞋帽等，用户购买产品的资金作为商户所得，商户根据订单情况进行物流配送。 |
| `response.data.split_bill_result[].split_ext_info.capital_instruction` | 资金流向说明 | `String` | `500` | `Y` | 请详细说明商户的资金流向，包括但不限于（交易所涉及的各方账户、资金流入流出过程等）。最大500个汉字，必填；示例值：用户选购产品后根据订单支付给商户，商户根据结算周期，结算到对公账户。 |
| `response.data.split_bill_result[].split_ext_info.function_instruction` | 功能开通用途说明 | `String` | `500` | `Y` | 请详述所申请功能的原因、场景、涉及对象类型。最大500个汉字，必填；示例值：企业工资代发 |
| `response.data.share_holder_info_list[]` | 股东信息 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.share_holder_info_list[].share_holder_id` | 股东编号 | `String` | `32` | `N` | 修改时必填；示例值： |
| `response.data.share_holder_info_list[].name` | 股东姓名 | `String` | `32` | `N` | 示例值：张三 |
| `response.data.share_holder_info_list[].cert_type` | 股东证件类型 | `String` | `2` | `N` | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》；支持00~11，以及12:营业执照；示例值：12 |
| `response.data.share_holder_info_list[].cert_validity_type` | 股东证件有效期类型 | `String` | `1` | `N` | 1:长期有效 0:非长期有效；示例值：1 |
| `response.data.share_holder_info_list[].cert_begin_date` | 股东证件有效期起始日 | `String` | `8` | `N` | 格式yyyyMMdd；示例值：20201223 |
| `response.data.share_holder_info_list[].cert_end_date` | 股东证件有效期到期日 | `String` | `8` | `N` | 格式yyyyMMdd; 非长期有效时必填；示例值：20301223 |
| `response.data.share_holder_info_list[].state` | 股东状态 | `String` | `1` | `N` | 1:有效 0:无效；示例值：1 |
| `response.data.share_holder_info_list[].mobile_no` | 股东手机号 | `String` | `11` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.head_office_flag` | 是否总部商户 | `String` | `1` | `N` | 1：总部， 0：分店，默认总部。示例值：0 |
| `response.data.uni_app_payment_config` | 银联线上收银台 | `String` | `—` | `N` | jsonObject字符串 |
| `response.data.uni_app_payment_config.switch_state` | 状态开关 | `String` | `1` | `N` | 0-关闭; 1-开通, 为空默认开通；示例值：1 |
| `response.data.uni_app_payment_config.debit_fee_rate` | 借记手续费（%） | `String` | `6` | `C` | 借记卡费率与贷记卡费率不能同时为空;；保留2位小数，最大值100.00，最小值0.00；示例值：0.02 |
| `response.data.uni_app_payment_config.credit_fee_rate` | 贷记手续费（%） | `String` | `6` | `C` | 借记卡费率与贷记卡费率不能同时为空;；保留2位小数，最大值100.00，最小值0.00；示例值：0.06 |
| `response.data.uni_app_payment_config.out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；示例值：1 ；如果不为空，则out_fee_acct_type，out_fee_huifuid，out_fee_flag取单独配置，否则取公共配置 |
| `response.data.uni_app_payment_config.out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填；示例值：[官网示例已脱敏] |
| `response.data.uni_app_payment_config.out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户，02-现金户，05-充值户，09-营销户；不填默认01；示例值：01 |
| `response.data.uni_app_payment_config.fee_charge_type` | 交易手续费收取类型 | `String` | `1` | `N` | 1:实收 2:后收；示例值：1 |
| `response.data.uni_app_payment_config.cloud_quick_pass_secret_free_flag` | 云闪付免密支付开通标识 | `String` | `1` | `N` | Y-开通/N-关闭 ；示例值：Y |
| `response.data.surrogate_config_list[]` | 代发配置 | `String` | `—` | `N` | jsonArray格式字符串 |
| `response.data.surrogate_config_list[].switch_state` | 开通状态 | `String` | `1` | `N` | 1:是 0:否, 为空默认开；示例值：1 |
| `response.data.surrogate_config_list[].surrogate_type` | 代发业务类型 | `String` | `2` | `N` | D0:当日到账；T1:下个工作日到账;；D1:下个自然日到账;；示例值：T1 |
| `response.data.surrogate_config_list[].fix_amt` | 手续费（固定/元） | `String` | `17` | `C` | 手续费（固定/元），保留小数点后两位；fee_formula_type为05，06时必填 示例值：1.00 |
| `response.data.surrogate_config_list[].fee_rate` | 手续费（百分比/%） | `String` | `6` | `C` | 手续费（百分比/%），保留小数点后两位；取值范围[0.00,100.00]；fee_formula_type为01，02，03，06时必填 示例值：0.05 |
| `response.data.surrogate_config_list[].out_fee_flag` | 是否交手续费外扣标记 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；优先级高于相同名称的公共参数；示例值：1 |
| `response.data.surrogate_config_list[].out_fee_acct_type` | 交易手续费外扣时账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01；优先级高于相同名称的公共参数 |
| `response.data.surrogate_config_list[].out_fee_huifu_id` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填，示例值：[官网示例已脱敏]；优先级高于相同名称的公共参数 |
| `response.data.surrogate_config_list[].surrogate_private_flag` | 是否允许对私代发 | `String` | `1` | `N` | 是否允许代发卡为对私类型；Y:允许 N:不允许；示例值：Y |
| `response.data.surrogate_config_list[].fee_formula_type` | 代发手续费计费模式 | `String` | `2` | `N` | 01: 百分比手续费，无封顶值或保底值；02: 百分比手续费，有保底值；03: 百分比手续费，有封顶值；05: 固定手续费 ；06: 固定手续费+百分比手续费；为空默认06 示例值：06 |
| `response.data.surrogate_config_list[].fee_max_amt` | 手续费封顶值（固定/元） | `String` | `17` | `C` | 手续费封顶值（固定/元），保留小数点后两位；fee_formula_type为03时必填 示例值：100.00 |
| `response.data.surrogate_config_list[].fee_min_amt` | 手续费保底值（固定/元） | `String` | `17` | `C` | 手续费保底值（固定/元），保留小数点后两位；fee_formula_type为02时必填 示例值：1.00 |
| `response.data.large_amt_pay_config` | 大额支付配置 | `String` | `—` | `N` | jsonObject字符串 内容参考：large_amt_pay_config |
| `response.data.large_amt_pay_config.large_amt_pay_config_info_list[]` | 大额支付配置列表 | `String` | `—` | `N` | 大额支付配置列表，jsonArray格式 |
| `response.data.large_amt_pay_config.large_amt_pay_config_info_list[].switch_state` | 功能开关 | `String` | `1` | `N` | 1:开通 0:关闭 默认：1；示例值：1 |
| `response.data.large_amt_pay_config.large_amt_pay_config_info_list[].business_model` | 大额支付业务模式 | `String` | `15` | `Y` | 大额支付业务模式 bank：银行模式 provisions：备付金模式；示例值：bank |
| `response.data.large_amt_pay_config.large_amt_pay_config_info_list[].fee_rate` | 费率（%） | `String` | `6` | `C` | 开通大额业务时必须填写一种收费方式；大于0,保留2位小数；示例值：1.00 |
| `response.data.large_amt_pay_config.large_amt_pay_config_info_list[].fee_fix_amt` | 交易手续费（固定/元） | `String` | `9` | `C` | 开通大额业务时必须填写一种收费方式；大于0,保留2位小数；示例值：10.00 |
| `response.data.large_amt_pay_config.large_amt_pay_config_info_list[].biz_type` | 大额调账标识申请类型 | `String` | `2` | `N` | 01-四要素，05-三要素；[订单匹配的要素信息](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_ddppys)；示例值：05 |
| `response.data.large_amt_pay_config.large_amt_pay_config_info_list[].mer_same_card_recharge_flag` | 是否允许绑卡支付 | `String` | `1` | `N` | Y-开通/N-关闭，备付金模式时，支持传入；备付金模式银行卡绑定支付权限；示例值：Y |
| `response.data.large_amt_pay_config.large_amt_pay_config_info_list[].allow_user_deposit_flag` | 是否允许用户入账 | `String` | `1` | `N` | Y-开通/N-关闭 ；默认为N；示例值：Y |
| `response.data.large_amt_pay_config.large_amt_pay_config_info_list[].provisions_auto_refund_flag` | 备付金固定账号模式自动退款 | `String` | `1` | `N` | Y-开通/N-关闭 ；示例值：Y；该配置仅在开通大额支付备付金绑卡模式时生效 |
| `response.data.large_amt_pay_config.out_fee_flag` | 交易手续费外扣标记 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；示例值：1 |
| `response.data.large_amt_pay_config.out_fee_huifu_id` | 交易手续费外扣huifuId | `String` | `18` | `C` | 交易手续费外扣时必填；示例值：[官网示例已脱敏] |
| `response.data.large_amt_pay_config.out_fee_acct_id` | 交易手续费外扣账户号 | `String` | `16` | `C` | 交易手续费外扣时必填；示例值：F00598602 |
| `response.data.large_amt_pay_config.mer_payer_card_type` | 商户付款方卡类型 | `String` | `10` | `N` | CORPORATE-对公,PRIVATE-对私,ALL-全部，默认全部；示例值：ALL |
| `response.data.half_pay_host_flag` | 统一收银台开关 | `String` | `1` | `N` | Y:是 N:否（为空默认未开通） ；示例值：Y |
| `response.data.mer_stat` | 商户状态 | `String` | `32` | `N` | NORMAL：正常 FREEZEWITHDRAWAL：冻结出金 CANCEL：注销 FREEZEDEPOSIT：冻结入金；示例值：NORMAL |
| `response.data.agent_recheck_config` | 代发复核 | `String` | `—` | `N` | jsonObject字符串 |
| `response.data.agent_recheck_config.agent_recheck_flag` | 代发复核开关 | `String` | `1` | `N` | Y:是 N:否（为空默认未开通） ；示例值：Y |
| `response.data.agent_recheck_config.agent_recheck_huifu_id` | 复核授权商户号 | `String` | `18` | `N` | 复核授权商户号只能填当前商户主体或总部商户号 |
| `response.data.agent_recheck_config.agent_recheck_type` | 复核类型 | `String` | `1` | `N` | A:复核 B:短信验证 |
| `response.data.online_recharge_flag` | 商户开通网银充值开关 | `String` | `1` | `N` | 1:开通 0:未开通，为空未配置(未开通);示例值：1 |
| `response.data.lla_withhold_config` | 本地生活 | `String` | `—` | `N` | jsonObject字符串 |
| `response.data.lla_withhold_config.fee_rate` | 佣金收取手续费率 | `String` | `9` | `Y` | — |
| `response.data.lla_withhold_config.lla_withhold_flag` | 本地生活配置开关 | `String` | `1` | `Y` | Y:开通,N:关闭；示例值：N |
| `response.data.refund_mend_open_flag` | 是否开通垫资退款 | `String` | `1` | `N` | Y:是 N:否 ；示例值：Y |
| `response.data.jxf_conf_info` | 捷行付配置 | `String` | `—` | `N` | jsonObject字符串 |
| `response.data.jxf_conf_info.bank_pay_open_flag` | 银行模式开关 | `String` | `—` | `N` | Y-开通 N-关闭 |
| `response.data.jxf_conf_info.jxf_bank_pay_info` | 银行模式配置 | `Object` | `—` | `N` | 银行模式配置 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.acct_type` | 账户类型 | `String` | `—` | `N` | 2:银行账户 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.bank_name` | 银行名称 | `String` | `—` | `N` | PINGAN-平安银行 BOC-中国银行；示例值：PINGAN |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info` | 银行账户信息 | `Object` | `—` | `N` | — |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.user_name` | 操作人姓名 | `String` | `—` | `N` | 示例：张三 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.operator_phone` | 操作人手机号 | `String` | `—` | `N` | 示例：[官网示例已脱敏] |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.acct_type` | 付款方账户类型 | `String` | `—` | `N` | 00：单位结算卡，不填默认单位结算卡 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.acct_no` | 付款方账号 | `String` | `—` | `N` | 示例：[官网示例已脱敏] |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.acct_name` | 付款方账户名称 | `String` | `—` | `N` | 示例：上海汇付支付有限公司 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.bank_branch_code` | 开户行联行号 | `String` | `—` | `N` | 示例：991290000099 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.bank_branch_name` | 开户行行名 | `String` | `—` | `N` | 示例：中国银行 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.sign_start_date` | 签约申请生效日期 | `String` | `—` | `N` | 示例：20261219 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.sign_end_date` | 签约申请失效日期 | `String` | `—` | `N` | 示例：20261219 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.remark` | 附言 | `String` | `—` | `N` | 示例：附言 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.org_code` | 机构编码 | `String` | `—` | `N` | 示例：12133 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info` | 手续费信息 | `Object` | `—` | `N` | — |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.open_card_fix_fee` | 虚拟卡开卡手续费（元） | `String` | `—` | `N` | 单位元，支持小数点后两位；示例值：1.00 虚拟卡开卡手续费收取方式为发放数量*固定手续费 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.quota_issue_fee_rate` | 虚拟卡额度发放手续费（%） | `String` | `—` | `N` | 百分比，支持两位小数；示例值：1.00 虚拟卡发放额度手续费收取方式为交易金额*费率手续费 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.out_fee_flag` | 捷行付手续费内外扣标记 | `String` | `—` | `N` | 1外扣 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.out_fee_huifuid` | 捷行付手续费外扣汇付ID | `String` | `—` | `N` | 捷行付手续费外扣汇付ID |
| `response.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.out_fee_acct_type` | 捷行付手续费扣款账户类型 | `String` | `—` | `N` | 捷行付手续费扣款账户类型 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.bank_resp_desc` | 业务开通状态 | `String` | `—` | `N` | S：成功 P:处理中 F:失败 |
| `response.data.jxf_conf_info.jxf_bank_pay_info.bank_status` | 业务开通状态 | `String` | `—` | `N` | S：成功 P:处理中 F:失败 |
| `response.data.jxf_conf_info.wx_ent_pay_open_flag` | 微信企业码模式开关 | `String` | `—` | `N` | Y-开通 N-关闭 |
| `response.data.jxf_conf_info.wx_ent_pay_info` | 微信企业码模式配置 | `Object` | `—` | `N` | — |
| `response.data.jxf_conf_info.wx_ent_pay_info.payment_background` | 付款背景介绍 | `String` | `—` | `N` | — |
| `response.data.jxf_conf_info.wx_ent_pay_info.apply_scenes` | 适用场景 | `String` | `—` | `N` | 1-企业差旅 2-因公宴请 3-会员积分 4-小额采购 5-商报直付 |
| `response.data.jxf_conf_info.wx_ent_pay_info.sub_mch_id` | 微信商户号 | `String` | `—` | `N` | 微信商户号 |
| `response.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info` | 微信企业码手续费信息 | `Object` | `—` | `N` | 微信企业码手续费信息 |
| `response.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.open_card_fix_fee` | 虚拟卡开卡手续费（元） | `String` | `—` | `N` | 虚拟卡开卡手续费（元） |
| `response.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.quota_issue_fee_rate` | 虚拟卡额度发放手续费（%） | `String` | `—` | `N` | 虚拟卡额度发放手续费（%） |
| `response.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.out_fee_flag` | 捷行付手续费内外扣标记 | `String` | `—` | `N` | 1外扣 |
| `response.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.out_fee_huifuid` | 捷行付手续费外扣汇付ID | `String` | `—` | `N` | 捷行付手续费外扣汇付ID |
| `response.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.out_fee_acct_type` | 捷行付手续费扣款账户类型 | `String` | `—` | `N` | 捷行付手续费扣款账户类型 |
| `response.data.jxf_conf_info.default_channel` | 默认通道 | `String` | `—` | `N` | 1-银行通道 2-微信企业码 |
| `response.data.merge_pay_config_info` | 合单支付配置信息 | `String` | `—` | `N` | jsonObject字符串 |
| `response.data.merge_pay_config_info.merge_pay_flag` | 合单支付开关 | `String` | `1` | `Y` | 合单支付开关 Y：开通 N：关闭 |
| `response.data.merge_pay_config_info.merge_pay_config` | 合单支付配置 | `Object` | `—` | `C` | 合单支付配置 （当合单支付开关为开时必填） |
| `response.data.merge_pay_config_info.merge_pay_config.merge_pay_mode` | 合单支付模式 | `String` | `1` | `Y` | 1:电商 2:加油站 3:停车场 4:物业 5:休闲娱乐 |
| `response.data.bill_payment_flag` | 是否开通账单支付 | `String` | `1` | `N` | Y:是 N:否 ；示例值：Y |
| `response.data.activated_products` | 产品大类 | `String` | `32` | `N` | 收款产品，02 账户与资金产品，03 业财数通产品；不传为空示例值：01,02,03 |
| `response.data.withhold_pay_scene` | 代扣场景 | `String` | `1` | `N` | 1:权益投流(订阅),2:非权益投流(订阅),3:保险缴纳,4:道路通行费(ETC),5:公共事业(水电煤)缴费,6:物业缴费 |
| `response.data.material_card_info` | 对公卡信息 | `String` | `—` | `N` | jsonObject字符串 |
| `response.data.material_card_info.card_type` | 银行账户类型 | `String` | `1` | `N` | 0：对公 |
| `response.data.material_card_info.card_name` | 银行账户名称 | `String` | `128` | `N` | — |
| `response.data.material_card_info.card_no` | 对公银行账号 | `String` | `32` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.material_card_info.prov_id` | 银行所在省 | `String` | `6` | `N` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310000 |
| `response.data.material_card_info.area_id` | 银行所在市 | `String` | `6` | `N` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)示例值：310100 |
| `response.data.material_card_info.branch_code` | 支行联行号 | `String` | `12` | `N` | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `response.data.qry_dy_conf_list[]` | 抖音支付配置信息 | `Array` | `—` | `N` | jsonArray格式 |
| `response.data.qry_dy_conf_list[].fee_rate` | 手续费（%） | `String` | `9` | `N` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.qry_dy_conf_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `9` | `N` | 固定金额保留2位小数；大于0。需要渠道商开通此功能。示例值：0.38 |
| `response.data.qry_dy_conf_list[].fee_charge_type` | 交易手续费收取类型 | `String` | `1` | `N` | 1:实收,2:后收；示例值：1 |
| `response.data.qry_dy_conf_list[].out_fee_flag` | 交易手续费外扣标记 | `String` | `1` | `N` | 1：外扣，2：内扣；（默认2内扣）；示例值：2 |
| `response.data.qry_dy_conf_list[].out_fee_huifu_id` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填，示例值：[官网示例已脱敏]；优先级高于相同名称的公共参数 |
| `response.data.qry_dy_conf_list[].out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `Y` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01；优先级高于相同名称的公共参数 |
| `response.data.qry_dy_conf_list[].dy_mer_infos` | 抖音商户号信息 | `String` | `—` | `N` | 参见下文描述 |
| `response.data.qry_dy_conf_list[].dy_mer_infos.bank_mer_code` | 银联商户号 | `String` | `32` | `N` | 商户在银联开通的抖音)商户号；示例值：2234544 |
| `response.data.qry_dy_conf_list[].dy_mer_infos.nucc_bank_mer_code` | 网联商户号 | `String` | `3` | `N` | 商户在网联开通的抖音)商户号；示例值：2234544 |
| `response.data.qry_dy_conf_list[].dy_mer_infos.sub_mer_id` | 二级商户号 | `String` | `32` | `N` | 示例值：6634423544 |
| `response.data.qry_dy_conf_list[].switch_state` | 功能开关 | `String` | `1` | `N` | 1:开通 0:关闭 |

## 申请单状态查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_sqdztcx.md>
- SHA-256：`8c39b88e199d2c877267994172fa09de5130c47d38eb5f01147d2d1520c2bef4`
- 说明：下表保留官方字段类型、长度、必填标记和字段说明；数组父路径以 `[]` 标记。

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
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 业务申请编号，同一商户号当天唯一；示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 格式yyyyMMdd，以北京时间为准。示例值：20220125 |
| `request.data.apply_no` | 申请单 | `String` | `18` | `Y` | 汇付返回商户的申请单号；参见商户基本信息入驻、业务开通等接口返回的apply_no；示例值：[官网示例已脱敏] |
| `request.data.huifu_id` | 汇付客户Id | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] |

### 响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务响应码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务响应信息 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.huifu_id` | 商户号 | `String` | `18` | `N` | 汇付分配的商户号，示例值：[官网示例已脱敏] |
| `response.data.reg_name` | 商户注册名称 | `String` | `128` | `N` | 商户注册名称；示例值：上海汇付支付服务有限公司 |
| `response.data.apply_reason` | 审核意见 | `String` | `512` | `N` | 审核意见 |
| `response.data.apply_status` | 申请单审核状态 | `String` | `1` | `N` | Y：审核通过，P：审核中，N：审核拒绝，F：系统处理失败；示例值：Y |
| `response.data.bank_card_conf_reason` | 银行卡业务开通描述 | `String` | `512` | `N` | 如银行卡业务开通失败，返回失败原因 |
| `response.data.bank_card_conf_status` | 银行卡支付业务开通状态 | `String` | `1` | `N` | P:处理中 S:成功 F:失败；示例值：S |
| `response.data.bank_sub_mer_id` | 银行卡银联商户号 | `String` | `20` | `N` | 银行卡银联商户号，示例值：66345234544 |
| `response.data.bind_card_status` | 绑卡状态 | `String` | `1` | `N` | P:处理中 S:成功 F:失败；示例值：P |
| `response.data.cash_status` | 取现配置状态 | `String` | `1` | `N` | P:处理中 S:成功 F:失败；示例值：P |
| `response.data.reg_status` | 商户入驻汇付状态 | `String` | `1` | `N` | P:处理中 S:成功 F:失败；示例值：P |
| `response.data.settle_status` | 结算配置状态 | `String` | `1` | `N` | P:处理中 S:成功 F:失败 ；示例值：P |
| `response.data.union_sub_mer_id` | 银联二维码银联商户号 | `String` | `20` | `N` | 银联二维码银联商户号，示例值：66345234544 |
| `response.data.union_conf_reason` | 银联二维码业务开通描述 | `String` | `512` | `N` | 如银联二维码业务开通失败，返回失败原因 |
| `response.data.union_conf_status` | 银联二维码业务开通状态 | `String` | `1` | `N` | P:处理中 S:成功 F:失败；示例值：P |
| `response.data.ali_conf_result_list[]` | 支付宝配置结果集合 | `String` | `—` | `N` | jsonArray格式；调用商户业务开通、商户业务开通修改接口，申请单支付宝业务配置会返回 |
| `response.data.ali_conf_result_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 1线下扫码；示例值：1 |
| `response.data.ali_conf_result_list[].pay_channel_id` | 子渠道号 | `String` | `50` | `N` | 不填入驻到渠道默认配置的支付宝渠道号下；示例值：JP00001 |
| `response.data.ali_conf_result_list[].sub_mer_id` | 二级商户号 | `String` | `32` | `N` | 在汇付做支付宝入驻时，汇付端生成的唯一二级商户号；示例值：A[官网示例已脱敏] |
| `response.data.ali_conf_result_list[].sub_mer_name` | 二级商户名 | `String` | `60` | `N` | 二级商户名 ；示例值：上海汇付支付服务有限公司 |
| `response.data.ali_conf_result_list[].ali_bank_mer_code` | 支付宝商户号 | `String` | `20` | `N` | 支付宝银行商户号；示例值：2234544 |
| `response.data.ali_conf_result_list[].ali_conf_reason` | 支付宝业务开通描述 | `String` | `512` | `N` | 支付宝业务开通描述 |
| `response.data.ali_conf_result_list[].ali_conf_status` | 支付宝业务开通状态 | `String` | `1` | `N` | P:处理中 S:成功 F:失败；示例值：S |
| `response.data.ali_conf_result_list[].fq_flag` | 分期标志 | `String` | `1` | `N` | 1：分期业务；示例值：1 |
| `response.data.ali_conf_result_list[].real_name_applyment_stat` | 实名认证状态 | `String` | `64` | `N` | 申请实名时返回；审核中(AUDITING)；待联系人确认(CONTACT_CONFIRM)；待法人确认(LEGAL_CONFIRM)；审核通过(AUDIT_PASS)；审核失败(AUDIT_REJECT)；已冻结(AUDIT_FREEZE)；已撤回(CANCELED)；未申请(NOT_APPLY)；示例值： |
| `response.data.ali_conf_result_list[].real_name_applyment_desc` | 实名认证描述 | `String` | `128` | `N` | 申请实名时返回；示例值： |
| `response.data.ali_conf_result_list[].qrcode_data` | 授权二维码 | `String` | `128` | `N` | 若实名认证状态 real_name_applyment_stat=；CONTACT_CONFIRM、LEGAL_CONFIRM时返回；示例值：https://qr.alipay.com/bax02911brluc2xieoph6001 |
| `response.data.wx_conf_result_list[]` | 微信配置结果集合 | `String` | `—` | `N` | jsonArray格式；调用商户业务开通、商户业务开通修改接口，申请单微信业务配置会返回 |
| `response.data.wx_conf_result_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 参见《[微信支付场景](https://paas.huifu.com/partners/api/doc/api_ggcsbm.md#微信支付场景)（官网相对地址原文：`api_ggcsbm.md#微信支付场景`）》说明 ；示例值：1 |
| `response.data.wx_conf_result_list[].pay_channel_id` | 子渠道号 | `String` | `50` | `N` | 不填入驻到渠道默认配置的微信渠道号下；示例值：JP00001 |
| `response.data.wx_conf_result_list[].sub_mer_id` | 二级商户号 | `String` | `32` | `N` | 在汇付做微信入驻时，汇付端生成的唯一二级商户号；示值值：W[官网示例已脱敏] |
| `response.data.wx_conf_result_list[].sub_mer_name` | 二级商户名 | `String` | `60` | `N` | 二级商户名 ；示例值：上海汇付支付服务有限公司 |
| `response.data.wx_conf_result_list[].wx_bank_mer_code` | 微信银行商户号 | `String` | `20` | `N` | 微信银行商户号；示例值：66345234544 |
| `response.data.wx_conf_result_list[].wx_conf_reason` | 微信业务开通描述 | `String` | `512` | `N` | 微信业务开通描述 |
| `response.data.wx_conf_result_list[].wx_conf_status` | 微信业务开通状态 | `String` | `1` | `N` | P:处理中 S:成功 F:失败；示例值：S |
| `response.data.wx_conf_result_list[].real_name_applyment_stat` | 实名认证状态 | `String` | `64` | `N` | 申请实名时返回；APPLYMENT_STATE_EDITTING--【编辑中】--可能在提交申请时发生错误导致，可用同一个业务申请编号重新提交；APPLYMENT_STATE_WAITTING_FOR_AUDIT--【审核中】--请耐心等待1~2个工作日，微信支付将会完成审核；APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT--【待确认联系信息】--请扫描微信支付返回的小程序码确认联系信息(此过程可修改超级管理员手机号)；APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON--【待账户验证】--请扫描微信支付返回的小程序码在小程序端完成账户验证；APPLYMENT_STATE_PASSED--【审核通过】--请扫描微信支付返回的小程序码在小程序端完成授权流程；APPLYMENT_STATE_REJECTED--【审核驳回】--请按照驳回原因修改申请资料，并更换业务申请编码，重新提交申请；APPLYMENT_STATE_FREEZED--【已冻结】--可能是该主体已完成过入驻，请查看驳回原因，并通知驳回原因中指定的联系人扫描微信支付返回的小程序码在小程序端完成授权流程；APPLYMENT_STATE_CANCELED--【已作废】--表示申请单已被撤销，无需再对其进行操作；APPLYMENT_STATE_NOAPPLY--未申请；示例值：APPLYMENT_STATE_WAITTING_FOR_AUDIT |
| `response.data.wx_conf_result_list[].real_name_applyment_desc` | 实名认证描述 | `String` | `128` | `N` | 申请实名时返回；示例值： |
| `response.data.wx_conf_result_list[].qrcode_data` | 授权二维码 | `String` | `128` | `N` | 若实名认证状态 real_name_applyment_stat=；APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT、；APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON、；APPLYMENT_STATE_PASSED、；APPLYMENT_STATE_FREEZED时返回；示例值：https://qr.alipay.com/bax02911brluc2xieoph6001 |
| `response.data.zft_apply_result_list[]` | 支付宝直付通申请结果集合 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.zft_apply_result_list[].apply_time` | 申请单创建时间 | `String` | `20` | `N` | 示例值：2017/11/11 12:00 |
| `response.data.zft_apply_result_list[].card_alias_no` | 进件生成的卡编号 | `String` | `32` | `N` | 进件生成的卡编号，在发起结算时可以作为结算账号 |
| `response.data.zft_apply_result_list[].fk_audit` | 风控审核状态 | `String` | `10` | `N` | CREATE：已创建待审批、SKIP：跳过风控审批步骤、PASS：风控审核通过、REJECT：风控审批拒绝；示例值：CREATE |
| `response.data.zft_apply_result_list[].fk_audit_memo` | 风控审批备注 | `String` | `64` | `N` | 风控审批备注，如有则返回 |
| `response.data.zft_apply_result_list[].kz_audit` | 支付宝业务开通状态 | `String` | `64` | `N` | CREATE：已创建待审批、SKIP：跳过客资审批步骤、PASS：客资审核通过、REJECT：客资审批拒绝；示例值：CREATE |
| `response.data.zft_apply_result_list[].kz_audit_memo` | 客资审批备注 | `String` | `64` | `N` | 客资审批备注，如有则返回 |
| `response.data.zft_apply_result_list[].merchant_name` | 进件时填写的商户名称 | `String` | `64` | `N` | 进件时填写的商户名称；示例值：上海汇付支付服务有限公司 |
| `response.data.zft_apply_result_list[].smid` | 二级商户id | `String` | `32` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.zft_apply_result_list[].sub_confirm` | 二级商户确认状态 | `String` | `16` | `N` | CREATE：已发起二级商户确认、SKIP：无需确认、FAIL：签约失败、NOT_CONFIRM：商户未确认、FINISH签约完成；示例值：CREATE |
| `response.data.combine_pay_config` | 补贴支付 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.combine_pay_config.switch_state` | 开通状态 | `String` | `1` | `Y` | 0:关闭 1:开通；示例值：1 |
| `response.data.combine_pay_config.fee_rate` | 支付手续费(%) | `String` | `9` | `N` | 支付手续费(%) 支持两位小数；示例值：0.38 |
| `response.data.combine_pay_config.fee_fix_amt` | 支付固定手续费(元) | `String` | `9` | `N` | 支付固定手续费(元)支持两位小数；示例值：1.00 |
| `response.data.wx_config_list[]` | 微信配置状态结果集 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.wx_config_list[].config_type` | 配置类型 | `String` | `2` | `Y` | 01 -公众号配置 02-小程序配置 |
| `response.data.wx_config_list[].config_value` | 配置值 | `String` | `1` | `Y` | S-成功,F-失败，B-部分成功 |
| `response.data.account_name` | 银行账户名 | `String` | `128` | `N` | 全域资金管理开通的银行账户名；示例值：上海汇付支付服务有限公司 |
| `response.data.electron_account` | 银行收款电子账号 | `String` | `32` | `N` | 全域资金管理开的银行电子账号；示例值： |
| `response.data.out_order_funds_status` | 银行收款入账状态 | `String` | `1` | `N` | 全域资金管理功能涉及字段； P：处理中S：成功F：失败；示例值：P |
| `response.data.out_order_funds_desc` | 银行收款入账描述 | `String` | `256` | `N` | 全域资金管理功能涉及字段；只返回错误描述；示例值： |
| `response.data.wx_zl_config` | 微信直连配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `response.data.wx_zl_config.sub_mch_id` | 特约商户号 | `String` | `32` | `N` | 示例值：1632157057 |
| `response.data.wx_zl_config.sales_scenes_type` | 经营场景类型 | `String` | `32` | `Y` | 线下门店：SALES_SCENES_STORE；公众号：SALES_SCENES_MP；小程序：SALES_SCENES_MINI_PROGRAM；互联网：SALES_SCENES_WEB；APP：SALES_SCENES_APP；企业微信：SALES_SCENES_WEWORK；示例值：SALES_SCENES_WEWORK |
| `response.data.wx_zl_config.confirm_url` | 超级管理员签约链接 | `String` | `512` | `N` | 示例值：https://www.huifu.com |
| `response.data.wx_zl_config.apply_state` | 申请单状态 | `String` | `32` | `N` | S：审核通过，P：审核中，N：审核拒绝，F：系统处理失败；C：待签约；示例值：S |
| `response.data.wx_zl_config.reject_reason` | 拒绝原因 | `String` | `256` | `N` | 示例值：支付功能未开通 |
| `response.data.wx_zl_config.mod_bank_acct_state` | 结算卡修改结果返回码 | `String` | `1` | `N` | S:成功 F失败；示例值：S |
| `response.data.wx_zl_config.mod_bank_acct_desc` | 结算卡修改结果返回描述 | `String` | `256` | `N` | 示例值：成功 |
| `response.data.ali_zl_config[]` | 支付宝直连配置列表 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.ali_zl_config[].apply_status` | 申请单状态 | `String` | `1` | `N` | S：审核通过，P：审核中，N：审核拒绝，F：系统处理失败；C：待签约；示例值：S |
| `response.data.ali_zl_config[].confirm_url` | 签约链接 | `String` | `256` | `N` | 示例值：https://www.huifu.com |
| `response.data.ali_zl_config[].mer_app_id` | 应用ID | `String` | `32` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.ali_zl_config[].reject_reason` | 拒绝原因 | `String` | `128` | `N` | 示例值：未开通支付 |
| `response.data.ali_zl_config[].mer_code` | 支付宝商户号 | `String` | `32` | `N` | 示例值：[官网示例已脱敏] |
| `response.data.ali_zl_config[].apply_type` | 申请类型 | `String` | `32` | `N` | FACE_TO_FACE：当面付；示例值：FACE_TO_FACE |
| `response.data.change_settle_state` | 意愿核实状态 | `String` | `1` | `N` | F：拒绝/失败 S：成功/通过 P：等待处理 C：已撤销（控台操作）；当【变更结算人核验方式 = 1】时返回意愿核实状态。；示例值：S |
| `response.data.agreement_info_list[]` | 协议信息 | `String` | `—` | `N` | 签署电子协议时返回 jsonArray格式 |
| `response.data.agreement_info_list[].agreement_link` | 协议签署连接 | `String` | `1024` | `N` | 申请实名且签署电子协议时返回；示例值： |
| `response.data.agreement_info_list[].agreement_id` | 协议编号 | `String` | `64` | `N` | 申请实名且签署电子协议时返回；示例值： |
| `response.data.agreement_info_list[].agreement_name` | 协议名称 | `String` | `256` | `N` | 申请实名且签署电子协议时返回；示例值： |
| `response.data.agreement_info_list[].con_stat` | 合同状态 | `String` | `2` | `N` | 电子协议类型会返回以下值：；2：创建合同异常；3：待签约 ；4：签约中；5：签约完成(电子协议只有签约完成才能做交易) ；6：已失效 ； 7：已拒签； 8：签约失败；示例值：5 |
| `response.data.agreement_info_list[].agreement_type` | _协议类型_ | `String` | `1` | `N` | 0-电子协议 |
| `response.data.agreement_info_list[].agreement_no` | 协议号 | `String` | `32` | `N` | 示例值：3245234 |

## 商户业务开通修改

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md>
- SHA-256：`3f9e0e6b302807646b4a7a02830ef50ae4c6b90f5fab1ddea9eaeb72d12c5cf4`
- 说明：下表保留官方字段类型、长度、必填标记和字段说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商或商户的huifu_id；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为总部商户时，此字段填写商户huifu_id |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：YYZY |
| `request.sign` | 加签结果 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/docs/start/#/api_v2jqyq) |
| `request.data` | 数据 | `Json` | `—` | `Y` | 业务请求参数，具体值参考API文档 |

### 响应信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/docs/start/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 业务申请编号，同一商户号当天唯一，示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 请求日期：yyyyMMdd，以北京时间为准；示例值：20220904 |
| `request.data.huifu_id` | 汇付客户Id | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] |
| `request.data.short_name` | 微信支付宝商户简称 | `String` | `64` | `N` | 修改微信、支付宝商户简称；示例值：汇付天下 |
| `request.data.agreement_info` | *协议信息实体* | `String` | `—` | `C` | jsonObject字符串；[签约协议材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%95%86%E6%88%B7%E5%90%88%E5%90%8C%E7%AD%BE%E7%BA%A6%E8%A7%84%E5%88%99.xlsx)；若未签署过协议的情况下，调用该接口时必填；若已签署过纸质或电子协议下，调用该接口时必填，且只可以选择纸质或电子协议；若已签署过挂网协议下，调用该接口时，选填。 |
| `request.data.agreement_info.agreement_type` | *协议类型* | `String` | `1` | `Y` | 0-电子协议 1-纸质协议 3-挂网协议；示例值：3；退出地区且开通（银联二维码或刷卡业务）不支持挂网协议；如果业务开通时选了纸质或电子，变更时也不支持挂网协议 |
| `request.data.agreement_info.agreement_url` | *挂网协议地址* | `String` | `256` | `C` | 挂网协议必填；**必须按示例值填写**，示例值：https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/PaymentServiceAgreement.htm |
| `request.data.agreement_info.agree_begin_date` | 纸质协议开始日期 | `String` | `8` | `N` | 格式yyyyMMdd，示例值：20220822 |
| `request.data.agreement_info.agree_end_date` | 纸质协议结束日期 | `String` | `8` | `N` | 格式yyyyMMdd，示例值：20230822 |
| `request.data.agreement_info.message_send_type` | 电子协议签约短信发送标识 | `String` | `1` | `N` | 协议类型为电子，业务开通审核通过后发送协议签约短信；0：发送，默认；1：不发送；示例值：1 |
| `request.data.agreement_info.agreement_async_return_url` | 电子协议异步通知地址 | `String` | `128` | `N` | 示例值：http://service.example.com/to/path |
| `request.data.out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1：外扣，2：内扣；（默认2内扣）示例值：2 该公共参数只影响：支付宝支付，微信支付，抖音支付，银行卡支付，银联二维码支付，花呗分期配置 以下支付方式手续费请在各配置域字段中修改：网银、快捷、手机WAP、余额支付、补贴支付、全域资金管理、银行大额转账 |
| `request.data.out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填；示例值：[官网示例已脱敏] 该公共参数只影响：支付宝支付，微信支付，抖音支付，银行卡支付，银联二维码支付，花呗分期配置 以下支付方式手续费请在各配置域字段中修改：网银、快捷、手机WAP、余额支付、补贴支付、全域资金管理、银行大额转账 |
| `request.data.out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01：基本户（不填默认01），02-现金户，05：充值户；09：营销户；示例值：01 该公共参数只影响：支付宝支付，微信支付，抖音支付，银行卡支付，银联二维码支付，花呗分期配置 以下支付方式手续费请在各配置域字段中修改：网银、快捷、手机WAP、余额支付、补贴支付、全域资金管理、银行大额转账 |
| `request.data.online_flag` | 是否开通网银 | `String` | `1` | `N` | Y:是 N:否；示例值：Y |
| `request.data.quick_flag` | 是否开通快捷 | `String` | `1` | `N` | Y：是， N：否；示例值：Y |
| `request.data.withhold_flag` | 是否开通代扣 | `String` | `1` | `N` | Y:是 N:否；示例值：Y |
| `request.data.delay_flag` | 延迟入账开关 | `String` | `1` | `N` | N：否，Y：是；默认否；示例值：Y |
| `request.data.alipay_pre_auth_flag` | 开通支付宝预授权 | `String` | `1` | `N` | Y：是，N：否；示例值：Y；目前仅支持MCC为7011住宿服务、7296服装出租、7512汽车出租三个行业开通预授权 |
| `request.data.wechatpay_pre_auth_flag` | 开通微信预授权 | `String` | `1` | `N` | Y：是，N：否；示例值：Y；目前仅支持MCC为7011住宿服务、7296服装出租、7512汽车出租三个行业开通预授权 |
| `request.data.mer_bus_type` | 商户业务类型 | `String` | `2` | `N` | 快捷，网银，手机WAP，银联统一在线收银台开通时（线上费率配置对象不为空）必填；取值参见[商户业务类型](http://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E5%95%86%E6%88%B7%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B)（官网原始地址为非 HTTPS，不得静默改写）；示例值：01 |
| `request.data.online_fee_conf_list[]` | 线上费率配置 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.online_fee_conf_list[].fee_type` | 业务类型 | `String` | `25` | `N` | ONLINE_PERSON:个人网银支付，online_flag开通了才需要填；ONLINE_ENT:企业网银支付，online_flag开通了才需要填；QUICK_DEBIT:快捷借记卡支付，quick_flag开通了才需要填；QUICK_CREDIT:快捷贷记卡支付，quick_flag开通了才需要填；WAP:手机WAP支付，online_flag开通了才需要填；ONLINE_ENT_TOP_UP:B2B网银充值，online_recharge_flag开通了才需要填；ONLINE_PERSON_TOP_UP:B2C网银充值，online_recharge_flag开通了才需要填；WITHHOLD_DEBIT:代扣借记卡支付；WITHHOLD_CREDIT:代扣贷记卡支付，withhold_flag开通了才需要填；示例值：ONLINE_PERSON |
| `request.data.online_fee_conf_list[].bank_id` | 银行编码 | `String` | `8` | `N` | 参考： [银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；示例值：01020000 |
| `request.data.online_fee_conf_list[].dc_flag` | 借贷标志 | `String` | `1` | `N` | D:借记,C:贷记；示例值：D |
| `request.data.online_fee_conf_list[].fix_amt` | 手续费（固定/元） | `String` | `16` | `N` | 必须填写一种收费方式；保留两位小数；保留两位小数；示例值：1.00 |
| `request.data.online_fee_conf_list[].fee_rate` | 费率（%） | `String` | `6` | `N` | 必须填写一种收费方式；保留两位小数；示例值：0.38 |
| `request.data.online_fee_conf_list[].bank_name` | 银行名称 | `String` | `50` | `N` | 示例值：中国工商银行上海市中山北路支行 |
| `request.data.online_fee_conf_list[].bank_short_chn` | 银行中文简称 | `String` | `50` | `N` | 示例值：工行上海市中北支行 |
| `request.data.online_fee_conf_list[].stat_flag` | 费率状态 | `String` | `1` | `N` | 1开，0关；示例值：1 |
| `request.data.online_fee_conf_list[].fee_min_amt` | 手续费最小值（元） | `String` | `6` | `N` | 必须填写一种收费方式；保留两位小数；保留两位小数；示例值：1.00 |
| `request.data.online_fee_conf_list[].fee_formula_type` | 代扣手续费计费模式 | `String` | `—` | `N` | withhold_flag为Y时，才可传入；01: 百分比手续费，无封顶值或保底值；02: 百分比手续费，有保底值；03: 固定手续费；04: 固定手续费+百分比手续费；为空默认04 示例值：04 |
| `request.data.ali_conf_list[]` | 支付宝配置对象 | `String` | `—` | `N` | jsonArray格式字符串 |
| `request.data.ali_conf_list[].fee_rate` | 手续费（%） | `String` | `9` | `N` | 数字类型，大于0,保留2位小数；示例值：0.38 |
| `request.data.ali_conf_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `6` | `N` | 固定金额保留2位小数；大于0。需要渠道商开通此功能。示例值：0.38 |
| `request.data.ali_conf_list[].mcc` | 商户经营类目 | `String` | `32` | `N` | 支付宝商户经营类目，[支付宝MCC](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_zfbmcc) ；示例值：5411 |
| `request.data.ali_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `N` | 1、线下扫码，2.线上扫码，3.非盈利费率；示例值：1 |
| `request.data.ali_conf_list[].pay_channel_id` | 子渠道号 | `String` | `50` | `N` | 不填入驻到渠道默认配置的支付宝渠道号下；示例值：JP00001 |
| `request.data.ali_conf_list[].switch_state` | *功能开关* | `String` | `2` | `Y` | 1:开通 0:关闭 示例值：1 |
| `request.data.ali_conf_list[].is_check_real_name` | 是否需要实名认证 | `String` | `1` | `N` | Y-是，业务功能开通成功后使用法人信息发起实名认证申请；N-否；默认为N；示例值：Y |
| `request.data.ali_conf_list[].al_real_name_info` | 实名认证信息 | `String` | `—` | `N` | 实名时需要填写；jsonObject字符串 ；若请求支付宝入驻成功，但实名申请失败需要调用单独的实名接口重新发起实名。 |
| `request.data.ali_conf_list[].al_real_name_info.finance_institution_flag` | 是否金融机构 | `String` | `5` | `N` | 选填，请根据申请主体的实际情况填写；1、若商户主体是金融机构，则填写：true。；2、若商户主体不是金融机构，则填写：false。；若未传入将默认填写：false；3，支付宝实名金融机构需要提供 F236：金融机构许可证图片一 ；F237：金融机构许可证图片二；F238：金融机构许可证图片三；F239：金融机构许可证图片四；F240：金融机构许可证图片五；补充资料填写在extended_material_list对象中；示例值：true |
| `request.data.ali_conf_list[].al_real_name_info.finance_type` | 金融机构类型 | `String` | `128` | `N` | 当主体是金融机构时，必填；金融机构类型需与营业执照/登记证书上一致；BANK_AGENT：银行业, 适用于商业银行、政策性银行、农村合作银行、村镇银行、开发性金融机构等；PAYMENT_AGENT：支付机构, 适用于非银行类支付机构；INSURANCE：保险业, 适用于保险、保险中介、保险代理、保险经纪等保险类业务；TRADE_AND_SETTLE：交易及结算类金融机构, 适用于交易所、登记结算类机构、银行卡清算机构、资金清算中心等；OTHER：其他金融机构, 适用于财务公司、信托公司、金融资产管理公司、金融租赁公司、汽车金融公司、贷款公司、货币经纪公司、消费金融公司、证券业、金融控股公司、股票、期货、货币兑换、小额贷款公司、金融资产管理、担保公司、商业保理公司、典当行、融资租赁公司、财经咨询等其他金融业务；示例值：BANK_AGENT |
| `request.data.ali_conf_list[].al_real_name_info.cert_type` | 证书类型 | `String` | `64` | `N` | 企业商户必填；枚举：；统一社会信用代码证书(CERTIFICATE_TYPE_2389)；慈善组织公开募捐资格证书(CERTIFICATE_TYPE_2397)；社会团体法人登记证书(CERTIFICATE_TYPE_2394)；民办非企业单位登记证书(CERTIFICATE_TYPE_2395)；基金会法人登记证书(CERTIFICATE_TYPE_2396)；农民专业合作社法人营业执照(CERTIFICATE_TYPE_2398)；宗教活动场所登记证(CERTIFICATE_TYPE_2399)；其他证书/批文/证明(CERTIFICATE_TYPE_2400)；示例值：CERTIFICATE_TYPE_2389；政府机关/事业单位/其他组织 对应需要补充单位证明函照片 文件类型F46；补充资料填写在extended_material_list对象中；示例值：CERTIFICATE_TYPE_2395 |
| `request.data.ali_conf_list[].al_real_name_info.micro_biz_type` | 小微经营类型 | `String` | `32` | `N` | 小微经营类型 必填字段；门店场所：MICRO_TYPE_STORE；流动经营/便民服务：MICRO_TYPE_MOBILE；线上商品/服务交易：MICRO_TYPE_ONLINE；个人商户需要填写；示例值：MICRO_TYPE_STORE；需要提供 F22：店铺门头照图片；F24：店铺内景图片； 补充资料填写在extended_material_list对象中 |
| `request.data.ali_conf_list[].al_real_name_info.special_category_id` | 特殊行业id | `String` | `20` | `N` | 特殊行业必填，参见支付宝商家行业二级类目code；1，支付宝实名特殊行业提供 F150:行业经营许可证资质照片一；F151:行业经营许可证资质照片二；F152:行业经营许可证资质照片三；F153:行业经营许可证资质照片四；F154:行业经营许可证资质照片五；F155:行业经营许可证资质照片六；补充资料填写在extended_material_list对象中；示例值：100 |
| `request.data.ali_conf_list[].al_real_name_info.contact_person_info` | 联系人信息对象 | `String` | `—` | `N` | — |
| `request.data.ali_conf_list[].al_real_name_info.contact_person_info.name` | 联系人姓名 | `String` | `64` | `N` | 为空时取企业商户取联系人姓名，个人商户取入驻时填写的名称；示例值：张三 |
| `request.data.ali_conf_list[].al_real_name_info.contact_person_info.mobile` | 联系人手机号 | `String` | `64` | `N` | 为空时取企业商户取联系人手机号；示例值：[官网示例已脱敏] |
| `request.data.ali_conf_list[].al_real_name_info.contact_person_info.id_card_number` | 联系人身份证号码 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info` | 法人身份信息 | `String` | `—` | `N` | — |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.legal_type` | 证件持有人类型 | `String` | `32` | `N` | 法人：LEGAL，为空时默认选项； 主体类型为企业、个体户、社会组织、小微商户时，必须为经营者/法人。；经办人：SUPER；主体类型为政府机关、事业单位时默认是法人。若因特殊情况，无法提供法人证件时可填经办人类型。；示例值：LEGAL |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.card_type` | 证件类型 | `String` | `32` | `N` | 枚举值：00:身份证 01:护照 13：港澳居民证 14:台湾居民证；为空时取开户时法人信息；个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关、小微商户仅支持身份证类型。；示例值：00 |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.person_name` | 姓名 | `String` | `64` | `N` | 为空时取开户时法人信息；示例值：李四 |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.card_no` | 证件号码 | `String` | `64` | `N` | 为空时取开户时法人信息；示例值：[官网示例已脱敏] |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.effect_time` | 证件生效时间 | `String` | `32` | `N` | 为空时取开户时法人信息；示例值：19990101 |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.expire_time` | 证件过期时间 | `String` | `32` | `N` | 为空时取开户时法人信息；示例值：20001101，长期有效时传“长期” |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.card_front_img` | 证件正面照 | `String` | `128` | `N` | 为空时取开户时法人信息，如果开户时未传该字段必填；上送图片上传返回的jfileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.card_back_img` | 证件反面照 | `String` | `128` | `N` | 为空时取开户时法人信息，如果开户时未传该字段必填；只有身份证类型需要上传反面；上送图片上传返回的jfileId；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.auth_letter_img` | 授权函照片 | `String` | `128` | `N` | 上送图片上传返回的jfileId；文件类型F224业务办理授权函；当证件持有人类型为经办人时必须上传。其他情况，无需上传。示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.ali_conf_list[].al_real_name_info.legal_person_info.is_benefit_person` | 是否为受益人 | `String` | `1` | `N` | Y-受益人;N-非受益人 默认值：Y；示例值：Y |
| `request.data.wx_conf_list[]` | 微信配置对象 | `String` | `—` | `N` | jsonArray格式字符串 |
| `request.data.wx_conf_list[].switch_state` | 开关状态 | `String` | `1` | `Y` | 1:开通，0关闭；示例值：1 |
| `request.data.wx_conf_list[].fee_rate` | 手续费（%） | `String` | `9` | `N` | 数字类型，大于0,保留2位小数；示例值：0.38 |
| `request.data.wx_conf_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `6` | `N` | 固定金额保留2位小数；大于0。需要渠道商开通此功能。示例值：0.38 |
| `request.data.wx_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `N` | 参见《[微信支付场景](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e6%94%af%e4%bb%98%e5%9c%ba%e6%99%af)》说明；示例值：1 |
| `request.data.wx_conf_list[].fee_rule_id` | 费率规则ID | `String` | `3` | `N` | [微信费率规则](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wxflgz)，简称cid。示例值：758 |
| `request.data.wx_conf_list[].pay_channel_id` | 子渠道号 | `String` | `32` | `N` | 不填入驻到渠道默认配置的微信渠道号下；示例值：JP00001 |
| `request.data.wx_conf_list[].service_codes` | 申请服务 | `String` | `100` | `N` | 微信(JSAPI:JSAPI支付,APPLET:小程序支付,MICROPAY:付款码支付,APP:app支付,MWEB:H5支付,PAP:委托代扣支付,AUTH:授权平台代扣支付),；示例值:[JSPAI","APPLET",MICROPAY"]；默认值为:[JSPAI","APPLET","MICROPAY"] |
| `request.data.wx_conf_list[].is_check_real_name` | 是否需要实名认证 | `String` | `1` | `N` | Y-是，业务功能开通成功后使用法人信息发起实名认证申请 ； N-否；默认为N ;示例值：Y |
| `request.data.wx_conf_list[].wx_real_name_info` | 实名认证信息 | `String` | `—` | `N` | 实名时需要填写 jsonObject字符串 ；若请求微信入驻成功，实名申请失败需要调用单独的实名接口重新发起实名。 |
| `request.data.wx_conf_list[].wx_real_name_info.finance_institution_flag` | 是否金融机构 | `String` | `5` | `N` | 选填，请根据申请主体的实际情况填写，可参考选择：https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html；1、若商户主体是金融机构，则填写：true。；2、若商户主体不是金融机构，则填写：false。；若未传入将默认填写：false；3，微信实名金融机构需要提供 F236：金融机构许可证图片一 ；F237：金融机构许可证图片二；F238：金融机构许可证图片三；F239：金融机构许可证图片四；F240：金融机构许可证图片五；补充资料填写在extended_material_list对象中；示例值：false |
| `request.data.wx_conf_list[].wx_real_name_info.finance_type` | 金融机构类型 | `String` | `128` | `N` | 当主体是金融机构时，必填；金融机构类型需与营业执照/登记证书上一致，可参考选择金融机构指引：；https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html；BANK_AGENT：银行业, 适用于商业银行、政策性银行、农村合作银行、村镇银行、开发性金融机构等；PAYMENT_AGENT：支付机构, 适用于非银行类支付机构；INSURANCE：保险业, 适用于保险、保险中介、保险代理、保险经纪等保险类业务；TRADE_AND_SETTLE：交易及结算类金融机构, 适用于交易所、登记结算类机构、银行卡清算机构、资金清算中心等；OTHER：其他金融机构, 适用于财务公司、信托公司、金融资产管理公司、金融租赁公司、汽车金融公司、贷款公司、货币经纪公司、消费金融公司、证券业、金融控股公司、股票、期货、货币兑换、小额贷款公司、金融资产管理、担保公司、商业保理公司、典当行、融资租赁公司、财经咨询等其他金融业务；示例值：INSURANCE |
| `request.data.wx_conf_list[].wx_real_name_info.cert_type` | 证书类型 | `String` | `64` | `N` | 企业商户必填；CERTIFICATE_TYPE_2388：事业单位法人证书；CERTIFICATE_TYPE_2389：统一社会信用代码证书；CERTIFICATE_TYPE_2394：社会团体法人登记证书；CERTIFICATE_TYPE_2395：民办非企业单位登记证书；CERTIFICATE_TYPE_2396：基金会法人登记证书；CERTIFICATE_TYPE_2399：宗教活动场所登记证；CERTIFICATE_TYPE_2400：其他证书/批文/证明；CERTIFICATE_TYPE_2520：执业许可证/执业证；CERTIFICATE_TYPE_2521：基层群众性自治组织特别法人统一社会信用代码证；CERTIFICATE_TYPE_2522：农村集体经济组织登记证；主体为政府机关/其他组织/事业单位时,F46：单位证明函照片必填；主体为政府机关/其他组织/事业单位时,F45：登记证书必填；补充资料填写在extended_material_list对象中；示例值：CERTIFICATE_TYPE_2389 |
| `request.data.wx_conf_list[].wx_real_name_info.micro_biz_type` | 小微经营类型 | `String` | `32` | `N` | 小微经营类型 必填字段；门店场所：MICRO_TYPE_STORE；流动经营/便民服务：MICRO_TYPE_MOBILE；线上商品/服务交易：MICRO_TYPE_ONLINE；个人商户需要填写；示例值：MICRO_TYPE_STORE ；需要提供 F22：店铺门头照图片；F24：店铺内景图片； 补充资料填写在extended_material_list对象中 |
| `request.data.wx_conf_list[].wx_real_name_info.special_category_id` | 特殊行业id | `String` | `3` | `N` | 特殊行业必填，参看微信支付提供的特殊行业id对照表：；https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/applysubject_new/chapter6_1.shtml；1，微信实名特殊行业提供 F150:行业经营许可证资质照片一；F151:行业经营许可证资质照片二；F152:行业经营许可证资质照片三；F153:行业经营许可证资质照片四；F154:行业经营许可证资质照片五；F155:行业经营许可证资质照片六；补充资料填写在extended_material_list对象中；示例值：100 |
| `request.data.wx_conf_list[].wx_real_name_info.contact_type` | 联系人类型 | `String` | `10` | `N` | LEGAL：经营者/法人；SUPER：经办人（经商户授权办理微信支付业务的人员），默认：LEGAL；1、主体为“小微/个人卖家”，可选择：LEGAL；2、主体为“个体工商户/企业/政府机关/事业单位/社会组织”，可选择：LEGAL、SUPER 示例值：LEGAL；联系人类型为SUPER时需在extended_material_list文件列表中上传联系人证件正反面照片；F28：联系人身份证正面照；F29：联系人身份证反面照；F33：联系人**护照**人像面；F241：联系人证件照正面，非身份证与护照类型；F242：联系人证件照反面，非身份证类型 |
| `request.data.wx_conf_list[].wx_real_name_info.name` | 联系人姓名 | `String` | `64` | `C` | 联系人类型contact_type=SUPER时必填。示例值：张三 |
| `request.data.wx_conf_list[].wx_real_name_info.mobile` | 联系人手机号 | `String` | `11` | `C` | 联系人类型contact_type=SUPER时必填。示例值：[官网示例已脱敏] |
| `request.data.wx_conf_list[].wx_real_name_info.contact_id_doc_type` | 联系人证件类型 | `String` | `10` | `C` | 联系人类型contact_type=SUPER时必填。；枚举值参见《自然人证件类型》说明，示例值：00；个体户/企业/事业单位/社会组织：可选择任一证件类型，政府机关仅支持身份证类型。 |
| `request.data.wx_conf_list[].wx_real_name_info.id_card_number` | 联系人证件号码 | `String` | `32` | `C` | 联系人类型contact_type=SUPER时必填。示例值：[官网示例已脱敏] |
| `request.data.wx_conf_list[].wx_real_name_info.contact_period_begin` | 联系人证件有效期开始时间 | `String` | `20` | `C` | 联系人类型contact_type=SUPER时必填；格式：yyyy-MM-dd；示例值：2019-06-06 |
| `request.data.wx_conf_list[].wx_real_name_info.contact_period_end` | 联系人证件有效期结束时间 | `String` | `20` | `C` | 联系人类型contact_type=SUPER时必填；格式：yyyy-MM-dd；示例值：2029-06-06；结束时间大于开始时间;若证件有效期为长期，请填写：长期 |
| `request.data.union_conf_list[]` | 银联二维码配置对象 | `String` | `—` | `N` | jsonArray格式字符串 |
| `request.data.union_conf_list[].charge_cate_code` | 银行业务手续费类型 | `String` | `2` | `N` | 01：减免类；02：优惠类；03：标准类，默认标准类 。（小微商户仅有03标准类）；04：线上类；示例值：03 |
| `request.data.union_conf_list[].switch_state` | 功能开关 | `String` | `2` | `N` | 1:开通 0:关闭 默认：1；示例值：1 |
| `request.data.union_conf_list[].debit_fee_rate` | 借记卡手续费（%） | `String` | `9` | `N` | 数字格式，大于等于0，保留2位小数；示例值：0.38 |
| `request.data.union_conf_list[].credit_fee_rate_up` | 贷记卡手续费1000以上（%） | `String` | `9` | `N` | 数字格式，大于等于0，保留2位小数；示例值：0.60 |
| `request.data.union_conf_list[].credit_fee_rate_down` | 贷记卡手续费1000及以下（%） | `String` | `9` | `N` | 数字格式，大于等于0，保留2位小数；示例值：0.60 |
| `request.data.bank_card_conf` | 银行卡支付配置信息 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.bank_card_conf.charge_cate_code` | 银行业务手续费类型 | `String` | `2` | `N` | 01：减免类；02：优惠类；03：标准类（默认03）；示例值：03 |
| `request.data.bank_card_conf.debit_fee_rate` | 借记卡手续费（%） | `String` | `9` | `Y` | 数字类型，大于0,保留2位小数；示例值：0.50代表费率为0.5% |
| `request.data.bank_card_conf.debit_fee_limit` | 借记卡封顶值 | `String` | `4` | `N` | 数字类型，大于0,保留2位小数；示例值：5.00 |
| `request.data.bank_card_conf.credit_fee_rate` | 贷记卡手续费（%） | `String` | `9` | `Y` | 数字类型，大于0,保留2位小数；示例值：0.60代表费率为0.6% |
| `request.data.bank_card_conf.is_open_small_flag` | 是否开通小额双免 | `String` | `1` | `N` | 开关状态；0：不开通双免；1：开通双免；2：仅免签；示例值：1 |
| `request.data.bank_card_conf.small_free_amt` | 小额双免单笔限额(元) | `String` | `9` | `N` | 限额需小于等于1000，不传默认0（不开通小额双免）；示例值：1000.00 |
| `request.data.bank_card_conf.small_fee_amt` | 小额双免手续费（%） | `String` | `9` | `N` | 数字类型，大于0,保留2位小数，开通小额双免填必须填制；示例值：0.38代表费率为0.38% |
| `request.data.bank_card_conf.switch_state` | 功能开关 | `String` | `2` | `N` | 1:开通 0:关闭 默认：1；示例值：1 |
| `request.data.bank_card_conf.is_open_cloud_flag` | 云闪付开通状态 | `String` | `1` | `N` | 0-关闭 1-开通 |
| `request.data.balance_pay_config` | *余额支付配置对象* | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.balance_pay_config.fee_rate` | 支付手续费(%) | `String` | `9` | `N` | 支持两位小数 fee_rate与fee_fix_amt不能同时为空；示例值：0.50代表费率为0.5% |
| `request.data.balance_pay_config.fee_fix_amt` | 支付固定手续费(元) | `String` | `9` | `N` | 支持两位小数 fee_rate与fee_fix_amt不能同时为空；示例值：1.50；注：如果fee_fix_amt与fee_rate都填写了则手续费=fee_fix_amt+支付金额\*fee_rate |
| `request.data.balance_pay_config.switch_state` | 功能开关 | `String` | `2` | `N` | 1:开通 0:关闭 默认：1；示例值：1 |
| `request.data.balance_pay_config.out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01；优先级高于相同名称的公共参数 |
| `request.data.balance_pay_config.out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填，示例值：[官网示例已脱敏]；优先级高于相同名称的公共参数 |
| `request.data.balance_pay_config.out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣），示例值：1；优先级高于相同名称的公共参数 |
| `request.data.balance_pay_config.balance_model` | *业务模式* | `String` | `1` | `Y` | 2-入驻商户货款（周期性结算）；3-营销补贴（周期性结算）；4-推广方（渠道/代理/个人）的服务佣金/抽成；5-红包发放；6-钱包功能；7-其他模式；8-线上入驻商户货款（周期性结算）；9-线上营销补贴（周期性结算）；10-线上推广方（渠道/代理/个人）的服务佣金/抽成；11-线上其他模式；单选；示例值：6 |
| `request.data.balance_pay_config.description_info` | *业务情况说明* | `String` | `—` | `Y` | jsonObject字符串 |
| `request.data.balance_pay_config.description_info.busi_instruction` | *业务模式说明* | `String` | `500` | `C` | 请详细说明商户的业务模式，包括不限于（业务参与方、各方的权利及义务关系等）。最大500个汉字，必填；示例值：商户向企业采购产品，并将其展示在其电商平台上，用户注册后购买其产品，产品主要有家电、服饰、鞋帽等，用户购买产品的资金作为商户所得，商户根据订单情况进行物流配送。 |
| `request.data.balance_pay_config.description_info.capital_instruction` | *资金流向说明* | `String` | `500` | `C` | 请详细说明商户的资金流向，包括但不限于（交易所涉及的各方账户、资金流入流出过程等）。最大500个汉字，必填；示例值：用户选购产品后根据订单支付给商户，商户根据结算周期，结算到对公账户。 |
| `request.data.balance_pay_config.description_info.function_instruction` | *功能开通用途说明* | `String` | `500` | `C` | 请详述所申请功能的原因、场景、涉及对象类型。最大500个汉字，必填；示例值：企业工资代发 |
| `request.data.balance_pay_config.charge_mode` | 扣费模式 | `String` | `2` | `N` | 内扣时枚举值: 01: 默认规则, 02: 收款方分摊, 03: 交易时指定承担方；外扣时枚举值: 10: 指定承担方, 11: 出款方承担, 12: 交易时指定承担方；示例值：11；内扣时默认为01，外扣时默认为10 |
| `request.data.balance_pay_config.pay_mode` | 余额支付模式 | `String` | `4` | `N` | pro，lite；示例值：pro；为空时默认为pro；lite版不支持当日收款资金余额支付；示例值：lite |
| `request.data.combine_pay_config` | 补贴支付 | `String` | `—` | `N` | jsonObject格式 |
| `request.data.combine_pay_config.switch_state` | 功能开关 | `String` | `1` | `Y` | 0：关闭，1：开通；示例值：1 |
| `request.data.combine_pay_config.fee_rate` | 支付手续费(%) | `String` | `9` | `N` | 支付手续费(%) 支持两位小数；示例值：0.50代表费率为0.5% |
| `request.data.combine_pay_config.fee_fix_amt` | 支付固定手续费(元) | `String` | `9` | `N` | 支付固定手续费(元)支持两位小数；示例值：1.50；注：如果fee_fix_amt与fee_rate都填写了则手续费=fee_fix_amt+支付金额\*fee_rate |
| `request.data.combine_pay_config.out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `Y` | 1:外扣，仅支持外扣，示例值：1；优先级高于相同名称的公共参数 |
| `request.data.combine_pay_config.out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `Y` | 开通交易手续费外扣业务时必填，示例值：[官网示例已脱敏]；优先级高于相同名称的公共参数 |
| `request.data.combine_pay_config.out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01；优先级高于相同名称的公共参数 |
| `request.data.online_pay_fee_conf_list[]` | 线上手续费承担方配置 | `String` | `—` | `N` | jsonArray格式 |
| `request.data.online_pay_fee_conf_list[].pay_type` | 业务类型 | `String` | `25` | `N` | ONLINE_PERSON:个人网银；ONLINE_ENT:企业网银；QUICK:快捷；WAP:手机WAP支付；ONLINE_ENT_TOP_UP:B2B网银充值；ONLINE_PERSON_TOP_UP:B2C网银充值；WITHHOLD:代扣支付；示例值：WAP |
| `request.data.online_pay_fee_conf_list[].out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户；示例值：01 |
| `request.data.online_pay_fee_conf_list[].out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填；示例值：[官网示例已脱敏] |
| `request.data.online_pay_fee_conf_list[].out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；示例值：2 |
| `request.data.online_pay_fee_conf_list[].switch_state` | 功能开关 | `String` | `1` | `N` | 0-关闭/1-打开；示例值：1 |
| `request.data.out_order_funds_config` | 全域资金管理配置(华通银行) | `String` | `—` | `N` | jsonObject字符串；**即将废弃**，请对接[全渠道资金管理配置接口](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_qypz) |
| `request.data.out_order_funds_config.switch_state` | 功能开关 | `String` | `1` | `Y` | 全域资金管理配置功能开关。0:关闭，1:开通；示例值：1 |
| `request.data.out_order_funds_config.out_order_auto_acct_flag` | 自动入账开关 | `String` | `1` | `Y` | 开通、关闭自动入账功能；0:关闭，1:开通；示例值：1；关闭自动入账需要[处理银行来账通知](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_lztz)，并调用[汇付入账确认接口](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_yhskfk)来确认入账。 |
| `request.data.out_order_funds_config.fee_rate` | 支付手续费(%) | `String` | `6` | `N` | 支持两位小数；示例值：0.45；fee_rate与fee_fix_amt与fee_min_amt不能同时为空 |
| `request.data.out_order_funds_config.fee_min_amt` | 手续费最小值(元) | `String` | `6` | `N` | 支付手续费最小值，支持两位小数；示例值：1.00fee_rate与fee_fix_amt与fee_min_amt不能同时为空 |
| `request.data.out_order_funds_config.out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户；示例值：01 |
| `request.data.out_order_funds_config.out_fee_flag` | 交易手续费外扣标记 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；示例值：2 |
| `request.data.out_order_funds_config.out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 示例值：[官网示例已脱敏] |
| `request.data.out_order_funds_config.out_order_acct_card` | 全域资金开户使用的银行卡信息 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.out_order_funds_config.out_order_acct_card.prov_id` | 银行所在省 | `String` | `6` | `N` | [参考省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000 |
| `request.data.out_order_funds_config.out_order_acct_card.area_id` | 银行所在市 | `String` | `6` | `N` | [参考省市区编码表](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310100 |
| `request.data.out_order_funds_config.out_order_acct_card.bank_code` | 银行编码 | `String` | `8` | `N` | 对公时根据支行编码获取总行编码；参考[银行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm)；示例值：01020000 |
| `request.data.out_order_funds_config.out_order_acct_card.branch_code` | 支行联行号 | `String` | `12` | `N` | card_type为0时必填，参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `request.data.out_order_funds_config.out_order_acct_card.branch_name` | 支行名称 | `String` | `64` | `N` | card_type为0时必填 ,参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：中国工商银行上海市中山北路支行 |
| `request.data.out_order_funds_config.out_order_acct_card.card_name` | 结算账户名 | `String` | `128` | `Y` | 银行卡对应的户名；示例值：上海汇付支付有限公司 |
| `request.data.out_order_funds_config.out_order_acct_card.card_no` | 银行卡号 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.out_order_funds_config.out_order_acct_card.card_type` | 卡类型 | `String` | `1` | `Y` | 0:对公 1:对私；示例值：0 |
| `request.data.out_order_funds_config.out_order_acct_card.cert_type` | 持卡人证件类型 | `String` | `2` | `C` | 00:身份证；示例值：00；card_type为1时选填。 |
| `request.data.out_order_funds_config.out_order_acct_card.cert_begin_date` | 持卡人证件有效期（起始） | `String` | `8` | `C` | card_type为1时选填；格式：yyyyMMdd，示例值：20210830；若填写cert_no，cert_validity_type，cert_type需同时填写。 |
| `request.data.out_order_funds_config.out_order_acct_card.cert_end_date` | 持卡人证件有效期（截止） | `String` | `8` | `C` | cert_validity_type变更为0时必填，格式：yyyyMMdd；示例值：20210830 |
| `request.data.out_order_funds_config.out_order_acct_card.cert_no` | 持卡人证件号码 | `String` | `32` | `C` | card_type为1时选填；示例值：[官网示例已脱敏] |
| `request.data.out_order_funds_config.out_order_acct_card.cert_validity_type` | 持卡人证件有效期类型 | `String` | `1` | `N` | card_type为1时选填；1:长期有效 0:非长期有效；示例值：0；若填写cert_begin_date，cert_no，cert_type需同时填写。 |
| `request.data.out_order_funds_config.out_order_acct_card.mp` | 银行卡绑定手机号 | `String` | `11` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.out_order_funds_config.out_order_acct_card.open_licence_no` | 开户许可证核准号 | `String` | `32` | `N` | 示例值：J2900123456789 |
| `request.data.out_order_funds_config.out_order_acct_open_fees` | 全域资金开户手续费 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.out_order_funds_config.out_order_acct_open_fees.fee_fix_amt` | 开户手续费(元) | `String` | `9` | `Y` | 支持两位小数；示例值：1.00 |
| `request.data.out_order_funds_config.out_order_acct_open_fees.out_fee_acct_type` | 开户手续费外扣时的账户类型 | `String` | `2` | `C` | 01-基本户，02-现金户，05-充值户，09-营销户，不填默认01；示例值：01；注：fee_fix_amt：开户手续费大于0时必填 |
| `request.data.out_order_funds_config.out_order_acct_open_fees.out_fee_huifuid` | 开户手续费外扣汇付ID | `String` | `18` | `C` | 开通手续费外扣业务时必填；示例值：[官网示例已脱敏]；注：fee_fix_amt：开户手续费大于0时必填 |
| `request.data.out_order_funds_config.business_model` | 全域支付业务模式 | `String` | `20` | `N` | acquiringMode：收单模式，；示例值：acquiringMode |
| `request.data.out_order_funds_config.other_payment_institutions_pic` | 全渠道资金管理补充材料 | `String` | `64` | `C` | 涉及文件类型：F504-全渠道资金管理补充材料；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.async_return_url` | 异步消息接收地址 | `String` | `128` | `N` | 审核消息接收地址，示例值：http://service.example.com/to/path 。为空不推送审核消息。 |
| `request.data.busi_async_return_url` | 业务开通结果异步消息接收地址 | `String` | `128` | `N` | 当前申请同步成功或者审核通过之后，示例值：http://service.example.com/to/path。为空不推送审核消息。 |
| `request.data.recon_resp_addr` | 交易异步应答地址 | `String` | `256` | `N` | 示例值：http://service.example.com/to/path。为空不推送交易异步消息。 |
| `request.data.online_media_info_list[]` | *运营媒介* | `String` | `—` | `N` | jsonArray字符串；如果开通快捷、网银、余额支付Pro版、分账、银行大额转账、代扣需提供运营媒介材料 |
| `request.data.online_media_info_list[].media_type` | *运营媒介类型* | `String` | `2` | `Y` | S1-PC网站；若媒介项为PC网站：必填字段（PC网站域名、ICP备案/许可证号）；S2-APP场景；若媒介项为APP场景：必填字段（APP名称、APP下载地址），若开通微信App支付，则新增app_id、app_name必填；S3-小程序场景；若媒介项为小程序：必填字段（小程序名称）；S4-公众号场景；若媒介项为公众号：必填字段（公众号名称）；S5-其他；媒介项为其他：其他有效信息或链接地址必填；线上场景时必填一项；示例值：S1 |
| `request.data.online_media_info_list[].media_name` | *媒介名称* | `String` | `200` | `C` | PC网站域名／APP名称／小程序名称／公众号名称；示例值：汇付服务；运营媒介类型为 ：S1/S2/S3/S4时，必填 |
| `request.data.online_media_info_list[].test_account` | *测试账号* | `String` | `64` | `N` | 示例值：test |
| `request.data.online_media_info_list[].test_secret` | *测试密码* | `String` | `64` | `N` | 示例值：test |
| `request.data.online_media_info_list[].mer_icp` | ICP备案/许可证号 | `String` | `200` | `C` | 运营媒介类型为 ：S1时必填；示例值：沪ICP备06046402号-28 |
| `request.data.online_media_info_list[].other_info` | *其他有效信息* | `String` | `200` | `C` | 其他有效信息或链接地址/APP下载地址；类型为S5或S2必填；示例值：http://download.huifu.com |
| `request.data.online_media_info_list[].media_front_page` | *运营媒介-首页* | `String` | `128` | `N` | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.online_media_info_list[].media_service_page` | *运营媒介-服务/商品明细页面* | `String` | `128` | `N` | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.online_media_info_list[].media_order_page` | *运营媒介-下单场景页面* | `String` | `128` | `N` | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.online_media_info_list[].media_pay_page` | *运营媒介-支付页面* | `String` | `128` | `N` | 通过[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)上传材料；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.online_media_info_list[].media_mer_common_flag` | *媒介主体与商户主体是否一致* | `String` | `1` | `C` | Y/N；示例值：Y；运营媒介为S1、S2、S3、S4且企业商户开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），必填；若不一致，则需提供ICP备案/APP/微信公众号/小程序主体与商户的使用授权或开发证明材料 |
| `request.data.online_media_info_list[].authorize_materials` | *授权或开发证明材料* | `String` | `128` | `C` | 运营媒介为S1、S2、S3、S4且媒介主体与商户主体不一致时，且企业商户开通快捷或网银，或大额转账，或余额支付或分账业务（20%（不含）-100%），或为个人商户开通分账业务（10%（不含）-100%），必填；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.online_media_info_list[].other_material` | 微信APP补充材料 | `String` | `128` | `C` | 运营媒介为S2且开通微信下app支付时选填，具体见[图片上传接口](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) |
| `request.data.online_media_info_list[].app_id` | appId | `String` | `128` | `C` | 运营媒介为S2且开通微信下app支付时必填 |
| `request.data.online_media_info_list[].app_name` | appId认证主体名称 | `String` | `128` | `C` | 运营媒介为S2且开通微信下app支付时必填 |
| `request.data.online_media_info_list[].supplement` | 补充说明 | `String` | `512` | `C` | 运营媒介为S2且开通微信下app支付时选填 |
| `request.data.extended_material_list[]` | *补充文件信息* | `String` | `—` | `N` | jsonArray字符串；根据开通的功能补充相关材料，包括[商户纸质协议说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%95%86%E6%88%B7%E5%90%88%E5%90%8C%E7%AD%BE%E7%BA%A6%E8%A7%84%E5%88%99.xlsx)、[线上行业补充材料](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E7%BA%BF%E4%B8%8A%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B%E7%BC%96%E7%A0%81%E5%8F%8A%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E.xlsx)、[开通余额支付补充材料](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E4%BD%99%E9%A2%9D%E6%94%AF%E4%BB%98%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99.xlsx) 、[分账功能提供材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/spin/files/20260611/KYC-%E5%88%86%E8%B4%A6%E5%8A%9F%E8%83%BD%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E%281%29.xlsx) 、[代扣支付补充材料](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/%E4%BB%A3%E6%89%A3%E6%94%AF%E4%BB%98%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99.xlsx) |
| `request.data.extended_material_list[].file_id` | *文件id* | `String` | `64` | `Y` | 请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.extended_material_list[].file_type` | *文件类型* | `String` | `64` | `N` | [参见文件类型说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；开通[分账功能提供材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%88%86%E8%B4%A6%E5%8A%9F%E8%83%BD%E6%8F%90%E4%BE%9B%E6%9D%90%E6%96%99.xlsx)；示例值：F01 |
| `request.data.online_busi_type` | *线上业务类型编码* | `String` | `8` | `C` | 开通快捷、网银、余额支付Pro版、银行大额转账、分账比例>30%、代扣必填；参见[线上业务类型编码及补充材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E7%BA%BF%E4%B8%8A%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B%E7%BC%96%E7%A0%81%E5%8F%8A%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E.xlsx)；示例值：H7999AL |
| `request.data.sign_user_info` | 签约人 | `String` | `—` | `C` | jsonObject字符串；agreement_info中选择电子签约时必填；个人商户填本人信息。 |
| `request.data.sign_user_info.type` | 签约人类型 | `String` | `7` | `Y` | LEGAL-法人，对公结算或对私法人结算时可选法人签约；CONTACT-联系人，对公结算可选联系人（经办人）签约；OTHER-其他，对私非法人结算选“其他”，必须是结算人；示例值：LEGAL |
| `request.data.sign_user_info.name` | 姓名 | `String` | `32` | `C` | 签约人类型=其他，必填；示例值：张三 |
| `request.data.sign_user_info.mobile_no` | 手机号 | `String` | `11` | `C` | 签约人类型=法人/其他 ，必填；注意：**签约人会做姓名+身份证+手机号验证，请正确填写**；示例值：[官网示例已脱敏] |
| `request.data.sign_user_info.cert_no` | 身份证 | `String` | `32` | `C` | 签约人类型=联系人/其他，必填 ；注意：**签约人会做姓名+身份证+手机号验证，请正确填写**；示例值：[官网示例已脱敏] |
| `request.data.sign_user_info.email` | 邮箱 | `String` | `32` | `N` | 示例值：example@email.com |
| `request.data.forced_delay_flag` | 商户开通强制延迟标记 | `String` | `1` | `N` | 选项：N：否 Y：是，默认否；**开关打开后商户所有交易都是延迟交易**，需要调用[交易确认接口](http://paas.huifu.com/open/doc/api/#/smzf/api_jyqr)（官网原始地址为非 HTTPS，不得静默改写）完成交易；示例值：N |
| `request.data.wx_zl_conf` | 微信直连配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `request.data.wx_zl_conf.sub_mch_id` | 微信子商户号 | `String` | `32` | `Y` | 微信支付分配的子商户号；示例值：1632157057 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list` | 配置集合 | `String` | `512` | `Y` | — |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.service_code` | 申请服务 | `String` | `16` | `Y` | JSAPI-公众号，APPLET-小程序；示例值：JSAPI |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sub_app_id` | 功能服务appid | `String` | `32` | `Y` | 子商户的公众号、小程序ID；示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.switch_state` | 功能开关 | `String` | `1` | `Y` | 0-关闭，1-打开；示例值：1 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.fee_rate` | 功能费率(%) | `String` | `6` | `Y` | 保留两位小数。示例值：0.60 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.operate_type` | 操作类型 | `String` | `10` | `C` | ADD-新增， UPDATE-修改， 默认新增；示例值：ADD |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.contact_info` | 联系人信息 | `String` | `—` | `C` | jsonObject字符串,新增时必填 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.contact_info.contact_type` | 联系人类型 | `String` | `1` | `Y` | 1： 法人；2：经办人；示例值：1 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.contact_info.contact_name` | 联系人姓名 | `String` | `128` | `C` | 联系人类型为经办人时必填；示例值：张三 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.contact_info.cert_type` | 联系人证件类型 | `String` | `2` | `C` | 联系人类型为经办人时必填；00：身份证；01:护照；11：港澳台同胞通行证；12：外国人居留证；13：港澳居民证；14：台湾居民证；示例值：00 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.contact_info.contact_cert_no` | 联系人证件号码 | `String` | `18` | `C` | 联系人类型为经办人时必填；示例值：[官网示例已脱敏] |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.contact_info.contact_mobile_no` | 联系人手机号 | `String` | `11` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.contact_info.contact_email` | 联系人电子邮箱 | `String` | `40` | `Y` | 示例值：carl.chen@huifu.com |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.contact_info.contact_file_list` | 联系人资料 | `String` | `—` | `C` | 联系人类型为经办人时必填；F28-联系人身份证国徽面 ；F29-联系人身份证人像面；F227-微信业务办理授权函；示例值： |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.contact_info.contact_file_list.file_type` | 文件类型 | `String` | `6` | `Y` | 示例值：F50 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.contact_info.contact_file_list.file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.contact_info.contact_cert_validity_type` | 证件有效期类型 | `String` | `1` | `Y` | 有效期类型 1:长期有效 0:非长期有效；示例值：1；若长期有效，则无需填写证书有效期截止日期 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.contact_info.contact_cert_begin_date` | 证件有效期开始日期 | `String` | `8` | `Y` | 格式：YYYYMMDD；示例值：20100908 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.contact_info.contact_cert_end_date` | 证件有效期截止日期 | `String` | `8` | `N` | 格式：YYYYMMDD；示例值：20300908 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.certificate_info` | 特殊主体登记证书 | `String` | `—` | `C` | jsonObject字符串，商户营业执照类型为政府机关/事业单位/其他组织时，传入相应信息。新增时需填入 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.certificate_info.cert_type` | 登记证书类型 | `String` | `32` | `Y` | CERTIFICATE_TYPE_2388：事业单位法人证书；CERTIFICATE_TYPE_2389：统一社会信用代码证书；CERTIFICATE_TYPE_2390：有偿服务许可证（军队医院适用）；CERTIFICATE_TYPE_2391：医疗机构执业许可证（军队医院适用）；CERTIFICATE_TYPE_2392：企业营业执照（挂靠企业的党组织适用）；CERTIFICATE_TYPE_2393：组织机构代码证（政府机关适用）；CERTIFICATE_TYPE_2394：社会团体法人登记证书；CERTIFICATE_TYPE_2395：民办非企业单位登记证书；CERTIFICATE_TYPE_2396：基金会法人登记证书；CERTIFICATE_TYPE_2397：慈善组织公开募捐资格证书；CERTIFICATE_TYPE_2398：农民专业合作社法人营业执照；CERTIFICATE_TYPE_2399：宗教活动场所登记证；CERTIFICATE_TYPE_2400：其他证书/批文/证明；示例值：CERTIFICATE_TYPE_2400 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.certificate_info.cert_no` | 证书号 | `String` | `32` | `Y` | 请填写登记证书上的证书编号。示例值：92650109MA79R8E308 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.certificate_info.cert_mer_name` | 证书商户名称 | `String` | `128` | `Y` | 请填写登记证书上的商户名称。示例值：上海汇付支付服务公司 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.certificate_info.reg_detail` | 注册地址 | `String` | `128` | `Y` | 请填写登记证书的注册地址。示例值：上海徐汇宜山路601号C5栋 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.certificate_info.legal_name` | 法人姓名 | `String` | `32` | `Y` | 1、只能由中文字符、英文字符、可见符号组成。；2、请填写登记证书上的法定代表人姓名。示例值：张三 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.certificate_info.cert_validity_type` | 证书有效期类型 | `String` | `1` | `Y` | 有效期类型 1:长期有效 0:非长期有效；示例值：0；若长期有效，则无需填写证书有效期截止日期 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.certificate_info.cert_begin_date` | 证书有效期开始日期 | `String` | `8` | `Y` | 格式：YYYYMMDD；示例值：20100908 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.certificate_info.cert_end_date` | 证书有效期截止日期 | `String` | `8` | `N` | 格式：YYYYMMDD；示例值：20300908 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.certificate_info.cert_file_list[]` | 文件列表 | `String` | `—` | `Y` | jsonArray，F46-单位证明函，F45-登记证书 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.certificate_info.cert_file_list[].file_type` | 文件类型 | `String` | `6` | `Y` | 示例值：F50 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.certificate_info.cert_file_list[].file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.ubo_info` | 最终受益人信息 | `String` | `—` | `C` | jsonObject字符串，商户类型为企业时，微信侧必填。（如果基本信息里有的话，可以不传取 huifu_id 对应的信息）。新增时填入 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.ubo_info.ubo_type` | 经营者/法人是否为受益人 | `String` | `1` | `Y` | Y-是，N-否；示例值：Y |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.ubo_info.ubo_info_list[]` | 受益人信息列表 | `String` | `—` | `C` | jsonArray格式,当ubo_type为Y时可不填 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.ubo_info.ubo_info_list[].ubo_cert_type` | 证件类型 | `String` | `2` | `Y` | 00:身份证 01:护照；示例值：00 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.ubo_info.ubo_info_list[].ubo_cert_no` | 证件号码 | `String` | `18` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.ubo_info.ubo_info_list[].ubo_name` | 姓名 | `String` | `32` | `Y` | 示例值：张三 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.ubo_info.ubo_info_list[].ubo_cert_doc_address` | 受益人证件居住地址 | `String` | `128` | `Y` | 示例值：上海宝山区共富路11号 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.ubo_info.ubo_info_list[].ubo_cert_validity_type` | 证件有效类型 | `String` | `1` | `Y` | 1:长期有效 0:非长期有效；示例值：0 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.ubo_info.ubo_info_list[].ubo_cert_begin_date` | 证件有效期开始日期 | `String` | `8` | `Y` | 示例值：20200908 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.ubo_info.ubo_info_list[].ubo_cert_end_date` | 证件有效期截止日期 | `String` | `8` | `N` | 示例值：20330908 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.ubo_info.ubo_info_list[].ubo_file_list[]` | 文件列表 | `String` | `—` | `Y` | jsonArray，F228-受益人身份证正面（国徽面），F229-联系人身份证反面（人像面）；示例值：F229 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.ubo_info.ubo_info_list[].ubo_file_list[].file_type` | 文件类型 | `String` | `6` | `Y` | 示例值：F50 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.ubo_info.ubo_info_list[].ubo_file_list[].file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info` | 经营场景 | `String` | `—` | `C` | jsonObject字符串，新增时填入 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.sales_scenes_type` | 经营场景类型 | `String` | `256` | `Y` | 多个以英文逗号分割，至少要有一个；线下门店：SALES_SCENES_STORE；公众号：SALES_SCENES_MP；小程序：SALES_SCENES_MINI_PROGRAM；互联网：SALES_SCENES_WEB；APP：SALES_SCENES_APP；企业微信：SALES_SCENES_WEWORK；示例值：SALES_SCENES_WEWORK |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.fee_rate` | 功能费率 | `String` | `6` | `C` | 仅支持渠道商传入该字段。示例值：0.06；平台商户为子商户开通微信直连支付时，不支持该字段，取平台商户费率上送微信。 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.fee_rate_file_list` | 文件列表 | `String` | `—` | `N` | 微信直连商户费率材料，根据微信要求上送。示例值：d1451277-85c6-3177-ac3d-a8be47b9ae9d |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.fee_rate_file_list.file_type` | 文件类型 | `String` | `6` | `Y` | 示例值：F75 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.fee_rate_file_list.file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：d1451277-85c6-3177-ac3d-a8be47b9ae9d |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.biz_store_name` | 门店名称 | `String` | `128` | `N` | 不传，取 huifu_id 关联信息,微信侧条件必填；示例值：卡卡奶茶共富店 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.biz_address_code` | 门店省市编码 | `String` | `128` | `N` | 不传，取 huifu_id 关联信息,微信侧条件必填；示例值：310100 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.biz_store_address` | 门店地址 | `String` | `128` | `N` | 不传，取 huifu_id 关联信息,微信侧条件必填；示例值：上海宝山共富路1号 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.biz_sub_jsapi_app_id` | 线下场所对应的商家公众号APPID | `String` | `256` | `C` | 开通线下门店场景时，填入。都填入时，取公众号的上送微信。示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.biz_sub_mini_app_id` | 线下场所对应的商家小程序APPID | `String` | `256` | `C` | 开通线下门店场景时，填入。都填入时，取公众号的上送微信。示例值：wxea9c30a90fs8d3fe |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.jsapi_app_id` | 服务商公众号 ID | `String` | `256` | `C` | 开通公众号场景时，直连服务商和商户的公众号 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.jsapi_sub_app_id` | 商家公众号APPID | `String` | `256` | `C` | 开通公众号场景时，直连服务商和商户的公众号 APP ID，二选一填入。示例值：wxea9c30a90fs8d3fe |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.mini_app_id` | 服务商小程序APPID | `String` | `256` | `C` | 开通小程序场景时，直连服务商和商户的小程序 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.mini_sub_app_id` | 商家小程序APPID | `String` | `256` | `C` | 开通小程序场景时，直连服务商和商户的小程序 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.app_app_id` | 服务商应用APPID | `String` | `256` | `C` | 开通 APP 场景时，直连服务商和商户的 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.app_sub_app_id` | 商家应用APPID | `String` | `256` | `C` | 开通 APP 场景时，直连服务商和商户的 APP ID，二选一填入。示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.web_domain` | 互联网网站域名 | `String` | `256` | `C` | 开通互联网场景时填入；示例值：huifu.com |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.web_app_id` | 互联网网站对应的商家APPID | `String` | `256` | `C` | 开通互联网场景时填入；示例值：wx51aa91a575359ff5 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.sub_corp_id` | 商家企业微信CorpID | `String` | `256` | `C` | 开通企业微信场景时填入；示例值：xxxxx |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.sales_scenes_file_list` | 文件列表 | `String` | `6` | `Y` | 场景资料文件；附件资料列表fileList；线下门店场景，F49与F50必传；公众号场景，F95，F96，F97，F98，F99，总共至少传1张，最多传5张；小程序场景，F60，F61，F62，F63，F64，总共至少传1张，最多传5张；APP场景，F65，F66，F67，F68，各传1张；互联网网站场景，若备案主体与申请主体不同，请务必上传加盖公章的网站授权函(F69)。；企业微信场景，F70，F71，F72，F73，F74，总共至少传1张，最多传5张；F49-店铺内景图片；F50-店铺门头照图片；F95-公众号页面截图一；F96-公众号页面截图二；F97-公众号页面截图三；F98-公众号页面截图四；F99-公众号页面截图五；F60-小程序截图截图一；F61-小程序截图截图二；F62-小程序截图截图三；F63-小程序截图截图四；F64-小程序截图截图五；F65-APP首页截图；F66-APP尾页截图；F67-APP应用内截图；F68-APP支付页截图；F69-网站授权函；F70-企业微信页面截图一；F71-企业微信页面截图二；F72-企业微信页面截图三；F73-企业微信页面截图四；F74-企业微信页面截图五；示例值：F74 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.sales_scenes_file_list.file_type` | 文件类型 | `String` | `6` | `Y` | 示例值：F50 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.sales_info.sales_scenes_file_list.file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.wx_card_info` | 银行账户信息 | `String` | `—` | `C` | jsonObject字符串，该字段不填时，取商户在汇付系统录入的结算账号信息。新增或修改时填入，修改时必填 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.wx_card_info.card_type` | 账户类型 | `String` | `1` | `Y` | 0：对公银行账户；1：经营者个人银行卡；示例值：0 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.wx_card_info.card_name` | 开户名称 | `String` | `128` | `Y` | 选择“经营者个人银行卡”时，开户名称必须与“经营者证件姓名”一致。选择“对公银行账户”时，开户名称必须与营业执照上的“商户名称”一致。；示例值：张三 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.wx_card_info.bank_code` | 开户银行 | `String` | `8` | `Y` | 客户按汇付银行编码上送；示例值：01020000 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.wx_card_info.prov_id` | 开户银行省编码 | `String` | `6` | `Y` | 按汇付的省市编码；示例值：310000 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.wx_card_info.area_id` | 开户银行市编码 | `String` | `6` | `Y` | 示例值：310100 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.wx_card_info.branch_code` | 开户银行联行号 | `String` | `20` | `C` | 开户银行联行号与开户银行全称（含支行)二选一；示例值：102290026507 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.wx_card_info.branch_name` | 开户银行全称（含支行) | `String` | `128` | `C` | 开户银行联行号与开户银行全称（含支行)二选一；示例值：中国工商银行股份有限公司上海市中山北路支行 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.wx_card_info.card_no` | 银行账号 | `String` | `30` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.business_addition_msg` | 补充说明信息 | `String` | `512` | `N` | 示例值：补充说明 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.addition_file_list[]` | 补充说明文件列表 | `String` | `—` | `N` | jsonArray格式，根据实际审核情况，额外要求商家提供指定的补充资料；F85-微信直连额外补充材料一；F86-微信直连额外补充材料二；F87-微信直连额外补充材料三；F88-微信直连额外补充材料四；F89-微信直连额外补充材料五；F90-法人开户承诺函；F91-法人开户意愿视频 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.addition_file_list[].file_type` | 文件类型 | `String` | `6` | `Y` | 示例值：F50 |
| `request.data.wx_zl_conf.wx_zl_pay_conf_list.addition_file_list[].file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.ali_zl_conf` | 支付宝直连配置对象 | `String` | `—` | `N` | jsonObject格式 |
| `request.data.ali_zl_conf.apply_type` | 申请类型 | `String` | `32` | `Y` | FACE_TO_FACE：当面付；示例值：FACE_TO_FACE |
| `request.data.ali_zl_conf.contact_name` | 联系人姓名 | `String` | `64` | `N` | 支付宝联系人信息，不传取商户的联系人信息；示例值：张三 |
| `request.data.ali_zl_conf.contact_mobile_no` | 联系人手机号 | `String` | `11` | `N` | 支付宝联系人信息，不传取商户的联系人信息；示例值：[官网示例已脱敏] |
| `request.data.ali_zl_conf.contact_email` | 联系人电子邮箱 | `String` | `40` | `N` | 支付宝联系人信息，不传取商户的联系人信息；示例值：carl.chen@huifu.com |
| `request.data.ali_zl_conf.order_ticket` | 订单授权凭证 | `String` | `40` | `N` | 示例值： |
| `request.data.ali_zl_conf.account` | 商户支付宝账号 | `String` | `128` | `Y` | 商户登录支付宝控台的账号；示例值：zhangsan |
| `request.data.ali_zl_conf.fee_rate` | 服务费率 | `String` | `6` | `C` | 仅支持渠道商。平台商户调用不支持该字段；服务费率（%），0.38~3之间，精确到0.01。示例值：0.06 |
| `request.data.ali_zl_conf.license_code` | 营业执照编号 | `String` | `20` | `N` | 工商营业执照编号，示例值：92650109MA79R8E308 |
| `request.data.ali_zl_conf.license_validity_type` | 营业执照有效期类型 | `String` | `1` | `N` | 1:长期有效 0:非长期有效示例值： |
| `request.data.ali_zl_conf.license_begin_date` | 营业执照有效期开始日期 | `String` | `8` | `N` | 日期格式yyyyMMdd，示例值：20110112 |
| `request.data.ali_zl_conf.license_end_date` | 营业执照有效期截止日期 | `String` | `8` | `N` | 日期格式yyyyMMdd，示例值：20110112 |
| `request.data.ali_zl_conf.file_list[]` | 文件列表 | `String` | `—` | `Y` | jsonArray格式，F47-企业特殊资质图片(可选，企业特殊资质图片，可参考商家经营类目中的“需要的特殊资质证书”)；F48-营业执照授权函图片（可选，个体工商户如果使用总公司或其他公司的营业执照认证需上传该授权函图片）；F49-店铺内景图片(可选)；F50-店铺门头照图片(必填)；示例值：F50 |
| `request.data.ali_zl_conf.file_list[].file_type` | 文件类型 | `String` | `6` | `Y` | 示例值：F50 |
| `request.data.ali_zl_conf.file_list[].file_id` | 文件jfileId | `String` | `64` | `Y` | 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.enter_fee` | 开户费用值(元) | `String` | `14` | `N` | 示例值：5.00 |
| `request.data.enter_fee_flag` | 开户费用类型 | `String` | `1` | `N` | 1-一次性开户费，2-平台套餐费（元/年）；示例值：2 |
| `request.data.online_refund` | 是否开通在线退款 | `String` | `1` | `N` | N：否 Y：是；示例值：Y |
| `request.data.platform_refund` | 是否支持平台退款 | `String` | `1` | `N` | N：否 Y：是；示例值：Y |
| `request.data.support_revoke` | 是否支持撤销 | `String` | `1` | `N` | N：否 Y：是；示例值：Y |
| `request.data.split_conf_info` | 分账配置信息 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.split_conf_info.rule_origin` | 分账规则来源 | `String` | `2` | `Y` | 01 接口发起 02页面配置；示例值：01 |
| `request.data.split_conf_info.div_flag` | 分账开关 | `String` | `1` | `Y` | Y：开，N：关；示例值：Y |
| `request.data.split_conf_info.apply_ratio` | 最大分账比例% | `String` | `9` | `Y` | 0-100 的数值，支持两位小数; 示例值：20.00 |
| `request.data.split_conf_info.acct_split_bunch_list[]` | 分账明细 | `Object` | `—` | `N` | 分账规则来源选择平台配置时必填,jsonArray格式 |
| `request.data.split_conf_info.acct_split_bunch_list[].fee_rate` | 分账比例 | `String` | `9` | `Y` | 百分比支持两位小数，示例值：0.20 |
| `request.data.split_conf_info.acct_split_bunch_list[].huifu_id` | 汇付Id | `String` | `18` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.split_conf_info.start_type` | 生效类型 | `String` | `1` | `N` | 0-审核通过即时生效；1-审核通过次日生效；示例值：1 |
| `request.data.split_conf_info.out_fee_flag` | 交易手续费外扣开关 | `String` | `1` | `N` | 1:外扣 2:内扣（默认）；示例值：1 |
| `request.data.split_conf_info.out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户(默认)，02-现金户，05-充值户；示例值：01 |
| `request.data.split_conf_info.out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 选择手续费外扣时必填；示例值： |
| `request.data.split_conf_info.split_fee_rate` | 手续费% | `String` | `9` | `N` | 开通分账业务时必须填写一种收费方式；百分比，支持两位小数；示例值：1.00 ；分账手续费收取方式为费率手续费与固定手续费之和 |
| `request.data.split_conf_info.per_amt` | 固定手续费 | `String` | `9` | `N` | 开通分账业务时必须填写一种收费方式；单位元，支持小数点后两位；示例值：1.00 ；分账手续费收取方式为费率手续费与固定手续费之和 |
| `request.data.split_conf_info.scene` | 分账模式 | `String` | `2` | `Y` | 00-其他；01-医美医院分账；02-线上其他；A1- 教培机构分账；A2-公办/民办学校分账；A3-医美渠道独立收款分账；A4-线上供应商货款；A5-线上推广方（渠道/代理/个人）的服务佣金/抽成；A7-入驻商户货款；A8-线下供应商货款；A9-线下推广方；A10-个人与合作方分账；单选；示例值：A9 |
| `request.data.split_conf_info.split_ext_info` | 业务情况说明 | `Object` | `128` | `N` | jsonObject；分账模式选择则其它，分账比例30%以上必填 |
| `request.data.split_conf_info.split_ext_info.busi_instruction` | *业务模式说明* | `String` | `500` | `Y` | 请详细说明商户的业务模式，包括不限于（业务参与方、各方的权利及义务关系等）。最大500个汉字，必填；示例值：商户向企业采购产品，并将其展示在其电商平台上，用户注册后购买其产品，产品主要有家电、服饰、鞋帽等，用户购买产品的资金作为商户所得，商户根据订单情况进行物流配送。 |
| `request.data.split_conf_info.split_ext_info.capital_instruction` | *资金流向说明* | `String` | `500` | `Y` | 请详细说明商户的资金流向，包括但不限于（交易所涉及的各方账户、资金流入流出过程等）。最大500个汉字，必填；示例值：用户选购产品后根据订单支付给商户，商户根据结算周期，结算到对公账户。 |
| `request.data.split_conf_info.split_ext_info.function_instruction` | *功能开通用途说明* | `String` | `500` | `Y` | 请详述所申请功能的原因、场景、涉及对象类型。最大500个汉字，必填；示例值：企业工资代发 |
| `request.data.uni_app_payment_config` | 银联线上收银台 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.uni_app_payment_config.switch_state` | 状态开关 | `String` | `1` | `N` | 0-关闭; 1-开通, 为空默认开通；示例值：1 |
| `request.data.uni_app_payment_config.debit_fee_rate` | 借记手续费（%） | `String` | `6` | `C` | 借记卡费率与贷记卡费率不能同时为空;；保留2位小数，最大值100.00，最小值0.00；示例值：0.02 |
| `request.data.uni_app_payment_config.credit_fee_rate` | 贷记手续费（%） | `String` | `6` | `C` | 借记卡费率与贷记卡费率不能同时为空;；保留2位小数，最大值100.00，最小值0.00；示例值：0.06 |
| `request.data.uni_app_payment_config.out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；示例值：1 ；如果不为空，则out_fee_acct_type，out_fee_huifuid，out_fee_flag取单独配置，否则取公共配置 |
| `request.data.uni_app_payment_config.out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填；示例值：[官网示例已脱敏] |
| `request.data.uni_app_payment_config.out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户，02-现金户，05-充值户，09-营销户；不填默认01；示例值：01 |
| `request.data.uni_app_payment_config.cloud_quick_pass_secret_free_flag` | 云闪付免密支付开通标识 | `String` | `1` | `N` | Y：是，N：否；示例值：Y |
| `request.data.fund_collection_flag` | 资金归集开通标记 | `String` | `1` | `N` | Y：是，N：否；示例值：Y |
| `request.data.surrogate_config_list[]` | 代发配置 | `String` | `—` | `N` | jsonArray格式字符串 |
| `request.data.surrogate_config_list[].switch_state` | 开通状态 | `String` | `1` | `N` | 1:是 0:否, 为空默认开；示例值：1 |
| `request.data.surrogate_config_list[].surrogate_type` | 代发业务类型 | `String` | `2` | `Y` | D0:当日到账；T1:下个工作日到账;；D1:下个自然日到账;；示例值：T1 |
| `request.data.surrogate_config_list[].fix_amt` | 手续费（固定/元） | `String` | `17` | `C` | 手续费（固定/元），保留小数点后两位；fee_formula_type为05，06时必填 示例值：1.00 |
| `request.data.surrogate_config_list[].fee_rate` | 手续费（百分比/%） | `String` | `6` | `C` | 手续费（百分比/%），保留小数点后两位；取值范围[0.00,100.00]；fee_formula_type为01，02，03，06时必填 示例值：0.05 |
| `request.data.surrogate_config_list[].out_fee_flag` | 是否交手续费外扣标记 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；优先级高于相同名称的公共参数；示例值：1 |
| `request.data.surrogate_config_list[].out_fee_acct_type` | 交易手续费外扣时账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01；优先级高于相同名称的公共参数 |
| `request.data.surrogate_config_list[].out_fee_huifu_id` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通交易手续费外扣业务时必填，示例值：[官网示例已脱敏]；优先级高于相同名称的公共参数 |
| `request.data.surrogate_config_list[].surrogate_private_flag` | 是否允许对私代发 | `String` | `1` | `N` | 是否允许代发卡为对私类型；Y:允许 N:不允许；示例值：Y |
| `request.data.surrogate_config_list[].fee_formula_type` | 代发手续费计费模式 | `String` | `17` | `C` | 01: 百分比手续费，无封顶值或保底值；02: 百分比手续费，有保底值；03: 百分比手续费，有封顶值；05: 固定手续费 ；06: 固定手续费+百分比手续费；为空默认06 示例值：06 |
| `request.data.surrogate_config_list[].fee_max_amt` | 手续费封顶值（固定/元） | `String` | `17` | `C` | 手续费封顶值（固定/元），保留小数点后两位；fee_formula_type为03时必填 示例值：100.00 |
| `request.data.surrogate_config_list[].fee_min_amt` | 手续费保底值（固定/元） | `String` | `17` | `C` | 手续费保底值（固定/元），保留小数点后两位；fee_formula_type为02时必填 示例值：1.00 |
| `request.data.large_amt_pay_config` | 大额支付配置 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[]` | 大额支付配置列表 | `String` | `—` | `Y` | 大额支付配置列表，jsonArray格式 |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].switch_state` | 功能开关 | `String` | `1` | `N` | 1:开通 0:关闭 默认：1；示例值：1 |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].business_model` | 大额支付业务模式 | `String` | `15` | `Y` | 大额支付业务模式 bank：银行模式 provisions：备付金模式；示例值：bank |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].fee_rate` | 费率（%） | `String` | `6` | `C` | 开通大额业务时必须填写一种收费方式；大于0,保留2位小数；示例值：1.00 |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].fee_fix_amt` | 交易手续费（固定/元） | `String` | `9` | `C` | 开通大额业务时必须填写一种收费方式；大于0,保留2位小数；示例值：10.00 |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].biz_type` | 大额调账标识申请类型 | `String` | `2` | `N` | 01-四要素，05-三要素；[订单匹配的要素信息](https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_ddppys)；示例值：05 |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].mer_same_card_recharge_flag` | 是否允许绑卡支付 | `String` | `1` | `N` | Y-开通/N-关闭，备付金模式时，支持传入；备付金模式银行卡绑定支付权限；示例值：Y |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].allow_user_deposit_flag` | 是否允许用户入账 | `String` | `1` | `N` | Y-开通/N-关闭 ；默认为N；示例值：Y |
| `request.data.large_amt_pay_config.large_amt_pay_config_info_list[].provisions_auto_refund_flag` | 备付金固定账号模式自动退款 | `String` | `1` | `N` | Y-开通/N-关闭 ；示例值：Y；该配置仅在开通大额支付备付金绑卡模式时生效 |
| `request.data.large_amt_pay_config.out_fee_flag` | 交易手续费外扣标记 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；示例值：1 |
| `request.data.large_amt_pay_config.out_fee_huifu_id` | 交易手续费外扣huifuId | `String` | `18` | `C` | 交易手续费外扣时必填；示例值：[官网示例已脱敏] |
| `request.data.large_amt_pay_config.out_fee_acct_id` | 交易手续费外扣账户号 | `String` | `16` | `C` | 交易手续费外扣时必填；示例值：F00598602 |
| `request.data.large_amt_pay_config.mer_payer_card_type` | 商户付款方卡类型 | `String` | `10` | `N` | CORPORATE-对公,PRIVATE-对私,ALL-全部，默认全部；示例值：ALL |
| `request.data.half_pay_host_flag` | 统一收银台开关 | `String` | `1` | `N` | Y:是 N:否（为空默认未开通） ；示例值：Y |
| `request.data.agent_recheck_config` | 代发复核配置 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.agent_recheck_config.agent_recheck_flag` | 代发复核开关 | `String` | `1` | `N` | Y:是 N:否（为空默认未开通） ；示例值：Y |
| `request.data.agent_recheck_config.agent_recheck_huifu_id` | 复核授权商户号 | `String` | `18` | `N` | 复核授权商户号只能填当前商户主体或总部商户号 |
| `request.data.agent_recheck_config.agent_recheck_type` | 复核类型 | `String` | `1` | `N` | A:复核 B:短信验证 |
| `request.data.online_recharge_flag` | 商户开通网银充值开关 | `String` | `1` | `N` | Y:是 N:否；示例值：Y |
| `request.data.refund_mend_open_flag` | 是否开通垫资退款 | `String` | `1` | `N` | Y:是 N:否 ；示例值：Y |
| `request.data.jxf_conf_info` | 捷行付配置 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.jxf_conf_info.bank_pay_open_flag` | 银行模式开关 | `String` | `—` | `N` | Y-开通 N-关闭 |
| `request.data.jxf_conf_info.jxf_bank_pay_info` | 银行模式配置 | `Object` | `—` | `C` | 当开通bank_pay_open_flag时必填 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.acct_type` | 账户类型 | `String` | `1` | `Y` | 2:银行账户 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.bank_name` | 银行名称 | `String` | `8` | `Y` | PINGAN-平安银行 BOC-中国银行；示例值：PINGAN |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info` | 银行账户信息 | `Object` | `—` | `C` | 当账户类型为银行账户时必填 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.user_name` | 操作人姓名 | `String` | `16` | `C` | 银行名称非平安银行时，需填写；示例：张三 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.operator_phone` | 操作人手机号 | `String` | `11` | `C` | 银行名称非平安银行时，需填写；示例：[官网示例已脱敏] |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.acct_type` | 付款方账户类型 | `String` | `2` | `N` | 00：单位结算卡，不填默认单位结算卡 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.acct_no` | 付款方账号 | `String` | `50` | `Y` | 示例：[官网示例已脱敏] |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.acct_name` | 付款方账户名称 | `String` | `25` | `Y` | 示例：上海汇付支付有限公司 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.bank_branch_code` | 开户行联行号 | `String` | `50` | `Y` | 示例：991290000099 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.bank_branch_name` | 开户行行名 | `String` | `25` | `Y` | 示例：中国银行 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.sign_start_date` | 签约申请生效日期 | `String` | `8` | `C` | 银行名称非平安银行时，需填写；示例：20251219 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.sign_end_date` | 签约申请失效日期 | `String` | `8` | `C` | 银行名称非平安银行时，需填写；示例：20261219 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.remark` | 附言 | `String` | `128` | `N` | 示例：附言 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_bank_info.org_code` | 机构编码 | `String` | `64` | `Y` | 示例：12133 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info` | 手续费信息 | `Object` | `—` | `N` | jsonObject字符串 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.open_card_fix_fee` | 虚拟卡开卡手续费（元） | `String` | `11` | `N` | 单位元，支持小数点后两位；示例值：1.00 虚拟卡开卡手续费收取方式为发放数量*固定手续费 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.quota_issue_fee_rate` | 虚拟卡额度发放手续费（%） | `String` | `6` | `N` | 百分比，支持两位小数；示例值：1.00 虚拟卡发放额度手续费收取方式为交易金额*费率手续费 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.out_fee_flag` | 捷行付手续费内外扣标记 | `String` | `1` | `N` | 捷行付手续费只支持外扣；1:外扣；示例值：1 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.out_fee_huifuid` | 捷行付手续费外扣汇付ID | `String` | `18` | `C` | 捷行付设置手续费时必填；示例值：[官网示例已脱敏] |
| `request.data.jxf_conf_info.jxf_bank_pay_info.jxf_fee_info.out_fee_acct_type` | 捷行付手续费扣款账户类型 | `String` | `2` | `C` | 捷行付手续费外扣时必填；01-基本户(默认)，05-充值户；示例值：01 |
| `request.data.jxf_conf_info.jxf_bank_pay_info.pay_confirm_flag` | 付款确认标识 | `String` | `1` | `N` | Y:是 N:否 ；示例值：Y |
| `request.data.jxf_conf_info.jxf_bank_pay_info.pay_confirm_req_url` | 付款确认请求URL | `String` | `256` | `C` | 付款确认标识为Y时，该字段必填 |
| `request.data.jxf_conf_info.wx_ent_pay_open_flag` | 微信企业码模式开关 | `String` | `—` | `N` | Y-是 N-否 |
| `request.data.jxf_conf_info.wx_ent_pay_info` | 微信企业码模式配置 | `Object` | `—` | `N` | 当开通wx_ent_pay_open_flag时必填 |
| `request.data.jxf_conf_info.wx_ent_pay_info.payment_background` | 付款背景介绍 | `String` | `512` | `N` | 付款背景介绍 |
| `request.data.jxf_conf_info.wx_ent_pay_info.apply_scenes` | 适用场景，多选逗号分隔 | `String` | `—` | `N` | 1-企业差旅 2-因公宴请 3-会员积分 4-小额采购 5-商报直付 |
| `request.data.jxf_conf_info.wx_ent_pay_info.sub_mch_id` | 微信商户号 | `String` | `—` | `N` | 微信商户号（出资子商户号） |
| `request.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info` | 微信企业码手续费信息 | `Object` | `—` | `N` | 微信企业码手续费信息 |
| `request.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.open_card_fix_fee` | 虚拟卡开卡手续费（元） | `String` | `11` | `N` | 单位元，支持小数点后两位；示例值：1.00 虚拟卡开卡手续费收取方式为发放数量*固定手续费 |
| `request.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.quota_issue_fee_rate` | 虚拟卡额度发放手续费（%） | `String` | `6` | `N` | 百分比，支持两位小数；示例值：1.00 虚拟卡发放额度手续费收取方式为交易金额*费率手续费 |
| `request.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.out_fee_flag` | 捷行付手续费内外扣标记 | `String` | `1` | `N` | 捷行付手续费只支持外扣；1:外扣；示例值：1 |
| `request.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.out_fee_huifuid` | 捷行付手续费外扣汇付ID | `String` | `18` | `C` | 捷行付设置手续费时必填；示例值：[官网示例已脱敏] |
| `request.data.jxf_conf_info.wx_ent_pay_info.jxf_fee_info.out_fee_acct_type` | 捷行付手续费扣款账户类型 | `String` | `2` | `N` | 捷行付手续费外扣时必填；01-基本户(默认)，05-充值户；示例值：01 |
| `request.data.jxf_conf_info.default_channel` | 默认通道 | `String` | `—` | `C` | 当开通bank_pay_open_flag或wx_ent_pay_open_flag时必填。1-银行通道 2-微信企业码 |
| `request.data.merge_pay_config_info` | 合单支付配置信息 | `String` | `—` | `N` | jsonObject字符串 |
| `request.data.merge_pay_config_info.merge_pay_flag` | 合单支付开关 | `String` | `1` | `Y` | 合单支付开关 Y：开通 N：关闭 |
| `request.data.merge_pay_config_info.merge_pay_config` | 合单支付配置 | `String` | `—` | `C` | 合单支付配置 （当合单支付开关为开时必填） |
| `request.data.merge_pay_config_info.merge_pay_config.merge_pay_mode` | 合单支付模式 | `String` | `1` | `Y` | 1:电商 2:加油站 3:停车场 4:物业 5:休闲娱乐（不同模式需上传不同材料信息，调用图片上传接口；若选择电商，需上传文件F673《电商平台商家入驻协议》、F674《商家入驻截图》，以及填写线上业务类型编码及运营媒介字段信息；若选择加油站，需上传文件F676《加油站与任一合单参与方合作协议》、F675《任一合单参与方经营照片》；若选择停车场，需上传文件F677《停车场与任一合单参与方合作协议》、F675《任一合单参与方经营照片》；若选择物业需上传文件F678《物业与任一合单参与方合作协议》、F675《任一合单参与方经营照片》；若选择休闲娱乐需上传文件F679《休娱与任一合单参与方合作协议》、F675《任一合单参与方经营照片》） |
| `request.data.bill_payment_flag` | 是否开通账单支付 | `String` | `1` | `N` | Y:是 N:否 ；示例值：Y |
| `request.data.withhold_pay_scene` | 代扣场景 | `String` | `1` | `C` | withhold_flag开通需填写 1:权益投流(订阅),2:非权益投流(订阅),3:保险缴纳,4:道路通行费(ETC),5:公共事业(水电煤)缴费,6:物业缴费 |
| `request.data.recon_resp_sys_id` | 交易应答返回推送系统号 | `String` | `32` | `N` | 交易应答返回推送系统号；示例值：[官网示例已脱敏] |
| `request.data.dy_conf_list[]` | 抖音配置对象对象 | `String` | `—` | `N` | jsonArray字符串 |
| `request.data.dy_conf_list[].fee_rate` | 手续费（%） | `String` | `9` | `N` | 数字格式，大于等于0，保留2位小数；示例值：0.38 |
| `request.data.dy_conf_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `9` | `N` | 金额保留2位小数；大于0。需要渠道商开通此功能。示例值：0.38 |
| `request.data.dy_conf_list[].out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣），示例值：1 |
| `request.data.dy_conf_list[].out_fee_huifuid` | 交易手续费外扣汇付ID | `String` | `18` | `N` | 开通抖音支付手续费外扣业务时必填，示例值：[官网示例已脱敏] |
| `request.data.dy_conf_list[].out_fee_acct_type` | 交易手续费外扣时的账户类型 | `String` | `2` | `N` | 01-基本户（不填默认01），02-现金户，05-充值户，09-营销户，示例值：01 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| `response.data.resp_desc` | 返回描述 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| `response.data.huifu_id` | 商户号 | `String` | `18` | `N` | 汇付分配的商户号，示例值：[官网示例已脱敏] |
| `response.data.apply_no` | 申请单号 | `String` | `18` | `N` | 审核中时有值，汇付返回商户的业务申请单号；示例值：202209120038432 |

### 审核异步信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.audit.resp_code` | 网关返回码 | `String` | `6` | `Y` | [网关返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#网关返回码) |
| `async.audit.resp_desc` | 网关返回描述 | `String` | `512` | `Y` | [网关返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#网关返回码) |
| `async.audit.sign` | 签名 | `String` | `512` | `Y` | 签名，对报文整体签名 |
| `async.audit.data` | 业务返回参数 | `String` | `—` | `N` | JSON |

### 审核异步 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.audit.data.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| `async.audit.data.sub_resp_desc` | 业务返回描述 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| `async.audit.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原样返回请求参数的请求流水号；示例值：[官网示例已脱敏] |
| `async.audit.data.req_date` | 请求时间 | `String` | `8` | `Y` | 原请求时间yyyyMMdd；示例值：20220912 |
| `async.audit.data.audit_status` | 审核结果 | `String` | `1` | `Y` | Y：审核通过 N：审核拒绝 F：失败 C：拒签；示例值：Y |
| `async.audit.data.audit_desc` | 审核描述 | `String` | `512` | `N` | 审核结果描述 |
| `async.audit.data.product_id` | 产品编号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：YYZY |
| `async.audit.data.huifu_id` | 汇付客户号 | `String` | `18` | `Y` | 汇付分配的商户号，示例值：[官网示例已脱敏] |
| `async.audit.data.apply_no` | 申请单号 | `String` | `18` | `N` | 汇付返回商户的业务申请单号；示例值：202209120038432 |

### 逐业务结果异步

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.business.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | 业务返回码 |
| `async.business.sub_resp_desc` | 业务返回描述 | `String` | `512` | `Y` | 业务返回描述 |
| `async.business.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原请求流水号；示例值：[官网示例已脱敏] |
| `async.business.req_date` | 请求时间 | `String` | `8` | `Y` | 原请求时间yyyyMMdd；示例值：20220912 |
| `async.business.product_id` | 产品编号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：YYZY |
| `async.business.huifu_id` | 汇付客户号 | `String` | `18` | `Y` | 汇付分配的商户号，示例值：[官网示例已脱敏] |
| `async.business.apply_no` | 申请单号 | `String` | `18` | `N` | 汇付返回商户的业务申请单号；示例值：202209120038432 |
| `async.business.notify_type` | 通知类型 | `String` | `1` | `Y` | W:微信 A：支付宝，Y:抖音，U:银联二维码，B:刷卡 E：全域资金管理，J:大额转账备付金模式，I:大额转账银行模式示例值：W |
| `async.business.reg_result_list[]` | 入驻结果集合 | `Array` | `—` | `N` | josnArray格式；notify_type等于A或者W时，此集合可能有多条数据 |
| `async.business.reg_result_list[].pay_scene` | 费率类型 | `String` | `2` | `N` | 请求参数pay_scene；当notify_type是W/A时返回；参见《[微信支付场景](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e6%94%af%e4%bb%98%e5%9c%ba%e6%99%af)》说明；示例值：1 |
| `async.business.reg_result_list[].business_stat` | 业务开通状态 | `String` | `1` | `N` | S-成功，F-失败；当notify_type是W/A/E时返回；示例值：S |
| `async.business.reg_result_list[].business_desc` | 业务开通描述 | `String` | `200` | `N` | 当notify_type是W/A/E时返回 |
| `async.business.reg_result_list[].sub_mer_id` | 二级商户号 | `String` | `32` | `N` | 微信/支付宝二级商户号；当notify_type是W/A时返回；示例值：A[官网示例已脱敏] |
| `async.business.reg_result_list[].bank_channel_no` | 渠道号 | `String` | `50` | `N` | 当notify_type是W/A时返回；示例值：JP00001 |
| `async.business.reg_result_list[].bank_mer_code` | 真实商户号 | `String` | `20` | `N` | 当notify_type是W/A时返回；示例值：[官网示例已脱敏] |
| `async.business.reg_result_list[].electron_bank_name` | 电子账户开户行 | `String` | `32` | `N` | 全域资金管理电子账户开户行, 当notify_type是E时返回；示例值：武汉众邦银行股份有限公司 |
| `async.business.reg_result_list[].electron_account` | 电子账号 | `String` | `32` | `N` | 全域资金管理电子账号, 当notify_type是E时返回；示例值：[官网示例已脱敏] |
| `async.business.reg_result_list[].real_name_applyment_stat` | 实名认证状态 | `String` | `64` | `N` | W:微信 A：支付宝 申请实名时返回；A：支付宝对应值；审核中(AUDITING)；待联系人确认(CONTACT_CONFIRM)；待法人确认(LEGAL_CONFIRM)；审核通过(AUDIT_PASS)；审核失败(AUDIT_REJECT)；已冻结(AUDIT_FREEZE)；已撤回(CANCELED)；未申请(NOT_APPLY)；W:微信对应值；APPLYMENT_STATE_EDITTING--【编辑中】--可能在提交申请时发生错误导致，可用同一个业务申请编号重新提交；APPLYMENT_STATE_WAITTING_FOR_AUDIT--【审核中】--请耐心等待1~2个工作日，微信支付将会完成审核；APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT--【待确认联系信息】--请扫描微信支付返回的小程序码确认联系信息(此过程可修改超级管理员手机号)；APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON--【待账户验证】--请扫描微信支付返回的小程序码在小程序端完成账户验证；APPLYMENT_STATE_PASSED--【审核通过】--请扫描微信支付返回的小程序码在小程序端完成授权流程；APPLYMENT_STATE_REJECTED--【审核驳回】--请按照驳回原因修改申请资料，并更换业务申请编码，重新提交申请；APPLYMENT_STATE_FREEZED--【已冻结】--可能是该主体已完成过入驻，请查看驳回原因，并通知驳回原因中指定的联系人扫描微信支付返回的小程序码在小程序端完成授权流程；APPLYMENT_STATE_CANCELED--【已作废】--表示申请单已被撤销，无需再对其进行操作；APPLYMENT_STATE_NOAPPLY--未申请；示例值：AUDITING |
| `async.business.reg_result_list[].real_name_applyment_desc` | 实名认证描述 | `String` | `128` | `N` | W:微信 A：支付宝 申请实名时返回；示例值：W |
| `async.business.reg_result_list[].qrcode_data` | 授权二维码 | `String` | `512` | `N` | W:微信 A：支付宝 申请实名时返回；若notify_type=W时 且 实名认证状态 real_name_applyment_stat=；APPLYMENT_STATE_WAITTING_FOR_CONFIRM_CONTACT、；APPLYMENT_STATE_WAITTING_FOR_CONFIRM_LEGALPERSON、；APPLYMENT_STATE_PASSED、；APPLYMENT_STATE_FREEZED时返回；若notify_type=A时 且 实名认证状态 real_name_applyment_stat=；CONTACT_CONFIRM、LEGAL_CONFIRM时返回；示例值：https://qr.alipay.com/bax02911brluc2xieoph6001 |
| `async.business.reg_result_list[].agreement_link` | 协议签署连接 | `String` | `1024` | `N` | 申请实名且签署电子协议时返回；示例值： |
| `async.business.reg_result_list[].agreement_id` | 协议编号 | `String` | `64` | `N` | 申请实名且签署电子协议时返回；示例值： |
| `async.business.reg_result_list[].agreement_name` | 协议名称 | `String` | `256` | `N` | 申请实名且签署电子协议时返回；示例值： |
| `async.business.ord_id` | 通知流水号 | `String` | `44` | `N` | 回调方返回应答，应答内容为：”RECV_ORD_ID_”+该ordId |
| `async.business.zl_async_info` | 直连结果合集 | `Object` | `512` | `N` | 直连微信/支付宝结果合集 |
| `async.business.zl_async_info.confirm_url` | 签约链接 | `String` | `256` | `N` | 示例值：https://www.huifu.com |
| `async.business.zl_async_info.mer_app_id` | 应用ID | `String` | `32` | `N` | 示例值：wx51aa91a575359ff5 |
| `async.business.zl_async_info.reject_reason` | 拒绝原因 | `String` | `128` | `N` | 示例值：支付功能未开通 |
| `async.business.zl_async_info.sub_mch_id` | 支付宝/微信商户号 | `String` | `32` | `N` | 示例值：1632157057 |
| `async.business.zl_async_info.apply_type` | 申请类型 | `String` | `32` | `N` | 示例值：FACE_TO_FACE |
| `async.business.zl_async_info.apply_state` | 申请单状态 | `String` | `1` | `N` | S：审核通过，P：审核中，N：审核拒绝，F：系统处理失败；新增状态枚举：C：待签约 |

### 电子协议异步

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.agreement.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | 业务返回码 |
| `async.agreement.sub_resp_desc` | 业务返回描述 | `String` | `512` | `N` | 业务返回描述 |
| `async.agreement.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原请求流水号；示例值：[官网示例已脱敏] |
| `async.agreement.req_date` | 请求日期 | `String` | `8` | `Y` | 原请求时间yyyyMMdd；示例值：20220912 |
| `async.agreement.huifu_id` | 汇付分配的商户号 | `String` | `18` | `Y` | 汇付分配的商户号，示例值：[官网示例已脱敏] |
| `async.agreement.apply_no` | 申请单号 | `String` | `18` | `Y` | 汇付返回商户的业务申请单号；示例值：202209120038432 |
| `async.agreement.agreement_info_list` | 协议信息 | `Object` | `—` | `N` | 签署电子协议时返回 |
| `async.agreement.agreement_info_list.agreement_type` | 协议类型 | `String` | `1` | `N` | 0-电子协议 |
| `async.agreement.agreement_info_list.agreement_link` | 协议签署链接 | `String` | `512` | `N` | 协议签署链接 |
| `async.agreement.agreement_info_list.agreement_no` | 协议号 | `String` | `32` | `N` | 示例值：3245234 |
| `async.agreement.agreement_info_list.agreement_name` | 协议名称 | `String` | `128` | `N` | 协议名称 |
| `async.agreement.agreement_info_list.con_stat` | 合同状态 | `String` | `2` | `N` | 电子协议类型会返回以下值： 2：创建合同异常 3：待签约 4：签约中 5：签约完成(电子协议只有签约完成才能做交易) 6：已失效 7：已拒签 8：签约失败 示例值：5 |

## 商户基本信息修改

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shjbxxxg_kyc.md>
- SHA-256：`f2146bc553eb4b1dc8c88d4487eb1b5c721468d6a8eec5be7d0ce9f086db4d6c`
- 说明：下表保留官方字段类型、长度、必填标记和字段说明；数组父路径以 `[]` 标记。

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
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号，同一商户号当天唯一；示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd，以北京时间为准 示例值：20220125 |
| `request.data.upper_huifu_id` | 直属渠道号 | `String` | `18` | `C` | 该商户进件完成后归属的渠道商huifu_id；sys_id主体为渠道商时填写；sys_id主体为总部商户时选填；示例值：[官网示例已脱敏] |
| `request.data.huifu_id` | 汇付客户Id | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] |
| `request.data.reg_name` | 商户名称 | `String` | `64` | `N` | 商户未开通业务时，支持修改。商户名称，必须与商家营业执照上的名称一致；个体工商户的营业执照如没有名称、名称为“\*”或空，则商户名称应填 “个体户XXX”（XXX为营业执照上经营者姓名），如“个体户张三”，汉字以2个字符计算。示例值：上海汇付支付有限公司 |
| `request.data.short_name` | 商户简称 | `String` | `64` | `N` | 商户简称，需与商户注册名称相关；示例值：汇付商城 |
| `request.data.mer_en_name` | 商户英文名称 | `String` | `256` | `N` | 商户英文名称；示例值：huifupay |
| `request.data.ent_type` | 公司类型 | `String` | `1` | `N` | 商户未开通业务时，支持修改。；1：政府机构；2：国营企业；3：私营企业；4：外资企业；5：个体工商户；6：其它组织；7：事业单位；9：业主委员会；示例值1 |
| `request.data.mcc` | 所属行业 | `String` | `7` | `N` | 商户未开通业务时，支持修改。参考[汇付MCC编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm) ；示例值：5311 |
| `request.data.license_type` | 营业执照类型 | `String` | `32` | `N` | 参见[机构证照类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E6%9C%BA%E6%9E%84%E8%AF%81%E7%85%A7%E7%B1%BB%E5%9E%8B)说明； 示例值：NATIONAL_LEGAL |
| `request.data.license_code` | 营业执照编号 | `String` | `18` | `N` | 商户未开通业务时，支持修改。工商营业执照编号。示例值：92650109MA79R8E308 |
| `request.data.license_validity_type` | 营业执照有效期类型 | `String` | `1` | `N` | 营业执照有效期类型;0：非长期有效； 1：长期有效；示例值：0 ；当使用总部资质时不填 |
| `request.data.license_begin_date` | 营业执照有效期开始日期 | `String` | `8` | `N` | 日期格式：yyyyMMdd，以北京时间为准； 示例值：20220125；当使用总部资质时不填 |
| `request.data.license_end_date` | 营业执照有效期截止日期 | `String` | `8` | `N` | 日期格式：yyyyMMdd，以北京时间为准。 ； 当license_validity_type=0时必填 ；当license_validity_type=1时为空；当使用总部资质时不填 ；示例值：20220125 |
| `request.data.reg_prov_id` | 注册省 | `String` | `6` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000 ；如修改省市区要级联修改；当使用总部资质时不填 |
| `request.data.reg_area_id` | 注册市 | `String` | `6` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000 ；如修改省市区要级联修改；当使用总部资质时不填 |
| `request.data.reg_district_id` | 注册区 | `String` | `6` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000；如修改省市区要级联修改 ；当使用总部资质时不填 |
| `request.data.reg_detail` | 注册详细地址 | `String` | `255` | `N` | 商户注册地址或营业执照住所，汉字以2个字符计算；，；示例值：上海市徐汇区XX路XX号；当使用总部资质时不填 |
| `request.data.reg_capital` | 注册资本 | `String` | `32` | `N` | 保留两位小数，国营企业、私营企业、外资企业、政府机构、事业单位、其他、集体经济必填，个体工商户可为空；示例值：100.00 |
| `request.data.business_scope` | 经营范围 | `String` | `64` | `N` | 示例值：日用百货、化妆品、珠宝、化工原料及产品(除危险品)、化学品、纺织原料 |
| `request.data.found_date` | 成立时间 | `String` | `8` | `N` | 示例值：20091212 |
| `request.data.legal_name` | 法人姓名 | `String` | `32` | `N` | 企业商户法人。最大支持16个汉字。企业商户时，结算类型为对私法人时，如果卡信息中证件号，证件类型，结算人证件有效期开始日期，结算人证件有效期结束日期，证件有效期类型任一字段为空，则必填。；当使用总部资质时不填；示例值：张三 |
| `request.data.legal_cert_type` | 法人证件类型 | `String` | `2` | `N` | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》。当card_type=0时为空； 当card_type=1或2时选填 示例值：00；当使用总部资质时不填 |
| `request.data.legal_cert_no` | 法人证件号码 | `String` | `32` | `N` | 法人证件号码，如法人证件类型为00：身份证，则填写身份证号码；示例值：[官网示例已脱敏]；当使用总部资质时不填；年龄不能小于18岁且不能大于80岁 |
| `request.data.legal_cert_validity_type` | 法人证件有效期类型 | `String` | `1` | `N` | 0：非长期有效；1：长期有效；示例值：0 |
| `request.data.legal_cert_begin_date` | 法人证件有效期开始日期 | `String` | `8` | `N` | 日期格式：yyyyMMdd，以北京时间为准；示例值：20220125 ；当使用总部资质时不填 |
| `request.data.legal_cert_end_date` | 法人证件有效期截止日期 | `String` | `8` | `N` | 日期格式：yyyyMMdd，以北京时间为准。示例值：20220125；当legal_cert_validity_type=0时必填；当legal_cert_validity_type=1时为空；当使用总部资质时不填 |
| `request.data.legal_addr` | 法人身份证地址 | `String` | `256` | `N` | 示例值：上海市徐汇区宜山路700号普天信息产业园2期C5栋 |
| `request.data.legal_mobile_no` | 法人手机号 | `String` | `11` | `N` | 示例值：[官网示例已脱敏] |
| `request.data.occupation` | *负责人职业* | `String` | `2` | `N` | 1A：各类专业,技术人员；1B：国家机关,党群组织,企事业单位的负责人；1C：办事人员和有关人员；1D：商业工作人员；1E：服务性工作人员；1F：农林牧渔劳动者；1G：生产工作,运输工作和部分体力劳动者；1H：不便分类的其他劳动者；个人商户可修改；示例值：1G |
| `request.data.prov_id` | 经营省 | `String` | `6` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000 ；如修改省市区要级联修改 |
| `request.data.area_id` | 经营市 | `String` | `6` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310100 ；如修改省市区要级联修改 |
| `request.data.district_id` | 经营区 | `String` | `6` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000 ；如修改省市区要级联修改 |
| `request.data.detail_addr` | 经营详细地址 | `String` | `255` | `N` | 示例值：上海市徐汇区XX路XX号 |
| `request.data.contact_name` | 管理员姓名 | `String` | `30` | `N` | 默认法人姓名；最大支持15个汉字。示例值：张三 |
| `request.data.contact_email` | 管理员电子邮箱 | `String` | `32` | `N` | 联系人电子邮箱，需要带@，遵循邮箱格式 ；示例值：huifu@xxx.com |
| `request.data.service_phone` | 客服电话 | `String` | `32` | `N` | 支持固话格式，手机格式；默认联系人手机号；示例值：021XXXXXXXX |
| `request.data.receipt_name` | 小票名称 | `String` | `50` | `N` | 可以作为POS小票的名称；示例值：汇付商城 |
| `request.data.card_info` | *结算卡信息配置* | `String` | `—` | `N` | 商户结算账户信息配置，jsonObject字符串；开通中信E管家结算的银行卡配置在【elec_acct_config】中 |
| `request.data.card_info.card_type` | 结算账户类型 | `String` | `1` | `Y` | 0：对公账户 1：对私法人账户 2：对私非法人账户 示例值：0；个人商户/用户不支持填写对公账户和对私非法人账户。；若涉及结算账户类型变更，请前往 [企业商户结算人变更](https://paas.huifu.com/open/doc/api/#/shgl/shjj/changeofpayee)了解意愿核实方案 |
| `request.data.card_info.card_name` | 结算账户名 | `String` | `128` | `Y` | 示例值：上海汇付支付有限公司； 当card_type=0时填写企业名称，，**企业非同名时，需要在extended_material_list中额外上传非同名结算证明材料，文件枚举：F516**； 当card_type=1时填写法人姓名，**对私法人结算银行户名与法人姓名必需一致**；当card_type=2时填写非法人姓名 |
| `request.data.card_info.card_no` | 结算账号 | `String` | `32` | `Y` | 结算账号，结算银行卡号，为避免资金结算失败，请正确填写；示例值：[官网示例已脱敏]；注意：系统会验证卡号所属银行，请准确填写 |
| `request.data.card_info.prov_id` | 银行所在省 | `String` | `6` | `N` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310000 ；如修改省市要级联修改 |
| `request.data.card_info.area_id` | 银行所在市 | `String` | `8` | `Y` | 参考[地区编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)；示例值：310100 ；如修改省市要级联修改 |
| `request.data.card_info.branch_code` | 支行联行号 | `String` | `12` | `C` | 当card_type=0时必填。参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm) 当card_type=0时必填， 当card_type=1或2时非必填 示例值：102290026507 |
| `request.data.card_info.cert_type` | 持卡人证件类型 | `String` | `2` | `C` | 参见《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》。； 当card_type=0时为空， 当card_type=1或2时必填； 示例值：00；持卡人证件类型04、11需要补充 F101【结算人】港澳台居民来往内地通行证；持卡人证件类型13需要补充 F513【结算人】外国人居留证；持卡人证件类型14、15需要补充 F514【结算人】港澳台居住证；其它持卡人证件类型补充F102【结算人】其它证件材料；补充材料填写在extended_material_list 扩展资料包中 |
| `request.data.card_info.cert_no` | 持卡人证件号码 | `String` | `32` | `N` | 持卡人证件号码，如持卡人证件类型为00：身份证，则填写身份证号码；示例值：[官网示例已脱敏]；当card_type=0时为空；当card_type=1或2时必填；年龄不能小于18岁且不能大于80岁 |
| `request.data.card_info.cert_validity_type` | 持卡人证件有效期类型 | `String` | `1` | `C` | 0：非长期有效, 1：长期有效, 示例值：0；当card_type=0时为空； 当card_type=1或2时必填 |
| `request.data.card_info.cert_begin_date` | 持卡人证件有效期开始日期 | `String` | `8` | `C` | 日期格式：yyyyMMdd，以北京时间为准； 当card_type=0时为空， 当card_type=1或2时必填， 示例值：20220125 |
| `request.data.card_info.cert_end_date` | 持卡人证件有效期截止日期 | `String` | `8` | `C` | 日期格式：yyyyMMdd，以北京时间为准。示例值：20220125； 当cert_validity_type=0时必填；当cert_validity_type=1时为空 |
| `request.data.card_info.reg_acct_pic` | 开户许可证 | `String` | `128` | `C` | 开户许可证图片文件，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F08；企业商户需要，结算账号为对公账户必填；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.card_info.legal_cert_front_pic` | 法人身份证人像面 | `String` | `128` | `C` | 请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F02；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.card_info.legal_cert_back_pic` | 法人身份证国徽面 | `String` | `128` | `C` | 请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F03；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.card_info.settle_card_front_pic` | 银行卡卡号面 | `String` | `128` | `C` | 银行卡卡号面图片文件对私结算必填，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F13；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.card_info.settle_cert_front_pic` | 结算人身份证人像面 | `String` | `128` | `C` | 对私结算必填，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F55；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.card_info.settle_cert_back_pic` | 结算人身份证国徽面 | `String` | `128` | `C` | 对私结算必填，请填写图片file_id，可通过 [商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc) 接口获取，文件类型F56；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.card_info.mp` | 结算人手机号 | `String` | `11` | `N` | 需为11位数字；示例值：[官网示例已脱敏] ；当card_type=0时为空; 当card_type=1或2时可修改；开通全域资金管理功能可修改 |
| `request.data.card_info.authentication_type` | 变更结算人核验方式 | `String` | `1` | `N` | 0：短信验证码 （不填默认）；1：短信链接 ；2：材料核实；示例值：1；当审核结果、意愿核验、电子协议签约均通过时，结算变更生效。 |
| `request.data.card_info.verify_code` | 短信验证码 | `String` | `6` | `C` | 结算卡、结算人变更需要短信验证码；当【变更结算人核验方式 = 0】时必填。 请先调用商户短信发送接口；示例值：851249 |
| `request.data.card_info.authentication_person_type` | 核验人类型 | `String` | `1` | `C` | 当【变更结算人核验方式 = 1】时必填。企业用户选择0:法人，1:原持卡人；示例值：0 |
| `request.data.card_info.authentication_person_mobile` | 核验人手机号 | `String` | `11` | `C` | 当【变更结算人核验方式 = 1】时必填。请根据核验人类型传入核验人实名手机号。示例值：[官网示例已脱敏] |
| `request.data.card_info.acct_ids` | 适用子账户 | `String` | `128` | `N` | 结算卡适用子账户，多个用逗号隔开；示例值：D02348323,D01236743 |
| `request.data.card_info.is_settle_default` | 默认结算卡标志 | `String` | `1` | `N` | 是否为默认结算卡标志；Y:是 N:否；如需更换结算卡，该字段需上送为Y；示例值：Y |
| `request.data.settle_agree_pic` | 结算协议图片文件 | `String` | `128` | `N` | 请填写图片file_id，示例值：57cc7f00-600a-33ab-b614-6221bbf2e529；可通过[商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)接口获取，文件类型F116 |
| `request.data.cash_config[]` | 取现信息配置 | `String` | `—` | `N` | 商户取现信息配置，jsonArray字符串 |
| `request.data.cash_config[].switch_state` | 状态 | `String` | `1` | `Y` | 1:开通 0:关闭 ；示例值：1 |
| `request.data.cash_config[].cash_type` | 业务类型 | `String` | `2` | `Y` | D0：当日到账；当日交易资金当天可取现到账；T1：下个工作日到账；D1：下个自然日到账；DM：当日到账；到账资金不包括当天的交易资金；示例值：T1 |
| `request.data.cash_config[].fix_amt` | 提现手续费（固定/元） | `String` | `6` | `C` | fix_amt与fee_rate至少填写一项， 需保留小数点后两位，不收费请填写0.00；示例值：1.00；注：当cash_type=D1时为节假日取现手续费 |
| `request.data.cash_config[].fee_rate` | 提现手续费率（%） | `String` | `6` | `C` | fix_amt与fee_rate至少填写一项，需保留小数点后两位，取值范围[0.00,100.00]，不收费请填写0.00；示例值：0.05；注：1、如果fix_amt与fee_rate都填写了则手续费=fix_amt+支付金额\*fee_rate；2、当cash_type=D1时为节假日取现手续费 |
| `request.data.cash_config[].weekday_fix_amt` | D1工作日取现手续费固定金额 | `String` | `6` | `C` | 单位元，需保留小数点后两位。不收费请填写0.00；示例值：1.00；cash_type=T1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算，若未配置则默认按照节假日手续费计算 |
| `request.data.cash_config[].weekday_fee_rate` | D1工作日取现手续费率 | `String` | `6` | `C` | 单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；示例值：0.05；cash_type=T1时，不生效 ；cash_type取现类型为D1时，遇工作日按此费率结算 ，若未配置则默认按照节假日手续费计算 |
| `request.data.cash_config[].out_fee_flag` | 是否交易手续费外扣 | `String` | `1` | `N` | 1:外扣 2:内扣（默认2内扣）；示例值：2 |
| `request.data.cash_config[].out_fee_huifu_id` | 手续费承担方 | `String` | `18` | `N` | 手续费外扣时必需指定手续费承担方ID；示例值：[官网示例已脱敏] |
| `request.data.cash_config[].out_fee_acct_type` | 手续费外扣的账户类型 | `String` | `2` | `N` | 01-基本户，02-现金户，05-充值户；不填默认01；示例值：01 |
| `request.data.cash_config[].is_priority_receipt` | 是否优先到账 | `String` | `1` | `N` | Y：是 ，N：否。不填，默认值为否。仅在取现类型配置为D1 和 T1 时生效。示例值：Y |
| `request.data.settle_config` | 结算规则配置 | `String` | `—` | `N` | 商户结算规则配置，jsonObject字符串 |
| `request.data.settle_config.settle_status` | 结算开关 | `String` | `1` | `Y` | 1:开通 0:关闭；示例值：1 |
| `request.data.settle_config.settle_cycle` | 结算周期 | `String` | `2` | `Y` | D1：下个自然日结算， T1：下个工作日结算；TS:笔笔结算； 示例值：T1 |
| `request.data.settle_config.min_amt` | 起结金额 | `String` | `17` | `N` | settle_cycle为TS时不填。账户余额大于等于起结金额才会发起结算。不传则不设置起结金额；单位元，小数点后两位，取值范围[0.00，99999999999.99]。示例值：1000.00 |
| `request.data.settle_config.remained_amt` | 留存金额 | `String` | `17` | `N` | settle_cycle为TS时不填。该部分资金不会结算。不传则不设置留存金额；单位元，需保留小数点后两位，取值范围[0.00，99999999999.99]。示例值：1000.00 |
| `request.data.settle_config.settle_abstract` | 结算摘要 | `String` | `128` | `N` | 结算摘要，可自定义结算打款备注，不填默认为空；支持配置格式化摘要内容，参见[结算配置示例说明](https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm)；示例值：汇付商城业务 |
| `request.data.settle_config.out_settle_flag` | 手续费外扣标记 | `String` | `1` | `N` | 1:外扣：结算时，从out_settle_huifuid账户扣手续费；2:内扣：从结算金额中扣手续费，默认为内扣；示例值：2 |
| `request.data.settle_config.out_settle_huifuid` | 结算手续费外扣商户号 | `String` | `18` | `C` | 结算手续费外扣商户号，填写承担手续费的汇付商户号；当out_settle_flag=1时必填，否则非必填；示例值：[官网示例已脱敏] |
| `request.data.settle_config.out_settle_acct_type` | 结算手续费外扣时的账户类型 | `String` | `2` | `N` | 结算手续费外扣账户类型；01：基本户（不填默认取值）；02：现金户；05：充值户；09：营销户；示例值：01 |
| `request.data.settle_config.settle_batch_no` | 结算批次号 | `String` | `16` | `N` | settle_cycle为TS时不填。结算批次号，按指定结算批次号进行资金结算；示例值：0；[参见结算批次说明](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc) |
| `request.data.settle_config.is_priority_receipt` | 是否优先到账 | `String` | `1` | `N` | settle_cycle为TS时不填。当settle_pattern=P0时选填，不填默认为N，该值在结算那批次号[0-500]间生效； Y：是，N：否，示例值：Y |
| `request.data.settle_config.settle_time` | 自定义结算处理时间 | `String` | `6` | `N` | settle_cycle为TS时不填。当settle_pattern=P1/P2自定义时间结算时必填；注意：00:00到00:30不能指定；到账时间，格式：HHmmss；示例值：103000 |
| `request.data.settle_config.fixed_ratio` | 节假日结算手续费率 | `String` | `6` | `C` | settle_cycle为D1、TS时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不收费请填写0.00；settle_cycle=T1时，不生效 ；settle_cycle为D1时，遇节假日按此费率结算 ；示例值：0.05 |
| `request.data.settle_config.constant_amt` | 节假日结算手续费固定金额 | `String` | `15` | `C` | settle_cycle为D1、TS时必填。单位元，需保留小数点后两位。不收费请填写0.00；settle_cycle结算周期为D1时，遇节假日按此费率结算；示例值：1.00 |
| `request.data.settle_config.workday_fixed_ratio` | 工作日结算手续费率 | `String` | `6` | `N` | settle_cycle为TS时必填。单位%，需保留小数点后两位。取值范围[0.00，100.00]，不填默认为0.00；示例值：0.05 |
| `request.data.settle_config.workday_constant_amt` | 工作日结算手续费固定金额 | `String` | `15` | `N` | settle_cycle为TS时必填。单位元，需保留小数点后两位。不填默认为0.00；示例值：1.00 |
| `request.data.settle_config.settle_pattern` | 结算方式 | `String` | `2` | `N` | settle_cycle为TS时不填。结算方式，批次结算指按照结算批次号进行资金结算，定时结算是指按照指定到账时间进行资金结算，不填默认P0：批次结算； P0：批次结算 ，P1：定时结算(建议选P0和P2)，P2:批次定时结算，E1:中信E管家 示例值：P1 |
| `request.data.mer_url` | 商户主页URL | `String` | `256` | `N` | 商户主页URL；示例值：https://paas.huifu.com/ |
| `request.data.mer_icp` | 商户ICP备案编号 | `String` | `50` | `N` | 商户ICP备案编号或网站许可证号；示例值：沪ICP备06046402号-28 |
| `request.data.beneficiary_info[]` | 受益人列表 | `String` | `—` | `N` | jsonArray字符串 |
| `request.data.beneficiary_info[].bo_id` | 受益唯一ID | `String` | `32` | `N` | 新增受益人时无需填写；示例值：[官网示例已脱敏] |
| `request.data.beneficiary_info[].bo_name` | 受益人名称 | `String` | `40` | `N` | 示例值：张三 |
| `request.data.beneficiary_info[].bo_type` | 受益人证件类型 | `String` | `2` | `N` | 00:身份证； 01:护照； 02:军官证； 03:士兵证； 04:回乡证； 05:户口本； 06:外国护照； 07:其他； 08:暂住证； 09:警官证； 10:文职干部证； 11:港澳同胞回乡证； 12:营业执照；示例值：00 |
| `request.data.beneficiary_info[].bo_no` | 受益人证件号 | `String` | `50` | `N` | 示例值：[官网示例已脱敏] |
| `request.data.beneficiary_info[].bo_date_start` | 受益人证件有效期开始时间 | `String` | `8` | `N` | 示例值：20210606 |
| `request.data.beneficiary_info[].bo_deadline` | 受益人证件有效期结束时间 | `String` | `8` | `N` | 示例值：20290606；若证件有效期为长期，请填写：29991231；要求结束时间大于开始时间 |
| `request.data.beneficiary_info[].bo_address` | 受益人地址 | `String` | `500` | `N` | 示例值：上海徐汇区共富一路55号401室 |
| `request.data.beneficiary_info[].bo_mobile_no` | 受益人手机号 | `String` | `11` | `C` | 开通全域资金管理业务时必填；示例值：[官网示例已脱敏] |
| `request.data.beneficiary_info[].final_beneficiary_mode` | 最终受益人受益方式 | `String` | `3` | `C` | A01：直接或间接控股25%（含）以上 ；A02：通过人事、财务等其他方式对公司进行控制 ；A03：高级管理人员 ；A04：法人或公司负责人 ；A05：其他；示例值：A01 ；开通全域资金管理业务时必填 |
| `request.data.beneficiary_info[].bo_stat` | 受益人有效标识 | `String` | `10` | `N` | active：有效，inactive：无效 示例值：active |
| `request.data.sign_user_info` | 签约人 | `String` | `—` | `C` | jsonObject格式；agreement_info中选择电子签约时必填；个人商户填本人信息。 |
| `request.data.sign_user_info.type` | 签约人类型 | `String` | `7` | `Y` | LEGAL-法人，对公结算或对私法人结算时可选法人签约；CONTACT-联系人，对公结算可选联系人（经办人）签约；OTHER-其他，对私非法人结算选“其他”，必须是结算人；示例值：LEGAL |
| `request.data.sign_user_info.name` | 姓名 | `String` | `32` | `N` | 签约人类型=其他，必填；示例值：张三 |
| `request.data.sign_user_info.mobile_no` | 手机号 | `String` | `11` | `N` | 签约人类型=法人/其他 ，必填；注意：**签约人会做姓名+身份证+手机号验证，请正确填写**；示例值：[官网示例已脱敏] |
| `request.data.sign_user_info.cert_no` | 身份证 | `String` | `32` | `N` | 签约人类型=联系人/其他，必填；注意：**签约人会做姓名+身份证+手机号验证，请正确填写**；示例值：[官网示例已脱敏] |
| `request.data.agreement_info` | 协议信息 | `String` | `—` | `N` | jsonObject格式；[签约协议材料说明](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%95%86%E6%88%B7%E5%90%88%E5%90%8C%E7%AD%BE%E7%BA%A6%E8%A7%84%E5%88%99.xlsx)；若未签署过协议的情况下，调用该接口时必填 ，且注册地址或经营地址为如下地区（江苏省、浙江省、湖南省、湖北省、云南省、贵州省、陕西省、河南省、吉林省、黑龙江省、福建省、海南省、重庆市、青海省、宁夏回族自治区）开通银联二维码或刷卡业务不支持挂网协议；若已签署过纸质或电子协议下，调用该接口时必填，且只可以选择纸质或电子协议；若已签署过挂网协议下，调用该接口时，选填。 |
| `request.data.agreement_info.agreement_type` | 协议类型 | `String` | `1` | `Y` | 0-电子协议，1-纸质协议，3-挂网协议示例值：3 |
| `request.data.agreement_info.agreement_url` | 挂网协议地址 | `String` | `256` | `C` | 挂网协议必填；**必须按示例值填写**，示例值：https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/PaymentServiceAgreement.htm |
| `request.data.agreement_info.agree_begin_date` | 纸质协议开始日期 | `String` | `8` | `N` | 示例值：20220606 |
| `request.data.agreement_info.agree_end_date` | 纸质协议结束日期 | `String` | `8` | `N` | 示例值：20230606；要求结束时间大于开始时间 |
| `request.data.agreement_info.agreement_async_return_url` | 电子协议异步通知地址 | `String` | `128` | `N` | 示例值：http://service.example.com/to/path |
| `request.data.license_pic` | 营业执照图片 | `String` | `64` | `N` | 企业商户可改。通过[商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)接口获取file_id，[参考文件类型](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)：F07；**注意执照不能是过期的**；示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.auth_entrust_pic` | 授权委托书 | `String` | `64` | `N` | 通过[商户图片上传](https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc)接口获取file_id，[参考文件类型](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)：F15；请填写图片file_id，[下载模板](https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/12%E3%80%90%E5%95%86%E6%88%B7%E3%80%91%E6%8E%88%E6%9D%83%E7%BB%93%E7%AE%97%E5%A7%94%E6%89%98%E4%B9%A6%EF%BC%88%E5%AF%B9%E7%A7%81%E7%BB%93%E7%AE%97%EF%BC%89%EF%BC%88%E7%BA%B8%E8%B4%A8%E5%90%88%E5%90%8C%E7%89%88%EF%BC%89.docx)。示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.scene_type` | 场景类型 | `String` | `8` | `N` | ONLINE：线上场景，OFFLINE：线下场景，ALL：线上线下；示例值：ALL |
| `request.data.store_header_pic` | 店铺门头照 | `String` | `64` | `N` | 文件类型：F22；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530；微信/支付宝实名认证个人商户，门头照也使用此字段；门店场所：提交门店门口照片，要求招牌清晰可见; ；小微商户流动经营/便民服务：提交经营/服务现场照片 |
| `request.data.store_indoor_pic` | 店铺内景/工作区域照 | `String` | `64` | `N` | 文件类型：F24；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530；微信/支付宝实名认证个人商户，内景照也使用此字段；门店场所：提交店内环境照片 ；小微商户流动经营/便民服务：可提交另一张经营/服务现场照片 |
| `request.data.store_cashier_desk_pic` | 店铺收银台/公司前台照 | `String` | `64` | `N` | 文件类型：F105；示例值：57cc7f00-600a-33ab-b614-6221bbf2e530 |
| `request.data.extended_material_list[]` | 扩展资料包 | `String` | `—` | `N` | jsonArray字符串。根据要求上传补充相关材料 |
| `request.data.extended_material_list[].file_id` | 文件id | `String` | `64` | `N` | 请填写图片file_id，可通过 商户图片上传 接口获取； 示例值：57cc7f00-600a-33ab-b614-6221bbf2e529 |
| `request.data.extended_material_list[].file_type` | 文件类型 | `String` | `64` | `N` | 参见文件类型说明；示例值：F01 |
| `request.data.async_return_url` | 异步通知地址 | `String` | `128` | `N` | 审核结果消息接收地址，为空时不推送消息；示例值：http://service.example.com/to/path |
| `request.data.elec_acct_config` | 斗拱e账户功能配置 | `String` | `—` | `N` | 用于总部商户、下级商户配置斗拱E账户功能 |
| `request.data.elec_acct_config.switch_state` | 电子账户开关 | `String` | `1` | `Y` | 电子账户开通总开关；0:关闭 1:开通；示例值：1 |
| `request.data.elec_acct_config.acct_type` | 账户类型 | `String` | `2` | `Y` | 01：中信e管家；示例值：01 |
| `request.data.elec_acct_config.cash_fee_party` | 电子账户提现手续费承担方 | `String` | `1` | `C` | 下级商户必填；1:总部 2:其他；示例值：1 |
| `request.data.elec_acct_config.scene` | 场景类型 | `String` | `3` | `Y` | 必填；与角色类型关联，[中信定义的资金类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；示例值：001 |
| `request.data.elec_acct_config.role_type` | 角色类型 | `String` | `6` | `Y` | 角色编号必填；与场景关联，[中信定义的角色类型](https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx)；示例值：001001 |
| `request.data.elec_acct_config.elec_card_list[]` | 银行卡信息 | `String` | `—` | `N` | jsonArray字符串 |
| `request.data.elec_acct_config.elec_card_list[].prov_id` | 银行所在省 | `String` | `6` | `N` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm)示例值：310000 |
| `request.data.elec_acct_config.elec_card_list[].area_id` | 银行所在市 | `String` | `6` | `N` | [参考省市区编码表；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm) 示例值：310100 |
| `request.data.elec_acct_config.elec_card_list[].bank_code` | 银行编码 | `String` | `8` | `Y` | [参考银行编码；](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm) 示例值：01020000 |
| `request.data.elec_acct_config.elec_card_list[].branch_code` | 支行联行号 | `String` | `12` | `Y` | 参考：[银行支行编码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm)；示例值：102290026507 |
| `request.data.elec_acct_config.elec_card_list[].branch_name` | 支行名称 | `String` | `64` | `Y` | 示例值：中国工商银行上海市中山北路支行 |
| `request.data.elec_acct_config.elec_card_list[].card_name` | 结算账户名 | `String` | `128` | `Y` | 银行卡对应的户名；示例值：上海汇付支付有限公司 |
| `request.data.elec_acct_config.elec_card_list[].card_no` | 银行卡号 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.elec_acct_config.elec_card_list[].card_type` | 卡类型 | `String` | `1` | `Y` | 0:对公 1:对私法人；示例值：0 |
| `request.data.elec_acct_config.elec_card_list[].default_cash_flag` | 默认卡标识 | `String` | `1` | `N` | 0：非默认卡 1：默认卡(不填，默认为0) |
| `request.data.elec_acct_config.elec_card_list[].mp` | 银行绑定手机号 | `String` | `11` | `C` | 个人必填 |
| `request.data.elec_acct_config.elec_card_list[].auth_version` | 用户授权协议版本号 | `String` | `64` | `C` | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的电子协议版本号，通过该版本号能够确定协议的具体内容 |
| `request.data.elec_acct_config.elec_card_list[].auth_no` | 用户授权协议号 | `String` | `64` | `C` | 该字段在绑定个人账户时必填，取值商户自定义。与个人用户签约的授权交易流水号，通过该流水号应能确定电子协议版本号、签约人、签约时间 |
| `request.data.elec_acct_config.elec_acct_sign_seq_id` | 中信签约短信流水号 | `String` | `64` | `N` | 示例值：EMSSBPG[官网示例已脱敏] |
| `request.data.elec_acct_config.sign_success_flag` | 签约成功标志 | `String` | `1` | `N` | Y：成功 |
| `request.data.share_holder_info_list[]` | 股东信息 | `String` | `—` | `N` | jsonArray字符串；全域资金业务新网银行必填 |
| `request.data.share_holder_info_list[].share_holder_id` | 股东编号 | `String` | `32` | `N` | 修改时必填；示例值： |
| `request.data.share_holder_info_list[].name` | 股东姓名 | `String` | `32` | `Y` | 示例值：张三 |
| `request.data.share_holder_info_list[].cert_type` | 股东证件类型 | `String` | `2` | `Y` | 参考《[自然人证件类型](https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b)》；支持00~11，以及12:营业执照；示例值：12 |
| `request.data.share_holder_info_list[].cert_no` | 股东证件号码 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.share_holder_info_list[].cert_validity_type` | 股东证件有效期类型 | `String` | `1` | `Y` | 1:长期有效 0:非长期有效；示例值：1 |
| `request.data.share_holder_info_list[].cert_begin_date` | 股东证件有效期起始日 | `String` | `8` | `Y` | 格式yyyyMMdd；示例值：20201223 |
| `request.data.share_holder_info_list[].cert_end_date` | 股东证件有效期到期日 | `String` | `8` | `N` | 格式yyyyMMdd; 非长期有效时必填；示例值：20301223 |
| `request.data.share_holder_info_list[].state` | 股东状态 | `String` | `1` | `N` | 1:有效 0:无效；示例值：1 |
| `request.data.share_holder_info_list[].mobile_no` | 股东手机号 | `String` | `11` | `N` | 示例值：[官网示例已脱敏] |
| `request.data.ext_mer_id` | 外部商户号 | `String` | `64` | `N` | 支持关联外部商户系统中的商户号；示例值：HF100001 |
| `request.data.remark` | 备注 | `String` | `300` | `N` | 备注内容；示例值：华东分公司 |
| `request.data.activated_products` | 产品大类 | `String` | `32` | `N` | 01：一体化收款产品，02：账户与资金产品，03：业财数通产品；不传为空 示例值：01,02,03 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务返回码 | `String` | `8` | `Y` | 参考[业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码)；示例值：00000000 |
| `response.data.resp_desc` | 业务返回描述 | `String` | `512` | `Y` | 示例值：处理成功 |
| `response.data.huifu_id` | 商户号 | `String` | `18` | `N` | 汇付商户号，状态为审核中时返回；示例值：[官网示例已脱敏] |
| `response.data.apply_no` | 申请单号 | `String` | `18` | `N` | 商户开户业务申请单号，状态为审核中时返回；示例值：[官网示例已脱敏] |
| `response.data.token_no` | 取现卡序列号 | `String` | `20` | `N` | 取现时使用；示例值：10004053462 |

### 审核异步 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.audit.data.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | 参考业务返回码；示例值：00000000 |
| `async.audit.data.sub_resp_desc` | 业务返回描述 | `String` | `512` | `N` | 业务返回描述；示例值：处理成功 |
| `async.audit.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原请求流水号；示例值：[官网示例已脱敏] |
| `async.audit.data.req_date` | 请求日期 | `String` | `8` | `Y` | 原请求日期 示例值：20220125 |
| `async.audit.data.audit_status` | 审核结果 | `String` | `1` | `Y` | 审核结果；Y：审核通过；N：审核拒绝 ；F：失败；示例值：Y |
| `async.audit.data.audit_desc` | 审核描述 | `String` | `512` | `N` | 审核描述，审核人员编辑的审核描述；示例值：审核通过 |
| `async.audit.data.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号；示例值：MCS |
| `async.audit.data.huifu_id` | 商户号 | `String` | `18` | `N` | 返回：处理成功时有值，汇付分配的商户号 |
| `async.audit.data.apply_no` | 申请单号 | `String` | `18` | `N` | 商户开户业务申请单号，状态为审核中时返回； 示例值：[官网示例已脱敏] |
| `async.audit.data.token_no` | 取现卡序列号 | `String` | `20` | `N` | 取现时使用；示例值：10004053462 |
| `async.audit.data.notify_type` | 通知类型 | `String` | `1` | `N` | Z：电子账户；示例值：Z |
| `async.audit.data.elec_acct_result` | 斗拱e账户开通结果 | `String` | `—` | `N` | jsonObject格式；notify_type=Z时返回 |
| `async.audit.data.elec_acct_result.acct_type` | 账户类型 | `String` | `2` | `Y` | 01：中信e管家；示例值：01 |
| `async.audit.data.elec_acct_result.bank_status` | 电子账户开通状态 | `String` | `1` | `Y` | S：成功 F：失败；示例值：S |
| `async.audit.data.elec_acct_result.bank_message` | 银行信息 | `String` | `512` | `N` | 银行信息 |
| `async.audit.data.elec_acct_result.sign_agreement_id` | 签约协议号 | `String` | `32` | `N` | 商户签约中信E管家协议编号； 签约成功才返回示例值：[官网示例已脱敏] |

### 电子协议异步

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `async.agreement.sub_resp_code` | 业务返回码 | `String` | `8` | `Y` | 参考业务返回码；示例值：00000000 |
| `async.agreement.sub_resp_desc` | 业务返回描述 | `String` | `512` | `N` | 业务返回描述；示例值：处理成功 |
| `async.agreement.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原请求流水号；示例值：[官网示例已脱敏] |
| `async.agreement.req_date` | 请求日期 | `String` | `8` | `Y` | 原请求日期 示例值：20220125 |
| `async.agreement.huifu_id` | 商户号 | `String` | `18` | `Y` | 汇付分配的商户号 |
| `async.agreement.apply_no` | 申请单号 | `String` | `18` | `Y` | 商户开户业务申请单号，状态为审核中时返回； 示例值：[官网示例已脱敏] |
| `async.agreement.agreement_info_list` | 电子协议信息 | `String` | `—` | `N` | 电子协议信息，签署电子协议时返回 |
| `async.agreement.agreement_info_list.agreement_type` | _协议类型_ | `String` | `1` | `N` | 0-电子协议 |
| `async.agreement.agreement_info_list.agreement_link` | 协议签署链 | `String` | `512` | `N` | 协议签署链 |
| `async.agreement.agreement_info_list.agreement_no` | 协议号 | `String` | `32` | `N` | 示例值：3245234 |
| `async.agreement.agreement_info_list.agreement_name` | 协议名称 | `String` | `128` | `N` | 协议名称 |
| `async.agreement.agreement_info_list.con_stat` | 签约状态 | `String` | `2` | `N` | 电子协议类型会返回以下值： 2：创建合同异常 3：待签约 4：签约中 5：签约完成(电子协议只有签约完成才能做交易) 6：已失效 7：已拒签 8：签约失败 示例值：5 |

## 商户费率信息查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_merchant_conf_search_cx.md>
- SHA-256：`20a3be9f505c542a716bbdad65da146f9089be05b206850c089c6df4e9ac050e`
- 说明：下表保留官方字段类型、长度、必填标记和字段说明；数组父路径以 `[]` 标记。

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
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号 |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd，以北京时间为准 |
| `request.data.huifu_id` | 汇付商户号 | `String` | `18` | `Y` | 汇付分配的商户号，示例值：[官网示例已脱敏] |
| `request.data.fee_rate_type[]` | 费率类型（支持多选） | `Array<string>` | `117` | `N` | 数组； ALI_FEE_RATE：支付宝支付费率信息；WX_FEE_RATE：微信支付费率信息；BANK_CARD_FEE_RATE：银行卡支付费率信息；UNION_FEE_RATE：银联二维码支付费率信息；不传则返回全部费率; 示例值：["ALI_FEE_RATE","WX_FEE_RATE","UNION_FEE_RATE"] |

### 响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务返回码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务返回描述 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.product_id` | 产品号 | `String` | `32` | `Y` | 同入参 |
| `response.data.huifu_id` | 汇付商户号 | `String` | `18` | `Y` | 同入参 |
| `response.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 同入参 |
| `response.data.req_date` | 请求日期 | `String` | `8` | `Y` | 同入参 |
| `response.data.wx_fee_rate_list[]` | 微信支付费率信息 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.wx_fee_rate_list[].fee_rate` | 手续费（%） | `String` | `9` | `Y` | 数字类型，大于等于0,保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.wx_fee_rate_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `6` | `N` | 固定金额保留2位小数；大于0。需要渠道商开通此功能。示例值：0.38 |
| `response.data.wx_fee_rate_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 参见《[微信支付场景](https://paas.huifu.com/partners/api/doc/api_ggcsbm.md#微信支付场景)（官网相对地址原文：`api_ggcsbm.md#微信支付场景`）》说明；示例值：1 |
| `response.data.wx_fee_rate_list[].pay_type` | 支付类型 | `String` | `3` | `Y` | C03-微信线下反扫支付；C04-微信线下公众号支付；C05-微信线下小程序支付；C06-微信线上公众号支付；C07-微信线上小程序支付；C14-微信非盈利费率交易；C15-微信缴费费率交易；C16-微信保险费率交易；C17-微信行业活动费率交易；C18-微信校园餐饮费率交易；C19-微信中小幼费率交易；C20-微信线下教培费率交易；C23-微信线上反扫支付；C30-微信APP支付 |
| `response.data.ali_fee_rate_list[]` | 支付宝支付费率信息 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.ali_fee_rate_list[].fee_rate` | 手续费（%） | `String` | `9` | `N` | 示例值：0.60 |
| `response.data.ali_fee_rate_list[].fee_min_amt` | 最低收取手续费（元） | `String` | `6` | `N` | 固定金额保留2位小数；大于0。需要渠道商开通此功能。示例值：0.38 |
| `response.data.ali_fee_rate_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 1、线下扫码，2、线上扫码，3、非盈利费率；示例值：1 |
| `response.data.ali_fee_rate_list[].pay_type` | 支付类型 | `String` | `3` | `Y` | D02-线下支付宝正扫支付；D03-线下支付宝反扫支付；D04-线下支付宝JS支付；D22-线上支付宝正扫支付；D23-线上支付宝反扫支付；D24-线上支付宝JS支付；D07-支付宝非盈利费率交易；D08-支付宝缴费费率交易；D09-支付宝行业活动费率交易；D21-支付宝校园餐饮费率交易 |
| `response.data.bank_card_fee_rate_list[]` | 银行卡支付费率信息 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.bank_card_fee_rate_list[].debit_fee_rate` | 借记卡手续费（%） | `String` | `9` | `Y` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]； 示例值：0.60 |
| `response.data.bank_card_fee_rate_list[].debit_fee_limit` | 借记卡封顶值 | `String` | `4` | `N` | 数字类型，大于0保留2位小数； 示例值：2.00 |
| `response.data.bank_card_fee_rate_list[].credit_fee_rate` | 贷记卡手续费（%） | `String` | `9` | `Y` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.90 |
| `response.data.bank_card_fee_rate_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 1、银行卡支付 |
| `response.data.union_fee_rate_list[]` | 银联二维码支付费率信息 | `String` | `—` | `N` | jsonArray格式 |
| `response.data.union_fee_rate_list[].fee_rate_up` | 银联二维码业务手续费1000(包含1000)以上（%） | `String` | `9` | `Y` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00];示例值：0.60 |
| `response.data.union_fee_rate_list[].fee_rate_down` | 银联二维码业务手续费1000(包含1000)以下（%） | `String` | `9` | `N` | 数字类型，大于0保留2位小数；取值范围（0.00,100.00]；示例值：0.60 |
| `response.data.union_fee_rate_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 1、线下银联二维码 2、线上银联二维码 |

## 商户状态变更

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/api_shgl_shztbg.md>
- SHA-256：`d2fe6ab4404abd79b3ac5f5eecffaaec9d61d245ac1a60ebccddee889535a07f`
- 说明：下表保留官方字段类型、长度、必填标记和字段说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id；示例值：[官网示例已脱敏] |
| `request.product_id` | 产品号 | `String` | `32` | `Y` | 汇付分配的产品号，示例值：YYZY |
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
| `request.data.req_date` | 请求日期 | `string` | `8` | `Y` | 请求时间 yyyyMMdd；示例值：20220921 |
| `request.data.req_seq_id` | 请求流水号 | `string` | `32` | `Y` | 请求流水号；示例值：[官网示例已脱敏] |
| `request.data.huifu_id` | 汇付客户Id | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID；示例值：[官网示例已脱敏] |
| `request.data.status` | 状态 | `String` | `1` | `Y` | 1:开通 0:关闭；示例值：1；注：支持关闭后再次打开 |
| `request.data.upd_status_reason` | 状态变更原因 | `String` | `512` | `Y` | 示例值：注销 |

### 同步响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 返回码 | `String` | `8` | `Y` | [返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%E5%95%86%E6%88%B7%E8%BF%9B%E4%BB%B6%E8%BF%94%E5%9B%9E%E7%A0%81) |
| `response.data.resp_desc` | 返回描述 | `String` | `512` | `Y` | [返回码描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%E5%95%86%E6%88%B7%E8%BF%9B%E4%BB%B6%E8%BF%94%E5%9B%9E%E7%A0%81) |
| `response.data.apply_no` | 申请单号 | `String` | `128` | `N` | 示例值：[官网示例已脱敏] |

## 商户短信发送

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shdxfs.md>
- SHA-256：`6982fe07d276cbb0739c9c205afbc5b238dd6d72422154efd6248932aa459b54`
- 说明：下表保留官方字段类型、长度、必填标记和字段说明；数组父路径以 `[]` 标记。

### 请求信封

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.sys_id` | 系统号 | `String` | `32` | `Y` | 渠道商/商户的huifu_id ；（1）当主体为渠道商时，此字段填写渠道商huifu_id；（2）当主体为直连商户时，此字段填写商户huifu_id |
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
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 示例值：[官网示例已脱敏] |
| `request.data.req_date` | 请求时间 | `String` | `8` | `Y` | 请求时间格式yyyyMMdd；示例值：20220903 |
| `request.data.huifu_id` | 商户汇付Id | `String` | `18` | `Y` | 斗拱分配的商户号；示例值：[官网示例已脱敏] |
| `request.data.phone` | 手机号 | `String` | `11` | `C` | verify_type='elecAcctSign'时，手机号为空，系统自动取联系人手机号; 示例值：[官网示例已脱敏] |
| `request.data.verify_type` | 验证类型 | `String` | `32` | `Y` | 枚举：结算卡变更-settleBankChange；中信E管家签约-elecAcctSign; 示例值：settleBankChange |
| `request.data.operation_type` | 操作类型 | `String` | `32` | `C` | verify_type='elecAcctSign'时必填；枚举值：sendSmsCode-发送验证码；identitySmsCode-验证码核实；示例值：sendSmsCode |
| `request.data.verify_code` | 验证码 | `String` | `6` | `C` | verify_type='elecAcctSign'且operation_type='identitySmsCode'时必填；示例值：123456 |
| `request.data.elec_acct_sign_seq_id` | 中信签约流水号 | `String` | `64` | `C` | verify_type='elecAcctSign'且operation_type='identitySmsCode'时必填；值为中信E管家签约发送短信时返回值；示例值：EMSSBPG[官网示例已脱敏] |

### 响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务响应码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| `response.data.resp_desc` | 业务响应信息 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码) |
| `response.data.verify_type` | 验证类型 | `String` | `32` | `N` | 枚举：结算卡变更-settleBankChange；中信E管家签约-elecAcctSign; 示例值：settleBankChange |
| `response.data.operation_type` | 操作类型 | `String` | `32` | `N` | 枚举值：sendSmsCode-发送验证码；identitySmsCode-验证码核实；示例值：sendSmsCode |
| `response.data.elec_acct_sign_seq_id` | 中信签约短信流水号 | `String` | `64` | `N` | verify_type='elecAcctSign'且operation_type='sendSmsCode'时；中信E管家签约发送短信时返回值；示例值：EMSSBPG[官网示例已脱敏] |
| `response.data.phone` | 手机号 | `String` | `11` | `N` | 手机号；示例值：[官网示例已脱敏] |

## 商户多费率配置

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflpz.md>
- SHA-256：`e4b23cb9bfaf59e9a88448a890f539d7ee9cbf7002d763a7d078294053aa7473`
- 说明：下表保留官方字段类型、长度、必填标记和字段说明；数组父路径以 `[]` 标记。

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
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号，同一商户号当天唯一 |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd，以北京时间为准 |
| `request.data.huifu_id` | 汇付商户号 | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID |
| `request.data.wx_conf_list[]` | 微信配置对象列表 | `String` | `—` | `N` | jsonArray格式，微信配置对象列表、支付宝配置对象列表不可同时为空 |
| `request.data.wx_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 1：线下反扫； 2：线下公众号； 3：线下小程序； 4：线上公众号； 5：线上小程序； 12：线上反扫； 示例值：1 |
| `request.data.wx_conf_list[].fee_rate` | 手续费底价（%） | `String` | `6` | `Y` | 数字类型，大于等于0,保留2位小数；示例值：0.38 |
| `request.data.wx_conf_list[].fee_sign` | 手续费场景标识 | `String` | `32` | `N` | 支付功能+场景维度生成的费率唯一标识，传入时支持修改 示例值：155677 |
| `request.data.ali_conf_list[]` | 支付宝配置对象列表 | `String` | `—` | `N` | jsonArray格式，微信配置对象列表、支付宝配置对象列表不可同时为空 |
| `request.data.ali_conf_list[].pay_scene` | 支付场景 | `String` | `2` | `Y` | 1：线下扫码； 2：线上扫码； 示例值：1 |
| `request.data.ali_conf_list[].fee_rate` | 手续费底价（%） | `String` | `6` | `Y` | 数字类型，大于等于0,保留2位小数；示例值：0.38 |
| `request.data.ali_conf_list[].fee_sign` | 手续费场景标识 | `String` | `32` | `N` | 支付功能+场景维度生成的费率唯一标识，传入时支持修改 示例值：155677 |

### 响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务响应码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务响应信息 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 原样返回请求参数的请求流水号；示例值：[官网示例已脱敏] |
| `response.data.req_date` | 请求日期 | `String` | `8` | `Y` | 原请求时间yyyyMMdd；示例值：20220912 |
| `response.data.conf_status` | 配置状态 | `String` | `1` | `Y` | Y：成功 F：失败 |
| `response.data.conf_list[]` | 配置信息 | `String` | `—` | `N` | jsonArray格式，配置成功时返回 |
| `response.data.conf_list[].pay_scene` | 支付场景 | `String` | `2` | `N` | 支付功能为W：微信时返回 1：线下反扫； 2：线下公众号； 3：线下小程序； 4：线上公众号； 5：线上小程序； 12：线上反扫； 支付功能为A：支付宝时返回 1：线下扫码； 2：线上扫码； 示例值：1 |
| `response.data.conf_list[].fee_rate` | 手续费底价（%） | `String` | `6` | `N` | 数字类型，大于等于0,保留2位小数；示例值：0.38 |
| `response.data.conf_list[].fee_sign` | 手续费场景标识 | `String` | `32` | `N` | 支付功能+场景维度生成的费率唯一标识，交易时支持传入 示例值：155677 |
| `response.data.conf_list[].pay_way` | 支付功能 | `String` | `1` | `N` | A：支付宝 W：微信 示例值：A |

## 商户多费率配置查询

- 原始地址：<https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflcx.md>
- SHA-256：`e2c0f53e77a1ef00827cc8be28ac688c068e5c8a4dc9f741845b841dcd16881a`
- 说明：下表保留官方字段类型、长度、必填标记和字段说明；数组父路径以 `[]` 标记。

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
| `response.sign` | 签名 | `String` | `512` | `Y` | [接口加签验签说明](https://paas.huifu.com/open/doc/guide/#/api_v2jqyq) |
| `response.data` | 响应内容体 | `Json` | `—` | `N` | 业务返回参数 |

### 请求 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `request.data.req_seq_id` | 请求流水号 | `String` | `32` | `Y` | 请求流水号，同一商户号当天唯一 |
| `request.data.req_date` | 请求日期 | `String` | `8` | `Y` | 日期格式：yyyyMMdd，以北京时间为准 |
| `request.data.huifu_id` | 汇付商户号 | `String` | `18` | `Y` | 渠道与一级代理商的直属商户ID |
| `request.data.fee_sign` | 手续费场景标识 | `String` | `32` | `N` | 支付功能+场景维度生成的费率唯一标识，交易时支持传入 示例值：155677 |

### 响应 data

| 完整字段路径 | 中文名 | 类型 | 长度 | 必填 | 官方说明 |
| --- | --- | --- | ---: | :---: | --- |
| `response.data.resp_code` | 业务响应码 | `String` | `8` | `Y` | [业务返回码](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.resp_desc` | 业务响应信息 | `String` | `512` | `Y` | [业务返回描述](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm) |
| `response.data.conf_list[]` | 配置信息 | `String` | `—` | `N` | jsonArray格式，配置成功时返回 |
| `response.data.conf_list[].pay_scene` | 支付场景 | `String` | `2` | `N` | 支付功能为W：微信时返回 1：线下反扫； 2：线下公众号； 3：线下小程序； 4：线上公众号； 5：线上小程序； 12：线上反扫； 支付功能为A：支付宝时返回 1：线下扫码； 2：线上扫码； 示例值：1 |
| `response.data.conf_list[].fee_rate` | 手续费底价（%） | `String` | `6` | `N` | 数字类型，大于等于0,保留2位小数；示例值：0.38 |
| `response.data.conf_list[].fee_sign` | 手续费场景标识 | `String` | `32` | `N` | 支付功能+场景维度生成的费率唯一标识，交易时支持传入 示例值：155677 |
| `response.data.conf_list[].pay_way` | 支付功能 | `String` | `1` | `N` | A：支付宝 W：微信 示例值：A |
