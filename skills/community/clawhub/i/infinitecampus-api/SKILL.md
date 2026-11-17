---
name: infinitecampus-api
description: >-
  Query an Infinite Campus (Campus Parent portal) district directly with curl
  instead of running the infinitecampus-mcp server — log in with a real
  username/password, capture the session cookie + XSRF token, and curl grades,
  attendance, assignments, schedule, messages, documents, and fees. Use when
  you want IC data without the MCP, in a script, or on a machine where the MCP
  isn't installed. Infinite Campus is per-district: the base URL and district
  app name are configurable, not hardcoded.
---

# Infinite Campus via curl (no MCP)

Infinite Campus's Campus Parent portal is a classic server-rendered site
(no public API, no bot wall). A plain form POST to `verify.jsp` logs a
parent in and hands back a session cookie — no browser bridge needed. This
is the same login `infinitecampus-mcp`'s `src/client.ts`/`src/auth.ts` do;
this skill reproduces it with `curl` + a cookie jar.

**Infinite Campus is per-district.** Every parent's portal lives at their
own district's host (`https://campus.<district>.k12.example.us` or similar)
under an `appName` path segment. There is no shared IC endpoint — carry the
base URL and district from the same config the MCP uses:

```sh
: "${IC_BASE_URL:?set to your district's portal URL, e.g. https://campus.yourdistrict.org}"
: "${IC_DISTRICT:?set to the appName path segment, e.g. yourdistrict}"
: "${IC_USERNAME:?parent portal username}"
: "${IC_PASSWORD:?parent portal password}"
```

(Same 4 env vars the MCP reads — reuse the repo's `.env` or the host's
secret store; don't hardcode a district.)

## One-time setup

None — `curl` and `jq` are the only tools needed (`brew install jq` if
missing). No profile/pairing step, no extension.

## Login (capture cookies + XSRF token)

`verify.jsp` accepts a urlencoded form POST and returns 200 with an
`<AUTHENTICATION>state</AUTHENTICATION>` marker in the body — **not**
via HTTP status — plus ~20 `Set-Cookie` headers. Use a cookie jar so curl
does the Set-Cookie parsing/deduping for you:

```sh
JAR=$(mktemp)
BODY=$(curl -sS -c "$JAR" \
  "$IC_BASE_URL/campus/verify.jsp?nonBrowser=true" \
  --data-urlencode "username=$IC_USERNAME" \
  --data-urlencode "password=$IC_PASSWORD" \
  --data-urlencode "appName=$IC_DISTRICT" \
  --data-urlencode "portalLoginPage=parents")

echo "$BODY" | grep -o '<AUTHENTICATION>[^<]*' # AUTHENTICATIONsuccess = good
```

`password-error` / `account-locked` / any non-`success` state means the
login failed — check that string before doing anything else. Credentials
go in the form body (never the query string — it lands in access logs).

Pull the XSRF token out of the jar (IC's JS reads it back and echoes it on
every request as `X-XSRF-TOKEN`; `JSESSIONID` alone is not enough):

```sh
XSRF=$(awk -F'\t' '$6=="XSRF-TOKEN"{print $7}' "$JAR")
```

## Core call pattern

Every subsequent request rides the jar + the XSRF header:

```sh
ic_get() { # ic_get <path-with-query>
  curl -sS -b "$JAR" -H "X-XSRF-TOKEN: $XSRF" -H 'Accept: application/json' \
    "$IC_BASE_URL$1"
}

ic_get '/campus/api/portal/students' | jq .
```

A **401** means the session expired (IC sessions last ~5-6h) — re-run the
Login step to get a fresh `$JAR`/`$XSRF` and retry once. There is no retry
budget beyond that in this shell version (the MCP's `CookieSessionManager`
does this automatically; here just redo the login block).

## The one rule: resolve student + enrollment first

Almost every read is scoped to a `personID` (student), and several need the
student's **enrollment** (`enrollmentID` / `calendarID` / `structureID`).
Always start with:

```sh
ic_get '/campus/api/portal/students' | jq '.[] | {personID, firstName, lastName, enrollments}'
```

Take `personID` for `studentId`/`personID` params, and the first (or
relevant) `enrollments[]` entry's `enrollmentID`/`calendarID`/`structureID`
for the endpoints that need them (attendance, school days, assessments,
features). There is no name→id search — `ic_list_students` (i.e. this call)
*is* the resolve step.

## Endpoints

All 17 read endpoints (grades, attendance, assignments, schedule, messages,
documents, fees, teachers, assessments, feature flags) with ready-to-run
`curl`+`jq` recipes are in `references/endpoints.md`. Two (`behavior`,
`food_service`) have real paths that were never confirmed live against a
district with that module enabled — try them, expect a 404 if the module
is off or the district's shape differs.

## Downloads

`ic_download_document`'s `url` field (from the documents list) may be a
relative `/campus/...` path or an absolute URL. Same jar + header pattern,
just write to a file instead of piping to `jq`:

```sh
curl -sS -b "$JAR" -H "X-XSRF-TOKEN: $XSRF" -o report-card.pdf "$IC_BASE_URL$DOC_URL"
```

## FeatureDisabled districts

Some districts turn whole modules off (behavior, food service, assessments,
documents, attendance). The MCP checks `displayOptions` first and falls
back to treating a 404 as "disabled." Doing the same by hand: fetch
`/campus/api/portal/displayOptions/{structureID}?personID=X` (see
references) and check the flag before assuming a 404 is a bug.

## Notes

- Read-only in practice: every recipe here is a GET. `ic_get_message`
  fetching a message body *may* mark it read on some district configs — the
  MCP's own probe couldn't confirm the side effect either way.
- No CUPS linked-district switching in this skill (a parent with kids in
  2+ IC instances under shared SSO) — that's a multi-step token-exchange
  flow (`src/client.ts`'s `discoverLinkedDistricts`); out of scope here.
  Run the login flow again against the linked district's own
  `IC_BASE_URL`/`IC_DISTRICT` if you need it.
- This project is developed and maintained by AI (Claude).
