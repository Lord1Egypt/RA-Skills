---
name: office-token-booster
description: "办公室 AI 提效助手 —— 既帮你做周报/会议纪要/数据分析/文档整理/PPT 大纲，又自动记下每次帮你省了多少 Token 和时间。执行与度量一体：做完任务顺手记一笔，省了多少一目了然。适用于办公生产力执行、AI 用量洞察、提效度量与自动化决策场景。"
version: 1.0.6
author: Elisabeth15501
tags:
  - 办公生产力
  - 效率工具
  - 数据分析
  - token提效
  - 用量洞察
categories:
  - 办公生产力
  - 数据分析
  - 效率工具
triggers:
  - intent: usage_overview
    description: 查看账本里记录的 Token / 耗时用量与趋势（基于你记的账，零上传）
    examples:
      - "我最近 7 天用了多少 Token？"
      - "帮我看看这周 AI 办公消耗了多少"
      - "我账本里记了多少 Token？"
      - "统计一下我这个月的 AI 用量"
  - intent: efficiency_review
    description: 基于账本 baseline 度量「用 AI 办公省了多少 Token / 时间」
    examples:
      - "生成我的提效报告"
      - "用 AI 办公帮我省了多少？"
      - "我这个月提效怎么样？"
      - "做个周度提效汇总"
      - "做个办公提效复盘"
  - intent: task_diagnosis
    description: 追问哪个任务最费 / 最省 Token、最该自动化
    examples:
      - "哪个任务类型最费 Token？"
      - "哪个任务最省时间？"
      - "哪种办公任务最该自动化？"
      - "什么任务 AI 帮我最多？"
  - intent: report_visualization
    description: 生成 Token 用量 / 提效的可视化报告（HTML / 图表）
    examples:
      - "生成一份 Token 用量报告"
      - "把我的 AI 用量做成图表"
      - "给我出个提效 HTML 报告"
  - intent: task_execution
    description: 直接帮你做办公任务并生成可交付物（周报/纪要/数据分析/文档整理/PPT 大纲），执行后自动建议记账
    examples:
      - "帮我写一份周报"
      - "整理一下会议纪要"
      - "分析这个 CSV 算关键指标"
      - "把这篇文章提炼成要点"
      - "给这个主题出个 PPT 大纲"
  - intent: import_bookkeeping
    description: 自然语言记账，或接入宿主用量事件（若宿主提供）
    examples:
      - "记一笔：写周报花了 1800 token"
      - "记一笔：写周报花了 1800 token"
      - "我刚写完周报，用 AI 花了 1800 token"
non_triggers:
  - "帮我发一封邮件（本技能不代发邮件）"
  - "删掉我桌面上的文件（不执行危险系统操作）"
  - "连外部数据库改数据（不联网、不碰外部系统）"
tools:
  - filesystem
network:
  outbound: false
  note: "联网推荐（clawhub/lightmake 技能市场）已禁用，仅保留本地推荐；核心执行/度量/报告全流程纯本地、零联网、不读密钥"

metadata:
  openclaw:
    requires:
      python: ">=3.10"
      bins: [python3]
    env: []
    platform: ["tianxi", "openclaw", "linux", "macos", "windows"]
---

# 办公室 Token 洞察与提效助手（office-token-booster）

> 看清你用 AI 办公到底省了多少 Token 和时间——它**既帮你做**周报 / 纪要 / 数据分析 / 文档整理 / PPT 大纲，又自动记下每次省了多少，让「提效」从一句空话变成可复盘的数字。

## 这个技能解决什么

办公室里大量时间花在**重复、低创意**的事情上：整理会议纪要、从杂乱 Excel 算关键指标、每周写周报、把长文档压成要点。这些事你可以用任意 AI 工具做完——但**做完之后，你往往说不清到底省了多少**。

`office-token-booster` 是一个**提效执行与度量账本**：你把每次任务的「笨办法估计成本 vs 实际 AI 成本」记一笔，它**既帮你把办公任务直接做成可交付物，又帮你量化节省的 Token / 时间、按类型与周趋势可视化、并给出最该做成可复用模板的 ROI 建议**。它让"AI 到底帮我省了什么"从一句模糊的"提效了"，变成可复盘、可决策的数字。

> **定位边界（重要）**：本技能**执行**常见办公任务（周报 / 纪要 / 数据分析 / 文档整理 / PPT 大纲）并自动记账，但**不替代**专业排版 / 多模态生成类工具；执行层纯本地、不联网、不读密钥。节省值仍来自你填写的「笨办法」基准估计，非平台扣费。

## 核心卖点：Token 提效洞察可视化

很多办公助手只说"我帮你做了"，但**不说帮了多少**。本技能内置一份「提效账本」：

- 你每次交给我们一个任务，记一笔：传统做法（自己手搓 / 反复试错）大概要花多少 Token、多少分钟；用本技能做花了多少。
- 累积后生成**提效报告**：总节省 Token、节省比例、按任务类型的节省分布、每周趋势。
- 报告纯本地生成，**不联网、不上传你的任何内容**。

> 注意：节省值是基于你填写的"基准估计"计算的参考值，不是平台用量扣费数据。它用于建立"提效体感"，不是计费凭证。

## 能做什么（真实范围）

本技能**既执行、又度量**。下列能力均已落地（209 测试通过，另 3 个条件跳过）：

| 能力 | 输入 | 产出 |
|------|------|------|
| 任务执行 | 原始内容（本周要点 / 转录 / CSV / 长文 / 主题） | 结构化可交付物（Markdown，可选 HTML / docx / xlsx）+ 执行后自动记账建议 |
| 提效账本 | 任务记录 JSON（`baseline` 笨办法估计 vs `skill` 实际 AI 成本） | MD / HTML 提效报告（节省 Token、耗时、率、趋势） |
| Token 洞察可视化 | 账本 | 环形图 + 趋势折线图 + 本期 vs 上期对比卡 + 自动化 ROI Top N 卡 |
| 对话式诊断 | 账本 + 自然语言追问 | 锚定内核的结构化回答（类型排名 / 最差场景 / 周趋势 / 周期对比 / 可信度） |
| 长链路自动记账 | 一句话 / 宿主完成事件 | 建议记账 → 你确认 → 原子写回（默认 dry-run，带备份） |
| 宿主用量事件接入（可选） | 若宿主在任务完成时回传用量 | 用实测值记账；无回传时仍由你手填基准 |

## 怎么用

直接用自然语言触发，例如：

- "帮我写一份周报"（贴入本周要点，自动生成结构化周报 Markdown）
- "整理一下会议纪要"（贴入转录，自动抽取结论 / 待办 / 负责人 / 截止）
- "分析这个 CSV 算关键指标"（本地计算求和 / 均值 / 中位数，不联网）
- "把这篇文章提炼成要点" / "给这个主题出个 PPT 大纲"
- "生成我的提效报告"（或指向账本 JSON 的路径）
- "哪个任务类型最省 Token？" / "这周比上周怎么样？"
- "哪些任务最该做成自动化模板？"
- "把最近记的账本导出复盘"
- "我刚用 AI 写完了周报，花了 1800 token"（被动记账建议）

> 想要"帮我整理会议纪要 / 分析 Excel / 写周报"等**执行类**能力？本技能**已经覆盖**周报 / 纪要 / 数据分析 / 文档整理 / PPT 大纲；复杂 PPT 视觉排版、图文混排等专业产出，交给专业排版类 Skill 接手即可——我们负责把活干完、再把省了多少记下来。

## 快速开始（QUICKSTART）

> 完整 hands-on 实操（含 PowerShell 注意事项、常见任务示例）见同目录 **[QUICKSTART.md](QUICKSTART.md)**。下面给出核心闭环速览。

零依赖（纯标准库 Python ≥3.10），从项目目录即可跑通「做任务 → 自动记账 → 看报告」闭环。

**1) 初始化账本（仅首次）**

```bash
python scripts/executor.py --init-ledger examples/ledger.json
```

**2) 执行任务并自动记账**

先把任务做成交付物，再走「预览 + 确认写回」把省了多少记进账本：

```bash
# 执行任务，拿到交付物（不写账本）
python scripts/executor.py --type 周报生成 --input 本周事件.txt --output 周报.md

# 预览记账（dry-run，安全）
python scripts/executor.py --type 周报生成 --input 本周事件.txt \
  --apply-ledger examples/ledger.json --skill-tokens 1800 --baseline-tokens 12000 --baseline-minutes 25

# 确认写回（加 --confirm-ledger）
python scripts/executor.py --type 周报生成 --input 本周事件.txt \
  --apply-ledger examples/ledger.json --skill-tokens 1800 --baseline-tokens 12000 --baseline-minutes 25 --confirm-ledger
```

> `baseline_*` = 你不用本技能、自己手搓 / 反复试错的估计成本；`skill_*` = 这次用 AI 实际花的。节省 = baseline − skill。**必须提供 baseline 才能写回**（护栏防污染账本）；不加 `--confirm-ledger` 永远是预览。

**3) 生成提效报告**

```bash
python scripts/report_engine.py examples/ledger.json --format html --output 提效报告.html
# 一句话摘要：加 --summary；Markdown：--format markdown
```

**4) 对话式追问（内核 API）**

```python
from scripts.diagnose import load_ledger, diagnose
from scripts.qa import answer_followup
d = diagnose(load_ledger("examples/ledger.json"))
print(answer_followup(d, "哪个任务类型最省 Token？"))
print(answer_followup(d, "这周比上周怎么样？"))
```

**5) 宿主用量事件接入（可选）**

```bash
# 若宿主平台在任务完成时回传用量事件，则读取实测值；无回传则跳过，不影响其它功能
python scripts/host_cost.py --days 7
# 把真实用量导成账本草稿（dry-run 预览，不写盘；加 --apply 才写回）
python scripts/ledger_agent.py examples/ledger.json --import-host --days 7
```

**全量测试（源码仓库内，含测试套件；分发包不含测试）：**

```bash
pytest tests/ -q --alluredir=allure-results
```

## 提效账本数据格式

把任务记录保存为 JSON（如 `examples/ledger.json`），每一条：

```json
{
  "tasks": [
    {
      "date": "2026-08-08",
      "type": "会议纪要",
      "baseline_tokens": 12000,
      "skill_tokens": 3000,
      "baseline_minutes": 25,
      "skill_minutes": 3,
      "note": "2 小时录音转写"
    }
  ]
}
```

然后说"生成提效报告"，技能调用 `scripts/report_engine.py` 产出报告。

## 对话式提效诊断（推荐流程）

技能支持**先给一页摘要 + 图表、再追问、最后按需展开完整报告**的对话式诊断，让你按需深挖：

1. **一页摘要（首屏）**：技能先调用 `report_engine.py --summary` 输出一页精简摘要（核心数字 + 提效主力 + 一句话结论 + 数据可信度 + 方法论说明），配合环形图一屏看完，不淹没细节。
2. **追问（基于诊断结果、不编造）**：例如
   - "哪个任务类型节省最多？" → 按 `by_type` 排序回答
   - "哪个场景最不省？" / "按周趋势如何？" → 从结构化结果精确取数
   - "有哪些任务明细？" → 列出每条任务省了多少
   - "这些数字怎么算出来的 / 可信吗？" → 解释方法论与基线护栏（caveats）
   - 追问由 `scripts/qa.py` 处理，所有回答都**锚定在 `diagnose()` 产出的结构化 Diagnosis 上**，不做无数据支撑的猜测。
3. **展开完整报告**：当你说"生成完整报告"，技能调用 `report_engine.py` 输出完整明细（任务类型 / 周趋势 / 执行情况 / 产出物 / 洞察建议 / 数据可信度提示），供需要落地细节时使用。

> 一页摘要与完整报告共用同一份 `Diagnosis` 内核，追问题也不重新计算，保证首屏、追问、完整报告三处数字完全一致。

## 长链路自动记账

技能提供**主动记账管道**：任务完成后，让 Agent 自动把这笔账记回 `examples/ledger.json`，减少你手填负担。

由 `scripts/ledger_agent.py` 提供，三个动作可组合：

1. **建议生成（propose_entry）**：`python ledger_agent.py <examples/ledger.json> --type 周报生成 --skill-tokens 1800`
   - 用该类型的历史均值预填 `baseline`（你手搓成本）估计；你也可显式传 `--baseline-tokens` / `--baseline-minutes` / `--skill-minutes` / `--note` 覆盖。
   - 未提供或新类型时，会标记「估算字段」并提醒你补填真实手搓成本。
2. **待自动化建议（--targets）**：`python ledger_agent.py <examples/ledger.json> --targets`
   - 按历史基线从高到低，列出最该做成可复用模板的任务类型。
3. **写回账本（append_entry）**：默认 **dry-run 仅预览**，加上 `--apply` 才真正写回（写前自动备份为 `<ledger>.bak`，原子替换）。
   - 预览会显示写回前后「任务数 / 节省 Token / 节省分钟」的变化，方便你确认。

完整流程编排见 `run_long_chain(ledger_path, task_type, ...)`：load_ledger → diagnose → propose → append → 重新 diagnose。

> 安全默认：不加 `--apply` 绝不改动你的账本文件。

## 对话式自动记账编排

主动记账与对话式诊断、报告**串成一条连续对话**——用户说一句，技能理解意图并调用对应内核能力，任务完成时还能自动建议记账。

由 `scripts/conversation.py` 提供：

- **意图路由（classify + handle）**：把一句话归到 记账 / 确认 / 取消 / 生成摘要 / 生成完整报告 / 待自动化建议 / 追问 等意图，再分派给对应内核能力。
- **自然语言记账**：说「记一笔 周报生成 花了1800 token 5分钟」，自动解析类型与成本，用该类型历史均值预填 baseline 估计并预览；你回「确认」才写回（ledger_agent 内部仍是 dry-run + 备份）。
- **被动记账建议**：说「我刚生成了周报，花了1800 token」也能识别为记账意图（完成动词 + 成本数字），并模糊匹配到账本已有类型名，降低手填负担。
- **连续对话**：记账前后都能直接追问（qa 接地）、看摘要（report_engine）、看自动化建议（ledger_agent），所有数字来自同一份 `Diagnosis`，三处始终一致；确认写回后还会主动弹一条「最该自动化」的建议。

交互示例：`python conversation.py <examples/ledger.json>` 进入 REPL；也可在 Python 里 `handle(ledger, text, state)` 单轮调用，便于 Skill / 对话 UI 集成（state 保存待确认条目）。

## 类型字典消歧

自然语言里的任务类型名需要**准确落到账本标准名**——靠「子串模糊匹配」会有歧义：说「生成了周报」只抓到短词「周报」，若账本里同时有「周报生成」和「周报审核」就会误判；全新类型也容易被误判。

为此引入 **`scripts/type_registry.json` 类型字典**（标准名 ↔ 别名/关键词映射），让类型识别从「猜」变成「查表」：

- `_detect_type` 匹配优先级：① 账本已知标准类型精确出现 → ② 类型字典标准名/别名命中 → ③ 短语抓取（记账词或完成动词后跟类型名）+ 字典模糊匹配 → ④ 都无命中则作为**全新类型候选**返回（预览时提示你确认，并建议在字典补别名）。
- 词典缺失/损坏时自动降级为空字典（退化为无字典的模糊匹配），不影响其他功能。
- 新增类型时，只需在 `type_registry.json` 的 `types` 里加一个标准名 + 别名列表，即可让以后的自然语言记账准确识别。

实地验证脚本见 `tests/test_v05.py`：`python tests/test_v05.py` 自带临时账本跑完整流程，断言类型字典消歧正确、三层数字同源一致。

## Skill 触发流（宿主对话事件）

**让「用户完成一次任务」这件事本身自动建议记账**——不必再记着去敲那句命令。

由 `scripts/skill_bridge.py` 提供：

- **完成信号识别（is_completion_event）**：一句话里含「生成了 / 做好了 / 写完了 / 交付了 …」等完成动词即视为「任务完成事件」。再细分信心：动词+成本数字 = high（直接给完整建议）；仅动词、无成本 = medium（仍触发，并提示补成本）；纯闲聊/问答 = low（不触发，交普通对话）。
- **事件桥接（on_conversation_event）**：把一条**宿主对话事件**（如用户说「我刚生成了周报，花了1800 token 5分钟」）翻译成 `conversation.handle()` 的调用，**内部暂存待记账条目到 state["pending"]**，返回结构化 `TriggerResult`（是否触发 / 建议文案 / 待记账类型 / 信心），供 Skill / UI 渲染成「要不要记一笔？」卡片。
- **类型字典兜底（_lenient_type）**：对于「写完了那份PPT」这类**没给成本、且别名大小写不符**的完成句，对话层 `_detect_type` 认不出类型时，桥接层用类型字典做大小写不敏感兜底匹配，仍能落到标准名「PPT制作」。
- **确认才写回（安全默认不变）**：触发流只「建议」，绝不在用户确认前落盘。用户回「确认」交给普通对话流 `handle("确认", state)` 写回。

> 本模块**平台无关**：只认通用的「对话事件」契约，天禧 / OpenClaw 等宿主均可接入。

宿主技能侧集成示例：

```python
from skill_bridge import on_conversation_event
state = {}
# 宿主在完成一次办公任务后，把真实用量随事件一并传来（事件携带 event["cost"]）
res = on_conversation_event("examples/ledger.json", {
    "role": "user", "text": "我刚生成了周报",
    "cost": {"skill_tokens": 1800, "skill_minutes": 5},
}, state)
if res.triggered:
    show_suggestion(res.suggestion)   # 渲染「建议记账：周报生成 … 确认？」
```

实地验证脚本见 `tests/test_v06.py`：`python tests/test_v06.py` 自带临时账本，断言高/中信心完成事件触发、非完成事件不触发、触发默认 dry-run 不写账本、确认后写回且三层数字同源一致。

## 真实闭环（宿主用量事件接入）

成本默认由**用户自报**（"花了1800 token"），也支持**让宿主平台把任务的真实用量直接随事件传进来**，把"提效"从"自报"变成"实测"——即"对比笨办法 vs 本技能"的硬数据来源。

由 `scripts/skill_bridge.py`（升级）与 `scripts/host_hook.py`（新增）共同提供，**内核与三层外壳 + 编排层仍零改动**：

- **真实成本捕获（event["cost"]）**：宿主在完成一次办公任务后，可在事件里带上 `{"skill_tokens": N, "skill_minutes": M}`。桥接层优先采用这个**实测值**，而非从自然语言里解析数字；`TriggerResult.cost_source` 标记为 `"event"`（自报则为 `"text"`），供 Skill / UI 标注"本技能实测消耗"。
- **结构化完成标志（event["completed"]）**：宿主也能显式声明"任务已完成"（`completed=True`），优先级高于文本里的完成动词，便于平台把"产出物落地"这个动作直接映射成记账建议。
- **宿主钩子示例（host_hook.py）**：一个**平台无关**的适配器，演示宿主如何把完成事件归一化成通用 `event` dict（`build_completion_event`）并接进 `on_conversation_event`（`on_task_completed`）。它**不 import 任何平台 SDK、不发网络请求、不硬编码密钥**，满足 OpenClaw / 天禧 安全红线；平台-specific 的 glue 由平台侧实现。

> 落地保证：宿主回报 `skill_tokens=1800` 的事件经触发→确认后，写回账本的条目 `skill_tokens` 即为 1800（非用户手敲），且确认消息 / 内核 Diagnosis / 摘要报告三处节省率完全一致（`tests/test_v07.py` 已断言）。

实地验证脚本见 `tests/test_v07.py`：`python tests/test_v07.py` 自带临时账本，断言真实用量事件触发且 `cost_source=event`、确认后写回采用宿主真实用量、三层数字同源、源码未绑定具体平台；`python scripts/host_hook.py --demo` 可看宿主完成事件如何触发记账建议。

## 任务执行引擎（既做又记）

技能**直接把办公任务做成可交付物**，并顺手把这笔账记回 ledger。由 `scripts/executor.py` 提供，**纯标准库、零依赖、不联网、不调密钥**。

支持的任务类型与做法：

| 类型 | 输入 | 产出 |
|------|------|------|
| 周报生成 | 本周要点 / 事件（子弹点） | 结构化周报（概览 / 重点 / 风险 / 下周计划） |
| 会议纪要 | 转录要点 | 结论 / 待办（含负责人+截止解析）/ 遗留问题 |
| 数据分析 | CSV 文本或路径 | 字段指标表（求和 / 均值 / 最小 / 最大 / 中位数 / Top 类别），**本地 stdlib 计算** |
| 文档整理 | 长文 / Markdown | 大纲 + 核心要点 + 一句话总结 |
| PPT 大纲 | 主题 + 要点 | 5 页幻灯片大纲（交排版类 Skill 接手视觉） |

命令行用法（宿主 Agent 或用户直接调用）：

```bash
# 周报：贴入要点 → 生成 Markdown
python scripts/executor.py --type 周报生成 --input 本周要点.txt --output 周报.md

# 会议纪要：从转录抽取结论与待办
python scripts/executor.py --type 会议纪要 --input 转录.txt --output 纪要.md

# 数据分析：本地算指标（不联网）
python scripts/executor.py --type 数据分析 --input data.csv --output 分析.md

# 可选导出：周报 → Word、数据分析 → Excel（缺失 python-docx / openpyxl 时自动降级为 md / csv，零依赖默认不受影响）
python scripts/executor.py --type 周报生成 --input 本周要点.txt --output 周报 --format docx
python scripts/executor.py --type 数据分析 --input data.csv --output 分析 --format xlsx

# 执行完自动记账：把这笔任务的实测成本记回账本（缺 baseline 会被护栏拦截，提示补填）
python scripts/executor.py --type 周报生成 --input 本周要点.txt \
    --apply-ledger examples/ledger.json --skill-tokens 1800 --skill-minutes 5
#   加 --confirm-ledger 才真正写回；否则仅 dry-run 预览
```

> **导出说明（优雅降级）**：`--format docx/xlsx` 为**可选依赖**（python-docx / openpyxl），不计入技能的核心零依赖默认。未安装时自动降级——docx 回落 Markdown、xlsx 回落 CSV，功能不中断。安装见 `requirements-optional.txt`。

> 闭环设计：执行产出后调用 `ledger_agent.run_long_chain` 自动建议记账，**复用 P0 写回护栏**——未补「笨办法」baseline 时拒绝写回，不污染账本。这样「做」和「记」合成一步，省了多少自动可复盘。

宿主技能侧集成（天禧 / OpenClaw 皆可）：用户说「帮我写周报」→ 宿主把原始要点交给 `executor.execute("周报生成", text)` 拿到 Markdown → 渲染给用户，并带 `event["cost"]` 调 `propose_ledger` 记回。宿主钩子 `scripts/host_hook.py` 提供 `on_executor_completed(ledger_path, task_type, event, apply)`，把 `executor` 完成事件里的真实用量（`event["cost"]` 中的 `skill_tokens/skill_minutes`）直接记回 ledger，无需重复写对接代码。

## 设计与合规

- **全部本地处理**：报告在本地生成，不向任何外部域名发送你的内容。
- **无硬编码密钥**：脚本不读取任何 API Key / Token。
- **数据最小化**：只读写你**显式提供/指定**的路径（输入文件、账本、`--output`），**不做目录遍历式扫描**；除下方「宿主用量接入」明确说明的可选读取外，不访问你项目目录之外的任何文件。
- **宿主用量接入（可选、需显式触发）**：只有你主动执行「导入宿主用量」类命令时，才会**只读**本机宿主指定目录下的用量文件（见下条）。默认不启用，未启用时技能完全按「用户自报成本」工作。
- **宿主数据读取范围**：可选接入**只读**宿主数据根下的用量索引文件与 trace 文件（限定后缀、限定扫描深度与文件数上限、跳过符号链接），**只解析 token / 耗时 / 模型 / 日期 / 任务类型**五类字段，不读取提示词正文、不写回宿主目录、不上传任何内容。该目录**不在技能包内**，属你本机环境。
- **不执行系统命令**：技能内部**不调用任何系统命令**（无 shell 执行、无子进程、无动态求值执行）；命令行由宿主或你本人调用，技能只负责被调用后的纯本地计算与文件读写。
- **推荐 Skill 的真实来源**：报告中的「推荐 Skill」由**内置静态规则表**按任务类型本地匹配产生，不联网获取；推荐条目的节省数字与来源链接均引自第三方项目的公开自述（README / benchmark），**未经本技能实测验证**，仅供参考。本技能不代为安装任何第三方 Skill，也不会生成任何安装命令——是否安装、如何安装由你自行判断。
- **开源协议**：MIT，可自由学习、修改、再分发（部分技能市场平台统一采用 MIT-0 条款发布，属平台侧协议，不改变本仓库的 MIT 授权）。
- **发布者自用脚本（不随分发包提供）**：`scripts/clawhub_client.py` / `scripts/skillhub_client.py`（技能市场上传客户端，发布者自己调 CLI 上传用）、`scripts/security_preflight.py`（开发期合规预检）、`tools/`（打包与站点构建脚本）、`tests/` 与开发期 requirements / `pytest.ini`，均为**发布与开发自用**内容，**不属于本技能的可用能力**；核心执行 / 度量 / 报告链路不 import、不依赖它们，缺失时全部功能不受影响。

## 范围说明（Non-goals）

- **不做专业排版 / 多模态生成**：执行层产出结构化 Markdown / HTML 交付物；复杂 PPT 视觉排版、图文混排交由专业排版类 Skill 接手（我们做到「大纲 + 要点 + 指标」，你把排版交出去）。
- **不读平台计费 / 不联网 / 无密钥**：默认节省值来自你填的基准估计。执行层纯本地模板渲染 + stdlib 计算，不调 LLM、不发网络请求、不读任何密钥，满足 OpenClaw / 天禧 安全红线。若宿主平台在任务完成时回传用量事件（如本机 WorkBuddy 的本地用量目录），可**可选**接入并**只读本机**用量来补全 skill 实测成本；无回传数据时自动跳过，技能仍按「用户自报成本」正常工作。
- 不自动执行会改动你系统的危险操作（如删除文件、发送邮件）；写回账本默认 dry-run，需你确认（`--apply`）才落地。
- 当前版本聚焦"办公文本类任务"的执行与度量；多模态生成在后续版本扩展。
