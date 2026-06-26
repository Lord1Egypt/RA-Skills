---
title: 新闻源目录
purpose: 为 OpenClaw 每日新闻抓取 subagent 提供可直接访问的主流站点首页与优先级建议。
---

# 新闻源目录

本目录面向“首页优先”的新闻抓取流程设计。默认做法不是直接跑全站搜索，而是**先进入站点首页或频道首页，再点击进入当日重点新闻链接**。这样更贴近编辑部值班流，也更适合生成“每日新闻简报”或“跨站对照版新闻汇编”。

使用本目录时，应优先覆盖 **国际主流媒体、 新加坡主流媒体、 中国内地主流媒体** 三个层级；如用户需要 Greater China 补充视角，再启用港媒补充源。对于存在登录墙、订阅墙或文本不完整的页面，应直接标记为“受限”，不要尝试绕过访问限制。

## 一、国际主流媒体

| 优先级 | 媒体 | 首页/频道 | 适用内容 | 使用提示 |
|---|---|---|---|---|
| Tier 1 | BBC News | https://www.bbc.com/news | 国际、世界、突发、解释性报道 | 从首页 Hero、Latest、World 卡片进入正文 |
| Tier 1 | Reuters | https://www.reuters.com/world/ | 硬新闻、外交、政策、财经 | 优先抓取 World、Asia Pacific、China 子频道 |
| Tier 1 | AP News | https://apnews.com/ | 国际、突发、区域新闻 | 适合作为线索交叉核验源 |
| Tier 1 | Al Jazeera | https://www.aljazeera.com/ | 中东、全球南方、国际政治 | 补足英美媒体视角之外的覆盖 |
| Tier 2 | CNN International | https://edition.cnn.com/ | 国际、突发、美国关联国际新闻 | 避免仅视频页，优先正文型文章 |
| Tier 2 | The Guardian | https://www.theguardian.com/international | 国际、解释、长文 | 区分新闻稿和 Opinion |
| Tier 2 | France 24 | https://www.france24.com/en/ | 欧洲、非洲、中东 | 适合作为区域补充源 |
| Tier 2 | DW | https://www.dw.com/en/top-stories/s-9097 | 欧洲、德国、地缘政治 | 优先 Top Stories 与 Asia |
| Tier 2 | Bloomberg | https://www.bloomberg.com/ | 全球商业、市场、宏观 | 注意部分文章存在订阅限制 |
| Tier 2 | CNBC World | https://www.cnbc.com/world/?region=world | 财经、市场、商业快讯 | 用于每日财经栏目补充 |
| Tier 2 | Nikkei Asia | https://asia.nikkei.com/ | 亚洲商业、产业、外交 | 适合亚洲企业与供应链新闻 |
| Tier 2 | NHK World | https://www3.nhk.or.jp/nhkworld/ | 日本、亚太、灾害、政府动态 | 对日本相关新闻非常有价值 |
| Tier 2 | AFP | https://www.afp.com/en/news | 国际快讯、全球线 | 可用作线索与标题交叉验证 |
| Tier 3 | Financial Times | https://www.ft.com/world | 国际商业、金融、地缘经济 | 订阅墙较多，抓可读页即可 |
| Tier 3 | The New York Times | https://www.nytimes.com/section/world | 世界新闻、解释报道 | 订阅墙较多，作为补充源 |
| Tier 3 | The Wall Street Journal | https://www.wsj.com/world | 世界、商业、地缘政治 | 订阅墙较多，作为补充源 |

## 二、新加坡主流媒体

| 优先级 | 媒体 | 首页/频道 | 适用内容 | 使用提示 |
|---|---|---|---|---|
| Tier 1 | CNA | https://www.channelnewsasia.com/ | 新加坡、东南亚、国际 | 作为新加坡新闻主抓源 |
| Tier 1 | The Straits Times | https://www.straitstimes.com/ | 新加坡、亚洲、国际、商业 | 首页与 Singapore 频道价值高 |
| Tier 1 | 联合早报 | https://www.zaobao.com/ | 新加坡、区域、国际、中文视角 | 适合作为中文源与双语对照源 |
| Tier 2 | TODAY | https://www.todayonline.com/ | 新加坡本地、政策、社会 | 可补足本地民生和政策新闻 |
| Tier 2 | The Business Times | https://www.businesstimes.com.sg/ | 新加坡财经、企业、市场 | 适合商业简报 |
| Tier 3 | Mothership | https://mothership.sg/ | 新加坡民生、热点、网生话题 | 只抓公共价值高的新闻 |
| Tier 3 | AsiaOne | https://www.asiaone.com/ | 新加坡、亚洲、热点整合 | 适合作为备选与线索补充 |

## 三、中国内地主流媒体

| 优先级 | 媒体 | 首页/频道 | 适用内容 | 使用提示 |
|---|---|---|---|---|
| Tier 1 | 新华网 | http://www.news.cn/ | 国内时政、国际要闻、权威发布 | 官方权威源，优先保留元数据 |
| Tier 1 | 人民网 | https://www.people.com.cn/ | 政治、社会、国际、评论背景 | 时政政策类新闻优先纳入 |
| Tier 1 | 央视网新闻 | https://news.cctv.com/ | 国内、国际、突发、直播报道 | 需避免纯视频页 |
| Tier 1 | 中国新闻网 | https://www.chinanews.com.cn/ | 国内、国际、综合快讯 | 抓取速度快，适合快讯流 |
| Tier 2 | China Daily | https://www.chinadaily.com.cn/ | 英文中国新闻、国际版表达 | 适合双语比对和对外叙事观察 |
| Tier 2 | 环球网 | https://www.huanqiu.com/ | 国际、地缘政治、快讯 | 需与其他源交叉验证 |
| Tier 2 | 澎湃新闻 | https://www.thepaper.cn/ | 深度、解释、时政、社会 | 适合补充背景段落 |
| Tier 2 | 财新网 | https://www.caixin.com/ | 财经、调查、商业 | 订阅限制常见，抓可读部分即可 |
| Tier 3 | 界面新闻 | https://www.jiemian.com/ | 财经、科技、公司 | 适合作为商业科技补充源 |
| Tier 3 | 经济观察网 | https://www.eeo.com.cn/ | 宏观、政策、商业 | 适合作为观察型补充源 |

## 四、Greater China 补充源

| 优先级 | 媒体 | 首页/频道 | 适用内容 | 使用提示 |
|---|---|---|---|---|
| Tier 2 | South China Morning Post | https://www.scmp.com/ | 中国、亚洲、国际 | 可作为英文桥接源，部分页面受限 |
| Tier 3 | 香港电台新闻 | https://news.rthk.hk/rthk/ch/ | 香港公共新闻、政府动态 | 作为港区公共广播补充源 |

## 五、推荐抓取组合

### 1. 标准版每日综合新闻

优先组合可设为：**BBC + Reuters + AP + CNA + 联合早报 + 新华网 + 人民网 + 央视网新闻 + 中国新闻网**。这一组合兼顾国际硬新闻、新加坡本地新闻、中国官方与综合快讯，适合生成每天早晚两版新闻汇编。

### 2. 国际重磅版

当用户更关注国际局势、战争、外交、地缘政治和全球市场时，可把 Reuters、BBC、AP、Al Jazeera、Bloomberg、Nikkei Asia 提升为主源，CNA 与联合早报作为亚洲和新加坡补充。

### 3. 中国与新加坡重点版

当用户更关心中文阅读与本地政策观察时，可把 新华网、人民网、央视网新闻、中国新闻网、联合早报、CNA、The Straits Times 设为核心组合。

## 六、首页点击策略摘要

抓取时应遵循以下顺序：先开首页，再抓主页主卡片与 latest 列表，再进入 world/asia/china/singapore/business 等频道页补足。对于导航、专题页、直播页、纯视频页、播客页、评论页和注册引导页，应默认降级或排除。若站点首页存在重复卡片，应优先保留正文最完整、发布时间最明确的页面。

## 七、与其他参考文件的关系

若需要机器可读清单，请读取 `source_manifest.yaml`。若需要中文翻译风格、字段规范与 Word 文档结构，请读取 `translation_docx_spec.md` 与模板文件 `../templates/daily_news_digest_template.md`。
