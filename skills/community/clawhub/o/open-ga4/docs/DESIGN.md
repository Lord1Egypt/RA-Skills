# Design: `open-ga4`

Status: accepted 2026-08-14, packaging half superseded 2026-08-16

**Read this alongside
[the skill design](superpowers/specs/2026-08-16-open-ga4-design.md).** That document
supersedes the packaging decisions here: D1 below is reversed (this ships as an OpenClaw
skill, not a plugin), D2's dependency count is now zero rather than one, D3's credential
list gained a source, and the six tools of D4 are seven commands on a command line. The
analytics decisions, D4's shape through D8, are unchanged and are why this file is still
here. Each superseded decision says so in place rather than being deleted, because the
reasoning that was rejected is the part worth keeping.

## Problem

An OpenClaw agent cannot answer "how did the site do last week?" without a
Google Analytics integration. The integrations that exist today each solve a
slice of the problem and impose real setup cost:

- **Python-shelling skills** ship a `SKILL.md` plus a `scripts/*.py` file and
  require `uv`, a virtualenv, and the `google-analytics-data` package (tens of
  megabytes, hundreds of transitive dependencies) before the first question can
  be asked. They typically expose exactly one hardcoded report.
- **Hosted MCP connectors** solve setup by routing analytics data through a
  third-party server. That is a privacy and trust cost the user cannot audit.
- **Thin API wrappers** expose `runReport` verbatim and leave the model to guess
  GA4's ~200 dimension and ~150 metric API names, which it gets wrong.

## Goals

1. Working answer in under five minutes, for someone who is not a developer.
2. The model picks correct dimensions and metrics on the first attempt.
3. Every privacy claim is enforced by code and covered by a test.
4. The dependency and network surface is small enough to audit in one sitting.

## Non-goals

- Writing to Google Analytics. It is read-only by construction.
- Replacing the GA4 UI. Deep, exploratory analysis stays in the console.
- Supporting Universal Analytics (shut down; the API is gone).

## Decisions

### D1. Package shape: `definePluginEntry` (reversed)

**Superseded.** This project no longer registers with OpenClaw's plugin API at all. It
ships as a skill: `SKILL.md` plus committed JavaScript, invoked as
`node <skill-dir>/lib/cli.js <command>`. The cost of that reversal, recorded in the newer
document, is that `resultContentSource` is only reachable through the plugin registration
API and therefore goes away; it was inert on every released host in any case. The original
reasoning follows.

`defineToolPlugin` is the obvious choice for a tools-only plugin and was the
first pick. It is wrong here. Reading the real SDK source rather than the docs
(`src/plugin-sdk/tool-plugin.ts`), the object it hands to `api.registerTool` is
exactly `{ name, label, description, parameters, outputSchema?, execute }`:
there is no way to set `resultContentSource`, and no `register(api)` callback,
so `registerHealthCheck` is unreachable. Both are load-bearing here (see D6).

So: `definePluginEntry` from `openclaw/plugin-sdk/plugin-entry`, with a
hand-maintained `openclaw.plugin.json`. The cost is that `contracts.tools` must
be kept in step with the code by hand; a test asserts the manifest matches the
registered tool names so drift fails CI rather than silently hiding a tool.

Ships built JavaScript (`./dist/index.js`) via `openclaw.extensions`, per the
packaging rule that source entries only work for workspace-local development.
`compat.pluginApi` targets the newest *released* host, not the repository's
`main` version; copying the bundled extensions' `>=2026.8.1` would make the
plugin uninstallable on every host that actually exists today.

### D2. Zero network dependencies

Runtime dependencies: **none at all**. `package.json` has no `dependencies` and no
`peerDependencies`, and every import in `src/` is either relative or `node:`-prefixed.

This originally read "`typebox` only", which OpenClaw itself depended on. Typebox was
imported in three files and only ever to build tool parameter schemas and the plugin
config schema, both of which existed to satisfy the plugin API and both of which died
with D1. Dropping to zero is not a vanity metric: it is what makes "install and it runs"
true, because there is no `node_modules` to be missing and no install step that can fail.

Rejected: `@google-analytics/data` (gRPC stack and generated protos),
`googleapis` (very large), `google-auth-library` (pulls `gaxios`, `gcp-metadata`,
and an HTTP stack we would then have to constrain).

Consequence: it implements OAuth service-account JWT assertion itself
with `node:crypto` (`createSign("RSA-SHA256")`) and calls the GA4 REST API with
the host's configured `fetch`. This is roughly 150 lines and it makes the egress
claim below verifiable by reading one file.

### D3. Auth: service account by default, ADC as fallback

Resolution order, first match wins:

1. `GA4_CREDENTIALS` holding the service-account JSON key's contents, pasted
   straight in.
2. `GA4_CREDENTIALS` holding a path to that key file instead. The two are told
   apart by whether the trimmed value starts with `{`. This replaced the
   original source 1, a path in the plugin's own config block, which went away
   with D1.
3. `GOOGLE_APPLICATION_CREDENTIALS`: the Google-standard environment variable.
   Chosen because existing GA4 skills already set it, so users migrating keep
   their setup.
4. Application Default Credentials at the well-known gcloud path
   (`~/.config/gcloud/application_default_credentials.json`), which is an
   authorized-user refresh-token grant rather than a service account.

Rejected as the default: an interactive OAuth loopback flow. It requires the
user to create their own OAuth client and consent screen in Google Cloud, and
unverified "Testing" apps have refresh tokens that expire after seven days;
the integration would silently break weekly.

Only ever requests `https://www.googleapis.com/auth/analytics.readonly`.

### D4. Operation surface: intent-shaped, with one escape hatch

Wide enough to cover what people ask, narrow enough that the model picks correctly.
These were six tools; they are now seven commands, with the same bodies behind them:

| Command | Purpose |
| --- | --- |
| `doctor` | Check every setup requirement and print the exact fix for the first failure. With `--json`, the single next thing the user must do. |
| `fields` | Search the property's live dimension and metric catalog by keyword. |
| `report` | The workhorse: one preset id picks a ready-made report. |
| `compare` | The same reports across two consecutive periods. |
| `live` | Active users in roughly the last 30 minutes. |
| `query` | The escape hatch: explicit dimensions, metrics, filter and sort. |
| `properties` | Every property the credential can read, with its numeric id. |

`report` takes a single preset id that expands to a verified dimension/metric
combination, so naming an intent is enough and there is nothing to guess.
Anything the presets do not cover goes to `query`.

Splitting those two rather than putting a preset argument alongside optional
`--dimensions` and `--metrics` on one command keeps the common case to one
value, which is the whole point: a model that only has to pick a preset id
cannot pick an incompatible dimension/metric pair.

`properties` was in the first draft, was folded into the diagnostic tool, and
is separate again. The original reason for folding it in was that every tool
schema is spent from the context window of every conversation whether it is
used or not; a command line costs nothing until it is run, and setup needs
property discovery on its own, before any report is possible.

Results render as markdown tables, not raw JSON: fewer tokens, and the model
reads them more reliably.

### D5. Privacy controls, enforced in code

Every one of these that can be turned off is turned off through an environment
variable and has no command-line flag, because a flag can be set by the model
and dimension values are written by site visitors.

| Control | Default | Enforcement |
| --- | --- | --- |
| Read-only scope | always | Scope constant; no write endpoint exists in the client. |
| Egress allowlist | always | Every request passes a host check; unknown hosts throw. |
| PII redaction of dimension values | on | Query strings, emails, phone numbers, UUIDs, and long digit runs are masked before the model sees them. |
| User-identifying dimensions blocked | on | `userId` and user-scoped custom dimensions require explicit opt-in. |
| Property allowlist | off | When set, requests to other properties are refused. |
| Report data persisted to disk | never | No cache file, no report log. |
| Credentials in output or logs | never | Redaction covers errors, logs, and tool results. |
| Telemetry | none | No analytics, no phone-home, no update check. |
| Local audit log | off | Opt-in; records query, property, and timestamp, never response bodies. |

The honest limitation, stated in `PRIVACY.md` rather than buried: report data
returned to the agent is seen by whatever model provider the user has
configured. The skill controls what leaves Google, not what the user's own LLM
does with it.

### D6. Analytics data is attacker-controlled input

This is the part most GA4 integrations miss. A dimension value like `pagePath`
or `pageTitle` is not authored by the property owner; it is whatever a visitor
requested. Anyone on the internet can visit
`yoursite.com/?ignore-previous-instructions-and…` and have that string appear in
tomorrow's report, and from there in an agent's context as though it were data
the owner wrote.

The consequence: report rows are rendered into a fenced, clearly labelled data
block rather than interpolated into prose, so injected text does not read as
instruction, and `SKILL.md` tells the agent the same thing in words.

There was a second consequence, and D1's reversal removed it: every tool
registered with `resultContentSource: "network"`, OpenClaw's marker for
externally controlled content, which was the concrete reason D1 could not use
`defineToolPlugin`. It is unreachable outside the plugin API and was read by no
released host, so what is lost is a label that would have taken effect on a
future upgrade.

This is not a complete defence against prompt injection (nothing is), but
labelling the provenance is strictly better than the common practice of
returning `JSON.stringify(response)` and hoping.

### D7. No hardcoded field catalog as the source of truth

GA4 renames things: `conversions` became `keyEvents`, and the old names survive
only in `MetricMetadata.deprecatedApiNames`. Two of the research briefs produced
hand-maintained field lists that disagreed with each other, which is the whole
argument against shipping one as truth.

The live `properties/{id}/metadata` response is authoritative and is what
`fields` searches. Diagnostics for a bad field name come from that metadata,
never from string-matching Google's error prose, which is unversioned and
undocumented.

*Superseded in part.* Two things named here did not ship. No metadata snapshot
is generated and no CI job re-fetches one: the preset definitions in
`src/ga4/presets.ts` name their fields directly and everything else is read
live. And `checkCompatibility` was implemented in the client but never called
by anything; it was deleted in the final review rather than left inside a
network surface whose completeness is the argument this document makes,
because a reader auditing that surface would find a method nothing uses.

### D8. Errors map to fixes, not stack traces

Every known GA4 failure maps to a sentence naming the cause and a next action:
API not enabled, service account missing property access, wrong property ID,
measurement ID (`G-XXXXXXX`) used where a numeric property ID is required,
invalid dimension or metric name (with the closest valid names suggested),
incompatible dimension/metric pairing, and quota exhaustion.

`doctor` runs the same checks proactively so a user can fix setup without
first triggering a failure.

## Architecture

```
src/cli/                 argv parsing, dispatch, exit codes, output streams
src/config.ts            settings resolved from the environment
src/setup/               doctor --json's one-blocking-step state machine
src/auth/                credential discovery, RS256 JWT, token cache
src/ga4/                 egress-guarded fetch, Data API, Admin API,
                         error taxonomy, dimension/metric catalog,
                         date parsing, markdown formatting
src/privacy/             redaction, dimension policy, property allowlist,
                         optional audit log
src/tools/               one file per operation, called by the CLI
```

Each module is independently testable: auth does not import the HTTP client,
redaction does not import the API layer, the CLI composes the rest.

## Verification

- `npm run check`: typecheck, then tests, then build.
- `npm test`: unit tests per module, with recorded GA4 responses as fixtures,
  plus the documentation tests that pin `SKILL.md` and `README.md` to the code.
- A live read-only smoke test against a real property, run manually, never in
  CI (CI has no credentials and must not need any).
