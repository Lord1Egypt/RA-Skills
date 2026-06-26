---
name: llm-daily-digest
description: 生成一份当日 LLM / 大模型领域的中文资讯简报。采集来源包括：**8 家头部厂商官方博客**（海外：OpenAI / Anthropic / Google DeepMind / Meta AI / xAI / Mistral；国内：DeepSeek / 通义千问 Qwen —— 最高优先级一手源）、GitHub Trending、arXiv（cs.CL / cs.AI / cs.LG / cs.CV）、Hugging Face、Papers With Code、Hacker News、X/Twitter、以及机器之心、量子位等中文媒体；覆盖四类内容：厂商官方发布、新开源项目、新论文、行业资讯/事件。只要用户说"跑一下今天的 AI 日报""生成大模型日报""今日大模型简报""总结一下今天 AI 动态""给我一份 LLM 快报""今天 AI 圈发生了啥""AI 圈今天有啥""看看今天大模型那边啥情况"，或被 cron 定时任务触发（触发消息中包含"日报""digest""brief"等关键字），都应使用此 skill。即使用户没说"日报"两个字，但表达出"整理今天 LLM 相关的项目/论文/新闻"意图的也应触发（例如"今天 HuggingFace 上有啥好东西""今天有什么 AI 新论文值得看""OpenAI / Anthropic / DeepSeek / Qwen 今天有啥新动态"）。产出是一份结构化 Markdown 文件，标题为 `🗣️ 今天 AI 圈发生了啥 · YYYY-MM-DD`，保存到 `~/.openclaw/workspace/digests/YYYY-MM-DD.md`，并在会话里附上文件路径和本日最值得看的 3 条精选。
---

# LLM 大模型每日简报 (llm-daily-digest)

这个 skill 让 OpenClaw agent 每天自动采集、筛选、汇总 LLM / 大模型领域的关键动态，产出一份**中文 Markdown 简报**。设计目标是"一份能让我在地铁上 5 分钟读完、又不漏掉当天真正重要的事"的日报。

## 核心工作流

按顺序执行以下步骤（其中步骤 2 的多个来源**可以并行**抓取，browser 工具支持多标签）：

1. **确定时间窗**：默认采集**过去 24 小时**的内容。如果用户说"这周""最近三天"则相应调整。把当前日期保存为 `TODAY`（格式 `YYYY-MM-DD`，时区 UTC+8 / 北京时间）。

2. **并行采集各来源**：按"来源清单"章节逐一抓取。遇到不可达的源（403、超时、Cloudflare 拦截等）记录一下但**跳过，不要中断整个流程**——宁可日报缺一个来源，也不要因为一个源挂掉就没日报。

3. **去重 & 筛选**：同一个项目/论文可能在多个源出现（比如 arXiv 一篇爆款论文同时上了 HN 和机器之心）。**合并成一条，保留最权威的原始链接**，但在备注里注明"也被 X / Y 报道"。筛选标准见下方"筛选与质量标准"。

4. **归类 & 重要度打分**：把所有条目归入 6 个分类（见"输出结构"），并为每条打一个内部重要度（高/中/低），用来决定要不要进"🔥 今日要闻"。

5. **写简报**：严格按"输出结构"章节的 Markdown 模板输出，中文撰写。每条 1-2 句话点到即止，不要复述原文——**这是简报不是翻译**。

6. **保存文件**：写到 `~/.openclaw/workspace/digests/<TODAY>.md`。如果当日文件已存在，追加 `-v2`、`-v3` 后缀，不要覆盖。

7. **回消息**：在当前 session 里回复用户三件事——
   - 简报文件路径
   - 本日 3 条精选（标题 + 一句话 + 链接）
   - 采集统计（共扫 N 个源，采到 M 条，归类后 K 条入选）

## 来源清单

下面每个来源都标注了 **URL**、**抓取方式**、**关注什么**、**跳过什么**。优先用 OpenClaw 的 `browser` 工具抓取渲染后的页面；静态 HTML 的源可以直接 `fetch`。

### 1. 头部厂商官方渠道（最高优先级 🏢）

这是**一手源**——头部厂商发布任何东西，简报都应该第一时间捕获。其他来源（HN、机器之心等）通常是这些官方发布的二次传播。**每天必查，哪怕没新东西也要确认一下是"今天确实没动静"而不是"漏了"**。

分为**海外头部**（6 家）和**国内头部**（2 家）两组。全部都是 Tier-1，每天都要轮询一遍。

#### 🌐 海外头部厂商

##### OpenAI

- **News**：https://openai.com/news/
- **Index（含 research、engineering、policy 帖）**：https://openai.com/index/
- **关注**：新模型发布（GPT-5、o 系列、Codex 等）、产品更新（ChatGPT / API / Sora / Operator 等）、research posts、safety & policy 公告。
- **筛选**：全收——OpenAI 发的内容基本没废话。仅跳过纯营销倒计时海报或纯招聘贴。

##### Anthropic

- **News**：https://www.anthropic.com/news
- **Research**：https://www.anthropic.com/research
- **关注**：Claude 新版本发布（当前 Claude Opus 4.7 属于 Claude 4.7 family）、产品功能（Claude Code、Claude for Excel/PowerPoint/Chrome、Cowork 等）、interpretability / alignment / safety research、policy 文章。
- **筛选**：全收。Research 板块的论文通常质量极高，即使没在 arXiv 被筛到也要独立收录。

##### Google DeepMind / Google AI

- **Google AI Blog**：https://blog.google/technology/ai/
- **Gemini 产品动态**：https://blog.google/products/gemini/
- **DeepMind Blog**：https://deepmind.google/discover/blog/
- **Google AI for Developers**：https://ai.google.dev/（文档更新和 Gemini API 变化）
- **关注**：Gemini 新版本发布（Pro / Flash / Ultra / Nano）、Gemini API 更新、DeepMind research（AlphaFold / AlphaProof / 视频生成 / 机器人等）、Google AI 产品集成。
- **筛选**：优先 deepmind.google 和 blog.google/technology/ai 的发布；blog.google/products/gemini/ 偏消费者向更新，除非是重大功能否则简报。
- **附加字段**：`subsidiary`（DeepMind / Google AI 二选一，同一家公司但品牌和定位不同）。

##### Meta AI

- **Blog**：https://ai.meta.com/blog/
- **Research**：https://ai.meta.com/research/publications/
- **关注**：Llama 新版本发布（Llama 4 系列及后续）、FAIR research、PyTorch / Segment Anything / V-JEPA 等工具和模型的更新、Meta AI 产品（助手、眼镜端侧模型等）。
- **筛选**：跳过纯营销广告贴（Meta AI 产品广告）；研究和开源发布全收。
- **特别说明**：Llama 是目前最重要的开源基模型家族，Meta 发布新 Llama 是行业级事件。

##### xAI

- **News**：https://x.ai/news
- **关注**：Grok 新版本发布（当前 4.x 系列，预期 Grok 5）、API 更新（Grok Imagine、Voice、Enterprise）、公司战略动态（融资、收购、数据中心）。
- **筛选**：Grok 模型更新和 API 发布全收；纯公司新闻（融资、人事）看是否是行业级事件——比如 xAI 被 SpaceX 收购这类就收，普通招聘启事跳过。
- **注意**：xAI 更新节奏快，有时新版本先在 grok.com / X 平台上线，news 页面才补上博客，简报当天 news 没看到不代表没发布，可以**辅助查 @xai / @elonmusk 的 X 推文**作为旁证。

##### Mistral AI

- **News**：https://mistral.ai/news
- **关注**：Mistral 新模型（Mistral Large / Medium / Small、Ministral、Mixtral、Codestral、Voxtral 等）、Le Chat 更新、企业版产品（Mistral AI Studio、OCR、Saba 等）、开源权重发布（Apache-2.0）。
- **筛选**：模型发布和技术博客全收；欧洲 AI 政策相关博文（他们偶尔会发）也收，属于行业观察角度。

#### 🇨🇳 国内头部厂商

##### DeepSeek

- **News**（主源，文章发在 API 文档站下）：https://api-docs.deepseek.com/news/
- **主站**：https://www.deepseek.com/ （首页的 banner 通常会挂最新模型发布）
- **关注**：模型发布（V3.x / V4 系列、R1 / R2 系列、Coder 系列、Math、VL、Janus 等）、Tech report（发到 HuggingFace 或仓库）、API 定价变更（DeepSeek 经常因发布新版降价一半以上，本身就是新闻）。
- **筛选**：全收——DeepSeek 发帖频率不高，每条都是重点。
- **注意**：DeepSeek 的技术报告常直接挂 HuggingFace 或 GitHub 而不是官网，所以需要**交叉查 https://huggingface.co/deepseek-ai 和 https://github.com/deepseek-ai** 看当天有没有新 push。

##### 通义千问 Qwen（阿里巴巴）

- **Blog**：https://qwenlm.github.io/blog/
- **GitHub 组织**：https://github.com/QwenLM （每个大版本都有独立仓库，README 顶部通常有最新更新日志）
- **HuggingFace**：https://huggingface.co/Qwen
- **关注**：Qwen 主线模型（当前 3.x 系列，3.6 已发、新子集持续放出）、专用模型（Qwen-Coder、Qwen-Math、Qwen-Image、Qwen-VL、Qwen-Omni、Qwen-TTS 等）、Qwen-Agent 框架、API（通过 Alibaba Cloud Model Studio）。
- **筛选**：全收。Qwen 家族非常大，小版本和量化版本可合并成一条（"Qwen3.6-35B-A3B 系列开源，含基础/指令/量化版本"），但新主线或新模态模型必须单独成条。
- **注意**：Qwen 有时发博客不同步 GitHub，或反之，**两边都要查**。

#### 厂商官方发布的处理原则

1. **不要错过**：每次运行都必须轮询上述 8 家的 news/blog 页面，检查是否有过去 24 小时内的新帖。
2. **直接进要闻**：任何一家的**新模型 / 新产品 / 新 API / 新论文** 一律算"高"，进 🔥 今日要闻候选池。公司新闻（融资、人事、合作）只有行业级事件才进要闻。
3. **描述要准，别抄营销文**：厂商官博往往有营销色彩，简报的一句话概括**要说清"发生了什么"而不是照抄营销语**。例如官方说 "Introducing GPT-5: Our most intelligent model yet."，简报应该写"OpenAI 发布 GPT-5，宣称在 XX 基准上较 GPT-4.5 提升 N%，上下文窗口扩至 X tokens"（具体数据以官博为准）。
4. **链回原文**：永远链到厂商官博原文，不要链到转载。
5. **通用产出字段**：`vendor`（OpenAI / Anthropic / Google / Meta / xAI / Mistral / DeepSeek / Qwen）、`title`、`published_date`、`type`（product / research / policy / safety / company）、`one_line_cn`、`link`。

### 2. GitHub Trending 🔗 https://github.com/trending

- **抓取**：分别拉 `?since=daily` 下的 All / Python / TypeScript / Jupyter Notebook 四种，避免只看一种语言漏掉东西。
- **关注**：repo 名、描述、今日新增 star 数、主语言、简短 README 摘要。
- **筛选关键词**（命中任一即入选）：`llm`、`gpt`、`agent`、`rag`、`multimodal`、`vlm`、`mllm`、`diffusion`、`transformer`、`fine-tun`、`inference`、`quantization`、`mcp`、`prompt`、`embedding`、`vector`、`finetune`、`distill`、`chat`、`claude`、`anthropic`、`openai`、`gemini`、`deepseek`、`qwen`、`llama`、`mistral`、`huggingface`、`ollama`、`vllm`、`sglang`。
- **跳过**：明显是 awesome-list 合集刷榜的；单纯 crypto / web3 工具；spec 类仓库被 AI 关键词命中但实际无关的。
- **产出字段**：`repo (owner/name)`、`stars_today`、`stars_total`、`language`、`one_line_cn`（一句中文概括）、`link`。

### 3. arXiv 新论文 🔗 https://arxiv.org/list/cs.CL/recent

- **抓取**：并行拉 4 个分类的 recent listing：`cs.CL`（自然语言）、`cs.AI`、`cs.LG`（机器学习）、`cs.CV`（计算机视觉，用于捕捉多模态相关）。
- **关注**：昨日/今日新投稿（状态为 `[new]` 而非 `[replaced]`）。
- **筛选**：
  - 标题或摘要包含 LLM / 多模态 / agent / RAG / reasoning / alignment / post-training / reinforcement learning from / inference / distillation / mixture of experts 等关键词。
  - 作者单位含 major labs 优先：OpenAI、Anthropic、Google DeepMind、Meta FAIR、Microsoft Research、DeepSeek、Qwen、Moonshot、智谱、百川、面壁、阶跃、MiniMax、Tsinghua NLP / THUDM、PKU、SJTU、HKUST、CMU、Stanford、MIT、Berkeley 等。
  - 每天大约选出 5-10 篇，**宁缺毋滥**。
- **产出字段**：`title`、`authors_short`（前 3 位 + 机构）、`one_line_cn`（中文摘要 1-2 句）、`arxiv_link`、`categories`。

### 4. Hugging Face 🔗 https://huggingface.co/models?sort=trending 和 https://huggingface.co/papers

- **抓取**：Models trending（日榜前 20）+ Papers 页（当日发布的）+ Datasets trending（可选，只在出现明显爆款时收录）。
- **关注**：新发布的基础模型、微调模型、新数据集、Daily Papers 列表里的高赞论文。
- **筛选**：跳过纯 fork/量化重传（名字里带 `-GGUF`、`-AWQ`、`-gptq` 但原模型已经在榜的）；优先收录带 model card 说明的首发模型。
- **产出字段**：`model/paper/dataset name`、`publisher`、`downloads_or_likes`、`one_line_cn`、`link`。

### 5. Papers With Code 🔗 https://paperswithcode.com/latest

- **抓取**：latest 页和按 task 的热门页（NLP、CV 任务）。
- **关注**：带开源代码的新论文，尤其 SOTA 更新。
- **产出字段**：`title`、`task`、`one_line_cn`、`pwc_link`、`code_link`。
- **注意**：这个站点和 arXiv、HF 有大量重叠，**强制去重**。

### 6. Hacker News 🔗 https://news.ycombinator.com/

- **抓取**：首页 + newest，找 AI/LLM 相关帖子。
- **关注**：点数 ≥ 80 且评论 ≥ 30 的"社区热议"；或者标题含 LLM/AI 关键词的新帖。
- **产出字段**：`title`、`points`、`comments`、`one_line_cn`（用帖子和评论区精华归纳出"为什么大家在讨论"）、`hn_link`、`source_link`（原链接）。
- **价值**：HN 适合捕捉"没上热搜但工程师都在聊"的技术讨论。

### 7. X/Twitter（可选，降级策略）

- **现实**：OpenClaw 的 browser 工具可能无法无痛访问 X（需要登录、JS 重度渲染）。**不要硬爬**。
- **降级方案**：
  - (a) 如果配置了 X API key，优先用 API 拉固定账号列表的最新推文（见下方账号名单）。
  - (b) 否则，用 web 搜索抓"昨天到今天"这些人的推文引用（搜 `site:nitter.net` 或从 google 搜索 `site:x.com @username`）。
  - (c) 实在拿不到，就跳过，在简报末尾的"数据覆盖"里注明"X 今日未采集"。
- **关注账号**：`@OpenAI`、`@AnthropicAI`、`@GoogleDeepMind`、`@Meta_AI`、`@deepseek_ai`、`@Alibaba_Qwen`、`@huggingface`、`@karpathy`、`@sama`、`@miramurati`、`@demishassabis`、`@jeremyphoward`、`@hardmaru`、`@_akhaliq`、`@rohanpaul_ai`、`@_philschmid`。

### 8. 机器之心 🔗 https://www.jiqizhixin.com/

- **抓取**：首页当日文章 + "最新" 频道。
- **关注**：国内外重大模型发布报道、深度技术解读、产业动态。
- **筛选**：跳过纯"某某融资 N 亿"类稿件，除非金额 > 10 亿美元或对行业格局有实质影响；跳过过度营销稿。
- **产出字段**：`title`、`author`、`publish_time`、`one_line_cn`（摘核心观点，不抄原文）、`link`。

### 9. 量子位 🔗 https://www.qbitai.com/

- **抓取**：首页当日文章。
- **关注**：偏技术落地、工程实践、国内厂商动态。
- **筛选**：同机器之心，跳过软文和过度营销。
- **产出字段**：同机器之心。

## 筛选与质量标准

采到的原始条目通常会有 100+，最终进入简报的应该 **25-40 条**（不含"要闻"重复）。把握以下几点：

1. **厂商官方发布优先**：上述 8 家头部厂商官博的任何新帖都直接进"🏢 厂商官方发布"对应的子分区；如果是**新模型 / 新产品 / 新 API** 类，还要进"🔥 今日要闻"头部。这些官博是最权威的一手源，哪怕只有一句发布公告也要收。
2. **优先原始源**：如果机器之心/量子位在转载 OpenAI 的发布，简报里链 OpenAI 官方博客原文，加备注"机器之心有中文报道"。
3. **去重要狠**：DeepSeek 发新模型，arXiv / HF / PwC / 机器之心 / HN / X 可能都在说。合并成一条。厂商官博发布和其他源的报道也要合并——原链接给厂商官博，正文提一句"HN 讨论 / 机器之心报道"。
4. **时效**：严格按 24 小时内；如果某条 48 小时前发布但今天才开始发酵（HN 热帖），可以收录并标注。
5. **反营销**：发布会预告、未发布的 demo 视频、纯观点稿，除非出自 OpenAI / Anthropic / Google / Meta / DeepSeek 这种重量级主体，否则不收。
6. **反水稿**：国内一些媒体会把同一个资讯改几个标题反复发，遇到相同主题的多篇稿件只保留信息量最大那篇。
7. **工程 vs 研究平衡**：尽量让 GitHub 新项目（工程向）和 arXiv 论文（研究向）都有一定比例，不要全是论文或全是工具。
8. **重要度打分**：
   - **高**：厂商官方新模型/新产品/新 API 发布、一线 lab 的重要研究、重大产品发布、行业格局事件（重大收购、关键人事变动）、technique 有明显 SOTA 突破。
   - **中**：厂商官方 research/policy 博文、开源项目 > 500 star 新增、研究有扎实 insight、有一定社区反响。
   - **低**：小幅改进、增量工作、仅有技术关注度但未产生讨论的。
   - 只有"高"和极少数特别有 insight 的"中"能进"🔥 今日要闻"；"低"可以直接扔掉。

9. **今日要闻跨源去重（重要！）**：一个事件常在多个来源同时出现——例如 Claude 新版发布可能同时被 Anthropic 官博、HN、arXiv、机器之心、量子位、X 多方报道。**在"🔥 今日要闻"里，同一事件最多占 1 个槽位**（链到最权威的一手源，正文一句话提"另有 X、Y、Z 报道"即可）。避免要闻 5 条里有 3 条都在讲同一件事的尴尬。判断"同一事件"以**核心主体 + 核心动作**为准（"Anthropic 发布 Opus 4.7" vs "Opus 4.7 在 SWE-bench 上刷新 SOTA" 算同一事件；"OpenAI 发 Agents SDK" vs "OpenAI 融资 $122B" 不算）。

## 输出结构

用这个模板输出 Markdown，**严格遵守 heading 结构**（方便后续做聚合 / RSS / 检索）。中文撰写，emoji 保留，链接用 Markdown 语法。

**空分区处理规则**（重要）：

- **🏢 厂商官方发布**：8 家**必须全部列出**，没内容写 "> 今日无新发布。" 留白——这是为了证明"查过了"而不是"漏了"，缺席本身就是信号。
- **📊 Papers With Code、🤗 Hugging Face Daily Papers**：这类聚合源经常被上游 arXiv / 厂商官博完全覆盖。如果今日所有能入选的条目都已在其他分区出现，**直接省略整节**，不要写"本期未单独入选"之类的占位文字——省略比留空壳更诚实、更清爽。
- **💬 社区热议**：HN 和 X 子分区任一有内容就保留整节；两个都无内容则整节省略。
- **🇨🇳 中文媒体精选**：今日无符合质量标准的内容时整节省略，不要硬凑。
- **📝 编者按**：没有可总结的趋势时省略。
- **🔥 今日要闻**：任何情况下都必须有，至少 1 条。如果真的啥也没有（极罕见），写"本期 AI 圈相对平静"并精简到 1-2 条次要亮点。

判断标准：**读者翻到这节能否得到比标题多的信息？能——保留；不能——省略**。

```markdown
# 🗣️ 今天 AI 圈发生了啥 · YYYY-MM-DD

> 数据窗口：YYYY-MM-DD HH:MM ~ YYYY-MM-DD HH:MM (UTC+8)
> 本期采集 N 个源 / M 条原始条目 / K 条入选

---

## 🔥 今日要闻

1. **<标题>** — 一到两句话说清"发生了什么"和"为什么重要"。[原始链接](url)
2. ...
3. ...

(3-5 条，超过 5 条说明没筛够狠，回去再砍。)

---

## 🏢 厂商官方发布

### 🌐 海外头部

#### OpenAI
- [**<标题>**](url) · YYYY-MM-DD · `product` / `research` / `policy` — 一到两句话说清核心内容。
- ...（若今日无则写 "> 今日无新发布。"）

#### Anthropic
- [**<标题>**](url) · YYYY-MM-DD · `product` / `research` — 一到两句话。

#### Google DeepMind / Google AI
- [**<标题>**](url) · YYYY-MM-DD · `DeepMind` / `Google AI` · `product` / `research` — 一到两句话。

#### Meta AI
- [**<标题>**](url) · YYYY-MM-DD · `Llama` / `FAIR` / `product` — 一到两句话。

#### xAI
- [**<标题>**](url) · YYYY-MM-DD · `Grok` / `API` / `company` — 一到两句话。

#### Mistral AI
- [**<标题>**](url) · YYYY-MM-DD · `model` / `product` — 一到两句话。

### 🇨🇳 国内头部

#### DeepSeek
- [**<标题>**](url) · YYYY-MM-DD · `model` / `tech-report` / `pricing` — 一到两句话。

#### 通义千问 Qwen
- [**<标题>**](url) · YYYY-MM-DD · `model` / `product` / `framework` — 一到两句话。

(这一节**每天都要有**，8 家都要列出。没内容的厂商写 "> 今日无新发布。" 保留结构，用来证明"确实查过了"而不是"漏了"。)

---

## 📦 GitHub 新项目 / 趋势

- [`owner/repo`](url) · ⭐ +today / total · `Python` — 一句话中文概括。
- ...

(按今日新增 star 数降序。)

---

## 📄 arXiv 新论文

- **<论文中文标题或英文原标题>** · `cs.CL` · 作者 et al. (机构) — 一到两句话摘要。[arXiv](url)
- ...

(5-10 篇，按相关度和重要度排序。)

---

## 🤗 Hugging Face

### 新模型
- [<model-id>](url) · 发布方 · ⬇️ N / ❤️ M — 一句话说明。

### Daily Papers 精选
- ...

---

## 📊 Papers With Code

- **<标题>** · 任务：`task-name` — 一句话。[论文](url) · [代码](url)
- ...

(跟 arXiv / HF 已覆盖的论文不重复。)

---

## 💬 社区热议

### Hacker News
- **<标题>** · ▲ points / 💬 comments — 为什么大家在讨论。[HN](hn-url) · [原链接](src-url)

### X / Twitter
- **@username**：引用或概括这条推文的核心信息。[链接](url)
- ...

**（传言/爆料必须单独隔离，放在 X 分区末尾）**：
- ⚠️ **未证实传言** · **@username**：内容概括——**需明确标注"未经官方证实"**。[链接](url)

传言判定标准：任何"内部人士爆料""预训练完成""x 天后发布""定价是 Y"等没有厂商官方博客同步印证的推文，都必须加 ⚠️ 前缀并放在传言小节。**宁可漏也不要让未证实信息混在正常条目里**——读者可能当成事实去决策，日报的可信度就崩了。

(如果 X 今日未采集，这个子章节写 "> 本期未采集到 X 内容。")

---

## 🇨🇳 中文媒体精选

- [**<标题>**](url) · 机器之心 — 核心观点一两句。
- [**<标题>**](url) · 量子位 — 核心观点一两句。
- ...

(每家 2-5 条，去除与前面章节重复的。)

---

## 📝 编者按

用 2-3 句话点出今日主题或趋势。例如"今天 DeepSeek 和 Qwen 都在推理优化上有新动作，开源社区对小模型 RL post-training 的热度持续上升"。**只有当确实有可总结的趋势时才写**，没有就省略这一节。

---

*本日报由 OpenClaw + llm-daily-digest skill 自动生成 · 仅供个人信息聚合使用，内容版权归原作者*
```

## 保存位置和命名

- **主文件**：`~/.openclaw/workspace/digests/YYYY-MM-DD.md`
- **同日重跑**：追加后缀 `-v2`、`-v3` 不覆盖。
- **目录不存在时**：先 `mkdir -p`。
- **索引**（可选功能）：生成完毕后更新 `~/.openclaw/workspace/digests/INDEX.md`，追加一行到开头 `- YYYY-MM-DD: [链接到今日文件] — 今日要闻第 1 条标题` 作为导航。

## Cron 定时任务配置（用户侧）

这个 skill 本身只是"怎么做"的说明，**"每天自动跑"这件事要在 OpenClaw 侧单独配置 cron job**。具体配置语法请以 OpenClaw 官方文档为准：

- 📖 https://docs.openclaw.ai/automation/cron-jobs
- 📖 https://docs.openclaw.ai/gateway/configuration

核心思路就是定一个调度，让它定时给 agent 发一条消息（比如 "跑一下今天的大模型日报"），agent 在读取该消息时会匹配到本 skill 的 description 从而触发执行。

关键配置点：

- **调度时间**：推荐 **北京时间早上 8-10 点**（cron 表达式如 `0 9 * * *`；注意 OpenClaw 的 cron 运行时区是否为系统本地时间或 UTC，需要相应换算）。避开 UTC 0:00 前后——国内媒体还没更新当日内容，arXiv 也刚换日期。
- **触发消息**：写 `跑一下今天的大模型日报` 或 `使用 llm-daily-digest skill 生成今日简报`，两者都能命中本 skill 的 description。
- **Session**：用 `main` session 即可（参见 OpenClaw 的 session 模型文档）。
- **失败重试**：如果 OpenClaw cron 支持失败重试策略，建议开启——某些源偶发 429 / 超时是常态。

配置完成后，可以先手动触发一次（直接给 agent 发测试消息）验证跑通，再让 cron 每日自动执行。

## 边界情况与故障处理

- **某来源被拦截（Cloudflare / 403）**：跳过并在简报最后"数据覆盖"里注明，不要让整个任务失败。
- **当日几乎没内容**（比如周末或节假日）：**不要硬凑**。可以输出一份精简版（3-5 条要闻 + 中文媒体摘要），在编者按里直接说"今日 AI 圈相对平静"。
- **重大事件日**（GPT/Claude/Gemini 新版发布、重大收购等）：适当扩大"今日要闻"到 6-8 条，并为该事件单独写一小段 200 字左右的背景梳理，加在"今日要闻"之后、分类列表之前。
- **arXiv 周末无新稿**：arXiv 周六周日不投稿，周一的日报会一次收到周末积压的论文，这是正常的，按日期分组展示即可。
- **同一模型多个版本发布**（Qwen-3-72B、Qwen-3-72B-Instruct、Qwen-3-72B-AWQ 同天放出）：合并成一条，说明"含基础 / 指令 / 量化版本"。
- **跨时区**：所有时间以北京时间为准；arXiv 的 EST 时间需要换算（EST 的"今天"可能对应北京时间"昨天+今天"）。

## 调用示例

**用户发起**：
> 跑一下今天的大模型日报

**Agent 行为**（简要）：
1. 读取本 SKILL.md，理解工作流
2. 并行用 browser 工具打开所有来源（8 家厂商官博 + GitHub + arXiv + HF + PwC + HN + X + 2 家中文媒体，共 14 个抓取入口）
3. 抓取 + 筛选 + 归类 + 打分
4. 写入 `~/.openclaw/workspace/digests/2026-04-17.md`
5. 回复用户：
   > ✅ 2026-04-17 日报已生成：`~/.openclaw/workspace/digests/2026-04-17.md`
   >
   > 今日 3 条精选：
   > 1. **Anthropic 发布 Claude Opus 4.7** — 推理与代码能力提升，Claude 4.7 family 首款旗舰（[链接]）
   > 2. **Qwen3.6-35B-A3B 开源** — 阿里巴巴 Qwen 团队发布最新混合专家模型（[链接]）
   > 3. **HuggingFace Trending：某 Agent 框架 24h +1.2k stars** — ...（[链接]）
   >
   > 本期采集 14 个入口 / 原始 142 条 / 入选 35 条。

## 可扩展方向

以下是可按需扩展的方向：

- **个性化**：基于用户过往标注的"感兴趣/不感兴趣"调整筛选权重
- **推送**：通过 OpenClaw 的 channels（Telegram/Slack/微信）把简报推送出去
- **周报 / 月报**：在每周日 / 每月末聚合生成周报月报
- **语音播报**：结合 OpenClaw 的 TTS 生成一份 5 分钟的播客版
- **更多厂商官方渠道**（Tier-2，按需扩展）：
  - 海外：Cohere、Stability AI、AI21、Together AI、Databricks / Mosaic、NVIDIA Research、Microsoft Research
  - 国内：智谱清言 / BigModel (zhipuai.cn)、Moonshot AI / Kimi、MiniMax、百川智能、阶跃星辰 StepFun、面壁智能 / ModelBest、商汤、昆仑万维
- **更多内容源**：Reddit r/LocalLLaMA、r/MachineLearning、AINews、Import AI、The Batch、Latent Space 博客等

---

*设计重点：可靠跑通 · 中文输出质量 · 易于人工审阅*
