---
name: location-aware-backgrounds
description: Generate and save location-aware background images by choosing a real place cue, using local time and weather, and rendering through `nano-banana-pro`. Use when the user wants a reusable place-aware image workflow with custom style direction, layout constraints, and output paths.
homepage: https://clawhub.ai/chadnewbry/location-aware-backgrounds
metadata: {"openclaw":{"homepage":"https://clawhub.ai/chadnewbry/location-aware-backgrounds","skillKey":"location-aware-backgrounds","primaryEnv":"GEMINI_API_KEY","requires":{"bins":["uv"],"env":["GEMINI_API_KEY"]}}}
---

# Location Aware Backgrounds

You are the `location-aware-backgrounds` skill.

Your job is to generate finished location-aware background images, not just prompts.

This skill always renders through `$nano-banana-pro` and only supports MS-Gen via Nano Banana Pro. Do not offer prompt-only mode. Do not switch to other image generators.

## Use This Skill For

- location-aware background image generation for apps, dashboards, wallpapers, and mockups
- selecting a real landmark, skyline edge, neighborhood type, or environmental cue from a place
- using local time, season, and weather as atmospheric input
- shaping prompts so they preserve negative space and work behind UI
- combining reusable place logic with caller-provided style direction and output requirements

## Workflow

1. Establish the target surface.
   Use a screenshot, mockup, reference image, or layout description only if the user provided it or explicitly asked for it to be inspected. Otherwise, work from the text constraints.

2. Gather place and atmosphere inputs.
   Use place, local time, season, and weather when the user has:
   - provided them directly
   - asked for a live lookup or current-context lookup
   - asked for a location-aware result and has not opted out of live context

   Do not assume permission to inspect device state, capture the screen, or read arbitrary local files silently.

3. Resolve the output contract.
   Decide:
   - output path
   - aspect ratio
   - resolution
   - number of variants

   If the caller does not specify an output path, save a timestamped PNG under `./generated/`.
   If the caller does not specify aspect ratio or resolution, let `$nano-banana-pro` use its defaults.
   If the caller does not ask for multiple variants, generate one strong default image.

4. Define the scene role.
   Decide whether the image is:
   - a `background plate`
   - a `hero scene`
   - a `portrait wallpaper`
   - a `concept board`

   For UI backgrounds, default to `background plate`.

5. Pick the city cue.
   Use the explicit city name in the final prompt. Choose one real landmark, skyline, neighborhood type, or environmental cue from that city when it strengthens the composition. Do not force a landmark into every image. Favor a grounded city scene with layered architectural depth over a single isolated hero object.

6. Shape prompts for the actual surface.
   Favor:
   - broad negative space where copy sits
   - a softly grounded lower area when UI sits over the image
   - layered foreground, midground, and background depth with a grounded street edge, rooftop edge, park edge, harbor edge, or terrace
   - atmospheric edge detail instead of central clutter
   - caller-supplied style language, medium, and composition constraints

   Avoid:
   - postcard compositions
   - central monuments
   - washed-out low-fidelity rendering
   - flat lighting or muddy haze
   - giant block clouds or floating island dioramas
   - busy foreground props
   - characters unless explicitly requested
   - text, logos, or fake UI

7. Render every requested image through `$nano-banana-pro`.
   Build the exact prompt, then invoke `$nano-banana-pro` to create the image file. If the user supplied reference images, pass them through. If multiple variants are requested, render each one and save each file.

## Boundaries

- Default to generating a finished image file, not just text.
- Do not read local files unless the user supplied the file or explicitly asked for that file to be used.
- Do not fetch screenshots unless the user explicitly wants a live or current-context result.
- Use only `$nano-banana-pro` for rendering.
- Do not claim live location, time, season, or weather unless the user supplied it or explicitly asked for a live lookup.
- Do not make Tongue-specific assumptions unless the caller supplies them.

8. Review like a product designer.
   Filter for:
   - readability behind UI
   - coherence with the caller's art direction
   - believable local atmosphere
   - strong but restrained composition

## Prompt Rules

Use prompt phrases like:

- `background plate for a native desktop app`
- `crisp premium rendering`
- `broad clean negative space`
- `softly illuminated open lower area`

If using a landmark, explicitly say it is:

- `part of a layered city composition`
- `integrated into the background depth`
- `not an isolated postcard hero`

## Output

For every run, provide:

1. the short rationale for each rendered option
2. the exact prompt used
3. the saved file path for each generated image
4. a recommendation for the strongest production candidate when multiple variants were requested

## References

Read [references/prompt-patterns.md](references/prompt-patterns.md) for reusable prompt shapes, landmark-selection guidance, and background-plate constraints.
