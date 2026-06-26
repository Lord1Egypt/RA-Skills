# PolySports Monitoring Rules

## Required Inputs

- Market price, executable sell price when available, and live PnL
- ESPN scoreboard, gamecast, and boxscore
- Key game events such as injury exits, foul trouble, rotation changes, runs, endgame possessions, garbage time, and overtime risk
- Targeted web search when a material in-game development needs confirmation or context

## Decision Priority

1. Game state first: score, remaining time, lineup quality, star-player condition, foul trouble, rebounding, turnovers, paint or perimeter profile, pace, and matchup changes.
2. Key events second: injury, foul crisis, unusual rotation, momentum swing, timeout adjustment, and clutch-possession dynamics.
3. Market price and PnL are validation inputs, not the main decision.
4. Do not use ESPN win probability as a decision signal.
5. Only take profit or stop out after the basketball case for the thesis materially changes, then use price and liquidity to confirm execution.
6. In early fourth-quarter but still reversible games without a hard trigger, do not exit only because of low implied win probability or weak liquidity.

## Automation Pattern

- Use a two-stage monitoring setup:
  1. Create one `at` starter scheduled for game start plus 5 minutes.
  2. Let that starter create the real `every 5m` monitoring loop.
  3. Verify the starter will actually create the recurring loop.
- Reuse [../assets/templates/monitor-launcher.prompt.md](../assets/templates/monitor-launcher.prompt.md) as the launcher template when you need a ready-made first-stage prompt.
- Keep prompts focused on the task. Do not dump unrelated system implementation detail into the cron message.
- Each monitoring prompt must explicitly load `polysports-trading-agent` before making PolySports calls.
- Each PolySports request must send `X-PolySports-Api-Key`, `X-PolySports-Skill: polysports-trading-agent`, and `X-PolySports-Client`.

## Exit Discipline

- Do not hardcode fixed take-profit or stop-loss thresholds into the monitoring prompt. Let AI judge from the combined game and market context.
- When the position is reported as flat or exited, confirm once more with the positions endpoint before declaring the workflow finished.
- After a successful closing trade, remove the monitoring cron job itself.
- Every closed position must get a review, regardless of profit or loss.
- Every monitoring or review run must report a result instead of failing silently.
