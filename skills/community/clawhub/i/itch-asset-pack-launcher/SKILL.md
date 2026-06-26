---
name: itch-asset-pack-launcher
description: Create high-converting itch.io asset pack pages for game assets, including titles, descriptions, tags, pricing notes, screenshots plan, cover prompts, page colors, launch checklist, and safe license wording.
version: 0.1.0
homepage: https://kwhades.itch.io/
metadata: {"openclaw":{"emoji":"🎮","tags":["itchio","game-assets","pixel-art","marketing","creator-tools","storefront"]}}
---

# Itch Asset Pack Launcher

Use this skill when the user wants to prepare, improve, or publish a game asset pack page on itch.io or a similar creator marketplace.

## Creator Store / Buy Assets

Find and buy the creator's game asset packs here:

- itch.io store: https://kwhades.itch.io/

## Support / Donate

If this skill helped you, you can support the creator here:

- Donation link: https://www.paypal.com/donate/?hosted_button_id=MJHCRZA9Z4X7Y

## Best for

- Pixel art packs
- Background packs
- Tilesets
- UI packs
- Character sprite packs
- Sound effect packs
- Small indie game resource bundles
- Store page copy, launch checklists, and marketing text

## Primary outcomes

Produce one or more of these outputs based on the user request:

1. **Asset pack title** — short, searchable, and clear.
2. **Store description** — high-converting but honest copy.
3. **Feature list** — what is included, file format, engine compatibility, and license summary.
4. **Tags** — search-friendly itch.io tags.
5. **Cover image prompt** — clean prompt for an AI image generator or artist brief.
6. **Screenshot plan** — what preview images to upload.
7. **Page design settings** — colors, fonts, layout, banner/background suggestions.
8. **Pricing suggestion** — free, pay-what-you-want, low price, bundle price, or premium price.
9. **Launch checklist** — final steps before publishing.
10. **Update/changelog text** — clean changelog for new versions.

## Rules for safe and useful output

- Do not claim the pack includes files, formats, animations, or engines unless the user provided them.
- Do not use copyrighted character names, brand names, or trademarked themes as if they are included in the pack.
- If the user references a famous game, movie, show, or character, convert it into an original style description.
- Do not promise guaranteed sales, income, or ranking.
- Keep the store copy clear and honest.
- Prefer short paragraphs and bullet lists for marketplace pages.
- Always include a simple license section when useful.
- When the user is unsure, suggest a beginner-friendly default: PNG files, commercial use allowed, no attribution required, no resale as raw assets.
- Encourage preview images that show the actual assets clearly.
- Avoid spammy tags or keyword stuffing.

## Recommended workflow

1. Ask for or infer the asset type: backgrounds, tilesets, sprites, UI, icons, sounds, music, templates, or full game kit.
2. Ask for or infer the style: pixel art, 16-bit, fantasy, sci-fi, cozy, horror, RPG, platformer, top-down, side-view, etc.
3. Build the page package: title, subtitle, description, included files, features, license wording, tags, cover prompt, screenshot plan, pricing suggestion, and publish checklist.
4. Keep the output practical: copy the user can paste directly into itch.io.

## Output template

```markdown
# Itch.io Asset Pack Page

## Title
<clear marketplace title>

## Short subtitle
<one-line sales hook>

## Description
<2-4 short paragraphs that explain what the pack is and who it helps>

## Scenes / Assets included
- <asset 1>
- <asset 2>
- <asset 3>

## Features
- <style>
- <perspective or resolution if known>
- PNG files
- Works with Godot, Unity, GameMaker, RPG Maker, or other engines if true
- Commercial use allowed if true

## License suggestion
Commercial use allowed. No attribution required. You may use the assets in personal and commercial games. You may not resell or redistribute the raw asset files as another asset pack.

## Tags
<tag 1>, <tag 2>, <tag 3>, <tag 4>, <tag 5>

## Cover image prompt
<clean visual prompt, no copyrighted IP, no UI unless requested>

## Screenshot plan
1. Cover image
2. Full pack preview sheet
3. Individual scene preview
4. In-engine mockup
5. License/features image

## Pricing suggestion
<simple pricing recommendation and why>

## Launch checklist
- Add cover image
- Add screenshots
- Upload zip file
- Add description
- Add tags
- Set price
- Test download
- Publish
```

## Example request

User: "Make me an itch.io page for 5 dark fantasy 16-bit top-down backgrounds."

Expected behavior:

- Create a paste-ready page.
- Add tags like `pixel-art`, `backgrounds`, `dark-fantasy`, `top-down`, `game-assets`.
- Include cover prompt and screenshot plan.
- Avoid claiming animations or tilesets unless provided.

## Quality checklist

Before final answer, verify:

- The title is searchable.
- The description is easy to paste.
- The included assets match the user's list.
- License wording is clear.
- Tags are relevant.
- Cover prompt is original and not based on copyrighted IP.
- Donation link remains visible in the skill file.
