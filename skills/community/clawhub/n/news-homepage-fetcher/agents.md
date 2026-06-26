# agents.md

## 总体设计

该 subagent 体系建议采用**一个总控代理 + 五个执行代理**的结构。这样设计的目的，不是为了炫耀多代理，而是把“选站点、点链接、抽正文、翻中文、出文档、做质检”这几种不同性质的工作分开，从而降低单代理在一个长链条任务中的失误率。

整个体系的主入口代理名称可设为 `daily-news-chief`。它负责解释用户请求、加载 `soul.md`、决定当次覆盖范围，并调度下游执行代理。其他代理不直接面向用户，而是面向 `daily-news-chief` 返回结构化中间结果。

## 代理列表

| Agent ID | 角色 | 主要职责 | 主要输入 | 主要输出 |
|---|---|---|---|---|
| `daily-news-chief` | 总控代理 | 理解任务、选新闻组合、分发任务、合并结果、控制质量 | 用户任务、时间窗口、覆盖范围 | 最终日报、失败清单、运行摘要 |
| `homepage-link-scanner` | 首页扫描代理 | 打开首页与频道页，筛选值得进入的正文链接 | 站点列表、频道优先级 | 候选文章链接池 |
| `article-body-extractor` | 正文提取代理 | 进入文章页，提取标题、时间、作者、正文与元数据 | 候选链接池 | 标准化文章对象 |
| `zh-translation-editor` | 中文翻译代理 | 生成中文标题、摘要、全文译文与关键词 | 标准化文章对象 | 中文文章对象 |
| `digest-assembler` | 文档组装代理 | 按模板将文章编排为日报或 Word-ready 文稿 | 中文文章对象、模板 | 每日新闻汇编稿 |
| `quality-gate-reviewer` | 质量审校代理 | 检查重复、缺字段、误译、来源缺失与格式异常 | 汇编稿、文章对象 | 质检后的最终稿与问题单 |

## 每个代理的工作说明

### 1. `daily-news-chief`

这是唯一需要直接理解用户意图的代理。它负责把用户请求映射为一次具体的日报任务，例如“抓取过去 24 小时 BBC、CNA、新华网和联合早报首页重点新闻，各站 3 篇，输出中文 Word 文档”。

它的关键职责有三项。第一，决定新闻源组合和每站抓取篇数。第二，决定栏目结构，例如国际、新加坡、中国、财经。第三，在最终交付前，检查是否已经保留了所有来源链接与异常说明。

### 2. `homepage-link-scanner`

这个代理只做一件事：**从首页和核心频道页里找到值得进一步点击的正文链接**。它不负责翻译，不负责写摘要，也不负责最终成文。它必须排除评论页、直播页、视频页、标签页、订阅页和作者页。

它输出的对象至少应包含：`source_name`、`homepage_url`、`article_url`、`section_guess`、`headline_preview`、`priority_score` 和 `selection_reason`。

### 3. `article-body-extractor`

这个代理负责进入文章正文页，并完成结构化提取。它必须尽量提取原始标题、发布时间、作者、正文段落、栏目、图片说明和原始链接。若正文抽取失败，应清楚记录失败类型，而不是返回空对象。

它的输出对象建议遵循如下字段：

```json
{
  "source_name": "BBC News",
  "source_region": "International",
  "section": "World",
  "article_url": "https://...",
  "title_original": "...",
  "published_at": "2026-04-16T08:30:00+00:00",
  "author": "...",
  "language_original": "en",
  "body_original": "...",
  "extraction_note": "complete | partial | paywalled | dynamic-load-failed"
}
```

### 4. `zh-translation-editor`

这个代理负责将结构化文章对象转为中文可交付对象。它必须严格遵守“忠实翻译、克制措辞、保留不确定性”的原则，不得自行加入评论。对于中文原文，它只负责生成规范化摘要与关键词，不做重复翻译。

它的输出对象至少增加以下字段：`title_zh`、`summary_zh`、`body_zh`、`keywords_zh`、`topic_label`。

### 5. `digest-assembler`

这个代理负责把多篇中文文章对象按模板整理成日报。它应当支持至少三种输出模式：

1. Word-ready Markdown；
2. 结构化 JSON；
3. 最终 DOCX 所需的中间稿。

它必须能够按栏目自动排序，并在附录中输出来源表和失败清单。

### 6. `quality-gate-reviewer`

这个代理是最后一道门。它要检查四类问题：

1. 来源是否缺失；
2. 中文标题和摘要是否明显失真；
3. 是否有重复稿、空正文、无时间文章混入；
4. Word-ready 格式是否可直接转入文档。

它可以打回上游代理重新抓取个别页面，但不能自己补造缺失正文。

## 编排流程

标准编排顺序如下：

```text
daily-news-chief
  -> homepage-link-scanner
  -> article-body-extractor
  -> zh-translation-editor
  -> digest-assembler
  -> quality-gate-reviewer
  -> daily-news-chief final delivery
```

若用户只要求“今日国际新闻快览”，则 `daily-news-chief` 可以缩短流程，只抓国际源并减少每站篇数。但无论任务大小，`quality-gate-reviewer` 都不应被跳过。

## 任务分发策略

### 标准日报

当用户请求“每日新闻”时，建议默认分发如下：

| 栏目 | 主抓代理输入 | 建议站点 |
|---|---|---|
| 国际 | 4 至 6 个国际源 | BBC、Reuters、AP、Al Jazeera |
| 新加坡 | 2 至 4 个新加坡源 | CNA、The Straits Times、联合早报 |
| 中国 | 3 至 5 个中国源 | 新华网、人民网、央视网新闻、中国新闻网 |
| 财经 | 2 至 4 个财经源 | Bloomberg、CNBC、财新网、Nikkei Asia |

### 单区域专报

当用户请求“新加坡新闻日报”或“中国新闻日报”时，应让 `daily-news-chief` 缩小范围，并允许 `homepage-link-scanner` 深入本地区频道页，而不是分散精力抓全局。

## 代理间的中间对象约束

所有代理之间应传递结构化对象，而不是大段自由文本。最小中间对象结构建议如下：

```json
{
  "run_id": "daily-2026-04-16-am",
  "source_name": "CNA",
  "source_region": "Singapore",
  "article_url": "https://...",
  "title_original": "...",
  "title_zh": "...",
  "published_at": "...",
  "summary_zh": "...",
  "body_zh": "...",
  "keywords_zh": ["...", "..."],
  "status": "ok"
}
```

## 错误处理协议

若某篇文章失败，执行代理不应中断整批任务，而应返回失败对象。失败对象至少包括：`article_url`、`source_name`、`failure_type`、`failure_note`。常见 `failure_type` 可定义为：`paywall`、`login_required`、`dynamic_load_failed`、`body_missing`、`duplicate`、`non_article_page`。

## 终态要求

只有当以下条件全部满足时，`daily-news-chief` 才能宣布任务完成：

1. 已形成完整日报目录；
2. 每篇入选文章都带来源与链接；
3. 所有失败项都已登记；
4. 中文摘要与正文通过质检；
5. 输出可直接进入 Word 生成链路。
