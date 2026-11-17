# Hybrid Training Plan API — what an API key can reach

Base URL: `https://api.hybridtrainingplan.app`
Auth: `Authorization: Bearer htp_<64 hex>`

An `htp_` key reaches only the routes below. Anything else answers
`403 {"error":"Not available to API keys — use the app"}`. A revoked key, or one
belonging to a deleted account, answers `401`.

| Method | Path |
|---|---|
| GET | `/api/watch/sessions` |
| GET | `/api/users/me`, `/api/users/me/dashboard` |
| GET | `/api/plans`, `/api/plans/:planId` |
| PATCH | `/api/plans/:planId/days/:date` |
| GET, PUT | `/api/session-logs` |
| GET, PUT | `/api/exercise-maxes` |

---

## GET /api/watch/sessions

The coming days' sessions, already worked out (suggested weights, run steps,
circuit stations). Rest days and skipped days are left out.

```json
{
  "version": 3,
  "state": "ok",
  "distanceUnit": "km",
  "sessions": [
    {
      "kind": "strength",
      "planId": "uuid", "sessionId": "string", "dayDate": "2026-10-11",
      "title": "Lower Strength", "sessionType": "strength",
      "description": "…", "durationMinutes": 55, "done": false,
      "strength": {
        "exercises": [{ "name": "Back Squat", "key": "back_squat", "kind": "reps", "label": "5 reps", "loadGuidance": "@RPE8" }],
        "sets": [{ "exerciseIdx": 0, "setIndex": 0, "warmupPercent": null, "target": 5, "weightKg": 100, "restAfter": 120, "isBenchmark": false }]
      }
    }
  ]
}
```

`kind` is `strength`, `run` (has `runSteps`), `circuit` (has `workout`, `sequence`)
or `simple`. `state` is `ok`, `no_plan`, `building`, `no_access`, `paused` or `ended`.
`sets` with a `warmupPercent` are warm-ups.

## GET /api/users/me/dashboard

Large: includes the whole plan document. The helper trims it to
`user.currentPlanId`, `plans[]`, `todaySession` (`{ planId, planTitle, day, distanceUnit }` or null), `distanceUnit`, `totalCompletedSessions`.

## GET /api/plans/:planId

`{ plan: {...}, content: { weeks: [{ weekNumber, days: [{ date, status, isRestDay, sessions: [...] }] }] }, version }`.
Day `status` is `planned`, `completed`, `skipped` or `moved`.

## PATCH /api/plans/:planId/days/:date

Body `{ "status": "completed" | "skipped" | "planned" }`.

## GET /api/session-logs

`?planId=&dayDate=` → `{ logs: [...] }` for the day.
`?planId=&sessionId=` → `{ log: {...} | null, prefill: {...} }` for one session.

## PUT /api/session-logs

Upsert one session's log, keyed on `planId` + `sessionId`. Saving any content
completes the day, and a set that implies a higher 1RM raises the stored max.

Required: `planId` (uuid), `sessionId`, `dayDate`, `sessionType`. Optional:

| Field | Type |
|---|---|
| `strengthSets` | `[{ exerciseName, exerciseKey, setIndex, reps?, weightKg?, durationSeconds?, distanceMetres? }]` |
| `runDistanceKm`, `runDurationSeconds` | number, integer |
| `rowDistanceM`, `rowDurationSeconds` | number, integer |
| `roundsCompleted` | integer |
| `warmupDone`, `cooldownDone` | boolean |
| `notes` | string |

A `0` in a numeric field is stored as "not recorded". Response `{ log: {...} }`.

## GET /api/exercise-maxes

`{ maxes: [{ exerciseKey, displayName, oneRepMaxKg, source, confidence, updatedAt, ... }] }`

## PUT /api/exercise-maxes

Body `{ "exerciseName": "Back Squat", "oneRepMaxKg": 140 }` (kg, 0 < x ≤ 1000).
A hand-set max is stored with `source: "user"`; the next benchmark set replaces it.
