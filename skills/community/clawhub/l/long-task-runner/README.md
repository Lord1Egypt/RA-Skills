# Long Task Runner

This ClawHub distribution uses MIT-0. The canonical GitHub repository uses MIT. Source commit: 3e267399cc5db606556ecbd0ec8b3746429b790b.

[中文说明](README.zh-CN.md) · [Skill instructions](SKILL.md) · [MIT-0 License](LICENSE)

Let Python handle slow commands, queues, waiting, retries, and routine checks. Keep the coding agent for planning, exceptional decisions, and final review.

An Agent Skill with a standard-library Python runner. Built and tested on **Windows / PowerShell**. Useful for video and 3D rendering, baking, local TTS, transcription, document conversion, builds, long tests, downloads, data jobs, and already-submitted remote jobs.

**This does not promise zero-token waiting.** A detached worker is not an agent completion notification. Whether the assistant can resume automatically depends on the actual host tools.

## Install

With the Skills CLI:

```sh
npx skills add dhzyw/long-task-runner --skill long-task-runner --agent codex
```

Or clone into your agent's supported personal skills directory. For current Codex on Windows:

```powershell
git clone https://github.com/dhzyw/long-task-runner.git "$env:USERPROFILE\.agents\skills\long-task-runner"
```

Do not install a second copy if the skill already exists elsewhere. Inspect executable skills before running them. Requires **Python 3.10+**; the core has no pip dependencies. The optional media checker needs existing FFmpeg / ffprobe.

Ask your agent:

> Use $long-task-runner to run this render batch using the existing scripts. Let the local runner wait, keep logs bounded, and verify the outputs before final review.

## Try a cheap local demo

From this repository, choose a new demo directory:

```powershell
python scripts/make_demo.py --directory ./work/demo --seconds 3
python scripts/runner.py start --spec ./work/demo/demo.json --job ./work/demo/job
python scripts/runner.py wait --job ./work/demo/job --seconds 25
```

The generated spec uses real absolute paths to your interpreter and the demo script. It performs no network or model calls. A successful result requires both exit code 0 and the expected JSON content.

## Fresh chats and reusable experience

After a complete task has been delivered, independent new work in the same conversation gets one reminder: start a fresh chat with a compact handoff, and optionally create or update a reusable skill from the proven workflow. Revisions of the same artifact, retries, and unfinished batch steps continue without a reminder.

The handoff carries verified methods, script locations, applicable preferences, and validation criteria. It does not copy the conversation history. Opening a chat and creating a skill are independent, opt-in choices; without a thread-creation tool, the assistant supplies a copyable starting prompt.

This is assistant guidance when the skill is selected, not a global chat listener or a promise of measured token savings. See the [handoff guide](references/task-handoff.md) and [compact template](assets/task-handoff-template.md).

## Interfaces

All commands take `--job <job-directory>`.

| Command | Purpose |
|---|---|
| `start --spec job.json` | Persist the configuration and launch a hidden worker; repeated starts of the same job do not launch it again |
| `status [--since REVISION]` | Read one small snapshot; optionally coalesce changes by task |
| `wait --seconds 25` | Wait locally for a terminal state or a bounded window; at most 55 seconds per invocation |
| `cancel` | Request termination of the local process tree; check the resulting state |
| `resume --replay-safe` | Resume only tasks explicitly declared safe to replay; recheck and skip completed tasks |
| `logs --bytes 4096` | Read a bounded log tail when an error needs investigation |

`wait` exits 0 on success, 2 on failure/interruption, and 3 while still active. Successful control/status commands exit 0 even if the job itself failed: inspect the JSON `status`.

## Guarantees and limits

- Sequential queues, per-job time limits, cross-job resource locks, atomic JSON state, failure IDs, and bounded rotating logs.
- Retries are off by default. Automatic retries require an explicit safe-replay declaration and allowed nonzero exit codes. Timeouts and validation failures are not automatically replayed.
- External mutations and paid submissions cannot be automatically retried or resumed. A read-only remote watcher tracks an existing job ID; cancelling the watcher does not cancel remote execution or billing.
- Completion means exit status **and configured checks** passed. Built-in checks cover fresh/nonempty files, JSON assertions, complete WAV data and duration, SHA-256, and read-only validators. Final visual/audio/business review remains necessary.
- Windows Job Objects contain descendants and terminate them when the worker exits or crashes. Commands must run in the foreground until their work finishes; this is not a service manager.
- CPU/RAM/GPU limits belong in application parameters. Resource locks coordinate cooperating runners; they are not hardware quotas or distributed locks.
- macOS/Linux paths are experimental. Normal process-group cleanup exists; worker-crash recovery cannot offer Windows-equivalent containment and is blocked for unverified active remnants.
- Job identity hashes the JSON spec, not input files or scripts. Use a new job directory after changing inputs. A safe-replay flag is a caller assertion, not proof of idempotency.
- No agent/model client, scheduled automation, hidden wakeup bridge, or global configuration modification is built in. Authorized local inference commands such as TTS remain the user's workload.

Read the short [SKILL.md](SKILL.md) first. Detailed references are loaded only when relevant: [job configuration](references/job-spec.md), [scenario table](references/scenarios.md), [host waiting](references/host-waiting.md), and [optional compression](references/optional-compression.md). Some detailed references are currently in Chinese.

## Tests and measurements

```powershell
python scripts/test_runner.py --root ./work/tests --report ./work/runner-tests.json
python scripts/test_remote.py --root ./work/tests --report ./work/remote-tests.json
python scripts/benchmark.py --directory ./work/benchmarks --report ./work/benchmark.json --seconds 6
```

The initial Windows validation passed 36 process tests and 8 loopback HTTP cases. It covered cancellation, worker crashes, duplicate starts, safe recovery, stale/corrupt outputs, validators, Unicode paths, log flooding, and coalesced events. See [CI](https://github.com/dhzyw/long-task-runner/actions) for checks on the published revision.

In one six-second demo, a local consumer making a status call every second used 8 CLI calls and returned 5,265 bytes; a consumer using one bounded wait used 2 calls and returned 1,434 bytes. Both consumers ran inside a local benchmark script. **These are interface calls and stdout/stderr bytes, not measured model requests, tokens, or billing savings.** Paths and timing affect the numbers; rerun the benchmark in your environment.

## Contributing

Focused fixes with reproductions are welcome. Keep the core dependency-free, keep logs bounded, preserve failure evidence and replay restrictions, and test Windows process cleanup when changing lifecycle code. Do not add new background agent calls or automatic external submissions.

Architectural inspiration: [HiveScanner](https://github.com/dhruvil009/hivescanner) for local event handling; [Turnlock](https://github.com/fanilosendrison/turnlock) for deterministic workflows with explicit judgment points. [RTK](https://github.com/rtk-ai/rtk) and [Context Mode](https://github.com/mksglu/context-mode) are optional output-handling ideas, not dependencies or endorsed integrations. No upstream code is bundled.
