---
name: portfolio-case-study-forge
description: Turn rough project notes into polished portfolio case studies with metrics,
  visuals checklist, and interviewer talking points.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Portfolio Case Study Forge

## Purpose

Turn rough project notes into polished portfolio case studies with metrics, visuals checklist, and interviewer talking points.

## Trigger phrases

- 做作品集案例
- turn this project into a case study
- 项目包装成作品集
- portfolio story
- 面试讲项目

## Ask for these inputs

- project notes
- target audience recruiter/client/interviewer
- available metrics
- screenshots or links
- tone

## Workflow

1. Structure the story into context, role, problem, approach, constraints, outcome, and lessons.
2. Identify missing proof points and suggest what screenshots or charts to add.
3. Generate short and long versions for portfolio sites and interviews.
4. Produce talking points and FAQ answers.
5. Avoid inflating impact; mark assumptions explicitly.

## Output contract

- case study draft
- visuals checklist
- talking points
- FAQ sheet

## Files in this skill

- Script: `{baseDir}/scripts/case_study_scaffold.py`
- Resource: `{baseDir}/resources/case_study_template.md`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 做作品集案例
- turn this project into a case study
- 项目包装成作品集

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/case_study_scaffold.py`.
- Bundled resource is local and referenced by the instructions: `resources/case_study_template.md`.
