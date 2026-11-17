# Advanced Human Writing & AI Humanizer

<p align="center"><img src="assets/logo.png" width="320" alt="Human Writing：奶白底色上的钢笔手写笔迹与终端代码"></p>

> 让 AI 写作更自然：以 Skills 和 DSH 插件提供多语言润色、长文分块协作与上下文一致性审查。

**DSH 插件安装：**用于在 DSH 中生成小说、论文和报告，前置去 AI 味规则并挂载本地审查工具。

```powershell
dsh plugin --profile web add https://github.com/whh110112/human-writing-skills/releases/download/dsh-v0.3.1/dsh-advanced-human-writing.tgz
```

桌面版把 web 换成 desktop；需要 Python 3.9+，无须另行 pip 安装核心。
详见 [DSH 插件说明](plugins/deepseek-harness/README.zh-CN.md)。

## 生成时前置去 AI 味与独立复核

**DSH 智能体模式：**按需调用 `writing__human-writing__agent_capabilities`，
检查当前智能体实际可见的委派工具及参数；自定义工具名可通过 `delegationToolName` 配置。
工具可见不等于执行器可用，也不代表子代理已完成。完整任务按角色交接，超大任务分页读取；
认领返回有效期，同一身份可在到期前续领。未配置子代理执行器时明确降级为顺序角色轮次。
已验证官方 DSH `0.2.1-rc.2` 的 Cordis/MCP 集成，真实模型子代理仍依赖宿主驱动、权限与容量。

`build`、`humanize` 和 MCP 的 `compile_generation_prompt` 默认加载精简的
`generation-quality` 协议：写之前确认读者、目的和材料，写作中约束套话、
修辞结构重复、冗余解释、装饰性细节、虚构经历、翻译腔和无意义收尾。
小说关注行动、对白回应与场景推进；事实类文章关注读者任务、证据和不确定性。
允许直接表达情绪、正式文风、必要重复和清楚结论，不强制加入犹豫、身体反应或悬念。
完整结尾审查等深度模块仍按需加载；有原文的改写自动保护作者声音。

事实类自媒体、产品体验和议论文可使用显式 `--source`；小说不会自动启用事实来源审查。

```powershell
human-writing-skills build --style self-media --task "根据测试记录写给购买者的说明" --source test-notes.md
human-writing-skills critique --draft article.md --style self-media --output diagnosis.md
human-writing-skills compare-blind --original original.md --candidate revised.md --style self-media --brief writing-brief.md --output-dir blind-review
human-writing-skills stats --draft article.md --language de --format json
human-writing-skills evaluate-editorial --cases ballots.json --format json
```

`critique` 只生成指出问题的提示，不代写。盲评时只把 `comparison.md` 交给不知道
修改历史的评审，另存 `version-key.json`；允许原稿胜出、平局或证据不足。
这些工具不会调用模型，人工评分也不会自动生成。参见[质量评测](docs/evaluation.zh-CN.md)。
单元测试验证程序行为，真实自然度仍需独立母语评审。

**增强版去 AI 写作 Skill / 高级 AI 写作工具**：支持去AI味、去AI写作、消除AI腔、
AI 人性化改写、AI 文本润色、小说润色、小说续写、长篇分块审查、文风统一和人物设定统一。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](pyproject.toml)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](pyproject.toml)

中文说明 | [English](README.md) | [Español](README.es.md) | [Português (Brasil)](README.pt-BR.md) | [Français](README.fr.md)

Advanced Human Writing & AI Humanizer 是一个开源、模块化的多语言 AI 写作技能包，也带有一个轻量级命令行工具。它把“写得自然一点”“不要有 AI 味”“长文不要忘设定”这些模糊要求，拆成 AI 能执行、能检查、能复用的 Markdown `SKILLS`。它既可以作为去 AI 味工具和 AI 文章润色工具，也可以用于小说创作、长文续写与严肃文本审校。为兼容已有安装和链接，Python 包名、GitHub 仓库名与 ClawHub slug 继续使用 `human-writing-skills`。

这不是只有说明文档的空提示词仓库。项目有两层刻意分开的能力：

- **可执行的 Python 工具层：** `humanwriting/` 提供可安装的
  `human-writing-skills` 命令行，可确定性地定位文本模式并给出证据位置、统计文本、
  预览保守修复、校验不可误改内容、编译提示词以及生成分阶段审稿文件。
- **由模型执行的编辑模块层：** `skills/*.md` 保存按需选择的文体与审稿规则，
  由写作模型执行。文学判断本来就不能完全靠固定算法，因此这些模块不会冒充
  “一键自动写好小说”的确定性程序。

测试套件同时覆盖可执行工具和模块按需激活逻辑。

## Agent 编排、MCP 与 DeepSeek Harness 插件

### 多 Agent 长篇写作、大纲驱动与逐块审稿

新增从大纲生成长文的五角色流程：大纲检查 Agent、切块规划 Agent、各块写作 Agent、
各块独立审查 Agent，以及负责上下文衔接的主 Agent。六万字符、每块五千字符会生成
12 个写作任务及对应审稿任务。每位写作者只拿到本块大纲和已确认的前文状态，
审稿必须覆盖每段，统稿必须核对每对相邻块；返修会使受影响的后续草稿和批准失效。

```powershell
human-writing-skills plan-writing --outline outline.md --context ledger.md --style fiction --target-length 60000 --chunk-size 5000 --output-dir book-writing
human-writing-skills writing-tasks --package-dir book-writing
```

默认按依赖顺序写作；用户明确要求并行、各块有已约定的入口/出口状态时，使用
`--execution-mode contract`，并用 `--max-parallel 4` 限制同时认领数。
`--length-unit words` 可改为按单词规划。真正的子 Agent 由宿主提供；DSH 仅在请求长篇输出
或明确多 Agent 写作时加载详细编排协议。[完整步骤、结果契约和恢复方式](docs/long-form-writing.zh-CN.md)。

### 共用审查状态

对于整本小说、系列报道或无法交给单一聊天窗口可靠审完的大型材料，可安装零额外依赖的
`human-writing-mcp` 服务。它把长篇任务图变成可由 Codex、Claude Code、OpenCode、DeepSeek
Harness、Manus 和 Hermes 共用的执行界面：Agent 领取有边界的任务、提交覆盖回执，全部必需
审查完成前不能领取统稿任务。服务只访问指定项目根目录，不会自行调用模型，也不会上传草稿。

```powershell
human-writing-mcp --root C:\writing-project
```

仓库还提供原生 DeepSeek Harness npm/Cordis Bundle，位于
[`plugins/deepseek-harness`](plugins/deepseek-harness)。它会挂载官方 DSH MCP 客户端并启动同一套
可验证本地协作服务。详见 [Agent 编排与 MCP 指南](docs/agent-orchestration.zh-CN.md) 与
[DeepSeek Harness 插件说明](plugins/deepseek-harness/README.zh-CN.md)。

MCP 现在也可处理日常单篇任务：`lint_text`、`get_style_statistics`、
`verify_protected_content`、`verify_fidelity`、`compile_humanize_prompt`、`compile_audit_prompt` 与
`compile_ledger_extraction`。对于实现 MCP Prompts 的客户端，还会提供精简的原生指令菜单，
如 `humanize-quick`、`dialogue-audit`、`continuity-audit`、`serious-rewrite` 等。它们只在
本地返回证据或编译后的指令，不会自行把草稿发送给模型。

## 账本自动提取与项目默认配置

长篇连续性不应该从人工逐条维护事实开始。`extract-ledger` 会为已有章节编译一份以证据为先的
提取 Prompt，供写作 Agent 生成**待确认连续性账本**。每项人物状态、道具、承诺、伤势、资源
变化或空间关系都必须给出引文/位置，并区分观察到的事实、推断、冲突与未知项；确认前不能当作
正式设定。

```powershell
human-writing-skills extract-ledger --draft chapters-01-10.md --context novel-ledger.md --output ledger-extraction-prompt.md
```

项目根目录可放置 `.humanwriting.json` 保存轻量默认项：文体、文档类型、相对账本路径与 lint
allowlist。显式 CLI 参数永远优先；配置文件不能偷偷开启深度 Profile、参考文风或资料来源等
高 token 阶段。临时命令需要忽略最近项目配置时可加 `--no-project-config`。详见[账本自动提取指南](docs/ledger-extraction.zh-CN.md)。

```json
{
  "style": "fiction",
  "document_type": "fiction",
  "context": "novel-ledger.md",
  "allow": ["END001"]
}
```

## 编辑器、CI 与 Python 分发

单篇文本命令支持 `--draft -` 从标准输入读取。`lint --format github` 会输出 GitHub Actions
行内标记；`list --kind rule` 可打印全部规则 ID、级别、分类和修订方向。

```powershell
git diff -- docs\ | human-writing-skills lint --draft - --style general --format github --source-name docs-change.md
human-writing-skills list --kind rule --format json
```

每个 GitHub Release 都会构建 wheel 与 source distribution，并附加到 Release Assets。PyPI 使用
GitHub Trusted Publishing：只有完成 PyPI 可信发布者配置，并设置仓库变量
`PYPI_PUBLISH_ENABLED=true` 后才会自动发布；仓库不保存 PyPI token。

它适合小说、网文、议论文、新闻报告、自媒体文章、科研论文等不同写作场景。项目重点不是伪装作者身份，而是提升 AI 辅助写作的质量：减少模板腔，增强上下文衔接，让文本更像经过人类编辑认真处理过。

## 长篇审查与文风统一

小说/网文达到至少三个可识别章节时，可显式使用 `chunk-audit --book-level`。
它会在逐块审查完成后只增加**一次全书结构审查**，对照人物选择与代价、冲突
发展、时间结构和过早解释主题等跨章问题，不给每块重复塞模块，也不用于报告。

项目现在提供可执行的 `chunk-audit`：把一年跨度的小说、系列文章或大体量报告按自然边界
切成唯一正文块，给每块附上少量只读前文，并统一对照“经用户确认的文风基准 + 大纲/账本”。它会
生成逐块审查提示词、跨块文风统计差异和最终汇总提示词，用于发现模型升级或长期写作造成的
叙述风格、人物对白、术语和章节功能漂移。

小说提供 `--outline` 或 `--context` 后，人物目标、知识、关系、边界、能力和说话方式才作为
权威设定参与审查；没有大纲时不会把临时推断冒充人物正史。新闻、论文、公文和报告则按
术语、事实、归因、结论范围与章节功能统一，不加载小说专用规则。

```powershell
human-writing-skills chunk-audit --draft full-novel.md --style fiction --outline novel-outline.md --output-dir novel-audit
human-writing-skills chunk-audit --draft full-novel.md --style fiction --outline novel-outline.md --book-level --output-dir book-audit
```

搜索关键词：**长篇审查、分块审查、文风统一、统一文风、人物设定统一、人物一致性审查、
跨章一致性、小说审查、报告审查、长文上下文一致性**。详见
[长篇分块审查指南](docs/long-form-consistency.zh-CN.md)。

## AI 式结尾与生硬结尾审查

AI 小说常在场景已经完成后，再补一段风景渐隐、众人沉默、人物反思、人生感悟或
“未来仍将继续”的总结。这类尾句看似圆润，实际没有新增选择、事实、后果或压力，
属于**伪收束、反思式尾句或无意义升华**。`earned-ending-audit` 会先定位“最后一个
有效变化”，再做删除测试；它不会把夕阳、沉默、感悟或抒情文字本身列为禁词。

- 小说和网文应停在已经赚到的后果、决定、发现、物件变化、未解压力，或在本场景中
  真正改变了意义的意象上。
- 硬新闻停在最后一个有用且可核实的事实、回应、限制或下一步；特写式结尾只有在
  新增意义时才保留，不能为了“有余味”强行拔高。
- 论文、技术报告和公文停在有依据的结论、局限、影响、决定、责任人或期限上，
  不套小说式抒情，也不补仪式化总结。

```powershell
human-writing-skills audit --draft chapter.md --document-type fiction --profile ending
human-writing-skills lint --draft chapter.md --style fiction
```

完整模块只在显式选择 `ending` 时加载；日常扫描、`ai-trace` 和完整审查由轻量级
`END001` 负责。搜索关键词：**AI小说结尾、AI式结尾、生硬结尾审查、场景结尾审查、
章节结尾审查、反思式结尾、总结式尾句、伪收束、无意义升华、去AI味结尾**。

## 重复回声、解释性旁白与场景经济性

有些稿子没有明显套话，读起来却仍然像模型生成：同一句、同一个意象、同一套动作或
同一个旁白结论被换词重播，场景并没有新增后果。叙事专用的
`repetition-exposition-audit` 会区分有意义的复沓、必要前情回顾与无效重复，审查逐字
回声、动作编排循环、平均扫视式细节清单，以及对台词/动作已表达内容的重复解释。

```powershell
# 独立且 token 受控的叙事审查
human-writing-skills audit --draft chapter.md --document-type fiction --profile repetition

# 长稿只在匹配到叙事信号时加入这一阶段
human-writing-skills pipeline --draft chapter.md --lint-style fiction --auto --output-dir chapter-audit
```

`REP001` 定位非短句的逐字回声；`NAT005`、`NAT006` 以低风险提示解释性旁白和
动作框架的高密度复现。它们是编辑证据，不是作者身份判断，也可用 allowlist 放行。
快速 humanize 与严肃文本流程不会加载这个模块。

## 这个项目解决什么

| 常见问题 | 项目提供的办法 |
| --- | --- |
| 文字空泛、对称、像模板 | 用具体的修订检查项压掉套话和泛泛表达 |
| 反复“不是……是……”“是……不是……”或“比……比……” | 检查句式家族与复现密度，保留必要纠错和真实比较，重写装饰性框架 |
| 改写时悄悄改变事实、语气强度、不确定性或因果 | 仅在提供原文时启用语义保真账本与新增细节检查 |
| 去AI味时把迟疑、意象、潜台词和人物口吻一起洗掉 | 对照原文保护有作用的含混、重复、母题和说话标记 |
| 句子表面流畅却漏字、漏宾语或连接成分 | 用句法槽位、并列对称和指代回查做独立终校 |
| 模糊归因、意义拔高、假范围、同义词轮换和排版套路反复出现 | 按文体和密度审查表层模式，不搞全局禁词 |
| 小说被“下午”“某地”“新的决定”等小标题切碎 | 只对叙事文体检查，保留作品名和章节名，要求用正文完成场景过渡 |
| 场景已经结束，又补风景、沉默、感悟或未来展望 | 定位最后一个有效变化，用删除测试清理伪收束，并按文体选择真正有功能的结尾 |
| 同一动作、反应或旁白反复重播，场景像在原地打转 | 仅叙事文体检查逐字回声、动作编排循环、平均扫视和冗余解释 |
| 不同文体都写成一种味道 | 为不同文体提供独立 `SKILLS` |
| 长文本容易忘记剧情和设定 | 使用轻量级 ledger 记录人物、规则、伏笔和状态 |
| 数月或一年间文风、人物对白因模型或提示词变化而漂移 | `chunk-audit` 用固定基准、大纲和唯一正文分块做跨块审查与文风统一 |
| 人物对白像同一个人或不合当下身份 | 按人物基线、谈话目的、知识边界、听众和压力生成并审核 |
| 台词后只接万能动作、风景或旁白，人物之间没有真正交接 | 对话表现审查核对听者承接、动作功能、状态变化和延迟回应 |
| 人物方言、敬语、语气词或外语突然串台 | 建立语言身份卡，按经历、听众和变调依据审核，不按地域或国籍刻板分配口音 |
| 关键台词或动作后无人承接，剧情生硬切走 | 检查回应义务，并把延迟回应记录为互动欠账 |
| 时代、技术、制度或世界规则互相冲突 | 抽取世界契约，再检查物件、行动和例外是否兼容 |
| 战力、技能、权限、装备、伤势和资源前后漂移 | 区分永久基线与临时状态，要求升级、损耗、克制和例外都有过程门与代价 |
| 调查、谈判、研发等过程被跳过，结果凭空成功 | 检查承诺、尝试、阻力、判断、代价和结果的赚取链 |
| 扩写只增加环境、心理和同义复述 | 比较场景承诺与注意力分配，把篇幅还给关键过程和后果 |
| 提示词越写越乱 | 用 CLI 把文体、上下文、任务编译成清晰指令包 |
| “像人写的”太抽象 | 把自然感拆成节奏、细节、转场、视角、证据等可执行规则 |

## 已内置的基础文体 SKILLS

| Skill | 适合场景 | 重点 |
| --- | --- | --- |
| `fiction` | 小说/故事 | 视角、人物行为、场景压力 |
| `argumentative` | 议论文/观点文 | 论点、证据、反驳、逻辑推进 |
| `news-report` | 新闻报告 | 事实顺序、消息来源、克制表达 |
| `self-media` | 自媒体文章 | 有用、直接、有个人判断，但不空喊口号 |
| `academic-paper` | 科研论文 | 谨慎表述、结构、术语一致性 |
| `formal-document` | 公文/正式文件 | 权责、依据、范围、动作、期限和克制语域 |
| `webnovel` | 网络小说/连载文 | 爽点、钩子、伏笔回收、战力和设定连续性 |

## 深层“人类痕迹”模块

这些模块不是做表面替换，而是处理更深的 AI 写作痕迹。

| Module | 修复什么 |
| --- | --- |
| `controlled-drift` | 逻辑过度顺滑、缺少联想跳跃、没有未完成思考 |
| `narrative-bridges` | 场景转折弱、万能转场多、段落之间没有因果和压力传递 |
| `relationship-state` | 人物关系重置、对白没有主动权变化、秘密和边界被遗忘 |
| `relationship-stance-audit` | 检查“谁在谁面前提谁”：敌对、多角、阵营、上下级、掌门/家族等关系立场错误 |
| `logic-causality-audit` | 检查因果、时间线、知识来源、动机、规则、资源和后果断裂 |
| `character-consistency-audit` | 检查人物目标、声音、能力、边界、知识和转变是否有过渡 |
| `dialogue-voice-audit` | 按人物基线与情境生成并审核对白，检查关键回合是否得到语言、动作、沉默或延迟回应 |
| `dialogue-performance-audit` | 复用对白模块的回应图，检查动作是否真正改变互动，而不是万能动作或风景垫句 |
| `speech-register-continuity` | 有明确证据时检查人物语言、方言经历、敬语、语气词、称谓和切换依据 |
| `capability-state-audit` | 检查战力、技能、权限、装备、伤势、资源、冷却、克制与变化过程 |
| `serial-reentry` | 有前章或账本时，检查前情倾倒、遗漏承接和章节状态重置 |
| `long-form-style-consistency` | 长篇分块审查、跨时段文风统一、人物设定与对白声音的跨块校验 |
| `chapter-momentum-audit` | 检查只铺气氛不推进、承诺未兑现、章间残留丢失和无依据钩子 |
| `world-ontology-audit` | 检查时代、技术、制度、社会习惯和架空规则是否兼容 |
| `process-earnedness-audit` | 检查关键结果是否由选择、阻力、证据和代价赚到 |
| `attention-budget-audit` | 检查低价值描写、语义回声和无状态变化扩写是否挤占核心内容 |
| `chapter-pattern-audit` | 对三章以上提取结构指纹，识别重复开场、转折、情绪峰值和钩子模板 |
| `narrative-distance-control` | 检查无动机拉近镜头、缺少场景定位和叙事距离漂移 |
| `imagery-load-audit` | 检查比喻堆叠、感官争抢和展示动作后重复解释情绪 |
| `paragraph-rhythm-audit` | 检查机械单行段落连发和塞入过多转折的长段 |
| `detail-disclosure-audit` | 检查人物履历、身材和外貌在剧情使用前集中倾倒 |
| `scene-entry-audit` | 检查精确时间、地点、光线天气、全套穿着和概括情绪同时挤在开场 |
| `natural-measurement` | 虚假精确：小说里不合语境的微小精确量化和机械计数 |
| `cliche-phrase-audit` | 论坛常吐槽的塑料套话、万能身体动作、空洞情绪标签和死转场 |
| `formulaic-structure-audit` | 过于整齐的三连式、双向“不是/是”对举、连续“比”比较和每段干净收束 |
| `prose-progress-audit` | 段落没有新增状态，或关键台词/动作尚未被接收就切换话题与场景 |
| `narrative-naturalness-audit` | 只在深度/显式 AI 痕迹审查中检查六拍以上反复出现的场景配方与开场/收束节拍 |
| `repetition-exposition-audit` | 仅叙事文体检查逐字回声、动作编排循环、平均扫视与冗余解释性旁白 |
| `earned-ending-audit` | 检查反思式尾句、风景渐隐、伪收束、套路 kicker 和最后有效变化之后的无意义升华 |
| `imperfect-prose` | 文字太干净、太对称、太像统一润色 |
| `vocal-rhythm` | 朗读时节奏单调、缺少呼吸点 |
| `embodied-emotion` | 只有情绪标签，没有身体、动作、矛盾和感知 |
| `cultural-anchors` | 文本像发生在真空里，没有时代、地域、社群和物质细节 |
| `spatial-blocking` | 防止车内、房间、电梯等狭小空间里人物瞬移 |
| `occupancy-capacity` | 检查座位、长椅、床、板凳、过道等物理资源是否超容量或形态不明 |
| `appearance-prop-continuity` | 防止服装、鞋子、道具、伤口等日常细节漂移 |
| `physical-continuity-audit` | 可选的轻量人工清单；不要与法医式物理 Profile 同时使用 |
| `proofreading-audit` | 最后检查错漏字、谓词必需成分、悬空连接词、指代、标点、称谓和排版 |
| `style-matrix` | 避免把一种“人类口吻”套到所有文体上 |
| `editor-loop` | 建立挑剔编辑式的审查与局部重写流程 |
| `ai-trace-rubric` | 把“还像 AI”拆成可诊断、可修复的维度 |
| `reference-style-alignment` | 只在明确提供参考资料或文风要求时，提炼可迁移的声音与写法，不复制内容 |
| `rewrite-fidelity` | 提供原文时检查意义漂移、凭空具体化、正反颠倒和不确定性变化 |
| `voice-ambiguity-preservation` | 防止过度清洗抹掉有意义的含混、重复、意象、迟疑、潜台词和人物口吻 |
| `humanize-examples` | 仅在明确要求时加载的改写前后示例库，不作为事实来源或默认范文 |
| `surface-pattern-audit` | 按文体审查表层格式、假范围、词汇轮换和叙事小标题，但不全局封禁句式 |
| `protected-content` | 防止润色时误改数字、引文、公式、链接、代码、原话和指定术语 |
| `source-grounding` | 严肃文本有明确来源时，核对主张、出处、适用范围和不确定性 |

## 快速开始

```powershell
git clone https://github.com/whh110112/human-writing-skills.git
cd human-writing-skills
python -m pip install .

human-writing-skills list --kind style
human-writing-skills list --kind module
human-writing-skills build --style webnovel --context examples/story-ledger.md --task "续写第三章，保留冲突但揭示一个新线索。"
human-writing-skills humanize --draft chapter.md --style fiction --mode quick
human-writing-skills chunk-audit --draft full-novel.md --style fiction --outline novel-outline.md --output-dir novel-audit
human-writing-skills lint --draft chapter.md --style fiction
human-writing-skills verify --source original.md --candidate revised.md
```

也可以不安装，继续使用 `python -m humanwriting.cli ...`。`build` 和 `humanize` 会输出一份可以直接复制给 Codex、ChatGPT、Claude、本地大模型或其他写作代理的指令包。

## 快捷 Humanize

`humanize` 是低门槛改写入口。它把 `--draft` 同时视为待改写原文，默认保持原语言、
文体、事实和意义，再处理模板腔与机械结构。

```powershell
# 最小组合：表层模式 + 原意保真 + 声音/含混保护
human-writing-skills humanize --draft chapter.md --style fiction

# 只有结构问题较重时才增加深度编辑模块
human-writing-skills humanize --draft article.md --style self-media --mode deep

# 示例库保持显式加载，不作为事实或文风来源
human-writing-skills humanize --draft chapter.md --style fiction --with-examples
```

`quick` 不加载套话、公式结构、段落推进和编辑循环；`deep` 才追加这些高成本模块。
`humanize-examples` 只有传入 `--with-examples` 才加载；`voice-ambiguity-preservation`
只用于有原文的改写或显式 preservation 审查。

## 多语言范围

法语、西语、葡语、日语和阿语的严肃文体自动识别现在要求组合线索；线索不足
时可显式指定 `--document-type`。非中英语言的 `stats` 只展示描述性统计，
不把统一阈值冒充经过各语种标定的判断。

技能指令没有中文限定，可以用于模型所支持的英文、日文、法文、西班牙文、
葡萄牙文、阿拉伯文、拉丁文及其他语言的小说和严肃写作。确定性词汇规则天然会
受语言影响，但连续性、物理状态、人物关系、场景衔接和大部分审稿标准与语言无关。
叙事标题扫描已经覆盖上述语言的常见时间卡，`stats` 也能区分汉字、假名、阿拉伯
文字和多种拉丁字母语言。混合语言或低资源语言仍应结合文体和人工复核。

## 指令包长什么样

```text
# Core Directive
# Continuity Protocol
# Selected Skill: webnovel
# Project Context
# Task
# Output Contract
```

它会把通用写作原则、长上下文协议、选中的文体技能、项目设定和本次任务放在一起，让 AI 不只是“知道主题”，还知道前文承诺了什么、哪些设定不能改、下一段必须从哪里接上。

## 明确触发的参考文风

参考文风模块默认关闭。只有传入 `--reference`、传入 `--reference-style`，或任务
中明确出现“参考/贴近/沿用某种文风”等要求时才激活。单独传入剧情账本或前文
章节作为 `--context` 不会误触发。

```powershell
human-writing-skills build `
  --style fiction `
  --context examples/story-ledger.md `
  --reference examples/reference-style-source.zh-CN.md `
  --task "续写下一场，贴近参考材料的克制节奏。"

human-writing-skills audit `
  --draft my-chapter.md `
  --reference examples/reference-style-source.zh-CN.md `
  --profile style-match
```

模块会提炼视角、句长节奏、词汇层级、意象密度、场景和人物描写方法、对白
节拍、情绪表达和转场方式。剧情事实仍以 `--context` 为准，不得复制参考资料的
人名、事件或标志性句子。详见 [docs/reference-style.zh-CN.md](docs/reference-style.zh-CN.md)。

## 原文改写保真

原有 `verify` 只核对数字、引文等字面内容。重要改写还应运行
`verify-fidelity --source original.md --candidate revised.md`：它会标出改动
的主张片段及主体、否定、可能性、范围、归因变化线索。只要正文改动就标为
**需逐条复核**，不会把“数字相同”误判为语义已通过。退出码 0=原样一致，
1=字面内容变化，2=改写后需审稿。

只有改写现有文字并且必须保持原意时才传入 `--original`。它会为生成或审稿单独
加载语义保真模块；普通创作不会承担这部分 Token。

```powershell
human-writing-skills build `
  --style self-media `
  --original original.md `
  --task "在不增加事实、不强化结论的前提下改得更清楚。"

human-writing-skills audit `
  --draft revised.md `
  --original original.md `
  --profile fidelity
```

`--original` 是改写语义依据，`--reference` 只提供文风依据，`--source` 只为严肃
文本提供事实证据。三种材料隔离加载，避免范文改写事实，也避免原文被误当成模仿
目标。详见 [docs/editing-tools.zh-CN.md](docs/editing-tools.zh-CN.md)。

## 多语言质量评测

仓库内置种子样例，可检查文体误报/漏报和改写保真分流：

```powershell
human-writing-skills evaluate --cases tests/fixtures/quality/multilingual-benchmark.json
```

**种子样例通过不等于母语盲审准确率。**经独立审稿人标注的样例单独计数，
并按语言和文体报告结果。流程见[质量评测指南](docs/evaluation.zh-CN.md)。

## 严肃文本来源依据

`--source` 与 `--reference` 完全分离。它只在论文、新闻、法律或技术文本中
激活 `source-grounding`，建立“主张 -> 来源位置 -> 支持范围 -> 结论”的证据表。
小说、网文、自媒体和普通问答不会自动加载。

```powershell
human-writing-skills audit `
  --draft paper.md `
  --document-type academic-paper `
  --source study-a.md `
  --source study-b.md `
  --profile sources
```

来源核验会区分“文献存在”和“文献支持当前结论”。没有外部数据库访问时，只会
把 DOI、标准、判例或元数据标为待核验，不会猜测真实性。

## 长文本连续性方案

长篇小说、网文、系列文章最容易出问题的地方，不是单句写不好，而是写着写着忘了：

- 人物关系变过没有
- 伤势、代价、能力限制还在不在
- 某个伏笔是否已经揭示
- 论证前后有没有自相矛盾
- 上一段结束时人物到底在哪里

因此项目使用轻量级 ledger 记录，并按“权威账本 -> 最新状态 -> 近期章节 ->
相关旧片段 -> 明示为不确定的推断”取用上下文。检索出来的旧段落只负责召回，不能
覆盖后续已经确认的新状态：

- 固定事实：人物、时间线、地点、关系、规则
- 活跃线索：未解决冲突、悬念、伏笔、论点
- 关系状态：谁知道、想要、隐瞒、亏欠、拒绝了什么，谁握有主动权
- 关系立场：公开/私下态度、当前听众、谁能在谁面前提谁、禁泄秘密和例外动机
- 声音锚点：叙述视角、用词、直接程度、披露习惯、知识边界、听众变化和禁用表达
- 语言身份：共同场景语言、已证明的方言/外语经历、敬语称谓、语气词与变调依据
- 能力状态：永久战力/技能/权限与临时伤势、装备、资源、冷却、克制、代价和变化门
- 对话契约：谁对谁说、为何现在说、想让对方做什么、不能透露什么、这轮要改变什么
- 互动欠账：哪句关键台词或动作仍待回应、拒绝、打断、后果或延迟回收
- 当前状态：上一段结束在哪里，下一段必须如何衔接
- 节拍桥：上一拍留下什么、下一拍为什么开始、中间发生什么微转折、结尾留下什么压力
- 新增事实：本次输出后哪些事情变成了真

示例见：[examples/story-ledger.md](examples/story-ledger.md)

`speech-register-continuity` 只有小说/网文存在对白，并且任务或账本明确给出地域、
语言、方言、敬语或语域证据时才自动加载；也可用 `audit --profile register` 单独审查。
它不会因为人物的地域或国籍就凭空给出某种口音。

`capability-state-audit` 在生成时只由本次任务中的战力/技能/资源等要求触发；流水线
自动审查还要求提供上下文账本。普通文戏不会加载。可显式使用
`audit --profile capability --context ledger.md`。

## Chatbox 使用

可以在 Chatbox 里用。这个项目生成的是纯文本指令包，不需要插件。长篇写作时，把 continuity ledger 当成上下文来源，并把编译后的指令包粘贴到 Chatbox 的 system prompt 或新会话第一条消息。

- 中文指南：[docs/chatbox.zh-CN.md](docs/chatbox.zh-CN.md)
- 英文指南：[docs/chatbox.md](docs/chatbox.md)
- 账本模板：[examples/chatbox-ledger-template.md](examples/chatbox-ledger-template.md)

## 物理连续性

如果写车内、房间、电梯、餐桌、病房等空间关系很重要的场景，使用 `--strict-continuity`。它会自动加入容量、空间调度、服装道具等生成约束；成稿法医式物理审查由 `audit --profile physical` 单独负责，在一张证据账本里统一判断容量、站位、服装、道具、障碍、触达和身体状态。

```powershell
python -m humanwriting.cli build `
  --style fiction `
  --strict-continuity `
  --review `
  --context examples/vehicle-scene-ledger.md `
  --task "续写车内争执。任何座位变化都必须写出动作过渡，保持服装和道具状态一致。"
```

- 说明：[docs/physical-continuity.zh-CN.md](docs/physical-continuity.zh-CN.md)
- 车辆场景账本：[examples/vehicle-scene-ledger.md](examples/vehicle-scene-ledger.md)
- 容量账本模板：[examples/capacity-ledger-template.md](examples/capacity-ledger-template.md)
- 容量冲突示例：[examples/capacity-conflict-draft.zh-CN.md](examples/capacity-conflict-draft.zh-CN.md)
- 成稿审查示例：[examples/problem-car-scene-draft.zh-CN.md](examples/problem-car-scene-draft.zh-CN.md)

## 关系立场连续性

如果对话涉及敌对关系、多角关系、门派/家族/公司阵营、上下级或秘密关系，使用 `--deep-review` 或显式加入 `relationship-stance-audit`。它会把每句对话抽成“说话人 -> 听话人/在场观众 -> 被提及第三方”，检查是否存在无动机的夸敌人、骂盟友、泄露隐藏关系、称谓错位或信息权限错误。

- 说明：[docs/relationship-stance-continuity.zh-CN.md](docs/relationship-stance-continuity.zh-CN.md)
- 关系账本模板：[examples/relationship-stance-ledger.zh-CN.md](examples/relationship-stance-ledger.zh-CN.md)

## 人物与情境对白

**双向互动承接审查：修复人物没有反应、动作悬空与回应缺失。** 审查同时覆盖对白和无声动作，
也包括第一人称叙述者自身的反应。按“发起者 → 受影响的人 → 言语/动作 → 接收依据 → 已完成或待回应状态”
检查：一句口头回复可能只回答问题，没有完成同时发出的动作；发起者移动，也不能默认别人已经跟上。
每个需要配合、注意或状态变化的互动都要有依据，拒绝、没察觉、停留、沉默和延迟回应也可以成立。
已有含蓄承接无需重复补写；不会强制每句台词添加动作、表情或感想。

基础小说/网文 Skill 保留简短承接规则，专项复用 `voice`，按需激活。
`pipeline --auto` 和长篇深度审查也识别有明确对象的人际动作；显式 `--profile voice` 可覆盖
自动线索没有识别的语言或表达。分块末尾尚待下文确认的回应交给统稿核对，不直接算漏写。
这些是模型执行的语境审核；规则扫描的命中不能替代逐段阅读，也不保证模型每次都执行完整。

`dialogue-voice-audit` 与 `dialogue-performance-audit` 把对白拆成四层：人物长期语言基线、当前场景对基线的
调制、每句话试图完成的行动，以及听者承接后的状态变化。职业、阶层、地域和性格标签只能提供知识、
利益、责任与语域变化线索，不能直接替代人物性格。生成时明确要求言语或人际动作场景
即可按需激活；已有稿件使用独立 `voice` 审稿：

```powershell
human-writing-skills audit `
  --draft my-dialogue-scene.md `
  --context my-novel-ledger.md `
  --profile voice
```

审核会区分“设定冲突”和“有动机的反差”，并检查谈话目的、知识边界、现实约束、
上一句回应、听众与权力关系。关键台词或动作不要求机械地回一句话，但在转场前
必须有语言、动作、可读的沉默、明确打断或延迟回应；否则会标记为互动回合悬空。
动作、触碰、道具、距离、停顿、服装和风景只有改变注意力、权限、关系、可达性或
下一步选择时才保留，不会强制给每句台词添加“低声”“一笑”“转身”之类的装饰。

如果已经有一段文本需要审稿，使用 `audit`：

```powershell
python -m humanwriting.cli audit `
  --draft examples/problem-car-scene-draft.zh-CN.md `
  --context examples/vehicle-scene-ledger.md
```

## 项目结构

```text
humanwriting/        Python 包和 CLI
skills/              可复用 Markdown 写作 SKILLS
examples/            剧情账本、文章 brief 示例
tests/               标准库单元测试
```

## 常用命令

### 按需叙事模块

新增能力采用渐进加载。生成任务只有明确要求对话、谈判、会谈、审问、争论、重逢、
试探、安慰、和解、对峙等言语场景，或检测到有明确对象的人际动作时，才自动加入对白模块；独处叙述
和严肃文体不会误触发。
审稿中的 `voice`、`register`、`capability`、`serial`、`world`、`process`、`momentum`、`salience`、
`recurrence`、`repetition`、`texture`、`sources`、`preservation` 仍不塞入宽覆盖的 `full`：

```powershell
human-writing-skills build --style fiction --task "写一场两位角色各有所求的谈判。"
human-writing-skills build --style webnovel --context ledger.md --module serial-reentry --task "续写第18章。"
human-writing-skills audit --draft chapters.md --profile momentum
human-writing-skills audit --draft chapter.md --profile texture
human-writing-skills audit --draft chapter.md --profile process
human-writing-skills audit --draft chapters.md --profile recurrence
```

对白模块不按职业套口吻，而是检查稳定语言基线、现实利益、知识边界、当场目标、回应
关系和有功能的动作落点。`dialogue-voice-audit` 独占“回应义务/互动债务”，`dialogue-performance-audit` 只检查已选动作是否有互动功能；语言身份、语气词、敬语与变调依据交给
`speech-register-continuity`，战力与资源状态交给 `capability-state-audit`。
`serial-reentry` 只有提供前章或账本
时才可使用；`momentum` 只审多章稿件的入场压力、变化、回报和章尾承接；`texture`
负责电影式开场堆料、叙事距离、比喻与感官负载、单行段落成串、动作后重复解释
情绪以及人物资料倾倒。`world` 只在明确世界坐标出现时检查兼容性；`process`
检查关键结果是否由过程赚到；`salience` 只对长稿检查注意力预算；`recurrence`
至少需要三章；`repetition` 只在足够长且出现重复解释/动作信号的叙事稿中加入；`sources`
需要严肃文体和明确来源文件。

生成时，`world`、`process` 和 `attention-budget-audit` 也只会分别在任务出现明确
世界设定、关键过程、扩写/长稿/灌水审查信号时加入，不随普通 `--deep-review` 加载。

### 审稿 Profile

`audit` 可以只加载当前需要的审查规则，避免无关模块干扰结果：

| Profile | 用途 |
| --- | --- |
| `full` | 宽覆盖默认审稿；高成本与强条件 Profile 保持独立 |
| `logic` | 因果、时间线、知识、动机、规则、资源与后果 |
| `character` | 人物目标、声音、能力、边界和变化桥梁 |
| `voice` | 人物基线、谈话目的、知识/角色约束、听众语域、变调依据和回应义务 |
| `register` | 语言身份、方言经历、敬语称谓、语气词、词汇与切换依据 |
| `capability` | 战力、技能、权限、装备、伤势、资源、克制与变化门；必须提供 `--context` |
| `serial` | 前情倾倒、遗漏承接和章节重置；必须提供 `--context` |
| `momentum` | 多章稿件的入场压力、不可逆变化、承诺回报、残留和章尾压力 |
| `world` | 时代、技术、制度、社会习惯和世界规则兼容性 |
| `process` | 承诺、尝试、阻力、判断、代价、证据与结果的赚取链 |
| `salience` | 长稿注意力分配、低价值扩写和跨段语义回声 |
| `recurrence` | 三章以上的章节结构指纹和模板复读 |
| `repetition` | 仅叙事文体检查逐字回声、动作框架复现和重复解释可见信息 |
| `texture` | 叙事距离、场景入场负载、意象、段落节拍和资料投放 |
| `physical` | 座位、空间、容量、触达、服装、道具和伤势 |
| `relationship` | 关系立场、当前听众、信息权限、称谓和秘密泄露 |
| `ai-trace` | 套话、公式结构、段落无推进和其他 AI 痕迹 |
| `ending` | 最后有效变化、反思式尾句、伪收束和不同文体的结尾功能 |
| `numbers` | 动作与情绪中的假精确数字 |
| `proofread` | 错漏字、句法槽位、悬空连接词、指代、标点、称谓和排版 |
| `fidelity` | 原意、实体、正反、不确定性、时间顺序、归因和新增细节；必须提供 `--original` |
| `preservation` | 有意义的含混、重复、母题、迟疑、潜台词和人物口吻；必须提供 `--original` 并显式选择 |
| `style-match` | 对照明确输入的参考资料检查文风漂移；没有参考信号时不可使用 |
| `sources` | 对照明确来源核验严肃文本主张；需要 `--source` 和严肃文体 |

Profile 可以重复组合，例如 `--profile relationship --profile ai-trace`。

普通生成只加载一句轻量句法完整性检查。完整的漏字、缺宾语、悬空连接词和指代审查仅在
`proofread` 或流水线校对阶段加载，避免长期占用生成 Token。

### 长篇分块审查与文风统一

当稿件远超单次上下文，或前后内容由不同模型版本、不同提示词、不同时间写成时，先用
`chunk-audit` 建立稳定基准，再分块检查。它和 `pipeline` 不重复：`chunk-audit` 解决“全文
太长”和“跨块漂移”，`pipeline` 解决“同一稿件不要一次检查所有问题”。二者可串联使用。

```powershell
human-writing-skills chunk-audit `
  --draft full-novel.md `
  --style fiction `
  --outline novel-outline.md `
  --reference approved-sample.md `
  --output-dir novel-consistency-audit
```

没有明确参考样文时，`--baseline-chunk` 只是候选基准，先在基准提取阶段确认或纠正；`--reference` 不会
被当作剧情事实。小说人物设定由大纲/账本约束并允许有依据的成长，严肃报告则保护事实、
数字、术语、归因和结论范围。默认每块约 8000 字符，大纲与基准均有独立预算，避免全量激活。

### 长文 Agent 覆盖审查

当需要确保全文没有被模型草草跳过时，显式加 `--agent-mode deep`。它会写入
`agent-plan.json` 任务图，要求每个审查任务提交 Coverage Receipt，并在 `reports/` 下规定
报告落点。基准报告确认后，所有只依赖 `baseline` 的任务可在不同的新会话或独立 API 请求中并行运行。

```powershell
human-writing-skills chunk-audit `
  --draft full-novel.md `
  --style fiction `
  --outline novel-outline.md `
  --agent-mode deep `
  --output-dir novel-agent-audit

human-writing-skills verify-chunk-audit `
  --package-dir novel-agent-audit
```

只有覆盖验证通过后，才运行 `9999-reconcile-prompt.md`。深度模式会为每块增加逐段文风审查；
仅在含对白或人际动作线索的块增加互动审查；仅在提供 `--source` 的严肃文本中增加事实证据审查。普通
`standard` 模式仍是每个唯一正文块一个完整审查任务。对明确的翻译或本地化长文可加
`--translationese`；它不会因为正文使用西语、葡语、法语或其他语言就自动激活。

- 详细说明：[docs/long-form-consistency.zh-CN.md](docs/long-form-consistency.zh-CN.md)

### 多阶段流水线

需要高精度审稿时，不必让一个模型一次检查所有问题。`pipeline` 会为同一稿件生成多份职责独立的提示词：

```powershell
human-writing-skills pipeline `
  --draft my-chapter.md `
  --context my-novel-ledger.md `
  --auto `
  --output-dir chapter-audit
```

每个阶段应放到新的模型会话或独立 API 请求运行。自动模式会保留逻辑、AI 痕迹和校对，再按人物、关系、空间、精确数字、持续对白、语言语域、战力状态、世界坐标、关键过程、稿件长度和多章结构追加专项阶段。`serial` 与 `capability` 需要账本；`fidelity` 需要原文；`salience` 只处理至少 4000 字符且段落充分的长叙事；`recurrence` 至少需要三章；`repetition` 只处理足够长且出现重复解释或动作框架信号的叙事稿；`sources` 只有来源文件与严肃文体同时成立才加载。高成本的 `preservation` 不自动加入，使用 `--stage preservation --original original.md` 显式运行。只有需要统计诊断时再加 `--with-stats`。清单会说明每项选择和跳过原因。

- 详细说明：[docs/audit-pipeline.zh-CN.md](docs/audit-pipeline.zh-CN.md)

### 确定性保护工具

`lint` 会给出规则编号、行列和原文证据；`stats` 提供可选的分布统计；`fix`
只预览保守的机械修复；`verify` 会比较改写前后受保护的数字、引文、公式、链接、
代码和术语。分数与统计只是透明的编辑启发式，不是 AI 作者身份鉴定。

内容保护只对论文、公文、新闻以及具有充分证据的法律/技术文档自动加载。小说、网文、
普通问答、搞怪文本和自媒体默认不加载；需要例外时使用 `--protect-content` 或
`--protect-term` 明确开启。

使用 `--style fiction` 或 `--style webnovel` 时，`lint` 还会检查未要求的叙事小标题
和多语言独立时间卡。作品名、章节名不会误报，新闻与论文的结构标题也不受影响。
修复要求补回自然的正文过渡，而不是删掉“下午”后把两个断裂段落硬接起来。

```powershell
human-writing-skills lint --draft my-chapter.md --style fiction
human-writing-skills stats --draft my-chapter.md --style fiction
human-writing-skills fix --draft my-chapter.md --preview
human-writing-skills verify --source original.md --candidate revised.md --protect-term "星港计划"
```

- 痕迹扫描：[docs/pattern-linter.zh-CN.md](docs/pattern-linter.zh-CN.md)
- 改写保真、统计和保守修复：[docs/editing-tools.zh-CN.md](docs/editing-tools.zh-CN.md)
- 内容保护：[docs/protected-content.zh-CN.md](docs/protected-content.zh-CN.md)

### 数字必要性审查

用于处理“人物动作和情绪里不自然的 1 厘米、3 厘米、7 秒”等假精确感，同时保留建筑高度、伤口鉴定、工程参数、新闻事实等必要数字。

```powershell
python -m humanwriting.cli audit `
  --draft examples/false-precision-draft.zh-CN.md `
  --profile numbers
```

- 说明：[docs/number-sense.zh-CN.md](docs/number-sense.zh-CN.md)
- 示例：[examples/false-precision-draft.zh-CN.md](examples/false-precision-draft.zh-CN.md)

### 常见写作问题审查

本项目把长文本中反复出现的问题整理成可执行审查项：套话、塑料感、三连式结构、过度顺滑、段落无推进、空情绪、万能转场、文化真空和长文漂移。

- 规则映射：[docs/forum-complaint-research.zh-CN.md](docs/forum-complaint-research.zh-CN.md)

列出所有文体：

```powershell
python -m humanwriting.cli list
```

生成指令包：

```powershell
python -m humanwriting.cli build `
  --style fiction `
  --module controlled-drift `
  --module narrative-bridges `
  --module relationship-state `
  --module natural-measurement `
  --module embodied-emotion `
  --module vocal-rhythm `
  --strict-continuity `
  --review `
  --context examples/story-ledger.md `
  --task "写下一场戏，保持林乔的听觉代价设定，不要提前解决冲突。"
```

`--review` 是长文友好的精简审查，只自动加入：

- `editor-loop`：先生成，再以挑剔编辑视角诊断，局部重写，最后定稿
- `ai-trace-rubric`：从认知平滑、表达泛化、情感平面、节奏单调、上下文漂移、节拍桥薄弱、关系重置、虚假精确、文化真空、过度干净、结论成瘾等维度评分

`--deep-review` 会在精简审查上加入：

- `relationship-stance-audit`：检查说话人、听话人、被提及第三方之间的关系立场、秘密和信息权限
- `cliche-phrase-audit`：检查高频套话、塑料身体动作、空洞情绪标签和万能转场
- `formulaic-structure-audit`：检查三连式、双向对举、连续“比”比较和每段都收束得太完整的公式结构
- `surface-pattern-audit`：按文体检查意义拔高、模糊归因、假范围、词汇轮换、排版套路和叙事小标题
- `prose-progress-audit`：检查每段是否真的推进了事实、关系、证据、动作或压力
- `narrative-naturalness-audit`：只在深度或显式 AI 痕迹审查中检查六拍以上重复的场景配方与开场/收束节拍；局部套话、结构和对白承接分别交给其主责模块；普通 quick 不加载
- `natural-measurement`：小说、网文和自媒体中检查不合语境的假精确数字

重复回声与解释性旁白属于成稿审查，不塞入普通生成提示词：使用 `audit --profile repetition`
或叙事 `ai-trace`；长稿则让 `pipeline --auto` 在命中相应信号后单独增加这一阶段。

`--strict-continuity` 会自动加入：

- `spatial-blocking`：座位、站位、前后左右、移动过渡检查
- `occupancy-capacity`：物理资源容量、形态、占用者和转换过渡检查
- `appearance-prop-continuity`：服装、鞋子、道具、伤口和身体状态检查

需要成稿物理状态矛盾审查时使用 `audit --profile physical`。`physical-continuity-audit` 只是轻量人工清单，不能与该法医式 Profile 同时使用。

运行测试：

```powershell
python -m unittest discover -s tests -v
```

## 写作理念

这个项目认为，“去 AI 味”不能只靠一句提示词。更可靠的做法是让模型持续遵守几类具体约束：

- 有现场：知道谁在说话、发生了什么变化、这一段为什么存在
- 有细节：用属于当前题材的具体材料，而不是万能句子
- 有连续性：尊重前文事实、伤势、代价、伏笔、论点和情绪变化
- 有文体：先理解小说、新闻、论文、自媒体的不同读者期待
- 有修订：删除空话、套话、万能转场和不必要的拔高

## 编辑边界

这个项目不承诺“完美隐藏作者身份”或“绕过检测器”。它关注的是写作工艺：声音、上下文、文体、修订和连续性。

如果要从出版物中提炼技法，请使用简短分析、公版文本、授权材料或自写示例。不要把受版权保护的大段原文复制进 skill。

## 贡献方向

欢迎贡献更多中文和英文写作技能，例如：

- 商业报告
- 法律文书
- 演讲稿
- 短视频脚本
- 产品文案
- 人物传记
- 悬疑、科幻、都市、玄幻等细分网文技能
- 不同模型的适配器和示例

请尽量写具体规则，不要只写“自然一点”“像人一点”。好的 `SKILL` 应该告诉模型：做什么、避开什么、如何衔接、怎样检查。

## 开源协议

MIT. 见 [LICENSE](LICENSE)。
