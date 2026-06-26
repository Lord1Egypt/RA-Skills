# 🛡️ JEP Guard v2.0.4

**Causal Operating System for OpenClaw Skills**

> *"Your AI agents collaborate. We make sure you can trace why."*

[![Version](https://img.shields.io/badge/version-2.0.4-blue)](https://clawhub.ai)
[![License](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)
[![IETF](https://img.shields.io/badge/IETF-JEP%20Draft-orange)](https://datatracker.ietf.org/doc/draft-wang-jep/)

---

## ✨ What is JEP Guard?

JEP Guard is the **invisible safety layer** for your OpenClaw skills ecosystem.

- 🔒 **Protects** — Blocks risky operations before they happen
- 📊 **Audits** — Records every decision, delegation, and verification
- 🔍 **Traces** — Reconstructs "who did what and why" across multiple agents
- 🏆 **Certifies** — Gives your skills a reputation score others can trust

---

## 🚀 Quick Start (30 seconds)

```bash
# Install
claw install jep-guard

# Initialize (interactive wizard)
claw run jep-guard init

# Start protecting your skills (manual daemon start)
claw run jep-guard daemon --mode skill_os

# Done! Your skills are now causally protected.
```

---

## 📊 User Experience

### For End Users

**Daily Use — Zero Friction**
```
You: "Plan my trip to Tokyo"
planner-skill → search-skill → booking-skill

[JEP Guard] ✅ 12 events protected · 0 blocked · 1 delegation chain
```

**When Things Go Wrong — Full Visibility**
```bash
$ claw run jep-guard log --last

Chain: planner#1 → search#2 → booking#3
  ├─ planner: judged "need flights"
  ├─ search: delegated to booking (scope: [book_flight])
  └─ booking: verified "JAL 123 booked"

Result: SUCCESS · 3.2s · All signatures valid
```

**Reputation Check Before Hiring an Agent**
```bash
$ claw run jep-guard skills reputation booking-skill

booking-skill v2.1
  ✅ Completion rate: 97.3% (145/149 tasks)
  ⚡ Avg response: 1.2s
  🔒 Zero violations
  🏆 JEP Certified
```

### For Skill Developers

**3-Line Integration**
```javascript
const guard = require('@jep-guard/sdk').init('my-skill');

// Before acting
const { token } = await guard.judge({ action: 'write', target: file });

// After acting
await guard.verify(eventId, 'approved', ['sha256:abc...']);
```

**Zero-Config Protection**
Even without SDK integration, JEP Guard protects your skill through OpenClaw hooks:
- File writes → Verified
- Shell execution → Confirmed
- Cross-skill delegation → Routed + logged

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           OpenClaw Skills              │
│  planner · coder · search · deploy     │
├─────────────────────────────────────────┤
│      JEP Guard v2.0 (Daemon)           │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │ Causal  │ │ Skill   │ │ Causal  │ │
│  │ Gate    │ │ Registry│ │ Router  │ │
│  └─────────┘ └─────────┘ └─────────┘ │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │ Policy  │ │Reputation│ │ Dispute │ │
│  │ Engine  │ │ Engine  │ │Resolver │ │
│  └─────────┘ └─────────┘ └─────────┘ │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │  Audit  │ │Extension│ │  TEE    │ │
│  │ Stream  │ │ Loader  │ │ Signer  │ │
│  └─────────┘ └─────────┘ └─────────┘ │
├─────────────────────────────────────────┤
│         JEP Core (4 Verbs)             │
│     J (Judge) · D (Delegate)            │
│     T (Terminate) · V (Verify)          │
└─────────────────────────────────────────┘
```

---

## 🔐 Security & Privacy (v2.0.4 Hardening)

- **Zero Auto-Execution**: Installer never spawns background processes. You start the daemon explicitly.
- **Zero Shell Commands**: No `child_process.exec`, `.spawn`, or `.execSync` in install/uninstall hooks.
- **Explicit Consent**: Full mode requires interactive confirmation; passive mode is default in CI/non-interactive environments.
- **MIT-0 License** — Public domain, forever
- **IETF Standard Track** — JEP draft submitted
- **Privacy by Design** — Digest-only anonymity, TTL expiration, identity rotation
- **Zero Knowledge** — Core verification needs no network calls

---

## 📦 Version History

| Version | Codename | Key Features |
|---------|----------|--------------|
| v1.0.2 | Baseline | Local command intercept, user confirm, temp tokens |
| v1.0.3 | Trust | Built-in Ed25519 signing, standard JEP logs |
| v1.1 | Connect | Cross-agent delegation, skill registry |
| v1.2 | Smart | Policy engine (OPA/Cedar), adaptive confirmation |
| v1.3 | Gate | **Causal Gate** — no event, no execution |
| v1.4 | Deep | Cognitive attestation (SAE), hardware trust (TEE) |
| v1.5 | Platform | **Skill OS** — full inter-skill routing & sandbox |
| v1.6 | Credit | Reputation system, workflow bundles |
| v1.7 | Team | Multi-user audit views, remote sync |
| v2.0 | Federation | **Multi-agent gateway, AEGIS native, unified bus** |
| **v2.0.4** | **Harden** | **Zero shell/exec, zero auto-start, explicit consent** |

---

## 🤝 Contributing

```bash
git clone https://github.com/hjs-foundation/jep-guard.git
cd jep-guard
npm install
npm run dev
```

---

## 📬 Contact

- **Email**: signal@humanjudgment.org
- **GitHub**: https://github.com/hjs-foundation/jep-guard
- **IETF Draft**: https://datatracker.ietf.org/doc/draft-wang-jep/

---

*JEP Guard — Because "it works" is not enough. You need to know **why** it works.*