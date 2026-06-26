---
name: macscreenshot
description: Capture macOS screenshots for the whole screen, a specific app window, or a precisely targeted desktop window using built-in system tools. Use when the user asks to screenshot the desktop, a frontmost app, a WeChat/Weixin window, a Chrome window, or to locate a macOS window by keyword and capture it. Prefer the built-in screencapture command and CoreGraphics window enumeration via inline Swift. If required capabilities are missing, tell the user exactly which macOS permissions to enable; if Swift tooling is unavailable, tell the user how to install Xcode Command Line Tools manually.
metadata: {"clawdbot":{"emoji":"📸","os":["darwin"],"requires":{"bins":["swift","screencapture","python3"]},"install":[{"id":"xcode-clt","kind":"shell","command":"xcode-select --install","bins":["swift"],"label":"Install Xcode Command Line Tools"}]}}
---

# macscreenshot

Capture screenshots on macOS with built-in tools only.

## Default workflow

1. For a full-screen capture, use `screencapture -x <output>`.
2. For a specific app window, first try to enumerate windows with inline Swift + CoreGraphics.
3. Filter returned windows by `owner` and `name`, matching keywords like `weixin`, `wechat`, or the app name the user gave.
4. Prefer a window whose `sharing` is `1`.
5. Capture the exact window with `screencapture -x -l <windowId> <output>`.
6. Save under the workspace.
7. Return the local path by default.
8. Only send or attach the screenshot into the current chat if the user explicitly asks for it.
9. Treat screenshots as potentially sensitive because they may contain confidential on-screen information.

## Scripted path

Prefer the bundled script when available:

```bash
scripts/capture-window-by-keyword.sh <keyword> [output_path]
scripts/capture-window-by-keyword.sh --list <keyword>
scripts/capture-window-by-keyword.sh --index <n> <keyword> [output_path]
```

Examples:

```bash
scripts/capture-window-by-keyword.sh wechat
scripts/capture-window-by-keyword.sh --list wechat
scripts/capture-window-by-keyword.sh --index 2 wechat
```

The script:
- enumerates on-screen windows with inline Swift + CoreGraphics
- filters by keyword against `owner` and `name`
- supports alias matching, for example `weixin -> wechat, wx`
- can list multiple matches without capturing
- can capture a specific match by 1-based index
- otherwise prefers a window with `sharing = 1`
- captures the exact window with `screencapture -x -l <windowId>`
- prints the output PNG path
- returns a local artifact by default
- only attach or send the PNG if the user explicitly asks for delivery into chat

## Proven method for targeting a window by keyword

Use this exact pattern to locate candidate windows:

```bash
swift - <<'SWIFT'
import CoreGraphics
import Foundation

let options = CGWindowListOption(arrayLiteral: .optionOnScreenOnly, .excludeDesktopElements)
let windows = (CGWindowListCopyWindowInfo(options, kCGNullWindowID) as? [[String: Any]]) ?? []

let matches = windows.compactMap { w -> [String: Any]? in
    let owner = (w[kCGWindowOwnerName as String] as? String) ?? ""
    let name = (w[kCGWindowName as String] as? String) ?? ""
    let low = (owner + " " + name).lowercased()
    guard low.contains("weixin") || low.contains("wechat") else { return nil }

    return [
        "id": w[kCGWindowNumber as String] ?? "",
        "owner": owner,
        "name": name,
        "sharing": w[kCGWindowSharingState as String] ?? "",
        "bounds": w[kCGWindowBounds as String] ?? ""
    ]
}

let data = try! JSONSerialization.data(withJSONObject: matches, options: [.prettyPrinted])
print(String(data: data, encoding: .utf8)!)
SWIFT
```

Typical success indicators:
- `owner` or `name` matches the requested app/window
- `id` is present
- `sharing = 1`

Then capture the window:

```bash
screencapture -x -l <windowId> <output.png>
```

## Lessons learned / success criteria

- Do not depend on Python `Quartz`; it may not be installed.
- Do not depend on `System Events` window attributes for window IDs; some apps do not expose `AXWindowNumber` reliably.
- Inline Swift calling `CGWindowListCopyWindowInfo` is the most reliable built-in approach on macOS.
- `screencapture -l <windowId>` is a true system window capture, not a cropped full-screen image.
- If enumeration succeeds but capture fails, inspect whether the target window is shareable and on screen.

## Troubleshooting

### If `screencapture` works for full screen but not for a window

Check whether the enumerated target has `sharing = 1`. If not, tell the user the app/window is not currently shareable for window capture and ask them to bring it to the front and try again.

### If `System Events` says assistive access is not allowed

Do not rely on that path. Prefer the Swift + CoreGraphics method. If the user still wants UI-structure inspection, tell them to enable:
- System Settings → Privacy & Security → Accessibility
- Turn on access for the actual host process running the agent, often `openclaw-gateway`, Terminal, or the active terminal host

### If screen capture is blocked

Tell the user to enable:
- System Settings → Privacy & Security → Screen & System Audio Recording (or Screen Recording on older macOS)
- Grant permission to the actual host process running the command

### If `swift` is not found

Tell the user to install Xcode Command Line Tools manually:

```bash
xcode-select --install
```

If that fails or they want the GUI path, tell them to install Xcode from the App Store or re-run the command after opening Software Update.

## Output location

Prefer saving screenshots into a workspace subdirectory like:
- `screenshots/`
- `captures/`

Use descriptive filenames with timestamps when the user may request multiple captures.

## Privacy and chat delivery rule

Treat screenshots as potentially sensitive local artifacts.

When a screenshot request comes from a chat surface:
- capture the screenshot first
- save it locally by default
- only send the PNG into the current chat if the user explicitly asks for delivery or attachment
- if explicit delivery is requested and an explicit messaging tool is available, prefer using it to send the file into the current conversation
