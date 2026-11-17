---
name: linkfox-zhihuiya-patent-family
description: 智慧芽专利家族查询工具。支持检索简单同族和 INPADOC 同族成员，用于查找跨国等同专利。
---

# 智慧芽专利家族查询（Zhihuiya Patent Family）

本技能通过智慧芽（PatSnap）平台查询专利家族信息，帮助用户发现给定专利的 Simple Family、INPADOC Family 与 PatSnap Family 成员。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过专利ID或公开号查询专利家族成员，覆盖 **简单同族（Simple Family）**、**INPADOC同族**、**PatSnap同族** 三种定义。
- 支持单条与批量查询（单次最多 100 条专利）。
- 用于查找跨国等同专利、了解专利在不同国家/地区的布局范围。

### ❌ 边界与限制

- **仅查询已知专利**：本工具仅检索已知专利ID/公开号的家族信息，不能按关键词进行专利全文检索或分类码检索。
- **批量上限**：单次请求最多 100 条专利ID或公开号。
- **数据来源**：家族数据来自智慧芽（PatSnap）数据库，相对最新专利局公开可能存在轻微延迟。
- **家族成员详情**：返回的家族成员为摘要对象；若需某成员的完整书目数据，可能需要单独查询。
- **不在范围内**：专利全文检索、专利估值或诉讼数据、自由实施（FTO）/侵权分析、专利申请提交或审查流程。

## 调用方式

- **API 端点**：`POST /zhihuiya/patentFamily`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_patent_family.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-patent-family-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 核心概念

**专利家族**是一组因优先权主张而相互关联的专利文献。不同家族定义对应不同的关联范围：

- **简单同族（Simple Family）**：共享完全相同的一组优先权申请的专利，通常是在不同国家/地区申请的直接等同专利。
- **INPADOC同族**：由欧洲专利局定义的更宽泛分组，链接所有至少共享一个共同优先权（即使是间接共享）的专利。
- **PatSnap同族**：智慧芽（PatSnap）专有家族定义，在 INPADOC 逻辑基础上扩展了启发式规则，以捕捉分案、续案等相关申请。

响应中每条专利都带有自己的 `simpleFamilyId`、`inpadocFamilyId` 与 `patsnapFamilyId`，作为各定义下家族分组的唯一标识。

## 使用示例

**1. 按公开号查询家族成员**
> "查一下 US10000001B2 的专利家族"
```json
{"patentNumber": "US10000001B2"}
```

**2. 批量查询多项专利的家族**
> "查这几个专利的 INPADOC 同族：EP3000001A1, CN112345678A, JP2020123456A"
```json
{"patentNumber": "EP3000001A1,CN112345678A,JP2020123456A"}
```

**3. 按专利ID查询**
> "用专利ID查家族：5af83e12-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```json
{"patentId": "5af83e12-xxxx-xxxx-xxxx-xxxxxxxxxxxx"}
```

**4. 对比不同家族范围**
> "我想看看 US20200012345A1 的简单同族和 INPADOC 同族有什么区别"
```json
{"patentNumber": "US20200012345A1"}
```
随后对比响应中的 `simpleFamily` 与 `inpadocFamily` 数组。

## 展示规则

1. **清晰呈现数据**：以结构化表格展示专利家族结果；用户要求对比时，按家族类型（Simple、INPADOC、PatSnap）分组展示。
2. **汇总数量**：始终说明每种家族定义下找到的成员数量，便于用户快速判断地域覆盖广度。
3. **突出国家/地区**：列出家族成员时，标明覆盖的国家/地区，帮助用户理解专利的地域保护范围。
4. **错误处理**：当 API 返回错误或空结果时，说明可能原因（公开号格式不正确、数据库中未找到该专利等），并给出修正建议。
5. **批量结果组织**：批量查询多个专利时，按专利分组组织结果，便于用户查找各专利的家族。
6. **不做主观法律建议**：仅呈现客观家族数据，不对专利保护范围、有效性或侵权提供法律意见。

## 用户表达与场景速查

**适用** —— 专利家族与等同专利查询：

| 用户说 | 场景 |
|--------|------|
| "XX 的专利家族" | 直接家族查询 |
| "这个专利的等同专利有哪些" | 简单同族查询 |
| "这个专利在哪些国家申请了" | 通过家族了解地域覆盖 |
| "INPADOC 同族成员" | 宽范围家族查询 |
| "相关专利 / 兄弟专利" | 家族探索 |
| "对比简单同族和扩展同族" | 多定义对比 |
| "批量查这些专利的家族" | 批量家族查询 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用skill内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个skill并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个skill。

---

# 智慧芽专利家族查询 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/patentFamily`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | 条件必填 | 专利ID，专利ID和公开号两个参数必须要有一个，如果两个都存在，会优先使用专利ID。多个用英文逗号隔开，上限100条。最大长度：60000字符 |
| patentNumber | string | 条件必填 | 公开公告号，专利ID和公开号两个参数必须要有一个，如果两个都存在，会优先使用专利ID。多个用英文逗号隔开，上限100条。最大长度：60000字符 |

- `patentId` 和 `patentNumber` 至少需要提供一个
- 如果两个参数都提供，API 会优先使用 `patentId`，忽略 `patentNumber`

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 专利家族结果列表（详见下方） |
| columns | array | 渲染的列定义 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

### data[] 对象字段

| 字段 | 类型 | 说明 |
|------|------|------|
| patentId | string | 专利ID |
| pn | string | 公开(公告)号 |
| simpleFamilyId | integer | 简单同族ID |
| simpleFamily | array | 简单同族专利列表 |
| inpadocFamilyId | integer | INPADOC同族ID |
| inpadocFamily | array | INPADOC同族专利列表 |
| patsnapFamilyId | integer | PatSnap同族ID |
| patsnapFamily | array | PatSnap同族专利列表 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析 `data` 等业务字段 |
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

### 通过公开号查询

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/patentFamily \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US10000001B2"}'
```

### 通过专利ID查询

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/patentFamily \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentId": "5af83e12-xxxx-xxxx-xxxx-xxxxxxxxxxxx"}'
```

### 批量查询多个公开号

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/patentFamily \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US10000001B2,EP3000001A1,CN112345678A"}'
```
