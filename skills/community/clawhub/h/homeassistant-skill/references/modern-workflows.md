# Capability discovery and modern Home Assistant workflows

Documentation/source review: 2026-10-12, against the 2026.10 release notes and
2026.10.1 Core command schemas. These are reference versions, not a claim about
the user's installation. Discover the installed version and capabilities first;
an integration can be absent or an account can lack access on an otherwise recent
installation. Never treat an unsupported query as an empty successful result.

## Choose the right interface

Prefer an existing native MCP connection for routine agent interaction when its
tools cover the request. This is an architectural recommendation: HA maintains
the server and tool schemas. Retain REST/WebSocket for deeper inspection; MCP
does not guarantee registry or recorder access. Current native MCP supports
OAuth with PKCE. Actual permissions depend on selected LLM APIs and account:
new installations can expose all LLM APIs and require admin by default. Do not
assume every MCP connection has the narrower built-in Assist scope. Discover
its configured tools before choosing a route. Avoid introducing a third-party
bridge unless the client genuinely requires one.

Cloud-hosted agents need a reachable HA endpoint; a local agent can use a trusted
LAN connection. Do not make a private instance internet-accessible for a test.
Connection setup is a separate user decision, not automatic skill installation.

| Need | Preferred interface | Important distinction |
| --- | --- | --- |
| Installed version, units, integrations, action names | `ha_read.py profile` | Omits coordinates, URLs, config paths and household name |
| One action's fields, selectors, targets, response declaration | `ha_read.py action-schema DOMAIN.ACTION` | GET discovery only; never calls the action |
| Current state or basic availability report | REST state read or `ha_read.py health` | Health lists unknown and unavailable separately; no full attributes |
| Disabled entities, device links, areas, floors, labels | WebSocket registry reads | State lists alone do not describe the registry |
| Automation/script inspection and snippet validation | WebSocket definition and validation reads | Definitions require admin; validation does not run actions |
| Assist agents, pipelines and supported languages | WebSocket Assist reads | Listing an agent does not establish its exposed entities |
| Existing Energy dashboard sources and recorder aggregates | WebSocket energy/statistics reads | Recorder statistics IDs are not always entity IDs |
| Existing repair issues | WebSocket repairs read | Do not dismiss, ignore or start a repair flow during diagnosis |
| Forecasts and calendar events | Existing REST helper commands | Forecasts return service data; all-day events use dates |
| Existing MCP connection for Assist context | MCP resource discovery | Prefer a declared read-only resource when available; do not change HA setup |

All Python commands below run from the skill folder with existing local
`HA_URL`/`HA_TOKEN` environment settings. Use `python3` where needed. Do not obtain
credentials from a browser session. REST requires only Python's standard library;
WebSocket reads optionally require a **local** environment with dependencies from
`requirements-websocket.txt`. This does not require installing anything on HA.
OpenClaw's curl/jq gates remain unchanged. Run both readers with `--help` for
command details; global `--timeout` precedes the subcommand.

## Discover version and actual schemas

```bash
python scripts/ha_read.py profile
python scripts/ha_read.py action-schema weather.get_forecasts
python scripts/ha_read.py action-schema light.turn_on
python scripts/ha_read.py health
python scripts/ha_ws_read.py read services
python scripts/ha_ws_read.py target-services --entity light.kitchen
```

REST `/api/services` is a **list of domain objects**, each with a `services` map.
WebSocket `get_services` returns a **domain-keyed object**. Do not parse them with
the same shape. Preserve field selectors, defaults, targets and response metadata;
discovery documents the exposed action, not permission to execute it. A `get_*`
name does not establish read-only safety: vendor actions can retrieve credentials
or perform external operations. Inspect documented semantics; never invoke token
or key retrieval actions for diagnostics. AI Task generation and Assist
conversation actions can transmit data, incur costs or control devices.
Check entity
capabilities and the installed schema before using cookbook values.
`target-services` uses `get_services_for_target` to discover applicable action
names for explicit targets. It shares target expansion's limit of 64 IDs and
rejects `all` and wildcards. Group expansion is opt-in. Applicability does not
prove authorization or expose every target-dependent field; inspect the action
schema and current entity attributes as well. Unsupported installations return
an error rather than silently falling back or calling an action.

The WS reader performs the `auth_required` → `auth` → `auth_ok` exchange, then
sends one request with a numeric ID and requires the corresponding successful
result. Output is `{ "ha_version": "...", "result": ... }`. It never subscribes,
reconnects, follows redirects, calls a generic service or runs a conversation.
It disables proxy routing, compression and credential-bearing debug logs, bounds
messages to 8 MiB, and closes the connection after each query.
The timeout bounds connection setup and the subsequent complete exchange,
including blocked sends; connection cleanup may take up to two additional seconds.
`unknown_command`, `unauthorized` and `not_found` are distinct errors. Do not change account roles to
make a diagnostic read succeed.

## Map entities to devices and locations

```bash
python scripts/ha_ws_read.py read entities
python scripts/ha_ws_read.py read devices
python scripts/ha_ws_read.py read areas
python scripts/ha_ws_read.py read floors
python scripts/ha_ws_read.py read labels
python scripts/ha_ws_read.py resolve-target --area kitchen --entity group.kitchen --expand-groups
```

Join the entity entry's `device_id` to device registry `id`. Use an entity's
explicit `area_id`, falling back to the device's area; then join the area's
`floor_id`. Preserve `disabled_by`, `hidden_by`, labels and integration links.
Disabled entities may have registry entries without state objects. A missing
registry entry is not proof that a state-only entity is invalid.

`extract_from_target` reports referenced entities/devices/areas and missing target
references without operating them. Inspect this result before any separately
authorized area/device/label batch. Group expansion is optional. The helper
accepts only explicit IDs, rejects `all`/wildcards, and bounds target counts.
Do not silently translate names to IDs or assume every target member is safe.

## Inspect automations before running them

```bash
python scripts/ha_ws_read.py definition automation.evening_routine
python scripts/ha_ws_read.py definition script.bedtime_routine
python scripts/ha_ws_read.py validate-config snippet.json
```

Definitions are read through `automation/config` or `script/config`; these require
an administrator account and return `{ "config": ... }` inside `result`.
Inspect conditions, actions, mode, service targets and indirect effects. During
read-only testing, do not trigger, reload, enable or disable anything.

The validation file must contain only `triggers`, `conditions` and/or `actions`
sections. For example:

```json
{"actions": [{"action": "light.turn_on", "target": {"entity_id": "light.kitchen"}, "data": {"brightness_pct": 20}}]}
```

The reader sends `validate_config`, not `call_service`. Its result reports schema
validation per supplied section; it does not prove real-world effects, current
entity availability, all template outcomes or physical completion. A result can
contain `valid: false` even though the read itself succeeds. For a complete
automation, select the relevant sections explicitly rather than uploading an
entire editor/storage document with unrelated metadata.

Core 2026.9.1 and 2026.10.1 use plural wire keys even though the public WebSocket API guide
still shows singular keys. The helper normalizes either local spelling to plurals
and rejects conflicting aliases. For an older server requiring singular wire keys,
select `validate-config snippet.json --legacy-keys` explicitly; it never retries
automatically. It also rejects an empty/mismatched validation result, so a server
silently ignoring a section cannot appear to have validated it.

## Assist and existing MCP connections

```bash
python scripts/ha_ws_read.py read assist-pipelines
python scripts/ha_ws_read.py read assist-agents
python scripts/ha_ws_read.py read assist-languages
```

Inspect the configured conversation engine, language and speech stages before
diagnosing voice requests. Do not run `conversation.process`, `/api/conversation/process`,
`/api/intent/handle`, or `assist_pipeline/run` as a read-only test: even a natural
language question can resolve to device actions or custom intents.

The built-in Assist LLM API works through exposed entities and intents and does
not perform administrative tasks. Direct REST/WebSocket credentials have a
different access scope; exposure to Assist is not a restriction on those tokens.
If an MCP Server integration is already connected, discover its tools/resources
first. When offered, `homeassistant://assist/context-snapshot` is a read-only
resource matching `GetLiveContext`. Its availability depends on the configured
LLM API. Inspect tool annotations and scope rather than treating every MCP tool as
read-only. Do not add the integration, start OAuth or alter exposure for testing.

## Energy and diagnostic reads

```bash
python scripts/ha_ws_read.py read energy-preferences
python scripts/ha_ws_read.py read energy-info
python scripts/ha_ws_read.py read statistics-metadata
python scripts/ha_ws_read.py statistics sensor.grid_energy --start 2026-10-11T00:00:00Z --end 2026-10-12T00:00:00Z --period hour
python scripts/ha_read.py history sensor.grid_power --start 2026-10-11T00:00:00Z --end 2026-10-12T00:00:00Z
python scripts/ha_ws_read.py read repairs
```

Match Energy preferences' configured source/statistic IDs to recorder metadata
before comparing consumption. Preserve units, `has_sum`, `has_mean` and statistic
source; external statistics may use `source:identifier`. Power (W) and accumulated
energy (kWh) are different quantities. The statistics reader requests `change`,
`sum`, `state`, and `mean` for one ID in a window up to 31 days. Use interval
`change` where applicable; never sum cumulative `sum` or `state` samples as usage.
Missing values are not zero. Use HA's reporting timezone when defining local-day
bounds; supply both ISO timestamps with explicit offsets. Data retention and
availability depend on Recorder configuration.

REST history is capped at seven days and one entity, with attribute-free minimal
responses. Empty results may mean no recorded history, not no current entity.
Repairs are diagnostic hints; ignoring or fixing them is a separate action.
Logs, registry records, automation definitions and Assist context can contain
private household data or integration secrets. Keep raw output local and redact
before sharing; credential redaction is not a comprehensive privacy filter.

## Release compatibility checks

The original REST-only assumptions need two additional checks for 2026.10:

- State conditions combining `for` with an attribute, multiple states or another
  entity's state now fail validation. Validate snippets rather than assuming a
  previously accepted condition still works.
- MQTT publish/dump and Synology reboot/shutdown now require administrator access
  for user-initiated calls. A discovered action can still be forbidden. Do not
  bypass that restriction with an automation or escalate the account for a test.

Sensor units, enums and availability may change across integration updates. Use
current state attributes and repair messages rather than hard-coded interpretations.

## Sources and validation boundary

- [2026.10 release notes](https://www.home-assistant.io/blog/2026/10/07/release-202610/)
- [WebSocket API](https://developers.home-assistant.io/docs/api/websocket/)
- [Current validation command source](https://github.com/home-assistant/core/blob/2026.10.1/homeassistant/components/websocket_api/commands.py)
- [2026.9.1 target discovery and validation source](https://github.com/home-assistant/core/blob/2026.9.1/homeassistant/components/websocket_api/commands.py)
- [Assist LLM API](https://developers.home-assistant.io/docs/core/llm/)
- [MCP Server integration](https://www.home-assistant.io/integrations/mcp_server/)
- [2026.10.1 registry source](https://github.com/home-assistant/core/tree/2026.10.1/homeassistant/components/config)
- [Automation source](https://github.com/home-assistant/core/blob/2026.10.1/homeassistant/components/automation/__init__.py)
- [Script source](https://github.com/home-assistant/core/blob/2026.10.1/homeassistant/components/script/__init__.py)
- [Assist pipeline source](https://github.com/home-assistant/core/blob/2026.10.1/homeassistant/components/assist_pipeline/pipeline.py)
- [Conversation agent source](https://github.com/home-assistant/core/blob/2026.10.1/homeassistant/components/conversation/http.py)
- [Energy source](https://github.com/home-assistant/core/blob/2026.10.1/homeassistant/components/energy/websocket_api.py)
- [Recorder source](https://github.com/home-assistant/core/blob/2026.10.1/homeassistant/components/recorder/websocket_api.py)
- [Repairs source](https://github.com/home-assistant/core/blob/2026.10.1/homeassistant/components/repairs/websocket_api.py)
- [WebSocket dependency API](https://websockets.readthedocs.io/en/stable/reference/sync/client.html)

Mock protocol tests establish request construction, validation and error behavior;
they do not establish the installed HA version or available integrations. During
this update, the authenticated in-app frontend showed installed Core 2026.9.1,
one connectivity sensor and weather forecast/light action discovery. No action,
state write or configuration change was executed. Browser checks do not prove
Python-client authentication or optional registry, Assist, calendar, Energy and
repair command support. The clients remain mock-tested; no existing CLI token
was available. Do not report mock version strings as the user's version.
