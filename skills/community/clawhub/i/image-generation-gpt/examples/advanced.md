# Example — advanced image editing

This example covers the heavier features of `/v1/images/edits`:

- **Multiple reference images** in a single call (style transfer / composition)
- **Mask-based inpainting** to limit edits to a specific region
- **Custom 4K size** with the strict-size rules
- Switching to a non-default model (`flux-kontext-pro`)
- Transparent background output

---

## Scenario

You have three product photos and one logo image. You want to:

1. Composite the three products onto a single hero shot.
2. Replace only the background region (defined by a PNG mask) with a soft gradient.
3. Render at 4K landscape, transparent PNG so designers can drop it into Figma.

---

## Local files

```
./product-front.jpg     # 1200x1200
./product-side.jpg      # 1200x1200
./product-top.jpg       # 1200x1200
./brand-logo.png        # 512x512, transparent
./bg-mask.png           # 3840x2160, transparent only where bg should be replaced
```

---

## Trigger

```text
编辑图片：把这三张产品图拼成一张英雄banner，左下角加品牌 logo 水印，背景换成柔和的青蓝色渐变；输出 4K，透明背景，使用 flux-kontext-pro 模型
```

The skill collects the attached files and builds a `multipart/form-data` request.

---

## Equivalent raw request

```http
POST https://wellapi.ai/v1/images/edits
Authorization: Bearer $WELLAPI_API_KEY
Content-Type: multipart/form-data; boundary=----oc

------oc
Content-Disposition: form-data; name="model"

flux-kontext-pro
------oc
Content-Disposition: form-data; name="prompt"

Composite the three product shots into a single hero banner with the brand logo
as a watermark in the bottom-left, replace the background region with a soft
teal-to-blue gradient.
------oc
Content-Disposition: form-data; name="n"

1
------oc
Content-Disposition: form-data; name="size"

3840x2160
------oc
Content-Disposition: form-data; name="quality"

high
------oc
Content-Disposition: form-data; name="format"

png
------oc
Content-Disposition: form-data; name="background"

transparent
------oc
Content-Disposition: form-data; name="image"; filename="product-front.jpg"
Content-Type: image/jpeg

<binary>
------oc
Content-Disposition: form-data; name="image"; filename="product-side.jpg"
Content-Type: image/jpeg

<binary>
------oc
Content-Disposition: form-data; name="image"; filename="product-top.jpg"
Content-Type: image/jpeg

<binary>
------oc
Content-Disposition: form-data; name="image"; filename="brand-logo.png"
Content-Type: image/png

<binary>
------oc
Content-Disposition: form-data; name="mask"; filename="bg-mask.png"
Content-Type: image/png

<binary>
------oc--
```

Notes:

- Field name `image` is **repeated** — that's how you pass multiple reference images.
- `mask` is applied to the **first** `image` field. Same WxH as that image required, PNG, < 4 MB.
- The skill enforces total payload ≤ 50 MB and max 16 `image` parts before sending.

---

## Size validation (why `3840x2160` is legal)

| Rule | Check |
|---|---|
| Longest side ≤ 3840 | 3840 ≤ 3840 ✅ |
| Both dims multiple of 16 | 3840 % 16 = 0, 2160 % 16 = 0 ✅ |
| Aspect ratio ≤ 3:1 | 3840 / 2160 ≈ 1.78 ✅ |
| Pixel count in [655 360, 8 294 400] | 3840 × 2160 = 8 294 400 ✅ |

If any rule fails, the skill falls back to `size=auto` and tells you why.

---

## Response

```json
{
  "created": 1778240000,
  "background": "transparent",
  "data": [
    { "b64_json": "iVBORw0KGgo..." }
  ],
  "output_format": "png",
  "quality": "high",
  "size": "3840x2160",
  "usage": {
    "input_tokens": 612,
    "input_tokens_details": { "image_tokens": 604, "text_tokens": 8 },
    "output_tokens": 4096,
    "total_tokens": 4708
  }
}
```

---

## Skill output

```text
MEDIA:/Users/you/.openclaw/work/wellapi-1778240000.png
```

OpenClaw attaches the 4K PNG to the chat. Designers can right-click → save, or the agent can pipe it into the next skill (e.g., upload to Figma).

---

## Cost & latency tips

- `quality=high` + 4K is the most expensive combination — only use it for final renders.
- Mask inpainting is cheaper than full re-render, because the model only re-paints masked pixels.
- For drafts, start at `size=1024x1024` and `quality=low`, iterate the prompt, then re-run once at 4K.
- `gpt-image-2` is generally cheapest; `flux-kontext-pro` / `flux-kontext-max` are stronger at preserving identity/composition during edits.

---

## Common pitfalls

- **Mask not transparent in the right region.** The transparent pixels mark the area the model *will* edit. Fully opaque areas are preserved.
- **Mask dimensions ≠ image dimensions.** API returns 400. Resize the mask in Photoshop/GIMP first.
- **Total upload > 50 MB.** Convert reference JPEGs to lower quality, or downscale before sending.
- **Prompt over 1000 chars.** The skill truncates and warns; trim manually for predictable results.
