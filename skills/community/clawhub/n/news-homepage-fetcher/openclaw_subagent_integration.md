# OpenClaw 新闻抓取 Subagent 集成说明

## 一、目标

本套文档的目标，是为 OpenClaw 提供一个可直接落地的“每日新闻抓取 subagent”设计框架，使其能够从主流新闻网站首页进入正文，提取内容并翻译成中文，最后生成可进入 Word 的日报文档。

这不是一个单独的爬虫脚本，而是一套由**身份定义、代理分工、技能说明、新闻源目录、翻译与文档规范、输出模板**共同组成的运行约束。

## 二、建议文件装配方式

建议将本套文件按下列方式接入 OpenClaw：

| 文件 | 角色 | 建议接入位置 |
|---|---|---|
| `soul.md` | subagent 核心人格与目标 | 作为该 subagent 的系统级身份说明 |
| `agents.md` | 多代理分工与编排规则 | 作为 orchestrator 的代理编排文档 |
| `skills/openclaw-news-homepage-fetcher/SKILL.md` | 抓取技能主说明 | 作为新闻抓取执行技能 |
| `skills/openclaw-news-homepage-fetcher/references/source_catalog.md` | 新闻源清单 | 供执行前选站点时读取 |
| `skills/openclaw-news-homepage-fetcher/references/source_manifest.yaml` | 机器可读源表 | 供程序化任务配置加载 |
| `skills/openclaw-news-homepage-fetcher/references/translation_docx_spec.md` | 中文翻译与 Word 规范 | 供翻译与文档生成阶段读取 |
| `skills/openclaw-news-homepage-fetcher/templates/daily_news_digest_template.md` | 日报模板 | 供 Word-ready Markdown 或 DOCX 中间稿复用 |

## 三、建议运行链路

推荐把执行链路固定为以下顺序：

1. 加载 `soul.md`，确定 subagent 的目标与边界。
2. 加载 `agents.md`，确定是否启用多代理编排。
3. 由总控代理读取 `SKILL.md`。
4. 按需读取 `source_catalog.md` 或 `source_manifest.yaml` 选择新闻源。
5. 抓取首页、进入正文、提取全文。
6. 读取 `translation_docx_spec.md` 生成中文摘要和中文正文。
7. 套用 `daily_news_digest_template.md` 输出 Word-ready 文稿。

## 四、推荐默认模式

### 1. 标准日报模式

适用于“抓取今天主流国际、新加坡、中国新闻，并翻译成中文文档”。建议输出 12 至 24 篇文章，按国际、新加坡、中国、财经四栏组织。

### 2. 新加坡专报模式

适用于“每天抓新加坡新闻”。建议重点使用 CNA、The Straits Times、联合早报、TODAY、Business Times。

### 3. 国际重磅模式

适用于“每天只抓国际要闻和全球市场”。建议重点使用 Reuters、BBC、AP、Al Jazeera、Bloomberg、Nikkei Asia。

### 4. 中文优先模式

适用于“更重视中文可读性与国内外中文源”。建议重点使用 联合早报、新华网、人民网、央视网新闻、中国新闻网、澎湃新闻。

## 五、建议的用户任务模板

以下任务模板可直接交给 OpenClaw：

> 请运行每日新闻 subagent，从 BBC、Reuters、CNA、联合早报、新华网和人民网首页抓取当日重点新闻，每站 3 篇，提取正文并翻译为中文，生成一份按“国际 / 新加坡 / 中国”分栏的 Word 文档。

> 请运行新加坡新闻专报 subagent，从 CNA、The Straits Times、TODAY、联合早报首页抓取过去 24 小时的重要新闻，提取正文并翻译成中文，输出 Word-ready Markdown 和 DOCX。

> 请运行国际重磅版 subagent，从 Reuters、BBC、AP、Al Jazeera、Bloomberg 首页抓取头条与 world 栏目重点新闻，筛掉 opinion 和 live blog，翻译成中文并输出日报。

## 六、为什么这样设计

该设计把“站点导航”“正文抽取”“中文翻译”“日报组装”“质量审校”拆成了不同层次，因此比把所有要求塞进一个超长提示词更稳定。与此同时，新闻源目录与翻译规范被拆到参考文件中，避免 `SKILL.md` 过长，也更容易维护。

## 七、后续可扩展方向

如果后续要把该 subagent 进一步产品化，最值得增加的不是更多媒体，而是以下能力：定时任务调度、重复新闻聚类、同题多源对照、自动 DOCX 生成脚本、失败重试机制、栏目热度评分和历史归档。
