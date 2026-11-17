# Execution doc · step-by-step for the four tasks

> 中文版见 [workflows.zh.md](workflows.zh.md) (Chinese version).

Read SKILL.md's routing table and common constraints first. This file is the
execution detail for each task. Run all commands from the skill directory:
`python3 scripts/kw_graph.py <subcommand> [--base-id N] ...`. The engine emits a
single JSON object to stdout; on `ok:false` the `error` field explains why.

Shared preconditions: confirm base_id (user-provided / config default), confirm
credentials are configured (see SKILL.md first-use). For each task, restate "I'll
run <task> on library <id>" to the user before executing.

---

<a id="structure"></a>
## 1. Structure

**When**: user asks "what's in this library / knowledge structure / what areas / how
is it structured".

**Run**:
```bash
python3 scripts/kw_graph.py structure --base-id 700
```

**Read the output**: `levels` (node counts per level l1/l2/l3) + `outline` (each
level-1 topic → its level-2 subtopics → level-3 leaves). `share_pct` is that
level-1 topic's count share among all level-1 topics.

**How to tell the user** (template):
> Library <id> (<file_count> documents) has <l1> level-1 topics, <l2> level-2, <l3>
> level-3. The level-1 topics are: <topic1>, <topic2>… (optionally with shares).
> The largest, "<top topic>", breaks down into <subtopics…>. Which area to go into?

**Discipline**: order the level-1 topics by outline or by count — but node names and
numbers must come from output. Don't recite all three levels (too long); give
level-1 + the heaviest topic's expansion first, more on request.

---

<a id="graph"></a>
## 2. Graph

**When**: user says "keyword graph / knowledge graph / word cloud / draw me a graph".

**Run** (always pass `--html` with an absolute path, else it writes to the state dir):
```bash
python3 scripts/kw_graph.py graph --base-id 700 --html /tmp/kw-700.html
```

**Read the output**: `levels` + `metric: sibling_count_percentage` + `html` (the
generated file path).

**How to tell the user**:
> The graph is ready (<l1>/<l2>/<l3> three levels), at `<html path>`.
> Interaction: click a level-1 topic → level-2 appears on an inner ring in the same
> chart; click level-2 → level-3 appears. On-chart percentages = a node's share among
> its **direct siblings** (each sibling group sums to 100%), not a whole-KB absolute
> share, and raw count is not shown.

**Discipline**: the graph is a self-contained single HTML, opens in a browser
offline. Don't claim it matches the 2brain web view node-for-node — it renders the
same API tree, but the presentation (sibling percentage + progressive ring) is ours.

---

<a id="topics"></a>
## 3. Topics

**When**: user asks "what topics / topic distribution / which area has the most /
what's the focus".

**Run**:
```bash
python3 scripts/kw_graph.py topics --base-id 700
```

**Read the output**: `topics` is level-1 topics in descending count, each with
`count` / `share_pct` (whole-KB level-1 share) / `platform_weight` (2brain's own
per-sibling importance 0-100) / `subtopic_count`.

**How to tell the user**:
> Topic distribution of library <id> (by volume):
> 1. <topic> — <share_pct>% (platform weight <platform_weight>)
> 2. …
> The head topics are <top1>, <top2>, meaning this library mainly accumulates
> material in these directions.

**Discipline**: `share_pct` (count share) and `platform_weight` (platform weight) are
two different lenses; use share_pct for "share/most", platform_weight for "what the
platform deems key"; reporting both is more complete. Don't conflate them.

---

<a id="relate"></a>
## 4. Relate

**When**: user asks "how do X and Y relate / how are these two connected".

**Run**:
```bash
python3 scripts/kw_graph.py relate --a Visa --b Sponsorship --base-id 700
```

**Read the output**: `relation` ∈ {ancestor-descendant, shared-parent (direct
siblings under one topic), cousin (same ancestor topic, different branch),
unrelated-in-graph (different level-1 topics)}, plus `explanation` and
`lowest_common_topic`. If a keyword isn't in the graph, `related:null` + a `message`.

**How to tell the user**: relay `explanation` directly, and add the `caveat` (the
relation only reflects level co-occurrence, not causation / semantic equivalence /
document-level provenance).

**Discipline**: keyword matching is case-insensitive. If a keyword appears in
multiple places in the tree (e.g. both a level-1 node and a leaf elsewhere), the
engine takes the first matched path — if needed, tell the user the word has multiple
positions, or suggest a more specific term. If a word isn't in the graph, say so
plainly — don't hard-code a relation.

---

<a id="troubleshooting"></a>
## 5. Troubleshooting

| Symptom (engine error / behavior) | Cause | Handling |
|---|---|---|
| `missing 2brain graph key` | TWOBRAIN_GRAPH_KEY / config.json not set | configure per SKILL.md first-use; tell the user to generate a graph key on the platform |
| `missing valid integer base_id` | no base_id given | ask the user for the target library's integer base_id; don't guess |
| `graph key invalid or expired (HTTP 401/403)` | wrong/expired key | tell them to regenerate the graph key; don't retry blindly |
| `cannot connect to 2brain` | host can't reach API_BASE | check network / TWOBRAIN_API_BASE; course env should point at test.2brain.ai |
| `no non-empty keywords_tree in response` | too little material / just ingested, not yet parsed | report honestly that material is insufficient to graph; for just-ingested, wait for parsing then re-pull with `--fresh` |
| numbers don't match the web view | stale cache / different-moment response | re-pull with `--fresh`; explain the graph changes as material is ingested |
