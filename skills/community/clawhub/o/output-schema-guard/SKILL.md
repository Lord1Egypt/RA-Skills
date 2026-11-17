---
name: output-schema-guard
display_name: 结构化输出校验护栏（Schema Guard）
display_name_en: "Output Schema Guard"
description: >-
  Treat model output as untrusted input: validate JSON against a schema for required fields, types and allowed values, then return a fix hint instead of a raw parse error.

  当用户说『模型返回的JSON又崩了』『字段缺失对不上』『下游解析失败』『怎么强制LLM输出合规结构』，或要把 LLM 的 JSON/结构化输出接进代码（API/数据库/表单）时使用。把模型输出当『不可信外部输入』：用 schema 校验必填字段·类型·枚举，缺则给可执行的修复提示而非裸报错。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：结构化输出、JSON校验、schema guard、输出格式、字段缺失、模型输出解析、function calling、tool output。
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep
category: AI工程方法
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
read_when:
  - LLM 返回的 JSON 偶发缺字段或类型不对，导致下游解析崩溃
  - 要把模型输出接进数据库 / API / 表单，必须结构稳定
  - 在用 function calling / tool 定义，但模型回传参数不可信
  - 用户抱怨「这次能跑、下次就挂」的不稳定解析
tags: [结构化输出, schema校验, JSON guard, function calling, 输出格式, agent优化, 可靠性]
slug: output-schema-guard
title: 结构化输出校验护栏（Schema Guard）
copyright: SynomosAI
description_zh: "当用户说『模型返回的JSON又崩了』『字段缺失对不上』『下游解析失败』『怎么强制LLM输出合规结构』，或要把 LLM 的 JSON/结构化输出接进代码（API/数据库/表单）时使用。把模型输出当『不可信外部输入』：用 schema 校验必填字段·类型·枚举，缺则给可执行的修复提示而非裸报错。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：结构化输出、JSON校验、schema guard、输出格式、字段缺失、模型输出解析、function calling、tool output。"
description_en: "Treat model output as untrusted input: validate JSON against a schema for required fields, types and allowed values, then return a fix hint instead of a raw parse error. Use it when model responses break your API, database or form pipeline, or when tool-call arguments must match a fixed shape."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/schema_guard.py
  runtime: python3
  call_pattern: args
input_schema:
  schema:
    type: string
    description: "schema"
    required: true
  text:
    type: string
    description: "text"
    required: false
  file:
    type: string
    description: "file"
    required: false
  json:
    type: bool
    description: "json"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - json
  - schema
  - validation
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
1. When users report that model JSON output keeps breaking — missing fields cause downstream API or database parsing to fail — this skill performs structured repair.
2. When the project must force the LLM to return compliant structures (such as function-calling tool arguments) under specific schema constraints.
3. As a safety barrier for "untrusted external input", validating model output against the registered/evidenced/gated principles before any code logic executes.

### Usage
The core script is `schema_guard.py`, callable either as an imported Python module or directly from the command line. Two key parameters are required: the raw text or JSON string to be validated, and a schema-definition object (required fields, data types and enum-value lists). The skill loads and caches its internal logic in `__pycache__` automatically; no manual compilation is needed.

### Workflow
1. Receive the LLM output and the associated schema validation rules.
2. Run `schema_guard.py` for initialization and data loading.
3. Walk through the input fields, compare required items and type constraints, and check enum compliance.
4. Validate per the LGD Three Laws (registered · evidenced · gated); on error, do not simply raise.
5. Return repair guidance pinpointing the exact location, or the cleaned corrected data.
6. Record the validation status so the system can continuously improve the trustworthiness and format stability of future model output.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once produced)
- Version: 1.0.1
- Safety: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. 当用户反馈模型 JSON 输出格式崩溃、字段缺失导致下游 API 或数据库解析失败时，本技能可执行结构化修复。
2. 在项目需要强制 LLM 返回合规结构（如函数调用工具参数）且必须满足特定 Schema 约束时使用。
3. 作为『不可信外部输入』的安全屏障，在执行代码逻辑前校验模型输出是否符合有籍·有证·有门禁原则。

### 用法
核心脚本为 `schema_guard.py`，支持通过 Python 模块导入方式或直接命令调用。调用时需提供两个关键参数：一是待校验的原始文本或 JSON 字符串，二是 Schema 定义对象（含必填字段、数据类型及枚举值列表）。技能将自动在内部加载并缓存于 `__pycache__` 环境中的逻辑，无需用户手动编译即可运行。

### 流程
1. 接收用户输入的 LLM 输出内容及相关 Schema 校验规则。
2. 调用 `schema_guard.py` 脚本进行初始化配置与数据加载。
3. 遍历输入字段，比对必填项与类型约束，检测枚举值合规性。
4. 依据 LGD 三律（有籍·有证·有门禁）逻辑执行验证，若发现错误则不直接报错。
5. 生成包含具体修改位置的修复提示或清洗后的修正数据返回给用户。
6. 记录校验状态以便系统持续优化后续模型输出的可信度与格式稳定性。

### 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「模型返回的 JSON 又崩了」 / "the model keeps returning broken JSON"
- 「字段缺一个下游就报错」 / "one missing field breaks the downstream job"
- 「怎么强制模型按格式输出」 / "how do I force the model into a fixed format"
- 「工具调用参数老是对不上」 / "tool call arguments never match the signature"
- 「解析失败能不能给个修复提示」 / "can the parse error tell me how to fix it"
- 「枚举值不在允许范围里」 / "the enum value is outside the allowed list"

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
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/output-schema-guard
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/output-schema-guard/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
