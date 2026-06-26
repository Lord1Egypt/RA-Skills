# OpenMath Lean Proof Playbook

This note is for the step after you have already downloaded a theorem workspace with:

```bash
python3 scripts/download_theorem.py <id>
```

It is not a replacement for `lean-proof`; it narrows that methodology to the OpenMath scaffold you get from `download_theorem.py`.

## Preflight First

Before proving anything, run the post-download preflight:

```bash
python3 scripts/check_theorem_env.py <workspace>
```

This checks the local Lean toolchain, validates that required skills such as `lean-proof` and `mathlib-build` are installed, and runs the initial build loop. If required skills are missing, use:

```bash
npx leanprover-skills install lean-proof
npx leanprover-skills install mathlib-build
```

Or, if you want preflight to install the missing skills for you, use an explicit target directory:

```bash
python3 scripts/check_theorem_env.py <workspace> --auto-install-skills --install-dir .codex/skills
```

The auto-install path clones `https://github.com/leanprover/skills.git` and copies the missing skill directories into the selected skills directory. Review the upstream repo first, and do not use auto-install without an explicit install dir.

## What To Read First

After download, read these files in order:

1. `README.md`
2. `theorem.json`
3. The generated theorem `.lean` file
4. `lakefile.lean`
5. `lean-toolchain`

Use them for different purposes:

- `README.md`: human summary, theorem id, next steps
- `theorem.json`: raw payload and exact platform metadata
- theorem `.lean`: the actual target statement and imports
- `lakefile.lean`: dependencies, especially Mathlib
- `lean-toolchain`: exact Lean version expected by the scaffold

## Default Build Loop

Before proving anything, make sure the workspace builds in its initial state.

If the generated `lakefile.lean` includes a mathlib dependency, fetch the cache first:

```bash
lake exe cache get
```

Then build:

```bash
lake build -q --log-level=info
```

If the project does not depend on mathlib (no `import Mathlib` in the theorem file), skip `lake exe cache get` and build directly.

If you only want to typecheck one file while iterating, use:

```bash
lake env lean path/to/TheoremFile.lean
```

Use `lake build -q --log-level=info` again before declaring the proof finished.

## Default Proof Loop

1. Open the generated theorem file.
2. Identify the main target theorem and any existing `sorry`.
3. Work on the hardest target first.
4. Replace one small step at a time.
5. Re-run Lean after each meaningful change.
6. Stop and fix the first real error before writing more proof text.
7. When the theorem works, simplify the proof immediately.

This should be combined with the stricter methodology in `lean-proof`.

## What Usually Works Best

For OpenMath-style Lean problems, start with:

- `simp`
- `aesop`
- `rfl`
- `rw [...]`
- `constructor`
- `cases`
- `induction`
- `linarith`
- `ring`
- `norm_num`

If the theorem looks algebraic or arithmetic, try `ring`, `linarith`, or `norm_num` early.
If it looks structural, try `cases`, `induction`, `constructor`, and local helper lemmas.

## Helper Lemma Strategy

Do not fully polish helper lemmas before the main theorem works.

Preferred approach:

1. Move helper facts earlier in the file.
2. Leave helper lemmas as `sorry` if they are not the current bottleneck.
3. Use the main theorem to tell you which helper statement is actually missing.
4. Only then go back and prove the required helper.

This is especially useful when the OpenMath statement is larger than it first appears.

## Searching For Useful Facts

When blocked, search locally before guessing.

- Search the theorem file and generated workspace:

```bash
rg -n "keyword_or_symbol" .
```

- Inspect imported names directly inside Lean with commands such as:

```lean
#check someLemma
#check Nat.succ_eq_add_one
```

- If a proof fails because of a dependency or environment issue rather than theorem logic, switch tools:
  - `lean-mwe`: minimize the failing case
  - `lean-bisect`: isolate a Lean regression
  - `nightly-testing`: understand nightly or toolchain breakage

## Build And Submission Readiness Checklist

Before using `openmath-submit-theorem`, confirm all of the following:

- No `sorry` remains in the theorem file
- `lake build -q --log-level=info` succeeds
- The final proof is saved in the generated theorem `.lean` file
- The theorem statement was not weakened or changed
- The proof does not depend on temporary debug commands or experiments

## When To Escalate Beyond Proof Work

Use other Lean/Mathlib skills only when the task expands beyond local proving:

- `mathlib-build`: project validation and rebuild discipline
- `mathlib-review`: checking whether an extracted fix is acceptable upstream
- `mathlib-pr`: preparing a Mathlib contribution
- `lean-pr`: preparing a Lean core contribution
- `lean-setup`: fixing a broken Lean repository clone or local toolchain link setup

For a normal downloaded OpenMath theorem, `lean-proof` plus `mathlib-build` should be the default pair.
