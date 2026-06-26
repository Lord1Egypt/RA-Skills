---
name: handbuilt-pottery-pit-firing-basics
description: >-
  Use when you need durable, repairable kitchenware, storage jars, tools, or ritual objects made from local clay without electricity, kilns, or commercial supply chains. Agent researches your local clay sources and soil types, generates customized project plans with material lists and firing schedules, tracks drying/firing logs via filesystem, sets automated reminders for each stage, and drafts troubleshooting decision trees; human performs all physical work — digging and processing clay, handbuilding, and pit firing.
metadata:
  category: skills
  tagline: >-
    Turn backyard dirt into leak-proof bowls, jars, and plates that last generations — agent handles research, planning, and tracking so you focus purely on the hands-on craft that builds real embodied self-reliance.
  display_name: "Handbuilt Pottery & Pit Firing Basics"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-31"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install handbuilt-pottery-pit-firing-basics"
---
# Handbuilt Pottery & Pit Firing Basics

Create functional, zero-waste pottery using only local clay, handbuilding techniques, and traditional pit firing — no wheels or electric kilns required. This protocol turns raw earth into waterproof bowls, storage jars, cups, and tools that survive real-world use in unstable times.

`npx clawhub install handbuilt-pottery-pit-firing-basics`

In a post-AI world where supply chains fracture and humans reclaim physical craft, handbuilt pottery with pit firing is one of the highest-leverage self-reliance skills: you produce your own tableware, food storage, and trade goods from the ground beneath your feet. The agent becomes your project architect and record-keeper; you stay in the clay, shaping and firing with your hands.

## When to Use This Skill
- Local clay is available (test with the 1-minute jar test the agent will run for you).
- You want to replace or supplement store-bought ceramics that break or become expensive.
- Grid-down or off-grid living requires non-electric food storage and cooking vessels.
- You need custom tools (seedling pots, oil lamps, ritual objects) that commercial markets do not sell.
- You are building long-term family or community resilience through tradable handmade goods.
- Existing plastic or metal items are failing and you want permanent, repairable replacements.

## Agent Role vs. Human Role
**Agent Handles (all bureaucracy and logic):**
- Runs local clay viability tests based on your GPS or soil description.
- Generates exact material lists, phased timelines, and safety checklists.
- Maintains a filesystem-based project log, inventory tracker, and firing schedule with automated reminders.
- Researches and adapts traditional pit-firing recipes to your climate and available burn materials (sawdust, manure, wood chips).
- Builds decision trees for troubleshooting cracks, leaks, or weak bisque.
- Drafts any local permit inquiries if scaling to a permanent outdoor pit.
- Calculates batch yields and cost-per-piece savings.

**Human Handles (all physical and embodied work):**
- Digs, cleans, and wedges the clay.
- Handbuilds every piece using pinch, coil, or slab methods.
- Constructs or prepares the pit and loads the ware.
- Tends the fire during the 6–12 hour firing cycle.
- Makes on-site tactile decisions about clay consistency and firing progress.

## Step-by-Step Protocol (4–6 Weeks per Batch)
### Phase 0: Site & Clay Assessment (Agent-Led, 1 Day)
Agent asks for: your location/climate zone, available outdoor space, preferred final pieces (bowls, jars, plates), and any existing burn materials.  
Agent runs the jar test protocol and tells you exactly how to process your local clay (how much grog to add, settling times).  
Decision tree output by agent:
- Clay too sandy? Add 20–30 % organic grog (crushed fired pottery or sand).
- Clay too sticky? Let it age 2 weeks in a sealed bucket.
- No local clay? Agent locates nearest public source or suggests mail-order raw clay as temporary bridge.

### Phase 1: Clay Preparation (Human Physical, 2–3 Days)
1. Dig 20–30 lb raw clay from identified deposit.
2. Follow agent’s exact dry-screen/wet-slake/wedge instructions (agent outputs step-by-step checklist with photos descriptions).
3. Wedge thoroughly until no air pockets remain — human senses the “leather-hard” readiness.
Agent logs clay batch ID and stores recipe for future repeats.

### Phase 2: Handbuilding (Human Physical, 3–7 Days)
Agent supplies three ready-to-use templates scaled to your needs:
- Pinch pot (small cup or bowl)
- Coil-built jar with lid
- Slab-built plate or shallow baking dish

Human builds 6–12 pieces per batch. Agent reminds you of wall thickness targets (¼–⅜ inch) and drying stages:
- Leather hard: 24–48 hours under damp cloth
- Bone dry: 3–5 days in shaded area

Agent generates drying log template and pings you daily until bone-dry.

### Phase 3: Pit Firing Preparation (Agent + Human, 1 Day)
Agent designs your pit:
- 2–3 ft diameter × 2 ft deep hole (or above-ground brick ring for urban).
- Material list: 50 lb sawdust or dry manure, 20 lb wood chips, sheet metal or old barrel lid for cover, wire for securing.

Human digs/prepares pit and places ware on a bed of sand and sawdust. Agent outputs exact loading diagram and burn-material layering sequence.

### Phase 4: The Firing (Human Physical, 8–12 Hours)
Agent provides timed checklist:
- 0–2 hrs: gentle smoke phase (low oxygen)
- 2–6 hrs: ramp to 800–1000 °C (visual cues: glowing orange, smoke color)
- 6–8 hrs: soak and cool slowly under cover

Human tends fire, rotates pieces if needed, and makes real-time tactile decisions (agent gives “if smoke turns black → add more air” rules).  
Agent logs temperature estimates from color and smoke and stores for next batch optimization.

### Phase 5: Unloading & Testing (Human + Agent, 1 Day)
Human unloads cooled ware. Agent generates:
- Water-tightness test protocol (fill and observe 24 hrs)
- Thermal shock test (boiling water pour)
- Repair protocol if hairline cracks appear (clay slip + refire)

## Ready-to-Use Templates & Scripts (Agent Maintains)
**Project Inventory Tracker** (filesystem Markdown table agent updates):
```
Batch ID | Piece Type | Quantity | Clay Source | Fired Date | Status | Notes
POT-2026-04-01 | Coil Jar | 4 | Backyard | 2026-04-15 | Tested watertight | Ready for glaze test
```

**Firing Log Template** (agent populates after each run):
- Start time, ambient temp, fuel used, visual milestones, total duration, yield %

**Safety & Materials Checklist** (agent exports to you before every phase)

**Email/Neighbor Trade Script** (agent customizes):
“Hi [Neighbor], I just pit-fired a fresh batch of handbuilt clay jars. Would you trade 2 jars for a bag of your applewood chips for next firing?”

## Decision Trees (Agent Runs Live)
**Crack During Drying?**
- Small hairline → score & fill with slip, re-dry slowly.
- Large → recycle into grog for next batch.

**Ware Not Watertight After Firing?**
- Agent calculates slip recipe and schedules micro-refire in smaller pit.

**Smoke Firing Color Not Dark Enough?**
- Agent adjusts manure/sawdust ratio for next batch.

## Success Metrics
- 75 % or more of fired pieces pass water-tightness and thermal-shock tests.
- Average cost per usable piece under $2 (tracked by agent).
- At least 3 new batches completed within 6 months.
- You can now produce custom replacements for any broken household ceramic.

## Maintenance / Iteration
Agent reviews your logs every 90 days and proposes:
- Clay body improvements (add grog percentages).
- New forms based on your usage data (e.g., taller jars if you store more grains).
- Seasonal timing adjustments for optimal drying weather.

## Rules / Safety Notes
- Always wear dust mask when dry-mixing clay and gloves when handling raw clay (bacteria risk).
- Pit firing is open-flame: maintain 10 ft clearance from structures, have water extinguisher ready, never leave unattended.
- Children and pets kept 20 ft away during firing.
- Test every new clay source for contaminants (agent guides simple home tests).
- Never fire in high wind or dry grass conditions.
- Food-safe rule: use only for dry storage or brief cooking unless you apply food-grade sealant (agent can research local options).

## Disclaimer
This skill provides professional-grade, evidence-based protocols drawn from traditional pit-firing methods (documented in archaeological records and texts such as *Primitive Pottery* techniques and John Seymour’s *The Self-Sufficient Life*) and modern adaptations. It is for educational and personal use only. Local fire regulations, soil testing for heavy metals, and food-safety guidelines vary by jurisdiction — verify compliance. The agent and skill authors assume no liability for injury, property damage, or food-borne illness. Start small, stay safe, and keep your hands in the clay.