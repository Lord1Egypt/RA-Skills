# pw-browser Quickstart Cookbook

> End-to-end examples for AI agents / scripts. Every example can be copied and run as-is.
> Convention: `pw-browser` stands for the full command
> `NODE_PATH="<SKILL_DIR>/node_modules" node "<SKILL_DIR>/pw-browser.js"`.
> All examples assume a daemon is already running in the background (`pw-browser daemon &`).

---

## Example 1: Fill a form and submit (most common)

Goal: open a page, locate the input and button, type text and submit.

```bash
# Open the page
pw-browser open https://example.com/login

# You MUST snap first to get the ref table
pw-browser snap
# → e1 input placeholder="Username"
# → e2 input placeholder="Password"
# → e5 button "Sign in"

# Fill and click (using the refs from snap)
pw-browser fill e1 "alice"
pw-browser fill e2 "s3cret"
pw-browser click e5

# Verify
pw-browser wait-for "text=Welcome" --timeout 8000
pw-browser snap
```

Key point: `snap` must come before `click`/`fill`, and refs stay stable across snaps (e1 this time is still e1 next time).

---

## Example 2: File upload + download round-trip

Goal: upload a local file, then trigger a download and confirm it landed on disk.

```bash
pw-browser open https://example.com/upload

pw-browser snap
# → e3 input type=file "Choose file"
# → e4 button "Upload"

# Upload (multiple files supported, space- or comma-separated)
pw-browser upload e3 /tmp/report.pdf /tmp/appendix.xlsx
pw-browser click e4

# Wait for upload to finish
pw-browser wait-for "text=Upload complete" --timeout 10000

# Trigger download: click a link/button that downloads, save to a dir
pw-browser snap
# → e9 a "Export CSV"
pw-browser download e9 --path /tmp/downloads --timeout 30000
# → { "ok": true, "savedPath": "/tmp/downloads/export.csv", "suggestedFilename": "export.csv" }
```

Note: `download` is symmetric to `upload`; without `--path` it saves to the current working directory. It can also be an `act` action:
`{"action":"download","ref":"e9","path":"/tmp/downloads"}`.

> 🔒 v1.3.10+: `suggestedFilename` is chosen by the web page and is untrusted input. When `--path` is a directory, the name is reduced to a `basename` and confined inside it; anything escaping returns `PathTraversal`.

---

## Example 3: Shadow DOM / iframe piercing

Goal: some elements live inside a shadow root or a same-origin iframe where normal selectors can't reach — the tool pierces them automatically.

```bash
pw-browser open https://example.com/widget

pw-browser snap
# → e2 button "Inner button"  inShadow:true
# → e7 button "iframe submit"  frameChain:[{sel:"iframe#frame1"}]

# Just click! Location uses css >>> piercing + frameLocator automatically, invisible to the caller
pw-browser click e2
pw-browser click e7
```

Key points:
- `inShadow: true` means the element is inside a shadow root; a non-empty `frameChain` means it's inside an iframe.
- `--annotate` screenshots only mark main-document elements (shadow/iframe elements can't be located by xpath for annotation, but remain clickable in the text snapshot).
- Cross-origin iframes are inaccessible and are skipped automatically.

---

## Example 4: Cookie / localStorage extraction and session restore

Goal: back up the session after login, then restore it next time to skip re-login.

```bash
pw-browser open https://example.com/dashboard
# (complete login manually or via Example 1 first)

# Back up cookies (defaults to ~/.pw-browser/cookies.json, kept inside the confined dir)
pw-browser cookies export
# → { "ok": true, "exported": "~/.pw-browser/cookies.json", "count": 12,
#     "warning": "SECURITY: this file holds live session credentials ..." }

# Back up localStorage (defaults to ~/.pw-browser/localStorage.json)
pw-browser storage export

# —— next session ——
pw-browser open https://example.com/dashboard
pw-browser cookies import          # reads the default ~/.pw-browser/cookies.json
pw-browser storage import          # reads the default ~/.pw-browser/localStorage.json

# Already authenticated after reload
pw-browser reload
pw-browser snap
```

> ⚠️ `cookies` / `storage` depend on a real http/https page origin; `file://` and `data:` pages don't support cookies, and `localStorage` behaviour there is unreliable.

> 📁 **Path confinement:** `cookies` / `storage` `export`/`import` are **confined to `~/.pw-browser/` by default** — a deliberate safety measure so credentials can't be silently scattered into `/tmp` or loaded from attacker-controlled paths elsewhere. A custom path must also live under `~/.pw-browser/` (paths are resolved through `realpath`, so symlinks can't escape either).
>
> 🛡️ **Waiving the confinement is the operator's call, not the caller's (v1.3.8):** earlier versions let any caller lift the guard just by adding `--unsafe` — handing the key to the very party the guard constrains. Escaping now requires **both**: ① the operator (a human) starts the daemon with `PW_BROWSER_ALLOW_UNSAFE_CRED_PATH=1` (a process env var, which a party sending HTTP commands cannot set), and ② the caller passes `--unsafe` (intent). `--unsafe` alone is rejected with `UnsafeOverrideNotPermitted`. Responses carry `confined` and `warning` fields, and the daemon logs every credential-path access to stderr for auditing.

> 🔒 **Security warning (read this):** the exported `cookies.json` / `localStorage.json` contain your **full authenticated session** — potentially `HttpOnly` cookies, bearer/session tokens, CSRF tokens, and other sensitive state. Anyone who obtains the file can **impersonate you** on the site. This tool's daemon **persists browser state across commands**, and the tool also exposes `eval` / `run-code` (which can read cookies/storage from the page context), so the saved material carries a higher risk of being misread, misused, or exfiltrated from your local environment.
> - **Do not** commit these files to git, upload them, or share them.
> - Delete them when done (`rm`); if you must keep them briefly, just leave them in the default `~/.pw-browser/` — since v1.3.9 that directory is created `0700` and credential files (plus the daemon auth token) are written `0600`, so **no manual `chmod` is needed**. On Windows POSIX mode bits aren't enforced by the OS; user-profile ACLs apply instead.
> - If credentials must never touch the disk at all, the operator can start the daemon with `PW_BROWSER_CRED_PERSIST=off`: `export`/`import` are then **refused** (`CredentialPersistenceDisabled`) while in-memory `cookies list` / `storage get|set|clear` keep working — finer-grained than `PW_BROWSER_SAFE_MODE=1`, which disables the credential primitives and code execution wholesale.
> - Restore a session file **only on your own machine and for the same site** — never reuse it across environments or accounts.
> - **Importing (restore) is just as risky:** restoring a session grants logged-in / privileged access to that site. Never auto-import from untrusted paths. In agent / automated workflows, **do not** persist credential material across runs by default — only restore deliberately and in a controlled way, to avoid unintended privilege persistence or session theft.
> - **Serving not-fully-trusted agents:** start the daemon with `PW_BROWSER_SAFE_MODE=1` — since v1.3.2 safe mode **disables all `cookies` / `storage` subcommands entirely** (blocked at the same level as `eval`/`run-code`), closing the session-credential surface at the root.

---

## Example 5: `act` multi-step + self-correction (recommended for agents)

Goal: send a whole sequence of actions to the daemon at once; if the page DOM changes mid-sequence (e.g. clicking a button pops a new menu), the daemon interrupts automatically and returns a fresh snapshot for you to re-plan.

```bash
pw-browser open https://example.com/form

pw-browser snap
# → e1 input "Title"
# → e2 button "Next"   (clicking dynamically reveals new fields e3/e4)

# Send the action sequence in one shot
pw-browser act '[
  {"action":"fill","ref":"e1","text":"Monthly report"},
  {"action":"click","ref":"e2"}
]'
# If clicking e2 reveals new elements → returns { interrupted: true, snap: <fresh snapshot> }
# Continue with the new refs from the returned snapshot:
#   pw-browser act '[{"action":"fill","ref":"e3","text":"..."},{"action":"click","ref":"e4"}]'

# A failed action comes with a diagnosis (whether the ref still exists, similar ref hints) for self-healing
```

Token-saving tip: `1 snap → 1 act → done`, no round-trips back to the model in between.

---

## Troubleshooting quick reference

| Symptom | Fix |
|---------|-----|
| Connection refused | daemon not running → `pw-browser daemon &`; or stale process → clear `~/.pw-browser/daemon.json` + kill port 19223, then restart |
| `ElementNotFound` | ref expired → re-`snap` for a fresh ref |
| `NavigationTimeout` | page loads slowly → `snap` to see actual state, or raise `--timeout` |
| snapshot truncated (`⚠ snapshot truncated`) | page has too many elements, hit the cap → raise `PW_BROWSER_SNAP_LIMIT` or interact first to narrow the page |

Full rules and the complete command table are in `SKILL.md` and `README.md`.
