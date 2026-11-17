---
name: linkfox-zhihuiya-pdf-data
description: 智慧芽专利 PDF 下载工具。支持通过专利 ID 或公开号批量或单篇导出并下载专利 PDF 全文原始文档。
---

# 智慧芽专利 PDF 下载（Zhihuiya Patent PDF Downloader）

本技能用于从智慧芽专利数据库获取专利 PDF 全文下载链接，支持按专利 ID 或公开号查询，单次最多 100 篇。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过专利 ID 或公开号获取专利 PDF 全文下载链接。
- 支持单篇或批量下载（单次最多 100 篇）。
- 当原专利 PDF 不可用时，可启用同族专利 PDF 替代。

### ❌ 边界与限制

- **标识符必填**：`patentId` 与 `patentNumber` 至少提供一个，两者皆空则请求失败。
- **优先级**：同时提供两者时，优先使用 `patentId`。
- **批量上限**：单次请求最多 100 篇专利。
- **PDF 可用性**：并非所有专利都有 PDF，可用 `replaceByRelated` 回退到同族专利。
- **不在范围内**：专利检索与发现（按关键词、申请人等找专利）；专利引用与法律状态分析；专利权利要求解读或翻译；专利组合分析与全景地图。

## 核心概念

智慧芽专利 PDF 服务提供全球专利全文 PDF 文档的下载链接，可按**专利 ID**或**公开号**查询，单次最多 100 篇。

- **查询优先级**：同时提供 `patentId` 和 `patentNumber` 时，优先使用 `patentId`。
- **同族替代**：原专利 PDF 不可用时，可返回同族相关专利的 PDF。

**标识符选择**：
- **专利 ID**（`patentId`）：智慧芽系统内部数字标识，适用于用户提供智慧芽专用 ID 的场景。
- **公开号**（`patentNumber`）：公开专利号（如 `US20230012345A1`、`CN115000000A`），适用于用户提供标准专利号的场景。

## 调用方式

- **API 端点**：`POST /zhihuiya/pdfData`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_pdf_data.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-pdf-data-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 按公开号查询单篇**
> "下载公开号 US20230012345A1 的专利 PDF"
参数：`{"patentNumber": "US20230012345A1"}`

**2. 按公开号批量查询**
> "下载 CN115000000A、CN115000001A、CN115000002A 的 PDF"
参数：`{"patentNumber": "CN115000000A,CN115000001A,CN115000002A"}`

**3. 按专利 ID 查询单篇**
> "获取专利 ID 12345678 的全文 PDF"
参数：`{"patentId": "12345678"}`

**4. 启用同族替代**
> "下载 EP4000000A1 的 PDF，如果不可用就用同族专利 PDF 替代"
参数：`{"patentNumber": "EP4000000A1", "replaceByRelated": "1"}`

**5. 按专利 ID 批量查询**
> "获取专利 ID 11111111、22222222、33333333 的 PDF"
参数：`{"patentId": "11111111,22222222,33333333"}`

## 展示规则

1. **清晰呈现下载链接**：以表格或列表展示每篇专利的公开号与 PDF 下载链接。
2. **标注替代情况**：若 PDF 由同族专利替代提供，明确说明并展示 `pnRelated`，让用户知道使用了哪篇同族专利。
3. **批量结果**：多专利返回时，用表格展示列：公开号、专利 ID、PDF 链接、替代说明（如有）。
4. **错误处理**：查询失败或无结果时说明原因，建议用户核对专利 ID 或公开号；若未启用 `replaceByRelated`，建议开启作为替代方案。
5. **无 PDF 情况**：返回的专利条目无 `pdfPath` 时，告知用户该专利 PDF 不可用，并建议启用同族替代。

## 用户表达与场景速查

**适用** —— 专利 PDF 文档获取：

| 用户说 | 场景 |
|--------|------|
| "下载专利 XX 的 PDF" | 单篇专利 PDF 获取 |
| "获取这些专利的全文文档" | 批量专利 PDF 下载 |
| "我要公开号 XX 的 PDF" | 按公开号查询 |
| "专利不可用能不能拿到文档" | 同族替代场景 |
| "批量导出专利 PDF" | 多专利批量下载 |

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

# 智慧芽 PDF全文查询 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/pdfData`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | 条件必填 | 专利ID（专利ID和公开号两个参数必须要有一个，如果两个都存在，会优先使用专利ID），多个用英文逗号隔开，上限100条 |
| patentNumber | string | 条件必填 | 公开公告号（专利ID和公开号两个参数必须要有一个，如果两个都存在，会优先使用专利ID），多个用英文逗号隔开，上限100条 |
| replaceByRelated | string | 否 | 当前专利PDF无法获取时是否用同族专利的PDF替代：`1` 是，`0` 否 |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 专利列表，每个元素包含PDF信息 |
| data[].patentId | string | 专利ID |
| data[].pn | string | 公开（公告）号 |
| data[].pdfPath | string | PDF全文下载地址（含path等信息） |
| data[].pnRelated | string | 替代专利的公开号（仅当使用同族专利替代时提供） |
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

### 通过公开号查询

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/pdfData \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US20230012345A1"}'
```

### 通过专利ID查询并启用同族替代

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/pdfData \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentId": "12345678", "replaceByRelated": "1"}'
```

### 批量查询多个公开号

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/pdfData \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "CN115000000A,CN115000001A,CN115000002A"}'
```
