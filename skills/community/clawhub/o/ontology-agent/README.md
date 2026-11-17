> **Bilingual — 中英文皆可适配**  This skill ships both Chinese and English content. The Chinese counterpart of this file is the same name with `.zh` inserted (e.g. `README.zh.md`). The authoritative zh<->en terminology map lives in `references/glossary.yaml`.

# Ontology Agent

A self-contained, vendor-neutral, portable Skill: you install it, describe your company in plain language, and it
builds that company into a runnable "ontology" — **knowledge graph (semantic layer) + logic graph (logic layer) +
decision graph (decision layer) + an AI expert team**, and as the company grows it can connect to real people and IM
(DingTalk / WeCom / Feishu).

> Install one Skill, turn your company into a runnable agent system.

## Quick start

See **`GUIDE.md`** (six-step English guide): describe company type → introduce situation → build department expert
team → inject owner profile & culture → inject business logic → get optimization advice.

Entry-point details in **`SKILL.md`**.

## Three deployment shapes

- **A · Skill package (current)**: runs on the WorkBuddy cloud runtime — subscribe and use, zero ops.
- **B · Edge-cloud sync**: edge keeps the core, cloud handles the heavy lifting (reference impl: OpenBMB EdgeClaw Box); sensitive data never leaves the domain.
- **C · Fully on-prem**: the whole spec + runtime self-hosted, fully offline (air-gapped), Palantir-style private deployment.

All three shapes share the same vendor-neutral ontology spec — swap the shell and it works.

## Directory

```
SKILL.md        entry point & overall explanation
GUIDE.md         six-step user onboarding
references/      three-layer ontology (semantic/logic/decision) + industry packs + bilingual term standard layer
scripts/         onboarding/build/monitor/export/integration engines
connectors/      DingTalk / WeCom / Feishu connectors (stub, no network by default)
experts-template/ 24-department team template
assets/avatars/   avatar pool
THIRD-PARTY.md   open-source components & license notices
LICENSE          copyright & license
```

## Copyright

© Tianjin Weishu Artificial Intelligence Technology Co., Ltd. See `LICENSE`.
