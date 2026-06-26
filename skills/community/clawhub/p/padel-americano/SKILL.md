---
name: padel-americano
description: "Create and manage fair-shuffled Padel Americano sessions: register players, generate fixed or open-ended rounds, record game scores, add/remove/substitute players mid-session, compute official and alternative leaderboards, and export statistics/schedules to PDF. Use it when you need to run a padel Americano tournament, generate rotations, record scores, adjust rosters, or export schedules and standings."
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Padel Americano

Use this skill when the user asks to create, run, score, update, or export a Padel Americano event.

## Tool

Use the bundled CLI:

```bash
SKILL_DIR=/path/to/padel-americano
python3 "$SKILL_DIR/scripts/padel_americano.py" --help
```

The CLI stores each tournament as JSON and can export PDF via headless Chrome/Chromium when available. It uses a fair-shuffled Americano rotation that avoids repeated partners/opponents where possible; it is not a strict printed rotation-chart template.
Player names are passed as a comma-separated `--players` string; do not pass a local file path as player input.

## Core Workflow

1. Ask the user for total points per game before creating a tournament or session. Recommend common short-game values such as 5 or 21 points when they are unsure.
2. For fixed events, create a tournament with player names, number of courts, rounds, and the chosen points per game.
3. For casual/open-ended events, create a session without a fixed round count and generate one round at a time.
4. Share the generated schedule with the user or export it.
5. Record scores as games finish.
6. Check the standard Americano leaderboard by total points, or alternative leaderboards by wins, points percentage, or wins percentage.
7. If a player needs to switch mid-session, replace that player from a specified round onward, then regenerate only unplayed future rounds.
8. Treat mid-session joins, leaves, pauses, and removals as operational extensions for real events, not core Americano rules.
9. If a new player joins mid-session, add that player from a specified round onward; do not force them to catch up to everyone else's total game count.
10. If a player leaves without a replacement, remove that player from a specified round onward, then regenerate only unplayed future rounds.
11. Export schedule, scores, and leaderboard to PDF when requested.

## Common Commands

Create a new Americano:

```bash
python3 "$SKILL_DIR/scripts/padel_americano.py" new \
  --name "Padel Americano" \
  --players "Alex,Blake,Casey,Drew,Elliot,Finley,Gray,Hayden" \
  --courts 2 \
  --rounds 6 \
  --points 24 \
  --out ./padel/americano.json
```

Create an open-ended Americano session:

```bash
python3 "$SKILL_DIR/scripts/padel_americano.py" new-session \
  --name "Padel Americano" \
  --players "Alex,Blake,Casey,Drew,Elliot,Finley,Gray,Hayden" \
  --courts 2 \
  --points 24 \
  --out ./padel/americano.json
```

Generate the next open-ended round:

```bash
python3 "$SKILL_DIR/scripts/padel_americano.py" next-round \
  ./padel/americano.json
```

Show schedule:

```bash
python3 "$SKILL_DIR/scripts/padel_americano.py" schedule \
  ./padel/americano.json
```

Record a score:

```bash
python3 "$SKILL_DIR/scripts/padel_americano.py" score \
  ./padel/americano.json \
  --round 1 --court 1 --score 14-10
```

The two team scores must add up to the configured `points_per_game`. For example, a 21-point game accepts `12-9`, `21-0`, or `10-11`, but rejects `12-8` and asks for the game score to be entered again.

Leaderboard:

```bash
python3 "$SKILL_DIR/scripts/padel_americano.py" leaderboard \
  ./padel/americano.json
```

The default leaderboard is `points`, matching standard Americano: total individual points, point difference, wins, points percentage, fewer games, then name.

Leaderboard variants:

```bash
python3 "$SKILL_DIR/scripts/padel_americano.py" leaderboard \
  ./padel/americano.json \
  --sort points

python3 "$SKILL_DIR/scripts/padel_americano.py" leaderboard \
  ./padel/americano.json \
  --sort wins

python3 "$SKILL_DIR/scripts/padel_americano.py" leaderboard \
  ./padel/americano.json \
  --sort points-pct

python3 "$SKILL_DIR/scripts/padel_americano.py" leaderboard \
  ./padel/americano.json \
  --sort wins-pct

python3 "$SKILL_DIR/scripts/padel_americano.py" leaderboard \
  ./padel/americano.json \
  --sort official
```

Switch a player from a round onward:

```bash
python3 "$SKILL_DIR/scripts/padel_americano.py" switch \
  ./padel/americano.json \
  --out-player "Alex" --in-player "Jordan" --from-round 4
```

Add a new player from a future round:

```bash
python3 "$SKILL_DIR/scripts/padel_americano.py" add-player \
  ./padel/americano.json \
  --player "Jordan" --from-round 5
```

Remove a player from a future round:

```bash
python3 "$SKILL_DIR/scripts/padel_americano.py" remove-player \
  ./padel/americano.json \
  --player "Alex" --from-round 4
```

Operational extension for open-ended player flow:

```bash
python3 "$SKILL_DIR/scripts/padel_americano.py" join-player \
  ./padel/americano.json \
  --player "Jordan"

python3 "$SKILL_DIR/scripts/padel_americano.py" leave-player \
  ./padel/americano.json \
  --player "Alex"

python3 "$SKILL_DIR/scripts/padel_americano.py" pause-player \
  ./padel/americano.json \
  --player "Blake"

python3 "$SKILL_DIR/scripts/padel_americano.py" resume-player \
  ./padel/americano.json \
  --player "Blake"
```

Export PDF:

```bash
python3 "$SKILL_DIR/scripts/padel_americano.py" export-pdf \
  ./padel/americano.json \
  --out ./padel/padel-americano.pdf
```

## Notes

- Americano scoring is individual: each player receives the points won by their team in each game.
- Each completed game must total exactly `points_per_game` across both teams. Draws are allowed when the two scores add up to the configured points per game.
- If a submitted score does not total the points-per-game value chosen at session creation, ask the user to enter the game score again.
- The standard Americano leaderboard is `points`: total individual points, point difference, wins, points percentage, fewer games, then name.
- Alternative leaderboard ranking supports `official`, `wins`, `points-pct`, and `wins-pct`.
- Official/wins-based leaderboard tie-breakers: wins, win percentage, total points, point difference, fewer games, then name. Use this only when the organizer explicitly wants wins prioritized over total points.
- Points percentage is `points_for / (games * points_per_game)`. Wins percentage is `wins / games`.
- Leaderboard columns put the primary ranking statistic immediately after the player name: `Pts` for points, `Wins` for official/wins, `Pts%` for points-pct, and `Win%` for wins-pct.
- Tied players share competition ranks, for example `1, 2, 2, 4`.
- Points leaderboard tie-breakers: points, point difference, wins, points percentage, fewer games, then name.
- Wins leaderboard tie-breakers: wins, wins percentage, points, point difference, fewer games, then name.
- Percentage leaderboard tie-breakers prioritize the requested percentage, then stronger raw results and more completed games before name.
- Completed games are never regenerated during a switch. Only future unscored rounds are adjusted.
- Mid-session join, leave, pause, resume, add, and remove commands are operational extensions for real event management. They are not part of the core Americano format.
- Removing a player is allowed only from a round that has no completed scores onward. Earlier scored rounds remain in the leaderboard.
- Open-ended sessions generate one round at a time using the latest active roster. Joining, leaving, pausing, and resuming affect the next generated round, not already generated rounds.
- In open-ended sessions, `next-round` normally requires the current round to be fully scored. Use `--force` only when intentionally running multiple unscored rounds in parallel.
- If player count exceeds court capacity or is not divisible by 4, the CLI warns about byes or idle courts. Byes roll by roster order from the first generated/regenerated round.
- A new mid-session player enters the rolling bye order normally; they are not forced to play every future round to match older players' game count.
