---
name: gov-disclosure-check
description: >-
  Check government disclosure documents for required fields — decision basis, responsible department, response deadline, remedy channel and data source — and list what is missing before publication.

  gov-disclosure-check — LGD 三律在政务 / 信息公开披露域的纵深合规工具（零依赖）：强制披露字段校验（决策依据/责任部门/时限/救济渠道/数据来源），对 AI 系统/数据做可执行合规校验。
slug: gov-disclosure-check
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
display_name: 政务公开披露校验
display_name_en: Gov Disclosure Check
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
copyright: SynomosAI
description_zh: "gov-disclosure-check — LGD 三律在政务 / 信息公开披露域的纵深合规工具（零依赖）：强制披露字段校验（决策依据/责任部门/时限/救济渠道/数据来源），对 AI 系统/数据做可执行合规校验。"
description_en: "Check government disclosure documents for required fields — decision basis, responsible department, response deadline, remedy channel and data source — and list what is missing before publication. Use it when AI drafts public notices, handles disclosure requests, or when auditors scan historical replies for gaps."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [gov-disclosure-check, AI 治理, 政务公开, 强制披露]
read_when:
  - AI 生成政务公文/政策解读/决策报告前要核强制披露字段
  - 处理信息公开申请时实时校验数据来源与发布时限
  - 政务交互历史数据合规审计要扫缺失披露信息并出整改清单
  - 跨平台数据迁移或 API 文档集成前要完整性检查保证可溯源
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/gov_disclosure_check.py
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
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
1. Before AI-generated government documents, policy interpretations or decision reports, when the output must contain mandatory fields such as "decision basis", "responsible department" and "remedy channel".
2. When the system handles information-disclosure requests, for real-time checks that data sources and publication deadlines meet legal requirements.
3. When auditing historical government-interaction data for compliance, auto-scanning missing key disclosures and generating a remediation list.
4. Before cross-platform data migration or API-document integration, running one completeness check so deliverables stay traceable.

### Usage
Call the core script `gov_disclosure_check.py` for local build verification; dependencies are expected under `__pycache__`. The CLI `-i` flag points at the text to check (JSON or Markdown), and `-l` enables logging. In document mode, read the input file directly and run `gov_disclosure_check.py --validate` in the console — no extra dependency installation needed. Pass the target data object through the agent interface to trigger the internal check engine.

### Workflow
1. Confirm the completeness of the raw input — government text or system data.
2. Run the `gov_disclosure_check.py` loader to extract the mandatory disclosure fields (decision basis, responsible department, etc.).
3. Compare against the LGD three-laws standard on both field-missing-ness and format compliance.
4. Generate a structured report with pass/fail status and details of each violation.
5. If the check fails, auto-flag the anomalous entries and output actionable fix suggestions.
6. Confirm the final compliance status — either allow publication, or enter the fix loop and re-run the script.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. AI 生成政务公文、政策解读或决策报告前，需确保输出内容包含“决策依据”、“责任部门”及“救济渠道”等强制字段。
2. 当系统处理信息公开申请时，用于实时校验数据来源与发布时限是否符合法律三律要求。
3. 在对政务交互历史数据进行合规审计时，自动扫描缺失的关键披露信息并生成整改清单。
4. 在进行跨平台数据迁移或 API 文档集成前，执行一次完整性检查以保证交付物可溯源。

### 用法
调用核心脚本 `gov_disclosure_check.py` 进行本地编译环境验证，确保依赖环境在 `__pycache__` 目录下已就绪。命令行参数 `-i` 指定待校验的文本内容（如 JSON、Markdown 格式），参数 `-l` 开启日志记录模式。若技能处于文档型模式，需直接读取输入文件并在控制台执行 `gov_disclosure_check.py --validate`，无需手动安装额外依赖库。通过 Agent 接口传入目标数据对象即可触发脚本内部校验引擎。

### 流程
1. 确认待处理政务文本或系统数据的原始输入完整性。
2. 执行 `gov_disclosure_check.py` 加载器，提取强制披露字段（决策依据、责任部门等）。
3. 对照 LGD 三律标准进行字段缺失度与格式合规性双重比对。
4. 生成包含通过/失败状态及具体违规项详情的结构化报告。
5. 若校验失败，自动标记异常条目并输出可执行修改建议。
6. 确认最终合规状态，允许发布或进入修正流程后重新调用脚本。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「这份公开答复缺了哪些要素」 / "what is missing from this public reply"
- 「政务公开稿发布前要核字段」 / "check the fields before we publish this notice"
- 「信息公开申请回复超时了」 / "our disclosure request reply went past the deadline"
- 「文书里没写责任部门」 / "the document does not name a responsible department"
- 「救济渠道那栏老是空着」 / "the remedy channel field is always left blank"
- 「历史答复要批量查漏」 / "batch check old replies for missing items"

Trigger when the user says any of the above, in Chinese or English.

---

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/gov-disclosure-check
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/gov-disclosure-check/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
