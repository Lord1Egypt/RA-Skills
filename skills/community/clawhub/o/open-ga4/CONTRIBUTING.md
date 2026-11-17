# Contributing

Thanks for looking. This document covers the things that are easy to get wrong here:
running the tests against the built bundle, never pointing the OpenClaw CLI at your real
installation, backing every privacy claim with a test, keeping the prose consistent with the
code, and adding a preset whose field names are real.

Everything you contribute is licensed MIT-0, same as the rest of the project.

---

## Getting set up

```bash
git clone <this repository>
cd open-ga4
npm install
```

Node 22.22.3 or newer, the floor `package.json`'s `engines.node` sets. The HTTP layer uses
`AbortSignal.any` and `AbortSignal.timeout`, and the package is native ESM throughout.

There are **zero runtime dependencies**. `package.json` has no `dependencies` and no
`peerDependencies`, and every import in `src/` is either relative or `node:`-prefixed. That
is a headline claim in the README, in `SECURITY.md` and in `PRIVACY.md`, and it is what
makes "install and it runs" true, because there is no `node_modules` to be missing. Adding
the first one is a design change, not a chore; open an issue first. Two tests hold the line:
one asserts the manifest is empty, the other walks `src/` and fails on any non-relative,
non-`node:` import, because a `dependencies: {}` check passes happily while a source file
imports something that happens to be present as a transitive devDependency. Authentication
is implemented on `node:crypto` and the GA4 REST API is called with `fetch`; both stay that
way.

---

## Running the tests

```bash
npm run check         # typecheck, then tests, then build
npm run typecheck     # tsc -p tsconfig.check.json
npm run build         # scripts/build-lib.mjs, emits lib/
npm run check:lib     # scripts/build-lib.mjs --check, fails if lib/ has drifted from src/
npm test              # vitest run
```

**`npm test` builds first.** `pretest` runs `npm run build`, because
`src/privacy/surface.test.ts` asserts against `lib/` (the built artifact that actually
ships), not against the source. Invoking `vitest` directly bypasses that and reads whatever
`lib/` happened to contain last, which means it can pass on code you have already deleted
and fail on code you have already fixed. Prefer `npm test`.

No test needs network access and no test needs credentials. If you find yourself wanting
either, you are writing an integration test; record the response as a fixture instead. A
live read-only smoke test against a real property is a manual step, run by hand, and never
part of the suite; CI has no credentials and must never need any.

Commit messages that change the suite carry the test count as their last line. Take it from
the vitest summary of the run you actually did.

---

## Never run `openclaw` directly from this repo

There is nothing here to validate through the CLI. `npm run check` is the whole gate:
typecheck, tests, build. The skill's own contract lives in `SKILL.md` and is checked by
`src/docs/skill.test.ts`, not by an OpenClaw subcommand.

If you do run the OpenClaw CLI against this repo (installing the local checkout as a skill,
for instance), use the wrapper:

```bash
./scripts/openclaw-sandbox.sh <command>
```

Several OpenClaw subcommands boot enough of the host runtime to run config doctor and state
migrations. Against a real installation, that can rewrite your `openclaw.json` and relocate
your state files, while you are debugging, which is the worst possible moment to discover
it.

`scripts/openclaw-sandbox.sh` redirects `HOME`, `XDG_CONFIG_HOME`, `XDG_STATE_HOME`,
`XDG_DATA_HOME`, `OPENCLAW_STATE_DIR` and `OPENCLAW_CONFIG_DIR` into a throwaway `.sandbox/`
inside the repo. Setting `OPENCLAW_STATE_DIR` on its own is **not** sufficient: state
migrations still probe the legacy paths under `HOME`, which is why the wrapper moves `HOME`
too.

If you need a different scratch location, set `OPENCLAW_SANDBOX_DIR`. Do not "just this
once" run the bare CLI.

---

## Every privacy claim needs a test

This is the rule the project exists to demonstrate. `README.md` and `PRIVACY.md` make
specific negative claims: that the skill does not do certain things. A negative claim in a
README is worth nothing on its own. Each one is checked against the built bundle.

| Claim | Where it is enforced | Where it is asserted |
| --- | --- | --- |
| Contacts only `oauth2.googleapis.com`, `analyticsdata.googleapis.com`, `analyticsadmin.googleapis.com` | `ALLOWED_HOSTS` + `assertAllowedUrl` in `src/ga4/http.ts`, checked before any request is issued | `src/ga4/http.test.ts`, and a scan of `lib/` in `src/privacy/surface.test.ts` |
| Requests no OAuth scope but `analytics.readonly` | the scope constant is the only one in the codebase | `src/privacy/surface.test.ts` |
| Never calls `properties.audienceExports`, `properties.audienceLists` or the Admin API's `runAccessReport`, the three surfaces built to return rows keyed to an individual visitor | those methods are not implemented in the client | `src/privacy/surface.test.ts` asserts the strings are absent from `lib/` |
| Writes no report data to disk | nothing outside the optional audit log opens a file for writing | `src/privacy/surface.test.ts` scans `lib/` for `writeFile`, `appendFile`, `createWriteStream`, `mkdir` |
| Blocks person-identifying dimensions unless opted in | `assertDimensionsAllowed` in `src/privacy/policy.ts` | `src/privacy/policy.test.ts` |
| Redacts identifiers out of dimension values, unless `GA4_REDACT` turns it off | `redactValue` in `src/privacy/redact.ts` | `src/privacy/redact.test.ts` |
| Keeps a credential out of any error message it prints, always | `redactText` in `src/privacy/redact.ts` | `src/privacy/redact.test.ts` |

So:

- **Adding a sentence to `README.md` or `PRIVACY.md` that says the skill does not do
  something means adding the assertion in the same commit.** If you cannot write the
  assertion, do not write the sentence.
- **A limitation that cannot be enforced in code is documented as a limitation, not softened
  into a claim.** The load-bearing example: report data returned to the agent is seen by
  whatever model provider the user has configured. This skill controls what it asks Google
  for and what it hands to the agent; it has no say in what the user's own LLM provider does
  with a report once the agent reads it. `PRIVACY.md` says that plainly and nothing in the
  docs may imply otherwise.
- **Do not weaken an assertion to make a change pass.** If `surface.test.ts` fails because
  your patch added a host, a scope, a disk write or a per-person API surface, the patch is
  the problem. Widening the allowlist is a reviewable decision with a discussion attached to
  it, not a one-line diff.

Three things are never acceptable in a patch: a write scope, any telemetry or phone-home
(including update checks), and persisting report data or tokens to disk. Tokens are held in
memory only. A cached access token in a file is a credential at rest that the user did not
agree to.

---

## Why a prose edit can fail the build

`src/docs.test.ts` reads `README.md`, `SETUP.md`, `SKILL.md`, `PRIVACY.md`, `SECURITY.md`,
`CONTRIBUTING.md`, `CHANGELOG.md` and `docs/DESIGN.md`, and fails on:

- a JSON block that does not parse;
- any mention of the plugin configuration block this project used to require, in the
  shipped source or the shipped documentation. That block no longer exists, and a hint
  naming it tells a stuck user to edit something that is not there. The test names the
  exact string; this file does not, so that the sweep does not trip over the sentence
  describing it;
- a `GA4_`-prefixed environment variable named in the documentation that no shipped source
  file reads;
- a claim about the number of runtime dependencies that disagrees with `package.json`,
  in the documentation or in `.github/dependabot.yml` and `.github/workflows/ci.yml`,
  because a comment in repository config made that claim and outlived the dependency;
- a retired tool name (`ga4_` plus report, compare, realtime, query, fields, diagnose or
  properties) anywhere under `src/` or in the shipped documentation. They were tool names
  under the plugin API and are commands now, so a message naming one sends a stuck user
  to type something that does not exist;
- this project calling itself a plugin: in the shipped source, the word at all; in the
  documentation, only the present-tense self-reference, meaning the word directly after
  "this", or after "the" and directly before a present-tense verb. Discussing the former
  plugin in the past tense is deliberate and stays, which is why the documentation half
  is narrow. This sentence does not spell either pattern out, so that the sweep does not
  trip over the description of itself;
- a backticked identifier shaped like a preset id that is not in `PRESETS`;
- an `npm run` script that is not in `package.json`;
- a `googleapis.com` host that is not in `ALLOWED_HOSTS`, apart from the two named in
  `SECURITY.md` as examples of what the allowlist rejects;
- `PRIVACY.md` not naming every allowed host, or not stating that the reader's own model
  provider still sees the data.

`src/docs/skill.test.ts` does the same job for the skill contract and fails on:

- a description over 300 characters, or a frontmatter `name` or `version` that disagrees
  with `package.json`;
- anything in `requires.env`, which would report "needs setup" forever for the three
  credential sources that variable is not;
- a command quoted in `SKILL.md` or `README.md` that `parseArgs` rejects;
- a command name in the decision table or in the reference table that is not in
  `COMMANDS`, or a command in `COMMANDS` that either table leaves out. Both tables are
  checked, because an invented name in the reference section would reach a reader exactly
  as easily as one in the decision table;
- a flag documented against a command that does not accept it, or a flag a command
  accepts that the flag table does not document, both checked against `KNOWN_FLAGS`.
  `--help` is the one exception, because `parseArgs` handles it before it validates
  flags at all;
- a `blocked_on` value the code can emit that has no section in the setup tree, or a
  section for a value the code cannot emit;
- an environment variable the code reads that the frontmatter does not declare, or the
  other way round. That last one is a publishing problem rather than a documentation one:
  ClawHub's security review compares declared metadata against actual behaviour.

So renaming a command, a script, a variable or a preset breaks the build until the sentence
that mentions it is updated in the same commit. What the tests cannot check is whether a
sentence is true. That is what review is for, and it is the harder half.

---

## Documentation claims about other projects

The competitor comparisons in `README.md` follow one rule: **a claim about another project
needs an artifact that was actually fetched, and a link to it.** State the verified fact,
link the source, move on. No characterisation beyond what the artifact shows, no adjectives,
no name-and-shame. If you cannot link to the file or page you read it in, it does not go in.

The same applies to the skill's own copy: no superlatives, no marketing voice. Write like
an engineer explaining their work.

---

## Proposing a new preset

Presets live in `src/ga4/presets.ts`. A preset turns an intent ("what are my top pages")
into a dimension and metric combination that is known to work, so the model does not guess
among roughly 200 dimensions and 150 metrics.

**Every `apiName` must be verified against a live `getMetadata` response.** Not against
Google's documentation tables, not against another plugin's field list, not from memory.
GA4 renames fields (`conversions` became `keyEvents`, `pageviews` became `screenPageViews`)
and both the docs and the model's training data are full of names that no longer resolve.
Two of the research briefs behind this project produced hand-maintained field lists that
disagreed with each other, which is the whole argument for checking against the property.

The easiest check is the skill itself: run `fields` with the field you intend to use and
confirm the exact `apiName` comes back.

For the receipt to paste into the pull request, read the metadata endpoint directly:

```bash
curl -s -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  "https://analyticsdata.googleapis.com/v1beta/properties/YOUR_PROPERTY_ID/metadata" \
  | grep -o '"apiName": *"[^"]*"' | sort -u
```

Then check every name in your preset appears in that output. Paste the matching lines into
the PR description. Names that cannot be confirmed are left out rather than guessed at;
that is why some obvious-looking fields are missing from the existing presets.

A preset PR should also satisfy:

- **An explicit `orderBys`**, unless the preset is a single-row KPI shape (`dimensions: []`
  with `limit: 1`, like `overview` and `sales_summary`). "Top pages" that is not sorted
  server-side is not top pages; it is an arbitrary 25 rows. The failure this guards against
  is real and shipped: `adamkristopher/ga4-api-toolkit`'s `src/api/reports.ts` `runReport()`
  destructures `filters` and `orderBy` and then never puts either in the request, so a
  filtered question returns unfiltered whole-site numbers with no error at all.
- **A test that the request built from the preset carries its dimensions, metrics and sort.**
  Same reason. A preset that is silently dropped on the way to the wire is worse than a
  missing preset.
- **Within the limits** in `src/ga4/limits.ts`: at most 9 dimensions and 10 metrics.
  `assertWithinLimits` will reject more, before a socket opens; Google counts client errors
  against a 10,000-per-15-minutes budget that blocks a whole project-and-property pair when
  exhausted, so an invalid request must never be sent.
- **Realtime presets** (`kind: "realtime"`) may only use the fields in `REALTIME_DIMENSIONS`
  and `REALTIME_METRICS`. The realtime surface is much smaller than the reporting one: no
  page dimensions, no traffic source, no sessions metric.
- **No person-identifying dimension.** `userId`, `signedInWithUserId` and `customUser:*` are
  blocked by `classifyDimension` and are not preset material under any intent.
- **An `intent` line the model reads**, written as a plain statement of what question the
  preset answers. It is a routing input, so make it discriminating: what it returns, and
  when another preset is the better call.
- **A `note`** when the shape needs explaining: an empty result that is normal (`ecommerce`
  without ecommerce events), a `(not set)` row that is expected, or a name that misleads
  (`search_terms` is on-site search, not Google organic queries).

---

## Commit style

Look at `git log` for the pattern. In short:

- **Imperative subject**, no trailing period, describing what the commit does:
  `Add access-token exchange and date-range parsing`. Not "Added", not "Adds", not
  "feat(auth):".
- **The body explains why**, not what. The diff already says what changed. The body is where
  the reasoning that is not visible in the code goes: what alternative was considered and
  rejected, what failure mode the change prevents, what surprising thing about the API forced
  the shape. If a future reader would ask "why on earth is it done this way", answer it here.
- Wrap the body at about 80 columns. Blank line after the subject.
- **Last line is the test count** from the vitest summary, when the commit changed the
  suite. The example below shows the form.
- **No AI attribution.** No `Co-Authored-By` trailers, no "Generated with", no tool
  footers, no emoji. The commit log is a technical record of decisions; whose keyboard the
  characters came from is not part of it.

A concrete example from this repository:

```
Add access policy, request limits, and bundle-surface guarantees

Access policy blocks only dimensions that link a row to an identified person
(userId, signedInWithUserId, customUser:*), and passes those through when
explicitly opted in. Per-call approval prompts for URL-bearing dimensions were
considered and rejected: pagePath appears in the most common question anyone
asks, and a tool that interrupts the most common question stops being used.
Unconditional value redaction covers that case instead.

...

160 tests.
```

Note what that body does: it names the rejected alternative and the reason. That is the part
you cannot reconstruct from the diff, and it is the part worth writing down.

---

## Before you open a pull request

```bash
npm run check
```

In the PR description, say what problem the change solves and what you considered and
rejected. If it touches the network surface, the credential path, or anything in the privacy
table above, say so explicitly at the top; those get read closely.

---

## Trademarks

This is an independent open-source project. It is not affiliated with, endorsed by, or
sponsored by Google LLC. Google Analytics and GA4 are trademarks of Google LLC.
