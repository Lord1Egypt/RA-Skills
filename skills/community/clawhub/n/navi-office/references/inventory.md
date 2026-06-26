# 库存管理 (inventory_*)

## 物料查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `inventory_queryMaterialList` | — | `materialName`(模糊) `materialCode`(精确) `materialType`(原材料/半成品/成品/包装材料) `page` `limit` | 物料列表 |

## 物料创建

`inventory_createMaterial(materialData: JSON)`

**必填**：`materialCode` `materialName` `unit`

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `categoryId` | 分类ID | — |
| `categoryName` | 分类名称 | — |
| `specification` | 规格型号 | — |
| `materialType` | 物料类型 | 1原料 / 2半成品 / 3成品 / 4其他 |
| `purchasePrice` | 采购价 | — |
| `salePrice` | 销售价 | — |
| `minStock` | 最低库存 | — |
| `maxStock` | 最高库存 | — |
| `safetyStock` | 安全库存 | — |
| `leadTime` | 采购周期(天) | — |
| `shelfLife` | 保质期(天) | — |
| `isBatchManage` | 是否批次管理 | true / false |
| `status` | 状态 | — |
| `remark` | 备注 | — |

## 仓库与库存

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `inventory_queryWarehouseList` | — | `warehouseName`(模糊) | 仓库列表；获取warehouseId |
| `inventory_queryStockList` | — | `materialName`(模糊) `warehouseId` `page` `limit` | 库存列表 |
| `inventory_queryStockReport` | — | `warehouseId` `materialCode` `materialName`(模糊) | 库存汇总报表 |
| `inventory_queryLowStockList` | — | `warehouseId` | 低于安全库存的物料 |

## 入库单创建

`inventory_createInbound(inboundData: JSON)`

**必填**：`inboundType` `inboundDate`(yyyy-MM-dd) `warehouseId`

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `inboundType` | 入库类型 | 1退货 / 2生产 / 3盘盈 / 4其他 |
| `warehouseName` | 仓库名称 | — |
| `inboundReason` | 入库原因 | — |
| `handlerId` | 经办人ID | — |
| `handlerName` | 经办人姓名 | — |
| `remark` | 备注 | — |

**detailList**（入库明细数组）：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `materialId` | 物料ID | 先调 `inventory_queryMaterialList` 获取 |
| `materialCode` | 物料编码 | — |
| `materialName` | 物料名称 | — |
| `specification` | 规格型号 | — |
| `unit` | 单位 | — |
| `quantity` | 数量 | — |
| `locationId` | 库位ID | — |
| `locationName` | 库位名称 | — |
| `batchNo` | 批次号 | — |
| `remark` | 备注 | — |

> 先调 `inventory_queryWarehouseList` 获取 `warehouseId`，先调 `inventory_queryMaterialList` 获取 `materialId`

## 出库单创建

`inventory_createOutbound(outboundData: JSON)`

**必填**：`outboundType` `outboundDate`(yyyy-MM-dd) `warehouseId`

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `outboundType` | 出库类型 | 1领料 / 2报废 / 3盘亏 / 4其他 |
| `warehouseName` | 仓库名称 | — |
| `outboundReason` | 出库原因 | — |
| `handlerId` | 经办人ID | — |
| `handlerName` | 经办人姓名 | — |
| `remark` | 备注 | — |

**detailList**（出库明细数组）：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `materialId` | 物料ID | 先调 `inventory_queryMaterialList` 获取 |
| `materialCode` | 物料编码 | — |
| `materialName` | 物料名称 | — |
| `specification` | 规格型号 | — |
| `unit` | 单位 | — |
| `quantity` | 数量 | — |
| `locationId` | 库位ID | — |
| `locationName` | 库位名称 | — |
| `batchNo` | 批次号 | — |
| `remark` | 备注 | — |

> 先调 `inventory_queryWarehouseList` 获取 `warehouseId`，先调 `inventory_queryMaterialList` 获取 `materialId`

## 库存分析

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `inventory_queryInOutStatistics` | — | `startDate` `endDate` `warehouseId` `materialName`(模糊) | 出入库统计 |
| `inventory_queryTurnoverAnalysis` | — | `startDate` `endDate` `warehouseId` | 库存周转分析（含呆滞物料） |
