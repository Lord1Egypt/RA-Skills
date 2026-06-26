# Gemini Image Generation API Reference

## Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent
```

## Authentication

Header: `Authorization: Bearer {GEMINI_API_KEY}`

Or query parameter: `key={GEMINI_API_KEY}`

## Supported Models

- `gemini-3.1-flash-image-preview` — **Default**, higher quality image generation (recommended)
- `gemini-2.5-flash-image` — Faster, lighter weight alternative

Note: These are Gemini models with native image generation capabilities.

## Request Format (Gemini)

```json
{
  "contents": [{
    "role": "user",
    "parts": [{ "text": "Your image generation prompt here" }]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
```

## Response Format (Gemini)

```json
{
  "candidates": [{
    "content": {
      "parts": [{
        "inlineData": {
          "mimeType": "image/png",
          "data": "base64_encoded_image"
        }
      }]
    }
  }]
}
```

## Aspect Ratios

Gemini supports these aspect ratios natively:

- `1:1` — Square (default)
- `4:3` — Standard landscape
- `16:9` — Widescreen
- `9:16` — Portrait/mobile
- `3:4` — Portrait

Map to nearest supported ratio when user requests unsupported ratios.

## Image Size Mapping

Requested size → Approximate pixels:

- `1K` → ~1024px on the longer edge
- `2K` → ~2048px on the longer edge (default)
- `4K` → ~3840px on the longer edge

Note: Gemini returns images at native resolution based on aspect ratio.

## Prompt Engineering

### Effective Prompt Structure

```
[Subject] + [Style/Modality] + [Composition] + [Lighting/Mood] + [Technical specs]

Example:
"A minimalist event poster for a jazz concert, art deco style, 
central illustration of a saxophone with geometric patterns, 
warm amber lighting on dark navy background, professional print quality"
```

### Style Keywords

- Photography: `photorealistic`, `cinematic`, `documentary`
- Illustration: `vector art`, `watercolor`, `line art`, `minimalist`
- Design: `flat design`, `material design`, `brutalist`, `art deco`
- Mood: `vibrant`, `moody`, `elegant`, `playful`, `professional`

### What to Avoid

- Copyrighted characters or brands
- Specific real people (unless you have rights)
- Text in the image (Gemini may render garbled text)
- Overly complex scenes with multiple focal points

## Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Invalid request | Check prompt for safety violations |
| 429 | Rate limit | Retry with backoff |
| 500 | Server error | Retry after delay |
| 503 | Service unavailable | Retry later |

## Retry Strategy

```javascript
const MAX_ATTEMPTS = 3;
const BASE_DELAY_MS = 1000;

for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
  try {
    return await generateImage(prompt);
  } catch (error) {
    if (attempt === MAX_ATTEMPTS) throw error;
    const delay = BASE_DELAY_MS * Math.pow(2, attempt - 1);
    await sleep(delay);
  }
}
```

## Rate Limits

- Free tier: 15 requests per minute
- Paid tier: Varies by model and project

Monitor `x-ratelimit-remaining` header in responses.

## Cost Considerations

- 1K images: ~$0.001-0.003 per image
- 2K images: ~$0.002-0.006 per image
- 4K images: ~$0.004-0.012 per image

Prices vary by model tier (Flash vs Pro).

## Reference Image Support

Include reference images for:
- Style transfer ("in the style of this image")
- Product placement ("place this product in the scene")
- Background replacement ("use this background")

Base64 encode images and include in `parts` array before the text prompt.

Example:
```json
{
  "contents": [{
    "role": "user",
    "parts": [
      {
        "inline_data": {
          "mime_type": "image/jpeg",
          "data": "base64_encoded_image_data"
        }
      },
      {"text": "Create a poster in this style..."}
    ]
  }]
}
```

## Safety Filtering

Gemini applies safety filters that may:
- Block certain prompts
- Blur or refuse generation
- Return empty results

Handle gracefully by:
1. Detecting empty/missing image in response
2. Providing user-friendly error message
3. Offering to adjust prompt

## API Integration

The skill uses **Gemini models** with native image generation:

- **Primary**: `gemini-3.1-flash-image-preview` (recommended)
  - Higher quality image generation
  - More powerful capabilities
  
- **Alternative**: `gemini-2.5-flash-image` ("Nano Banana")
  - Faster, lighter weight
  - Good for quick drafts

These models use the standard Gemini API with `responseModalities: ["TEXT", "IMAGE"]` to enable image generation.
