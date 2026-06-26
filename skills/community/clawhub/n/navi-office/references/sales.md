# 销售管理 (sales_*)

## 订单查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `sales_queryOrderList` | — | `orderName`(模糊) `customerName`(模糊) `customerId` `executionStatus` `startDate` `endDate` `page` `limit` | 订单列表 |
| `sales_queryOrderDetail` | `orderId` | — | 订单详情（含明细/合同/交付） |

## 订单创建

`sales_createOrder(orderData: JSON)`

**必填**：`name` `customerId` `amount`

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `orderType` | 订单类型 | 1产品销售 / 2计量检测 / 3其他服务 |
| `customerName` | 客户名称 | — |
| `opportunityId` | 关联商机ID | — |
| `opportunityName` | 商机名称 | — |
| `serviceStartTime` | 服务开始时间 | yyyy-MM-dd |
| `serviceEndTime` | 服务完成时间 | yyyy-MM-dd |
| `contractNumber` | 合同编号 | — |
| `quotationId` | 报价单ID | — |
| `remark` | 备注 | — |

**detailList**（订单明细数组）：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `productId` | 产品ID | — |
| `productName` | 产品名称 | — |
| `specification` | 规格型号 | — |
| `unit` | 单位 | — |
| `quantity` | 数量 | — |
| `price` | 单价 | — |
| `amount` | 金额 | — |
| `taxRate` | 税率(%) | — |
| `taxAmount` | 税额 | — |
| `totalAmount` | 含税金额 | — |
| `remark` | 备注 | — |

> 先调 `crm_queryCustomerList` 获取 `customerId`

## 合同查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `sales_queryContractList` | — | `searchKey`(模糊) `orderId` `page` `limit` | 合同列表 |

## 合同创建

`sales_createContract(contractData: JSON)`

**必填**：`name` `orderId`

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `userId` | 客户ID | — |
| `content` | 合同内容 | — |
| `filePath` | 合同文件路径 | — |
| `fileType` | 文件类型 | — |
| `fileSize` | 文件大小 | — |
| `expireNotify` | 到期提醒 | 0不提醒 / 1提醒 |
| `remark` | 备注 | — |

## 应收计划生成

`sales_generateReceivable(receivableData: JSON)`

**必填**：`orderId` `plans`（收款计划数组）

**plans 每项字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `period` | 期次 | — |
| `amount` | 应收金额（**必填**） | — |
| `receivableDate` | 应收日期（**必填**） | yyyy-MM-dd |
| `dueDate` | 到期日期 | yyyy-MM-dd |
| `settlementMethod` | 结算方式 | — |
| `paymentTerms` | 付款条款 | — |
| `remark` | 备注 | — |

> 先调 `sales_queryOrderList` 获取 `orderId`，支持一次性或分期收款

## 销售分析

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `sales_queryStatistics` | — | `startDate` `endDate` | 销售额/订单数/客户数（默认本月） |
| `sales_queryRanking` | — | `startDate` `endDate` | 销售员排名 |
| `sales_queryCustomerList` | — | `customerName`(模糊) `page` `limit` | 有销售记录的客户列表 |
