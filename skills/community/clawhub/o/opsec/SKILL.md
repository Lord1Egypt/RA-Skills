---
name: clawguard
slug: opsec
version: 1.0.0
homepage: https://clawhub.com/skills/opsec
description: "Security review and risk auditing for OpenClaw skills and deployments. Inspect third-party skills, dangerous instructions, credential requests, privilege risks, and generate clear remediation reports before incidents happen."
---

# clawguard

clawguard 是一个面向 OpenClaw 的本地优先安全审查技能。  
clawguard is a local-first security review skill for OpenClaw.

它帮助你在安装第三方技能之前先发现风险。  
It helps you discover risks before installing third-party skills.

它会审查 SKILL.md、脚本说明和可疑安装指令。  
It reviews SKILL.md files, script instructions, and suspicious installation steps.

它关注高危命令、远程下载、密码请求、越权访问和高风险承诺。  
It focuses on risky commands, remote downloads, credential requests, privileged access, and high-risk claims.

它输出带证据的专业报告，而不是只有模糊警告。  
It produces professional evidence-based reports instead of vague warnings.

它默认支持人类可读输出，也支持 JSON 输出供其他工作流使用。  
It supports human-readable output by default and also JSON output for other workflows.

## 适用场景  
## Use when

当你准备安装一个第三方 skill 时。  
When you are about to install a third-party skill.

当你想在信任一个 skill 之前先做审查时。  
When you want to review a skill before trusting it.

当你需要风险等级、证据和修复建议时。  
When you need severity, evidence, and remediation guidance.

当你想让安全审查结果可供其他 agent 继续处理时。  
When you want your security findings to be reusable by other agents.

## v1 检查重点  
## What v1 checks

高危 shell 或命令执行模式。  
Risky shell or command execution patterns.

远程下载、外联脚本和不透明安装方式。  
Remote downloads, external fetches, and opaque installation behavior.

密码、Token、API Key 等敏感凭证请求。  
Requests for passwords, tokens, API keys, and other sensitive credentials.

管理员权限、敏感路径访问与系统级修改倾向。  
Administrator privileges, sensitive path access, and system-level modification tendencies.

“自动修复”“绕过限制”“无需审查直接执行”等高风险表述。  
High-risk claims such as “auto-fix,” “bypass restrictions,” or “execute without review.”

## 输出形式  
## Output

人类可读安全报告。  
Human-readable security report.

结构化 JSON 结果。  
Structured JSON results.

风险等级、命中位置、证据片段、影响说明和修复建议。  
Severity, matched location, evidence snippet, impact explanation, and remediation guidance.

## 安全立场  
## Safety posture

clawguard 是审查工具，不是全自动修复工具。  
clawguard is a reviewer, not a fully automatic remediation tool.

它不承诺完全保护系统。  
It does not promise to fully secure a system.

它的目标是在执行前帮助你发现风险并做出更稳妥的判断。  
Its goal is to help you identify risks and make safer decisions before execution.
