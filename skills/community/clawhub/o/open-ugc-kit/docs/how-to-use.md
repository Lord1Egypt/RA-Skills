# How to use The Open UGC Kit

Built for **Seedance 2.5**. Two generations: a still, then an 8-second image-to-video clip.

```
product facts → still (9:16) → Seedance 2.5 I2V (720×1280, 8s, audio on) → captions in-app
```

Do not ask Seedance to invent the first frame from a vague paragraph. Lock the opening as a still. Then animate that still. Full model rules: [seedance-2.5.md](seedance-2.5.md).

## Tools

1. **Still** — any photoreal image model (Nano Banana, Seedream, Flux, …)
2. **Motion** — Seedance 2.5 on [ezugc.ai](https://ezugc.ai) (`bytedance:seedance@2.5`)
3. **Captions** — CapCut or your editor. Never bake text into the generation.

You need a product photo or a clear description, and about 10 minutes.

## Brackets

Replace every `[BRACKET]` before you generate. Leave nothing in square brackets.

| Bracket | What to put | Example |
|---|---|---|
| `[PRODUCT]` | Name + one visual fact | matte sage 50ml serum bottle with a pump |
| `[PACKAGING]` | How it arrives | brown mailer with a white tissue wrap |
| `[CREATOR]` | Age range, presentation, outfit | woman, late 20s, gold hoops, grey hoodie |
| `[SETTING]` | Only if you override the scene | skip this if the opening already names a room |
| `[HOOK_LINE]` | First thing they say, under 8 words | wait I actually like this |
| `[BENEFIT]` | One concrete claim you can stand behind | it doesn't pill under makeup |
| `[CTA]` | One ask | link in bio / waitlist is open / I bought the bundle |

If you did not measure a claim, do not write it.

## Path A — ready opening (default)

1. Open `prompts/unboxing.md`, `street-interview.md`, `face-cam-review.md`, or `qa-who-sells-more.md`.
2. Copy the **still prompt**. Fill brackets. Generate 9:16. Leave space around hands and product (motion room).
3. Copy that scene's **Seedance 2.5 prompt**. Fill `[HOOK_LINE]`.
4. Run Seedance 2.5 image-to-video: still as first frame, **8s**, **720 × 1280**, audio on. Draft at **480 × 854** if you are iterating.
5. Caption off-model.

## Path B — new scene in a format

1. Run a master in `docs/format-masters.md` to get a still prompt.
2. Animate with the matching master in `docs/animation-masters.md`.

## Path C — clone a viral ad (Ad Spy)

1. Open [Ad Spy](https://app.ezugc.ai/dashboard/ad-spy). Pick an ad in your niche.
2. Screenshot the first 1–2 seconds.
3. Run `docs/clone-viral-scene.md` with the screenshot and a product photo.
4. Generate the remake still, then Seedance 2.5 I2V on [ezugc.ai](https://ezugc.ai).

Copy camera, room, and timing. Do not copy a creator's face or a trademarked pack. Full click-path: `workflows/clone-from-ad-spy.md`.

## Realism checklist (still)

Reject and regenerate if:

- Skin is poreless or plastic
- Extra fingers or melted product
- Showroom / three-point studio light
- Invented or misspelled logo
- Caption, sticker, or watermark already in the frame
- Product or hands cropped so tight they cannot move

A good UGC still is slightly messy.

## Seedance duration

| Length | Use |
|---|---|
| 4–5s | One beat. Fastest iteration. |
| **8s** | **Default.** Opening + one handling beat. |
| 15s | Two connected beats. Write more `[time]` windows. |
| 30s | Ceiling. Only with a full beat sheet. |

## What this kit does not do

- It does not write a 60-second script.
- It does not add paid media targeting.
- It does not replace a real testimonial when the brief requires one.
