# Rocq Companion Skills

These companion skills are optional enhancements. `openmath-rocq-theorem` must still be usable when they are absent.

Use a companion skill only if it is already installed in the active agent, or if you are working from the full repository and have explicitly reviewed and installed it into a deliberate project-local skills directory such as `.codex/skills` or `.claude/skills`.

## Common Companions

- `rocq-proof`: Use when you need detailed tactic guidance, one-step-at-a-time proof discipline, or Ltac/Ltac2 help while proving the theorem itself.
- `rocq-ssreflect`: Use when the workspace depends on MathComp or the proof style is clearly SSReflect-oriented.
- `rocq-setup`: Use when the Rocq toolchain, opam switch, editor integration, or environment activation is broken or unclear.
- `rocq-dune`: Use when `dune build` fails because of project layout, dune stanzas, `_CoqProject`, or module path issues.

## Optional Companions

- `rocq-mwe`: Use when you need to shrink a failing example to a small reproducible case.
- `rocq-bisect`: Use when a theorem or build started failing after a Rocq version change and you suspect a regression.
- `rocq-extraction`: Use only if the work expands beyond proof completion into extraction workflows.
- `rocq-mathcomp-build`: Use when MathComp packages or related opam dependencies are the primary blocker.

## Decision Rule

- If the blocker is environment or switching: prefer `rocq-setup`.
- If the blocker is project build wiring: prefer `rocq-dune`.
- If the blocker is proof search or tactic choice: prefer `rocq-proof`.
- If the theorem is MathComp-heavy or SSReflect-style: add `rocq-ssreflect`.

If none of these companion skills are installed, continue with the local workflow in `openmath-rocq-theorem` and keep the task scoped to the theorem workspace.
