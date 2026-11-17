---
name: linkfox-zhihuiya-abstract-image
description: 智慧芽专利摘要附图获取工具。通过专利 ID 或公开号查询并查看专利文件中的摘要示意图或图纸。
---

# 智慧芽-专利摘要附图查询（Zhihuiya Abstract Image）

本技能用于从智慧芽专利数据库获取专利摘要附图（摘要示意图/图纸），帮助用户快速查看与特定专利相关的附图。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过专利 ID（`patentId`）或公开号（`patentNumber`）查询专利的摘要附图下载路径。
- 支持单条查询与批量查询（多个值用英文逗号隔开，上限 100 条）。
- 返回附图下载路径，便于直接查看专利图纸/示意图。

### ❌ 边界与限制

- **必填条件**：`patentId` 与 `patentNumber` 至少提供一个；两者都提供时优先使用 `patentId`。
- **数量上限**：单次请求最多查询 100 条专利。
- **仅返回摘要附图**：不提供专利全文、权利要求、法律状态、同族、引用/对比文件、估值或侵权分析。
- **不含专利检索**：不支持按关键词或分类号检索专利，需用户自行提供专利 ID 或公开号。
- **成本约束**：本工具消耗积分，同一会话同一参数组合默认只调用一次，失败/空结果不得自动换号连续试探。

## 调用方式

- **API 端点**：`POST /zhihuiya/abstractImage`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_abstract_image.py '<JSON 参数>' [--inline]`
- **成本约束**：同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-abstract-image-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 按公开号查询单条专利**
> "查一下专利 CN115059423A 的摘要附图。"
```json
{"patentNumber": "CN115059423A"}
```

**2. 按公开号批量查询**
> "获取专利 US11234567B2、EP3456789A1、CN115059423A 的摘要附图。"
```json
{"patentNumber": "US11234567B2,EP3456789A1,CN115059423A"}
```

**3. 按专利 ID 查询**
> "获取专利 ID 为 5e6f7a8b9c 的摘要附图。"
```json
{"patentId": "5e6f7a8b9c"}
```

**4. 混合标识符批量查询**
> "我有这些专利 ID：abc123、def456，请获取它们的摘要附图。"
```json
{"patentId": "abc123,def456"}
```

## 展示规则

1. **展示图片**：响应含 `abstractDrawingPath` 时，用 Markdown 图片语法直接展示附图，便于用户直观查看。
2. **标明专利**：每张附图旁标注公开号（`pn`），让用户知道该图属于哪件专利。
3. **缺失附图**：某专利无摘要附图（`abstractDrawingPath` 为空）时，明确告知用户该专利无摘要附图。
4. **批量结果**：多专利查询时，以清晰的列表或表格组织结果。
5. **错误处理**：查询失败时，依据响应说明原因，并建议用户核实专利 ID 或公开号。
6. **不做主观分析**：只呈现附图与元数据，不添加主观专利分析或法律解读。

## 用户表达与场景速查

**适用** —— 专利摘要附图检索：

| 用户说 | 场景 |
|--------|------|
| "看一下专利 XX 的摘要附图" | 单条专利附图查询 |
| "获取这些专利的图纸" | 批量专利附图查询 |
| "专利附图长什么样" | 摘要附图获取 |
| "获取 XX 的专利示意图" | 附图下载路径获取 |
| "我要公开号 XX 的摘要附图" | 按公开号查询 |

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

# 智慧芽-摘要附图 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/abstractImage`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | 条件必填 | 专利ID。`patentId` 和 `patentNumber` 两个参数必须至少提供一个，如果两个都存在，会优先使用 `patentId`。多个用英文逗号隔开，上限100条。最大长度60000字符。 |
| patentNumber | string | 条件必填 | 公开公告号。`patentId` 和 `patentNumber` 两个参数必须至少提供一个，如果两个都存在，会优先使用 `patentId`。多个用英文逗号隔开，上限100条。最大长度60000字符。 |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 专利摘要附图结果列表 |
| data[].patentId | string | 专利ID |
| data[].pn | string | 公开(公告)号 |
| data[].abstractDrawingPath | string | 摘要附图图片下载路径 |
| columns | array | 渲染的列定义 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

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
# 通过公开公告号查询
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/abstractImage \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "CN115059423A"}'
```

```bash
# 通过专利ID查询
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/abstractImage \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentId": "5e6f7a8b9c"}'
```

```bash
# 批量查询多个公开公告号
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/abstractImage \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "CN115059423A,US11234567B2,EP3456789A1"}'
```
