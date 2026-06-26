---
name: pop_cam
description: AI image generation in any visual style — photorealistic, cinematic, cartoon, illustration, and more. Transform photos or generate from text prompts via the Pop-cam NanoBanana API.
version: 1.3.0
metadata:
  openclaw:
    requires:
      env:
        - POPCAM_API_TOKEN
      bins:
        - curl
    primaryEnv: POPCAM_API_TOKEN
    emoji: "\U0001F34C"
    homepage: https://www.pop-cam.com/openclaw
---

# Pop-cam NanoBanana Skill

Generate images with the Pop-cam NanoBanana API. The model supports **any visual style** — photorealistic, cinematic, cartoon, illustration, watercolor, 3D render, and anything else you can describe in a prompt.

This skill supports two modes:

- **Image-to-image**: send a base64-encoded photo and a prompt describing how to transform it.
- **Text-to-image**: send only a `prompt` field (no `image`) to generate an image from scratch.

Both modes cost 1 credit per generation and use the same endpoint.

## Authentication

All generation requests require a Pop-cam API token (`pk_` prefix) in the Authorization header.

If the user does not have a token yet, walk them through these steps **in order**:

1. **Sign up** at https://www.pop-cam.com/sign-up (skip if they already have an account).
2. **Sign in** at https://www.pop-cam.com/sign-in.
3. **Create an API token** at https://www.pop-cam.com/developer — label it "OpenClaw". Copy the token immediately; it is only shown once.

Store the token and send it on every request:

```
Authorization: Bearer pk_YOUR_TOKEN
```

If unsure whether the user is signed in, call the auth-status endpoint first:

```bash
curl https://www.pop-cam.com/api/openclaw/auth-status
```

The response tells you whether sign-in is needed and provides the relevant URLs.

## Skill Definition JSON

For a machine-readable version of this entire skill (features, endpoints, schemas, examples), call:

```bash
curl https://www.pop-cam.com/api/openclaw/skill
```

## Generation Endpoint

```
POST https://www.pop-cam.com/api/v1/nanobanana
```

### Headers

| Header | Value |
|--------|-------|
| Authorization | `Bearer pk_YOUR_TOKEN` |
| Content-Type | `application/json` |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | string | No | Base64 data URL of the source image (`data:image/png;base64,...`). **Omit entirely for text-to-image.** |
| `prompt` | string | No | Generation prompt. **Required when `image` is omitted.** Optional for image-to-image (a default prompt is used if omitted). |
| `webhook_url` | string | No | HTTPS URL to receive the result asynchronously. Omit for synchronous mode. |

### Image-to-Image Example

Transform an existing photo:

```bash
curl -X POST https://www.pop-cam.com/api/v1/nanobanana \
  -H "Authorization: Bearer $POPCAM_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/png;base64,iVBOR...",
    "prompt": "Enhance this photo with cinematic lighting and shallow depth of field"
  }'
```

### Text-to-Image Example

Generate an image from a text prompt only — no source photo needed:

```bash
curl -X POST https://www.pop-cam.com/api/v1/nanobanana \
  -H "Authorization: Bearer $POPCAM_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A photorealistic portrait of a man in a leather jacket standing on a city rooftop at golden hour, natural lighting, shallow depth of field"
  }'
```

### Synchronous Response (200)

```json
{
  "job_id": "a1b2c3d4-...",
  "image_url": "https://cdn.pop-cam.com/generated/user_id/a1b2c3d4.png",
  "download_url": "https://...r2.cloudflarestorage.com/...?X-Amz-Signature=...",
  "used_prompt": "A photorealistic portrait of a man in a leather jacket standing on a city rooftop at golden hour, natural lighting, shallow depth of field",
  "credits_remaining": 22,
  "mode": "text-to-image"
}
```

**Important**: Use `download_url` to fetch the generated image. It is a presigned URL valid for 1 hour that works regardless of storage bucket privacy settings. The `image_url` is the permanent stored reference but may not be directly accessible if the bucket is private.

The `mode` field is `"text-to-image"` or `"image-to-image"` depending on which path was used.

### Webhook / Async Mode

Include `webhook_url` to get an immediate HTTP 202 response with a `job_id`. Pop-cam POSTs the result to your URL when generation completes (retries up to 3 times with exponential backoff).

Initial response (202):

```json
{
  "job_id": "a1b2c3d4-...",
  "status": "processing",
  "message": "Your image is being generated. Results will be POSTed to your webhook_url."
}
```

Webhook delivery payload includes `download_url` (presigned, 1-hour expiry) for fetching the image.

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid or missing token | Ask the user to create or refresh their token at https://www.pop-cam.com/developer |
| 402 | Insufficient credits | Direct the user to buy credits at https://www.pop-cam.com/checkout |
| 403 | Account not synced | Ask the user to sign in via the web app first |
| 400 | Bad request (e.g. missing prompt for text-to-image, invalid image format) | Check the request body and fix the issue |

## Credits

- Each generation (both modes) costs **1 credit**.
- New accounts receive starter credits for free.
- Every response includes `credits_remaining`.
- Purchase more at https://www.pop-cam.com/checkout.

## Prompt Tips

The model is **not limited to any single style**. The output depends entirely on your prompt. Here are example styles you can request:

| Style | Example prompt snippet |
|-------|----------------------|
| Photorealistic | "photorealistic photo, natural lighting, 85mm lens" |
| Cinematic | "cinematic still frame, anamorphic lens flare, moody color grading" |
| Cartoon | "colorful cartoon style, bold outlines, flat shading" |
| Illustration | "editorial illustration, clean vector style" |
| Oil painting | "oil painting on canvas, visible brushstrokes, impressionist style" |
| Watercolor | "delicate watercolor painting, soft washes, paper texture" |
| 3D render | "3D rendered scene, volumetric lighting, octane render" |
| Pencil sketch | "detailed pencil sketch on white paper, crosshatching" |
| Anime | "anime style, Studio Ghibli-inspired, vibrant colors" |

For the most realistic output, include details like lighting conditions, camera lens, depth of field, and environment in your prompt.

## Quick Reference

| Task | How |
|------|-----|
| Transform a photo | Send `image` + optional `prompt` |
| Generate from text | Send `prompt` only, **no `image` field** |
| Download the result | Use `download_url` from the response (presigned, 1-hour expiry) |
| Async processing | Add `webhook_url` to the request body |
| Check auth state | `GET /api/openclaw/auth-status` |
| Full skill JSON | `GET /api/openclaw/skill` |
| Buy credits | https://www.pop-cam.com/checkout |
| Create token | https://www.pop-cam.com/developer |
