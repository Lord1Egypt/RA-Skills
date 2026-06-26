# CP2K Defaults

This file records the default starting points used by the CP2K OpenClaw skill.

These defaults are intended for first-pass draft generation.
They are not guaranteed to be optimal.
They do not replace convergence testing.

---

## 1. First-version scope

This version prioritizes:

1. molecule + xyz + geometry optimization
2. molecule + xyz + single-point energy

Other cases may be handled conservatively with warnings.

---

## 2. General philosophy

The skill should prefer:
- conservative defaults
- runnable drafts
- simple explicit input structure
- transparent assumptions

The skill should avoid:
- claiming "best" settings
- silently inventing difficult physical information
- pretending convergence has been validated

---

## 3. Method family defaults

### 3.1 Basic electronic-structure route
Default method family:
- Quickstep DFT-style workflow

### 3.2 Typical first-pass XC functional
Default XC functional:
- PBE

### 3.3 Basis / potential family
Default basis set:
- DZVP-MOLOPT-GTH

Default pseudopotential:
- GTH-PBE

### 3.4 Basis/potential notes
- If later element-specific logic is added, this file may be extended with per-element mappings.
- Some elements may only provide short-range basis options such as `DZVP-MOLOPT-SR-GTH`.
- For higher-accuracy production work, basis-set convergence should be reviewed.

### 3.5 Quickstep draft block defaults

For first-pass molecular DFT jobs, prefer:

- METHOD = Quickstep
- QS method = GPW
- SCF guess = ATOMIC

For non-periodic molecular jobs:
- prefer a non-periodic electrostatics treatment
- use an isolated-style Poisson setup when appropriate for the generated input template

For closed-shell nonmetal molecules:
- prefer OT-based SCF as the first draft choice

For metallic, small-gap, difficult open-shell, or problematic SCF cases:
- do not force OT blindly
- allow fallback to a more conservative diagonalization-style SCF strategy
- add a warning to the report

---

## 4. Molecular xyz defaults

### 4.1 System interpretation
If the input file is `.xyz` and the user does not explicitly request periodic crystal/surface behavior:
- interpret the system as an isolated molecule

### 4.2 Periodicity
Default:
- PERIODIC NONE

### 4.3 Cell handling
For xyz-only molecular jobs:
- automatically add a vacuum box
- use a geometry-based box if available
- otherwise use a conservative fallback cubic box

Preferred first-version geometric rule:
- cell length along each axis = molecular span along that axis + 10 Å

Minimum fallback:
- if any axis remains smaller than 15 Å after padding, use 15 Å for that axis

Conservative cubic fallback:
- 15 Å × 15 Å × 15 Å
---

## 5. Priority presets

### 5.1 Fast
Use when the user emphasizes speed.

Suggested defaults:
- cutoff = 400
- rel_cutoff = 40
- eps_scf = 1.0E-5
- max_scf = 80
- max_geo_opt_iter = 150

Use case:
- rough screening
- quick draft calculations
- lower-cost first pass

### 5.2 Balanced
Use when the user does not specify speed vs accuracy.

Suggested defaults:
- cutoff = 500
- rel_cutoff = 60
- eps_scf = 1.0E-6
- max_scf = 100
- max_geo_opt_iter = 200

Use case:
- standard first-pass molecular calculations

### 5.3 High
Use when the user emphasizes higher accuracy.

Suggested defaults:
- cutoff = 700
- rel_cutoff = 80
- eps_scf = 1.0E-7
- max_scf = 150
- max_geo_opt_iter = 300

Use case:
- more careful first-pass calculations
- still requires later convergence review

---

## 6. Charge and multiplicity defaults

If the user gives no charge and no evidence of a charged system:
- default charge = 0

If the user gives no multiplicity and no evidence of open-shell behavior:
- default multiplicity = 1

Also add warnings:
- review charge if the system is not neutral
- review multiplicity if the system is not closed-shell

## 6.1 Spin treatment defaults

If multiplicity = 1:
- use a closed-shell treatment by default

If multiplicity > 1:
- enable an unrestricted treatment in the generated draft
- add a warning that the spin state should be reviewed carefully

---

## 7. Hardware defaults

If the user does not specify machine information:
- hardware.type = unknown
- hardware.cores = null
- hardware.memory_gb = null

Do not invent machine details.

---

## 8. Geometry optimization defaults

For task type `geometry_optimization`:

### GLOBAL
- RUN_TYPE GEO_OPT

### MOTION / GEO_OPT
- OPTIMIZER BFGS
- MAX_ITER according to priority preset

---

## 9. Single-point defaults

For task type `single_point`:

### GLOBAL
- RUN_TYPE ENERGY

No geometry optimization section is required.

## 9.1 SCF default behavior

For balanced first-pass molecular jobs:
- prefer EPS_SCF according to the selected priority preset
- prefer MAX_SCF according to the selected priority preset

For closed-shell nonmetal molecules:
- prefer OT-style SCF in the first draft

Do not force this rule for:
- metallic systems
- likely open-shell radicals
- difficult transition-metal systems
- cases already flagged by the ambiguity policy

In such cases:
- keep the draft conservative
- add a warning for manual review

---

## 10. Input structure organization

For simple systems:
- prefer explicit coordinates in `&COORD`

For first version:
- prefer direct inline coordinates after reading xyz
- assume uploaded xyz coordinates are in angstrom
- preserve the original atom order unless there is a clear reason to change it

For more complex systems:
- external structure-file workflows may be added later

---

## 11. Important caveats

These defaults are starting points only.

The following must be reviewed carefully for serious calculations:
- basis-set quality
- cutoff / rel_cutoff convergence
- charge and multiplicity
- periodicity
- cell size for isolated molecules
- metal / open-shell / heavy-element / excited-state cases

## 11.1 Escalation cases

Do not silently finalize standard defaults for:

- transition-metal systems
- charged radicals
- heavy elements outside the validated default map
- periodic crystals or slabs inferred only from xyz
- excited-state requests
- spectroscopy-style requests such as TDDFT, XAS, EPR, or NMR

Instead:
- generate a conservative draft if possible
- add prominent warnings
- mark the relevant fields as needing review

---

## 12. Future extensions

Later versions may add:
- cif-based crystal defaults
- surface/slab defaults
- k-point rules
- element-specific basis/potential maps
- special warnings for transition metals
- alternative functionals
- smarter cell construction