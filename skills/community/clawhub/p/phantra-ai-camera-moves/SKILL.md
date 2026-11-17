---
name: camera-moves
description: A vocabulary of camera moves and framings for Phantra scene prompts (push-in, pull-back, orbit, handheld, locked-off, rack focus, whip pan, crane, top-down, POV; close, medium, wide), with when each works in a 2-10 second shot and the rule of one move per shot. Use when someone asks how to shoot a beat, names a move, or wants a shot calmer or more alive. NOT for a camera move on an existing still (effects), the whole scene (write-scene) or the light and palette of a look (look-matching).
---

# Camera moves

Each timed window in a scene is rendered as its own clip (the model is handed
that window's text, with the rest of the scene only as continuity to keep
identical), so a window is ONE camera setup: one move, one framing, one
action, 2 to 10 seconds. The move starts and finishes inside the window and is
written in plain words -- what it does, how fast, what it ends on. Never name
a film, a director or a camera brand. Nothing here spends.

## The moves

| move | what it does | fits | write it like |
|---|---|---|---|
| push-in | closes on a face or object; a decision, a tightening | 3-6s | "slow push-in from medium to close on Sam's face as he reads it" |
| pull-back | reveals where we are; isolation, scale | 4-8s | "steady pull-back from the cup to the whole empty table" |
| orbit | shows a form in the round; a product, a figure | 4-8s | "a half-orbit left to right at chest height around the bottle" |
| handheld | immediacy, unease; a walk | 2-10s | "handheld, small breathing movement, follows Sam down the hall" |
| locked-off | stillness; lets the action and the comedy play | 2-10s | "locked-off wide; nothing moves but Sam" |
| rack focus | moves attention between two depths | 2-4s | "rack focus from the keys in front to the door behind" |
| whip pan | a jolt between two subjects | 2-3s | "whip pan right from Sam to the window; settle on it" |
| crane / rise | scale; an opening or an ending | 4-8s | "the camera rises from eye height to above the roofline" |
| top-down | hands at work, pattern, a product on a surface | 3-8s | "top-down, locked, as two hands lay the parts out in a row" |
| POV | through a character's eyes | 2-6s | "POV from Sam's eyes, handheld, looking down at the open tin" |

## Framings and heights

- **Close**: one detail -- a face, hands, a label. Holds a likeness best.
- **Medium**: waist up -- a person and what they hold or do.
- **Wide**: the whole space -- where we are; establish, then cut closer.
- **Eye height** is neutral; **chest height** sits a little lower and grounds
  the subject; **low** gives scale or menace -- a product looming, a figure in
  a doorway.

## Writing a move into a beat

`(start-end s) [framing], [height], [move]; [subject] [one action]; [what the
move ends on].` One move and one action per window; a second move is a second
window. Pair motion with stillness (a push-in, then a locked-off cut). The
lens and the depth of field belong in the scene's style block, not in every
beat, unless one shot changes them ("a longer lens here, shallow"). Match the
move to the length: 2-3s takes a whip pan, a rack focus or a close cut-in;
4-6s a push, a pull or a half-orbit; 7-10s a rise, a full orbit or a walk.

Example beats (the rest of the scene follows write-scene's shape):

```
(0-3s) Close, chest height, locked-off; Sam's thumb lifts the tin's lid a
finger's width and stops.
(3-8s) Medium, eye height, slow push-in; Sam reads the note inside, his face
unmoving; the push ends on his eyes.
(8-10s) Wide, low, whip pan from Sam to the front door; it is open. End.
```

## When the motion matters

Big moves (an orbit, a rise, a walk) show more of the frame and ask more of
the model than a locked-off close; a push-in on a face keeps a likeness best.
`recommend_model` reads the JOB off `what`, not the move -- a face or hands in
it, sound, a long take, a cheap test or a final deliverable -- and with
`seconds` ranks the models with a reason and its credits each ("a handheld
walking shot with a face in it", "a final product spot, realistic, with
sound"); `video_models` lists their lengths and frames. Say the reason; the
person picks the model, and that pick goes on `quote` as `model`, so the price
they see is for that model, then on `approve` with the quote's tokens once
they have seen the price and said yes in this chat (price-and-render).

## Then

Fold the beats into the full scene (opening line, style, beats, sound, avoid)
and save it with `write_scene` (write-scene). Pricing and the render --
`quote`, the person's yes in this chat, `approve` -- are price-and-render.

## Do not

- Never two moves in one window, and never a move with no end point.
- Never a move the length cannot hold (a full orbit in 2 seconds).
- Never "cinematic", "epic" or a film's name in place of a move.
- Never put a cut or a change of place inside a window; those go between.
