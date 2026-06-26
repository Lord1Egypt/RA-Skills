# 🗞️ Mzu News Briefing

> **多源 AI / 科技新闻智能简报聚合器**
> Multi-source AI/Tech News Aggregator — Intelligent Daily Briefings

---

## ✨ 核心能力 · What It Does

| 功能 · Feature | 说明 |
|---|---|
| 🤖 **AIHOT 并行链路** | 168 信源 / 5 分类 / 匿名 API，零配置极速覆盖 |
| 🔍 **8 维度强制搜索** | A–G 全维度执行，搜索次数 ≥ 8 次，不缩水 |
| 📊 **热度分级输出** | 🔥 高热 3–5 条 · ⚡ 中热 5–8 条 · 💤 低热 3–5 条 |
| 🌐 **中英双语** | 中文为主，专业术语附英文原文 |
| ✅ **来源可溯** | 每条新闻均可回溯原始链接，摘要 ≠ 原文 |

---

## 🚀 核心更新 · v2.0 Highlights

### 🆕 AIHOT 并行快速覆盖（第零步）

与传统 8 维度搜索**完全并行**，互不依赖：

```
AIHOT API → 获取当天精选（168 信源 / 5 分类）
维度 A–G  → 深度专项搜索（7 个维度）
第四步合并 → 去重 · 补漏 · 置信度标注
```

**为什么有效？**
- AIHOT 擅长产品动态（Perplexity Mac / Codex Chrome / DeepSeek V4）
- 维度搜索擅长财经/政策大事件（融资/监管/估值）
- 两者互补，覆盖率大幅提升

### ⚡ 执行纪律强制化

| 规则 | 要求 |
|------|------|
| 维度 A–G | **必须全部执行**，不允许跳过 |
| 搜索次数 | **≥ 8 次**（不含 AIHOT）|
| 条目上限 | **15–20 条**（高热 3–5 / 中热 5–8 / 低热 3–5）|

---

## 📋 工作流 · Workflow

```
第零步 ── AIHOT 并行快速覆盖（匿名 API，无需 key）
  ↓
第一步 ── 锁定日期窗口
  ↓
第二步 ── 多维度分层搜索
        A. 周报 / Newsletter 聚合
        B. 社区热度（Hacker News / Reddit / GitHub）
        C. AI 模型 / 大厂动态
        D. 中文专业媒体（36kr / 机器之心 / 量子位）
        E. 财经 / 融资 / IPO
        F. 监管 / 政策
        G. 财经市场（补充）
  ↓
第三步 ── 内容验证（规则 A–D）
  ↓
第四步 ── 合并（去重 → 补漏 → 置信度标注）
  ↓
第五步 ── 内容验证与交叉确认
  ↓
第六步 ── 置信度标注与最终确认
  ↓
第七步 ── 热度分级
  ↓
第八步 ── 输出（中文为主）
```

---

## 📰 输出示例 · Output Sample

```
📰 Mzu 每日简报 2026-05-08 09:00

本班共收录 17 条 | 搜索 10 次 | 覆盖维度：A/B/C/D/E/F
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 高热度

1. Anthropic 估值突破 $1,000 亿登顶全球最高
   来源：Bloomberg / BeBeez | 时间：2026-05-08 | 标签：#AI #融资
   摘要：Anthropic 完成新一轮融资，估值达 $1,000 亿，超过 OpenAI
   
   ▶ 深度：为什么这条重要
   · 刷新全球 AI 公司最高估值纪录
   · 估值背后是 Claude 模型商业化加速
   · 对 OpenAI 上市计划产生压力

⚡ 中热度

2. EU 高风险 AI 规则推迟至 2027 年执行
   来源：Reuters / AIHOT industry | 时间：2026-05-07 | 标签：#监管 #政策
   摘要：欧盟委员会宣布高风险 AI 系统监管时间表延后两年

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AIHOT 覆盖：模型(2) 产品(3) 行业(1) 论文(0) 技巧(1)
维度覆盖：A(2) B(1) C(2) D(1) E(2) F(1)
搜索次数：10 次（不含 AIHOT）
```

---

## 🔧 安装 · Installation

### 第一步：安装 agent-reach

```bash
python -m venv ~/.agent-reach-venv
source ~/.agent-reach-venv/bin/activate  # Windows: .\.agent-reach-venv\Scripts\activate
pip install agent-reach
```

### 第二步：配置搜索后端（二选一）

#### 方案 A：Twitter/X（推荐 / 推荐 / Free）

```bash
npm install -g @steipete/bird

# 从 Chrome 导出 auth_token + ct0
# 保存到 ~/.agent-reach-twitter.env

# 验证
bird --auth-token YOUR_AUTH_TOKEN --ct0 YOUR_CT0 whoami
```

#### 方案 B：Grok API

```bash
# 在 https://x.ai/api 免费注册获取 API Key
echo "YOUR_GROK_API_KEY" > ~/.grok-api-key
# 无需额外 CLI，Grok 直接集成在工作流中
```

### 第三步：设置每日定时简报（可选）

```bash
# 每天 08:00 早间简报
openclaw cron add "0 8 * * *" "请按 skills/mzu-news-briefing/SKILL.md 生成今日简报" --announce

# 每天 22:00 晚间简报
openclaw cron add "0 22 * * *" "请按 skills/mzu-news-briefing/SKILL.md 生成今日简报" --announce
```

---

## 🔮 搜索维度说明 · Dimensions

| 维度 | 主题 | 主要信源 |
|------|------|---------|
| **AIHOT（第零步）** | 快速覆盖 · 168 信源 · 5 分类 | aihot.virxact.com（匿名 API）|
| A | 周报 / Newsletter 聚合 | NeuralBuddies · gtmaipodcast · labla.org |
| B | 社区热度信号 | Hacker News · Reddit r/ML · GitHub Trending |
| C | AI 模型 / 大厂动态 | Twitter/X · releasebot.io · Grok API |
| D | 中文专业媒体 | 36氪 · 机器之心 · 量子位 |
| E | 财经 / 融资 / IPO | aifundingtracker · Bloomberg AI |
| F | 监管 / 政策 | Reuters AI · Politico · NYT AI |
| G | 财经市场（补充）| 重大市场事件时触发 |

> ⚠️ **Windows PowerShell 用户**：首次运行前设置 `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`，避免中文乱码。

---

## ⚠️ 反模式 · Anti-Patterns

| ❌ 错误做法 | ✅ 正确做法 |
|-----------|------------|
| `"AI news today"` → SEO 噪音 | 用 "this week" / "latest" |
| 加具体年月日 → 预测文章 | 用相对时间描述 |
| 只搜 3 次就开始写 → 覆盖率不足 30% | 至少 8 次搜索后再输出 |
| 跳过维度 A–G 中的任何一个 | 所有维度必须全部执行 |
| 把 AIHOT 摘要当原文引用 | 必须回 url 字段核对原文 |
| 搜索次数不足 8 次就输出 | 搜索次数不足 8 次 → 不得输出简报 |

---

## 📊 信息源质量分级 · Source Quality

| 等级 | 来源 | 说明 |
|------|------|------|
| 🟢 权威/官方 | OpenAI Blog · Anthropic 官网 · Google Blog · Reuters | 官方公告，直接使用 |
| 🟡 专业媒体 | TechCrunch · Ars Technica · 36氪 · 机器之心 | 记者核实，可信 |
| 🔵 社区/UGC | Hacker News · Reddit r/ML · GitHub Trending | 反映真实热度，需交叉验证 |
| 🟠 投资分析 | Motley Fool · Seeking Alpha · Business Insider | **观点/预测为主**，降级处理 |
| 🔴 聚合/SEO | 无名 News 聚合站 · 内容农场 | 摘要≠正文，不作主链 |

---

## 📌 必读提醒 · Notes

- HTTPS 链接优先
- 付费墙内容标注「需订阅」
- 客观叙述，不做主观评价
- 所有条目注明来源，每条均可溯源
