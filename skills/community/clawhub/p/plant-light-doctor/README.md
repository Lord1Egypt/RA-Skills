# Plant Light Doctor

**Why do houseplants die? Mostly it's the light — and nobody can measure it.**

Every plant shop tag says "bright indirect light". No tag says what that means,
and no apartment matches. A north window in Helsinki delivers ~8× less light
than a south window in Athens — yet both get sold the same monstera. The result:
millions of slow, etiolated, pale plants and millions of people convinced they
have a "black thumb".

## The problem

- "Low / medium / bright indirect" is unmeasurable folk wisdom.
- The same window orientation differs radically by **latitude, floor,
  obstructions, glass, climate** — none of which the plant tag accounts for.
- Winter light collapse: a window that's a jungle in July is a cave in December.
- Grow lights are bought blindly: too weak, wrong spectrum hours, or 10×
  overkill — because nobody translates "my plant needs more light" into
  PPFD × hours × watts.

## The solution

`plant-light-doctor` computes the real horticulture metric — **DLI
(Daily Light Integral, mol·m⁻²·day⁻¹)** — for YOUR window from physics:
solar declination → day length → clear-sky PPFD → vertical wall capture by
orientation → corrections for floor, obstruction, glass, overhang, climate.
It then matches 40+ common houseplants against the window's **worst month**
with honest verdicts: **THRIVES / SURVIVES / STRUGGLES / IMPOSSIBLE** — and if
you want a plant the window can't feed, it sizes the grow light: required
PPFD, photoperiod, and realistic wattage for your shelf.

## Quick start

```bash
# Audit: north window, 4th floor, cloudy city (Helsinki)
python3 scripts/plant_light_analyzer.py --orientation N --latitude 60.2 \
    --floor 4 --climate cloudy

# Purchase decision: can this E window grow basil (Berlin)?
python3 scripts/plant_light_analyzer.py --orientation E --latitude 52.5 \
    --floor 2 --check basil

# Ground floor S window blocked 70% by the building across the street
python3 scripts/plant_light_analyzer.py --orientation S --latitude 41.0 \
    --floor 1 --obstruction 0.7 --list-matches

# Size a grow light to reach herbs-grade DLI (12) in a dark window
python3 scripts/plant_light_analyzer.py --orientation NW --latitude 55.7 \
    --floor 5 --grow-light --target-dli 12
```

## What you get

- **Monthly DLI table** for the exact window, worst month highlighted
  ("plan around THIS")
- **Verdict per plant** at worst and best month, with plain-language
  expectations ("will live but never bloom", "will etiolate by March")
- **Ranked match lists**: what THRIVES in this window vs what's IMPOSSIBLE
- **Grow-light spec**: gap in mol/day → required PPFD at canopy →
  watts for quality vs cheap fixtures → hang height and timer advice
- **Symptom cross-reference** (references/plant-dli-table.md): leggy stems,
  faded variegation, no fenestration, no rebloom — mapped to DLI deficits

## Who needs this

- Anyone buying a plant for a specific spot (before killing it)
- Plant owners diagnosing leggy/pale/non-blooming plants
- Windowsill herb/lettuce growers deciding if a grow light is worth it
- People in high-latitude or low-light apartments who keep being told
  "just get a snake plant"

## Files

- `SKILL.md` — full workflow, pitfalls, example sessions
- `scripts/plant_light_analyzer.py` — the analyzer (pure stdlib, no deps)
- `references/light-physics.md` — the model, formulas, worked examples,
  how to measure real light with a phone
- `references/plant-dli-table.md` — DLI needs for 40+ plants, symptom
  diagnostics, placement cheat sheet

## Accuracy

The model is honest about being ±30%: it beats folk wisdom by an order of
magnitude but can't see your net curtains. For precision, the reference
includes a phone-lux-meter conversion method (PPFD ≈ lux/54 for sunlight).

## License

MIT © Denis Voronin
