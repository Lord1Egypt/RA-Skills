---
name: linkfox-amazon-ads-manager
description: 管理亚马逊 SP/SB/SD 广告的查询与创建、修改、调价等写操作。
---


# Amazon Ads 广告管理

亚马逊广告管理 skill，支持 SP/SB/SD 三条产品线的 list（查询）和 create / update（创建与修改）操作，自动处理 token、分页、过滤字段规范化。参数与字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询（list）SP/SB/SD 的广告活动、广告组、关键词、否定关键词、商品广告、定向、否定定向、创意等实体元数据。
- 创建/修改（create/update）上述实体，含出价调整、预算修改、状态变更、Budget Rules。
- 自动分页、过滤器结构规范化、多账号 profileId 解析。

### ❌ 边界与限制

- **只给 metadata，不含指标**：返回实体字段（id/名称/状态/匹配类型等）；曝光/点击/花费/转化等指标交给 `linkfox-amazon-ads-report`，按 id join。
- **不支持 DELETE**：可通过 update state 为 `ARCHIVED` 实现归档，但归档不可逆。
- **SB keywords/targets 等无 list all**：Amazon 官方未提供，需按 id 单查（不在本 skill）。
- **SD 非基础实体接口不在范围内**：按 id 单查、brandSafety、recommendations、forecasts、optimizationRules、locations 等。
- **DSP / ST 实体不在本 skill**。
- **依赖 `linkfox-amazon-ads-auth`**：未安装时 exit 42，stderr 打 `DEPENDENCY_MISSING`。
- 授权 / token / profile 交给 `linkfox-amazon-ads-auth`；指标报表交给 `linkfox-amazon-ads-report`。

## 执行流程

### 1. 解析 profileId（多账号场景，调用前必做）

【输入】用户自然语言提及的站点/账号（如"美国站"、"日本站"、"我的店铺"）。
【动作】按下列顺序处理，不要跳过：
1. 调 `linkfox-amazon-ads-auth` 的 `authorized_stores.py` 拉出已授权账号 × 站点清单。
2. 按用户提到的站点映射到 `countryCode`（如 美国→`US`）匹配候选 profile：
   - 只有 1 个候选 → 静默取对应 profileId，继续调用；不要把 profileId 数字播报给用户。
   - ≥ 2 个候选（同站点多个授权账号）→ 必须向用户澄清，用 `accountName` 问："你在美国站授权了 A 和 B 两个账号，这次用哪个？"
   - 0 个候选 → 告知该站点未授权，引导去 `linkfox-amazon-ads-auth` 做授权。
3. 严禁让用户直接报 profileId 数字；严禁在歧义下"挑第一个"绕过澄清。
【输出】确定本次调用所需的数字 `profileId`（内部使用，不播报）。完整决策表见 `linkfox-amazon-ads-auth` SKILL.md 的 Usage Scenarios 第 4 节。

### 2. 选择脚本与构造参数

【输入】profileId、用户意图（查询/创建/修改哪个实体）、过滤或变更字段。
【动作】按下方「可用脚本」一览选择 `scripts/<sp|sb|sd>/<op>.py`；按 [references/api.md](references/api.md) 及对应子文档（[sp.md](references/api/sp.md) / [sb.md](references/api/sb.md) / [sd.md](references/api/sd.md)）构造 JSON 参数（共用参数、过滤器结构、枚举值）。
【输出】一条合法的 JSON 参数字符串。

### 3. 执行调用与输出

【输入】脚本名 + JSON 参数。
【动作】运行 `python scripts/<脚本名>.py '<JSON 参数>' [--inline]`。写操作（create/update）按下方「财务安全指引」先确认再执行；非 2xx 不自动重试。
【输出】完整响应落盘到 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-ads-manager-<timestamp>.json`；stdout 按大小输出摘要或全量（`--inline` 强制全量）。失败时保留 `httpStatus` + `body` 告知用户。

## 可用脚本

脚本路径前缀为 `scripts/`，下表列各实体的查询/创建/修改脚本名。

### SP（Sponsored Products v3）

| 实体 | 查询 | 创建 | 修改 |
|------|------|------|------|
| 广告活动 | `sp/list_campaigns.py` | `sp/create_campaigns.py` | `sp/update_campaigns.py` |
| 广告组 | `sp/list_ad_groups.py` | `sp/create_ad_groups.py` | `sp/update_ad_groups.py` |
| 关键词 | `sp/list_keywords.py` | `sp/create_keywords.py` | `sp/update_keywords.py` |
| 否定关键词 | `sp/list_negative_keywords.py` | `sp/create_negative_keywords.py` | `sp/update_negative_keywords.py` |
| 商品广告 | `sp/list_product_ads.py` | `sp/create_product_ads.py` | `sp/update_product_ads.py` |
| 商品定向 | `sp/list_targets.py` | `sp/create_targets.py` | `sp/update_targets.py` |

额外：活动级否定关键词 `sp/create|update_campaign_negative_keywords.py`、活动级否定定向 `sp/create|update_campaign_negative_targets.py`、广告组级否定定向 `sp/create|update_negative_targets.py`、预算规则 `sp/list|create|update_budget_rules.py`、预算规则关联 `sp/create_budget_rules_association.py`。

### SB（Sponsored Brands v4）

| 实体 | 查询 | 创建 | 修改 |
|------|------|------|------|
| 广告活动 | `sb/list_campaigns.py` | `sb/create_campaigns.py` | `sb/update_campaigns.py` |
| 广告组 | `sb/list_ad_groups.py` | `sb/create_ad_groups.py` | `sb/update_ad_groups.py` |
| 广告创意 | `sb/list_ads.py` | `sb/create_ads.py` | `sb/update_ads.py` |

额外：预算规则 `sb/list|create|update_budget_rules.py`。

### SD（Sponsored Display v3）

| 实体 | 查询 | 创建 | 修改 |
|------|------|------|------|
| 广告活动 | `sd/list_campaigns.py` | `sd/create_campaigns.py` | `sd/update_campaigns.py` |
| 广告组 | `sd/list_ad_groups.py` | `sd/create_ad_groups.py` | `sd/update_ad_groups.py` |
| 商品广告 | `sd/list_product_ads.py` | `sd/create_product_ads.py` | `sd/update_product_ads.py` |
| 定向子句 | `sd/list_targets.py` | `sd/create_targets.py` | `sd/update_targets.py` |
| 否定定向子句 | `sd/list_negative_targets.py` | `sd/create_negative_targets.py` | `sd/update_negative_targets.py` |
| 创意素材 | `sd/list_creatives.py` | `sd/create_creatives.py` | `sd/update_creatives.py` |

额外：预算规则 `sd/list|create|update_budget_rules.py`。详细过滤器、枚举值、返回字段见 [references/api/sp.md](references/api/sp.md) / [references/api/sb.md](references/api/sb.md) / [references/api/sd.md](references/api/sd.md)。

## 调用方式

- **API 端点**：`POST /amazonAds/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。
- **输出策略**：始终将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-ads-manager-<timestamp>.json`（`<session>` 取自环境变量 `SESSION_ID`；禁止写入 /tmp，不可写则报错）；响应体 ≤ 8 KB 落盘后打印完整 JSON 到 stdout，> 8 KB 仅输出摘要；`--inline` 强制全量打印（同样落盘）。
- **读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取。

共用参数、过滤器结构、枚举值、错误码见 [references/api.md](references/api.md)。核心机制：自动分页（`fetchAll` 默认 true，SP/SB 用 `nextToken`、SD 用 `startIndex+count`，`maxPages=50` 兜底）；过滤器结构不统一（Object/Array/Scalar/Text/Client 五类，本 skill 自动规范化）；SB 仅 3 个 list、SD 为 GET + querystring。

## 财务安全指引

创建和更新操作可能直接影响广告花费，立即生效且无法撤回。

| 用户状态 | Agent 行为 |
|----------|-----------|
| 已授权（说过"自动调价"/"按你判断来"/"不用问我"/"确认"等） | 直接执行 → 输出操作回执 |
| 未授权（首次交互、未明确表态） | 先输出确认摘要 → 等用户确认后执行 |

**确认摘要模板**（未授权时，执行前输出）：
```
📋 即将执行：
- 操作：[创建/修改] [N 个] [实体类型]
- 变更：[关键字段变化，如 bid $1.0→$1.5 / budget $50→$100]
- 影响：[花费变化预估，引用日预算作为上限]
确认执行？后续如需自动处理，告诉我即可。
```

**操作回执模板**（每次写操作执行后必须输出）：
```
✅ 已执行：[简短描述]
- 范围：[实体数量、名称或 ID]
- 变化：[具体变更内容]
- 结果：[成功 N 个 / 失败 M 个]
```

## 使用示例

### 1. 列活跃 SP 广告活动
```bash
python scripts/sp/list_campaigns.py '{"profileId":1234567890,"region":"NA",
  "stateFilter":{"include":["ENABLED"]}}'
```

### 2. 看某 SP campaign 下的广告组
```bash
python scripts/sp/list_ad_groups.py '{"profileId":1234567890,"region":"NA",
  "campaignIdFilter":{"include":["998877665544"]}}'
```

### 3. 按 ASIN 反查 SP 投放（客户端过滤）
```bash
python scripts/sp/list_product_ads.py '{"profileId":1234567890,"region":"NA",
  "asinFilter":{"include":["B01ABCDEFG"]},
  "campaignIdFilter":{"include":["998877665544"]}}'
```

### 4. 与 report 配合分析指标
本 skill 返回实体元数据；指标（曝光、点击、花费、转化）交给 `linkfox-amazon-ads-report`（`reportTypeId: "spTargeting"` / `"sbCampaigns"` / `"sdCampaigns"` 等），按 id join。

## 展示规则

1. 返回字段原样保留，不改名、不翻译、不补算派生指标。
2. `truncated=true` 时明确提示数据未取完。
3. 写操作必须输出操作回执（见「财务安全指引」）。
4. 查询失败时说明原因并建议调整参数（如放宽筛选、核对过滤器结构）。

## 用户表达与场景速查

**适用** —— 亚马逊 SP/SB/SD 广告查询与写操作：

| 用户说 | 场景 |
|--------|------|
| "看下我的 SP 广告活动"、"列下活跃广告" | 查询广告活动 |
| "某 campaign 下的广告组/关键词" | 查询子实体 |
| "按 ASIN 反查投放" | 商品广告客户端过滤 |
| "把某关键词出价调到 $1.5" | 修改出价 |
| "把某活动预算改到 $100" | 修改预算 |
| "暂停某广告组" | 状态变更 |
| "创建一个 SP 广告活动" | 创建实体 |
| "给某活动加预算规则" | Budget Rules |

不适用场景见上方【能力边界】。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用 skill 内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个 skill 并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个 skill。

---

# linkfox-amazon-ads-manager — 参数与字段参考（总览）

按 Amazon Ads 广告产品分类维护。

| 广告产品 | 脚本子目录 | 查询参考 |
|---------|-----------|---------|
| **Sponsored Products (SP)** — v3 | `scripts/sp/` | [api/sp.md](./api/sp.md) |
| **Sponsored Brands (SB)** — v4 | `scripts/sb/` | [api/sb.md](./api/sb.md) |
| **Sponsored Display (SD)** — v3 | `scripts/sd/` | [api/sd.md](./api/sd.md) |

> Sponsored Television (ST) / Amazon DSP 暂未覆盖。

## 通用约定

- 每个脚本接受一个 JSON 字符串作为唯一位置参数
- 鉴权：环境变量 `LINKFOX_AGENT_API_KEY`（或旧名 `LINKFOXAGENT_API_KEY`）（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）
- API 网关地址：环境变量 `LINKFOX_TOOL_GATEWAY`（默认 `https://tool-gateway.linkfox.com`）
- 依赖 `linkfox-amazon-ads-auth`（脚本启动自动检查；缺失时 exit 42，stderr 打 `DEPENDENCY_MISSING`）

## 共用参数（SP + SB + SD 均适用）

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `profileId` | number | ✅ | — | 从 ads-auth 获取 |
| `region` | string | ✅ | — | `NA` / `EU` / `FE` |
| `fetchAll` | boolean | 否 | `true` | 自动翻页（SP / SB 跟 `nextToken`，SD 用 `startIndex + count`） |
| `maxResults` | integer | 否 | `100` | 单页 1-100；超限上游可能静默 clamp；对应 SD 端 `count` |
| `skipDepCheck` | boolean | 否 | `false` | 跳过依赖检查 |
| `includeExtendedDataFields` | boolean | 否 | — | 返回扩展字段（部分实体）；SD 通过路径切换为 `/sd/<entity>/extended` 实现 |
| `locale` | string | 否 | — | 本地化（keywords 支持） |

## 输出格式

```json
{
  "success": true,
  "<entityKey>": [ /* 实体数组 */ ],
  "total": 157,
  "pagesFetched": 2,
  "truncated": false
}
```

客户端过滤时（SP productAds 的 asinFilter/skuFilter）额外带 `serverTotalBeforeClientFilter` + `clientSideFilters`。

失败：
```json
{
  "error": "Upstream HTTP 401",
  "httpStatus": 401,
  "body": "...",
  "pagesFetched": 0
}
```

## 通用错误码

| httpStatus / exit | 含义 | 建议 |
|-------------------|------|------|
| 200 | 成功 | — |
| 400 | 入参结构错 | 核对对应 adProduct 的过滤器结构（api/sp.md / api/sb.md / api/sd.md） |
| 401 | accessToken 过期 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 402 | 积分或余额不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 403 | profileId 无权限 | 核对 profileId 归属 |
| 429 | 限流 | 间隔 2-5s 重试 |
| exit 42 | 依赖 skill 未安装 | 先装 `linkfox-amazon-ads-auth` |
