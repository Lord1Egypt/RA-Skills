# From a reference to a fresh short video

## Understand the reference

Obtain the actual file through the user's supplied path or the host's supported download/export
tool. A social page is not a direct media URL. If the recording is inaccessible, explain the
missing material and continue only with the text or assets actually available.

Run `media.mjs inspect` and inspect its contact sheet and sampled frames. Use the metadata for
duration, dimensions and audio presence. Sparse frames may miss fast cuts or brief text; inspect
additional relevant moments or watch the recording before describing those details.

Write a compact `reference-analysis.md` with:

- The opening: the first visible promise, surprise or question, and when it appears.
- The beat sequence: setup, evidence/reveal, escalation, payoff and ending where present.
- Shot and text rhythm: measured or observed changes, important readable words, and how captions
  interact with speech. Mark timings approximate when they are.
- Visual rules: framing, subject placement, motion, palette and recurring graphic treatment.
- Sound: observable speech/music/effects and their timing. Mark unexamined sound as unknown.
- Transferable mechanism: what to carry forward and why, separated from observed facts.

Do not claim view counts, retention or commercial performance from the video's appearance.

## Adapt the idea

Write a short brief naming the new audience, subject, message, desired action and delivery format.
Keep the reference's useful structure while making the script and visual choices specific to the
new subject. Replace factual claims with supported facts supplied by the user; invented product
benefits do not become true because they fit a template.

Develop the opening before expanding the rest. Make the first shot and first line earn attention
together. Each later beat should add information or change the viewer's expectation. Give the
ending a purpose: resolution, loop, question or requested action that fits the brief.

Save `script.md` with spoken lines, visible text and the approximate timing of each beat. Then
write a shot plan: purpose, duration, local asset or generation request, and the edit that joins it
to the next shot. Use current API limits when choosing generated shots; a long scene can combine
several intentionally chosen shots, with each additional generation counted in the spend.

## Make and assemble material

Prefer material already available when it serves the creative intent. For every generated shot,
create a separate request JSON and durable job file. Direct the shot with subject, setting,
action, framing, light and motion. Read the actual returned asset before using it in the edit.

The current video API is text-driven. A reference may guide your analysis without becoming a
conditioning input to generation. Character/face continuity, voice performances and lip sync need
capabilities that actually support them; do not promise those from an ordinary text-to-video call.

Use `edit.json` to arrange shots, timed captions, supplied narration and music. Captions should
follow the words or reveal they support, leave time to read, and stay away from faces and important
product details. The basic renderer supplies a clear containing canvas; the Agent can develop
additional local visuals when the production requires them and the user wants that scope.

## Review and deliver

Watch the exported video, not only the input shots. Check the opening at normal speed, text at the
target display size, shot joins, sound balance and the ending. Compare the result with the brief
and correct observed problems. Save revisions to new files so the user can compare them.

Deliver the MP4 and editable project, identify the materials used, and report actual dimensions
and duration from the render report. Keep generated-shot evidence separate from the final edited
composition. A successful render proves that the media was assembled; it does not prove that the
creative work will go viral.
