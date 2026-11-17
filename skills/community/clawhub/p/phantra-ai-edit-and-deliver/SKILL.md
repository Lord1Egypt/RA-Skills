---
name: edit-and-deliver
description: Finishes a video with Phantra's free edits: finds clips in the library, trims one, joins several (a cut or a crossfade), reformats to a platform's shape and hands over a download link. Every result is a new item and nothing spends credits. Use when someone says trim it, cut these together, make a vertical version or send me the file. NOT for changing the picture itself (effects), the shape each platform wants (platform-delivery) or rendering (price-and-render).
---

# Edit and deliver

A rendered clip is in the person's library as `gen:<id>`; a clip or picture
they brought in is `asset:<id>`. Four tools finish a video from there, all on
the studio's own server, all free. Each makes a NEW item; no source is ever
changed or deleted. Nothing in this skill makes a clip that was never rendered.

| step | tool | what it costs |
|---|---|---|
| find clips and uploads | `library`, `search` (`scene` only says which shots have a clip) | nothing |
| keep a range of one clip | `trim_clip` | nothing |
| join clips, optional music | `assemble_clips` | nothing |
| a copy in another shape | `reformat` | nothing |
| a download link | `share_link` | nothing |

## Find the clips

1. `library` with `kind=video` (and `project_id` when the work is in a
   project): each row carries its id, length in seconds, frame and project.
   `scene` with a scene's id shows which of its shots have a clip, in shot
   order, as links, not ids: take the ids from `library` (`kind=video`, the
   scene's `project_id`) or `search`, which finds a render by its prompt's words.
2. Show the person the ids and the order you intend, and get a yes before
   joining. The order given to `assemble_clips` is the order in the video.

## Trim

`trim_clip` with `ref`, `start` and `end` (seconds, inside the clip's length)
and a `title`. The new clip keeps the source's own sound.

## Join

`assemble_clips` with `clips` (2 to 20 ids, in order; one may repeat),
`transition` cut (the default) or crossfade with `crossfade_s` (0.1 to 2
seconds, at most half the shortest clip), and a `title`. `music` is an
optional bed under the clips' own sound: an audio `asset:<id>` from `library`
with `kind=audio`, uploaded in the studio's editor (`upload_link` takes
pictures and clips, not audio). Clips of different shapes are refused unless
`letterbox` is true, which fits them inside the first clip's frame with black
bars; reformatting them to one shape first is usually better. `project_id`
files the result in a project. The result is a new `gen:<id>` and an editable
cut in the studio's editor.

## Reformat

`reformat` with `ref`, `aspect` (9:16, 16:9, 1:1 or 4:5) and `fit`: pad keeps
the whole picture with black where the shapes differ (the default); crop fills
the frame and keeps the middle, and is refused when the two shapes are too far
apart. One call per shape wanted. platform-delivery says which shape each
platform takes.

## Hand over

`share_link` with the `ref` and `hours` (default 24, at most 168). Give the
link to the person in the chat, never to a page or a form: anyone holding it
can download the file until it expires.

## Jobs

`trim_clip`, `assemble_clips` and `reformat` run in the background and return
a `job_id`. Poll `job` with `wait=15`; call again while it is still running.
Its result names the new `gen:<id>`. Jobs live in memory: if `job` says it is
gone, `library` (newest first) shows whether the result landed.

## A worked example

Person: "Join the three shots of scene 403 with a soft crossfade, make a
square version and send me the file."

1. `scene` 403 shows three shots, each with a clip. `library` kind=video with
   the scene's project gives their ids, newest first: gen:912, gen:911,
   gen:910. Put them back in shot order and show them; yes.
2. `assemble_clips` clips=[gen:910, gen:911, gen:912], transition=crossfade,
   crossfade_s=0.5, title="Scene 403 cut". `job` with wait=15 until done:
   gen:913.
3. `reformat` ref=gen:913, aspect=1:1, fit=pad, title="Scene 403 square".
   `job` until done: gen:914.
4. `share_link` ref=gen:914: "Here is the square cut, good for 24 hours:
   <url>. The three shots and the 9:16 cut are still in your library."

## Do not

- Never say a result is ready until `job` says done or `library` lists it.
- Never pass a URL as a ref; ids come from `library` or `search`, never `scene`.
- A refusal (a range outside the clip, shapes too far apart to crop, a music
  id that is not audio, more than twenty clips) comes back in words: repeat
  it and change the call. Never retry the identical call.
- Never promise a clip that has not been rendered; that is price-and-render.
