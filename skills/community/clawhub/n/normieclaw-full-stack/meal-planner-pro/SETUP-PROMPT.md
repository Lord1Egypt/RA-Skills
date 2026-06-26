# Meal Planner Pro — First-Run Setup

When this skill is activated for the first time, follow this setup sequence exactly.

---

## Step 1: Create Directory Structure

Run these commands to create all necessary directories and set permissions:

```bash
set -euo pipefail
umask 077
mkdir -p data/meal-plans data/grocery-lists data/prep-plans
chmod 700 data data/meal-plans data/grocery-lists data/prep-plans
```

## Step 2: Initialize Data Files

Create empty starter files with secure permissions:

```bash
printf '%s\n' '{}' > data/household.json
printf '%s\n' '[]' > data/ratings.json
printf '%s\n' '[]' > data/meal-history.json
printf '%s\n' '[]' > data/freezer.json
printf '%s\n' '[]' > data/flagged-recipes.json
chmod 600 data/household.json data/ratings.json data/meal-history.json data/freezer.json data/flagged-recipes.json
```

## Step 3: The Interview (Household Profile Builder)

Guide the user through this conversation. Keep it warm, fun, and lightweight — like a friend getting to know their kitchen. Don't make it feel like a form. Adapt your phrasing to the user's energy.

### 3a. Who's in the household?

Say something like:
> "Let's get to know your household! Who's eating? Give me names, ages, and whether they're an adult or kid. Example: 'Me (35), my partner Alex (33), and our daughter Mia (6).'"

For each person, create a member object in `data/household.json` with these fields:
- `name` (string)
- `age` (integer)
- `role` ("adult" or "child")
- `allergies` (array, empty for now)
- `hard_dislikes` (array, empty for now)
- `texture_issues` (array, empty for now)
- `adventurousness` (integer 1-5, set later)
- `protein_preference` (string, set later)
- `dietary_style` (null for now)
- `notes` (string, empty for now)

### 3b. Allergies & Dietary Restrictions

> "Any allergies or dietary restrictions I should know about? This is the important stuff — I'll NEVER suggest anything with these ingredients. Even if it's just one person, tell me who and what."

Update each member's `allergies` array. Be thorough — ask follow-up if vague ("When you say 'nut allergy,' is that all tree nuts, or just peanuts?").

If anyone follows a dietary style (vegetarian, keto, gluten-free, etc.), set their `dietary_style` field and reference `config/dietary-profiles.md` for what that means.

### 3c. Loves & Hates

> "Now the fun part! What does everyone LOVE to eat? And what makes someone go 'absolutely not'? Let's go person by person."

Update `hard_dislikes` for each member. Also capture notes about favorite foods — put these in the `notes` field.

### 3d. Texture Issues

> "This one's especially handy for kids (but adults too!) — any texture things? Like 'no mushy stuff,' 'hates slimy textures,' 'won't eat anything crunchy'?"

Update `texture_issues` array. Common ones: "mushy", "slimy", "gritty", "chewy", "crunchy" (when unexpected).

### 3e. Adventurousness Scale

> "On a scale of 1-5, how adventurous is each person with food?
> 1 = chicken nuggets and plain pasta only
> 2 = safe comfort food, nothing weird
> 3 = open to familiar cuisines (Mexican, Italian, Chinese)
> 4 = loves trying new things
> 5 = bring on the weird stuff, the spicier the better"

Set `adventurousness` for each member.

### 3f. Protein Preferences

> "If you had to rank proteins for each person, what's the order? Like 'chicken > beef > fish' or 'tofu > chicken > shrimp'?"

Set `protein_preference` as a ranked string for each member.

### 3g. Preferred Stores

> "Where do you usually shop? Just the main store is fine, or if you have a strategy (like 'Costco for bulk, Whole Foods for produce'), I can work with that!"

Update `preferred_stores` in the household object:
```json
"preferred_stores": [
  { "name": "Store Name", "role": "primary", "color": "green" }
]
```
Roles: "primary" (main store), "bulk_staples" (Costco/Sam's), "produce" (farmers market/specialty), "specialty" (ethnic grocery, etc.).

### 3h. Budget Preference

> "Last one — how would you describe your grocery budget style?
> - **Budget:** Let's keep it lean, lots of pantry meals
> - **Moderate:** Mix of nice ingredients and practical choices
> - **Generous:** Quality ingredients, no stress about price"

Set `budget_preference` on the household object.

## Step 4: Write the Complete Profile

After gathering all answers, write the complete `data/household.json` file. Read it back to the user for confirmation:

> "Here's your household profile! Take a look and let me know if anything needs tweaking:"

Display a summary of each member with their key attributes. Ask for confirmation before proceeding.

Set final permissions:
```bash
chmod 600 data/household.json
```

## Step 5: Verification — The Fridge Test

> "Profile looks great! Let's take it for a spin. Got anything in the fridge right now? Snap a photo and I'll suggest tonight's dinner using what you already have — tailored to your household's tastes!"

If the user sends a photo, follow the "What's in My Fridge?" Photo Mode instructions from SKILL.md to identify ingredients, cross-reference profiles, and suggest 3-5 meals.

If they don't have a photo handy:
> "No worries! Whenever you're ready, just send a fridge pic or say 'plan my week' and we'll get cooking. 🍳"

## Step 6: Confirm Setup Complete

> "You're all set! Here's what I can do:
> - **'Plan my week'** — I'll generate a full meal plan for your household
> - **Send a fridge photo** — I'll tell you what to make tonight
> - **'Grocery list'** — Get an organized shopping list after a plan is set
> - **'Prep day'** — Get a timed schedule for batch cooking
> - **Rate meals** — Tell me what everyone thought so I get smarter
>
> The more you use me, the better I get. Let's eat! 🎉"
