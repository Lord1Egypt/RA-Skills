---
name: linkfox-zhihuiya-fulltext-image
description: 智慧芽专利全文附图获取工具。支持查看和下载专利文件内部嵌入的所有视觉图纸、技术示意图与图表。
---

# 智慧芽-专利全文附图获取（Zhihuiya Patent Fulltext Image）

本技能通过智慧芽专利数据服务获取专利文件中嵌入的全文附图（图纸、示意图、图表），帮助用户访问并分析专利中的视觉内容。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过 **专利ID**（`patentId`，内部标识）或 **公开号**（`patentNumber`，如 `US20230012345A1`、`CN115000000A`）查询专利全文附图。
- 返回每张图片的下载路径（`fulltextImagePath`）、图片类型（`imageType`）等元数据。
- 支持 `limit`/`offset` 分页浏览附图。

### ❌ 边界与限制

- **标识符必填**：`patentId` 与 `patentNumber` 至少需提供其中一个。
- **单次上限**：每请求最多返回 100 张图片。
- **参数类型**：所有参数值均为字符串类型，数值型参数（如 `limit`、`offset`）也须以字符串传入，最大长度 1000 字符。
- **不在范围内**：专利文本/摘要/权利要求检索；专利同族或引证分析；专利法律状态查询；专利申请人或发明人检索；与专利无关的通用图片搜索。

## 核心概念

专利全文附图是嵌入在专利文件中的图纸、示意图与图表，对理解发明技术细节至关重要。本工具查询智慧芽专利数据库，针对指定专利返回图片元数据（下载路径与图片类型）。

**查询方式**：可通过 **专利ID**（内部标识）或 **公开号**（对外公开的专利号，如 `US20230012345A1`、`CN115000000A`）查询，二者至少提供一个。

## 调用方式

- **API 端点**：`POST /zhihuiya/fulltextImage`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_fulltext_image.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改参数连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-fulltext-image-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 按公开号获取专利全部附图**
```
获取专利 US20230012345A1 的全文附图。
```
参数：`{"patentNumber": "US20230012345A1"}`

**2. 按专利ID获取附图**
```
获取专利ID为 abc123def456 的图纸。
```
参数：`{"patentId": "abc123def456"}`

**3. 分页获取附图**
```
获取专利 CN115000000A 的前 20 张附图。
```
参数：`{"patentNumber": "CN115000000A", "limit": "20", "offset": "0"}`

**4. 获取下一页附图**
```
获取专利 CN115000000A 的第 21-40 张附图。
```
参数：`{"patentNumber": "CN115000000A", "limit": "20", "offset": "20"}`

## 展示规则

1. **清晰呈现数据**：以结构化表格展示图片类型、下载路径与专利号。
2. **图片链接**：始终将 `fulltextImagePath` 以可点击链接形式呈现，便于用户直接查看或下载图片。
3. **分页提示**：当 `total` 超过当前返回数量时，告知用户还有更多附图，并询问是否获取下一页。
4. **错误处理**：查询失败时说明原因，并建议核对专利ID或公开号。
5. **禁止编造**：不得捏造专利ID、公开号或图片URL，仅展示 API 返回的数据。
6. **总数提示**：始终说明该专利可用的附图总数。

## 用户表达与场景速查

**适用** —— 涉及专利视觉内容的请求：

| 用户说 | 场景 |
|--------|------|
| "看看专利 XX 的图纸" | 全文附图获取 |
| "获取这个专利的附图" | 全文附图获取 |
| "下载专利 XX 的图片" | 全文附图获取 |
| "专利 XX 里有几张图" | 附图数量查询 |
| "专利 XX 包含哪些示意图" | 附图列举 |
| "看一下技术图纸" | 全文附图获取 |

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

# 智慧芽-全文附图 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/fulltextImage`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | 否* | 专利ID |
| patentNumber | string | 否* | 公开(公告)号 |
| limit | string | 否 | 返回图片总量，最大100，默认 `"100"` |
| offset | string | 否 | 偏移量 |

> *`patentId` 和 `patentNumber` 至少需提供其中一个。

- 所有参数值均为字符串类型，最大长度 1000 字符。

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 专利列表 |
| data[].patentId | string | 专利Id |
| data[].pn | string | 公开(公告)号 |
| data[].fulltextImagePath | string | 图片路径 |
| data[].imageType | string | 图片类型 |
| columns | array | 渲染的列 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 402 | - | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/fulltextImage \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US20230012345A1", "limit": "100", "offset": "0"}'
```
