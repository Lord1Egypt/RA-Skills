---
name: product-ad-video
description: >
  Turn a product image into a short ad or promo video, the highest-polish commercial outcome: a
  hero product still in motion. Use when the user says "make a video ad for this product", "turn
  this product photo into a commercial", "a promo clip for my product", "animate this into an ad",
  or wants a polished spot for a launch, landing page, or paid social. For a creator-style
  testimonial, unboxing, or talking-head ad, use ugc-ad instead. For plain motion with no ad
  framing, use animate-image.
---

# Product ad video

Produce a short ad or promo clip starting from a product still. The still anchors the product's exact look (shape, color, label, material), and the prompt directs the motion and camera around it. This is image-to-video for a flagship video model, run as an async task. For dropping a new product into footage you already shot, swap instead of generate (see Technique).

## Inputs to collect

- **The product still.** A clean hero shot of the product. This is the anchor and is required. (Ask only if none provided.)
- **The vibe and the motion.** What the spot should feel like (sleek tech, warm lifestyle, energetic) and what should move (slow push-in, orbit, product rotating, hands interacting, scene reveal).
- **Duration and aspect ratio.** Most flagships run 5 to 10 seconds. Confirm the target (vertical for social, wide for landing pages).
- Optional: voiceover or music (route to `voiceover`), and whether there is existing footage to swap the product into rather than generate fresh.

## Models

- **Default flagships (image-to-video):** Seedance 2.0 (`bytedance:seedance@2.0`), Veo 3.1 (`google:3@2`), Kling 3.0 Turbo (`klingai:kling-video@3.0-turbo`), Wan2.7 (`alibaba:wan@2.7`). All are `live` and accept a starting image. Pick by feel: Veo 3.1 for cinematic polish with native audio, Seedance 2.0 for physics-aware motion and multi-reference, Kling 3.0 Turbo for a faster cheaper draft pass, Wan2.7 for reference consistency with native audio.
- **Swap a product into existing footage:** Pruna P-Video-Replace (`prunaai:p-video@replace`) replaces one on-camera object in a source video using a reference image, keeping the actor, motion, timing, camera, and audio. Use this when you have a shot creator pitch and want to fan out one product variant per call.
- Confirm the live model, its capability tag (`io:image-to-video` for the flagships, `io:video-to-video` for the swap), and its exact input fields via `runware-models` + `runware-run` before calling. Do not hardcode a stale pick.

## Workflow

1. Resolve the model schema (`runware-run`) and confirm the starting-image field, the duration/resolution options, and that the task is `videoInference`.
2. Upload the product still (and any reference) as a URL or base64 into the schema's input field.
3. Run `videoInference` **asynchronously** with a prompt that directs motion and camera only. The task returns a `taskUUID`. Poll `getResponse` until terminal, then read `videoURL`.
4. Draft cheap, finish expensive: run a fast draft (Kling Turbo, or a lower resolution) to lock the motion, then re-run the approved version on the flagship at full resolution.
5. For a product swap into footage, run `prunaai:p-video@replace` with the source video plus a clean product reference and a directive prompt (see Technique).
6. To add narration or music, hand the finished `videoURL` to the `voiceover` skill.

## Technique

- **The still anchors, the prompt directs.** The starting image fixes the product's identity and the opening composition. Spend the prompt on what changes over time: subject motion, camera move (slow push-in, orbit, dolly, rack focus), lighting shifts, and a scene reveal. Do not re-describe the product the image already shows. See `runware-prompting` for image-to-video grammar.
- **Cinematic grammar, three to four sentences.** Flagship video models read camera vocabulary directly. A compact scaffold (framing, camera motion, lighting, action) beats a wall of adjectives.
- **Fill the ad-shot brief, then write the prompt from it.** Pin the spot before prompting. Fill each line, then turn the filled brief into the three-to-four-sentence motion prompt.

  ```
  Product moment: <the one beat the product earns, e.g. cap lifts, light catches the glass>
  Motion: <what moves, e.g. slow orbit, product rotates, hands interact>
  Camera: <named move + pace, e.g. slow push-in, gentle quarter orbit>
  Setting: <where it sits, e.g. clean studio sweep, warm kitchen counter>
  Mood: <feel, e.g. sleek tech, warm lifestyle, energetic>
  Duration: <5 or 10, confirm allowed values per model>
  ```
  Drop the lines the starting image already fixes (do not re-describe the product). Load `references/examples.md` for three worked recipes (hero clip, footage swap, social loop) with the real async request and result shape.
- **Swap, do not regenerate, when you have footage.** To put a new product into an existing clip, P-Video-Replace works off a **clean product photograph of the target alone** (no person, no hands, no extra props, plain neutral background) plus a directive `positivePrompt`. Name the exact thing to replace in the source and everything that must stay: "Replace the matte-black case the woman is holding with the brushed-steel tumbler from the reference image. Preserve the woman, her face, her gestures, her speech, the studio, the lighting, the camera, and the audio exactly as they appear in the source. Only the object in her right hand should change; everything else stays as the source." That closing "only X changes, everything else stays" line is the load-bearing direction that turns a global swap into a local one.
- **Match the reference framing to the source.** A product held vertically at chest level pairs with a vertical product shot. A garment seen torso-on pairs with a flat-lay of its front face.
- **Batch low, finish high.** A single source recording fans into many product variants through one replace call each at 720p for review, then re-run only the approved variants at 1080p.

## Parameters that matter

- `taskType: videoInference` with `deliveryMethod: async`. Video is a polled task, never a blocked sync call.
- Starting image and `referenceImages`. Confirm the exact field name against the live schema and never guess. P-Video-Replace takes the source under `inputs.video` and up to **3** images under `inputs.referenceImages`.
- `duration`. Typically 5 or 10 seconds on the flagships. Confirm the allowed values per model.
- `resolution`. Draft at 720p, finish at 1080p where supported.
- `seed`. Fix it to hold a take while iterating the prompt, and vary it for alternates.
- The prompt carries motion and camera, not a `strength` dial. Be specific about what moves.

## Quality bar

- The product reads as the same product from the still: shape, color, label, and material did not drift.
- Motion is intentional and on-brand, not a jittery or melting loop. The camera move serves the product reveal.
- For a swap, only the named element changed and the actor, timing, camera, and audio of the source are intact.
- **Brand-safety:** no invented claims, ratings, testimonials, or reviews, no fabricated logos or award badges, and no readable on-screen copy unless the user supplied the exact wording. Retry or cut anything that asserts a fact the user did not provide.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`. Sibling outcomes: `animate-image` (general still-to-motion), `ugc-ad` (creator-style spots), `replace-in-video` (object/character swap), `voiceover` (add narration or music).
