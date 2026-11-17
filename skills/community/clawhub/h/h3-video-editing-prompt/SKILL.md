---
name: h3-video-editing-prompt
description: Write or revise MiniMax H3 Ref2VA prompts for editing a source video from reference images or audio, especially masked or false-colour person replacement, face replacement, costume or object replacement, cross-shot identity persistence, overlay cleanup, and lip-sync preservation. Use when a request provides a source video and asks to change marked visible content while retaining its performance or timing.
metadata:
  trigger-words: [H3 video editing, Ref2VA editing, masked person replacement, inverted overlay, false-colour mask, cross-shot replacement, face replacement, lip sync, 视频人物替换, 蒙版换人, 反相遮罩, 伪彩遮罩, 跨镜头替换, 换脸, 对口型, 口型同步]
---

# MiniMax H3 Video-Editing Prompts

Write the target result, not a post-production command. In `detailed_description`, prefer `carries the appearance of`, `is rebuilt as`, or `continues from`; do not tell H3 to “swap”, “key”, or “remove” pixels.

This skill writes prompts. It must not imply that wording alone can guarantee a spatial mask, an untouched time range, or frame-accurate lip sync.

## Workflow

1. Inspect the actual assets before writing:
   - source duration, fps, resolution, frame count, and shot cuts;
   - whether the source video has audio or a separate audio asset is supplied;
   - whether the generation runtime actually receives the intended synchronized audio;
   - mask coverage, opacity, colour transform, first active frame, shot-by-shot presence, and whether internal structure and the mouth remain readable;
   - reference appearance, occluders, held props, off-frame body parts, and other people.
2. Assign ownership:
   - appearance comes from the reference material;
   - visible pose, motion, gaze, expression, and mouth trajectory come from source frames when readable;
   - audio validates vocal timing only when the synchronized final signal reaches the generator;
   - lighting, perspective, contact, and occlusion come from the source scene.
3. Select the lip-sync branch below.
4. Write the six Ref2VA fields and run the quality gate.

For uncommon target types, read [references/universal-replacement-template.md](references/universal-replacement-template.md). For copy-ready examples and pipeline failure handling, read [references/editing-recipes.md](references/editing-recipes.md).

## Output contract

Unless the user requests analysis or another format:

- Return only one English `text` block.
- Preserve dialogue, lyrics, and visible text in their original language.
- Use these fields, in this order and with these exact names:

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

- A video-editing summary begins, after the task prefix, with `The target video is an edited version of <Video 1>.`
- Target about 7000 characters and never exceed 10000 characters. Count characters before delivery.
- Save a copy to the workspace `outputs/` folder only when the current environment provides a workspace and the user wants a file.

## Ref2VA labels

- `<Video N>` identifies the source video or its whole-run structure, not the person inside it.
- `<Subject N>` identifies reusable visible content such as the source performer or reference identity.
- A reference image used only for appearance is cited inside `<Subject N>`; do not add a standalone `<Picture N>` line unless the picture is a keyframe or composition anchor.
- Add `<Audio N>` only when an audio signal is actually available to the target workflow.
- Use only official labels. Never output `<Theme N>`, `<Topic N>`, `Topic definition`, `Task`, or `Retain analysis`.

Task types are `video editing`, `reference generation`, `audio reuse`, `audio reference`, `keyframe completion`, and `video continuation`. Combine only the relationships that truly occur.

## Masked replacement ownership

The mask identifies the target; it does not make the rest of the frame immutable.

- Everything visually inside the replacement mask belongs to the rebuilt appearance. Do not list the source hair, hat, clothing, or accessories inside that mask as retained.
- Source elements inside the mask that must disappear are named once as `not carried over`.
- Motion, pose, timing, contact, and depth order remain owned by `<Video 1>` when they are visible or can be inferred from exposed joints.
- Elements outside the mask are retained explicitly.
- Other figures keep their own appearance, position, motion, timing, and depth order.
- A prompt cannot enforce a time window. If the mask begins partway through the clip, keep untouched frames outside H3, generate only the active segment, and splice it back.

Opaque and translucent masks are different:

- **Translucent:** visible facial and body structure remains usable. Preserve the observed performance from the source frames.
- **Opaque:** the covered geometry is gone. Use only exposed anchors; do not claim to recover erased expressions or lip shapes from the video.

### False-colour or inverted full-subject overlays

A negative, cyan/blue, green, or other false-colour overlay may corrupt the complete appearance while leaving the face, body contours, clothing folds, mouth shapes, and motion readable. Treat this as **appearance-corrupted but geometry-readable**, not as an opaque blank:

- Source frames still own silhouette, pose, movement, expression, gaze, mouth trajectory, contact, crop, and occlusion.
- The overlay owns no target colour, skin, hair, clothing, material, or texture. All marked appearance comes from the reference subject.
- The result states once that no green, cyan, blue, negative colour, transparency, fringe, hard patch, double outline, source-feature leakage, ghosting, or flicker remains.
- The target uses the source scene's lighting and perspective, but never the overlay's false colour or the reference picture's studio lighting.

Define `<Subject 1>` as the **same persistent marked character**, not as an anonymous region:

```text
<Subject 1> is the same marked target character wherever any part of that character appears in <Video 1>, including full, partial, cropped, edge-of-frame, foreground, and post-cut appearances.
```

For every measured cut, write a new `[Shot N] At MM:SS.mmm` paragraph and reassert that every visible portion of `<Subject 1>` carries the same `<Subject 2>` identity. A cut changes composition and visible area; it never resets the replacement assignment.

- When the target is partly outside the frame, keep the original crop; do not pull missing body parts into view.
- When only a small foreground fragment remains after a cut, name its side, scale, crop, and depth order so it is not mistaken for unmarked scenery.
- When the target is absent from a shot, state that it is absent; do not invent it.
- When the target reappears without a visible overlay, continue replacement only if continuity, position, or the user's instruction identifies it as the same target.

Prompt wording cannot guarantee cross-cut identity. If the output still restores the source character, leaks false colour, or flickers at a cut, generate each target-bearing shot separately and concatenate at the original hard cuts.

## Reference-condition video + picture + separate audio

Use this as the default input contract when the user supplies three assets:

- `<Video 1>`: the reference-condition video. Its coloured overlay identifies the only target region; its visible frames provide motion, pose, expression, gaze, mouth motion, timing, camera, lighting, contact, and occlusion.
- `<Subject 1>`: the masked carrier abstracted from `<Video 1>`, used for performance and geometry rather than retained appearance.
- `<Subject 2>`: the target person or object from `<Picture 1>`, used for the complete appearance inside the overlay.
- `<Audio 1>`: the separately supplied audio, only when its actual role and alignment have been verified.

Do not assume every condition video matches the inspected sample. Measure each clip. For a full-run translucent overlay, no temporal segmentation is needed and all readable motion and facial evidence remain usable.

### Classify the picture target

- **Person or face-capable character:** transfer the complete appearance covered by the overlay. Reproduce the carrier's observable performance moment by moment: brow and eyelid motion, eye tension, gaze and blinks, mouth-corner tension, head motion, posture, gestures, weight shifts, speed, pauses, and secondary motion. Preserve the emotional performance through these visible changes; do not replace it with one static emotion adjective.
- **Object:** transfer the object's shape, colour, pattern, material, and details. Its position, occupied space, orientation, scale change, velocity, motion path, contact, and occlusion follow the masked carrier. Do not add expression, emotion, gaze, speech, or lip-sync clauses to an ordinary object.

If a person-shaped mask is filled with an object of very different topology, preserve the carrier's centre, scale, orientation, path, and timing rather than claiming that the object reproduces human joints or facial motion.

### Classify the separate audio

1. Verify duration, start offset, time base, silence padding, and intended speaker against `<Video 1>`.
2. If the audio is the exact signal that will remain in the final video, use `<Audio 1>`, `audio reuse`, and `fully_copy` even when it is a separate file.
3. If the audio supplies only timbre, genre, mood, or delivery style, use `audio reference`; it is not an absolute lip-sync timeline.
4. Apply lip sync only when the audible voice belongs to the masked person or face-capable target.
5. If the audio is synchronized to the visible source mouth performance, use source frames and audio jointly as in branch 1 below.
6. If the audio contains new wording or a different timeline, do not also demand the source's exact lip shapes. Keep the source's eye, brow, head, body, gesture, and overall performance timing, while the supplied final audio drives the new lips and jaw. Precise results require a dedicated audio-driven lip-sync or face-reenactment stage after H3.

## Lip-sync decision table

### 1. Source mouth readable and synchronized final audio reaches H3

Use source frames and the synchronized final audio jointly. The frames own the visible articulation; the audio checks the opening, closure, sustained sound, pause, breath, and emphasis timing. The audio may be embedded in the source video or supplied separately, but it must share the same timeline. Do not make audio replace the source mouth trajectory.

Compact wording:

```text
Her visible articulation follows <Video 1>: the upper- and lower-lip contours, mouth corners, jaw opening, visible teeth and tongue, full closures, pauses, and coupled head motion keep the source frames' timing. <Audio 1> is reused unchanged and validates the same openings, closures, sustained sounds, pauses, breaths, and emphasis. No new dialogue is added.
```

Mark `<Audio 1>` as `fully_copy` only when it is actually reused. Do not invent `<d>` content. Known dialogue may be preserved for semantics, but it must not define a hand-written mouth timeline.

### 2. Source mouth readable, but H3 receives frames only

Preserve the visible lip shapes and timing from `<Video 1>`, but do not claim audio-driven synchronization and do not define `<Audio 1>` in the H3 prompt. Reattach the untouched original track after generation. If precise sync is required, use a dedicated audio-driven lip-sync or face-reenactment stage after H3.

```text
Her upper- and lower-lip contours, mouth corners, jaw opening, visible teeth and tongue, full closures, pauses, and coupled head motion keep the exact visible sequence and timing from <Video 1>. No audio-based synchronization is claimed in this generation pass.
```

### 3. Mouth is opaque or erased, but synchronized audio reaches H3

The audio can provide approximate articulation timing, but the source video cannot supply erased mouth geometry. Say so in analysis; do not promise frame accuracy. For exact sync, plan a dedicated downstream lip-sync pass using the original audio.

### 4. No usable audio

- If the mouth remains readable, preserve only its visible shapes and timing.
- If the mouth is also erased, state that no audio anchor or visible mouth trajectory exists. Use a neutral closed mouth unless the user supplies reliable dialogue plus alignment data.
- Never estimate phoneme, syllable, word, or character timings by hand.

## When a rendered result is already out of sync

Stop rewriting the prompt as if phrasing alone will fix it. Obtain the rendered clip, keep the original audio, and classify the error:

- **Fixed offset:** mouth is consistently early or late. Measure audiovisual lag before shifting anything; verify that demuxing, decoding, resampling, and remuxing did not introduce the offset.
- **Local wrong shapes:** timing is broadly right but individual closures or vowels are wrong. Use audio-driven lip sync or face reenactment.
- **Cumulative drift:** error grows over time. Check fps, frame count, duration, sample rate, time base, and any speed conversion; correct the timeline before lip-sync processing.

Do not hand-write a phoneme schedule and do not claim that another prompt revision will produce exact sync.

## Person-performance wording

When the face is readable, cover only observable ownership:

- expression: brow and eyelid positions, eye and mouth tension;
- gaze: target, drift, return, and blink rhythm;
- head/body: turns, tilts, posture, limb paths, weight shifts, speed, and pauses;
- secondary motion: hair, clothing, and accessories following the body;
- mouth: use exactly one lip-sync branch above.

Avoid emotion labels and inferred intent. Do not describe a person as singing, speaking, livestreaming, rehearsing, or thinking unless the source or user establishes it. Do not add new action, dialogue, or events.

## ComfyUI_Qwen_H3_Prompt adaptation

This node receives frames without their audio track. Therefore:

- return plain text rather than a Markdown fence;
- omit `audio reuse`, `<Audio 1>`, and `fully_copy` from the H3 prompt;
- use lip-sync branch 2 or 4;
- set `overall_soundscape: N/A` and `non_diegetic_music: N/A` unless the user explicitly requests new audio and a later stage supports it;
- never claim that this frames-only pass will align lips to the original sound;
- preserve the exact requested duration and keep shot timestamps inside it.

## Quality gate

- [ ] The picture target was classified as a person/face-capable character or an ordinary object; object prompts contain no emotion or lip-sync clauses.
- [ ] Embedded or separate audio presence, role, duration, offset, and intended speaker were verified rather than assumed.
- [ ] `audio reuse` is used for the final copied signal; `audio reference` is used only for characteristics such as timbre or style.
- [ ] The generator's audio input capability was verified separately from audio-file presence.
- [ ] New wording or a different audio timeline is not combined with a demand for the source's exact lip shapes.
- [ ] Exactly one lip-sync branch is used; mouth ownership is not contradictory.
- [ ] No hand-written word, syllable, phoneme, or character timing appears.
- [ ] Six official fields appear in the correct order; only official reference labels are used.
- [ ] Masked appearance is rebuilt; masked source appearance is not also retained.
- [ ] False-colour or inverted overlays are classified as geometry-readable when internal structure remains visible; their colours and textures are never retained.
- [ ] `<Subject 1>` is a persistent target across shots rather than an anonymous region.
- [ ] Every measured cut has its own `[Shot N]` paragraph, and partial/cropped post-cut appearances explicitly retain `<Subject 2>`.
- [ ] Frame-edge crops remain crops; off-frame body parts are not pulled into view.
- [ ] Lighting, geometry, contact, occlusion, other people, and off-frame parts remain source-owned.
- [ ] Any inactive mask interval is enforced by segmentation, not prompt wording.
- [ ] The prompt does not promise exact lip sync when H3 lacks audio or visible mouth evidence.
- [ ] Character count was measured: target about 7000, hard maximum 10000.
