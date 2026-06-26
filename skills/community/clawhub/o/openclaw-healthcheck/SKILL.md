---
name: openclaw-healthcheck
description: This skill should be used when the user asks for an OpenClaw health check, OpenClaw security audit, server hardening review, exposure review, gateway safety check, or production-readiness audit for a machine running OpenClaw.
---

# OpenClaw Healthcheck

Run a lightweight operational and security review for an OpenClaw deployment.

## What this skill checks
- gateway reachability and process status
- exposed listeners / suspicious open ports
- risky config patterns in the running OpenClaw config
- browser session / relay surface hints
- recent log errors worth operator attention
- update / runtime hygiene signals

## When to use
Use this skill when a user asks:
- "run an OpenClaw health check"
- "audit my OpenClaw security"
- "is this OpenClaw deployment safe"
- "check my OpenClaw server exposure"
- "review my OpenClaw setup before production"
- "why does my OpenClaw runtime feel unhealthy"

## Workflow
1. Confirm target machine / workspace.
2. Run the bundled healthcheck script.
3. Review score, findings, and recommendations.
4. If findings are high-risk, stop and fix before wider rollout.

## Command
```bash
node {baseDir}/scripts/healthcheck.mjs
```

## Output format
The script returns JSON with:
- score
- verdict
- findings
- recommendations
- evidence

## Verdicts
- `PASS` — no major operational or security issue detected in this lightweight pass
- `WARN` — usable but risky or incomplete
- `FAIL` — high-risk exposure or broken runtime detected

## Important limits
- This is a lightweight operator check, not a full penetration test.
- A `PASS` result does not guarantee safety.
- Human review is still required for internet-exposed systems.

## References
- `{baseDir}/references/checklist.md`
