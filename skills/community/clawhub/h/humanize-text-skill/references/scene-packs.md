<!--
  Migrated from shuorenhua/references/scene-packs.md (MIT, MrGeDiao).
  humanize-text-skill absorbs shuorenhua's Chinese completeness verbatim;
  cross-references updated to humanize-text-skill paths where needed.
-->

# Scene Packs / 可直接发场景包

Scene Packs 是面向可发布文本的子场景策略。它不替代 [场景禁改表](./scene-guardrails.md)、[Protected Spans](./protected-spans.md) 或 `Tier` 判断；只要文本本身像 README、release note、forum post 或 issue reply，就进一步判断“这段应该像哪一种发布文本”。

使用顺序：

1. 先判大场景：`chat / status / docs / public-writing`
2. 先划 protected spans：版本号、路径、链接、命令、引用、编号、责任归属都不能漂
3. 再看是否命中本文件的 scene pack
4. 最后按 scene pack 的发布目的收束语气；如果它同时像 `docs / status`，取更保守的保真边界

默认不要因为 scene pack 新增全局词条。只有新样本已经超出现有问题族，且会改变误杀边界时，才考虑补 `phrases` 或 `structures`。

## 交互合同 / Interaction contract

命中 scene pack 时，不只是“按规则改”，还要按该场景的发布目的来组织回应。默认流程：

1. 先说这段属于什么场景
2. 再说本场景最优先保留什么
3. 再决定是 `rewrite`、`audit-only` 还是 `minimal edit`
4. 最后用该场景能直接发出去的语气给结果

默认不要把所有场景都改成同一种“自然口语”。README、release note、forum post、issue reply 都应该像各自那种文本。

## Scene-first response shapes / 场景优先的输出形状

### `README`

- 先给一版能放在第一屏的 intro
- 如果原文缺定位，直接指出“缺这是什么 / 给谁用 / 解决什么问题”
- 默认不展开成长篇讲解

### `release-note`

- 优先改成可扫描的变更项
- 如果原文没有具体变更，不编造，直接指出“这里需要补 changelog 项”
- 不把 release note 改成品牌宣言

### `forum-post`

- 先保留“做了什么、踩了什么坑、现在怎么想”
- 可以有个人语气，但要压掉项目发布稿腔
- 如果原文有真实经历，默认只清姿态层，不重写叙事结构

### `issue-reply`

- 先回答“能不能复现 / 是否成立 / 下一步是什么”
- 再决定要不要补一句礼貌性承接
- 不要用客服话术稀释判断

## `README`

默认目标：

- 第一屏能让读者快速知道：这是什么、给谁用、解决什么问题。
- 语气可以有个性，但不能只剩愿景、价值和姿态。

必须保留：

- 项目名、目标用户、核心能力、支持平台
- 命令、安装方式、文件路径、链接
- 已有 benchmark 数量、版本号和能力边界

优先删除：

- `AI 全面重塑开发范式`
- `面向未来`
- `深度赋能`
- `内容生产链路`
- `价值闭环`
- 只说“先进 / 智能 / 全方位”但不说具体做什么的句子

默认力度：

- `standard`
- 如果 intro 只剩口号，可以升到 `aggressive`，但不能编造项目能力

误杀边界：

- README intro 允许一句有辨识度的定位句
- `CLI / API / benchmark / Codex / ChatGPT` 等项目术语应保留
- 不要把 README 改成社交媒体短帖

Before:

> 在 AI 全面重塑开发范式的今天，我们打造了一款真正面向未来的中文表达优化工具，深度赋能开发者的内容生产链路。

After:

> `说人话` 是一个中文优先的 rewrite skill，用来把 AI 写出来的套话、表演感和工程师腔改回自然表达。适合 README、release note、issue 回复和日常协作文本。

Few-shot cue:

- **Do**: 先说是什么、给谁用、解决什么问题
- **Don't**: 先讲时代趋势、价值闭环、方法论升级
- **Preferred answer shape**: 一段定位句 + 一句能力边界

## `release-note`

默认目标：

- 让读者快速知道这一版改了什么、怎么验证、有没有破坏性变化。
- 优先列表化，少写发布宣言。

必须保留：

- 版本号、日期、文件名、配置项、issue / PR 编号
- 变更类型：新增、修复、调整、测试
- 已知限制和迁移提示

优先删除：

- `Release Highlights` 后面只写空泛升级
- `系统性升级`
- `全新跃迁`
- `感谢所有用户持续支持`
- `共同见证`
- 没有来源的性能、效率、用户反馈数据

默认力度：

- `standard`
- 如果缺少具体 changelog，不要编造；改成提示“这里需要补具体变更”

误杀边界：

- release note 可以正式、简洁、列表化
- 不要为了“像人”把 changelog 列表改成故事
- 不要删版本号、文件路径、case 数量和 PR / issue 编号

Before:

> 本次版本是一次面向真实场景的系统性升级，感谢所有用户的持续支持，让我们共同见证中文 AI 写作体验的全新跃迁。

After:

> - 新增 `references/scene-packs.md`，覆盖 README、release note、forum post 和 issue reply
> - `evals/benchmark.md` 增加 8 条 scene pack 回归用例
> - 新增 `evals/results-v1.8.0.md` 记录本轮复核结果

Few-shot cue:

- **Do**: 列变更、版本号、验证方式、已知限制
- **Don't**: 写“感谢支持”“共同见证”“全新跃迁”
- **Preferred answer shape**: 变更列表；若缺项，返回“待补具体变更”

## `forum-post`

默认目标：

- 像维护者在社区里讲真实观察：做了什么、发现什么、哪里还不稳、想要什么反馈。
- 允许口语，但要有具体经历支撑。

必须保留：

- 时间、动作、具体文件、样本数量、观察到的问题
- 原作者真实态度和社区语气
- 链接、命令、版本号和被讨论词

优先删除：

- 公司公告腔
- `系统性重塑`
- `用户痛点`
- `多元场景`
- `方法论闭环`
- `稳稳接住核心诉求`

默认力度：

- `standard`
- 如果帖子本来有具体经历，只清理姿态层，不要改成正式公告

误杀边界：

- 具体经历后的口语词可以保留
- 社区帖允许“踩坑 / 折腾 / 还差一点”这类真实语气
- 不要把个人复盘改成 README 或 release note

Before:

> 折腾这个工具一个月后，我深刻意识到，中文 AI 写作治理不是一次简单的词表扩张，而是一场围绕真实表达场景的系统性重塑。

After:

> 做这个工具一个月后，我发现光删词表不够。README、release note、issue 回复和论坛帖看起来都是“公开文本”，但改法其实不一样。

Few-shot cue:

- **Do**: 保留维护者视角、踩坑过程、真实观察
- **Don't**: 改成产品官宣或论文摘要
- **Preferred answer shape**: 具体经历 + 一个判断 + 下一步关注点

## `issue-reply`

默认目标：

- 先回答问题是否成立，再给复现状态、判断和下一步。
- 不做客服式安抚，不替维护者承诺未排期能力。

必须保留：

- bad case 原句、场景标签、复现结果
- issue / PR 编号、文件路径、规则名、benchmark 编号
- “已确认 / 未复现 / 需要更多样本 / 会补测试”的状态

优先删除：

- `感谢宝贵反馈`
- `你问到了核心`
- `我们已经充分接住这个场景`
- `持续优化相关能力`
- `如果你愿意我可以继续帮你`

默认力度：

- `minimal` 或 `standard`
- 有具体技术信息时保守处理；没有具体下一步时，不要编造排期

误杀边界：

- issue 回复可以短、硬、直接
- `bad case / docs / SNF / benchmark / repro` 是维护语境里的正常术语
- 不要把明确的维护回复改成社交式寒暄

Before:

> 感谢你非常宝贵的反馈！你这个问题问到了项目体验的核心。我们已经充分接住了这个场景，也会在后续版本中持续优化相关能力。

After:

> 收到，这个 case 我能复现。它属于 `docs` 场景里的误杀，下一版先补一条 SNF；如果现有规则已经能放行，就只加回归用例。

Few-shot cue:

- **Do**: 先说是否复现、归类、下一步
- **Don't**: 先安抚，再空泛承诺持续优化
- **Preferred answer shape**: 结论句 + 状态句 + 下一步

## Few-shot mini pack / 小型 few-shot 包

这些例子不是新增规则，而是告诉模型“收到这类场景时，该怎么开始、怎么停手”。

### A. `README` intro

**Input**
> 在 AI 全面重塑内容生产范式的今天，我们打造了一套面向未来的表达优化底座，深度赋能开发者和内容团队完成高质量输出闭环。

**Better**
> `humanize-text-skill` 是一个中英双语的 rewrite skill，用来把 AI 文本里的套话、空话和表演感改回自然表达。适合 README、release note、issue 回复和公开写作。

Why this is better:

- 第一屏先交代项目定位
- 删掉时代口号和商业黑话
- 没有编造不存在的能力

### B. `release-note`

**Input**
> 本次版本是一次围绕真实场景展开的系统性升级，帮助团队在复杂协作环境中获得更加丝滑、完整、可持续的表达体验。

**Better**
> 这段缺具体变更，暂时不建议直接发。至少补三类信息：改了什么、怎么验证、有没有破坏性变化。

Why this is better:

- 原文没有 changelog，就先指出缺口
- 不用空话替代版本内容
- 这里适合 `audit-only`

### C. `forum-post`

**Input**
> 我们从用户痛点出发，持续打磨方法论闭环，终于让这个项目在多元场景下稳稳接住了大家的核心表达诉求。

**Better**
> 做了几轮样本之后，我发现最难的不是删套话，而是别把不同场景改成同一个口气。README、issue 回复和论坛帖，改法真的不一样。

Why this is better:

- 保留“复盘”的主用途
- 用观察替代姿态层
- 口气像维护者，不像市场稿

### D. `issue-reply`

**Input**
> 感谢你的宝贵反馈！这个问题对我们很重要，我们已经充分接住这个场景，后续会持续优化相关能力。

**Better**
> 这个 case 我能复现。它更像 `status` 场景，不该按 `public-writing` 的力度去洗。下一步我会先补一条 SNF 用例。

Why this is better:

- 先回答问题本身
- 给归类和下一步
- 不做空承诺
