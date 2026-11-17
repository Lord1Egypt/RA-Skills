# Daily browser and concurrent research

## CDP only, after OpenCLI diagnosis

For browser reads, use a supported CDP connection to the user's daily browser
and profile, retaining that profile's existing login state. Public APIs, AnySearch
and static pages need no browser. AnySearch uses its HTTP API, not CDP.
Use a separate or isolated browser only if the user explicitly requests one;
connection failure does not authorize switching away from the daily browser.
Follow an explicitly selected browser. Verify
browser/profile identity before reading: a host's default may be an isolated
agent browser or an in-app browser. Do not silently use those as the daily browser.
If multiple daily profiles remain ambiguous, ask which one to use.
Never use browser extensions, including ones already installed. The browser
fallback is bundled in job-hunt; no external browser skill is needed. Run the
OpenCLI capability diagnosis first, following
[browser-fallback.md](browser-fallback.md).

1. Reuse an authorized CDP connection to the intended daily browser.
   Verify the transport and browser/profile identity before use.
   Open only task-owned tabs and retain their IDs. Do not read unrelated
   tabs, history, credentials or cookies to establish access.
2. Use the bundled `scripts/browser_cdp.mjs` for diagnosed fallback reads.
   It discovers only the selected Chrome or Edge's `DevToolsActivePort`, creates
   a task-owned tab through browser-level CDP and reads the URL. It closes the
   completed task tab, but hands a login or verification page to the user and
   leaves that page open and visible.
   Select `--browser chrome` or `--browser edge` from the customer's preference;
   it never falls back to another browser. `--endpoint` is only for an explicitly
   selected browser-level WebSocket endpoint. The bundled session service is started by the prepared runtime; no extra
   skill or separately installed service is needed. Do not restart the daily browser or copy a profile to establish access.
3. On supported Chrome (144+), the user enables remote debugging at
   `chrome://inspect/#remote-debugging` and accepts Chrome's connection prompt.
   Start `python scripts/run_tool.py browser-session start` once and wait for
   consent; use `browser-session status` instead of repeated starts while waiting.
   Startup briefly waits for an already authorized handshake. If it still reports
   `waiting_for_consent`, check status once before asking the user to find a prompt;
   an updated `connected` state needs no further manual action.
   A missing or stale endpoint, a disconnected session, or an expired consent
   request must be handed back with the command's setup guidance. Keep failed
   starts distinct from `waiting_for_consent`; never report them as connected.
   OpenCLI and fallback captures reuse this connection. Close it with
   `browser-session stop` at the end. Idle sessions expire after 30 minutes;
   browser restarts or disconnections require a new explicit start and consent.
   The service listens only on loopback, uses a random private endpoint, and
   closes only client-owned tabs; a page handed to the user is released from
   automatic cleanup and survives idle expiry or session shutdown. It never
   reconnects automatically. Edge must expose its selected
   daily profile through a valid debugging endpoint too; do not promise this
   mechanism on every browser or managed machine.
4. OpenCLI is the first extraction route to diagnose. Inspect the installed
   runtime and official help before selecting its CDP endpoint.
   Version 1.8.7 still selects Browser Bridge for ordinary website adapters even
   with `OPENCLI_CDP_ENDPOINT`; upstream commit
   [4e8109b](https://github.com/jackwener/opencli/commit/4e8109b6c84afea5e535a7b9a35bc352d1b92fc2)
   fixes that selection. Re-check newer releases rather than assuming the fix is
   installed. If a website adapter selects Browser Bridge, classify its CDP
   extraction as unsupported and use built-in CDP. Never execute the adapter
   through that bridge, install an extension or patch global OpenCLI core to
   make this route work. Keep the diagnostic and browser evidence.

Chrome's consent is distinct from macOS automation permission. This is minimal
manual setup, not guaranteed zero configuration. Modern Chrome does not honor
legacy remote-debugging flags on the default data directory; do not relaunch the
user's browser with those flags, copy a profile, or export cookies as a shortcut.
Never close the daily browser or the user's original tabs. Close only completed
tabs created for this task; retain any page awaiting user login or verification,
even after disconnecting the tool. Site refusal and login
recovery rules still apply across all tools and survive a connection change.

For pages that fail to load, use [bounded network recovery](network-recovery.md)
before declaring the source unavailable: classify the failure, retry only within
the limit, and check relevant VPN/split-routing evidence when appropriate.

Official references: [Chrome existing-session connection](https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session),
[default-profile debugging restriction](https://developer.chrome.com/blog/remote-debugging-port),
[OpenCLI CDP guide](https://github.com/jackwener/opencli/blob/main/docs/advanced/cdp.md).

## Parallelize independent sources

Apply this to all research modes and information sources, including job boards,
company sites, AnySearch, WeChat public accounts, GitHub and relevant articles. Do not run
unneeded sources merely to fill a batch.

- Schedule independent reads concurrently, normally at most **4 in flight** in
  total, with at most **1 per protected site**. Lower limits from a provider or
  the host take precedence. Count individual queries inside AnySearch
  `batch_search` against the total; batch up to available capacity. If batch is
  unavailable, use bounded parallel tool calls. Inspect every success or error.
- Give each browser read its own task-owned tab ID/session. Never share a global
  active page. If a backend cannot reliably isolate targets (including an
  OpenCLI CDP endpoint that automatically picks one page), serialize that backend
  while other independent sources continue in parallel.
- Same-site pagination, dependent detail reads and login recovery are sequential.
  Classify and import a site's current capture before scheduling its next read.
  On refusal cancel queued work for that site and follow user recovery; do not
  switch tools or launch another worker. Already authorized independent sites
  may finish. Existing per-site page, query, row and detail budgets are shared
  across workers/backends, never multiplied by concurrency.
- One coordinator owns budgets and appends journal/import receipts serially as
  results arrive. Give raw captures unique filenames; workers must not append
  to the same journal concurrently. Preserve original outputs, partial failures
  and source identity, then deduplicate findings for the report.

Use native parallel tool calls; extra agents are not required. If concurrency is
not supported, serialize only the affected operations and record that limitation.
Profile reuse does not authorize a new social platform: existing per-consultation
platform authorization and anonymous-source requirements remain unchanged.
