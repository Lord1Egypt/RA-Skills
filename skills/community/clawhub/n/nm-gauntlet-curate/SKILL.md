---
name: curate
description: Adds developer-authored annotations to the gauntlet knowledge base
version: 1.10.3
triggers:
  - capturing tribal knowledge or rationale not visible in code
metadata: {"openclaw": {"homepage": "https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet", "emoji": "\ud83e\udd9e"}}
source: claude-night-market
source_plugin: gauntlet
---

> **Night Market Skill**: ported from [claude-night-market/gauntlet](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet). For the full experience with agents, hooks, and commands, install the Claude Code plugin.


# Curate Knowledge

Add developer-authored annotations to the knowledge base.

## When NOT To Use

- Knowledge derivable from the code itself (use `gauntlet:extract`)
- The DSA problem bank (use `gauntlet:problem-bank`)

## Steps

1. Identify the module to annotate
2. Ask for the concept (key insight or rule)
3. Ask for the why (rationale, history, context)
4. Generate YAML annotation file
5. Save to `.gauntlet/annotations/<slug>.yaml`
6. Confirm saved and will be included in future challenges

## Exit Criteria

- [ ] A YAML file exists at `.gauntlet/annotations/<slug>.yaml`
  after the skill completes, where `<slug>` is derived from the
  annotated module and concept
- [ ] The YAML file contains at minimum a `concept` field (key
  insight or rule) and a `why` field (rationale/history/context)
- [ ] Confirmation message states the annotation will be included
  in future challenges, indicating it is on the discovery path
  for `gauntlet:extract`
- [ ] Annotation does not duplicate an existing entry under the
  same slug (checked before saving)
