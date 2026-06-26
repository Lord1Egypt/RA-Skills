# Category Groups and Matching Algorithm

---

> Currently only `visual` is active. The rest are defined for future expansion.

## visual
```
image_generation, illustration, art, drawing, design, graphic, graphic_design,
photo, photography, animation, video, render, rendering, concept_art, sketch,
painting, anime, digital_art, character, character_design, webtoon, manhwa,
manga, portrait, thumbnail, banner, logo, icon, sprite, texture, storyboard,
realistic, photorealistic
```

## writing
```
copywriting, writing, content, blog, article, editing, proofreading,
storytelling, script, scriptwriting, social_media, marketing_copy, ux_writing,
caption, tagline, newsletter, press_release, resume, cover_letter
```

## translation
```
translation, translate, localization, l10n, i18n, subtitling, subtitle, dubbing
```

## code
```
code, coding, programming, development, software, web, app, backend, frontend,
fullstack, api, automation, script, bot, plugin, debugging, refactor
```

## data
```
data_analysis, data, analysis, research, statistics, excel, spreadsheet,
reporting, visualization, dashboard, scraping, crawling, survey
```

---

## Matching Algorithm

`calcMatch()` normalizes the job category (lowercase, replace hyphens/spaces with underscores) and tries stages in order:

1. **Exact alias (100%):** `allAliases.includes(normalizedCategory)`
2. **getGroup (80%):** `getGroup(normalizedCategory)` returns a configured group
3. **Token overlap (50%):** Tokenize by `_`, filter tokens 2 chars or shorter. For each token, check `getGroup(token)`
4. **Default fallback (30%):** `capabilities.default` exists
5. **No match (0%):** Auto-skip

`getGroup(token)` checks each group's alias list for an exact match or substring inclusion.
