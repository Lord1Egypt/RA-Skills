# Evolution Logic — How the Meta-Harness Loop Works

Detailed explanation of the evolution algorithm, selection strategy, and how the proposer reasons about candidates.

## The Core Insight

From the Meta-Harness paper: **richer feedback enables better search**. The key difference from prior text optimizers:
- OPRO/TextGrad/etc.: compress feedback to 100-30K tokens
- Meta-Harness: exposes full history (~10M tokens possible) via filesystem

For Hoss, this means:
- Proposer reads ALL prior candidates' source + traces
- NOT just "score improved" or "failed" — actual reasoning about WHY
- The proposer decides what to inspect, like a developer navigating a codebase

## The Search Loop

```
Iteration t:
  1. Proposer reads ~/hoss-evolution/candidates/ (all prior candidates)
  2. Proposer reads ~/hoss-evolution/best/current/ (current best)
  3. Proposer identifies failure patterns across candidates
  4. Proposer proposes 1 targeted harness edit
  5. Candidate validated (lightweight check)
  6. Candidate evaluated on benchmark (all 20 scenarios)
  7. Results logged: candidate + scores + proposer reasoning
  8. Pareto frontier updated
  9. Next iteration: proposer reads updated history
```

## Parent Selection

**No fixed parent-child relationship.** Unlike genetic algorithms that select specific parents, Meta-Harness lets the proposer inspect ANY prior candidate. This is intentional:
- The proposer decides what's relevant to build on
- A bad candidate might have one good idea worth extending
- The proposer isn't constrained by selection pressure

The proposer typically gravitates toward:
1. Current best (strong baseline to extend)
2. Recent high-variance candidates (different approaches)
3. Failed candidates near the Pareto frontier (close but not quite)

## Pareto Frontier Logic

At any point, the Pareto frontier = all candidates where no other candidate has BOTH higher score AND lower complexity.

```python
def is_pareto_optimal(candidate, all_candidates):
    for other in all_candidates:
        if (other.score > candidate.score and
            other.complexity < candidate.complexity):
            return False  # other dominates this candidate
    return True
```

**Why Pareto?** We care about both performance AND simplicity. A harness that's 1 point better but 10× more complex isn't actually better — it's overfit.

**Complexity measure:** Sum of diff sizes between candidate harness and iteration 0 (the original Hoss configs). Larger changes = higher complexity.

## Proposer Reasoning Patterns

From paper observations, good proposers follow patterns:

### Pattern 1: Failure Mode Diagnosis
```
Proposer reads: candidate_5 (score=58, failed on memory_2)
Proposer reads: candidate_7 (score=62, also failed on memory_2)
Proposer reason: "Both failed on memory_2 (updating MEMORY.md).
  Looking at traces, the issue is HEARTBEAT.md doesn't prioritize
  memory checks during active hours. Let me add memory health to
  the batched checks."
Proposal: Edit HEARTBEAT.md to include memory consistency checks
```

### Pattern 2: Successful Strategy Extension
```
Proposer reads: candidate_12 (score=71, excellent on code_1 and code_2)
Proposer reason: "candidate_12 nailed the code scenarios.
  Its SOUL.md has detailed quality standards section.
  Let me try extending that approach to memory — add a
  'Memory Quality Standards' section to SOUL.md."
Proposal: Add section to SOUL.md building on what worked for code
```

### Pattern 3: Ablation Exploration
```
Proposer reads: candidate_9 (score=68, complex — changed 4 files)
Proposer reason: "candidate_9 had high score but changed a lot.
  Let me try isolating just the TOOLS.md change — the code
  scenarios improved there. Can I get the same gain with
  just that one file?"
Proposal: Minimal edit — only TOOLS.md change
```

### Pattern 4: Cross-Category Transfer
```
Proposer reads: candidate_15 (score=65, great on research_1)
                candidate_18 (score=59, weak on research_1)
Proposer reason: "candidate_15 uses more specific search queries.
  Its TOOLS.md has a note about search quality.
  candidate_18 just does generic searches. Let me apply
  the search specificity idea to candidate_18's approach."
Proposal: Merge search quality approach into different base
```

## When Proposals Fail

Common failure modes:
1. **Too ambitious** — proposer tries to rewrite everything → incoherent harness
2. **False pattern** — proposer sees correlation that isn't causal → wrong fix
3. **Benchmark gaming** — proposer overfits to specific scenario wording
4. **Discontinuity** — big change breaks something unrelated

The Pareto frontier naturally handles #4: if a candidate regresses on something important, it'll drop off the frontier even if it gains on other metrics.

## What to Look for in Proposer Reasoning Traces

Good reasoning traces should contain:
- Reference to specific prior candidates (by number)
- Identification of what's working/not working
- Hypothesis about WHY something works
- Specific change being proposed
- Expected improvement

Bad reasoning traces:
- Vague ("improved overall")
- No reference to prior candidates
- No hypothesis

## Convergence

How do you know when evolution has converged?
- Pareto frontier hasn't changed in 5+ iterations
- Proposer keeps proposing similar edits
- Best score plateaus

When converged: the best harness is the current Pareto-optimal candidate with the highest score.

## Initialization

Iteration 0 = Hoss's current workspace configs. These are the seed:
```bash
cp ~/.openclaw/workspace/SOUL.md ~/hoss-evolution/candidates/candidate_0/harness/
cp ~/.openclaw/workspace/IDENTITY.md ~/hoss-evolution/candidates/candidate_0/harness/
cp ~/.openclaw/workspace/AGENTS.md ~/hoss-evolution/candidates/candidate_0/harness/
cp ~/.openclaw/workspace/TOOLS.md ~/hoss-evolution/candidates/candidate_0/harness/
cp ~/.openclaw/workspace/HEARTBEAT.md ~/hoss-evolution/candidates/candidate_0/harness/
```

This gets evaluated as the baseline — everything else is improvement over Hoss-as-is.

## Diversity Maintenance

The proposer might converge to a local optimum. To prevent:
- Keep recent failed candidates in the pool — they contain negative signal
- Occasionally force the proposer to try a different starting point
- If convergence seems stuck, manually add a "diversity push" scenario

## Key Tuning Parameters

| Parameter | Default | Effect |
|-----------|---------|--------|
| Proposals per iteration | 1 | More = more search, slower |
| Validation strictness | Medium | Too strict = never evaluates; too loose = crashes |
| Benchmark size | 20 | Larger = more signal, slower |
| Pareto frontier size | unbounded | Tracked but not pruned |

## Interaction with Tyler

Tyler should NOT be evaluating candidates — the benchmark does that. Tyler's role:
1. Define/approve benchmark scenarios (does this test what matters?)
2. Subjective spot-check (does score match your quality impression?)
3. Emergency override (if a proposal is dangerous, flag it)

Tyler's NOT supposed to read proposer reasoning traces unless something looks wrong.
