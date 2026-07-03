# MagicHaqi Agent Integration (protocol reference)

MagicHaqi is a **pure front-end H5 game** backed by KeepWork PersonalPageStore. There is
**no MagicHaqi REST backend**. Agents operate it the way a person would: open the site,
log in, navigate, click — plus three agent shortcuts described here.

## A. Authentication

Reuse the **KeepWork** login REST API (the only REST call involved):

```http
POST https://api.keepwork.com/core/v0/users/login
{ "username": "...", "password": "...", "platform": "WEB" }
-> { "token": "..." }
```

Inject the token by opening: `MagicHaqi.html?token=<TOKEN>`. The app reads `?token=` at
boot and sets the SDK token. Visual fallback: click `#mhLoginBtn` and complete the form.

Check `getState().loggedIn === true` to confirm.

## B. Navigation (URL params)

| param            | effect |
|------------------|--------|
| `?token=`        | Inject auth token (logged-in boot). |
| `?view=`         | Force a view: `planet`/`field`/`pet`/`cell` (zoom levels), `game`, `chat`, `shop`, `ops`. |
| `?agent=<id>`    | Set the acting agent id; binds the current pet's `agentOwner` (co-parent). |
| `?adopt=1`       | Go straight into the adopt/hatch flow. |
| `?cmd=<enc>`     | URL-encoded command, executed once at boot (one-shot). |
| `?home_planet=`  | (existing) land on a themed planet. |
| `?skip_onboarding=1` | (existing) skip the new-user story. |

## C. Hidden agent command interface

The page injects three hidden nodes plus a global object:

- `window.MagicHaqiAgent.exec(cmdText)` → `Promise<result>` — run a command.
- `window.MagicHaqiAgent.getState()` → state object — read state.
- `window.MagicHaqiAgent.listCommands()` → string[].
- `#mh-agent-cmd` — hidden `<textarea>`; write a command + dispatch `change` to run it.
- `#mh-agent-result` — `<script type="application/json">` holding the last result.
- `#mh-agent-state` — `<script type="application/json">` holding the live state snapshot,
  refreshed after every render and after every command.
- Event: `window.addEventListener('magichaqi:agent-result', e => e.detail)` to avoid polling.

### Command protocol
- Input: JSON `{ "cmd", "args", "requestId" }` or shorthand `cmd k=v k2=v2`.
- Output: `{ ok, cmd, requestId?, result | error, state }`.
- Always pass a unique `requestId` to correlate async results.
- Write commands are appended to `agent/audit.log` (actor = the `agent` id).

See `commands.md` for the full command table and state shape.

## D. Workspace & data scope

All data lives in the `MagicHaqi` PersonalPageStore workspace
(`pets/<id>.json`, `pets/<id>.memory.md`, `user/profile.json`, `agent/audit.log`, ...).
The agent does not get raw filesystem access; it acts through commands and (optionally)
the SDK file tools scoped to this workspace.

## E. Permissions & safety

- **Read is free** (`getState`, `listCommands`).
- **Care writes** (feed/clean/play/sleep/say) are allowed but should be paced and confirmed
  by re-reading state.
- **Spending** (`buy`) costs in-game coins — require explicit human consent.
- **Adoption** binds an agent owner — confirm with the human first.
- Everything is auditable via `agent/audit.log`; nothing is irreversible without consent.

## F. Errors
- Unknown command → `{ ok:false, error:'unknown command "x"', availableCommands:[...] }`.
- Bad JSON → `{ ok:false, error:'parse error: ...' }`.
- Missing pet/args → `{ ok:false, error:'...' }`. Re-read state and retry.

## G. Verifying with screenshots
After a write command, take a screenshot of the pet view to visually confirm the result,
and cross-check with the `state` returned in the command result.
