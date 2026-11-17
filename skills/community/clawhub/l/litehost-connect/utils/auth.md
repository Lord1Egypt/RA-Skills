# Authentication

Authenticated requests to `https://connect.litehost.io` send:

```
Authorization: Bearer lh_live_xxx
```

## Find the key (every session)

1. `LITEHOST_API_KEY` environment variable, if set
2. `~/.config/litehost/credentials.json` (`{"apiKey": "...", "email": "..."}`)

`scripts/litehost.sh` does this lookup on every call. Check the key once per session:

```bash
scripts/litehost.sh session
```

```json
{"status":"success","data":{"email":"you@example.com","plan":"pro","apiKey":{"expiresAt":"2026-12-27T12:00:00.000Z","renewsWhileInUse":true}}}
```

Equivalent curl: `curl https://connect.litehost.io/v1/auth/session -H "Authorization: Bearer <key>"`.

If there is no key, do **not** sign in by default. Publishing needs no key
(`actions/temp-project.md`). Sign in (`actions/otp-sign-in.md`) only when the user wants you to
manage their projects.

## Making calls

With the helper (preferred — works even though each command runs in a new shell):

```bash
scripts/litehost.sh api GET /v1/user
scripts/litehost.sh api POST /v1/projects -F "title=My Site" -F "files=@index.html"
```

The curl examples in the action files use `$LITEHOST_API_KEY`. Without the helper, make sure the
key is available in **that same command**, e.g.:

```bash
curl https://connect.litehost.io/v1/user \
  -H "Authorization: Bearer $(sed -n 's/.*"apiKey"[^"]*"\([^"]*\)".*/\1/p' ~/.config/litehost/credentials.json)"
```

## Key types

| Source | Lifetime | In dashboard |
|---|---|---|
| Dashboard → Integrations | Never expires; revocable | Yes |
| Sign-in (`/v1/auth/otp/verify`) | Renews while in use; expires after 90 days unused | No |

## On 401

Read the `code`:

| Code | Do this |
|---|---|
| `API_KEY_MISSING` | You did not send the key. Send the saved key. Do not sign in. |
| `API_KEY_INVALID` | Revoked or wrong key. `scripts/litehost.sh forget`, then sign in once (or ask for a dashboard key). |
| `API_KEY_EXPIRED` | Unused for 90 days. `scripts/litehost.sh forget`, then sign in once. |

Never retry the same request with the same key after `API_KEY_INVALID` or `API_KEY_EXPIRED`.
Never hardcode a key in project files or commit it.

## No-auth endpoints

`GET /health`, `GET /v1`, `GET /llms.txt`, `GET /openapi.json`, `POST /v1/auth/otp/request`,
`POST /v1/auth/otp/verify`, `POST /v1/projects/temp`.
