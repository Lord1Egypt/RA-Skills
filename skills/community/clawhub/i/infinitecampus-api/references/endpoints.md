# Infinite Campus endpoints for curl

Assumes the Login block from `../SKILL.md` has already run (`$JAR`, `$XSRF`,
`$IC_BASE_URL` set) and the `ic_get` helper is defined:

```sh
ic_get() { curl -sS -b "$JAR" -H "X-XSRF-TOKEN: $XSRF" -H 'Accept: application/json' "$IC_BASE_URL$1"; }
```

All paths are transcribed from `infinitecampus-mcp`'s `src/tools/*.ts` and
`docs/endpoints.md` — the same requests the `ic_*` MCP tools make. `$PID` =
a student's `personID` from the resolve-first step.

Some IC/prism responses serialize a 1-item collection as a bare object
instead of a 1-element array — pipe through `jq 'if type=="array" then . else [.] end'`
if a recipe below assumes an array and you get an object back.

---

## Students (resolve-first — always start here)

```sh
ic_get '/campus/api/portal/students' \
  | jq '.[] | {personID, firstName, lastName, enrollments}'
```

Each `enrollments[]` entry carries `enrollmentID`, `calendarID`,
`structureID`, `schoolName`, `endDate` — needed by several endpoints below.

## Schedule

```sh
ic_get "/campus/resources/portal/roster?personID=$PID" | jq .
```

(Only `personID` is honored server-side — there is no date/term filter, so
the MCP tool takes none.)

## Assignments

```sh
# all assignments (full term history, ~hundreds of rows)
ic_get "/campus/api/portal/assignment/listView?personID=$PID" | jq .

# scoped to one course (sectionID from the schedule call above)
ic_get "/campus/api/portal/assignment/listView?personID=$PID&sectionID=$SECTION_ID" | jq .

# client-side filters (server ignores date/missing params entirely):
ic_get "/campus/api/portal/assignment/listView?personID=$PID" \
  | jq --arg since 2026-01-01 '[.[] | select(.dueDate >= $since)]'
```

## Recent (recently-graded) assignments

Server-side filtered by `modifiedDate` (defaults to 14 days ago in the MCP;
reproduce with `date -u -v-14d '+%Y-%m-%dT00:00:00'` on macOS):

```sh
SINCE=$(date -u -v-14d '+%Y-%m-%dT00:00:00')
ic_get "/campus/api/portal/assignment/recentlyScored?modifiedDate=$SINCE&personID=$PID" | jq .
```

## Grades

```sh
ic_get "/campus/resources/portal/grades?personID=$PID" | jq .
# scoped to one term:
ic_get "/campus/resources/portal/grades?personID=$PID&termID=$TERM_ID" | jq .
```

## Attendance (per-course summary, loop over each enrollment)

```sh
ic_get "/campus/resources/portal/attendance/$ENROLLMENT_ID?courseSummary=true&personID=$PID" \
  | jq '.terms[]?.courses[]? | {absentList, tardyList, presentList, earlyReleaseList}'
```

Feature-gated: check `displayOptions.attendance` first (see Feature flags,
below) — a 404 here on a district with attendance disabled is expected, not
a bug.

## Attendance events (individual absences/tardies, loop over each enrollment)

```sh
ic_get "/campus/resources/portal/attendance/events?enrollmentID=$ENROLLMENT_ID&personID=$PID" \
  | jq '.events[]? | {date: .localDate, code, description, excuse, comments}'

# excused-only, since a date (client-side filter):
ic_get "/campus/resources/portal/attendance/events?enrollmentID=$ENROLLMENT_ID&personID=$PID" \
  | jq --arg since 2026-01-01 '[.events[]? | select((.localDate[0:10] >= $since) and (.excuse == "E"))]'
```

## School days / calendar (loop over each enrollment)

Two calls per enrollment, then join term windows to days client-side:

```sh
ic_get "/campus/resources/term?structureID=$STRUCTURE_ID" | jq .          # term boundaries
ic_get "/campus/resources/calendar/instructionalDay?calendarID=$CALENDAR_ID" | jq .  # day list
# some districts 500 on instructionalDay (#253) — same days via calendar/day:
ic_get "/campus/resources/calendar/day?calendarID=$CALENDAR_ID" | jq '[.[] | select(.isInstructionalDay)]'
# day labels (holidays, workdays, early release) — the day lists no longer carry comments:
ic_get "/campus/resources/portal/dayEvent/byEnrollment?personID=$PID" | jq '[.[].events[] | {date, name, instruction}]'
# Campus version, no session needed (footer of the parent login page):
curl -s "$IC_BASE_URL/campus/portal/parents/$IC_DISTRICT.jsp" | grep -o 'Version:Campus-[0-9.]*'

# days within term N's [startDate,endDate]:
jq --slurpfile terms terms.json --arg t "$TERM_ID" \
  '[.[] | select(.date >= $terms[0][0].startDate and .date <= $terms[0][0].endDate)]' days.json
```

## Assessments (standardized tests, loop over each enrollment)

```sh
ic_get "/campus/resources/prism/portal/assessments?personID=$PID&calendarID=$CALENDAR_ID" \
  | jq '{stateTests, nationalTests, districtTests}'
```

Feature-gated on `displayOptions.assessment`; test-item shape varies by
district/test type — pass through unchanged, don't assume field names
beyond `stateTests`/`nationalTests`/`districtTests`.

## Behavior *(path unconfirmed — never verified live against a district with the module on)*

```sh
ic_get "/campus/resources/portal/behavior?personID=$PID" | jq .
# with a date range:
ic_get "/campus/resources/portal/behavior?personID=$PID&startDate=2026-01-01&endDate=2026-06-01" | jq .
```

Feature-gated on `displayOptions.behavior` — a 404 is the expected result
on most districts (few enable this module for parent portal).

## Food service *(path unconfirmed — same caveat as behavior)*

```sh
ic_get "/campus/resources/portal/foodService?personID=$PID" | jq .
ic_get "/campus/resources/portal/foodService?personID=$PID&startDate=2026-01-01&endDate=2026-06-01" | jq .
```

Feature-gated on `displayOptions.foodService`.

## Documents + download

```sh
ic_get "/campus/resources/portal/report/all?personID=$PID" \
  | jq '.[] | {name, type, url, moduleLabel, endYear}'

# download (url may be relative /campus/... or an absolute URL — handle both):
DOC_URL='/campus/resources/portal/report/...'   # from the .url field above
curl -sS -b "$JAR" -H "X-XSRF-TOKEN: $XSRF" -o report-card.pdf \
  "$( [[ "$DOC_URL" == http* ]] && echo "$DOC_URL" || echo "$IC_BASE_URL$DOC_URL" )"
```

Feature-gated on `displayOptions.documents`.

## Teachers + counselors

```sh
ic_get "/campus/resources/portal/section/contacts?personID=$PID" | jq .
ic_get "/campus/resources/portal/studentCounselor/byUser?personID=$PID" | jq .
```

Either endpoint 404ing is treated as "no results" (not FeatureDisabled) by
the MCP — do the same.

## Messages (three independent sources — combine client-side)

```sh
# 1. prism notifications (assignment/grade/attendance alerts)
ic_get '/campus/prism?x=notifications.Notification-retrieve&limitCount=20' \
  | jq '.data.NotificationList.Notification'

# 2. Messenger 2.0 inbox (teacher messages, district announcements)
ic_get '/campus/api/portal/process-message' | jq .

# 3. portal userNotice announcements
ic_get '/campus/resources/portal/userNotice' | jq .
```

Each inbox item's `url` field feeds `ic_get_message` below (normalize a bare
or `portal/...`-relative URL to `/campus/portal/...` first).

## Get one message body (HTML → text)

```sh
# normalize: bare "portal/..." → "/campus/portal/..."; already-absolute /campus/... stays as-is
MSG_PATH='/campus/portal/messageView.xsl?x=messenger.MessengerEngine-getMessageRecipientView&messageID=...&messageRecipientID=...'
curl -sS -b "$JAR" -H "X-XSRF-TOKEN: $XSRF" -H 'Accept: text/html' "$IC_BASE_URL$MSG_PATH"
# then strip tags/entities yourself, or eyeball the rendered HTML — this is
# an HTML fragment, not JSON, so `jq` doesn't apply.
```

Fetching a message body *may* mark it read on some district configs
(unconfirmed either way).

## Fees (two endpoints in parallel; either can 404 independently)

```sh
ic_get "/campus/api/portal/fees/feeAssignments?personID=$PID" | jq .
ic_get "/campus/api/portal/fees/feeTransactionDetail/totalSurplus/-1?personID=$PID" | jq .
```

Both 404 → module is off for this district. One 404 → report the other
side plus a note that the failing endpoint may be disabled.

## Feature flags (displayOptions — check before assuming a 404 is a bug)

```sh
ic_get "/campus/api/portal/displayOptions/$STRUCTURE_ID?personID=$PID" \
  | jq '{attendance, behavior, assessment, documents, foodService, grades, schedule}'
```

`false` = district has that module turned off for this enrollment; `true`
or absent = available. ~90 flags total; the MCP caches this per
`(district, structureID)` for the session lifetime since it rarely changes
mid-session — worth doing the same if you're calling it more than once.

---

## Not covered here (out of scope for this skill)

- **CUPS linked-district discovery/switching** — a parent with kids at 2+
  IC-hosted districts under shared SSO. Multi-step: fetch
  `cups/linkedAccounts`, `userAccountSwitch/originalDistrict`,
  `districts/current`, then per linked account a `cups/loginToken` POST
  followed by a second `verify.jsp`-style POST at the *linked* district's
  own host with the CUPS token. Fully discoverable in `src/client.ts`
  (`discoverLinkedDistricts`) but a lot of shell for a one-shot skill —
  just re-run the Login block against the linked district's own
  `IC_BASE_URL`/`IC_DISTRICT` instead.
