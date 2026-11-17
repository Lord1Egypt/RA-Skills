---
name: pet-poison-triage
description: Use when a pet (dog/cat) may have eaten something toxic — species-aware hazard scoring with the first-30-minutes protocol (never induce vomiting unless told; fur decontamination for cats), chocolate theobromine mg/kg dose math across 7 product types, xylitol hypoglycemia (0.1 g/kg) and kidney-injury (0.5 g/kg) thresholds with the birch-sugar rename trap, grape/raisin unknown-toxin protocol, plant lookup (TRUE lily + cat = ER, sago palm, lily of the valley vs peace lily), and the pet poison kit + emergency card.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [pets, poison, toxicity, emergency, dogs, cats, chocolate, xylitol, lilies, veterinary]
---

# Pet Poison Triage

A dog eats a tray of brownies at 11 PM. The owner googles "chocolate
dog" and gets a wall of contradictory advice — some of it genuinely
dangerous (salt-induced vomiting, milk, hydrogen peroxide for cats).
What actually decides outcomes is (a) knowing the species-specific
hazard class within seconds, (b) doing dose math instead of vibes, and
(c) not wasting the decontamination window on folk remedies. This skill
is the calm first 30 minutes: what it is, how bad for THIS animal, what
to do now, what never to do, and what to bring to the ER.

## When to Use

- Pet just ate something suspicious (food, plant, medication, chemical)
- "Is this actually toxic?" — species-aware answer fast (cat vs dog
  differ dramatically: xylitol barely affects cats; acetaminophen kills
  them at tiny doses)
- Dose math for the calculable ones: chocolate (theobromine mg/kg),
  xylitol (g/kg vs hypoglycemia/AKI thresholds)
- Plant identification of risk: true lily vs peace lily vs lily of the
  valley — three completely different emergencies for a cat
- Building the pet poison kit / emergency card BEFORE anything happens

**Always in parallel:** call ASPCA Animal Poison Control (888) 426-4435
or Pet Poison Helpline (855) 764-7661, or your ER. This tool makes the
call faster and better-informed — it is not a substitute. If gums are
pale/blue/yellow, breathing is labored, or the pet collapses: ER now,
skip everything else.

## The Method

```bash
# The generic entry point — hazard class + first-30-min protocol
python3 scripts/pet_poison_triage.py triage "sugar-free gum" --species dog
python3 scripts/pet_poison_triage.py triage "tiger lily" --species cat

# Dose math (the calculable toxins)
python3 scripts/pet_poison_triage.py chocolate --product baking_chocolate \
    --grams 30 --weight-kg 10
python3 scripts/pet_poison_triage.py xylitol --grams 3 --weight-kg 25 --pure

# Unknown-toxin protocol (no safe dose exists)
python3 scripts/pet_poison_triage.py grapes --species dog

# Plant risk lookup + the poison kit checklist
python3 scripts/pet_poison_triage.py plants "easter lily"
python3 scripts/pet_poison_triage.py kit
```

## Dose Thresholds (what the math means)

**Chocolate (dogs):** theobromine mg/kg — <20 monitor; 20-40 mild
(vomiting, restlessness); 40-60 moderate (tremors, arrhythmia → vet
now); >60 severe (seizures → ER). Product theobromine: baking/cocoa
16-20 mg/g vs milk 1.5 mg/g vs white ~0 — 10× differences make
"amount of chocolate" meaningless without the type.

**Xylitol (dogs):** ≥0.1 g/kg hypoglycemia (crash in 10-60 min);
≥0.5 g/kg acute kidney injury. Sugar-free gum runs ~0.3-1 g/piece —
count pieces. Rename trap: "birch sugar" = xylitol.

**Grapes/raisins (dogs):** toxin unidentified, no safe dose, individual
sensitivity — any confirmed ingestion = vet same day, ideally <6h for
decontamination + 48-72h kidney monitoring.

## Species Asymmetry Table (the lethal traps)

| Toxin | Dog | Cat |
|---|---|---|
| xylitol | severe (hypoglycemia) | minimal |
| acetaminophen | severe | deadly (10 mg/kg) |
| ibuprofen | severe | deadly |
| true lilies | mild | deadly (pollen/vase water) |
| chocolate | severe | moderate (cats rarely eat it) |
| permethrin (dog flea spot-on) | ok | deadly — never share |

## Common Pitfalls

1. **Inducing vomiting yourself.** Wrong method (salt, ipecac, finger)
   causes harm; right method (3% peroxide, dogs only) needs dose and
   timing and is contraindicated for some toxins (corrosives,
   hydrocarbons). Only on professional instruction.
2. **"He seems fine."** The deadly toxins have lag: antifreeze has a
   fake-recovery phase, sago palm and grapes show signs at 1-3 days,
   rat poison at 3-5 days. Asymptomatic ≠ safe for these.
3. **Cat treated as small dog.** Cats differ in direction AND degree
   (lilies deadly for cats/mild for dogs; xylitol reverse). Species
   selection matters more than weight math.
4. **White chocolate panic / milk-chocolate complacency.** Both wrong:
   run the math on product type + amount + weight.
5. **Ignoring fur contamination.** Cats are poisoned by grooming
   (lily pollen, antifreeze on paws). Wash with dish soap; that IS
   the intervention.
6. **Losing the wrapper.** The ER needs the product (xylitol content,
   rodenticide type — three classes with different antidotes).
7. **Waiting for the hotline fee to be worth it.** $75-85 vs a $3,000
   ER visit or a dead pet; the fee is trivially worth it whenever
   dose math lands in a severe band.

## Verification Checklist

- [ ] Species confirmed (drives everything)
- [ ] Weight in kg actually measured (doses are per kg)
- [ ] Product type identified from packaging (not memory)
- [ ] Ingestion time noted (decontamination windows)
- [ ] Hotline/ER called for any moderate+ verdict
- [ ] Wrapper/product in the bag for the ER
- [ ] Kit restocked: unopened 3% peroxide (it expires), syrup, numbers

## References

- `references/toxin-reference.md` — the full toxin table with doses,
  onset windows, decontamination rules, what to bring per toxin class,
  hotline numbers by country, and the toxic-vs-safe plant shortlist.
