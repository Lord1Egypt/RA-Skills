# GLR downstream Python quality baseline (v1)

This contract applies to projects USING GLR: adapters, trainers, evaluators,
recorders, replay tools, and reusable training utilities, as well as GLR itself.
A collection of runnable scripts is not a distributable training application.
New projects must follow this baseline. Existing projects migrate one owned
package and its callers at a time, with recorded remaining gaps.

## Package and architecture contract

Use the module responsibility and migration contract in generated
`ARCHITECTURE.md` (the Skill's `module-boundaries.md` reference).

- Use `pyproject.toml`, an explicit build backend, and `src/<project_namespace>/`.
  Each reusable Python component belongs to an installable wheel. Do not use
  `[tool.uv] package = false` for an application containing reusable Python logic.
- Declare runtime dependencies and supported GLR versions; commit an application
  lock file. Keep development tools and optional learner/monitoring dependencies
  separate. An editable install is a development convenience, not release proof.
- Use qualified imports. Do not patch `sys.path`, inject `PYTHONPATH`, change the
  working directory for imports, or load sibling source files by filename.
  Tests must import installed packages, not compensate for missing packaging.
- Keep adapters learner-neutral. Separate environment contracts, learner
  updates, orchestration, persistence, and observability. Entrypoints call these
  components; reusable policy/reward/checkpoint logic never lives in loose scripts.
- Put runtime resources in the wheel and read them with `importlib.resources`.
  Configurations, checkpoints, datasets, and logs use explicit external paths.
  Importing a module must not launch a game, start training, open a log file,
  initialize an error-reporting SDK, or change global logging configuration.

## Standard logging interface

Use Python's standard `logging.Logger` as the integration boundary, rather than
a framework-specific replacement or scattered file writers.

```python
import logging

logger = logging.getLogger(__name__)


def report_checkpoint(run_id: str, step: int) -> None:
    logger.info(
        "Checkpoint saved at step %d",
        step,
        extra={"event": "training.checkpoint_saved", "run_id": run_id, "step": step},
    )
```

- Library modules use `getLogger(__name__)` and propagate to application handlers.
  A package-level `NullHandler` is optional. Libraries must not call
  `basicConfig`, install file/network handlers, or change the root logger level.
- The application composition root owns `logging.config.dictConfig` (or
  equivalent explicit setup), levels, handlers, formatters, filters, and shutdown.
  Preserve existing third-party loggers (`disable_existing_loggers=False`).
  Repeated initialization must not duplicate handlers or listener threads.
- Use lazy message formatting and `logger.exception` within exception handlers.
  Record an error once at the owning boundary; propagate or return an explicit
  failure. Logging an exception must not turn a failed update into success.
- Define structured fields: UTC timestamp, level, logger, event, run_id, role,
  and message; include episode_id, step, update_index, error_code, and traceback
  when applicable. Context values are opaque application IDs, not account or
  machine identifiers. Use `LoggerAdapter`, `extra`, or a producer-side filter.
- JSONL is the machine-readable file format; each record is one valid JSON line
  including escaped multiline tracebacks. stderr may use a readable formatter;
  reserve stdout for declared CLI or transport protocols.
- Log lifecycle transitions and failures at INFO/WARNING/ERROR. Sample or throttle
  per-step diagnostics. Persist learner metrics and authoritative outcomes through
  the GLR telemetry/run-store contract; logs are diagnostic projections, never a
  replacement for durable metrics, update evidence, or terminal receipts.

## Threaded output, rotation, and shutdown

Training threads emit through `QueueHandler` into a bounded queue. One
`QueueListener` owns the output handlers and performs file IO outside the
training path. Set `respect_handler_level=True`. Use one rotating writer per
file: `RotatingFileHandler` with positive size/backup limits, or
`TimedRotatingFileHandler` with UTC and explicit retention. Use UTF-8.

Multiple processes must not independently rotate the same file. Use a dedicated
collector with a process-safe queue or separate per-worker files. A thread queue
does not establish process safety. Do not route multiprocessing's own internal
queue diagnostics through that same queue.

The application's logging configuration must define and test:

- queue capacity, message-size bounds, overflow policy, and visible dropped-record
  counters; the default nonblocking QueueHandler may drop on a full queue;
- bounded producer latency; do not block a training/game thread indefinitely when
  disk or network sinks stall;
- an emergency local path for errors and an explicit disk-full/permission-error
  policy, without recursively logging through the failed handler;
- creation of run/thread context before enqueueing, since listener threads do not
  inherit producer context automatically;
- traceback preservation: default QueueHandler preparation formats exceptions and
  clears `exc_info`; structured exception consumers must capture before that
  transformation or use a deliberately tested serialization strategy;
- stopping producers before draining, then stopping the listener, flushing and
  closing owned handlers; define a shutdown deadline and account for undelivered
  records. Full bounded queues must not prevent the shutdown sentinel;
- restart/reconfiguration without leaked threads, open handles, or duplicate logs.
  Abrupt process termination cannot promise a drained queue.

## Error aggregation (Sentry or another provider)

Monitoring is optional and application-owned. The core package must import and
run without a monitoring SDK or DSN. Put the provider dependency in an optional
extra, resolve secrets from deployment configuration, and initialize once in the
application process that owns the events.

For Sentry, use the official `LoggingIntegration`: INFO breadcrumbs and ERROR
events are a useful starting policy. Keep error events and the separate Sentry
Logs product explicitly configured. Do not combine automatic error capture with
unconditional `capture_exception` for the same exception. Use an offline test
transport to verify exactly one event with a usable stack trace.

Attach release, environment, run_id, role, and stable error_code for correlation.
Keep unique run IDs out of issue fingerprints; group by stable error identity.
Scrub outbound events and breadcrumbs using the provider's hooks, including
exception messages, stack locals, and paths. A file-handler filter alone does not
sanitize records intercepted by an SDK. Disable local-variable collection and
default PII unless an explicit reviewed use case requires them.

Sending must be asynchronous with bounded queues/timeouts and bounded shutdown
flush. Test unavailable networks, disabled configuration, and provider failures:
they must not change learner outcomes or deadlock training. High-frequency
metrics belong in the metrics store, not in error aggregation.

## Required quality gates

| Gate | Required evidence |
| --- | --- |
| Static | Ruff and type checking over owned source; reject import path mutation; no new blanket ignores |
| Unit | Pure reward, action mask, termination, configuration, and checkpoint behavior with deterministic fixtures |
| Contract | GLR synthetic conformance, stale identities, duplicate results, malformed observations, invalid actions, and timeout/cleanup behavior |
| Package | Build an exact wheel; fresh non-editable install; run imports and applicable tests outside checkout without PYTHONPATH |
| Training | Seeded bounded synthetic run; finite loss/gradients, real parameter change when learning is expected, checkpoint save/load and resume invariants |
| Logging | Concurrent producers, rotation/retention, valid JSONL, context isolation, exception fidelity, overflow, IO failure, drain, repeated setup |
| Monitoring | Optional-dependency absence, one captured error, correct stack/context, redaction, offline transport, bounded failure/flush |
| Regression | Every fixed defect gets a minimal behavioral fixture, expected result, and regression test; replay does not require a live game |
| Live | Separate explicitly authorized host/game acceptance with authoritative evidence; never inferred from synthetic tests |

Run deterministic gates in CI on the exact proposed revision, without game
installation, private paths, credentials, or a running monitoring service.
Use temporary directories and committed anonymized fixtures. Keep slow/live tests
explicitly marked and report skips as missing evidence. Track changed-code branch
coverage and critical failure paths; a coverage percentage alone is not acceptance.

A training smoke must check behavior, not only exit code or a printed loss.
Mock external IO at the adapter boundary, not the algorithm being verified.
Validate checkpoint schema/config/version compatibility and failure on corruption.

## Scaffold commands and existing-project migration

Generated projects carry this document as `QUALITY.md`. Run `vx run check`
for the initial static/unit baseline and `vx run package-check` for a clean
wheel installation and tests from outside the checkout. `vx run ci` combines
both gates for CI. The package gate accepts
`--find-links <wheelhouse>` when run directly as
`vx uv run python scripts/check_wheel.py`; use that for an unpublished GLR wheel.
The smoke scaffold does not implement a production logger, Sentry integration,
or a real learner: the corresponding gates become mandatory when adding them.

For existing training projects:

1. Inventory entrypoints, import roots, dependency pins, ad-hoc log writers,
   fixtures, and tests that need a live game or local data.
2. First preserve critical behavior as offline regression fixtures. Move one
   cohesive component to an owned package and migrate its callers together.
3. Replace source-path injection with installation and explicit imports.
4. Route diagnostics to standard logging and configure sinks in one application
   entrypoint. Preserve durable GLR telemetry and checkpoint semantics.
5. Enable the gates above, then migrate remaining components. Record the exact
   tested revision, package versions, commands, outcomes, and deferred live gates.
   Do not call a project compliant while known gaps remain.

## Primary references

- [Python logging cookbook](https://docs.python.org/3.10/howto/logging-cookbook.html)
  covers library integration and single-writer process coordination.
- [Python logging handlers](https://docs.python.org/3.10/library/logging.handlers.html)
  defines queue preparation, listeners, and rotation behavior.
- [Sentry logging integration source](https://github.com/getsentry/sentry-python/blob/master/sentry_sdk/integrations/logging.py)
  documents interception, breadcrumbs, and error events; pin and test the SDK
  version chosen by the downstream application.
