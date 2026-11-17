---
name: ugc-unboxing
description: Writes a UGC-style unboxing scene in Phantra: a person opening a package on their phone camera (the sealed box, the open, the product lifted out, a first touch of its details, a first impression in their own words), rendered against their own face, product and packaging photos. Use when someone asks for an unboxing, a "what arrived", a first-look or a package-opening video. NOT for a verdict after use (ugc-review), a general talk-to-camera ad (ugc-ad) or a product-only film (product-shots).
---

# UGC unboxing

An unboxing is the moment before the review: hands, a package, and what the
person thinks the first time they see the thing. Most of it is hands and
sound; the face appears at the start and the end. You write the prompt here
(free), save it with `write_scene`, then price it.

## The elements it needs

`elements`: a **character** (the face) and a **prop** (the product), each
with photos. The **packaging** matters here more than anywhere: ask for a
photo of the box or mailer as it arrives and add it as a second prop. Never
invent what a box, its print or its inserts look like; with no packaging
photo, write a plain unbranded mailer and say that is what will render.

Missing a picture? `upload_link` with `element_kind` and `element_name` for
a file on their device (give them the `url`, they pick the file, then
`elements` again), or `add_element` for the https address they gave you of
an image or of the product's own page. Never find or guess one for them. On
`write_scene` the face has role `subject` and goes FIRST, because the render
anchors on it; the product and the packaging are `product`.

## Whose words these are

Every line spoken, every claim ("it cleared my skin in a week"), every number
and every review comes from the person, in this conversation. Ask what they
want said and what they can stand behind, and use their words. Never write a
testimonial, a star rating, a "customers say", a before-and-after or a
statistic they did not give you, and never put a line in the mouth of a
customer, a friend or an expert. A claim you cannot source to them is left
out, and you say why.

An unboxing is a first impression, so it carries no claim about how the
product performs. Ask what is in the box (the product, a cable, a card) and
list only what they tell you; a made-up accessory is a made-up promise.

## The beats (12 to 20 seconds, three or four shots)

Each window is ONE shot of 2-10 s; windows run contiguously from 0 to the
total (a scene is 4 to 30 s).

1. **It arrived**: to camera, the sealed package held up, one line in their
   words. Mid-motion, no greeting.
2. **The open**: top-down on their hands and the package on a table; the
   tape or the lid, one action, the sound of it.
3. **The reveal**: the product lifted out toward the lens, label readable,
   packing falling away.
4. **First touch and first words**: close on a detail (weight in the hand,
   a texture, a cap turning), then up to their face for one honest line.
   End abruptly.

Phone feel, in craft terms: a phone propped overhead for the table shots and
held at arm's length for the face; the room's own light, no fill; small sway
when handheld, locked when propped; true colour. Sound carries an unboxing:
"No background music. Only diegetic sound: tape, card, tissue, their voice."

## A worked skeleton (replace everything; the quoted lines are the person's)

```
Ultra-realistic UGC-style unboxing in 9:16. The attached photo of Leo is his
exact face and clothing; the attached photo of the headphones is the exact
product; the attached photo of the box is the exact packaging. Style: phone
footage in a living room, daylight from the left, no fill; top-down shots
locked off, face shots handheld with small sway; true colour, phone
sharpness.
(0-3s) Leo to camera, the sealed box held up beside his face: "okay, it's
here."
(3-9s) Top-down, locked: his hands slit the tape and fold back the flaps,
tissue lifting.
(9-14s) He lifts the headphones out toward the lens, the box sliding out of
frame, the label side readable.
(14-18s) Close on his thumb running along the headband, then up to his
face: "heavier than I expected." End abruptly.
No background music. Only diegetic sound: tape, card, tissue, his voice.
Avoid: plastic AI sheen, invented text on the box, extra accessories, cartoon
reactions, slow motion, added captions or logos.
```

## Save, price and render

Show the prompt and take their edits. Then `write_scene` with `prompt`,
`seconds`, `refs` (the face first), `roles`, a `title`, and `project_id` when
it belongs to a project. `quote` the `scene_id`: it prices the keyframes and
the clip (one render per timed shot, each with a `token`) beside the
`balance`. Say the quote's own numbers and WAIT for a yes in this chat naming
what to run. Only then `approve` with `what` (`keyframes` or `clip`), the
quote's `tokens` and the same renderer choice; `job` (`wait` 15) until
`done`; `scene` shows the stills, the clips and the studio link. Tokens last
an hour and work once; an edit means a new `quote` and a new yes. Never
approve unasked or twice; refused `insufficient_credits`, stop and say
credits are added in the studio. The steps in full are price-and-render.
