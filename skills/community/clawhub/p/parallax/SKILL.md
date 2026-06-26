---
name: parallax
version: 1.0.0
description: >
  Views every decision from five simultaneous stakeholder perspectives —
  the user who touches it, the developer who maintains it, the operator
  who deploys it, the attacker who probes it, and the business that funds it.
  Reveals the blind spots that single-perspective thinking guarantees.
author: J. DeVere Cooley
category: decision-intelligence
tags:
  - multi-perspective
  - decision-making
  - architecture
  - stakeholder-analysis
metadata:
  openclaw:
    emoji: "🔭"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - cognitive
      - architecture
---

# Parallax

> "In astronomy, parallax is the apparent shift of an object when viewed from two different positions. The shift reveals depth. Without it, the universe is flat."

## What It Does

Parallax forces every significant decision through **five simultaneous perspectives** before a single line of code is written. Not as a checklist. Not as an afterthought. As the *primary mode of reasoning*.

Most architectural mistakes aren't wrong from every angle. They're wrong from the angle nobody was standing at.

## The Five Parallax Lenses

| Lens | Persona | Core Question | Failure Mode When Ignored |
|---|---|---|---|
| **User** | The person touching the interface | "Does this feel right?" | Feature nobody uses despite being technically sound |
| **Maintainer** | The developer reading this code in 6 months | "Can I understand and change this?" | Code that works but can't evolve |
| **Operator** | The engineer deploying and monitoring this | "Can I run this at 3am when it breaks?" | System that works in dev, nightmare in prod |
| **Adversary** | The attacker probing for weaknesses | "Where does this trust too much?" | Vulnerability hiding in a convenient assumption |
| **Sponsor** | The business funding this work | "Does this create or capture value?" | Technical excellence that generates zero revenue |

## How Each Lens Works

### Lens 1: The User

The User lens doesn't ask "is the UX good?" — it asks **"what story does this interface tell?"**

```
ANALYSIS AXES:
├── Cognitive Load: How many things must the user hold in mind?
├── Error Recovery: When (not if) they make a mistake, what happens?
├── Trust Signal: Does this interaction build or erode confidence?
├── Time Respect: Does this value the user's time or waste it?
└── Accessibility: Can someone with different abilities use this equally?
```

**What it catches:** Features that are powerful but unusable. Flows that make sense to the developer but confuse the user. Efficiency optimizations that sacrifice clarity.

### Lens 2: The Maintainer

The Maintainer lens asks **"what will confuse the next person who reads this?"**

```
ANALYSIS AXES:
├── Naming Clarity: Do names describe actual behavior?
├── Abstraction Depth: How many layers deep must you go to understand?
├── Change Locality: To change this behavior, how many files do you touch?
├── Test Confidence: If I modify this, will the tests tell me if I broke something?
└── Knowledge Required: What unwritten context is needed to work here?
```

**What it catches:** Clever code that requires tribal knowledge. Abstractions that obscure rather than clarify. Designs that are optimal for writing but hostile to reading.

### Lens 3: The Operator

The Operator lens asks **"what happens when this fails at 3am on a holiday weekend?"**

```
ANALYSIS AXES:
├── Observability: Can I see what's happening without reading source code?
├── Failure Modes: Does it fail loudly, quietly, or in a way that looks like success?
├── Recovery Path: Can I fix it without a deploy?
├── Blast Radius: If this fails, what else fails?
└── Resource Behavior: Does it degrade gracefully or cliff-edge?
```

**What it catches:** Systems with no logging. Failures that cascade silently. Recovery paths that require the original developer. Memory leaks that only manifest under production load.

### Lens 4: The Adversary

The Adversary lens asks **"where does this assume good faith?"**

```
ANALYSIS AXES:
├── Trust Boundaries: Where does external input enter?
├── Assumption Surface: What would break if I lied to this system?
├── Privilege Scope: Does this have more access than it needs?
├── Information Leakage: What does the error message reveal?
└── Timing Attacks: Can I learn secrets from how long things take?
```

**What it catches:** Input that's validated for format but not intent. Error messages that reveal internal architecture. APIs that trust client-side state. Rate limits that don't exist.

### Lens 5: The Sponsor

The Sponsor lens asks **"does this advance the mission or just feel productive?"**

```
ANALYSIS AXES:
├── Value Delivery: Does this solve a problem someone will pay for?
├── Opportunity Cost: What are we NOT building while we build this?
├── Time to Value: How long until this generates measurable impact?
├── Reversibility: If this is wrong, how expensive is the course correction?
└── Leverage: Does this multiply future capability or just add linearly?
```

**What it catches:** Over-engineered solutions to low-value problems. Refactors that improve code quality but delay features. Infrastructure investments with unclear ROI.

## The Parallax Process

```
INPUT: A proposed change, feature, or architectural decision

STEP 1: SINGLE-PERSPECTIVE PASS
├── Generate the default analysis (whatever perspective comes naturally)
└── Document: which lens did you instinctively use?

STEP 2: FULL PARALLAX
├── Run the remaining four lenses
├── For each lens, generate:
│   ├── Top concern from this perspective
│   ├── Blind spot this lens reveals
│   └── Modification this perspective demands
└── Flag conflicts between lenses

STEP 3: TRIANGULATION
├── Identify where 3+ lenses agree (high confidence)
├── Identify where lenses conflict (design tension)
├── For each conflict:
│   ├── Which lens has priority given the current project phase?
│   ├── Can the tension be resolved or must it be managed?
│   └── What's the least-bad tradeoff?
└── Produce final recommendation with explicit tradeoff map

OUTPUT: Decision with full perspective coverage and documented tradeoffs
```

## Conflict Resolution Matrix

When lenses disagree, priority depends on project phase:

| Phase | Primary Lens | Secondary | Rationale |
|---|---|---|---|
| **Prototype** | Sponsor → User | Maintainer | Validate value before investing in quality |
| **MVP** | User → Sponsor | Adversary | Ship something real, don't ship something dangerous |
| **Growth** | Operator → Adversary | Maintainer | Scale without breaking or being broken into |
| **Maturity** | Maintainer → Operator | User | Long-term sustainability over short-term features |
| **Turnaround** | Sponsor → User | Operator | Re-find product-market fit, fast |

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║                    PARALLAX ANALYSIS                        ║
║         Decision: "Add caching layer to user API"           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  👤 USER:       Faster responses (+). Stale data risk (-).   ║
║                 → Ensure cache invalidation is immediate     ║
║                   for profile changes.                       ║
║                                                              ║
║  🔧 MAINTAINER: New complexity layer (-). Clear boundary (+) ║
║                 → Cache must be a swappable interface,       ║
║                   not hardcoded to Redis.                    ║
║                                                              ║
║  📟 OPERATOR:   Reduces DB load (+). New failure point (-).  ║
║                 → Need cache hit/miss metrics and            ║
║                   graceful fallback to direct DB.            ║
║                                                              ║
║  🗡️ ADVERSARY:  Cache poisoning vector (-). Rate limit       ║
║                 bypass via cache (-).                        ║
║                 → Cache keys must not be user-controllable.  ║
║                                                              ║
║  💼 SPONSOR:    Reduces infra cost (+). Delays feature X (-) ║
║                 → Worth it only if current p95 latency is    ║
║                   actually causing churn.                    ║
║                                                              ║
║  CONFLICTS:                                                  ║
║  ├── User (freshness) vs Operator (DB load) → TTL tradeoff  ║
║  └── Sponsor (cost) vs Maintainer (complexity) → Phase check ║
║                                                              ║
║  RECOMMENDATION: Proceed with 60s TTL, swappable interface,  ║
║  cache metrics dashboard, and cache-poisoning guards.        ║
║  Defer if p95 latency is under 200ms.                        ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- Before any architectural decision that will be expensive to reverse
- During design reviews and RFC discussions
- When a decision "feels right" but you can't articulate why (you're stuck in one lens)
- When stakeholders disagree (they're each looking through a different lens)
- Before adding any new dependency, service, or abstraction layer

## Why It Matters

The #1 cause of architectural regret isn't choosing the wrong solution. It's choosing a solution that's optimal from one perspective while being catastrophic from another perspective nobody considered.

Parallax doesn't make decisions for you. It makes sure you're making decisions with **depth perception**.

Zero external dependencies. Zero API calls. Pure multi-perspective reasoning.
