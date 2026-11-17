---
name: medical-device-qms-gmp
title: "Medical Device QMS/GMP Documents"
display_name: 医械质量体系GMP文档
display_name_en: Medical Device QMS/GMP Documents
description: >-
  Generate and review medical-device GMP / ISO 13485 QMS documents: quality manual, procedure framework, process validation (IQ/OQ/PQ), reprocessing validation (clean-disinfect-sterilize-package for reusable devices), and sterilization qualification. Covers regulatory system-audit preparation.

  生成与核查医疗器械 GMP/ISO 13485 质量体系文档：质量手册、程序文件框架、工艺验证（IQ/OQ/PQ）、复用器械再处理验证、灭菌确认，覆盖体系核查准备。
description_zh: "生成与核查医疗器械 GMP/ISO 13485 质量体系文档：质量手册、程序文件框架、工艺验证（IQ/OQ/PQ）、复用器械再处理验证、灭菌确认，覆盖体系核查准备。"
description_en: "Generate and review medical-device GMP / ISO 13485 QMS documents: quality manual, procedure framework, process validation (IQ/OQ/PQ), reprocessing validation (clean-disinfect-sterilize-package for reusable devices), and sterilization qualification. Covers regulatory system-audit preparation."
version: 0.1.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
author: SynomosAI
category: knowledge-management
tags: [medical-device-qms-gmp, 医疗器械, GMP, ISO 13485, 质量体系, 工艺验证]
license: MIT
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
slug: medical-device-qms-gmp
classification:
  skillhub: ["medical-device", "quality", "regulatory"]
  iso_25010: ["Maintainability"]
read_when:
  - 需要生成/核查 GMP 或 ISO 13485 质量手册与程序文件框架
  - 需要做工艺验证（IQ/OQ/PQ）、复用器械再处理验证、灭菌确认方案
  - 体系核查（飞检/稽核）前准备与缺陷整改台账
ai_protocol: true
spec: usk/1.0
interface:
  type: prompt
  entry_point: SKILL.md
  runtime: none
  call_pattern: prompt
input_schema:
  args:
    type: string
    description: CLI arguments per skill usage
    required: false
output_schema:
  stdout: structured result (JSON IR)
  exit_code: rc=0 ok / rc=1 warning / rc=2 bad input
capabilities:
- medical-devices
- qms
- gmp
- regulatory
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: '3.8'
changelog: '0.1.1: Bilingual rewrite (EN-first) + read_when/classification; legacy author/copyright/platform refs neutralized; 0.1.0 initial upload (USK v3 injected round2)'
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

# Medical Device QMS/GMP Documents

The quality management system is the foundation of registration and production. This skill provides framework generation and review checklists for GMP/ISO 13485 system documents, focusing on process validation, reusable-device reprocessing validation, and sterilization qualification — high-frequency audit points.

## When to use
- Generate/review GMP or ISO 13485 quality manuals, procedure frameworks, process validation (IQ/OQ/PQ), reprocessing validation, or sterilization qualification.
- Triggers: GMP, ISO 13485, process validation, IQ/OQ/PQ, reprocessing, sterilization, system audit.

## How to use
- Writing-assistance skill, no `scripts/`; follow the seven-step process below.
- Rules/official links: see `medical-device-reg-hub`; after generation, self-check with `medical-device-compliance-grader` C5 dimension.

## Workflow (7 steps)
1. Define system scope (design / procurement / production / inspection / after-sales).
2. Build quality manual + procedure framework per ISO 13485:2016.
3. Process validation: IQ/OQ/PQ for key processes.
4. Reprocessing validation (reusable devices): clean→disinfect→sterilize→package, confirm repeatable SAL.
5. Sterilization qualification per ISO 11135 (EO) / 11137 (irradiation) / 17665 (moist heat); sterile barrier per ISO 11607.
6. System-audit self-check → defect rectification ledger.
7. Self-check loop via `medical-device-compliance-grader` C5 dimension.

## Key points
- Process validation is not one-time; key-process changes and equipment moves require re-qualification.
- Reusable-device IFU reprocessing must match the reprocessing validation conclusion.
- Sterilization status must be truthfully reflected on labels/IFU.
- Risk management (ISO 14971) runs through the system.

## Boundary
Not legal/regulatory advice; follow the latest official releases. Inputs/outputs desensitized.

## Evidence & safety
- Evidence: see bundled ATTESTATION.md / manifest.json / security_results.json.
- Version: 0.1.1; Security: local closed-loop, zero credentials, sensitive_hits=[] per bundled snapshot.

## 中文

# 医械质量体系 GMP 文档

质量体系是注册与生产的底座。本技能提供 GMP/ISO 13485 体系文档的框架生成与核查清单，重点覆盖工艺验证、复用器械再处理验证、灭菌确认——体系核查高频必查点。

## 何时用
- 需要生成与核查 GMP / ISO 13485 质量手册、程序文件框架、工艺验证、再处理验证、灭菌确认。
- 触发词：GMP、ISO 13485、工艺验证、IQ/OQ/PQ、再处理验证、灭菌确认、体系核查。

## 用法
- 编写辅助型技能，无 scripts/；按七步流程执行。
- 规则/官方链接走 `medical-device-reg-hub`；生成后用 `medical-device-compliance-grader` C5 维度自测。

## 使用流程（七步）
定体系范围 → 搭质量手册与程序框架（ISO 13485:2016）→ 关键工序 IQ/OQ/PQ → 复用器械清洗-消毒-灭菌-包装再处理验证 → 灭菌确认（ISO 11135/11137/17665，无菌屏障 ISO 11607）→ 体系核查自查与缺陷整改台账 → C5 维度自测闭环。

## 要点速查
工艺验证非一次性（变更/搬迁须再确认）；复用器械 IFU 再处理须与验证结论一致；灭菌状态须如实标注；风险管理（ISO 14971）贯穿体系。

## 注意事项
不构成法规意见，以监管机构最新发布为准；输入/输出去敏。

## 证据与安全声明
- 证据：见包内 ATTESTATION.md / manifest.json / security_results.json。
- 版本：0.1.1；安全：本地闭环、零凭据、sensitive_hits=[]。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-qms-gmp
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-qms-gmp/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
