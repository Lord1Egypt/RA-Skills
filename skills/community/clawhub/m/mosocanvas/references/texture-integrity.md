# Texture Integrity

Load this file when skin, fabric, fur, foliage, liquid, or another material has passed through
reference transfer or repeated generation/editing, or when the user reports maze-, fingerprint-,
scale-, polygon-, topographic-, or over-sharpened texture.

## Classify what is visible

Use `technical`, not `preference`, when a repeated surface motif contradicts the intended material.
Record:

```text
surface_texture_hallucination/<pattern-class>
```

Useful classes: `maze-topographic`, `fingerprint`, `polygon-cell`, `scale-like`,
`over-sharpened-pore-field`, and `cross-material-homogenization`.

`cross-material-homogenization` applies when skin, fabric, hard surfaces, liquid, or negative space
collapse into a related etched, faceted, scaly, or directional rendering language. The marks need
not be pixel-identical; the failure is loss of material distinction.

## Separate observation from cause

High-confidence observations include location, continuity, repetition, line width, material
coverage, viewing scale, and change across versions.

Causal claims require controlled comparison:

- stronger after using an edited image as the next parent supports edit anchoring or cumulative
  re-synthesis;
- stronger with a textured reference and weaker in a text-only branch supports reference transfer;
- stronger only with weathering, extreme-detail, or lighting variants supports prompt interaction;
- recurrence in a neutral text-only control shows that neither contaminated input nor negative
  pathology words are necessary.

Do not call inference-time drift “model collapse.” Do not name a model-internal cause from one
output. Treat repeated generative editing as a risk factor, not proof that freezing or multi-round
repair itself is wrong.

## Inspect three scales

1. **Use scale:** judge the real carrier and viewing distance.
2. **Detail scale:** inspect 100–200% when identity, print enlargement, or repeated editing makes
   microstructure consequential.
3. **Material scale:** inspect at least three different materials and one region outside the
   reported target.

Natural material variation is irregular, locally variable, and non-continuous. Pathology forms a
recognizable network or repeated directional field.

Whole-image edge density is not proof of repair. Prefer:

- matched crops at identical transforms;
- human severity `0 pass` to `3 blocker`;
- continuity, closed-loop, or patch-repetition evidence;
- protected-region pixel/perceptual comparison when valid;
- a material matrix for skin, fabric, hard surface, liquid, and negative space.

## Judge impact and trend separately

Record:

- `use_scale`: pass, risk, or fail;
- `detail_scale`: pass, risk, or fail;
- `trend`: improving, stable, or worsening;
- `coverage`: local, one material, or cross-material;
- `user_judgment`: accepted, rejected, or pending.

A faint detail-scale trace may be acceptable when the real carrier passes and the trace remains
stable. Escalate when it becomes visible at use scale, spreads, intensifies across rounds, destroys
material distinction, or violates an explicit production requirement.

## Route repair without disabling iteration

Use the lowest-risk method that can plausibly improve the defect:

1. deterministic frequency or texture retouching inside a reviewed material mask;
2. masked or region-scoped synthesis from the best accepted checkpoint;
3. a new branch from an earlier clean checkpoint;
4. clean regeneration from the frozen Visual Spec when contamination is global.

Multiple repairs are allowed. Every round needs a named parent, bounded target, pass condition, and
trend comparison. Do not use a failed texture repair as the next parent unless the user explicitly
accepts the tradeoff and the next operation depends on it.

Pattern removal is necessary but not sufficient. Reject a smoother result when anatomy, material,
lighting, identity, hierarchy, or protected content becomes worse.

## Use a small benchmark when the cause matters

Before spending more full-composition attempts, generate a small controlled set that keeps subject,
pose, framing, and medium stable while changing one factor at a time, such as:

- neutral versus weathered surface language;
- ordinary versus extreme detail;
- diffuse versus dramatic light;
- clean text-only generation versus reference-conditioned editing.

Keep pathology terms in the evaluator rather than every generation prompt. One sample per condition
can guide routing but cannot establish a population-level cause.

If a neutral control still shows a faint pattern but passes at use scale, record it as a model/tool
risk rather than an automatic blocker. If the requirement is strict large-format or close-detail
skin, change the model/tool route, use an authorized photographic base, or change the concept's
material requirement.

## Pass conditions

A repair or branch passes only when:

- the intended material works at the real carrier;
- detail-scale risk is within the declared tolerance;
- anatomy and broad light planes remain coherent;
- repaired material matches adjacent protected regions;
- non-target content and dimensions pass their checks;
- the trend is stable or improving;
- the user accepts any remaining subjective tradeoff.
