# 计量检测 (calibration_*)

## 委托单查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `calibration_queryCommissionList` | — | `keyword`(委托单号或客户名模糊) `commissionStatus`(0待检测/1检测中/2待审核/3已完成/4已交付) `customerId` `receiveDateStart` `receiveDateEnd` `page` `limit` | 委托单列表 |
| `calibration_queryCommissionDetail` | `commissionId` | — | 委托单详情（客户/器具清单/检测进度） |

## 委托单创建

`calibration_createCommission(commissionData: JSON)`

**必填**：`receiveDate`(yyyy-MM-dd)

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `salesOrderId` | 关联销售订单ID | — |
| `salesOrderNo` | 关联销售订单号 | — |
| `customerId` | 客户ID | 先调 `crm_queryCustomerList` 获取 |
| `customerName` | 客户名称 | — |
| `salesmanId` | 业务员ID | — |
| `salesmanName` | 业务员姓名 | — |
| `expectedFinishDate` | 预计完成日期 | yyyy-MM-dd |
| `contactName` | 联系人姓名 | — |
| `contactPhone` | 联系人电话 | — |
| `totalAmount` | 总金额 | — |
| `deliveryDate` | 交付日期 | yyyy-MM-dd |
| `deliveryPerson` | 交付人 | — |
| `receiverName` | 接收人 | — |
| `remark` | 备注 | — |

**commissionDetails**（委托明细数组）：

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
| `type` | 类型 | — |
| `status` | 状态 | — |
| `remark` | 备注 | — |

> 先调 `crm_queryCustomerList` 获取 `customerId`

## 从销售订单创建委托单

`calibration_createCommissionFromOrder(salesOrderId)`

**必填**：`salesOrderId`（销售订单ID）

> 先调 `sales_queryOrderList` 获取 `salesOrderId`

## 器具

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `calibration_queryInstrumentList` | — | `instrumentName`(模糊) `instrumentStatus`(0待检/1检测中/2完成/3已交付) `expireDays`(N天内到期) `customerId` `page` `limit` | 器具列表 |

## 证书

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `calibration_queryCertificateList` | — | `certificateNo` `instrumentId` `result`(合格/不合格/准用) `expireDays`(N天内到期) `page` `limit` | 证书列表 |

## 业绩统计

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `calibration_querySalesmanPerformance` | — | `startDate` `endDate` `page` `limit` | 业务员业绩（委托单数/器具数/收入/排名） |
| `calibration_queryEngineerPerformance` | — | `startDate` `endDate` `page` `limit` | 工程师业绩（检测任务数/器具数/工时/排名） |
