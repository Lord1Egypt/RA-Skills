---
name: jobber-fpx
description: >-
  Read your Jobber Client Hub — the customer portal a service business (pest
  control, lawn care, HVAC, cleaning) uses to send you appointments, quotes and
  invoices — from a shell with the fpx CLI (@fetchproxy/cli), instead of running
  the jobber-mcp server. Use when you want your Jobber data without the MCP, in
  a script, or on a machine where the MCP isn't installed.
---

# Jobber Client Hub via fpx (no MCP)

This reads the **customer** side of Jobber: the hub a business shares with you,
at `clienthub.getjobber.com`. It is not the Jobber Developer API — that one
serves the business running on Jobber and needs an OAuth app you cannot register
as their customer. See `references/why-not-the-api.md`.

`clienthub.getjobber.com` sits behind a Cloudflare managed challenge that
fingerprints the **TLS client**, so plain `curl` and Node get `403 Just a
moment` even with a current Chrome User-Agent and the full browser header set.
`fpx` issues the request from inside your own signed-in tab, which has already
cleared the challenge. There is no server-side path; the bridge is not optional
here.

## One-time setup

```sh
npm install -g @fetchproxy/cli               # provides `fpx`
fpx profile add jobber --domain getjobber.com # fetch capability only — no cookie scope needed
```

The first fetch prints a pair code to **stderr**; approve it in the ContextMint
Bridge extension popup. Pairing persists — every later call reuses it.

Requirements: the **ContextMint Bridge** extension (from
https://github.com/nullnet-app/contextmint-bridge/releases — Chrome: load the
chrome zip unpacked; Safari isn't available yet, so use Chrome for now), an open
`clienthub.getjobber.com` tab signed into the hub, and the extension's
**Site access** allowing `getjobber.com`. (ContextMint Bridge is the fetchproxy
extension renamed, same maintainer; source at
https://github.com/nullnet-app/contextmint-bridge — verify a release zip with
`shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`.)

> Only the fetch capability is declared, deliberately. Cookies ride the tab
> automatically, so no cookie scope is needed — and widening scope *after* the
> first approval leaves fetches working on the old grant while the new
> capability errors. Everything this skill does is covered by the grant above.

## Your hub URL is a credential

Each business gives you a **different** hub, identified by a UUID:

```
https://clienthub.getjobber.com/client_hubs/<hub-uuid>/
```

Anyone holding that URL can read the hub, so treat it like a password: keep it
in an env var, never in a committed file or a shell history you share.

Get it from any email that vendor sent you — the "View Details" / "View
Invoice" button — or from the address bar of an open hub tab.

```sh
export JOBBER_HUB='https://clienthub.getjobber.com/client_hubs/<hub-uuid>'
```

One export per business. If two vendors both use Jobber, they are two hubs with
nothing in common; there is no combined view and no account that spans them.

## Core call

Fetch the page, pipe it through the parser, and you have JSON for `jq`:

```sh
PARSE="$(dirname "$0")/references/parse-clienthub.mjs"   # or an absolute path

fpx get -p jobber "$JOBBER_HUB/appointments" \
  | node "$PARSE" appointments \
  | jq '.'
```

The parser is dependency-free — a bare `node` runs it, no install step.

`jq` alone cannot do this job: the hub is server-rendered HTML, and its two page
families store data two different ways (JSON islands for appointments, plain
cards for everything else). The parser hides that split behind one interface.

| Command | Reads |
| --- | --- |
| `node "$PARSE" appointments` | visits — Today / Upcoming / Past |
| `node "$PARSE" invoices` | invoices, with section state (`Paid`, …) |
| `node "$PARSE" quotes` | quotes |
| `node "$PARSE" work_requests` | requests you raised |

Ready-to-run recipes — next visit, unpaid invoices, totals, a single record —
are in `references/recipes.md`.

### Record `url`s are hub-relative

Every record's `url` is relative to your hub — `appointments/2236612358`,
`invoices/150208512` — because the hub UUID is a credential and stays out of
the output. Prefix `$JOBBER_HUB/` to open or fetch one:

```sh
node "$PARSE" invoices < page.html | jq -r --arg base "$JOBBER_HUB/" '.[] | $base + .url'
```

> **Changed in 1.0.7 (output contract).** Earlier versions printed
> `/client_hubs/<hub-uuid>/appointments/N` (and the same for invoice, quote and
> work-request cards). A script that prefixed
> `https://clienthub.getjobber.com` to `.url` must now prefix `$JOBBER_HUB/`
> instead, or it builds a URL with no hub in it.

## Pass the right kind — the failure is silent otherwise

`appointments` reads embedded JSON; the other three read HTML cards. Point the
appointments reader at the invoice page and it finds the page's one island — an
unrelated *referral widget* — which parses cleanly and contains no invoices. It
looks like "you have no invoices" rather than like a bug.

The parser warns on stderr whenever it returns an empty list, for exactly this
reason. An empty result with no warning means the page genuinely had none.

## Exit codes

The parser follows the `fpx` convention, so a pipeline can branch on either:

| Code | Meaning |
| --- | --- |
| `0` | parsed (possibly an empty list — check stderr) |
| `3` | Cloudflare interstitial, not a hub page — the request missed the tab |
| `64` | bad usage (unknown kind) |
| `65` | empty input — the upstream `fpx` call produced nothing |

From `fpx` itself: `2` bridge down, `3` bot wall, `4` upstream non-2xx.

```sh
fpx get -p jobber "$JOBBER_HUB/invoices" > page.html || {
  echo "fpx failed ($?) — is Chrome running with a signed-in hub tab?" >&2; exit 1; }
node "$PARSE" invoices < page.html
```

## What this cannot do

Read-only, by design and by capability:

- **No writes.** Submitting a work request, approving a quote or confirming an
  appointment are form POSTs with CSRF and, on some flows, a Turnstile token
  read from the DOM. `fpx` has no DOM-read verb, so it cannot complete them.
- **No PDF or file downloads.** Invoice and quote PDFs are served as
  `Content-Disposition: attachment`; the bridge does `fetch()`, not navigation,
  so these URLs can only be *resolved* for you to open, never fetched.
- **No payments.** Paying an invoice means entering card or bank details. Never
  automate that — open the hub and do it yourself.

## In context groups

The jobber-mcp server (not this skill) joins the **home** context group on an
mcp-host that publishes groups. Its tools carry `_meta.mint` hints; the
group's intent tools call its canonical reads for you:

- **what's on** → `jobber_list_appointments`, per hub, over the asked range
  (`start`/`end`), in `view: 'brief'` (`Visit 9:00am at <address> — 2026-06-28 — upcoming`).
- **what's due** → `jobber_list_invoices`, per hub, in `view: 'brief'`: the
  invoices still owed (every section but Paid) with their due date.
- **Subjects** are the configured hub labels (`JOBBER_HUB_LABEL` /
  `JOBBER_HUBS`), one per provider; hub ids are never published.

A compound ask reads across the group: "any visits at the house this week —
and anything I owe the pest company?" answers both reads for each hub. The
server reaches the hub through the browser bridge, so when Chrome is closed or
the extension is not paired the group says Jobber **needs your browser open**
rather than answering "nothing".
