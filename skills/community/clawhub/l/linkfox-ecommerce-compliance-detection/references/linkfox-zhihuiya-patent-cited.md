---
name: linkfox-zhihuiya-patent-cited
description: 智慧芽专利被引用（前向引用）数据查询工具。用于分析专利的影响力、被引频次及具体的引用专利详情。
---

# 智慧芽-专利被引用（前向引用）查询

本技能用于从智慧芽（PatSnap）查询专利被引用数据，帮助用户了解特定专利的被引情况与影响力。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询专利被引用次数，包括 3 年内（`citedBy3y`）与 5 年内（`citedBy5y`）被引次数。
- 查询专利同族被引情况，覆盖简单同族（`citedBySimpleFamily`）、INPADOC 同族（`citedByInpadocFamily`）与 PatSnap 同族（`citedByPatsnapFamily`）。
- 查询哪些专利引用了某一专利（`citedByPatents`）。
- 支持按公开公告号（`patentNumber`）或智慧芽内部专利 ID（`patentId`）查询，单次最多 100 条。

### ❌ 边界与限制

- **必填参数**：`patentId` 与 `patentNumber` 至少提供其一；两者同时存在时优先使用 `patentId`。
- **标识符要求**：用户提供公开公告号（如 `US10123456B2`）时用 `patentNumber`，提供内部 ID 时用 `patentId`。
- **不在范围内**：专利全文检索或语义检索；专利法律状态或审查历史；专利估值或授权许可建议；后向引用（专利自身引用的参考文献）。

## 核心概念

专利被引用分析揭示一项专利在其技术领域内的影响力。当专利 B 在其参考文献中引用了专利 A，则称专利 A「被专利 B 引用」。被引次数越高，通常意味着技术重要性越大、行业影响越广。

**关键指标**：
- **3 年被引**（`citedBy3y`）：专利公开后 3 年内被引用次数，反映早期影响。
- **5 年被引**（`citedBy5y`）：公开后 5 年内被引用次数，反映中期影响。
- **简单同族被引**（`citedBySimpleFamily`）：简单专利同族中被引专利数量。
- **INPADOC 同族被引**（`citedByInpadocFamily`）：INPADOC 专利同族中被引专利数量。
- **PatSnap 同族被引**（`citedByPatsnapFamily`）：PatSnap 定义的专利同族中被引专利数量。

## 调用方式

- **API 端点**：`POST /zhihuiya/patentCited`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_cited_by.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-patent-cited-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 按公开公告号查询单个专利被引**
> "查一下专利 US10123456B2 被引用了多少次？"
```json
{
  "patentNumber": "US10123456B2"
}
```

**2. 多个专利被引对比**
> "对比一下 CN112345678A 和 CN113456789B 的被引情况"
```json
{
  "patentNumber": "CN112345678A,CN113456789B"
}
```

**3. 按专利 ID 查询**
> "查专利 ID abc123def456 的被引数据"
```json
{
  "patentId": "abc123def456"
}
```

**4. 多个 ID 批量查询**
> "查这几个专利 ID 的被引信息：id001、id002、id003"
```json
{
  "patentId": "id001,id002,id003"
}
```

## 展示规则

1. **以表格呈现数据**：用清晰的结构化表格展示被引结果，包含公开公告号、3 年被引、5 年被引及各同族被引次数。
2. **突出关键指标**：对比多个专利时，突出被引次数最高的专利。
3. **解释同族类型**：用户不熟悉专利同族时，简要说明 Simple、INPADOC、PatSnap 同族定义的差异。
4. **引用专利详情**：响应含 `citedByPatents` 数组时，以子表或可展开列表呈现引用专利详情。
5. **错误处理**：查询失败时根据响应说明原因，并建议核对专利号或 ID 是否正确。
6. **不做主观建议**：仅呈现事实性的被引数据，不对专利价值或投资决策做判断。

## 用户表达与场景速查

**适用** —— 专利被引用分析场景：

| 用户说 | 场景 |
|--------|------|
| "这个专利被引用了多少次" | 基础被引次数查询 |
| "哪些专利引用了它" | 引用专利列表 |
| "专利影响力分析" | 基于被引的影响力评估 |
| "对比这几个专利的被引情况" | 多专利对比 |
| "3 年 / 5 年被引次数" | 时间窗口被引指标 |
| "专利同族被引数据" | 同族级被引分析 |
| "专利 X 的前向引用" | 被引查询的同义表达 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题
发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用skill内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个skill并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个skill。

---

# 智慧芽-专利被引用 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/patentCited`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | 否* | 专利ID，多个用英文逗号隔开，上限100条。如果 `patentId` 和 `patentNumber` 两个都存在，会优先使用 `patentId`。最大长度：60000字符 |
| patentNumber | string | 否* | 公开公告号，多个用英文逗号隔开，上限100条。最大长度：60000字符 |

\* `patentId` 和 `patentNumber` 两个参数必须至少提供一个。如果两个都存在，会优先使用 `patentId`。


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 专利列表（详见下方字段说明） |
| columns | array | 渲染的列定义 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

### data 数组元素字段

`data` 数组中每个对象包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| patentId | string | 专利ID |
| pn | string | 公开(公告)号 |
| citedBy3y | integer | 3年内被引用次数 |
| citedBy5y | integer | 5年内被引用次数 |
| citedBySimpleFamily | integer | 简单同族被引专利数量 |
| citedByInpadocFamily | integer | INPADOC同族被引专利数量 |
| citedByPatsnapFamily | integer | PatSnap同族被引专利数量 |
| citedByPatents | array | 被引用专利列表 |

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

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/patentCited \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US10123456B2"}'
```

### 单次请求查询多条专利

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/patentCited \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US10123456B2,CN112345678A"}'
```

### 使用专利ID查询

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/patentCited \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentId": "abc123def456"}'
```
