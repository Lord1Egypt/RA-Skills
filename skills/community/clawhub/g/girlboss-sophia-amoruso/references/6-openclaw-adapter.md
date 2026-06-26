# OpenClaw/Hermes Adapter — Running Spinner Ads on Agent Platforms

> Source: Direct code analysis of Kickbacks v0.3.174 injection mechanism, OpenClaw Gateway architecture, and agent platform comparison.

## Why This Matters

Kickbacks currently works on VS Code-hosted AI tools (Claude Code, Codex) because those tools render a DOM-based spinner in a webview. The injection strategy is **file-system patching** — replacing text in the tool's install directory before it loads.

But agent platforms are a much bigger surface:
- **OpenClaw** — Gateway + TUI + WebChat (native SwiftUI) + Menu Bar
- **Hermes** — Terminal-based agent with streaming responses
- **ClawHub** — Agent skill marketplace with reply routing

Each platform has its own "waiting zone." The question is: **how do we put an ad there?**

---

## The Kickbacks Injection Pattern (For Reference)

Kickbacks' current injection works in 4 steps:

### Step 1: Locate the Target
```typescript
// adapter.ts — locateClaudeCode() finds installation directory
const base = locateClaudeCode();      // ~/.vscode/extensions/anthropic.claude-code-*/
const webviewDir = join(base, "webview");
```

### Step 2: Patch the CSP
```typescript
// adapter.ts — insert loopback connect-src
// Finds: default-src 'none'; ${p}
// Replaces: default-src 'none'; connect-src http://127.0.0.1:*; ${p}
// This lets the ad block fetch metrics to a local HTTP server
```

### Step 3: Inject the Ad Block
```typescript
// adapter.ts — append 67KB self-contained JS to webview/index.js
const block = resolveAsset("claude-code", "block.asset.js");
// Fill template vars: __VIBE_ADS_AD__, __VIBE_ADS_TIER__, etc.
writeFileSync(targetIndex, cleanOriginal + filledBlock);
```

### Step 4: Run the Loopback Server
```typescript
// loopback.ts — local HTTP server for impression/click telemetry
const server = createServer((req, res) => {
  // GET /vibe-ads/<token>/impression  → records view
  // GET /vibe-ads/<token>/click        → records click + redirects
});
```

### What This Means for Other Platforms

The core insight: **you need a place to inject text + a way to track views/clicks.** If the platform has either a DOM webview or a CLI output line, you can inject. If it has neither, you need a different approach.

---

## OpenClaw Adapter Strategies

OpenClaw has no webview and no DOM. Its interfaces are:
- **TUI** (terminal, text-based)
- **WebChat** (native SwiftUI app)
- **Menu Bar** (macOS native)
- **Gateway** (WebSocket events, the "brain")

Here are 3 strategies to run spinner ads on OpenClaw, from simplest to most powerful:

---

### Strategy A: Gateway Sponsor Line (Simplest)

**Where:** The agent's "thinking" status indicator in the Menu Bar and TUI.

**How it works:**
When OpenClaw sends a `chat.send` and the model is processing, the Gateway emits activity events:
```json
{
  "type": "activity",
  "state": "started",
  "kind": "llm_thinking"
}
```

**The injection:**
Add an optional `sponsor` field to the activity event:
```json
{
  "type": "activity",
  "state": "started",
  "kind": "llm_thinking",
  "sponsor": {
    "text": "Ramp · save time and money",
    "url": "https://ramp.com",
    "tracking": {
      "impression": "https://kickbacks.ai/v/imp/<token>",
      "click": "https://kickbacks.ai/v/click/<token>"
    }
  }
}
```

**Where it shows:**
- **TUI:** Right after the tool execution line: `🛠️ Exec: thinking…  [Sponsor: Ramp · save time and money]`
- **Menu Bar:** The status row text becomes `Main · thinking [Ramp · save time and money]`
- **WebChat:** The "thinking" indicator becomes `OpenClaw is thinking… [Sponsor: Ramp]`

**Implementation complexity:** ⭐ (1/5)
- One field added to Gateway activity event payload
- TUI/WebChat/Menu Bar each render the field in their existing status area
- No file patching, no DOM

**Pros:**
- Works across all OpenClaw interfaces
- No hacky file injection
- Gateway-native (plugins can add it)

**Cons:**
- Less visible than Kickbacks (status text, not front-and-center)
- Only visible during model thinking (sub-second to seconds)
- No animated spinner to hijack

---

### Strategy B: TUI Activity Overlay (Medium)

**Where:** The TUI's tool execution lines — the most actively watched area.

**How it works:**
OpenClaw's TUI shows tool execution lines like:
```
🛠️ Exec: search "book-skills" (running)
🛠️ Read: /tmp/results.json (running)
🛠️ Write: /tmp/output.md (running)
```

Each of these renders with a "(running)" suffix and eventually replaces with the result.

**The injection:**
Replace the "(running)" text with a sponsored line that stays visible during execution:
```
🛠️ Exec: search "book-skills"  →  [Ramp — save time and money · ramp.com]  (2.3s)
```

**How to implement:**
This is essentially the same as Kickbacks — but instead of `querySelector('[class*="spinnerRow_"]')`, we hook into the TUI's tool rendering pipeline.

In the TUI component code:
```typescript
// tui/components/tool-display.ts (simplified)
renderStatusLine(toolName: string, elapsed: number, sponsor?: Sponsor) {
  if (sponsor && elapsed > 0) {
    return `${toolName}  →  [${sponsor.text} · ${sponsor.url}]  (${elapsed}s)`;
  }
  return `${toolName} (running)`;
}
```

**Tracking:**
The TUI or Gateway can `fetch` impression/click endpoints — same loopback architecture as Kickbacks, just no browser DOM involved.

**Implementation complexity:** ⭐⭐ (2/5)
- Modify TUI tool rendering (open-source, well-structured)
- Add Gateway event for sponsor data
- Backend for impression/click tracking

**Pros:**
- Much more visible than A — right in the user's focus zone
- Feels natural — the "waiting" text IS the ad, like Kickbacks
- Terminal-native, no webview needed

**Cons:**
- Only works in TUI (not WebChat/Menu Bar)
- Requires TUI code changes

---

### Strategy C: WebChat Thinking Widget + ClawHub Integration (Most Powerful)

**Where:** The WebChat UI and the ClawHub skill reply flow — the "always-on" surfaces.

**How it works:**
This combines two approaches:

**C1: WebChat Thinking Widget**
WebChat's "OpenClaw is thinking…" indicator (visible when model is processing) gets a small sponsored text badge that shows during processing and collapses when the reply arrives.

**C2: ClawHub Reply Watermark as Default Advertiser**
Every ClawHub skill reply already has a watermark:
```
*Generated by [Heardly App](https://www.heard.ly) — turning books into knowledge you can Listen and Execute.*
```

**The strategy: own the watermark.**
Instead of waiting for an advertiser to bid, **we are the default advertiser.** Every ClawHub reply carries our brand. If anyone else wants that slot, they bid for it — and we make money from their bids.

This is the "default advertiser" model:
1. We launch first → occupy the watermark slot
2. We define the format standard → watermark with link + tracking
3. We open a bid market → advertisers compete for the slot
4. We earn from every bid → platform operator + default advertiser dual role

**Implementation complexity:** ⭐⭐⭐ (3/5)
- Watermark system already exists (Heardly skills use it)
- Need: bid marketplace backend + impression tracking + payout system
- Need: WebChat widget extension (optional)

**Pros:**
- We own the slot before anyone else
- Revenue from advertiser bids (we don't even need our own ads)
- Scales to entire ClawHub ecosystem
- WebChat + TUI + Menu Bar simultaneously

**Cons:**
- Requires bid marketplace infrastructure
- Needs advertiser onboarding
- "Ad platform" positioning must be careful (privacy, user experience)

---

## Default Advertiser Blueprint

This is the playbook for becoming the default advertiser on any agent platform:

### Phase 1: Occupy the Slot (Week 1)
- ✅ Deploy watermark on all ClawHub skills (Heardly App brand)
- ✅ Standardize watermark format (link + tracking token)
- ✅ Track impressions across all skills

### Phase 2: Define the Standard (Week 2-3)
- [ ] Publish OpenClaw Gateway Plugin: "Sponsor Line" event extension
- [ ] Add `sponsor` field to activity events (Strategy A)
- [ ] Build TUI tool-line overlay (Strategy B)
- [ ] Document the adapter pattern for other platforms

### Phase 3: Open the Market (Month 1-2)
- [ ] Launch bid marketplace (self-serve, minimum $1/1,000 impressions)
- [ ] Advertiser onboarding flow (web form → bid queue → live)
- [ ] Revenue dashboard for developers (same 50/50 model as Kickbacks)
- [ ] Payout system (Stripe Connect)

### Phase 4: Scale (Month 3+)
- [ ] Hermes adapter (terminals, TUI-like overlay)
- [ ] More agent platforms (ACP protocol, Model Context Protocol)
- [ ] Programmatic bidding API
- [ ] Multi-platform impression aggregation

---

## Platform Compatibility Matrix

| Platform | Injection Surface | Adapter Strategy | Difficulty |
|---|---|---|---|
| **Claude Code (VS Code)** | Webview DOM spinner | File patch + loopback | ✅ Solved (Kickbacks) |
| **Codex (VS Code)** | Webview DOM shimmer | File patch + loopback | ✅ Solved (Kickbacks) |
| **Claude Code (CLI)** | ~/.claude/settings.json statusLine + spinnerVerbs | Config patch | ✅ Solved (Kickbacks) |
| **OpenClaw TUI** | Tool execution lines | B: Activity Overlay | ⭐⭐ Medium |
| **OpenClaw WebChat** | Thinking indicator | C1: Thinking Widget | ⭐⭐ Medium |
| **OpenClaw Menu Bar** | Status row text | A: Sponsor Line | ⭐ Easy |
| **Hermes (terminal)** | Streaming response line | B-like: Terminal overlay | ⭐⭐ Medium |
| **ClawHub Skills** | Reply watermark | C2: Watermark as default advertiser | ⭐⭐ Medium |
| **ACP (Agent-to-Agent)** | Protocol events | Custom sponsor event in spec | ⭐⭐⭐ Hard |

---

## How We Become the Default Advertiser

**We don't ask for permission. We occupy the slot.**

1. **Watermarks first** — Every Heardly ClawHub skill already carries our brand in its reply watermark. This is the beachhead.

2. **Gateway plugin next** — Release an OpenClaw Gateway plugin that adds a sponsor field to activity events. We're the first sponsor in the queue.

3. **Open the market** — Once the slot is defined and working, open it to advertisers. We collect platform fees + our own ads get priority placement (default advertiser privilege).

4. **Never use Heardly as the ad brand** — We're the platform. Heardly is just one of many products we own. The ad-slot brand is **Jayson Meng** (or an anonymous platform brand). This keeps the door open for other advertisers who might compete with Heardly.

---

## Technical Reference: Kickbacks Injection Code Walkthrough

For developers implementing platform adapters:

### block.asset.js — The Ad Rendering Block (67 KB)
```javascript
// Key functions:
findSpinner()        // querySelector('[class*="spinnerRow_"]') — find the DOM target
rowActive(row)       // Check if spinner glyph is animating (U+2722 ✢ etc.)
buildAdHtml(tier, s) // Build clickable <a> tag with tier-based formatting
ensureOverlay()      // Create/update the ad overlay DOM element
```

### adapter.ts — The Patch Engine
```typescript
// Critical constants:
VERB_SET               // ["Discombobulating","Flibbertigibbeting","Clauding"…]
CSP_ANCHOR_RE          // /default-src 'none'; (\$\{[a-zA-Z_]\w*\})/
BLOCK_START            // "/* VIBE-ADS-START */"
BLOCK_END              // "/* VIBE-ADS-END */"

// Patch flow:
preflight()            // Check CC version compatibility
install()              // 1. Patch CSP, 2. Inject block, 3. Write settings.json
uninstall()            // 1. Remove block, 2. Restore CSP, 3. Restore settings.json
```

### loopback.ts — Telemetry Server
```typescript
// Local HTTP server with VS Code asExternalUri tunnel
// GET /vibe-ads/<token>/impression  → 200 OK + metrics record
// GET /vibe-ads/<token>/click       → 302 Redirect to CLICKURL + metrics record
```

---

## FAQ: Agent Platform Advertising

**Q: Can I just copy-paste Kickbacks' injection code into OpenClaw?**
A: No. Kickbacks relies on DOM manipulation inside a VS Code webview. OpenClaw has no DOM — it uses terminal rendering (TUI) and native SwiftUI (WebChat). Use strategies A/B/C instead.

**Q: How much can I earn from agent platform ads vs. Claude Code ads?**
A: Too early to compare. Claude Code has a large install base with heavy daily usage, making spinner impressions frequent. Agent platform impressions depend on adoption — but ClawHub skills get a steady stream of queries from any agent that invokes them.

**Q: What if Kickbacks itself expands to OpenClaw?**
A: That's competition. But by being the default advertiser first, we define the format and capture the platform revenue before anyone else enters.

**Q: How do I track impressions without a browser DOM?**
A: Same as Kickbacks' loopback server — a local HTTP endpoint that receives GET requests for impressions/clicks. In TUI/CLI contexts, a Node.js or Python HTTP server handles it. No browser needed.

**Q: Is this privacy-safe like Kickbacks?**
A: Yes. The injection only touches the "waiting state" text — never code, prompts, or model responses. Tracking is anonymous impression/click counts, same model as Kickbacks.

**Q: Can I run multiple ad slots across different agent platforms simultaneously?**
A: Yes. The adapter architecture is independent per platform. You can be the default advertiser on ClawHub while also running ads on Claude Code via Kickbacks.
