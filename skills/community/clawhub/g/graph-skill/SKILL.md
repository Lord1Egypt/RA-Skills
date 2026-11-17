---
name: graph
description: Execute coding work as a cached dependency graph with local quality gates, parallel agents, localized retries, resume support, token telemetry, and an interactive report. Use for /graph requests.
homepage: https://github.com/gwaghmar/graph
metadata:
  openclaw:
    requires:
      binaries: ["python3"]
---

# Graph execution

If `.graph/graph.py` is missing from the workspace, bootstrap the shared runtime first with `npx graph-skill install --target openclaw`.

Sizing: estimate F = files to change, D = open design decisions, R = cross-cutting risk (auth, shared utilities, public APIs, migrations). S (F ≤ 1, D = 0, no R): one implementation node + `quality`, no extra agents. M (F 2–4 or D = 1, no R): 2–3 nodes, plan inline, at most one reviewer agent. L (F ≥ 5, D ≥ 2, or R): full protocol with planner, 2–6 workers (one per independent file-scope cluster), and reviewer. Never spawn more workers than independent clusters. State the tier and F/D/R in one line before building the graph. The full protocol below is for M and L.

1. Initialize with `python3 .graph/graph.py init "<task>" --host openclaw`. For `/graph --resume`, run `python3 .graph/graph.py resume` and continue the returned run.
2. Record planner, plan-review, implementation, validation, and synthesis nodes using `.graph/graph.py node`. Each update prints a live ASCII graph and refreshes the local HTML graph — both rendered locally, no model tokens. Use `.graph/graph.py tree <run>` to reprint it on demand.
3. Before a model call, check `.graph/graph.py cache-get <run> <node> --files <relevant-files>`. A cache hit replaces that model call.
4. Split only independent work into bounded, non-overlapping agents.
5. Run `.graph/graph.py quality <run>` before reviewer agents. Prefer tests, lint, type checking, and other deterministic checks over extra model calls.
6. If a node fails, use `.graph/graph.py retry-plan <run> --include-dependents` and rerun only listed nodes. Maximum two retries per node.
7. Store successful reusable node output with `.graph/graph.py cache-put`.
8. Record token usage only when OpenClaw exposes it. Do not estimate unless clearly marked.
9. Finish with `.graph/graph.py finish <run> --status complete`. It prints the final run summary (node graph, checks, files, retries, cache hits, duration, report path); include it verbatim in your reply along with the implementation result.
10. Only when explicitly requested, commit through `.graph/graph.py commit <run> --yes`.

Never push, deploy, or create a PR without explicit instruction.
