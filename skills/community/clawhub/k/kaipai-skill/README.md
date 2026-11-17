# Kaipai AI (OpenClaw skill)

Process images and video with **Kaipai AI**: watermark removal and quality restoration. Works inside [OpenClaw](https://github.com/openclaw/openclaw) with a single CLI entrypoint: `scripts/kaipai_ai.py`.

## Capabilities

Run `python3 scripts/kaipai_ai.py capabilities` to see the modules included in your package.
Core image/video processing works without notification providers and returns result URLs.
Optional delivery modules are loaded only when selected; omitted providers cannot be used.

Calls go to the **Kaipai commercial API** and **consume account quota** (credits) for the configured **MT_AK** tenant. Agents must not tell users the service is free or guess pricing — see [SKILL.md](SKILL.md) (*Billing and user-facing claims*).

Executable task IDs are server-driven. The skill supports image/video watermark removal and quality restoration, but callers must discover current IDs before naming or running a task.

## Install

Install the skill folder as your OpenClaw skill (path or marketplace URL your host documents), then restart the gateway if required.

## One-time setup

1. Put **MT_AK** and **MT_SK** in `scripts/.env` (or export them in the environment).
2. Run:

```bash
python3 scripts/kaipai_ai.py preflight
```

Output must be `ok`.

## Dependencies

```bash
python3 scripts/kaipai_ai.py install-deps
```

Uses `scripts/requirements.txt` (e.g. `requests`, OSS client as needed).

## Discover current tasks

```bash
python3 scripts/kaipai_ai.py catalog
python3 scripts/kaipai_ai.py catalog --media-type video
```

V2 output includes `material_id`, `name`, `description`, and `media_type`. Select by the display fields, then pass the exact returned `material_id` to `--task`; this avoids ambiguity when display names repeat. A legacy alias is valid only when the response is explicitly `config_mode: legacy` and returns that alias. Configuration failure stops the flow; no local task fallback is used. This command does not upload media, consume quota, or submit an algorithm job.

## URL inputs (`--input https://...`)

- **Shell:** Quote the full URL so `&` in query strings is not broken (e.g. signed storage URLs).
- **Limits:** Streamed download with **15s connect / 120s read** timeouts and **100MB** max by default (shared with `resolve-input --url`). Override: `MT_AI_URL_CONNECT_TIMEOUT`, `MT_AI_URL_READ_TIMEOUT`, `MT_AI_URL_MAX_BYTES`.
- **Large or slow media:** Use `resolve-input --url …` to save locally, then pass the returned `path` as `--input`.

## Quick examples

**Image watermark removal (blocking):**

```bash
python3 scripts/kaipai_ai.py run-task \
  --task "<image_catalog_material_id_or_confirmed_legacy_alias>" \
  --input "https://example.com/photo.jpg"
```

**Video task (async worker payload):**

```bash
python3 scripts/kaipai_ai.py spawn-run-task \
  --task "<video_catalog_material_id_or_confirmed_legacy_alias>" \
  --input "https://example.com/clip.mp4" \
  --deliver-to "oc_xxx_or_ou_xxx" \
  --deliver-channel none
```

Pass the printed `sessions_spawn_args` to OpenClaw `sessions_spawn`. Keep **`runTimeoutSeconds`** at the payload default (**3600**); do not reduce it without accepting timeout risk. Wall time varies. If a host **session/tool wait cap** cuts off before JSON finishes, recover with **`last-task`** / **`history`** / **`query-task`** (see [SKILL.md](SKILL.md) and [docs/errors-and-polling.md](docs/errors-and-polling.md)).

**Two-stage video** (watermark removal then restoration): select both video task entries from the remote catalog and use their `material_id` values, then run **`spawn-run-task` + `sessions_spawn` twice** — one embed per stage. After the first worker finishes, pass its **`primary_result_url`** as the second stage's **`--input`**.

**Resume polling by task id:**

```bash
python3 scripts/kaipai_ai.py query-task --task-id "<full_task_id>"
```

**Last run / history (local state under `~/.openclaw/workspace/openclaw-kaipai-ai/`):**

```bash
python3 scripts/kaipai_ai.py last-task
python3 scripts/kaipai_ai.py history
```

**IM attachment → local path for `--input`:**

```bash
python3 scripts/kaipai_ai.py resolve-input --telegram-file-id "AgAC..." --output-dir /tmp
```

See [docs/im-attachments.md](docs/im-attachments.md) and [SKILL.md](SKILL.md) for agents.

## Build the Skill package

```bash
python3 scripts/package_skill.py
```

The default still includes both Feishu and Telegram delivery for compatibility. Select a smaller package explicitly:

```bash
python3 scripts/package_skill.py --channels none
python3 scripts/package_skill.py --channels feishu
python3 scripts/package_skill.py --channels telegram --include-sdk
```

Non-default variants have a `-channels-<selection>` suffix, so they do not overwrite one another.
Their file allowlist, `scripts/features.json`, metadata, CLI provider choices and delivery instructions
match the selected modules. No-provider packages omit notification code and return result links.
Input URL/IM attachment resolution remains core functionality; these switches select delivery modules only.

The unified source retains `upload`, `notify` (when a provider is bundled), `list-tasks`,
global `--ak`/`--sk`, and the `kaipai_ai.py` legacy entrypoint. This entrypoint uses the
same Kaipai configuration; invoking it does not switch to domestic services. Prefer environment
credentials to avoid command-history exposure; configure worker credentials in the host or `.env`.
SDK `execute` and `query` aliases remain available with `--include-sdk`.

### Video metadata for bundled notification providers

When `capabilities` lists a bundled delivery channel, `notify` can include a cover and duration:

```bash
python3 scripts/kaipai_ai.py notify \
  --channel "<bundled-channel>" --type video \
  --source /path/to/video.mp4 --to "<recipient-id>" \
  --cover-url "https://example.com/cover.jpg" --duration-ms 120000
```

`--duration-ms` and the provider API `send_video(..., duration_ms=120000)` always mean
milliseconds. Telegram converts to whole seconds, rounding up (1500 ms becomes 2 s).
Both new CLI options apply only to video. With no bundled provider, `notify` is unavailable.

Existing callers do not need to change: provider `duration` and independent sender
`--duration` keep their original units (Feishu: milliseconds; Telegram: seconds).
Do not combine `duration_ms` with a nonzero legacy `duration`; this is rejected before
credentials, upload or sending. Omitting the new parameter preserves the existing behavior.

Creates `dist/kaipai-<version>-<YYYYMMDD-HHMMSS>.zip` and its `.zip.sha256` checksum.
Use `--brand kaipai` to generate the Kaipai distribution, named
`kaipai-<version>-<YYYYMMDD-HHMMSS>.zip`, including its generated Skill card.
Brand conversion does not translate all prompts or documentation.
Use `--outdir /path/to/output` to select another directory, or `--force` to
replace an existing artifact with the same timestamp. Offline tests run before packaging; `--skip-tests`
is available for a previously verified build.

The default ZIP contains `openclaw-kaipai-ai/` with Skill instructions, runtime
scripts, documentation, the credential example, and the standalone `install.sh`
migrated from the sprint packager. The Skill runs through `scripts/kaipai_ai.py`;
the separate `sdk/` directory is excluded by default. A strict file allowlist excludes real `.env`
files, tests, caches, media, and build tools. Configured AK/SK values and private
key material are checked without printing their contents. Version constants and
required SBOM files are validated before artifacts are written.

To retain the legacy Python SDK and SDK CLI for existing integrations:

```bash
python3 scripts/package_skill.py --include-sdk
```

This creates `dist/kaipai-<version>-full-<YYYYMMDD-HHMMSS>.zip` and its checksum, with
the same Skill entry point plus `sdk/`. The separate name keeps the full and
Skill-only packages available side by side.

Runtime dependencies are in `scripts/requirements.txt`. Maintainers can install
test dependencies with `python3 -m pip install -r scripts/requirements-dev.txt`;
the development requirements are excluded from both release packages.

After extracting, install into your project's Skill directory:

```bash
bash openclaw-kaipai-ai/install.sh codex-project /path/to/project
# Or for OpenClaw:
bash openclaw-kaipai-ai/install.sh openclaw-workspace /path/to/workspace
```

Existing `scripts/.env` credentials are preserved by the installer.

## Operators

**One line:** Video tasks → **`spawn-run-task`** (not a blocking **`run-task`** in the main session); if a job was cut off or the user asks for status → **`last-task`** / **`query-task`** — never submit **`run-task`** again for the same **`task_id`**.

**New jobs:** Agents must submit only via **`kaipai_ai.py run-task`** (or the same command inside **`spawn-run-task`**); do not call AIGC/wapi directly and skip **`/skill/consume.json`** — see [SKILL.md](SKILL.md) section **API submission path (MANDATORY)**.

## Docs

- [SKILL.md](SKILL.md) — agent instructions
- [docs/multi-platform.md](docs/multi-platform.md) — delivery (Feishu, Telegram, Discord, …)
- [docs/errors-and-polling.md](docs/errors-and-polling.md) — env vars, polling, failures
- [docs/feishu-send-video.md](docs/feishu-send-video.md) — Feishu native video send

## License

MIT (see repository root if present).
