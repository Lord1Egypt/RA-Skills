# Prompt Examples Gallery

A collection of example prompts for different styles and use cases.

## Pixel Art

```
"A pixel art sword, 64x64, transparent background"
"A pixel art castle on a hill, 128x128, retro game style"
"A tiny pixel art cat, 32x32, white and orange"
"A pixel art potion bottle, glowing blue liquid"
```

## Logos & Branding

```
"A minimalist wolf logo, vector style, white on black"
"A geometric eagle logo, modern minimalist, silver on dark blue"
"A coffee cup icon, flat design, warm brown tones"
"A letter S monogram, elegant serif, gradient gold"
```

## Photo-Realistic

```
"A portrait photo of a woman, studio lighting, professional headshot"
"A landscape photo of autumn forest, golden hour light"
"A close-up photo of a mechanical watch, macro photography"
"A street scene in Tokyo at night, neon lights, cinematic"
```

## Creative & Abstract

```
"A holographic butterfly on a dark background, glowing colors"
"A floating island with waterfalls, fantasy art, dreamlike"
"A geometric crystal formation, glowing from within, dark void"
"A nebula in a bottle, cosmic colors, ethereal lighting"
```

## Characters

```
"A brave knight in shining armor, fantasy art, detailed"
"A cute robot mascot, blue and white, pixel art style"
"A wise old wizard with a long beard, mystical atmosphere"
"A fierce dragon, scales shimmering, ready to fly"
```

## Technical/Specifc

```
"A diagram showing neural network architecture, clean vector style"
"A flowchart of the user journey, minimalist white on blue"
"An exploded view of a mechanical keyboard, technical illustration"
"A heat map visualization, vibrant colors on dark background"
```

## Tips for Best Results

1. **Be specific** - Include style, colors, lighting, composition
2. **Add technical terms** - "transparent background", "studio lighting"
3. **Use style keywords** - "pixel art", "watercolor", "3D render"
4. ** Specify size** - "64x64", "1024x1024"
5. **Lighting matters** - "golden hour", "dramatic lighting", "soft light"

## Batch Generation

Generate multiple variations:

```bash
for prompt in "A red rose" "A blue rose" "A white rose" "A black rose"; do
    ~/.openclaw/workspace/scripts/flux-gen "$prompt"
    sleep 5
done
```
