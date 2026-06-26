# Design Rules

This file defines the behavior rules for the CP2K OpenClaw skill.

## 1. Product goal

The purpose of this skill is:

- accept simple natural-language requests
- accept uploaded structure files
- infer a safe CP2K job draft
- apply conservative defaults when possible
- generate:
  - normalized JSON job spec
  - CP2K input draft
  - short explanation report

This skill is designed for ease of use, not for claiming globally optimal settings.

---

## 2. Core principles

1. Prefer practical defaults over over-complication.
2. Avoid unnecessary follow-up questions.
3. Never silently invent physically critical information.
4. Always expose assumptions in `defaults_applied` or `notes`.
5. Treat generated parameters as starting points, not guaranteed best settings.

---

## 3. Safe defaults

These defaults may be applied automatically.

### 3.1 Task defaults
- If the user says "optimize", "结构优化", or "几何优化", assume `geometry_optimization`.
- If the user says "single point", "单点", or "单点能", assume `single_point`.

### 3.2 Structure defaults
- If the uploaded file is `.xyz` and the user does not mention periodicity, assume an isolated molecule.
- If the uploaded file is `.cif`, prefer crystal-like interpretation unless the user clearly says otherwise.
- If the uploaded file is `.pdb`, default to molecular treatment unless the user explicitly says periodic crystal/surface.

### 3.3 Priority defaults
- If the user does not specify speed vs accuracy, use `balanced`.
- If the user says "快一点", "尽量快", "先粗算", use `fast`.
- If the user says "精度高", "更精确", "更高精度", use `high`.

### 3.4 Periodicity defaults
- For isolated molecule handling, default to `NONE`.
- For simple xyz molecular jobs, add a vacuum box automatically.
- Default molecular box size may be a conservative cubic cell such as 15 Å unless later replaced by a geometry-based rule.

### 3.5 Charge and multiplicity defaults
- If the request looks like a normal closed-shell molecular job and there is no evidence otherwise, use:
  - `charge = 0`
  - `multiplicity = 1`
- Also add a warning reminding the user to review charge/multiplicity if the system is not neutral closed-shell.

### 3.6 Hardware defaults
- If hardware is not specified:
  - `hardware.type = "unknown"`
  - `hardware.cores = null`
  - `hardware.memory_gb = null`

---

## 4. Things that must NOT be silently invented

Do NOT silently invent these if they are physically important:

- nonzero charge
- open-shell multiplicity
- whether a crystal/surface is really periodic if only xyz is provided
- advanced method choices for:
  - transition metals
  - excited states
  - strongly correlated systems
  - unusual heavy-element cases
- k-point strategy for clearly periodic materials unless enough information is available

If these are missing, either:
- add a warning to `notes`, or
- ask a follow-up question only if the ambiguity blocks safe draft generation

---

## 5. Follow-up question policy

The skill should minimize follow-up questions.

Ask a follow-up only when the missing information changes the physical meaning of the job.

### Ask if:
- the user says "surface" or "crystal" but only provides `.xyz`
- the system appears likely charged but charge is unspecified
- the system appears open-shell but multiplicity is unspecified
- the user asks for a specialized calculation that cannot be safely defaulted

### Do not ask if:
- the user omitted speed/accuracy preference
- the user omitted hardware details
- the user omitted explicit vacuum-box preference for a simple molecule
- the user used informal wording but the task is still clear enough

---

## 6. Normalized JSON requirements

The skill must normalize requests into a JSON object with these keys:

- task_type
- system_type
- structure_file
- periodicity
- charge
- multiplicity
- priority
- hardware
- notes
- defaults_applied

### Example shape

```json
{
  "task_type": "geometry_optimization",
  "system_type": "molecule",
  "structure_file": "uploaded.xyz",
  "periodicity": "NONE",
  "charge": 0,
  "multiplicity": 1,
  "priority": "balanced",
  "hardware": {
    "type": "cpu",
    "cores": null,
    "memory_gb": null
  },
  "notes": [],
  "defaults_applied": []
}