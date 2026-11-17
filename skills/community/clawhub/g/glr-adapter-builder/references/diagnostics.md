# Adapter diagnostics for the agent workbench

Read before adding learning visibility, process output, custom data panels, or
media production. The runtime owns gameplay semantics and authoritative receipts;
the diagnostic path never grants action authority or supplies rewards.

1. Resolve `glr --version`, project/context and the role's inherited
   `GLR_RUN_ID`, `GLR_STORE_PATH`, and `GLR_RUN_DIR`. Use
   `glr --json telemetry schema` as the installed capability contract.
2. Keep observation/action/lifecycle APIs learner-neutral. Emit actual
   `agent.decision`, `agent.execution`, `learning.update`, and route observations
   at their owning boundary. Include exact `episode_id` and `step_id` when known;
   omit unknown values rather than guessing correlations.
3. For Python, `BridgeTelemetry.from_env("bridge.stable-source")` prepares and
   sends versioned events/metrics. For other runtimes, use the same HTTP envelope
   and bearer token supplied by the role environment, or
   `glr telemetry ingest --file batch.json`. Read `$defs.workbench` for optional
   game-neutral panels. Never hardcode a game name into GLR's frontend to add
   adapter fields.
4. Publish `bridge.state.payload.workbench` with schema `glr.workbench.v1`, a
   `title`, and `sections`. `stats` has labelled scalar fields and optional units;
   `table` has columns and equal-width scalar rows; `text` has plain text.
   Optional `agent`, `objective`, and `phase` are producer descriptions. Each
   source publishes a complete snapshot: latest state replaces its previous
   `run + source + kind` value. Keep distinct sources separate.
5. Provide `summary`, `input`, `output`/`receipt`, and measured `duration_ms` on
   process events when available. Summaries are recorded explanations, not
   inferred model reasoning. A process start or FFmpeg frame is not a learner
   update. Numeric chart signals must be explicitly recorded as metrics.
6. Legacy roles may emit UTF-8 JSONL with one complete object per flushed line.
   The workbench can render it without migration, but file records stay separate
   from typed events and metrics. Forward recorder stdout/stderr, including
   `vx ffmpeg` progress/errors, to the managed capture log. Do not silence errors
   merely to make output easier to parse.
7. Keep reporting off the game thread, bounded and passive. Reuse the same
   prepared batch ID/content after uncertain delivery; never repeat a game
   action because diagnostics failed. Persist a project-owned queue if delivery
   must survive restart and drain it before terminal run status. Limits are
   64 KiB per batch, 1–64 records, 12 KiB per event; reject or reduce oversized
   snapshots rather than silently truncating evidence.
8. Write finalized artifacts under the actual run directory, then register
   their run-relative path, source file, role, media type and digest via the
   run store. Registration does not copy data. Videos need matching capture
   manifests and indexed steps for event seeking; screenshots/video alone do
   not prove training quality. Do not auto-associate external files by timestamp.
9. Verify HTTP/CLI readback of source state, events and metrics, inspect the
   structured process view, reopen the observer, and verify a completed-run
   archive. Record schema/identity errors and unknown delivery separately from
   gameplay success. Do not rewrite history to conceal missing collection.

Example domain mappings: combat state/candidates, economy/budget/inventory,
survival/wave/loadout, or adapter-defined data. The same views work without
asserting any specific game is integrated. Tables are bounded to 8 columns and
40 rows, stats to 12 fields, and views to 8 sections; the containing payload
budget still applies. Do not send HTML/JS, inline image/video bytes, credentials,
machine bindings or private account details as presentation data.

When the `glr-cli` Skill is also installed, its `references/data-collection.md`
contains Python examples and the complete operator/readback workflow. These
instructions and the installed CLI schema suffice for standalone adapter work.
