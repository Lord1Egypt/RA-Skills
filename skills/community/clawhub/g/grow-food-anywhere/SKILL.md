---
name: grow-food-anywhere
description: >-
  Practical food growing for complete beginners. Apartment balcony, backyard, or windowsill. What actually produces enough to matter, realistic timelines, and what to skip. Use when someone wants to grow food but has never done it.
metadata:
  category: skills
  tagline: >-
    Start growing real food this week. What works on a balcony, what works in a yard, and what's a waste of your time.
  display_name: "Grow Food Anywhere"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-18"
  openclaw:
    requires:
      tools: [calendar, filesystem]
    install: "npx clawhub install howtousehumans/grow-food-anywhere"
---

# Grow Food Anywhere

Most "grow your own food" content is aspirational nonsense from people with acres of land and years of experience. This is for desk workers who've never grown anything, live in apartments or small houses, and need to start producing real food with minimal investment. Focus: what actually yields enough to matter, what's a waste of time, and the 20% of effort that produces 80% of results.

## Sources & Verification

- **USDA Cooperative Extension System** — every county in the U.S. has a free extension office with locally adapted planting guides, pest management, and soil testing. Find yours at extension.org
- **Master Gardener Programs** (run through extension offices) — free hotlines and local clinics where trained volunteers answer gardening questions. Search "[your county] master gardener"
- **USDA Plant Hardiness Zone Map** — the standard reference for determining what grows in your climate. planthardiness.ars.usda.gov
- **"Square Foot Gardening" by Mel Bartholomew** — the most practical guide to high-yield small-space food production, especially relevant for raised beds and containers
- **"The Vegetable Gardener's Bible" by Edward C. Smith** — comprehensive reference on growing food in various climates and conditions, with realistic yield expectations

## When to Use

- User wants to grow food but has never gardened
- Lives in an apartment, small house, or has limited outdoor space
- Wants to reduce grocery bills with homegrown food
- Looking for practical starting point, not a lifestyle change
- Interested in food self-sufficiency as a hedge

## Instructions

### Step 1: Assess your space honestly

**Agent action**: Ask the user about their living situation and create a personalized growing plan. Save to `~/documents/food-growing/my-plan.md`.

Before buying anything, figure out what you actually have:

```
SPACE ASSESSMENT:

[] How many hours of direct sunlight? (hold your hand up — if you can
   see a sharp shadow, that's direct sun)
   -> 6+ hours: you can grow almost anything
   -> 4-6 hours: leafy greens, herbs, some root vegetables
   -> 2-4 hours: lettuce, spinach, herbs only
   -> Less than 2: don't grow food outdoors, consider sprouts/microgreens indoors

[] What space type?
   -> Sunny windowsill (2-4 sq ft): herbs and microgreens
   -> Balcony (15-50 sq ft): containers, serious production possible
   -> Patio/deck (50-200 sq ft): container garden, very productive
   -> Backyard (any size): in-ground beds or raised beds

[] Climate zone — search "[your zip/postal code] plant hardiness zone"
```

### Step 2: Start with what actually produces

Most beginners plant tomatoes and get disappointed. Here's what actually feeds you, ranked by calories and nutrition per square foot of effort:

```
BEST RETURN ON EFFORT (ranked):

TIER 1 — Start here, almost impossible to fail:
- Lettuce/salad greens: harvest in 30 days, regrows after cutting
- Green onions: buy from store, put roots in soil, infinite supply
- Herbs (basil, cilantro, parsley, mint): saves $3-8/week on groceries
- Radishes: ready in 25 days, grow anywhere

TIER 2 — High yield, slight learning curve:
- Zucchini/summer squash: ONE plant produces 20-40 lbs per season
- Bush beans: easy, prolific, fix nitrogen in soil
- Cherry tomatoes: way easier than large tomatoes
- Kale/chard: cut-and-come-again for months

TIER 3 — Worth it if you have ground space:
- Potatoes: grow in bags or ground, 10:1 return on what you plant
- Winter squash: one vine = 20+ lbs of storable food
- Garlic: plant in fall, harvest in summer, stores for months

SKIP THESE AS A BEGINNER:
- Corn (needs huge space for tiny yield)
- Large tomatoes (disease-prone, fussy)
- Carrots (slow, finicky germination)
- Anything "exotic" (save it for year 2)
```

### Step 3: Container setup (apartments/balconies)

```
MINIMUM CONTAINER SETUP — under $30:

- 3-5 five-gallon buckets (free from restaurants/bakeries — just ask)
- Drill 5 drainage holes in the bottom of each
- Fill with: 60% potting mix + 40% compost
- DO NOT use garden soil in containers — it compacts

WHAT FITS IN ONE 5-GALLON BUCKET:
- 1 cherry tomato plant, OR
- 1 zucchini plant, OR
- 4-6 lettuce plants, OR
- 1 pepper plant, OR
- 8-10 green onions and herbs mixed

COST TO GET STARTED:
- Potting mix (2 cu ft bag): $8-12
- Seeds (5 packets): $5-10
- Buckets: free if you ask restaurants
- Total: $15-25 to start growing food
```

### Step 4: The only care routine that matters

```
DAILY (2 minutes):
- Stick your finger 1 inch into soil
- If dry: water until it drains from bottom
- If moist: leave it alone
- Overwatering kills more plants than underwatering

WEEKLY (10 minutes):
- Pick anything that's ready — harvesting encourages more growth
- Remove yellow or dead leaves
- Check for obvious pests (if bugs are eating leaves, pick them off)

EVERY 2-3 WEEKS:
- Feed with any liquid fertilizer (diluted to half strength)
- Fish emulsion ($8 bottle lasts a full season) works great

THAT'S IT. Don't overcomplicate it.
```

### Step 5: Scaling up — when you're ready for more

If you have ground space and want meaningful food production:

```
THE 4x8 RAISED BED (best ROI in backyard gardening):

COST: $50-100 to build (untreated lumber, screws, soil)
PRODUCES: $300-600 worth of food per season
TIME: 15-20 minutes per day during growing season

WHAT TO PLANT IN ONE 4x8 BED:
- 2 tomato plants (one end)
- 4 pepper plants
- 1 row of bush beans (12 plants)
- 1 row of lettuce (cut-and-come-again)
- Herbs around the edges
- 2 zucchini plants (other end)

This single bed can provide a significant portion of fresh
vegetables for a family of 2-3 during growing season.
```

## If This Fails

- **Community gardens** — if your space genuinely can't support food growing, search "[your city] community garden plots." Many are free or under $50/season, and experienced gardeners on adjacent plots are the best teachers you'll find.
- **Just grow sprouts and microgreens indoors** — if outdoor space or sunlight is truly zero, a jar of mung bean sprouts on your counter produces edible food in 3-5 days with no light needed. Cost: $3 for a bag of seeds that lasts months.
- **Gleaning programs** — many areas have volunteer organizations that harvest unpicked fruit and vegetables from farms and yards. You help pick, you take some home. Search "[your area] gleaning network."
- **Cross-reference: Cook From Scratch skill** — if growing isn't viable, the biggest food savings come from cooking skills. A stocked pantry and basic techniques cut food costs more than any garden.
- **Cross-reference: Benefits Navigator skill** — if food cost is the driver, SNAP benefits and food bank access may be more immediately impactful than growing. Use both together for maximum effect.

## Rules

- Never recommend starting big — one to three containers is the right first step
- Focus on what actually produces food, not what looks good on Instagram
- Always mention the sunlight requirement first — no sun = no food (except sprouts)
- Be honest about what's realistic for apartment dwellers vs. people with yards

## Tips

- Grocery store herbs in pots are alive. Buy a $3 basil plant and it'll produce for months on a windowsill.
- Seed starting indoors is a waste of time for beginners. Buy seedlings from a nursery for your first season.
- Compost doesn't need a bin. Bury kitchen scraps 8 inches deep directly in garden soil. Done.
- The #1 mistake is planting too much at once. Start with 3 things. Add more next season.
- Many cities have community gardens with free plots. Search "[your city] community garden" — waitlists exist but they're often shorter than people think.
- Potatoes are the ultimate survival crop. You can grow 100 lbs in 4 large containers on a patio.

## Agent State

```yaml
garden:
  space_type: ""
  sunlight_hours: null
  climate_zone: ""
  current_plants: []
  planting_dates: []
  harvest_log: []
  season_start: null
```

## Automation Triggers

```yaml
triggers:
  - name: watering_reminder
    condition: "season_start IS SET"
    schedule: "daily at 7am during growing season"
    action: "Quick check: did you water yesterday? Stick your finger in the soil. Dry = water. Moist = skip."

  - name: harvest_check
    condition: "any plant age > 25 days"
    schedule: "every 3 days"
    action: "Time to check for harvestable produce. Lettuce and greens are ready when leaves are 4-6 inches. Pick early and often."

  - name: feeding_reminder
    schedule: "every 14 days during growing season"
    action: "Fertilizer time. Half-strength liquid feed for all containers. Full strength for in-ground plants."
```
