# Privacy behaviour of `open-ga4`

## 1. What this document is

A specification of what the code does, not a promise about what we intend. Every
guarantee names the file that enforces it and the test that proves it. If a claim
here and the code disagree, the code is right and this document is a bug.

| Guarantee | Enforced in | Proven by |
| --- | --- | --- |
| Only three Google hosts are ever contacted | `src/ga4/http.ts`: `assertAllowedUrl` before every `fetch`, and `redirect: "error"` so a 302 cannot reach a fourth | `src/ga4/http.test.ts`, `src/privacy/surface.test.ts` |
| Only one OAuth scope is ever requested | `src/auth/jwt.ts`: one `ANALYTICS_READONLY_SCOPE` constant | `src/privacy/surface.test.ts` |
| The audience-export and access-report surfaces are never called | `src/ga4/client.ts`: five read methods, the whole client | `src/privacy/surface.test.ts` |
| Dimension values in reports are redacted before the model sees them | `src/privacy/redact.ts`, applied in `src/ga4/format.ts` | `src/privacy/redact.test.ts` |
| Person-identifying dimensions are refused by default | `src/privacy/policy.ts`: `assertDimensionsAllowed` | `src/privacy/policy.test.ts` |
| Credentials never reach output, logs or errors | `src/privacy/redact.ts`: `redactText`, called in `src/ga4/http.ts` | `src/ga4/http.test.ts`, `src/privacy/redact.test.ts` |
| No report data is written to disk | the only writer is the opt-in audit log, which records what was asked and never what came back | `src/privacy/surface.test.ts` |

The tests in `src/privacy/surface.test.ts` run against `lib/` (the bundle that
ships), not the source. Intentions do not survive a build; strings do.

**Where the tests named here are.** In the repository, not in the installed skill.
The bundle carries `src/` so the code behind each guarantee can be read next to the
`lib/` built from it, but it stopped carrying the test suite in 0.2.0: an installed
copy has no test runner, so those files could only ever be read there, and a security
scanner reading a deliberately fake credential fixture reports it as a finding against
the artifact you installed. Every test file this document names is at
<https://github.com/anatoli-iliev/open-ga4/tree/main/src>, where `npm install && npm test`
runs it. Reading a test is worth less than running one.

## 2. What leaves your machine

Three hosts, listed as the `ALLOWED_HOSTS` constant in `src/ga4/http.ts`. Every
request goes through `guardedFetch`, which calls `assertAllowedUrl` before it
touches the network.

| Host | Why | What is sent |
| --- | --- | --- |
| `oauth2.googleapis.com` | Exchange a credential for a one-hour access token | Service account: an RS256-signed JWT assertion carrying the service-account email, the single scope, the audience, and issue/expiry times. gcloud user credential: `client_id`, `client_secret`, `refresh_token`. |
| `analyticsdata.googleapis.com` | `runReport`, `runRealtimeReport`, `metadata` | Bearer token, numeric property id, dimension and metric names, date ranges, any filters and sort you asked for, a row limit. |
| `analyticsadmin.googleapis.com` | `accountSummaries`, the property list `properties` and `doctor` print | Bearer token, a page size, and, when the account list runs past one page, the continuation token Google itself returned. Nothing else. |

Never sent, to any host: your conversation, your prompts, the model's output, your
hostname, username, file paths, an install id, a version ping, or anything
resembling telemetry. No code exists that could send them (section 6). Your private
key never leaves the process either: `node:crypto` `createSign("RSA-SHA256")` signs
the assertion locally in `src/auth/jwt.ts`, and the signature goes to Google, not
the key.

The check is exact-match on `URL.host`, and only `https:` passes. Tests cover the
usual bypasses (a lookalike suffix, a userinfo segment smuggling the real host
before an `@`, a different Google API, a non-default port, plain HTTP, a `file://`
URL) and assert the refusal happens before `fetch` is called at all. Redirects are
not followed: `guardedFetch` passes `redirect: "error"`, because the allowlist is
checked once, before the request, and a 302 would otherwise carry it to a host that
was never checked.

**Caveat.** The skill uses the `fetch` it is given. If OpenClaw is configured with
an HTTP proxy, or your machine has a TLS-intercepting middlebox, this traffic
traverses it exactly as all other OpenClaw traffic does. The allowlist constrains
which host the skill asks for, not what your OS and your OpenClaw configuration
then do with the request.

## 3. What this skill cannot do

**Write to Google Analytics.** The only scope requested is
`https://www.googleapis.com/auth/analytics.readonly`, defined once in
`src/auth/jwt.ts`. A test scans the built bundle for every
`https://www.googleapis.com/auth/...` string and asserts the set is exactly that
one. Google enforces this server-side regardless of what the client asks for.

**Reach a write method, because none exists.** `src/ga4/client.ts` is the complete
Google surface used, four read methods: `runReport`, `runRealtimeReport`,
`getMetadata`, `listAccountSummaries`. Adding one more is a visible diff in one
hand-written file; there is no generated SDK where an update could quietly
introduce `deleteProperty`.

**Call the audience-export or access-report endpoints.** The skill never calls
`properties.audienceExports`, `properties.audienceLists`, or the Admin API's
`runAccessReport`, and `src/privacy/surface.test.ts` walks every `.js` file in
`lib/` asserting the strings `audienceExport`, `audienceList`, `runAccessReport`
and `userDataRetention` do not appear.

That test is the whole claim, and it is deliberately narrower than "cannot read
per-user data". It checks four strings in the built bundle; it proves nothing about
rows. `runReport`, which the skill does call, returns a row per person the moment a
`userId` dimension is used. That is why section 5 refuses that dimension by default
rather than leaning on this test.

## 4. What it does to data before you see it

Every dimension value in every report passes through `redactValue`
(`src/privacy/redact.ts`) as the report is rendered in `src/ga4/format.ts`. That is
the last point at which a stray email in a URL can be stopped, so it runs on every
row returned by `report`, `compare`, `live` and `query`, unless you turn it off.

The other three commands do not render reports and do not go through `format.ts`,
so their output is not redacted. `fields` returns GA4 field names and Google's own
descriptions of them; `properties` and `doctor` return the property ids, property
names and account names the credential can reach, plus one active-user count. All
three take `|` out of their table cells and collapse newlines, using the same
`tableCell` function report rows go through, but nothing in any of them is matched
against the patterns below.

| Masked | Recognised as | Replaced with |
| --- | --- | --- |
| Query-parameter values not on the keep list | anything after `=` in the query string, and in a `#` fragment, where implicit-flow tokens land | `[redacted]` |
| JWTs | `eyJ…` with three base64url segments | `[redacted:jwt]` |
| Email addresses | plain, and with the `@` percent-encoded as `%40` or doubly as `%2540` | `[redacted:email]` |
| UUIDs | RFC 4122 versions 1–8 | `[redacted:uuid]` |
| Phone numbers | E.164 (`+14155552671`) and `(415) 555-2671` | `[redacted:phone]` |
| Long opaque tokens | 32+ characters of `[A-Za-z0-9_-]` with at least one digit and one letter | `[redacted:token]` |
| Card numbers | 13–19 digit runs that pass a Luhn check | `[redacted:card]` |

This is a list of patterns, not an understanding of your data. A format it does not
know (an internal reference id, a name in a page title, a national identifier)
passes through untouched. Section 7 says more about what that costs you.

The pattern list is fixed. `redactValue` still takes an `extraPatterns` argument
(masked as `[redacted:custom]`) and a `keepQueryParams` list, but nothing supplies
anything other than the defaults below: the plugin config block that used to carry
them died with the plugin, and there is no environment variable in its place. Adding
your own patterns today means editing `src/config.ts`.

Query strings are handled as raw text rather than round-tripped through `new URL()`,
which re-encodes relative paths into something you no longer recognise. Identifiers
sitting in a *path* segment are caught by the pattern list instead.

Deliberately **not** masked:

- **GA4 sentinels**: `(not set)`, `(other)`, `(none)`, `(direct)`, `(no data)`,
  `(not provided)`. Literal strings GA4 emits; they carry no identity.
- **The default kept query parameters**: `utm_source`, `utm_medium`, `utm_campaign`,
  `utm_term`, `utm_content`, `utm_id`, `page`, `q`, `query`, `search`, `sort`,
  `category`, `lang`, `locale`, `ref`, `source`: what marketing reports are *about*.
  Patterns still apply inside a kept parameter: `?q=ada@example.com` becomes
  `?q=[redacted:email]`.
- **Long digit runs that fail Luhn.** The Luhn check exists so
  `/product/1234567890123456` survives while `/receipt/4242424242424242` does not.
  Without it, ordinary SKUs and order numbers get mangled, reports become useless,
  and people switch redaction off, a worse outcome than a slightly leakier default.

Redaction is idempotent, so re-rendering a row does not double-mask it, and it counts
what it masked: a report containing masked values says how many, rather than leaving
the model to infer it from a `[redacted:email]` in a cell. Metric values are numbers
and are not redacted; column headers are GA4 field names and are not redacted.

Separately and **not configurable**: `redactText` strips PEM private-key blocks,
`Bearer` tokens, and the JSON fields `access_token`, `refresh_token`, `id_token`,
`private_key`, `client_secret`, `api_key` and `apiKey` from every error and log line.
Applied in `guardedFetch` (`src/ga4/http.ts`) and in the error mapper
(`src/ga4/errors.ts`). There is no legitimate reason to surface a credential, so
there is no switch.

## 5. What is blocked outright

`src/privacy/policy.ts` refuses certain *questions* before a request is spent. Blocked
by default: `userId`, `signedInWithUserId`, and any dimension whose name begins
`customUser:`, the prefix GA4 gives user-scoped custom dimensions, so one created on
your property after this skill shipped is blocked too, with no skill update.

**Blocked wherever the name appears, not only in the output columns.** A dimension name
reaches a request through three channels: the column list (`--dimensions`), a filter
field (`query --filter userId:exact:...`), and a sort key (`--sort userId`). All three go
through the same check. This is worth stating because only the first is obvious, and the
other two are the dangerous ones: a filter is what selects *which* rows a report
describes, and the filter field never appears as a column, so a report filtered to one
person comes back as ordinary page paths and dates with nothing in it to redact. That
was a real hole in this skill, closed in `buildFilters` and `buildOrderBys`
(`src/ga4/filters.ts`) rather than at their call site, so a future caller inherits the
check instead of having to remember it. The refusal says so in as many words: filtering
on a person-identifying dimension is a request for person-level data even when that
dimension is not among the columns. Tests in `src/tools/reports.test.ts` pin all three
channels, including the two sharpest shapes of the bypass (an existence check for one
id, and a `begins_with` walk that enumerates ids a character at a time).

`src/runtime.ts` also reads the property's live metadata and hands `classifyDimension`
the names *that* property treats as person-identifying, which is more than the rules
above can know:

- Its user-scoped custom definitions. These all carry the `customUser:` prefix, so here
  the metadata confirms the prefix rule rather than extending it.
- Every **deprecated alias** of anything the rules block. `getMetadata` returns
  `deprecatedApiNames` alongside `apiName`, and Google still accepts the old spellings,
  so a name-based check that ignores that field is complete only by luck. Both
  directions are covered: an old alias of `userId`, and a *new* name whose deprecated
  alias is `userId`, which is the same column under a name the rules have never heard
  of. A dimension's names stand or fall together.

If the metadata call fails, the rules above still apply: they are the gate, and this
sharpens it. What is lost is the property-specific extra.

The refusal names the exact setting that lifts it, the `GA4_ALLOW_USER_DIMENSIONS`
environment variable, and suggests `totalUsers` or `activeUsers`, which answer "how
many people" without naming anyone; a test asserts the message contains both. The
optional `GA4_PROPERTY_ALLOWLIST` refuses any property id you did not list.

Both are environment variables and neither has a command-line flag, deliberately.
So do `GA4_REDACT` and `GA4_AUDIT_LOG`. These four are the settings that weaken a
default, a flag can be set by the model, and the values the model reads are authored
by site visitors; an environment variable is set by a person. `src/cli/args.ts`
rejects every plausible flag spelling of all four with an error saying so.

**Why URL-bearing dimensions are not gated.** The obvious alternative is to prompt for
approval whenever a query touches `pagePath`, `pageLocation`, `searchTerm` and
friends, since those are where leaked identifiers actually live. We rejected it. "What
are my top pages?" is the single most common question anyone asks an analytics tool,
and a tool that interrupts the most common question is one people stop using, or one
where they click through the prompt unread, which is worse than not prompting. Those
dimensions are allowed and redaction runs on every value of every row instead. A test
in `src/privacy/policy.test.ts` pins the choice: *"permits free-text dimensions, which
are redacted rather than blocked"*.

Those same values are visitor-authored (anyone can put a string in your `pagePath` by
visiting a URL, and anyone holding your measurement id, which sits in the tag on your
own site, can send an arbitrary `eventName` straight to Google's collect endpoint), so
report rows are rendered inside a fenced block introduced as untrusted data rather than
interpolated into prose. Which dimensions this applies to is not a list anybody can
finish, so nothing is built on one: redaction runs on every value of every dimension
column and the untrusted framing is attached to every row, whatever the dimension is
called. `policy.ts`'s free-text list records the ones that are known, for documentation
and for the `fields` listing, and says in as many words that it is not exhaustive. That fenced, labelled block is
the whole of it. An earlier version of this project was an OpenClaw plugin and also
marked every result with `resultContentSource: "network"`, the host's marker for
externally controlled content; that field is only reachable through the plugin
registration API and went away with the plugin. It was inert in any case: the string
does not occur anywhere in openclaw 2026.7.1-2, the newest released host. What is
lost is a label that would have taken effect on a future host upgrade. A mitigation,
not a solution.

## 6. What is stored

Nothing.

- **No report cache.** Rows are rendered and returned, never written.
- **No token file.** Access tokens live in a variable in `src/auth/token.ts` for their
  one-hour lifetime and die with the process. A cached access token on disk is a
  credential at rest the user never agreed to.
- **No credential copy.** A credential file is read from wherever you pointed the skill,
  and a pasted key is read out of the environment. Neither is copied, rewritten, or
  normalised back onto disk by this skill. Note the one place a key does come to rest
  that is not of this skill's making: if you paste the key's *contents* into
  `GA4_CREDENTIALS` through OpenClaw, OpenClaw stores it in `~/.openclaw/openclaw.json`
  and writes a `.bak` beside that file on every change. Setting `GA4_CREDENTIALS` to a
  path instead keeps the key in the one file you chose.
- **No telemetry.** No analytics, no crash reporting, no phone-home, no update check.
  The allowlist makes this structural: there is no host it could reach.
- **In memory only, per process**: one access token, and a `Map` of GA4 field metadata
  keyed by property id. Metadata is schema (the names of your dimensions and metrics),
  not measurements.

`src/privacy/surface.test.ts` asserts no shipped file outside the audit-log module
contains `writeFile`, `appendFile`, `createWriteStream` or `mkdir`.

**The audit log is the one exception, and it is off by default.** Set the
`GA4_AUDIT_LOG` environment variable to a path and the skill appends one JSON line per
report the agent runs (`report`, `compare`, `live` and `query`), recording the time,
the property id, the command, the dimensions and metrics asked for, the **field names**
any filter narrowed the report to and any sort ordered it by, the date range, and how
many rows came back. It records no response bodies, no row values and no
totals: a count of rows, never the rows. The log's `tool` field holds the command name
exactly as it is typed, so a line reads back as the thing that was run. `fields`,
`properties` and `doctor` are not logged. The log covers the reports the agent asked
for, not setup and discovery, and `doctor` does run one live `activeUsers` query as its
Data API check, so if you need a record of every Data API call this file is not it.

**It records filter field names and never filter values, deliberately.** A filter is
what selects which rows a report is about, and the field it selects on is not one of
the columns that comes back, so a line naming only the columns cannot tell a whole-site
page report apart from the same report narrowed to one named person. The field name is
what makes that visible. The value is not recorded, because the value is the person: it
is the customer id, the email, or the URL with a token in it, and writing it here would
put exactly the data this skill keeps off disk into the file you enabled in order to
feel safer. So a line says a report was filtered on `userId`, and never to which
`userId`. `src/privacy/audit.test.ts` asserts the whole key set of a written line, so a
value cannot be added to it quietly.

It exists so you can answer "what did the agent look at last Tuesday" without keeping
the data itself. If the file cannot be written the skill warns and continues, because
losing a log line is a smaller failure than losing the answer.

## 7. The limits of these guarantees

Everything above concerns the boundary between your machine and Google. It does not
cover the following, and no amount of code in this repository could.

- **Report data goes to your LLM provider.** A returned report enters the agent's
  context and is sent to whatever model provider you configured OpenClaw to use, under
  that provider's terms, not ours. Redaction reduces what is in those rows; it does not
  keep them off the wire. Returning data to the model *is* the feature. If your threat
  model excludes your model provider, this skill does not change that calculus.
- **Aggregate data can still identify people.** "One session, from Reykjavík, on an
  iPhone, that hit `/careers/apply`" is not anonymous in a small enough cohort, and no
  pattern can fix it, because every individual field is innocuous.
- **Redaction is pattern-based and will miss things.** It does not catch a name in a
  page title, a 20-character internal reference with no digits, a birthdate, or a
  format invented at your company last month. The skill does not know what your
  identifiers look like, and there is currently no setting that teaches it: the
  pattern list is what ships.
- **Google's thresholding is Google's.** When Google withholds rows covering very few
  users, the skill surfaces that as a caveat and tells you to read the totals as lower
  bounds. It cannot say which rows were withheld or how many, because Google does not,
  and it cannot turn the behaviour on or off.
- **Redaction does not change what Google holds.** Masking happens on the way out of
  the skill, on data Google already stored. If your site sends emails to GA4 in a URL,
  that is still true after you install this; the fix is on your site.
- **Visitor-authored values are attacker-controlled input.** Anyone can make a string
  appear in tomorrow's `pagePath` report by visiting a URL on your site. Framing rows
  as untrusted data helps. It is not a complete defence against prompt injection, and
  nothing is.
- **Local configuration is as trusted as your machine.** Anyone who can set
  environment variables for the process can set `GA4_REDACT` to `false` or
  `GA4_ALLOW_USER_DIMENSIONS` to `true`. These are safe defaults, not access controls.
  Keeping them out of the command line stops a page title from reaching them, because
  a value in a report cannot become a flag. It does not stop whoever controls the
  environment the skill runs in, and in an agent setup that is not only the person at
  the keyboard: an agent that can edit its own configuration or export a variable
  before invoking the skill is in that set too. What the skill can do about it, and
  does, is refuse to hide it: with redaction off, every report carries a caveat saying
  so and `doctor --json` reports it in `warnings`.
- **This is not legal advice or a compliance product.** No claim is made about your
  obligations under any privacy regime.

## 8. How to verify all of this yourself

From a clone of the repo, about five minutes:

```bash
# The egress allowlist, in full, in the file that enforces it.
grep -n -A6 'ALLOWED_HOSTS' src/ga4/http.ts

# Every https host in the built bundle. Expect six lines: the three above,
# www.googleapis.com (only ever inside the OAuth scope identifier), and
# console.cloud.google.com, which src/ga4/errors.ts prints as the "enable this
# API" link and never fetches, and analytics.google.com, which src/setup/state.ts
# prints as the Property access management link. Neither is on the allowlist, so
# a request to either would be refused.
npm run build && grep -rhoE 'https://[a-z0-9.-]+' lib | sort -u

# Every OAuth scope in the source. Expect three lines: the constant in
# src/auth/jwt.ts, and the two tests that pin it.
grep -rn 'googleapis.com/auth' src

# The audience-export and access-report endpoints. Expect three hits, all in
# src/privacy/surface.test.ts, the test that asserts they are nowhere else,
# and nothing at all from lib/.
grep -rn 'audienceExport\|audienceList\|runAccessReport' src lib

# Anything that writes to disk. Expect three hits: two in src/privacy/audit.ts,
# which is the audit log, and one in src/privacy/surface.test.ts, the test that
# names these APIs in order to assert nothing else calls them.
grep -rn 'writeFile\|appendFile\|createWriteStream' src

# The structural guarantees, asserted against lib/ rather than src/. Expect
# both to pass. No test needs a network connection or a Google credential.
npx vitest run src/privacy/surface.test.ts && npm test

# The entire authentication path: key handling, signing, scope.
wc -l src/auth/jwt.ts src/auth/credentials.ts src/auth/token.ts

# The complete runtime dependency tree.
npm ls --omit=dev --all

# Every import in the shipped source. Expect nothing but relative paths and
# node: builtins.
grep -rhoE "from \"[^\"]+\"" src --include="*.ts" | sort -u
```

The last two commands are the dependency policy. `npm ls --omit=dev --all` prints the
project and nothing beneath it, because there are **zero runtime dependencies**: no
`dependencies`, no `peerDependencies`, and every import is either relative or
`node:`-prefixed. A test asserts both halves, so this cannot quietly stop being true.
That is the point: auditing this skill's network and data behaviour is a morning's
reading, not a supply-chain investigation.

---

Not affiliated with, endorsed by, or sponsored by Google. Google Analytics and GA4 are
trademarks of Google LLC.

MIT-0 (MIT No Attribution) licensed. Copyright 2026 Anatoli Iliev <anatoli@helphabit.com>.
