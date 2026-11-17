> **Bilingual — 中英文皆可适配**  This skill ships both Chinese and English content. The Chinese counterpart of this file is the same name with `.zh` inserted (e.g. `README.zh.md`). The authoritative zh<->en terminology map lives in `references/glossary.yaml`.

# Ontology Agent · Onboarding Guide (GUIDE)

Welcome to **Ontology Agent** — a skill that helps you build your company into a "runnable agent system." After
installing the skill, spend 5 minutes following the 6 steps below; the system auto-detects your company type, matches
the right industry pack, generates your company instance, and builds the expert team in one click.

> The "company instance" you describe lives only in your own runtime environment (local / private) — never sent back,
> never leaves the domain. Sensitive info such as ID numbers, bank cards, and receipt images is never written in plaintext.

---

## Step 0 · You have installed the skill

Seeing this guide means the skill is active. From here you only answer each step's question in **natural language**; the
system structures your answers and auto-generates the config. No technical knowledge required.

## What's built in (capability overview)

- **Three-layer ontology core (thickened)**: semantic layer (13 entity types + 28 relations + 8 global constraints),
  logic layer (12 departments / 141 deduped actions, fused from public methodologies), decision layer (PII red lines +
  multi-role governance + concrete compliance clauses).
- **8 built-in industry packs**: one-person company (opc) / e-commerce (ecommerce) / small-micro (sme) / manufacturing
  (manufacturing, 12 sub-types) / public institution (public_institution) / financial institution (finance) /
  healthcare-biomed (biomed) / education-research (edu_research). opc/ecommerce/sme are easiest to start; the rest match
  on demand.
- **Guided instantiation**: just describe the company in plain language; the system auto-matches the pack, generates the
  instance, builds the expert team in one click; sensitive info never in plaintext, data never leaves the domain.
- **Enterprise-ready**: later connect DingTalk / WeCom / Feishu to assign role views to real employees (see `connectors/`).

## Step 1 · Describe your company type

Tell me in one sentence what kind of company you are, e.g.:
- "I run a one-person company doing AI tech services"
- "I sell on Taobao and Douyin, an e-commerce shop"
- "I started a small company, hired seven or eight people"

The system auto-matches the best pack from `packs/` (8 types built in: one-person / e-commerce / small-micro /
manufacturing / public institution / finance / healthcare / education-research). If unsure, just describe the business
and the system recommends one with reasons.

## Step 2 · Introduce the company

State these as clearly as you can (gaps can be filled later):
- Industry / main business
- Region (e.g. Tianjin, Heping District)
- Legal form (one-person LLC / sole proprietorship / small-micro, etc.)
- Registration info (unified social credit code, founding date, etc., can be added later)
- Scale (headcount, any employees)

## Step 3 · Build departments & expert team

The system gives a **recommended department list** based on the matched pack. The skill ships a **24-department library**
(12 core + 12 optional); a one-person company defaults to the 12 core. You can:
- Accept the recommendation directly (say "build with the recommendation")
- Add/remove departments (e.g. "drop R&D, add a customer service")
- Rename a department (e.g. "rename Finance-Tax to CFO")
- Set a department's role gender to male/female (affects avatar & tone only, not capability)
- Add a fully private AI employee (e.g. "add a Chief Security Officer")
After confirming, say **"build the expert team with this"** and the system generates one AI employee (expert) per
department, each bound to the ontology's corresponding view, reporting to the owner (you).

## Step 3b · Owner profile & company personality (make the digital employees "sound like your company")

This step injects "who runs the company and what temper" into the persona, making the expert team fit you better. State
as clearly as you can (defaults if missing):
- **Owner profile**: how to address you (e.g. "Shunran"), decision style (data/intuition/consultative), risk appetite
  (conservative/balanced/aggressive), communication tone (colloquial/formal, short/detailed, Chinese/zh-en mix),
  authorization boundary (full delegation / owner confirms key actions), professional background, value ranking
  (growth/compliance/profit), taboos (platforms or info not to touch).
- **Company culture**: mission/vision, brand tone (e.g. professional pragmatic), external taboo topics.
- **Business context**: current stage (just founded/growing), core products, customer type (ToB/ToC/government), this
  quarter's goal, tool stack (DingTalk/WeCom/Feishu).
> This info lives only in your local instance, never leaves the domain; switching to another company of the same type
> only swaps this layer, the 24 base department personas stay.
> Your renames / add-removes / gender settings are also written only into your own instance, never modifying the skill
> package itself — the skill package always stays that general "arsenal."

## Step 4 · Inject business logic / workflows

Describe your company's core business flow, e.g.:
"customer orders → I deliver → issue VAT invoice → bookkeeping → monthly tax filing → review & optimize"
The system turns it into an executable workflow (see `logic.yaml`'s stage state machine).

## Step 5 · Get optimization advice

After building, the system proactively gives an "optimization advice pack":
- Missing departments / actions
- Compliance gaps (invoice norms, tax filing, social security, Tianjin local policy, etc.)
- Upgradeable closed-source deep industry packs (e.g. deep tax planning, e-commerce compliance templates)

---

## One-line team-build command (shortcut)

If you've already described the company and confirmed departments, just say:
> **"build the expert team with this"**

The system generates the 12 core (or your selected, 24 in the library total) department experts from
`experts-template/`, auto-assigning the corresponding-gender avatars — no repeated steps.

## What you'll have after completion

- A company instance (`instance.yaml`, in your local stable data dir, e.g.
  `C:\Users\li_sh\.workbuddy\company-data\<company>\instance.yaml`)
- A department-divided AI employee expert team
- A running core business workflow
- A compliance & optimization advice pack
- A company memory log (`company-memory.md`) that continuously accumulates your decisions and risks
- A local ops database (`ops.db`, with todos/department matrix/finance-tax calendar/daily ops report), continuously
  written as the company runs

**Ports to real systems are reserved**: the local data layer (`scripts/ops_db.py`) and DingTalk/WeCom/Feishu connectors
(`connectors/`) are currently stubs — with no API credentials configured they only hint, never network; fill credentials
to enable, no architecture change.

**Key: the instance and memory are persistent.** Every time you open the digital company afterwards, the steward first
reads them so the 12 employees collaborate on the same company facts instead of re-asking you each time. New facts you
confirm in chat are proactively written back by the steward (appended to the memory log, written back to the instance
when necessary), and the company state accumulates across sessions. ID numbers, bank cards, receipt images and other
sensitive info are never written in plaintext.

---

## Nice-to-have · Autonomous monitoring & spontaneous-behavior layer (on by default, can disable)

After building the digital company, it's not just "answer when asked" — when **you haven't actively assigned work and
internal normal operations are unaffected**, it additionally "from time to time" digs up relevant info for the enterprise
(policy benefits / competitor moves / risk warnings / customer signals / ops reminders), like a good employee watching
your back. This is an add-on layer above the core framework, not modifying departments or the action library:

- **Thin profile (little recorded)**: auto-runs general monitoring (policy / industry / opinion / business health),
  immediately "has signal," and in onboarding gently asks you to complete the profile for precision.
- **Thick profile (more recorded)**: adds precise monitoring (competitors / customers / risk / talent), higher hit rate,
  lower noise.
- **No disturbance**: signals handled in four tiers — silent observe / light reminder / **draft awaiting confirmation
  (default)** / execute within authorization; any overreach (tax filing / invoicing / major contracts / fund transfer)
  is always draft + await your confirmation. Intel aggregated into a briefing pushed every 1–3 days.
- On by default: "policy inspection (weekly) + ops daily report"; opinion / competitors / customers / risk one-click
  enable in the expert center.

---

## After building: the digital company proactively onboards you (no need to recall what to give)

You don't have to figure out "what else should I tell the digital company" — the steward owns **progressive proactive
onboarding**: collects company data by priority, only 1–2 items at a time with purpose + reassurance, never a one-time
bombardment, never raising security concerns. Say whatever comes to mind, or "skip / later" anytime. Design notes in
`references/onboarding.md`; at runtime the steward calls `scripts/onboarding.py`.

## Want to see the full structure

`examples/demo_company/` has a **fictional example company's** instance and sample ops DB (with sample data) for you to
follow the structure with your own. Note: this is a generic sample for all users, not Weishu internal data.

## After a skill upgrade: sync the embedded copy inside the digital company

The expert package (digital company) embeds a copy of this skill. After you update the Ontology Agent skill, the
embedded copy **does not auto-change**. Have the steward prompt you to run:
`python <skill dir>/scripts/sync_embedded.py <expert package dir>` to sync (your instance / memory unaffected).
