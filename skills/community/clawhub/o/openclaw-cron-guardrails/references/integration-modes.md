# Integration Modes

This skill/plugin is designed to work in more than one integration style.

## Mode 1 — Natural-language quick start
Use this when:
- a human wants to create a cron quickly
- the upstream system wants a friendly default path

What this mode is good for:
- common reminder / worker / visible-delivery requests
- recommended patterns
- safe defaults

What this mode is not for:
- covering every possible phrasing edge case
- replacing a stronger upstream planner or model

## Mode 2 — Normalized-intent handoff
Use this when:
- the upstream product/model already interpreted the request
- you want a stable middle layer before rendering a cron spec

Recommended shape:
- use the normalized intent structure from `references/intent-routing.md`
- then convert with `scripts/intent_to_cron_spec.py`

Why this exists:
- lets upstream systems keep freedom in prompt understanding
- keeps this plugin focused on safe translation and guardrails

## Mode 3 — Spec-first deterministic path
Use this when:
- the caller wants maximum predictability
- the system already knows what job should be created
- validation and rendering matter more than natural-language convenience

Recommended flow:
1. prepare cron spec JSON
2. validate with `scripts/validate_cron_spec.py`
3. render with `scripts/render_cron_command.py`
4. create with `scripts/create_cron.py` if desired

Why this exists:
- this is the most stable path
- it minimizes dependence on prompt interpretation quality

## Design Principle
Natural language is a convenience layer.
The core product value is safe scheduled-task construction, validation, and routing.
