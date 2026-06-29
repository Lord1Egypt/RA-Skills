# Community Discord Tutorials

These notes were distilled from the PixelLab Discord `#tutorials` channel on 2026-06-21 after scrolling from the channel start on 2023-06-07 to the newest visible post on 2026-06-20. The channel is mostly a curated tutorial feed, so this file tracks source coverage and preserves the workflow tips that came from Discord post text rather than from transcript analysis.

No Discord screenshots, media, tokens, cookies, raw chat exports, downloaded videos, or audio files belong in this uploadable package.

## How To Use This Reference

- Use `official-youtube-index.md` for the full official PixelLab YouTube inventory and transcript status.
- Use this file when the user specifically asks about Discord `#tutorials`, external community tutorials, or whether a tutorial-channel link was accounted for.
- Treat Nikola/community videos as external references. They can inform the workflow, but they do not change the official PixelLab channel coverage count.
- If a tutorial depends on visible UI settings, open the linked video at the relevant timestamp before turning the screen into a hard rule.

## Channel-Only Workflow Tips

### Top-Down RPG Direction And Walk Sheets

For RPG-style four-direction character sheets, chain tools:

1. Use a style workflow to create the initial sprite in the target game style.
2. Rotate the sprite into the required directions.
3. Use Movement or Simple Movement to create the walking frames.

The community tip specifically called out three frames per direction. Style and rotation may work quickly, while movement often needs a few retries to get feet and walking motion right.

### Side-Scroller Terrain Prompts

When side-scroller tile generation misunderstands the terrain, simplify the material wording. A Discord post said `ice floor` was not the best description and that `ground` would have been better. Preserve visible, non-inpainted context around the edit so PixelLab can infer missing tile information from the surrounding image.

### Style-Consistent Character Variants

The tutorial feed reinforces a repeatable route for character families:

1. Generate a base character or sprite with `Create M-XL image` or the current character workflow.
2. Use inpainting to create variations while preserving the base style.
3. Rotate the character after the style is acceptable.
4. Add held equipment such as a shield or sword with inpainting, including the hands or arms that must change to hold it.

### Pixelorama And PixelLab

The Pixelorama tutorials are workflow bridges: create or edit with PixelLab, do local pixel cleanup in Pixelorama, then return to PixelLab for rotation, animation, or inpainting when the AI step adds value. Keep each asset export explicit so later engine import is deterministic.

### Godot And MCP Tutorials

For Godot and MCP tutorials, keep the concept but adapt the agent:

- Generate PixelLab assets first.
- Save sprites, tilesets, maps, states, and animations into the project asset tree.
- Wire the files in Godot or the target engine as a separate step.
- Do not assume Claude Code is installed; Codex/OpenClaw can perform the same asset and code wiring if the local project allows it.

## Tutorial Feed Coverage

The table below records the tutorial-channel items captured from Discord. Corrected YouTube IDs are used where the Discord text or screenshot could be confused by `O`/`0`, `I`/`l`, or similar glyphs.

| Date | Source | Video ID | Tutorial role |
|---|---|---|---|
| 2023-06-07 | Channel start | none | Tutorial channel opened; first posts point users to the PixelLab tutorial feed. |
| 2023-06-14 | PixelLab | `wijMirHw6QQ` | Short attack-animation tutorial; official ledger marks it caption-unavailable. |
| 2023-08-09 | PixelLab | `mlCa0UdAhow` | Creating pixel-art animations with PixelLab. |
| 2023-08-13 | PixelLab | `NCINAMZqWjg` | Panda animation walkthrough. |
| 2023-08-21 | PixelLab | `yuXcjgZJJv0` | Early side-scroller map tile setting and workflow. |
| 2023-09 | PixelLab | `qVc_cMn53sk` | Rotation cleanup with init images and inpainting. |
| 2023-09-29 | Discord text tip | none | Top-down RPG flow: style, rotate, then movement/simple movement. |
| 2023-10-08 | PixelLab | `iBMq3P_Fazk` | Style-consistent images with the style generation tool. |
| 2023-10-08 | PixelLab | `w_E_kbCXRn4` | Animation with a template. |
| 2023-10-18 | PixelLab | `bNtMm0SeJ74` | Character rotation tutorial. |
| 2023-10-31 | PixelLab | `Xx4UQpDyMFQ` | Creating maps and tiles with PixelLab. |
| 2023-11-19 | PixelLab | `XVlbYNMI3xg` | Side-scroller map tiles; includes the `ice floor` versus `ground` prompt note. |
| 2023-11-19 | PixelLab | `O9maOTbLuHQ` | Map Workshop tutorial. |
| 2023-12-11 | PixelLab | `br2EO65qHAU` | Exporting PixelLab maps to Godot. |
| 2023-12-19 | PixelLab | `OdRIHQ4ar2c` | Pixel-art UI generation. |
| 2023-12-23 | PixelLab | `XdgK1KeN-3s` | Animate with text. |
| 2024-01-27 | PixelLab | `hOZzbQBjKPc` | Pixelorama workflow covering skeleton animation, rotation, and inpainting. |
| 2024-02-06 | Nikola | `rvkiN2k2d7g` | External zero-to-hero workflow: character, rotation, walking animation. |
| 2024-04-03 | PixelLab | `rAtY1U9QWKM` | Character and animation from scratch with skeleton tooling. |
| 2024-04-24 | PixelLab | `inyHAOkwDlc` | Skeleton and quick animation workflow. |
| 2024-05-14 | PixelLab | `RVVuDhyEbRI` | Running animation template. |
| 2024-07-27 | PixelLab | `5o1oK4ILYBM` | Infinitely tiling backgrounds and parallax-style extension. |
| 2024-08-20 | PixelLab | `ptWw9gkgorQ` | Generating pixel-art characters and animations. |
| 2025-01-27 | PixelLab | `68BYzLoLh-U` | Style-consistent characters through inpainting, rotation, and equipment edits. |
| 2025-02-05 | PixelLab | `T4by1uEXuE4` | Isometric animals and related workflow. |
| 2025-02-10 | PixelLab | `0SQRclReGo4` | Destructible environments and damaged states. |
| 2025-03-02 | PixelLab | `84yChPoOaew` | Full side-scroller level with tiles and backgrounds. |
| 2025-03-09 | PixelLab | `qVDkp1baJkU` | Interior maps for top-down games. |
| 2025-03-13 | PixelLab | `8TRHAC3fUpo` | Walking animations. |
| 2025-03-18 | PixelLab | `zghUW8fGqsM` | Animate with text v3. |
| 2025-03-25 | PixelLab | `1CjxHZoZE_I` | Interpolate or animate between two frames. |
| 2025-05-07 | PixelLab | `p1l9S3ta_XA` | New tileset workflow. |
| 2025-05-15 | PixelLab | `jPPznIEK7HY` | Tilesets and maps using the newer tileset and map-extension workflow. |
| 2025-06-02 | PixelLab | `H-dPJKmKr1E` | Side-scroller maps and tilesets. |
| 2025-06-14 | PixelLab | `CuBvG9mfQng` | Isometric tiles and maps. |
| 2025-07-06 | PixelLab | `owkamgYVWAs` | Animation-to-animation. |
| 2025-07-16 | PixelLab | `XhmpenTmPLg` | Edit tool workflow. |
| 2025-07-29 | Nikola | `eQ3KIXyNk5s` | External animation tricks: animate with text, animate with skeleton, animation-to-animation. |
| 2025-08-04 | Nikola | `5BvfyHEABBQ` | External game workflow using animate with text, tilesets, and Godot import. |
| 2025-10-03 | PixelLab | `THwZYWuOdZI` | PixelLab MCP plus Godot game-building workflow; adapt agent tooling to Codex/OpenClaw. |
| 2026-05-11 | PixelLab | `moCpjMOOBGk` | GBA-style characters, maps, and animations. |
| 2026-05-25 | PixelLab | `oCJWxfEwX-o` | Character states for animation. |
| 2026-06-02 | PixelLab | `9KUAQqzaxsU` | Pixelorama plus PixelLab create, edit, rotate, and animate workflow. |
| 2026-06-20 | PixelLab | `LcJQQwltQ2Q` | Latest captured tutorial: same-style character generation and animation states. |

## Coverage Boundaries

- Official PixelLab tutorial-channel videos that also appear in `official-youtube-index.md` inherit that file's transcript status.
- External Nikola videos were metadata-checked on 2026-06-21. Caption download returned YouTube HTTP 429 during this pass, so no external transcript text was added to the package.
- The old unavailable attack link was normalized to the official ledger ID `wijMirHw6QQ`.
- This file is an index and distilled workflow guide, not a raw transcript archive.
