# DM取现额度查询

官方来源：<https://paas.huifu.com/partners/api/doc/jyjs/qx/api_DMqxedcx.md>。来源快照：2026-11-04；SHA-256：`494415e9a7aa7f93249845ba587db28cb178224b2b7452280f715315024a2339`。

接口：`/v2/trade/settlement/enchashment/dmamt/query`。方法：POST。

## 使用条件与边界

商户须已开通DM取现权限；渠道商或SaaS服务商可为商户查询并展示额度，不能因此把目标huifu_id换成服务商自身ID。DM可取现额度查询只读取额度，不发起取现；DM到账资金不包括当天交易资金，不等于账户总余额、D0额度或某笔支付终态。`huifu_id:String(32) Y`；`acct_id:String(32) N`，仅基本户、现金户支持DM，未填取基本户。不要补造req_date、req_seq_id或token_no。

响应额度为 `response.data.dm_amt:String(16) N`，单位元；未返回该可选字段时，不能自行补成0或宣称已获得确定额度。

精确路由为 `/v2/trade/settlement/enchashment/dmamt/query`，官方保留enchashment拼写；不能“修正”为主动取现的encashment。使用 `V2TradeSettlementEnchashmentDmamtQueryRequest`。实际取现另选主动取现接口、到账类型DM及已绑定token_no；额度查询成功不代表已出金。权限或账户配置任务再交接进件Skill。

## 信封传输差异

请求信封data正式String(JSON)，示例和官方SDK最终body.data为对象。目录保留正式String及解码子路径；SDK实际发送对象data，不二次JSON编码。此差异不能据其他接口静默改写。

## 完整字段与SDK

单字段类型/必填、完整DTO或同步响应字段均按接口与方向读取 `payment-extension-complete-field-catalog.md` 中的“DM取现额度查询”，覆盖13条正式字段路径。代码任务联读 `payment-extension-sdk-matrix.md` 与 `shared-server-sdk-matrix.md`；专属类 `V2TradeSettlementEnchashmentDmamtQueryRequest`，Python模块 `v2_trade_settlement_enchashment_dmamt_query`。扩展字段先拒绝覆盖SDK已声明字段，再经官方SDK发送；SDK合并本身不提供此保护。日期、流水、金额、账户和角色ID保持调用方值，来源头按实际参与的Skill确定。
