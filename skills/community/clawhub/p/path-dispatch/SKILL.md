---
name: path-dispatch
description: >
  Discrete Hamiltonian task dispatch for multi-hop workflows.
  Maps task dependencies as a graph, precomputes reachability matrices,
  and solves constrained path queries under budget. Enables LLMs to decompose
  and sequence 10-1000+ step tasks without losing state.
env:
   PATH_DISPATCH_NO_CACHE      
---

# Path-Dispatch: Discrete Hamiltonian Task Dispatch

## Problem

Large workflows (API integrations, data pipelines, test suites) often span 10–100+ logical steps.

**Why this breaks LLMs:**
- Context limits force batching → loses intermediate state
- Attention is local → can't track distant dependencies
- Token budget forces trade-offs → fewer reasoning steps per hop

**What we need:**
> "Given current task and target, what is the valid next task under remaining budget?"

Not "what are all reachable tasks?" but "what doesn't lead to a dead end?"

---

## Core Model: Discrete Hamiltonian System

### Mathematical Foundation

Define a **discrete Hamiltonian system** on task space:

| Concept | Mathematical Object | Role |
|---|---|---|
| Task space | Nodes $V$ | Workflow tasks/objects |
| Dependencies | Adjacency matrix $A$ | Direct task → task edges |
| "Time" (budget) | Steps remaining $k$ | Reachability horizon |
| Value function | $R[k][i][j]$ | Can reach $j$ from $i$ in $\leq k$ steps? |
| Discrete HJ equation | $R[k] = R[k-1] \vee A^{k}$ | Precomputable reachability closure |
| Optimal policy | `next_hops(v, T, k)` | Single step along viable path |

### Key Insight: Hamilton-Jacobi Analogy

In continuous Hamiltonian mechanics, value functions satisfy the HJ equation to minimize cost.

Here:
- **Discrete HJ equation:** $R[k] = \bigvee_{i=0}^{k} A^i$ (reachability in $\leq k$ steps)
- **Policy:** `next_hops(current, target, budget)` = neighbors that **still reach target** with remaining budget
- **Dispatch:** Follow this policy at each step → no dead ends

### Precomputation Cost

| Phase | Complexity | When |
|---|---|---|
| Build graph | $O(n)$ | Parse triples once |
| Compute $R[k]$ | $O(n^4)$ worst case | Once per workflow |
| Single `next_hops` query | $O(n)$ | Every decision point |

**In practice:** Precompute once (seconds), query thousands of times (milliseconds).

---

## Hypergraph Normalization

Real workflows often have **multi-source, multi-sink tasks**:

```
Design & Spec  ──→  {Impl_A, Impl_B}  ──→  Integration
```

This is a **hyperedge**: one logical relation but 2×2 = 4 binary sub-edges.

### Solution: Virtual Nodes

Transform every triple into a **binary 2-step** chain via virtual node:

**Original triple:**
```
<<{[src1, src2], process, [dst1, dst2]}.
```

**Normalized form (inside graph):**
```
src1 ──→ __virtual_rel__ ──→ dst1
src2 ──→ __virtual_rel__ ──→ dst2
```

**Result:**
- One logical hop = two physical steps
- All edges are now binary
- Hyperedge **fan-in and fan-out** is transparent to the algorithm

**From LLM's perspective:**
```
next_hops(design, deploy, logical_budget=3)
→ [{impl_A, impl_B}]   # parallel dispatch set
```

---

## Input Format

Triples in markdown (compatible with `narrative-topology`):

```markdown
# Task Dependencies

<<{auth_service, blocks, token_validator}.
<<{auth_service, blocks, rate_limiter}.
<<{token_validator, blocks, user_db}.
<<{rate_limiter, blocks, redis_cache}.
<<{user_db, blocks, audit_log}.
<<{redis_cache, blocks, audit_log}.
<<{audit_log, blocks, deploy}.

# Hyperedge Example

<<{[design_doc, spec], blocks, [impl_A, impl_B]}.
<<{[impl_A, impl_B], blocks, integration_test}.
<<{integration_test, blocks, deploy}.
```

### Rules

- `<<{Subject, Predicate, Object}.` format (period-dot terminator)
- Subject/Object can be bare atoms or `[list, of, items]`
- Predicate is ignored (only structure matters)
- One triple per line
- Safely embedded in markdown

---

## Usage
### 0. Know Your Script

You are equipped with `dispatch.py`, a standalone Python script that implements all core functions.

*   **Commands**: Supports `matrix`, `path <start> <end>`, `query <current> <target> <budget>`, and `deps <node>`.
*   **Performance**: Precomputes a distance matrix and caches it (`.cache` file) to make repeated queries instantaneous. Set `PATH_DISPATCH_NO_CACHE=1` to disable caching.

### 1. Build Graph and Precompute

```bash
python dispatch.py tasks.md matrix
```

Output:
```
=== Original Nodes ===
  0  auth_service
  1  token_validator
  2  user_db
  3  audit_log
  4  deploy

=== Virtual Nodes (7) ===
  5  __rel_0__  (auth_service → token_validator)
  6  __rel_1__  (auth_service → rate_limiter)
  ...

=== Adjacency Matrix (A) ===
     0  1  2  3  4  5  6 ...
  0  0  0  0  0  0  1  1      auth_service
  1  0  0  1  0  0  0  0      token_validator
  ...

=== Transitive Closure (R*) ===
[full reachability matrix]

Nodes: 12  |  Convergence depth: 5
```

### 2. Find Shortest Path

```bash
python dispatch.py tasks.md path auth_service deploy
```

Output:
```
Shortest logical path (4 hops):
  auth_service → token_validator → user_db → audit_log → deploy
```

### 3. Query Next Valid Hops (Core Dispatch)

```bash
python dispatch.py tasks.md query auth_service deploy 4
```

Output:
```
next_hops(current=auth_service, target=deploy, logical_budget=4)
  → ['token_validator', 'rate_limiter']
```

**Interpretation:**
- From `auth_service`, both `token_validator` and `rate_limiter` are valid next steps
- Both can still reach `deploy` with ≤3 remaining hops
- Model can dispatch **either or both** (breadth-first parallel execution)

### Hyperedge Query

```bash
python dispatch.py tasks.md query design_doc deploy 3
```

Output:
```
next_hops(current=design_doc, target=deploy, logical_budget=3)
  → ['{impl_A, impl_B}']
```

**Interpretation:**
- Next logical step is a **parallel set** `{impl_A, impl_B}`
- Dispatch both simultaneously
- Reconverge when both complete

---

## Integration with LLM Dispatch

### Pattern 1: Sequential Single-Path

```
User: "Fix the auth pipeline in 4 steps max"

Model:
1. Call: query(auth_service, deploy, budget=4)
   → next = [token_validator]
2. Work on token_validator, call: query(token_validator, deploy, budget=3)
   → next = [user_db]
3. Work on user_db, call: query(user_db, deploy, budget=2)
   → next = [audit_log]
4. Work on audit_log, call: query(audit_log, deploy, budget=1)
   → next = [deploy]
5. Verify/deploy
```

### Pattern 2: Parallel Hyperedge Dispatch

```
User: "Implement features A and B independently, then integrate"

Model topology:
  feature_request → {feature_A, feature_B} → integration → release

Model:
1. query(feature_request, release, budget=4) → {feature_A, feature_B}
2. Spawn two parallel threads:
   - Thread A: query(feature_A, release, budget=3) → integration
   - Thread B: query(feature_B, release, budget=3) → integration
3. Both converge: query(integration, release, budget=1) → release
4. Verify
```

### Pattern 3: Dead-End Detection

```
Model queries: next_hops(current_node, target, remaining_budget=1)
Response: ∅ (empty set)

→ Current path is blocked
→ Model backtracks, reports blocker, or asks for help
```

### Pattern 4: Dependency Check 

```

Model queries: deps(target_node)
Response: from {source_A, source_B} via 'blocks'
from source_C via 'blocks'

→ Current plan requires target_node, but its dependencies are not all satisfied
→ Model checks which sources are already completed
→ For missing sources, either:

· Add them to the execution queue (if they are feasible),
· Or report blocker: "Cannot reach target_node because source_A is not done."

```


```example

User: "I want to start chem_topic_test, but I'm not sure what I need to do first."

Model:
python dispatch.py exam.md deps chem_topic_test
→ from math_topic_review_mistakes via 'blocks'
→ from chem_advanced_practice via 'blocks'

Model to user:
"Before starting chem_topic_test, you must complete:

1. math_topic_review_mistakes
2. chem_advanced_practice
   Please finish these first, then retry."

```
---

## API Reference

### Query: `next_hops(current, target, logical_budget)`

**Parameters:**
- `current` (str): Current task node
- `target` (str): Goal task node
- `logical_budget` (int): Remaining hops

**Returns:**
- List of valid next-task nodes
- Each element is either:
  - Single node name (binary edge)
  - Set notation `{a, b, c}` (hyperedge parallel dispatch)
- Empty list `[]` = dead end or budget exhausted

**Semantics:**
> "All tasks I can move to such that I can still reach `target` with `budget-1` remaining hops."

### Query: `path(start, end)`

**Parameters:**
- `start` (str): Starting task
- `end` (str): Goal task

**Returns:**
- Shortest logical path (list of node names)
- Hop count
- `None` if unreachable

**Use case:**
- Initial planning: "How many steps minimum?"
- Budget negotiation: "Can you do it in k steps?"

### Query: `matrix()`

**Returns:**
- Adjacency matrix A (direct edges)
- Transitive closure R* (all reachable pairs)
- Convergence depth (HJ equation termination)

**Use case:**
- Visualize task DAG
- Detect cycles (if any exist)
- Audit path existence

---

## Design Rationale

### Why Precompute Reachability?

At decision time, the model must answer: "Is this next step on a valid path?"

- **Naive:** BFS from each candidate → $O(n^2)$ per query, too slow
- **Precomputed:** Lookup $R[k]$ → $O(n)$ per query, real-time feasible

Precomputation is one-time amortized cost.

### Why Hypergraph Normalization?

Real workflows have:
- Build system spawning parallel jobs
- API calls fanning out to multiple backends
- Conditional logic (if A then {B, C} else {D})

Without normalization, these become edge-label complexity. Normalization:
- Keeps algorithm simple (binary matrix operations)
- Makes parallelism **explicit** in the graph structure
- Preserves logical hop count (virtual nodes are transparent)

### Why Not Use a Generic Graph Library?

Standard graph libs (NetworkX, igraph) are built for undirected analysis (shortest paths, clustering, centrality).

Here we need:
- Precomputed reachability across all (source, budget) pairs
- Hyperedge support as a first-class citizen
- Logical vs physical step distinction
- Real-time LLM dispatch (no I/O)

Custom minimal implementation enables all three.

---

## Workflow: From Narrative to Dispatch

### Step 1: Extract Task Relations

Use `narrative-topology` to mark task dependencies in long discussion:

```markdown
## Architecture Discussion

We need:
1. Design the schema
2. Implement backend (parallel A and B)
3. Write tests
4. Deploy

<<{schema_design, blocks, [backend_A, backend_B]}.
<<{[backend_A, backend_B], blocks, integration_test}.
<<{integration_test, blocks, deploy}.
```

### Step 2: Build Dispatch Graph

```bash
python dispatch.py architecture.md matrix
```

Review the matrices, estimate budget requirements.

### Step 3: Invoke Dispatch at Decision Points

Model starts task, calls `next_hops()` when:
- Subtask completes
- Parallel batch converges
- Unexpected blocker encountered

### Step 4: Iterative Refinement

If model hits dead ends (`next_hops() = ∅`):
- Add missing edges to the triple file
- Recompute matrix
- Re-try

This closes the feedback loop between task execution and plan verification.

---

## Example: API Integration Pipeline

### Task Graph

```
auth ──→ {cache, db} ──→ validation ──→ {log, metrics} ──→ serve
```

### Triples

```markdown
<<{auth_setup, blocks, [cache_init, db_connect]}.
<<{[cache_init, db_connect], blocks, request_validation}.
<<{request_validation, blocks, [audit_log, metrics_emit]}.
<<{[audit_log, metrics_emit], blocks, serve_response}.
```

### Dispatch Sequence

| Step | Query | Budget | Response | Action |
|---|---|---|---|---|
| 1 | `(auth_setup, serve_response, 4)` | 4 | `[cache_init, db_connect]` | Spawn 2 threads |
| 2a | `(cache_init, serve_response, 3)` | 3 | `[request_validation]` | Wait for 2b, then proceed |
| 2b | `(db_connect, serve_response, 3)` | 3 | `[request_validation]` | Wait for 2a, then proceed |
| 3 | `(request_validation, serve_response, 2)` | 2 | `{audit_log, metrics_emit}` | Spawn 2 threads |
| 4a | `(audit_log, serve_response, 1)` | 1 | `[serve_response]` | Complete |
| 4b | `(metrics_emit, serve_response, 1)` | 1 | `[serve_response]` | Complete |
| 5 | — | 0 | — | Done |

**Insight:** Model sees exact next-step targets, not entire graph. Reduces context bloat.

---

## Limitations & Extensions

### Current Scope

- ✓ DAG workflows (no cycles)
- ✓ Budget-constrained dispatch
- ✓ Hyperedge support
- ✓ Reachability queries
- ✗ Cost-weighted paths (all edges = 1 hop)
- ✗ Probabilistic edge weights
- ✗ Cycles / feedback loops

### Future Extensions

1. **Weighted edges:** `<<{A, ~5, B}.` → cost 5 instead of 1
   - Enables true optimal control (Bellman on weighted graph)
   - Use case: prioritize cheap tasks

2. **Conditional edges:** `<<{decision, if_true→A, if_false→B}.`
   - Fan-out based on runtime condition
   - Requires SAT/SMT solver

3. **Cycle detection & structural analysis:**
   - Identify SCCs (strongly connected components)
   - Warn on circular task dependencies

4. **Cost modeling:**
   - Annotate nodes: `{token_validator, ~0.5_tokens, user_db}`
   - Model selects among valid next hops based on token budget

---
## Incremental Dispatch Pattern (增量调度)

For complex workflows containing hyperedges (parallel branches), **do not expand all combinations**. Instead, adopt incremental dispatch:

1. **Plan**: Run `path(start, end)` to obtain the minimum logical steps.
2. **Negotiate budget**: Ensure your available logical budget ≥ min steps.
3. **At current node**: Run `query(current, end, remaining_budget)`.  
   The result may be a single task or a set `{A, B, ...}` (parallel dispatch).
4. **Execute**: Perform **all tasks** in the returned set simultaneously (or in any order, but wait for all to complete).
5. **Converge**: After all parallel tasks finish, you are at the next logical stage.  
   Set `current` to **any** of the tasks just completed – the reachability matrix guarantees they all lead to the same feasible suffix.
6. **Decrease budget**: `remaining_budget -= 1`.
7. **Repeat** from step 3 until `current == end`.

This pattern avoids path explosion and keeps decision local. The algorithm ensures you never enter a dead end.

## Free Semantics: Using Predicates as Annotations

The `predicate` field in each triple `<<{subject, predicate, object}.` is **ignored by the dispatch algorithm** – only the graph structure (subject → object) matters.

This is intentional: the core dispatch is **structure-only**. You are free to use the predicate field for any human‑ or AI‑readable semantics:

- `<<{auth, requires, token}.`
- `<<{build, triggers, test}.`
- `<<{design, optional, review}.`
- `<<{deploy, blocks, verify}.`

Because the predicate does not affect reachability or path planning, you can:

1. **Write expressive workflows** without being constrained by a fixed vocabulary.
2. **Perform semantic filtering after querying** – for example, filter `next_hops` results to only those edges whose predicate matches `'requires'` or `'triggers'`.

### Semantic Post‑Processing Example

```python
# After obtaining raw candidates from dispatch.py
candidates = dispatch.next_hops(current, target, budget)

# Suppose you have a mapping from (current, candidate) to predicate value
# Filter only edges marked as 'requires'
filtered = [c for c in candidates if get_predicate(current, c) == 'requires']
```

This separation of concerns keeps the core dispatcher small and deterministic, while allowing unlimited semantic richness on top.

Recommendation for LLM Agents

When generating triples from natural language, keep the predicate consistent within a single workflow (e.g., always use blocks or depends_on) to avoid confusion. But you are free to change it per project – the dispatcher will not care,  But you can use grep command find sentence of some predicate.
## Philosophy

**Why this matters for LLM task dispatch:**

Large workflows expose the **attention-context tradeoff**: either lose state by chunking, or run out of tokens before completion.

Path-dispatch solves this by:

1. **Precomputing structure** (graph topology) once
2. **Querying structure** (reachability) at each step
3. **Letting LLM focus** on task logic, not navigation

The model doesn't memorize the entire dependency graph—it **queries it**. This is the same principle as:
- Databases for structured data
- APIs for service coordination
- Search engines for information retrieval

**Task dispatch is just another form of information retrieval.**

---

## Summary

**Path-dispatch** models multi-hop workflows as discrete Hamiltonian systems, precomputing reachability matrices to enable efficient constrained-path queries.

- **Input:** Task dependencies as RDF-style triples
- **Precompute:** Boolean reachability matrices via discrete HJ equation
- **Query:** `next_hops(current, target, budget)` → valid next tasks
- **Output:** Enables LLMs to sequence 10–100+ step tasks without losing state

Hypergraph normalization makes parallelism and fan-out explicit. Real-time dispatch costs $O(n)$ per query, one-time precomputation is $O(n^4)$ worst case.

Use this when:
- Task workflows exceed context window
- Parallel fan-out/fan-in is common
- Model needs to avoid dead-end paths
- Intermediate state is expensive to track

Pair with `narrative-topology` for end-to-end workflow extraction and dispatch.

## Security Note

This skill uses `pickle` for fast caching. Pickle files are **not safe** to load from untrusted sources.

**Safe usage:**
- Only run the skill in your own project directory where you control the files.
- Never copy `.cache` files from untrusted sources.
- If you process untrusted triples files, set `PATH_DISPATCH_NO_CACHE=1` to disable caching.

**For shared environments (CI, multi-user):**
- Set the environment variable to disable caching, or
- Run in a container where the cache directory is ephemeral.