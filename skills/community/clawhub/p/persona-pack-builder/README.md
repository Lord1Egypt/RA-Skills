# persona-pack-builder

A skill for building, refining, and packaging sellable AI persona / prompt products.

It is designed for workflows like:
- turning rough persona notes into structured prompt packs
- generating reusable deliverables such as `SYSTEM_PROMPT.md`, `PERSONA_CORE.md`, and `config.json`
- packaging persona bundles for sale, reuse, or internal operations
- converting prompt-product workflows into repeatable OpenClaw skill patterns

## Why this skill is useful
- Focuses on productized persona packs, not raw prompt dumping
- Separates system prompt, persona spec, examples, and packaging logic
- Helps standardize deliverables for resale or repeated generation
- Includes references and a starter script for faster pack generation

## Included files

```text
persona-pack-builder/
├── SKILL.md
├── README.md
├── references/
│   ├── openclaw-skill-variant.md
│   ├── persona-product-blueprint.md
│   └── safety-positioning.md
└── scripts/
    └── generate_persona_pack.py
```

## Trigger examples
- "Build me a sellable AI girlfriend prompt pack"
- "Turn these persona notes into a structured product"
- "Create a reusable persona system with examples and config"
- "Package this persona workflow as an OpenClaw skill"

## Packaging angle

This repository is shaped like a public-facing skill pack:
- clear SKILL frontmatter
- reusable references
- script support
- lightweight documentation for listings and discovery

## License

MIT
