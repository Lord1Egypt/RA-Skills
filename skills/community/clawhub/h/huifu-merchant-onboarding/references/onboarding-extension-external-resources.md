# 进件扩展接口外部资料索引

本页登记十二个进件扩展接口字段说明中出现的公共规范、编码表、前置接口和第三方渠道资料。字段类型、长度、必填性和完整路径仍以 `onboarding-extension-complete-field-catalog.md` 为准；冲突处理读取 `onboarding-extension-field-contracts.md`。

## 输出规则

1. 仅在用户问题命中对应字段时输出资料，必须同时给出完整字段路径、用途和原始地址。
2. SPA 地址的 `#` 片段属于官方原文；基础页面可访问不等于片段内容已形成稳定下载合同，不得根据标题补枚举。
3. 原文为 `http://` 时保留原址并提示非 HTTPS，不静默改写；第三方微信资料不是汇付字段合同，不能覆盖汇付参数表。
4. 合同链接、二维码、回调地址和示例图片 URL 是运行时值或示例，不作为外部资料、默认值或推荐地址。

## 公共规范

| 完整字段路径 | 用途 | 原始地址 |
| --- | --- | --- |
| 十二接口正式声明的 `request.sign/response.sign` | 接口加签验签说明；微信配置本轮不再声明同步/异步外层，不能据此补回 `async.sign` | `https://paas.huifu.com/open/doc/guide/#/api_v2jqyq` |
| 各响应或异步的 `resp_code/resp_desc/sub_resp_code/sub_resp_desc` | 业务返回码或网关返回码 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm` |
| 统一页面进件 `async.resp_code` | 网关返回码锚点 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#%E7%BD%91%E5%85%B3%E8%BF%94%E5%9B%9E%E7%A0%81` |
| 统一页面进件 `async.audit.data.sub_resp_code`、`async.business.data.sub_resp_code` | 商户进件返回码锚点 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#%E5%95%86%E6%88%B7%E8%BF%9B%E4%BB%B6%E8%BF%94%E5%9B%9E%E7%A0%81` |
| 微信配置 `response.data.resp_code` | 商户进件返回码锚点；保留当前原文未编码中文地址。异步为 `async.data.sub_resp_code`，引用上方通用业务返回码入口，不能生成 `async.data.resp_code` | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码` |

返回码公共 Markdown `https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md` 可用于读取公共全集，但不能替换接口页对字段长度、方向和必填性的定义。

## 页面进件与微信配置

| 完整字段路径 | 用途 | 原始地址 |
| --- | --- | --- |
| `request.data.head_office_flag`（统一页面进件） | 开通下级商户权限配置前置能力 | `https://paas.huifu.com/open/doc/api/#/shgl/shywkt/api_shjj_shywkt_xjshpz` |
| 统一页面查询的接口前置说明 | 商户统一进件（页面版）接口 | `https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtyjjweb` |
| `async.business.data.reg_result_list[].pay_scene`（统一页面进件） | 微信支付场景 | `https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e6%94%af%e4%bb%98%e5%9c%ba%e6%99%af` |
| `response.data.wx_real_name_list[].pay_scene`（统一页面查询） | 官网链接文字写“微信业务开通类型”，目标却是微信支付场景；保持原文并标记 `[需要官方确认]` | `https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e6%94%af%e4%bb%98%e5%9c%ba%e6%99%af` |
| `request.data.fee_type`（微信配置）；`response.data.atu_config_bo_list[].fee_type`、`response.data.atu_config_bo_fail_list[].fee_type`（微信配置查询） | 微信业务开通类型 | `https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e4%b8%9a%e5%8a%a1%e5%bc%80%e9%80%9a%e7%b1%bb%e5%9e%8b` |
| `request.data.bank_channel_no`（微信配置和查询） | 支付渠道号说明 | `https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo` |

## 微信实名认证

| 完整字段路径 | 用途 | 原始地址 |
| --- | --- | --- |
| `request.data.pay_channel_id`（申请和查询） | 支付渠道号说明 | `https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo` |
| `request.data.pay_scene`（申请和查询） | 微信业务开通类型；官网原文为 HTTP | `http://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e4%b8%9a%e5%8a%a1%e5%bc%80%e9%80%9a%e7%b1%bb%e5%9e%8b` |
| `request.data.contact_id_doc_type` | 自然人证件类型 | `https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b` |
| `request.data.store_address_code` | 省市区编码 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm` |
| `request.data.finance_institution_flag`、`request.data.finance_type` | 微信金融机构接入指引（腾讯第三方资料） | `https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html` |
| `request.data.category_id` | 微信特殊行业 ID 对照表（微信支付第三方资料） | `https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/applysubject_new/chapter6_1.shtml` |
| 微信实名申请页的前置说明 | 商户图片上传 | `https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc` |
| `request.data.contact_type` 的官方示例图 | 超级管理员类型示例（腾讯第三方资料） | `https://kf.qq.com/faq/220509Y3Yvym220509fQvYR7.html` |
| `response.data.applyment_stat`（实名查询） | 同一官方页下方的申请单状态说明 | `https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_wxsmrzztcx.md#微信实名认证申请单状态` |

## 支付宝实名认证

| 完整字段路径 | 用途 | 原始地址 |
| --- | --- | --- |
| 支付宝实名查询的接口前置说明 | 支付宝实名认证申请接口 | `https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_zfbsmrz` |
| `request.data.pay_channel_id`（申请和查询） | 支付渠道号说明 | `https://paas.huifu.com/open/doc/api/#/czsm/api_czsm_bankChannelNo` |
| `request.data.auth_identity_info.support_credentials.province_code/city_code/district_code` | 地区码 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm` |
| `request.data.auth_identity_info.qualification_info_list[].mcc_code` | 支付宝商家行业二级类目编码 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_zfbmcc` |
| `request.data.legal_person_info.card_front_img/card_back_img` | 商户图片上传；页面开头另有 HTTP 版本链接，字段行使用 HTTPS | `http://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc`、`https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc` |

## 访问复核

`2026-09-15` 复查时，汇付开发指南/API 基础页、公共返回码 Markdown、微信实名状态原页、两份腾讯指引和微信支付特殊行业页面均返回 HTTP 200；微信支付旧地址会跳转至当前文档页。该结果只证明当时可访问，不冻结第三方正文，也不授权把第三方规则复制成汇付字段枚举。后续访问失败时保留原始地址并标记 `[需要人工访问/确认]`。
