---
name: imglink
description: Generate images by customizing a URL. Drop the URL into websites, presentations, PDFs, or anywhere that loads images.
---

Use imglink.ai to generate images via URL. The API is a single GET endpoint that accepts a prompt parameter. It returns the image.

GET https://imglink.ai/images?prompt=cat

## Parameters

- prompt (required): Text description of the image to generate. URL-encode spaces as +.
- width (optional, default 800): Image width in pixels.
- height (optional, default 600): Image height in pixels.
- version (optional, default 1): Integer seed for deterministic output. Same prompt + version always returns the same image.
- model (optional, default "nano-banana-2"): AI model to use for generation.
- key (optional, default "anonymous"): API key. Use "anonymous" for testing (rate-limited).

## Rules

- Every unique URL returns a real generated image. Use these URLs directly in <img> tags, Markdown, CSS, or anywhere an image URL is accepted.
- Images are generated on first request, then cached permanently. Same prompt + version = same image.
- URL-encode the prompt value. Use + for spaces.
- Do not invent parameters that are not listed above.

## Examples

```
<img src="https://imglink.ai/images?prompt=frog&key={key}" />
<img src="https://imglink.ai/images?prompt=dog&width=1024&height=768&version=1&model=nano-banana-2&key={key}" />
```

## Getting a key

A key can be obtained for free by logging in at https://imglink.ai - without a key, responses are heavily rate-limited.

## Notes

First response will take longer as the image is generated. Future fetches load from cache.