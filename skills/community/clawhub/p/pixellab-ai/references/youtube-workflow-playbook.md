# YouTube Workflow Playbook

This playbook distills the official PixelLab YouTube corpus into reusable agent behavior. It uses source links and timestamps, not transcript dumps. If a task depends on a screen-only setting, inspect the linked timestamp before turning it into a rule.

For community-tested recipes from the PixelLab Discord `#helpful-posts` list, also read `community-discord-workflows.md`. For the Discord `#tutorials` feed, channel-only tips, and external community tutorial links, read `community-discord-tutorials.md`.

## Coverage

- Channel inventory captured on 2026-06-20: 156 items from videos plus shorts.
- Transcript coverage: 53 transcript-API captions, 38 `yt-dlp` auto-caption transcripts, and 59 local Whisper fallback transcripts, 35,114 words analyzed.
- Remaining unresolved rows: 2 no-speech/no-caption rows, 1 caption-unavailable row, and 3 rows where English auto captions are listed but YouTube returned HTTP 429 during caption download. Every item is still indexed in `official-youtube-index.md` with an explicit status.
- Raw transcript and audit artifacts are intentionally kept outside this uploadable skill package.

## Default Asset Strategy

Do not treat PixelLab as one generic image generator. First classify the request:

1. New standalone image or sprite.
2. Existing image cleanup, resize, inpaint, or pixel-art conversion.
3. Consistent asset family.
4. Character/object directions.
5. Animation/state generation.
6. Top-down map, side-scroller level, isometric tile, or UI pack.
7. Export into an engine such as Godot.

If the user asks for a game-ready map or level, build a workflow: tileset, map layout, props/objects, characters, edits, export. Do not try to make the full game area as one flat prompt.

For agent-driven game work, keep the asset plan and code-import plan separate. Generate or fetch the PixelLab asset, save it to a project asset folder, then wire the resulting sprite sheet, map, state, or animation in the engine code.

For PixelLab MCP or Godot tutorial workflows, translate the agent step to the current environment. Do not assume Claude Code is available; Codex/OpenClaw can follow the same split between asset generation, saved outputs, engine import, and code wiring.

## General Image Generation

Choose the general image tool by target use:

- Use larger/general image generation for backgrounds, large scenes, visual-novel backdrops, and broad compositions.
- Use more pixel-focused image routes or character/object routes for sprites that need crisp pixel constraints, directions, or later animation.
- Use low init-image strength when a sketch or blob is only a loose composition guide; increase it when the shape or placement must remain recognizable.
- If a character faces the wrong way, adjust both the explicit direction/view language and the endpoint's guidance controls instead of only retrying the same prompt.
- For large backgrounds, keep the final game aspect ratio in mind early. If the endpoint has a square-ish size cap, design within a larger canvas or stretched aspect workflow, then crop/fit in-engine deliberately.
- For canvas extension beyond the normal small square workflow, back up the image first. Keep `Trim content outside the canvas` unchecked when resizing/extending unless deleting outside content is intentional.

## Tilesets

Use tileset-specific language instead of scene prompts.

- Top-down tilesets: define terrain relationships such as inner/outer terrain, for example water versus sand or grass versus path. Relevant sources: [Generating pixel art tilesets](https://www.youtube.com/watch?v=q9z2Vhpz-Z8&t=630s), [Make Maps 10x Faster with AI Tilesets](https://www.youtube.com/watch?v=O9maOTbLuHQ&t=30s).
- Side-scroller tilesets: separate center/body tile material from top/surface material. Relevant sources: [Full Side Scroller Level](https://www.youtube.com/watch?v=84yChPoOaew&t=90s), [Side-scroller map and tilesets](https://www.youtube.com/watch?v=H-dPJKmKr1E&t=0s).
- High top-down tilesets are structured specs: tile size, lower terrain, upper terrain, transition amount, outline/shading/detail, adherence controls, palette, and output method. This was confirmed by visual review of the official high top-down tile UI.
- Side-scroller tilesets use their own structured form. In the current API, use `lower_description` for the main platform material and optional `transition_description` for the top/decorative edge, plus target image/style controls, target palette, and output method when available.
- When a side-scroller terrain prompt fails, simplify the terrain noun before adding more style words. Community tutorial text specifically called out replacing an over-specific description such as `ice floor` with a clearer material like `ground`, while keeping visible context so the model can infer the missing edge.
- Create Tiles Pro supports multiple tile families such as isometric, flat-top hex, pointy-top hex, octagonal, and square top-down. Use it when the user needs tile type, tile size, view angle, depth, or up to 16 style tiles as consistency references.
- Inspect transitions, not only individual tile beauty. Bad edge transitions make the set unusable even when each tile looks good.
- Generate alternates, choose the most readable set, then edit/inpaint specific bad transitions instead of regenerating the whole pack.
- Test candidate tiles in an auto-tile or map preview before calling the tileset usable. A beautiful generated tile can still fail at map edges.
- For export, preserve the tileset format and engine expectations; see [Export PixelLab Map to Godot](https://www.youtube.com/watch?v=br2EO65qHAU&t=0s).
- For Sprite Fusion, use PixelLab's `Export To Sprite Fusion` output and import it into Sprite Fusion by drag-and-drop or `Import tileset`, then test the resulting autotile layer.
- For Create M-XL tileset starts, use a rough init blockout, increase init strength, and feed improved generations back as init images. If colors drift, recolor with eyedropper plus Replace Color (`Shift+R`), where the secondary color is the target to apply and the primary color is the color being replaced.

Endpoint bias:

- Use `/v2/create-tileset` for top-down inner/outer terrain.
- Use `/v2/create-tileset-sidescroller` for platformer terrain; current payloads use `lower_description` and optional `transition_description`.
- Use `/v2/create-isometric-tile` for a single isometric tile before building a map.
- Use `/v2/map-objects` or object workflows for props that should sit on a map.

## Maps

Maps are iterative compositions.

- Build or choose the base terrain first, then add objects, characters, entrances, props, and visual interest.
- For map-tile workflows, start with good base tiles. Existing tiles the user already likes should be used as inspiration because later transition and extension passes inherit that quality.
- Make terrain transitions deliberately: grass to beach, beach to water, road to beach, path to cave, and similar edge cases should be selected and inpainted as transitions, not added as isolated decorative tiles.
- Keep useful surrounding context visible when editing or extending a map. PixelLab performs better when it can see adjacent good tiles, but the active change should still be in or near the center of the selected region.
- Use larger selections when duplicating/extending terrain so the model can see context; return to smaller selections for precise objects such as trees, benches, cave openings, treasure chests, or tile-edge repairs.
- The older map-tile workflow was described as strongest around 16x16 tiles. Treat larger/custom sizes as context tools, not as a reason to skip tile testing.
- For interiors, define the room purpose, floor/wall material, object placement, and top-down camera style. Relevant source: [Interior Maps for Top-Down Games](https://www.youtube.com/watch?v=qVDkp1baJkU&t=30s).
- When extending a map, preserve context at the edge. Avoid repainting the whole selected area unless the user wants a full redesign.
- Describe the middle of the selected area clearly. The model needs to know what should appear in the active generation region.
- For side-scroller levels, create terrain tiles and background layers separately, then combine and extend. Relevant sources: [Full Side-Scroller Asset Pack](https://www.youtube.com/watch?v=o8AZRTx36DE&t=330s), [Side-scroller map and tilesets](https://www.youtube.com/watch?v=H-dPJKmKr1E&t=510s).
- For infinitely tiling side-scroller backgrounds or parallax layers, extend the canvas from an approved background and preserve overlap context. Do not regenerate a full background if only the repeat seam or edge continuation is wrong.
- In Map Workshop, a full map can start from two described tiles or two uploaded single tiles, then auto-connect while drawing. Use built-in object placement and inpainting for layout details, then use inpaint v3 for final landmarks or personality details.
- Keep generation, tile testing, map assembly, and engine export as separate phases. Do not collapse them into one "make a map" API call.

## UI

UI must match the game world, not just exist.

- Generate UI as a pack: menu panel, health bar, inventory slot, button states, icons, and frames should share material, palette, outline thickness, and lighting.
- Use a concept image or style reference when the UI must match an existing environment. The UI tool exposes a concept-image slot, description, optional color palette, output method, and remove-background option.
- Prompt with concrete material and function: `wood and gold pause menu`, `stone inventory slot`, `red health bar with brass frame`.
- Avoid default empty boxes. If the result is generic, add world nouns, material, palette, border treatment, and game theme.
- Relevant source: [Easiest way to create pixel art UI](https://www.youtube.com/watch?v=OdRIHQ4ar2c&t=60s).

Endpoint bias:

- Use `/v2/generate-ui-v2` for UI elements and packs.
- Use style/reference routes when UI must match an existing game scene.

## Style Consistency

Consistency is a workflow, not a single prompt adjective.

- Reuse style references, seed strategy, resolution, outline weight, color palette, detail density, and camera angle.
- When creating families, start with a small approved reference set, then generate related characters/items against that set.
- Style-image generation tends to borrow colors from the reference. It works best when the requested object or character can plausibly share the reference palette; otherwise specify the palette change directly.
- Increase style guidance when matching the reference is more important than variety. Lower it when the reference is only loose inspiration.
- For a cast of related side-scroller characters, generate one approved full-body character first, then use one or more style references to create variants before animating.
- For large same-style casts, use the latest character workflow as a repeatable pipeline: create one approved character, keep the same style references and sprite-sheet constraints, create variants, then add states and animations only after the style family is locked.
- Do not rely on broad labels like `GBA style` or `fantasy style` alone. Spell out outline, palette, proportions, rendering density, and view.
- For very small sprites or tightly constrained styles, set the canvas to the target sprite footprint, use a perspective-matched style image, and tune style/init weights upward until the style holds. Community examples used style guidance around `90-120` and init strength around `350-400` as starting ranges.
- Relevant sources: [Generate Consistent Pixel Art for Games](https://www.youtube.com/watch?v=nITrIQw1gag&t=0s), [Building a Cohesive Game Art Style](https://www.youtube.com/watch?v=7HTLYLo3tTQ), [Style consistent characters with inpainting](https://www.youtube.com/watch?v=68BYzLoLh-U).

Endpoint bias:

- Use `/v2/create-image-bitforge` or `/v2/generate-with-style-v2` when reference control matters.
- Use prompt enhancement before expensive generation when the style prompt is vague.

## Characters And Objects

Choose the durable asset unit before generating.

- For character prompts, use labeled feature blocks instead of a single vague sentence. Start with `Body`, `Clothing`, and `Expression`, then add `Pose`, `Accessories`, `Weapon`, `Aura`, `Palette`, or `Silhouette` when those traits matter. The goal is to give PixelLab precise drawing commands for each visible feature.
- Match prompt structure with plugin controls. `sidescroller (eye level)` produces a taller full-body read, while `high top-down (45-degree)` pushes toward compact top-down RPG proportions. Keep `Direction` explicit, such as `south (facing camera)`, and do not rely on prompt wording alone for camera/view control.
- For a new character, draw a rough init image first to lock scale and stance, then keep the text prompt simple while naming colors for each visible part. If the first result is close, use it as the next init image and rerun the same settings.
- For non-human humanoids, create a human baseline first and reuse it as style plus init reference. Lower init strength enough that the prompt can add species traits; try joined terms such as `tigerman` before literal fallbacks such as `human body with tiger head`.
- For held weapons or equipment, sketch the object into a duplicate base frame with the right size, position, and color. Inpaint the item plus the nearby hands/arms, and prompt the full finished sprite.
- For style-preserving character edits, mask only the changing trait, prompt the full target image, reuse the original as a low-strength init image, and avoid masking eyes unless they must change.
- Use character/object creator workflows when the user needs reusable states, directions, or animations later.
- Use object creator for packs, object states, and animation-ready props. Relevant source: [Object Creator](https://www.youtube.com/watch?v=Hhx9QZwYoZY).
- For interactable world props, keep the object identity stable and add states: normal/cracked/open/damaged, then animate between or from those states. This is better than generating unrelated one-off props.
- Use V3-style animation when the motion should stay subtle; try Pro-style animation when the prop needs a more dramatic effect such as crumbling or a chest opening.
- For animated objects or characters from scratch, use the text-driven animated object/character workflow when there is no base sprite. Describe subject, pose/material, motion, resistance/weight, particles, and end state, then export the sprite sheet.
- For top-down characters, choose camera/view early. Changing view later can break consistency.
- For families or crowds, use one style reference set and generate variants rather than unrelated one-off prompts.

Endpoint bias:

- Use `/v2/create-character-with-4-directions` or `/v2/create-character-with-8-directions` when direction packs matter.
- Use `/v2/create-character-state` and `/v2/objects/{object_id}/states` for later reusable state work.
- Use `/v2/create-1-direction-object` or `/v2/create-8-direction-object` for props and objects.

## Rotation

Rotation is stronger with visual reference and explicit facing language.

- Use init, concept, or style images when rotating an existing asset.
- Ask for the exact target direction, and include prompt language such as `facing east`, `side view`, `in profile`, or `south-facing`.
- For a complete direction pack, prefer full rotation endpoints over repeated one-off generations.
- If rotation is close but not clean, use the rotated output as an init/reference image and inpaint the broken body parts rather than restarting the whole direction pack.
- Relevant sources: [Pixelorama rotate workflow](https://www.youtube.com/watch?v=9KUAQqzaxsU&t=330s), [Generate rotations](https://www.youtube.com/watch?v=ufQ72nGORC0&t=0s), [Rotation and animations in one click](https://www.youtube.com/watch?v=RISPOYqeEGo&t=90s).

## Animation

Animation quality comes from smaller controlled steps.

- Start with a few frames to prove the motion, then increase complexity.
- For frame-rate upgrades, generate the four extreme/key frames first, then interpolate empty frames between them by adjusting frame rate and starting frame.
- Before animating from a stiff idle pose, create a better character state for the motion, then animate from that state. This gives the animation a stronger first frame.
- Use text animation for broad action labels such as walking, attacking, idle breathing, or casting.
- Use first/last frame workflows for action arcs where start and end poses matter.
- Use skeleton workflows when limb placement or exact motion matters. Estimate the skeleton, then inspect and adjust points before generation.
- For character states, generate durable states such as idle, walk, attack, sleep, hurt, or interact, then reuse them instead of ad hoc one-off clips.
- Transfer outfit/style to animation when the motion is already good but the sprite identity or clothing needs to change. Clean imperfect frames with edit-animation or inpaint instead of starting over.
- For facial/portrait animation, isolate the actual moving parts such as eyes and mouth so the rest of the portrait keeps the same style.
- Build pose libraries from reference animations when motion matters. Treat the reference as skeleton/proportion data, resize it to the target character's proportions, and process complex motions in small frame groups.
- To create animation variants, finish one character animation first, generate the variant from the original as init, then use the finished animation frames as init images for the variant. If more than four frames are generated in batches, keep the seed consistent across batches.
- For cleaner init-image animation, start from a similarly sized reference animation, recolor the reference-frame pieces toward the generated character, tune init/style balance, and expect manual cleanup. A community example used init weight around `150` for a similar reference and up to `600` for complicated motion, so treat values as tuning probes.
- For top-down RPG spritesheets, chain the tools instead of asking one endpoint to solve everything: create a style-locked sprite, rotate it into the needed directions, then run movement/simple movement for the walking frames. Traditional four-direction sheets often use three frames per direction, and the movement step may need retries even when style and rotation worked quickly.
- Relevant sources: [Character States](https://www.youtube.com/watch?v=oCJWxfEwX-o&t=180s), [Walking animations](https://www.youtube.com/watch?v=8TRHAC3fUpo&t=60s), [Animate Between 2 Frames](https://www.youtube.com/watch?v=1CjxHZoZE_I&t=270s), [Skeleton animation](https://www.youtube.com/watch?v=zBfVT5pwCSs&t=0s).

Endpoint bias:

- Use `/v2/animate-with-text-v3` for modern text-guided animation.
- Use `/v2/animate-with-skeleton` when pose control matters.
- Use `/v2/edit-animation-v2`, `/v2/interpolation-v2`, or first/last-frame workflows when refining motion.

## Editing, Inpainting, And Scale

Use the smallest edit region that solves the problem.

- Preserve useful context around the selected area.
- Inpaint bad regions instead of regenerating the full asset family.
- Use sketch/color hints inside the inpainted region when precise placement matters, such as a fireball, boots, tree, cave opening, treasure chest, or map landmark.
- For scale correction, place the existing correct-size asset beside the new generation area so PixelLab can infer the intended scale from adjacent context.
- If a sprite has too many colors or looks muddy, reduce or force it into the project's approved palette before judging whether the shape needs more edits.
- Remove backgrounds before composing sprites into scenes when transparency matters.
- Resize or scale after the usable form is established; do not mix scale correction with major concept changes.
- For color cleanup, swap colors deliberately before another init pass. Use reference swatches and replacement tools instead of expecting later generation to recover the intended palette by itself.
- Relevant sources: [Pixelorama and edit workflow](https://www.youtube.com/watch?v=9KUAQqzaxsU&t=600s), [Animated scenes edit pass](https://www.youtube.com/watch?v=1FWEXTiJnlc&t=270s), [Edit tool tutorial](https://www.youtube.com/watch?v=XhmpenTmPLg).

## Isometric Tiles

Treat isometric generation as a separate workflow, not top-down generation with angle words.

- Start from an isometric shape/tool selection when available.
- Use reference shape/type, description, outline/shading/detail, tile size, guidance weight, init image strength, color/palette, output method, seed, and shape options.
- Build and validate a single tile before scaling to a set or map.
- Relevant source: [Creating pixel art isometric tiles and map](https://www.youtube.com/watch?v=CuBvG9mfQng&t=150s).

## Visual Review Protocol

Some YouTube guidance is screen-dependent. Trigger visual review when a source window or user request depends on:

- "this", "these", "that", "here", "the button", "the dropdown", "the slider", "left/right/top/bottom", or visible settings.
- Tile transition quality, UI style matching, skeleton point placement, map export settings, scale correction, or before/after comparisons.

When visual review is needed:

1. Open the timestamped source link from `official-youtube-index.md` or the local visual queue.
2. Inspect the frame or short sequence around the timestamp.
3. Record the actual visible setting, button, layout, or result as a derived rule.
4. Do not invent screen details from transcript text alone.
