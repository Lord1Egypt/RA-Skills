---
name: gmp2025-transition
title: "GMP 2025 Transition Assistant"
description: 中国《医疗器械生产质量管理规范》2025 版（国家药监局 2025 年第 107 号公告，2026-11-01 施行）过渡时间线、倒计时与企业自查行动清单。
description_zh: "中国医疗器械 GMP 2025 版（107号公告，2026-11-01 施行）过渡倒计时、阶段判定与 12 项企业自查行动清单。"
description_en: "Transition assistant for China's medical-device GMP 2025 (NMPA Announcement No.107 of 2025, effective 2026-11-01): countdown, phase judgment, and a 12-item self-inspection action checklist."
license: MIT
metadata:
  author: SynomosAI
  category: other
  tags: [medical-device, GMP, china, QMS, regulatory]
permalink: skills/gmp2025-transition/skill
tags: [gmp2025-transition, medical-device, GMP, QMS]
version: 1.0.1
category: 医疗器械合规
classification:
  skillhub: ["medical-device", "regulatory", "productivity"]
  iso_25010: ["Maintainability"]
read_when:
  - 需要算 GMP 2025 版（107号公告）距 2026-11-01 施行的倒计时与阶段
  - 体系升级排期、内审/管理评审前的企业自查行动清单
  - 注册项目衔接、日常倒计时看板提醒
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/gmp_transition.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "subcommands passed through; see scripts/gmp_transition.py --help"
    required: false
output_schema:
  stdout: phase/timeline/checklist text; structured JSON with --json
  exit_code: 0 ok / non-zero usage or runtime error
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (EN-first) + read_when/classification; 1.0.0 initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

# GMP 2025 Transition Assistant

Given a reference date, compute days remaining to the 2026-11-01 effective date, the current phase, and recommended actions for China's medical-device GMP 2025.

## Verified fact baseline

| Item | Content |
|---|---|
| Announcement | NMPA **Announcement No.107 of 2025** |
| Effective | **2026-11-01** |
| Replaces | 2014 version (Announcement No.64 of 2014) after effective date |
| Structure | **15 chapters, 132 articles**; adds chapters on quality assurance, validation & verification, and contract manufacturing/outsource processing |
| Data frozen | 2026-09-21 (multi-source cross-check) |

## Usage
```bash
python scripts/gmp_transition.py status                     # current phase & countdown
python scripts/gmp_transition.py timeline                   # national + provincial timeline
python scripts/gmp_transition.py checklist                  # 12-item self-inspection
python scripts/gmp_transition.py sources                    # data sources
python scripts/gmp_transition.py status --json
```

| Days to effective | Phase | Advice |
|---|---|---|
| > 180 | Preparation | gap analysis, training, document revision schedule |
| 91–180 | Self-inspection rectification | close gaps, schedule internal audits & training records |
| ≤ 90 | Sprint | system version upgrade, internal audit, management review, timely filing |
| < 0 | In effect | run under new rules, follow up on nonconformities |

## Boundary
Outputs timing and action prompts only; does NOT judge compliance or replace official interpretation. Provincial deadlines are examples; follow local NMPA notices. Medical-device compliance must be reviewed by qualified personnel.

## Requirements
Python 3.8+, zero third-party deps.

## Evidence & safety
- Evidence: TBD; Version: 1.0.1; Security: no independent scan (TBD).

## 中文

# gmp2025-transition

中国《医疗器械生产质量管理规范》**2025 版过渡助手**。给定基准日期，算出距施行还有多少天、处于哪个阶段、该做什么。

## 已核验的事实基线

| 项 | 内容 |
|---|---|
| 公告 | 国家药监局 **2025 年第 107 号公告** |
| 施行日 | **2026-11-01** |
| 替代关系 | 施行后替代 2014 年版 |
| 新版结构 | 共 **15 章 132 条**；新增质量保证、验证与确认、委托生产与外协加工三章 |
| 数据核定 | 2026-09-21 |

## 使用方法
```bash
python scripts/gmp_transition.py status        # 当前阶段与倒计时
python scripts/gmp_transition.py timeline      # 过渡时间线
python scripts/gmp_transition.py checklist     # 12 项自查行动清单
python scripts/gmp_transition.py sources       # 数据来源
```

阶段划分：>180 天准备期 / 91–180 天自查整改期 / ≤90 天冲刺期 / <0 已施行。

## 边界声明
只输出时间与行动提示，不判定是否符合《规范》，不替代官方解读；省级时限为示例，以属地药监局为准；合规判断须由具备资质人员复核。

## 环境要求
Python 3.8+，零第三方依赖。

## 证据与安全声明
- 证据：TBD；版本：1.0.1；安全：未做独立扫描（TBD）。
