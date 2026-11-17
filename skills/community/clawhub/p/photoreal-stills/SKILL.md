---
name: photoreal-stills
description: >
  Generate images that read as real photographs, not AI renders: candid portraits, editorial,
  documentary, food, architectural, lifestyle. Use when the user says "make it look like a real
  photo", "this looks too AI", "less plastic skin", "shot on film", "candid not posed",
  "photorealistic", or wants stock-style, reportage, or interior shots that pass for a camera
  capture. For a product or packshot specifically (white background, hero, e-commerce), use
  product-photography instead. When exact lettering matters, use text-in-image.
---

# Photoreal stills

Produce still images that a person would believe came out of a camera, not a model. The hard part is not resolution, it is defeating the "AI look": waxy skin, plastic textures, eerie symmetry, blown-out studio light, and over-saturated everything. The lever is prompting for real optical and lighting behavior plus deliberate imperfection, then judging the result against an is-this-a-photo bar.

## Inputs to collect

- **The scene / subject** and the genre it belongs to (candid portrait, editorial, documentary, food, architectural, lifestyle). Genre sets the lens, light, and framing defaults.
- **The vibe / reference**: a era, film stock, magazine, or photographer style if the user has one. (Ask only if the request is generic.)
- **Aspect ratio and orientation** for the intended use (vertical for phone/social, 3:2 for editorial, square for grid).
- Optional: a real reference image to match, brand-safety constraints (no readable on-image text or logos unless supplied), how many variants.

## Models

- **Default: FLUX.2 [max]** (`bfl:7@1`), flagship text-to-image with the strongest prompt adherence and the most convincing micro-texture and lighting. Best general pick for photoreal.
- **Strong alternative: Qwen-Image-2.0-Pro** (`alibaba:qwen-image@2.0-pro`), high visual fidelity and reliable text/iconography, good for editorial and lifestyle frames that include signage or packaging.
- **ByteDance Seedream** for a different texture and fast iteration: **Seedream 4.5** (`bytedance:seedream@4.5`) for high-fidelity 2K to 4K, or **Seedream 5.0 Lite** (`bytedance:seedream@5.0-lite`) as a cheaper, faster draft tier.
- Confirm each is `live` and inspect its schema before calling. Use `runware-models` (live lookup) + `runware-run`. Never hardcode a stale choice. Models change weekly.

## Workflow

1. Resolve the model + schema via `runware-run`. Confirm field names (dimensions/aspect ratio, steps, guidance, seed, output format) against the live schema, do not assume them.
2. Build the prompt from the genre defaults plus the anti-AI-look checklist below: name the camera, lens, light, time of day, and one or two real imperfections.
3. Run `imageInference` synchronously (stills are fast). Request a small batch (3 to 4) rather than one. Photoreal is a numbers game, you pick the most believable frame.
4. Judge every frame against the quality bar. Reject the plastic ones outright rather than upscaling them.
5. Iterate by changing one variable at a time (light, lens, or imperfection clause), keeping a fixed seed when you want to isolate the effect.

## Technique

This is the core of the skill: an anti-"AI-look" checklist. AI renders fail in predictable ways. Counter each one explicitly. For prompt phrasing per model family, lean on `runware-prompting`.

**Build the prompt in this order** so nothing gets dropped:

1. **Subject + moment** (who/what, doing what, candid not posed).
2. **Camera + lens + aperture** (the optics that make it a photo).
3. **Film / sensor + grain** (the texture layer that kills plastic).
4. **Light source + time of day + direction** (real, directional, with falloff).
5. **One or two named imperfections** (skin texture, asymmetry, a stray element).
6. **Color restraint** (natural, not over-saturated).

Skipping any one of these is usually exactly where the frame goes synthetic.

**Specify the camera, not just the scene.** A photo is made by a specific lens on a specific sensor. Name them.

- **Lens and aperture:** "shot on a 35mm lens at f/2", "85mm portrait lens, shallow depth of field", "wide 24mm with mild distortion". Aperture buys you real, gradual background blur (bokeh) instead of the flat cut-out AI default.
- **Camera / film / sensor:** "Kodak Portra 400", "shot on 35mm film", "Fujifilm grain", "full-frame digital, slight noise in the shadows". Film stock and grain are the single fastest way out of the plastic look.
- **Real focal behavior:** call out **depth of field** and where focus falls ("focus on the eyes, background falls off softly"). Mention **motion blur** or a fast shutter for candids. These read as optics, which AI defaults omit.

**Defeat the plastic-skin / over-smoothed texture failure.** This is the #1 tell.

- Ask for **skin texture**: "visible pores, fine lines, slight skin imperfections, natural blemishes, peach fuzz". Refuse airbrushed perfection.
- Add **micro-detail** appropriate to the surface: fabric weave and lint, scuffs on leather, condensation on glass, crumbs and oil sheen on food, fingerprints, dust, wear.
- For non-skin subjects the same rule holds: surfaces in the real world are never uniform. Name the wear.

**Break the symmetry and the perfection.** Real frames are slightly off. Perfect things look fake.

- **Asymmetry:** "natural asymmetric face", uneven hair, a stray strand, clothing that sits unevenly, an object slightly out of place. Symmetrical faces and mirror-perfect compositions scream render.
- **Candid framing over posed:** "caught mid-gesture", "looking away from camera", "unposed, natural expression", "off-center composition". Eye-contact-dead-center hero shots read as stock-AI. A slightly imperfect crop reads as a real moment.
- **One imperfection on purpose:** a small light flare, a soft out-of-focus foreground element, a bit of clutter at the edge, a reflection. Tidiness is suspicious.

**Use real light, not generic studio light.** Flat, even, shadowless lighting is an AI signature.

- Name a **real source and time of day**: "golden hour, low warm sun from camera left", "overcast soft diffused daylight", "single window light, hard shadows", "tungsten interior at dusk, mixed color temperature".
- Let light have **direction and falloff**: shadows on one side, highlights that clip slightly, a color cast from the source. Even illumination with no shadow is the studio-AI tell.
- For interiors and food, **mixed and practical light** (lamps, window, candle) beats a clean key light.

**Hold back saturation and contrast.** AI over-cooks color.

- Ask for **natural / muted / true-to-life color**, "not over-saturated", "filmic color", "slightly desaturated". Skies that aren't electric blue, greens that aren't neon.
- A touch of **flatness or haze** ("slight atmospheric haze", "low contrast film look") reads more real than punchy HDR.

**Fix the small structural tells.** Beyond skin and light, these quietly betray a render:

- **Hands, teeth, ears, jewelry, text** are where models break. For tight portraits, keep hands out of frame or describe them simply, and never put readable on-image text or a logo in unless the user supplied the exact wording.
- **Backgrounds that melt or repeat:** keep the background plausible and specific ("a real cafe interior, slightly out of focus") rather than an abstract gradient, and let depth of field hide what the model would otherwise invent.
- **Reflections and shadows must agree with the light** you named. A shadow falling the wrong way, or a catchlight with no source, reads as fake even when everything else is right.

**Genre defaults, as starting points:**

- **Candid portrait:** 50 to 85mm, f/1.8 to f/2.8, window or golden-hour light, eyes in focus, skin texture, unposed expression, slightly off-center.
- **Editorial / fashion:** 85mm, controlled but directional light, film stock, intentional styling but a candid moment within it.
- **Documentary / reportage:** 28 to 35mm, available light, motion in frame, imperfect crop, grain, no retouching.
- **Food:** 50mm macro, side window light, shallow depth of field, real steam/crumbs/oil sheen, natural color, slightly messy plating.
- **Architectural / interior:** 24mm (correct verticals or note the keystone), natural daylight plus practicals, mixed color temperature, real reflections, lived-in detail not showroom-sterile.
- **Lifestyle / stock:** 35mm, soft daylight, natural interaction, muted color, candid gesture, room to breathe in the frame.

## Parameters that matter

- **Dimensions / aspect ratio.** Set for the use (vertical 3:4 or 9:16 for social, 3:2 for editorial, 1:1 for grid). Confirm whether the model takes width/height or an aspect-ratio field via the live schema.
- **Seed.** Fix it to isolate the effect of one prompt change across iterations, or vary it to explore alternates.
- **Steps / guidance (CFG).** High guidance can push the over-saturated, over-sharp AI look. If outputs look cooked, ease guidance down. Confirm the field names and valid ranges in the schema (`runware-run`) and never guess.
- **Negative prompt.** Where the model supports it (real field or inline clause, check the schema), push against the failure modes directly, e.g. "smooth plastic skin, over-saturated, symmetrical, studio lighting, CGI, render, airbrushed, waxy". See `runware-prompting` for inline-vs-field negation.
- **Batch size.** Request several. Believability varies frame to frame, so pick the best rather than forcing one.

## Quality bar

The one question: **would a person scrolling believe this is a photo, not a render?** Reject the frame if any of these is true:

- Skin is smooth and waxy with no pores, lines, or blemishes.
- The face or composition is suspiciously symmetrical or perfectly centered.
- Lighting is flat, shadowless, and sourceless (generic studio glow).
- Color is over-saturated or HDR-punchy beyond what a camera captures.
- Textures are uniform and plastic (no wear, weave, dust, or grain).
- The pose is stiff and the eye contact is dead-center hero-shot.
- Any background detail melts, repeats, or defies physics.

A pass has visible texture, directional real light, restrained color, a candid or imperfect framing, and at least one small honest imperfection. When a frame fails, fix it by adding the missing real-world cue (grain, a named light, skin texture, asymmetry), not by upscaling.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `product-photography` (product-in-context and packshots), and `character-consistency` (keep the same face across a photoreal set).
