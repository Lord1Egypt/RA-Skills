---
name: cp2k-input-generator
description: This skill should be used when generating CP2K input drafts (.inp) for quantum chemistry calculations from local structure inputs. It is a documentation-driven skill that uses reference files to interpret requests, apply conservative defaults, and explain assumptions. The current documented workflow supports local .xyz structures.
---

# CP2K Input Generator

This skill helps the user generate a CP2K input draft from:
- a simple natural-language description
- an uploaded local structure file such as .xyz

The uploaded skill package is intentionally scoped to a local-only, documentation-driven workflow. It does not perform automatic retrieval from external structure databases such as PubChem or Materials Project, and it does not include Python runtime helper scripts in the uploaded version.

## What this skill does

This skill should:
1. Understand the user's CP2K job request from plain language.
2. Read or reference the uploaded local structure file.
3. Normalize the request into a standard CP2K job specification.
4. Apply conservative defaults from the reference files when the missing information is safe to infer.
5. Avoid unnecessary follow-up questions when the ambiguity is not physically important.
6. Produce:
   - a CP2K input draft
   - a short explanation report describing defaults, assumptions, and limitations

## When to use this skill

Use this skill when the user:
- asks for a CP2K input file
- describes a simulation in natural language
- uploads a local .xyz structure file and wants a CP2K job draft
- asks for geometry optimization, single-point energy, or a simple CP2K setup

Do not use this skill to claim that a structure has been automatically retrieved from an online source. In the current uploaded package, external databases may be mentioned only as manual suggestions for where the user could obtain a structure.

## Core principles

- Prefer practical, conservative defaults.
- Be explicit about assumptions.
- Do not claim that the generated settings are globally optimal.
- Do not claim that convergence has been fully validated unless the user explicitly provides such evidence.
- Default silently only when the missing field does not change the physical meaning of the calculation.

## Safe defaults

Apply defaults silently when safe:

- If the user uploads a local .xyz file and does not mention periodicity, assume an isolated molecular calculation.
- If the user asks to "optimize" a structure, assume geometry optimization.
- If the user does not specify speed vs accuracy, use balanced settings.
- If the structure is an isolated molecule without cell information, add a vacuum box as a default container for the generated CP2K input.
- If hardware details are missing, leave hardware fields as unknown rather than inventing machine details.

## Reference files

The skill should use the following reference files during decision-making:

- `references/cp2k-task-map.md`
  - use this file to map a user request to CP2K task settings

- `references/cp2k-kinds.md`
  - use this file to assign default basis sets and pseudopotentials by element

- `references/cp2k-defaults.md`
  - use this file to fill in conservative general defaults

- `references/ambiguity-policy.md`
  - use this file when the user request is underspecified or physically ambiguous

These reference files are used as decision support within the skill instructions. In the uploaded skill package, they are not executed by local helper scripts.

## Do not silently invent these

Do NOT silently invent:
- total charge, if the system is likely not neutral
- spin multiplicity, if open-shell behavior is plausible
- whether a system is truly periodic if the user says crystal or surface but only provides xyz
- advanced method choices for metals, excited states, strongly correlated systems, or unusual elements

If such information is missing, either:
- add a warning to notes
- or ask a follow-up question only if the ambiguity is physically important

## Execution flow

When handling a user request, the skill should follow this order:

1. Determine the request type:
   - CP2K input generation
   - parameter refinement
   - explanation or debugging of an existing CP2K input

2. Determine the system type:
   - molecule
   - bulk crystal
   - surface/slab
   - 2D material

3. Normalize the request into the standard CP2K job contract.

4. Use `references/cp2k-task-map.md` to map the request to:
   - task type
   - run type
   - method family
   - SCF style
   - periodicity assumptions
   - k-point behavior
   - geometry/cell optimization behavior

5. Use `references/cp2k-kinds.md` to assign element-dependent basis/potential defaults.

6. Use `references/cp2k-defaults.md` to fill in remaining conservative defaults.

7. If ambiguity remains, apply `references/ambiguity-policy.md`.

8. Produce:
   - a CP2K input draft
   - an explanation report

## Output requirements

Every successful run should produce, at minimum:

1. job.inp
2. report.md

The report should always include:
- interpreted task
- detected system type
- defaults applied
- warnings
- fields that may need user review

If a normalized intermediate representation is used during reasoning, it should be treated as an internal contract for the skill logic rather than a required user-facing artifact in the uploaded package.

## Current limitations

- The uploaded skill package does not include Python runtime scripts.
- The current documented workflow supports local .xyz structures only.
- The skill does not automatically retrieve structures from external databases.
- The generated settings are draft-quality and must be reviewed by the user before production use.

## Standard JSON contract

When internal normalization is needed, use a JSON object with the following keys:

```json
{
  "task_type": "geometry_optimization",
  "run_type": "GEO_OPT",
  "system_type": "molecule",
  "structure_file": "uploaded.xyz",
  "periodicity": "NONE",
  "charge": 0,
  "multiplicity": 1,
  "priority": "balanced",
  "xc_functional": "PBE",
  "basis_family": "DZVP-MOLOPT-GTH",
  "potential_family": "GTH-PBE",
  "scf_mode": "OT",
  "kpoints_scheme": "GAMMA",
  "cell_handling": "auto_vacuum_box",
  "cutoff": 500,
  "rel_cutoff": 60,
  "eps_scf": 1.0e-6,
  "max_scf": 100,
  "optimizer": "BFGS",
  "hardware": {
    "type": "unknown",
    "cores": null,
    "memory_gb": null
  },
  "notes": [],
  "defaults_applied": [
    "task_type=geometry_optimization",
    "run_type=GEO_OPT",
    "periodicity=NONE",
    "xc_functional=PBE",
    "basis_family=DZVP-MOLOPT-GTH",
    "potential_family=GTH-PBE",
    "scf_mode=OT",
    "kpoints_scheme=GAMMA",
    "cell_handling=auto_vacuum_box",
    "cutoff=500",
    "rel_cutoff=60",
    "eps_scf=1.0e-6",
    "max_scf=100",
    "optimizer=BFGS"
  ],
  "review_required": []
}
```