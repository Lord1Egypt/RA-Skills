# Number Sense

AI prose often creates false precision: exact tiny measurements in emotional, bodily, or conversational beats where no person would naturally measure.

Examples:

- her finger moved three centimeters
- he was silent for seven seconds
- she stepped back one centimeter
- they stood 2.3 meters apart during an emotional exchange

These can make prose sound instrument-measured rather than observed.

## Do Not Remove All Numbers

Keep exact numbers when they are earned:

- public facts: a building is 476 meters tall
- medical or forensic evidence: a wound is 2.3 cm
- engineering, science, finance, recipes, logistics, sports, legal, or news contexts
- age, date, room number, train time, price, dosage, score, case number
- clues, rules, countdowns, costs, constraints, or payoffs

## Usage

Before generation:

```powershell
python -m humanwriting.cli build `
  --style fiction `
  --review `
  --number-sense `
  --task "Write a tense dialogue scene without unnecessary exact micro-measurements."
```

Fiction, webnovel, and self-media automatically include `natural-measurement` under `--deep-review`. Compact `--review` omits the full number module to preserve long-form context. It can also be selected explicitly with `--number-sense`.

After a draft exists:

```powershell
python -m humanwriting.cli audit `
  --draft examples/false-precision-draft.zh-CN.md `
  --profile numbers
```

## Audit Standard

For each exact number, ask:

- Who knows this number in the moment?
- Was it measured, recorded, reported, inferred, or merely decorative?
- Does it change evidence, risk, plot, characterization, or world state?
- Would felt scale, relational scale, or approximate scale sound more natural?

## Repair

| False precision | Better |
| --- | --- |
| Her finger moved three centimeters. | Her finger edged a little higher. |
| He was silent for seven seconds. | He was silent long enough for her to look away. |
| She stepped back one centimeter. | She shifted back, just out of the light. |
| The wound was 2.3 cm. | Keep if medical/forensic context. |
