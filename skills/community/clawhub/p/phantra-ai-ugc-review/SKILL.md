---
name: ugc-review
description: Writes a UGC-style review scene in Phantra: a person telling their phone camera what they think after using a product (the verdict, the one thing they noticed, the product in use, an honest drawback), rendered against their own face and product photos, every word of the verdict theirs. Use when someone asks for a review video, a testimonial-style spot, an "honest review" or a verdict to camera. NOT for a general talk-to-camera ad (ugc-ad), an unboxing (ugc-unboxing) or a how-to (ugc-tutorial).
---

# UGC review

A review is one person's verdict on a thing they have used, said to their
phone. It differs from an ad in its order: the opinion comes first, then the
evidence. You write the prompt here (free), save it with `write_scene`, then
price it. The person reviewing is the one you are talking to, or someone
whose face they have the right to use.

## The two elements it needs

`elements`: a **character** (the face) and a **prop** (the product), each
with photos. Missing one? Ask the person for the picture: `upload_link` with
`element_kind` and `element_name` for a file on their device (give them the
`url`, they pick the file, then `elements` again), or `add_element` for the
https address they gave you of an image or of the product's own page. Never
find or guess a picture for them. On `write_scene` the face has role
`subject` and goes FIRST, because the render anchors on it; the product is
`product`.

## Whose words these are

Every line spoken, every claim ("it cleared my skin in a week"), every number
and every review comes from the person, in this conversation. Ask what they
want said and what they can stand behind, and use their words. Never write a
testimonial, a star rating, a "customers say", a before-and-after or a
statistic they did not give you, and never put a line in the mouth of a
customer, a friend or an expert. A claim you cannot source to them is left
out, and you say why.

For a review, ask four things before writing: how long they have used it,
the one thing they noticed, what they did not like (a review with no
drawback is theirs to choose, never yours to invent), and who they would
tell to buy it. A score or a star rating appears only if they gave one.

## The beats (15 to 25 seconds, three or four shots)

Each window is ONE shot of 2-10 s; windows run contiguously from 0 to the
total (a scene is 4 to 30 s).

1. **The verdict, to camera**, mid-thought: their opinion in one line, the
   product already in their hand.
2. **The thing they noticed, shown**: the product in use, hands and face in
   the same shot, their line about it said while doing it.
3. **The drawback**, if they gave one: to camera, plainly, no apology.
4. **The bottom line**, to camera: who it is for, in their words. End
   abruptly, without a sign-off.

Phone feel, in craft terms: the front camera at arm's length, face height,
slight wide-angle distortion; the room's own light, no fill; small handheld
sway; true colour and phone sharpness. The voice is diegetic: "No background
music. Only diegetic sound: their voice, the room, the product."

## A worked skeleton (replace everything; the quoted lines are the person's)

```
Ultra-realistic UGC-style review in 9:16. The attached photo of Dana is her
exact face and clothing; the attached photo of the flask is the exact product
and label. Style: front phone camera at arm's length, face height, slight
edge distortion; daylight from a kitchen window, no fill; handheld with small
sway; true colour, phone sharpness; the kitchen soft behind her.
(0-5s) Dana, mid-thought to camera, flask in hand: "three weeks in, and
I've stopped buying coffee out."
(5-12s) Same setup, closer: she unscrews the lid and pours, steam rising:
"it was still hot at four in the afternoon."
(12-17s) To camera, a small shrug: "the lid is fiddly with one hand."
(17-22s) To camera, flask at her shoulder: "if you commute, get it." End
abruptly.
No background music. Only diegetic sound: her voice, the lid, the pour.
Avoid: plastic AI sheen, CGI-looking skin, cartoon reactions, added captions,
star ratings or review text on screen, named brands or people.
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
credits are added in the studio. The steps in full are price-and-render;
shorter or re-ordered versions are ad-variations.
