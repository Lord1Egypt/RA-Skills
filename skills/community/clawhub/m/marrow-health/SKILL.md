---
name: marrow-health
description: Read and log your own health and fitness data from the Marrow iPhone app (Apple Health metrics, sleep, meals, water, weight, workouts, strength sets, mood). Use when the user asks how they slept, how today compares with their usual, what they ate, about training, steps, heart rate or weight, wants a weekly review, or asks to log something.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🦴"
    homepage: https://marrowhealthapp.com/mcp
---

# Marrow Health

Marrow is an iPhone app that keeps a person's health data in one place:
Apple Health metrics, sleep, meals, water, weight, workouts, strength
sets, symptoms and mood. Its MCP server, `marrow`, answers from the
user's own Marrow data, reconciled the way the app shows it. Answer from
it, never from assumptions.

## Setup (once)

The user needs the Marrow app (App Store) with Cloud MCP turned on, a
Marrow Pro feature: in Marrow, open Connects, then AI, then OpenClaw.

1. Add the server to `~/.openclaw/openclaw.json` under `mcp.servers`:

   ```json
   {
     "mcp": {
       "servers": {
         "marrow": {
           "url": "https://connect.marrowhealthapp.com/mcp",
           "transport": "streamable-http",
           "auth": "oauth"
         }
       }
     }
   }
   ```

   No Node, no bridge and no token in the file: sign-in is OAuth.
2. Run `openclaw mcp login marrow` and open the printed link. The page
   asks "Which Marrow is this?": in Marrow, open Connects, then AI,
   then OpenClaw, tap Copy your link and paste it. Then type the
   six-character code the page shows into Marrow and tap Approve.
3. Check with `openclaw mcp doctor marrow --probe`.

If the browser runs on another device than OpenClaw, finish the page
there and pass the final redirect address to
`openclaw mcp login marrow --callback-url '<url>'`. A 401 later means
the sign-in was revoked in Marrow: run `openclaw mcp logout marrow`, then
log in again.

People who run Marrow's server at home or on their own machine use the
address Marrow shows for that door instead. Marrow's OpenClaw screen
gives the exact JSON for each.

## Which tool answers what

- Today, or "how am I doing": `daily_brief`. Each key metric comes with
  a phrase against the user's own recent normal, food and water against
  targets, last night's sleep, training, mood and flags. Start here.
- Is a number usual for this person: `baselines`. Compare with their own
  normal, not with population ranges.
- What is different lately, weekly reviews: `what_changed`.
- Before concluding something did not happen: `data_quality`. A stale
  or missing stream is not a zero.
- Detail: `health_summary`, `metric_daily`, `metric_samples`,
  `workouts`, `strength_log`, `nutrition_log`, `sleep_log` (the source
  for nights), `symptoms_and_mood`, `targets`.
- Every read takes `days` back, or `from` and `to` on the phone's
  calendar (YYYY-MM-DD).

## Logging

Only when the user asks: `log_meal`, `log_water`, `log_weight`,
`log_workout`, `log_strength`, `log_sleep`, `log_symptom`, `log_mood`,
`edit_entry`, `delete_entry`, `set_targets`, `undo_entry`. The phone
applies each change. If a write answers that adding entries is turned
off, the switch is in Marrow: Connects, AI, OpenClaw, Allow AI write.
Never log, change or remove anything the user did not ask for, and ask
before an edit, a deletion or an undo. Confirm what was logged in one
line.

## Limits

- Only the signed-in user's own data.
- No bulk delete. `delete_entry` removes one food entry at a time. The
  whole copy is deleted in Marrow: Connects, Cloud MCP, Delete the copy.
- Types without a log tool (blood pressure, medications) cannot be
  logged from here. Say so and point to the phone's health app.
- Water and weight cannot be undone from here once applied.

## Wording

Neutral wellness wording. Describe, compare with the user's own normal,
suggest. Do not diagnose or alarm. Quote units. Say plainly when data is
missing or stale.
