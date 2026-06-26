---
name: orchard-fruit-trees
description: >-
  Planting and managing fruit trees and berry bushes for food production. Use when someone wants to grow fruit, is planting trees on a property, needs to maintain existing fruit trees, or wants faster-producing options like berry bushes.
metadata:
  category: skills
  tagline: >-
    Plant a tree that feeds your family for 50 years — site selection, pruning, pest management, and realistic timelines for fruit production.
  display_name: "Orchard & Fruit Tree Management"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install orchard-fruit-trees"
---

# Orchard & Fruit Tree Management

A single mature apple tree produces 200-400 lbs of fruit per year for decades. That's real food security. But fruit trees are a long game — you're making decisions now that determine production 5, 10, 50 years from now. This skill covers everything from site selection and variety choice to pruning, pest management, and the faster-payoff option of berry bushes for people who can't wait five years for their first apple. The critical insight most people miss: rootstock selection and formative pruning in the first three years determine 80% of your tree's lifetime productivity.

```agent-adaptation
# Localization note — fruit tree management is deeply climate-specific.
# Agent must follow these rules when working with non-US users:
- USDA Plant Hardiness Zones are US-specific. International equivalents:
  UK: RHS Hardiness Ratings (H1-H7)
  Europe: EEA plant hardiness maps
  Australia: Sunset Climate Zones or ANBG zones
  Canada: Canadian Plant Hardiness Zones (similar to USDA but separate system)
- Chill hour requirements are universal but sources differ by country.
  Agent MUST look up the user's specific zone and chill hours.
- Variety recommendations are regional. Local extension service equivalents:
  UK: Royal Horticultural Society (rhs.org.uk)
  Australia: State Department of Primary Industries
  Canada: Provincial agriculture ministry
  EU: National agricultural advisory services
- Pest and disease pressures vary by region. The spray schedules listed
  assume temperate North American conditions. Agent should reference
  local integrated pest management (IPM) guides.
- Citrus zones referenced (USDA 9-11) should be converted to local
  equivalent zones. Container growing is viable anywhere with indoor
  winter storage.
- Berry bush recommendations (blueberry soil pH, raspberry management)
  are broadly applicable but variety selection must be localized.
```

## Sources & Verification

- **USDA Plant Hardiness Zone Map** -- essential for variety selection. [planthardiness.ars.usda.gov](https://planthardiness.ars.usda.gov/)
- **Michael Phillips, "The Holistic Orchard"** -- comprehensive organic orchard management
- **Fedco Trees catalog** -- variety descriptions are excellent practical references for cold-climate growers
- **State cooperative extension fruit tree guides** -- free, research-backed, regionally specific (search "[your state] extension fruit tree guide")
- **University IPM (Integrated Pest Management) programs** -- evidence-based pest management by region
- **Lee Reich, "Grow Fruit Naturally"** -- organic fruit growing without synthetic inputs
- **USDA Web Soil Survey** -- free soil type maps for any parcel. [websoilsurvey.nrcs.usda.gov](https://websoilsurvey.nrcs.usda.gov/)

## When to Use

- User wants to plant fruit trees and doesn't know where to start
- Someone just bought property and wants to maximize food production
- User has existing fruit trees that aren't producing well or look unhealthy
- Someone wants fruit but doesn't want to wait years — berry bushes
- User needs help choosing varieties for their specific climate zone
- Someone is planning a small home orchard layout

## Instructions

### Step 1: Assess the site

**Agent action**: Ask the user for their location (or zip code for zone lookup), property details, and goals. Check the non-negotiable requirements before recommending anything.

```
SITE ASSESSMENT CHECKLIST:

Sunlight (non-negotiable):
[ ] 6+ hours of direct sun daily — most fruit requires full sun
[ ] 8+ hours is ideal for stone fruit and maximum production
[ ] Partial shade (4-6 hours) limits you to: sour cherry,
    gooseberry, currants, some raspberry varieties

Drainage:
[ ] Dig a 12" deep hole, fill with water, time the drain
    -> Drains in 1-4 hours: excellent
    -> Drains in 4-6 hours: acceptable for most fruit trees
    -> Drains in 6-12 hours: raised beds for berries only
    -> Standing water after 12 hours: not suitable for fruit trees
[ ] Fruit trees die in wet feet — this is the #1 site killer

Air circulation:
[ ] Gentle air movement reduces fungal disease
[ ] Avoid frost pockets (low spots where cold air settles)
[ ] Hilltops and slopes are better than valleys for fruit

Soil:
[ ] Get a soil test ($15-30 through your county extension office)
[ ] Most fruit trees prefer pH 6.0-7.0
[ ] Blueberries need pH 4.5-5.5 (acidic — plan ahead)
[ ] Soil test tells you what amendments to add BEFORE planting

Space:
[ ] Dwarf trees: 8-10 ft apart
[ ] Semi-dwarf trees: 12-15 ft apart
[ ] Standard trees: 20-25 ft apart
[ ] Berry bushes: 3-6 ft apart depending on type
```

### Step 2: Choose the right varieties

**Agent action**: Look up the user's USDA zone and chill hours. Recommend varieties that actually work for their climate. This is where most beginners go wrong.

```
UNDERSTANDING CHILL HOURS:

Chill hours = hours below 45F during winter dormancy.
If your area doesn't get enough chill hours for a variety,
the tree will never produce fruit reliably. Period.

Lookup: Search "[your city] chill hours" or check your
state extension office website.

High chill (800-1000+ hours): Northern US, upper Midwest
Medium chill (400-700 hours): Mid-Atlantic, Pacific Northwest
Low chill (100-400 hours): Deep South, coastal California
Minimal chill (<100 hours): Southern Florida, Hawaii, tropics

FRUIT TYPE GUIDE:

APPLES (most forgiving for beginners):
- Need 2 different varieties for cross-pollination
- Hundreds of varieties — match chill hours to your zone
- Produce in 2-3 years (dwarf) to 5-7 years (standard)
- Disease-resistant varieties save you spray work:
  Liberty, Enterprise, Freedom, GoldRush, Pristine

PEARS:
- Similar requirements to apples, less pest pressure
- European pears (Bartlett, Bosc) — pick unripe, ripen off tree
- Asian pears — eat crisp off the tree, less cold-hardy
- Fire blight is the main disease risk — choose resistant varieties

STONE FRUIT (peach, plum, cherry, apricot):
- Shorter-lived trees (15-25 years vs 50+ for apple)
- More disease and pest pressure
- Incredible production when they work
- Peaches: many are self-fertile (one tree is enough)
- Sweet cherries: need a pollinator, large trees
- Sour cherries: self-fertile, smaller, easier
- Plums: European (self-fertile) vs Japanese (need pollinator)

CITRUS (zones 9-11 only, or container anywhere):
- Meyer lemon is the easiest starter citrus
- Container citrus works in any climate with indoor winter storage
- Need winter temps above 28F (most varieties)
```

### Step 3: Select rootstock

**Agent action**: Explain rootstock and its impact. This decision affects the next 50 years.

```
ROOTSTOCK DETERMINES:

-> Tree size at maturity
-> Years until first fruit
-> Lifespan and vigor
-> Disease resistance
-> Anchoring (some need permanent staking)

ROOTSTOCK OPTIONS:

DWARF (8-10 ft mature height):
- First fruit: 2-3 years
- Full production: 4-5 years
- Requires permanent staking (weak root system)
- Easier to prune, spray, and harvest
- Best for: small yards, intensive management
- Common apple dwarf rootstocks: M9, M26, Bud 9

SEMI-DWARF (12-15 ft mature height):
- First fruit: 3-4 years
- Full production: 5-6 years
- May need staking first 2-3 years only
- Best balance of size, production, and manageability
- RECOMMENDED FOR MOST HOME GROWERS
- Common: M7, MM106, MM111

STANDARD (20-30 ft mature height):
- First fruit: 5-7 years
- Full production: 8-10 years
- No staking needed, deep root system
- Massive production (10-20 bushels per tree)
- Requires ladder for pruning and harvest
- Best for: large properties, low-maintenance orchards
- Common: seedling rootstock
```

### Step 4: Plant correctly

**Agent action**: Walk through planting technique. Mistakes at planting create problems for decades.

```
PLANTING GUIDE:

TIMING:
- Bare root trees: plant during dormancy (late winter/early spring)
  Cheapest option, widest variety selection
- Potted trees: plant anytime ground isn't frozen
  More expensive, limited selection, more forgiving timing

PLANTING STEPS:

1. Dig the hole:
   - Width: 2x the root ball or root spread
   - Depth: SAME as root ball — do NOT plant too deep
   - The graft union (bulge where rootstock meets variety)
     must be 2-3 inches ABOVE soil line
   - Planting too deep causes rootstock to root above the graft,
     defeating the purpose of your rootstock choice

2. Prepare roots:
   - Bare root: soak in water for 1-2 hours before planting
   - Trim any broken or circling roots
   - Spread roots outward — NEVER let them circle
   - Circling roots eventually girdle and kill the tree

3. Backfill:
   - Use the same soil you dug out (no amendments in the hole)
   - Amendments in the hole create a "bathtub effect" —
     roots won't grow out into native soil
   - Tamp gently to remove air pockets
   - Water thoroughly — 5-10 gallons to settle soil

4. Mulch:
   - 3-4 inches of wood chips in a donut shape
   - Keep mulch 6 inches away from the trunk (prevents rot)
   - Extend mulch to the drip line

5. Staking (dwarf rootstock only):
   - One sturdy stake, 18" from trunk
   - Tie loosely — allow some movement for trunk strength
   - Leave stakes for 2-3 years (permanent for M9)
```

### Step 5: Formative pruning (years 1-3)

**Agent action**: Explain the two main pruning forms and the counterintuitive first-year rule.

```
THE FIRST 3 YEARS DETERMINE EVERYTHING:

YEAR 1 — COUNTERINTUITIVE BUT CRITICAL:
Remove all fruit in year 1. Yes, all of it.
Let the tree build its root system and framework.
Picking off flowers/fruitlets now means dramatically
better production for the next 20-50 years.

PRUNING FORMS:

Central Leader (for apples, pears):
- One dominant vertical trunk
- Scaffold branches spiral around it at 6-8" vertical spacing
- Creates a Christmas tree shape
- Strong structure, good light penetration

Open Center / Vase (for stone fruit):
- Remove the central leader at planting
- Select 3-4 scaffold branches growing outward
- Creates an open bowl shape
- Better for stone fruit — more light, air circulation

YEAR 1 PRUNING:
Central leader: Head the tree at 30-36" at planting.
  Select the strongest upright shoot as the leader.
  Remove competing leaders.

Open center: Cut the trunk to 24-30" at planting.
  Select 3-4 well-spaced scaffold branches.
  Remove everything else.

YEARS 2-3 PRUNING:
- Continue shaping the framework
- Remove crossing branches
- Remove inward-growing branches
- Remove water sprouts (vigorous vertical shoots)
- Maintain open canopy for light and air
- Head scaffold branches to encourage branching

THE 3 D'S (every year, forever):
Always remove Dead, Diseased, and Damaged wood first.
Then address structure.
```

### Step 6: Ongoing management

**Agent action**: Cover annual care, thinning, and pest/disease management.

```
ANNUAL CARE CALENDAR:

LATE WINTER (dormant):
- Major pruning (while you can see the structure)
- Apply dormant oil spray (smothers overwintering insects and eggs)
- Order any new trees for spring planting

SPRING (bud break through petal fall):
- Fertilize lightly (compost ring around drip line, or balanced
  organic fertilizer — do NOT over-fertilize, excess nitrogen
  means lots of leaves, little fruit)
- Neem oil spray at petal fall (when petals drop, NOT during bloom —
  spraying during bloom kills pollinators)
- Monitor for fire blight on apples/pears (blackened, wilted shoots)

EARLY SUMMER:
- THIN FRUIT: Remove 50% of developing fruitlets
  -> Counterintuitive, but remaining fruit is larger, sweeter,
     and the tree stays healthier
  -> Apples: thin to one fruit per cluster, 6" apart on branch
  -> Stone fruit: thin to 4-6" between fruit
- Continue spray program every 2-3 weeks if using organic sprays
- Monitor for codling moth, apple maggot, plum curculio

SUMMER:
- Water deeply during dry spells (1-2" per week)
- Monitor for pest and disease
- Harvest as fruit ripens

FALL:
- Clean up fallen fruit (reduces pest overwintering)
- Apply tree wrap to young trunks (prevents sunscald and rodent damage)
- Final mulch application before winter
- Do NOT prune in fall (wounds heal slowly, invites disease)

COMMON DISEASES:
- Apple scab: fungal, causes spots and cracking. Resistant varieties
  eliminate this problem entirely.
- Fire blight: bacterial, kills branches fast. Prune 12" below
  visible infection, sterilize tools between cuts.
- Brown rot: stone fruit nightmare. Remove mummified fruit,
  improve air circulation, fungicide if severe.
- Cedar-apple rust: remove nearby cedar/juniper or plant resistant
  varieties.
```

### Step 7: Berry bushes for faster results

**Agent action**: If the user wants faster production or has limited space, present berry options as a complement or alternative to fruit trees.

```
BERRY BUSHES — FRUIT IN 1-3 YEARS:

BLUEBERRIES:
- Need ACID soil: pH 4.5-5.5 (amend with sulfur if needed)
- Plant 2+ varieties for cross-pollination
- Production: small harvest year 2-3, full production year 5-6
- Yield: 5-10 lbs per mature bush
- Lifespan: 20-30 years
- Need: full sun, consistent moisture, acidic mulch (pine needles)
- Easiest varieties: Bluecrop, Duke, Patriot (highbush)

RASPBERRIES:
- Production: small harvest year 2, full production year 3
- Yield: 3-5 lbs per row-foot per year
- Types: summer-bearing (one crop) vs everbearing (two crops)
- They SPREAD AGGRESSIVELY — plant in a contained bed or
  be prepared to manage suckers constantly
- Pruning: remove canes that fruited (they only fruit once
  on summer-bearing), keep new canes for next year
- Easiest: Heritage (everbearing), Latham (summer-bearing)

BLACKBERRIES:
- Production: year 2, full production year 3
- Yield: 5-10 lbs per plant
- Thornless varieties exist and produce well (Triple Crown, Chester)
- Similar management to raspberries — contain the spread
- More heat-tolerant than raspberries

STRAWBERRIES:
- Production: small harvest year 1, full production year 2
- Yield: ~1 lb per plant per year
- Types: June-bearing (one big crop) vs everbearing (smaller
  continuous harvest)
- Replace plants every 3-4 years (they decline)
- Great for small spaces, raised beds, containers
- Net them or the birds get everything

CURRANTS AND GOOSEBERRIES:
- Tolerate partial shade (4+ hours sun)
- Production: year 2-3
- Yield: 5-10 lbs per bush
- Very cold-hardy, low maintenance
- Illegal to grow in some areas (white pine blister rust host) —
  check state regulations
```

## If This Fails

- **Tree isn't producing fruit after expected timeframe?** Check: chill hours met? Pollination partner present? Over-fertilizing with nitrogen? Pruning too aggressively (removing fruit wood)? Some varieties are biennial bearers (heavy crop one year, light the next).
- **Tree looks sick?** Take photos of leaves, bark, and fruit to your county extension office or local nursery. They diagnose for free. Don't guess on treatments.
- **Deer eating everything?** Individual tree cages (welded wire, 5 ft tall minimum) are the only reliable solution short of a full perimeter fence. Spray deterrents work temporarily at best.
- **Overwhelmed by pest management?** Plant disease-resistant apple varieties (Liberty, Enterprise) and skip the spray schedule entirely. You'll get imperfect-looking fruit that tastes just as good.
- **Wrong variety for your climate?** If a tree isn't thriving after 3 years, consider grafting a better variety onto the existing rootstock rather than starting over. Or accept the loss and replant correctly.

## Rules

- Always look up the user's USDA zone and chill hours before recommending specific varieties
- Never recommend planting without confirming adequate drainage and sunlight
- Emphasize formative pruning in years 1-3 — this is when most beginners make permanent mistakes
- If the user has existing sick trees, recommend extension office diagnosis before suggesting treatments
- Adjust all timing for the user's hemisphere and climate
- Always mention pollination requirements — a single apple tree won't produce

## Tips

- Buy from local nurseries when possible. Their stock is selected for your climate, and their advice is specific to your area. Mail-order is fine for variety selection but local beats catalog every time.
- Fruit tree tags at big box stores often list the wrong zone. Trust the variety name and look up the specs yourself.
- The best time to plant a fruit tree was 10 years ago. The second best time is this dormant season.
- Start with 2-3 trees maximum. Learn on those before expanding. A neglected orchard produces worse than no orchard.
- Save your pruning cuts to use as scion wood. Once you learn to graft, you can multiply any variety for free.
- Compost is the best fertilizer for fruit trees. A 2-inch layer around the drip line each spring is all most trees need.

## Agent State

```yaml
state:
  site:
    usda_zone: null
    chill_hours: null
    sun_hours: null
    drainage_tested: false
    soil_test_done: false
    soil_ph: null
    space_available_sqft: null
  trees:
    planted: []
    varieties: []
    rootstocks: []
    planting_dates: []
    current_year_of_growth: {}
    pruning_form: {}
  berries:
    planted: []
    varieties: []
    planting_dates: []
  management:
    last_pruning_date: null
    last_spray_date: null
    thinning_done_this_year: false
    pest_issues_current: []
    disease_issues_current: []
  harvest:
    total_yield_lbs: {}
    harvest_dates: []
  follow_up:
    next_pruning_due: null
    next_spray_due: null
    seasonal_tasks_pending: []
```

## Automation Triggers

```yaml
triggers:
  - name: dormant_pruning_reminder
    condition: "management.last_pruning_date IS NULL OR month_since(management.last_pruning_date) >= 11"
    schedule: "annually in late winter (February-March)"
    action: "Dormant season is here — time for major pruning. This is the most important annual maintenance task. Want to walk through what to remove on each tree?"

  - name: spray_schedule_prompt
    condition: "trees.planted IS NOT EMPTY AND management.last_spray_date IS NULL"
    schedule: "late winter"
    action: "If you're following a spray schedule, dormant oil application should happen before bud break. Are you planning to spray this season? I can walk through the timing."

  - name: fruit_thinning_reminder
    condition: "trees.planted IS NOT EMPTY AND management.thinning_done_this_year = false"
    schedule: "June"
    action: "Early summer is fruit thinning time. Removing 50% of developing fruitlets now means bigger, better fruit and a healthier tree. Need a refresher on spacing?"

  - name: zone_check
    condition: "site.usda_zone IS NULL AND trees.planted IS EMPTY"
    action: "Before we pick varieties, I need to look up your USDA zone and chill hours. What's your zip code or city?"

  - name: first_year_fruit_removal
    condition: "ANY tree in trees.current_year_of_growth = 1"
    schedule: "spring"
    action: "Your first-year trees should have all flowers and fruitlets removed. It feels wrong, but it redirects energy to roots and structure. This pays off massively in years 3-5."
```
