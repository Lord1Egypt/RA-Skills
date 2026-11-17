---
name: linkfox-ruiguan-gun-parts-search
description: 基于睿观的图片政策合规性检测工具，通过视觉相似度比对识别潜在的违规及禁售风险商品。
---

# 睿观-图片政策合规监测（Ruiguan Gun Parts Search）

本技能基于睿观对产品图片进行政策合规检测，通过视觉相似度比对，在已知违规商品库中检索视觉相似商品，识别潜在的违规及禁售风险。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 根据产品图片 URL，在违规商品库中进行基于视觉相似度的检索，返回匹配的违规商品列表。
- 返回每条匹配的相似度分数（cosine，0~1）、违规商品图片、中英文标题等信息。
- 支持本地图片：用户提供本地文件路径时，先上传获取公开 URL，再发起检测。

### ❌ 边界与限制

- **仅基于图片**：本工具只分析图片 URL，不分析文本描述或商品元数据。
- **URL 可访问性**：图片 URL 必须可被检测服务公开访问；本地文件须先上传。
- **URL 长度上限**：图片 URL 不得超过 1000 字符。
- **相似度≠定论**：结果基于视觉相似度，不构成确定性的政策裁定。
- **不在范围内**：文本类合规分析；商品类目分类；知识产权/商标侵权；专利或版权检测（使用其他睿观技能）。

## 核心概念

睿观图片政策合规检测是一项基于图片的合规筛查服务。给定产品图片 URL，在已知违规商品库中检索视觉相似商品，并按相似度排序返回。

**相似度分数（cosine）**：取值 0~1，值越高表示与已知违规商品视觉越相似；接近 1.0 表示几乎与已标记的违规商品完全一致。

## 调用方式

- **API 端点**：`POST /ruiguan/gunPartsSearch`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/ruiguan_image_compliance_search.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词或翻页连续试探；需要继续检索时先向用户说明会产生额外消耗。

**本地图片上传**：本工具要求**公开可访问的图片 URL**。若用户提供本地文件路径（如 `C:\Users\...\photo.png`、`/home/.../image.jpg`），须先上传获取公开 URL：

```bash
python scripts/upload_image.py /path/to/local/image.png
```

脚本会返回一个公开 URL（24 小时有效），用作图片 URL 参数。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-ruiguan-gun-parts-search-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 单张产品图片合规检测**
```
检测这张产品图片是否有合规风险：https://example.com/images/product-123.jpg
```

**2. 批量检测多张产品图片**
```
请扫描这些产品图片，看是否存在潜在违规：
- https://example.com/images/item-a.jpg
- https://example.com/images/item-b.jpg
```

**3. 上架前合规预检**
```
上架这个产品前，帮我检查图片是否会触发政策风险：
图片：https://example.com/new-product.png
```

## 展示规则

1. **清晰表格呈现**：以结构化表格展示每条匹配的违规商品图片、相似度分数、中英文标题。
2. **高亮高相似匹配**：当 cosine 分数超过 0.8 时，明确标记为强匹配，提示需重点关注。
3. **展示违规图片**：返回结果含 `pdImgOssUrl` 时，展示匹配的违规商品图片，便于用户直观对比。
4. **解释分数含义**：始终说明相似度分数的含义——值越高表示与已知违规商品越相似。
5. **错误处理**：查询失败时说明原因，并建议检查图片 URL 是否有效且公开可访问。
6. **不做法律建议**：客观呈现检测结果，不提供法律结论；提醒用户以平台政策为准进行核实。

## 用户表达与场景速查

**适用** —— 基于图片的产品政策合规检测：

| 用户说 | 场景 |
|--------|------|
| "检测这张产品图片是否有合规风险" | 单图合规检测 |
| "扫描我的产品图片是否有违规" | 批量合规筛查 |
| "这张图片是否被标记为禁售商品" | 特定违规查询 |
| "上架前帮我筛查一下图片的政策风险" | 上架前合规预检 |
| "找一下这张产品图片的相似违规" | 相似度违规检索 |
| "这个产品能安全上架吗" | 合规风险预检 |
| "帮我检测一下这个图片是否违规" | 单图合规检测 |

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

# 睿观-图片合规检测 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/ruiguan/gunPartsSearch`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`）读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| imageUrl | string | 是 | 待检测的产品图片URL（最大长度 1000 字符） |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 检测出的政策违规产品列表（详见下方） |
| detectId | string | 检测记录 id |
| columns | array | 渲染的列 |
| costToken | integer | 消耗token |
| type | string | 渲染的样式 |

### data 数组元素字段

| 字段 | 类型 | 说明 |
|------|------|------|
| pdImgOssUrl | string | 匹配到的违规产品图片 URL |
| cosine | number | 检测产品与违规产品相似度 |
| pdTitle | string | 匹配到的违规产品标题 |
| pdTitleCHNCensored | string | 匹配到的违规产品中文标题 |

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
curl -X POST https://tool-gateway.linkfox.com/ruiguan/gunPartsSearch \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"imageUrl": "https://example.com/product-image.jpg"}'
```
