---
name: life-fork-simulation-stack
description: |
  Life Fork Simulation Stack / 人生岔路模拟栈。用于把任何“如果当年……”复盘问题，先拆成人生迁移语法：岔路动作、系统切换、自我叙事断裂、三种结果、事件冲击和可回收资产，再生成判词首屏、分叉图、三种结果卡、事件冲击卡和 30 天验证实验。适配 DeepSeek、OpenClaw 及其衍生实体，支持 sub-agent 并行，也支持普通对话顺序角色模拟。
---

# Life Fork Simulation Stack

中文名：人生岔路模拟栈

用户可见名：如果当年 / 人生岔路复盘

内部模块：决策 Bug Report

用人生迁移语法和多角色模拟框架，复盘一个人没走过的人生岔路；把个人处境、外部事件、具体场景、现实代价和决策盲点拆成一份可保存、可复看的用户报告。

本 Skill 面向 DeepSeek、OpenClaw 及其衍生实体设计。基础版只依赖对话和 Markdown；有 sub-agent、文件、脚本或浏览器能力时再增强交付形态。默认文件交付生成可保存、可浏览的 HTML 用户报告。

## 使用边界

- 做结构化复盘、隐性因素显影和决策系统校准。
- 前 2-3 轮优先建立用户画像，避免一上来要求用户填写长表。
- 假设结果必须使用概率性、条件性、情景化表达。
- 避免命理化、心理诊断、投资建议、法律建议、医疗建议。
- 避免替用户做重大决定。
- 避免承诺未来结果。
- 避免“准确还原人生”“命运推断”等包装。
- 默认不联网，不执行发帖、评论、登录、抓取私密内容等外部动作。
- 涉及高风险内容时读取 `references/safety-boundaries.md`。

## 多 Agent 运行方式

支持 sub-agent 的环境：

- 可并行运行人生叙事、职业路径、资产现金流、关系家庭、健康能量、时代事件等 Agent。
- 总控 Agent 汇总各 Agent 的分歧，保留冲突，不强行抹平。
- 汇总后交给反方审计 Agent 修正过度浪漫化、过度后悔和单一路径光环。
- 最后交给交付编辑 Agent 生成可保存、可复读、可继续追问的报告交付包。

普通对话环境：

- 按顺序模拟各 Agent。
- 每个 Agent 输出核心判断、最担心的风险、最支持哪条路径、需要反方审计的地方。
- 最终合并成一份报告。

详细角色定义见 `references/agent-simulation-stack.md`。

## 五种模式

### 模式 A：人生岔路模拟报告

触发词：

- 如果当年去了北京，会怎样
- 留学后如果没有回国，会怎样
- 如果当年进了体制，会怎样
- 如果没有离开上一家公司，会怎样
- 帮我复盘一条没走过的人生岔路

输入要求：

- 至少提供当年选择点、实际选择、想复盘的假设结果和当前困扰。
- 信息不足时先输出材料有限版，并列出 5 个补充问题。

内部生成检查：

- 语法识别：岔路动作、系统切换、自我叙事断裂、可回收资产
- 张力轴识别：2-3 个主张力轴和隐秘交换
- 原型识别：主原型、副原型、隐藏不甘、隐秘交换
- Magic Score：检查首屏判词命中、不可替换、隐秘交换和事件承托
- 反车轱辘检查：每个判断必须有年份或阶段、生活场景、现实代价、情绪代价、误判点和验证动作

用户可见输出：

- 判词
- 用户真正放不下的东西
- 三种结果：现实结果、假设结果、回补结果
- 每种结果给什么、拿走什么、最大陷阱
- 事件冲击卡：只选 4-6 张深卡，固定六段，包含事件锚点、生活场景、现实代价、情绪代价、误判点、今天验证
- 选择和时代拆分
- 30 天验证实验：按 4 周拆解，低风险、可执行、能获得现实反馈
- 源 Markdown 继续解释段：多角度判断、外部变化、材料缺口和决策边界
- HTML 用户界面：质量评分和修订记录隐藏，只展示人话折叠解释层

使用 `templates/life-fork-simulation-report.md`。

### 模式 B：人生选择沙盘

触发词：

- 我要不要跳槽 / 转岗 / 换城市 / 创业
- 重大选择前帮我做压力测试
- 帮我看几个选项的好情况和坏情况

输入要求：

- 正在发生的选择。
- 至少 2 个选项。
- 当前资源、约束、时间窗和最担心的坏情况。

输出结构：

- 选项拆解
- 好情况
- 坏情况
- 拖延情况
- 资源不足情况
- 不可逆点
- 最小验证动作

使用 `templates/choice-sandbox.md`。

### 模式 C：决策 Bug Report

触发词：

- 为什么我总在同一个地方卡住
- 为什么我总做相似错误选择
- 帮我分析这个决策 bug
- 为什么我总不发言 / 总被加活 / 工作不可见

输入要求：

- 一个反复出现的行为或判断模式。
- 最近一次发生场景。
- 用户想改变的点。

输出结构：

- 一句话判定
- 最近一次场景
- 重复出现的触发点
- 现实代价和情绪代价
- 可能误判
- 下次当场动作
- 长期补法
- 30 天验证实验

使用 `templates/bug-report.md`。

### 模式 D：多视角深度模拟

触发词：

- 我会给很多个人情况，帮我深度模拟
- 用多 Agent 跑一版
- 把个人情况、行业周期、家庭关系和现金流都加进去
- 做一个更可信的人生岔路模拟

输入要求：

- 尽量使用 `templates/intake.md`。
- 包含个人、职业、现金流、家庭、健康、性格、当年选择、外部环境等材料。
- 信息缺失时先跑材料有限版，再列 5 个关键补充问题。

输出结构：

- 多角色摘要
- 三种结果推演
- 外部事件冲击
- 反方审计修正
- 综合报告
- 报告交付包可选

使用：

- `references/agent-simulation-stack.md`
- `references/life-fork-grammar.md`
- `references/archetype-tension-axes.md`
- `references/life-archetype-library.md`
- `references/archetype-composer.md`
- `references/verdict-rewrite-patterns.md`
- `references/event-impact-framework.md`
- `references/event-shock-engine.md`
- `references/life-scene-library.md`
- `references/magic-score-rubric.md`
- `references/anti-generic-writing-rules.md`
- `templates/life-fork-simulation-report.md`

### 模式 E：报告交付包生成

触发词：

- 给我可保存版
- 输出 HTML 用户报告
- 给我用户版报告
- 把报告整理成最终交付
- 生成复盘清单和补充问题

输入要求：

- 一份人生岔路模拟报告，或用户原始输入。
- 用户指定交付形式：完整报告 / HTML 用户报告 / 复盘清单。

输出结构：

- 首屏只放报告名、用户问题、强判词和下滑提示。
- 第二屏放“人生分叉图”：一次选择，后来分出了三种结果，并在图下用一段人话解释怎么读图。
- 第三屏放三张结果卡，解释每种结果给什么、拿走什么、最大误判。
- 默认展开区保留：人生分叉图、三种结果卡、事件冲击卡、真正放不下什么、30 天验证实验。
- 事件冲击卡只选 4-6 张，每张合计 160-260 字，必须写具体时间、具体场景、现实代价、情绪代价、误判点和验证动作。
- 用户可见折叠层使用人话标题：你当年没算进去的事、哪些是你选的哪些是时代推的、我为什么会这样判断、换几个角度看这件事、那几年外部环境也在变、还有哪些信息会改写结论、这份报告不能替你决定什么。
- 质量评分和修订记录只保留在开发者草稿、日志或注释里。
- 4 周 30 天验证实验。
- 5 个补充问题
- HTML 用户报告可选

使用：

- `references/report-style-guide.md`
- `references/html-report-delivery.md`
- `templates/delivery-pack.md`

## 默认流程

1. 识别用户的岔路动作，读取 `references/life-fork-grammar.md`。
2. 识别系统切换：用户从哪个系统进入哪个系统，或停在哪个系统。
3. 找到自我叙事断裂：首屏判词从这里生成。
4. 读取 `references/archetype-tension-axes.md`，识别 2-3 个张力轴，写出隐秘交换。
5. 匹配人生原型，读取 `references/life-archetype-library.md`，输出主原型、副原型和隐藏不甘。
6. 固定原型命中不足时，读取 `references/archetype-composer.md`，用承载物、张力轴、系统切换和事件锚点组合临时原型。
7. 读取 `references/verdict-rewrite-patterns.md`，生成首屏判词，只命名用户放不下的遗憾。
8. 用 `references/magic-score-rubric.md` 检查判词命中、不可替换、隐秘交换和事件承托；低于通过线时先回到张力轴和原型层重写。
9. 生成三种结果：现实结果、假设结果、回补结果。
10. 从 `references/era-event-timeline-2008-2026.md` 选择 3-6 个高相关事件或周期。
11. 读取 `references/event-shock-engine.md` 和 `references/life-scene-library.md`，把事件转成事件冲击卡。
12. 生成 30 天验证实验，围绕可回收资产设计低风险动作。
13. 输出 HTML 用户报告：首屏、分叉图、三种结果卡、事件冲击卡、30 天实验。
14. 继续解释段才展示多角色判断、事件表、已知信息和补充问题。

快速运行口令：

```text
先判张力轴，再匹配原型；先写判词，再出三种结果；再给 4-6 张事件冲击卡，最后给 30 天实验。
```

补充流程：

- 首轮处理材料有限输入时，读取 `references/first-response-protocol.md`；用户不想填时直接跑材料有限版。
- 信息不足时，用 `references/onboarding-question-flow.md` 做 2-3 轮快速画像；用户不愿补充时，先输出材料有限版并列 5 个关键问题。
- 深度模拟时按多 Agent 栈运行，但多角色结果进入继续解释段，不抢用户主线。
- 读取 `references/anti-generic-writing-rules.md` 和 `references/insight-specificity-standard.md`，把抽象判断改成具体年份、生活场景、因果链、误判点和验证动作。
- 用 `references/report-quality-rubric.md` 给报告评分，并按低分项修订一次。
- 用 `references/magic-score-rubric.md` 和 `references/verdict-rewrite-patterns.md` 做内容命中评分；结构评分通过后，Magic Score 仍需通过。
- 生成 HTML 用户报告前，有脚本能力时先用 `scripts/validate_report_structure.py` 检查判词型正文结构和继续解释段位置。
- 结构通过后，可用 `scripts/render_html_report.py` 生成移动友好 HTML 用户报告。
- 修改问答、材料有限版报告、事件库、语法文件或多 Agent 规则后，运行 `scripts/validate_dialogue_event_agent_flow.py` 检查真实对话、材料有限样本、事件卡片和冲突审计链路。
- 修改原型库或 Magic Score 规则后，运行 `scripts/validate_magic_score.py` 检查原型字段、判词承托和六个回归 demo。
- 上传或发布前，运行 `scripts/validate_skill_package.py` 做包级自检。

## 外部事件使用规则

- 已经发生的事件可用于过去复盘。
- 未来事件只能作为情景变量。
- 必须区分个人选择、外部环境和随机运气。
- 不用宏观事件制造焦虑。
- 不把外部事件写成确定预测。
- 详见 `references/event-impact-framework.md` 和 `references/event-shock-engine.md`。
- 2008-2026 事件检索见 `references/era-event-timeline-2008-2026.md`。

## 参考文件

只在需要时读取：

- `references/agent-simulation-stack.md`：多 Agent 角色和运行方式。
- `references/life-fork-grammar.md`：通用人生迁移语法，优先识别岔路动作、系统切换、自我叙事断裂和可回收资产。
- `references/archetype-tension-axes.md`：原型张力轴，用 2-3 个张力组合泛化新问题。
- `references/life-archetype-library.md`：人生原型库，在语法之后匹配城市折返、海外未竟、AI 错过窗口、买房绑定等高密度原型。
- `references/archetype-composer.md`：原型组合器，固定原型命中不足时生成临时原型，避免继续扩充案例库。
- `references/verdict-rewrite-patterns.md`：判词重写规则，用替换测试、隐秘交换和事件承托修复首屏判词。
- `references/first-response-protocol.md`：首轮响应协议，用户只给一句话或拒绝填表时先跑材料有限版。
- `references/onboarding-question-flow.md`：2-3 轮用户画像问答。
- `references/topic-question-bank.md`：高频主题专用追问库。
- `references/era-event-timeline-2008-2026.md`：2008 至 2026 事件知识库。
- `references/event-impact-framework.md`：国内、全球、行业和个人冲击层。
- `references/event-shock-engine.md`：把 2008-2026 事件转成人生场景、现实代价、情绪代价、误判和验证动作。
- `references/life-scene-library.md`：把城市、海外、买房、职业、AI 等主题转成生活场景。
- `references/anti-generic-writing-rules.md`：反车轱辘规则，要求每段有年份、场景、现实代价、情绪代价、误判和动作。
- `references/magic-score-rubric.md`：命中感评分，检查首屏判词有无不可替换、隐秘交换和事件承托。
- `references/report-style-guide.md`：报告交付和 HTML 用户报告风格。
- `references/html-report-delivery.md`：Markdown、HTML 用户报告交付流程；需要用户留档说明时再读取。
- `references/report-quality-rubric.md`：报告评分和回写优化规则。
- `references/insight-specificity-standard.md`：防止车轱辘话的洞察具体度标准。
- `references/bug-taxonomy.md`：常见决策 Bug 类型。
- `references/safety-boundaries.md`：安全边界。
- `templates/intake.md`：结构化输入材料。
- `templates/life-fork-simulation-report.md`：深度模拟报告模板。
- `templates/life-fork-report.md`：轻量人生岔路报告模板。
- `templates/choice-sandbox.md`：人生选择沙盘模板。
- `templates/bug-report.md`：决策 Bug Report 模板。
- `templates/delivery-pack.md`：报告交付包模板。
- `templates/quality-scorecard.md`：开发者质量评分表模板。
- `examples/real-dialogue-flows.md`：真实对话流回归样例。
- `examples/low-information-report.md`：用户懒得填时的材料有限版报告回归样例。
- `examples/magic-score-regression.md`：Magic Score 内置回归样例，覆盖常规题和留出题。
- `scripts/validate_report_structure.py`：报告正文结构验证脚本。
- `scripts/validate_html_first_skill.py`：HTML 优先和真实对话流校验脚本。
- `scripts/validate_report_specificity.py`：洞察具体度校验脚本。
- `scripts/validate_dialogue_event_agent_flow.py`：2-3 轮问答、2008-2026 事件库和多 Agent 冲突链路校验脚本。
- `scripts/validate_magic_score.py`：人生原型库和 Magic Score 回归校验脚本。
- `scripts/validate_skill_package.py`：上传前包级自检脚本，检查入口元数据、关键文件、旧口径残留和内置回归。
- `scripts/render_html_report.py`：零依赖 Markdown 到移动友好 HTML 渲染脚本。

## 输出原则

- 结论先行。
- 语法识别、张力轴、原型命中、Magic Score 和质量评分只用于内部检查，不放进用户版报告正文。
- 第一屏只服务命中感：报告名、用户问题、强判词和下滑提示。
- 第二屏用一个简单分叉图解释：一次选择，后来分出了三种结果。
- 分叉图下面必须写“怎么读这张图”，说明它只做分叉关系解释和条件情景复盘。
- 图表后进入三种结果卡和事件冲击卡，再进入“你真正放不下的是什么”和“30 天验证实验”。
- 默认展开区保留用户当下最关心的解释、事件冲击卡和 4 周实验。
- 多角色判断和外部事件放入折叠解释层，不抢用户主线。
- 用户正文减少“变量、路径、矩阵、框架、Agent”等系统词。
- 每种结果都要有收益和代价。
- 每个判断都要可审计，避免像预言。
- 每个关键判断必须有机制链、反证条件和证据债。
- 每个假设结果都要标注成立条件和待验证信息。
- 语法识别通过后，还要过张力轴、原型命中和 Magic Score；结构正确但判词空泛时先重写。
- 用户要报告时先给 Markdown；实体支持时优先生成 HTML 用户报告。
- HTML 正文优先给用户判词、分叉图、核心执念和可补动作；各视角细节进入人话折叠解释层。
- 质量评分和修订记录保留在开发者草稿、日志或注释，用户版 Markdown 和 HTML 均不展示。
- HTML 用户报告第一屏应像一页判词，不放已知信息程度、按钮、今日行动和复杂表格。
- “30 天验证实验”按 4 周拆解，每周都要有低风险动作和现实反馈。
- 完整用户报告默认不附质量评分和修订记录；低于 20 分时先小改再交付。
- 公开案例另行处理；本 Skill 默认服务用户本人复盘和报告交付，避免暴露真实人物和私有经历。
