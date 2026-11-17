# Image-to-3D asset: worked recipes

Three end-to-end recipes. Each shows the scenario, the async `3dInference` request, and the GLB result shape. Confirm the AIR is `live` and the field names against the live schema (`runware-run`) before sending. Run async: the request returns a `taskUUID`, then poll `getResponse` until terminal. The finished GLB is at `outputs.files[].url`.

All AIRs below are verified `live` against the Runware catalog: `hyper3d:rodin@gen-2` (Rodin Gen-2), `meshy:meshy@6` (Meshy-6).

## 1. Photo to rig-ready product asset (Rodin Gen-2)

Scenario: a clean studio photo of a glazed ceramic owl figurine. The client wants a 3D version they can drop into an engine and later rig, so the topology has to deform cleanly. Use image-to-3D for fidelity, `Quad` mesh mode for clean edge loops, and PBR materials so it relights in the engine.

The photo goes in `inputs.images`. The first image seeds the materials, so lead with the best-lit view. Set `meshMode: "Quad"` (the rig-ready default) and a `quality` preset for a rough target. Keep `material: "PBR"` so base color, metallic, roughness, and normal maps come back ready to light.

```json
[
  {
    "taskType": "3dInference",
    "taskUUID": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "model": "hyper3d:rodin@gen-2",
    "inputs": {
      "images": ["https://example.com/owl-front.jpg"]
    },
    "settings": {
      "meshMode": "Quad",
      "quality": "medium",
      "material": "PBR"
    }
  }
]
```

Result:

```json
{
  "data": [
    {
      "taskType": "3dInference",
      "taskUUID": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "outputs": {
        "files": [
          {
            "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "url": "https://im.runware.ai/image/os/a14d18/ws/2/ii/a1b2c3d4-e5f6-7890-abcd-ef1234567890.glb"
          }
        ]
      }
    }
  ]
}
```

Why it works: a single isolated, evenly-lit subject gives the model an unambiguous read on shape and surface, so the mesh comes back crisp instead of melted. `Quad` topology flows in clean loops that deform predictably once rigged. `quality: "medium"` maps to 18,000 Quad faces, enough surface for a product viewer without HighPack weight. To turn the figurine into a humanoid character you will skin, add `settings.taPose: true` to force a neutral T/A pose. For a hero close-up, swap to `addons: ["HighPack"]` (Quad only, roughly triples cost). If you have up to five turnaround views of the same owl, pass them all in `inputs.images` with the best angle first.

## 2. Text to 3D shape, no reference (Rodin Gen-2)

Scenario: the client is concepting a sci-fi blaster prop that does not exist yet, so there is nothing to photograph. Use text-to-3D for invention. Prompt for form and material, not camera or lighting. This is a static hero prop, so use `Raw` mode for denser triangulated detail and a high `quality` preset.

The description goes in `positivePrompt` and is mutually exclusive with `inputs.images`. Name the object, its shape, its material, and its style. `meshMode: "Raw"` clears add-ons, so HighPack has no effect here. `Raw` `high` maps to 500,000 faces.

```json
[
  {
    "taskType": "3dInference",
    "taskUUID": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "model": "hyper3d:rodin@gen-2",
    "positivePrompt": "A sci-fi blaster pistol, sleek angular hard-surface design, gunmetal body with a glowing cyan energy cell along the top, chunky grip and trigger guard, game prop",
    "settings": {
      "meshMode": "Raw",
      "quality": "high",
      "material": "PBR"
    }
  }
]
```

Result:

```json
{
  "data": [
    {
      "taskType": "3dInference",
      "taskUUID": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
      "outputs": {
        "files": [
          {
            "uuid": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
            "url": "https://im.runware.ai/image/os/a14d18/ws/2/ii/b2c3d4e5-f6a7-8901-bcde-f23456789012.glb"
          }
        ]
      }
    }
  ]
}
```

Why it works: the prompt leads with the object, then layers shape and material, which is what shapes a mesh. It skips the camera and lighting language that would belong in an image prompt, because you frame and light the model yourself. `Raw` gives the dense, irregular detail a static hero prop wants and that you can retopologize yourself later. The more the asset matters, the more the prompt should say. A bare `"a blaster"` is invented from scratch. Set a `seed` (0 to 65535) to reproduce or deliberately vary a result you like.

## 3. Game-ready low-poly variant (Meshy-6)

Scenario: a background prop for a mobile game with a hard engine budget. The client needs a textured asset that stays under a tight triangle ceiling. Route to Meshy-6 for low-poly control and use `meshType: "lowpoly"`. Image-to-3D from a clean reference keeps it anchored.

The photo goes in `inputs.images` (Meshy accepts up to 4). Set `meshType: "lowpoly"` for a faceted game-asset look. Set `imageEnhancement: false` if the input is an already-polished render so the model works from it untouched. Note: in `lowpoly` mode Meshy ignores `polyCount`, `topology`, `decimation`, and `remesh`, so use `polyCount` only on a `standard` mesh.

```json
[
  {
    "taskType": "3dInference",
    "taskUUID": "c4278a91-6c18-494d-a0d9-a4359dcbd783",
    "model": "meshy:meshy@6",
    "inputs": {
      "images": ["https://example.com/crate.jpg"]
    },
    "settings": {
      "meshType": "lowpoly",
      "imageEnhancement": false,
      "pbr": true
    }
  }
]
```

Result:

```json
{
  "data": [
    {
      "taskType": "3dInference",
      "taskUUID": "c4278a91-6c18-494d-a0d9-a4359dcbd783",
      "outputs": {
        "files": [
          {
            "uuid": "d3e4f5a6-b7c8-9012-cdef-345678901234",
            "url": "https://im.runware.ai/image/os/a14d18/ws/2/ii/d3e4f5a6-b7c8-9012-cdef-345678901234.glb"
          }
        ]
      }
    }
  ]
}
```

Why it works: `lowpoly` gives the faceted, lightweight mesh a background prop and a mobile budget want, where nobody inspects the surface up close. `pbr: true` adds the metallic, roughness, and normal maps the engine relights with. `imageEnhancement: false` keeps a polished render faithful instead of repainting detail you meant to keep. For a hard triangle ceiling instead of a preset, drop `meshType` to its `standard` default and set `polyCount` directly (100 to 300,000). For a riggable character, add `settings.pose: "t-pose"` and `settings.topology: "quad"`.
