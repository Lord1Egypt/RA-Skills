# Home Assistant Skill

An AI agent skill for inspecting Home Assistant capabilities and controlling authorized devices and automations. REST examples cover 25 entity domains; optional read-only WebSocket workflows add registries, Assist discovery, automation validation, energy statistics and repair diagnostics.

Works with [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenClaw](https://github.com/openclaw/openclaw), [Cursor](https://cursor.com), and any tool supporting the [SKILL.md](https://agentskills.io) standard.

[![ClawHub](https://img.shields.io/badge/ClawHub-homeassistant--skill-blue)](https://clawhub.ai/anotb/homeassistant-skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Part of [unsol.dev](https://unsol.dev)

## Prerequisites

- Home Assistant instance with API access
- Bash, `curl` and `jq` for the shell examples, or Python 3.10+ for the optional read-only helper (standard library only)

OpenClaw readiness still requires both `curl` and `jq`, plus `HA_URL` and `HA_TOKEN`,
as declared in the skill metadata. Python alone runs the standalone read-only
helper but does not satisfy those OpenClaw dependency gates.

## Installation

### Claude Code

```bash
git clone https://github.com/anotb/homeassistant-skill.git ~/.claude/skills/homeassistant-skill
```

### OpenClaw (via ClawHub)

```bash
clawhub install homeassistant-skill
```

### Cursor / Other

Clone to your agent's skill directory.

## Configuration

1. Supply an existing Home Assistant access token through your local environment or secret store. Credential creation requires separate authorization.
2. Set environment variables:

```bash
export HA_URL=http://10.0.0.10:8123
export HA_TOKEN=your-long-lived-access-token
```

Use a trusted base origin without `/api`; the helper refuses credentials embedded
in URLs, redirects and malformed settings. Prefer verified HTTPS. Local HTTP sends
the token without encryption. Never paste tokens into chat, commit `.env` files,
enable shell tracing, or put tokens in command arguments.

The token inherits its HA user's permissions; its theft can expose household
data and allow device actions. Reader allowlists do not reduce the token's
server-side permissions. Use an existing account with suitable access and keep
presence, location, calendar and history results private unless sharing is
authorized. The Bash examples pass headers through stdin and require curl 7.55+.

The shell examples use Bash. On Windows the read-only helper works with `python`:

```powershell
# Set HA_URL and HA_TOKEN privately in this process before running.
python scripts/ha_read.py get /api/
python scripts/ha_read.py profile
python scripts/ha_read.py action-schema light.turn_on
python scripts/ha_read.py health
python scripts/ha_read.py get /api/services
python scripts/ha_read.py get /api/states/sensor.temperature
python scripts/ha_read.py calendar calendar.personal --days 7
python scripts/ha_read.py forecast weather.home --type daily
```

Use `python3` on platforms where that is the Python 3 command. Paths are relative
to the skill directory. The helper deliberately has no device-control command.
It makes direct connections, ignores proxy environment variables, verifies TLS,
refuses redirects, bounds socket waits (default 30 seconds, maximum 120) and
responses (8 MiB), and does not retry. Output can include private state, location
or calendar information; keep it local or redact before sharing.

## What You Can Do

The [modern workflow guide](references/modern-workflows.md) describes capability
discovery, device/entity mapping, Assist and existing MCP context, automation
inspection, energy/statistics reads and release compatibility checks. For optional
WebSocket reads, use a local Python environment with `requirements-websocket.txt`:

```bash
python -m pip install -r requirements-websocket.txt
python scripts/ha_ws_read.py read areas
python scripts/ha_ws_read.py read assist-pipelines
python scripts/ha_ws_read.py definition automation.evening_routine
python scripts/ha_ws_read.py read energy-preferences
python scripts/ha_ws_read.py read repairs
```

Install dependencies on the agent's computer/environment, not on Home Assistant.
The REST helper stays dependency-free. WebSocket queries have no generic command,
subscription, retry or device-control path. An administrator account is required
for definition reads; unavailable or unauthorized commands fail without changing
permissions. Schema validation never executes the supplied actions.

| Domain | Actions |
|--------|---------|
| Switches | Turn on, off, toggle |
| Lights | On/off, brightness, color, color temp |
| Scenes | Activate scenes |
| Scripts | List, run, run with variables |
| Automations | Trigger, enable, disable |
| Climate | Set temperature, HVAC mode |
| Covers | Open, close, set position (blinds, garage) |
| Locks | Lock, unlock (with safety confirmation) |
| Fans | On/off, speed |
| Media players | Play, pause, volume |
| Vacuum | Start, return to dock |
| Alarm | Arm, disarm (with safety confirmation) |
| Notifications | Send to mobile devices, list targets |
| Person / Presence | Who is home, device locations |
| Weather | Current conditions, daily/hourly forecast |
| Input helpers | Boolean, number, select, text, datetime |
| Calendar | List calendars, upcoming events |
| Text-to-Speech | Speak messages on media players |
| Sensors | Read temperature, humidity, power, etc. |
| Areas & Floors | Discover areas, floors, entities by area |
| History | Entity state history, logbook |
| Templates | Evaluate Jinja2 templates server-side |

## Usage Examples

```bash
# "Turn on the office light at 80%"
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 -X POST "$HA_URL/api/services/light/turn_on" \
  -H @- \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.office", "brightness_pct": 80}'

# "What's the temperature?"
printf 'Authorization: Bearer %s\n' "$HA_TOKEN" | curl -q -fsS --noproxy '*' --connect-timeout 5 --max-time 30 "$HA_URL/api/states" -H @- \
  | jq '.[] | select(.attributes.device_class == "temperature") | {name: .attributes.friendly_name, temp: .state, unit: .attributes.unit_of_measurement}'
```

## Agent connection options

| Route | Useful for | Requirements and limits |
| --- | --- | --- |
| Native Home Assistant MCP | Routine home queries and authorized control through discovered tools | An existing MCP connection; selected LLM APIs and account determine access |
| Direct REST | State, schema, profile, calendar, forecast and history reads; explicit authorized cookbook actions | Trusted origin and existing token; Assist exposure does not limit this token |
| Direct WebSocket | Registries, Assist configuration, Energy statistics, repairs and validation | Same existing credentials plus the optional local dependency; commands vary by HA version and permissions |

Use MCP when its tools cover the task, then use direct reads for details those
tools do not provide. The skill supports both routes without a custom server or
HA integration. Setting up a new connection, granting access or making HA
reachable from the internet requires separate authorization. See
[modern workflows](references/modern-workflows.md) for scope and query examples
and the [official MCP setup guide](https://www.home-assistant.io/integrations/mcp_server/)
for client-specific connection instructions.

## Validation

Run the suite from the repository root. REST tests use the standard library;
WebSocket loopback tests require the optional dependency and report a skip if it
is absent. The client is exercised against supported websockets releases 15.0.1
and 17.2; Python 3.10+ is supported (newer dependency releases may require 3.11+).

```bash
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
git diff --check
```

Tests use a loopback mock HTTP server, fake credentials and no real Home Assistant
access. They verify response-data handling, encoded calendar bounds, exact reads,
redirect refusal, credential redaction, limits and non-retry behavior. Additional
tests cover WebSocket authentication/correlation, query allowlists, permission and
missing-command errors, registry/Assist/energy command construction, target/schema
validation and safe version/schema/availability reports.

For live verification, supply the trusted HA origin and an **existing** token
privately through the local environment. First run only `get /api/`,
`get /api/config`, `get /api/services`, and `get /api/states/ENTITY_ID` for one
user-selected sensor. Report the HA version, HTTP results and response shape,
not the token or full configuration. A browser login alone does not provision the
CLI's environment. No credential creation, device actions, security changes,
publishing or pushes are part of this test. Forecast and calendar reads are
optional separate checks after the user selects those entities.

Prefer `profile` and `action-schema` for reports that omit full sensitive config.
Through an accessible already signed-in HA frontend, inspect the equivalent
version, schemas, selected sensor, registry and configured capabilities without
extracting browser credentials. On 2026-10-12, authenticated in-app browser checks
verified installed Core 2026.9.1, Supervisor 2026.09.3, OS 18.2 and Frontend
20260826.6. The States tool displayed one connectivity sensor, and the Actions
editor exposed `weather.get_forecasts` with daily, hourly and twice-daily choices
and `light.turn_on`. No action was performed and no state or configuration was
changed. Available update versions were not treated as installed versions.
These checks verify frontend discovery only: the Python clients remain tested
against local mocks, because no existing CLI token was available. Browser access
does not establish CLI authentication or every optional integration's support.

The maintained API links and action safety requirements are in [SKILL.md](SKILL.md).
Release history is in [CHANGELOG.md](CHANGELOG.md). Maintainers should follow
[RELEASING.md](RELEASING.md) to verify and publish matching GitHub and ClawHub versions.
Credential scope, private data and the prior ClawHub findings are explained in
[SECURITY.md](SECURITY.md).

## License

MIT
