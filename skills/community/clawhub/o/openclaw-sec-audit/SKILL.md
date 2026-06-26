# OpenClaw Security Audit

Source repository: https://github.com/haooyi/openclaw-sec

Maintainer: haooyi

## Purpose

Run a local security audit against the current OpenClaw installation and runtime environment, then return high-signal risks, impacted locations, and prioritized remediation steps.

## When To Trigger

- The user asks whether the current OpenClaw environment is secure
- The user suspects API key leaks, log leaks, overly broad permissions, or public exposure
- The user wants a locally executable security report

## How To Execute

Use local shell execution to run `resources/run_audit.sh`. The wrapper invokes the bundled standalone Python source shipped with the skill and does not depend on the repository checkout or the main project install.

## Output Requirements

- Never print raw secrets
- Keep config-derived evidence redacted or summarized instead of echoing raw values
- Summarize risks, impacted files, priority, and remediation only
- Order remediation steps as `critical -> high -> medium -> low`
- If a host check is unsupported or permission-limited, say `skipped` or `unsupported` explicitly

## Suggested Invocation

```bash
./skills/openclaw-sec-audit/resources/run_audit.sh --format all
```

## Runtime Assumption

The host must provide `python3`. No editable install of the main project is required for the skill path.
