---
name: nutri-calc
description: "Precise nutrition calculator — Chinese food database, goal-oriented macro tracking"
---

# Nutri Calc (nutri-calc)

Nutrition analysis tool with a 2000+ entry Chinese food database. Accepts natural language food descriptions ("一碗牛肉面", "三两饺子"), calculates TDEE and macro targets from user profile, compares intake vs goals, identifies gaps, and suggests corrective meals.

## Workflow

1. Parse natural language — accept free-text meal descriptions (e.g. "早餐两个鸡蛋+牛奶, 午餐红烧牛肉饭+可乐"). Segment into individual food items. Estimate portion sizes from common Chinese serving units (碗, 份, 两, 个, 杯, 盘). Handle regional dish variants.
2. Query nutrition database — look up each item from the Chinese food composition database. Return: calories, protein (g), fat (g), carbs (g), fiber (g), sodium (mg) per 100g or per serving. Fallback: estimate from similar dishes when exact match missing.
3. Calculate daily requirements — use user profile (weight, height, age, gender, activity level) to compute:
   - BMR (Mifflin-St Jeor formula)
   - TDEE (BMR × activity multiplier)
   - Macro split by goal: muscle gain (40P/30F/30C), fat loss (35P/25F/40C), maintenance (30P/25F/45C)
4. Compare intake vs targets — for each meal and cumulative daily total, show: actual vs target for calories and each macro. Color-code (green = on track, yellow = 10-20% off, red = >20% off).
5. Gap analysis — identify specific macro shortfalls or excesses:
   - "Protein shortfall 20g → you need ~100g chicken breast or 2 eggs + 1 cup milk"
   - "Carbs excess 40g → consider reducing rice portion by 1/3 at dinner"
6. Smart supplement suggestions — for identified gaps, suggest realistic Chinese-diet additions: "备选: 加一份卤牛肉(30g蛋白) 或 一杯豆浆(10g蛋白+健康脂肪)". Consider meal time and meal balance.
7. Multi-day tracking — accept consecutive day inputs. Plot trend: daily caloric surplus/deficit, macro consistency, weekly averages. Alert on drastic swings.
8. Output — nutrition report: per-meal breakdown table + daily totals vs targets + radar chart (5 dims) + gap fill suggestions + trend summary for multi-day. Export as Markdown or screenshot-friendly text block.

## Sample prompts

- `nutri-calc track --weight 75 --height 178 --age 30 --gender male --activity moderate --goal muscle --meals "早餐两个鸡蛋+牛奶, 午餐红烧牛肉饭"`
- `nutri-calc track --weight 65 --goal fat-loss --meals "早餐: 三两饺子, 午餐: 宫保鸡丁+米饭, 晚餐: 沙拉"`
- `nutri-calc analyze --food "一碗兰州牛肉面"`
- `nutri-calc history --days 7`
