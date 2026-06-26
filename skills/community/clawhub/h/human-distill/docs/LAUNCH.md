# Human Distill — 发布手册

GitHub: https://github.com/spikesubingrui-design/human-distill

---

## 一、ClawHub（已上架 v1.0.0）

- 页面：https://clawhub.ai/skills/human-distill
- 安装：`clawhub install human-distill`

推荐用统一双端口脚本（GitHub + ClawHub）：

```bash
bash ~/.openclaw/workspace/scripts/skill-publish-dual.sh human-distill --bump patch -c "..."
```

手动 ClawHub 时请用**绝对路径**（相对路径 `.` 可能报 `SKILL.md required`）。

安装（他人）：

```bash
clawhub install human-distill
# 或
npx clawhub@latest install human-distill
```

后续更新：

```bash
clawhub publish . --slug human-distill --version 1.0.1 --changelog "..."
# 或批量
clawhub sync --bump patch --changelog "..."
```

---

## 二、社交媒体文案

### 中文 · 短文（X / 微博 / 即刻）

```
开源了一个 OpenClaw / Cursor Agent Skill：Human Distill 🧠

一句话：把博主/KOL 的抖音+全网内容，蒸馏成带 [确认]/[推断] 标签的人物观点档案。

• 全网搜索 + 抖音逐条文案（browser）
• quick / standard / deep 三档
• 输出 markdown 画像，可直接进知识库

GitHub ⭐ 欢迎：https://github.com/spikesubingrui-design/human-distill

#OpenClaw #AIAgent #抖音 #知识管理
```

### 中文 · 小红书 / 公众号（长一点）

**标题：** 我做了个 Agent Skill：自动「蒸馏」任意博主的世界观

**正文：**

跟 AI 说「帮我了解某某博主在营养/投资上的完整观点」，以前只能搜几条碎片。

**Human Distill** 把流程写进 Skill，Agent 会自动：

1. **全网搜索** — 公众号、知乎、YouTube、课程页、访谈  
2. **抖音深度**（可选）— 滚动主页、按关键词筛视频、提取描述 + AI 章节要点  
3. **合并蒸馏** — 7 维人物画像，每条观点标 **[确认]** 还是 **[推断]**

三档模式：
- **quick**：只要快速画像  
- **standard**：默认，含抖音文案  
- **deep**：再接本地深度研究（LDR）

开源 MIT，适配 OpenClaw + Cursor。

👉 GitHub：https://github.com/spikesubingrui-design/human-distill  
👉 觉得有用请 Star，方便更多人发现

---

### English · X / LinkedIn

```
Shipped: Human Distill — an OpenClaw / Cursor agent skill that turns a creator's scattered content into an evidence-graded persona dossier.

• Track A: web_search + web_fetch (articles, courses, interviews)
• Track B: Douyin browser scrape (captions + AI chapter summaries)
• Every claim tagged [confirmed] vs [inferred] vs [conflict]

quick / standard / deep modes. MIT licensed.

⭐ https://github.com/spikesubingrui-design/human-distill

#OpenClaw #AIAgents #KnowledgeExtraction
```

### English · Hacker News (Show HN style)

**Title:** Show HN: Human Distill – agent skill to distill a creator's worldview from web + Douyin

**Body:**

I built a text-only agent skill (SKILL.md) for OpenClaw/Cursor that:

1. Runs parallel web search across articles, YouTube, course pages
2. Optionally deep-scrapes Douyin via browser (scroll container trick documented)
3. Outputs a 7-section persona markdown with [confirmed]/[inferred]/[conflict] labels

No Douyin API. Browser + search tools only. MIT.

Repo: https://github.com/spikesubingrui-design/human-distill

Would love feedback on the evidence-grading schema and search query templates.

---

## 三、README 上架后更新（ClawHub 成功后）

在 README Installation 区增加：

```markdown
[![clawhub](https://img.shields.io/badge/clawhub-human--distill-blue)](https://clawhub.ai/skills/human-distill)

\`\`\`bash
clawhub install human-distill
\`\`\`
```

（将 `clawhub.ai` 链接换成 publish 成功后 `clawhub inspect human-distill` 返回的实际 URL。）

---

## 四、发布检查清单

- [ ] `clawhub login` + `whoami` 通过
- [ ] `clawhub publish` 成功
- [ ] README 加 ClawHub badge + install 命令
- [ ] GitHub Topics 已有（openclaw, cursor, agent-skill…）
- [ ] 发一条中文 + 一条英文推文
- [ ] （可选）Show HN / V2EX / 即刻
