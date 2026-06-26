---
name: mzu-news-briefing
description: "多源 AI 科技新闻简报聚合器。覆盖 AI 大模型、科技、财经，按热度分级输出，来源全程可溯。AIHOT 168 信源并行覆盖。8 维度强制搜索，15-20 条精选内容。支持 Twitter/X 和 Grok API。"
version: 2.0.4
tags:
  - AI简报
  - 新闻聚合
  - AI工具
  - 每日简报
  - 科技资讯
  - 财经新闻
  - 多源聚合
  - AIHOT
---

# Mzu News Briefing · 每日科技简报

> 多源新闻聚合与智能简报生成工具。覆盖 AI / 科技 / 财经 / 世界大事，按热度分级输出。
>
> **双搜索后端可选**：Twitter/X（需 cookies 配置）或 Grok API（需 API Key）。两者至少配一个，以 Twitter 为优先。

---

## 快速开始

### 第一步：安装依赖

```bash
# 1. 安装 agent-reach（bird CLI + RSS 读取）
python -m venv ~/.agent-reach-venv
source ~/.agent-reach-venv/bin/activate  # Windows: .\.agent-reach-venv\Scripts\activate
pip install agent-reach

# 2. 配置搜索后端（二选一）
# 选项 A：Twitter/X 搜索（优先，免费，需 cookies）
#   → 见"配置 Twitter/X" 章节

# 选项 B：Grok API 搜索（需 xAI API Key）
#   → 见"配置 Grok API" 章节
```

### 第二步：生成简报

```bash
# 告诉你的 AI 助手：
"帮我生成今天的新闻简报"
```

### 第三步：设置定时推送（可选）

```bash
# 每天 08:00 自动推送
openclaw cron add "0 8 * * *" "请按 mzu-news-briefing 技能生成简报并发送给我" --announce

# 每天 22:00 自动推送
openclaw cron add "0 22 * * *" "请按 mzu-news-briefing 技能生成简报并发送给我" --announce
```

---

## 配置指南

### 配置 Twitter/X（选项 A）

#### 安装 bird CLI

```bash
npm install -g @steipete/bird
```

#### 导出 Twitter Cookies

1. 在 **Chrome** 中登录 x.com
2. 按 **F12** → Application → Cookies → x.com
3. 复制 `auth_token` 和 `ct0` 的完整值

#### 保存认证信息

```bash
# 创建认证文件
echo "AUTH_TOKEN=你的auth_token值" > ~/.agent-reach-twitter.env
echo "CT0=你的ct0值" >> ~/.agent-reach-twitter.env
```

#### 验证连接

```bash
bird --auth-token 你的auth_token --ct0 你的ct0 whoami
# 应返回你的 Twitter 用户名
```

#### 加载认证（每次新 session 前）

```bash
# PowerShell（Windows）
Get-Content "~\.agent-reach-twitter.env" | ForEach-Object { $kvp = $_.Split('=',2); [Environment]::SetEnvironmentVariable($kvp[0], $kvp[1], 'Process') }

# Linux/macOS
export $(cat ~/.agent-reach-twitter.env | xargs)
```

---

### 配置 Grok API（选项 B）

#### 获取 API Key

1. 访问 https://x.ai/api 免费注册
2. 免费额度含实时搜索
3. 将 API Key 保存到 `~/.grok-api-key`

#### 验证连接

```bash
curl https://api.x.ai/v1/models \
  -H "Authorization: Bearer $(cat ~/.grok-api-key)"
```

#### 使用方式

Grok API 集成在搜索工作流里，**无需额外工具调用**——在维度 C 直接用 Grok 模型搜索即可：

```
使用 Grok 模型，工具：web_search，搜索：
"OpenAI announcement" OR "Anthropic Claude" this week
```

---

## 内容优先级

| 层次 | 比重 | 覆盖范围 |
|------|------|---------|
| 🥇 核心 | 50% | AI / 大模型 / Agent / 工具 / 研究 / 融资 |
| 🥈 延伸 | 30% | 科技行业 · 大厂动态 · 产品发布 · 平台新闻 |
| 🥉 补充 | 20% | 财经市场 · 股市 · 大宗商品 · 货币政策 |
| 🌍 背景 | 10% | 世界大事 · 地缘冲突 · 重大突发事件 |

> 军事新闻：少报，仅当事件对科技/财经/AI领域产生实质影响时入选。重大例外：若军事事件直接冲击科技供应链、能源市场或AI行业格局，可突破比重限制。

---

## 环境准备（Windows PowerShell）

> 每次执行简报前，**必须**设置 UTF-8 编码，否则 HTTP API 响应中文乱码：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```

---

## 执行纪律（必须遵守）

> ⚠️ **本 skill 强制要求以下纪律，不遵守则简报质量不合格：**

1. **AIHOT + 维度 A-G 必须全部执行完毕，不得跳过、缩减或合并**
   - 第零步（AIHOT）：必须调用
   - 第一步（日期窗口）：必须确认
   - 第二步（维度 A-G）：每个维度至少 1 次搜索，**不得以"时间不够""差不多了"等理由跳过**
   - 总搜索次数：**不得少于 8 次**（不含 AIHOT 调用）

2. **AIHOT 并行链路和维度 A-G 独立并行执行，互不依赖，不交叉引用直到第四步合并**

3. **搜索次数不足 8 次，不得输出简报**

4. **所有进入简报的条目，必须验证原文**（AIHOT 摘要 ≠ 原文）

---


---

## 工作流程

### 第零步（并行）：AIHOT 快速覆盖

> 与维度 A-G **并行执行**，不等待，不依赖。

**调用 AIHOT 公开 API（匿名免费，无需 key）：**

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

# 拉当天精选（按发布时间倒序，take=50）
curl -sH "User-Agent: $UA" \
  "https://aihot.virxact.com/api/public/items?mode=selected&take=50" \
  | jq '.items[] | {title, source, publishedAt, url, category, summary}'
```

**同时按 5 个分类拉当天日报（可选，作为补充参考）：**

```bash
# 当天日报（UTC 0点切片，北京时间 08:00 后才生成）
curl -sH "User-Agent: $UA" \
  "https://aihot.virxact.com/api/public/daily" \
  | jq '{date, lead: .lead.title, sections: [.sections[] | {label, n: (.items | length)}]}'
```

**输出要求：**
- 将 AIHOT 返回的条目按 category 分组整理
- 标注每条的 `publishedAt`（转换为北京时间）
- 保留 `url` 原文链接（供后续验证）
- **不输出原始 API 参数名、端点路径、限流数字等基础设施细节**

**并行逻辑：** AIHOT 结果与维度 A-G 的搜索结果**平行收集**，在第四步（合并）之前不交叉。AIHOT 负责广度，维度 A-G 负责验证和置信度。

---

### 第一步（必须优先执行）：锁定日期窗口

> ⚠️ **本步不可跳过。未锁定日期就直接开始搜索是导致旧闻污染的主要原因。**

在开始任何搜索之前，立即确认：
1. **今天日期**（YYYY-MM-DD）
2. **date_after 参数** = 今天日期的前一天（YYYY-MM-DD）
   - 例如：今天是 2026-03-27 → `date_after: "2026-03-26"`
3. **每条搜索都必须携带 `date_after`**，所有维度统一

**错误做法**：搜索词里写 "this week" / "March 2026" 而不带 date_after → 搜索引擎返回整月 SEO 聚合旧文
**正确做法**：搜索词 + `date_after: "2026-03-26"` → 强制只取昨天之后的新内容

### 第二步：多维度分层搜索

> ⚠️ **Brave 并发限制**：Brave Free Plan 同时只接受 1 个请求。
>
> **调用规则：**
> - 逐一串行执行，禁止并行调用 Brave
> - 每次调用后等待 **3 秒**再继续（留 1 秒 buffer）
> - 连续调用 **4 次**后，等待 **10 秒**再继续
> - 触发 429 后，等待 **30 秒**再重试
> - 如果需要超过 4 次 Brave 搜索，将其余搜索任务分配给 x_search（Grok）

#### 维度 A：周报 / Newsletter 聚合（最优先）

信息密度最高，一篇覆盖 10+ 条新闻。

```
搜索词（均需携带 date_after 参数）：
web_search("AI weekly roundup today", date_after="YYYY-MM-DD")
web_search("site:substack.com AI news", date_after="YYYY-MM-DD")
```

发现周报后，用 `web_fetch` 抓取全文，提取所有新闻线索。

**实测有效周报源：**
- https://www.neuralbuddies.com
- https://www.gtmaipodcast.com
- https://www.labla.org

#### 维度 B：社区热度信号（关键）

自下而上的社区爆款，泛搜索几乎无法触达。

```
搜索词（均需携带 date_after 参数）：
web_search("site:news.ycombinator.com AI", date_after="YYYY-MM-DD")
web_search("site:reddit.com/r/MachineLearning AI today", date_after="YYYY-MM-DD")
web_search("site:github.com/trending AI", date_after="YYYY-MM-DD")
```

#### 维度 C：AI 模型 / 大厂动态（重点）

**搜索后端优先级**：Twitter bird > Grok API > Brave 搜索引擎

```
# Twitter bird（已配置时）
bird search "@OpenAI OR @AnthropicAI OR @GoogleAI" -n 10
bird search "OpenAI announcement today" -n 5

# Grok API（无 Twitter 时）
使用 Grok 模型搜索："OpenAI OR Anthropic OR Google DeepMind today"

# Brave（最后备用，所有搜索必须带 date_after）
web_search("GPT-5 OR Claude 4 OR Gemini 3 announcement", date_after="YYYY-MM-DD")
web_search("DeepSeek OR MiniMo OR Llama model release", date_after="YYYY-MM-DD")
```

**固定页面抓取（web_fetch，每次都要当天日期过滤）：**
- https://releasebot.io/updates/openai — OpenAI 官方发布记录
- https://llm-stats.com/llm-updates — AI 模型发布追踪（GPT/Claude/Gemini）

#### 维度 D：中文专业媒体

```
搜索词（均需携带 date_after 参数）：
web_search("site:36kr.com AI 大模型", date_after="YYYY-MM-DD")
web_search("site:jiqizhixin.com AI", date_after="YYYY-MM-DD")
web_search("量子位 OR 机器之心 AI", date_after="YYYY-MM-DD")
```

**实测有效固定信源：**
- 36氪（36kr.com）
- 机器之心（jiqizhixin.com）
- 量子位（1baijia.com）

#### 维度 E：财经 / 市场信号

```
搜索词（均需携带 date_after 参数）：
web_search("AI startup funding today", date_after="YYYY-MM-DD")
web_search("AI IPO OR AI acquisition today", date_after="YYYY-MM-DD")
web_search("AI 融资 OR 人工智能投资 今天", date_after="YYYY-MM-DD")
```

**推荐固定信源：**
- https://aifundingtracker.com — AI 融资追踪
- Bloomberg AI 融资报道
- TechCrunch 融资板块

#### 维度 F：监管 / 政策

```
搜索词（均需携带 date_after 参数）：
web_search("AI regulation policy", date_after="YYYY-MM-DD")
web_search("AI law government today", date_after="YYYY-MM-DD")
```

**实测有效固定信源：**
- Reuters AI 政策报道
- Politico / Nextgov（美国政策）
- NYT AI 政策报道

#### 维度 G：财经市场（补充）

当本日有重大市场事件时补充：
```
搜索词（均需携带 date_after 参数）：
web_search("AI stocks market today", date_after="YYYY-MM-DD")
web_search("Nasdaq OR S&P 500 AI stocks", date_after="YYYY-MM-DD")
```

---

### 第三步：内容验证（关键，必须执行）

> ⚠️ **本步不可跳过。搜索摘要 ≠ 真实内容。SEO 聚合页会显示丰富摘要，但页面正文可能为空或无关。**

每条拟进入简报的新闻，必须完成以下验证之一：

#### 规则 A：官方/权威来源
- 来源为官方公告（OpenAI Blog、Anthropic 官网、Google Blog）、Reuters、BBC、36氪、机器之心等
- → 用 `web_fetch` 抓取正文，确认摘要内容与正文一致

#### 规则 B：SEO 聚合页降级为线索，不作主链
- 来源为未验证的 News 聚合站、AI 内容站（如 crescendo.ai 等）
- → 用 `web_fetch` 抓取
  - **正文有实质内容且与摘要吻合** → 降级为线索，搜索该事件找更权威来源确认
  - **正文为空/极少（如低于 500 字）/ 与摘要不符** → 丢弃该来源，不进入简报

#### 规则 C：无法验证的高热度话题
- 若某事件仅有不可靠来源，但热度信号极强（3+ 个低质量源同时提及）
- → 搜索该事件找官方或权威媒体确认
- → 确认不了 → 降低热度等级或丢弃

#### 规则 D：模型发布/版本升级类新闻 — 必须确认实际发布日期（新增，v1.1.2）
- 若某模型版本号（如 GPT-5.4）出现在媒体报道中，**必须追溯到官方发布渠道确认实际发布时间**
- **媒体报道日期 ≠ 模型发布日期**（典型错误：今天媒体报道"GPT-5.4 发布"，但模型已发布约两周）
- 验证方式：访问 `releasebot.io/updates/openai` 或 `llm-stats.com/llm-updates` 确认实际版本发布日期
- 结论判断：
  - 媒体报道日期 == 官方发布时间 → 当天新闻，可信
  - 媒体报道日期 > 官方发布时间（模型已发布多日）→ **降级为"跟进讨论"或"行业动态"，不列入当天高热度新闻**
  - 确认不了 → 降级或丢弃

#### 验证失败的标准（满足任一即丢弃）
- `web_fetch` 返回正文低于 500 字
- 页面内容与搜索摘要描述明显不符
- 来源域名无实质内容团队（可通过域名判断：纯聚合/SEO 农场特征）
- 属于已知的假新闻/谣言模式（如：凭空出现的"神秘模型发布"）
- 模型发布类新闻无法追溯官方发布日期 → 丢弃

---

### 第四步：合并 — AIHOT 与维度 A-G 结果整合

> AIHOT 精选和维度 A-G 搜索是**两条独立链路**，在合并前不做交叉引用。

**合并步骤：**
1. **去重**：AIHOT 的条目和维度 A-G 的条目做标题/URL 去重，保留最早或最权威来源
2. **补漏**：检查维度 A-G 中是否有 AIHOT 未覆盖的重大事件（如 AIHOT 精选中没有但维度 C 搜到的官方发布）
3. **置信度标注**：AIHOT 有但维度 A-G 没有独立验证的事件 → 降低热度等级；两者都有 → 提高热度等级
4. **最终条目数**：合并后总条目 **10-15 条**，高热 3-5 条

---

### 第五步：内容验证与交叉确认

> ⚠️ **所有进入简报的条目必须验证。AIHOT 的摘要 ≠ 原文，引用前请用 url 字段回原站核对。**

- Newsletter 提到但初轮未覆盖 → 专项搜索
- 同一事件被 **3+ 个不同来源**提及 → 确认热点，深入挖掘
- 中文源与英文源热点完全不同 → 两边各保留最有代表性条目
- **搜索不足 8 次不开始输出**（AIHOT 不计入搜索次数）

---

### 第六步：置信度标注与最终确认

- AIHOT 有但维度 A-G 没有独立验证的事件 → 降低热度等级
- 两者都有交叉验证 → 提高热度等级
- 更名项目视为同一事件（已在第四步处理）
- 最终确认进入简报的条目清单（10-15 条，高热 3-5 条）

---

### 第七步：热度分级

| 等级 | 信号 | 输出 |
|------|------|------|
| 🔥 高 | 3+ 来源确认 / 社区病毒传播 / 大厂官方公告 / 重大政策 | 深度分析段落（3-5 条）|
| ⚡ 中 | 2 个来源 / 有数据支撑 / 行业影响明确 | 标准摘要（5-8 条）|
| 💤 低 | 单来源 / 泛泛报道 / PR稿 | 仅标题或简短标注（3-5 条）|

---

### 第八步：输出语言

- **中文为主**
- 专业术语首次出现：英文原词（中文翻译）
- 例：Large Language Model（大语言模型）

---

## 输出格式

```
📰 Mzu 每日简报 YYYY-MM-DD HH:MM

本班共收录 XX 条 | 搜索 XX 次 | 覆盖维度：A/B/C/D/E/F
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 高热度

1. [新闻标题](https://...)
   来源：媒体名 | 时间：YYYY-MM-DD | 标签：#AI #Agent
   摘要：（50字以内）

   ▶ 深度：为什么这条重要
   · （分析点1）
   · （分析点2）

⚡ 中热度

2. [新闻标题](https://...)
   来源：媒体名 | 时间：YYYY-MM-DD | 标签：#大厂 #产品
   摘要：（含关键数据）

💤 低热度（如有）

3. [新闻标题](https://...)
   来源：... | 标签：...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AIHOT 覆盖：模型(X) 产品(X) 行业(X) 论文(X) 技巧(X)
维度覆盖：A(X) B(X) C(X) D(X) E(X) F(X)
搜索次数：X 次（不含 AIHOT 调用）
```

---

## 信息源质量分级

| 等级 | 来源 | 说明 |
|------|------|------|
| 🟢 权威/官方 | OpenAI Blog、Anthropic 官网、Google Blog、Reuters、BBC | 官方公告，直接使用 |
| 🟡 专业媒体 | TechCrunch、Ars Technica、36氪、机器之心、The Verge | 记者核实，可信 |
| 🔵 社区/UGC | Hacker News、Reddit/r/ML、GitHub Trending | 反映真实热度，需交叉验证 |
| 🟠 投资分析 | Motley Fool、The Fool、Seeking Alpha、Business Insider | **观点/预测为主，不是新闻事实**，降级处理 |
| 🔴 聚合/SEO | 未具名的 News 聚合站、内容农场 | 摘要≠正文，不作主链 |

---

## 反模式清单

❌ `"AI news today"` → SEO 聚合页噪音
❌ 加具体年月日 → 偏向预测文章
❌ **搜索时不带 `date_after` 参数** → 搜索引擎返回整月旧闻合集
❌ **只根据搜索摘要就进入简报** → 未验证内容导致今日 GPT-5.4 假新闻事故
❌ 只搜 3 次 → 覆盖率不到 30%
❌ 信任 SEO 聚合页/内容农场的摘要 → 页面可能为空，摘要≠正文
❌ **把投资分析网站当新闻源** → Motley Fool、The Fool、Seeking Alpha 等网站的标题常含观点性表述（"Huge News"、"Why X Matters"、"Is X Good?"），这类内容是分析观点而非新闻事实 → 降级处理或丢弃
❌ **把预期/预测当新闻** → "即将发布"、"预计"、"目标 Q2" 等表述不是已发生的事实，需标注为"行业动态"或"跟进"而非高热度新闻

✅ AIHOT 精选的摘要由 LLM 生成，引用前必须回原文 `url` 核对
✅ 每条搜索都必须携带 `date_after: "YYYY-MM-DD"`（今天的前一天）
✅ 至少 8 次搜索（AIHOT 不计入搜索次数）
✅ 用 `date_after` 约束时间窗口，而非依赖 "today"/"this week" 等模糊词
✅ **进入简报前，必须用 `web_fetch` 验证正文；正文不足 500 字或与摘要不符 → 丢弃**
✅ 优先以官方来源/权威媒体为主链；SEO 聚合页只作线索，不作主链

---

## 注意事项

- 优先 HTTPS 链接
- 付费墙标注「需订阅」
- 不做主观评价
- 总条数 **15-20 条**，高热度占 3-5 条，中热度占 5-8 条，低热度占 3-5 条
- 全程保留来源标注，每条均可溯源
- **所有维度 A-G 必须全部执行完毕，不得以任何理由缩减或跳过**
