---
name: look-matching
description: Sets the visual look of a Phantra scene from the person's elements and from an image or frame they describe or attach, says what each photo is FOR (its role), and explains what the studio can and cannot match. Use when someone says "make it look like this", attaches a reference image, asks for a mood, light or texture, or wants a photo used only for its light or palette. NOT for writing the whole scene (write-scene), prices (credits-and-limits), or finding or copying a real person's face.
---

# Look matching

Phantra renders a scene against **the person's own elements
(photos of characters, props, places)** (characters, props, places), never against a name or an
image somebody else chose for them. A look is written into the scene's style
block in cinematography terms; the photos decide identity, product and place.

## The rule on people

Never look for, describe for copying, or ask for a specific real person's
face. If the scene needs a face, it is the person's own or someone they have
the right to use, provided by them as an element. Say this plainly when asked
for a celebrity, a public figure or "someone who looks like X", and do not
add a picture of one with `add_element` or ask for one through `upload_link`.

## Working with the person's photos

- `elements` lists their characters, props and places with photo refs and a
  short description. Read it before writing a look: a room they photographed
  is a room the scene can be set in; a product they photographed is the exact
  product on screen.
- If the look needs a photo they do not have (a product, a location, a
  wardrobe), say which and ask them for it. Besides the studio's own Elements
  page, two ways in from the chat:
  - `add_element` files ONE picture as a character, prop or location. Its
    `source` is an https address **the person gave you** in this conversation
    (an image file -- jpg, png or webp -- or a product's page, whose main
    picture is taken), or `gen:<id>` of one of their own renders that
    `project` lists. Give it a `kind`, a `name` and a few words of `notes`. A
    name they already have of that kind gains the picture instead of making a
    second element. It draws nothing and spends nothing.
  - `upload_link` when the picture is on their phone or computer: call it
    with `purpose` reference and the `element_kind` + `element_name` it
    belongs to, give the person the `url`, and tell them to open it, pick the
    file and come back. One file (jpg, png, webp or heic), good for thirty
    minutes; afterwards `elements` lists it. Another file needs another link.
- Never give `add_element` an address you found or guessed, and never search
  for a picture on the person's behalf. The photo is theirs to choose.
- Refs go into `write_scene` as listed by `elements`, most important first:
  the face before the room, the product before the backdrop. The first ref is
  what the render anchors on.

## Say what each photo is for: roles

A photo is attached for WHAT IT SHOWS or for HOW IT LOOKS, and the scene must
know which. `write_scene` and `duplicate_scene` take `roles`, `{ref: role}`:

- `subject`, `product`, `place`: the picture is OF the thing on screen -- the
  exact face, the exact product, the exact room. With no role given, a photo
  is read this way.
- `light`, `palette`, `framing`, `style`: ONLY that is taken from the photo.
  A frame attached for its dusk light lends its light, not its street or the
  stranger in it; a palette photo lends its colours and nothing else.

Two rules the studio holds to, so hold to them when ordering `refs`:

1. **Adapt a reference's look, never copy its subject.** A look-only photo
   is translated into the style block; the people, products and places on
   screen come from the subject photos.
2. **A look-only photo is never the anchor.** The subject photo goes first in
   `refs`; a photo with a light, palette, framing or style role goes after.

Worked example: Sam's portrait, and a rain-soaked street at dusk the person
likes for its light, brought in through `upload_link`. `refs: [sam_ref,
street_ref]`, `roles: {street_ref: "light"}`. The street's blue-hour glow and
wet reflections go into the style block; Sam is the face; the street itself
is not on screen unless the beats put it there.

## Reading an attached image or video frame

When the person shares an image or a frame, translate it into the terms the
scene's style block uses, and offer that back for their yes: light (source,
direction, colour temperature, hardness, time of day); surfaces (wet, dusty,
matte, worn); framing (how close, what height, lens feel, depth of field);
palette and grade (saturated, muted, contrast); motion (what moves, how fast,
handheld or locked); finish (grain, softness, sharpness).

Say what the studio will match (light, surfaces, framing, palette) and what it
will not (a specific film's or campaign's authorship, a brand's logo, a
person's likeness). Do not promise it will "reproduce" the reference.

## Writing the look into the scene

The look lives in part 2 of the scene prompt (see write-scene): two or three
sentences in cinematography and colour-grade terms, the subject photos winning
over the look on anything they show. Realism comes from practical light,
believable physics and restraint. Never name a film, a director, a brand or a
real person in it.

## Reply shape

One short block, readable on a phone: which element photos the scene is held
to (by name, ref and role), and the look in the words that will go into the prompt.
