# Prompt Cheatsheet

Use PixelLab terminology and workflow hints rather than generic image-prompt filler.

## General Scenes

- `top-down cave room with stairs and treasure chest, pixel art, medium detail`
- `small forest shrine, mossy stones, soft torch light, high top-down, 32-bit game style`
- `cozy potion shop interior, shelves of bottles, warm colors, pixel art`

For maps, describe what appears in the middle of the selected area. Preserve overlap/reference context when extending a map.

For large backgrounds, choose the game aspect ratio before generating. If needed, create a larger scene, then crop or fit it in-engine after the art direction is established.

For canvas-extension workflows, make a backup first. When resizing/extending a canvas, keep `Trim content outside the canvas` unchecked unless the user explicitly wants off-canvas content deleted.

## Characters

- `cute wizard, blue robe, staff, high top-down, south-facing`
- `small slime, glossy green body, simple face, side view`
- `armored knight with red plume, facing right, in profile`

Before writing a final PixelLab prompt for a named character, turn the user's rough idea into a visual brief. The user does not need to know the categories. The agent should infer ordinary defaults and ask at most three questions only for identity-critical gaps.

Use this brief shape:

```text
Name/role: who this is in the game.
Game use: playable hero, companion, enemy, NPC, pickup, portrait, etc.
Body: proportions, creature type, age/read, silhouette.
Face/expression: visible personality cues.
Clothing/materials: outfit, armor, shell, fur, metal, cloth, colors.
Pose/camera: side-view, low top-down, high top-down, facing language.
Accessories/signature features: one to three must-keep traits.
Palette/style: era, outline, shading, detail level, background handling.
Do not include: traits that would make the identity wrong.
Approval criteria: what seed candidates must get right.
```

Only after that, convert the brief into labeled prompt blocks and generate seed candidates. If the first seed candidates miss the identity, fix the brief before generating a pack.

For character generation, prefer labeled prompt blocks over one flat sentence. Use categories as drawing commands:

```text
Body: tall and lean robed warrior with a calm commanding presence.
Clothing: layered brown and muted gray robes with a pale waist sash.
Expression: thoughtful and measured.
Pose: standing upright, one hand relaxed, one hand holding a glowing blue blade.
Accessories: simple belt, soft boots, no helmet.
Aura: disciplined, restrained, heroic.
```

Add or remove categories to fit the asset: `Body`, `Clothing`, `Expression`, `Pose`, `Accessories`, `Weapon`, `Aura`, `Palette`, `Material`, and `Silhouette`. The point is precision: each category gives the model a separate feature to draw.

For direction-sensitive requests, use endpoint controls only when that endpoint supports them, and always include explicit prompt language like `facing right`, `in profile`, `north-facing`, or `high top-down`.

Camera view changes the character read even when the prompt and direction stay similar. For `/v2/create-character-v3`, use `side`, `low top-down`, or `high top-down`; do not send a separate `direction` field. Put facing language such as `facing east in profile` or `south-facing` inside the prompt, or choose a 4/8-direction endpoint when a direction pack matters.

When starting a character, draw a crude init image first to lock scale, stance, and rough proportions. Keep the text prompt simple, but spell out important colors for each part: face, hands, robe, belt, boots, trim, weapon, and similar elements. If the first result is close, reuse it as the next init image and run the same settings again.

For non-human humanoids, generate a human baseline first. Use it as style and init reference, lower init strength enough for the prompt to change species traits, and try joined terms such as `tigerman` before falling back to literal language like `human body with tiger head`.

For held equipment, do not rely on text alone. Duplicate the base frame, sketch the equipment in the correct size, position, and color, then inpaint the item plus the hands/arms that need to grip it. Prompt the full final character, not just the held object.

For character changes that must keep the same style, inpaint only the changing regions, reuse the original as a low-strength init image, and avoid masking the eyes when possible so the face stays anchored.

## Style Packs

- `treasure chest in the same style as my reference set`
- `three potion bottles sharing the same outline weight, palette, and highlight style`
- `enemy sprite matching the existing cute wizard reference, same camera angle`

Use the same seed, palette language, and reference images when the user wants controlled variants.

If using a style image, keep the new object's palette compatible with the reference or explicitly describe the palette shift. Increase style guidance for closer matching; lower it when the reference is only loose inspiration.

For a very specific small-sprite style, set the canvas to the target footprint, use a matching perspective style image, raise style guidance until the look holds, and keep the prompt simple but color/material-specific. Community examples used style guidance around `90-120` and init strength around `350-400` for tight style matching, but these are tuning starts, not defaults.

## UI

- `medieval stone button`
- `inventory slot with brass trim`
- `health bar, red fill, dark metal frame`
- `small pause menu panel, readable pixel-art border`

Keep UI prompts concrete: element type, material, color, border, and state.

## Tilesets And Isometric Tiles

- Top-down: `inner tile water, outer tile sand`
- Sidescroller: `lower_description: dirt platform`, `transition_description: grass top edge`
- Isometric: `rocky path`, `wooden floor`, `grass on top of dirt`
- Create Tiles Pro style: `grass to dirt transition`, `stone wall edge`, `water edge, square top-down, high top-down view`

Use the tileset-specific terms the endpoint expects instead of one broad scene prompt.

For maps, start with good base tiles, then prompt transitions and landmarks as inpainted local changes: `grass to beach transition`, `cave entrance`, `bench under tree`, `treasure chest in the corner`.

For Sprite Fusion, export the PixelLab tileset with `Export To Sprite Fusion`, import it into Sprite Fusion, then test the autotile layer before approving the pack.

For Create M-XL tileset starts, use a rough init blockout and feed each improved result back as the next init image. If the colors drift, choose reference swatches, use eyedropper plus Replace Color (`Shift+R`), then reuse the recolored image as the next init.

For side-scroller tiles, use the current endpoint language: `lower_description` for the main platform material and `transition_description` for the decorative/top edge. Simple terrain nouns such as `ground` can work better than over-specific labels when the model misunderstands the surface. Keep nearby good tiles visible during inpainting so the model can copy the edge logic.

## Animation

- `walking`
- `jumping`
- `attacking`
- `idle breathing`
- `casting a spell`

Start with fewer frames when identity consistency matters. Expand only after the reference motion is acceptable.

For stronger animation starts, create a state first: `same character, forward-running start pose`, then animate that state with `walk loop` or `attack slash`.

For frame-rate upgrades, create four key poses first, then interpolate empty frames between them.

For pose libraries, treat reference animation frames as skeleton/proportion guides. Resize or squash them to match the target character before using them as pose references.

To animate a variant character with the same motion, finish one character animation first. Generate the variant from the original character as init, then use the finished animation frames as init images for the variant. If the animation needs more than four frames, keep the same seed across every frame batch.

For cleaner init-image animation, start from a reference animation with similar size and motion, recolor reference-frame pieces toward the generated character, tune init/style balance, and manually repair tiny details such as eyes or helmet pixels when needed.

For top-down RPG walking sheets, build in sequence: style-locked character, rotations, then movement/simple movement. A common four-direction sheet uses three frames per direction; expect the movement step to need retries even if style and rotation are good.

### Layered Sprite Animation

Start from a neutral base body with transparent background when the final game needs modular clothes, armor, hair, weapons, or VFX. Generate or choose the base animation first, then treat every later layer as a child of that exact frame grid.

Lock the frame contract before generating layers: same canvas size, same frame count, same direction/action order, same pivot/origin, same transparent background, and no per-frame cropping. If the base sheet is 64x64 with 8 frames facing south, every outfit, hair, weapon, shadow, and VFX layer should be 64x64 with those same 8 frame slots.

For outfit swaps, use transfer outfit to apply a reference outfit to the finished base animation. The result is a merged dressed sprite. Then use edit animation with a prompt such as:

```text
Remove the character body and skin pixels. Leave only the outfit layer, preserving the exact clothing motion, frame alignment, transparent background, and empty pixels where the body was removed.
```

For state-driven animation, make a better starting pose first, then animate from that state. For example:

```text
same character in a forward-running start pose, same palette and outfit, stable face, transparent background
```

For equipment, do not rely on a text-only prompt. Sketch or place the weapon/shield in a duplicate frame, include the gripping hand/arm area, then use inpaint or edit animation to propagate the held item. Keep the prompt about the full final sprite, not just the item.

For frame-rate upgrades, create readable key poses first, then interpolate between them. Do not interpolate layers independently after the fact unless each layer still lands on the same frame slots as the base.

## Palette And Cleanup

- `reduce to existing 16-color palette`
- `keep outline weight and palette, fix only the face`
- `change only the boots, preserve the body and pose`

Use small inpaint regions and visible color/shape hints when placement matters.
