# M*A*L*P Tasks

## Table of contents

- [NOTES.txt conventions](#notestxt-conventions)
- [FOB.txt conventions](#fobtxt-conventions)
- [Tool-backed FOBs](#tool-backed-fobs)
- [SUMMARY.txt depth](#summarytxt-depth)
- [Opening a malp](#opening-a-malp)
- [Kino](#kino)
- [`what malps do we have?`](#what-malps-do-we-have)
- [`lets send malp to <path>`](#lets-send-malp-to-path)
- [Staleness and retirement](#staleness-and-retirement)

## NOTES.txt conventions

`NOTES.txt` is a living scratchpad, not a log. It should shrink over time.

## FOB.txt conventions

`FOB.txt` is the current forward operating base. It is a tactical snapshot, not a history file.

Use it when the user wants a compact "where we are operating right now" view inside a malp.

### What belongs in FOB.txt

- a short list of active paths or files
- a few current topics, fronts, or areas under investigation
- temporary focus points that may change during the task
- links between the tracked path and a small number of external fronts

### What does NOT belong

- diary-style notes
- long explanations
- exhaustive file inventories
- resolved work that belongs in history
- duplicate task tracking already present in `NOTES.txt`
- broad project overview that belongs in `SUMMARY.txt`

### Suggested shape

Keep it terse. A simple bullet list is usually enough.

Example:

```text
Forward Operating Base
----------------------
- Path: src/Search/TripSearch/
- Path: tests/Search/TripSearch/
- Topic: child filter-set projection shape
- Topic: reservation alias `R` restoration rules
- Front: related customer bug notes outside repo
```

If `FOB.txt` grows beyond a quick glance, consider pruning it or splitting the focus more cleanly.

That is a judgment call, not a blind rule. Some malps are doing frontier work and may temporarily carry more unresolved weight than a mature malp should. The real question is whether the FOB is still helping the current operation or has turned into durable context that belongs in `NOTES.txt` or a deeper malp.

## Tool-backed FOBs

A project-local tool directory can be a conceptual FOB when it is the current source of reconnaissance. For `.clawpatch/`, read `references/clawpatch.md` and keep generic clawpatch procedure in the skill rather than in the repo malp.

In repo `.malp/` files, record only what is local to the project:
- active finding IDs and short titles
- current reachability / plausibility-to-recreate judgments
- whether the finding is ordinary-browser reachable, direct-route/API-only, endpoint-owner-unclear, dead-code risk, or unresolved semantic risk
- next verification front

Do not turn `FOB.txt` into a generic tool manual.

### When to create or refresh automatically

Create or refresh `FOB.txt` when one or more of these are true:

- most of the current work sits under one meaningful subdirectory
- the work repeatedly returns to the same small set of files
- the malp root is broad, but the active operation is narrow
- there is temptation to split off a child malp, but the current focus still fits inside the parent cleanly

This is especially useful when sending a malp to a broad parent path while the real action is happening deeper down. In that case, `FOB.txt` marks the forward base without forcing an immediate child malp.

Default bias: absorb the deeper focus into the parent malp through `FOB.txt` first. Only split into a child malp when the user explicitly wants that separation or the work truly needs a durable independent probe.

When absorbing a deeper focus, do not let the parent become bloated. Shed stale breadth and re-center around the newly important front. If the parent has become mostly scaffolding while child malps now carry the durable work, retiring the parent may be cleaner than absorbing everything back upward.

### Open questions format

Use checkbox format for open questions and tasks:

```
- [ ] Unresolved item — describe what needs to be determined or done.
- [x] Resolved item — brief description. → What was decided or found.
```

- Open items use `- [ ]`.
- Closed items use `- [x]` and append ` → <resolution>` inline so the decision is visible alongside the item.
- Closed items can remain briefly for context, but should be pruned once the resolution is formalized elsewhere (README, committed code, etc.).
- **Pruning signal**: more than ~10 resolved items is a strong sign that a prune may be due. Remove resolved items whose resolutions are already captured in committed files.
- Do not apply that mechanically. A malp that is breaking new ground may carry a larger unresolved working set for a while. Prune based on whether the file is still serving the work, not just on item counts.

### Exit criteria section

Every `NOTES.txt` should include an explicit **Exit criteria** section near the top:

```text
Exit criteria
-------------
Before this work is considered done, each note here should be one of:
- formally documented in a committed file (README, code, etc.)
- checked off as solved
- removed because it is no longer relevant
```

The goal is for `NOTES.txt` to shrink toward empty as work matures. If it keeps growing, that's a signal that items aren't being resolved or formalized.

### What belongs in NOTES.txt

- Open questions and unresolved decisions
- Tribal knowledge not yet in committed files (tag provenance: "Per Alice:", "Bob notes:", etc.)
- Working context (partial findings, hypotheses, things to verify)
- Design philosophy and intent not obvious from the code
- Cross-references to related malps (e.g., "See also: `../related-project/.malp/NOTES.txt`")

Cross-references are pointers, not permission. By default, read only the `.malp` the user asked for. If another `.malp` looks relevant, ask before reading it or bringing it into context. Example: if one malp says `See also: ../related-project/.malp/NOTES.txt`, do not open that file unless the user says to.

### What does NOT belong

- Resolved items with no pending follow-up (prune these)
- Content already formalized in README or committed code
- Raw logs or meeting notes (summarize the actionable parts)
- Credentials or secrets (reference where they live instead). If secrets are already present and the path is inside a git repo, proactively recommend an ignore strategy — see `repo-strategies.md`.

### SUMMARY.txt depth

`SUMMARY.txt` should stay short. It is the quick orientation layer, not the main workspace.

Default bias:
- keep it brief enough to scan quickly
- answer what the path is and how it is shaped
- avoid storing active investigation there
- move working detail, open questions, and accumulating context into `NOTES.txt`

Scale with the directory:
- **Leaf project / small tool** — usually a short paragraph: what it is, how to run it, one or two key details.
- **Larger project** — a compact overview: what it is, architecture, tech stack, a few key files.
- **Monorepo root** — a concise structural map: directory structure, tech stack, key paths, and only the most important recent context.

If `SUMMARY.txt` starts behaving like a second `NOTES.txt`, trim it and move the living material back into `NOTES.txt`.

## Opening a malp

### Current worksite

When opening a malp as the current worksite:

1. Read `SUMMARY.txt`.
2. Read `NOTES.txt`.
3. Read `FOB.txt` if present.
4. Judge whether `FOB.txt` still looks tactical or has become overgrown.
5. Judge whether the malp as a whole may need a prune.
6. If it looks overgrown, stale, or structurally confused, recommend a course of action before or alongside the task work.

### Reference-only

When opening a malp only as reference material:

1. Pull only the minimum context needed.
2. Do not automatically treat its `FOB.txt` as something that must be maintained now.
3. Mention structural issues only when they materially affect the current task.

## Kino

Use Kino when ordinary malp handling would be friction-heavy, too broad, or too context-expensive.

The bar to invoke Kino is intentionally low. Design Kino to be safe under casual overuse by keeping traversal cheap to report rather than by relying on restraint.

Typical triggers:
- the user asks for the best malp for a question, task, or workstream
- the user wonders whether a path should get a malp
- the user asks `what malps do we have?` but a plain map listing is not enough to answer well
- you realize another malp may need to be pulled into context, but want to choose deliberately first
- the agent needs to compare multiple candidate malps before recommending one
- the question clearly benefits from heuristic scouting before a concise answer is possible

When invoking Kino:

If a lightweight heuristic pass is useful, prefer the bundled helper:

```bash
python3 <skill-dir>/scripts/kino.py --json \
  --question "Which malp should come into context next?" \
  --current-malp /path/to/current/.malp \
  --path /related/worksite/path \
  --scan-near-path
```

For provenance-style questions where the malps may know the topic but not the origin story, allow a bounded git auxiliary pass:

```bash
python3 <skill-dir>/scripts/kino.py --json \
  --question "Does any malp know who first added Google API support in Tres?" \
  --git-aux
```

For trustworthiness / drift questions, allow territory-scoped git freshness on the recommended malp:

```bash
python3 <skill-dir>/scripts/kino.py --json \
  --question "Which malp knows about TAPOS?" \
  --git-freshness
```

For cluster / neighborhood questions, allow bounded containment estimation:

```bash
python3 <skill-dir>/scripts/kino.py --json \
  --question "Is TAPOS strictly contained in a group of tags?" \
  --containment
```

Use the helper's output as a recommendation surface, not as permission to load everything it inspected.

Treat helper output as provisional reconnaissance. A Kino pass that does not quickly improve the answer is not a failure; it is a scout report you can abandon.

Treat malp-space as larger than `.malp/*.txt`: it includes both malp telemetry and the attached project territory. If needed, a shallow slice of recent git history may be used as auxiliary territory evidence.

1. State the concrete question Kino is trying to answer.
   - examples: `Which malp should come into context next?` or `Does this path need a new malp?`
2. Start from the best available anchor:
   - a specific target `.malp/`
   - a path the user mentioned
   - an active map entry
   - a likely candidate surfaced during discovery
3. Read the anchor malp if one exists, including `SUMMARY.txt`, `NOTES.txt`, and `FOB.txt` when present.
4. If the anchor already answers the question well enough, Kino may stop there — but the main requirement is that any further scouting must still return a narrow recommendation rather than a bulky context dump.
5. Include the containing directory only when it materially shapes interpretation.
6. Prefer a quick read of project doctrine or orientation files when they sharpen the answer (for example `README.md`, `STATUS.md`, `DESIGN-RULES.md`, or similarly central files).
7. If doctrine and structure are still ambiguous, Kino may consult shallow recent git history as supporting territory evidence.
   - keep it recent and small
   - use it as a tie-breaker or confirmation layer
   - do not treat commit chatter as the main semantic substrate
8. Generate leads, then follow those leads heuristically as far as needed within reason. Valid leads include:
   - paths named in `FOB.txt`
   - key paths named in `SUMMARY.txt`
   - explicit cross-malp references in `NOTES.txt`
   - structural cues in the containing directory
   - active map entries
   - attic hints when needed for orientation
   - nearby unindexed `.malp/` paths already surfaced by the current investigation
9. Kino may inspect many paths or malps without loading all of them into active context.
10. Collapse broad traversal into a narrow recommendation whenever possible:
   - recommend the specific malp to bring into context next, if any
   - or recommend staying with the current malp
   - or recommend sending a new malp first when no existing malp is a good fit
11. Say what kind of promotion Kino is recommending.
   - `reference` means the malp looks useful as supporting context or analogy
   - `working` means the malp should probably become an active worksite
   - territory-driven analogies often point to `reference` promotion even when the malp notes themselves are thin
12. Attach a concrete confidence level to that recommendation.
   - use plain labels like high / medium / low, or a compact numeric score when useful
   - confidence should reflect how strongly the inspected evidence supports the recommendation, not fake precision
   - the helper script already emits a recommendation, promotion, confidence, short reasons, and ranked alternatives; prefer summarizing that output over re-expanding the crawl inline
   - when `--git-aux` is used on a provenance-style question, the helper may also emit:
     - `direct_answer` — whether the malps appear to answer that provenance question directly
     - `auxiliary` — a bounded git-history finding when shallow repo history materially helps
   - when `--git-freshness` is used, the helper may also emit:
     - `git_freshness.status` — `fresh`, `slightly-behind`, `stale`, or `unknown`
     - `git_freshness.last_malp_update`
     - `git_freshness.last_territory_commit`
     - `git_freshness.commits_since_malp`
     - `git_freshness.dirty`
   - when `--containment` is used, the helper may also emit:
     - `containment.status` — `strictly-contained`, `mostly-contained`, `not-contained`, or `insufficient-signal`
     - `containment.term`
     - `containment.cluster_tags`
     - `containment.supporting_malps`
     - `containment.outside_hits`
13. Keep the answer bounded even when traversal is broad:
   - report conclusions, uncertainty, and the small set of paths or malps that materially informed the answer
   - do not dump every inspected path
   - distinguish between inspected material and surfaced material when that matters
   - it is acceptable to say `this malp never noticed it, but its project territory looks similar`
14. Do not surface attic malps in the answer unless the user explicitly asks for attic or archived material.
15. If an unindexed malp materially informs the answer, say so plainly.
16. If git history materially informed the recommendation, say so briefly rather than pretending the signal came only from malp files.
17. If git freshness materially affects whether the recommended malp should be trusted without refresh, say so briefly.
18. If containment materially helps answer whether a term lives inside one conceptual neighborhood, report that bounded cluster result rather than expanding into a broad tag dump.
19. Stop expanding once additional traversal is no longer changing the recommendation in a meaningful way.
20. If Kino cannot produce a better recommendation than the current malp after a reasonable pass, say so and stop instead of escalating further.

Default bias:
- favor heuristic synthesis over exhaustive enumeration
- let Kino scout freely when it improves the answer
- keep the social cost of trying Kino near zero
- prefer a concrete next-malp recommendation over vague broad summary
- let project territory dominate when telemetry is narrow and the territory signal is stronger
- use git history only as a shallow supporting signal
- keep reporting selective and explicit
- optimize for context-safe output, not restraint theater
- drop Kino quickly when notes, source, or direct inspection are already giving a better answer

## `what malps do we have?`

When the user asks `what malps do we have?` or an equivalent discovery request:

1. Read `~/.malp-home/MAP.txt`.
2. If `~/.malp-home/TAGS.txt` exists, read it too and use it only to surface user-defined tags alongside matching malp paths.
3. Summarize the available active `.malp` paths in a short list.
4. Do not include attic material by default unless the user explicitly asks for archived, retired, or attic malps too.
5. Do not read or summarize attic material during normal discovery; attic is cold storage.
6. If an unindexed `.malp/` appears through the current task, a user-provided path, or some other already-in-scope evidence, list it separately as unindexed rather than silently treating it as active or attic.
7. Do not proactively scan the filesystem for unindexed `.malp/` directories during ordinary discovery unless the user explicitly asks for a path or scope audit, or unless Kino is needed to answer the actual question well.
8. Ask the user whether they know why each unindexed malp is unindexed before proposing any classification change.
9. Do not automatically read unindexed malps into active context just because they exist.
10. If the map is empty or missing, say so plainly.
11. If a plain listing is insufficient to answer the real question, invoke Kino quietly and return a better recommendation or categorization instead of stopping at the map.
12. Ask the user which `.malp` they want to open when that is still the best next step.
13. When the user chooses one, read that `.malp` and summarize the relevant contents or follow-up instructions.

`TAGS.txt` is optional and user-maintained. Do not add tags automatically. Use one line per malp in this format:

```text
backend,legacy:/full/path/to/.malp
```

Keep explanatory or disabled lines commented out with `#`.

## `lets send malp to <path>`

When the user says `lets send malp to <path>`:

1. Create a `.malp` directory inside `<path>`.
2. Perform a quick summary of the contents of `<path>`.
3. Write the summary to `.malp/SUMMARY.txt`. Scale depth to directory complexity.
4. If the project already has doctrine or reference files that govern wording, product truth, or interaction rules (for example `DESIGN-RULES.md`, `README.md`, `STATUS.md`, or similar), read them before refreshing the malp and treat them as first-class context.
   - Do not create such files just because a malp exists.
   - Do not assume every project needs them.
   - Do not treat their absence as a problem.
5. Keep `.malp/NOTES.txt` as the primary workspace for project-local progress, problems, design philosophy, and tribal knowledge.
6. Assess whether the active work appears to cluster under a deeper subpath, feature area, or recurring topic set.
7. If that cluster is meaningful, create or refresh `.malp/FOB.txt` automatically as the current forward operating base.
8. Prefer updating `FOB.txt` over creating a child malp. A deeper focus should usually be absorbed by the parent malp unless the user explicitly wants a separate malp or the deeper path clearly needs durable independent tracking.
9. If the parent absorbs that deeper focus, make room for it: narrow the active scope, prune stale or secondary fronts from `FOB.txt`, and let `NOTES.txt` reflect the new center of gravity.
10. Keep `SUMMARY.txt` up to date as the concise overview of `<path>` itself, using `<path>/.malp/NOTES.txt` for context when helpful.
11. Remove items from `NOTES.txt` as they are solved or formalized in `<path>`.
12. After a new `.malp` has been created, maintain `~/.malp-home/MAP.txt` as a newline-delimited list of every `.malp` directory path created so far; primarily append new paths and leave old ones in place.
13. If a `.malp` already exists for `<path>`, verify whether `SUMMARY.txt` still fits the current contents, verify that `MAP.txt` still references the path, refresh the summary if needed, refresh `FOB.txt` if the current operational center has changed, and reflect any relevant existing project doctrine or reference files in `SUMMARY.txt`, `NOTES.txt`, or `FOB.txt` as needed.
14. If a project-local `.malp/` exists but the path is absent from both active and attic maps, report it as unindexed before changing anything.
15. If the user wants that unindexed malp classified, ask whether it should become active, attic, or remain unindexed, then update the appropriate map explicitly.
16. Reply to the user with the summary.
17. Do **not** proactively raise version control concerns about `.malp/`. See `repo-strategies.md` if the user asks.

## Staleness and retirement

- If a malp's NOTES are mostly resolved and it hasn't been touched recently, suggest retirement.
- Retirement means removing the path from active `MAP.txt` and then either recording it in `~/.malp-home/attic/MAP.txt` with optional attic metadata or snapshots, or deleting the `.malp/` directory, depending on what the user wants.
- Default bias: if the goal is to keep history but avoid loading context, suggest the attic.
- Don't retire without asking — the user may want to keep it for historical context.
- A parent malp can also be retired structurally when it no longer helps coordinate the work and the meaningful activity now lives in child malps.
- In that case, prefer letting the child malps stand on their own rather than forcing a re-absorption into the parent.
- Read `references/attic.md` when the user wants to design, use, or refine attic behavior.
- Read `references/indexing.md` when the user wants to reason about active vs attic vs unindexed state.
