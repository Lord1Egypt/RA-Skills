---
name: image-to-3d-asset
description: >
  Turn a photo or a text prompt into a real 3D model: a textured mesh you can
  drop into a game engine, AR scene, or product viewer. Use when the user says
  "make this into a 3D model", "turn this photo into 3D", "I need a GLB", "a
  game-ready asset", "3D-print this", "text to 3D", or wants a mesh with real
  topology and PBR materials, not a render or a turntable video.
---

# Image-to-3D asset

Produce a real 3D model from a single photo, a few photos, or a text description: a mesh with usable topology and PBR materials, returned as a **GLB file** that loads straight into a game engine, an AR scene, or a web viewer. The lever is a clean input (image-to-3D for fidelity, text-to-3D for invention) plus the topology and budget settings that match where the asset will be used.

## Inputs to collect

- **The reference image(s)** if the user has them. One clean shot is enough, and up to four or five views of the *same* object improve fidelity. (Ask only if none provided and no prompt either.)
- **Or a text description** of the object when no reference exists: what it is, its shape, and what it's made of.
- **Where the asset is used:** game/real-time, AR, hero render, product viewer, or 3D print. This drives topology, polygon budget, and texture resolution.
- **Will it be rigged or animated?** Decides quad vs raw topology and whether to force a T/A pose.

## Models

- **Default: Rodin Gen-2** (`hyper3d:rodin@gen-2`). Production-ready meshes, the richest control surface (mesh mode, polygon budget, HighPack 4K, T/A pose, PBR vs baked). Best general pick.
- **Cheaper/faster alt: Meshy-6** (`meshy:meshy@6`). Clean geometry, low-poly and symmetry control, image-enhancement toggle. Good for volume and game assets.
- **Other strong picks: Hunyuan 3D 3.1 Pro** (`tencent:hunyuan-3d@3.1-pro`) and **Tripo 3D v3.1** (`tripo:v3.1@0`). Both do image-to-3D and text-to-3D, with Tripo the lowest-cost tier.
- Confirm the live model + its schema via `runware-models` + `runware-run` before calling. Control fields differ per model, so never copy one model's `settings` onto another without checking.

## Workflow

1. Resolve the model schema (`runware-run`) and confirm the input field, the `settings` it allows, and that the model is `live`.
2. Provide the input. Image-to-3D goes under `inputs.images` (URL, base64, data URI, or a UUID from a prior task or the Image Upload API). Text-to-3D goes under `positivePrompt`. A request runs in **one mode at a time**.
3. Run **`taskType: "3dInference"` asynchronously.** 3D generation takes time, so the call returns a `taskUUID`. Poll `getResponse` until it reports terminal. Do not block a single sync call on it.
4. Read the result at **`outputs.files[].url`**, which is the GLB. Download it or hand the URL to a viewer.
5. Review the mesh (see Quality bar). If topology or budget is wrong for the target, adjust `settings` and rerun, don't post-process blindly.

## Technique

- **Image-to-3D for fidelity, text-to-3D for invention.** When a reference exists, use it: it anchors the silhouette and surface to something concrete and the result is predictable. Reach for text-to-3D only for shapes you can describe but can't photograph.
- **Isolate the subject.** A clean reconstruction needs **one object, evenly lit, on a plain background**. Busy backgrounds or a second item in frame split the model's attention and the mesh comes back soft. Crop tight before sending.
- **Lead multi-view sets with your best angle.** Up to five images (Rodin) or four (Meshy) of the same object help, and the **first image seeds the materials**, so put the most representative, best-lit view first. Keep every view to the same subject, a turnaround, not a mix of objects.
- **2D art works too.** Image-to-3D reconstructs from a flat illustration or concept art, giving the character a back it never showed. Simple, clearly-outlined art reconstructs more cleanly than busy or heavily-shaded drawings.
- **Prompt for form, not photography.** In text-to-3D, name the object, its overall shape, its style, and what it's made of. Skip the camera and lighting language that belongs in an image prompt, because you light and frame the mesh yourself. The more the asset matters, the more the prompt should say, a bare `"a chair"` is invented from scratch.
- **Topology follows the downstream job.** Quad-dominant topology deforms cleanly when rigged and subdivides for smoothing, so it's the default for anything that moves. Raw/triangulated is denser and more irregular, suited to static hero props or meshes you'll retopologize yourself.
- **Match the budget to where the asset is seen.** Faceted low-poly is right for background props and mobile, while smooth high-poly earns its weight on hero and close-up assets. See `runware-prompting` for writing the text-to-3D prompt itself.

Fill in this brief before building the request, then map each line to `settings`. `quality` and `polyCount` are mutually exclusive, so pick one.

```
Object:    <what it is>
Source:    <image (inputs.images) | text (positivePrompt)>
Mesh mode: <Quad (rig/animate) | Raw (static/retopo)>
Budget:    <quality preset (high/medium/low/extra-low) | polyCount (one or the other, never both)>
Materials: <PBR (relights in engine) | baked (Shaded) | both (All)>
```

Load `references/examples.md` for three worked recipes (photo-to-product, text-to-shape, low-poly game asset) with full requests and the GLB result shape.

## Parameters that matter

- `inputs.images` is the image-to-3D input. Rodin accepts up to **5**, Meshy up to **4**. First image seeds materials.
- `positivePrompt` is the text-to-3D input. Meshy caps it at **600 characters**. Mutually exclusive with `inputs.images`.
- **Rodin `settings.meshMode`**: `Quad` (default, rig/animate, subdivides cleanly) vs `Raw` (static/retopo, denser triangulated detail). Raw mode clears add-ons.
- **Rodin `settings.quality` XOR `settings.polyCount`** are *mutually exclusive*, and sending both is a validation error. Presets `high`/`medium`/`low`/`extra-low` map to fixed face counts that depend on mesh mode. Use `polyCount` for a hard engine budget (Quad 1,000 to 200,000, Raw 500 to 1,000,000).
- **Rodin `settings.addons: ["HighPack"]`** gives ~16× face count and 4K textures (vs default 2K), Quad only, roughly triples cost. Reserve for hero assets and close-ups.
- **Rodin `settings.taPose: true`** forces a neutral T/A pose for humanoids you'll rig. No effect on props or creatures.
- **Rodin `settings.material`**: `PBR` (default, relights correctly in engines) vs `Shaded` (lighting baked into the texture, for viewers that won't relight) vs `All` (both). `settings.hdTexture` raises texture quality independently.
- **Rodin `settings.useOriginalAlpha: true`** uses a cutout's alpha as the silhouette instead of edge detection. Image input only.
- **Rodin `settings.boundingBox: [Y, Z, X]`** caps max dimensions so a set of props shares scale.
- **Meshy `settings.imageEnhancement: false`** skips the photo cleanup pass for already-polished renders or stylized assets, so the model works from your image untouched. No effect in text-to-3D.
- `seed` fixes a result to reproduce or deliberately vary it (Rodin: 0 to 65535). Confirm exact field names and ranges against the live schema (`runware-run`), never guess.

## Quality bar

- The result is a valid **GLB** at `outputs.files[].url`, with the mesh and PBR materials packed together, that loads in your target engine/viewer.
- The silhouette and surface match the reference (image-to-3D) or the described form (text-to-3D), with no melted or lumpy approximation.
- Topology fits the downstream job: Quad if it will be rigged or animated, Raw only for static or retopo-bound assets.
- Polygon budget suits where the asset is seen: low-poly for background/mobile, high-poly or HighPack only where close inspection earns it.
- `quality` and `polyCount` were not sent together. For rigged characters, a T/A pose was used.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `product-photography` (clean single-object reference shots that reconstruct well, or the same product across stills).
