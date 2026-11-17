---
name: ugc-tutorial
description: Writes a UGC-style tutorial scene in Phantra: a person showing their phone camera how they use a product, one step per shot, the result first and last, rendered against their own face and product photos, with every step, quantity and tip coming from them. Use when someone asks for a tutorial, a how-to, a routine, a step-by-step clip or a get-ready-with-me. NOT for a verdict (ugc-review), a narrated explainer with no person (explainer) or a general talk-to-camera ad (ugc-ad).
---

# UGC tutorial

A tutorial shows a way of doing something, in the order it is done, by the
person who does it. Each step is one shot, because each timed shot is
rendered as its own clip: one action, one camera setup, 2 to 10 seconds. You
write the prompt here (free), save it with `write_scene`, then price it.

## The two elements it needs

`elements`: a **character** (the face) and a **prop** (the product), each
with photos. Missing one? Ask the person for the picture: `upload_link` with
`element_kind` and `element_name` for a file on their device (give them the
`url`, they pick the file, then `elements` again), or `add_element` for the
https address they gave you of an image or of the product's own page. Never
find or guess a picture for them. On `write_scene` the face has role
`subject` and goes FIRST, because the render anchors on it; the product is
`product`. A tool or a second product used in a step is another prop.

## Whose words these are

Every line spoken, every claim ("it cleared my skin in a week"), every number
and every review comes from the person, in this conversation. Ask what they
want said and what they can stand behind, and use their words. Never write a
testimonial, a star rating, a "customers say", a before-and-after or a
statistic they did not give you, and never put a line in the mouth of a
customer, a friend or an expert. A claim you cannot source to them is left
out, and you say why.

In a tutorial that covers the method itself. Ask for the steps as THEY do
them and write those: never add a step, a quantity, a waiting time, a
temperature or a safety instruction of your own, and never promise a result
("in one week") they did not state. When a step needs a warning, ask them
for it rather than writing one.

## The beats (15 to 30 seconds, one step per shot)

Windows run contiguously from 0 to the total (a scene is 4 to 30 s), which
fits three or four steps. More steps is a second scene, joined afterwards
with `assemble_clips` (no credits).

1. **The result first**: the finished look, dish or setup, held up or
   turned to the lens, with their promise in one line.
2. **Step one**, then **step two**, then **step three**: each a single
   action in close-up, hands and product in frame, their instruction said
   while doing it ("two pumps, palms first").
3. **The result again**, to camera, same framing as the open. End abruptly.

Keep the framing the same from step to step (same surface, same height,
same light) so the cuts read as one continuous session. Phone feel, in
craft terms: a phone propped at chest height or held at arm's length; the
room's own light, no fill; true colour and phone sharpness. "No background
music. Only diegetic sound: their voice and the product's own sounds."

## A worked skeleton (replace everything; the quoted lines are the person's)

```
Ultra-realistic UGC-style tutorial in 9:16. The attached photo of Ines is her
exact face and clothing; the attached photo of the hair oil is the exact
product and label. Style: phone propped at chest height on a bathroom shelf,
light from a mirror strip, no fill; locked frame; true colour, phone
sharpness; the same framing in every shot.
(0-4s) Ines turns her head so the finished hair catches the light, to
camera: "this is the whole routine, three steps."
(4-10s) Close on her palm: two pumps of oil from the bottle, label to the
lens: "two pumps, warm it up."
(10-17s) Medium: she works it through the ends only, head tilted: "ends
first, never the roots."
(17-23s) Close: she twists one section round a finger and lets it fall:
"twist, and leave it."
(23-27s) Same framing as the open, to camera: "that's it." End abruptly.
No background music. Only diegetic sound: her voice, the pump, the room.
Avoid: plastic AI sheen, CGI-looking hair or skin, on-screen step numbers or
captions, slow motion, named brands or people.
```

## Save, price and render

Show the prompt and take their edits. Then `write_scene` with `prompt`,
`seconds`, `refs` (the face first), `roles`, a `title`, and `project_id` when
it belongs to a project. `quote` the `scene_id`: it prices the keyframes and
the clip (one render per timed shot, each with a `token`) beside the
`balance`; more steps means more shots to render, so say the count. Say the
quote's own numbers and WAIT for a yes in this chat naming what to run. Only
then `approve` with `what` (`keyframes` or `clip`), the quote's `tokens` and
the same renderer choice; `job` (`wait` 15) until `done`; `scene` shows the
stills, the clips and the studio link. Tokens last an hour and work once; an
edit means a new `quote` and a new yes. Never approve unasked or twice;
refused `insufficient_credits`, stop and say credits are added in the
studio. The steps in full are price-and-render.
