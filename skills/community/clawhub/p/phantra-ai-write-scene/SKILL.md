---
name: write-scene
description: Writes the scene prompt for an idea the person chose, in the shape Phantra renders from, and saves it with the `write_scene` tool against their elements. Use when someone asks to write the scene, the prompt, the shots or the script, says "make the scene" after choosing an idea, or wants a saved scene changed. NOT for choosing between ideas (ideas-and-projects), pricing or rendering (price-and-render), or choosing photos or a look (look-matching).
---

# Write the scene

A scene in Phantra is ONE paste-ready prompt a video model reads top
to bottom, rendered one timed shot at a time against the elements the
person added. You write it in the chat (free), then `write_scene` saves it.

## Before writing

1. Have the idea in one or two sentences: what we see, and why it holds
   (ideas-and-projects, or the person). Inside a project, `project` gives the
   brief and the look the scene must keep to.
2. `elements`: the person's characters, props and places with their photo
   refs. A scene is never rendered from a name, and not at all until it is
   held to at least one photo. A face, product or room with no photo: ask for
   one (`add_element`, or `upload_link` for a file on their device).
3. Settle the length in seconds (4 to 30; 10 is the default) and whether the
   idea wants cuts or one continuous take. Default to cuts: two or more shots.
   One continuous shot only when the person asked for one.

## The shape (five parts, in this order)

Write every look in cinematography and colour-grade terms; never name a film,
a director, a brand or a real person.

1. **Opening line.** "Ultra-realistic grounded [tone] video in 9:16," then say
   which attached photo is the EXACT face, the EXACT outfit, the EXACT product
   or the EXACT place ("the attached photo of Sam is his exact face and
   clothing"). Name the photos; do not re-describe what they show. With no
   photos for a character, describe the person plainly.
2. **Style.** The look in two or three sentences: palette, light (source,
   direction, colour, hardness), lens and framing height, depth of field,
   finish and grade. Realism is practical light, believable physics and
   restraint; never "raw handheld, matte, muted" by habit.
3. **Beats, as timed shots.** Each shot opens with its window, written like
   `(0-4s)`. Windows start at 0s, are contiguous, never overlap, and end at the
   total length. Each window is rendered as its own clip by a model that sees
   only that window, so **each window is ONE shot**: one camera setup, one
   clear action that fits its length, 2 to 10 seconds. Cuts and location
   changes happen between windows, never inside one; say them ("hard cut to",
   "reverse on"). Open on an arresting image, turn or reveal; end abruptly;
   reactions serious, never cartoon. As many shots as the idea needs.
4. **Sound.** Begin "No background music." then only the diegetic sound: what
   you would hear in that scene, nothing else.
5. **Avoid.** "Avoid: plastic AI sheen, CGI-looking skin or fabric, cartoon
   reactions, dramatic slow motion, named films, brands or actors."

A worked skeleton (replace everything in it):

```
Ultra-realistic grounded deadpan comedy in 9:16. The attached photo of Sam is
his exact face and clothing. Style: soft daylight from one window, true-to-life
colour with gentle contrast, a 35mm frame at chest height, shallow depth when
close, practical light only, a real lived-in kitchen.
(0-4s) Sam lifts the lid of a dented biscuit tin and freezes, both hands still
on it.
(4-10s) Hard cut to the hallway: Sam backs away from the open front door, the
tin held against his chest, and the door swings wider on its own. End abruptly.
No background music. Only diegetic sound: the tin lid's scrape, a floorboard,
the door's hinge.
Avoid: plastic AI sheen, CGI-looking skin or fabric, cartoon reactions,
dramatic slow motion, named films, brands or actors.
```

## Save it

Show the prompt to the person first and take their edits. Then `write_scene`
with `prompt` (all five parts), `seconds`, `refs` (the photo refs exactly as
`elements` lists them, **the most important one first** -- the first ref is
what the render anchors on: the face before the room), `roles` when a photo is
for its light or palette only, a `title`, and `project_id` when it belongs to
a project. The reply gives the scene's id, how many shots were written and its
link in the studio. Nothing is spent.

**A scene with no photos is saved as a draft** (`needs_reference`): it cannot
be priced; add a photo and `write_scene` again with its `scene_id` and `refs`.

**To change a scene**, `write_scene` with its `scene_id` and the whole new
prompt: it replaces the text, so show the new version and get a yes first.

## Then

Price-and-render: `quote` the scene (keyframes and clip in credits, a signed
token per render, good for an hour); show the price and WAIT for the person's
yes; only then `approve` with `what` ("keyframes" or "clip"), the quote's
`tokens` and the same renderer choice; `job` until done, `scene` for the clips.
One yes covers exactly the quotes the person was shown and named; anything else
needs its own yes. Refused for credits: stop; credits are added in the studio.
The scene's page in the studio is the other place they can approve it.

## Do not

- Never invent a photo ref, never pass a URL, and never leave a
  `{placeholder}` in the prompt (the tool refuses it).
- Never write a window over 10 seconds or under 2, and never describe the look
  by naming a film, a brand or a person.
