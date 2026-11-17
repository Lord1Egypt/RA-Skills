---
name: linkfox-zhihuiya-utility-patent-image-search
description: 基于智慧芽的专利图片相似度搜索，支持通过图片URL检索实用新型专利。当用户提到实用新型专利图片搜索、实用新型专利侵权检查、实用新型专利搜索、以图搜专利、实用新型专利相似度检测、专利图片匹配、专利形状/图案/色彩匹配、检查产品结构是否侵犯已有实用新型专利、patent image search, utility model patent search, patent reverse image search, utility model patent lookup, PatSnap, patent similarity时触发此技能。即使用户未明确提及"智慧芽"或"专利图片"，只要其需求涉及通过图片查找相似实用新型专利或排查实用新型专利风险，也应触发此技能。本技能仅支持实用新型专利，外观设计专利检索请使用 linkfox-zhihuiya-patent-image-search。
---

# 智慧芽专利以图搜图（实用新型专利）

本技能引导你使用智慧芽专利数据库进行图片相似度检索，帮助用户识别潜在相似的**实用新型专利**。本技能仅支持实用新型专利；外观设计专利检索请使用 `linkfox-zhihuiya-patent-image-search`。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过**公开可访问的图片 URL** 检索全球专利图片数据库，返回按相似度排序的专利列表。
- 仅支持实用新型专利（`U`）。
- 支持按受理局国家、法律状态、申请人、申请/公开日期等多维筛选。
- 用于侵权排查、产品结构风险检测、先行技术调研等场景。
- 提供本地图片上传脚本，将本地文件转为可用的公开图片 URL。

### ❌ 边界与限制

- **输入要求**：必须提供**公开可访问的图片 URL**；本地图片路径需先经上传脚本转 URL，且上传后 URL 有效期 24 小时。
- **匹配范围**：仅基于视觉相似度，不构成法律侵权判定；法律结论须咨询专业专利律师。
- **专利类型匹配**：`model` 须与 `patentType` 匹配——本技能仅实用新型专利（`U`），模型 3-4；外观设计专利（`D`，模型 1-2）请使用 `linkfox-zhihuiya-patent-image-search`。
- **不在范围内**：基于文本的专利检索（关键词/摘要/权利要求检索）；外观设计专利检索；洛迦诺分类（LOC）筛选（仅适用于外观专利）；专利法律状态监控或年费管理；专利估值或许可谈判；FTO（自由实施）法律意见；专利族或引证分析。
- **成本约束**：本工具消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换图、翻页或改参数连续试探；需继续检索时先向用户说明会产生额外消耗。

## 核心概念

**专利以图搜图**使用视觉 AI 模型，将给定产品或设计图片与全球专利图片库比对，返回相似专利排序列表，供用户评估侵权风险或进行先行技术调研。

**本技能仅支持实用新型专利：**

| 类型 | 代码 | 说明 |
|------|------|------|
| 实用新型专利 | `U` | 保护产品的功能性形状/结构 |

**检索模型**（实用新型专利）：

| 模型 ID | 专利类型 | 策略 | 推荐 |
|---------|----------|------|------|
| 3 | 实用新型（`U`） | 匹配形状 | 仅形状比对 |
| 4 | 实用新型（`U`） | 匹配形状/图案/色彩 | 推荐用于实用新型专利 |

> 外观设计专利（模型 1/2）不在本技能支持范围，请使用 `linkfox-zhihuiya-patent-image-search`。

**评分逻辑**：`score` 越高表示视觉相似度越高。展示结果时按 `score` 降序排列（最相似在前），便于用户优先复核最相关的专利。

## 调用方式

- **API 端点**：`POST /zhihuiya/patentImageSearch`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_utility_patent_image_search.py '<JSON 参数>' [--inline]`
- **成本约束**：见上方【能力边界】中的成本约束说明。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-utility-patent-image-search-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从落盘 json 文件按需抽取，避免整份 JSON 进入上下文。

## 本地图片上传

本工具要求**公开可访问的图片 URL**。若用户提供本地图片路径（如 `C:\Users\...\photo.png`），须先运行上传脚本获取公开 URL（有效期 24 小时）：
```bash
python scripts/upload_image.py /path/to/local/image.png
```

## 使用示例

**1. 基础实用新型专利检索（推荐起点）**
按形状/图案/色彩匹配，跨所有国家检索与产品图相似的实用新型专利：
```json
{
  "url": "https://example.com/my-product.jpg",
  "patentType": "U",
  "model": 4,
  "limit": 20
}
```

**2. 限定国家的实用新型专利检索**
仅在中国检索：
```json
{
  "url": "https://example.com/my-product.jpg",
  "patentType": "U",
  "model": 4,
  "country": "CN",
  "limit": 20
}
```

**3. 仅按形状匹配的实用新型专利检索**
仅比对形状（忽略图案/色彩）：
```json
{
  "url": "https://example.com/my-product.jpg",
  "patentType": "U",
  "model": 3,
  "country": "CN",
  "limit": 20
}
```

**4. 限定日期范围内的有效实用新型专利**
检索 2020 年后申请的有效实用新型专利：
```json
{
  "url": "https://example.com/my-product.jpg",
  "patentType": "U",
  "model": 4,
  "simpleLegalStatus": "1",
  "applyStartTime": "20200101",
  "limit": 30
}
```

**5. 按指定申请人检索并返回中文标题**
```json
{
  "url": "https://example.com/my-product.jpg",
  "patentType": "U",
  "model": 4,
  "assignees": "Apple Inc.",
  "lang": "cn",
  "limit": 20
}
```

## 展示规则

1. **按相似度排序**：始终按 `score` 降序排列（最相似在前），帮助用户快速识别最相关的侵权风险。

2. **展示完整信息**：汇总结果或生成报告时，逐条专利包含以下全部字段，不得省略或缩写：申请号（`apno`）、专利名称（中文，使用 `lang: cn` 或提供翻译）、发明人（`inventor`）、命中的专利附图（`url`）、图片列表中的**每一张**专利图片、专利摘要、专利说明书、IPC/UPC 分类信息、雷达结果（`radarResult`，如有）、专利规格说明。

3. **法律声明**：结果末尾附加友好提示：
   > 本检索结果由 LinkfoxAgent 生成。建议咨询专业专利律师获取法律意见。

4. **评分说明**：提醒用户 `score` 表示视觉相似度——分数越高匹配越接近，但不构成侵权的法律判定。

5. **分页指引**：当总数超出本次返回数量时，告知匹配专利总数，并引导用户使用 `offset` 和 `limit` 获取后续页。

6. **错误处理**：查询失败时说明原因，并建议调整（如确认图片 URL 公开可访问、检查国家代码、调整日期格式）。

## 用户表达与场景速查

**适用** —— 基于图片的实用新型专利相似度检索：

| 用户说 | 场景 |
|--------|------|
| "检查我的产品结构是否侵犯实用新型专利" | 实用新型专利侵权排查 |
| "搜索相似的实用新型专利" | 实用新型专利相似度检索 |
| "找和这张图相似的实用新型专利" | 视觉实用新型专利查询 |
| "我的产品结构有没有相似专利" | 实用新型风险评估 |
| "以图搜实用新型专利" | 实用新型检索 |
| "检查这个产品在中美的实用新型专利风险" | 多国实用新型专利排查 |
| "找这个类别下有效的实用新型专利" | 带筛选的实用新型专利检索 |
| "谁持有和这个结构相似的实用新型专利" | 竞品实用新型专利发现 |

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

# 智慧芽专利图像检索 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/zhihuiya/patentImageSearch`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`）读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

### 必填参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | 是 | 图像的URL（最大1000字符） |
| patentType | string | 是 | 专利类型：`D`（外观专利）或 `U`（实用新型专利）。默认：`D` |
| model | integer | 是 | 图像检索模型。外观专利：`1`（智能联想，推荐）、`2`（搜索此图）；实用新型专利：`3`（匹配形状）、`4`（匹配形状/图案/色彩，推荐） |

### 可选参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| country | string | 否 | 专利受理局（国家/组织/地区代码），多个用英文逗号隔开。例如：`CN,US,JP`。不传时代表查询全部专利受理局的数据 |
| loc | string | 否 | LOC分类（洛迦诺分类号），多个分类号可以用逻辑符 AND/OR/NOT 连接 |
| legalStatus | string | 否 | 专利的法律状态，多个用英文逗号隔开。可选值：`1`（公开）、`2`（实质审查）、`3`（授权）、`8`（避免重复授权）、`11`（撤回）、`12`（撤回-未指定类型）、`17`（撤回-视为撤回）、`18`（撤回-主动撤回）、`13`（驳回）、`14`（全部撤销）、`15`（期限届满）、`16`（未缴年费）、`21`（权利恢复）、`22`（权利终止）、`23`（部分无效）、`24`（申请终止）、`30`（放弃）、`19`（放弃-视为放弃）、`20`（放弃-主动放弃）、`25`（放弃-未指定类型）、`222`（PCT未进入指定国-指定期内）、`223`（PCT进入指定国-指定期内）、`224`（PCT进入指定国-指定期满）、`225`（PCT未进入指定国-指定期满） |
| simpleLegalStatus | string | 否 | 专利的简单法律状态，多个用英文逗号隔开。可选值：`0`（失效）、`1`（有效）、`2`（审中）、`220`（PCT指定期满）、`221`（PCT指定期内）、`999`（未确认） |
| assignees | string | 否 | 申请（专利权）人（最大1000字符） |
| applyStartTime | string | 否 | 专利申请起始时间，格式：`yyyyMMdd` |
| applyEndTime | string | 否 | 专利申请截止时间，格式：`yyyyMMdd` |
| publicStartTime | string | 否 | 专利公开起始时间，格式：`yyyyMMdd` |
| publicEndTime | string | 否 | 专利公开截止时间，格式：`yyyyMMdd` |
| limit | integer | 否 | 返回专利条数，1-100。默认：`10` |
| offset | integer | 否 | 偏移量，0-1000。默认：`0` |
| field | string | 否 | 返回结果排序字段：`SCORE`（按照最相关排序）、`APD`（按照申请日排序）、`PBD`（按照公开日排序）、`ISD`（按照授权日排序）。默认：`SCORE` |
| order | string | 否 | 当 field 选择 APD/PBD/ISD 时有效：`desc`（降序）或 `asc`（升序）。默认：`desc` |
| lang | string | 否 | 设置标题的语言优先选择：`original`（专利原文标题）、`cn`（专利中文翻译标题）、`en`（专利英文翻译标题）。默认：`original` |
| preFilter | integer | 否 | 是否开启前置国家/LOC过滤：`1`（开启）、`0`（关闭）。默认：`1` |
| stemming | integer | 否 | 是否开启截词功能：`1`（开启）、`0`（关闭）。默认：`0` |
| mainField | string | 否 | 专利主要字段，包括标题、摘要、权利要求、说明书、公开号、申请号、申请人、发明人和IPC/UPC/LOC分类号（最大1000字符） |
| includeMachineTranslation | boolean | 否 | 搜索包含机器翻译数据 |
| scoreExpansion | boolean | 否 | 分数拓展 |
| isHttps | integer | 否 | 选择是否返回https域名图片：`1`（返回https）、`0`（返回http）。默认：`0` |
| returnImgId | boolean | 否 | 是否返回img_id。默认：`false` |

**注意**：
- `model` 参数须与 `patentType` 匹配：模型1-2用于外观专利（`D`），模型3-4用于实用新型专利（`U`）

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 本次返回的记录数 |
| allRecordsCount | integer | 数据库中匹配的总记录数 |
| data | array | 匹配的专利记录列表 |
| columns | array | 渲染的列定义 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗token |

### 专利记录字段（`data` 中的每条记录）

| 字段 | 类型 | 说明 |
|------|------|------|
| patentId | string | 相似专利ID |
| patentPn | string | 相似专利号 |
| apno | string | 申请号 |
| title | string | 专利名称 |
| inventor | string | 发明人 |
| originalAssignee | string | 原始申请人 |
| currentAssignee | string | 当前申请人 |
| authority | string | 受理局（国家代码） |
| url | string | 相似的专利附图URL |
| score | number | 相似度分数（分数越高越相似；仅当 field 为 `SCORE` 时有效） |
| loc | array | LOC分类（洛迦诺分类号） |
| locMatch | integer | 是否命中高权重LOC：`1`（命中）、`0`（未命中）。仅当 model=1 且 field=SCORE 时有效 |
| apdt | integer | 申请日（时间戳） |
| pbdt | integer | 公开日（时间戳） |
| imgId | string | 专利附图img_id（仅当 `returnImgId` 为 true 时返回） |

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/zhihuiya/patentImageSearch \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/product-image.jpg",
    "patentType": "D",
    "model": 1,
    "country": "CN,US",
    "limit": 20,
    "lang": "cn"
  }'
```

### 响应示例

```json
{
  "total": 20,
  "allRecordsCount": 1523,
  "data": [
    {
      "patentId": "abcdef123456",
      "patentPn": "CN305123456S",
      "apno": "CN202130123456.7",
      "title": "台灯",
      "inventor": "张三",
      "originalAssignee": "示例公司",
      "currentAssignee": "示例公司",
      "authority": "CN",
      "url": "http://images.zhihuiya.com/patent/12345.jpg",
      "score": 0.95,
      "loc": ["26-05"],
      "locMatch": 1,
      "apdt": 1640995200000,
      "pbdt": 1656633600000
    }
  ],
  "columns": [],
  "type": "patent_image",
  "costToken": 100
}
```

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

---

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-xxx-xxx",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter
- `sentiment`: Choose ONE — `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE — `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
