# Hazmat Disposal Router — Reference

## Scale of the problem
The average household stores 3-10 gallons of hazardous leftovers
(paints, solvents, pesticides, auto fluids). Most of it is discarded
wrong at least once: poured down drains, trashed wet, or mixed. The
downstream costs are huge and invisible: garbage truck fires from
lithium batteries (up sharply in most major cities — collection
agencies now run public campaigns), treatment-plant upsets from
solvents, groundwater contamination from oil (1 L ≈ 1M L water
contaminated), sanitation-worker needle injuries.

The routing knowledge is genuinely simple — 5 channels cover
everything — but it's not common knowledge, and cleanout days are
when mistakes concentrate.

## The five channels
1. **HHW facility** (municipal): everything chemical/flammable/
   toxic. Usually free for residents; often limited hours (weekly or
   monthly). This is the default for anything liquid-and-chemical.
2. **Retailer take-back**: auto parts (oil, batteries), electronics
   (WEEE in EU is a legal obligation on like-purchase), battery bins
   at supermarkets (EU), CFL bins at big-box entrances, paint
   retailers in PaintCare states.
3. **Trash (with preparation)**: dried latex paint, modern alkaline
   batteries (US), LEDs/incandescents, empty aerosols — the
   "preparation" step is the whole game (dry it, empty it).
4. **Pharmacy/sharps programs**: meds and needles — the two items
   where the wrong bin hurts specific workers.
5. **Professional/abatement**: asbestos-suspect, refrigerant
   (appliance with Freon), commercial quantities.

## Item deep-dives

### Paint
- **Latex/water-based**: dry to solid (cat litter, hardener, or air),
  then trash. Cans with liquid = refused by many haulers.
- **Oil-based**: always HHW. Pre-1980 paints may carry lead — never
  sand or scrape-dry indoors.
- **Still good?** Paint banks / PaintCare states / community reuse
  shelves take usable leftovers.

### Batteries — the fire problem
- **Li-ion (phones, tools, e-bikes, laptops)**: the compactor fire
  driver. Terminals taped, bagged individually, HHW or battery
  channel. Swollen packs: don't puncture, sand-free surface, facility
  notified in advance.
- **Lead-acid**: the most recycled product on earth (~99%); retailer
  cores + scrap pay. Keep upright.
- **Alkaline**: landfill-OK in the US since mercury removal (~1996);
  EU battery bins. Rechargeables never trash.
- **Button cells**: tape — they short against each other in jars.

### Auto fluids
- Motor oil: auto parts stores take it free and resell to re-refiners;
  use a clean sealed container, never a bleach jug (residue reacts).
- Coolant: toxic-sweet — animals lap spills; HHW.
- Gasoline: HHW in an approved can. Old gas (>1 yr) loses volatility
  but stays ignitable — don't "burn it off" in a mower; small-engine
  shops quote carb jobs for a reason.

### Mercury items
CFLs/tubes (vapor), old thermometers/thermostats (liquid). Intact →
HHW. Broken CFL: leave the room 10 min, then jar the fragments (never
vacuum), wipe with damp towel, seal and HHW. Never shop-vac mercury.

### Meds and sharps
Take-back is the safe channel everywhere. Flushing puts active
pharmaceuticals through treatment into surface water (measurable in
rivers for decades). Sharps: rigid, labeled container; loose needles
and soda bottles are the #1 sanitation injury source.

### Propane/aerosols
Pressurized = compactor hazard, always. Exchanges take grungy BBQ
tanks; HHW takes 1-lb cylinders (check locally — some areas have
special programs). Aerosols: fully empty → trash in most US areas;
anything that still sprays → HHW.

### E-waste
EU: retailer take-back on like-purchase is law. US: Best Buy/Staples
type programs + municipality e-days. Wipe drives first. CRT TVs are
the expensive item (leaded glass) — expect fees at some facilities.

## Storage until the run
The failure mode is the six-month limbo. Rules in `storage` output;
the critical ones: original containers, never mixed, lithium taped and
segregated, flammables away from ignition sources, plan the trip
within a month.

## Transport checklist
- Upright, sealed, nothing rolling loose
- Ventilated vehicle (windows cracked), no smoking
- Lithium away from solvents/gas, terminals taped
- Heavy batteries on the floor, not seats
- HHW hours checked BEFORE loading the car

## Local verification
Verdicts here are the consensus default across US EPA / EU Waste
Framework / UK EA guidance, but local programs differ (e.g., some US
cities say "no alkalines in trash, use battery bins"; some EU
municipalities collect chemicals door-side). The search pattern:
`<city/county> + item + disposal` on municipal sites.
