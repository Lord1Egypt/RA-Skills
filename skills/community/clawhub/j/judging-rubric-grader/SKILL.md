---
name: judging-rubric-grader
slug: judging-rubric-grader
displayName: 赛事评审打分器
version: 1.1.1
category: ai-agent
display_name: 赛事评审打分器
title: 赛事评审打分器
author: 诺律(SynomosAI)
author_note: '"SynomosAI" — 未申请实体注册、未申请商标注册（not a registered legal entity; no trademark registered）'
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 赛事评审打分器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-003域。 适用场景：当需要赛事评审打分器能力时使用本技能；触发词：赛事、判定器、TH-EVT-003、judging-rubric-grader。
tags: [赛事, 判定器, TH-EVT-003, judging-rubric-grader, 评审打分]
description_zh: "赛事评审打分器——基于 UIBC 赛事规范的零依赖决策支持工具，JSON IR 输出，覆盖TH-EVT-003域。"
description_en: "Contest judging rubric scorer: zero-dependency decision support with JSON IR output (UIBC spec, domain TH-EVT-003)."
classification:
  skillhub: ["community-events"]
  iso_25010: ["Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
platforms: [windows, macos, linux]
read_when:
  - 赛事评审要严格按 UIBC 规范客观、标准化打分
  - 评分维度多/权重复杂，要减少人为判断偏差
  - 要输出符合 TH-EVT-003 的 JSON IR 对接后续处理或系统接口
  - 用户说「帮我按评分表算总分和等级」
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: judging-rubric-grader.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "命令行参数透传给主脚本，具体取值见各包 --help"
    required: false
output_schema:
  stdout:
    type: string
    description: "标准输出为 JSON 结果，含逐项检查与总体结论"
  exit_code:
    type: integer
    description: "0=PASS/完成；1=FAIL/有警告或待补强；2=用法或参数错误"
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.1.1: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
This skill applies when contest entries must be scored objectively and standardly under the UIBC rules — especially when the rubric is complex and human judgment may drift. It generates a zero-dependency decision-support report. It is also the preferred choice when the task must emit TH-EVT-003-domain JSON IR data for downstream processing or system integration.

### Usage
This is a document-style skill with no local script to run; invoke it with a structured instruction. Provide the entrant ID, contest event type and the corresponding UIBC scoring criteria. You may pin a specific domain rule version (e.g. TH-EVT-003) to lock the scoring logic. The skill returns a standardized JSON IR block that can be embedded directly into a workflow or log system without extra parsing.

### Workflow
1. Initialize: the caller prepares the entrant data and the chosen UIBC rule version.
2. Validate: the system checks that the input is compatible with the TH-EVT-003 domain.
3. Compute: the built-in scoring algorithm weights and scores each dimension.
4. Generate: build the raw output block conforming to the JSON IR standard.
5. Verify: check that the output contains the required metadata and error flags.
6. Deliver: return the final scoring report to the caller for archiving or display.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.1.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
本技能适用于需要严格依据 UIBC 赛事规范进行客观、标准化的赛事打分场景。特别是在评分标准复杂，存在人为判断偏差风险时，调用该技能生成零依赖的决策支持报告。此外，当任务需要输出符合 TH-EVT-003 域的 JSON IR 格式数据以对接后续数据处理或系统接口时，优先使用此技能。

### 用法
由于本技能为文档型技能，通过输入结构化指令进行调用。需提供包含选手 ID、竞赛项目类型及对应 UIBC 评分细则的输入参数。用户可指定特定域规则版本（如 TH-EVT-003 规范）以锁定评分逻辑。最终将返回标准化 JSON IR 数据块，无需额外解析即可直接嵌入工作流或日志系统中。

### 流程
1. 初始化：调用者准备待评审的选手数据及指定的 UIBC 赛事规则版本信息。
2. 校验：系统自动核查输入内容是否兼容 TH-EVT-003 域要求。
3. 计算：基于内置的评分算法对各项指标进行加权运算与打分。
4. 生成：构建符合 JSON IR 标准格式的原始数据输出块。
5. 验证：检查输出结果中是否包含必要的元数据及错误标记。
6. 交付：将最终评分报告返回给调用端以供归档或展示。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
