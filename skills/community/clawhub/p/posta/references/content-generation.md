# AI Content Generation Patterns

## Image Generation — fal.ai (FLUX)

Generate images using FLUX models via fal.ai.

**Endpoint:** `https://fal.run/fal-ai/flux/schnell` (fast/cheap) or `https://fal.run/fal-ai/flux/dev` (higher quality)

**Required:** `FAL_KEY` environment variable.

- **Get a key:** Sign up at https://fal.ai and create a key at https://fal.ai/dashboard/keys
- **Key format:** `<key_id>:<key_secret>` (contains a colon)
- **Auth header:** `Authorization: Key ${FAL_KEY}`
- **Auto-discovery:** The skill searches env vars, `~/.posta/credentials`, and `.env` files (dedicated config only — shell profiles are never read)
- **Validation:** Run `fal_validate_key` to confirm your key is set before generating images

**Error handling:**
```bash
# Validate before spending credits
fal_validate_key || { echo "Fix your fal.ai key first"; exit 1; }
```

### Request

```bash
RESULT=$(curl -s -X POST "https://fal.run/fal-ai/flux/schnell" \
  -H "Authorization: Key ${FAL_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "your prompt here, photorealistic, natural colors, proper white balance, vivid but not oversaturated, clean lighting, high quality, detailed, subtle background",
    "image_size": "square_hd",
    "num_images": 1,
    "enable_safety_checker": true
  }')

IMAGE_URL=$(echo "$RESULT" | jq -r '.images[0].url')
CONTENT_TYPE=$(echo "$RESULT" | jq -r '.images[0].content_type // "image/jpeg"')
```

**Response:** JSON with a hosted image URL — upload it to Posta with `posta_upload_from_url "$IMAGE_URL" "$CONTENT_TYPE"` (no local file needed).

```json
{
  "images": [{ "url": "https://fal.media/files/.../out.jpg", "width": 1024, "height": 1024, "content_type": "image/jpeg" }],
  "seed": 123456,
  "has_nsfw_concepts": [false]
}
```

### `image_size` by Aspect Ratio

| `image_size`     | Pixels    | Use Case |
|------------------|-----------|---------------------|
| `square_hd`      | 1024×1024 | Instagram feed |
| `portrait_16_9`  | 1080×1920 | TikTok, Reels, Stories |
| `landscape_16_9` | 1920×1080 | LinkedIn, X/Twitter |
| `portrait_4_3`   | 1080×1440 | Pinterest |

(You can also pass a custom `{"image_size": {"width": 1024, "height": 1024}}`.)

### Prompt Tips
- Append quality modifiers: "photorealistic, natural colors, proper white balance, high quality, detailed"
- FLUX has no `negative_prompt` — describe what you *want*, not what to avoid
- `fal-ai/flux/dev` gives higher fidelity (slower/pricier); `fal-ai/flux/schnell` is fast and cheap
- Pass a fixed `"seed"` for reproducible results from the same prompt

---

## Captions & Hashtags

Write captions and hashtags yourself — you are Claude, so no external text-generation API (Gemini/OpenAI) is needed. Tailor copy to each platform: hook in the first line, a clear call to action, platform-appropriate length and tone, and a sensible hashtag mix (broad + niche). Always include relevant hashtags by default.

---

## Combined Workflow: Generate Image + Caption + Post

Full workflow using bash helper functions:

```bash
# Source the helper
source "${POSTA_SKILL_ROOT:-${OPENCLAW_SKILL_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}}/skills/posta/scripts/posta-api.sh"

# 1. Generate image with fal.ai (FLUX)
RESULT=$(curl -s -X POST "https://fal.run/fal-ai/flux/schnell" \
  -H "Authorization: Key ${FAL_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "a beautiful sunset over mountains, photorealistic, vivid colors, high quality",
    "image_size": "square_hd",
    "num_images": 1
  }')
IMAGE_URL=$(echo "$RESULT" | jq -r '.images[0].url')

# 2. Upload the hosted image to Posta
MEDIA_ID=$(posta_upload_from_url "$IMAGE_URL" "image/jpeg")

# 3. Write the caption yourself (you are Claude) — no text API needed
CAPTION="Golden hour over the peaks 🌄 Nature's daily masterpiece. Where would you watch this from?"

# 4. Get connected accounts
ACCOUNTS=$(posta_list_accounts)
# Parse account IDs for target platforms

# 5. Create and schedule post
posta_create_post "{
  \"caption\": \"${CAPTION}\",
  \"hashtags\": [\"sunset\", \"mountains\", \"nature\", \"photography\"],
  \"mediaIds\": [\"${MEDIA_ID}\"],
  \"socialAccountIds\": [\"account-id-1\", \"account-id-2\"],
  \"isDraft\": false,
  \"scheduledAt\": \"2026-03-02T09:00:00Z\"
}"
```

---

## Platform-Specific Tips

| Platform | Best Image Size | Caption Length | Hashtag Limit |
|-----------|----------------|---------------|---------------|
| Instagram | 1080x1080 (feed), 1080x1920 (stories/reels) | 2200 chars | 30 |
| TikTok | 1080x1920 | 2200 chars | varies |
| X/Twitter | 1200x675 | 280 chars | 3-5 recommended |
| LinkedIn | 1200x627 | 3000 chars | 3-5 recommended |
| Facebook | 1200x630 | 63,206 chars | minimal |
| Pinterest | 1000x1500 | 500 chars | 20 |
| YouTube | 1280x720 (thumbnail) | 5000 chars | 500 chars total |
| Threads | 1080x1080 | 500 chars | minimal |
