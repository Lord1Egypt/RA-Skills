# pet-food-calculator 🐾

**Feed your pet the right amount — computed with veterinary-standard math.**

Over half of dogs and cats are overweight, and the main cause isn't a mystery:
owners eyeball portions, bag guidelines are generous, and nobody has a
70×W^0.75 calculator in their head. This skill runs the exact formulas your
vet uses (RER → MER energy requirements) and turns them into grams of *your*
food per meal, a treat budget, a safe weight-loss timeline, and monthly cost.

## The real-world problem

- **59% of dogs, 61% of cats are overweight** (APOP surveys) — costing ~2 years of life expectancy
- Bag feeding charts are rounded up for active animals; a "cup" of kibble varies ~20% by density
- Weight-loss attempts fail or endanger pets: crash-dieting cats can develop fatal hepatic lipidosis
- Multi-food comparison (dry/wet/premium/prescription) is tedious guesswork

## What it does

```bash
python3 scripts/pet_food_calculator.py --species dog --weight 30 \
  --age adult --food-calories 3800
```

- **Daily calories** from species, life stage (puppy/kitten growth factors,
  neuter status, senior), and activity
- **Exact grams/day** from your food's kcal/kg label (the "metabolizable
  energy" line on every bag), split into meals
- **Treat budget** — enforces the veterinary ≤10% rule and subtracts it from kibble
- **Weight-loss plans** — computed at *ideal* weight, 1-2%/week (dogs) /
  0.5-1%/week (cats) targets, with feline calorie floors enforced
  automatically to prevent hepatic lipidosis
- **Food cost** — kg/month, monthly spend, how long a bag lasts
- **7-day transition schedule** — 25→50→75→100% to avoid GI upset when switching
- Growth guidance for puppies (keep lean, protect joints)

## Example

```
Cat FEEDING PLAN
 Life stage   : weightloss (×0.8 RER)
 Weight       : 7.2 kg now → 5.5 kg target
 Daily energy : 201 kcal/day
 PORTION      : 38 g/day of food (4800 kcal/kg), 19 g × 2 meals
 Treat budget : ≤ 20 kcal/day

 WEIGHT-LOSS PLAN
   Lose 1.7 kg at ~1.0%/week → ≈ 27 weeks
   Weigh every 2 weeks; adjust ±10% based on loss rate
```

## Safety notes

The calculator enforces: feline floors (never below 0.5×RER or 18 kcal/kg
ideal weight), max loss rates, and warns against crash diets. It is not a
substitute for veterinary care — unexplained weight changes need a vet.

## License

MIT © Denis Voronin
