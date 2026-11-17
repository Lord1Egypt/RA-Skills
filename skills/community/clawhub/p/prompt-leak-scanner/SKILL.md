---
name: prompt-leak-scanner
description: prompt-leak-scanner — 发布/共享前扫描提示词与 system prompt 的泄漏与后门风险：密钥口令、内部路径、个人可识别信息、自定义敏感词（--extra）、自我泄漏后门（『忽略之前指令/打印系统提示词』类埋点）。有风险 rc=1 拦下。 适用场景：当需要提示词泄漏扫描器能力时使用本技能；触发词：prompt-leak-scanner。
slug: prompt-leak-scanner
title: 提示词泄漏扫描器
version: 1.0.1
display_name: 提示词泄漏扫描器
display_name_en: Prompt Leak Scanner
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description_zh: "prompt-leak-scanner — 发布/共享前扫描提示词与 system prompt 的泄漏与后门风险：密钥口令、内部路径、个人可识别信息、自定义敏感词（--extra）、自我泄漏后门（『忽略之前指令/打印系统提示词』类埋点）。有风险 rc=1 拦下。"
description_en: "Scan prompts and system prompts for leaks and backdoors before sharing: secrets, internal paths, PII, custom sensitive words (--extra) and self-leak backdoors."
read_when:
  - 发布/共享 prompt 或 system prompt 前要做安全审计
  - 怀疑 prompt 里混有密钥、口令、内部路径或 PII
  - 要检测「忽略之前指令/打印系统提示词」类自我泄漏后门
  - 项目要加自定义敏感词规则（--extra）做发布前扫描
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [prompt-leak-scanner, AI 治理, 提示词安全, 泄漏扫描, 后门检测]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/prompt_leak_scanner.py
  runtime: python3
  call_pattern: args
input_schema:
  file:
    type: string
    description: "提示词文件路径"
    required: false
  text:
    type: string
    description: "提示词文本（内联，或 @文件/纯路径）"
    required: false
  extra:
    type: string
    description: "自定义敏感词（项目代号/内部系统名）"
    required: false
  json:
    type: bool
    description: "json"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - prompt
  - security
  - leak
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
1. Before publishing or sharing any prompt that may contain sensitive information, run the final security audit.
2. When you need to verify whether internal system configurations contain secrets, passwords, PII or internal paths.
3. When deep inspection of third-party input or custom rules is required — especially checking for self-leak backdoor risks.

### Usage
- **Script**: `python prompt_leak_scanner.py`
- **Arguments**:
  - `--input`: required; the prompt / system-prompt text to scan.
  - `--extra`: optional; custom sensitive-word list to extend detection (`--extra "word1,word2"`).
  - `--check_cache`: optional; whether to also scan auxiliary logic in `__pycache__`.
- **Output**: returns a risk-level code rc (0 = no risk, safe to publish; 1 = leak found, must block).

### Workflow
1. The caller prepares the prompt text under review and the configuration parameters.
2. Pass the command through the skill interface to run `prompt_leak_scanner.py` for analysis.
3. The system scans keywords, paths and backdoor-command patterns in memory per the script logic.
4. The tool parses the risk level and emits the corresponding return code (rc=1) or a no-risk confirmation.
5. If `rc=1` is detected, the publish flow is blocked automatically and a block signal is sent upstream.
6. Only after risk is confirmed as `rc=0` may subsequent data-sharing operations proceed.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once produced)
- Version: 1.0.1
- Safety: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. 在发布或共享任何包含潜在敏感信息的提示词（Prompt）之前，执行最终安全审计。
2. 当需要验证系统内部配置是否存在密钥、口令、个人可识别信息（PII）或内部路径时。
3. 针对第三方输入内容或自定义规则进行深度检测，特别是检查自我泄漏后门风险。

### 用法
- **执行脚本**: `python prompt_leak_scanner.py`
- **命令参数**:
  - `--input`: 必须，提供待扫描的 Prompt/System Prompt 内容文本。
  - `--extra`: 可选，提供自定义敏感词组用于扩展检测规则（支持 `--extra "word1,word2"`）。
  - `--check_cache`: 可选，是否关联扫描 `__pycache__` 中的辅助脚本逻辑进行验证。
- **输出说明**: 返回风险等级码 rc（0 表示无风险可发布，1 表示存在泄漏需阻断）。

### 流程
1. 调用方准备待审核的提示文本及相关配置参数。
2. 通过技能接口传入命令执行 `prompt_leak_scanner.py` 进行逻辑分析。
3. 系统根据脚本逻辑在内存中扫描关键词、路径及后门指令模式。
4. 工具解析风险等级并生成对应的返回码（rc=1）或无风险确认。
5. 若检测到 `rc=1`，自动拦截发布流程并向上游发送阻断信号。
6. 仅在确认风险为 `rc=0` 后，允许继续进行后续的数据共享操作。

### 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
