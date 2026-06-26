---
name: huo15-odoo19-module-dev
version: 1.0.0
slug: odoo19-module-dev
description: Odoo 19 模块开发技能 — 从项目结构、模型定义、视图设计到业务逻辑，完整覆盖 Odoo 19 模块开发全流程
aliases:
  - Odoo19模块开发
  - Odoo19开发
  - Odoo模块
  - odoo module
  - odoo19
---

# SKILL.md — huo15-odoo19-module-dev

## 触发条件

用户提到以下内容时激活本技能：
- Odoo19 模块开发
- 开发 Odoo 模块
- Odoo 模型/视图/业务逻辑
- Odoo manifest / `__manifest__.py`
- Odoo 插件安装
- Odoo XML/JS/CSS 资源

---

## Odoo 模块开发核心概念

### 模块结构（标准化）

```
my_module/
├── __init__.py          # 模块导入声明
├── __manifest__.py      # 元数据清单（必需）
├── models/
│   ├── __init__.py
│   └── models.py         # 所有模型定义
├── views/
│   ├── views.xml         # 视图定义
│   └── templates.xml     # Web 模板
├── security/
│   └── ir.model.access.csv
├── data/
│   └── demo.xml          # 演示数据
├── controllers/
│   ├── __init__.py
│   └── controllers.py    # HTTP 路由
├── wizards/
│   ├── __init__.py
│   └── wizard.py         # 向导/向导模型
└── static/
    ├── src/xml/          # JS/QWeb 模板
    ├── src/js/           # JavaScript
    └── src/css/          # CSS
```

### `__manifest__.py` 最小模板

```python
{
    'name': "我的模块",
    'version': '1.0.0',
    'summary': '模块一句话描述',
    'description': """
        模块详细说明（多行）
    """,
    'category': 'Hidden',  # Hidden/Productivity/Manufacturing/...
    'author': '火一五信息科技',
    'website': 'https://www.huo15.com',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'installable': True,
    'application': False,
}
```

---

## 模型开发（Model）

### 基本模型模板

```python
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MyModel(models.Model):
    _name = 'my.model'           # 必填，点分格式
    _description = '我的模型'    # 模型描述
    _order = 'sequence, id'      # 默认排序
    _inherit = []                # 继承，可为空列表

    name = fields.Char(
        string='名称',
        required=True,
        index=True,
        help='这是帮助文本'
    )
    
    active = fields.Boolean(
        string='活跃',
        default=True,
        index=True
    )
    
    description = fields.Text(string='描述')
    
    date = fields.Date(string='日期')
    datetime = fields.Datetime(string='时间')
    
    # 关联字段
    partner_id = fields.Many2one(
        'res.partner',
        string='客户',
        index=True,
        ondelete='cascade'  # cascade/restrict/set null
    )
    
    line_ids = fields.One2many(
        'my.model.line',
        'parent_id',
        string='明细行'
    )
    
    # 计算字段
    amount_total = fields.Float(
        string='合计',
        compute='_compute_amount',
        store=True  # 存储以便搜索
    )
    
    # 状态字段
    state = fields.Selection([
        ('draft', '草稿'),
        ('confirm', '已确认'),
        ('done', '完成'),
        ('cancel', '已取消'),
    ], string='状态', default='draft', index=True)
    
    # SQL 约束
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', '名称不能重复！'),
    ]
    
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name:
                raise ValidationError('名称不能为空')
    
    @api.depends('line_ids.price', 'line_ids.qty')
    def _compute_amount(self):
        for rec in self:
            rec.amount_total = sum(
                line.price * line.qty 
                for line in rec.line_ids
            )
```

### 关系字段对比

| 字段类型 | 语法 | 用途 |
|---------|------|------|
| Many2one | `fields.Many2one('other.model', ...)` | 多选一（外键） |
| One2many | `fields.One2many('other.model', 'rel_field', ...)` | 一对多 |
| Many2many | `fields.Many2many('other.model', ...)` | 多对多 |
| Reference | `fields.Reference(...)` | 可变模型引用 |

### 常用字段参数

```python
# 通用参数
string='标签'           # UI 显示名
required=True          # 必填
index=True             # 数据库索引
help='提示文本'         # 鼠标悬停提示
default=...             # 默认值
copy=True/False         # 复制时是否带值
readonly=True          # 只读
store=True             # 存储到数据库（计算字段）
tracking=True           # 变更追踪（邮件通知）

# Char
size=200               # 最大长度（旧版，新版已废弃）
translate=True          # 允许翻译

# Numeric
digits=(16, 2)         # 总位数，小数位

# Date/Datetime
calendar='gregorian'   # 日历类型

# Selection
selection=[('a','A'),('b','B')]  # 选项列表
```

### 核心 API 方法

```python
# 创建
record = self.env['my.model'].create({'name': 'value'})

# 搜索
records = self.env['my.model'].search([
    ('active', '=', True),
    ('name', 'like', 'test%'),
])

# 读取
record.read(['name', 'active'])
record.mapped('partner_id.name')  # 提取字段

# 写入
record.write({'name': 'new name'})

# 删除
record.unlink()

# 复制
record.copy()

# 过滤
filtered = records.filtered(lambda r: r.active)

# 排序
sorted_records = records.sorted(key=lambda r: r.create_date)
```

### 模型方法覆盖

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    # 覆盖 create 方法
    @api.model
    def create(self, vals):
        # 添加默认值或预处理
        vals['client_order_ref'] = vals.get('name', '')
        return super().create(vals)
    
    # 覆盖 write 方法
    def write(self, vals):
        # 业务逻辑
        if 'state' in vals and vals['state'] == 'sale':
            self.mapped('order_line').write({'state': 'sale'})
        return super().write(vals)
    
    # 按钮方法
    def action_confirm(self):
        for order in self:
            if not order.partner_id:
                raise ValidationError('请先选择客户')
            order.write({'state': 'sale'})
        return True
    
    # 动作返回
    def action_view_invoice(self):
        # 返回视图
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.invoice_ids.ids)],
        }
```

---

## 视图开发（Views）

### Window Action + Menu

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- 窗口动作 -->
    <record id="action_my_model" model="ir.actions.act_window">
        <field name="name">我的模型</field>
        <field name="res_model">my.model</field>
        <field name="view_mode">tree,form</field>
        <field name="context">{'default_active': True}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                创建您的第一条记录
            </p>
        </field>
    </record>

    <!-- 菜单 -->
    <menuitem id="menu_my_model"
              name="我的模块"
              action="action_my_model"
              parent='menu_root'     <!-- 父菜单 -->
              sequence="10"/>
</odoo>
```

### Tree（列表）视图

```xml
<tree>
    <field name="sequence" widget="handle"/>  <!-- 拖拽排序 -->
    <field name="name"/>
    <field name="partner_id"/>
    <field name="date"/>
    <field name="amount_total" sum="合计"/>  <!-- sum/x editable 属性 -->
    <field name="state" widget="badge" decoration-success="state=='done'"/>
    <field name="active" invisible="1"/>
    <!-- 按钮 -->
    <button name="action_confirm" type="object" icon="fa-check" string="确认"/>
</tree>
```

### Form（表单）视图

```xml
<form>
    <sheet>
        <!-- 头部 -->
        <div class="oe_title">
            <h1>
                <field name="name" placeholder="名称..."/>
            </h1>
        </div>
        
        <group>
            <group string="基本信息">
                <field name="partner_id"/>
                <field name="date"/>
                <field name="state"/>
            </group>
            <group string="金额">
                <field name="amount_total" readonly="1"/>
            </group>
        </group>
        
        <!-- Notebook 分页 -->
        <notebook>
            <page string="明细行" name="lines">
                <field name="line_ids">
                    <tree editable="bottom">  <!-- bottom/top -->
                        <field name="product_id"/>
                        <field name="qty" sum="数量"/>
                        <field name="price" sum="单价"/>
                        <field name="subtotal" sum="小计"/>
                    </tree>
                </field>
            </page>
            <page string="备注" name="notes">
                <field name="description"/>
            </page>
        </notebook>
    </sheet>
</form>
```

### 搜索视图

```xml
<search>
    <field name="name" string="名称" filter_domain="[('name','ilike',self)]"/>
    <field name="partner_id" string="客户" operator='child_of'/>
    <field name="date" string="日期"/>
    
    <filter string="活跃" name="active" domain="[('active','=',True)]"/>
    <filter string="已确认" name="confirmed" domain="[('state','=','confirm')]"/>
    
    <separator/>
    <filter string="本月" name="this_month"
            domain="[('date','>=', (context_today() + relativedelta(day=1)).strftime('%Y-%m-%d'))]"/>
    
    <group expand="0" string="分组">
        <filter string="客户" name="partner" context="{'group_by': 'partner_id'}"/>
        <filter string="状态" name="state" context="{'group_by': 'state'}"/>
        <filter string="日期" name="date" context="{'group_by': 'date:month'}"/>
    </group>
</search>
```

### 看板视图（Kanban）

```xml
<kanban class="oe_kanban_small_column" 
        default_group_by="state"
        records_draggable="1">
    <templates>
        <t t-name="kanban-box">
            <div class="oe_kanban_card">
                <div class="oe_kanban_card_header">
                    <strong><field name="name"/></strong>
                </div>
                <field name="partner_id"/>
                <field name="amount_total"/>
                <div class="oe_kanban_footer">
                    <field name="state" widget="badge"/>
                </div>
            </div>
        </t>
    </templates>
</kanban>
```

---

## 权限控制（ACL）

### `ir.model.access.csv`

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,base.group_user,1,1,1,1
access_my_model_manager,my.model.manager,model_my_model,,1,1,1,1
```

**组ID选项：**
- `base.group_user` — 普通用户
- `base.group_portal` — 门户用户
- `base.group_public` — 匿名访客
- 空 = 所有用户

**权限位：** `perm_read,perm_write,perm_create,perm_unlink` — 1=允许，0=拒绝

---

## 业务逻辑（Business Logic）

### 按钮与动作

```python
class MyModel(models.Model):
    _name = 'my.model'
    
    def action_draft(self):
        """重置为草稿"""
        self.write({'state': 'draft'})
        return True
    
    def action_confirm(self):
        """确认"""
        for rec in self:
            if rec.state != 'draft':
                raise UserError('只能确认草稿状态的记录')
            rec.write({'state': 'confirm'})
        return True
    
    def action_done(self):
        """完成"""
        self.write({'state': 'done'})
        # 触发其他逻辑
        self.mapped('line_ids').write({'done': True})
        return True
    
    def action_cancel(self):
        """取消"""
        for rec in self:
            if rec.invoice_count > 0:
                raise UserError('有关联发票，不能取消')
        self.write({'state': 'cancel'})
        return True
    
    def unlink(self):
        """删除前检查"""
        for rec in self:
            if rec.state == 'done':
                raise UserError('不能删除已完成的记录')
        return super().unlink()
```

### 计算字段

```python
from odoo import api

class MyModel(models.Model):
    _name = 'my.model'
    
    price = fields.Float(string='单价')
    qty = fields.Float(string='数量')
    tax = fields.Float(string='税率')
    
    subtotal = fields.Float(
        compute='_compute_subtotal',
        store=True,
        string='小计'
    )
    
    total = fields.Float(
        compute='_compute_total',
        store=True,
        string='含税合计'
    )
    
    @api.depends('price', 'qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.price * rec.qty
    
    @api.depends('subtotal', 'tax')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.subtotal * (1 + rec.tax / 100)
    
    @api.onchange('price', 'qty')
    def _onchange_price_qty(self):
        """当单价或数量变化时触发"""
        if self.price and self.qty:
            self.subtotal = self.price * self.qty
        return {
            'warning': {
                'title': '提示',
                'message': '小计已自动更新'
            }
        }
```

### 约束验证

```python
from odoo.exceptions import ValidationError, UserError

class MyModel(models.Model):
    _name = 'my.model'
    
    date_start = fields.Date(string='开始日期')
    date_end = fields.Date(string='结束日期')
    
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_end and rec.date_start > rec.date_end:
                raise ValidationError(
                    '开始日期不能晚于结束日期！'
                )
    
    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount < 0:
                raise ValidationError('金额不能为负数')
```

---

## 服务端动作（Server Action）

```xml
<record id="action_mass_confirm" model="ir.actions.server">
    <field name="name">批量确认</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="state">code</field>
    <field name="code">
records = env['my.model'].browse(context.get('active_ids'))
records.action_confirm()
    </field>
</record>

<record id="action_mass_cancel" model="ir.actions.server">
    <field name="name">批量取消</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="state">code</field>
    <field name="code">
records = env['my.model'].browse(context.get('active_ids'))
for rec in records.filtered(lambda r: r.state == 'draft'):
    rec.action_cancel()
    </field>
</record>
```

---

## 自动动作（Automated Actions / Cron）

```python
class MyModel(models.Model):
    _name = 'my.model'
    
    @api.model
    def _cron_check_overdue(self):
        """定时任务：检查逾期"""
        overdue = self.search([
            ('state', 'in', ['draft', 'confirm']),
            ('date_end', '<', fields.Date.today())
        ])
        for rec in overdue:
            rec.write({'state': 'overdue'})
            # 发送通知邮件
            rec._send_overdue_notification()
    
    def _send_overdue_notification(self):
        """发送逾期通知"""
        self.ensure_one()
        template = self.env.ref('my_module.email_template_overdue')
        if template:
            template.send_mail(self.id, force_send=True)
```

---

## 权限记录规则（Record Rule）

```xml
<!-- security/ir.model.access.csv 同级 security/record_rules.xml -->
<record id="my_model_rule" model="ir.rule">
    <field name="name">只能查看自己的记录</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
    <field eval="[('create_uid', '=', user.id)]" name="domain_force"/>
    <!-- perm_read/perm_write/perm_create/perm_unlink -->
</record>
```

---

## 开发工作流

### 1. 创建模块骨架

```bash
# 进入 addons 目录
cd ~/.openclaw/workspace/huo15-odoo19-docker/custom_src/odoo/addons

# 创建模块目录
mkdir -p my_module/{models,views,security,data,controllers,wizards,static/src/js,static/src/xml}

# 创建 __init__.py
echo 'from . import models' > my_module/__init__.py
echo 'from . import controllers' >> my_module/__init__.py
echo 'from . import wizards' >> my_module/__init__.py

# 创建 models/__init__.py
echo 'from . import models' > my_module/models/__init__.py

# 创建其他 __init__.py
touch my_module/controllers/__init__.py
touch my_module/wizards/__init__.py
```

### 2. 编写模块清单

```python
# my_module/__manifest__.py
{
    'name': '我的模块',
    'version': '1.0.0',
    'author': '火一五信息科技',
    'category': 'Productivity',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/demo.xml',
    ],
    'installable': True,
}
```

### 3. 安装与调试

```bash
# 升级模块（在 Odoo 界面或命令行）
# 界面：应用 → 搜索模块 → 升级

# 或通过命令行
docker exec -it odoo19 odoo-bin -u my_module -d huo15 --stop-after-init

# 查看日志
docker logs -f odoo19
```

### 4. 常见问题排查

| 问题 | 排查方法 |
|------|---------|
| 模块不显示 | 检查 `__manifest__.py` 语法；确认在 addons 路径 |
| 视图报错 | 检查 XML 语法；查看 Odoo 日志定位标签 |
| 权限不足 | 检查 `ir.model.access.csv` 配置 |
| 计算字段不更新 | 确认 `store=True`；检查 `@api.depends` 依赖 |
| 按钮无响应 | 检查 `type="object"`；确认方法签名正确 |

---

## 最佳实践

### 代码组织

- **一个模型一个文件**：`models/sale_order.py`
- **常量为类属性**：`STATE = [('draft','草稿'),...]`
- **按钮方法简洁**：委托给 `_action_*` 私有方法

### 命名规范

| 元素 | 规范 | 示例 |
|------|------|------|
| 模块目录 | 下划线 | `my_module` |
| 模型名 | `x_<name>`（避免冲突） | `x_my_model` |
| 字段名 | 下划线 | `partner_id` |
| 方法名 | 下划线 | `_compute_amount` |
| 视图ID | `model_name_view_type` | `my_model_tree` |

### 安全建议

1. **始终使用 `raise UserError`** 而不是 `raise Exception`
2. **`unlink()` 前检查状态**
3. **金额字段用 `Decimal`**，避免浮点精度问题
4. **`sudo()` 只在必要时用**，记录原因

---

## 快速参考

### 模型三要素

```python
class MyModel(models.Model):
    _name = 'x.my.model'      # 点分格式，唯一
    _description = '我的模型'  # 用户可见名称
    _inherit = []              # 继承 ['base.model']
```

### 常用字段速查

```python
fields.Char(size=XX)          # 文本（size已废弃用 Char）
fields.Text()                  # 多行文本
fields.Html()                  # 富文本
fields.Integer()               # 整数
fields.Float(digits=(16,2))   # 小数
fields.Boolean()               # 布尔
fields.Date()                  # 日期
fields.Datetime()              # 日期时间
fields.Binary()                # 二进制/文件
fields.Selection([(...)])     # 单选
fields.Many2one('res.partner') # 多选一
fields.One2many('sale.line','order_id')  # 一对多
fields.Many2many('res.users')  # 多对多
```

### 常用装饰器

```python
@api.model         # 不依赖记录，用 cls
@api.depends()     # 计算字段依赖
@api.onchange()    # UI 自动触发
@api.constrains()  # 约束验证
@api.returns()     # 返回模型链
@api.multi         # 方法处理多条记录（默认）
```

---

*本技能基于 Odoo 19 开发规范，适配辉火云企业套件环境。*