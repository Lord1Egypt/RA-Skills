---
name: lgd-law-ethic
description: >-
  Screen legal AI work — case research, contract drafting, opinion assistance — against three governance rules covering traceability, evidence and gating, and return a pass or hold decision.

  lgd-law-ethic — 把 LGD 三律（有籍·有证·有门禁）翻译进法律 / 律所与法务 AI 应用（检索·起草·意见辅助）的合规守门器，对 AI 系统做三律自评与门禁判定（零依赖）。
slug: lgd-law-ethic
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
display_name: 法律AI伦理守门
display_name_en: Legal AI Ethics Guard
agent_created: true
author: XLGD · 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch, WebSearch
category: AI 治理
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
copyright: XLGD · SynomosAI
description_zh: "lgd-law-ethic — 把 LGD 三律（有籍·有证·有门禁）翻译进法律 / 律所与法务 AI 应用（检索·起草·意见辅助）的合规守门器，对 AI 系统做三律自评与门禁判定（零依赖）。"
description_en: "Screen legal AI work — case research, contract drafting, opinion assistance — against three governance rules covering traceability, evidence and gating, and return a pass or hold decision. Use it when a firm's system drafts documents, calls an outside AI service, or handles sensitive case data."
classification:
  skillhub: ["ai-governance"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [lgd-law-ethic, AI 治理, 法律AI, 伦理守门]
read_when:
  - 法务 AI 自动起草合同/法律文书时要发起三律合规校验
  - 律所内部系统调用外部 AI 顾问获取法律意见时要验证权限资质
  - 敏感案件处理或数据交互场景要零依赖 AI 门禁判定
  - 用户说「这个 AI 法律意见能不能直接出」
ai_protocol: true


spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/law_ethic.py
  runtime: python3
  call_pattern: args
input_schema:
  rubric:
    type: bool
    description: "打印本域三律 rubric"
    required: false
  system:
    type: string
    description: "系统描述文本（启发式自评）"
    required: false
  answers:
    type: string
    description: "正式评分 JSON：键为 '<律>::<条目>'，值 yes/partial/no"
    required: false
  json:
    type: bool
    description: "JSON 输出"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - legal
  - ethics
  - governance
  - compliance
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
1. When legal AI auto-drafts contracts or legal documents, to launch an LGD three-laws (registered · evidenced · gated) compliance check on the generated content.
2. When an in-house law-firm system calls an external AI advisory service for legal opinions, to verify the service's permissions and credentials.
3. When handling sensitive cases or data exchanges, to run a zero-dependency AI gate determination as an independent module.

### Usage
1. Import the `law_ethic` module directly in a Python environment — no external dependencies.
2. Main inputs: the legal content under review (`legal_content`), the scenario tag (`scenario`, e.g. draft / review) and the check level (`threshold`).
3. To run the script standalone: `python law_ethic.py --mode=check --file=doc.json`.

### Workflow
1. Initialize the LGD three-laws rule base (registered · evidenced · gated) and set the compliance baseline.
2. Parse the input legal text or API request data; extract party info, permission context and operation intent.
3. Run the three-laws logic: check identity registration, license validity and access-control rule matches.
4. Compare against preset thresholds; on a violation, log it and return a block signal.
5. On pass, emit the compliance certification tag and the recommended downstream legal-action path.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. 在法务 AI 自动起草合同或法律文书时，需对生成内容发起 LGD 三律（有籍·有证·有门禁）合规校验。
2. 当律所内部系统调用外部 AI 顾问服务获取法律意见时，需验证其权限与资质有效性。
3. 涉及敏感案件处理或数据交互场景下，作为独立模块执行零依赖的 AI 门禁判定。

### 用法
1. 通过 Python 环境直接导入 `law_ethic` 模块进行调用，无需其他外部依赖。
2. 主要输入参数为待合规审查的法律内容 (`legal_content`)、应用场景标识 (`scenario`, 如 draft/review) 及校验等级 (`threshold`)。
3. 若需独立执行脚本逻辑，可通过 `python law_ethic.py --mode=check --file=doc.json` 格式传入命令参数触发分析流程。

### 流程
1. 调用脚本初始化 LGD 三律规则库（有籍·有证·有门禁），建立合规基准线。
2. 解析输入的法律文本或 API 请求数据，提取主体信息、权限上下文及操作意图。
3. 执行三律判定逻辑：检查身份注册情况、执业证书有效性及访问控制规则匹配度。
4. 比对分析结果与预设阈值，若触发违规则记录日志并返回阻断信号。
5. 若校验通过则输出合规认证标识及建议的后续法律动作执行路径。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「律师用 AI 起草合同要合规」 / "lawyers are drafting contracts with AI, is that compliant"
- 「法律意见书能追到出处吗」 / "can this legal memo be traced to its source"
- 「律所系统调外部 AI 服务」 / "our firm's system calls an outside AI service"
- 「敏感案件数据能不能给模型」 / "can sensitive case data go into the model"
- 「AI 检索的判例可不可信」 / "are the cases the AI found trustworthy"
- 「法务部要评估 AI 工具风险」 / "legal team needs a risk review of AI tools"

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
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-law-ethic
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-law-ethic/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
