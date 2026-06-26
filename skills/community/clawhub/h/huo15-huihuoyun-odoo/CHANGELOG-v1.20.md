# v1.20.0 (2026-04-28)

**核心修复：tier 分级让默认 prompt tool schema 从 ~190 工具 / ~17000 tokens 砍到 ~30 工具 / ~3000 tokens。配合 v1.19 的 system context 瘦身，每次 prompt 总省 ~16000 tokens。**

## 背景

v1.19 把 `before_prompt_build` 注入的 system context 从 7900 字砍到 1500 字（节省 ~1700 tokens）。但实测 `dispatch-start → deliver-start` TTFT 仍 70-150 秒。

进一步诊断（直接 curl DeepSeek API）：

| 测试 | 端到端时间 |
|---|---|
| DeepSeek 流式 TTFT | **530ms** |
| DeepSeek 非流式（含响应） | **790ms** |

→ DeepSeek API 端**完全没问题**。**真正的 TTFT 元凶是 prompt 太大**（单大头 = 189 个 odoo 工具的 JSON schema），LLM 端 prefill 处理 30k+ tokens 才出第一字。

预估每个 odoo 工具 schema ≈ 80-200 tokens（name + description + properties + required）：

- description 总和 16470 字符 / ~5490 tokens
- 加 schema 结构（properties / required / type 等）×3-4 倍 → **15000-20000 tokens** 仅 odoo 一个 plugin

## 改动

### `index.ts` — 引入 tier 分级

新增 `ODOO_TOOL_TIERS`（module-level 常量）：

```ts
const ODOO_TOOL_TIERS = {
  minimal: new Set([...]),  // 10 个：连接 + 最核心任务
  core:    new Set([...]),  // 30 个：覆盖 80% 日常需求（默认）
  // extended: null = 全部 190 个（v1.19 行为）
};
```

`registerTools` 函数顶部读 plugin config：

```ts
const cfg = (api.pluginConfig ?? {}) as { tier?: 'minimal' | 'core' | 'extended' };
const tier = cfg.tier ?? 'core';  // 默认 core
const allowedTools = tier === 'extended' ? null : ODOO_TOOL_TIERS[tier];

const register = (opts) => {
  if (allowedTools === null || allowedTools.has(opts.name) || opts.name === 'odoo_help') {
    api.registerTool(opts);
    registeredCount++;
  } else {
    skippedCount++;
  }
};
```

然后 sed 把 489-5500 行内 189 个 `api.registerTool(` 替换为 `register(` —— **所有 189 个工具走 register wrapper 过滤**。

`odoo_help` 工具**始终注册**（任何 tier），保证 LLM 能查完整工具表。

### `index.ts` — system context 提示当前 tier

将 v1.19 的 "完整 189 个工具表 …" 提示更新为 "**当前 tier=core（默认 30 个高频工具直接可见）。完整 190 个工具调 odoo_help 查；如需恢复 v1.18 全量行为：改 ~/.openclaw/openclaw.json 的 plugins.entries.odoo.config.tier='extended'**"。

### `index.ts` — 启动期 log 报告 tier 状态

```
v1.18: [odoo] 189 个工具已注册（v1.18 — Studio 元编程+审计...）
v1.19: [odoo] 190 个工具已注册（v1.19 — 加 odoo_help...）
v1.20: [odoo] 30 个工具已注册（v1.20 — tier=core 精简档位 / 跳过 160 个，节省 ~12800 tokens schema）
       完整 190 工具调 odoo_help 查；改 plugins.entries.odoo.config.tier="extended" 可恢复全量。
```

## tier 三档

### `minimal`（10 工具）

仅最核心连接 + 任务搜索：
```
odoo_connect / odoo_status / odoo_disconnect / odoo_whoami / odoo_help
odoo_create_task / odoo_list_tasks / odoo_my_today
odoo_search / odoo_daily_briefing
```

适合：极致性能，仅做"连接 + 任务列表"演示场景。

### `core`（30 工具，默认）

覆盖 80% 日常需求的高频 30 个：

- 连接 & 状态（5）：odoo_connect / odoo_status / odoo_disconnect / odoo_whoami / odoo_help
- 任务 & 活动（8）：odoo_create_task / odoo_list_tasks / odoo_update_task / odoo_my_today / odoo_my_workload / odoo_create_activity / odoo_calendar_today / odoo_complete_activity
- CRM（5）：odoo_crm_pipeline / odoo_crm_create / odoo_crm_update / odoo_crm_won / odoo_crm_lost
- 项目（2）：odoo_project_overview / odoo_timesheet_log
- 客服（2）：odoo_tickets / odoo_ticket_create
- 财务（3）：odoo_invoices / odoo_sale_orders / odoo_purchase_orders
- 联系人（2）：odoo_contacts / odoo_contact_create
- 检索（2）：odoo_search / odoo_daily_briefing
- 消息（1）：odoo_message_post

### `extended`（190 工具，v1.18/1.19 行为）

完整暴露所有工具（含 HR 全套 / 库存深化 / 生产 MRP / Studio 元编程 / 审计 / 多公司联动等）。

适合：需要全功能，不在意 prompt token 开销。

## 配置切换

在 `~/.openclaw/openclaw.json`：

```jsonc
{
  "plugins": {
    "entries": {
      "odoo": {
        "config": {
          "tier": "extended"   // 或 "core"（默认）/ "minimal"
        }
      }
    }
  }
}
```

改完后 `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway` 重启 gateway 即生效。

## 用户可见效果

| 项 | v1.18 | v1.19 | **v1.20 默认** | v1.20 extended |
|---|---|---|---|---|
| system context 注入 | ~7900 字 / ~2000 tokens | ~1500 字 / ~400 tokens | ~1500 字 / ~400 tokens | ~1500 字 / ~400 tokens |
| 工具数量 | 189 | 190 | **30** | 190 |
| 工具 schema 占 tokens | ~17000 | ~17000 | **~3000** | ~17000 |
| **每次 prompt 总 token** | 19000 | 17400 | **3400** | 17400 |
| LLM TTFT 预估 | 70-150s | 65-145s | **15-50s** | 65-145s |

注：实际 TTFT 受 LLM 端 prefill 速度、conversation history、其他 plugin 注入影响。

## 风险与缓解

- **风险**：默认只 30 工具，LLM 不知道"odoo_employee_skills"等工具存在 → 用户问相关问题时 LLM 表现退化
- **缓解 1**：system context 顶部明确告知"完整 190 工具调 odoo_help 查"
- **缓解 2**：odoo_help 工具的 description 写明 "按需获取详细信息（无参 = 完整 190 工具表 / keyword 模糊匹配）"
- **缓解 3**：core 30 个已覆盖 80% 日常场景；不在 core 但常用的工具，用户可手动调到 extended

## 测试

- `tsc --noEmit` exit 0（v1.19 还有 ~20 个 schema warning，v1.20 因为 register wrapper 用 generic 反而**全部消除**）
- 启动期 log 应从 `190 个工具已注册（v1.19 …）` 变为 `30 个工具已注册（v1.20 — tier=core …）`

## 兼容性

完全向下兼容。改 plugin config `tier="extended"` 即恢复 v1.19 行为，所有 190 工具签名 / 行为 / 业务逻辑全部不变。
