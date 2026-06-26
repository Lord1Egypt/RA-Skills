---
name: openclaw-tool-audit
description: Audit OpenClaw agent tool exposure versus observed use. Use when reviewing allowed tools, spotting broad or unused tool allowances, or checking whether agent tool configs are tighter than necessary. Uses an already-installed trusted local CLI and can emit markdown or JSON summaries. Repository: https://github.com/pfrederiksen/openclaw-tool-audit
---

# OpenClaw Tool Audit

Use this skill to audit local OpenClaw agent tool configuration against observed tool usage.

## Repository

Primary source repo:
- https://github.com/pfrederiksen/openclaw-tool-audit

## Prerequisites

Required:
- a trusted local installation of `openclaw-tool-audit`
- access to the local OpenClaw config and session data the tool reads

Before running:
- verify the local binary or source install is one you trust
- inspect local source if you did not build or install it yourself
- avoid elevated/root execution unless you actually need it
- confirm local session/config files do not expose secrets you are unwilling to inspect

## When to use

Use this when the user asks to:
- audit which tools agents are allowed to use
- compare allowed tools vs tools actually used
- spot overly broad tool access
- review whether agent tool configs could be tightened
- generate a markdown or JSON tool exposure report

## Safe source guidance

Prefer one of these:
- a previously installed trusted local binary on `PATH`
- a trusted local source checkout you have already inspected
- a pinned internal/local install workflow you control

Do not instruct users to install directly from a remote GitHub URL inside this skill.

## Recommended commands

Default markdown summary:

```bash
openclaw-tool-audit --markdown --top-tools 15
```

JSON output:

```bash
openclaw-tool-audit --json
```

Broadest-first review:

```bash
openclaw-tool-audit --markdown --broadest-first
```

Unused-only review:

```bash
openclaw-tool-audit --markdown --unused-only
```

If the binary is not on `PATH`, use the trusted local path you already manage.

## Parser / transcript notes

Real-world OpenClaw installs may have nested tool config shapes and transcript variants that require recent upstream fixes. If the tool crashes or reports zero observed invocations unexpectedly:

- verify you are using a trusted current local build
- validate with `--json`
- check whether observed agent names and tool tokens look sane before making policy decisions

## Recommended interpretation

Use the report to answer:
- which agents have very broad allowlists
- which tools are actually used most often
- which agents have a high unused-allowance ratio
- whether any observed tool tokens look like parser mistakes or unmatched config/runtime shapes

## Packaging / safety

Keep this skill minimal and transparent:
- plain text only
- no binaries
- no obfuscation
- no remote install commands in SKILL.md
- prefer already-installed local/auditable tooling
