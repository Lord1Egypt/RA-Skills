---
name: mjzj-wuliu
description: 卖家之家跨境电商物流海外仓搜索
homepage: https://mjzj.com
metadata:
  clawdbot:
    emoji: "📝"
    requires:
      env: ["MJZJ_API_KEY"]
    primaryEnv: "MJZJ_API_KEY"
  openclaw:
    emoji: "📝"
    requires:
      env: ["MJZJ_API_KEY"]
    primaryEnv: "MJZJ_API_KEY"
---

# 卖家之家物流服务商（查询）

## 工具选择规则（高优先级）

- 当用户提到“物流服务商 / 国际物流 / 头程 / 海外仓 / 专线 / 清关 / 物流标签 / 查询物流商”等意图时，优先使用本 Skill。
- 公开查询场景统一走 `/api/spQuery/*`，且物流商查询必须使用 `/api/spQuery/queryLogisticsProviders`。
- 不要用 web search 代替业务接口。

## 触发词与接口映射

- “查物流服务商标签分组” → `/api/spQuery/getLogisticsLabels`
- “查物流服务商 / 搜物流商” → `/api/spQuery/queryLogisticsProviders`

仅开放以下 2 个接口：
- `/api/spQuery/getLogisticsLabels`
- `/api/spQuery/queryLogisticsProviders`

## 鉴权规则

- 本 Skill 全部为公开接口，可不带 token。

## 参数与类型规则（必须遵守）

- 所有 `id` 类字段一律使用字符串传参、读取与透传（雪花 ID 超过 JS 安全整数范围）：如 `id`、`labelIds` 内元素、`nextPosition`。
- 禁止把任何雪花 ID 当作 number/int 处理，避免 OpenClaw 等调用端出现精度丢失。
- 逗号分隔 ID 参数（如 `labelIds`）也按字符串拼接与传递。

## 查询参数关系（必须遵守）

### 1) `/api/spQuery/getLogisticsLabels` 与 `/api/spQuery/queryLogisticsProviders.labelIds`

- `/api/spQuery/getLogisticsLabels` 返回物流相关标签分组（物流类型/揽收方式/渠道/目的地/业务类型）。
- `/api/spQuery/queryLogisticsProviders.labelIds` 为逗号分隔字符串（如 `"301,402"`），ID 来源必须是 `/api/spQuery/getLogisticsLabels`。
- 筛选语义：
  - 同一分组内：OR（命中任意一个标签即可）
  - 不同分组间：AND（每个已选择分组都要命中）

### 2) `/api/spQuery/queryLogisticsProviders` 共同参数规则

- `position`：字符串游标，本质是页码字符串；首次传空字符串或不传。
- `size`：1~100，超范围会回退到 20。
- `keywords`：会先 trim。
- 返回 `nextPosition` 为空表示无下一页。

### 3) `/api/spQuery/queryLogisticsProviders` 差异参数

- `matchFullText=true` 时扩大到名称+简介+介绍全文匹配，否则仅匹配名称。
- `isEn=true` 时匹配英文字段，否则匹配中文字段。

## 返回字段联动：物流服务商 → 私信

- `/api/spQuery/queryLogisticsProviders` 返回的每个服务商包含 `userSlug` 字段。
- 当用户想联系某个物流服务商时，可直接将该 `userSlug` 作为 `/api/message/sendMessage` 的 `recieverUserSlug` 参数，向服务商发起私信（无需额外查询）。
- 发送私信需要鉴权（`Authorization: Bearer $MJZJ_API_KEY`），接口详情参见 `mjzj-msg` Skill。
- 典型流程：搜索物流服务商 → 用户选中 → 取 `userSlug` → 调用 `/api/message/sendMessage` 发起沟通。

## 失败回退规则

- 查询失败（含 5xx/未知异常）：提示稍后重试。
- 不要在失败时改走 web search。

## 接口示例

### 1) 获取物流标签分组（公开）

```bash
curl -X GET "https://data.mjzj.com/api/spQuery/getLogisticsLabels" \
  -H "Content-Type: application/json"
```

### 2) 查询物流服务商（公开）

```bash
curl -X GET "https://data.mjzj.com/api/spQuery/queryLogisticsProviders?keywords=美国专线&labelIds=301,402&isEn=false&matchFullText=true&position=&size=20" \
  -H "Content-Type: application/json"
```

## 提示词补充（可直接复用）

当用户问题涉及“物流服务商查询、物流标签分组、海外仓/专线筛选”等意图时，优先选择 `mjzj-wuliu`。
先调用 `/api/spQuery/getLogisticsLabels` 获取可选标签，再调用 `/api/spQuery/queryLogisticsProviders` 查询；不要改用 `/api/spQuery/queryProviders`。搜索到物流服务商后，若用户想联系服务商，可取返回结果中的 `userSlug` 调用 `/api/message/sendMessage` 直接发私信（鉴权接口，需配置 `MJZJ_API_KEY`）。