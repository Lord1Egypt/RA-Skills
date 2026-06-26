# Prompt Structuring for Stitch Operations

Use this reference when a request is underspecified, overly broad, or clearly likely to drift.

## Four-layer prompt model

Structure prompts using four layers:

### 1. Context

Define:

- product or screen type
- target user or workflow
- whether this is a new concept or a redesign of an existing screen

### 2. Structure

Specify:

- layout model
- major sections
- critical components that must exist
- the structural fingerprint: what makes this screen composition different from
  a default hero/card/template layout

### 3. Visual direction

State:

- style vocabulary
- density and spacing
- color direction
- typography intent

### 4. Constraints

Always make explicit:

- device
- what must remain unchanged
- whether the task is a full screen, a component, or a revision
- what content must not be invented, such as metrics, testimonials, logos,
  prices, case-study claims, or social proof

## Core rules

### Prefer plain language

Write short, direct instructions. Stitch responds better to concrete constraints than to abstract creative language.

### Structure before style

Choose the screen structure before asking for color, font, motion, or polish.
If the prompt only says "modern", "clean", or "premium", expect a generic
screen. Name the layout logic instead:

- index-first
- stat-led
- workbench
- catalogue
- dense dashboard
- document-like long page
- editorial split
- task-first mobile surface

Use the structure that fits the product job. Do not default to a centered hero,
three cards, and a CTA unless that is genuinely the right shape.

### One screen, one major intent

A prompt should do one of these, not several:

- generate a new screen
- edit one existing screen
- explore visual alternatives for one screen

Do not mix multiple screens, large content rewrites, and global design-system changes in the same instruction.

### Honest content

Prompts should not ask Stitch to fabricate credibility. If proof is unknown,
say so.

Use:

```text
Do not invent metrics, logos, testimonials, prices, customer counts, or case-study claims.
Use neutral placeholders only where proof is required.
```

For product UI, prefer a structure that works without social proof.

### Preserve explicitly

For redesign work, define invariants. Do not assume unchanged elements will remain unchanged.

Template:

```text
<screen>. <device>.
Keep <required elements>.
Improve only <layout / spacing / hierarchy / polish>.
Do not remove <critical elements>.
```

Example:

```text
Goal selection screen. Mobile.
Keep the BMI indicator, the three calorie preview values, the goal choices, and the primary CTA.
Improve only spacing, typography hierarchy, and visual polish.
Do not remove any of these elements.
```

### Component isolation

If the user wants a component rather than a full screen, explicitly prevent full-app generation.

Template:

```text
Design a single standalone UI component.
Do not generate a full application screen.
Show it isolated on a neutral background.
Make sure all text is fully visible.
```

### Avoid fake chrome

Do not ask for decorative browser bars, phone shells, IDE frames, traffic-light
dots, or fake code-window title bars unless that chrome is the actual product
being evaluated. Ask for real product UI, plain figures, or no chrome.

## Prompt repair patterns

### Weak to strong

Weak:

```text
A dashboard
```

Stronger:

```text
Analytics dashboard. Desktop.
Use a left sidebar, four KPI cards, a central area chart, and a compact activity feed.
Keep the layout information-dense but readable.
Use a restrained dark palette with teal accents.
Do not invent customer logos or growth metrics.
```

### Redesign without drift

```text
Today screen. Mobile.
Keep the meal sections, calorie summary, progress ring, and primary add-entry action.
Improve only spacing, visual hierarchy, and compactness.
Do not add new sections or remove existing ones.
Avoid generic app chrome that is not in the existing product.
```

### Small edit prompt

```text
Keep the existing layout and design language.
Make the primary CTA darker, reduce card padding slightly, and increase section-title contrast.
Do not change copy or remove components.
```
