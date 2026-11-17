---
name: kimi-webbridge
description: |
  Kimi WebBridge lets AI control the user's real browser — navigate, click, type, read, screenshot, and interact with any website using the user's actual login sessions. Use this skill whenever the user wants to interact with websites, automate browser tasks, scrape web content, or perform any action requiring a real browser. Also use when the user mentions "浏览器", "网页", "打开网页", "打开网址", "截图", "上网", "搜一下", "操控浏览器", "browser", "webpage", "open URL", "screenshot", or asks to read/interact with any website. Use even for simple-sounding browser requests — the daemon handles all complexity.
license: Apache-2.0
metadata:
  version: "3.0.7"
  agent_created: true
---

> **WorkBuddy 适配版（由 OpenClaw 版本改写）**
> - 守护进程 `kimi-webbridge.exe` 已通过 Windows 计划任务 **KimiWebBridge-Watchdog**（登录自启 + 崩溃每 1 分钟重启）常驻化，**不会因 WorkBuddy 会话退出或电脑重启而丢失**。
> - 调用方式见下方 **Windows 约定**：所有中文请求体必须用文件体（Python 写 UTF-8 JSON + `curl.exe --data-binary @文件`），**绝不用 `echo`/heredoc 内联**，否则中文变 `?`。本会话已实测直驱 `http://127.0.0.1:10086/command` 成功。
> - 连不上 daemon（connection refused）时，**自己 `start` 即可，不要问用户**：二进制 `start` 幂等，已在运行则 no-op（详见 `references/operations.md`）。

# Kimi WebBridge

Control the user's real browser (with their login sessions) via a local daemon at `http://127.0.0.1:10086`.

## 原作者与许可（Attribution）

- **原始项目**：**Kimi WebBridge**，由 **月之暗面（Moonshot AI / Kimi）** 推出，是一套让 AI 控制真实浏览器（复用用户已登录会话）的基础设施。官网：<https://www.kimi.com/features/webbridge>
- **社区适配**：本 Skill 基于 OpenClaw 生态中对 Kimi WebBridge 的改写版本进行适配。
- **WorkBuddy 适配版**：由 **微光浮影** 改写为 WorkBuddy 可用的形态（含 Windows 守护进程常驻化、中文请求体文件体约定等）。
- **许可**：本适配层以 **Apache-2.0** 协议开源；原始 Kimi WebBridge 的功能、协议与商标归 **Kimi / Moonshot AI** 所有，使用时请遵守其服务条款。

## Tools

| Tool | Args | Returns | Note |
|------|------|---------|------|
| `navigate` | `url`, `newTab`(bool), `group_title` | `{success, url, tabId}` | First call opens a tab — see [Tabs](#tabs-and-the-current-tab). `group_title` sets the group's visible label |
| `find_tab` | `url`, `active`(bool) | `{success, url, tabId, borrowed}` | Re-select a tab **this session** opened; `active:true` borrows the tab the **user** is viewing — see [Tabs](#tabs-and-the-current-tab) |
| `snapshot` | — | `{url, title, tree}` with `@e` refs | **Accessibility tree** (text) — use this to read page content and locate elements |
| `click` | `selector` (@e ref or CSS) | `{success, tag, text}` | Synthetic `el.click()` |
| `fill` | `selector`, `value` | `{success, tag, mode}` | Works on `<input>`/`<textarea>` AND `[contenteditable]` (ProseMirror/Lexical/Slate). `mode` is `"value"` or `"contenteditable"` |
| `evaluate` | `code` (supports async/await) | `{type, value}` | |
| `cdp` | `method`, `params` | raw CDP response | Raw `chrome.debugger` passthrough — what `evaluate` is to JS, `cdp` is to CDP. Low-level escape hatch for cases the tools above don't cover |
| `screenshot` | `format`(png\|jpeg), `quality`(0-100), optional `selector` (@e/CSS), optional `path` | `{format, path, sizeBytes, mimeType}` | Returns a file path, not base64 — see [Screenshots](#screenshots) |
| `network` | `cmd`(start\|stop\|list\|detail), `filter`, `requestId` | request/response data | |
| `upload` | `selector`, `files`(string[]) | `{success, fileCount}` | |
| `save_as_pdf` | `paper_format`, `landscape`, `scale`, `print_background`, optional `path` | `{path, sizeBytes, mimeType, pageTitle}` | Render current page → PDF, returns a file path — see [Save as PDF](#save-the-current-page-as-pdf) |
| `list_tabs` | — | `{success, tabs:[{tabId, url, title, active, groupTitle}]}` | Inspect tabs in the current session |
| `close_tab` | — | `{success, closed: bool}` | Close the current tab in the session |
| `close_session` | — | `{success, closed: int}` | Close all tabs in the session — `closed` is the count. See [Sessions](#sessions) for when to call |

### Tabs and the current tab

Single-tab tools (`snapshot`, `click`, `fill`, `screenshot`, `save_as_pdf`) act on the **current tab** — the one you most recently opened with `navigate` or selected with `find_tab`.

- **Opening pages**: use `newTab:true` when pages should coexist (comparing, cross-referencing); omit it to send the current tab to a new URL.
- **Going back to an earlier tab**: call `find_tab` to make a tab **you opened earlier in this session** the current one again. Pass the tab's **full URL** — take it from `list_tabs` or the earlier `navigate` result. A bare root domain (`kimi.com`) may miss a `www.kimi.com` tab, so prefer the exact URL. By default `find_tab` searches **only this session's own tabs** — it never reaches into the user's other tabs or windows.
- **Acting on a page the user already has open**: pass `active:true` ("use my open X tab" / "the X page I'm viewing"). It **borrows** the tab the user is currently viewing (returns `borrowed:true`); the borrowed tab is operated in place — it is not pulled into the session's tab group.
- If `find_tab` errors with "no tab matching … in this session", the page isn't open in this session — `navigate` with `newTab:true` instead.

```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -d '{"action":"find_tab","args":{"url":"https://www.kimi.com","active":true},"session":"k26-research"}'
```

### Call Format

Every command carries a top-level `session` naming the current task — see [Sessions](#sessions) below. The examples in later sections omit it only for brevity; in real calls always include it. The command format depends on the user's OS.

**macOS / Linux** — inline JSON is fine:

```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","args":{"url":"https://example.com","newTab":true,"group_title":"My task"},"session":"my-task"}'
```

**Windows (PowerShell / cmd)** — the shell corrupts non-ASCII characters (Chinese etc.) carried inline in command arguments or pipes; they reach the daemon as `?` and the text is unrecoverable. Send **every** request as a file body instead:

1. Write the JSON body to a **uniquely-named** temp file with your own file-write tool — never with shell `echo`/heredoc, which corrupts non-ASCII the same way. Give **every** request its own filename with a random suffix (e.g. `webbridge-req-<random>.json`) so concurrent requests never share a file and overwrite each other.
2. POST the file with `curl.exe` — always `curl.exe`, never bare `curl`, which Windows PowerShell aliases to `Invoke-WebRequest`:

```powershell
curl.exe -s -X POST http://127.0.0.1:10086/command -H "Content-Type: application/json" --data-binary "@$env:TEMP\webbridge-req-<random>.json"
```

3. Delete the temp file as soon as the request returns — don't leave request bodies on disk.

**WorkBuddy 推荐写法（Python 写文件体，杜绝中文乱码）：**

```python
import json, os, urllib.request
body = {"action":"navigate","args":{"url":"https://example.com","newTab":True,"group_title":"示例任务"},"session":"my-task"}
p = os.path.join(os.environ["TEMP"], "wb-webbridge-req.json")
with open(p, "w", encoding="utf-8") as f:
    json.dump(body, f, ensure_ascii=False)
req = urllib.request.Request("http://127.0.0.1:10086/command",
    data=open(p,"rb").read(), headers={"Content-Type":"application/json"})
print(urllib.request.urlopen(req, timeout=30).read().decode("utf-8","ignore"))
os.remove(p)
```

## Sessions

**One task = one session = one tab group.** A `session` collects every tab the task opens into one tab group, so the user sees a single group for "what the agent is doing right now". Pass it as a **top-level field** of the request body (not inside `args`).

- **Pick one session name at the task's start, put it on every command, and never switch mid-task — even across different sites.** Switching session names per site is the #1 cause of fragmented tab groups.
- Name it after the **task**, not the site (`camping-research`, `phone-compare`). Use multiple sessions only for genuinely unrelated parallel tasks.
- `group_title` is the human-readable group label — write it in the user's language, on the **first** `navigate` of the task.
- When you create the group (the first `navigate` of a task), tell the user once that this task's pages are collected under group «title», and that you'll close them whenever they ask.

```bash
# First tab: set session + a human label (in the user's language)
curl -s -X POST http://127.0.0.1:10086/command \
  -d '{"action":"navigate","args":{"url":"https://www.kimi.com","newTab":true,"group_title":"K2.6 feature research"},"session":"k26-research"}'
# Another site, same task → same session → joins the same group automatically
curl -s -X POST http://127.0.0.1:10086/command \
  -d '{"action":"navigate","args":{"url":"https://www.moonshot.cn","newTab":true},"session":"k26-research"}'
```

## Screenshots

The daemon writes the image to disk and returns `{format, path, sizeBytes, mimeType}` — never base64, since the model can't read raw image bytes. Take the `.path` and open it with the `Read` tool to actually see it.

```bash
# Default: PNG of the visible viewport, daemon picks a temp path
curl ... -d '{"action":"screenshot","args":{}}'
# Options (each independent): JPEG quality, element-only via @e/CSS selector, custom output path
curl ... -d '{"action":"screenshot","args":{"format":"jpeg","quality":60}}'
curl ... -d '{"action":"screenshot","args":{"selector":"@e123"}}'
```

A caller-supplied `path` is honored verbatim (parent dirs created, existing file overwritten) — use a unique name to avoid clobbering. `save_as_pdf` follows the same rule.

## Prefer snapshot over CSS/JS selectors

`snapshot` returns interactive elements with `@e` refs based on semantic role/name. Use them directly with click/fill — they survive CSS class hash changes that break manually-written selectors.

Fall back to `evaluate` (JS) only when:
- The target has no `@e` ref in the snapshot
- You need attributes not in the snapshot (e.g., `href`)
- You need to dispatch complex event sequences, or scroll

## Evaluate Tips

- Always use compact `JSON.stringify(data)` — never add `null, 2` formatting. Indentation and newlines can inflate the response several times over, causing truncation during transmission.
- `evaluate` calls share the page's JS realm — re-declaring the same `const`/`let` across two calls throws `SyntaxError`. Wrap in an IIFE for a fresh scope: `(() => { const x = ...; return x; })()`.

## Text input — use `fill`

`fill` (selector = CSS or `@e` ref, plus the value) works on `<input>`/`<textarea>` (returns `mode: "value"`) and on `[contenteditable]` rich editors — ProseMirror, TipTap, Lexical, Slate, Quill, etc. (returns `mode: "contenteditable"`), firing the right input events so the page reacts.

`fill` is **clear-and-insert**: existing content is replaced. To append, read the current value via `evaluate`, concatenate, then `fill` with the result.

## Form submit / special keys

There's no separate "press Enter" tool. To submit a form, click the submit button directly (`click` on the @e ref or selector). To dispatch a key event programmatically (e.g. Escape to close a modal):

```bash
{"action":"evaluate","args":{"code":"document.activeElement.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))"}}
```

## Save the current page as PDF

`save_as_pdf` renders the current page to PDF and returns the file path. All args optional:
- `paper_format`: `letter` (default) \| `a4` \| `legal` \| `a3` \| `tabloid`
- `landscape`: `false` (default)
- `scale`: `1.0` (default), range `[0.1, 2.0]`
- `print_background`: `true` (default) — keep background colors
- `path`: caller-supplied output path; if absent, daemon picks a default under OS temp dir using the page title as the filename

`path` semantics match `screenshot`: written verbatim, parent dirs auto-created, existing files overwritten.

Decoded PDF cap is 100 MB. Above that the daemon refuses; reduce `scale` or split the page.

## Known limitations

- **Sites that strictly check `event.isTrusted`** (some banking portals, captchas) ignore `click` / `fill` because those fire DOM-level synthetic events (`isTrusted=false`). For these, tell the user the page needs manual interaction. (Trusted input is possible at the protocol level via the `cdp` escape hatch, but treat that as advanced.)
- **Cross-origin iframes**: `fill`, `click`, `evaluate`, and `snapshot` operate on the top frame. If a target element lives in a same-page iframe from a different origin (e.g. embedded sandbox demos), navigate to the iframe's URL directly instead.

## If a tool call fails (daemon or extension not ready)

**If a tool call can't reach the daemon (connection refused), start it yourself — don't ask the user. This is safe to run anytime: it no-ops if the daemon is already up.**

**macOS / Linux:**

```bash
~/.kimi-webbridge/bin/kimi-webbridge start
```

**Windows (PowerShell):**

```powershell
& "$env:USERPROFILE\.kimi-webbridge\bin\kimi-webbridge.exe" start
```

Then retry the tool call. If it still fails — or the browser extension won't connect — point the user to the help page instead of deep-troubleshooting:

- English: https://www.kimi.com/features/webbridge
- 中文: https://www.kimi.com/zh-cn/features/webbridge

Never run `stop` / `restart` / `uninstall` automatically — those kill a running daemon. See `references/operations.md` for anything deeper.

## Version mismatches

If a tool returns an error containing **"Please update the Kimi WebBridge extension"**, the user's browser extension is older than this skill. Don't try to reconcile versions yourself — just tell the user, in their language, to update the extension and retry:

- English: https://www.kimi.com/features/webbridge
- 中文: https://www.kimi.com/zh-cn/features/webbridge

## 自动结束夸克进程（WorkBuddy 适配版默认行为）

WorkBuddy 适配版在用户授权下，任何 WebBridge 浏览器任务**向用户交付结果后**，会自动收尾，不留夸克（Quark）后台进程——夸克有关窗后仍驻留后台（含 `QuarkUpdater` 更新进程）的坏习惯，用户不愿其常驻。

**标准收尾流程（交付结果时自动执行，不需用户再次要求）：**
1. 若该任务开过 tab 组，先 `close_session` 关掉（避免留标签）。
2. 随即强制结束夸克所有进程——直接调用封装脚本（推荐）：
   ```powershell
   powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.kimi-webbridge\close_quark.ps1"
   ```
   脚本逻辑：`Get-Process -Name "quark*" | Stop-Process -Force`，再复核无残留，并确认 `kimi-webbridge.exe` 守护进程未被误杀。
3. 脚本输出 `QUARK_CLEAN` / `QUARK_KILLED` 即成功；若 `WARN_STILL_RUNNING` 需重试或向用户报障。

**注意事项：**
- 此操作会关闭**所有**夸克窗口（Chromium 单进程树，无法只杀 AI 开的标签）。若用户自己也在用夸克浏览，执行前应口头提醒，或仅 `close_session` 不杀进程——但默认按用户授权执行 kill。
- **只杀夸克，绝不动 `kimi-webbridge.exe` 守护进程**（那是 WorkBuddy 的桥，由 watchdog 计划任务保活）。
- kill 后 WebBridge 浏览器扩展随夸克一起死；下次任务前需确保夸克已启动且扩展已连 daemon（daemon 自己仍在）。连不上就提示用户开夸克，或自行 `start` daemon 后重试 `navigate`——但浏览器端仍需用户开夸克。
- 阿里"夸克X"PC 版主程序为 `quark.exe` / `QuarkX.exe`，后台含 `QuarkUpdater`；`quark*` 通配一并覆盖，纯 ASCII 无中文参数，`Stop-Process` 不受中文乱码铁律影响。
