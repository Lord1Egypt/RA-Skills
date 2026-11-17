---
name: series-and-continuity
description: Makes several Phantra scenes read as one series (episodes, a campaign): one project and look, the same refs in the same order and roles, the same style block, a fixed length, frame and model, each episode started from the last with `duplicate_scene`. Use when someone wants part two, a series, episodes, "the same as the last one but...", or asks why two scenes differ. NOT for a single scene (write-scene), choosing a look (look-matching) or choosing between ideas (ideas-and-projects).
---

# Series and continuity

The studio renders each scene, and each shot in it, on its own; no render
remembers the last one. What makes two scenes read as one series is what you
carry across on purpose: the same photos in the same order with the same
roles, the same style block word for word, the same length, frame and model.
Setting a series up and writing its episodes spends nothing; a render is
`quote`, the person's yes in chat, then `approve` (price-and-render).

## Set up once

1. One project. `projects`; when none fits, `create_project` with a `title`,
   a `brief` (who it is for, what every episode must always show and never
   show) and a `look` (the style block, in cinematography terms). Every scene
   in the series is saved with its `project_id`.
2. One cast. `elements`: the characters, products and places the series uses.
   Decide the ref ORDER once (the anchor first: the face before the room) and
   the `roles` once ({ref: role}). Write both down in the chat so every
   episode uses the same list.
3. One style block: two or three sentences (palette, light, lens and framing
   height, depth of field, finish). It is the project's `look`; paste it into
   every scene unchanged.
4. Fixed defaults: `set_preferences` with `seconds` and `video_model`, so
   `write_scene` and `quote` called with nothing else still match the series;
   the 9:16 shape is the studio's own frame, not a preference. `preferences`
   reads them back; a value the catalogue lacks is refused.

## Each new episode

1. `project` with the id: the brief, the look, the scenes so far and the
   references they used. Then `scene` on the last episode's `scene_id` for its
   full prompt (`project` shows only the start of each).
2. `duplicate_scene` from the last episode's `scene_id`, passing only the
   new `prompt` (and `seconds` when it changes). `refs`, `roles` and
   `project_id` are copied, so the order and the roles hold. Its stills and
   clips are not copied: the copy is a fresh scene.
3. In the new prompt change only the beats. Keep the opening line and the
   style block word for word, keep the sound line's shape, keep the avoid
   list, and name the same photos the same way.
4. Show it to the person, then `quote` it: the keyframes (the credits for
   `each` still) and the clip, one render per shot with its credits and a
   token, against the balance; with a series default set,
   `preference` says which model it priced. Say the price in credits and WAIT
   for the person's yes in chat.
5. Only on that yes: `approve` with the quote's tokens and the same renderer
   choice (provider, model, frame, duration), then `job` until done and
   `scene` for the clips. Never approve on the person's behalf, never twice;
   `insufficient_credits` (needs, available) means stop and say credits are
   added in the studio (price-and-render).

Episode 2 from scene 418, with episode 1's opening line and style block
pasted in unchanged (replace the beats):

```
duplicate_scene(scene_id=418, prompt="Ultra-realistic grounded deadpan comedy
in 9:16. The attached photo of Sam is his exact face and clothing. Style: soft
daylight from one window, true-to-life colour with gentle contrast, a 35mm
frame at chest height, shallow depth when close, practical light only.
(0-5s) Sam opens the same dented tin on the same kitchen counter; inside, a
folded map.
(5-10s) Hard cut to the hallway, the framing of episode 1: Sam reads the map,
and the front door is already open. End abruptly.
No background music. Only diegetic sound: paper, the hinge.
Avoid: plastic AI sheen, CGI-looking skin or fabric, cartoon reactions,
dramatic slow motion, named films, brands or actors.")
```

## Check continuity after the renders

`scene` on each episode lists the clips rendered so far. Read them against
the series rules: the same frame and length, the anchor's face or product in
every episode, the same light and palette. A clip that drifted is not edited
here: say what drifted (a changed style sentence, a ref in a different order,
a different model or frame), fix the prompt or the refs, and `duplicate_scene`
again as a new scene, quoted and approved on a yes like any episode. Over
time `what_works` says which model and preset the person kept most, which is
the one to hold the series to.

## Do not

- Never reorder the refs between episodes: the first ref is the anchor, and a
  new first ref is a new look.
- Never rewrite the style block to improve one episode; change it for the
  whole series: the person changes the project's look in the studio (no tool
  here does), the new block goes into every episode written after it, and an
  earlier episode that must match is made again with `duplicate_scene`, never
  rewritten in place.
- Never move one episode to another model or frame to save credits without
  saying the look will shift; price the draft frame instead, where the series'
  model has one (`video_models` says which do):
  `set_preferences` with `draft_first` true, then `quote` with no renderer
  named, and `approve` naming the model and frame the quote answered.
- Never promise two renders will match exactly. What you can promise is the
  same photos, words, length, frame and model.
