---
name: product-ad-set
description: Turns one product photo into a set of Phantra ads: three or four ad stills in different styles and, when wanted, two or three short video ads with different hooks. Agrees the set, quotes every still and scene separately and makes only what the person says yes to. Use when someone asks for ads, a campaign or a launch set, or gives a product photo and says "make me ads". NOT for one product film (product-shots), a person to camera (ugc-ad) or versions of an existing ad (ad-variations).
---

# A set of ads from one product photo

One photo of the product in, a handful of finished ads out. A still is drawn
by `generate_image`, ONE image per call; a video ad is a scene. Each still
and each scene has its own quote in credits and runs only on the person's
yes. Planning, writing and saving cost nothing.

## 1. Get the product in

`elements`: is the product there as a **prop** with a photo? If not, ask:

- a file on their device: `upload_link` with `purpose` reference,
  `element_kind` prop and `element_name`; give them the `url`, they pick the
  file, then call `elements` again;
- a picture or the product's own page at an address THEY gave you:
  `add_element` with `kind` prop, a `name` and that address as `source`
  (from a page, its main picture is taken and what the page states about
  the product is kept in the notes). Never an address you found.

No photo at all? A still can be drawn from words alone, but it will not be
their exact product or label. Say so and let them choose.

## 2. Agree the set before anything is quoted

Offer directions in craft terms, never as a brand's or an artist's name:

- **Studio hero**: the product alone on a seamless sweep, one soft key and
  a rim, a clean reflection under it.
- **In use**: in a hand or on a real surface (a desk, a gym bench, a
  kitchen counter) in daylight.
- **Macro**: a few centimetres from one detail, shallow depth.
- **Bold graphic**: a flat colour field, the product large, a short
  headline in their words.

Then say the size of the set plainly: "four stills is four quotes, and each
video ad is its own quote". Agree the frame (4:5 or 1:1 for a feed, 9:16
for a story), and keep the set together with `create_project` (a title, a
brief, a look), passing its `project_id` on every call below.

Every headline, claim, number, price and offer on an ad comes from the
person. Never write a discount, a review, a "best-selling" or a result they
did not give you.

## 3. The stills

1. `image_models`: read each model's own line. To show THEIR product,
   choose a model whose `max_references` is 1 or more and pass the prop's
   `ref` in `references`; a model with 0 draws from the prompt alone. For a
   headline on the image, prefer one whose line says it is good at text.
2. Write one prompt per style: the product ("the attached photo is the
   exact product and label"), where it sits, the light, the lens, the
   background, any words in quotes with their place, and "no other text".
3. For each still, `generate_image` with `prompt`, `model`, `aspect`,
   `references` and NO `quote_token`: it draws nothing and answers a quote.
4. Show the quotes together, one line each, in the quotes' own numbers, with
   the balance. WAIT. The person names which to draw; a still they did not
   name is not drawn.
5. For each one named, call `generate_image` again with the SAME arguments
   plus its own `quote_token`; `job` with `wait` 15 until `done` gives the
   image's address and its `ref` (a `gen:<id>`).

## 4. The video ads (when wanted)

1. Write the first ad as a scene: two or three timed shots, 6 to 15 seconds,
   the pack shot the FIRST ref with role `product` (write-scene and
   product-shots have the shape). Save it with `write_scene`.
2. For each other hook, `duplicate_scene` with that `scene_id` and a
   `prompt` whose FIRST window alone is rewritten (the product arriving in
   frame, a hand reaching for it, a detail first). One change per copy.
3. `quote` each `scene_id`: the keyframes and the clip, one render per timed
   shot, with a `token` each. Show the quotes side by side and WAIT.
4. On a yes to a named scene, `approve` with that `scene_id`, `what`
   (`keyframes` or `clip`), its `tokens` and the same renderer choice;
   `job` until `done`; `scene` shows the clips.

## 5. Hand over the set

`library` (with `project_id`) lists everything made, by `gen:<id>`.
`reformat` makes another shape of any still or clip (`aspect` 9:16, 16:9,
1:1 or 4:5; `fit` pad or crop) at no credit cost, and `share_link` gives a
download link for each. Later, `what_works` reads which they kept.

## The spending rules

- One yes covers exactly the quotes the person was shown
  and named; anything else needs its own yes. Never draw or approve on their behalf,
  and never a second time on one yes.
- A token is good for one hour and for exactly that request; a changed
  prompt, model or frame needs a new quote and a new yes.
- `refused: insufficient_credits` (with `needs` and `available`): stop, say
  both numbers and that credits are added in the studio. Offer a smaller
  set.
- Never state a price yourself or add quotes up in your head: read each
  number from its quote.
