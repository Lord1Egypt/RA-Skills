---
name: browser-relay-reliability
description: Harden OpenClaw browser extension relay behavior by eliminating blank-target tab churn, fixing download behavior forwarding, and standardizing download paths.
metadata: { "openclaw": { "emoji": "🧱", "requires": { "bins": ["rg"] } } }
---

# OpenClaw Browser Relay Reliability

Use this skill when extension-relay browser sessions show flaky target creation, missing download behavior, or inconsistent download locations.

## What this improves

- Reuse active target for blank `Target.createTarget` requests to avoid throwaway tabs.
- Forward `Browser.setDownloadBehavior` as `Page.setDownloadBehavior` through the extension bridge.
- Standardize default download output to `~/Downloads/OpenClaw`.
- Align temp download path builder with shared default download directory.

## Proof points

- `assets/chrome-extension/background.js`
- `src/browser/extension-relay.ts`
- `src/browser/paths.ts`
- `src/browser/pw-tools-core.downloads.ts`

## Verify quickly

1. Start extension-relay flow and trigger a blank target create request; confirm no extra tab churn.
2. Trigger a browser download in relay mode; confirm the behavior applies and file saves under `~/Downloads/OpenClaw`.
3. Repeat in a second session to confirm stable path and no random temp download roots.

## When to run

- After extension relay changes.
- When debugging failed or missing downloads in relay mode.
- During browser automation reliability hardening.
