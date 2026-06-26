---
name: home-food-planner
description: "Family meal planning tool that provides weekly menu planning, nutrition analysis, shopping list generation, ingredient management, and recipe recommendations. Use when user needs to plan family meals, create weekly menus, manage groceries, analyze nutrition, or get recipe recommendations based on available ingredients."
---

# Home Food Planner — Family Meal Planning

Your family meal planning assistant, helping you plan weekly menus, manage ingredients, generate shopping lists, and make family meals healthier and more organized.

## Quick Reference

| Feature | Example Commands |
|---------|-----------------|
| Weekly Menu | "Plan this week's menu" "Generate a weekly menu" |
| Ingredient Management | "What's in my fridge" "Record ingredients" |
| Shopping List | "Generate shopping list" "What do I need to buy" |
| Nutrition Analysis | "Analyze today's nutrition" "Is this meal balanced" |
| Recipe Recommendations | "Recommend dinner" "What to make with chicken" |
| Special Diets | "Vegetarian menu" "Low-fat meal plan" |

## Core Features

### 1. Weekly Menu Planning

**Planning Dimensions:**

| Dimension | Description |
|-----------|-------------|
| Number of Diners | Adults, children, seniors |
| Dietary Preferences | Tastes, cuisines, restrictions |
| Nutrition Goals | Balanced, weight loss, muscle gain, wellness |
| Time Constraints | Quick weekday meals, weekend slow cooking |
| Budget Range | Daily/weekly budget |
| Special Needs | Allergies, religious diets, medical diets |

**Menu Structure:**
```
Monday:
  Breakfast: Oatmeal with milk + Boiled egg + Fruit
  Lunch: Tomato egg noodles
  Dinner: Steamed sea bass + Garlic broccoli + Rice
  
Tuesday:
  ...
```

**Planning Principles:**
- Nutritional balance: Proper ratio of protein, carbs, fats, vitamins
- Ingredient reuse: Avoid waste, multi-purpose ingredients
- Cooking efficiency: Balance complex and simple dishes
- Taste rotation: Avoid repetition

### 2. Ingredient Management

**Ingredient Categories:**

| Category | Examples | Shelf Life |
|----------|----------|------------|
| Vegetables | Bok choy, tomatoes, potatoes | 3-7 days |
| Fruits | Apples, bananas, oranges | 3-14 days |
| Meat | Pork, chicken, beef | Refrigerated 2-3 days, frozen 1-3 months |
| Seafood | Fish, shrimp, shellfish | Refrigerated 1-2 days, frozen 1-2 months |
| Eggs & Dairy | Eggs, milk, yogurt | 7-21 days |
| Soy Products | Tofu, dried tofu | 3-7 days |
| Dry Goods | Rice, flour, beans | 6-12 months |
| Condiments | Oil, salt, soy sauce | 6-24 months |

**Management Functions:**
- Stock recording: Purchase date, quantity, expiration date
- Inventory query: What ingredients are currently available
- Expiration reminders: Ingredients approaching expiration
- Usage tracking: Record consumption

### 3. Shopping List Generation

**Generation Logic:**
1. Calculate required ingredients based on menu plan
2. Compare with current inventory
3. Generate purchase list
4. Organize by supermarket sections

**List Categories:**
```
🥬 Produce Section:
   - Tomatoes 500g
   - Broccoli 1 head
   
🥩 Meat Section:
   - Chicken breast 300g
   - Ground pork 200g
   
🐟 Seafood Section:
   - Sea bass 1 fish
   
🥛 Dairy Section:
   - Milk 1L
   - Eggs 12 pieces
```

### 4. Nutrition Analysis

**Analysis Dimensions:**

| Nutrient | Daily Recommendation | Function |
|----------|---------------------|----------|
| Calories | 1800-2400 kcal | Energy supply |
| Protein | 50-70g | Tissue repair |
| Carbohydrates | 250-350g | Main energy |
| Fat | 50-70g | Essential fatty acids |
| Dietary Fiber | 25-30g | Gut health |
| Vitamin C | 100mg | Immunity |
| Calcium | 800mg | Bone health |
| Iron | 12-18mg | Blood health |

**Analysis Output:**
- Single meal nutrition analysis
- Daily nutrition summary
- Weekly nutrition trends
- Nutritional gap alerts

### 5. Recipe Recommendations

**Recommendation Methods:**

#### By Ingredients
```
User: I have chicken, potatoes, and carrots in the fridge

Recommendations:
1. Potato Stewed Chicken - Classic combo, nutritious
2. Curry Chicken - Great with rice
3. Chicken Salad - Refreshing and healthy
```

#### By Scenario
```
Quick Weekday Meals (under 15 minutes):
- Tomato scrambled eggs
- Garlic broccoli
- Green pepper shredded pork

Weekend Slow Cooking (over 1 hour):
- Braised pork belly
- Slow-cooked soup
- Baking
```

#### By Nutrition Goal
```
Weight Loss Meals:
- High protein, low carb
- Steaming, boiling, cold dishes

Muscle Gain Meals:
- High protein, moderate carbs
- Chicken breast, beef, eggs
```

### 6. Special Diet Planning

**Supported Types:**

| Type | Characteristics | Considerations |
|------|-----------------|----------------|
| Vegetarian | No meat/eggs/dairy or no meat only | Protein supplementation, B12 |
| Weight Loss | Low calorie, high protein | Avoid excessive restriction |
| Muscle Gain | High protein, moderate carbs | Training coordination |
| Blood Sugar Control | Low GI foods | Blood sugar monitoring |
| Low Sodium | Low salt cooking | Kidney function |
| Children | Balanced nutrition, easy to digest | Avoid allergens |
| Seniors | Soft and easy to chew | Chronic disease management |

## Usage Examples

### Example 1: Weekly Menu Planning
```
User: Plan this week's menu, 2 adults, prefer Chinese cuisine, budget 500 yuan

Plan:
Monday:
  Breakfast: Soy milk and fried dough sticks + Tea egg
  Lunch: Kung Pao chicken rice bowl
  Dinner: Tomato egg soup + Stir-fried seasonal vegetables + Rice

Tuesday:
  Breakfast: Milk and oatmeal + Fried egg
  Lunch: Beef noodles
  Dinner: Steamed fish + Garlic broccoli + Rice

... (full week)

Estimated: Ingredient cost about 480 yuan
```

### Example 2: Ingredient Management and Shopping List
```
User: Record today's grocery purchases, generate shopping list

Stock Record:
- Tomatoes 500g (shelf life 7 days)
- Chicken breast 300g (refrigerated 3 days)
- Eggs 12 pieces (shelf life 21 days)

Current Inventory:
- Vegetables: Tomatoes, bok choy, potatoes
- Meat: Chicken breast, ground pork
- Other: Eggs, milk

Items needed for this week's menu:
- Sea bass 1 fish
- Broccoli 1 head
- Tofu 1 block
```

### Example 3: Nutrition Analysis
```
User: Analyze today's nutrition intake

Today's Intake:
Breakfast: Oatmeal + Egg + Milk
Lunch: Rice + Braised pork + Green vegetables
Dinner: Noodles + Tomato eggs

Nutrition Analysis:
- Calories: 2100 kcal ✅
- Protein: 65g ✅
- Carbs: 280g ✅
- Fat: 70g ⚠️ Slightly high
- Dietary fiber: 22g ⚠️ Slightly low
- Vitamin C: 85mg ⚠️ Slightly low

Recommendations:
- Tomorrow reduce oil, increase vegetables and fruits
```

## Recipe Collection

### Quick Meals (15 minutes)

| Dish | Main Ingredients | Difficulty | Time |
|------|-----------------|------------|------|
| Tomato Scrambled Eggs | Tomatoes, eggs | ⭐ | 10 min |
| Garlic Broccoli | Broccoli, garlic | ⭐ | 8 min |
| Green Pepper Shredded Pork | Green pepper, pork | ⭐⭐ | 15 min |
| Mapo Tofu | Tofu, minced meat | ⭐⭐ | 15 min |
| Hot and Sour Shredded Potatoes | Potato, chili | ⭐ | 10 min |

### Home-style Dishes (30 minutes)

| Dish | Main Ingredients | Difficulty | Time |
|------|-----------------|------------|------|
| Braised Pork Belly | Pork belly | ⭐⭐⭐ | 45 min |
| Steamed Fish | Sea bass | ⭐⭐ | 20 min |
| Cola Chicken Wings | Chicken wings | ⭐⭐ | 30 min |
| Potato Stewed Beef | Beef, potatoes | ⭐⭐⭐ | 60 min |
| Sweet and Sour Ribs | Ribs | ⭐⭐⭐ | 40 min |

### Soups

| Soup | Main Ingredients | Benefits |
|------|-----------------|----------|
| Tomato Egg Soup | Tomatoes, eggs | Appetizing |
| Seaweed Egg Drop Soup | Seaweed, eggs | Iodine supplement |
| Winter Melon Rib Soup | Winter melon, ribs | Cooling |
| Corn Carrot Soup | Corn, carrots | Sweet and refreshing |
| Silver Ear Lotus Seed Soup | Silver ear, lotus seeds | Lung nourishing |

## Nutrition Tips

### Daily Diet Recommendations

**Breakfast (30% calories):**
- Carbs: Whole wheat bread / oatmeal / porridge
- Protein: Eggs / milk / soy milk
- Vitamins: Fruit / vegetables

**Lunch (40% calories):**
- Staple: Rice / noodles
- Protein: Meat / fish / soy products
- Vegetables: 2 or more types

**Dinner (30% calories):**
- Light meals preferred
- Eat until 70% full
- Finish 3 hours before sleep

### Ingredient Pairing Principles

**Golden Combinations:**
- Tomato + Egg: Nutritional complement
- Tofu + Fish: Better calcium absorption
- Lean meat + Vegetables: Better iron absorption
- Grains + Beans: Protein complement

**Avoid Combinations:**
- Spinach + Tofu (calcium oxalate)
- Soy milk + Eggs (affects absorption)

## Related Skills

- `ming` — Destiny analysis (dietary taboos)
- `yhd` — YiHaoDian shopping
- `shopping` — General shopping guidance
- `health` — Health management (if available)

## Feedback

- If useful: `clawhub star home-food-planner`
- Updates: `clawhub sync`