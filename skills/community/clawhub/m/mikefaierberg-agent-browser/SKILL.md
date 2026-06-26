---
name: agent-browser
description: Fast browser automation via `agent-browser` CLI + OpenClaw `browser` tool. Use for web research, form filling, navigation, and screenshotting.
---

# Agent Browser Skill

Two browser automation options are available, sharing the **same** Chrome for Testing v148 binary:

1. **OpenClaw `browser` tool** — built-in plugin, managed by gateway, auto-started
2. **`agent-browser` CLI** (v0.26.0) — standalone, extra features (batch, auth vault, visual diff, chat)

**Rule of thumb:** Public websites → OpenClaw `browser` tool. Logged-in sites → Tandem Browser `profile="user"`. Complex automation → `agent-browser` CLI via exec.

---

## Quick Reference

### Status

```tool
browser doctor           # Check health
browser status           # Running state
browser start            # Launch (auto-start if not running)
browser stop             # Shutdown
```

### Navigate & Read

```tool
browser navigate url="https://example.com"
browser snapshot              # Accessibility tree with @ref IDs
browser snapshot refs="aria"  # Playwright aria refs (more stable)
browser screenshot            # Visual capture
```

### Act (use snapshot refs)

```tool
browser act request={kind:"click", ref:"@e1"}
browser act request={kind:"fill", ref:"@e3", text:"value"}
browser act request={kind:"type", ref:"@e3", text:"value slowly"}
browser act request={kind:"press", key:"Enter"}
browser act request={kind:"select", ref:"@e2", values:["option1"]}
browser act request={kind:"hover", ref:"@e5"}
browser act request={kind:"wait", timeMs:2000}
```

### Tab Management

```tool
browser open url="...", label="my-tab"   # Open with named label
browser focus targetId="my-tab"           # Switch to tab
browser close targetId="t1"               # Close tab
browser tabs                              # List all open tabs
```

### Agent-Browser CLI (via exec)

```
agent-browser open https://...
agent-browser snapshot -i -c
agent-browser click @e2
agent-browser fill @e3 "text"
agent-browser screenshot --annotate
agent-browser keyboard type "text"
agent-browser auth save <name> --url <url> --username <u> --password <p>
agent-browser diff snapshot
agent-browser batch ["open url" "snapshot -i" "click @e1"]
```

---

## Operating Loop

1. **Check status** — `browser status` or `browser doctor` if health unknown
2. **Navigate** — `browser navigate url="<target>"`
3. **Read** — `browser snapshot` to get interactive elements with @ref IDs
4. **Act** — Use refs from snapshot for click/fill/press/select
5. **Re-snapshot** — After any navigation or UI change, snapshot again (refs become stale)
6. **Recover** — If ref fails, snapshot once more; if still broken, report as manual action
7. **Profile pick** — Omit `profile` for public sites; use `profile="user"` for logged-in Tandem sessions

## Tips

- Use `refs="aria"` for more stable element references that survive page re-renders
- Label task tabs at open time: `label="research"`
- `agent-browser chat "..."` for AI-driven natural language browser tasks
- `agent-browser --headed` to show browser window for debugging
- `agent-browser --profile Default` to reuse Chrome login state
