---
name: platform-delivery
description: Delivers a Phantra video in the shape and length each platform wants (9:16 for Reels, TikTok and Shorts; 16:9 for YouTube; 1:1 or 4:5 for a feed): sets a default length, writes each scene to its platform's length, reformats a finished clip per platform and hands over a download link. Use when someone names a platform, asks what size or length a video needs, or wants versions per platform (the studio does not post). NOT for the edit steps (edit-and-deliver) or a cover image (thumbnails).
---

# Platform delivery

The studio makes the file. Posting is the person's, on the platform itself:
nothing in this connector posts, schedules or publishes anywhere, and say so
plainly when asked. Reformatting runs on the studio's own server and spends
nothing; a render of a scene is priced by `quote` and runs only after the
person's yes in this chat, through `approve` (price-and-render).

## Shapes and lengths the studio advises, per platform

| platform | shape | length |
|---|---|---|
| Instagram Reels, TikTok, YouTube Shorts | 9:16 | short: 6 to 15 s for one idea, up to 30 s when the scene earns it |
| YouTube (the feed, not Shorts) | 16:9 | the whole scene; join scenes for longer |
| Instagram or Facebook feed post | 4:5 or 1:1 | 6 to 15 s |
| a story or a vertical ad placement | 9:16 | under 15 s |

A scene is written 4 to 30 seconds. Nothing here is a platform's rule; it is
the studio's advice, and the person's own `what_works` numbers outrank it.

## The order

1. **Ask which platforms, and which one leads.** The leading platform decides
   the length the scene is written to; every other platform gets a `reformat`
   copy of the finished clip.
2. **Defaults.** `preferences` reads the workspace's defaults; `set_preferences`
   with `seconds` sets the length scenes are written to (its `aspect` is the
   frame for stills and does not touch a video). A default is used only where
   a call passes nothing, and every value is checked against the catalogue: a
   refusal names the choices.
3. **Write to the length.** `write_scene` with `seconds` at the platform's
   length, the windows filling that total. The shape is not set here: a shape
   word in the prompt is not read, the render comes in the studio's own
   vertical frame, and other shapes are `reformat` copies (step 5). The same
   idea at another length is `duplicate_scene` with `seconds` and a `prompt`
   whose windows are rewritten to fit; its stills and clips are never copied,
   so it is a fresh scene to price.
4. **Render.** `quote` the scene; show the person the credits and wait for
   their yes in this chat. Then `approve` with what=clip, the quote's
   `tokens` and the same renderer choice (provider, model, frame, duration;
   price-and-render); `job` with `wait=15` until done, then `scene` for the
   clips. Never approve on the person's behalf, never twice; a refusal
   `insufficient_credits` (with `needs` and `available`) means stop and say
   credits are added in the studio.
5. **One shape per platform.** `reformat` the finished clip (a `gen:<id>` from
   `library` or `recent`; `scene` says the clip has landed but lists it by
   address, not id) once per shape, each a new item; poll `job` with
   `wait=15` (edit-and-deliver). Pad or crop, by the picture:
   - 9:16 to 4:5 or 1:1: `fit=crop` when the action sits in the middle of
     the frame (the top and bottom go); `fit=pad` when something at the top
     or bottom matters (black at the sides).
   - 9:16 to 16:9, or back: crop keeps about a third of the picture and pad
     leaves about two thirds of the frame black; say which it will be and let
     the person choose. No tool here sets the shape a scene renders in.
6. **Deliver.** `share_link` per file, named by platform in the chat: "Reels
   9:16: <url>. Feed 4:5: <url>." Each link is good for `hours` (24 by
   default, at most 168).

## A worked example

Person: "This is for Reels, and I want a feed version too."

1. Leading platform Reels, so 9:16; `set_preferences` seconds=10 on a yes.
2. `write_scene` with seconds=10 and "Ultra-realistic grounded ... in 9:16"
   as the opening line; two windows fill 0 to 10 s.
3. `quote` with model=ltx2.3 prices the two windows as two six-second LTX 2.3
   shots, each with its credits, and their total against the balance. On the person's
   yes, `approve` what=clip with the two tokens and the same renderer choice;
   `job` wait=15 until done. `scene` shows the clip has landed; `library`
   with kind=video lists it newest first as gen:920.
4. `reformat` ref=gen:920, aspect=4:5, fit=crop (the face is centred). `job`
   until done: gen:921.
5. `share_link` for gen:920 and gen:921, each named. "Post them on the
   platform yourself; the studio does not post. Once they have numbers,
   `what_works` reads what you posted with a scene behind it."

## Do not

- Never say the studio can post, schedule or publish; it cannot.
- Never crop a clip whose edges carry the action; ask, or pad.
- Never state a platform's limits as fact; say what the studio advises.
- Never price a second render yourself; its credits come from `quote`.
- Never call `approve` without a yes in this chat to the price `quote`
  showed, and never on a quote already approved.
