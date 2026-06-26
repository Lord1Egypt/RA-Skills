---
name: plant-fiber-cordage-making-basics
description: >-
  Use when you need strong, biodegradable rope, cord, or twine for hauling, binding loads, building shelters, fishing lines, or trade goods and commercial rope is unreliable or unavailable. Agent identifies safe local plants from your photos, calculates fiber yield and breaking strength, generates retting/drying schedules with timed reminders, tracks twist ratios and quality tests, and produces inventory/barter templates. Human performs every physical step — harvesting, retting, drying, twisting, and testing — rebuilding tactile self-reliance in low-tech cordage production.
metadata:
  category: skills
  tagline: >-
    Turn backyard weeds and wild plants into 200+ kg test-strength rope that replaces store-bought cord — agent owns the botany and math so you stay in the harvesting and twisting.
  display_name: "Plant Fiber Cordage Making Basics"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-31"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install plant-fiber-cordage-making-basics"
---
# Plant Fiber Cordage Making Basics

Turn common wild plants and garden waste into strong, natural rope and cord that can haul 50+ kg loads, lash shelters, or serve as tradable goods. No machinery required — just your hands and a few sticks. The agent owns all plant identification, yield math, scheduling, and testing protocols; you own the physical harvesting, processing, and twisting that turns fiber into functional line.

`npx clawhub install plant-fiber-cordage-making-basics`

## When to Use

Deploy this skill when:
- Commercial rope, paracord, or twine becomes expensive, scarce, or you want zero-plastic alternatives.
- You need custom-length cord for emergency shelters, animal tethers, fishing nets, or barter.
- You have access to common fiber plants (nettle, dogbane, yucca, milkweed, flax) and refuse to stay dependent on supply chains.
- Existing cordage is degrading and you want a renewable, repairable source.
- You want a repeatable micro-business or trade good (one 30 m hank can trade for days of labor in many regions).

**Do not use** if you cannot safely identify plants or lack access to water for retting. Agent will flag toxic look-alikes immediately.

## Agent Role vs. Human Role (Clear Division of Labor)

**Agent owns:**
- All plant ID from user-submitted photos using established botanical references.
- Fiber-yield calculations, retting-time predictions, and twist-ratio formulas.
- Automated retting/drying calendars and strength-test logging.
- Barter templates, inventory trackers, and escalation if fiber breaks below 20 kg test load.
- Full safety protocol enforcement (gloves, skin-irritant warnings).

**Human owns:**
- All physical contact: harvesting, stripping, retting, drying, splicing, and twisting.
- Sensory judgment of fiber readiness (snap test, pliability).
- Manual twisting and final load testing.

## Step-by-Step Protocol (21-Day First Hank Cycle)

### Phase 0: Plant Survey & ID (Agent-led, 1 day)
1. Agent asks for GPS or nearest town + photos of candidate plants.
2. Agent cross-references against safe fiber species and issues a 5-question field ID checklist.
3. Agent outputs top 3 plants with exact harvest volume needed (≈2 kg green stalks for one 30 m hank).

### Phase 1: Harvesting (Human 1–2 hrs + Agent tracking, Day 1)
- Human cuts and bundles stalks; agent provides exact height and season guidelines.
- Agent requests photo of bundle and logs initial weight.

### Phase 2: Retting (Agent reminders, Days 2–10)
- Agent calculates water-retting or dew-retting schedule based on local temperature/humidity.
- Human submerges bundles in pond, stream, or bucket; agent issues daily “check for slip” reminders.
- Human performs snap test on Day 8–10; agent logs results and advances schedule.

### Phase 3: Drying & Stripping (Human 2 hrs, Days 11–12)
- Agent sets drying timeline (2–4 days to brittle).
- Human strips outer bark and extracts inner fibers; agent provides exact hand-stripping technique and photo checkpoints.

### Phase 4: Twisting (Human 3–4 hrs total, Days 13–18)
Agent supplies three ready-to-use templates:
- 2-ply twine (fishing line strength)
- 3-ply cord (25 kg test)
- 4-ply rope (50+ kg test)

Human twists using thigh-roll or spindle method. Agent issues timed 20-minute sessions with rest prompts and logs diameter/turns-per-meter.

### Phase 5: Testing & Finishing (Day 19–21)
- Human performs 10 kg, 25 kg, and 50 kg load tests; agent logs break points.
- Agent generates “Next Batch Improvements” report.
- Optional sealing: agent supplies pine-resin dip recipe for water resistance.

## Decision Tree (Agent Runs This Automatically)

**Plant ID uncertain or toxic look-alike flagged?**
- Agent halts and requests new photo or switches to known-safe garden plant (flax, hemp).

**Fiber fails snap test after retting?**
- Agent extends retting by 48 hrs or switches to dew-retting protocol.

**Cord breaks below target strength?**
- Agent adjusts twist ratio (+10 % turns) or adds splicing technique.

**All hanks pass 50 kg test with <5 % stretch?**
- Agent auto-generates inventory card + barter template: “30 m 4-ply plant-fiber rope — 50 kg test, biodegradable, trade value ≈ 2 kg rice or 2 hrs labor.”

## Ready-to-Use Templates & Scripts

**Plant Field Report (Human fills, Agent processes)**
```
Plant name (suspected): 
Location: [GPS or description]
Photo attached: yes
Stalk length/quantity: 
Skin irritation noted: 
Notes:
```

**Retting Log (Agent maintains)**
```
Day X — Bundle Y
Water temp: 
Appearance (slimy = ready?): 
Snap test result: 
Agent recommendation: Continue / Harvest fiber
```

**Barter / Trade Script (Agent customizes)**
```
Subject: Hand-Twisted Plant-Fiber Rope — 50 kg Test, 30 m Hanks

Made from local nettle/dogbane with 4-ply construction. Tested to 50+ kg, biodegradable. Trade value ≈ 1 hank per 2 kg rice or 2 hrs labor. Photos and test results attached.
```

**Progress Dashboard (Agent maintains in filesystem)**
- Total meters produced
- Average breaking strength
- Plant sources ranked by yield
- Next retting batch reminder

## Success Metrics (Agent Tracks)

**Minimum Viable Success (Week 3)**
- One 30 m 4-ply hank that holds 50 kg
- Zero skin reactions during processing
- One hank used daily for 14 days (lashing, hauling) with no degradation

**Master Level (Month 3)**
- 5+ hanks with <5 % failure rate
- Ability to produce custom diameters from any local fiber user supplies
- Spliced variants or net-making on demand
- 200+ meters in active rotation or traded

## Maintenance & Iteration

Agent runs a 30-day “Review & Scale” routine:
- Asks human for usage feedback and plant performance notes.
- Generates next-batch optimizations (e.g., “Add 15 % milkweed for extra flexibility”).
- Archives successful plant recipes as reusable templates.
- Suggests advanced variants (netting, bowstring cord) only after three successful basic hanks.

## Rules / Safety Notes

- Wear gloves during harvesting and retting — many fiber plants cause skin irritation.
- Never harvest from polluted water or chemically sprayed areas.
- Test every new plant batch with a 10 cm sample twist before full hank.
- Children only under direct adult supervision; no retting participation.
- Store finished cordage dry and away from rodents.
- Stop immediately if you develop rash or respiratory issues — agent will pause and trigger full safety reset.

## Disclaimer

This skill encodes traditional plant-fiber cordage techniques refined over millennia and cross-checked against ethnobotanical references and modern bushcraft protocols. Results depend on plant species, retting conditions, and twist consistency. No guarantees against breakage or skin irritation. Use at your own risk; improper plant ID carries toxicity hazards. Agent cannot physically harvest or twist — all tactile and sensory decisions remain 100 % human. Consult local foraging regulations and perform patch tests. Not a substitute for professional rope-engineering standards.