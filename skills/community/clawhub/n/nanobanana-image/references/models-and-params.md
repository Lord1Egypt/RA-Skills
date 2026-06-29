# Nano Banana Models and Parameters Quick Reference

## Model ID Reference

| Name | Model ID | Positioning |
|------|----------|-------------|
| Nano Banana 2 (recommended) | `gemini-3.1-flash-image` | Best overall performance, fast, most feature-rich |
| Nano Banana Pro | `gemini-3-pro-image` | Professional asset production, highest quality, slower |
| Nano Banana | `gemini-2.5-flash-image` | High concurrency, low latency, 1K resolution only |

---

## Feature Comparison

| Feature | gemini-3.1-flash-image | gemini-3-pro-image | gemini-2.5-flash-image |
|---------|------------------------|-------------------|------------------------|
| Max resolution | 4K | 4K | ~1K (fixed) |
| Min resolution | 512 (0.5K) | 1K | - |
| Reference images (high-fidelity objects) | Up to 10 | Up to 6 | Up to 3 |
| Reference images (character consistency) | Up to 4 characters | Up to 5 characters | - |
| Google Web Search | Yes | Yes | - |
| Google Image Search | Yes (exclusive) | - | - |
| Video input (YouTube/local) | Yes (exclusive) | - | - |
| Thinking mode | Configurable (minimal/high) | On by default, cannot be disabled | - |
| Thinking level | minimal / high | Fixed | - |

---

## Aspect Ratios (aspect_ratio)

### gemini-3.1-flash-image (most supported)

```
1:1  1:4  1:8  2:3  3:2  3:4  4:1  4:3  4:5  5:4  8:1  9:16  16:9  21:9
```

### gemini-3-pro-image / gemini-2.5-flash-image

```
1:1  2:3  3:2  3:4  4:3  4:5  5:4  9:16  16:9  21:9
```

---

## Resolution (image_size)

### gemini-3.1-flash-image

| image_size | 1:1 pixels | 16:9 pixels |
|------------|------------|-------------|
| `512` | 512x512 | 688x384 |
| `1K` (default) | 1024x1024 | 1376x768 |
| `2K` | 2048x2048 | 2752x1536 |
| `4K` | 4096x4096 | 5504x3072 |

### gemini-3-pro-image

| image_size | 1:1 pixels | 16:9 pixels |
|------------|------------|-------------|
| `1K` (default) | 1024x1024 | 1376x768 |
| `2K` | 2048x2048 | 2752x1536 |
| `4K` | 4096x4096 | 5504x3072 |

Note: `gemini-2.5-flash-image` does not support the `image_size` parameter; it outputs approximately 1024px by default.

---

## API Parameters

### generate_content Call Structure (Python)

```python
response = client.models.generate_content(
    model="gemini-3.1-flash-image",
    contents=[prompt],                           # or [prompt, image1, image2, ...]
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],   # or ["IMAGE"]
        response_format={
            "image": {
                "aspect_ratio": "16:9",
                "image_size": "2K",              # Gemini 3 series only
            }
        },
        tools=[{"google_search": {}}],           # Optional: Web Search
        thinking_config=types.ThinkingConfig(    # Optional: gemini-3.1-flash-image only
            thinking_level="High",
            include_thoughts=True,
        ),
    )
)
```

### Contents Description

| Type | Syntax | Description |
|------|--------|-------------|
| Text | `"prompt text"` or `types.Part(text=...)` | Description prompt |
| Local image | `Image.open("file.jpg")` | PIL Image object |
| YouTube video | `types.Part(file_data=types.FileData(file_uri="https://..."), video_metadata=...)` | 3.1 Flash only |
| Files API video | `types.Part(file_data=types.FileData(file_uri="files/..."))` | After uploading local video |

---

## Response Structure

```python
for part in response.parts:
    if part.thought:               # Thinking process (intermediate images)
        ...
    elif part.text is not None:    # Text description
        print(part.text)
    elif part.inline_data is not None:  # Image data
        image = part.as_image()    # PIL Image
        image.save("output.png")
```

---

## Error Codes / Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| `INVALID_ARGUMENT` | Invalid parameter format | Check aspect_ratio case, use uppercase K for image_size |
| `PERMISSION_DENIED` | Invalid or unactivated API Key | Check GEMINI_API_KEY environment variable |
| `RESOURCE_EXHAUSTED` | Rate limit exceeded | Reduce call frequency or upgrade quota |
| No image in response | Content safety block | Adjust prompt, avoid policy-violating content |
| image_size ignored | Using gemini-2.5-flash-image | Switch to gemini-3.1-flash-image |

---

## Notes

- All generated images contain **SynthID watermarks** (invisible)
- **Transparent backgrounds** are not supported; post-process if needed
- **Face generation** is subject to content policy restrictions
- Image Search cannot be used to search for real people
- Text rendering tip: let the model generate text first, then request images with text
- Video input: processes up to 131,072 tokens of frames (approximately video segments at 0.5 FPS)
