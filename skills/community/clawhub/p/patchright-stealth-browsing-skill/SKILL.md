---
name: patchright-stealth-browsing-skill
description: Perform stealth browser automation to bypass bot detection (Cloudflare, Akamai, Datadome) using Patchright.
version: 2.1.1
metadata:
  openclaw:
    emoji: "🕵️"
    requires:
      bins:
        - node
      mcp:
        - patchright_navigation
        - patchright_interaction
        - patchright_session
        - patchright_execution
---

# Patchright Stealth Browsing Skill

> [!IMPORTANT]
> **Hard Dependency Warning:**
> This skill is **strictly dependent** on the `patchright-mcp` server. It **will not work** unless the `patchright-mcp` server is correctly installed, configured, and running in the OpenClaw environment.
>
> **Repository Access:**
> The `patchright-mcp` server repository is **private**. Accessing, cloning, and managing the server requires proper authentication credentials and repository privileges.

This skill enables the OpenClaw agent to automate browser interactions stealthily on websites protected by active anti-bot systems (e.g., Cloudflare, Akamai, Datadome). It runs over the `patchright-mcp` server, which uses a patched Chromium browser.

The browser capabilities are consolidated into **four core tools**:
1. `patchright_navigation`: Manages page lifecycle, navigation, HTML content retrieval, and screenshot captures.
2. `patchright_interaction`: Executes clicks, text typing, option selections, scrolling, global keys, and elements synchronization.
3. `patchright_session`: Handles reading, writing, and clearing context cookies, as well as named profiles.
4. `patchright_execution`: Evaluates page scripts and extracts structured interactive element snapshots.

---

## Guidelines for the Agent

1. **Sequential Lifecycle Management**:
   - Begin by navigating directly using `patchright_navigation` with action `navigate` and the target `url`.
   - Always finish execution by calling `patchright_navigation` with action `close` to safely release the browser process and memory.

2. **Stealth Interaction Flow**:
   - To interact with a page, first get the structure using `patchright_execution` with action `snapshot`. This extracts all visible interactive elements (buttons, links, inputs) along with their CSS selectors.
   - Use the retrieved selectors to trigger clicks, hovers, or inputs via `patchright_interaction`.

3. **Performance Optimization (Bulk Fill)**:
   - When filling forms with multiple inputs, **do not** call `fill` repeatedly. Instead, use `patchright_interaction` with action `bulk_fill` and pass the list of fields in the `items` array. This reduces roundtrips and handles fallback evaluations automatically.

4. **Synchronizations and Waits**:
   - If pages load elements dynamically, synchronize using `patchright_interaction` with action `wait_for` targeting the element's selector and expected state (`visible`, `hidden`, `attached`, or `detached`).

5. **Visual Validation**:
   - Capture screenshots using `patchright_navigation` with action `screenshot` after major actions (like form submissions or clicks) to verify the visual state of the page.

6. **Authentication & Session Reuse**:
   - Use `patchright_session` with action `get_cookies` to save authentication state, and `set_cookies` to restore sessions without needing to re-login.

7. **Multi-Page & Tab Targeting**:
   - Multiple tabs can be targeted using the optional `pageIndex` parameter (zero-based index) available in navigation, interaction, and execution tools.
   - List active tabs with `patchright_navigation` (action `list_pages`) and select the target tab using `pageIndex` instead of performing profile switches.

8. **Video Recording & Verification**:
   - To record interaction videos, set the `recordVideo: true` flag in the `open` or `navigate` actions. 
   - Videos are saved as WebM files in `~/videos`.
   - Use `patchright_navigation` with action `close_page` to finalize the video for a specific tab, or call `list_videos` to retrieve the paths of recorded files.

9. **Dynamic Proxy Configuration & Rotation**:
   - Pass proxy parameters (`proxyServer`, `proxyBypass`, `proxyUsername`, `proxyPassword`) inside the `open`, `navigate`, or `create_profile` actions to route traffic.
   - To rotate proxies dynamically, pass the new `proxyServer` parameter in subsequent calls; the server will automatically recreate the context with the new proxy.
   - Omit proxy parameters to continue using the active proxy of the context.
   - To explicitly clear/remove the proxy and restore system/direct routing, call the `open` action without proxy parameters.

10. **Custom Client Configurations**:
    - You can dynamically override browser launch settings by passing parameters such as `headless`, `userAgent`, `viewport` (e.g. `{ "width": 800, "height": 600 }`), and `deviceScaleFactor` to the `open` or `navigate` actions inside `patchright_navigation`.
    - Use these overrides to simulate different device types (mobile/desktop viewports) or rotate user agents to prevent fingerprint-based blockings.

---

## Edge Cases and Failure Handling

1. **Element Selector Timeouts**:
   - If an interaction (e.g., `click`, `fill`) fails due to a timeout, verify if the element is loaded by calling `patchright_interaction` with action `wait_for` and state `visible`.
   - If an element is hidden or obstructed by a modal, use `patchright_execution` with action `evaluate` to trigger a native JS click: `document.querySelector('selector').click()`.

2. **Isolated Context Variable Sharing**:
   - Remember that `evaluate` scripts execute in an isolated context (utility world) for anti-bot stealth.
   - If you need to verify or set properties on the page's main execution context, store them as custom DOM attributes (e.g., `element.setAttribute('data-state', 'value')`) rather than attaching them directly to `window.propertyName`.

3. **Anti-bot Block Pages / CAPTCHAs**:
   - If you encounter a CAPTCHA or blocker page, do not repeat failing navigation commands.
   - Run `patchright_navigation` with action `screenshot` to verify if a challenge is present.
   - If a challenge page appears, instruct the user or wait for manual solver actions, rather than retrying automated scripts recursively.

4. **CDP Connection Disconnects**:
   - If the remote CDP port `9222` falls back to a subprocess launch, verify if the process crashed by retrying `open`. The server automatically spins up a local fallback browser if the remote socket is unresponsive.
