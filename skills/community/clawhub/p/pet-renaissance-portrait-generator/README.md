# Pet Renaissance Portrait Generator

Generate stunning royal Renaissance oil painting portraits of any pet from text descriptions. Describe your dog, cat, rabbit, or any pet, and receive a museum-quality baroque masterpiece depicting them as 17th-century aristocrats, medieval knights, or baroque nobility — complete with velvet robes, ornate gold jewelry, and dramatic Rembrandt lighting.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

**Via npx skills:**
```bash
npx skills add blammectrappora/pet-renaissance-portrait-generator
```

**Via ClawHub:**
```bash
clawhub install pet-renaissance-portrait-generator
```

---

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

```bash
node petrenaissanceportraitgenerator.js "<prompt>" --token YOUR_TOKEN [--size <size>] [--ref <uuid>]
```

### Examples

Generate a portrait of a golden retriever as a Renaissance nobleman:
```bash
node petrenaissanceportraitgenerator.js \
  "a majestic golden retriever dressed in elaborate 17th-century aristocratic clothing, velvet robes, ornate gold jewelry, regal pose, dramatic Rembrandt lighting, baroque oil painting style" \
  --token "$NETA_TOKEN"
```

Generate a landscape-format portrait of a Persian cat as a royal duchess:
```bash
node petrenaissanceportraitgenerator.js \
  "a regal Persian cat in the style of a baroque duchess portrait, wearing an ornate lace collar and pearl necklace, rich jewel-toned background, old master painting" \
  --token "$NETA_TOKEN" \
  --size landscape
```

Use a reference image UUID for style inheritance:
```bash
node petrenaissanceportraitgenerator.js \
  "a noble beagle in a 17th-century military uniform, dramatic lighting, Renaissance oil painting" \
  --token "$NETA_TOKEN" \
  --ref "some-picture-uuid-here"
```

### Output

Returns a direct image URL printed to stdout. Redirect or pipe it as needed:

```bash
IMAGE_URL=$(node petrenaissanceportraitgenerator.js "a majestic tabby cat in velvet robes" --token "$NETA_TOKEN")
echo "$IMAGE_URL"
```

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | *(required)* | Your Neta API token |
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--ref` | UUID string | *(none)* | Reference image UUID for style inheritance |

### Size Dimensions

| Size | Width | Height |
|------|-------|--------|
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `square` | 1024 | 1024 |
| `tall` | 704 | 1408 |

---

## Default Prompt

If you want a ready-made starting point, try this default prompt (replace `[pet breed]` with your pet's breed):

```
a majestic Renaissance oil painting portrait of a [pet breed], dressed in elaborate 17th-century aristocratic clothing, velvet robes, ornate gold jewelry and collar, regal dignified pose, dramatic Rembrandt lighting, rich jewel-toned background, museum-quality baroque masterpiece, highly detailed brushwork, old master painting style
```

---

## How It Works

1. Your text description is sent to the Neta AI image generation API.
2. The API queues a generation job and returns a task UUID.
3. The script polls for completion every 2 seconds (up to 90 attempts / ~3 minutes).
4. When the image is ready, the direct image URL is printed to stdout.

