# Ancillary Assets for Product Videos

Use this guide to enrich Remotion scenes with generated assets.
Treat this as the default path for scene visuals unless the user opts out.

Do not outsource narrative structure to generated clips. Keep Remotion as the final editor and timeline authority.

## 1) Default Use

Use pixcli-generated outputs for:

- Stills and backgrounds.
- Transparent product/object assets for compositing.
- Scene illustrations and visual metaphors.
- Upscaled hero images for crisp renders.

Avoid using one generated image as the entire scene — compose it with text, animation, and branding in Remotion.

## 2) Scene-by-Scene Asset Suggestions

### Attention

- Generate one high-impact visual metaphor still.
- Use dramatic lighting and contrast to create urgency.

```bash
pixcli image "Frustrated [persona] dealing with [pain], cinematic lighting, high contrast, room for headline text" -r 16:9 -o public/assets/attention.png
```

### Interest

- Generate a clean product-context image.
- Keep visuals explanatory, not ornamental.

```bash
pixcli image "Same [persona] using [product context], clear relief and control, clean composition" -r 16:9 -o public/assets/interest.png
```

### Desire

- Generate use-case context visuals by persona/environment.
- Prefer 1 asset per use case over many shallow assets.

```bash
pixcli image "[Persona] achieving [result] with [product], authentic workplace context" -r 16:9 -o public/assets/desire.png
```

### Action

- Build CTA card in Remotion (text/vector layout in code).
- Support with a subtle background image or gradient.

```bash
pixcli image "Abstract subtle gradient background, dark theme, professional" -r 16:9 -o public/assets/cta-bg.png
```

## 3) Prompt Constraints

Add constraints to every asset prompt:

- Aspect ratio (`-r 16:9` or `-r 9:16`)
- Camera language in the prompt (close-up, wide, over-shoulder)
- Style consistency keywords reused across all scenes
- Use `-t` for transparent assets that will be composited

## 4) Asset Organization

```
public/
├── assets/
│   ├── attention.png
│   ├── interest.png
│   ├── desire-1.png
│   ├── desire-2.png
│   ├── cta-bg.png
│   └── product-nobg.png
└── audio/
    ├── vo-attention.mp3
    ├── vo-interest.mp3
    └── music.mp3
```

## 5) Integration Pattern in Remotion

1. Generate assets with `pixcli image` and `pixcli edit`.
2. Save files to `public/assets/`.
3. Reference in Remotion as `Img` components with `staticFile()`.
4. Control positioning, scaling, and animation in timeline code.

```tsx
import { Img, staticFile } from "remotion";

<Img src={staticFile("assets/hero.png")} style={{ width: "100%", height: "100%" }} />
```

## 6) Audio Assets

Generate voiceover, music, and sound effects with pixcli and save to `public/audio/`:

### Voiceover
```bash
pixcli voice "Tired of juggling ten different tools?" -o public/audio/vo-attention.mp3
pixcli voice "Meet FlowPilot — one dashboard, zero noise." -o public/audio/vo-interest.mp3
pixcli voice "Teams ship 40% faster with FlowPilot." -o public/audio/vo-desire.mp3
pixcli voice "Start free today at flowpilot.com" -o public/audio/vo-action.mp3
```

### Background music
```bash
pixcli music "Corporate ambient, builds gradually, positive energy, not overpowering" -d 45 -o public/audio/music.mp3
```

### Sound effects
```bash
pixcli sfx "Smooth cinematic whoosh transition" -d 1 -o public/audio/whoosh.mp3
pixcli sfx "Soft notification chime, positive" -d 1.5 -o public/audio/chime.mp3
pixcli sfx "Subtle UI click" -d 0.5 -o public/audio/click.mp3
```

### Mount in Remotion
```tsx
import { Audio, staticFile } from "remotion";

<Audio src={staticFile("audio/vo-attention.mp3")} />
<Audio src={staticFile("audio/music.mp3")} volume={0.3} />
<Audio src={staticFile("audio/whoosh.mp3")} startFrom={0} />
```
