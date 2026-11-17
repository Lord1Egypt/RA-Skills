---
name: ugc-ad
description: Writes a UGC-style ad scene in Phantra: a person talking to their phone camera about a product they hold, rendered against their own face and product photos in a handheld feel, with every spoken line and claim coming from the person. Use when someone asks for a UGC ad, a creator-style ad, a talk-to-camera product video or "something that looks like a customer filmed it". NOT for a verdict after use (ugc-review), an unboxing (ugc-unboxing) or a product-only scene with no face (product-shots).
---

# UGC-style ad

A UGC (user-generated content) ad looks like one person filmed themselves on
a phone talking about a thing they use. In Phantra that person is
the one you are talking to, or someone whose face they have the right to
use, and the thing is their own product: both are elements, and the scene is
held to those photos. The words are theirs too. You write the prompt here
(free), save it with `write_scene`, then price it (price-and-render).

## The two elements it needs

1. `elements`: find a **character** (the face) and a **prop** (the product).
   The ad renders against both; nothing is made up from a name.
2. Missing one? Ask the person for the picture. `add_element` takes the https
   address they gave you of an image file or of the product's own page
   (`kind` character or prop, a `name`, a few words of `notes`). A photo on
   their phone comes in through `upload_link` with `element_kind` and
   `element_name`: give them the `url`, they pick the file, then call
   `elements` again. Never find or guess a picture for them.
3. Roles on `write_scene`: the face is `subject`, the product is `product`.
   The face ref goes FIRST; the render anchors on it. The pack shot goes
   second; a room or mood photo after, as `place`, `light` or `palette`.

## Whose words these are

Every line spoken, every claim ("it cleared my skin in a week"), every number
and every review comes from the person, in this conversation. Ask what they
want said and what they can stand behind, and use their words. Never write a
testimonial, a star rating, a "customers say", a before-and-after or a
statistic they did not give you, and never put a line in the mouth of a
customer, a friend or an expert. A claim you cannot source to them is left
out, and you say why.

## The style block (phone feel, in craft terms)

Write it as cinematography, never as a brand or a creator's name: a phone's
front camera at arm's length, face or chest height, wide with slight edge
distortion; the room's own light (a window, a lamp, a mirror strip) with no
fill; handheld with small natural sway, no stabiliser gloss; true-to-life
colour, mild contrast, phone sharpness, a little noise in the shadows; a real
room soft behind them. Realism comes from the light and the sway, not from
roughness for its own sake.

## The shots (timed, with to-camera moments)

Two or more windows, each ONE shot of 2-10 s, contiguous from 0 to the total
(4-30 s; 15 is a good ad length). Mix to-camera and product moments:

- a to-camera open, mid-sentence, with the hook in their words;
- the product raised into frame, label to lens, then used (opened, applied,
  worn), hands and face in the same shot;
- a to-camera close with the one line they want remembered, cut abruptly.

Write what they say inside the shot ("Sam, to camera: '...'"). The voice is
diegetic: "No background music. Only diegetic sound: their voice, the room,
the product's own sounds."

A worked skeleton (replace everything in it; the quoted lines are the
person's, taken down from this conversation):

```
Ultra-realistic UGC-style ad in 9:16. The attached photo of Sam is her exact
face and clothing; the attached photo of the tin is the exact product and
label. Style: front phone camera at arm's length, face height, wide with
slight edge distortion; bathroom light from a mirror strip, no fill;
handheld with small sway; true colour, mild contrast, phone sharpness, light
shadow noise; the bathroom soft behind her.
(0-4s) Sam, mid-sentence to camera: "okay so I've been using this for two
weeks" -- she lifts the tin into frame, label to the lens.
(4-10s) Same setup, closer: she opens it, scoops with two fingers and works
it into the back of one hand, glancing up at the lens.
(10-15s) To camera, tin at her shoulder: "that's it, that's the whole
routine." End abruptly.
No background music. Only diegetic sound: her voice, the tin lid, a tap
dripping.
Avoid: plastic AI sheen, CGI-looking skin, cartoon reactions, slow motion,
added captions or logos, named brands or people.
```

## Save, price and render

Show the prompt, take their edits, then `write_scene` with `prompt`,
`seconds`, `refs` (face first), `roles`, `title`, and `project_id` when it
belongs to a project. Then `quote` the `scene_id`: it prices the keyframes
(`stills` x `each`) and the clip (one render per shot, each with `credits`
and a `token`; a window is fitted up to the model's shortest length) beside
the `balance`. Say the quote's numbers plainly -- the keyframes and their
credits, the shots and theirs, the balance -- and WAIT for a yes in this chat naming what to
run. Only then `approve` with `what` (`keyframes` or `clip`), the quote's
`tokens` and the same renderer choice; `job` (`wait` 15) until `done`;
`scene` shows the stills, the clips and the studio link. Tokens last an
hour and work once; an edit means a new `quote` and a new yes. Never approve
unasked or twice; refused for credits (`insufficient_credits`), stop and say
credits are added in the studio. Versions of this ad are ad-variations.
