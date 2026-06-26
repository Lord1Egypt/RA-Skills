# JEP Guard

**Causal Operating System for OpenClaw Skills**

> Invisible protection. Complete audit. Trusted reputation.

## Install

```bash
claw install jep-guard
```

## Quick Start

```bash
# Initialize (interactive wizard)
claw run jep-guard init

# Start daemon (explicit manual start)
claw run jep-guard daemon --mode skill_os

# View dashboard
claw run jep-guard dashboard
```

## What It Does

- **Protects** — Blocks risky operations before execution (Causal Gate)
- **Audits** — Records every judgment, delegation, verification in JEP format
- **Traces** — Reconstructs "who did what and why" across multiple agents
- **Certifies** — Gives skills reputation scores based on real performance

## For Users

```
You: "Plan my trip to Tokyo"
planner-skill → search-skill → booking-skill

[JEP Guard] ✅ 12 events protected · 0 blocked · 1 chain
```

## For Skill Developers

```javascript
const guard = require('@jep-guard/sdk').init('my-skill');

// Before acting
const { token } = await guard.judge({ action: 'write', target: file });

// After acting
await guard.verify(eventId, 'approved', ['sha256:...']);
```

## Architecture

```
OpenClaw Skills
      ↓
JEP Guard Daemon
  ├── Causal Gate      (pre-execution control)
  ├── Skill Registry   (identity + capabilities)
  ├── Causal Router    (cross-skill delegation)
  ├── Policy Engine    (OPA/Cedar rules)
  ├── Reputation       (objective scoring)
  └── Audit Stream     (JEP standard export)
```

## Security Notes (v2.0.4)

- Installer does **not** auto-start background processes.
- No shell commands are executed during install/uninstall.
- Full-protection mode requires explicit interactive consent.

## References

- IETF JEP Draft: https://datatracker.ietf.org/doc/draft-wang-jep/
- IETF JAC Draft: https://datatracker.ietf.org/doc/draft-wang-jac/
- License: MIT-0 (Public Domain)