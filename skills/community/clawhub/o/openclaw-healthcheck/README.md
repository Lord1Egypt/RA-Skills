# OpenClaw Healthcheck

**A lightweight operator audit for OpenClaw runtime health, security posture, and production-readiness.**

`openclaw-healthcheck` is a small diagnostic skill for checking whether an OpenClaw deployment looks healthy enough to trust before wider rollout.

It is designed for questions like:
- "Run an OpenClaw health check"
- "Audit my OpenClaw security posture"
- "Check my gateway exposure"
- "Review this machine before I put OpenClaw into production"
- "Why does this OpenClaw setup feel unhealthy?"

---

## What it checks

This skill runs a lightweight review across a few high-value areas:

- **Runtime health**
  - whether `openclaw status` succeeds
- **Gateway visibility**
  - whether the expected listener appears present
- **Network exposure hints**
  - listening ports associated with OpenClaw / browser workflows
- **Config hygiene**
  - risky patterns in `~/.openclaw/openclaw.json`
- **Browser attach surface**
  - signs of Chrome remote debugging / relay capabilities
- **Recent log signals**
  - common error patterns worth operator attention

This is intentionally a **fast operator check**, not a deep forensic audit.

---

## What it does not do

This skill does **not** replace:
- a full host hardening review
- a penetration test
- firewall design
- secret rotation policy
- backup / recovery validation
- detailed compliance or threat modeling work

A `PASS` result means **"nothing obviously bad was found in this lightweight pass"**, not **"the system is secure."**

---

## Install / Run

From the skill directory:

```bash
cd ~/.openclaw/workspace/skills/openclaw-healthcheck
node scripts/healthcheck.mjs
```

If you expose the package bin locally:

```bash
openclaw-healthcheck
```

---

## Output

The script returns JSON with these top-level fields:

- `score`
- `verdict`
- `findings`
- `recommendations`
- `evidence`

### Verdict meanings

- **PASS** — no major operational or security issue detected in this lightweight pass
- **WARN** — deployment is usable, but risk or drift is present
- **FAIL** — high-risk exposure or broken runtime signal detected

Example shape:

```json
{
  "score": 82,
  "verdict": "WARN",
  "findings": [
    {
      "level": "MEDIUM",
      "area": "browser",
      "issue": "Chrome remote debugging listener detected (9222)"
    }
  ],
  "recommendations": [
    "Verify Chrome existing-session / remote debugging is enabled intentionally and not left open unnecessarily."
  ]
}
```

---

## Current checks in the script

### 1) OpenClaw runtime status
Runs:

```bash
openclaw status
```

If this fails, the skill treats it as a major runtime health signal.

### 2) Listening ports
Looks for listeners related to likely OpenClaw surfaces, including:
- `18789`
- `3000`
- `9222`
- browser / node / electron processes

This helps surface accidental browser debugging exposure or a missing expected gateway listener.

### 3) Config review
Reads:

```bash
~/.openclaw/openclaw.json
```

Current lightweight checks include:
- `acpx.permissionMode === "approve-all"`
- presence of `chrome-relay`
- invalid JSON
- missing default config path

### 4) Recent log scan
Scans the current day log under:

```bash
/tmp/openclaw/openclaw-$(date +%F).log
```

Looks for patterns such as:
- `AcpRuntimeError`
- `Permission denied`
- `exited with code 1`
- `prerender-error`
- `Could not find LinkedIn editor`

---

## Recommended operator workflow

1. Run the healthcheck.
2. Read the `verdict` first.
3. Review every `HIGH` and `MEDIUM` finding.
4. Apply the narrowest fix that reduces risk.
5. Re-run the check after changes.
6. If internet-exposed, do a separate host/network hardening review before calling it done.

---

## Files

- `SKILL.md` — agent-facing usage instructions
- `scripts/healthcheck.mjs` — executable healthcheck script
- `references/checklist.md` — lightweight review checklist

---

## Notes for future improvement

Good next upgrades for this skill would be:
- add automated tests with fixture configs/logs
- distinguish localhost-only vs public listeners
- inspect gateway bind settings explicitly
- add stale-version / update checks
- add recovery-readiness cross-checks against backup skills
- separate operational findings from security findings more cleanly

---

## Bottom line

Use `openclaw-healthcheck` when you want a **quick, practical safety pass** over an OpenClaw deployment.

It is best for catching **obvious operator mistakes, exposure hints, and runtime drift** before they become expensive.
