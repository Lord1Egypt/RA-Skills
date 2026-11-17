# Architecture

Companion to `SKILL.md`. Read this when explaining the design or extending the
scaffold beyond what the template ships.

## Purpose

A reusable commerce operating system for digital products, creator storefronts
and multi-product studios. Optimised for **short-prompt generation and fast
deployment**, with an honest line between what is scaffolded and what is a
placeholder.

## Single source of truth

`SKILL.md` owns every rule. Everything else is downstream:

```
SKILL.md  --> templates/base   (the compliant reference implementation)
          --> scripts/         (scaffold + quality gate that enforce the rules)
          --> references/      (why-it-is-like-this, read on demand)
```

If a rule and an artifact disagree, the rule wins and the artifact is a bug.
Every gate in `SKILL.md` section 1 maps to a check in
`scripts/validate_generated_project.py` — change both together or they drift.

## Layers

### 1. Presentation — React + Vite + TypeScript
Seven routes, shared layout (`Navbar`, `Footer`, global `CartDrawer`, global
`AIChatWidget`), light motion via `framer-motion`, Tailwind with a two-palette
theme.

### 2. Application — Zustand + react-router
Two persisted stores (cart, wishlist). Derived values (`total`, `itemCount`) are
computed, never stored. Navigation is always client-side.

### 3. Utility — `src/utils/format.ts`
`formatPrice()` and `FREE_SHIPPING_THRESHOLD`. This is the only place a currency
symbol may appear, which is what makes the money gate (G-03) possible.

### 4. API — Hono-style edge handlers + Node handler
`functions/api/{products,checkout,assistant}.ts` (edge) and
`functions/node/stripe-webhook.ts` (Node). All four are mock-first and carry a
header comment describing the replacement path.

### 5. Commerce — data + flows
Product records, cart state, checkout session, payment-mode switch, order
lifecycle hooks. See `commerce-flows.md`.

### 6. Deployment — EdgeOne Pages
Static `dist/` plus edge and Node functions, configured by environment variables.
See `deployment.md`.

## Deliberate constraints

- **No `src/lib/`.** Shared code lives in `src/utils/`; the old `src/lib/api.ts`
  is a forbidden leftover (gate F-04). One obvious place beats two competing ones.
- **No extra dependencies.** The stack is fixed so generated projects build
  identically everywhere and reviews stay fast.
- **Images ship with the template.** The 16-image pool under `static/images/`
  makes output deterministic and offline-safe; remote images are the exception,
  not the default.
- **The template is a working store, not a placeholder shell.** It ships a real
  catalog, real categories and real copy in zh-CN. That makes "copy the template"
  a *safe* strategy for an agent — which is the failure mode this skill exists to
  remove.

## What this skill does not do

- It does not implement a real payment backend, authentication, inventory or
  order persistence. It names the entry points and documents what to connect.
- It does not pretend placeholders are production logic; handoff notes state the
  difference explicitly.
