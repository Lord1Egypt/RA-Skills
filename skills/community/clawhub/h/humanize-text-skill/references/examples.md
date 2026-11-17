<!--
  Migrated from shuorenhua/references/examples.md (MIT, MrGeDiao).
  humanize-text-skill absorbs shuorenhua's Chinese completeness verbatim;
  cross-references updated to humanize-text-skill paths where needed.
-->

# Rewrite Examples

> Each example shows the same passage in an AI-shaped version and a human-sounding version.

## Chinese Examples

### Example 1: Project introduction

**AI version:**
> 该项目是一个创新性的解决方案，旨在通过深度整合多种前沿技术，为用户提供全方位、一站式的智能化体验。它不仅能够显著提升工作效率，还能有效降低运营成本，实现真正的降本增效。

**Human version:**
> 这个项目把语音识别和自动翻译接到一起，用户说中文就能直接出英文字幕。上线两周日活 1200，翻译准确率 94%。

**What changed:**
- 删掉"创新性""前沿技术""全方位""一站式""智能化"——全是空词
- 删掉"不仅…还能…"的二元结构
- 加了具体功能描述和数据

---

### Example 2: Technical summary

**AI version:**
> 综上所述，通过对系统架构的全面优化和持续迭代，我们在性能、安全性和可维护性等方面均取得了显著提升。这一成果充分体现了团队在技术创新方面的不懈追求和卓越实力。

**Human version:**
> 这轮改完之后：API 响应时间从 800ms 降到 120ms，修了 3 个 SQL 注入漏洞，把 6000 行的 God Class 拆成了 12 个模块。

**What changed:**
- 删掉"综上所述"和整个总结式开头
- "显著提升"换成具体数据
- 删掉"充分体现""不懈追求""卓越实力"——自吹自擂
- 用具体改动代替抽象描述

---

### Example 3: Message reply

**AI version:**
> 好问题！这确实是一个值得深入探讨的话题。让我来为你详细解释一下。首先，我们需要了解的是，这个问题的本质在于……

**Human version:**
> 核心原因是缓存没失效。用户改了头像但 CDN 还在用旧的，TTL 设了 7 天太长了。改成 1 小时就行。

**What changed:**
- 删掉全部谄媚和铺垫
- 直接给原因和解决方案

---

### Example 4: News summary

**AI version:**
> 在当今快速发展的人工智能领域，OpenAI 近日发布了其最新的大语言模型，引发了业界的广泛关注和热烈讨论。该模型在多个关键指标上实现了显著突破，标志着人工智能技术迈入了一个全新的发展阶段。

**Human version:**
> OpenAI 发了 GPT-5。MMLU 跑分 92.3%，比上一代高 7 个点。上下文窗口翻倍到 256K。API 价格没涨。

**What changed:**
- 删掉"在当今""快速发展""广泛关注""热烈讨论"——全是废话
- "显著突破"换成具体跑分
- "全新的发展阶段"删掉——读者自己会判断

---

### Example 5: Engineer-slang / debug-slang

**AI version:**
> 我先拆开看了一下，发现根因偏硬，不太好直接打掉。目前已经把差异收窄了，和刚抓到的现象也对上了。接下来稳稳兜住，落盘之后就能收口。

**Human version:**
> 查了一下，原因是配置写死了，不能直接改。我把排查范围缩小到两个可能的地方，和之前的报错信息对得上。先把结论记下来，回头改一版就行。

**What changed:**
- "拆开看"→"查了一下"，"根因偏硬"→"原因是配置写死了"
- "打掉"→"改"，"收窄"→"缩小"，"抓到的现象"→"报错信息"
- "兜住"→删掉，"落盘"→"记下来"，"收口"→"就行"
- 整段从 postmortem 腔调改成正常同事对话

---

### Example 6: Xiaohongshu AI tone

**AI version:**
> 姐妹们！今天给大家拆解一个保姆级避坑攻略！这个工具真的绝绝子，狠狠提升了效率！建议收藏！划重点：免费！

**Human version:**
> 推荐一个工具：Raycast。免费版就够用，主要是启动快、插件多。我之前用 Alfred，切过来之后每天大概能省十几分钟，主要省在切窗口和查文档上。

**What changed:**
- 删掉全部硬凹人设的网络语
- "拆解""保姆级""避坑""绝绝子""狠狠""建议收藏""划重点"全删
- 换成具体工具名、具体用法、具体省了多少时间

---

### Example 7: Register mixing

**AI version:**
> 诚然，这个 bug 的修复确实存在一定的技术复杂度。不过说白了就是绝绝子的体验！我们需要进一步深入探讨其底层逻辑，稳稳把核心链路兜住。综上所述，未来可期。

**Human version:**
> 这个 bug 不好修，涉及到三个服务之间的调用顺序。我先把支付服务的超时时间从 3 秒调到 10 秒，观察一周再说。

**What changed:**
- 原文混搭了 5 种语域（学术/网络/商业/工程/鸡汤），统一成技术口语
- 把空泛描述换成具体方案

---

## English Examples

### Example 1: Product description

**AI version:**
> Our groundbreaking platform serves as a testament to the transformative potential of AI, empowering teams to navigate complex challenges and unlock unprecedented levels of productivity. Nestled at the intersection of innovation and practicality, it showcases how cutting-edge technology can foster meaningful collaboration.

**Human version:**
> The platform auto-assigns tickets based on who fixed similar bugs before. Teams using it close issues 2 days faster on average.

**What changed:**
- Removed "groundbreaking", "testament", "empowering", "navigate", "unprecedented", "nestled", "showcases", "cutting-edge", "foster"
- Replaced vague claims with specific functionality and data

---

### Example 2: Technical update

**AI version:**
> We're excited to announce a comprehensive update that significantly enhances performance, bolsters security, and streamlines the developer experience. This pivotal release underscores our commitment to delivering robust, scalable solutions.

**Human version:**
> This release cuts cold start time by 60%, patches CVE-2024-3891, and drops the config from 200 lines to 40. Upgrade guide is in the changelog.

**What changed:**
- "Comprehensive update" → specific changes
- "Significantly enhances" → "cuts by 60%"
- "Bolsters security" → specific CVE
- "Streamlines developer experience" → specific config reduction
- Deleted "pivotal", "underscores", "commitment", "robust", "scalable"

---

### Example 3: Analysis (two-pass demo)

**AI version:**
> The landscape of remote work has undergone a profound transformation. It's not just about working from home — it's about reimagining the very fabric of how we collaborate. Companies that fail to navigate this paradigm shift risk being left behind in an increasingly competitive ecosystem.

**First pass:**
> Remote work changed how teams collaborate. The teams that leaned into async communication and cut meetings adapted faster.

**Audit — what still feels AI?**
- "changed how teams collaborate" is still broad
- "adapted faster" is vague and a bit polished

**Final:**
> Remote work changed how teams collaborated, but not every company adjusted in the same way. Some changed how they communicated and worked together. Others just kept the same habits in a different setting.

**What changed in second pass:**
- Replaced the broad opener with a clearer contrast that stays inside the original claim
- Removed the vague "adapted faster"
- Broke the rhythm a bit without inventing new facts

---

## Two-pass examples | Residual Audit

### Example A：公开写作里的一遍 vs 两遍

**Original:**
> 这次把 onboarding 流程改了一遍，新用户从注册到完成首次导入少走了两步。更重要的是，这也说明我们开始真正理解用户在第一天最容易卡住的地方。

**First pass:**
> 这次把 onboarding 流程改了一遍，新用户从注册到完成首次导入少走了两步。我们也更清楚用户第一天最容易卡在哪里。

**Second pass:**
> 这次把 onboarding 流程改了一遍，新用户从注册到完成首次导入少走了两步。用户第一天最容易卡的地方，就是首次导入。

**What changed in the second pass:**
- 去掉了 `更重要的是 / 这也说明我们开始真正理解` 这层 narrator 话术
- 保留原文已有判断，只把它压回更直接的句子
- 没有补新事实，也没有重写整段

### Example B：status 场景里的克制 second pass

**Original:**
> 4 月 13 日把重试次数从 2 次调到 5 次。支付超时从 1.9% 降到 0.7%。这次调整也进一步验证了我们的优化方向是正确的。明天继续看晚高峰数据。

**First pass:**
> 4 月 13 日把重试次数从 2 次调到 5 次后，支付超时从 1.9% 降到 0.7%。这次调整说明方向是对的。明天继续看晚高峰数据。

**Second pass:**
> 4 月 13 日把重试次数从 2 次调到 5 次后，支付超时从 1.9% 降到 0.7%。明天继续看晚高峰数据。

**What changed in the second pass:**
- 只删掉 `方向是对的` 这种空判断
- 保留日期、数字和下一步，不往更口语的方向抛光
- `status` 场景如果第一遍已经够直接，第二遍就到这里停

---

## Bounded dual-output example | Bounded Scope Example

> Bounded output has two parts: cleaned body text and a deletion list that the user must confirm. Example (synthetic text):

**原文**

> 在数字化浪潮席卷各行各业的今天，提效工具层出不穷。我们团队过去三个月把周报流程从手填 Excel 改成了机器人自动汇总，每周大约省出两小时。研究表明，重复性事务的自动化能显著提升组织效能。具体做法是：机器人每周五拉取任务系统的状态变更，生成草稿，负责人只补一句风险说明。这不仅仅是一次流程优化，更是一种工作方式的革新。下个月我们准备把例会纪要也接进来。

**Body after in-sentence cleanup**

> 提效工具很多。我们团队过去三个月把周报流程从手填 Excel 改成了机器人自动汇总，每周大约省出两小时。具体做法是：机器人每周五拉取任务系统的状态变更，生成草稿，负责人只补一句风险说明。下个月我们准备把例会纪要也接进来。

**Suggested deletions (needs confirmation)**

1. 「研究表明，重复性事务的自动化能显著提升组织效能。」——无源权威铺垫；删掉后该段信息点不变（前后句已经给出做法和收益），也不承担过渡。不建议改写成「听说 / 据说」，那只是把无源说法换个壳。
2. 「这不仅仅是一次流程优化，更是一种工作方式的革新。」——价值拔高收尾；剥掉句式后没有剩余信息，前句（具体做法）和后句（下月计划）直接相接不断裂。

第一句「在数字化浪潮……层出不穷」没有进清单：剥掉铺垫后还剩「提效工具很多」这个实质判断，所以走句内洗，不删整句。

---

## Annotation Mode Examples

> The following groups show the difference between `annotation mode` and the default rewrite mode on the same text.

### Example A：公开文案里的无源引用

**Original:**
> 研究表明，采用 AI 协作开发的团队交付效率显著提升。业内人士认为，这一趋势将在未来十年持续加速。

**Annotation mode：**
- `问题族`：无源引用
- `触发点`：`研究表明`、`业内人士认为`
- `建议动作`：补具体来源；如果没有来源，删掉权威铺垫
- `是否建议改写`：是

**默认改写：**
> 用 AI 协作开发的团队，交付速度可能会更快，但这段话没有给出具体来源。要么补研究出处，要么直接把结论改写得更克制。

### Example B：status 场景里的保守处理

**Original:**
> 数据显示，这次改版显著提升了留存率。业内人士认为，这个方向已经验证可行。

**Annotation mode：**
- `问题族`：无源引用
- `触发点`：`数据显示`、`业内人士认为`
- `建议动作`：在 `status` 场景优先补数据来源和归属，不要改写成像已证实的事实
- `是否建议改写`：是

**默认改写：**
> 这段缺数据来源和观点归属。作为 status，同步时应补具体报表、时间范围或负责人；在补齐之前，不建议把它写成已经证实的结论。

---

## Scene-pack few-shot examples

> These examples are closer to the actual response shape a model should produce. The focus is not line-level rewriting but scene judgment, output shape, and stop conditions.

### Example I：README intro

**User intent:**
> 帮我把这个 README 开头去一下 AI 味，别改得像广告。

**Original:**
> 在 AI 全面重塑开发范式的时代背景下，我们打造了一套真正面向未来的表达优化基础设施，深度赋能开发者在复杂协作环境中实现高质量输出闭环。

**Recommended response shape:**
1. 先点明这是 `README` intro
2. 直接给可落到第一屏的版本
3. 简短说明删掉了哪些口号层

**Reference output:**
> 这是 `README` intro，优先要说清“这是什么、给谁用、解决什么问题”。
>
> 改写：
> `humanize-text-skill` 是一个中英双语的 rewrite skill，用来把 AI 文本里的套话、空话和表演感改回自然表达。适合 README、release note、issue 回复和公开写作。
>
> 我删掉了“全面重塑开发范式”“面向未来”“深度赋能”“输出闭环”这层口号，保留成项目定位句。

### Example J：release note 缺具体变更

**User intent:**
> 把这段发版说明改自然一点。

**Original:**
> 本次版本是一次围绕真实场景的系统性升级，我们在多个关键维度完成了全面优化，帮助团队获得更丝滑、更完整的使用体验。

**Recommended response shape:**
1. 先点明这是 `release-note`
2. 如果没有具体变更，优先 `audit-only`
3. 明说缺什么，不编 changelog

**Reference output:**
> 这是 `release-note`，但原文没有具体变更项，直接润色会把空话写得更顺，不建议那样做。
>
> 更稳的发法是先补：
> - 改了什么
> - 怎么验证
> - 有没有 breaking change
>
> 如果你要，我可以在你补完 changelog 项后帮你收成可发版本。

### Example K：issue reply

**User intent:**
> 帮我回这个 issue，别太客服。

**Original:**
> 感谢你的宝贵反馈！你这个问题对我们很重要，我们已经关注到这个场景，后续会持续优化。

**Recommended response shape:**
1. 先判断是否复现 / 是否成立
2. 再给归类和下一步
3. 礼貌可以有，但不要盖过信息

**Reference output:**
> 这个 case 我能复现。它更像 `docs` 场景里的误杀，不该按 `public-writing` 的力度处理。下一步我会先补一条 SNF 用例；如果现有规则已经能放行，就只加回归测试。

### Example L：forum post

**User intent:**
> 这段论坛复盘太像项目宣传稿了，帮我改回正常人会发的帖子。

**Original:**
> 我们从用户痛点出发，持续打磨方法论闭环，终于在多元表达场景下完成了系统性重塑。

**Recommended response shape:**
1. 先保留“复盘 / 观察”用途
2. 改成维护者在讲自己踩坑后的判断
3. 不扩写成立项宣言

**Reference output:**
> 做了几轮样本之后，我发现最难的不是删套话，而是别把不同场景都改成一个口气。README、issue 回复和论坛帖，看起来都像公开文本，实际改法差很多。

---

## Mode-specific examples

### Example M：`detect` mode

**User intent:**
> 先别改，帮我看这段哪里最像 AI。

**Original:**
> 综上所述，这一系统性升级不仅显著提升了协作效率，更标志着团队迈向未来工作方式的重要一步。

**Reference output:**
> P1:
> - `综上所述`：总结式收尾
> - `系统性升级`：空泛大词
> - `不仅…更…`：二元拔高骨架
> - `迈向未来工作方式的重要一步`：意义拔高
>
> 判断：
> - 明确问题，不是边界案例
> - 这段适合直接重写，不需要保留原骨架

### Example N：`edit` mode

**User intent:**
> 只小修这条 status，别重写。

**Original:**
> 4 月 12 日我们对支付链路进行了系统性优化，显著提升了稳定性。王宁会在今天把漏掉的 `source=campaign` 维度补回去。

**Reference output:**
> 编辑：
> - `系统性优化` → `调整了重试和超时配置`
> - `显著提升了稳定性` → 建议补具体指标；没有就先删掉
>
> 改后：
> 4 月 12 日我们调整了支付链路的重试和超时配置。王宁会在今天把漏掉的 `source=campaign` 维度补回去。
>
> 说明：
> - 保留了日期、责任人和 `source=campaign`
> - 没有补不存在的稳定性指标

### Example O：技术文档里的不改案例

**Original:**
> 网关在请求超时后返回 504。缓存服务每 5 分钟刷新一次热点 key。负载均衡器将流量按权重分配到三个后端节点。

**Annotation mode：**
- `问题族`：无明显问题
- `触发点`：系统主语和技术术语都属于正常文档写法
- `建议动作`：保持不动
- `是否建议改写`：否

**默认改写：**
> 网关在请求超时后返回 504。缓存服务每 5 分钟刷新一次热点 key。负载均衡器将流量按权重分配到三个后端节点。

---

# humanize-text-skill original examples (5 groups)

> These five groups show what `humanize-text-skill` adds beyond the two parent projects: bilingual symmetry, policy-driven scene handling, and the voice addition layer. The "engine evidence" in each group comes from actual test output (`npm test` reproduces it), not hand-written judgments.

## Example H1 ｜ Chinese README intro (jargon cleanup + protected span preservation)

**Before (AI-shaped):**

> 在 AI 全面重塑开发范式的今天，我们打造了一款真正面向未来的中文表达优化工具，深度赋能开发者的内容生产链路。

**After (humanized):**

> `humanize-text-skill` 是一个中英双语的 rewrite skill，把 AI 写出来的套话、表演感和工程师腔改回自然表达。适合 README、release note、issue 回复和日常协作文本。

**Engine evidence**：`score: 15 → 0`，命中 `tier1`（打造/面向未来/深度赋能/内容生产链路）。

**What changed**：
- 删掉「全面重塑开发范式 / 面向未来 / 深度赋能 / 内容生产链路」——全是空词
- 「打造」→「是」，直接说项目是什么、给谁用、解决什么
- 保留项目名 `humanize-text-skill`（protected span，术语不动）
- 按 `README` scene pack：第一屏要说清「这是什么、给谁用」

---

## Example H2 ｜ English LinkedIn post (English tier1 + voice->casual pull)

**Before（AI 味，目标 voice = casual）：**

> In today's rapidly evolving landscape, we leverage cutting-edge technology to deliver seamless, robust solutions. Moreover, this transformative platform empowers organizations to navigate the intricacies of modern business.

**After (humanized, pulled toward casual):**

> We ship tools that work. The platform handles the boring parts — retries, caching, fallbacks — so teams can focus on the actual problem. It runs in production at three companies now.

**Engine evidence**：`score: 40`，命中 `tier1`（leverage/cutting-edge/seamless/robust/transformative/empower/navigate/intricacies）+ `transition`（Moreover）；**`voice.drift: 44`**（casual 目标），2 条拉拢建议。

**What changed**：
- 7 个 tier1 词全换成人话（leverage→use, cutting-edge→实际能力描述）
- 删掉「Moreover」过渡废话
- voice 建议：句长过匀（CV 低）→ 混入短句（"We ship tools that work."）
- voice 建议：换 casual 偏好的连接词（and/but/so）

> ★ 这一组是两个父项目都做不到的：`avoid-ai-writing` 能去 tier1 词，但**不往 casual 拉**；shuorenhua 不管英文。humanize-text-skill 同时做了减法（去词）+ 加法（drift 44 + 具体建议）。

---

## Example H3 ｜ status scene routing (policy: audit-only, do not present as proven)

**Before（status 报告里的无源引用）：**

> 数据显示，这次改版显著提升了留存率。业内人士认为，这个方向已经验证可行，后续只要继续投入就能稳定放大收益。

**After（status 场景按 policy 走 audit-only）：**

> 这次改版后留存率有变化（具体数字待补报表和归因）。方向上还需要更长观察周期和对比组，目前不能确认是改版带来的。建议下周带 AB 数据再同步。

**Engine evidence**：`score: 10`（`sceneMode: status`），命中 `tier1`（数据显示/业内人士认为）+ `tier3`（显著）。

**What changed**：
- 按 `policy/scenes.toml`：`status` 的无源引用默认策略是 `audit-only`——**不补虚构来源，也不改写成像已证实**
- 「数据显示」→ 明确点出缺报表和归因
- 「业内人士认为」→ 删掉，因为不知道是谁
- 「稳定放大收益」→ 改成「需要观察周期和对比组」
- 没有编造任何图表、分析师或百分比

> ★ 这一组展示 policy 数据化的价值：同一句无源引用，在 `public-writing` 走 `rewrite-safe`（直接删权威铺垫），在 `status` 走 `audit-only`（点明缺来源）。**两个父项目都把这种区别写死在散文里，humanize-text-skill 是 TOML 可调、CI 可验。**

---

## Example H4 ｜ issue 回复（客服腔 → 直接答 + 保留术语）

**Before（AI 客服腔）：**

> 感谢你非常宝贵的反馈！你这个问题问到了项目体验的核心。我们已经充分接住了这个场景，也会在后续版本中持续优化相关能力。如果你愿意，我可以先帮你把这段文本整体梳理一遍。

**After（issue-reply scene pack）：**

> 收到，这个 case 我能复现。它属于 `docs` 场景里的误杀，下一版先补一条 SNF；如果现有规则已经能放行，就只加回归用例。

**Engine evidence**：`score: 17`，命中 `tier1`（感谢宝贵反馈/问到了核心/接住场景）+ `tier2`（持续/相关 聚集）。

**What changed**：
- 按 `issue-reply` scene pack：先回答问题是否成立，再给复现状态和下一步
- 删掉客服式安抚（感谢宝贵反馈/充分接住/持续优化/如果你愿意我可以）
- **保留** issue 语境术语：`case` / `docs` / `SNF` / `回归用例`（这些是维护者正常用语，protected）
- 没有替维护者承诺未排期能力

---

## Example H5 ｜ 双语对称（同一概念中英同 type 命中）

**同一个「二元对比」反模式，中英各一段：**

| | 文本 | 引擎命中 |
|---|---|---|
| **zh** | 真正的竞争力不是功能堆砌，而是体验细节。 | `false-concession` ✓ |
| **en** | It is not about features, it is about the details of the experience. | `false-concession` ✓ |

**Engine evidence**：两种语言命中**同一个 type**（`false-concession`）——这是 humanize-text-skill 的**强对称契约**。

**为什么这是卖点**：
- `avoid-ai-writing` 的英文「It's not X, it's Y」没有专门的结构检测（只靠 tier1 词兜底）
- shuorenhua 的中文「不是 X 而是 Y」有检测，但不管英文
- humanize-text-skill 让**同一概念在中英两侧用同一个 type**，`bilingual.test.js` 用 CI 钉死这个对称

**改写方向（中英对照）**：
- zh：体验细节决定产品能不能长期被用下去。（直接陈述，去掉二元对比骨架）
- en：The details of the experience decide whether the product lasts.（直接陈述，去掉 "not X but Y" 骨架）

> ★ 这是双语引擎的核心：改中文的人、改英文的人、改中英混排的人，看到的是**一致的检测语义**，不会出现"中文报了问题、英文同样的结构却没报"。
