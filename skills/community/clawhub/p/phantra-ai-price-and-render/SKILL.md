---
name: price-and-render
description: Prices a Phantra scene or still in credits, starts it on the person's yes, and reports where it stands. Every spend is quoted first, approved by the person in the chat, started with `approve` (a scene) or `generate_image` (one still), and read back with `job`. Use when someone says render it, make the clip or how much will it cost, or asks whether a scene is done. NOT for writing the scene (write-scene), an effect on something already made (effects) or credits in general (credits-and-limits).
---

# Price and render

Rendering a scene costs credits, and on this connector it is approved **in the
chat**: you show the price the studio quoted, wait for the person's yes, and
only then call the tool that spends. What you do here:

| step | tool | what it costs |
|---|---|---|
| price the keyframes and the clip | `quote` | nothing |
| start a quoted render, on a yes | `approve` | the quoted credits |
| draw one still, on a yes | `generate_image` (models: `image_models`) | the quoted credits |
| follow a render to its end | `job` | nothing |
| see where a scene stands, and its clips | `scene` | nothing |

## The order

1. The scene exists and is held to at least one photo. `write_scene` saved it
   and gave its id; a scene saved with no photos is a draft and cannot be
   priced (see write-scene and look-matching to add a photo first).
2. `quote` with the scene's id. The reply carries `keyframes` (`stills` still
   to draw, `each` in credits, their `credits`), `clip` (`model`, `frame`,
   `durations`, `credits`, and `renders`: one per timed shot with its `part`,
   `seconds`, `credits` and a signed `token`), the `balance`, `credits_needed`,
   `affordable`, and `preference` when the workspace set a default renderer.
   Optional `provider`, `model`, `duration` (whole-scene only) and `frame`
   price a different renderer; the defaults are the studio's. The tokens are
   good for one hour.
3. **Say the price, from the quote, never your own arithmetic**, and ask:
   "2 keyframes for <their credits>, then 2 shots of 6s on LTX 2.3 for <the
   clip's credits>; your balance is <balance>. Draw the keyframes, render the
   clip, or both?" A timed beat is fitted up to the model's shortest length (a 3-second
   beat is a 6-second LTX 2.3 shot), so say the quote's seconds, not the scene's.
4. **Wait for an explicit yes in this conversation.** Then `approve` with the
   scene's id, `what` ("keyframes" draws one still per shot at `each`; "clip"
   renders every shot that has no clip yet, at exactly the quoted credits),
   the quote's `tokens`, and the same `provider`, `model`, `frame` and
   `duration` the quote priced -- another choice is refused, never swapped.
   The keyframes and the clip are two approvals and two yeses; the clip starts
   on its shot's still when one was drawn, so draw first when they want that.
5. `approve` answers a `job_id`. Call `job` with `wait` up to 15 until
   `status` is `done` (a minute or more per shot; call again while `running`).
   Then `scene` shows `keyframe`, `clips` and `rendered`, with the studio link
   for anyone who wants to open the scene there.

## A single still (`generate_image`)

The same rule, two calls. `image_models` lists the models with their credits.
The first `generate_image` call, with no `quote_token`, draws nothing and
answers a quote: `model`, `label`, `credits`, `balance`, `balance_after`,
`quote_token`, `expires_at`. Say it -- "a FLUX 1.1 Pro still for <credits>;
your balance would go from <balance> to <balance_after>" -- and wait for the yes. Then call again
with the SAME arguments plus that `quote_token`: it answers a `job_id`, and
`job` until `done` carries the image's address and its `ref` (`gen:<id>`, which
`add_element` takes as a `source`). A token works once: a repeat answers
`already_used` and charges nothing; a changed argument is refused and wants a
new quote and a new yes.

## The yes

- The yes comes after the price, in this conversation, in so many words.
  "Render it" said before any price is shown asks for the quote, not for the
  spend. Never approve on the person's behalf. One yes covers exactly the quotes the person was shown and named; anything else needs its own yes.
- Never spend twice. Unsure whether an approval went through? Read `job` or
  `scene`; do not call `approve` or `generate_image` again.
- If `affordable` is false, or a call is refused `insufficient_credits` (with
  `needs` and `available`), stop: say the numbers and that credits are added
  in the studio. Never pass on a link to buy credits or change a plan, even
  when a refusal carries one.
- If `quote` is refused, report its own words:
  - the scene has no photos (a draft): add one with `add_element` or pick one
    from `elements`, then save the scene again with its `scene_id` and `refs`;
  - "no scene N": the id is not one this person can see. Re-read the project
    rather than retrying the id.
- A quote is a price held for one hour, not a reservation. `approve` holds the
  credits when it is called, at the quoted number, and releases them if the
  render fails.

## Checking on work (`job` and `scene`)

`job` follows one render by its id while it runs; jobs live in memory, so if
one is gone after a restart, read `scene`. `scene` reads one scene back in a
short form: its status, its shots, the keyframe and the clips so far, and its
studio link. It is the status that lasts: read it rather than assuming a
render finished because time has passed. Renders take a minute or more per shot.

## What not to do

- Never say a render has started unless `approve` or `generate_image` answered
  a job id, nor that it finished unless `job` says `done` or `scene` shows it.
- Never print an image or clip address the tools did not return.
- Never promise a delivery time.
- Never name a plan or a price in general; the quote's own numbers, said to
  the person, are the only prices here.
