# Novel Timeline Constraint Audit

Turn chapter-level dates, relative times, ages, and travel durations into an evidence-backed story timeline. The skill flags chronology, age, and travel conflicts and offers the smallest possible revision options without changing the plot.

![Novel Timeline Constraint Audit promo](assets/promo-1600x900.png)

## Input and result

Provide up to 20 scenes or 100 events with chapter/scene IDs, explicit or relative times, travel minutes, and optional `flashback: true`. You receive a story-time ordered table, conflict locations and arithmetic, minimal revision options, and missing or indeterminate intervals. Chapter numbers are never treated as invented dates.

```bash
npx skills add xxjrq/novel-timeline-audit-cn
```

Copyable fixtures: [successful input](fixtures/success-input.json) and [delivery](fixtures/success-delivery.md); [insufficient-evidence input](fixtures/failure-input.json) and [delivery](fixtures/failure-delivery.md).

## Local check

```bash
python3 scripts/audit_timeline.py fixtures/success-input.json
python3 scripts/self_test.py
```

This skill audits only event-time constraints; it does not rate, continue, or replan a novel. See [LICENSE](LICENSE) for MIT terms.
