# Paper Collage Remotion Skill

A reusable Codex skill for creating layered paper-cutout animations in Remotion.

It turns a script into a controlled local video workflow: plan shots, generate or supply independent cutouts, remove chroma-key backgrounds, split character sheets, stage depth, animate by narrative role, and render with Remotion.

## What it covers

- Background, distant, subject, foreground, and caption layer planning
- Independent PNG character and prop workflow
- Green-screen removal with a soft alpha matte
- Grid-based character-sheet splitting
- Staggered entrances, cut-paper outlines, shadow, parallax, and occlusion
- Remotion Studio, still-render, FFmpeg, and final-video checks
- A configuration-driven Remotion starter and automatic asset validation

## Install

Copy this folder to your Codex skills directory:

```bash
git clone https://github.com/ToBeWin/paper-collage-remotion-skill.git
cp -R paper-collage-remotion-skill "${CODEX_HOME:-$HOME/.codex}/skills/paper-collage-remotion"
```

Restart or refresh Codex, then invoke it with:

```text
Use $paper-collage-remotion to create a layered paper-collage animation from my script and assets.
```

## Local utilities

Remove a uniform green background:

```bash
python scripts/key_to_alpha.py input-green.png output-alpha.png --tolerance 92
```

Split an alpha character sheet into four layers:

```bash
python scripts/split_sheet.py characters-alpha.png public/assets/layers character 4 --columns 2 --rows 2
```

Both scripts require Pillow:

```bash
python -m pip install Pillow
```

## Starter template

Copy `assets/remotion-starter/` to a new directory, then add your own images under its `public/` folder and edit only `script.json` for shot timing, captions, positions, sizes, z-order, and stagger delays.

```bash
cp -R assets/remotion-starter my-paper-video
cd my-paper-video
npm install
python ../../scripts/validate_project.py script.json public
npm run start
npm run render
```

The manifest separates content from rendering behavior:

```json
{
  "composition": {"width": 1080, "height": 608, "fps": 30},
  "scenes": [{
    "id": "opening",
    "durationInFrames": 180,
    "background": "assets/plates/opening.png",
    "caption": {"title": "Your story", "subtitle": "Your visual hierarchy"},
    "layers": [{"src": "assets/layers/hero.png", "role": "primary", "x": 360, "y": 70, "width": 420, "delay": 12, "z": 5, "from": "bottom"}]
  }]
}
```

## Tang Dynasty example

The repository includes an actual 30-second Tang Dynasty court sample. It is an application of the workflow—not part of the Skill's required style.

[Watch the MP4](examples/tang-dynasty/preview/tang-paper-collage-30s.mp4)

| Establishing shot | Tribute close-up |
| --- | --- |
| ![Tang Dynasty establishing shot](examples/tang-dynasty/preview/wide.png) | ![Tang Dynasty tribute close-up](examples/tang-dynasty/preview/close.png) |

The example also includes the transparent PNG layers and background plates under `examples/tang-dynasty/assets/`, so its visual hierarchy can be inspected or adapted.

## Example applications

Use the same workflow for historical explainers, product stories, city evolution videos, relationship diagrams, educational explainers, or brand narratives. A Tang Dynasty court is only one example; the workflow is subject-agnostic.

## License

MIT. See [LICENSE](LICENSE).
