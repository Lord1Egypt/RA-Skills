# 用户开户外部资料索引

命中字段说明中的外部资料时，输出“外部资料提示”，写出完整字段路径、触发条件和未经改写的官方地址。未读取正文时要求人工核验，不得从示例推导编码。

| 资料 | 触发字段 | 官方地址 |
| --- | --- | --- |
| V2 加签验签 | 公共 `sign` | https://paas.huifu.com/partners/start/api_v2jqyq.md |
| 加密解密 | 接口说明明确要求加密/解密的敏感字段 | https://paas.huifu.com/partners/start/api_jiami_jiemi.md |
| 密钥角色与获取 | 请求加签、同步/异步验签和指定字段加解密 | https://paas.huifu.com/partners/start/guide_gsycshq.md |
| 接口异步通知 | `request.data.async_return_url` | https://paas.huifu.com/partners/start/ybxx/jiekouguifan_ybxx.md |
| 自然人证件类型 | `legal_cert_type`、`cert_type` | https://paas.huifu.com/open/doc/api/#/api_ggcsbm?id=%e8%87%aa%e7%84%b6%e4%ba%ba%e8%af%81%e4%bb%b6%e7%b1%bb%e5%9e%8b |
| 国籍编码 XLSX | 法人/个人外国人居留证触发国籍 | https://cloudpnrcdn.oss-cn-shanghai.aliyuncs.com/opps/api/prod/download_file/area/%E5%9B%BD%E7%B1%8D.xlsx |
| 省市区编码 | 注册地、个人地址、结算卡、e账户卡省市区 | https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_dqbm |
| 汇付 MCC | 企业/个人 `mcc` | https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_hfmccbm |
| 文件类型 | 所有 `file_list[].file_type` | https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx |
| 图片上传 | 所有 `file_list[].file_id` 来源 | https://paas.huifu.com/open/doc/api/#/shgl/shjj/api_shjj_shtpsc |
| 银行编码 | e账户卡或查询卡信息 | https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_yhbm |
| 银行支行编码 | `request.data.card_info.branch_code`、`request.data.elec_acct_config.elec_card_list[].branch_code`、`response.data.card_info.branch_code`、`response.data.qry_cash_card_info_list[].branch_code`、`response.data.elec_acct_config.elec_card_list[].branch_code` | https://paas.huifu.com/partners/api/doc/csfl/api_csfl.md |
| 结算批次 | `settle_batch_no` | https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_jspc |
| 结算摘要配置 | `settle_abstract` | https://paas.huifu.com/open/doc/api/#/jyjs/api_jyjs_pzslsm |
| 中信资金/角色类型 | `elec_acct_config.scene/role_type` | https://paas.huifu.com/open/doc/api/#/yuer/api_zxegjzllx |
| 业务返回码 | `resp_code/sub_resp_code` | https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_ywm |

图片上传链接属于商户进件文档命名空间。其 `data.huifu_id` 只支持直属商户号，不支持本 Skill 返回的用户号；读取该页面时必须联读 `$huifu-merchant-onboarding` 的图片安全边界。

`response.data.qry_cash_card_info_list[].branch_code` 的接口字段行本身只写“请参考点击查看”且链接缺失；接入方补充的官方“基础参数汇总”明确提供银行支行编码 XLSX、JSON、CSV 下载，因此现按完整路径绑定上表公共入口。这个裁决来自公共资料，不是按同名叶字段猜测。

接口 `async_return_url` 与控台 Webhook 是两套协议。Webhook 只在用户明确选择控台事件订阅时读取 `https://paas.huifu.com/partners/devtools/doc/webhook/webhook_jieshao.md`；不得用其终端密钥、任意2xx应答或重推规则覆盖接口异步通知。

回调地址、示例网站、图片裸 URL、下载地址或运行时 `async_return_url` 不自动构成“外部资料”，也不是默认值。
