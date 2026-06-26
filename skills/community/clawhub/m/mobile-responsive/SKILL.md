---
name: mobile-responsive
description: Deep responsive design workflow—breakpoints, content priority, touch targets, typography, performance on mobile networks, and testing on real devices. Use when fixing mobile UX, defining responsive patterns, or auditing layouts across viewports.
---

# Mobile Responsive (Deep Workflow)

Responsive design is **not** “three fixed widths”—it is **fluid** **layouts**, **touch-first** **interaction**, **readable** **typography**, and **performance** **under** **real** **constraints**.

## When to Offer This Workflow

**Trigger conditions:**

- Layout **breaks** **on** **small** **screens**; **horizontal** **scroll**
- **Touch** **targets** **too** **small**; **hover-only** **patterns**
- **CLS** **or** **LCP** **issues** **on** **mobile**

**Initial offer:**

Use **six stages**: (1) viewport & breakpoints, (2) content priority, (3) layout & grids, (4) touch & gestures, (5) typography & readability, (6) performance & verification. Confirm **design** **system** **tokens** **if** **any**.

---

## Stage 1: Viewport & Breakpoints

**Goal:** **Breakpoint** **strategy** **matches** **content** **not** **only** **devices**.

### Practices

- **Content-first** **min-width** **media** **queries** **where** **possible**
- **Test** **real** **ranges** **(320–428+** **px** **common** **phones)**
- **Safe** **area** **insets** **for** **notch** **devices**

**Exit condition:** **Breakpoint** **table** **with** **what** **changes** **per** **tier**.

---

## Stage 2: Content Priority

**Goal:** **Mobile** **shows** **what** **matters** **first**—**not** **shrunk** **desktop**.

### Practices

- **Reorder** **stack** **for** **primary** **CTA** **above** **fold** **when** **appropriate**
- **Hide** **non-essential** **via** **progressive** **disclosure** **not** **`display:none`** **without** **a11y** **plan**

**Exit condition:** **Priority** **annotated** **wireframe** **for** **key** **templates**.

---

## Stage 3: Layout & Grids

**Goal:** **Fluid** **grid**; **no** **overflow** **surprises**.

### Practices

- **Max-width** **containers**; **images** **with** **dimensions** **or** **aspect** **ratio**
- **Flex** **/** **grid** **gap** **consistent**; **avoid** **fixed** **px** **widths** **for** **main** **columns**

---

## Stage 4: Touch & Gestures

**Goal:** **WCAG** **2.5** **target** **size** **(≥44×44** **px** **approx)** **and** **spacing**.

### Practices

- **No** **hover-only** **tooltips**; **tap** **to** **reveal**
- **Swipe** **only** **when** **discoverable** **or** **documented**

---

## Stage 5: Typography & Readability

**Goal:** **Min** **font** **size** **~16px** **body** **to** **prevent** **iOS** **zoom**; **line-height** **comfortable**.

### Practices

- **Contrast** **ratios** **for** **small** **text** **outdoors**

---

## Stage 6: Performance & Verification

**Goal:** **LCP** **images** **optimized**; **JS** **budget** **for** **mobile** **CPU**.

### Verification

- **Chrome** **device** **mode** **insufficient** **alone**—**real** **devices** **or** **BrowserStack**
- **RUM** **by** **device** **class**

---

## Final Review Checklist

- [ ] Breakpoints and content priority defined
- [ ] No critical horizontal scroll; images stable
- [ ] Touch targets and focus order work
- [ ] Typography readable; contrast OK
- [ ] Performance validated on mobile networks

## Tips for Effective Guidance

- **`100vw`** **often** **causes** **overflow** **with** **scrollbar**—**use** **`100%`** **or** **`min`** **carefully**.
- **Sticky** **headers** **and** **virtual** **keyboard** **interactions** **need** **test** **on** **device**.
- **Dark** **mode** **and** **contrast** **are** **part** **of** **responsive** **readability**.

## Handling Deviations

- **Native** **app** **vs** **web**: **same** **touch** **and** **priority** **principles**; **platform** **patterns** **differ**.
- **Desktop-only** **internal** **tool**: **still** **minimum** **1280** **and** **zoom** **to** **200%** **for** **a11y**.
