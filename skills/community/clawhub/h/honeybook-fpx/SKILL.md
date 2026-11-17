---
name: honeybook-fpx
description: >-
  Read HoneyBook client-portal data (contracts, invoices, proposals, payment
  methods, workspace status) from a shell with the fpx CLI (@fetchproxy/cli)
  instead of running the honeybook-mcp server — capture a vendor session once
  via the signed-in browser tab, then curl api.honeybook.com directly. Use
  when you want HoneyBook data without the MCP, in a script, or on a machine
  where the MCP isn't installed.
---

# HoneyBook via fpx + curl (no MCP)

HoneyBook has **no server-side login** a script can drive — a client never
gets a password, only a magic-link email per vendor. The credential is
whatever the signed-in `*.hbportal.co` portal tab already holds: a bearer
token + user id in `localStorage["HONEYBOOK_REACT_CURR_USER"]`. (HoneyBook
used to keep these in the AngularJS `localStorage["jStorage"]` blob as
`HB_AUTH_TOKEN`/`HB_AUTH_USER_ID`; that blob is now down to
`HB_TRUSTED_DEVICE`, `SESSION_COMPANY_ID` and routing state.)
There's no bot wall on the API itself once you have those — `honeybook-mcp`'s
own `client.ts` proves plain Node `fetch` works fine against
`api.honeybook.com`. So this skill is **hybrid**: `fpx` captures the session
**once** (per vendor), then plain `curl` does every read from then on.

This mirrors `src/auth.ts` (`captureSessionViaFetchproxy`) and `src/client.ts`
(`HoneyBookClient.request`) in `honeybook-mcp` — same headers, same base URL,
same retry rules.

## Multi-domain scope

Two apexes are declared on one profile:
- `hbportal.co` — the vendor's branded portal (e.g. `acme.hbportal.co`),
  where the stored session lives.
- `honeybook.com` — the main app, where the same session is also valid.

## One-time setup

```sh
npm install -g @fetchproxy/cli   # provides `fpx`
fpx profile add honeybook --domain honeybook.com --domain hbportal.co
fpx profile declare honeybook \
  --local-storage HONEYBOOK_REACT_CURR_USER \
  --local-storage jStorage
fpx pair -p honeybook            # prints a pair code → approve in ContextMint Bridge
```

Requirements: the **ContextMint Bridge** browser extension installed
([releases](https://github.com/nullnet-app/contextmint-bridge/releases):
Chrome loads the chrome zip unpacked; Safari isn't available yet, so use
Chrome for now), its Chrome **Site access** allowing both `honeybook.com` and
`hbportal.co`, and a vendor magic-link URL already open (signed in) in that
browser. Pairing persists — after the first approval every later `fpx` call
reuses it.

ContextMint Bridge is the fetchproxy extension renamed, same maintainer (see [fetchproxy#extension](https://github.com/chrischall/fetchproxy#extension)); source at [nullnet-app/contextmint-bridge](https://github.com/nullnet-app/contextmint-bridge) — build it yourself or verify a release zip with `shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`.

## Capture a vendor session (once per vendor, and again when it expires)

1. Click the vendor's HoneyBook magic-link email in the browser with
   ContextMint Bridge installed. This signs you into `<vendor>.hbportal.co`.
2. **While that tab is open**, run:

```sh
fpx session -p honeybook --storage-domain hbportal.co > /tmp/hb-session.json
```

The tab only has to be **open and signed in**. Nothing is sniffed off a live
request, so it does not matter whether the page has gone idle.

3. Extract the fields `client.ts` needs (each localStorage value is one raw
   JSON string — parse it with `fromjson`):

```sh
AUTH_TOKEN=$(jq -r '.localStorage.HONEYBOOK_REACT_CURR_USER | fromjson | .authentication_token' /tmp/hb-session.json)
USER_ID=$(jq -r '.localStorage.HONEYBOOK_REACT_CURR_USER | fromjson | ._id' /tmp/hb-session.json)
# Optional — the API returns 200 without it. The React blob and jStorage hold
# DIFFERENT values; either is accepted. `// empty` keeps an absent field from
# becoming the literal string "null".
TRUSTED_DEVICE=$(jq -r '.localStorage.jStorage | fromjson | .HB_TRUSTED_DEVICE // empty' /tmp/hb-session.json)
PORTAL_ORIGIN='https://<vendor>.hbportal.co'   # the magic-link URL's origin
```

If `AUTH_TOKEN` or `USER_ID` comes back empty/`null`, the capture didn't see
what it needed — re-open the magic link and re-run step 2.

With more than one vendor tab open at once, disambiguate with
`--storage-subdomain <vendor>` (e.g. `--storage-subdomain acme`).

4. Get the current API version (`client.ts`'s `fetchApiVersion` parses this
   same endpoint):

```sh
API_VERSION=$(curl -s 'https://api.honeybook.com/api/gon?callback=parseGon' \
  | grep -oE '"api_version":[[:space:]]*[0-9]+' | grep -oE '[0-9]+$')
```

## Core call pattern

Every real request carries the same headers
(`client.ts`'s `HoneyBookClient.request`). Only `hb-api-auth-token`,
`hb-api-user-id` and a current `hb-api-client-version` are load-bearing —
`hb-trusted-device` is optional and `hb-api-fingerprint` is no longer
required at all:

```sh
curl -s "https://api.honeybook.com/api/v2/users/$USER_ID/workspace_files" \
  -H 'accept: application/json, text/plain, */*' \
  -H "hb-api-auth-token: $AUTH_TOKEN" \
  -H "hb-api-user-id: $USER_ID" \
  ${TRUSTED_DEVICE:+-H "hb-trusted-device: $TRUSTED_DEVICE"} \
  -H "hb-api-client-version: $API_VERSION" \
  -H "hb-api-duplicate-calls-prevention-uuid: $(uuidgen)" \
  -H 'hb-admin-login: false' \
  | jq '.data'
```

`hb-api-duplicate-calls-prevention-uuid` must be a **fresh random UUID on
every request** — the MCP mints one with `crypto.randomUUID()` per call, not
once per session. Reusing a value risks HoneyBook treating a legitimate
repeat as a duplicate.

Ready-to-run commands for all four read endpoints are in
`references/requests.md`.

## Other reads the portal makes (same headers)

```sh
# Projects ("events") and the workspace id each one carries
curl -s "https://api.honeybook.com/api/v2/client/events" "${HB_HEADERS[@]}"
curl -s "https://api.honeybook.com/api/v2/events/$EVENT_ID/details" "${HB_HEADERS[@]}"
# The feed: messages (feed_message / workspace_email / workspace_file_email) and activity
curl -s "https://api.honeybook.com/api/v2/workspaces/$WS_ID/feed" "${HB_HEADERS[@]}" \
  | jq '.feed.feed_items[] | select(.type|test("email|message")) | {id:._id, subject:.data.subject, from:.sender_id, sent:.data.sent_on}'
# Tasks (curr_date MUST be MM/DD/YYYY), notes, loose files, payment schedule
curl -s "https://api.honeybook.com/api/v2/tasks/workspaces/$WS_ID?page=1&perPage=30&sort_by=due_date&sort_desc=false&curr_date=09%2F02%2F2026" "${HB_HEADERS[@]}"
curl -s "https://api.honeybook.com/api/v2/notes/workspace/$WS_ID" "${HB_HEADERS[@]}"
curl -s "https://api.honeybook.com/api/v2/workspaces/$WS_ID/attachments" "${HB_HEADERS[@]}"
curl -s "https://api.honeybook.com/api/v2/workspaces/$WS_ID/payments" "${HB_HEADERS[@]}"
```

Sending a message is a two-step "client pending task", not a POST of the
message: `POST /api/v2/client_pending_task` with
`{"task_type":"send_workspace_message","task_data":{"ws_id":…,"subject":…,"html_body":…,"force":false,"general_files":[],"image_files":[],"flow_attachments":[]}}`
returns `{task_id}`; poll `GET /api/v2/client_pending_tasks?task_ids[]=<id>`
until `pending_task_state_cd` is 2 (Finished) or 3 (Aborted). It emails the
vendor for real — prefer the MCP's `send_message`, which previews first.

## The rules that matter

- **401, or 404 with an `HBUnauthorizedError` body → session expired.** A
  revoked token does not reliably come back as 401, so check the body type
  before concluding a resource is missing. Re-run the capture (magic link tab must still
  be open and signed in).
- **429 → rate limited.** `client.ts` waits 2s and retries once; do the same
  before giving up.
- **Body contains `"HBWrongAPIVersionError"` → stale `hb-api-client-version`.**
  The error body itself carries the correct value at
  `.error_data.server_api_version` — read that (or re-run the `/api/gon`
  fetch above) and retry the SAME request with the fresh version.
- **`sign_contract` / `pay_invoice` are not real API calls.** `honeybook-mcp`
  can't replay HoneyBook's browser-side signing/SCA flow, so those tools just
  return a deep link — `$PORTAL_ORIGIN/app/workspace_file/<file_id>/agreement`
  (sign) or `/invoice` (pay) — for the user to open themselves. There's no
  POST body to transcribe for either; don't invent one.

## Output / exit-code contract

- `fpx session`/`fpx pair`/`fpx health` are bridge round-trips: exit `0` on a
  successful bridge read regardless of upstream status, `1` on a usage error
  (bad flag, undeclared scope), `2` if the bridge/extension is unreachable or
  pairing is still pending. There's no bot-wall (`3`)/upstream-HTTP (`4`)
  exit code on these — HoneyBook's own API isn't bridge-walled.
- The actual reads go through plain `curl` afterward — check the HTTP status
  and the `HBWrongAPIVersionError` body text yourself, as above.

## Notes

- Session data (`AUTH_TOKEN`, `TRUSTED_DEVICE`) is opaque and
  long-lived server-side (no client-visible JWT expiry) — keep it in shell
  variables, not a world-readable file, if you must persist it at all.
- This project is developed and maintained by AI (Claude).
