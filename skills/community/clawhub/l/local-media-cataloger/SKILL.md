---
name: local-media-cataloger
description: Index local photos, videos, and creative assets into a searchable manifest
  with tags, dates, shoot info, and reuse ideas.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Local Media Cataloger

## Purpose

Index local photos, videos, and creative assets into a searchable manifest with tags, dates, shoot info, and reuse ideas.

## Trigger phrases

- 整理素材库
- catalog my media folder
- 摄影素材归档
- 视频素材清单
- asset manifest

## Ask for these inputs

- media folder path
- tagging rules
- project or shoot name
- deliverable types
- favorite selection criteria

## Workflow

1. Scan files and extract basic metadata such as extension, size, timestamps, and dimensions when available.
2. Apply consistent tags and generate a manifest CSV/JSON.
3. Flag near-duplicates for manual review using filename/date heuristics.
4. Suggest folder structures for archive, selects, exports, and delivery.
5. Return a catalog summary and reuse opportunities.

## Output contract

- media manifest
- folder plan
- duplicate candidates
- reuse ideas

## Files in this skill

- Script: `{baseDir}/scripts/media_manifest.py`
- Resource: `{baseDir}/resources/metadata_schema.json`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 整理素材库
- catalog my media folder
- 摄影素材归档

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/media_manifest.py`.
- Bundled resource is local and referenced by the instructions: `resources/metadata_schema.json`.
