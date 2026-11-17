---
name: effects
description: Changes something already in the person's Phantra library with one of the seven effect tools: `edit_image`, `remove_background`, `animate_still`, `camera_move`, `upscale_clip`, `add_sound`, `reframe_clip`. Quotes it in credits and runs it only on the person's yes. Use when someone asks to edit, animate, cut out, upscale, reshape or add sound to something already made. NOT for a new still (thumbnails), the free edits (edit-and-deliver) or a scene's sound line (sound-plan).
---

# Effects

An effect takes something that already exists in the person's library and
makes a NEW item from it; the source is never changed. Every effect spends
credits, so every one is quoted first and runs only on their yes.

## 1. Is there a free way first?

A new shape by padding or cropping is `reformat`; a shorter clip or clips
joined is `trim_clip` or `assemble_clips`. None costs credits. Use an effect
when the picture itself has to change, and say so when a free edit would do.

## 2. Pick the tool

| they want | tool | takes |
|---|---|---|
| a change to an image by instruction | `edit_image` | 1-4 images, a `prompt`; `mode` faithful (default, keeps faces and products steady), precise (one image: swap an object, change text) or composite (combines images) |
| the subject cut out | `remove_background` | one image or one clip; a clip can go on a `background` colour |
| a still turned into a short animated clip | `animate_still` | one image (two for heart_gesture), a `template` |
| a still turned into a clip with a camera move | `camera_move` | one image, a `move`, a `prompt` for what happens |
| a clip sharper or smoother | `upscale_clip` | one clip; `factor` 2 or 1, `fps` 24/30/60 |
| sound for a clip | `add_sound` | one clip up to 30 s, a `prompt` for what it sounds like |
| a clip in a new shape, the new area generated | `reframe_clip` | one clip up to 10 s, an `aspect`; `quality` standard or high |

Each tool's own schema lists its legal choices: the templates, the moves,
the shapes, the colours. Name one only from that list; never from memory.
For templates, read out a few that fit what they are making rather than
guessing what a name does.

## 3. What it acts on

Sources are ids from `library`, and nothing else:

- `gen:<id>`: something made in their studio (a still, a rendered clip, an
  earlier effect's result);
- `asset:<id>`: a file they uploaded.

A web address, a photo that is only an element, or anything else is
refused, and only their own ids work. A picture not in the library yet comes
in through `upload_link`; `library` then lists it with its id. A clip is
measured before it is priced.

## 4. Quote, yes, run

1. Call the tool with its arguments and NO `quote_token`. Nothing runs. The
   answer is the quote: what will run, the sources, the credits, the balance
   and the balance after, a `quote_token`, and for a clip its measured
   length and size.
2. Say what will be made and from what, with the quote's own credits, and
   WAIT for an explicit yes in this chat.
3. Call the SAME tool again with the SAME arguments plus that `quote_token`.
   It answers a `job_id`; poll `job` with `wait` 15, as many times as it
   takes, until `done`. The result has its address and its `ref`, a new
   `gen:<id>` in `library`.

A token works once, for one hour and for exactly that request: a different
tool, choice, source or prompt needs a new quote and a new yes. A repeat
with a used token answers `already_used` and charges nothing.

## 5. What to ask before quoting

- **An edit by instruction**: the change in one sentence, and what must
  stay the same ("the label stays readable, only the background changes").
- **A template or a camera move**: which one; offer a few names that fit.
- **Sound**: what it should sound like, as the prompt.
- **A new shape by extension**: the shape, and what belongs in the new
  area. Say that the added area is generated, not filmed.
- **A cut-out**: a person or an object, and for a clip a see-through
  background (a .webm) or a flat colour (an .mp4).

## 6. Chains

A result is an ordinary library item, so it can be the next source: a still
given a camera move, that clip given sound, that clip upscaled. Each link
is its own quote and its own yes. Say the whole chain and how many quotes
it is before starting, and stop after any step they do not like.

## The spending rules

- Never run an effect on the person's behalf, never twice on one yes, and
  never one they did not name.
- `refused: insufficient_credits` (with `needs` and `available`): stop, say
  both numbers and that credits are added in the studio.
- A refusal comes in plain words (a clip too long, a choice that tool does
  not take, a source not theirs). Repeat it and change something.
- Never state a price yourself, and never promise how a result will look.
- A person's face is edited only at their own request, on their own
  photo. Never use an edit to put someone where they were not, to change
  what a product is, or to remove a mark that is not theirs.
