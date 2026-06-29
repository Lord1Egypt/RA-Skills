# Odoo 19 销售 / 采购 / 库存 模型与 XML-RPC API 速查

> 源码核对：`~/workspace/study/odoo/odoo-19.0+e.20260501/odoo/addons/`（sale / purchase / purchase_stock / stock）。

## ⚠️ 三模块共同的 v19 字段坑（最易错）

1. **销售行**：单位 `product_uom_id`（非 product_uom）、税 `tax_ids`（非 tax_id）、数量 `product_uom_qty`。
2. **采购行**：单位 `product_uom_id`、税 `tax_ids`（非 taxes_id）、数量 **`product_qty`**（注意和销售不同！）。
3. **state 都无 `done`**：销售 draft/sent/sale/cancel；采购 draft/sent/to approve/purchase/cancel；锁定都用 `locked` 布尔（旧 done 态废弃）。
4. **库存**：v19 删了 `move_ids_without_package`（用 `move_ids`）；完成量是 `quantity`（非 qty_done）。
5. **确认是写操作有副作用**：sale `action_confirm` / purchase `button_confirm` 会自动建交货/入库单（stock.picking）。技能里 confirm/cancel/validate/invoice 执行前应向用户确认。

---

## 一、销售 sale.order

`_order='date_order desc, id desc'`。state：`draft`(报价单)/`sent`(已发送)/`sale`(销售订单)/`cancel`。

| 字段 | 含义 |
|---|---|
| name(单号,自动) · partner_id(客户,required) · user_id(销售员) · date_order · state · amount_untaxed/amount_tax/amount_total · invoice_status(`no`/`to invoice`含空格/`invoiced`/`upselling`) · order_line · client_order_ref · locked · picking_ids(sale_stock) · invoice_ids | |

**sale.order.line**：product_id · name(Text) · **product_uom_qty**(数量) · **product_uom_id** · price_unit · discount · **tax_ids** · qty_delivered · qty_invoiced · price_subtotal · display_type(`line_section`/`line_subsection`/`line_note`/False)。

**方法**：`action_confirm`(draft→sale,装 sale_stock 建交货单) · `action_cancel` · `action_draft` · `_create_invoices`(返 account.move ids) · `action_lock`/`action_unlock`。

**创建**（最小 partner_id + order_line）：
```python
call('sale.order','create',[{'partner_id':7,'order_line':[
  (0,0,{'product_id':25,'product_uom_qty':2}),                    # 价/税自动算
  (0,0,{'product_id':30,'product_uom_qty':5,'price_unit':88.0})]}])
```
**查询**：我的 `('user_id','=',uid)`；报价单 `('state','in',['draft','sent'])`；已确认 `('state','=','sale')`；待开票 `('invoice_status','=','to invoice')`。

---

## 二、采购 purchase.order

`_order='priority desc, id desc'`。state：`draft`(询价 RFQ)/`sent`/`to approve`(待批准)/`purchase`(采购订单)/`cancel`。

| 字段 | 含义 |
|---|---|
| name · partner_id(供应商,required) · user_id(采购员) · date_order · state · amount_total · invoice_status(`no`/`to invoice`/`invoiced`) · receipt_status(`pending`/`partial`/`full`,需 purchase_stock) · order_line · partner_ref · note(非 notes) · locked · picking_ids · invoice_ids | |

**purchase.order.line**：product_id · name(Text) · **product_qty**(数量,非 product_uom_qty) · qty_received(实物产品只读) · **product_uom_id** · price_unit · **tax_ids** · price_subtotal · date_planned · display_type。

**方法**：`button_confirm`(draft→purchase 或 to approve) · `button_approve`(to approve→purchase) · `button_cancel` · `button_draft` · `action_create_invoice`(生成供应商账单) · `button_lock`/`button_unlock`。
**确认副作用**：装 purchase_stock 时 button_approve 自动建入库单 stock.picking；qty_received 实物产品由入库 done 自动算，不可直接写。**删除前必须先 button_cancel**。

**创建**（partner_id + order_line，行用 product_qty）：
```python
call('purchase.order','create',[{'partner_id':7,'order_line':[
  (0,0,{'product_id':16,'product_qty':10,'price_unit':50.0}),
  (0,0,{'product_id':17,'product_qty':5})]}])     # 价由供应商价表算
```
**查询**：询价单 `('state','=','draft')`；已确认 `('state','=','purchase')`；待批准 `('state','=','to approve')`；待收货 `('receipt_status','in',['pending','partial'])`。

---

## 三、库存 stock

### 查产品库存（最简：product.product 字段，别手动聚合 quant）
`qty_available`(在手) · `free_qty`(可用=在手-预留) · `virtual_available`(预测=在手-待出+待入) · `incoming_qty`(待入) · `outgoing_qty`(待出)。都是 compute+search，可 read/domain，**不能 read_group 聚合**。
**限仓库/库位走 context**（不是 domain）：
```python
call('product.product','read',[[pid]],{'fields':['free_qty','qty_available','virtual_available'],
  'context':{'warehouse_id':wh_id}})   # 或 {'location': loc_id}；不传=所有 internal 库位
```
要按库位拆：read_group `stock.quant` 的 `quantity:sum`+`reserved_quantity:sum`（这俩可聚合），domain `location_id.usage='internal'`，客户端相减得可用量。

### stock.picking（出入库单）
state 6 值：`draft`/`waiting`(等上游)/`confirmed`(待预留,UI 显示 Waiting)/`assigned`(就绪)/`done`/`cancel`。
字段：name · partner_id · picking_type_id · **picking_type_code**(`incoming`收货/`outgoing`发货/`internal`调拨) · location_id/location_dest_id · scheduled_date · state · origin · **move_ids**(明细)。
**stock.move**：product_id · **product_uom_qty**(需求) · **quantity**(完成,非 qty_done) · state(7 值,多 partially_available)。

**方法**：`action_assign`(预留库存→assigned) · `button_validate`(验证过账,**必传 context skip_backorder=True 否则返回向导 dict**) · `action_cancel`。
**RPC 验证标准三步**：① action_assign 预留 → ② 写每条 move `quantity`=product_uom_qty + `picked`=True → ③ button_validate with `context={'skip_backorder':True,'picking_ids_not_to_backorder':[id]}`。

**查询**：待处理 `('state','in',['waiting','confirmed','assigned'])`；收货 `('picking_type_code','=','incoming')`；某库位 `('location_id','child_of',loc_id)`。

### 库位/仓库
`stock.location`（usage: supplier/view/internal/customer/inventory/production/transit；查实体库位 usage='internal'）；`stock.warehouse`（name/code/lot_stock_id）。

---

## 四、XML-RPC 示例（要点）

```python
def call(m,meth,a,kw=None): return models.execute_kw(db,uid,pw,m,meth,a,kw or {})

# 销售：建报价单→确认→生成发票
oid = call('sale.order','create',[{'partner_id':7,'order_line':[(0,0,{'product_id':25,'product_uom_qty':2})]}])
call('sale.order','action_confirm',[[oid]])
inv_ids = call('sale.order','_create_invoices',[[oid]])

# 采购：建询价→确认（自动建入库单）
pid = call('purchase.order','create',[{'partner_id':7,'order_line':[(0,0,{'product_id':16,'product_qty':10,'price_unit':50})]}])
call('purchase.order','button_confirm',[[pid]])

# 库存：查库存 + 验证出入库
call('product.product','read',[[25]],{'fields':['free_qty','qty_available']})
call('stock.picking','action_assign',[[picking_id]])
mv = call('stock.move','search_read',[[('picking_id','=',picking_id),('state','not in',['done','cancel'])]],{'fields':['product_uom_qty']})
for m in mv: call('stock.move','write',[[m['id']],{'quantity':m['product_uom_qty'],'picked':True}])
call('stock.picking','button_validate',[[picking_id]],{'context':{'skip_backorder':True,'picking_ids_not_to_backorder':[picking_id]}})
```
