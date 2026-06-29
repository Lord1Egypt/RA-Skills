# Sprite Animation Layering

Use this reference when the user asks for animation sprites, modular outfits, hair/equipment layers, engine-ready sprite sheets, frame-grid cleanup, pivots/origins, hitboxes, or reusable character customization.

## Core Principle

Do not treat an animated game sprite as one prompt. Build a stable base motion first, then attach, remove, or regenerate layers against that locked motion contract.

The production contract matters more than any single frame:

- Same canvas size for every frame and layer.
- Same frame count and frame order for every layer.
- Same direction/action ordering across base, outfit, hair, weapon, shadow, and VFX layers.
- Same pivot/origin across all exported frames.
- Transparent background unless the user explicitly wants a baked background.
- No per-frame cropping after generation unless the same crop is applied to every layer.

## Domain Glossary

- Base body layer: neutral body animation used as the timing, silhouette, and pivot source.
- Outfit layer: clothing or armor pixels that composite over the base body.
- Equipment layer: held or worn items such as weapon, shield, backpack, or tool.
- Hair/head/face layer: optional customization pixels that should stay locked to the head motion.
- Shadow layer: ground shadow, often under every character layer.
- VFX layer: non-body effects such as slash arcs, magic, impact flashes, dust, or glow.
- Mask: white/black image or selected region that limits edits or inpainting.
- State: a posed version of the same character used as a better first frame before animation.
- Action: the motion description, such as walk loop, idle breathing, slash attack, or jump.
- Direction: the facing direction for a frame row or animation set.
- Frame grid: the fixed sequence of frame slots in a sprite sheet or exported frame folder.
- Pivot/origin: the point the game engine uses to place and align a sprite frame.
- Draw order: the render stack, such as shadow, base body, outfit, hair, equipment, VFX.
- Atlas/sprite sheet: packed image containing multiple frames.
- Hitbox/hurtbox: gameplay collision rectangles, not visual art; keep them tied to frame slots.

## Decision Tree

Use the workflow that preserves the most existing truth:

| Need | PixelLab route | Notes |
|---|---|---|
| New motion from a still character | `/v2/create-character-state` then `/v2/animate-with-text-v3` | Pose first when the original is stiff, then animate from the state. |
| More frames between key poses | `/v2/interpolation-v2` | Create readable key poses first, then interpolate in-betweens. |
| Outfit on a finished animation | `/v2/transfer-outfit-v2` | Apply a reference outfit to exact base animation frames. |
| Outfit-only layer after transfer | `/v2/edit-animation-v2` | Remove body/skin pixels while preserving the clothing motion and transparent canvas. |
| Cleanup across frames | `/v2/edit-animation-v2`, `/v2/inpaint`, or `/v2/inpaint-v3` | Use the smallest edit region that solves the problem. |
| Existing motion reused for a new design | PixelLab animation-to-animation UI/workflow, or verified current API route | Do not invent an API path if the route is not present in current docs. Verify first. |
| Held item or weapon | Sketch/position item on a duplicate frame, then inpaint/edit animation | Include the gripping hands/arms in the edit region. Text alone is usually too weak. |

## Modular Outfit Pipeline

1. Generate or choose a neutral base character with no hair/clothes when customization matters.
2. Create the complete base animation first, including all needed directions and actions.
3. Export or prepare the base frames with identical canvas size, transparent background, and frame naming.
4. Use `/v2/transfer-outfit-v2` with a reference outfit and the exact base animation frames.
5. Save the merged dressed animation as a quality-control artifact.
6. Use `/v2/edit-animation-v2` on the merged result to remove the character body and skin pixels, leaving only the outfit layer.
7. Check the outfit-only result against the base body by compositing the same frame indexes together.
8. Repeat for hair, armor, cape, held item, or accessories as separate layers when the game needs runtime swapping.
9. Export every layer with the same frame count, direction order, canvas size, and pivot/origin.

Use this prompt for the body-removal edit:

```text
Remove the character body and skin pixels. Leave only the outfit layer, preserving the exact clothing motion, frame alignment, transparent background, and empty pixels where the body was removed.
```

Use this transfer instruction when applying an outfit:

```text
Apply only the outfit to the character. Preserve pose, silhouette, frame timing, facing direction, canvas alignment, and transparent background.
```

## Frame-Grid Contract

Before generating layer variants, write the contract down in the payload notes or task notes:

```text
Character: hero
Action: walk
Direction order: south, west, east, north
Frames per direction: 8
Canvas: 64x64
Pivot/origin: bottom-center at x=32 y=56
Layers: shadow, base, outfit, hair, weapon, VFX
Background: transparent
Export: individual PNG frames and sheet atlas
```

Use stable frame names:

```text
hero/base/walk_south_00.png
hero/base/walk_south_01.png
hero/outfits/guard/walk_south_00.png
hero/outfits/guard/walk_south_01.png
hero/weapons/sword/walk_south_00.png
hero/weapons/sword/walk_south_01.png
```

Never approve a modular sprite pack if the layers have different sizes, different frame counts, shifted feet, or mismatched ordering. Those issues become game-engine bugs.

## State-First Animation

If the starting sprite is an idle pose and the desired action is active, create a state first:

```json
{
  "character_id": "REPLACE_WITH_CHARACTER_ID",
  "edit_description": "same character in a forward-running start pose, same palette and outfit, stable face, transparent background",
  "no_background": true,
  "use_color_palette_from_reference": true,
  "seed": 0
}
```

Then pass the state as the first frame for `/v2/animate-with-text-v3`:

```text
walk loop, stable face, consistent outfit, no camera movement, feet planted on a consistent ground line
```

Do a small cleanup pass if the face, mouth, hands, or weapon jitters. Copying a clean face or inpainting only the head region is often safer than regenerating the whole animation.

## Equipment And Weapons

For held items, make the model see the constraint:

1. Duplicate the best base frame.
2. Sketch the weapon/shield/tool in the exact target size, color, and hand position.
3. Mask the item plus the fingers, wrist, and arm segment that must grip it.
4. Prompt the full final sprite, including body, pose, outfit, item, and hand relationship.
5. Propagate through edit animation or animation reuse.
6. Export the item as its own layer only after the merged version aligns.

Use separate layers when gameplay needs independent rendering, hit detection, swaps, tinting, or VFX. Bake the item into the outfit only when it will never change.

## Interpolation And Frame Rate

Use interpolation to fill controlled gaps, not to discover the whole animation from scratch.

- First make key poses with clear extremes.
- Keep the same canvas, pivot, and silhouette scale for start/end images.
- Use `/v2/interpolation-v2` with a concise action.
- Review for duplicated frames, melted hands, unstable face, and foot sliding.
- Delete weak frames only if all layers keep the same final frame slots.

## QA Checklist

Before calling the sprite pack ready:

- Frame count matches across every layer.
- Frame order matches across every layer.
- Canvas size matches across every layer.
- Pivot/origin is documented and consistent.
- Background is transparent where expected.
- Outfit-only layer has no body/skin pixels.
- Hair/equipment layers do not include accidental body pixels unless intentionally baked.
- Feet and ground contact do not drift between layers.
- Face and hands stay stable across the loop.
- Palette, outline weight, and lighting match the base pack.
- No per-frame crop, scale, or offset was introduced.
- Sprite sheet export has matching row/column metadata for the engine.
- Runtime composite was tested by stacking at least a base frame plus each layer frame.
- Hitboxes/hurtboxes are tied to frame indexes and are not inferred from changing art bounds.

## Source Trail

PixelLab video transcripts that informed this workflow:

- `1EDq2xHQcJ8` - `https://www.youtube.com/watch?v=1EDq2xHQcJ8`: modular clothes workflow using a blank base character, transfer outfit to animation, then edit animation to leave clothing only.
- `OZWtWFBeGCA` - `https://www.youtube.com/watch?v=OZWtWFBeGCA`: create a character state before animating so motion starts from a useful pose.
- `Lx9r3TzoIWY` - `https://www.youtube.com/watch?v=Lx9r3TzoIWY`: frame count and export guidance for character animation, including keeping the best frames.
- `y-RL3FgiEhg` - `https://www.youtube.com/watch?v=y-RL3FgiEhg`: animation-to-animation workflow preserves an existing motion structure while applying a new character design.
- `qOhMp_X_gbU` - `https://www.youtube.com/watch?v=qOhMp_X_gbU`: generate key poses first, then interpolate between them to increase frame rate.
- `XF3VEbLnWCw` - `https://www.youtube.com/watch?v=XF3VEbLnWCw`: transfer outfit, edit animation, inpaint cleanup, then export the sprite sheet.
- `PTGZU6w6J8E` - `https://www.youtube.com/watch?v=PTGZU6w6J8E`: reuse existing animations and rotations with new sprite variations frame-for-frame.
- `w_E_kbCXRn4` - `https://www.youtube.com/watch?v=w_E_kbCXRn4`: template animation, init-image motion guidance, and layer/selection care during cleanup.
