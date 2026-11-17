# Recover an unavailable page

Use this in every research mode when a requested source will not load. This is
an agent workflow over the existing browser tools, not an automatic retry daemon.
Keep the selected browser, profile, transport and original source identity.

## Classify before repeating a read

Preserve the actual URL, time and browser/tool error under `raw/`. Import a valid
site snapshot before the next read, as described in [browser-fallback.md](browser-fallback.md).
If navigation failed without a valid site snapshot, retain the original tool
failure and record it in `recovery.md`; do not manufacture an empty successful
capture. A browser error page is not evidence that a search found zero jobs.

| Observation | Next action |
|---|---|
| Login wall, CAPTCHA, 401/403/429 or other site refusal | Stop this site across all tools and follow [user-recovery.md](user-recovery.md). No network retry or proxy change to get past it. |
| Browser/CDP connection unavailable | Check the selected connection locally under [daily-browser.md](daily-browser.md). Do not infer a website problem or restart a shared browser/daemon. |
| Page still loading or rendering | Wait in the same task-owned tab for up to 15, 30, then 60 seconds. Inspect after each stage, stop when the requested content renders, and stop immediately on a login or human-verification wall. Do not reload merely because rendering is slow or interpret missing fields as zero results. |
| Explicit DNS, connection, TLS, address-unreachable or timeout error | Follow the bounded sequence below. An error name identifies a symptom, not its cause. |
| Blank page or unexplained failure | Inspect the current tab and available task-specific error/resource evidence once. If the cause remains unknown, disclose it; do not assume a VPN problem. |

## Bounded network recovery

1. Allow at most **three attempts total**, only for transport failures with no
   refusal signal. Retain the original URL and existing browser/profile, and
   increase the per-attempt wait budget from 15 to 30 to 60 seconds. Preserve
   and inspect each failure before the next attempt; do not stop after just the
   first timeout. A page that already exists should use the rendering waits
   above instead of repeated navigation. Inspect OpenCLI's retained trace when
   a generic timeout may hide a login or human-verification page.
2. Check only relevant local state: whether the selected browser uses a proxy,
   VPN or domain split-routing rule, and which route the failed hostname takes.
   Use observed task-page resource hosts when a shell loads but content does not.
   Do not read unrelated browsing history, cookies, credentials or full secret
   configuration dumps. A VPN being connected alone does not prove causation.
3. If evidence points to a route problem, explain the proposed exact host/suffix
   change. Existing explicit authorization for that routing repair is sufficient;
   otherwise ask before changing network configuration. Back up the relevant
   rule, make the smallest reversible change and verify the effective route.
   Do not disable the user's VPN, reset global proxy settings, disable TLS
   validation or add broad CDN/provider domains just to make one source load.
4. Within the same three-attempt limit, after one authorized repair make at most **one verification read** of the
   original failed URL, using the same browser/profile. Preserve and classify its
   result before continuing. If it fails again, stop recovery for that source,
   report the remaining gap and continue independent authorized sources. A newly
   observed refusal takes precedence immediately.

The limit is the initial attempt plus at most two further network attempts per
failed URL in this consultation, including attachment navigation/download and
other workers/tools. Do not reset it by changing the backend or workspace. All
reads still consume the existing site/page/detail budgets; when those are
exhausted, this workflow grants no additional reads. A loading-state observation
does not grant another navigation attempt.

The bundled reader preserves the actual DOM after its final rendering deadline,
including `load_timed_out` and the attempted wait budgets. An incomplete load
with no extracted rows is a transport result, not a successful empty search.
When a page shell loads before the job body, use `--wait-for-text` with the
observed description heading; `document.readyState` alone does not prove that a
client-rendered job description is present. A preserved page still needs its
normal region, identity and full-description checks before customer delivery.

In `recovery.md`, record attempts, exact errors, diagnostic evidence, any user
authorization and route change, and the final result. Preserve failure evidence
even after success. A successful retry establishes access now; it does not prove
the original cause. An accessible announcement does not establish that its
attachment, job-specific requirements or salary were verified. Report those
separately, offering an official alternate source or a user-provided document
when useful.
