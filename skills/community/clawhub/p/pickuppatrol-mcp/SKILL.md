---
name: pickuppatrol-api
description: "Read and change your children's school dismissal plans on PickUp Patrol (app.pickuppatrol.net) from a shell with curl — students, weekly defaults, day-by-day changes, school cutoff times."
---

# PickUp Patrol from a shell

`app.pickuppatrol.net` is a ServiceStack JSON API behind an Ionic/Vue SPA. It is
reachable **server-side with plain `curl`** — no bot wall, no captcha, no
browser bridge. Use this when you want PickUp Patrol data in a script or on a
machine without the `pickuppatrol-mcp` server.

Full captured shapes: `references/api.md`.

## Sign in once per shell

```bash
export PUP_USER='you@example.com'
read -rs PUP_PASS && export PUP_PASS      # never put the password in a command line
export PUP=https://app.pickuppatrol.net/api/json/reply

pup_login() {
  local jar; jar=$(mktemp -t pupjar)
  curl -sS -c "$jar" -X POST "$PUP/Authenticate" \
    -H 'Content-Type: application/json' \
    -d "$(jq -nc --arg u "$PUP_USER" --arg p "$PUP_PASS" \
          '{provider:"credentials",UserName:$u,Password:$p,RememberMe:true}')" \
    -o /tmp/pup_auth.json -w '%{http_code}' >/tmp/pup_code
  [ "$(cat /tmp/pup_code)" = 200 ] || { jq -r '.ResponseStatus.Message' /tmp/pup_auth.json >&2; return 1; }
  export PUP_JAR="$jar"
  # This deployment returns cookies only — BearerToken comes back null. The
  # JWT path exists server-side, so keep a token if one ever appears.
  PUP_TOKEN=$(jq -r '.BearerToken // empty' /tmp/pup_auth.json); export PUP_TOKEN
}

# Every call goes through this: it sends the session cookies, and the bearer
# token as well when the deployment issued one.
pup() {
  local method=$1 dto=$2; shift 2
  local -a auth=(-b "$PUP_JAR")
  [ -n "$PUP_TOKEN" ] && auth+=(-H "Authorization: Bearer $PUP_TOKEN")
  curl -sS -X "$method" "$PUP/$dto" -H 'Content-Type: application/json' "${auth[@]}" "$@"
}
```

**Never re-run a rejected login.** PickUp Patrol answers bad credentials with
`ResponseStatus.ErrorCode` starting `LOGIN-ERROR`, counts the attempt against
the account, and a lockout clears only through their support desk. One failure
= stop and fix the credentials.

## Reads

```bash
pup GET GetSession | jq '{name:.DisplayName, email:.Email, kids:[.Children[].StudentId]}'
pup GET GetChildren | jq -r '.[] | "\(.StudentId)  \(.FirstName) — \(.SchoolName)"'

# Weekly default plan for one student. DayId is 1-based, SUNDAY = 1.
pup GET GetChildren | jq '.[] | select(.StudentId==1050046) | .DefaultPlans
  | sort_by(.DayId) | map({day:.WeekDayName, option:.TransportationName, note:.Note})'

# The dismissal options a school offers, with the rules each imposes.
pup GET "GetTransportations?SchoolId=1703" | jq -r '.[] | select(.IsActive)
  | "\(.TransportationId)\t\(.Name)\tnote=\(.IsNoteRequired)\tcar=\(.UseCarNumbers)\tearly=\(.IsEarlyDismissal)"'

# GetPlanEdit returns the date's OVERRIDE, not the effective plan: a date with
# no specific plan reads back null even when a weekday default exists.
pup GET "GetPlanEdit?PlanDate=2026-08-17&StudentId=1050046" | jq '{TransportationName,Note,IsLocked}'
pup GET "GetInvalidPlanDates?SchoolId=1703" | jq 'length'   # non-school days
```

## Writes

Writes change how a child actually leaves school. Read
`GetTransportations` first and obey the option's rules, or the request is
rejected (or worse, silently ignored):

- `IsNoteRequired` → `Note` must be non-empty
- `UseCarNumbers` → send `CarNumber`; otherwise omit the key
- `IsEarlyDismissal` → send `EarlyDismissalTime` as `HH:MM:SS`; otherwise omit it
- `IsLimited` → only usable if the id is in the student's `LimitedIds`

**Change specific dates** — `Plans` is an array, one entry per date:

```bash
pup PUT UpdatePlans -d '{"Plans":[{
  "StudentId":1050046,"SchoolId":1703,"PlanDate":"2026-08-17",
  "TransportationId":41246,"TransportationName":"PickUp","Note":"Chris Hall"}]}'
```

**Clear a date back to the weekly default** — a null transportation:

```bash
pup PUT UpdatePlans -d '{"Plans":[{
  "StudentId":1050046,"SchoolId":1703,"PlanDate":"2026-08-17",
  "TransportationId":null,"TransportationName":"Default plan","Note":null}]}'
```

**Change the weekly defaults** — there is no default-plans endpoint. Read the
whole student, edit `DefaultPlans`, PUT the whole record back
(`references/api.md` has the read-modify-write recipe).

### Always re-read to verify

A 2xx is not proof. The school silently ignores a change past its cutoff time.

```bash
pup GET "GetPlanEdit?PlanDate=2026-08-17&StudentId=1050046" | jq '.TransportationId'
```

Compare `TransportationId` **and `Note`** — never `ModifiedDate`, which advances
on its own and would make every write look successful. The note matters: every
option seen so far is `IsNoteRequired`, so a note-only edit is ordinary, and an
id-only comparison would pass without observing it. After *clearing* a date,
expect `null` — not the weekday default.

## In context groups

When `pickuppatrol-mcp` is hosted on mcp-host, its tools join the **school**
group (`_meta.mint` on every tool except `pup_healthcheck`).

- **Canonical read:** `pup_list_plans` answers *what's on* — how each child
  leaves school on each day of a range (`when` = `start_date`/`end_date`).
  `view: "brief"` answers one line per child per day,
  `<child>: <option> — <YYYY-MM-DD> — <default|changed|blocked|scheduled>`,
  inside the untrusted-data envelope (option names are school-authored; plan
  notes are left off), with `-- none` for an empty range and
  `-- N of M shown` when capped. A title starting with `-- ` or `\` is
  escaped with one leading `\` so it never reads as a note.
- **No subject:** the read already covers every student on the account in one
  call, so it names no subject argument.
- Nothing here answers *what's new* or *what's due*; the other reads are
  `lookup` hints and the three writes are `change` hints, still behind their
  confirmation.
- A compound ask looks like "what's on at school tomorrow — and how is
  everyone getting home?": the group calls `pup_list_plans` for that day
  beside the other school members.
- Not browser-bridged: the server signs in server-side, so the group never
  answers "needs your browser open" for it.
