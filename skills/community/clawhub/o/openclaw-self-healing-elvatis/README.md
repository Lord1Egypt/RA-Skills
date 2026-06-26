# openclaw-self-healing-elvatis

**Current version: `0.2.16`**

OpenClaw plugin that improves resilience by automatically fixing reversible failures.

## What it heals

- **Model outage** — Detect rate limit / quota / auth-scope failures, put model into cooldown, patch pinned session to a safe fallback
- **WhatsApp disconnect** — If WhatsApp appears disconnected repeatedly: restart the gateway (streak threshold + minimum restart interval guard)
- **Cron failures** — If a cron job fails repeatedly: disable it + create a GitHub issue
- **Plugin crashes** — If a plugin reports `status=error` or `status=crash`: auto-disable + GitHub issue

## Changelog

### v0.2.16 — 2026-04-10
**Fix fallback model in modelOrder: gpt-5.1 -> gpt-5.2-codex**
`openai-codex/gpt-5.1` does not exist in the CLI bridge allowlist, causing
"model not allowed" errors when the self-heal plugin tried to failover.
Fixed to `vllm/openai-codex/gpt-5.2-codex` which routes through the CLI bridge.

Updated modelOrder:
1. `vllm/cli-claude/claude-sonnet-4-6`
2. `vllm/openai-codex/gpt-5.2-codex`
3. `github-copilot/claude-sonnet-4.6`

### v0.2.15 — 2026-04-10
**Revert default modelOrder back to CLI models**
The CLI bridge proxy (v2.3.0) now supports tool calling, multimodal content,
and autonomous execution. CLI models can be used as primary models for all
use cases including agents that need tools.

Reverted default order back to CLI models:
1. `vllm/cli-claude/claude-sonnet-4-6` (CLI proxy — full tool support via v2.3.0)
2. `openai-codex/gpt-5.1` (OpenAI API — full tool support)
3. `github-copilot/claude-sonnet-4.6` (Copilot-routed — full tool support)

### v0.2.14 — 2026-04-10
**Fix: Default modelOrder must use tool-capable models only**
Temporary fix: switched to API models while CLI bridge lacked tool support.
Reverted in v0.2.15 after CLI bridge v2.3.0 added tool calling.

### v0.2.13 — 2026-04-10
Version bump to trigger npm + ClawHub publish via GitHub release CI.

### v0.2.12 — 2026-04-10
**Fix: Default model fallback order used Google Gemini CLI as last resort**
The default `modelOrder` included `google-gemini-cli/gemini-2.5-flash` as the final fallback.
Google Gemini CLI models have no system permissions (cannot write files or execute tools),
making the plugin non-functional when all higher-priority models were in cooldown.

Updated default order to use only models with full system/write permissions:
1. `vllm/cli-claude/claude-sonnet-4-6` (Claude CLI — full permissions)
2. `openai-codex/gpt-5.1` (OpenAI Codex — write access)
3. `github-copilot/claude-sonnet-4.6` (Copilot-routed Claude — write access)

Also fixed mismatch between `DEFAULT_MODEL_ORDER` in code and the `openclaw.plugin.json`
schema default — both now use the same values.

### v0.2.11 — 2026-03-19
**Feature: Heal metrics export to JSONL**
Heal events are now written to `~/.aahp/metrics.jsonl` (configurable via `metricsFile` config key).
Each entry is a JSON line with `ts`, `plugin`, `event`, and event-specific fields:
- `{ ts, plugin, event: "model-cooldown", model, reason, cooldownSec, trigger }`
- `{ ts, plugin, event: "session-patched", sessionKey, oldModel, newModel, trigger }`
- `{ ts, plugin, event: "whatsapp-restart", disconnectStreak }`
- `{ ts, plugin, event: "cron-disabled", cronId, cronName, consecutiveFailures }`
- `{ ts, plugin, event: "model-recovered", model, isPreferred }`

Metrics writes are skipped in dry-run mode. The parent directory is created automatically.
Closes #12.

### v0.2.10 — 2026-03-08
Docs fix: README and STATUS.md version headers were stuck at 0.2.8 after v0.2.9 bump; SKILL.md missing version footer; add universal release-rule to CONVENTIONS.md.

### v0.2.9 — 2026-03-07
**Fix: Plugin health monitoring JSON parsing**
Extract JSON from stdout before parsing — channels subprocess output includes
non-JSON log lines (e.g. `[INFO] ...`) before the JSON payload, causing parse
failures in plugin health checks.

### v0.2.8 — 2026-03-07
**Fix: Infinite gateway restart loop**
`lastRestartAt` and `disconnectStreak` are now saved to disk **before** calling
`openclaw gateway restart`. Previously they were saved after, but systemd kills
the process during restart — state was never persisted, the rate-limit guard was
bypassed on every boot, causing an infinite restart loop when used alongside
any plugin that triggers a config-driven gateway restart (e.g. `openclaw-cli-bridge-elvatis`).

### v0.2.7 — 2026-03-07
Fix `runCommandWithTimeout` call signature + field name.

### v0.2.6 — 2026-03-02
Status snapshot file, startup config validation, integration tests.

### v0.2.5 and earlier
Model failover, WhatsApp reconnect, cron failure, dry-run mode, active recovery probing, config hot-reload.

## Install

From ClawHub:

```bash
clawhub install openclaw-self-healing-elvatis
```

For local development:

```bash
openclaw plugins install -l ~/.openclaw/workspace/openclaw-self-healing-elvatis
openclaw gateway restart
```

## Config

```json
{
  "plugins": {
    "entries": {
      "openclaw-self-healing": {
        "enabled": true,
        "config": {
          "modelOrder": [
            "vllm/cli-claude/claude-sonnet-4-6",
            "openai-codex/gpt-5.1",
            "github-copilot/claude-sonnet-4.6"
          ],
          "cooldownMinutes": 300,
          "autoFix": {
            "patchSessionPins": true,
            "disableFailingPlugins": false,
            "disableFailingCrons": false,
            "issueRepo": "elvatis/openclaw-self-healing-elvatis"
          }
        }
      }
    }
  }
}
```

`autoFix.issueRepo` must use `owner/repo` format. Invalid values are ignored and the plugin falls back to `GITHUB_REPOSITORY` (if valid) or `elvatis/openclaw-self-healing-elvatis`.

### Config validation

The plugin validates configuration at startup and refuses to start if any value is invalid. All validation errors are logged via `api.logger.error` before the plugin exits.

| Key | Valid range | Default |
|-----|------------|---------|
| `modelOrder` | At least one entry (non-empty array) | 3 default models |
| `cooldownMinutes` | 1 - 10080 (1 minute to 1 week) | 300 |
| `probeIntervalSec` | >= 60 | 300 |
| `autoFix.whatsappMinRestartIntervalSec` | >= 60 | 300 |
| `stateFile` | Parent directory must be writable | `~/.openclaw/workspace/memory/self-heal-state.json` |
| `statusFile` | Path to status snapshot JSON | `~/.openclaw/workspace/memory/self-heal-status.json` |

## Status file

On every monitor tick (60s), the plugin writes a JSON status snapshot to `statusFile`. External scripts, dashboards, or other plugins can poll this file without subscribing to the event bus.

Default path: `~/.openclaw/workspace/memory/self-heal-status.json`

The file is written atomically (write to `.tmp` then rename) to prevent partial reads. The JSON structure matches the `StatusSnapshot` type:

```json
{
  "health": "healthy | degraded | healing",
  "activeModel": "vllm/cli-claude/claude-sonnet-4-6",
  "models": [
    {
      "id": "vllm/cli-claude/claude-sonnet-4-6",
      "status": "available | cooldown",
      "cooldownReason": "rate limit (only when in cooldown)",
      "cooldownRemainingSec": 1234,
      "nextAvailableAt": 1700001234,
      "lastProbeAt": 1700000900
    }
  ],
  "whatsapp": {
    "status": "connected | disconnected | unknown",
    "disconnectStreak": 0,
    "lastRestartAt": null,
    "lastSeenConnectedAt": 1700000000
  },
  "cron": { "trackedJobs": 2, "failingJobs": [] },
  "config": { "dryRun": false, "probeEnabled": true, "cooldownMinutes": 300, "modelOrder": ["..."] },
  "generatedAt": 1700000000
}
```

Fields `cooldownReason`, `cooldownRemainingSec`, `nextAvailableAt`, and `lastProbeAt` on model entries are only present when the model is in cooldown.

## Notes

Infrastructure changes remain ask-first.

## Critical Guardrail: openclaw.json validation

This plugin treats `~/.openclaw/openclaw.json` as a boot-critical file.

Before any self-heal action that could restart the gateway or change cron/plugin state, it verifies:
- the config file exists
- it is valid JSON

If the config is invalid, the plugin will refuse to restart the gateway to avoid restart loops.

It also creates timestamped backups before restarts or disruptive changes:
`~/.openclaw/backups/openclaw.json/openclaw.json.<timestamp>.bak`
