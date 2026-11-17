# Property Tax Appeal Kit

Fewer than 5% of homeowners appeal their property assessment — which is exactly why mass-appraisal errors persist: nobody checks them. The record card carries the previous owner's "finished basement," the model doesn't know the highway arrived behind your fence, and a 25–45-day appeal window ticks from the notice date while owners assume "you can't fight city hall." You can, with math: boards rule on **facts and ratios**, not on "my taxes are too high."

This kit replaces the "we'll appeal for 50% of your savings" firm with four commands:

1. **equalize** — your assessment ratio vs the town average; verdict bands from STRONG UNEQUALITY (file today, savings quantified at your millage) to UNDERASSESSED (do NOT appeal — you'd invite a raise).
2. **card** — record-card factual-error audit (wrong square footage/baths is the cheapest win in appeals; no comps needed, mechanical value impact).
3. **comps** — comparable-sales grading (±25% size band, outlier dropping, median $/sqft) with a subject value estimate and whether the market argument helps or backfires.
4. **timeline** — dated steps from your notice date: informal review call, card audit, evidence packet, formal filing with a safety margin before the hard deadline.

Plus the hearing script: lead with factual errors, then uniformity, then market value, and close with ONE requested number backed by recomputable math.

## Real problem it solves
Median US property tax is ~$2,800/yr and errors of 10–25% are common after revaluation years; a successful appeal saves $500–2,000/yr *until the next reassessment cycle*, and the evidence (public record card, public rolls, closed sales) costs nothing but the effort of assembling it. The kit tells you whether you have a case (equalization verdict), what kind (factual vs uniformity vs market), what it's worth (savings × cycle years), and by when (dated timeline) — before you spend a single afternoon or a contingency fee.

## Quick start
```bash
python3 scripts/ptax.py equalize --assessed 420000 --market-est 365000 \
    --town-avg-ratio 0.92 --millage 24.5
python3 scripts/ptax.py card --card-sqft 2100 --actual-sqft 1950 \
    --card-baths 2.5 --actual-baths 1.5 --assessed 420000 --market-est 365000
python3 scripts/ptax.py comps --assessed 420000 --subject-sqft 1950 \
    --sales "385000,2400" "322000,1900" "359000,2150" "341000,2000" "299000,1650"
python3 scripts/ptax.py timeline --notice 2027-01-15 --window 30
```

## Contents
- `SKILL.md` — three argument classes ranked, verdict bands, pitfalls, example session
- `references/appeal-procedure-reference.md` — evidence hierarchy, procedure, state deadline map, where to get every number, hearing script, cost-benefit, annual audit
- `scripts/ptax.py` — stdlib-only CLI (equalize / card / comps / timeline)
