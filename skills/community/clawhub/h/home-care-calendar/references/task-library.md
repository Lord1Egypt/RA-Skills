# Task Library & Maintenance Intervals — Reference

Intervals below consolidate manufacturer guidance, HVAC industry standards
(EPA/DOE/ACCA), fire-safety recommendations (NFPA), and insurance-industry
practice. Adjust ±25% for climate and usage; the registry supports per-item
overrides via re-adding with a different interval is NOT needed — frequency
comes from the kind library, and `done` keeps the clock honest.

## HVAC & Heating

| Task | Interval | Why | Neglect trajectory |
|---|---|---|---|
| HVAC filter change (1" fiberglass) | 30–60 d | airflow → blower strain | energy +15%, then compressor wear |
| HVAC filter change (1" pleated) | 60–90 d | same, better loading capacity | same |
| HVAC filter (4–5" media) | 180–365 d | high-capacity media | same |
| Furnace pro service | 365 d | combustion + heat-exchanger check | efficiency loss → winter failure ($5k+) |
| Furnace visual check | 90 d | flame color, rust, short-cycling | catches pro-visit issues early |
| AC condenser coil clean | 365 d | heat exchange capacity | capacity loss → compressor death |
| AC drain line flush | 90 d | algae clog → overflow pan → ceiling | water damage |
| Chimney pro inspection | 730 d | creosote, liner cracks | chimney fire / CO |
| Boiler service | 365 d | same as furnace | same |

## Water

| Task | Interval | Why | Neglect trajectory |
|---|---|---|---|
| Water heater sediment flush | 365 d | sediment insulates tank | efficiency −, tank life − years, rumbling |
| TPR valve test | 365 d | safety valve must move | catastrophic failure risk (rare but total) |
| Water shutoff exercise | 365 d | valves seize closed | can't shut off in emergency |
| Sump pump bucket test | 90 d | pump failure found during flood | finished-basement flood ($10k+) |
| Softener salt check | 90 d | salt-out breaks softening | scale in everything |
| Exterior drains check | 180 d | storm readiness | yard/house flooding |
| Washer drain filter | 180 d | debris → pump death | pump replacement, leaks |
| Dishwasher filter | 90 d | pump strain, film | pump death, smells |

## Safety

| Task | Interval | Why |
|---|---|---|
| Smoke detector battery + test | 365 d (test monthly) | NFPA: dead batteries → no alarm |
| Smoke detector unit expiry | 365 d check | sensors expire at 10 yr |
| CO detector battery + expiry | 365 d | units last 5–10 yr |
| Dryer vent deep clean | 365 d | lint = leading fire cause |
| Range hood filter degrease | 180 d | grease fire load |
| GFCI outlet test | 180 d | button test; they fail with age |
| Fire extinguisher gauge | 180 d | pressure loss is silent |

## Envelope & Exterior

| Task | Interval | Why | Neglect trajectory |
|---|---|---|---|
| Gutter cleaning | 180 d (spring + after leaf-fall) | clog → fascia rot, foundation water, ice dams | rot spreads into roof edge ($k) |
| Roof visual (ground) | 365 d | lifted shingles, flashing | leak found at ceiling = late |
| Caulk/grout inspection | 180 d | sealant fails in 2–5 yr | hidden wall damage |
| Weatherstrip check | 365 d (fall) | drafts, energy | comfort + heating cost |
| Deck wash + seal | 365 d | water absorption → rot | board replacement, falls |
| Tree clearance prune | 730 d (late winter) | storm damage | roof damage in first storm |
| Refrigerator coils | 180 d | heat exchange | energy +, compressor life − |
| Refrigerator door seal | 365 d | leak = constant run | energy + |
| Faucet aerator descale | 365 d | flow, fixture scale | fixture replacement |
| Garage door lubrication | 365 d | track/roller wear | opener death, stuck door |

## Seasonal Anchor Strategy

Tie tasks to dates you already remember:

- **DST spring forward / fall back** — smoke/CO batteries + unit expiry check.
- **September/October** — furnace pro service (before heating season), gutter
  clean AFTER leaf-drop in your area, chimney inspection before first fire.
- **March/April** — AC pro service (before cooling season), exterior drains,
  sump test before thaw/rains.
- **Late winter** — tree pruning (bare branches show true clearance).
- **Whenever a filter looks gray at month 2** — your interval is too long for
  your dust load; change kind or just do it sooner.

## Neglect-Cost Model

Each task carries `neglect_cost_per_month` — an expected-value rough figure
combining probability of failure with typical repair cost, amortized. Examples:

- HVAC filter ($25/mo): +15% energy on a $150/mo bill plus compressor wear.
- Gutter neglect ($40/mo): fascia/soffit rot repairs $1–4k over years.
- Sump pump ($45/mo): finished-basement flood risk $10k+ at low annual prob.
- Dryer vent ($35/mo): fire expected-value (NFPA loss data).

These are prioritization numbers, not invoices. Their job is ranking — the
$1,800 water-heater flush debt outranks the $1.67 filter debt in the report,
and both are wrong to obsess over individually.

## Pro vs DIY

Most tasks here are DIY with a screwdriver and an hour. Book pros for: furnace
combustion service, AC refrigerant/coil work, chimney, tree work near
structures, and anything gas-line related. "BOOK A PRO" appears in calendar
output and ICS descriptions for these — the point of the tool is doing the
right tasks, not all tasks yourself.
