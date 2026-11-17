---
name: sound-plan
description: Plans the sound of a Phantra scene: writes the "No background music. Only diegetic sound:" line and each shot's own sound, says which models render sound with the picture, and where music and voice go (a music bed through `assemble_clips`; a voice the person records). Use when someone asks what a scene will sound like, wants music or a voice-over, or asks why a clip is silent. NOT for the whole scene (write-scene), a full explainer (explainer) or sound added to a finished clip (effects).
---

# Sound plan

A scene's sound is written into the prompt as DIEGETIC sound: what you would
hear standing in that scene. Music, narration and captions are not in the
prompt. Nothing in this plugin generates a voice or a song. Ambience can be
added to a finished clip with an effect, quoted first like a render (effects).

## Where each sound comes from

| sound | where it is made |
|---|---|
| what the scene itself makes (steps, a kettle, rain) | the prompt's sound line, rendered with the picture by a model that does sound |
| music | a bed under the clips: the studio's editor, or `assemble_clips` with `music` = an audio `asset:<id>` |
| a voice, narration, a spoken line | recorded by the person and laid on in the studio's editor |
| ambience or sound effects on a finished clip | an effect, quoted in credits first (effects) |

`upload_link` takes pictures and clips, never audio: a music file goes in
through the studio's editor, and `library` with `kind` audio lists it as an
`asset:<id>`.

## The sound line

The scene ends, before the avoid list, with one line:

    No background music. Only diegetic sound: <two to five sounds, in the
    order they happen, each a thing on screen or just off it>.

Write sounds the picture explains: a footstep needs a foot, an engine a car.
Say the room -- "close and dead", "a tiled echo", "wind over the mic". Never
write a song, a score, a "cinematic swell" or a spoken line: the model either
ignores it or invents a voice.

## Per shot

The studio renders each timed window as its own clip. The closing sound line
reaches every shot as the scene's memory, which is right when the sounds run
through the whole scene. When the shots differ -- a kitchen, then a street --
give each window its own sentence opening "Sound:" after its action, **and
give every window one**: a "Sound:" sentence on only the last shot is read as
the scene's closing line, not as that shot's. The closing line then names
what runs under all of them.

```
(0-4s) Mara lifts the lid of the pot and leans back from the steam. Sound:
the lid's clink, the boil, the hood's hum.
(4-10s) Hard cut to the doorstep: she steps out, pot in both hands, into the
rain. Sound: rain on the step, the door behind her, a car passing. End
abruptly.
No background music. Only diegetic sound: the pot, the rain, her breath.
Avoid: ...
```

Save with `write_scene`. A change to a saved scene goes in with its `scene_id`
and the whole new prompt: show the new version and get a yes first.

## Which models render sound

`video_models` lists the models with the lengths, frames and credits each
takes. `recommend_model` with "with sound" in `what` ("a product clip with
sound") ranks the ones whose catalogue line says they render sound with the
picture, one reason each. A model not described that way is not promised to
have sound: plan for its sound to be laid on in the editor.

`quote` with `model` prices the scene on the one chosen and spends nothing:
`keyframes` (the stills to draw, `each` in credits), `clip` (one render per
timed shot, each with its credits and a `token`), `balance` and
`credits_needed`. Repeat the quote's own numbers -- `each` for a still, the
credits of each shot's render -- never a guess, and WAIT for a yes
in this chat; never say it for the person. Only then `approve` with the
`scene_id`, `what` ("keyframes" draws the stills, "clip" renders every shot
without one), the quote's `tokens` and the SAME `provider`, `model`, `frame`
and `duration`; poll `job` with `wait`, then `scene` shows the keyframe, the
clips and the scene's studio link. Tokens live one hour and work once; a
different renderer is a new quote and a new yes. Refused for
`insufficient_credits`? Stop, and say credits are added in the studio.

## Music and voice, after the render

1. Music: `assemble_clips` over the rendered `gen:<id>`s with `music` = the
   audio `asset:<id>` from `library`. The bed is trimmed to the picture and
   lowered under the clips' own sound. Free; poll `job` with `wait`. The
   result is a new `gen:<id>` and an editable cut in the studio's editor,
   where the person balances it. For one clip alone, the editor.
2. The voice: the person records it (a phone in a quiet room is enough) and
   lays it on in the editor. Write the words with them if asked, as a script
   they read, never as a line in the prompt.
3. Captions for those words: the editor's caption track, not the prompt.

## Do not

- Never put music, a score, lyrics or a spoken line in the prompt.
- Never say a voice or a track was generated here; nothing is.
- Never pass audio through `upload_link` or `add_element`.
- Never promise a clip has sound unless the model's catalogue line says so.
- Never `approve` without the price shown and a yes here, and never twice.
