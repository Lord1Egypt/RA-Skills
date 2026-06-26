---
name: outreach-sequence-crafter
description: Build respectful multi-touch outreach sequences with channel mix, follow-up
  timing, objection handling, and logging templates.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Outreach Sequence Crafter

## Purpose

Build respectful multi-touch outreach sequences with channel mix, follow-up timing, objection handling, and logging templates.

## Trigger phrases

- 写邀约话术
- build an outreach sequence
- 私域触达节奏
- cold outreach cadence
- 招商邀约流程

## Ask for these inputs

- offer
- target persona
- channels
- timeline
- proof assets
- dos and don'ts

## Workflow

1. Clarify the offer, audience, and desired action.
2. Select a cadence preset from the resources file.
3. Draft first touch, follow-up, breakup, and reply branches.
4. Generate a lightweight tracking table with status codes.
5. Keep claims verifiable and avoid spammy patterns.

## Output contract

- multi-touch sequence
- reply branches
- tracking sheet
- testing plan

## Files in this skill

- Script: `{baseDir}/scripts/sequence_builder.py`
- Resource: `{baseDir}/resources/cadence_presets.yaml`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 写邀约话术
- build an outreach sequence
- 私域触达节奏

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/sequence_builder.py`.
- Bundled resource is local and referenced by the instructions: `resources/cadence_presets.yaml`.
