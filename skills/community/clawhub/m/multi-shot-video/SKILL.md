---
name: multi-shot-video
description: >
  Tell a short story across several cuts in one video call, not one continuous take. Use when the
  user says "a reel that cuts between shots", "a few beats in one clip", "wide then close-up then
  end on…", "storyboard this", "multi-shot sequence", "a mini montage of one subject", or wants
  several angles or moments of the same subject stitched without an editor. One API call, multiple
  shots. For a single continuous shot, use cinematic-video or animate-image.
---

# Multi-shot video

Produce a multi-shot reel (a single subject's story told across several cuts) in **one** video call, instead of one continuous take or hand-stitching clips in an editor. The lever is the model's own shot template written into the prompt, with the cuts, the per-shot timing, and the cross-cut continuity all carried by the text (and, on some models, an anchor frame).

## Inputs to collect

- **The story beats.** Two to six shots: what each shot shows, in order (wide establishing, close on hands, end on the finished thing).
- **Total length** and roughly how many cuts. This sets the per-shot time budget.
- **The subject's identifying details** (wardrobe, color, key features) that must stay the same across every cut.
- Optional: an **anchor frame** (one or two stills) to lock the opening and/or closing look exactly. Ask only if brand assets or an exact character must survive frame-for-frame.
- Optional: aspect/orientation and whether you want the native ambient audio bed.

## Models

- **Default storyboard reel: Alibaba HappyHorse 1.1** (`alibaba:happyhorse@1.1`). Natural-language storyboard cues (`Begin with… / Cut to… / Shift to… / End on…`), up to 15 seconds, native audio crossing the cuts. Best when the brief reads like a script.
- **Per-shot timing control: Kling 3.0 Turbo** (`klingai:kling-video@3.0-turbo`). Inline `shot N, seconds, description;` template, up to **6 shots**, per-shot seconds you budget yourself. Optional first-frame anchor via `inputs.frameImages`.
- **Anchor-frame multi-clip: PixVerse V6** (AIR `pixverse:1@8`, slug `pixverse-v6`). One or two anchor frames pin the bracketing look, `settings.multiClip: true` plus a beat prompt invents the cuts between them. Best when you have stills that must match exactly at the open/close.
- Confirm each is `live` and inspect its schema via `runware-models` + `runware-run` before calling. Do not hardcode a stale choice. All three are `videoInference` with `io:text-to-video` and `io:image-to-video`.

## Workflow

1. Resolve the model schema (`runware-run`) and confirm the prompt cap, the duration range, and whether the model takes an anchor frame (`inputs.frameImages`) or a multi-clip flag (`settings.multiClip`).
2. Budget the time: pick the total `duration`, then assign seconds per shot. On Kling Turbo the **per-shot seconds must sum to `duration` exactly** or the request is rejected.
3. If using anchors, upload the still(s) into `inputs.frameImages` and pin each with its position (`frame: "first"` / `frame: "last"`).
4. Write the prompt in the model's shot template (see Technique) with a continuity clause naming what must persist.
5. Run `videoInference` **asynchronously**, since multi-shot reels are minutes-long jobs. Poll `getResponse` until terminal. Do not block a sync call on it.
6. Read `videoURL`, then check the cuts landed where you named them and the subject reads as one continuous identity across them. Retry drifting shots with a tighter continuity clause or an anchor.

## Technique

- **The template turns one take into a reel.** Without the shot grammar, every one of these models renders a single continuous take from the same prompt. The cues are the switch. Plain description in, one shot out. Template in, cuts out.
- **Two template dialects, same idea.** HappyHorse and PixVerse read **directorial cues** (`Begin with… / Cut to… / Shift to… / End on…` or `Start with…`). Kling Turbo reads a **numbered shot list** with explicit seconds: `shot 1, 3, …; shot 2, 2, …;`. Match the dialect to the model.
- **Establish the subject once, at the top.** A single opening line ("an elderly Swiss watchmaker at his bench") gives the model one identity to hold. Repeating the full description inside every beat reads noisier and helps less, except on Kling Turbo where each shot is read independently and the identifying details belong in **every** shot's text.
- **Lead each beat with its shot-direction phrase.** "Cut to a slow tracking shot orbiting…", "End on a wide pull-back…". The model uses the first words of a beat to decide framing. Cinematic vocabulary (wide, medium, close-up, push-in, pull-back, orbit, low-angle, over-the-shoulder) reads as a real camera instruction, not scene description.
- **Close with a preservation clause.** The template carries no hidden continuity between shots. End the prompt with an explicit hold: "Preserve his clay-stained denim apron, short dark hair, and the warm sunlit studio across every shot." Without it, wardrobe color, accessories, and skin details drift by shot 4.
- **Anchor frames lock the truth at frame zero (and last).** When an exact character, brand asset, or specific environment must survive, pass it as an anchor rather than trusting the prose. PixVerse takes up to two (`first` and `last`) and brackets the reel between them. Kling Turbo takes one, pinned to the first frame.
- **One continuous subject, not a montage.** Cuts only render cleanly when the model recognizes a single thread to carry. A reel that jumps between unrelated subjects gives it nothing to hold, so skip the multi-shot path for those.

**Shot-list template.** Fill one row per shot before writing the prompt. On Kling Turbo the seconds column must sum to `duration` exactly. On HappyHorse and PixVerse leave seconds blank and let the model pace the cuts.

```
Subject (one line, holds across every shot): ___
Total duration: ___ s    Shot count: ___

Shot | Seconds | Shot-direction phrase + description
  1  |  ___    | ___
  2  |  ___    | ___
  3  |  ___    | ___
  ...
Sum of seconds = duration (Kling Turbo only): ___ = ___

Preservation clause (wardrobe, color, key details to hold): ___
```

Load `references/examples.md` for worked recipes in each dialect.

## Parameters that matter

- `positivePrompt` carries the shot list. Caps differ: HappyHorse **2500** chars, Kling Turbo **3 to 3072** (drops to 2500 with an anchor, 512 per shot), PixVerse **2048**. Confirm against the live schema.
- `duration` is integer seconds. HappyHorse and Kling Turbo **3 to 15** (default 5), PixVerse **1 to 15** (default 5). Match length to shot count: 2 beats want 5 to 7s, 3 want 8 to 10, 4 to 5 want 10 to 14, 6 wants the full 15.
- **Per-shot seconds (Kling Turbo only)** must sum to `duration` exactly. Plan the budget before writing the shots.
- `inputs.frameImages` holds anchor stills. Kling Turbo takes one, first-frame only. PixVerse takes up to two, each pinned `frame: "first"` / `"last"`. Presence switches to image-to-video and usually forbids `width`/`height` (aspect comes from the anchor).
- `settings.multiClip: true` (PixVerse) flips multi-shot mode on. Off by default, and a caption-style prompt with it on still yields a single take.
- `settings.audio` (PixVerse) and `settings.thinking` (PixVerse) tune the synced ambient bed and shot-planning depth. HappyHorse and Kling Turbo generate native audio that crosses the cuts as one bed.
- `resolution` / `width`+`height` are mode-dependent. Anchor modes use `resolution` tiers, text modes use an allowed dimension list. Mirror the schema's field names exactly, never guess.

## Quality bar

- The cuts land at the beats you named, and the count matches the brief (no single-take output from a multi-shot request).
- On Kling Turbo, per-shot seconds sum to `duration` and the request validated (no math error).
- The subject reads as the **same** person/object across every cut, with wardrobe, color, and key details held. Retry drift with a stronger preservation clause or an anchor.
- Where anchors were used, the opening (and closing) frame matches the supplied still rather than being redrawn.
- The reel was run async and polled, not blocked on a sync call.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `cinematic-video` (a single directed take), `animate-image` (bring one still to life without cuts).
