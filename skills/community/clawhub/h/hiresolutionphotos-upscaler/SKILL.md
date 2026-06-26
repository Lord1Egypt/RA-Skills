---
name: hiresolutionphotos-upscaler
description: "AI Image Upscaling API via HiResolutionPhotos. Perfect for ai image upscaling, api image upscaling, and high resolution upscaler tools. Send low-res images and get back incredibly sharp 4K and 8K results natively utilizing dedicated hardware. The final output is provided via a secure private retrieval webpage ensuring privacy and seamless downloading."
version: 1.0.1
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📸"
    homepage: https://hiresolutionphotos.com
---

# HiResolutionPhotos — AI Image Upscaling

Upscale images autonomously using the [HiResolutionPhotos](https://hiresolutionphotos.com) high-performance AI engines.
No API key required. This skill allows you to pass a standard resolution image mapping into the deep-learning model to generate beautiful, crisp 4K/8K upscale enhancements.

> **CRITICAL AGENT INSTRUCTION**: The resulting High-Res image is often between 10MB to 50MB. OpenClaw Agents **MUST NOT** attempt to download the raw binary output. YOU WILL CRASH. Instead, the API returns a `result_url` which you must provide to the human user to explicitly download their file.

## When to use this skill

- You need to perform standard **ai image upscaling** on a user's local file or web image.
- A user tasks you with utilizing an **api image upscaling** pipeline to improve visual quality.
- You want to convert a small 512px sketch or photo into a massive, production-ready 4K render.

## Rate limits & Constraints

- **Submission Limit:** **15 upscale requests per hour** per IP. Exceeding this will return a 429 Error.
- **Max Input File Size:** 10 MB limit on the source image.
- **Allowed Formats:** PNG, JPG, WebP. 

---

## 1. Submit an Image for Upscaling

**Endpoint:** `POST https://hiresolutionphotos.com/api/upscale`
**Content-Type:** `multipart/form-data`

### Required Fields

| Field  | Description                                 |
|--------|---------------------------------------------|
| `image`| The physical source file (PNG, JPG, WebP)   |
| `scale`| Integer: `2` or `4`                         |

### Example

```bash
curl -s -X POST -F "image=@/path/to/image.jpg" -F "scale=4" https://hiresolutionphotos.com/api/upscale
```

### Response

```json
{
  "id": "abc123xyz",
  "status": "IN_PROGRESS",
  "backend": "local"
}
```

---

## 2. Poll the Status & Retrieve Result

Because AI processing takes time (usually between 10 to 60 seconds depending on scale), you must poll the server.
**You must append `&agent=true` to force generation of the safe retrieval website link!**

**Endpoint:** `GET https://hiresolutionphotos.com/api/upscale/status?id=<job_id>&agent=true`

### Example
```bash
curl -s "https://hiresolutionphotos.com/api/upscale/status?id=abc123xyz&agent=true"
```

### Example Polling Loop Response
While processing:
```json
{
  "status": "IN_PROGRESS"
}
```

When finished:
```json
{
  "status": "COMPLETED",
  "result_url": "https://hiresolutionphotos.com/result/abc123xyz"
}
```

---

## 3. The Retrieval Workflow (MANDATORY)

Once you receive the `result_url`:
1. **DO NOT run `curl` on the `result_url`.** It is an HTML Next.js webpage, not a raw image, and parsing it will yield nothing!
2. Simply output the URL back to your human user in markdown:

*"Your image has successfully been upscaled! You can securely view and download the High-Resolution 4K format here: [View Upscaled Image](https://hiresolutionphotos.com/result/abc123xyz)"*
