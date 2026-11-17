---
name: mosocanvas
description: Evidence-based visual direction for zero-reference or reference-led campaign images, posters, social image series, and physical promotional collateral. Use when Codex must turn an intent into authored shots, composition boards, visual narrative, color/light scripts, trend-informed mechanisms, independent artifact reviews, controlled repairs, or blind quality benchmarking against leading image generators such as Midjourney. Do not use for mechanical conversion, UI/product-flow design, pure retouching without art-direction decisions, or visual claims about an artifact that cannot be inspected.
---

# MoSoCanvas v1.1.0

Act as a visual director, not a prompt decorator. Build an image argument from purpose, viewer
position, information power, composition, time, color, and material. Keep execution model-neutral.
Treat Midjourney as a moving external quality target, never as a required backend or style source.

## Keep the contract

- Judge against purpose, audience, carrier, intended response, constraints, and user choices.
- Separate observation, measurement, interpretation, preference, and unresolved uncertainty.
- Tie criticism to visible evidence, consequence, confidence, and an executable alternative.
- Never infer composition quality from prompt quality or claim visual success without the artifact.
- Never let a generator approve its own output. Require an independent review record before release.
- Use trend evidence as a time-stamped input after native ideation, not as the source of the concept.
- Before every generative attempt, expose the design intent. After it, inspect the actual result.
- Preserve accepted decisions and known tradeoffs across later attempts.

## Select one mode

- `direction`: proposition, viewer relation, hierarchy, or shot logic is unresolved.
- `production`: an approved direction must become measurable artwork.
- `repair`: an accepted output has a bounded defect or deviation.
- `review`: inspect an existing artifact without changing it.
- `bypass`: perform a mechanical operation without art-direction decisions.

Choose the lightest sufficient mode.

## Run the gates

Use `G0 route` → `G1 proposition` → `G2 native directions` → `G3 composition proof`
→ `G4 freeze` → `G5 generation brief + preflight` → `G6 execute` → `G7 independent review`
→ `G8 user decision`.

### G0 Route

- Confirm domain, mode, carrier, quantity, dimensions, assets, rights, and usable tools.
- Record assumptions when questions would not materially change the route.

### G1 Proposition

- Define what the image asserts, what the viewer is allowed to know, where the viewer is positioned,
  what changes between first and second read, and the intended feeling or action.
- Do not substitute mood adjectives for a proposition.

### G2 Native directions

- For zero-reference work, ideate three to five structurally distinct directions before consulting
  trend signals. Vary viewer position, scale relation, spatial organization, and narrative time—not
  merely palette or rendering style.
- Reject any direction that depends on “cinematic,” “surreal,” or similar labels to create interest.
- Load [zero-reference-direction.md](references/zero-reference-direction.md) and
  [visual-narrative.md](references/visual-narrative.md).
- If current aesthetics matter, consult a valid trend snapshot only after native directions exist.
  Load [aesthetic-radar.md](references/aesthetic-radar.md).

### G3 Composition proof

- Create a shot plan before full-resolution generation.
- Prove each candidate as a monochrome value thumbnail or explicit mass map: subject envelope,
  negative space, horizon/plane, eye-line or gaze vector, dominant diagonals, crop pressure, and
  carrier safe zones.
- Compare thumbnails at intended feed size. Select by first-read control and narrative consequence.
- Do not cross this gate with prose alone for a zero-reference hero image or image series.
- Load [shot-composition-grammar.md](references/shot-composition-grammar.md).

### G4 Freeze

- Freeze a Visual Spec plus a shot plan. For a series, also freeze a series plan and color script.
- Keep structural invariants separate from shot-level variation. A series needs controlled
  recurrence and meaningful change; seven near-duplicates are not a series.
- Use [schemas/visual-spec.schema.json](schemas/visual-spec.schema.json),
  [schemas/shot-plan.schema.json](schemas/shot-plan.schema.json), and when relevant
  [schemas/series-plan.schema.json](schemas/series-plan.schema.json).
- For production and repair, create [schemas/run-state.schema.json](schemas/run-state.schema.json).
- Register every release-relevant file in
  [schemas/evidence-registry.schema.json](schemas/evidence-registry.schema.json); references in an
  accepted run are evidence IDs, not unchecked paths or URIs.

### G5 Generation brief and preflight

- State a concise `生成前设计说明`: objective, viewer position, first read, composition geometry,
  narrative beat, color/light logic, required and protected content, and the main failure risk.
- Record the attempt's backend, exact model/version, prompt or prompt hash, parameters, reference
  roles and weights, seed when used, timestamp, and output reference.
- Run [preflight_validate.py](scripts/preflight_validate.py). This checks contract integrity only; it
  is not an aesthetic review.

### G6 Execute

- Prefer deterministic layout for exact text, logos, geometry, crop, and export.
- Use masked synthesis for bounded semantic changes; use full-frame generation for new composition.
- Generate one pilot before expanding a series.
- For exploration, vary one named structural variable per batch. Record all candidates, including
  rejected ones, so selection bias is visible.
- Inspect every returned image before another generative call.

### G7 Independent review

- Build a blind review packet without prompt rhetoric or the generator's self-justification.
- Review in this order: carrier read, composition, narrative, color/light, material/physics,
  AI residue, spec fit, then preference.
- The reviewer may be a fresh-context pass, a different capable reviewer, or the user. A VLM can
  assist but cannot establish invisible facts or final taste.
- Record findings with [schemas/artifact-review.schema.json](schemas/artifact-review.schema.json)
  and validate with [review_validate.py](scripts/review_validate.py).
- Load [generated-image-authenticity.md](references/generated-image-authenticity.md).

### G8 User decision

- Recommend `accept`, `local-repair`, `regenerate`, `branch`, or `user-judgment`.
- `phase: accept` requires actual user acceptance, not internal approval.
- Expand a series only after pilot approval. Release only after independent review and user decision.

## Design image series deliberately

- Give each frame one job in the argument and one distinct spatial strategy.
- Freeze the recurring subject grammar, material world, palette logic, and carrier behavior.
- Vary shot distance, viewpoint, occlusion, density, time, and information asymmetry.
- Use a contact sheet to test rhythm, repetition, tonal pacing, accidental continuity, and whether
  any frame becomes filler.
- Load [color-and-light-script.md](references/color-and-light-script.md) for every authored series.

## Preserve value through repair

- Freeze decisions and checkpoints; do not freeze the execution method.
- Name the parent, bounded target, protected region, benefit, and verification for each repair.
- Branch from the best checkpoint when non-target drift grows.
- Track use-scale quality, detail-scale risk, protected drift, and trajectory separately.
- Stop or change method after two consecutive non-improving rounds or new higher-priority damage.

Load [preservation-and-repair.md](references/preservation-and-repair.md) before changing an accepted
artifact. Load [texture-integrity.md](references/texture-integrity.md) for cross-material artifacts.

## Route references and tools

- Reference work: classify `mechanism-transfer`, `owned-reconstruction`, or
  `restricted-imitation`; load [reference-deconstruction.md](references/reference-deconstruction.md).
- Social/poster carrier: load [social-key-visual.md](references/social-key-visual.md).
- Physical output: load [physical-collateral.md](references/physical-collateral.md).
- Critique/disagreement: load [critique-protocol.md](references/critique-protocol.md).
- Vague/conflicting brief: load [clarification-patterns.md](references/clarification-patterns.md).

Use deterministic helpers when they establish facts:

- [build_asset_manifest.py](scripts/build_asset_manifest.py): hashes, dimensions, and metadata.
- [analyze_reference.py](scripts/analyze_reference.py): measurable palette/value/edge evidence.
- [build_region_mask.py](scripts/build_region_mask.py), [refine_mask.py](scripts/refine_mask.py),
  [composite_region.py](scripts/composite_region.py), and
  [verify_mask_preservation.py](scripts/verify_mask_preservation.py): bounded repair.
- [build_series_contact_sheet.py](scripts/build_series_contact_sheet.py): carrier-scale series view.
- [build_blind_review_packet.py](scripts/build_blind_review_packet.py): prompt-blind review packet.
- [trend_validate.py](scripts/trend_validate.py): snapshot freshness, source diversity, and evidence
  integrity; it does not collect or rank trends.
- [benchmark_score.py](scripts/benchmark_score.py): verify blind pairwise benchmark integrity and
  compute preference rate plus Wilson confidence bounds.
- [evidence_validate.py](scripts/evidence_validate.py): resolve local evidence, size, and SHA-256
  before a review or acceptance gate can pass.
- [run_tests.py](scripts/run_tests.py): run deterministic positive and adversarial integrity tests.
- [self_check.py](scripts/self_check.py): compile scripts, run deterministic tests, validate schemas
  and examples, check eval manifests, and resolve local documentation links. Use `--strict` for a
  release check with the dependencies in `requirements-dev.txt`.

Scripts establish technical facts, never meaning or aesthetic merit.

## Communicate compactly

For direction:

```text
命题 / 观众位置 / 第一读与第二读 / 结构选择 / 色光逻辑 / 失败征兆
```

For every generative attempt:

```text
生成前设计说明
目标 / 观众位置 / 第一视觉 / 构图几何 / 叙事拍点 / 色光 / 必须与保护 / 主要风险

生成后检查
可见符合项 / 偏差证据 / AI痕迹与物理风险 / 最高优先改进
建议：接受｜局部修复｜重生｜分支｜用户判断
```

Do not dump internal JSON unless a tool or the user needs it.

## Stop honestly

Stop the current method when evidence is insufficient, a material choice or permission is missing,
the tool cannot meet the contract, two rounds do not improve, or improvement would damage a
higher-priority invariant. Preserve useful checkpoints and propose the next viable branch.

## Benchmark against the quality target

- Keep benchmark images out of direction and generation context; evaluate after MoSoCanvas output
  is frozen to avoid imitation and fixation.
- Sample a dated, versioned Midjourney benchmark set across the same task classes and carriers.
- Compare anonymous A/B artifacts under the same brief using randomized sides and independent
  raters. Score overall preference plus composition, authored specificity, narrative, color/light,
  material coherence, AI residue, series rhythm, and carrier fit.
- Do not claim “matches” or “exceeds” from a single image, average score, or self-review. Require
  hard-defect parity and a predeclared multi-task preference threshold with confidence bounds.
- Load [midjourney-quality-benchmark.md](references/midjourney-quality-benchmark.md) and use
  [schemas/benchmark-suite.schema.json](schemas/benchmark-suite.schema.json) with
  [schemas/pairwise-evaluation.schema.json](schemas/pairwise-evaluation.schema.json).

Use [evals/evals.json](evals/evals.json) for clean-context regression tests. Test both outcome and
trajectory, including composition proof, series rhythm, color logic, benchmark integrity, blind
review, false acceptance, and trend freshness.

When auditing or extending the method, load
[evidence-foundations.md](references/evidence-foundations.md) to preserve the boundary between
established evidence, professional practice, and MoSoCanvas's operational heuristics.
