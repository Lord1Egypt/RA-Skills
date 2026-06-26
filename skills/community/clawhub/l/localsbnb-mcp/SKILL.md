---
name: LocalsBnb 路客云 MCP
description: 在 OpenClaw、Hermes Agent、Cursor 等支持 MCP 的客户端中，通过 npm 包 localsbnb-mcp-server 调用路客云（LocalsBnb / Lukeyun）官方 HTTP API，查询房态、房价、订单与经营数据；需由用户在客户端配置 APP_ID 与 APP_SECRET。含订单五类意图路由与「本周」自然周约定。
version: 1.0.1
metadata:
  openclaw:
    requires:
      env:
        - APP_ID
        - APP_SECRET
      bins:
        - npx
    primaryEnv: APP_SECRET
    homepage: https://www.npmjs.com/package/localsbnb-mcp-server
    install:
      - kind: node
        package: localsbnb-mcp-server
        bins:
          - localsbnb-mcp
---

# LocalsBnb 路客云 MCP（技能说明）

本技能描述如何**正确配置并调用**已发布在 npm 上的 **`localsbnb-mcp-server`**，经 MCP 仅向**路客云官方 API 域名**发起 HTTPS 请求，不访问任意用户指定 URL。**本文件不含任何密钥**；`APP_ID` / `APP_SECRET` 须由用户在 MCP 客户端环境变量中自行配置（见本文件 YAML frontmatter 中 `metadata.openclaw.requires.env`）。

## 适用场景

- 酒店 / 民宿运营方已在路客云开通 API 或 MCP 访问能力。
- 用户问题涉及：**今日房态、房态日历、房价、今日/预抵/在住/预离订单、按日期查订单、订单详情、经营数据（OCC/ADR/RevPAR 等）**。

## 前置条件

1. 安装 Node.js **≥ 18**。
2. 从路客云管理员处获取 **`APP_ID`（营地/物业 ID）** 与 **`APP_SECRET`（访问令牌）**，并确认账号具备对应只读权限（房态、房价、订单、经营数据等）。
3. 在 MCP 客户端中配置服务器（勿将真实 token 写入仓库或聊天明文长期留存）。

## MCP 配置示例（通用）

将占位符替换为真实值（与仓库根目录 `mcp.sample.json` 结构一致；不同客户端外层字段名可能为 `mcpServers`，以各端文档为准）：

```json
{
  "LocalsBnb MCP": {
    "command": "npx",
    "args": ["--yes", "localsbnb-mcp-server"],
    "env": {
      "APP_SECRET": "<你的 APP_SECRET，勿提交到 Git>",
      "APP_ID": "<你的 APP_ID>"
    }
  }
}
```

### OpenClaw 快速接入提示

在已安装 Node.js ≥ 18 的前提下，可在 OpenClaw 中用自然语言引导安装 `localsbnb-mcp-server`，并注入 `APP_SECRET`、`APP_ID`；**凭证建议在私聊或受控环境传递**，避免在公开群明文发送。

## 工具一览与选型（必须按意图选对工具）

| 工具名 | 用途摘要 |
|--------|----------|
| `query_room_status_new` | 按房型**日历**查房态、可售、库存等（**不是房价**）。「本周/上周」房态须传 `timeRange`：`this_week` / `last_week`（上海自然周）。 |
| `query_today_room_status` | **单日**房态汇总（指定 `date` 或默认当天）。 |
| `query_room_prices` | **房价 / 渠道价**；「本周/上周房价」同样须 `timeRange`，勿用「近 7 天」代替「本周」。 |
| `query_today_orders` | **今日订单（聚合）**：并行预抵 11、在住 10、预离 12 三组并组装；关键词如：今日订单、待办、订单情况。 |
| `query_pre_arrival_orders` | **仅预抵**（orderType=11）。 |
| `query_in_house_orders` | **仅在住**（orderType=10）。 |
| `query_pre_departure_orders` | **仅预离**（orderType=12）。 |
| `query_orders_by_date_range` | **按日期区间查订单**（`startDate`/`endDate` 或 `timeRange`）；与上述「今日三类」**不要混用**。 |
| `get_order_details_v2` | 按 `orderId` 查详情；回复用户时须带**客人姓名**（接口可能脱敏）。 |
| `query_operational_data_v2` | 经营分析、夜审、首页实时等；「本周经营」须 `timeRange` 或显式周起止，勿只用单日 `date` 代表整周。 |

## 订单类意图路由（五类独立事件，禁止混用）

1. **今日订单 / 待办视角** → 仅 `query_today_orders`（三组聚合）。
2. **预抵** → 仅 `query_pre_arrival_orders`。
3. **在住** → 仅 `query_in_house_orders`。
4. **预离** → 仅 `query_pre_departure_orders`。
5. **某时间段订单**（如「今年 3 月 1～31 日」）→ 仅 `query_orders_by_date_range`，必须传 `startDate`/`endDate`（或自然周 `timeRange`）。

订单类列表接口默认 **`pageSize=10`**，响应中含**总数**；翻页传 `pageNum`。

## 日期与「本周」约定

- **自然周**：周一至周日，**上海时区**。
- 用户说「本周」「上周」时：房态、房价、经营、订单区间类工具应使用 **`timeRange: this_week` 或 `last_week`**，必要时配合 `date` 锚定是哪一周。
- 用户说「近 7 天」「最近一周」且无「本周」字样时：可用 `date` + `days`（如房态 `days: 7`）。

## 回复用户时的数据与合规

- 金额类字段接口多为**分**；工具输出已换算为**元**时请逐项说明，避免只报一个含糊总数。
- 同一 `orderId` 可能对应多条 `orderDetailId`（多房/多明细），须**逐条**展示，勿擅自合并为「同一主单」省略明细。
- 客人姓名即使脱敏也须**逐条保留**，与订单标识对应。
- 无房态/订单等权限时，客户端会收到规范话术，应引导用户联系管理员在路客云侧开通权限。

## 与源码仓库的关系

- **npm 包**：`localsbnb-mcp-server`（实现 MCP 协议与路客云 HTTP 调用）。
- **本 Skill**：仅文档与使用约定，**不包含**服务器源码；更新 MCP 行为以发 npm 新版本为准，Skill 内说明可随版本更新 `SKILL.md` 后再次执行 `clawhub publish`。

## 相关链接

- npm：`https://www.npmjs.com/package/localsbnb-mcp-server`
- 路客云 / 权限与 token 获取：以贵司管理员文档或路客云后台为准。
