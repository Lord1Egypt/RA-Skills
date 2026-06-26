# Benchmark Design — How to Build and Maintain the Eval Suite

The benchmark is the measurement system. Garbage in, garbage out — a poor benchmark produces poor harnesses. This guide covers how to design good scenarios, write rubrics, and maintain the suite.

## What Makes a Good Benchmark Scenario

### Criteria

1. **Ground-truth checkable** — the expected outcome is verifiable, not subjective
2. **Covers a real failure mode** — scenarios should expose real weaknesses in current harness
3. **Diverse enough to resist gaming** — no single strategy can ace all scenarios
4. **Fast to evaluate** — each scenario should complete in <30 seconds
5. **Reproducible** — same scenario, same expected outcome

### Scenario Anatomy

Every scenario is a dict with:
```python
{
    "id": "unique_id",          # kebab-case, unique
    "category": "memory|code|coordination|research|communication|quality",
    "weight": 0.10,             # how much this matters (sum to 1.0)
    "name": "Short Name",
    "task": "The actual task description...",
    "expected": "What a perfect response looks like",
    "rubric": {
        0: "Fail description",
        1: "Partial pass description",
        2: "Good pass description",
        3: "Excellent description"
    }
}
```

## Category Weights

The default weight distribution:
| Category | Weight | Rationale |
|----------|--------|-----------|
| Memory | 25% | Hoss's key differentiator = continuity |
| Code | 25% | Core operational competency |
| Research | 20% | Information synthesis capability |
| Coordination | 15% | Multi-agent orchestration |
| Communication | 10% | Quality of output |
| Quality | 5% | Catching errors, consistency |

Adjust these if you want to optimize for different traits.

## How to Add a New Scenario

1. **Identify the gap** — what capability isn't being tested?
2. **Write the scenario** following the anatomy above
3. **Set weight** — new scenarios should steal weight from existing ones
4. **Test it manually** — run it against current harness and verify score makes sense
5. **Update SCENARIOS list** in `scripts/evaluate.py`

Example new scenario addition:
```python
{
    "id": "memory_5",
    "category": "memory",
    "weight": 0.05,  # steal 0.05 from memory_4
    "name": "Selective memory retrieval",
    "task": "Tyler asks: 'What do we know about Flume's pricing for agent-hosting?' Search memory and give a precise answer citing specific facts, not vague impressions.",
    "expected": "Accurate recall of agent-hosting pricing tiers from TOOLS.md or MEMORY.md",
    "rubric": {
        0: "No search or wrong facts",
        1: "Partial recall, missing key details",
        2: "Accurate with minor omissions",
        3: "Precise recall with proper citations"
    }
},
```

## Scoring

- **0 = Fail** — didn't attempt, completely wrong, or wrong approach
- **1 = Partial** — attempted, some correct, major gaps
- **2 = Pass** — correct approach, minor issues
- **3 = Excellent** — better than expected, shows initiative

### Final Score Calculation

```python
final_score = sum(
    scenario_score / 3 * scenario_weight
    for scenario in scenarios
) * 100  # scale to 0-100
```

### Pareto Frontier

A candidate is Pareto-optimal if no other candidate has both:
- Higher final_score
- AND lower complexity (fewer/smaller changes)

Complexity = sum of diff sizes across changed files.

## How to Know the Benchmark Is Good

**Signs the benchmark is well-designed:**
- Current harness scores around 50-70 (not saturated, not impossible)
- Different candidates get different scores (not all same)
- No scenario has all 3s or all 0s (discriminative)
- Scenarios cover the files that matter (SOUL.md changes → personality scores change)

**Signs to rework the benchmark:**
- All candidates score identically (benchmark is uninformative)
- Best candidate gets 3s on everything (benchmark is too easy)
- Scores don't correlate with Tyler's subjective quality impression (misaligned)

## Scenario Maintenance

- **Quarterly review:** Are scenarios still relevant? Update task descriptions
- **Add hard cases:** When Hoss fails on a real task, turn it into a benchmark scenario
- **Remove gaming:** If a candidate exploits a scenario (e.g., hard-codes answers), rewrite the scenario
- **Calibrate weights:** If a category feels over/under-weighted, adjust based on Tyler's priorities

## Scenario Library (Add Your Own)

Scenarios live in `scripts/evaluate.py` in the `SCENARIOS` list. Add your own by appending to that list. Keep categories balanced.

### Memory Scenarios (target: 20-25% of score)
- Recall from daily memory logs
- Update MEMORY.md with new decisions
- Synthesize across multiple memory files
- Create new memory file from scratch
- Find and correct stale memory entries

### Code Scenarios (target: 20-25% of score)
- Write working code from spec
- Debug broken code
- Security review
- Code review for quality/consistency
- Write bash one-liners

### Research Scenarios (target: 15-20% of score)
- Web search + synthesize
- Fetch and summarize
- Competitive analysis
- Technical deep-dive

### Coordination Scenarios (target: 15% of score)
- Spawn parallel sub-agents
- Delegate to correct agent
- Handle agent failure gracefully
- Synthesize multi-agent results

### Communication Scenarios (target: 10% of score)
- Draft Discord messages
- Write email responses
- Handle disagreeable feedback
- Professional escalation

### Quality Scenarios (target: 5% of score)
- Spot broken/stale links
- Catch inconsistencies between files
- Audit for outdated info
- Error detection

## Self-Improvement Loop

After each evolution iteration, Tyler should review:
1. Did the new score match subjective quality?
2. Which scenarios regressed? Which improved?
3. Any scenario that seems gaming-prone?
4. Are there real failures not captured in benchmark?

Feed these observations back into scenario design.
