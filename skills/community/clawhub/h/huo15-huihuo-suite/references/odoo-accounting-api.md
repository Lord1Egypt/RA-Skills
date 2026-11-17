# Odoo 19 会计模块模型与 XML-RPC API 速查

> 源码核对：`~/workspace/study/odoo-19.0+e.20260501/odoo/addons/account/models/`

## ⚠️ v19 字段坑（最易错）

1. **state 只有 3 值**：`draft`(草稿) / `posted`(已过账) / `cancel`(已作废)。**无 done**。
2. **move_type 决定一切**：`out_invoice`=客户发票 / `in_invoice`=供应商账单 / `out_refund`=客户退款 / `in_refund`=供应商退款 / `entry`=日记账 / `out_receipt`=销售收据 / `in_receipt`=采购收据。
3. **payment_state**：`not_paid`/`in_payment`/`paid`/`partial`/`reversed`/`blocked`/`invoicing_legacy`。`invoicing_legacy` 是旧版遗留，不用管。
4. **金额全是 compute/store**：`amount_untaxed`/`amount_tax`/`amount_total`/`amount_residual` 不可直接 write，由 `invoice_line_ids` 自动算。
5. **invoice_line_ids ≠ line_ids**：`invoice_line_ids` 是 `line_ids` 的子集（只含产品行/分节行/注释行，domain `[('display_type','in',('product','line_section','line_subsection','line_note'))]`）。
6. **过账是写操作**：`action_post`(draft→posted) 会生成凭证行（account.move.line），有副作用。
7. **account.payment 创建**：需 `payment_type`(inbound=收/outbound=付) + `partner_type`(customer/supplier) + `amount` + `partner_id` + `journal_id`；创建后需 `action_post` 过账。

---

## 一、account.move（发票/账单/日记账）

`_order='date desc, name desc, invoice_date desc, id desc'`。

### 核心字段

| 字段 | 含义 |
|---|---|
| name(单号,compute自动) · ref(参考号) · date(记账日期,Date) · state(draft/posted/cancel) · move_type(见上) · payment_state(见上) | 标识/状态 |
| partner_id(客户/供应商) · journal_id(账簿,required) · company_id · currency_id | 关联 |
| invoice_date(发票/账单日期,Date) · invoice_date_due(到期日,Date) · delivery_date(交货日) | 日期 |
| invoice_payment_term_id(付款条件 m2o account.payment.term) · partner_bank_id(收款银行账户) · fiscal_position_id(税位) | 付款/税 |
| amount_untaxed(未税,compute) · amount_tax(税额,compute) · amount_total(总额,compute) · amount_residual(待付,compute) | 金额 |
| line_ids(全部凭证行) · invoice_line_ids(发票行=line_ids子集) · narration(备注,Html) | 明细 |
| reversed_entry_id(反向关联) · auto_reverse(自动反向) · recurring(self-recurring) | 冲销/周期 |

### 方法

| 方法 | 说明 |
|---|---|
| `action_post` | 过账 draft→posted，生成凭证行 |
| `button_draft` | 回草稿 posted/cancel→draft |
| `button_cancel` | 作废 →cancel |
| `action_reverse` | 建反向发票（退款/信用票据），返回新 move id |
| `action_register_payment` | 打开登记付款向导（UI 用，API 不直接用） |

### 创建客户发票

```python
call('account.move', 'create', [{
    'move_type': 'out_invoice',
    'partner_id': 7,
    'invoice_line_ids': [
        (0, 0, {'product_id': 25, 'quantity': 2}),           # 价/税由 product 自动算
        (0, 0, {'product_id': 30, 'quantity': 5, 'price_unit': 88.0}),
    ],
}])
```

### 创建供应商账单

把 `move_type` 换成 `'in_invoice'`，其余一样。

### 查询

- 我的发票：`('move_type','in',('out_invoice','out_refund')), ('create_uid','=',uid)`
- 未付款：`('payment_state','in',('not_paid','partial'))`
- 供应商账单：`('move_type','in',('in_invoice','in_refund'))`
- 草稿：`('state','=','draft')`；已过账：`('state','=','posted')`

---

## 二、account.move.line（凭证行）

发票行（invoice_line_ids）的关键字段：

| 字段 | 含义 |
|---|---|
| product_id(产品 m2o) · name(描述,Text) · quantity(数量) · price_unit(单价) | 基础 |
| tax_ids(税, m2m account.tax) · account_id(科目 m2o account.account, compute from product) | 税/科目 |
| price_subtotal(小计,compute) · price_total(含税,compute) · amount_currency | 金额 |
| display_type(line_section/line_subsection/line_note/product) | 行类型 |
| analytic_distribution(分析会计,Json) · partner_id | 分析 |

---

## 三、account.journal（账簿）

`_order='sequence, type, code'`。

| 字段 | 含义 |
|---|---|
| name(名称) · code(代码,size=5) · type(sale/purchase/cash/bank/credit/general) · active | 基础 |
| default_account_id(默认科目 m2o account.account) · suspense_account_id(银行暂记科目) · bank_account_id(银行账户, type=bank) | 科目 |

type 含义：
- **sale**：客户发票账簿
- **purchase**：供应商账单账簿
- **bank**：银行账簿（需配 bank_account_id）
- **cash**：现金账簿
- **credit**：信用卡账簿
- **general**：通用/日记账

---

## 四、account.account（会计科目）

`_order='code, placeholder_code'`。

| 字段 | 含义 |
|---|---|
| name(名称) · code(代码) · account_type(见下) · active · reconcile(可对账) | 基础 |
| tax_ids(默认税, m2m) · currency_id(币种) · company_ids(公司) | 关联 |
| internal_group(equity/asset/liability/income/expense/off, compute from account_type) | 分组 |

account_type 取值：
- **asset_receivable**(应收) / **asset_cash**(银行现金) / **asset_current**(流动资产) / **asset_non_current**(非流动) / **asset_prepayments**(预付) / **asset_fixed**(固定资产)
- **liability_payable**(应付) / **liability_credit_card**(信用卡) / **liability_current**(流动负债) / **liability_non_current**(非流动负债)
- **equity**(权益) / **equity_unaffected**(本年利润)
- **income**(收入) / **income_other**(其他收入)
- **expense**(费用) / **expense_other**(其他费用) / **expense_depreciation**(折旧) / **expense_direct_cost**(成本)
- **off_balance**(表外)

---

## 五、account.payment（付款）

`_order="date desc, name desc"`。

| 字段 | 含义 |
|---|---|
| name(单号,compute) · date(日期,Date,required) · state(draft/in_process/paid/canceled/rejected, compute) · amount(金额,Monetary) · memo(备注) · payment_reference(付款参考) | 基础 |
| payment_type(inbound=收 / outbound=付, required) · partner_type(customer=客户 / supplier=供应商, required) | 类型 |
| partner_id(客户/供应商, required) · journal_id(账簿, required) · currency_id(币种) | 关联 |
| payment_method_line_id(付款方式 m2o) · outstanding_account_id(暂记科目, compute) · destination_account_id(目标科目) | 方式/科目 |
| is_reconciled(已对账, compute) · is_matched(已匹配银行流水, compute) | 状态 |

### 方法

| 方法 | 说明 |
|---|---|
| `action_post` | 过账（draft→in_process/paid，生成 account.move 凭证） |
| `action_draft` | 回草稿 |
| `action_cancel` | 取消 |
| `action_is_sent` | 标记已发送 |

### 创建付款

```python
call('account.payment', 'create', [{
    'payment_type': 'inbound',       # 收款
    'partner_type': 'customer',
    'partner_id': 7,
    'amount': 5000.0,
    'journal_id': 3,                  # bank/cash 账簿
    'date': '2026-08-01',
    'memo': '客户付款',
}])
# 创建后需 action_post
call('account.payment', 'action_post', [[payment_id]])
```

### 查询

- 收款：`('payment_type','=','inbound')`
- 付款：`('payment_type','=','outbound')`
- 草稿：`('state','=','draft')`
- 已付款：`('state','=','paid')`

---

## 六、account.payment.term（付款条件）

| 字段 | 含义 |
|---|---|
| name(名称) · line_ids(付款明细行) | 基础 |

创建发票时可指定 `invoice_payment_term_id`，系统按条件自动算 `invoice_date_due`。

---

## 脚本对应关系

| 脚本命令 | 模型方法 |
|---|---|
| `accounting.py invoices` | search_read account.move |
| `accounting.py show` | read account.move + account.move.line |
| `accounting.py add` | create account.move (out_invoice) |
| `accounting.py bill` | create account.move (in_invoice) |
| `accounting.py post` | action_post |
| `accounting.py cancel` | button_cancel |
| `accounting.py draft` | button_draft |
| `accounting.py journals` | search_read account.journal |
| `accounting.py accounts` | search_read account.account |
| `accounting.py pay` | create account.payment + action_post |
| `accounting.py payments` | search_read account.payment |
