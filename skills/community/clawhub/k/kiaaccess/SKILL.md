---
name: kiaaccess
description: This skill should be used when the user asks about their Kia vehicle through the Kia Access / Kia Owners account. Triggers on phrases like "is the car locked", "unlock the Kia", "start the car's climate", "warm up the car", "where is my car", "what's the EV charge at", "check the car's battery", "lock the doors", or any request to read or command a Kia vehicle.
---

# kiaaccess-mcp

MCP server for the Kia Owners API used by the Kia Access app — vehicle status, location, EV charge state, and confirmation-gated door, climate, and charging commands, using the user's own Kia account.

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

1. `kia_start_login`, confirmed (see [Confirmations](#confirmations)) → returns `otpKey` + `xid` and the masked destinations Kia has on file.
2. `kia_send_otp(otpKey, xid, notifyType)` — ask the user whether they can read `SMS` or `EMAIL` right now. The code expires in ~2 minutes.
3. `kia_verify_otp(otpKey, xid, otp)` — same `otpKey`/`xid`, plus the code the user received.
4. `kia_list_vehicles` to confirm, and to get the `vehicleKey` every other tool needs.

The remember-me token is then stored locally and refreshes sessions silently forever; MFA is never needed again on that machine. `kia_forget_session` (confirmation-gated) throws it away so the bootstrap can be repeated.

A server with no one to read an OTP cannot run these steps at all. Bootstrap it elsewhere and have the user copy the `rmtoken` from that machine's `~/.kiaaccess-mcp/session.json` into `KIA_RMTOKEN` themselves (no tool returns it, and it must never pass through the conversation), with `KIA_DEVICE_ID` set to the same uuid on both machines — the token is minted against a device uuid and is worthless with a different one. `KIA_RMTOKEN` wins over the local store.

**If a login is rejected, STOP.** Kia counts failed logins and eventually enforces reCAPTCHA, which breaks server-side login for that account permanently. Tell the user to check the credentials in the Kia Access app and fix the environment — never retry with a guessed password.

## Tools

### Account
| Tool | Notes |
|------|-------|
| `kia_session_status` | Configured? Bootstrapped? Which write mode? No network call, no secrets. Start here when a tool says it is not configured. |
| `kia_start_login` / `kia_send_otp` / `kia_verify_otp` | The three bootstrap steps above. |
| `kia_forget_session(confirmToken?)` | Deletes the locally stored session. Local only — Kia is not contacted. |

### Reads
| Tool | Notes |
|------|-------|
| `kia_list_vehicles` | Enrolled vehicles with `vehicleKey`, nickname, model, mileage. VINs masked to 6 chars. |
| `kia_vehicle_status(vehicle_key, include_raw?)` | Cached status: `doorLock`, `ign3`, the nested `climate` block, and (with `include_raw`) battery/EV detail, doors, tyres. |
| `kia_refresh_status(vehicle_key)` | Wakes the telematics unit. Slow, draws power, returns no data — re-read `kia_vehicle_status` after. |
| `kia_vehicle_location(vehicle_key)` | Last reported position + map link. Not a live fix. |
| `kia_charge_targets(vehicle_key)` | Target state of charge per plug type. |

### Commands (all confirmation-gated, all take `confirmToken?`)
| Tool | Mode | Notes |
|------|------|-------|
| `kia_start_climate(vehicle_key, temperature?, durationMinutes?, defrost?, waitSeconds?, confirmToken?)` | `comfort` | Verified live. Temperature is best-effort — do not promise the user an exact cabin temperature. |
| `kia_stop_climate(vehicle_key, waitSeconds?, confirmToken?)` | `comfort` | Verified live. |
| `kia_start_charge` / `kia_stop_charge` / `kia_set_charge_limits` | `comfort` | Verified against a plugged-in car. A success status means Kia accepted the command, not that the car acted — confirm charge start/stop via `kia_vehicle_status` (`evStatus.batteryCharge`), and limits via `kia_charge_targets`. `kia_set_charge_limits` REPLACES the target list, so send both plug types. Starting a charge on an unplugged car succeeds and does nothing. |
| `kia_lock_doors(vehicle_key, waitSeconds?, confirmToken?)` | `all` | Verified live by re-reading `doorLock`. |
| `kia_unlock_doors(vehicle_key, waitSeconds?, confirmToken?)` | `all` | Leaves the car unsecured. Only when the user explicitly asked for this vehicle. |

## Confirmations

Every write — each command, plus `kia_start_login` and `kia_forget_session` — asks the user first. A client that can show a confirmation prompt shows one and the tool proceeds on approval (unless the server sets `MCP_CONFIRM_ELICITATION=off`). Otherwise the first call does nothing and returns `status: "confirmation-required"` with a `preview` and a `confirmToken`; show the user the preview, get their approval in chat (under the default `MCP_CONFIRM_MODE=ask-user`), then call the SAME tool again with the SAME arguments plus `confirmToken`. The token works once (`TOKEN_REUSED` after that), expires after `MCP_CONFIRM_TTL_SECONDS` (default 600), and is bound to the exact request: changing anything that would be sent returns `DRAFT_CHANGED` with a fresh preview and token. Under `MCP_CONFIRM_MODE=refuse` such clients get `reason: "confirmation-unsupported"` and nothing is sent.

## Reading a command result

- **`status: "confirmation-required"` means nothing happened.** The tool made no network call and returned a `preview` of the exact request plus a `confirmToken`. Show the user that preview; never describe it as if the car acted.
- **`commandAccepted` ≠ `stateConfirmed`.** Kia returning success only means the request was accepted. Only `stateConfirmed: true` means the car actually reads locked / unlocked / climate-on. Changes take 30–60 seconds; `waitSeconds` controls how long the tool keeps re-reading. It defaults to 30 so the call finishes inside a client's own request timeout; an unconfirmed result (or a client-side timeout) still means the command WAS sent — re-read the vehicle status, never re-send the command to "retry".
- **`stateConfirmed: false` is not "it failed"** — it means the tool stopped waiting. Say exactly that, and offer to re-read `kia_vehicle_status`.
- **`alreadyInState: true` weakens `stateConfirmed`.** The cached read already showed the target state before the command, so a matching re-read does not prove the car acted. Say so; if it matters, `kia_refresh_status`, wait, then re-read.
- **On an EV, `engine` stays false with the climate running.** `ign3` is the ignition proxy. Never report the car as off because `engine` is false.
- **`syncDate` advances on every read** and proves nothing changed.

## Caution

- **Confirm with the user before every command** — these move a real vehicle. Unlocking especially: it leaves the car open until someone locks it.
- **Never guess a `vehicleKey`.** Call `kia_list_vehicles` first. Pass it as `vehicle_key` on every tool. The read tools default it to the only car on a one-vehicle account; the command and charging tools always require it, so every command names the car it acts on.
- **Never retry a rejected login** (see above) and never echo the password, the `rmtoken`, or a session id into the conversation.
- **A cached read can be stale.** If freshness matters, `kia_refresh_status`, wait, then re-read.

## In context groups

On mcp-host, every tool here except `kia_healthcheck` carries a `_meta.mint` hint placing it in the **`home`** group: the reads (`kia_list_vehicles`, `kia_vehicle_status`, `kia_vehicle_location`, `kia_charge_targets`, `kia_session_status`) as `lookup`, climate / charging / door commands as `turn-on-off`, `kia_set_charge_limits` as `change`, and the sign-in and refresh plumbing as `other`. Aliases carry the words people say ("warm up the car", "where is my car", "lock the car").

- **No canonical read.** A car answers no "what's new / what's due / what's on" question, so a compound ask such as "what's new at home…and anything due at school?" draws nothing from this server; it is reached by its own words ("is the car charged, and where did I park?").
- **No subject.** Vehicles are not published as a label enum: listing them needs a live Kia session, and this server will not attempt a sign-in at start (failed sign-ins push the account into permanent reCAPTCHA). Name the car with `vehicle_key` from `kia_list_vehicles` as usual.
- Commands stay confirmation-gated whatever the group asks. With no signed-in session the group gets the same "run the MFA bootstrap" error as any other call.
