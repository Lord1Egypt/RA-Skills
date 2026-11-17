# 卖大律 产品侵权 TRO 风险检测 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/maidalv/checkApiFlash`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退 `LINKFOXAGENT_API_KEY`（如未配置，按 SKILL.md 的 **## 解决认证和算力问题** 处理）
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：150s

## 请求参数

POST Body（JSON）。`mainProductImage` 为必填，其余为可选增强输入。

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| mainProductImage | string | 是 | - | 主商品图片。可为图片 URL，或带数据 URI 头的 Base64（如 `data:image/jpeg;base64,{base64_data}`）。最大长度 1000 |
| referenceImages | string[] | 否 | - | 相似产品的参考图片数组（URL 或 data URI），最多 3 张 |
| otherProductImages | string[] | 否 | - | 额外产品图片数组（URL 或 data URI），最多 5 张 |
| ipImages | string[] | 否 | - | 与 IP 相关的图片数组（URL 或 data URI），最多 3 张 |
| referenceText | string | 否 | - | 来自相似产品的文本（如产品标题），最大 1000 字符 |
| description | string | 否 | - | 产品描述，建议仅使用产品标题，最大 1000 字符 |
| ipKeywords | string[] | 否 | - | 与知识产权相关的关键词数组，最多 20 个 |
| language | string | 否 | zh | 响应中法律意见报告的语言，仅影响报告语言；取值 `zh` 或 `en` |

> 图片输入说明：URL 须可公开访问；本地图片需先上传获取公开 URL（见 SKILL.md「本地图上传」），或转成 `data:image/...;base64,...` 形式直接传入。

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码，200 表示成功（其他值见「错误码」） |
| errmsg | string | 状态说明（成功为 `ok`） |
| status | string | 分析的整体状态（成功为 `success`） |
| checkId | string | 本次检测的唯一标识 |
| type | string | 渲染样式（如 `tableListWorkbenches`） |
| costToken | integer | 本次消耗 token |
| total | integer | 高风险侵权项数量（即 `results` 数组长度） |
| riskLevel | string | 总体风险评估（`高风险` / `中风险` / `低风险`，对应 High/Medium/Low Risk） |
| results | array | 高风险潜在侵权项列表，详见下方「侵权项字段」 |
| nonResults | array | 非高风险 / 低相似度 IP 项列表（商标、版权、专利等，含 TRO 原告信息），详见下方「侵权项字段」 |
| columns | array | 渲染列定义（渲染元数据，长度可与数据数组不同，仅供展示） |

### 侵权项字段（results / nonResults 元素）

| 字段 | 类型 | 说明 |
|------|------|------|
| ipType | string | IP 类型，实际返回为大写首字母：`Trademark` / `Copyright` / `Patent` |
| text | string | IP 文本内容（商标文字、专利标题或版权标题） |
| ipOwner | string | 知识产权权利人 |
| regNo | string | 注册号（商标序列号、专利号或版权登记号；可能返回 JSON 字符串形式的数组，如 `["1221667"]`） |
| riskLevel | string | 风险级别（High/Medium/Low Risk）；无评分时为 `null` |
| riskScore | number | 数值风险分（0-10）；无评分时为 `null` |
| riskDescription | string | 风险级别文字说明；无评分时为 `null` |
| ipAssetUrls | string[] | 查看 IP 证据图片的 URL 列表 |
| plaintiffId | integer | 原告 ID，仅当该 IP 出现在 TRO 案件中时存在 |
| plaintiffName | string | 原告名称，仅当该 IP 出现在 TRO 案件中时存在 |
| numberOfCases | integer | 该原告提起的案件数量，仅当出现在 TRO 案件中时存在 |
| lastCaseDocket | string | 最近案件的法院案号，仅当出现在 TRO 案件中时存在 |
| lastCaseDateFiled | string | 最近案件的立案日期，仅当出现在 TRO 案件中时存在 |
| report | string | AI 生成的法律评估报告（按 `language` 参数输出中文或英文） |

> 字段填充规则：IP 项的字段是**按需出现**的——非 TRO、未评分的项只返回基础字段（`ipType`/`text`/`ipOwner`/`regNo`/`ipAssetUrls`），`plaintiffName`/`plaintiffId`/`numberOfCases`/`lastCaseDocket`/`lastCaseDateFiled` 等字段**不出现**（而非 null）；当该 IP 出现在 TRO 案件中时，`plaintiffName`/`plaintiffId` 带值返回，`numberOfCases`/`lastCaseDocket`/`lastCaseDateFiled` 可能为 `null`（无案件细节）。`riskLevel`/`riskScore`/`riskDescription` 仅在给出评分时出现，否则不出现。高风险项（命中）放入 `results`，其余放入 `nonResults`。

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务成功与否通过响应体中的 `errcode` 字段区分（`errcode = 200` 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 `errcode` 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和算力问题** 处理。 |
| 402 | 算力不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和算力问题** 处理。 |
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

### 基础检测（仅主图）

```bash
curl -X POST https://tool-gateway.linkfox.com/maidalv/checkApiFlash \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "mainProductImage": "https://m.media-amazon.com/images/I/71jKJgFpg8L._AC_SL1500_.jpg",
    "language": "zh"
  }'
```

### 带参考图与 IP 关键词

```bash
curl -X POST https://tool-gateway.linkfox.com/maidalv/checkApiFlash \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "mainProductImage": "https://example.com/product.jpg",
    "referenceImages": ["https://example.com/ref1.jpg"],
    "ipKeywords": ["apple", "iphone"],
    "language": "zh"
  }'
```

---

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-maidalv-product-tro-detection",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Detection was accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-maidalv-product-tro-detection`)
- `sentiment`: Choose ONE — `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE — `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
