# Creative Guidelines

Use these standards for every production request.

## 1) Narrative first

- Start with one sentence: "Who is this for and what action should they take?"
- Build arc: Hook -> Problem/Desire -> Solution -> Proof -> CTA.
- Keep one dominant message per scene.

## 2) Visual consistency system

- Lock style variables early: color palette, lens style, lighting mood, typography tone.
- Reuse anchor references (product angle, mascot, character wardrobe, set design).
- For iterations, keep style keywords stable and only change one dimension at a time.
- Generate all scene images with shared style cues in the prompt.

## 3) Asset strategy

- Generate a reusable still kit first with `pixcli image` (hero, alt angle, background, detail close-up).
- Use `-n 4` to generate variations and pick the best.
- Use `--search` when real-world accuracy matters (correct logos, real product designs, current branding). Only works with Nano Banana models.
- Use `--from` with multiple reference images to blend styles or combine elements into new creations.
- Edit/upscale winners with `pixcli edit` before compositing.
- Keep transparent PNG variants (`-t`) for Remotion compositing.

## 4) Motion strategy

- Use `pixcli video --from` for short hero moments (3-8s). Use Remotion for deterministic text, transitions, captions.
- Combine both: generate a 5s hero clip with `pixcli video`, then composite it in Remotion with text overlays and branding.
- Avoid overusing camera motion; reserve strong movement for key beats.

## 5) Audio strategy

- Generate voiceover with `pixcli voice`, music with `pixcli music`, SFX with `pixcli sfx`.
- Use `--audio` on `pixcli video` for native audio generation (BGM, SFX, dialogue) on supported models — useful for self-contained clips that don't need separate audio layering.
- Write voiceover lines from storyboard scene goals.
- Keep voiceover intelligibility first (music ducking, clean pauses).
- Target integrated loudness around web/social norms and avoid clipped peaks.

## 6) Product marketing defaults

- Show product in the first 3-5 seconds.
- Demonstrate one core value before listing features.
- Add evidence: metric, testimonial quote, benchmark, or clear visual proof.

## 7) Explainer defaults

- Define the problem in plain language.
- Explain mechanism visually (steps, overlays, animated callouts).
- End with a single next action and expected outcome.

## 8) Revision loop

- Round 1: narrative and pacing approval.
- Round 2: visual style and brand alignment.
- Round 3: polish (caption timing, transitions, audio mix, export settings).

## 9) Delivery checklist

- Correct aspect ratio and safe zones.
- Captions aligned with voiceover.
- No flicker/jumps across scene joins.
- Proper CTA frame hold (at least 2 seconds).

## 10) Reliability

- Keep outputs in predictable folders (`assets`, `scenes`, `audio`, `final`).
- Store storyboard + manifests with each render for reproducibility.
- Use `--json` output from pixcli to track generated files programmatically.
