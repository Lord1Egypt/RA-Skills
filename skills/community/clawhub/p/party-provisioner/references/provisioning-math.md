# Party Provisioning Reference — The Math Behind the Tool

## 1. Why guest-hours, not headcount

Consumption is a *rate*. A guest at a 2-hour dinner drinks ~3 servings; the
same guest at a 6-hour wedding drinks ~7. Every professional rule
(Tot Cookbook, catering guides, bartending schools) is expressed per
**guest-hour**, then adjusted:

```
servings = rate × guests × hours × adjustments
```

## 2. Alcohol baselines (industry standard)

| Setting | Rate |
|---|---|
| General evening party | 2 drinks first hour + 1/hour after |
| Wine-focused dinner | 1.5 glasses/hour |
| Champagne toast | +1 × 100ml pour per guest |
| Business function | −20% (daytime, professional) |
| Dancing / active | +10% |
| Hot weather (>27°C) | +20% — but shift toward beer/water |
| Beer-only crowd | ~2 beers first hour + 1/hr |

**Standard drink equivalence** (all ≈14g pure ethanol):
1 beer (355ml @5%) = 1 glass wine (150ml @12%) = 1 shot (44ml @40%).
This is why the tool tracks "drinks" as a single currency before splitting
by preference mix.

## 3. Bottle yields — where hosts get burned

| Container | Yield | Note |
|---|---|---|
| 750ml wine | **5 glasses** | 150ml catering pour; home pours run 6-7 → runs dry |
| 750ml spirits | **17 shots** | 44ml jigger; free-pour averages 25% more → 13 |
| 750ml champagne (toast) | **8 glasses** | 100ml toast pour |
| 750ml champagne (drinking) | 5 glasses | |
| Case of beer | 24 | 15-20% breakage/spill buffer for big events |
| 2L soda | 8-9 cups | over ice ~7 |
| Half-barrel keg | ~165 beers | equals ~7 cases |

**Free-pour drift** is the silent budget killer: untrained hosts pour
50-60ml "shots". With a jigger, one 750ml serves 17; without, 12. The tool
assumes jigger pours — buy +25% spirits if the party will free-pour.

## 4. Ice math

Ice needs scale with (a) drinks served on ice, (b) cooler/melt losses,
(c) weather.

- Bar service: ~1.5 lb per drinking guest for an evening (catering rule of
  thumb: 1 lb/person + chilling needs)
- Heat: +0.5 lb per drinker-hour over 27°C
- Chilling bottled drinks from room temp: salted ice bath halves the time;
  a 20lb bag chills ~24 beers in 30 min with water+salt
- Bagged: US 20lb / EU 10-12kg typical

## 5. Food rules (catering norms)

| Style | Rule |
|---|---|
| Sit-down dinner | 1.2 lb total food per adult (6-8oz protein + sides + dessert) |
| Cocktail/appetizers only | 12 bites per person per hour (no meal following) |
| Appetizers before a meal | 3-4 bites per person per hour |
| BBQ | ½ lb cooked protein per adult per meal + 1 lb sides total |
| Dessert | 1 serving per guest (cake cutting yields ~10% fewer than pan claims) |
| Kids | ½ adult portion |
| Big eaters / sports crowd | ×1.25 |

Protein shrinkage: buy raw weight ÷ 0.75 for cooked (25% loss). A "½ lb
protein" target means ~⅔ lb raw per adult.

## 6. Beverage mix estimation

If you don't know the crowd:
- Default US mixed crowd: 40/40/20 beer/wine/spirits
- Dinner party: 20/60/20
- Backyard BBQ: 50/30/20
- Wedding reception: 30/50/20 (+ toast)
- Young crowd: 40/20/40
Adjust after the first event — note what's left over; hosts systematically
over-buy wine and under-buy mixers and non-alc.

## 7. Non-alcoholic — the #1 failure

Non-drinkers (30% of a typical mixed invite list) consume **2
servings/hour**. Drinkers add ~0.5 water/hr (more in heat). Running out of
water/soda mid-party is more common than running out of beer, and in heat
it's a safety problem. Rule: **non-alc servings ≥ alcohol servings × 0.8**,
always visibly placed (a water station cuts alcohol consumption ~30% —
cheaper than buying more beer).

## 8. Supplies quick table

| Item | Rule |
|---|---|
| Glasses/cups | 2 per guest (no glassware staff) or 1 + washing |
| Plates | 1.5 × guests (seconds/breakage) |
| Napkins | 3 × guests |
| Trash bags (13gal) | 1 per 10 guests |
| Toilet paper | 1 roll per 15 guests beyond household stock |
| Cooling | 1 cooler per 15 guests |

## 9. Timing checklist (host card)

- **T-1 day**: shop; freeze water bottles (drinkable ice); chill whites
- **T-4h**: beer/white wine into fridge; ice pickup scheduled
- **T-1h**: bar set, garnishes cut, water station out, trash cans placed
- **T0**: open with already-chilled drinks only
- **60% mark**: inventory check — the tripwire rule (any category <25% left
  → deploy backup)
- **Plan the end**: last call 30 min before the official end; switch to
  water/coffee; this is both hosting skill and liability management.

## 10. Responsible-hosting notes

Serve food with alcohol, keep water visible, stop serving before the end,
arrange rideshare info. Most jurisdictions hold hosts partially liable for
guests' DUIs (social host liability). The math in this tool optimizes
*provisioning*, never over-serving.
