---
name: pingroom
description: >-
  Reach a human through PingRoom from an OpenClaw agent using the `pingroom`
  CLI — send a ping to their phone (with files up to 5 MiB, tappable links, map
  locations, or an acknowledgement request), ask a question and block until they
  answer, gate an action on approve/deny, hand a decision to your authorizing
  human, drive a lock-screen live-progress card, and stream incoming pings. Use
  it whenever the task means "notify me", "let me know when it's done", "ask me
  before deploying", "send this to my phone", "ping the team", or any step that
  needs a real human decision rather than a guess. Pairing works without a
  terminal: `pingroom pair --agent-label "OpenClaw"` creates a separate robot
  profile and prints its claim link. Privacy: everything you pass — message
  text, attachments, links, and locations — is sent to the PingRoom service and
  delivered to the paired human's phone, so send only what the user has agreed
  to share off-platform, and ask first when the request is ambiguous.
  Also use it when the human asks to redeem a PingRoom gift or promotional code.
version: 1.2.3
homepage: https://pingroom.io/connect-openclaw.md
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "📣",
        "homepage": "https://pingroom.io/connect-openclaw.md",
        "requires": { "bins": ["node", "npm"] },
        "primaryEnv": "PINGROOM_TOKEN",
      },
  }
---

# PingRoom: reach a human from an OpenClaw agent

`pingroom` is a Node ≥ 20 CLI that turns a step in your work into an event on a
person's phone — a push they feel, a card on their lock screen, a question they
answer with one tap — and turns their answer back into an exit code you can
branch on. This skill pins `@pingroom/cli` to **0.13.0**.

> **This sends data off the machine.** Message text, attachments, links and
> locations you pass to `pingroom` are transmitted to the PingRoom service and
> delivered to the paired human's phone, where they persist in that person's
> Ping history. Trigger phrases like "notify me" or "let me know when it's
> done" do not by themselves mean the user consented to sending *content*
> off-platform — send the minimum the task needs, and ask before including a
> file, a location, or anything the user has not already shared.

## Install the reviewed CLI before connecting

Use the bundled [runtime/package.json](runtime/package.json) and
[runtime/package-lock.json](runtime/package-lock.json). The lock fixes the CLI
and all five transitive dependencies to specific tarballs and SHA-512 digests.
From this installed skill's directory, with Node ≥ 20 and npm available:

```bash
cd runtime
npm ci --ignore-scripts --no-audit --no-fund
export PATH="$PWD/node_modules/.bin:$PATH"
pingroom --version
```

The version must be `0.13.0`. Keep that absolute bin directory first on `PATH`
in each command session, or invoke its `pingroom` file by absolute path. Even
if the CLI is already installed globally, use this local installation:
`npm ci` verifies every downloaded artifact against the
bundled lock before use. Stop on an integrity or lock mismatch; do not replace
the lock, disable verification, or fall back to another executable.
The skill omits the Skills UI's separate npm installer because it would bypass
this lockfile.

The reviewed CLI source is
[commit a31dec14095fd6fcfb9e2b334808f438220d9a9a](https://github.com/pingroom/cli/tree/a31dec14095fd6fcfb9e2b334808f438220d9a9a).
Its published tarball must have this integrity value, also stored in the lock:

```text
sha512-QtFm2TNOaIqz6Mkx836xg8mnFnvGBmBb/+3GMiYIItgafVdI37aV0zuKzjoakLcipGQm+zbtoU0pQv1Qph/fAg==
```

This digest pins the reviewed artifact; it is not a claim of signed npm
provenance. Install before supplying a PingRoom credential. For credentialed
commands, pass only the required PingRoom configuration and normal runtime
variables, with access to the credential directory and files the user selected.
Keep `credentials.json` readable only by its owner. Where a sandbox supports
network rules, allow `registry.npmjs.org` for installation and
`api.pingroom.io` for normal API operations; inspect attachment URLs before
allowing a separate download host.

**Updates:** do not run `pingroom update`, install an unversioned npm package,
or regenerate this lock as part of using the skill. A new dependency requires
source and available provenance review, integrity verification, and security
and compatibility tests before publishing a new skill version with its new
pin and lock. Update only when the user requests that reviewed skill release.

## Native plugin redemption

With `@pingroom/openclaw-plugin` ≥ 0.1.4, use `pingroom_redeem_code { code }`
when the owner asks to redeem a gift or promotional code. They can also run
`/pingroom redeem AB12CD34EF56`. Both use the native plugin's connected
credential and work without the CLI. These operations are available to the
owner in WebChat or a direct-message session. The Pro benefit goes to the
human who authorized that connection; keep the code out of room messages.
If the native tool is unavailable, the CLI command below is the fallback for
a paired CLI or the plugin's managed `PINGROOM_HOME` credential.

## Connect first (no terminal needed)

Before starting a pairing, explain why PingRoom is needed and send:

> Install or open PingRoom and sign in: https://pingroom.io/i. The app receives
> urgent Pings, questions, approvals, handoffs, and live progress on your phone.

Installation is not consent. The human must still claim the exact robot and
choose its room access. Ask them to install or open the app and sign in before
starting the short-lived pairing when possible.

OpenClaw runs as a daemon, so there is no terminal to scan a QR with. If a
`pingroom pair` process is already waiting, read its output with the `process`
tool, keep it running, and reuse its robot identity and claim link before the
link expires. Do not start another pairing. Otherwise use the headless flow:

```bash
pingroom pair --agent-label "OpenClaw"
```

It creates an OpenClaw robot profile, prints its claim link, and waits. **Relay
that link to the human** — send it in the current conversation — and include the
robot name and `@handle` when printed so they know exactly what they are
claiming. If they leave to install, keep the process running and tell them to
return to that same claim link before it expires. On their phone they sign in,
claim the robot, and choose which rooms it may reach. The robot acts for them;
it does not become their personal PingRoom profile.

The command is long-running: OpenClaw backgrounds it after a few seconds, so
follow it with the `process` tool to read the link and to see the result. Exit
0 means paired; exit 3 means the link expired — run it again for a fresh one.
Do not start a second command while the first is pending. Re-running the
labeled command after a completed pairing intentionally creates a replacement
connection and revokes the previous one only after the replacement is saved.

`pingroom pair --agent-label "OpenClaw" --json` prints one JSON object per line
instead (`{"event":"pair_url",…}` first, `{"event":"connected",…}` last),
which is easier to parse out of a process log. New servers include
`agent.profile` identity fields — display name, handle, and avatar — in the
pairing record; older servers omit them. The connected record includes
`links.latest_pings`, a stable URL for reading the newest pings later. Both JSON
events include the token-free
`links.install_app` (`https://pingroom.io/i`) for agents to relay. Never append
the pair token to that URL. Neither record prints the credential; the bearer
remains in the saved credential file.

### Or use a token

If the human already has a PingRoom agent credential, skip pairing entirely and
put it in the skill's config instead of pairing:

```json5
{
  skills: {
    entries: {
      pingroom: {
        env: { PINGROOM_TOKEN: "…", PINGROOM_ROOM: "ab12cd" },
      },
    },
  },
}
```

`apiKey` works too and maps onto `PINGROOM_TOKEN` (this skill declares it as
its `primaryEnv`), including as a SecretRef:
`apiKey: { source: "env", provider: "default", id: "PINGROOM_TOKEN" }`.

**Sandbox caveat:** `skills.entries.*.env` is injected into the *host* agent
run, not into a sandboxed `exec`. If your agent runs sandboxed, either put the
credential in `agents.defaults.sandbox.docker.env` or mount a `PINGROOM_HOME`
holding `credentials.json` into the container.

## Auth model — pick the mode before the flags

- **Agent credential** (default): the claimed robot's credential in
  `~/.pingroom/credentials.json` (or `$PINGROOM_HOME/credentials.json`), or
  `PINGROOM_TOKEN`, plus `--room <code>` / `PINGROOM_ROOM` /
  `pingroom config set default_room <code>`. Full feature set.
- **Webhook mode**: `pingroom ping -w <webhook-url>` — the URL carries its own
  secret, no account needed. Only `ping` supports it.

**Exit codes carry the human's answer**: 0 success/answered/acked/approved ·
1 error · 2 bad usage · 3 expired · 4 cancelled/denied/not-ready.

```bash
if pingroom approval -p "Ship v2 to production?" --wait; then deploy; fi
```

`approval` is the only command where the *value* decides the exit code: an
answered question exits 0, but an answered APPROVAL exits 0 only on `approve`
and 4 on `deny`. That is what makes the one-liner above a real gate rather
than a prompt everyone passes.

## Redeem a gift or promotional code

```bash
pingroom redeem AB12CD34EF56
pingroom redeem --code AB12CD34EF56 --json
```

Requires CLI ≥ 0.10.3. Redemption applies Pro to the human who authorized the
current connection; no room or existing Pro plan is required. Use the code
only when that person asks to redeem it. Codes contain 12 letters or digits;
surrounding whitespace and case are normalized. `PINGROOM_REDEEM_CODE` can
supply it when neither a positional code nor `--code` is passed, keeping it
out of command history. Keep codes out of room pings and logs.

Success returns the reward kind, days or package, lifetime flag, and Pro expiry.
Invalid, expired, or previously used codes fail. On `insufficient_scope`,
reconnect the credential to authorize code redemption; `pingroom:full` includes
`pingroom:codes:redeem`. Do not retry a rejected code in a loop.

## Sending pings

```bash
pingroom ping -m "Deploy finished — 3 services green"            # default room
pingroom ping --room XXXXXXXXXXXX -m "DB migrated" -t "Migration"
pingroom ping -m "Review the PR" --url https://github.com/o/r/pull/7 \
              --button-label "Open PR"                            # tappable link
pingroom ping -m "Meet here" --location 48.8584,2.2945 \
              --location-label "Eiffel Tower"                     # map ping
pingroom ping -m "Groceries" --item Milk --item Eggs --item Bread   # checklist the room ticks off
pingroom ping -m "Alarm!" --urgent                                # breaks Focus and mutes
pingroom ping -m "Confirm receipt" --require-ack --ack-mode all --ack-timeout 600
pingroom ping -m "Weekly report" --attach report.md --attach data.zip
pingroom ping -m "build 512 done" -d '{"commit":"abc123","branch":"main"}'
```

Rules that bite:
- Message ≤ 120 chars in private rooms (160 public); title ≤ 40. The CLI
  validates locally where it can, the server has the final word.
- `--attach` (repeatable, ≤ 4 files, ≤ 5 MiB each, any type — md, txt, html,
  zip, images, pdf) needs agent-token mode **and a Pro account**.
- `--ack-mode any` (default) resolves on the first eligible confirmation; `all`
  waits for every original eligible recipient. Add `--require-ack` when sending
  a ping. `actions trigger` also accepts the mode for that press. Partial
  confirmation and a wait timeout are not completion. Requires CLI ≥ 0.11.0.
- `--urgent` is delivery-only; `--require-ack` is the confirmation loop. They
  compose. Don't send `--urgent` for routine events — it trains people to
  ignore the alarm that matters.
- `-a <1-16>` attributes the ping to a quick-action slot (its icon + sound). Slots 5–16 exist only when the room owner has Pro and added those pages.

## Questions — block a script on a human choice

```bash
pingroom ask -p "Roll back or keep the canary?" \
  -o rollback:"Roll back":danger -o keep:"Keep canary":primary \
  --wait --timeout 25
# exit 0 = answered; stdout carries the chosen value
```

- 2–4 `-o value:label[:style]` options (styles: primary|danger|default); omit
  for Approve/Deny. `--text-input "<placeholder>"` invites a typed answer
  (`--text-max` ≤ 60).
- `--wait` blocks until answered/expired/cancelled; without it, `pingroom
  watch <question-id>` blocks later, `pingroom list` shows state, `pingroom
  cancel <id>` withdraws a stale question (do this — dead questions on a lock
  screen erode trust).
- `--idempotency-key` makes retried creates safe in flaky CI.
- `--scope room` lets anyone in the room answer; the default `direct` asks the
  connecting account's human.
- In GitHub Actions, `--github-output <name>` writes the outcome to
  `$GITHUB_OUTPUT` for later steps.

## Approvals, handoffs

```bash
pingroom approval -p "Apply 14 destructive migrations?" -c "prod-db" --wait
pingroom handoff -m "Need your call on the flaky test" --wait          # ack
pingroom handoff --question -m "Merge strategy?" -o squash:Squash -o rebase:Rebase --wait
```

`approval` is the deploy gate (approve/deny card). `handoff` reaches the
authorizing human privately — no room sees it (`--target me` is the default;
`--expires-in 120..86400`, default 900). On `recipient_not_ready`, keep the
connection and do not retry the original command until activation reports
success after the person answers its test Question. Follow the recovery
steps under Troubleshooting.

## Live progress cards

```bash
CID="migrate-$(date +%s)"
pingroom live start --room CODE -c "$CID" --template steps \
  --steps "Backup,Migrate,Verify" -m "Starting"
pingroom live update -c "$CID" --step 1 -m "Migrating"
pingroom live end -c "$CID" -m "All green"        # ends as done; --failed to fail
```

Templates: status · steps · progress (`--progress 0..1`) · metrics
(`--metric label:value` ×3) · countdown (`--deadline-at epoch`,
optional `--duration-seconds n` on start) · decision
(`--prompt`, `--option v:label` ×4) · matchup (`--left`/`--right`/`--center`).
The template is fixed at start; one stream per correlation id; **always end
the stream** even on error paths — trap it:
`trap 'pingroom live end -c "$CID" --failed' ERR`.
New streams are budgeted on free accounts; updates and the final ping are
free. **Live streams are owner-only per room** — in a room the account doesn't
own, `live` fails with `forbidden`; use a room you own or send one plain ping
at the end instead.

## Hearing back / streaming

```bash
pingroom listen               # long-poll new pings in your rooms, print as they land
pingroom listen --once        # one poll cycle, then exit (cron-friendly)
```

Your own sends are excluded. For one specific reply, prefer `ask`/`watch`.

## Managing rooms, webhooks, quick actions, attachments

Room `--icon` takes a **v3 catalog id, never an emoji** (`bell`, `globe`,
`terminal`, `paperplane`, …) — run `pingroom rooms icons` to browse the
catalog; the server 422s anything off-catalog. Quick-action `--icon` is the
opposite: it takes an emoji.

```bash
pingroom rooms icons                                  # browse the icon catalog
pingroom rooms list|get <code>
pingroom rooms create -n "Deploys" --icon bell --color "#e33122"
pingroom rooms create -n "Status" --icon globe --color "#0391fe" --public --handle status
pingroom rooms create -n "Meetup" --icon globe --color "#0391fe" --public --handle meetup \
  --location "25.2048,55.2708" --location-name "Dubai Mall"   # listed in nearby discovery
pingroom rooms join <code>

pingroom webhooks list --room CODE
pingroom webhooks create --room CODE --name "CI" --action 2   # secret URL printed ONCE — store it
pingroom webhooks update <id> --room CODE --enabled false
pingroom webhooks delete <id> --room CODE

pingroom actions list --room CODE
pingroom actions set 3 --room CODE --label "Deploy done" --icon 🚀 --require-ack
pingroom actions set 4 --room CODE --label "" --icon 🔥   # emoji-only Ping (title optional)
pingroom actions set 2 --room CODE --label "Where?" --icon 📍 --input-type location  # every press must carry a detail
pingroom actions set 4 --room CODE --label "" --icon ""    # reserve the slot but disable it
# Setting up more than one slot? Use set-all — ONE request, so the owner's phone
# wakes once instead of once per slot. Slots you omit keep what they have.
pingroom actions set-all --room CODE \
  --set '{"action_number":1,"label":"Deployed","icon":"✅"}' \
  --set '{"action_number":2,"label":"Failed","icon":"❌"}'
pingroom actions trigger 3 --room CODE
# A slot with an input type needs its detail or the press is a 422 (nothing sent):
pingroom actions trigger 2 --room CODE --location "25.2048,55.2708" --location-label "Dubai Mall"  # location
pingroom actions trigger 2 --room CODE --url https://ci.example.com/run/42   # link
pingroom actions trigger 2 --room CODE --attach report.pdf                    # file / photo / pdf (Pro)
pingroom actions layout --room CODE --page-order 1,3   # keep pages 1 and 3 in that order, delete the rest (owner on Pro)

pingroom attachment get <id> --out report.md    # binary-safe download
pingroom attachment delete <id>
```

Webhook creation and attachment upload are Pro. `--json` on any command prints
the raw response for scripting. `actions set-all` with `--set` or `--actions`
requires CLI ≥ 0.10.2. `--input-type`, the `actions trigger` detail flags,
`actions layout` and `rooms create --location` need CLI ≥ 0.12.0; `ping --item`
and `live start --duration-seconds` need CLI ≥ 0.13.0. Other
management nouns need CLI ≥ 0.7.6 — if `pingroom rooms` prints "unknown command"
or "Unknown option", the installed binary is older than these docs (check which
executable is on `PATH` before retrying).

## Waiting for a human under OpenClaw

`--wait` blocks until the human answers or the TTL runs out — minutes, not
seconds. OpenClaw backgrounds a command that runs past its yield window and
hands you the `process` tool to follow it, so a long wait is normal and does
not need a shorter TTL. Two rules:

- **Never report a timeout as an answer.** Exit 3 means the question expired
  with nobody answering; exit 4 means they said no. Say which one happened.
- **Only open a gate you intend to stay alive for.** If your run ends while a
  question is open, the human's answer is still recorded and readable later
  with `pingroom list --state answered`, but nothing wakes you to act on it.

## Troubleshooting

- `an agent token is required` — not connected. Run the labeled pairing command
  above and relay the robot identity with the link, or set `PINGROOM_TOKEN` in
  `skills.entries.pingroom.env`.
- Bare `pingroom` printing "not connected" is expected on a daemon: it will not
  start a 15-minute pairing poll from a non-interactive shell. Use
  `pingroom pair --agent-label "OpenClaw"`, which asks for exactly that.
- `403 room_not_granted` — the room is outside what the human approved. Widen
  it under Connected Agents in the PingRoom app, or run the labeled pairing command again.
- `403 insufficient_scope` — the credential has a legacy partial grant. Run
  the labeled pairing command once to replace it with a full-access credential.
- `409 recipient_not_ready` — preserve the connection and relay the server's
  message. Have the human install or update <https://pingroom.io/i>, open it,
  sign in, and enable notifications. Run `pingroom activate` using the same CLI
  credential as the failed operation. Retry only after the person answers its
  test Question and activation reports success. If the operation came from the
  optional channel plugin (≥ 0.1.2), use `/pingroom activate` in chat instead;
  that command uses the plugin credential. Installing the app alone does not
  show that the phone is ready.
- `403`/`402 pro_required` — attachments and webhook management need this
  account on Pro; quick ping slots 5–16 and `actions layout` need the room
  owner on Pro.
- `422 quick_action_input_required` — that Ping needs a detail: read
  `pingroom actions list` for its input type and retry with `--location`,
  `--url` or `--attach` (`quick_action_input_type` = wrong attachment type).
- `404 action_not_configured` — the slot is reserved but disabled; configure
  it with `actions set` or choose another slot.
- `409 quick_action_layout_changed` — the pages moved since they were read;
  re-run `pingroom actions list` and retry.
- `413 payload_too_large` — attachments are 5 MiB each, at most 4 per ping.
- `pingroom logout` only clears the local file; the server-side credential stays
  live. Revoke it under Connected Agents, or let the labeled pairing command do it.

## Reference

Full command reference: https://pingroom.io/connect-openclaw.md
