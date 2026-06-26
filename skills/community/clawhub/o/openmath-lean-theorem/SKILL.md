---
name: openmath-lean-theorem
description: Configures Lean environments, installs external proof skills, runs preflight checks, and guides the workflow for proving downloaded OpenMath Lean theorems locally.
version: v1.0.2
requirements:
  commands:
    - python3
    - lean
    - lake
    - elan
  environment_variables:
    - OPENMATH_SKILL_DIRS
    - OPENMATH_LEAN_SKILL_INSTALL_DIR
    - OPENMATH_LEAN_SKILL_REPO_URL
side_effects:
  - May clone the reviewed leanprover/skills repo and copy missing Lean skills into an explicit install dir only when preflight is run with --auto-install-skills and --install-dir (or OPENMATH_LEAN_SKILL_INSTALL_DIR)
---

# OpenMath Lean Theorem

## Instructions

Set up the Lean proving environment, validate toolchains, and prove downloaded OpenMath theorems locally. Assumes the theorem workspace was already created by the `openmath-open-theorem` skill.

This skill does not run benchmark providers, prompt-based agent comparisons, or trace persistence workflows. Those belong to the separate `openmath-lean-benchmark` skill.

### Workflow checklist

- [ ] **Environment**: Verify `lean`, `lake`, and `elan` are installed and match the workspace `lean-toolchain`.
- [ ] **External skills**: Install required Lean proof skills from [leanprover/skills](https://github.com/leanprover/skills). Preferred manual install:
  ```bash
  npx leanprover-skills install lean-proof
  npx leanprover-skills install mathlib-build
  ```
  If you use preflight auto-install, first review the upstream repo and then pass an explicit target such as `--install-dir .codex/skills` or `--install-dir .claude/skills` so the write location is deliberate. Do not run auto-install without an explicit install dir.
- [ ] **Preflight**: Run `python3 scripts/check_theorem_env.py <workspace>` (see [references/preflight.md](references/preflight.md)).
- [ ] **Prove**: Use `lean-proof` / `mathlib-build` skills to complete the proof. See [references/proof_playbook.md](references/proof_playbook.md) for the OpenMath-specific proving loop.
- [ ] **Verify**: Confirm `lake build -q --log-level=info` passes and no `sorry` remains.
- [ ] **Submit**: Use the `openmath-submit-theorem` skill to hash and submit the proof.

### Scripts

| Script | Command | Use when |
|--------|---------|----------|
| Preflight check | `python3 scripts/check_theorem_env.py <workspace>` | After download, before proving; validates toolchain, required skills, and initial build. |
| Preflight (auto) | `python3 scripts/check_theorem_env.py <workspace> --auto-install-skills --install-dir <path>` | Auto-install missing Lean skills during preflight into an explicit skills dir. |

### Notes

- **Lean version**: Scaffolds pin `leanprover/lean4:v4.28.0` and `mathlib4 v4.28.0` (set by `openmath-open-theorem`'s `download_theorem.py`).
- **External skills**: Not bundled. Required: `lean-proof`, `mathlib-build`. Optional: `lean-mwe`, `lean-bisect`, `nightly-testing`, `mathlib-review`, `lean-setup`. Manual `npx leanprover-skills install ...` is preferred; preflight auto-install additionally requires `git`, explicit user approval, and an explicit install dir.
- **Benchmarking**: For agent evaluation, prompt comparison, or regression testing on the bundled Lean benchmark corpus, use the separate `openmath-lean-benchmark` skill.

## References

Load when needed (one level from this file):

- **[references/preflight.md](references/preflight.md)** — Lean preflight command, skill checks, and initial build loop.
- **[references/proof_playbook.md](references/proof_playbook.md)** — Step-by-step workflow for proving a downloaded Lean theorem locally.
- **[references/languages.md](references/languages.md)** — Lean version and standard library.
