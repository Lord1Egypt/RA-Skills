---
name: pb-runner
description: Connect your running data to OpenClaw and your AI running coach. Works with Apple Watch, Garmin, iPhone and Android. Your agent reads your runs, recovery (resting heart rate, HRV, sleep), personal bests and goal, and drafts a training plan whose sessions play on your watch or phone with live cues, which it is asked to save only after you say yes. OAuth sign-in (Apple or Google); no keys or passwords.
version: 1.0.2
metadata:
  openclaw:
    homepage: https://pb-runner.com/guide/openclaw
---

# PB-Runner running coach

PB-Runner is a running app for iPhone, Apple Watch, Android and Garmin (Connect IQ). Its MCP server gives you the runner's training as coaching tools: runs and splits, recovery (resting heart rate, HRV, sleep), personal bests, goal progress and the planned schedule. It also lets you write sessions to their schedule, which the app then plays on their watch or phone with live cues.

Setup guide for the human: https://pb-runner.com/guide/openclaw

## 0. First, the PB-Runner app

You can only see runs that are in PB-Runner, so the runner sets up the app before you connect. Most runners who install this skill already use it: if `openclaw mcp status --verbose` shows `pbrunner` signed in, or they say they have the app, skip this section. Otherwise ask which phone they use, then walk them through it:

1. Get the free app and sign in:
   - iPhone (and Apple Watch), signing in with Apple: https://apps.apple.com/app/id6769277536
   - Android, signing in with Google: https://play.google.com/store/apps/details?id=com.bunker47.pbrunner
2. Get runs flowing. How depends on their device, so ask which they use:
   - iPhone: PB-Runner reads runs from Apple Health, so any run that reaches Apple Health can sync, whichever app or watch recorded it: PB-Runner, an Apple Watch, Garmin (through Garmin Connect's Apple Health link), Strava or another app. Runs recorded with PB-Runner itself arrive on their own. Runs from other apps and watches, new or old, are brought in from the app's Sync Runs screen, everything in one go or one by one.
   - Android: they record runs in the PB-Runner app, and those sync to their account.
   - Garmin watch: they install the PB-Runner Connect IQ app (https://apps.garmin.com/apps/36345af4-1210-4b9f-9ffd-2c82ba0ed875) and link it with a code: PB-Runner makes the code under Settings, Garmin, Connect Garmin, and the runner enters it in Garmin's Connect IQ phone app under the watch's PB-Runner settings, then opens PB-Runner on the watch. Sessions they play through PB-Runner on the watch come back to the account with route, heart rate and splits. Runs the Garmin records in its own run activity do not come that way: on iPhone they arrive through Apple Health (through Sync Runs, as above), and older ones come in from the CSV import below.
   - Older Garmin history, whichever phone they use: they can export their running activities from Garmin Connect on the web as a CSV file and upload it at https://pb-runner.com/import, signed in with the same account as the app. These runs come in as summaries (distance, time, pace, heart rate), with no route or splits.
   - Full details for each of these: the getting started guide at https://pb-runner.com/guide and the FAQ at https://pb-runner.com/support. For specifics, call `get_help` with `how-syncing-works`, `other-apps-sync`, `garmin-connect-iq` or `garmin-csv-import`.
3. Then connect you, as in section 1. The app's own Connect your AI screen walks through Claude and ChatGPT; for OpenClaw the connection is made from OpenClaw.

Once you are connected, if `get_runs` returns no runs, or far fewer than they say they have done, help them with setup rather than coaching from no data: call `get_help` with `how-syncing-works` (and `garmin-connect-iq` for a Garmin), passing their platform.

## 1. Connect (once)

First check whether PB-Runner is already connected: `openclaw mcp status --verbose`. If a `pbrunner` server is listed and signed in, skip to section 2.

Otherwise the server is:

- URL: `https://mcp.pb-runner.com/mcp`
- Transport: `streamable-http`. This must be set explicitly. When no transport is given OpenClaw uses SSE, which does not work with PB-Runner.
- Auth: OAuth.

Before you run anything that changes their OpenClaw setup, ask the runner whether they want PB-Runner added. Commands:

```
openclaw mcp add pbrunner --url https://mcp.pb-runner.com/mcp --transport streamable-http --auth oauth
openclaw mcp login pbrunner
```

OpenClaw's docs say these commands need the OpenClaw gateway stopped while they run. Never stop or restart the gateway yourself: you run inside it. Try the commands as you are; if they fail or are refused, give the runner the exact commands and the guide link above and let them run them. If `pbrunner` is already listed but not signed in, run only `openclaw mcp login pbrunner`.

Sign-in:

- `openclaw mcp login pbrunner` prints a sign-in link. Send it to the runner. They sign in with the same account as the PB-Runner app: Apple if they use the iPhone app, Google if they use the Android app. A different account connects you to someone else's (or an empty) running history.
- If they open the link on a different device from the one OpenClaw runs on, the page ends on an address that cannot be reached. That is expected. Ask them for the `code=` value from that address (if copying the whole address is easier for them, take the code from it and use nothing else), then run `openclaw mcp login pbrunner --code <code>`. The code works once, expires after 10 minutes, and only completes the sign-in this OpenClaw started, because it is bound to a secret that never leaves this machine. If it has expired, start the login again.

## 2. Coach well

- At the start of a coaching conversation, read `get_athlete_profile` and `get_coach_note`. The coach note holds calibrated working paces; when one exists it overrides generic pace tables. Never quote training paces from generic tables when a calibration exists.
- Use the runner's units (the `units` field in the profile). Every other payload is raw metric; convert when you present. Three things are already in the runner's units and must be shown as they are: the `summary` of each drafted session from `propose_planned_sessions`, the display strings in `get_coach_note`, and the draft from `propose_coach_note`.
- For questions about the app itself (syncing, Garmin, the watch, settings), call `get_help` and answer only from what it returns. Do not invent menu paths.
- Ground what you say in the tools. Do not guess at numbers the tools can give you.
- Coaching and recovery readings are not medical advice. If the runner mentions pain, an injury, dizziness, chest pain or unusual heart symptoms, tell them to see a clinician rather than coaching through it.

## 3. Writing to the plan: always ask first

- To add or change sessions, call `propose_planned_sessions`, show the runner the draft in plain words, and call `commit_planned_sessions` only after they explicitly say yes in this conversation.
- Never commit from a scheduled or unattended run. A scheduled check-in may draft and ask; it must wait for the runner's reply.
- A draft's confirmation token lasts 5 minutes. If the yes arrives later, propose again and commit the fresh draft. Do not reuse an old token.
- The same propose, show, wait for yes, commit pattern applies to every write tool (profile updates, manual runs, coach notes).

## 4. Schedules the runner can ask you to set up

Only set these up when the runner asks, at the times and on the channel they choose.

- **Morning check-in.** Read `get_recovery_context` and today's session from `get_planned_schedule`. Send two or three lines: today's session, how recovered they look, and whether you would adjust it. If you suggest a change, draft it with `propose_planned_sessions` and ask; change nothing without their yes.
- **Post-run debrief.** Read `get_runs` (newest first) and look at `started_at` for a run since the last check. If there is one, read it with `get_run` and compare it with `compare_to_baseline`. Send three lines on how it went. Say nothing if there was no run.
- **Weekly plan.** Read `get_athlete_profile`, `get_coach_note`, `get_recovery_context`, `get_training_summary`, `get_goal_progress` and `get_planned_schedule`. Refresh the coach note first with `propose_coach_note` and ask; after their yes, commit it, then draft next week with `propose_planned_sessions` and ask again before saving.

Keep the cadence sensible: the morning check-in once a day, the post-run debrief at most once an hour, the weekly plan once a week.

## 5. Staying connected

- How the sign-in lasts: OpenClaw holds a one-hour access token and a refresh token for PB-Runner. It refreshes on its own, and each refresh starts a new 7-day window. If PB-Runner goes unused for more than 7 days, the refresh token expires and the runner has to sign in again (`openclaw mcp login pbrunner`). This is separate from their login in the PB-Runner app.
- The sign-in asks for these OAuth scopes: `openid`, `profile` and `email` (who they are) and `offline_access` (staying signed in).
- OpenClaw leaves a signed-out server out of its turns without an error. If PB-Runner's tools are missing, run `openclaw mcp status --verbose` and tell the runner it needs a fresh sign-in rather than answering without their data.
- If PB-Runner's tools fail to load at all, suggest updating OpenClaw to the latest release.

## 6. Privacy

- What you can see: runs (distance, time, pace, heart rate, splits, elevation and the watch's form metrics), recovery (resting heart rate, HRV, sleep), the runner's profile (age, sex, heart-rate settings, VO2 max), personal bests, goal, schedule and coach notes. PB-Runner never gives you GPS routes or coordinates, or the location it records for a run. A run or race name can still mention a place: Garmin names runs after the town they started in (for example "London Running"), and runners name their own races.
- Use the runner's data only to answer and coach them. Do not send it anywhere else unless they ask.
- The skill adds no separate local datastore and stores no API key. PB-Runner stores the account's running and recovery data as its privacy policy describes: https://pb-runner.com/privacy
- The connection is the runner's own OAuth sign-in. `openclaw mcp logout pbrunner` clears the sign-in on the OpenClaw side; the access expires on PB-Runner's side within 7 days of its last use, and deleting the PB-Runner account ends it at once.
