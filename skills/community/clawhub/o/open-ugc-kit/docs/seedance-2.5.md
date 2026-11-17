# Seedance 2.5

This kit is written for **Seedance 2.5** (`bytedance:seedance@2.5`). Other video models can still take the stills. Motion prompts follow Seedance's five-layer shot brief.

Official prompting pattern: [Runware — Prompting Seedance 2.5](https://runware.ai/docs/models/bytedance-seedance-2-5/guides/prompting).

## Default settings (UGC)

| Field | Value | Why |
|---|---|---|
| Duration | **8** | One micro-narrative. 4–5s is a single beat. 15s+ only if you wrote more beats. |
| Size | **720 × 1280** | 9:16 at 720p. Do not use the `resolution` preset — that renders 16:9. |
| Draft size | **480 × 854** | Iterate here, then re-run the same prompt at 720 × 1280. |
| Audio | **on** | Seedance builds a native track. Name it with `Audio:`. |
| First frame | the still | Image-to-video. Do not re-describe the picture. |
| Product lock | `@Image1` | Attach a product photo when the label has to stay exact. |

Range is 4–30 seconds. Under ~5s the model compresses hard. Past 30 the request is rejected.

## Five layers (every motion prompt)

Write them in this order. Dropping a layer hands that decision to the model.

1. **Shot** — camera first: `handheld phone`, `static locked-off`, `slow push-in`. Seedance reads crew language: dolly-in, orbit, crane, handheld, locked-off. For UGC, default is **handheld** with organic micro-shake. Do not ask for anamorphic, drone, or dolly-zoom.
2. **Subject** — one continuity sentence. Do not re-describe hair, wardrobe, or the room if they are already in the still.
3. **Action** — what the body and product do, in time order. One dominant arc. Separate this from the camera clause.
4. **Light** — `keep the existing lighting and composition` for I2V.
5. **Audio** — `Audio: …` then `No BGM`. `No subtitles` at the end so it does not burn captions in.

## Timed beats

Seedance reads `[0-2s]` windows. Keep them **continuous**, about one-second granularity, no gaps. Put too little in a window and it improvises. Pack too much and it drops a beat.

Do not ask for high-frequency micro-control ("shake three times a second").

## Dialogue

Put spoken words in double quotes, attributed:

```
She looks at the lens and says: "I wasn't even going to film this."
```

## Image-to-video vs text-to-video

| Mode | Prompt job |
|---|---|
| **I2V (default in this kit)** | Motion, camera, audio, continuity. The still already is the picture. |
| T2V | You must also write subject, room, and light from scratch (five full layers). |

Re-describing a visible face or product in I2V is how identity drifts.

## Still → Seedance

1. Generate a 9:16 still (leave space around hands and product so they can move).
2. Attach it as the **first frame**.
3. Paste the scene's **Seedance 2.5 prompt** (or a format master in `animation-masters.md`).
4. 8s · 720 × 1280 · audio on. Draft at 480 × 854 if you are iterating.
5. Caption in an editor. Never ask Seedance to add on-screen text.

## What to cut

- Cinematic / commercial color grade
- Studio rim light, beauty dish, anamorphic
- On-screen text, lower thirds, vs graphics
- Music beds (`No BGM`)
- Two unrelated action arcs in one 8s clip
