---
name: huo15-yh-usage
displayName: 火一五·烟花智汇用量账单
version: 1.1.0
description: "凭客户烟花智汇 API Key(fsk-)查询该 Key 的 token 用量与费用——总览/按供应商/按模型/按天趋势,人民币¥与美元$双币种可切换(--usd),数据来自平台服务端权威计费(含缓存折价、分组倍率)。"
homepage: https://github.com/zhaobod1/huo15-skills
metadata: { "openclaw": { "emoji": "🎆", "requires": { "bins": ["node"] } } }
aliases:
  - 火一五·烟花智汇用量账单
  - 烟花用量
  - 烟花智汇用量
  - 烟花智汇账单
  - token 账单
  - model usage
  - 用量统计
  - 费用统计
---

# 烟花智汇 · 用量账单(Model Usage)

凭**客户提供的烟花智汇 API Key(`fsk-...`)**,统计**该 Key**近 N 天的 **token 消耗与费用**,输出中文报告:总览 + 按模型 + 按天趋势。

> 与 Cherry Studio / AionUI / Lobe Chat / OpenCat / AIaW 等 BYOK 客户端不同——它们大多只在聊天里**逐条**显示 token、**不聚合、不算钱、不分模型/天**(费用全甩给上游)。本技能直接读**烟花智汇服务端权威计费**(按 `apiKeyId` 聚合的真实扣费,含缓存折价、分组倍率),做得更全、是真账单不是估算。

## 何时用
- 客户问「我这把 key 花了多少 token / 多少钱」「哪个模型最费」「这几天用量趋势」。
- 给客户/销售出一份按模型、按天的用量与费用小结。

## 怎么用

**优先跑脚本**(零依赖,Node 18+ 自带 fetch):

```bash
node scripts/usage.mjs <fsk-...客户的key> [天数=30] [--usd]
# 例:node scripts/usage.mjs fsk-xxxxxxxx 30          # 人民币 ¥
#     node scripts/usage.mjs fsk-xxxxxxxx 30 --usd    # 美元 $(按端点 usdRate 折算)
# 要原始 JSON:加 --json
```

脚本会请求 `GET https://fireworks-simulator-api.huo15.com/v1/usage?days=N`(`Authorization: Bearer <key>`),并格式化为中文 markdown 报告直接展示给客户。

**没有 Node 时用 curl**:
```bash
curl -s "https://fireworks-simulator-api.huo15.com/v1/usage?days=30" -H "Authorization: Bearer <fsk-key>"
```
然后按下方「输出口径」自己排版。

## 数据端点(平台侧,fsk- key 鉴权)
`GET /v1/usage?days=<1-90>` → 返回:
- `totals`:`calls` 调用数、`promptTokens` 输入、`completionTokens` 输出、`cachedTokens` 命中缓存、`totalTokens` 合计、`cost` 费用(CNY)。
- `byProvider[]`:每**供应商**(烟花智汇接入的 Sidus/润嘉云/OpenSand/DeepSeek 等)`provider/calls/totalTokens/cost`,**按费用降序**——看钱花在哪家。
- `byModel[]`:每模型 `model/calls/promptTokens/completionTokens/totalTokens/cost`,**按费用降序**。
- `currency:"CNY"` + `currencies:["CNY","USD"]` + `usdRate`(人民币/美元):美元 = cost / usdRate,供 `--usd` 与客户端币种切换。
- `daily[]`:每天 `day/tokens/cost/calls`。
- `key`:`name` + 脱敏 `masked`(`fsk-••••后四位`);`currency: "CNY"`。

## 输出口径(对标最佳实践)
- **总览**:调用次数、输入/输出/缓存/合计 token(K/M 友好)、**费用合计 ¥**、统计区间。
- **按模型**:表格(模型|调用|输入|输出|总Token|费用),按费用降序——一眼看出「哪个模型最费」。
- **按天趋势**:费用/Token 的迷你条形,看波动。
- 费用强调是**平台实际计费金额(¥)**,非本地估算;明细按调用看可去控制台 `/me/usages`。

## 注意
- key 必须 `fsk-` 开头且 active;无效/禁用会返回 401(脚本已提示)。
- 费用单位人民币 ¥;已含缓存命中折价与用户分组倍率(平台计费规则)。
- 该端点只看**这一把 key** 的用量;某用户名下多 key 的汇总需登录控制台看 `/me/stats`。
- `days` 上限 90 天。
