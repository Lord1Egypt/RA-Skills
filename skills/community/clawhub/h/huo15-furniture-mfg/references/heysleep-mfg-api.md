# 和栖家居（test.heysleep.cn）制造域 API 知识沉淀

> 2026-06-13 对 test 库（辉火云企业套件 v19 企业版，295 模块）fields_get + 实数据验证。
> 改任何 ORM 调用前先对照本文，别凭记忆写字段。

## 环境

- URL `https://test.heysleep.cn`，db `test`，XML-RPC `/xmlrpc/2/*` 与 JSON-RPC `/jsonrpc` 均可用
- 业务规模（验证当日）：SO 702 / MO 475 / QC 470 / picking 608 / PO 84 / 产品模板 359 / 内部用户 28
- 装机特征：MRP + quality_mrp + stock_barcode 全开；**mrp.workorder=0、BOM 仅 8、workcenter 仅 1** —— 工单/工序/标准 BOM 未启用

## 链路模型（和栖按单生产）

```
sale.order ──(mrp.production.origin = so.name，覆盖 435/475)──▶ mrp.production
    │                                                             │
    └─(stock.picking.sale_id / origin)──▶ stock.picking ◀─(picking_ids m2m)─┘
                                              │
quality.check.production_id / picking_id ◀────┘   (质检挂 MO 或出库单)
```

## 已踩坑（全部实测验证）

### 1. Odoo 19 `name_search` 参数改名

`args=` → **`domain=`**。XML-RPC 传 `args` 报 `TypeError: BaseModel.name_search() got an unexpected keyword argument 'args'`。

### 2. `quality.check` 状态字段是 `quality_state`

取值 `none`(待检)/`pass`/`fail`。**没有 `state` 字段**（fields_get 验证缺失），按 `state` 查直接 Invalid field。

### 3. 非存储计算字段不能进 `order`

`product.product.qty_available / free_qty / virtual_available` 报
`ValueError: Cannot convert ... to SQL because it is not stored`。取回后本地 sort。

### 4. Odoo 19 `stock.move` 实收字段是 `quantity`

17 以前的 `quantity_done` 已不存在。组件需求 `product_uom_qty`，可供性 `forecast_availability` + `forecast_expected_date`。

### 5. 本库质检单 94% 不挂 `product_id`（27/470）

质检点挂在作业类型上。统计分组用 `title`（实际取值：成品入库质检 438 / 销售出库时质检 21 / 销售出库质检 5），别用 `product_id`。

### 6. 本库 MO 基本不挂 BOM

全库 `stock.move.raw_material_production_id != False` 仅 8 条。`move_raw_ids` 为空是常态，欠料逐项展开要兜底文案；`components_availability_state` 字段本身始终可用（无组件 = available）。

## selection 取值（fields_get 实测）

| 模型.字段 | 取值 |
|---|---|
| sale.order.state | draft / sent / sale / cancel |
| sale.order.delivery_status | pending / started / partial / full |
| sale.order.invoice_status | upselling / invoiced / to invoice / no |
| mrp.production.state | draft / confirmed / progress / to_close / done / cancel |
| mrp.production.components_availability_state | available / expected / late / unavailable |
| mrp.production.reservation_state | confirmed(等待) / assigned(就绪) / waiting(等其他作业) |
| stock.picking.state | draft / waiting / confirmed / assigned / done / cancel |
| quality.check.quality_state | none / pass / fail |
| purchase.order.state | draft / sent / to approve / purchase / cancel |
| purchase.order.receipt_status | pending / partial / full |

## 客户定制字段（huo15_sale_contractt_exchanges + Studio）

| 模型 | 字段 | 含义 |
|---|---|---|
| sale.order | `x_salesperson_user_id` (m2o) | 销售人（区别于标准 user_id） |
| sale.order | `x_follower_user_id` (m2o) | **跟单人**（跟单场景关键字段，实数据在用） |
| sale.order | `x_source_order_ref` (char) | 来源订单号（电商平台单号） |
| sale.order | `x_actual_shipment_time` (datetime) | 实际发货时间 |
| product.* | `x_studio_xinghao` (char) | 型号（如 C3），库存模糊查询第四字段 |

其余 `x_studio_char_field_*` 一批 Studio 匿名字段（sale.order / purchase.order / product 上都有），label 不可读，未接入；接入前先 `fields_get` 看 string。

## P1 写操作与报表（2026-06-13 实测）

### message_post（chatter 留言）

```python
execute_kw(model, "message_post", [[res_id]], {
    "body": "<p>HTML 内容</p>",
    "partner_ids": [partner_id, ...],     # @谁（用户须先 res.users → partner_id）
    "message_type": "comment",
    "subtype_xmlid": "mail.mt_comment",   # comment=通知 followers+@；mt_note=内部备注零通知
})
```

- **返回值是 `[id]` 列表**（XML-RPC 把 mail.message recordset 序列化成 list），取标量再存。
- 误发补救：`unlink("mail.message", id)`，admin 权限可删。

### mail.activity（跟进提醒）

- 必填 `res_model_id`（**ir.model 的 id**，不是模型名字符串）+ `res_id`
- `date_deadline` 是 **Date**（YYYY-MM-DD，不要转 UTC datetime）
- `activity_type_id`：本库 To-Do=4、Call=2、Meeting=3
- 完成走 `action_feedback`（归档非删除）；测试清理可直接 unlink

### 计划日期可写字段

- MO 计划开始：`mrp.production.date_start`（datetime UTC）
- SO 承诺交期：`sale.order.commitment_date`（datetime UTC）

### QWeb PDF 报表渲染（XML-RPC 做不到）

走 web session 两步（report.py 已封装）：
1. `POST /web/session/authenticate`（json：db/login/password）拿 session cookie
2. `GET /report/pdf/<report_name>/<res_id>`，校验响应以 `%PDF` 开头

本库关键 report_name（ir.actions.report 实测）：

| 别名 | 模型 | report_name |
|---|---|---|
| contract | sale.order | huo15_sale_contract_report.report_sale_contract_quotation |
| contract | stock.picking | huo15_sale_contract_report.report_sale_contract |
| contract-seller | sale.order | huo15_sale_contract_report.report_sale_contract_quotation_seller |
| quote | sale.order | sale.report_saleorder |
| label | picking/MO | huo15_product_label_a5.report_package_label |
| workorder | mrp.production | huo15_product_label_a5.report_production_work_order |
| delivery | stock.picking | huo15_product_label_a5.report_delivery_slip |

## P3 行业深化字段（2026-06-13 实测）

### 拍照质检（huo15_quality_multi_picture，已装）

- `quality.check.picture_ids`：m2m → ir.attachment（rel 表 huo15_quality_check_picture_rel）
- 挂图：`ir.attachment` create（name/datas base64/mimetype + **res_model='quality.check', res_id=qc_id**——归属必须直接挂质检单，模块 wizard 也是这么修正的）→ `picture_ids: [(4, att_id)]`
- 判定：`do_pass()` / `do_fail()` 记录级方法（odoo.call）；判定后 quality_state 不可随意撤销

### 非标定制（sale_product_custom，已装）

- `sale.order.line`：`custom_length/custom_width/custom_height`（cm，Float）+ `custom_material`（Char 主料）+ `is_custom_product`（Bool）
- 实测：draft SO 写这些字段会触发模块定价逻辑（非标尺寸自动算价，1 件 2000×2200×280 算出 ¥12,480）
- 全库 is_custom_product 行为 0——客户没用起来（手动建"(非标-...)"产品替代），对话流是把标准玩法用起来

### 渠道判定

- `x_source_order_ref`（来源订单号）：64% 确认订单有值（电商平台单）；69 开头 19 位 = 抖音系单号
- **huo15_xhs_shop（x_xhs_order_id）/ huo15_douyin_ecommerce（douyin_order_id）模块在 test 库未安装**——仓库有代码但未部署，查这两个字段会 Invalid field；装上后才能精确分平台

## 后端定制动作 RPC 速查（hey_smart_addons · 实现 P4/P5 时用）

> 这些是后端定制模块提供的可调用业务动作；实现操作功能时优先复用，仍走确认制包装。
> 完整规划与优先级见 [operations-roadmap.md](../../docs/operations-roadmap.md) §二·五。

```python
# 企微发文本（晨报/预警/留言 后端通道；userid 须 res.users.wecom_userid）
odoo.execute_kw("huo15.wecom.api","send_text",[[], "内容"])  # 实际 send_text(userids, content)，单参形式按模型签名
# 企微 OA 审批：建请求 → 提交（AI 只发起，人在企微批）
sp = odoo.create("huo15.wecom.approval.request", {"name":..., "template_id":..., "apply_data":{...}})
odoo.call("huo15.wecom.approval.request","action_submit_to_wecom",[sp])     # 回查 action_sync_from_wecom
# 文本自动建客户档案（姓名/电话/地址智能解析）
pid = odoo.create("res.partner", {"autofill_text":"张三 13800000000 佛山顺德…"})
odoo.call("res.partner","action_apply_autofill_text",[pid])
# 小红书聚光营销数据同步
odoo.call("xhs.spotlight.account","sync_balance",[acc_id])      # / sync_dashboard_data
# 品牌档案（报价带 Logo/付款码/地址）
odoo.search_read("product.brand",[],["name","company_name","bank_name"])
# 批量序列号
odoo.call("stock.lot","generate_lot_names",[lot_id, first_lot, count])
```

注意：企微动作依赖 `huo15.wecom.api` 配置（corp_id/agent_id/secret）+ 用户 `wecom_userid`；调用前 fields_get/读配置确认已就绪，未配置会 UserError。

## 单号格式

`SO-YYMMDD-NNN` / `MO-YYMMDD-NNN` / `DO-YYMMDD-NNN` / `PO-YYMMDD-NNN` / `QC00NNN`。
日期段是建单日，模糊查询用尾段数字也能命中（ilike）。

## 时区

所有 Datetime UTC 存储。本地（Asia/Shanghai）日界换算用 `odoo_utils.day_range_utc(offset)`；
"今天"的统计如果直接拿 UTC 日期切，早上 8 点前的单会落到昨天。
