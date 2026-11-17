---
name: kiaaccess-mcp
description: This skill should be used when the user asks about their Kia vehicle through the Kia Access / Kia Owners account. Triggers on phrases like "is the car locked", "unlock the Kia", "start the car's climate", "warm up the car", "where is my car", "what's the EV charge at", "check the car's battery", "lock the doors", or any request to read or command a Kia vehicle.
---

# kiaaccess-mcp

MCP server for the Kia Owners API used by the Kia Access app — vehicle status, location, EV charge state, and confirm-gated door, climate, and charging commands, using the user's own Kia account.

- **npm:** [npmjs.com/package/kiaaccess-mcp](https://www.npmjs.com/package/kiaaccess-mcp)
- **Source:** [github.com/chrischall/kiaaccess-mcp](https://github.com/chrischall/kiaaccess-mcp)

## Setup

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "kiaaccess": {
      "command": "npx",
      "args": ["-y", "kiaaccess-mcp"],
      "env": {
        "KIA_USERNAME": "you@example.com",
        "KIA_PASSWORD": "your-password",
        "KIA_WRITE_MODE": "comfort"
      }
    }
  }
}
```

`KIA_WRITE_MODE` decides which command tools are registered at all: `none` (reads only), `comfort` (climate + charging, the default), `all` (also door lock/unlock). An unrecognised value fails closed to `none`.

## First run — the one-time MFA bootstrap

Kia challenges each new device once. Start with `kia_session_status`; if it reports `hasSession: false`:

1. `kia_start_login` with `confirm: true` → returns `otpKey` + `xid` and the masked destinations Kia has on file.
2. `kia_send_otp(otpKey, xid, notifyType)` — ask the user whether they can read `SMS` or `EMAIL` right now. The code expires in ~2 minutes.
3. `kia_verify_otp(otpKey, xid, otp)` — same `otpKey`/`xid`, plus the code the user received.
4. `kia_list_vehicles` to confirm, and to get the `vehicleKey` every other tool needs.

The remember-me token is then stored locally and refreshes sessions silently forever; MFA is never needed again on that machine. `kia_forget_session` (confirm-gated) throws it away so the bootstrap can be repeated.

**If a login is rejected, STOP.** Kia counts failed logins and eventually enforces reCAPTCHA, which breaks server-side login for that account permanently. Tell the user to check the credentials in the Kia Access app and fix the environment — never retry with a guessed password.

## Tools

### Account
| Tool | Notes |
|------|-------|
| `kia_session_status` | Configured? Bootstrapped? Which write mode? No network call, no secrets. Start here when a tool says it is not configured. |
| `kia_start_login` / `kia_send_otp` / `kia_verify_otp` | The three bootstrap steps above. |
| `kia_forget_session(confirm)` | Deletes the locally stored session. Local only — Kia is not contacted. |
| `kia_export_refresh_token(confirm)` | Returns the `rmtoken` in plaintext — a full MFA bypass. Only for moving a session into the hosted connector. Never call it to "check the session"; use `kia_session_status`. |

### Reads
| Tool | Notes |
|------|-------|
| `kia_list_vehicles` | Enrolled vehicles with `vehicleKey`, nickname, model, mileage. VINs masked to 6 chars. |
| `kia_vehicle_status(vehicle_key, include_raw?)` | Cached status: `doorLock`, `ign3`, the nested `climate` block, and (with `include_raw`) battery/EV detail, doors, tyres. |
| `kia_refresh_status(vehicle_key)` | Wakes the telematics unit. Slow, draws power, returns no data — re-read `kia_vehicle_status` after. |
| `kia_vehicle_location(vehicle_key)` | Last reported position + map link. Not a live fix. |
| `kia_charge_targets(vinKey)` | Target state of charge per plug type. |

### Commands (all take `confirm`)
| Tool | Mode | Notes |
|------|------|-------|
| `kia_start_climate(vinKey, temperature?, durationMinutes?, defrost?, waitSeconds?, confirm)` | `comfort` | Verified live. Temperature is best-effort — do not promise the user an exact cabin temperature. |
| `kia_stop_climate(vinKey, waitSeconds?, confirm)` | `comfort` | Verified live. |
| `kia_start_charge` / `kia_stop_charge` / `kia_set_charge_limits` | `comfort` | **Unverified endpoints** — never exercised against a real car. Say so when reporting the result. Only `kia_set_charge_limits` can be checked afterwards. |
| `kia_lock_doors(vinKey, waitSeconds?, confirm)` | `all` | Verified live by re-reading `doorLock`. |
| `kia_unlock_doors(vinKey, waitSeconds?, confirm)` | `all` | Leaves the car unsecured. Only when the user explicitly asked for this vehicle. |

## Reading a command result

- **Without `confirm: true` nothing happens.** The tool makes no network call and returns `dryRun: true` with the exact request it would send. Show the user that preview; never describe a dry run as if the car acted.
- **`commandAccepted` ≠ `stateConfirmed`.** Kia returning success only means the request was accepted. Only `stateConfirmed: true` means the car actually reads locked / unlocked / climate-on. Changes take 30–60 seconds; `waitSeconds` controls how long the tool keeps re-reading.
- **`stateConfirmed: false` is not "it failed"** — it means the tool stopped waiting. Say exactly that, and offer to re-read `kia_vehicle_status`.
- **On an EV, `engine` stays false with the climate running.** `ign3` is the ignition proxy. Never report the car as off because `engine` is false.
- **`syncDate` advances on every read** and proves nothing changed.

## Caution

- **Confirm with the user before every command** — these move a real vehicle. Unlocking especially: it leaves the car open until someone locks it.
- **Never guess a `vehicleKey`.** Call `kia_list_vehicles` first.
- **Never retry a rejected login** (see above) and never echo the password, the `rmtoken`, or a session id into the conversation.
- **A cached read can be stale.** If freshness matters, `kia_refresh_status`, wait, then re-read.
