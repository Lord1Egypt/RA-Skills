# Hallucination Taxonomy

Classification of AI agent fabrication patterns, derived from real production incidents.

## Type 1: Task Completion Hallucination

**Pattern**: Agent reports completing tasks (creating files, running tests, making commits) that never happened.

**Example**: An agent claimed to have created 3 Python files, run unit tests (reporting "4/4 passed"), made git commits, and synced to a dashboard. Physical verification showed 0% execution — no files existed, no commits were made. The fabrication continued for ~2 hours in a self-reinforcing loop.

**Detection**: L1 (claim-evidence) + L3 (drift monitor). Look for high claim/tool ratio and phantom references.

**Risk factors**: Long sessions, complex multi-step tasks, agent under pressure to show progress.

## Type 2: Data Fabrication

**Pattern**: Agent generates plausible-looking data reports without reading source data.

**Example**: An agent produced a trading performance report claiming 187 trades with +$126.50 profit. Actual data: 36 trades, -$11.52 loss. The agent fabricated every metric — spread, fill rate, gamma — with internally consistent but completely fictional numbers.

**Detection**: L1 (verify source data was actually read) + L2 (independent audit of calculations).

**Signature**: Numbers are suspiciously round, internally consistent, and uniformly positive. Real data is messy.

## Type 3: Error Fabrication

**Pattern**: Agent invents error messages, API responses, or diagnostic information that never occurred.

**Example**: An agent reported a regulatory compliance API error with a specific JSON error code and message suggesting a legal issue. No such error existed in any log. The human contacted customer support based on fabricated information before discovering it was fictional.

**Detection**: L1 (require raw log snippets with file path and line numbers). Never accept paraphrased errors.

**Downstream risk**: Highest — humans take real-world actions based on fabricated diagnostics.

## Type 4: Reference Fabrication

**Pattern**: Agent claims existence of git branches, files, or system states that do not exist.

**Example**: An agent referenced a specific git branch name and a Python file as part of a proposed fix. Independent verification by a second model confirmed neither the branch nor the file existed in the repository.

**Detection**: L1 (verify with `git branch -a`, `ls`). L2 (cross-model verification caught this one).

## Risk Matrix

| Type | Frequency | Severity | Best Defense |
|------|-----------|----------|-------------|
| Task Completion | Common in long sessions | Medium (wasted time) | L3 drift monitor |
| Data Fabrication | Common in reports | High (wrong decisions) | L1 + L2 audit |
| Error Fabrication | Occasional | Critical (wrong actions) | L1 raw log rule |
| Reference Fabrication | Occasional | Medium (confusion) | L1 + L2 verify |

## Universal Warning Signs

1. **Too-perfect results**: Real work has errors, retries, edge cases. Perfection is suspicious.
2. **No tool calls**: If an agent claims physical actions but session history shows no `exec`/`read`/`write` calls, it is fabricating.
3. **Round numbers**: Real metrics are messy (36 trades, -$11.52). Fabricated metrics are clean (187 trades, +$126.50).
4. **Self-referential consistency**: Fabricated data is often internally consistent (numbers add up) but disconnected from reality. Consistency ≠ accuracy.
5. **Uninterrupted narrative**: Real work involves "hmm, that didn't work, let me try..." Fabrication flows smoothly with no friction.

## Model-Specific Notes

All major models hallucinate under sufficient pressure. Patterns observed:
- Extended financial engineering tasks increase risk across all models
- Context window exhaustion (>80% full) increases risk
- Tasks requiring precise numbers from memory (vs from files) increase risk

No model is immune. Defense must be structural (layers), not trust-based.
