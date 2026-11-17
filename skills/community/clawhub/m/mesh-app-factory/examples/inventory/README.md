# 进销存系统（inventory）

基于至简网格开发的中小企业进销存系统，满足日常进销存管理需求，操作步骤精简（扫码开单、一键入库/出库、快捷盘点）。

## 功能清单

- **商品管理**：商品档案（条码、分类、单位、售价、成本价、库存、最低库存、供应商），支持模糊搜索、扫码查找
- **分类 / 供应商 / 客户**：基础档案维护
- **采购管理**：创建采购单 → 添加商品 → 完成入库（自动加库存 + 记录流水）
- **销售管理**：创建销售单 → 扫码/搜索加商品 → 折扣/支付方式 → 确认收款（自动减库存 + 记录流水）
- **库存管理**：库存流水追溯（采购入库/销售出库/退货回补/盘点调整）、库存调整（盘点）、低库存预警
- **报表统计**：今日/本月销售额、近7日毛利、销售趋势图、热销商品排行、库存预警列表

## 角色权限（api/pub.json）

- admin 店长：全部功能（含盘点调整、报表、客户档案维护）
- purchaser 采购人员：商品、分类、供应商维护 + 采购
- salesperson 销售人员：销售开单、客户查询

> 接口级 RBAC：product/category/supplier/customer 的写操作按角色授权；
> sales 接口仅 admin/salesperson 可调用，purchase 接口仅 admin/purchaser 可调用（见各接口 feature 配置）。

## 服务依赖（service.cfg）

config、seqid、keystore、user 四个基础服务。

## 部署

将本目录（inventory）作为服务目录部署到至简网格服务器（单例版或集群版）：

1. 服务目录名即服务名，保持 `inventory`
2. 首次启动自动建库建表（rdb: inventory/log，sdb: inventory 搜索索引），并自动初始化序列号（`__initseqid`）
3. 在 user 服务中为服务添加用户并分配角色（admin/purchaser/salesperson）
4. 端侧安装应用时下载 `ui/` 压缩包，入口 `index.html`

## 数据库

| 库 | 类型 | 表 |
| --- | --- | --- |
| inventory | rdb | products, suppliers, customers, categories, stock_ops |
| inventory | sdb | products/suppliers/customers/categories 搜索索引 |
| log | rdb | purchase_orders, purchase_items, sales_orders, sales_items, sales_stats |

库存流水 stock_ops：`(orderId, productId, type)` 唯一，type = PUR 采购入库 / SAL 销售出库 / RET 退货回补 / ADJ 盘点调整；销售明细快照成本价（costPrice）用于毛利统计。

## 业务规则（v0.2）

- 库存变更全部走流水：新建商品带初始库存（ADJ）、采购完成入库（PUR）、销售加项扣减（SAL）、移除/取消回补（RET）、盘点调整（ADJ）；**编辑商品不允许直接改库存**，需用盘点调整。
- 采购完成时按移动加权平均更新商品成本价：`costPrice=(costPrice*stock+subTotal)/(stock+qty)`，保证毛利统计准确。
- 幂等保护：销售/采购单 completeOrder、cancelOrder 均要求 status=0，重复操作返回 EXISTS，避免重复加库存/重复累计报表。
- 销售加项时校验库存充足（expect:true），库存不足直接报错，防止负库存。

## 接口一览

- product: list / search / create / update / delete / get / adjustStock / stockOps
- purchase: createOrder / setSupplier / addItem / removeItem / completeOrder / cancelOrder / listOrders / getOrder
- sales: createOrder / setCustomer / addItem / removeItem / completeOrder / cancelOrder / listOrders / getOrder
- category / supplier / customer: list / search / create / update / delete
- report: stats / salesTrend / topProducts / profit / lowStockList
