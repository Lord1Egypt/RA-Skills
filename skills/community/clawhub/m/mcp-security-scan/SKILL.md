---
name: mcp-security-scan
display_name: MCP 安全扫描（MCP Security Scan）
display_name_en: "MCP Security Scan"
description: "当用户说『接了个MCP server不放心』『MCP工具能执行命令怕有风险』『怎么审计MCP权限』『第三方MCP会不会偷数据』，或要把某 MCP server(模型上下文协议)接进 agent、担心它是新攻击面时使用。把 MCP server 当『需审查的第三方』：扫工具清单里的 命令执行/文件系统写/网络外联/凭证暴露 四类风险，给风险评级与最小授权建议。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：MCP安全、mcp security、MCP审计、MCP权限、第三方MCP、MCP风险、server扫描、协议安全。"
version: 1.1.1
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, WebFetch
category: AI安全
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
read_when:
  - 要把第三方 MCP server 接进 agent
  - 担心 MCP 工具能执行命令/读写文件/外联
  - 问「怎么审计 MCP 权限」
  - 怕 MCP 偷数据或越权
tags: [MCP安全, mcp security, MCP审计, 协议安全, 第三方审查, 最小授权, AI安全, 攻击面]
slug: mcp-security-scan
title: MCP 安全扫描（MCP Security Scan）
copyright: SynomosAI
description_zh: "当用户说『接了个MCP server不放心』『MCP工具能执行命令怕有风险』『怎么审计MCP权限』『第三方MCP会不会偷数据』，或要把某 MCP server(模型上下文协议)接进 agent、担心它是新攻击面时使用。把 MCP server 当『需审查的第三方』：扫工具清单里的 命令执行/文件系统写/网络外联/凭证暴露 四类风险，给风险评级与最小授权建议。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：MCP安全、mcp security、MCP审计、MCP权限、第三方MCP、MCP风险、server扫描、协议安全。"
description_en: "Security-scan MCP servers before onboarding: tool-permission audit, command-execution risk, data-exfiltration surface and prompt-injection exposure analysis."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
ai_protocol: true


spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/mcp_scan.py
  runtime: python3
  call_pattern: args
input_schema:
  tools:
    type: string
    description: "tools"
    required: true
  json:
    type: bool
    description: "json"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - mcp
  - security
  - scanning
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.1.1: Bilingual rewrite (full EN+ZH, English first); read_when kept; 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
- When the user plans to connect a third-party MCP server to the current agent and needs to assess whether it introduces a new attack surface.
- When the user is concerned about MCP tools executing commands, file-write access or network egress.
- Whenever auditing MCP permissions and confirming LGD three-laws (registered · evidenced · gated) compliance — this skill must be used for pre-onboarding review.

### Usage
Call the main script `mcp_scan.py` with the target MCP server's config or metadata as input. Specify `target_server_name`, `access_config` and risk concerns (e.g. `command_exec`, `fs_write`). The skill reads its built-in security rules, runs the simulated detection and returns a standardized JSON report with detailed risk categories and the LGD compliance verdict.

### Workflow
First, receive the MCP server's identity and config description, confirming it is a "third party under review". Then run `mcp_scan.py` to score the four risk classes: command execution, filesystem write, network egress and credential exposure. Cross-validate against the LGD three-laws model that the permission boundary is closed and traceable. Finally, generate the report with risk rating (high/medium/low) and least-privilege recommendations, for the decision-maker to admit or circuit-break.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.1.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
当用户计划将第三方 MCP server 接入当前 Agent，需评估其是否构成新的安全攻击面时。
当检测到用户对 MCP 工具执行命令、文件写权限或网络外联存在风险疑虑时。
在涉及如何审计 MCP 权限及确认 LGD 三律（有籍·有证·有门禁）合规性时，必须使用此技能进行前置审查。

### 用法
调用主脚本 `mcp_scan.py` 并注入目标 MCP server 的配置信息或元数据作为输入参数。需指定 `target_server_name`、`access_config` 以及风险关注点（如 `command_exec`, `fs_write`）。技能将读取脚本内的安全规则，执行模拟检测逻辑，并返回标准化的 JSON 格式报告，包含详细的风险分类与 LGD 合规判定结果。

### 流程
首先接收 MCP server 的身份信息与配置描述，确认其作为“需审查的第三方”属性；其次运行 `mcp_scan.py` 对命令执行、文件系统写、网络外联及凭证暴露四大类风险进行扫描与打分；接着依据 LGD 三律模型交叉验证权限边界是否封闭且可追溯；最后生成包含风险评级（高/中/低）与最小授权建议的最终报告，供决策者执行准入或熔断。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
