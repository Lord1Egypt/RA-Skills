---
name: lgd-gov-guard
description: >-
  Check government AI applications against three governance rules before they go live: whether data has a legal basis, whether every output carries evidence, and whether risky actions pass a gate.

  lgd-gov-guard — 把 LGD 三律（有籍·有证·有门禁）翻译进政务 / 公共部门 AI 应用（决策辅助·公开答复·数据治理）的合规守门器，对 AI 系统做三律自评与门禁判定（零依赖）。
slug: lgd-gov-guard
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
display_name: 政务AI治理守门
display_name_en: Government AI Governance Guard
agent_created: true
author: XLGD · 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
copyright: XLGD · SynomosAI
description_zh: "lgd-gov-guard — 把 LGD 三律（有籍·有证·有门禁）翻译进政务 / 公共部门 AI 应用（决策辅助·公开答复·数据治理）的合规守门器，对 AI 系统做三律自评与门禁判定（零依赖）。"
description_en: "Check government AI applications against three governance rules before they go live: whether data has a legal basis, whether every output carries evidence, and whether risky actions pass a gate. Use it for decision-support tools, public reply bots and cross-department data sharing in public-sector projects."
classification:
  skillhub: ["ai-governance"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [lgd-gov-guard, AI 治理, 政务AI, 数据治理]
read_when:
  - 政务 AI 决策辅助系统生成政策建议前要校验数据来源法定授权
  - 公共部门自动回复机器人涉及敏感信息时要三律门禁判定
  - 跨部门共享请求或隐私脱敏输出前要自主身份与权限审计
  - AI 应用启动自检要确认自身逻辑未违规依赖外部权限
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/gov_guard.py
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
  network: true
  filesystem: true
  subprocess: true
  scope: project-dir-only   # 只处理调用者指定目录；外发需人逐次确认，无预设接收端
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
1. Before a government AI decision-support system generates policy advice, to verify the data source holds a legal authorization basis.
2. When a public-sector auto-reply bot touches sensitive information, to trigger the three-laws gate determination.
3. Before internal data-governance tools process cross-department sharing requests or desensitized output, to run autonomous identity and permission audits.
4. When an AI app boots in self-check mode to confirm its own logic does not rely on external permissions or fall short of the LGD standard.

### Usage
1. Run `python gov_guard.py` directly as the main entry point — no extra environment dependencies.
2. Core parameters: `--input_data` (the text or dataset under evaluation) and `--mode` (decision / reply / governance).
3. To read the logic, inspect the three-laws determination functions and rule set defined in `gov_guard.py`.

### Workflow
1. Load the government AI content or data stream to be checked into a temporary workspace.
2. The script initializes the LGD three-laws (registered · evidenced · gated) rule engine and sets thresholds.
3. The system independently evaluates data source, authorization evidence and access permissions in parallel.
4. Produce the internal compliance score and the verdict on whether the zero-dependency standard is met.
5. Emit an audit report with detailed risk points to the standard log file.
6. Based on the verdict, automatically release or block the downstream AI task.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. 政务 AI 决策辅助系统在生成政策建议前，需校验数据来源是否具备法定授权依据。
2. 公共部门面向公众的自动回复机器人涉及敏感信息时，需触发三律门禁判定。
3. 内部数据治理工具在处理跨部门共享请求或隐私脱敏输出前，进行自主身份与权限审计。
4. AI 应用启动自检模式以确认其自身逻辑未违规依赖外部权限及不符合 LGD 标准。

### 用法
1. 直接调用 `python gov_guard.py` 作为主入口脚本运行，无需额外环境依赖。
2. 核心参数包括：`--input_data` (待评估的文本或数据集), `--mode` (决策/答复/治理)。
3. 若需读取逻辑细节，可直接阅读分析 `gov_guard.py` 源码中定义的三律判定函数与规则集。

### 流程
1. 输入端加载待校验的政务 AI 内容或数据流至临时工作区。
2. 脚本初始化 LGD 三律（有籍·有证·有门禁）规则引擎并配置阈值。
3. 系统依次对数据来源、授权证明、访问权限进行独立并行评估。
4. 生成内部合规评分及是否符合“零依赖”标准的判定结果。
5. 输出包含风险点明细的审计报告至标准日志文件。
6. 根据判定结果自动触发放行或阻断后续 AI 任务执行动作。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「政务大模型上线前要过合规」 / "our government model needs a compliance check before launch"
- 「AI 给的政策建议有依据吗」 / "is this AI policy advice backed by any source"
- 「自动回复机器人碰到敏感信息」 / "the auto-reply bot is touching sensitive data"
- 「部门间数据共享怎么审」 / "how do we review data sharing between departments"
- 「政务系统要自查权限边界」 / "public sector system needs to audit its own permissions"
- 「公共部门AI怎么留证据」 / "how should a public agency document AI decisions"

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
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-gov-guard
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-gov-guard/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
