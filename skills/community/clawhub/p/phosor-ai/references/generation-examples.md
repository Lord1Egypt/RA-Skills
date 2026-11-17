# Generation examples

### MiniMax H3 — Text-to-Video

H3 is **duration-based**, not frame-based: it ignores `--num-frames` / `--fps` (output is
always 24fps) and bills per output second. Pick the frame size with
`--resolution-tier` + `--aspect` instead of `--width/--height`.

```bash
python3 scripts/phosor_client.py submit "A cat walking on a beach at sunset" \
  --model minimax/h3/text-to-video \
  --resolution-tier 768p --aspect 16:9 --duration 5
```

For the Turbo variant, keep the same inputs and add `/turbo` to the model ID:

```bash
python3 scripts/phosor_client.py submit "A cat walking on a beach at sunset" \
  --model minimax/h3/text-to-video/turbo \
  --resolution-tier 768p --aspect 16:9 --duration 5
```

### MiniMax H3 — Image-to-Video

```bash
# Upload first and use the returned s3_key; public HTTPS image URLs are also subject to URL validation
python3 scripts/phosor_client.py upload-image /path/to/first-frame.jpg

python3 scripts/phosor_client.py submit "The person starts dancing" \
  --model minimax/h3/image-to-video \
  --image-url "images/img-xxx.jpg" \
  --end-image-url "images/img-yyy.jpg" \
  --resolution-tier 480p --aspect 9:16 --duration 6
```

`--end-image-url` is optional and pins the closing frame.

### MiniMax H3 — Reference-to-Video (Ref2VA)

Feed reference **images**, **videos**, and **audio** together; you may refer to them positionally in
the prompt as `<Picture 1>`, `<Picture 2>`, … At least one of `--reference-image-urls` /
`--reference-video-urls` is required.

```bash
python3 scripts/phosor_client.py submit \
  "Use <Picture 1> and <Picture 2> as sequential keyframes; slow push-in, cinematic 35mm look." \
  --model minimax/h3/reference-to-video \
  --reference-image-urls "images/a.jpg,images/b.jpg" \
  --reference-audio-urls "audio/voice.mp3" \
  --resolution-tier 768p --aspect 16:9 --duration 5
```

Reference inputs are billed on top of the output — see **Ref2VA Pricing** below, and
**Ref2VA Reference Limits** for the caps (the same at 480p and 768p).

For Turbo Reference-to-Video, use `minimax/h3/reference-to-video/turbo` with the same
reference flags and duration/resolution/aspect controls.

### Text-to-Video (Wan)

Wan is frame-based. Add `/turbo` to the model id for the fast, ~3x cheaper variant
(it ignores `--steps` / `--guidance`).

```bash
# Submit T2V job (480p, 81 frames, 16fps)
python3 scripts/phosor_client.py submit "A cat walking on a beach at sunset" \
  --width 854 --height 480 --num-frames 81 --fps 16

# Check status
python3 scripts/phosor_client.py status <request_id>

# Get result (video URL)
python3 scripts/phosor_client.py result <request_id>
```

### Image-to-Video

**Two-step flow**: upload image first, then submit with the returned S3 key.

```bash
# Step 1: Upload image
python3 scripts/phosor_client.py upload-image /path/to/photo.jpg
# Returns: {"file_id": "img-xxx", "s3_key": "images/img-xxx.jpg", ...}

# Step 2: Submit I2V job using the s3_key as image_url
python3 scripts/phosor_client.py submit "The person in the photo starts dancing" \
  --image-url "images/img-xxx.jpg" --width 854 --height 480
```

### Text-to-Image

```bash
# Submit T2I job (1024x1024, default settings)
python3 scripts/phosor_client.py submit "A futuristic city skyline at dusk" \
  --model qwen-image/v2512/text-to-image --width 1024 --height 1024

# Generate multiple images at once (1-4)
python3 scripts/phosor_client.py submit "A futuristic city skyline at dusk" \
  --model z-image/turbo/text-to-image --width 1024 --height 768 --num-images 4

# Check status and get result (image URL)
python3 scripts/phosor_client.py status <request_id>
python3 scripts/phosor_client.py result <request_id>
# Returns: {"data": {"image": {"url": "..."}, "seed": 12345}, ...}
```

### Image-to-Image

**Two-step flow**: upload source image first, then submit with the returned S3 key.

```bash
# Step 1: Upload source image
python3 scripts/phosor_client.py upload-image /path/to/photo.jpg
# Returns: {"file_id": "img-xxx", "s3_key": "images/img-xxx.jpg", ...}

# Step 2: Submit I2I job using the s3_key as image_url
python3 scripts/phosor_client.py submit "Transform into oil painting style" \
  --model z-image/turbo/image-to-image --image-url "images/img-xxx.jpg" \
  --width 1024 --height 1024 --strength 0.7
```

### Image Edit (Multi-image Reference)

**Two-step flow**: upload reference images first, then submit with S3 keys as `image_urls`.

```bash
# Step 1: Upload reference images (up to 3)
python3 scripts/phosor_client.py upload-image /path/to/ref1.jpg
python3 scripts/phosor_client.py upload-image /path/to/ref2.jpg

# Step 2: Submit image-edit job
python3 scripts/phosor_client.py submit \
  "The girl in image 1 is wearing the outfit from image 2" \
  --model qwen-image/v2511/image-edit \
  --image-urls '["images/img-ref1.jpg","images/img-ref2.jpg"]' \
  --width 1024 --height 1024

```

### Speech-to-Video (S2V)

**Two-step flow**: upload both audio and reference image first, then submit with the returned S3 keys.

```bash
# Step 1: Upload reference image
python3 scripts/phosor_client.py upload-image /path/to/face.jpg
# Returns: {"file_id": "img-xxx", "s3_key": "images/img-xxx.jpg", ...}

# Step 2: Submit S2V job using the s3_key as image_url and audio URL as audio_url
python3 scripts/phosor_client.py submit "A person speaking naturally" \
  --model wan/v2.2-a14b/speech-to-video \
  --image-url "images/img-xxx.jpg" --audio-url "https://example.com/speech.wav" \
  --width 854 --height 480
```

### Animate

**Two-step flow**: upload both source video and reference image first, then submit.

```bash
# Step 1: Upload reference image
python3 scripts/phosor_client.py upload-image /path/to/character.jpg
# Returns: {"file_id": "img-xxx", "s3_key": "images/img-xxx.jpg", ...}

# Step 2: Submit Animate job using the s3_key as image_url and video URL as video_url
python3 scripts/phosor_client.py submit "The character performs the dance moves" \
  --model wan/v2.2-a14b/animate \
  --image-url "images/img-xxx.jpg" --video-url "https://example.com/dance.mp4" \
  --width 854 --height 480
```

### LTX Video 2.3: image and optional audio to video

Use `ltx-video/v2.3/image-audio-to-video`, not an invented alias. Required inputs:
`prompt`, `image_url`; optional `audio_url`. For example:

```bash
python3 scripts/phosor_client.py submit \
  --model ltx-video/v2.3/image-audio-to-video \
  "The subject turns slowly toward the camera" \
  --image-url "YOUR_UPLOADED_IMAGE_URL" --width 1280 --height 720 \
  --num-frames 121 --fps 24
```

480p costs USD 0.0008/frame; 720p USD 0.0012/frame. 121 frames at 720p estimate
USD 0.1452 / 1.452 credits. Do not use Wan's 16 fps conversion or frame alignment.
Use the supported size presets listed in the model reference.
1080p has no separate published rate key; confirm its quote before submitting.
See [LTX details](api.md#ltx-video-model-ids).

### Text-to-Image (GPT Image 2)

Its own resolution set and **always exactly 1 image** (`--num-images` is ignored).

```bash
python3 scripts/phosor_client.py submit "A ceramic mug on a linen cloth, soft window light" \
  --model openai/gpt-image-2/text-to-image --width 1024 --height 1024
```

Allowed sizes: **1024×1024, 1920×1072, 1072×1920, 2560×1440, 1440×2560**. Other sizes are rejected.
It ignores `--num-images`, `--steps` and `--guidance` — the only parameters it accepts are
prompt, model, width, height and seed.

### Text-to-Image (FLUX.2-dev)

FLUX.2-dev has its own resolution whitelist and is **fixed at 1 image per request**
(`--num-images` and `--steps` are ignored).

```bash
python3 scripts/phosor_client.py submit "Editorial product photo, soft window light" \
  --model flux2/dev/text-to-image --width 2048 --height 1536
```

### Image Edit (FLUX.2-dev)

```bash
python3 scripts/phosor_client.py upload-image /path/to/source.jpg

python3 scripts/phosor_client.py submit "Replace the background with a marble surface" \
  --model flux2/dev/image-edit --image-url "images/img-xxx.jpg" \
  --width 1024 --height 1024
```

### Text-to-Speech

TTS takes `text` (not a prompt) and is billed per character with a minimum charge.

```bash
python3 scripts/phosor_client.py submit-tts "Hello, welcome to Phosor AI." \
  --speaker Sohee --language English
```

### LoRA Upload (Custom Pre-trained)

**Video LoRA** requires two .safetensors files (high_noise + low_noise). **Image LoRA** requires a single .safetensors file.

```bash
# Video LoRA: upload two .safetensors files
python3 scripts/phosor_client.py upload-lora high_noise.safetensors low_noise.safetensors --name "My Style"

# Image LoRA: import single .safetensors file via URL
python3 scripts/phosor_client.py import-lora \
  "https://example.com/my_lora.safetensors" \
  --name "My Image Style"

# Video LoRA: import two files via URL
python3 scripts/phosor_client.py import-lora \
  "https://example.com/high_noise.safetensors" \
  "https://example.com/low_noise.safetensors" \
  --name "My Video Style"

# Check status, then use
python3 scripts/phosor_client.py lora-status <lora_id>
python3 scripts/phosor_client.py submit "A person walking" --lora-id <lora_id>
```

