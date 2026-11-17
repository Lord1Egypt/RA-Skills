# Security Policy

`open-ga4` runs on your machine, holds a Google credential, and returns data
that strangers on the internet can write into. This document says what it defends
against, how the defence is enforced, and where it stops.

## Supported versions

| Version | Supported | Notes |
| --- | --- | --- |
| 0.1.x | Yes | Current line. Security fixes ship as a patch release. |
| < 0.1.0 | - | No earlier releases exist. |

Fixes land on the newest patch of a supported line. There are no backports to older
patches; upgrade instead.

## Reporting a vulnerability

Use either channel. Both reach the same person.

- **Email** anatoli@helphabit.com, with `open-ga4` in the subject.
- **GitHub private security advisory**:
  <https://github.com/anatoli-iliev/open-ga4/security/advisories/new>

Please do not open a public issue, discussion, or pull request for a vulnerability.

| Stage | Target |
| --- | --- |
| Acknowledgement | 72 hours |
| Severity assessment and a fix plan | 7 days |
| Fix released | 30 days from the report |
| Public advisory | Published with the fix, or later by agreement |

Disclosure is coordinated. The advisory goes out when the fix is available, or sooner
if the issue is already public. If you need more than 30 days for your own reasons,
say so and we will agree a date. You will be credited in the advisory unless you ask
not to be.

Useful in a report: the skill version, the OpenClaw version, Node version, what you
did, what happened, and what you expected. A failing test is the fastest possible
report.

**Do not paste a service-account key, an access token, or a live GA4 report into your
report.** A redacted excerpt is enough, and the key is a password.

Bug bounty: there is no bounty programme. This is an unfunded open-source project.

## Threat model

Six threats, in the order they are worth worrying about. Each says what the skill
does and what it does not do.

Each one names the test that holds it. Those tests are in the repository, not in the
installed skill: the bundle ships `src/` so the enforcing code can be read beside the
`lib/` built from it, but from 0.2.0 it leaves the suite out, because an installed copy
has no runner and a scanner reads the redaction tests' fake credentials as findings
against the artifact. Run them from
<https://github.com/anatoli-iliev/open-ga4/tree/main/src>.

### 1. Credential theft from the key file on disk

**The risk.** The Google service-account JSON key is a password in a file. Anyone who
reads it can read every GA4 property that key has been granted, from anywhere, until
the key is revoked. The same is true of the `authorized_user` file that
`gcloud auth application-default login` writes.

**What the skill does.**

- Reads the credential from where you put it and nothing else: `GA4_CREDENTIALS`
  (holding either the key's contents or a path), `GOOGLE_APPLICATION_CREDENTIALS`, or
  gcloud's application-default file. Nothing is copied, rewritten, or normalised back
  onto disk (`src/auth/credentials.ts`).
- Never writes key material to a log, an error, or a tool result. `redactText`
  (`src/privacy/redact.ts`) strips PEM `PRIVATE KEY` blocks, `Bearer` tokens, and the
  JSON fields `access_token`, `refresh_token`, `id_token`, `private_key`,
  `client_secret`, `api_key` and `apiKey`. It runs unconditionally in `guardedFetch`
  (`src/ga4/http.ts`) and in the error mapper (`src/ga4/errors.ts`). There is no
  config switch, because there is no legitimate reason to surface a key.
- `doctor` reports where a credential was found and whether it parsed: a label, a
  path, and a status. It never prints the contents, and for a value that failed to
  load it does not print the path either, because a value that was supposed to be a
  path may be a mis-pasted key.
- The private key never leaves the process. `node:crypto` `createSign("RSA-SHA256")`
  signs the OAuth assertion locally; the signature goes to Google, the key does not.
- Access tokens live in a variable for their one-hour lifetime and die with the
  process. No token file. A cached Google token on disk is a credential at rest that
  you never agreed to.

**Your part.** `chmod 600` the key file. Keep it out of the repository, out of any
synced or backed-up folder, and out of your shell history. If you paste the key's
contents into `GA4_CREDENTIALS` rather than a path, know where that lands: OpenClaw
stores it in `~/.openclaw/openclaw.json` and writes a `.bak` beside it on every
change, so the key is then in two files rather than one. Delete the key in Google
Cloud when you stop using it; revocation is instant and free.

**Rotating or revoking the key.** Both happen in Google Cloud, not here, and neither
needs this skill's cooperation. Revoking is the emergency move and it takes effect at
once:

1. Open <https://console.cloud.google.com/iam-admin/serviceaccounts>, click the
   `ga4-reader` account, open its **Keys** tab.
2. Delete the key you want dead. Nothing can be signed with it from that moment; an
   access token already minted from it keeps working until it expires, which is at most
   an hour.
3. To cut off access altogether rather than one key, remove the service account's email
   address from Google Analytics instead: **Admin**, then **Property access management**.
   That revokes every key the account has, including any you have forgotten about.

Rotate on the same screen, in this order: **Add key**, **Create new key**, **JSON**;
point `GA4_CREDENTIALS` at the new file; confirm with `doctor --json`; then delete the
old key. That order leaves no window where the skill has no working credential.

Rotate whenever the file might have been seen: a shared or lost machine, a backup you
cannot account for, a key pasted into a chat or an issue, or somebody leaving the
project. A service-account key does not expire, so nothing rotates it for you and an
old one stays valid indefinitely.

**The option with no key file.** If you have the `gcloud` CLI, `gcloud auth
application-default login` avoids a downloadable key entirely. The skill reads that
credential as a fallback, and Google invalidates it when you change your password or
revoke the grant, which is the thing a JSON key on disk cannot offer. It also expires
and needs re-running, which is the trade, and it is why the key file is still the
documented default for someone who wants this to keep working unattended.

**What it does not do.** File permissions are the operating system's job. Anything
running as your user can read your key, with or without this skill.

### 2. Prompt injection through GA4 dimension values

**The risk.** GA4 dimension values are not written by you. They are written by whoever
visited your site. Anyone can open `yoursite.com/?<any text they like>` and that text
appears in `pagePath` and `pagePathPlusQueryString` in tomorrow's report. The same
holds for `pageTitle`, `pageReferrer`, `landingPage`, `searchTerm`,
`sessionCampaignName` and every other visitor-derived or marketer-written field.
Referrer spam has been pushing strings into Google Analytics for a decade for SEO
reasons. An agent that reads those values turns that into a prompt-injection channel.

**What the skill does.**

- Report rows are rendered inside a fenced block introduced, in the text above it, as
  values supplied by site visitors and not to be treated as instructions. Rows are
  never interpolated into prose (`src/ga4/format.ts`). `fields`, `properties` and
  `doctor` list field, property and account names in a plain table without that fence,
  because those names come from Google and from your own Analytics configuration
  rather than from visitors.
- In every table cell of every command, a `|` is replaced with U+FF5C, a fullwidth
  vertical line that cannot delimit, and newlines are collapsed to spaces. One function,
  `tableCell` in `src/ga4/format.ts`, which `src/tools/discovery.ts` imports rather than
  reimplementing, so a value cannot forge a table row or start a line of its own.
  Replacement rather than escaping, and this is the correction of a real defect: both
  renderers used to escape `|` as `\|`, which turns a value's existing `\|` into `\\|`.
  Markdown reads that as an escaped backslash followed by a **live** pipe, so the escape
  manufactured the delimiter it existed to remove. A visitor loading
  `?q=pricing\|999999` put that straight into `searchTerm`, it matched no personal-data
  pattern so redaction passed it through, and `report search_terms` emitted five fields
  under four headers: `eventCount` read 999999 instead of 3 and every later metric
  shifted a place. Removing the character means no escape sequence is involved and there
  is nothing left to order wrongly. `src/ga4/format.test.ts` and
  `src/tools/discovery.test.ts` count the fields in a rendered row for values holding
  pipes and backslashes in every arrangement.
- The header and caveat lines are generated by the skill from Google's
  `ResponseMetaData`, never from row content, so injected text cannot impersonate a
  date range or a warning.
- Redaction runs on every value of every row of a report before the model sees it
  (`src/privacy/redact.ts`), unless you set `GA4_REDACT` to a false value, which turns
  it off entirely and which `doctor` reports as a FAIL. `fields`, `properties` and
  `doctor` return field and property names rather than measurements, and are not
  redacted.
- The four settings that weaken a privacy default (`GA4_REDACT`,
  `GA4_ALLOW_USER_DIMENSIONS`, `GA4_PROPERTY_ALLOWLIST`, `GA4_AUDIT_LOG`) are
  environment variables and have no command-line flag, deliberately. A flag can be set
  by the model, and the text the model is reading was written by site visitors, so a
  flag would make "turn redaction off" reachable from a page title. `src/cli/args.ts`
  rejects every plausible flag spelling of all four with an error saying so, and a
  test enumerates the spellings.
- **What used to be here and is not.** An earlier version of this project was an
  OpenClaw plugin, and every tool registered with `resultContentSource: "network"`,
  the host's marker for externally controlled content. That field is only reachable
  through the plugin registration API, so it went away when the plugin did. It was
  inert regardless: the string occurs zero times in openclaw 2026.7.1-2, the current
  `latest`, and appears only in the 2026.8 line. What is given up is a label that would
  have taken effect on a future host upgrade. The framing and escaping above are what
  separate visitor-authored text from trusted output, as they already were.

**What it does not do.** None of this stops a model from acting on text it read. It
reduces the risk; it does not eliminate it, and nothing does. If you wire an agent to
act on GA4 data (send email, file tickets, change bids), keep a human in that loop.
The numbers are trustworthy. The strings are not.

**In scope for a report:** a dimension value that escapes the fenced block, forges a
header or caveat line, or otherwise breaks the framing. That is a bug in this skill.
**Out of scope:** a model choosing to follow instructions that were correctly framed as
visitor-supplied data.

### 3. Exfiltration through a compromised dependency

**The risk.** The usual way to talk to GA4 is `@google-analytics/data` or
`googleapis`, which bring a gRPC stack, generated protos, and hundreds of transitive
packages. Any one of them can ship a postinstall script or a patched HTTP call, and
the credential is right there.

**What the skill does.**

- **Zero runtime dependencies.** Not one npm package: `package.json` has no
  `dependencies` and no `peerDependencies`, `npm ls --omit=dev --all` prints the
  project and nothing beneath it, and a test fails the build on any import that is
  neither relative nor `node:`-prefixed. OAuth is a signed JWT built on `node:crypto`;
  the GA4 REST API is called with `fetch`. No gRPC, no generated SDK, no
  `google-auth-library`, no Python.
- The egress allowlist (below) means the skill's code has one route to the network and
  it is guarded.
- CI has no credentials and needs none, so a compromised devDependency running in a
  pull-request build has nothing to steal. Workflow permissions are `contents: read`.

**What it does not do.** The allowlist is not a sandbox. It constrains code that goes
through `guardedFetch`; a malicious package inside your Node process can call `fetch`
or `net` directly, and no library-level check can stop it. The real mitigation here is
that there is almost nothing to compromise: no dependencies at all, and an audit of
the whole network path is a morning's reading.

### 4. SSRF and egress to an attacker-controlled host

**The risk.** A URL that reaches an HTTP client from data (a property id, a field
name, a `help.links[].url` inside a Google error payload) is a route out of the
machine, carrying a bearer token in the header.

**What the skill does.** `assertAllowedUrl` in `src/ga4/http.ts` runs before every
request, and `guardedFetch` is the only way out. The check is exact-match on
`URL.host`, and only `https:` passes:

| Host | Why |
| --- | --- |
| `oauth2.googleapis.com` | Exchange a credential for a one-hour access token |
| `analyticsdata.googleapis.com` | `runReport`, `runRealtimeReport`, `metadata` |
| `analyticsadmin.googleapis.com` | `accountSummaries`, the property list `properties` and `doctor` print |

Nothing else, ever. Adding a host is a visible, reviewable diff in one constant.

`src/ga4/http.test.ts` covers the bypasses that matter:

| Blocked | Example |
| --- | --- |
| Unrelated host | `https://evil.example.com/steal` |
| Lookalike suffix | `https://analyticsdata.googleapis.com.evil.example.com/x` |
| Lookalike prefix | `https://notanalyticsdata.googleapis.com/x` |
| A different Google API | `https://gmail.googleapis.com/v1/messages` |
| Userinfo smuggling the real host | `https://analyticsdata.googleapis.com@evil.example.com/x` |
| Non-default port on an allowed host | `https://analyticsdata.googleapis.com:8443/x` |
| Plain HTTP | `http://analyticsdata.googleapis.com/v1beta/x` |
| Non-HTTPS scheme | `file:///etc/passwd` |
| Unparseable input | `not-a-url` |

One test asserts the refusal happens **before** `fetch` is called at all, not after.
The allowlist is checked once, so `guardedFetch` passes `redirect: "error"`: a 302 from
an allowed host is a failure rather than a request to a host that was never checked.
What is fetched is the `URL` object the allowlist was applied to, not the string that
was handed in, so the checked thing and the fetched thing cannot come apart if a future
parser, or an injected `fetch`, parses differently. Separately,
`src/privacy/surface.test.ts` scans every `.js` file in `lib/` for `https://` hosts and
fails on any host that is neither contacted nor an explicitly listed console link shown
to a human.

One URL in a message is not authored here: the `google.rpc.Help` link in Google's error
body, printed into fix text as "enable the API at ...". Nothing fetches it, and it can
only arrive from a host on the allowlist above, so this is not an egress control. It is
still a link somebody may follow because this skill told them to, so it has to be https
on a `google.com` host or the console URL the code already knows is used instead. A
rejected link degrades to a correct one, never to no link.

**What it does not do.** The skill uses the `fetch` it is given. If OpenClaw is
configured with an HTTP proxy, or your machine has a TLS-intercepting middlebox, this
traffic traverses it exactly as all other OpenClaw traffic does. The allowlist
constrains which host the skill asks for, not what your OS and your OpenClaw
configuration then do with the request.

### 5. Over-broad Google permissions

**The risk.** A credential granted more than reporting needs. Write scope, account-level
access instead of property-level, or a Cloud IAM role nobody understands.

**What the skill does.**

- Requests exactly one OAuth scope:
  `https://www.googleapis.com/auth/analytics.readonly`. A test asserts the set of
  `https://www.googleapis.com/auth/...` strings in the shipped bundle is exactly that
  one. Google enforces scope server-side regardless of what a client asks for.
- The complete Google surface is four read methods in one hand-written file
  (`src/ga4/client.ts`): `runReport`, `runRealtimeReport`, `getMetadata`,
  `listAccountSummaries`. There is no generated SDK in which an update could quietly
  introduce `deleteProperty`.
- **It never calls `properties.audienceExports`, `properties.audienceLists`, or the
  Admin API's `runAccessReport`**, the three surfaces built to hand back rows keyed to
  an individual visitor rather than aggregates. `src/privacy/surface.test.ts` walks
  every `.js` file in `lib/` and asserts those strings are absent from the built
  bundle. That test is the whole claim, and it is deliberately narrower than "it cannot
  read per-user data", which would be an overclaim: `runReport` returns per-person rows
  as soon as the `userId` dimension is used, which is why that dimension is blocked by
  default.
- `userId`, `signedInWithUserId` and user-scoped custom dimensions are refused by
  default (`src/privacy/policy.ts`), on every channel that can carry a dimension name
  into a request: the output column list, a `query --filter` field, and a `--sort` key.
  The last two matter most, because neither appears as a column in the answer, so a
  report filtered to one person returns ordinary page paths with nothing in it for
  redaction to catch. Turning them on means setting `GA4_ALLOW_USER_DIMENSIONS` in the
  environment; there is no flag for it.
- The optional `GA4_PROPERTY_ALLOWLIST` refuses any property id you did not list.
- Setup grants **Viewer on one property**, inside Google Analytics under
  Admin > Property access management. No Cloud IAM role is needed and none helps.

**What it does not do.** Scope is a ceiling, not a floor. If you grant the service
account access to your whole Analytics account, the read-only scope still prevents
writes, but everything in that account becomes readable. Grant Viewer, on the
properties you actually want read, and nothing more.

### 6. Supply-chain tampering of the published skill

**The risk.** Someone publishes a build that was not built from this source, or a moved
Git tag silently changes what the release pipeline runs.

**What the skill does.**

- **Pinned CI.** Every GitHub Action in `.github/workflows/ci.yml` is pinned to a full
  commit SHA with the version in a trailing comment. A tag can be moved; a SHA cannot.
  Dependabot proposes updates weekly (`.github/dependabot.yml`) so pinning does not
  mean rotting.
- **Least privilege in CI.** `permissions: contents: read` at workflow level, in both
  workflows, and a test fails if anything wider is ever granted. `.github/workflows/ci.yml`
  uses no secret at all, because the tests need no credentials and no network. The one
  secret this repository has, `CLAWHUB_TOKEN`, exists only in the release workflow, and
  only in the two steps that need it: the one that checks it is configured, and the one
  that publishes.
- **A pinned publisher, and the credential only where it publishes.** Releasing runs one
  external tool, which is also the only thing that ever holds the ClawHub credential. It is
  installed in its own step from `.github/publish/package-lock.json`, committed to this
  repository, with an integrity hash for every package in its tree, with npm lifecycle
  scripts disabled so nothing in that tree can execute during install, and with no secret
  in that step's environment. The next step supplies the token and runs the binary that
  install produced. A single `npx clawhub` invocation used to do both jobs at
  once: that pinned the top-level version and left everything underneath it to be resolved
  by semver range at the moment the release ran, with the token already in scope. Pinning
  the top level is worth little when the resolution that matters is one level down, so the
  publisher gets the same treatment as the actions: resolved once, recorded, and updated
  deliberately by Dependabot.
- **Nothing is published to npm.** `package.json` is marked `private`, and the npm
  package name is abandoned rather than renamed: this is a skill, not a library, and
  nobody should `npm install` it. Distribution is ClawHub and `git`, which copy the
  repository's own files.

- **Committed build output, held honest by a test.** No install route runs a
  build, so the JavaScript that runs is committed in `lib/`, alongside the TypeScript it
  came from, one readable file per source module. Committing build output is normally
  bad practice, and the price of it is a CI job (`.github/workflows/ci.yml`) that
  rebuilds from `src/` and fails if the committed output differs by a byte, so the two
  cannot drift and a hand-edited artifact does not survive a pull request.

**Provenance: the workflow exists, nothing has published under it yet.** Nothing has
been released. `.github/workflows/release.yml` runs only when a GitHub release is
published, never on a push (a publish job that can fire on a push is a foot-gun), and it
stays inert until the `CLAWHUB_TOKEN` secret is deliberately configured. When it runs, it
passes the source repository, ref and commit to `clawhub skill publish` explicitly, so
the listing records which commit produced it. No release has been published yet, so the
workflow has never run: treat anything that claims to be `open-ga4` before the first
tagged release as not from here.

## What is out of scope

These are real considerations. They are not vulnerabilities in this skill, and
reports about them will be closed with a pointer back here.

- **Your own LLM provider seeing report data.** A returned report enters the agent's
  context and is sent to whatever model provider you configured OpenClaw to use, under
  that provider's terms. Returning data to the model *is* the feature. This skill
  controls what it asks Google for and what it hands to the agent; redaction runs here,
  on a response that has already left Google and arrived in full. It has no say in what
  your provider does with a report afterwards. Redaction reduces what is in those
  rows. It does not keep them off the wire. If your threat model excludes your model
  provider, no skill can change that calculus: choose the property, the date range
  and the provider accordingly.
- **Google's own data handling.** What Google collects, retains, samples, thresholds
  or infers about your visitors is between you and Google, and is unchanged by
  installing this. Read Google's own documentation and terms rather than a
  paraphrase here.
- **Anything requiring local access you already have.** Setting `GA4_REDACT` to
  `false` or `GA4_ALLOW_USER_DIMENSIONS` to `true` in the environment, reading the key
  file, or patching the shipped JavaScript. These are safe defaults, not access controls. An
  attacker already executing code as your user can read the credential directly; the
  skill is not the weakest link in that scenario.
- **Findings that require a modified build.** Reports must reproduce against a clean
  checkout or a published release.
- **Aggregate data identifying a person.** "One session, from Reykjavík, on an iPhone,
  that hit `/careers/apply`" is not anonymous in a small enough cohort. Every
  individual field is innocuous and no pattern can fix it. This is a property of
  analytics, not a defect here.

---

This is an independent open-source project. It is not affiliated with, endorsed by, or
sponsored by Google. Google Analytics and GA4 are trademarks of Google LLC.

MIT-0 (MIT No Attribution) licensed. Copyright 2026 Anatoli Iliev <anatoli@helphabit.com>.
