---
name: ad-variations
description: Makes A/B variants of a saved Phantra scene with `duplicate_scene`, changing one thing (the hook, the length, the first shot, the product photo or the video model), each a new scene priced on its own and read back later with `what_works`. Use when someone asks for versions, variants, an A/B test, "try it shorter" or "same ad with the other photo". NOT for the first version (write-scene), a first set of ads from one product photo (product-ad-set) or setting a look (look-matching).
---

# Ad variations

A variant is a **new scene** copied from one that exists, with one thing
changed, filed in the same project. The source is never touched, its stills
and clips are never copied, and nothing is spent until the person has seen a
variant's price from `quote` and said yes to it in the chat. Change ONE thing
per variant, so what gets kept says something.

## The order

1. Find the source: `recent`, `search` or `project` gives its `scene_id`;
   `scene` reads it in full (prompt, seconds, title, the timed shots) and gives
   only the COUNT of its photos; the refs themselves are what you passed, or
   `project`'s `references` list, each naming the scenes it is on. Read it first.
2. Agree the variable with the person: hook, length, first shot, product
   photo or model. Draft the change, show it, get a yes.
3. `duplicate_scene` with the `scene_id` and ONLY the fields that change;
   the rest is copied. The reply gives the new `scene_id` and `copied_from`.
4. Note which is which (below), then `quote` each variant and say its price:
   `keyframes` (stills, `each` credits a still) and `clip` (its `credits` in
   all), beside the `balance`. Then WAIT. One yes covers exactly the quotes the
   person was shown and named; anything else needs its own yes.
5. On the yes, `approve` with that `scene_id`, `what` "clip", the `tokens`
   from its quote and the same `provider`, `model` and `frame` the quote was
   priced with (and its `duration` when the scene is one shot). Tokens are
   good for one hour; a changed choice is refused, never re-priced. `what`
   "keyframes" draws the stills instead, on a yes of its own. Then `job` with
   the returned id (`wait` up to 15) until it is done; `scene` shows the clips.
6. Later, `what_works` reads what was kept.

## The five changes

- **Hook** (`prompt`): rewrite the first window's line only -- the first
  sentence said, or the first image -- in the person's own words, and keep
  every other window, the style block, the sound and the avoid list as is.
- **Length** (`prompt` + `seconds`): re-time the windows so they still run
  contiguously from 0 to the new total, each 2-10 s; drop or shorten a shot
  rather than squeeze them all; `seconds` is the last window's end.
- **First shot** (`prompt`): swap the opening window for a different image
  (the product before the face, or the reverse); the rest stays timed.
- **Product photo** (`refs` + `roles`): a different pack shot from `elements`
  as the first ref with role `product` (or a different face as `subject`).
  The first ref anchors the render, so this changes the picture most. A ref
  `elements` did not list is refused.
- **Model**: a scene carries no model; it is picked at the quote, so no copy
  is needed. `recommend_model` ranks models for the job in words; `quote`
  with `model` (and `frame`) prices the same scene on another one, and
  `approve` with those tokens and that same choice renders it there;
  `set_preferences` with `video_model` makes it the default wherever a call
  passes nothing (the quote then says so in `preference`; name it again at
  `approve`), and `draft_first` true prices the cheaper draft frame where a
  model has one. `video_models` lists them with credits per frame.

## Telling variants apart

A copy is titled "<source title> (copy)" and cannot be renamed from here (a
`write_scene` rewrite replaces a scene's text, never its title), so keep a
short table in the chat as you go and say which `scene_id` is which:

| scene_id | variable | change | credits (each from its own quote) |
|---|---|---|---|
| 412 | source | -- | 3 shots: its quote's total |
| 418 | hook | opens on "two weeks" | 3 shots: its quote's total |
| 419 | length | 15 s to 10 s | 2 shots: its quote's total |

## Worked example

Source 412 is a 15 s to-camera ad with three windows and the person wants a
shorter one. Re-time it: (0-4s) the open unchanged, (4-10s) the product shot
two seconds shorter with the closing line moved to its end, the third window
dropped. Then `duplicate_scene` with `scene_id` 412, the re-timed `prompt`
and `seconds` 10: it gives scene 419. `quote` 419 with `model` ltx2.3 reads
two shots, each with its credits, and their total (each window is fitted up
to the model's shortest length), beside the balance. Say that and wait. On "yes", `approve`
419, `what` "clip", the two `tokens`, `provider` fal, `model` ltx2.3, `frame`
1080p; `job` until it is done; `scene` 419 shows the clip.

## Reading the result

`what_works` says, per model and per preset, how many outputs were made and
kept (downloaded, cut, starred, used again), how many tries a keeper takes,
and what was posted with a scene behind it. When `enough_data` is false,
say so rather than read a winner into two renders. `scene` on each variant
shows which clips landed, with its studio link.

## Do not

- Never change two variables in one copy and call it a test.
- Never call `approve` without a yes in this chat to that variant's own
  price, never approve on the person's behalf, and never carry one yes over
  to the next variant or a second render of the same one.
- When `quote` or `approve` answers `insufficient_credits` (with `needs` and
  `available`), stop and say so: credits are added in the studio.
- Never put a URL in `refs` (exactly as `elements` lists them), and never
  rewrite the source with `write_scene` to make a variant; copy it.
