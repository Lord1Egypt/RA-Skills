---
name: linkfox-zhihuiya-description-data-translated
description: 智慧芽专利说明书翻译工具。支持将专利的完整说明书、技术描述及实施例翻译为中、英、日等语言。
---

# 智慧芽-专利说明书翻译（Zhihuiya Patent Description Translated）

本技能引导你通过智慧芽数据服务获取翻译后的专利说明书（描述）文本，支持翻译为中文、英文、日语，并可通过专利 ID 或公开号查询。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 获取专利说明书（specification，专利全文技术描述）的**翻译版本**，目标语言支持中文（`cn`）、英文（`en`）、日语（`jp`）。
- 通过专利 ID 或公开（公告）号查询，支持单条与批量（最多 100 条）查询。
- 当原专利说明书不可获取时，可选使用**同族专利**（在其他 jurisdiction 就同一发明提交的相关专利）的说明书替代。

### ❌ 边界与限制

- **至少一个标识**：`patentId` 与 `patentNumber` 必须至少提供一个；两者同时提供时优先使用 `patentId`。
- **语言范围**：仅支持 `en`/`cn`/`jp` 三种目标语言，默认 `en`。
- **不翻译非说明书内容**：仅翻译说明书文本，不涉及权利要求、法律状态、引证分析等。
- **依赖原文可用性**：原文说明书缺失时需开启 `replaceByRelated=1` 才能以同族说明书替代，否则返回为空。
- **不在范围内**：专利检索/发现、权利要求分析、法律状态与审查历史、引证分析、专利组合统计。

## 核心概念

专利说明书（specification）是专利文档的完整技术文本。本工具从智慧芽专利库中获取该文本的**翻译版本**，支持三种目标语言：中文（`cn`）、英文（`en`）、日语（`jp`）。

当某专利说明书不可获取时，工具可选使用**同族专利成员**（在其他司法管辖区就同一发明提交的相关专利）的说明书进行替代。

## 调用方式

- **API 端点**：`POST /zhihuiya/descriptionDataTranslated`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_description_translated.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-description-data-translated-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 按公开号获取英文翻译**
```
patentNumber: "US10123456B2"
lang: "en"
```

**2. 按专利 ID 获取中文翻译**
```
patentId: "abc123def"
lang: "cn"
```

**3. 批量查询并启用同族替代**
```
patentNumber: "US10123456B2,EP3456789A1,CN112345678A"
lang: "en"
replaceByRelated: 1
```

**4. 获取某专利的日语翻译**
```
patentNumber: "JP2021012345A"
lang: "jp"
```

## 展示规则

1. **清晰呈现译文**：直接展示专利说明书翻译文本。对长文本，给出摘要或首段，并告知完整文本已可获取。
2. **标明替代来源**：响应中存在 `pnRelated` 时，明确告知用户该说明书取自同族专利，并展示该同族公开号。
3. **批量结果**：返回多条专利时，以结构化列表展示，各专利说明书之间清晰分隔。
4. **错误处理**：查询失败时基于响应说明原因，并建议用户核对专利 ID 或公开号是否正确。
5. **禁止编造**：不得编造或改写专利文本，仅展示接口返回的内容。

## 用户表达与场景速查

**适用** —— 专利说明书/规格翻译查询：

| 用户说 | 场景 |
|--------|------|
| "把这个专利说明书翻译成英文" | 单条专利翻译 |
| "我需要专利 US10123456 的中文版" | 指定语言翻译 |
| "获取这几个专利的说明书文本" | 批量说明书获取 |
| "专利 CN112345678A 描述了什么？" | 专利说明书查阅 |
| "给我这个专利全文的日语翻译" | 日语翻译 |
| "说明书缺失，能用同族专利吗？" | 同族替代 |

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

# 智慧芽-说明书翻译 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/descriptionDataTranslated`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | 条件必填 | 专利ID。`patentId` 和 `patentNumber` 两个参数必须至少提供一个，如果两个都存在，会优先使用 `patentId`。多个用英文逗号隔开，上限100条。最大长度60000字符 |
| patentNumber | string | 条件必填 | 公开(公告)号。`patentId` 和 `patentNumber` 两个参数必须至少提供一个，如果两个都存在，会优先使用 `patentId`。多个用英文逗号隔开，上限100条。最大长度60000字符 |
| lang | string | 否 | 翻译语言，支持 `en`（英文，默认）、`cn`（中文）、`jp`（日语）。最大长度1000字符 |
| replaceByRelated | integer | 否 | 说明书无法获取时是否用同族专利说明书替代：`1` 是、`0` 否（默认 `0`） |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 专利列表（详见下方） |
| columns | array | 渲染的列定义 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

### data 数组元素字段

`data` 数组中每个元素包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| patentId | string | 专利ID |
| pn | string | 公开(公告)号 |
| description | string | 说明书翻译文本 |
| pnRelated | string | 替代专利的公开号（仅当使用同族专利替代时提供） |

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
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/descriptionDataTranslated \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US10123456B2", "lang": "en", "replaceByRelated": 0}'
```

### 批量查询示例

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/descriptionDataTranslated \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US10123456B2,EP3456789A1,CN112345678A", "lang": "cn", "replaceByRelated": 1}'
```
