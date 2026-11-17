# Product ad video: worked recipes

Three end-to-end recipes for `product-ad-video`. Each shows the scenario, the real async request, the poll step, and the result shape. Confirm field names and ranges against the live schema (`runware-run`) before sending. AIRs verified `live` in the Runware catalog.

Shared contract for all three:

- `taskType` is `videoInference`, `deliveryMethod` is `async`.
- The async call returns a `taskUUID`. Poll `getResponse` until the task is terminal, then read `videoURL`.
- The starting image goes in `inputs.frameImages` as `[{ "image": <url|base64>, "frame": "first" }]`. The prompt directs motion and camera only and does not re-describe the product the image already fixes.
- Terminal result shape (one entry):
  ```json
  {
    "taskType": "videoInference",
    "taskUUID": "…",
    "videoUUID": "…",
    "videoURL": "https://vm.runware.ai/video/…mp4",
    "seed": 1234567890
  }
  ```

---

## Recipe 1: Product still to a hero motion clip

**Scenario.** A clean studio still of a perfume bottle becomes a 10-second landing-page hero. Slow push-in, a slow orbit, light catching the glass. Cinematic polish with native audio, so route to Veo 3.1.

On Veo 3.1, sending a starting image forces `duration` to `8`, and `resolution` (`720p`/`1080p`/`4K`) is only available alongside `frameImages`. Native audio is on by default through `providerSettings.google.generateAudio`.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "8f2c1a90-7b3d-4e6f-9a21-0c4d5e6f7a8b",
    "model": "google:3@2",
    "deliveryMethod": "async",
    "inputs": {
      "frameImages": [
        { "image": "https://example.com/perfume-hero-still.jpg", "frame": "first" }
      ]
    },
    "positivePrompt": "Slow cinematic push-in toward the bottle, then a gentle quarter orbit around it. Soft studio key light sweeps across the glass and catches a highlight on the cap. The camera move is steady and unhurried. Quiet ambient room tone, no music.",
    "duration": 8,
    "resolution": "1080p",
    "providerSettings": {
      "google": {
        "generateAudio": true
      }
    }
  }
]
```

Poll `getResponse` on the returned `taskUUID` until terminal, then read `videoURL`. For a silent clip, set `providerSettings.google.generateAudio` to `false` and add narration later through the `voiceover` skill.

---

## Recipe 2: Swap a product into existing footage

**Scenario.** A creator pitch was already shot holding a competitor's tumbler. Drop in the client's brushed-steel tumbler without re-shooting, keeping the creator, motion, timing, camera, and audio. This is a swap, not a generate, so route to Pruna P-Video-Replace.

The model takes the source clip under `inputs.video` and one to three clean product photographs under `inputs.referenceImages`. The `positivePrompt` names the exact element to replace and everything that must stay, then closes with the load-bearing "only X changes, everything else stays" line. The reference is a bare product shot (no person, no hands, plain background) framed to match how the source presents the object.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "model": "prunaai:p-video@replace",
    "deliveryMethod": "async",
    "inputs": {
      "video": "https://example.com/source-creator-pitch.mp4",
      "referenceImages": ["https://example.com/ref-product-tumbler.jpg"]
    },
    "positivePrompt": "Replace the matte-black tumbler the woman is holding in the source video with the brushed-stainless-steel coffee tumbler from the reference image. Preserve the woman, her face, her hair, her clothing, her gestures, her speech, the studio, the lighting, the camera, and the audio exactly as they appear in the source. Only the object in her right hand should change; everything else stays as the source.",
    "resolution": "720p"
  }
]
```

Poll `getResponse`, then read `videoURL`. Run the variant batch at `720p` for review, then re-run only the approved variants at `1080p`. To swap a garment and the product in one call, add a second reference image (`referenceImages` accepts up to 3) and index each in the prompt ("reference image 1", "reference image 2").

---

## Recipe 3: Short looping social cut

**Scenario.** A sneaker still becomes a fast 5-second vertical loop for paid social. Tight motion, quick rotation, energetic feel. Draft cheap and fast on Kling 3.0 Turbo before committing to a flagship pass.

Kling 3.0 Turbo takes the starting image in `inputs.frameImages` (first frame only). `duration` is an integer from 3 to 15 (use `5`). With a starting image, set aspect through `resolution` (`720p`/`1080p`), not `width`/`height`.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "3c9e7f10-2a4b-4d8c-b6e1-5f9a0b1c2d3e",
    "model": "klingai:kling-video@3.0-turbo",
    "deliveryMethod": "async",
    "inputs": {
      "frameImages": [
        { "image": "https://example.com/sneaker-still.jpg", "frame": "first" }
      ]
    },
    "positivePrompt": "The sneaker rotates a smooth continuous turn on its axis as the camera holds a tight vertical frame. A quick sweep of light crosses the upper as it turns. Energetic, clean, looping motion that ends near where it began.",
    "duration": 5,
    "resolution": "720p"
  }
]
```

Poll `getResponse`, read `videoURL`, and review the motion. Once the move is locked, re-run the approved take on a flagship (Seedance 2.0 `bytedance:seedance@2.0`, Veo 3.1 `google:3@2`, or Wan2.7 `alibaba:wan@2.7`) at full resolution. Seedance accepts the same `frameImages` first-frame shape and takes `duration` as an integer from 4 to 15 with `resolution` of `480p`/`720p`/`1080p`/`4k`.

---

## Brand-safety check on every output

No invented claims, ratings, testimonials, or reviews. No fabricated logos or award badges. No readable on-screen copy unless the user supplied the exact wording. Retry or cut anything that asserts a fact the user did not provide.
