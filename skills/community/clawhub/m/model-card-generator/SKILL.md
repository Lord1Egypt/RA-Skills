---
name: model-card-generator
description: model-card-generator — 给团队内任何 AI 系统/智能体生成一页『模型卡』：身份/用途/数据/限制/风险/联系人，输出 Markdown+JSON，对齐模型卡惯例与透明度义务。 适用场景：当需要模型卡生成器能力时使用本技能；触发词：model-card-generator。
slug: model-card-generator
title: 模型卡生成器
version: 1.0.1
display_name: 模型卡生成器
display_name_en: Model Card Generator
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description_zh: "model-card-generator — 给团队内任何 AI 系统/智能体生成一页『模型卡』：身份/用途/数据/限制/风险/联系人，输出 Markdown+JSON，对齐模型卡惯例与透明度义务。"
description_en: "Generate one-page model cards for any AI system or agent: identity, purpose, data, limitations, risks and contact, in Markdown plus JSON, aligned with model-card conventions."
read_when:
  - AI 系统/智能体上线前要补一页标准化身份与用途文档
  - 合规审查要求提供透明度报告、数据范围与模型限制
  - 需要 Markdown+JSON 双格式模型元数据归档
  - 事故发生后没有可查的模型归属与风险记录
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [model-card-generator, AI 治理, 模型卡, 透明度, 文档]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/model_card_generator.py
  runtime: python3
  call_pattern: args
input_schema:
  name:
    type: string
    description: "系统/智能体名称"
    required: true
  org:
    type: string
    description: "所属团队"
    required: false
  purpose:
    type: string
    description: "用途（一句话）"
    required: true
  data:
    type: string
    description: "训练/处理数据说明"
    required: false
  limits:
    type: string
    description: "已知限制"
    required: false
  risks:
    type: string
    description: "主要风险与缓解"
    required: false
  contact:
    type: string
    description: "负责人/联系方式"
    required: false
  out:
    type: string
    description: "输出 Markdown 路径"
    required: false
  json:
    type: bool
    description: "json"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - mlops
  - model-card
  - documentation
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
1. Before an AI system or agent goes live, when you need to quickly produce a standardized document stating its identity and intended use.
2. When internal compliance review requires a transparency report, data-usage scope and model-limitations information.
3. When team collaboration requires storing model metadata in both Markdown and JSON formats for archival.

### Usage
1. Run the core script `model_card_generator.py`; it must be executed inside a Python environment where the project directory contains the script.
2. Pass the required input parameters, such as model name, data-source description, and the risk points to highlight.
3. When the skill is consumed as an interface, pass the task configuration and context information via JSON-RPC.

### Workflow
1. Collect the model's training objective, main use cases and key functional identity-definition information.
2. Organize risk elements such as data-privacy scope, known biases and system performance limits.
3. Run the generation script to output a model-card draft that meets transparency obligations.
4. Check that the generated Markdown and JSON include contact information and the disclaimer section.
5. Save the final document to the project repository or deployment-package directory for team review.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once produced)
- Version: 1.0.1
- Safety: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. 在 AI 系统或智能体上线前，需要快速生成包含身份与用途说明的标准化文档时。
2. 内部合规审查要求提供透明度报告、数据使用范围及模型限制信息时。
3. 团队协作中需以 Markdown 和 JSON 双格式存储模型元数据并归档时。

### 用法
1. 执行命令调用核心脚本 `model_card_generator.py`，需处于 Python 环境且项目目录下存在该文件。
2. 传入必要的输入参数，如模型名称、数据源描述及需要强调的风险点。
3. 若技能作为接口使用，则通过 JSON-RPC 方式传递任务配置与上下文信息。

### 流程
1. 收集模型的训练目标、主要用途及关键功能身份定义信息。
2. 整理数据隐私范围、已知偏差及系统性能限制等风险要素。
3. 运行生成脚本，输出符合透明度义务要求的模型卡草稿。
4. 检查生成的 Markdown 与 JSON 内容是否包含联系人信息与声明章节。
5. 将最终文档保存至项目存储库或部署包目录中供团队查阅使用。

### 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
