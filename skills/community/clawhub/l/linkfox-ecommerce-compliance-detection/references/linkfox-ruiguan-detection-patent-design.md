---
name: linkfox-ruiguan-detection-patent-design
description: 基于睿观的跨国/地区外观设计专利侵权检测工具，用于排查产品图片的外观专利与 TRO 诉讼风险。
---

# 睿观-外观专利检测（Ruiguan Design Patent Detection）

本技能基于睿观引擎进行外观设计专利侵权检测，帮助电商卖家与知识产权从业者在产品上架前识别潜在的外观专利风险。完整参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 以产品图片为输入，对比全球外观设计专利数据库，返回按相似度排序的专利结果。
- 支持 25+ 国家/地区的外观专利检索（US、EU、CN、JP、KR、DE、GB、FR 等）。
- 提供 TRO（临时禁令）维权史查询，识别有主动维权记录的专利权人。
- 可选启用 AI 雷达分析，给出疑似侵权的判定与说明。
- 支持按 LOC（洛迦诺）分类限定检索范围，或交由模型自动预测分类。

### ❌ 边界与限制

- **图片要求**：需提供公开可访问的图片 URL；本地图片须先上传获取 URL（见下方【本地图片上传】）。
- **检测范围**：仅覆盖外观设计专利，不包含发明专利、实用新型专利。
- **相似度口径**：相似度分数为视觉 resemblance 参考值，不构成法律结论。
- **成本约束**：每次调用消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词或连续试探。
- **不在范围内**：发明专利/实用新型检索；商标侵权检测；版权/DMCA 问题；法律案件管理与诉讼策略；专利申请与申报；Listing 优化与定价。

## 核心概念

外观专利检测通过视觉相似度算法将产品图片与全球外观设计专利数据库进行比对，返回按相似度排序的专利结果，并附带 TRO 维权诉讼史，帮助评估侵权风险。

**相似度分数**：取值 0-1，数值越高表示与专利附图的视觉相似度越高。`similarity >= 0.7` 或有 TRO 维权史的专利需重点关注并仔细审查。

**雷达分析**：启用雷达后，每个专利结果包含 `radarResult`，其中 `same` 标记是否疑似侵权（true/false），`exp` 给出判定说明，提供超越原始相似度的 AI 判定。

**LOC 分类**：洛迦诺分类（LOC）是工业品外观设计的国际分类体系。可指定 LOC 代码缩小检索范围，或不指定由模型自动预测合适类目。

参数详情见 [references/api.md](references/api.md)。

## 调用方式

- **API 端点**：`POST /ruiguan/detectionPatentDesign`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/ruiguan_detection_patent_design.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-ruiguan-detection-patent-design-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 本地图片上传

本工具要求**公开可访问的图片 URL**。若用户提供的是本地图片文件路径（如 `C:\Users\...\photo.png`、`/home/.../image.jpg`），须先上传以获取公开 URL。

运行上传脚本：
```bash
python scripts/upload_image.py /path/to/local/image.png
```

脚本会返回一个公开 URL（有效期 24 小时），可作为 imageUrl 参数使用。

## 使用示例

**1. 基础专利检测（美国市场）**
```json
{
  "imageUrl": "https://example.com/product.jpg",
  "queryMode": "hybrid",
  "topNumber": 50,
  "regions": "US"
}
```

**2. 多地区检测并补充产品上下文**
```json
{
  "imageUrl": "https://example.com/product.jpg",
  "queryMode": "physical",
  "topNumber": 100,
  "regions": "US,EU,CN",
  "productTitle": "Portable Wireless Charger Stand",
  "productDescription": "A foldable wireless charging stand for smartphones",
  "enableRadar": true
}
```

**3. 使用 LOC 分类缩小范围（家具）**
```json
{
  "imageUrl": "https://example.com/chair.jpg",
  "queryMode": "hybrid",
  "topNumber": 80,
  "regions": "US,DE",
  "topLoc": "06",
  "patentStatus": "1"
}
```

**4. 线条图模式检索**
```json
{
  "imageUrl": "https://example.com/sketch.png",
  "queryMode": "line",
  "topNumber": 50,
  "regions": "CN,JP,KR"
}
```

**5. 同时检索有效与失效专利**
```json
{
  "imageUrl": "https://example.com/product.jpg",
  "queryMode": "hybrid",
  "topNumber": 100,
  "regions": "US",
  "patentStatus": "1,0"
}
```

## 展示规则

1. **高风险专利突出展示**：生成摘要或报告时，对所有 `similarity >= 0.7` 或 `troCase = true` 的专利**完整**展示详情，包括：申请号、专利标题（中文）、发明人、TRO 维权史、最相似专利附图、专利图片列表中的每张图片、专利摘要、专利说明书、LOC 信息、雷达分析结果与说明书文本。此详细呈现至关重要，**不得省略或缩写**这些字段。
2. **免责声明**：结尾始终附上友好提醒：“本检测结果由 LinkfoxAgent 生成。建议咨询专业知识产权律师获取法律意见。”
3. **相似度解读**：明确说明相似度分数越高，视觉相似度越大、侵权风险越高。
4. **雷达结果展示**：当 `radarResult.same` 为 true 时，显著标记该专利为疑似侵权匹配，并展示 `exp` 说明。
5. **TRO 警告**：`troCase = true` 或 `troHolder = true` 的专利应加警告标识，表明专利权人有通过临时禁令主动维权的历史。
6. **图片展示**：同时展示 `patentImageUrl`（最相似专利附图）与完整 `images` 列表，便于用户将产品与所有专利附图直观对比。
7. **错误处理**：请求失败时说明原因并建议纠正措施（如检查图片 URL 可访问性、核实地区代码）。
8. **如实呈现数据**：按查询结果原样展示，不添加超出工具自身分析的主观法律结论。

## 用户表达与场景速查

**适用** —— 外观设计专利风险评估：

| 用户说 | 场景 |
|--------|------|
| "检查这个产品是否侵犯外观专利" | 基础专利检测 |
| "这张图片的专利风险排查" | 基于图片的专利检索 |
| "这个产品有 TRO 风险吗" | TRO 维权史查询 |
| "美国和欧盟的外观专利检索" | 多地区专利检测 |
| "检查这件家具的外观专利" | 按类目专利检索 |
| "这个产品设计卖起来安全吗" | 上架前专利排查 |
| "查找相似的外观专利" | 基于相似度的专利发现 |
| "专利侵权分析" | 综合专利风险报告 |

不适用场景见上方【能力边界】。

**边界判断**：当用户提及“专利检查”或“IP 风险”时，若关注点是产品外观/设计与已有专利的相似度，则适用本技能；若涉及发明专利、商标、版权，或需要实际法律咨询，则不适用。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**
- **响应提示积分或余额不足**：消息含“积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值”，或类似含义的内容。

### 措施
- 优先采用 skill 内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个 skill 并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个 skill。

---

# 睿观-外观专利检测 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/ruiguan/detectionPatentDesign`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`）读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| imageUrl | string | 是 | - | 产品图片文件URL，用于与专利数据库进行比对（最大1000字符） |
| queryMode | string | 是 | hybrid | 检索模式：`physical`（实物图检索）、`line`（线条图检索）、`hybrid`（混合检索）。最大1000字符 |
| topNumber | integer | 是 | 100 | 召回专利数量（最大100） |
| regions | string | 否 | US | 商品所售卖国家/地区代码，多选时用逗号隔开（如 `US,EU,CN`）。支持：US、EU、CN、JP、KR、DE、GB、FR、IT、AU、CA、BR、MX、IN、TH、SE、CH、IE、IL、DK、NZ、AT、BX、FI、WO。最大1000字符 |
| productTitle | string | 否 | - | 产品标题，用于补充检索上下文（最大1000字符） |
| productDescription | string | 否 | - | 产品描述，用于补充检索上下文（最大1000字符） |
| patentStatus | string | 否 | 1 | 专利有效性筛选：`1`（有效专利）、`0`（失效专利）、`1,0`（全部）。最大1000字符 |
| enableRadar | boolean | 否 | true | 是否启用雷达图（AI侵权判定分析） |
| topLoc | string | 否 | - | 指定检索的一级LOC范围（如 `06,07`）。格式：`^(0[1-9]\|1[0-9]\|2[0-9]\|3[0-2]\|ALL)(,(0[1-9]\|1[0-9]\|2[0-9]\|3[0-2]\|ALL))*$`。不指定时使用模型LOC预测服务的结果 |
| sourceLanguage | string | 否 | - | 原语言代码，需要标记以便统一翻译成英文（如 `zh-CN`）。文本为英语时传空即可。最大1000字符 |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 返回的专利记录总数 |
| data | array | 专利列表（详见下方专利对象） |
| columns | array | 渲染的列定义 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

### 专利对象（`data` 数组中的每个元素）

| 字段 | 类型 | 说明 |
|------|------|------|
| applicationNumber | string | 专利申请号 |
| publicationNumber | string | 专利公开号 |
| patentProd | string | 专利标题（英文） |
| patentProdCn | string | 专利标题（中文） |
| similarity | string | 专利与产品图片的相似度（0-1） |
| patentImageUrl | string | 与产品图片相似度最高的专利附图URL |
| images | array | 专利图片列表 |
| abstracts | string | 专利摘要 |
| specification | string | 专利说明书 |
| inventors | array | 发明人列表 |
| applicants | array | 申请人列表 |
| applicantAddresses | array | 申请人地址 |
| troCase | boolean | 是否有TRO维权史 |
| troHolder | boolean | 是否是TRO权利人的专利 |
| radarResult | object | AI雷达分析结果 |
| radarResult.same | boolean | 是否疑似侵权 |
| radarResult.exp | string | 预期描述（雷达判定说明） |
| patentLoc | string | 该专利的LOC分类（多个用逗号隔开） |
| locOneInfo | string | LOC一级详情 |
| locTwoInfo | string | LOC二级详情 |
| patentValidity | string | 专利有效性 |
| applicationDate | string | 专利申请日 |
| publicationDate | string | 专利公开日 |
| grantDate | string | 专利授权日 |
| estimatedDueDate | string | 预估到期日 |
| registrationOfficeCode | string | 专利注册受理局 |
| patentFamily | array | 同族专利列表 |
| globalPatentId | string | 全球专利ID |
| globalImageId | string | 专利图片的ID |
| isSketchText | string | 是否线稿图 |

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
curl -X POST https://tool-gateway.linkfox.com/ruiguan/detectionPatentDesign \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "imageUrl": "https://example.com/product.jpg",
    "queryMode": "hybrid",
    "topNumber": 50,
    "regions": "US",
    "enableRadar": true
  }'
```

## 多地区检索示例

```bash
curl -X POST https://tool-gateway.linkfox.com/ruiguan/detectionPatentDesign \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "imageUrl": "https://example.com/product.jpg",
    "queryMode": "physical",
    "topNumber": 100,
    "regions": "US,EU,CN",
    "productTitle": "便携式无线充电支架",
    "productDescription": "一款可折叠的智能手机无线充电支架",
    "patentStatus": "1",
    "enableRadar": true
  }'
```
