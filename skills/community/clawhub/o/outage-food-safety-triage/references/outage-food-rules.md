# Power-Outage Food Safety — Full Reference (FDA/USDA grounding)

## 1. The physics and biology of a closed fridge

A closed, unpowered refrigerator is an insulated box with a cold thermal
mass. Field-measured behavior (and the basis of the FDA/USDA consumer
guidance):

| Appliance | State | Safe runway (closed) |
|---|---|---|
| Refrigerator | any | **4 hours** before perishables enter the danger zone |
| Freezer | half full | **24 hours** |
| Freezer | full (frozen jugs filling gaps) | **48 hours** |

Every door opening costs roughly 30 minutes of that runway. The door
shelves warm first (they're outside the main insulated cavity); the back-
bottom shelves hold longest.

## 2. The danger zone

**40–140°F (4–60°C).** In this band, pathogenic bacteria (Salmonella, E.
coli O157:H7, Staph aureus, B. cereus, Listeria) double roughly every 20
minutes at warm-kitchen temperatures. Two distinct hazards:

1. **Vegetative cells** — killed by thorough cooking.
2. **Preformed toxins** (Staph aureus enterotoxin, B. cereus emetic toxin)
   — NOT destroyed by cooking OR refreezing. This is why "cook it to save
   it" only works for items that never spent meaningful time warm.

The 4-hour fridge window assumes ≤40°F the whole time. Without a
thermometer you're estimating from duration alone — which is why the
worst-case duration rule exists.

## 3. Category disposition table (what people get wrong)

### TOSS after 4h in the danger zone
- Deli/luncheon meats, cold cuts (listeria class — the classic post-outage
  ER visit)
- Leftovers, takeout, casseroles, cooked rice/pasta/stew/soup
- Raw meat/poultry/fish/seafood (2h window above 40°F, not 4)
- Milk, cream, yogurt, sour cream, kefir, soft cheeses (brie, ricotta,
  cottage), shredded cheese
- Cut fruit, **especially cut melon** (FDA-recognized listeria vector)
- Prepared infant formula, expressed breast milk, opened baby food
- Creamy/opened dairy-based salad dressings

### KEEP (survivors)
- Butter, margarine (fat-dominant, low water activity)
- Hard cheese blocks (parmesan, cheddar, swiss) — trim surface if mold
  appears later
- Commercial condiments: mayonnaise, ketchup, mustard, hot sauce, soy
  sauce (commercial mayo is pasteurized + acidic; the "mayo kills you"
  folk rule is wrong — the *deli meat under it* is the hazard)
- Vinegar pickles, jams/jellies, peanut butter
- Whole intact produce, bread/bakery, all pantry dry goods
- Uncracked eggs (then cook thoroughly)

### The famous mayonnaise case
Commercial mayonnaise is too acidic for pathogen growth. Home-made mayo
(raw eggs) is perishable and follows the 4h/toss rule. Most "the potato
salad poisoned the picnic" stories are actually Staph from handled
potatoes/ham, not the jar mayo.

## 4. Freezer triage and refreezing

Freezer food is safe if it still contains **ice crystals** or registers
≤40°F — ice is proof it never entered the danger zone.

| Observed state | Verdict |
|---|---|
| Hard-frozen, frozen core | Safe; refreeze or keep frozen |
| Partially thawed, ice crystals present | Refreeze-safe (quality drops) |
| Thawed, cold (≤40°F), no crystals | Cook immediately (veg/fruit) or toss (meat/fish) |
| Thawed, >40°F, or unknown | Toss — assume toxin window elapsed |
| Ice cream, frozen yogurt soft | Toss (never refreeze; texture + safety margins) |
| Stuffed poultry/fish, thawed | Toss always (dense core = slow cooling) |

Refreeze rules: only if ≤40°F throughout; refreezing slows but does not
stop quality loss; label and use first. "Thawed then frozen then thawed"
cycles accumulate both quality damage and risk.

## 5. The taste-test myth

Appearance, smell, and taste detect spoilage organisms — they detect
NOTHING about pathogen toxins. Staph enterotoxin is odorless and tasteless
at doses that cause violent illness. Tasting suspected food is the single
most common identified cause of post-outage food poisoning.

## 6. High-risk households — stricter cutoffs

Pregnant (listeria crosses the placenta), adults 65+, immunocompromised,
infants: apply a 2-hour rule instead of 4, and zero uncertainty tolerance:
if the duration is debated, the item is out.

## 7. Preparedness (making the next outage a 2-minute call)

1. Appliance thermometer *inside* the fridge (≤$5) — it converts
   "unknown" into data. Target ≤40°F.
2. Frozen water jugs filling freezer air gaps — thermal mass buys ~24h.
3. Door sign taped inside: start-time line + the 4/24/48 numbers + the
   toss-first/keep lists (the `doorsign` command prints it).
4. Coolers + frozen gel packs staged for >4h outages: pack perishables
   with ice, keep closed.
5. Know your utility's outage line; note the START time immediately.

## 8. Sources and scope

Encodes USDA FSIS "Keeping Food Safe During an Emergency" and FDA consumer
guidance, as commonly published (4h fridge / 24-48h freezer / 40°F danger-
zone thresholds). For commercial food service, HACCP plans and local
health codes govern — this is household guidance only.
