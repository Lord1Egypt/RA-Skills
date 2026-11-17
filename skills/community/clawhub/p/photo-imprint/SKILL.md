---
name: "photo_imprint"
version: "1.6.1"
description: "Photo Imprint (印痕) — 留住那张照片，只换一种笔触去记。Use when turning photos into a consistent illustrated social-media carousel (including 照片转手绘轮播): keep silhouette/proportions/anchors, redraw in watercolor. EXIF ordering, source-specific briefs, plan+sample gate, clean-plate normalization, deterministic composition, typed revisions, two-level QA, verified packaging."
source:
  repository: "locoda/photo-imprint-skill"
  ref: "main"
  provenance: "frontmatter-tracked per gh skill spec, travels with SKILL.md"
---

# Photo Imprint (印痕)

## Purpose
Keep the photo, remember it in a different stroke. 留住那张照片，只换一种笔触去记。Convert photos into one coherent illustrated carousel — keep silhouette, proportions, cap/lid, logo position, only the brushwork changes. `presets/travel-food-journal.json` supplies complete workflow defaults; actual subject plates still require a configured renderer and validated receipt. Eight style profiles in repo, 6 active: `watercolor-journal` (default), `blue-lavender-watercolor`, `highway-485-lithograph`, `sumi-e-ink`, `hiroshige-bokashi`, `seurat-conte` + 2 pending `botanical-watercolor`, `paper-collage`; each contributes only technique, never subjects. See `references/configuration.md` for overrides.

## Renderer contract — subject-only plate

**This section is blocking.** External renderers must output **subject-only plate**, not full scene.

- `contains_only: "subject"` — plate must contain only the photographed subject on transparent or isolated background. No table, no surface, no environment, no room, no landscape, no secondary props.
- ImageGen and similar tools ignore `background: transparent` — output remains RGB with background. You must explicitly **negate** environment in prompt: `NO table, NO surface, NO environment, NO room, NO background, NO ground, isolated subject on white, centered`.
- Passing original photo as image-to-image causes model to faithfully reproduce full composition — `prompt: "留白"` will fail. Must use negative environment + high `isolation` weight, or use segment-then-generate.
- Black-box tools that do not return model name: use `model=unspecified-by-tool` with `renderer-kind=external` and `external-service=<tool>` — allowed placeholder per 1.6.0.

If plate contains background, composition will produce rectangular blocks, seams, and non-uniform paper. Detect early in `clean_plate` empty-area noise.



### Architecture
Modular layers with invariants; weaker model executes without guessing.

- **Config layer:** `presets/travel-food-journal.json` + `profiles/styles/*.json` → `work/resolved-config.json` (SHA256). Single source of truth for canvas, paper, typography, style default, ordering, QA. Override only via explicit `--preset` and logged in resolved-config.
- **Plan layer:** `work/manifest.json` (EXIF-ordered) → `work/render-plan.json` → `work/production-plan.md` + `work/approval-state.json` + `work/sample-scope.json`. Contains `production_brief` per page and `sample_style_contract` 6-key frozen.
- **Gate layer:** 2.5 style gate mandatory before any render → `work/style_choice.json`; Step 3 sample gate 🔴 CHECKPOINT; Step 4 approval gate 🛑 STOP. No batch before approval.
- **Render layer:** `bin/renderer_receipt.py` → `bin/clean_plate.py` → `bin/compose.py`. Receipt validation blocks continuation; plates normalized per active style policy; composition deterministic with manifest binding config/plan/receipt/font/plates/pages.
- **QA layer:** `bin/qa_images.py` two dimensions independent: page-level compliance vs set-level cohesion. Both must pass before packaging.
- **Package layer:** `bin/package_verified.py stage + verify`. Hash-locks staged bytes, revalidates sources/captions/provenance/QA, writes `trusted-manifest.json` + `verify-report.json`.

Invariants (never violated):
1. EXIF order immutable; sample = first EXIF only.
2. Single-select style; no blending; style contract hash-locked into batch.
3. Sample generated image never becomes style reference.
4. Every rendered plate has validated receipt with consent flag.
5. Outputs contain no EXIF/GPS/XMP.
6. No invention of location/date/caption facts.

### Explicit Defaults (executable, no invention)
These values are the preset's truth, visible without opening JSON. If a project overrides, record the override in `work/resolved-config.json`; never invent a different value.

| Concern | Default Value | Executable Source |
|---|---|---|
| Canvas | 9:16 vertical, 1152×2048 px, deterministic | `composition.vertical-journal` |
| Paper | warm #F1EBDD, shared across set, 50% blank space minimum (sample shows #FAF6F0 warm) | `unification.warm-paper-journal` |
| Caption position | bottom-center, below subject, two lines `location` / `date`, `center_y_ratio=0.72`, `top_clear=0.55`, `edge_margin=0.07`, `min_clearance=0.08` | `composition.vertical-journal.caption_zone` |
| Caption typography | Noto Sans Light 30px at 1080px, #3B3832, textured serif fallback, EXIF-confirmed only | preset caption module |
| Style default | `watercolor-journal` loose observational line + transparent low-sat watercolor | `profiles.style = watercolor-journal` |
| Style alternatives | 8 profiles in repo: 6 active — `blue-lavender-watercolor`, `highway-485-lithograph`, `sumi-e-ink`, `hiroshige-bokashi`, `seurat-conte`, `watercolor-journal` (default) + 2 pending `botanical-watercolor`, `paper-collage` — each opt-in, single-select, no blending | `profiles/styles/*.json` |
| Order | EXIF capture_time ascending; fail closed if missing unless user authorizes draft | `workflow_defaults.ordering` |
| Sample gate | first EXIF page only before approval; generated sample never becomes style reference | `workflow_defaults.approval` |
| Renderer | no backend by default; validated receipt required for every output | `workflow_defaults.renderer` |
| QA | full-size + 360×640 phone scale, page-level + set-level separate | `workflow_defaults.qa` |
| Composition | 9:16 1152×2048, bottom-center, 55% top whitespace, 0.07 edge margin | `workflow_defaults.composition` |
| Plate pipeline | normalize → compose, profile-driven cleanup | `workflow_defaults.plate_pipeline` |
| Revision | feedback → revision-scope → re-compose | `workflow_defaults.revision` |
| Packaging | stage → verify → ZIP | `workflow_defaults.packaging` |

If any value above is absent in `work/resolved-config.json`, stop and rebuild config; do not substitute.

## Workflow

Each step lists exact Input, Output, and Command. No step runs without its listed Input existing. Every Output is hash-logged. Replace soft wording with imperative actions.

### 0. Preflight and inspect state

- **Input:** `requirements.txt`, `presets/travel-food-journal.json`, font file path from user
- **Output:** `work/preflight-report.json`, `work/env.json`
- **Command:** `python3 bin/check_environment.py [--config work/resolved-config.json --font <font-file>]`

Install `requirements.txt`, run check. Typography requires explicit readable font file; never substitute silently. `python3 bin/workflow.py --project <project-dir> status|next` reports state without writing or bypassing a gate.

If preflight fails → install declared dependency or supply configured font, then rerun preflight. Do not continue with failed preflight.

### 1. Resolve and preprocess

- **Input:** `presets/travel-food-journal.json`, `<photos>` with EXIF
- **Output:** `work/resolved-config.json` (SHA256 logged), `work/manifest.json` (EXIF-ordered items)
- **Command:** 
```bash
python3 bin/resolve_config.py --preset presets/travel-food-journal.json --output work/resolved-config.json
python3 bin/preprocess.py --input <photos> --output work/manifest.json --config work/resolved-config.json
```

Order by EXIF. Stop on missing factual metadata unless user explicitly authorizes draft mode. Never invent captions, dates, locations, or page-specific subject decisions.

If EXIF missing → write `work/manifest.json` with `missing_exif: true`, notify user with file list, wait for explicit `draft authorized` message, then rerun with `--allow-draft`. If user denies → stop, do not guess.

### 2. Complete the plan inputs

- **Input:** `work/resolved-config.json`, `work/manifest.json`
- **Output:** `work/render-plan.json`, `work/production-plan.md`, `work/approval-state.json`, `work/sample-scope.json`
- **Command:**
```bash
python3 bin/build_render_plan.py --config work/resolved-config.json --manifest work/manifest.json --output work/render-plan.json
python3 bin/build_production_plan.py --render-plan work/render-plan.json --output work/production-plan.md --state-output work/approval-state.json
python3 bin/render_scope.py --render-plan work/render-plan.json --state work/approval-state.json --mode sample --output work/sample-scope.json
```

For every page, fill required `production_brief` JSON:
```json
{
  "subject_priority": "starbucks small cup on tray",
  "thumbnail_read": "small cup must read at 360px",
  "preserve_anchors": ["red logo position", "lid shape", "cup height ~50% blank"],
  "abstract_or_omit": ["background crowd", "stray shadows"],
  "material_depth_cues": ["glass transparency", "paper grain"],
  "structural_lines": [{"element": "counter edge", "operation": "retain_but_simplify"}],
  "forbidden_inventions": ["road", "mountain", "invented logo"]
}
```
Confirm `sample_style_contract` with 6 mandatory keys:
```json
{
  "mark_edge_quality": "soft dry-brush, no hard outline",
  "negative_space_rules": "50% paper-white minimum, no fill",
  "fill_tonal_rules": "transparent wash, cool blue-lavender grouping",
  "background_cleanliness": "no texture, no invented scenery",
  "frame_border_policy": "no border, no seam",
  "abstraction_level": "simplify 40%, keep anchors",
  "generated_page_is_style_reference": false
}
```

If any `production_brief` field empty → rebuild that page entry from source photo, do not fabricate. If `sample_style_contract` missing a mandatory field → stop, list missing keys, wait for user or profile fix.

### 2.5 Style Selection Gate — 🔴 CHECKPOINT

- **Input:** `assets/samples/*.webp` (5 thumbnails), `profiles/styles/*.json`
- **Output:** `work/style_choice.json` (SHA256), updated `work/resolved-config.json`, `work/sample_style_contract.json`
- **Command:** `python3 bin/resolve_config.py --preset <preset-with-style> --output work/resolved-config.json` after choice

**This gate is mandatory before any render.** Do not render until this gate passes.

1. List 5 bundled style thumbnails from `assets/samples/`:
   - `style-sumi-e-cup.webp` (sumi-e-ink) — sparse ink line, pale wash, 60% blank
   - `style-hiroshige-bokashi-cup.webp` (hiroshige-bokashi) — flat color block, bokashi gradation, woodblock texture, no rain lines
   - `style-seurat-conte-cup.webp` (seurat-conte) — no hard contour, Conte hatching, paper highlight
   - `blue-lavender-watercolor/reference.webp` — transparent wash, cool grouping
   - `highway-485-lithograph/reference.webp` — broken contour, paper-white negative
2. Present them in one message with technique description and blank-space rule for each.
3. State default: `watercolor-journal` (or `blue-lavender-watercolor` for food-journal preset) and why.
4. If user says "你定 / 不懂 / 随便" → use default, render sample immediately, and record `style_choice.json`:
```json
{"selected": "watercolor-journal", "user_delegated": true, "timestamp": "2026-08-30T19:45:00Z", "alternatives_shown": 5}
```
5. If user picks one → record `work/style_choice.json`:
```json
{"selected": "hiroshige-bokashi", "user_delegated": false, "timestamp": "...", "alternatives_shown": 5}
```
6. Write selected style into `work/resolved-config.json` and freeze into `work/sample_style_contract.json`.

If user asks for style blending → reject: "单选其一，不混合。重选一个。" If user uploads private reference without external-processing consent → store locally only, do not upload, ask for explicit consent naming external service.

No render before `work/style_choice.json` exists. Violation = fail closed.

### 3. Render, normalize, and discuss only page one — 🔴 CHECKPOINT

- **Input:** `work/production-plan.md`, `work/sample-scope.json`, `work/style_choice.json`, font file
- **Output:** `work/renderer-receipt-sample.json`, `work/plates/sample-clean.webp`, `work/samples/page01-1080x1920.webp`, `work/last-step.md`
- **Command:**
```bash
python3 bin/renderer_receipt.py --mode sample --config work/resolved-config.json --scope work/sample-scope.json --output work/renderer-receipt-sample.json
python3 bin/clean_plate.py --input work/plates/sample-raw.webp --style <selected> --output work/plates/sample-clean.webp
python3 bin/compose.py --config work/resolved-config.json --plan work/render-plan.json --receipt work/renderer-receipt-sample.json --font <font-file> --output work/samples/page01-1080x1920.webp
```

Render only the first EXIF page. Register and validate receipt containing:
```json
{"kind": "replicate|local", "model": "sdxl-1.0", "version": "abc123", "seed": 42, "settings": {"steps": 30}, "source_hashes": ["sha256..."], "reference_hashes": ["sha256..."], "output_hashes": ["sha256..."], "consent": {"external_processing": false}}
```
A `not-configured` receipt is an honest blocker, not permission to continue.

The Markdown plan must exist. Send it as artifact or faithful summary with all 6 contract fields, always together with sample. Record mode with `review_gate.py mark-shown`. See `references/review-gate.md`.

**Step notification required:** after this step, send message containing:
- `work/production-plan.md` (artifact or 200-char faithful summary with all 6 contract fields)
- `work/sample-scope.json` hash
- first composed sample image (1152×2048)
- next step: "等待你批准第1张样张，批准后才渲染 2..N"

If renderer not configured → stop, report `renderer_receipt.status=not-configured`, do not fabricate output, do not claim batch exists.

### 4. Record explicit approval and batch — 🛑 STOP

- **Input:** user exact approval message string, `work/approval-state.json`
- **Output:** `work/approval-state-approved.json`, `work/batch-scope.json` (pages 2..N), `work/last-step.md`
- **Command (actual CLI):**
```bash
python3 bin/review_gate.py approve --state work/approval-state.json --approval-text "<exact user message>" --explicit-user-approval
python3 bin/render_scope.py --render-plan work/render-plan.json --state work/approval-state-approved.json --mode batch --output work/batch-scope.json
```

Copy user's exact approval message into approve. Batch scope contains pages 2..N only. Propagate frozen sample style contract into every page prompt. Use only original approved references; never use page one as style reference.

**Lock rule:** batch prompts must hash-lock:
- `work/style_choice.json` SHA256
- `work/sample_style_contract.json` SHA256
- `work/render-plan.json` style_reference_locks
- source hashes for pages 2..N

If any lock mismatches → discard batch scope, rebuild plan, return to sample gate. If user changes style after approval → invalidate approval, return to 2.5 gate.

**Step notification:** after approval recorded, send "已锁定样张契约，开始批量 2..N，共 N-1 张，风格 <id> 已冻住" with `work/batch-scope.json` page list.

### 5. Normalize plates and compose deterministically

- **Input:** `work/batch-scope.json`, `work/renderer-receipt-batch.json`, raw plates
- **Output:** `work/plates/*.clean.webp` (normalized), `work/composed/*.webp`, `work/composition-manifest.json`, `work/last-step.md`
- **Command:**
```bash
python3 bin/renderer_receipt.py --mode batch --config work/resolved-config.json --scope work/batch-scope.json --output work/renderer-receipt-batch.json
python3 bin/clean_plate.py --batch work/batch-scope.json --style <selected> --output-dir work/plates/
python3 bin/compose.py --config work/resolved-config.json --plan work/render-plan.json --receipt work/renderer-receipt-batch.json --font <font-file> --output-dir work/composed/
```

Use active style's profile-driven cleanup policy. Watercolor/pale media and opaque collage must not be treated like line art. Register full-set receipt whose source/reference sets exactly match approved plan and whose outputs hash-lock every normalized plate; record per-page seeds when needed. Apply shared paper, placement, typography, route, markers, watermark, disclosure only after clean plates pass. `compose.py` writes manifest binding config, plan, receipt, font, plates, final pages.

If plate normalization fails (alpha missing for `alpha-required`, or paper-key removes subject) → regenerate plate with corrected policy, do not color-key aggressively, rerun compose.

**Step notification:** after compose, send contact sheet 3×3 + list of 9:16 outputs, state "已合成，待双维 QA".

### 6. Review two independent acceptance dimensions

- **Input:** `work/composed/*.webp`, `work/render-plan.json`, `work/resolved-config.json`
- **Output:** `work/qa-report.json`, `work/review-checklist.json`, `work/last-step.md`
- **Command (actual CLI):**
```bash
python3 bin/qa_images.py --input work/composed/ --output work/qa-report.json --config work/resolved-config.json --render-plan work/render-plan.json --plates work/plates/ --checklist-output work/review-checklist.json
```

Run QA. Open every final page at full size and phone scale, not only contact sheet.

- **Page-level compliance:** each page satisfies its own production_brief, source fidelity, material/depth cues, structural-line operations, background cleanliness, border/seam policy.
- **Set-level cohesion:** ordered set passes shared paper, style, typography, rhythm, dimensions, overall visual unity.

Record evidence and validate `review-checklist.json`. Packaging blocked unless both dimensions pass. See `references/quality-checks.md`.

If QA fails → fix causal layer (plate, prompt, or composition), not cosmetic patch, rerun QA on current staged bytes.

**Step notification:** send QA summary with per-page pass/fail and set cohesion verdict.

### 7. Handle post-approval feedback without overcorrection

- **Input:** user feedback string, `work/review-checklist.json`
- **Output:** `work/revision-scope.json`, updated plates/composed if needed, `work/last-step.md`
- **Command (actual CLI):**
```bash
python3 bin/revision_scope.py --render-plan work/render-plan.json --state work/approval-state.json --staging-manifest work/composition-manifest.json --changes '{"changes":[]}' --request-text "<exact user text>" --impact page-local --output work/revision-scope.json
# or --impact sample-style-system when touching sample/style/shared/source-order
```

For non-sample page-local corrections, create changes using only: `remove`, `retain_but_simplify`, `add_as_secondary`, `preserve_unchanged`. Scope marks only affected pages stale and hash-locks unchanged approved pages.

Any change to page one, style contract/reference, source/order, shared layout, or system plan invalidates batch approval and returns to plan+sample gate.

If revision touches gate-reset domains (`sample`, `style-reference`, `shared-system`, `source-order`) → invalidate approval, notify user, return to 2.5.

### 8. Stage, package, and deliver

- **Input:** `work/composed/*.webp`, `work/review-checklist.json`, `work/composition-manifest.json`
- **Output:** `work/staged/` (numbered 01..N), `work/package.zip`, `work/package-manifest.json`, `work/trusted-manifest.json`, `work/verify-report.json`
- **Command (actual CLI):**
```bash
python3 bin/package_verified.py stage --input work/composed/ --output work/staged/
python3 bin/package_verified.py package --input work/composed/ --staging-manifest work/composition-manifest.json --review-checklist work/review-checklist.json --state work/approval-state.json --composition-manifest work/composition-manifest.json --output work/package.zip --manifest-output work/trusted-manifest.json
python3 bin/package_verified.py verify --zip work/package.zip --manifest work/trusted-manifest.json
```

Lock staged numbered images; rerun QA against exact stage and approved config/plan; package with composition manifest only after checklist validation; then verify. Packaging revalidates current sources, confirmed captions, renderer/plate provenance, QA input locks, review evidence, exact staged bytes. Artifact delivery copies verified staged outputs and must not regenerate images.

If staging hash mismatch → discard checklist, review current staged bytes, restage.

## Step Notification Contract

Every workflow step must notify user and show intermediate product. No silent step.

Each notification writes `work/last-step.md` with:
```
## Step N: <name>
Completed: 2026-08-30T19:45:00Z
Inputs: resolved-config.json:abc123, manifest.json:def456
Outputs: render-plan.json, production-plan.md, approval-state.json, sample-scope.json
Next: Run 2.5 style gate, show 5 thumbnails
Needs user: yes
Command: python3 bin/build_render_plan.py --config ... --output ...
```

And sends chat message with file list + thumbnail if image. Include SHA256 of key outputs.

Missing notification = workflow violation → rerun `workflow.py status` and send missing `last-step.md`.

## Failure Handling — Explicit Failure Mode Matrix

Fail closed always. No silent substitution. Repair causal stage only. Every row lists detection, action, recovery, notification.

| Code | Trigger | Detection | Action (fail closed) | Recovery | Notification |
|---|---|---|---|---|---|
| F-ENV | `requirements.txt` missing or font unreadable | `check_environment.py` exit !=0, `preflight-report.json.status=failed` | stop before Step1, do not invent dependency | install declared dependency / supply explicit font path, rerun preflight | send `preflight-report.json` with failed field list |
| F-EXIF | any photo missing capture_time/location/date | `preprocess.py` sees EXIF absent → `manifest.json.missing_exif=true` | write manifest with flag, do not guess | wait for user message exactly `draft authorized`, rerun with `--allow-draft`; if denied → stop | send missing file list, wait |
| F-FONT | typography file unreadable or substitution attempted | `check_environment.py` font readability check fails | stop, report font path | user supplies valid font path | send font path error, block compose |
| F-RENDERER | renderer not configured | `renderer_receipt.py` returns `status=not-configured` | stop at render scope, do not fabricate receipt or claim output | user configures renderer backend, rerun receipt | send `renderer-receipt.json` with not-configured |
| F-STYLE-MISSING | `work/style_choice.json` absent | gate check `style_choice.json` not exists | return to 2.5 gate, block any render | run 2.5 gate, show 5 thumbnails, record choice | send "风格未选，回 2.5 门" |
| F-STYLE-BLEND | user asks blend 2+ styles | message contains blend intent | reject | prompt "单选其一，不混合。重选一个。" | send rejection with single-select rule |
| F-BRIEF-EMPTY | `production_brief` any field empty | `build_render_plan.py` validation fails | stop, do not fabricate subject | rebuild that page entry from source photo | list empty field names |
| F-CONTRACT-INCOMPLETE | `sample_style_contract` missing mandatory key | contract validation missing key in 6-key set | stop, list missing keys | user or profile fixes missing key | send missing key list |
| F-RECEIPT-INVALID | receipt missing kind/model/version/seed/settings/hashes/consent | `renderer_receipt.py` validation fails | discard receipt, block compose | regenerate receipt with full fields | send invalid field list |
| F-SOURCE-HASH | source photo hash changed vs manifest | `package_verified.py` source hash mismatch | discard batch scope, rebuild plan, return to sample gate | rebuild manifest from current sources | send hash diff, return to gate |
| F-REFERENCE-HASH | style reference hash changed vs approved locks | reference hash mismatch in `render-plan.json` locks | invalidate approval, return to 2.5 | re-approve reference or select new style | send reference hash diff |
| F-PLATE-ALPHA | plate requires alpha but alpha missing | `clean_plate.py` alpha-required check fails | regenerate plate with correct policy, do not color-key aggressively | switch to alpha-preserving normalization | report plate id + policy switch |
| F-PLATE-PAPER-KEY | paper-key removes subject | paper-key subject erosion detected | regenerate plate, do not color-key aggressively | use subject-aware key | report plate id |
| F-QA-PAGE | page fails production_brief, fidelity, material cue, background, border | `qa_images.py` page-level fail | fix causal layer (plate/prompt/composition), not cosmetic patch, rerun QA on current bytes | if 2nd failure → switch normalization policy and report | send per-page fail reason |
| F-QA-SET | set fails paper/style/typography/rhythm/dimension unity | `qa_images.py` set-level fail | fix shared system layer | adjust shared paper/typography/layout | send set fail reason |
| F-STAGING-MISMATCH | staged bytes hash != manifest | `package_verified.py verify` hash mismatch | discard checklist, review current staged bytes, restage | restage from current composed | send hash mismatch |
| F-APPROVAL-INVALIDATED | user changes style, source, order, shared layout after approval | approval-state lock check fails | invalidate approval, return to 2.5/3 gates | re-run plan+sample review | notify "批准已失效，回 2.5" |
| F-USER-REJECT-SAMPLE | user rejects sample | approval-state rejection reason recorded | update production_brief or style_choice, rerender sample only, do not batch | rerender sample with corrected brief | send rejection reason |
| F-PRIVATE-CONSENT | private reference without external consent | consent flag `external_processing=false` but upload attempted | store locally only, do not upload | ask for explicit consent naming service | send consent request |
| F-DIMENSION | output not 1152×2048 9:16 | QA dimension check fails | objective fail cannot be overridden by manual pass | fix compose canvas | report dimension actual vs expected |
| F-CAPTION-UNCONFIRMED | caption not EXIF-confirmed | caption source != EXIF | block compose | supply EXIF-confirmed caption or omit caption | send caption source error |

Manual review decides semantic and aesthetic checks only; it never overrides machine-verifiable failures listed above. Second failure on same code → escalate: switch policy + report full evidence.

## Dangerous Actions & Blacklist (Do Not Do)

This skill must never:

- invent location, date, caption facts, or page subject decisions from style reference;
- use generated sample page as style reference for batch (sample is evidence only);
- blend 2+ styles implicitly; single-select only;
- upscale or change proportions of small subjects (e.g., small cup becomes large mug) — preserve anchors and ~50% blank space;
- render pages 2..N before explicit user approval message copied via `review_gate.py approve`;
- upload private user photos or private style references to external image service without explicit consent naming that service;
- claim consistency, transparency, or QA success without opening actual outputs;
- bypass `renderer_receipt` validation or fabricate a receipt;
- write final images with EXIF, GPS, or XMP metadata;
- silently substitute font, paper, or 9:16 dimensions;
- add logos, text overlays, hands, fabric, or reference painting subjects into output;
- treat local storage consent as external-processing consent.

If any blacklist action is requested → refuse, explain why, offer allowed alternative.

## Output Contract
- `production-plan.md` always exists before the first render.
- `work/style_choice.json` exists before any render, with `selected`, `user_delegated`, `timestamp`, `alternatives_shown` fields.
- `work/last-step.md` exists after every step and is sent to user, containing Completed, Inputs with hashes, Outputs, Next, Needs user, Command.
- Before explicit approval, only the first EXIF page is renderable.
- The approved visual method is structured, hash-locked, and propagated to batch prompts; batch prompts contain frozen `style_choice` and `sample_style_contract` hashes.
- Plates are normalized/validated under the active style policy.
- Every page and the set pass separate evidence-bearing QA gates with `qa-report.json` and `review-checklist.json`.
- Page-local revisions preserve unchanged approved pages with hash-locks.
- Objective failures such as wrong dimensions, invalid plates, severe seam/frame/background diagnostics, changed source hashes, or review/staging hash mismatches cannot be overridden by manual `pass` entries.
- Every rendered plate has a validated renderer receipt with kind, model, version, seed, settings, source/reference/output hashes, and consent flag; an unconfigured renderer is reported as unavailable, never simulated.
- Deterministic outputs and packaged files contain no EXIF, GPS, or XMP metadata.
- The ZIP contains only verified staged files plus its release manifest; verification also requires the separately written trusted manifest sidecar and `verify-report.json`.

## Operating Rules
1. Keep style separate from subject; reference images contribute techniques, never objects.
2. Keep private references local and out of delivery/version control unless rights permit.
3. Do not claim consistency, transparency, or QA success without opening the actual outputs.
4. Fix the causal layer, not a cosmetic patch.
5. Preserve user authority over plan, sample, revisions, and approval.
6. Keep reusable watermark defaults off; names, handles, and marks are project overrides, never universal defaults.
7. Treat local storage of a private reference and transmission to an external image service as separate permissions. Never upload a private reference without explicit external-processing consent.
8. Lock approved style contract into batch; never drift style across pages.
9. Notify every step with intermediate product; never run silently.
10. Every step lists Input, Output, Command; no soft wording; no invention.
11. Fail closed on any code in Failure Matrix; second failure escalates with policy switch and full evidence.
12. Architecture invariants 1-6 are non-negotiable; any violation invalidates approval and returns to gate.
