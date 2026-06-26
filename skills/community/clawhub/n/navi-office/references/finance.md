# 财务管理 (finance_*)

## 财务看板

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `finance_queryDashboard` | — | `startDate` `endDate` | 收支利润总览（默认本月） |
| `finance_queryDepartmentExpense` | — | `startDate` `endDate` | 部门费用统计 |
| `finance_queryPayableReceivable` | — | — | 应收应付总览 |
| `finance_queryProfitAnalysis` | — | `startDate` `endDate` `dimension`(month/quarter/year) | 利润分析 |
| `finance_queryRevenueStatistics` | — | `startDate` `endDate` `dimension` | 收入统计明细 |
| `finance_queryRevenueTrend` | — | `months`(默认6) | 最近N个月收支利润走势 |

## 应收账款查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `finance_queryReceivableList` | — | `customerName`(模糊) `status`(0未收/1部分/2已收/3逾期) `dueDateStart` `dueDateEnd` `page` `limit` | 应收列表 |
| `finance_queryReceivableStatistics` | — | — | 应收总额/已收/未收/收款率 |

## 应收账款创建

`finance_createReceivable(receivableData: JSON)`

**必填**：`customerName` `receivableAmount` `receivableDate`(yyyy-MM-dd)

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `businessType` | 业务类型 | 1销售收入 / 2服务收入 / 3其他收入 |
| `orderId` | 销售订单ID | — |
| `businessNo` | 业务单据号 | — |
| `contractNo` | 合同编号 | — |
| `dueDate` | 到期日期 | yyyy-MM-dd |
| `settlementMethod` | 结算方式 | — |
| `paymentTerms` | 付款条款 | — |
| `employeeId` | 业务员ID | — |
| `employeeName` | 业务员姓名 | — |
| `needInvoice` | 是否需要发票 | 0否 / 1是 |
| `remark` | 备注 | — |

## 应付账款查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `finance_queryPayableList` | — | `supplierName`(模糊) `status`(0未付/1部分/2已付/3逾期) `dueDateStart` `dueDateEnd` `page` `limit` | 应付列表 |

## 应付账款创建

`finance_createPayable(payableData: JSON)`

**必填**：`supplierName` `payableAmount` `payableDate`(yyyy-MM-dd)

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `businessType` | 业务类型 | 1采购 / 2预算 / 3日常 / 4费用 / 5其他 |
| `businessNo` | 业务单据号 | — |
| `projectId` | 关联项目ID | — |
| `projectName` | 项目名称 | — |
| `dueDate` | 到期日期 | yyyy-MM-dd |
| `settlementMethod` | 结算方式 | — |
| `paymentTerms` | 付款条款 | — |
| `employeeId` | 经办人ID | — |
| `employeeName` | 经办人姓名 | — |
| `needInvoice` | 是否需要发票 | 0否 / 1是 |
| `remark` | 备注 | — |

## 费用查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `finance_queryExpenseList` | — | `page` `limit` | 费用记录列表 |

## 费用创建

`finance_createExpense(expenseData: JSON)`

**必填**：`projectId` `type` `amount` `payTime`(yyyy-MM-dd)

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `type` | 收付款类型 | 1收款 / 2付款 |
| `expenseType` | 费用类型 | 1招待 / 2出差 / 3税费 / 4固定资产 / 5居间费 / 6其他 |
| `invoiceStatus` | 发票状态 | 1未开票 / 2已开票 |
| `invoiceTime` | 开票时间 | yyyy-MM-dd |
| `accountType` | 账户类型 | 1公账 / 2私账 |
| `remark` | 备注 | — |

> `projectId` 先调 `project_queryProjectList` 获取
