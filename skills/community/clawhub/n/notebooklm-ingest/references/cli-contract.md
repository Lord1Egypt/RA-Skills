# notebooklm-ingest — notebooklm-py CLI contract

The command surface this bundle spawns, the environment it spawns it with, and
what it is allowed to say about the credential afterwards. `scripts/nlm-cli.js`
is the only file that spawns `notebooklm`; everything below is its contract.

Research: `javis.is/docs/superpowers/specs/2026-10-29-notebooklm-connector-research.md`
— F4 (the command surface), F44–F52 (auth, the jar, the login path), F54/F59
(rotation), F62 (the transport), F32/F33 (the gates).

> **UNVERIFIED IN THE CONTAINER, AND DELIBERATELY SO.** `notebooklm-py` is
> Python ≥ 3.10, and whether the per-user openclaw container has a Python
> runtime it can use is a DeepShareIAC question that this build defers. So
> nothing in this bundle has been exercised against a real notebook: every test
> stubs the spawn boundary, and `doctor` turns a missing CLI into the named
> refusal `cli_missing` rather than a stack trace. The command surface below is
> read from the library's own CLI reference, not from a run in the container.

## Commands

Built as **argv arrays, never shell strings**, so a notebook title containing a
quote or a semicolon is an argument rather than syntax. The global `-p <profile>`
comes first, as the CLI requires.

| constructor | argv | what it is for |
|---|---|---|
| `argvNotebooks(p)` | `-p <p> list` | the notebook pick list |
| `argvNoteList(id, p)` | `-p <p> note list <id>` | one notebook's notes |
| `argvNoteGet(id, p)` | `-p <p> note get <id>` | one note's text — the read that feeds the push |
| `argvDownloadReport(id, dest, p)` | `-p <p> download report <id> <dest>` | a generated report as markdown |
| `argvAuthCheck(p, {test})` | `-p <p> auth check [--test]` | does the stored session still work |
| `argvDoctor(p)` | `-p <p> doctor` | the library's own diagnostics |

**No flag is invented.** In particular there is **no `--json`**: nothing in the
research confirms one on these commands, so stdout comes back as text and
`SKILL.md`'s flow has the **agent** read the ids and titles out of it. A script
that guessed at the output format would silently mis-identify notes the day
Google changes it — which it did, in five documented ways, at the 2026-07-16
rebrand. This is the house split: thin script, thick SKILL.md.

`list`, `note list` and `note get` are also the only commands this bundle needs.
`artifact list` / `artifact get` / `summary` / `source fulltext` exist (F4) and
are not used: audio overviews are out of scope, and a source's full text belongs
to whoever published it rather than to the user's own thinking.

## Environment

| variable | what this bundle does with it |
|---|---|
| `NOTEBOOKLM_TRANSPORT` | **Deleted from the child environment**, so the library's own default (`httpx`) runs. If the inherited environment names the impersonating TLS-fingerprint transport, the module **refuses to spawn at all** — see below. Any other value is dropped with a warning and the default still runs. |
| `NOTEBOOKLM_HOME` | The credential directory. **Write-probed before any read**; a read-only path is the named refusal `credential_path_readonly`. Defaults to `~/.notebooklm`. |
| `NOTEBOOKLM_PROFILE` | Not read. The profile comes from `prefs.json` and is passed as `-p`, so one container can hold more than one account without an env change. |
| `NOTEBOOKLM_AUTH_JSON`, `NOTEBOOKLM_REFRESH_CMD`, `NOTEBOOKLM_HEADLESS_REAUTH`, `NOTEBOOKLM_BACKEND` | Not set by this bundle. They are the unattended-credential shape (F46) and the android backend (F45); both are credential decisions the spec leaves open, and inventing one here would be the wrong place for it. |

### The transport pin (R15)

The library ships `_curl_cffi_transport.py` — which this bundle must never
select — and its own docstring says it exists
to speak to Google over a connection that impersonates a real browser's
TLS/JA3/HTTP-2 fingerprint. It is opt-in and self-labelled a proof of concept.
The research spike ran the plain default path and it **worked** (F58), so the
impersonating transport buys nothing today — and the design's anti-goal is
explicit: defeating a protective measure is a failure even if it ships.

So the rule is not "prefer the default". It is:

- the variable is **removed** from the child environment, which pins the default
  without depending on its name;
- an environment that **names** the impersonating transport is a **refusal**,
  not a silent override. An ops-set variable is a person declaring intent, and
  overriding it quietly would hide the attempt. `transport_forbidden` is the
  code, and its next action says to unset the variable — never to honour it.
- selecting it is a change to the spec requiring explicit approval. It is never
  an ops fix, and never something the agent does because a fetch failed.

The effective transport rides on **every** result from `run()`, success and
refusal alike, so `doctor` and the run digest can both name it (TC-S4-3 step 2
reads it from the run's log line).

### The credential path (R14)

The jar lives at `$NOTEBOOKLM_HOME/profiles/<profile>/storage_state.json`
(F44) — a Playwright cookie jar, which `auth check` validates by "Cookies
present" and "SID cookie".

Google rotates these cookies on a **measured 600-second cadence**:
`POST accounts.google.com/RotateCookies` answers `[["identity.hfcr",600],…]` and
sets fresh `SIDCC` / `__Secure-1PSIDCC` / `__Secure-3PSIDCC` (F59). The library
writes the refreshed jar back to disk, so a read-only path does not fail at
mount time — it fails about ten minutes later, silently, and every later call
then fails as a dead session. Upstream issue #312 is exactly this.

That is why the probe happens **before** the first read rather than at the first
write failure: otherwise the symptom (`session_dead`) and the cause
(`credential_path_readonly`) are the same event minutes apart, and the next
morning nobody can tell which it was.

## What this bundle may say about the credential

**Path, presence, size, mtime and a sha256 digest. Nothing else.**
`credentialFingerprint()` returns exactly those, and
`test/nlm-cli.test.js` asserts that a jar containing a cookie named `LSID` with
a secret value yields a fingerprint carrying **neither the name nor the value**.

No command in this bundle prints a cookie, logs one, echoes one into a digest,
or passes one to javis-server. TC-S5-2 records the digest across a rotation
window for exactly this reason: an mtime that advances and a digest that changes
prove rotation persisted without anyone looking at a credential.

See `credential-contract.md` for what the credential actually is and why it
matters that much.

## Failure classification

A non-zero exit becomes one machine-readable code, matched most-specific first:

| order | code | matched on |
|---|---|---|
| 1 | `dbsc_canary` | any `Sec-Session-` in the output. First, because a sighting changes what the whole design believes (F56) and must not be swallowed by the auth pattern it arrives beside. |
| 2 | `transport_forbidden` | the impersonating transport named in the output — the library's own error when that path is half-configured. |
| 3 | `location_gate` | `?location=unsupported` and friends (F32) |
| 4 | `rate_limited` | `RateLimitError`, rate-limit wording, `429` |
| 5 | `session_dead` | `CookieMismatch`, `not authenticated`, auth errors, `sign in again` (F33: a password change signs a stored session out by design) |
| 6 | `cli_missing` | `ModuleNotFoundError`, `command not found`, exit 127, spawn `ENOENT` |
| — | `nlm_failed` | anything else. Carries the **last** line of output, bounded to 300 characters: a traceback's useful half is at the bottom, and the detail is about to be rendered into the user's chat. |

The first four and `cli_missing` and `dbsc_canary` **stop a fetch**: every later
note would fail the same way. `nlm_failed` is per-note, so one unreadable note
never loses the batch.

**A zero exit is classified too, for one code only.** `Sec-Session-Registration`
is how DBSC *starts*: Google sends it on a call that SUCCEEDS, as the invitation
to bind the session to a device key. A canary that only ran over failures would
therefore first fire months later, as a 401, when enforcement had already broken
the path. So a successful call whose **stderr** names a `Sec-Session-*` header
comes back as `dbsc_canary` with `exit: 0`.

**Stderr only, on the success path.** On a successful `note get`, stdout IS the
note — third-party text out of a shared notebook. Scanning it would let a note
whose body merely types `Sec-Session-Id` end every run and post a false first
sighting to the account's permanent canary record. Headers are diagnostics and
arrive on stderr; a failing call still matches on both streams, where there is
no note body to confuse.
