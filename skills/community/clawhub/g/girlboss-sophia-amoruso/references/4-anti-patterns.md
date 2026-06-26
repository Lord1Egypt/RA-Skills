# Anti-Patterns — Troubleshooting and Common Issues

> Source: kickbacks.ai product documentation and VS Code Marketplace Q&A

## Installation Issues

### "Kickbacks incompatible"

**Cause:** Your Claude Code version is older than what the current Kickbacks build supports.
**Fix:** Update Claude Code to the latest version via the VS Code extension marketplace.

### "Kickbacks offline"

**Causes (in order of likelihood):**
1. No internet connection — the extension needs backend access.
2. Corporate VPN or firewall blocking `kickbacks.ai` API calls.
3. Backend temporarily down (rare — the service has auto-recovery).
4. First-install authentication delay (wait 10–15 seconds).

**Troubleshooting steps:**
1. Check your internet connection.
2. Wait 10–15 seconds for initial auth.
3. Click "Kickbacks offline" in the status bar to trigger reconnection.
4. Check if your network blocks `api.kickbacks.ai`.
5. Reinstall the extension.

### Extension Not Showing

**Causes:**
- Installed but not activated (VS Code sometimes delays activation).
- Conflicting extension disabling Kickbacks.
- VS Code workspace settings overriding extension permissions.

**Fix:** Open VS Code, go to Extensions panel, verify Kickbacks shows as installed and enabled. Reload window.

> **Case: Corporate Firewall** (Product): A user behind a strict corporate VPN couldn't authenticate. The extension's API calls to `api.kickbacks.ai` were blocked by the company's outbound proxy. Solution: exclude `kickbacks.ai` from the proxy block, or install on a personal machine.

## Earnings Misconceptions

### "I'm not earning because I didn't sign in"

**Truth:** Preview impressions (shown before sign-in) don't earn revenue. You must sign in with Google for earnings to accrue. This is by design — the preview is a product demo, not a paid feature.

### "I should see thousands of dollars"

**Truth:** Kickbacks generates micro-earnings. At current market rates, a heavy user earns roughly $5-40/month. It's designed as passive bonus income from time you'd spend waiting anyway, not a primary revenue stream.

### "More machines = more money"

**Partial truth:** Yes, installing on more machines increases impression volume. However, earnings also depend on advertiser demand, which fluctuates by season and market conditions. Diminishing returns apply after 3-4 machines.

## Technical Errors

### Spinner Not Changing

**Causes:**
- Kickbacks is disabled (check status bar).
- Your Claude Code version is too new (extension needs an update).
- VS Code Workspace Trust is blocking the extension.

**Fix:** Enable Kickbacks in the status bar. Update both Claude Code and Kickbacks to the latest versions. Ensure VS Code trusts the workspace.

### Auto-Update Failures

Kickbacks auto-updates silently. If updates stop:
1. Check if VS Code's auto-update setting is enabled.
2. Reinstall from the marketplace.
3. Verify you haven't pinned the extension to a specific version.

> **Case: Version Pinning** (Product): A user pinned Kickbacks to v1.0.0 for "stability" but missed security and compatibility patches. After 3 weeks, the pinned version stopped working with Claude Code's v2.3 update. Solution: unpin and allow auto-updates.

## Privacy Concerns

**Common misconception:** "The extension reads my code or prompts to show relevant ads."

**Reality:** Kickbacks never reads code, prompts, or completions. The ad selection is server-side, based only on bid priority and available inventory. The extension only reads the position of the spinner text to know where to insert the ad line.

### Uninstall Process

1. Click "Kickbacks: Off" in the status bar.
2. Open VS Code Extensions panel (Cmd+Shift+X).
3. Find "Kickbacks.ai" in your installed extensions.
4. Click the gear icon → "Uninstall".
5. (Optional) Reload window to ensure complete removal.
