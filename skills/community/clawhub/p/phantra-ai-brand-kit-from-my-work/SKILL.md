---
name: brand-kit-from-my-work
description: Builds a brand kit from the person's own Phantra work: reads what they kept and posted, their library, elements and recipes, draws out palette, light, framing and product rules, confirms each, and saves the kit as a recipe and a project look. Use when someone says "make me a brand kit" or "what is my style", or wants new scenes to match what worked. NOT for a look from an attached reference image (look-matching), starting a project (start-a-project) or captions (hooks-and-first-seconds).
---

# Brand kit from my work

A brand kit here is a short set of visual rules -- palette, light, lens and
framing, finish, how the product and people are shown, what to avoid --
written in cinematography terms and read off what the person already made and
kept. Nothing is invented: every rule points at a render, a photo or a sentence
of theirs. Nothing in this skill renders or spends credits: the kit is read off
their work and saved, never drawn. Load phantra-ai-use first.

## 1. Read their work (every call is free)

1. `what_works`: what they kept per model and preset, how many tries a keeper
   takes, what they posted and its numbers. If `enough_data` is false, say so:
   the kit then leans on their photos and their own words.
2. `library` with `kind` render, then `kind` upload: the renders they made,
   each with its model, frame, project and the first words of its prompt. For
   the look words that recur, read the full prompt with `scene` on the scene
   ids `recent` and `project` list. Weigh the posted ones most: `what_works`
   names each posted scene's `scene_id`. Nothing marks a render as kept, so
   ask the person which they count as their best.
3. `elements`: the faces, products and places every scene is held to; a
   product's notes often state its colour, material and size.
4. `recipes`, then `recipe` for any of their own: a way of working they
   already wrote down is the kit's first draft, not something to replace.
5. `recent`, and `project` on their main projects: a `look` already saved
   there, the brief's must-haves and nevers, and what the project learned.

## 2. Draw out the rules

For each heading write one or two lines, and after each a note of where it
came from ("from the 4 kept renders", "from the Ember candle notes", "you
said"). Leave a heading out rather than guess.

- **Palette**: the two or three colours that recur, and their contrast.
- **Light**: source, direction, colour, hardness (one window; warm tungsten
  from camera left; overcast skylight).
- **Lens and framing**: focal length feel, camera height, depth of field,
  movement (locked off, slow push, handheld).
- **Finish**: grade, grain, contrast, texture.
- **People and product**: how the face is shown, how the product sits in
  frame, what is always in shot and what never is.
- **Avoid**: what they discarded or asked never to see.

Never name a film, a director, a brand or a real person for the look. Say
nothing about taglines, claims, reviews, numbers or awards: what the brand
SAYS is the person's to write, never yours.

## 3. Confirm, then save

1. Show the kit as a list and ask them to keep, change or strike each rule.
   Only confirmed rules are saved.
2. `save_recipe` with a `name` (letters, numbers and hyphens; not a name the
   studio's shelf uses, such as product-still) and the confirmed rules as
   `body`. Saving the same name again keeps a new version; nothing is
   overwritten. Add a `project_id` when the kit belongs to one project.
3. Make it the look scenes are held to: `create_project` with `look` set to
   the kit's palette, light, lens and finish lines, plus a `title` and `brief`
   -- a new project for the next piece of work. A project that already carries
   a look keeps it; say which project got the kit.
4. Offer the next step: write-scene inside that project, where the opening
   line and the style block follow the kit.

## Worked example

"Make me a brand kit from what I've done so far."

- `what_works`: 9 outputs, 4 kept, all on one model; `enough_data` true.
- `what_works` names one posted scene; `scene` on it and on the three scenes
  the person calls their best: all four prompts say "one window, soft
  daylight", "35mm at chest height", "true colour, gentle contrast".
- `elements`: the "Ember candle" notes say amber glass, cream label.
- Draft: Palette -- amber, cream, warm grey (from the 4 kept renders); Light
  -- one soft window from camera left (same); Lens -- 35mm, chest height,
  shallow when close (same); Product -- candle lit, label to camera, no hands
  (from the candle notes and your brief); Avoid -- hard flash, text on screen
  (you said).
- They strike "warm grey" and keep the rest. `save_recipe` with `name`
  "ember-brand-kit" and those lines; `create_project` "Ember spring" with the
  look lines. Report the recipe's `name` and `version` and the project's id.

## Do not

- Never state a rule you cannot point at a render, a photo or their words.
- Never save before they confirmed; never pass a web address anywhere.
