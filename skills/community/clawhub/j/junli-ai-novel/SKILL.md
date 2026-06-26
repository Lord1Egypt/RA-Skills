---
name: junli-ai-novel
description: 平台向长篇网文连载写作助手。负责新项目立项、章节续写、单章返修、项目记忆维护、长篇分卷治理和章节质检。内置章节/场景/语言三层写法原则，适配爽文、言情、权谋等主流题材，支持从脑洞到超长篇全流程。更多信息关注抖音君黎。
---

# 君黎 AI 网文连载

先读 `PROJECT.md`。它把本仓库重封装成 `Rule / Workflow / Command` 三层索引，适合先找入口，再决定是否下钻到原子命令。

## 核心目标

1. 最高优先级：连载稳定、追读牵引、卖点兑现、长线不崩。
2. 默认按平台向长篇网文处理，不按出版文学标准做默认决策。
3. 先读档，再下笔；先编排，再正文；先检查，再宣称完成。
4. 任何新内容不得与更高层级记忆硬冲突。

## 默认入口顺序

优先顺序不是“先背命令”，而是：

1. 先看 `PROJECT.md`
2. 再判断当前任务属于哪个 Workflow
3. 只有需要拆解排查时，才回到底层 Command

默认 Workflow：

- 继续写下一章：`next-chapter`
- 章节静态预审 + 审稿稿本：`review`
- 商业化包装：`marketing`
- 长篇治理：`bootstrap-longform` + `governance` + `audit`

## 硬门槛

命中续写、开写、返修、恢复记忆、长篇治理时，下面都是必须动作：

> **快捷路径**：续写场景直接用 `next-chapter` 命令，它会自动串联步骤 1-3 中的所有前置动作（`preflight → resume → plan → compose → start`），无需单独执行每一条原子命令。只有当 Workflow 失败或需要精细排查时，才拆回原子命令。

1. 正文前必须先跑：

```bash
python3 scripts/chapter_pipeline.py preflight <项目目录>
python3 scripts/chapter_pipeline.py resume <项目目录>
```

2. 长篇项目正文前必须先跑：

```bash
python3 scripts/chapter_pipeline.py plan <项目目录> --chapter-num <章节号> --chapter-title "标题"
python3 scripts/chapter_pipeline.py compose <项目目录> --chapter-num <章节号> --chapter-title "标题"
python3 scripts/chapter_pipeline.py start <项目目录> <章节号> --chapter-title "标题"
```

3. 写完后必须先跑：

```bash
python3 scripts/chapter_pipeline.py check <章节文件路径>
python3 scripts/chapter_pipeline.py finish <项目目录> <章节号> <章节文件路径> --chapter-title "标题" --summary "摘要"
```

4. 满足任一条件即视为长篇治理范围：
   - 目标字数超过 100 万字
   - 实际已写超过 30 万字
   - 项目已写到 20 章以上
   - 用户明确要求分卷、阶段、卷末结算、结构变更、超长篇控盘（此条由 AI 自行判断，工具不检测）

5. 长篇治理范围内，缺治理文件时先跑：

```bash
python3 scripts/chapter_pipeline.py bootstrap-longform <项目目录>
```

6. 长篇治理范围内，每 10-20 章必须跑阶段审计；每卷结束必须跑卷审计：

```bash
python3 scripts/chapter_pipeline.py audit <项目目录> --scope stage
python3 scripts/chapter_pipeline.py audit <项目目录> --scope volume
```

7. 如果 `preflight` 因当前卷 / 当前阶段 / 阶段目标缺失而失败，先跑：

```bash
python3 scripts/chapter_pipeline.py governance <项目目录> --current-volume "第一卷" --current-phase "阶段1" --phase-goal "目标"
```

8. 如果要改全书终局、主角长期弧线、世界底层规则、长线关系边界，必须先更新 `docs/变更日志.md`，再继续正文。
9. 如果无法执行命令、无法读取关键文件或前置校验失败，必须明确报告阻塞；禁止假装已经恢复上下文、已经检查或已经同步进度。

## 常见失误

下面这些做了等于白做，必须避免：

- 没跑 `preflight` / `resume` 就续写正文（上下文没恢复）
- 记忆文件缺失时假装已恢复，继续写
- 长篇项目缺卷纲 / 阶段规划 / 变更日志，却平推正文
- 超过一个阶段没跑 `audit`
- 核心设定或终局方向改了，却没写进变更日志
- 用户只要求局部返修，却整章重写

## 任务分流

先把请求归进下面 5 类。命中 D 或 E 时，先修 D / E，再回到 B / C。

### A. 新项目 / 设定不完整

触发：
- 从零开始
- 项目目录不存在
- 只有脑洞、梗概或人设碎片

必须动作：
- 只补齐 5 问立项：题材风格、主角结构、主角核心性格、核心冲突、预计章节规模
- 先用主线三步法：终点站 -> 起爆事件 -> 连锁反应
- 再用终极锚点 -> 逆推问题链 -> 分卷锚点
- 最后初始化项目：

```bash
python3 scripts/chapter_pipeline.py init "项目名" --mode single
```

`--mode` 可选值：
- `single`：单主角线（默认，适合大多数升级流、爽文、言情）
- `dual`：双主角或双视角结构（CP 文、双雄文、平行叙事）
- `ensemble`：群像多线（权谋、宫斗、多主角群像）

参考：
- `references/main-plot-construction.md`
- `references/outline-template.md`
- `references/chapter-plan-template.md`
- `references/outline-refinement.md`
- `references/longform-governance.md`

### B. 继续连载 / 下一章

触发：
- 继续写
- 下一章
- 新开对话续旧项目

必须动作：
- 先过硬门槛
- 读取顺序固定：`task_log.md` -> `docs/项目总纲.md` -> `docs/章节规划.md` -> `plot/伏笔记录.md` -> `plot/时间线.md` -> 相关角色档案 -> 上一章正文
- 恢复输出至少包含：创作阶段、最近 2-3 章摘要、主角当前状态、活跃伏笔、下一章目标
- 长篇项目必须先 `plan` / `compose`
- 再进入场景拆分和正文

### C. 单章扩写 / 重写 / 润色 / 质检

触发：
- 用户明确点名某章
- 用户要扩字数、改节奏、修对白、减 AI 味
- 用户要检查爽点、毒点、情绪曲线或一致性

必须动作：
- 读取目标章节
- 至少补读上一章、下一章或相关设定中的必要部分
- 只做定向返修，不全文推倒
- 如果是局部问题，优先从 `references/micro-revision-ops.md` 中选择单一微操作
- 如果问题在主线或章节层，先回上层重查

### D. 恢复记忆 / 修复项目记忆

触发：
- 恢复上下文
- 唤醒记忆
- 记忆文件缺失

必须动作：
- 明确报告缺失文件
- `resume` 只作机器摘要，不等于修复完成
- 从正文、现有文档、角色档案手动重建
- 先补记忆，再继续正文

### E. 长篇治理 / 阶段审计 / 卷审计 / 结构变更

触发：
- 超长篇控盘
- 分卷
- 阶段规划
- 卷末结算
- 结构变更

必须动作：
- 确认存在：
  - `docs/全书宪法.md`
  - `docs/卷纲.md`
  - `docs/阶段规划.md`
  - `docs/变更日志.md`
- 用 `governance` 同步当前卷 / 当前阶段 / 阶段目标
- 阶段切换前跑 `audit --scope stage`
- 卷末结算前跑 `audit --scope volume`
- 结构性改动先写 `变更日志.md`
- 审计失败时，禁止继续正文

## 项目结构

```text
[项目目录]/
├── docs/
│   ├── 项目总纲.md
│   ├── 章节规划.md
│   ├── 作者意图.md
│   ├── 当前焦点.md
│   ├── 全书宪法.md
│   ├── 卷纲.md
│   ├── 阶段规划.md
│   ├── 变更日志.md
│   ├── 冲突设计.md
│   ├── 世界观.md
│   ├── 法则.md
│   ├── 关系图.md
│   └── 群像主题拆分.md
├── characters/
├── manuscript/
├── plot/
├── runtime/
│   ├── chapter-0001.intent.md
│   ├── chapter-0001.context.json
│   ├── chapter-0001.scenes.md
│   ├── chapter-0001.rule-stack.yaml
│   └── chapter-0001.trace.json
└── task_log.md
```

约束：
- `manuscript/` 只放纯正文
- `runtime/` 只放本章运行时产物，不手写正文
- `docs/作者意图.md`、`docs/当前焦点.md` 属于输入治理层
- `docs/项目总纲.md`、`docs/卷纲.md`、`docs/阶段规划.md`、`docs/变更日志.md` 属于结构治理层
- 旧项目若仍只有 `docs/大纲.md`，默认把它视作 `项目总纲 + 章节规划` 的兼容入口

## 四层记忆

- L1 会话工作记忆：本章目标、场景推进链、开头钩子、上章悬念
- L2 项目运行记忆：`task_log.md`、`docs/章节规划.md`、`plot/伏笔记录.md`、`plot/时间线.md`
- L3 结构治理记忆：`docs/项目总纲.md`、`docs/卷纲.md`、`docs/阶段规划.md`、`docs/变更日志.md`
- L4 宪法记忆：`docs/全书宪法.md`、`docs/世界观.md`、`docs/法则.md`、`characters/*.md`

消歧顺序：`L4 > L3 > L2 > L1`

## 正文写法原则

这是写正文时应该主动对标的标准，不是事后检查清单。

### 章节层

- **目标单一**：每章核心事件不超过 2 条，多了就切章，别塞
- **章尾造压**：用未解决的张力收尾——不是总结，是读者不读下一章会难受
- **每章必须有一次实感回报**：翻盘、揭秘、关系进展、能力升级任选其一；没有回报，读者掉追读
- **受挫必须给补偿基础**：主角挫败后，同章或紧邻章节给出反击或希望的锚点，不能连续几章只有憋屈

### 场景层

- **每个场景从状态 A 走到状态 B**，开头和结尾的人物处境或信息量不能一样
- **高能前放慢**：爆发场景前插 1-2 个低强度段给读者换气，高能后给收尾拍，别急着跳下一幕
- **对白的作用只有两种**：推进冲突、暴露性格。不用对白解释背景设定，那是说明书
- **视角纪律**：第三人称紧贴主 POV 的认知边界，不提主角不知道的信息，不在同段乱切脑内

### 语言层

- **规避 AI 高频套语**：以 X 为 Y、在这一刻、心中涌起、岁月/征程、结尾感悟升华、"他知道"+"他明白"连用
- **心理描写不超标**：思路链路是"想法 → 行动 → 结果"，不用旁白总结角色感受，让读者自己感受
- **具体优于抽象**：写"刀口从肩膀切下去，皮肤往两侧翻"而不是"他受了重伤"；写"她没说话，拿起外套走了"而不是"她很失望"
- **情绪不要直接命名**：不写"他感到愤怒"，写愤怒的行为和身体反应

## 常用命令入口

高频场景直接用这四条，其余原子命令查 `python3 scripts/chapter_pipeline.py commands`：

```bash
# 续写下一章（自动串联 preflight→resume→plan→compose→start）
python3 scripts/chapter_pipeline.py next-chapter <项目目录> --chapter-title "标题"

# 章节质检（静态预审 + 审稿稿本）
python3 scripts/chapter_pipeline.py review <章节文件路径> --project-path <项目目录>

# 长篇治理初始化 / 状态同步
python3 scripts/chapter_pipeline.py bootstrap-longform <项目目录>
python3 scripts/chapter_pipeline.py governance <项目目录> --current-volume "第一卷" --current-phase "阶段1" --phase-goal "目标"

# 商业化包装
python3 scripts/chapter_pipeline.py marketing <项目目录> --platform 起点中文网 --audience 男频读者
```

## 参考资料地图

立项 / 规划：
- `references/main-plot-construction.md`
- `references/outline-template.md`
- `references/chapter-plan-template.md`
- `references/outline-refinement.md`
- `references/longform-governance.md`
- `references/character-template.md`
- `references/character-building.md`
- `references/plot-structures.md`
- `references/conflict-design.md`
- `references/worldbuilding-logic.md`
- `references/worldbuilding-presentation.md`
- `references/golden-finger-design.md`
- `references/idea-incubation.md`

章节创作 / 续写：
- `references/chapter-workflow.md`
- `references/micro-revision-ops.md`
- `references/chapter-guide.md`
- `references/chapter-template.md`
- `references/flow-break-writing.md`
- `references/hook-techniques.md`
- `references/dialogue-writing.md`
- `references/ensemble-writing.md`
- `references/content-expansion.md`
- `references/daily-narrative.md`
- `references/nonlinear-narrative.md`
- `references/reader-compensation.md`
- `references/literary-opening.md`
- `references/suspense-design.md`

写后检查 / 风格护栏：
- `references/quality-checklist.md`
- `references/consistency.md`
- `references/style-guardrails.md`
- `references/rule-linting.md`
- `references/writing-quickref.md`（由 `plan` / `compose` 命令自动注入 intent 文件，无需手动读取）

工具吸收 / 方法沉淀：
- `references/tooling-adoption-roadmap.md`
- `references/marketing.md`

## 题材补充

平台向默认规则：
- 书名先承担题材识别和核心钩子
- 前 3 章默认按“前三秒”标准自查
- 不靠擦边、影射、审核侥幸维持吸引力

女频 / 言情 / 大女主：
- 把主体性、补偿机制、叙事立场视为高敏感检查项
- 出现“男主膈应”“女主太憋屈”“人设塌了”时，优先读 `references/style-guardrails.md`

## 外部材料接入

如果用户提供方法论、访谈、经验材料：

1. 先判断它影响的是立项、长篇治理、章节推进还是风格
2. 长篇治理相关优先并入 `references/longform-governance.md`
3. 大纲修整相关优先并入 `references/outline-refinement.md`
4. 局部返修相关优先并入 `references/micro-revision-ops.md`
5. 工具与工作台相关优先并入 `references/tooling-adoption-roadmap.md`
6. 只吸收可操作、可复用、可验证的内容
7. 只适用于单项目的经验，写进项目文档，不污染通用规则
