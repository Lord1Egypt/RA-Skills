# Profile-Aware Video Prompting Guide

This guide covers how to prompt the active video pipeline while keeping prompts aligned with format and genre profiles rather than hard-coded service assumptions.

## Active Video Profile

Current active profile: `video_limited_series`

- Master output target: 32-second episode master
- Preview output target: 8-second trailer/preview
- `video_url` remains the canonical master asset in platform APIs
- `preview_video_url` and `preview_poster_url` are separate discovery assets

These runtime values belong to the active format profile. They are not global invariants for every future format.

## Prompt-Selects-Pipeline

Use prompts to refine within the selected pipeline, not to define the pipeline itself.

- `format_profile_id` selects runtime, structure, and provider defaults
- `genre` and optional `genre_profile_id` select pacing, camera, motion, lighting, audio, and reveal defaults
- prompt fields add story-specific semantics inside those constraints

## Structured Prompt Formula

Write prompts in this order:

1. `Subject`
2. `Action`
3. `Camera`
4. `Environment`
5. `Audio`
6. `Style`
7. `Constraints`

Example:

```text
Subject: A detective in a rain-soaked trench coat.
Action: Walks slowly beneath flickering streetlights while checking a folded map.
Camera: Medium tracking shot from behind with a slight left-to-right pan.
Environment: Wet cobblestone alley at night, neon reflections, light fog.
Audio: Soft rain, distant traffic, "We only have one chance," the detective whispers.
Style: Neo-noir contrast with cool cyan shadows and warm practical highlights.
Constraints: No logos, no readable text overlays.
```

## Genre Defaults

Genre profiles shape defaults before prompt refinement:

- pacing bias
- camera bias
- motion bias
- lighting bias
- audio bias
- reveal/conceal bias
- shot emphasis

Write prompts that cooperate with those defaults instead of fighting them.

## Active Profile Authoring

For `video_limited_series`:

- `episode_master_plan` should define a clean 4-beat progression for the 32-second master
- `trailer_prompt` should define the hook, reveal, escalation, and unresolved ending for the 8-second preview
- keep characters, wardrobe, geography, and lens language stable across the master
- keep the preview teaser-oriented, not a compressed episode summary

## Reference Imagery

Reference imagery is provider-conditional.

- Discovery posters remain valid metadata for every production
- Only mention reference-image conditioning when the selected provider lane requires image input
- Do not assume every video submission needs a globally required `video_reference_url`

## Recommended Prompt Habits

- Use one primary action per shot
- Be explicit with camera language
- Include ambient sound even when dialogue is short
- Specify lighting and atmosphere concretely
- Keep constraints explicit

## Troubleshooting

| Issue | Fix |
|---|---|
| Weak composition | Strengthen Subject + Camera fields |
| Unclear action | Reduce to one explicit action sentence |
| Audio mismatch | Add concise dialogue/ambient cues in Audio |
| Overly generic style | Add specific look references in Style |
