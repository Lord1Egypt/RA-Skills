# Replay Evaluation

## General method

历史回放用于验证流程能否复现关键决策与门禁，不重新评价作者当时的判断。回放只读历史文件，不修改原稿、策划和发布物料。

每个案例记录：

- 历史输入和最终结果。
- Skill 预期生成的 case bundle。
- Gate A 应出现的确认项。
- Gate B 应出现的张力项。
- 事实与红线应被哪一道门禁拦截。
- 与历史流程的差异和遗漏。

## Case 1: Fireworks AI

### Inputs

- `Fireworks-AI-策划-20260727-v1.md`
- `Fireworks-AI-策划-20260727.md`
- `Fireworks-AI-正文初稿-20260727.md`

### Must reproduce

- Fireworks 作为案例证据，文章主线是推理基础设施层重估。
- 原创性复核识别已有融资、人物和 Token 工厂报道。
- 正面处理纯托管无结构性护城河的反方。
- Gate A 覆盖标题、compute-to-data 比重、中美对比深���、反方引用和 Cursor 位置。
- 终稿保留 Cursor 作为证伪变量。

### Failure signals

- 写成公司介绍或融资复盘。
- 把“推理即护城河”当作无需证明的前提。
- 忽略 SemiAnalysis 张力或客户集中度。
- 把摘要、标签和发布备注混入正式正文。

## Case 2: Kimi / model-weight controls

### Inputs

- `中国AI出口管制-策划-20260727.md`
- `中国AI出口管制-正文初稿-20260727.md`

### Must reproduce

- 把“已启动”修正为讨论、酝酿或未落地。
- 修正宏观数据分母和时间口径。
- 检索 2025 年美国模型权重管制及撤销的历史。
- 形成权重与 Token、资产与服务、能力定价与合规定价的分析框架。
- Gate A 覆盖标题、蒸馏指控篇幅、合集归属和发布时间。
- 终稿前重新核验政策状态。

### Failure signals

- 把搜索摘要当作政策原文。
- 混用讨论、草案和正式禁令。
- 滑向地缘输赢叙事。
- 未处理法律状态和时效变化。

## Case 3: Europe AI — Open Source as Sovereignty

### Inputs

- `文章_微信_01_开源即主权.md`
- `欧洲AI深度研究系列_三平台传播运营策划.md`
- `审核报告_欧洲AI深度研究系列_全面复审.md`

### Must reproduce

- 系列定位只作为上下文，单篇可以独立阅读。
- 三平台共享事实与核心判断，平台表达分别适配。
- 识别中英文对举、系列自指、元信息、营销词和口语缓冲。
- 改稿后执行机器扫描与人工通读。
- 不把系列排期、运营动作和商业意图写进正文。

### Failure signals

- 把“前几篇、下一篇、系列收官”等过程信息留在单篇。
- 中文规则严格、英文规则放松。
- 只跑一次 Grep，改稿后不复扫。
- 把运营 KPI 当作文章论据。

## Acceptance record

```markdown
# Replay Result

## Case
- Name:
- Historical inputs:
- Read-only confirmed: yes/no

## Workflow coverage
- Input gate:
- Fact table:
- Originality review:
- Gate A:
- Draft gate:
- Eight-role review:
- Gate B:
- Final re-check:

## Differences
- Expected but missed:
- Newly added but unnecessary:
- False positives:
- False negatives:

## Verdict
- pass / conditional pass / fail
- Required skill changes:
```

第一版验收要求三个案例均达到 pass 或 conditional pass，且无 P0 安全问题、无历史文件修改。
