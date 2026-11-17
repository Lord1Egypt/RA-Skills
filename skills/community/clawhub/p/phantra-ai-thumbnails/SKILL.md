---
name: thumbnails
description: Draws a cover image in Phantra (a YouTube thumbnail, a Reels, TikTok or Shorts cover, a feed cover) as a still with `generate_image`, in the platform's frame, with a few words that stay readable small, on a model from `image_models`; quoted first and drawn on the person's yes. Use when someone asks for a thumbnail, a cover, a title card or a poster frame. NOT for editing an existing still (effects), the first seconds of the video (hooks-and-first-seconds) or a set of ad stills (product-ad-set).
---

# Thumbnails and covers

A cover is one still: `generate_image` draws ONE image per call, quoted in
credits first and drawn only on the person's yes. Writing the prompt, picking
the model and making other shapes afterwards cost nothing.

## 1. What it is a cover for, and its frame

Ask what the video or post is about in one sentence, and where the cover
will be seen. Frames the studio advises (its advice, not a platform's rule):

| where | `aspect` |
|---|---|
| a YouTube video | 16:9 |
| a Reels, TikTok or Shorts cover | 9:16 |
| a feed post | 4:5 or 1:1 |

`image_models` lists the aspects every model takes. Draw the cover AT the
frame it will be shown in: text placed for 16:9 does not survive a crop.

## 2. One idea, readable small

A cover is seen at the size of a postage stamp. Agree with the person:

- **One subject, large**: a face with one clear expression, or one object.
  Close framing, off-centre, with clean space on one side for the words.
- **Few words**: four or fewer, in their words. The video's title already
  sits beside the cover, so the text adds to it and never repeats it.
- **Contrast**: a simple background, light against dark, one accent colour.
- **Clear edges**: keep text off the bottom of a 9:16 cover and the
  bottom-right of a 16:9 one, where apps draw their own labels.

Never put a claim, a number, a price, a quote or a result on a cover that
the person did not give you, and never draw a fake screenshot, a made-up
review or another company's logo.

## 3. The model

Call `image_models` and read each model's own line; never pick from memory.

- **Words on the image**: choose a model whose line says it is good at text
  or typography.
- **Their own face or product**: it must come from a photo. Choose a model
  whose `max_references` is 1 or more and pass the photo's `ref` (from
  `elements`) in `references`. A model with `max_references` 0 draws from the
  prompt alone and will not show their face or product; say so.
- **Both**: prefer a model whose line names text and takes references. When
  none fits, say the trade-off and let the person choose.

No photo yet? `upload_link` (with `element_kind` and `element_name`) for a
file on their device, or `add_element` for a picture at an address they gave.

## 4. The prompt

Write it as one still, in this order: the subject and what it is doing or
feeling; the framing (close, off-centre, which side is left clear); the
light; the background; then the exact words in quotes with where they sit
and how they look in plain craft terms (a heavy sans-serif, white with a
dark outline, two lines), and "no other text". Name no brand, film or
person for the look.

```
Close portrait, off-centre left, of the woman in the attached photo, eyebrows
raised, holding a cracked phone toward the lens. Hard key from the right,
deep blue shadow side. Plain dark teal background with a soft falloff. On
the right third, two lines of heavy white sans-serif with a thin dark
outline: "I FIXED IT" above "IN 5 MIN". No other text, no logos.
```

## 5. Quote, yes, draw

1. `generate_image` with `prompt`, `model`, `aspect` and `references`, and
   NO `quote_token`: it draws nothing and answers the quote (the model, the
   credits, the balance and the balance after, a `quote_token`).
2. Say the quote's own numbers and wait for an explicit yes in this chat.
3. Call again with the SAME arguments plus that `quote_token`. It answers a
   `job_id`; `job` with `wait` 15 until `done` gives the image's address and
   its `ref` (a `gen:<id>`).

A token works once and for exactly that request. Never draw on the person's
behalf, and never twice on one yes. `refused: insufficient_credits` means
stop: say what it needs and what there is, and that credits are added in
the studio.

## 6. Options and other shapes

- **A second option** is a second call, a second quote and a second yes.
  Change one thing (the words, the expression, the colour) so the choice
  means something. Say how many quotes a request for "a few" will be.
- **Another shape of the same cover**: `reformat` with its `gen:<id>`,
  `aspect` (9:16, 16:9, 1:1 or 4:5) and `fit` pad or crop. It costs no
  credits and the original is untouched. A crop can cut the words off: when
  the text matters in the new shape, draw the cover again at that `aspect`.
- **The file**: `share_link` with the `gen:<id>` gives a download link.
  Uploading the cover to the platform is the person's; nothing here posts.
