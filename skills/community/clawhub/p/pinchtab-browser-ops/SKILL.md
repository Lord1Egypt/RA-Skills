---
name: pinchtab-browser-ops
description: Browser automation via PinchTab CLI (nav/snap/find/click/fill/press/text) with low-token accessibility-tree flow. Use when the user asks to operate websites, fill forms, publish content (for example 小红书), collect page text, or run repeatable browser workflows and wants PinchTab instead of screenshot-driven control.
---

# PinchTab Browser Ops

Use PinchTab as the default browser-control path.

## Workflow

1. Start and verify PinchTab
2. Navigate and snapshot page structure
3. Operate elements by refs (`click/fill/press`) from fresh snapshots
4. Verify outcome with `text`, URL, and key UI markers

## 1) Instance lifecycle policy (mandatory)

Always reuse existing running instance first.

Rules:
- Reuse current running instance/profile whenever it is operable.
- Launch a new instance only when no operable instance exists.
- Do not close browser instances after task completion.
- Keep the instance alive for subsequent tasks and state continuity.

Check state first:

```bash
pinchtab health
pinchtab instances
pinchtab tab list
```

Only if unavailable, start service/instance:

```bash
pinchtab server
# then launch an instance only when needed
```

## 2) Navigate and map page

Open the target page:

```bash
pinchtab nav <url>
# or
pinchtab nav <url> --new-tab
```

Get actionable structure (preferred):

```bash
pinchtab snap -i -c
```

Use `pinchtab find "<label>"` if the page is large, then confirm with a fresh `snap` before action.

## 3) Operate safely by refs

Prefer deterministic commands:

```bash
pinchtab click <ref>
pinchtab fill <ref> "..."
pinchtab press <ref> Enter
```

Rules:
- Re-snapshot after each major state change (modal open, route change, submit, tab switch).
- Insert a short stabilization delay (`1-2s`) between critical actions on dynamic pages.
- Do not reuse stale refs after navigation or rerender.
- Retry at most 2 times with fresh `snap`; then ask for human intervention.

## 4) Verify and finish

Always validate completion using:

```bash
pinchtab text
pinchtab tab list
```

Check at least one concrete success signal (for example: “草稿箱(1)”, “保存成功”, changed URL, expected title).

## Login/CAPTCHA policy

- Require user to complete login, QR scan, SMS code, CAPTCHA, or 2FA manually in local browser.
- Do not request, store, or relay one-time codes.
- Resume automation only after user confirms “已登录”.

## Fallback policy

If strict `nav/snap/find/click/fill/press/text` cannot progress:
1. Recheck page state and auth state.
2. Ask user for one manual step (focused unblock only).
3. Use `eval` only when explicitly approved and only for short-lived unblock; revert to normal flow immediately.

## Resource map

- 小红书长文发布标准流程（标题<=20、正文描述、话题、暂存离开）: `references/xiaohongshu-longform.md`
