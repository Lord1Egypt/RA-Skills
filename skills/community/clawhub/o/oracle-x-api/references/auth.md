# Authentication

Oracle-X authenticates with a Supabase JWT presented as a bearer token. The
backend verifies it against the project's Supabase instance on every request,
so there is no local session to establish and no login endpoint to call.

## Which endpoints need one

Everything scoped to a person, and nothing else:

| Endpoint | Why it is scoped |
|---|---|
| `POST /api/chat` | Runs on the caller's own LLM provider settings. |
| `POST /api/chat/jobs`, `GET /api/chat/jobs/{job_id}` | A chat job holds a question and its answer. |
| `GET/POST/DELETE /api/chat/history`, `/api/chat/sessions*` | The caller's conversations. |
| `GET/POST/DELETE /api/home/watchlist` | The caller's tracked symbols. |
| `POST /api/analysis/jobs/{timeframe}` | Generation spends the instance's provider budget. |

Prices, technicals, candles, news, analysis reports, macro, chains,
liquidations, funding, whale flow, ownership and the whole RAG surface are open
on a default instance. Do not attach a token to those calls; it buys nothing
and puts a credential on a request that did not need one.

## Getting a token

The token is the Supabase access token for a signed-in Oracle-X user. Three
ways to obtain one, in order of how much you should prefer them:

1. **Ask the user.** They can copy it from the terminal's own session — in the
   browser, the Supabase client stores it under a `sb-<project-ref>-auth-token`
   key in local storage, and `session.access_token` is the field.

2. **Sign in against Supabase directly**, if the user gives you credentials to
   use. This returns an access token valid for an hour:

   ```bash
   curl -sf -X POST \
     "$SUPABASE_URL/auth/v1/token?grant_type=password" \
     -H "apikey: $SUPABASE_ANON_KEY" \
     -H 'Content-Type: application/json' \
     -d '{"email":"...","password":"..."}' \
   | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])'
   ```

   Only do this when the user explicitly hands over credentials for it. Read
   them from the environment or from their message, never from a file you went
   looking for.

3. **Skip authentication.** If no token is available, answer the question from
   the open endpoints and tell the user which part needed a signed-in call.
   That is a better outcome than an unexplained 401.

## Using it

```bash
curl -sf -H "Authorization: Bearer $ORACLE_X_TOKEN" \
     "${ORACLE_X_URL:-http://localhost:8000}/api/home/watchlist"
```

Keep the token in `ORACLE_X_TOKEN` in the environment. It must not be written
into a script, a config file, a URL query string, or a log line — a Supabase
access token is a live credential for that user's account for as long as it
lives.

## Verifying one

The cheapest authenticated call is the watchlist:

```bash
curl -s -o /dev/null -w '%{http_code}\n' \
  -H "Authorization: Bearer $ORACLE_X_TOKEN" \
  "${ORACLE_X_URL:-http://localhost:8000}/api/home/watchlist"
```

- `200` — the token is good.
- `401` — missing, malformed or expired. Supabase access tokens are short-lived;
  an hour-old token is usually the explanation.
- `403` — the account is suspended. `get_current_user` refuses suspended
  accounts at the one choke point every authenticated route passes through.

## One asymmetry worth knowing

`GET /api/chat/jobs/{job_id}` answers `404` for a job belonging to another
user, not `403`. That is deliberate: confirming an id exists would already tell
a stranger something about a private conversation. So a 404 there means either
"no such job" or "not yours" — retrying will not distinguish them, and neither
should the answer you give the user.
