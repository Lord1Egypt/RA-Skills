# Video Scenarios

Supported scenarios:

- prompt-only video generation
- single-image animation
- first-frame to last-frame transition planning
- reference-driven continuity with one or more seed images
- Seedance multimodal reference with image + video
- Seedance multimodal reference with image + audio

## Visual Consistency Rule

Text-only runs are independent generations. They are not a reliable continuity mechanism for the same character or scene.

When the user asks for "the same subject", sequels, storyboard shots, or continuity across requests, route toward an image-based mode and reuse a prior asset as the source or reference image.

## Text To Video

### 1. Prompt-Only Concept Clip

Use when the user wants a fast first result without supplying any source media.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_video \
  --model-id ima-pro-fast \
  --extra-params '{"duration":5,"resolution":"480p"}' \
  --prompt "paper lanterns drifting over a calm night lake" \
  --output-json
```

## Image To Video

### 2. Animate One Key Visual

Use when the image itself should become the opening frame and the model should animate from it.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_video \
  --model-id ima-pro-fast \
  --input-images ./product-shot.jpg \
  --extra-params '{"duration":5,"resolution":"480p"}' \
  --prompt "slow turntable movement with soft studio highlights" \
  --output-json
```

## First Last Frame To Video

### 3. State Transition Between Two Fixed Frames

Use when the user has an explicit start frame and end frame and wants the model to synthesize the motion between them.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type first_last_frame_to_video \
  --model-id ima-pro-fast \
  --input-images ./state-a.png ./state-b.png \
  --extra-params '{"duration":5,"resolution":"480p"}' \
  --prompt "smooth transition between these two poses" \
  --output-json
```

This mode is about endpoint control. The two supplied images are treated as the start and end of the shot.

## Reference Image To Video

### 4. Character Or Style Continuity From One Reference Image

Use when the user wants to keep the same subject identity or art direction, but the reference should not be treated as the literal first frame.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type reference_image_to_video \
  --model-id ima-pro-fast \
  --reference-images ./character-sheet.png \
  --extra-params '{"duration":5,"resolution":"480p"}' \
  --prompt "the same character jogging through neon rain" \
  --output-json
```

### 5. Seedance Multimodal Reference With Image And Video

Use when `ima-pro` / `ima-pro-fast` should borrow both identity from an image and motion rhythm or camera language from a short reference video.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type reference_image_to_video \
  --model-id ima-pro-fast \
  --reference-images ./character-sheet.png \
  --reference-videos ./camera-motion.mp4 \
  --extra-params '{"duration":5,"resolution":"480p"}' \
  --prompt "keep the same character and follow the reference movement style" \
  --output-json
```

### 6. Seedance Multimodal Reference With Image And Audio

Use when `ima-pro` / `ima-pro-fast` should keep a visual subject from an image while also conditioning the output with narration, music, or rhythm from a short audio clip.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type reference_image_to_video \
  --model-id ima-pro-fast \
  --reference-images ./character-sheet.png \
  --reference-audios ./voiceover.mp3 \
  --extra-params '{"duration":5,"resolution":"480p","audio":true}' \
  --prompt "keep the same subject and align pacing to the reference audio" \
  --output-json
```

Reference mode is about identity and style guidance. For Seedance models, it can also incorporate short reference video and audio. For non-Seedance models, support remains limited to the capability exposed by the live catalog.

## Ambiguity Rule

Two or more input images without explicit roles are not auto-mapped. The runtime asks what each image is for before execution.
