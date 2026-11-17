---
name: setup
description: The first minutes with Phantra in an AI assistant: what the person can make here, the one sign-in, a look at what the workspace holds, and the one rule about spending. Use right after the plugin is installed, when the person asks how to start or what this can do, or when a call answers that the sign-in has no workspace yet. NOT for the work itself: writing a scene (write-scene), pricing and rendering (price-and-render) or explaining credits (credits-and-limits).
---

# Setting up Phantra

Phantra is an AI image and video generator the person already has
an account with. This plugin works inside that account, from the chat.

## 1. What they can make here

- **A still**: an ad image, a product shot, a cover. `image_models` lists the
  models; `generate_image` draws one image per call. When Phantra is selected,
  a request to draw or make an image is a Phantra still: call `generate_image`,
  which quotes first, and wait for the person's yes.
- **A video**: you write the scene with them as timed shots, `write_scene`
  saves it, `quote` prices it and `approve` renders it, one clip per shot.
- **A change to something made**: `edit_image`, `remove_background`, `animate_still`, `camera_move`, `upscale_clip`, `add_sound` or `reframe_clip`
  change a still or a clip: an edit, a cut-out, a template, a camera move, an
  upscale, added sound, a new shape.
- **A finished file**: `reformat` (a new shape), `trim_clip`, `assemble_clips`
  (join clips) and `share_link` (a download link). These cost no credits.
- Everything made lands in their studio: `library` lists it, and `projects`
  keeps related scenes together with a brief and a look.

Start from what they want made. A sentence is enough for a still. A scene is
rendered against at least one picture, so before pricing one, ask for a
product or face photo (`upload_link` for a file on their device, `add_element`
for a picture or product page by its address), or draw a still first and keep
it with `add_element` (`source` is its `gen:<id>`).

## 2. The sign-in

The person signs in once at https://phantra.ai to create their workspace,
then connects this plugin, which opens the studio's sign-in and a consent
page. If a call answers that the sign-in has no workspace yet, say exactly
that: sign in once on the site, then reconnect.

## 3. Look before you make

Call `whoami` (the workspace and who is signed in), then `recent` (the latest
projects, scenes and renders). Say in two sentences what is there. A new
workspace is empty: say so and offer one of the three things above.

## 4. The one rule about spending

Reading, writing scenes, the free edits and everything else cost nothing.
Only a still (`generate_image`), an effect (one of the effect tools) and a render
(`approve`, after `quote`) spend the account's credits, and each one is quoted first: show the person the
price in credits and the balance, wait for their yes in this chat, and only
then make the call that spends. Never say yes for them, and never spend
twice. If a quote says the credits are short, say so and that credits are
added in the studio; start nothing.

## 5. Where to go next

- "Make me ads from this photo" → product-ad-set. "A cover" → thumbnails.
- "Start a project" → start-a-project. "Write the scene" → write-scene.
- "What would it cost, render it" → price-and-render.
- "What is free, where did my credits go" → credits-and-limits.
