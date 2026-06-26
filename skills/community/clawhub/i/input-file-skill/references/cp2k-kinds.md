# cp2k_kinds.md

This file defines element-to-default `&KIND` mapping rules for routine CP2K Quickstep calculations.

## 1. Scope

These defaults are for **routine pseudopotential DFT** in CP2K using:
- Gaussian basis sets from the MOLOPT family
- GTH pseudopotentials
- typically PBE exchange-correlation

They are intended as **skill defaults**, not as a substitute for explicit convergence testing.

## 2. Global defaults

### Default basis family
- Primary default: `DZVP-MOLOPT-SR-GTH`
- Tight / higher-accuracy option: `TZVP-MOLOPT-SR-GTH`
- For H and light-element molecules where cost is modest and accuracy matters, `TZVP-MOLOPT-GTH` or `TZV2P-MOLOPT-GTH` may be promoted by the skill

### Default pseudopotential family
- If XC functional is PBE-family: use `GTH-PBE` or the corresponding `GTH-PBE-qN` form
- If XC functional is BLYP-family: prefer matching GTH flavor when available
- If user explicitly requests all-electron treatment: use `POTENTIAL ALL` and an appropriate all-electron basis instead of GTH

### Default file names
- Basis file: `BASIS_MOLOPT`
- Pseudopotential file: `GTH_POTENTIALS`

## 3. Rule hierarchy

When generating a `&KIND` block, apply rules in this order:
1. explicit user request
2. task-specific override (for example XAS excited atom → all-electron)
3. XC-functional-matched pseudopotential family
4. element default from this file
5. project-wide fallback

## 4. Standard `&KIND` template

```text
&KIND <label>
  ELEMENT <element>
  BASIS_SET <basis>
  POTENTIAL <potential>
&END KIND
```

Use `ELEMENT` explicitly whenever the kind label differs from the chemical symbol, such as `Mg_surf`, `O_defect`, or `Pt1`.

## 5. Recommended default map for common elements

### 5.1 Main-group elements most common in chemistry/materials workflows

| Element | Default basis | Default potential |
|---|---|---|
| H  | DZVP-MOLOPT-SR-GTH | GTH-PBE-q1 |
| He | DZVP-MOLOPT-SR-GTH | GTH-PBE-q2 |
| Li | DZVP-MOLOPT-SR-GTH | GTH-PBE-q3 |
| Be | DZVP-MOLOPT-SR-GTH | GTH-PBE-q4 |
| B  | DZVP-MOLOPT-SR-GTH | GTH-PBE-q3 |
| C  | DZVP-MOLOPT-SR-GTH | GTH-PBE-q4 |
| N  | DZVP-MOLOPT-SR-GTH | GTH-PBE-q5 |
| O  | DZVP-MOLOPT-SR-GTH | GTH-PBE-q6 |
| F  | DZVP-MOLOPT-SR-GTH | GTH-PBE-q7 |
| Ne | DZVP-MOLOPT-SR-GTH | GTH-PBE-q8 |
| Na | DZVP-MOLOPT-SR-GTH | GTH-PBE-q9 |
| Mg | DZVP-MOLOPT-SR-GTH | GTH-PBE-q10 |
| Al | DZVP-MOLOPT-SR-GTH | GTH-PBE-q3 |
| Si | DZVP-MOLOPT-SR-GTH | GTH-PBE-q4 |
| P  | DZVP-MOLOPT-SR-GTH | GTH-PBE-q5 |
| S  | DZVP-MOLOPT-SR-GTH | GTH-PBE-q6 |
| Cl | DZVP-MOLOPT-SR-GTH | GTH-PBE-q7 |
| Ar | DZVP-MOLOPT-SR-GTH | GTH-PBE-q8 |
| K  | DZVP-MOLOPT-SR-GTH | GTH-PBE-q9 |
| Ca | DZVP-MOLOPT-SR-GTH | GTH-PBE-q10 |
| Br | DZVP-MOLOPT-SR-GTH | GTH-PBE-q7 |
| I  | DZVP-MOLOPT-SR-GTH | GTH-PBE-q7 |

## 6. Transition-metal defaults

Transition metals are less safe to map blindly because multiple valence-core partitions may exist depending on the GTH library entry, oxidation-state needs, semicore treatment, and target property.

### Policy
- Default basis: `DZVP-MOLOPT-SR-GTH`
- Default potential family: `GTH-PBE`
- But the skill must **verify the exact potential name present in the chosen CP2K potential file** before final rendering.
- For higher-accuracy solid-state or catalytic calculations, promote to `TZVP-MOLOPT-SR-GTH` or `TZV2P-MOLOPT-SR-GTH` when cost allows.

### Conservative skill behavior for 3d metals
For: Sc, Ti, V, Cr, Mn, Fe, Co, Ni, Cu, Zn
- basis default: `DZVP-MOLOPT-SR-GTH`
- potential default placeholder: `GTH-PBE`
- note: renderer should replace with the exact library name actually available in `GTH_POTENTIALS`

### Conservative skill behavior for 4d / 5d metals
For: Y, Zr, Nb, Mo, Tc, Ru, Rh, Pd, Ag, Cd, Hf, Ta, W, Re, Os, Ir, Pt, Au, Hg
- basis default: `DZVP-MOLOPT-SR-GTH`
- potential default placeholder: `GTH-PBE`
- verify exact library entry before rendering

## 7. Accuracy upgrades

### Standard mode
- basis: `DZVP-MOLOPT-SR-GTH`

### Better-accuracy mode
- basis: `TZVP-MOLOPT-SR-GTH`

### High-accuracy molecular mode
- basis: `TZV2P-MOLOPT-GTH` when available and affordable

### Very large screening jobs
- remain on DZVP unless the user explicitly asks for tight accuracy

## 8. Special overrides

### 8.1 All-electron tasks
Use when:
- user explicitly requests all-electron
- XAS / core-level excited atom treatment
- validation benchmark against pseudopotential setup

Policy:
- `POTENTIAL ALL`
- use a compatible all-electron basis (for example pcseg-n, 6-311G**, cc-pVXZ, pcX-n depending on workflow)
- do **not** keep MOLOPT+GTH on the excited atom in core-spectroscopy workflows

### 8.2 Mixed labels for chemically same element
Example:
```text
&KIND O_bulk
  ELEMENT O
  BASIS_SET DZVP-MOLOPT-SR-GTH
  POTENTIAL GTH-PBE-q6
&END KIND

&KIND O_ads
  ELEMENT O
  BASIS_SET DZVP-MOLOPT-SR-GTH
  POTENTIAL GTH-PBE-q6
&END KIND
```

### 8.3 Ghost atoms
Only create `GHOST` kinds if the workflow explicitly requires floating basis functions / BSSE-style setups.

## 9. Renderer validation requirements

Before writing the final input, the renderer should validate:
1. every element in the structure has a `KIND` mapping
2. each chosen basis exists in the loaded basis file
3. each chosen pseudopotential exists in the loaded potential file
4. if a kind label differs from the element symbol, `ELEMENT` is present
5. if the task requests all-electron on selected atoms, those atoms do not retain GTH pseudopotentials

## 10. Practical fallback behavior

If the exact `GTH-PBE-qN` entry is unknown at normalization time:
- store placeholder `GTH-PBE`
- mark `needs_library_resolution: true`
- let the rendering stage resolve the exact library entry from the installed CP2K data files

If no exact basis can be confirmed:
- fallback order:
  1. `DZVP-MOLOPT-SR-GTH`
  2. `DZVP-MOLOPT-GTH`
  3. raise a validation warning instead of silently inventing a name
