# pw-browser

> A Playwright-based browser automation CLI — daemon + client architecture that drives your system's Chrome/Edge directly, with no extra browser download required.

> 📘 This is the English documentation. 中文文档见 [`README.md`](./README.md). The agent-facing instructions live in [`SKILL.md`](./SKILL.md), which is currently Chinese-only; a Chinese-reading agent (or the user) can follow it. For end-to-end examples see [`QUICKSTART.en.md`](./QUICKSTART.en.md).

> ⚠️ **Full capabilities (includes code execution & credential manipulation)**: this tool is **NOT just "open web pages"** — it ships two **code-execution** abilities, `eval` (arbitrary in-page **JavaScript**) and `run-code` (Playwright/Node code in the daemon context), plus `cookies` / `storage` **credential read/write primitives** that can extract/inject login state and session tokens **without any code execution**. All are controlled by a persistent local daemon (127.0.0.1:19223), gated by a daemon token; `PW_BROWSER_SAFE_MODE=1` **fully disables** code-exec and credential access (v1.3.2+). Read "🔐 Permission Model & Least Privilege" and "⚠️ Security Boundaries" below to understand the full attack surface and applicable boundaries before authorizing.

## Features

- **System browser reuse**: connects to your installed Chrome or Edge via Playwright's `channel: 'chrome'`, no Chromium download.
- **Cross-platform**: Windows, macOS, Linux.
- **Persistent session**: the daemon keeps browser state alive across commands — no restart per call.
- **Accessibility snapshot**: `snap` produces a page element tree with stable `ref` references, no CSS selectors to write.
- **Non-headless**: the browser window is always visible so the user can monitor every action in real time.
- **Human-in-the-loop**: automatically hands off to the user for login / CAPTCHA.

## Installation

```bash
git clone <repo-url> pw-browser
cd pw-browser
npm install
```

> Requires: [Node.js](https://nodejs.org/) 18+ and Chrome or Edge installed on the system.

## Quick start

```bash
# 1. Start the daemon (background)
node pw-browser.js daemon &

# 2. Wait for the daemon to be ready
sleep 4

# 3. Open a page
node pw-browser.js open https://www.baidu.com

# 4. Take a snapshot (required! snap before every interaction)
node pw-browser.js snap

# 5. Interact — using the e0, e1, e2... refs from the snapshot
node pw-browser.js fill e12 "weather forecast"
node pw-browser.js click e13

# 6. Check the result
sleep 2
node pw-browser.js snap

# 7. Close
node pw-browser.js close --all
```

## Command reference

| Category | Command | Description |
|----------|---------|-------------|
| Lifecycle | `init` / `open <url>` / `close` / `close --all` / `recover` | start, navigate, close, recover |
| State | `snap` / `wait-for <target>` | snapshot (**refs stay stable across snaps**, same element = same ref) |
| Interaction | `click <ref>` / `fill <ref> "text"` / `type "text"` / `press <key>` / `hover <ref>` / `select <ref> <opt>` / `check <ref>` / `uncheck <ref>` / `upload <ref> <file...>` / `drag <ref-from> <ref-to>` / `download <ref> [--path dir]` | click, fill, press, upload, drag, download, etc. |
| Cookie/Storage | `cookies list` / `export [--path f]` / `import <file>` / `clear` / `set <name> <value> [--domain d]` · `storage get [key]` / `set <k> <v>` / `clear` / `export [--path f]` / `import <file>` | read/write cookies and localStorage (open a real http/https page first) |
| Navigation | `goto <url>` / `go-back` / `go-forward` / `reload` | page navigation |
| Tabs | `tab list` / `tab select <idx>` / `tab close <idx>` | multi-tab management |
| Batch | `act '[{"action":"click","ref":"e13"}, ...]'` | run an action sequence at once; auto-interrupts and re-snaps on DOM change |
| History | `history [--limit N] [--clear]` | view/clear operation history |
| Advanced | `screenshot [--annotate]` / `mousewheel <dx> <dy>` / `eval "<expr>" [ref]` ⚠️ / `run-code "<code>"` ⚠️ | screenshot (`--annotate` overlays numbered boxes matched to refs), scroll, code execution. Without `ref`, `eval` runs against the page global scope (`scope: "page"`); with `ref`, the identifier **`el`** is bound to that DOM node (`scope: "element"`), e.g. `eval "el.textContent" e3`. Return values must be JSON-serializable |
| Delay | `sleep <seconds>` | wait |
| Dialog | `dialog-accept [text]` / `dialog-dismiss` | handle native alert/confirm/prompt dialogs |
| Daemon | `shutdown` | stop the persistent daemon and free the browser process |

> ⚠️ `eval` runs JS in the **browser context** (no Node access); `run-code` runs Playwright code in a **restricted `vm` sandbox** in the daemon (no direct Node `fs`/`process`/`child_process`, but it can read/write local files via browser download/upload and issue arbitrary network requests). Both have full browser control. Use only for explicitly authorized tasks.

## Architecture

```
┌──────────────┐     HTTP (localhost:19223)     ┌──────────────┐
│  pw-browser  │ ──────────────────────────────→│   Daemon     │
│  (CLI client)│                                │  (browser)    │
└──────────────┘                                └──────┬───────┘
                                                       │
                                                       ├─ Playwright
                                                       ├─ Chrome / Edge
                                                       └─ persistent page state
```

The daemon runs continuously after start; browser and page state persist across commands. The CLI calls the daemon over HTTP each time.

## Core workflow rules

1. **Observe before you act**: `snap` before every interaction, act on the snapshot refs.
2. **Login handoff**: on a login/CAPTCHA page, tell the user to act manually; continue after they confirm.
3. **Identify pagination type before paging**: numbered pages / infinite scroll / "load more" each need a different approach.
4. **Daemon recovery**: on connection error, kill the process on port 19223 → delete `daemon.json` → restart.

See `SKILL.md` for detailed rules and examples.

## Enhanced capabilities (inspired by browser-use)

This tool is positioned as a "**secure, controllable browser CLI base + persistent daemon; planning is left to the external AI**", rather than an "all-in-one brain+hand" agent framework like browser-use. We borrowed four capabilities from browser-use that are also valuable for a CLI base:

### A. Stable element references (stable ref)
- `snap` no longer re-numbers refs each time; it builds a persistent `stableKey → ref` map by the element's **semantic identity** (text/placeholder/aria-label when present, else a DOM branch-path hash).
- **The same logical element keeps the same ref across snaps**, so the external AI can reuse a previous ref without re-snapping every step (e.g. after filling a form, e13 is still that submit button).
- `findElement` adds **Strategy 0: precise xpath first** — pins the element by the exact xpath recorded in the snapshot, eliminating the "same-name element mis-click" ambiguity of pure semantic lookup.

### B. Visual-aided screenshot (`screenshot --annotate`)
- Injects an overlay drawing a red border + numbered label for **each element matched to a snap ref** (`document.evaluate(xpath)` for precise positioning).
- The overlay is removed after the screenshot. A multimodal AI can "read the numbers off the picture" to locate `e13` spatially,弥补ing the lack of spatial info in a plain-text snapshot.

### C. Action sequence + self-correction (`act`)
- `act '[{"action":"click","ref":"e13"}, ...]'` sends a sequence at once, reusing `executeSingle` step by step.
- Before each non-first action it re-snaps and compares the `branchPathHash` set: if the page shows **new elements** (DOM change), it sets `interrupted=true` and returns a fresh snapshot for the external AI to re-plan — mirroring browser-use's `multi_act` mid-sequence interrupt.
- A failed action carries a `diagnosis` (whether the ref still exists, similar-ref hints) for self-healing.

### D. Structured input + operation history (`history`)
- `act` takes a structured JSON action array (instead of scattered subcommands), lowering the external AI's CLI-arg error rate.
- `history` records `{ ts, cmd, params (token filtered), ok, elapsedMs }` per operation, capped at 500, with `--clear`. The external AI can review "what I clicked, which step failed" — compressing context and enabling review, echoing browser-use's Mem0-style history compression (here with a lightweight local history instead of a vector store).

### E. Shadow DOM / iframe piercing
- The snapshot recurses into **open shadow roots** and **same-origin iframes**; those elements appear in the ref table and can be directly `click`/`fill`/`upload`/`drag`.
- A ref carries `inShadow: true` (inside shadow) or `frameChain` (iframe chain); location is done automatically via `css >>>` piercing + `frameLocator`, invisible to the external AI.
- Cross-origin iframes are inaccessible and skipped; `--annotate` screenshots only mark main-document elements (shadow/iframe elements can't be located by xpath for annotation, but remain clickable in the text snapshot).

### F. File upload and drag
- `upload <ref> <file1> [file2 ...]`: sets files on an `<input type="file">` (multiple supported).
- `drag <ref-from> <ref-to>`: drag via Playwright `dragTo`.
- `download <ref> [--path dir]`: symmetric to `upload` — optionally click `<ref>` to trigger a download, saved to `--path` (default cwd); also usable as an `act` action.
  > 🔒 v1.3.10+: the page-supplied suggested filename is reduced to a bare `basename` and confined inside `--path` (out-of-bounds returns `PathTraversal`), so a hostile page can no longer use a name like `../../.bashrc` to write outside the directory. If `--path` names an explicit file, it is used verbatim.

### G. Cookies and local storage (first-class commands)
- `cookies list|export|import|clear|set`: read/write the current context's cookies, no more `eval` workarounds.
- `storage get|set|clear|export|import`: read/write based on `localStorage`.
- Typical use: `cookies export` after login to back up the session, `cookies import` next time to skip re-login.
- 📁 **Path confinement (operator-gated):** `export`/`import` are confined to `~/.pw-browser/` by default (so credentials can't be scattered into `/tmp` or loaded from attacker-controlled paths elsewhere; paths are resolved through `realpath`, so symlinks can't escape). Since v1.3.8 the confinement **cannot be waived by the caller**: escaping it requires **both** ① the operator starting the daemon with `PW_BROWSER_ALLOW_UNSAFE_CRED_PATH=1`, and ② the caller passing `--unsafe`. `--unsafe` alone returns `UnsafeOverrideNotPermitted`. Responses carry `confined` and `warning` fields, and every credential-path access is logged to the daemon's stderr.
- 🔒 **Session-persistence risk (Rogue Agent / Medium):** `export`/`import` let the login state be written to disk and restored across runs — convenient, but a rogue/misbehaving agent can use it for **privilege persistence**. Treat exported session files as secrets: delete when done; if kept, just leave them under `~/.pw-browser/` — since v1.3.9 that directory is created `0700` and both credential dumps and the daemon token file are written `0600`, so no manual `chmod` is needed (on Windows POSIX mode bits aren't enforced; user-profile ACLs apply). To forbid credentials on disk entirely, start the daemon with `PW_BROWSER_CRED_PERSIST=off`: `export`/`import` are **blocked** (`CredentialPersistenceDisabled`) while `list`/`get`/`set`/`clear` keep working — finer-grained than safe mode, for long-running agents that need full automation but must not leave restorable sessions behind. `cookies clear` / `storage clear` and `shutdown` the daemon when not needed (idle auto-exit defaults to 15 min). For not-fully-trusted callers, start the daemon with `PW_BROWSER_SAFE_MODE=1` — since v1.3.2 it **disables all cookies/storage subcommands entirely** (credential primitives blocked at the same level as code execution); pair with sandbox isolation if needed.

## Token saving & daemon lifecycle

**No "LLM call per step" token black hole**: this skill is just a deterministic executor + persistent daemon; the model only lives in the external orchestration layer and only spends tokens when it actively calls. Keep these habits to stay token-efficient:

- Plan with a text `snap` (ref table, tens of tokens) instead of a `screenshot` (hundreds of KB base64) fed to a vision model every step.
- Reuse stable refs across snaps instead of re-snapping every step.
- Batch a string of actions into one `act '<json>'`; the daemon self-corrects internally without returning to the model.

**The daemon is intentionally persistent** (reuses one browser across commands, avoiding reopening Chrome each time). Therefore:

- It's normal to still see the browser window after a task ends — the daemon still holds it.
- Stop explicitly: `pw-browser shutdown` (hardened — even if `browser.close()` hangs it times out and exits, never stuck/hanging the client).
- **Idle auto-exit**: by default the daemon **auto-closes the browser and exits after 15 minutes idle**; `PW_BROWSER_IDLE_MS` adjusts this (`0` disables). No manual cleanup needed after you leave.
- **Configurable port + conflict avoidance**: default `127.0.0.1:19223`, override with `PW_BROWSER_PORT`. On startup, if a daemon is already alive on the target port it exits immediately (no double-start); if the port is taken by something else it auto-increments and writes the actual port back to `~/.pw-browser/daemon.json`, which the client reads automatically.
- Prefer `shutdown` or idle exit over force-killing the process to avoid orphaned browser children.

## Security

- The daemon listens on `127.0.0.1:19223`, localhost-only.
- **Command auth**: every daemon command except the `/health` probe requires a random `token`, generated at daemon start and written to `~/.pw-browser/daemon.json` (default readable only by the current user). The CLI carries it automatically; a local process that hasn't read that file cannot call in — closing the "unauthenticated HTTP endpoint = RCE surface" gap.
- **Safe mode**: `PW_BROWSER_SAFE_MODE=1 node pw-browser.js daemon` fully disables `run-code` / `eval` **and all `cookies` / `storage` credential primitives** (v1.3.2+), keeping only the whitelisted snap/click/fill commands — suitable when serving not-fully-trusted agents.
- `eval` runs in the browser context; `run-code` runs in a `vm` restricted sandbox (no direct Node system APIs, but it can read/write local files via browser download/upload). Local trusted environments only.
- The browser runs non-headless so the user can monitor in real time.
- Not recommended as a public API service; if you must, add auth and an operation whitelist.
- **Permission model note**: the frontmatter `capabilities` / `allowed-tools` are **free-form metadata** describing this skill's attack surface — **not a permission grant or a sandbox boundary**. Having a capability means the skill *can* do it, not that it is *limited* to it. There is **no** formal permission system beyond the daemon token / safe mode / path confinement; any "least privilege" need must be met at the orchestration layer via **deployment mode (safe mode + sandbox) + scoped operation agreements**. See SKILL.md "🔐 Permission Model & Least Privilege".

### Dependency security note (CVE-2025-59288)

This project depends directly on `playwright-core@1.61.1` (Playwright core, no browser-download logic, ≥ 1.55.1). CVE-2025-59288 affects the full `playwright` package's install script that downloads and installs a browser (`curl -k` without cert verification). This tool depends only on `playwright-core`, **contains no browser-download code at all**, and at runtime reuses the system's installed Chrome/Edge via `channel: 'chrome'`. The vulnerability is therefore completely untriggerable on this tool's usage path.

## Using as an AI Skill

This tool can be used as a skill by an AI assistant. Drop the whole directory into the skill install path and the assistant follows the rules in `SKILL.md` to automate.

## License

[MIT](LICENSE)
