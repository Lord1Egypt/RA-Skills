---
name: one-person-company-os
description: Build a visual operating cockpit for an AI-native one-person company across promise, buyer, product, delivery, cash, learning, and assets.
---

# One Person Company OS For Claude Skills

Use this skill when the user wants to create, operate, or improve an AI-native one-person company.

The visible operating loop is:

`promise -> buyer -> product capability -> delivery -> cash -> learning -> asset`

## Default Behavior

- Treat the user as founder and final decision-maker.
- Clarify the sellable promise, first buyer, and core problem before creating files.
- Persist only inside the founder-approved workspace.
- Keep the first reading surface as an operating cockpit.
- Keep markdown as editable work material and DOCX as formal deliverables.
- Use deterministic SVG/HTML for exact operating data.
- Treat AI image prompts as optional creative material.

## Runtime

If local filesystem and Python execution are available, prefer the canonical scripts from the repository root:

```bash
python3 scripts/preflight_check.py --mode create-company
python3 scripts/init_business.py "North Star Lab" --path ./workspace --product-name "North Star Assistant" --target-user "independent builders" --core-problem "they need one visible loop for product, revenue, delivery, and cash" --product-pitch "a visual operating cockpit for one-person AI companies" --language en-US --confirmed
python3 scripts/validate_release.py
```

If script execution is unavailable, continue manually and clearly say which content is not saved.

## Required Output Frame

Every substantial response should include:

- current primary goal
- current bottleneck
- primary arena: `sales / product / delivery / cash / asset`
- shortest action today
- saved path or unsaved reason
- next cockpit surface to open

## Boundaries

- Do not auto-install system packages.
- Do not request unrelated credentials.
- Do not write outside the approved workspace.
- Ask for founder approval before pricing, budget, legal, launch, or high-risk customer-facing actions.
