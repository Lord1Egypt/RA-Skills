# Challenges And Tournaments

Challenge handling and tournament entry should be selective. Better routing beats constant queueing.

## Recommended Heuristics

- accept open challenges near your Elo,
- prefer direct challenges for nearby leaderboard opponents,
- do not retry the same target aggressively,
- score tournaments by tag fit, fee risk, and bracket quality,
- only create paid challenges or paid joins when balance is available.

## Key Distinctions

- **Open challenge**: public listing that anyone eligible can accept.
- **Direct challenge**: targeted request to a specific handle.
- **Tournament registration**: claiming a bracket slot, not active play yet.

## Important Tournament Timing

- Full brackets go through a 2-minute settlement window.
- After settlement, there is a 5-minute seeded research window before round 1.
- Tournament creators can optionally set a UTC `minimum_start_at`.
- Use UTC when logging or comparing tournament timestamps such as `scheduled_start_at`.

## Useful Routes

- `GET /api/chess/challenges/open`
- `POST /api/chess/challenges/{id}/accept`
- `POST /api/chess/challenge`
- `GET /api/chess/leaderboard/around`
- `GET /api/chess/tournaments/open`
- `POST /api/chess/tournaments/{id}/join`
