---
name: paper-collage-remotion
description: Create, revise, or render layered paper-cutout / collage animations in Remotion. Use for videos where backgrounds, characters, props, and foreground decorations need to be independent PNG layers with staged entrances, parallax, cut-paper outlines, occlusion, captions, narration, and audio effects; especially historical explainers, knowledge videos, brand stories, and city or character narratives.
---

# Paper Collage Remotion

Build depth from independently movable layers, not by applying camera motion to a single flattened illustration. Use Imagegen or another image model only for source assets; use Remotion as the timing, compositing, and rendering system.

For a new project, copy `assets/remotion-starter/` into the project root. Fill `script.json`, add public assets at the declared paths, and run `scripts/validate_project.py script.json public` before opening Remotion Studio. Use `examples/tang-dynasty/` only as a concrete visual reference, never as a required subject or style.

## 1. Establish the edit before generating assets

Turn the script into a shot list. For every shot, record: narrative beat, duration, focal subject, viewpoint, subject order, layer list, and caption/audio cue. Design around one dominant subject per shot.

Use this depth order unless the shot has a deliberate exception:

1. background plate: paper texture, landscape, architecture
2. distant layer: remote figures and small environment details
3. middle layer: supporting characters and props
4. primary layer: story-critical person or object
5. foreground layer: kneeling figures, petals, tape, torn-paper edges
6. captions and graphic accents

Do not put a main character into the background plate. Generate each character/prop as a complete, standalone layer; keep head, hands, feet, and held props inside the canvas.

## 2. Specify and prepare assets

Generate background plates without people. For each cutout, request a solid chroma background, a defined facing direction, no text/watermark/shadow, and a light paper outline. Prefer a source sheet only when it improves character consistency.

For a green-screen source, remove green before splitting. Tune tolerance against the actual source and inspect hair, sleeves, and thin props:

```bash
python "$CODEX_HOME/skills/paper-collage-remotion/scripts/key_to_alpha.py" \
  public/assets/source/close-six-green.png public/assets/source/close-six-alpha.png --tolerance 92
```

Then split the transparent sheet:

```bash
python "$CODEX_HOME/skills/paper-collage-remotion/scripts/split_sheet.py" \
  public/assets/source/close-six-alpha.png public/assets/layers close 6
```

It supports either `--columns` or `--rows` for non-square grids, `--padding` for a shared gutter, and `--no-trim` when every cell must retain the same dimensions. Inspect several outputs for clipped limbs and non-transparent backgrounds before animating.

Use an asset manifest in the project rather than scattering raw paths:

```ts
type LayerRole = "primary" | "secondary" | "tertiary" | "foreground";
type Layer = {src: string; role: LayerRole; x: number; y: number; width: number; delay: number; z: number};
```

Use the starter's `script.json` as the manifest. Keep all scene duration, copy, background paths, and layer values in that file; use code only for reusable rendering behavior. This makes the same animation system usable across subjects.

## 3. Compose a still first

Place all layers at their final positions without entrances. Make the primary subject visibly largest; decrease size, contrast, and motion with narrative importance. Verify that feet share a plausible ground line, faces and props remain unobscured, and foreground objects create intentional overlap.

Give cutouts a consistent outline and elevation shadow:

```tsx
filter: "drop-shadow(4px 0 #f5eedc) drop-shadow(-4px 0 #f5eedc) drop-shadow(0 4px #f5eedc) drop-shadow(0 18px 9px rgba(20,15,12,.32))"
```

Reference all public assets through `staticFile()` and render images with Remotion's `Img` component. Keep all movement frame-driven with `useCurrentFrame()` and `interpolate()`; do not use CSS transitions or keyframe animations.

Ensure the project entry file calls `registerRoot(RemotionRoot)`; pass that entry file (commonly `src/index.ts`) to the Remotion CLI, rather than a component file.

## 4. Animate by depth and narrative role

Stage the build: primary first, then supporting characters, then distant/foreground details. Offset every entrance; avoid a full cast appearing on the same frame. Use `Sequence from={delay}` for audio/entrance coordination.

Start from these visual ranges at 30 fps and tune to the shot, not to an arbitrary formula:

| Role | Entrance travel | Rise | Start scale |
| --- | ---: | ---: | ---: |
| primary | 78 px | 55 px | 0.86 |
| secondary | 58 px | 38 px | 0.90 |
| tertiary | 38 px | 22 px | 0.95 |
| foreground | 50 px | 30 px | 0.92 |

Use eased interpolation for an entrance and a small continuous bob after landing. Keep background drift and push-in near 1%; foreground may move slightly faster than the subject to make parallax readable. Keep positional values inline in the relevant `style` block when Studio editability matters.

```tsx
const local = frame - layer.delay;
const roleMotion = {
  primary: {distance: 78, rise: 55, startScale: 0.86},
  secondary: {distance: 58, rise: 38, startScale: 0.90},
  tertiary: {distance: 38, rise: 22, startScale: 0.95},
  foreground: {distance: 50, rise: 30, startScale: 0.92},
};
const enter = interpolate(local, [0, 14], [0, 1], {
  easing: Easing.bezier(0.16, 1, 0.3, 1),
  extrapolateLeft: "clamp", extrapolateRight: "clamp",
});
const travel = roleMotion[layer.role].distance;
const bob = local > 14 ? Math.sin((local - 14) / 11) * 3 : 0;

<Img src={staticFile(layer.src)} style={{
  position: "absolute", left: layer.x, top: layer.y, width: layer.width, zIndex: layer.z,
  opacity: enter,
  translate: `${(1 - enter) * travel}px ${roleMotion[layer.role].rise * (1 - enter) + bob}px`,
  scale: interpolate(enter, [0, 1], [roleMotion[layer.role].startScale, 1]),
  filter: paperCutoutFilter,
}} />
```

## 5. Add audio and captions after picture timing works

Let narration duration set each scene duration. Use one caption track at the bottom; keep it away from feet and key props. Mix music below narration. Align impact sounds with primary entrances, whooshes with secondary entrances, and light ticks/pops with tertiary details. Use `Audio` from `@remotion/media` and `staticFile()` for local audio.

## 6. Preview and accept

Use Remotion Studio for timing and a still render for a fast layout check. Render the MP4 only after reviewing static composition and entrances.

```bash
npx remotion studio
npx remotion still <composition-id> --frame=150 --scale=0.25
npx remotion render <composition-id> out/final.mp4
ffprobe -v error -show_streams -show_format out/final.mp4
ffmpeg -ss 5 -i out/final.mp4 -frames:v 1 check-05.png
```

Check: no cut limbs; correct facing directions; clear size hierarchy; correct z-order; staggered entrances; captions unobstructed; sound onset on its intended frame; audio stream, dimensions, and duration valid.

## 7. Validate mechanically before review

Run the bundled validator before rendering. It checks the scene schema, asset paths, PNG alpha channels, layer bounds, required role motion, and expected duration.

```bash
python "$CODEX_HOME/skills/paper-collage-remotion/scripts/validate_project.py" script.json public
```

Treat warnings as review items: an intentional off-screen entrance is fine; a final position outside the frame, missing alpha, or absent asset is not.
