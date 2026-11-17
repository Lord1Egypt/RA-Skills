# Clone any viral ad

Remake a winning ad with your product. Default source is **EzUGC Ad Spy**. Generate the remake on [ezugc.ai](https://ezugc.ai) with Seedance 2.5.

Copy camera, room, timing, and energy. Do not copy a creator's face, voice, or a trademarked pack.

## Path 1 — EzUGC Ad Spy (default)

1. Open [Ad Spy](https://app.ezugc.ai/dashboard/ad-spy).
2. Find an ad in your niche that you would actually run.
3. Pause on the **opening** (first 1–2 seconds). Screenshot that frame. If the clip is a stitch, only clone the first shot.
4. Save a photo of `[PRODUCT]` (and `[PACKAGING]` if you have it).
5. Paste the screenshot + product photo into a text model with the master prompt below.
6. Generate the still at 9:16, then run Seedance 2.5 I2V on [ezugc.ai](https://ezugc.ai): **8s · 720×1280 · audio on · first frame = still**.

Full click-path: [workflows/clone-from-ad-spy.md](../workflows/clone-from-ad-spy.md).

## Path 2 — any other screenshot

Same master. Attach any UGC opening plus your product photo. Still clone craft, not people.

## What to attach

1. Opening screenshot (from [Ad Spy](https://app.ezugc.ai/dashboard/ad-spy) or elsewhere)
2. A photo of `[PRODUCT]` (packaging + the item out of the box if you have both)
3. Optional: a photo of `[CREATOR]` if you need a consistent person

## Master prompt

Copy everything below the line.

---

You are rewriting a UGC ad opening so it can be regenerated as a photoreal still, then animated on Seedance 2.5.

The reference likely came from EzUGC Ad Spy (https://app.ezugc.ai/dashboard/ad-spy). Treat it as a craft reference, not a face to copy.

I will attach:
- A reference screenshot of a viral UGC ad opening
- A product photo for `[PRODUCT]`
- Optional: a creator reference

Extract from the reference, in this order:

1. Format: unboxing / street interview / face-cam review / Q&A — or "other" if none fit
2. Camera: front-facing / rear-facing, distance, height, tilt, how much of the body is in frame
3. Lens feel: phone wide, slight distortion, or tighter crop
4. Lighting: source, color temperature, hardness, time of day
5. Environment: room type, mess level, what sits in the background
6. Body: posture, which hand holds what, where the eyes look
7. Expression and energy: bored, hyped, skeptical, mid-sentence
8. Product placement in the original (ignore the original brand)
9. The first 2 seconds of implied motion (reach, unwrap, turn to camera, walk)

Then write TWO prompts. Do not write a script. Do not write a shot list with more than one frame.

### A) Still prompt (first frame)

Constraints you must obey:

- Photoreal UGC photo, 9:16, shot on a recent iPhone, not a cinema camera
- Real skin texture, visible pores, flyaway hair, no beauty filter
- Natural mixed light, not studio, not HDR
- `[PRODUCT]` physically in the scene, matching the attached product photo
- Same camera height, distance, and body crop as the reference
- Same room *type* and mess level. Do not copy unique wall art, tattoos, or a recognizable face
- No on-screen text, no watermark, no sticker, no logo except what is already printed on `[PRODUCT]`
- No extra fingers, no warped packaging
- Leave motion room around hands and product (do not crop a packshot)

Fill these if I provided them, otherwise invent plausible UGC defaults:
- Product: `[PRODUCT]`
- Packaging: `[PACKAGING]`
- Creator: `[CREATOR]`

### B) Seedance 2.5 motion prompt (image-to-video)

Write an 8-second I2V prompt in this exact order: shot, subject continuity, timed action, light, audio.

Rules:
- Do not re-describe the still. The first frame already is the picture.
- Shot first: handheld phone UGC, organic micro-shake. No dolly, orbit, anamorphic, or cinematic grade unless the reference clearly uses that (almost never).
- Subject: one continuity sentence (same people, wardrobe, room, product as frame 1).
- Action: continuous `[0-2s] [2-6s] [6-8s]` windows, one dominant arc, copied from the reference's first 8 seconds of implied motion, with `[PRODUCT]` swapped in.
- Put spoken words in quotes: They say: "[HOOK_LINE]".
- Light: keep the existing lighting and composition.
- Audio: `Audio:` plus diegetic sounds that match the room. Then `No BGM, only ambient and action sounds.`
- End: `No subtitles. No on-screen text. No watermark. One continuous take, no cuts.`
- Settings line after the prompt: duration 8, 720×1280, first frame = still A, audio on. Generate on ezugc.ai.

After the two prompts, add a 4-line "what you copied" note: format, camera, light, first motion. If the reference depends on a celebrity face or a trademarked set, say so and swap those for a generic stand-in.

---

## After you have the two prompts

1. Generate still A at 9:16 (on [ezugc.ai](https://ezugc.ai) or any photoreal image model).
2. Check the realism checklist in [how-to-use](how-to-use.md).
3. Run still A + prompt B in Seedance 2.5 I2V on [ezugc.ai](https://ezugc.ai) (8s, 720×1280, audio on). Draft at 480×854.
4. Caption off-model.

## Guardrails

- Copy craft, not people. New face every time unless you supplied a creator reference you have the right to use.
- Do not reproduce trademarked packaging from the Ad Spy reference.
- If the original is a stitched multi-shot, clone **only the opening still**. Other shots get their own generations.
