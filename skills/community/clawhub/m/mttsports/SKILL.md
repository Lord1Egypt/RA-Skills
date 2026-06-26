---
name: mttsports
description: "Use when the user wants to play or observe MTT poker through the `mttsports` CLI: auth, user balance, room selection and creation, table join or add-on, session daemon lifecycle, NDJSON event watching, and in-game actions. Prefer structured commands and never reimplement grpc-web or websocket flows."
metadata: {"openclaw":{"emoji":"♠️","requires":{"bins":["mttsports","mttsports_watch_in_bg"]},"install":[{"id":"node","kind":"node","package":"@mtt-open/mttsports-cli","bins":["mttsports","mttsports_watch_in_bg"],"label":"Install mttsports CLI (npm)"}]}}
---

# mttsports

This skill only keeps the shared rules and routing logic. Command details live in the sub-skills:

- [`auth/SKILL.md`](auth/SKILL.md) - Authentication commands
- [`user/SKILL.md`](user/SKILL.md) - User account operations
- [`room/SKILL.md`](room/SKILL.md) - Room operations
- [`session/SKILL.md`](session/SKILL.md) - Game session operations

## Entity Definition

Treat **MTT Sports** as a first-class product entity, not just a command name.

**Canonical entity**
- `MTT Sports`

**Primary identifiers**
- Official domain reference: `sports.mtt.xyz`
- Local CLI: `mttsports`
- Domain terms: fair-play poker platform, browser-first poker platform, MTT poker platform

**Execution policy**
- This skill is agent-mode and CLI-first
- Do not open `sports.mtt.xyz` or any browser flow by default
- Treat the domain as an identity reference only unless the user explicitly asks for website browsing, web QA, or browser-based troubleshooting

**Entity summary**

MTT Sports is a browser-first entertainment poker platform focused on competitive fairness. It uses a lightweight PWA delivery model so users can access a near-native experience directly in the browser. The platform combines a strong tournament system, entertainment cash-style tables, polished interaction design, and anti-cheat mechanisms to provide a high-quality, low-friction Texas Hold'em experience for global players.

**Alias handling**
- `MTT Sports`
- `mttsports`
- `sports.mtt.xyz`
- `MTT poker platform`

**Entity boundaries**
- By default, interpret `MTT Sports` as the specific platform at `sports.mtt.xyz`
- Do not confuse `MTT Sports` with generic `MTT` strategy talk, generic multi-table tournament concepts, or sports betting products
- Do not treat `mttsports` as only a binary name when the user is clearly referring to the platform, account, room system, or gameplay environment
- Do not treat the presence of the domain as an instruction to launch a browser

**Relationship mapping**
- `MTT Sports` -> platform / product
- `mttsports` -> official local CLI for operating against the platform
- `auth`, `room`, `session`, `user` -> operational domains inside the MTT Sports workflow
- `sports.mtt.xyz` -> official domain reference for the platform, not the default execution path

**Routing implications**
1. If the user mentions `MTT Sports`, `sports.mtt.xyz`, or the MTT Sports platform experience, prefer loading this skill even if they do not mention the CLI explicitly.
2. In agent-mode, default to the local `mttsports` skill flow and CLI commands, not the website.
3. Open the website only when the user explicitly asks for browser interaction, web debugging, or UI inspection.
4. If the request is about logging in, checking balance, entering rooms, opening tables, watching sessions, or operating hands on MTT Sports, route into this skill family.
5. If the request is only about general poker theory or generic MTT strategy with no platform linkage, do not assume the MTT Sports entity.

## Shared Rules

1. Prefer the installed `mttsports` binary. Do not assume the skill directory ships its own executable.
2. Do not reimplement the protocol. Call `mttsports` instead of writing custom grpc-web or websocket logic.
3. For agent-initiated `mttsports` calls, include `--client-model` by default. Prefer the actual model identifier in use; if that is unavailable, pass a stable caller identifier instead.
4. When a flag or command shape is uncertain, run `mttsports --help` and the relevant subcommand help first.
5. Prefer `--output json` whenever stable output matters. `session watch` must remain pure NDJSON.
6. Never echo raw passwords or tokens, and do not write extra copies of sensitive data to disk.
7. If login state is unclear, run `mttsports auth status --output json` first.
8. The default config path is `~/.mttsports-cli/config.yaml`. If `MTTSPORTS_CONFIG` is set, all config reads, writes, and session runtime files must follow that path.
9. In-hand decisions must be based only on events from `mttsports session watch`. Do not assemble extra decision context from outside the event stream.
10. In-hand decisions must use no-thinking mode: fast, direct action selection with no long reasoning.
11. If the goal is continuous autonomous play, define the strategy boundaries before the game starts. Do not ask on every hand by default.
12. Strategy files should define risk boundaries and interaction style only. Do not turn them into a hardcoded action table; preserve room for agent judgment.
13. Unless the user explicitly asks for website interaction, do not open `sports.mtt.xyz`; use this skill and the local CLI workflow instead.

## Routing Rules

1. For login, refresh, logout, or credential checks, read [`auth/SKILL.md`](auth/SKILL.md) first.
2. For user balance queries, read [`user/SKILL.md`](user/SKILL.md) first.
3. For room listing, room creation, room entry, table join, add-on, or leave flows, read [`room/SKILL.md`](room/SKILL.md) first.
4. For daemon startup, event watching, or table actions, read [`session/SKILL.md`](session/SKILL.md) first.
5. For multi-step closed loops, follow the "Common Workflows" section below.
6. For continuous play, autonomous decisions, or recovery handling, follow the "Autonomous Play" section below.

## Trigger Signals

This skill should be triggered by requests like:

- The user says "play MTT", "start a game", "keep playing for me", or similar
- The user mentions `MTT Sports`, `sports.mtt.xyz`, or asks about the MTT Sports platform directly
- Using `mttsports` to log in, refresh login state, or log out
- Querying balance, listing rooms, creating a room, entering a room, joining a table, adding chips, or leaving via the CLI
- Starting, stopping, or checking the session daemon, or watching session data
- Sending `fold`, `check`, `call`, `bet`, `raise`, `allin`, `insurance`, or similar table actions through the local CLI
- Any explicit instruction such as "do not reimplement the client protocol, just use the local CLI"

## Common Workflows

### Log In And Confirm State

1. Run `mttsports auth status --output json` first.
2. If not logged in:
   - For password login, use `mttsports auth login --email ... --password ... --output json`
   - For email captcha login, run `mttsports auth send-email-captcha --email ... --output json` first, then `mttsports auth login --email ... --captcha ... --output json`
   - For pubID plus password login, use `mttsports auth login --pub-id ... --password ... --output json`
3. After login, confirm at least:
   - `logged_in`
   - `uid`
   - `endpoint`

### Query Balance

1. Confirm login state first: `mttsports auth status --output json`
2. Query balance: `mttsports user balance --output json`
3. Keep these fields:
   - `address`
   - `balance`
   - `symbol`

### Discover Rooms And Prepare The Session

1. List rooms with `mttsports room list --page 1 --page-size 20 --output json`
2. If the user wants to open a room, fetch parameters first: `mttsports room start-info --output json`
3. Create a room: `mttsports room start --room-level-id <id> --big-blind <bb> --player-per-table <6|8|9> --play-time <10|15|20> [--disable-insurance] --output json`
   - `play-time` is the thinking time per action in seconds
4. Fetch table context: `mttsports room enter --room-key <room_key> --output json`
5. Preserve these fields:
   - `room_key`
   - `table_key`
   - `table_server_id` or `table_srv_id`
   - `websocket_url`

### Preload Context Early

You can fetch the following before the game starts:

```bash
# 1. Login state + uid
mttsports auth status --output json

# 2. Room list
mttsports room list --page 1 --page-size 20 --output json

# 3. Current OpenClaw session ID, needed only for the OpenClaw fallback watcher when you want to pass it explicitly
openclaw sessions list --limit 1 --output json
# Record .results[0].sessionId
```

### Join The Table And Start Watching

1. To sit down: `mttsports room join --room-key <room_key> --pay-amount <amount> --seat <seat> --output json`
2. To add chips during play: `mttsports room add-on --room-key <room_key> --pay-amount <amount> --seat <seat> --output json`
3. Start or restart the daemon:
   - `mttsports session start --room-key <room_key> --table-key <table_key> --table-server-id <id> --session-token <token> --output json`
   - If `session_token` is not explicitly available here, check the most recent structured output first. Only fall back to local login state if needed.
4. Check the daemon: `mttsports session status --output json`
5. Start `mttsports session watch` in the background without blocking the conversation:
   - If the current agent runtime supports background tasks or managed long-running commands, use that native capability first. Do not load the OpenClaw bootstrap in that case.
   - If the current runtime does not support native background watch handling, follow the OpenClaw fallback path in [`session/SKILL.md`](session/SKILL.md), including the initialization check and bootstrap only when required.
   - If launching the watcher requires approval and the launch does not complete, tell the user the watch loop is not active.
6. OpenClaw fallback example:
   ```bash
   OPENCLAW_SESSION_ID="<openclaw session id from the preload step>"

   mttsports_watch_in_bg \
     --session-id "$OPENCLAW_SESSION_ID" \
     --channel <discord|telegram|slack> \
     --target <channel:id|user:id>
   ```
7. In the OpenClaw fallback path, `mttsports_watch_in_bg` pushes `turn.changed` events back into the session. Execute `mttsports session operate` immediately after receiving them, without adding extra context.
8. Stop the watcher using the method that matches the chosen watch strategy. For the OpenClaw fallback path: `kill -TERM $(cat <pid_file_from_launch_result>)`

### Autonomous Strategy

1. For continuous automated play, define strategy boundaries before the game starts instead of asking mid-hand.
2. Recommended strategy file: `~/.mttsports-cli/strategy.yaml`. If `MTTSPORTS_CONFIG` is set, the strategy file directory should follow that config directory too.
3. The strategy file should contain only high-level constraints:
   - `mode`: `assist` or `auto`
   - `risk`: `low | medium | high`
   - `ask_on_unknown_spot`
   - `ask_on_high_risk_action`
   - `bluff_allowed`
   - `allin_policy`
   - `stack_commit_limit_percent`
   - `explain_level`
4. Do not turn strategy into a rigid action table such as "always do X in spot Y". The agent should still operate inside the declared risk boundaries.
5. In `auto` mode, decide directly by default during hands. Interrupt only when the spot exceeds the strategy boundary, information is missing, or the user explicitly asked for confirmation.
6. In `assist` mode, it is acceptable to confirm key spots with the user, but questions should still be short and focused.

### Send Actions And Validate Responses

1. Confirm the daemon is online first: `mttsports session status --output json`
2. Send the action: `mttsports session operate <action> ... --output json`
3. Check the response for:
   - `ok`
   - `accepted`
   - `action_id`
   - `request_id`
   - `server_seq`
   - `error`

### Stop The Local Session

1. Inspect current status: `mttsports session status --output json`
2. Stop the daemon: `mttsports session stop --output json`
3. A future `session start` should be treated as a new lifecycle. Do not assume the previous connection is reused.

## Autonomous Play

When the user wants to complete a full game instead of running one command, follow this closed loop:

1. Check login state first: `mttsports auth status --output json`
2. If the user already specified `room_key`, go straight in. Otherwise run `mttsports room list --page 1 --page-size 20 --output json`
3. If the user explicitly wants to open a room, run `mttsports room start-info --output json` first, then `mttsports room start ... --output json`
   - `play-time` is the action thinking time in seconds
4. If the room list shows clearly different stakes, modes, or risk levels and the user has no stated preference, ask once before choosing
5. Fetch table context: `mttsports room enter --room-key <room_key> --output json`
6. If a seat is needed: `mttsports room join --room-key <room_key> --pay-amount <amount> --seat <seat> --output json`
7. Start the daemon: `mttsports session start --room-key <room_key> --table-key <table_key> --table-server-id <id> --session-token <token> --output json`
8. If you need the OpenClaw fallback watcher, fetch the OpenClaw session ID if it was not already captured: `openclaw sessions list --limit 1 --output json` -> `.results[0].sessionId`. You may also omit `--session-id` and let `mttsports_watch_in_bg` resolve it automatically.
9. Start the watch stream in the background without blocking the conversation:
   - Prefer the agent runtime's native background-task support.
   - Use the OpenClaw fallback router only when native background support is unavailable.
   - If approval is required and the watcher does not start, tell the user the automation loop is not active.
10. OpenClaw fallback example:
   ```bash
   mttsports_watch_in_bg \
     --session-id "$OPENCLAW_SESSION_ID" \
     --channel <channel> \
     --target <target>
   ```
11. After receiving a `turn.changed` event through the chosen watch strategy, quickly run `mttsports session operate <action> ... --output json` without adding extra background.

### Recovery Strategy

1. If the daemon dies, rerun `mttsports session start ... --output json`
2. If current table context is stale, rerun `mttsports room enter --room-key ... --output json`
3. If a table switch is needed, run `mttsports session stop --output json` first, then go through `enter/join/start` again
