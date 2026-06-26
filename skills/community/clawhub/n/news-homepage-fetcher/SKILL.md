---
name: openclaw-news-homepage-fetcher
description: "Homepage-first news collection from major international, Singaporean, and China-focused outlets. Use for: opening news homepages, clicking article links, extracting article text and metadata, translating into Chinese, deduplicating stories, and assembling Word-ready daily digests."
---

# OpenClaw News Homepage Fetcher

使用本技能时，应把任务理解为**“从主流新闻网站首页出发，进入当天重点文章，提取正文，翻译成中文，并整理成可直接进入 Word 的日报素材”**，而不是单纯做搜索引擎聚合。

## 何时使用

在以下场景中触发本技能：

1. 用户要求抓取每日新闻、早报、晚报、国际新闻汇总、新加坡新闻汇总或中国新闻汇总。
2. 用户要求从 BBC、CNA、联合早报、新华社、人民网、路透社等主流媒体首页点击进入新闻正文。
3. 用户要求提取文章全文、保留出处、翻译成中文，并进一步生成 Word 文档或 Word-ready 中间稿。
4. 用户要求按国家、地区、媒体类别或栏目汇总新闻，并去重后输出日报。

## 不适用场景

在以下场景中，不要把本技能作为主方法：

1. 用户只要单篇文章摘要，而不需要首页导航式抓取。
2. 用户要求抓取社交媒体帖子、论坛内容或非新闻站点。
3. 用户要求绕过付费墙、登录墙或访问限制。
4. 用户要求实时高频监控、秒级推送或全站爬虫式抓取。

## 先读取哪些参考文件

默认先读以下文件，再开始执行。

| 文件 | 何时读取 | 作用 |
|---|---|---|
| `references/source_catalog.md` | 每次选新闻源时 | 查看主流站点链接、优先级和使用建议 |
| `references/source_manifest.yaml` | 需要程序化配置站点时 | 读取机器可读的站点清单 |
| `references/translation_docx_spec.md` | 需要翻译、摘要、生成 Word-ready 输出时 | 对齐字段规范、中文风格和文档结构 |
| `templates/daily_news_digest_template.md` | 需要生成最终汇编时 | 复用日报模板 |

## 默认工作流

按以下顺序执行，不要跳步。

1. **确定新闻范围。** 先判断用户要国际新闻、新加坡新闻、中国新闻、财经新闻，还是综合日报；再决定抓取的媒体组合和每个媒体的篇数上限。
2. **打开首页或频道首页。** 优先从站点首页进入；必要时补充 world、asia、china、singapore、business 等频道页。
3. **筛选候选链接。** 只保留正文型文章链接，排除直播页、纯视频页、播客页、评论页、注册页、专题聚合页和广告页。
4. **进入文章正文。** 提取标题、作者、发布时间、栏目、正文段落、原始链接和站点名。
5. **执行正文清洗。** 删除导航、推荐阅读、广告、社交按钮、版权尾注和重复段落；保留对理解事件有用的图片说明或关键引述。
6. **执行去重。** 若多家媒体报道同一事件，保留多源版本，但避免同一媒体同一事件的重复卡片；对重复稿使用统一事件标签。
7. **生成中文结果。** 对英文原文生成中文标题、中文摘要和中文全文译文；对中文原文生成标准化摘要。
8. **组装日报。** 按国际、新加坡、中国、财经等栏目编排，输出为 Word-ready Markdown、结构化 JSON 或直接 DOCX 所需中间稿。
9. **标记异常。** 遇到付费墙、正文缺失、脚本加载失败或链接失效时，写入失败说明，不要伪造内容。

## 首页抓取规则

默认采用“首页优先、频道补充、正文确认”的策略。

### 链接选择

优先点击以下位置的链接：

1. 首页主卡片或 Hero 区块。
2. Latest / Top Stories / World / Asia / Singapore / China / Business 列表。
3. 栏目页前两屏内的正文型文章卡片。

默认跳过以下链接：

1. Opinion / Comment / Editorial。
2. Live updates / Live blog。
3. Video、Podcast、Photo gallery。
4. Newsletter、Subscribe、Sign in。
5. Tag 页面、专题页、作者主页、列表分页页。

### 文章完整性判断

只有在下列条件至少满足大部分时，才把文章纳入最终结果：

- 标题明确
- 来源可识别
- 正文至少提取到数个实质段落
- 时间信息可见或可以从页面元数据获得
- 页面不是纯视频或纯图库

## 翻译与输出规则

中文翻译和 Word 编排时，严格遵循 `references/translation_docx_spec.md`。最低要求如下：

1. 保留原文标题和原文链接。
2. 生成中文标题、120 至 220 字中文摘要和中文正文。
3. 保留作者、时间、栏目和来源。
4. 对不确定信息保留原文中的不确定性表达。
5. 不得把摘要写成评论或观点稿。

## 默认输出字段

每篇文章至少产出以下字段：

| 字段 | 说明 |
|---|---|
| source_name | 来源媒体 |
| source_region | 来源地区 |
| section | 频道或栏目 |
| article_url | 原文链接 |
| title_original | 原始标题 |
| title_zh | 中文标题 |
| published_at | 发布时间 |
| author | 作者或机构 |
| language_original | 原文语言 |
| summary_zh | 中文摘要 |
| body_zh | 中文正文 |
| keywords_zh | 中文关键词 |
| extraction_note | 抓取备注或异常说明 |

## 质量门槛

始终满足以下要求：

1. **可追溯。** 每篇文章都必须保留来源和链接。
2. **可核查。** 不要补写未从页面获得的信息。
3. **可阅读。** 中文标题和摘要必须通顺，不要只做机械直译。
4. **可筛选。** 区分突发、政策、国际、财经、科技、社会等主题标签。
5. **可交付。** 最终结果必须能直接进入 Word 文档，而不是一堆无结构文本。

## 站点访问与限制处理

1. 遇到付费墙或登录墙时，记录为“受限页面”，然后换抓其他可访问稿件。
2. 遇到动态渲染正文时，优先使用浏览器正文视图；必要时回退到页面源码提取，但不要执行不受信任脚本。
3. 遇到首页重复卡片时，优先保留正文更完整、发布时间更清晰的版本。
4. 遇到纯快讯、正文极短的内容时，可纳入“快讯栏”，但不要冒充完整文章。

## 推荐默认配置

### 标准每日综合版

- 国际：BBC、Reuters、AP、Al Jazeera
- 新加坡：CNA、The Straits Times、联合早报
- 中国：新华网、人民网、央视网新闻、中国新闻网
- 每站建议抓取：2 至 5 篇高价值文章

### 中文优先版

- 国际：Reuters、BBC
- 新加坡：联合早报、CNA
- 中国：新华网、人民网、央视网新闻、中国新闻网、澎湃新闻
- 每站建议抓取：2 至 4 篇

### 财经增强调研版

- 国际：Reuters、Bloomberg、CNBC、Financial Times、Nikkei Asia
- 新加坡：The Business Times
- 中国：财新网、界面新闻、经济观察网
- 每站建议抓取：1 至 3 篇深度稿

## 最终交付格式

默认输出为以下三层之一：

1. **结构化中间稿**：适合后续程序转 DOCX。
2. **Word-ready Markdown**：直接套用模板文件。
3. **最终 DOCX**：当环境中已有可用的 DOCX 生成链路时再生成。

若用户没有明确要求格式，优先输出 Word-ready Markdown，并说明其已按 DOCX 结构编排。
