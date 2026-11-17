# H3 prompt preparation

Read this before authoring or troubleshooting H3 Standard/Turbo prompts. The full customer guide is [H3 prompt guide](https://phosor.ai/docs/minimax-h3-prompt-guide); model IDs and current limits are in [api.md](api.md).

## Inputs and shot planning

- Preserve the user's model, cast, actions, words and camera intent. Keep the number of actions and words plausible for the clip duration.
- For text-to-video, describe the scene. For image-to-video, animate from the opening image; an ending image anchors the ending state. For references, state which asset supplies identity, outfit, prop, location, motion or style.
- API prompts use `<Picture N>`, `<Video N>`, `<Audio N>` with one-based indices in their respective arrays. Interface `@ImageN` labels are not a portable API syntax. Do not invent missing reference files.
- Bind a voice to a named character explicitly. When reference-video soundtracks are enabled, their audio slots precede separately supplied audio. Images and audio at the same index are not implicitly paired.
- Distinguish camera travel, body facing, gaze and subject travel. Specify action order and prop ownership. One continuous take should have a compatible camera path; a cut must fit the clip duration.

## Dialogue and silence

Supply the actual words and an explicit speaker, preferably one utterance per line:

```text
Ada says: "Stay here."
Ben says: "I will."
```

For Chinese scripts, `Dialogue | woman (Mandarin): "Let us try it first."` makes the speaker, language and line explicit. State who speaks first, and whether the speaker is visible, off-screen or a voiceover. Keep voice qualities and actions outside the quoted words. Preserve wording, punctuation, order and repeated lines.

A sign that says "EXIT", a person named "Ada", a "watercolor" style and “never look at or speak to the camera” are not supplied spoken words. Do not add dialogue to satisfy a missing-container error. A request to introduce a product without a script does not authorize inventing exact words; obtain or draft words within the user's creative scope before submitting if audible wording matters.

“No dialogue or voiceover” permits requested nonverbal sounds, ambience and instrumental music. “Complete silence” removes all sound. An audio voice reference is an identity reference, not an implicit transcript.

## Enhancement and submission

Ordinary H3 prompts are compiled automatically. Users do not need to hand-author the model's three/six sections or `<d>` containers. For review, POST `/api/v1/inference/prompt/enhance` with authentication, prompt, model, duration and matching reference context. It returns text without creating a video job. Check `enhanced`; HTTP 200 alone is insufficient.

Submit the original prompt with the same model, duration and reference context. Every H3 video generation submission performs mandatory prompt processing, including structured input; previews and client-provided receipts cannot bypass it. There is no customer opt-out switch. Processing failure stops generation and follows the refund path for deducted credits. Do not claim a preview is a completed or visually verified video. Save the request ID; check history after a submission timeout before making a duplicate paid request.

For failures, retain the original prompt, model, reference mapping, settings, preview result and request ID. Do not log API keys. Request status/result and download successful outputs rather than relying on an expiring result URL as permanent storage.

Use `--avoid-model-limitations` only when the user allows camera/framing adaptation; omitted means faithful mode. It does not disable mandatory prompt processing. Do not pass negative prompts or model sampling controls to H3.
