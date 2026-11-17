---
name: linkfox-amazon-store-customer-feedback
description: 亚马逊店铺买家反馈洞察。支持分析 ASIN 或类目节点的评论主题、评价趋势、退货原因及星级影响。
---

# 亚马逊店铺买家反馈（Amazon Store Customer Feedback）

本 skill 与 **`linkfox-amazon-store-auth`** 等同属 Amazon Store 系列：先 `POST /spApi/storeTokens`，再 `POST /spApi/developerProxy` 转发 `GET`。接口属于 Customer Feedback（买家评论/退货洞察），不是 Orders 订单 API；订单见 `linkfox-amazon-store-orders`。完整参数、响应与错误码见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 调用 SP-API Customer Feedback **v2024-06-01**，分析 ASIN 或 browse node 的评论主题、评价趋势、退货主题与退货趋势。
- 支持按 `MENTIONS` / `STAR_RATING_IMPACT` 排序评论主题，对比买家关注点与星级影响。
- 通过 `get_item_browse_node` 由 ASIN 反查类目节点，再下钻类目级反馈。

### ❌ 边界与限制

- **前置依赖**：依赖 `linkfox-amazon-store-auth` 完成授权；未授权无法调用。
- **非订单接口**：订单查询见 `linkfox-amazon-store-orders`。
- **角色要求**：通常需 Brand Analytics 或 Selling Partner Insights 等角色；站点以官方为准（常见 US/UK/DE 等）。
- **ASIN 口径**：一般为子体 ASIN；topics 类接口需 `sortBy`（`MENTIONS` 或 `STAR_RATING_IMPACT`）。
- **网关白名单**：需放行 `customerFeedback/2024-06-01/`。
- **数据时效**：刷新频率以 Amazon 为准（通常按周）。
- **成本约束**：本工具消耗积分；失败/空结果不得自动换关键词、翻页或连续试探；继续检索前先向用户说明额外消耗。

## 执行流程

复杂 skill：多接口编排，建议按以下顺序逐步调用。

### 步骤 1 — ASIN 评论主题

- 【输入】`sellerId`、`region`、`marketplaceId`、`asin`、`sortBy`
- 【动作】运行 `get_item_review_topics.py`，`sortBy` 分别取 `MENTIONS` 与 `STAR_RATING_IMPACT` 各调一次以对比
- 【输出】`itemReviewTopics`（评论主题、提及量与星级影响）

### 步骤 2 — ASIN 评论趋势

- 【输入】`sellerId`、`region`、`marketplaceId`、`asin`
- 【动作】运行 `get_item_review_trends.py`
- 【输出】`itemReviewTrends`（评价趋势）

### 步骤 3 — 反查类目节点

- 【输入】`sellerId`、`region`、`marketplaceId`、`asin`
- 【动作】运行 `get_item_browse_node.py`
- 【输出】`itemBrowseNode`（取得 `browseNodeId`）

### 步骤 4 — 类目级反馈

- 【输入】`sellerId`、`region`、`marketplaceId`、`browseNodeId`（来自步骤 3）；topics 接口另需 `sortBy`
- 【动作】按需运行 `get_browse_node_review_topics` / `get_browse_node_review_trends` / `get_browse_node_return_topics` / `get_browse_node_return_trends`
- 【输出】`browseNodeReviewTopics` / `browseNodeReviewTrends` / `browseNodeReturnTopics` / `browseNodeReturnTrends`

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）。
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见下方使用示例）。
- **成本约束**：失败/空结果不得自动换关键词、翻页或连续试探；继续检索前先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：

- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-customer-feedback-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）。
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout。
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）。
- 加 `--inline` 强制全量打印到 stdout（同样落盘）。

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_item_review_topics.py '{"sellerId":"A1...","region":"NA","asin":"B0...","marketplaceId":"ATVPDKIKX0DER","sortBy":"MENTIONS"}'

python scripts/get_item_browse_node.py '{"sellerId":"A1...","region":"NA","asin":"B0...","marketplaceId":"ATVPDKIKX0DER"}'

python scripts/get_browse_node_review_topics.py '{"sellerId":"A1...","region":"NA","browseNodeId":"123456","marketplaceId":"ATVPDKIKX0DER","sortBy":"STAR_RATING_IMPACT"}'
```

## 展示规则

1. 先看 `developerProxy.errcode` / `httpStatus`，再读各脚本解析字段（如 `itemReviewTopics`）。
2. 网关白名单需包含 `customerFeedback/2024-06-01/`。
3. 数据刷新频率以 Amazon 为准（通常按周）。
4. 以结构化表格呈现评论主题、提及量、星级影响与趋势变化，只呈现数据，不做主观商业建议。

## 用户表达与场景速查

**适用** —— 亚马逊 ASIN / 类目节点买家反馈洞察：

| 用户说 | 场景 |
|--------|------|
| "这个 ASIN 的评论主题是什么"、"买家最关心什么" | ASIN 评论主题（MENTIONS） |
| "哪些主题拉低了星级"、"星级影响" | ASIN 评论主题（STAR_RATING_IMPACT） |
| "这个 ASIN 评价趋势"、"评论走势" | ASIN 评论趋势 |
| "这个 ASIN 属于哪个类目"、"反查 browse node" | ASIN 类目节点 |
| "这个类目的评论主题"、"类目买家反馈" | browse node 评论主题 |
| "这个类目退货原因"、"退货主题" | browse node 退货主题 |
| "类目评价趋势"、"类目退货趋势" | browse node 趋势 |

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

# linkfox-amazon-store-customer-feedback — API 参考

Customer Feedback **v2024-06-01**，经 LinkFox `storeTokens` + `developerProxy` 调用。

官方总览：[Customer Feedback API](https://developer-docs.amazon.com/sp-api/docs/customer-feedback-api-v2024-06-01-use-case-guide)

---

## 1. 脚本与 path

| 脚本 | GET path |
|------|----------|
| `get_item_review_topics.py` | `customerFeedback/2024-06-01/items/{asin}/reviews/topics` |
| `get_item_browse_node.py` | `customerFeedback/2024-06-01/items/{asin}/browseNode` |
| `get_item_review_trends.py` | `customerFeedback/2024-06-01/items/{asin}/reviews/trends` |
| `get_browse_node_review_topics.py` | `customerFeedback/2024-06-01/browseNodes/{browseNodeId}/reviews/topics` |
| `get_browse_node_review_trends.py` | `customerFeedback/2024-06-01/browseNodes/{browseNodeId}/reviews/trends` |
| `get_browse_node_return_topics.py` | `customerFeedback/2024-06-01/browseNodes/{browseNodeId}/returns/topics` |
| `get_browse_node_return_trends.py` | `customerFeedback/2024-06-01/browseNodes/{browseNodeId}/returns/trends` |

前缀均为 `customerFeedback/2024-06-01/`；共享模块：`_spapi_customer_feedback_common.py`。

---

## 2. 公共入参

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId | 是 | 卖家 ID |
| region | 是 | `NA` / `EU` / `FE` 等 |
| marketplaceId | 是 | 单站点；或 `marketplaceIds` 数组取第一个 |
| skipDepCheck | 否 | 跳过依赖检查 |

---

## 3. 按接口

### getItemReviewTopics / getBrowseNodeReviewTopics / getBrowseNodeReturnTopics

| 字段 | 必填 |
|------|------|
| asin 或 browseNodeId | 是（按接口） |
| sortBy | 是 | `MENTIONS` \| `STAR_RATING_IMPACT` |

Query：`marketplaceId`、`sortBy`

解析字段：`itemReviewTopics` / `browseNodeReviewTopics` / `browseNodeReturnTopics`

### getItemBrowseNode

| 字段 | 必填 |
|------|------|
| asin | 是 |

Query：`marketplaceId`
解析字段：`itemBrowseNode`

### getItemReviewTrends / getBrowseNodeReviewTrends / getBrowseNodeReturnTrends

Query：`marketplaceId`
解析字段：`itemReviewTrends` / `browseNodeReviewTrends` / `browseNodeReturnTrends`

---

## 4. 推荐调用顺序（ASIN）

1. `get_item_review_topics`（`sortBy=MENTIONS` 与 `STAR_RATING_IMPACT` 各一次）
2. `get_item_review_trends`
3. `get_item_browse_node` → 取 `browseNodeId`
4. 对 browse node 调用 review/return 的 topics 与 trends

---

## 5. 限制

- 非订单接口；订单用 `linkfox-amazon-store-orders`。
- **401**：HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。
- **402**：HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。
- **403**：角色或站点不支持。
- **1005**：网关需放行 `customerFeedback/2024-06-01/`。
