---
name: lygo-automation-workflows
description: "LYGO Automation Workflows — consent-aware playbook for identifying repetitive lattice/steward tasks worth automating, designing trigger→action plans, and choosing local-first tools (Sandcastle, Continuum, n8n self-hosted) before SaaS. Use when designing LYGO workflows, steward automation audits, or comparing Zapier/Make/n8n under P0/privacy constraints. Not a generic 'automate anything' trigger. Advisor only: no network, no account linking, no auto-publish."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "⚙️"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-automation-workflows"
    requires:
      anyBins: [python, python3]
  lygo: true
  signature: "Delta9Phi963-AUTOMATION-WORKFLOWS-v1.0.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/lygo-automation-workflows"
  inspired_by: "jk-0001/automation-workflows"
  security_review: "1.0.0-narrow-triggers-privacy-first"
  permissions:
    network: false
    shell: false
    subprocess: false
    filesystem:
      write: "optional --write with --i-consent"
    publish: false
---

# LYGO Automation Workflows v1.0.0

**LYGO edition** of the solopreneur automation playbook — rebuilt for the lattice:

- **Narrow triggers** (not every “save time” chat)
- **Privacy / least-privilege / consent** warnings first
- **Local-first** preference: Sandcastle · Continuum · mint · PDW · Ollama army · self-hosted n8n
- **Advisor only** — does not connect Zapier/Make/CRM or move data for you

**Signature:** `Delta9Phi963-AUTOMATION-WORKFLOWS-v1.0.0`  
Inspired by community skill `jk-0001/automation-workflows` (credit); LYGO hardening is original.

---

## When to use

- Designing **LYGO steward / agent** automations with audit trails
- Auditing repetitive lattice ops (ledger rebuilds, witness packs, heartbeat touches)
- Comparing **Zapier / Make / n8n** **after** local options, with privacy constraints
- Emitting a **consent-aware workflow plan JSON** via the local planner CLI

## When NOT to use

- Vague “automate my life” without a concrete recurring task
- Secretly wiring payment/CRM webhooks without steward review
- Auto-publishing to social / ClawHub / HF / live Star Chart
- Any request that needs this skill to **execute** third-party APIs (it won’t)

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-automation-workflows
python scripts/self_check.py
python scripts/workflow_planner.py demo
```

FULL unlocked engineer zip: SkillHub `#full-lygo` → `lygo-automation-workflows-full.zip`

---

## Local planner CLI (optional)

```bash
# Score a task
python scripts/workflow_planner.py audit-task \
  --name "Rebuild PDW ledger" --minutes 10 --frequency-per-month 30 --repetitive

# Emit a plan (stdout); write needs --i-consent
python scripts/workflow_planner.py plan \
  --name "Form to local CRM" \
  --trigger "New form submission" \
  --action "P0-gate payload" \
  --action "Store minimal fields locally" \
  --field email --field name \
  --tool lygo-sandcastle --tool n8n-self-hosted
```

| Command | Network | Subprocess | Writes |
|---------|---------|------------|--------|
| audit-task / plan / demo / self_check | none | none | only `--write` + `--i-consent` |

---

## Step 1 — Identify what to automate (LYGO lens)

Automate tasks you do **≥2×/week** that are **repetitive + rule-based** and **don’t need creative judgment**.

**Time cost:** `(minutes × frequency_per_month) / 60` hours/month.

**Good lattice candidates**
- Scheduled heartbeat / deadman `touch`
- Digest/witness packs from known local files
- Continuum seal after a known folder of claims
- Mint → anchor snippet generation (human still posts)
- Rebuild ledgers / run self_checks

**Keep manual**
- Champion persona replies that need nuance
- Live Star Chart accepts
- Anything touching raw payment/PII until a privacy design exists

---

## Step 2 — Choose tools (local-first)

| Preference | Tool | Notes |
|------------|------|-------|
| **1st** | `lygo-sandcastle` | YAML workflows + P0 gate on your hardware |
| **1st** | `lygo-continuum` / integrator | Falsifiable receipts · ∫(Truth×Light) |
| **1st** | Self-hosted **n8n** | Full control; still needs least-privilege tokens |
| **2nd** | Make / Zapier | SaaS — treat as untrusted egress; minimize fields |
| **Avoid by default** | Blind multi-vendor CRM+payment+Slack chains | High breach blast radius |

---

## Step 3 — Design (with privacy)

```
TRIGGER: …
CONDITIONS: … (+ P0 / validation)
ACTIONS: …
DATA FIELDS: list every field moved (minimize)
VENDORS: list every system that receives data
ERROR HANDLING: alert steward — never silent fail
DISABLE PATH: how to turn it off + who can audit logs
CONSENT: who approved connecting each vendor
```

**Hard rules**
- No secrets in Slack/email alerts
- Prefer redacted notifications
- Document retention
- Human remains the publisher for social/lattice posts

---

## Step 4 — Build & test

1. Dry-run / validate each step  
2. Test empty fields + garbage input (P0)  
3. Confirm failure alerts fire  
4. Only then enable on a schedule  

---

## Step 5 — ROI (same math, LYGO values)

Payback months ≈ setup cost / monthly time-value saved. Prefer payback **&lt; 3 months**, unless the automation unlocks safety (e.g. deadman heartbeat).

---

## Mistakes to avoid (LYGO)

- Automating a broken process  
- Over-broad skill triggers (“automate everything”)  
- No error handling  
- Moving PII/payments across vendors without consent review  
- Skipping Continuum/mint receipts for consequential runs  

---

## Pair with

| Skill | Role |
|-------|------|
| `lygo-sandcastle` | Local YAML orchestrator |
| `lygo-continuum` | Seal done claims |
| `lygo-continuum-integrator` | Integral / phase-lock receipts |
| `lygo-mint-verifier` | Hash packs + anchor snippets |
| `lygo-pure-data-witness` | Digest archives (consent-gated fetch) |
| `lygo-protocol-stack-operator` | Full stack ops |

---

## Security

See `references/SECURITY.md` and `references/SKILLSPECTOR_AUDIT.md`.

**Δ9Φ963 — automate the repetitive · protect the sensitive · consent before vendors · human publishes.**
