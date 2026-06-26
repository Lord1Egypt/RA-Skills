---
name: osmotic-pressure
version: 1.0.0
description: >
  Detects and maps complexity imbalances across system boundaries. When one
  side of an interface absorbs all the complexity while the other stays
  artificially simple, the pressure builds until something ruptures. Like
  osmosis in biology, complexity flows toward concentration — this skill
  tells you where the pressure is building and what will burst first.
author: J. DeVere Cooley
category: architecture-health
tags:
  - complexity
  - architecture
  - balance
  - pressure-analysis
metadata:
  openclaw:
    emoji: "💧"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - cognitive
      - architecture
---

# Osmotic Pressure

> "In biology, osmotic pressure drives water from low-concentration regions to high-concentration regions through a semipermeable membrane. In software, complexity follows the same law — it flows toward where it's already concentrated, until the membrane tears."

## What It Does

Every system has boundaries: between frontend and backend, between services, between modules, between your code and the framework. At each boundary, complexity must live *somewhere*. The question is: where does it accumulate, and when does the accumulation become unsustainable?

Osmotic Pressure maps the **complexity gradient** across every boundary in your system. It finds the places where one side has absorbed a disproportionate share of the system's complexity — making it fragile, hard to test, and expensive to change — while the other side coasts on artificial simplicity that exists only because the hard work was pushed across the membrane.

## The Biology of Complexity

| Biological Concept | Software Equivalent |
|---|---|
| **Cell** | Module, service, or component |
| **Cell Membrane** | API, interface, or boundary |
| **Solute** | Complexity (logic, state, error handling, edge cases) |
| **Osmotic Pressure** | The force driving complexity to accumulate on one side |
| **Lysis** (cell bursting) | Module becomes unmaintainable, must be rewritten |
| **Crenation** (cell shriveling) | Module becomes trivially thin, serves no purpose |
| **Isotonic** | Complexity balanced appropriately across boundary |

## The Five Pressure Patterns

### 1. The God Module (Hypertonic)
One module has absorbed the complexity of its entire neighborhood. Everything is "simple" because everything delegates to it.

```
┌──────────────────┐     ┌──────┐
│   API Gateway     │────▶│ Auth │  simple
│   1,847 lines     │     └──────┘
│   43 functions    │     ┌──────┐
│   12 dependencies │────▶│ Log  │  simple
│   89% of bugs     │     └──────┘
│                   │     ┌──────┐
│   ALL THE         │────▶│ DB   │  simple
│   COMPLEXITY      │     └──────┘
└──────────────────┘
          ▲
    osmotic pressure is here
```

**Symptom:** Every bug ticket, every new feature, every refactor touches the same module. Other modules are "clean" because they're empty of responsibility.

**Pressure indicator:** Module size × dependency count × bug frequency. When this exceeds neighbors by > 3x, pressure is critical.

### 2. The Distributed Monolith (Isotonic Failure)
Complexity is "evenly distributed" — but only because every module reimplements the same logic. The membrane between them allows no sharing, so each cell independently evolved the same complexity.

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Service A │  │ Service B │  │ Service C │
│ validates │  │ validates │  │ validates │
│ formats   │  │ formats   │  │ formats   │
│ retries   │  │ retries   │  │ retries   │
│ caches    │  │ caches    │  │ caches    │
└──────────┘  └──────────┘  └──────────┘
  identical     identical     identical
  complexity    complexity    complexity
```

**Symptom:** Total system complexity is 3-5x what it should be. Fixing a bug means fixing it in N places. "We have microservices" but each service is a mini-monolith.

**Pressure indicator:** Code similarity > 60% across modules that should be independent.

### 3. The Thin Facade (Hypotonic)
A module's public interface is beautifully simple. Its internals are a nightmare. The complexity was pushed inward rather than addressed — a clean API hiding a disaster.

```
Public Interface:          Implementation:
┌─────────────────┐       ┌─────────────────────────────┐
│ createUser()    │──────▶│ 17 conditional branches      │
│ getUser()       │       │ 4 retry loops                │
│ deleteUser()    │       │ 8 implicit state transitions  │
│                 │       │ 3 undocumented side effects   │
│ Clean. Simple.  │       │ 2 race conditions             │
│ 3 functions.    │       │ 1 prayer                      │
└─────────────────┘       └─────────────────────────────┘
```

**Symptom:** The module is easy to use and impossible to maintain. New developers can call it on day one. No developer can modify it after a year.

**Pressure indicator:** Public surface area vs. internal cyclomatic complexity. Ratios > 1:10 indicate excessive inward pressure.

### 4. The Complexity Cascade (Pressure Chain)
Complexity flows downhill through a chain of modules. Each layer pushes its hard problems to the next, until the bottom module bears the accumulated weight of every decision above it.

```
Frontend   →  "Let the API handle that"
API Layer  →  "Let the service handle that"
Service    →  "Let the database handle that"
Database   →  [Complex stored procedures, triggers, views, materialized
               aggregations doing what should be application logic]
```

**Symptom:** The bottom of the stack is fragile and critical. Changing the database schema requires understanding the entire application. The database is doing business logic.

**Pressure indicator:** Complexity increases monotonically down the call stack. The ratio of bottom-layer complexity to top-layer complexity exceeds 5:1.

### 5. The Boundary Void (Zero Pressure)
Two modules interact but have no defined boundary. Complexity flows freely in both directions. There's no membrane at all — just a zone of chaos where one module bleeds into the other.

```
┌─────────────────────────────────────┐
│  Module A ... ??? ... Module B      │
│  imports from B, B imports from A   │
│  shared state, shared types         │
│  no clear interface                 │
│  no clear ownership                 │
│  entropy: maximum                   │
└─────────────────────────────────────┘
```

**Symptom:** Nobody knows where A ends and B begins. Pull requests touch both "modules." Tests can't be scoped to one side.

**Pressure indicator:** Circular dependencies + shared mutable state + zero interface definition.

## Measurement Framework

### Complexity Metrics Per Module

| Metric | What It Measures |
|---|---|
| **Lines of Logic** | Executable lines, excluding declarations and imports |
| **Cyclomatic Complexity** | Branching paths through the module |
| **State Surface** | Number of mutable state variables managed |
| **Error Handling Density** | Ratio of error/edge-case code to happy-path code |
| **Dependency Weight** | Number and depth of dependencies consumed |
| **Export Surface** | Number of things exposed to consumers |
| **Change Frequency** | How often this module changes (git analysis) |
| **Bug Density** | Bugs-per-line (from commit message analysis) |

### Pressure Calculation

```
For each boundary between module A and module B:

  Complexity(A) = weighted sum of all metrics for A
  Complexity(B) = weighted sum of all metrics for B

  Pressure = |Complexity(A) - Complexity(B)| / max(Complexity(A), Complexity(B))

  0.0 - 0.2  →  Isotonic (healthy balance)
  0.2 - 0.4  →  Mild pressure (monitor)
  0.4 - 0.6  →  Moderate pressure (rebalance recommended)
  0.6 - 0.8  →  High pressure (rebalance needed)
  0.8 - 1.0  →  Critical (lysis imminent)
```

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║                 OSMOTIC PRESSURE ANALYSIS                   ║
║            System Equilibrium Score: 0.58 (Stressed)        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  PRESSURE MAP:                                               ║
║                                                              ║
║  Frontend ──[0.31]──▶ API ──[0.72]──▶ Service ──[0.44]──▶ DB║
║  (low)                      (HIGH)              (moderate)   ║
║                                                              ║
║  CRITICAL IMBALANCE:                                         ║
║  ┌──────────────────────────────────────────────┐            ║
║  │  API Layer → Service Layer                    │            ║
║  │  Pressure: 0.72 (High — approaching lysis)    │            ║
║  │  Pattern: God Module (Service layer)          │            ║
║  │                                                │            ║
║  │  API Layer:    142 LOL, CC 8, 3 state vars    │            ║
║  │  Service Layer: 2,847 LOL, CC 67, 28 state    │            ║
║  │                                                │            ║
║  │  Diagnosis: API is a thin pass-through.        │            ║
║  │  Service absorbed ALL business logic, ALL      │            ║
║  │  error handling, ALL state management.          │            ║
║  │                                                │            ║
║  │  Recommendation: Extract validation,            │            ║
║  │  transformation, and error policy to API layer. │            ║
║  │  Target pressure: < 0.40                        │            ║
║  └──────────────────────────────────────────────┘            ║
║                                                              ║
║  PATTERN SUMMARY:                                            ║
║  ├── God Modules: 1 (ServiceLayer)                           ║
║  ├── Thin Facades: 2 (APIGateway, AuthModule)                ║
║  ├── Complexity Cascades: 1 (Frontend → DB)                  ║
║  ├── Distributed Duplication: 0                              ║
║  └── Boundary Voids: 0                                       ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- During architecture design (set healthy pressure budgets before building)
- After rapid feature development (complexity accumulates under speed pressure)
- When one module seems to attract all the bugs
- When a "simple" module is impossible to test
- Before a rewrite (understand where the pressure is before redistributing)

## Why It Matters

Complexity is conserved. You can't eliminate it — only distribute it. The question isn't "how do we reduce complexity?" but "where should complexity live, and is it living there?"

Systems don't fail because they're complex. They fail because the complexity is **concentrated** where it shouldn't be — behind thin facades, inside god modules, at the bottom of cascading chains. Osmotic Pressure makes the invisible distribution visible.

Zero external dependencies. Zero API calls. Pure complexity analysis.
