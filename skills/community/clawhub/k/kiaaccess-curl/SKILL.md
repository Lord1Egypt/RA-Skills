---
name: kiaaccess-curl
description: Query and command a Kia vehicle directly with curl against the Kia Owners API (api.owners.kia.com), without running the MCP server. Use when the user wants a one-off read of their Kia's status, location, or EV charge state, or to lock/unlock/start climate from the shell — "check my Kia", "is the car locked", "what's the EV9 charge", "lock the car from the terminal". Requires KIA_USERNAME/KIA_PASSWORD and a one-time SMS/email MFA bootstrap.
---

# Kia Owners API via curl

The Kia Access app's API is reachable server-side — no browser, no bridge, no
extension. This skill talks to it directly with `curl`.

Prefer the `kiaaccess-mcp` server for anything conversational or repeated; use
this for one-off shell work, debugging, or when the server isn't running.

**Ready-to-run request bodies and `jq` recipes: `references/requests.md`.**
Full shape reference (verified live): `../../docs/KIA-API.md`.

## Setup

```bash
export KIA_USERNAME='you@example.com'
export KIA_PASSWORD='…'
export KIA_DEVICE=$(uuidgen)        # keep this stable across runs
```

## Two rules that will bite you

1. **Every request needs an RFC-1123 `date` header.** Omit it and you get
   `errorCode 9200 "Missing mandatory data in header"` — a message that does not
   name the culprit. Regenerate it per request; a stale one is rejected.
2. **HTTP is 200 even on failure.** Success is `status.statusCode == 0` in the
   *body*. Never branch on the HTTP code.

Source `references/requests.md`'s `kia_headers` helper rather than hand-rolling
headers — it handles both.

## Auth: one-time MFA, then silent refresh

`authUser` → `sendOTP` → `verifyOTP` yields a **`sid`** (session, short-lived)
and an **`rmtoken`** (refresh, durable), both as *response headers*.

Afterwards, `authUser` with the `rmtoken` header mints a fresh `sid` with **no
MFA**. So you do the SMS dance once and then never again — save the `rmtoken`.

> **Never retry a rejected login.** `errorCode 1001` (bad credentials) or `1037`
> (bad email) increments `payload.loginAttempt`; enough failures set
> `enforceRecaptcha` and **permanently break shell-based login**. Fix the
> credential and try once.

Store the `rmtoken` at `$KIA_SESSION` (default `~/.kiaaccess-mcp/curl-session.json`)
with `chmod 600`. It is a credential: it re-authenticates the account without a
password prompt.

> Do **not** write it to `~/.kiaaccess-mcp/session.json`. That path belongs to the
> `kiaaccess-mcp` server, whose store is keyed by `accountId` with a different
> schema — overwriting it corrupts the server's session and forces it back
> through MFA.

## Calling

Reads and commands take `sid` (+ `vinkey` for vehicle-scoped calls). Get the
`vinkey` from `ownr/gvl` → `payload.vehicleSummary[0].vehicleKey`.

| Want | Endpoint |
| --- | --- |
| vehicles | `GET ownr/gvl` |
| status (cached) | `POST cmm/gvi` |
| status (force refresh) | `POST rems/rvs` |
| EV charge targets | `GET evc/gts` |
| lock / unlock | `GET rems/door/lock` / `rems/door/unlock` |
| climate on / off | `POST rems/start` / `GET rems/stop` |
| charge start / stop / limits | `POST evc/charge` / `GET evc/cancel` / `POST evc/sts` |

## Confirming a command actually worked

**A `statusCode: 0` means "accepted", not "done".**

- **Do not poll `cmm/gts`.** Despite taking an `xid`, it returns global flags and
  never reports per-action completion — polled through a real lock it never
  changed.
- **Re-read `cmm/gvi` and diff the field.** That is the only proof. Allow ~30–60s.

Fields to diff:

| Command | Field |
| --- | --- |
| lock / unlock | `vehicleStatus.doorLock` |
| climate on / off | `vehicleStatus.climate.airCtrl` and `vehicleStatus.ign3` |

Three traps when writing that comparison:

- **`syncDate` advances on every read.** Include it and *every* command looks
  successful. Exclude it.
- **There is no `airCtrlOn`.** Climate is nested under `vehicleStatus.climate`,
  and the whole block is **absent** unless you request `cmm/gvi` with
  `vehicleConfigReq.airTempRange: "1"` and `seatHeatCoolOption: "1"`.
- **On an EV, `engine` stays `false`** with climate running — use `ign3`.

## Verification status

Every endpoint here was verified live against a 2024 EV9 — all reads, the door
and climate commands, and (against a plugged-in car) `evc/charge`, `evc/cancel`
and `evc/sts`, each proven by a re-read rather than a 200.

Charging proof fields live under `vehicleStatus.evStatus`: `batteryCharge`
(true while charging), `batteryStatus` (SOC %), `batteryPlugin`. `evc/sts` is
proven by re-reading `evc/gts`.

One caveat: **`rems/start`'s temperature may not apply** — a start requesting 70
left `airTemp.value` at 72. Treat it as best-effort.
