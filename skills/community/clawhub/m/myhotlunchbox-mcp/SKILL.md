---
name: myhotlunchbox
description: Read and manage a My Hot Lunchbox school-lunch account from a shell with curl — sign in, list students, read the lunch calendar and cart, check orders, deliveries and payments. Use when you want My Hot Lunchbox data without running the MCP server, in a script, or on a machine where the MCP is not installed.
---

# My Hot Lunchbox from the shell

`ordernow.myhotlunchbox.com` exposes a plain JSON API behind an OAuth2 password
grant. It is reachable server-side — no browser, no extension, no bridge. Two
`curl` calls get you data: one to sign in, one per read.

## Sign in once per shell

Credentials come from the environment; never paste them into a command line
(that puts them in shell history).

```sh
export MHLB_USER='you@example.com'
export MHLB_PASS='…'          # e.g. read -rs MHLB_PASS
export MHLB=https://ordernow.myhotlunchbox.com

mhlb_login() {
  local resp
  resp=$(curl -sS -X POST "$MHLB/api/auth/login" \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -H 'Accept: application/json' \
    --data-urlencode 'grant_type=password' \
    --data-urlencode "username=$MHLB_USER" \
    --data-urlencode "password=$MHLB_PASS" \
    --data-urlencode 'scope=openid offline_access email profile roles') || return 1
  MHLB_TOKEN=$(printf '%s' "$resp" | jq -r '.access_token // empty')
  if [ -z "$MHLB_TOKEN" ]; then
    printf '%s' "$resp" | jq -r '.error_description // .error // "login failed"' >&2
    return 1
  fi
  export MHLB_TOKEN
}

# Authenticated GET.  usage: mhlb_get /parent/childrenInfo [curl args…]
mhlb_get() {
  local endpoint=$1; shift   # NOT `path`: zsh ties $path to $PATH
  curl -sS "$MHLB/api$endpoint" -H "Authorization: Bearer $MHLB_TOKEN" -H 'Accept: application/json' "$@"
}

mhlb_login && mhlb_get /auth/userinfo | jq '{name, email, students_count, pending_orders_count, parent_credit_value}'
```

**A failed sign-in must not be retried.** The server is OpenIddict and counts
failed attempts; repeated failures can escalate to a CAPTCHA and remove
server-side sign-in for that account entirely. If `invalid_grant` comes back,
stop and check the credentials.

The token lasts about an hour. Re-run `mhlb_login` when a call starts returning
`401`.

## The three reads that answer most questions

```sh
# Who the students are — the id feeds everything else
mhlb_get /parent/childrenInfo | jq '.[] | {id, firstName, schoolName, gradeTeacher, isInactive}'

# The lunch calendar for a date range (POST, despite being a read).
# The fields are `start`/`end`. Using `startDate`/`endDate` returns 200 with an
# EMPTY events array — a silent wrong answer, not an error.
curl -sS -X POST "$MHLB/api/calendar/studentSchoolData" \
  -H "Authorization: Bearer $MHLB_TOKEN" -H 'Content-Type: application/json' \
  -d '{"start":"2026-09-01","end":"2026-09-30"}' | jq '.events[] | {studentId, id, start, className}'

# What is in the cart but not yet paid for
mhlb_get '/event/shoppingCart' | jq .
```

`references/endpoints.md` has the rest — deliveries, transactions,
subscriptions, gift cards, per-day order detail, and the printable reports.

## Ordering is read-modify-write

There is no "add item X" call. To place or change an order you fetch the model,
edit it, and post it back whole:

```sh
mhlb_get '/event/createOrder?eventId=123&studentId=456' > order.json
# edit quantities in order.json
curl -sS -X POST "$MHLB/api/event/createOrder" \
  -H "Authorization: Bearer $MHLB_TOKEN" -H 'Content-Type: application/json' \
  -d @order.json
```

Anything missing from the payload is **cleared**, not preserved.

**The write request bodies are unverified** — their paths and verbs were read
out of the site's own compiled client, but no write has been exercised against a
live account. Inspect what you are about to send, and re-read the resource
afterwards to confirm it landed. A `200` is not proof.

`/payment/checkout` charges a real card. Do not call it speculatively.

## Reading the errors

| Status | Meaning |
|---|---|
| `400` + `invalid_grant` | wrong username/password — **do not retry** |
| `401` on an API call | token expired; run `mhlb_login` again |
| `403` | the endpoint belongs to the school-admin or vendor role, not a parent |
| non-JSON `200` | either a `/parentReports/print*` PDF (expected — see references) or the session lapsed into an HTML page |
| `500` on `/parentReports/printOrders` | usually a caller mistake: empty `studentIds`, or no order matching that date and status |

## In context groups

The MCP's tools carry context-group hints (`_meta.mint`) placing them in the
**school** group, beside the other school MCPs a host groups together.

- **Canonical read:** `mhlb_get_calendar` answers *what's on* — the lunch
  calendar over `startDate`…`endDate`, one line per lunch with `view: "brief"`
  (`<student>: title — <date> — <status>`, e.g. `paid`, `scheduled`,
  `subscribed`, `past`, `school event`), inside the untrusted-data envelope
  since titles come from the school and its vendors. `-- none` means an empty
  range; a line whose own text starts with `-- ` or `\` is escaped with one
  leading `\`, so it never reads as a note.
- **Subject:** `student` — the students' first names, listed once at start
  and published as the argument's enum; a student id is accepted too.
- Nothing here answers *what's new* or *what's due*; every other tool is a
  lookup or a confirmed write.

A compound ask reads like "what's for lunch this week, and anything due at
school?" — the host asks this calendar for the week beside the other school
members' canonical reads. This MCP signs in server-side, so it needs no
browser open.

## Prefer the MCP when it is available

`myhotlunchbox-mcp` wraps all of this with typed tools and a confirmation step
for every mutation — a prompt where the client can show one (unless the server
sets `MCP_CONFIRM_ELICITATION=off`), otherwise a preview plus a single-use
`confirmToken`.
Use this skill when the MCP is not installed, or inside a script.
