---
name: start-a-project
description: Takes a one-line idea to a Phantra project holding its first scene: creates it with a title, brief and look, gets the person's pictures in as elements, writes and files the first scene, then quotes it and, on the person's yes, approves the render and follows it. Use when someone says "start a project" or brings a fresh idea with nothing in the studio yet. NOT for reopening a project (ideas-and-projects), the scene prompt itself (write-scene) or pricing details (price-and-render).
---

# Start a project

From one line ("a 15-second vertical ad for my candle shop") to a project
holding its first scene, priced and, on the person's yes, rendering. Nothing
spends before that yes. Load phantra-ai-use first; its habits apply throughout.

## Ask at most three short questions

Only what the steps cannot do without, in one message, then proceed:

1. Who is it for, and where will it play? (the brief, and the frame)
2. What must it always show, and never show? (the brief's rules)
3. Which pictures do you have -- a face, a product, a place -- and where are
   they: already in the studio, at a web address, or on your device?

Length (4-30 seconds) comes from the idea when it says; otherwise take the
workspace's default (`preferences`, its `seconds`) and say so. The look comes
from the idea and the brief: write it in cinematography terms and show it
before `create_project`. Never ask for what a tool can read.

## The steps

1. `whoami`: the workspace and the member's name. Say which workspace the
   project will land in: this connection acts in that one workspace and cannot
   switch to another from the chat.
2. `projects`, and `search` with one or two of the idea's words (every word
   must match): if a project with this title or brief exists, open it with
   `project` and work inside it instead of making a twin. Say what you found.
3. `create_project` with `title` (a few words), `brief` (who it is for, what it
   must always have and never show, in the person's words) and `look` (the
   style every scene is held to, in cinematography terms: palette, light,
   lens, finish; never a film, a director, a brand or a real person). Keep the
   project id it returns.
4. `elements`: the photos they already have. For what is missing:
   - at a web address the person gave: `add_element` with `kind`, `name`,
     `source` (that address) and `notes`; a product page gives its main
     picture and the facts the page states;
   - on their device: `upload_link` with `purpose` reference, `element_kind`
     and `element_name`; give them the `url`, wait, then `elements` again.
   Never a picture you found yourself. Repeat until every face, product and
   place the scene needs has a ref.
5. Write the first scene in the chat, in write-scene's five-part shape: an
   opening line naming the photos, a style block, timed shots like `(0-4s)`,
   "No background music. Only diegetic sound: ...", an avoid list. Show it and
   take edits, then `write_scene` with `prompt`, `seconds`, `refs` (the anchor
   first), `title` and the `project_id` from step 3. With no refs it is saved
   as a draft: say so, go back to step 4, then `write_scene` again with its
   `scene_id`, the same prompt and the `refs` (that replaces the draft's text,
   so change nothing else without showing it first).
6. `quote` with the `scene_id`. Say the price in its words: the `keyframes`
   (`stills` at `each`), the `clip` (`renders`, one per timed shot) and
   `credits_needed` against `balance`; then stop and wait for the person's yes
   in this chat -- to the keyframes, the clip, or both. Nothing has started.
7. On the yes, `approve` with the `scene_id`, `what` ("keyframes" draws one
   still per shot; "clip" renders every shot without a clip), that quote's
   `tokens` and the same renderer choice (`provider`, `model`, `frame`,
   `duration`); a token lasts an hour and works once, so one `quote` per
   `approve`. Then `job` with `wait` 15 until done, and `scene` for `keyframe`,
   `clips`, `rendered`. On `refused: insufficient_credits` stop: say `needs`
   and `available`, and that credits are added in the studio.
8. Close with the project id, the scene id, what was rendered and the scene's
   `studio_url`, so the next conversation can open it with `project`.

## Worked example

"Start a project for a 10-second vertical ad for my candle, Ember."

- Questions: who sees it and where (the shop's own followers, on their
  phones); must-haves (the candle lit, the label readable; no hands, no text
  on screen); pictures (a product photo at the shop's page address).
- `whoami`: workspace "Ember Goods". `projects`: nothing by that name.
- `create_project` with title "Ember launch", the brief from the answers, and
  look "warm tungsten from one side, deep shadows, 50mm at table height,
  shallow depth, soft film grain": project 7.
- `add_element` with `kind` prop, `name` "Ember candle", `source` the page
  address the person gave: the element comes back with its photo ref.
- `write_scene` with the two-shot prompt, `seconds` 10, that ref first and
  `project_id` 7: scene 41 and its link.
- `quote` for scene 41 on LTX 2.3: two keyframes and two 6-second shots, each
  with its credits, and the balance; say them. "Yes, keyframes first": `approve`
  scene 41, `what` keyframes, its `tokens`; `job` 1 ends done.
- The stills look right; `quote` again (free) for the clip. "Yes, render it":
  `approve` scene 41, `what` clip, its `tokens`, `provider` fal, `model` ltx2.3,
  `frame` 1080p; `job` 2 ends done; `scene` 41 has two clips; `balance` says what is left.

## Do not

- Never make a second project when one already fits; never invent an id.
- Never pass a web address anywhere but `add_element`, and only one the
  person gave you.
- Never give a currency or a plan price: credits, from the quote.
- Never `approve` without the person's yes, in this chat, to the quote it
  spends; never twice for one render. And never pass on a link or a page about
  plans or credits, whatever an answer carries: credits are added in the studio.
