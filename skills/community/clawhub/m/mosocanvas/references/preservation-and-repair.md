# Preservation and Repair

Load this file before modifying an accepted artifact or claiming that a repair preserved approved
content.

## Freeze checkpoints, not methods

- Keep the original and every user-approved checkpoint immutable.
- Give each candidate a parent reference and change reason.
- Record source dimensions and hash when available.
- Freeze approved decisions, relationships, and pixels where required; allow the execution method
  to change when evidence supports it.
- Do not confuse “latest” with “best.” Promote a candidate only after verification and user
  acceptance.

Repeated repair is valuable when it preserves decisions and produces measurable improvement.
Repeated full-frame synthesis is risky because a prompt-scoped request does not protect non-target
pixels. The correct control is lineage plus verification, not a universal repair-count limit.

## Choose the parent deliberately

Choose among:

1. **Last accepted checkpoint:** use when it is clean and the new change depends on its accepted
   improvement.
2. **Earlier clean checkpoint:** use when the latest branch accumulated non-target drift or when
   the new change is independent.
3. **Frozen Visual Spec:** regenerate a new branch when composition, material system, or subject
   must be rebuilt.

Chaining V2 into V3 is allowed when V2 is genuinely better, the next repair depends on it, and the
verification plan covers cumulative risk. Branch instead when the previous edit failed or added
unrelated damage.

## Route by operation and risk

| Operation | Preferred method | Default verification |
|---|---|---|
| exact text, logo, crop, color, size | deterministic layout/compositing | dimensions, glyphs, pixel bounds |
| remove or replace a local object | mask/region edit | mask preview, outside-mask comparison |
| local pose, light, or material | masked generative edit | semantic review plus protected-region drift |
| new composition or global material system | full regeneration from Visual Spec | spec-based visual review |
| uncertain locality | branch or handoff | state preservation as unverified |

For organic-surface artifacts, also load [texture-integrity.md](texture-integrity.md).

## Write a repair contract

```yaml
parent_ref: <immutable asset or accepted checkpoint>
target: <region, object, or property>
observed_problem: <fact, not causal speculation>
allowed_changes: [<specific properties>]
preserve: [<identity, pixels, text, layout, lighting, approved content>]
method: deterministic|masked-generative|full-regeneration|handoff
pass_conditions: [<observable checks>]
verification: pixel-diff|perceptual-diff|visual-only|user-judgment
```

Expand scope or attempt budget only after reporting why it is useful and what new risk it creates.

## Inspect at the right scales

1. **Use scale:** thumbnail, feed, poster distance, packaging shelf, or physical mockup.
2. **Detail scale:** 100%; use 200% for identity, hands, small type, logos, repeated patterns, or
   multi-round generative edits.

Record these separately:

- use-scale function;
- detail-scale technical risk;
- protected-region drift;
- trend versus the parent and earlier checkpoints.

A defect visible only at 200% is not automatically a product failure. Escalate when it affects the
real carrier, violates a production requirement, spreads across rounds, or predicts downstream
failure such as print enlargement.

## Verify preservation

When tools allow:

- compare dimensions, format, color mode, and alpha;
- compute changed-pixel bounds for lossless operations;
- compare protected pixels or perceptual distance with a declared tolerance;
- inspect semantic identity separately from pixel difference;
- store evidence with the source, candidate, and parent relationship.

Pixel equality is inappropriate after compression or color-profile conversion. Perceptual
similarity is not proof of exact preservation.

## Track quality debt

Use four states:

| State | Use scale | Detail scale | Trend | Decision |
|---|---|---|---|---|
| safe | passes | minor | stable | continue |
| watch | passes | visible risk | stable | continue with evidence |
| warning | weakening | material risk | worsening | branch or change method |
| block | fails | severe | spreading or damaging | stop this branch |

Do not promote a technically cleaner result that loses a more important identity, narrative,
hierarchy, or material quality.

## Stop or branch

Stop the current method when:

- hard constraints pass and the user accepts remaining tradeoffs;
- two consecutive rounds fail the predefined criterion;
- new damage appears outside the target;
- quality debt increases across accepted checkpoints;
- a deterministic tool, authoritative asset, or real selection is required but unavailable;
- the change has become a new direction rather than a repair.

Preserve useful checkpoints. Explain whether the next action is a new parent, a new method, a new
direction, or a handoff.
