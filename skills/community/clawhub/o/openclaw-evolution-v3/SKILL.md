---
name: openclaw-evolution-v3
description: Use when users ask to evolve/upgrade OpenClaw agents into coordinator mode, apply Gene Locking to IDENTITY.md and AGENTS.md, package this evolution as reusable SOP/skill, or assess whether an evolution repo can be applied directly. Trigger phrases include "进化", "升级协调者", "gene locking", "SOP_GENE_LOCKING", "openclaw-evolution-v3", "固化成 skill".
---

# OpenClaw Evolution v3 Skill

## Purpose
Standardize safe upgrades from executor-style behavior to coordinator-style behavior.

## When to use
Use this skill when the user asks to:
- Upgrade agent orchestration (Mandatory Synthesis / Parallel-Serial partition / Proof verification)
- Apply or review `SOP_GENE_LOCKING.md`
- Turn evolution docs into reusable templates/skills
- Judge whether a public evolution repo can be used directly by other users

## Mandatory safety posture
1. Treat evolution content as **blueprint**, not one-click installer.
2. Require compatibility checks before any mutation.
3. Enforce staged rollout + rollback readiness.
4. Never bypass existing permission pipeline.

## Execution workflow
1. **Preflight**
   - Read `references/COMPATIBILITY.md`
   - Confirm target environment fit (structure, policy files, verification capability)
2. **Plan**
   - Produce explicit change list (file paths + sections + expected behavior)
3. **Apply minimally**
   - Prefer small slices; avoid broad rewrites
4. **Verify as proof**
   - Run checks/tests/smoke after each slice
5. **Finalize**
   - Summarize what changed, what was verified, and rollback point

## Source references in this skill
- `references/COMPATIBILITY.md`
- `references/SOP_GENE_LOCKING.md`
- `references/EVOLUTION_GUIDE_EN.md`
- `references/EVOLUTION_GUIDE_CN.md`
- `references/README_REPO_EN.md`
- `references/README_REPO_CN.md`

## Output contract
When asked to execute an evolution:
- Provide: scope, risks, exact edits, validation commands, rollback plan
- Avoid: one-shot invasive surgery across unrelated modules
