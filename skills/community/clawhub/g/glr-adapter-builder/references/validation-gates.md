# Adapter validation gates

## Contract gate

- Spec shapes, dtypes, bounds, masks, capabilities, and protocol versions match.
- Reset creates a new episode at step zero; attach creates a fresh logical
  episode without claiming a physical reset.
- Step identity increments exactly once for each accepted action.
- Terminated and truncated are never both true for one participant.
- Closed adapters reject further work.

## Bridge gate

- Authentication completes before `describe` or action calls.
- Exact target binding is revalidated at each mutating boundary.
- Payload size, deadline, queue depth, and main-thread work are bounded.
- Stale episode/cursor requests fail before action execution.
- Lost mutating responses trigger authoritative readback, never blind repost.
- Disconnect and watchdog paths release owned input state.
- Metadata is denied by default and allowlisted explicitly.

## Knowledge and reward gate

- Research sources have provenance, access dates, and compact paraphrases.
- Version-sensitive claims are refreshed against current sources.
- Advisory claims cannot expand action authority or satisfy authoritative reward
  terms.
- Required reward signals fail closed when missing.
- Duplicate, unknown, wrong-source, stale, non-finite, and outlier signals are
  covered by negative tests.
- Reward contribution breakdowns reproduce the configured total.

## Evidence gate

- Apply [downstream-quality.md](downstream-quality.md) to the complete owned
  Python training package, including logging and optional monitoring changes.
- Install the exact wheel into a clean environment and test outside the source
  checkout; source-path injection and editable installs are not package evidence.
- Each fixed training defect has an offline behavioral regression fixture.

- Unit tests and synthetic conformance pass from a clean environment.
- Optional integrations are tested separately from the NumPy-only core.
- Live acceptance uses only an explicitly authorized environment.
- Public reports contain aggregate counts only, not paths, IDs, observations,
  actions, screenshots, or proprietary data.
- Rust promotion includes a reproducible before/after benchmark and parity
  fixtures; language preference alone is not evidence.
