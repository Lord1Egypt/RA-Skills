> **Bilingual — 中英文皆可适配**  This skill ships both Chinese and English content. The Chinese counterpart of this file is the same name with `.zh` inserted (e.g. `README.zh.md`). The authoritative zh<->en terminology map lives in `references/glossary.yaml`.

# Ontology Agent · Product Introduction

> This is the unified intro copy for users / channels / investors. Positioning, three modes, digital twin and AI-FDE
> vision are based on landed capabilities, no exaggeration; scale and rigor are below tier-one vendors, but on the same
> spectrum and extensible.

---

## 1. One-line positioning

**Ontology Agent is a general engine that "turns any enterprise into a runnable digital twin."**

You install it, describe your company in natural language, and it auto-builds that company into an AI expert team + a
readable, writable, executable, closed-loop business knowledge network — and **the same "company brain" seamlessly
switches between three deployment shapes.**

> Install one Skill, turn your company into an agent system that works on its own.

---

## 2. The real core IP: the vendor-neutral "ontology spec"

Most AI tools sell a "shell" (some app, some platform). We sell the **spec layer** inside — a vendor-neutral, portable
enterprise ontology:

- **Semantic layer**: defines a company's people, departments, customers, orders, contracts, equipment… as related
  "business entities" (not cold table fields).
- **Logic layer**: writes core business flows (order→produce→deliver→collect) as orchestratable state machines and functions.
- **Decision layer**: writes "who can do what, where the red lines are, when the owner must confirm" as governance rules.
- **Action library**: 141 directly callable enterprise actions (invoicing, tax filing, opinion monitoring, risk warning…).
- **24-department library + industry packs + private customization**: general skeleton + industry flavor + your own fine-tuning.

This spec is **pure data (YAML)**, not bound to any runtime platform. Which means —

> **It is not software that only runs in one place, but an "enterprise OS spec" you can carry with you and use by
> swapping the shell.**

---

## 3. Three deployment shapes: one spec, three landings

This is what sets the product apart from ordinary AI tools: **the same company brain, three delivery modes, upgrade as
needed, no re-buy, no re-build.**

| Shape | Essence | For whom | Where's data |
|---|---|---|---|
| **A · Skill package (current)** | spec runs on WorkBuddy cloud runtime, subscribe & use, zero ops | SMEs / OPC / want to try first | instance local + KB in cloud |
| **B · Edge-cloud sync** | "edge keeps core, cloud handles heavy": sensitive data stays local, complex reasoning & external retrieval go cloud (ref impl: OpenBMB EdgeClaw Box) | manufacturing, regulated industries, with shop floor, data must not leave domain | sensitive on edge, public intel on cloud |
| **C · Fully on-prem** | whole spec + runtime self-hosted, fully offline (air-gapped), Palantir-style air-gap deployment (ref impl: JD JoyAgent, Dify and other open frameworks) | military / government / strong-compliance core assets | all local, nothing out the door |

**Why "perfectly self-consistent access" to the other two?** Because the other two runtime shapes just put the same spec
into different "runtime shells" (edge light box / self-hosted open framework; EdgeClaw, JoyAgent, Dify etc. as reference
impls) — semantic, logic, decision identical, so when the enterprise switches shape the business brain is not lost, not
rewritten. We deliberately don't bind the product to any single vendor — any product meeting the "runtime capability
contract" can connect (see `references/deployment.yaml`'s `patterns` section).

**Then can it only run on WorkBuddy?** Today the skill's "shell" is the WorkBuddy format, so it runs directly on
WorkBuddy; but that "vendor-neutral ontology spec" depends on no platform. We provide `adapters.py`'s host-platform
"wrap scaffold" (Coze / Dify / Claude / Tencent Yuanqi / Baidu Qianfan / WorkBuddy etc.) to port the same spec to
different competitor platforms, **spec zero-rewrite** — so our real IP is the "spec," not "some platform's shell."

---

## 4. What it already delivers: enterprise digital twin + AI-FDE auto-delivery

### 4.1 Enterprise digital twin (vs Palantir Ontology)

Traditional digital twin is a "read-only 3D model." Ours is a **readable, writable, executable, closed-loop dynamic
business OS**: the AI expert team collaborates on the same company source of truth, and when it spots an opportunity it
can draft action, overreach only awaits your confirmation — exactly the "digital twin" core of tier-one vendors'
Ontology.

### 4.2 AI-FDE: automating the "forward-deployed engineer" (vs Palantir FDE / Zhongshu Ruizhi AI-FDE)

Palantir relies on **FDE (Forward Deployed Engineer)** to go deep into the client site and spend 6–9 months building the
Ontology; domestic "China's Palantir" Zhongshu Ruizhi has upgraded it to **AI-FDE** — letting agents be "digital field
engineers," taking 80%+ of standardized work (requirements understanding, ontology modeling, rule configuration),
compressing delivery to 1–2 months.

**Our system is essentially an out-of-the-box AI-FDE**: progressive onboarding auto-walks the enterprise through the
full Ontology landing flow "define entities → build relations → configure rules → executable actions." The owner needs
no tech skills — digitizes the company just by chatting.

> In one line: what tier-one vendors deliver with a consultant team in months, we generate instantly with one Skill.

---

## 5. Use cases: who should use it

- **One-person company / OPC, e-commerce, small-micro**: out of the box, 12 AI employees on duty immediately.
- **Manufacturing factory**: built-in manufacturing industry pack (apparel / food / electronics / machinery / chemical
  etc., 12 sub-types), produce→QC→deliver core loop + safety/environment/quality red lines.
- **Public institution / financial / healthcare / education-research**: built-in 4 horizontal industry packs — public
  institution (state assets / gov procurement / staffing), finance (AML / suitability / capital regulation, red lines are
  reference framework not legal opinion), healthcare (human genetic resources / GMP / health data), education-research
  (research funding / tech transfer); each pack's industry "heart" departments can be privately added.
- **Regulated / with shop floor / data must not leave domain**: upgrade to edge-cloud sync, sensitive business loops locally.
- **Military / government / strong-compliance core**: upgrade to fully on-prem, fully offline, auditable.
- **Enterprises wanting a "good employee" experience**: autonomous monitoring + spontaneous-behavior layer makes the
  digital company from time to time proactively dig up policy, competitors, risk relevant to you — like a real good
  employee watching your back.

---

## 6. Room to grow: what it will become

1. **Industry packs keep expanding**: 8 built in (OPC / e-commerce / small-micro / manufacturing / public institution /
   finance / healthcare-biomed / education-research); later energy, logistics, agriculture etc.
2. **Deeper autonomy**: monitoring & spontaneous behavior from "draft + remind" toward "execute within authorization,"
   the digital company more like a real team.
3. **Full-spectrum three-mode coverage**: from zero-threshold trial to strong-compliance on-prem, a full-lifecycle
   digitalization base for one enterprise.
4. **Portable delivery shape**: spec exportable, sellable to other enterprises, portable to any edge-cloud / fully-on-prem
   runtime (ref impls EdgeClaw, JoyAgent, Dify), or via "wrap scaffold" to Coze / Dify / Claude / Yuanqi / Qianfan host
   platforms — **this is Weishu's real IP and the future commercialization base.**

---

## 7. Continuous refinement: private customization self-heal + feedback

Ontology Agent is a multi-industry enterprise ontology, large in size; in actual use occasional minor semantic, logic or
functional shortcomings are normal. If you hit one, no need to wait for a version update — just describe the problem to
your "steward": the steward privately customizes a fix **without modifying the core ontology spec**, saves the fixed
capability in your **local private instance**, and the function returns to normal for long-term use. Your local
customization is yours alone, polluting no system kernel, affecting no later upgrade or cross-platform port.

> If it involves system kernel-level issues (runtime / engine-layer bug), the steward guides you to feedback to us; we
> also **welcome your timely feedback on inconveniences found in use** for continuous improvement in later versions.

This "user describes problem → steward privately fixes → saves local → function back to normal" mechanism lets the system,
despite its size and inevitable occasional shortcomings, still resolve them in-place in your actual experience — also the
dividend of our deliberate strict separation of "spec" and "instance."

## 8. Relation to tier-one vendors: same spectrum, not a copy

We belong to the same spectrum as **Palantir Ontology** (semantic + kinetic + dynamic-layer digital-twin OS) and
**Zhongshu Ruizhi AI-FDE** (China's Palantir auto-delivery) — all solving the fundamental problem of "turning an
enterprise into a runnable digital twin."

Our route difference: **enter with "portable ontology spec + light runtime,"** zero-cost delivery via the WorkBuddy
kernel first, while reserving edge-cloud-sync and fully-on-prem exits. This lets us avoid tier-one vendors' heavy
bottom-layer investment, yet with the same spec reach the full spectrum from micro-company to strong-compliance clients.

> **Honest positioning**: in delivery scale and engineering rigor we are not yet at tier-one vendors; but on the vision
> of "letting an enterprise instantly own a runnable digital twin + AI field engineer," we are already on the same
> spectrum, extensible, and first to be out-of-the-box.
