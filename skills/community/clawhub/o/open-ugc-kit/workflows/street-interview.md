# Workflow: Street interview

From a blank screen to an 8s Seedance 2.5 sidewalk reaction.

## You need

- `[PRODUCT]` in a form you could actually hand to a stranger (bottle, pouch, box, device)
- A still that already includes two people (or an interviewer hand + subject)
- An image model + Seedance 2.5

## Steps

1. **Still.** Pick [`prompts/street-interview.md`](../prompts/street-interview.md) or the street interview format master. The still must look like a phone held by the interviewer.
2. **Check the background.** If it is an empty grey void, regenerate with "busy sidewalk, out-of-focus pedestrians, storefronts."
3. **Motion.** Use that scene's Seedance 2.5 prompt, or the street interview master in [`docs/animation-masters.md`](../docs/animation-masters.md). The product should be turned or weighed in the hands. That is the proof, not the dialogue.
4. **Settings.** Duration **8**. Size **720 × 1280**. Audio **on**. First frame = still. Draft at **480 × 854**.
5. **Captions.** Interviewer question on screen first, then the reply. Two lines max. Seedance should not burn them in (`No subtitles`).
6. **Do not** generate a filmed "crew." No boom mics, no second camera in frame.

## Caption pattern

```
you: would you pay $X for this?
them: wait that's it?
```

Swap `$X` for a real price. Invented discounts look like ads.

## Common failures

- Both faces become the same person mid-clip → add "two distinct people, same as frame 1."
- Product melts while they turn it → add the rigid-object line from the animation doc.
- Background extras duplicate → keep duration at 8s; do not stretch to 15 without more beats.
- Music bed → `No BGM, only ambient and action sounds.`
