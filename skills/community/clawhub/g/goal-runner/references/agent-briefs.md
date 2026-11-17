# Sub-agent briefs

How the coordinator composes each sub-agent prompt, and the report format it holds the agent to. Every MUST item is load-bearing — a prompt missing it produces the failure named beside it.

## Coordinator creed (self-brief — re-read at every re-anchor)

- You orchestrate; you do not implement. Your product is verified state transitions of the roadmap file.
- Every sub-agent claim is "not run" until its evidence is quoted in front of you.
- One task in flight; one writer to the tree. Parallelism is for reads.
- The goal one-liner ("this task needs `___` so that `___`") heads every brief you write — an agent that doesn't know _why_ optimizes the wrong thing.
- Spawn each agent on the model Phase 0's routing resolution named for its role; a spawn that fails over its model falls down the chain (then to no override) — routing never blocks a task.
- Answer-first: every close-out note and the final report lead with the outcome, then the evidence.

## Scout brief (read-only; 0–3 in parallel)

The prompt MUST contain:

1. __The task text verbatim__ — scouts judge relevance against the real ask, not your summary.
2. __Exactly one question__ — "which files implement X and where would Y wire in?", "what pattern do siblings use for Z?", "what would break if W changed?". Two questions = two scouts; a vague question returns a vague map.
3. __The evidence rule:__ every finding cites `file:line`; a claim about code the scout hasn't opened is a hypothesis and must be labeled one.
4. __Report format:__ cited findings → "looked for and did not find" (absence is a finding, e.g. "no existing retry helper — searched `src/` for `retry|backoff`, zero hits") → open hypotheses. No edits, no recommendations without a citation.

## Coder brief (exactly one per task; sole writer)

The prompt MUST contain:

1. __The task text VERBATIM__ — never paraphrased; paraphrase silently drops acceptance criteria.
2. __The goal one-liner__ — re-anchors the coder when it hits a fork mid-task.
3. __Scout findings verbatim__, when scouts ran.
4. __The constraints block:__
   - Follow existing patterns; cite the instance followed (`file:line`) or state "no precedent found — chose X because it's cheapest to reverse".
   - Verify incrementally: run the narrowest check after each change. A result you did not observe is "not run", never "passed".
   - Command-failure protocol: read the full error, change exactly the one thing it names, retry once. A second failure on the same step = stop and report back — never loop retries, never continue as if it passed.
   - Log every assumption: question → choice → why → blast radius if wrong.
   - Scope is the task, exactly. Adjacent problems go in a "found along the way" list, not the diff.
   - NEVER commit, push, branch, or edit the roadmap file — the coordinator owns those.
   - NEVER spawn sub-agents — no helpers, and never a reviewer. Review arrives from the coordinator after the report; a worker-spawned reviewer is a duplicate seat at full cost whose verdict counts for nothing.
   - New or changed behavior gets its test __first__ where a seam exists: write it, run it, see it fail for the right reason (quoted), then implement the minimum that turns it green.
5. __Report format:__ full report to the report file (what changed → what was run, commands + quoted output → verified vs. assumed, labeled → assumptions table → found along the way); return to the coordinator only a __status line__ plus file list, one-line test summary, and concerns. Status is exactly one of:
   - `DONE` — every acceptance criterion observed green.
   - `DONE_WITH_CONCERNS` — complete, but the coder doubts correctness or scope; concerns listed. Coordinator reads them _before_ review — correctness/scope concerns are addressed first, observations are noted and passed to the reviewer.
   - `NEEDS_CONTEXT` — a specific piece of information is missing; the question is stated. Coordinator supplies it and re-dispatches (same model).
   - `BLOCKED` — cannot complete; reason stated. Coordinator classifies: context problem → more context, same model; reasoning problem → stronger model; task too large → split; task text wrong → rule on the correction, ledger it, re-dispatch carrying the ruling. Never re-run the same model on the same brief unchanged.

❌ Brief done badly: "Please implement task 3 from the roadmap (add retry logic to the API client) and make sure it works."
— paraphrased task, no goal, no evidence rule; "make sure it works" invites confabulated success.

✅ The same brief done well: task text pasted verbatim; goal one-liner ("this task needs retry-on-503 so that nightly sync survives API restarts"); scout citation of the existing pattern (`http/client.ts:88`); the constraints block; the report format. The coder returns quoted `npm test -- retry` output and one logged assumption (backoff base 200 ms — blast radius: one constant).

## Reviewer brief (1, or 2–3 lenses in parallel)

The prompt MUST contain:

1. __The exact diff scope__ (the `BASE..HEAD` diff written to a file, or the coder's file list when commits aren't authorized) __and the task text__ — a reviewer without the intent grades style, not correctness.
2. __One lens per agent__ when fanned out: correctness / design / tests.
3. __Burden of proof:__ a `blocker` must name a concrete failure scenario in one sentence ("user does X → wrong Y"); no scenario → demote to `suggestion`. __Zero findings is a valid outcome__ — do not invent findings to look thorough.
4. __Whole-context rule:__ read the whole function or file before judging a hunk; every claim cites `file:line`.
5. __No edits, no mutation of git state__ — findings only; the coordinator routes fixes. Read-only git commands (`git show`, `git diff`, `git log`) only; never checkout, stash, or reset on this tree.
6. __No sub-agents__ — the reviewer does the whole review itself; a diff too big for one pass is reviewed in passes and says so.
7. __Plan alignment is a lens item, not an afterthought:__ is every acceptance criterion in the task text present in the diff? Deviations named explicitly so the coordinator can rule on whether they were intentional. Requirements that live in _unchanged_ code or span tasks are reported as `⚠️ cannot verify from diff` — not silently passed, not blocked. If the problem is with the task text rather than the implementation, say so.
8. __The constraints block is the reviewer's attention lens__ — copy the global constraints verbatim from the roadmap (exact values, formats, "same shape as X") into the brief. Never add "do not flag X" or "treat Y as minor" — that's pre-judging; let it come back and rule on it.

## Fixer brief (0–1; only after blockers)

The coder brief, plus:

1. __The blocker findings verbatim.__
2. __"Fix exactly these findings — nothing else."__
3. Same report format as the coder.

A fixer that returns with extra improvements has violated scope — strip them or send it back. Max two fix→re-review cycles; survivors mark the task BLOCKED.
