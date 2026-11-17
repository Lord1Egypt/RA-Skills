# Midjourney quality benchmark

Treat Midjourney as a moving external target, not an execution dependency, prompt language, style
reference, or source of hidden inspiration.

## Benchmark two different things

### Curated ceiling

Sample dated images from Midjourney Explore `Top`/`Hot`, Spotlight, or other documented curated
surfaces. Use this lane to study the current ceiling in:

- immediate visual selection;
- composition and crop;
- authored specificity and originality;
- color/light integration;
- material coherence and selective detail;
- finish at carrier and detail scale.

This lane is not a matched-task comparison. It may reveal quality gaps but cannot prove that one
system follows the same brief better.

### Matched challenge

Use the same frozen brief, carrier, aspect ratio, output count, selection budget, and human-selection
policy for MoSoCanvas and the target system. Keep target artifacts unavailable to the direction and
generation context until MoSoCanvas outputs are frozen.

Only this lane may support a claim that MoSoCanvas matches or exceeds the target.

## Construct the benchmark set

- Record target version or visible generation metadata when available.
- Record collection surface, capture date, source URL, creator attribution, and rights status.
- Sample across at least five task classes: photographic scene, illustration, conceptual/editorial
  image, material/product image, and multi-image narrative or another declared domain.
- Include ordinary prompts and difficult failure probes; do not benchmark only spectacular fantasy.
- Keep a fixed hidden holdout set. Do not tune MoSoCanvas on every benchmark task.
- Refresh the target set monthly or after a material target-model update.

Do not download or redistribute images beyond authorized evaluation use. Store source references and
hashes when permitted.

## Run anonymous pairwise evaluation

For each comparison:

1. normalize display size, crop policy, and background;
2. hide source, model, prompt rhetoric, and self-review;
3. randomize left/right order;
4. ask for overall preference first;
5. then score composition, authored specificity, narrative, color/light, material coherence,
   AI residue, series rhythm, and carrier fit;
6. reveal source assignment only after the rating is committed.

Use independent human raters where possible. A fresh-context model reviewer may diagnose defects but
does not replace human aesthetic preference.

## Predeclare claims

Default minimum for a release benchmark:

- at least 5 task classes;
- at least 30 committed pair judgments;
- at least 5 independent raters;
- no remaining severity-3 defect disadvantage;
- `meets`: Wilson lower confidence bound at least 0.45 with a 5-point non-inferiority margin;
- `exceeds`: Wilson lower confidence bound above 0.50 and observed preference at least 0.60.

Count a tie as half a win for each side. Report task-level results so one easy category cannot hide
failure in another. These are operational release thresholds, not universal scientific constants;
change them only before a benchmark run.

Never claim `exceeds` from one hero image, a self-score, an unblinded panel, an unmatched curated
image, or an average that hides hard defects.

## Why this is aligned with the target

Midjourney documents image-aesthetics selection, Explore curation, and pairwise new-version rating
tasks. Its magazine selection also names clarity, originality, and composition. These practices
support using blinded preference plus craft diagnostics rather than trying to imitate a parameter
recipe.

Official sources checked 2026-07-28:

- https://docs.midjourney.com/hc/en-us/articles/33390759197197-Complete-Tasks
- https://docs.midjourney.com/hc/en-us/articles/33329460426765-Website-Overview
- https://docs.midjourney.com/hc/en-us/articles/28012940139021-Midjourney-Magazine-Subscription-FAQ
- https://updates.midjourney.com/high-res-rating/
- https://updates.midjourney.com/v8-1-is-now-the-default-model/
