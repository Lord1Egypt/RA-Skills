---
name: product-shots
description: Writes a product-led Phantra scene: the product as the subject, in macro and turntable shots, held to the person's own product photos, and says what a 4:5 or 1:1 reformat does afterwards. A pack-shot still can be drawn too (`generate_image`, quoted first). Use when someone asks for product shots, a product video, a pack shot in motion or a hero clip. NOT for a person to camera (ugc-ad), a set of ad stills (product-ad-set) or A/B versions (ad-variations).
---

# Product shots

A product scene is held to the person's own product photos: the exact
object, label and colour on screen come from them, and the scene's job is to
light it, move around it and show its surfaces. The clip is a **scene**, written
here free, saved with `write_scene`, quoted, and rendered on the person's yes.

## Get the product in as a prop

1. `elements`: is the product there as a **prop** with photos? Its `description`
   says what the studio read off them (name, colour, size).
2. If not, ask the person for it. `add_element` with `kind` prop, a `name`
   and `source`: the https address they gave you of the product's own page
   (its main picture is taken, and what the page states about the product
   is kept in the notes as copied text) or of an image file. A photo on
   their device comes in through `upload_link` with `element_kind` prop and
   `element_name`: hand them the `url`, they pick the file, then `elements`
   again. One picture per call; the same name again adds to it. Never give
   `add_element` a picture you found yourself.
3. Two or three photos help: a clean pack shot (front, label readable) and
   one showing the top or the back. Ask rather than guess what the back
   looks like.

## Roles and anchor

On `write_scene` the pack shot is the FIRST ref with role `product`: the
render anchors on it. A photo attached for its lighting alone (a mood frame,
a surface) gets `light`, `palette` or `style` and goes after; a look-only
photo is never the anchor. A room photo gets `place`.

## The style block: surfaces and reflections

Name the surfaces, because they are what the model renders: the product's
own finish (matte card, brushed metal, glass with visible thickness, frosted
plastic) and what it sits on (wet slate, linen, a mirror, raw concrete). Say
where reflections come from and how sharp they are: one large soft source
gives a long soft highlight down a bottle; a hard point source gives a small
bright one. Say the background (a seamless sweep, a dark falloff, a real
counter) and the lens (a macro a few centimetres away, or a 50-85mm at table
height with shallow depth). Say "label faces the lens and stays readable".
No brand is named for the look; the product's own name is on its label.

## Shot patterns (each window ONE shot, 2-10 s)

- **Macro drift**: the lens a few centimetres from one detail (cap, seam,
  embossed name), a slow push or slide, focus racking from texture to label.
- **Turntable**: the product on a slow rotating surface, camera locked, a
  half or full turn in 4-6 s, the highlight sliding across it as it turns.
- **Reveal**: a hand sets it down, a lid lifts, mist clears; one action,
  then still.
- **Hero hold**: locked three-quarter view, a slow 10-degree orbit, light
  wrapping the edge.

Two or more windows, contiguous from 0 to the total (4-30 s; 8-12 is usual).
Sound is diegetic: "No background music. Only diegetic sound: the surface,
the cap, the pour, the turntable's quiet motor."

## Worked skeleton (replace everything in it)

```
Ultra-realistic product film in 9:16. The attached photo of the serum bottle
is the exact product, label and colour. Style: amber glass with a visible
wall and a brushed-metal cap; one large soft source high left giving a long
soft highlight down the bottle, a hard rim from behind right; wet black
slate with a sharp inverted reflection; dark seamless falloff; macro at 5 cm
for details, 85mm at table height for the whole; shallow depth, true colour,
no bloom.
(0-4s) Macro on the cap's brushed grain, a slow slide down to the label,
focus racking onto the name. Label faces the lens.
(4-10s) Hard cut: the bottle on a slow turntable, locked 85mm, a half turn,
the highlight sliding round the glass, the reflection turning with it.
No background music. Only diegetic sound: the turntable's faint motor, one
drop of water on slate.
Avoid: plastic AI sheen, invented text on the label, extra bottles, lens
flare, named brands for the look.
```

## Save, quote, approve, and the shape afterwards

Show the prompt, take edits, then `write_scene` (`prompt`, `seconds`, `refs`
pack shot first, `roles`, `title`, `project_id`). `quote` it: `keyframes`
(`stills` x `each`), `clip` (a render per timed shot, each with a `token`) and
`balance`. Say them in the quote's own numbers -- the model, the shots and
their credits, the keyframes, the balance -- and WAIT for an explicit yes; only then `approve`
(`what` clip or keyframes, the quote's `tokens`, its renderer choice), `job`
until done; `scene` shows `clips`. A still is `generate_image` (the prop's
`ref` in `references`; `image_models` says which take them): the first call is
the quote only, the same call plus its `quote_token` the draw, once. Never
approve for the person or reuse a token; `refused: insufficient_credits` means
stop: credits are added in the studio. Once a clip has landed, `reformat` (its
`gen:<id>` from `library`) makes a copy in 4:5 or 1:1 for a feed (free, a
`job`, the source untouched): `fit` pad keeps the whole picture with black bars
where the shapes differ; `fit` crop fills the frame and keeps the middle, which
is why the product should sit near the centre of the scene.
