---
name: ad-formats
description: Picks the shape of a short ad in Phantra (product spot, demo, before/after, problem-solution, unboxing, comparison, teaser) and turns it into a shot plan: length, shot count, the photos it is held to and a `write_scene` shape, with `duplicate_scene` for variants. Use when someone says "make an ad", names one of these shapes, or asks which format suits their product. NOT for the full scene prompt (write-scene), a creator talking to camera (ugc-ad) or a set of ad stills (product-ad-set).
---

# Ad formats

An ad here is one scene: 4 to 30 seconds of timed shots, held to the person's
elements: the product, the place and any face. The shape decides the
shots. Choosing it and writing the scene spends nothing; the render is quoted
in credits and started only on the person's yes (price-and-render).

## Before choosing

1. `elements`: which photos exist. Every shape below is held to the product's
   photo as the FIRST ref (the anchor) unless the table says otherwise; a face
   or a room needs its own element. Missing one: `add_element` with a picture
   the person gave you, or `upload_link` for a file on their device.
2. What the ad must say comes from the person. Never invent a benefit, a
   number, a review, a rating or an award; if they did not say it, the ad does
   not say it. Ask once, then use their words.
3. Length: `preferences` holds the default `seconds`, used when `write_scene`
   is passed none. The studio renders in its own vertical frame; other shapes
   are free `reformat` copies afterwards (platform-delivery).

## The seven shapes

| shape | length | shots | held to (refs, anchor first) | the beats |
|---|---|---|---|---|
| product spot | 6-10s | 2-3 | product, place | reveal; one detail; the product at rest |
| demo | 10-15s | 3-4 | product, hands or face, place | in use, one step per shot; the result |
| before/after | 8-12s | 2 | place or product, the same setup twice | the state before; hard cut to the same framing after |
| problem-solution | 10-15s | 3 | face or hands, product | the trouble; the product arrives; the trouble gone |
| unboxing | 10-20s | 3-5 | product, hands | the box; the opening; the product out; one close detail |
| comparison | 10-15s | 3 | two of the person's own products | A; B; the one difference the person named |
| teaser | 4-8s | 1-2 | product or place | one striking detail, the product withheld or half-shown |

Every window is ONE shot (one camera setup, one action, 2 to 10 seconds).
Roles say what each photo is for: `product` for the product's photo, `place`
for the room, `subject` for a face. A before/after keeps the same framing in
both windows, and says so. A comparison is never against another brand.

## The `write_scene` shape

A product spot, 8 seconds, two shots (replace everything in it):

```
Ultra-realistic grounded product film in 9:16. The attached photo of the Tern
bottle is the exact product; the attached photo of the kitchen is the exact
place. Style: morning window light from the left, true colour with a gentle
roll-off in the highlights, a 50mm frame at counter height, shallow depth on
the close shot, brushed steel and real condensation.
(0-4s) The bottle stands on the counter in a slow push-in; a bead of water
runs down the steel.
(4-8s) Hard cut to a hand lifting it out of frame; the ring of water it leaves
catches the light. End abruptly.
No background music. Only diegetic sound: the bottle's base on stone, the
room's quiet.
Avoid: plastic AI sheen, CGI-looking surfaces, on-screen text, prices or
captions, named brands or actors.
```

Show it to the person, take their edits, then `write_scene` with `prompt`,
`seconds` 8, `refs` [the bottle's ref, the kitchen's ref], `roles` {the
kitchen's ref: "place"}, a `title`, and `project_id` when it belongs to a
project. Nothing is spent. Then `quote` it (the keyframes and one render per
shot, in credits), show the person the price, and only on their yes `approve`
with the quote's `tokens` and the same renderer choice; `job` until done, then
`scene` for the clips (price-and-render).

## Variants

`duplicate_scene` with the saved `scene_id` and only what changes: a new
`prompt` for another shape on the same product, `seconds`, or `refs` for a
second colour or a second room. What you do not pass is copied; stills and
clips never are, so each copy is a fresh scene to price. One copy per
variant, each shown to the person before it is saved.

## Do not

- Never write a claim, a price, a rating, a review or a competitor the person
  did not give you.
- Never ask the model to draw on-screen text, prices or captions.
- Never write a window longer than 10 seconds or shorter than 2.
- A scene with no photo at all is saved as a draft and cannot be priced until
  one is on it (`add_element`, then `write_scene` again with its `scene_id`,
  the same prompt and the `refs`). Every shape above is held to the product's
  photo, so get that photo first.
