# List Operations — Grocery

## Adding Items

### Basic add
"Add milk" → adds to current list with default quantity

### With quantity
"Add 2L of milk" → specific amount

### With context
"Add ingredients for carbonara" → extract: pasta, eggs, guanciale, pecorino, black pepper

### Bulk add
User shares list → parse line by line, deduplicate

## Removing Items

"Remove the milk" → removes from list
"Actually, skip the pasta" → removes
"I already have eggs" → removes + optionally update pantry

## Modifying

"Make it 3kg of chicken instead" → update quantity
"Change almond milk to oat milk" → substitute

## List Management

### Multiple lists
- Default: "weekly" list
- Create named: "Add to camping list: flashlight batteries"
- Switch: "Show me the party list"

### Clear / reset
"Clear my list" → archive to history, empty current
"Start fresh" → same

### Share / export
"Give me the list" → formatted output grouped by section

## Section Grouping

When user requests organized list:
```
🥬 Produce
- Lettuce
- Tomatoes (2kg)
- Onions (1kg)

🥛 Dairy
- Milk (4L)
- Greek yogurt (x4)

🧊 Frozen
- Peas
- Ice cream
```

## Meal Plan Integration

When user provides meals:
1. Parse each meal for ingredients
2. Check pantry for existing stock
3. Calculate quantities for household size
4. Add missing items to list
5. Report: "Added 12 items for this week's meals. You already have onions and olive oil."

## Conflict Resolution

Same item, different quantities:
- "You added rice twice (1kg + 500g). Merging to 1.5kg?"

Conflicting restrictions:
- "Recipe calls for cheese but you noted dairy-free. Substitute or skip?"
