# obscure-package-master

A tool for decreasing coding hallucinations when working with obscure or poorly-known Python packages by providing a deterministic, versioned mirror of package repositories with a built-in coordinate system.

This project allows an AI agent to "ground" its understanding of an API by reading the actual source code instead of relying on training data.

## How it works

1.  **Grep Map Generation:** The `scripts/generate_mirror.py` script downloads any Python package from PyPI and uses AST parsing to create a "grep map".
2.  **Coordinate System:** The map identifies every class and function, its full signature, first-line docstring, and exact line ranges.
3.  **Deterministic Mirror:** The script creates a local skill for that specific package version in `.skills/`, including a full copy of the source code in `references/`.
4.  **Zero Hallucination:** When the agent needs to use the package, it refers to the grep map and performs surgical `read_file` calls on the local source.

## Installation

To use this as a global skill:

1.  Clone this repository.
2.  Copy the `SKILL.md` and `scripts/` directory to your agent's global skills folder (e.g., `~/.cursor/skills/` or similar):
    ```bash
    mkdir -p ~/.skills/obscure-package-master/scripts
    cp SKILL.md ~/.skills/obscure-package-master/
    cp scripts/generate_mirror.py ~/.skills/obscure-package-master/scripts/
    ```

## Usage

When an agent's uncertainty with a package API is > 5%, it should trigger this skill:

```bash
python3 ~/.skills/obscure-package-master/scripts/generate_mirror.py <package_name> <version>
```

Example:
```bash
python3 ~/.skills/obscure-package-master/scripts/generate_mirror.py pydantic 2.0.0
```

This will create a new local skill at `.skills/pydantic-2.0.0/` which the agent can then use for grounded API exploration.

## Core Principles

- **No LLM interpretation:** The map is built purely via static analysis (AST).
- **Dense references:** Focus on exact line ranges for surgical reads.
- **Strictly source-based:** If it's not in the code, it's not in the skill.
