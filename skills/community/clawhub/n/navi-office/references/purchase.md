# 采购管理 (purchase_*)

## 供应商查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `purchase_querySupplierList` | — | `supplierName`(模糊) `level`(1战略/2核心/3普通) `page` `limit` | 供应商列表 |

## 供应商创建

`purchase_createSupplier(supplierData: JSON)`

**必填**：`supplierName`

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `supplierCode` | 供应商编码 | — |
| `supplierType` | 供应商类型 | 1生产厂家 / 2代理商 / 3经销商 / 4其他 |
| `level` | 等级 | 1战略 / 2核心 / 3普通 |
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
| `rating` | 评分 | — |
| `ownerId` | 负责人ID | — |
| `ownerName` | 负责人姓名 | — |
| `status` | 状态 | — |
| `remark` | 备注 | — |

## 采购订单查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `purchase_queryOrderList` | — | `supplierId` `supplierName`(模糊) `startDate` `endDate` `page` `limit` | 采购订单列表 |
| `purchase_queryOrderDetail` | `orderId` | — | 订单详情（含明细/收货情况） |

## 采购订单创建

`purchase_createOrder(orderData: JSON)`

**必填**：`supplierId` `orderDate`(yyyy-MM-dd)

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `orderName` | 订单名称 | — |
| `supplierName` | 供应商名称 | — |
| `projectId` | 关联项目ID | — |
| `projectName` | 关联项目名称 | — |
| `expectedDate` | 期望到货日期 | yyyy-MM-dd |
| `buyerId` | 采购员ID | — |
| `buyerName` | 采购员姓名 | — |
| `deptId` | 部门ID | — |
| `totalAmount` | 总金额 | — |
| `discountAmount` | 折扣金额 | — |
| `finalAmount` | 最终金额 | — |
| `requestId` | 采购申请ID | — |
| `requestNo` | 采购申请号 | — |
| `sourceType` | 来源类型 | — |
| `sourceNo` | 来源单据号 | — |
| `remark` | 备注 | — |

> 先调 `purchase_querySupplierList` 获取 `supplierId`

## 采购统计

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `purchase_queryStatistics` | — | `startDate` `endDate` | 采购总额/订单数/供应商数/平均周期 |
