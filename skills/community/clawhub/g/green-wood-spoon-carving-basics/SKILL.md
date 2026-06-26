---
name: green-wood-spoon-carving-basics
description: >-
  Use when you need custom, food-safe, long-lasting wooden spoons, spatulas, or small utensils made from local green hardwood for daily cooking, eating, or trade goods and commercial options are unreliable or unavailable. Agent identifies suitable local wood species from your photos/GPS, calculates green-to-dry shrinkage and carving timelines, generates ready-to-trace templates and progress checklists, tracks batch drying and oiling reminders, and produces inventory/barter templates. Human performs every physical step — selection, roughing, carving, finishing, and testing — rebuilding knife fluency and tactile self-reliance in green woodworking.
metadata:
  category: skills
  tagline: >-
    Turn fresh-cut branches into heirloom-quality spoons and utensils that last decades — agent owns the species math and schedules so you stay in the knife work and grain reading.
  display_name: "Green Wood Spoon Carving Basics"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-31"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install green-wood-spoon-carving-basics"
---
# Green Wood Spoon Carving Basics

Turn fresh-cut green hardwood branches into beautiful, functional, food-safe spoons, spatulas, and small utensils using only a straight knife and hook knife. No power tools, no drying kiln, no prior experience required — just a sharp edge and your hands. The agent owns all wood-species verification, shrinkage math, template generation, and timeline tracking; you own the physical carving, grain reading, and finishing that turns backyard branches into tradable daily-use tools.

`npx clawhub install green-wood-spoon-carving-basics`

## When to Use

Deploy this skill when:
- Commercial wooden or plastic utensils become expensive, scarce, or you refuse single-use plastic dependence.
- You have access to fresh hardwood branches (maple, birch, cherry, walnut) and want a repeatable micro-craft that produces heirloom items.
- You need custom sizes for specific kitchen tasks or high-value barter goods (one well-carved spoon can trade for hours of labor in many regions).
- Existing kitchen tools are wearing out and you want a renewable, repairable source that improves with use.
- You want to build knife skills and embodied focus in a short, satisfying project cycle.

**Do not use** if you lack a sharp carving knife or cannot work outdoors (sap and chips). Agent will flag unsuitable wood species immediately.

## Agent Role vs. Human Role (Clear Division of Labor)

**Agent owns:**
- All wood-species identification and suitability scoring from user photos/GPS.
- Shrinkage calculations, carving-order templates, and multi-day drying/oiling schedules.
- Automated reminders, photo-request checkpoints, and quality checklists.
- Barter templates, inventory trackers, and escalation if wood cracks during drying.
- Full safety protocol enforcement (knife-sharpening reminders, ergonomic breaks).

**Human owns:**
- All physical contact with wood: branch selection, rough shaping, bowl carving, handle refining, sanding, and oiling.
- Sensory judgment of grain direction, moisture feel, and final surface smoothness.
- Manual testing of balance and food-safe use.

## Step-by-Step Protocol (14-Day First Spoon Cycle)

### Phase 0: Wood Survey & Selection (Agent-led, 1 day)
1. Agent asks for GPS/nearest town plus photos of available branches.
2. Agent cross-references safe green-wood species and issues a 4-question field checklist (straight grain, no knots, 5–8 cm diameter).
3. Agent outputs top 3 species with exact branch length needed (≈30 cm for one spoon) and ranks by ease for beginners.

### Phase 1: Harvest & Rough Shaping (Human 45 min + Agent tracking, Day 1)
- Human cuts fresh branches; agent provides exact cut angles and “no-crack” splitting protocol.
- Human splits and roughs the blank with axe or saw; agent requests photo of blank and logs initial dimensions.

### Phase 2: Green Carving (Human 2–3 hrs total, Days 2–4)
Agent supplies three ready-to-trace templates:
- Beginner teaspoon (small bowl, short handle)
- Everyday tablespoon (deeper bowl, ergonomic handle)
- Spatula or serving spoon (wide blade)

Human carves using stop-cut and scoop techniques. Agent issues 20-minute timed work sessions with built-in 5-minute “rest-and-assess” prompts and grain-direction reminders. Agent logs depth and wall thickness via photo uploads.

### Phase 3: Initial Drying (Agent reminders, Days 5–9)
- Agent calculates local humidity-adjusted drying schedule (typically 5–7 days to stable).
- Human monitors for cracks; agent requests daily weight photos and updates shrinkage log automatically.
- Agent flags any warping and supplies corrective clamping technique.

### Phase 4: Final Carving & Sanding (Human 60–90 min, Days 10–11)
- Human refines details and sands progressively (80–400 grit); agent provides exact grit sequence and “no-fuzz” photo checkpoints.
- Agent logs final dimensions and weight.

### Phase 5: Oiling & Curing (Agent reminders, Days 12–14)
- Agent supplies food-safe oil recipe (boiled linseed, walnut, or mineral oil) and application schedule (3 coats over 48 hrs).
- Human applies oil; agent sets 48-hour cure timer and requests final photos.
- Agent generates “Next Spoon Improvements” report (e.g., “Deepen bowl 2 mm on next batch”).

## Decision Tree (Agent Runs This Automatically)

**Wood species unsuitable or cracks during roughing?**
- Agent immediately switches to secondary species or supplies “soak-and-re-split” protocol.

**Cracks appear during drying >5 %?**
- Agent triggers “slow-dry environment audit” and recommends sealing end-grain or slower schedule.

**Bowl too thin or handle unbalanced?**
- Agent provides corrective recarving steps or template adjustment for next blank.

**Spoon passes balance test and 24-hour water test?**
- Agent auto-generates inventory card + barter template: “Hand-carved green-wood tablespoon — cherry, food-safe, trade value ≈ 1 spoon per 500 g honey or 45 min labor.”

## Ready-to-Use Templates & Scripts

**Wood Selection Field Report (Human fills, Agent processes)**
```
Species (suspected): 
Location: [GPS or description]
Diameter & length: 
Grain notes: 
Photos attached: yes
```

**Daily Drying Log (Agent maintains)**
```
Day X — Spoon Y
Weight: g
Cracks observed: 
Ambient humidity %: 
Agent recommendation for next 24 h:
```

**Barter / Trade Script (Agent customizes)**
```
Subject: Hand-Carved Green-Wood Spoon — Cherry/Maple, Food-Safe

Carved from fresh local hardwood using traditional green-wood techniques. Finished with food-grade oil. Perfect daily use or gift. Trade value ≈ 1 spoon per 500 g rice, honey, or 45 min labor. Photos and test results attached.
```

**Progress Dashboard (Agent maintains in filesystem)**
- Total spoons completed
- Success rate by species
- Wood sources ranked by workability
- Next carving batch reminder

## Success Metrics (Agent Tracks)

**Minimum Viable Success (Week 2)**
- 3 completed spoons, all crack-free and passing 24-hour water test
- Zero major grain tear-outs
- One spoon used daily for 14 days with no warping or off-flavors

**Master Level (Month 3)**
- 20+ spoons across multiple species with <5 % failure rate
- Ability to carve any shape from memory or custom request
- Custom handle designs or engraved variants on demand
- 50+ spoons in active rotation or traded

## Maintenance & Iteration

Agent runs a 30-day “Review & Scale” routine:
- Asks human for real-world use feedback (balance, cleaning ease, flavor transfer).
- Generates next-batch optimizations (e.g., “Switch to walnut for darker grain”).
- Archives successful templates as reusable files.
- Suggests advanced variants (ladles, butter knives, small bowls) only after three successful basic spoons.

## Rules / Safety Notes

- Always carve with the grain; stop immediately if you feel resistance or hear cracking.
- Keep both hands behind the blade at all times; use thumb-stop or chest-lever techniques.
- Sharpen knife every 30 minutes of carving (agent issues timed reminders).
- Work outdoors or in well-ventilated area; wear cut-resistant gloves until confident.
- Children only under direct adult supervision; no carving participation until age 12+ with training.
- Dispose of chips responsibly (compost or fire starter).
- Stop immediately if you feel wrist strain — agent will pause schedule and suggest 48-hr rest plus ergonomic review.

## Disclaimer

This skill encodes traditional green-wood carving techniques refined over centuries in Scandinavian, Appalachian, and bushcraft traditions and cross-checked against modern spoon-carving references. Results depend on wood species, moisture content, and knife control. Carving involves sharp tools that can cause serious cuts if mishandled. No guarantees against cracking or personal injury. Use at your own risk; improper knife technique carries laceration hazards. Agent cannot physically carve or hold wood — all tactile, sensory, and safety decisions remain 100 % human. Consult local regulations for harvesting branches and perform a patch test with finished spoons before food use. Not a substitute for professional woodworking or knife-safety training.