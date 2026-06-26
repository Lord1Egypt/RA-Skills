# OpenClaw Enterprise 关键词路由表

## 路由规则

| 关键词 | Agent | 分类 |
|--------|-------|------|
| 原料、供应商、行情、比价、采购 | 原料采购Agent | procurement |
| 库存、库位、仓储、备货 | 仓储管理Agent | procurement |
| 物流、车队、运输、发货 | 物流调度Agent | procurement |
| 排产、工单、交期、产能 | 生产调度Agent | production |
| 质量、检测、合格率、质检 | 质量检测Agent | production |
| 报价、价格、定价、询价 | 报价Agent | sales |
| 订单、发货、履约、跟踪 | 订单履约Agent | sales |
| 客户、跟进、复购、CRM | 客户管理Agent | sales |
| 成本、毛利、利润、核算 | 成本核算Agent | finance |
| 风控、预警、信用、风险 | 风险预警Agent | finance |
| 数据、报表、月报、分析 | 数据分析Agent | operations |
| 报告、会议、文档、纪要 | 报告生成Agent | operations |
| 售后、投诉、客服、支持 | 客服支持Agent | operations |

## 默认路由
无法匹配时默认路由到：数据分析Agent
