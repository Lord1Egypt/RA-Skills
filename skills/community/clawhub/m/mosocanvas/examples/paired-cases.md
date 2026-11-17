# Paired Cases

Use these cases to calibrate behavior, not to copy their visual directions.

## Reference-led social poster

**Input:** “I like these blue-and-pink retro illustrations. Make a MoSoCanvas promotion image.”

**Weak response:** “Great style. I will use blue, pink, neon, and a retro studio.”

**Why it fails:** It extracts a color cliché, not the shared mechanisms. It tends to produce a clean generic AI-retro image.

**MoSoCanvas response:** Identify analog ink density, fine grain, dark silhouette mass, restricted practical coral light, detailed linework, generous blue negative space, and quiet everyday tension. State what not to copy: the diner, car, coast, or exact composition. Freeze two or three mechanisms before generating.

**Pass evidence:** The output remains tactile without outlining every edge in neon, and no reference subject or layout is reproduced.

## Unknown brand versus mature-brand restraint

**Input:** “The small sign is elegant, but nobody knows our product. The name must be visible in the thumbnail.”

**Weak response:** Enlarge the environmental sign slightly while protecting the original restraint.

**Why it fails:** It treats mature-brand subtlety as a universal aesthetic rule and ignores acquisition context.

**MoSoCanvas response:** Separate atmosphere from recognition. Keep a small in-scene sign as discovery, and add a large editorial title in available negative space as the first-read layer. Test the name at thumbnail scale.

**Pass evidence:** Brand name is readable at approximately 160 px width while the scene remains the emotional second read.

## Portrait typography and recursive drift

**Input:** “Keep this hooded portrait. Change only the title from ivory-red to a cold-blue / alert-red treatment.”

**Weak response:** Send the previous generated edit back through a full image model twice and report that only typography changed.

**Why it fails:** The face and fabric can be re-synthesized. Repeated fingerprint-like skin texture may appear only at 100% zoom.

**MoSoCanvas response:** Return to the immutable approved portrait. Recolor or rebuild the title with deterministic compositing. Protect the portrait region, compare changed-pixel bounds, and inspect skin at 100–200%.

**Pass evidence:** Protected portrait pixels are unchanged for a lossless operation; all changed pixels fall inside the title region.

## Organic surface texture pathology

**Input:** “The poster works, but the man's skin has faint terrain or maze lines. Fix only that.”

**Weak response:** Send the approved full frame through another image edit with a longer list of
negative texture words, then accept it because the thumbnail looks clean.

**Why it fails:** Prompt scope is not a mask. High-fidelity input conditioning can preserve and
elaborate the existing texture, while a visually attractive full frame hides the failure at normal
review size.

**MoSoCanvas response:** Classify the visible network as a technical
`surface_texture_hallucination`. Freeze the last clean checkpoint, inspect matched torso and hand
crops at use scale and 100–200%, and route the skin only to masked synthesis or deterministic
retouching. Record use-scale impact, detail-scale risk, coverage, and trend separately. Continue
repairing while a named checkpoint improves and protected content remains stable; branch or change
method after two consecutive non-improving rounds.

**Pass evidence:** Skin reads as the intended material at use scale; close inspection shows sparse,
irregular microvariation within the declared tolerance; anatomy and protected content remain
intact; the trend is stable or improving.

## Multi-round frozen repair

**Input:** “The last three local fixes improved the cat, helmet, and title. Keep repairing, but do
not lose what has already been approved.”

**Weak response:** Refuse because a universal repair-count limit has been reached.

**Why it fails:** It mistakes repair count for risk and discards the value of frozen checkpoints.

**MoSoCanvas response:** Keep every approved checkpoint immutable. Name the best parent for the next
change, explain whether the new repair depends on the latest version, bound the target, and verify
both the new benefit and cumulative non-target drift. Continue if the trajectory improves; branch
from an earlier checkpoint when the latest version carries avoidable quality debt.

**Pass evidence:** Each accepted round has a parent, change reason, protected-elements check, and
use/detail-scale comparison. No universal count cap is imposed.

## Low-status corporate tote brief

**Input:** “White tote, red straps, Huizhou front, insurance logo and anti-fraud slogan on the back. Make it less low.”

**Weak flattering response:** “This has great potential; add elegant Huizhou motifs.”

**Weak sharp response:** “Corporate giveaways are inherently cheap.”

**MoSoCanvas response:** The brief is not the failure. Motif stacking, equal hierarchy, oversized warning copy, and default bold type would create the giveaway look. Use one structural Huizhou mechanism such as courtyard negative space; keep the official logo small; turn the required slogan into restrained bilingual editorial typography; use a small seal only if its language and cultural form are authoritative.

**Pass evidence:** Required information remains exact and legible, the front has one coherent cultural mechanism, and the print can be produced with limited inks.

## Approved mockup to production master

**Input:** “This tote mockup is approved. Produce the print files and only add the anti-fraud
footer.”

**Weak response:** Treat the mockup as a loose style reference, redraw the Huizhou illustration,
replace its single-line typography with a new two-line headline, and report that the visual
language was preserved.

**Why it fails:** It changes approved relationships while confusing visual similarity with
checkpoint fidelity.

**MoSoCanvas response:** Select `production` mode. Record the mockup as `approved-mockup` with path,
dimensions, and hash. Freeze illustration geometry, front/back hierarchy, logo relationship,
headline line count, and seal position. Set the footer as the only allowed addition. Rebuild exact
text and official assets deterministically, then compare the production proof with the checkpoint
before delivery.

**Pass evidence:** The approved relationships remain within the declared comparison tolerance, the
new footer is the only intentional difference, and unresolved production assets are explicitly
flagged.

## Intentional roughness

**Input:** “I want a deliberately rough punk poster with torn type and misregistration.”

**Weak response:** Correct all alignment and texture because they violate design rules.

**MoSoCanvas response:** Roughness is not the error. Check whether every element breaks order at equal intensity. Preserve torn type and misregistration; stabilize one information anchor unless unreadability itself is the confirmed proposition.

**Pass evidence:** The result makes intentional disorder distinguishable from accidental noise.

## Non-trigger: mechanical conversion

**Input:** “Convert this approved PNG to WebP at the same dimensions.”

**Correct behavior:** Bypass MoSoCanvas diagnosis and perform the mechanical operation with normal file validation.

## Existing output without image access

**Input:** “Check whether the logo is too small,” but no image is available.

**Correct behavior:** State that the real output has not been seen. Ask for the image or provide a hypothetical check; do not invent coordinates or a pass/fail result.
