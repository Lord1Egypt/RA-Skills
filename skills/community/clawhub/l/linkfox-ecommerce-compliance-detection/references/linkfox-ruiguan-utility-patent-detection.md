---
name: linkfox-ruiguan-utility-patent-detection
description: 基于亚马逊等产品信息进行实用新型和发明专利检测，评估潜在的专利侵权与TRO风险。
---

# 睿观-实用新型专利检测（Ruiguan Utility Patent Detection）

本技能基于产品标题、描述与目标销售地区检索相似的实用新型（发明）专利，帮助跨境电商卖家在刊登产品前评估潜在专利侵权与 TRO 风险。完整参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 基于产品标题与描述，检索目标市场（当前仅 US）相似的实用新型/发明专利。
- 返回每条专利的相似度评分、有效性状态、申请/公开信息、TRO 维权史等结构化数据。
- 帮助卖家在刊登前识别高相似度、有效专利与 TRO 风险专利，优先关注需复核项。

### ❌ 边界与限制

- **地区覆盖**：当前仅支持检索 US 专利。
- **结果上限**：单次最多返回 200 条专利。
- **输入长度**：`productTitle` 与 `productDescription` 各限 1000 字符。
- **非法律意见**：结果仅表示相似度，不构成对侵权的法律判定，建议咨询专利律师获取权威结论。
- **不在范围内**：外观设计专利检索、商标/品牌侵权核查、版权问题、产品合规认证（FCC、CE 等）、一般法律咨询与合同审查。

## 核心概念

**实用新型专利**（utility patent，亦称发明专利）保护新的、有用的发明或功能性改进，区别于保护外观的外观设计专利，它保护产品的工作方式、结构或组成。侵犯实用新型专利可能导致产品下架、诉讼或 TRO（临时限制令）。

**相似度评分**：每条返回专利包含 `similarity` 字段（0--1），数值越高表示与查询产品越相关，高分专利需重点复核。

**TRO 风险指标**：两个布尔字段标记维权历史：
- `troCase` —— 该专利是否有 TRO 维权行动记录
- `troHolder` —— 专利权人是否以发起 TRO 案件著称

任一为真的专利需格外谨慎。

**专利有效性**：`patentValidity` 字段标明专利为 `Active`（有效）或 `Invalid`（无效），仅有效专利存在侵权风险。

## 调用方式

- **API 端点**：`POST /ruiguan/utilityPatentDetection`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/ruiguan_utility_patent_detection.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-ruiguan-utility-patent-detection-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 产品基础专利风险检查**
> "帮我查一下这款硅胶厨用铲在美国有没有专利风险。"

用描述性的产品标题与描述构建请求，`region` 设为 `US`，`topNumber` 取合理值。

**2. 上架前全面专利排查**
> "我准备上新一款无线耳机，做一次全面的专利排查。"

`topNumber` 取 200 以最大化覆盖，描述需详尽，涵盖蓝牙版本、充电仓设计、降噪特性等。

**3. TRO 风险快速扫描**
> "在美国卖 LED 灯带有没有 TRO 风险？"

获取结果后，过滤并突出 `troCase` 或 `troHolder` 为 true 的专利。

**4. 特定品类深入排查**
> "查一下带 USB 充电的便携搅拌机的专利风险。"

同时提供产品标题与详尽描述，重点描述功能性特征（电机类型、刀片设计、充电方式、容量）。

## 展示规则

1. **表格呈现数据**：以清晰的结构化表格展示结果，关键列包括专利标题、相似度评分、专利有效性、申请号、公开日、TRO 标记、预估到期日。
2. **按相关性排序**：按相似度评分降序展示（最高相似度优先）。
3. **突出高风险专利**：重点提示相似度高于 0.7、有效、或带 TRO 标记的专利。
4. **TRO 警示**：若返回专利中存在 `troCase=true` 或 `troHolder=true`，需显著提示维权风险升高。
5. **有效性区分**：展示时明确区分 Active 与 Invalid 专利，强调仅有效专利需关注。
6. **结果量提示**：结果较多时展示最相关的若干条（如按相似度前 10--20 条），其余汇总说明。
7. **错误处理**：查询失败时说明原因，并建议调整产品标题或描述以提升匹配效果。
8. **双语标题**：可用时同时展示英文标题（`title`）与中文标题（`titleCn`），便于理解。
9. **不提供法律建议**：仅客观呈现专利数据，不对是否侵权作出法律结论，建议咨询专利律师获取权威评估。

## 用户表达与场景速查

**适用** —— 产品专利风险评估相关查询：

| 用户说 | 场景 |
|--------|------|
| "查一下我产品的专利风险" | 基础专利检测 |
| "有没有实用新型/发明专利问题" | 实用新型专利检索 |
| "这个产品能不能卖（专利方面）" | 上架前专利排查 |
| "这个产品有 TRO 风险吗" | TRO 维权风险 |
| "找相似专利" | 专利相似度检索 |
| "专利侵权排查" | 上架前风险评估 |
| "卖这个会不会被起诉" | 专利风险评估 |

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

# 睿观-发明专利检测 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/ruiguan/utilityPatentDetection`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productTitle | string | 是 | 产品标题，最大1000字符 |
| productDescription | string | 是 | 产品描述，最大1000字符 |
| region | string | 是 | 商品想要售卖的国家/地区代码，多个用逗号分隔，当前支持 US。默认 `US` |
| topNumber | integer | 是 | 召回数量，范围：10--200，默认 `100` |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| detectId | string | 检测ID |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |
| columns | array | 渲染的列定义 |
| data | array | 专利列表（详见下方） |

### 专利对象字段

| 字段 | 类型 | 说明 |
|------|------|------|
| globalUtilityId | string | 专利ID |
| title | string | 发明专利标题 |
| titleCn | string | 发明专利标题（中文） |
| similarity | number | 产品与该专利的相似度（0--1） |
| patentValidity | string | 专利有效性：`Active`（有效）或 `Invalid`（无效） |
| applicationNumber | string | 申请号 |
| applicationDate | string | 申请日（yyyy-MM-dd） |
| publicationNumber | string | 公开号 |
| publicationDate | string | 公开日（yyyy-MM-dd） |
| estimatedDueDate | string | 预估到期日（yyyy-MM-dd） |
| region | string | 受理局 |
| patentAbstract | string | 摘要 |
| patentAbstractCn | string | 摘要（中文） |
| claims | string | 权利要求 |
| claimsCn | string | 权利要求（中文） |
| specification | string | 说明书 |
| specificationCn | string | 说明书（中文） |
| inventors | array | 发明家和国家拼接，数组格式 |
| inventorAddresses | array | 发明人地址，数组格式 |
| applicants | array | 申请人和国家拼接，数组格式 |
| applicantAddresses | array | 权利人地址，数组格式 |
| priorityNumber | array | 优先权号，数组格式 |
| relatedPublicationDate | array | 首次公开日（yyyy-MM-dd），数组格式 |
| patentImageUrl | string | 专利封面图 |
| images | array | 专利附图 |
| classNumList | array | 类别号路径列表，格式：classNum1 > classNum2 > classNum3 |
| cpcKindRaw | array | CPC分类（原始 JSONArray） |
| troCase | boolean | 是否有TRO维权史 |
| troHolder | boolean | 是否是TRO权利人的专利 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 402 | 积分或余额不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
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
curl -X POST https://tool-gateway.linkfox.com/ruiguan/utilityPatentDetection \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"productTitle": "便携式USB-C 65W氮化镓快充充电器", "productDescription": "一款紧凑型65W氮化镓USB-C快充充电器，配备可折叠插脚，支持PD3.0和QC4.0协议，双USB-C端口和一个USB-A端口，适用于笔记本电脑、手机和平板电脑。", "region": "US", "topNumber": 100}'
```
