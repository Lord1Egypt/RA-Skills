---
name: monolith-modularization
description: Deep workflow for evolving monoliths—mapping domains, defining module seams, strangler patterns, data ownership, incremental extraction, and testing/deployment safety. Use when reducing coupling before splitting services or improving maintainability.
---

# Monolith Modularization (Deep Workflow)

**Modularize** **before** **microservice** **splintering** **when** **possible**: **clear** **internal** **APIs** **and** **data** **boundaries** **lower** **risk** **than** **distributed** **rewrites**.

## When to Offer This Workflow

**Trigger conditions:**

- **Tangled** **code**; **long** **build/test** **times**; **fear** **of** **changes**
- **Preparing** **for** **extract** **services** **later**
- **Team** **parallelism** **blocked** **by** **merge** **conflicts**

**Initial offer:**

Use **six stages**: (1) map current state, (2) define target modules, (3) enforce boundaries, (4) migrate data & calls incrementally, (5) extract candidates, (6) validate & iterate. Confirm **language** **ecosystem** **(Java** **modules**, **packages**, **etc.)**.

---

## Stage 1: Map Current State

**Goal:** **Dependency** **graph** **and** **pain** **hotspots**.

### Activities

- **Categorize** **by** **domain** **(feature** **areas)**
- **Identify** **shared** **DB** **tables** **across** **features**
- **Build** **ownership** **per** **directory** **package**

**Exit condition:** **Simple** **diagram** **or** **list** **of** **coupling** **edges**.

---

## Stage 2: Define Target Modules

**Goal:** **Bounded** **contexts** **as** **packages** **or** **layers** **with** **explicit** **APIs**.

### Practices

- **Public** **API** **surface** **per** **module**; **internal** **packages** **hidden**
- **Dependency** **rule**: **feature** **→** **core** **allowed**; **not** **feature** **↔** **feature** **(eventually)**

**Exit condition:** **Rule** **document** **(lint** **or** **arch** **tests** **when** **possible)**.

---

## Stage 3: Enforce Boundaries

**Goal:** **Tooling** **backs** **intent** **(ArchUnit**, **dependency-cruiser**, **eslint** **boundaries)**.

### Practices

- **CI** **fails** **on** **new** **violations** **(ratchet)**
- **Gradual** **allowlist** **until** **legacy** **cleaned**

---

## Stage 4: Incremental Migration

**Goal:** **Strangler** **inside** **the** **monolith**: **new** **code** **behind** **facades**.

### Patterns

- **Extract** **interface** **+** **impl** **swap** **later**
- **Outbox** **table** **for** **events** **before** **Kafka** **exists**

**Exit condition:** **No** **big-bang** **rewrite** **without** **feature** **flags**.

---

## Stage 5: Extract Candidates

**Goal:** **Choose** **first** **service** **by** **clear** **data** **ownership** **and** **low** **coupling**.

### Heuristics

- **Stable** **API** **already** **emerged** **internally**
- **Different** **scaling** **needs** **or** **release** **cadence**

---

## Stage 6: Validate & Iterate

**Goal:** **Metrics**: **build** **time**, **test** **time**, **defect** **rate** **per** **module**.

### Practices

- **Retros** **on** **boundary** **pain**; **adjust** **modules**

---

## Final Review Checklist

- [ ] Domain map and coupling understood
- [ ] Target module boundaries and public APIs defined
- [ ] Enforcement (lint/tests) in CI where feasible
- [ ] Incremental migration path without big-bang
- [ ] Extraction candidates prioritized with rationale

## Tips for Effective Guidance

- **Shared** **DB** **rows** **are** **the** **hardest** **coupling**—**plan** **migrations** **early**.
- **“Anti-corruption”** **layer** **when** **integrating** **legacy** **subdomains**.
- **Modular** **monolith** **often** **beats** **premature** **microservices**.

## Handling Deviations

- **Rails** **/ Django** **/** **Spring**: **map** **to** **packaging** **and** **engines** **/** **modules** **specifically**.
- **Tiny** **codebase**: **folder** **structure** **+** **import** **rules** **only**.
