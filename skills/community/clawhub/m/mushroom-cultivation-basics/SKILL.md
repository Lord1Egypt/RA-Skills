---
name: mushroom-cultivation-basics
description: >-
  Use when you need reliable, low-space, waste-based food production for nutrition security, supplemental income, or embodied self-reliance in post-AI gig-economy instability. Agent personalizes species and method by your exact space, climate, budget, and goals; generates scaled recipes, automated calendars with reminders, supplier research, contamination decision trees, yield forecasts, and filesystem logs. Human performs all physical substrate prep, sterile inoculation, daily environmental adjustments, and harvesting — the hands-on craft only a human can feel and perfect.
metadata:
  category: skills
  tagline: >-
    Turn coffee grounds, straw, and sawdust into pounds of gourmet and medicinal mushrooms in a closet — agent runs the planning, tracking, and iteration; you own the living craft of cultivation
  display_name: "Mushroom Cultivation Basics"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-30"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install mushroom-cultivation-basics"
---
# Mushroom Cultivation Basics

This skill delivers a complete, professional-grade, phased system to grow oyster, lion’s mane, or shiitake mushrooms at home using free or cheap waste substrates. Expect first harvest in 4–8 weeks and continuous production thereafter. Startup cost under $80 for a setup that yields 5–15 lbs per month once rolling. Agent handles all research, personalization, scheduling, logging, and troubleshooting logic. You handle the physical inoculation, monitoring, and harvest — the embodied, sensory craft that rebuilds human connection to living systems in an unstable world.

`npx clawhub install mushroom-cultivation-basics`

```agent-adaptation
# Agent Localization and Personalization Rules
- Begin every session by collecting: exact location (for local suppliers, climate zone, and legal spore status), available dedicated space (closet shelf, basement corner, apartment balcony), weekly time budget, primary goal (food, medicinal, sale, learning), and any allergies or dietary needs.
- Use tools to research current local spawn suppliers, substrate sources, and any cultivation/sale regulations.
- Generate custom timelines, scaled recipes, shopping lists, and filesystem-based progress logs.
- Adjust all temperatures, humidity, and lighting for local conditions (e.g., add heating mat instructions for cold climates).
- Prioritize beginner-friendly, legal, non-psilocybin species only.
- Maintain state across conversations via filesystem logs for multi-batch continuity.
```

## Sources & Verification

Protocols are drawn directly from:
- Paul Stamets, *Growing Gourmet and Medicinal Mushrooms* (2005) — species-specific fruiting parameters and contamination biology.
- Stamets & Chilton, *The Mushroom Cultivator* (1983) — sterile technique, substrate formulas, and yield mathematics.
- Penn State University Extension mycology guides and Cornell University Small Farms Program — peer-reviewed beginner and commercial small-scale methods.
- University of Georgia Cooperative Extension and North Carolina State mycology resources — pasteurization science and waste-substrate efficacy studies.
- FreshCap Mushrooms and North Spore commercial cultivation manuals — modern home-scale adaptations with contamination rate data (<5 % success benchmark for experienced growers).

All techniques have been cross-verified against peer-reviewed mycology literature and commercial spawn producer field data as of 2026.

## When to Use

- Grocery supply chains feel fragile and you want 5–15 lbs of fresh mushrooms per month from a 4 sq ft footprint.
- You have access to free waste substrates (coffee grounds from local cafés, straw from farms, hardwood sawdust from cabinet shops).
- You want a high-return, low-land embodied skill that produces both food and potential side income at farmers’ markets.
- You seek the meditative, sensory satisfaction of watching living mycelium colonize and fruit — a direct counter to screen-based existence.
- You are already running basic gardening or livestock and want to stack a zero-land protein source.
- You want to explore lion’s mane or oyster for nutritional density (high in beta-glucans, B vitamins, and protein) while the agent tracks everything.

**Do not use** if you cannot maintain basic hygiene or have no 65–80 °F space for incubation.

## Agent Role vs Human Role

**Agent Handles (all bureaucracy and logic):**
- Intake interview and species/method recommendation.
- Real-time research on suppliers, current prices, and local regulations.
- Creation and maintenance of a 12-week rolling cultivation calendar with automated reminders.
- Scaled recipe generation and shopping-list drafting.
- Daily/weekly check-in prompts and filesystem logging of colonization %, contamination events, yields, and notes.
- Decision-tree execution for troubleshooting (user describes symptoms or uploads photo description).
- Drafting of supplier emails, market-listing templates, or recipe ideas post-harvest.
- Long-term iteration: yield analysis, cost-per-pound calculation, next-batch optimization.

**Human Handles (all physical and sensory work):**
- Collecting and preparing substrates (mixing, pasteurizing, packing).
- Performing sterile inoculation in still-air box or glovebox.
- Daily visual, smell, and tactile monitoring of jars/bags/blocks.
- Adjusting humidity, fresh-air exchange, and light by hand (misting, fanning, moving blocks).
- Harvesting at peak ripeness by feel and sight.
- Sensory evaluation and emotional connection to the living process.

## Step-by-Step Protocol

### Phase 0: Planning & Intake (Day 1)
Agent runs full intake. Recommends:
- Oyster mushrooms (Pleurotus ostreatus or citrinopileatus) for fastest 3–6 week cycle and highest forgiveness on waste substrates.
- Lion’s mane (Hericium erinaceus) if medicinal focus and slightly slower 6–10 week cycle.
- Shiitake (Lentinula edodes) if flavor preference and access to hardwood.

Agent outputs:
- Feasibility checklist.
- 12-week master calendar in markdown table format saved to filesystem.

### Phase 1: Materials Acquisition (Days 1–3)
Agent generates exact shopping list scaled to your target (start with 10 lb total substrate for first batch).

**Starter shopping list (≈ $60–80):**
- 2–4 lb grain spawn or liquid culture syringe of chosen species (North Spore, Field & Forest, or local).
- Substrate base: 10 lb spent coffee grounds OR chopped wheat straw OR hardwood sawdust.
- 10–20 wide-mouth quart jars or 5 lb grow bags with 0.2 μm filter patches.
- Vermiculite (4 qt) and gypsum (1 lb) for PF Tek or supplementation.
- 70 % isopropyl alcohol, nitrile gloves, lighter for needle sterilization.
- Spray bottle, digital hygrometer/thermometer, small fan.
- Still-air box materials (clear storage tote + gloves) if not already owned.
- Pressure cooker (if doing full sterilization) or large stockpot for pasteurization.

**Human action:** Order spawn, collect free coffee grounds (visit 3 cafés with printed “free grounds for mushroom growing” note drafted by agent), source straw/sawdust.

### Phase 2: Substrate Preparation & Inoculation (Days 4–7)

**Method A — Coffee-Ground Oyster Buckets (easiest, zero equipment)**
1. Collect 5 lb spent coffee grounds (moisture like wrung-out sponge).
2. Mix 80 % grounds + 20 % vermiculite or gypsum.
3. Pasteurize: submerge in 160 °F water for 60 minutes or microwave in batches.
4. Cool to room temp in sanitized bucket.
5. Agent provides exact spawn-to-substrate ratio (1:5 by weight).
6. Human: In still-air box, layer spawn and substrate in 5-gal bucket with lid drilled for air exchange. Seal and label.

**Method B — PF Tek Jars (most sterile for beginners)**
1. Mix 2 parts vermiculite : 1 part brown rice flour : 1 part water by volume.
2. Fill half-pint jars ½ full, add dry vermiculite top layer.
3. Pressure cook 45 min at 15 psi or steam 90 min.
4. Cool overnight.
5. In still-air box, flame-sterilize syringe needle, inject 1–2 cc liquid culture or 1 tsp grain spawn per jar.

Agent provides printable jar labels and exact timing.

**Human action:** Complete inoculation. Wipe all surfaces with alcohol. Place in dark incubation area 70–78 °F.

### Phase 3: Incubation & Colonization (Weeks 2–5)
- Maintain 70–78 °F, dark, no direct airflow.
- Agent sets daily “check-in” reminders: user reports % colonization (visual estimate) and any odors/colors.
- Full colonization = white mycelium covering 100 % substrate, no green/black/red.

**Decision Tree for Incubation (agent runs live):**
- White fluffy mycelium, caramel smell → perfect; proceed to fruiting.
- Green mold (Trichoderma) → isolate immediately, discard outside, increase sterility next batch (agent logs cause and adjusts protocol).
- Wet, sour smell, no growth → bacterial contamination; discard, lower moisture next batch.
- No growth after 14 days → temp too low/high or spawn dead; agent orders replacement and adjusts schedule.

### Phase 4: Fruiting (Weeks 5–8 and ongoing)
Move colonized blocks to fruiting chamber:
- 65–75 °F (drop 5–10 °F from incubation for most species).
- 85–95 % humidity (mist 2–3× daily).
- Fresh air exchange 4–6× daily (fan 30 seconds or open chamber).
- 12 hours indirect light / 12 hours dark (window or 6500 K LED).

Oysters pin in 3–7 days; harvest when caps flatten but before spores drop. Lion’s mane when teeth reach ½ inch. Shiitake when caps fully open.

**Human action:** Mist, fan, harvest by twisting base cleanly. Multiple flushes (3–5 for oysters) by re-soaking blocks 24 hours after each harvest.

Agent updates calendar with next flush dates and yield logging.

### Phase 5: Harvest, Preservation & Continuous Production (Week 8+)
- Harvest at peak: oysters when edges curl up slightly; lion’s mane when spines elongate.
- Clean with soft brush; store fresh in paper bag in fridge up to 7 days.
- Agent suggests preservation: dehydrate at 110 °F for 8 hours (store in vacuum-sealed jars 1+ year) or sauté and freeze.
- Log exact fresh and dry weight per flush in filesystem.
- Immediately start next batch for continuous supply (stagger inoculations every 3 weeks).

## Decision Trees / If-Then Branches

**Contamination Decision Tree (agent executes):**
- Green/blue mold → discard entire block outside; sterilize chamber; increase alcohol use 2× next batch.
- Cobweb mold (thin gray) → increase fresh air; isolate block.
- Bacterial wet spot (yellow slime) → lower moisture 10 % next batch.
- No pins after 14 days fruiting conditions → check humidity (too low), FAE (too low), or light (too dark).

**Yield Troubleshooting:**
- <0.5 lb per 5 lb block → substrate too dry or spawn rate too low; agent recalculates.
- Flushes stop after 2 → soak longer or supplement with new spawn.

## Ready-to-Use Templates & Scripts

**Supplier Inquiry Email (agent customizes with your location):**
```
Subject: Inquiry — [Species] Grain Spawn Availability for Small Home Grower

Hi,

I’m starting a small home mushroom project in [City, State] and am looking for 2–4 lb of [oyster/lion’s mane] grain spawn. Do you ship to my area? Price for 2 lb? Any current availability?

Thank you,
[Your Name]
```

**Market Sales Listing Template (for side income):**
```
Fresh [Oyster/Lion’s Mane] Mushrooms – Locally Grown on Coffee Grounds
$12/lb or $10/lb for 2+ lb
Pickup [your neighborhood] or local farmers market booth.
```

**Progress Log Template (agent maintains in filesystem):**
```
Batch ID | Start Date | Species | Substrate | Inoculation Date | Colonization % (Day 14/21) | Fruiting Start | Harvest 1 Weight | Total Yield | Notes
```

## Success Metrics

- First harvest within 8 weeks of inoculation.
- Consistent 0.75–1.5 lb fresh mushrooms per 5 lb substrate block across 3+ flushes.
- Contamination rate <10 % after third batch.
- Monthly production ≥5 lb with <4 sq ft space.
- User reports measurable increase in self-reliance and satisfaction from the living craft (logged in final check-in).

## Maintenance / Iteration

- After 3 successful batches, agent prompts agar-plate work (clone best fruits for strain improvement).
- Rotate species every 4 months to prevent adaptation issues.
- Annual review: agent calculates true cost-per-pound and suggests scaling (more blocks or small commercial kit sales).
- Save 10 % of best colonized substrate as future spawn.
- Compost spent blocks in garden or outdoor pile.

## Rules / Safety Notes

- Never eat any mushroom unless 100 % certain of identification and freshness. Start only with purchased gourmet spawn.
- Maintain strict sterility: 70 % alcohol on all surfaces, flame needle, work in still-air box.
- Mold exposure can cause respiratory irritation; wear mask if sensitive.
- Lion’s mane has emerging cognitive research but is not medical advice — consult physician for any therapeutic use.
- Check local laws: spore sales legal in most US states but cultivation/sale may have restrictions.
- Keep children and pets away from fruiting chamber during active growth.
- Dispose of contaminated material in sealed bags in regular trash — never compost near grow area.

## Disclaimer

This protocol is for informational and educational purposes only. Success depends on your execution, local conditions, and adherence to sterility. HowToUseHumans, contributors, and referenced sources are not liable for crop failure, financial loss, allergic reactions, legal issues, or any other consequence. Always verify local regulations and consult professionals for commercial activity or medicinal use. Eat only mushrooms you have grown from verified gourmet spawn.