# Rocq Language Specification

*   **Version**: OpenMath Rocq workspaces target **Rocq 9.1.0** (current stable, September 2025) with Platform 2025.08.2. Legacy Coq 8.x is supported by older projects.
*   **Standard Library**: Use `From Stdlib Require Import` for Rocq 9.x. The legacy `From Coq Require Import` still works with a deprecation warning.
*   **Libraries**: Stdlib, `Mathematical Components` (MathComp) when required by the theorem.
*   **Proof Style**: SSReflect style preferred. Use the `rocq-proof` and `rocq-ssreflect` skills.
*   **Preflight**: Verify environment before proving:
    ```bash
    rocq --version
    rocq -e 'From Stdlib Require Import Arith. Check Nat.add_comm.'
    dune --version
    opam list rocq-prover
    ```
*   **Companion skills**: Rocq proof helper skills such as `rocq-proof`, `rocq-ssreflect`, `rocq-setup`, and `rocq-dune` are separate sibling skills in the full repository. They may not be present in an isolated `openmath-rocq-theorem` skill package; use them only when they are already installed or when you have explicitly reviewed and installed them from the full repo.
