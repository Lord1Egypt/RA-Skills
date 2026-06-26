# Lean Language Specification

*   **Version**: Primarily supports **Lean 4** (specifically `leanprover/lean4:v4.28.0` for generated scaffolds).
*   **Standard Library**: `Mathlib4` is mandatory for most theorems.
*   **Common Tactics**: `aesop`, `simp`, `linarith`, `ring`.
*   **Preflight**: After download, run `python3 scripts/check_theorem_env.py <workspace>` to validate the toolchain, required skills, and initial `lake` build.
*   **Coding Standard**:
    *   Use `PascalCase` for types and `camelCase` for terms/lemmas.
    *   Avoid long proofs in a single `by` block; use `have` for intermediate steps.
