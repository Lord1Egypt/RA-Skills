---
name: persona-pack-builder
description: Build, refine, and package sellable AI persona/prompt products such as companion personas, roleplay personas, prompt packs, and style bundles. Use when creating a persona product from scratch, converting rough prompt notes into a structured pack, generating deliverables like SYSTEM_PROMPT.md/config.json/examples, or preparing a persona pack for sale or internal reuse. Best for prompt products and persona bundles, not for impersonating real people.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🎭"
    homepage: "https://github.com/xiaonizhou-crypto/persona-pack-builder"
---

# Persona Pack Builder

Build persona products as prompt packs first. Treat this skill as a product-packaging workflow for personality/style bundles, not as a real-person cloning workflow.

## Output goal

Produce a reusable folder that usually contains:

- `README.md`
- `SYSTEM_PROMPT.md`
- `PERSONA_CORE.md`
- `config.json`
- `examples/short_replies.md`
- `examples/conversations.md`
- optional `modes/*.md`
- optional `SALES_COPY.md`
- optional `FAQ.md`

If the user only needs a lightweight deliverable, collapse this to a single `persona.md` plus `examples.md`.

## Workflow

### 1. Classify the product

Identify which product is being built:

- **Prompt pack**: reusable persona for end users across AI platforms
- **Persona system**: pack with multiple modes, JSON config, and examples
- **Builder kit**: reusable templates for generating many persona products
- **OpenClaw skill candidate**: only when the user explicitly wants an OpenClaw-installable workflow

Default to **prompt pack** unless the user clearly asks for a skill, installer, or agent workflow.

### 2. Extract the persona shape

Define these before writing files:

- positioning: what the persona feels like
- relationship: friend / lover / coach / creator / etc.
- tone: direct / soft / playful / cool / mature / etc.
- boundaries: what it must not do
- formats: which platforms or prompt slots it must fit
- monetization tier: lite / standard / pro / custom

When source material references a real person, abstract it into public-trait language. Do not claim identity, ownership, or exact replication of a real person.

### 3. Create the core files

Write the files in this order:

1. `SYSTEM_PROMPT.md` — concise, model-facing instructions
2. `PERSONA_CORE.md` — expanded human-facing spec
3. `examples/*.md` — short replies and multi-turn examples
4. `config.json` — structured representation for products/apps
5. `README.md` — buyer/operator instructions
6. optional `modes/*.md`, `SALES_COPY.md`, `FAQ.md`

Prefer fewer stronger examples over large amounts of repetitive filler.

### 4. Keep the pack sellable

Optimize for:

- clear emotional effect
- consistent tone
- low cringe / low oiliness
- platform portability
- easy customization

The buyer should be able to answer:

- What feeling does this persona create?
- Where do I paste it?
- How do I tune it?
- What makes it different from random prompts online?

### 5. Package for the right audience

If the buyer is a normal AI user, deliver a prompt pack.

If the buyer is an advanced OpenClaw user, optionally also create:

- a skill folder with this workflow
- templates under `assets/`
- references under `references/`

Do not force persona content itself into a skill unless the user specifically wants agent-side automation.

## Writing rules

- Use short, concrete language
- Keep the system prompt tighter than the human docs
- Keep examples natural; avoid repetitive catchphrases
- Avoid obvious customer-support phrasing
- Avoid direct celebrity impersonation or “I am X” framing
- Prefer style abstractions such as “top-star energy”, “direct but warm”, or “protective but restrained”

## File guidance

### SYSTEM_PROMPT.md

Include:

- role and tone
- interaction rules
- forbidden styles
- response priorities

Keep it compact enough to fit platforms with smaller system fields when possible.

### PERSONA_CORE.md

Include:

- positioning
- traits
- relationship dynamic
- language style
- emotional logic
- naming/calling style
- dos and don'ts

### examples/

Include at least:

- 15-30 short replies
- 5-10 multi-turn dialogues

Cover likely emotional states and product-selling moments.

### config.json

Represent:

- name/version
- traits
- speech style
- modes
- boundaries
- optional tuning knobs

### README.md

Explain:

- what the pack is
- who it is for
- included files
- how to use it
- what not to claim publicly

## Decision rule: prompt pack vs skill

Choose **prompt pack** when the user wants to sell or use a persona directly.

Choose **skill** when the user wants an OpenClaw workflow that repeatedly generates persona packs, audits them, or standardizes packaging.

If both are useful, build the prompt pack first and the skill second.

## Bundled resources

### assets/templates/

Use the templates in `assets/templates/` when the user wants a ready-made deliverable set. They provide a starter pack for:

- `README.md`
- `SYSTEM_PROMPT.md`
- `PERSONA_CORE.md`
- `config.json`
- `examples/short_replies.md`
- `examples/conversations.md`
- `SALES_COPY.md`

Copy and customize them instead of rewriting the same scaffolding from scratch.

### scripts/

Use `scripts/generate_persona_pack.py` to generate a starter persona-product folder from templates.

Example:

```bash
python3 scripts/generate_persona_pack.py --output /tmp/my-pack
```

To override defaults, create a JSON file with replacement keys and pass:

```bash
python3 scripts/generate_persona_pack.py --output /tmp/my-pack --values values.json
```

Use the script when speed and packaging consistency matter more than bespoke wording.

## References

- Read `references/persona-product-blueprint.md` for a compact packaging blueprint.
- Read `references/safety-positioning.md` when the request is inspired by a public figure or risks identity confusion.
- Read `references/openclaw-skill-variant.md` when converting the persona-product workflow into an installable OpenClaw skill.
