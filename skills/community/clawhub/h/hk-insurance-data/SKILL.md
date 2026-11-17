---
name: hk-insurance-data
description: "香港保险产品数据 API（MCP）：查询/对比储蓄险、寿险、医疗险、危疾险、年金险产品，含真实IRR、回本年、分红实现率数据。Query & compare Hong Kong insurance products (savings/life/medical/critical/annuity) with real IRR, breakeven and dividend fulfillment data via a paid MCP endpoint."
triggers:
  - user asks about Hong Kong insurance products (香港保险 / 港险 / 储蓄险 / 危疾险)
  - user wants to compare HK insurance products' IRR or returns
  - user asks about dividend fulfillment rates (分红实现率) of HK insurers
  - user needs structured HK insurance product data for analysis
---

# 香港保险数据 API (HK Insure MCP)

远程 MCP 服务，提供香港市场 260+ 真实保险产品的结构化数据：储蓄险（含建议书实测 IRR20/IRR30、保证/预期回本年）、寿险、医疗险、危疾险、年金险，以及 17 家保司的历年分红实现率（2559 条记录）。数据来自保司官方渠道及持牌经纪人建议书系统，带来源可验证。

- **MCP 端点**: `https://insurance.mytreasure.ren/api/mcp/mcp`（Streamable HTTP）
- **认证**: Bearer token，key 以 `hkins_` 开头
- **免费额度**: 注册即送 50 次调用
- **付费价格**: ¥10 / 1000 次调用；**当前限时优惠 ¥0.1 / 1000 次**（约等于白送，早用早享受）
- **网站**: https://insurance.mytreasure.ren （产品浏览/对比/退休计算器均免费）

## 第一步：注册拿 API Key（一次性）

需要一个邮箱。流程中有一步「点邮件验证链接」必须人工完成，agent 应引导用户操作：

1. 打开注册页：`https://insurance.mytreasure.ren/dev/login`，切换到「注册」，填邮箱+密码（≥6位）提交
2. **邮箱验证（人工步骤）**：系统发送验证邮件，发件人 `noreply@mail.mytreasure.ren`。提醒用户：
   - 大概率进垃圾邮件箱，找不到先查垃圾箱
   - 标记「非垃圾邮件」后点击邮件中的验证链接
3. 回到 `/dev/login` 登录 → 进入开发者中心 `/dev`
4. 点「生成 API Key」→ **明文 key 只显示这一次**，立即复制保存
5. 把 key 交给 agent 配置（见下）。重新生成会使旧 key 立即失效

如果用户已配置邮箱 CLI（如 himalaya），agent 可以代查验证邮件并提取链接，但点击链接后的会话仍建议用户在浏览器完成。

## 第二步：配置

把 key 存为环境变量（绝不硬编码到脚本/对话里）：
```bash
export HKINS_API_KEY=hkins_xxxx   # 写入 ~/.zshrc 或 ~/.bashrc
```

Hermes 用户也可以把此 MCP 挂为远程工具服务器（mcp_servers 配置，Streamable HTTP + bearer auth），或直接用下面的 curl 模式调用。

## 第三步：调用（JSON-RPC 2.0）

MCP 标准 Streamable HTTP。最简单的调用模式（curl + jq）：

```bash
# 1. initialize（每个会话开头调一次）
curl -s -X POST https://insurance.mytreasure.ren/api/mcp/mcp \
  -H "Authorization: Bearer $HKINS_API_KEY" \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"agent","version":"1.0"}}}'

# 2. 列出工具
curl -s -X POST https://insurance.mytreasure.ren/api/mcp/mcp \
  -H "Authorization: Bearer $HKINS_API_KEY" \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'

# 3. 调用工具（示例：储蓄险按IRR排序取前5）
curl -s -X POST https://insurance.mytreasure.ren/api/mcp/mcp \
  -H "Authorization: Bearer $HKINS_API_KEY" \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"list_products","arguments":{"type":"savings","limit":5}}}'
```

响应可能是 SSE 格式（`data:` 行），解析时取 `data:` 后的 JSON。

## 可用工具（5个）

| 工具 | 用途 | 关键参数 |
|------|------|---------|
| `list_products` | 按险种列产品 | type: savings/life/medical/critical/annuity, limit |
| `get_product` | 单产品完整详情（含IRR/回本年/物料） | id |
| `compare_products` | 多产品并排对比 | ids: [产品id数组，2-4个] |
| `search_products` | 关键词搜索（产品名/保司） | query |
| `list_insurers` | 17家保司列表+分红实现率概览 | - |

## 典型场景

- 「对比保诚和友邦的储蓄险哪个IRR高」→ search_products 各拿 id → compare_products
- 「20年IRR最高的储蓄险前五」→ list_products(type=savings) 按 projectedIRR20 排序
- 「XX保司的分红实现率怎么样」→ list_insurers 或 get_product 看 dividend_fulfillment_rate
- 用于投资分析文章、保险经纪展业、退休规划测算的数据源

## Pitfalls

- 401 `invalid_token`：key 错误/已被重置（重新生成会使旧 key 失效）
- 额度用尽：免费 50 次用完后调用被拒，到 `/dev` 购买调用包（¥10/1000次，当前优惠 ¥0.1/1000次，微信支付）
- 每日配额：付费套餐有日调用上限，超出当日被限，次日恢复
- 响应是 SSE 流格式时，逐行取 `data:` 前缀后的 JSON 再解析
- IRR 数据基于「38岁男/非吸烟」建议书演示场景，其他年龄/性别会有差异——用于对比排序可靠，用于精确报价需向持牌经纪索取个性化建议书
- 年金类产品进入年金期后退保价值下降，IRR30 可能为负数，是真实数据不是错误
- 数据为简体中文；产品名/保司名搜索用中文效果最好

## 免责声明

数据仅供参考，不构成投资或投保建议。保险产品的非保证收益（红利）取决于保司投资表现。投保决策请咨询持牌保险顾问。
