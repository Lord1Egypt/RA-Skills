---
name: ontology-agent
description: >-
  Ontology Agent — a self-contained, vendor-neutral, portable skill that turns any company description into a runnable
  business "ontology": a knowledge graph (semantic layer) + logic graph (logic layer) + decision graph (decision
  layer) + an AI expert team. As the company grows it can connect to real people and IM (DingTalk / WeCom / Feishu).
  Use it when you want to digitize a company, build an AI-employee team, model an enterprise as agents, or turn a
  one-person company / e-commerce / small business into a runnable agent system. Trigger words: ontology, enterprise
  digital twin, AI employees, expert team, one-person-company setup, enterprise knowledge graph, Ontology Agent, turn
  my company into agents. China-optimized edition (24 departments, 8 industry packs, DingTalk/WeCom/Feishu connectors).
  For enterprise-grade deployment (custom build / edge-cloud sync / air-gapped Palantir-style mode) contact Weishu AI.
version: 1.2.0
type: product
category: Productivity
platforms: [WorkBuddy, ClawHub]
---

> **Bilingual — 中英文皆可适配 (Chinese and English are both fully supported)**
> This skill ships **both** Chinese and English content, so it serves Chinese- and English-speaking users alike.
> Routing rule — pick the edition by the user's language:
> - **English user** → read the default files: `SKILL.md`, `README.md`, `GUIDE.md`, `references/*.yaml`, `references/packs/*.yaml`, `experts-template/*.yaml`.
> - **Chinese user** → read the `.zh` counterparts: `SKILL.zh.md`, `README.zh.md`, `GUIDE.zh.md`, `references/*.zh.yaml`, `references/packs/*.zh.yaml`, `experts-template/department_experts.zh.yaml`.
> - Both editions are **complete**: every kernel file (semantic / logic / decision / action_specs / department_actions / 8 industry packs / department experts / monitoring / deployment / roles / proactive) plus the docs `customization.md`, `onboarding.md`, `portability.md`, `product_intro.md`, `LICENSE.md`, `THIRD-PARTY.md` exist in both languages — 31 `.zh` files in total.
> - Machine keys are **identical** in both editions (action `slug`, department codes, `source` codes, entity type names, and the entire `scripts/` + `experts-template/` layer), so every script works unchanged in either language.
> - Authoritative zh↔en terminology map: `references/glossary.yaml`.

# Ontology Agent

## What this is

A self-contained, vendor-neutral, portable Skill. You install it, describe your company in plain language, and it
builds that company into a runnable "ontology":

**Knowledge graph (semantic layer) + Logic graph (logic layer) + Decision graph (decision layer) + an AI expert team**,
and as the company grows it can connect to real people and IM.

> Install one Skill, turn your company into a runnable agent system.

**This "company brain" seamlessly switches between three deployment shapes** (see `references/product_intro.md` and
`references/deployment.yaml`):
- **A · Skill package (current)**: runs on the WorkBuddy cloud runtime — subscribe and use, zero ops.
- **B · Edge-cloud sync**: edge keeps the core, cloud handles the heavy lifting (reference impl: OpenBMB EdgeClaw Box); sensitive data never leaves the domain.
- **C · Fully on-prem**: the whole spec + runtime self-hosted, fully offline (air-gapped), Palantir-style.

All three shapes share the same vendor-neutral ontology spec — swap the shell and it just works, **perfectly
self-consistent**. It already delivers a **readable, writable, closed-loop digital twin** of a company, and automates
Palantir's **FDE (Forward-Deployed Engineer)** delivery model into an out-of-the-box AI-FDE — the owner digitizes the
company just by chatting.

## First step after install (guided instantiation)

New users follow these six steps to describe their company; the skill auto-matches an industry pack, generates an
instance, and builds the expert team. Full guidance in `GUIDE.md` (detailed Phase-5 version); here is the instant
entry point:

0. **Read the guide**: start with `GUIDE.md` (six-step English guide).
1. **Name your company type**: one-person company / e-commerce / small business / other.
2. **Introduce the company**: industry, region (e.g. Tianjin), scale, registration info.
3. **Pick departments**: the skill ships a **24-department library** (12 core defaults + 12 optional) — accept the recommendation or mix freely; you can later rename / set gender / add private departments (see below).
4. **Describe business logic**: core flows (e.g. order → invoice → bookkeeping → tax filing).
5. **Get optimization advice**: after building, the skill suggests missing departments / compliance gaps / closed-source upgrade packs (open-core monetization entry).

→ The skill matches the corresponding pack under `references/packs/`, writes the profile into `instance.yaml` (separate
from the template), and builds the expert team in one click.

## Where the company instance lives (persistence · digital-twin source of truth)

The generated `instance.yaml` is the company's **authoritative source of truth** (basics, departments, workflows,
owner profile, culture, context). It defaults to a stable data directory (separate from the skill code, valid across
workspaces):

- Weishu example: `C:\Users\li_sh\.workbuddy\company-data\weishu\instance.yaml`
- Companion memory log: `C:\Users\li_sh\.workbuddy\company-data\weishu\company-memory.md`

**The digital company (expert team) automatically Reads these two files at the start of every session**, collaborating
on the same company facts. When the owner confirms a new fact / decision / risk, the steward **appends** it to the
memory log and writes back to the instance when necessary. This way the company state accumulates across sessions
instead of being rebuilt empty each time. PII (ID numbers, bank cards, receipt images) is never written in plaintext.
> This data directory is the persistent layer of the "digital twin"; when later connecting real systems (knowledge
> base / IM), the source of truth migrates from here to a database.

## File map
```
ontology-agent/
  SKILL.md                  # you are here: entry point
  GUIDE.md                  # six-step user onboarding guide
  references/
    product_intro.md        # product intro copy (for users/channels/investors: 3 modes + digital twin + AI-FDE)
    contact.yaml            # vendor contact info (site/email/phone + enterprise deployment guidance; AI can read & answer)
    deployment.yaml         # three deployment shapes + sync boundaries + runtime options
    portability.md          # portable deployment & integration (Mode B/C landing artifacts, export + integration flow)
    glossary.yaml           # bilingual term standard layer (zh/en reference throughout: 24 dept codes / 18 semantic entities / 8 industry packs / source codes)
    semantic.yaml           # semantic layer template (13 entity types full fields + 28 relation library + 8 global constraints)
    logic.yaml              # logic layer template (references action_specs + stage state machine + industry workflows)
    decision.yaml           # decision layer (13 decision rules + concrete compliance clauses incl. Tianjin policy)
    roles.yaml              # multi-role governance (Phase 3, reserved for enterprises)
    department_actions.yaml # 24 departments / 177 action list (12 core + 12 optional, dedup-merged)
    action_specs.yaml       # 159 action full specs (141 core + 18 optional-dept extensions; desc/inputs/outputs/uses_entities/skill_ref)
    packs/                  # industry packs (Phase 4)
      opc.yaml              # one-person company (first release)
      ecommerce.yaml        # e-commerce
      sme.yaml              # small & micro business
      manufacturing.yaml    # manufacturing factory (12 sub-types in subtypes section)
      public_institution.yaml # public institution / government-affiliated unit (state assets / gov procurement / staffing)
      finance.yaml          # financial institution (AML / suitability / capital regulation, reference non-legal opinion)
      biomed.yaml           # healthcare / biomedicine (genetic resources / GMP / health data)
      edu_research.yaml     # education / research institute (research funding / tech transfer)
    onboarding.md           # progressive proactive onboarding design notes (the digital company owns onboarding)
    customization.md        # user private customization mechanism (rename/add-remove/gender, zero intrusion to skill package)
    monitoring.yaml         # autonomous monitoring signal domains + toggleable automation templates
    proactive.yaml          # spontaneous-behavior four-tier grading + authorization gate
  experts-template/         # 24-department team-building template (12 core + 12 optional)
  assets/avatars/           # avatar pool (24 core × male/female + team icon + generic backups; by gender, distributable)
  connectors/               # DingTalk / WeCom / Feishu connectors (stub, API ports left, no network by default)
  scripts/
    init.py                 # guided interview + pack selection + instance generation + team build
    ops_db.py               # local data layer SQLite (knowledge-base 4 core tables + extension tables, remote master port left)
    onboarding.py           # progressive onboarding engine (reads instance, returns next questions + progress)
    sync_embedded.py        # sync embedded expert package after skill update
    avatars.py              # avatar selection + gender logic + write to expert package
    monitor.py              # autonomous monitoring engine (thin/thick profile parse + signal ingestion)
    proactive.py            # spontaneous-behavior engine (grading + intel briefing)
    export_spec.py          # spec exporter: spec + instance packed into portable bundle
    adapters.py             # integration config generator: vendor-neutral mode list + reference impls + host-platform scaffolds
  examples/                 # generic demo seed (fictional example company, for other users to reference structure, not Weishu-specific)
    demo_company/
  VERSION                   # skill version number (for sync comparison)
  THIRD-PARTY.md / LICENSE / README.md
```

## Connecting real systems (port layer · no network by default)

The skill ships with the **framework and ports** to connect real systems, but everything defaults to stub state — when
any external API credential is missing it only prints a hint and never makes a real network request, guaranteeing
install-and-use, no misfires, no leaks.

- **Local data layer** (`scripts/ops_db.py`): lands the knowledge-base 4 core tables (todo inbox / department matrix /
  finance-tax calendar / daily ops report) + extension tables as SQLite, default at `company-data/<company>/ops.db`,
  same directory as `instance.yaml` (digital-twin persistent layer). Remote master integration: see `RemoteDatasource`
  in the same file (fill space_id / api_token / endpoint to enable dual-write).
- **IM connectors** (`connectors/`): unified DingTalk / WeCom / Feishu interface (send msg / receive events / pull
  members); fill each platform's `CREDENTIALS` and complete the `TODO` to enable.

So you can run the company locally and accumulate operational data right now; once you get DingTalk / WeCom / Feishu or
knowledge-base API credentials, fill them in to switch from stub to real integration — no architecture change needed.

## Skill update → sync embedded expert package (important)

The expert package (digital company) embeds a copy of this skill. After the skill itself upgrades, **the embedded copy
does not auto-change**. Run the sync script (or let the digital company remind you to run it):

```bash
python <skill dir>/scripts/sync_embedded.py <expert package dir>
```

- At the start of every session the digital company (steward) compares the "embedded copy VERSION" with the
  "user-level skill VERSION" (`~/.workbuddy/skills/ontology-agent/VERSION`); if they differ, it proactively prompts you
  to run the sync command above.
- Sync contents: SKILL.md / GUIDE.md / VERSION / references/ / scripts/ / connectors/ / experts-template/;
  it **never touches** your `instance.yaml` / `company-memory.md` (that's your data, not the skill itself).

## The digital company proactively onboards you (progressive Onboarding)

You don't have to remember "what should I tell the digital company" — the digital company owns onboarding and
progressively collects company data by priority: only 1–2 highest-priority gaps at a time, with purpose + reassurance,
never a one-time bombardment, never raising security concerns. See `references/onboarding.md`; at runtime the steward
calls `scripts/onboarding.py` to get the next question and post progress. Generic demo seed in `examples/demo_company/`.

## 24-department library & user private customization (no change to skill package integrity)

The skill ships **24 departments** (`experts-template/department_experts.yaml`):
**12 core** (Lead / Admin / HR / Finance-Tax / Legal / R&D / Content / Channel / SEO / Sales / Data / Strategy, default
team) + **12 optional** (Customer Service / Product / Design / Ops / Procurement / Quality / IT-Security / PR /
Investment-Finance / Customer Success / Cross-border / Risk-Control, activate on demand). This way the general edition
still defaults to 12 (preserving the validated experience) while the package is fully stocked for most commercial
enterprises.

**Users can privately customize any department, and it is always stored only in their own `company-data/<company>/instance.yaml`, never modifying the skill package itself:**

| Operation | Command | Touches skill package? |
|-----------|---------|------------------------|
| Rename | `python scripts/init.py --slug <short> --rename finance "Chief Financial Officer"` | No |
| Set gender (avatar/tone only) | `python scripts/init.py --slug <short> --gender sales female` | No |
| Disable dept | `python scripts/init.py --slug <short> --disable mkt_seo` | No |
| Add private AI employee | `python scripts/init.py --slug <short> --add-dept cso --name "Chief Security Officer" --gender male --expertise "security strategy, compliance governance"` | No |
| List current depts | `python scripts/init.py --slug <short> --list-depts` | — |
| Browse 24-dept library | `python scripts/init.py --catalog` | — |

**Language flag — `--lang en|zh` (default `en`):**

Every command above accepts `--lang`. It switches the *kernel data* the scripts read, so the same
installation serves both audiences:

| `--lang` | Kernel files read | Expert names & terms | Industry pack |
|----------|-------------------|----------------------|---------------|
| `en` (default) | `references/*.yaml`, `packs/*.yaml` | English | English pack |
| `zh` | `references/*.zh.yaml`, `packs/*.zh.yaml` | Chinese | Chinese pack |

Machine keys (action `slug`, `source` codes, department codes, entity type names) are byte-identical
in both languages, so scripts and `instance.yaml` behave the same either way.

```bash
python scripts/init.py --demo --lang en    # English expert team
python scripts/init.py --demo --lang zh    # Chinese expert team, Chinese kernel
```

> Merge logic in `scripts/init.py: resolve_departments()`; details in `references/customization.md`.
> During progressive onboarding the digital company gently suggests optional departments and explicitly states "these
> changes live only in your own company data, never modifying the skill package."

## Avatars & gender (better experience)

- Avatar pool `assets/avatars/` ships: 12 core departments × male/female (24) + team icon `team.png` + 4 generic
  backups (2 each gender).
- Each department has a `gender_default`; after the user overrides with `--gender`, regenerating/syncing the expert
  package applies the corresponding avatar. **Gender only affects avatar and tone, never department capability.**
- Optional 12 departments and custom departments fall back to the generic pool if they have no dedicated avatar; a
  dedicated avatar can be generated with one command when needed.
- Write the chosen avatar into the expert package: `python scripts/avatars.py --slug <short> --pkg <expert package dir>`.

## Autonomous monitoring & spontaneous-behavior layer (nice-to-have · zero intrusion · Phase 10)

On the premise that the user has **not actively assigned work and internal normal operations are unaffected**, the
digital company additionally "from time to time" digs up information relevant to the enterprise, making the user feel
"like a good employee is watching my back." This layer sits above the core framework as an **add-on layer**, not
modifying the 24-department template / 159-action library / decision governance.

- **What it monitors**: see `references/monitoring.yaml` — 8 signal domains (policy / industry hotspot / public opinion
  / business health / competitors / customers / risk / talent), each mapped to a real department + existing action;
  **thin profile** (little recorded) runs general domains (policy / industry / opinion / business health), **thick
  profile** (more recorded) adds precise domains (competitors / customers / risk / talent).
- **Spontaneous logic**: see `references/proactive.yaml` — trigger pipeline (signal → relevance → value score →
  authorization check → decision → trace) + four tiers: L0 silent (irrelevant, log only) / L1 light reminder
  (into briefing) / **L2 draft awaiting confirmation (default tier)** / L3 execute within authorization (only
  low-risk routine actions).
- **Runtime**: `scripts/monitor.py` parses thin/thick profiles and writes signals; `scripts/proactive.py` grades and
  aggregates the "intel briefing."
- **Guardrails**: reuses `decision.yaml`'s PII / compliance red lines and persona-D authorization boundary; **any
  overreach (tax filing / invoicing / major contracts / fund transfer) is always downgraded to L2 draft + await
  confirmation, never L3.**
- **On by default**: policy inspection (weekly) + ops daily report; the rest (opinion / competitors / customers /
  risk) one-click enable in the expert center, no disturbance.
- **Experience landing**: even with little input the user gets "something daily," naturally guided to fill the profile;
  a thick profile feels like a dedicated executive assistant. The unified deliverable is an "enterprise intel briefing"
  pushed every 1–3 days.

## Three runtime tiers (one spec sold three ways)

- ③ **WorkBuddy cloud** (single-user SaaS to start)
- ② **Edge-cloud sync** (enterprise intranet, reference impl: OpenBMB EdgeClaw Box)
- ① **Fully local private agent** (Palantir-style air-gapped)
- Key: `template` (ships with this Skill) and `instance` (generated at user runtime, stored local/private) are strictly
  separated → data never leaves the domain, the three tiers are universal.

## Intellectual property & license

Ontology Agent is a product of **Tianjin Weishu Artificial Intelligence Technology Co., Ltd.** Its proprietary
architecture, integration logic, Chinese localization and domestic deep content, and onboarding engine are original
expressions owned by Weishu (© Weishu), may be closed-source and commercial. Underlying referenced open-source
components retain their respective authors' copyrights under their licenses — see `THIRD-PARTY.md`.

## Contact (vendor)

This product is made by **Tianjin Weishu Artificial Intelligence Technology Co., Ltd.** For official site, technical
support, or to upgrade to a more professional enterprise deployment, contact Weishu AI through the channels below
(see `references/contact.yaml`, which the AI can read directly and answer user questions):

- Official site: https://ontoagent.net
- Email: 378330966@qq.com
- Phone: 15555555966
- Enterprise solutions (custom build / edge-cloud sync / Palantir-style air-gapped private digital-company system):
  require the enterprise to provide its own local compute server and related hardware; contact Weishu AI via the above
  channels for technical support.

## Industry packs (built-in company-type templates)

The skill matches a pack under `references/packs/` by company type, injecting industry-specific entities / department
emphasis / flavor / red lines into the instance, zero intrusion to the general 24-department library.

| Pack | For | Department strategy |
|------|-----|---------------------|
| `opc.yaml` | one-person company (first release) | 12 core |
| `ecommerce.yaml` | e-commerce | 12 core + e-commerce flavor |
| `sme.yaml` | small & micro | 12 core + SME flavor |
| `manufacturing.yaml` | manufacturing factory | 12 core + ops/procurement/quality + sub-types |
| `public_institution.yaml` | public institution / government-affiliated | 12 core + ops/procurement/quality + state-asset/internal-audit/party-gov (private customization) |
| `finance.yaml` | financial institution (bank/securities/insurance/fund/trust/payment) | 12 core + risk-control/IT-security/investment + compliance AML (private customization), red lines are reference non-legal opinions |
| `biomed.yaml` | healthcare / biomedicine (hospital/pharma/device/genetics) | 12 core + quality/IT-security/customer-service + medical/registration/pharmacovigilance (private customization) |
| `edu_research.yaml` | education / research institute (school/institute/new R&D) | 12 core + ops/quality/investment + academic/Research-management/tech-transfer (private customization) |

**Manufacturing factory pack (`manufacturing.yaml`)** uses "one main pack + built-in subtypes section" to cover
sub-sectors without a separate file each (avoids bloat):
- Common: factory/line/equipment/process/work-order/yield/capacity/material/BOM/supplier entities; produce→QC→deliver
  core loop; safety/environment/quality-system (ISO9001·IATF16949·GMP·CCC)/special-equipment/fire-protection red lines
  (`decision.yaml` `manufacturing_safety`); manufacturing-specific monitoring signals (downtime/OEE, yield fluctuation,
  material break, safety-env incident, energy, recall — see `monitoring.yaml` `manufacturing` domain).
- 12 sub-types (auto-matched by match_keywords, only differences filled): apparel-textile / food-beverage /
  electronics / machinery (heavy) / chemical / building-materials / pharma-bio / FMCG / automotive-parts / metal-smelting
  / packaging-printing / plastic-toys.
- Manufacturing "heart" departments (production/manufacturing, equipment-engineering, process-engineering) are not in
  the 24-department general library; suggested via `suggested_custom_departments` for the user to privately add, no
  change to skill package integrity.

## Portable deployment & integration (Mode B / Mode C landing)

The spec layer is vendor-neutral data; three modes = same spec + different runtime shells. **Swap the shell and it
works, the business brain is not lost, no rewrite.**
- Export spec: `python scripts/export_spec.py --bundle all --slug <short> --zip` → generates self-contained
  `exports/<short>_ontology_bundle/` (all `references/` + instance + `manifest.json` contract). `--bundle source`
  exports only the blank spec template, `--bundle instance` only the digital twin.
- Integrate runtime: `python scripts/adapters.py --bundle exports/<short>_ontology_bundle --pattern edge_cloud`
  (vendor-neutral mode list, main output)
  - Reference impls (pick any): `--target edgeclaw` (OpenBMB EdgeClaw Box) / `--target joyagent` (JD JoyAgent-JDGenie)
    / `--target both`
  - **Mode B edge-cloud sync (ref impl: OpenBMB EdgeClaw Box)**: produces `edgeclaw_manifest.yaml`, `sync_boundary`
    keeps sensitive on edge, external brain to cloud, auto splits edge/cloud by department sensitivity (`lead/admin/hr/
    finance/legal` stay on edge).
  - **Mode C fully on-prem (ref impl: JD JoyAgent-JDGenie)**: produces `joyagent_manifest.yaml` +
    `joyagent.docker-compose.yml` (deploy template hint), fully offline, local model, spec zero-rewrite, ERP/MES
    write-back hooks.
- Host-platform "wrap scaffold" (answering "is it WorkBuddy-only?"): `python scripts/adapters.py --slug <short>
  --target coze|dify|claude|yuanqi|qianfan|workbuddy` → ports the same vendor-neutral spec to competitor platforms, spec
  zero-rewrite.
- Both scripts read-only references / instance, **never modify** the core; the integration manifest only *references*
  the spec (`./references`, `./instance`), zero-rewrite — this is the ground of "perfectly self-consistent access."
  Full flow in `references/portability.md`.

## Term convention (bilingual term standard layer)

All yaml machine keys are English, user-facing text is Chinese; the mapping lives in `references/glossary.yaml`. Register
new terms in the glossary before use.

**Standard layer scope**: `glossary.yaml` already covers — core four layers / atomic concepts / packaging-instantiation
/ governance-security / 8 industry packs / three runtime tiers / connectors / source codes / **24 department codes
zh-en** / **18 semantic entities zh-en** / reference-library sources. The standard layer is injected into the expert
`system_prompt` as a "term standard layer · zh-en mapping" appendix (see `scripts/init.py: glossary_block()`),
ensuring every AI employee uniformly uses Chinese terms while recognizing internal English identifiers — the standard
layer is **actually used**, not left idle. IP registration note: user-facing terms carry no "original/borrowed" tag;
the source-code section only records action provenance (OPB/Frog/slav/ReS/sober/easy are borrowed, WSHU is Weishu's
own), registered in a dedicated attachment under the "cite + lightweight modification + no exclusive claim" discipline.
