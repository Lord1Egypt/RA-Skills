# Inspector Runtime Design

## Separation of concerns

### Skill directory

Keep reusable code and documentation in:

- `~/.openclaw/skills/inspector/`

This directory should contain:
- `SKILL.md`
- `scripts/`
- `references/`

Do **not** keep mutable runtime registry, logs, or state here.

### Runtime directory

Keep mutable runtime data in:

- `~/.openclaw/inspector/`

Suggested layout:

```text
~/.openclaw/inspector/
├── registry.json
├── config.env
├── state/
├── logs/
└── systemd/
```

## registry.json schema

Recommended shape:

```json
{
  "sessions": [
    {
      "session_id": "a13ec701-e0ef-4eac-b8cc-6159b3ff830c",
      "session_key": "optional-stable-key",
      "delivery_channel": "telegram",
      "delivery_target": "8298444890",
      "delivery_account_id": "codingtg",
      "agent": "coding",
      "workspace": "/home/ubuntu/http-server/dev/dual-tls-socks5-tunnel",
      "registered_at": "2026-03-26T22:30:00+08:00",
      "enabled": true,
      "profile": "default",
      "inactive_threshold_seconds": 1800,
      "cooldown_seconds": 3600,
      "running_cooldown_seconds": 600,
      "blocked_cooldown_seconds": 3600,
      "notes": "optional note"
    }
  ]
}
```

## Field meanings

- `session_id`: primary session identifier for inspection
- `session_key`: optional alternate stable session reference
- `agent`: agent name
- `delivery_channel`: explicit IM channel used for visible delivery override
- `delivery_target`: explicit target passed to CLI `--to` for visible delivery
- `delivery_account_id`: explicit channel account / bot identity used for visible delivery
- `workspace`: associated repo/workdir
- `registered_at`: registry write time
- `enabled`: whether this session is actively inspected
- `profile`: named policy profile
- `inactive_threshold_seconds`: no-message threshold for inactive inspection
- `cooldown_seconds`: generic resend cooldown
- `running_cooldown_seconds`: cooldown after `STATUS: RUNNING`
- `blocked_cooldown_seconds`: cooldown after `STATUS: BLOCKED`
- `notes`: freeform operator note

## config.env suggestions

Example:

```bash
SCAN_INTERVAL_SECONDS=30
DEFAULT_INACTIVE_THRESHOLD_SECONDS=1800
DEFAULT_COOLDOWN_SECONDS=3600
DEFAULT_RUNNING_COOLDOWN_SECONDS=600
DEFAULT_BLOCKED_COOLDOWN_SECONDS=3600
DEFAULT_MAX_LAST_ACTIVITY_AGE_SECONDS=43200
DEFAULT_MAX_STATUS_LOOKBACK_MESSAGES=5
```

## Global service convention

Recommended service name / label:

- Linux systemd: `openclaw-inspector.service`
- macOS launchd label: `openclaw-inspector`
- Windows scheduled task name: `openclaw-inspector`

Recommended script entrypoint:

- `~/.openclaw/skills/inspector/scripts/watch-registered-sessions.js`

Runtime home should contain generated data only, not copied script entrypoints.

Recommended behavior:
- inspect only registry sessions
- ignore disabled entries
- maintain per-session state under `state/`
- write diagnosis and delivery logs under `logs/`
- use `[SYSTEM_INSPECTION]` as the prompt title

## Suggested state behavior

- `STATUS: DONE` → suppress until new activity
- `STATUS: WAITING` → suppress until new user-side progress
- `STATUS: BLOCKED` → apply blocked cooldown
- `STATUS: RUNNING` → apply running cooldown and preferably verify a live execution chain before trusting it
