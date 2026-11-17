---
name: client-treatment
description: Writes a one-page client treatment (a pitch) for a Phantra project from what it holds: brief, look, scenes and references (`project`), renders (`library`), a clip link (`share_link`) and what worked before (`what_works`). Use when someone asks for a treatment, a pitch, a one-pager or a proposal. Claims, numbers and awards come from the person, never invented. NOT for writing the scenes (write-scene), planning the sequence (storyboard) or prices (credits-and-limits).
---

# Client treatment

A treatment is the page a client reads before saying yes: the idea, why it
fits them, what it will look like, what they get and what happens next. You
write it in the chat, paste-ready, from the project's own material. Nothing
here renders or spends.

## Gather (every call is read-only)

1. `projects` to find the project; `project` with its id (and `chat_turns`,
   up to 40) for the brief, the look, what it learned, its scenes with their
   status, the references they used, its renders and the latest chat. The chat
   is where the person said what the client asked for; read it first.
2. `library` with `project_id` and `kind` video for the renders; pick the one
   that shows the idea best (`origin` says render or upload). A `library` row
   names no scene: the render's scene id is the `scene` field on `project`'s
   renders list, so `scene` with that id says which beat it is.
   `share_link` with that `gen:<id>` (and `hours`, up to 168) gives a download
   link: anyone holding it can download the file, so hand it to the person for
   their own email, never paste it into the page.
3. `what_works` for evidence: what the person kept, per model and preset, and
   what they posted with its numbers. Use it only when `enough_data` is true,
   and present it as the person's own history ("our last three posted shorts
   averaged ..."), never as the client's results and never as a promise.
4. Ask the person for what the project cannot tell you: the client's name,
   the goal, the deliverables (shapes, lengths, how many), the timeline, and
   any claim they want on the page.

## The page (in this order, one page)

1. **Title and one line.** The piece's name and what it is, in one sentence.
2. **The idea.** Two or three sentences from the brief: what we see, why it
   holds, how it ends.
3. **Why it works for [client].** Tie the idea to the goal the person gave.
4. **The look.** The project's look in cinematography and colour-grade terms:
   light, palette, lens, finish. Never name a film, a director, a brand or a
   real person.
5. **The scenes.** One line per scene: its title and `status` from `project`,
   its length from `scene` on that id (`seconds`, and the shots' windows):
   "1. Kitchen (8s) -- Sam finds the tin." Say which are rendered.
6. **Deliverables.** The shapes and lengths they get. Any cut can be copied
   into 9:16, 16:9, 1:1 or 4:5 with `reformat`, free, as a new item.
7. **What we need from you.** Photos of the people, product and place the
   scenes are held to, approvals, and when the first cut is due.
8. **Next step.** One sentence: what the client says yes to, and by when.

Show the draft; take the person's edits; rewrite until they say it is right.
If they want the shape kept for the next client, `save_recipe` with a `name`
and the page as its `body` keeps it as their own text, versioned.

## Claims (the rule)

Every claim, testimonial, customer quote, number, award and "as seen in" on
the page comes from the person. Ask for it; where they have none, write a
bracket -- "[client to supply: results from the last campaign]" -- never a
plausible sentence. `what_works` numbers belong to the person's own posted
videos: say so, and never carry them over to the client's audience.

If the page names cost, say credits only, taken from `quote` on the scene;
never a currency or a plan price. Most treatments leave the fee to the
person: ask before writing any figure.

## A worked skeleton (replace everything in it)

```
THE TIN -- a 24-second short for [client]
A man finds a biscuit tin that will not stay shut.
Why it works: your brief asked for ...
The look: soft daylight from one window, true-to-life colour, 35mm, ...
Scenes: 1. Kitchen (8s) ... 2. Hallway (10s) ... 3. Doorstep (6s) ...
Deliverables: one 24s cut in 9:16 and 16:9; a 6s cut-down in 1:1.
We need: a product shot of the tin, two photos of your presenter, ...
Next step: a yes on the idea by Friday; first cut ten days after.
```

## Do not

- Never invent a quote, a statistic, an award or a client's result.
- Never paste a `share_link` into the page; it is the person's to send.
- Never say a render is done unless `scene` shows the clip.
