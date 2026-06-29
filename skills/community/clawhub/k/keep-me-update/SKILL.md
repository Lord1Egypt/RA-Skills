---
name: keep-me-update
description: "Daily tech/AI/geek news digest powered by RSS + web search. 基于 RSS 和网络搜索的每日科技/AI/极客新闻摘要。触发后先交互配置，再自动生成。"
version: 1.0.0
author: Nemocccc
license: MIT
metadata:
  hermes:
    tags: [news, daily-digest, rss, tech, ai]
    homepage: https://github.com/Nemocccc/KeepMeUpdate
---

# KeepMeUpdate — 每日科技新闻摘要 / Daily Tech Digest

## 理念 / Why This Skill

每天从 RSS 源 + 网络搜索双渠道获取最新科技/AI/极客新闻，经筛选编排后生成「导读 + 链接」风格的摘要。

> 不依赖固定的配置文件，首次使用通过问答引导用户完成配置，配置存储在本地 `user_config.yaml`，后续自动复用。

### 触发场景

> "今天有啥新鲜事" / "keep me updated" / "最近科技圈发生了什么" / "latest tech news" / "what's new in AI"

---

## 工作流程

### Step 0: 配置交互

**持久化方案**：用户配置写入 `{skill_dir}/user_config.yaml`，不依赖 agent 上下文和 memory。

> 关于交互配置模式的设计思路和复用方法，参见 `references/config-flow.md`。

```yaml
# user_config.yaml 示例
language: zh
timezone: Asia/Shanghai
output_mode: terminal
output_dir: ~/DailyENews/
retention_days: 7
arxiv_retry: true
```

> 注意：`feeds_path` 不存储在配置中——脚本硬编码读取 `{skill_dir}/scripts/rss_feeds.json`，首次使用需复制 `rss_feeds.default.json`。

首次触发时，agent 按如下顺序依次询问用户。已有完整配置则跳过此步骤，直接进入 Step 1。

#### 问询 1：语言

先尝试通过以下方式获取默认语言（按优先级）：
1. 终端 `locale` 命令输出中的 `LANG=zh_CN` / `LANG=en_US`
2. Hermes 配置语言（如有）
3. **以上都拿不到则询问用户**

**问题**："你要中文还是 English？(zh/en)"

#### 问询 2：时区

先尝试读取系统时区：
- macOS: `readlink /etc/localtime` 或 `systemsetup -gettimezone`
- Linux: `timedatectl show --value -p Timezone` 或 `/etc/timezone`
- **拿不到则询问用户**

**问题**："你在哪个时区？(如 Asia/Shanghai, America/New_York, Europe/London)"

#### 问询 3：输出方式

**问题**："摘要怎么给你？"
- **终端输出 (terminal)** — 直接打印到 stdout。简单直接，适合 cron 转发到 Telegram/邮件/Slack。
- **本地文件 (file)** — 写入 Markdown 文件。需要确认路径（默认 `~/DailyENews/`）。

如选 file，补问路径。按用户回答设置 `output_dir`。

#### 问询 4：RSS 源

**问题**："用我内置的源列表，还是你有自己的源要加？"

- **内置源 (default)** — 直接使用 `scripts/rss_feeds.default.json`，包含 28 个高质量科技源（HN、TechCrunch、Ars Technica、36氪、IT之家、GitHub Trending、arXiv 等）。内置源分中英文两组，根据 language 自动选择。
- **用户自备源 (custom)** — 用户逐个提供 RSS URL，agent 验证（`curl -sL -o /dev/null -w "%{http_code}"` 检查 HTTP 状态码 + 确认返回 XML/RSS 格式）后加入 `user_config.yaml`。
- **上网找源 (search)** — agent 搜索 "best tech RSS feeds 2026" 等，列出热门源供用户勾选确认。

**高级选项（可选询问）**：
- 是否启用 arXiv 二次重试（默认开启）
- 文件保留天数（默认 7 天，仅 file 模式有效）

配置写入后立即生效。后续触发时 agent 先读取 `user_config.yaml`，缺字段才补问。

---

### Step 1: 获取 RSS 文章

```bash
python3 {skill_dir}/scripts/rss_fetch.py
```

> ⚠️ **首次使用前**：确保 `{skill_dir}/scripts/rss_feeds.json` 存在。默认源文件名为 `rss_feeds.default.json`，首次运行需复制一份：
> ```bash
> cp {skill_dir}/scripts/rss_feeds.default.json {skill_dir}/scripts/rss_feeds.json
> ```
> 脚本硬编码读取 `rss_feeds.json`（而非 `rss_feeds.default.json`），`user_config.yaml` 中的 `feeds_path` 字段仅作记录，不被脚本读取。

输出 JSON 到 stdout，包含 `cache_file` 路径和 `total_articles`。读取缓存文件获取完整文章列表。

> **注意**: stderr 输出进度日志。JSON 在 stdout。如因控制字符解析失败，用 Python 直接 `open(cache_file)` 读取。
>
> ⚠️ **URL 可能已过时**：缓存中的 URL 路径可能在发布后发生变化（slug 被编辑、站点迁移、文章下架）。Ars Technica、DeepMind、TechCrunch 等源尤其常见。Step 5 生成导读时应基于 RSS 的 `title` 和 `summary` 字段，不要依赖 URL 中的文字来推断新闻内容。Step 6.5 会做全量 HTTP 验证捕获失效链接。

> **arXiv 延迟**: arXiv cs.AI 源首次抓取常返回 `count: 0`，同天稍后重试会正常。如 `arxiv_retry: true` 且 `total_articles` < 50，建议重新拉取一次（脚本会自动跳过已读文章，通过 `seen_guids.json` 跟踪）。

#### 空结果处理

如果 RSS 返回 `total_articles = 0` 或非常少（< 5）：
1. **不要终止流程**。仍继续执行 Step 2（web search 补充 + --fetch 兜底）。即使所有 RSS 源同时挂了，web search 和直接抓取仍可能找到今日新闻。
2. 记录 `rss_empty = true` 供后续步骤知晓 RSS 池为空。
3. 如果 **Step 1 + Step 2 合并后可用的新闻总数为 0**（RSS 空 + web search 空 + --fetch 也空），告知用户：「今天各数据源均未返回新内容，请稍后再试。」并终止执行。

> 因此，即使 RSS 无数据，仍必须执行 web search 兜底。Step 5.5 的链接验证池会仅包含 web search 结果。

---

### Step 2: 搜索补充新闻

运行 `web_search`，至少搜 3 组不同角度。根据 config 的 language 字段选择搜索词语言：

**中文模式**（language=zh）：
```
"AI 人工智能 大模型 最新 2026"
"科技 数码 硬件 芯片 手机 新能源 汽车 评测"
"开源 GitHub 编程 开发者工具 框架 语言"
"互联网 科技公司 融资 IPO 财报 收购"
"网络安全 数据隐私 漏洞 攻击"
"机器人 具身智能 自动驾驶 航天 卫星"
```

**英文模式**（language=en）：
```
"latest AI news today 2026"
"tech hardware gadgets chip smartphone EV"
"open source developer tools programming language framework"
"cybersecurity data breach vulnerability zero day"
"startup funding IPO acquisition tech companies"
"robotics autonomous driving space launch satellite"
"cloud computing infrastructure devops kubernetes"
```

#### DDG 限流时的兜底方案

如果 `web_search` 搜索返回空（DDG 被限流），切换到直接抓取知名新闻源首页：

```bash
# Hacker News 首页（开发者社区最热）
python3 {skill_dir}/scripts/search_web_stdlib.py "https://news.ycombinator.com" --fetch

# TechCrunch 首页（创业/科技商业）
python3 {skill_dir}/scripts/search_web_stdlib.py "https://techcrunch.com" --fetch

# Ars Technica 首页（深度科技）
python3 {skill_dir}/scripts/search_web_stdlib.py "https://arstechnica.com" --fetch

# The Verge 首页（消费电子/科技文化）
python3 {skill_dir}/scripts/search_web_stdlib.py "https://www.theverge.com" --fetch

# Wired 首页（科技文化/趋势）
python3 {skill_dir}/scripts/search_web_stdlib.py "https://www.wired.com" --fetch
```

> 提取技巧：HN 内容格式为 `序号. 标题 ( 域名 )` + `分数 points by 用户 时间 ago`，可用正则提取。TechCrunch 和 Ars 为文章标题列表。各源 --fetch 一次即可获取完整首页内容，比反复试搜索词更高效。
>
> ⚠️ **重要：HN --fetch 不输出 URL**。`search_web_stdlib.py --fetch` 提取的 HN 首页内容仅包含标题、域名、分数和评论数，**不包含每条故事的实际链接**（无论是 original URL 还是 HN 讨论页 URL）。因此从 HN --fetch 得到的标题不能直接使用——必须到 RSS 缓存或 web 搜索结果中交叉查找验证过的 URL。见 Step 3 的详细规则。

---

### Step 3: 合并去重 —— 链接保真规则 🚨

**这是本技能最重要的质量关卡。**

1. 合并 RSS 文章 + web 搜索结果到统一池
2. 按 URL 去重（同一 URL 只保留一条；标题相似但 URL 不同的保留两条）
3. 按发布时间排序（最新的优先）
4. 剔除不相关内容（广告、纯电商、纯娱乐八卦）

**链接保真规则**：

> **每条新闻的原文链接必须使用 RSS 或 web_search 返回的原始 URL。不得猜测、不得替换、不得凭记忆编写。**

- 如果 RSS 返回的 URL 是 `https://news.ycombinator.com/item?id=12345`（HN 讨论页），链接就用这个。不要替换成所谓「原文」。
- 如果 RSS 返回的 URL 是 `https://techcrunch.com/...`，链接就用 TechCrunch。不要替换成公司官网。
- web_search 返回的 URL 如有 `uddg=` 参数，解析出真实 URL 再使用。
- **绝对不要**根据标题自己拼 URL 或凭记忆写一个。

**🚨 关键陷阱：非 HN 聚合源的 URL 同样可能不准确**

Lobsters、Linux Reddit 等聚合源的 RSS 返回的 URL 通常是**原始文章链接**（Patreon、OMG Ubuntu、个人博客等），而非聚合站本身的讨论页。**不得**将 `来源` 字段标注为聚合源名称——必须标注 URL 实际指向的网站域名。

例如：
- Lobsters RSS 返回 `https://www.omgubuntu.co.uk/2026/06/audacity-4-0-beta` → 来源写 `OMG Ubuntu`，不能写 `Lobsters`
- Linux Reddit RSS 返回 `https://github.com/...` → 来源写 `GitHub`，不能写 `Reddit`

处理方式同 HN --fetch 规则：从 RSS 缓存中按标题 keywords 提取真实 URL，或 web_search 搜索。都无法验证则放弃。

**🚨 关键陷阱：HN --fetch 无 URL 问题**

`search_web_stdlib.py --fetch` 抓取 HN 首页时，返回的内容中每条故事只有标题、域名和分数——**没有可点击的 URL**。这常引诱 agent 凭标题猜测 URL（如生成虚构的 `news.ycombinator.com/item?id=XXXXXXXX`）。

**正确的处理流程**：
1. 将 HN --fetch 中感兴趣的标题作为搜索线索
2. 在 RSS 缓存文件（`articles_YYYY-MM-DD.json`）中按标题关键词搜索，提取 RSS 返回的真实 URL
3. 如果 RSS 中没有匹配，用 web_search 搜索该标题找到真实 URL
4. **如果以上两种方式都无法验证 URL，则放弃这条新闻**。宁可漏不可假

**自检方法（写入文件前必须执行）**：
```python
# 检查是否有虚构链接残留
import re
content = open(filepath).read()
fake_patterns = ['item?id=48571526', 'item?id=12345678', '12345678', '23456789']
for p in fake_patterns:
    if p in content:
        raise ValueError(f"FAKE URL DETECTED: {p} — STOP. Do not write file.")
```

> 🔑 **核心原则**：链接就是信任。一条没有可验证 URL 的新闻，比一条有假 URL 的新闻好一百倍。宁可漏掉一条好新闻，也不要让读者点进一个不相干的页面。

---

### Step 4: 分类编排

按内容分配到 5 个板块。判断依据（按优先级从上到下）：

| 板块 | 图标 | 判断逻辑 |
|------|------|---------|
| 今日头条 / Top Headlines | 🔥 | 影响面广、跨领域。来源权重高（TechCrunch/Ars/HN首页/36氪头条）且标题无明显分类倾向 |
| AI 前沿 / AI & Models | 🤖 | 标题含 AI/模型/智能/LLM/Agent/机器人；来源为 arXiv/DeepMind/Nature AI |
| 极客开源 / OSS & Dev | ⚡ | 标题含 开源/GitHub/编程/框架/库/工具；来源为 GitHub Blog/Mozilla/Cloudflare |
| 科技公司 / Companies | 🏢 | 标题含 融资/收购/上市/财报/股价/IPO |
| 硬件消费电子 / Hardware | 📱 | 标题含 芯片/手机/iPhone/Mac/GPU/CPU/显示器/硬件 |

> 分类技巧：同一篇文章匹配多个分类时，按表从上到下优先级判断。AI 芯片归 AI 前沿而非硬件。

**各板块建议条数**：总计 15-25 条，按当日热度动态分配。

---

### Step 5: 生成导读

每条新闻写 **1-2 句导读**。风格（按配置语言）：

**中文示例**：
```
Anthropic 发布 Claude Fable 5，首款公众可用的 Mythos 级模型。
华为 HDC 开幕，大会议程涉及「全新 UI design kit」，基本确认鸿蒙 7。
```

**英文示例**：
```
Anthropic launches Claude Fable 5, the first publicly accessible Mythos-tier model.
Huawei HDC kicks off with a 'new UI design kit' session, basically confirming HarmonyOS 7.
```

要点：为什么值得关注 + 核心信息。不要超过两句话。

---

### Step 5.5: 链接来源验证（防幻觉）

**程序化验证**——不是建议，必须执行。在 Step 5 生成导读后、Step 6 写入前执行。

**原理**：收集 Step 1（RSS 缓存）和 Step 2（web search / --fetch）中所有出现过的真实 URL 构建来源池，检查每条待发表新闻的 URL 是否在池中。不在池中 = 可能是 agent 凭空生成的幻觉链接。

```python
source_urls = set()
for a in rss_articles: source_urls.add(a['url'])
for e in websearch_results: source_urls.add(e['url'])   # uddg= 已解析
for f in fetch_results: source_urls.add(f['url'])

for item in selected_articles[:]:  # 遍历副本以便删除
    url = item['url']
    if url in source_urls:
        continue
    # 不在来源池——尝试按标题关键词模糊匹配
    keywords = item['title'].split()[:4]
    matched = [su for su in source_urls if any(k in su for k in keywords)]
    if matched:
        item['url'] = matched[0]
    else:
        selected_articles.remove(item)  # 宁缺毋滥
```

> 此验证自动覆盖：编造 HN 讨论页 URL、混淆文章标题和链接、Lobsters 短链接错误展开等所有场景。无需额外规则。

---

### Step 6: 写入/输出

根据 `user_config.yaml` 中的 `output_mode`：

**terminal 模式**：直接打印到 stdout。按模板格式输出完整内容。

> 模板文件位于 `{skill_dir}/templates/report.{language}.md`，包含以下占位符，agent 写入前必须全部替换：
> - `{datetime}` — 当前日期时间，含时区（如 2026-06-16 09:45 CST）
> - `{total_articles}` — RSS 新增文章总数
> - `{rss_ok}` — 成功抓取的 RSS 源数
> - `{rss_total}` — 总 RSS 源数
> - `{date_info}` — 日期信息描述
> - `{headlines}` / `{ai_news}` / `{oss_news}` / `{biz_news}` / `{hardware_news}` — 各板块新闻列表
> - `{selected_count}` — 最终收录的文章数
> - `{extra_sources}` — 额外数据源描述（如 "HN/TC/Ars --fetch"）
>
> 每板块内的新闻条目格式：
> ```markdown
> ### {序号}. {标题}
>
> {1-2 句导读}
>
> > 来源: {来源名} · [原文链接]({URL})
> ```

**file 模式**：
```python
import os, json, subprocess
from datetime import datetime, timezone, timedelta

# 1. 用 tz_offset.py 获取准确时区偏移
result = subprocess.run(
    ['python3', '{skill_dir}/scripts/tz_offset.py', config.timezone],
    capture_output=True, text=True, timeout=10
)
tz_info = json.loads(result.stdout)
offset_hours = tz_info['offset_hours']

# 2. 计算本地时间
tz = timezone(timedelta(hours=offset_hours))
now = datetime.now(tz)
date_str = now.strftime('%Y-%m-%d')
time_str = now.strftime('%H%M')

# 3. 写入文件
base = os.path.expanduser(config.output_dir)
daily_dir = os.path.join(base, date_str)
os.makedirs(daily_dir, exist_ok=True)

filepath = os.path.join(daily_dir, f"KeepMeUpdate-{time_str}.md")
try:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已写入: {filepath}")
except (OSError, PermissionError) as e:
    # 4. 降级到 terminal 模式
    print(f"⚠️ 文件写入失败 ({e})，降级到终端输出：")
    print(content)
```

> 时区偏移量通过 `tz_offset.py` 脚本计算，支持任意 IANA 时区名。如果文件写入失败（无权限、磁盘满等），自动降级到 terminal 模式并提示用户。

---

### Step 6.5: 写入后全量验证（200-or-die）

写入文件后，**必须对每条链接执行 HTTP GET 验证**，确认可达。这是防链接失真的最后一道物理防线。

优先使用可复用的验证脚本（比内联代码更健壮，不会被跳过）：

```bash
python3 {skill_dir}/scripts/verify_links.py <filepath>
```

脚本功能：
- 提取文件中所有 URL 并逐个发 GET 请求
- **已知付费墙域名**（bloomberg.com, reuters.com, ft.com, wsj.com 等）的 401/403 视为预期行为，警告但不阻断
- 检测重复 URL（不同条目共用同一链接）
- 非 200 且非付费墙的链接判定为断裂，退出码非零
- 内建站点超时差异化（github/arxiv/patreon 给 15s，其余 10s）

> ⚠️ **常见失败模式**：RSS 缓存的 URL 可能因 slug 变更、站点迁移或文章下架而 404。验证失败的链接必须回 RSS 缓存跨源匹配正确 URL（同一标题可能在另一个 feed 中有不同路径），无法匹配则移除整条新闻。
>
> 触发 `raise` 后流程立即中止，必须先修复或移除断裂链接后重新验证。不得在验证失败的情况下交付摘要。

---

### Step 7: 标记 RSS 已读

脚本使用 `{skill_dir}/scripts/seen_guids.json` 自动跟踪已读文章。**无需额外操作**——每次 `rss_fetch.py` 运行时，已抓取过的文章 GUID 会被记录，下次自动跳过。

> 如果需要**强制重新抓取所有文章**（例如首次配置后或想刷新 arXiv 数据），删除 `seen_guids.json` 再运行脚本即可。

---

### Step 8: 清理过期文件（仅 file 模式）

删除 `output_dir` 下超过 `retention_days` 天的旧目录。

> **注意**: 跳过当天日期目录。先列出 `output_dir` 下所有日期子目录，排除当天（`datetime.now(TZ).strftime('%Y-%m-%d')`），再逐个检查过期时间。

---

## 时效性原则

1. **今天的事优先** — 今天发布的优先于昨天的
2. **不看旧文** — 超过 3 天的新闻除非有重大后续，否则不收录
3. **宁可漏不可旧** — 如果 RSS 和搜索都没出新鲜内容，缩小条数
4. **紧跟发布动态** — 新模型、新开源项目、新硬件是重点目标

## 质量要求

- 每条新闻必须有**导读** — 不只是标题堆砌
- 每条新闻必须有**来源链接** — 且必须来自原始数据（见 Step 3 链接保真规则）
- 语言按 `user_config.yaml` 的 `language` 字段：zh 用中文输出，en 用英文输出
- 不要 AI 感过重 — 像人整理的一样自然

## 知识层（固定规则，每次执行必读）

以下规则固化在 SKILL.md 中，agent 每次执行都应遵守：

- **链接保真规则**（Step 3） — 不得猜测或替换链接
- **分类规则**（Step 4 表格） — 按优先级判断文章归类
- **时效原则**（见上） — 今天优先，超过3天不收录
- **质量要求**（见上） — 每条有导读、有来源链接
- **写入后必验证**（Step 6.5） — 未运行 verify_links.py 就交付视为流程违规

这些规则不依赖配置，是技能的核心质量标准。

> 关于交互配置模式的设计思路和复用方法，参见 `references/config-flow.md`。

---

## 文件结构

```
{skill_dir}/
├── SKILL.md                       # 本文件
├── README.md                      # 用户指引
├── skill.json                     # ClawHub 元信息
├── scripts/
│   ├── rss_fetch.py               # RSS 抓取引擎（stdlib only）
│   ├── rss_feeds.default.json     # 默认 28 源列表
│   ├── search_web_stdlib.py       # web 搜索兜底脚本（stdlib fallback）
│   ├── tz_offset.py               # 时区偏移计算脚本
│   └── verify_links.py            # 链接全量验证器（Step 6.5）
├── templates/
│   ├── report.zh.md               # 中文输出模板
│   └── report.en.md               # 英文输出模板
├── references/
│   └── config-flow.md             # 交互配置模式说明
└── user_config.yaml               # 用户配置（首次交互后生成，.gitignore 排除）
```

## 依赖

- Python 3.9+（stdlib only — 无需 pip 安装任何包）
- `web_search` 工具（DDG 搜索补充，可选 — 兜底方案纯 stdlib）
- 网络连接（RSS 抓取 + URL fetch）
