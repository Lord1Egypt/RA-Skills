---
name: model-prompting
description: Chooses the video model a Phantra scene renders on and writes the scene for it: `video_models` for what each model takes (lengths, frames, credits, a draft frame), `recommend_model` for a job described in words, and the wording that follows from the catalogue. Use when someone asks which model to use, what a model takes, why a quote is what it is, or how to write for a model. NOT for the scene's story and beats (write-scene), the balance (credits-and-limits) or camera language (camera-moves).
---

# Model prompting

One scene, in the studio's shape, renders on any model in the catalogue. Every
model is handed the same scene text, with the studio's own continuity line in
front of each shot; you never write a model's own syntax. What changes with
the model is what it can take (length, frame) and what it does with the words
(sound, one long take). Read those off the catalogue, never from memory.
Reading the catalogue spends nothing; a render waits on a quote and a yes.

## Read the catalogue

1. `video_models`: every model with the lengths in seconds it takes, the
   frames (resolutions), the credits a short clip costs at each frame, and the
   cheaper draft frame where it has one. These numbers are for choosing;
   `quote` prices a scene exactly.
2. `recommend_model` with the job in words ("a cheap test", "a final spot
   with sound", "one 20-second take"), `seconds`, `budget_credits`, and
   `draft` true to prefer a draft tier. Each pick carries one reason and its
   credits at that length; the reasons also say what the person kept before.
   Repeat the reasons; add nothing about a model the catalogue did not say.
3. Check the fit: the frame must be one the model lists, and a whole-scene
   `duration` one of its lengths; either off the list is refused at the quote,
   never rounded. A timed scene is priced shot by shot, each window fitted UP
   to the model's nearest legal length (a 3-second shot on a model whose
   shortest clip is 6 seconds is priced as 6), so keep shots at or above the
   model's shortest length to pay only for what is on screen.

## What follows from what the catalogue says

- **Sound.** When a pick's reason says it generates sound with the picture,
  the sound line is heard. Write it concrete and sparse, still after "No
  background music.": "Only diegetic sound: the lid's scrape, one floorboard."
  Never ask for a voice saying words the person did not write. Keep the line
  for every model; what a model does with it is the model's.
- **Length and cuts.** A model whose lengths run to 20 or 30 seconds can take
  a single continuous window: a scene written as one take renders whole at
  its full length (`quote` with `duration` prices that), so fewer cuts. A
  model whose lengths stop near 10 seconds renders a ten-shot scene one shot
  at a time, but cannot take a 20-second single take. Default to cuts of 2 to
  10 seconds either way; one take only when the person asked for one.
- **Frame and draft.** The frame multiplies the price. A draft frame (a
  cheaper one, where `video_models` lists it) is for choosing a take; it is
  finished in the studio. `set_preferences` with `video_model` and
  `draft_first` true makes a `quote` given no renderer choice price that
  model's draft frame; a `quote` passed `model` or `frame` ignores the
  preference, so for one scene pass the draft frame as `frame` yourself.

## Choose, then approve

1. `recommend_model`; say the top pick, its reason and its credits, and the
   runner-up when the reasons differ.
2. The person picks. `set_preferences` with `video_model` for the workspace's
   default, or pass `model` (and `frame`) to `quote` for this one scene.
3. Write the scene as write-scene says. The words do not change by model
   beyond the two points above.
4. `quote` with `model` and `frame`. Say the price from the quote (each
   shot's seconds and credits, the keyframes, the balance) and WAIT for the
   person's yes in this chat. Only then `approve` with `what="clip"`, the
   quote's `tokens` and the same `provider`, `model` and `frame` (and
   `duration` for a one-take scene); `job` until it is done, `scene` for the
   clips (price-and-render). A short balance answers `insufficient_credits`:
   start nothing, and say credits are added in the studio.

A worked exchange, with the names and numbers taken from the tools' replies:

```
recommend_model(what="a final client spot with sound, two people in a
kitchen", seconds=10, budget_credits=300)
-> picks, each with a reason and credits for 10s at its default frame
Say: "For a spot with sound the catalogue ranks <first pick> first: <its
reason>, <its credits> credits for 10 seconds at <its frame>. <Runner-up>
is <its reason> at <its credits>. Which one? I can set it as your default."

quote(scene_id=411, model="ltx2.3", frame="1080p")
-> clip: one 6s shot with its credits and one token; keyframes: 1 still; the balance
Say: "On LTX 2.3 at 1080p that is one 6-second shot for <its credits> (its
still would be <each> more); you have <balance>. Render it?" On a yes:
approve(scene_id=411, what="clip", tokens=[that token], provider="fal",
model="ltx2.3", frame="1080p", duration=6), then job until done.
```

## Do not

- Never state a rule the catalogue did not give you: a model's prompt syntax,
  a word limit, a camera tag, a negative-prompt field. Every model is handed
  the same scene text.
- Never quote credits per second from memory; read `video_models` or `quote`.
- Never pick for the person: rank, say why, and let them choose. A changed
  model or frame re-prices the scene, so `quote` again and approve only with
  the new quote's tokens and that same renderer choice.
- Never call `approve` before the person has said yes to the quoted price in
  this chat, never on their behalf, and never twice for one quote.
- Never pass a length or frame a model does not list, and never promise a
  model will match a render made on another one.
