---
name: linkfox-maidalv-product-tro-detection
description: 通过卖大律检测产品是否存在 TRO（临时限制令）与知识产权（商标/专利/版权）侵权风险，输入产品主图（支持图片 URL 或 Base64 data URI），可补充参考图、参考文本、IP 关键词，返回总体风险等级、高风险侵权项与低风险 IP 清单（含 TRO 原告、立案日期、法院案号、案件数）、0-10 数值风险分及 AI 生成的法律评估报告。当用户提到 TRO 检测、TRO 风险、TRO 侵权、知识产权侵权检测、商标侵权、专利侵权、版权侵权、IP 风险检测、产品合规检测、卖大律、product TRO detection, IP infringement risk, trademark/patent/copyright infringement check 时触发此技能。即使用户未明确提及"卖大律"或"TRO"，只要用户提供产品图片并希望评估其在商标、专利、版权或 TRO 方面的侵权风险，也应触发此技能。
---

# Product Infringement & TRO Risk Detection

This skill detects whether a product carries TRO (Temporary Restraining Order) or IP infringement risk by checking a product image against a database of IP assets (trademarks, patents, copyrights) and TRO case plaintiffs. It returns an overall risk level, high-risk hits, a low-risk IP list with TRO plaintiff details, numeric risk scores, and an AI-generated legal report.

## Core Concepts

TRO (Temporary Restraining Order) is a legal injunction brand owners file against sellers (often Amazon listings) for trademark/copyright/patent infringement. This tool takes a **main product image** (URL or Base64 data URI) plus optional reference images / text / IP keywords, runs visual + text matching against IP assets and TRO case records, and returns a structured risk assessment with an AI legal report (localized by the `language` parameter).

## Data Fields

**Top-level response:**

| Field | Description |
|-------|-------------|
| errcode | 200 = success; see api.md for other codes |
| status | Overall analysis status (`success`) |
| checkId | Unique ID for this detection run |
| riskLevel | Overall risk: 高风险/中风险/低风险 (High/Medium/Low Risk) |
| total | Count of high-risk hits (length of `results`) |
| results | High-risk infringement items (array) |
| nonResults | Low-risk / non-high IP items incl. TRO plaintiff info (array) |
| costToken | Tokens consumed this call |
| columns | Render column metadata (display only) |

**Each item (results / nonResults):**

| Field | Description |
|-------|-------------|
| ipType | `Trademark` / `Copyright` / `Patent` |
| text | IP text (trademark word, patent/copyright title) |
| ipOwner | IP rights owner |
| regNo | Registration number (may be a JSON-string array, e.g. `["1221667"]`) |
| riskLevel / riskScore / riskDescription | Risk rating / 0-10 score / text; present only when scored |
| ipAssetUrls | URLs to IP evidence images |
| plaintiffName / plaintiffId | TRO plaintiff (present only when IP appears in a TRO case) |
| numberOfCases | Plaintiff's case count (TRO only) |
| lastCaseDocket / lastCaseDateFiled | Most recent court docket / filing date (TRO only) |
| report | AI-generated legal assessment (localized by `language`) |

## Parameter Guide

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| mainProductImage | Yes | - | Main product image: URL or `data:image/...;base64,...` (≤1000 chars) |
| referenceImages | No | - | Reference images for similar products, up to 3 (URL or data URI) |
| otherProductImages | No | - | Additional product images, up to 5 (URL or data URI) |
| ipImages | No | - | IP-related images, up to 3 (URL or data URI) |
| referenceText | No | - | Text from similar products (e.g. product title), ≤1000 chars |
| description | No | - | Product description (title recommended), ≤1000 chars |
| ipKeywords | No | - | IP-related keywords, up to 20 |
| language | No | zh | Legal report language (`zh` / `en`); only affects the `report` language |

**Image rules:** URL must be publicly accessible; Base64 must include the `data:image/...;base64,` prefix. For a local image, either upload it first (see 「Local Image Upload」) or convert it to a data URI.

## 调用方式

- **API 端点**：`POST /maidalv/checkApiFlash`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/maidalv_check_api_flash.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、换主图或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-maidalv-product-tro-detection-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## Local Image Upload

This tool accepts a **publicly accessible image URL** or a Base64 data URI. If the user provides a local image file path, either upload it first to obtain a public URL, or encode it to a data URI.

Run the upload script:
```bash
python scripts/upload_image.py /path/to/local/image.png
```

The script returns a public URL (valid for 24 hours) usable as `mainProductImage`.

## Usage Examples

**1. Basic detection (main image only)**
```
检测这个产品的 TRO 和知识产权侵权风险，图片地址为 https://m.media-amazon.com/images/I/71jKJgFpg8L._AC_SL1500_.jpg
```

**2. English legal report**
```
Check this product for TRO and IP infringement risk: https://example.com/product.jpg — give me the legal report in English.
```

**3. With reference image + IP keywords**
```
检测这个图片的侵权风险，主图 https://example.com/product.jpg，参考图 https://example.com/ref.jpg，IP 关键词 apple、iphone
```

## Display Rules

1. **Lead with the overall verdict**: Show `riskLevel` (高风险/中风险/低风险) and `checkId` first.
2. **High-risk items first**: If `results` is non-empty, list each hit's `ipType` / `text` / `ipOwner` / `riskScore` / `riskDescription` prominently.
3. **TRO plaintiff detail**: For items with `plaintiffName`, show plaintiff, `numberOfCases`, `lastCaseDocket`, `lastCaseDateFiled` — these drive TRO risk.
4. **Evidence images**: Display `ipAssetUrls` inline for visual comparison when available.
5. **AI legal report**: Surface the `report` field (long-form legal assessment) for high-risk items.
6. **Counts**: Always state `total` (high-risk count) and `nonResults` length.
7. **No secondary processing**: Results are a one-shot analysis; no SQL/secondary query is available.

## Important Limitations

1. **One-shot analysis**: Results are not stored in a database; cannot use `_dataQuery_executeDynamicQuery` for secondary processing.
2. **Image input**: `mainProductImage` is required. Local images must be uploaded or Base64-encoded (with `data:image/...;base64,` prefix).
3. **Language scope**: `language` only affects the `report` text; field values remain as returned.
4. **Conditional fields are expected**: Non-TRO / unscored items return only base fields (`ipType`/`text`/`ipOwner`/`regNo`/`ipAssetUrls`); plaintiff/case and risk fields are **absent** (not null) when not applicable — do not treat missing fields as an error.
5. **`columns` is render-meta**: Its length differs from the data arrays; do not use it to infer result counts (use `results` / `nonResults` lengths).

## User Expression & Scenario Quick Reference

**Applicable** — Product TRO / IP infringement risk checks:

| User Says | Scenario |
|-----------|----------|
| "这个产品有没有 TRO 风险" / "会不会被起诉" | Basic TRO risk check |
| "这个图片有没有商标/专利/版权侵权" | IP infringement detection |
| "这个 Amazon 产品上架有没有侵权风险" | Pre-listing compliance check |
| "查一下这个产品的原告信息" | TRO plaintiff lookup |
| "给我英文的法律评估报告" | English legal report |

**Not applicable** — Beyond this tool:

- 1688 / Amazon image-based product sourcing (use 以图搜图 skills)
- Patent全文 / 权利要求检索 (use 智慧芽/Eureka patent skills)
- Listing 文案优化或关键词分析

**Boundary judgment**: When the user provides a product image and asks about infringement/TRO/legal risk, this skill applies. If they want supplier sourcing or keyword analytics, use the respective sourcing/keyword tools instead.

## 算力消耗规则

消耗 113 算力（约 150000 token）。

> 用户会因算力消耗而支付费用。本工具单次调用成本较高（含 AI 法律评估），请充分评估：当需要高频调用本技能，或用户对算力消耗量预期不足时，务必提醒用户，由用户决定是否继续。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
