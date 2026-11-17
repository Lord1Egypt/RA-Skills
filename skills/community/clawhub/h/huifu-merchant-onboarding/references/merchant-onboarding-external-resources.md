# 商户进件字段外部资料索引

本页只处理十三个商户进件接口字段说明中出现的外部文档、编码表、下载文件和固定协议地址。字段的类型、长度、必填性、枚举、默认值和条件仍以 `merchant-onboarding-field-contracts.md` 为准。

## 目录

- [强制输出合同](#强制输出合同)
- [十三个接口原始来源](#十三个接口原始来源)
- [公共资料映射](#公共资料映射)
- [商户业务开通专项资料](#商户业务开通专项资料)
- [详情与申请状态专项资料](#详情与申请状态专项资料)
- [不得误报为外部资料的 URL](#不得误报为外部资料的-url)
- [交付前自检](#交付前自检)

## 强制输出合同

当回答涉及的字段说明命中本页任一资料时，答案必须单列 `外部资料提示`，不得只写“参考官网”“查看附件”或只给资料名。每条至少包含：

1. 完整字段路径；
2. 资料名称和类型（官方文档、编码表、HTML 协议、XLSX 文件或第三方渠道指引）；
3. 触发条件或用途；
4. **未经改写、未经缩短的原始地址**；绝对地址同时以可点击链接和可复制的明文 URL 展示。官网只给相对地址或 `#锚点` 时，必须分别写出“官网相对地址原文”和“按已登记官方文档命名空间（无例外时按来源页）解析后的绝对地址”，不得把解析结果冒充原文；
5. 当前读取状态：本地只保存地址和字段触发关系时，必须写“未读取外部文件内容，请按原始地址人工核验”，不得声称已经核对 XLSX/外站正文。

同一地址被多个相关字段命中时可以去重一次，但必须把全部相关字段路径列全。每条资料都要重复写出完整路径，禁止用“同字段”“同上”“该字段”代替路径。原文为 `http://` 时保留原始 `http://`，可另外提示其不是 HTTPS，但不得静默改写成 `https://`。原始地址失效或无法打开时仍要原样给出，并标记 `[需要人工访问/确认]`；不得猜测最新地址或换成网站首页。完整字段目录会把字段说明中的相对地址按已登记官方文档命名空间（无例外时按来源页）解析为可点击绝对地址，并在同一说明中保留“官网相对地址原文”；这只修复合并文档中的跳转上下文，不改变官方合同。

交付前将每条链接目标及明文URL与索引逐字符比对，特别检查百分号编码、大小写、文件名末尾和扩展名；不要凭记忆重打或截短长XLSX地址。链接名称可以简写，目标地址必须完整。

推荐输出格式：

```markdown
### 外部资料提示

- 字段：`request.data.extended_material_list[]`
  - 资料：代扣支付补充材料（XLSX）
  - 触发：申请代扣能力时
  - 可点击链接：使用 Markdown 链接，链接目标填写完整原始 URL
  - 明文地址：`完整原始URL`
  - 状态：未读取外部文件内容，请按原始地址人工核验。
```

固定协议地址是字段值约束，不只是阅读资料。命中 `request.data.agreement_info.agreement_type=3` 时，必须把完整路径 `request.data.agreement_info.agreement_url` 和本页的 `PaymentServiceAgreement.htm` 原始地址同时写入参数建议和 `外部资料提示`；不得把路径缩短成 `data.agreement_info.agreement_url` 或 `agreement_url`，也不得替换成任意商户网页。

## 十三个接口原始来源

这些地址用于说明映射来源。它们不代替下面字段级资料地址。

| 接口 | 原始来源 |
| --- | --- |
| 企业商户进件 | `https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md` |
| 个人商户进件 | `https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_grshjbxxrz_kyc.md` |
| 商户业务开通 | `https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_kyc.md` |
| 图片上传 | `https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json` |
| 商户详细信息查询 | `https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md` |
| 申请单状态查询 | `https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_sqdztcx.md` |
| 商户业务开通修改 | `https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md` |
| 商户基本信息修改 | `https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shjbxxxg_kyc.md` |
| 商户费率信息查询 | `https://paas.huifu.com/partners/api/doc/shgl/shjj/api_merchant_conf_search_cx.md` |
| 商户状态变更 | `https://paas.huifu.com/partners/api/doc/shgl/api_shgl_shztbg.md` |
| 商户短信发送 | `https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shdxfs.md` |
| 商户多费率配置 | `https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflpz.md` |
| 商户多费率配置查询 | `https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflcx.md` |

## 公共资料映射

下表为了压缩索引，部分请求路径以 `data.*` 简写；生成答案时必须机械展开为 `request.data.*`。响应路径必须保留 `response.data.*`，异步路径必须保留具体 `async.*` 数据面。路径中的 `/` 表示同一资料适用的多个叶子字段，`[]` 表示数组元素。只输出与用户本次问题、生成参数或评审字段有关的资料，不要把整张表无差别倾倒给用户，也不得把简写直接交付给用户。

| 命中接口与字段路径 | 资料 / 用途 | 原始地址 |
| --- | --- | --- |
| 其余九个Markdown接口顶层 `sign`（不含图片上传；三份捷行付变更页见下一行） | 接口加签验签说明 | `https://paas.huifu.com/open/doc/guide/#/api_v2jqyq` |
| 业务开通、开通修改、详情查询的请求/响应 `sign`（六处链接） | 接口加签验签说明（2026-11-03更新） | `https://paas.huifu.com/docs/start/#/api_v2jqyq` |
| 企业 `data.mcc`；个人 `data.mcc` | 汇付 MCC 编码 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm` |
| 企业 `data.license_pic/legal_cert_back_pic/legal_cert_front_pic/reg_acct_pic/settle_card_front_pic/settle_cert_back_pic/settle_cert_front_pic/auth_entrust_pic/store_header_pic/store_indoor_pic/store_cashier_desk_pic/extended_material_list[].file_id`；个人的图片材料与 `extended_material_list[].file_id`；业务开通 `data.online_media_info_list[].media_front_page/media_service_page/media_order_page/media_pay_page/other_material`、`data.extended_material_list[].file_id`；详情响应图片材料；图片上传前置 | 商户图片上传接口 | `https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc` |
| 企业 `data.license_type`；详情响应 `data.license_type` | 机构证照类型 | `https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E6%9C%BA%E6%9E%84%E8%AF%81%E7%85%A7%E7%B1%BB%E5%9E%8B` |
| 企业/个人经营和银行省市区字段；业务开通银行省市区字段；详情响应注册、经营和银行省市区字段 | 地区码 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm` |
| 企业 `request.data.material_card_info.prov_id/area_id` | 对私结算时补充对公同名账户的地区码；不得与经营省市或 `card_info` 省市合并 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm` |
| 企业 `data.legal_cert_type/beneficiary_info[].bo_type/card_info.cert_type/share_holder_info_list[].cert_type`；个人 `data.card_info.cert_type`；详情响应法人、持卡人和股东证件类型 | 自然人证件类型 | `https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b` |
| 企业/个人 `data.head_office_flag` | 开通下级商户权限配置接口 | `https://paas.huifu.com/open/doc/api/#/shgl/shywkt/api_shjj_shywkt_xjshpz` |
| 企业/个人 `data.card_info.branch_code`、电子账户银行卡 `branch_code`；业务开通和详情响应的支行字段 | 银行支行编码 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm` |
| 企业 `request.data.material_card_info.branch_code` | 对私结算时补充对公同名账户的支行联行号 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhzhbm` |
| 个人 `data.card_info.bank_code`、电子账户银行卡 `bank_code`；业务开通 `bank_id/bank_code`；详情响应银行编码 | 银行编码 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm` |
| 企业/个人 `data.settle_config.settle_abstract` | 结算配置示例说明 | `https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm` |
| 企业/个人 `data.settle_config.settle_batch_no`；详情响应结算批次 | 结算批次说明 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc` |
| 企业/个人 `data.elec_acct_config.scene/role_type`；详情响应电子账户场景/角色 | 中信 E 管家资金类型和角色类型 | `https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx` |
| 企业/个人 `data.elec_acct_config.elec_card_list` | 电子账户绑卡接口 | `https://paas.huifu.com/open/doc/api/#/yuer/api_acct_dzzhbk` |
| 企业/个人/业务开通 `data.extended_material_list[].file_type`；图片上传 `data.file_type` | 文件类型说明 / 枚举取值表 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx` |
| 同步或异步响应 `resp_code/resp_desc/sub_resp_code/sub_resp_desc` | 业务返回码和网关返回码 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm` |
| 同步或异步响应 `resp_code/resp_desc/sub_resp_code/sub_resp_desc` | 返回码规范 Markdown（用于读取公共全集；不替换字段说明中的旧 SPA 原文） | `https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md` |
| 公共编码或术语核验 | 基础参数汇总 / 名词解释；只作公共字典入口，不覆盖具体接口字段合同 | `https://paas.huifu.com/partners/api/doc/csfl/api_csfl.md`、`https://paas.huifu.com/partners/api/doc/csfl/api_csfl_mcjs.md` |
| 商户状态变更响应 `response.data.resp_code/resp_desc` | 商户进件返回码 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%E5%95%86%E6%88%B7%E8%BF%9B%E4%BB%B6%E8%BF%94%E5%9B%9E%E7%A0%81` |
| 基本信息修改 `request.data.card_info.auth_entrust_pic` | 授权结算委托书模板（DOCX） | `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/12%E3%80%90%E5%95%86%E6%88%B7%E3%80%91%E6%8E%88%E6%9D%83%E7%BB%93%E7%AE%97%E5%A7%94%E6%89%98%E4%B9%A6%EF%BC%88%E5%AF%B9%E7%A7%81%E7%BB%93%E7%AE%97%EF%BC%89%EF%BC%88%E7%BA%B8%E8%B4%A8%E5%90%88%E5%90%8C%E7%89%88%EF%BC%89.docx` |
| 基本信息修改收款人变更相关字段 | 收款人变更说明页 | `https://paas.huifu.com/open/doc/api/#/shgl/shjj/changeofpayee` |
| 业务开通修改 `request.data.extended_material_list`；分账能力修改 | 分账功能提供材料（XLSX） | `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%88%86%E8%B4%A6%E5%8A%9F%E8%83%BD%E6%8F%90%E4%BE%9B%E6%9D%90%E6%96%99.xlsx` |

返回码文档在官网字段中还出现了带锚点的原始写法。若用户明确询问商户进件返回码或网关返回码，优先原样输出对应地址：

- 商户进件返回码：`https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#商户进件返回码`
- 网关返回码：`https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm?id=%e7%bd%91%e5%85%b3%e8%bf%94%e5%9b%9e%e7%a0%81`
- 个人进件页使用的网关返回码锚点原文：`https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm#网关返回码`

同时给出可直接阅读的规范 Markdown：`https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md`。旧 SPA/锚点是字段来源原文，规范 Markdown 是公共全集阅读地址，两者并存，不得互相覆盖。

## 商户业务开通专项资料

### 业务类型、材料和协议

| 字段路径 / 触发条件 | 资料类型与用途 | 原始地址 |
| --- | --- | --- |
| `data.mer_bus_type` | 商户业务类型编码；官网原文为 HTTP | `http://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%E5%95%86%E6%88%B7%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B` |
| `data.online_busi_type`；开通快捷、网银、余额支付 Pro、银行大额转账、分账比例大于 30% 或代扣 | 线上业务类型编码及补充材料说明（XLSX） | `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E7%BA%BF%E4%B8%8A%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B%E7%BC%96%E7%A0%81%E5%8F%8A%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E.xlsx` |
| `data.extended_material_list`；纸质协议或 `data.agreement_info` | 商户合同签约规则 / 签约协议材料说明（XLSX） | `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%95%86%E6%88%B7%E5%90%88%E5%90%8C%E7%AD%BE%E7%BA%A6%E8%A7%84%E5%88%99.xlsx` |
| `data.extended_material_list`；余额支付 | 余额支付补充材料（XLSX） | `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E4%BD%99%E9%A2%9D%E6%94%AF%E4%BB%98%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99.xlsx` |
| `data.extended_material_list`；分账 | 分账功能材料说明（XLSX） | `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/spin/files/20260611/KYC-%E5%88%86%E8%B4%A6%E5%8A%9F%E8%83%BD%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E%281%29.xlsx` |
| `data.extended_material_list`；代扣 | 代扣支付补充材料（XLSX） | `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/%E4%BB%A3%E6%89%A3%E6%94%AF%E4%BB%98%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99.xlsx` |
| `data.agreement_info.agreement_type=3` 与 `data.agreement_info.agreement_url` | 挂网支付服务协议固定地址（HTML）；这是必须按官网示例填写的字段值 | `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/PaymentServiceAgreement.htm` |

不得根据这些文件名猜测文件内的全部枚举、材料数量或审核口径。只有实际读取并核验文件正文后才可引用其内容；否则只提示原始地址和触发条件。

`data.mer_bus_type` 的字段说明原始跳转必须保留上表的 HTTP 地址；若用户还需要可直接审阅的通用参数 Markdown 原文，可同时给出 `https://paas.huifu.com/partners/api/doc/api_ggcsbm.md`。两者用途不同，不得用 Markdown 首页替换字段说明中的原始锚点。

### 渠道、资金与交易专项

| 字段路径 / 触发条件 | 资料 / 用途 | 原始地址 |
| --- | --- | --- |
| `data.out_order_funds_config` | 该字段即将废弃，转全渠道资金管理配置接口 | `https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_qypz` |
| `data.forced_delay_flag=Y` | 强制延迟交易的交易确认接口；官网原文为 HTTP | `http://paas.huifu.com/open/doc/api/#/smzf/api_jyqr` |
| `data.ali_conf_list[].mcc`、`data.wx_conf_list[].mcc`、`data.hb_fq_fee_config.ali_mcc` | 支付宝 MCC | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_zfbmcc` |
| `data.wx_conf_list[].pay_scene` 与逐业务通知 `pay_scene` | 微信支付场景 | `https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e5%be%ae%e4%bf%a1%e6%94%af%e4%bb%98%e5%9c%ba%e6%99%af` |
| `data.wx_conf_list[].fee_rule_id` | 微信费率规则 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wxflgz` |
| `data.wx_conf_list[].wx_real_name_info.finance_institution_flag/finance_type` | 微信金融机构选择指引（腾讯第三方文档） | `https://kf.qq.com/faq/220215IrMRZ3220215n6buiU.html` |
| `data.wx_conf_list[].wx_real_name_info.special_category_id` | 微信支付特殊行业 ID 对照表（微信支付第三方文档） | `https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/applysubject_new/chapter6_1.shtml` |
| `data.union_conf_list[].mcc` 与银联配置中的 `mcc` | 银联 MCC 编码 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylmccbm` |
| `data.out_order_funds_config.out_order_auto_acct_flag=0` | 处理银行来账通知 | `https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_lztz` |
| `data.out_order_funds_config.out_order_auto_acct_flag=0` | 汇付入账确认接口 | `https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_yhskfk` |
| `data.large_amt_pay_config.large_amt_pay_config_info_list[].biz_type` | 订单匹配的要素信息 | `https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_ddppys` |
| 逐业务通知 `ord_id` | `RECV_ORD_ID_` 应答说明原始页；只适用于存在 `ord_id` 的逐业务通知 | `https://spin.cloudpnr.com/topds/regMerBusiInfo.html#id19` |

支付宝实名认证的 `special_category_id` 字段说明只写“参见支付宝商家行业二级类目 code”，没有给出可核验原始地址。回答应写 `[需要官方确认]`，不得套用微信特殊行业地址或自行搜索一个替代页。

## 详情与申请状态专项资料

详情响应中的以下路径命中时仍要给原始资料地址，因为查询值不能替代编码表或材料说明：

| 字段路径 | 资料 / 用途 | 原始地址 |
| --- | --- | --- |
| `response.data.mcc` | 银联 MCC 编码 | `https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ylmccbm` |
| `response.data.agreement_info_list[]` | 签约协议说明（XLSX） | `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E5%95%86%E6%88%B7%E5%90%88%E5%90%8C%E7%AD%BE%E7%BA%A6%E8%A7%84%E5%88%99.xlsx` |
| `response.data.online_busi_type` | 线上业务类型编码及补充材料说明（XLSX） | `https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/kyc/KYC-%E7%BA%BF%E4%B8%8A%E4%B8%9A%E5%8A%A1%E7%B1%BB%E5%9E%8B%E7%BC%96%E7%A0%81%E5%8F%8A%E8%A1%A5%E5%85%85%E6%9D%90%E6%96%99%E8%AF%B4%E6%98%8E.xlsx` |
| 详情 `response.data.qry_wx_conf_list[].pay_scene` | 微信支付场景。官网字段使用相对地址 `api_ggcsbm.md#微信支付场景`；输出时保留该原文并同时提示规范公共文档地址 | 原文：`api_ggcsbm.md#微信支付场景`；规范地址：`https://paas.huifu.com/partners/api/doc/api_ggcsbm.md#微信支付场景` |
| 申请状态 `response.data.wx_conf_result_list[].pay_scene` | 微信支付场景。官网字段使用相对地址 `api_ggcsbm.md#微信支付场景`；输出时保留该原文并同时提示规范公共文档地址 | 原文：`api_ggcsbm.md#微信支付场景`；规范地址：`https://paas.huifu.com/partners/api/doc/api_ggcsbm.md#微信支付场景` |
| 费率查询 `response.data.wx_fee_rate_list[].pay_scene` | 微信支付场景。官网字段使用相对地址 `api_ggcsbm.md#微信支付场景`；输出时保留该原文并同时提示规范公共文档地址 | 原文：`api_ggcsbm.md#微信支付场景`；规范地址：`https://paas.huifu.com/partners/api/doc/api_ggcsbm.md#微信支付场景` |
| `response.data.out_order_funds_merge.out_order_auto_acct_flag=0` | 处理银行来账通知 / 汇付入账确认接口 | `https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_lztz`；`https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_yhskfk` |
| `response.data.large_amt_pay_config.large_amt_pay_config_info_list[].biz_type` | 订单匹配的要素信息 | `https://paas.huifu.com/open/doc/api/#/dejy/api_dejy_ddppys` |

申请单状态查询除加签说明、返回码和微信支付场景外，没有新增下载文件。不要因状态字段名称与业务开通相似而自动追加业务开通的全部 XLSX。

## 不得误报为外部资料的 URL

以下 URL 在官网字段中只是格式示例、运行时值或响应样例。回答不得把它们列为“官方资料”“推荐地址”或默认值：

| 类型 / 字段 | 官网示例 | 正确处理 |
| --- | --- | --- |
| `async_return_url/busi_async_return_url/recon_resp_addr/agreement_async_return_url` | `http://service.example.com/to/path` | 由调用方提供真实受控回调地址；示例不能提交。 |
| 商户主页、签约回跳等运行时 URL | `https://paas.huifu.com/`、`https://www.huifu.com/home/`、`https://www.huifu.com` | 仅说明格式；不得当默认地址。 |
| `online_media_info_list[].other_info` | `http://download.huifu.com` | 商户自己的有效信息、网站或 APP 下载地址；不是资料链接。 |
| 逐业务通知 `qrcode_data` | `https://qr.alipay.com/bax02911brluc2xieoph6001` | 渠道返回的运行时二维码；不得写入请求。 |
| 图片上传 `data.file_url` | 官网图片 URL 示例（原址不在 Skill 中复述） | 必须替换为调用方真实受控文件地址。 |
| 图片上传请求示例 | 占位图片 URL（原址不在 Skill 中复述） | 仅用于说明格式，不得提交。 |
| 详情响应中的 `jfile` 图片链接 | 返回样例中的运行时文件地址（原址不在 Skill 中复述） | 不得复用、下载或作为材料默认值。 |

若用户询问这些字段，仍应明确提示“该 URL 是示例或运行时 URL，不是外部资料，也不是默认值”，但不要把示例地址作为建议值重复输出。

## 交付前自检

- 是否只加载并输出了本次相关字段的资料，而非无差别列出全部地址？
- 是否有独立标题 `外部资料提示`？
- 是否同时给了完整字段路径、资料名、触发条件、可点击链接和明文原始 URL？
- 是否每条都重复了完整字段路径，没有使用“同字段”“同上”或短字段名？
- 是否保留了原始协议、锚点、大小写、百分号编码和 `http://`，没有改成首页或短链接？
- 官网只有相对地址或 `#锚点` 时，是否同时给出原文与按已登记官方文档命名空间（无例外时按来源页）解析后的绝对地址，而不是只给其中一个？
- 是否对未实际读取的 XLSX/外站正文明确写了“未读取外部文件内容，请按原始地址人工核验”？
- 是否把固定的 `agreement_url` 与普通示例 URL 区分开？
- 是否避免把回调地址、商户网站、二维码、图片示例或 `other_info` 当成官方资料？
- 是否没有用链接替代字段本身的类型、长度、必填性、枚举、默认值和条件校验？
