# Novel Studio

> 中文网文连载创作流水线 — 强制审批门 × 往复式写作 × 记忆持久化

## 核心差异

**为什么不用直接生成的小说 skill？**

| 直接生成的痛点     | Novel Studio 的解法                     |
| ------------------ | --------------------------------------- |
| 一次生成，整改困难 | 分阶段产出，每阶段可审查和修改          |
| 大纲不清导致写偏   | 必须先完成大纲和人物卡才能动笔          |
| 没有交付标准       | 每阶段有明确的完成标准 + 用户审批门     |
| 写到一半不知道在哪 | 项目状态文件记录当前进度、阶段、阻塞点  |
| 反馈不知道改哪里   | 反馈检测机制 + 范围评估，不乱改         |
| 只能一口气写完     | 指定章节数，写完校对再继续，不限时      |
| 中断后无法继续     | 记忆系统保存所有上下文，随时可中断/继续 |

## 核心原则

**强制审批门** — 每个阶段完成后必须等待用户明确确认，未经批准不自动推进。"看起来不错"不是批准，必须说"确认"或"继续"。

**禁止跳阶段** — 必须按顺序完成，不得从模糊想法直接跳到完整正文。没有大纲 = 不写正文。没有人物卡 = 不写正文。

**文件优先** — 阶段成果必须持久化到项目文件，不接受仅存在于对话中的临时内容。

**Supervisor-first 落盘** — 父 agent 负责流程掌控、审批解释、落盘决策和 subagent 调度。一旦正式文件被写入或刷新，立即进入对应审批门，不再把它当作“还在讨论”。
**章节级进度持久化** — 章节执行进度必须进入 `.novel-state.json`，例如 `第1章初稿中`、`第1章初稿待审核`、`第2章润色中`、`第3章审核中`、`第4章已完成`，不再只靠聊天记忆判断。

**拒绝敷衍** — 不能因为"有东西存在"就判定阶段完成，必须达到可用标准。大纲要具体到情节点，人物要具体到动机和冲突。

**开篇门优先** — 开篇门是 drafting 之前的强制前置审批门。没有 `04A_开篇设计.md` 或没有明确通过 Opening Gate，不进入第一批正文。

**风格锁定** — 风格不是聊天里一句“偏热血 / 偏细腻”就算定了。必须生成 `01A_风格圣经.md`，后续 subagent 统一按同一份风格合约创作。

**长篇账本** — 长篇稳定不靠记忆硬扛。必须维护世界规则、伏笔、关系、资源四类账本，避免中后期崩设定。

**叙事智能层** — 在现有状态文件、账本、审校链之上，外挂统一真相源、动态状态追踪、矛盾配对、证据链、角色认知追踪、伏笔三元组追踪等能力；它负责“检查与索引”，不替代主控审批，也不替代 subagent 写审校。
- `05F_时间与事件图谱.md` / `05G_伏笔三元组账本.md` / `05H_角色认知与误判表.md` / `05I_证据链与矛盾对照表.md` 是父 agent 维护的正式衍生文件。
- planning 通过后可初始化 `05F` 到 `05I`；accepted 的 drafting / polishing / proofreading 会刷新 `narrativeIntelligence.*`。
- accepted proofreading 会额外刷新 `05I` 和 `openCriticalIssues`；若存在证据支撑的关键一致性问题，会明确停掉 autopilot，而不是吞掉停止原因。

**Cliche Exhaustion Loop** — 这是 supervisor 侧的反俗套协议层，不是新阶段。
- `Discovery` 用 `quick`：先把直觉俗套版本摊开，再保留值得继续的“新鲜轴”。
- `Story Planning` 用 `deep`：planning 审批前必须完成更深一轮反俗套穷举，不能只写抽象提醒；如果 supervisor 启动了这轮 deep pass，必须先在所选分支的 `05_定稿结论.md` 里落结论，才能批准 planning。
- `Opening` 只验证保留下来的新鲜轴有没有真正落到前 3 / 10 / 20 章，不重开大范围脑暴。
- `Proofreading` 在本 slice 里只做父侧轻量回滑检测 / 报告，不单独重开 planning，也不改 child proofreading 协议。
- `.novel-state.json`、staging 分支选择、canonical 回填、分支清理仍然只归父 agent。

## 三大核心机制

### 往复式写作

不要求一口气写完整本小说。按批次进行：

```
[写 N 章节] → [校对] → [审批门] → [写下 N 章节] → [校对] → [审批门] → ...
```

- 每批次写几章由用户决定（1章、3章、5章均可）
- 每批次完成后进行校对和质量检查
- 通过审批门后才继续下一批次
- 支持中途暂停，下一次继续时从断点恢复

### 记忆系统

每个小说项目都有独立的记忆文件，记录：

- **世界观设定**：修炼体系、势力分布、地理环境
- **人物档案**：姓名、性格、当前状态、与其他人物的关系
- **情节进展**：已写章节摘要、伏笔埋设、待回收线索
- **项目状态**：当前阶段、批次编号、审批状态
- **正式落盘状态**：待审批文件、最后一次正式落盘阶段、是否处于 brainstorming 分支模式
- **自动推进状态**：`autoPilot` 是否开启、终点章节、最近进度、停止原因

写作中断后，重新启动时 Agent 会读取记忆文件，自动恢复上下文，无需复述。

### 反馈修订

写作过程中用户可随时提出修改意见。Agent 会：
1. 检测并分类反馈（结构调整 / 人物改动 / 细节修正 / 风格调整）
2. 评估影响范围（仅影响当前批次 / 需追溯前文 / 涉及大纲调整）
3. 询问是否记录为正式反馈
4. 在对应阶段范围内修改，不做未授权的大范围改动

### Autopilot 自动推进

- 默认仍是手动审批。没有明确授权时，所有审批门继续人工确认。
- 只有用户给出显式、带终点章节的授权才会开启 autopilot，例如 `后续你来主控，继续到第10章结束`。单独一句 `继续` 不算。
- 自动推进不改变职责分工：父 agent 仍负责流程控制、审批解释、状态落盘和进度汇报；`drafting` / `polishing` / `proofreading` 仍由各自 subagent 执行。
- `advance_autopilot.py` 每次只前进一步：补 `scopeConfirmed`、在 `05_本轮章节规划.md` 可安全解析时批准 `chapterPlanApproved` 并重建 `chapterTasks`、或代批 `waiting_draft_feedback` / `waiting_polishing_feedback` / `waiting_proofreading_feedback`。
- 每次调用 `advance_autopilot.py` 都会返回 `report`：明确告诉父 agent 现在是继续中、暂停中还是已停止，以及这一步是否应该主动通知用户。
- 如果 `report.shouldNotify=true`，父 agent 必须立刻把 `report.userFacingMessage` 发给用户；不能只把信息留在状态文件里。
- 如果这次通知用了 `report.pendingEventIds` 对应的章节进度，发完后要用 `chapter_progress_report.py --ack <event-id>` 回执，避免下次重复播报同一条。
- 自动推进期间仍持续汇报章节进度；不会因为进入 autopilot 就停止 `chapterTasks` / `pendingProgressItems` 的更新和对外汇报。
- 以下情况必须停下并给出明确原因：子 agent 返回 `blocked`、用户发来实质性打断、目标章节达到经批准的 proofreading 完成状态、或用户改成新的终点章节。
- `waiting_final_review_feedback` 永远不自动批准；最终审校和最终交付仍是人工决定。

## 7 阶段流水线

```
发现 → 大纲规划 → 人物体系 → 正文写作 → 润色 → 校稿 → 最终审校
 ↓          ↓          ↓          ↓        ↓      ↓        ↓
审批门    审批门      审批门      审批门    审批门  审批门   审批门
```

| 阶段                  | 核心产出                 | 门控条件                   |
| --------------------- | ------------------------ | -------------------------- |
| Discovery 发现        | 选题报告、确认标题       | 标题经用户确认             |
| Story Planning 大纲   | 完整大纲文件             | 大纲覆盖主要情节点         |
| Character System 人物 | 人物设定卡、关系图       | 核心人物有动机和冲突       |
| Drafting 正文         | 分章正文文件（批次进行） | 章节在项目目录中（非对话） |
| Polishing 润色        | 精修后的章节             | 无AI味、语言流畅           |
| Proofreading 校稿     | 无矛盾/逻辑漏洞的章节    | 通过OOC和一致性检查        |
| Final Review 最终审校 | 评分报告、交付判断       | 达到验收分数               |

正式文件一旦写入，立刻打开当前阶段的审批门；不会继续把已经落盘的成果当作开放讨论。

## 开篇门与稳定器

Novel Studio 现在把市场调研里最关键的四件事硬化成流程要求：

- 开篇抓取：前 3 章要完成点火、显规、留钩
- 角色驱动：前 10 章必须证明主角为什么非动不可
- 长线承重：前 20 章必须让卷级主线和代价体系站住
- 平台适配：起点 / 番茄 / 通用模式在节奏、信息密度、章尾钩子上分别锁定

开篇门是 drafting 之前的强制前置审批门，执行上要求：

- 生成 `04A_开篇设计.md`
- 明确前三章任务、前十章驱动、前二十章卷级承重
- 经用户明确确认后，才允许进入第一批 prose drafting

同时，项目必须在正文前准备：

- `00C_底盘与切口决策.md`
- `01A_风格圣经.md`
- `01B_总主线与卷级推进.md`
- `05B_世界规则账本.md`
- `05C_伏笔回收台账.md`
- `05D_关系状态表.md`
- `05E_能力与资源变化表.md`

如果显式进入脑暴 / 分支探索，并且要跑反俗套穷举分支，`staging/<stage>/<branch-id>/` 下推荐固定放：
- `00_脑暴任务卡.md`
- `01_直觉俗套清单.md`
- `02_反驳与否认.md`
- `03_变异候选.md`
- `04_保留候选.md`
- `05_定稿结论.md`

只有 `05_定稿结论.md` 可以授权把该分支结论回填到 canonical 文件；没有这份结论，就不允许把探索分支当正式方向。

## Subagent 执行接入

`drafting` / `polishing` / `proofreading` 默认走父 agent 编排 + subagent 执行。

标准父流程是 `prepare -> spawn -> extract -> finalize`：
- `scripts/prepare_stage_subagent_dispatch.py`
- `spawn_agent(..., fork_context=false)`
- `scripts/extract_stage_subagent_result.py`
- `scripts/finalize_stage_subagent_dispatch.py`

`prepare_stage_subagent_dispatch.py` 支持 `--dispatch-dir` 生成标准化 dispatch workspace。
prepare 的返回结果会带 `dispatchDir` / `bundleFile` / `promptFile` / `manifestFile` / `rawFile` / `resultFile` / `validatedFile`，父 agent 不必再手写整套临时文件路径。
标准布局固定为 `bundle.json` / `prompt.txt` / `manifest.json` / `child-response.txt` / `result.json` / `validated.json`。
如果你显式传了 `bundleFile` / `promptFile` / `manifestFile`，且三者位于同一个父目录，prepare 也会自动把这个目录当成 `dispatchDir`，继续为 `rawFile` / `resultFile` / `validatedFile` 生成标准路径。
`extract_stage_subagent_result.py` 和 `finalize_stage_subagent_dispatch.py` 也支持直接吃 `--dispatch-dir`。
显式传入的 `rawFile` / `resultFile` / `bundleFile` / `manifestFile` / `validatedFile` 会覆盖 `dispatchDir` 默认路径。
如果父 agent 用 Python 编排，可以直接 import `scripts/subagent_dispatch_runtime.py`。
`prepare_dispatch(...)` 负责生成 `childPrompt`，也就是发给子 agent 的 prompt。
`record_child_output(...)` 只负责记录子 agent 的原始输出。
`finalize_dispatch(...)` 会串起 extract + validate + apply。

运行规则：
- 所有 `bundle` / `prompt` / `manifest` / `child-response` / `result` / `validated` 中间产物都必须放在项目根目录之外
- 只把 `executionPackage` 发给子 agent
- `validationContext` 只留在父 agent
- 章节范围必须同时以 `requiredInputs.chapterLabels` 的结构化列表进入 dispatch package
- `drafting` / `polishing` 的 `targetFiles` 必须非空且位于 `manuscript/` 下
- `outputContract.requiredReturnFields` 必须严格等于协议字段列表，`outputContract.mustWriteFiles` 必须严格等于 `targetFiles`
- `completed` 结果必须真实触达本次 dispatch 的全部 `outputContract.mustWriteFiles`
- `proofreading` 必须只写 `05A_本轮校对报告.md`，且 `overwriteFlag=true`
- `targetFiles` / `mustNotModify` / `changedFiles` / `createdFiles` 等 path list 不允许重复项
- `validationContext.executionPackageDigest` / `baselineFilesDigest` / `bundleFingerprint` 必须和当前 bundle 内容一致；一旦手改过 bundle，应直接重建
- `prepare_stage_subagent_dispatch.py` 默认会写出 sidecar `manifest`
- sidecar `manifest` 会同时记录 `bundle` 摘要，以及可选 `promptFile` / `promptSha256` 完整性信息
- `finalize_stage_subagent_dispatch.py` 可以用 `--manifest-file` 先校验 bundle sidecar
- 子 agent 只允许返回一个 JSON object
- `blocked` / `needs_clarification` 必须带非空 `blockedReasons`；`completed` 必须保持 `blockedReasons=[]`
- `proofreading` 的 `completed` 结果必须给出非空的 `continuity` / `logic` / `characterOOC` / `fixDirection`；若 judgment=`needs revision`，`blockers` 也必须非空
- `proofreading` 若 judgment=`acceptable`，`blockers` 必须为空
- `proofreading` 若 judgment=`conditionally acceptable`，`blockers` 必须为空且 `risks` 必须非空
- 父 agent 只有在 extract、validate 都通过后才能 apply 结果
- 如果子 agent 返回 prose、多个 JSON、空输出或非法 JSON，按协议失败处理，不得静默兜底

章节进度汇报：
- 父 agent 会把章节级状态变化落到 `.novel-state.json` 的 `chapterTasks` 和 `pendingProgressItems`
- 默认汇报文案会合并成类似 `第1章初稿待审核；第2章润色中`
- 自动推进主循环优先读取 `advance_autopilot.py` 返回的 `report.pendingProgressSummary` / `report.userFacingMessage`
- 读取待汇报摘要：`python3 skills/novel-studio/scripts/chapter_progress_report.py <项目目录>`
- 汇报成功后确认这些事件已发送：`python3 skills/novel-studio/scripts/chapter_progress_report.py <项目目录> --ack <event-id>`

`staging/` 只用于明确要求的脑暴 / 分支探索。only explicit brainstorming mode may write to `staging/`

Drafting 示例：

```bash
python3 skills/novel-studio/scripts/prepare_stage_subagent_dispatch.py \
  "$PROJECT_ROOT" \
  drafting \
  --batch-range "第1章" \
  --target-file "manuscript/第1章_开端.md" \
  --dispatch-dir "$TMP_DIR"
```

父 agent 可以直接读取 prepare 返回的 `childPrompt`，或使用 prepare 输出的 `promptFile`。

拿到 child 原始输出后：

```bash
python3 skills/novel-studio/scripts/extract_stage_subagent_result.py \
  --dispatch-dir "$TMP_DIR" \
  --project-root "$PROJECT_ROOT"

python3 skills/novel-studio/scripts/finalize_stage_subagent_dispatch.py \
  "$PROJECT_ROOT" \
  --dispatch-dir "$TMP_DIR"
```

如果你不走标准布局，仍然可以显式传 `--raw-file` / `--result-file` / `--bundle-file` / `--manifest-file` / `--validated-file` 覆盖默认解析。

Python 父 agent 也可以直接写成：

```python
from pathlib import Path

from subagent_dispatch_runtime import finalize_dispatch, prepare_dispatch, record_child_output


payload = prepare_dispatch(
    project_root,
    "drafting",
    batch_range="第1章",
    target_files=["manuscript/第1章_开端.md"],
    dispatch_dir=tmp_dir,
)

child = spawn_agent(
    agent_type="worker",
    fork_context=False,
    message=payload["childPrompt"],
)
child_done = wait_agent(ids=[child.id], timeout_ms=180000)
dispatch_dir = Path(payload["dispatchDir"])
record_child_output(project_root, child_done["final_message"], dispatch_dir=dispatch_dir)
applied = finalize_dispatch(project_root, dispatch_dir=dispatch_dir)
```

如果你只想理解运行时协议，先看：
- `references/subagent-execution.md`
- `references/subagent-dispatch-template.md`

如果你要继续把一致性检查做深，再看：
- `references/cfpg-tracker.md`
- `references/narrative-intelligence.md`

## 使用方式

```bash
/spencergo:novel-studio
```

## 典型对话

```
用户：我要写一个都市重生小说，先写5章
Agent：好的，进入发现阶段。先扫描当前都市重生题材热点……
（热点扫描完成）
Agent：[阶段报告] 当前热门方向是……请确认是否按此方向推进？

用户：确认
Agent：进入大纲规划阶段……（大纲完成）
用户：确认
Agent：进入人物体系阶段……（人物卡完成）
用户：确认，开始写第一章到第五章

Agent：批次1/？ 开始撰写第1-5章……
（第5章完成，进入校对阶段）
Agent：[校对报告] 第1-5章一致性检查完成，OOC检查通过……
请确认是否继续下一批次？

用户：我觉得第3章主角性格有点崩
Agent：[反馈评估] 检测到人物相关反馈，影响范围：第3章及后续批次。
是否记录为正式反馈并修订？

用户：确认
Agent：（修订第3章，复查一致性）修订完成，请确认。
用户：确认，继续写6-10章

Agent：批次2/？ 从第6章继续写作……
```

## 项目状态

用户可随时询问：
- 现在在哪个阶段？写了到第几章？
- 当前批次进度如何？
- 有哪些阻塞点？
- 上次的反馈应用了吗？
- 大纲有调整吗？

Agent 会基于项目状态文件给出可读的进度报告。

## 安装

### Claude Code（spencergo 市场）

```bash
/plugin marketplace add spencerkit/spencergo-marketplace
/plugin install spencergo@spencerkit/spencergo-marketplace
```

### OpenClaw（ClawHub）

```bash
# 安装 ClawHub CLI
npm i -g clawhub

# 或直接从市场安装
clawhub install novel-studio
```

## License

MIT
