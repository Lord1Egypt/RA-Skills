# 用户开户官方来源索引

当前活动快照：`2026-11-09`；九份接口原文逐页下载并锁定，相对11-04原文字节均未变，正式路径无增删，仍为644条（请求345、响应227、异步72）。10-25已完成以下变更：业务入驻/修改新增协议与外扣账户配置，通知区分E/A/U/Z并调整account_info编码；状态/详情新增协议和失败原因，企业/个人开户补充sys_id上下级绑定说明。历史快照保持不可变。

| 接口 | 官方页面 | 页面更新时间 | SHA-256 |
| --- | --- | --- | --- |
| 企业用户开户 | https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_qyyhjbxxzc.md | 2026.10.21 | `9ae70289683601611a7e9e675c382778e8447b48786ded16a345460ab630c476` |
| 个人用户开户 | https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_gryhjbxxzc.md | 2026.10.21 | `41f9a75dab6ff2d157ff9f02793afa1ada3baec8f0d67664bed8c1ad08e53bf2` |
| 用户业务入驻 | https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_ywrz.md | 2026.10.20 | `bef9e9e82e9e0dfc5f4d0445242abfb711fe32195386dd99618366f3110b1191` |
| 用户申请单状态查询 | https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhsqdzt.md | 2026.09.24 | `50ee782a7bec09697018ce22927ab8fed3c7eb1ff8e745ec53c19a4d2d65b053` |
| 用户信息查询 | https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhywcx.md | 2026.10.20 | `3347a35c7706eca63557a8e2c24b7048defd5095540ca5ed32832705c89391ca` |
| 企业用户基本信息修改 | https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_qyyhjbxxxg.md | 2026.09.04 | `bb0b2a7339463d9731243e7d91ec9bfd729180d844646bb119b68655a11a5df8` |
| 个人用户基本信息修改 | https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_gryhjbxxxg.md | 2026.09.04 | `b1495f896cfc12f8e8324c8aa1f97655c0c87d41c626ea636eda54b7b3aa741c` |
| 用户业务入驻修改 | https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_ywrzxg.md | 2026.10.20 | `cea918c6a5d5674cdfe22981ffb1066866f40ab4ea649bb312f36fe1296e0cd2` |
| 用户列表查询 | https://paas.huifu.com/partners/api/doc/yhgl/api_yhgl_yhlbcx.md | 2026.09.04 | `b10ab1529c58d5739cae0f38b5f385a105e3f2d6b3348400f6882328b7421d9d` |

辅助公共资料（读取于 `2026-08-10`，不计入当前九接口644个字段节点）：

| 资料 | 官方页面 | SHA-256 |
| --- | --- | --- |
| 异步消息简介 | https://paas.huifu.com/partners/start/ybxx/jiekouguifan_ybxx.md | `e5f1ad5d92511c343d6bbf7d5f09ef0eee4a252bdac3b4d53934c177f6805364` |
| 开发规范 | https://paas.huifu.com/partners/start/kfgf.md | `340ba948aae4cb1fc6b12503b58e24d11c538b5ba70d0728ef374b0d1a4137a5` |
| 加签验签 | https://paas.huifu.com/partners/start/api_v2jqyq.md | `f3ddf23effad316d247033eb5d2f781e57a8d3d23260387b42470de8e1fd76c5` |
| 加密解密 | https://paas.huifu.com/partners/start/api_jiami_jiemi.md | `de9c44b0dc59d34a609ea6fde5437cc7d633722cd770ecadf37a13b347f4bb82` |
| 获取密钥 | https://paas.huifu.com/partners/start/guide_gsycshq.md | `8f79c590233daba14ba2c958ba89d4f6326f624a20bff053d5c5159ec03afab0` |
| 开发接入说明 | https://paas.huifu.com/partners/start/api_kfzn.md | `a50c162dcbafd71044c1c6687b6b908e050a5e5aa54267336ef75661b1f5410d` |
| 基础参数汇总 | https://paas.huifu.com/partners/api/doc/csfl/api_csfl.md | `2d8b73e1009da4b2fccfae75b0bc2546acfc105b2219ada12a2af41f2b6da191` |
| Webhook 介绍 | https://paas.huifu.com/partners/devtools/doc/webhook/webhook_jieshao.md | `8a14a938445d9b7e15f2bce5af27b0a38708a601fbbfd88c3004a045cb333089` |

接口解释以冻结原文、完整字段目录、字段合同和 `user-onboarding-platform-contracts.md` 共同为依据。刷新时如果 SHA 变化，先生成语义差异并人工复核，再更新原子页；不能只替换网页或只改字段计数。公共资料解决传输、签名、密钥、编码表和通知协议，不覆盖接口页的字段名、类型、长度、Y/N/C 或嵌套结构。
