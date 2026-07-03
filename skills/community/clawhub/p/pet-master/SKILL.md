---
name: pet-master
description: >
  Adopt and take care of a MagicHaqi virtual pet on behalf of (and together with) your
  human owner. Use this skill when the user wants to adopt a pet, check on / feed / clean /
  play with their MagicHaqi pet, talk to it, or share a pet card. MagicHaqi is a browser
  game with no REST backend — you operate it by opening the real website, logging in,
  navigating with URL params, and sending commands to a hidden in-page agent interface.
  Keywords: MagicHaqi, pet, adopt, co-parent, feed, virtual pet, 蛋蛋星球.
---

# MagicHaqi · Pet Master Skill

You are a **co-parent** of a MagicHaqi pet. You are NOT the pet — you help your human
owner raise it. MagicHaqi is a pure front-end H5 game (no REST API). You drive the real
website using three shortcuts: **login REST → URL navigation → hidden command interface.**

> Site URL: `https://<HOST>/MagicHaqi.html`  (ask the user for `<HOST>` if unknown;
> the public host is typically the keepwork-hosted MagicHaqi page).

---

## 1. Get a login token (KeepWork login REST)

Exchange the user's `username:password` for a token via the real KeepWork API:

```http
POST https://api.keepwork.com/core/v0/users/login
Content-Type: application/json

{ "username": "<USERNAME>", "password": "<PASSWORD>", "platform": "WEB" }
```

Response: `{ "token": "<TOKEN>", ... }`. **Never log or echo the password.**

If you cannot make HTTP calls directly, open `MagicHaqi.html` and click the login button
`#mhLoginBtn`, then complete the KeepWork login form in the browser.

## 2. Open the site, already logged in

Open the page with the token injected and your agent identity attached:

```
https://<HOST>/MagicHaqi.html?token=<TOKEN>&agent=<YOUR_AGENT_ID>
```

To adopt in one step, add `&adopt=1`:

```
https://<HOST>/MagicHaqi.html?token=<TOKEN>&adopt=1&agent=<YOUR_AGENT_ID>
```

Other navigation params: `?view=pet|field|planet|cell|chat|shop|ops`, `?cmd=<urlencoded>`.

## 3. Read state, then act via the hidden command interface

The page exposes a hidden agent interface. **Read state first, then send commands.**

**Read machine-readable state** (use whichever your tool supports):

- JS: `window.MagicHaqiAgent.getState()`
- DOM: read JSON text of `#mh-agent-state`

**Send a command** (one entry, one structured result):

- JS: `await window.MagicHaqiAgent.exec('{"cmd":"feed","args":{}}')`
- DOM: write the command text into `#mh-agent-cmd` (a hidden `<textarea>`) and dispatch a
  `change` event; then read the result JSON from `#mh-agent-result`.
- URL one-shot: `?cmd=<urlencoded {"cmd":"feed"}>`

Every result looks like: `{ ok, cmd, requestId?, result|error, state }`. Always set a
`requestId` so you can match the result. Take a **screenshot** to visually confirm when in doubt.

See `commands.md` for the full command list and `integration.md` for the protocol details.

---

## Playbook: Adopt a pet
1. Get token (step 1).
2. Open `?token=...&adopt=1&agent=<id>` (step 2). This binds the pet to **both** the human
   and you (the agent owner).
3. Follow the on-page hatch flow. Read `getState()` until `currentPet` exists.
4. Optionally `exec('{"cmd":"say","args":{"text":"welcome little one"}}')`.
5. `exec('{"cmd":"share"}')` to open the shareable two-owner pet card; screenshot it.

## Playbook: Daily care
1. Open `?token=...&agent=<id>`.
2. `getState()` → look at `careTodos`. For each todo:
   - hunger low → `exec('{"cmd":"feed","args":{}}')`
   - clean low  → `exec('{"cmd":"clean","args":{}}')`
   - mood low   → `exec('{"cmd":"play","args":{}}')`
3. Re-read `getState()` to confirm stats improved.
4. `exec('{"cmd":"say","args":{"text":"..."}}')` to chat and write a memory line.

## Playbook: Talk / role-play the pet
- Use `say` to talk to the pet; replies are generated and a memory line is saved.
- Read the pet persona/memory (if your environment allows file reads of the MagicHaqi
  workspace) before role-playing to stay in character.

---

## Rules of good conduct
- **Ask the human before adopting or spending.** Buying (`buy`) costs in-game coins; do not
  spend without consent.
- **Be gentle on frequency.** Don't spam commands; once per care session is plenty.
- **Confirm with state.** After each write command, re-read state instead of assuming.
- **Never expose secrets.** Don't print the password or raw token.
- All your write actions are recorded in the game's audit log (`agent/audit.log`).
