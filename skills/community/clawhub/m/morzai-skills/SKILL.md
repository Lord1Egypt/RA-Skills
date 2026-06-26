---
name: morzai
description: >-
  Unified entry point for Morzai workflows. Routes requests through
  api/commands.json into the matching child skill.
metadata:
  openclaw:
    emoji: "🛍️"
    tags: ["ecommerce", "fashion", "listing-set", "ai-editing"]
---

# Morzai AI Skills

This is the master gateway for the Morzai AI suite. It identifies user needs and routes them to the appropriate specialized sub-skill.

## Root Responsibility

- Route the request to exactly one child skill.
- Read `api/commands.json` before asking follow-up questions.
- Ask only for missing required inputs, and ask at most 2 short questions in one turn.
- After routing, open the target child skill and continue the task in the same user-facing agent.
- Do not promise unsupported behavior from the root layer.

## Capability Layers

### Layer 1: Single-Function Editing Tools
- `apparel-recolor`
- `garment-retouch`
- `clothing-adjustment`

### Layer 2: Composite Listing Workflow
- `morzai-ecommerce-product-kit`

## Source Of Truth

- Routing rules, required inputs, follow-up prompts, and execution mapping are defined in [api/commands.json](api/commands.json).
- Child skill details stay in:
  - [skills/apparel-recolor/SKILL.md](skills/apparel-recolor/SKILL.md)
  - [skills/garment-retouch/SKILL.md](skills/garment-retouch/SKILL.md)
  - [skills/clothing-adjustment/SKILL.md](skills/clothing-adjustment/SKILL.md)
  - [skills/ecommerce-product-kit/SKILL.md](skills/ecommerce-product-kit/SKILL.md)

## Flow

### Step 1: Detect Intent
- Read `api/commands.json`.
- Choose the single best matching command.
- If still ambiguous, ask one short disambiguation question.

### Step 2: Fill Missing Inputs
- Use the command's `required_inputs` and `optional_inputs`.
- Ask only for missing required inputs first.
- If the user gave a sample image for recolor, treat it as a way to derive the target color, not as permission to skip color confirmation entirely.

### Step 3: Enter Child Skill
- Open the routed child skill file.
- From this point on, follow the child skill's workflow and constraints.
- The root skill stops being the domain expert after routing and missing-input collection.

### Step 4: Execute
- Use the command's `execution` mapping from `api/commands.json`.
- Layer 1 workflows use the routed child skill's remote MCP metadata.
- `morzai-ecommerce-product-kit` uses the public `morzai` CLI path.
- Return a clean result summary to the user.

## Command Map

### Layer 1
- `apparel-recolor` -> [skills/apparel-recolor/SKILL.md](skills/apparel-recolor/SKILL.md)
- `garment-retouch` -> [skills/garment-retouch/SKILL.md](skills/garment-retouch/SKILL.md)
- `clothing-adjustment` -> [skills/clothing-adjustment/SKILL.md](skills/clothing-adjustment/SKILL.md)

### Layer 2
- `morzai-ecommerce-product-kit` -> [skills/ecommerce-product-kit/SKILL.md](skills/ecommerce-product-kit/SKILL.md)

## Guardrails

- The root skill must not invent new parameters outside `api/commands.json`.
- The root skill must not restate all child-skill knowledge.
- The root skill must not keep working at the root layer after the child skill has been selected.
