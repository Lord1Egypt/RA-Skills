---
name: lgd-fin-guard
description: >-
  Screen a financial AI system against the three laws of registered, evidenced and gated before it goes live, so licensed advisory, risk-control and anti-money-laundering use cases hold up.

  lgd-fin-guard — 把 LGD 三律（有籍·有证·有门禁）翻译进金融 / 持牌机构 AI 应用（投顾·风控·反洗钱）的合规守门器，对 AI 系统做三律自评与门禁判定（零依赖）。
slug: lgd-fin-guard
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
display_name: 金融AI合规守门
display_name_en: Finance AI Compliance Guard
agent_created: true
author: XLGD · 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
copyright: XLGD · SynomosAI
description_zh: "lgd-fin-guard — 把 LGD 三律（有籍·有证·有门禁）翻译进金融 / 持牌机构 AI 应用（投顾·风控·反洗钱）的合规守门器，对 AI 系统做三律自评与门禁判定（零依赖）。"
description_en: "Screen a financial AI system against the three laws of registered, evidenced and gated before it goes live, so licensed advisory, risk-control and anti-money-laundering use cases hold up. It checks licence qualifications, verifies external data sources, and gates high-sensitivity decisions such as credit approval and large transfers."
classification:
  skillhub: ["ai-governance"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [lgd-fin-guard, AI 治理, 金融合规, 持牌机构]
read_when:
  - 金融 AI 系统上线前要确认算法模型具备投顾/风控持牌资质
  - 外部数据接入前要校验源端是否满足有籍·有证身份认证
  - 高敏感交易决策（信贷审批/大额转账）触发前要准入门禁判定
  - 用户说「这个风控模型上线合规吗」
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/fin_guard.py
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
1. Before a financial AI system goes live, to confirm the algorithm model holds advisory or risk-control licensed qualifications.
2. Before external data ingestion, to check that the source meets the "registered · evidenced" identity-authentication requirement.
3. As the admission gate before high-sensitive transaction decisions (credit approval, large transfers) are triggered.

### Usage
Call the core script `fin_guard.py` to run the compliance check, with configurable check dimensions. Example: `python fin_guard.py --mode=guard --entity=<AI system id> --scope=qualification/permission`. Here `--mode` is `audit` or `gate`, and `--entity` is the model or business ID under check.

### Workflow
1. Identify the AI application module under compliance verification and its associated business scenario.
2. Run `python fin_guard.py`, passing the entity ID and the three-laws determination mode.
3. The script reads the files and performs the internal LGD three-laws (registered · evidenced · gated) self-assessment.
4. Generate the compliance verdict report, stating pass/reject and the specific missing items.
5. The system automatically allows passage or blocks the data flow based on the result.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. 金融 AI 系统上线前，需确认算法模型具备投顾或风控持牌资质。
2. 外部数据接入前，校验源端是否满足“有籍·有证”身份认证要求。
3. 高敏感交易决策（如信贷审批、大额转账）触发前的准入门禁判定。

### 用法
调用核心脚本 `fin_guard.py` 执行合规检查逻辑，支持参数配置校验维度。例如：`python fin_guard.py --mode=guard --entity=<AI 系统标识> --scope=资质/权限`，其中`--mode`设定为`audit`(审计)或`gate`(门禁)，`--entity`填入待校验的模型或业务 ID。

### 流程
1. 确认待合规验证的 AI 应用模块及其关联的业务场景需求。
2. 执行 `python fin_guard.py` 命令，传入实体标识与三律判定模式参数。
3. 脚本读取文件资料对 LGD 三律（有籍·有证·有门禁）进行内部自评计算。
4. 生成合规判定报告，明确通过/拒绝状态及具体缺失项。
5. 系统根据结果自动执行允许通行或阻断数据流的动作。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「投顾算法上线前要查牌照吗」 / "does our robo-advisor need a licence check"
- 「外部数据源进模型前怎么核验」 / "verify data sources before they feed the model"
- 「大额转账的自动决策要加门禁」 / "gate automated decisions on large transfers"
- 「风控模型要不要做合规自评」 / "should the risk model run a compliance review"
- 「反洗钱系统能过监管检查吗」 / "will our AML system pass regulatory scrutiny"
- 「持牌机构的智能应用怎么过审」 / "how do licensed firms get AI approved"

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
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-fin-guard
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-fin-guard/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
