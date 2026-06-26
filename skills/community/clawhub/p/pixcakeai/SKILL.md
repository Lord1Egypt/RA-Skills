# Photo Enhance Skill

Enhance photos with Canon IXUS 130 CCD effect and custom watermark.

## Description

This skill applies professional photo enhancements:
- Canon IXUS 130 classic CCD camera effect
- Skin retouching with clarity preservation
- Color optimization
- Optional custom text watermark at bottom

## Usage

Upload a photo and optionally provide `watermark_text` parameter.

### Examples

**Basic enhancement:**
```json
{
  "image": "base64_or_file",
  "effect": "ixus130"
}
```

**With watermark:**
```json
{
  "image": "base64_or_file",
  "watermark_text": "© 2026 My Name"
}
```

## Parameters

| Name | Type | Required | Default |
|------|------|----------|---------|
| image | file | Yes | - |
| watermark_text | string | No | null |
| effect | string | No | ixus130 |

## Output

- Format: JPEG
- Quality: 95%
- Progressive: true

## Effects Applied

1. Sharpening (sigma: 1.2)
2. Brightness +8%, Saturation +15%
3. Light blur (0.3) for skin softening
4. Final sharpening (sigma: 0.8)
5. Color grading (brightness +5%, saturation +12%)
6. Gamma correction (1.02)
7. Optional watermark (bottom, 12% height)

## Security

- Pure memory processing (no file system access)
- Input validation
- XSS protection (XML escaping)
- No data retention
