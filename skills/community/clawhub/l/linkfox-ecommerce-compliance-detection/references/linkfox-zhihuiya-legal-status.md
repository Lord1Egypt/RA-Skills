---
name: linkfox-zhihuiya-legal-status
description: 智慧芽专利法律状态查询工具。支持核查专利有效性，查看转让、许可、诉讼及复审等历史法律事件。
---

# 智慧芽专利法律状态查询（Zhihuiya Patent Legal Status）

本技能用于通过智慧芽（PatSnap）数据库查询专利法律状态信息，帮助用户快速判断一个或多个专利的当前法律状态及法律事件历史。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询专利的**简单法律状态**（有效、失效、审中、未确认等）与**详细法律状态**（公开、实质审查、授权、撤回、驳回、撤销、期限届满等）。
- 查询专利的**法律事件**历史（权利转移、许可、质押、信托、异议、复审、海关备案、诉讼、保全、无效程序、口头审理、国防解密、一案双申等）。
- 支持按专利ID或公开（公告）号查询；单次请求最多 100 条；两者同时提供时以 `patentId` 为准。

### ❌ 边界与限制

- **至少需要一个标识**：`patentId` 与 `patentNumber` 必须至少提供一个，否则请求失败。
- **patentId 优先**：两者同时提供时系统使用 `patentId`，忽略 `patentNumber`。
- **数据覆盖**：结果取决于智慧芽（PatSnap）数据库覆盖范围，部分最新申请可能尚未收录。
- **不在范围内**：按关键词、分类号或申请人检索专利；专利全文或权利要求获取；专利估值或商业分析；自由实施（FTO）分析；专利族或引证分析。

## 调用方式

- **API 端点**：`POST /zhihuiya/legalStatus`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_legal_status.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-legal-status-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 核心概念

智慧芽专利法律状态工具为每个专利返回三层法律信息：

1. **简单法律状态**（simpleLegalStatus）——专利当前总体状态的高层摘要（如有效-Active、失效-Inactive、审中-Pending、未确认-Undetermined、PCT指定期内、PCT指定期满）。
2. **法律状态**（legalStatus）——描述专利生命周期阶段的详细状态（如公开-Published、实质审查-Examining、授权-Granted、放弃-Abandoned、撤回-Withdrawn、驳回-Rejected、期限届满-Expired、全部撤销-Revoked、权利终止-Ceased、权利恢复-Restoration 等）。
3. **法律事件**（eventStatus）——专利上发生过的具体法律行为（如权利转移-Transfer、许可-License、质押-Pledge、异议-Opposition、诉讼-Litigation、复审-Re-examination、海关备案-Customs、保全-Preservation、无效程序-Invalid-procedure、口头审理-Oral-procedure、国防解密-Declassification、一案双申-Double application、信托-Trust）。

**专利识别**：可通过专利ID或公开（公告）号查询。两者同时提供时以 `patentId` 为准。单次请求可提交多个值（英文逗号隔开，上限 100）。

## 使用示例

**1. 检查单个专利是否仍然有效**
```
查询公开号 CN115000000A 的法律状态。
```

**2. 批量查询多个专利的法律状态**
```
查询专利 US11000000B2、EP3000000A1、CN115000001A 的法律状态。
```

**3. 识别专利上的法律事件**
```
专利 CN115000000A 是否涉及诉讼、权利转移或质押事件？
```

**4. 判断专利是否过期或被撤销**
```
检查专利 US10000000B1 是否过期、被撤销或仍然有效。
```

**5. 按专利ID查询**
```
查询专利ID abc123、def456 的法律状态。
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示每个专利的公开号、简单法律状态、详细法律状态与法律事件。
2. **状态值翻译**：当用户语言偏好明确时，用对应语言呈现状态标签，同时在括号内保留规范英文值以保证精确。
3. **突出关键结论**：若用户在核查有效性，在响应顶部显著标明每个专利是有效-Active、失效-Inactive 还是审中-Pending。
4. **法律日期上下文**：`legalDate` 可用时一并展示，让用户了解状态信息的新鲜度。
5. **错误处理**：查询失败或无结果时，说明可能原因（公开号格式不正确、数据库未收录等），建议用户核对输入。
6. **批量提示**：查询大量专利时，先展示汇总表格并标注返回总数。

## 用户表达与场景速查

**适用** —— 专利法律状态与事件查询：

| 用户说 | 场景 |
|--------|------|
| "这个专利还有效吗/是否有效" | 简单法律状态核查 |
| "专利 XX 的法律状态是什么" | 详细状态查询 |
| "这个专利有没有被转让或许可" | 法律事件查询 |
| "查一下这些专利是否过期" | 批量有效性核查 |
| "这个专利有诉讼吗" | 法律事件筛选 |
| "专利 CN115XXXXXXA 的法律状态" | 按公开号直查 |

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

# 智慧芽专利法律状态查询 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/legalStatus`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| patentId | string | 条件必填 | 专利ID。`patentId` 和 `patentNumber` 两个参数必须至少提供一个，如果两个都存在，会优先使用 `patentId`。多个用英文逗号隔开，上限100条。最大长度：60000字符。 |
| patentNumber | string | 条件必填 | 公开(公告)号。`patentId` 和 `patentNumber` 两个参数必须至少提供一个，如果两个都存在，会优先使用 `patentId`。多个用英文逗号隔开，上限100条。最大长度：60000字符。 |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 专利法律状态列表 |
| data[].patentId | string | 专利ID |
| data[].pn | string | 公开(公告)号 |
| data[].simpleLegalStatus | array | 简单法律状态。可选值：失效-Inactive、有效-Active、审中-Pending、未确认-Undetermined、PCT指定期内-PCT designated period、PCT指定期满-PCT designated expiration |
| data[].legalStatus | array | 法律状态。可选值：公开-Published、实质审查-Examining、授权-Granted、避重授权-Double、放弃-未指定类型-Abandoned-Undetermined、放弃-主动放弃-Abandoned-Voluntarily、放弃-视为放弃-Abandoned-Deemed、撤回-未指定类型-Withdrawn-Undetermined、撤回-主动撤回-Withdrawn-Voluntarily、撤回-视为撤回-Withdrawn-Deemed、驳回-Rejected、全部撤销-Revoked、期限届满-Expired、未缴年费-Non-Payment、权利恢复-Restoration、权利终止-Ceased、部分无效-P-Revoked、申请终止-Discontinuation、PCT国际公布-PCT published、PCT进入指定国（指定期内）-PCT entering(designated period)、PCT进入指定国（指定期满）-PCT entering(designated expiration)、PCT未进指定国-PCT unentered |
| data[].eventStatus | array | 法律事件。可选值：权利转移-Transfer、许可-License、质押/担保-Pledge、信托-Trust、异议-Opposition、复审-Re-examination、海关备案-Customs、诉讼-Litigation、保全-Preservation、无效程序-Invalid-procedure、口头审理-Oral-procedure、国防解密-Declassification、一案双申-Double application |
| data[].legalDate | integer | 法律状态更新日期（时间戳） |
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
# 通过公开号查询
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/legalStatus \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "CN115000000A"}'
```

```bash
# 通过专利ID查询（多个）
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/legalStatus \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentId": "abc123,def456"}'
```

```bash
# 查询多个公开号
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/legalStatus \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"patentNumber": "US11000000B2,EP3000000A1,CN115000001A"}'
```
