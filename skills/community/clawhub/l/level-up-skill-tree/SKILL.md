---
name: level-up-skill-tree
description: Organize learning goals into a skill tree with dependencies, current level, upgrade conditions, and the next best path. Use when the user wants a realistic growth roadmap across study, work, or personal interests.
---

# Level Up Skill Tree

Chinese name: 技能树成长

## Purpose
Turn scattered learning goals into a skill tree with dependencies so the user can stop guessing what to learn next.
This skill is descriptive only. It does not run assessments, enroll courses, or call external services.

## Use this skill when
- The user wants to learn many things but needs a realistic order.
- The user feels stuck on a plateau and wants a next upgrade path.
- The user needs to balance core growth with side branches.
- The user wants a role-based learning map instead of a flat task list.

## Inputs to collect
- Target role or identity
- Core capabilities to build
- Existing baseline or prior experience
- Time constraints and resource limits
- Current blockers or plateau symptoms
- Desired outcome horizon

## Workflow
1. Collect the target role, important capabilities, existing foundations, and real-world constraints.
2. Break the capabilities into trunk skills, branch skills, prerequisite nodes, passive buffs, and breakthrough nodes.
3. Define each node with current level, upgrade condition, recommended practice action, and whether a skip is realistic.
4. Draw the current-stage tree and mark already unlocked nodes.
5. Recommend the next best upgrade route with one short-cycle training action and a validation method.

## Output Format
- Role positioning with a main-role and side-role style summary.
- Skill tree overview with branches, dependencies, and already unlocked nodes.
- Next upgrade route with a reasoned priority order.
- This week's smallest upgrade actions and how to verify progress.

## Quality bar
- The tree must reflect dependencies rather than a flat list.
- Recommendations must match the user's real time and baseline.
- Include at least one short-cycle action that can be validated quickly.
- Avoid unrealistic leapfrogging when prerequisites are missing.

## Edge cases and limits
- If the user has too many goals, choose one main tree and park the rest as side branches.
- If skill labels are too abstract, translate them into trainable behavior first.
- Do not present this as professional certification, academic advising, or formal career assessment.

## Compatibility notes
- Works for students, parents, self-learners, career shifters, and long-term builders.
- Can pair conceptually with achievement-unlock-tracker or quest-chain-decomposer.
- Fully dialogue-based, no assessment API required.
