---
name: explainer
description: Plans and writes a short explainer video in Phantra (what it is, how it works, why now) as timed shots held to the person's own product or place photos, then joins the rendered scenes and makes one copy per platform. Use when someone asks for an explainer, a how-it-works video, a product walkthrough, a launch clip or "a video that tells people what this does". NOT for one dramatic scene (write-scene), a long-form spoken script (youtube-script) or a person showing how they use it (ugc-tutorial).
---

# Explainer

An explainer is three beats -- WHAT it is, HOW it works, WHY now -- written as
timed shots the studio renders one at a time against the person's elements.
Words come after the render: on-screen captions live in the studio's editor,
not in the prompt, and the voice is recorded by the person. Nothing here
generates speech; a render spends credits only after a yes to its quote.

## Before writing

1. Get the three beats from the person in their words: what the thing is, how
   it works (one action you can SEE), and why now (the problem it ends, the
   moment it fits). Claims about results, numbers, reviews or awards come
   from the person; never invent one, and keep claims out of the picture
   anyway -- they belong in the captions and the voice.
2. `elements`: the scene must be held to the product or the place. A product
   explainer needs a photo of the exact product (a prop); a service or a
   venue needs the place. With none, ask for one: an https image address the
   person gave you goes in with `add_element`; a file on their phone or
   computer comes in through `upload_link` with `purpose` reference,
   `element_kind` and `element_name`, so it lands on that element.
3. `projects` / `project` when it belongs to a project: the brief says what
   must always show and never show. Settle the total length (4-30 s; 15-20 s
   suits three beats) and the frame the first platform wants.

## The shape

One scene in write-scene's five parts. Each beat is one timed window holding
ONE shot (one camera setup, one clear action, 2-10 s); a beat that needs two
actions gets two windows. Write what the camera sees, never what a narrator
says: no spoken lines, no on-screen text, no logos drawn in -- the product in
the photo carries its own.

- (what) the product or place, still and clear, in its real setting
- (how) hands using it, one action from start to finish
- (why now) the moment it matters: the before, the turn, the after

A worked skeleton (replace everything in it):

```
Ultra-realistic grounded product video in 9:16. The attached photo of the
Kettle is the exact product; the attached photo of the Kitchen is the exact
place. Style: morning window light, clean true colour, a 50mm frame at
counter height, shallow depth on the product, practical light only.
(0-5s) The kettle on the counter, steam just starting; the camera holds.
(5-11s) Hard cut, closer: a hand lifts it and pours into a cup, the stream
steady, steam rising into the light.
(11-16s) Reverse on the cup: two hands wrap round it as the window behind
goes from grey to sun. End abruptly.
No background music. Only diegetic sound: the kettle's tick, the pour, the
cup set down.
Avoid: on-screen text, logos drawn in, plastic AI sheen, CGI-looking skin,
cartoon reactions, dramatic slow motion, named films, brands or actors.
```

Show it to the person, then save with `write_scene`: `prompt`, `seconds`,
`refs` with the product first, `title`, `project_id`. A longer explainer is
several scenes, one per beat, each saved on its own and joined later.

## The render, then the join

1. `quote` prices the scene in credits, beside the `balance`: `keyframes` (one
   still per shot, with the credits for `each`) and `clip` (one render per
   timed shot, each with its credits and a `token`, and the total for all
   three shots above). Say the quote's credits and WAIT for a yes in chat.
2. On the yes, `approve` with `scene_id`, `what` "clip", the quote's `tokens`
   and the renderer choice it priced (`provider`, `model`, `frame`, `duration`):
   every shot without a clip yet, at exactly the quoted credits. `what`
   "keyframes" draws the stills first, on their own yes, to see the look
   before the clip. A token works once, for one hour; a stale quote is
   refused. `affordable: false`, or `insufficient_credits` (`needs`,
   `available`), means stop: credits are added in the studio.
3. `job` with `wait` until done; `scene` shows `keyframe`, `clips`, `rendered`.
4. Several scenes become one video with `assemble_clips`: their `gen:<id>`s
   from `library` in beat order, `transition` cut or crossfade, and an
   optional `music` bed that is an audio `asset:<id>` uploaded in the
   studio's editor. Free; it starts a job, so poll `job` with `wait`. The
   result is a new `gen:<id>` and an editable cut in the editor.
5. The captions (the name, the claims, the offer) and the recorded voice go
   on in that editor. Say so; never write them into the prompt.
6. One copy per platform with `reformat`: 9:16 for vertical feeds, 1:1 or
   4:5 for square ones, 16:9 for wide. `fit` pad keeps the whole picture;
   crop fills the frame. Each copy is a new library item; `share_link`
   hands one over as a download.

## Do not

- Never write dialogue, a voice-over or on-screen text into the scene.
- Never state a benefit, a number or a review the person did not give you.
- Never pass a URL as a ref; refs are ids exactly as `elements` lists them.
- Never call `approve` without the person's yes to that quote in this chat, or
  for more than it priced; never point them at a page for credits.
- Never say a render or a join has finished: read `scene` or `job`.
