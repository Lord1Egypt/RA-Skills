---
name: myatriumhealth-fpx
description: >-
  Read MyAtriumHealth (Atrium Health's Epic MyChart patient portal) — test
  results, medications, allergies, immunizations, health issues, visits, goals
  — from a shell with the fpx CLI (@fetchproxy/cli), by relaying requests
  through your signed-in Chrome tab. Use when you want your MyChart data in a
  script or one-shot without running the myatriumhealth-mcp server.
---

# MyAtriumHealth via fpx

Atrium Health's patient portal is Epic MyChart at `my.atriumhealth.org`. Its web app
talks to a clean JSON API, and this skill drives that same API through your signed-in
browser tab.

**Why the browser is required:** every MyChart cookie is `HttpOnly`, so the session
cannot be read or reproduced outside the browser, and login is MFA-gated. Requests are
relayed through the tab; the session cookie is never extracted or stored.

This reads personal health information. It only ever touches the signed-in user's own
account.

## One-time setup

    npm i -g @fetchproxy/cli          # also needs the ContextMint Bridge extension

ContextMint Bridge comes from
https://github.com/nullnet-app/contextmint-bridge/releases (Chrome: load the `chrome`
zip unpacked; use Chrome for now — Safari will ship inside the ContextMint app, which
has no public download yet). It is the fetchproxy extension renamed, same maintainer;
source is public there — build it, or verify a zip with `shasum -a 256 -c <zip>.sha256`.

Create the profile with its **full scope declared up front** — widening scope later
invalidates the grant and forces a re-pair:

    fpx profile add myatriumhealth --domain atriumhealth.org
    fpx profile declare myatriumhealth \
      --cookie '_Host-MyChart_Session' \
      --cookie '__RequestVerificationToken_L215YXRyaXVtaGVhbHRo0' \
      --cookie '_Host-MyChartLocale' --cookie 'MYCPERS' --cookie 'p-MYC-LBPersistence' \
      --capture-header 'cookie@my.atriumhealth.org'

Then sign in to MyAtriumHealth in Chrome and run any command below. The first one
prints a pair code — approve it in the ContextMint Bridge popup. The trust persists.

## Use it

    source references/mah.sh
    mah_signed_in || echo "sign in to MyAtriumHealth in Chrome first"
    export MAH_TOKEN="$(mah_token)"      # cache once per shell

    mah_api allergies/LoadAllergies | jq '[.dataList[].allergyItem | {name, severe: .isSevere}]'

`mah_api <area/Action> [json-body]` posts to the modern `api/…` endpoints (body
defaults to `{}`, which is all most of them need). `mah_legacy <Area/Controller/Action>
[querystring]` handles the older form-encoded ones (visits).

Every call needs the ASP.NET antiforgery token — `mah_token` scrapes it from a
signed-in page and the helpers attach it. Responses are large (test results 33 KB,
medications 30 KB); always project with `jq`.

**See `references/endpoints.md`** for the full endpoint list with ready-to-run,
live-verified `jq` recipes, and `references/mah.sh` for the helpers.

## Check the session, not the status code

MyChart answers an **expired session with HTTP 200 whose body is the login page**, and
the JSON endpoints then quietly return `{}`. A status check would report success
forever. `mah_signed_in` tests the body — use it when results come back empty. Sessions
are short-lived; expect to sign in again between uses.

There is a second, sneakier false green: an **empty** body. fetchproxy issues requests
from *inside* a tab on the target host, so with no my.atriumhealth.org tab open it
relays nothing — and empty text contains no login marker, so a naive "is this the login
page?" check reports SIGNED IN for a response that never happened. `mah_signed_in`
checks emptiness first and returns `2` with the real remedy (exit `1` means signed out,
`0` means signed in).

## Exit codes (fpx)

`0` ok · `1` usage · `2` bridge unavailable (extension not connected, or pairing not
approved) · `3` bot wall · `4` upstream HTTP error.

Data goes to stdout, pair codes and status to stderr — so `| jq` stays clean.

## Messages

`mah_messages [folderTag]` reads the Message Center. It is the one endpoint that cannot
be called with `{}`: it needs a five-key body whose `PageNonce` is the CSP nonce of an
`/app/*` page, and whose `externalLoadParams` must list the **non-local** organizations
only (filter `api/conversations/GetOrganizations` on the explicit `isLocal` flag —
passing the local org returns HTTP 500). The helper handles all of that.

`api/item-feed/FetchItemFeed` still needs parameters that have not been captured.

## In context groups

The myatriumhealth-mcp server (not this skill) joins the **health** group on hosts
that read its `_meta.mint` hints. Its canonical reads, each with `view: 'brief'`
(one line per item, `title — <ISO date | no date> — <status>`, at most 120 characters,
after a leading `-- patient: <label>` note naming whose chart was read, and `-- none`
when there is nothing; the lines ride in the untrusted-data envelope's `data` array,
since every title is the health system's or its staff's text):

- **what's new** — `mah_list_messages`: Message Center threads, dated by the latest
  message, `unread` / `read`.
- **what's on** — `mah_list_upcoming_visits`: appointments, `in progress` /
  `upcoming`.
- **what's due** — `mah_list_billing_accounts`: accounts with a balance, `<amount> due`.

None takes a subject: every read serves the session's active patient
(`mah_set_active_patient` switches it, a write), so a question about another patient
on the same login is a switch first, not a fan-out. A compound ask looks like "any new
messages from the doctor, and do I have appointments this week?" — one line per item
from each read. Through the browser bridge (no `MAH_USERNAME` / `MAH_PASSWORD`), the
group answers "needs your browser open" when no signed-in my.atriumhealth.org tab is
there to relay through.
