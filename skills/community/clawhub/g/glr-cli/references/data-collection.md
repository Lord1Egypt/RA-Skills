# Collect, render, and trace training data

Read this when wiring diagnostics, diagnosing missing workbench data, or handing
training evidence to another agent. All paths in this Skill are relative to its
own directory; a GLR source checkout is not required.

## Bind before collecting

1. Inspect `glr --version`, `glr --project . --json doctor`, and
   `glr --json telemetry schema`. An older installed release may not support the
   workbench APIs. Do not treat repository source as installed capability.
2. Resolve the selected project/context and an existing running run. GLR-launched
   roles inherit `GLR_RUN_ID`, `GLR_STORE_PATH`, and `GLR_RUN_DIR`; do not invent a
   run ID or attach observations from another environment/episode.
3. Use `glr --project . dashboard` when human controls or HTTP ingestion are
   needed. `observe` and automatic training observers are read-only. The server
   announces its URL; do not assume a fixed port. Select a run context on the
   supported training/runtime operation, not on `dashboard` itself.

## Choose the data path

| Data | Producer path | Consumer |
| --- | --- | --- |
| Existing JSON, JSONL, text or FFmpeg stderr | Managed role stdout/stderr | Process logs; file records do not become persisted events or metrics |
| Agent decisions, execution receipts, custom observations | `BridgeTelemetry` events or Python `Telemetry.event` | Event trace with source/run/episode/step provenance |
| Measured numeric training signals | `metrics[]` or `Telemetry.metric` | Metric charts; diagnostic values cannot satisfy authoritative reward terms |
| Explicit learner updates | `Telemetry.learning_update` after an actual update | Learning stage and measured metrics |
| Latest adapter data panels | `bridge.state` with `payload.workbench` | Game-neutral stats, tables and notes |
| Image, video, Markdown, checkpoint, report | Finalized file + artifact registration | Media/document view and verified run archive |

For legacy logs, write one complete JSON object per line, UTF-8, and flush at
useful boundaries. For example, `{"kind":"status","hp":72}` is rendered as a
record automatically. This improves display only; it does not create trusted
events, timestamps, chart metrics or learning evidence. Never parse a log and
silently backfill a terminal run as if observations were collected live.

## Bridge reporting through Python, HTTP, or CLI

```python
from game_learning_runtime import BridgeTelemetry

publisher = BridgeTelemetry.from_env("bridge.example")
if publisher is not None:
    batch = publisher.prepare(
        events=[
            {
                "kind": "agent.execution",
                "episode_id": "episode-example",
                "step_id": 42,
                "payload": {
                    "summary": "Synthetic example receipt",
                    "input": {"action": "inspect"},
                    "output": {"accepted": True},
                    "duration_ms": 12,
                },
            }
        ],
        metrics=[{"name": "bridge.latency_ms", "value": 12, "step_id": 42}],
    )
    publisher.send(batch)
```

The example values are synthetic. Replace them with the runtime's measured
inputs, receipts and identifiers. `duration_ms` must be measured; never infer it
from adjacent log messages. Record a concise producer-supplied decision summary,
not invented private model reasoning. Keep candidates, selected action and
execution receipt distinct. Do not emit `learning.update` merely because a
process is running or a checkpoint file exists.

Dashboard-launched roles receive `GLR_TELEMETRY_URL` and
`GLR_TELEMETRY_TOKEN`. HTTP producers send `glr.bridge-telemetry.v1` JSON to that
URL with `Authorization: Bearer TOKEN` and JSON Content-Type. Never put the token
in URLs, logs, presets, source packages or reports. The SDK uses HTTP when these
bindings exist, or GLR's local CLI with `GLR_CLI_PATH`/project bindings otherwise.
Independent producers must obtain the correct run and token through their
project's configuration channel; do not inspect unrelated process environments.

Agents can submit the same versioned batch without Python:

```powershell
glr --project . --json telemetry ingest --file batch.json
glr --project . --json telemetry ingest --file queue.jsonl --jsonl
```

Use the runtime schema for the exact envelope (`schema_version`, `run_id`,
`source`, `batch_id`, `events`, `metrics`). Preserve the same prepared batch ID and
content after an uncertain response. Reusing an ID with changed content fails.
Never retry gameplay actions because telemetry failed. The SDK does not provide
an automatic durable spool: persist prepared batches in a project-owned queue
if delivery must survive restart, and drain it before the run reaches terminal
state. Bound traffic off the game thread. Limits: 64 KiB per batch, 1–64 combined
events/metrics, 12 KiB per event payload. `_glr` and `authority` are reserved;
server provenance and diagnostic authority cannot be overridden.

For an in-process Python learner, call the direct store helper at the completed
update boundary. The arguments below come from the learner, not sample values:

```python
from game_learning_runtime.telemetry import Telemetry


def on_optimizer_update(step_id, measured_metrics, update_details):
    telemetry = Telemetry.from_env()
    if telemetry is not None:
        telemetry.learning_update(step_id=step_id, metrics=measured_metrics, details=update_details)
```

The helper commits the update event and its numeric metrics, then optionally
mirrors the event to stderr. `GLR_TELEMETRY_STDERR=0` disables that mirror, not
storage. Catch/report delivery failures at the diagnostic worker boundary without
retrying the optimizer or a game action. Use `BridgeTelemetry` for bridge source
state and workbench views so ingestion validates the schema and stamps source
provenance; raw JSONL and direct store events do not populate that source-state
projection automatically.

## Adapt the workbench without hardcoding games

Inspect `$defs.workbench` in `glr --json telemetry schema`. Send a complete view
under `bridge.state.payload.workbench`:

```json
{
  "schema_version": "glr.workbench.v1",
  "title": "Synthetic training view",
  "agent": "policy.example",
  "objective": "Compare candidate actions",
  "phase": "Evaluation",
  "sections": [
    {"id": "state", "title": "State", "kind": "stats",
     "fields": [{"label": "Health", "value": 72, "unit": "%"}]},
    {"id": "choices", "title": "Candidates", "kind": "table",
     "columns": ["Action", "Score", "Selected"],
     "rows": [["inspect", 0.8, true]]}
  ]
}
```

Choose labels, values and units from the adapter's domain. Combat may report
health/stamina and action candidates; economy games may report budget, inventory
and shop choices; survival games may report waves, elapsed time and upgrades.
These are mapping patterns, not proof of a working game adapter. Unknown events
still have a raw inspector. Route views require real `navigation.route_sample`
events with finite coordinates and explicit world/route/episode identity.

Supported sections: `stats`, `table`, plain `text`. IDs are unique; table rows
match column count. Maximums: 8 sections, 12 stat fields, 8 table columns, 40 rows,
240 characters per scalar string, 4,000 characters per text section, within the
outer payload budget. Latest state replaces the prior snapshot for
`run + source + kind`; include the full current view rather than partial patches.
Sources remain separate. Recorded status/phase is not a live connectivity check.

## Capture and register media

Read [recording.md](recording.md), then resolve `glr capture preset` and
`glr capture layout`. Keep recorder stderr connected to `capture.log`, including
output from `vx ffmpeg`; do not suppress FFmpeg errors. `GLR_LOG_STDERR=0` disables
terminal mirroring only. Never parse FFmpeg's encoded frame count as a GLR step.

Write finalized media beneath the current `GLR_RUN_DIR`. Using
`TrainingStore(GLR_STORE_PATH).register_artifact`, supply the actual `run_id`,
run-relative `path`, on-disk `source`, `role`, and `media_type`. This API records
size/digest; it does not copy files. Do not register an arbitrary external path
and expect the dashboard to serve it, or modify finalized evidence after hashing.

For example, after the recorder has closed a real `media/preview.mp4` beneath
the inherited run directory:

```python
import os
from pathlib import Path

from game_learning_runtime import TrainingStore

relative = "media/preview.mp4"
TrainingStore(os.environ["GLR_STORE_PATH"]).register_artifact(
    os.environ["GLR_RUN_ID"],
    path=relative,
    source=Path(os.environ["GLR_RUN_DIR"]) / relative,
    role="recording",
    media_type="video/mp4",
)
```

MP4/WebM playback, common raster images, Markdown and text previews are supported.
Markdown relative images/links resolve only to loaded registered artifacts;
HTML/SVG are download-only. Browser-local media preview is temporary and does not
upload, persist or associate a file with a run. Register it deliberately only if
the run association is real. A video alone is review media: episode/step seeking
requires a checked capture manifest, video identity and monotonic
`glr.capture-frame.v1` mapping. Browser playback does not rehash the whole video
or establish training eligibility.

## Read back, debug and archive

```powershell
glr --project . --json telemetry state RUN_ID
glr --project . --json runs trace RUN_ID --events-after -1 --metrics-after 0
glr --project . --json runs log RUN_ID --path trainer.log --offset 0
glr --project . --json report build RUN_ID
glr --project . --json backup create --output ../history-backup
glr --project . --json backup verify ../history-backup
glr --project . --json backup restore ../history-backup --output ../restored-history
glr --project . observe --archive ../restored-history
```

Continue independent event and metric cursors until exhausted. Browser exports
contain only the loaded window. For logs, continue `next_offset`; `/api/v1/log`
also supports a mutually exclusive `before` byte cursor for earlier pages.
Process logs initially show a 64 KiB tail; Earlier/Next/Read from start/Follow
latest browse the complete source with a bounded 16-page buffer. Partial JSON
records need their adjacent page before structured rendering. UTF-8 partial
characters are deferred, not discarded. Search applies to the loaded window.
Operation output remains a labelled 64 KiB tail; the job store retains the file.

When a panel is empty, distinguish: no source report; wrong run/context; only
legacy file output; paused observation; off-screen/filtered records; missing
artifact registration; truncated browser window; unsupported installed version.
Read back via CLI/API before changing an adapter or claiming loss. At minimum
verify one real published event and metric, latest source state, the intended
artifact registration, and persistence after reopening the observer.

Backups include committed SQLite state and completed-run files. Active runs are
database-only; make a fresh backup after completion for final recordings and
checkpoints. Verify before restoring into a new directory. Source packages are
for project code/configuration; history archives are for records and evidence.
Neither restores a running game or proves model compatibility. Backups are
explicit, without implicit retention, automatic scheduling or deletion.
