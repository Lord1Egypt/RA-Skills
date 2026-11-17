---
name: linkfox-amazon-opportunity-report-by-keyword
description: 按关键词查询亚马逊商业洞察报告，包含市场潜力、产品特征、用户评论、人群画像、搜索趋势及定价分析。
---

# 亚马逊-机会报告（Amazon Market Opportunity Report）

本技能用于按关键词生成亚马逊商业洞察报告，帮助卖家基于数据做出选品与市场进入决策。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 按关键词生成亚马逊商业洞察报告，基于实时亚马逊数据由 AI 分析六大维度：市场潜力、产品特征、用户评论、客户画像、搜索趋势、定价分析。
- 报告以结构化 Markdown 文档形式交付，作为选品与市场进入的决策支持。

### ❌ 边界与限制

- **仅支持美国站**：当前 `site` 仅支持 `US`（美国市场），用户请求其他站点时需告知本工具暂不支持。
- **非结构化输出**：返回 Markdown 报告，而非结构化 JSON 数据；不能与数据查询工具配合做二次聚合分析。
- **生成耗时**：报告涉及 AI 分析，耗时长于普通数据查询。
- **快照数据**：报告反映生成时点的数据，不会持续更新。
- **不在范围内**：实时关键词排名追踪（用 ABA 或 SIF 工具）；单品详情查询（用商品详情工具）；历史价格追踪（用 Keepa）；指定 ASIN 的评论级分析（用评论工具）；广告/PPC 策略。

## 核心概念

本工具通过分析亚马逊关键词的六大核心维度，生成综合商业洞察报告：

1. **市场潜力（Market Potential）**：搜索量、需求趋势与增长机会。
2. **产品特征（Product Characteristics）**：常见商品属性、材质、功能。
3. **用户评论（User Reviews）**：客户情感、痛点与满意度驱动因素。
4. **客户画像（Customer Profile）**：买家人群特征、偏好与行为模式。
5. **搜索趋势（Search Trends）**：关键词热度走势与季节性。
6. **定价分析（Pricing Analysis）**：价格分布与竞争价格格局。

报告由 AI 基于实时亚马逊数据生成，以结构化 Markdown 文档交付。它是用于决策支持的快照分析，而非实时监控工具。

## 调用方式

- **API 端点**：`POST /amazon/opportunity/reportByKeyword`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/amazon_opportunity_report.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-opportunity-report-by-keyword-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 基础商业洞察报告**
```
帮我搜索美国站，关键词是 hair mousse travel size 的商业洞察报告
```

**2. 细分品类调研**
```
帮我生成美国站关键词 magnetic shelves for whiteboard 的商业洞察报告
```

**3. 趋势选品**
```
我想了解美国站 solar power ac unit 这个关键词的商业洞察，帮我生成报告
```

## 展示规则

1. **直接呈现报告**：API 在 `stdout` 字段返回 Markdown 格式报告，原样展示给用户。
2. **不做主观建议**：呈现 AI 生成的分析，不添加自己的商业建议。
3. **说明数据范围**：提醒用户报告基于时点快照，作为决策参考。
4. **错误处理**：查询失败时，依据 `msg` 字段说明原因，并建议检查关键词或重试。
5. **不支持二次分析**：本工具的输出不能作为数据查询工具的输入做进一步处理，若用户尝试需告知限制。

## 用户表达与场景速查

**适用** —— 关键词级别的综合市场分析：

| 用户说 | 场景 |
|--------|------|
| "帮我分析这个关键词的市场机会" | 市场机会评估 |
| "给 XX 生成一份市场洞察报告" | 完整洞察报告 |
| "XX 的竞争格局如何" | 竞争与定价分析 |
| "XX 产品的消费者画像" | 客户行为洞察 |
| "XX 这个关键词值不值得做" | 市场进入评估 |
| "选品报告"、"商业洞察" | 中文市场调研请求 |

不适用场景见上方【能力边界】。

**边界判断**：当用户提到"市场分析"或"选品调研"时，若希望获得关键词市场机会的整体多维度概览，则适用本技能；若需要具体数据点（精确销量、单品详情、关键词历史排名），应引导至对应专项工具。

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

# 亚马逊商业洞察报告 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/amazon/opportunity/reportByKeyword`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）
- **User-Agent**：`LinkFox-Skill/1.0`

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| site | string | 是 | 亚马逊站点代码，当前仅支持 `US` |
| keyword | string | 是 | 要查询洞察报告的搜索关键词 |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| code | string | 响应码 |
| msg | string | 提示信息或错误信息 |
| stdout | string | 综合商业洞察报告内容（Markdown 格式），包含市场潜力、产品特征、用户评论、客户画像、搜索趋势、定价分析六大维度 |
| costTime | integer | 总处理耗时（毫秒） |
| costToken | integer | token 消耗量 |
| type | string | 响应类型 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 code 字段区分。当遇到未授权等情况时，HTTP 状态码为 401。

| 错误码 | 含义 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | 正常解析 `stdout` 字段，将 Markdown 报告展示给用户 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 其他非200值 | 业务异常 | 参考 `msg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/amazon/opportunity/reportByKeyword \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/1.0" \
  -d '{"site": "US", "keyword": "ice bricks"}'
```
