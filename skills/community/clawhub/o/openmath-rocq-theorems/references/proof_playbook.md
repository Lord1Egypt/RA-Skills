# OpenMath Rocq Proof Playbook

This note is the standalone fallback workflow for proving a downloaded OpenMath Rocq theorem workspace when no companion Rocq skills are available.

## Preflight First

Run the local environment checks before editing proof terms:

```bash
rocq --version
rocq -e 'From Stdlib Require Import Arith. Check Nat.add_comm.'
dune --version
opam list rocq-prover
```

If the project has an `opam` file, install missing dependencies before proving:

```bash
opam install . --deps-only
```

Then confirm the workspace builds in its initial state:

```bash
dune build
```

## What To Read First

After download, read these files in order:

1. `README.md`
2. `theorem.json`
3. The generated theorem `.v` file
4. `dune-project`, `dune`, or `_CoqProject` files if present
5. Any project `opam` file

Use them to identify the target theorem, the expected libraries, and the build entrypoints.

## Minimal Proof Loop

Follow this loop even when no companion skills are installed:

1. Open the target `.v` file and identify the main theorem plus any `admit` or `Admitted.` markers.
2. Write one proof command or tactic at a time.
3. After each meaningful change, re-run `dune build` or `rocq compile <file>.v`.
4. Stop at the first real error and fix that error before writing more proof text.
5. Prefer the hardest blocked subgoal first; leave unrelated helper lemmas for later.
6. Before finishing, remove every `admit` and `Admitted.` and rerun `dune build`.

## Basic Tactic Starting Points

For many OpenMath-style Rocq theorems, start with a small set of predictable tools:

- `intros`
- `destruct`
- `induction`
- `simpl`
- `rewrite`
- `reflexivity`
- `apply`
- `exact`

For arithmetic-heavy goals, first check whether the required lemma is already in `Stdlib` or the imported libraries before inventing a custom helper.

## Submission Readiness Checklist

Before using `openmath-submit-theorem`, confirm all of the following:

- `dune build` succeeds, or the project-specific compile command succeeds
- No `admit` or `Admitted.` remains
- The theorem statement was not weakened or changed
- The final proof is saved in the generated theorem file
