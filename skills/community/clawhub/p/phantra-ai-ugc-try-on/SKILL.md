---
name: ugc-try-on
description: Writes a UGC-style try-on scene in Phantra: a person trying on clothing, shoes or an accessory for their phone camera (held up, worn, a mirror turn, a close detail, a verdict), rendered against their own face and photos of the actual garment, with nothing about their body changed. Use when someone asks for a try-on, a haul, an outfit or fit check, or a wear test. NOT for a general talk-to-camera ad (ugc-ad), a review of something not worn (ugc-review) or a garment with no person (product-shots).
---

# UGC try-on

A try-on answers one question: what does this look like on a real person.
So the two photos matter more than the writing. You write the prompt here
(free), save it with `write_scene`, then price it.

## The two elements it needs

`elements`: a **character** (the person, ideally a full-length photo) and a
**prop** (the actual garment, laid flat or on a hanger, front showing).
Missing one? Ask the person for the picture: `upload_link` with
`element_kind` and `element_name` for a file on their device (give them the
`url`, they pick the file, then `elements` again), or `add_element` for the
https address they gave you of an image or of the product's own page. Never
find or guess a picture for them. On `write_scene` the person has role
`subject` and goes FIRST, because the render anchors on it; the garment is
`product`. A second piece (the shoes, the bag) is another prop.

Say plainly what a render can and cannot promise: it shows the garment's
colour, cut and print on this person from the photos given; it is not a
fitting, and it cannot show how a size fits.

## Their body is theirs

Write "the attached photo is their exact face and build" and leave it there.
Never ask for, write or accept a slimmer, taller, smoother or otherwise
altered body, and put body reshaping and retouching in the avoid list.
The person shown is the one you are talking to, or someone whose likeness
they have the right to use.

## Whose words these are

Every line spoken, every claim ("it cleared my skin in a week"), every number
and every review comes from the person, in this conversation. Ask what they
want said and what they can stand behind, and use their words. Never write a
testimonial, a star rating, a "customers say", a before-and-after or a
statistic they did not give you, and never put a line in the mouth of a
customer, a friend or an expert. A claim you cannot source to them is left
out, and you say why.

For a try-on that means fit: "true to size", the size they are wearing,
their height, "it runs small" are said only if they said them.

## The beats (10 to 20 seconds, three or four shots)

Each window is ONE shot of 2-10 s; windows run contiguously from 0 to the
total (a scene is 4 to 30 s). The change of clothes is a CUT between two
shots, never a morph inside one.

1. **The piece**: to camera, the garment held up on its hanger, one line.
2. **Hard cut to wearing it**: full length in a mirror, phone in hand at
   chest height, a small step back.
3. **The turn**: a slow half turn, the back and the side seen, the fabric
   moving the way that fabric moves (say what it is: stiff denim, loose
   linen, heavy knit).
4. **A detail and the verdict**: close on a cuff, a waistband or a hem, then
   their face for one line. End abruptly.

Phone feel, in craft terms: a mirror selfie with the phone visible, or a
phone propped at hip height; the room's own light, no fill; small sway;
true colour, so the garment's colour is the photo's colour.

## A worked skeleton (replace everything; the quoted lines are the person's)

```
Ultra-realistic UGC-style try-on in 9:16. The attached photo of Maya is her
exact face and build; the attached photo of the jacket is the exact garment,
colour and stitching. Style: mirror selfie in a bedroom, phone in hand at
chest height, daylight from a window on the right, no fill; small handheld
sway; true colour, phone sharpness.
(0-3s) Maya to camera, the jacket held up on its hanger: "the green one
came."
(3-8s) Hard cut: full length in the mirror, wearing it open over a white
tee, she steps back half a pace.
(8-13s) Same mirror: a slow half turn, the stiff cotton holding its shape
across the shoulders.
(13-17s) Close on her hand turning back a cuff, then her face in the
mirror: "the sleeves are long on me." End abruptly.
No background music. Only diegetic sound: her voice, the fabric, the room.
Avoid: plastic AI sheen, CGI-looking fabric, body reshaping, retouching, a
different colour or cut from the photo, added captions or logos, slow motion.
```

## Save, price and render

Show the prompt and take their edits. Then `write_scene` with `prompt`,
`seconds`, `refs` (the person first), `roles`, a `title`, and `project_id`
when it belongs to a project. `quote` the `scene_id`: it prices the
keyframes and the clip (one render per timed shot, each with a `token`)
beside the `balance`. Say the quote's own numbers and WAIT for a yes in this
chat. Only then `approve` with `what` (`keyframes` or `clip`), the quote's
`tokens` and the same renderer choice; `job` (`wait` 15) until `done`;
`scene` shows the result. Tokens last an hour and work once. Never approve
unasked or twice; refused `insufficient_credits`, stop: credits are added in
the studio (price-and-render has the steps in full).
