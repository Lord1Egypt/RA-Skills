# Workflow: Unboxing

From a blank screen to an 8s Seedance 2.5 unboxing clip.

## You need

- `[PRODUCT]` description or photo
- `[PACKAGING]` description or photo
- `[CREATOR]` (or let the image model invent a person)
- An image model + Seedance 2.5

## Steps

1. **Still.** Pick an opening in [`prompts/unboxing.md`](../prompts/unboxing.md) or run the unboxing master in [`docs/format-masters.md`](../docs/format-masters.md). Fill brackets. Generate 9:16. Leave space around hands and the box.
2. **Reject junk.** Poreless skin, extra fingers, invented logo, studio lighting → regenerate. Change only the still prompt, not the format.
3. **Motion.** Paste the still as the first frame in Seedance 2.5 with that scene's Seedance prompt, or the unboxing master in [`docs/animation-masters.md`](../docs/animation-masters.md).
4. **Settings.** Duration **8**. Size **720 × 1280**. Audio **on**. Draft at **480 × 854**.
5. **Captions off-model.** Hook line from the opening, or write your own under 8 words.
6. **Optional second beat.** New still: product in use. Animate with the face-cam motion master. Cut the two clips together. Do not ask one generation to do both rooms.

## Timing to aim for

| Time | Picture | Caption idea |
|---|---|---|
| 0–2s | Hands on closed package, glance at lens | I wasn't going to open this on camera |
| 2–6s | Tape / flap / lid | wait |
| 6–8s | Product up, label in the light | okay this is actually nice |

## Common failures

- Product appears before the box is open → still was already a hero shot. Pick an earlier moment.
- Box logo is a fake brand → describe packaging as unbranded mailer, or attach a real pack shot as `@Image1`.
- Identity drifts → the I2V prompt re-described the face. Cut that. Continuity sentence only.
- Music bed → add `No BGM, only ambient and action sounds.`
- Burned-in captions → add `No subtitles.`
