---
name: hosting-feeding-groups
description: >-
  Practical skills for cooking and hosting groups of 10-50 people. Use when someone needs to feed a crowd for events, community gatherings, family reunions, block parties, or regular group meals on a budget.
metadata:
  category: skills
  tagline: >-
    Cook for 10, 20, or 50 people without losing your mind -- scaling recipes, timing multiple dishes, and budget group meals.
  display_name: "Hosting & Feeding Groups"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-19"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install hosting-feeding-groups"
---

# Hosting & Feeding Groups

Feeding 4 people is cooking. Feeding 20 is logistics. The difference isn't just multiplying ingredients -- it's timing, equipment, food safety, and setup. Most people either panic and overspend, or wing it and run out of food at a party. Neither has to happen. This skill covers the practical mechanics of feeding 10-50 people well, safely, and cheaply. The core move: pick foods that are forgiving, scale reliably, and serve themselves.

```agent-adaptation
# Localization note
- Portion sizes vary by culture (US portions run large, ~8oz protein; many other
  countries serve 4-6oz portions with more sides)
- Common crowd-feeding foods differ: rice and curry (South/Southeast Asia),
  asado/BBQ (South America), tagine (North Africa), stews (West Africa),
  pierogi/dumplings (Eastern Europe), rice and beans (Caribbean/Latin America)
- Temperature units: Fahrenheit in US, Celsius elsewhere
  140F = 60C (hot holding), 40F = 4C (cold holding)
- Food safety regulations for community events vary by jurisdiction
- Swap unit measurements: cups/ounces/pounds vs. grams/kilograms/liters
- Dietary restriction prevalence varies (celiac awareness higher in Northern Europe,
  vegetarian baseline higher in India)
```

## Sources & Verification

- **USDA Food Safety for Large Events** -- food safety guidelines for serving groups, temperature requirements, and holding times. https://www.fsis.usda.gov/food-safety
- **ServSafe Food Handler Guidelines** -- industry-standard food safety training and protocols. https://www.servsafe.com
- **Feeding America Community Meal Guides** -- practical resources for community meal coordination. https://www.feedingamerica.org
- **Commercial kitchen scaling references** -- professional recipe scaling ratios and techniques
- **Anthropic, "Labor market impacts of AI"** -- March 2026 research showing this occupation/skill area has near-zero AI exposure. https://www.anthropic.com/research/labor-market-impacts

## When to Use

- User is hosting a family reunion, block party, or community event and needs to feed a crowd
- Someone volunteers to cook for a group and doesn't know where to start
- User wants to do regular group meals (Sunday dinner, community kitchen, potluck coordination)
- Someone is feeding a crowd on a tight budget
- User is overwhelmed by the logistics of cooking for more than 8 people
- Potluck coordination help (what to assign, how to avoid 15 desserts and no main course)

## Instructions

### Step 1: Recipe Scaling Math

**Agent action**: Teach the user how recipe scaling actually works -- because it's not just multiplication.

```
RECIPE SCALING -- WHAT MULTIPLIES AND WHAT DOESN'T

THE BASIC RULE:
- Original recipe serves 6, you need to serve 24
- Multiplier = 24 / 6 = 4x

WHAT SCALES LINEARLY (multiply directly):
- Meat, beans, rice, pasta, vegetables
- Butter, oil, cream
- Canned goods (tomatoes, broth, coconut milk)
- Sugar in baked goods (mostly)

WHAT DOES NOT SCALE LINEARLY:
- SALT: Use 70-80% of the multiplied amount, then taste and adjust
  (Example: Recipe calls for 1 tsp salt, 4x = 4 tsp, use 3 tsp and taste)
- SPICES AND HERBS: Use 60-75% of the multiplied amount
  Spices get stronger in larger volumes -- start low, taste, adjust
- LIQUID IN SOUPS/STEWS: Use 80% of multiplied amount
  Less evaporation per volume in a bigger pot
- GARLIC: Use 75% of multiplied amount (gets sharper at scale)
- CHILI/HOT PEPPERS: Use 50-60% of multiplied amount
  Heat compounds unpredictably -- you can always add more
- BAKING POWDER/SODA: For batches over 3x, reduce to 70% and
  test one batch first. Chemistry changes at scale.
- THICKENERS (flour, cornstarch): Use 80% of multiplied amount

THE GOLDEN RULE: You can always add more. You can't take it out.
Season incrementally at scale.
```

### Step 2: Plan the Menu

**Agent action**: Help the user choose dishes that work for crowds. The criteria: holds well, serves itself, scales reliably, and is affordable.

```
MENU PLANNING FOR CROWDS

THE BEST CROWD FOODS SHARE THESE TRAITS:
- One-pot or sheet-pan (minimal timing coordination)
- Good at room temperature or held warm for 1-2 hours
- Self-serve friendly (people can plate themselves)
- Cheap per serving
- Forgiving (won't ruin if overcooked by 15 minutes)

WORST CROWD FOODS:
- Anything that must be served immediately (souffle, eggs, fried food)
- Anything requiring individual plating
- Anything with a narrow doneness window (steaks, fish fillets)
- Anything with expensive per-serving costs ($$$)

MENU STRUCTURE FOR 20 PEOPLE:
1. ONE main protein dish (chili, pulled pork, chicken thighs)
2. ONE starch (rice, pasta, bread, tortillas, potatoes)
3. ONE vegetable side (roasted vegetables, coleslaw, green salad)
4. ONE "extra" (bread/rolls, chips and salsa, fruit)
5. ONE dessert (optional but appreciated -- brownies, cookies)

PORTION PLANNING:
- Protein: 6-8 oz per adult (1/3 to 1/2 pound raw)
- Starch: 1 cup cooked per person
- Vegetable/salad: 1/2 cup to 1 cup per person
- Total food: Plan for 1 to 1.25 pounds of food per adult
- Always make 15-20% more than headcount (seconds, surprises, leftovers)
- If alcohol is served, people eat 10-15% less food
- If it's a potluck, plan as if 1/3 of promised dishes won't show up
```

### Step 3: Budget Crowd Meals

**Agent action**: Show the user specific cost breakdowns for feeding groups at different budget levels.

```
COST PER HEAD ANALYSIS (US prices, 2026 approximate)

$3/HEAD -- THE BARE BONES:
- Rice and beans with salsa and tortillas
- Pasta with red sauce, garlic bread
- Soup and bread (potato soup, minestrone, chili)
- Bulk oatmeal bar with toppings (for breakfast events)

$5/HEAD -- THE SWEET SPOT:
- Taco bar (ground beef or chicken, shells, toppings)
- Chili bar (chili, rice, cheese, sour cream, cornbread)
- Pasta bar (2 sauces, garlic bread, salad)
- Sheet-pan chicken thighs, rice, roasted vegetables

$8/HEAD -- IMPRESSIVE ON A BUDGET:
- Pulled pork (buy pork shoulder on sale ~$2/lb), coleslaw, rolls
- Baked potato bar with chili, broccoli, cheese, sour cream
- Chicken and rice with 2 sides and rolls
- Enchilada assembly (can prep day before)

$12-15/HEAD -- NICE EVENT:
- BBQ spread (2 meats, 3 sides, rolls, dessert)
- Italian spread (lasagna, salad, garlic bread, dessert)
- Fajita bar with guacamole and all the fixings

WHERE TO SAVE:
- Buy protein in bulk or on sale and freeze (pork shoulder, chicken
  thighs, ground beef/turkey)
- Costco/Sam's Club for cheese, tortillas, bread, condiments
- Restaurant supply stores (open to public) for disposable
  serving ware -- much cheaper than grocery store party supplies
- Generic/store brand for anything going into a big pot
- Root vegetables (potatoes, carrots, onions) are always cheap
```

### Step 4: Timing Multiple Dishes

**Agent action**: Help the user create a reverse timeline so everything is ready at the same time.

```
REVERSE TIMELINE METHOD

TARGET SERVING TIME: ___:___ (fill in)
Work backwards from there.

EXAMPLE: Taco bar for 20, serving at 6:00 PM

5:45  Set out toppings (cheese, sour cream, lettuce, salsa, etc.)
5:40  Warm tortillas (oven at 300F, wrapped in foil, 10 min)
5:30  Final taste/season check on meat
5:00  Rice into rice cooker (or finish stovetop rice)
4:30  Start browning ground beef (season at 4:45)
4:00  Prep all toppings (chop lettuce, dice tomatoes, open cans,
      grate cheese, slice limes)
3:00  Go to store for anything missing
DAY BEFORE: Make salsa. Grate cheese. Prep any slow-cook items.

GENERAL TIMING RULES:
- Anything that can be prepped the day before, should be
- Starches (rice, pasta) take 20-45 min, start 1 hour before serving
- Proteins take 30 min to 6 hours depending on method
- Slow cooker proteins: start 6-8 hours before serving
- Oven proteins: start 1.5-3 hours before serving
- Stovetop proteins: start 45-90 minutes before serving
- Toppings/sides: prep 2 hours before, set out 15 min before
- ALWAYS add 30-minute buffer. Something will take longer than planned.

DELEGATING:
- Give helpers the prep work (chopping, grating, setting up)
- Keep the cooking to 1-2 people who know the recipes
- Assign ONE person to manage drinks and ice
- Assign ONE person to manage setup (tables, plates, utensils)
```

### Step 5: Equipment for Crowd Cooking

**Agent action**: Help the user figure out what equipment they need and how to get it without buying everything.

```
EQUIPMENT NEEDS BY GROUP SIZE

10-15 PEOPLE (your normal kitchen can handle this):
- Your largest pot (8+ quart)
- 2 sheet pans
- Rice cooker or large pot for starch
- Serving spoons and tongs

16-30 PEOPLE (borrow or supplement):
- Second large pot (borrow from a neighbor)
- Slow cooker or Instant Pot (6-8 quart)
- Chafing dishes for keeping food warm (buy disposable: $8-12 each
  at restaurant supply or Amazon)
- Extra sheet pans (2-4 total)
- Large mixing bowls for salads and toppings
- Insulated beverage dispenser for coffee/tea

30-50 PEOPLE (you're running a small operation):
- Multiple slow cookers (borrow 3-4 from friends)
- Turkey roaster/electric roaster oven ($30-50, reusable, holds
  20+ quarts -- the secret weapon for large group cooking)
- Folding tables for serving line ($30 each or borrow)
- Full chafing dish setup (3-4 stations)
- Large coolers for cold items and drinks
- Possibly a second grill if doing BBQ

WHERE TO GET EQUIPMENT WITHOUT BUYING:
1. Borrow from neighbors (tool-lending network from mutual aid skill)
2. Church/community center kitchens (many let you use facilities)
3. Ask the group -- "I'm cooking, who can bring a slow cooker?"
4. Restaurant supply stores sell cheap basics
5. Rental companies rent chafing dishes, tables, chairs ($50-100/event)
```

### Step 6: Food Safety at Scale

**Agent action**: Cover the food safety basics that matter when serving groups. Foodborne illness at a group event is a real risk.

```
FOOD SAFETY -- NON-NEGOTIABLE AT SCALE

THE DANGER ZONE: 40F - 140F (4C - 60C)
Food in this range grows bacteria rapidly.
Maximum time food can sit in the danger zone: 2 HOURS.
If the ambient temperature is above 90F/32C: 1 HOUR.

HOT FOOD: Keep above 140F/60C
- Chafing dishes with sterno cans
- Slow cookers on "warm" setting
- Oven at lowest setting (170F) with door cracked
- Check with a food thermometer every 30 minutes

COLD FOOD: Keep below 40F/4C
- Serve on ice (fill a tray with ice, nest serving bowl in it)
- Coolers with ice for backup supplies
- Don't put everything out at once -- refill from cold storage

THE 2-HOUR RULE:
After 2 hours at room temperature, toss it. No exceptions.
This is the rule that prevents making 20 people sick.
Set a timer when food goes out.

HAND WASHING:
- Set up a hand-washing station if no convenient sink
  (water jug with spigot + soap + paper towels)
- Every cook washes hands before starting
- After touching raw meat, wash before touching anything else

LEFTOVERS:
- Refrigerate within 2 hours of serving
- Divide into shallow containers (cools faster)
- Label with date
- Use within 3-4 days or freeze

ALLERGIES:
- Label every dish with its major allergens
- Keep at least one dish that is: gluten-free, dairy-free, nut-free
- When in doubt, print ingredient lists and put them next to each dish
```

### Step 7: Five Crowd-Tested Recipes

**Agent action**: Provide these tested recipes that scale reliably to 20 servings.

```
RECIPE 1: ALL-PURPOSE CHILI (serves 20)

5 lbs ground beef or turkey (or 4 cans black beans for vegetarian)
3 large onions, diced
8 cloves garlic, minced
4 cans (28 oz each) crushed tomatoes
4 cans (15 oz each) kidney beans, drained
4 cans (15 oz each) black beans, drained
3 tbsp chili powder
2 tbsp cumin
1 tbsp smoked paprika
2 tsp salt (adjust to taste)
1 tsp black pepper
Optional: 2 chipotle peppers in adobo sauce (adds smoky heat)

Brown meat in batches in largest pot. Add onions, cook 5 min.
Add garlic, spices, cook 1 min. Add tomatoes and beans.
Simmer 45-90 minutes. The longer, the better.
Serve with: shredded cheese, sour cream, diced onion, cornbread.
Cost: ~$3.50/serving with toppings.

---

RECIPE 2: PULLED PORK (serves 20-25)

8-10 lbs pork shoulder (bone-in is cheaper and more flavorful)
Your favorite BBQ rub (or: 2 tbsp brown sugar, 2 tbsp paprika,
  1 tbsp each garlic powder, onion powder, black pepper, salt,
  1 tsp cayenne)
2 cups apple cider vinegar
2 cups BBQ sauce (plus more for serving)

Rub pork shoulder all over with spice rub. Refrigerate overnight.
Slow cooker: Add vinegar, cook on low 10-12 hours.
Oven: 275F in covered Dutch oven for 6-8 hours.
When it falls apart with a fork, it's done.
Shred with two forks. Mix in BBQ sauce. Serve on buns.
Cost: ~$2-3/serving (buy shoulder on sale at $1.50-2/lb).

---

RECIPE 3: PASTA BAR (serves 20)

4 lbs pasta (penne or rigatoni -- holds sauce better than spaghetti)
SAUCE 1 -- Red: 4 jars (24 oz) marinara + 1 lb browned Italian sausage
SAUCE 2 -- Alfredo: 3 jars (15 oz) Alfredo sauce, heated
TOPPINGS: Parmesan, red pepper flakes, fresh basil, garlic bread

Cook pasta in batches (your pot probably holds 2 lbs max).
Slightly undercook (1 min less than package says) -- it'll keep
cooking in the warm serving vessel. Toss with a little oil to
prevent sticking. Keep warm in covered pot or chafing dish.
Cost: ~$3/serving with garlic bread.

---

RECIPE 4: TACO BAR (serves 20)

5 lbs ground beef or chicken thighs
3 packets taco seasoning (or make your own: 3 tbsp chili powder,
  2 tbsp cumin, 1 tbsp garlic powder, 1 tbsp onion powder,
  2 tsp salt, 1 tsp paprika, 1/2 tsp cayenne)
40 taco shells or 40 small flour/corn tortillas (or both)
TOPPINGS: shredded lettuce, diced tomatoes, shredded cheese,
  sour cream, salsa, diced onion, cilantro, lime wedges,
  hot sauce, canned jalapenos

Brown meat in batches. Add seasoning and 1.5 cups water per batch.
Simmer 10 min until thickened. Keep warm in slow cooker.
Set up assembly line: shells/tortillas > meat > toppings.
Cost: ~$4/serving with all toppings.

---

RECIPE 5: SHEET-PAN CHICKEN AND RICE (serves 20)

10 lbs chicken thighs (bone-in, skin-on -- cheapest and most flavor)
Olive oil, salt, pepper, garlic powder, paprika, Italian seasoning
6 cups uncooked rice (makes ~18 cups cooked)
3 lbs mixed vegetables (broccoli, bell peppers, zucchini, onions)

Season chicken generously. Spread on sheet pans (5-6 thighs per pan,
you'll need 3-4 pans). Roast at 425F for 35-40 minutes until
internal temp hits 165F. On separate pans, roast vegetables with
oil, salt, pepper at 400F for 20-25 minutes.
Cook rice in batches or use rice cooker(s).
Cost: ~$4-5/serving (buy thighs in bulk at $1-2/lb).
```

### Step 8: Potluck Coordination

**Agent action**: If the user is coordinating a potluck rather than cooking everything themselves, provide a system that prevents the "15 desserts and no entree" problem.

```
POTLUCK COORDINATION SYSTEM

ASSIGN CATEGORIES, NOT SPECIFIC DISHES:
Tell each person which category to bring, not what specific dish.
This avoids duplicates while letting people make what they're good at.

CATEGORIES AND RATIOS (for 20 people, 12 contributors):
- Main dish / protein: 3 people (each brings enough for 8-10)
- Starch / carb side: 2 people (each brings enough for 10-12)
- Vegetable / salad: 3 people (each brings enough for 8-10)
- Bread / snack / appetizer: 2 people
- Dessert: 2 people
- Drinks: Host provides, or assign 1 person

WHAT THE HOST PROVIDES:
- Plates, utensils, napkins, cups
- Ice and coolers
- Serving utensils (many people forget these)
- Table setup and serving area
- At minimum: one main dish as backup

POTLUCK COMMUNICATION TEMPLATE (send to group):

"[Event Name] Potluck -- [Date, Time, Location]

We have [X] people coming. To avoid 12 desserts and no main course,
I'm assigning categories. Please bring enough of your dish to
serve [8-10] people.

Your assignment: [CATEGORY]

Please bring your dish in/on something you don't mind losing track
of (or label it with your name). Bring your own serving utensil.

If your dish contains common allergens (nuts, dairy, gluten, shellfish),
please put a note card next to it.

Reply with what you're planning to bring so we can avoid duplicates.
See you there!"

TRACKING (simple):
Name          | Category    | Bringing          | Serves
______________|_____________|___________________|_______
              |             |                   |
```

## If This Fails

- If you're completely overwhelmed, just make one big pot of chili and buy cornbread and a bag of shredded cheese. That feeds 20 for $70 and nobody complains.
- If timing goes wrong and food isn't ready, put out bread, chips, and any cold items first. People can graze while the main course finishes.
- If you run out of food, you didn't make enough. For next time, increase quantities by 25%.
- If food safety is compromised (food sat out more than 2 hours in warm conditions), do not serve it. Order pizza. It's cheaper than making people sick.
- If the potluck is unbalanced despite assignments, the host's backup dish saves the day. Always have one.

## Rules

- The 2-hour rule for food in the danger zone is not flexible. Set a timer.
- Always have at least one dish that covers the most common dietary restrictions (gluten-free, dairy-free, vegetarian)
- Label every dish at a potluck or buffet with its contents and major allergens
- Cook proteins to safe internal temperatures every time: chicken 165F, ground beef 160F, pork 145F
- Taste and adjust seasoning at scale -- never trust the math alone
- Start prepping the day before. Day-of-only cooking for 20+ people is how you end up crying in the kitchen at 5pm.

## Tips

- Chicken thighs are the crowd-cooking cheat code: cheap, hard to overcook, always flavorful. Skip breasts.
- One extra bag of ice is always the right call. You will run out of ice.
- Disposable aluminum chafing pans and sterno cans turn any table into a buffet line for $10 per station.
- If you're cooking for 30+, make two different things in large quantities rather than five things in small quantities. Simpler logistics, better results.
- Self-serve bars (taco, pasta, baked potato, chili) are the best format for crowds. Less work for you, people customize their own plate, dietary restrictions handle themselves.
- Ask for help with cleanup before the event. "I'll cook if two people will handle cleanup" is a fair deal that people accept.
- Leftover containers: have a stack of cheap takeout containers or ask people to bring their own. Sending people home with food is the best party favor.

## Agent State

```yaml
hosting:
  event_type: null
  guest_count: null
  budget: null
  budget_per_head: null
  menu_planned: false
  dishes:
    - name: null
      serves: null
      prep_time: null
      cost: null
  timeline_created: false
  equipment_needed: []
  equipment_secured: []
  dietary_restrictions: []
  potluck_assignments: []
  shopping_list_created: false
  day_before_prep_done: false
```

## Automation Triggers

```yaml
triggers:
  - name: timeline_creation
    condition: "menu_planned IS true AND timeline_created IS false"
    action: "You've planned your menu but don't have a cooking timeline yet. Let's build a reverse timeline from your serving time so everything is ready together."

  - name: shopping_list
    condition: "menu_planned IS true AND shopping_list_created IS false"
    action: "Menu is set. Let's build a shopping list with quantities scaled for your group size, organized by store section."

  - name: day_before_reminder
    condition: "event is tomorrow AND day_before_prep_done IS false"
    action: "Your event is tomorrow. Here's what to prep tonight: chop vegetables, make sauces, marinate proteins, set up the serving area, and confirm your equipment is clean and ready."

  - name: food_safety_timer
    condition: "event is in progress"
    action: "Food safety check: has any dish been sitting out for more than 90 minutes? If approaching 2 hours, either refresh from hot/cold storage or remove from the serving line."
```
