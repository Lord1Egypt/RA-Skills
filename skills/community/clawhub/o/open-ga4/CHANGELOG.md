# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Nothing yet.

## [0.2.1] - 2026-08-19

Two wording corrections, both from ClawHub's review of 0.2.0, neither changing
what any command does. Both are cases where the text was stronger than the
truth, or told somebody to do something more dangerous than it needed to.

### Fixed

- **"It writes nothing to disk" was not true, and one place said so in the same
  breath as itself.** The claim appeared in README.md, PRIVACY.md and SKILL.md,
  and it is false the moment `GA4_AUDIT_LOG` is set, because the audit module is
  a write path. PRIVACY.md's table contradicted itself inside a single row: the
  guarantee column said nothing is written while the column beside it said "no
  writer exists outside the opt-in audit log". README.md was the worst of the
  three, because the bare sentence sat in the list of reasons to trust the skill
  with no exception named anywhere near it. The claim is now narrowed to what
  holds under every setting, that **no report data** is written to disk (no row,
  no value, no total), with the audit log named alongside it and what it does and
  does not record. A test keeps the exception in the same table row, list item or
  paragraph as the claim, so it cannot drift into another section where a reader
  will not meet the two together.
- **The clock-skew fix no longer hands over a privileged command to paste.** It
  used to read "Paste, on Linux: `sudo timedatectl set-ntp true`", in SKILL.md,
  in SETUP.md, in the CLI's error message and in `doctor`'s output. The command is
  still named, because it is the answer on Linux and withholding it would leave
  somebody stuck on a real problem that looks exactly like a bad key. What changed
  is that it is offered rather than prescribed: the operating system's Date & Time
  setting comes first, the command is presented with what it needs
  (administrator rights) and whose job it is (the user's, not the agent's), and
  `sudo` is not written out to be pasted unread. Two tests hold this against the
  built output, one that no privileged command is prescribed anywhere in `lib/`,
  and one that the fix is still named and still says what it costs, so the
  message cannot be sanitised into uselessness instead.

Deliberately not changed: the remaining review findings ask for the ambient
gcloud credential fallback to be removed, for setup diagnostics to stop being
agent-driven, for property enumeration to be dropped, and for network egress to
be declared in a manifest field that OpenClaw's frontmatter does not have. The
first three are the features, not accidents, and the fourth cannot be expressed.

`.github/workflows/release.yml` runs whenever a GitHub release is published: it
verifies the build, then publishes to ClawHub with the source commit recorded. It
has still never run. Both releases so far were published from a maintainer's
machine with `clawhub skill publish`, so `CLAWHUB_TOKEN` remains unconfigured and
whoever cuts the first GitHub release is the one who finds out whether it works.

## [0.2.0] - 2026-08-19

Answers the six findings and four static-analysis reports from ClawHub's security
review of 0.1.0, which had recommended against installing it. No command changed,
and nothing about what the skill sends, returns or refuses is different. What
changed is a dependency floor, what the bundle contains, and how honestly the
skill describes itself before you agree to run it.

### Security

- **The declared floor for `vitest` was below the fix for CVE-2026-47429**, an
  arbitrary file read and execute that applies when the Vitest UI server is
  listening. It is a development dependency and never in the installed runtime
  path, and the committed lockfile already resolved 3.2.7, which is patched. But
  `^3.2.0` spanned the vulnerable range, and neither a scanner nor a careful
  person reading the manifest can tell a patched resolution from a permitted
  vulnerable one. The floor is now `^3.2.7`, above the whole advisory, and
  `npm audit` reports nothing.
- **The test suite no longer ships in the published bundle**, which drops it from
  105 files to 80. The tests were never runnable from an installed copy, since it
  has no test runner, no `vitest.config.ts` and none of the paths two of them
  read, so they shipped to be read rather than run. Read by a scanner instead,
  they produced four CRITICAL findings against the artifact a user installs, and
  all four were false positives in test code: `child_process` calls that exercise
  this repository's own build script and release workflow, and the deliberately
  fake credentials that the redaction tests cannot do without, a test proving a
  bearer token gets redacted having to contain a bearer token. `src/` still ships,
  so the code behind every guarantee can still be read beside the `lib/` built
  from it. The tests are in the public repository, where they run rather than only
  being read, and PRIVACY.md, SECURITY.md and README.md now say so and link there.
- **Rotating and revoking the service-account key are now documented**, with the
  steps and the order. The review's remaining findings were both about the same
  thing: a service-account JSON key is a persistent credential, and while the
  documentation already steered towards storing it as a `chmod 600` path rather
  than pasting its contents into config, it said only that revocation is "instant
  and free" without saying how. SECURITY.md now gives the console steps, says that
  removing the account's email from Google Analytics revokes every key at once
  including forgotten ones, notes that a key never expires so nothing rotates it
  for you, and puts new-key-before-old-key-deleted in an order that leaves no
  window without a working credential. It also names the option with no key file
  at all, `gcloud auth application-default login`, and says what the trade is.

### Changed

- **The frontmatter description no longer implies the skill stays on your
  machine.** It said "Read only, runs on your machine, no Python", which reads as
  nothing leaving the machine, while every command in fact signs a credential,
  calls Google over HTTPS and returns rows into the conversation. It now says
  "Read-only; calls Google's Analytics API with your credential and returns the
  rows here". Read-only was accurate and is kept; local-only was never claimed on
  purpose and is now not implied.
- **SKILL.md opens with a "What leaves the machine" section**, so the agent can
  answer the question before running anything: the three hosts, the one
  `analytics.readonly` scope, `assertAllowedUrl` and `redirect: "error"` as what
  stops a fourth, report rows entering the model provider's context, the audit log
  as the single disk write and only when `GA4_AUDIT_LOG` names a path, `doctor`
  reading local configuration without printing the credential, and `properties`
  enumerating what the credential can reach unless `GA4_PROPERTY_ALLOWLIST` narrows
  it.
- **SETUP.md asks you to name the skill when starting setup by voice**, "use
  open-ga4 to set up my analytics" rather than a bare "set up my analytics", and
  says why: a generic phrase can pull in whichever skill matches, and `doctor` is a
  real check that reads your configuration and credential file rather than a menu,
  so it should run when you decide it runs.

Not changed, deliberately: no permissions block was invented for the frontmatter.
The review asked for outbound network access to be declared in metadata, and the
OpenClaw frontmatter schema has no field for it. Every environment variable the
skill reads is already declared in `envVars`, the egress allowlist is stated in
SKILL.md, README.md and PRIVACY.md and pinned against the built output by
`src/privacy/surface.test.ts`, and a key that nothing enforces would look like a
sandbox guarantee while being a comment.

## [0.1.0] - 2026-08-14

First release. An OpenClaw skill: a folder with `SKILL.md` at its root and
runnable JavaScript beside it, installed with `openclaw skills install` and
needing no build step and no `npm install`.

An earlier draft of this release was an OpenClaw plugin, installed by cloning
the repository, running a build, and hand-editing a plugin entry into
`openclaw.json`. Every one of those is a step the intended audience does not
take, so the packaging changed and the analytics core did not.

### Commands

- `report`: 15 preset reports (overview, daily trend, top pages, landing
  pages, traffic sources, channels, countries, devices, browsers, events, key
  events, ecommerce, sales summary, new vs returning, site search terms), each
  using dimension and metric names verified against Google's published schema.
- `compare`: the same reports across two consecutive periods of equal
  length, for questions about change rather than level.
- `live`: active users in roughly the last 30 minutes, by country,
  screen or event.
- `query`: explicit dimensions, metrics, filter and sort order, for
  anything the presets do not cover.
- `fields`: searches the property's live metadata, so custom dimensions
  and metrics defined on that property are found without a skill update.
- `properties`: every property the credential can read, with its numeric id.
- `doctor`: setup checks in dependency order, each naming its own fix. Only a
  credential that cannot be found or read stops the run, because nothing after
  it can be checked without one. With `--json`, the single next thing the user must do, as a
  `blocked_on` state with a link and the exact string to paste, plus a
  `warnings` array for anything worth saying that is blocking nothing.

### Privacy and security

- Egress allowlist of three `googleapis.com` hosts, enforced before any request
  is issued. Covered by tests for lookalike domains, userinfo smuggling and
  non-default ports.
- Redaction of dimension values, on by default and turned off only by setting
  `GA4_REDACT`: emails (including percent-encoded), UUIDs, JWTs, long opaque
  tokens, Luhn-valid card numbers, E.164 phone numbers, and the values of query
  parameters outside a keep list. With it off, every report says so in its
  caveats and `doctor --json` says so in `warnings`.
- Unconditional stripping of credentials from every error message and warning
  the skill prints, which no setting can turn off.
- Person-identifying dimensions (`userId`, `signedInWithUserId`,
  `customUser:*`, and any user-scoped custom definition the property reports)
  are refused unless explicitly enabled.
- Optional per-property allowlist.
- Optional local audit log recording what was asked, never what came back.
- The four settings that weaken a privacy default are environment variables
  with no command-line equivalent, because a flag can be set by the model and
  the values the model reads are written by site visitors. Passing one as a
  flag is refused with an error saying so.
- Read-only by scope: `analytics.readonly` and nothing else.
- Tests assert against the built bundle that no per-person Google API surface
  (`audienceExports`, `audienceLists`, `runAccessReport`) is referenced, that no
  other OAuth scope appears, and that nothing writes to disk outside the audit
  log.
- Report rows are rendered inside a fence introduced as data supplied by site
  visitors, because GA4 dimension values are written by whoever visits the site
  and are an injection channel.
- No telemetry. Access tokens are held in memory only.

### Notes

- Zero runtime dependencies: no `dependencies`, no `peerDependencies`, and
  every import either relative or a `node:` builtin. OAuth assertions are
  signed with `node:crypto`; the API is called with `fetch`.
- Exit codes are a contract, since an agent reads them to decide what to say:
  0 worked, 1 an internal failure nothing can name, 2 the query is wrong, 3
  setup unfinished, 4 Google refused for a reason that is not about the query.
  The code says what to do next, not which side of the network decided it: a
  privacy refusal made here and Google's own "that query is invalid" both exit
  2 because the answer to both is to change the query, while a measurement id
  in GA4_PROPERTY_ID exits 3 (it is a setup step, and doctor has an answer for
  it) and a request the egress guard blocked exits 1 (it can only mean a defect
  in the skill). Every message says where the decision was made, so a refusal
  made on this machine is never relayed as Google's.
- Errors are diagnosed from Google's machine-readable `status` and `reason`
  fields, never from its message prose. Clock skew is detected from the
  response `Date` header and reported as clock skew rather than as a bad
  credential.
- Relative date ranges are sent as GA4 relative tokens so Google resolves them
  in the property's own time zone. A range counted back in days (`last 7 days`,
  `N days`) ends yesterday, never today, because today is partial and including
  it makes a period comparison misleading. The "so far" ranges (`this week`,
  `this month`, `this year`) do run to today and say so in their labels, as
  does `today` itself.
- Retired metric names are rewritten to their replacements
  (`conversions` becomes `keyEvents`) and the rewrite is reported.
- Licensed MIT-0, matching what ClawHub serves, so the licence a user receives
  is the licence in the repository.

[Unreleased]: https://github.com/anatoli-iliev/open-ga4/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/anatoli-iliev/open-ga4/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/anatoli-iliev/open-ga4/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/anatoli-iliev/open-ga4/releases/tag/v0.1.0
