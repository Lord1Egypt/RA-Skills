---
name: iaqualink-curl
description: Read an iAqualink (Zodiac / Jandy / Fluidra) pool system straight from a shell with curl — sign in, list systems, and fetch the iAqua home/aux screens or an eXO chlorinator's shadow — without running the iaqualink-mcp server. Use for a one-off "what's the pool temperature" from the terminal, scripting, or debugging the API. Credentials come from the macOS Keychain item "iaqualink". Derived from iaqualink-py 0.7.0; the sign-in, system list and iAqua reads are seen live, the eXO shadow read is not yet.
---

# iAqualink via curl

> **Derived from iaqualink-py 0.7.0, partly verified live.** The recipes
> transcribe the open-source client Home Assistant uses. Sign-in,
> `devices.json` and the iAqua `get_home` / `get_devices` reads have been seen
> working on a real panel; the eXO shadow read has not. Shape reference:
> `../../docs/IAQUALINK-API.md`.

The iAqualink cloud is reachable server-side with a plain email/password
sign-in — no browser, no bridge. Prefer the `iaqualink-mcp` tools (the
`iaqualink` skill) for anything conversational or for control: they verify
writes and bind confirmations. Use this for reads and debugging.

## Setup (once)

```bash
# The Keychain item: account = your iAqualink email, password = the secret (prompted).
security add-generic-password -s iaqualink -a 'you@example.com' -w
. skills/iaqualink-curl/references/iaqualink.sh   # bash or zsh
```

`IAQ_EMAIL` / `IAQ_PASSWORD` override the Keychain; `IAQ_DRY_RUN=1` prints each
request (password redacted) instead of sending it. The helper keeps its own
session at `$IAQ_SESSION` (default `~/.iaqualink-curl/session.json`, mode 600 —
a credential; delete it to sign out).

## Sign in — once, never in a loop

```bash
iaq_login
```

A refusal means the email/password is wrong. **Fix it and try once — never
retry in a loop**: repeated failed sign-ins are how accounts get locked. When a
later call answers 401, run `iaq_refresh` (and `iaq_login` only if that is
refused too).

## Reads

```bash
iaq_devices | jq -r '.[] | [.serial_number, .device_type, .name] | @tsv'

# iAqua (device_type "iaqua"): the home screen — rows 4+ are {name: state}
iaq_home IAQ123 | jq '.home_screen[4:] | add | {air_temp, pool_temp, spa_temp, pool_set_point, spa_set_point, pool_pump, spa_pump, pool_heater, spa_heater}'
# states: "0" off, "1" on, "2" standby, "3" enabled (heating); "" = no reading

# iAqua aux circuits and lights
iaq_auxes IAQ123 | jq '.devices_screen[3:][] | to_entries[0] | {aux: .key} + (.value | add)'

# eXO (device_type "exo"): the shadow
iaq_shadow EXO456 | jq '.state.reported | {connection: .aws.status, heating, swc: .equipment.swc_0 | {production, swc, boost, low, ph_sp, orp_sp, filter_pump}}'
```

## Writes (prefer the MCP)

iAqua `set_pool_pump`, `set_spa_pump`, `set_pool_heater`, `set_spa_heater`,
`set_solar_heater` and `set_aux_<n>` are **toggles**: read `get_home` /
`get_devices` first and send only when the state differs, or you will flip it
the wrong way.

```bash
iaq_command IAQ123 set_temps 'temp1=102&temp2=86'   # with a spa: temp1 = spa, temp2 = pool (send both)
```

eXO writes are `POST …/devices/v1/<serial>/shadow` with
`{"state":{"desired":{…}}}` and apply asynchronously — see the API doc's table.
