# Web Image Optimization

## Responsive Images

Standard `srcset` widths: **320w, 640w, 768w, 1024w, 1366w, 1600w, 1920w**

```html
<img
  srcset="image-320.webp 320w,
          image-640.webp 640w,
          image-1024.webp 1024w,
          image-1920.webp 1920w"
  sizes="(max-width: 640px) 100vw,
         (max-width: 1024px) 50vw,
         33vw"
>
```

- Do not generate every possible size; match real CSS breakpoints.
- Four or five sizes is usually enough for one asset.
- Width descriptors are safer than DPR-only guesswork when layouts vary.
- If art direction changes by viewport, use `<picture>` or separate crops, not one crop forced everywhere.
- Do not force a single desktop crop into mobile if the subject or text loses meaning; mobile often needs a different crop, not just fewer pixels.

## LCP, Lazy Loading, and Fetch Priority

Use `loading="lazy"` for:
- Below-the-fold images
- Galleries and long lists

Do not lazy-load:
- Hero or likely LCP images
- First visible product or content images
- Critical background replacements that define the first viewport

Useful defaults:
- LCP image: `loading="eager"` and consider `fetchpriority="high"`
- Non-critical images: `loading="lazy"`

## Aspect Ratio and CLS

Always reserve space:

```html
<img width="800" height="600">
```

Or:

```css
.container { aspect-ratio: 16 / 9; }
```

Common ratios:

| Ratio | Use |
|------|-----|
| 16:9 | Hero banners, video covers |
| 4:3 | Traditional photos |
| 3:2 | DSLR photos |
| 1:1 | Products, avatars, social |
| 21:9 | Wide banners |

- Never ship web images without reserved space if layout stability matters.

## Format Rules for Web

- AVIF first when the stack and audience can handle it.
- WebP is the pragmatic default for most modern photo delivery.
- PNG stays useful for UI, screenshots, diagrams, and alpha-safe assets.
- JPEG is still a fallback, not a failure, when compatibility wins.
- SVG is ideal for icons and simple illustrations but must be validated against the target pipeline.
- OG and social-preview images are a special case: PNG or high-quality JPEG often survive platform ingest more predictably than aggressively compressed modern formats.
- Meaningful content images should not be hidden only in CSS backgrounds when semantic HTML image delivery would be more accessible and controllable.

## SVG and Text-in-Image Rules

- Run SVGs through SVGO.
- Keep `viewBox`; remove hardcoded `width` and `height` when CSS should control size.
- Inline very small critical SVGs; externalize bigger or reusable ones.
- Avoid embedding essential copy inside raster images when HTML text should carry meaning.
- If the SVG comes from design tools, inspect it for hidden raster layers, giant embedded paths, or exported cruft before shipping it.

## CMS and Pipeline Reality

- Many CMSs and site builders resize, rename, or recompress uploads after you hand them off.
- If the destination pipeline creates its own responsive derivatives, start from a clean master instead of pre-baking every size blindly.
- A web upload that looks sharp in the media library can still be rendered too large in the layout and become blurry.

## Delivery Traps

- Shipping one oversized source and trusting CSS to resize it.
- Using one crop for every breakpoint even when the composition breaks on narrow screens.
- Choosing AVIF for everything even when fallback or encoding time makes the workflow worse.
- Forgetting that email builders, CMS pipelines, and some older browsers may still flatten the format decision back to JPEG or PNG.

## Performance Checklist

```
□ LCP image not lazy-loaded
□ Width/height or aspect-ratio reserved
□ Modern format chosen intentionally
□ srcset/sizes only for real breakpoints
□ No oversized originals shipped to the browser
□ Alt text present when the image conveys meaning
```
