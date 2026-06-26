# karpathy-curated-rss-brief

A Claude Code skill that fetches articles from Andrej Karpathy's curated RSS feed list and generates a high-quality Chinese tech daily newsletter.

[English](#english) | [中文](#中文)

---

## English

### Inspiration

This skill was sparked by two ideas arriving at the same time:

**1. Karpathy's RSS list** — In a [tweet](https://x.com/karpathy/status/2018043254986703167), Andrej Karpathy shared his personal RSS subscription list: 93 hand-picked blogs from top engineers, researchers, and writers in tech. The list reads like a curated course on how the best minds in the field actually think.

**2. Cory Doctorow on RSS** — In [*The web is bearable with RSS*](https://pluralistic.net/2026/03/07/reader-mode/), Cory Doctorow argues that RSS is one of the few remaining technologies that lets you own your information diet — no algorithm, no engagement bait, just the writing people actually chose to publish. The article is a timely reminder that the open web is still worth tending.

Both pieces converged on the same insight: the best signal is already out there, distributed across personal blogs and feeds. The challenge is aggregation and synthesis — exactly what an AI agent is good at.

**3. YouMind** — The skill itself was built and published via [YouMind](https://youmind.com/~skills/019c4fce-220b-7f35-974b-0cc543b7682d), a platform for sharing and discovering Claude Code skills.

### What it does

1. Fetches the latest articles from all 93 feeds asynchronously
2. Selects the 8–10 most valuable pieces (prioritizing AI breakthroughs, major product launches, then diversity and depth)
3. Reads each article in full via WebFetch
4. Generates a structured Chinese newsletter following a consistent template
5. Writes an editorial observation section — a synthesized, opinionated take connecting themes across articles
6. Saves the output as `{YYYY-MM-DD}-Karpathy精选RSS日报.md` with encoding validation

### Installation

**Via ClawHub (recommended):**
```bash
npm install -g clawhub
clawhub install karpathy-curated-rss-brief
```

**Via skills.sh:**
```bash
npx skills@latest install karpathy-curated-rss-brief
```

**Via Claude Code Plugin Marketplace:**
```
/plugin marketplace add MESevenJourney/eric-awesome-skills
/plugin
```
Browse to `karpathy-curated-rss-brief` and select **Install**.

**Dependency:** [`uv`](https://docs.astral.sh/uv/) for running the Python fetch script.

### Usage

In Claude Code, type:
```
RSS 日报
```

---

## 中文

### 灵感来源

这个 Skill 的诞生来自两篇内容几乎同时出现：

**1. Karpathy 的 RSS 订阅列表** — Andrej Karpathy 在[一条推文](https://x.com/karpathy/status/2018043254986703167)中分享了他的个人 RSS 订阅列表：93 个精心挑选的博客，作者都是技术领域最顶尖的工程师、研究员和写作者。这份列表本身就是一份关于"顶级思考者如何思考"的精选课程。

**2. Cory Doctorow 谈 RSS** — 在[《有了 RSS，网络还是可以忍受的》](https://pluralistic.net/2026/03/07/reader-mode/)一文中，Cory Doctorow 指出 RSS 是少数几种仍然让你掌控自己信息来源的技术——没有算法推送，没有注意力陷阱，只有人们真正选择发布的文字。这篇文章是一个及时的提醒：开放网络仍然值得我们去守护。

两篇内容指向同一个洞察：最好的信号已经散落在各处的个人博客和订阅源里。难点在于聚合与提炼——而这正是 AI Agent 擅长的事情。

**3. YouMind** — 这个 Skill 本身通过 [YouMind](https://youmind.com/~skills/019c4fce-220b-7f35-974b-0cc543b7682d) 发布，一个用于分享和发现 Claude Code Skills 的平台。

### 它做什么

1. 异步并发抓取 93 个订阅源的最新文章
2. 筛选 8-10 篇最有价值的内容（优先 AI 重大进展、重磅产品发布，兼顾多样性和深度）
3. 用 WebFetch 逐篇读取全文
4. 按固定模板生成结构化中文日报
5. 撰写编者观察：综合所有文章，提炼跨领域的联系和反直觉洞察
6. 保存为 `{YYYY-MM-DD}-Karpathy精选RSS日报.md`，并自动校验编码

### 安装

**通过 ClawHub（推荐）：**
```bash
npm install -g clawhub
clawhub install karpathy-curated-rss-brief
```

**通过 skills.sh：**
```bash
npx skills add https://github.com/MESevenJourney/eric-awesome-skills.git --skill karpathy-curated-rss-brief
```

**通过 Claude Code 插件市场：**
```
/plugin marketplace add MESevenJourney/eric-awesome-skills
/plugin
```
找到 `karpathy-curated-rss-brief`，选择 **Install**。

**依赖：** [`uv`](https://docs.astral.sh/uv/)，用于运行 Python 抓取脚本。

### 使用

在 Claude Code 中输入：
```
RSS 日报
```

---

### Feed Sources

The 93 feeds come from Karpathy's personal OPML — notable voices include Simon Willison, Paul Graham, Troy Hunt, Krebs on Security, Daring Fireball, gwern, antirez, Dan Abramov, Gary Marcus, Dwarkesh Patel, Cory Doctorow, geohot, and many others.

### References

- Karpathy's tweet: https://x.com/karpathy/status/2018043254986703167
- Cory Doctorow, *The web is bearable with RSS*: https://pluralistic.net/2026/03/07/reader-mode/
