# Adapter: Systems

Use this adapter when the paper's main contribution is a system design, systems optimization, infrastructure mechanism, implementation strategy, or performance tradeoff under a concrete workload and environment.

## What to prioritize

1. The bottleneck or systems problem being attacked.
2. Design choices and tradeoffs.
3. Workload, deployment setting, and hardware / software environment.
4. Measurement methodology.
5. Throughput, latency, memory, reliability, efficiency, or cost metrics.
6. Benchmark fairness and realism.

## Questions to answer in the note

- What exact bottleneck is the system trying to relieve?
- What is the central systems idea?
- What assumptions about hardware, workload, or deployment are required?
- Which metric improves, and what is the tradeoff?
- Are the comparisons apples-to-apples?
- Would the gain likely survive in realistic production conditions?

## Minimum insertions into the note

Add or expand these sections:

### Problem setup

- workload and environment
- hardware / software assumptions
- performance target and constraints

### Technical core

- architecture or design diagram in prose
- control flow or data flow
- where the performance gain is supposed to come from
- tradeoff surface

### Evidence

- benchmark methodology
- datasets / traces / deployment environment
- strongest competing systems
- sensitivity to load, scale, or hardware changes

## Special reading rules

- Read figure captions and benchmark setup carefully; many systems claims live there.
- Ask whether the workload is representative or cherry-picked.
- Distinguish algorithmic novelty from systems engineering novelty.
- Check whether the claimed gain depends on a narrow hardware stack or benchmark configuration.

## Typical failure patterns to watch for

- unrealistic or underspecified workload
- unfair baseline implementations
- incomplete cost accounting
- throughput gains hiding latency or reliability regressions
- improvement that vanishes outside one hardware setting

## Reusable note prompts

- “The core systems tradeoff is …”
- “The gain comes from shifting the bottleneck from … to …”
- “The benchmark is credible because … but limited because …”
- “This result is deployment-sensitive to …”
