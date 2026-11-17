# Workflow: Q&A / who sells more

From a blank screen to an 8s Seedance 2.5 argument-hook.

This format is for comments. The still is two people disagreeing about `[PRODUCT]`. The clip is them talking over each other. You caption the question.

## You need

- `[PRODUCT]`
- Two distinct people in one frame (friends, siblings, couple, coworkers)
- An image model + Seedance 2.5

## Steps

1. **Still.** Pick [`prompts/qa-who-sells-more.md`](../prompts/qa-who-sells-more.md) or the Q&A format master. Both faces readable. Product in a hand or on the table between them.
2. **Tension check.** If they look like a stock-photo hug, regenerate. You want one leaning in and one unconvinced.
3. **Motion.** That scene's Seedance 2.5 prompt, or the Q&A master in [`docs/animation-masters.md`](../docs/animation-masters.md). Pointing, passing, head-shakes. No split screen. No vs graphic.
4. **Settings.** Duration **8**. Size **720 × 1280**. Audio **on**. First frame = still. Draft at **480 × 854**.
5. **Captions.** Put the question on screen the whole time, or flash it at 0–2s. Seedance must not burn it in.

```
who would you actually buy this from?
```

or

```
be honest — creator or brand page?
```

6. **Pin a comment** once it is live (on TikTok/Reels) asking people to pick a side. The prompt kit does not do that part. You do.

## Variants

- Creator vs brand site
- Cheap dupe vs the thing you are selling
- "My version" vs "the one from ads"
- Would you buy it from a stranger at a table vs this link

Keep it one question. Two questions kills the comment bait.

## Common failures

- Model invents a lower-third with names → add `No subtitles. No on-screen text.`
- Third person appears → "only the two people from the still."
- Product cloned into two bottles → "one [PRODUCT] in the scene."
- Music or vs stingers → `No BGM.`
