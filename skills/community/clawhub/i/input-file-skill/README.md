# CP2K Input Generator

A skill for OpenClaw that helps generate CP2K input drafts from natural language requests and local structure inputs.

## Overview

This skill helps users create runnable CP2K input files for molecular simulations without needing to memorize complex input syntax. Simply describe what you want to simulate, and the skill will generate an appropriate input file.

The current uploaded skill package is intentionally scoped to a local-only workflow. It does not perform automatic retrieval from external structure databases such as PubChem or Materials Project. Those resources may still be referenced in the documentation as manual suggestions for obtaining structures.

## Features

- **Natural Language Interface**: Describe your simulation in plain English
- **Structure File Support**: Currently supports local .xyz structure files
- **Smart Defaults**: Applies conservative, physically sound default settings
- **Multiple Calculation Types**:
  - Geometry Optimization (GEO-OPT)
  - Single Point Energy (ENERGY)
  - Molecular Dynamics (MD)
  - Transition State Search

## Supported Methods

- **Functionals**: PBE, PBE0, BLYP, BP86, etc.
- **Basis Sets**: DZVP-MOLOPT-GTH, TZVP-MOLOPT-GTH, etc.
- **Pseudopotentials**: GTH (Goedecker-Teter-Hutter)

## Usage Examples

### Example 1: Geometry Optimization
```
Generate a CP2K input file for water molecule geometry optimization using PBE functional.
```

### Example 2: Molecular Dynamics
```
Create an MD input file for ethanol at 300K with 5000 steps and 0.5 fs timestep.
```

### Example 3: With Structure File
```
I uploaded benzene.xyz. Please generate a CP2K input for single point energy calculation.
```

## Output

The skill generates:
1. A CP2K input draft (.inp)
2. An explanation of applied defaults, assumptions, and current limitations

## Directory Structure

```
cp2k-input-generator/
├── SKILL.md              # Skill definition and instructions
├── README.md             # This file
├── assets/               # Static assets and report assets
└── references/           # Reference documentation used for defaults and policy
```

## Requirements

- OpenClaw with skill support
- No Python runtime scripts are included in the uploaded skill package

Because the uploaded version excludes the original Python helper scripts, the current package should be understood as a documentation- and reference-driven skill definition rather than a standalone local Python tool.

## Installation

## Default Settings

The skill applies the following safe defaults:

| Parameter | Default Value         |
|-----------|-----------------------|
| Functional | PBE                   |
| Basis Set | DZVP-MOLOPT-GTH       |
| Pseudopotential | GTH-PBE               |
| Cutoff | 400 Ry                |
| Poisson Solver | MT (for non-periodic) |
| Optimizer | BFGS (for GEO-OPT)    |

## Limitations

- Supports local .xyz structures only in the current documented workflow
- Does not automatically retrieve structures from external databases
- Does not perform convergence validation
- Does not optimize method choices for special systems (metals, excited states, etc.)
- Users should verify all generated settings before production runs

## Contributing

Contributions are welcome! Please ensure:
- All defaults are physically sound and conservative
- Generated inputs are well-commented
- Documentation is clear and accurate

## License

MIT License - See LICENSE file for details

## References

- CP2K Official Website
- CP2K Input Reference
- MOLOPT Basis Sets

## Author

Created for OpenClaw - Making molecular simulations accessible.

## Version History

- **1.0.0** - Initial release with local-structure, documentation-driven CP2K input generation scope
