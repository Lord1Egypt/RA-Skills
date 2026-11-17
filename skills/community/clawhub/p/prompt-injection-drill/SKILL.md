---
name: prompt-injection-drill
title: "Prompt Injection Drill"
slug: prompt-injection-drill
display_name: 提示词注入演练器
display_name_en: Prompt Injection Drill
version: 1.0.1
agent_created: true
author: SynomosAI
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: ai-governance
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description: 提示词注入演练器 — 为 system prompt 生成 8 类注入攻击演练用例（角色覆盖/指令覆盖/诱导泄密/编码绕过/工具滥用/越权伪造/长程拖延/拒绝绕过）+ 期望行为清单，供上线前红队自测。
description_zh: "为 system prompt 生成 8 类注入攻击演练用例（角色覆盖/指令覆盖/诱导泄密/编码绕过/工具滥用/越权伪造等）+期望行为清单，供上线前红队自测。"
description_en: "Generate eight categories of injection-attack drill cases for your system prompt (role and instruction override, secret elicitation, encoding bypass, tool abuse, privilege forgery, long-horizon delay, refusal bypass) plus expected behaviors, for pre-launch red-team self-testing."
classification:
  skillhub: ["security-compliance", "ai-governance", "prompt-security"]
  clawhub: ["development", "security"]
  iso_25010: ["Security"]
read_when:
  - 模型/智能体上线部署前做安全基线检查与 Prompt 防御能力验证
  - 红队渗透测试需模拟角色覆盖/指令篡改等高危场景挖漏洞
  - 处理敏感数据或高权限业务的应用需全面注入风险排查与加固
risk_tier: medium
risk_rationale: "调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [prompt-injection-drill, AI 治理, 安全, 红队, security-compliance]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/prompt_injection_drill.py
  runtime: python3
  call_pattern: args
output_schema:
  stdout: structured drill cases + expected behaviors
  exit_code: rc=0 ok / rc=1 warning / rc=2 bad input
changelog: "1.0.1: Bilingual rewrite (EN-first) + read_when/classification; risk_rationale ref neutralized; 1.0.0 initial"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

# Prompt Injection Drill

## When to use
1. Before a model/agent goes live, for security baseline checks and prompt-defense validation.
2. In red-team penetration testing, to actively simulate role override and instruction tampering.
3. For apps handling sensitive data or high-privilege actions, to run full injection-risk triage and hardening.

## How to use
- Main script: `python scripts/prompt_injection_drill.py`.
- Pass the target system context; use `--mode` to select attack categories (e.g. encoding bypass).
- Ensure the Python environment can load the script and its modules.

## Workflow
1. Pass the system prompt under test as the analysis target.
2. Configure drill parameters for the 8 injection categories to cover.
3. Run the script to generate attack cases and expected behaviors.
4. Compare the generated cases against the system's actual responses.
5. Identify defense failures or logic flaws; record abnormal trigger paths.
6. Summarize into a red-team self-test report for the go-live decision.

## Evidence & safety
- Evidence: TBD; Version: 1.0.1; Security: no independent scan (TBD).

## 中文

# 提示词注入演练器

## 何时用
1. 模型/智能体正式上线前做安全基线检查与 Prompt 防御能力验证。
2. 红队渗透测试时主动模拟角色覆盖、指令篡改等高危场景挖掘漏洞。
3. 处理敏感数据或高权限业务的应用做全面注入风险排查与加固评估。

## 用法
- 主脚本：`python scripts/prompt_injection_drill.py`。
- 传入待测系统上下文；用 `--mode` 指定攻击类别（如编码绕过）。
- 确保 Python 环境能加载脚本与模块。

## 流程
传入待测 System Prompt → 配置 8 类注入覆盖方向 → 运行脚本生成攻击用例与期望行为清单 → 对照验证实际响应 → 识别防御失效并记录异常路径 → 汇总红队自测报告作为上线依据。

## 证据与安全声明
- 证据：TBD；版本：1.0.1；安全：未做独立安全扫描（TBD）。
