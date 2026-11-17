---
name: hooks-and-first-seconds
description: Writes the first shot of a Phantra scene so it holds attention (an arresting image, a turn or a reveal in the first seconds) and puts it into the scene's first timed shot, reading `what_works` and `score_caption` as evidence rather than verdicts. Use when someone asks for a hook, says the opening is slow, wants the first seconds rewritten, or asks for a caption. NOT for the whole scene's shape (write-scene), the cover image (thumbnails) or the platform's shape and length (platform-delivery).
---

# Hooks and the first seconds

A short is decided in its first two or three seconds. The first shot of a
scene is rendered as its own clip, so the hook is written as `(0-Ns)`, the
first timed window, and nothing comes before it. Writing costs nothing.

## What holds

1. **Open on the arresting image, mid-action.** The first frame is already
   the situation: hands on the tin, the door already open. No establishing
   shot, no walk into frame, no title.
2. **A turn or a reveal inside the window.** By the end of the shot the frame
   is not what it seemed, or a second thing has entered. The question it
   leaves the viewer with is why they stay for shot 2.
3. **Serious reactions.** People react as people do: a freeze, a glance, a
   step back. Never a cartoon face, hands thrown up, a look to camera.
4. **One shot, one setup.** 2 to 4 seconds, one camera position, one action
   that fits it. The cut to shot 2 is the first edit; land it on the turn.
5. **Sound is half the hook.** Name the first diegetic sound in the Sound
   line (the lid's scrape, a hinge) and nothing else; no music, no voice.
6. **End the scene abruptly.** The last shot stops on its strongest frame:
   no fade, no lingering, no resolution the viewer can predict.

Shapes that work: the reveal (the frame holds a thing that should not be
there); the interruption (an ordinary action stopped by something entering);
the wrong scale or the wrong place (an everyday object, an impossible
setting). Not: a title card, a logo, text on screen (the avoid list forbids
overlays), "wait for it", a slow push-in on nothing.

## Writing it into the scene

Follow write-scene's five parts. In the beats:

- The first window is short, `(0-3s)` or `(0-4s)`, and starts at 0.
- Image first, then the turn: "(0-3s) Close on Sam's hands lifting the lid of
  a dented biscuit tin; inside, a house key on a bed of crumbs. He stops."
- Name the reaction physically, never by its emotion ("he freezes", not "he
  is shocked").
- Shot 2 answers with a cut: "(3-8s) Hard cut to the hallway ..."; the later
  windows are reflowed so they still fill the total length.
- The look stays in the style block; the hook carries action only.

Save with `write_scene`. To change the opening of a saved scene, call
`write_scene` with its `scene_id`, the WHOLE prompt, and the same `refs`,
`seconds` and `roles` again (a rewrite keeps nothing it is not handed; with
no `refs` the scene becomes a draft with no photos). It replaces the text the
scene had and detaches any clips already on it, so show the new version and
get a yes first; to keep the original and its clips, `duplicate_scene` with
the new `prompt` instead. Then `quote`, the person's yes, and `approve` with
the quote's tokens (price-and-render).

## Evidence first: `what_works`

Before rewriting a hook for someone who has posted before, call `what_works`.
It reads their own studio: what they kept per model and camera preset, how
many tries a keeper takes, and what they posted with a scene behind it, with
its latest numbers. Use its `lines` as evidence for how THEY open (the
presets they kept, the posted scenes that did well), never as a rule, and
when `enough_data` is false say so and write from craft.

## The caption: `score_caption`

A caption rides beside the hook on the platform. Draft it with the person
from THEIR claims: never invent a number, a quote, a review or an award. Then
`score_caption` with the text: a score from 0 to 1 against the words, topics
and hooks of their OWN posted videos that beat their median, with the
evidence behind each movement. Read it as evidence, not a verdict: a low
score against a handful of posts is a hint, and a neutral score (fewer than
four posted videos with numbers) means no evidence, which it says. Show the
evidence lines, offer one revision, and let the person choose. Never loop on
`score_caption` until a caption reads high.

## A worked example

Person: "The opening of scene 403 is slow; make it grab."

1. `scene` 403: shot 1 is "(0-5s) Sam walks into the kitchen and looks
   around." Nothing happens in it.
2. `what_works`: `enough_data` true; the preset they kept most was
   handheld_rough, and `posted` names the scene with the best numbers;
   `scene` on that `scene_id` shows it opened on a reveal.
3. Rewrite shot 1 as "(0-3s) Close on Sam's hands lifting the lid of a dented
   biscuit tin; inside, a house key on a bed of crumbs. He stops." and reflow
   the windows to fill 10 s.
4. Show the whole scene; on a yes, `write_scene` scene_id=403 with it and the
   same `refs` and `seconds` as before.
5. Caption drafted from what they told you; `score_caption`; show the
   evidence lines and the one revision they suggest.

## Do not

- Never put text, a logo or a voice-over pitch in the first shot.
- Never invent numbers, quotes, reviews or results for the caption.
- Never say a hook "will perform"; say what the person's own evidence shows.
