---
name: "Pantry Staple Reset"
description: "Build a lean pantry restock list from current staples, upcoming meals, and real gaps without overbuying or making dietary assumptions."
version: "1.0.0"
type: prompt-flow
license: "MIT-0"
language: "en"
tags: ["home admin", "pantry", "grocery planning", "restock", "meal planning"]
---

# Pantry Staple Reset

## Trigger

Use this skill when the user wants to reset pantry basics, make a grocery list from what they already have, or restock essentials without buying duplicates.

Good trigger phrases include:

- "Help me reset my pantry"
- "What staples should I restock?"
- "Make a lean grocery list"
- "I keep overbuying pantry items"
- "Plan pantry basics for the week"
- "Group this grocery list by aisle"

## Deliverable

Produce a **Pantry Reset List** with:

1. Current staple inventory
2. Useful quantities to keep on hand
3. Upcoming meal needs
4. Actual gaps to buy
5. Store aisle groups
6. A lean cart with optional extras separated

## Required Inputs

Ask for any missing details that materially affect the list:

- Household size or number of people eating from the pantry
- Current pantry staples, even if rough or photographed and transcribed by the user
- Upcoming meals, cooking plans, or eating pattern for the next few days
- Store preference if aisle grouping matters
- Allergies, avoid-list items, dietary restrictions, or label concerns
- Budget or space limit, if relevant

If the user does not provide meals, create a simple neutral restock list based only on common pantry categories and clearly label it as a draft.

## Workflow

### 1. List staples

Organize the user's current staples by category:

- Grains and starches
- Canned and jarred goods
- Proteins
- Baking basics
- Oils, vinegar, and sauces
- Spices and seasonings
- Breakfast and snacks
- Freezer helpers
- Household cooking supplies

### 2. Estimate useful quantities

Suggest modest target quantities based on household size, storage space, and expected use. Avoid bulk-buying by default.

Use ranges instead of rigid rules, for example:

- Rice or pasta: one open pack plus one backup if used weekly
- Canned tomatoes or beans: two to four cans if used in planned meals
- Cooking oil: replace only if low or near empty

### 3. Check upcoming meals

Map planned meals to pantry needs. If meals are unknown, ask for two to five expected meals or use a short placeholder section.

```text
MEAL NEEDS
- [Meal]: [pantry items needed]
- [Meal]: [pantry items needed]
```

### 4. Find gaps

Compare current inventory against target quantities and meal needs. Mark each gap as:

- Buy now
- Check before buying
- Optional
- Skip for now

### 5. Group by store aisle

Group the final list in a practical shopping order:

- Produce if needed for planned meals
- Bakery or bread
- Dry goods and grains
- Canned and jarred goods
- Condiments and sauces
- Spices and baking
- Refrigerated
- Frozen
- Household supplies

Keep aisle groups flexible because stores differ.

### 6. Build a lean cart

Separate true needs from nice-to-have items. Include a no-overbuy note for each category where the user already has enough.

## Output Template

```text
PANTRY RESET LIST

1. SNAPSHOT
- Household assumption: [number or unknown]
- Planning window: [days]
- Main constraint: [budget, space, allergies, none stated]

2. CURRENT STAPLES
- [Category]: [items on hand]

3. TARGET QUANTITIES
- [Item]: [modest target] - [reason]

4. UPCOMING MEAL GAPS
- [Meal]: [items needed]

5. BUY / CHECK / SKIP
Buy now:
- [item] - [quantity] - [why]

Check before buying:
- [item] - [what to verify]

Optional:
- [item] - [why optional]

Skip for now:
- [item] - [why enough]

6. STORE AISLE GROUPS
- [Aisle group]: [items]

7. LEAN CART
- Must buy: [items]
- Only if budget allows: [items]
- Do not buy this trip: [items]
```

## Example Prompts

- "My pantry is full but I still can't figure out what to cook. Help me reset my staples — list what I have, what I need, and build a lean grocery list."
- "I keep buying duplicates of things I already have. Guide me through a pantry reset so I only buy what I actually need this week."
- "I'm planning meals for the next five days. Help me check my pantry staples, find the gaps, and group my shopping list by store aisle."

## Safety Boundary

- Do not make dietary, allergy, religious, medical, or cultural food assumptions.
- Ask about allergies, avoid-list foods, and label needs before recommending specific food substitutions.
- Remind the user to check ingredient labels when allergies, intolerances, or dietary restrictions are involved.
- Do not provide medical nutrition advice or claim that a pantry list treats a health condition.
- Keep quantities modest by default to avoid overbuying, waste, and storage problems.
