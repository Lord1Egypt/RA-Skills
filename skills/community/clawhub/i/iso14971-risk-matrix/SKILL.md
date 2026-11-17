---
name: iso14971-risk-matrix
description: ISO 14971 risk-management helper for medical devices. Score a risk with a reference 5x5 severity x probability matrix (with an optional residual-risk comparison), print the risk-control option hierarchy of ISO 14971:2019 7.1, and check whether a risk-management file covers the elements ISO 14971:2019 requires (4.4 plan, 4.5 file, 5 analysis, 6 evaluation, 7 control incl. 7.3/7.4, 8 overall residual risk, 9 review, 10 post-production).
slug: iso14971-risk-matrix
title: iso14971-risk-matrix
version: 1.0.1
license: MIT
author: SynomosAI
tags:
- medical-device
- risk-management
- iso14971
- quality
- regulatory
category: 医疗器械合规
description_zh: "ISO 14971 医疗器械风险管理助手：5×5 严重度×概率风险矩阵（含残余风险对比）、ISO 14971:2019 7.1 风险控制选项层级、风险管理文件 16 要素完整性核查。"
description_en: "ISO 14971 medical-device risk helper: reference 5x5 severity×probability matrix with residual-risk comparison, ISO 14971:2019 7.1 control-option hierarchy, and a 16-element RM-file completeness check."
read_when:
  - 严重度×概率要转成一致风险等级（用标准自身的词汇）
  - 建/审风险管理文件前做 ISO 14971:2019 条款完整性核查
  - 团队培训或核查风险控制选项层级使用是否正确
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/risk_matrix.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "子命令与参数透传给主脚本，具体取值见 scripts/risk_matrix.py --help"
    required: false
output_schema:
  stdout:
    type: string
    description: "标准输出为风险矩阵/风险评分/控制选项层级文本"
  exit_code:
    type: integer
    description: "0=ok；1=阻断发现；2=用法错误"
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
- Turn a severity/probability pair into a risk level consistently, in the vocabulary the standard itself uses.
- Build or audit a risk management file; do a clause-by-clause completeness pass against ISO 14971:2019 before a QMS audit or submission.
- Train or check a team's use of the risk-control option hierarchy — the most common audit finding is a file that jumps straight to "add a warning label".
- Falsification check: does the file show any evidence that controls actually reduced anything?

### Usage
```bash
python scripts/risk_matrix.py matrix            # reference 5x5
python scripts/risk_matrix.py assess -s 4 -p 2
python scripts/risk_matrix.py assess -s 5 -p 5 --rs 2 --rp 1
python scripts/risk_matrix.py options         # ISO 14971:2019 7.1 hierarchy
python scripts/risk_matrix.py check rm_file.md # 16-element completeness
```
Exit `0` = ok, `1` = blocking finding, `2` = usage error.

### Reference matrix
Severity 1–5 × probability 1–5; score = S × P. 1–4 low (record & monitor), 5–9 ALARP (reduce to as low as reasonably practicable), 10–25 high (redesign / protective measures; residual-still-unacceptable → benefit-risk analysis 7.4).

> ⚠️ Convention, not the standard. ISO 14971:2019 §4.4 requires the manufacturer to define the acceptable-risk policy in its RM plan. The plan wins.

### `assess` also prints
The clause-3 vocabulary chain (hazard → events → hazardous situation → harm) as a completeness prompt; with `--rs/--rp`, flags suspicious patterns (residual still H, residual worse than initial, residual identical to initial).

### `check` looks for
16 elements across clauses 4–10 (EN+ZH keywords). Critical vs optional separated. Keyword hits mean "mentioned", not "done".

### Known limits
- ISO 14971 mandates no specific matrix; 5×5 is one common convention. The RM plan's bands win.
- Probability anchors are indicative only, not from the standard.
- `check` is keyword-based, EN+ZH only; other languages / unusual headings → false "missing".
- Does not write the file, does not decide acceptability, not a regulatory opinion.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
- 需要把 严重度 × 概率 转成一致风险等级；建 / 审风险管理文件做 ISO 14971:2019 条款完整性核查。
- 触发词：ISO 14971、风险矩阵、风险控制选项层级、风险管理文件自查。

### 用法
```bash
python scripts/risk_matrix.py matrix            # 参考 5×5 矩阵
python scripts/risk_matrix.py assess -s 4 -p 2   # 评一个风险
python scripts/risk_matrix.py assess -s 5 -p 5 --rs 2 --rp 1  # 初始+残余对比
python scripts/risk_matrix.py options            # ISO 14971:2019 7.1 层级
python scripts/risk_matrix.py check rm_file.md   # 16 要素核查
```
退出码 0 = ok / 1 = 阻断发现 / 2 = 用法错误。

### 参考矩阵
严重度 1–5（可忽略/轻度/严重/危重/灾难性）× 概率 1–5（极不可能/罕见/偶然/很可能/频繁）；分值 = S × P。1–4 低（记录并监测），5–9 ALARP（降至合理可行最低），10–25 高（重新设计/防护措施；残余仍不可接受 → 7.4 获益-风险分析）。

> ⚠️ 本矩阵是惯例而非标准。ISO 14971:2019 §4.4 要求制造商在风险管理计划中自行定义可接受风险政策，**计划优先**。

### assess 额外输出
打印条款 3 词汇链（危害→事件序列→危险处境→伤害）作为完整性提示；带 `--rs/--rp` 时标记可疑模式（残余仍 H、残余比初始更差、残余与初始完全相同）。

### check 核查项
覆盖 ISO 14971:2019 第 4–10 条款 16 要素（中英文关键词），关键项与可选项分列。关键词命中只表示"文档提及"，不代表"已落实"。

### 已知局限
- ISO 14971 未规定具体矩阵；本 5×5 为常见惯例，以风险管理计划的分级带为准。
- 概率锚点（每设备生命周期 1e-6…1e-2）仅为示意，非源自标准。
- `check` 基于关键词、仅中英文；其他语言或非常规标题会产生假"缺失"。
- 不代写风险文件、不替你判定可接受性、不构成法规意见。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
