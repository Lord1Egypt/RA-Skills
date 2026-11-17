---
name: ideas-and-projects
description: Turns a brief into a few story ideas the person chooses between in the chat, and keeps the work in a Phantra project. Use when someone describes a video, ad, short or scene they want made, asks what they are working on, wants to open or start a project, or wants to decide between ideas. NOT for writing the scene (write-scene), prices or rendering (price-and-render, credits-and-limits), or choosing a visual look (look-matching).
---

# Ideas and projects

Ideas are worked out here, in the conversation. There is no idea board to
read or fill: nothing is saved until the person has chosen an idea and its
scene is written (write-scene). A **project** is where a piece of work lives
in the studio: a brief, a look, its scenes, the references they used and its
renders.

Nothing on this skill's path spends credits.

## Before you start

Call `projects` first when the person refers to work they already have ("the
bottle ad", "what am I working on"). `project` with a project's id opens it:
read its brief, its look and its scenes before proposing anything, so a new
idea fits what is already there.

If a call errors with "no workspace yet" or a sign-in message, the person has
not created their workspace yet: ask them to sign in once at
https://phantra.ai (the workspace is created on the first sign-in) and
reconnect.

## Turning a brief into ideas

1. Read the brief. Ask at most **three** short questions, and only when the
   answer changes the idea: who it is for, how long (seconds), and what must
   be in frame (a product, a place, a person they have photos of). Offer
   choices as short chips, not open questions. Do not ask about budget, tools
   or style here.
2. Propose **two to four** ideas in the chat, each as: a working title, one
   sentence of what we see, one sentence of why it holds attention. Keep them
   different from each other.
3. Wait for the person to choose. Do not save anything for ideas they did
   not choose.
4. Hand over to write-scene with the chosen idea. The scene it saves is the
   first thing that exists in the studio.

## Projects

- `projects` lists the person's projects, most recently touched first.
- `project` opens one by id: brief, look, what it has learned, its scenes,
  the elements those scenes used, its renders and the latest turns of
  its chat. A project made in the studio opens the same way.
- `project_chat` pages back through a project's chat history when the person
  asks what was said before.
- `create_project` starts one with a `title` and, when the person has given
  them, a `brief` (who it is for, what must be in it, what must never be) and
  a `look`. Offer it when the work is more than one scene, or when they ask
  to keep things together. A scene does not need a project.
- A scene is filed in a project by passing the project's id to `write_scene`.
  A still drawn with `generate_image` is filed the same way, by `project_id`
  -- quoted first, and drawn only on the person's yes (price-and-render).

## What to say and not say

- Summaries, not dumps: report the few projects or scenes that fit what was
  asked, not everything a call returned.
- Never invent an id. Every project or scene id you use comes from a
  `projects`, `project`, `create_project` or `write_scene` reply in this
  conversation.
- Never say a scene is rendering, drawn or scheduled unless `approve` started
  that job in this conversation, after `quote` showed its price in credits
  and the person said yes (price-and-render). `scene` says where a scene
  really stands.
