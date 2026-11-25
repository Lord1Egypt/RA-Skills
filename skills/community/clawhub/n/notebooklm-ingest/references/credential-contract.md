# notebooklm-ingest — credential contract

What the stored Google session is, what this bundle is allowed to say about it,
and what it must never do with it.

Research: `javis.is/docs/superpowers/specs/2026-10-29-notebooklm-connector-research.md`
— F44 (the jar), F49/F51 (how it is minted), F54/F59 (rotation), F56/F57 (DBSC),
F63 (what it actually grants), F33 (what invalidates it).

## What it is

A **Playwright cookie jar** at
`$NOTEBOOKLM_HOME/profiles/<profile>/storage_state.json`.

And it is not a NotebookLM-scoped token. It is a **Google account** cookie jar:
29 cookies across 5 domains, including `LSID` and `__Host-GAPS`, scoped to
`myaccount.google.com` among others, with roughly a 13-month expiry (F63). That
is the honest description, and the spec carries it in the user's own words at
sign-in because it is the thing they are actually agreeing to.

There is no smaller credential available. Google publishes no API that can read
notes, reports or chat answers (F15, F17), so there is no scope to ask for and
nothing an OAuth grant could cover. The existing `google` provider — Calendar
plus read-only Gmail — cannot be reused for that reason.

## How it is created (R8)

By the **user**, once, in a real browser. `login --browser chrome` drives the
system Chrome under Playwright and the person types their own password into
Google's own form; Google accepted exactly this in the research spike, with no
automation challenge (F49). In HiJavis the same thing happens through the in-app
sign-in webview, the mechanism Luma's cookie capture already uses.

**Javis never types a Google credential.** Not into a form, not into a CLI
prompt, not from a stored value. If a path seems to require it, that path is
wrong.

Chrome's own cookie store is **not** an alternative: `--browser-cookies chrome`
failed on every profile with "macOS Keychain item not found" (F51), and a
broader sweep of other browsers' cookie stores was deliberately not performed.
Reading a browser's credential store is not a fallback this design has.

## What this bundle may say about it

**Path, presence, size, mtime, and a sha256 digest of the file.** That is the
whole of `credentialFingerprint()`, and it is what `doctor` reports.

**Never a cookie name, and never a cookie value.** Not in stdout, not in a
digest pushed to the user's chat, not in a log line, not in a refusal's detail
field, and never to javis-server. `test/nlm-cli.test.js` asserts it against a
jar containing `LSID` with a secret value: neither the name nor the value
appears in the fingerprint.

The digest exists so that rotation can be **proved without looking**: TC-S5-2
records the mtime and the digest, waits past the rotation window, and checks
that both moved. That is a liveness check made from metadata alone.

## Why the path must be writable (R14)

Google declares a **600-second rotation cadence**:
`POST accounts.google.com/RotateCookies` answers `[["identity.hfcr",600],…]` and
sets fresh `SIDCC` / `__Secure-1PSIDCC` / `__Secure-3PSIDCC` (F59). The library
writes the refreshed jar back to disk.

So a read-only credential directory is not a hygiene problem. It is a **ten
minute** liveness problem: the mount succeeds, the first read succeeds, and
roughly ten minutes later every call fails as a dead session. Upstream issue
#312 is precisely this. Which is why `nlm-cli.js` **write-probes the directory
before the first read** and refuses with `credential_path_readonly` — otherwise
the cause and the symptom are the same event minutes apart, and nobody can tell
afterwards which one happened.

## What invalidates it

- **A password change or reset.** Google signs the account out everywhere except
  verification devices, some third-party-authorised devices and home devices; a
  stored jar is none of those (F33). This is **by design and it will happen**,
  which is why R11 exists: the skill says the session has ended, says no wiki
  content was lost, and offers re-authorisation. It never retries, and it never
  presents the breakage as a bug.
- **Expiry**, about 13 months out.
- **Revocation** from the Google account's own device list.

In every case the answer is the same: report it, lose nothing, offer the
re-authorise action. `wiki_ingest_external_tool` still accepts hand-fed text
with no Google access at all, so the wiki keeps working while the automated leg
is dead.

## DBSC, and the canary (R16)

Device Bound Session Credentials never **engaged** in the research. No
`Sec-Session-*` header appeared on any request from either origin:
`DBSC_MARKERS_SEEN: NONE` on all four observations (F56). The correct reading is
not "device binding tolerates an off-device session" — it is "**the API surface
notebooklm-py uses sits outside DBSC enforcement today**".

A Playwright-minted jar **is** DBSC-enrolled at the browser layer (F57). So the
risk is not that DBSC might refuse us; it is that Google may extend enforcement
to this path. That is a roadmap risk with an observable tripwire rather than a
present blocker.

The tripwire is R16, and it is owned by **javis-server**, which watches the
shared credential and must fire even when no skill is running. This bundle
carries a second, cheaper half of it: if the CLI's own diagnostics ever mention
a `Sec-Session-*` header, `nlm-cli.js` classifies it as `dbsc_canary` **before**
every other pattern, including the auth pattern it would arrive beside — and on
a call that SUCCEEDED as well as one that failed, because
`Sec-Session-Registration` arrives on a working call, which is how DBSC begins.
A sighting is reported verbatim and the run stops. It is never retried, and it
is never worked around.

The sighting then has to reach the account, which is the only place "the FIRST
appearance" can be known. It travels two ways, and both are needed: the run
stops with an `upstream_error` push (`response_headers` carrying the NAMES, no
values), and every push that follows in the same run carries the same names, so
a report lost to a network error is not a tripwire that never fired. The server
writes its `source_canary` row once per account, so the repetition costs
nothing.

## The anti-goals, restated because they are easy to erode

- **No defeating a protective measure.** No residential-proxy egress to disguise
  a datacenter origin. No engineering around DBSC. No TLS-fingerprint
  impersonation — `NOTEBOOKLM_TRANSPORT` is pinned to the library default and
  the impersonating transport is a refusal, not a setting (see
  `cli-contract.md`). If a control blocks a host, the design moves the host:
  that is what the `host` field is for.
- **No silent staleness.** A connector that stops updating without saying so is
  worse than none, because the wiki looks current and is not.
- **No credential in a place the user was not told about.** The spec takes the
  established server-side path, consistent with Luma's captured cookies, and
  says so rather than claiming a smaller blast radius than it has.
