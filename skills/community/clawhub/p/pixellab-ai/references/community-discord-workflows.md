# Community Discord Workflow Notes

These notes were distilled from the PixelLab Discord `#helpful-posts` list on 2026-06-20. They are community recipes, not API guarantees. Re-check current UI labels and slider ranges before treating a value as exact.

No Discord screenshots, media, tokens, cookies, or raw chat exports belong in this uploadable package.

For the Discord `#tutorials` channel feed and channel-only tutorial tips, read `community-discord-tutorials.md`.

## Covered Posts

The visible `#helpful-posts` index contained these 13 entries:

- Hugo: Using PixelLab tilesets with Sprite Fusion.
- Community post: Generating larger images than 200x200.
- JosephT: Building a pose library.
- JosephT: Add weapons and held equipment.
- JosephT: Repeat a very specific style.
- JosephT: Make non-human, humanoid species.
- JosephT: Change a character but keep the style consistent.
- JosephT: Text prompts and basic PixelLab workflow for characters.
- Judas: Detailed prompts.
- Judas: Creating tilesets with Create M-XL image.
- Hampe: Animating characters with a similar style.
- NikolaIPatricioStar: Animation tutorial video.
- NikolaIPatricioStar: Animations with init images.

## Tilesets And Sprite Fusion

For a PixelLab tileset intended for Sprite Fusion:

1. Generate or export the PixelLab tileset with the `Export To Sprite Fusion` option.
2. Import that file into Sprite Fusion by drag-and-drop or the `Import tileset` action.
3. Use the imported autotile layer to draw and test the map immediately.

Do not call a tileset finished until it has been tested in an autotile or map editor. Pretty tiles can still fail at edge transitions.

## Large Canvas Workflow

For images larger than the normal square canvas:

- Make a backup before resizing or extending the canvas.
- When resizing/extending a canvas, keep `Trim content outside the canvas` unchecked unless the user explicitly wants outside content deleted.
- Establish the art direction first, then crop, extend, or fit the result to the game aspect ratio.

## Character Prompt Blocks

Detailed prompts work best when the visible features are separated into labeled drawing commands:

```text
Body: tall and lean warrior with a calm commanding presence.
Clothing: layered brown and muted gray robes.
Expression: thoughtful and measured.
Pose: upright stance, one hand relaxed, one hand holding a glowing blade.
Accessories: simple belt and boots.
```

Add categories only when they matter: `Body`, `Clothing`, `Expression`, `Pose`, `Aura`, `Weapon`, `Palette`, `Material`, `Silhouette`, or `Accessories`.

Match the prompt with plugin settings. `sidescroller (eye level)` gives a taller full-body read. `high top-down (45-degree)` gives compact top-down proportions. Keep the direction control explicit, such as `south (facing camera)`.

## Basic Character Iteration

For a new character:

1. Draw a rough init image first, even if it is crude. It gives PixelLab the intended scale, stance, and composition.
2. Keep the text prompt simple.
3. Spell out the color of each important part: face, hands, robe, belt, shoes, trim, weapon, and similar elements.
4. If the first generation is close but not good enough, use it as the next init image and rerun with the same settings.

## Specific Style Matching

For a restricted sprite size or a very specific style:

- Set the canvas to the target sprite size so the model cannot grow the subject beyond the intended footprint.
- Use a style reference image with matching perspective.
- Raise style guidance when exact matching matters. The community example used a high range around `90-120`, but this must be tuned per style.
- Keep the prompt simple, but describe all colors and materials.
- If needed, reuse the same reference as the init image and increase init strength. The community example used a stronger range around `350-400`.

## Non-Human Humanoid Characters

For humanoid species that are not plain humans:

1. Generate or draw a human baseline first to lock size, limb proportions, and style.
2. Use that baseline as both style and init reference.
3. Lower init strength enough that the prompt can change species traits.
4. Prefer joined species words when they are common enough, such as `tigerman`, before trying separated words.
5. If the joined word is too vague, add a literal fallback such as `human body with tiger head`.

Balance the species prompt carefully. Too much species language can destroy the humanoid body; too little produces a normal human.

## Editing A Character While Keeping Style

When changing one trait while preserving the same style:

- Inpaint only the regions that must change.
- Prompt the full target image, not only the masked detail.
- Reuse the original as a low-strength init image so style and pose stay anchored.
- Avoid masking the eyes when possible. Stable eye placement helps keep the face aligned.
- Expect small face or eye cleanup after the generation.

## Weapons And Held Equipment

Putting items into hands needs more than a text prompt:

1. Use the base sprite as the style image.
2. Duplicate the base frame.
3. Draw a crude placeholder for the equipment with the correct size, position, and color.
4. Inpaint the equipment plus any nearby arms or hands that must move to hold it.
5. Prompt the whole final sprite, not just the new equipment.

Balance style and init strength. Too much style can overwrite the placeholder; too much init can prevent the grip from improving.

## Pose Libraries

A pose library can be built from existing animation references:

- Treat the reference as a skeleton/proportion source, not necessarily a style source.
- Resize or squash the reference frames if the target character has shorter or different proportions.
- Work in small frame groups. Traditional four-frame JRPG walks may only need the key frames, while complex motions need chunking into manageable frame groups.
- Keep the cleaned pose references for later state or animation generation.

## Reusing A Finished Animation For Variants

To make multiple characters share a similar animation:

1. Finish one character and one good animation first.
2. Generate the variant character using the original character as an init image.
3. Use the finished animation frames as init images for the variant.
4. If the animation needs more than four frames, use the same seed across every generation batch that contributes frames.

In the community thread, a similar reference image plus init weight around `150` was used for the variant-animation pass. Treat that as a starting point, not a universal default.

## Animation With Init Images

For cleaner animations from a reference pack:

- Start from a reference animation with a similar size and motion.
- Generate an idle or base character that matches the reference size.
- Recolor the reference-frame pieces toward the generated character before using them as init inputs. This helps PixelLab understand which body parts and colors should carry over.
- Expect failed frames. Tune style and init balance, then manually clean or replace colors where needed.
- For complicated motion, init strength can be much higher than usual; one community example mentioned using `600`.
- Add tiny details such as eyes or helmet pixels manually when the model will not reliably preserve them.

Do not recommend this as the fastest method for every animation. It is a control-heavy method for cases where cleaner motion and shared style matter more than speed.

## External Animation Tutorial Link

The helpful-posts list also points to a community YouTube animation tutorial. Treat it as a supplemental visual walkthrough. Do not fold it into the official PixelLab YouTube coverage counts unless it is separately indexed and reviewed.
