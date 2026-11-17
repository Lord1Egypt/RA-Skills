---
name: linkfox-zhihuiya-description-data
description: 智慧芽专利说明书获取工具。支持通过专利 ID 或公开号查看完整的专利技术描述、实施方式及全文文本。
---

# 智慧芽-专利说明书获取（Zhihuiya Patent Description Data）

本技能用于从智慧芽专利数据库查询专利说明书（描述）数据，帮助用户获取特定专利的全文说明书内容。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过专利 ID 或公开（公告）号查询一项或多项专利的说明书（描述）全文。
- 支持批量查询（最多 100 条），返回说明书各章节内容。
- 当目标专利说明书不可用时，可启用同族专利替代获取近似内容。

### ❌ 边界与限制

- **标识符要求**：`patentId` 与 `patentNumber` 至少提供一个；不支持按关键词、申请人、分类号检索专利。
- **批量上限**：单次请求最多查询 100 条专利。
- **优先规则**：若同时提供 `patentId` 和 `patentNumber`，优先使用 `patentId`。
- **数据可用性**：并非所有专利在数据库中都有说明书；可使用 `replaceByRelated: "1"` 尝试同族替代。
- **不在范围内**：专利检索（按关键词/申请人/分类号）、权利要求分析与权利要求图表、法律状态与审查历史、专利全景与统计分析、自由实施（FTO）或侵权分析意见。

## 核心概念

专利说明书（specification）是随专利申请提交的详细技术文档，披露发明工作原理、优选实施方式及其他专利法要求的技术细节。本工具查询智慧芽数据库，按专利内部 ID 或公开公告号返回一项或多项专利的说明书数据。

- **标识符优先**：同一查询同时给出专利 ID 与公开号时，专利 ID 优先。
- **同族替代**：若某专利说明书不可获取，工具可选择性地返回同族专利的说明书替代。

## 调用方式

- **API 端点**：`POST /zhihuiya/descriptionData`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_description_data.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-description-data-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 按公开号查询单个专利说明书**
> "查一下 CN115099012A 这篇专利的说明书"
```
patentNumber: "CN115099012A"
```

**2. 批量查询多个专利说明书**
> "帮我获取这几个专利的说明书：CN115099012A、US20230012345A1"
```
patentNumber: "CN115099012A,US20230012345A1"
```

**3. 启用同族替代**
> "CN115099012A 没有说明书的话，用同族专利的说明书代替"
```
patentNumber: "CN115099012A"
replaceByRelated: "1"
```

**4. 按专利 ID 查询**
> "用这个专利 ID 查说明书"
```
patentId: "some-patent-id"
```

## 展示规则

1. **忠实呈现数据**：清晰展示返回的说明书内容，不篡改技术细节、不添加主观解读。
2. **结构化输出**：当说明书包含多个章节（背景技术、发明内容、具体实施方式、权利要求等）时，用清晰标题分节呈现以提升可读性。
3. **同族替代提示**：若响应包含 `pnRelated` 字段，明确告知用户该说明书来自同族替代专利，并给出替代公开号。
4. **批量结果分隔**：返回多个专利时，以公开号为标题清晰分隔每个专利的内容。
5. **错误处理**：查询失败或无数据时说明原因，并建议用户核对专利 ID 或公开号。
6. **大内容提醒**：专利说明书可能很长，先概述关键章节，再询问用户是否需要查看全文。

## 用户表达与场景速查

**适用** —— 专利说明书 / 描述内容查询：

| 用户说 | 场景 |
|--------|------|
| "看一下 XX 专利的说明书" | 单个专利说明书查询 |
| "获取这几篇专利的完整说明书" | 批量专利说明书获取 |
| "我要 CN115099012A 的详细文本" | 按公开号查询 |
| "用同族专利的说明书代替" | 同族替代查询 |
| "这篇专利技术上都讲了什么" | 说明书内容阅读 |

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

# 智慧芽专利说明书查询 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/descriptionData`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | 条件必填 | 专利ID（专利ID和公开号两个参数必须要有一个，如果两个都存在，会优先使用专利ID）。多个用英文逗号隔开，上限100条。最大长度60000字符。 |
| patentNumber | string | 条件必填 | 公开公告号（专利ID和公开号两个参数必须要有一个，如果两个都存在，会优先使用专利ID）。多个用英文逗号隔开，上限100条。最大长度60000字符。 |
| replaceByRelated | string | 否 | 当前专利说明书无法获取时是否用同族专利的说明书替代：`1` 是，`0` 否。最大长度1000字符。 |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 返回的专利记录数 |
| data | array | 专利列表，每个元素包含说明书数据 |
| data[].patentId | string | 专利ID |
| data[].pn | string | 公开（公告）号 |
| data[].pnRelated | string | 替代专利的公开号（仅当使用同族专利替代时提供） |
| data[].description | array | 说明书内容章节 |
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

**通过公开号查询：**

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/descriptionData \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "CN115099012A"}'
```

**通过专利ID查询并启用同族替代：**

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/descriptionData \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentId": "abc123def456", "replaceByRelated": "1"}'
```

**批量查询多个公开号：**

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/descriptionData \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "CN115099012A,US20230012345A1,EP4123456A1"}'
```
