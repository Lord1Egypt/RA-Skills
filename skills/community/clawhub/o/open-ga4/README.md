# Open GA4

**Ask your OpenClaw agent how your website is doing, and get a straight answer.**

You: *"What were my top pages last month?"*

Your agent runs one command and comes back with this:

```markdown
| pagePath | screenPageViews | activeUsers | userEngagementDuration |
| --- | --- | --- | --- |
| / | 1,842 | 612 | 2h 32m |
| /pricing | 938 | 401 | 1h 27m |
| /blog/how-we-cut-latency | 705 | 388 | 3h 28m |
| /docs/getting-started | 402 | 297 | 2h 13m |
| /contact | 233 | 180 | 24m 0s |
```

No dashboard to open, no report builder, no remembering that "pageviews" is spelled
`screenPageViews` and that "conversions" is called `keyEvents` now.

It reads your Google Analytics 4 data and nothing else. It cannot change anything, and it
never sends your data anywhere except back to you.

## Install

```bash
openclaw skills install @anatoli-iliev/open-ga4
```

That is the whole install. No build step, nothing to compile, no `npm install`. You need
Node 22.22.3 or newer, which OpenClaw already runs on.

Not released to ClawHub yet, so until the first tagged release use one of these instead:

```bash
openclaw skills install git:anatoli-iliev/open-ga4
openclaw skills install /path/to/open-ga4
```

## Set it up by asking

Google's side takes about ten minutes and has one step that almost everybody gets wrong.
So let the agent walk you through it:

> **"Set up my analytics."**

It checks what is missing and gives you one thing to do at a time, with the link to click
and the exact text to paste. Do that step, say you are done, and it checks again. Under the
hood it is reading this:

```json
{
  "ok": false,
  "blocked_on": "no_credentials",
  "next": {
    "where": "your environment",
    "action": "Set GA4_CREDENTIALS to your service-account key's contents, or a path to it, then run doctor again."
  }
}
```

One step, never a wall of errors. When it says `"ok": true`, you are done.

Prefer to do it yourself? [SETUP.md](SETUP.md) has the click-by-click version with console
links. The short form is: create a Google Cloud project, enable the Analytics Data API,
create a service account, download its JSON key, **then grant that service account's email
address Viewer access inside Google Analytics** (Admin, then Property access management).

You can also run the diagnostic yourself, without going through the agent. Ask OpenClaw
where the skill landed, then run it:

```bash
openclaw skills info open-ga4
node <skill-dir>/lib/cli.js doctor
```

Do not hardcode `<skill-dir>`: a `--global` install puts it somewhere else. Every command
below works the same way if you would rather drive it by hand than ask for it.

That last step is the one people miss, because it happens in Analytics and not in Google
Cloud, and skipping it produces a 403 that explains nothing. Ask the agent to run the
diagnostic and it will translate it for you.

## Two settings

```bash
GA4_CREDENTIALS   # your service-account JSON key: paste the contents, or give a file path
GA4_PROPERTY_ID   # your property's 9 or 10 digit number, so you never have to say which site
```

`GA4_CREDENTIALS` takes either form. Pasting the contents is one step instead of three, and
it is what the "Save key" box in the OpenClaw Control UI writes.

The honest trade: pasting puts a private key inside `~/.openclaw/openclaw.json`, and OpenClaw
writes a `.bak` beside that file whenever it changes, so the key ends up in two places
rather than one. Saving the file somewhere private, `chmod 600`, and giving the **path**
keeps it in one. Both work. Pick knowing that.

`GA4_PROPERTY_ID` is the number under **Admin > Property details**, not the
`G-XXXXXXXXXX` from your website's tag. Paste that by mistake and the skill will tell you
which number it actually needs.

## What you can ask

| You say | You get |
| --- | --- |
| "How did my site do last month?" | Users, sessions, engagement, key events, revenue |
| "What were my top pages?" | Most-viewed pages, ranked |
| "Where is my traffic coming from?" | Sources, mediums, channels |
| "Are we up or down on last month?" | Two periods side by side, with the change |
| "Is anyone on my site right now?" | Active users in roughly the last 30 minutes |
| "Which countries? What devices?" | Countries, devices, browsers |
| "How many people signed up?" | Key events and conversions |
| "Is my analytics set up correctly?" | A per-step check naming the first thing that is wrong |

Ask in whatever words come naturally. The agent picks the command; you do not need to know
there are seven of them (`report`, `compare`, `live`, `query`, `fields`, `properties` and
`doctor`), or that `report` has eighteen ready-made reports behind it.

When nothing pre-built fits, `query` takes your own dimensions, metrics, filter and sort
order directly.

## What it will not do

- **It cannot change anything.** The only permission it asks Google for is read-only.
- **It will not tell you about individual people.** `userId` and person-scoped custom
  dimensions are refused unless you deliberately turn them on, and that applies to
  filtering and sorting by them too, not just to asking for them as a column.
- **It masks personal data before your agent sees it.** Email addresses, phone numbers,
  card numbers, tokens and unexpected query-string values in your reports are replaced, and
  the report tells you how many values were masked.
- **It writes no report data to disk.** No cache of your reports, no saved access
  token, no telemetry, no update check. One thing can be written, and only if you ask
  for it: an audit log of what was *asked*, off unless you set `GA4_AUDIT_LOG` to a
  path, and it never records what came back.

## Built to be checked

The reason to trust this is not that the README says nice things. It is that the claims are
small enough to verify and there are tests that fail when one stops being true.

- **Zero runtime dependencies.** Every import is either a relative path or a `node:`
  builtin, and a test fails the build on anything else. The OAuth signature is built with
  `node:crypto`; the API is called with `fetch`. No gRPC stack, no generated protos, no
  Python. There is no `node_modules` to be missing, stale, or compromised, and you can read
  the whole client in one sitting.
- **An egress allowlist enforced in code.** It can only talk to three hosts. One guard
  rejects any host other than `oauth2.googleapis.com`, `analyticsdata.googleapis.com` and
  `analyticsadmin.googleapis.com`
  before a request is made, and treats a redirect as an error rather than following it, so a
  302 cannot reach a host that was never checked. A test scans the shipped code for `https://`
  URLs and fails on any host that is neither one of those three nor on a short reviewed list
  that only ever appears as text: `console.cloud.google.com` and
  `console.developers.google.com` (the "enable the API here" link in an error message),
  `www.googleapis.com` (inside the OAuth scope string), and `analytics.google.com` (the
  Property access management link shown when a grant is missing).
- **Read-only by scope.** Not by promise. The only scope requested is
  `https://www.googleapis.com/auth/analytics.readonly`, and a test asserts no other
  `googleapis.com/auth/` string exists in what ships.
- **What ships is what you can read.** The compiled JavaScript is committed in `lib/`, one
  readable file per source file, because no install route runs a build. Committing build
  output is normally bad practice; the price paid for it here is a CI job that rebuilds from
  `src/` and fails if the committed output differs by a byte, so the two cannot drift apart.
- **Errors name the fix.** A missing grant becomes "add this address in Admin > Property
  access management with the Viewer role". A disabled API becomes the console link that
  enables it. A drifted clock becomes "turn on network time sync" rather than
  `invalid_grant`. Diagnosis reads Google's machine-readable status and reason fields, never
  its prose.
- **Reports say what they do not mean.** Sampling, Google's minimum-aggregation
  thresholding, `(other)` rollups, restricted metrics and the property's own time zone each
  produce one plain sentence, and only when that flag is actually set.

Your credentials go to Google and to no third party. Note that the allowlist governs which
host this skill asks for, not what your machine then does with the request: if you run an
HTTP proxy or a TLS-intercepting middlebox, this traffic traverses it exactly as the rest of
your OpenClaw traffic does.

## Your visitors write some of this data

This is the part most analytics integrations miss, and it is worth understanding before you
wire an agent to act on the numbers.

GA4 dimension values are not written by you. They are written by whoever visited your site.
Anyone can open `yoursite.com/?<any text they like>` and that text appears in `pagePath` in
tomorrow's report. The same goes for `pageTitle`, `pageReferrer`, `landingPage`,
`sessionCampaignName` and every other visitor-derived or marketer-written field. Referrer
spam has been doing exactly this to Google Analytics for over a decade. An agent that reads
those values turns them into a prompt-injection channel.

What separates visitor-authored text from trusted output here is how the output is framed.
Report rows go inside a fenced block introduced as data supplied by site visitors, never
interpolated into a sentence. In every cell of every command a `|` is **replaced** with a
fullwidth one that cannot delimit, and newlines are collapsed, so a value cannot forge table
structure or start a line of its own.

Replacement rather than escaping, for a reason worth recording: escaping `|` as `\|` turns a
value's existing `\|` into `\\|`, which markdown reads as an escaped backslash followed by a
live delimiter. The escape creates the very split it exists to prevent, and a visitor could
use it to shift a column and make a fabricated number look measured. Removing the character
leaves no escape sequence to get wrong.

`fields`, `properties` and `doctor` print field, property and account names in a plain table
without that fence, because those names come from Google and from your own Analytics
configuration rather than from visitors.

This reduces risk. It does not eliminate prompt injection, and nothing does. If you wire an
agent to act on GA4 data (send email, file tickets, change bids), keep a human in that loop.
**The numbers are trustworthy. The strings are not.**

## Privacy

Full detail in [PRIVACY.md](PRIVACY.md). The parts worth knowing up front:

- Redaction is on by default and covers emails, phone numbers, UUIDs, JWTs, card numbers
  confirmed by Luhn, long opaque tokens, and the values of query parameters outside a
  keep-list.
- The four settings that weaken a privacy default (`GA4_REDACT`,
  `GA4_ALLOW_USER_DIMENSIONS`, `GA4_PROPERTY_ALLOWLIST` and `GA4_AUDIT_LOG`) are environment
  variables and deliberately have **no** command-line flag. A flag can be set by the model,
  and a page title is attacker-controlled text that reaches the model. Passing one as a flag
  is refused with an error explaining why.
- The skill never calls `properties.audienceExports`, `properties.audienceLists` or the
  Admin API's `runAccessReport`, the three surfaces built to return rows keyed to an
  individual visitor, and a test asserts those strings are absent from what ships.
- **What this does not protect you from:** the reports your agent reads are seen by whatever
  model provider you have configured. This skill controls what it asks Google for and what
  it hands to your agent. Redaction runs here, on a response that has already arrived on
  your machine in full, so it changes what the model sees, not what Google holds. Choose the
  property, the date range and the provider accordingly.

## How it compares

Both rows are backed by a fetched copy of the other project's code.

| Project | What it does | Here instead |
| --- | --- | --- |
| [`adamkristopher/ga4-api-toolkit`](https://github.com/adamkristopher/ga4-api-toolkit) | `src/api/reports.ts` `runReport()` accepts `filters` and `orderBy`, then never uses them when building the request, so a filtered question quietly returns whole-site numbers. It also defaults `save=true`, writing results to disk. | A parameter this skill cannot honour raises an error naming why, rather than being dropped: asking `overview` for a filter says that report has no dimension to filter on. Nothing writes report data to disk. |
| [`jdrhyne/agent-skills`](https://github.com/jdrhyne/agent-skills) GA4 skill | `skills/ga4/SKILL.md` declares `requires: {"bins": ["python3"]}` and every example runs `python3 scripts/ga4_query.py`. Those scripts tell you to `pip install google-analytics-data google-auth-oauthlib` on the host. | Both are skills, so the comparison is what each one makes you install first. This one requires `node`, which OpenClaw already runs on. No Python, no `pip`, no virtualenv, and zero npm dependencies either, so there is no install step left that can fail. |

## Development

```bash
npm install           # devDependencies only: typescript and vitest
npm run check         # typecheck, then tests, then build
npm test              # vitest, no network, no credentials
```

`npm test` builds first, because `src/privacy/surface.test.ts` asserts the privacy
guarantees against `lib/`, the code that actually ships, rather than against the source.

The test suite lives here and only here. The published skill ships `src/` so its code can
be read, but not the tests: an installed copy has no runner to execute them with, and a
scanner reading the fake credential fixtures in the redaction tests reports them as
findings against the bundle. Clone this repository to run them.

`src/docs.test.ts` and `src/docs/skill.test.ts` check the prose in this file and in
`SKILL.md`: every command quoted must parse, every setup state the code can report must
appear in `SKILL.md`'s tree, every environment variable the frontmatter declares must be one
the code reads and the other way round, and every preset id, npm script and Google host
named anywhere in the documentation must exist. Documentation drifts silently, and a careful
reader is not a control.

If you run the OpenClaw CLI against this repo, use `scripts/openclaw-sandbox.sh`. Several
subcommands boot enough of the runtime to run config doctor and state migrations, which
against a real installation can rewrite your config and relocate your state files. Setting
`OPENCLAW_STATE_DIR` alone is not enough, because migrations still probe the legacy paths
under `$HOME`. The wrapper redirects `HOME`, the XDG directories and the OpenClaw config and
state directories into a throwaway `.sandbox/`.

Design decisions, and what was rejected, are in [docs/DESIGN.md](docs/DESIGN.md) for the
analytics core and
[docs/superpowers/specs/2026-08-16-open-ga4-design.md](docs/superpowers/specs/2026-08-16-open-ga4-design.md)
for the skill packaging.

## License

MIT-0 (MIT No Attribution) © 2026 Anatoli Iliev <anatoli@helphabit.com>. See
[LICENSE](LICENSE).

## Trademarks

This is an independent open-source project. It is not affiliated with, endorsed by, or
sponsored by Google LLC. Google Analytics and GA4 are trademarks of Google LLC.
