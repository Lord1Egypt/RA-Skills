# ambiguity_policy.md

This file defines how the skill should make automatic, conservative choices when the user request is incomplete, underspecified, or scientifically ambiguous.

## 1. Core principle

When the user is vague, the skill should:
1. infer the **minimum scientifically reasonable workflow**
2. choose **conservative, standard CP2K defaults**
3. record all inferred choices explicitly in normalized JSON or notes
4. avoid silently selecting exotic methods
5. surface warnings when ambiguity could materially change results

## 2. Ambiguity classes

### 2.1 Task ambiguity
Examples:
- “帮我算一下这个结构”
- “生成一个 CP2K 输入文件”
- “看看这个材料的性质”

Resolution order:
1. if user mentions “optimize / relax / 弛豫” → `GEO_OPT`
2. if user mentions “cell / lattice / 晶格常数” → `CELL_OPT`
3. if user mentions “MD / 动力学 / 温度” → `MD`
4. if user mentions “band / DOS / band gap / 能带” → periodic SCF + band/DOS workflow
5. if user mentions “adsorption / binding / 吸附能” → adsorption workflow
6. otherwise fallback to single-point `ENERGY`

## 3. Structure-class ambiguity

If the user does not state the system class, infer from structure source / composition / metadata.

### 3.1 Molecule or cluster
Indicators:
- xyz-like finite coordinates
- small organic / inorganic molecule
- no lattice vectors

Default decisions:
- `PERIODIC NONE`
- add vacuum box
- no k-points
- OT SCF

### 3.2 Bulk crystal
Indicators:
- CIF / POSCAR / Materials Project entry
- lattice vectors present and clearly 3D periodic

Default decisions:
- periodic cell retained
- use k-points unless the supercell is very large
- if task is “optimize structure” and bulk-like → prefer `CELL_OPT` rather than `GEO_OPT`

### 3.3 2D material / slab
Indicators:
- monolayer name, slab, surface index, large vacuum in one direction, user mentions “surface”, “adsorption on”, “2D”, “monolayer”

Default decisions:
- preserve vacuum direction
- use k-point mesh `kx ky 1`
- if adsorption requested, add dispersion by default

## 4. XC-functional ambiguity

If XC is not specified:
- default to `PBE`

If user only says “GGA”:
- map to `PBE`

If user asks for “high accuracy” but gives no functional:
- keep `PBE` unless there is a clear need for a hybrid
- optionally annotate: “hybrid functional not auto-selected because cost may increase substantially”

If user asks for hybrid but not which one:
- molecule / molecular crystal: prefer `PBE0`
- periodic semiconductor/material screening: prefer `HSE06` if hybrid is feasible
- metallic large systems: warn and fall back to PBE unless user insists

## 5. Basis/pseudopotential ambiguity

If user gives no basis:
- standard default: `DZVP-MOLOPT-SR-GTH`

If user asks for better accuracy without naming a basis:
- promote to `TZVP-MOLOPT-SR-GTH`

If user does not specify pseudopotential:
- use GTH family matched to XC flavor
- for PBE: `GTH-PBE`/`GTH-PBE-qN`

If exact transition-metal pseudopotential entry is uncertain:
- do not invent the suffix
- store placeholder and require render-time library resolution

## 6. SCF ambiguity

### 6.1 If electronic character is not specified
Infer from composition and system type:
- isolated closed-shell molecule → insulating
- organic crystal / typical semiconductor → likely finite-gap
- bulk metal / elemental metal / known metallic surface → metallic
- uncertain transition-metal oxide → mark as uncertain

### 6.2 Default SCF choices
- likely insulating, gamma-point, no smearing need → OT
- metallic, small-gap, or explicit k-point mesh → diagonalization + mixing + smearing
- uncertain case → diagonalization is safer than OT for robustness

## 7. k-point ambiguity

If molecule / cluster:
- no k-points

If periodic bulk and cell is primitive/small:
- auto-generate Monkhorst-Pack mesh
- initial heuristic:
  - large supercell: `1 1 1`
  - ordinary bulk: start from about `4 4 4`
  - anisotropic cells: reduce along long dimensions

If 2D material:
- `kx ky 1`
- start from about `6 6 1` for small primitive cells, lower for larger supercells

If metallic system:
- prefer denser mesh than insulating analogue

Always note that k-point convergence is still required for publishable results.

## 8. Dispersion ambiguity

Add dispersion by default when any of the following is true:
- layered material
- molecular crystal
- organic adsorbate on surface
- physisorption / interface / van der Waals heterostructure

Do not force dispersion by default when:
- strongly ionic/covalent bulk screening and no inter-fragment vdW physics is central

Preferred automatic choice:
- D3(BJ)-style correction when available in template/policy

## 9. Cell and vacuum ambiguity

### Molecules
- create cubic or orthorhombic box with 10 Å minimum padding from outermost atom

### 2D slabs
- preserve in-plane lattice
- ensure at least ~15 Å vacuum normal to slab if structure source does not already provide enough

### Adsorption systems
- keep slab cell fixed unless user explicitly asks for full cell relaxation

## 10. Spin / charge ambiguity

### Charge
- if user provides charge, use it
- otherwise default to `CHARGE 0`

### Multiplicity / UKS
- obvious closed-shell main-group molecule: `MULTIPLICITY 1`, no UKS
- isolated radical / odd electron count / magnetic atom present: enable UKS and infer likely multiplicity
- transition-metal systems with unknown spin: set UKS and choose a conservative high-spin initial guess only when chemically reasonable; attach warning

If spin cannot be safely inferred:
- do not pretend certainty
- emit `ambiguity_warning: spin_state_uncertain`

## 11. Geometry constraints ambiguity

If adsorption/slab optimization is requested but no constraints are mentioned:
- freeze bottom slab layer(s) by default only when the slab is clearly a surface model
- otherwise leave all atoms free and note the choice

If the user asks for a bulk relaxation:
- do not freeze atoms unless explicitly requested

## 12. MD ambiguity

If user asks for MD but omits ensemble/temperature/time:
- default ensemble: `NVT`
- default temperature: 300 K
- default timestep: 0.5 fs if H present, otherwise 1.0 fs
- default steps: 5000 for a short test run
- annotate that this is a short equilibration/testing trajectory, not a production MD campaign

## 13. Adsorption-energy ambiguity

If user asks for adsorption energy but does not specify protocol:
- use:
  - `E_ads = E(total) - E(slab) - E(adsorbate)`
- keep same XC, cutoff, basis, pseudopotential family, cell convention, and k-point logic across all calculations
- if charged or spin-polarized fragments are involved, warn that a more careful protocol may be needed

## 14. Escalation policy

The skill should **auto-decide silently** only when the choice is standard and low-risk.

The skill should **emit a warning but still proceed** when:
- metallic vs insulating character is uncertain
- spin state of transition-metal system is uncertain
- surface constraints are inferred automatically
- k-point mesh is heuristic
- exact transition-metal pseudopotential entry needs library resolution

The skill should **refuse to over-assume and require explicit user input** only when:
- multiple chemically distinct structures could match the request
- TS/NEB path is not defined
- charge/spin choices would dominate the scientific conclusion
- requested method is beyond the project’s supported template space

## 15. Normalized-output fields the skill should populate

When automatic decisions are made, record them explicitly, for example:

```json
{
  "inferred_task": "geo_opt",
  "inferred_system_class": "2d_slab",
  "inferred_periodicity": "xy",
  "inferred_xc": "PBE",
  "inferred_basis": "DZVP-MOLOPT-SR-GTH",
  "inferred_potential_family": "GTH-PBE",
  "inferred_scf_mode": "diagonalization",
  "inferred_kpoints": [6, 6, 1],
  "inferred_dispersion": true,
  "warnings": [
    "kpoint_mesh_is_heuristic",
    "spin_state_uncertain"
  ]
}
```

## 16. Final style rule

When ambiguity exists, prefer:
- standard over exotic
- reversible defaults over aggressive assumptions
- warnings over false certainty
- reproducible explicit notes over hidden heuristics
