# CRM 客户管理 (crm_*)

## 客户查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `crm_queryCustomerList` | — | `customerName`(模糊) `level`(1重要/2普通/3潜在) `source` `industry` `contact` `page` `limit` | 客户列表 |
| `crm_queryCustomerDetail` | `customerId` | — | 客户详情；先查列表获取ID |

## 客户创建

`crm_createCustomer(customerData: JSON)`

**必填**：`customerName` `customerType`

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `customerType` | 客户类型 | 1企业 / 2个人 |
| `customerCode` | 客户编码 | — |
| `categoryId` | 分类ID | — |
| `categoryName` | 分类名称 | — |
| `industry` | 行业 | — |
| `level` | 等级 | 1重要 / 2普通 / 3潜在 |
| `source` | 来源 | — |
| `contact` | 联系人 | — |
| `phone` | 电话 | — |
| `mobile` | 手机 | — |
| `email` | 邮箱 | — |
| `address` | 地址 | — |
| `website` | 网站 | — |
| `taxNo` | 税号 | — |
| `bankName` | 开户行 | — |
| `bankAccount` | 银行账号 | — |
| `creditLimit` | 信用额度 | — |
| `creditDays` | 账期天数 | — |
| `ownerId` | 负责人ID | — |
| `ownerName` | 负责人姓名 | — |
| `productId` | 关联产品ID | — |
| `status` | 状态 | — |
| `remark` | 备注 | — |

## 商机查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `crm_queryOpportunityList` | — | `stage`(线索/初步接触/需求确认/方案提交/商务谈判/赢单/输单) `customerName`(模糊) `customerId` `page` `limit` | 商机列表 |
| `crm_queryOpportunityDetail` | `opportunityId` | — | 商机详情 |

## 商机创建

`crm_createOpportunity(opportunityData: JSON)`

**必填**：`opportunityCode` `opportunityName` `customerId` `customerName` `stage`

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `stageId` | 阶段ID | — |
| `stageName` | 阶段名称 | — |
| `amount` | 金额 | — |
| `winRate` | 赢率(%) | — |
| `expectedCloseDate` | 预计成交日期 | yyyy-MM-dd |
| `needs` | 客户需求 | — |
| `competitors` | 竞争对手 | — |
| `ownerId` | 负责人ID | — |
| `ownerName` | 负责人姓名 | — |
| `status` | 状态 | — |
| `salesOrderId` | 关联销售订单ID | — |
| `salesOrderName` | 关联销售订单名称 | — |
| `winReason` | 赢单原因 | — |
| `loseReason` | 输单原因 | — |
| `remark` | 备注 | — |

> 先调 `crm_queryCustomerList` 获取 `customerId` 和 `customerName`

## 销售分析

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `crm_queryPerformance` | — | `startDate` `endDate` `employeeId` | 销售业绩（不填查自己）；按姓名查先获取employeeId |
| `crm_querySalesFunnel` | — | `startDate` `endDate` | 销售漏斗各阶段数据 |
