# Image-First Reference (music-with-comfyui)

> The image-with-comfyui skill has an analogous file. Open that one for the
> shared rules; this one only covers the audio-specific behavior.

## When the user sends an image

- If the user sends an image **and** then asks for music (style/genre, "make a
  song about …", "give it a theme", etc.), use the image to derive the
  **style tags** and, if appropriate, **lyrics**, then run `music`.
- The image is read by the **agent**, never sent to ComfyUI. AceStep 1.5's
  workflow has no image input anywhere — the only node that takes text is
  `TextEncodeAceStepAudio1.5` (tags + lyrics). The agent visual-reads the image,
  turns it into tags/lyrics, and hands **only that text** to the script.
- Consequence: this skill has **no `--tags-image` / image-upload flag**. Any
  doc that mentions "upload the reference image" is wrong.

## Deriving the tags

Let the image set the mood, and layer the user's explicit request on top:

1. **Read the image** (visual analysis) → note dominant mood, setting, colors,
   energy, season, time of day.
2. **Map to a sound:**
   - bright, playful, sunny → upbeat pop / indie / acoustic
   - dark, stormy, tense → cinematic / ambient / trap
   - calm, nature, soft → ambient / lo-fi / piano
   - energetic, sporty → EDM / rock / house
3. **Add the user's explicit constraints** (genre, tempo, language, vocals) to
   whatever the image implies. Never contradict the user if they specified one.

### Example

- Image: a rainy city street at night, neon reflections.
- User: "make a song about it, no vocals."
- → `--tags "moody neon synthwave, rain at night, slow-mid tempo, warm arpeggios, cinematic, no vocals"`

## Deriving lyrics (only when it fits)

- Prefer **instrumental** by default unless the user asks for words or the image
  clearly needs them.
- If writing lyrics, keep them short, on-theme, and in `--language` (default `en`).
- Do not invent specific real people's names/lyrics that could be inappropriate.

## The image is optional context, not a requirement

- A request with no image still works fine: just use `--tags` from the request.
- An image-only request is valid input: derive style and (if the user wants words)
  lyrics from it. The image is context for the prompt, not a mandatory "prompt text"
  requirement of the workflow itself.
