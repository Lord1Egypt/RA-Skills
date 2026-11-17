---
name: omega-architect-formal-proof
description: >
  Formal theorem proving with omega-architect: install the CLI, configure a Lean 4
  toolchain and an LLM backend, and drive the generate -> compile -> verify loop
  (`omega prove`), including strategy modes, budgets and no-LLM smoke tests.
category: research
tags: [lean4, theorem-proving, formal-verification, proof-search, mcts]
author: Li Shen
version: 1.0.3
permissions: [shell, file_read, file_write, network]
metadata:
  hermes:
    homepage: https://github.com/diamond2nv/omega-architect
    tags: [lean4, theorem-proving, formal-verification, proof-search, mcts, ai4s]
    related_skills: [exo-suite-linkage]
---

# omega-architect — Formal Proof Workflow

> **Part of the Exo suite** — literature (`hfpclawer`) → experiments (`expflow-pde`) → proofs
> (`omega-architect`). Three independent CLIs that meet through **files and CLI calls**, never imports.
> Entry skill: `exo-suite-linkage` (wiring, cost tiers **low → medium → high**, degradation ladder).
> Install: `uv tool install hfpclawer` · `uv tool install expflow-pde` ·
> `uv tool install "omega-architect @ git+https://github.com/diamond2nv/omega-architect@v0.2.3"`

Drive Ω-Architect (`omega`) to turn a **Lean 4 theorem header** into a machine-checked proof:
generate candidates with an LLM, compile them with a real Lean toolchain (CompileGate), and
keep only what the compiler accepts.

> **Cost is real.** Generation spends LLM tokens and every candidate is compiled by Lean.
> This is the most expensive stage of the AI-for-Science toolchain — bound each run with
> `--samples`, `--rounds`, `--timeout` and the budget section of `omega.toml`.
> A **local GPU backend** (Ollama / vLLM) is the lever that moves spend from API tokens to
> local compute; how much it saves depends on model strength and workload and must be
> measured, not assumed.

## When to use

- A statement must be *proved*, not argued: invariants, conservation laws, bounds, type-level facts.
- A formula-registry entry needs machine-checked backing (see `exo-suite-linkage`).
- You want proof search (DFS / beam / hybrid) over candidate tactics with real compile checks.

## Prerequisites

- **Python ≥ 3.11**
- **Lean 4 toolchain** — `lean` (and ideally `lake`) on `PATH`: install
  [elan](https://github.com/leanprover/elan) plus a Lean 4 release. Without Lean, T2/CompileGate
  is unavailable and nothing is compiler-verified.
- **An LLM backend** — a remote API key (default model `deepseek/deepseek-v4-flash`) or a local
  Ollama / vLLM model passed via `--model`. The local backend is what reduces API token spend;
  its effectiveness is workload-dependent and should be tuned by measurement.

## Install

```bash
# 1) Recommended — uv tool, pinned to a tag (isolated environment, `omega` on PATH)
uv tool install "omega-architect @ git+https://github.com/diamond2nv/omega-architect@v0.2.3"

# 2) From the wheel attached to the GitHub release
uv tool install "https://github.com/diamond2nv/omega-architect/releases/download/v0.2.3/omega_architect-0.2.3-py3-none-any.whl"

# 3) Development checkout
git clone https://github.com/diamond2nv/omega-architect && cd omega-architect
uv pip install -e ".[all]"     # or: pip install -e .

# 4) Run it without installing (package name and entry point differ: --from)
# pin the version — `uvx`/`uv tool run` reuse an installed tool env (may run an older
# release), and an unpinned launch is a supply-chain (rug-pull) risk
uvx --from "git+https://github.com/diamond2nv/omega-architect@v0.2.3" omega --help

# 5) pipx — classic CLI installer (needs a recent pipx; 1.0.0 cannot parse git specs)
pipx install "git+https://github.com/diamond2nv/omega-architect@v0.2.3"
```

## Quick start

```bash
omega init                     # write omega.toml (--skip-lean = configure without Lean discovery)
omega status                   # which models are reachable + routing history
omega prove 'theorem add_zero (n : ℕ) : n + 0 = n := by'    # generate -> compile -> verified
```

`prove` takes a **Lean theorem header** (statement ending in `:= by`), not prose:

```bash
omega prove 'theorem my_bound (x : ℝ) (h : 0 ≤ x) : 0 ≤ x^2 := by' \
  --mode auto --samples 4 --rounds 2 --timeout 120 --imports 'import Mathlib'
```

## Command reference

| Command | Purpose | Key flags |
|:--|:--|:--|
| `omega init` | Generate `omega.toml` | `--skip-lean`, `--output`, `--force` |
| `omega status` | Model-router health + routing history | — |
| `omega route` | Preview the ModeRouter decision for a theorem | theorem header |
| `omega prove` | Prove one theorem: generate → compile → verified | `--mode auto\|dfs\|beam\|hybrid`, `--model`, `--samples`, `--rounds`, `--timeout`, `--imports` |
| `omega prove-batch` | Batch proving (allocate → prove → aggregate) | dataset |
| `omega run` | Autonomous proof search for a research goal | — |
| `omega bench` / `omega benchmark` | Theorem benchmark (T2 pass rate) / hardware tok/s | dataset |

## What the loop actually does

1. **Generate** — the LLM (or a local model) proposes a proof body for the theorem header.
2. **Compile** — CompileGate runs the real Lean toolchain on the candidate (`--imports`,
   default `import Mathlib`); candidates that do not compile are discarded.
3. **Verify** — only compiler-accepted proofs count as verified; error memory and the error
   classifier feed the next round (`--rounds`).
4. **Route** — ModeRouter picks the strategy (`auto`), or you pin one (`dfs` / `beam` / `hybrid`).

Sampling and rounds multiply cost: `--samples × --rounds` candidates, each compiled. Start at
`--samples 1 --rounds 1` to validate the plumbing, then raise.

## Working without an API key

```bash
omega init --skip-lean                                  # configuration only
python scripts/mcts_lean_smoke.py --generator fixed     # Lean + search + diagnosis, no LLM
```

`--generator fixed` cycles a built-in tactic list: it needs a working Lean toolchain, not an LLM
key — use it to verify the toolchain before spending tokens. For real proofs without a remote key,
point `--model` at a local backend (Ollama / vLLM).

## Pitfalls

1. **Prose statements do not work** — `prove` expects a Lean header (`theorem … := by`).
2. **No Lean ⇒ no verification** — generation may still run, but nothing is compiler-checked;
   check `omega status` and `lean --version` before interpreting results.
3. **Unbounded sampling is the usual budget blow-up.**
4. **`import Mathlib` is the default import set** — a narrower set compiles much faster; use
   `--imports ''` for core-only statements.
5. **Alpha software** — CLI and config keys can change between versions; pin a tag.

## Verification checklist

- [ ] `omega status` shows the intended model reachable
- [ ] `lean --version` works before any "unverified" result is interpreted
- [ ] Each proof artifact keeps its statement, proof body and import set together
- [ ] Run metadata recorded: model, `--samples`, `--rounds`, `--timeout`
- [ ] Only compiler-accepted proofs are reported as verified
