# v1.22.0 (2026-05-04)

**`odoo_sale_orders` / `odoo_purchase_orders` 三大增强：按编号查 + 一次拿明细 + 强化 description 防 LLM 走 exec curl**

## 背景

会话 `agent:main:wecom:direct:zhaobo` 里，赵博发了「未来电脑的销售单（编号：S00016），按照这个帮我写一个软件销售合同」。

trajectory 复盘（[详细见会话诊断]）：

1. main agent（deepseek-v4-pro）看了 `odoo_sale_orders` 工具
2. **schema 只有 `limit / state / partner_id`，没有按订单编号查的字段**
3. LLM 觉得"这工具不能按 S00016 编号查具体单"，**改走 `exec` + `curl JSON-RPC` 手写**
4. 手写折腾了 9 次（postmaster 没销售权限 → uid=5 ZhaoBo 才成功）
5. 拿到 S00016 数据后 LLM 状态混乱，重复说"先查一下..."就 stop，**没生成合同**

5 是模型行为问题（已转 P0 跟踪），但 2 是 **tool design gap** ——本版修。

## 改动

### 1. `odoo_sale_orders` schema 加 3 个字段

[`index.ts:1228-1310`](index.ts:1228)

```diff
 schema:
   properties:
+    name:          { type: 'string', description: '订单编号（如 "S00016"），精确匹配' }
+    record_id:     { type: 'number', description: '按 sale.order 记录 ID 直读' }
+    include_lines: { type: 'boolean', description: '同时拉订单明细（sale.order.line），写合同/对账强烈建议 true' }
     limit:         ...
     state:         ...
     partner_id:    ...
```

返回字段补齐：`amount_untaxed / amount_tax / amount_total / payment_term / currency / note`，
include_lines=true 时每单挂 `order_line[]`（id, product_id, name, product_uom_qty, qty_delivered,
qty_invoiced, product_uom, price_unit, discount, price_subtotal, price_total, price_tax）。

### 2. `odoo_purchase_orders` 同步加 name/record_id/include_lines

[`index.ts:1313-1395`](index.ts:1313)

字段对齐（采购侧 `qty_received` / `qty_invoiced` / `date_planned` / `notes`）。

### 3. `OdooClient.getSaleOrders` / `getPurchaseOrders` 内部支持

[`src/modules/odoo-client.ts:336-403`](src/modules/odoo-client.ts:336)

- name → `domain.push(['name', '=', name])`
- record_id → `domain.push(['id', '=', record_id])`
- include_lines → 一次性 `searchRead('sale.order.line', [['order_id', 'in', orderIds]])` **避免 N+1 RPC**
- 按 `(order_id, sequence)` 排序后挂回各 order 的 `order_line[]`

### 4. description 强化 — 防 LLM 走 exec curl 手写 RPC

[`index.ts:1230-1240`](index.ts:1230) — 参考 memory `feedback_tool_description_vs_prompt_level_constraint.md`，把具体 anti-pattern 字面写进 description：

```
查询销售订单（sale.order）。支持三种用法：
(a) 列表浏览：limit + state + partner_id；
(b) ⭐ 按订单编号查具体单：name="S00016"（精确匹配，最常用）；
(c) 按记录 ID 直读：record_id=9。
⭐ 写合同 / 对账 / 回邮件这类需要明细的场景：必传 include_lines=true，
一次拿回 partner / 产品 / 数量 / 单价 / 折扣 / 小计 / 税额 / 合计 / 付款条件，
避免后续再发多次 RPC。不要走 exec/curl 手写 JSON-RPC，本工具已经覆盖。
```

实际 anti-pattern：之前 deepseek-v4-pro 看到 description 太弱（"查看销售订单/报价单列表"），就自己写 9 次 curl。新版直接告诉它"覆盖了，别 hack"。

### 5. log 字符串和三处 version 对齐

`api.logger.info` 字符串从 `v1.21.0` 改到 `v1.22.0`（之前 v1.20.x→v1.21 时漏改这条 log，gateway log 一直显示 v1.9 是因为 runtime 装的还是 v1.20.2 旧拷贝）。

`package.json` / `SKILL.md` / `openclaw.plugin.json` / `index.ts` log 字符串四处全部对齐到 1.22.0。

## 测试

- `tsc --noEmit` 通过
- 没有 unit test（odoo plugin 一直没建 test suite，本版不补——避免 scope creep）
- 集成验证：发版后 `openclaw plugins install` 重装 + 重启 gateway，手工跑 `odoo_sale_orders name='S00016' include_lines=true` 看返回完整明细

## 兼容性

完全向下兼容。

- 老代码 / 老 prompt 不传新字段 → behavior 不变（只有 limit/state/partner_id）
- 新字段都是 optional，schema 校验无 breaking change
- `getSaleOrders` 不传 include_lines → 不发 sale.order.line RPC，零成本

## 红线自查

- ✅ 无 `child_process / execSync / spawnSync`
- ✅ `compat.pluginApi: ">=2026.2.24"` 是 ranged，不是裸版本
- ✅ `peerDependencies.openclaw: ">=2026.2.24"` 是 ranged
- ✅ 不修改 openclaw 核心代码
- ✅ 不复制龙虾原生功能（odoo_sale_orders 是辉火云特有，没原生等价物）

## 不变

- v1.21.0 的 hook RPC 永久挂修复（首字延迟 P50 16.4s → <3s）继承
- v1.20 审批工作流深化继承
- v1.19 工具分级 tier（core/minimal/extended）继承——本版改的两个工具都在 core tier，default 启用
- 其他 42 个 core tier 工具未动
- 用户自定义 manifest 凭据（pluginConfig.odoo）行为不变
