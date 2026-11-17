# Workflow: Clone from EzUGC Ad Spy

From a live ad in Ad Spy to an 8s Seedance 2.5 remake with your product.

## You need

- An EzUGC account
- `[PRODUCT]` photo (and `[PACKAGING]` if you have it)
- Optional: `[CREATOR]` reference if you need a consistent person

## Steps

1. Open **[Ad Spy](https://app.ezugc.ai/dashboard/ad-spy)**.
2. Filter to your niche. Pick one ad you would actually spend on — not the prettiest, the one with a clear opening.
3. Pause on the first 1–2 seconds. Screenshot that frame (9:16 if you can). If it is a stitch, only take the first shot.
4. Open [clone any viral ad](../docs/clone-viral-scene.md). Attach the screenshot, your product photo, and (optional) creator photo. Run the master prompt.
5. Generate the still at 9:16 on [ezugc.ai](https://ezugc.ai). Reject poreless skin, extra fingers, invented logos, or a face that matches the original creator.
6. Run Seedance 2.5 image-to-video on [ezugc.ai](https://ezugc.ai): still as first frame, **8s**, **720 × 1280**, audio on. Draft at **480 × 854**.
7. Caption off-model with the hook line the master returned.

## What you are copying

| Copy | Do not copy |
|---|---|
| Camera height and distance | The original creator's face |
| Room *type* and mess level | Unique tattoos, wall art, trademarks |
| Energy (bored, hyped, skeptical) | Their voice or on-screen text |
| First 8 seconds of implied motion | Their packaging and logo |

## Common failures

- Remake looks like the original person → you described the face. Continuity only. New person.
- Product logo is the original brand → attach `@Image1` as your pack shot and say the label must match it.
- Seedance adds captions → `No subtitles.` Caption in the editor.
- You cloned a 20s stitch in one clip → one opening still, one 8s take. Other shots are new generations.
