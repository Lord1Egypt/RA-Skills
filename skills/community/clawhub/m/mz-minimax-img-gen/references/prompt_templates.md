# MiniMax Image-01 Prompt Templates

## Region & API Configuration

| Region | API Endpoint | Get Key From |
|--------|-------------|-------------|
| **China** | `api.minimax.chat` | platform.minimaxi.com |
| **Global** | `api.minimax.io` | www.minimax.io |

Set region in script: `--region cn` or `--region global`

---

## Style Templates

Replace `{subject}` with your content:

### Photography
```
Professional photography of `{subject}`, soft natural lighting, shallow depth of field, Canon 85mm f/1.4, film grain, warm tones, 4K resolution
```

### Digital Art / Illustration
```
Digital illustration of `{subject}`, vibrant colors, detailed linework, Studio Ghibli inspired, anime style, 4K resolution
```

### Cyberpunk / Sci-Fi
```
Cyberpunk `{subject}`, neon lighting, rain-slicked streets, Blade Runner atmosphere, dark moody tones, cinematic, highly detailed
```

### Product Photography
```
Clean product photography of `{subject}`, white background, soft studio lighting, commercial quality, minimalist, 4K
```

### UI / Interface
```
Modern UI design of `{subject}`, clean interface, Figma style, dark mode, glassmorphism, 4K resolution
```

### 3D Rendering
```
3D render of `{subject}`, octane render, unreal engine, soft shadows, studio lighting, 8K quality, hyperrealistic
```

### Fantasy
```
Fantasy scene of `{subject}`, magical lighting, epic composition, detailed environment, digital art, 4K, masterpiece
```

### Portrait
```
Portrait of `{subject}`, professional photography, soft lighting, natural skin tones, detailed, 4K, studio quality
```

---

## Quality Parameters Reference

| Category | Keywords |
|----------|----------|
| Lighting | cinematic lighting, soft natural light, volumetric light, rim lighting, golden hour |
| Details | intricate details, hyperrealistic, macro detail, sharp focus |
| Mood | moody, ethereal, dramatic, serene, dark and moody |
| Quality | 4K, 8K, masterpiece, professional quality, highly detailed |
| Camera | Canon 85mm, f/1.4, shallow depth of field, wide angle |

---

## Aspect Ratios

| Ratio | Dimensions | Best For |
|-------|-----------|---------|
| 16:9 | 1920×1080 | Landscape, video thumbnails |
| 1:1 | 1024×1024 | Social media, cards |
| 9:16 | 1080×1920 | Mobile, stories, vertical |
| 4:3 | 1024×768 | Blog posts, documentation |
| 21:9 | 2560×1080 | Ultrawide, cinematic |

---

## Usage Examples

```bash
# China user - generate cyberpunk scene
python image_gen.py "neon city at night with flying cars" --region cn --aspect 16:9

# Global user - product photography
python image_gen.py "modern wireless headphones" --region global --aspect 1:1 --n 4

# Disable enhancement (raw prompt)
python image_gen.py "simple geometric pattern" --region cn --no-enhance

# Generate multiple variations
python image_gen.py "fantasy castle landscape" --region global --n 9 --aspect 21:9
```

---

**Author:** Mzusama
