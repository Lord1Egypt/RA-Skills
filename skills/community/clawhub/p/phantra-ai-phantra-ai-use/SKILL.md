---
name: phantra-ai-use
description: The habits every Phantra skill assumes, loaded before any writing tool: reuse what the person has, hold every scene to a photo, quote before anything costs, wait for the person's yes before anything spends, and never overwrite. Use when work on the connector starts, before the first `write_scene`, `create_project` or `add_element`, or when unsure what a tool spends or changes. NOT for one job's steps: a scene (write-scene), a render (price-and-render) or credits (credits-and-limits).
---

# Use the studio well

Every other skill in this plugin assumes these five habits. Read this once,
then keep to it on every call. Only `generate_image` (a still), the effect
tools (`edit_image`, `remove_background` and the rest) and `approve` (a scene's keyframes or clip) spend credits, each after a
quote and the person's yes; the rest reads, saves text or starts a free edit.

## 1. Reuse what exists before making anything

Before a new project, element, scene or recipe, look for the one already there:

- `projects`, then `project` with its id: the brief, look, scenes, references,
  renders and chat the person already has. A scene belongs in an existing
  project when one fits; `search` with a few words finds it.
- `elements`: the characters, props and places with their photo refs. A name
  already there gains a photo instead of becoming a second element.
- `library`: renders (`gen:<id>`) and uploads (`asset:<id>`), the ids the free
  edits and `share_link` take.
- `recipes`, then `recipe`: the studio's shelf and the person's own, so a way
  of working they saved is used, not reinvented.
- `recent` is the quick version of the first and third: the latest projects,
  open scenes and renders. It lists no elements, uploads or recipes.

## 2. A picture on every scene

A scene needs at least one element picture from the person. With none it is saved as a draft
and can be neither priced nor rendered. The refs you pass are photo refs
exactly as `elements` lists them, the anchor first (a face before a room); a
look-only photo (`roles` light, palette, framing, style) is never first. When
no element fits:

- a picture at a web address the PERSON gave you: `add_element` with `kind`,
  `name` and that address as `source`. It is the one tool that takes an
  address, and never one you found or guessed.
- a picture on their phone or computer: `upload_link` with `purpose` reference,
  `element_kind` and `element_name`; give them the `url`, wait for them to come
  back, then call `elements` again.

## 3. Quote before anything costs credits

Making media is the only thing that costs, and it is quoted first. For a scene,
`quote` with the `scene_id` before anyone decides: the keyframes, the clip per
shot, the balance. For a still or an effect, the first `generate_image` or
effect-tool call, with no `quote_token`, IS the quote. Say the price in the quote's own
words: never your own arithmetic, never a currency; credits only.
`recommend_model`, `video_models` and `image_models` help choose a model;
`quote` with `model` or `frame` prices that choice exactly.

## 4. Browsing never spends, and nothing spends without a yes

Every read tool is free, and `reformat`, `trim_clip` and `assemble_clips` spend
nothing: they start jobs, so poll `job` (`wait` holds up to 15 seconds). A
render is quote, yes, approve: show the quote's price, wait for an explicit yes
in this chat (never approve on the person's behalf), then spend once -- a scene
through `approve` with the `scene_id`, `what` (keyframes or clip), the quote's
`tokens` and the same renderer choice; a still or an effect through the same call
again, the SAME arguments plus its `quote_token`. Tokens last one hour; a `quote_token`
works once (a repeat answers `already_used` and charges nothing), a changed
argument is refused, and a new render is a new quote and a new yes; never call
`approve` twice on one yes. Then `job` with `wait` until done, and `scene` shows
what landed. `refused: insufficient_credits` means stop: say it needs more
credits than the workspace has, and that credits are added in the studio.

## 5. Nothing is overwritten

Every edit makes a new item: `reformat` and `trim_clip` make copies,
`assemble_clips` a new clip, `duplicate_scene` a fresh scene, `save_recipe` a
new version, `set_preferences` a new entry, a still or an effect a new item. The
one exception is `write_scene` with a `scene_id`: it replaces that scene's TEXT.
Show the person the whole new version and get a yes before calling it.

## Three smaller rules

- **Defaults.** `preferences` holds `aspect`, `seconds`, `video_model`,
  `image_model` and `draft_first`; they are read only where a call passes
  nothing. Change them with `set_preferences` only when the person asks.
- **Refusals** come back in plain words. Repeat them to the person and change
  something; never retry the identical call. "no scene N" or "no project N"
  means the id is not this person's: re-read `project` or `recent`.
- **Ids are never invented.** A `scene_id`, `project_id`, `gen:<id>`,
  `asset:<id>`, photo ref or quote token comes from a tool's reply in this
  conversation, never from memory or a guess.

## Worked example

"Make my coffee ad vertical and send me the file."

1. `recent` shows project 12 "Coffee" with render `gen:88` in 16:9.
2. `reformat` with `ref` `gen:88`, `aspect` 9:16, `fit` pad, `project_id` 12;
   `job` with `wait` 15 until it finishes; it returns `gen:91`, a new item.
3. `share_link` with `ref` `gen:91`: hand the person the link and say when it
   expires.

Nothing was rendered, nothing was spent, and `gen:88` is untouched.
