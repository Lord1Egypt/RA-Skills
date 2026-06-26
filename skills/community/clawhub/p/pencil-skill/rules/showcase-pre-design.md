---
title: Pre-Design Planning
impact: HIGH
impactDescription: Designs started without clear goals and style guidance often require full rework later.
tags: showcase,planning,style-guide,workflow
---

## Pre-Design Planning

Before starting design, define goals, audience, and tone, collect references, and establish a style guide. Skipping this step often produces generic AI-style design or leads to full redesign after feedback like “the vibe is off.”

### Required pre-design checklist

#### 1️⃣ Define goals
- [ ] What is the design goal: landing, onboarding, dashboard, or marketing?
- [ ] What is the key user action (CTA)?
- [ ] Success metrics: conversion rate, time on page, sign-ups?

#### 2️⃣ Understand audience
- [ ] Who is the primary user persona?
- [ ] Technical level and device context (mobile/desktop ratio)?
- [ ] Language and cultural context?

#### 3️⃣ Tone & Brand
- [ ] Tone: professional, friendly, bold, calm, luxury?
- [ ] Are existing brand guidelines available?
- [ ] Did you collect at least 3 competitor/reference examples?

#### 4️⃣ Style guide draft
- [ ] Primary color finalized (not Tailwind defaults)
- [ ] Display + Body font pairing selected
- [ ] Spacing tokens defined on an 8pt grid
- [ ] Define responsive breakpoints (375/768/1440)

#### 5️⃣ Token registration
- [ ] Register color tokens with `set-variables` (including themes.mode)
- [ ] Register type-scale tokens
- [ ] Register spacing tokens
- [ ] Verify with `get-variables`

Start actual design work only after all checklist items pass.
