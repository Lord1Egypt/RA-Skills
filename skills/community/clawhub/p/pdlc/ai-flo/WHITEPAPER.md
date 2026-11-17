# AI-FLO — Whitepaper

**AI-Driven Flow Orchestrator**

**Version:** 1.0.0
**Author:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Date:** 2026-06-13

---

## The Problem

The AI-* Family has 10 packages across two layers. Each package knows its own job — but none of them knows where to go next. The handoff between packages is manual: the user finishes AI-PILC, then has to know that AI-ADLC comes next, manually point it at the PIP output, and hope they didn't skip a step.

Worse: packages in different layers can't talk to each other. AI-PPM (Portfolio layer) needs project health data from AI-GCE and AI-TGE (Project layer). Without a courier, that data doesn't flow. The portfolio manager either gets stale data or manually asks each project team for updates.

The chain exists in theory. In practice, without orchestration, it's a set of disconnected tools that the user must manually sequence.

---

## The Solution

AI-FLO is the router and orchestrator on the edge between layers. It does two things:
1. **Route** — detect what package just finished and determine what comes next
2. **Carry** — transport data across the layer boundary (Portfolio ↔ Project)

**Package-to-package flow, automated. Layer-to-layer data, delivered.**

AI-FLO doesn't DO work — it routes work. It reads marker files, makes routing decisions based on package output state, and either hands off to the next package or carries data across the layer boundary for portfolio-level consumption.

---

## How It Works

```
Marker File Detected → Identify Source Package → Apply Routing Rules → Determine Destination → Handoff / Carry
```

**Two primary functions:**

| Function | Direction | What Happens |
|----------|-----------|--------------|
| **Route** | Horizontal (same layer) | Detect completion marker → suggest or activate next package |
| **Carry Down** | Portfolio → Project | Dispatch authorizations from AI-PPM → activate Project-layer packages |
| **Carry Up** | Project → Portfolio | Roll-up payloads (health, progress, compliance) → deliver to AI-PPM |

### Routing Logic

AI-FLO uses marker files as its detection mechanism:

| Marker Found | Meaning | Default Next |
|-------------|---------|-------------|
| `pilc-state.md` (complete) | AI-PILC finished | Route to AI-ADLC or AI-PPM |
| `adlc-state.md` (complete) | AI-ADLC finished | Route to AI-DWG |
| `ilc-state.md` (approved) | AI-ILC approved an idea | Route to AI-PILC or fast-track to AI-ADLC |
| Dispatch authorization | AI-PPM authorized start | Route to specified Project-layer packages |

---

## Who It's For

| Role | Pain Point Solved |
|------|-------------------|
| **PMO Director** | Automated flow between lifecycle stages — no dropped handoffs between packages |
| **Portfolio Manager** | Cross-layer data delivery — project health arrives without chasing PMs |
| **Project Manager** | Clear "what's next" guidance after each package completes |
| **Platform Engineer** | Consistent routing conventions — marker-based detection, not path assumptions |
| **Anyone new to the family** | The router tells you where to go — no memorizing the chain sequence |

---

## Key Differentiators

### 1. Layer Boundary Enforcement

AI-FLO enforces the family's communication law: **cross-layer communication MUST go through FLO**. Portfolio packages never read Project-layer state files directly. Project packages never send data up to Portfolio directly. FLO is the boundary courier — keeping layers decoupled while enabling visibility.

### 2. Marker-Based Detection (Not Path-Based)

FLO detects package completion by marker file presence and state, not by file paths. This means packages can live anywhere — different repos, different folders, different machines. If the marker exists and its state says "complete," FLO knows what to route.

### 3. Graceful Degradation

FLO is optional. Without it:
- Same-layer routing still works (packages detect each other's markers directly)
- Cross-layer communication falls back to manual (user provides status updates)
- The chain still functions — just with manual handoffs instead of automated routing

### 4. Router, Not Controller

FLO doesn't own the flow. It suggests and facilitates. The user can override any routing decision. FLO can propose "AI-ADLC is next" — but the user might say "actually, I want to go straight to AI-DWG." FLO respects that.

---

## Position in AIFLC — the AI-* PDLC Family

AI-FLO sits on the **edge between layers** — the only package that spans both:
- Reads markers from **Portfolio layer** (AI-PPM dispatch authorizations)
- Reads markers from **Project layer** (completion states, health data)
- Carries data **down** (Portfolio → Project: authorizations)
- Carries data **up** (Project → Portfolio: roll-up payloads)
- Routes **horizontally** within each layer (suggesting next package)

It is not part of either layer — it IS the connection between them.

---

*AI-FLO — Because a chain without orchestration is just a list.*
