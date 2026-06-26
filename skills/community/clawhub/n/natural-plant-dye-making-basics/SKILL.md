---
name: natural-plant-dye-making-basics
description: >-
  Use when commercial dyes or colored fabric become unreliable, expensive, or unavailable and you need vibrant, light-fast, wash-fast natural dyes made from local foraged or garden plants for coloring yarn, clothing, rugs, or trade goods. Agent identifies safe local dye plants from your photos/GPS, calculates mordant ratios and extraction timelines, generates multi-day harvest/extract/fix schedules with timed reminders, tracks color-fastness tests, and produces inventory/barter templates. Human performs every physical step — harvesting, chopping, simmering, straining, and dyeing — rebuilding tactile self-reliance in plant-to-color conversion.
metadata:
  category: skills
  tagline: >-
    Turn backyard weeds and wild plants into rich, permanent dyes that color wool, cotton, and linen without synthetics — agent owns the chemistry and schedules so you stay in the simmering and stirring.
  display_name: "Natural Plant Dye Making Basics"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-31"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install natural-plant-dye-making-basics"
---
# Natural Plant Dye Making Basics

Turn common wild plants, garden scraps, and kitchen waste into rich, light-fast, wash-fast natural dyes for yarn, clothing, rugs, or high-value trade goods using only a pot, water, and your hands. No synthetic chemicals required — just foraged color and simple mordants. The agent owns all plant identification, mordant math, extraction formulas, and timeline tracking; you own the physical harvesting, chopping, simmering, and dyeing that turns everyday growth into lasting color.

`npx clawhub install natural-plant-dye-making-basics`

## When to Use

Deploy this skill when:
- Commercial fabric dyes or colored thread become expensive, scarce, or you refuse chemical dependence.
- You need custom colors for knitting, weaving, clothing repairs, or barter items that hold up to sun and washing.
- You have access to abundant dye plants (onion skins, black walnut, goldenrod, berries, leaves) and want a repeatable craft that produces zero-waste color.
- Existing textiles are fading and you want a renewable way to refresh or create new patterns.
- You want a repeatable micro-business or trade good (one well-dyed skein historically trades for hours of labor in many regions).

**Do not use** if you cannot safely identify plants or lack access to stainless steel or enamel pots. Agent will flag toxic or fugitive plants immediately.

## Agent Role vs. Human Role (Clear Division of Labor)

**Agent owns:**
- All plant-species identification and color-potential scoring from user photos/GPS.
- Mordant ratio calculations, pH adjustments, and extraction yield formulas.
- Automated harvest/extract/dye/fix schedules with photo checkpoints.
- Color-fastness test logging and escalation if dye fades.
- Barter templates, inventory cards, and “next-batch optimization” reports.
- Full safety protocol enforcement (boiling warnings, ventilation, glove reminders).

**Human owns:**
- All physical contact with plants: harvesting, chopping, simmering, straining, mordanting, and dyeing.
- Sensory judgment of color depth, simmer readiness, and final shade on fabric.
- Manual stirring and real-world wash/light tests.

## Step-by-Step Protocol (21-Day First Dye Batch Cycle)

### Phase 0: Plant Survey & ID (Agent-led, 1 day)
1. Agent asks for GPS or nearest town plus photos of candidate plants.
2. Agent cross-references safe high-yield dye species and issues a 5-question field checklist (color when crushed, abundance, season).
3. Agent outputs top 3 plants with exact harvest volume needed (≈2–3 kg fresh for one 100 g yarn batch) and mordant recipe.

### Phase 1: Harvesting & Prep (Human 1–2 hrs + Agent tracking, Day 1)
- Human gathers and chops plant material; agent provides exact part-to-use guidelines (flowers, leaves, bark, roots).
- Agent requests photo of prepared material and logs weight.

### Phase 2: Extraction (Agent reminders, Days 2–5)
- Agent calculates simmer time and water ratio (typically 1:2 plant-to-water by weight).
- Human simmers in stainless pot; agent issues timed stir prompts and color-check reminders every 30 minutes.
- Agent flags readiness and advances to mordant phase.

### Phase 3: Mordanting the Fiber (Human 60–90 min, Days 6–7)
Agent supplies three ready-to-use mordant options (alum, iron, copper — food-safe where possible).
Human pre-mordants yarn or fabric; agent times the soak and provides exact temperature windows.

### Phase 4: Dyeing & Shifting (Human 2–3 hrs total, Days 8–10)
- Human adds mordanted fiber to dye bath; agent issues timed simmer/stir schedule and pH adjustment prompts.
- Agent logs color development via photo and suggests modifiers (vinegar, soda ash) for shade shifts.

### Phase 5: Rinsing, Fixing & Drying (Agent reminders, Days 11–14)
- Human rinses and air-dries; agent sets 48–72 hour cure timer.
- Agent requests daily color photos and updates fastness log.

### Phase 6: Testing & Finishing (Days 15–21)
- Human performs wash test, light-fast test, and rub test; agent logs results.
- Agent generates “Next Batch Improvements” report.

## Decision Tree (Agent Runs This Automatically)

**Plant yields weak color?**
- Agent extends simmer time or switches to secondary species with stronger pigment.

**Dye fades after wash test?**
- Agent adjusts mordant strength or adds tannin fixative.

**Uneven color or spotting?**
- Agent triggers “even-stir protocol” or pre-wet fiber technique.

**All tests pass (no bleeding after 3 washes, minimal light fade)?**
- Agent auto-generates inventory card + barter template: “100 g hand-dyed wool yarn — goldenrod yellow, light-fast, trade value ≈ 1 skein per 500 g rice or 1 hr labor.”

## Ready-to-Use Templates & Scripts

**Plant Harvest Field Report (Human fills, Agent processes)**
```
Plant species (suspected): 
Location: [GPS or description]
Part harvested & weight: 
Color when crushed: 
Photos attached: yes
```

**Dye Batch Progress Log (Agent maintains)**
```
Day X — Batch Y
Simmer time achieved:
Color depth (photo): 
Fastness test result: 
Agent note: Next action in ___ hours
```

**Barter / Trade Script (Agent customizes)**
```
Subject: Hand-Dyed Natural Yarn — Plant-Based, Light-Fast, Ready to Trade

Made from local [plant] with traditional mordant method. Rich color that holds through washing and sun. Trade value ≈ 1 skein per 500 g rice, 200 g fiber, or 1 hr labor. Photos and test results attached.
```

**Progress Dashboard (Agent maintains in filesystem)**
- Total batches completed
- Average color fastness score
- Plant sources ranked by yield
- Next harvest window reminder

## Success Metrics (Agent Tracks)

**Minimum Viable Success (Week 3)**
- One 100 g yarn batch that passes 3-wash test and 2-week light test with no bleeding or significant fade
- Zero plant identification errors
- One dyed item used daily for 14 days with color intact

**Master Level (Month 3)**
- 5+ batches across multiple plants and mordants with <5 % failure rate
- Ability to produce custom shades from any local plant user supplies
- 500+ g of dyed goods in active rotation or traded
- Modifier and over-dye variants produced on demand

## Maintenance & Iteration

Agent runs a 30-day “Review & Scale” routine:
- Asks human for real-world performance feedback (color vibrancy, wash durability, light exposure).
- Generates next-batch optimizations (e.g., “Double alum for deeper walnut brown”).
- Archives successful plant-mordant pairs as reusable templates.
- Suggests advanced variants (eco-printing, bundle dyeing, natural inks) only after three successful basic batches.

## Rules / Safety Notes

- Work outdoors or under strong ventilation — some plants release strong vapors during simmering.
- Wear gloves and apron; many dyes stain skin and clothes permanently.
- Never use aluminum or reactive metal pots (agent specifies stainless or enamel only).
- Test every new plant with a small 10 g sample before full batch.
- Children only under direct adult supervision; no hot-pot handling.
- Dispose of spent dye baths responsibly (agent supplies composting or garden-use instructions).
- Stop immediately if you feel respiratory irritation or skin reaction — agent will pause and trigger full safety reset.

## Disclaimer

This skill encodes traditional natural plant dye techniques refined over centuries in cultures worldwide and cross-checked against historical textile references and modern natural-dyeing manuals. Results depend on plant freshness, mordant accuracy, and fiber type. Dyeing involves hot liquids and plant compounds that can cause staining, irritation, or allergic reactions if mishandled. No guarantees against color fade or material damage. Use at your own risk; improper technique carries burn, stain, and sensitivity hazards. Agent cannot physically harvest or simmer plants — all tactile, sensory, and safety decisions remain 100 % human. Consult local foraging regulations and perform a skin patch test with finished dyed items. Not a substitute for professional textile-dyeing or chemistry training.