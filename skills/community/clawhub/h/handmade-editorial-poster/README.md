# Handmade Editorial Poster

Turn every reference photo into its own quiet, handmade editorial-poster cover.

[![Agent Skill](https://img.shields.io/badge/Agent-Skill-orange.svg)](SKILL.md)
[![Image capable](https://img.shields.io/badge/Image-reference%20workflow-blue.svg)](references/platform-adapters.md)

## What It Does

`handmade-editorial-poster` turns each supplied photograph into a separate high-end illustration: a tiny recognizable subject, large paper-like negative space, up to four source-derived colors, and deliberately imperfect hand-drawn acrylic-and-paper texture. It preserves the visual relationship that makes the photograph recognizable without reproducing it as photography.

```text
Make handmade posters from these photos. One illustrated poster per photo; no collage.
```

## Why Use It

| | A generic image prompt | This skill |
| --- | --- | --- |
| Multiple photos | Often combines them into one image | One independent output for every input photo |
| Recognition | May lose the source subject or gesture | Preserves silhouette, pose, object, and relationship |
| Art direction | Drifts toward ads or polished vectors | Enforces quiet editorial space and physical paper texture |
| Missing image tool | May claim an output exists | Produces a mapped, ready-to-paste prompt instead |

## Use Cases

| Scenario | Fit | Why |
| --- | --- | --- |
| Personal photographs as art-book-like covers | ✅ | Minimal illustrated reinterpretation, one result per photo |
| A poetic social post or zine cover | ✅ | Quiet, small-subject editorial composition |
| Photo restoration or faithful photographic retouching | ❌ Use a photo-restoration workflow | This skill intentionally redraws and simplifies the source |
| Collages, contact sheets, or multi-photo composites | ❌ Use a layout/design workflow | This skill prohibits shared compositions |
| Product ads or conversion-focused campaign creative | ❌ Use a marketing-design workflow | The visual brief is non-commercial and restrained |
| 3D characters or polished vector mascots | ❌ Use a character/3D illustration workflow | Material imperfection and paper texture are essential here |

## Trigger Keywords

**English:** `make handmade posters from these photos`, `turn these photos into minimalist editorial covers`, `create one illustrated poster per photo`, `photo-to-paper art posters`, `make an art-book cover from this photo`, `make a paper-textured illustration poster`, `quiet editorial poster`, `minimal handmade cover`, `illustrated zine cover`, `one photo one poster`.

## Quick Start

Install with your host's normal Skill mechanism, then attach one or more photos and use natural language. You can also invoke it explicitly as `$handmade-editorial-poster`.

```text
Turn these photos into minimalist handmade editorial covers. Process each photo independently, in order. Use 9:16 for portrait photos and 16:9 for landscape photos. No collage and no invented text.
```

For Codex, OpenClaw, Claude Code, Hermes, DeepSeek Harness, and other agent hosts, see [platform adapters](references/platform-adapters.md).

## Example

**Input:** three attached photos: a cyclist, a dog by a chair, and a person holding flowers.

**Output:** three independent posters in the same attachment order. Each has a small lower-center illustration, warm paper background, four or fewer colors from its own source image, and no invented captions.

## Architecture

```text
handmade-editorial-poster/
├── SKILL.md                       # Core workflow and quality gate
├── README.md                      # English documentation
├── agents/openai.yaml             # Optional Codex UI metadata
└── references/
    ├── prompt-library.md          # Bilingual master and retry prompts
    └── platform-adapters.md       # Capability-first host integration
```

## Customization

- Provide a verified short title, place, year, or number only when you want optional typography. Otherwise the skill omits text.
- Ask for a `vertical 9:16` or `landscape 16:9` override when the source orientation should not control the poster.
- To keep a series cohesive, specify a shared paper tone or a named 2–4 color palette; recognition of each individual source photo remains the priority.

## Troubleshooting

| Issue | Cause | Fix |
| --- | --- | --- |
| Several source photos appear in one output | The generation call was batched into one composition | Re-run one image job per reference and state `no collage` |
| The poster looks like a smooth vector graphic | The material constraints were underweighted | Use the provided “More handmade” retry phrase |
| The subject is not recognizable | Simplification removed the source relationship | Use the “Better recognition” retry phrase |
| The host has no image tool | The active model is text-only | Return one ready-to-paste prompt per photo; configure an image-capable tool separately |

## Credits

- Concept and implementation: [Jialin / 0xcjl](https://github.com/0xcjl)
- Skill format: compatible with the open `SKILL.md` convention used by modern coding-agent hosts.
