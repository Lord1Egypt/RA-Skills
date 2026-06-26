# 测试数据集

## 电商域（ecommerce/）

四张表，完整外键关联链：

```
customers (15行) ──── orders (30行)
                         │
                    order_items (53行)
                         │
products (20行) ──────────┘
```

| 文件 | 主键 | 外键 | 说明 |
|------|------|------|------|
| customers.csv | customer_id | — | 客户信息，含城市/省份/客户段 |
| products.csv | product_id | — | 商品信息，含品类/品牌/价格 |
| orders.csv | order_id | customer_id → customers | 订单主表，含支付方式/状态/金额 |
| order_items.csv | item_id | order_id → orders, product_id → products | 订单明细，含数量/折扣/小计 |

**典型查询示例：**
- 哪些客户的累计消费最高？
- 各商品类别的销售额和利润是多少？
- 最近一个月哪些订单被取消或退款了？
- Apple 品牌的产品卖出了多少件，带来多少收入？
- 企业客户 vs 消费者的平均订单金额对比？

---

## HR 域（hr/）

两张表，含树形上下级关系：

```
departments (12行) ←── employees (30行)
     │                      │
     └── parent_dept_id     └── manager_id → employees（自引用）
```

| 文件 | 主键 | 外键 | 说明 |
|------|------|------|------|
| departments.csv | dept_id | parent_dept_id → departments（自引用） | 部门树，含预算/编制 |
| employees.csv | employee_id | dept_id → departments, manager_id → employees | 员工信息，含职级/薪资/奖金比例 |

**典型查询示例：**
- 各部门的平均薪资是多少？
- 技术部门有哪些员工，各自的职级和薪资？
- 销售部门的奖金比例为什么最高？
- 谁是哪个员工的直属上级？
- 2022年之后入职的员工有多少人，分布在哪些部门？
- 人均薪资最高的三个部门是哪些？

---

## 跨域关联说明

两个业务域目前没有直接外键关联（现实中也是分库的），但可以用于测试：
- 多数据源同时连接
- 跨源语义搜索（搜"销售"同时返回电商和HR相关表）
- 分别在不同上下文中回答业务问题
