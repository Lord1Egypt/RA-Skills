---
name: linkfox-ecommerce-compliance-detection
display_name: Linkfox 电商合规检测
display_name_en: LinkFox E-commerce Compliance Detection
description: 电商知识产权与合规检测一站式 AI 工具集，整合睿观知产合规检测（版权/商标/外观专利/实用新型专利/图片政策）与智慧芽专利数据查询（著录/权利要求/说明书/附图/法律状态/家族/引用/以图搜图/PDF）共 2 类底层工具、22 项子能力。
description_zh: 电商知产与合规检测工具集，整合睿观（ruiguan_ip_detection）与智慧芽（zhihuiya_patent）2 类底层工具、22 项子能力。睿观覆盖图片版权、图形/文字商标、外观专利、实用新型专利、图片政策合规检测，返回相似度、权利人、TRO 与雷达侵权判定，支持 25+ 国家/地区。智慧芽覆盖专利核心/详细著录、标题摘要/权利要求/说明书及翻译、附图、法律状态、专利家族、引用分析、PDF 下载及外观/实用新型以图搜图。当用户需上架前版权/商标/专利侵权排查、TRO 风险评估、图片合规审查、专利查询翻译或以图搜专利时触发。参数见 references/，脚本见 scripts/。
description_en: One-stop e-commerce IP & compliance detection AI toolkit integrating 22 sub-capabilities across 2 tool families — Ruiguan (ruiguan_ip_detection: image copyright, graphic & text trademark, design & utility-model patent, and policy/compliance detection with similarity, rights owner, TRO litigation history and radar infringement verdicts across 25+ countries) and PatSnap/Zhihuiya (zhihuiya_patent: patent core/detailed bibliography, title-abstract translation, claims & translation, description & translation, abstract/fulltext drawings, legal status & event history, patent family, forward & back citations, PDF download, and design/utility-model patent image search). Triggered when the user needs pre-launch copyright/trademark/patent infringement checks, TRO risk assessment, product image compliance review, patent detail lookup & translation, or image-based patent search. Full params per sub-capability are in references/, executable scripts in scripts/.
category: e-commerce
version: 1.0.0
author: LinkFox
---

# Linkfox 电商合规检测（E-commerce Compliance Detection）

电商知识产权与合规检测一站式 AI 工具集，整合 **2 类底层工具、22 项子能力**：睿观（`ruiguan_ip_detection`）负责图片/文本类知产侵权与合规风险检测，智慧芽（`zhihuiya_patent`）负责专利数据查询与以图搜图。各子能力完整参数、响应字段与错误码见 `references/` 下对应文件，可执行脚本见 `scripts/`。

## 能力边界

### ✅ 能力范围
- **图片版权侵权检测**（`ruiguan_ip_detection`）：对图片 URL 与已登记版权作品库比对，返回相似度、权利人、版权标识码、TRO 维权史与雷达侵权判定（linkfox-ruiguan-copyright-detection）。
- **图形商标 / Logo 检测**（`ruiguan_ip_detection`）：产品图片与全球 15 国已注册图形商标库视觉相似度比对，含商标名、注册状态、尼斯分类、申请人、雷达判定（linkfox-ruiguan-trademark-graphic-detection）。
- **文字商标检测**（`ruiguan_ip_detection`）：产品 Listing 标题/描述文本与 15 国注册商标库比对，返回整体风险等级、黑白名单与逐条命中（linkfox-ruiguan-text-trademark-detection）。
- **外观设计专利检测**（`ruiguan_ip_detection`）：产品图片检索 25+ 国家/地区外观专利，含 AI 雷达侵权判定、TRO 风险与专利法律状态（linkfox-ruiguan-detection-patent-design）。
- **实用新型 / 发明专利检测**（`ruiguan_ip_detection`）：基于产品标题与描述检索相似实用新型/发明专利，含 TRO 风险与预估到期日（linkfox-ruiguan-utility-patent-detection，当前仅支持 US）。
- **图片政策合规检测**（`ruiguan_ip_detection`）：在已知违规/禁售商品库中按视觉相似度检索潜在违规商品（linkfox-ruiguan-gun-parts-search）。
- **专利以图搜图**（`zhihuiya_patent`）：通过图片 URL 检索相似外观设计（`D`）与实用新型（`U`）专利，按视觉相似度排序，支持按受理局、洛迦诺分类、法律状态、申请人、日期多维筛选（linkfox-zhihuiya-patent-image-search、linkfox-zhihuiya-utility-patent-image-search）。
- **专利著录查询**（`zhihuiya_patent`）：核心著录（标题/摘要/发明人/申请人/IPC·CPC 主分类）与详细著录（完整分类号/引用/优先权/预估到期日）（linkfox-zhihuiya-simple-bibliography、linkfox-zhihuiya-bibliography）。
- **专利全文与翻译**（`zhihuiya_patent`）：权利要求及翻译、说明书及翻译、标题摘要翻译，支持中/英/日（linkfox-zhihuiya-claim-data、linkfox-zhihuiya-claim-data-translated、linkfox-zhihuiya-description-data、linkfox-zhihuiya-description-data-translated、linkfox-zhihuiya-abstract-data-translated）。
- **专利附图**（`zhihuiya_patent`）：摘要附图与全文附图（图纸/示意图/图表）下载路径（linkfox-zhihuiya-abstract-image、linkfox-zhihuiya-fulltext-image）。
- **专利法律状态与家族**（`zhihuiya_patent`）：法律状态及事件历史（转让/许可/质押/诉讼/复审）、简单同族/INPADOC 同族跨国等同专利（linkfox-zhihuiya-legal-status、linkfox-zhihuiya-patent-family）。
- **专利引用分析**（`zhihuiya_patent`）：被引用次数（3/5 年）及引用专利列表、参考文献（在先技术，含专利与非专利文献）（linkfox-zhihuiya-patent-cited、linkfox-zhihuiya-patent-forward-citation）。
- **专利 PDF 下载**（`zhihuiya_patent`）：单篇/批量（上限 100）专利 PDF 全文下载链接（linkfox-zhihuiya-pdf-data）。
- 覆盖睿观 25+ 国家/地区（外观专利）与 15 国（商标）、智慧芽全球专利库；本地图片可经 `upload_image.py` 转公开 URL 后检测/检索。

### ❌ 边界与限制
- **API Key 必需**：所有工具均需环境变量 `LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`）；各工具独立计费、独立限频，数据时效与站点覆盖随数据源而异。
- **计费约束**：同一会话同一参数组合默认只调用一次（脚本带 24h 本地缓存）；失败或空结果不得自动换图、换关键词、翻页或改参数连续试探；需继续检索时先向用户说明会产生额外消耗（各工具计费规则见 `skills-version.json` 对应条目与 references 内 api.md 的 `costToken` 字段；睿观雷达检测开启时计费翻倍，智慧芽多数按返回条数计费）。
- **图片 URL 必需**：睿观图片类检测与智慧芽以图搜图仅接受可公开访问的图片 URL，不直接接收本地文件；本地图片须先用 `scripts/upload_image.py` 转为公开 URL（有效期 24 小时）。
- **非法律意见**：所有检测结果仅呈现数据（相似度、风险指标、专利信息），不提供侵权法律结论、FTO 自由实施意见或诉讼策略；法律结论须咨询专业律师。
- **不在范围内**：商标/专利/版权的注册申请与登记办理；店铺运营（Listing 刊登/订单/库存）、广告投放、物流与供应链；音乐/视频版权检测；基于文本的专利检索（关键词/摘要检索，本工具仅支持以图搜图）；专利年费管理与监控、专利估值或许可谈判；与平台或权利人的直接沟通；非电商任务。
- **数据时效**：睿观检测为实时/准实时抓取；智慧芽专利数据为其数据库更新周期，`costToken`/`lastUpdate` 等字段标识消耗与刷新。

## 工具选择指南

按需求在下表定到子能力，再跳到【业务需求路由速查】查端点/脚本/references 取参执行。

| 需求 / 用户说 | 默认推荐（子能力） | 何时换用其他 |
|---|---|---|
| 图片版权侵权 / TRO 风险（"这张图有没有版权问题"） | `linkfox-ruiguan-copyright-detection` | 查图形商标/Logo 用 `linkfox-ruiguan-trademark-graphic-detection`；查外观专利用 `linkfox-ruiguan-detection-patent-design` |
| 图形商标 / Logo 侵权（"图片有没有商标问题"） | `linkfox-ruiguan-trademark-graphic-detection` | 查文字商标（标题/描述文本）用 `linkfox-ruiguan-text-trademark-detection` |
| 文字商标 / 标题品牌侵权（"标题有没有商标问题"） | `linkfox-ruiguan-text-trademark-detection` | 查图形商标用 `linkfox-ruiguan-trademark-graphic-detection` |
| 外观专利侵权 / TRO（"产品外观有没有专利风险"） | `linkfox-ruiguan-detection-patent-design`（睿观，25+ 国，含雷达判定与 TRO） | 仅需视觉相似专利列表（不要 TRO/侵权判定）用 `linkfox-zhihuiya-patent-image-search`（patentType=`D`） |
| 实用新型/发明专利风险（"产品结构有没有专利风险"） | `linkfox-ruiguan-utility-patent-detection`（基于标题描述，仅 US） | 有产品图片想以图搜实用新型专利用 `linkfox-zhihuiya-utility-patent-image-search` |
| 图片政策合规 / 禁售商品（"这图有没有违规/禁售风险"） | `linkfox-ruiguan-gun-parts-search` | — |
| 以图搜外观专利（"用图找相似外观专利"） | `linkfox-zhihuiya-patent-image-search`（仅 `D`，强制 model 1/2） | 要实用新型以图搜图用 `linkfox-zhihuiya-utility-patent-image-search`；要 TRO/侵权判定用 `linkfox-ruiguan-detection-patent-design` |
| 以图搜实用新型专利（"用图找相似实用新型专利"） | `linkfox-zhihuiya-utility-patent-image-search`（仅 `U`，强制 model 3/4） | 要外观专利以图搜图用 `linkfox-zhihuiya-patent-image-search`；要基于标题描述的实用新型侵权检测用 `linkfox-ruiguan-utility-patent-detection` |
| 专利基本信息 / 发明人申请人（"这专利是谁的"） | `linkfox-zhihuiya-simple-bibliography`（核心著录，轻量） | 要完整分类号/引用/优先权/预估到期日用 `linkfox-zhihuiya-bibliography` |
| 专利详细著录 / 分类号 / 优先权（"专利完整信息"） | `linkfox-zhihuiya-bibliography` | 只要标题/摘要/发明人用 `linkfox-zhihuiya-simple-bibliography` |
| 专利标题/摘要翻译（"翻译专利摘要"） | `linkfox-zhihuiya-abstract-data-translated`（中/英/日） | 要权利要求翻译用 `linkfox-zhihuiya-claim-data-translated`；要说明书翻译用 `linkfox-zhihuiya-description-data-translated` |
| 专利权利要求（"看权利要求"） | `linkfox-zhihuiya-claim-data` | 要翻译用 `linkfox-zhihuiya-claim-data-translated` |
| 专利说明书（"看说明书/全文"） | `linkfox-zhihuiya-description-data` | 要翻译用 `linkfox-zhihuiya-description-data-translated`；要 PDF 用 `linkfox-zhihuiya-pdf-data` |
| 专利附图 / 图纸（"看专利图"） | `linkfox-zhihuiya-abstract-image`（摘要附图，单张） | 要全部图纸用 `linkfox-zhihuiya-fulltext-image` |
| 专利法律状态 / 是否有效（"这专利还有效吗"） | `linkfox-zhihuiya-legal-status` | — |
| 专利家族 / 跨国等同（"这专利的家族/等同专利"） | `linkfox-zhihuiya-patent-family` | — |
| 专利被引用次数 / 影响力（"被引用多少次"） | `linkfox-zhihuiya-patent-cited`（被引用，看谁引用了本专利） | 要本专利引用了哪些文献用 `linkfox-zhihuiya-patent-forward-citation` |
| 专利参考文献 / 在先技术（"引用了哪些专利"） | `linkfox-zhihuiya-patent-forward-citation`（参考文献，看本专利引用了谁） | 要被引用次数用 `linkfox-zhihuiya-patent-cited` |
| 专利 PDF 下载（"下载专利 PDF"） | `linkfox-zhihuiya-pdf-data` | — |

### 工具选择思路
- **重要**：多个子能力满足需求时，要依据需求深入分析子能力的功能、用途、出入参，从中调研出最合适的子能力，并推荐用户，让用户自己决定。
- 满足程度同等的前提下，向用户推荐"默认推荐子能力"。

## 业务需求路由速查

按【工具选择指南】定到子能力 后，下表查端点、脚本与 references 文件取参执行：

### 子能力 ↔ references 文件 ↔ 端点 ↔ 脚本（22 项）

**ruiguan_ip_detection**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-ruiguan-copyright-detection | references/linkfox-ruiguan-copyright-detection.md | POST /ruiguan/copyrightDetection | ruiguan_copyright_detection.py |
| linkfox-ruiguan-trademark-graphic-detection | references/linkfox-ruiguan-trademark-graphic-detection.md | POST /ruiguan/trademarkGraphicDetection | ruiguan_trademark_graphic_detection.py |
| linkfox-ruiguan-text-trademark-detection | references/linkfox-ruiguan-text-trademark-detection.md | POST /ruiguan/textTrademarkDetection | ruiguan_text_trademark_detection.py |
| linkfox-ruiguan-detection-patent-design | references/linkfox-ruiguan-detection-patent-design.md | POST /ruiguan/detectionPatentDesign | ruiguan_detection_patent_design.py |
| linkfox-ruiguan-utility-patent-detection | references/linkfox-ruiguan-utility-patent-detection.md | POST /ruiguan/utilityPatentDetection | ruiguan_utility_patent_detection.py |
| linkfox-ruiguan-gun-parts-search | references/linkfox-ruiguan-gun-parts-search.md | POST /ruiguan/gunPartsSearch | ruiguan_image_compliance_search.py |

**zhihuiya_patent**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-zhihuiya-patent-image-search | references/linkfox-zhihuiya-patent-image-search.md | POST /zhihuiya/patentImageSearch | zhihuiya_patent_image_search.py |
| linkfox-zhihuiya-utility-patent-image-search | references/linkfox-zhihuiya-utility-patent-image-search.md | POST /zhihuiya/patentImageSearch | zhihuiya_utility_patent_image_search.py ¹ |
| linkfox-zhihuiya-simple-bibliography | references/linkfox-zhihuiya-simple-bibliography.md | POST /zhihuiya/simpleBibliography | zhihuiya_simple_bibliography.py |
| linkfox-zhihuiya-bibliography | references/linkfox-zhihuiya-bibliography.md | POST /zhihuiya/bibliography | zhihuiya_bibliography.py |
| linkfox-zhihuiya-abstract-data-translated | references/linkfox-zhihuiya-abstract-data-translated.md | POST /zhihuiya/abstractDataTranslated | zhihuiya_abstract_translated.py |
| linkfox-zhihuiya-claim-data | references/linkfox-zhihuiya-claim-data.md | POST /zhihuiya/claimData | zhihuiya_claim_data.py |
| linkfox-zhihuiya-claim-data-translated | references/linkfox-zhihuiya-claim-data-translated.md | POST /zhihuiya/claimDataTranslated | zhihuiya_claim_translated.py |
| linkfox-zhihuiya-description-data | references/linkfox-zhihuiya-description-data.md | POST /zhihuiya/descriptionData | zhihuiya_description_data.py |
| linkfox-zhihuiya-description-data-translated | references/linkfox-zhihuiya-description-data-translated.md | POST /zhihuiya/descriptionDataTranslated | zhihuiya_description_translated.py |
| linkfox-zhihuiya-abstract-image | references/linkfox-zhihuiya-abstract-image.md | POST /zhihuiya/abstractImage | zhihuiya_abstract_image.py |
| linkfox-zhihuiya-fulltext-image | references/linkfox-zhihuiya-fulltext-image.md | POST /zhihuiya/fulltextImage | zhihuiya_fulltext_image.py |
| linkfox-zhihuiya-legal-status | references/linkfox-zhihuiya-legal-status.md | POST /zhihuiya/legalStatus | zhihuiya_legal_status.py |
| linkfox-zhihuiya-patent-family | references/linkfox-zhihuiya-patent-family.md | POST /zhihuiya/patentFamily | zhihuiya_patent_family.py |
| linkfox-zhihuiya-patent-cited | references/linkfox-zhihuiya-patent-cited.md | POST /zhihuiya/patentCited | zhihuiya_cited_by.py |
| linkfox-zhihuiya-patent-forward-citation | references/linkfox-zhihuiya-patent-forward-citation.md | POST /zhihuiya/patentForwardCitation | zhihuiya_cited_references.py |
| linkfox-zhihuiya-pdf-data | references/linkfox-zhihuiya-pdf-data.md | POST /zhihuiya/pdfData | zhihuiya_pdf_data.py |

> ¹ `linkfox-zhihuiya-patent-image-search` 与 `linkfox-zhihuiya-utility-patent-image-search` 共用同一端点 `/zhihuiya/patentImageSearch`，均源自 `skills/` 下已拆分的同名 skill（外观版仅 `D`/model 1-2、实用新型版仅 `U`/model 3-4，互为镜像）。源脚本同名（`zhihuiya_patent_image_search.py`），为避免文件冲突，实用新型版在 `scripts/` 中更名为 `zhihuiya_utility_patent_image_search.py`；两者内容逐字保留、各强制对应专利类型。其 references 归档正文仍按源文件逐字保留原脚本名。

## 调用方式

- **网关**：`${LINKFOX_TOOL_GATEWAY}/<端点>`，请求方式 POST、Content-Type `application/json`，认证 Header `Authorization: <api_key>`（api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取；未配置按下方【解决认证和积分问题】处理）。各端点路径见上方【业务需求路由速查】与对应 references 文件。
- **Python 脚本**：每项子能力对应 `scripts/<脚本名>.py '<JSON 参数>' [--inline]`（脚本名与端点见路由速查表）。图片类工具需先 `scripts/upload_image.py <本地图片路径>` 获取公开 URL。脚本内部完成网关调用、鉴权与落盘。
- **输出策略（脚本默认行为）**：始终将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill>-<timestamp>.json`（`<cwd>` 为脚本执行时工作目录；`<session>` 取自环境变量 `SESSION_ID`；禁止写入 /tmp，当前目录不可写则报错）；响应体 ≤ 8 KB 落盘后完整打印到 stdout，> 8 KB 仅打印摘要（顶层字段、常见计数、最大列表长度 + 前 3 条样本）；加 `--inline` 强制全量打印（同样落盘）。
- **读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 PowerShell `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。
- **完整参数**：每个子能力的请求参数、响应字段、错误码、curl 示例见 `references/<子能力>.md`（文件内含该子能力 SKILL.md 正文与 api.md 全文）。

## 使用示例

以下按数据层给出代表性子能力的出入参示例；其余子能力参数见对应 references 文件。睿观图片类工具的 `imageUrl`、智慧芽以图搜图的 `url` 均须为可公开访问的图片 URL（本地图片先经 `upload_image.py` 转换）；智慧芽查询类统一用 `patentId` 或 `patentNumber`（公开号，二选一）。

### 知产合规检测层（睿观 ruiguan_ip_detection）

**1. 图片版权检测（copyrightDetection → ruiguan_copyright_detection.py）**
```json
{"imageUrl": "https://example.com/product-image.jpg", "topNumber": 100, "enableRadar": true}
```
出参：`data[]`（similarity/rightsOwner/copyrightCode/subRadarResult/troCase/troHolder/path/pathThumb）、`total`、`costToken`。`enableRadar` 开启时计费翻倍但含雷达侵权判定。

**2. 图形商标检测（trademarkGraphicDetection → ruiguan_trademark_graphic_detection.py）**
```json
{"imageUrl": "https://example.com/product-image.jpg", "topNumber": 10, "regions": "US,EM", "enableRadar": true}
```
出参：`data[]`（similarity/trademarkName/tradeMarkStatus/registrationOfficeCode/niceClassName/applicantName/subRadarResult/image）、`total`、`boundingBoxCount`、`radarResult`、`costToken`。

**3. 文字商标检测（textTrademarkDetection → ruiguan_text_trademark_detection.py）**
```json
{"productTitle": "Wireless Bluetooth Headphones Noise Cancelling Over Ear", "regions": "US", "limit": 100}
```
出参：`data[]`（trademarkName/region/score/highestModeScore/holder/isFamous/isActiveHolder）、`total`、`textTrademarkRadar`、`blacklistTrademarks`、`whitelistTrademarks`、`costToken`。基于文本（标题/描述），无需图片。

**4. 外观专利检测（detectionPatentDesign → ruiguan_detection_patent_design.py）**
```json
{"imageUrl": "https://example.com/product.jpg", "queryMode": "hybrid", "topNumber": 50, "regions": "US", "enableRadar": true}
```
出参：`data[]`（similarity/patentProdCn/applicationNumber/patentLoc/patentValidity/troCase/troHolder/radarResult{same,exp}/patentImageUrl/images）、`total`、`costToken`。覆盖 25+ 国家/地区，`queryMode` 可选 `hybrid`/`image`/`text`。

**5. 实用新型/发明专利检测（utilityPatentDetection → ruiguan_utility_patent_detection.py）**
```json
{"productTitle": "便携式USB-C 65W氮化镓快充充电器", "productDescription": "紧凑型65W氮化镓USB-C快充充电器，可折叠插脚，支持PD3.0/QC4.0，双USB-C+USB-A", "region": "US", "topNumber": 100}
```
出参：`data[]`（similarity/title/titleCn/patentValidity/applicationNumber/publicationDate/estimatedDueDate/troCase/troHolder/patentImageUrl/images）、`total`、`costToken`。基于标题+描述检索，当前仅支持 US。

**6. 图片政策合规检测（gunPartsSearch → ruiguan_image_compliance_search.py）**
```json
{"imageUrl": "https://example.com/product-image.jpg"}
```
出参：`data[]`（cosine/pdImgOssUrl/pdTitle/pdTitleCHNCensored）、`total`、`costToken`。在违规/禁售商品库中按视觉相似度检索。

### 专利数据查询层（智慧芽 zhihuiya_patent）

**7. 专利以图搜图-外观（patentImageSearch → zhihuiya_patent_image_search.py）**
```json
{"url": "https://example.com/my-product.jpg", "patentType": "D", "model": 1, "limit": 20}
```
出参：`data[]`（patentPn/title/score/url/loc）、`allRecordsCount`、`costToken`。本脚本仅支持外观设计专利（强制 `patentType=D`、`model∈{1,2}`）；实用新型以图搜图用 `zhihuiya_utility_patent_image_search.py`（见示例 8）。

**8. 专利以图搜图-实用新型（patentImageSearch → zhihuiya_utility_patent_image_search.py）**
```json
{"url": "https://example.com/my-product.jpg", "patentType": "U", "model": 4, "country": "CN", "limit": 20}
```
出参：同上；脚本强制 `patentType=U`、`model∈{3,4}`，外观专利检索请用 `zhihuiya_patent_image_search.py`。

**9. 专利核心著录（simpleBibliography → zhihuiya_simple_bibliography.py）**
```json
{"patentNumber": "US11234567B2"}
```
出参：`data[]`（pn/title/abstractContent/applicants/inventors/assignees/ipcMain/cpcMain/citedPatents）、`costToken`。

**10. 专利详细著录（bibliography → zhihuiya_bibliography.py）**
```json
{"patentNumber": "US10123456B2"}
```
出参：`data[]`（pn/patentType/applicants/assignees/inventors/classificationIpcr/classificationCpc/priorityClaims/referenceCitedPatents/exdt）、`costToken`。比核心著录更全（含完整分类号/引用/优先权/预估到期日）。

**11. 专利权利要求（claimData → zhihuiya_claim_data.py）**
```json
{"patentNumber": "CN115000000A"}
```
出参：`data[]`（pn/claims/claimCount/pnRelated）、`total`、`costToken`。翻译版加 `lang`（`cn`/`en`/`jp`）用 `zhihuiya_claim_translated.py`。

**12. 专利法律状态（legalStatus → zhihuiya_legal_status.py）**
```json
{"patentNumber": "CN115000000A"}
```
出参：`data[]`（pn/simpleLegalStatus/legalStatus/eventStatus/legalDate）、`costToken`。`simpleLegalStatus`：`0`失效/`1`有效/`2`审中。

**13. 专利被引用（patentCited → zhihuiya_cited_by.py）**
```json
{"patentNumber": "US10123456B2"}
```
出参：`data[]`（pn/citedBy3y/citedBy5y/citedBySimpleFamily/citedByInpadocFamily/citedByPatents）、`costToken`。看"谁引用了本专利"。

**14. 专利 PDF 下载（pdfData → zhihuiya_pdf_data.py）**
```json
{"patentNumber": "US20230012345A1"}
```
出参：`data[]`（pn/pdfPath/pnRelated）、`total`、`costToken`。支持单篇/批量（上限 100），`replaceByRelated` 可同族替代。

## 展示规则

1. **客观呈现数据**：以清晰表格展示检测结果/专利信息，不做主观法律结论（除非用户主动要求）；标注数据来自睿观还是智慧芽。
2. **来源标注**：展示数据时说明来自哪个工具/数据源（睿观版权/商标/外观专利/实用新型专利/政策合规，或智慧芽著录/权利要求/说明书/附图/法律状态/家族/引用/PDF/以图搜图）。
3. **高风险高亮**：睿观检测中相似度较高（如 ≥ 0.80）或雷达判定侵权（`subRadarResult`/`radarResult` = 1）或存在 TRO 维权史（`troCase`/`troHolder` = true）时，明确标注为高风险条目并醒目提示。
4. **不可用数据**：值为 `0` 或 `-1` 的字段表示数据不可用，标注"N/A"或省略，不作实际值展示。
5. **法律声明**：以图搜图与侵权检测结果末尾附加提示：结果基于视觉相似度/数据比对，不构成侵权法律判定，建议咨询专业律师。
6. **错误处理与协同**：查询失败时根据响应 `errcode`/`errmsg` 说明原因并建议修正（图片 URL 不可公开访问、ASIN/专利号格式、站点/国家代码、参数越界等）；连续使用多工具时将各工具发现汇总为连贯分析，标注数据来源与时间窗。

## 解决认证和积分问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

**注意**：你是workbuddy，并且渠道是workbuddy，使用 onboarding 引导登录注册时 channel **必须**为 workbuddy。这非常重要！

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。
