# 生产管理 (mes_*)

## 生产订单查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `mes_queryProductionOrderList` | — | `status`(生产中等) `keyword`(订单号或产品名模糊) `productId` `page` `limit` | 生产订单列表 |
| `mes_queryProductionOrderDetail` | `orderId` | — | 详情（排产/进度/物料/工单） |

## 生产订单创建

`mes_createProductionOrder(orderData: JSON)`

**必填**：`orderType` `productId` `planQuantity` `planStartDate`(yyyy-MM-dd) `planEndDate`(yyyy-MM-dd)

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `orderType` | 订单类型 | 1销售订单 / 2补库 / 3研发试产 |
| `sourceType` | 来源类型 | 1销售订单 / 2手工 |
| `sourceId` | 来源单据ID | — |
| `sourceNo` | 来源单据号 | — |
| `productCode` | 产品编码 | — |
| `productName` | 产品名称 | — |
| `productSpec` | 产品规格 | — |
| `productUnit` | 产品单位 | — |
| `customerId` | 客户ID | — |
| `customerName` | 客户名称 | — |
| `priority` | 优先级 | 1紧急 / 2高 / 3正常 / 4低 |
| `workshopId` | 车间ID | — |
| `workshopName` | 车间名称 | — |
| `bomId` | BOM ID | — |
| `bomVersion` | BOM版本 | — |
| `remark` | 备注 | — |

> 销售订单转生产：先查销售订单获取 `sourceId`

## 工单查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `mes_queryWorkOrderList` | — | `status` `productionOrderId` `keyword` `page` `limit` | 工单列表 |
| `mes_queryWorkOrderDetail` | `workOrderId` | — | 工单详情（BOM/工艺/进度/质检） |

## 工单创建

`mes_createWorkOrder(workOrderData: JSON)`

**必填**：`productionOrderId` `productId` `planQuantity` `planStartTime`(yyyy-MM-dd HH:mm:ss) `planEndTime`(yyyy-MM-dd HH:mm:ss)

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `productionOrderNo` | 生产订单号 | — |
| `productCode` | 产品编码 | — |
| `productName` | 产品名称 | — |
| `productSpec` | 产品规格 | — |
| `productUnit` | 产品单位 | — |
| `workshopId` | 车间ID | — |
| `workshopName` | 车间名称 | — |
| `processId` | 工序ID | — |
| `processCode` | 工序编码 | — |
| `processName` | 工序名称 | — |
| `equipmentId` | 设备ID | — |
| `equipmentCode` | 设备编码 | — |
| `equipmentName` | 设备名称 | — |
| `workerId` | 操作员ID | — |
| `workerName` | 操作员姓名 | — |
| `bomId` | BOM ID | — |
| `remark` | 备注 | — |

> 操作员姓名→先调 `hr_queryEmployeeList` 获取 `workerId`

## 设备

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `mes_queryEquipmentList` | — | `equipmentName`(模糊) `status`(运行中/停机/故障/维修中) `page` `limit` | 设备列表 |
| `mes_queryEquipmentDetail` | `equipmentId` | — | 设备详情（参数/维护/故障历史/当前工单） |
