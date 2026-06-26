# Corvus Pattern Engines

## Routine Engine

Detects recurring activities with predictable cadence.

Signals evaluated: transactions, location visits, booking confirmations, calendar entries, app usage patterns.

Detection criteria:
- Signal recurrence across at least 3 instances
- Temporal interval consistency within configured tolerance
- Cross-domain confirmation (same pattern visible from multiple signal sources)

Validation: minimum 3 occurrences, interval deviation < 30%, at least one cross-domain corroboration.

## Thread Engine

Detects incomplete activity clusters — topics, projects, or investigations that appear repeatedly without resolution.

Signals evaluated: research topics, document edits, message threads, task status.

Detection criteria:
- Topic appears in 2+ sessions without a conclusion signal
- Activity continues but no resolution artifact exists
- Time since last activity within configured staleness window

Validation: at least 2 sessions, no completion signal detected, last activity within window.

## Interest Engine

Identifies emerging interest areas through signal clustering across domains.

Signals evaluated: search activity, document edits, messages, research topics, purchases, media consumption.

Detection criteria:
- Signal cluster forms around a coherent topic
- Signals span at least 2 domains (e.g., search + purchase, or research + conversation)
- Growth rate exceeds baseline activity rate

Validation: minimum 5 signals, at least 2 domains, growth rate > 1.5× baseline.

## Opportunity Engine

Detects useful connections between previously unrelated entities or domains.

Signals evaluated: entity co-occurrence, temporal alignment, relationship proximity.

Detection criteria:
- Two entities or topics that have not been previously linked
- Shared context or temporal alignment suggests a useful connection
- The connection has actionable potential

Validation: no prior relationship in Chronicle, at least 2 supporting signals, actionable follow-up identifiable.

## Anomaly Engine

Identifies meaningful deviations from established patterns.

Signals evaluated: spending, schedule, location, communication frequency, routine adherence.

Detection criteria:
- Established pattern exists with sufficient history
- Current observation deviates beyond configured threshold
- Deviation is not explained by known context (e.g., scheduled travel)

Validation: baseline pattern confidence > 0.7, deviation > 2 standard deviations, no explanatory context found.

## Confidence Scoring

All engines use a common confidence scale:
- **high** (>0.8) — strong evidence, multiple corroborating signals
- **med** (0.5–0.8) — reasonable evidence, some corroboration
- **low** (<0.5) — weak evidence, hypothesis-level only

Only patterns with med or higher confidence become insight proposals.
