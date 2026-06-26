---
name: openmath-rocq-theorem
description: Configures Rocq environments, runs preflight checks, and guides the proving workflow for OpenMath Rocq theorems. Use when the user wants to set up Rocq tooling, prove a downloaded OpenMath theorem in Rocq/Coq, or verify and submit a Rocq proof.
version: v1.0.2
requirements:
  commands:
    - rocq or coqc
    - dune
    - opam
side_effects:
  - Runs local Rocq, dune, and opam commands in the theorem workspace
---

# OpenMath Rocq Theorem

## Instructions

Set up the Rocq proving environment, validate opam switches, and prove downloaded OpenMath theorems. Assumes the theorem workspace was already created by the `openmath-open-theorem` skill.

This skill package is self-contained: it consists of this `SKILL.md` plus the local `references/` files in this directory. It does not bundle or install sibling `rocq-*` companion skills.

### Workflow checklist

- [ ] **Environment**: Verify `rocq` (or `coqc`), `dune`, and `opam` are installed and the active opam switch matches the project's `.opam-switch` or `opam` file. See the `rocq-setup` skill for installation and switch management.
- [ ] **Companion skills**: If companion Rocq skills such as `rocq-proof`, `rocq-ssreflect`, `rocq-setup`, or `rocq-dune` are already installed in the active agent, use them. See [references/companions.md](references/companions.md) for when each one is useful. This isolated package does not include their code and does not install them for you.
- [ ] **Preflight**: Confirm the environment is healthy before proving:

  ```bash
  rocq --version
  rocq -e 'From Stdlib Require Import Arith. Check Nat.add_comm.'
  dune --version
  opam list rocq-prover
  ```

- [ ] **Prove**: Follow the minimal Rocq proving loop in [references/proof_playbook.md](references/proof_playbook.md). If `rocq-proof` or `rocq-ssreflect` is already installed, use them as companion guidance; otherwise continue with the local workflow in this skill.
- [ ] **Verify**: Confirm `dune build` (or `rocq compile <file>.v`) passes and no `admit` or `Admitted.` remains:

  ```bash
  dune build
  grep -rn 'admit\|Admitted\.' *.v
  ```

- [ ] **Submit**: Use the `openmath-submit-theorem` skill to hash and submit the proof.

### Scripts

| Action | Command | Use when |
|--------|---------|----------|
| Check Rocq version | `rocq --version` | Verify the active opam switch has the expected Rocq release. |
| Verify stdlib loads | `rocq -e 'From Stdlib Require Import Arith. Check Nat.add_comm.'` | Confirm the standard library is reachable before proving. |
| Build project | `dune build` | After each proof attempt; must exit 0 with no errors. |
| Compile single file | `rocq compile <file>.v` | Quick check on a single `.v` file without a full dune build. |
| Check for admits | `grep -rn 'admit\|Admitted\.' *.v` | Before submitting; must return no matches. |
| Install opam deps | `opam install . --deps-only` | After cloning or changing the project `opam` file. |

### Notes

- **Rocq version**: OpenMath Rocq workspaces target Rocq 9.1.0 (current stable, September 2025) with Platform 2025.08.2.
- **Companion skills**: `rocq-proof` (proving methodology, tactic reference, Ltac2), `rocq-ssreflect` (SSReflect / MathComp style), `rocq-setup` (opam, toolchain, editor), and `rocq-dune` (build system, `_CoqProject`, dune stanzas) are useful companions when already installed. Optional companions: `rocq-mwe`, `rocq-bisect`, `rocq-extraction`, `rocq-mathcomp-build`.
- **Install boundary**: This isolated skill should not instruct copying unseen `rocq-*` directories into `~/.agents/skills` or any other global skills directory. If you are installing from the full repository, review the companion skill folders there and copy them only into a deliberate project-local skills directory such as `.codex/skills` or `.claude/skills`.
- **Stdlib prefix**: Use `From Stdlib Require Import` for Rocq 9.x. The legacy `From Coq Require Import` still works with a deprecation warning; prefer `From Stdlib` for all new proofs.
- **Verification status**: A proof is complete only when `dune build` exits 0, no `admit` or `Admitted.` remains, and the LSP panel shows no errors or warnings.

## References

Load when needed (one level from this file):

- **[references/companions.md](references/companions.md)** — When to use optional Rocq companion skills if they are already installed.
- **[references/languages.md](references/languages.md)** — Rocq version, Stdlib prefix, libraries, and proof style.
- **[references/proof_playbook.md](references/proof_playbook.md)** — Minimal standalone proving loop for downloaded OpenMath Rocq theorem workspaces.
