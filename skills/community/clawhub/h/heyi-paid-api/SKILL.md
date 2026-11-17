---
name: heyi-paid-api
slug: heyi-paid-api
version: 1.2.0
displayName: 小红书 API｜抖音、B站、快手社媒数据接口
summary: 小红书 API、抖音 API、B站 API、快手 API 的付费 HTTP 数据接口，支持笔记/视频搜索、详情、评论、用户作品和积分计费。
description: Use when a user wants an AI agent to call Heyi's Xiaohongshu, Douyin, Kuaishou, or Bilibili HTTP APIs with a Bearer API Key, including endpoint discovery, point billing, balance checks, pagination, batching, error handling, retries, or usage reconciliation.
tags: [小红书API, 小红书数据接口, XHS API, 抖音API, B站API, 哔哩哔哩API, 快手API, 社媒数据接口, 内容搜索, 笔记详情, 评论接口, 用户作品]
homepage: https://api.01011.top
triggers:
  - 小红书 API
  - XHS API
  - 抖音 API
  - Douyin API
  - B站 API
  - 哔哩哔哩 API
  - Bilibili API
  - 快手 API
  - Kuaishou API
  - heyi paid api
  - 笔记搜索
  - 视频解析
  - 内容数据接口
  - 社媒 API
inputs:
  api_key:
    note: Bearer API Key（必填）
    secret: true
    env: HEYI_API_KEY
  base_url:
    note: API Base URL
    default: https://bot.01011.top
    env: HEYI_API_BASE_URL
  query_or_body:
    note: 按接口 schema 决定放 query 或 JSON body
    required: true
outputs:
  api_response:
    note: HTTP JSON 响应（code / msg / data）
  bill_summary:
    note: 调用是否计费的判定（按 HTTP 200 + 业务 code 200/2000/缺失）
  call_record_ref:
    note: 服务端积分流水条目指针，用于事后对账
dependencies:
  - curl 或任意 HTTP 客户端
  - Node.js >= 14（仅 check / snapshot 命令需要）
  - 有效 API Key（注册赠送 50 点；填邀请码双方各 +10）
---

# Heyi 付费 API

这是一个面向 API 使用者的调用协议。用户提供或配置 API Key 后，Agent 负责选择正确的接口、在可能扣费前说明费用、发起 HTTP 请求、准确返回服务端数据，并按服务端账务核对扣费。

## 调用范围

本 Skill 用于调用 `https://bot.01011.top/api/external/` 下的 API Key 接口，包括公开目录、积分查询，以及公开目录中启用的小红书、抖音、快手、Bilibili 等接口。

不要把平台后台管理、数据库、RBAC 或仅限后台调用的接口当作 API Key 接口调用。如果接口目录或错误信息表明该接口不支持 API Key，应停止并说明当前认证方式不适用；不要擅自用其他凭据替换 API Key。

## 调用前提

- 如何申请与使用 API Key，请参见飞书指南：<https://my.feishu.cn/wiki/SzpMwQQ1Piw3rck0NAPc7la1npe>。
- API Key 应由用户提前在控制台创建，并通过安全凭据或 `HEYI_API_KEY` 提供给 Agent。
- 不要要求用户把完整 Key 粘贴到聊天中；没有 Key 时，只说明需要配置它，不要伪造示例 Key 发起请求。
- API Base URL：`https://bot.01011.top`。
- 所有业务 API path 必须以 `/api/external/` 开头；不要通过用户输入拼接任意主机地址。

## 认证与请求格式

所有 API Key 请求都使用：

```http
Authorization: Bearer <api_key>
Accept: application/json
```

```bash
export HEYI_API_BASE_URL="https://bot.01011.top"
export HEYI_API_KEY="<your_api_key>"
```

- GET 参数放 query string。
- POST、PUT、PATCH 等请求按接口 schema 放 JSON body，并设置 `Content-Type: application/json`。
- 不要把 API Key 放进 URL、query、JSON body、日志、截图或最终回复。
- `X-Business` 只有在用户明确指定业务域时才添加；不确定时使用服务端默认值，不要自行猜测。`X-Platform` 同理。

## 调用流程

按以下顺序执行：

1. 判断用户是在询问接口用法，还是明确授权真实调用。仅解释时不要调用付费接口。
2. 用公开目录查找接口；读取接口详情中的 `method`、`path`、`params_schema`、`request_sample` 和价格字段。
3. 判断本次请求是否可能扣费。若可能，告诉用户接口、参数摘要、预计请求次数和预计最大扣点。
4. 只有在用户明确确认后，才调用付费接口。余额查询、公开目录查询等只读请求可以直接执行。
5. 发送 Bearer 请求，保留 HTTP 状态码、响应 JSON、业务 `code` 和 `msg`。
6. 根据本 Skill 的扣费规则解读响应；不确定时查询积分流水，不要猜测。

## 发现接口

接口路径、方法、参数和价格可能随后台配置变化。未知接口禁止凭名称猜测，优先查询：

```text
GET /api/external/platform/public/summary/
GET /api/external/platform/public/endpoints/
GET /api/external/platform/public/endpoints/<code>/
```

公开目录不需要 API Key：

```bash
curl --fail-with-body \
  "$HEYI_API_BASE_URL/api/external/platform/public/endpoints/?keyword=xhs"

curl --fail-with-body \
  "$HEYI_API_BASE_URL/api/external/platform/public/endpoints/search_notes/"
```

列表接口返回接口元数据；单接口详情才包含 `params_schema` 和 `request_sample`。按 schema 处理参数：

- `in=query`：放 URL 查询参数；
- `in=body`：放 JSON body；
- `in=path`：替换路径占位符并 URL 编码；
- `in=header`：只添加该接口明确要求的 header，不覆盖 `Authorization`。

列表接口当前返回的字段为：`name / code / method / path / group_code / group_name / original_price_points / effective_price_points / discount_percent / discount_name / description`。按 `group_code`（`xhs` / `douyin` / `bili` / `kuaishou`）或 `keyword` 筛选。

> `category` 二级能力分类（`search / detail / user / comment / interaction / playback / live / tool / statistics`）与 `sub_title` 入参提示已在后端实现，但**尚未部署到生产**。不要依赖这两个字段做筛选；上线后 `npx heyihub-skill check` 会以 `changed` 提示你升级 Skill。

完整 OpenAPI 可能只在开发环境暴露；它不是替代公开目录的理由。旧的 `/platform/public/catalog/` 仅作为兼容入口。

## 费用、余额与扣费

### 价格来源

调用可能收费的接口前，先查询：

```text
GET /api/external/points/cost-config
```

该接口需要有效认证，返回结构重点是：

```json
{
  "code": 2000,
  "data": {
    "api_costs": {
      "search_notes": 2,
      "get_note_info": 1,
      "douyin_search": 2,
      "bilibili_get_video_playurl": 1
    }
  }
}
```

`api_costs` 是费用配置快照，可能同时带有其他配置字段。公开接口详情中的 `original_price_points`、`effective_price_points`、`discount_percent` 用于查看接口当前价格和折扣。最终扣费以服务端响应和积分流水为准，客户端不得自行扣费或用旧价格覆盖新价格。

### 余额

```bash
curl --fail-with-body \
  -H "Authorization: Bearer $HEYI_API_KEY" \
  "$HEYI_API_BASE_URL/api/external/points/balance"
```

返回的 `data` 通常包含 `balance`、`total_earned`、`total_consumed`。批量调用前必须先检查余额，并按最大请求量预留预算。

### 扣费判定

只有同时满足以下条件，付费请求才符合成功扣费规则：

```text
HTTP 状态码 == 200
且业务 code == 200、2000 或缺失
```

以下情况不扣费：参数错误、API Key 无效或无权限、余额不足、限流、上游失败、超时和其他非 `200` 响应。价格为 `0` 的免费接口即使成功，也不会产生消费积分流水。

### 积分流水

```text
GET /api/external/points/records
  ?page=1&page_size=20&change_type=consume&points_type=<points_type>
```

流水返回 `data.list`、`total`、`page`、`page_size`。单条记录常见字段包括 `points`、`balance_before`、`balance_after`、`points_type`、`request_path` 和 `create_datetime`。

成功扣费的付费请求通常对应一条 `change_type=consume` 记录；免费请求或失败请求不要因为没有消费记录而报错。

## 直接调用示例

调用前先完成接口发现、价格确认和用户授权：

```bash
# GET：参数放 query
curl --fail-with-body --get \
  -H "Authorization: Bearer $HEYI_API_KEY" \
  -H "Accept: application/json" \
  --data-urlencode "keywords=咖啡" \
  --data-urlencode "page=1" \
  "$HEYI_API_BASE_URL/api/external/xhs/search_notes"

# POST：参数放 JSON body
curl --fail-with-body -X POST \
  -H "Authorization: Bearer $HEYI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"keyword":"露营","offset":0}' \
  "$HEYI_API_BASE_URL/api/external/douyin/search"
```

不要假定示例参数适用于所有接口；以对应 endpoint 详情的 schema 为准。

## 客户端代码片段

### Node.js（Node 18+ 原生 fetch）

```javascript
// heyi-client.mjs
const BASE = process.env.HEYI_API_BASE_URL || "https://bot.01011.top";
const KEY = process.env.HEYI_API_KEY;

async function heyi(path, { method = "GET", body, query } = {}) {
  if (!KEY) throw new Error("HEYI_API_KEY is required");
  const url = new URL(BASE + path);
  if (query) for (const [k, v] of Object.entries(query)) {
    if (v !== undefined && v !== null) url.searchParams.set(k, v);
  }
  const res = await fetch(url, {
    method,
    headers: {
      "Authorization": `Bearer ${KEY}`,
      "Accept": "application/json",
      ...(body ? { "Content-Type": "application/json" } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const json = await res.json().catch(() => ({}));
  return { http: res.status, code: json.code, msg: json.msg, data: json.data };
}

// 示例：小红书关键词搜索
const r = await heyi("/api/external/xhs/search_notes", {
  query: { keywords: "咖啡", page: 1 }
});
console.log(r);  // { http: 200, code: 2000, msg: "...", data: {...} }
```

### Python（httpx）

```python
# heyi_client.py
import os, httpx

BASE = os.environ.get("HEYI_API_BASE_URL", "https://bot.01011.top")
KEY = os.environ["HEYI_API_KEY"]

def heyi(path: str, method: str = "GET", params: dict | None = None,
         json_body: dict | None = None) -> dict:
    headers = {"Authorization": f"Bearer {KEY}", "Accept": "application/json"}
    if json_body is not None:
        headers["Content-Type"] = "application/json"
    r = httpx.request(method, f"{BASE}{path}",
                      params=params, json=json_body,
                      headers=headers, timeout=30.0)
    r.raise_for_status()
    body = r.json()
    return {"http": r.status_code, "code": body.get("code"),
            "msg": body.get("msg"), "data": body.get("data")}

# 示例：抖音关键词搜索（POST）
r = heyi("/api/external/douyin/search", method="POST",
         json_body={"keyword": "露营", "offset": 0})
print(r)
```

## 典型场景示例

下面四类是 Agent 最常被问到的组合调用。**每次扣费前都先告诉用户接口、价格、预计请求数**，获得明确授权后再发。

### 1. 小红书：关键词搜索 → 笔记详情 → 评论

```text
1.  GET /api/external/xhs/search_notes?keywords=咖啡&page=1
    → 拿 note_id 列表
2.  对前 N 条：
    GET /api/external/xhs/get_note_info?note_id=<id>
    → 拿正文、图、视频、互动数据
3.  对感兴趣的：
    GET /api/external/xhs/get_note_comments?note_id=<id>&page=1
    → 拿评论
```

计费预估：搜索 N 次 + 详情 N 次 + 评论 N 次。

> `get_note_info` 自 v1.1.0 起不再接受 `video_detail` 开关——业务方反馈 heyi_agent 已统一返回完整数据。响应字段以当前 `params_schema` 为准，不要再携带 `video_detail=true|false`。

### 2. 博主视角：用户主页 → 作品列表 → 逐条详情

```text
1.  GET /api/external/xhs/get_user_info?user_id=<uid>
    → 拿博主昵称、粉丝、画像
2.  GET /api/external/xhs/get_user_notes?user_id=<uid>&page=1
    → 拿作品列表（游标型）
3.  对每条作品：
    GET /api/external/xhs/get_note_info?note_id=<id>
    → 拿单条详情
```

计费预估：1（主页）+ 列表页数 × 每页成本 + 详情数 × 单条详情价。

### 3. 抖音：关键词搜索 → 视频详情

```text
1.  POST /api/external/douyin/search  body: {"keyword":"露营","offset":0}
    → 拿 aweme_id 列表
2.  GET /api/external/douyin/get_video_info?aweme_id=<id>
    → 拿视频详情、下载链接
```

### 4. B站：BV 号搜索 → 视频详情 → 评论

```text
1.  GET /api/external/bili/search_videos?keyword=xxx&page=1
    → 拿 bvid / aid
2.  GET /api/external/bili/get_video_info?bvid=<BVxxxx>
    → 拿 cid、UP 主、播放量
3.  GET /api/external/bili/get_comments?oid=<aid>&type=1&page=1
    → 拿评论
```

> 通用提醒：批量前必须先 `GET /points/balance` 看余额是否覆盖最大请求量；批内出现 5xx / 超时先停手对账，再决定是否继续。

#### B站 V1 → V2 切换

下列 V1 endpoint 已在后端 `ApiEndpoint.description` 前缀 `[已废弃]` 标记，且响应头注入 `Deprecation: true` / `Sunset: 2026-09-07`，下个版本（≥ 1.2.0）移除前请升级并切换：

| V1（已废弃） | 替代 | 说明 |
| --- | --- | --- |
| `GET /api/external/bili/get_dynamic_detail` | `GET /api/external/bili/get_dynamic_detail_v2` | 动态详情 V2 字段更稳定 |
| `GET /api/external/bili/search_all` | `GET /api/external/bili/search_by_type` | 不传 `search_type` 即等同原行为；指定类型更精确 |

注意：`get_video_detail`（aid 入参）和 `get_video_info`（bvid 入参）是 B 站官方两个独立 API，**不能互相替代**，调用前确认入参类型。

## 响应结构与 Agent 输出

常见响应壳为：

```json
{
  "code": 2000,
  "msg": "获取成功",
  "data": {}
}
```

- `code` 是业务状态码；`200`、`2000` 和缺失表示业务成功候选。
- `msg` 是服务端提示；失败时用于排错。
- `data` 的具体结构由接口详情决定，不要统一假定为 `list`。
- HTTP `200` 也可能携带业务失败 code 或合法空结果。
- 不要给服务端数据补造字段、擅自脱敏业务数据或把空结果改写成失败。

调用完成后，简洁报告：

```text
接口：<METHOD> <path>
HTTP：<status>
业务 code：<code 或缺失>
扣费：按规则应扣 / 不扣 / 尚未对账
结果：<原始 data 或必要摘要>
```

没有查询流水时，不要声称“实际已扣 N 点”；应写“按成功规则预计扣 N 点，最终以流水为准”。

## 常见错误

| HTTP | 业务 code | 含义 | 处理 |
| --- | --- | --- | --- |
| `200` | `200` / `2000` / 缺失 | 业务成功候选 | 读取 `data`，必要时对账 |
| `200` | `400` | 参数或业务校验错误 | 按 schema 修正，不重试相同请求 |
| `401` | — | Key 缺失、格式错误、无效、禁用或过期 | 检查 Key，不重复发送同一错误请求 |
| `402` | `4003` | 余额不足 | 查询余额或充值后再试，不扣费 |
| `403` | `403` | 未授权目标接口分组 | 让 Key 获得对应分组权限，不扣费 |
| `404` | `4040` | 接口不存在或已下线 | 先跑 `npx heyi-paid-api check` 确认是否本地下线；查公开目录替代接口；不扣费 |
| `429` | `429` | 触发限流 | 读取 `Retry-After`；否则按指数退避串行重试，**不并发** |
| `500` | — | 服务端内部错误 | 单次重试前先对账；批内出现先停 |
| `502` / `503` / `504` | — | 网关 / 上游超时 / 上游不可达 | 多半是上游社媒平台抖动；指数退避后少量重试；批内停止 |
| 网络异常（DNS / SSL / 连接重置 / 超时） | — | 客户端或链路问题 | 不等同"未扣费"；先 `points/records` 对账 |

业务失败和非 `200` 响应不扣费。**网络异常则不等同于"确定未扣费"**，必须先对账。

### 调试清单（Agent 排查时按顺序执行）

1. **Key 是否生效**：先 `GET /points/balance`，能拿到 `balance` 字段即视为有效；返回 `401` 则回控制台查 Key 状态。
2. **接口是否还在**：跑 `npx heyihub-skill check`，看是否报 `retired`；或匿名 `GET /platform/public/endpoints/?keyword=<关键字>` 确认 `code` 还在目录里。
3. **价格是否变动**：跑 `GET /points/cost-config`，对比上次调用的扣点；差异通常意味着 `changed`。
4. **余额够不够**：扣费规则只在 `HTTP 200 + 业务成功` 时扣点，所以 `402 / 4003` 说明余额不足或预算超限。
5. **限流状态**：连续 `429` 时读 `Retry-After`；批量任务应暂停 5–10 分钟再继续。
6. **响应壳是否完整**：服务端响应可能不带 `code` 字段（如部分旧接口），按"缺失"视为成功候选，但**不可假设**——若该接口历史上都有 `code`，缺失也可能是异常。
7. **是否已扣费**：始终以 `points/records` 为准，不要凭"上次调用失败"就断言未扣。
8. **客户端问题**：
   - DNS 解析失败 → 检查代理 / VPN / `/etc/resolv.conf`
   - SSL 错误 → 检查系统时间、CA 证书、是否被中间人代理
   - 连接重置 → 检查防火墙、端口 443 是否被屏蔽

任何一步不通过，先解决这一步再回到调用流程，不要带着未排查的故障继续扣费调用。

## 重试与幂等

当前协议没有通用幂等键。遇到超时、连接重置、响应体缺失或 JSON 解析失败时，服务端可能已经完成业务处理；重试前必须先查 `points/records`。

- `400`、`401`、`402`、`403`、`404`：修正原因后再请求，不自动重试原请求；
- `429`：优先读取 `Retry-After`，否则退避后串行重试；
- `5xx`：最多少量指数退避重试，但批量任务必须先暂停并对账；
- 对账发现已有消费记录时，不要再次重试同一业务请求；
- 对账无法确认时，停止自动补偿并向用户报告，不要伪造退款或补单。

## 分页与批量调用

分页参数和停止条件由接口 schema 与返回数据决定，不能把所有接口都当成 `page/page_size`：

- 页码型：递增 `page`，直到接口返回的结束标记或空结果；
- 游标型：只使用服务端返回的 `cursor`、`search_id` 等下一页值；
- 偏移型：使用接口声明的 `offset`、`count` 等字段；
- 详情接口通常没有分页，不要对单条详情盲目循环。

在分页、批量、循环或并发前，必须向用户说明：接口、预计请求数、单次价格、最大总扣点和限流风险，并获得用户明确确认。优先小批量、串行执行；每次成功调用都要按实际返回的停止条件继续或停止。批量中出现异常时暂停，先查流水再决定是否继续。

## 安全要求

- API Key 只放在安全环境变量或凭据存储中；不写入代码、日志、命令历史、截图或回复。
- 不要把 `Authorization`、Cookie、密码、支付密钥或上游凭据转发给第三方。
- 不要在用户未确认时发起可能扣费的调用。
- 不要把 `billable` 当作 HTTP API 的”免扣费开关”；实际扣费由服务端接口配置和响应规则决定。
- 不要因为工具列表、MCP 包装器或旧文档与公开目录不一致，就绕过目录查询。
- 原样保留真实业务数据；不编造空字段或成功结果。

### API Key 轮换建议

- **频次**：常规 90 天一次；发生过泄露或离职交接立即轮换。
- **步骤**：
  1. 在控制台创建新 Key（或调用 `POST /api/external/platform/api-keys/<id>/regenerate/`）。
  2. 新旧 Key **短暂并行运行 1–24 小时**，让依赖旧 Key 的调用方逐步切换。
  3. 监控旧 Key 的最后调用时间；归零即停用。
  4. 收回旧 Key（控制台”禁用”或删除）。
- **避免业务中断**：轮换窗口内不要批量并发切换；先在低流量时段验证新 Key，再全量切。
- **多环境隔离**：开发 / 测试 / 生产用不同 Key；某环境 Key 泄露不影响其他环境。

## 常见问题（FAQ）

**Q1：创建 API Key 后多久能用？**
A：立即生效。如果 `GET /points/balance` 拿不到余额，先确认 `Authorization: Bearer <key>` 头格式正确、Key 未被禁用。

**Q2：余额查不到，但 Key 是新的？**
A：先 `curl -v` 看响应头，确认请求真的带上了 `Authorization`；环境变量名 `HEYI_API_KEY` 大小写敏感。再用 `GET /platform/public/endpoints/` 匿名端点验证连通性。

**Q3：扣费和我预期对不上？**
A：始终以 `points/records` 为准。客户端不会自行扣费；客户端看到的”预计扣点”只是按规则推算，实际可能因为上游失败、超时或免费时段而不扣。

**Q4：`npx heyihub-skill check` 一直报 `retired` / `changed`，怎么办？**
A：先看 diff 是哪些 endpoint；若是 V1 接口被废弃（已在 description 加 `[已废弃]`），就切到推荐的 V2 接口；若是价格变动，确认 `cost-config` 与目录详情一致即可。

**Q5：批量调用中途余额不足会被中断吗？**
A：服务端按单次调用扣费，遇到 `402 / 4003` 时**当前请求不扣费**且后续请求会被服务端拒绝。批量脚本应在每轮循环检查余额，提前 10% 停止。

**Q6：同一接口可以同时用多种认证方式调用吗？**
A：可以。`apps/api/authentication.py` 同时识别多种 `Authorization` 头。但本 Skill 只覆盖 API Key 路径；仅限后台凭据使用的接口（后台管理）请勿混入。

**Q7：MCP 包装器报 `billable=false`，调用真的免费吗？**
A：不一定。某些 MCP 实现把 `billable` 当作客户端标记，与后端扣费规则无关。**最终扣费以 `points/records` 为准**。

**Q8：旧 Skill 报 401 但 Key 没换？**
A：常见原因是 `HEYI_API_BASE_URL` 指向了旧域名（`api.heyi.cloud` 之类），或 Agent 工作台没重启仍加载旧 `SKILL.md`。先确认 Base URL，再重启 Agent。

## 监控建议（生产级使用）

定期拉取以下数据建立监控/告警：

| 指标 | 来源 | 频率 |
| --- | --- | --- |
| 余额 | `GET /points/balance` | 每 5–15 分钟；< 阈值告警 |
| 当日消耗 | `GET /points/records?change_type=consume&start_time=...` | 每小时聚合 |
| 错误率 | 业务 `code != 200/2000` 占比 | 实时；> 5% 告警 |
| `429` 频率 | 响应 `Retry-After` / 客户端日志 | 实时；连续触发降并发 |
| 5xx 比例 | 服务端 5xx / 总调用 | 实时；> 1% 触发暂停 |

**预算硬上限**：建议在客户端写一个 wrapper，超出预算时直接拒绝调用，避免被脚本跑飞消耗光积分。批量任务**始终**在循环里检查余额。

## 可选适配：MCP

MCP 只是本 API 的工具包装层，不是调用前提。使用 MCP 时仍遵循本 Skill 的接口发现、用户确认、参数、扣费和重试规则。某些 MCP 的 `billable` 参数只影响客户端如何标记 `charged`，不能阻止后端扣费；最终以 API 响应和 `points/records` 为准。

## 验证方式

只验证连通性时，先调用匿名目录：

```bash
curl --fail-with-body \
  "$HEYI_API_BASE_URL/api/external/platform/public/endpoints/"
```

验证 API Key 时，再调用只读余额接口。仓库内 skill 回归测试：

```bash
node tests/test_heyi_paid_api_skill.mjs
```

### 运行期自检（check）

```bash
npx heyihub-skill check              # 或 npx heyihub-skill check
npx heyihub-skill check --strict     # 让 added（新增接口）也退出码 1
npx heyihub-skill check --base-url https://bot.01011.top
```

`check` 拉取远端公开目录，与 npm 包内嵌快照 `snapshots/catalog.json` 对比，分类报告：

- `retired`（已下线）：本地快照有但远端缺——很可能导致 `4040`，请升级 Skill 或排查 SKILL.md 中相关章节。
- `changed`（契约变动）：`(code, method, path)` 相同，但 `category / group_code / 价格 / 折扣` 任一不同——升级后调用前最好重新读公开目录详情。
- `added`（新增接口）：远端有但本地快照没有——默认 **soft**（不报错），加 `--strict` 后才退出码 1。

退出码：

- `0` 一致，或仅有 `added`（默认 soft）
- `1` 发现 `retired` / `changed`（`--strict` 时 `added` 也算）
- `2` 网络/HTTP/JSON 失败，或快照文件缺失

建议在以下时机跑一次：升级 Skill 之后、首次接入、长期未升级、排查 `4040` 之前。开发期可用 `npx heyihub-skill snapshot`（或 `node bin/install.js snapshot`）重新生成 `snapshots/catalog.json`，随 npm release 发布。
