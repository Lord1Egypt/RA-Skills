---
name: nextjs-app-router
description: Deep Next.js App Router workflow—layouts, routing, Server vs Client Components, data fetching and caching, revalidation, streaming, and deployment (Node, serverless, edge). Use when building or debugging Next.js 13+ apps.
---

# Next.js App Router (Deep Workflow)

App Router **changes** **mental** **models**: **where** **code** **runs**, **what** **is** **cached**, **and** **how** **HTML** **streams**. **Defaults** **differ** **from** **Pages** **Router**—**call** **that** **out** **explicitly**.

## When to Offer This Workflow

**Trigger conditions:**

- **New** **App** **Router** **project** **or** **migration** **from** **pages/**
- **Confusion** **Server** **vs** **Client** **Components**; **hooks** **errors**
- **Stale** **data**, **wrong** **cache**, **need** **ISR** **semantics**

**Initial offer:**

Use **six stages**: (1) route & layout model, (2) Server vs Client boundaries, (3) data fetching & cache, (4) revalidation & tags, (5) streaming & UX, (6) deployment & runtime. Confirm **Next** **version** **and** **hosting** **(Vercel** **self**, **etc.)**.

---

## Stage 1: Route & Layout Model

**Goal:** **`app/`** **directory** **=** **nested** **layouts** **+** **col** **ocated** **routes**.

### Practices

- **`layout.tsx`** **for** **shared** **UI** **and** **providers** **(client** **where** **needed)**
- **`page.tsx`** **is** **leaf** **UI** **per** **segment**
- **`loading.tsx`**, **`error.tsx`**, **`not-found`** **for** **UX** **boundaries**

**Exit condition:** **URL** **tree** **matches** **folder** **tree** **mental** **model**.

---

## Stage 2: Server vs Client Components

**Goal:** **Default** **Server** **Components**; **`use client`** **only** **where** **interactivity** **needs** **browser** **APIs** **or** **state**.

### Rules of thumb

- **Data** **fetch** **on** **server** **by** **default** **(async** **components)**
- **Leaf** **interactive** **islands** **as** **client** **components**
- **Prop** **serialization**: **only** **JSON-serializable** **props** **across** **boundary**

**Exit condition:** **List** **of** **client** **components** **and** **why**.

---

## Stage 3: Data Fetching & Cache

**Goal:** `fetch` **cache** **semantics** **(force-cache** **vs** **no-store** **vs** **revalidate)** **explicit** **per** **call**.

### Practices

- **Align** **with** **auth**: **no-store** **or** **request** **memoization** **patterns** **for** **user-specific** **data**
- **Parallel** **fetch** **where** **possible** **to** **avoid** **waterfalls**

**Exit condition:** **Per-route** **data** **dependency** **graph** **(simple** **diagram)**.

---

## Stage 4: Revalidation & Tags

**Goal:** **Fresh** **when** **needed** **without** **DDOS** **origin**.

### Practices

- **`revalidatePath`** / **`revalidateTag`** **from** **server** **actions** **or** **route** **handlers**
- **Webhook-triggered** **revalidation** **for** **CMS**

**Exit condition:** **Invalidation** **owner** **and** **trigger** **documented**.

---

## Stage 5: Streaming & UX

**Goal:** **`Suspense`** **boundaries** **with** **meaningful** **fallbacks**; **a11y** **for** **loading**.

### Practices

- **Avoid** **waterfall** **inside** **suspense** **trees** **(sequential** **awaits)**

---

## Stage 6: Deployment & Runtime

**Goal:** **Node** **vs** **edge** **runtime** **per** **route** **segment** **when** **using** **edge**.

### Practices

- **Edge** **cannot** **use** **all** **Node** **APIs**—**verify** **compat**
- **ISR** **on** **serverless** **may** **need** **warming** **or** **cron** **revalidate**

---

## Final Review Checklist

- [ ] Layouts and route segments match product IA
- [ ] Server/Client split justified; props serializable
- [ ] Fetch cache and auth story correct per route
- [ ] Revalidation path defined for CMS/dynamic data
- [ ] Streaming/suspense without accidental waterfalls
- [ ] Runtime (edge vs node) matches dependencies

## Tips for Effective Guidance

- **Refer** **to** **current** **Next.js** **docs** **for** **default** **fetch** **caching** **—** **defaults** **changed** **across** **versions**.
- **Middleware** **for** **auth** **redirects** **—** **mind** **matcher** **performance**.
- **Colocation** **of** **tests** **and** **Storybook** **for** **client** **components** **helps** **isolation**.

## Handling Deviations

- **Pages** **Router** **legacy**: **map** **equivalents** **(getServerSideProps** **→** **async** **RSC)** **carefully**.
- **Turbopack** **/** **Webpack** **—** **different** **perf** **profiles** **in** **dev**.
