---
name: orshot-design
description: "Design craft for Orshot studio templates: one focal point, a 2-font type system, 60-30-10 color, copy that still fits when the data changes, restrained motion, the brand kit when the design should be on-brand, layouts that do not repeat, and a create-then-critique loop over the hosted Orshot MCP server. The shared craft base that every Orshot use-case skill loads when it creates or refines a template (posts, stories, carousels, ads, banners, thumbnails, video). Use when: \"design a template for this\", \"make this template look less generic\", \"refine this design\", \"build an on-brand post template\", \"why does this look AI-made\". NOT for rendering, batches or posting (use orshot) or for a whole job end to end (use its use-case skill, for example orshot-blog-images or orshot-ad-creative)."
homepage: https://orshot.com/agents/skills
license: MIT
metadata:
  author: Orshot
  version: "1.3.0"
  mcp-server: orshot
  openclaw:
    emoji: "🎨"
    homepage: https://orshot.com/agents/skills
    primaryEnv: ORSHOT_API_KEY
    requires:
      env: []
      bins: []
    envVars:
      - name: ORSHOT_API_KEY
        required: false
        description: Orshot API key. Only for REST. Not needed over the hosted Orshot MCP server with OAuth.
---

# Orshot Design: the craft layer

Make Orshot studio templates that look designed, not like the generic centered-text "AI" look. This skill is judgement: layout, hierarchy, type, color, copy fit and motion taste. It works on top of the MCP design tools (`orshot_create_template_design`, `orshot_update_template_design`, `orshot_patch_template_elements`, `orshot_get_brand_kit`). Use the `orshot` skill to render.

## Where the facts live

This skill does not restate field names, style keys, value types, units, animation schema, audio fields, canvas sizes or the craft systems. Read them from the source, through one MCP tool, `orshot_get_design_spec`, by topic:

- `template-json`: pages, elements, styles, text rules, shapes, SVG, animation, audio, subtitles. Also https://orshot.com/docs/definitions/template-json.md.
- `craft`: the systems every template follows (hierarchy, two fonts, text fit and its floors, 60-30-10 colour, composition, imagery), the brand mapping, the compatibility rules that break renders, the anti-patterns.
- `social-pack`: posts, stories and carousels: formats and safe areas, drawn graphics, a concrete element tree.
- `layout`: computed layouts (rows, stacks, grids, anchors instead of hand-set x/y).
- `video-pack`, `film`, `film-pack`: motion and video. Also https://orshot.com/docs/definitions/film.md, https://orshot.com/docs/orshot-studio/animations.md, https://orshot.com/docs/orshot-studio/motion.md, https://orshot.com/docs/video-generation/video-options.md, https://orshot.com/docs/video-generation/adding-subtitles.md.
- `formats-catalogue`, `post-formats`, `ad-formats`, `video-post-formats`, `youtube-thumbnail-layouts`: the formats real brands run, to browse; `orshot_plan_design` returns the ones that fit a job.
- Text fit modes: https://orshot.com/docs/orshot-studio/text-modes.md.

## Operating principle

**Design serves the task.** Decide the one thing the viewer must take away, then make everything support it. Respect the brand and the platform over generic prettiness.

## Workflow (in order)

1. **Shape.** Restate the goal, the audience and the single key message before placing anything.
2. **Plan.** `orshot_plan_design` with the brief, `job` (what the user is making, in their words), the canvas size and `on_brand: true` when the design should be on-brand. It returns the formats real brands run for that job (skeleton, size, fields, what makes each work) and the plan: palette, font pair, type scale, material. Pick the format whose fields match what changes per render and name it. With no matching format (a document, an unusual job) the plan carries a slot layout and a ready skeleton: build that.
3. **Gather, in parallel.** `orshot_get_design_spec` topic `template-json` once per session, plus the pack for the medium (`social-pack`; `video-pack` and `film` for anything that moves). If the design should be on-brand, `orshot_get_brand_kit` (filter with its per-type tag arguments, such as `imageTags: "logo"`, only when the kit is tagged); its colours and fonts win over the plan's.
4. **Build the complete design in one call.** `orshot_create_template_design` with the format's skeleton in the plan's palette and type, finished copy, real assets, the dynamic fields and, for video, motion and timing. Set `includeThumbnails: true` so the create is also the visual check. Do not send a sparse first draft to refine later.
5. **Critique.** Read the thumbnail, the "Design checks" warnings and, for a recognised vertical, the "🎨 Design check" block. Check the design against the format's notes (what every strong one shares). Fix only concrete findings, in one focused `orshot_update_template_design` or `orshot_patch_template_elements` call. Never ship a pass you have not looked at.

## Copy fit (the template must survive real data)

A template is rendered with copy you have not seen. Design for the longest realistic value, not the sample: fill the template with copy at the length the user will really send, then render the longest value once before calling it done. The fit mode, its floors per role, highlight spans and line breaks are in the `craft` topic.

## Variety

Never repeat a layout for the same content type. `orshot_plan_design` rotates the look per workspace; between templates of the same kind, pick a different format or a different shape of the same format.

## Motion and sound (video templates)

Making video look designed, not generated:

- **Reveal in sections over about 4 to 5 s.** Layers that form one unit (icon and label, a spec row, the footer) share the same enter animation and start time. Stagger about 0.3 to 0.5 s between sections, in reading order. Where the timing keys sit is the spec's number one gotcha: read its animation section.
- **Every full-bleed photo gets a slow Ken Burns ambient** (zoom about 1.08 to 1.15). A still photo held 3 seconds reads as a dead frame. Alternate the pan direction between pages.
- **Ambient motion stays subtle and slow:** 6 to 10 s cycles against a 0.5 s enter. If the viewer can name the motion, it is too strong, unless it is a deliberate accent. Looping ambients need linear easing or the loop seam shows.
- **Every word gets read.** A viewer reads at about 2.5 words a second (0.4 s per word) from when a block starts entering, blocks one after another in entrance order, then the scene holds about 1 s before the cut; the last arrival in a scene holds 2 s or more, and line draws take 2 to 3 s. Too long? Cut words, never speed up the motion. The film checks ("Cut too soon", "Dead stretch") measure this.
- **One cut family per video,** 0.9 to 1.2 s per cut, chosen by what the cut means (`orshot_get_design_spec` topic `film-pack`). A different transition per cut is the clearest tell of an auto-generated edit. A video over 8 s or with more than one scene is a film: the `orshot-video-generator` skill.
- **Sound.** A voice track at full volume plus a quiet music or ambient bed (about 0.08 to 0.18 volume) sounds produced. That is 2 tracks on a page, and the number of tracks per page depends on the plan (video-options.md), so a render over the limit fails. Budget narration at about 2.5 words per second with 1 s of headroom. Burn in captions over speech, with a thicker stroke over busy footage (presets: adding-subtitles.md). On Claude clients the server does not offer generated narration or sound effects; use brand audio or uploaded files.
- **Check the layout with a still, not a video.** The motion preview from `includeThumbnails` is free. Before a paid mp4, render one page as a PNG to check composition.

## Examples

### Example 1: "Make an Instagram post announcing our new feature"

1. `orshot_plan_design` with `job: "instagram post announcing our new feature"`, 1080x1350 and `on_brand: true`: it returns the changelog card (chip with platform and version, a 1 to 3 word headline, the hero render owning the right half) and the palette and type. In parallel: `orshot_get_design_spec` topic `template-json` if not read this session; `orshot_get_brand_kit`.
2. Name the format, then lay out its skeleton at the default feed size.
3. `orshot_create_template_design` with `includeThumbnails: true`: brand display font for the headline, the brand's dominant color as the background, the accent color on one word, logo and handle in the footer, the headline and image as parameters.
4. Check: read the thumbnail and the "🎨 Design check" lines (repetition, fonts, contrast). If one shows a real issue, fix it in one `orshot_patch_template_elements` call.

### Example 2: "Refine this template, it looks generic"

1. `orshot_get_studio_template` to read the current design.
2. Diagnose against the anti-patterns: centered stack? 3 fonts? no focal point? brand ignored?
3. `orshot_patch_template_elements` with `includeThumbnails: true`: one focal headline, 2 fonts, brand colors in 60-30-10, left or bottom alignment.
4. Stress-test the copy fit: `orshot_render_template` with `format: "png"`, `responseType: "base64"` and the longest realistic headline in `modifications`, so you can see the result. If the text overflows or shrinks below its floor, shorten the box's job or split the line.

## Troubleshooting

**A headline will not break, or breaks in the wrong place.** In rich text use `<br>`, not `\n`. A highlighted span never wraps; shorten it or move the highlight to color.

**Colors or fonts look off-brand.** The brand kit was skipped or mapped by label. Call `orshot_get_brand_kit` and map colors by role and fonts by family name.

**The "🎨 Design check" warns about repetition.** The layout matches a recent template of the same type. Plan again with another format of the same post type, or another shape of the format, and move the focal point.
