# Grocery Store Sections Reference

Use this to organize grocery lists by aisle/section. Items are sorted in this order (matching a typical grocery store layout — perimeter first, then center aisles).

---

## Section Order

| # | Section | Icon | Common Items |
|---|---------|------|-------------|
| 1 | **Produce** | 🥬 | Fresh fruits, vegetables, herbs, salad mixes, pre-cut veggies, avocados, potatoes, onions, garlic, ginger, lemons, limes |
| 2 | **Bakery** | 🍞 | Bread, rolls, tortillas, pita, baguettes, burger buns, naan, bagels |
| 3 | **Meat & Seafood** | 🥩 | Chicken (breast, thighs, whole), ground beef, ground turkey, steak, pork chops, bacon, sausage, salmon, shrimp, tilapia |
| 4 | **Dairy & Eggs** | 🧀 | Milk, butter, eggs, yogurt (Greek, regular), cheese (shredded, block, sliced), cream cheese, sour cream, heavy cream, plant milks |
| 5 | **Deli** | 🥪 | Deli meats (turkey, ham), prepared salads, hummus, olives, specialty cheeses |
| 6 | **Frozen** | ❄️ | Frozen vegetables, frozen fruit, frozen pizza, ice cream, frozen meals, frozen fish, frozen berries, frozen corn, frozen peas |
| 7 | **Pantry & Dry Goods** | 📦 | Pasta, rice, quinoa, oats, flour, sugar, breadcrumbs, panko, cereal, crackers, dried beans, lentils, couscous, ramen noodles |
| 8 | **Canned & Jarred** | 🥫 | Canned tomatoes (diced, crushed, paste), canned beans, chicken/vegetable broth, coconut milk, canned tuna, pasta sauce, salsa, peanut butter |
| 9 | **Spices & Condiments** | 🧂 | Salt, pepper, cumin, chili powder, paprika, garlic powder, Italian seasoning, curry powder, garam masala, soy sauce, fish sauce, hot sauce, olive oil, vinegar, Worcestershire, mustard, ketchup, mayo |
| 10 | **Beverages** | 🥤 | Water, juice, coffee, tea, sparkling water, milk alternatives |
| 11 | **Snacks** | 🍿 | Chips, nuts, dried fruit, granola bars, popcorn, pretzels, trail mix |
| 12 | **Other / Non-Food** | 🧹 | Paper towels, dish soap, trash bags, aluminum foil, plastic wrap, ziplock bags |

---

## Sorting Rules for the Agent

1. When generating a grocery list, assign each item to one of the sections above.
2. Within each section, sort items alphabetically.
3. If the household has multiple stores, create a separate section-organized list per store.
4. Mark pantry staples (from `data/household.json` → `pantry_staples`) with a "🏠 Staple" indicator.
5. Show quantity + source meals for combined items: "Chicken thighs (3.5 lbs) — Mon dinner + Wed lunch"
6. Estimate price per section and total at the bottom.

## Ambiguous Item Placement

Some items could go in multiple sections. Use these rules:
- **Fresh herbs** (basil, cilantro, parsley) → Produce
- **Tofu** → Produce (refrigerated section) or Dairy (depends on store)
- **Tortillas** → Bakery (or Pantry for shelf-stable)
- **Eggs** → Dairy & Eggs
- **Butter** → Dairy & Eggs
- **Nuts** → Snacks (unless specifically for cooking, then Pantry)
- **Coconut milk** → Canned & Jarred (canned version) or Dairy (carton version)
