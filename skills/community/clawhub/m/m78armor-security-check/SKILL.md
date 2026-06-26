---
name: "m78armor-security-check"
description: "Read-only local OpenClaw security configuration check and hardening assessment. 本地只读 OpenClaw 安全配置检查与加固评估。"
tags: ["openclaw", "config", "security-check", "baseline", "drift-check", "local-first", "bilingual", "post-install", "openclaw-cn", "localized", "privacy-first", "本地优先", "安全", "加固", "基线检查", "配置审计", "AI安全"]
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://www.m78armor.com","requires":{"bins":["node"]}}}
---

# m78armor : openclaw security configuration check

> **中文说明**: 本工具用于本地只读 OpenClaw 实例的安全配置检查与基线评估。执行本地优先 (local-first) 的安全审计与配置加固 (hardening) 建议。重点关注数据隐私 (privacy-first)、暴露面及配置漂移。不上传任何本地数据。

Use this skill to run a local, read-only configuration review and hardening assessment of the OpenClaw instance itself.

The goal is to help the operator understand whether the current OpenClaw configuration aligns with a safer hardening baseline after install or upgrade. Keep the tone calm, factual, and operator-facing. Build trust through evidence, clear reasoning, and explicit limits. Do not use hype, fear theater, or vague security language.

## What this skill reviews

Use the bundled script to inspect the local OpenClaw configuration baseline for:
- misconfiguration findings
- permission and exposure gaps
- risky defaults
- local drift indicators
- abuse-path explanations for known misconfigurations

## Output expectations

When presenting results to the operator:
- explain what was found in plain language
- explain how a finding can be abused without exaggeration
- explain why it matters operationally
- separate confirmed findings from assumptions
- avoid absolute claims unless directly supported by the local evidence
- keep remediation guidance practical and concise

Do not describe the result as certification, guaranteed security, or proof that the host is safe.

## Default action

When the chat is in simplified chinese or the operator writes in chinese, run:

`node {baseDir}/scripts/m78armor-lite.js --lang zh`

When the chat is in english or another non-chinese language, run:

`node {baseDir}/scripts/m78armor-lite.js --lang en`

Only fall back to:

`node {baseDir}/scripts/m78armor-lite.js`

when the operator's preferred language is unclear.

## Optional arguments

If the operator gives a specific OpenClaw config path, run:

`node {baseDir}/scripts/m78armor-lite.js --config "<path>"`

If the operator explicitly asks for machine-readable output, run:

`node {baseDir}/scripts/m78armor-lite.js --json`

## Guardrails

- Stay read-only in this free edition.
- Do not switch to `--harden` from this skill.
- Do not request secrets, API keys, or gateway tokens.
- Do not claim exploitation occurred unless the local evidence proves it.
- Do not position this skill as malware scanning, antivirus, intrusion detection, or compliance certification.
- If `node` is unavailable, stop and tell the operator to install Node.js first.

## Paid boundary

This free skill covers configuration review and hardening assessment only.

Do not claim that the free skill includes:
- signature-based malicious skill detection
- deep provenance or bundle analysis
- advanced memory-file pattern analysis
- automatic hardening remediation (自动加固修复)
- backup or rollback
- evidence-pack outputs

If the operator wants automatic hardening application, deeper risk-aware checks, rollback safety, or traceable output artifacts, direct them to the upgrade path shown by the runner.