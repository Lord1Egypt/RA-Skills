# 商户进件官方来源索引

普通回答使用本地 references；以下 URL 只用于来源追溯、维护刷新和显式联网核验。

## 十三接口来源

| 接口 | 官方原始地址 | 当前 SHA-256 |
| --- | --- | --- |
| 企业商户进件 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_qyshjbxxrz_kyc.md | `6606629100f94813a7a4238c8f1ffc970ec3b905d1af9487bb92baee6138822e` |
| 个人商户进件 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_grshjbxxrz_kyc.md | `09862a3923b114abcf7dbc9e7545798481abc37f88b6eb64911ce7d53f9f5437` |
| 商户业务开通 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_kyc.md | `42d692619bd409ae11b95b43a0badec25794316e8fa0fc6de3c02c5fa2ae4ddd` |
| 图片上传 | https://paas.huifu.com/navigator/ossApi/api_shjj_shtpsc.json | `2fcb84dd1cfe0260cfa3d49b79174d2e7b8a287cdf860faa62011bfc1e8472dd` |
| 商户详情查询 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shxxxxcx_kyc.md | `3fb7115e030937181c3040f8d57c16ce8b44aa75fb78849d950af8816fc0a918` |
| 申请状态查询 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_sqdztcx.md | `8c39b88e199d2c877267994172fa09de5130c47d38eb5f01147d2d1520c2bef4` |
| 商户业务开通修改 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywktxg_kyc.md | `3f9e0e6b302807646b4a7a02830ef50ae4c6b90f5fab1ddea9eaeb72d12c5cf4` |
| 商户基本信息修改 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shjbxxxg_kyc.md | `f2146bc553eb4b1dc8c88d4487eb1b5c721468d6a8eec5be7d0ce9f086db4d6c` |
| 商户费率信息查询 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_merchant_conf_search_cx.md | `20a3be9f505c542a716bbdad65da146f9089be05b206850c089c6df4e9ac050e` |
| 商户状态变更 | https://paas.huifu.com/partners/api/doc/shgl/api_shgl_shztbg.md | `d2fe6ab4404abd79b3ac5f5eecffaaec9d61d245ac1a60ebccddee889535a07f` |
| 商户短信发送 | https://paas.huifu.com/partners/api/doc/shgl/shjj/api_shjj_shdxfs.md | `6982fe07d276cbb0739c9c205afbc5b238dd6d72422154efd6248932aa459b54` |
| 商户多费率配置 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflpz.md | `e4b23cb9bfaf59e9a88448a890f539d7ee9cbf7002d763a7d078294053aa7473` |
| 商户多费率配置查询 | https://paas.huifu.com/partners/api/doc/shgl/shywkt/api_shjj_shywkt_dflcx.md | `e2c0f53e77a1ef00827cc8be28ac688c068e5c8a4dc9f741845b841dcd16881a` |

核验快照：`2026-11-09`。十三接口相对11-04快照有1页原文字节变化：业务开通修改的sign_start_date长度7修正为8；完整路径新增0、删除0、同路径属性变化1，总计2,258路径（请求1,301、响应777、异步180）。其余用户、扩展和子账户23份来源均未变。历史快照保持不可变。

辅助公共资料（不计入上述13个接口快照）：[基础参数汇总](https://paas.huifu.com/partners/api/doc/csfl/api_csfl.md)、[返回码](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_ywm.md)、[名词解释](https://paas.huifu.com/partners/api/doc/csfl/api_csfl_mcjs.md)。它们用于公共编码、返回码全集和术语释义，不能覆盖具体接口页的字段类型、长度、必填性、层级或通知结构。

## 使用规则

1. 官网 URL 不列入“本轮实际使用的 references”。
2. 当前本地目录是冻结快照，不自动代表官网未来版本。
3. 字段说明引用外部编码、XLSX、协议或第三方资料时，读取 `merchant-onboarding-external-resources.md`。
4. 未读取外部正文时明确要求人工核验，不根据文件名猜规则。
5. 刷新来源时必须记录 URL、获取时间、SHA 和字段 delta。

## 子账户配置来源

当前新增快照：`2026-11-09`；两接口130条路径，读取 `merchant-account-complete-field-catalog.md` 与 `merchant-account-sdk-matrix.md`。

| 接口 | 官方地址 | SHA-256 |
| --- | --- | --- |
| 子账户开通配置 | https://paas.huifu.com/partners/api/doc/zhgl/api_zhgl_zhpz_kyc.md | `b496d1493ed0615115e8972272f0a717289a5feab6206080a62c83615ea9eb8b` |
| 修改子账户配置 | https://paas.huifu.com/partners/api/doc/zhgl/api_zhgl_xgzh_kyc.md | `6c041ff7af41573a97463077062725c6a0ca2815b0d64b64fea6c32e21bd3c05` |
